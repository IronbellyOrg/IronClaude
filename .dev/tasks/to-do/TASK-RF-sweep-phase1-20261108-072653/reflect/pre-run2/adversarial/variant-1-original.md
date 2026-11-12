# Reviewer 1 card with blind calibration (merge input, run 2)

Weight findings by the calibration: refuted findings carry no weight; weakened findings use calibrated_severity where given.

## Reviewer card
```yaml
# Written by the orchestrator verbatim from reflect-reviewer 1's returned YAML (read-only agent).
schema: sc-reflect-reviewer-card/v1
mode: UC-1 pre-execution
run: 2
reviewer: 1
persona: analyzer
model_slot: sonnet
model_class: claude-gw-tier1b
brief: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/reviewer-briefs/reviewer-1.md
spec: docs/designs/orchestrator-mode.md
tasklist: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
codegraph_used: false
findings:
  - id: R1-G1
    severity: MEDIUM
    gap_class: gate-bypass
    tag: Grounded
    t1_relation: confirms F1
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1265
    claim: >-
      Step 1.0a may legitimately end in two outcomes that SPEC 7.3 and SPEC section 17 allow: a worker-list cursor template (one extra template) or a run-current --json need (an allowlist change that goes to the owner). Item 7.17 stops only on a field-name difference, so neither outcome has a route to the owner. Items 8.10 and 10.3 fix the allowlist at exactly ten templates and pin the set by exact count. If step 1.0a finds either outcome, the build either breaks SPEC 7.3 (more than ten templates with no owner note) or fails the 8.10 and 10.3 count checks with no instruction on what to do. A paging or plain-output surprise is the kind of result that live capture is meant to surface, so this is a likely case and not a remote one.
    evidence:
      - ref: docs/designs/orchestrator-mode.md:552
        quote: "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field"
      - ref: docs/designs/orchestrator-mode.md:971
        quote: "a `--json` need goes to the owner as an allowlist change"
      - ref: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1485
        quote: "a count of `ALLOWED_ORCA`"
    remediation: >-
      In item 7.17 add a third Branch: if the capture shows a cursor field, or shows that run-current needs --json, write a PENDING owner-note record naming the extra template or the changed template, then a HALT item, using the same Branch 1 and Branch 2 pattern as 7.15. In items 8.10 and 10.3 replace the fixed count of ten with the count recorded in the facts file or the owner note. Check by reading: 7.17 has a cursor or --json branch that ends in a HALT, and 8.10 and 10.3 name where the count comes from.
  - id: R1-G2
    severity: MEDIUM
    gap_class: gate-bypass
    tag: Grounded
    t1_relation: confirms F3
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1142
    claim: >-
      The Phase 7 preamble says every HALT item follows the item 6.2 procedure, but item 6.2 is the "Log the OQ-1 decision (L3, no HALT)" item and holds no HALT procedure or branches. The shared HALT procedure that exists is in the QA Gate Protocol, a different place. Item 7.15 Branch 2 then sets status RESOLVED and resets the task status without requiring the person's own words or a source quote, and Branch 1 triggers only on an empty Run id. Item 14.7 Branch 2 drops the clause that the source quotes the owner's words. The OQ-1 record shows the intended standard (decider named, source quoted), so the PENDING decisions are held to a weaker bar than the one already resolved. An executor can flip a PENDING record to RESOLVED on its own.
    evidence:
      - ref: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1142
        quote: "follows the item 6.2 procedure"
      - ref: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1244
        quote: "set `status: RESOLVED`, log the Run id"
    remediation: >-
      Change the Phase 7 preamble to point at the QA Gate Protocol HALT rule, or copy the Branch 1 and Branch 2 pattern into it. In 7.15, 7.17 and 14.7 make Branch 2 require a source quote of the person's or the owner's own words and a named decider before status RESOLVED may be set. Check by reading: each Branch 2 names the decider and requires the quote, and the preamble pointer resolves to text that exists.
  - id: R1-G3
    severity: MEDIUM
    gap_class: unsound-check
    tag: Grounded
    t1_relation: refines F5
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1249
    claim: >-
      SPEC 15.1 says worker-show and task-list are run once before and once after the capture and must be identical apart from timestamps, and that a difference stops the build. Item 7.16 turns this into a HALT. A live worker's worker-show output can change between the two reads for ordinary reasons (state or activity fields), so the HALT can fire with no real violation of the read-only rule. The method for removing timestamps is also not specified, so two executors could compare differently. This is a plan-side gap: the SPEC states the rule, but the item gives the executor nothing to tell a normal state change from a write. [INFERRED] on how Orca fields behave in a live run.
    evidence:
      - ref: docs/designs/orchestrator-mode.md:875
        quote: "A difference stops the build"
    remediation: >-
      In 7.16 name the fields that are compared (for example the task-list rows and the identifying fields of worker-show) and the exact timestamp-stripping rule, and add a Branch for a difference that is only a state-change field: record it in the facts file and go to the person for a ruling rather than treating it as a silent stop or a silent pass. Check by reading: 7.16 lists the compared fields and the strip rule, and has a branch that ends in a person decision.
  - id: R1-G4
    severity: LOW
    gap_class: gate-bypass
    tag: Grounded
    t1_relation: refines F12
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1249
    claim: >-
      SPEC 15.1 says the live capture is run by the person or the coordinator and never by a test. The TASKLIST has the executing agent run it in item 7.16 (TASKLIST side [INFERRED] from the item text read in the brief). The plan has a precedent for handing a live step to the person (item 14.8 Branch B), but 7.16 does not use it. If the executing agent is neither the person nor the coordinator, the SPEC provenance rule is not met.
    evidence:
      - ref: docs/designs/orchestrator-mode.md:868
        quote: "never by a test"
    remediation: >-
      In 7.16 state who runs the capture (the person or the coordinator) and add the same hand-off Branch B used in 14.8 for the case where the executor is neither. Check by reading: 7.16 names the runner and has the hand-off branch.
  - id: R1-G5
    severity: LOW
    gap_class: unsound-check
    tag: "[INFERRED]"
    t1_relation: confirms F13
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1272
    claim: >-
      The 7.18 grep for the word coder also matches longer words such as encoder, so the check can pass or fail for the wrong reason [INFERRED from the grep pattern as read in the brief]. The 7.16 forbidden-token grep expects a forbidden-list sentence that the 7.16 Action never tells the executor to write [INFERRED from the item text in the brief]. Both checks cannot be judged from the Action as written.
    evidence: []
    remediation: >-
      Anchor the 7.18 pattern with word boundaries (for example a word-boundary form of coder, or the full path segment) and add the forbidden-list sentence to the 7.16 Action or drop that grep. Check by reading: the 7.18 pattern is anchored, and every string 7.16 greps for is written by an Action step.
  - id: R1-G6
    severity: LOW
    gap_class: unsound-check
    tag: "[INFERRED]"
    t1_relation: new
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1249
    claim: >-
      The 7.16 Verification says every command in the capture is one of the eight templates or a file read, but Action step 6 runs echo and ls -la, which are neither [INFERRED from the item text as read in the brief; the exact wording is not re-quoted here]. A literal reader fails the check, and a lax reader learns to skip it. The capture also needs worktree ps and the new agent-wait forms only if step 1.0a touches them, so the template list in the check should match the list in the Action.
    evidence: []
    remediation: >-
      Reword the 7.16 Verification to say "an Orca template from the allowlist, a file read, or echo and ls on local paths". Check by reading: every command in the Action is allowed by the Verification sentence.
  - id: R1-G7
    severity: LOW
    gap_class: gate-bypass
    tag: "[INFERRED]"
    t1_relation: new
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1418
    claim: >-
      Item 8.1 greps the substring status: RESOLVED in the OQ-1 record, which is a sound pre-flight. Later items that depend on the same decision (8.12, 9.1, 9.3, 14.8) rely on that pre-flight or on Context text and do not read the record again. Item 9.3 has no path to re-resolve if the Run id changes after 8.1 passed. [INFERRED from the item list; the effect is small because the OQ-1 record is already RESOLVED and the PENDING decisions are checked at their own gates].
    evidence: []
    remediation: >-
      Add one line to 9.3 and 14.8 saying "re-read the decision file; stop if status is not RESOLVED". Check by reading: each late item that depends on a decision names the file it re-reads.
  - id: R1-G8
    severity: LOW
    gap_class: traceability
    tag: Grounded
    t1_relation: new
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:163
    claim: >-
      Key Constraints says the ten read templates are "eight called in Phase 1 plus the two R5" forms. SPEC 7.3 says worktree list and worktree current are pinned but not called in Phase 1, and that worktree ps --json is the discovery call. The ten includes the two worktree forms that are never called, so "eight called" misstates which templates Phase 1 uses. A reader tracing NFR-014 or NFR-003 from this line will count the wrong set.
    evidence:
      - ref: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:163
        quote: "ten read templates"
      - ref: docs/designs/orchestrator-mode.md:548
        quote: "Phase 1 code does not call them"
    remediation: >-
      Reword line 163 to say ten templates are pinned, and name which of them Phase 1 calls and which are pinned only (worktree list and worktree current). Check by reading: the sentence matches SPEC 7.3.
  - id: R1-G9
    severity: LOW
    gap_class: unsound-check
    tag: "[INFERRED]"
    t1_relation: new
    location: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2467
    claim: >-
      SPEC step 1.28 asks that every hit of the src/superclaude grep is justified. Item 14.5 turns this into "0 scoped hits and a full-tree count of 168", tied to base commit 5dc29d23 [INFERRED from the item text in the brief]. The scoped zero is a good check, but the fixed full-tree count of 168 fails after any unrelated change on the base, and it drops the justification step the SPEC asks for.
    evidence: []
    remediation: >-
      In 14.5 keep the scoped zero-hit check, state the full-tree count as informational against the base, and add one line that any new hit outside the scoped files gets a written justification. Check by reading: the pass condition no longer depends on a fixed total.
row_coverage:
  - {id: FR-001, verdict: covered, agrees_with_t1: true, items: ["9.1", "9.2", "10.6"], evidence: ["docs/designs/orchestrator-mode.md:755", "docs/designs/orchestrator-mode.md:444"], tag: Grounded, note: "Command group and main.py registration are built in 9.1 and 9.2 and tested in 10.6."}
  - {id: FR-002, verdict: covered, agrees_with_t1: true, items: ["8.10", "9.1", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:756", "docs/designs/orchestrator-mode.md:445"], tag: Grounded, note: "bind_run and the binding errors are built in 8.10 and 9.1; the fourth test depends on the run-current capture in 7.14 to 7.17."}
  - {id: FR-003, verdict: covered, agrees_with_t1: true, items: ["9.1", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:757", "docs/designs/orchestrator-mode.md:446"], tag: Grounded, note: "The window parser is in 9.1 and the contract test in 10.7."}
  - {id: FR-004, verdict: covered, agrees_with_t1: true, items: ["9.1", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:758", "docs/designs/orchestrator-mode.md:447"], tag: Grounded, note: "Root walk and output check are in 9.1 and tested in 10.7."}
  - {id: FR-005, verdict: covered, agrees_with_t1: true, items: ["8.3", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:759", "docs/designs/orchestrator-mode.md:448"], tag: Grounded, note: "Result rows and reconciliation are built in 8.3 and tested in 10.7."}
  - {id: FR-006, verdict: covered, agrees_with_t1: true, items: ["8.3", "8.4", "10.2", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:760", "docs/designs/orchestrator-mode.md:449"], tag: Grounded, note: "Rule table in 8.4 with the guard refused case and the report wording test in 10.5."}
  - {id: FR-007, verdict: covered, agrees_with_t1: true, items: ["8.3", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:761", "docs/designs/orchestrator-mode.md:450"], tag: Grounded, note: "SweepContext in 8.3 and classify tests in 10.2 (the range match in the matrix is a lead, the items were read)."}
  - {id: FR-008, verdict: covered, agrees_with_t1: true, items: ["8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:762", "docs/designs/orchestrator-mode.md:451"], tag: Grounded, note: "Fallback rule 9 is built in 8.4 and tested in 10.2."}
  - {id: FR-009, verdict: covered, agrees_with_t1: true, items: ["8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:763", "docs/designs/orchestrator-mode.md:452"], tag: Grounded, note: "Rule 2 decline and note are in 8.4 and tested in 10.2."}
  - {id: FR-010, verdict: covered, agrees_with_t1: true, items: ["2.5", "3.3", "4.1", "4.3", "4.4", "8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:764"], tag: Grounded, note: "Delivery is in 8.4 and 10.2; the phase 2 to 4 items are SPEC edits, not delivery."}
  - {id: FR-011, verdict: covered, agrees_with_t1: true, items: ["8.12", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:765", "docs/designs/orchestrator-mode.md:454"], tag: Grounded, note: "Section order and the sort are in 8.12 and tested in 10.5 although no item carries the FR id."}
  - {id: FR-012, verdict: covered, agrees_with_t1: true, items: ["8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:766", "docs/designs/orchestrator-mode.md:455"], tag: Grounded, note: "safe_to_close rules are in 8.4 and tested in 10.2."}
  - {id: FR-013, verdict: covered, agrees_with_t1: true, items: ["8.4", "10.2", "10.3"], evidence: ["docs/designs/orchestrator-mode.md:767", "docs/designs/orchestrator-mode.md:456"], tag: Grounded, note: "Removable condition in 8.4, tests in 10.2 and the parse_status fixture in 10.3."}
  - {id: FR-014, verdict: covered, agrees_with_t1: true, items: ["8.3", "8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:768", "docs/designs/orchestrator-mode.md:457"], tag: Grounded, note: "Package states and the FINAL line-start rule are built in 8.3 and 8.4 and tested in 10.2."}
  - {id: FR-015, verdict: covered, agrees_with_t1: true, items: ["8.4", "8.5", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:769", "docs/designs/orchestrator-mode.md:458"], tag: Grounded, note: "Shared-package marking in 8.4 and the git argv flag in 8.5."}
  - {id: FR-016, verdict: covered, agrees_with_t1: true, items: ["8.12", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:770", "docs/designs/orchestrator-mode.md:459"], tag: Grounded, note: "sanitize and cell in 8.12 with the injection fixture in 10.5."}
  - {id: FR-017, verdict: covered, agrees_with_t1: true, items: ["9.1", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:771", "docs/designs/orchestrator-mode.md:460"], tag: Grounded, note: "Publish naming and the commit-point print order are in 9.1 and tested in 10.7."}
  - {id: FR-018, verdict: covered, agrees_with_t1: true, items: ["9.1", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:772", "docs/designs/orchestrator-mode.md:461"], tag: Grounded, note: "Exit mapping in 9.1 with one test per exit code in 10.7."}
  - {id: FR-019, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:773", "docs/designs/orchestrator-mode.md:462"], tag: Grounded, note: "Orca unavailable continuation is built in 8.10 and tested in 10.7."}
  - {id: FR-020, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.3", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:774", "docs/designs/orchestrator-mode.md:463"], tag: Grounded, note: "Budget and byte limits in 8.10 with boundary fixtures in 10.3 and the header line test in 10.5."}
  - {id: FR-021, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.3"], evidence: ["docs/designs/orchestrator-mode.md:775", "docs/designs/orchestrator-mode.md:464"], tag: Grounded, note: "Read-only package and the forbidden verb list held in the test are in 8.10 and 10.3."}
  - {id: FR-022, verdict: covered, agrees_with_t1: true, items: ["11.1", "11.3", "11.4"], evidence: ["docs/designs/orchestrator-mode.md:776", "docs/designs/orchestrator-mode.md:465"], tag: Grounded, note: "Command and skill are built in 11.1 and 11.3 and tested in 11.4."}
  - {id: FR-023, verdict: covered, agrees_with_t1: true, items: ["5.3", "12.1", "12.2", "12.3"], evidence: ["docs/designs/orchestrator-mode.md:777", "docs/designs/orchestrator-mode.md:466"], tag: Grounded, note: "Delivered as WC-16 in 12.1 to 12.3 after the phase 5 design edit."}
  - {id: FR-024, verdict: covered-in-substance, agrees_with_t1: true, items: ["11.2", "12.4", "13.1", "13.2", "13.3", "13.4", "13.5", "13.6"], evidence: ["docs/designs/orchestrator-mode.md:778", "docs/designs/orchestrator-mode.md:467"], tag: Grounded, note: "Routing rows R1 to R8 are delivered by name in phase 13, relying on SPEC section 9 and 12; items do not cite FR-024."}
  - {id: FR-025, verdict: covered, agrees_with_t1: true, items: ["8.6", "8.9", "13.7"], evidence: ["docs/designs/orchestrator-mode.md:779", "docs/designs/orchestrator-mode.md:468"], tag: Grounded, note: "The gitignore line is in 8.6 with the real-git test in 8.9."}
  - {id: FR-026, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.3"], evidence: ["docs/designs/orchestrator-mode.md:780", "docs/designs/orchestrator-mode.md:469"], tag: Grounded, note: "Result kinds and parser are in 8.10 and 10.3; case 4 stays gated by the run-current capture, see R1-G1."}
  - {id: NFR-001, verdict: covered, agrees_with_t1: true, items: ["9.1", "10.4", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:781", "docs/designs/orchestrator-mode.md:470"], tag: Grounded, note: "Single write and exit-0 rule are in 9.1 with the snapshot test in 10.4 and the unlink case in 10.7."}
  - {id: NFR-002, verdict: covered, agrees_with_t1: true, items: ["8.5", "8.9"], evidence: ["docs/designs/orchestrator-mode.md:782", "docs/designs/orchestrator-mode.md:471"], tag: Grounded, note: "Git argv and env are set in 8.5 and exercised by the 8.9 real-git test."}
  - {id: NFR-003, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.3"], evidence: ["docs/designs/orchestrator-mode.md:783", "docs/designs/orchestrator-mode.md:472"], tag: Grounded, note: "Allowlist checks in 8.10 and 10.3; the count depends on the R1-G1 route."}
  - {id: NFR-004, verdict: covered, agrees_with_t1: true, items: ["8.4", "8.12", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:784", "docs/designs/orchestrator-mode.md:473"], tag: Grounded, note: "Pure classify and report modules are built in 8.4 and 8.12 with the AST test in 10.2."}
  - {id: NFR-005, verdict: covered, agrees_with_t1: true, items: ["8.3", "8.12", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:785", "docs/designs/orchestrator-mode.md:474"], tag: Grounded, note: "No clock in render and to_json, with an equal-bytes test in 10.5."}
  - {id: NFR-006, verdict: covered, agrees_with_t1: true, items: ["8.2", "10.6"], evidence: ["docs/designs/orchestrator-mode.md:786", "docs/designs/orchestrator-mode.md:475"], tag: Grounded, note: "Lazy attribute loading in 8.2 and the registration test in 10.6."}
  - {id: NFR-007, verdict: covered, agrees_with_t1: true, items: ["8.10", "10.3", "11.3", "11.4"], evidence: ["docs/designs/orchestrator-mode.md:787", "docs/designs/orchestrator-mode.md:476"], tag: Grounded, note: "Ninety second budget in 8.10 and the skill timeout in 11.3, with tests in 10.3 and 11.4."}
  - {id: NFR-008, verdict: covered-in-substance, agrees_with_t1: true, items: ["10.5"], evidence: ["docs/designs/orchestrator-mode.md:788", "docs/designs/orchestrator-mode.md:477"], tag: Grounded, note: "Unscanned reasons flow to could not determine through the source-loss fixture in 10.5; no item names the NFR id."}
  - {id: NFR-009, verdict: covered, agrees_with_t1: true, items: ["8.12", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:789", "docs/designs/orchestrator-mode.md:478"], tag: Grounded, note: "JSON v1 key set is built in 8.12 and tested in 10.7."}
  - {id: NFR-010, verdict: covered, agrees_with_t1: true, items: ["8.4", "10.2"], evidence: ["docs/designs/orchestrator-mode.md:790", "docs/designs/orchestrator-mode.md:479"], tag: Grounded, note: "Rule order is built in 8.4 and pinned by name in 10.2."}
  - {id: NFR-011, verdict: covered, agrees_with_t1: true, items: ["11.1", "11.3", "11.4", "14.5"], evidence: ["docs/designs/orchestrator-mode.md:791", "docs/designs/orchestrator-mode.md:480"], tag: Grounded, note: "Installed-path rule is built in 11.1 and 11.3 and checked by the 14.5 grep, see R1-G9."}
  - {id: NFR-012, verdict: covered-in-substance, agrees_with_t1: true, items: ["14.1", "14.2", "14.3", "14.4"], evidence: ["docs/designs/orchestrator-mode.md:792", "docs/designs/orchestrator-mode.md:481"], tag: Grounded, note: "Repo gates are the step 1.25 to 1.27 commands in 14.1 to 14.4, not named NFR-012."}
  - {id: NFR-013, verdict: covered, agrees_with_t1: true, items: ["8.8", "10.4"], evidence: ["docs/designs/orchestrator-mode.md:793", "docs/designs/orchestrator-mode.md:482"], tag: Grounded, note: "Patched seams and the autouse subprocess guard are in the 8.8 conftest and exercised in 10.4."}
  - {id: NFR-014, verdict: covered, agrees_with_t1: true, items: ["6.3", "8.10", "10.3"], evidence: ["docs/designs/orchestrator-mode.md:794", "docs/designs/orchestrator-mode.md:483"], tag: Grounded, note: "Ten templates after the owner R5 allow decision with an exact-set pin; the fixed count is the gap in R1-G1."}
  - {id: NFR-015, verdict: covered, agrees_with_t1: true, items: ["8.10", "8.12", "10.5"], evidence: ["docs/designs/orchestrator-mode.md:795", "docs/designs/orchestrator-mode.md:484"], tag: Grounded, note: "Version constant and reader are in 8.10 with the lock line shown in 8.12 and tested in 10.5."}
  - {id: step-1.0a, verdict: partial, agrees_with_t1: false, items: ["7.14", "7.15", "7.16", "7.17", "7.18"], evidence: ["docs/designs/orchestrator-mode.md:906", "docs/designs/orchestrator-mode.md:552", "docs/designs/orchestrator-mode.md:875"], tag: Grounded, note: "Capture is delivered, but two outcomes SPEC allows (cursor template, run-current --json need) and a normal live-worker state change have no route, see R1-G1 and R1-G3."}
  - {id: step-1.0b, verdict: covered, agrees_with_t1: true, items: ["7.1", "7.3", "7.5", "7.7", "7.9", "7.11", "7.13"], evidence: ["docs/designs/orchestrator-mode.md:907", "docs/designs/orchestrator-mode.md:Section 8 gate"], tag: Grounded, note: "Each owner decision has a PENDING record and a HALT item; Branch 2 is too weak per R1-G2 but the delivery exists."}
  - {id: step-1.1, verdict: covered, agrees_with_t1: true, items: ["8.2"], evidence: ["docs/designs/orchestrator-mode.md:908"], tag: Grounded, note: "Package skeleton at 8.2 runs after the 8.1 pre-flight; SPEC gate column is satisfied."}
  - {id: step-1.2, verdict: covered, agrees_with_t1: true, items: ["8.3"], evidence: ["docs/designs/orchestrator-mode.md:909"], tag: Grounded, note: "Data types at 8.3 follow 8.2."}
  - {id: step-1.3, verdict: covered, agrees_with_t1: true, items: ["8.4"], evidence: ["docs/designs/orchestrator-mode.md:910"], tag: Grounded, note: "Classifier at 8.4; the D9 gate the SPEC places here is checked by the pre-flight, a stated addition."}
  - {id: step-1.4a, verdict: covered, agrees_with_t1: true, items: ["8.5", "8.6", "8.9"], evidence: ["docs/designs/orchestrator-mode.md:911"], tag: Grounded, note: "The first code commit is not run; the ordering is kept as a working-tree rule with a stated reason."}
  - {id: step-1.4, verdict: covered, agrees_with_t1: true, items: ["8.10", "9.3"], evidence: ["docs/designs/orchestrator-mode.md:912"], tag: Grounded, note: "Probes at 8.10 with the live check moved to 9.3 for a stated reason; the template count depends on R1-G1."}
  - {id: step-1.5, verdict: covered, agrees_with_t1: true, items: ["8.12"], evidence: ["docs/designs/orchestrator-mode.md:913"], tag: Grounded, note: "Report module at 8.12 after the decisions it depends on."}
  - {id: step-1.6, verdict: covered, agrees_with_t1: true, items: ["9.1"], evidence: ["docs/designs/orchestrator-mode.md:914"], tag: Grounded, note: "Command module at 9.1 follows the facts-file gate from 7.17 and 7.18."}
  - {id: step-1.7, verdict: covered, agrees_with_t1: true, items: ["5.6", "9.2"], evidence: ["docs/designs/orchestrator-mode.md:915"], tag: Grounded, note: "Registration is built in 9.2; 5.6 is a SPEC edit and not delivery."}
  - {id: step-1.8, verdict: covered, agrees_with_t1: true, items: ["8.8", "10.1"], evidence: ["docs/designs/orchestrator-mode.md:916"], tag: Grounded, note: "Base conftest moved to 8.8 with a stated reason; fixtures at 10.1 give the new templates 9 and 10 no fixture, covered by the positive test in 10.3."}
  - {id: step-1.9, verdict: covered, agrees_with_t1: true, items: ["10.2"], evidence: ["docs/designs/orchestrator-mode.md:917"], tag: Grounded, note: "Classify tests at 10.2 follow the classifier."}
  - {id: step-1.10, verdict: covered, agrees_with_t1: true, items: ["10.3"], evidence: ["docs/designs/orchestrator-mode.md:918"], tag: Grounded, note: "Allowlist tests at 10.3 pin the ten templates; see R1-G1 for the fixed count."}
  - {id: step-1.11, verdict: covered, agrees_with_t1: true, items: ["10.4"], evidence: ["docs/designs/orchestrator-mode.md:919"], tag: Grounded, note: "Read-only tests at 10.4."}
  - {id: step-1.12, verdict: covered, agrees_with_t1: true, items: ["10.5"], evidence: ["docs/designs/orchestrator-mode.md:920"], tag: Grounded, note: "Report tests at 10.5."}
  - {id: step-1.13, verdict: covered, agrees_with_t1: true, items: ["10.6", "10.7"], evidence: ["docs/designs/orchestrator-mode.md:921"], tag: Grounded, note: "Registration and contract tests at 10.6 and 10.7."}
  - {id: step-1.14, verdict: covered, agrees_with_t1: true, items: ["11.1"], evidence: ["docs/designs/orchestrator-mode.md:922"], tag: Grounded, note: "Command file at 11.1."}
  - {id: step-1.15, verdict: covered, agrees_with_t1: true, items: ["11.3"], evidence: ["docs/designs/orchestrator-mode.md:923"], tag: Grounded, note: "Skill at 11.3 after the OQ gates on the 1.5 and 1.6 outputs."}
  - {id: step-1.16, verdict: covered, agrees_with_t1: true, items: ["11.4"], evidence: ["docs/designs/orchestrator-mode.md:924"], tag: Grounded, note: "Command tests at 11.4."}
  - {id: step-1.16a, verdict: covered, agrees_with_t1: true, items: ["5.7", "7.19"], evidence: ["docs/designs/orchestrator-mode.md:925"], tag: Grounded, note: "Record-only after design fix R4; the files field is dropped for that reason."}
  - {id: step-1.17, verdict: covered, agrees_with_t1: true, items: ["12.1"], evidence: ["docs/designs/orchestrator-mode.md:926", "docs/designs/orchestrator-mode.md:Section 8 gate"], tag: Grounded, note: "Gated by GQ-11 from step 1.0b and by 1.16a, both ordered before phase 12."}
  - {id: step-1.18, verdict: covered, agrees_with_t1: true, items: ["12.2"], evidence: ["docs/designs/orchestrator-mode.md:927"], tag: Grounded, note: "Same gate as 1.17; ordering matches SPEC 15.2."}
  - {id: step-1.19, verdict: covered, agrees_with_t1: true, items: ["12.3"], evidence: ["docs/designs/orchestrator-mode.md:928"], tag: Grounded, note: "Same gate as 1.17; ordering matches SPEC 15.2."}
  - {id: step-1.20, verdict: covered, agrees_with_t1: true, items: ["11.2"], evidence: ["docs/designs/orchestrator-mode.md:929"], tag: Grounded, note: "Command copy at 11.2."}
  - {id: step-1.21, verdict: covered-in-substance, agrees_with_t1: true, items: ["13.1", "13.2"], evidence: ["docs/designs/orchestrator-mode.md:930", "docs/designs/orchestrator-mode.md:467"], tag: Grounded, note: "Delivered as routing rows R1 and R2, relying on SPEC section 9; R2 before R1 is a stated order."}
  - {id: step-1.22, verdict: covered-in-substance, agrees_with_t1: true, items: ["13.3"], evidence: ["docs/designs/orchestrator-mode.md:931"], tag: Grounded, note: "Delivered as routing row R3; R1, R2 and R3 stay together in one working tree."}
  - {id: step-1.23, verdict: covered-in-substance, agrees_with_t1: true, items: ["13.4"], evidence: ["docs/designs/orchestrator-mode.md:932"], tag: Grounded, note: "Same commit as 1.21 becomes the same working tree because the task never commits."}
  - {id: step-1.24, verdict: covered-in-substance, agrees_with_t1: true, items: ["13.5"], evidence: ["docs/designs/orchestrator-mode.md:933"], tag: Grounded, note: "Delivered as a routing row item relying on SPEC section 9."}
  - {id: step-1.24a, verdict: covered, agrees_with_t1: true, items: ["12.4"], evidence: ["docs/designs/orchestrator-mode.md:934"], tag: Grounded, note: "Exact match at 12.4."}
  - {id: step-1.24b, verdict: covered, agrees_with_t1: true, items: ["13.6"], evidence: ["docs/designs/orchestrator-mode.md:935"], tag: Grounded, note: "Exact match at 13.6."}
  - {id: step-1.25, verdict: covered-in-substance, agrees_with_t1: true, items: ["14.1"], evidence: ["docs/designs/orchestrator-mode.md:936"], tag: Grounded, note: "Repo gate command at 14.1 after all build phases."}
  - {id: step-1.26, verdict: covered-in-substance, agrees_with_t1: true, items: ["14.2"], evidence: ["docs/designs/orchestrator-mode.md:937"], tag: Grounded, note: "Repo gate command at 14.2."}
  - {id: step-1.27, verdict: covered-in-substance, agrees_with_t1: true, items: ["14.3", "14.4"], evidence: ["docs/designs/orchestrator-mode.md:938"], tag: Grounded, note: "Repo gate commands at 14.3 and 14.4; the 14.3 parity test is the safety net for the byte copy."}
  - {id: step-1.28, verdict: covered, agrees_with_t1: true, items: ["14.5"], evidence: ["docs/designs/orchestrator-mode.md:939"], tag: Grounded, note: "Covered with the scoped-zero reading; the fixed full-tree count is a weak check, see R1-G9."}
  - {id: step-1.29, verdict: covered, agrees_with_t1: true, items: ["14.6", "14.7", "14.8"], evidence: ["docs/designs/orchestrator-mode.md:940"], tag: Grounded, note: "Owner and person gates are present; Branch 2 of 14.7 is the weak point in R1-G2."}
best_practice_compliance:
  grade: 4
  scale: 0-5
  reasons:
    - "+ Every one of the 76 slice rows has a delivering item in phases 7 to 14, and the gate order matches SPEC 15.2 except for additions the TASKLIST explains (D9 on step 1.3, OQ gates on 1.5, 1.6 and 11.3, the live check moved to 9.3, the base conftest moved to 8.8, R2 before R1)."
    - "+ The SPEC commit groupings (1.4a first code commit, 1.23 same commit as 1.21, R1 R2 R3 together) are kept as working-tree and ordering rules with stated reasons, since the TASKLIST never commits."
    - "+ The R5 decision flows through 6.1 to 6.4, 7.13, 7.16, 8.1, 8.10 and 10.1 to 10.3 as a recorded owner decision with a pre-flight check, and the record states which pins are not withdrawn."
    - "- Step 1.0a has two SPEC-allowed outcomes (a cursor template, a run-current --json need) with no route to the owner, and the allowlist count is fixed at ten before the capture runs."
    - "- The PENDING decision gates in Phase 7 and 14.7 point to a procedure in 6.2 that has no HALT, and their Branch 2 does not require the person's or owner's own words with a source."
    - "- Several check lines (7.16, 7.18, 14.5) cannot be judged cleanly from the Action text."
self_reported_confidence: 0.72
confidence_rationale: >-
  The gate and R5 flow findings rest on SPEC text and TASKLIST lines I read, but the item bodies for 7.16, 7.18 and 14.5 were judged from the brief hunks and some wording is re-stated from memory, so those three findings are tagged INFERRED.
summary:
  rows_audited: 76
  rows_disagreeing_with_t1: 1
  findings_high: 0
  findings_medium: 3
  findings_low: 6
```

