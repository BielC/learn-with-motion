# Explain Skills

Two independently installable agent skills for understanding technical subjects:

| Skill | Output | Use |
| --- | --- | --- |
| [explain-video](skills/explain-video/SKILL.md) | Narrated MP4 | A watchable explanation with connected diagrams and measured narration. |
| [explain-interactive](skills/explain-interactive/SKILL.md) | Self-contained HTML | Self-paced diagrams, traces, comparisons and meaningful experiments. |

Both start with the actual subject: what it is, what it does, why it is useful and where it fits. They establish necessary background before architecture and relevant mechanisms. Examples and numerical depth are chosen for the explanation. The default visual style is warm paper, dark ink, generous spacing and restrained accents.

## Install

This repository is a collection, not a skill folder. Install the desired subfolder, or both. Each includes its own required assets and references and works without its sibling or the repository checkout.

For Codex, clone the collection outside the skills directory, then copy the packages:

```bash
git clone https://github.com/BielC/learn-with-motion.git explain-skills
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R explain-skills/skills/explain-video "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R explain-skills/skills/explain-interactive "${CODEX_HOME:-$HOME/.codex}/skills/"
```

If either destination exists, review and back it up before replacing it. A previous installation under the old skill name should be backed up outside the skills directory and retired after verifying the replacement. Preserve any personal narration/runtime setup privately. Other agents supporting `SKILL.md` can install either subfolder through their own mechanism. Each package has its own optional Codex UI metadata in `agents/openai.yaml`.

## Use

```text
Use $explain-video to explain this PR as a narrated video.
Establish the existing system and show old versus new behavior.
```

```text
Use $explain-interactive to explain this framework in an offline HTML page.
Let me inspect how a request moves through its components.
```

The video skill delivers a film without a companion webpage and uploads the finished video privately to the user's Google Drive, retaining the local file. Drive delivery requires available upload tooling and verified restricted access; local-only delivery can be requested. The interactive skill creates a page without requiring a video. Produce both only when requested. Guided questions are optional in the interactive skill, and neither format requires quizzes.

## Runtime

Reading the instructions needs no additional packages. Video production requires an authoring/rendering stack, typically HTML/SVG with a headless browser and FFmpeg. The video package includes a dependency-free clock/export helper, not a universal one-command film generator. Interactive pages normally use HTML, SVG, CSS and JavaScript; browser automation is needed to verify them.

The video package's [local narration recipe](skills/explain-video/references/narration.md) uses **Qwen3-TTS BF16 through MLX-Audio on Apple silicon**, with coherent paragraphs, separate speech/alignment caches and local Whisper alignment. Python 3.12, FFmpeg, optional dependencies and separately downloaded models are required. Kokoro and ElevenLabs are explicit alternatives, with no automatic voice or cloud fallback. The interactive package is text/visual by default and can integrate explicitly requested audio through available narration tooling.

## Sharing

The distribution contains generic instructions, reusable code and a synthetic retry example. Keep real lesson sources, private PRs, generated media, credentials, model weights, runtime paths and learner records outside the repository. Source access does not grant publication permission. A selected cloud voice provider sends the script to that provider and needs authorization covering the material.

The package checker enforces explicit file boundaries, independent local references and common sensitive patterns. Review the staged content too; pattern checks cannot establish that arbitrary material is publishable.

## Development checks

```bash
python3 tools/check_package.py
python3 -m unittest discover -s tests -v
node --check skills/explain-video/assets/film-player.js
node --check skills/explain-interactive/assets/film-player.js
node --check skills/explain-interactive/assets/film-viewport.js
pre-commit run --all-files
```

Helper/package tests check cache behavior and independent installation boundaries. They do not establish educational quality. Evaluate revisions through fresh-agent task execution, evidence-based artifact review and learner feedback. Compare fixed source snapshots and prompts under the same model/settings before claiming a quality or cost improvement.

## License and research

[MIT](LICENSE) for these instructions and code; each package includes the license. Third-party models, voices, sources and media retain their own terms. [Research provenance](research/peer-research.md) records earlier public-source comparisons. It is not required reading for ordinary explanation tasks. No third-party media is bundled.
