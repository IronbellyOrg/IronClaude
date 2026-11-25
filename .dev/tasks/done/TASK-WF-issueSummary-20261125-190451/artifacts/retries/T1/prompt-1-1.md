94d675266ef2574ec1488ee2221bf037eceac4ed
Review one task for spec compliance.

Task brief: ## Task 1: Rewrite the create decision rule in the create reference

Edit `src/superclaude/skills/sc-issue-protocol/refs/create.md` (source requirement: additions never ask; one combined question only for a supported contradiction; retained additions disclosed). Change four places and nothing else:

- Wave 4 text at line 57 (the sentence that says the worker lists new material and any contradiction in `draft-notes.md`): state that new material is kept without any question, and that a contradiction is one of exactly four categories: reversed choice (the draft reverses a choice the user stated), dropped requirement (the draft omits a requirement the user stated), changed flag (the drafted issue would not honor `--mode`, `--type` or `--depth` as given) and user-stated fact contradicted by verified code (the worker read the code and the user's stated fact is false). Say that each contradiction line carries the category, the user's own words and the conflicting evidence, that a line without all three is recorded as new material, and that an addition which is the only evidence of a contradiction is listed under Contradictions.
- Line 69 (the "Assumption:" paragraph): keep "one line per assumption, starting with Assumption:" under "New material", and replace "so the contradiction prompt rule below applies to it" with a statement that assumptions are kept and never cause a question. Leave line 63 (the `PLAN_SECTIONS_RULE` sentence) byte-identical.
- The "Contradiction prompt rule (default D14)" section at lines 82-84: keep the heading text. Replace the body with the decision: no contradiction items (empty list, or only `None` under both headings) means zero questions and Wave 5 posts; one or more supported contradiction items means exactly one `AskUserQuestion`, naming every item, asked once per run, whose choices are "keep my wording" (change the draft to honor the user's words), "keep the draft" (accept the draft's change) and "edit"; the answer is applied to `<D>/issue-body.md` before Wave 5 and changes only the contradicted items; every New material item stays in the body and in `draft-notes.md` whatever the answer; the sentence "The full body is never shown for approval (B1)" stays in this section; worker disagreement with a supplied flag is not a contradiction when the issue is filed with the user's flag (point to the Wave 2 sentence "The issue is filed with the user's flags when the user gave them" at line 38 and to Wave 5 step 7 at line 96).
- Wave 5 step 8 at line 97 (the print step): add that the final output also lists every retained addition, one line each, in the form `kept without approval: <item>`, and states whether a contradiction question was asked and how it was answered. Keep every existing clause of that step, including "Do not stage or commit `.dev/issues/` (default D24)".

Acceptance criteria:
- [T1.AC1] `grep -n "lists new material" src/superclaude/skills/sc-issue-protocol/refs/create.md` prints nothing, and `grep -n "keep all" src/superclaude/skills/sc-issue-protocol/refs/create.md` prints nothing.
- [T1.AC2] The file names all four categories, the words "exactly one" question, the `None` rule, the incomplete-line-becomes-new-material rule, the flag-disagreement carve-out, the addition-as-evidence rule and the phrase `kept without approval:` (one `grep -n` for each prints at least one line).
- [T1.AC3] The Contradiction prompt rule section still contains the words "never shown for approval".
- [T1.AC4] `PLAN_SECTIONS_RULE` still appears exactly once in the file (`uv run pytest tests/skills/test_issue_protocol.py -k "create_ref_defines_priority_rule_set_and_required_sections" -v` passes).
- [T1.AC5] `git diff -U0 src/superclaude/skills/sc-issue-protocol/refs/create.md` shows no change on the lines holding the GitHub-write rule paragraph, the lookup paragraph or Wave 5 step 6 (`uv run pytest tests/skills/test_worker_contract.py -k "classification" -v` passes for the create.md entries).
- [T1.AC6] Dependents that must keep working or be updated: SKILL.md create mode steps 5 and 6 (Task 4), the three worker files (Task 3), `docs/designs/sc-issue-command.md` (Task 6).
Global constraints: ## Constraints

- Base branch is `integration` (the issue text says `master`; that is stale). Edit only canonical sources under `src/superclaude/`, `docs/` and `tests/`. The generated project mirrors are refreshed only by `make sync-dev`, never edited by hand.
- Keep `AskUserQuestion` in the `allowed-tools` line of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (pinned by `ALLOWED_TOOLS` in `tests/skills/test_issue_protocol.py:40`).
- Keep the full issue body never shown for approval (default B1), the post-create flag pushback comment (create Wave 5, `templates/create-review-comment.md`), the three required plan sections and their one shared rule sentence (`PLAN_SECTIONS_RULE`, `tests/skills/test_issue_worker_agents.py:34-39`), claim assignment, ClickUp, Orca, watcher and launch safeguards, the stage-claim recommendation skip from pull request 833, and the launched `worktree` agent's plan-approval boundary. None of these text blocks may change in meaning. Task 9 and Task 10 each carry a check that the launch-level safeguards stay untouched.
- Lines of `src/superclaude/skills/sc-issue-protocol/refs/create.md` that `tests/skills/test_worker_contract.py` pins verbatim (the GitHub-write rule paragraph near line 9, the lookup paragraph near line 20 and step 6 of Wave 5 near line 95) must stay byte-identical. SKILL.md step 6 of create mode (line 103) is also pinned there; Task 4 updates that pinned copy together with the line.
- Do not add a new return-contract field, flag, script, agent or dependency to the product. The classification is instruction text plus tests, as the current rule is. The kit of Task 9 is evidence tooling under this package's `./artifacts/`, not product code.
- A contradiction counts only with all three parts: its category, the user's own words (a quote from `description.md` or a flag passed on the command line), and the conflicting evidence (draft text, or a verified `path:line` of code the worker read). A line missing any part is New material. `None` is the empty marker, never an item, and a notes file with `- None` under both headings is the same state as empty notes.
- The changed-flag category means the drafted issue itself would not honor a flag the user passed (for example it would be filed with another mode or type). A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; it stays a pushback comment.
- When an addition is also the only evidence for a contradiction, it is listed under Contradictions, and "keep my wording" removes only that content; every other New material item stays.
- The session that carries out this plan is a launched session whose guard refuses the installer for the whole tool, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub CLI together with `issue` or `api`. No task here runs a create flow, starts a child session or runs `superclaude install`. Task 9 therefore prepares a kit and leaves the controlled runs to a person, and the final report calls the plan partial until that run fills the matrix.
Start sha: 94d675266ef2574ec1488ee2221bf037eceac4ed
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/refs/create.md b/src/superclaude/skills/sc-issue-protocol/refs/create.md
index 8ae944c72..f3105f60b 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/create.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/create.md
@@ -54,7 +54,7 @@ Mode selects feature or bug; depth selects simple or complex:
 | standard | `issue-worker-t2` | `/sc:analyze` (no `--depth`) |
 | deep | `issue-worker-t1` | `/sc:analyze --depth deep` |
 
-At deep depth the `issue-worker-t1` spawn falls back to `issue-worker-t2` as described in Wave 2. The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts), except in the three required plan sections defined in the next subsection. It lists, in `<D>/draft-notes.md` (from `templates/draft-notes.md`), any new material it added beyond the description and any contradiction between the description and the code.
+At deep depth the `issue-worker-t1` spawn falls back to `issue-worker-t2` as described in Wave 2. The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts), except in the three required plan sections defined in the next subsection. It lists, in `<D>/draft-notes.md` (from `templates/draft-notes.md`), under New material every addition beyond the description (assumptions included), which is kept without any question, and under Contradictions only a supported contradiction of the user's own words. A contradiction is one of exactly four categories: reversed choice (the draft reverses a choice the user stated), dropped requirement (the draft omits a requirement the user stated), changed flag (the drafted issue would not honor `--mode`, `--type` or `--depth` as given) and user-stated fact contradicted by verified code (the worker read the code and the user's stated fact is false). Each contradiction line carries its category, the user's own words in quotes (or the flag as passed) and the conflicting evidence (draft text, or a `path:line` the worker read); a line missing any of the three is recorded as New material instead. An addition that is the only evidence of a contradiction is listed under Contradictions.
 
 ### Required plan sections (Priority, Fix approach, Test plan)
 
