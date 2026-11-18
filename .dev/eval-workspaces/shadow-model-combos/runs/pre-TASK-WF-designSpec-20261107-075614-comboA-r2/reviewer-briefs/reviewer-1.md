# Reviewer 1 brief - persona: analyzer

Audit target: UC-1 pre-execution. Spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, issue #375, pr-submit merge guard). Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks, 5 phases).

ATTRIBUTION NOTE (binding): this is a PRE-execution audit of the frozen spec+plan pair. The spec's facts F1-F13 are pinned at base commit e8db2fe6 (2026-11-07); verify anything pre-landing with `git show e8db2fe6:<path>` if needed. HEAD has since evolved (the feature landed); do NOT file findings that rest on HEAD source text - audit the plan's coverage against the frozen spec only. NEVER read anything under .dev/tasks/done/TASK-WF-designSpec-20261107-075614/ (it is the implement-history answer key).

Your lens: root-cause and internal-consistency of the plan's CORE LOGIC tasks (Tasks 2-6, 11): do the pure-module contracts, fold semantics, decision tables, event schema, flag and script contracts faithfully encode spec sections 3, 4.1-4.4? Look for contradictions between tasks, unimplementable contracts, miscounted enumerations, import hazards.
## T1 card excerpt
Verbatim excerpt from t1-card.md (hypotheses + core-contract grounding slice):

> ## Hypotheses (candidate findings, pre-calibration)
>
> - **H1 [MINOR - spec wording]** Spec F5 calls `--conflict-max-tier` "the one enum flag of this parser (`choices=`)" but `--monitor` also uses `choices=` at fsm.py:81 at the pin. Not load-bearing for the plan (Task 6 copies the SHAPE of --conflict-max-tier, not a uniqueness claim), but the fact as stated is imprecise. Grounded: fsm.py:80-81,103-109 at pin.
> - **H3 [CONFORMANCE - verified]** All 13 tasks map onto spec sections 3-10 with no uncovered requirement found at T1 depth; the dependency graph is complete; the add-last classification discipline and per-task `make sync-dev` are restated everywhere the spec demands them.
> - **H5 [note]** The spec's own line-number citations (models.py:24, run_log.py:117-125, test_run_log.py:171-175, test_codex_reviews.py:441, test_static_grep.py:791) were all verified accurate at the pin.
>
> ## Grounding (verified at pin e8db2fe6)
>
> EventType exactly 43 members; merge_guard.py absent; RunLog.append rejects unknown types; detect_crash_window push-only, pairs by idempotency_key; CONFLICT_CYCLE_PREFIXES = ("sync-", "conflict-"); recovery.py imports run_log; run_log imports only models; conflicts imports fsm; fsm imports loop_guard/models/severity_router - so run_log -> merge_guard -> conflicts -> fsm closes NO cycle; BRANCH_A_LANDED/"landed", BRANCH_B_NOT_LANDED, BRANCH_C_AMBIGUOUS (recovery.py:40-42); FIX_APPLIED/PUSH_INITIATED/PUSH_COMPLETED/REREVIEW_REQUESTED exist (models.py:63,69-70,84).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:05:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Grounding is by direct Read: the spec (`.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`) and plan (`.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`) are on disk. Verify code claims ONLY against the pin `git show e8db2fe6:<path>` (Bash is not available to you; use the excerpts below and the two input documents; where a code fact matters and is not excerpted, cite the spec/plan text instead of unverified code).

### Key verified code facts (at pin e8db2fe6, orchestrator-verified)

- EventType: exactly 43 members at pin (models.py); FIX_APPLIED, PUSH_INITIATED, PUSH_COMPLETED, REREVIEW_REQUESTED exist (models.py:63,69,70,84).
- RunLog.append rejects unknown event_type (run_log.py:117-125 docstring "43 closed").
- detect_crash_window is push-only, pairs by idempotency_key (recovery.py:69-92); BRANCH_A_LANDED="landed", BRANCH_B_NOT_LANDED="not_landed", BRANCH_C_AMBIGUOUS="ambiguous" (recovery.py:40-42); recovery.py imports run_log (recovery.py:37).
- CONFLICT_CYCLE_PREFIXES=("sync-","conflict-") (conflicts.py:46); is_conflict_cycle (conflicts.py:1242).
- Import chain: run_log->models; conflicts->fsm,models; fsm->loop_guard,models,severity_router. NO cycle through merge_guard->conflicts.
- --conflict-max-tier uses choices=[0,1,2] (fsm.py:103-109); --monitor ALSO uses choices= (fsm.py:80-81) - spec F5's "one enum flag" wording is imprecise.

## Coverage slice

Your assigned rows (INF ids from the union matrix; all 45 rows resolved COVERED at T1 - your job is to pressure-test that resolution for YOUR rows):

INF-003..INF-021 (19 rows: core-decides rule, behaviour table, purity/imports, decision-function contracts incl. applied_edits/held_cycle_published/BM-RANCH/publish/guard_status, RECONCILE reasons, EventType 43->45, fsync ordering, fold dict/effects, original_is_draft, flag effectiveness, script exit codes)

The full matrix with per-row quotes is at artifacts/coverage-matrix.yaml and artifacts/pass2-inferred.yaml (Read them if you need the row quotes).

Report each finding as one JSON line per the instruction above. A zero-finding result is valid; if you verify your rows are covered, return an empty findings block and list the row ids you verified under `coverage_rows` in EACH finding only when you have a finding; for a zero-finding card write exactly `[]` inside the fence plus your `coverage_rows_observed` line AFTER the fence as a plain line listing the INF ids you checked.
