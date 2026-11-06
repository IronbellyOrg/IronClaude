# Reviewer 2 brief (persona: qa, model class: haiku, mode: UC-1 pre-execution)

## T1 card excerpt

From `.dev/reflect/pre-addOneSentenceTo-20261105204136/artifacts/tier1-card.md` (coverage section):

> Pass 1 (labeled IDs): 0 parsed rows. The spec is one unlabeled sentence.
> Pass 2 (inference): 1 row. INF-001, quote "Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude", citation source.md:1, match Task 1.
> `parsed_count = 0`, `inferred_count = 1` -> `coverage_degraded: parsed-sparse`. `coverage_pct_union` = 1.0.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T20:41Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/p1-live-workflow projectPath=/home/coder/workspaces/worktrees/IronClaude/p1-live-workflow

### .dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/source.md:1

```text
Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude
```

### .dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md:17-30

```markdown
## Constraints

- Only README.md changes; add exactly one sentence and edit no other sentence, section or file.
- The sentence goes inside the `## Installation` section (README.md), not in Quick start or later sections.

## Phase 1: Document the --force behavior

## Task 1: Add the --force overwrite sentence to the README Installation section

In README.md, under `## Installation` > `### Install the current package/CLI`, add one sentence at the end of the paragraph that starts "This installs the package, then framework assets". The sentence says that `superclaude install --force` overwrites files that already exist in `~/.claude`. Use backticks around the command and the path, as the surrounding text does. Do not touch the `### Upgrading to 5.0.0` paragraph, which already mentions `--force` separately.

Acceptance criteria:
- README.md contains one new sentence in the `## Installation` section that names `superclaude install --force` and `~/.claude` and says it overwrites files that already exist there.
- `git diff -- README.md` shows only that sentence added (one changed line, no other hunks), and `git diff --stat` lists no file other than README.md.
```

### README.md:53-64

```markdown
## Installation

### Install the current package/CLI

The package still uses the historical name `superclaude`, but install it from this repository. The `superclaude` package on PyPI (`pipx install superclaude`) is the upstream SuperClaude Framework, not IronClaude.

```bash
pipx install git+https://github.com/IronbellyOrg/IronClaude
superclaude install
```

This installs the package, then framework assets (core files, commands, agents, skills, ccsession wiring, hooks, templates and user setup), followed by the codegraph phase (a pinned, checksum-verified codegraph registered as a user-level MCP server; a failure there exits 1) and a bounded, non-fatal cleanup of old user-level MCP registrations that IronClaude wrote itself. See the [MCP installation guide](docs/user-guide/mcp-installation.md) for details. Installing from the repository URL needs read access to it.
```

### README.md:75

```markdown
Restart Claude sessions afterwards. A plain `superclaude install` keeps framework files that already exist, so use `--force` to refresh them. Do not upgrade with `superclaude update`: it never installs codegraph or retires old MCP registrations. See [Upgrading](docs/getting-started/upgrading.md) for the full steps and the [5.0.0 release notes](docs/releases/v5.0.0.md) for what changed.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 (inferred): add one sentence to README Installation section stating `superclaude install --force` overwrites existing files in ~/.claude | Task 1 | covered | source.md:1; plan Task 1 |
