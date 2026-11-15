8a1b2afbe65d4a8073e4302f59658077d3eb86d8
Review one task for spec compliance.

Task brief: ## Task 19: Run every test and every build check and save the logs

Depends on: Task 18

Follow `RL/IMPLEMENTATION.md` step 8 and `RL/TESTING.md` section 6 items 1 to 7. Create `RL/results/` outputs by running, from `REPO`:

- `$T $RL/tests -q -m "not slow and not freeze"` and save its summary line and the counts of passed, failed, skipped and deselected tests to `RL/results/tests-final.log`.
- `$T $RL/tests -q -m slow` and append its summary line and counts to the same log.
- `$T $RL/tests -q --collect-only -m freeze` to list the tests with marker `freeze` and append the list and their count to the log; do not run them (they read the real ground truth or need a second author's records) and record that they were not run and why.
- `uv run --frozen --project $REPO ruff check $RL` and `uv run --frozen --project $REPO ruff format --check $RL`.
- `$T $REPO/tests/review -q` again (the baseline of Task 1 must still hold).
- `bash $RL/bin/copy-shared.sh --check` and `$PYRUN $RL/rl/cli.py lens --validate`.
- The rehearsal of Task 13 once more, and `git status --porcelain` over `src/`, `tests/`, `.claude/`, `.dev/tasks/` (other than this plan package), `SW` and `EVAL`, which must show no change made by the build.
- Per-kind counts: the number of tests per kind U, I, C (copied), F (freeze, not run), taken from the test files and markers, for the report.

If any command fails, fix the cause in the file that owns it (never a copied file) and rerun that command and the full run until it passes, or, if the cause is a copied test or a missing sibling piece, record it with its reason in `RL/results/tests-final.log` and `RL/results/step0.md` for the report.


Acceptance criteria (ids added by the orchestrator, in source order):
T19.AC1: `RL/results/tests-final.log` holds the three summary lines (not slow and not freeze, slow, freeze collected-only), the ruff results, the `tests/review` result and the `copy-shared.sh --check` result, each with its exit code.
T19.AC2: Every non-freeze test passes, or each remaining failure is a copied test with a recorded cause; no copied file was edited.
T19.AC3: No path under `src/`, `tests/`, `.claude/`, `SW`, `EVAL` or an existing `.dev/tasks/` folder changed (shown by the `git status` output saved in the log).
T19.AC4: No ground-truth file was opened (the build used only `RL/fixtures/gt/` synthetic files).

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


Start sha: 8a1b2afbe65d4a8073e4302f59658077d3eb86d8
Diff against the start snapshot: (the diff is 2428 lines; it is saved as a file: read /tmp/rl-impl/T19/diff.patch with the Read tool, in parts. It holds the edit of results/step0.md and the new run folder runs/rehearsal-rl-final/. One touched file is not in it because git ignores *.log: .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/tests-final.log (a new file; read it in full from disk). The other files exist on disk under the repo; read them as needed. Saved raw outputs of the commands: /tmp/rl-t19/fast.out, /tmp/rl-t19/all.out, /tmp/rl-t19/fast-nofallback-unset.out and /tmp/rl-t19/kinds/ (scratch, read only).)

Codegraph context: index_state: fresh; checked_at: 2026-11-15T03:24:25Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
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
