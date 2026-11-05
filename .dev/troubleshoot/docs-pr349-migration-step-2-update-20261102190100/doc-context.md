# Documentation Context Card

**Generated**: 2026-11-02T19:08:57Z
**Wave**: 1.5
**Scope**: docs/releases/v5.0.0.md:147

## Release context

- **Release**: v5.0.0
- **Artifacts**: .dev/releases/current/v5.0.0/DECISIONS.md, .dev/releases/current/v5.0.0/RELEASE-READINESS.md, .dev/releases/current/v5.0.0/A3-RESULT.md
- **Summary**: Decision 7.6 (DECISIONS.md:7) and RELEASE-READINESS.md:67/:151/:180 treat `superclaude update` and `./update.sh` as interchangeable because both force-refresh files; none checks whether `update` runs the codegraph phase or the retire step. Gate G7 (RELEASE-READINESS.md:198) runs `./update.sh`, so it never exercises the `update` path the notes recommend.
- **Confidence**: 0.85

## Architectural docs consulted

- `docs/user-guide/mcp-installation.md` — verdict: `current` — install (and so ./update.sh) installs codegraph and runs the retire step (:7, :23, :54, :64-66); update never touches MCP registrations (:70); :71 ambiguous wording on install --force.
- `docs/reference/mcp-server-guide.md` — verdict: `current` — codegraph installed and registered by superclaude install (:13, :29, :43).
- `docs/getting-started/installation.md` — verdict: `current` — upgrade described as `superclaude update` only (:53-57, :326-333, :363); :365 says install --force "does the same"; no codegraph mention.
- `docs/releases/v5.0.0.md` — verdict: `current` — the defective text under review (:3, :69, :143-150, :152).
- `docs/developer-guide/testing-debugging.md`, `docs/reference/diagnostic-reference.md`, `docs/user-guide/freshness-hooks.md`, `docs/user-guide/flags.md`, `CLAUDE.md` — verdict: `current` — install --force semantics for framework files; no MCP content.
- `docs/reference/troubleshooting.md` — verdict: `stale` — unrelated stale quick fixes (:10).

> CAUTION: docs/reference/troubleshooting.md is stale per the Section 2 currency check; treat its claims as advisory, not authoritative.

## Restrictions / decisions that constrain the fix

- `src/superclaude/cli/main.py:407` (update) — "# Read-only: update never touches MCP registrations."
- `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:848` (decision D7) — update.sh and superclaude update unchanged; "`update.sh:8` already runs `install --force`; `update` is documented never to touch MCP state"
- `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:192` (upgrade path) — "after `./update.sh` on an existing workspace, Serena and codebase-memory must be completely absent."
- `src/superclaude/rules/core/changelog_maintenance.md:180` (release notes) — "- ❌ **NEVER** forget migration notes for breaking changes"
- `src/superclaude/cli/install_retired_mcp.py:3` (retire step) — "Runs at the end of ``superclaude install`` and never changes its exit code."

## Re-frame signals

- The code behavior is the documented design (D7, main.py:407, mcp-installation.md:70): the defect is in the release notes, not in `superclaude update`. Remediation target: docs, not code.
- The design's upgrade path is `./update.sh` = `superclaude install --force` (phase-2 spec :192, :848); the notes must point upgraders at `superclaude install --force` and must not call `update` equivalent to `update.sh`.
- Related, out of scope for this finding: docs/getting-started/installation.md:326-333/:365 and decision 7.6 share the same update-vs-install conflation (log for follow-up).
