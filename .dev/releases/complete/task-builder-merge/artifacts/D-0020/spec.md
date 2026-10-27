# D-0020 — Degradation Rule + Hidden-Input Guard Spec

**Task:** T02.05 — Wire degradation rule + hidden-input guard
**Phase:** Phase 2 / Milestone M2 (FR-CONV.2 / PR-01)
**Roadmap rows:** R-038 (Degradation rule), R-039 (Hidden-input guard)
**Branch:** feat/sufficiency-challenge-and-branch-trace-mitigation
**Generated:** 2026-05-17
**Dependencies satisfied:** T02.01 (D-0016 PASS), T02.02 (D-0017 PASS); TB-Add-7 from Phase 1 (D-0015 PASS)

---

## 1. Scope

T02.02 (D-0017) wired the three DM-001 emitters (References / Source areas / Key constraints) and embedded omit-when-degraded language in each per-emitter rule. T02.05 promotes that embedded language into two named, standalone rules so producer behavior and consumer cross-validation are both unambiguous:

1. **R-038 — Degradation rule.** Define "minimal BUILD_REQUEST" operationally and require the Source areas and Key constraints bullets to be **physically absent** from the rendered block (not blank-but-present, not stub-bulleted).
2. **R-039 — Header-wide hidden-input guard.** Require a final `grep -cE "src/|/.*:[0-9]+"` scan over the entire block range (heading line through closing `---`), uniformly applied to the fully-populated and degraded forms. The Source-areas-only guard from T02.02 catches one path-leak source; this header-wide guard is the boundary check that catches BUILD_REQUEST-derived leaks in References (verbatim GOAL / WHY text) and Key constraints (verbatim invariant text).
3. **TB-Add-7 tolerance.** Update the rf-qa cross-validator to explicitly emit `tb-add-7-degraded-tolerated` (not FAIL) when the block is present but the `**Source areas:**` line is absent.

## 2. Implementation Locations

| Surface | Line range | Change |
|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | 942–973 (new "Degradation rule (R-038 …)" + "Header-wide hidden-input guard (R-039 …)" paragraphs replacing the prior compact 2-sentence degradation note at the old 942–944 range) | Replaced the textual hint with two named rules carrying explicit emit/omit semantics, an operational definition of "minimal BUILD_REQUEST," and the post-assembly grep-scan procedure with one allowed rewrite cycle and a `header-leak-suppressed` fallback annotation. |
| `src/superclaude/agents/rf-qa.md` | 308 (TB-Add-7 paragraph extended in place) | Added the `tb-add-7-degraded-tolerated` verdict for the References-only form; added a consumer-side spot-check re-run of the R-039 grep with explicit FAIL behavior on hit. |
| `.claude/skills/task-builder/SKILL.md` and `.claude/agents/rf-qa.md` | mirrors | `make sync-dev` ran post-edit; `make verify-sync` PASS. |

**Venue note (consistent with D-0017 § 2):** R-038 / R-039 are codified in the task-builder SKILL.md spawn-prompt body, adjacent to the per-emitter rules from T02.02 (`SKILL.md:898–932`) and the wrapper template from T02.01 (`SKILL.md:1561–1568`). The `rf-task-builder` agent reads this body at spawn time, so behavior is consumed per the roadmap's intent (R-038 / R-039 list `rf-task-builder.md` as the venue; consolidation in SKILL.md mirrors the T02.02 deviation rationale).

## 3. The Two Rules (verbatim summary)

### 3.1 R-038 — Degradation rule

- **"Minimal BUILD_REQUEST" definition (operational):** GOAL is the only populated rollup-signal field. WHY may be empty or duplicate GOAL; `related_docs` is empty; `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` are absent; fewer than 3 distinct source areas are inferable across all research files.
- **Required output:** a single `**References:**` bullet. The Source areas and Key constraints bullets are **absent** from the rendered block (not present-and-blank, not stub-bulleted).
- **What stays:** the `## Execution Context` heading and the `<!-- OPTIONAL header ... -->` reader-aid comment.
- **What goes:** the two omitted bullet lines are physically gone from the output.
- **Truly-empty fallback:** if even GOAL-derived References cannot be produced, OMIT the entire block (heading included).

### 3.2 R-039 — Header-wide hidden-input guard

