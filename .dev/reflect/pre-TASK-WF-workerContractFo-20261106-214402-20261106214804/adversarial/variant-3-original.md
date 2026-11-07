# Reviewer 3 card (refactorer lens, opus slot, reflect-reviewer agent). Persisted by the orchestrator on receipt.
reviewer: 3
lens: refactorer
model_slot: opus
findings:
  - id: R3-1
    priority: P2
    claim: >
      The brief asks to keep "a plugin or spec copy" of WC-4 text consistent. Task 1 searches only tests/ and
      plugins/. The design spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72 holds a full
      WC-4 restatement with "`artifacts` (every other file written)", which the plan never names. Separate from
      RF-1 (docs/ developer guide). No plugin copy of WORKER-CONTRACT.md exists.
    evidence:
      - source.md:14
      - TASK-WF-workerContractFo-20261106-214402.md:30
      - .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72
    exact_change: >
      Task 1: grep tests/, plugins/, docs/ and .dev/orca-command-refactor/specs/orca-worker-contract-spec.md; then
      add the one-sentence rule to the spec's WC-4 row, or record that the spec is the approved design record and
      stays unchanged.
    verifier: "grep -n 'git ignores' .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (a hit, or a recorded reason in the plan)"
  - id: R3-2
    priority: P3
    claim: >
      Task 1 AC3 says the write-verb classification tests guard new WORKER-CONTRACT.md text, but the scan covers
      only skills, commands and agents; WC-9 already holds an unclassified literal `git add`. The criterion passes
      for any sentence.
    evidence:
      - tests/skills/test_worker_contract.py:1054-1058
      - src/superclaude/core/WORKER-CONTRACT.md:41-42
      - TASK-WF-workerContractFo-20261106-214402.md:35
    exact_change: >
      Replace Task 1 AC3 with "the new WC-4 sentence does not contain the literal `git add` (grep of the WC-4
      lines); WORKER-CONTRACT.md is outside the write-verb scan roots", or drop it.
    verifier: Read tests/skills/test_worker_contract.py:1054-1058 and confirm core/ is absent from AUDIT_ROOTS
  - id: R3-3
    priority: P3
    claim: >
      The planned WC-4 assertion does not say how the WC-4 text is cut out; _contract() returns the whole file and
      _check_rule matches anywhere, so a sentence placed in WC-9 would still pass.
    evidence:
      - TASK-WF-workerContractFo-20261106-214402.md:30
      - tests/skills/test_worker_contract.py:383-394
      - source.md:14
    exact_change: >
      Task 1: assert on the WC-4 span only (from the line starting "- **WC-4." up to the line starting
      "- **WC-8.") containing "git ignores" and "outside the repository".
    verifier: Move the sentence into WC-9 in a scratch copy (monkeypatch CONTRACT_PATH as in test_worker_contract.py:581-583); the assertion must fail
  - id: R3-4
    priority: P3
    claim: >
      Tasks 3 and 4 remove only the restated reason but keep other parts of the WC-4 rule: build keeps "except
      paths outside the repository and paths git ignores" and "the build report names where they were written";
      the new test.md clause adds "which the test report names instead". Those parts stay written twice.
    evidence:
      - src/superclaude/commands/build.md:104
      - TASK-WF-workerContractFo-20261106-214402.md:54
      - TASK-WF-workerContractFo-20261106-214402.md:66
      - source.md:13
    exact_change: >
      Task 3: keep only build-specific parts (files the build tool reports, git check-ignore, typical ignored
      paths, "left out per WC-4"). Task 4: "left out per WC-4", drop "which the test report names instead". Or
      record that the repetition is deliberate.
    verifier: "grep -n 'outside the repository\\|names where' src/superclaude/commands/build.md src/superclaude/commands/test.md returns no hit in the Unattended sections"
  - id: R3-5
    priority: P3
    claim: >
      return-contract.md (installed skill ref) never mentions WORKER-CONTRACT.md, so a bare "WC-4" pointer in its
      YAML comment cannot be followed; no criterion forbids a src/superclaude/ path in the pointer text.
    evidence:
      - src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:43-54
      - TASK-WF-workerContractFo-20261106-214402.md:43
    exact_change: >
      Task 2: write the pointer in return-contract.md as "left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)"; the
      command files may use bare "WC-4". Add to Tasks 2-4 acceptance criteria: no `src/superclaude/` path in new text.
    verifier: grep -n 'WORKER-CONTRACT' src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md finds a hit; grep -n 'src/superclaude' on changed lines finds none
