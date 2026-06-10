# QA Report — Research Gate (Partition 2 of 2)

**Topic:** CLI wrapper `superclaude reflect run` — research quality gate
**Date:** 2026-06-08
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files (4):** research/05-frontmatter-writeback.md, research/06-taskbuilder-template-integration.md, research/07-test-patterns.md, research/08-reflect-invocation-degradation-semantics.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage, cross-references) limited to assigned subset. Full cross-file verification requires merging both partition reports.]

---

## Overall Verdict: PASS (with 1 IMPORTANT + 3 MINOR advisories — none block the builder)

All four assigned research files are Complete, evidence-dense, and their load-bearing claims independently verified against source. Every claim flagged for re-verification in the spawn prompt was confirmed TRUE against the actual source files. No fabrications, no unsupported assertions-stated-as-fact, no untagged doc claims. The two `[CODE-CONTRADICTED]` flags in file 06 are correctly raised and accurate.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (4 files, Status: Complete + Summary) | PASS | All 4 read end-to-end; each carries `**Status:** Complete` + a Summary/TL;DR section (05:1-5, 06:1-3+182, 07:3+297, 08:3+210) |
| 2 | Evidence density (file:line per claim) | PASS (Dense) | >90% of claims carry file:line. Spot-verified ~25 distinct citations (see checks 4-15); all resolved to real lines |
| 3 | Scope coverage (FR-3/5/6/7/8/9/11 in subset) | PASS | 05→FR-6/FR-7; 06→template/FR-3 inputs; 07→test/NFR-7; 08→FR-2/3/5/8/9/11. No assigned-subset gap |
| 4 | Doc cross-validation tags ([CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]) | PASS | File 06 tag tally (11 verified / 2 contradicted / 0 unverified) is accurate; every CODE-VERIFIED claim I re-checked held |
| 5 | Contradiction resolution | PASS | File 08 §8 surfaces 7 contradictions/flags; file 06 surfaces 2; all are real and correctly characterized (verified below) |
| 6 | Gap severity (any gap = FAIL) | PASS | No CRITICAL/IMPORTANT *research* gaps in subset. The IMPORTANT item below is an open seam the files themselves correctly flag, not a missing finding |
| 7 | Depth appropriateness (Deep: end-to-end trace) | PASS | File 08 §7+§9 traces contract→verdict→exit end-to-end; file 05 §4 traces read→splice→compare→replace |
| 8 | Integration point coverage | PASS | File 06 documents SKILL.md edit seams (L853-856, L1827+, L1994-1999, L2051, L2108); file 08 §9 documents the slash-prompt/argv boundary |
| 9 | Pattern documentation | PASS | File 05 documents atomic-write/splice/dumper patterns; file 07 documents 3 ClaudeProcess stub idioms + fixture layout |
| 10 | Incremental-writing compliance | PASS | All 4 show iterative structure (numbered sections, cross-references, tally tables appended) — not one-shot |
| 11 | _IndentDumper at cache.py:37-48 (file 05) | PASS | `class _IndentDumper(yaml.SafeDumper)` at L37; `increase_indent` at L47. Exact match |
| 12 | frontmatter.py parse-only/top-level-scalars (file 05) | PASS | `extract_frontmatter -> dict[str,str] \| None` at L90; `_TOPLEVEL_KEY_RE.match` skips indented lines; no serializer in 125-line file |
| 13 | Phase-N HALT item SKILL.md:1992-2006 (file 06) | PASS | Verbatim-accurate quote; item is penultimate before "N.X Update task status to Done" |
| 14 | Rule #19 + checklist L2051 hardcode `/sc:reflect` (file 06) | PASS | L2108 Rule #19: "handoff command uses `/sc:reflect`...MALFORMED if omitted"; L2051 checklist confirmed verbatim |
| 15 | TCS section L2114 + formula L2133 + O4 L2152 (file 06) | PASS | Header, `TCS = 3·S1+4·S2+2·S3+2·S4+5·S5+4·S6`, and O4 "POST gate depth ∈ {standard,deep}...NEVER quick" all exact |
| 16 | BUILD_REQUEST POST_REFLECT_GATE L853-856 (file 06) | PASS | `DEPTH: <max(tcs-derived depth, standard)>` confirmed at L855 |
| 17 | Template lacks start_commit/executor_model_class (file 06 CODE-CONTRADICTED ×2) | PASS | Frontmatter template L1925-1949 grep: only spec_path/reflect_post present; real example L55 carries `start_commit:` → contradiction is real |
| 18 | --allow-single-vendor/--timeout/--dry-run/--promote NOT reflect flags (file 08) | PASS | reflect.md Options table + SKILL grep: `--allow-single-vendor` appears ONLY as "v1.1 candidate hardening" (SKILL.md:1803), not a current flag; --timeout/--dry-run absent; bare --promote absent (only --no-promote/--promote-dry-run/-anyway/-mode/-resume exist) |
| 19 | status: stopped-precondition NOT in §9.1 enum (file 08) | PASS | SKILL.md:655 enum = `success \| partial \| failed \| dry-run`; grep for `stopped-precondition` in SKILL = exit 1 (no match); reflect.md:30 DOES claim it → contradiction real & correctly flagged |
| 20 | --executor-model real (SKILL.md:584) but absent from reflect.md table (file 08) | PASS | L584 documents the flag; reflect.md grep for `executor-model` = exit 1. Both halves confirmed |
| 21 | Alias routing table SKILL.md:219-224 + zero-aliases-tier2-conflict slug (file 08) | PASS | 5-row table verbatim; `stop_reason: "zero-aliases-tier2-conflict"` at L221 confirmed |
| 22 | contract_version 1.3.0 (file 08) | PASS | SKILL.md:651/654 confirm `contract_version: "1.3.0"` |
| 23 | Test precedent files exist (file 07) | PASS | test_cli_smoke.py / test_file_passing.py / test_e2e.py / test_suite_loader.py / test_ban_import_rule.py all exist; prd_group import at L11 confirmed |
| 24 | Makefile lint/format/test + no-mypy (file 07) | PASS | test:L13, lint:L48 (`ruff check .`), format:L53 (`ruff format .`); no mypy target |
| 25 | FR-11 routing table completeness vs spec (file 08 §6) | PASS | All spec FR-11 triggers (L31) mapped to contract field+value+anchor; exit codes match spec L77-82 exactly |
| 26 | Coverage gap: file 06 byte-identical halt-arm text | PASS (advisory) | Verbatim halt item IS quoted in §(a); reversible-edit §ptr-3 references "L1994-1999 BYTE-IDENTICAL" by line range (see MINOR-1) |
| 27 | Coverage gap: file 07 compare-mismatch→sidecar test | PASS | Verdict-matrix case #8 + §6 "Write-back specifics (case 7/8)" cover it |
| 28 | Coverage gap: file 08 complete FR-11 routing table | PASS | §6 14-row table + §6.1 NOT-halt exceptions = complete |

