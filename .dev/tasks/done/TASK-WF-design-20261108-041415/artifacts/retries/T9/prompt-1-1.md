8c2187e50df7c483ccc5bfe42c01e6c693f727a7
Review one task for spec compliance.

Task brief: ## Task 9: Update the user guide for the new create behaviour

Depends on: Task 6

Edit `docs/user-guide/commands.md` and `docs/user-guide/flags.md`. Source sections: decisions Q5, Q6, Q7; section 3.1. In `commands.md` the create description (line 349), the `--mode` row (line 365), the `--type` row (line 366) and the Will line (line 394) currently say labels from a fixed set and `type: <value>` labels: rewrite them to the new behaviour (issue type Feature, Bug or Test; Complexity field from depth; mode label only; anything not set is listed). In `flags.md` the `--mode` row (line 228) and `--type` row (line 229) get the same treatment. Keep the value lists of both flags unchanged.

Acceptance criteria:
- Neither file says that `/sc:issue --create` applies `type:` or `complexity:` labels or labels "from a fixed set".
- Both files say the issue type and the Complexity field are set, the mode label is applied when it exists, and unset items are listed in the final output.
- The `--type` value list in both files is unchanged.

AC ids:
T9.AC1: Neither file says that `/sc:issue --create` applies `type:` or `complexity:` labels or labels "from a fixed set".
T9.AC2: Both files say the issue type and the Complexity field are set, the mode label is applied when it exists, and unset items are listed in the final output.
T9.AC3: The `--type` value list in both files is unchanged.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 8c2187e50df7c483ccc5bfe42c01e6c693f727a7
Diff against the start snapshot: 
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 38472be6..85579032 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -346,7 +346,7 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 
 ### `/sc:issue` - GitHub Issue Claim and Create
 
-**When to use:** Take an existing GitHub issue on the repository `origin` points at, or file a new one. `--claim` assigns the issue to you, checks whether its text is still accurate against today's code and the pull requests merged since it was opened, writes a summary (with an effort estimate in hours) and a next-step prompt under `.dev/issues/<N>/`, posts an accuracy-check comment and a claim comment, then creates (or reuses) an Orca worktree named `issue-<N>` and launches one Claude Code agent in it. How far that agent goes is the `--pipeline` level (below); nothing ever merges. Orca must be running: without it the claim stops with `E-ORCA-REQUIRED` before it assigns or posts anything. `--create` turns a description into an issue built from one of four templates (feature or bug, simple or complex) with labels from a fixed set.
+**When to use:** Take an existing GitHub issue on the repository `origin` points at, or file a new one. `--claim` assigns the issue to you, checks whether its text is still accurate against today's code and the pull requests merged since it was opened, writes a summary (with an effort estimate in hours) and a next-step prompt under `.dev/issues/<N>/`, posts an accuracy-check comment and a claim comment, then creates (or reuses) an Orca worktree named `issue-<N>` and launches one Claude Code agent in it. How far that agent goes is the `--pipeline` level (below); nothing ever merges. Orca must be running: without it the claim stops with `E-ORCA-REQUIRED` before it assigns or posts anything. `--create` turns a description into an issue built from one of four templates (feature or bug, simple or complex). It sets the GitHub issue type (Feature, Bug or Test) and the Complexity issue field of your organization (Simple, Medium or Complex, from `--depth`), and applies the `enhancement` or `bug` label when the repository has it. Anything it could not set is listed in the final output.
 
 **Syntax:**
 
@@ -362,8 +362,8 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 | `--claim <number\|url>` | claim | - | The issue to claim: a number (`302`, `#302`) or an issue URL on the origin repo |
 | `--create "<description>"` | create | - | The feature or bug description, as text or `@path` to a file |
 | `--depth quick\|standard\|deep` | create | `quick` | How hard the command checks your flags and fills the body; `deep` uses the complex template |
