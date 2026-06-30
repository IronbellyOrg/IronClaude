# Code Review: PR #193 — feat(tasklist): add RFMerger P1–P5 enhancements to the sc:tasklist generator

**Target**: PR [#193](https://github.com/IronbellyOrg/IronClaude/pull/193)
**Reviewer**: /sc:auggie-review (depth=standard, focus=all)
**Generated**: 2026-06-20 19:05 UTC
**Base ↔ Head**: `master` (63f1a81) ↔ `feature/rfmerge-p1-p5` (4553981)
**Stats**: 168 files changed in the PR, but only **5 are reviewable source** (684 insertions / 11 deletions). The other 163 are `.dev/` workspace artifacts (QA reports, test logs, the executed MDTM task workspace) — out of code-review scope.
**Reviewable surface**:
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (+155 / −11) — the deterministic generator contract
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` (+13)
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (+9)
- `tests/skills/test_task_builder_merge.py` (+59)
- `tests/tasklist/test_tasklist_cli.py` (+459)

---

## Summary

**Recommendation: approve-ish / nits-only. No blocking findings.**

This PR implements the five RFMerger proposals (P1 Context-Armed Steps, P2 Bounded Patch Loop, P3 DNSP synthetic findings, P4 Evidence-Anchored Validation, P5 Tier Calibration Advisory) plus a cross-cutting `--spec` Input-Contract reconciliation, in the `sc:tasklist` deterministic generator spec. The work is high-quality: the three borrowed contracts (DM-003, Execution Context, PR-02) are genuinely reused **byte-exact** (verified — em-dash literals, dedup_key shape, and halt strings all match the task-builder source), the P5 advisory is correctly fenced as a pure read-only function, and the new tests are reasonably thorough at the presence/substring level. **125 affected tests pass on the PR head** (57 tasklist + 68 task-builder-merge), confirming the author's green-suite claim.

The Auggie deep pass produced 7 findings + 3 cross-cutting observations, but **5 of them were dropped as false positives** during the file:line grounding pass — Auggie indexed the reviewer's checked-out base branch rather than the PR head, so it read pre-change line content and flagged changes as "not landed." After grounding against the actual PR-head content, the surviving items are all **Low / Nit test-robustness and clarity polish** — none block merge.

The single recurring (advisory) theme worth the author's attention: several new tests assert **presence/substring** ("the literal appears somewhere") rather than **byte-exact parity** or **runtime emission**. The contracts are conformant *today*, so these are future-drift-detection gaps, not current defects.

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._ (Auggie reported 3 "high" findings; all three were false positives — see "Dropped findings" below.)

### 🟡 Medium

_None._

### 🟢 Low (nice-to-have)

#### L1. `## Execution Context` "VERBATIM" reuse is tested at sub-field-name level, not byte-exact block parity
- **File**: `tests/skills/test_task_builder_merge.py:429`
- **Category**: tests (test robustness)
- **Source**: auggie (grounded)
- **Status**: real but advisory — the contract **is** byte-exact today (verified: `References` / `Source areas` / `Key constraints` shape matches the task-builder source).
- **Why this matters**: `test_p1_execution_context_contract_identical_across_surfaces` asserts the three sub-field *names* appear on both surfaces and that the `file:line` discipline is mentioned. It would still pass if the emission rule (e.g. the "References-only degraded form" branch) drifted between the SKILL inline copy and the task-builder source. The "VERBATIM" claim is stronger than the test enforces.
- **Recommendation**: Either add a block-extraction test asserting byte-equality of the Execution Context template across both `SKILL.md` files (modulo the documented `GOAL` vs `R-###` placeholder difference), or soften the PR/spec wording from "VERBATIM" to "MIRRORS" if intentional differences exist.

#### L2. DM-003 recommendation literal asserted by substring, not exact-equality
- **File**: `tests/skills/test_task_builder_merge.py:410`
- **Category**: tests (test robustness)
- **Source**: auggie (grounded)
- **Status**: real but advisory — the literal **is** byte-exact today (verified: `Manual review required — partition agent failed twice`, em-dash U+2014, no hyphen-minus variant, no trailing whitespace, present identically in both `task-builder/SKILL.md:881` and `sc-tasklist-protocol/SKILL.md:1384`).
- **Why this matters**: `assert "Manual review required — partition agent failed twice" in body` is a substring check. A future accidental trailing suffix or a hyphen-for-em-dash substitution that *contains* the substring could slip past it, despite the spec pinning this as a "byte-exact" invariant.
- **Recommendation**: Extract the `recommendation:` literal from its line and assert exact equality (`==`) rather than membership.

#### L3. Template-mirror parity is guarded at heading/field level, not full emission-rule parity
- **File**: `tests/tasklist/test_tasklist_cli.py:386` (and `:637`)
- **Category**: tests (test robustness)
- **Source**: auggie (grounded, partially corrected)
- **Status**: real but advisory. Auggie claimed "no test verifies the mirrors" — that is **wrong**: `test_execution_context_mirror_in_phase_template`, `test_execution_context_block_not_in_index`, and `test_p5_advisory_index_template_mirror` do guard the mirrors. The residual gap is that they assert heading + key-field *presence*, not byte-exact parity of the deterministic emission branches (emit-iff-≥1-ref, References-only-degraded, omit-when-none) between `SKILL.md` §4.1d and `phase-template.md`.
- **Why this matters**: The phase/index templates correctly *reference* `SKILL.md` §4.1d as the authority (good single-source design), so drift risk is already low. But the emission-branch wording could still diverge without a test catching it.
- **Recommendation**: Optional — add a branch-parity assertion, or rely on the existing reference-to-§4.1d design and accept presence-level guarding as sufficient.

#### L4. P2 bounded-loop iteration table is tested for spec-text presence, not runtime emission
- **File**: `tests/tasklist/test_tasklist_cli.py:520` (`TestP2BoundedPatchLoop`)
- **Category**: tests (coverage gap)
- **Source**: auggie (grounded)
- **Status**: real but advisory, and partly by-design. The P2 guards (regression > monotonicity precedence, strict-shrink, byte-exact halt strings, `synthetic-dnsp` exclusion from `F_k`) **are** tested via `test_p2_bounded_loop_guards` and `test_p2_excludes_synthetic_dnsp_from_fk`. What is not tested is an end-to-end emission of the per-pass `|F_{k-1}|` / `|F_k|` history table — but this test suite validates *spec content*, not the runtime generator, so runtime emission may be out of its intended scope.
- **Why this matters**: The iteration table is the operator's debugging evidence for *why* a loop halted; if it were silently never emitted, no current test would notice.
- **Recommendation**: If/when a runtime harness exists for the generator, add an integration test asserting a 2-pass loop emits a table with correct `|F_k|` values. No action needed for this PR if runtime testing is out of scope.

### 💬 Nits

- **N1** — `SKILL.md:1339` (gate-results.txt inlining): the orchestrator-read step is already stated inline three times ("the orchestrator Reads `gate-results.txt` and inlines its full text into the spawn payload", lines 1339/1344/1353). Auggie suggested promoting it to a standalone numbered step for a strictly-literal executor. The current wording is adequate; this is optional polish, not a defect.

## Architectural / Cross-Cutting Observations

- **Contract-reuse fidelity is genuinely high.** The three "reused VERBATIM" contracts were spot-checked at the byte level and all hold: DM-003 recommendation literal (em-dash preserved), the `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]` dedup_key shape, and the PR-02 halt strings (`Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and `[HALT-MONOTONICITY] |F|=<n>`). This is the strongest part of the PR.
- **P5 read-only fence is correctly placed and tested.** The "Pure-function invariant (P5 fence)" is the first paragraph of §5.3 (line 581, immediately after the heading at 579, before the compute sub-sections), and `test_p5_advisory_does_not_mutate_scored_tiers` enforces the read-only guarantee. The advisory reads `feedback-log.md` READ-ONLY and never mutates `tier_scores`.
- **`--spec` Input-Contract reconciliation landed cleanly and is behavior-preserving.** The Input Contract now states the roadmap is the *primary required* input with `--spec`/`--tdd-file`/`--prd-file`/auto-wired TDD-PRD as *optional supplementary* enrichment, with the roadmap as the final spec-resolution fallback — preserving roadmap-only baseline behavior (verified PR-head `SKILL.md:49-71`).

## Dropped findings (false positives — full transparency)

Five findings were dropped during grounding. Four were caused by Auggie indexing the reviewer's working tree (base branch `feat/recommend-minstar`) instead of the PR head, so it read pre-change content:

| Auggie finding | Reported sev | Why dropped |
|---|---|---|
| "Input Contract change didn't land; SKILL.md still says 'exactly one input'" | High | **Landed.** PR head `SKILL.md:49-71` has the full supplementary-inputs contract. Auggie read the base branch. |
| "Self-Check 17→20 fix incomplete; line 1729 still says 'all 17 checks'" | High | **Complete.** PR head lines 1266/1269/1732 all say "20 checks"/"20/20"; no `17 checks` remains. `test_self_check_count_is_20_not_17` guards it. |
| "P5 pure-function fence is after the §5.3 algorithm" | High | **Wrong.** The fence is the first paragraph of §5.3 (line 581), before the compute rules. |
| "F_k may double-count persistent synthetic-dnsp → non-convergence" | Medium | **Resolved by spec.** `SKILL.md:1581` defines `F_k` as the "post-dedup cardinality... it EXCLUDES `source: \"synthetic-dnsp\"` records." Excluded → contributes 0. `test_p2_excludes_synthetic_dnsp_from_fk` guards it. |
| "ValidationReport.md manual-review section template not shown" | Low | **Specified.** The `## Manual Review Required (synthetic-dnsp)` heading is named at `SKILL.md:1510` and `:1532`. |

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0); exit 0; ~2m44s wall.
- Findings dropped during grounding: 5 (4 stale-ref false positives + 1 already-specified).
- Independent verification: 125 affected tests run **green** on a PR-head worktree (`tests/tasklist/test_tasklist_cli.py` + `tests/skills/test_task_builder_merge.py`).
- Byte-level contract checks: DM-003 literal, dedup_key shape, PR-02 halt strings — all confirmed byte-exact vs task-builder source.
- Persona cross-check: disabled (depth=standard).
