4d156b3d9a00ca748b1e48a815817863c8d98c62
Review one task for spec compliance.

Task brief: ## Task 13: Write the panel launcher, the fallback logic and the integration tests

Depends on: Task 12

Follow `RL/IMPLEMENTATION.md` step 5 (launcher) and `RL/DESIGN.md` sections 2.1, 2.2, 7.5, 8 and 9.1, 9.6, 10, REQ-12, REQ-27, REQ-30, REQ-46. Create `RL/bin/run-panel.sh --arm {Z0-raw|Z0|K|RL} --panel {primary|haiku|sonnet} --doc <id> --replicate <n> --block <n> --seed <int> --run-id <id> [--b <seconds>] [--dry-run]` writing to `RL/runs/<run-id>/`: check the sandbox is clean (`git status --porcelain`, K4), start the panel clock before the lens render, render briefs (RL arm: lens render with fallback to the Z0 briefs and `fallback=true` decided before any reviewer starts; no source drops C2), `--dry-run` writes `briefs/`, `lens/`, `run.json`, prints the three `claude` command lines with brief sha256 and starts nothing, start three reviewers in parallel under the hang guard, record `rev_end`, run `rl/cli.py check` and (ember only, `ledger_missing`, `reask_allowed`) `rl/cli.py reask` and a re-check, set `check_skipped=true` on any exception and merge the raw reports, stop the clock, then outside the clock run `scaffold/normalise.py` (order: check, then H2, then merge), build `resolution.json`, call `superclaude review merge --ledger ... --doc ... --round 1 --report <rid>=... --resolution ... --out ...` (a killed or invalid reviewer is absent; `merge_refused` is recorded, not re-run), run the sandbox-clean check, write `run.json` and `timing.json` (fields of `RL/DESIGN.md` 2.2 and 9.3 including `reask_s`, `panel_elapsed_s`, `slowest_reviewer_s`, row cap, `b`, `c`, `concurrent_panels_at_start`). Exit codes: 0 done, 2 usage or sandbox invalid, 3 `no_budget`, 4 refused. No verifier step exists and `VERIFIER` defaults to 0.

Write the integration tests (marker `slow`) in `RL/tests/test_run_panel_fake.py` (`test_long_anchor_survives_h2_then_merge`, `test_forced_exception_in_check_merges_as_written`, `test_ember_reask_runs_once_and_is_accepted`, `test_reask_rejected_when_findings_differ`, `test_no_reask_when_clock_too_late` with `--b 1`, `test_luna_ledger_missing_is_not_reasked`, `test_reask_failure_keeps_original_report`, `test_reask_not_counted_as_retry`, `test_repaired_rows_never_promoted`, `test_sleeping_reviewer_killed`, `test_no_retry_on_failure`, `test_killed_reviewer_absent_from_merge`, `test_order_check_then_h2_then_merge`), `RL/tests/test_fallback.py` (`test_forced_exception_in_lens_render_runs_z0_briefs`, `test_invalid_lens_table_falls_back`, `test_fallback_decided_before_first_reviewer_starts`), `RL/tests/test_sandbox_clean.py::test_dirty_after_run_is_flagged` (K4), `RL/tests/test_run_json_fields.py::test_fields_match_sibling_schema` (DR-12), `RL/tests/test_blindness.py::test_merged_report_has_no_telemetry_keys`, `RL/tests/test_verifier_off_path.py` (REQ-46: `test_no_verifier_step_in_clock`, `test_verifier_default_off`, `test_verifier_time_excluded`) and the REQ-26 test `no_budget` exit code 3. Then run rehearsal A7 of `RL/TESTING.md` section 5.1 on the fake claude over the real sandbox of one study document: `export SW_SB_ROOT=/tmp/evalsb-recipe-rehearsal`, `bash $RL/bin/build-sandbox.sh TASK-WF-designSpec-20261107-075614`, then `PATH=$RL/tests/fakes:$PATH FAKE_SCENARIO=ok FAKE_CALL_LOG=/tmp/rl-rehearsal-calls.log bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-designSpec-20261107-075614 --replicate 1 --block 1 --seed 1 --run-id rehearsal-rl`. Do not open any ground-truth file in the sandbox or the repository.

Acceptance criteria (ids added by the orchestrator, in source order):
T13.AC1: `$T $RL/tests/test_fake_claude_rl.py $RL/tests/test_clock.py $RL/tests/test_hang_guard.py $RL/tests/test_fallback.py $RL/tests/test_run_panel_fake.py $RL/tests/test_sandbox_clean.py $RL/tests/test_run_json_fields.py $RL/tests/test_blindness.py $RL/tests/test_verifier_off_path.py -q` exits 0 (REQ-02 whole path, REQ-12, REQ-27 whole path, REQ-30, REQ-46).
T13.AC2: The rehearsal log `/tmp/rl-rehearsal-calls.log` shows exactly three review lines and no model was started; the run folder holds `run.json`, `timing.json`, `check/check.json`, `merged/merged-1.md` and a merged report with none of `probe`, `src`, `class`, `ledger-v1`.
T13.AC3: A forced `RL_FORCE_EXC=lens` run uses Z0 briefs with `fallback: true` before the first fake call; `RL_FORCE_EXC=check` merges the raw reports with `check_skipped: true`.
T13.AC4: The Z0, K and Z0-raw arms render and run through the same script (K adds only the copied K paragraph; Z0-raw uses the base brief and the raw sandbox built by `bin/build-sandbox.sh --raw`).

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: 4d156b3d9a00ca748b1e48a815817863c8d98c62
Diff against the start snapshot: (the diff is 1728 lines; it is saved as a file: read /tmp/rl-impl/T13/diff.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

Codegraph context: index_state: fresh; checked_at: 2026-11-14T23:20:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

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
