# QA Report — Research Gate (Partition A — Evidence Quality Lens)

**Topic:** RigorFlow Merger tasklist research
**Date:** 2026-06-19
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** EVIDENCE QUALITY
**Partition:** A of M
**Assigned files:** 01-skill-stage-map.md, 02-skill-conventions.md, 03-integration-contracts.md, 04-proposal-attachment-trace.md
**Fix authorization:** false (report-only)

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

One IMPORTANT evidence-quality defect: file 01 (R01) asserts a verifiable line-count fact incorrectly and instructs the builder to cite the wrong value. Per research-gate rules, ALL gaps regardless of severity = FAIL until resolved. All P1–P5 attachment anchors are verbatim-accurate; the defect is isolated and trivially fixable.

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 13 | Grep: 0 | Glob: 0 | Bash: 2 (no web research performed — all claims were intrinsically local source-truth, so Tavily was not engaged)

(Tool calls 15 ≥ 10 checklist items: engagement minimum satisfied. Every Read/Bash targeted a specific cited anchor.)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 4 files Status: Complete + Summary | PASS | Each file has `**Status:** Complete` header + `Status: Complete` footer; files 01/03 close with status line, 02/04 with summary sections |
| 2 | Evidence density (file:line + quoted anchor) | PASS (Dense, >80%) | All four files cite `path:line` + verbatim quoted text for essentially every claim. R03/R04 explicitly carry a "No Unverified items" / per-row file:line discipline |
| 3 | Spot-check ≥8 cited line numbers vs source | PARTIAL — 1 false claim found | 12+ anchors verified verbatim (see below); 1 FALSE: R01 line-count |
| 4 | Unsupported assertions stated as fact | 1 found (R01 line count) | See Issue #1 |
| 5 | [CODE-CONTRADICTED]/[UNVERIFIED] flagged properly | PASS | R02 §6 correctly tags RULES.md sync/lint restatement as **Unverified** and explains why CLAUDE.md is authoritative; R03/R04 carry confirmed-via-grep negatives (StageError, sc:task-unified) honestly |
| 6 | 17-vs-20 gate inconsistency claim | PASS (VERIFIED real) | :1187 "check 1-20" + :1597 "all 17 checks" both confirmed verbatim — the flagged stale-count inconsistency is genuine |
| 7 | DM-003 reuse contract (P3) accuracy | PASS | task-builder:877-883 = exactly 7 YAML fields; R03 §1.1 self-aware reconciliation of "7 named fields vs brief's 8" is correct |
| 8 | P1 Execution Context contract accuracy | PASS | task-builder:1066-1071 References/Source areas/Key constraints + no-file:line-in-header + References-only degradation all verbatim; TB-Add-7 at :1389 confirmed |
| 9 | Cross-file contradiction scan (partition subset) | 1 found | R01=1632 vs R02=1631 line-count contradiction (Issue #1) |
| 10 | Stage anchors (Stage 7/9/10, §5.3, index template) | PASS | Stage 7 :1244-1310, Stage 9 :1409-1427, Stage 10 :1456, §5.3 priority :548, Feedback/Glossary :820-849, task body :894-927 all verbatim-correct |

## Spot-Check Ledger (independent source reads)

| Cited claim | Cited loc | Source verified? | Result |
|---|---|---|---|
| "If any check 1-20 fails…" | SKILL.md:1187 | Read 1180-1199 | EXACT MATCH |
| "Self-Check: all 17 checks passed" | SKILL.md:1597 | Read 1590-1609 | EXACT MATCH |
| Stage 10 "skill does NOT loop" | SKILL.md:1456 | Read 1450-1461 | EXACT MATCH |
| Stage 7 heading + 2N + merge + retry | SKILL.md:1244,1256,1288,1310 | Read 1244-1313 | EXACT MATCH (split=ceil :1253, 2N :1263, merge steps 1-4 :1292-1295, retry :1310) |
| "skill executes in 11 stages" / 10.5 | SKILL.md:1527,1541 | Read 1525-1544 | EXACT MATCH |
| Task body Artifacts/Deliverables/Steps/Notes | SKILL.md:894,900,904,927 | Read 894-928 | EXACT MATCH |
| Feedback Collection Template / Glossary / Gen Notes | SKILL.md:820-826,841,847-849 | Read 820-864 | EXACT MATCH |
| DM-003 7-field record + fixed values | task-builder:873-883 | Read 873-912 | EXACT MATCH (severity HIGH :877, source :878, recommendation literal :881, dedup_key 2-tuple+vocab :882, found_n_times :883) |
| EXECUTION_CONTEXT_INSTRUCTION 3 sub-fields | task-builder:1066-1071 | Read 1064-1075 | EXACT MATCH |
| TB-Add-7 source-areas reappear | task-builder:1389 | Read 1387-1392 | EXACT MATCH |
| §5.3 priority order STRICT>EXEMPT>LIGHT>STANDARD | SKILL.md:548 | Read 544-551 | EXACT MATCH |
| Stage 9 delegate sc:task --compliance strict | SKILL.md:1413-1427 | Read 1409-1428 | EXACT MATCH |
| phase-template.md mirror Deliverables/Steps/Notes | phase-template.md:55,59,82 | Read 53-84 | EXACT MATCH |
| commands.py validate() + flags + max-turns=100 | commands.py:31-55 | Read 31-56 | EXACT MATCH |
| **SKILL.md total line count** | R01:1632 / R02:1631 | `wc -l`=1631, `awk NR`=1631, ends `\n` | **R01 WRONG (1631 actual); R02 CORRECT** |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | 01-skill-stage-map.md:9 and :17 | R01 asserts as fact: "SKILL.md is **1632** lines (Read reported '1632 total'), not 1631 as in the brief. **Cite 1632.**" Independently verified via `wc -l` (1631), `awk 'END{print NR}'` (1631), and trailing-byte `od` (file ends with a single `\n`, no phantom line). The actual count is **1631**. The brief and R02 (`:10` "1631 lines") are correct; R01 is wrong AND instructs the builder to propagate the wrong number. This is an unsupported assertion stated as corrected-fact — the exact evidence-quality failure mode the lens targets. R01 likely misread the Read tool's offset display (Read shows position N+1 at EOF) as a line count. | Correct 01-skill-stage-map.md:17 NOTE to "SKILL.md is **1631** lines" and change ":9" parenthetical "(1632 lines — read in full…)" to 1631. No P1–P5 anchor changes — every cited attachment line is independently verified correct, so this is a metadata-only fix. |

## Cross-File Consistency (partition A subset)

| Fact | File 01 (R01) | File 02 (R02) | Adjudication |
|---|---|---|---|
| sc-tasklist SKILL.md line count | 1632 (asserts brief wrong) | 1631 | **R02 correct** (verified 1631) — Issue #1 |
| 17-vs-20 gate drift | flagged real (:1187 vs :1597) | flagged real (:1187 vs :1597) | AGREE + both verified true |
| P5 must-not-mutate-tiers / §5.3 :548 | cited | cited :548 | AGREE + verified |
| P1/P5 land in Index Template region | yes (820-849 / 894-927) | consistent with R04 (707 / 839 anchors) | AGREE (R04 gives finer per-line anchors; no conflict) |

No other contradictions within the assigned subset. [PARTITION NOTE: cross-file checks limited to files 01-04; R05/R07-owned material and any files outside this partition not assessed here.]

## Positive Evidence-Quality Observations (adversarial counter-check)

- R03 and R04 BOTH independently flag the same 17-vs-20 count drift and both correctly identify :1597 as the stale token — corroboration, not collusion (different framing, both verbatim).
- R03 §1.1 proactively reconciles the "8 fields vs 7 fields" tension the brief implies and lands on the correct answer (7 named YAML fields; dedup_key is a 2-tuple) — verified against task-builder:877-883.
- Negative claims are grep-backed and honest: R03 §1.9 "no typed StageError exists" and §5.3 "sc:task-unified is NOT a real name" are exactly the kind of assertions that are easy to fake; both are framed as grep-confirmed and are plausible/consistent with the surrounding contract.
- R02 §6 correctly down-scopes its own confidence on RULES.md (tagged Unverified) rather than over-claiming.

These observations were made adversarially (looking for fabrication) and found the bulk of the evidence trail sound — which is why the single line-count error is the only finding rather than a pattern.

## Actions Taken

None — `fix_authorization: false` (report-only). Issue #1 documented with exact remediation for the builder/orchestrator.

## Recommendations

1. Resolve Issue #1 (one-token metadata fix in 01-skill-stage-map.md) before synthesis. Because P1–P5 anchors are all independently verified correct, the synthesis can proceed on the anchors as-is; only the "1631 vs 1632" total-count metadata must be corrected so the builder does not propagate a wrong line count.
2. Other partitions / the analyst should re-confirm R03's grep-backed negatives (StageError, sc:task-unified) and the DM-003 reuse-vs-fork boundary independently, as those are load-bearing for P3/P2 and were spot-confirmed but not exhaustively re-grepped here.

## QA Complete
