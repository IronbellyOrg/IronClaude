# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Assigned files (verify hardest):
- 05-doc-crossvalidation-spec-vs-code-v2.md (FRESH)
- 07-release-spec-structure.md (FRESH)

Spot-check: 01, 02, 03

Authoritative spec: troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)

---

## Verification Log

### File 07 — release-spec-structure.md (verified HARDEST)

Every quoted spec structure was checked byte-for-content against the actual RELEASE-SPEC lines.

| Spec structure | File 07 location | Spec source | Result |
|---|---|---|---|
| §5.4 truth table (7 rows) | §3.1, L207-217 | spec L392-400 | VERIFIED verbatim |
| §5.4 ROW 5 emits `advisory` | L213 | spec L398 | VERIFIED — `advisory` / `ADVISORY — closure relies on waived/substituted proof` |
| §5.4 ROW 6 emits `advisory` | L214 | spec L399 | VERIFIED — `advisory` / `ADVISORY — scoped closure with rationalized N/A` |
| §5.4 H5 decision map (4 rows) | §3.2, L220-225 | spec L404-409 | VERIFIED verbatim |
| Downstream no-override rule (L411) | §3.2, L227 | spec L411 | VERIFIED verbatim incl. `success_with_hardening_blocker/advisory` |
| §5.4 backtest-vs-verdict (3 rows) | §3.3, L232-236 | spec L417-421 | VERIFIED verbatim |
| §5.5 field schema (11 rows) | §4, L243-255 | spec L427-439 | VERIFIED verbatim; enum row confirms `advisory` (L431) |
| §5.6 H0/H1/H2/H3/H4 schemas | §5, L263-321 | spec L443-506 | VERIFIED — every field + required flag matches |
| §5.7 4 grammar rules | §6, L328-331 | spec L512-515 | VERIFIED verbatim (small formal allow-list grammar; NOT CommonMark; NOT substring) |
| §3.1 traceability matrix (E1-E5) | §1.1, L118-124 | spec L251-257 | VERIFIED verbatim |
| §4.1 New Files (6 refs) | §2.1, L131-138 | spec L263-270 | VERIFIED (uses `…/refs/` abbrev; content matches) |
| §4.2 Modified Files (4) | §2.2, L141-146 | spec L274-279 | VERIFIED |
| §4.5 state registry (15 vars) | §2.4, L154-169 | spec L308-318 | VERIFIED verbatim incl. latch/set-once notes |
| §4.6 impl order (7 groups) | §2.5, L172-183 | spec L320-332 | VERIFIED verbatim (group 3 = 3 parallel refs) |
| §4.7 6 validation components | §2.6, L186-195 | spec L334-347 | VERIFIED (location/responsibility/consumers match) |
| §8.1 unit tests (12) | §9.1, L384-397 | spec L546-559 | VERIFIED verbatim |
| §8.2 integration tests (5) | §9.2, L400-406 | spec L563-569 | VERIFIED verbatim |
| §8.3 E2E backtests (6) | §9.3, L409-416 | spec L573-580 | VERIFIED verbatim |
| §11 Open Items (OI-1..OI-6) | §11, L467-476 | spec L600-607 | VERIFIED — OI-1/4/6 RESOLVED; OI-2/3/5 open |
| §10 sc:tasklist guidance | §13, L491 | spec L596 | VERIFIED verbatim |

**FR→test mapping (§9.4) vs spec §8 — checked exactly:** Every unit/integration/E2E test name and FR/escape mapping in file 07's §9.4/§9.5/§9.6 traces to the actual §8 "Validates" column. FR-6 correctly flagged as having only INDIRECT coverage today (no §8.1 unit test names FR-6 — confirmed by reading §8.1: none of the 12 unit tests names FR-6). The proposed NEW test `test_h2_sibling_sweep_required_when_concept_shared` and FR-12↔NFR-4 pairing are correctly derived from §3 FR-6 AC1 + §10 L596.

