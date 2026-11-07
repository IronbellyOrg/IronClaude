# Reviewer 3 (persona refactorer, opus slot, reflect-reviewer). Persisted verbatim by the orchestrator ("plan" = the P2 static plan path below).
reviewer: 3
persona: refactorer
model_slot: opus
plan: .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
findings:
  - id: R3-F1
    severity: P1
    claim: >-
      Task 16 (tasklist) misses the nested `sc:task` call in tasklist Stage 9, which runs `sc:task` through Skill
      with `--compliance strict` and loops back to it. Task 12 gives task `--unattended`, and the plan's own rule
      (plan:26) says a caller passes `--unattended` and a nested report directory to every callee that accepts it at
      P2. Task 16 only nests the Stage 10.5 reflect call; its EXPECTED_NESTING is ["reflect"] and it depends only on
      Task 15. Under --unattended, Stage 9 would start sc:task as an attended run with its default outward behaviour
      (commit/push and the committed TFEP report), which WC-9 forbids; the test data would lock that gap in.
    evidence:
      - src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557
      - src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1612-1635
      - plan:26
      - plan:233
      - plan:284-295
      - .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:182
    deviation_class: drift
    suggested_fix: >-
      In Task 16, make every Stage 9 sc:task call (loop-backs included) pass `--unattended --report-dir
      <report-dir>/nested/task-<n>/`; add "task" to the tasklist EXPECTED_NESTING, add "Depends on: Task 12", update
      the Task 20 literal; record it as a decision or spec observation (spec row 182 names only Stage 10.5).
  - id: R3-F2
    severity: P2
    claim: >-
      cli-eval: spec row 164 says `run` needs `--suite` and the safety flags in the brief, else blocked. The plan keeps
      `--suite` but drops "else blocked" for the safety flags; W3 asks the user to confirm them. The FR-G5 offer and
      the --no-pty choice get no resolution or AC.
    evidence:
      - .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164
      - plan:60
      - plan:248
      - src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:135-146
      - src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:150-152
    deviation_class: drift
    suggested_fix: >-
      Add to Task 13: a `run` whose brief lacks the safety flags is blocked, with an exact-phrase assertion; state what
      happens to FR-G5 and --no-pty under --unattended; or record the narrowing as an owner decision.
  - id: R3-F3
    severity: P2
    claim: >-
      After Task 17 workflow's reflect step writes to `<report-dir>/nested/reflect-<n>/`, but workflow.md:72 and
      refs/return-contract.md still describe the `.dev/reflect/` run directory, and test lines 837-844 pin that
      clause. Check ADDITIVE lets workflow.md delete one line, which Task 17 spends on line 75, so line 72 stays stale
      and no AC catches it.
    evidence:
      - src/superclaude/commands/workflow.md:72
      - src/superclaude/commands/workflow.md:75
      - tests/skills/test_worker_contract.py:805-844
      - plan:41
      - plan:297-309
      - src/superclaude/skills/sc-reflect-protocol/SKILL.md:58-62
      - src/superclaude/commands/reflect.md:101
    deviation_class: drift
    suggested_fix: >-
      Add a line (or reuse the replacement line) saying reflect's files sit under `<report-dir>/nested/reflect-<n>/`
      under --unattended; update the 837-844 pin in the same task; check return-contract.md; or name workflow.md:72 as
      a second ADDITIVE exemption.
  - id: R3-F4
    severity: P2
    claim: >-
      Task 8 (release-split) handles the brainstorm and adversarial calls but not Part 4's "Invoke appropriate
      analysis (Skill `sc:analyze` or inline verification)"; under --unattended a nested analyze would run with no
      flag and no nested directory.
    evidence:
      - src/superclaude/skills/sc-release-split-protocol/SKILL.md:324
      - src/superclaude/skills/sc-release-split-protocol/SKILL.md:149
      - src/superclaude/skills/sc-release-split-protocol/SKILL.md:190
      - plan:179
    deviation_class: drift
    suggested_fix: State that Part 4 uses inline verification under --unattended, or nest analyze with `nested/analyze-<n>/` and add it to EXPECTED_NESTING.
  - id: R3-F5
    severity: P2
    claim: >-
      Task 15 (reflect) does not cover Wave 1B's optional `tech-research` call (`--depth deep` only); tech-research has
      no Unattended mode, the same case as brainstorm's research-deep arm, which the plan settles but this one it does not.
    evidence:
      - src/superclaude/skills/sc-reflect-protocol/SKILL.md:632
      - src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:190
      - plan:26
    deviation_class: drift
    suggested_fix: In Task 15, "Under --unattended, the Wave 1B tech-research step is skipped and recorded", with an exact-phrase assertion; cite D-P2-1.
  - id: R3-F6
    severity: P3
    claim: >-
      brainstorm.md:158 and sc-brainstorm-protocol/SKILL.md:352 say the handoffs are skipped because their skills "do
      not accept the flag at this phase"; after P2 that reason is false for the P2 targets. ADDITIVE allows only one
      deleted line in brainstorm.md, which Task 18 spends.
    evidence:
      - src/superclaude/commands/brainstorm.md:156-158
      - src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:352
      - plan:41
    deviation_class: drift
    suggested_fix: Record it as an open item in the Task 21 report, or add a line giving the post-P2 reason.
  - id: R3-F7
    severity: P3
    claim: >-
      Task 3 says improve gets the "Same edits" as cleanup, but cleanup's Safety Threshold section has no counterpart
      in improve (Approval Required at :117, Explicitly Will NOT at :125); the executor has no anchor for the copied edit.
    evidence:
      - src/superclaude/commands/cleanup.md:107-127
      - src/superclaude/commands/improve.md:117
      - src/superclaude/commands/improve.md:125
      - plan:110
    deviation_class: drift
    suggested_fix: Name improve's own anchors in Task 3.
  - id: R3-F8
    severity: P3
    claim: >-
      Task 12 says to add the flag "to the flag list line" (task.md:44, "Key flags:") but also "new lines only";
      changing line 44 deletes a line and fails Check ADDITIVE.
    evidence:
      - src/superclaude/commands/task.md:44-48
      - plan:233
      - plan:41
    deviation_class: drift
    suggested_fix: Say "add a new row to the flag table (lines 46-48)"; do not edit line 44.
  - id: R3-F9
    severity: P3
    claim: >-
      cleanup and improve list only Edit/MultiEdit under Tool Coordination; their Unattended report writes a file, and
      P1 pinned that kind of Write for explain. The plan adds no matching assertion.
    evidence:
      - src/superclaude/commands/cleanup.md:49
      - src/superclaude/commands/improve.md:49
      - tests/skills/test_worker_contract.py:847
    deviation_class: drift
    suggested_fix: Add a Write line and a test like test_explain_declares_write_under_tool_coordination, or record why not.
  - id: R3-F10
    severity: P3
    claim: The Task 1 format baseline omits tests/skills/test_sc_recommend_routing_contract.py, which Task 6 edits.
    evidence:
      - plan:73
      - plan:149
    deviation_class: drift
    suggested_fix: Add that file to the baseline list.
  - id: R3-F11
    severity: P2
    claim: >-
      source.md:7 asks each P2 command's `artifacts` clause to point at WC-4 ("left out (WC-4)"); the plan pins it only
      for cleanup and improve; Tasks 4, 13, 14 use other wording and the rest say nothing.
    evidence:
      - .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:7
      - plan:97
      - plan:110
    deviation_class: drift
    suggested_fix: >-
      One parametrized test over all 15 P2 commands: the text after the first backticked `artifacts` contains
      "left out (WC-4)" wherever the command can write ignored files, and never contains "git add".
  - id: R3-F12
    severity: P3
    claim: >-
      [INFERRED] For the D-P2-1 research-light arm, brainstorm's enrichment table expects enrichment/research-light.md
      but /sc:research writes claudedocs/research_[topic]_[timestamp].md; the plan does not say which path brainstorm
      reads. The table also names `Skill sc-research-protocol`, which does not exist.
    evidence:
      - src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189
      - src/superclaude/commands/research.md:103
    deviation_class: drift
    suggested_fix: State the output path in D-P2-1 and correct the skill name in the edit.
  - id: R3-F13
    severity: P3
    claim: >-
      [INFERRED] Task 21's AC requires git status to equal an exact path list; any unrelated dirty or untracked file
      (for example .dev/reflect run folders) fails it.
    evidence:
      - plan:372
    deviation_class: drift
    suggested_fix: Compare against a baseline git status taken in Task 1, or limit the check to the edited paths.
  - id: R3-F14
    severity: P3
    claim: Confirms T1-F2; under the subset rule every existing case still fails, so "drop the equality case" has no target.
    evidence:
      - tests/skills/test_worker_contract.py:898-903
      - tests/skills/test_worker_contract.py:1001-1012
    deviation_class: drift
    suggested_fix: Remove the instruction.
verified_ok:
  - "Depends on chains correct: 12->11, 13->5, 16->15, 17->15, 18->4."
  - "The 11 deferred:P2 WRITE_VERB_CLASSIFICATION entries match the plan's count; no two tasks change the same entry."
  - "No conflicting EXPECTED_NESTING edits; test_only_brainstorm_lists_nested_commands updated in one place."
  - "Mirror rule: pinned files and named plugin copies exist; no plugin WORKER-CONTRACT.md, and the plan claims none."
  - "Task 20's same-line pin can be met: brainstorm.md:157 already has nested/ paths and --unattended on one line."
  - "auggie-review options (--post-pr, --no-remediation-offer, --output-dir) exist at auggie-review.md:49-57."
self_confidence: 0.8
self_audit: >-
  Read the whole plan and source.md; every command and skill anchor cited above at the lines given; the relevant
  parts of test_worker_contract.py; spec rows 140-184. Did not compare the P1 model plan or CLAUDE.md section by
  section. R3-F12 and R3-F13 are [INFERRED]. R3-F1 is the only P1; a reader could argue spec row 182 limits tasklist
  to Stage 10.5, but that would leave an unattended run starting an attended task with outward defaults.
