# Reviewer 3 card with its blind calibration attached (Wave 3C), for the Wave 4 adversarial merge.
# Part 1: reviewer card
# Saved verbatim by the orchestrator from the read-only reflect-reviewer's returned card.
schema: sc-reflect-reviewer-card/v1
mode: UC-1 pre-execution
reviewer: 3
persona: refactorer
model_class: claude-gw-tier1a
brief: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-briefs/reviewer-3.md
spec: docs/designs/orchestrator-mode.md
tasklist: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
codegraph_used: false
# TL below means the tasklist path above.
row_verdicts:
  - {id: R1, verdict: covered, items: ["13.2"], evidence: "TL:2263; docs/designs/orchestrator-mode.md:692-701", tag: Grounded, note: "Routing row edit is planned in 13.2."}
  - {id: R2, verdict: covered, items: ["5.2", "13.1"], evidence: "TL:771; TL:2256-2261", tag: Grounded, note: "13.1 carries the R4 bound (TL:2258, TL:2260)."}
  - {id: R3, verdict: covered, items: ["13.4"], evidence: "TL:2277-2282", tag: Grounded, note: "10.2 (TL:1783) matches the row on keywords only and does not edit the routed file. That match is false; 13.4 is the real coverage."}
  - {id: R4, verdict: covered, items: ["13.3"], evidence: "TL:2270", tag: Grounded, note: ""}
  - {id: R5, verdict: covered, items: ["11.2"], evidence: "TL:1957-1962", tag: Grounded, note: "Item 6.4 shows that the section 9 R5 row and the Fix cycle 3 R5 row are different rows (TL:1003)."}
  - {id: R6, verdict: covered, items: ["13.5"], evidence: "TL:2284", tag: Grounded, note: ""}
  - {id: R7, verdict: covered, items: ["12.4"], evidence: "TL:2124-2129", tag: Grounded, note: ""}
  - {id: R8, verdict: covered, items: ["5.9", "13.6"], evidence: "TL:820; TL:2291-2296; docs/designs/orchestrator-mode.md:701", tag: Grounded, note: "13.6 goes beyond R8. See R3-G6."}
  - {id: FR-010, verdict: covered-in-substance, items: ["2.5", "3.3", "4.4"], evidence: "TL:270; TL:437; TL:611", tag: Grounded, note: "The list-incomplete fixtures and notes are planned. The transcript rule for a single row outside the window is lost. See R3-G1."}
  - {id: FR-023, verdict: covered, items: ["5.3"], evidence: "TL:778", tag: Grounded, note: ""}
  - {id: NFR-003, verdict: covered-in-substance, items: ["2.16"], evidence: "TL:347", tag: "[INFERRED]", note: "2.16 is a SPEC-fidelity QA lens, not an edit. It checks the requirement only indirectly."}
  - {id: NFR-014, verdict: covered, items: ["6.1", "6.3"], evidence: "TL:980; TL:994", tag: Grounded, note: ""}
  - {id: GQ-103, verdict: covered, items: ["2.3"], evidence: "TL:256", tag: Grounded, note: ""}
  - {id: D6, verdict: covered, items: ["5.3", "5.4"], evidence: "TL:778; TL:785; docs/designs/orchestrator-mode.md:812", tag: Grounded, note: "D6 records the cadence change, but the owner never approves it. See R3-G4."}
  - {id: D9, verdict: covered, items: ["3.3"], evidence: "TL:437", tag: Grounded, note: ""}
  - {id: SP-27, verdict: covered, items: ["5.4"], evidence: "TL:785-789", tag: Grounded, note: "The appended sentence is kept, consistent with the rule at docs/designs/orchestrator-mode.md:690."}
  - {id: SP-29, verdict: covered, items: ["3.3"], evidence: "TL:437", tag: Grounded, note: ""}
  - {id: step-1.0a, verdict: covered, items: ["2.4"], evidence: "TL:263", tag: Grounded, note: ""}
  - {id: step-1.7, verdict: covered, items: ["5.6"], evidence: "TL:799", tag: Grounded, note: ""}
  - {id: step-1.16a, verdict: covered, items: ["5.7"], evidence: "TL:806", tag: Grounded, note: "Record-only step. 5.12 greps for it (TL:843)."}
  - {id: step-1.17, verdict: covered, items: ["5.3"], evidence: "TL:778; docs/designs/orchestrator-mode.md:835", tag: Grounded, note: "Marked as a historical name."}
  - {id: step-1.19, verdict: covered-in-substance, items: ["5.7"], evidence: "TL:806", tag: Grounded, note: "The master test constraints are recorded but not restated as a separate step."}
  - {id: INF-005, verdict: false-match, items: ["2.12"], evidence: "TL:319", tag: Grounded, note: "2.12 is an actionability QA lens and does not address the B1 inference."}
  - {id: INF-014, verdict: false-match, items: ["5.4"], evidence: "TL:785", tag: Grounded, note: "5.4 records D6. It does not implement the 'this design wins' precedence."}