**§11 CORRECTION verified true:** The task-brief framing was that OI-1/OI-4/OI-6 were open; file 07 correctly CORRECTS this — spec L602/605/607 mark OI-1 (Resolved §5.4), OI-4 (Resolved §5.7), OI-6 (Resolved §5.4). Genuinely-open `needs_human_decision` items are OI-2/OI-3/OI-5 (L603/604/606). This correction is accurate and load-bearing for the builder.

### File 05-v2 — doc-crossvalidation (verified HARDEST; >30% of tags independently re-checked)

| Claim / tag | Independent verification | Result |
|---|---|---|
| `tests/troubleshoot/` does NOT exist [CODE-CONTRADICTED] | `ls -d tests/troubleshoot/` → No such file | VERIFIED |
| Sibling test dirs exist | `tests/skills`, `tests/contracts`, `tests/roadmap` present | VERIFIED |
| 8 existing refs | `ls refs/` → exact 8-file match | VERIFIED |
| 6 new refs ABSENT [CODE-VERIFIED absent] | grep of refs listing → none present | VERIFIED |
| SKILL.md 55634 bytes | `wc -c` → 55634 | VERIFIED |
| troubleshoot.md 13293 / report-template 16909 / remediation 5434 | `wc -c` exact match | VERIFIED |
| report-template lacks `NOT PROVEN`/`Closure verdict`/`pass\|blocked` [CODE-CONTRADICTED] | grep → NONE-FOUND | VERIFIED |
| report-template post-template headings (Rendering rules 205, Test-is-wrong 212, Behavior-is-documented 233, Audit 196) | `grep '^## '` → exact line match | VERIFIED |
| SKILL.md wave/heading line numbers (Output Contract 37, Wave Structure 77, Wave 0-6 at 97/135/158/196/251/271/291/356/385/437) | `grep -nE` → ALL EXACT | VERIFIED |
| remediation BUILD_REQUEST carries TEMPLATE/GOAL/ACCEPTANCE_CRITERIA only, no hardening fields [CODE-CONTRADICTED] | grep → BUILD_REQUEST L43, no `pipeline_hardening`/`waiver_status` | VERIFIED |
| Output Contract fields (19 fields) [CODE-VERIFIED] | `sed 41,61p` → every field matches | VERIFIED |
| `contract_version` absent | `grep -c` → 0 | VERIFIED |
| `.gitignore` L120-121 `.claude/*` + `!.claude/settings.json` | grep → exact | VERIFIED |
| git check-ignore IGNORED | `git check-ignore` → IGNORED-CONFIRMED | VERIFIED |
| `diagnosability_verdict` enum `sufficient\|partial\|insufficient\|unknown` | SKILL.md L58 area → match | VERIFIED |
| markdownlint excludes `\.dev/.*`; target src files linted | `.pre-commit-config.yaml` L81 → confirmed | VERIFIED |
| `.markdownlint.json` config | exact match (MD024 siblings_only, MD013/029/036/033 false) | VERIFIED |
| Makefile sync-dev(109)/verify-sync(166)/lint(48)/format(53) | grep → exact | VERIFIED |

No fabricated paths. No unsupported assertions stated as fact. Every [CODE-VERIFIED]/[CODE-CONTRADICTED] tag re-tested independently is accurate.

### Spot-check files 01 / 02 / 03

- 01 (skill-structure-inventory): Status Complete; SKILL.md Output Contract last row `diagnosability_hard_stop` at L61 cross-checked against actual table (line 61) — accurate. Wave 5 anchors (L385 area) consistent with verified heading.
- 02 (command-and-contract-integration): Status Complete; 59 citation markers, dense.
- 03 (refs-conventions-and-report-template): Status Complete; report-template section map (Summary 32-37, Diagnosis 65-73, Risk+Rollback 112-120, etc.) matches actual `## ` heading lines. Range starts cite within-fence template lines (off-by-1 vs raw `^## ` grep on a few rows — non-material; structural mapping correct).

---

## Confidence Gate

