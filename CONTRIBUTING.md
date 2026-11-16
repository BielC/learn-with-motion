# Contributing

Open an issue for a bug or proposal, or send a focused pull request. For a larger change, discuss the intended behavior in an issue first. Use public or synthetic examples and explain the problem the change solves.

## Work on a branch

Fork this repository, clone your fork and create a branch from the latest `main`:

```bash
git switch main
git pull --ff-only
git switch -c describe-your-change
```

Install the skill packages using the [README instructions](README.md#install). Keep generated lessons, source snapshots, model weights, credentials and personal runtime settings outside the repository.

## Run the local checks

Use Python 3.12 or newer, Node.js and pre-commit. The helper tests do not need downloaded models, speech synthesis or network access.

```bash
python3 tools/check_package.py
python3 -m unittest discover -s tests -v
node --check skills/explain-video/assets/film-player.js
node --check skills/explain-interactive/assets/film-player.js
node --check skills/explain-interactive/assets/film-viewport.js
pre-commit run --all-files
git diff --check
```

Each skill must remain independently installable. Keep its required assets and references inside its own folder. If you add a distribution file, update the corresponding allowlist in `tools/check_package.py`. The checker catches common sensitive patterns, but you must also review the diff for private material.

## Send a pull request

Push your branch to your fork and open a pull request against this repository's `main`. Describe the problem, the resulting behavior and the checks you ran. If a check could not run, say why. Keep unrelated changes in separate pull requests.

`main` requires pull requests, including maintainer changes, and blocks force pushes and deletion. An approving review is not mandatory while the project has a single maintainer. Checks run locally; include their results in the pull request.

For explanation or narration changes, distinguish package/helper checks from evidence about the finished explanation. Do not claim improved learning or voice quality from passing tests alone. Never include credentials, private sources or generated private media in an issue or pull request.

Contributions to the repository's instructions and code use its [MIT license](LICENSE). Third-party sources, models, voices and media retain their own terms.
