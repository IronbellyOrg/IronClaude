reviewer: 1
persona: analyzer
model_class: sonnet
verdict: PASS
self_confidence: 0.7
findings:
  - id: R1-F1
    severity: should-fix
    deviation_class: drift
    tasks: [2, 5]
    claim: >
      Task 5 tells the executor to assert the fan-in cap "at most 10" and says this is "as written in section 2.3".
      The spec never writes "at most 10". Section 2.3 says "the merge command's maximum of 10 inputs" and "never
      exceeds 10", and the only matching phrase in the spec is "at least 2". Task 2's acceptance criteria repeat the
      paraphrase "at most 10 inputs". The executor can therefore write a contract and a test around wording that is
      not in the spec, while the test's own rule says each assertion uses a phrase quoted from source.md. A strict QA
      reviewer comparing the test with the spec could flag it. A contract written with the spec's own wording would
      fail the test the plan describes.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:112"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:56"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:122"
    recommendation: >
      In Tasks 2 and 5, replace "at most 10" with the spec's wording ("maximum of 10 inputs", "never exceeds 10") and
      keep "at least 2".
  - id: R1-F2
    severity: should-fix
    deviation_class: none
    tasks: [1, 3, 4, 8]
    claim: >
      Task 8 requires "a PASS or FAIL line with an evidence file" for each of 11 checks. Earlier tasks produce no
      saved evidence file for AC-0.1 (Tasks 1 and 3 run commands but name no artifact) or AC-0.2 and AC-0.3 (Task 4
      names only the t4-wider-compare artifact). Task 8 itself says only to re-run AC-C1, AC-C2, AC-C3, AC-C5 and
      AC-C6, and does not say where to save the AC-C1 and AC-C2 output. It does not tell the executor to re-run or
      save AC-0.1, AC-0.2 or AC-0.3. An executor that cites only chat output leaves Task 8's AC unmet (the evidence
      file is missing). The task's QA would then flag it as an unmet acceptance criterion, which is a blocking type
      and would halt the run. A resourceful executor will probably create the files, so I rate this should-fix.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:47"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:72"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:93"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:147"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:154"
    recommendation: >
      In Task 8, add: "re-run the AC-0.1 (three commands), AC-0.2, AC-0.3, AC-C1 and AC-C2 checks and save each
      output to ./artifacts/<id>.txt", and cite those files as the evidence for the report lines.
  - id: R1-F3
    severity: should-fix
    deviation_class: drift
    tasks: [6]
    claim: >
      Task 6 requires each allowlisted hit to carry "the phase that converts its command". Many hits have no such
      phase. The spec puts /sc:pr-submit and /sc:git on the never-as-worker list, and P4 converts pr-submit only if
      D3 (b) is chosen. The spec records D3 as option (a), so a "P4" label would be false. Several hits are in skills
      with no converted command at all (task-builder and sc-crash-recovery show up in the write-verb grep). The
      reason format has no slot for "never a worker" or "no converting command". The executor must either invent a
      phase or write a reason that breaks the task's own instruction. The test would still pass, so a QA reviewer is
      unlikely to block, but the allowlist would contain false statements about phases.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:125"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:61"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:174"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:201"
    recommendation: >
      Change the reason format to "WC-9 allowed | converting phase P<n> | never a worker (section 4 / D3) | no
      command converts it (state why)", so the classification table has a valid value for every hit.
  - id: R1-F4
    severity: should-fix
    deviation_class: none
    tasks: [1, 2]
    claim: >
      WORKER-CONTRACT.md is a core file that installs into other projects. Repo CLAUDE.md forbids installed
      primitives from pointing at src/superclaude/... paths, and requires installed paths such as
      ~/.claude/WORKER-CONTRACT.md. The plan says "restate" the spec but never says to drop the spec's internal
      evidence citations (CAPS:, INV-A:, src/superclaude/cli/install_core.py:36, and so on). A literal restatement of
      sections 2.1 to 2.3 would carry those citations and src/ paths into a shipped file. The plan's Constraints do
      not list the rule, and the FINAL review reads only the plan's Constraints, so nothing would catch it.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:37"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:22"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:59"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:72"
    recommendation: >
      Add a Constraints line: "WORKER-CONTRACT.md and the HOW-WE-WORK.md section use installed paths only
      (~/.claude/...). They do not copy the spec's CAPS:/INV- evidence ids or src/superclaude/ paths."
  - id: R1-F5
    severity: minor
    deviation_class: none
    tasks: [3]
    claim: >
      Task 3 points the executor at scripts/build_superclaude_plugin.py as the deciding file. A grep of that script
      for "core" finds nothing, but the script does decide the question. Its copied-folder list at line 75 is
      agents, commands, hooks, scripts and skills, so core/ is not distributed. The task does not name that line.
      The executor has to infer from an absence. The repo also has two tests that pin plugin core copies of
      CODEGRAPH.md. If the executor weighs only the existing listing, it may mirror the file for no distribution
      benefit. The acceptance criterion only needs a recorded, cited decision, so the task is satisfiable either way.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/scripts/build_superclaude_plugin.py:75"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/commands/test_routing_plugin_parity.py:3"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/commands/test_impact_command.py:308"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:69"
    recommendation: >
      In Task 3, name build_superclaude_plugin.py:75 (the copied-folder list, which has no "core") and the plugin
      parity tests as the evidence to cite.
