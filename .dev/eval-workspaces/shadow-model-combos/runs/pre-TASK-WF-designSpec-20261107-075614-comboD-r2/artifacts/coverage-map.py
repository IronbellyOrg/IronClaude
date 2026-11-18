"""Step 1B.0 / 1B.2b coverage mapping for the sc:reflect UC-1 run (deterministic; no LLM in matching).

Pass 1: ID_REGEX over spec and tasklist outside fenced code. Pass 2: quote-pinned INF rows below; a row whose
quote is not a verbatim substring of ONE spec line is INVALID and dropped. Matching: containment >= 0.6.
Usage: uv run python coverage-map.py <spec> <tasklist> <out.json>
"""
import json
import re
import sys

spec_path, tl_path, out_path = sys.argv[1:4]
spec_lines = open(spec_path, encoding="utf-8").read().splitlines()
tl_text = open(tl_path, encoding="utf-8").read()
ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")


def ids_outside_fences(lines):
    found, fenced = [], False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            found += [(m.group(1), n) for m in ID_REGEX.finditer(line)]
    return found


pass1_spec = ids_outside_fences(spec_lines)
pass1_tl = ids_outside_fences(tl_text.splitlines())

# Pass 2 rows: (quote). Ids are assigned in order, INF-001...
QUOTES = [
    '''engage at the first verified Medium-or-higher finding routed to a fix''',
    '''release when the fix push is confirmed on the PR head, before replies and the re-trigger''',
    '''an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports''',
    '''Nothing mutates. A held guard found in the log is reported with the clear command.''',
    '''Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger; a held guard is reported with the clear command.''',
    '''Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made.''',
    '''The line is written in the SKILL.md output table, which every run loads, not only in the guard ref.''',
    '''Read, decide, request, `--to draft`, settle. Print the clear command once.''',
    '''Settle `skipped/already_draft`, phase `disabled`, never mutate.''',
    '''Diagnosis ends with no edit (`applied_edits == 0`)''',
    '''Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing.''',
    '''Release, cause `pushed`, before reply, resolve and the S5a re-trigger.''',
    '''Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report.''',
    '''Do not release; report `held (timeline unreadable)`; keep pushing.''',
    '''Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`.''',
    '''PR stays draft; report `held` with the clear command.''',
    '''No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conflicts.is_conflict_cycle`.''',
    '''Never collides with `CONFLICT_CYCLE_PREFIXES`.''',
    '''1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none.''',
    '''Guard requests with no matching settle, matched by `idempotency_key`''',
    '''`applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field''',
    '''`True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id`''',
    '''a test imports both modules and asserts equality, because the core cannot import `recovery`.''',
    '''phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded)''',
    '''A halt with reason `draft_guard_unavailable` reports `unavailable`.''',
    '''`classify_toggles(guard, read)` (the only foreign-toggle test; no actor identity, F11):''',
    '''`failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action''',
    '''`mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)`''',
    '''`RETRY_RELEASE` (release first, then re-decide)''',
    '''`guard` exists and `classify_toggles == "foreign"`''',
    '''`guard is None` and `read.is_draft`''',
    '''`ENGAGE`; `notes` carries `auto_merge_armed` when set''',
    '''`push_completed` and `read.head_sha == target_sha`''',
    '''`HOLD(head_mismatch or push_not_completed)`''',
    '''`(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`)''',
    '''`RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous`''',
    '''re-enter `release_decision` with `push_completed=True`''',
    '''`dangling_branch == "not_landed"` and phase `HELD`''',
    '''`HOLD(ambiguous_remote_tip)`''',
    '''Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`):''',
    '''appended and fsynced BEFORE the draft/ready call''',
    '''`idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction)''',
    '''default `None`, added to `_NEW_KEY_DEFAULTS`''',
    '''It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded.''',
    '''`original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one.''',
    '''The matcher `pending_requests` uses the same key pairing as `detect_crash_window`, but over the two guard event types, so push recovery and guard recovery stay independent.''',
    '''`choices=["draft", "off"]` (same shape as `--conflict-max-tier`, F5)''',
    '''Effective only at `--monitor 3`; accepted and inert below.''',
    '''`RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated.''',
    '''`set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing.''',
    '''Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); 2 usage; 127 missing dependency.''',
    '''`--to` is idempotent, so a retry or a resume re-issue is safe.''',
    '''Loaded lazily at L3 Wave 3, Wave 6 and Wave 8.''',
    '''No new python fence (the one-fence tests,''',
    '''Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git`''',
    '''Overlay note: the guard phases are fold values, not `MonitorState` members.''',
    '''`--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling".''',
    '''Flag row and a paragraph: what it does, the clear command, `held` meaning, default on.''',
    '''A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>`''',
    '''The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key.''',
    '''With `--merge-guard off` nothing changes.''',
    '''is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py`''',
    '''The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only).''',
    '''Acceptance trace (must appear in this order in the run log)''',
    '''next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`.''',
    '''Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result''',
    '''so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record.''',
    '''Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`''',
    '''the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`''',
    '''export the public guard names''',
    '''fake `gh` on PATH, exit codes 0/1/2/127, `--repo` on every call, an old log folds to `draft_guard: None`''',
    '''A static test asserts `merge_guard.py` has no `gh` or `git` word.''',
    '''a test that `BRANCH_LANDED`, `BRANCH_NOT_LANDED` and `BRANCH_AMBIGUOUS` equal the `recovery.py` constants''',
    '''a crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger''',
    '''ledger test: observed above `run_toggles + slack`; ready-then-draft round trip (FR-12, FR-13)''',
    '''No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`).''',
    '''The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly.''',
    '''Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number''',
    '''Declare dependencies completely, one `Depends on:` line per dependency''',
    '''The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet.''',
    '''The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get an acceptance criterion that a wrong implementation would fail.''',
    '''The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result.''',
    '''Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line.''',
    '''each ends with adding its `WRITE_VERB_CLASSIFICATION` entries (exact stripped line, category `never-worker`) and runs `uv run pytest tests/skills/test_worker_contract.py -q`.''',
    '''The L2 line is written into the SKILL.md output table; its acceptance criterion is a test that the literal line is in `SKILL.md`''',
    '''the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window`''',
    '''scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (pytest would collect them twice)''',
    '''is asserted on `RunLog.read_events()`''',
    '''the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string constants taken from the existing pins, not against `git show HEAD:`''',
    '''the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition.''',
]

