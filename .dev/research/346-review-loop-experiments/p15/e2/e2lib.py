"""Shared small helpers for the E2 offline scripts (paths, label schema, sandbox builders)."""
from __future__ import annotations

import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
JEV = HERE.parent / "jev"
for _p in (str(HERE), str(JEV)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from p15common import harnesslib as H   # noqa: E402

OFF = HERE / "offline"
LEDGER = OFF / "workers.json"
FIELDS = ["defect_real", "evidence_sufficient", "evidence_minimal"]          # decision fields (agreement, adjudication)
ENUM = {"defect_real": {"yes", "no", "undecidable"},
        "evidence_sufficient": {"yes", "no", "n/a", "undecidable"},
        "evidence_minimal": {"yes", "no", "n/a", "undecidable"}}

RUBRIC = """# Labeling rubric (read fully before you start)

You will label {n} proposed defects. For each case you get a document, one proposed defect (a sentence) and the quoted passages
that the proposer believes show it. Judge only from the document text. Do not edit the document. Do not search the document for
other problems; answer `other_blocker` only if you happened to notice one while checking the claim.

## Blocking (the grading check, verbatim from the review rules)

For each finding before you mark it blocking, write the sentence "An implementer who follows the stated text as written builds X,
and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each
other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion
cannot pass. Grade it Medium (NOT blocking) when the sentence needs a guess that the implementer picks the worse of two readings
the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an
unspecified edge case) rather than a stated text that does harm. An apparent conflict that the document itself resolves (a
condition that separates the cases, an explicit exception) is not a defect.

## Fields (one JSON object per case, one line per case, in `labels.jsonl`)

- `case_id`: copied from the case.
- `defect_real`: `yes` if the proposed defect is real AND blocking per the grading check; `no` otherwise.
- `evidence_sufficient`: `yes` if the quoted passages alone, read in the document, show the defect without reading anything else;
  `no` if another passage is needed; `n/a` when `defect_real` is `no`.
- `evidence_minimal`: `yes` if no quoted passage can be dropped without losing the defect; `no` if one can; `n/a` when
  `defect_real` is `no`.
- `other_blocker`: another blocking defect you noticed (a short quote plus one sentence), or `none`.
- `evidence`: one quote from the document (at most 300 characters) that supports your `defect_real` answer.
- `confidence`: `high` or `low`. Use `low` whenever you had to guess.

Example line (format only, not a real case):
{{"case_id": "x-00", "defect_real": "no", "evidence_sufficient": "n/a", "evidence_minimal": "n/a", "other_blocker": "none", "evidence": "...", "confidence": "high"}}

Write all {n} lines to `labels.jsonl` in the workspace root (the directory that holds this rubric). Use the Write tool.
"""

ADJ_RUBRIC = """# Adjudication rubric (read fully before you start)

You adjudicate {n} cases on which two independent labelers disagreed, were unsure, or agreed that the quoted evidence needs
correcting. For each case you get the document, the proposed defect, the proposed quotes and BOTH labelers' answers with their
evidence. Decide from the document text yourself; do not simply pick a side.

## Blocking (the grading check, verbatim from the review rules)

For each finding before you mark it blocking, write the sentence "An implementer who follows the stated text as written builds X,
and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each
other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion
cannot pass. Grade it Medium (NOT blocking) when the sentence needs a guess that the implementer picks the worse of two readings
the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an
unspecified edge case) rather than a stated text that does harm. An apparent conflict that the document itself resolves (a
condition that separates the cases, an explicit exception) is not a defect.

## Fields (one JSON object per case, one line per case, in `adjudication.jsonl`)

- `case_id`
- `defect_real`: `yes`, `no`, or `undecidable` (use `undecidable` only when the document text genuinely cannot settle it).
- `final_evidence_quotes`: when `defect_real` is `yes`, the MINIMAL set (2 or 3, rarely 1) of exact quotes from the document whose
  joint reading shows the defect. Start from the proposed quotes; drop one that is not needed; add the missing passage if the
  proposed set is insufficient. Each quote must be an exact, contiguous substring of one line of the document (copy it, do not
  paraphrase), at most 300 characters, and unique enough to locate. Use `[]` when `defect_real` is `no` or `undecidable`.
- `evidence_sufficient` and `evidence_minimal`: about YOUR `final_evidence_quotes` (`yes` when you were able to give a set;
  `n/a` when `defect_real` is `no`; `undecidable` otherwise).
- `other_blocker`: another blocking defect you noticed, or `none`.
- `reason`: one sentence.
- `confidence`: `high` or `low`.

Write all {n} lines to `adjudication.jsonl` in the workspace root (the directory that holds this rubric). Use the Write tool.
"""


def line_range(doc_text: str, quote: str) -> str:
    i = doc_text.find(quote)
    if i < 0:
        return "not found"
    a = doc_text.count("\n", 0, i) + 1
    b = a + quote.count("\n")
    return f"{a}-{b}"


def case_view(case: dict, doc_text: str) -> dict:
    """What a labeler sees about a case: opaque id, document file name, proposed defect, quotes with line numbers.
    Never author_intent, category, layer, group, family or variant metadata."""
    from p15common import datasets
    pk = datasets.label_packet(case, ["defect", "evidence_quotes", "doc"])["packet"]
    return {"case_id": case["case_id"], "document": "docs/" + pathlib.Path(pk["doc"]).name,
            "proposed_defect": pk["defect"],
            "proposed_evidence": [{"quote": q, "lines": line_range(doc_text, q)} for q in pk["evidence_quotes"]]}


def build_sandbox(sid: str, cases_view: list, doc_srcs: dict, rubric: str, extra_files: dict | None = None) -> pathlib.Path:
    sb = OFF / "sb" / sid
    if sb.exists():
        shutil.rmtree(sb)
    ws = sb / "ws"
    (ws / "docs").mkdir(parents=True)
    (sb / "home").mkdir()
    for name, src in doc_srcs.items():
        shutil.copyfile(src, ws / "docs" / name)
    (ws / "RUBRIC.md").write_text(rubric.format(n=len(cases_view)))
    (ws / "cases.json").write_text(json.dumps(cases_view, indent=1, ensure_ascii=False))
    for rel, content in (extra_files or {}).items():
        (ws / rel).write_text(content)
    return sb


def write_prompt(sid: str, brief: str) -> pathlib.Path:
    sb = OFF / "sb" / sid
    p = OFF / "prompts" / f"{sid}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(H.wrap(str(sb), brief, False))
    return p


def read_jsonl(path) -> list:
    p = pathlib.Path(path)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text().splitlines():
        ln = ln.strip()
        if ln.startswith("{"):
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
    return out


def write_jsonl(path, rows) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
