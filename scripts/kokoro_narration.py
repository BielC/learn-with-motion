"""Cached local Kokoro narration with measured sentence and cue boundaries.

Accepts the same [{id, text}] script as elevenlabs_narration.py. Requires
kokoro-onnx==0.5.0, soundfile, numpy, ffmpeg, and explicit local model files.
No credentials, network calls, model downloads, or cloud fallback.
"""

import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import re
import subprocess
import time
import wave


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def duration(path):
    with wave.open(str(path), 'rb') as source:
        if (source.getnchannels(), source.getsampwidth(), source.getframerate()) != (1, 2, 44100):
            raise ValueError(f'Expected 44.1 kHz mono PCM16: {path.name}')
        return source.getnframes() / source.getframerate()


def generate(args):
    import numpy as np
    import soundfile as sf
    from kokoro_onnx import Kokoro

    cues = json.loads(args.script.read_text())
    if not isinstance(cues, list) or not cues:
        raise ValueError('Provide a nonempty JSON list of {id, text}.')
    for cue in cues:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', cue.get('id', '')) or not cue.get('text', '').strip():
            raise ValueError('Cue IDs must be simple and text must be nonempty.')
    if len({cue['id'] for cue in cues}) != len(cues):
        raise ValueError('Cue IDs must be unique.')
    if not math.isfinite(args.speed) or not 0.5 <= args.speed <= 2:
        raise ValueError('Speed must be between 0.5 and 2.')
    if not args.model_path.is_file() or not args.voices_path.is_file():
        raise ValueError('Pass existing local Kokoro ONNX model and voices files.')

    settings = {'engine': 'kokoro-onnx', 'version': importlib.metadata.version('kokoro-onnx'),
                'model_sha256': digest(args.model_path), 'voices_sha256': digest(args.voices_path),
                'voice': args.voice, 'language': args.language, 'speed': args.speed,
                'sentence_gap': 0.12, 'sample_rate': 44100, 'schema': 1}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    model = None
    segments = []
    generated = 0
    for cue in cues:
        fingerprint = hashlib.sha256(json.dumps({**settings, 'text': cue['text']}, sort_keys=True).encode()).hexdigest()[:24]
        directory = args.out_dir / fingerprint
        directory.mkdir(exist_ok=True)
        audio, metadata = directory / 'speech.wav', directory / 'segment.json'
        cached = audio.is_file() and metadata.is_file()
        if cached:
            result = json.loads(metadata.read_text())
            if abs(duration(audio) - result['seconds']) > 1 / 44100:
                raise ValueError('Cached audio duration differs from its metadata; preserve it for inspection.')
        else:
            if model is None:
                model = Kokoro(str(args.model_path), str(args.voices_path))
            if args.voice not in model.voices:
                raise ValueError(f'Voice {args.voice} is not in the supplied voice bundle.')
            chunks = re.split(r'(?<=[.!?])\s+', cue['text'].strip())
            pieces, sentences, cursor = [], [], 0
            sample_rate = None
            for index, text in enumerate(chunks):
                samples, sr = model.create(text, voice=args.voice, speed=args.speed, lang=args.language)
                if samples.size == 0 or not np.isfinite(samples).all() or np.max(np.abs(samples)) < 1e-5:
                    raise ValueError(f'Empty, invalid or silent speech in cue {cue["id"]}.')
                if sample_rate is not None and sample_rate != sr:
                    raise ValueError('Kokoro sample rate changed within a cue.')
                sample_rate = sr
                sentences.append({'text': text, 'start': cursor / sr, 'end': (cursor + len(samples)) / sr})
                pieces.append(samples)
                cursor += len(samples)
                if index < len(chunks) - 1:
                    gap = np.zeros(round(settings['sentence_gap'] * sr), dtype=np.float32)
                    pieces.append(gap)
                    cursor += len(gap)
            native = directory / 'native.wav'
            sf.write(str(native), np.concatenate(pieces), sample_rate, subtype='PCM_16')
            staged = directory / 'speech.next.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(native), '-ar', '44100', '-ac', '1',
                            '-c:a', 'pcm_s16le', str(staged)], check=True)
            staged.replace(audio)
            result = {'seconds': duration(audio), 'sentences': sentences, 'settings': settings}
            metadata.write_text(json.dumps(result, indent=2) + '\n')
            generated += 1
        segments.append({'id': cue['id'], 'text': cue['text'], 'path': str(audio.resolve()),
                         'seconds': result['seconds'], 'sentences': result['sentences'], 'cached': cached})
        print(json.dumps({'cue': cue['id'], 'seconds': round(result['seconds'], 3), 'cached': cached}), flush=True)
    manifest = {'provider': 'Kokoro (local)', 'voice_id': args.voice, 'model': 'Kokoro-82M v1.0',
                'settings': settings, 'characters': sum(len(c['text']) for c in cues), 'segments': segments,
                'generated_cues': generated, 'elapsed_seconds': round(time.monotonic() - started, 3),
                'cloud_synthesis_requests': 0, 'api_credits_used': 0,
                'timing': 'Measured sentence boundaries from separate synthesis; no word alignment claimed.'}
    staged = args.out_dir / 'manifest.json.next'
    staged.write_text(json.dumps(manifest, indent=2) + '\n')
    staged.replace(args.out_dir / 'manifest.json')
    print(json.dumps({k: v for k, v in manifest.items() if k not in ['segments', 'settings']}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--model-path', type=Path, required=True)
    parser.add_argument('--voices-path', type=Path, required=True)
    parser.add_argument('--voice', default='bm_george')
    parser.add_argument('--language', default='en-gb')
    parser.add_argument('--speed', type=float, default=1.0)
    generate(parser.parse_args())


if __name__ == '__main__':
    main()
