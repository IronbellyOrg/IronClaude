3800f60ed60e85388e0d4e0dd95c90709bbf101f
Review one task for spec compliance.

Task brief: ## Task 10: Update the sc-issue command design document

Depends on: Task 9

Edit `docs/designs/sc-issue-command.md`. Source sections: decisions Q1 to Q8; section 3.1. Replace the statements that labels come from a fixed set or that `type:` and `complexity:` labels are applied, at the places listed by grep for "label" (around lines 18, 76, 77, 197, 207, 224, 225, 283 to 293, 354, 366, 370, 449, 479 and 492): the create bullet; the `--mode` and `--type` option rows; the Wave 1 lookup text (add the issue types and the Complexity field lookups and the single `orgs/` read); the Wave 2 sentence ending "not silently relabelled" (use "reclassified"); the Wave 5 step list; section 11 "Label set" (now: the two mode labels, the issue type rule and the Complexity field mapping, with a note that the `type:` and `complexity:` labels were dropped because the repo has none); the error row for a missing label; the file-table rows for `SKILL.md` return contract keys and `refs/labels.md`; the gh flags table row for `gh issue create` (add `--type`) and the acceptance line 6. Keep rule B7 ("none are created on the fly") true and add that no issue type or field is created either. Leave history and decision-log entries as they are except for wording that is now false.

Acceptance criteria:
- `docs/designs/sc-issue-command.md` no longer says that `type: <type>` or `complexity: <...>` labels are applied, and its section 11 matches `refs/labels.md` from Task 1.
- The `gh issue create` row lists `--type`, and the return contract description lists `issue_type`, `complexity_field` and `classification_missing`.
- Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read.

AC ids:
T10.AC1: `docs/designs/sc-issue-command.md` no longer says that `type: <type>` or `complexity: <...>` labels are applied, and its section 11 matches `refs/labels.md` from Task 1.
T10.AC2: The `gh issue create` row lists `--type`, and the return contract description lists `issue_type`, `complexity_field` and `classification_missing`.
T10.AC3: Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 3800f60ed60e85388e0d4e0dd95c90709bbf101f
Diff against the start snapshot: 
diff --git a/docs/designs/sc-issue-command.md b/docs/designs/sc-issue-command.md
index 73530bea..b1a0dd31 100644
--- a/docs/designs/sc-issue-command.md
+++ b/docs/designs/sc-issue-command.md
@@ -15,9 +15,9 @@
 `/sc:issue` has two modes:
 
 - **`--claim <number|url>`**: take an existing GitHub issue. Assign it to the current user on GitHub and, when it exists, on its ClickUp task; check whether the issue text is still accurate against today's code and the pull requests merged since the issue was opened; write a summary cheatsheet; build the next-step prompt (which commands to run, with which flags, on which model tier); post the results to the issue; then **stop**. It never starts the brainstorm, design, plan or implementation itself.
-- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with labels from a fixed set, and post it. GitHub only: no ClickUp task.
+- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label, and post it. GitHub only: no ClickUp task.
 
-Out of scope: running the next-step chain, creating labels, creating ClickUp tasks, editing CLAUDE.md core rule 10 (which still governs issues filed without `/sc:issue`), and any interaction with an upstream parent repository.
+Out of scope: running the next-step chain, creating labels, issue types or issue fields, creating ClickUp tasks, editing CLAUDE.md core rule 10 (which still governs issues filed without `/sc:issue`), and any interaction with an upstream parent repository.
 
 ## 2. Binding decisions (issue body + three comments)
 
@@ -31,7 +31,7 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 | B4 | `/sc:recommend` picks the starting chain and depth; downstream skills size their own work. | Comment 1 |
 | B5 | Every output comes from a template and is saved under `.dev/issues/<number>/`: four issue-body templates, the summary doc, the accuracy-check comment. Issue templates start from GFxAI `ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`. | Comment 1 |
 | B6 | `--create` makes the GitHub issue only, no ClickUp task. | Comment 1 |
-| B7 | Labels come from a fixed set defined in this spec; none are created on the fly. | Comment 1 |
+| B7 | Classification comes from a fixed set defined in this spec (the mode labels, the issue type and the Complexity field); none is created on the fly. (Amended 2026-11-08, issue 438: the area and complexity labels were replaced by the issue type and the Complexity field, because the repository has no such labels.) | Comment 1; amended by issue 438 |
 | B8 | Agent definitions pin a model by its picker ID (for example `claude-gw-tier1`). | Comment 1 |
 | B9 | Claim edge cases: assigned to someone else -> stop and say so; closed -> stop; claimed before -> update the earlier comment, no duplicate. | Comment 1 |
 | B10 | The repo is always the one `origin` points at, never an upstream parent. | Comment 1 |
