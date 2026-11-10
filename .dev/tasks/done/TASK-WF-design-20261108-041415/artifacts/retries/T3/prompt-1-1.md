dc2e9bf9211f2a7d01c3bde2e96a8ae6947713d5
Review one task for spec compliance.

Task brief: ## Task 3: Update SKILL.md to match the new create behaviour and return contract

Depends on: Task 1, Task 2

Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md`. Source sections: decisions Q4, Q6; specification 2.2, 2.3, 2.5. Change these places, re-reading the live line numbers first: the frontmatter description (line 3) and the create bullet (line 18) so they say the issue is filed with an issue type, the Complexity field and a mode label instead of "labels from a fixed set"; the files-table row for `refs/labels.md` (line 31); the GitHub call rules (lines 73 and 74): add the single `orgs/<owner of R>/issue-fields` read exception for the T3 worker and add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list, workers still never write; the create steps 1 to 6 (lines 98 to 103) so Wave 1 and Wave 5 match `refs/create.md`; the return contract: keep the first block key for key and the claim block unchanged, add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`, and the sentence "Create mode adds these three fields after the claim block (claim mode prints none of them; on a STOP the fields that do not apply are `null`)"; the error table row for a missing label (line 161) plus two new rows (issue type not available or not applied, Complexity field not available or write failed), both listed and non-fatal; and the Will Not list (lines 172 to 177): keep every existing item and add that the skill never creates an issue type or an issue field and never writes a field other than Complexity.

Acceptance criteria:
- `SKILL.md` has no "labels from a fixed set" wording left, and its Will Not list still contains the tokens `/sc:implement`, `/task`, a commit, a push, `/sc:pr-submit`, "Merge anything." and "Pass an Orca link flag".
- The Return contract section holds exactly three YAML blocks; the first block's keys are unchanged and the third block's keys are exactly `issue_type`, `complexity_field`, `classification_missing`.
- The error table has a row for each of: missing label, issue type not set, Complexity field not set; each says skip or continue and list it in the final output; `gh issue create` failure stays STOP `E-CREATE-FAILED`.
- The call rules name the one `orgs/<owner of R>/issue-fields` exception and the field POST, and the file contains no `-X PUT`, no brace placeholder and no `src/superclaude/`.

AC ids:
T3.AC1: `SKILL.md` has no "labels from a fixed set" wording left, and its Will Not list still contains the tokens `/sc:implement`, `/task`, a commit, a push, `/sc:pr-submit`, "Merge anything." and "Pass an Orca link flag".
T3.AC2: The Return contract section holds exactly three YAML blocks; the first block's keys are unchanged and the third block's keys are exactly `issue_type`, `complexity_field`, `classification_missing`.
T3.AC3: The error table has a row for each of: missing label, issue type not set, Complexity field not set; each says skip or continue and list it in the final output; `gh issue create` failure stays STOP `E-CREATE-FAILED`.
T3.AC4: The call rules name the one `orgs/<owner of R>/issue-fields` exception and the field POST, and the file contains no `-X PUT`, no brace placeholder and no `src/superclaude/`.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: dc2e9bf9211f2a7d01c3bde2e96a8ae6947713d5
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index d8069129..c7921f09 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: sc:issue-protocol
-description: "Behavioral protocol for /sc:issue: --claim assigns an existing GitHub issue on the origin repo (and its ClickUp task), checks its accuracy, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the --pipeline level; --create files a templated GitHub issue with labels from a fixed set. Spawns tier-pinned worker agents for every lookup and draft; the orchestrator makes every GitHub and ClickUp write."
+description: "Behavioral protocol for /sc:issue: --claim assigns an existing GitHub issue on the origin repo (and its ClickUp task), checks its accuracy, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the --pipeline level; --create files a templated GitHub issue with a GitHub issue type, the Complexity issue field and a mode label. Spawns tier-pinned worker agents for every lookup and draft; the orchestrator makes every GitHub and ClickUp write."
 allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion
 ---
 
