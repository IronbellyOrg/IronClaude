reviewer: 1
persona: analyzer
model_class: sonnet
agent_type: reflect-reviewer
plan: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md
spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md
findings:
  - id: F1
    severity: blocking
    category: ordering
    claim: "Task 3's begin must exit 5 on prior-verdict mismatch and seal's prior link needs 'confirmed and open in review N-1', but final-status derivation lands in Task 4 and compute_verdict in Task 5."
    evidence: [plan:57, plan:60, plan:68, plan:77, source.md:62, source.md:64]
    recommendation: "Move status/verdict computation into Task 3 (Tasks 4-5 extend it), or move the prior-verdict-mismatch part of begin and its test to Task 5."
  - id: F2
    severity: blocking
    category: ordering
    claim: "Task 5's finalize label-count line uses 'the same function as Task 6's count', but Task 6 depends on Task 5 (confirms T1 A1)."
    evidence: [plan:77, plan:80, plan:83, plan:87]
    recommendation: "Define the label-count function (including form-only dropped claims) in Task 5 or Task 3; Task 6 only wraps it as the count subcommand."
  - id: F3
    severity: blocking
    category: acceptance
    claim: "Task 7 replay cannot run as written: at review 3 begin needs a prior review-2 report with a valid sentinel, spec= hash and matching verdict; the control r1 round-2 report has none, the plan names no prior-report fixture and forbids synthetic substitutes; uncovered-hunk handling in replay unspecified."
    evidence: [plan:96, plan:57, source.md:62, source.md:64, source.md:93]
    recommendation: "Have the test build a prior review-2 report with a sentinel in tmp_path as declared scaffolding; say whether replay adds checked lines or asserts only ratchet statuses."
  - id: F4
    severity: minor
    category: deviation
    claim: "spec-panel.md Usage line 23 advertises --unattended; Task 9 keeps it, so the variant advertises a flag it refuses; Task 10 replaced-block list and Task 9 acceptance do not cover it."
    evidence: [src/superclaude/commands/spec-panel.md:23, src/superclaude/commands/spec-panel.md:451-462, plan:21, plan:123, plan:135, source.md:256]
    recommendation: "Drop the --unattended Usage line (or token) in Task 9, add it to Task 10's replaced blocks, add grep -c -- '--unattended' = 0 to Task 9 acceptance."
  - id: F5
    severity: minor
    category: coverage
    claim: "Spec test 'two claims on one prior counted once' is in no task acceptance list and the rule is stated nowhere in Tasks 3-5."
    evidence: [source.md:128, plan:60, plan:71, plan:80]
    recommendation: "Add the case and the rule to Task 3 or Task 5."
  - id: F6
    severity: minor
    category: coverage
    claim: "Task 12 stages before Tasks 13-14 create INSTALL.md and briefs; nothing stages them and Task 13's git diff --cached check only sees Task 12's staging."
    evidence: [plan:27, plan:161, plan:172, plan:182]
    recommendation: "Stage .dev/brainstorms/346-stoprule/ and .dev/tasks at the end of Tasks 13 and 14."
  - id: F7
    severity: minor
    category: ordering
    claim: "Task 13 must list Task 14's templates and Task 14's acceptance requires INSTALL.md to list eleven files, but Task 14 has no instruction to edit INSTALL.md."
    evidence: [plan:172, plan:180, plan:190]
    recommendation: "Check the list in Task 13's acceptance, or have Task 14 update INSTALL.md."
  - id: F8
    severity: minor
    category: coverage
    claim: "Writers of final/verdict ledger lines, the source of sentinel brief=/grader_model=/ratchet=, and parent= (escalation g) are unspecified."
    evidence: [source.md:34, source.md:69-70, source.md:73, plan:77]
    recommendation: "Name the writer subcommands and the source of brief= in Task 5; define parent= or drop it."
  - id: F9
    severity: minor
    category: coverage
    claim: "apply-audit defines real:true only for claims; a real:true on a seeded unclaimed hunk has no defined outcome."
    evidence: [plan:68, source.md:68]
    recommendation: "Define the outcome (e.g. FAIL) with a test in Task 4."
  - id: F10
    severity: minor
    category: risk
    claim: "Task 7's hand-transcribed quotes decide anchored vs late-found; the quote-selection rule is unstated."
    evidence: [plan:96, source.md:93, source.md:193]
    recommendation: "Quote the line the report cites and record the choice per claim."
  - id: F11
    severity: minor
    category: acceptance
    claim: "The stdlib import grep is only in Task 3; Tasks 4-6 extend the script unchecked. test_worker_contract.py scans new primitives for git/gh write verbs."
    evidence: [plan:26, plan:61, plan:20, tests/skills/test_worker_contract.py:1940-1951]
    recommendation: "Repeat the import grep in Task 6; forbid git/gh write-verb text in new files in Tasks 3 and 8."
  - id: F12
    severity: minor
    category: coverage
    claim: "Measurement copy not produced by any task (not a plan defect: section 3 omits it); INSTALL.md's 'differ only in lines from master' is unverified. Control r1 files exist in the sibling checkout."
    evidence: [source.md:163, plan:172, plan:96]
    recommendation: "Task 13 records the repo copy's line count and diff against the 472-line base instead of asserting; name exact source paths in Task 7."
