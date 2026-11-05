# Reviewer 3 brief: persona refactorer, model opus (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md` (Read it in full) against its spec `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/source.md` and the design `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md` (Design 3.1, 3.2, NFR-003). Lens: structure, smallest correct diff, scope discipline and task boundaries. Assume mistakes exist. Check: is the change confined to data plus one shared-path fix; does any task invite scope creep (new code, new keys, edits to forbidden files, `.claude/` staging); are task boundaries and dependencies sound and each task independently reviewable; does the Python fix as described converge every failure path in one place; does anything in the plan contradict the project rules in `CLAUDE.md` (never stage `.claude/`, `.dev/tasks` always staged, no `src/superclaude/` paths in installed primitives, UV only)? Grade each finding blocking or minor (blocking = wrong behaviour, false claim, missing required deliverable, or a security/data-loss risk).

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-3
    kind: acceptance-ambiguity
    claim: "Task 2's 'at most 5 changed lines' is ambiguous: the design's shape adds one line and changes three (git counts 4 insertions plus 3 deletions)."
  - id: F-5
    kind: cohesion
    claim: "The manual install proof (AC-M1..M3) sits in Task 4, the CHANGELOG task; M1b/M1c need a Claude session in a throwaway HOME, which likely has no credentials, so they will probably be UNVERIFIED."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T12:45:03Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin

### src/superclaude/cli/install_user_setup.py:288-311

The failure-label loop the plan's Task 2 fixes. Read it.

### src/superclaude/cli/user_settings_defaults.json:10-13, 28-49

`env` (two keys), `enabledPlugins` (six), `extraKnownMarketplaces` (two). Read it.

### docs/getting-started/installation.md:353-366

The default-plugin paragraph ("six plugins, including ...") and the `CLAUDE_CONFIG_DIR` note the plan inserts before. Read it.

### CHANGELOG.md:1-20

Empty `[Unreleased]` and the `### topic` / `#### Changed (...)` heading style. Read it.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-010 three defaults entries | Task 1 | covered | source.md:1 |
| INF-011 failure-label fix at most 5 lines | Task 2 | covered | source.md:1 |
| INF-014 no change to main.py, update.sh, doctor.py, output styles, primitives, .claude/ | none (Constraints) | unmapped by containment | source.md:1 |
| INF-017 superseded package untouched | none (Constraints) | unmapped by containment | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, verdict, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
