# D-0010 — Skill-Level Output-Path Policy Guard Spec

**Task:** T04.01
**Roadmap Item:** R-010 (sourced from FR-L3.1)
**Deliverables:**
- A refusal clause in `src/superclaude/skills/sc-release-split-protocol/SKILL.md` Prerequisites step 2a.
- A documented policy entry in `src/superclaude/commands/release-split.md` Options table.
- `.claude/skills/sc-release-split-protocol/` in sync via `make sync-dev`.

## Policy

The `sc-release-split-protocol` skill MUST refuse `--output` paths under any of three forbidden prefixes BEFORE any artifact is written:

| # | Forbidden prefix | Reason |
|---|------------------|--------|
| 1 | `.claude/skills/` | Reserved for distributable skill packages |
| 2 | `.claude/agents/` | Reserved for distributable agent definitions |
| 3 | `.claude/commands/` | Reserved for distributable slash command files |

**Redirect destination:** `.dev/` — specifically `.dev/releases/current/<release-name>/` for release-split artifacts, or `.dev/eval-workspaces/<skill-name>/` for skill iteration workspaces. Canonical convention documented in `.dev/README.md`.

## Behaviour

1. **Pre-write enforcement:** The guard runs in Prerequisites step 2a, BEFORE Part 1 (Discovery & Proposal) begins and BEFORE any file is created in the output directory.
2. **Prefix matching:** The check matches absolute, relative, and repo-rooted forms of the three forbidden prefixes.
3. **Refusal message:** Names all three forbidden prefixes AND the redirect destination (`.dev/`), with concrete example destinations and a pointer to `.dev/README.md`.
4. **Documentation:** The Options table in `src/superclaude/commands/release-split.md` documents the same policy on the `--output` row.

## Acceptance Criteria (mirrored from phase-4-tasklist T04.01)

- `src/superclaude/skills/sc-release-split-protocol/SKILL.md` Prerequisites step 2a refuses `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`.
- `src/superclaude/commands/release-split.md` Options table contains the policy entry naming all three forbidden prefixes.
- Invoking `sc-release-split-protocol --output .claude/skills/foo/` aborts BEFORE writing any artifact and emits an error mentioning `.dev/`.
- `make verify-sync` exits 0 after `make sync-dev`.

## Files Touched

- `src/superclaude/skills/sc-release-split-protocol/SKILL.md` — added Prerequisites step 2a and a new row in the Error Handling table.
- `src/superclaude/commands/release-split.md` — extended the `--output` row of the Options table with the policy clause.
- `.claude/skills/sc-release-split-protocol/SKILL.md` — propagated via `make sync-dev` (mirror of `src/`).
- `.claude/commands/release-split.md` — propagated via `make sync-dev`.

## Out of Scope

- Sibling skills (`sc-adversarial-protocol`, `sc-cleanup-audit-protocol`) — handled by optional task T04.02.
- L1 hook layer (`reject-workspace-writes.sh`) — handled in Phase 1 / M1.
- L2 CI gate (`make verify-sync` messaging) — handled in Phase 2 / M2.
