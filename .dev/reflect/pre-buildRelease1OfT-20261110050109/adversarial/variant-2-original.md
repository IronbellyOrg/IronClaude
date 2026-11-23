# Reviewer 2 card (persona: qa, model class: opus). Persisted by the orchestrator from the agent's returned text; claims condensed, citations kept verbatim.
reviewer: 2
persona: qa
model_class: opus
calibrated_confidence_self_report: 0.8
findings:
  - id: QA-01
    severity: blocking
    task: "Tasks 3, 5, 6"
    claim: "No contract test uses the missing, stale or contradictory fixtures. Task 3 only checks that its four fixtures are redacted, and Tasks 5 and 6 test against the success file and synthetic fakes. SPEC section 7 says the R1 gate stays closed without all four kinds pinned in a contract test."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:215"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:222"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:63-65"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:86"
    suggested_fix: "Add Task 6 or Task 7 acceptance criteria that run each of the four fixture files through a fake runner and assert: success parses; missing gives scope unknown, reported unknown and per-field UNKNOWN; stale gives old evidence age with the source still OK; contradictory gives duplicates ignored, time-went-back and changed during read."
  - id: QA-02
    severity: blocking
    task: "Task 8"
    claim: "T33 (empty states) is not excluded by the plan but no task builds or pins it: 'no observed items in this source window; not proof none exist' and 'worker-list returned 0 workers in scope=bound'."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:172"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:385"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:75"
    suggested_fix: "Add both strings to the Task 8 view model and a T33 criterion for the empty variant and for a bound scope with zero rows."
  - id: QA-03
    severity: blocking
    task: "Task 6"
    claim: "The instruction lists 'PARTIAL (empty page k)', 'reported T1-T2 (changed during read)' and 'collected n / reported T (mismatch)' but the acceptance criteria pin only T4 and T18."
    evidence_file_line:
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:100-106"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:158"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:331"
    suggested_fix: "Add fake-runner criteria for the empty-page, total-changed and mismatch outcomes."
  - id: QA-04
    severity: blocking
    task: "Tasks 6, 7"
    claim: "No acceptance criterion covers the FAILED (shape) path of T32 (missing required field, or more than one JSON envelope) or that the last good snapshot is kept; Task 5 tests only ShapeError at parser level."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:378"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:325"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:118"
    suggested_fix: "Add a Task 6 criterion mapping a shape error or two envelopes to FAILED (shape), and a Task 7 criterion that a shape-failed cycle keeps the previous snapshot."
  - id: QA-05
    severity: blocking
    task: "Tasks 6, 7"
    claim: "T5 requires the cycle to end within the 15 s budget, but the plan only bounds each call (DEFAULT_TIMEOUT_S under 15), so five calls can run far longer and no criterion checks total cycle time."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:369"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:322"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:104"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:106"
    suggested_fix: "Give each call a timeout of min(DEFAULT_TIMEOUT_S, time left in the 15 s budget) and add a fake-clock test where every call is close to the timeout and the cycle stops within 15 s with 'cycle overran'."
  - id: QA-06
    severity: minor
    task: "Tasks 6, 8"
    claim: "The PARTIAL disclosure text '(newest first; oldest rows not read; long-running active workers may be among them)' and 'reported T (page k)' appear in no instruction or criterion."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:158"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:349"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:103"
    suggested_fix: "Add the full text and page form to the Task 8 COUNTS tokens and assert them at view level."
  - id: QA-07
    severity: minor
    task: "Tasks 8, 9"
    claim: "T31 (cost renders 'cost unavailable', never '$0') is not excluded but no acceptance criterion pins it."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:377"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:129-136"
    suggested_fix: "Add a Task 8 criterion: the COUNTS tokens contain 'cost unavailable' and no variant output contains '$0'."
  - id: QA-08
    severity: minor
    task: "Task 8"
    claim: "Several Task 8 behaviours have no criterion: 'not reobserved' for a dropped row (second half of T41), the 'selected <id> no longer in source window' placeholder, the 'filter <expr>: k of n collected' text, 'scope unknown' and 'one Run only', and the NOT AVAILABLE and NOT POLLED strip cells."
    evidence_file_line:
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:135"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:393"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:55"
    suggested_fix: "Add Task 8 criteria for each of these texts."
  - id: QA-09
    severity: minor
    task: "Tasks 11, 9"
    claim: "The spec says help and the inspector state that caps are per observer process. Task 11 puts it in --help only, and its criterion only checks option names."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:352"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:177"
    suggested_fix: "Assert the three help statements and add a per-process caps line to the Task 9 inspector."
  - id: QA-10
    severity: minor
    task: "Task 8"
    claim: "SPEC section 9 says the header also shows 'read k of N Runs since start' and T45 pins it with the start-up-only view choice; Task 8 omits it and no task pins T45 or lists it as excluded."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:355"
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:397"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
    suggested_fix: "Add T45 to the plan's stated exclusions with the reason, or add the header token and a never-switches test."
  - id: QA-11
    severity: minor
    task: "Tasks 7, 8, 9"
    claim: "SPEC section 4 requires that when the source is STALE every value keeps its last-known reading with an 'as of HH:MM:SS' qualifier; no task builds this and no criterion renders a STALE or FAILED snapshot through the view."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:154"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:116"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:129-136"
    suggested_fix: "Add a Task 8 criterion: a STALE snapshot renders the 'STALE <age>' cell and 'as of HH:MM:SS' on last-known values; a FAILED snapshot renders 'FAILED (exit 2) 1m'."
  - id: QA-12
    severity: minor
    task: "Task 1"
    claim: "Task 1 departs from the spec's switch rule ('if the spike fails, switch to Textual') by stopping as blocked, without recording it as a deviation, and its spike criterion cannot fail because an artifact recording 'fail' satisfies it."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:298"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:33"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:39"
    suggested_fix: "Record the override as a deliberate deviation in Constraints (owner-decisions item 5) and assert a minimum number of Live repaints and decoded keys in one pty run."
