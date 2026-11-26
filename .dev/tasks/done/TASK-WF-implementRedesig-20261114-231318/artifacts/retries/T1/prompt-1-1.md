425f1d1f9d6b52546b1f56cde8ae0d30df59dd94
Review one task for spec compliance.

Task brief: ## Task 1: Run the four preflight checks and write RL/results/step0.md

Follow `RL/IMPLEMENTATION.md` section 1 and step 0 (sub-steps 0.1 to 0.5). Create `RL/results/` and write `RL/results/step0.md` and `RL/results/import-time.md`. Scratch goes to `/tmp/rl-step0/`.

- Run `$T $REPO/tests/review -q`. The code this design imports (`src/superclaude/cli/review/findings.py`, `merge_cmd.py`, `ledger.py`) must be healthy; if it fails, stop and report it, do not fix `src/`.
- Write `/tmp/rl-step0/merge_keys.py` (about 20 lines, run with `$PYRUN`): build one report whose findings line carries `"class"`, `"probe"` and `"src"`, run `superclaude.cli.review.merge_cmd.command` through click's `CliRunner` with `--ledger`, `--doc` (a fixture plan under `/tmp`), `--round 1`, `--report r1=<report>` and `--out` all under `/tmp/rl-step0/`, and print the exit code and whether the merged text contains the three keys. Read `SW/results/step0.md` first (it holds the sibling's answer) and run the probe anyway.
- Run the sibling-state check of 0.3: `cd $SW && sha256sum -c` over the non-ABSENT rows of `RL/SHARED-MANIFEST-DESIGN-TIME.tsv` (read only), `ls -l` of the twelve Tier B paths of that file, and `ls $SW/results $SW/implement-report`.
- Run the transcript-shape check of 0.4 with `jq` on one `*.attempt1.json` per reviewer model (luna, haiku, sonnet, ember) under `EVAL/<document>/reviews/combos/`: list event types, assistant block types and `tool_use` input keys. Open no ground-truth, score or judge file.
- Time `$PYRUN -c "import superclaude.cli.review.findings"` five times and write the five numbers and their median to `RL/results/import-time.md`.

Acceptance criteria (ids added by the orchestrator, in source order):
T1.AC1: `RL/results/step0.md` holds four answers (tests/review result, merge-keys result, sibling-state result, transcript-shape result), each with the decision taken under the decision rules of `RL/IMPLEMENTATION.md` section 1.
T1.AC2: `RL/results/import-time.md` exists with five timings and the median, so the row-check time budget of `RL/DESIGN.md` 10.1 has a measured number.
T1.AC3: The merge-keys answer states whether the real merge accepts `class`, `probe` and `src` and keeps them out of the merged report (REQ-11). If it rejects them, `step0.md` says the telemetry moves to a side file and names `RL/DESIGN.md` 7.2 check 11 as the part to change.
T1.AC4: `git status --porcelain` shows no change under `src/`, `tests/`, `.claude/`, `SW` or `EVAL` caused by this task.

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


