# Learn with Motion

An agent skill for explaining technical ideas through narrated video. Use it for a PR, paper, article, framework or codebase when a summary gives the big picture but leaves the details disconnected.

Start by explaining the actual subject: what it is, what it does, why it is needed, and where it fits. Ground examples in that subject. Then explain the architecture and design: what each part does, how the parts connect, what changes, and why a choice matters. Use everyday language and explain unfamiliar terms as they become relevant. Numerical examples are optional. Separate diagrams and useful stillness are welcome. A short storyboard review happens before narration.

The default output is an MP4 with narration and centered phrase subtitles. An interactive HTML lesson is available when explicitly requested. The default visual style uses warm paper, dark ink, generous spacing and restrained accents.

## Install

This repository is the skill folder. For Codex, clone it into your user skills directory:

```bash
git clone https://github.com/BielC/learn-with-motion.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/learn-with-motion"
```

If that destination already exists, review and back it up before replacing it. Other agents that support `SKILL.md` folders can load this repository through their own skill installation mechanism. `agents/openai.yaml` supplies optional Codex UI metadata; the core instructions are in [SKILL.md](SKILL.md).

## Use

```text
Use $learn-with-motion to explain this public PR as a narrated video.
Show the old and new behavior, then explain the design that causes the change.
```

```text
Use $learn-with-motion to explain this paper's architecture.
Choose the depth that matters for understanding the method. Create video only.
```

For a guided conversation, ask to learn one connection at a time. For HTML, request it explicitly. The skill does not launch a video generator by itself; the agent reads the source, authors the explanation and scenes, generates narration, renders the film, and checks the deliverable.

## Runtime and narration

Reading the skill needs no extra packages. Producing a video needs an authoring/rendering stack, typically HTML/SVG with a headless browser and FFmpeg. The renderer is chosen for the explanation; this repository includes reusable scene-player assets, not a universal one-command video builder.

The default local voice recipe uses **Qwen3-TTS BF16 through MLX-Audio on Apple silicon**. Its portable helper is included, with local Whisper alignment, cue caching and explicit model paths. See [the narration setup](references/narration.md). Python 3.12, FFmpeg, optional Python dependencies and model downloads are required for that recipe. Other hardware requires a deliberately selected compatible voice engine; there is no automatic cloud fallback.

Kokoro is an optional lightweight helper. ElevenLabs is optional and requires a user-supplied key, voice selection and permission to send the script to the provider. No API key is included or needed for local narration.

## Sharing and private material

The package contains generic instructions, reusable code and a synthetic retry example. It includes no real PR examples, work documents, recordings, generated lessons, model weights or credentials.

Keep lesson sources and outputs in a separate working directory. A source being accessible to an agent does not make it publishable. Private code, screenshots, identifiers, captions and narration all need the same care as the original material. Local voice generation does not make the agent itself offline; source retrieval and the agent's model have their own data-handling rules.

The package checker rejects unexpected files, credential patterns, machine-specific paths and broken local reference links. It is a guardrail, not a guarantee that arbitrary future content is safe to publish. Review the staged diff and every new example before pushing. Generated audio/video, environments, model files and credential files are ignored by default.

## Development checks

These checks need only Python's standard library and Node.js for JavaScript syntax checks:

```bash
python3 tools/check_package.py
python3 -m unittest discover -s tests -v
node --check assets/film-player.js
node --check assets/film-viewport.js
```

With pre-commit installed, `pre-commit run --all-files` runs the package and helper checks. Synthesis quality and rendered scenes need their own visual/listening checks; structural validation alone does not establish teaching quality.

## License and references

[MIT](LICENSE) for the skill's instructions and code. Third-party models, voices, source material and media have separate licenses. Production references acknowledge [Brag](https://github.com/latent-spaces/brag); no Brag media is bundled. The skill takes inspiration from explanatory animation, including 3Blue1Brown, without claiming affiliation.

[Peer skill research](references/peer-research.md) records the inspected revisions, useful ideas, rejected constraints and resulting improvements. It is background research, not additional reading required for every lesson.
