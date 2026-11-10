# Design: /sc:issue --create sets the issue type and the Complexity field (#438)

- Command: `/sc:design @.dev/issues/438/issue-summary.md --type component --format spec`
- Component: create mode of `sc:issue-protocol` (Wave 1 lookup, Wave 2 flags, Wave 5 post) and everything that repeats its label behaviour.
- Status: design only. No source file is changed by this document.
- Sources read: `issue-summary.md`, `analysis/analyze-sc-issue-protocol.md`, `refs/labels.md`, `refs/create.md`, `SKILL.md`, `commands/issue.md`, `agents/issue-worker-t3.md`, the three create templates, `tests/skills/test_issue_protocol.py`, and GitHub's REST docs for issue field values and issues.

<!-- PART:decisions -->
## 1. Decisions (each open question from the issue, with a default)

The issue marks five points "Not known yet". Two are now answered from GitHub's REST docs. Three are owner decisions; each has a default the plan uses unless the owner says otherwise.

| # | Question | Answer or default | Basis |
|---|---|---|---|
| Q1 | How to set the issue type | `gh issue create --repo <R> --type <name>` at creation. The wanted name is checked first against `gh api repos/<R>/issue-types`. After creation it is read back with `gh issue view <N> --repo <R> --json issueType`. | gh 2.103.3 help (from the issue summary); the REST docs say the type is silently dropped when the caller lacks push access, so the read-back is required. |
| Q2 | How to set the Complexity field | A separate call after `gh issue create`: `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <D>/complexity-field.json`, body `{"issue_field_values":[{"field_id":<id>,"value":"<Simple\|Medium\|Complex>"}]}`. For a single-select field the value is the option name. POST adds a value; PUT would replace all values, so POST is used. Read back with `gh api repos/<R>/issues/<N>/issue-field-values`. | GitHub Docs, "REST API endpoints for issue field values" (verified in this session). No gh flag exists. |
| Q3 | Permission | Push access to the repo. A 403 means no permission. The current user has admin on the repo, so the happy path is expected to work. The write itself was not run (read-only design). | Same docs page. |
| Q4 | Field id lookup breaks the `repos/<R>/` path rule | **Default: allow exactly one extra read path.** The T3 lookup worker may run `gh api orgs/<owner of R>/issue-fields` (GET only, `<owner>` is the part of `<R>` before the slash, never typed from user input) and look up the field named `Complexity`. No other `orgs/` path is allowed, and the orchestrator and the T1/T2 workers keep the old rule. A test pins the exception. The field id and option names are never hard-coded. | `repos/<R>/issue-fields` returns 404, so no repo-scoped lookup exists. |
| Q5 | Area values (`--type`, 11 values) have no org counterpart | **Default: keep the `--type` flag and its 11 values, stop turning them into `type:` labels.** The area is recorded in `flags.md` and in the pushback comment, and it decides one thing: area `tests` on a feature gives issue type Test. Nothing else reads it. | Owner may instead drop the flag or move the area into the body. Changing the templates is out of scope here. |
| Q6 | Mode labels `bug` / `enhancement` | **Default: keep them.** They exist in the repo, apply today and cost nothing; `labels_applied` / `labels_missing` stay for them. The skill still never creates a label. | Owner may drop them later; that is a one-line change in `labels.md`. |
| Q7 | Which issue type for which input | Mode `bug` gives Bug. Mode `feature` with area `tests` gives Test. Every other feature gives Feature. Task is never chosen. | Issue text: "feature to Feature, bug to Bug, tests to Test where it fits". A bug in tests stays Bug because mode already says what the issue is. |
| Q8 | Complexity value | Follows depth as today: quick = Simple, standard = Medium, deep = Complex, matched to the field's option names without case sensitivity. | `refs/create.md` Wave 2; the three options match one to one. |
| Q9 | `--claim` | Unchanged. It writes a complexity word into its comment but sets no field. The issue scopes `--create` only. | Analysis finding F10. |

<!-- PART:spec -->
## 2. Specification

### 2.1 Flow of create mode after the change

