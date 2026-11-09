56252a1c3f1e7dab9027444aaeda94b91d6cca0e
Review one task for spec compliance.

Task brief: ## Task 6: Update the /sc:issue command file wording

Depends on: Task 3

Edit `src/superclaude/commands/issue.md`. Source sections: decisions Q5, Q6; section 3.1. Change the frontmatter description (line 4) and the create bullet (line 17) from "labels from a fixed set" to an issue type, the Complexity field and a mode label; the `--mode` row (line 41) to "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"; the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests` and is otherwise recorded in `flags.md`, and no longer maps to a `type: <value>` label; the Will line for create (line 89) to "set the issue type and the Complexity field, apply only the mode label that already exists in the repo, and list everything it could not set"; and the Will Not line (line 93) to also say it creates no issue types or issue fields. The Options table values for `--type` stay the same 11 values. The file must not contain `src/superclaude/`.

Acceptance criteria:
- `commands/issue.md` has no "labels from a fixed set" and no `type: <value>` label wording.
- The `--type` value list is unchanged, and `uv run pytest tests/skills/test_issue_protocol.py -k "command" -v` passes.
- The Will and Will Not lists agree with the skill's Will and Will Not lists on the new create behaviour.

AC ids:
T6.AC1: `commands/issue.md` has no "labels from a fixed set" and no `type: <value>` label wording.
T6.AC2: The `--type` value list is unchanged, and `uv run pytest tests/skills/test_issue_protocol.py -k "command" -v` passes.
T6.AC3: The Will and Will Not lists agree with the skill's Will and Will Not lists on the new create behaviour.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 56252a1c3f1e7dab9027444aaeda94b91d6cca0e
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index 42cbd5b0..7d8b9753 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -1,7 +1,7 @@
 ---
 name: issue
 version: "1.1.0"
-description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then create an Orca worktree and launch an agent in it) or create a templated issue with labels from a fixed set"
+description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then create an Orca worktree and launch an agent in it) or create a templated issue with a GitHub issue type, the Complexity issue field and a mode label"
 category: workflow
 complexity: advanced
 mcp-servers: [auggie, codegraph]
@@ -14,7 +14,7 @@ argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit]
 Two modes on the repository that `origin` points at:
 
 - `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` creates the worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); when the worktree has no L2 pre-push layer it warns with `W-L2-ABSENT` and the launch continues (the L2 layer is not built yet). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
-- `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.
+- `--create` turns a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label. GitHub only: no ClickUp task.
 
 Both modes post directly to GitHub; nothing is shown for approval first.
 
@@ -38,8 +38,8 @@ Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...
 | `--claim` | claim | - | issue number (`302`, `#302`) or issue URL on the origin repo | Claim this issue |
 | `--create` | create | - | free text, or `@path` to a file holding the description | Description of the feature or bug |
 | `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body |
-| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template and the `enhancement` / `bug` label |
-| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; maps to a `type: <value>` label |
+| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label |
+| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md`; no label is applied for it |
 | `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes. Every value creates the worktree; `none` launches no agent |
 | `--submit` | claim | off | no value | Only with `--pipeline full`: the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
 
@@ -86,11 +86,12 @@ After a claim, the launched agent works from `.dev/issues/<N>/launch-prompt.md`
 - Spawn tier-pinned worker agents for every lookup, accuracy check and draft.
 - Write every artifact under `.dev/issues/` from a template.
 - On claim: assign the issue, assign the ClickUp task when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, post or update the accuracy-check and claim comments, create or reuse the Orca worktree `issue-<N>`, and (unless `--pipeline none`) launch one agent in it at the chosen level. Nothing is ever merged.
-- On create: apply only the labels of the fixed set that already exist in the repo, and list the rest as not applied.
+- On create: set the issue type and the Complexity field, apply only the mode label that already exists in the repo, and list everything it could not set.
 
 **Will Not:**
 - Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose).
-- Create labels, ClickUp tasks, or interact with any repository other than `origin`.
+- Create labels, issue types, issue fields, ClickUp tasks, or interact with any repository other than `origin`.
+- Write any issue field other than Complexity.
 - Stage or commit `.dev/issues/`.
 - Pass an Orca link flag.
 - Merge anything.

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
