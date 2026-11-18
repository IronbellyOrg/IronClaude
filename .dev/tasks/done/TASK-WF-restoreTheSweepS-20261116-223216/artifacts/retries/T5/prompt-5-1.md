87cb74c0ee4bd092fb85664c19165d93c135b691
Review one task for spec compliance.

Task brief: ## Task 5: Update the design doc and run the full checks

Depends on: Task 3

In `docs/designs/orchestrator-mode.md`, update every statement that says rule 5 is inert or the names are uncaptured, found with `git grep -n -i "open item 6\|Rule 5\|agentWait\|inert\|not yet captured" docs/designs/orchestrator-mode.md`, in particular: the section 7.2 "Rule 5 (SP-24), one condition per line" bullet (near line 493) restated as `liveness_verdict == "live"`, `outcome == "in_progress"` (the `projection.outcome` field; `dispatch.status` is `dispatched` for a running worker), `agent_wait_present is True`, `agent_wait is None`, with the field sources now captured (`worker-show` `projection.liveness.verdict`, `projection.outcome`, and `agentWait` from `observation` then `terminal`) and a sentence that the meaning of a non-null `agentWait` is UNVERIFIED and that such a row is rule 4; the D7 row (near line 841) and the SP-24 mapping row (near line 877) so they say the restore happened with the real names (record the date 2026-11-16 and the capture file name `q24-orca-capture2-20261116.md`); the step 1.0a item 4 row (near line 914) with the observed names and values; open item 6 (near line 1003) marked resolved for `agentWait` presence, `liveness.verdict` and the outcome value, and still open (UNVERIFIED) for the non-null `agentWait` shape; the `tests/sweep/test_classify.py` row of the test table (near line 767) so it no longer says the `working` case expects `fallback` or that the four-condition case returns when Rule 5 is restored; and a short note that `status == "ready"` in rule 4 is the sweep's own marker for `task-list --ready` rows, not a `dispatch.status` value. Do not change the wording of the SP24 report footnote text quoted in the doc. Then run the whole verification and record the real counts.

Acceptance criteria:
T5.AC1: A Grep of `docs/designs/orchestrator-mode.md` for "Rule 5 is inert", "inert" next to Rule 5, and "show `status` \"in_progress\"" style leftovers (`status == "in_progress"`) finds none, and every remaining mention of open item 6 says what is still UNVERIFIED.
T5.AC2: `uv run pytest tests/sweep -q` passes with no failures (record passed, failed and skipped counts) and `uv run ruff check src/superclaude/cli/sweep tests/sweep` reports no errors.
T5.AC3: `make verify-sync` passes, and `git diff --stat` shows no change under `.claude/`, none to `ALLOWED_ORCA` or `ALLOWED_GIT`, and none to the `SP24` text in `src/superclaude/cli/sweep/report.py`.
Global constraints: 
- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.
Start sha: 87cb74c0ee4bd092fb85664c19165d93c135b691
Diff against the start snapshot: docs/designs/orchestrator-mode.md: 6 lines changed, none added or removed (lines 493, 767, 841, 877, 914, 1003)
--- OLD line 493:
- Rule 5 (SP-24), one condition per line: `liveness_verdict == "live"`; `status == "in_progress"`; `agent_wait_present is True`; `agent_wait is None`. All four must hold once the names are known. Until step 1.0a item 4 records them (open item 6) Rule 5 is inert: it returns None and a row that would reach it falls to the fallback, and these four conditions are kept in `classify.py` as the text to restore. Field sources (the `worker-show` field names, the `live` and `in_progress` values and the `agentWait` key are NOT yet captured, UNVERIFIED): `liveness_verdict`, `status`, `agentWait` presence and value would come from `worker-show`; `worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231).
+++ NEW line 493:
- Rule 5 (SP-24), one condition per line: `liveness_verdict == "live"`; `outcome == "in_progress"`; `agent_wait_present is True`; `agent_wait is None`. All four must hold. Restored on 2026-11-16 from a read-only capture of a running worker (`q24-orca-capture2-20261116.md`): `dispatch.status` is `dispatched` for that worker, and the word `in_progress` is the value of `projection.outcome`, so the rule tests `outcome`, not `status` (the earlier text of this line named `status`, which could never match). Field sources, captured: `liveness_verdict` is `projection.liveness.verdict` (`live`); `outcome` is `projection.outcome` (`in_progress`); `agent_wait_present` and `agent_wait` come from `observation.agentWait`, else `terminal.agentWait` (the key is present with value null for a running worker). A non-null `agentWait` was never captured, so what it looks like and what it means are UNVERIFIED; such a row is taken by rule 4 (waiting on a person) before rule 5 and is never `working`. A finished worker shows `completed`, `succeeded` and `unverifiable` and is not `working`. `status == "ready"` in rule 4 is not a `dispatch.status` value: the sweep sets it itself on the rows it builds from `task-list --ready`. `worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231).