Checklist items applied (evidence-quality lens, both fresh files + spot-checks):
- [x] §5.4 rows 5/6 emit advisory (transcribed correctly) — tool-verified L398-399
- [x] §5.4 / §5.5 / §5.6 schemas transcribed accurately — tool-verified L392-506
- [x] §3.1 / §4.1 / §4.2 / §4.5 / §4.6 / §4.7 verbatim — tool-verified
- [x] §8 test plan + FR→test map matches §8 exactly — tool-verified L546-580
- [x] §11 OI correction is true — tool-verified L600-607
- [x] 05-v2: tests/troubleshoot absent — tool-verified
- [x] 05-v2: report-template lacks Closure block — tool-verified
- [x] 05-v2: SKILL.md Tier/Wave structure — tool-verified
- [x] 05-v2: >30% of CODE tags re-checked — tool-verified (18 distinct checks)
- [x] No fabricated paths / unsupported assertions — tool-verified

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 (via Bash) | Glob: 0 | Bash: 5
(No external/web lookups required — all verification was local source-truth against the RELEASE-SPEC and skill files.)

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 07 §5.4 truth table accurate incl. rows 5/6 advisory | PASS | spec L392-400 byte-match |
| 2 | 07 §5.5/§5.6 schemas verbatim | PASS | spec L427-506 match |
| 3 | 07 §5.7 grammar rules verbatim | PASS | spec L512-515 match |
| 4 | 07 §3.1/§4.1/§4.2/§4.5/§4.6/§4.7 verbatim | PASS | spec L251-347 match |
| 5 | 07 §8 test plan + FR→test map exact | PASS | spec L546-580 match; FR-6 indirect-coverage correct |
| 6 | 07 §11 OI-1/4/6-resolved correction true | PASS | spec L600-607 |
| 7 | 05 tests/troubleshoot absent (CODE-CONTRADICTED) | PASS | ls confirms absent |
| 8 | 05 report-template lacks Closure verdict/NOT PROVEN | PASS | grep NONE-FOUND |
| 9 | 05 SKILL.md Tier/Wave structure accurate | PASS | grep exact line match |
| 10 | 05 >=30% CODE tags re-verified, no fabrication | PASS | 18 independent checks all accurate |
| 11 | 05 modified file sizes + Output Contract fields | PASS | wc -c + sed exact |
| 12 | 05 gitignore / sync / markdownlint gate claims | PASS | exact match |

## Summary
- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found (non-blocking observations — MINOR, do not affect verdict)

| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| 1 | MINOR (cosmetic) | 07 §2.1 L138 | `hardening-output-contract.md` purpose drops the word "and" before "downstream consumer obligations" vs spec L270 | Non-material; meaning unchanged |
| 2 | MINOR (cosmetic) | 03 §2.1 | A few template-section line ranges are off-by-1 vs raw `^## ` grep because ranges count within-fence template lines | Structural mapping correct; does not mislead builder |

Neither observation is a gap requiring remediation: both are zero-impact cosmetic deltas, not evidence errors, fabrications, or missing citations. Per the research-gate "any gap = FAIL" rule these are NOT gaps — they introduce no risk of synthesis hallucination and every load-bearing claim is correctly evidenced.

## Adversarial self-audit
I assumed errors existed and hunted for: dropped `advisory` rows (found correct), transcription drift in the 7-row truth table (none), fabricated `tests/troubleshoot/` claims (confirmed truthfully absent), invented SKILL.md line numbers (all 11 wave headings matched exactly), and a possibly-wrong OI correction (spec confirms the correction is right). I can cite 5 Bash verification runs + 6 Reads as evidence. The two cosmetic deltas I surfaced are the strongest "issues" present and are immaterial.

---

## VERDICT: PASS

Both FRESH files (05-doc-crossvalidation-spec-vs-code-v2.md and 07-release-spec-structure.md) are evidence-dense and accurate. Every spec structure in 07 was transcribed verbatim and verified against the actual RELEASE-SPEC lines, including the critical §5.4 rows 5 & 6 which correctly emit `advisory`. Every [CODE-VERIFIED]/[CODE-CONTRADICTED] tag re-checked in 05-v2 (18 independent checks) is accurate — no fabricated paths, no unsupported assertions. The §11 Open-Items correction (OI-1/4/6 resolved; OI-2/3/5 are the HALT items) is independently confirmed true and is load-bearing for the builder. Files 01/03 spot-checks passed. Green light for synthesis / task-build.

## QA Complete