@@ -15,7 +15,7 @@ mcp-servers: [auggie, codegraph]
 Two modes, chosen by the command (`~/.claude/commands/sc/issue.md`), which has already validated the flags:
 
 - **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then create or reuse the Orca worktree `issue-<N>` and copy `.dev/issues/<N>/` into it, and (unless `--pipeline none`) launch one agent there at the level `--pipeline` names: `worktree` (default) plans and waits for approval, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Nothing ever merges. This skill never runs a step of `next-steps.md` itself (B2).
-- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with labels from a fixed set, and post it. GitHub only: no ClickUp task and no self-assignment (B6).
+- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label, and post it. GitHub only: no ClickUp task and no self-assignment (B6).
 
 For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
 
@@ -28,7 +28,7 @@ For issues filed through `/sc:issue --create`, its four templates replace the `I
 | `refs/claim.md` | at the start of claim mode: Waves 0-8 in detail, the effort and complexity rubric, marker handling |
 | `refs/create.md` | at the start of create mode: Waves 0-5, flag-settling table, depth-to-worker table, contradiction prompt rule |
 | `refs/chains.md` | claim Wave 5: the six default next-step chains and the `/sc:recommend` goal format |
-| `refs/labels.md` | create Wave 5: the fixed label set and the maintainer's one-time creation lines |
+| `refs/labels.md` | create Wave 5: the mode labels, the issue type and Complexity field rules, the output lines and the maintainer's one-time label creation lines |
 | `refs/tiers.md` | before the first worker spawn of either mode: tier map, pinning rule, `E-TIER-UNAVAILABLE` |
 | `scripts/origin_repo.py` | Wave 0 of both modes: prints `owner/repo` from `origin`; with `--claim` also checks the claim argument against it |
 | `scripts/clickup_claim.py` | claim Wave 3: assigns the matching ClickUp task |
@@ -70,8 +70,8 @@ Every spawn prompt names each exact path the job must write under `.dev/issues/`
 ## Repository and GitHub call rules
 
 - `<R>` is the `origin` repo, printed by `uv run --no-project python "<skill base>/scripts/origin_repo.py"`. Nothing else is consulted: not `gh repo set-default`, not gh's fork-parent default, not a `--repo` flag (B10). There is no `--repo` option on the command.
-- Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder.
-- The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` and `scripts/clickup_claim.py`. Workers never write to either.
+- Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder. The one exception is the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash; no other `orgs/` path is allowed, and the orchestrator and the T1 and T2 workers keep the old rule).
+- The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` (create mode adds `--type <name>`), `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and `scripts/clickup_claim.py`. Workers never write to either.
 - `git fetch origin` is the only fetch; no other remote is added or fetched.
 - Posts go up directly (B1); the full body or comment is never shown for approval. The only user prompt is the create-mode contradiction question (`refs/create.md`, default D14).
 - `.dev/issues/` is never staged or committed by this skill (default D24).
@@ -96,15 +96,15 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 Load `refs/create.md` now. `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then `.dev/issues/<N>/` (default D10).
 
 1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py"` resolves `<R>` (STOP `E-NO-ORIGIN`); `gh auth status` (else STOP `E-GH-AUTH`); create `<D>`; write `<D>/description.md` from `templates/description.md`.
-2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13): repo labels and possible duplicates into `<D>/scout.md`.
-3. **Wave 2, settle the flags** by the depth table of `refs/create.md`; complexity follows depth; the result goes to `<D>/flags.md` from `templates/flags-decision.md`. Deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`.
+2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13): repo labels, repo issue types, the Complexity field of the organization and possible duplicates into `<D>/scout.md`.
+3. **Wave 2, settle the flags** by the depth table of `refs/create.md`; complexity follows depth and the `Issue type` row follows from the mode and the area; the result goes to `<D>/flags.md` from `templates/flags-decision.md`. Deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`.
 4. **Wave 3, pick the template**: mode selects feature or bug; `quick`/`standard` select the simple template, `deep` the complex one.
 5. **Wave 4, draft the body** with the depth's worker into `<D>/issue-body.md` and `<D>/draft-notes.md`. Ask one question only when `draft-notes.md` lists new material or a contradiction.
