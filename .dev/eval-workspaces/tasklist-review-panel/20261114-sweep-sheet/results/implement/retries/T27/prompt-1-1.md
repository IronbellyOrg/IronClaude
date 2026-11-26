866bdcf71c20ee8fcf7ce7a16aaea4c626655976
Review one task for spec compliance.

Task brief: ## Task 27: Create the reviewer and panel launchers and the fake-claude integration tests

Depends on: Task 26, Task 25, Task 8, Task 7, Task 4

Create `bin/run-reviewer.sh` as the changes against `RR` listed in DESIGN 11.1: writes under `RUN/reviews`, candidate and source from `SB/cand/<doc>/`, brief from a file on stdin, `NOFALLBACK=1` required and one attempt (DD-8; no model ladder, no retry), `cd SB/<doc>/repo`, `timeout <hang guard>`, the same flags as `RR` line 48 (`--no-session-persistence`, `--permission-mode bypassPermissions`, `--disallowedTools Edit Write NotebookEdit`), the model-identity check kept, `BLOCK_OK` from `fnd.parse_block` after H2 on a temporary copy, `meta.json` and `cost.json` with `hang_s`, `killed` and `prompt_sha256`. Create `bin/run-panel.sh` (arms Z0-raw, Z0, K and SS: S0 sandbox check, S1 under `timeout` at `kill_s`, brief render, three reviewers in parallel with the hang guard, S5 under a catch that sets `check_skipped`, H2, the real `superclaude review merge` (`MRG.command` through the `superclaude review merge` command) with `resolution.json`, `run.json`, `timing.json`, the fallback decision taken before any reviewer starts, the `git status --porcelain` before and after every run, the reviewer-unavailable re-assign, and the `VERIFIER` default 0). Create `tests/test_run_panel_fake.py`, `tests/test_sandbox_clean.py` and `tests/test_blindness.py`, and extend `tests/test_kill_fallback.py` (from Task 26) with `test_sleeping_stub_is_killed_and_falls_back` (`SW_PREPASS_CMD=sleep 5`, `SW_KILL_S=1`: the process group is killed after about 1 s, no `prepass/` folder remains, the Z0 brief is used with an equal sha256, `run.json` has `fallback: true` and `reason: kill`) and `test_forced_exception_in_prepass_and_render_falls_back`.

Acceptance criteria:
- T27.AC1: `$T $SW/tests/test_run_panel_fake.py $SW/tests/test_sandbox_clean.py $SW/tests/test_kill_fallback.py $SW/tests/test_blindness.py -q` exits 0, and `$T $SW/tests/test_clock.py $SW/tests/test_hang_guard.py -q` still exits 0.
- T27.AC2: `test_run_panel_fake.py` has `test_prepass_finishes_before_first_reviewer`, `test_no_trigger_run` (reviewer brief hashes equal the Z0 hash, `no_trigger: true`), `test_sleeping_reviewer_killed`, `test_no_retry_on_failure` (`FAKE_CALL_LOG` shows one call per reviewer), `test_killed_reviewer_absent_from_merge`, `test_forced_exception_in_check_merges_as_written` (`check_skipped: true`, raw text given to the merge), `test_order_s5_then_h2_then_merge` and `test_no_source_run` (a document whose `source` is null: `run.json` has `no_source: true` and no brief holds the CB-1 text), and all pass with the fake `claude`.
- T27.AC3: `test_sandbox_clean.py::test_dirty_after_run_is_flagged` shows a fake reviewer that writes a file in the sandbox makes the run `sandbox_dirty`; `test_blindness.py::test_merged_report_has_no_telemetry_keys` shows `merged-1.md` and `merged/ledger.json` contain none of `probe`, `src`, `class` or `ledger-v1`.
- T27.AC4: `grep -rn "claude-opus-5-5" $SW/bin $SW/sweep $SW/scaffold` hits only `bin/judge-one.sh` once Task 28 exists (Task 33 re-runs it). `gitcheck $SW/bin` (Constraints) prints nothing over the scripts that exist after this task, `bin/build-sandbox.sh` passing because its writes are `git -C "$SBT" ...`; run over a temporary directory holding a file with the line `git add -A` it prints that line (the probe), and Task 33 re-runs it over the finished `bin/`.
- T27.AC5: Dependents: `analysis/analyze.py` reads `run.json` and `timing.json` (Tasks 29 and 30), `bin/run-schedule.sh` and `bin/run-spike.sh` call `bin/run-panel.sh` (Task 32).

