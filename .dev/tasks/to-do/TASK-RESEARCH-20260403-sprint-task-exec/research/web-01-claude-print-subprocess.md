# Web Research: Claude `--print -p` Subprocess Behavior

**Topic**: What does `claude --print -p` actually do? What context does a headless Claude subprocess inherit?
**Date**: 2026-04-03
**Status**: In Progress
**Researcher**: Claude Opus 4.6 (1M context)

## Research Questions

1. What does `--print` mode do vs interactive mode?
2. Does `--print` mode load CLAUDE.md automatically?
3. Does it load skills from `.claude/skills/`?
4. Does it respect `settings.json`?
5. How does `--no-session-persistence` affect behavior?
6. What is the difference between `--print` and `--bare`?
7. What context does a headless claude subprocess have access to?

## Codebase Context

The sprint executor spawns:
```
claude --print -p '<prompt>' --tools default --no-session-persistence
```

Codebase analysis (research file 03) concluded that since `--bare` is NOT passed, full auto-discovery runs -- CLAUDE.md loads, skills resolve, settings apply. But this needs external confirmation.

---

## Findings

*(Appending as research progresses...)*

