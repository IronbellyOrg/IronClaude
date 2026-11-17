# Refactoring Plan (Step 4)

## Overview
- Base variant: V1 (`variant-1-original.md`, analyzer, sonnet class).
- Incorporated: V2 (earlier-finding checks, base-text comparison, Task 2 cap pin), V3 (Task 6 walk, tracked-files scan, registry row model), invariant probe (`invariant-probe.md`), debate final grades (`debate/round2-advocate-3.md` section 3).
- Output: `merged-review-card.md` in the same folder. Review status: auto-approved.
- Merged finding list (IDs G1 to G14). Grades are the settled debate grades; MEDIUM means a non-blocking warning (a real weakness that is not a wrong result by itself) and is reported as non-blocking.

## Planned Changes

| # | Merged finding | Grade | Built from | Notes for the executor |
|---|---|---|---|---|
| 1 | G1 Task 1 acceptance line P4:37 cannot be met (stage 3 summary says the window runs later, S3:158, S3:162); fix: check the ledger go row, require the summary to exist and quote RT1 and RT2; the ledger has no column for window evidence (README:15), so say where the window result is recorded | blocking | V1 F1, V2 D2, V3 F1, INV-010, INV-018 | keep V1 F1 citations, add INV-010 sentence |
| 2 | G2 Task 5 acceptance P4:89 removes `follow-up candidates` that `tests/skills/test_review_severity_mapping.py` pins on both spec-panel surfaces (lines 55, 58, 71, 72); no stage 4 task re-pins or runs it; conditional on stage 3 Task 8 as written (S3:122 names no spec-panel text; S3:125 needs the test green with spec-panel unchanged); FR-8 line `spec-panel.md:332` is also reached by the grep | blocking | V1 F2 and F5, INV-019, round 2 evidence | state the condition and the one grep that settles it (`grep -n "follow-up candidates\|once per loop" tests/skills/test_review_severity_mapping.py` after stage 3) |
| 3 | G3 pinning tests never run after the last edit: `test_review_severity_rule.py`, `test_review_brief_placement.py:134` (plugin prompt must stay a byte copy of `document_review_loop_prompts.md`; Task 5 says edit in place), `test_review_prompt_overrides.py` (Task 2 only), `tests/skills/test_worker_contract.py:893-926` (reads the Unattended section Task 5 edits); one final run in Task 6 | MEDIUM | V1 F6, V3 F4, INV-008, INV-016, INV-020 | the probe raised V1 F6 from minor |
| 4 | G4 Task 5 cannot be applied to the plugin twin as worded: `plugins/superclaude/commands/spec-panel.md` has no `## Unattended mode` section (source has it at :455); P4:84 never orders the pointer that P4:90 expects; no plugin carrier can name the plugin mirror (byte-copy rule on the prompts twin; precedent `${CLAUDE_PLUGIN_ROOT}` fallback in `test_review_brief_placement.py:129-138`) | MEDIUM | V1 F7, INV-006, INV-007 | verified by orchestrator: grep finds the section only in the source |
| 5 | G5 Task 5's narrowing is not checked: P4:84's parenthesis restates today's Grading bullet (PANEL:259) and no acceptance line checks that the `classified as **CRITICAL** severity` sentence (PANEL:372) changed | MEDIUM | INV-012 | |
| 6 | G6 gate checks run after the edits; with C-001 unfixed a halt after five template edits cannot be corrected in place because `/sc:implement` fails on a changed plan (README:3); fix the plan before the first task | MEDIUM | V1 F8, INV-017 | probe raised from minor |
| 7 | G7 Tasks 1 and 3 name "the allow-list of the stage 3 scan test"; the list is the "Merge-rule allow-list" section of `refs/scale-map.md` | minor | V1 F3, V3 F5 | |
| 8 | G8 Task 3 line 3: tdd file holds only lowercase "after 2 fix cycles" at :125 | minor | V1 F4 | |
| 9 | G9 acceptance lines not pinned by content ("T1 passes" with no command, "consumer-line instruction", "the L1 merge text") | minor | V1 F9, V3 F4 first half | |
| 10 | G10 Task 2 has no cap-sentence line (request line 12) and no check that `document_review_loop_prompts.md` lost the Medium wording | minor | V2 D3, INV-016 | |
| 11 | G11 strict T2 reads git-tracked files and Task 6 never stages the copied folder, so the reverse-scan half of P4:102 is vacuous | minor | V3 F2 | parity (T15) still binds the mirror to the source |
| 12 | G12 registry row model: a second `canonical` row with a repo path versus the `plugin` surface; pins on 1 canonical row and 19 rows (S1:100, S1:209) | minor | V3 F3, INV-005 | conditional on the stage 1 test |
| 13 | G13 strict T2 could trip on unregistered files holding the fence opener or the old sentence (stage 1 doctor check), with no Task 6 step to register or exempt them | minor (conditional) | round 2 N-1, INV-014 | a grep before the switch settles it |
| 14 | G14 small gaps: Task 1's OD16 edit near `agent_template_qa.md:333` has no check (INV-013); `refs/scale-map.md` carries repo paths into the plugin copy (INV-015); no line reads that the stage 3 package is done (INV-011); Task 7 does not say the audit-window sentence ends the summary | minor | INV-013, INV-015, INV-011, V2 note | |

## Earlier-review findings (section "Resolution of the earlier review")
From V2 and V3 and the T1 card: F3, F9, F13 (allow-list ordering): resolved by the order registry row, allow-list entry, copy, tests (P4:99); the existence check would fail between steps but no test runs there (V3 walk, INV-003). F4 (analysis template): resolved (P4:33, P4:38, P4:39; INV-002 counts 11 digest carriers). F5, F12 (T3 scope): resolved in text (P4:50, P4:87; S1:209). F6 (later acceptance lines): resolved; no acceptance line is falsified by a later task (P4:24; V2 note, INV-009).

## Changes NOT Being Made
- V2 D1 (plan generated before its preconditions hold): dropped as a process note; P4:20 and P4:36 gate execution and no edit of the plan text can change when it was generated.
- V2 D4 and the matrix omission (C-012), C-015 (consumer line inside a fence, speculative), S-001, S-002, X-001, X-003: dropped by all three advocates (reasons in `debate-transcript.md`).

## Risk Summary
Low: all changes are additive wording of a review card; no repository file is edited.

## Review Status
auto-approved