--- OLD line 767:
[row start omitted] One parametrized case per rule 1 to 9 (the `working` case expects rule `fallback` while Rule 5 is inert, open item 6), reaching every name in `CLASSES` except `working` until Rule 5 is restored; rule-name order pin `[r.name for r in RULES]`; window cases (5 h old row, windows under and at 6 h; record timestamp older than mtime); the four FR-008 inputs; a late-heartbeat live row is never `stalled (proved)` (SPEC line 444); the two FR-009 cases with the exact note; rule 1 decline notes (M6); the rule 5 case (it never matches while the names are uncaptured; the four-condition case returns when Rule 5 is restored); [row rest unchanged]
+++ NEW line 767:
[row start omitted] One parametrized case per rule 1 to 9 (the `working` case expects rule `working`: Rule 5 was restored on 2026-11-16), reaching every name in `CLASSES`; rule-name order pin `[r.name for r in RULES]`; window cases (5 h old row, windows under and at 6 h; record timestamp older than mtime); the four FR-008 inputs; a late-heartbeat live row is never `stalled (proved)` (SPEC line 444); the two FR-009 cases with the exact note; rule 1 decline notes (M6); the rule 5 cases (the four-condition row, `liveness_verdict` `live` and `outcome` `in_progress` with `agentWait` present and null, is `working`; each single broken condition is not; `status` `in_progress` with no `outcome` is not; a non-null `agentWait` is rule 4, never `working`); [row rest unchanged]

--- OLD line 841:
| D7 | Rule 5 at line 253 reads only "`live`, `in_progress`, `agent_wait_present` and null"; the report says nothing about classes Phase 1 cannot observe | Rule 5 restated as four conditions, one per line, with each field source; the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred | SP-24 | 7.2, 7.5 |
+++ NEW line 841:
| D7 | Rule 5 at line 253 reads only "`live`, `in_progress`, `agent_wait_present` and null"; the report says nothing about classes Phase 1 cannot observe | Rule 5 restated as four conditions, one per line, with each field source; the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred. Update 2026-11-16: the live capture showed `in_progress` is `projection.outcome` (`dispatch.status` is `dispatched`), so condition 2 tests `outcome`; Rule 5 is active. The footnote covers stalled and fenced only: a zero `working` count now means no row met the four conditions. What a non-null `agentWait` means stays UNVERIFIED | SP-24 | 7.2, 7.5 |

--- OLD line 877:
| SP-24 | Applied as D7 | 7.2, 7.5 |
+++ NEW line 877:
| SP-24 | Applied as D7; Rule 5 restored with the captured names on 2026-11-16 | 7.2, 7.5 |

