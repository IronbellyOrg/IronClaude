7d543ee1a424e2fe77cf4bfa5e271152369edbdf
Review one task for spec compliance.

Task brief: ## Task 1: Create the folder layout, lint config, study config and path and model guards

Create under `SW`: `ruff.toml` (one line `extend = "../../../../pyproject.toml"`, four levels from `SW` to the repository root, same idea as `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml`), empty `scaffold/__init__.py`, `sweep/__init__.py`, `analysis/__init__.py`, `config/packages.json`, `config/panels.json` (three panels with caps 8/8/8, 6/9/9 and 6/9/9 as in DESIGN 7.1), `config/values.json` (planning values for `b` per panel and document, `c` per model, `kill_s`, `hang_s` inputs, `K` = 8, `K_single` = 12, `cap` = 12; DESIGN 12.7), and `bin/common.sh` with `sw_assert_writable`, `sw_assert_model`, `sw_assert_nofallback`, the path variables and `sw_py` (`uv run --frozen --project $REPO python`). Model allowlist per DESIGN K2: `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`; `claude-opus-5-5` only for `bin/judge-one.sh`. Create `tests/test_paths.py`, `tests/test_model_allowlist.py` and `tests/test_layout.py` (TESTING section 4 rows K1, K2, K7). The override guard (`sw_assert_override` in `bin/common.sh`, reused by `tests/conftest.py`) treats each override variable by its kind: the path variables `SW_SB_ROOT` and `SW_SRC_REPO` are refused unless they point under `/tmp/`; `SW_KILL_S` is accepted only as a number from 0.1 to 15 (so `1` passes, `9999` and text are refused); `SW_PREPASS_CMD` is accepted only when its first word is `sleep` or `false` (the stubs of the kill test), anything else is refused.

Acceptance criteria:
- T1.AC1: `$T $SW/tests/test_paths.py $SW/tests/test_model_allowlist.py $SW/tests/test_layout.py -q` exits 0.
- T1.AC2: `test_paths.py::test_refuses_output_outside_sw` shows a path under `REPO/src` or `REPO/tests` is refused with `E_NOT_WRITABLE`, and `::test_override_must_be_under_tmp` shows `SW_SB_ROOT` set to a path outside `/tmp/` is refused; `::test_kill_s_is_numeric_only` shows `SW_KILL_S=1` is accepted and `9999` and `abc` are refused; `::test_prepass_cmd_stub_only` shows `SW_PREPASS_CMD="sleep 5"` is accepted and `rm -rf x` is refused.
- T1.AC3: `test_model_allowlist.py::test_reviewer_models`, `::test_opus_only_in_judge` and `::test_fable_and_tier0_refused` pass: `sw_assert_model` accepts exactly the four reviewer ids and refuses Opus, Fable, Qwen and glm.
- T1.AC4: `test_layout.py::test_no_ignored_folder_names` passes: `git check-ignore` flags no folder under `SW` that holds code.
- T1.AC5: `$PYRUN -c "import json,sys; [json.load(open(f)) for f in sys.argv[1:]]" $SW/config/packages.json $SW/config/panels.json $SW/config/values.json` exits 0, and the caps in `panels.json` sum to 24 for each panel; `test_layout.py::test_values_selection_constants` shows `values.json` holds `K` = 8, `K_single` = 12 and `cap` = 12.
- T1.AC6: `ruff check` and `ruff format --check` on `SW` exit 0. Later tasks depend on `common.sh` (Tasks 8, 23, 27, 28, 32, 33) and on `config/panels.json` (Tasks 20, 26).

(AC ids: T1.AC1 to T1.AC6, in the order of the bullets above.)
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
Start sha: 7d543ee1a424e2fe77cf4bfa5e271152369edbdf
Diff against the start snapshot: The unified diff (task start tree 7d543ee1a424e2fe77cf4bfa5e271152369edbdf to reviewed tree 6a721ece1d3e7f25eed9baf83e3a4c006746e395) is saved at /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T1/diff-1-1.patch; read it, and read the real current files it names under /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Ignore the ledger file `progress.md` and `results/implement/retries/*/q0-head` in it (orchestrator bookkeeping, not task output). Evidence logs the task produced are under .dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/logs/ (git ignores *.log, so they are not in the diff; read them from disk). Changed files (status path):
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/analysis/__init__.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/common.sh
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/config/packages.json
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/config/panels.json
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/config/values.json
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T1/q0-head
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/ruff.toml
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/scaffold/__init__.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/sweep/__init__.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/helpers.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_layout.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_model_allowlist.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_paths.py
M	.dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/progress.md

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
