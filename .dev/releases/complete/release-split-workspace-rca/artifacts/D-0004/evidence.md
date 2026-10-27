# D-0004 -- Evidence: verify-sync probe outputs

Captured 2026-05-13 against `Makefile` after the T02.01 edit landed.

## Probe A — workspace branch (no SKILL.md)

**Setup:**
```
mkdir -p .claude/skills/_probe-workspace
```

**Command:** `make verify-sync`

**Filtered output (workspace + summary lines):**
```
  ❌ _probe-workspace has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/_probe-workspace/.
❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
```

**Exit code:** `2` (non-zero — `make` prints `Error 1`; the shell observes `2` because of the trailing `make: *** [Makefile:156: verify-sync] Error 1`).

**Acceptance check:**
- ✅ Verbatim message matches FR-L2.1 (em-dash U+2014 preserved).
- ✅ Exit status non-zero.

## Probe B — legitimate-skill branch (with SKILL.md)

**Setup:**
```
mkdir -p .claude/skills/_probe
printf -- '---\nname: _probe\ndescription: test\n---\n# probe\n' > .claude/skills/_probe/SKILL.md
```

**Command:** `make verify-sync`

**Filtered output (probe + summary lines):**
```
  ❌ MISSING in src/superclaude/skills/: _probe (not distributable!)
❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
```

**Exit code:** `2` (non-zero).

**Acceptance check:**
- ✅ Original "MISSING in src/superclaude/skills/" message preserved (no regression on the legitimate drift case).
- ✅ Exit status non-zero.

## Probe C — clean tree (no probes)

**Setup:** all probe directories removed.

**Command:** `make verify-sync`

**Filtered output:**
```
✅ All components in sync.
```

**Exit code:** `0`.

**Acceptance check:**
- ✅ No false positives on a clean tree.

## Summary table

| Probe | SKILL.md present? | Emitted message | Exit |
|---|---|---|---|
| A `_probe-workspace` | No | `_probe-workspace has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/_probe-workspace/.` | non-zero |
| B `_probe` | Yes | `MISSING in src/superclaude/skills/: _probe (not distributable!)` | non-zero |
| C clean | n/a | `All components in sync.` | 0 |

All three acceptance criteria from `phase-2-tasklist.md` T02.01 satisfied.