---

## Summary

- Checks passed: 28 / 28
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: ~30 (batched in 6 Bash calls) | Glob: 0 | Bash: 6 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 (no external-web claim required lookup — all claims are local-source-bound)

Tool-engagement note: 4 Reads (the 4 assigned files) + 6 Bash calls each running multiple targeted greps/seds = ~34 discrete verification actions against 28 checklist items. Above the tool-engagement minimum. Every claim flagged in the spawn prompt for re-verification was checked against source, not accepted from the research file's own assertion.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (advisory — does not block builder) |
|---|----------|----------|-------|--------------------------------------------------|
| 1 | IMPORTANT | 06 §(e), shared seam R02/R05/this track | `executor_model_class` frontmatter source is unresolved: the SKILL template emits NO `executor_model_class:` field, yet FR-3 expects `--executor-model` "from frontmatter/`EXECUTOR_MODEL_CLASS`". File 06 correctly flags this as a gap but does NOT resolve which source the wrapper reads. File 08 confirms reflect falls back env→commit-author-heuristic→`unknown` (fail-open, not STOP). | Builder must decide: (a) add `executor_model_class:` to the SKILL frontmatter template, OR (b) wrapper reads `EXECUTOR_MODEL_CLASS` env only. File 08 §1.1 + SKILL.md:584-586 show env fallback is safe (missing = fail-open WARN, never STOP), so option (b) is the lower-risk default. This is a DECISION the builder must make explicit, not a missing research finding. |
| 2 | MINOR | 05 §1, §7 | File 05 says frontmatter.py is "126 lines total" / "full read (126 lines)"; actual `wc -l` = 125. Off-by-one (likely trailing-newline counting). | Cosmetic; does not affect the parse-only conclusion. No action needed. |
| 3 | MINOR | 06 reversible-edit §ptr-3 | The `halt` arm is specified as "emit the current L1994-1999 item BYTE-IDENTICAL" by line-range reference; the verbatim text lives in §(a) (L1992-2006). A builder must cross-reference two sections to assemble the byte-identical halt arm. | Builder should copy the §(a) verbatim block as the halt arm. Adequate as-is; a single consolidated copy-block would be marginally cleaner. |
| 4 | MINOR | 06 §(a) note / 08 §9 | File 06's quoted POST command includes `--remediate`; the wrapper's synthesized invocation (08 §9 / spec §8 L119) does NOT include `--remediate`. Files don't explicitly reconcile whether the wrapper drops `--remediate` (the wrapper is audit-only by default per FR-9). | Non-blocking: spec §8 L119 is authoritative for the wrapper prompt (no `--remediate`); the manual `/sc:reflect` halt-arm path keeps `--remediate`. Builder should note the wrapper prompt deliberately omits `--remediate` (audit-only). Both files are internally correct; the seam is just unstated. |

---

## Actions Taken

None (fix_authorization: false — report-only).

---

## Recommendations

1. **Green-light synthesis for this partition.** All 4 files are builder-ready. The single IMPORTANT item (#1) is an unresolved DECISION the files correctly surfaced, not a research defect — it should be carried into synthesis Open Questions, not sent back for more research. The spec's FR-3 ("frontmatter/`EXECUTOR_MODEL_CLASS`") + file 08's fail-open finding already bound the answer space.
2. **Merge note for orchestrator:** this is Partition 2 of 2. Cross-file contradiction/coverage checks were limited to files 05-08. The `executor_model_class` seam (#1) and the `start_commit` source seam touch R02 (contract) which is in Partition 1 — confirm Partition 1's report addresses the contract-side of those fields before final research-gate verdict.
3. No fabrication, no hallucinated paths, no untagged doc claims detected in the assigned subset.

## QA Complete

VERDICT: PASS
