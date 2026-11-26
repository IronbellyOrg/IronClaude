68f8010c4a33e6778aef6a44a35dc9a231bac82d
Review one task for spec compliance.

Task brief: ## Task 20: Write RL/IMPLEMENTATION-REPORT.md

Depends on: Task 19

Follow `RL/IMPLEMENTATION.md` step 9 and `RL/TESTING.md` section 6 item 8 and section 5.4 and 5.5. Write `RL/IMPLEMENTATION-REPORT.md` from the files on disk (`RL/config/shared-manifest.json`, `RL/results/step0.md`, `RL/results/tests-final.log`, the file tree of `RL`) with sections, filled section by section:

- What was built, per phase of this plan, with file lists (recipes, lens table and render, row check, re-ask, launcher and arms, judge copy, analysis, schedule, spike, freeze and check scripts) and which parts RUN, which are STUBBED and which are NOT BUILT.
- Which Tier B files were copied and which were built locally (from `shared-manifest.json`, with the sibling's state at copy time).
- Test counts per kind (U, I, C, F) and the summary lines of `tests-final.log`, including the freeze tests collected and not run.
- The exact commands to run one panel of ember (`t2b-1`, `muse-ember-1.0`) plus two luna reviewers (`t4-1` and `t3-1`, `gpt-6-luna`) on each of the three study packages `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649` and `TASK-WF-design-20261108-041415`, for the Z0 control arm and for the RL arm, taken from `RL/TESTING.md` 5.4 and 5.5: the environment lines (`REPO`, `RL`, `SW_SB_ROOT=/tmp/evalsb-recipe`, `NOFALLBACK=1`), `bash $RL/bin/build-sandbox.sh <doc>`, the `--dry-run` look, then `bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc <doc> --replicate 1 --block 1 --seed 20261115 --run-id derive-Z0-<doc>` and the same with `--arm RL --run-id derive-RL-<doc>`, run one panel at a time and in the same block, the `jq` lines to read the result, and the scoring command `bash $RL/bin/judge-batch.sh --runs <z0 run> <rl run>` flagged as needing the owner's go-ahead because it starts the blind Opus judge. State that these commands were not run against any model by this build.
- Every requirement not met or only partly met, with the reason: REQ-08 (second-author record open), REQ-28 manual audit, REQ-17, REQ-32 and the spike (need models), REQ-31 and REQ-33 and REQ-36 and REQ-41 bands and REQ-44 and REQ-45 manual records, REQ-35 model-stage ablation (96 runs, owner decision, DR-13), the `freeze` tests not run, REQ-18 to REQ-24 (Redesign 1 only, not built), every copied test that failed with its cause, every Tier B file built locally and not yet reconciled with the sibling (`copy-shared.sh --diff`), and the open owner decisions of `RL/DESIGN.md` 13.1 (items 1 to 10).
- A statement that no model, judge or network call was made, no ground-truth file was opened, and that Recipe Ledger working is not shown by this build (the experiment decides it).

After the file exists, check each claim in it against disk (counts against `tests-final.log`, file lists against `ls`, commands against `RL/TESTING.md` 5.4 and 5.5).


Acceptance criteria (ids added by the orchestrator, in source order):
T20.AC1: `RL/IMPLEMENTATION-REPORT.md` exists and contains the six sections above, with the six exact commands (3 packages x 2 arms) written out in full and the `NOFALLBACK=1` and `SW_SB_ROOT` settings.
T20.AC2: The test counts in the report equal the numbers in `RL/results/tests-final.log`.
T20.AC3: Every requirement of `RL/TESTING.md` section 3 appears in the report either as met (with the test name that shows it) or as not met with a reason.
T20.AC4: The report does not call any piece "done" or "working" that is stubbed, not built or only shown by a fake claude.

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


Start sha: 68f8010c4a33e6778aef6a44a35dc9a231bac82d
Diff against the start snapshot: (the diff is 2727 lines; it is saved as a file: read /tmp/rl-impl/T20/diff.patch with the Read tool, in parts. It holds the new file IMPLEMENTATION-REPORT.md, the new run folder runs/rehearsal-rl-clean/ and the deletion of the stray config/freeze.json. One touched file is not in it because git ignores *.log: .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/tests-final.log (a Task 19 file that was edited in this task: an addendum under section 7 and a re-run line under section 4; read it in full from disk). The other files exist on disk under the repo; read them as needed. Saved raw outputs of the Task 19 commands: /tmp/rl-t19/fast.out, /tmp/rl-t19/all.out, /tmp/rl-t19/fast-nofallback-unset.out and /tmp/rl-t19/kinds/ (scratch, read only); the report claim check script and its inputs are in /tmp/rl-impl/T20/ (scratch, read only).)

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
