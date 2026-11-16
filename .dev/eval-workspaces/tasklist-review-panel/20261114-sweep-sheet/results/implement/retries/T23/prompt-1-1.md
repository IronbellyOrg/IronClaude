7fc95f1e58124c1390cd12ecf97022bc268602af
Review one task for spec compliance.

Task brief: ## Task 23: Create the pre-pass timing script, kill fallback test and the time checkpoint

Depends on: Task 22

Create `bin/time-prepass.sh` (runs `sweep prepass` on a given snapshot and prints and records the seconds) and `tests/test_prepass_timing.py::test_largest_tree_under_kill_limit` (marker `slow`, REQ-24). The kill-and-fallback tests of REQ-18 need the launcher, so `tests/test_kill_fallback.py` is created in Tasks 26 and 27, not here (a re-split of IMPLEMENTATION step 9). Run the checkpoint of IMPLEMENTATION step 9: `bin/time-prepass.sh` on the repository root and on two smaller snapshots, with the DD-5 scope, and write the seconds into `config/values.json` as `prepass_s` and into `SW/results/prepass-timing.md`.

Acceptance criteria:
- T23.AC1: `$T $SW/tests -q -m slow` exits 0 and `bash $SW/bin/time-prepass.sh --help` exits 0.
- T23.AC2: `SW/results/prepass-timing.md` holds three measured numbers for S1 and the scope string used; `config/values.json` holds `prepass_s`.
- T23.AC3: If S1 on the repository root is over 10 s, this task is reported blocked with the number, DD-5 and DD-10 are named as the items to revisit (IMPLEMENTATION step 9 checkpoint), and later tasks are not started.
- T23.AC4: Dependents: the `prepass_s` and kill limit in `scaffold/clock.py` (Task 26) and the fallback path of `bin/run-panel.sh` (Task 27).

(AC ids: T23.AC1 to T23.AC4, in the order of the bullets above.)
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
Start sha: 7fc95f1e58124c1390cd12ecf97022bc268602af
Diff against the start snapshot: The unified diff (task start tree 7fc95f1e58124c1390cd12ecf97022bc268602af to reviewed tree 0c78f0486a19336873e25990a698cc93e520ea7d) is saved at /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T23/diff-1-1.patch; read it, and read the real current files it names under /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Ignore the ledger file `progress.md` and `results/implement/retries/*/q0-head` in it (orchestrator bookkeeping, not task output), and ignore every path under .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/ and under .dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/ and `results/implement/retries/*/diff-*.patch`, `prompt-*.md` (files that an unrelated concurrent session wrote into the working tree; they are not this task's output and are outside its scope). Evidence logs the task produced are under .dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/logs/ (git ignores *.log, so they are not in the diff; read them from disk). Changed files (status path):
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/__init__.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/copy-shared.sh
M	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/rl-env.sh
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/sibling/make_sibling.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/__init__.py
A	.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/time-prepass.sh
M	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/config/values.json
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/implement/retries/T23/q0-head
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/prepass-timing.md
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/prepass-timing.tsv
A	.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prepass_timing.py
M	.dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/progress.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T2/prompt-1-1.md
A	.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/artifacts/retries/T3/q0-head
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
