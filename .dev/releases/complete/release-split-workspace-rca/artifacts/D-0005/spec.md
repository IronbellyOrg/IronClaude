# D-0005 -- Spec: `*-workspace` blocklist in `lint-architecture`

**Source:** Phase 2 tasklist T02.02; roadmap item R-005; FR-L2.3.

## Requirement

`.claude/skills/<X>-workspace/` directories must be rejected by an
enforcing Makefile target regardless of whether they contain a
`SKILL.md`. The check fires unconditionally on the `-workspace` suffix
and is complementary to T02.01 (which fires only when `SKILL.md` is
absent).

## Verbatim error message (FR-L2.3)

```
Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.
```

Backticks are literal characters in the emitted message; the recipe
escapes them so the shell does not interpret command substitution.

## Insertion site

`Makefile` target `lint-architecture`, added as a new section
"=== Check 10: Workspace Suffix Blocklist ===" between Check 9 and the
NEEDS DESIGN placeholder block. Errors increment the existing `errors`
accumulator so the Summary block fails the target with exit non-zero.

## Acceptance behaviour

- `*-workspace/` directory under `.claude/skills/` → emit verbatim
  message, exit non-zero.
- No `*-workspace/` directories → emit `✅ [Check 10]: no *-workspace
  directories under .claude/skills/`, contribute zero errors.
