# Reviewer 2 (persona qa, haiku slot, reflect-reviewer). Persisted verbatim by the orchestrator.
reviewer: 2
persona: qa
model_slot: haiku
findings:
  - id: R2-F1
    severity: P1
    claim: >-
      Task 13 omits cli-eval's required blocked outcome when the brief lacks
      safety flags. It blocks a missing --suite, but treats the command line
      as given as the confirmed invocation without checking the required
      safety inputs. This contradicts the section 3.2 cli-eval row.
    evidence:
      - ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:248"
    deviation_class: Drift
    suggested_fix: >-
      Specify how the required safety inputs are identified from the fresh
      digest, block before launch when they are missing, and add separate
      assertions for missing-suite and missing-safety-input resolutions.
  - id: R2-F2
    severity: P2
    claim: >-
      Task 20 says to derive gate-resolution assertions from the entries added
      by Tasks 2-16, but those entries frequently contain only labels, not
      resolutions. For example, cleanup pins "Approval Required" and "not
      applied" separately, while release-split pins "blocked_question" without
      tying it to either blocked gate. [INFERRED] Reversing a resolution while
      retaining these labels would satisfy the prescribed phrase checks.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:97"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:179"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:345"
    deviation_class: Drift
    suggested_fix: >-
      Give each gate a concrete expected phrase that joins its condition to
      its outcome. Require negative cases that reverse or remove the outcome
      while preserving the gate label, rather than only deleting labels.
  - id: R2-F3
    severity: P2
    claim: >-
      F1 remains incompletely verified. Only cleanup and improve explicitly
      add "left out (WC-4)" to their expected phrases; research, cli-eval and
      tdd describe exclusions but omit that phrase from their test entries.
      No task assigns the required short local sentence for reports that
      name where excluded files went. This confirms and sharpens T1-F1.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:7"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:97"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:110"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:123"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:248"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:261"
      - ".dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/artifacts/coverage-matrix.yaml:14"
    deviation_class: Drift
    suggested_fix: >-
      Add a clause-scoped F1 check for all fifteen P2 commands, covering
      run-written files, named exclusions, the WC-4 pointer and absence of
      the repeated reason. Assign the conditional report sentence explicitly
      and correct the matrix's test-coverage claim.
  - id: R2-F4
    severity: P2
    claim: >-
      Task 21 cannot deliver the complete commit-path list requested by the
      brief. Its acceptance criterion restricts the report's path list to
      src, tests and plugins, while the same task stages the package's report
      and evidence under .dev/tasks. Those staged deliverables are excluded
      from the asserted exact list.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:367"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:371"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:372"
    deviation_class: Drift
    suggested_fix: >-
      Include the task package and its artifacts in the commit manifest and
      its equality check. Distinguish pre-existing unrelated changes from
      paths produced by this plan.
  - id: R2-F5
    severity: P3
    claim: >-
      The coverage matrix omits two requirement-bearing spans from source
      line 14: placing tested text after the first backticked artifacts key,
      and requiring each check to fail on pre-change text. INF-017 and
      INF-018 cover only the preceding phrase-strength and old-wording
      requirements.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14"
      - ".dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/artifacts/coverage-matrix.yaml:25-36"
      - ".dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md:27"
    deviation_class: Drift
    suggested_fix: >-
      Add separate inferred rows for both spans and link them to concrete
      task-level checks, not only the general constraint.
self_confidence: 0.94
self_audit: >-
  Read all 21 plan tasks, all 28 coverage rows, the driving brief, the relevant
  specification sections and approved decisions. Inspected the existing
  worker-contract helpers, nesting tests, AC14 cases and write-verb
  classifications, and checked the explicitly named per-task test-file
  paths for existence. No commands, tests, live Orca operations or file
  modifications were performed.
