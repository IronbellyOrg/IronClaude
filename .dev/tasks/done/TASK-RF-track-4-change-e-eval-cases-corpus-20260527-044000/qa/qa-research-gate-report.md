# QA Report — Research Gate

**Topic:** Track 4 Change E — NEW FILE calibrator-eval-cases.md corpus
**Date:** 2026-05-27
**Phase:** research-gate
**Fix cycle:** N/A
**Depth tier:** Standard

---

## Overall Verdict: FAIL

## Stance
Adversarial. Assume claims contain errors. Verifying every quote, path, line citation, and inventory claim against ground truth using independent tool calls.

---

## Independent Verifications (Spawn-Prompt Targets a-e)

### (a) Proposal quotes spot-checked against CROSS-ENV-PROPOSAL-MERGED.md L290-372

Read proposal L280-380 directly. Spot-checked 4 quotes:

| Location | Research 01 claim | Ground-truth (proposal) | Match |
|---|---|---|---|
| L290 heading | "Change E — NEW FILE: `src/.../refs/calibrator-eval-cases.md`" | literal match | YES |
| L298-301 file header | `# Calibrator Eval Cases` + intro listing 4 trigger files | literal match (escalation-rubric, confidence-calibrator, hypothesis-card-template, sc-troubleshoot-protocol/SKILL.md) | YES |
| L334-336 Fixture 7 | "Replays actual `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500`" | literal match | YES |
| L350 P1 row | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` | literal match including U+27F9 ⟹ | YES |

Research 01 spec-extraction is faithful to source.

### (b) T4 directory absence — independently verified

`find /config/workspace/IronClaude -maxdepth 8 -type d -name "*t4-pane*"` → empty output.
`find ... -maxdepth 10 -type d -name "*pane-title*"` → empty.
`find ... -name "*20260526-101500*"` → empty.

CONFIRMED: `t4-pane-title-20260526-101500` does not exist. Research 03 §1.1-1.2 claim correct.

### (c) refs/ inventory — independently verified

`ls src/superclaude/skills/sc-troubleshoot-protocol/refs/` returned exactly 6 files: doc-discovery.md, escalation-rubric.md, hypothesis-card-template.md, remediation-handoff.md, report-template.md, triage-checklist.md. Matches research 02 §1.

Line counts via `wc -l`:

| File | wc -l (actual) | Research 02 §1 | Research 03 §7.1 |
|---|---|---|---|
| doc-discovery.md | 182 | 182 | n/a |
| escalation-rubric.md | 52 | 52 | n/a |
| hypothesis-card-template.md | **108** | **152 (WRONG)** | **108 (correct)** |
| remediation-handoff.md | 122 | 122 | n/a |
| report-template.md | 196 | 196 | n/a |
| triage-checklist.md | 65 | 65 | n/a |

**Intra-research contradiction:** research 02 says hypothesis-card-template.md is 152 lines; research 03 §7.1 says 108 lines; ground truth is **108 lines**.

### (d) Cross-link claim — hypothesis-card-template.md:105 references calibrator-eval-cases.md

Research 02 §8 (file line 194) asserts the new file is "ALREADY pre-referenced" at hypothesis-card-template.md:105 with the text "MANDATORY in v2.0 (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability)."

Verification:

1. Read line 105 directly → contains the literal text `0.92` (a confidence-score example inside the card template). Does NOT contain "MANDATORY in v2.0..." text.
2. `grep -n "calibrator-eval-cases" hypothesis-card-template.md` → **ZERO matches**.
3. The file is only 108 lines — research 02's cited lines `:116`, `:118`, `:123`, `:125-152` are out-of-range.

**FABRICATION CONFIRMED.** Research 02 describes a post-PR#89 hypothetical state of the file that does not exist on this branch.

### (e) U+27F9 ⟹ character grep in refs/

`grep -lP "\x{27F9}" refs/*.md` → empty. `grep $'⟹' refs/*.md` → empty.

CONFIRMED: U+27F9 absent from current refs/. Research 02 §7 claim accurate. Proposal L350-352 DOES use U+27F9 (verified in (a)).

---

## Items Reviewed — 10-Item Research Gate Checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory: all research files marked Complete with Summary | PARTIAL | File 01 header line 5 says `Status: In Progress` but ends with `## Status: Complete` at L413 + has `## Summary` section L415. Files 02 and 03 marked `Status: Complete` correctly with Summary sections. Minor inconsistency in 01 frontmatter vs body, but the content is complete. |
| 2 | Evidence density: every claim cites specific files+lines, paths verified | DENSE for 01 + 03; ADEQUATE for 02 | Research 01 quotes proposal L290-372 verbatim with line anchors throughout. Research 03 cites Makefile L108-163, .pre-commit-config.yaml L70-82 + L98-109 verbatim. Research 02 has good structural claims but the line citations into hypothesis-card-template.md (`:36, :82, :105, :116, :118, :123, :125-152`) are FABRICATED against current ground truth (108-line file, calibrator-eval-cases never referenced) — see verification (d). |
| 3 | Scope coverage: research-notes EXISTING_FILES discussed | COVERED | All 7 EXISTING_FILES entries from research-notes.md L11-18 are addressed across the three files. Target path, refs/ dir, confidence-calibrator.md, escalation-rubric.md, hypothesis-card-template.md, proposal, and T4 dir all examined. |
| 4 | Documentation cross-validation: doc claims tagged [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED] | MISSING | No `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags present anywhere in the 3 research files (grep returned 0). Research relies on direct code/file reads but does not annotate the verification status. This is a SOFT FAIL — verification clearly happened (research 03 ran find/ls commands; research 01 quoted the proposal verbatim) but the tagging convention from SKILL.md research procedure is not applied. |
| 5 | Contradiction resolution | UNRESOLVED CONTRADICTION | Research 02 §1 + §10 claim hypothesis-card-template.md = 152 lines. Research 03 §7.1 claims it is 108 lines (Change B target description: "existing 108-line file"). Ground truth: 108 lines. Contradiction not flagged in either file or in the analyst report. |
| 6 | Gap severity: all gaps resolved | FAIL | Research-notes.md GAPS_AND_QUESTIONS §1 (Fixtures 7-9 real-card extraction) is resolved by research 03 §1.4 (inline content fallback). However NEW gaps surfaced during QA: (a) fabricated/stale line citations in research 02 — see issue F-01; (b) line-count contradiction — see issue F-02; (c) missing doc-validation tags — see issue F-03. |
| 7 | Depth appropriateness (Standard tier — file-level coverage) | PASS | Standard tier achieved. Three files cover spec, conventions, and workflow at file-level depth. T4 hunt was thorough (4 find commands at varying depths). |
| 8 | Integration point coverage | PASS | Integration with Makefile (sync-dev/verify-sync), pre-commit hooks (markdownlint + block-claude-generated-mirrors), source-of-truth rule, and dependency on Changes A+C all documented (research 03 §3-5; research 01 §9). |
| 9 | Pattern documentation | PASS for refs/ style; FAIL for accuracy | Research 02 documents 8 convention dimensions (H1, intro, headings, tables, code fences, Unicode, backticks, bold). The convention CATEGORIES are correctly identified. The specific line-citations into hypothesis-card-template.md are wrong. The CONCLUSIONS (sentence-case H2s, em-dash H3 separators, no code fences, U+27F9 is novel) are sound and verifiable from other files. |
| 10 | Incremental writing compliance | PASS | Files show progressive structure (multiple H2 sections, status markers, "(verified via grep)" annotations indicating iterative tool engagement). No signs of one-shot generation. |

---

## Summary

- Checks passed: 6 / 10 (#1 partial, #4 missing-tags, #5 unresolved contradiction, #6 fail, #9 fail-on-accuracy)
- Checks failed / partial: 4
- Critical issues: 1 (F-01: fabricated line citations)
- Important issues: 2 (F-02: contradiction; F-03: missing doc-validation tags)
- Minor issues: 1 (F-04: file 01 status header inconsistency)
- Issues fixed in-place: 0 (`fix_authorization: false`)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-01 | CRITICAL | research/02-refs-conventions.md §1 (L25, L240), §4 (L84 cites L116/L123 in 108-line file), §7 (L154 cites L36/L82/L118), §8 (L194 — the "MANDATORY in v2.0... calibrator-eval-cases.md... ALREADY pre-referenced" claim against L105) | Fabricated/stale citations: hypothesis-card-template.md is 108 lines on this branch, line 105 contains `0.92`, file contains ZERO references to `calibrator-eval-cases`. The "ALREADY pre-referenced" claim is FALSE against current ground truth. This appears to be a post-PR#89 hypothetical state of the file. | Re-read hypothesis-card-template.md on the current branch (108 lines). Replace all line citations with actual line numbers. Remove or correct the "ALREADY pre-referenced" claim. If research 02 was deliberately researching a post-PR#89 state, the file must explicitly flag that scope and the task file must not assume the cross-reference exists. |
| F-02 | IMPORTANT | research/02 §1 (152) vs research/03 §7.1 ("existing 108-line file") | Unresolved intra-research contradiction on hypothesis-card-template.md line count (152 vs 108). Ground truth: 108. Neither file flags the disagreement; the analyst report does not catch it. | Reconcile to 108 (ground truth on this branch). Update research 02 §1 line-count column and §10 length-table row. Either file must explicitly note: "Change B (PR #89) has not yet landed on this worktree; the file is still at 108 lines. Post-PR#89 state would be 152 lines and would add the calibrator-eval-cases cross-reference at L105." |
| F-03 | IMPORTANT | All 3 research files | Documentation cross-validation tags (`[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]`) are entirely absent. Research 03's claims about Makefile/pre-commit are code-derived and verifiable, but the tagging convention from SKILL.md research workflow is not applied — making it harder for downstream synthesis to know which claims have been spot-checked. | Audit each major claim in research 02 (refs/ conventions) and add `[CODE-VERIFIED]` tags after spot-checking against current sibling files. Annotate the line-citation findings as `[CODE-CONTRADICTED]` once F-01 is corrected. Tag research 01 proposal-quote claims as `[SOURCE-VERIFIED]` (they trace to a single source document, not project code). |
| F-04 | MINOR | research/01-change-e-spec-extraction.md L5 vs L413 | Status header inconsistency: line 5 says `Status: In Progress`; line 413 says `## Status: Complete`. The body is complete; the header is stale. | Update L5 to `Status: Complete` to match L413. |

---

## Actions Taken

None. `fix_authorization: false` for this gate.

---

## Confidence

Verified: 10/10 (every checklist item mapped to specific tool evidence) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

Tool engagement: Read: 7 | Grep: 3 | Glob: 0 | Bash: 9 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

Tool engagement exceeds the 10-item checklist size; each item maps to at least one specific tool call (Read of research file, Read of source file, Grep of refs/, Bash find/wc/ls/grep, or proposal Read). No external web research was needed — all verifications were against local files.

---

## Recommendations

Before proceeding to synthesis:

1. **Fix F-01 (CRITICAL):** Re-read hypothesis-card-template.md on this branch. Either replace the fabricated citations with real ones, OR explicitly scope research 02 to a post-PR#89 hypothetical with a clear caveat. Without this, the task file may emit a calibrator-eval-cases.md that references a cross-link in hypothesis-card-template.md that does not exist.

2. **Fix F-02 (IMPORTANT):** Reconcile the 152-vs-108 line-count contradiction. The current branch reality is 108 lines.

3. **Fix F-03 (IMPORTANT):** Add `[CODE-VERIFIED]` / `[SOURCE-VERIFIED]` tags to each major claim. This is the SKILL.md research workflow contract and not optional.

4. **Fix F-04 (MINOR):** Update file 01's L5 status header.

5. **Re-spawn rf-analyst on this finding set OR proceed only after fixes land.** The analyst's PASS verdict (with 2 minor cosmetic findings) was incorrect — the analyst did not independently verify research 02's hypothesis-card-template.md line citations against the actual file. ALL gaps regardless of severity must be resolved before proceeding to synthesis (per the Research Gate rule).

## QA Complete