-6. **Wave 5, post.** Load `refs/labels.md`. Apply only the labels of the fixed set that exist in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory and the labels not applied. No ClickUp call (B6).
+6. **Wave 5, post.** Load `refs/labels.md`. Apply only the mode label, and only when it exists in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` and `--type "<name>"` when the wanted issue type is listed in `scout.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; read the issue type back; set the Complexity field with the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`); post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory, the labels not applied and every `not set` line. A failed type or field never stops the run once the issue exists. No ClickUp call (B6).
 
 ## Return contract
 
-Print this block last, in both modes, including after a STOP (fields that do not apply are `null`):
+Print this return contract last, in both modes, including after a STOP (fields that do not apply are `null`). The block below is printed first; the mode's added fields follow it. `labels_applied` and `labels_missing` cover the mode label only:
 
 ```yaml
 status: success | stopped | failed
@@ -135,6 +135,14 @@ enforcement_hook: installed | missing | null
 
 `launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` reports the IR-4 preflight of the launch: `installed` means it passed (also when the launch then failed), `missing` means it failed and the launch was refused (`launch_status` `failed`, `launch_warning` `W-ENFORCEMENT-ABSENT`, no agent started), and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). `launch_warning` is the first launch code: a `launched` claim without an L2 pre-push layer carries `W-LAUNCH-NOT-CCSESSION` there when that also applies, else `W-L2-ABSENT`. The claim `status` stays `success` through any worktree or launch warning.
 
+Create mode adds these three fields after the claim block (claim mode prints none of them; on a STOP the fields that do not apply are `null`):
+
+```yaml
+issue_type: <name of the issue type read back from the issue, or null>
+complexity_field: <option name read back from the issue, or null>
+classification_missing: [<each "not set" line without its prefix>, ...]
+```
+
 On a STOP, also print the STOP code and its message.
 
 ## Error handling
@@ -158,7 +166,9 @@ On a STOP, also print the STOP code and its message.
 | `/sc:recommend` asks a question or finds no route | Record it in `recommend.md`; `next-steps.md` uses the default row from `refs/chains.md` and says so |
 | `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |
 | `gh issue create --repo <R>` fails | STOP `E-CREATE-FAILED`; the draft directory is kept |
-| A label of the fixed set is missing in the repo | Skip it; list it in the final output |
+| The mode label is missing in the repo | Skip it; list it as `not applied: label missing in repo: <name>` in the final output |
+| The wanted issue type is missing in the repo, the lookup failed, or the type is not applied after create | Create the issue without `--type` or keep it as created; continue and list `not set: issue type <name>: <reason>` in the final output |
+| The Complexity field or its option is missing, the lookup failed, the POST fails or the value is not applied after create | Keep the issue; continue and list `not set: field Complexity <value>: <reason>` in the final output |
 | codegraph or auggie unavailable for `/sc:analyze` | The worker continues on Grep, Glob and Read and records it in its file |
 
 ## Will
@@ -174,7 +184,8 @@ On a STOP, also print the STOP code and its message.
 - Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself, or any step of `next-steps.md` (the launched agent may, at the level the user chose).
 - Merge anything.
 - Pass an Orca link flag, or call `orca` anywhere but `scripts/orca_worktree.py`.
-- Create a label, a ClickUp task or a GitHub repository setting.
+- Create a label, an issue type, an issue field, a ClickUp task or a GitHub repository setting.
+- Write any issue field other than Complexity.
 - Pass the `model` parameter on an Agent call, or fall back to an alias.
 - Touch any repository other than `origin`, or fetch any other remote.
 - Stage or commit `.dev/issues/`, or edit source code.

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
