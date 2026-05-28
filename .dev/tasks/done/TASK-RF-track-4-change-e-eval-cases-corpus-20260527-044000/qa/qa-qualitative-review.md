# QA Report — Task File Qualitative Review

**Topic:** Track 4 Change E — Calibrator Eval Cases Corpus
**Date:** 2026-05-27
**Phase:** task-qualitative
**Fix cycle:** 1
**Adversarial stance:** Active — assumed errors present; verified every command and reference

---

## Overall Verdict: PASS (after 2 in-place fixes applied)

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-1 | FAIL->FIXED | Step 5.1(h) prescribed `grep -P "\xE2\x9F\xB9"` would have failed: this host's `grep` is **ugrep 7.5.0**, and `\xNN` literal-byte escapes inside `-P` patterns do NOT match in ugrep PCRE (verified: `echo "⟹" \| grep -P "\xE2\x9F\xB9"` -> exit 1, no match, even though the bytes are present). Executor would have hit a false negative — the U+27F9 check would report 0 matches and erroneously fail the verification. **Fixed in-place**: replaced with portable `python3 -c "...read().count(b'\xe2\x9f\xb9')"` form. Verified portable form returns 3 on a test input containing three ⟹. |
| 2 | Project convention compliance | none | PASS | New file targets `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (source-of-truth side, not `.claude/`). `make sync-dev` (Makefile lines verified) mirrors src/ -> .claude/; `make verify-sync` enforces parity. Markdownlint excludes `\.dev/.*` but the new file lives at `src/superclaude/...` (NOT excluded). All three project conventions correctly observed. |
| 3 | Intra-phase execution order simulation | none | PASS | Phase 2 Write (H1+intro) -> Phase 3 Edit appends 5 H2 sections in order -> Phase 3.6 read-back -> Phase 4 sync+verify+lint -> Phase 5 final structural grep. Each Edit's `old_string` correctly anchors on the previously-appended section's tail content. No item reads a file before it's created. No item depends on later content. |
| 4 | Function signature / value verification | none | PASS | Verified every line-reference cited in the task: research file 01 Sections 3 (L50-176), 4 (L180-249), 5 (L253-267), 6 (L288-302), 7 (L321-329) all match cited ranges. Fixture verbatim line refs (Fixtures 1@L64-69, 2@L86-90, 3@L106-110, 4@L126-130, 5@L146-150, 6@L162-166, 7@L196-199, 8@L216-219, 9@L236-239) all verified. Proposal L298-370 boundaries verified. U+27F9 UTF-8 = E2 9F B9 verified via `python3 -c "print('⟹'.encode('utf-8').hex())"` -> `e29fb9`. |
| 5 | Module context analysis | none | PASS | Verified refs/ sibling directory contains exactly the 6 expected files: doc-discovery.md, escalation-rubric.md, hypothesis-card-template.md, remediation-handoff.md, report-template.md, triage-checklist.md (matches research file 02 inventory). The new file's H1+intro+H2 structure conforms to the convention documented in research file 02 Sections 2/3/4. |
| 6 | Downstream consumer analysis | none | PASS | Task correctly identifies that the corpus has 5 trigger files (Suite integrity bullets) but the intro lists only 4 (omits `confidence-check/SKILL.md`) — accurate per proposal. Task correctly notes hypothesis-card-template.md L105 already pre-references the new corpus file (sibling Change B / PR #89 landed). Task correctly identifies that pytest harness is downstream consumer (deferred). |
| 7 | Test validity | none | PASS | Phase 5 verification is non-trivial: 10 deterministic grep/byte-count checks (a)-(j) covering H2 count (5), Fixture count (9), [V2 merged] bracket count (3), Expected calibrated count (8), Expected behavior count (1), property test rows (5), soft assertion (1), U+27F9 count via two independent methods (literal char + byte-pattern), V2-merged Change F annotation (1), Implementation hook H2 (1). Each check has a documented "expected vs actual" pathology mapping. NOT a rubber-stamp test. |
| 8 | Test coverage of primary use case | none | PASS | All 6 Key Objectives are verified by Phase 5 checks: (1) file creation = Phase 2/3 + Phase 5 file-existence implicit via grep success; (2) 7 provenance markers = grep checks c/i/(implicit in d/e); (3) U+27F9 byte preservation = check (h) dual form; (4) sync mirror = Phase 4.1/4.2; (5) markdownlint pass = Phase 4.3; (6) structural verification = entire Phase 5. |
| 9 | Error path coverage | none | PASS | Each phase includes "If unable to complete..." blocker-logging guidance with templated format. Phase 4.1 explicitly anticipates non-zero exit, missing mirror file, byte-level diff divergence. Phase 4.3 anticipates markdownlint auto-fix mutating content and instructs to re-run Phase 4 from Step 4.1. Phase 5 captures actual-vs-expected counts for each failed check. |
| 10 | Runtime failure path trace | AX-2 | FAIL->FIXED | Same defect as Item 1: the grep -P path would have produced a false "U+27F9 not byte-preserved" pathology signal — a runtime data-flow break. The fixed python3 form correctly traces input bytes -> count -> assertion. |
| 11 | Completion scope honesty | AX-2 | FAIL->FIXED | Step 5.1(a) contained a muddled reference: "confirm with the actual proposal content via research file 01 Section 1+3+4+5+6+7". Research file 01 Section 1 is the OUTSIDE-the-fence proposal metadata block (NOT an H2 in the new file); Section 2 is the H1+intro pair (NOT an H2 either). The five H2 sections correspond to research file 01 Sections **3+4+5+6+7** only — six numbered Sections in the original reference is an internal contradiction with the asserted "exactly 5 H2 sections" count. **Fixed in-place** to "Sections 3+4+5+6+7" with an explanatory parenthetical clarifying why Sections 1 and 2 are excluded. |
| 12 | Ambient dependency completeness | none | PASS | New file path mirrors into `.claude/` via Phase 4.1 (make sync-dev). The hypothesis-card-template.md L105 pre-reference is already in place. No import, registry, or dispatch-table updates needed (corpus is a static markdown file, not code). Frontmatter update protocol (status, dates) covered in Phase 1.1 + Post-Completion. |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg" / "add parameter" sequencing exists in this task — it's a file-creation task with no function signatures involved. Adapted check: verified Phase 2 creates the file with H1+intro BEFORE Phase 3 appends H2 sections (`old_string` anchors require the prior content to exist). Adapted check passes. |
| 14 | Function existence claims | none | PASS | Adapted to value verification: every grep-test expected count is independently verifiable against the proposal text. Counted in proposal extract: H2 (5 — proposal L303, L332, L346, L356, L367); Fixture H3 (9 — L305, L310, L315, L319, L323, L328, L334, L338, L342); [V2 merged] (3 — L334, L338, L342); Expected calibrated (8 — L307, L312, L317, L321, L330, L336, L340, L344); Expected behavior (1 — L325); property rows starting `\| P[1-5] ` (5 — L350-L354); Soft assertion (1 — L354); ⟹ (3 — L350, L351, L352); (V2-merged Change F) (1 — L363); ## Implementation hook... (1 — L367). All 10 counts verified ground truth. |
| 15 | Cross-reference accuracy for templates | none | PASS | Adapted to source verification: spot-checked every fixture's verbatim text against proposal: Fixture 1 L305-308, Fixture 5's `**Expected behavior**:` (asymmetric) at L325, Fixture 7's `[V2 merged]` suffix at L334, P5's `**Soft assertion**` annotation at L354, Suite-integrity bullet 5 `(V2-merged Change F)` at L363, Implementation hook deferral text at L369. All citations match proposal byte-exactly. |

---

## Summary

- Checks passed: 15 / 15 (after 2 in-place fixes applied)
- Checks failed pre-fix: 2 distinct defects (Items 1 & 10 are the SAME defect surfaced via different axes; Item 11 is distinct)
- Critical issues: 1 (grep -P byte-pattern incompatibility — would have produced a false-negative U+27F9 failure that blocked Phase 5)
- Important issues: 1 (Section 1+3+4+5+6+7 muddled reference — internal contradiction with the asserted 5-H2 count)
- Minor issues: 0
- Issues fixed in-place: 2 (both fixes verified)
- Axis lens status: AX-1 active (drift baseline = BUILD_REQUEST GOAL captured); AX-2..AX-5 active

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 5.1 check (h), the `grep -P "\xE2\x9F\xB9"` byte-pattern command | This host's `grep` is `ugrep 7.5.0`, not GNU grep. `ugrep -P "\xE2\x9F\xB9"` does NOT interpret `\xNN` as a literal-byte escape (it requires `\x{27F9}` codepoint form). The command returns exit 1 even when bytes are present (verified empirically: `echo "⟹" \| grep -P "\xE2\x9F\xB9"` -> exit 1). Executor would interpret this as "mojibake / HTML-entity substitution" and incorrectly fail Phase 5, blocking task completion despite a correctly-encoded file. | Replace with `python3 -c "import sys; data=open(PATH,'rb').read(); print(data.count(b'\\xe2\\x9f\\xb9'))"` which is portable and counts byte occurrences (verified: returns 3 on a 3-⟹ input). Applied in-place. |
| 2 | IMPORTANT | Step 5.1 check (a), the parenthetical "confirm with the actual proposal content via research file 01 Section 1+3+4+5+6+7" | Internal contradiction: the same check asserts `^## ` count = exactly 5 (5 H2s), but cites SIX numbered research file 01 Sections as the cross-reference. Research file 01 Section 1 is the OUTSIDE-the-fence proposal metadata (NOT an H2); Section 2 is the H1+intro pair (also NOT an H2). The 5 H2s correspond to research file 01 Sections **3+4+5+6+7** only. An executor following the muddled reference might count 6 H2s and incorrectly flag the file as missing a section. | Corrected to "Sections 3+4+5+6+7" with explanatory parenthetical noting why Sections 1 and 2 are excluded. Applied in-place. |

