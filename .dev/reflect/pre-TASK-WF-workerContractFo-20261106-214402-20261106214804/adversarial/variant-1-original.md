# Reviewer 1 card (analyzer lens, sonnet slot, reflect-reviewer agent). Persisted by the orchestrator on receipt.
reviewer: 1
lens: analyzer
model_slot: sonnet
findings:
  - id: R1-1
    priority: P2
    claim: >
      Task 5's "exited 0" assertion can pass with the old contradicting sentence still in place ("The run is
      succeeded when the audit finished, and failed otherwise" at init-lite.md:92; "`succeeded` when the audit
      finished, else `failed`" at SKILL.md:61). No existing pin catches this (test_worker_contract.py:787-797).
    evidence:
      - tests/skills/test_worker_contract.py:777-797
      - src/superclaude/commands/init-lite.md:92
      - src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61
      - TASK-WF-workerContractFo-20261106-214402.md:76
    exact_change: >
      Task 5: assert "exited 0" present and "when the audit finished" absent in each text; optionally assert
      "exited 0" inside the init-lite.md _artifacts_clause, since the status sentence follows the artifacts key on
      that line.
    verifier: Revert only the old-wording removal and run `uv run pytest tests/skills/test_worker_contract.py -q`; the "not in" assertion must fail.
  - id: R1-2
    priority: P2
    claim: >
      The WC-4 sentence "the report names where those files were written" applies to every command, but workflow's
      report_path is the plan <id>.md, which does not name .dev/reflect/runs.jsonl or .superclaude/memory/. After
      Task 2 replaces workflow's reason with a WC-4 pointer, the shared rule demands something workflow does not do.
    evidence:
      - src/superclaude/commands/workflow.md:72
      - src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52
      - src/superclaude/commands/build.md:104
      - source.md:13
      - TASK-WF-workerContractFo-20261106-214402.md:30
    exact_change: >
      Reword Task 1's sentence to "...; where the command's report can say so, it names where those files were
      written", or have Task 2 keep a workflow-specific note that the ignored files live at the fixed reflect paths
      it lists. Record the choice as an owner note, since source.md:13 asks for the unconditional wording.
    verifier: Read WC-4 and workflow.md:72 after the edit; no command's pointer contradicts the WC-4 wording.
  - id: R1-3
    priority: P3
    claim: >
      Task 1 AC3 checks nothing: the write-verb scan walks only skills, commands and agents; core/WORKER-CONTRACT.md
      already holds unclassified `git add` at :41-42. The test that does read every contract line is
      _check_repo_setup_gated (test_worker_contract.py:445-461, regex :430-435), which would fail on a new
      backticked program or script span without a user-instruction gate.
    evidence:
      - tests/skills/test_worker_contract.py:1054-1058
      - tests/skills/test_worker_contract.py:445-461
      - src/superclaude/core/WORKER-CONTRACT.md:41-42
      - TASK-WF-workerContractFo-20261106-214402.md:35
    exact_change: >
      Replace Task 1 AC3 with: "test_every_repo_setup_line_is_gated and the RULE_PHRASES['WC-4'] pins still pass;
      the new sentence adds no backticked span that names a program or script file."
    verifier: uv run pytest tests/skills/test_worker_contract.py -q -k "repo_setup or WC-4"
  - id: R1-4
    priority: P3
    claim: >
      Task 1's assertion "the WC-4 text read from CONTRACT_PATH" is ambiguous; against _contract() (whole file) it
      would still pass if the sentence moved to another rule.
    evidence:
      - tests/skills/test_worker_contract.py:383-384
      - src/superclaude/core/WORKER-CONTRACT.md:31-37
    exact_change: Slice text.split("- **WC-4.", 1)[1].split("\n- **WC-8.", 1)[0] and assert both phrases on that slice.
    verifier: Move the sentence into WC-9 in a scratch copy via _patched_copy; the assertion must fail.
  - id: R1-5
    priority: P3
    claim: >
      "exited 0" agrees with superclaude init-lite: --dry-run returns before the scaffold (init_lite.py:348-352,
      exit 0); a partial scaffold failure raises an uncaught FileExistsError (init_lite.py:221-240, 267-282),
      exit non-zero (test_init_lite.py:257-258); an audit failure raises ClickException (init_lite.py:247-262).
      Gaps: SKILL.md:63 allows an in-skill fallback with no exit code; the plan does not say report_path still
      names a report written before a scaffold failure.
    evidence:
      - src/superclaude/cli/init_lite.py:221-240
      - src/superclaude/cli/init_lite.py:247-262
      - src/superclaude/cli/init_lite.py:267-282
      - src/superclaude/cli/init_lite.py:348-359
      - tests/cli/test_init_lite.py:238-261
      - src/superclaude/skills/sc-init-lite-protocol/SKILL.md:63
    exact_change: >
      Add to Task 5: "report_path still names the report when the failure came after it was written" and "when the
      audit is run without the tool, succeeded means every step finished".
    verifier: Read the two edited init-lite texts against init_lite.py:348-359 and test_init_lite.py:257-261.
  - id: R1-6
    priority: P3
    claim: >
      _artifacts_clause returns the rest of the first Unattended-section line containing `artifacts`
      (test_worker_contract.py:769-774); Task 4 must put WC-4 and [] after the `artifacts` token on the Contract
      bullet and mention `artifacts` in no earlier bullet. The plan does not say this.
    evidence:
      - tests/skills/test_worker_contract.py:769-774
      - src/superclaude/commands/test.md:97-107
    exact_change: Add to Task 4 the placement rule above.
    verifier: uv run pytest tests/skills/test_worker_contract.py -q, including the new test.md pin.