confirmed: [A2 necessary deviation, A3 authorized deviation, A4 reporting-only (design doc should reword source.md:36), Q2 lexical misses covered, Q5 every task has acceptance criteria]
deviation_counts: {authorized: 1, necessary: 1, drift: 0, regression: 0}
calibration:
  calibrator_model_class: opus
  calibrator_diversity: degraded
  dimensions: {citation_grounding: 0.88, coverage_completeness: 0.75, deviation_classification_clarity: 0.65, risk_surface_coverage: 0.70, recommendation_actionability: 0.85}
  C: 0.77
  per_finding:
    - {id: F1, finding_confidence: 0.60, reason: "Real ordering defect; workable by an implementer reading ahead, blocking is a stretch."}
    - {id: F2, finding_confidence: 0.50, reason: "Real forward reference to Task 6's count; fixable inside Task 5."}
    - {id: F3, finding_confidence: 0.55, reason: "Real gap (begin needs a sentinel prior); plan:96 bans substitutes only for missing files, not test scaffolding."}
    - {id: F4, finding_confidence: 0.80, reason: "Verified spec-panel.md:23 advertises --unattended; Task 9 keeps it."}
    - {id: F5, finding_confidence: 0.85, reason: "Verified source.md:128 case absent from Tasks 3-5 acceptance."}
    - {id: F6, finding_confidence: 0.65, reason: "Nothing stages files created after Task 12."}
    - {id: F7, finding_confidence: 0.35, reason: "Mostly ordering awkwardness; names fixed in advance."}
    - {id: F8, finding_confidence: 0.60, reason: "Inherited underspecification of final/verdict writers and grader_model= source."}
    - {id: F9, finding_confidence: 0.65, reason: "Real gap inherited from source.md:68."}
    - {id: F10, finding_confidence: 0.55, reason: "Quote-line selection rule unstated."}
    - {id: F11, finding_confidence: 0.45, reason: "Import grep gap minor; write-verb risk caught by Task 10 running test_worker_contract.py."}
    - {id: F12, finding_confidence: 0.35, reason: "Card says not a plan defect; only the unverified INSTALL sentence remains."}
  notes:
    - "F1-F3 fit major better than blocking under the wrong-or-missing-deliverable test."
    - "source.md:128 'PASS-time audit reinstatement -> FAIL' is tested at plan:71 only as a status, not a FAIL verdict."
    - "Usage line 23 also keeps --report-dir, which applies only in unattended mode."
