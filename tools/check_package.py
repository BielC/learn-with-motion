"""Check the deliberately small, text-only skill distribution before sharing.

This catches common accidental inclusions. It cannot determine whether arbitrary
prose/code is confidential; review every new example and the staged diff too.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    'explain-video': {
        'SKILL.md', 'LICENSE', 'agents/openai.yaml', 'requirements-qwen.txt',
        'examples/narration.json', 'assets/film-player.js',
        'references/film-direction.md', 'references/narration.md',
        'references/player-runtime.md', 'references/visual-patterns.md',
        'scripts/elevenlabs_narration.py', 'scripts/kokoro_narration.py',
        'scripts/qwen_narration.py',
    },
    'explain-interactive': {
        'SKILL.md', 'LICENSE', 'agents/openai.yaml',
        'assets/film-player.js', 'assets/film-viewport.js',
        'assets/film-viewport.css', 'assets/lesson.css', 'assets/retry-trace.html',
        'references/html-output.md', 'references/player-runtime.md',
        'references/guided-learning.md',
    },
}
ALLOWED = {
    '.gitignore', '.pre-commit-config.yaml', 'README.md', 'LICENSE',
    'research/peer-research.md', 'tools/check_package.py', 'tests/test_helpers.py',
} | {f'skills/{package}/{name}' for package, files in PACKAGES.items() for name in files}
PATTERNS = {
    'machine-specific home path': r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
    'private network URL': r'https?://(?:localhost|127\.0\.0\.1|10\.[0-9.]+|192\.168\.[0-9.]+|172\.(?:1[6-9]|2\d|3[01])\.[0-9.]+)(?=[:/\s]|$)',
    'private host suffix': r'https?://[^/\s]+\.(?:internal|corp)(?=[:/\s]|$)',
    'GitHub credential': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b',
    'AWS access key': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'provider credential': r'\b(?:sk-[A-Za-z0-9_-]{30,}|sk_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})\b',
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
}


def inspect_contents(name, raw):
    failures = []
    if name not in ALLOWED:
        failures.append('unexpected distribution file')
    if len(raw) > 250_000:
        failures.append('file exceeds text-package size budget')
    if b'\x00' in raw:
        return failures + ['binary content']
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        return failures + ['non-UTF-8 content']
    for label, pattern in PATTERNS.items():
        if re.search(pattern, content):
            failures.append(label)
    if not content.endswith('\n'):
        failures.append('missing final newline')
    return failures


def candidate_files():
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                            cwd=ROOT, check=True, stdout=subprocess.PIPE)
    return sorted(set(p.decode() for p in result.stdout.split(b'\0') if p))


def markdown_link_failures(path, content, boundary):
    """Check local links inside the independently installable package boundary."""
    failures = []
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
        if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
            continue
        relative = target.split('#')[0]
        if not relative:
            continue
        resolved = (path.parent / relative).resolve()
        if not resolved.is_relative_to(boundary.resolve()):
            failures.append('local reference escapes distribution boundary')
        elif not resolved.is_file():
            failures.append('broken local reference: ' + relative)
    return failures


def main():
    failures, names = [], candidate_files()
    for name in names:
        path = ROOT / name
        if path.is_symlink():
            failures.append((name, 'symlinks are outside the distribution boundary'))
            continue
        if not path.is_file():
            failures.append((name, 'missing file'))
            continue
        raw = path.read_bytes()
        failures.extend((name, reason) for reason in inspect_contents(name, raw))
        if path.suffix == '.md':
            parts = Path(name).parts
            boundary = ROOT / 'skills' / parts[1] if parts[0] == 'skills' else ROOT
            failures.extend((name, reason) for reason in
                            markdown_link_failures(path, raw.decode('utf-8'), boundary))
    missing = ALLOWED - set(names)
    failures.extend((name, 'required distribution file missing') for name in sorted(missing))
    for name, reason in failures:
        print(f'{name}: {reason}')  # Categories only; never print credential matches.
    print(f'Checked {len(names)} allowlisted text files; {len(failures)} issue(s).')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
