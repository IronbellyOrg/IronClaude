# Create mode (`/sc:issue --create "<description>"`)

Loaded at the start of create mode. `<R>` is the origin repo (`owner/repo`), `<skill base>` the directory that holds this skill's `SKILL.md`. Files are written to `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then the directory is renamed to `.dev/issues/<N>/` (default D10). `<slug>` is built from the first words of the description: lower-case it, replace every run of characters other than `a-z` and `0-9` with one `-`, drop any leading or trailing `-`, cut it to at most 40 characters (dropping a trailing `-` left by the cut), and use `untitled` when nothing is left. The slug therefore holds only `a-z`, `0-9` and `-`: never `/`, `.`, `\`, a space or `..`, so `<D>` always stays directly under `.dev/issues/`.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.

Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md` (Claude Code reads the project `.claude/agents/` copy first when one exists). Load `refs/tiers.md` before the first spawn. A worker that needs a codebase pass runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). Every file under `<D>` starts as a copy of its template under `templates/`.

Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder, with one exception: the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash). No other `orgs/` path is allowed, and the orchestrator and the T1 and T2 workers keep the old rule. Only the orchestrator writes to GitHub: besides `gh issue create --repo <R>` and `gh issue comment <N> --repo <R>`, its only GitHub field write is the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values`). Create mode makes no ClickUp call and no self-assignment (B6).

## Wave 0: prerequisites (orchestrator)

1. `uv run --no-project python "<skill base>/scripts/origin_repo.py"` prints `<R>` from the `origin` remote; a non-zero exit is STOP `E-NO-ORIGIN`.
2. `gh auth status` must succeed; else STOP `E-GH-AUTH`.
3. Check that `<slug>` matches `^[a-z0-9]+(-[a-z0-9]+)*$`; if it does not, rebuild it by the rule above before going on. Create `<D>`.
4. Write the description to `<D>/description.md` from `templates/description.md`. An `@path` description is read from that file.

## Wave 1: lookup (issue-worker-t3, B13)

Spawn `issue-worker-t3` with the job "create lookup", `<R>`, the description's keywords and `<D>`. The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), reads the issue types of the repo (`gh api repos/<R>/issue-types`) and the Complexity field of the organization (`gh api orgs/<owner of R>/issue-fields`, the one allowed `orgs/` path; it records the id, the data type and the option names of the field named `Complexity`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`) and writes `<D>/scout.md` from `templates/scout-report.md` (create section: `### Repo labels`, `### Repo issue types`, `### Complexity field`, `### Possible duplicates`). A lookup that fails is recorded as `lookup failed: <reason>` and never stops the run. Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).

Worker returns no file or an empty one: retry once, then STOP `E-WORKER-NO-OUTPUT` naming the path.

## Wave 2: settle the flags

"All flags given" means both `--mode` and `--type` were passed. When only one was passed, keep it and choose the missing one as in the "a flag missing" column (default D12).

| Depth | All flags given | A flag missing |
|---|---|---|
| quick | Take the user's flags at face value; the orchestrator writes `<D>/flags.md` | `issue-worker-t2` reads `description.md` and `scout.md` and chooses |
| standard | `issue-worker-t2` runs a quick validation of the user's flags; differences become a pushback comment posted after the issue (Wave 5) | `issue-worker-t1` chooses |
| deep | Two variants debated: the orchestrator writes `<D>/flags-user.md` (the user's flags) and `issue-worker-t1` writes `<D>/flags-t1.md` (an independent choice), then `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`; differences become the pushback comment (default D13) | `issue-worker-t1` runs `/sc:analyze` on the code the description touches, then chooses |

Every `issue-worker-t1` spawn in this mode (the Wave 2 flag choices and the Wave 4 deep body) follows the T1 -> T2 fallback of `refs/tiers.md`: when `claude-gw-tier1b` is not served to this user, retry the same job once with `issue-worker-t2`, same inputs and output paths. The retry's spawn prompt tells the T2 worker to put `Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.` in the first lines of `flags.md` (or `flags-t1.md`) for a flag job and of `draft-notes.md` for a body job. Only a T2 fallback that is not served is STOP `E-TIER-UNAVAILABLE`; there is no alias fallback.

Complexity follows depth, as the issue body pairs them (default D17): `quick` = Simple, `standard` = Medium, `deep` = Complex; the value is the option name of the Complexity field.

Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, issue type, complexity, reasons); `flags-user.md` and `flags-t1.md` use the same template. The `Issue type` row is derived by the orchestrator from the mode and the area by the rule of `refs/labels.md` (a bug is Bug, a feature in the area `tests` is Test, any other feature is Feature), after any worker returns. The issue is filed with the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently reclassified), else with the worker's choice.