- **Trigger:** post-assembly — after all three emitters have run and the candidate block is assembled, but before the block is committed to the task file.
- **Range:** from the `## Execution Context` heading line through the next `---` separator line, inclusive.
- **Check:** `grep -cE "src/|/.*:[0-9]+"` against that byte range MUST return 0.
- **Coverage uniformity:** applies identically to the fully-populated 3-bullet form and to the degraded References-only form. The Source-areas-only guard at `SKILL.md:913–921` is a first-line defense for that specific bullet; R-039 is the boundary check that catches leaks in References (verbatim GOAL / WHY) or Key constraints (verbatim invariants).
- **On hit (count ≥ 1):** rewrite the offending bullet to remove the path / `:NN` reference (e.g., a GOAL line mentioning `src/foo/bar.py:42` becomes "the foo module" or "the bar handler"), re-run assembly, re-scan. **Allow at most one rewrite cycle.** If the second scan still hits, OMIT the entire block and surface a `header-leak-suppressed` annotation in the builder's return value.

## 4. TB-Add-7 Cross-Validator Tolerance (D-0015 integration)

Updated `src/superclaude/agents/rf-qa.md:308`:

- **When Source areas bullet is PRESENT:** unchanged behavior — every named source area MUST reappear in at least one item's Context field, else FAIL.
- **When Source areas bullet is ABSENT but the block is present (References-only degraded form):** the cross-validation has no source-area set to check. Emit verdict `tb-add-7-degraded-tolerated` and **do not FAIL**. This is the intended R-038 degradation.
- **When the entire block is absent (no heading):** unchanged — surface `tb-add-7-inactive` annotation.
- **Key constraints bullet:** irrelevant to TB-Add-7 (it cross-validates Source areas only).
- **Hidden-input spot check:** TB-Add-7 may additionally re-run the R-039 grep against the block range as a consumer-side spot check, FAILing if count > 0. This is producer-then-consumer defense-in-depth.

## 5. Acceptance Criteria (per phase-2-tasklist.md L242-246)

| # | Criterion | Verification |
|---|-----------|--------------|
| AC1 | Minimal-BUILD_REQUEST fixture generates header with only `References:` line; Source areas and Key constraints lines absent (not blank-but-present) | `evidence.md` § 2 — grep counts: Source areas = 0, Key constraints = 0, References = 1 against `sample-minimal-buildrequest.md` block range |
| AC2 | `grep -cE "src/|/.*:[0-9]+" <header-range>` returns 0 on the minimal fixture | `evidence.md` § 3 — grep count = 0 |
| AC3 | TB-Add-7 cross-validator tolerates the degraded form (no FAIL emitted) | `evidence.md` § 4 — TB-Add-7 rule text at `rf-qa.md:308` cited; verdict `tb-add-7-degraded-tolerated` documented |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0020/evidence.md` | `evidence.md` present |

## 6. Regression Coverage — Fully-populated form unaffected

The R-039 header-wide grep also runs on the T02.02 fully-populated sample (`artifacts/D-0017/sample-emitter-output.md`); count = 0. Source areas and Key constraints bullets remain present (counts = 1 each). The new R-039 guard is therefore strictly additive — no existing PASS becomes a FAIL.

## 7. Producer / Consumer Contract Reference

- **Producer:** `rf-task-builder` agent (SKILL.md spawn-prompt body, R-038 + R-039 paragraphs).
- **Consumer:** `rf-qa` agent via TB-Add-7 (degraded-tolerated verdict) + optional consumer-side R-039 grep spot check.
- **Schema:** DM-001 v1.0.0 frozen at T01.13 (D-0011 § 1). R-038 + R-039 are derivation rules over the same DM-001 fields — schema unchanged.
- **Wrapper template:** MDTM Output Structure at `SKILL.md:1561–1568` (T02.01 / D-0016) — unchanged.

## 8. Rollback

Per roadmap (R-038, R-039): revert the two new paragraphs at `SKILL.md:942–973` and revert the TB-Add-7 paragraph extension at `rf-qa.md:308`. The T02.02 per-emitter degradation hints (embedded language at `SKILL.md:874–877`, `:888–891`, `:899–901`) remain operational as fallback; behavior degrades to T02.02 baseline (per-emitter omit semantics with no header-wide guard or explicit TB-Add-7 tolerance verdict).

## 9. Cross-References

- DM-001 frozen contract: `artifacts/D-0011/spec.md` § 1
- FR-CONV.2 wrapper landing: `artifacts/D-0016/spec.md`
- DM-001 emitters: `artifacts/D-0017/spec.md` + `artifacts/D-0017/sample-emitter-output.md`
- TB-Add-7 cross-validator origin: `artifacts/D-0015/` (Phase 1)
- Phase 2 tasklist row: `phase-2-tasklist.md` L206–254 (T02.05)
- Roadmap M2 rows R-038 / R-039: `roadmap.md` L170–171
