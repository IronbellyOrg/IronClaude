"""The rank function's weights as one table (DESIGN 5.2) and its sha256 (`prepass.json: rank_table_sha256`).

The numbers are not typed again here: each weight is read from the constant the extractor in `sweep/extractors.py`
uses, so the table and the extractors cannot disagree (tests/test_select.py pins both against the DESIGN 5.2 numbers
and against the priorities real candidates get). The table is frozen with the extractors (AO-5).

Each row is `{base, plus, minus, required, lo, hi}`:
    base      the starting rank
    plus      signal -> the most the signal can add (weight times its cap)
    minus     signal -> the most it can take away
    required  signal -> what a candidate of this row always carries (E5 has at least one missing identifier, E7 at
              least one clause with no overlap and one block with two shared tokens)
    lo, hi    the range of the row, from base, plus, minus and required, clamped to 0-100 (the DESIGN 5.2 range)
Rows are keyed by extractor id; E1 has two, `E1.completeness` (class C1) and `E1.universal` (class C6).
"""

from __future__ import annotations

import hashlib
import json

from sweep import extractors as x

CLAMP = (0, 100)


def _row(base, plus=None, minus=None, required=None) -> dict:
    plus, minus, required = plus or {}, minus or {}, required or {}
    lo = max(
        CLAMP[0], min(CLAMP[1], base + sum(required.values()) - sum(minus.values()))
    )
    hi = max(CLAMP[0], min(CLAMP[1], base + sum(plus.values())))
    return {
        "base": base,
        "plus": dict(plus),
        "minus": dict(minus),
        "required": dict(required),
        "lo": lo,
        "hi": hi,
    }


RANK_TABLE: dict[str, dict] = {
    "E1.completeness": _row(
        x.E1_BASE,
        plus={
            "bound_none": x.E1_BOUND_NONE,
            "scope_differs": x.E1_SCOPE_DIFFERS,
            "extra_set_words": x.E1_EXTRA_WORD * x.E1_EXTRA_CAP,
        },
    ),
    "E1.universal": _row(
        x.E1_BASE,
        plus={
            "names_path": x.E1_NAMES_PATH,
            "extra_set_words": x.E1_EXTRA_WORD * x.E1_EXTRA_CAP,
            "limiter_line": x.E1_LIMITER,
            "enforcing_test": x.E1_TEST,
        },
    ),
    "E2": _row(
        x.E2_BASE_PRIORITY,
        plus={
            "no_match": x.E2_NO_MATCH,
            "near_miss": x.E2_NEAR_MISS,
            "selector_zero": x.E2_SELECTOR_ZERO,
        },
    ),
    "E3": _row(
        x.E3_BASE_PRIORITY,
        plus={
            "long_stem": x.E3_LONG_STEM,
            "distinctive": x.E3_DISTINCTIVE,
            "unnamed_test_files": x.E3_TEST_WEIGHT * x.E3_TEST_CAP,
            "unnamed_other_files": x.E3_OTHER_WEIGHT * x.E3_OTHER_CAP,
            "gate_names_none": x.E3_GATE_NONE,
        },
        minus={"common_stem": x.E3_COMMON_STEM_PENALTY},
    ),
    "E4": _row(
        x.E4_BASE_PRIORITY,
        plus={
            "count_change": x.E4_COUNT_CHANGE,
            "long_needle": x.E4_LONG_NEEDLE,
            "unnamed_root_hit": x.E4_ROOT_WEIGHT,
            "unnamed_hits": x.E4_UNNAMED_WEIGHT * x.E4_UNNAMED_CAP,
        },
    ),
    "E5": _row(
        x.E5_BASE_PRIORITY,
        plus={"missing_identifiers": x.E5_PER_MISSING * x.E5_MISSING_CAP},
        required={"missing_identifiers": x.E5_PER_MISSING},
    ),
    "E6": _row(
        x.E6_BASE_PRIORITY,
        plus={"read_occurrences": x.E6_PER_READ * x.E6_READ_CAP},
        required={"read_occurrences": x.E6_PER_READ},
    ),
    "E7": _row(
        x.E7_BASE_PRIORITY,
        plus={
            "zero_overlap_clauses": x.E7_ZERO_WEIGHT * x.E7_ZERO_CAP,
            "shared_tokens": x.E7_SHARED_WEIGHT,
        },
        required={
            "zero_overlap_clauses": x.E7_ZERO_WEIGHT,
            "shared_tokens": x.E7_SHARED_WEIGHT,
        },
    ),
}


def row_key(extractor: str, kind: str) -> str:
    """The RANK_TABLE row of a candidate: `E1.<kind>` for E1, the extractor id for every other extractor."""
    return f"{extractor}.{kind}" if extractor == "E1" else extractor


def canonical(table: dict | None = None) -> str:
    """The table as JSON text: sorted keys, ensure_ascii False, trailing newline (DESIGN 2.4)."""
    return (
        json.dumps(
            RANK_TABLE if table is None else table,
            sort_keys=True,
            ensure_ascii=False,
            indent=1,
        )
        + "\n"
    )


def sha256(table: dict | None = None) -> str:
    return hashlib.sha256(canonical(table).encode("utf-8")).hexdigest()


rank_table_sha256 = sha256()
