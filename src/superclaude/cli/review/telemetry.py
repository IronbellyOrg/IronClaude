"""Review telemetry (review-telemetry/1): append-only JSONL records, task variables, SQLite loader.

No document text, quote, anchor or claim ever enters a record. Standard library only.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "review-telemetry/1"
TRUTH_BASES = ("catalog-v1", "theme-v1", "adjudicated-v1")
KINDS = ("first", "re-review", "audit")

_RUN_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_ID_TOKEN = r"(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b"
_ID_RE = re.compile(r"\b" + _ID_TOKEN)
_SECTION_RE = re.compile(r"\bsection\s+\d+(?:\.\d+)*", re.I)
_RFC_RE = re.compile(r"\b(?:MUST NOT|MUST|SHALL|SHOULD|MAY|REQUIRED)\b")
_BOLD_DEF = re.compile(r"^\s*(?:[-*+]\s+)?\*\*(" + _ID_TOKEN + ")")
_STOP = {"the", "and", "of", "to", "is", "a", "in", "that", "for"}

REVIEWER_GROUPS: dict[str, tuple[str, ...]] = {
    "panel": (
        "template_id",
        "template_version",
        "template_sha256",
        "tiers_version",
        "tiers_sha256",
        "environment",
        "panel_size",
    ),
    "slot": (
        "slot_id",
        "tier",
        "alias",
        "strategy",
        "seed",
        "fallback_depth",
        "stand_in",
    ),
    "model": ("resolved", "launch", "observed"),
    "task": (
        "doc_sha256",
        "doc_bytes",
        "doc_lines",
        "language",
        "doc_format",
        "specialization",
        "sections",
        "max_heading_depth",
        "tables",
        "table_rows",
        "ids_defined",
        "cross_refs",
        "rfc2119",
        "review_kind",
    ),
    "output": (
        "block_ok",
        "findings",
        "blocking",
        "by_severity",
        "verdict",
        "verdict_mismatch",
    ),
    "cost": (
        "tokens_in",
        "tokens_cache_read",
        "tokens_cache_write",
        "tokens_out",
        "wall_s",
    ),
}
REVIEWER_TOP = (
    "schema_version",
    "kind",
    "record_id",
    "ts_utc",
    "run_id",
    "step",
    "round",
    "reviewer_id",
)
OUTCOME_KEYS = (
    "schema_version",
    "kind",
    "record_id",
    "ts_utc",
    "run_id",
    "reviewer_record_id",
    "truth_basis",
    "confirmed_tp",
    "false_pos",
    "unconfirmed",
    "unique_tp",
    "overlap_mean_jaccard",
    "recall_vs_confirmed",
    "precision",
    "cost_per_confirmed_tp",
    "supersedes",
)
OUTCOME_COLUMNS = OUTCOME_KEYS + ("stratum",)
SEVERITIES = ("CRITICAL", "MAJOR", "MINOR")
STRATA = (
    "sonnet",
    "haiku",
)  # owner decision D3: every record may carry a stratum tag; strata are never pooled


def new_record_id() -> str:
    return uuid.uuid4().hex


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- task variables


def _table_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    cur: list[str] = []
    for ln in lines + [""]:
        if ln.lstrip().startswith("|"):
            cur.append(ln.strip())
        else:
            if cur:
                blocks.append(cur)
            cur = []
    return blocks


def task_variables(
    text: str, specialization: str = "unspecified", review_kind: str = "first"
) -> dict:
    """Descriptive variables of a reviewed document (contract C8)."""
    lines = text.splitlines()
    heads = [ln for ln in lines if re.match(r"^#{1,6}\s", ln)]
    depth = max((len(re.match(r"^#+", h).group(0)) for h in heads), default=0)  # type: ignore[union-attr]
    tables = 0
    table_rows = 0
    defining = 0
    defined: set[str] = set()
    for block in _table_blocks(lines):
        sep = next(
            (i for i, ln in enumerate(block) if re.match(r"^\|\s*:?-{3,}", ln)), None
        )
        if sep is None:
            continue
        tables += 1
        table_rows += len(block) - (sep + 1)
        for ln in block:
            cells = ln.strip().strip("|").split("|")
            first = cells[0] if cells else ""
            toks = _ID_RE.findall(first)
            defined.update(toks)
            defining += len(toks)
    for ln in lines:
        m = _BOLD_DEF.match(ln)
        if m:
            defined.add(m.group(1))
            defining += 1
    occurrences = len(_ID_RE.findall(text)) + len(_SECTION_RE.findall(text))
    words = re.findall(r"[a-z']+", text.lower())
    share = (sum(1 for w in words if w in _STOP) / len(words)) if words else 0.0
    return {
        "doc_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "doc_bytes": len(text.encode("utf-8")),
        "doc_lines": len(lines),
        "language": "en" if share >= 0.02 else "unknown",
        "doc_format": "markdown",
        "specialization": specialization,
        "sections": len(heads),
        "max_heading_depth": depth,
        "tables": tables,
        "table_rows": table_rows,
        "ids_defined": len(defined),
        "cross_refs": max(occurrences - defining, 0),
        "rfc2119": len(_RFC_RE.findall(text)),
        "review_kind": review_kind,
    }


# ---------------------------------------------------------------- validation


def validate_record(rec: Any) -> list[str]:
    """Schema errors of one telemetry record (an empty list means valid)."""
    if not isinstance(rec, dict):
        return ["record must be a JSON object"]
    errors: list[str] = []
    kind = rec.get("kind")
    if rec.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be '{SCHEMA_VERSION}'")
    if kind == "reviewer_run":
        required: list[str] = list(REVIEWER_TOP) + list(REVIEWER_GROUPS) + ["context"]
        allowed = set(required) | {"supersedes", "stratum"}
        for key in required:
            if key not in rec:
                errors.append(f"missing key '{key}'")
        for key in rec:
            if key not in allowed:
                errors.append(f"unknown key '{key}'")
        for group, keys in REVIEWER_GROUPS.items():
            sub = rec.get(group)
            if group not in rec:
                continue
            if not isinstance(sub, dict):
                errors.append(f"{group} must be an object")
                continue
            for key in keys:
                if key not in sub:
                    errors.append(f"missing key '{group}.{key}'")
            for key in sub:
                if key not in keys:
                    errors.append(f"unknown key '{group}.{key}'")
        by = (
            (rec.get("output") or {}).get("by_severity")
            if isinstance(rec.get("output"), dict)
            else None
        )
        if (
            "output" in rec
            and isinstance(rec.get("output"), dict)
            and "by_severity" in rec["output"]
        ):
            if not isinstance(by, dict) or any(k not in by for k in SEVERITIES):
                errors.append("output.by_severity must hold CRITICAL, MAJOR and MINOR")
        if "context" in rec and not isinstance(rec["context"], dict):
            errors.append("context must be an object")
        if "round" in rec and (
            not isinstance(rec["round"], int) or isinstance(rec["round"], bool)
        ):
            errors.append("round must be an integer")
    elif kind == "outcome":
        for key in OUTCOME_KEYS:
            if key not in rec:
                errors.append(f"missing key '{key}'")
        for key in rec:
            if key not in OUTCOME_KEYS and key != "stratum":
                errors.append(f"unknown key '{key}'")
        if "truth_basis" in rec and rec["truth_basis"] not in TRUTH_BASES:
            errors.append("truth_basis must be catalog-v1, theme-v1 or adjudicated-v1")
    else:
        return errors + ["kind must be 'reviewer_run' or 'outcome'"]
    if rec.get("stratum") is not None and rec["stratum"] not in STRATA:
        errors.append("stratum must be 'sonnet' or 'haiku'")
    if "ts_utc" in rec and not (
        isinstance(rec["ts_utc"], str) and _TS.match(rec["ts_utc"])
    ):
        errors.append("ts_utc must look like 2026-11-10T12:00:00Z")
    if "run_id" in rec and not (
        isinstance(rec["run_id"], str) and _RUN_ID.match(rec["run_id"])
    ):
        errors.append("run_id must match ^[A-Za-z0-9._-]{1,64}$")
    if "record_id" in rec and not (
        isinstance(rec["record_id"], str) and rec["record_id"]
    ):
        errors.append("record_id must be a non-empty string")
    return errors


# ---------------------------------------------------------------- append-only files


def append_record(directory: str | Path, rec: dict) -> Path:
    """Validate and append one record to its run file; never rewrites or deletes a line."""
    errors = validate_record(rec)
    if errors:
        raise ValueError("invalid telemetry record: " + "; ".join(errors))
    root = Path(directory) / "records"
    name = (
        f"{rec['run_id']}.outcomes.jsonl"
        if rec["kind"] == "outcome"
        else f"{rec['run_id']}.jsonl"
    )
    existing = sorted(root.glob(f"*/*/{name}")) if root.is_dir() else []
    if existing:
        path = existing[0]
    else:
        year, month = rec["ts_utc"][:4], rec["ts_utc"][5:7]
        path = root / year / month / name
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
    return path


# ---------------------------------------------------------------- SQLite loader


def _flatten_reviewer(rec: dict) -> dict:
    row: dict[str, Any] = {k: rec.get(k) for k in REVIEWER_TOP}
    row["supersedes"] = rec.get("supersedes")
    row["stratum"] = rec.get("stratum")
    for group, keys in REVIEWER_GROUPS.items():
        sub = rec.get(group) or {}
        for key in keys:
            val = sub.get(key)
            if key == "by_severity" and isinstance(val, dict):
                for sev in SEVERITIES:
                    row[f"output_by_severity_{sev}"] = val.get(sev)
                continue
            row[f"{group}_{key}"] = val
    ctx = rec.get("context") or {}
    row["context_experiment"] = ctx.get("experiment")
    row["context_arm"] = ctx.get("arm")
    row["context_replicate"] = ctx.get("replicate")
    row["context_json"] = json.dumps(ctx, sort_keys=True)
    return row


def _reviewer_columns() -> list[str]:
    template = _flatten_reviewer({})
    for group, keys in REVIEWER_GROUPS.items():
        for key in keys:
            if key == "by_severity":
                for sev in SEVERITIES:
                    template.setdefault(f"output_by_severity_{sev}", None)
            else:
                template.setdefault(f"{group}_{key}", None)
    return list(template)


def _sql_value(v: Any) -> Any:
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (dict, list)):
        return json.dumps(v, sort_keys=True)
    return v


def _iter_lines(directory: Path) -> Iterable[tuple[Path, int, str]]:
    for path in sorted((directory / "records").rglob("*.jsonl")):
        with open(path, encoding="utf-8") as fh:
            for no, line in enumerate(fh, 1):
                if line.strip():
                    yield path, no, line


_VIEW = """
CREATE VIEW model_scores AS
SELECT r.model_observed AS model_observed, r.slot_tier AS slot_tier, r.slot_stand_in AS slot_stand_in, r.stratum AS stratum, o.truth_basis AS truth_basis,
       COUNT(DISTINCT r.record_id) AS n_runs,
       SUM(o.confirmed_tp) AS sum_confirmed_tp,
       SUM(o.false_pos) AS sum_false_pos,
       AVG(o.precision) AS mean_precision,
       AVG(o.recall_vs_confirmed) AS mean_recall_vs_confirmed,
       SUM(o.unique_tp) AS sum_unique_tp,
       CAST(SUM(r.cost_tokens_out) AS REAL) / NULLIF(SUM(o.confirmed_tp), 0) AS cost_per_confirmed_tp