Start sha: 425f1d1f9d6b52546b1f56cde8ae0d30df59dd94
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/import-time.md b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/import-time.md
new file mode 100644
index 000000000..17550af6f
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/import-time.md
@@ -0,0 +1,14 @@
+# Import time of `superclaude.cli.review.findings` (step 0.5, measured 2026-11-14)
+
+Command, five times, wall clock around the whole process: `uv run --frozen --project <repo> python -c "import superclaude.cli.review.findings"` (with `PYTHONDONTWRITEBYTECODE=1`).
+
+| Run | Seconds |
+|---|---|
+| 1 | 0.283 |
+| 2 | 0.295 |
+| 3 | 0.271 |
+| 4 | 0.272 |
+| 5 | 0.279 |
+| **Median** | **0.279** |
+
+The number includes `uv run` start-up and interpreter start. `RL/DESIGN.md` 10.1 uses it for the row-check time budget: the row check itself is timed excluding interpreter start (the Task 9 test), and the per-panel overhead of one interpreter start is about 0.28 s. The sibling measured 0.28 s once; this build agrees.
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/step0.md b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/step0.md
new file mode 100644
index 000000000..3a29e6171
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/step0.md
@@ -0,0 +1,16 @@
+# Step 0 results: the four no-model checks (2026-11-14)
+
+No model was started and no network call was made. Scratch scripts and outputs are in `/tmp/rl-step0/` (not committed). Nothing under `src/`, `tests/`, `.claude/`, `SW` or `EVAL` was changed.
+
+| # | Check | Result | Decision (rule of `IMPLEMENTATION.md` section 1) |
+|---|---|---|---|
+| 1 | `uv run --frozen --project <repo> pytest -p no:cacheprovider tests/review -q` | 126 passed in 0.74 s | Pass. The code this design imports (`findings.py`, `merge_cmd.py`, `ledger.py`) is healthy. Go on. |
+| 2 | Merge-keys probe (`/tmp/rl-step0/merge_keys.py`, click `CliRunner` over `superclaude.cli.review.merge_cmd.command`, one invented report, run once plain and once with `"class":"C1","probe":"C1.1","src":"ledger"` added to the findings line) | Both runs exit 0. The merged report and the ledger JSON contain none of `class`, `probe`, `src` as keys (the only hit of the word "probe" in the merged text is the invented claim sentence). | Accepted and dropped by the real merge (REQ-11). Go on: `RL/DESIGN.md` 7.2 check 11 stays as designed; telemetry is read from the checked report, never from the merged report. The sibling's `SW/results/step0.md` reports the same answer (one real ember report, both exit 0, keys dropped). |
+| 3 | Sibling state (read only): `sha256sum -c` of the 50 non-ABSENT rows of `SHARED-MANIFEST-DESIGN-TIME.tsv` run from inside `SW`; `ls -l` of the 12 Tier B paths; `ls SW/results SW/implement-report` | All 50 rows OK: no Tier A, S, T or fixture file changed since the design-time record. All 12 Tier B paths are still ABSENT (`SW/bin` holds only `build-sandbox.sh` and `common.sh`, `SW/scaffold` only the six Tier A modules). `SW/results` holds `step0.md`, `copy-briefs.py` and an `implement/` folder; `SW/implement-report` holds two empty session files. | Tier A, S, T and the nine fixtures are copied as they are. Every Tier B file is a candidate for a local build (expected result: all 12 `built-local`). The sibling is still being edited live (codegraph listed two pending edits under `SW/sweep` and `SW/tests`), so `copy-shared.sh` must keep the two-reads-60-seconds-apart rule for Tier B. |
+| 4 | Transcript shape: `jq` over one `*.attempt1.json` per model under `EVAL/TASK-WF-designSpec-20261107-075614/reviews/combos/` (luna `g3-sonnet-luna-ember-r1/t4-1`, ember `g3-.../t2b-1`, sonnet `g3-.../t1b-1`, haiku `c1-haiku-luna/t4-1`; model checked in each `*.attempt1.meta.json`). No ground-truth, score or judge file was opened. Full output: `/tmp/rl-step0/transcript-shapes.txt`. | All four files are JSON arrays of events with types `system/init`, `assistant`, `user`, `result/success` (plus `system/thinking_tokens` for ember, sonnet and haiku). Assistant blocks: `thinking`, `tool_use`, `text`. `user` blocks: `tool_result` (a `text` block as well for luna). Ember, sonnet and haiku: `tool_use` names are only `Bash` and `Read`, input keys `command`, `description`, `file_path`, and every `tool_result.content` is a string. Luna differs: `tool_use` names also include `Skill`, `mcp__codegraph__codegraph_node` (4) and `mcp__litellm__augment_code-augment_code_search` (1), with input keys such as `file`, `projectPath`, `query`, `repo_owner`, `repo_name`, `branch`, `skill`; 4 of its 9 `tool_result.content` values are arrays of `{"type":"text"}` blocks, not strings. | Different for luna, so the rule says the reader must accept both shapes before step 4. Decision: the transcript corpus (Task 7) reads a tool result whether `content` is a string or an array of text blocks, and `analysis/ran_check.py` (Task 16) treats a search by a non-`Bash` tool (`mcp__codegraph__*`, `mcp__litellm__*`, `Grep`) as a tool call that can verify a search row, in addition to a `Bash` call. `RL/DESIGN.md` 7.7 is a specification file the build never edits, so this note is the record of the difference. |
+
+## Limits of these results
+
+- Check 2 used one invented report. It shows the three keys are accepted and dropped for that case. It does not show the behaviour for a report with an invalid line.
+- Check 4 used one transcript per model of one study document, so it shows which shapes exist, not how often each occurs. The luna transcript is the only one with MCP tool names; a different luna run may use other tools.
+- Check 3 is a snapshot of 2026-11-14T23:2x UTC; the sibling may change after it.

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
