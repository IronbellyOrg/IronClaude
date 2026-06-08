# Roadmap: Sandbox Auth Hardening v0.1-e2e-tl3

## 1) Executive Summary

A small two-phase roadmap whose first phase is deliberately STRICT/critical-path
heavy (auth + credential migration) so the per-phase COMPLEXITY_SCORE override
fires (`n_cpo ≥ 1 OR n_strict ≥ 2` → floor `--depth deep --tier 2`). The work is
SIMULATED inside the sandbox — agents only create throwaway markdown/text under
`.dev/e2e-reflect/tl-3/work/`; no real auth code is written.

## 2) Phased Implementation Plan with Milestones

### Phase 1 — Authentication & Credential Migration (critical path)

- R-001: Design the token-refresh authentication flow and write it to
  `.dev/e2e-reflect/tl-3/work/auth-design.md` (security-sensitive; critical path).
- R-002: Migrate the legacy credential store schema; document the migration and
  rollback in `.dev/e2e-reflect/tl-3/work/credential-migration.md`
  (data migration; breaking-change; critical path).
- R-003: Document the password-hashing parameters in
  `.dev/e2e-reflect/tl-3/work/hashing-params.md` (security-sensitive).

### Phase 2 — Documentation

- R-004: Add a short overview `.dev/e2e-reflect/tl-3/work/overview.md` linking the three Phase-1 docs.

## 3) Success Criteria

- SC-1: All four sandbox docs exist.
- SC-2: Phase 1 is classified STRICT/critical-path so reflect runs at depth=deep/tier=2.
