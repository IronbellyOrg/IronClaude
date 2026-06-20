# R0 Acceptance Report

**Phase:** 5 Step 5.4
**Run date:** 2026-06-01
**Branch:** `refactor/roadmap-pipeline-r0-r1-rewrite`
**HEAD:** `bdfad6d3`
**Parent (pre-R0 master):** `91095144`

## Executive summary

**R0 PASS — ready for R1 gate (PG5.1).** All three R0 deliverables shipped on schedule across 4 commits on `refactor/roadmap-pipeline-r0-r1-rewrite`. MultiModelSwarm anti-instinct halt fully resolved (zero HIGH undischarged on the user's currently-halting roadmap). 4 Contract items (#5, #8, #9, #10) are now CI-enforced — Contract #5 pipeline-blocking via `make lint-architecture` Check 11; Contracts #8, #9, #10 PR-blocking via dedicated pytest files. PRESERVE invariants byte-identical (commands.py / structural_checkers.py / convergence.py / cosmetic_remediator.py).

## Commits on R0

| Commit | Phase | Contract items closed |
|---|---|---|
| `6cee1eb1` | Phase 2 (R0.1) | #9 — Spec-ID registry + MERGE_GATE containment |
| `f41ea931` | Phase 3 (R0.2) | #10 — Anti-instinct allowlist + recurrence fixtures |
| `665d34ca` | Phase 3 M8 fix | M8 imperative-verb override (prevents allowlist over-broadening) |
| `bdfad6d3` | Phase 4 (R0.3) + Phase 5 Step 5.1 | #5 + #8 — `superclaude.contracts` SoT + arch-lint + Check 11 CI gate |

4 commits total on branch, parent `91095144` (last pre-R0 master).

## R0 deliverables — landing phase, key file, test coverage

| R0 item | Landing phase | Key file(s) | Test file(s) |
|---|---|---|---|
| R0.1 — Spec-ID registry (Contract #9) | Phase 2, commit `6cee1eb1` | `src/superclaude/cli/roadmap/id_registry.py` (NEW) | `tests/roadmap/test_spec_roadmap_id_containment.py` (11 PASS) |
| R0.2 — Anti-instinct allowlist (Contract #10) | Phase 3, commits `f41ea931` + `665d34ca` (M8 fix) | `src/superclaude/cli/roadmap/obligation_scanner.py` (allowlist + imperative-verb override); `tests/roadmap/fixtures/recurrence/anti_instinct/*` (5 fixtures) | `tests/roadmap/test_anti_instinct_recurrence.py` (8 PASS) |
| R0.3 — Contracts SoT (Contract #5 + #8) | Phase 4, commit `bdfad6d3` | `src/superclaude/contracts/__init__.py` (NEW, 99 LOC); `src/superclaude/tools/arch_lint.py` (NEW, 255 LOC); 3 consumer migrations | `tests/roadmap/test_threshold_registry.py` (12 PASS); `tests/contracts/test_arch_lint.py` (11 PASS) |

## Contract satisfaction matrix (R0 items closed)

| Contract # | Mechanism | Pipeline-Blocking? | Test file | Recurrence fixtures | CI Wired? |
|---|---|---|---|---|---|
| #5 (no return-True fragility stubs) | `make lint-architecture` Check 11 (arch-lint walker) | **YES** (via `lint: lint-architecture` Makefile dep) | `tests/contracts/test_arch_lint.py` + `tests/roadmap/test_threshold_registry.py::test_arch_lint_passes_on_clean_repo` | n/a (Contract #5 is a code-shape invariant) | ✅ Check 11 in Makefile L463-473 |
| #8 (no duplicate cross-skill constants) | `superclaude.contracts` SoT + arch-lint walker | **YES** (Check 11 same as Contract #5) | `tests/roadmap/test_threshold_registry.py` (12 tests) | n/a | ✅ Same Check 11 wiring; PR-blocking pytest via standard CI |
| #9 (roadmap_ids ⊆ spec_ids ∪ accepted_deviations) | `id_registry.py` registry + MERGE_GATE containment check | **PR-blocking** | `tests/roadmap/test_spec_roadmap_id_containment.py` (11 tests, incl. fail-shut on sidecar missing) | n/a | ✅ Standard pytest CI |
| #10 (anti-instinct allowlist with documented FP fixtures) | `obligation_scanner.py` `_ALLOWLIST_PHRASES` + imperative-verb override | **PR-blocking** | `tests/roadmap/test_anti_instinct_recurrence.py` (8 tests) | 5 fixtures under `tests/roadmap/fixtures/recurrence/anti_instinct/` (multimodelswarm_fp_case, stub_worker_parallelism_fp_case, module_path_fp_case, valid_obligation_case, imperative_verb_override_case) | ✅ Standard pytest CI |

## Contract items deferred to R1

Per BUILD-REQUEST §R1 scope (out of R0 scope):

| Contract # | Reason for R1 deferral |
|---|---|
| #1 (full recurrence corpus — ≥1 fixture per RECURRENT row) | R0.2 seeded only 5 fixtures (anti-instinct cluster); rows #1, 2, 4, 5, 7, 8, 9, 12, 14, 15, 16, 17, 19, 20, 21, 22 require fixtures during R1 final acceptance (Phase 13). |
| #2 (dispatch-reachability AST walker) | R1 only — wired in R1.5 `verify-implementation` terminal step. |
| #3 (PR-lint generator-constraint) | R1.4 only — emerges from tool-write rewrite of generator steps. |
| #4 (no-silent-PASS on empty target) | R1 only — depends on R1.2 envelope arrival to detect empty targets reliably. |
| #6 (frontmatter parser consistency) | R1.6 cleanup only — canonicalize on `pipeline/gates.py:_check_frontmatter` L91 after dual parsers are deleted. |
| #7 (retry mutates input) | R1 only — depends on R1.3 `CodeAssertion` slot. |

## Acceptance gates (BUILD-REQUEST §Acceptance gates 1-8) — status

| Gate | Status | Evidence |
|---|---|---|
| #1 — All Contract items 1-10 enforced as CI gates | **R0: 4/10 enforced (#5, #8, #9, #10).** R1: remaining 6. | See Contract satisfaction matrix + deferral table above. |
| #2 — All current passing tests in `tests/roadmap/` still pass | **R0-introduced tests: 42/42 PASS.** 12 pre-existing failures verified to predate R0 (baseline `91095144` reproduction). | `phase-outputs/test-results/r0-acceptance-full-validation.txt` |
| #3 — Pipeline runs without halting on anti-instinct FPs of catalogued classes | **PASS for MultiModelSwarm class.** R1 verifies broader corpus. | `phase-outputs/test-results/r0-acceptance-multimodelswarm-summary.md` |
| #4 — Recurrence corpus seeded ≥1 per RECURRENT row | **R0 partial:** 5 fixtures (anti-instinct cluster, row #6). 16 RECURRENT rows still need fixtures in R1 final acceptance (Phase 13). | `tests/roadmap/fixtures/recurrence/anti_instinct/*` |
| #5 — MultiModelSwarm anti-instinct halt resolved | **PASS.** Direct `obligation_scanner.scan_obligations()` invocation: 0 HIGH undischarged, 0 obligations on previously-FP lines 207/211/213. | `phase-outputs/test-results/r0-acceptance-multimodelswarm-scan.txt` + summary |
| #6 — Step count ≤ 14 | **PASS — 14 steps.** R0 did not add pipeline steps. | `_get_all_step_ids(config)` returned 14 IDs (extract / 2× generate-sonnet / diff / debate / score / merge / anti-instinct / test-strategy / spec-fidelity / wiring-verification / deviation-analysis / remediate / certify). |
| #7 — Zero `return True` fragility stubs in `src/superclaude/cli/` | **R1.6 cleanup scope.** R0 contract: must NOT ADD fragility stubs. **Verified: 2 `return True` lines added by R0 are substantive boolean predicates (containment check success in `id_registry.py`, allowlist final-clause in `obligation_scanner.py`), NOT fragility stubs.** 113 pre-existing `return True` lines remain; cleanup is R1.6 scope per BUILD-REQUEST §R1.6. | `git diff 91095144 bdfad6d3 -- src/superclaude/cli/` searched for `+\s*return True\s*$` — 2 matches, both substantive predicates. |
| #8 — `verify-implementation` terminal step live and wired | **R1.5 scope (deferred).** | n/a in R0. |

## MultiModelSwarm halt resolution evidence

The user's currently-halting MultiModelSwarm pipeline run was the primary trigger for R0 (Acceptance Gate #5). Resolution evidence:

- **Direct scan of current roadmap** (`/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/roadmap.md`, 78,760 bytes):
  - Total obligations: 3
  - HIGH: 0
  - MEDIUM: 3 (2 undischarged — both code-block-adjacent, not the original FP cluster)
  - LOW: 0
- **Previously-FP line cluster (L207/211/213, per Phase 3 record):** 0 obligations emitted on any of these lines.
- **MEDIUM undischarged sites (L457, L464):** neither in the original FP cluster; neither blocking (only HIGH undischarged trigger halts per convergence-threshold logic).

The R0.2 allowlist (5 seed phrases + `frozenset` + imperative-verb override) demotes the previously-HIGH-firing prose. Pipeline halt resolved.

## Test counts (cumulative across all R0 commits)

| Suite | Count | Status |
|---|---|---|
| `tests/roadmap/test_spec_roadmap_id_containment.py` (Contract #9, R0.1) | 11 | PASS |
| `tests/roadmap/test_anti_instinct_recurrence.py` (Contract #10, R0.2) | 8 | PASS |
| `tests/roadmap/test_threshold_registry.py` (Contract #8, R0.3) | 12 | PASS |
| `tests/contracts/test_arch_lint.py` (Contract #5 walker, R0.3) | 11 | PASS |
| **R0-introduced total** | **42** | **42/42 PASS** |
| Full `tests/roadmap/` + `tests/contracts/` | 1770 | 1758 PASS, 12 FAIL (pre-existing — baseline-reproduced), 13 skip |

## PRESERVE invariant audit

`git diff --stat 91095144 -- <PRESERVE targets>` — empty output. All four PRESERVE targets byte-identical to pre-R0 master baseline:

| File | Diff vs `91095144` |
|---|---|
| `src/superclaude/cli/roadmap/commands.py` | (empty — no changes) |
| `src/superclaude/cli/roadmap/structural_checkers.py` | (empty — no changes) |
| `src/superclaude/cli/roadmap/convergence.py` | (empty — no changes) |
| `src/superclaude/cli/roadmap/cosmetic_remediator.py` | (empty — no changes) |

## M8 status

**Resolved in `665d34ca`.** M8 (imperative-verb override prevents allowlist short-circuit) was patched during Phase 3 R0.2 work. `_ALLOWLIST_IMPERATIVE_OVERRIDE_RE` in `obligation_scanner.py` ensures imperative-verb + scaffold-term pairs still emit HIGH even when the line matches an allowlist phrase. Test: `tests/roadmap/test_anti_instinct_recurrence.py::test_imperative_verb_overrides_allowlist[recurrence_case0]` (PASS).

## Open Questions / Deferrals for R1

1. **NFR-pattern reconciliation** (R0.3 §E deviation): the SoT pattern `r"NFR-\d+(?:\.\d+)?"` is broader than BUILD-REQUEST §MVR §5 verbatim `r"NFR-\d+"`. R1.1 reconciles by either widening the SoT or adding an `NFR_SUB` family.
2. **5 R1.1-scope consumer migrations** queued: `fidelity_checker.py` heading regex; `fingerprint.py` threshold scalars; `spec_structural_audit.py` threshold scalars; prose constants in `gates.py` + `executor.py`.
3. **`audit` subcommand absence on `superclaude roadmap` CLI** (surfaced by Step 5.2). The orchestrator-suggested invocation `uv run superclaude roadmap audit <roadmap>` does not exist; only `run`, `validate`, `accept-spec-change` are exposed. R1 can either (a) add an `audit` subcommand that wraps `obligation_scanner.scan_obligations()`, or (b) treat anti-instinct as a roadmap-internal step only (current behavior). Direct Python invocation is the documented escape clause used in this Step.
4. **Pre-existing 12 test failures** (haiku→sonnet default-agent drift from `70ef6486` + pipeline integration step-count drift). Not R0-caused but should be addressed in R1 final-acceptance cleanup (Phase 13).
5. **Recurrence-corpus seeding** for the remaining 16 RECURRENT rows (Phase 13 scope per BUILD-REQUEST §Acceptance Gate #4).

## Ready for R1

**Verdict: PASS — Ready for R1 (after PG5.1 R0 acceptance gate).**

- R0 deliverables landed.
- 4 Contract items CI-enforced.
- MultiModelSwarm halt resolved.
- PRESERVE invariants intact.
- No regressions caused by R0.
- 5 named deferrals queued for R1 with explicit phase assignments.

PG5.1 (rf-qa-qualitative R0 acceptance verification) is the next gate; PG5.2 acts on the verdict.
