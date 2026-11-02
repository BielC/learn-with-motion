"""Generate one continuous, cached ElevenLabs reading and split it at cue boundaries.

Input JSON: [{"id": "intro", "text": "Spoken words."}, ...].
Only the selected script is sent. Credentials stay in the environment/env file.
No balance requests, automatic generation retries, or billing changes.
"""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
import wave


def generate(args):
    cues = json.loads(args.script.read_text())
    if not cues or any(not re.fullmatch(r"[A-Za-z0-9_-]+", c["id"]) or not c["text"].strip() for c in cues):
        raise ValueError("Provide nonempty text and simple, unique cue IDs.")
    if len({c["id"] for c in cues}) != len(cues):
        raise ValueError("Cue IDs must be unique.")
    text = "\n\n".join(c["text"] for c in cues)
    if len(text) > 5000:
        raise ValueError("This single-request helper supports at most 5,000 characters.")
    payload = {
        "text": text, "model_id": args.model, "language_code": args.language,
        "voice_settings": {"stability": 0.5}, "seed": 287,
    }
    fingerprint = hashlib.sha256(json.dumps({"voice": args.voice_id, "payload": payload}, sort_keys=True).encode()).hexdigest()[:20]
    directory = args.out_dir / fingerprint
    directory.mkdir(parents=True, exist_ok=True)
    response_file = directory / "generation.json"
    cached = response_file.is_file()
    if not cached:
        key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not key and args.env_file:
            for line in args.env_file.expanduser().read_text().splitlines():
                name, sep, value = line.strip().removeprefix("export ").partition("=")
                if sep and name.strip() == "ELEVENLABS_API_KEY":
                    key = value.strip().strip("\"'")
                    break
        if not key:
            raise ValueError("Configure ELEVENLABS_API_KEY or pass an explicit --env-file.")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", args.voice_id):
            raise ValueError("Invalid voice ID.")
        request = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}/with-timestamps?output_format=mp3_44100_128",
            data=json.dumps(payload).encode(),
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        print(f"Generating {len(text)} characters in one ElevenLabs request.", flush=True)
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            # HTTP 401 can mean authentication, quota or another provider rejection.
            # Retain only a machine-readable category, never raw bodies or messages.
            status = None
            try:
                detail = json.loads(error.read(16384)).get("detail", {})
                if isinstance(detail, dict):
                    category = detail.get("status") or detail.get("code") or detail.get("type")
                    if isinstance(category, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,80}", category):
                        status = category
            except (ValueError, AttributeError, UnicodeError):
                pass
            failure = {"http_status": error.code, "provider_status": status, "automatic_retry": False}
            (directory / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")
            category_note = f" ({status})" if status else " (provider category unavailable)"
            raise RuntimeError(f"ElevenLabs returned HTTP {error.code}{category_note}; no automatic retry was made.") from None
        except urllib.error.URLError:
            raise RuntimeError("ElevenLabs connection failed; no automatic retry was made.") from None
        staged = directory / "generation.json.next"
        staged.write_text(json.dumps(result))
        staged.replace(response_file)
    result = json.loads(response_file.read_text())
    alignment = result.get("alignment")
    if not alignment or "".join(alignment["characters"]) != text:
        raise ValueError("Original-text alignment unavailable; saved response retained, no regeneration attempted.")
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    if len(starts) != len(text) or len(ends) != len(text) or any(a > b for a, b in zip(starts, ends)):
        raise ValueError("Invalid character timing.")
    mp3, pcm = directory / "continuous.mp3", directory / "continuous.wav"
    mp3.write_bytes(base64.b64decode(result["audio_base64"], validate=True))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(pcm)], check=True)
    with wave.open(str(pcm), "rb") as source:
        rate = source.getframerate()
        frames = source.readframes(source.getnframes())
    duration = len(frames) / (2 * rate)
    offsets, cursor = [], 0
    for cue in cues:
        offsets.append((cursor, cursor + len(cue["text"])))
        cursor += len(cue["text"]) + 2
    # Midpoints of the inter-sentence gaps preserve both neighboring words.
    cuts = [0.0] + [(ends[previous[1] - 1] + starts[current[0]]) / 2 for previous, current in zip(offsets, offsets[1:])] + [duration]
    if any(a >= b for a, b in zip(cuts, cuts[1:])):
        raise ValueError("Cue boundaries are not strictly increasing.")
    segments = []
    for cue, begin, end in zip(cues, cuts, cuts[1:]):
        path = directory / f"{cue['id']}.wav"
        first, last = round(begin * rate), round(end * rate)
        data = frames[first * 2:last * 2]
        with wave.open(str(path), "wb") as target:
            target.setnchannels(1); target.setsampwidth(2); target.setframerate(rate)
            target.writeframes(data)
        segments.append({"id": cue["id"], "path": str(path.resolve()), "seconds": len(data) / (2 * rate)})
    report = {"provider": "ElevenLabs", "voice_id": args.voice_id, "model": args.model,
              "characters": len(text), "cached": cached, "segments": segments}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "segments"}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--voice-id", required=True)
    parser.add_argument("--model", default="eleven_v3")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()
    try:
        generate(args)
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
