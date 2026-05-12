---
blocking_issues_count: 3
warnings_count: 1
tasklist_ready: false
---

## Findings

- **[BLOCKING]** Structure: Dangling reference `OQ-CFLT-002` in a milestone task row.
  - Location: roadmap.md:259; roadmap.md:105-112; roadmap.md:231-240
  - Evidence: `COMP-002` says "immediate-login chaining per OQ-CFLT-002", but the roadmap defines `OQ-CONFLICT-001`, `OQ-CONFLICT-002`, `OQ-REFRESH-TRANSPORT-001`, `OQ-002`, `OQ-PRD-001..004`, and `OQ-001` only. No `OQ-CFLT-002` exists in the roadmap.
  - Fix guidance: Replace `OQ-CFLT-002` with the intended in-roadmap ID, or add a properly defined OQ row with owner/target/resolution and update all references consistently.

- **[BLOCKING]** Coverage: The original API-consumer/programmatic refresh requirement is not covered by a matching roadmap task; the roadmap substitutes a different contract.
  - Location: test-prd-user-auth.md:117,139,313-314; test-tdd-user-auth.md:285,434,526-550; roadmap.md:30,111,192,206,465
  - Evidence: The PRD requires Sam to "refresh tokens without user interaction," and the TDD defines `POST /auth/refresh` with `refreshToken` in the request body. The roadmap instead commits to browser-only HttpOnly-cookie transport and says dual-mode/request-body refresh is not shipped in v1.0 pending `OQ-REFRESH-TRANSPORT-001`. That leaves the original source requirement without a concrete matching roadmap task.
  - Fix guidance: Either add explicit roadmap tasks for an API-consumer refresh path compatible with the source docs, or update the TDD/PRD to remove that requirement before tasklist generation.

- **[BLOCKING]** Traceability: `NFR-COMPLIANCE-001` / "all auth events logged" does not trace to concrete implementation rows for several auth flows; only late QA asserts it.
  - Location: test-prd-user-auth.md:251-254,324-325; extraction.md:80-81; roadmap.md:139-140,191,207,276,359
  - Evidence: The source requires all auth events to be logged. The roadmap has explicit audit-emission tasks for login and registration (`OPS-AUDIT-LOGIN`, `OPS-AUDIT-REG`) plus revoke/logout side effects, but no concrete implementation rows for audit writes on refresh, `/me`, reset-request, or reset-confirm. Despite that, `OPS-AUDIT-QA` asserts that every `FR-AUTH-001..005` path plus logout emits exactly one audit row.
  - Fix guidance: Add explicit implementation deliverables for audit emission on each missing auth flow, or narrow the QA claim and source requirement so requirement-to-deliverable tracing is complete and unambiguous.

- **[WARNING]** Decomposition: Several roadmap rows are compound and likely need splitting before `sc:tasklist`.
  - Location: roadmap.md:69,259,208,285
  - Evidence: Examples include `DM-001` ("TypeScript interface + PostgreSQL schema"), `COMP-002` (register UI + consent + immediate-login chaining + failure-compensation path), `COMP-015` ("backend + frontend pair"), and `JTBD-GAP-001` (query surface + lock-account action + admin-scope behavior). These bundle multiple outputs/actions into one row.
  - Fix guidance: Split each row into single-output tasks with one primary artifact/action per row so the task splitter can generate cleaner, non-compound tasks.

## Summary

- BLOCKING: 3
- WARNING: 1
- INFO: 0

Overall assessment: the roadmap is **not ready** for tasklist generation. Schema, milestone/test-strategy alignment, parseability, and proportionality are acceptable, but the dangling reference, source-contract gap on refresh transport, and incomplete requirement-to-deliverable audit tracing must be fixed first.

## Interleave Ratio

Using milestones that contain explicit test deliverables (`TEST-###` rows):

- unique_milestones_with_deliverables = 3 (`M2`, `M3`, `M4`)
- total_milestones = 5
- interleave_ratio = 3 / 5 = **0.60**

Assessment: within the required range `[0.1, 1.0]`, and test activities are **not** back-loaded into only the final milestone.
