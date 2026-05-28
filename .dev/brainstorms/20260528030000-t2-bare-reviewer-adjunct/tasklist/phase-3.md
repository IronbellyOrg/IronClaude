---
phase_id: 3
title: Caller plumbing (5 commands)
depends_on: [1.5, 2]
blocks: [4]
estimated_loc: 200 modified
compliance_tier: STANDARD
acceptance_gates: [AC-3.1, AC-3.2, AC-3.3, AC-3.4, AC-3.5, AC-3.6, AC-3.7]
---

# Phase 3 — Caller plumbing

## Scope

Wire `--bare-reviewers N` + companion flags into 5 caller commands. Each caller adds ~30-50 LOC of flag handling + skill invocation + return-contract handling.

Per `multi-caller-integration-evaluations.md`, each caller has different recommended defaults — bake into the per-caller flag defaults (subject to A/B test override).

## Tasks

### T-3.1 — /sc:troubleshoot integration
- Add flags: `--bare-reviewers N` (default 0), `--bare-c7`, `--bare-c7-libs`
- Per-caller default if `SC_DEFAULT_BARE_REVIEWERS=3`: invoke as `--bare-reviewers 3`
- Tier 2 hypothesis pipeline gains bare adjunct as an additional evidence source
- Pass `--challenge-label="troubleshooting"` to c7-enrichment
- LOC modified: ~40

### T-3.2 — /sc:reflect integration (HIGHEST ROI per evaluations)
- Add flags as above
- UC-2 (post-execution audit) is the highest-yield case — replicate the 7.8 experiment shape
- Pass `--challenge-label="completeness-audit"` to c7-enrichment
- **A/B test population primary target** per Deliverable 3 redirect
- LOC modified: ~40

### T-3.3 — /sc:auggie-review integration
- Add flags as above + `--bare-pr-post-mode {strict, loose}` (default: strict)
- PR-post mode gated by IMM-1/IMM-2 quality verification
- Pass `--challenge-label="code-review"` to c7-enrichment
- LOC modified: ~50

### T-3.4 — /sc:code-review integration
- Add flags as above (default `--bare-reviewers 2`, not 3 — per eval)
- Existing 3-layer adversarial structure already covers most cases; bare adds primarily `--bare-c7` library docs value
- Pass `--challenge-label="code-review"` to c7-enrichment
- LOC modified: ~35

### T-3.5 — /sc:tech-research integration (LOWEST PRIORITY)
- Add flags as above (default `--bare-reviewers 2`, post-Phase-6 only)
- Research-producer not finding-emitter — bare's added value is narrow (rf-qa-qualitative already covers similar ground)
- Pass `--challenge-label="feasibility-study"` to c7-enrichment
- LOC modified: ~35

## Acceptance Gate

All AC-3.1..AC-3.7 must pass.

- **AC-3.6** — Each caller respects `SC_DEFAULT_BARE_REVIEWERS` env var when flag omitted
- **AC-3.7** — Each caller surfaces bare-review return-contract status in its own return contract

## Per-Caller Test Fixtures

Each caller needs a small integration test:
- Caller invocation with `--bare-reviewers 2` → produces expected file layout
- Caller invocation with `--bare-c7` → c7-context/ directory appears
- Caller invocation with missing T2ProxyKey → STOP with clear message; caller surfaces

## Risks

- **Per-caller default-value drift** — without empirical A/B data, defaults are speculative. Phase 3 ships with conservative defaults; A/B test (parallel stream) revises if data justifies
- **Flag-naming consistency** — all 5 callers must use identical flag names (`--bare-reviewers`, `--bare-c7`, etc.); enforce via lint or shared snippet
