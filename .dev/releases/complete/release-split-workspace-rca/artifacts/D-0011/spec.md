# D-0011 — Output-Path Policy Guard for Sibling Skills

**Task:** T04.02 (optional — defer-pending-capacity)
**Roadmap Item:** R-011 (sourced from FR-L3.2)
**Deliverables:**
- A refusal clause applied to `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` Prerequisites.
- An exemption notice for `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` (documented in `notes.md`).
- `.claude/skills/` propagation via `make sync-dev`.

## Scope

Generalize the T04.01 output-path policy guard to sibling skills that also accept an `--output` argument.

| Sibling skill | Accepts `--output`? | Guard applied? | Notes |
|---------------|---------------------|----------------|-------|
| `sc-adversarial-protocol` | Yes (Configurable Parameters table) | Yes — added Prerequisites section + Error Handling row | Same clause as T04.01 |
| `sc-cleanup-audit-protocol` | No — output is hardcoded to `.claude-audit/` | No (exempt) | See `notes.md` for rationale |

## Policy (mirror of T04.01)

The applicable sibling skill MUST refuse `--output` paths under any of three forbidden prefixes BEFORE any artifact is written:

| # | Forbidden prefix | Reason |
|---|------------------|--------|
| 1 | `.claude/skills/` | Reserved for distributable skill packages |
| 2 | `.claude/agents/` | Reserved for distributable agent definitions |
| 3 | `.claude/commands/` | Reserved for distributable slash command files |

**Redirect destination:** `.dev/` — specifically `.dev/eval-workspaces/<skill-name>/` for skill iteration workspaces, or `.dev/releases/current/<release-name>/` for release artifacts. Canonical convention documented in `.dev/README.md`.

## Behaviour

1. **Pre-write enforcement:** The guard runs in the skill's new "Prerequisites (before Step 1)" section, BEFORE Step 1 (Diff Analysis) begins and BEFORE any file is created in the output directory.
2. **Prefix matching:** The check matches absolute, relative, and repo-rooted forms of the three forbidden prefixes.
3. **Refusal message:** Names all three forbidden prefixes AND the redirect destination (`.dev/`), with concrete example destinations and a pointer to `.dev/README.md`.
4. **Error Handling Matrix:** An `output_path_forbidden` entry was added at the top of `error_handling:` mirroring the T04.01 row in `sc-release-split-protocol/SKILL.md`.

## Acceptance Criteria (mirrored from phase-4-tasklist T04.02)

- Both sibling SKILL.md files either contain the refusal clause OR `notes.md` documents the exemption rationale.
- Invocation of each in-scope sibling skill with a forbidden `--output` would abort pre-write (verified at protocol-text level — these skills are markdown protocol documents, not Python CLI entrypoints).
- `make verify-sync` exits 0 after `make sync-dev`.
- All evidence captured in `evidence.md`.

## Files Touched

- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` — added Prerequisites section (after Required Input, before Triggers) and a new `output_path_forbidden` entry in the Error Handling Matrix.
- `.claude/skills/sc-adversarial-protocol/SKILL.md` — propagated via `make sync-dev` (mirror of `src/`).
- `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` — NOT MODIFIED (exempt; see `notes.md`).

## Out of Scope

- `sc-release-split-protocol` — handled in T04.01 (D-0010).
- L1 hook layer — handled in Phase 1 / M1.
- L2 CI gate — handled in Phase 2 / M2.
- Other skills that may grow an `--output` argument in the future — they can adopt the same pattern at that time.
