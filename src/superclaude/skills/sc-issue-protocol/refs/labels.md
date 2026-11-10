# Labels, issue type and fields

Loaded in create Wave 5.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout).)

`--create` classifies the new issue in three ways: a mode label, a GitHub issue type and the Complexity issue field of the organization. These are the only classifications `/sc:issue` ever sets (B7). It never creates a label, an issue type or an issue field. `--claim` changes no label, type or field.

## Mode label

| Mode | Label |
|---|---|
| feature | `enhancement` |
| bug | `bug` |

## Issue type

The wanted issue type follows the mode and the area (`--type`):

| Mode | Area (`--type`) | Issue type |
|---|---|---|
| bug | any | Bug |
| feature | tests | Test |
| feature | any other area | Feature |

Task is never chosen. A bug in tests stays Bug, because the mode already says what the issue is. The area is recorded in `flags.md` and decides nothing else.

## Complexity field

Complexity follows depth. The value is the option name of the Complexity field of the organization, matched without regard to case:

| Depth | Value |
|---|---|
| quick | Simple |
| standard | Medium |
| deep | Complex |

## At run time

1. Labels: the wanted label is the mode label. Intersect it with the repo labels that `scout.md` lists (create Wave 1 read them with `gh label list --repo <R> --limit 200 --json name`). Pass it as one `--label "<name>"` to `gh issue create --repo <R>`. List it as `not applied: label missing in repo: <name>` when the repo has no such label. Never create it.
2. Issue type. When the wanted type is listed under `### Repo issue types` in `scout.md`, pass `--type "<name>"` to `gh issue create --repo <R>`. Otherwise omit the flag and remember `not set: issue type <name>: type missing in repo`, or `lookup failed` when the lookup recorded in `scout.md` failed.
3. After `gh issue create --repo <R>` succeeds and the draft directory is renamed to `.dev/issues/<N>/`, read the type back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. When `--type` was passed and the result is empty or differs, remember `not set: issue type <name>: not applied after create` (GitHub drops the type silently when the caller lacks push access).
4. Complexity field: when `### Complexity field` in `scout.md` lists the field and an option equal to the wanted value, write `.dev/issues/<N>/complexity-field.json` with the body `{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`. A POST adds a value; a PUT would replace every existing value, so it is not used. A non-zero exit remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After a success, read the values back with `gh api repos/<R>/issues/<N>/issue-field-values`; when the value is absent, remember `not set: field Complexity <value>: not applied after create`. When `scout.md` has no such field, remember `not set: field Complexity <value>: field not found in org`, or `lookup failed` when the lookup failed; when the field has no option equal to the value, remember `option not found`.
5. A failed type or field never stops the run once the issue exists. Print the issue URL, the directory, every `not applied` line and every `not set` line. Never create a label, a type or a field.

### Field read-back shape

For a single-select field, the read-back's `value` is an option id, not an option name. Locate the row whose `issue_field_id` equals the field id from `scout.md`, then compare `single_select_option.name` with the selected option name (without regard to case). Do not compare the numeric `value` directly with `Simple`, `Medium` or `Complex`. A failed or unparseable read-back does not prove success: report `not set: field Complexity <value>: not applied after create`.

## Output lines

```text
not applied: label missing in repo: <name>
not set: issue type <name>: <type missing in repo | lookup failed | not applied after create>
not set: field Complexity <value>: <field not found in org | option not found | lookup failed | write failed (<error>) | not applied after create>
```

## One-time creation lines for a maintainer (default D16)

A maintainer may run these by hand, once, to add the two mode labels to a repo. The skill never runs them. Replace `<owner/repo>` with the target repo.

```bash
gh label create "bug" --repo <owner/repo>
gh label create "enhancement" --repo <owner/repo>
```

`bug` and `enhancement` are GitHub's default labels and usually exist already. Issue types and issue fields are created by an organization owner in the organization settings, never by this skill.
