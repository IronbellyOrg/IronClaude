# Refactoring Plan — Adversarial Merge

## Overview

- **Base variant:** Variant C (combined score 0.930) — honest G1-status framing; the only variant whose state-claims match git ground truth.
- **Incorporated from:** Variant A (analytical primitives, git forensics), Variant B (theatre scorecard structure, Contract Identity Ledger).
- **Planned changes:** 10 grafts. **Rejected changes:** 8 (documented for transparency).
- **Overall risk:** Medium — most grafts are additive, but two carry HIGH integrity risk (fabrication removal + relabel rule) and are governed by binding constraints from `round3-resolution.md`.
- **Binding constraints (from Round 2.5 invariant probe + Round 3 remediation):**
  - **BC-1 (relabel rule, INV-009):** Every imported scorecard/matrix cell MUST be stripped of all run-result tokens (`8/8`, `7/7`, `100%`, `3.0%`, `round 2`, `✓ caught`, `did_catch`) and carry the literal token `NOT YET PROVEN (pre-build)`. Header relabel alone is INSUFFICIENT.
  - **BC-2 (crosswalk, INV-001/006):** The canonical crosswalk (E1–E5 ↔ M-instances ↔ 9-row table ↔ contract-implementations source) is the single reconciliation backbone. E4 is sourced from `contract-implementations.md`, has **no** row in the 9-row table; "E4" ≠ table "PRD-E04" (the `--file` bug is canonical **E1**).
  - **BC-3 (boundary, INV-007/008/016):** Use the 3-bucket ledger. Neither "nothing was fixed" nor "the refactor is validated" is permitted.
  - **BC-4 (metric, X-002):** `59%/41%` is a per-stage value/ceremony mean, NOT an escape-catch rate; never present it as a catch rate.

## Planned Changes

| # | Title | Source → Target | Rationale (debate evidence) | Risk |
|---|-------|------------------|------------------------------|------|
| 1 | Honest G1-status header & posture | C → top of report | X-007 unanimous; `git diff 94d5baa0..master` empty. Spine of the merged doc. | Low |
| 2 | Corrected executive verdict | C + A/B → §1 | Stack was largely theatre for the registry-miss class; every M-series miss surfaced at runtime; lone pre-runtime catches were #154-review + sc:reflect, not the design-stage debate. | Low |
| 3 | Canonical crosswalk table (E1–E5 ↔ M-instances ↔ 9-row table ↔ source-of-record ↔ fix status) | round3-resolution → §3 | BC-2; resolves INV-001 orphaned-E4 + INV-006 four-scheme collision. | Medium |
| 4 | 3-bucket committed/unbuilt ledger | round3-resolution → §4 | BC-3; UNBUILT H0–H5 vs MERGED #149/#151/#153/#154/#155 (E1/E2/E3/E5) vs UNMERGED `b97c9960` (E4). | Medium |
| 5 | Per-stage theatre scorecard (relabeled) | A/B (S-004) → §5 | C lacks it; graft under BC-1. | **High** (BC-1) |
| 6 | Would-have-caught matrix (predicted, relabeled) | A/B (S-005) → §6 | C lacks it; map E1–E5 × H-waves; every cell `NOT YET PROVEN (pre-build)`. | **High** (BC-1) |
| 7 | Corrected lone-catch attribution + caveat | C + A/B → §7 | X-001 synthesis: #154 `r3383060121`→F-A/E2; sc:reflect→E5; human-vs-tool actor unproven (explicit caveat). | Medium |
| 8 | Analytical primitives as design rationale | A (U-001 patch-relative, U-002 negative-witness; §7 irreducibility) → §8 | High-value unique contributions; framed as rationale for the (unbuilt) H-waves. | Low |
| 9 | Contract Identity Ledger | B → §9 | Best mechanism for the E4 + M6 contract-identity class; keep M6 (`prd/executor.py:259` vs `prd/config.py:30`, true blame `27962ddb2`/`09e2ccc0d`) and E4 as separate rows. | Low |
| 10 | Hardening-spec linkage + paste-ready G1 prompt | C → §10 | Halt-pending-approval posture; H0–H5 target + closure controls. | Low |

## Changes NOT Being Made (rejected — transparency)

| Rejected | Source | Why rejected |
|----------|--------|--------------|
| §6 "rollback-replay 8/8 / 100%" | A | Fabricated (X-007); refactor never built. DELETE. |
| "7/7 rollback-replay" + "implemented" claims | B | Fabricated (X-007). DELETE. |
| 6.25% (A) / 3.0% (B) theatre ratios as headline | A, B | Self-built denominators not grounded in any evidence card; only `59%/41%` (value/ceremony mean) is grounded, and only qualitatively (BC-4). |
| 8-item (A) / 7-item (B) as the canonical escape SET | A, B | Canonical set is E1–E5; these are instances (X-003). Kept inside the crosswalk only. |
| "PR #158-equivalent" phrasing | B | No PR #158 exists; `b97c9960` is unmerged (X-005). |
| "M6 committed in #149" | consensus draft | Imprecise; true blame `27962ddb2`/`09e2ccc0d` (INV-012). |
| Blanket "nothing was fixed" | (anti-overclaim) | E1/E2/E3/E5 point-fixes shipped; would be a NEW overclaim (INV-007). |
| Treating E4 as purely "spec-only awaiting G1" | C | E4 fix exists committed-but-unmerged on `origin/fix/prd-executor-advisory-gate` (INV-016). |

## Review Status

- **Approval:** Auto-approved (non-interactive run).
- **Timestamp:** 2026-06-10
