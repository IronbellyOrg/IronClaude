---
blocking_issues_count: 6
warnings_count: 4
tasklist_ready: false
---

## Findings

- **[BLOCKING]** Traceability — Source requirement IDs `FR-AUTH-003`, `FR-AUTH-004`, `FR-AUTH-005` are remapped/overwritten with different semantics in the roadmap.
  - Location: roadmap.md M2 row 5–6; M3 rows 3–5
  - Evidence: TDD §5.1 defines `FR-AUTH-003` = JWT issuance+refresh (single req), `FR-AUTH-004` = User profile retrieval (`GET /auth/me`), `FR-AUTH-005` = Password reset (two-step). Roadmap splits these: `FR-AUTH-003` = "User Login (token issuance path)", `FR-AUTH-004` = "Token Refresh", `FR-AUTH-005` = "Password Change (authenticated)" — which is NOT in the source at all. Profile retrieval is renamed to `FR-PROF-001`; password reset is split into new `FR-AUTH-006`/`FR-AUTH-007`.
  - Fix guidance: Either (a) preserve source IDs (FR-AUTH-004 → profile, FR-AUTH-005 → reset) and introduce new IDs (e.g., FR-AUTH-PWCHG) for additions, or (b) add an explicit "ID remap table" in the executive summary and update all references. Remove citations to nonexistent PRD FR-007/008/009.
- **[BLOCKING]** Traceability — Endpoint path deviation unreconciled.
  - Location: roadmap.md M3 row 1 (FR-PROF-001 / API-005); TDD §8.2 "GET /auth/me"
  - Evidence: TDD contract says `GET /auth/me`; roadmap implements `GET /profile`. No decision record or CONFLICT entry explains the change; Decision Summary lists 13 decisions, none address this path divergence.
  - Fix guidance: Either restore `/auth/me` path or add a CONFLICT-3 / Decision row documenting the rename with rationale and consumer migration impact.
- **[BLOCKING]** Coverage — `AuthProvider` component from source is not distinctly covered.
  - Location: extraction.md COMP-006 "AuthProvider"; TDD §10.2–10.3; roadmap.md M4 row 6
  - Evidence: Source defines `AuthProvider` as the React Context provider managing `AuthToken` state + silent refresh + 401 interception. Roadmap M4 `COMP-006` is "AuthGuard router component" — a route guard, not a context provider. FEAT-SILENTREF/FEAT-401INT cover the behaviors but no deliverable row represents the provider component itself. Component hierarchy from TDD §10.3 (App → AuthProvider → Routes) is not preserved.
  - Fix guidance: Add a dedicated `COMP-AUTHPROV` (AuthProvider context) deliverable in M4, or rename current COMP-006 and note the equivalence.
- **[BLOCKING]** Structure — ID collisions: `OPS-001..005` and `DM-002` are reused across source and roadmap with different meanings.
  - Location: roadmap.md M5 rows 6–10 (OPS-001..005); M2 row 1 (DM-002); compare extraction.md OPS-001..005 and DM-002
  - Evidence: Source OPS-001 = Runbook/AuthService down; roadmap OPS-001 = "Production Prometheus + Grafana provisioned". Source OPS-002 = Runbook/Token-refresh; roadmap OPS-002 = Tempo backend. All five OPS-* IDs are reused with unrelated semantics. Source DM-002 = `AuthToken` response model; roadmap DM-002 = RefreshToken Redis entity.
  - Fix guidance: Rename roadmap infra rows to OPS-INFRA-PROM, OPS-INFRA-TEMPO, etc.; keep OPS-001..005 for the runbooks/observability from source (or explicitly map them to OBS-007 runbook family). Rename DM-002 (RefreshToken) to DM-REFRESH and introduce a separate DM-AUTHTOKEN response-contract row.
- **[BLOCKING]** Cross-file consistency — test-strategy milestone date windows do not match roadmap milestone windows.
  - Location: test-strategy.md §2; roadmap.md "Timeline Estimates"
  - Evidence: test-strategy V1 runs 2026-03-30→2026-04-10, but roadmap M1 runs 2026-04-20→2026-05-04 (V1 window ends *before* M1 starts). V2 2026-04-13→2026-04-24 vs M2 2026-05-04→2026-05-18. V3 2026-04-27→2026-05-15 vs M3 2026-05-11→2026-05-25. V5 2026-06-01→2026-06-12 vs M5 2026-05-26→2026-06-09. Only V4/M4 partially overlap.
  - Fix guidance: Regenerate test-strategy dates to match the compressed roadmap schedule (M1 start 2026-04-20 per OQ-M1-001 decision). Update `spec_source` frontmatter accordingly.
