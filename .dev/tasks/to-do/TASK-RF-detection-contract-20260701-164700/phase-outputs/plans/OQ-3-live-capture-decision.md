# OQ-3 Live GitHub Capture Timing Decision

Status: Complete

- Open Question: OQ-3 / V2 live capture timing
- Recommended default: `file-based-v1-only`
- Selected value: `file-based-v1-only`
- Decision recorded at: 2026-07-01 19:21 UTC
- Decision source: user selected File-based v1 (Recommended) during the Step 1.5 human-decision gate.

## Rationale

The approved v1 scope is file-based evidence loading and validation from captured probe JSON. The design explicitly treats live capture as a later `load_evidence` source and the requirements place optional GitHub capture after file-based validation is tested.

## Hard Scope Statement

No live polling, live GitHub API fetch, or `gh` capture may be implemented by this task unless a later explicit decision replaces this file with `include-live-capture-v2`. Phase 2 and Phase 3 evidence/readiness work must remain file-based by default and must not introduce network/API side effects from setup or readiness paths.

## Dependent Phases Unlocked

- Phase 2 evidence loading/validation may consume existing captured files such as `gh-reviews.json`, `gh-comments.json`, `gh-check-runs.json`, and `combined-payload.json`.
- Phase 2 candidate derivation and validation must treat omitted surfaces distinctly and must not infer unobserved fields from defaults alone.
- Phase 3 readiness validation may diagnose and validate existing file-based evidence; it must not fetch live GitHub data.
- Phase 4 evidence/no-side-effect tests must prove setup and readiness paths stay file-based and introduce no live GitHub polling, `gh` capture, or network/API side effects.

## Blocking Status

Decision is non-PENDING. Evidence implementation may proceed after the prior Phase 1 gate passes, but only within the file-based v1 scope. The `include-live-capture-v2` alternative is not approved by this decision.