## Wave 3: pick the template

Mode selects feature or bug; depth selects simple or complex:

| Mode | `quick` or `standard` | `deep` |
|---|---|---|
| feature | `templates/issue-feature-simple.md` | `templates/issue-feature-complex.md` |
| bug | `templates/issue-bug-simple.md` | `templates/issue-bug-complex.md` |

## Wave 4: draft the body

| Depth | Worker | Codebase pass |
|---|---|---|
| quick | `issue-worker-t3` | `/sc:analyze --depth quick` on the touched area |
| standard | `issue-worker-t2` | `/sc:analyze` (no `--depth`) |
| deep | `issue-worker-t1` | `/sc:analyze --depth deep` |

At deep depth the `issue-worker-t1` spawn falls back to `issue-worker-t2` as described in Wave 2. The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts). It lists, in `<D>/draft-notes.md` (from `templates/draft-notes.md`), any new material it added beyond the description and any contradiction between the description and the code.

### Contradiction prompt rule (default D14)

If `draft-notes.md` lists new material or a contradiction, ask the user one question (AskUserQuestion) naming each item, with the choices "keep all", "drop the new material" and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5. If it lists nothing, post the issue without any prompt. The full body is never shown for approval (B1).

## Wave 5: post (orchestrator, directly)

Load `refs/labels.md`.

1. Labels = the mode label only (`enhancement` for feature, `bug` for bug), intersected with the repo labels in `scout.md`. A missing one is listed in the final output, never created (B7). No label for the area or for the complexity is requested.
2. Issue type: the wanted type follows the rule of `refs/labels.md`. When it is listed under `### Repo issue types` in `scout.md`, the create command of step 3 gets `--type "<name>"`; otherwise omit the flag and remember `not set: issue type <name>: type missing in repo` (or `lookup failed`).
3. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label "<label>"` (give `--label` only when step 1 kept the label; omit it when the repo lacks the label; plus `--type "<name>"` when step 2 allows it), with the prefix `[FEATURE] ` or `[BUG] ` (default D21). Failure -> STOP `E-CREATE-FAILED`; the draft directory is kept.
4. Read `<N>` from the issue URL that step 3 prints, then rename `<D>` to `.dev/issues/<N>/`.
5. Type read-back: `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. When `--type` was passed and the result is empty or different, remember `not set: issue type <name>: not applied after create`.
6. Complexity field: when `### Complexity field` in `scout.md` lists the field and an option equal to the wanted value (`quick` = Simple, `standard` = Medium, `deep` = Complex), write `.dev/issues/<N>/complexity-field.json` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` (body and error handling in `refs/labels.md`). A failed POST remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After a success, read the values back with `gh api repos/<R>/issues/<N>/issue-field-values` and remember `not set: field Complexity <value>: not applied after create` when the value is absent. A missing field remembers `not set: field Complexity <value>: field not found in org` (or `lookup failed`).
7. Standard or deep with all flags given and a disagreement in Wave 2: write `.dev/issues/<N>/create-review.md` from `templates/create-review-comment.md` (it ends with `<!-- sc:issue:create-review -->`) and post it with `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md`. Failure -> STOP `E-POST-FAILED`.
8. Print the issue URL, the directory, every `not applied: label missing in repo` line and every `not set` line (formats in `refs/labels.md`). No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).

A failed type or field never stops the run once the issue exists. Only `gh issue create --repo <R>` (`E-CREATE-FAILED`) and the pushback comment (`E-POST-FAILED`) keep their STOP codes.
