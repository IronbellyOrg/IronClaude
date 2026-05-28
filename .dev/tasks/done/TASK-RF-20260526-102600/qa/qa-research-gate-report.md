# QA Report — Research Gate

**Topic:** PR A — F1+F3+F5 fix from PR #86 review (task-builder MDTM task file)
**Date:** 2026-05-26
**Phase:** research-gate
**Fix cycle:** N/A
**Tier:** Quick (3 researchers)
**Fix authorization:** false (report-only)

---

## Overall Verdict: **FAIL**

One CRITICAL issue: research file 02 (`02-patterns-and-conventions.md`) contains
systematically incorrect line numbers across most of its evidence citations (offset
by 1–10 lines from the actual PR-sha file). The substantive pattern claims are
correct, but every line-number anchor it gives the builder is wrong. Since the
builder will rely on these numbers to position new code, this is blocking.

R1 (file inventory) and R3 (template) verify clean.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory + Status: Complete + Summary | PASS | All 3 files present (`ls`), each has `**Status:** Complete` header and a `## Summary` section (Read confirmed). |
| 2 | Evidence density — every claim verifiable | FAIL | R1: dense and verified (all 6 touch points re-grounded with `git show 67ab0af5`). R3: dense and verified (template line cites 730/732/736/744/779/821/etc. all confirmed via `grep -n` on template file). **R2: FAIL — most line-number anchors are wrong.** See Issue #1. |
| 3 | Scope coverage — every SUGGESTED_PHASES area covered | PASS | research-notes.md SUGGESTED_PHASES specifies R1=file inventory, R2=patterns/conventions, R3=template & examples. All three areas produced output; the G1–G4 verification gaps from research-notes are addressed by R1 (G1 touch-point line numbers, G2 spec_evidence audit, G3 case-sensitivity audit, G4 verification commands). |
| 4 | Documentation cross-validation — doc-sourced claims tagged | PASS | No external-doc claims in research files. All claims are sourced from `git show 67ab0af5:...` (R1, R2) or from the local template file (R3). No untagged doc claims found. |
| 5 | Contradiction resolution | PARTIAL FAIL | R1 explicitly corrects 4 line-number claims from the upstream merged-output.md spec (touch points 1, 5, 6) — this is the planned-correction case the prompt mentions, NOT a contradiction. **However, R2 silently disagrees with R1 on `_extract_identifiers` location (R2 says 405; R1 says 412 — R1 is correct).** This is an unresolved internal contradiction. See Issue #1. |
| 6 | Gap severity — all gaps classified | PASS | Severity ratings applied in Issues section below. |
| 7 | Depth appropriateness — matches Quick tier | PASS | 3 researchers as specified; 6 touch points (R1) + 5 convention categories (R2) + template + 1 done-example (R3) — appropriate for Quick tier conversion task with no discovery. |
| 8 | Integration point coverage | PASS | R1 covers the production-test integration (touch point 6 maps test fixture to `_signature_subsumed`). R1 G3 audit confirms scope confinement (only one case-sensitive site exists). |
| 9 | Pattern documentation | PASS (with caveat) | R2's pattern descriptions (docstring style, regex compilation, naming, type hints) are substantively correct when re-grounded against the actual file. Caveat: the line citations supporting each pattern are wrong (see Issue #1) — the patterns themselves are real and the builder can re-find them. |
| 10 | Incremental writing compliance | PASS | All 3 files show iterative structure: per-touch-point sections (R1), per-convention sections (R2), per-template-section tables (R3). No signs of one-shot synthesis. |

---

## Summary

- Checks passed: 8 / 10
- Checks failed: 2 (Evidence density on R2; Contradiction resolution between R1 and R2)
- Critical issues: 1
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization=false)

---

## Issues Found

### Issue #1 — CRITICAL — R2 line numbers systematically wrong

**Location:** `research/02-patterns-and-conventions.md` — multiple sections

**What's wrong:** R2 cites specific line numbers throughout (e.g., `_classify_mechanism` at line 374, `_extract_identifiers` at line 405, `_signature_subsumed` at line 416, `# --- Internal helpers ---` banner at line 371, `mechanism_signature` field at line 134, function-local regex at lines 293/306, inline `re.findall` at lines 411–414, etc.). **None of these line numbers match the file at PR sha `67ab0af5`.** Independent verification via `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py | grep -n '^def \|^# --- Internal'`:

