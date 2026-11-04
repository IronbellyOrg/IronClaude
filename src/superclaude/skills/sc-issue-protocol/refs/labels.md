# Label set

Loaded in create Wave 5.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`.)

These are the only labels `/sc:issue` ever applies (B7). It never creates a label. `--claim` changes no labels.

| Group | Labels | Applied by |
|---|---|---|
| Mode | `bug`, `enhancement` | `--create` (`feature` mode gets `enhancement`, `bug` mode gets `bug`) |
| Type | `type: cicd`, `type: command`, `type: skill`, `type: agent`, `type: hook`, `type: cli`, `type: core`, `type: docs`, `type: tests`, `type: install`, `type: other` | `--create` |
| Complexity | `complexity: simple`, `complexity: medium`, `complexity: complex` | `--create` |

## At run time

1. The wanted labels are the mode label, `type: <type>` and `complexity: <simple|medium|complex>`.
2. Intersect them with the repo labels that `scout.md` lists (create Wave 1 read them with `gh label list --repo <R> --limit 200 --json name`).
3. Pass each label that exists as one `--label "<name>"` to `gh issue create --repo <R>`.
4. List every label that does not exist in the final output as `not applied: label missing in repo: <name>`. Never create it.

## One-time creation lines for a maintainer (default D16)

A maintainer may run these by hand, once, to add the labels to a repo. The skill never runs them. Replace `<owner/repo>` with the target repo.

```bash
gh label create "bug" --repo <owner/repo>
gh label create "enhancement" --repo <owner/repo>
gh label create "type: cicd" --repo <owner/repo>
gh label create "type: command" --repo <owner/repo>
gh label create "type: skill" --repo <owner/repo>
gh label create "type: agent" --repo <owner/repo>
gh label create "type: hook" --repo <owner/repo>
gh label create "type: cli" --repo <owner/repo>
gh label create "type: core" --repo <owner/repo>
gh label create "type: docs" --repo <owner/repo>
gh label create "type: tests" --repo <owner/repo>
gh label create "type: install" --repo <owner/repo>
gh label create "type: other" --repo <owner/repo>
gh label create "complexity: simple" --repo <owner/repo>
gh label create "complexity: medium" --repo <owner/repo>
gh label create "complexity: complex" --repo <owner/repo>
```

`bug` and `enhancement` are GitHub's default labels and usually exist already.
