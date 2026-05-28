#!/usr/bin/env python3
"""
Replace haiku with sonnet (case-preserving) across all files that define
haiku as a default model value.

Usage:
    uv run python .dev/replace-haiku-with-sonnet.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Files where haiku is defined as a default value.
# Paths are relative to repository root.
TARGET_FILES: list[str] = [
    # --- Sprint summarizer: hardcoded HAIKU_MODEL constant ---
    "src/superclaude/cli/sprint/summarizer.py",

    # --- Audit scanner agent: frontmatter model default ---
    "src/superclaude/agents/audit-scanner.md",
    ".claude/agents/audit-scanner.md",

    # --- Validate-roadmap protocol: ALL agents MUST use haiku ---
    "src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md",
    ".claude/skills/sc-validate-roadmap-protocol/SKILL.md",

    # --- RoadmapConfig dataclass: default agents include haiku ---
    "src/superclaude/cli/roadmap/models.py",

    # --- Roadmap executor: runtime fallback defaults to haiku ---
    "src/superclaude/cli/roadmap/executor.py",

    # --- Roadmap CLI: help text documenting haiku default ---
    "src/superclaude/cli/roadmap/commands.py",

    # --- Release-split protocol: default agent pairing includes haiku ---
    "src/superclaude/skills/sc-release-split-protocol/SKILL.md",
    ".claude/skills/sc-release-split-protocol/SKILL.md",

    # --- Fidelity script: Agent B defaults to haiku when no variants found ---
    "scripts/fidelity-check-setup.sh",

    # --- Roadmap CLI guide: documents haiku defaults and persona fallback ---
    "docs/guides/roadmap-cli-tools-release-guide.md",

    # --- Command docs: document haiku as default in --agents tables ---
    "src/superclaude/commands/roadmap.md",
    "src/superclaude/commands/release-split.md",
    ".claude/commands/sc/release-split.md",

    # --- Roadmap protocol skill: references CLI default (opus:architect,haiku:architect) ---
    "src/superclaude/skills/sc-roadmap-protocol/SKILL.md",
    ".claude/skills/sc-roadmap-protocol/SKILL.md",
]


def replace_case_preserving(text: str, old: str, new: str) -> str:
    """Replace all occurrences of *old* with *new*, preserving the case pattern
    of each matched substring.

    Patterns handled:
      - all lowercase   : haiku   -> sonnet
      - all uppercase   : HAIKU   -> SONNET
      - title case      : Haiku   -> Sonnet
    """
    # Order: title case first so "Haiku" isn't partially matched by "haiku"
    replacements = [
        (old.upper(), new.upper()),
        (old.capitalize(), new.capitalize()),
        (old.lower(), new.lower()),
    ]
    for o, n in replacements:
        text = text.replace(o, n)
    return text


def process_file(path: Path, dry_run: bool) -> tuple[int, int]:
    """Read *path*, replace haiku->sonnet, and write back unless *dry_run*.

    Returns (line_count_before, replacement_count).
    """
    if not path.exists():
        print(f"  SKIP (not found): {path}", file=sys.stderr)
        return 0, 0

    original = path.read_text(encoding="utf-8")
    modified = replace_case_preserving(original, "haiku", "sonnet")

    line_count = original.count("\n") + 1
    replacement_count = sum(
        1
        for o, _ in [
            ("haiku", "sonnet"),
            ("HAIKU", "SONNET"),
            ("Haiku", "Sonnet"),
        ]
        for _ in range(original.count(o))
    )

    if original == modified:
        print(f"  NO CHANGE: {path}")
        return line_count, 0

    if dry_run:
        print(f"  WOULD MODIFY ({replacement_count} replacements): {path}")
    else:
        path.write_text(modified, encoding="utf-8")
        print(f"  MODIFIED ({replacement_count} replacements): {path}")

    return line_count, replacement_count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace haiku with sonnet in default-model files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    print(f"Repository root: {repo_root}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"Files to scan: {len(TARGET_FILES)}")
    print()

    total_replacements = 0
    for rel_path in TARGET_FILES:
        full_path = repo_root / rel_path
        _, count = process_file(full_path, args.dry_run)
        total_replacements += count

    print()
    print(f"Total replacements: {total_replacements}")
    if args.dry_run:
        print("Run without --dry-run to apply changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
