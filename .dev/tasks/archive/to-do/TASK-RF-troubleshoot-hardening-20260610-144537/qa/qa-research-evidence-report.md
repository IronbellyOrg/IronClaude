# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Pipeline Hardening Closure mode for sc:troubleshoot-protocol
**Date:** 2026-06-10
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS

The research is dense, evidence-based, and the primary load-bearing insertion anchors are byte-exact correct. All 9 file targets (4 edit / 5 new) verified. The driving spec and all E1-E5 evidence dirs exist. Doc-validation tags in 05 are complete and consistent. A small cluster of off-by-one line-count/header-line drifts (all of the trailing-newline / header-start class) were found; none corrupt the primary insertion seams, but they warrant a MINOR flag so the builder uses anchor TEXT (not raw line numbers) for the few affected section-map rows.

---

## Items Reviewed (10-item research-gate checklist, evidence-quality lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (6 files, Status: Complete, Summary) | PASS | All 6 read; each has `**Status:** Complete` (01:5, 02:5, 03:5, 04:5, 05:5, 06:5). 02/04/05/06 carry Summary; 01/03 carry recommendation+status sections. No incomplete file. |
| 2 | Evidence density (file:line/section per claim) | PASS (Dense >80%) | Every structural claim carries SKILL.md/troubleshoot.md/report-template/Makefile line refs. Spot-checked ~25 anchors against source — see Spot-Checks below; all primary anchors CONFIRMED. |
| 3 | Scope coverage (key files discussed) | PASS | SKILL.md (01), command (02), refs+report-template+remediation-handoff (03), MDTM template+task-builder skill (04), spec+evidence cross-val (05), Makefile+lint+tests (06). All edit/create targets covered. |
| 4 | Doc cross-validation tags applied | PASS | 05 carries 28 real `[CODE-VERIFIED]` tags; the lone `[CODE-CONTRADICTED]`/`[UNVERIFIED]` strings are on L139 in the "ZERO ... ZERO" summary sentence (not findings). Every doc-sourced claim tagged. Verified each major `[CODE-VERIFIED]` independently. |
| 5 | Contradiction resolution | PASS | No cross-file contradictions. R3↔R1 agree on report-template/SKILL ref wiring; R5↔R2 agree on 548-line SKILL.md count (R1 says 549 — see I-3). F1/F2 in 05 are spec-internal self-consistency notes, correctly flagged non-blocking. |
| 6 | Gap severity (all gaps = FAIL) | PASS | No CRITICAL/IMPORTANT research gaps. The line-count drifts (I-1..I-4) are MINOR data-quality flags, not coverage gaps — the underlying anchor TEXT is verified correct, so the builder is not blocked. |
| 7 | Depth appropriateness (Deep: data flow end-to-end) | PASS | 02 §3 traces the full downstream chain Wave 5 → output contract → Wave 6 Tier 3 → task-builder → reflect, with the §5.2 remediation-gating seam. 04 traces template→QA-gate→completion end-to-end. |
| 8 | Integration point coverage | PASS | Command↔skill handoff (02 §1.4, L80), output-contract↔report-template↔remediation-handoff threading (02 §3, 03 §3), SKILL.md↔refs lazy-load+registry convention (01 §5, 03 §1.7), sync-dev↔verify-sync↔markdownlint (06). |
| 9 | Pattern documentation | PASS | Ref house-style (03 §1: no-frontmatter, single-H1, fence-language, table-style), wave/emit/verdict-enum conventions (01 §6), MD025/MD040 lint traps (03 §5, 06 §2), MDTM B2/anti-orphaning/POST-reflect (04). Rich and implementation-ready. |
| 10 | Incremental writing compliance | PASS | Files show growing structure (numbered sub-sections, per-escape rows, per-file build recs) consistent with iterative writing; no one-shot perfection artifacts or truncation. 03 has trailing blank lines (benign). |

## Spot-Checks (mandatory ≥20% — performed ~25 independent file opens)