## Blind calibration
```yaml
# Written by the orchestrator verbatim from the confidence-calibrator's returned YAML (read-only agent).
card_ref: "/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/reviewer-cards/reviewer-1-card.yaml"
dimensions:
  citation_grounding:
    score: 0.50
    reason: "All 14 finding-level citations matched their quotes exactly (tasklist 163, 1142, 1244, 1249, 1265, 1272, 1418, 1485, 2467; design 548, 552, 868, 875, 971). The other evidence is weak. Four findings (R1-G5, R1-G6, R1-G7, R1-G9) have empty evidence lists, and one of them (R1-G7) is refuted on reading. Every FR and NFR row cites a second design line in the 444 to 484 range, and none of those 41 lines matches its row. The range holds the closing fence of the 7.1 code block, the exit-mapping paragraph and the 7.2 data-model and rule tables, so these look like SPEC line numbers given the design file path. Two row refs read Section 8 gate, which is not a line."
  coverage_completeness:
    score: 0.90
    reason: "The card lists 76 rows: FR-001 to FR-026, NFR-001 to NFR-015 and the 35 design steps from 1.0a to 1.29, including 1.4a, 1.16a, 1.24a and 1.24b. That matches its rows_audited count. Each row names delivering items, and the primary design row refs I checked (755 to 760, 792 to 795, 906 to 913, 936 to 940) match. There is no explicit coverage_pct field, and I did not check the row-to-item mappings item by item."
  deviation_classification_clarity:
    score: 0.60
    reason: "Each finding has exactly one gap_class (gate-bypass, unsound-check or traceability) and one t1_relation, and each row has one verdict (covered, covered-in-substance or partial). None of them uses the rubric's Aligned, Refinement, Drift and Regression categories. Some classes are also arguable. R1-G3 calls something a plan-side gap when the tasklist does what the SPEC requires. R1-G9 calls a replace-every-hit rule a dropped justification, when it is closer to a Refinement."
  risk_surface_coverage:
    score: 0.70
    reason: "The card raises real gate risks. R1-G1 is a fixed allowlist count that breaks if the capture shows a cursor template or a run-current --json need, and it traces the effect to 8.10, 10.3, FR-002, FR-026 and NFR-003. R1-G2 is a Branch 2 that is weaker than the preamble and can let an executor mark a PENDING record RESOLVED on its own. R1-G5 and R1-G6 are checks that cannot pass as the items are written. One MEDIUM finding (R1-G3) is weakened and one LOW finding (R1-G7) is refuted, so part of the risk register is inflated. Apart from R1-G1, there is little reasoning about how far a failure would spread."
  recommendation_actionability:
    score: 0.85
    reason: "Every remediation names the item to edit (7.15, 7.16, 7.17, 7.18, 8.10, 10.3, 14.5, 14.7, line 163) and ends with a Check by reading success test. Two weak spots: R1-G7's fix targets a gap that does not exist, and the second sentence of R1-G6 (about the agent-wait forms) does not lead to a clear action."
calibrated_confidence: 0.71
self_reported_confidence: 0.72
calibration_delta: "-0.01"
citations_checked: 78
citations_failed: 41
citations_unverifiable_notes:
  - "41 row_coverage second refs in the range docs/designs/orchestrator-mode.md:444 to :484 do not match their rows. Examples: 444 is a code fence, 446 and 448 are blank, 447 is the 7.2 heading, 483 is rule-table row 9. They are probably SPEC merged-requirements.md line numbers under the wrong file path. I did not read the SPEC to confirm."
  - "docs/designs/orchestrator-mode.md:Section 8 gate (rows step-1.0b and step-1.17) is not a line reference and cannot be spot-checked."
  - "I did not read item 10.3, so the claim in R1-G1 that 10.3 pins exactly ten templates is unverified. The same claim for 8.10 is confirmed at tasklist line 1485."
  - "The t1_relation values (F1, F3, F5, F12, F13) cannot be checked without the Tier-1 card, which was not part of this calibration's input."
  - "I did not read item 8.12, so the part of R1-G7 about 8.12 not re-reading the decision file stays unverified."
  - "The card's model_class field says claude-gw-tier1b while model_slot says sonnet. Sonnet is used as the reviewer class here."
per_finding_check:
  - id: "R1-G1"
    verdict: "confirmed"
    note: "The only branch in 7.17 at line 1267 stops on a live field name that differs from the design. A recorded cursor field or a run-current --json need has no route to the owner. The 8.10 check at line 1485 requires the ALLOWED_ORCA count to be 10. Design line 552 (the cursor template is added after 1.0a) and line 971 (a --json need goes to the owner) match the quotes."
  - id: "R1-G2"
    verdict: "confirmed"
    note: "Item 6.2 at line 989 is Log the OQ-1 decision (L3, no HALT), so the preamble pointer at line 1142 is wrong. Branch 2 of 7.15 at line 1244 has no condition, and Branch 2 of 14.7 at line 2483 drops the clause requiring a source that quotes the owner. Two things lower the impact: the preamble at line 1142 writes out both branches itself, and the 7.15 verification at line 1246 requires the giver and the source to be filled in."
  - id: "R1-G3"
    verdict: "weakened"
    note: "Item 7.16 at line 1262 halts for owner review on a before-and-after difference, which is what design line 875 requires (a difference stops the build and goes to the owner), so this part is not a plan gap. The missing rule for removing timestamps is a real gap, since line 1260 only says compare with timestamps removed. The [INFERRED] point that live state fields cause false halts is still unproven."
  - id: "R1-G4"
    verdict: "confirmed"
    note: "The [INFERRED] part is confirmed by reading. Item 7.16 at lines 1249 to 1263 never says who runs the capture, while design line 868 says it is run by the person or the coordinator. The hand-off precedent exists in 14.8 Branch (B) at line 2490. The impact is low because no test runs the capture, so the never-by-a-test part of the rule is already met."
  - id: "R1-G5"
    verdict: "confirmed"
    note: "Both [INFERRED] parts are confirmed. The 7.18 grep at line 1276 searches for the bare word coder with no word boundaries, so it also matches words like encoder and decoder. The 7.16 verification at line 1262 expects the forbidden-token grep to find only the forbidden-list sentence, but the Action at line 1260 never tells the executor to write that sentence into readonly-probe.md."
  - id: "R1-G6"
    verdict: "confirmed"
    note: "The main [INFERRED] claim is confirmed. Line 1262 requires every command in the file to be one of the eight templates or a file read, but Action step 6 at line 1260 runs echo and ls -la. The second sentence, about worktree ps and the agent-wait forms, is not supported: line 1259 says --agent-wait is not run in step 1.0a."
  - id: "R1-G7"
    verdict: "refuted"
    note: "Item 9.3 reads the OQ-8 record directly (line 1640), and its HALT asks the person to name another Run if the Run cannot be read (line 1643), so the claim that 9.3 has no way to re-resolve is false. Item 8.4 re-checks OQ-7 at line 1441, and 14.8 depends on the 14.7 gate (lines 2483 and 2489), not on the 8.1 pre-flight. Item 9.1 lists the OQ-2 and OQ-5 records as gates at line 1626. The 8.1 grep for status RESOLVED at line 1420 is confirmed but harmless."
  - id: "R1-G8"
    verdict: "weakened"
    note: "The quote at line 163 is exact, and design line 548 says Phase 1 code does not call worktree list or worktree current. But the step 1.0a capture, which belongs to Phase 1, does call templates 7 and 8 (lines 1257, 1258 and step 3 of 1260). Eight called in Phase 1 is therefore true of the capture and only false of the code. This is ambiguous wording, not a misstatement."
  - id: "R1-G9"
    verdict: "weakened"
    note: "The [INFERRED] text is confirmed: line 2468 records 168 hits at 5dc29d23 and line 2472 requires an unchanged full-tree count. The claim that it fails after any unrelated change on the base is overstated, because line 2471 recounts at the recorded base when the base differs. Line 2471 also requires every hit to be replaced with the installed path, which is stricter than justifying it, so the claim that it drops the justification step is better seen as a Refinement than a gap."
calibrator_model_class: "opus"
reviewer_model_class: "sonnet"
```