(AC ids: T27.AC1 to T27.AC5, in the order of the bullets above.)
Global constraints: - Names used by every task. `SW` is the folder `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (repo-relative). Its three specification files are `SW/DESIGN.md`, `SW/IMPLEMENTATION.md` (section 2 holds the steps) and `SW/TESTING.md` (section 2 fixtures, section 3 requirement map, section 4 constraint tests). Section and row names in a task refer to those files. Test names written `file::function` live under `SW/tests/`. `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`, `RR` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`, `JJ` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh`, `FND` is `src/superclaude/cli/review/findings.py`, `MRG` is `src/superclaude/cli/review/merge_cmd.py`, `LED` is `src/superclaude/cli/review/ledger.py`.
- Shell variables for every command, run from the repository root: `REPO="$(git rev-parse --show-toplevel)"`, `SW="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet"`, `T="uv run --frozen --project $REPO pytest -p no:cacheprovider"`, `PYRUN="uv run --frozen --project $REPO python"`, and `export PYTHONDONTWRITEBYTECODE=1`. Python only through `uv run`; never `python -m`, `pip install` or bare `python script.py`.
- Git-write check. `gitcheck() { grep -rnE '\bgit\b[^|;&]*\b(add|commit|tag|push)\b' "$1" | grep -vE 'git -C "\$\{?SB[A-Za-z_]*\}?' | grep -vE ':[0-9]+:[[:space:]]*(#|echo|printf)'; }` prints nothing for a directory when no script in it runs `git add`, `commit`, `tag` or `push` except as `git -C "$SB..."` (a sandbox directory variable), in printed text or in a comment. A script that must read a tag uses `git rev-parse`, `git log` or `git for-each-ref`, never `git tag`. Tasks 8, 27 and 33 run it; Task 27 also shows it prints the probe line for a temporary file that holds `git add -A`, so the check is not vacuous.
- Write scope (DESIGN K1). Every file the build creates lives under `SW`. Scratch goes only to pytest `tmp_path` or `/tmp`; the sandbox root is `/tmp/evalsb-sweep`. `src/`, `tests/`, `.claude/` and every existing folder under `.dev/tasks/` are not touched. Evidence a task produces is written under `SW/results/`, not into this plan's package.
- Git scope. The build stages, commits and pushes nothing, and creates no tag (DESIGN K5). Staging of this plan's package stays with the session that runs `/sc:implement`. The sandbox builder's own `git init`, `git add` and snapshot commit run inside a throwaway sandbox under `/tmp` and are not repository writes; they are spelled `git -C "$SB..."`, which is how the git-write check (`gitcheck`, above) tells them from a write to the real repository.
- No model. No reviewer, judge or spike session is started. Every test that needs `claude` uses the fake `SW/tests/fakes/claude` (TESTING F-FAKE). Scripts that start models in real use (`bin/run-spike.sh`, `bin/run-schedule.sh`, `bin/judge-batch.sh`) are built and tested only against the fake.
- Never open any `ground-truth*.json` or score file. Tests marked `freeze` (the real-ground-truth lint, the recall tests) are written but not run by the build; the build runs `-m "not slow and not freeze"` plus `-m slow` where a task says so.
- Read-only imports. `FND`, `MRG` and `LED` are imported or called, never edited. `FND._check_finding` and `FND._blocks_after` are private; they are reached only through `SW/scaffold/fnd.py` (DESIGN section 2.3).
- Folder names. No folder is named `lib/` (`.gitignore` line 13 ignores it; DESIGN K7). Code folders are `scaffold/`, `sweep/` and `analysis/`.
- Decisions DD-1 to DD-15 of DESIGN section 1.3 hold as written; a conflict between this plan and DESIGN.md is settled by DESIGN.md. Step 0 is done (`SW/results/step0.md`); its sub-steps 0.4, 0.5 and 0.6 were not run, so the task that needs each one runs or reads it first (0.4 in Task 24, 0.5 in Task 26, 0.6 in Tasks 6 and 28). Step 0.3 measured a scope taken from IMPLEMENTATION.md, not the DD-5 scope; Task 23 measures the DD-5 scope.
- Out of scope: steps 14 to 16, Redesign 2, the optional verifier of `MR` 3.0.9, any change under `src/`, and any file under `fixtures/recall/` or `holdout-gt/`.
- Line counts in the design are planning values (unmeasured).
Start sha: 866bdcf71c20ee8fcf7ce7a16aaea4c626655976
Diff against the start snapshot: The unified diff (task start tree 866bdcf71c20ee8fcf7ce7a16aaea4c626655976 to reviewed tree 9feac2d71b9831a2aa9686fc45f6c994dcf41bbc) is saved at /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T27/diff-1-1.patch; read it, and read the real current files it names under /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Ignore the ledger file `progress.md` and `results/implement/retries/*/q0-head` in it (orchestrator bookkeeping, not task output), and ignore every path under .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/ and under .dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/ and `results/implement/retries/*/diff-*.patch`, `prompt-*.md` (files that an unrelated concurrent session wrote into the working tree; they are not this task's output and are outside its scope). Evidence logs the task produced are under .dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/logs/ (git ignores *.log, so they are not in the diff; read them from disk). Changed files (status path):
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/reports/make_rl_reports.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/transcripts/make_transcripts.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/cli.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/ledger_api.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/rowcheck.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/scaffold/ledgerv1.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/scaffold/telemetry.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_ground_truth_not_read.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_rowcheck.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_telemetry.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/common.sh
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/run-panel.sh
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/run-reviewer.sh
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T27/q0-head
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/sweep/cli.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/sweep/prepass.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/fakes/claude
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/panel_support.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_blindness.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_kill_fallback.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_paths.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prepass.py
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prepass_inputs.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_run_panel_fake.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_sandbox_clean.py
M	.dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/progress.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T7/notes.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T7/probe-1-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T7/prompt-1-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T7/prompt-2-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T7/review-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T8/notes.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T8/prompt-1-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T8/q0-head
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T9/q0-head
M	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/progress.md

Codegraph context: index_state: fresh; checked_at: 2026-11-14T20:52:06Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files this task changed are new files that the graph does not index (shell, JSON, new Python); no dependents outside the diff were found, Grep/Read floor used.
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
