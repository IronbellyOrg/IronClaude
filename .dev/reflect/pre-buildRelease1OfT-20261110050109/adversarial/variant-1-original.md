# Reviewer 1 card (persona: analyzer, model class: haiku). Persisted by the orchestrator from the agent's returned text; claims condensed, citations kept verbatim.
reviewer: 1
persona: analyzer
model_class: haiku
calibrated_confidence_self_report: 0.94
findings:
  - id: R1-01
    severity: blocking
    task: "Tasks 6 and 7"
    claim: "The timeout criteria do not enforce the total 15-second cycle budget. Task 6 permits five sequential calls and only requires each timeout to be below 15 seconds."
    evidence_file_line: ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
    suggested_fix: "Pass a monotonic cycle deadline into poll, limit each call to the smaller of its timeout and the remaining budget, stop paging when the budget expires, and test several individually timely pages that together exhaust it."
  - id: R1-02
    severity: blocking
    task: "Task 6; Constraints; Task 11"
    claim: "Reusing _find_orca runs a live subprocess (skills list --json) outside the worker-list-only runner boundary, so T36 (subprocess.run patched to raise) and the fake runner cannot stop it."
    evidence_file_line:
      - "src/superclaude/cli/install_user_setup.py:209"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:23"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:105"
    suggested_fix: "Treat the binary discovery probe as a separate, approved startup call with its own budget, inject discovery independently of Runner, keep fixture mode outside discovery, and say whether the argv trace covers discovery."
  - id: R1-03
    severity: blocking
    task: "Tasks 10 and 11"
    claim: "Writing the JSON snapshot only after successful cycles means the file never reports a later ERROR or STALE state, although the frozen contract has source.status and source.error per cycle."
    evidence_file_line:
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173"
      - ".dev/issues/409/tuibbs-review/architecture-options.md:79"
      - ".dev/issues/409/tuibbs-review/architecture-options.md:88"
    suggested_fix: "Publish an atomic snapshot for failed cycles and STALE transitions too, keeping last-good rows and observedAt while updating source.status and source.error; test a good poll followed by a failure and the 45 s threshold."
  - id: R1-04
    severity: blocking
    task: "Constraints; Tasks 2, 9 and 10"
    claim: "The constraint that no absolute path, terminal handle or credential is 'printed' conflicts with showing and exporting sanitized free-text worker fields (stage.detail, stage.activity, stderr). The sanitizer removes terminal controls only, so printable sensitive values can pass through."
    evidence_file_line:
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:25"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:45"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:157"
    suggested_fix: "Narrow the constraint to what the executor commits and logs, or specify suppression or redaction of these fields before display and export; add tests with printable sensitive values."
  - id: R1-05
    severity: minor
    task: "Task 5"
    claim: "Task 5's acceptance criteria use the duplicate-out-of-order variant that Task 4 creates, but Task 5 depends only on Task 3."
    evidence_file_line:
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:71"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:80"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:88"
    suggested_fix: "Add Task 4 to Task 5's dependencies, or use the contradictory golden fixture for that test."
  - id: R1-06
    severity: minor
    task: "Tasks 8 and 9"
    claim: "The empty fixture is created but its required empty-state text is not assigned to a rendering task or acceptance criterion (T33)."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:172"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:75"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
    suggested_fix: "Assign T33 to the view and renderer tasks and assert the exact empty-state message and the named scope."
  - id: R1-07
    severity: minor
    task: "Tasks 6, 8 and 9"
    claim: "The partial-result criteria omit the unread-oldest-rows warning and the 'reported T (page k)' qualifier."
    evidence_file_line:
      - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:158"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:103"
      - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
    suggested_fix: "Carry the last-read page and the cap-stop reason into the view model and assert both in screen and export tests."
