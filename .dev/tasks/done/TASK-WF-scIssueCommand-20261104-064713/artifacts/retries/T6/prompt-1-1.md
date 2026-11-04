71954debbc384e62d4e8df229e8e891b8a2fa80b
Review one task for spec compliance.

Task brief: ## Task 6: Write the orchestrator SKILL.md

Depends on: Task 1, Task 2, Task 3, Task 5

Create `src/superclaude/skills/sc-issue-protocol/SKILL.md` (source section 15 row, sections 5, 7, 8, 13, 14, D26). Frontmatter: `name: sc:issue-protocol`, a one-line `description`, `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`. Body, fewer than 500 lines as counted by `len(text.splitlines())`, at the WHAT/WHEN level: the two modes; Wave 0 of both modes calls `uv run --no-project python "<skill base>/scripts/origin_repo.py"` to resolve `<R>` (STOP `E-NO-ORIGIN`); per-wave ref loading (`refs/claim.md` for claim, `refs/create.md` for create, `refs/chains.md` in claim Wave 5, `refs/labels.md` in create Wave 5, `refs/tiers.md` before the first spawn); the claim waves and the create waves as short steps pointing at their refs; the spawn rule ("spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter"); the orchestrator is the only place that writes to GitHub or ClickUp, and every `gh` call carries `--repo <R>` while every `gh api` path spells `repos/<R>/...` (section 13); `/sc:recommend` invoked as `Skill sc-recommend` with its output saved verbatim to `.dev/issues/<N>/recommend.md`; the claim stops after posting and printing the `next-steps.md` path, never running a next-step command (B2); the return contract fields `status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`; the full error table of source section 14 with every STOP code (`E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-GH-AUTH`, `E-NOT-AN-ISSUE`, `E-TIER-UNAVAILABLE`, `E-WORKER-NO-OUTPUT`, `E-ASSIGN-FAILED`, `E-POST-FAILED`, `E-CREATE-FAILED`); the D26 one-line note that for issues filed through `/sc:issue --create` its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; `.dev/issues/` is never staged or committed by the skill (D24); Will / Will Not. Every ref and template the skill uses is named in `SKILL.md` by its skill-relative path (`refs/...`, `templates/...`, `scripts/...`).

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/SKILL.md` exists, has fewer than 500 lines by the `len(text.splitlines())` rule (the same rule Task 7's test uses), and has the frontmatter above.
- Every `refs/*.md`, `templates/*.md` and `scripts/*.py` file in the skill directory is named in `SKILL.md`, and every such path named in `SKILL.md` exists.
- `SKILL.md` contains "never pass the `model` parameter", every STOP code listed above, and the D26 rule-10 line.
- `grep -n 'src/superclaude' src/superclaude/skills/sc-issue-protocol/SKILL.md` prints nothing.

AC ids: T6.AC1..T6.AC4 = the four acceptance bullets in order. The executor's check output is saved at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t6-skill-checks.txt.

Coordinator constraints that apply here (binding; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md and round2-minor-findings.md):
- C2: claim Wave 0 calls the tested URL-versus-origin check `origin_repo.py --claim "<argument>"` (Task 1's script; exit 3 = E-FOREIGN-REPO).
- C4 correctness fixes applied: F-03 (every gh issue/pr/label mention in SKILL.md, the error table and the write list included, carries --repo <R>; the placeholder rule is written without the literal brace token); F-17 (the D26 rule-10 sentence has one fixed wording, which Task 8's command file and test reuse byte for byte): "For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`."
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 4, 5, 6, 7, 8, 13, 14, 15 (SKILL.md row), defaults D24, D26.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 71954debbc384e62d4e8df229e8e891b8a2fa80b
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
new file mode 100644
index 00000000..443d4142
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -0,0 +1,153 @@
+---
+name: sc:issue-protocol
+description: "Behavioral protocol for /sc:issue: --claim assigns an existing GitHub issue on the origin repo (and its ClickUp task), checks its accuracy, writes a summary and a next-step prompt, then stops; --create files a templated GitHub issue with labels from a fixed set. Spawns tier-pinned worker agents for every lookup and draft; the orchestrator makes every GitHub and ClickUp write."
+allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion
+---
+
+<!-- Extended metadata (for documentation, not parsed):
+category: workflow
+complexity: advanced
+mcp-servers: [auggie, codegraph]
+-->
+
+# /sc:issue protocol
+
+Two modes, chosen by the command (`~/.claude/commands/sc/issue.md`), which has already validated the flags:
+
+- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then **stop**. The claim never runs a next-step command (B2).
+- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with labels from a fixed set, and post it. GitHub only: no ClickUp task and no self-assignment (B6).
+
+For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
+
+`<skill base>` below is the directory that holds this `SKILL.md` (`~/.claude/skills/sc-issue-protocol/` when installed; the project `.claude/skills/sc-issue-protocol/` copy in a dev checkout).
+
+## Files of this skill
+
+| Path (skill-relative) | Loaded or used |
+|---|---|
+| `refs/claim.md` | at the start of claim mode: Waves 0-6 in detail, the effort and complexity rubric, marker handling |
+| `refs/create.md` | at the start of create mode: Waves 0-5, flag-settling table, depth-to-worker table, contradiction prompt rule |
+| `refs/chains.md` | claim Wave 5: the six default next-step chains and the `/sc:recommend` goal format |
+| `refs/labels.md` | create Wave 5: the fixed label set and the maintainer's one-time creation lines |
+| `refs/tiers.md` | before the first worker spawn of either mode: tier map, pinning rule, `E-TIER-UNAVAILABLE` |
+| `scripts/origin_repo.py` | Wave 0 of both modes: prints `owner/repo` from `origin`; with `--claim` also checks the claim argument against it |
+| `scripts/clickup_claim.py` | claim Wave 3: assigns the matching ClickUp task |
+| `templates/scout-report.md` | `scout.md` (both modes) |
+| `templates/accuracy-check-comment.md` | `accuracy-check.md` (claim, posted) |
+| `templates/summary.md` | `summary.md` (claim) |
+| `templates/recommend-record.md` | `recommend.md` (claim) |
+| `templates/next-steps.md` | `next-steps.md` (claim) |
+| `templates/claim-comment.md` | `claim-comment.md` (claim, posted) |
+| `templates/description.md` | `description.md` (create) |
+| `templates/flags-decision.md` | `flags.md`, `flags-user.md`, `flags-t1.md` (create) |
+| `templates/issue-feature-simple.md` | `issue-body.md` (create, feature, quick or standard) |
+| `templates/issue-feature-complex.md` | `issue-body.md` (create, feature, deep) |
+| `templates/issue-bug-simple.md` | `issue-body.md` (create, bug, quick or standard) |
+| `templates/issue-bug-complex.md` | `issue-body.md` (create, bug, deep) |
+| `templates/draft-notes.md` | `draft-notes.md` (create) |
+| `templates/create-review-comment.md` | `create-review.md` (create, posted when needed) |
+
+Every output file starts as a copy of its template (stub first) and is filled in place. `clickup.json` has no template: it is the script's machine output (default D15).
+
+## Workers and the spawn rule
+
+Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.
+
+| Agent | Picker ID (frontmatter `model:`) | Installed file |
+|---|---|---|
+| `issue-worker-t3` | `claude-gw-tier3` | `~/.claude/agents/issue-worker-t3.md` |
+| `issue-worker-t2` | `claude-gw-tier2` | `~/.claude/agents/issue-worker-t2.md` |
+| `issue-worker-t1` | `claude-gw-tier1a` | `~/.claude/agents/issue-worker-t1.md` |
+
+Claude Code reads the project `.claude/agents/` copy first when one exists. The Agent call's `model` parameter takes aliases only and overrides the frontmatter, so passing it would lose the pin (`refs/tiers.md`). A spawn that fails because the picker ID is not served is STOP `E-TIER-UNAVAILABLE`; there is no alias fallback.
+
+Workers make read-only GitHub and git calls, write only under `.dev/issues/`, run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` when their job needs a codebase pass, and return only the paths they wrote. Read each returned file from disk. A worker that returns no file or an empty one is retried once, then STOP `E-WORKER-NO-OUTPUT` with the expected path.
+
+## Repository and GitHub call rules
+
+- `<R>` is the `origin` repo, printed by `uv run --no-project python "<skill base>/scripts/origin_repo.py"`. Nothing else is consulted: not `gh repo set-default`, not gh's fork-parent default, not a `--repo` flag (B10). There is no `--repo` option on the command.
+- Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder.
+- The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` and `scripts/clickup_claim.py`. Workers never write to either.
+- `git fetch origin` is the only fetch; no other remote is added or fetched.
+- Posts go up directly (B1); the full body or comment is never shown for approval. The only user prompt is the create-mode contradiction question (`refs/create.md`, default D14).
+- `.dev/issues/` is never staged or committed by this skill (default D24).
+- `CLICKUP_API_TOKEN` is never printed, echoed or inlined.
+
+## Claim mode
+
+Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
+
+1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py" --claim "<argument>"` resolves `<R>` and `<N>`: exit 1 STOP `E-NO-ORIGIN`, exit 3 STOP `E-FOREIGN-REPO`, exit 4 STOP `E-NOT-AN-ISSUE`. Then `gh auth status` (else STOP `E-GH-AUTH`), the default branch, and create `<D>`.
+2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13); it writes `<D>/scout.md` from `templates/scout-report.md`.
+3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
+4. **Wave 3, assign.** `gh issue edit <N> --repo <R> --add-assignee @me` (failure STOP `E-ASSIGN-FAILED`, before ClickUp and any comment), then `scripts/clickup_claim.py` with stdout to `<D>/clickup.json`; every ClickUp outcome except an argument error is non-fatal.
+5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/summary.md` (effort in hours) and, when out of date, `<D>/analysis/`.
+6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line.
+7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Print the `next-steps.md` path and STOP. Never run a next-step command (B2).
+
+## Create mode
+
+Load `refs/create.md` now. `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then `.dev/issues/<N>/` (default D10).
+
+1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py"` resolves `<R>` (STOP `E-NO-ORIGIN`); `gh auth status` (else STOP `E-GH-AUTH`); create `<D>`; write `<D>/description.md` from `templates/description.md`.
+2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13): repo labels and possible duplicates into `<D>/scout.md`.
+3. **Wave 2, settle the flags** by the depth table of `refs/create.md`; complexity follows depth; the result goes to `<D>/flags.md` from `templates/flags-decision.md`. Deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`.
+4. **Wave 3, pick the template**: mode selects feature or bug; `quick`/`standard` select the simple template, `deep` the complex one.
+5. **Wave 4, draft the body** with the depth's worker into `<D>/issue-body.md` and `<D>/draft-notes.md`. Ask one question only when `draft-notes.md` lists new material or a contradiction.
+6. **Wave 5, post.** Load `refs/labels.md`. Apply only the labels of the fixed set that exist in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory and the labels not applied. No ClickUp call (B6).
+
+## Return contract
+
+Print this block last, in both modes, including after a STOP (fields that do not apply are `null`):
+
+```yaml
+status: success | stopped | failed
+mode: claim | create
+issue_number: <N or null>
+issue_url: <url or null>
+dir: <.dev/issues/<N>/ or the draft directory>
+clickup_status: <status field of clickup.json, or null on create>
+labels_applied: [<label>, ...]
+labels_missing: [<label>, ...]
+next_steps_path: <.dev/issues/<N>/next-steps.md, or null on create>
+```
+
+On a STOP, also print the STOP code and its message.
+
+## Error handling
+
+| Scenario | Behavior |
+|---|---|
+| Both or neither of `--claim` / `--create`; bad flag value; empty description; `--depth`, `--mode` or `--type` with `--claim` (`E-CREATE-ONLY-FLAG`) | The command STOPs with usage before Activation |
+| No `origin`, or `origin` is not GitHub | STOP `E-NO-ORIGIN` |
+| Claim URL on another repo | STOP `E-FOREIGN-REPO` |
+| `gh auth status` fails | STOP `E-GH-AUTH` |
+| Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
+| Assigned to someone else | STOP, message names the assignee, no writes |
+| Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
+| Worker spawn fails because the picker ID is not served | STOP `E-TIER-UNAVAILABLE` naming the agent file and picker ID; no alias fallback |
+| Worker returns no file, or an empty one | Retry that worker once; then STOP `E-WORKER-NO-OUTPUT` with the path expected |
+| `gh issue edit <N> --repo <R> --add-assignee @me` fails | STOP `E-ASSIGN-FAILED` before ClickUp and before any comment |
+| ClickUp skipped, not found, ambiguous, already assigned or error | Continue; the claim comment states the outcome |
+| `/sc:recommend` asks a question or finds no route | Record it in `recommend.md`; `next-steps.md` uses the default row from `refs/chains.md` and says so |
+| `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |
+| `gh issue create --repo <R>` fails | STOP `E-CREATE-FAILED`; the draft directory is kept |
+| A label of the fixed set is missing in the repo | Skip it; list it in the final output |
+| codegraph or auggie unavailable for `/sc:analyze` | The worker continues on Grep, Glob and Read and records it in its file |
+
+## Will
+
+- Resolve the repo from `origin` only and pass it explicitly on every GitHub call.
+- Spawn the T3 worker before any lookup of its own, and pin every worker by `subagent_type`.
+- Write every artifact under `.dev/issues/` from its template.
+- Post directly, and edit an earlier marked comment instead of posting a duplicate.
+- Stop a claim after writing `next-steps.md`.
+
+## Will Not
+
+- Run any next-step command, brainstorm, design, plan or implementation.
+- Create a label, a ClickUp task or a GitHub repository setting.
+- Pass the `model` parameter on an Agent call, or fall back to an alias.
+- Touch any repository other than `origin`, or fetch any other remote.
+- Stage or commit `.dev/issues/`, or edit source code.
+- Print the ClickUp token.
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t6-skill-checks.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t6-skill-checks.txt
new file mode 100644
index 00000000..9eba71dc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t6-skill-checks.txt
@@ -0,0 +1,19 @@
+$ SKILL.md checks (uv run python)
+lines by len(text.splitlines()): 153
+frontmatter: ['name: sc:issue-protocol', 'allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion']
+files on disk not named in SKILL.md: []
+paths named in SKILL.md that do not exist: []
+never-pass-model phrase present: True
+E-NO-ORIGIN True
+E-FOREIGN-REPO True
+E-GH-AUTH True
+E-NOT-AN-ISSUE True
+E-TIER-UNAVAILABLE True
+E-WORKER-NO-OUTPUT True
+E-ASSIGN-FAILED True
+E-POST-FAILED True
+E-CREATE-FAILED True
+D26 line present: True
+gh mentions missing --repo: [] brace placeholder: False
+$ grep -n 'src/superclaude' src/superclaude/skills/sc-issue-protocol/SKILL.md
+exit=1 (grep exit 1 = no match)

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
