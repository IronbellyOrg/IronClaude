# D-0011 — Spec: Source-to-dev sync and release verification for B-12

| Field | Value |
|---|---|
| Deliverable ID | D-0011 |
| Task | T05.01 |
| Roadmap Item | R-011 |
| Drift Item | B-12 |
| Tier | STANDARD |
| Generated | 2026-05-26 |

## What B-12 requires

`release-scope.md:181-194` (B-12 entry) plus `release-scope.md:198-205` (acceptance criteria 2–4) define the closeout work:

1. After source edits land in `src/superclaude/commands/` and `src/superclaude/skills/sc-roadmap-protocol/refs/` (B-1 through B-8) and in `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` (B-9), the three locations carrying copies of `roadmap.md` and `validate-roadmap.md` must be re-synced:
   - `src/superclaude/commands/` (source of truth)
   - `.claude/commands/sc/` (repo-local dev mirror)
   - `/config/.claude/commands/sc/` (global install)
2. `make verify-sync` must pass (release acceptance criterion 3).
3. A slash-command regression must confirm `/sc:roadmap` and `/sc:validate-roadmap` still execute end-to-end against a sample spec (release acceptance criterion 4).

## Decision

Run the mechanical sync sequence prescribed by `release-scope.md:193` ("Run `make sync-dev` (re-syncs `.claude/`) and a separate manual copy to `/config/.claude/` after merging B-1, B-2") and record three-way md5sum parity plus pytest-backed regression evidence in `evidence.md`.

## Deliverable shape

- `spec.md` (this file) — task framing.
- `notes.md` — scope clarifications and what is and is not authorized.
- `evidence.md` — the actual command outputs, md5sums, verify-sync result, and regression test results that satisfy the acceptance criteria.

## What is NOT in scope

- Editing `src/superclaude/` sources. By the time T05.01 runs, every B-1…B-10 source change has already been committed by T01.01–T04.01.
- Touching `.claude/` directly. Per CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents", `.claude/skills,commands,agents,hooks,templates/*` is gitignored sync-dev output; only `.claude/settings.json` is tracked. T05.01 generates `.claude/` only via `make sync-dev`, never via direct edit, and does not stage any `.claude/` paths.
- Touching `/config/.claude/`. This is the global install location, outside the repo. T05.01 refreshes it via mechanical `cp` from `src/superclaude/commands/`, which is the practice spelled out in `release-scope.md:193`.
- B-11 (global-install gap). `verification.md:193-205` REFUTED B-11 — both skills are already globally installed and byte-identical to `src/`. Phase 5 carries no B-11 workstream.

## Acceptance check at task close

- [x] `make sync-dev` ran successfully (T05.01 step 3).
- [x] Global command copies refreshed at `/config/.claude/commands/sc/` (T05.01 step 4).
- [x] `make verify-sync` exited 0 (T05.01 step 5, release acceptance criterion 3).
- [x] md5sum three-way parity recorded for `roadmap.md` and `validate-roadmap.md` (T05.01 step 5).
- [x] Regression check executed `/sc:roadmap` and `/sc:validate-roadmap` CLI entry points against fixtures (T05.01 step 5, release acceptance criterion 4).
- [x] `evidence.md` records all six outcomes with verbatim command output (T05.01 step 6).