@@ -73,8 +73,8 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 | `--claim` | claim | - | issue number (`302`, `#302`) or issue URL on the origin repo | Claim this issue |
 | `--create` | create | - | free text, or `@path` to a file holding the description | Description of the feature or bug |
 | `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body (section 8) |
-| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template and the `enhancement` / `bug` label |
-| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; maps to a `type: <value>` label |
+| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label |
+| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md` and no label is applied for it |
 
 STOP rules (in the command file, before Activation):
 
@@ -194,7 +194,7 @@ Load `refs/create.md` at the start of this mode. Files are written to `<D>` = `.
 
 **Wave 0: prerequisites.** Same repo, auth and directory steps as claim Wave 0. Write the description to `<D>/description.md`.
 
-**Wave 1: lookup (issue-worker-t3, B13).** The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`), and writes `<D>/scout.md` (same template as claim, create section). Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).
+**Wave 1: lookup (issue-worker-t3, B13).** The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), reads the repo's issue types (`gh api repos/<R>/issue-types`) and the Complexity field of the organization (`gh api orgs/<owner of R>/issue-fields`, the one allowed `orgs/` read; a failed lookup is recorded and never stops the run), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`), and writes `<D>/scout.md` (same template as claim, create section). Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).
 
 **Wave 2: settle the flags.** "All flags given" means both `--mode` and `--type` were passed. When only one was passed, the given one is kept and the missing one is chosen as in the "missing" rows (default D12).
 
@@ -204,7 +204,7 @@ Load `refs/create.md` at the start of this mode. Files are written to `<D>` = `.
 | standard | `issue-worker-t2` runs a quick validation of the user's flags; differences become a pushback comment posted after the issue (Wave 5) | `issue-worker-t1` chooses |
 | deep | Two variants debated: `<D>/flags-user.md` (the user's flags) and `<D>/flags-t1.md` (an independent choice by `issue-worker-t1`), then `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`; differences become the pushback comment (default D13) | `issue-worker-t1` runs `/sc:analyze` on the code the description touches, then chooses |
 
-Complexity follows depth, as the issue body pairs them: `quick` = simple, `standard` = medium, `deep` = complex. Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, complexity, reasons). The flags the issue is filed with are the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently relabelled), else the worker's choice.
+Complexity follows depth, as the issue body pairs them: `quick` = Simple, `standard` = Medium, `deep` = Complex (the option names of the Complexity field). Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, issue type, complexity, reasons); the `Issue type` row is derived from the mode and the area (a bug is Bug, a feature in `tests` is Test, any other feature is Feature). The flags the issue is filed with are the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently reclassified), else the worker's choice.
 
 **Wave 3: pick the template.** Mode selects feature or bug; depth selects simple or complex: `quick` and `standard` -> simple template, `deep` -> complex template (issue body).
 
@@ -221,11 +221,13 @@ The worker fills the chosen template into `<D>/issue-body.md`, keeping every hea
 If `draft-notes.md` lists new material or a contradiction, the orchestrator asks the user one question (AskUserQuestion) naming each item, with choices "keep all", "drop the new material", "edit" (issue body: "result in a prompt to the user to confirm"). If it lists nothing, the issue is posted without any prompt. The full body is never shown for approval (B1; default D14 explains how the two rules fit together).
 
 **Wave 5: post (orchestrator, directly).**
-1. Labels = the mode label + `type: <type>` + `complexity: <simple|medium|complex>`, intersected with the labels that exist in `<R>` (section 11). Missing ones are listed in the final output, never created (B7).
-2. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label <label> ...` with prefix `[FEATURE] ` or `[BUG] ` (from the GFxAI templates).
-3. Rename `<D>` to `.dev/issues/<N>/`.
-4. Standard or deep with all flags given and a disagreement in Wave 2: post `.dev/issues/<N>/create-review.md` (from `templates/create-review-comment.md`, marker `<!-- sc:issue:create-review -->`) with `gh issue comment <N> --repo <R> --body-file ...`.
-5. Print the issue URL and the directory. No ClickUp call (B6). No self-assignment.
+1. Labels = the mode label only, intersected with the labels that exist in `<R>` (section 11). A missing one is listed in the final output, never created (B7).
+2. Issue type: the wanted type follows the mode and the area (section 11). When it is listed in `scout.md`, the create command of step 3 gets `--type "<name>"`; otherwise the flag is omitted and the gap is listed.
+3. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label <label>` (plus `--type "<name>"`) with prefix `[FEATURE] ` or `[BUG] ` (from the GFxAI templates).
+4. Rename `<D>` to `.dev/issues/<N>/`, then read the type back (`gh issue view <N> --repo <R> --json issueType`) and list it as not set when it is empty or different.
+5. Complexity field: when `scout.md` lists the field and the option, write `.dev/issues/<N>/complexity-field.json` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`; read the values back and list the field as not set when the POST fails or the value is absent.
+6. Standard or deep with all flags given and a disagreement in Wave 2: post `.dev/issues/<N>/create-review.md` (from `templates/create-review-comment.md`, marker `<!-- sc:issue:create-review -->`) with `gh issue comment <N> --repo <R> --body-file ...`.
+7. Print the issue URL, the directory, every `not applied` line and every `not set` line. A failed type or field never stops the run once the issue exists. No ClickUp call (B6). No self-assignment.
 
 ## 9. Next-step chains (what `next-steps.md` may contain)
 
