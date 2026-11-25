3346c8b112660b2552f5fb5034d590102eb86d38
Review one task for spec compliance.

Task brief: ## Task 2: Rewrite the draft-notes template

Depends on: Task 1

Edit `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` (source requirement: the two lists get different consequences, the four categories, user quotation and evidence, and `None` handling). Keep the two headings `## New material` and `## Contradictions` unchanged, because the workers and `refs/create.md` refer to them by name. Replace the intro line 3 ("The orchestrator asks the user one question only when either list has an item") with the new consequence: items under New material never cause a question and are kept in the body and the final output; one or more supported items under Contradictions cause exactly one question. Under New material keep the comment about source (`path:line` or command) and add that assumptions are listed here as `Assumption: <text>`. Under Contradictions replace the comment with the required line format: category (one of the four names), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a `path:line` the worker read); say that a line missing any of the three parts belongs under New material; say that a worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; and say that an addition which is the only evidence of a contradiction is listed here. Keep "None" as the empty marker under both headings and state it is not an item and that `- None` under both headings is the same state as empty notes.

Acceptance criteria:
- [T2.AC1] `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` still has exactly the headings `## New material` and `## Contradictions`, each still holding a `- None` default line.
- [T2.AC2] The template names the four categories, states "no question" for New material and "one question" for Contradictions in plain words, and contains the flag-disagreement exception (a `grep -n "disagreement"` on the file prints at least one line).
- [T2.AC3] `grep -n "either list" src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` prints nothing.
- [T2.AC4] `uv run pytest tests/skills/test_issue_protocol.py -k "template" -v` passes (heading-order, marker and no-ClickUp checks on the issue-body templates are unaffected).
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
Start sha: 3346c8b112660b2552f5fb5034d590102eb86d38
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md b/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md
index 80ca33689..79e37caab 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md
@@ -1,15 +1,15 @@
 # Draft notes
 
-Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.
+Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.
 
 ## New material
 
-<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->
+<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). List an assumption as `Assumption: <text>`. A contradiction line that lacks its category, the user's own words or its conflicting evidence belongs here instead. -->
 
 - None
 
 ## Contradictions
 
-<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->
+<!-- Only a supported contradiction of the user's own description, instruction or flag, one per line, in this form: category (reversed choice, dropped requirement, changed flag, or user-stated fact contradicted by verified code), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a path:line the worker read). A line missing any of the three parts belongs under New material. A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag. An addition that is the only evidence of a contradiction is listed here. -->
 
 - None


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