findings:
  - id: R3-G1
    gap_class: design-fix
    severity: MEDIUM
    tag: Grounded
    t1_relation: new
    claim: "R3-B1 edit 4 deletes 'and that transcript is None with the same note' from the sentence about a single row outside the window. The R3-B2 text that replaces it covers only 'several scoped Dispatch rows'. After both edits, DESIGN 7.2 no longer says what the transcript is when one row lies outside the window, yet the fixtures still expect S None."
    evidence: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md:90; .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md:148; .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md:115-116; TL:249; TL:423"
    recommendation: "In item 2.2, keep a transcript clause for the single-row case, or word the item 3.1 rule as 'one or more scoped Dispatch rows'. Add a grep check for the clause to 2.4."
  - id: R3-G2
    gap_class: design-fix
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "The fallback in item 3.1, '(as for duplicate Dispatch rows, in this bullet)', is wrong. The duplicate Dispatch rule is in the observation rules, not in the worker bullet."
    evidence: "TL:423; docs/designs/orchestrator-mode.md:494-505; .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md:148"
    recommendation: "Point the fallback at the observation rules (DESIGN 7.2, around line 505), or drop the parenthesis."
  - id: R3-G3
    gap_class: unsound-check
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "The item 5.5 verification greps for ':545', ':865', ':470' and ':398'. DESIGN writes these pins as '(line 545)' and so on, so those four patterns can never match and the check passes without testing anything. The 'line 624' pin is not checked at all. Item 5.10 covers this only in part."
    evidence: "TL:792; TL:827; docs/designs/orchestrator-mode.md:677-680; docs/designs/orchestrator-mode.md:686"
    recommendation: "Grep for 'line 545', 'line 865', 'line 470', 'line 398' and 'line 624', and expect one hit each."
  - id: R3-G4
    gap_class: gate-bypass
    severity: MEDIUM
    tag: Grounded
    t1_relation: refines F9
    claim: "R4 changes the substance of the coordinator rule. It adds a 5-minute cadence and drops 'It sweeps on every wake'. The only authority is builder decision OQ-15, recorded in D6. DESIGN still says owner approval of the rule text is required (status line and open item 20, GQ-11). Items 7.3 and 7.4 ask the owner only for the rule id, WC-16 or an amended WC-1. No item puts the revised text or the departure from 'Phase 1 sets no cadence' to the owner, so the approval gate can pass on an id choice alone."
    evidence: "docs/designs/orchestrator-mode.md:5; docs/designs/orchestrator-mode.md:988; TL:1156-1168; TL:2877; src/superclaude/core/WORKER-CONTRACT.md:110"
    recommendation: "Add the full revised WC-16 text and the cadence difference to the 7.3 decision file. Change the 7.4 completion gate to require owner approval of the text as well as the id."
  - id: R3-G5
    gap_class: partial
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "The Triggers text in item 11.1 says 'the coordinator on every wake' without the R4 bound 'at most once every 5 minutes'. Items 5.2, 5.4 and 13.1 all carry the bound, so the planned code docs will contradict WC-16."
    evidence: "TL:1952; TL:773; TL:787; TL:2258"
    recommendation: "Add 'at most once every 5 minutes' to item 11.1's Triggers wording, matching TL:773."
  - id: R3-G6
    gap_class: scope-creep
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "Item 13.6 adds a CHANGELOG bullet for tests/sweep/ and test_sweep_command.py. Routing row R8 does not list that bullet."
    evidence: "TL:2293; docs/designs/orchestrator-mode.md:701"
    recommendation: "Drop the test bullet, or record it as an authorized addition in the 13.6 Context."
  - id: R3-G7
    gap_class: missing-reuse
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "In item 8.8, the fake patch_git records 'the env the real _git would build'. The fake therefore copies the env-building logic instead of testing it. The reflect conftest precedent swaps only the function and leaves building to the code under test."
    evidence: "TL:1467; tests/cli/reflect/conftest.py:59-74"
    recommendation: "Move argv and env building into a pure helper in the probes module. Unit-test that helper, and have the fake record the values it receives."
  - id: R3-G8
    gap_class: test-plan
    severity: LOW
    tag: Grounded
    t1_relation: confirms F5
    claim: "Boundary B5 holds by construction: no sweep model name is among the contracts exports. However, no item verifies it, and contracts relies on make lint-architecture to catch redefinitions, including dataclass shadowing."
    evidence: "src/superclaude/contracts/__init__.py:1-6; src/superclaude/contracts/__init__.py:35-36; src/superclaude/contracts/__init__.py:302-313; TL:1430"
    recommendation: "Add 'make lint-architecture' to item 8.3's verification, with the expected result 'exit 0'."
  - id: R3-G9
    gap_class: missing-reuse
    severity: LOW
    tag: Grounded
    t1_relation: new
    claim: "This is a positive check. The tasklist says neither publish precedent is a reusable helper, and that is true. recovery.py links without fsync, and atomic.py uses fsync with replace, not link. Reflect _git uses text mode, check=True and no optional-locks env, while the sweep seam needs bytes for -z, check=False and GIT_OPTIONAL_LOCKS=0. Writing a fresh seam is justified. The one thing missing is a test-file pointer to the fsync-plus-link ordering."
    evidence: "src/superclaude/cli/sprint/recovery.py:424-434; src/superclaude/cli/swarm/atomic.py:22-38; src/superclaude/cli/reflect/config.py:64-78"
    recommendation: "No change needed. Optionally, cite atomic.py:31 as the fsync precedent in the _publish item."
  - id: R3-G10
    gap_class: design-fix
    severity: LOW
    tag: Grounded
    t1_relation: confirms F9
    claim: "Phases 2 to 6 are authorized, and they re-anchor by heading, not by line number. The R4 renumbering covers every WC-14 hit in DESIGN: section 8 in 5.1, sections 9 and 10 in 5.2, the rest in 5.3, with D6 and step 1.17 kept as historical names. The anchors are correct on master. R5 is held for the owner: 6.2 requires the owner's words, and option (a) HALTs and re-runs /task-builder. The checks for both totals appear in 2.4, 3.3, 5.3, 5.4, 5.8, 5.12 and 6.4."
    evidence: "TL:764-806; TL:843; TL:987; TL:1003; tests/skills/test_worker_contract.py:25; tests/skills/test_worker_contract.py:155-173; docs/designs/orchestrator-mode.md:659-686"
    recommendation: "No change needed beyond R3-G4."
