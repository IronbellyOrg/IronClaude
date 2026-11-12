# Reviewer 3 card with blind calibration (merge input, run 2)

Weight findings by the calibration: refuted findings carry no weight; weakened findings use calibrated_severity where given.

## Reviewer card
```yaml
# Written by the orchestrator verbatim from reflect-reviewer 3's returned YAML (read-only agent).
schema: "sc-reflect-reviewer-card/v1"
mode: "UC-1 pre-execution"
run: 2
reviewer: 3
persona: "refactorer"
model_slot: "opus"
model_class: "claude-gw-tier1a"
brief: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/reviewer-briefs/reviewer-3.md"
spec: "docs/designs/orchestrator-mode.md"
tasklist: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md"
codegraph_used: true
findings:
  - id: "R3-G1"
    severity: "MEDIUM"
    gap_class: "design-fix"
    tag: "Grounded"
    t1_relation: "refines F4"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:998"
    claim: "The D10 deviation row that item 6.3 writes is incomplete in three cells. (1) The SPEC cell leaves out NFR-003 (SPEC line 132, the `worktree ps --agent-wait` negative) and SPEC lines 323 and 510, which also forbid the flag. (2) The Design cell does not say that the NFR-014 exact-set pin grows from eight to ten templates, although SPEC line 143 requires a test that the allowlist \"equals the pinned set of eight\". (3) The Section cell \"7.3, 11, 15.1\" leaves out 2.2 (the GQ-109 row) and 12 (the NFR-014 row), and item 6.3 edits both. As a result, D10 under-reports how far R5 departs from SPEC."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:998"
      quote: "| D10 | NFR-014 and SPEC lines 310, 500, 504, 562 and 619: `worktree ps` never carries `--agent-wait` |"
    remediation: "Change the D10 SPEC cell to name NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619. Add \"the NFR-014 exact-set pin covers ten templates, not eight\" to the Design cell. Set the Section cell to \"2.2, 7.3, 11, 12, 15.1\"."
  - id: "R3-G2"
    severity: "LOW"
    gap_class: "design-fix"
    tag: "Grounded"
    t1_relation: "confirms F7"
    location: "docs/designs/orchestrator-mode.md:181"
    claim: "The item 6.3 step (8) grep for 'eight\\|8 templates' misses two places that still give the old count: section 4 line 181 \"ALLOWED_ORCA (8)\" and line 196 \"8 read templates\". Neither matches the pattern, so R5 can leave the template count stale in section 4. Also, no item pins zero argv for templates 9 and 10, although OQ-16 says they are not called in Phase 1. Item 10.3 (line 1793) pins zero argv only for `worktree list` and `worktree current`."
    evidence:
      ref: "docs/designs/orchestrator-mode.md:181"
      quote: "ALLOWED_ORCA (8)"
    remediation: "Widen the step (8) grep to 'eight\\|(8)\\|8 read\\|8 templates' and list lines 181 and 196 in the 6.3 Output. Add zero-argv assertions for the two `worktree ps --agent-wait` templates to item 10.3, or state that they may be called."
  - id: "R3-G3"
    severity: "LOW"
    gap_class: "traceability"
    tag: "Grounded"
    t1_relation: "confirms F8"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:163"
    claim: "Key Constraints says eight templates are called in Phase 1. DESIGN 7.3 line 548 says `worktree list` and `worktree current` are allowlisted but never called, and the NFR-003 recording test asserts zero argv for both. So six templates are called in the sweep, plus the 1.0a capture reads."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:163"
      quote: "The Orca allowlist has ten read templates (eight called in Phase 1 plus the two R5 `worktree ps --agent-wait` forms)"
    remediation: "Reword it as \"ten read templates: six called by the sweep, `worktree list` and `worktree current` allowlisted but not called, and the two R5 `worktree ps --agent-wait` forms allowlisted but not called; step 1.0a uses templates 1 to 8\"."
  - id: "R3-G4"
    severity: "LOW"
    gap_class: "design-fix"
    tag: "Grounded"
    t1_relation: "confirms F11"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:838"
    claim: "The 5.11 row text places the draft-name markers in sections 13 and 14. Section 14 starts at DESIGN line 837, and both WC-14 hits being marked (D6 at line 812 and the 1.17 row at line 835) are in section 13. The grep of section 14 finds no hit, so the row text is false and the 5.3 section list over-reaches."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:838"
      quote: "marked the SPEC and REPORT draft names in 13 and 14"
    remediation: "Change \"in 13 and 14\" to \"in 13\", and remove 14 from the 5.3 section list on line 780, unless a section 14 hit is shown."
  - id: "R3-G5"
    severity: "MEDIUM"
    gap_class: "design-fix"
    tag: "Grounded"
    t1_relation: "new"
    location: "docs/designs/orchestrator-mode.md:221"
    claim: "Item 6.3 adds `ALLOWED_ORCA` templates 9 and 10, the two `worktree ps --agent-wait` forms. The extension-point rule in DESIGN section 4 still allows a new template only after a capture. Capture item 11 (line 892) is the NFR-014 check that each template accepts its flags. Item 7.16 explicitly does not run the agent-wait forms (line 1259), and the OQ-1 probe does not record the `--json` form. After Phase 6, the design breaks its own extension rule, and no evidence shows that template 10 parses."
    evidence:
      ref: "docs/designs/orchestrator-mode.md:221"
      quote: "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)"
    remediation: "Item 6.3 should either reword line 221 to \"only after a capture or a recorded owner decision (R5, 2026-11-08)\", or add the two agent-wait forms to the step 1.0a capture under capture item 11. Then record the result in readonly-probe.md."
  - id: "R3-G6"
    severity: "MEDIUM"
    gap_class: "unsound-check"
    tag: "Grounded"
    t1_relation: "new"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1000"
    claim: "The 6.3 Verification (no hit forbids the flag) and the 6.4 pass rule cannot both pass as written. The D10 row that 6.3 writes quotes SPEC as \"`worktree ps` never carries `--agent-wait`\", and the R5 Fix cycle 3 row says INV-005 condition 1 forbade it. Both are hits that forbid the flag, and 6.3 has no historical-text exemption like the one Phase 5 uses. Separately, 6.4 requires a 15.1 hit that allows the flag, but 6.3 step (4) only removes `--agent-wait` from the 15.1 forbidden list and may leave 15.1 with no hit at all."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1005"
      quote: "the hits in 7.3 (the two `ALLOWED_ORCA` templates), 11, 13 (D10) and 15.1 allow it"
    remediation: "Add an exemption to both checks for quoted SPEC text in the D10 row and the section 18 history rows. Have 6.3 step (4) write a positive 15.1 sentence, for example \"`worktree ps --agent-wait` is allowed by R5 but not run in step 1.0a\", so that the 6.4 rule has a hit to match."
  - id: "R3-G7"
    severity: "LOW"
    gap_class: "traceability"
    tag: "[INFERRED]"
    t1_relation: "new"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:998"
    claim: "The section list \"(7.3, 11, 13, 15.1)\" that ends the R5 Fix cycle 3 row in item 6.3 step (7) leaves out 2.2 and 12, although item 6.3 edits the GQ-109 row in 2.2 and the NFR-014 row in 12 (6.3 Output, line 999). The history line would under-report the edit."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:999"
      quote: "[INFERRED] from the 6.3 Output naming the section 12 NFR-014 row and the GQ-109 row, compared with the step (7) section list on line 998"
    remediation: "Change the step (7) list to \"(2.2, 4, 7.3, 11, 12, 13, 15.1)\" so that it matches the sections 6.3 actually touches (include 4 if R3-G2 is applied)."
  - id: "R3-G8"
    severity: "LOW"
    gap_class: "traceability"
    tag: "Grounded"
    t1_relation: "new"
    location: ".dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:415"
    claim: "The R4 5-minute cadence contradicts three SPEC places: line 415 (no cadence in Phase 1), line 532 (no cadence required) and line 583 (OQ-7). Item 5.4 rewrites D6, yet D6 keeps its SPEC cell at lines 404-408 only and its Source cell at SP-27 only. OQ-15 (line 2880) says the cadence departure is recorded in D6, but the cell neither cites the contradicting SPEC lines nor names R4."
    evidence:
      ref: ".dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:415"
      quote: "Phase 1 sets no cadence"
    remediation: "In item 5.4, add SPEC lines 415, 532 and 583 to the D6 SPEC cell, and add \"R4 (owner, 2026-11-08)\" to its Source cell."
  - id: "R3-G9"
    severity: "LOW"
    gap_class: "missing-reuse"
    tag: "Grounded"
    t1_relation: "new"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:148"
    claim: "Source Areas names the reflect `_git` seam as the pattern to follow, but the item 8.5 Context (line 1447), which builds the probes `_git` seam, does not cite `src/superclaude/cli/reflect/config.py:64-78`. That helper runs git with `-C`, `check=True` and `timeout=10`, while the design's `_git` uses `--no-optional-locks`, an env override, `check=False` and `GitCallFailed`. Without the citation and a list of differences, the executor may copy `check=True` or build the seam from scratch. Item 9.1 does this kind of comparison for `_publish`."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:148"
      quote: "`superclaude.cli.reflect` (the `_git` seam pattern)"
    remediation: "Cite `src/superclaude/cli/reflect/config.py:64-78` in the item 8.5 Context. State that only the seam shape is reused, and that `--no-optional-locks`, the env override, `check=False` and `GitCallFailed` differ from it."
  - id: "R3-G10"
    severity: "LOW"
    gap_class: "traceability"
    tag: "Grounded"
    t1_relation: "new"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1627"
    claim: "The item 9.1 Action counts five helpers plus `_publish`. DESIGN 7.1 (lines 436-442) gives `run`, four helpers (`_parse_window`, `_find_root`, `_check_output`, `_check_run_ids`) and `_publish`. The wrong count invites the executor to invent a fifth helper, which would be scope creep."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1627"
      quote: "the five helpers and `_publish`"
    remediation: "Change it to \"the four helpers (`_parse_window`, `_find_root`, `_check_output`, `_check_run_ids`) and `_publish`\"."
  - id: "R3-G11"
    severity: "LOW"
    gap_class: "test-plan"
    tag: "Grounded"
    t1_relation: "new"
    location: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2881"
    claim: "OQ-16 says no fixture covers templates 9 and 10. Item 6.3 step (3) adds a positive agent-wait case to the 15.1 and 11 test plan, and item 10.3 (line 1793) pins ten templates with a positive agent-wait case. The open-question record contradicts the plan, so a later reviewer cannot tell which statement is true."
    evidence:
      ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2881"
      quote: "step 1.0a runs only templates 1 to 8 and no fixture covers templates 9 and 10"
    remediation: "Reword OQ-16 as \"no live capture covers templates 9 and 10; the allowlist test in item 10.3 covers them as unit cases\"."
row_coverage:
  - id: "R3-B1"
    verdict: "covered"
    agrees_with_t1: true
    items: ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.25"]
    evidence: "TASKLIST lines 244-286 and 412"
    tag: "Grounded"
    note: "Phase 2 edits and gate are present."
  - id: "R3-B2"
    verdict: "covered"
    agrees_with_t1: true
    items: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.23"]
    evidence: "TASKLIST lines 425-453 and 579"
    tag: "Grounded"
    note: "Phase 3 edits and gate are present."
  - id: "R3-B3"
    verdict: "covered"
    agrees_with_t1: true
    items: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.24"]
    evidence: "TASKLIST lines 592-627 and 753"
    tag: "Grounded"
    note: "Phase 4 edits and gate are present."
  - id: "G-1"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row; delivering items not re-read item by item"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INV-005"
    verdict: "covered"
    agrees_with_t1: true
    items: ["6.3", "6.4", "10.3"]
    evidence: "TASKLIST lines 998-1005 and 1793"
    tag: "Grounded"
    note: "Covered, but the D10 record is incomplete (R3-G1) and the check is unsound (R3-G6)."
  - id: "INV-017"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "R1"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Routing row in DESIGN section 9; the exact item-to-row mapping comes from T1."
  - id: "R2"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Mapping comes from T1."
  - id: "R3"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Mapping comes from T1."
  - id: "R4"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Routing row R4, not design fix R4."
  - id: "R5"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Routing row R5, not design fix R5."
  - id: "R6"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Mapping comes from T1."
  - id: "R7"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Mapping comes from T1."
  - id: "R8"
    verdict: "covered"
    agrees_with_t1: true
    items: ["13.1-13.8"]
    evidence: "TASKLIST lines 2258-2307"
    tag: "[INFERRED]"
    note: "Mapping comes from T1."
  - id: "INF-002"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-003"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-004"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-006"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "Agrees with T1 status."
  - id: "INF-007"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "Agrees with T1 status."
  - id: "INF-009"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "Agrees with T1 status."
  - id: "INF-010"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-011"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-012"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-013"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-014"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: []
    evidence: "Stated in the Execution Context only"
    tag: "[INFERRED]"
    note: "No checklist item delivers it; it is a constraint, not an action."
  - id: "INF-015"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-016"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-021"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-022"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-023"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "Agrees with T1 status."
  - id: "INF-025"
    verdict: "covered"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "No contrary evidence found."
  - id: "INF-026"
    verdict: "covered-in-substance"
    agrees_with_t1: true
    items: ["per T1 matrix"]
    evidence: "T1 matrix row"
    tag: "[INFERRED]"
    note: "Agrees with T1 status."
best_practice_compliance:
  grade: 4
  scale: "0 = unusable, 5 = executable as written with no rework"
  reasons:
    - "The design-fix phases are well ordered, re-anchored to master 5dc29d23, and each has a gate."
    - "R5 matches the owner decision \"Allow it, no conditions needed.\", and the related scope (templates 9 and 10, ClassifiedRow and the dimension fields) is authorized by the owner and by OQ-11, OQ-14 and OQ-16. No unauthorized scope creep was found."
    - "Item 9.1 shows good reuse discipline for `_publish`, while item 8.5 does not do the same for `_git` (R3-G9)."
    - "The R5 grep checks are unsound: they would fail on the historical quotes and miss section 4 (R3-G2, R3-G6). The D10 and D6 records under-report the SPEC departures (R3-G1, R3-G8)."
self_reported_confidence: 0.75
confidence_rationale: "All findings on the design-fix and R5 edits are grounded in DESIGN, SPEC and TASKLIST lines I read. Row coverage for the G-1, INV-017, R1 to R8 and INF rows relies on the T1 matrix item mapping and was not re-read item by item, so those rows are tagged [INFERRED]."
summary:
  rows_audited: 32
  rows_disagreeing_with_t1: 0
  findings_high: 0
  findings_medium: 3
  findings_low: 8
```