-| `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template and the `enhancement` or `bug` label |
-| `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; maps to a `type: <value>` label |
+| `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` or `bug` label |
+| `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md` and no label is applied for it |
 | `--pipeline worktree\|full\|none` | claim | `worktree` | How far the launched agent goes (see the levels below); every value creates the worktree, `none` launches no agent |
 | `--submit` | claim | off | Only with `--pipeline full`: the agent also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Takes no value |
 
@@ -391,7 +391,7 @@ No level merges anything: people review and merge. The agent starts behind the c
 /sc:issue --create @notes/new-command.md --depth deep
 ```
 
-It posts directly to GitHub, without showing the comment or the issue body for approval first. It never creates labels: a label from the fixed set that the repository does not have is skipped and listed. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. The claim itself never runs a step of `.dev/issues/<N>/next-steps.md`: the launched agent does, at the level you chose (with `--pipeline none` you run them yourself in the worktree). A re-claim reuses the existing worktree and does not launch a second agent, also when you re-claim from inside the worktree; the claim output names the two files that hold the launch (`.dev/issues/<N>/worktree.json` and a file in the worktree's git directory), and removing the `launch` entry from both launches again. Worktree or launch problems are warnings: the issue stays assigned and the comments stay posted.
+It posts directly to GitHub, without showing the comment or the issue body for approval first. It never creates labels, issue types or issue fields: a mode label that the repository does not have, and an issue type or Complexity field it cannot set, are skipped and listed in the final output. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. The claim itself never runs a step of `.dev/issues/<N>/next-steps.md`: the launched agent does, at the level you chose (with `--pipeline none` you run them yourself in the worktree). A re-claim reuses the existing worktree and does not launch a second agent, also when you re-claim from inside the worktree; the claim output names the two files that hold the launch (`.dev/issues/<N>/worktree.json` and a file in the worktree's git directory), and removing the `launch` entry from both launches again. Worktree or launch problems are warnings: the issue stays assigned and the comments stay posted.
 
 **ClickUp settings (claim only, environment variables):**
 
diff --git a/docs/user-guide/flags.md b/docs/user-guide/flags.md
index bfc31632..3e328eb8 100644
--- a/docs/user-guide/flags.md
+++ b/docs/user-guide/flags.md
@@ -225,11 +225,13 @@ Opt in only for PRs from collaborators trusted with your credentials: lock regen
 | `--claim` | Claim an existing issue on the origin repo | Issue number (`302`, `#302`) or issue URL |
 | `--create` | File a new issue | Text, or `@path` to a file holding the description |
 | `--depth` | How hard create mode checks your flags and fills the body (create only) | `quick` (default), `standard`, `deep` |
-| `--mode` | Feature or bug template and label (create only) | `feature`, `bug`; chosen by a worker when omitted |
-| `--type` | Area of the change, mapped to a `type: <value>` label (create only) | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other`; chosen by a worker when omitted |
+| `--mode` | Feature or bug template, issue type (Feature or Bug) and mode label (create only) | `feature`, `bug`; chosen by a worker when omitted |
+| `--type` | Area of the change; a feature in `tests` gets the issue type Test, otherwise it is recorded in `flags.md` and no label is applied (create only) | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other`; chosen by a worker when omitted |
 
 Pass exactly one of `--claim` and `--create`. There is no repository flag: the repository is always `origin`.
 
+On `--create` the command sets the GitHub issue type and the Complexity issue field of your organization (Simple, Medium or Complex, from `--depth`: quick, standard or deep), applies the `enhancement` or `bug` mode label when the repository has it, and lists anything it could not set in the final output. It never creates a label, an issue type or an issue field.
+
 ## Advanced Control Flags
 
 Like the flags at the top of this page, the flags under Scope and Focus and Execution Control are hints Claude may honour, not options every command accepts. No installed file defines them since 5.0.0 (`FLAGS.md` is no longer shipped and an old copy in `~/.claude/` is not loaded), so Claude knows them only if you explain them. Check a command's own entry in the [Commands Reference](commands.md) before passing one. The System Flags further down are different: System Flags are options of the `superclaude` command (run in a terminal), not slash-command flags; the table names the command or subcommand for each.

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