best_practice_compliance:
  grade: 4
  scale: 0-5
  reasons:
    - "+ Design-fix edits anchor by heading. Every phase has a mechanical gate with the commands written out, and the totals are rechecked in every phase."
    - "+ The R5 owner decision HALTs rather than defaulting. Reuse claims about _publish and _git are correct and justified."
    - "+ Master anchors are correct (test_worker_contract.py:25, 155-173, 382-391; WORKER-CONTRACT.md:110)."
    - "- The owner is asked only for the rule id, not the substantive WC-16 text (R3-G4)."
    - "- The R3-B1 and R3-B2 edits leave a rule gap (R3-G1). Some grep patterns can never match (R3-G3)."
    - "- The wording in phases 8 to 13 is not fully aligned with R4 (R3-G5), and there is small scope creep in 13.6 (R3-G6)."
self_scores:
  citation_grounding: 0.85
  coverage_completeness: 0.80
  deviation_classification_clarity: 0.85
  risk_surface_coverage: 0.75
  recommendation_actionability: 0.85
  C: 0.82
summary:
  rows_audited: 24
  findings_high: 0
  findings_medium: 2
  findings_low: 8

# Part 2: blind calibration (calibrated scores and per-finding verdicts outrank self-reports)
# CAL: # Saved verbatim by the orchestrator from the read-only confidence-calibrator output.
# CAL: card_ref: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-cards/reviewer-3-card.yaml
# CAL: calibrator_model_class: sonnet
# CAL: dimensions:
# CAL:   citation_grounding: 0.88        # about 40 citations read and none failed. TL:423 and TL:792 point at an item heading, not at the exact line that holds the quoted text (TL:425 and TL:796). The items are still identifiable.
# CAL:   coverage_completeness: 0.78     # all 24 rows have a verdict. INF-005 and INF-014 are marked false-match and NFR-003 is only covered in substance, yet none of them produces a finding. No gap registry entry exists for them.
# CAL:   deviation_classification_clarity: 0.78  # every finding has one gap_class and one severity. G9 and G10 are positive confirmations filed as LOW findings. G1 is rated MEDIUM above what the text supports. G7 is labelled missing-reuse though it is a test-design point.
# CAL:   risk_surface_coverage: 0.72     # it catches the owner-approval gate gap (G4), the dead grep patterns (G3) and the transcript-clause ambiguity (G1). It gives little blast-radius reasoning. It does not follow up the false-match rows, and the only MEDIUM finding that stands is a process gate.
# CAL:   recommendation_actionability: 0.85  # most recommendations name an item, a grep string or an expected result. G1 offers two alternatives and G7 asks for a design change with no item target.
# CAL: calibrated_confidence: 0.80
# CAL: self_reported_confidence: 0.82
# CAL: calibration_delta: -0.02  # slight overstatement. The card is well grounded, but it rates G1 too high and it files positive checks as findings.
# CAL: citations_checked: 40
# CAL: citations_failed: 0
# CAL: finding_verdicts:
# CAL:   - id: R3-G1
# CAL:     holds: partly
# CAL:     calibrated_severity: LOW
# CAL:     reason: "Edit 4 does drop the single-row transcript clause (research/04:90). However, the R3-B2 text at research/04:148 speaks of matching rows in general and ends with 'a transcript with a tab-map entry that fails the window takes these notes'. That covers one row. The fixtures at research/04:115-117 pin S None, so this is wording ambiguity, not a lost rule."
# CAL:   - id: R3-G2
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "TL:425 offers '(as for duplicate Dispatch rows, in this bullet)' as an alternative. The duplicate-Dispatch rule is in the observation rules (design:505), not in the worker bullet at design:494. The same text says 'whichever is accurate', so an executor can avoid the error."
# CAL:   - id: R3-G3
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "The 5.5 grep at TL:796 uses ':545', ':865', ':470' and ':398'. Design lines 679-686 write '(line 545)' and the like, so four patterns cannot match. 'line 624' is not in that grep. Item 5.10 (TL:827) and the read-each-line step in 5.5 give partial cover."
# CAL:   - id: R3-G4
# CAL:     holds: yes
# CAL:     calibrated_severity: MEDIUM
# CAL:     reason: "Design line 5 and open item 20 (design:988) require owner approval of the rule text. Items 7.3 and 7.4 (TL:1156-1168) ask only for the rule id. The cadence change is a builder decision (OQ-15, TL:2877). It copies master's already merged line (WORKER-CONTRACT.md:110), so the substance risk is small and the gap is mainly in the gate."
# CAL:   - id: R3-G5
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "TL:1952 says 'the coordinator on every wake' with no bound. Items 5.2 (TL:773) and 13.1 (TL:2258) carry 'at most once every 5 minutes'. It is a wording mismatch in the planned command doc."
# CAL:   - id: R3-G6
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "TL:2293 adds the tests bullet. Design row R8 (design:701) lists only the command, skill, rule id and ignore entry. The extra is harmless and nearly a nit. The card does not mention that the never-as-worker bullet is also beyond R8."
# CAL:   - id: R3-G7
# CAL:     holds: partly
# CAL:     calibrated_severity: LOW
# CAL:     reason: "TL:1467 does say the fake records 'the env the real _git would build'. The reflect precedent (conftest.py:59-74) also replaces the whole _git, so its argv and env building are untested too. The point is a reasonable design preference, not a defect."
# CAL:   - id: R3-G8
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "The contracts exports (__init__.py:302-313) hold no sweep name, and lint-architecture is the guard (__init__.py:1-6, 35-36). The 8.3 verification at TL:1434 lacks it. Sweep models do not redefine contracts constants, so the added check has little value."
# CAL:   - id: R3-G9
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "recovery.py:424-433 links with no fsync, atomic.py:31-32 uses fsync then replace, and config.py:64-78 uses text=True and check=True with no env. The claim is accurate, but it is a confirmation with 'no change needed', so it should not count as a finding."
# CAL:   - id: R3-G10
# CAL:     holds: yes
# CAL:     calibrated_severity: LOW
# CAL:     reason: "test_worker_contract.py:25 and 155-173 match the card, and items 5.2, 5.5 and 6.4 behave as stated (TL:773, TL:796, TL:1003). It is a positive check with no defect, so it is informational only. I did not verify the claimed checks in 2.4, 3.3, 5.8 and 5.12."