## Blind calibration
```yaml
# Written by the orchestrator verbatim from the confidence-calibrator's returned YAML (read-only agent).
card_ref: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/reviewer-cards/reviewer-3-card.yaml"
dimensions:
  citation_grounding:
    score: 0.80
    reason: "All 11 findings carry a location and a quoted snippet, and 10 of the 11 quotes matched the cited line verbatim. R3-G7 is the exception: its quote field holds a reviewer note, not file text. Some citations omit the file (the SPEC lines resolve to merged-requirements.md, and line 1259 resolves to the tasklist). About 21 of the 32 coverage rows cite only T1 matrix row with an INFERRED tag. The card marks these itself, so the grounding gap is disclosed, but it is still a gap."
  coverage_completeness:
    score: 0.70
    reason: "All 32 rows are audited and the card gives the zero disagreements with T1 as a count. Only three phase rows (R3-B1 to R3-B3) and INV-005 were checked item by item. The G-1, INV-017, R1 to R8 and INF rows rely on the T1 matrix and say so (partial coverage with an explicit gap registry). Findings go deep on the R5 and D6 edits and on items 5.x, 6.x, 8.5, 9.1 and 10.3. The rest of the tasklist got little independent review."
  deviation_classification_clarity:
    score: 0.85
    reason: "Each finding has exactly one gap_class, one severity, one tag and one t1_relation (new, confirms or refines). There is no hedging. Severity is mostly defensible. R3-G5 is rated MEDIUM, but the owner decision and tasklist line 1259 already give an exemption path, so LOW would fit better. The card does not use the Aligned, Refinement, Drift and Regression labels. It uses its own taxonomy consistently."
  risk_surface_coverage:
    score: 0.70
    reason: "Findings cover the stale template count, an unsound mechanical check that would fail on its own historical quotes, an allowlist template with no evidence that it parses, and a possible executor miscopy of the git seam. There is no blast-radius reasoning on what running the agent-wait forms means for the INV-005 lock-safety argument. SPEC line 510 says the flag turns on terminal wait-state reads. The card also reports no HIGH findings and no execution-order or rollback risks."
  recommendation_actionability:
    score: 0.90
    reason: "Every finding gives a concrete edit: replacement wording, exact cell values, a widened grep pattern, or a line to add to a named item (6.3, 5.4, 8.5, 9.1, 10.3, OQ-16). Two weaknesses: few remediations state how to verify the fix, and R3-G8 asks for an edit that item 5.4 explicitly forbids (change nothing else in that row)."
calibrated_confidence: 0.79
self_reported_confidence: 0.75
calibration_delta: "+0.04. The card under-claims slightly. Its findings held up well on spot-check, but the many T1-inherited coverage rows and the missing blast-radius analysis keep the score below 0.85."
citations_checked: 36
citations_failed: 0
citations_unverifiable_notes:
  - "R3-G7 evidence.quote is not text from the cited file. It is a reviewer note. The substance still matched tasklist lines 998 and 999, so it was not counted as a failed citation."
  - "The row_coverage evidence ranges (tasklist lines 244-286, 412, 425-453, 579, 592-627, 753, 2258-2307) were not read. The 21 rows that rely on the T1 matrix cannot be verified from this card alone."
  - "R3-G4 was checked against the 5.3 hit list at tasklist lines 780 to 783 and the section 14 start at design line 837. I did not grep section 14 itself for WC-14."
  - "The R3-G9 differences in the design _git seam (no-optional-locks, env override, check=False, GitCallFailed) were confirmed from tasklist line 1447 and 1448 text, not from the design section 7.3 lines."
  - "R3-G1 and R3-G7 say the GQ-109 row sits in section 2.2. Tasklist line 997 only says near line 66, and I did not read the design there."
  - "R3-G5 says the OQ-1 probe does not record the json form of the agent-wait template. I did not check that."
  - "R3-G3 and R3-G1 depend on design line 548 for the claim that templates 7 and 8 are never called by code. This was confirmed. I did not independently count six called templates."
per_finding_check:
  - id: "R3-G1"
    verdict: "confirmed"
    note: "Tasklist line 998 D10 row and its Section cell (7.3, 11, 15.1) match the quote. SPEC lines 132, 143, 323, 510 all forbid the flag or pin eight templates. Line 999 Output names section 12 and the GQ-109 row, so the Section cell under-reports."
  - id: "R3-G2"
    verdict: "confirmed"
    note: "Design line 181 reads ALLOWED_ORCA (8) and line 196 reads 8 read templates. Neither matches the grep pattern eight or 8 templates. Tasklist line 1793 pins zero argv only for worktree list and worktree current."
  - id: "R3-G3"
    verdict: "weakened"
    note: "Tasklist line 163 quote and design line 548 are accurate. Step 1.0a runs templates 1 to 8 including list and current (line 1257 and 1258), so the phrase eight called in Phase 1 is imprecise but not false. This is a wording issue."
  - id: "R3-G4"
    verdict: "confirmed"
    note: "Tasklist line 838 says in 13 and 14. Design line 837 starts section 14, and the D6 (812) and 1.17 (835) hits are in section 13. The 5.3 hit list names no section 14 hit."
  - id: "R3-G5"
    verdict: "confirmed"
    note: "Design line 221 quote matches. Capture item 11 at design line 892 does not cover the agent-wait forms, and tasklist line 1259 says they are not run in step 1.0a. Severity MEDIUM is arguable because the owner decision is the stated override."
  - id: "R3-G6"
    verdict: "weakened"
    note: "Tasklist line 1005 quote matches. The 15.1 half holds: step (4) only removes the flag from the forbidden list, and 6.4 needs a 15.1 hit that allows it. The D10 half is overstated because the D10 row's design cell does say the flag is allowed. The claim that both checks cannot pass is too strong, though the checks are ambiguous."
  - id: "R3-G7"
    verdict: "confirmed"
    note: "Step (7) list at tasklist line 998 omits 2.2 and 12, while line 999 names them. The finding overlaps R3-G1 and its quote field is a note, not file text."
  - id: "R3-G8"
    verdict: "weakened"
    note: "SPEC lines 415, 532 and 583 do say no cadence, and the D6 SPEC cell (design line 812) cites only 404-408 with source SP-27. Item 5.4 (tasklist line 789) already cites lines 415 and 583 and says change nothing else in the D6 row. OQ-15 also records it. The remedy conflicts with the item as written."
  - id: "R3-G9"
    verdict: "confirmed"
    note: "Tasklist line 148 quote matches. Reflect config.py lines 64 to 78 use -C, check=True and timeout=10. Tasklist line 1447 and 1448 build a different _git seam and do not cite config.py."
  - id: "R3-G10"
    verdict: "confirmed"
    note: "Tasklist line 1627 says the five helpers and _publish. Design lines 436 to 442 list four helpers plus _publish, with run and the group separate."
  - id: "R3-G11"
    verdict: "weakened"
    note: "OQ-16 at tasklist line 2881 matches the quote, and item 10.3 at line 1793 covers the two templates with a positive unit case. OQ-16 speaks of step 1.0a fixtures, so the two statements are loosely inconsistent rather than contradictory."
calibrator_model_class: "sonnet"
reviewer_model_class: "opus"
```
