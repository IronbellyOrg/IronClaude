9288a336452a2fd6530c9837fe586bf1a964cb6a
Review one task for spec compliance.

Task brief: ## Task 6: Align the design document and the user guide

Depends on: Task 5

Edit `docs/designs/sc-issue-command.md`: the paragraph at lines 223-225 (the worker "lists, in `<D>/draft-notes.md`, any new material ... and any contradiction", and the next paragraph that says the orchestrator asks one question when notes list new material or a contradiction) and the D14 row at line 460 ("Create asks the user one question only when the drafter found new material or a contradiction"). Rewrite both to the new rule: no question for new material, one combined question only for a supported contradiction in one of the four categories, additions kept and printed. Keep the line-381 file-table row naming "contradiction prompt rule" valid. Edit `docs/user-guide/commands.md` at line 357 ("It posts directly to GitHub, without showing the comment or the issue body for approval first"): add one sentence that `--create` asks one question only when the drafted issue contradicts what you said, and keeps and lists everything else it added.

Acceptance criteria:
- [T6.AC1] `grep -rn "new material or a contradiction" docs/ src/` prints nothing.
- [T6.AC2] Both docs still say posting is never shown for approval, and the D14 row explains why that does not conflict with the single contradiction question.
- [T6.AC3] No other design-document decision row (D1 to D26 other than D14) changes.
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
Start sha: 9288a336452a2fd6530c9837fe586bf1a964cb6a
Diff against the start snapshot: diff --git a/docs/designs/sc-issue-command.md b/docs/designs/sc-issue-command.md
index 0f13e8107..f7c071697 100644
--- a/docs/designs/sc-issue-command.md
+++ b/docs/designs/sc-issue-command.md
@@ -220,9 +220,9 @@ Complexity follows depth, as the issue body pairs them: `quick` = Simple, `stand
 | standard | `issue-worker-t2` | `/sc:analyze` (no `--depth`) |
 | deep | `issue-worker-t1` | `/sc:analyze --depth deep` |
 
-The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts), except in the `Priority`, `Fix approach` and `Test plan` sections: at every depth the worker fills those three from its `/sc:analyze` pass, "Not known yet" is not allowed in them, and where the pass leaves a gap the worker states its assumption in the section and lists it in `<D>/draft-notes.md`. The Priority rule set (Urgent, High, Medium and Low, each with its trigger) is defined once in `refs/create.md`. It lists, in `<D>/draft-notes.md`, any **new material** it added beyond the description and any **contradiction** between the description and the code.
+The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts), except in the `Priority`, `Fix approach` and `Test plan` sections: at every depth the worker fills those three from its `/sc:analyze` pass, "Not known yet" is not allowed in them, and where the pass leaves a gap the worker states its assumption in the section and lists it in `<D>/draft-notes.md`. The Priority rule set (Urgent, High, Medium and Low, each with its trigger) is defined once in `refs/create.md`. It lists, in `<D>/draft-notes.md`, every **addition** beyond the description (assumptions included) under New material, which is kept without any question, and under Contradictions only a supported **contradiction** of the user's own words in one of four categories (reversed choice, dropped requirement, changed flag, user-stated fact contradicted by verified code), each with the user's quoted words and the conflicting evidence.
 
-If `draft-notes.md` lists new material or a contradiction, the orchestrator asks the user one question (AskUserQuestion) naming each item, with choices "keep all", "drop the new material", "edit" (issue body: "result in a prompt to the user to confirm"). If it lists nothing, the issue is posted without any prompt. The full body is never shown for approval (B1; default D14 explains how the two rules fit together).
+If `draft-notes.md` lists one or more supported contradictions, the orchestrator asks the user exactly one question (AskUserQuestion) naming each item, with choices "keep my wording", "keep the draft", "edit" (issue body: "result in a prompt to the user to confirm"). If it lists no contradiction, whether it lists additions or nothing, the issue is posted without any prompt, and every addition is kept in the body and printed in the final output. The full body is never shown for approval (B1; default D14 explains how the two rules fit together).
 
 **Wave 5: post (orchestrator, directly).**
 1. Labels = the mode label only, intersected with the labels that exist in `<R>` (section 11). A missing one is listed in the final output, never created (B7).
@@ -457,7 +457,7 @@ Each is a **design default**: a choice made where the issue and comments are sil
 | D11 | Possible duplicates found on create are listed in the body's related-issues section; they do not stop the run | Not specified; B1 favours posting directly |
 | D12 | One of `--mode` / `--type` given: keep it, choose the other as in the "flag missing" row | Not specified |
 | D13 | Create, deep, all flags given: two variants (user's flags, T1's independent choice) debated with `/sc:adversarial --compare ... --depth quick` | The issue's "parallel agents each invoke `/sc:adversarial --depth quick`" needs at least two variants to compare; this is the smallest form |
-| D14 | Create asks the user one question only when the drafter found new material or a contradiction; otherwise it posts without any prompt; the full body is never previewed | The issue body requires that confirmation; B1 forbids routine previews. The two do not conflict once the prompt is limited to those findings |
+| D14 | Create asks the user one question only when the drafter found a supported contradiction of the user's own description, instruction or flag; added material and assumptions never cause a question and are kept and printed; the full body is never previewed | The issue body requires confirmation of a contradiction; B1 forbids routine previews. The two do not conflict once the prompt is limited to a supported contradiction, because added material that contradicts nothing needs no approval |
 | D15 | `clickup.json` has no template | It is a script's machine output, not a document |
 | D16 | A missing mode label, issue type or Complexity field is skipped and reported; `refs/labels.md` gives the maintainer's one-time creation lines for the two mode labels | B7 forbids creating labels, types and fields at run time |
 | D17 | On create, complexity follows depth (quick = simple, standard = medium, deep = complex) | The issue body pairs them |
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index cfa2ede3f..cc18cb2cf 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -354,7 +354,7 @@ No level merges anything: people review and merge. The agent starts behind the c
 /sc:issue --create @notes/new-command.md --depth deep
 ```
 
