# Reviewer 2 card (qa lens, haiku slot, reflect-reviewer agent). Persisted verbatim by the orchestrator on receipt.
reviewer: 2
lens: qa
model_slot: haiku
findings:
  - id: QA-1
    priority: P1
    claim: >-
      Task 4's planned assertion does not pin the ignored-output exclusion.
      Checking only WC-4, [] and absence of write verbs allows a clause
      that lists ignored coverage output to pass. [INFERRED] This leaves
      the main requirement of Follow-up 2 unprotected.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md:66-70"
      - ".dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/source.md:19-20"
      - "tests/skills/test_worker_contract.py:769-774"
      - "src/superclaude/commands/test.md:103"
    exact_change: >-
      Extend Task 4's test instruction to require an explicit ignored-path
      exclusion and report-location wording within the extracted artifacts
      clause, alongside WC-4 and []. Add a negative check showing that
      removing that exclusion while retaining WC-4 and [] fails.
    verifier: >-
      Run the planned worker-contract suite after implementation. The new
      clause check must also reject a synthetic clause saying
      "lists every other file written; see WC-4; [] when none" because it
      omits the exclusion and report-location rule.
  - id: QA-2
    priority: P2
    claim: >-
      Task 1 names the write-verb classification tests as verification for
      new WORKER-CONTRACT.md text, but those tests do not scan core files.
      Their roots contain only skills, commands and agents.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md:35"
      - "tests/skills/test_worker_contract.py:1054-1058"
      - "tests/skills/test_worker_contract.py:1095-1107"
      - "tests/skills/test_worker_contract.py:1119-1124"
    exact_change: >-
      Replace Task 1's claimed classification coverage with a targeted
      assertion that the newly added WC-4 artifacts-rule sentence has no
      WRITE_VERB_RE match. Keep the existing classification suite for the
      command and skill edits; do not expand its roots merely to validate
      this sentence.
    verifier: >-
      The targeted assertion must pass for the intended WC-4 sentence and
      fail when a synthetic copy of that sentence contains a git staging
      command. Run it through the planned worker-contract suite.
self_reported_confidence: 0.94
checked_and_found_clean:
  - "Task 5's final verification criterion retains all six pytest files, lint, formatting, sync and verify-sync required by source.md."
  - "The proposed WC-4 exclusion tokens, workflow and build WC-4 pointers, test artifacts clause, and init-lite 'exited 0' checks do not already pass on current text."
  - "Tasks 2 and 3 retain the existing 'left out' assertions and update the checks at test_worker_contract.py:799 and :808."
  - "Task 5 can change the status wording without changing the existing init-lite artifacts clauses."
  - "Task 2 identifies both changed workflow plugin copies and includes the existing byte-parity tests."
limitations:
  - "Static pre-execution audit only. No commands or tests were run."
# Wave 3C blind calibration (confidence-calibrator, opus slot), persisted on receipt.
blind_calibration:
  calibrated_confidence: 0.82
  dimensions: {citation_grounding: 0.95, coverage_completeness: 0.75, deviation_classification_clarity: 0.80, risk_surface_coverage: 0.75, recommendation_actionability: 0.85}
  per_finding:
    - {id: QA-1, verdict: confirmed, calibrated_priority: P1, note: "Plan :66 checks only WC-4, [] and no write verb for the test.md clause, unlike build and workflow ('left out' at test_worker_contract.py:799, :808); AC at plan :69 requires the exclusion. Softened: a WC-4 pointer carries the rule by reference."}
    - {id: QA-2, verdict: confirmed, calibrated_priority: P2, note: "AUDIT_ROOTS (test_worker_contract.py:1054-1058) never reads core/WORKER-CONTRACT.md; plan :35 criterion is vacuous; reword or drop is the smallest fix. P3 defensible."}
  missed: "Task 5 (plan :76) checks 'exited 0' anywhere in each init-lite file, not tied to the worker_status sentence."
  not_verified: "Card's claim that no other test pins the removed 'because WC-9 stages' / 'git refuses' wording."
