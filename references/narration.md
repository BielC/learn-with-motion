# Narration

Preserve a selected voice and provider. The default local recipe uses **Qwen3-TTS BF16 through MLX-Audio on Apple silicon**, with coherent paragraphs and caption alignment afterward. Local synthesis uses no TTS API credits but costs local compute. Models and dependencies must be installed separately; the helpers do not download models or silently fall back to a cloud service. Check hardware, disk and memory before setup. Voice quality and prosody need human judgment.

## Qwen paragraph workflow

The included [scripts/qwen_narration.py](../scripts/qwen_narration.py) accepts a JSON list of `{id, text}`. Synthesize each coherent paragraph continuously, then use local Whisper to estimate sentence timing against the known text. Inspect mismatches around numbers, acronyms and technical terms. A high recognition agreement score does not establish good delivery. Reuse the audio for visual or caption edits.

The tested recipe is MLX-Audio 0.6.3, `mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16`, speaker `Ryan`, English, with `Systran/faster-whisper-small.en` for alignment. The default direction is a warm, measured British documentary delivery; it does not claim to reproduce a specific person. Override `--instruct`, `--speaker`, and `--asr-prompt` when appropriate. This helper supports English narration. For other languages, use a suitable alignment model/workflow explicitly.

Create a Python 3.12 environment on an Apple silicon Mac, install [requirements-qwen.txt](../requirements-qwen.txt), and install FFmpeg separately. With the Hugging Face CLI, explicitly download the model repositories to directories you choose. Review their licenses. Model weights do not belong in the skill repository.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-qwen.txt
hf download mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16 --local-dir ./models/qwen-tts
hf download Systran/faster-whisper-small.en --local-dir ./models/whisper

.venv/bin/python scripts/qwen_narration.py \
  --script examples/narration.json \
  --out-dir ./output/audio \
  --model-path ./models/qwen-tts \
  --asr-path ./models/whisper \
  --speaker Ryan \
  --asr-prompt "Technical narration. Add the topic's technical terms here."
```

If the skill was installed inside an agent's skills directory, resolve these files relative to that skill directory. The surrounding output, virtualenv and model directories can be anywhere suitable on the authoring machine. A short `--limit 1` run produces `sample-manifest.json` for checking a new direction before generating the whole script.

The helper validates cue IDs and existing local paths, rejects clipped/near-silent output, and caches by text, model identity and synthesis/alignment settings. It fingerprints local model artifacts; first use of a large model can therefore take time. Changing the contents of a model directory invalidates that cache identity. Outputs include the script and absolute local audio paths, so keep output manifests private unless reviewed for sharing.

The manifest is `{provider, model, voice_id, settings, segments}`. Each segment includes `{id, text, path, seconds, sentences:[{text,start,end}]}`. Sentence times are ASR estimates, not exact measurements. Derive scene timing from them and deliberate holds, and split subtitles into centered phrases afterward. Review invalid/out-of-range animation landmarks as errors rather than silently mapping them to scene start. Twenty to thirty seconds of useful stillness is acceptable.

## Optional lightweight Kokoro

[scripts/kokoro_narration.py](../scripts/kokoro_narration.py) uses `kokoro-onnx==0.5.0`, NumPy, soundfile, FFmpeg, and explicit local model/voice files. It requires no credentials and makes no downloads or network calls. `bm_george` is one British voice option; Kokoro and ElevenLabs voices with similar names are distinct.

```bash
python scripts/kokoro_narration.py \
  --script examples/narration.json --out-dir ./output/kokoro \
  --model-path ./models/kokoro-v1.0.onnx \
  --voices-path ./models/voices-v1.0.bin \
  --voice bm_george --language en-gb --speed 1.0
```

This helper synthesizes sentences separately and records their boundaries. That can sound disconnected. Prefer coherent paragraph delivery when the chosen engine and alignment workflow support it. Do not switch to sentence stitching merely to obtain convenient timestamps.

## Optional ElevenLabs

Use [scripts/elevenlabs_narration.py](../scripts/elevenlabs_narration.py) only when that cloud provider is explicitly selected and sending the script is authorized. It sends the selected text to ElevenLabs. Read the credential from `ELEVENLABS_API_KEY` or an explicit `--env-file`; never commit credentials, response caches or generated private narration. Choose a voice with `--voice-id` rather than relying on someone else's account configuration.

```bash
python scripts/elevenlabs_narration.py \
  --script examples/narration.json --out-dir ./output/elevenlabs \
  --voice-id YOUR_VOICE_ID
```

The helper caches continuous speech with character timestamps and cuts cue WAVs. It supports at most 5,000 characters per request, including separators. Preserve successful speech rather than paying to regenerate it. On failure it records only HTTP status and a sanitized category, makes no automatic generation retry, and does not poll balances or change account limits. A 401 response alone does not establish why access failed.

## Verify the delivered artifact

Measure real audio duration. For video, mux that same track, decode the finished file, confirm non-silent narration, and compare its audio against the source track. For explicitly requested HTML, embed essential audio for offline playback and verify pause/seek/speed synchronization. WAVs existing on disk alone do not finish narration integration.

## Provenance and licenses

The production references adapt ideas from [Brag](https://github.com/latent-spaces/brag); no Brag media is bundled. The Qwen paragraph/alignment workflow is included here as a local authoring helper. This repository's license does not grant rights to third-party models, voices, music, fonts or source material; review each separately.
