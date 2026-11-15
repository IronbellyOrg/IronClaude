ae211d07b5f8dd2fedff00dc3d6321d8f477dae6
Review one task for spec compliance.

Task brief: ## Task 6: Write the brief renderer, the lens subcommand and the render, target and ablation tests

Depends on: Task 5

Follow `RL/IMPLEMENTATION.md` step 3 (render part) and `RL/DESIGN.md` sections 2.4, 6.1 to 6.5, 11.3 and DR-2, DR-3, DR-7. Create `RL/rl/render.py`: the RL brief is the copied renderer's Z0 text (`scaffold.briefs.render("Z0", doc, None, source)`, never re-implemented) then the copied ledger rule, then `recipes/rl-block.txt` with `{{LENS_ROW_CAP}}` filled, then the line `## RECIPES ASSIGNED TO YOU`, then the reviewer's recipes printed as `R-C<n>. <text>` one paragraph each in lens order, then (search role only) the search-form line, joined by the copied module's `SEPARATOR`; on `fallback` the Z0 text only. Create `RL/rl/cli.py` with the subcommand `lens` (`--validate`, `--panel`, `--doc`, `--out`) writing `lens/<rid>.json`, `briefs/<rid>.txt`, `briefs/<rid>.sha256` and the `run.json` fields of `RL/DESIGN.md` 2.2 (`no_source`, `c2_not_applicable`, `no_budget`, `fallback`, `recipes_sha256`, `lenses_sha256`, row cap, `b` and `c` used); JSON is written with `sort_keys=True`, `ensure_ascii=False` and a trailing newline.

Write `RL/tests/test_render.py` (REQ-01: CB-1 present with a source and absent without, C2 recipe dropped without a source, `no_source` flags; REQ-05 RL parts: brief starts with the exact Z0 text, fallback brief equals Z0 by sha256, part order, row-cap placeholder equals the `MR` quote at 14 and only the number changes at 6 and 8 (DR-3); REQ-09: no `src/superclaude/` path in any brief of any arm, panel, reviewer, with and without a source; REQ-25: generated briefs match the lens table for each of the three panels, recipe paragraphs equal `recipes.json` byte for byte, at most 4 per brief, parsed by the heading `R-C<n>.`; byte-identical same inputs), `RL/tests/test_targets.py` (REQ-37: spec fixture with its parent as source has all eight recipes, documentation fixture has no C2 and seven others, with `no_source` and `c2_not_applicable`, every lens at least 2 recipes), `RL/tests/test_ablation.py` (REQ-35, DR-13: removing one recipe leaves every other recipe paragraph, Z0 part and lens position byte for byte unchanged) and the render part of `RL/tests/test_ground_truth_not_read.py` (K3, REQ-34: a read hook on `open` shows the lens and brief render never open a trap file named like a ground-truth file in the F-REPO fixture).

Acceptance criteria (ids added by the orchestrator, in source order):
T6.AC1: `$T $RL/tests/test_lens.py $RL/tests/test_render.py $RL/tests/test_targets.py $RL/tests/test_ablation.py $RL/tests/test_ground_truth_not_read.py -q` exits 0.
T6.AC2: `$PYRUN $RL/rl/cli.py lens --validate` prints the three panels and exits 0 (checkpoint of step 3).
T6.AC3: Every rendered RL brief begins with the Z0 brief of the same document and source state, and the three briefs of a panel hold the recipe sets of the lens table.
T6.AC4: A bad lens table makes the `lens` subcommand exit non-zero with `E_LENS_INVALID`, which Task 13 turns into a Z0 fallback.

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


Start sha: ae211d07b5f8dd2fedff00dc3d6321d8f477dae6
Diff against the start snapshot: (the diff is 1088 lines; it is saved as a file: read /tmp/rl-impl/T6/diff.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

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
