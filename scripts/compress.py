"""CLI wrapper for markdown compression.

The real compression logic lives in ``superclaude.compression``. This script
is a thin CLI that preserves the historical invocation surface:

    uv run python scripts/compress.py <file.md> --type {roadmap|spec|tasklist}
                                                 [--aggressive] [--output PATH] [--dry-run]

It prints a human-readable per-strategy savings report.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure we can import the in-tree package when running the script directly
# without an editable install.
_REPO_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_REPO_SRC) not in sys.path:
    sys.path.insert(0, str(_REPO_SRC))

from superclaude.compression import (  # noqa: E402
    PIPELINES,
    StrategyStat,
    run_pipeline,
)


def print_report(
    input_path: str,
    doc_type: str,
    aggressive: bool,
    stats: list[StrategyStat],
    output_path: str,
) -> None:
    """Print a per-strategy savings report."""
    mode = "aggressive (lossy enabled)" if aggressive else "lossless"
    print(f"\n{'=' * 72}")
    print(f"  Compression report: {input_path}")
    print(f"  Pipeline: {doc_type} ({mode})")
    print(f"{'=' * 72}\n")

    col_strategy = 44
    col_num = 10
    header = (
        f"  {'Strategy':<{col_strategy}}"
        f"{'Before':>{col_num}}"
        f"{'After':>{col_num}}"
        f"{'Saved':>{col_num}}"
        f"{'%':>7}"
    )
    print(header)
    print(f"  {'-' * (col_strategy + col_num * 3 + 7)}")

    for s in stats:
        pct = f"{s.pct_saved:.1f}%"
        label = f"{s.id} {s.name}"
        if len(label) > col_strategy:
            label = label[: col_strategy - 1] + "\u2026"
        print(
            f"  {label:<{col_strategy}}"
            f"{s.bytes_before:>{col_num},}"
            f"{s.bytes_after:>{col_num},}"
            f"{s.bytes_saved:>{col_num},}"
            f"{pct:>7}"
        )

    print(f"  {'-' * (col_strategy + col_num * 3 + 7)}")
    if stats:
        total_before = stats[0].bytes_before
        total_after = stats[-1].bytes_after
        total_saved = total_before - total_after
        total_pct = (total_saved / total_before * 100) if total_before else 0
        pct_str = f"{total_pct:.1f}%"
        print(
            f"  {'TOTAL':<{col_strategy}}"
            f"{total_before:>{col_num},}"
            f"{total_after:>{col_num},}"
            f"{total_saved:>{col_num},}"
            f"{pct_str:>7}"
        )
    print(f"\n  Output: {output_path}")
    print(f"{'=' * 72}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compress markdown documents using per-type strategy stacks.",
        epilog=(
            "Strategies run in order: A1 (rule-based) first, then A2 (structural).\n"
            "Lossy strategies are OFF by default; enable with --aggressive.\n"
            "\n"
            "Examples:\n"
            "  %(prog)s roadmap.md --type roadmap\n"
            "  %(prog)s spec.md --type spec --output compressed.md\n"
            "  %(prog)s tasklist.md --type tasklist --aggressive\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", help="Path to markdown file to compress")
    parser.add_argument(
        "--type",
        "-t",
        choices=sorted(PIPELINES.keys()),
        required=True,
        dest="doc_type",
        help="Document type (determines strategy stack)",
    )
    parser.add_argument(
        "--aggressive",
        action="store_true",
        default=False,
        help="Enable lossy strategies (requires review of output)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: <name>.compressed.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print report only, do not write output file",
    )

    args = parser.parse_args()
    input_path = Path(args.file)

    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1

    if input_path.suffix != ".md":
        print(
            f"Warning: file does not have .md extension: {input_path}",
            file=sys.stderr,
        )

    text = input_path.read_text(encoding="utf-8")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".compressed.md")

    compressed, stats = run_pipeline(text, args.doc_type, args.aggressive)

    if not args.dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(compressed, encoding="utf-8")

    print_report(
        str(input_path),
        args.doc_type,
        args.aggressive,
        stats,
        str(output_path) if not args.dry_run else "(dry run - no file written)",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
