f9c01be6f4c25a3abaf89e27831da5618811e023
Review one task for spec compliance.

Task brief: ## Task 8: Implement linking, demotion and promotion of ledger rows

Depends on: Task 7

Follow `RL/IMPLEMENTATION.md` sub-steps 4.2 and 4.3 and `RL/DESIGN.md` sections 7.2 checks 7 to 11, 1.4 (`SWD` DD-3, DD-11, DD-12) and 7.4. Write the link, demote and promote logic in `RL/scaffold/ledgerv1.py` (if `built-local`; otherwise in the RL adapter of Task 9 without editing the copy): link each findings line to a row by `probe` or by the row's flattened `quote_plan` lying inside the line's flattened `anchor`; demote a linked blocking finding to non-blocking when its row is an unsupported PROBLEM (`row_unsupported`), an UNSURE row (`row_unsure`), has no CB-3 sentence (`no_cb3`) or failed to parse (`row_missing`), keeping its severity; leave unlinked findings untouched (switch `CHECK_SCOPE=linked|all`, `all` unused); count `format_induced_demotions`; promote a PROBLEM row with no linked line using the row's own `problem` as `claim` and `quote_plan` as `anchor`, validated with `FND._check_finding`, inserted inside the single findings block, severity MINOR, `blocking` false, `src` `ledger`, `class` from the row id prefix, and only when the row is not `unknown_item`, not `over_budget`, has a present `quote_plan_ok` `quote_plan`, and its ledger was not repaired by a re-ask (check 10). Failures are logged in `promotion_failures` and skipped.

Write the REQ-15 and REQ-16 tests in `RL/tests/test_rowcheck.py`: `test_promotion_copies_problem_and_anchor`, `test_promotion_validates_with_check_finding` (long id, short anchor, duplicate id), `test_promotion_inside_single_block`, `test_promotion_failure_logged_and_skipped`, `test_promotion_requires_quote_plan_ok`, `test_no_promotion_for_over_budget_unknown_or_reask_rows`, `test_class_key_added_from_row_prefix`, `test_unsupported_row_demotes_linked_finding`, `test_unsure_never_blocks`, `test_blocking_needs_cb3_and_two_quotes_or_search`, `test_unlinked_finding_untouched`, `test_quote_other_corpora`, `test_check_scope_all_switch_off_by_default`, `test_format_induced_demotions_counted`.

Acceptance criteria (ids added by the orchestrator, in source order):
T8.AC1: `$T $RL/tests/test_rowcheck.py -q -k "promotion or demotes or unsure or blocking or unlinked or corpora or scope or format_induced"` exits 0.
T8.AC2: A `quote_other` found only in a tool result of the transcript is supported as a search result, one found only in assistant text is not, and an unlinked blocking finding stays blocking (REQ-16, DR-9).
T8.AC3: The raw `reviews/<rid>.md` is never edited by any function; checked output goes to a separate `checked.md`.

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


Start sha: f9c01be6f4c25a3abaf89e27831da5618811e023
Diff against the start snapshot: (the diff is 721 lines; it is saved as a file: read /tmp/rl-impl/T8/diff.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

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
