## Template-Conformance QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md`
**Lens:** Template-Conformance (checklist a-d: 10 sections present, ordering, no placeholders/sentinels/TODO, ToC matches headers)
**Date:** 2026-11-08
**Template used:** `~/.claude/skills/tech-research/SKILL.md` "Report Structure" (lines 1311-1487) and Assembly rules (lines 1281-1306)

### Checklist results

| Check | Result | Evidence |
|---|---|---|
| (a) All 10 sections present | PASS | Top-level headers for S1-S10 at report lines 31, 78, 476, 629, 742, 874, 1004, 1045, 1265 and 1351; none marked N/A |
| (b) Section order, no merged sections | PASS (with notes) | S1-S10 in template order; deviations only inside sections (6.4/6.5 before the comparison, extra 10.3/10.4), see F8 and F5 |
| (c) No placeholders, sentinels or TODO | FAIL | No TODO/TBD/FIXME/PLACEHOLDER text, but two unresolved `[CONTRADICTION ...]` sentinels remain (lines 384 and 1140), referenced from lines 466, 662, 1279 and 1331 |
| (d) ToC matches headers | FAIL (minor) | ToC lines 10-21: top-level names match; sub-entries are paraphrased and incomplete, see F4 |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | §2.5(c), line 384 (referenced at 466, 662, 1331) | Unresolved assembly sentinel: `[CONTRADICTION: ... Both versions presented for QA resolution.]` on whether `git rev-parse --path-format=absolute --git-path hooks/pre-push` was exercised. synth-01 says [UNVERIFIED]; synth-02 (G-26, §4.5) and synth-04 (R9) say it is answered by web-01 D3. The report therefore states both an open and a resolved answer to the same question. Template assembly rule 7 forbids leftover sentinels. | Resolve in favour of the web-01 D3 evidence (if it holds on re-check): update the 2.5(c) table and the §2 open-question row 3 (line 466), delete the marker at 384, and drop the "see the [CONTRADICTION]" pointers at lines 662 and 1331. |
| 2 | IMPORTANT | §8.6 end, line 1140 (referenced at 1279) | Unresolved assembly sentinel: `[CONTRADICTION ...]` on which file holds the L1 regression tests. Phase 6.7 (synth-03) names `tests/hooks/test_launch_level_guard_with_identity.py`; §9 rows 7, 8 and 29 (synth-04) name `tests/hooks/test_launch_level_guard.py`. Both files exist (Glob confirmed), so a reader of the plan cannot tell where the test goes. | Choose one target file (or state that each covers a distinct case), make Phase 6.7 and §9 rows 7, 8 and 29 agree, delete the marker at 1140 and the pointer at 1279. |
| 3 | IMPORTANT | §8.1-8.7 | Required template fields missing: none of the seven phases has the template's **Goal:** or **Dependencies:** line (Grep for `\*\*Goal` and `\*\*Dependencies` returns no match). Phase ordering dependencies (for example Phase 6 tests depending on Phases 1-5) are left implicit, which reduces the plan's actionability. | Add a **Goal:** and a **Dependencies:** line under each phase header 8.1-8.7. |
| 4 | MINOR | ToC, lines 10-21 | Sub-entries are paraphrases rather than the actual header text (for example "4.1 G-1 to G-43", "5.4 recommendations", "9.2 unverified claims", "2.1 L1 text guard"); sub-entries have no anchor links; the 2.5 level-4 subsections (a)-(f) and phases 8.1-8.7 are collapsed or omitted. Assembly rule 4 says the ToC is generated from the actual headers. | Regenerate the ToC from the real `##`/`###` headers with anchor links. |
| 5 | MINOR | §10.1 | Codebase Research table uses columns File / Topic / Status / Key finding instead of the template's File / Topic / Agent Type; the Agent Type column is missing. Extra subsections 10.3/10.4 are additions beyond the template. | Add the Agent Type column (extra columns may stay). |
| 6 | MINOR | §10.4, line 1416 | Evidence list deferred elsewhere: "Later gate, validation and reflect reports: see `qa/` and `reflect/post/`; the final list is in the Task Log." The trail is not self-contained. | List the `qa/` report files by name (28 exist at review time). |
| 7 | MINOR | §5.1, §5.2 | Relevance values outside the template vocabulary HIGH/MEDIUM/LOW ("LOW-MEDIUM" at W1-20, "HIGH (JGit and isomorphic-git MEDIUM)" at W1-25); the Relationship column is renamed "Relation to 04" and uses values outside supports/extends/contradicts ("Neither", "EXPLAINS", "Agrees with..."). | Normalise to the template vocabularies; move qualifiers into a Notes cell. |
| 8 | MINOR | §6 | Option blocks use **Placement.** instead of the template's **Description:** and **How it works:**; Effort is Medium / Medium-high / High instead of XS-XL; sub-choices 6.4 and 6.5 sit between the options and the comparison; the 6.6 comparison lacks Maintainability, Integration complexity and Reuse potential rows and uses "Coexistence risk" for Risk. | Rename the labels, map Effort to XS-XL, add the missing comparison rows, and move 6.4/6.5 after the comparison or into §7. |
| 9 | MINOR | §7, line 1006 | Template labels **Recommended approach:** and **Rationale:** absent; the report uses "**Recommended: ...**" plus a reasons table. Content is present. | Rename to the template labels. |
| 10 | MINOR | §4.1, lines 658-679 | Several Gap rows use "—" as a placeholder cell for Current or Target State (for example G-22, G-23, G-27, G-29, G-30, G-40, G-43; G-41 uses it in Notes). Empty-value dashes read as unfilled cells. | Write "n/a (resolved)", "not measured" or the actual state in each cell. |
| 11 | MINOR | Header, lines 25-27 | Non-template "Source key" and "Tags" paragraphs between the ToC and S1. Useful, but not in the template. | Keep, or move under the header block; recorded as a note only. |
| 12 | MINOR | §10, line 1382 | States synth-03's OQ-1 to OQ-20 "are carried as Section 9 rows" with no OQ-to-row mapping, so the claim cannot be checked from the report. | Add an OQ-n to §9 row mapping, or remove the claim. |

### Summary

- Total findings: 12
- Critical: 0
- Important: 3
- Minor: 9

Verdict: FAIL (0 critical + 3 important; 9 minor findings listed as notes)

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 10 | Grep: 6 | Glob: 3 | Bash: 0
