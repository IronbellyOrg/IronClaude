# Merge Log

## Metadata
- Base: Variant 1 (qwen3.6-plus)
- Executor: sc:adversarial merge (in-context)
- Changes planned: 8 / applied: 8 / failed: 0 / skipped: 0
- Status: success
- Merged output: `../merged-audit.md`
- Timestamp: 2026-07-07

## Changes Applied

| # | Change | Status | Provenance tag | Validation |
|---|--------|--------|----------------|------------|
| 1 | AUD-1 terminal-gate → MINOR reconciliation | ✅ applied | `<!-- Source: adjudicator (A-001/A-002) + qwen F1 + glm C1 -->` | Cross-checked vs task L476/L482/L484/L535 |
| 2 | AUD-2 verification-round skip | ✅ applied | `<!-- Source: glm C2 — CONFIRMED via qa/ dir listing -->` | `qa-final-verification-*.md` absent confirmed |
| 3 | AUD-3 test-count drift (merged) | ✅ applied | `<!-- Source: qwen F3 + glm I2 -->` | vs L123/L410/L436/L478/L500/L501/L512 |
| 4 | AUD-4 aienv.py scope drift | ✅ applied | `<!-- Source: glm I1 — CONFIRMED via git diff -->` | `git diff --stat` = 1 file, 1±1 |
| 5 | AUD-5 additive-only VERIFIED | ✅ applied | `<!-- Source: qwen F4 + git verification -->` | `contract.py`+`models.py` 0-diff |
| 6 | AUD-6 xpass follow-up | ✅ applied | `<!-- Source: glm I4 -->` | vs L500/L567 |
| 7 | AUD-7 sync-dev → WARN | ✅ applied | `<!-- Source: glm I5 (supersedes qwen F2) -->` | vs L130/L509 |
| 8 | AUD-8 coverage/tcs → LOW | ✅ applied | `<!-- Source: adjudicator (supersedes glm C3) -->` | vs L22/L24/L28 |

## Post-Merge Validation
- **Structural integrity:** ✅ Pass — H1→H2→H3 hierarchy consistent; no orphaned sections.
- **Internal references:** Total 9, Resolved 9, Broken 0 (all AUD-N ids + task line refs resolve).
- **Contradiction re-scan:** New contradictions introduced by merge: 0. The base's two internal contradictions (qwen F2 "violation" vs glm I5 WARN; absent-C2) are resolved, not carried.
- **Suspect-source provenance:** every CONFIRMED finding carries a filesystem/git citation; every DOWNGRADE/REJECT carries the counter-evidence line.

## Summary
Planned 8 / applied 8 / failed 0 / skipped 0. Merge upgraded the audit from two individually-untrustworthy suspect-source reviews (one truncated + over-reaching, one missing the top catches) into a single evidence-verified report whose verdict (CONTINUE — non-blocking) differs from **both** input verdicts (`FAIL` / `CONDITIONAL FAIL`).
