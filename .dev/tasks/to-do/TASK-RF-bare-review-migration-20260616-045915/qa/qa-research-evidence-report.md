# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Corrective MDTM tasklist for sc-bare-review M8/M9 migration
**Date:** 2026-06-16
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS

All 5 assigned research files are evidence-dense, every priority spot-check confirmed
against real source, and no CRITICAL or IMPORTANT evidence defects found. Two MINOR
nits (off-by-one line counts) do not affect the migration plan. No gaps that would
cause synthesis to hallucinate.

> [PARTITION NOTE: This is partition coverage of files 01-05 (the full assigned set
> for this lens). Cross-file contradiction checks were applied across all 5 assigned
> files; no merge with other partitions needed — this lens covers the whole research dir.]

---

## Priority Spot-Checks (all CONFIRMED against real source)

| # | Claim (file) | Verification | Result |
|---|---|---|---|
| P1 | R2 B-5: inline `run_cmd` calls only `dispatch_wave1`, NOT normalize/reduce/emit_contract | Read commands.py:1554-1578 — `dispatch_wave1(preflight_result, transport_for_slot=…, logger=logger)` with NO `prompt=`/`worker_spec=`; L1569-1577 is an explicit "Return-contract emission stub -- M5 replaces this". grep confirms `normalize_wave2`/`reduce_wave3` only at L1781/1788/1952/1977 (resume branch); `emit_contract` never called in commands.py. | CONFIRMED |
| P2 | R2 B-1..B-4: `swarm run` lacks `--reviewers`/`--target-line-cap`/`--timeout-sec`/`--label` | Read decorator stack commands.py:1181-1303 (9 options + 1 positional). Negative grep for those 4 flag strings returns ZERO matches. | CONFIRMED |
| P3 | R3: parity test has whole-module `skipif(not LEGACY_SCRIPT.exists())` guard + compares library surfaces | Read test_bare_review_parity.py: `pytestmark = pytest.mark.skipif(not LEGACY_SCRIPT.exists(), …)` present; imports `BareReviewV1` + `determine_status` + `LENSES` (lib-level, no CliRunner); `LEGACY_SCRIPT` resolves to `…/sc-bare-review/scripts/t2_normalize.py`. | CONFIRMED |
| P4 | R4: release-notes "~60-line thin caller" claim is FALSE; SKILL.md=231 lines | Read release-notes-v1.md:16-26 — present-tense "is now a ~60-line thin caller" verbatim. `wc -l SKILL.md` = 231. scripts/ still holds t2_dispatch.sh + t2_normalize.py + t2_preflight.sh. [CODE-CONTRADICTED] tag is correct. | CONFIRMED |

### Additional corroborating spot-checks (broadening past 20%)