| Wave | Who | What changes |
|---|---|---|
| 1 lookup | `issue-worker-t3` | Besides repo labels and duplicates, it runs `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`, and writes two new sections into `scout.md`: `### Repo issue types` (the names, or `lookup failed: <reason>`) and `### Complexity field` (field id, data type, option names; or `not found` / `lookup failed: <reason>`). A failed lookup is recorded, never fatal. |
| 2 flags | orchestrator or T1/T2 worker | Unchanged flag settling. `flags.md` gets one derived row, `Issue type`, by rule Q7. The `Complexity` row now holds the field option name (Simple, Medium, Complex) instead of a label word. |
| 5 post, step 1 | orchestrator | Labels: the mode label only (`enhancement` or `bug`), intersected with the repo labels in `scout.md`. No `type:` or `complexity:` label is requested any more. |
| 5 post, step 2 | orchestrator | Wanted issue type = rule Q7. If it is listed under `### Repo issue types`, add `--type "<name>"` to `gh issue create --repo <R> ...`. Otherwise omit the flag and remember `not set: issue type <name>: type missing in repo` (or `lookup failed`). |
| 5 post, step 3 | orchestrator | `gh issue create` and the rename of `<D>` to `.dev/issues/<N>/`, as today. Failure is still STOP `E-CREATE-FAILED`. |
| 5 post, new step | orchestrator | Read back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. If `--type` was passed and the result is empty or different, remember `not set: issue type <name>: not applied after create` (covers the silent drop when the caller lacks push access). |
| 5 post, new step | orchestrator | Complexity: if `scout.md` has the field and an option equal to the wanted value, write `.dev/issues/<N>/complexity-field.json` with the body of Q2 and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`. A non-zero exit remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After success, read back with `gh api repos/<R>/issues/<N>/issue-field-values` and remember `not set: field Complexity <value>: not applied after create` if the value is absent. Field missing in the scout: `not set: field Complexity <value>: field not found in org` (or `lookup failed`). |
| 5 post, last | orchestrator | Pushback comment as today, then print the issue URL, the directory, every `not applied: label missing in repo: <name>` line and every `not set: ...` line. |

A failed type or field never stops the run once the issue exists. Only `gh issue create` and the pushback comment keep their STOP codes.

### 2.2 Return contract (create mode)

The first block (shared by both modes) stays key for key. A third YAML block is added after the claim block, so claim output does not change:

```yaml
issue_type: <name of the type read back from the issue, or null>
complexity_field: <option name read back from the issue, or null>
classification_missing: [<each "not set: ..." line without the prefix>, ...]
```

The text says: "Create mode adds these three fields after the claim block (claim mode prints none of them; on a STOP the fields that do not apply are `null`)". `labels_applied` / `labels_missing` now describe the mode label only.

### 2.3 Rule changes that other files depend on

- **gh api path rule** (SKILL.md "Repository and GitHub call rules", `refs/create.md` intro, `agents/issue-worker-t3.md` Rules): "every `gh api` path is `user` or starts with `repos/<R>/`" gains one exception: the T3 worker's read-only `GET orgs/<owner of R>/issue-fields`. T1 and T2 keep the old rule.
- **Orchestrator writes list** (SKILL.md): adds `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and `gh issue create --repo <R> ... --type <name>`. Workers still never write.
- **Will Not**: still never creates a label, and now also never creates an issue type or an issue field, and never writes a field other than Complexity.
- **`refs/labels.md`** keeps its file name (four tests pin the five-ref inventory) and is retitled "Labels, issue type and fields". It lists the two mode labels, the type rule Q7 with its three names, the Complexity mapping Q8, the run-time steps above, and the exact text of every `not set` line. The 11 `type:` labels, the 3 `complexity:` labels and their `gh label create` lines are removed; the two mode label lines stay in the maintainer block.

### 2.4 Exact output lines

```text
not applied: label missing in repo: <name>
not set: issue type <name>: <type missing in repo | lookup failed | not applied after create>
not set: field Complexity <value>: <field not found in org | option not found | lookup failed | write failed (<error>) | not applied after create>
```

### 2.5 Failure cases covered

| Case | Result |
|---|---|
| Repo has no issue type of that name | No `--type`; `not set` line; issue still created |
| `issue-types` lookup fails | Same, reason `lookup failed` |
| Caller lacks push access (type silently dropped) | Caught by the read-back; `not set` line |
| Org has no Complexity field, or the repo belongs to a user (no fields) | `not set` line, reason `field not found in org` |
| Field option names changed | `option not found` |
| POST returns 403, 404, 422 or 503 | `write failed (...)`; issue stays |
| Draft directory already renamed when the field step fails | Body file is written under `.dev/issues/<N>/`, so no path is lost |
| `gh issue create` itself fails | STOP `E-CREATE-FAILED`, draft kept, as today |