| R2 claim | R2 line | Actual line @ PR sha 67ab0af5 | Drift |
|---|---|---|---|
| `# --- Internal helpers ---` banner | 371 | **380** | -9 |
| `def _classify_mechanism` | 374 | **382** | -8 |
| `def _extract_identifiers` | 405 | **412** | -7 |
| `def _signature_subsumed` | 416 | **424** | -8 |
| `mechanism_signature: tuple[...] = field(...)` | 134 | **132** | +2 |
| `contracts: list[IntegrationContract] = field(...)` | 153 | **152** | +1 |
| `def extract_integration_contracts(...)` | 167 | **166** | +1 |
| `seen_signatures: dict[...]` | 178 | **177** | +1 |
| `dispatch_family = re.compile(...)` | 293 | **291** | +2 |
| `impl_verbs = re.compile(...)` | 298 | **298** | 0 (correct) |
| Inline `re.findall(...)` in `_extract_identifiers` | 411–414 | **417–420** | -6 |
| `from __future__ import annotations` | 13 | **13** | 0 (correct) |

R2's line numbers also do NOT match the current-branch (master) file (which has `def _extract_identifiers` at line 347, `# --- Internal helpers ---` at line 314). They do not match any of the 4 most-recent shas in the file's history either (which had `def _extract_identifiers` at 347/351/352/294). R2 either fabricated the numbers or read from a stale, untracked snapshot.

**Why this is CRITICAL:** R2's section-5 recommendation tells the builder "Place definition under the `# --- Internal helpers ---` banner near end of file, after `_signature_subsumed`." That position is line 380+424 territory, not 371+416. If the task-builder embeds R2's line numbers into the MDTM checklist items (e.g., "Insert `_canonicalize_identifiers` after line 416"), the builder will be telling the executor to insert code 8 lines too early — landing inside `_extract_identifiers`'s body, NOT after `_signature_subsumed`.

**Mitigating factor:** R2's *substantive* claims (the conventions themselves — docstring style, regex compilation patterns, naming, type hint style) are correct when re-grounded against the actual file. Only the line anchors are wrong. R1's line numbers for the same file are verified accurate.

**Required fix:** Re-ground R2's line citations against `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py` using either:
- (a) Re-run R2 with explicit instruction to `git show 67ab0af5:...` for every line citation, OR
- (b) Patch R2 in-place: replace the 10 wrong line numbers with the verified values from the table above, OR
- (c) Have the task-builder rely ONLY on R1 for line citations and use R2 ONLY for pattern descriptions (no line anchors).

Option (c) is the lightest-touch fix and is consistent with the SUGGESTED_PHASES division of labor (R1 owns line numbers; R2 owns patterns).

### Issue #2 — IMPORTANT — R1/R2 internal contradiction on `_extract_identifiers` line

**Location:** R1 §"Touch Point 1" (line 412) vs R2 §1 evidence header (line 405)

**What's wrong:** R1 and R2 disagree on where `_extract_identifiers` is defined. R1 says PR-line 412 (verified correct). R2 says line 405 (verified wrong). Per QA Principle "Contradictions are critical — never resolve silently." The analyst's completeness report does not flag this contradiction.

**Required fix:** Resolution rule for the task-builder — when R1 and R2 disagree on a line number, **trust R1** (R1's numbers are independently verified against the PR sha; R2's are not). Document this resolution in either the analyst's report or in the task file's "Open Questions"/header. Strictly speaking, this is fully captured by fixing Issue #1, so the two are linked.

---

## Actions Taken

None (fix_authorization=false). Report-only mode.

---

## Recommendations for the task-builder skill

1. **BEFORE building the MDTM task file**, address Issue #1 via one of the three options above (recommend Option (c): task-builder uses R1 line numbers exclusively for code-insertion anchors; R2 contributes pattern guidance only).
2. **Embed an explicit resolution note** in the task file's Open Questions section noting that R1 line numbers supersede R2 line numbers when they conflict.
3. **Re-verify any line number that ends up in a checklist item** via `git show 67ab0af5:<path> | sed -n '<line>p'` as a final sanity check before marking the task ready for execution.
4. Once Issue #1 is addressed, the research is sufficient for the Quick-tier conversion task: R1 covers the 6 touch points + verification commands, R2 covers the 5 convention categories (substance), R3 covers the template structure + one done-example. Scope confinement is verified (R1 G3: only one case-sensitive site).

---

## Confidence

- **Verified:** 10/10 checklist items checked with tool evidence (Read on all 3 research files, the analyst report, the research-notes.md, the template, and the cliEval-P4 done-task; Bash for `git show 67ab0af5:<path>` verification of every R1 touch point and most R2 line cites; Bash for `make lint` to verify R1 G4; Bash for `wc -l` and `grep -n` to verify file sizes and section positions).
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 (via Bash) | Glob: 0 | Bash: 14 | Edit: 1 | Write: 1
- **Tavily engagement:** N/A — verification is purely local source-truth based; no external claims to verify.

## QA Complete