| Cited claim | Source | Independent finding | Result |
|---|---|---|---|
| SKILL.md ~548 lines | R2/R5 say 548; R1 says 549 | `wc -l`=548, `awk NR`=548, trailing `\n` present | CONFIRMED 548 (R1 off-by-one — see I-1) |
| Output Contract table L37-61 | R1/R2 | L37=`## Output Contract`, table header L41-42, L43=`status`, L58=`diagnosability_verdict`, L61=`diagnosability_hard_stop` | CONFIRMED |
| Wave 4 ends ~L382, `---` seam L383, Wave 5 L385 | R1 | L382 blank, L383=`---`, L385=`### Wave 5: Synthesis + Report`; Wave 4 hdr L356 | CONFIRMED |
| Wave Structure map L77/79-91 | R1 | L77=`## Wave Structure`, fence+map lines present incl Wave4 then Wave5 | CONFIRMED |
| Wave 1.7 L251 + exit L263 | R1 | L251 header, L263 Exit-criteria w/ `Emit "Wave 1.7 complete"` | CONFIRMED |
| Refs registry L536, rows 540-546 | R1 | L536=`## Refs`, 7 ref rows L540-546 exact | CONFIRMED |
| Tier2 calibration gate L327 | R1 | L327=`#### Tier 2 calibration completeness gate (hard precondition for report publishing)` | CONFIRMED |
| Wave 6 precondition L439 | R2/R5 | L439=`**Preconditions**: --fix ... success (not partial) AND user accepts` | CONFIRMED |
| command description L3 | R2 | L3 matches verbatim | CONFIRMED |
| Behavioral Summary L60-67 | R2 | L60=`## Behavioral Summary`, L62 keep-thin sentence, L67 step 4 | CONFIRMED |
| Handoff `> Skill sc:troubleshoot-protocol` L80 | R2 | L80 exact | CONFIRMED |
| `--output-dir` row L56 | R2 | L56 artifact-list row exact | CONFIRMED |
| report-template insertion ~L132 | R3 | L132=`If there are no follow-ups, write "None."`, L133 blank, L134=`## Grounding Gaps`; full section map matches grep | CONFIRMED |
| report-template four-backtick fence L7 open / L203 close | R3 | L7=`` ````markdown ``, L203=`` ```` `` | CONFIRMED |
| Makefile sync-dev:109 / verify-sync:166 | R5/R6 | L109=`sync-dev:`, L166=`verify-sync:` | CONFIRMED |
| 5 new refs ABSENT | R5 | all 5 absent; refs/ has 8 existing files | CONFIRMED |
| 4 edit-targets EXIST | R5 | all 4 exist | CONFIRMED |
| driving spec exists, §9 list | R5 | spec 382 lines; §9 Primary-edits L320 + new-refs L327 match 4+5 paths verbatim | CONFIRMED |
| spec §6.2 verdict enum L105 | R5/F1 | L105 = `pass, blocked, advisory, or not_applicable` | CONFIRMED |
| spec §8 Closure-verdict L311 omits not_applicable; NOT PROVEN L314 | R3/R5/F1 | L311=`pass \| blocked \| advisory`; L314 NOT PROVEN paragraph | CONFIRMED (validates F1) |
| E1-E5 escape dirs + root-cause.md/remediation.md | R5 §2 | all 5 dirs present; E1 & E5 each contain root-cause.md + remediation.md (+hyp/rem) | CONFIRMED |
| generalized-remediation-set.md R1-R7 | R5 §3 | file present, R1-R7 enumerated | CONFIRMED |
| task-builder SKILL.md L2193-2198 / L2302 / L2312 | R4 | POST-reflect SELF-RUN item, rule 15 anti-orphaning, rule 20 MALFORMED all present and faithfully cited | CONFIRMED |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues found: 4 (all MINOR — line-count/header-line drift; report-only, no fix authorized)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | MINOR | 01 (research file) §0 note L10 | R1 claims SKILL.md is "549 lines (brief said 548; off by one — confirmed by Read)". Actual = 548 (`wc -l`, `awk`, trailing newline present). R1's note asserting 549 is itself the off-by-one error; R2 and R5 correctly say 548. CRUCIALLY: R1's downstream line ANCHORS (L37/L43/L58/L61/L251/L263/L356/L383/L385/L536) all independently verified CORRECT despite the wrong header count — so no insertion seam is corrupted. | Builder: trust the verified anchor TEXT, not the "549" count. No edit needed to research; flag carried so builder doesn't propagate a 549-based off-by-one when authoring Edit items. |
| I-2 | MINOR | 03 §2.1 section-map table | `## Documentation Context` listed at "39-48"; actual header is at **L38** (grep confirms `38:## Documentation Context`). Off-by-one on that section-map row's start line. The primary insertion anchor (after L132, before L134) is unaffected and byte-exact correct. | Builder: anchor report-template edits on TEXT (`## Follow-up tasks` / `If there are no follow-ups, write "None."` / `## Grounding Gaps`), which are verified, not on the §2.1 table's absolute line numbers. |
| I-3 | MINOR | 03 §2 / §2.1 | report-template.md stated as "259 lines"; actual = 258 (trailing-newline class, same as I-1). Four-backtick fence close stated at L203 — verified correct. | None blocking; builder uses the verified L132/L134 text anchors. |
| I-4 | MINOR | 03 §3.1 remediation-handoff map | `## The user offer` listed "line 4" (actual L5); `## Failure modes` listed "116-123" (actual header L115, file is 122 lines not 123). The wiring TEXT anchors (load-condition L1-2, `## Failure modes` table, last data row) are correct in substance; only the absolute line numbers drift by one. | Builder: anchor remediation-handoff edits on the `## Failure modes` header TEXT and the load-condition line TEXT, not the §3.1 absolute numbers. |