FROM reviewer_runs r
LEFT JOIN outcomes o
       ON o.reviewer_record_id = r.record_id
      AND o.record_id NOT IN (SELECT supersedes FROM outcomes WHERE supersedes IS NOT NULL)
WHERE r.record_id NOT IN (SELECT supersedes FROM reviewer_runs WHERE supersedes IS NOT NULL)
GROUP BY r.model_observed, r.slot_tier, r.slot_stand_in, r.stratum, o.truth_basis
"""


def load(directory: str | Path, db_path: str | Path) -> dict:
    """Load every record under directory/records into SQLite. Idempotent; invalid lines are reported and skipped."""
    directory = Path(directory)
    con = sqlite3.connect(str(db_path))
    try:
        rcols = _reviewer_columns()
        con.execute(
            "CREATE TABLE IF NOT EXISTS reviewer_runs ("
            + ", ".join(
                f'"{c}"' + (" PRIMARY KEY" if c == "record_id" else "") for c in rcols
            )
            + ")"
        )
        con.execute(
            "CREATE TABLE IF NOT EXISTS outcomes ("
            + ", ".join(
                f'"{c}"' + (" PRIMARY KEY" if c == "record_id" else "")
                for c in OUTCOME_COLUMNS
            )
            + ")"
        )
        counts = {"reviewer_runs": 0, "outcomes": 0, "invalid": []}
        for path, no, line in _iter_lines(directory):
            where = f"{path}:{no}"
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                counts["invalid"].append(f"{where}: not valid JSON: {exc.msg}")
                continue
            errors = validate_record(rec)
            if errors:
                counts["invalid"].append(f"{where}: {errors[0]}")
                continue
            if rec["kind"] == "reviewer_run":
                row = _flatten_reviewer(rec)
                cur = con.execute(
                    "INSERT OR IGNORE INTO reviewer_runs ("
                    + ", ".join(f'"{c}"' for c in rcols)
                    + ") VALUES ("
                    + ", ".join("?" * len(rcols))
                    + ")",
                    [_sql_value(row.get(c)) for c in rcols],
                )
                counts["reviewer_runs"] += cur.rowcount
            else:
                cur = con.execute(
                    "INSERT OR IGNORE INTO outcomes ("
                    + ", ".join(f'"{c}"' for c in OUTCOME_COLUMNS)
                    + ") VALUES ("
                    + ", ".join("?" * len(OUTCOME_COLUMNS))
                    + ")",
                    [_sql_value(rec.get(c)) for c in OUTCOME_COLUMNS],
                )
                counts["outcomes"] += cur.rowcount
        con.execute("DROP VIEW IF EXISTS model_scores")
        con.execute(_VIEW)
        con.commit()
        return counts
    finally:
        con.close()
