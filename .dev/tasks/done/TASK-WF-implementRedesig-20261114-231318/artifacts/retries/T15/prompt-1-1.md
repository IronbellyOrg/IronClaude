f76bd67f8f5e0113575b2bf856dad506a59ee6d2
Review one task for spec compliance.

Task brief: ## Task 15: Write the analysis script, the synthetic ground truth and the run-folder fixtures

Depends on: Task 14

Follow `RL/IMPLEMENTATION.md` step 6 (analysis part) and `RL/DESIGN.md` sections 9.3, 12.2 to 12.5 and REQ-17, REQ-29, REQ-31, REQ-39 to REQ-45. Create `RL/fixtures/gt/synthetic-gt.json` (F-GT, invented items for the fixture plan) and `RL/fixtures/runs/make_runs.py` (F-RUNS-RL: synthetic run folders for arms Z0-raw, Z0, K, RL, 2 documents, 5 replicates, known found sets, timings, flags, ledgers and scores, and `expected.json` written by hand-written arithmetic, not by calling `analyze.py`). Create `RL/analysis/analyze.py` with subcommands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`, `ablate-report`: every metric of `RL/DESIGN.md` 12.5 defined only in this file (`found_fraction` and the other metric names), Wilson intervals, a bootstrap that resamples documents then runs, gates D1 to D7 (D1 on per-document medians, same block only, mean and median both reported; D6 blocking), the three labelled shares `Z0 - Z0raw`, `K - Z0`, `RL - Z0` never summed, per-stage rows `stages.jsonl` (extraction null, selection, act, merge survival, judge credit, class, reviewer id), kills and retries per arm with re-asks apart, non-probe findings per run excluding `probe` lines and `src: ledger` lines, the REQ-45 claim sentence, and `analysis/g0.py` is written in Task 16. The analysis reads real ground truth only when a person runs it on real runs after the freeze; no test or build step does.

Write `RL/tests/test_analyze.py`, `RL/tests/test_report.py` (the REQ-31 `test_report_shows_planned_and_measured`, REQ-40 `test_three_shares_separate` and `test_no_summed_headline`, REQ-45 `test_claim_template_text`), `RL/tests/test_stages.py` (REQ-41), `RL/tests/test_prereg.py::test_act_bands_for_all_classes`, and the analysis-side tests of REQ-29, REQ-30, REQ-39, REQ-42 and REQ-43 listed in `RL/TESTING.md` sections 3.4 and 3.7.

Acceptance criteria (ids added by the orchestrator, in source order):
T15.AC1: `$T $RL/tests/test_analyze.py $RL/tests/test_report.py $RL/tests/test_stages.py $RL/tests/test_prereg.py -q` exits 0.
T15.AC2: Every metric on the F-RUNS-RL fixture equals `expected.json`, and an AST search of `RL` finds `found_fraction` defined only in `analysis/analyze.py`.
T15.AC3: A fixture where D2 and D3 pass and D6 fails yields "do not adopt"; the report has no line that adds two share names.
T15.AC4: `analyze.py compliance` on the fixture reports `ledger_missing`, `recipe_missing`, quote validity, format errors and `none_found` per class equal to the hand-computed values (REQ-17 check itself).

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


Start sha: f76bd67f8f5e0113575b2bf856dad506a59ee6d2
Diff against the start snapshot: (the diff is 3979 lines; it is saved as a file: read /tmp/rl-impl/T15/diff.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

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
