# QA Report — Synthesis-Gate Fix-Cycle Content Verification (FR-DRS TDD)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep
**Date:** 2026-06-21
**Phase:** fix-cycle (content-verify of 5G.8 fixes S-1..S-6)
**Fix cycle:** 1 (verification only — `fix_authorization: FALSE`)
**Stance:** Adversarial — assumed the applied fixes introduced a semantic inconsistency or broke cross-section narrative.

---

## Overall Verdict: FAIL

The three substantive fixes (S-1 eval-case split, S-2 forbid-list de-conflation, S-3 FR-006 split) are
**semantically correct and code-grounded in the three S-3-named target files** (synth-02, synth-03 §6.3,
synth-09 §23). BUT the FR-006 split was **not propagated to three parallel sections** that restate AC-4
verbatim, leaving a genuine internal contradiction inside synth-09 (§23 vs §24.1) and residual
present-tense "sprint executor reads the deterministic scalars" goal/success/DoD claims in synth-01 and
synth-05. Per Critical Rule #6 a contradiction is never MINOR.

## Items Reviewed
| # | Check (spawn axis) | Result | Evidence |
|---|--------------------|--------|----------|
| a | FR-006 split semantically coherent across synth-02 / synth-03 §6.3 / synth-09 §23; no residual "executor reads today" | **FAIL** | Named-3 files correct; residuals in synth-09 §24.1, synth-01 G4+metric, synth-05 §11.1 (see I-1..I-3) |
| b | Eval-case 5-row split correct (41=test-only-ref count host; 39=dynamic-dispatch degraded/reg0; 37=FAIL-pre/PASS-post reg1); matches all 3 files | **PASS** | synth-01:150-156, synth-02:30, synth-05:119-125 all render 5 distinct rows; matches research/04:92-122,176-180 exactly |
| c | Forbid-list de-conflation accurate (observed vs SKILL overlap only on `runtime_surface_reachable`) | **PASS** | synth-01:76 vs research/00 §3:47-49 (observed) and research/03 §1.1:45-46 (SKILL); overlap = `runtime_surface_reachable` only |
| d | Fixes did not break problem→req→arch→data→testing narrative; nothing aspirational presented as shipped | **PASS (with caveat)** | Architecture/data correctly tag module as DESIGNED/SPEC; executor.py code-fact verified true. Caveat folded into axis (a) residuals |
| e | FR-count math after split | **PASS** | synth-02: 14 FR + 1 deferred FR-006a, itemized correctly (MH 11 / SH 2 / Deferred 1) |
| f | FR-006a code claim ("executor imports TurnLedger for budget only, reads no reflect contract") | **PASS** | Live grep: executor.py:42 imports TurnLedger (budget gates only); zero `runtime_surface`/`return-contract` in all of cli/sprint/ |