@@ -280,17 +282,19 @@ The four issue-body templates, adapted from GFxAI `.dev/proj_mgmt/clickup-integr
 
 Every posted template ends with its hidden marker line (`<!-- sc:issue:claim -->`, `<!-- sc:issue:accuracy-check -->`, `<!-- sc:issue:create-review -->`, `<!-- sc:issue:create template=<name> -->`).
 
-## 11. Label set
+## 11. Labels, issue type and fields
 
-The only labels `/sc:issue` ever applies (B7). It never creates a label.
+The only classifications `/sc:issue` ever sets (B7). It never creates a label, an issue type or an issue field. `--claim` changes none of them.
 
-| Group | Labels | Applied by |
+| Classification | Values | Set by |
 |---|---|---|
-| Mode | `bug`, `enhancement` | `--create` (GitHub's default labels; present on IronbellyOrg/IronClaude, checked 2026-11-04) |
-| Type | `type: cicd`, `type: command`, `type: skill`, `type: agent`, `type: hook`, `type: cli`, `type: core`, `type: docs`, `type: tests`, `type: install`, `type: other` | `--create` |
-| Complexity | `complexity: simple`, `complexity: medium`, `complexity: complex` | `--create` |
+| Mode label | `bug`, `enhancement` | `--create` (GitHub's default labels; present on IronbellyOrg/IronClaude, checked 2026-11-04) |
+| Issue type | Bug (mode bug), Test (feature in the area `tests`), Feature (any other feature); Task is never chosen | `--create` through `gh issue create --type` |
+| Complexity field | Simple, Medium, Complex (quick, standard, deep) | `--create` through one POST to `repos/<R>/issues/<N>/issue-field-values` |
 
-At run time the skill applies only the labels from this set that already exist in `<R>` and lists the rest as "not applied: label missing in repo". `refs/labels.md` holds the one-time `gh label create "<name>" --repo <owner/repo>` lines a maintainer may run by hand to add them (default D16). `--claim` changes no labels.
+The earlier area labels (one per `--type` value) and complexity labels were dropped on 2026-11-08 (issue 438): the repository never had them, so they were always reported as not applied.
+
+At run time the skill sets what it can and lists the rest: "not applied: label missing in repo: <name>", "not set: issue type <name>: <reason>" and "not set: field Complexity <value>: <reason>". The exact lines and reasons are in `refs/labels.md`, which also holds the one-time `gh label create "<name>" --repo <owner/repo>` lines a maintainer may run by hand to add the two mode labels (default D16). A failed type or field never stops the run once the issue exists.
 
 ## 12. ClickUp lookup and assignment
 
@@ -327,8 +331,8 @@ Implementation-time check: the response shapes of `GET /user` and the task list
 ## 13. Repository resolution and GitHub call rules
 
 - `<R>` is parsed from `git remote get-url origin`, accepting `https://github.com/<owner>/<repo>(.git)` and `git@github.com:<owner>/<repo>(.git)`. Nothing else is consulted: not `gh repo set-default`, not `gh`'s fork-parent default, not a `--repo` flag (B10).
-- Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>`; every `gh api` path spells `repos/<R>/...`, never `{owner}/{repo}`. This matches the fork rule in the project `CLAUDE.md` and how `/sc:pr-submit` pins its target.
-- Workers make read-only `gh` calls only. All writes (`gh issue edit`, `gh issue comment`, `gh api -X PATCH`, `gh issue create`) happen in the orchestrator.
+- Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>`; every `gh api` path spells `repos/<R>/...`, never `{owner}/{repo}`, with one exception: the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash; no other `orgs/` path). This matches the fork rule in the project `CLAUDE.md` and how `/sc:pr-submit` pins its target.
+- Workers make read-only `gh` calls only. All writes (`gh issue edit`, `gh issue comment`, `gh api -X PATCH`, `gh issue create` with `--type`, and `gh api -X POST repos/<R>/issues/<N>/issue-field-values`) happen in the orchestrator.
 - `git fetch origin` is the only fetch; no other remote is added or fetched.
 
 ## 14. Error handling
@@ -351,7 +355,9 @@ Implementation-time check: the response shapes of `GET /user` and the task list
 | `/sc:recommend` asks a question or finds no route | Record it in `recommend.md`; `next-steps.md` uses the default row from `refs/chains.md` and says so |
 | Comment post or edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |
 | `gh issue create` fails | STOP `E-CREATE-FAILED`; the draft directory is kept |
-| A label in the fixed set is missing in the repo | Skip it; list it in the final output |
+| The mode label is missing in the repo | Skip it; list it in the final output |
+| The wanted issue type is missing, its lookup failed, or it is not applied after create | Create without `--type` or keep the issue; list `not set: issue type ...`; continue |
+| The Complexity field or option is missing, the POST fails, or the value is not applied after create | Keep the issue; list `not set: field Complexity ...`; continue |
 | `codegraph` / `auggie` unavailable for `/sc:analyze` | The worker continues on Grep/Glob/Read and records it in its file |
 
 ## 15. Files to create or change
@@ -363,11 +369,11 @@ All under `src/superclaude/` unless stated. Nothing under `.claude/` is edited o
 | Path | Content |
 |---|---|
 | `src/superclaude/commands/issue.md` | Thin command (~100-150 lines): frontmatter (`name: issue`, `category: workflow`, `complexity: advanced`, `mcp-servers: [auggie, codegraph]`, `personas: [analyzer]`, `argument-hint`), Usage, Options table (section 4), STOP rules, Examples, Boundaries, `## Activation` -> `Skill sc:issue-protocol`, naming `~/.claude/skills/sc-issue-protocol/SKILL.md` |
-| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | `name: sc:issue-protocol`; `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`; waves of sections 7 and 8 at the WHAT/WHEN level; per-wave ref loading; spawn rule (never pass `model`); return contract (`status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`); error table (section 14); Will / Will Not. Under 500 lines |
+| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | `name: sc:issue-protocol`; `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`; waves of sections 7 and 8 at the WHAT/WHEN level; per-wave ref loading; spawn rule (never pass `model`); return contract (`status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`, and in create mode `issue_type`, `complexity_field`, `classification_missing`); error table (section 14); Will / Will Not. Under 500 lines |
 | `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Claim waves in detail; effort and complexity rubric (default D5); marker handling |
 | `src/superclaude/skills/sc-issue-protocol/refs/create.md` | Create waves; flag-settling table; depth-to-worker table; contradiction prompt rule |
 | `src/superclaude/skills/sc-issue-protocol/refs/chains.md` | The six default chains of section 9 and the `/sc:recommend` goal format |
-| `src/superclaude/skills/sc-issue-protocol/refs/labels.md` | The fixed label set and the maintainer's one-time `gh label create` lines |
+| `src/superclaude/skills/sc-issue-protocol/refs/labels.md` | The mode labels, the issue type and Complexity field rules, the output lines and the maintainer's one-time `gh label create` lines |
 | `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` | Tier map, the pinning rule and its verified reason, `E-TIER-UNAVAILABLE` |
 | `src/superclaude/skills/sc-issue-protocol/templates/` | `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `issue-summary.md`, `accuracy-check-comment.md`, `claim-comment.md`, `next-steps.md`, `scout-report.md`, `recommend-record.md`, `description.md`, `flags-decision.md`, `draft-notes.md`, `create-review-comment.md` |
 | `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` | Section 12; standard library only; no secrets in output |