--- OLD line 914:
| 4 | `worker-show --dispatch <dispatch> --json` field names: the field that can carry `session_join` (a Claude session id, pane key or terminal handle), `agentWait` presence and value, `liveness.verdict`, `status`, and whether `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are present and in what shape (the static bundle read gives the SQLite form `YYYY-MM-DD HH:MM:SS` UTC for `dispatchedAt` only; the form of `completedAt` is UNVERIFIED and either that form or ISO 8601 is possible, which 7.2 accepts; `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`); also record, for one worker, whether `dispatchedAt` is earlier than the first transcript record of its session, and whether `completedAt` is set for `failed` and `circuit_broken` rows | Rule 5, the join paths of section 7.2, the path-B time window, GQ-108, open item 23 |
+++ NEW line 914:
| 4 | `worker-show --dispatch <dispatch> --json` field names: the field that can carry `session_join` (a Claude session id, pane key or terminal handle), `agentWait` presence and value, `liveness.verdict`, `status`, and whether `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are present and in what shape (the static bundle read gives the SQLite form `YYYY-MM-DD HH:MM:SS` UTC for `dispatchedAt` only; the form of `completedAt` is UNVERIFIED and either that form or ISO 8601 is possible, which 7.2 accepts; `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`); also record, for one worker, whether `dispatchedAt` is earlier than the first transcript record of its session, and whether `completedAt` is set for `failed` and `circuit_broken` rows. Observed 2026-11-16 for a running worker (`q24-orca-capture2-20261116.md`): `dispatch.status` `dispatched`, `projection.outcome` `in_progress`, `projection.liveness.verdict` `live`, `agentWait` present with value null at `observation.agentWait` and at `terminal.agentWait`; for a finished worker `completed`, `succeeded`, `unverifiable`. A non-null `agentWait` was not seen | Rule 5, the join paths of section 7.2, the path-B time window, GQ-108, open item 23 |

--- OLD line 1003:
| 6 | `worker-show` names for `agentWait`, `liveness.verdict` and `status` | Step 1.0a item 4 | Rule 5 cannot match; rows fall to the fallback |
+++ NEW line 1003:
| 6 | `worker-show` names for `agentWait`, `liveness.verdict` and `status` | Step 1.0a item 4 | Resolved 2026-11-16 for a running worker: `agentWait` (present, null), `liveness.verdict` `live` and `projection.outcome` `in_progress` are captured and Rule 5 is active. Still UNVERIFIED: what a non-null `agentWait` looks like and means (a row with one is rule 4, never `working`) |

diff --git a/src/superclaude/cli/sweep/classify.py b/src/superclaude/cli/sweep/classify.py
index a470eddaa..9163b60ba 100644
--- a/src/superclaude/cli/sweep/classify.py
+++ b/src/superclaude/cli/sweep/classify.py
@@ -226,7 +226,7 @@ def _rule_fenced(row: SessionRow, ctx: SweepContext) -> Classification | None:
 def _rule_waiting_signal(row: SessionRow, ctx: SweepContext) -> Classification | None:
     orca, contract = row.orca, row.contract
     if orca is not None and orca.agent_wait is not None:
-        since = orca.agent_wait_since  # reserved: set by nothing yet (open item 6)
+        since = orca.agent_wait_since  # reserved: no captured field names a wait time
         notes: tuple[str, ...] = ()
         evidence = "agent_wait is non-null (worker-show agentWait)"
         if since is not None and since > ctx.now:

Codegraph context: index_state fresh (checked 2026-11-16T22:34:54Z); call codegraph only when index_state: fresh, never to widen scope. The design-doc rows are shown whole (old, then new) except line 767, a very long table row, where only the span holding both edits is shown; the full lines are in docs/designs/orchestrator-mode.md. Results after the change: uv run pytest tests/sweep -q gives 649 passed, 0 failed, 0 skipped; uv run ruff check src/superclaude/cli/sweep tests/sweep passes. make verify-sync first failed with MISSING entries in .claude/skills for skills this task did not touch, because this fresh worktree's gitignored .claude/ mirror had never been synced; after make sync-dev (which writes only the gitignored .claude/ mirror) make verify-sync prints All components in sync. git status shows no .claude path, and git diff --stat shows no change to ALLOWED_ORCA or ALLOWED_GIT or to the SP24 text in report.py. The classify.py hunk is a one-line comment fix (the old comment said the wait time was set by nothing yet, open item 6).
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