<!-- PART:changes -->
## 3. Change surface and tests

Edit `src/superclaude/` only, then run `make sync-dev`. Never stage `.claude/` paths. Line numbers are from the issue analysis on `1aa2e5c3` and must be re-read before each edit.

### 3.1 Files

| File | Change |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/refs/labels.md` | Rewrite as in 2.3 (keep the file name). |
| `src/superclaude/skills/sc-issue-protocol/refs/create.md` | Intro path rule (`:9`); Wave 1 (`:18-22`) adds the two lookups; Wave 2 (`:34-36`) adds the derived type row and the field option names; Wave 5 (`:61-69`) per 2.1. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | Description (`:3`), create summary (`:18`), files table (`:31`), path rule and writes list (`:73-74`), create steps (`:99-103`), return contract (`:105-119`, third block), error row (`:161`), Will Not (`:172-177`). |
| `src/superclaude/commands/issue.md` | Description (`:4`), create bullet (`:17`), `--mode` and `--type` rows (`:41-42`), Will (`:89`) and Will Not (`:93`). |
| `src/superclaude/agents/issue-worker-t3.md` | Create lookup job (`:22`) and the read-only rule (`:27`) per 2.3. |
| `templates/scout-report.md` | Create section (`:42-44`): add `### Repo issue types` and `### Complexity field`. |
| `templates/flags-decision.md` | Add the `Issue type` row; `Complexity` row values become Simple / Medium / Complex. |
| `templates/create-review-comment.md` | "was not relabelled" becomes "was not reclassified" (`:3`). |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md`, `docs/designs/sc-issue-command.md` | Replace every statement that `type:` and `complexity:` labels are applied (analysis F9 lists the lines). Do not rewrite history sections beyond the wording. |
| `src/superclaude/core/HOW-WE-WORK.md:329` | "labels from a fixed set" becomes "an issue type, the Complexity field and a mode label". Then copy byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and re-run the level-table copy into `src/superclaude/core/CLAUDE.md` (project rule; tests check both). |

Not changed: `--claim` code and text, `scripts/*.py`, the four issue body templates, the T1 and T2 worker files, `refs/tiers.md`.

### 3.2 Tests (`tests/skills/test_issue_protocol.py`)

Existing tests to update: `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` (three blocks, new key list, new sentence), the Will / Will Not match test against the command file (re-read it before editing; it compares the two lists), and any test that asserts the old label wording.

New tests, each of which must fail if the behaviour breaks:

1. `labels.md` names no `type:` or `complexity:` label and no `gh label create` line for them.
2. Every `orgs/` path found in the skill files and the agents equals `orgs/<owner>/issue-fields`, and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`.
3. The skill writes the field with `-X POST` and `issue-field-values`, and no file contains `-X PUT`.
4. `create.md` and `labels.md` carry the three exact `not set` / `not applied` line formats.
5. `issue-worker-t3.md` lists `issue-types` and `issue-fields` in its create lookup, and the scout template has the two new headings.
6. Rule Q7 and Q8 are stated (Feature, Bug, Test; Simple, Medium, Complex) in `labels.md`.
7. The existing fork-safety scans still pass, so every new `gh issue ...` line carries `--repo <R>` and no file holds a brace placeholder.

Run: `uv run pytest tests/skills/test_issue_protocol.py -v`, then `make verify-sync`, then `make lint`.

### 3.3 Order of work

1. `labels.md`, `create.md`, `SKILL.md` (the rules), then the scout and flags templates and the T3 worker.
2. Command file and the review-comment wording.
3. Tests, run until green.
4. Docs and the `HOW-WE-WORK.md` mirror, then `make sync-dev` and `make verify-sync`.

### 3.4 Risks and what is not verified

- **UNVERIFIED:** nothing in this design wrote to GitHub. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and gh help, not from a run. The plan must end with one manual check by the owner: file a test issue with `/sc:issue --create` and confirm the type and Complexity show on it.
- Org-level `issue-fields` visibility is "organization members only" for Complexity; a caller outside the org gets a `not set` line, not a failure.
- GitHub's field API is versioned (`X-GitHub-Api-Version: 2026-03-10` in the docs). If gh sends an older default version and the endpoint answers 404, the result is a `not set` line, which is the intended safe failure.
- Owner decisions Q4, Q5 and Q6 change only wording and one test each if reversed.