@@ -66,7 +66,7 @@ At every depth (quick, standard and deep) the worker fills `## Priority`, `## Fi
 - **Fix approach**: the ordered steps to do the work; for each step the files or components it touches (taken from the `/sc:analyze` pass); the SC commands or skills to run in order (for example `/sc:workflow`, then `/sc:implement`, then `/sc:pr-submit --monitor 3`); and the repo and the base branch.
 - **Test plan**: the tests to add or change, the regression gate (the full suite, lint and sync checks), and how a reviewer verifies the result.
 
-An assumption the worker makes where the pass leaves a gap goes under "New material" in `draft-notes.md`, one line per assumption, starting with "Assumption:", so the contradiction prompt rule below applies to it.
+An assumption the worker makes where the pass leaves a gap goes under "New material" in `draft-notes.md`, one line per assumption, starting with "Assumption:". Assumptions are kept and never cause a question.
 
 The Priority rule set is defined once, here; the templates and the workers point at it.
 
@@ -81,7 +81,7 @@ Choose the highest level whose trigger the issue meets.
 
 ### Contradiction prompt rule (default D14)
 
-If `draft-notes.md` lists new material or a contradiction, ask the user one question (AskUserQuestion) naming each item, with the choices "keep all", "drop the new material" and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5. If it lists nothing, post the issue without any prompt. The full body is never shown for approval (B1).
+Ask only when `draft-notes.md` lists a supported contradiction of the user's own description, instruction or flag: reversed choice, dropped requirement, changed flag, or a user-stated fact contradicted by verified code (each with the user's own words and the conflicting evidence). Empty notes, or notes with only `None` under both headings, ask zero questions and Wave 5 posts. One or more supported contradiction items ask exactly one question (AskUserQuestion), once per run, naming every item, with the choices "keep my wording" (change the draft to honor the user's words), "keep the draft" (accept the draft's change) and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5; it changes only the contradicted items. Every New material item, assumptions included, stays in the body and in `draft-notes.md` whatever the answer, and is listed in the final output. A worker's disagreement with a supplied flag is not a contradiction when the issue is filed with the user's flag (Wave 2, line "The issue is filed with the user's flags when the user gave them"); it stays the pushback comment of Wave 5 step 7. The full body is never shown for approval (B1).
 
 ## Wave 5: post (orchestrator, directly)
 
@@ -94,6 +94,6 @@ Load `refs/labels.md`.
 5. Type read-back: `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. When `--type` was passed and the result is empty or different, remember `not set: issue type <name>: not applied after create`.
 6. Complexity field: when `### Complexity field` in `scout.md` lists the field and an option equal to the wanted value (`quick` = Simple, `standard` = Medium, `deep` = Complex), write `.dev/issues/<N>/complexity-field.json` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` (body and error handling in `refs/labels.md`). A failed POST remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After a success, read the values back with `gh api repos/<R>/issues/<N>/issue-field-values` and remember `not set: field Complexity <value>: not applied after create` when the value is absent. A missing field remembers `not set: field Complexity <value>: field not found in org` (or `lookup failed`).
 7. Standard or deep with all flags given and a disagreement in Wave 2: write `.dev/issues/<N>/create-review.md` from `templates/create-review-comment.md` (it ends with `<!-- sc:issue:create-review -->`) and post it with `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md`. Failure -> STOP `E-POST-FAILED`.
-8. Print the issue URL, the directory, every `not applied: label missing in repo` line and every `not set` line (formats in `refs/labels.md`). No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).
+8. Print the issue URL, the directory, every `not applied: label missing in repo` line and every `not set` line (formats in `refs/labels.md`), one `kept without approval: <item>` line for every retained addition, and whether a contradiction question was asked and how it was answered. No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).
 
 A failed type or field never stops the run once the issue exists. Only `gh issue create --repo <R>` (`E-CREATE-FAILED`) and the pushback comment (`E-POST-FAILED`) keep their STOP codes.


Codegraph context:
index_state=stale checked_at=2026-11-25T19:23:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor; dependents of the changed text that are not in this task's touched set are edited by later tasks of the plan.

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