---

## Actions Taken

- **Fixed Issue 1 (CRITICAL)** in `TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000.md` Step 5.1 check (h) — replaced `grep -P "\xE2\x9F\xB9"` byte-pattern command with portable `python3 -c "...read().count(b'\xe2\x9f\xb9')"` form and added explanatory note about why grep -P is unsuitable on ugrep hosts. Verified the python3 form works (returns 3 on test input).
- **Fixed Issue 2 (IMPORTANT)** in the same file (Step 5.1 check (a)) — replaced "research file 01 Section 1+3+4+5+6+7" with "Sections 3+4+5+6+7" and added explanatory parenthetical noting Sections 1 and 2 are excluded because they reference the outside-the-fence metadata and the H1+intro pair respectively.
- Both fixes verified by Edit tool successful return.

---

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

I relied on the rf-qa task-integrity PASS verdict for the following items (skipped structural re-checking):

- Relied on rf-qa PASS for "proposal L298-370 verbatim verification" -> semantic counterpart verified: independently spot-checked Fixture 1/5/7, P5 row, Suite integrity bullet 5 (`(V2-merged Change F)`), Implementation hook deferral text — all match proposal byte-exactly (Read tool on proposal L290-370).
- Relied on rf-qa PASS for "target file does NOT exist" -> semantic counterpart verified: ran `ls src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` directly -> "No such file or directory" confirmed.
- Relied on rf-qa PASS for "refs/ has 6 sibling files" -> semantic counterpart verified: `ls` of refs/ directory returned the expected 6 files (doc-discovery.md, escalation-rubric.md, hypothesis-card-template.md, remediation-handoff.md, report-template.md, triage-checklist.md).
- Relied on rf-qa PASS for "T4 source directory absent" -> semantic counterpart verified: ran `find . -type d -name "t4-pane-title-20260526-101500"` from worktree root -> empty result.
- Relied on rf-qa PASS for "5 vs 6 H2 discrepancy resolved" -> semantic counterpart verified: counted H2 headings in proposal L298-370 directly (5: L303, L332, L346, L356, L367) — confirmed 5 is correct. Also discovered the AX-2 contradiction in Step 5.1(a)'s parenthetical reference (Issue 2 above).
- Relied on rf-qa PASS for "U+27F9 dual-check approach" -> semantic counterpart verified: ran the actual byte-encoding check `python3 -c "print('⟹'.encode('utf-8').hex())"` -> confirmed `e29fb9` matches the task's claim. AND independently tested `grep -P "\xE2\x9F\xB9"` on this host -> discovered it does NOT work on ugrep (Issue 1 CRITICAL above). rf-qa's structural verdict that the dual-check approach is *present* is correct; my semantic check exposed that one of the two checks would *fail in execution*.
- Relied on rf-qa PASS for "Fixture 5 Expected-behavior asymmetry preserved" -> semantic counterpart verified: confirmed proposal L325 uses `**Expected behavior**:` while L307, L312, L317, L321, L330, L336, L340, L344 use `**Expected calibrated**:` (8 vs 1 asymmetry matches task's check (d) = 8 and check (e) = 1).
- Relied on rf-qa PASS for "deferred pytest harness OUT OF SCOPE" -> semantic counterpart verified: proposal L367-370 read directly — confirms "Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal" verbatim.

**Anti-inflation evidence:** The CRITICAL grep-P defect (Issue 1) and the IMPORTANT Section-1+3+... contradiction (Issue 2) were both discovered by my own tool engagement (running `grep -P` empirically, counting H2 numbered Sections semantically) — NOT by re-running rf-qa structural checks. This is the semantic-counterpart work the anti-inflation rule requires.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on rf-qa PASS for: proposal L298-370 verbatim verification, target file absence, refs/ sibling inventory, T4 source directory absence, 5-vs-6 H2 resolution, U+27F9 dual-check structural presence, Fixture 5 Expected-behavior asymmetry preservation, deferred pytest harness OUT OF SCOPE.

**(b) Independent semantic checks (>=1 required, INV-019):**

- **Empirical execution of `grep -P "\xE2\x9F\xB9"` on this host** — verified by Bash tool: `echo "⟹" | grep -P "\xE2\x9F\xB9"` -> exit 1 (FAIL). Host grep is `ugrep 7.5.0` (verified via `grep --version`). The rf-qa structural PASS did NOT execute this command; it only verified the dual-check approach is *structurally present*. My execution found a CRITICAL runtime defect that rf-qa could not have caught.
- **Semantic count of research file 01 numbered Sections** — verified by Read of research file 01: Section 1 = outside-fence metadata, Section 2 = H1+intro pair, Sections 3-7 = the 5 H2 sections of the new file. The task's "Section 1+3+4+5+6+7" reference is an internal contradiction with the same check's asserted "5 H2 sections" — IMPORTANT-severity AX-2 finding that rf-qa structural checks did not surface.
- **UTF-8 byte encoding of ⟹** — verified by Bash python3: `'⟹'.encode('utf-8').hex()` returns `e29fb9` confirming UTF-8 bytes E2 9F B9 = U+27F9. Independent of rf-qa structural verdict.
- **Markdownlint pre-commit config inspection** — verified by Read of `.pre-commit-config.yaml`: `--fix` arg is enabled; `exclude` pattern is `\.dev/.*` (does NOT exclude src/superclaude/ — confirms Phase 4.3 markdownlint will actually run on the new file).
- **File-size estimate sanity-check** — verified by Bash `sed -n '299,369p' ... | wc -l` -> 71 lines (proposal extract). Task's "~70-90 lines" estimate is accurate. Independent of rf-qa structural verdict.

---

## Confidence

- Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: **100.0%**
- Tool engagement: Read: 5 | Grep: 0 | Glob: 0 | Bash: 7

Each verification cites the specific tool output. Several checks shared evidence (e.g., one Read of research file 01 supported items 4, 14, 15; one Read of the proposal supported items 14, 15; one Bash grep --version supported items 1, 10). No padding. All 15 items verified.

---

## Recommendations

1. **Both fixes already applied in-place** — task file ready for execution. No further structural changes required.
2. **Optional MINOR (not blocking)**: Step 4.3 could be more explicit that markdownlint's `--fix` mode means an auto-fix that mutates content will silently happen — the current Step 4.3 text mentions this possibility and instructs to re-run Phase 4 from Step 4.1 only if the content diverges from proposal text. Consider adding: "If markdownlint auto-fix triggers AND the resulting content still matches proposal L298-370 byte-exactly, no re-sync is needed — just re-run `make verify-sync` to confirm src/ <-> .claude/ parity post-autofix." Not blocking; current guidance is sufficient.
3. **Operational reminder for the executor**: the corpus's *expected scores* (Fixtures 1/2/4/7/8 <= caps) only validate AFTER Changes A and C ship. The task correctly notes this in the frontmatter `depends_on` (Change A and Change C entries) and in research file 01 Section 9 HARD-prerequisite section. This task creates the corpus FILE only; harness execution validation is the deferred follow-up.

---

## VERDICT: PASS

All 15 task-qualitative checks pass after the 2 in-place fixes (1 CRITICAL grep-P portability, 1 IMPORTANT internal Section-reference contradiction). The task file is now executable end-to-end on this host with no false-negative gate failures and no internal contradictions in the structural-verification guidance.

## QA Complete
