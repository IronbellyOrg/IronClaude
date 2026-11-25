e040381e39dd33e20236858d081a7ff7b39c1131
Review one task for spec compliance.

Task brief: ## Task 4: Align SKILL.md and its pinned copy in the worker-contract test

Depends on: Task 3

Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md` in three places. Line 76 ("The only user prompt is the create-mode contradiction question"): say the only prompt is one question for a supported contradiction of the user's own description, instruction or flag, never for added material, and keep the words "never shown for approval" in that line. Line 102 (create step 5, "Ask one question only when `draft-notes.md` lists new material or a contradiction"): replace with the new decision (zero questions for additions-only or empty notes, one combined question only for a supported contradiction). Line 103 (create step 6, the post step): add that the printed output lists every retained addition in the exact form `kept without approval: <item>` and the question outcome, keeping every other clause. Leave the `allowed-tools` line 4 unchanged. Because line 103 is pinned verbatim as a key in the `WRITE_VERB_CLASSIFICATION` table of `tests/skills/test_worker_contract.py` (the entry whose key line starts `6. **Wave 5, post.** Load`), change that key string to the new line 103 text and keep its category `never-worker` and reason unchanged.

Acceptance criteria:
- [T4.AC1] `grep -n "lists new material" src/superclaude/skills/sc-issue-protocol/SKILL.md` prints nothing, and line 4 still ends with `AskUserQuestion`.
- [T4.AC2] `grep -n "kept without approval:" src/superclaude/skills/sc-issue-protocol/SKILL.md` prints the new line 103, and `grep -n "never shown for approval" src/superclaude/skills/sc-issue-protocol/SKILL.md` prints the line 76 text.
- [T4.AC3] `uv run pytest tests/skills/test_worker_contract.py -k "classification" -v` passes, including `test_classification_table_has_no_stale_entries` (the updated key matches the live SKILL.md line).
- [T4.AC4] `uv run pytest tests/skills/test_issue_protocol.py -v` passes (frontmatter, size and allowed-tools checks at lines 40 and 137-144, and `test_rule_10_line_is_carried_verbatim` for SKILL.md).
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
Start sha: e040381e39dd33e20236858d081a7ff7b39c1131
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index ab06d8c67..126f312d0 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -73,7 +73,7 @@ Every spawn prompt names each exact path the job must write under `.dev/issues/`
 - Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder. The one exception is the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash; no other `orgs/` path is allowed, and the orchestrator and the T1 and T2 workers keep the old rule).
 - The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` (create mode adds `--type <name>`), `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and `scripts/clickup_claim.py`. Workers never write to either.
 - `git fetch origin` is the only fetch; no other remote is added or fetched.
-- Posts go up directly (B1); the full body or comment is never shown for approval. The only user prompt is the create-mode contradiction question (`refs/create.md`, default D14).
+- Posts go up directly (B1); the full body or comment is never shown for approval. The only user prompt is one question for a supported contradiction of the user's own description, instruction or flag, never for added material (`refs/create.md`, default D14).
 - `.dev/issues/` is never staged or committed by this skill (default D24).
 - `CLICKUP_API_TOKEN` is never printed, echoed or inlined.
 
@@ -99,8 +99,8 @@ Load `refs/create.md` now. `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/`
 2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13): repo labels, repo issue types, the Complexity field of the organization and possible duplicates into `<D>/scout.md`.
 3. **Wave 2, settle the flags** by the depth table of `refs/create.md`; complexity follows depth and the `Issue type` row follows from the mode and the area; the result goes to `<D>/flags.md` from `templates/flags-decision.md`. Deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`.
 4. **Wave 3, pick the template**: mode selects feature or bug; `quick`/`standard` select the simple template, `deep` the complex one.
-5. **Wave 4, draft the body** with the depth's worker into `<D>/issue-body.md` and `<D>/draft-notes.md`. At every depth the worker fills `## Priority`, `## Fix approach` and `## Test plan` from the `/sc:analyze` pass and never writes "Not known yet" there (rules in `refs/create.md`). Ask one question only when `draft-notes.md` lists new material or a contradiction.
-6. **Wave 5, post.** Load `refs/labels.md`. Apply only the mode label, and only when it exists in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` and `--type "<name>"` when the wanted issue type is listed in `scout.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; read the issue type back; set the Complexity field with the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`); post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory, the labels not applied and every `not set` line. A failed type or field never stops the run once the issue exists. No ClickUp call (B6).
+5. **Wave 4, draft the body** with the depth's worker into `<D>/issue-body.md` and `<D>/draft-notes.md`. At every depth the worker fills `## Priority`, `## Fix approach` and `## Test plan` from the `/sc:analyze` pass and never writes "Not known yet" there (rules in `refs/create.md`). Ask no question when `draft-notes.md` holds only additions or nothing; ask one combined question only for a supported contradiction of the user's own description, instruction or flag.
+6. **Wave 5, post.** Load `refs/labels.md`. Apply only the mode label, and only when it exists in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` and `--type "<name>"` when the wanted issue type is listed in `scout.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; read the issue type back; set the Complexity field with the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`); post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory, the labels not applied, every `not set` line, one `kept without approval: <item>` line for every retained addition and the question outcome. A failed type or field never stops the run once the issue exists. No ClickUp call (B6).
 
 ## Return contract
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 019966285..f4feaf11e 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -3057,7 +3057,7 @@ WRITE_VERB_CLASSIFICATION = {
     (
         "src/superclaude/skills/sc-issue-protocol/SKILL.md",
         "gh api",
-        '6. **Wave 5, post.** Load `refs/labels.md`. Apply only the mode label, and only when it exists in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` and `--type "<name>"` when the wanted issue type is listed in `scout.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; read the issue type back; set the Complexity field with the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`); post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory, the labels not applied and every `not set` line. A failed type or field never stops the run once the issue exists. No ClickUp call (B6).',
+        '6. **Wave 5, post.** Load `refs/labels.md`. Apply only the mode label, and only when it exists in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` and `--type "<name>"` when the wanted issue type is listed in `scout.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; read the issue type back; set the Complexity field with the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`); post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory, the labels not applied, every `not set` line, one `kept without approval: <item>` line for every retained addition and the question outcome. A failed type or field never stops the run once the issue exists. No ClickUp call (B6).',
     ): (
         "never-worker",
         "/sc:issue is on the never-as-worker list; its type, field and comment writes run only in the coordinator or person session",


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
