#!/usr/bin/env python3
"""Secret scan for run records: scan_secrets.py <folder> [--redact].

Reads every file under the folder and reports token-like material as
`path:line: <pattern name>`; the value is never printed. Exit 0 when clean,
1 when anything was found. For .jsonl files the values of the keys "signature"
and "thinking" are skipped (opaque model blobs, not credentials). With
--redact each finding is replaced in place by `[REDACTED:<pattern name>]` and
the scan runs again; the exit status is that of the second scan.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKIP_KEYS = {"signature", "thinking"}
PATTERNS = {
    "github-token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}"),
    "sk-prefix-key": re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    "cloud-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b|\bAIza[0-9A-Za-z_-]{30,}"),
    "slack-token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    "private-key-header": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "password-assignment": re.compile(r"(?i)\bpassword\s*=\s*[^\s\"'<>`$)]{4,}"),
    "long-key-string": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|authorization|bearer)[\"']?\s*[:=]?\s*[\"']?(?!\$)[A-Za-z0-9_\-./+=]{32,}"
    ),
}


def _text_of(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw[:4096]:
        return None
    return raw.decode("utf-8", errors="replace")


def _strip(value):
    if isinstance(value, dict):
        return {k: ("" if k in SKIP_KEYS else _strip(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [_strip(v) for v in value]
    return value


def _scan_lines(path: Path, text: str):
    for number, line in enumerate(text.splitlines(), 1):
        view = line
        if path.suffix == ".jsonl":
            try:
                view = json.dumps(_strip(json.loads(line)))
            except ValueError:
                pass
        for name, pattern in PATTERNS.items():
            if pattern.search(view):
                yield number, name


def scan(folder: Path) -> list[tuple[Path, int, str]]:
    found = []
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        text = _text_of(path)
        if text is None:
            continue
        for number, name in _scan_lines(path, text):
            found.append((path, number, name))
    return found


def redact(findings: list[tuple[Path, int, str]]) -> None:
    by_file: dict[Path, set[int]] = {}
    for path, number, _name in findings:
        by_file.setdefault(path, set()).add(number)
    for path, numbers in by_file.items():
        lines = (_text_of(path) or "").splitlines(keepends=True)
        for number in numbers:
            for name, pattern in PATTERNS.items():
                lines[number - 1] = pattern.sub(f"[REDACTED:{name}]", lines[number - 1])
        path.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    paths = [a for a in argv if not a.startswith("--")]
    if len(paths) != 1 or not Path(paths[0]).is_dir():
        sys.stderr.write("usage: scan_secrets.py <folder> [--redact]\n")
        return 2
    folder = Path(paths[0])
    findings = scan(folder)
    if findings and "--redact" in argv:
        redact(findings)
        print(f"redacted {len(findings)} finding(s):")
        for path, number, name in findings:
            print(f"  {path}:{number}: {name}")
        findings = scan(folder)
    for path, number, name in findings:
        print(f"{path}:{number}: {name}")
    files = sum(1 for p in folder.rglob("*") if p.is_file())
    print(f"scanned {files} file(s) under {folder}: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