@@ -446,7 +452,7 @@ Each is a **design default**: a choice made where the issue and comments are sil
 | D13 | Create, deep, all flags given: two variants (user's flags, T1's independent choice) debated with `/sc:adversarial --compare ... --depth quick` | The issue's "parallel agents each invoke `/sc:adversarial --depth quick`" needs at least two variants to compare; this is the smallest form |
 | D14 | Create asks the user one question only when the drafter found new material or a contradiction; otherwise it posts without any prompt; the full body is never previewed | The issue body requires that confirmation; B1 forbids routine previews. The two do not conflict once the prompt is limited to those findings |
 | D15 | `clickup.json` has no template | It is a script's machine output, not a document |
-| D16 | Missing labels from the fixed set are skipped and reported; `refs/labels.md` gives the maintainer's one-time creation lines | B7 forbids creating labels at run time |
+| D16 | A missing mode label, issue type or Complexity field is skipped and reported; `refs/labels.md` gives the maintainer's one-time creation lines for the two mode labels | B7 forbids creating labels, types and fields at run time |
 | D17 | On create, complexity follows depth (quick = simple, standard = medium, deep = complex) | The issue body pairs them |
 | D18 | Two marked comments on claim (accuracy check, claim overview); a re-claim edits both | B5 names the accuracy-check comment; B9 forbids duplicates |
 | D19 | Picker IDs are written without the `[1m]` context suffix | Comment 1's example form; the suffix belongs to session launch, not to subagent pinning. The plan's smoke step confirms one spawn per worker |
@@ -476,9 +482,10 @@ Checked on 2026-11-04 against the installed files `~/.claude/commands/sc/<name>.
 | `/sc:pr-submit` | `--monitor 3`, `--head`, `--title`, `--body` | `pr-submit.md` Options table |
 | `/task` | `<task file path>` (this is the `task` skill, not `/sc:task`) | `~/.claude/skills/task/` installed; `troubleshoot.md` names "`/task <path>`" as the MDTM route's user step |
 | `gh issue edit` | `--add-assignee @me`, `--repo` | `gh issue edit --help` |
-| `gh issue create` | `--title`, `--body-file`, `--label` (repeatable), `--repo` | `gh issue create --help` |
+| `gh issue create` | `--title`, `--body-file`, `--label` (repeatable), `--type`, `--repo` | `gh issue create --help` (gh 2.103.3, checked 2026-11-08) |
+| `gh api` (issue types and fields) | `repos/<R>/issue-types` (GET); `orgs/<owner of R>/issue-fields` (GET, the one allowed `orgs/` read); `-X POST repos/<R>/issues/<N>/issue-field-values --input <file>` with body `{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}`; `repos/<R>/issues/<N>/issue-field-values` (GET read-back) | GitHub Docs, "REST API endpoints for issue field values" (read 2026-11-08); the POST itself has not been run against a real issue |
 | `gh issue comment` | `--body-file`, `--repo` (`--edit-last` deliberately not used: it edits the user's last comment, not necessarily the claim comment) | `gh issue comment --help` |
-| `gh issue view`, `gh label list` | `--json <fields>`, `--repo` | `gh issue view --help`, `gh label list --help` |
+| `gh issue view`, `gh label list` | `--json <fields>` (including `issueType`), `--repo` | `gh issue view --help`, `gh label list --help` |
 
 ## 20. Acceptance criteria for the implementation
 
@@ -489,7 +496,7 @@ Checked on 2026-11-04 against the installed files `~/.claude/commands/sc/<name>.
 3. A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write.
 4. A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`; no `gh` call is made without `--repo <origin repo>`.
 5. With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped; with a token and a task that links the issue URL, that task gains the user as assignee.
-6. `/sc:issue --create "<text>" --mode bug --type cli` at each depth posts an issue whose body follows the selected template's headings, with only labels from section 11 that exist in the repo; at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made.
+6. `/sc:issue --create "<text>" --mode bug --type cli` at each depth posts an issue whose body follows the selected template's headings, with the issue type and the Complexity field of section 11 set where the repo and organization allow it, the mode label when it exists in the repo, and every classification it could not set listed in the final output; at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made.
 7. Each worker agent file pins its picker ID, and the skill never passes `model` on an Agent call (static test); one manual smoke run per worker shows it was served by the pinned tier.
 8. `next-steps.md` contains only commands and flags listed in section 19, starts with the `/model` tier line of section 9, and never contains `--handoff tasklist` or `--handoff design` on a brainstorm step.
 9. `make verify-sync` passes; the tests of section 16 pass; `uv run pytest tests/core tests/commands` passes; the `src/superclaude` path grep shows no new hit in the new primitives.

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
