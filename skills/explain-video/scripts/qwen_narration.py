"""Cache local English paragraph speech and align its known script with local ASR.

Apple silicon + MLX-Audio. All model paths are explicit. No downloads or cloud
fallback. Run --help without installing the optional synthesis dependencies.
"""

import argparse
import difflib
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import wave

SMALL = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
    'sixteen', 'seventeen', 'eighteen', 'nineteen',
]
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
DEFAULT_DIRECTION = (
    'Speak in British English as a mature male documentary narrator, with a '
    'warm, resonant lower register. Use an unhurried, measured pace, quiet '
    'curiosity, precise diction, gentle emphasis and natural pauses between '
    'ideas. Keep the sentences connected and avoid theatrical or promotional delivery.'
)


def number(value):
    value = int(value)
    if value < 20:
        return SMALL[value]
    if value < 100:
        return TENS[value // 10] + (' ' + SMALL[value % 10] if value % 10 else '')
    if value < 1000:
        return SMALL[value // 100] + ' hundred' + (' ' + number(value % 100) if value % 100 else '')
    if value < 1000000:
        return number(value // 1000) + ' thousand' + (' ' + number(value % 1000) if value % 1000 else '')
    return ' '.join(SMALL[int(c)] for c in str(value))


def canonical(text):
    def expand(match):
        value = match[0]
        if '.' not in value:
            return number(value)
        whole, fraction = value.split('.')
        prefix = number(whole) + ' ' if whole and int(whole) else ''
        return prefix + 'point ' + ' '.join(SMALL[int(c)] for c in fraction)

    text = re.sub(r'(?<![a-z])(?:\d+\.\d+|\.\d+|\d+)', expand, text.lower())
    return re.findall(r'[a-z]+', text.replace('nonzero', 'non zero'))


def load_cues(path, limit=None):
    cues = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(cues, list) or not cues:
        raise ValueError('Provide a nonempty JSON list of {id, text}.')
    for cue in cues:
        if not isinstance(cue, dict):
            raise ValueError('Each cue must be an object.')
        if not isinstance(cue.get('id'), str) or not re.fullmatch(r'[A-Za-z0-9_-]+', cue['id']):
            raise ValueError('Cue IDs must contain only letters, digits, hyphens and underscores.')
        if not isinstance(cue.get('text'), str) or not canonical(cue['text']):
            raise ValueError('Each cue needs nonempty English text.')
        validate_bookmarks(cue['text'], cue.get('bookmarks', {}))
    if len({cue['id'] for cue in cues}) != len(cues):
        raise ValueError('Cue IDs must be unique.')
    if limit is not None and limit < 1:
        raise ValueError('--limit must be positive.')
    return cues[:limit] if limit is not None else cues


def validate_bookmarks(text, bookmarks):
    """Find unique script phrases before spending time on synthesis."""
    if not isinstance(bookmarks, dict):
        raise ValueError('Bookmarks must map names to unique phrases in the cue text.')
    tokens, spans = canonical(text), {}
    for name, phrase in bookmarks.items():
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', name):
            raise ValueError('Bookmark names use letters, digits, hyphens and underscores.')
        needle = canonical(phrase) if isinstance(phrase, str) else []
        matches = [i for i in range(len(tokens) - len(needle) + 1)
                   if needle and tokens[i:i + len(needle)] == needle]
        if len(matches) != 1:
            raise ValueError(f'Bookmark {name!r} must match exactly one script phrase; found {len(matches)}.')
        spans[name] = (matches[0], matches[0] + len(needle))
    return spans


def cache_key(identity):
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:24]


def speech_identity(text, settings):
    # Stable when a cue is renamed, moved, or preceded by a newly inserted cue.
    seed = int(hashlib.sha256(f"{settings['seed']}:{text}".encode()).hexdigest()[:8], 16)
    return {'text': text, 'settings': settings, 'cue_seed': seed, 'cache_version': 2}


def alignment_identity(speech_key, audio_hash, settings):
    return {'speech_key': speech_key, 'audio_sha256': audio_hash, 'settings': settings}


def file_digest(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    staged = path.with_suffix(path.suffix + '.next')
    staged.write_text(json.dumps(value, indent=2) + '\n')
    staged.replace(path)


def model_identity(directory):
    """Content fingerprint, not a machine-specific directory name or mtime."""
    if not directory.is_dir():
        raise ValueError('Pass an existing local model directory.')
    extensions = {'.safetensors', '.json', '.txt', '.model', '.bin', '.tiktoken', '.npz', '.onnx'}
    files = sorted(p for p in directory.rglob('*') if p.is_file()
                   and p.suffix in extensions
                   and not any(part.startswith('.') for part in p.relative_to(directory).parts))
    if not files:
        raise ValueError('The local model directory has no recognized model/config files.')
    digest = hashlib.sha256()
    for path in files:
        file_hash = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                file_hash.update(block)
        digest.update(json.dumps([path.relative_to(directory).as_posix(), file_hash.hexdigest()]).encode())
    return {'sha256': digest.hexdigest(), 'files': len(files)}


def word_alignment(text, words, seconds):
    """Map known script words to ASR times; missing words remain estimates."""
    tokens = canonical(text)
    observed, times = [], []
    for index, word in enumerate(words):
        # Whisper can emit both a redundant zero and a decimal fragment.
        if word['word'].strip() == '0' and index + 1 < len(words) and words[index + 1]['word'].lstrip().startswith('.'):
            continue
        if not (0 <= word['start'] <= word['end'] <= seconds + .15):
            raise ValueError('Invalid ASR word timing; inspect the saved alignment.')
        for token in canonical(word['word']):
            observed.append(token)
            times.append((word['start'], word['end']))
    matcher = difflib.SequenceMatcher(None, tokens, observed, autojunk=False)
    mapping = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            mapping[block.a + offset] = block.b + offset
    ratio = 2 * len(mapping) / max(1, len(tokens) + len(observed))
    if ratio < .86:
        raise ValueError(f'Low speech/script agreement: {ratio:.3f}; inspect saved audio and ASR.')

    def boundary(index, end=False):
        if index in mapping:
            return times[mapping[index]][int(end)]
        left = max((i for i in mapping if i < index), default=None)
        right = min((i for i in mapping if i > index), default=None)
        if left is None:
            return times[mapping[right]][0] if right is not None else 0
        if right is None:
            return times[mapping[left]][1]
        a, b = times[mapping[left]][1], times[mapping[right]][0]
        return a + (b - a) * (index - left) / (right - left)

    differences = [
        {'source': ' '.join(tokens[a:b]), 'heard': ' '.join(observed[c:d])}
        for op, a, b, c, d in matcher.get_opcodes() if op != 'equal'
    ]
    agreement = {
        'agreement': round(ratio, 5), 'heard_text': ' '.join(w['word'].strip() for w in words),
        'differences': differences, 'source_word_count': len(tokens),
        'recognized_word_count': len(observed),
    }
    return boundary, agreement


def align(text, words, seconds):
    """Estimate sentence boundaries; do not replace the script with ASR text."""
    boundary, agreement = word_alignment(text, words, seconds)
    sentences, offset = [], 0
    for chunk in re.split(r'(?<=[.!?])\s+', text.strip()):
        count = len(canonical(chunk))
        if not count:
            raise ValueError('A sentence contains no alignable English words.')
        start = max(0, min(seconds, boundary(offset)))
        finish = min(seconds, max(start + .04, boundary(offset + count - 1, True)))
        if not math.isfinite(start + finish) or finish <= start:
            raise ValueError('Invalid sentence timing; inspect the saved alignment.')
        sentences.append({'text': chunk, 'start': round(start, 4), 'end': round(finish, 4)})
        offset += count
    if any(a['end'] > b['start'] + .15 for a, b in zip(sentences, sentences[1:])):
        raise ValueError('Overlapping sentence timing; inspect the saved alignment.')
    return sentences, agreement


def resolve_landmarks(text, words, seconds, bookmarks):
    spans = validate_bookmarks(text, bookmarks)
    if not spans:
        return {}
    boundary, _ = word_alignment(text, words, seconds)
    landmarks = {}
    for name, (start, end) in spans.items():
        a, b = boundary(start), boundary(end - 1, True)
        if not (math.isfinite(a + b) and 0 <= a < b <= seconds):
            raise ValueError(f'Invalid timing for bookmark {name!r}; inspect the alignment.')
        landmarks[name] = {'start': round(a, 4), 'end': round(b, 4)}
    return landmarks


def check_wav(path):
    with wave.open(str(path), 'rb') as audio:
        if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) != (1, 2, 44100):
            raise ValueError('Expected mono PCM16 audio at 44.1 kHz.')
        return audio.getnframes() / audio.getframerate()


def generate(args):
    cues = load_cues(args.script, args.limit)
    if not shutil.which('ffmpeg'):
        raise ValueError('Install ffmpeg before synthesis.')
    tts_identity = model_identity(args.model_path)
    asr_identity = model_identity(args.asr_path)
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
    import numpy as np
    import soundfile as sf

    tts_settings = {
        'engine': 'mlx-audio', 'version': importlib.metadata.version('mlx-audio'),
        'model': 'Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16', 'model_identity': tts_identity,
        'speaker': args.speaker, 'language': 'English', 'instruct': args.instruct,
        'temperature': .7, 'top_p': 1., 'top_k': 50, 'repetition_penalty': 1.05,
        'max_tokens': 1800, 'seed': 731, 'synthesis_unit': 'complete cue paragraph',
    }
    asr_settings = {
        'asr_identity': asr_identity, 'asr_version': importlib.metadata.version('faster-whisper'),
        'alignment_version': 5, 'asr_prompt': args.asr_prompt, 'language': 'en',
        'beam_size': 5, 'word_timestamps': True, 'condition_on_previous_text': False,
        'vad_filter': False, 'temperature': 0, 'compute_type': 'int8',
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    model = asr = None
    segments, begun = [], time.monotonic()
    for cue in cues:
        identity = speech_identity(cue['text'], tts_settings)
        speech_key = cache_key(identity)
        directory = args.out_dir / 'speech' / speech_key
        directory.mkdir(parents=True, exist_ok=True)
        wav, metadata = directory / 'speech.wav', directory / 'synthesis.json'
        speech_cached = wav.is_file() and metadata.is_file()
        if speech_cached:
            stats = json.loads(metadata.read_text())
            if (stats['identity'] != identity or file_digest(wav) != stats['audio_sha256']
                    or abs(check_wav(wav) - stats['seconds']) > 1 / 44100):
                raise ValueError('Speech cache differs from its identity/audio; preserve it for inspection.')
        else:
            if wav.exists() or metadata.exists():
                raise ValueError('Incomplete speech cache; preserve it for inspection before retrying.')
            import mlx.core as mx
            if model is None:
                from mlx_audio.tts.utils import load_model
                print(json.dumps({'loading_local_model': True}), flush=True)
                model = load_model(str(args.model_path))
            mx.random.seed(identity['cue_seed'])
            tick = time.monotonic()
            results = list(model.generate_custom_voice(
                text=cue['text'], speaker=args.speaker, language='English',
                instruct=args.instruct, stream=False, temperature=tts_settings['temperature'],
                top_p=tts_settings['top_p'], top_k=tts_settings['top_k'],
                repetition_penalty=tts_settings['repetition_penalty'],
                max_tokens=tts_settings['max_tokens'], verbose=False,
            ))
            if len(results) != 1:
                raise ValueError('Expected one complete paragraph, not sentence stitching.')
            result = results[0]
            samples, native_rate = np.asarray(result.audio, dtype=np.float32), result.sample_rate
            if result.token_count >= tts_settings['max_tokens'] - 1:
                raise ValueError('Generation reached its token cap; inspect the paragraph length.')
            if samples.ndim != 1 or len(samples) <= native_rate or not np.isfinite(samples).all() or np.sqrt(np.mean(samples ** 2)) <= .005:
                raise ValueError('Speech is too short, invalid, or near-silent.')
            if np.max(np.abs(samples)) > .99:
                samples *= .99 / np.max(np.abs(samples))
            sf.write(str(directory / 'native.wav'), samples, native_rate, subtype='PCM_16')
            staged = directory / 'speech.next.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(directory / 'native.wav'),
                            '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', str(staged)], check=True)
            staged.replace(wav)
            stats = {'identity': identity, 'audio_sha256': file_digest(wav), 'seconds': check_wav(wav),
                     'synthesis_seconds': round(time.monotonic() - tick, 3),
                     'tokens': result.token_count, 'peak_memory_GB': result.peak_memory_usage}
            write_json(metadata, stats)

        seconds = stats['seconds']
        alignment = alignment_identity(speech_key, stats['audio_sha256'], asr_settings)
        align_dir = args.out_dir / 'alignments' / cache_key(alignment)
        align_dir.mkdir(parents=True, exist_ok=True)
        align_meta, words_path = align_dir / 'segment.json', align_dir / 'asr-words.json'
        alignment_cached = align_meta.is_file() and words_path.is_file()
        if alignment_cached:
            value = json.loads(align_meta.read_text())
            words = json.loads(words_path.read_text())
            if value['identity'] != alignment or file_digest(words_path) != value['words_sha256']:
                raise ValueError('Alignment cache differs from its identity/words; preserve it for inspection.')
        else:
            if asr is None:
                from faster_whisper import WhisperModel
                asr = WhisperModel(str(args.asr_path), device='cpu', compute_type='int8',
                                   cpu_threads=6, local_files_only=True)
            pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(wav), '-ar', '16000',
                                           '-ac', '1', '-f', 'f32le', '-'])
            recognized, _ = asr.transcribe(
                np.frombuffer(pcm, dtype=np.float32), language='en', beam_size=5,
                word_timestamps=True, condition_on_previous_text=False, vad_filter=False,
                temperature=0, initial_prompt=args.asr_prompt,
            )
            words = [{'word': w.word, 'start': w.start, 'end': w.end, 'probability': w.probability}
                     for segment in recognized for w in (segment.words or [])]
            write_json(words_path, words)
            sentences, agreement = align(cue['text'], words, seconds)
            value = {'text': cue['text'], 'seconds': seconds, 'sentences': sentences,
                     'agreement': agreement, 'identity': alignment, 'words_sha256': file_digest(words_path)}
            write_json(align_meta, value)
        cached = speech_cached and alignment_cached
        segments.append({'id': cue['id'], 'text': cue['text'], 'path': str(wav.resolve()),
                         'seconds': value['seconds'], 'sentences': value['sentences'],
                         'agreement': value['agreement'], 'cached': cached,
                         'speech_cached': speech_cached, 'alignment_cached': alignment_cached,
                         'landmarks': resolve_landmarks(cue['text'], words, seconds, cue.get('bookmarks', {})),
                         'synthesis_seconds': stats['synthesis_seconds']})
        print(json.dumps({'cue': cue['id'], 'seconds': round(value['seconds'], 3),
                          'agreement': value['agreement']['agreement'], 'cached': cached,
                          'speech_cached': speech_cached, 'alignment_cached': alignment_cached}), flush=True)
    manifest = {
        'provider': 'Qwen3-TTS (local MLX)', 'model': tts_settings['model'], 'voice_id': args.speaker,
        'settings': {'speech': tts_settings, 'alignment': asr_settings},
        'segments': segments, 'elapsed_seconds': round(time.monotonic() - begun, 3),
        'cloud_synthesis_requests': 0,
        'timing': 'ASR-estimated word timestamps aligned to the known script; sentence boundaries approximate.',
    }
    target = args.out_dir / ('sample-manifest.json' if args.limit else 'manifest.json')
    write_json(target, manifest)
    print(json.dumps({'done': True, 'cues': len(segments), 'manifest': str(target)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--model-path', type=Path, required=True)
    parser.add_argument('--asr-path', type=Path, required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--speaker', default='Ryan')
    parser.add_argument('--instruct', default=DEFAULT_DIRECTION)
    parser.add_argument('--asr-prompt', default='Clear English technical narration.')
    try:
        generate(parser.parse_args())
    except (ValueError, ImportError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