| Claim | Verification | Result |
|---|---|---|
| R2 §2 lens field values | bare_review.py:40-75 — `default_workers=3`, `default_target_line_cap=4000`, `suspect=True`, `recipe_name`/`normalizer_strategy="bare-review-v1"` all match | CONFIRMED |
| R3 §2.1 CliRunner pattern | test_e2e_user_guide.py:68-70 `_run(runner,*args)=runner.invoke(swarm_group,…)`; bare-review stub run + `"dispatched job (mode=lens, workers=3, results=3)"` assertion present | CONFIRMED |
| R3 §3.3 dispatch-only pin | `test_quickstart_does_not_emit_m5_artifacts` exists at L104, pins NO merged.md/return-contract.yaml/done.json — independently corroborates B-5 | CONFIRMED |
| R4 §3 lens-contribution-policy | `docs/dev/lens-contribution-policy.md` = 515 lines; `docs/swarm/lens-contribution-policy.md` ABSENT → RELOCATE/cross-ref classification correct | CONFIRMED |
| R5 §2.1 MIG-001 pre-commit hook | .pre-commit-config.yaml:117-124 — `verify-bare-review-mirror-matches-src`, `files: '^src/superclaude/skills/sc-bare-review/'` present | CONFIRMED |

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (all Complete + Summary) | PASS | R1 "Status: Complete" +§4 summary; R2 "Status: Complete" + Net findings; R3 "Status: Complete" + Summary (note: line 3 header still says "In Progress" — see MINOR-1); R4 "Status: Complete" + §summary; R5 "Status: Complete" + §5 summary |
| 2 | Evidence density (file:line on every claim) | PASS — Dense (>80%) | Every claim in all 5 files carries explicit file:line. Spot-checked P1-P4 + 5 corroborating; all resolved to real lines. R2/R3 are exhaustively cited; R1's KEEP/DROP table cites SKILL.md line ranges; R4 tags every doc claim [CODE-VERIFIED]/[CODE-CONTRADICTED] |
| 3 | Scope coverage (key files discussed) | PASS | All 5 lens areas covered: SKILL.md+scripts (R1), swarm CLI surface (R2), parity tests (R3), docs (R4), MDTM template+sync (R5). No unexamined key file in scope |
| 4 | Doc cross-validation (tags + verify) | PASS | R4 systematically tags every doc-sourced claim. The load-bearing [CODE-CONTRADICTED] (release-notes thin-caller) independently re-verified false (231 lines, scripts present) |
| 5 | Contradiction resolution | PASS | No unresolved cross-file contradictions. R1 (231→~60 migration plan) and R4 (231 actual = staleness defect) are consistent: R4 explicitly defers SKILL.md authority to R1 (R4:96). R2 (B-5 inline gap) and R3 (§3.3 dispatch-only blocker) agree and cross-reference each other |
| 6 | Gap severity (all gaps surfaced) | PASS | Gaps are surfaced as actionable migration blockers (B-1..B-5, parity-self-deactivation, M5 dependency, 0/6 OPS docs). These are findings the tasklist must address, not research gaps — research itself is complete |
| 7 | Depth appropriateness (end-to-end trace) | PASS | R2 §4 traces the inline `run_cmd` data flow end-to-end (steps 1-12) with the exact gap (no prompt/worker_spec, no normalize/reduce). R3 traces the parity test composition end-to-end |
| 8 | Integration point coverage | PASS | Lens→recipe→normalize→reduce→contract integration documented (R2 §2-4); SKILL.md→swarm CLI flag mapping (R2 §1); sync/verify hook integration (R5 §2); cross-skill caller wiring (R1 §1.3) |
| 9 | Pattern documentation | PASS | MDTM template B2/L-patterns/M3 gate (R5 §1); swarm test CliRunner convention (R3 §2); normalization domain semantics / SEV_ALIASES parity surface (R1 §2.3, R2 §3) |
| 10 | Incremental writing compliance | PASS | Files show structured growth (numbered sections, per-claim evidence, builder-summary tails). R3 header "In Progress" remnant (MINOR-1) is actually a sign of incremental authoring, not a one-shot |

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Priority spot-checks confirmed: 4 / 4 + 5 corroborating
- CRITICAL issues: 0
- IMPORTANT issues: 0
- MINOR issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | 03-parity-and-swarm-test-conventions.md:3 vs :205 | Header says **"Status: In Progress"** at line 3 while line 205 says "Status: Complete". Stale header line; file is in fact complete. | Update line 3 to "Status: Complete" for consistency. Does not block the builder. |
| 2 | MINOR | 03 (`:13`) and R5 (`:310`) cite `test_bare_review_parity.py` as **795 / 17 tests**; actual `wc -l` = **794 lines** | Off-by-one line count (795 vs 794). The 17-test collection count is plausible and not re-counted, but the line figure is 1 off. Immaterial to the design (the test composition claims, skipif guard, imports, and assertion line numbers all verified correct). | None required for the builder; note for precision. The cited internal line numbers (e.g. :217-224 guard, :97-100 imports) all resolved correctly, so the 794-vs-795 discrepancy is cosmetic. |

Neither MINOR issue affects the migration plan, introduces a hallucination risk, or
changes any builder-facing decision. Per research-gate policy, MINOR issues are still
listed; however both are cosmetic metadata nits on file 03, not evidence defects in the
substantive findings. Recommend the builder proceed; optionally have file 03's header
line corrected.

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 8 (incl. wc/ls/grep/sed verifications)
- No web research performed (all claims intrinsically local source-bound).
- Every checklist item marked VERIFIED cites specific tool output above (file:line reads
  + bash grep/wc/ls results). Tool-call count (15) exceeds checklist item count (10) +
  priority spot-checks — engagement minimum satisfied.

---

## Recommendations

1. **Green light for synthesis / tasklist build.** Research is evidence-dense and the
   five migration blockers (B-1..B-5), the parity-gate self-deactivation hazard, the M5
   dependency, and the 0/6 OPS-docs gap are all documented with verified file:line
   anchors a builder can act on directly.
2. **Optional polish (non-blocking):** fix file 03's line-3 "In Progress" → "Complete"
   and note the 794-line parity-test figure.
3. **Builder must preserve the cross-file dependency R2↔R3 surfaced:** the permanent CLI
   parity gate (R3 §4) is hard-blocked on R2/M5 wiring normalize+reduce onto the inline
   `swarm run` path. This is correctly flagged in both files; the tasklist must encode it
   as an L5 conditional/sequencing dependency, not parallelize them.

---

## QA Complete

**VERDICT: PASS** — 10/10 checks passed, 4/4 priority spot-checks confirmed, 0 CRITICAL,
0 IMPORTANT, 2 MINOR (cosmetic, non-blocking). Research is evidence-grade and ready to
drive the corrective MDTM tasklist build.