- **[BLOCKING]** Cross-file consistency — test-strategy cites many deliverables that do not exist in the roadmap.
  - Location: test-strategy.md §§3, 6 (V1–V5)
  - Evidence: Dangling refs include `DM-001..004` (roadmap has DM-001/DM-AUDIT/DM-002/DM-RESET — no numeric DM-003/004), `DEP-001..007`, `ERR-ENV-001` (roadmap has API-ERR), `DOC-API-M2`/`DOC-API-M3`, `ADMIN-001`, `FE-CLOCK-SKEW`, `FE-ERROR-HANDLING`, `RSA-KEY-ROTATION`, `PRD-GAP-LOGOUT`, `REFLECT-M2`/`REFLECT-M3`, `CAPTCHA-INTEG`, `OBS-008`/`OBS-009` (roadmap stops at OBS-007), `OPS-006`/`OPS-007`/`OPS-008` (roadmap M5 has OPS-001..005 + OPS-011 only), `SEC-001..006`, `COVERAGE-GATE`, `DATA-MIG-SCRIPT`, `PERF-BASELINE`, `LOAD-TEST-FULL`, `NFR-COMP-002-RETENTION`, `NFR-COMP-001-CONSENT`, `SEC-AUDIT-TOKEN`, `AUDIT-002-COVERAGE`, `RELIABILITY-READINESS`, `SEC-CSP`, `CORS-PREFLIGHT-TEST`, `TEST-DUP-EMAIL`, `TEST-WEAK-PWD`, `TEST-REVOKE`, `TEST-RESET-FLOW`, `TEST-E2E-RESET`.
  - Fix guidance: Either add these as concrete roadmap deliverables (preferred — the test activities are real and the roadmap is otherwise shy on test-category rows) or remove/rename them in the test-strategy to reference existing roadmap IDs.

- **[WARNING]** Decomposition — Several row-level deliverables are compound and will require splitting by sc:tasklist.
  - Location: roadmap.md M1 row 8 (FR-AUTH-002); M1 row 1 (DM-001); M2 row 2 (COMP-JWTSVC)
  - Evidence: FR-AUTH-002 AC mixes valid/duplicate/weak-password/consent flows in one row. DM-001 AC enumerates 11 column constraints + migration + index verification. COMP-JWTSVC bundles sign/verify/getPublicKey/rotateKeys (four distinct ops).
  - Fix guidance: No action required at roadmap level — flag to tasklist generator that these rows should decompose into ≥2 tasks each.
- **[WARNING]** Structure — Heading inconsistency between M1 and M2–M5.
  - Location: roadmap.md `## M1: Foundation …` vs `## Milestone M2: …`
  - Evidence: M1 omits the "Milestone" prefix and omits a `### Deliverables — M1` H3 (table is placed directly under the H2); M2–M5 all use "Milestone {N}: …" and introduce a `### Deliverables — M{N}` H3 before the table.
  - Fix guidance: Normalize to `## Milestone M1: Foundation …` and add `### Deliverables — M1` before the table.
- **[WARNING]** Cross-file consistency — test-strategy frontmatter `spec_source` points at `test-tdd-user-auth.md` (uncompressed) while roadmap frontmatter points at `test-tdd-user-auth.compressed.md`.
  - Location: test-strategy.md frontmatter line 7; roadmap.md frontmatter line 2
  - Evidence: Divergent spec_source values make it ambiguous which upstream the validation layer should trust.
  - Fix guidance: Align both to the same source (use `.compressed.md` for both since roadmap is compressed-source-derived).
- **[WARNING]** Proportionality (observation) — roadmap has many rows with no matching test-strategy coverage because the strategy references phantom IDs instead.
  - Location: test-strategy.md §6 V4/V5 vs roadmap.md M4/M5
  - Evidence: Roadmap M4 adds OBS-001..007, COMP-018/019, API-007..011 — test-strategy refers to OBS-008/009, SEC-CSP, etc. instead. Symmetric gap.
  - Fix guidance: See BLOCKING #6; once dangling refs are reconciled this warning resolves.

## Summary

Total: 6 BLOCKING + 4 WARNING + 0 INFO. Roadmap is **not ready** for tasklist generation. Primary issues are (1) source requirement IDs (FR-AUTH-004/005, OPS-001..005, DM-002) being reassigned to different deliverables without a remap table, (2) missing or renamed first-class components (AuthProvider, `/auth/me`), and (3) a test-strategy artifact whose dates and deliverable IDs are out of sync with the roadmap. Coverage against source entities is otherwise strong (107 task rows vs ~36 source entities; interleave_ratio = 1.0).

## Interleave Ratio

interleave_ratio = unique_milestones_with_deliverables / total_milestones = 5 / 5 = **1.0** (within [0.1, 1.0]; test activities are present in every milestone — TEST-001/002/004 + k6 in M1, TEST-003/005/ME in M2, TEST-PROFILE/RESET in M3, TEST-006/E2E-REFRESH/E2E-LOGOUT in M4, chaos drills in M5; no back-loading).
