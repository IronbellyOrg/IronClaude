# D-0015 — Test Specification: AC4 CLAUDE.md Pointer Resolution

**Task:** T05.04 — AC4 test: grep CLAUDE.md pointers resolve to existing files
**Roadmap Item:** R-015
**Phase:** 5 (Acceptance Validation)
**Date:** 2026-05-13

## Purpose

Assert that every documentation pointer remaining in `CLAUDE.md` after
the T01.02 pointer repair resolves to an existing file on disk.
Concretely: a regex grep of the original three doc pointer names
(`PLANNING.md`, `TASK.md`, `KNOWLEDGE.md`) against `CLAUDE.md` must
return only `KNOWLEDGE.md` matches, and `KNOWLEDGE.md` must exist at
the repo root.

This directly exercises SC-004 in the source roadmap.

## Layered defense — pointer hygiene under test

T01.02 removed dangling references to `PLANNING.md` and `TASK.md` from
`CLAUDE.md` because those files do not exist in the IronClaude tree
(they referred to the upstream SuperClaude_Framework convention).
`KNOWLEDGE.md` was retained because the file is present. This test is
the post-state probe: it confirms the cleanup landed and no surviving
pointer is dangling.

## Commands under test

| # | Command | Expected |
|---|---------|----------|
| 1 | `grep -nE 'PLANNING\.md\|TASK\.md\|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md` | Only `KNOWLEDGE.md` lines printed; zero `PLANNING.md` / `TASK.md` matches |
| 2 | `grep -cE 'PLANNING\.md' CLAUDE.md` | `0` |
| 3 | `grep -cE 'TASK\.md' CLAUDE.md` | `0` |
| 4 | `grep -cE 'KNOWLEDGE\.md' CLAUDE.md` | `>= 1` |
| 5 | `test -f KNOWLEDGE.md` | exit `0` |

## Acceptance gate (from phase-5-tasklist.md)

- `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md`
  shows only `KNOWLEDGE.md` matches; zero `PLANNING.md` and zero
  `TASK.md` matches.
- Test FAILS if any unexpected `PLANNING.md` or `TASK.md` match
  appears.
- `test -f KNOWLEDGE.md` exits 0.
- Grep + `test -f` outputs captured in this directory's `evidence.md`.
- Result aligns with SC-004 success criterion in the source roadmap.

## Dependencies

- T01.02 — CLAUDE.md pointer repair must be landed.

## Notes

This is the canonical AC4 acceptance test (LIGHT tier, sanity check).
No rollback path needed; the test is read-only.