self_audit: >
  I read the whole tasklist and spec sections 2.1 to 2.3, 3 to 4, 6 and 7. I also read the executor severity rules
  (SKILL.md:79-97, qa.md:40-70 and 276-312) and the grounding hunks. I checked these against live files:
  KNOWN_CORE_FILES and the set-equality test; the pinned install manifest in tests/unit/test_cli_install.py (it
  checks that baseline files are present, so a new core file does not break it); the plugin build script; the
  routing-guide tests (the ASCII rule and the marker/heading rules constrain the new Orca section, but Task 4's own
  test run will surface them); Orca's depth-trace files under /opt/Orca (they exist); and the profile file (it holds
  "nestedWorkerMaxDepth":1, so Task 7 is feasible). I found no blocking defect. Every spec-required static outcome
  (AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, and AC-C1 to AC-C6) maps to a task with a runnable acceptance criterion.
  The two-part split is authorized by spec line 238. The reflect candidates did not turn into blockers. Task 1 and
  the KNOWN_CORE_FILES entry land together, which is correct. Task 3's plugin-copy decision is determinable. Task 6's
  phase wording is a should-fix, not a halt, because the task's acceptance criteria do not require a phase. I could
  not verify that `make verify-sync` is clean today, and no baseline is recorded for it. If it already drifts,
  Tasks 4 and 8 would fail on AC-C2, but that comes from the spec's own check.
calibration:
  calibrator_model_class: fable
  self_reported_confidence: 0.70
  dimensions: {citation_grounding: 0.90, coverage_completeness: 0.85, deviation_classification_clarity: 0.85, risk_surface_coverage: 0.75, recommendation_actionability: 0.95}
  calibrated_confidence: 0.86
  severity_holds: {R1-F1: "yes", R1-F2: "yes", R1-F3: "yes", R1-F4: "yes", R1-F5: "yes"}
  notes:
    - "All plan citations verified byte-for-byte: plan:112 ('at most 10' + 'as written in section 2.3'), :56, :47, :72, :93, :125, :147, :154, :37, :22, :69."
    - "Spec citations verified: source:122 says 'maximum of 10 inputs' / 'never exceeds 10' / 'at least 2'; the phrase 'at most 10' appears nowhere in the 452-line spec (full read), so F1's core claim holds."
    - "F3 grounded: source:61 (pr-submit on never-as-worker list), :174 (row applies only if D3 (b)), :201 (never an Orca worker, no Phase 4 changes), :224 and :392 (D3 approved as option (a))."
    - "F4 grounded: source:59 carries 'src/superclaude/cli/install_core.py:36,56,65-70' and CAPS: ids; source:72 carries cmd/ and sk/ evidence paths; plan Constraints (lines 17-27) do not name the installed-path rule."
    - "F5: build_superclaude_plugin.py:75 verified (agents, commands, hooks, scripts, skills; no core). test_routing_plugin_parity.py:3 verified. test_impact_command.py: the plugin core copy is at line 309, not 308 (off by one); the 'two tests' count was not independently confirmed."
    - "Unverified card claim: that task-builder and sc-crash-recovery appear in the write-verb grep (no grep available to the calibrator); it is not load-bearing for F3's severity."
    - "F1 and F3 are borderline should-fix: qa.md:52 makes breach of an explicit task instruction a blocking trigger, so an executor who writes a test phrase not quoted from source.md (F1) or a reason without a converting phase (F3) could draw a B4 finding. The card under-states this route; severity still holds because the executor can satisfy both plan and spec wording, and Task 6's ACs do not require a phase."
    - "F2 holds at should-fix: Task 8's AC is satisfiable by the executor saving outputs at re-run time; the plan under-specifies, it does not prevent the outcome."
    - "Coverage spot-checks found no missed blocker: tests/recommend, tests/core, tests/commands, tests/cli and tests/cli/test_issue_body_templates.py all exist; test_known_core_set_matches_shipped (test_how_we_work_install.py:43-44) confirms the card's KNOWN_CORE_FILES set-equality claim."
    - "Not raised by the card: AC-0.3's numstat check depends on HOW-WE-WORK.md having no pre-existing deletions on this branch versus merge-base; low risk given the branch's recent commits are spec docs only."
    - "Self-reported 0.70 under-states the card's grounding; calibrated 0.86 (+0.16). Delta driven by near-complete citation verification and concrete, placeable recommendations."