STOP = set("""a an the and or but nor of to in on at by for with from as is are was were be been being it its this that these those
not no do does did will would shall should can could may might must has have had then than so such there here when where which
who whom whose if else also only any each every per via into onto over under after before between""".split())


def words(text):
    toks = re.findall(r"[a-z0-9_]+", text.casefold())
    return {t for t in toks if t not in STOP and len(t) > 1}


# Task items: each "## Task N:" section of the tasklist is one item.
tasks, cur = {}, None
for line in tl_text.splitlines():
    m = re.match(r"^## Task (\d+):", line)
    if m:
        cur = f"Task {m.group(1)}"
        tasks[cur] = []
    elif line.startswith("## "):
        cur = None
    if cur:
        tasks[cur].append(line)
task_words = {k: words("\n".join(v)) for k, v in tasks.items()}

rows, dropped = [], []
parsed_span_lines = set()  # no parsed rows when Pass 1 is empty; kept for the dedup rule
for i, q in enumerate(QUOTES, 1):
    nq = re.sub(r"\s+", " ", q).strip()
    hit = [n for n, l in enumerate(spec_lines, 1) if nq in re.sub(r"\s+", " ", l)]
    rid = f"INF-{i:03d}"
    if not hit:
        dropped.append({"id": rid, "quote": q, "reason": "quote not verbatim in a single spec line"})
        continue
    if hit[0] in parsed_span_lines:
        dropped.append({"id": rid, "quote": q, "reason": "overlaps a parsed requirement span"})
        continue
    qw = words(q)
    best_id, best_ratio = None, 0.0
    for tid, tw in task_words.items():  # tasks iterate in tasklist order: first-in-order tiebreak
        r = len(qw & tw) / len(qw) if qw else 0.0
        if r > best_ratio:
            best_id, best_ratio = tid, r
    method = "containment" if best_ratio >= 0.6 else "none"
    rows.append({"requirement_id": rid, "source": "inferred", "quote": q, "citation_line": hit[0],
                 "matched_task_ids": [best_id] if method != "none" else [], "match_method": method,
                 "best_ratio": round(best_ratio, 3), "content_words": len(qw)})

matched = [r for r in rows if r["match_method"] != "none"]
total = len(rows)
out = {
    "pass1_spec_ids": pass1_spec, "pass1_tasklist_ids": pass1_tl,
    "parsed_count": len({i for i, _ in pass1_spec}), "inferred_count": total, "inferred_dropped": dropped,
    "coverage_pct": None if not pass1_spec else None,  # parsed_total 0 -> null
    "coverage_pct_union": round(len(matched) / total, 4) if total else None,
    "unmapped_requirements": [], "unmapped_requirements_union": [r["requirement_id"] for r in rows if r["match_method"] == "none"],
    "coverage_degraded": "parsed-sparse" if total > len({i for i, _ in pass1_spec}) else None,
    "coverage_undefined": total == 0 and not pass1_spec,
    "task_count": len(tasks),
    "thin_matches_lt_0.75": [(r["requirement_id"], r["best_ratio"], r["matched_task_ids"]) for r in rows if 0.6 <= r["best_ratio"] < 0.75],
    "rows": rows,
}
json.dump(out, open(out_path, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1)[:3500])