self_reported_confidence: 0.8
checked_and_found_clean:
  - "The WC-4 sentence cannot trip the write-verb test (core/ outside AUDIT_ROOTS; 'git ignores' and 'git check-ignore' do not match WRITE_VERB_RE at :1062-1065)."
  - "The WC-4 phrase pin (:107, contract line 32) and the identifier pin (line 31, :392-394) are unaffected by a new sentence or sub-bullet."
  - "_check_repo_setup_gated would not fire on the planned wording."
  - "No other test or mirror pins WORKER-CONTRACT text; no plugin copy."
  - "Workflow and return-contract 'names WC-4' assertions fail before the edit and pass only after it; runs.jsonl and 'left out' stay pinned."
  - "Build UNATTENDED_EXPECT pins (:339-343) unaffected."
  - "No edited line holds `git add` today; no WRITE_VERB_CLASSIFICATION key breaks."
  - "Section checks (:501-518) cannot be tripped by 'WC-4', 'htmlcov/', '.pytest_cache/' or 'exited 0'."
  - "Plugin parity: only workflow.md and return-contract.md are mirrored; plugin test.md has no Unattended section; no plugin init-lite or WORKER-CONTRACT copy."
  - "Task order is sequential under /sc:implement; no parallel-edit risk."
  - "RF-1 (developer guide :1002) is a summary with no pin; P3 is right."
# Wave 3C blind calibration (confidence-calibrator, opus slot), persisted on receipt.
blind_calibration:
  calibrated_confidence: 0.85
  dimensions: {citation_grounding: 0.95, coverage_completeness: 0.85, deviation_classification_clarity: 0.75, risk_surface_coverage: 0.80, recommendation_actionability: 0.90}
  per_finding:
    - {id: R1-1, verdict: confirmed, calibrated_priority: P1, note: "Plan :76 asks only for 'exited 0' present; old sentence at init-lite.md:92 and SKILL.md:61, nothing at test_worker_contract.py:787-797 rejects it; planned test passes on contradicting text (P1 by definition)."}
    - {id: R1-2, verdict: confirmed, calibrated_priority: P2, note: "workflow.md:72 report_path is the plan <id>.md; only build.md:104's report names where ignored files went; unconditional WC-4 wording (source.md:13, plan :30) is false for workflow. Owner note is right."}
    - {id: R1-3, verdict: confirmed, calibrated_priority: P3, note: "AUDIT_ROOTS (:1054-1058) excludes core/; WORKER-CONTRACT.md:41-42 already has git add; plan :35 AC is vacuous. test_every_repo_setup_line_is_gated name not verified."}
    - {id: R1-4, verdict: confirmed, calibrated_priority: P3, note: "_contract() (:383-384) returns whole file; WC-4 is :31-37, WC-8 starts :38; the proposed slice isolates WC-4."}
    - {id: R1-5, verdict: confirmed, calibrated_priority: P3, note: "dry-run returns at init_lite.py:348-352; report written :354 before scaffold :358-359; FileExistsError uncaught (test_init_lite.py:257-258); ClickException :247-262."}
    - {id: R1-6, verdict: confirmed, calibrated_priority: P3, note: "Misplacement would make the new pin fail, not pass wrongly; placement note."}
  not_verified: "_patched_copy helper name; whether 'paths outside the repository' applies to init-lite --project-root."
