# D-0004 -- Spec: Context-aware verify-sync error message

**Task:** T02.01 (phase-2-tasklist.md)
**Roadmap Item:** R-004
**Source FR:** FR-L2.1

## Goal

The `make verify-sync` target previously emitted a single, misleading message for any directory present under `.claude/skills/<name>/` but absent from `src/superclaude/skills/<name>/`:

```
❌ MISSING in src/superclaude/skills/: <name> (not distributable!)
```

This is correct for legitimate skill drift but actively misleading for the workspace-misplacement case (a non-skill working directory accidentally placed under `.claude/skills/`): it tells the author to add the directory to `src/superclaude/skills/`, which would propagate the architectural error rather than fix it.

## Behaviour

`verify-sync` now branches on the presence of `SKILL.md` (or `skill.md`) in the offending `.claude/skills/<name>/` directory:

| Condition | Emitted message |
|---|---|
| `SKILL.md` (or `skill.md`) **absent** | `❌ <name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/.` |
| `SKILL.md` (or `skill.md`) **present** | `❌ MISSING in src/superclaude/skills/: <name> (not distributable!)` (unchanged) |

Both branches set `drift=1`, so the target still exits non-zero in either case.

## Out of Scope

- Wildcard-suffix detection (e.g. `*-workspace/`) — handled by T02.02 via a dedicated `lint-architecture` rule, fires unconditionally regardless of `SKILL.md` presence.
- CI wiring — handled by T02.03.

## References

- `Makefile` verify-sync target (anchor: the `.claude/skills/*/` reverse-loop).
- `.dev/README.md` (created by T01.01) for the `.dev/eval-workspaces/` convention cited in the new message.
