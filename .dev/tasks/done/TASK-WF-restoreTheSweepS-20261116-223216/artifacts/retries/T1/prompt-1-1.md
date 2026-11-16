55d98f621897eef78feb46d59222dd6b645f90de
Review one task for spec compliance.

Task brief: ## Task 1: Add the sanitized running-worker fixture and record it in the fixtures source note

Create `tests/sweep/fixtures/captured-worker-show-running.json` as the full `worker-show` envelope (top-level keys `id`, `ok`, `result`, `_meta`, the same shape as `tests/sweep/fixtures/captured-worker-show-1.json`) copied from the JSON block under "worker-show output" in `/home/coder/captures/q24-orca-capture2-20261116.md`. Apply the sanitize rules already written in `tests/sweep/fixtures/SOURCES.md`: replace the home prefix `/home/coder` with `/home/user` and the account name `coder` with `user` (rules 1 and 2); replace every UUID (envelope id, runtime epoch, runtime id, pane key parts, incarnation id, terminal handle UUID part, worktree id) with a stable fake UUID `00000000-0000-4000-8000-<12 digits>` numbered after the highest number already used in the other fixtures (rule 3; find it with a Grep over `tests/sweep/fixtures`); keep the `ctx_`, `run_`, `task_` and `wtr_` ids as captured (rule 4); replace the two `[text omitted]` values (`terminal.title`, `terminal.preview`) with `<text removed>` (rule 5). Keep every field name and value type, in particular `dispatch.status` `dispatched`, `projection.outcome` `in_progress`, `projection.liveness.verdict` `live`, `terminal.agentWait` null and `observation.agentWait` null. Add one row for the new file to the Files table in `tests/sweep/fixtures/SOURCES.md` (source: the 2026-11-16 second Q24 read-only capture, command `orca-ide orchestration worker-show --dispatch ctx_6c922cf310da --json`, exit 0, rules beyond 1 to 3: text of title and preview removed, a running worker with no non-null `agentWait` seen) and update the file count sentence in the Notes section of that file. Grep `tests/` and `docs/` for a pinned fixture count or folder listing (for example "19 files" or a glob of `captured-*.json`) and update any such pin.

Acceptance criteria:
T1.AC1: `tests/sweep/fixtures/captured-worker-show-running.json` parses as JSON and `jq` shows `.result.dispatch.status` `"dispatched"`, `.result.projection.outcome` `"in_progress"`, `.result.projection.liveness.verdict` `"live"`, `.result.terminal.agentWait` and `.result.observation.agentWait` both `null` (key present).
T1.AC2: The file contains no `coder` account name, no `/home/coder`, no real UUID from the capture, and no prompt or message text: a Grep for `coder`, `/home/coder` and for each original UUID of the capture returns nothing in the new file.
T1.AC3: `tests/sweep/fixtures/SOURCES.md` lists the new file and its sentence about the number of files is correct; `uv run pytest tests/sweep -q` still has the same pass count as before this task (no test depends on the new file yet).
Global constraints: 
- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.
Start sha: 55d98f621897eef78feb46d59222dd6b645f90de
Diff against the start snapshot: diff --git a/tests/sweep/fixtures/SOURCES.md b/tests/sweep/fixtures/SOURCES.md
index ff45ffc97..b18212a71 100644
--- a/tests/sweep/fixtures/SOURCES.md
+++ b/tests/sweep/fixtures/SOURCES.md
@@ -22,6 +22,7 @@ All files here were copied from the step 1.0a read-only capture (item 7.16) and
 | `captured-worker-show-3.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_7c86fffa9716 --json` | 0 | Same. |
 | `captured-worker-show-4.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_9a3728b21883 --json` | 0 | Same. |
 | `captured-worker-show-5.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_dad78c5c1332 --json` | 0 | Same. |
+| `captured-worker-show-running.json` | not in the step 1.0a probe | `orca-ide orchestration worker-show --dispatch ctx_6c922cf310da --json` (second Q24 read-only capture, 2026-11-16; a worker that was running: `dispatch.status` `dispatched`, `projection.outcome` `in_progress`, `projection.liveness.verdict` `live`, `agentWait` null on both `terminal` and `observation`) | 0 | Rules 1 to 3 and 5 (the `title` and `preview` text was already omitted in the source capture and reads `<text removed>`); the 7 UUIDs are numbered 55 to 61, after the highest number used above. Only a null `agentWait` was seen; a non-null value was never captured (UNVERIFIED). |
 | `captured-task-list-ready.json` | 5 | `orca-ide orchestration task-list --ready --run run_a4723d345399 --json` | 0 | None. Empty `tasks` list. |
 | `captured-task-list.json` | 5 | `orca-ide orchestration task-list --run run_a4723d345399 --json` | 0 | Rule 5 (`spec` and long `result` text removed). 5 tasks. |
 | `captured-worktree-ps.json` | 6 | `orca-ide worktree ps --json` | 0 | Rules 5 and 6 (3 of 28 worktrees kept). |
@@ -37,6 +38,6 @@ All files here were copied from the step 1.0a read-only capture (item 7.16) and
 
 ## Notes
 
-- Items 1 and 13 of the capture are plain text, not JSON. Each is stored as a small JSON wrapper that holds the captured text unchanged, so every fixture here is a `captured-*.json` file (19 files) and the folder holds only those and this file. A first version stored them as `.txt` and plain tab-map files; the item 7.20 check on this folder allows only `captured-*.json` and `SOURCES.md`, so they were converted (logged in `### Phase 7 Findings`).
-- All five workers in this capture had exited (`liveness.verdict` `exited`, `dispatch.status` `completed`). No fixture shows a live worker, a `failed` or `circuit_broken` row, a bound `run-current`, a second `worker-list` page or the Orca-unavailable shape; those stay UNVERIFIED (`phase-outputs/discovery/1.0a-facts.md`).
+- Items 1 and 13 of the capture are plain text, not JSON. Each is stored as a small JSON wrapper that holds the captured text unchanged, so every fixture here is a `captured-*.json` file (20 files) and the folder holds only those and this file. A first version stored them as `.txt` and plain tab-map files; the item 7.20 check on this folder allows only `captured-*.json` and `SOURCES.md`, so they were converted (logged in `### Phase 7 Findings`).
+- All five workers in the step 1.0a capture (`captured-worker-show-1.json` to `-5.json`) had exited (`liveness.verdict` `exited`, `dispatch.status` `completed`). Only `captured-worker-show-running.json` shows a live worker. No fixture shows a `failed` or `circuit_broken` row, a bound `run-current`, a second `worker-list` page or the Orca-unavailable shape; those stay UNVERIFIED (`phase-outputs/discovery/1.0a-facts.md`).
 - The sanitized UUID numbering is stable only for the file set above; regenerating from a new capture renumbers them.

NEW UNTRACKED FILE (not in the start snapshot): tests/sweep/fixtures/captured-worker-show-running.json, 212 lines, sha256 e03383c08618a372. Its full contents are the file on disk: Read it. No other file changed. Test run after the change: uv run pytest tests/sweep -q gives 636 passed (same as before).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
