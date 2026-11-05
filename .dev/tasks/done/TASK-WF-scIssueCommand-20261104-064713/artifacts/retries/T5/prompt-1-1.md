51e981f2a58e171f257c851bd0960eb2470787a0
Review one task for spec compliance.

Task brief: ## Task 5: Create the five skill refs

Depends on: Task 4

Create under `src/superclaude/skills/sc-issue-protocol/refs/`:
- `claim.md`: claim Waves 0 to 6 of source section 7 in detail, the gh commands exactly as written there (each with `--repo <R>`), with one addition: the merged-PR query `gh pr list --repo <R> --state merged ...` also passes `--limit 200` and the worker records in `scout.md` when the result hit that limit (gh's default is 30). Wave 1 also carries the git commands as written there: `git fetch origin` (origin only; no other remote is added or fetched) followed by `git log --since=<createdAt> --name-only` on `origin/<default branch>`. Also: the edge-case STOPs of Wave 2 (closed, assigned to someone else, pull request number, re-claim allowed), the marker handling that edits an earlier `<!-- sc:issue:claim -->` / `<!-- sc:issue:accuracy-check -->` comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>` instead of posting a duplicate (B9, D18), the ClickUp script call `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R>` writing stdout to `.dev/issues/<N>/clickup.json`, and the effort and complexity rubric of default D5 (simple up to 4 hours in one area; medium over 4 up to 16 hours; complex over 16 hours, more than one subsystem, or a security/data-migration change; effort recorded in hours).
- `create.md`: create Waves 0 to 5 of source section 8, the draft directory `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` renamed to `.dev/issues/<N>/` after creation (D10), the flag-settling table of Wave 2 (including D12 and D13: deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`), complexity following depth (D17), the template choice of Wave 3, the depth-to-worker table of Wave 4, the one-question contradiction prompt rule (D14), duplicates listed in related issues without stopping (D11), labels intersected with the repo's labels and never created (B7), title prefixes `[FEATURE] ` / `[BUG] ` (D21), no ClickUp call and no self-assignment (B6).
- `chains.md`: the six default chains of source section 9 copied exactly (tier lines and chains, every brainstorm step with `--models opus,sonnet` and no `--handoff`), the four notes under that table, and the `/sc:recommend` goal format of section 7 Wave 5 step 1 (issue URL, type, complexity, summary path, suggested default row).
- `labels.md`: the fixed label set of source section 11 and one `gh label create "<name>" --repo <owner/repo>` line per label for a maintainer to run by hand (D16), with the statement that the skill never runs them.
- `tiers.md`: the tier map of source section 6, the four verified pinning facts (resolution order; the Agent call's `model` parameter takes aliases only and overrides frontmatter; frontmatter accepts a full model ID; `haiku` follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`), the note that an installed mod's `agent.spawn` hook can override the pin, and `E-TIER-UNAVAILABLE` with no alias fallback (D4).

Every one of the five refs carries the sentence "Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter." (source section 6: "`SKILL.md` and every ref state"). Each ref names agents and the analyze command by installed path (`~/.claude/agents/issue-worker-t<N>.md`, project `.claude/agents/` first; `~/.claude/commands/sc/analyze.md`) and templates by their path relative to the skill base.

Acceptance criteria:
- The five ref files exist at the paths above.
- `grep -n -- '--handoff' src/superclaude/skills/sc-issue-protocol/refs/chains.md` shows no `--handoff tasklist` and no `--handoff design`; every `/sc:brainstorm` line in it carries `--models opus,sonnet`.
- `grep -rIn 'src/superclaude' src/superclaude/skills/sc-issue-protocol/refs` prints nothing.
- `grep -L 'never pass the `model` parameter' src/superclaude/skills/sc-issue-protocol/refs/*.md` prints nothing (all five refs carry the phrase).
- `refs/claim.md` contains `git fetch origin` and `--limit 200` on the merged-PR query.

AC ids: T5.AC1..T5.AC5 = the five acceptance bullets in order (files exist; chains.md handoff and --models checks; no src/superclaude in refs; all five refs carry the never-pass-model phrase; claim.md has git fetch origin and --limit 200). The executor's check output is saved at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t5-ref-checks.txt.

Coordinator constraints that apply here (binding; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md and round2-minor-findings.md):
- C2: claim Wave 0 resolves <R> and <N> through the tested script call `origin_repo.py --claim "<argument>"` (exit 1 E-NO-ORIGIN, 3 E-FOREIGN-REPO, 4 E-NOT-AN-ISSUE; Task 1's script). No live /sc:issue run is made.
- C4 correctness fixes applied: F-03 (every gh issue/pr/label mention carries --repo <R>, the placeholder rule is written without the literal brace token, checked by the shared scan from tests/skills/test_issue_worker_agents.py); F-18 (claim Wave 2 reads `is_pull_request` from scout.md and STOPs E-NOT-AN-ISSUE first).
- Disclosed executor choices inside this task: claim Wave 0 step 3 resolves the default branch with `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name` (repo named explicitly) so the worker can run the `git log ... origin/<default branch>` the source requires; the earlier comment ID is read from the `#issuecomment-<id>` part of the comment URL; ClickUp script exit 2 (bad arguments) stops the run, matching source.md:163 ("Any ClickUp outcome other than an argument error is non-fatal").
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 6, 7, 8, 9, 11, 12, 13, 14, defaults D4-D25.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 51e981f2a58e171f257c851bd0960eb2470787a0
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
new file mode 100644
index 00000000..8c67b816
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -0,0 +1,90 @@
+# Claim mode (`/sc:issue --claim <number|url>`)
+
+Loaded at the start of claim mode. `<R>` is the origin repo (`owner/repo`), `<N>` the issue number, `<D>` = `.dev/issues/<N>/`, `<skill base>` the directory that holds this skill's `SKILL.md`.
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.
+
+Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md` (Claude Code reads the project `.claude/agents/` copy first when one exists). Load `refs/tiers.md` before the first spawn. A worker that needs a codebase pass runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`. Every file under `<D>` starts as a copy of its template under `templates/`.
+
+Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub or ClickUp.
+
+## Wave 0: prerequisites (orchestrator)
+
+1. Resolve `<R>` and `<N>` in one call:
+   `uv run --no-project python "<skill base>/scripts/origin_repo.py" --claim "<argument>"`
+   It reads only the `origin` remote and prints `{"repo": "<owner/repo>", "number": <N>}`. Exit 1 = STOP `E-NO-ORIGIN` (no `origin`, or not a GitHub URL). Exit 3 = STOP `E-FOREIGN-REPO` (a URL naming any repo other than origin, B10). Exit 4 = STOP `E-NOT-AN-ISSUE` (a `/pull/<N>` URL, or not an issue number or URL). Print the script's stderr line with the STOP.
+2. `gh auth status` must succeed; else STOP `E-GH-AUTH`.
+3. Resolve the default branch `<B>` with `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name` (the repo is named explicitly).
+4. Create `<D>`.
+
+No GitHub or ClickUp write happens before Wave 3.
+
+## Wave 1: lookup (issue-worker-t3, B13)
+
+Spawn `issue-worker-t3` before doing any lookup yourself, with the job "claim lookup", `<R>`, `<N>`, `<B>` and `<D>`. The worker:
+
+- runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`;
+- lists pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url` (gh's default limit is 30) and records in `scout.md` whether the result reached the 200 limit;
+- runs `git fetch origin` (origin only; no other remote is added or fetched), then `git log --since=<createdAt> --name-only origin/<B>` for the recent commits on the default branch;
+- finds an earlier claim by this user: a comment authored by the current login whose body contains `<!-- sc:issue:claim -->`, and likewise `<!-- sc:issue:accuracy-check -->`. The comment ID used for editing is the number after `#issuecomment-` in that comment's `url`. When more than one comment carries the same marker, the latest one is used;
+- writes `<D>/scout.md` from `templates/scout-report.md` (claim section): state, `url`, `is_pull_request` (true when `url` contains `/pull/`), assignees, current login, earlier comment IDs, the merged pull requests and changed files since creation and whether that list was truncated, a first complexity guess (`simple|medium|complex`) and a type guess (`feature|bug`), each with a one-line reason;
+- returns the path.
+
+Worker returns no file or an empty one: retry that worker once, then STOP `E-WORKER-NO-OUTPUT` naming `<D>/scout.md`.
+
+## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)
+
+Checked in this order; every STOP here makes no GitHub or ClickUp write (B9):
+
+1. `is_pull_request` is true -> STOP `E-NOT-AN-ISSUE`: "#N is a pull request, not an issue; not claimed."
+2. `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed."
+3. Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed."
+4. Already assigned to the current login -> continue (re-claim is allowed and idempotent).
+5. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).
+
+## Wave 3: assign (orchestrator)
+
+1. `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED`; ClickUp is not touched and no comment is posted.
+2. Run the ClickUp script and write its stdout to `<D>/clickup.json`:
+   `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`
+   Every outcome it prints (`assigned`, `already_assigned`, `skipped`, `not_found`, `ambiguous`, `error`) is non-fatal and is reported in the claim comment. Exit 2 means the skill passed bad arguments: STOP and print the script's usage message; the GitHub assignment stays. Never print, echo or inline `CLICKUP_API_TOKEN`.
+
+## Wave 4: accuracy check and summary
+
+Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` sizes the issue `complex` (default D8), with the job "accuracy check and summary", `<R>`, `<N>` and `<D>`. The worker assumes the issue text is out of date and:
+
+- checks each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and checks each merged pull request and changed file from `scout.md` for relevance;
+- writes `<D>/accuracy-check.md` from `templates/accuracy-check-comment.md` with the verdict `current` or `out_of_date` and the evidence for each changed claim;
+- when `out_of_date`: runs `/sc:analyze` on the paths the issue touches (`--depth deep` when complex, no `--depth` otherwise) and saves the report under `<D>/analysis/`;
+- always writes `<D>/summary.md` from `templates/summary.md`: what the issue asks for, the relevant files and systems (the cheatsheet), type, complexity, the effort estimate in hours using the rubric below (B3), and links to anything under `<D>/analysis/` (default D22);
+- returns both paths.
+
+Missing or empty file: retry the worker once, then STOP `E-WORKER-NO-OUTPUT` naming the missing path.
+
+### Effort and complexity rubric (default D5)
+
+| Complexity | Rule |
+|---|---|
+| simple | up to 4 hours of work in one area |
+| medium | over 4 and up to 16 hours |
+| complex | over 16 hours, or more than one subsystem, or a security or data-migration change |
+
+Effort is always recorded in hours.
+
+## Wave 5: next steps (orchestrator)
+
+Load `refs/chains.md`.
+
+1. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`: issue URL, type, complexity, the summary path and the default chain row for that type and complexity as the suggested route. `/sc:recommend` picks the starting chain and depth (B4). Save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`.
+2. Write `<D>/next-steps.md` from `templates/next-steps.md`: the `/model` tier line first (simple -> `claude-gw-tier2`, medium and complex -> `claude-gw-tier1a`, default D6), then the commands in order with their flags and the inputs each needs (`@.dev/issues/<N>/summary.md`), the effort estimate, and, when `/sc:recommend` chose differently from the default row, one line naming the default row and why it was not used (default D23). When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and use the default row, saying so.
+3. Do not run any of those commands (B2).
+
+## Wave 6: post (orchestrator, directly, B1)
+
+1. Accuracy-check comment, body `<D>/accuracy-check.md` (it ends with `<!-- sc:issue:accuracy-check -->`). If Wave 2 remembered an earlier accuracy-check comment ID, edit it:
+   `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md`
+   otherwise post a new one:
+   `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`
+2. Claim comment: write `<D>/claim-comment.md` from `templates/claim-comment.md`: who claimed it, the ClickUp result from `clickup.json`, the summary overview, effort estimate, complexity, accuracy verdict, the first next step, and repo-relative links to `<D>/summary.md`, `<D>/next-steps.md` and `<D>/analysis/` with the one-line note that they open on GitHub only after someone commits and pushes the files (default D9). It ends with `<!-- sc:issue:claim -->`. Edit the earlier claim comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md`, or post it with `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`.
+3. A post or edit that fails -> STOP `E-POST-FAILED`; the files stay in `<D>`, and a re-run edits rather than duplicates because of the markers.
+4. Print the `next-steps.md` path and STOP. Do not stage or commit `.dev/issues/` (default D24).
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/create.md b/src/superclaude/skills/sc-issue-protocol/refs/create.md
new file mode 100644
index 00000000..27022aab
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/refs/create.md
@@ -0,0 +1,69 @@
+# Create mode (`/sc:issue --create "<description>"`)
+
+Loaded at the start of create mode. `<R>` is the origin repo (`owner/repo`), `<skill base>` the directory that holds this skill's `SKILL.md`. Files are written to `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then the directory is renamed to `.dev/issues/<N>/` (default D10). `<slug>` is the first words of the description in lower case, joined by `-`, at most 40 characters.
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.
+
+Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md` (Claude Code reads the project `.claude/agents/` copy first when one exists). Load `refs/tiers.md` before the first spawn. A worker that needs a codebase pass runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`. Every file under `<D>` starts as a copy of its template under `templates/`.
+
+Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub. Create mode makes no ClickUp call and no self-assignment (B6).
+
+## Wave 0: prerequisites (orchestrator)
+
+1. `uv run --no-project python "<skill base>/scripts/origin_repo.py"` prints `<R>` from the `origin` remote; a non-zero exit is STOP `E-NO-ORIGIN`.
+2. `gh auth status` must succeed; else STOP `E-GH-AUTH`.
+3. Create `<D>`.
+4. Write the description to `<D>/description.md` from `templates/description.md`. An `@path` description is read from that file.
+
+## Wave 1: lookup (issue-worker-t3, B13)
+
+Spawn `issue-worker-t3` with the job "create lookup", `<R>`, the description's keywords and `<D>`. The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`) and writes `<D>/scout.md` from `templates/scout-report.md` (create section). Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).
+
+Worker returns no file or an empty one: retry once, then STOP `E-WORKER-NO-OUTPUT` naming the path.
+
+## Wave 2: settle the flags
+
+"All flags given" means both `--mode` and `--type` were passed. When only one was passed, keep it and choose the missing one as in the "a flag missing" column (default D12).
+
+| Depth | All flags given | A flag missing |
+|---|---|---|
+| quick | Take the user's flags at face value; the orchestrator writes `<D>/flags.md` | `issue-worker-t2` reads `description.md` and `scout.md` and chooses |
+| standard | `issue-worker-t2` runs a quick validation of the user's flags; differences become a pushback comment posted after the issue (Wave 5) | `issue-worker-t1` chooses |
+| deep | Two variants debated: the orchestrator writes `<D>/flags-user.md` (the user's flags) and `issue-worker-t1` writes `<D>/flags-t1.md` (an independent choice), then `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`; differences become the pushback comment (default D13) | `issue-worker-t1` runs `/sc:analyze` on the code the description touches, then chooses |
+
+Complexity follows depth, as the issue body pairs them (default D17): `quick` = simple, `standard` = medium, `deep` = complex.
+
+Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, complexity, reasons); `flags-user.md` and `flags-t1.md` use the same template. The issue is filed with the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently relabelled), else with the worker's choice.
+
+## Wave 3: pick the template
+
+Mode selects feature or bug; depth selects simple or complex:
+
+| Mode | `quick` or `standard` | `deep` |
+|---|---|---|
+| feature | `templates/issue-feature-simple.md` | `templates/issue-feature-complex.md` |
+| bug | `templates/issue-bug-simple.md` | `templates/issue-bug-complex.md` |
+
+## Wave 4: draft the body
+
+| Depth | Worker | Codebase pass |
+|---|---|---|
+| quick | `issue-worker-t3` | `/sc:analyze --depth quick` on the touched area |
+| standard | `issue-worker-t2` | `/sc:analyze` (no `--depth`) |
+| deep | `issue-worker-t1` | `/sc:analyze --depth deep` |
+
+The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts). It lists, in `<D>/draft-notes.md` (from `templates/draft-notes.md`), any new material it added beyond the description and any contradiction between the description and the code.
+
+### Contradiction prompt rule (default D14)
+
+If `draft-notes.md` lists new material or a contradiction, ask the user one question (AskUserQuestion) naming each item, with the choices "keep all", "drop the new material" and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5. If it lists nothing, post the issue without any prompt. The full body is never shown for approval (B1).
+
+## Wave 5: post (orchestrator, directly)
+
+Load `refs/labels.md`.
+
+1. Labels = the mode label (`enhancement` for feature, `bug` for bug) + `type: <type>` + `complexity: <simple|medium|complex>`, intersected with the repo labels in `scout.md`. Missing ones are listed in the final output, never created (B7).
+2. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label "<label>" ...` (one `--label` per applied label), with the prefix `[FEATURE] ` or `[BUG] ` (default D21). Failure -> STOP `E-CREATE-FAILED`; the draft directory is kept.
+3. Read `<N>` from the issue URL that step 2 prints, then rename `<D>` to `.dev/issues/<N>/`.
+4. Standard or deep with all flags given and a disagreement in Wave 2: write `.dev/issues/<N>/create-review.md` from `templates/create-review-comment.md` (it ends with `<!-- sc:issue:create-review -->`) and post it with `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md`. Failure -> STOP `E-POST-FAILED`.
+5. Print the issue URL, the directory and any `not applied: label missing in repo` lines. No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/chains.md b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
new file mode 100644
index 00000000..e69533d9
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
@@ -0,0 +1,39 @@
+# Next-step chains
+
+Loaded in claim Wave 5.
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`.)
+
+These are the default rows passed to `/sc:recommend` as the suggested route. `/sc:recommend` makes the final pick (B4). `<S>` = `.dev/issues/<N>/summary.md`; `<symptom>` is the bug's one-line symptom from the summary (at least 10 words); `<scope>` is the main path from the summary. `/sc:issue` never runs these commands (B2); it writes them into `next-steps.md` from `templates/next-steps.md`.
+
+| Type / complexity | Tier line | Chain |
+|---|---|---|
+| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
+| Feature, medium | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
+| Feature, complex | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
+| Bug, simple | `/model claude-gw-tier2` | 1. `/sc:troubleshoot "<symptom>" --depth quick --context <S> --scope <scope>`<br>2. `/sc:implement <REPORT.md path printed by step 1>` |
+| Bug, medium | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --fix --context <S> --scope <scope>` (plan route: after the report it offers to build the `/sc:workflow` package; the user accepts, and it then prints the `/sc:implement` command)<br>2. `/sc:implement <plan path printed by step 1>` |
+| Bug, complex | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --depth deep --fix --context <S> --scope <scope>` (MDTM route: after the report it offers to build the task file with `task-builder`; the user accepts, and it then prints the `/task` command)<br>2. `/task <task file path printed by step 1>` |
+
+Notes:
+- `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
+- `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
+- `/sc:brainstorm --models` defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only. Every brainstorm row passes `--models opus,sonnet` so no proposal runs on the `haiku` alias, which on this workspace resolves to `glm-5.3` (`refs/tiers.md`), below T2 (B14). Aliases cannot name a picker ID, so this is the closest the chain can get to B14 inside a brainstorm; the session tier itself is pinned by the `/model` line (default D25).
+- `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.
+
+No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:workflow` and `/sc:design` run as their own steps.
+
+## Goal sent to `/sc:recommend` (claim Wave 5 step 1)
+
+Invoke `Skill sc-recommend` with this goal, filled from `summary.md`:
+
+```text
+Pick the next-step chain for GitHub issue <issue url>.
+Type: <feature|bug>. Complexity: <simple|medium|complex>.
+Summary: .dev/issues/<N>/summary.md
+Suggested route (default row "<Type>, <complexity>" of the /sc:issue chains):
+<tier line>
+<the numbered chain of that row, one step per line>
+```
+
+Save the skill's output verbatim to `.dev/issues/<N>/recommend.md` from `templates/recommend-record.md`. When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and write `next-steps.md` from the default row, saying so. When it chooses a different route, `next-steps.md` follows `/sc:recommend` and names the unused default row in one line (default D23).
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/labels.md b/src/superclaude/skills/sc-issue-protocol/refs/labels.md
new file mode 100644
index 00000000..22d48060
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/refs/labels.md
@@ -0,0 +1,45 @@
+# Label set
+
+Loaded in create Wave 5.
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`.)
+
+These are the only labels `/sc:issue` ever applies (B7). It never creates a label. `--claim` changes no labels.
+
+| Group | Labels | Applied by |
+|---|---|---|
+| Mode | `bug`, `enhancement` | `--create` (`feature` mode gets `enhancement`, `bug` mode gets `bug`) |
+| Type | `type: cicd`, `type: command`, `type: skill`, `type: agent`, `type: hook`, `type: cli`, `type: core`, `type: docs`, `type: tests`, `type: install`, `type: other` | `--create` |
+| Complexity | `complexity: simple`, `complexity: medium`, `complexity: complex` | `--create` |
+
+## At run time
+
+1. The wanted labels are the mode label, `type: <type>` and `complexity: <simple|medium|complex>`.
+2. Intersect them with the repo labels that `scout.md` lists (create Wave 1 read them with `gh label list --repo <R> --limit 200 --json name`).
+3. Pass each label that exists as one `--label "<name>"` to `gh issue create --repo <R>`.
+4. List every label that does not exist in the final output as `not applied: label missing in repo: <name>`. Never create it.
+
+## One-time creation lines for a maintainer (default D16)
+
+A maintainer may run these by hand, once, to add the labels to a repo. The skill never runs them. Replace `<owner/repo>` with the target repo.
+
+```bash
+gh label create "bug" --repo <owner/repo>
+gh label create "enhancement" --repo <owner/repo>
+gh label create "type: cicd" --repo <owner/repo>
+gh label create "type: command" --repo <owner/repo>
+gh label create "type: skill" --repo <owner/repo>
+gh label create "type: agent" --repo <owner/repo>
+gh label create "type: hook" --repo <owner/repo>
+gh label create "type: cli" --repo <owner/repo>
+gh label create "type: core" --repo <owner/repo>
+gh label create "type: docs" --repo <owner/repo>
+gh label create "type: tests" --repo <owner/repo>
+gh label create "type: install" --repo <owner/repo>
+gh label create "type: other" --repo <owner/repo>
+gh label create "complexity: simple" --repo <owner/repo>
+gh label create "complexity: medium" --repo <owner/repo>
+gh label create "complexity: complex" --repo <owner/repo>
+```
+
+`bug` and `enhancement` are GitHub's default labels and usually exist already.
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
new file mode 100644
index 00000000..b8aa058d
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
@@ -0,0 +1,44 @@
+# Model tiers and worker pinning
+
+Loaded before the first worker spawn of either mode.
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.
+
+Workers are the agent files `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`; Claude Code reads the project `.claude/agents/` copy first when one exists. Workers run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`.
+
+## Tier map (default D3)
+
+| Tier | Picker ID pinned in agent frontmatter | Agent | Used for |
+|---|---|---|---|
+| T3 | `claude-gw-tier3` | `issue-worker-t3` | the first lookup on every claim and create (B13); quick-depth issue body |
+| T2 | `claude-gw-tier2` | `issue-worker-t2` | accuracy check and summary on simple and medium claims; flag choice at quick depth when a flag is missing; validation of user-given flags at standard depth; standard-depth body. Next-step chains for simple work (B14) |
+| T1 | `claude-gw-tier1a` | `issue-worker-t1` | accuracy check and summary on complex claims; flag choice at standard and deep depth when a flag is missing; the independent flag variant for the deep adversarial check; deep body. Next-step chains for medium and complex work (B14) |
+
+Picker IDs are written without the `[1m]` context suffix (default D19).
+
+## Why the pin lives in frontmatter
+
+Verified against the Claude Code subagent docs (`https://code.claude.com/docs/en/sub-agents`, read 2026-11-04):
+
+1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
+2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
+3. Frontmatter `model:` accepts an alias, a full model ID (the same values as the `--model` flag) or `inherit`.
+4. The `haiku` alias resolves through `ANTHROPIC_DEFAULT_HAIKU_MODEL`, which on this Coder workspace is `glm-5.3`. So "spawn with haiku" does not guarantee the T3 tier.
+
+So each tier has its own agent file whose `model:` is the picker ID, and the spawn passes only `subagent_type`.
+
+An installed mod whose `agent.spawn` hook sets a model overrides the pin (same docs page). The skill does not try to detect this; if a worker is served by the wrong model, look there first.
+
+## `E-TIER-UNAVAILABLE` (default D4)
+
+If a spawn fails because the picker ID is not served (for example, outside a ccsession tier workspace), STOP `E-TIER-UNAVAILABLE`, naming the agent file and the picker ID, for example:
+
+```text
+E-TIER-UNAVAILABLE: ~/.claude/agents/issue-worker-t3.md pins claude-gw-tier3, which this session cannot serve.
+```
+
+There is no alias fallback: a fallback to `haiku` can land on a non-Claude model (`glm-5.3` here), which defeats B13.
+
+## Next-step tier (defaults D6 and D25)
+
+The tier for the user's next-step chain is written into `next-steps.md` as its first line: `/model claude-gw-tier2` for simple work, `/model claude-gw-tier1a` for medium and complex work. The user runs the chain in their own session (B2, B14).
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t5-ref-checks.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t5-ref-checks.txt
new file mode 100644
index 00000000..e8674d0b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t5-ref-checks.txt
@@ -0,0 +1,29 @@
+$ ls src/superclaude/skills/sc-issue-protocol/refs
+chains.md
+claim.md
+create.md
+labels.md
+tiers.md
+$ grep -n -- '--handoff' src/superclaude/skills/sc-issue-protocol/refs/chains.md (no '--handoff tasklist' and no '--handoff design' may appear)
+11:| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
+12:| Feature, medium | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
+13:| Feature, complex | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
+$ grep -c -e '--handoff tasklist' -e '--handoff design' src/superclaude/skills/sc-issue-protocol/refs/chains.md
+0
+$ /sc:brainstorm step spans in the chain table (each must carry --models opus,sonnet)
+`/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet`
+`/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`
+`/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`
+$ grep -rIn 'src/superclaude' src/superclaude/skills/sc-issue-protocol/refs
+exit=1 (grep exit 1 = no match)
+$ grep -L 'never pass the `model` parameter' src/superclaude/skills/sc-issue-protocol/refs/*.md (prints the files that lack the phrase)
+(nothing above = all five refs carry the phrase)
+$ grep -n 'git fetch origin\|--limit 200' src/superclaude/skills/sc-issue-protocol/refs/claim.md
+27:- lists pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url` (gh's default limit is 30) and records in `scout.md` whether the result reached the 200 limit;
+28:- runs `git fetch origin` (origin only; no other remote is added or fetched), then `git log --since=<createdAt> --name-only origin/<B>` for the recent commits on the default branch;
+$ fork-safety scan (gh_lines_missing_repo from tests/skills/test_issue_worker_agents.py) over refs: file, mentions missing --repo, brace placeholder present
+chains.md [] False
+claim.md [] False
+create.md [] False
+labels.md [] False
+tiers.md [] False

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