## Why these are MINOR (not IMPORTANT/CRITICAL)
The four issues are a single systematic class: **trailing-newline line-count drift and a few header-start off-by-ones**. They do NOT corrupt any of the load-bearing insertion seams, because every primary anchor was independently verified by TEXT (e.g., "insert after `If there are no follow-ups, write "None."` / before `## Grounding Gaps`") and those text anchors are byte-exact. They become harmful ONLY if the builder authors raw-line-number Edit operations against the drifted section-map rows instead of text-anchored Edits. Since MDTM Edit items must use exact `old_string` text matches anyway (per the task-builder pattern in 04), the practical blast radius is near-zero — but the flag is recorded so the builder explicitly anchors on text.

## Actions Taken
None — `fix_authorization: false` (report-only QA pass). All issues documented for the builder.

## Recommendations
- Builder MUST author every Edit item using exact `old_string` TEXT anchors (which are all verified correct), NOT absolute line numbers from the section-map tables in 01 §0 / 03 §2.1 / 03 §3.1.
- Builder should treat SKILL.md as 548 lines and report-template.md as 258 lines (ignore the 549/259 claims).
- The verified primary insertion anchors the builder can rely on byte-exact: SKILL.md Output-Contract append-after-L61; SKILL.md Refs-table append-after-L546; SKILL.md Wave-4.5 seam at the `---`/L383 before Wave 5/L385; report-template insert between `## Follow-up tasks` body ("...write \"None.\"") and `## Grounding Gaps`; remediation-handoff `## Failure modes` table-row append.

## Confidence Gate

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: ~6 (within Bash) | Glob: 0 | Bash: 7

Every checklist item is marked VERIFIED with cited tool output (file:line anchors independently opened). Tool calls (6 Read + 7 Bash, each Bash bundling targeted grep/sed/wc/ls against specific claims) exceed the 10-item floor and each maps to a specific verification, not padding. No web research was required (all claims are local source-truth).

## QA Complete

**VERDICT: PASS** — Research is builder-ready. Zero CRITICAL/IMPORTANT issues. 4 MINOR line-count/header-line drift flags recorded so the builder anchors Edit items on verified TEXT rather than the few drifted absolute line numbers. The 9 file targets, driving spec, E1-E5 evidence, doc-validation tags, and all primary insertion seams are independently confirmed.