correctness_gaps_advisory_non_gating:
  - id: R3-A1
    claim: "The new WC-4 'report names where those files were written' duty applies to all converted commands; workflow's report (the plan <id>.md) never names .dev/reflect/runs.jsonl or .superclaude/memory/."
    evidence: [src/superclaude/commands/workflow.md:72, source.md:13]
  - id: R3-A2
    claim: "WC-9 also stages report_path; a report_path inside an ignored path is not covered by the new exclusion (out of brief scope)."
    evidence: [src/superclaude/core/WORKER-CONTRACT.md:41, src/superclaude/commands/build.md:104]
  - id: R3-A3
    claim: "init-lite artifacts lists scaffold files under .dev/superclaude/ with no WC-4 link; a project that ignores .dev/ would conflict with the new rule."
    evidence: [src/superclaude/commands/init-lite.md:92, src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61]
self_reported_confidence: 0.82
checked_clean:
  - "Grep for 'git refuses|stages every' outside .dev/ finds only workflow.md:72, return-contract.md:52, build.md:104 and the two byte-identical plugin copies (plus unrelated CONTRIBUTING.md:29)."
  - "A new sub-bullet after WORKER-CONTRACT.md:32 fits WC-4's structure; the pin at test_worker_contract.py:102-108 stays intact."
  - "Depends-on links are sound; /sc:implement runs tasks in source order, so test-file edits cannot collide."
  - "No scope creep beyond the brief."
  - "Ignored paths named by the plan are really ignored (.gitignore:7,9,21,37,40,44,48,114)."
  - "No plugin copy of WORKER-CONTRACT.md; install_core.py:26 lists only the file name."
  - "_artifacts_clause (test_worker_contract.py:769-774) will find a new backticked `artifacts` on the test Contract line."
not_checked: "Task 5 init-lite wording against tests/cli/test_init_lite.py."
# Wave 3C blind calibration (confidence-calibrator, opus slot), persisted on receipt.
blind_calibration:
  calibrated_confidence: 0.82
  dimensions: {citation_grounding: 0.92, coverage_completeness: 0.75, deviation_classification_clarity: 0.78, risk_surface_coverage: 0.75, recommendation_actionability: 0.90}
  per_finding:
    - {id: R3-1, verdict: confirmed, calibrated_priority: P2, note: "source.md:14 asks for spec copies; plan :30 greps only tests/ and plugins/; orca-worker-contract-spec.md:72 restates WC-4."}
    - {id: R3-2, verdict: confirmed, calibrated_priority: P3, note: "AUDIT_ROOTS (:1054-1058) excludes core/; plan :35 criterion passes for any text."}
    - {id: R3-3, verdict: confirmed, calibrated_priority: P2, note: "_contract() (:383-384) returns whole file; plan :30 does not say how the WC-4 span is cut; a misplaced sentence would pass."}
    - {id: R3-4, verdict: confirmed, calibrated_priority: P3, note: "Duplicated text at build.md:104 and plan :66, not a defect."}
    - {id: R3-5, verdict: confirmed, calibrated_priority: P3, note: "return-contract.md never names WORKER-CONTRACT.md; src/ path leak is a possible risk only."}
    - {id: R3-A1, verdict: confirmed, calibrated_priority: P2, note: "WC-4 'report names where' duty not met by workflow's plan <id>.md (workflow.md:72)."}
    - {id: R3-A2, verdict: partly, calibrated_priority: P3, note: "Speculative and outside the brief."}
    - {id: R3-A3, verdict: confirmed, calibrated_priority: P3, note: "Matters only in a project that ignores .dev/."}
  missed: "test_worker_contract.py:792 rejects 'failed tool run' inside the init-lite artifacts clause, which includes the status sentence on init-lite.md:92; plan :76 names only 'on a failed run'. Pin at :795-796 ('as each file is written' / 'as it is written') is not repeated in the plan."
