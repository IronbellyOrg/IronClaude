"""The one import point for superclaude.cli.review.findings (DESIGN 2.3).

Everything in scaffold/ and sweep/ gets the real parser from here. `_check_finding` and `_blocks_after` are
private in the source; tests/test_fnd_contract.py pins their names and signatures, so a rename or change shows
up in that one test and this file is the only one to edit.
"""

from __future__ import annotations

from superclaude.cli.review.findings import (  # noqa: F401  (re-exports)
    _HEAD_FINDINGS,
    CATEGORIES,
    _blocks_after,
    _check_finding,
    flat,
    locate,
    parse_block,
    same_defect,
)


def lenient_lines(report: str) -> list[str]:
    """The raw lines of the findings block (the last findings-v1 fence, like parse_block), blank lines dropped.

    Lines are returned as written, valid JSON or not, so a caller can repair or count the bad ones.
    No heading or no findings-v1 fence gives []. An unclosed fence still gives the lines read before the end.
    """
    _, blocks = _blocks_after(report, _HEAD_FINDINGS, "findings-v1")
    if not blocks:
        return []
    return [raw for _, raw in blocks[-1][1] if raw.strip()]
