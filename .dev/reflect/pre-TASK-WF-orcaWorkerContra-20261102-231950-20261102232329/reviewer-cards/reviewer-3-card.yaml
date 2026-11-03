reviewer: 3
persona: refactorer
model_class: opus
verdict: FAIL
self_confidence: 0.72
findings:
  - id: R3-F1
    severity: blocking
    deviation_class: drift
    claim: >-
      Task 7 contradicts itself. Its body says to commit first, then ask for approval and run
      `uv run superclaude install --force`, and then says "Make the commit the last action of
      the task". Its acceptance criterion also requires t7-approvals.md to record the commit ID
      and the install output. If the commit really is the last action, that file cannot hold
      the commit ID unless it is written after the commit. The step order and the acceptance
      criterion cannot both be met. This is the task that runs an owner-approved commit and a
      --force overwrite of ~/.claude, so the executor should not have to guess the order.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:110
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:113
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:282
    recommendation: >-
      Choose one order and write it down. For example: install (approval 2), then write
      t7-approvals.md without the commit ID, then commit (approval 1) as the last repo action,
      then add the commit ID to the ledger or progress.md. Or drop the "commit last" sentence
      and let the artifact stay uncommitted under .dev/tasks.
  - id: R3-F2
    severity: blocking
    deviation_class: drift
    claim: >-
      The spec's section 7.2 step 5 says each phase report must name at least one checked run
      that lasted longer than the heartbeat cadence, so the WC-10 heartbeat check is not passed
      by default. Task 8 does not require any smoke run to be that long, and none of its
      acceptance criteria records it. All three P0 runs could finish under the cadence, and
      step 5 would then pass without checking heartbeats at all.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:125
      - .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1412
    recommendation: >-
      Add a Task 8 acceptance criterion: ac-0.4-smoke.md names at least one run longer than the
      preamble cadence, with its start and end times. If none qualifies, add or extend a run.
  - id: R3-F3
    severity: minor
    deviation_class: drift
    claim: >-
      Task 1's acceptance criterion applies to the whole file: it must contain "no `orca
      orchestration` verb syntax". Task 2 then has to add section 2.3 and WC-6 to the same
      file, and those contain Orca verb syntax (`task-create --spec`, `worker-start --worktree
      new-child --base-branch`, `worker-start --worktree path:`, `orca worktree rm`, `--deps`).
      The spec's "never copies them" rule covers only the worker-session duties. Once Task 2 is
      done, Task 1's criterion fails if the final review re-checks it.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:42
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:49
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:59
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:74
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:88
    recommendation: >-
      Limit Task 1's criterion to the worker-session duties section (WC-3, WC-5, WC-7, WC-12,
      WC-13 and heartbeats), matching source.md:59.
  - id: R3-F4
    severity: minor
    deviation_class: drift
    claim: >-
      Task 7 says to stage "the explicit P0 paths" but never lists them. It commits with
      `git commit --only -- <paths>` while also staging .dev/tasks. With --only, a staged
      .dev/tasks is left out of the commit unless it is named in <paths>. Task 7 also does not
      depend on Task 3, so a dependency-driven executor could commit before install_core.py
      changes.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:108
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:110
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:56
    recommendation: >-
      List the paths: src/superclaude/core/WORKER-CONTRACT.md, src/superclaude/cli/install_core.py,
      src/superclaude/core/HOW-WE-WORK.md, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md,
      tests/skills/test_worker_contract.py, plugins/superclaude/core/WORKER-CONTRACT.md only if
      Task 3 adds it, and .dev/tasks. Name .dev/tasks inside the `--only` pathspec. Add Task 3
      to Task 7's dependencies.
  - id: R3-F5
    severity: minor
    deviation_class: drift
    claim: >-
      Task 1 cannot be reviewed on its own because it leaves the repo with a failing test.
      Creating core/WORKER-CONTRACT.md adds the file to list_core_files() (the installer picks
      up every *.md in core/). test_known_core_set_matches_shipped then fails until Task 3
      updates KNOWN_CORE_FILES. Task 1's own acceptance criteria do not mention this.
    evidence:
      - tests/cli/test_how_we_work_install.py:43
      - tests/cli/test_how_we_work_install.py:44
      - src/superclaude/cli/install_core.py:13
      - src/superclaude/cli/install_core.py:140
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:35
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:60
    recommendation: >-
      Move the KNOWN_CORE_FILES edit into Task 1 so the file creation and its registration are
      one change, or state that tests/cli stays red between Task 1 and Task 3.
  - id: R3-F6
    severity: minor
    deviation_class: regression
    claim: >-
      Task 4 edits HOW-WE-WORK.md but runs only three test files. At least four other test
      files read the guide or its plugin copy. The AC-C3 baseline covers only tests/skills/,
      so a break in tests/commands or tests/recommend would go unnoticed.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:77
      - tests/commands/test_routing_plugin_parity.py:38
      - tests/recommend/test_routing_refresh.py:90
      - tests/recommend/test_routing_refresh.py:609
      - tests/commands/test_help_command.py:39
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:263
    recommendation: >-
      Extend Task 4's acceptance criterion to `uv run pytest tests/core tests/commands
      tests/recommend tests/cli -q`, compared against a baseline taken in Task 1.
  - id: R3-F7
    severity: minor
    deviation_class: drift
    claim: >-
      Task 4 writes the current phase state into HOW-WE-WORK.md ("after P0, none") and copies
      the never-as-worker set into it. That line goes stale every phase, and fixing it means
      editing a line in the guide and its plugin copy, which works against the additive SA-5
      approach. It also repeats what the spec's section 6 table already says.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:74
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:212
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:228
    recommendation: >-
      Say instead that a command accepts --unattended only when its file has an `## Unattended
      mode` section, and point to ~/.claude/WORKER-CONTRACT.md for the never-as-worker list.
      That wording does not need to change between phases.
  - id: R3-F8
    severity: minor
    deviation_class: drift
    claim: >-
      The negative checks in Tasks 5 and 6 have no safe way to run. The test reads fixed
      src/ paths, and the audit scans src/superclaude/skills/. Running them against a scratch
      copy therefore means editing the real WORKER-CONTRACT.md or adding a scratch skill under
      src/superclaude/skills/. A scratch skill left behind would make verify-sync report a
      missing .claude/ copy. AC-C1 and AC-C2 run only in Task 4, before these tasks.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:87
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:91
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:100
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:79
      - Makefile:171
      - Makefile:174
    recommendation: >-
      Have the test take the contract path and the scan roots from a fixture or environment
      variable, run the negative checks against tmp_path copies, and re-run AC-C1 and AC-C2
      after Task 6.
  - id: R3-F9
    severity: minor
    deviation_class: drift
    claim: >-
      Task 5 does not say how specific its assertions must be. A test that only checks for
      labels such as "WC-2" passes on a file that names rules without stating them. The
      negative check would still pass, because deleting the label fails the assertion. The
      spec's own pass condition, "not empty of rules", is weak too.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:87
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:298
    recommendation: >-
      Require at least one distinctive phrase per rule, for example: the WC-4 error text, the
      seven field names, the four `guard refused:` texts, "at most 10" and "at least 2", the
      guard line, and the `<caller report-dir>/nested/` path.
  - id: R3-F10
    severity: minor
    deviation_class: drift
    claim: >-
      Task 2's brief template copies the section 3.1 "Brief must pass" flags as they are. For
      cleanup-audit and workflow those flags include `--report-dir <dir>`, which no command
      accepts until P1; searching src/superclaude/commands for --report-dir finds nothing. A
      coordinator using the installed template between P0 and P1 would pass a flag the command
      does not know.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:49
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:143
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:152
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:221
    recommendation: >-
      Have the template mark `--report-dir` as "from P1". The P0 smoke-run commands in Task 8
      already leave it out.
  - id: R3-F11
    severity: minor
    deviation_class: drift
    claim: >-
      No closing task gives a single P0 pass or fail result, even though P1 may start only
      after it. AC-C5 is never recorded as run, even though no command file changes in P0.
      AC-C1 and AC-C2 run mid-plan and are not repeated at the end. The spec says a phase
      passes only when every check passes and refers throughout to a "phase report"; the
      tasklist spreads the results across separate files.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:216
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:241
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:271
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:15
      - .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1409
    recommendation: >-
      Add a final task that re-runs AC-C1, AC-C2 and AC-C4, records AC-C5 with no files to
      check, and writes artifacts/p0-phase-report.md with one PASS or FAIL line per check,
      linking the existing artifacts.
  - id: R3-F12
    severity: minor
    deviation_class: drift
    claim: >-
      Task 3 cites KNOWN_CORE_FILES as lines 13-25. The frozenset actually runs from line 13
      to line 27, with entries on lines 15-25. This is a small citation error and does not
      affect correctness.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:60
      - src/superclaude/cli/install_core.py:13
      - src/superclaude/cli/install_core.py:27
    recommendation: Cite the symbol name rather than a line range, or use 13-27.
  - id: R3-F13
    severity: minor
    deviation_class: drift
    claim: >-
      Task 6 lets a git or gh write-verb hit pass with the label "refused under --unattended by
      the phase that converts its command". At P0 nothing is refused, so that label proves
      nothing yet. The task also does not define what counts as a `gh api` post (-X POST,
      --method, -f/-F).
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:97
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:305
    recommendation: >-
      At P0, require every hit to be either allowed by WC-9 or on the allowlist, with a
      reference to the phase that will convert it. Spell out the `gh api` post patterns
      (`-X POST`, `--method POST`, `-f`, `-F`, `--input`).
  - id: R3-F14
    severity: minor
    deviation_class: drift
    claim: >-
      Task 8 records the AC-0.6 yes or no answer but does not say what to do if it is no:
      switch the step-5 checks to `--source terminal` and record the gap. Without that, the
      step-5 results could rest on a transcript that does not show tool calls.
    evidence:
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291
      - .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:127
    recommendation: >-
      Read the AC-0.6 transcript first. If tool calls are not named, run step 5 for all three
      runs on `--source terminal` and record that in ac-0.4-smoke.md.
agreements_with_t1_card:
  - >-
    Tasks 1 and 2 refer to spec rules by label instead of copying them. That keeps drift down,
    and it is why the containment matcher under-counts sections 2.1-2.3
    (coverage-matrix.yaml:1405). By meaning, those rows are assigned to WORKER-CONTRACT.md.
    The remaining risk is in how specific Task 5's assertions are (R3-F9).
  - >-
    Task 6's forward reference "refused under --unattended" has nothing to check against at P0,
    so every hit has to sit on the allowlist (TL:97; source.md:305). See R3-F13.
disagreements_with_t1_card:
  - >-
    The T1 card ties Task 3's plugin-mirror decision to UNVERIFIED item 8 (source.md:432). Item 8
    is about plugins/superclaude/commands/, not plugins/superclaude/core/, and P0 edits no command
    files, so item 8 does not apply in P0. On the core question, the evidence points to no copy:
    scripts/build_superclaude_plugin.py:75 copies only agents, commands, hooks, scripts and skills,
    never core, and plugins/superclaude/core/ is only partial (no HOW-WE-WORK.md, CLAUDE.md or
    ISSUE-*). The AC-C1 exclusion of plugins/superclaude/core/WORKER-CONTRACT.md (source.md:252)
    would then never match anything.
  - >-
    The T1 card has no blocking finding about structure. Task 7's contradictory order (R3-F1) is
    a real defect: an acceptance criterion that cannot pass, in the task that runs the
    owner-approved --force install.
self_audit: >-
  I read the brief, the whole tasklist (1-137), source.md 51-214, 215-372 and 425-452, the whole
  coverage matrix, install_core.py, test_how_we_work_install.py, test_issue_body_templates.py,
  build_superclaude_plugin.py, the Makefile sync-dev and verify-sync targets (109-353), and the
  tests that read HOW-WE-WORK.md. I did not open test_sc_recommend_routing_contract.py or
  test_help_command.py beyond their Grep hits, and I did not open the "Key Documentation Files"
  part of the repo CLAUDE.md beyond what the session context showed. Codegraph's index state was
  unknown, so I used only Read, Grep and Glob. The repo-layout assumptions hold: install_core.py,
  KNOWN_CORE_FILES, test_how_we_work_install.py:44, plugins/superclaude/core/ (6 .md files),
  scripts/build_superclaude_plugin.py, src/superclaude/core/HOW-WE-WORK.md and the sc-recommend
  refs copy all exist. No plugins/superclaude/core/HOW-WE-WORK.md exists, so Task 4 is right to
  name only the sc-recommend copy plus the CLAUDE.md level table. R3-F2 is graded blocking
  because the spec states the cadence-length run as a requirement on every phase report; an
  orchestrator could reasonably treat it as a coverage gap rather than a structural one. R3-F1
  could be settled by executor judgment, but as written the acceptance criterion cannot pass.
calibration:
  calibrator_model_class: fable
  scores: {citation_grounding: 0.88, coverage_completeness: 0.85, deviation_classification_clarity: 0.85, risk_surface_coverage: 0.85, recommendation_actionability: 0.90}
  calibrated_confidence: 0.87
  severity_holds: {R3-F1: "yes (blocking; 'AC cannot pass' overstated, artifact can be written after the commit)", R3-F2: "no (downgrade to minor: Task 8 incorporates 7.2 step 5 by reference at TL:122)", R3-F3: yes, R3-F4: yes, R3-F5: yes, R3-F6: "yes (count and test_help_command cite overstated)", R3-F7: yes, R3-F8: yes, R3-F9: yes, R3-F10: yes, R3-F11: yes, R3-F12: yes, R3-F13: yes, R3-F14: yes}