## Summary
- Checks passed: 5 / 6 axes (a FAILs)
- Checks failed: 1 axis (a — FR-006 split coherence incomplete)
- Critical issues: 0
- Important issues: 1 (I-1, intra-file contradiction synth-09 §23 vs §24.1)
- Minor issues: 3 (I-2, I-3, I-4)
- Issues fixed in-place: 0 (verification-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I-1 | IMPORTANT | synth-09 §24.1 line 193 (Definition of Done, AC-4 checkbox) | Lists the **unmodified** AC-4 ("§5.3 pre-filter AND `sprint run` executor read the deterministic scalars") as a release-gating DoD item. This directly contradicts the same file's §23 Phase 2 exit criterion (line 161, an S-3 fix target) which states the executor read is "**NOT** an exit criterion… FR-DRS v1 does not wire it (deferred FR-006a)." Taken literally, v1 can never satisfy its own DoD because one DoD item is explicitly deferred. The S-3 fix touched §23 but left the parallel §24.1 DoD unreconciled. | Reword the §24.1 AC-4 checkbox to scope it to v1: "AC-4 (v1 scope) — the §5.3 forbid-STOP pre-filter reads the deterministic scalars; the `sprint run` executor read is deferred (FR-006a, net-new, not wired by this rollout)." Mirror synth-02:66 / synth-09:161 phrasing. |
| I-2 | MINOR | synth-01 §3.1 G4 (line 104) + §4.1 metric (line 144) | Restate AC-4 verbatim presenting the `sprint run` executor read as an **in-scope GOAL / measured metric** ("Wire the deterministic values into the consumers… `sprint run` executor read the deterministic scalars"). Contradicts synth-02 FR-006a (Deferred Non-Goal v1) and synth-01's own §3.2 Non-Goals scoping. | Append the deferred caveat to G4 and the metric row: "(§5.3 in-scope; sprint executor read deferred — FR-006a, not wired this rollout)." |
| I-3 | MINOR | synth-05 §11.1 Success Criteria (line 80) | "§5.3 pre-filter and sprint executor read the deterministic scalars (AC-4)" drops the `(spec)` marker that the **same flow's** step-6 (line 70) correctly carries ("sprint executor (spec) gates on…"). Intra-file inconsistency. | Add the marker to line 80: "§5.3 pre-filter reads the deterministic scalars; sprint executor read is deferred/SPEC-ONLY (AC-4, FR-006a)." |
| I-4 | MINOR | synth-02 §5.3 Gaps table G2 disposition (line 75) | "TDD must decide if executor wiring is in FR-DRS scope or deferred; FR-006 as written assumes the read path exists" is stale relative to the now-resolved split (decision was made: deferred → FR-006a). Defensible as a record of the research-surfaced open question, but the disposition column should reflect the resolution. | Update G2 disposition to: "RESOLVED — deferred to FR-006a (net-new integration, not wired v1)." Low priority; this is a gaps-log entry, not a live spec claim. |

## What was verified CORRECT (the fixes that held)
- **S-1 eval-case split** — all three named tables now render 5 distinct rows. Case identities match research/04 verbatim: 37 `uc2-unwired-surface-passes` (FAIL-pre/PASS-post, `unreached≥1` + **regression 1**), 38 `uc2-surface-positive-control` (unreached 0 / degraded false), 39 `uc2-surface-dynamic-dispatch` (`[project.scripts]` → degraded true, **regression 0**, DEGRADE never UNREACHED), 40 `uc2-surface-degraded-backend` (Grounding Gap, no STOP), **41 `uc2-surface-test-only-ref` = the count-invariant host**. The collapsed-4-row defect is gone. No file mis-assigns the count-invariant host or swaps the 37/41 regression semantics.
- **S-2 forbid-list de-conflation** — synth-01 §2.2 (line 76) now correctly separates the OBSERVED ad-hoc set (research/00 §3) from the SKILL explicit forbid-list (research/03 §1.1) and states they "overlap the observed set only on `runtime_surface_reachable`; the persistence is structural." Verified against both sources — exact.
- **S-3 in the three named targets** — synth-02 FR-006 (in-scope) / FR-006a (deferred) cleanly split; synth-02 AC-4 coverage row (line 66) correctly scopes in-scope vs deferred; synth-03 §6.3 (line 96) correctly frames the executor as "Deferred (SPEC-ONLY)… NOT a live reader… NOT wired by this rollout"; synth-09 §23 Phase 2 exit (line 161) correctly excludes the executor read.
- **Code-fact grounding** — `executor.py:42` imports `TurnLedger` for budget gates only; **zero** `runtime_surface`/`return-contract`/`reflect` references across all of `src/superclaude/cli/sprint/`. The deferred framing is factually true in live source, not aspirational.
- **Narrative spine** — problem (prose-only can't emit) → requirements (FR-001..013 + deferred FR-006a) → architecture (DESIGNED/SPEC tagged, not presented as shipped) → data (synth-04 SPEC-ONLY tags on the executor consumer) → testing (synth-07 AC-4 notes "sprint executor is SPEC-ONLY today") is coherent. The module is consistently described as greenfield/DESIGNED everywhere; nothing aspirational is presented as merged.

## Self-Audit
**(a) Reliance list — structural items NOT re-checked (no Inherited Structural Verdict block supplied; standalone mode):**
- None relied on — operated standalone; independently re-verified every content claim with tools below.

**(b) Independent semantic checks (≥1 required, INV-019):**
- FR-006 split coherence — verified by `grep -rniE "sprint.*read|executor.*read"` across all 9 synth files (15 hits triaged into correctly-deferred vs residual present-tense), cross-read against synth-09:161 vs synth-09:193 to surface the intra-file §23↔§24.1 contradiction (I-1).
- Eval-case identity — verified by Read of all three tables + `grep` of research/04:92-122,176-180 (case→fixture→expected-verdict mapping).
- Forbid-list de-conflation — verified by `grep` of research/00 §3:47-49 (observed) and research/03 §1.1:45-46 (SKILL forbid-list); computed the overlap set = `{runtime_surface_reachable}`.
- FR-006a code-fact — verified by live `grep` of `src/superclaude/cli/sprint/executor.py` + package-wide token sweep (would have been impossible to confirm from synth text alone; required own tool work).

**Confidence:** Verified: 6/6 axes | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (of axes); verdict FAIL is evidence-driven, not low-confidence.
**Tool engagement:** Read: 7 | Grep/Bash-grep: 7 | Glob: 0 | Bash(other): 2
**Web research:** none performed (all verification local-file/source-bound); Tavily not invoked — no external lookup required.

## Recommendations
1. Apply I-1 (IMPORTANT) before assembly — the §23↔§24.1 contradiction is the load-bearing residual; an assembler copying §24.1 verbatim into the final TDD's Definition of Done ships an unsatisfiable release gate.
2. Apply I-2, I-3 (MINOR) for cross-section consistency so every AC-4 restatement carries the deferred caveat (synth-01 G4/metric, synth-05 §11.1 success-criteria). These are the same single defect (un-propagated FR-006 split) in three more places.
3. I-4 (MINOR) optional — update the synth-02 G2 gaps-log disposition to "RESOLVED → FR-006a."
4. Root cause for the fix-author: S-3's "Affected synth file(s)" column scoped the fix to three files, but the AC-4-verbatim string lives in six places. A `grep "sprint.*executor.*read"` sweep after any FR-split fix would have caught all residuals in one pass.

## QA Complete