-It posts directly to GitHub, without showing the comment or the issue body for approval first. It never creates labels, issue types or issue fields: a mode label that the repository does not have, and an issue type or Complexity field it cannot set, are skipped and listed in the final output. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. The claim itself never runs a step of `.dev/issues/<N>/next-steps.md`: the launched agent does, at the level you chose (with `--pipeline none` there is no worktree and you run them yourself from this checkout). A re-claim reuses the existing worktree and does not launch a second agent, also when you re-claim from inside the worktree; the claim output names the two files that hold the launch (`.dev/issues/<N>/worktree.json` and a file in the worktree's git directory), and removing the `launch` entry from both launches again. Worktree or launch problems are warnings: the issue stays assigned and the comments stay posted.
+It posts directly to GitHub, without showing the comment or the issue body for approval first. The one exception is `--create`: it asks one question only when the drafted issue contradicts what you said (your description, an instruction or a flag you passed), and it keeps and lists everything else it added. It never creates labels, issue types or issue fields: a mode label that the repository does not have, and an issue type or Complexity field it cannot set, are skipped and listed in the final output. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. The claim itself never runs a step of `.dev/issues/<N>/next-steps.md`: the launched agent does, at the level you chose (with `--pipeline none` there is no worktree and you run them yourself from this checkout). A re-claim reuses the existing worktree and does not launch a second agent, also when you re-claim from inside the worktree; the claim output names the two files that hold the launch (`.dev/issues/<N>/worktree.json` and a file in the worktree's git directory), and removing the `launch` entry from both launches again. Worktree or launch problems are warnings: the issue stays assigned and the comments stay posted.
 
 **ClickUp settings (claim only, environment variables):**
 


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
