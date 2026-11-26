"""The pre-pass, S1 to S3 (DESIGN 2.1, 2.2, 2.4, 5.1, 10 rows 1 and 3).

    run(candidate, source, repo, *, seed, out, panel="primary")

takes exactly three inputs, the candidate file, the source file (or None) and the repository snapshot (a git checkout
that nobody changes while it runs), plus the seed. `out` is the folder of the run, not an input: the pre-pass writes
`out/prepass.tmp/` and renames it to `out/prepass/` only when every step succeeded. A failure removes the temporary
folder, leaves no `prepass/`, writes `out/prepass.error.json` (exception class, stage, extractor; no message, because a
message can hold an absolute path) and re-raises, so the caller falls back to the Z0 briefs (DESIGN 10 row 1).

    parse        plan.parse of the candidate and, when there is one, of the source (default format of both)
    find, top-K, attach   extractors.run_extractors (DD-10)
    select       select.select (DD-4, 5.1 steps 4 and 5)
    assign       assign.assign over the panel's reviewers (7.2); the seed only orders each reviewer's items
    render       render.items_json, render.render_sheets

Files in `prepass/`: items.json, candidates.json, assignment.json, prepass.json, prepass.log, sheets/<rid>.md and
sheets/<rid>.json. Determinism (DESIGN 2.4): no clock, no network, no model, no random source but assign's
random.Random(f"{seed}:{rid}"); every list is sorted or in document order; JSON is written by select.dumps (sorted
keys, ensure_ascii False, trailing newline); no absolute path is written anywhere. The only processes started are the
`git` calls of extractors.py (`rev-parse --show-toplevel`, `ls-files`, `grep`) on the snapshot.

Gaps in DESIGN 2.4 and 2.2 resolved here (each is a choice the design leaves open):
  P1  The panel is a parameter (default "primary"), not an input: assign needs its caps and DESIGN 2.4 does not name
      it. config/panels.json is read like config/values.json, so the output stays a function of the three inputs,
      the seed, the panel name and the frozen config.
  P2  `sweep_version` (DESIGN 2.4 lists it as a determinism input, no value is given) is the constant SWEEP_VERSION
      below; it is written to prepass.json and bumped by hand when the pre-pass logic changes.
  P3  Both documents are parsed with the default format ("plan"), as the extractor tests do. A source is read by E5
      through its lines only.
  P4  items.json holds the DESIGN 6.1 items from render.items_json (question, replicas, extractor, kind); an item that
      assign dropped as `dropped:cap_slots` is left out of it, and its candidates.json row gets that status and
      `drop_reason: cap_slots`, so the two files agree.
  P5  candidates.json gets one extra key, `classes_triggered` (the classes with at least one candidate found; DESIGN 10
      row 4 reads it there). prepass.json repeats it with the counts.
  P6  An empty sheet (no item selected, DESIGN 10 row 3) is a success: the files are written, `no_trigger` is true in
      prepass.json, every sheet text is empty. Only an exception is a pre-pass error.
  P7  The error file sits next to `prepass/`, not inside it, because `prepass/` must not exist after a failure.
  P8  An existing `prepass/` is replaced after the new one is complete (rmtree, then rename); a stale `prepass.tmp/`
      is removed first.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import traceback
from pathlib import Path

from sweep import assign, extractors, plan, rank, render, select

SWEEP_VERSION = "1"
SCHEMA = "sweep-prepass/1"
TMP_NAME, FINAL_NAME, ERROR_NAME = "prepass.tmp", "prepass", "prepass.error.json"
_EXTRACTOR_FRAME = re.compile(r"^(?:find|attach)_e(\d)$")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _counts(rows, key) -> dict:
    out: dict[str, int] = {}
    for r in rows:
        out[r[key]] = out.get(r[key], 0) + 1
    return dict(sorted(out.items()))


def _build(
    candidate, source, repo, seed, panel, tmp: Path, stage: list, available=None
) -> None:
    """Every step of the pre-pass; the files land in tmp. stage[0] names the step now running (for the error file)."""
    stage[0] = "parse"
    cand_bytes = Path(candidate).read_bytes()
    doc = plan.parse(cand_bytes)
    src_bytes = Path(source).read_bytes() if source is not None else None
    src_doc = plan.parse(src_bytes) if src_bytes is not None else None

    stage[0] = "find"
    ctx = extractors.Ctx(doc, source=src_doc, snapshot=Path(repo), seed=seed)
    scope_string = (
        ctx.scope_string
    )  # builds the scope: a snapshot that is not a git repository raises here
    cands = extractors.run_extractors(ctx)

    stage[0] = "select"
    sel = select.select(cands, seed, ctx.constants)

    stage[0] = "assign"
    asg = assign.assign(sel.items, panel=panel, available=available, seed=seed)
    cand_rows = sel.candidates
    for row in cand_rows:  # P4
        if row["item_id"] in asg.dropped:
            row["status"] = asg.dropped[row["item_id"]]
            row["drop_reason"] = "cap_slots"
            row["item_id"] = None

    stage[0] = "render"
    items = render.items_json(sel.items, asg, doc=doc)
    sheets = render.render_sheets(sel.items, asg, doc=doc)
    render.write(tmp, sheets)

    classes = sorted({r["class"] for r in cand_rows})  # P5
    cands_json = sel.candidates_json()
    cands_json["classes_triggered"] = classes
    (tmp / "candidates.json").write_text(select.dumps(cands_json), encoding="utf-8")
    (tmp / "items.json").write_text(select.dumps(items), encoding="utf-8")
    (tmp / "assignment.json").write_text(select.dumps(asg.to_json()), encoding="utf-8")

    info = {
        "schema": SCHEMA,
        "sweep_version": SWEEP_VERSION,
        "seed": seed,
        "panel": panel,
        "candidate_sha256": _sha(cand_bytes),
        "source_sha256": _sha(src_bytes) if src_bytes is not None else None,
        "no_source": ctx.no_source,
        "not_applicable": ctx.not_applicable,
        "scope": scope_string,
        "tasks_without_citations": sorted(ctx.tasks_without_citations),
        "blocks": len(doc.blocks),
        "block_kinds": _counts(doc.blocks, "kind"),
        "candidates": len(cand_rows),
        "candidates_by_status": _counts(cand_rows, "status"),
        "classes_triggered": classes,
        "classes_selected": sorted({i["class"] for i in items["items"]}),
        "items": len(items["items"]),
        "k": sel.k,
        "no_trigger": not items["items"],
        "constants": {key: ctx.constants[key] for key in ("K", "K_single", "cap")},
        "rank_table_sha256": rank.sha256(),
        "sheets": {
            rid: {
                "chars": len(s.text),
                "items": len(s.items),
                "sheet_trimmed": s.trimmed,
            }
            for rid, s in sorted(sheets.items())
        },
    }
    (tmp / "prepass.json").write_text(select.dumps(info), encoding="utf-8")

    log = [
        f"sweep prepass {SWEEP_VERSION}",
        f"seed: {seed}",
        f"panel: {panel}",
        f"blocks: {info['blocks']}",
        f"no_source: {str(info['no_source']).lower()}",
        f"candidates found: {info['candidates']}",
        *(f"  status {s}: {n}" for s, n in info["candidates_by_status"].items()),
        f"classes triggered: {', '.join(classes) or 'none'}",
        f"items selected: {info['items']}",
        f"no_trigger: {str(info['no_trigger']).lower()}",
        *(
            f"sheet {rid}: {v['items']} items, {v['chars']} characters, trimmed {str(v['sheet_trimmed']).lower()}"
            for rid, v in info["sheets"].items()
        ),
    ]
    (tmp / "prepass.log").write_text("\n".join(log) + "\n", encoding="utf-8")


def _error_info(exc: BaseException, stage: str) -> dict:
    ext = None
    for fr in traceback.extract_tb(exc.__traceback__):
        m = _EXTRACTOR_FRAME.match(fr.name)
        if m:
            ext = f"E{m.group(1)}"  # the innermost extractor frame wins
    return {"error": type(exc).__name__, "extractor": ext, "stage": stage}


def run(candidate, source, repo, *, seed, out, panel="primary", available=None) -> Path:
    """Run the pre-pass; return the path of `out/prepass/`. See the module text for the failure behaviour.

    `available` (P9): the reviewer ids that can still be launched, for the pre-launch reviewer-unavailable case
    (DESIGN 7.3, 10 row 9); None means all of the panel's reviewers. It goes to assign.assign unchanged.
    """
    stage = ["start"]
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    tmp, final, err = out / TMP_NAME, out / FINAL_NAME, out / ERROR_NAME
    shutil.rmtree(tmp, ignore_errors=True)  # P8
    err.unlink(missing_ok=True)
    tmp.mkdir()
    try:
        _build(candidate, source, repo, seed, panel, tmp, stage, available)
    except BaseException as e:
        shutil.rmtree(tmp, ignore_errors=True)
        if isinstance(e, Exception):
            err.write_text(select.dumps(_error_info(e, stage[0])), encoding="utf-8")
        raise
    shutil.rmtree(final, ignore_errors=True)
    tmp.rename(final)
    return final
