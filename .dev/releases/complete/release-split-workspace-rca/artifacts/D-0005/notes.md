# D-0005 -- Notes: target choice + design decisions

## Target choice: `lint-architecture` (not `verify-sync`)

Per Section 4.9 tie-breaker rule 4 (reversible / changes fewest existing
interfaces):

- `verify-sync` is the **sync-verification** interface: it compares
  `src/superclaude/` against `.claude/` for distributability. Adding an
  architectural-rule check there would couple two concerns.
- `lint-architecture` is the **architectural-rules** interface: it
  already enforces command↔skill pairing, size limits, frontmatter
  completeness, and naming conventions. The `*-workspace` blocklist is
  another architectural rule and slots in naturally.

Adding to `lint-architecture` mutates one interface; adding to
`verify-sync` would mutate two (the sync-verification recipe gains an
architectural concern, and CI wiring would need to handle a recipe whose
scope is no longer "sync"). Rule 4 selects `lint-architecture`.

## Non-duplication with T02.01

T02.01's branch in `verify-sync` fires only when the entry has no
`SKILL.md`. T02.02's Check 10 in `lint-architecture` fires whenever a
directory matches `*-workspace`, regardless of `SKILL.md` presence.

The two are complementary:

| Scenario | T02.01 (`verify-sync`) | T02.02 (`lint-architecture` Check 10) |
|---|---|---|
| `_probe-workspace/` without `SKILL.md` | ✅ fires (missing SKILL.md branch) | ✅ fires (suffix branch) |
| `_probe-workspace/` with `SKILL.md` | original "MISSING in src/" message | ✅ fires (suffix branch) |
| `_probe/` without `SKILL.md` | ✅ fires (missing SKILL.md branch) | does not fire |
| `_probe/` with `SKILL.md` | original "MISSING in src/" message | does not fire |

Together, every `*-workspace` directory is rejected by at least one
target — and the suffix-suffixed case with a (legitimate-looking)
`SKILL.md` is now rejected by Check 10 where previously it would have
passed verify-sync.

## Backtick handling in the recipe

The literal message contains backticks. In a Makefile recipe expanded
by `/bin/sh`, double-quoted backticks are command substitution. Two
options:

1. Use single quotes (breaks `$$name` interpolation).
2. Escape backticks with `\``.

Option 2 was chosen so `$$name` continues to interpolate. The runtime
output retains the backticks verbatim, as required by FR-L2.3.

## Pre-existing errors are unrelated

A clean-tree run of `make lint-architecture` returns exit 2 because of
three pre-existing errors (Check 1 `tdd.md` lacks paired skill;
Check 4 `spec-panel.md` exceeds 500 lines; Check 6 `task.md` missing
`## Activation`). These pre-date T02.02 and are outside this task's
scope. Check 10 itself produces zero errors on a clean tree (see
`evidence.md` Probe B).
