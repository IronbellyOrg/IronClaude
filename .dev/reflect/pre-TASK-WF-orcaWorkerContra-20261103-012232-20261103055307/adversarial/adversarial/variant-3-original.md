reviewer: 3
persona: refactorer
model_class: opus
verdict: FAIL
self_confidence: 0.6
findings:
  - id: R3-F1
    severity: blocking
    deviation_class: drift
    tasks: [4]
    claim: >
      The Constraints say "P0 edits no command, skill or agent file". Task 4 tells the executor to write
      plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md, which is a file inside a skill
      package. QA counts a quoted Constraints breach as blocking as soon as the quoted text is
      byte-present in the plan, and here it is. A repair cannot satisfy both the constraint and the
      task instruction. So a strict Task 4 reviewer ends the run in a ladder-end halt or a dispute
      halt. The spec only says "no command edits" and requires the mirrored copy. The plan widened
      the wording and created this conflict itself.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:21"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:90"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:220"
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:52"
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:61"
    recommendation: >
      Reword the constraint as: "P0 edits no command file, no SKILL.md and no agent file; the only
      file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md in
      plugins/superclaude/skills/sc-recommend/refs/ that Task 4 makes."
  - id: R3-F2
    severity: should-fix
    deviation_class: drift
    tasks: [2]
    claim: >
      The Constraints say WORKER-CONTRACT.md "restates only what ./source.md sections 2.1, 2.2 and
      2.3 say". Task 2 tells the executor to put content from other sections into it: the "Brief
      must pass" flags of section 3.1 for 12 commands, and the "from P1" marker taken from section 6.
      Spec section 6 (P0 row) does require this, but the Constraints never name 3.1 or 6. A reviewer
      who quotes the constraint against Task 2's diff can raise a blocking finding that no repair can
      close.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:22"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:58"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:139"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:220"
    recommendation: >
      Add to the constraint: "plus, in the brief template only, the section 3.1 'Brief must pass'
      flags and the section 6 phase markers (`--report-dir` from P1)."
  - id: R3-F3
    severity: should-fix
    deviation_class: drift
    tasks: [1, 2, 3, 5]
    claim: >
      Task 5 must assert, for each rule, "a phrase quoted from ./source.md". Tasks 1 and 2 only
      require verbatim text for the three reason texts, the WC-4 error text and the guard line. If
      Tasks 1 and 2 paraphrase any other rule, Task 5 has no source phrase to pin. Its only way out is
      to edit WORKER-CONTRACT.md, a file Task 5 does not own and that Tasks 1-3 already delivered and
      checked. If Task 3 added a plugin copy, that edit also breaks Task 3's `cmp` acceptance check
      after the fact. The managed FINAL review returns `issues` when "a later change contradicts" an
      acceptance check, which blocks archiving.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:45"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:61"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:74"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:104"
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:310"
    recommendation: >
      Add an acceptance check to Tasks 1 and 2: each rule carries at least one key phrase copied
      verbatim from source.md, with the phrases listed in a ./artifacts file that Task 5 then pins.
      Alternatively, let Task 5 edit the contract, and make it re-run Task 3's install check and
      `cmp` afterwards.
  - id: R3-F4
    severity: should-fix
    deviation_class: none
    tasks: [3, 5]
    claim: >
      If Task 3 adds plugins/superclaude/core/WORKER-CONTRACT.md, nothing keeps it in sync after
      Task 3's one `cmp`. `make verify-sync` checks only skills, agents, commands, hooks, templates
      and installer registration, not core. No test pins the copy either. P1-P4 will edit the
      contract, so the copy will silently go stale.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/Makefile:170"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/Makefile:202"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/Makefile:228"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/Makefile:254"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/Makefile:280"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:69"
    recommendation: >
      If Task 3 adds a copy, Task 5's test asserts the plugin copy is byte-identical to the src
      file, following the existing pattern in tests/commands/test_workflow_command.py
      (test_plugin_mirror_matches_src).
  - id: R3-F5
    severity: should-fix
    deviation_class: drift
    tasks: [6]
    claim: >
      Task 6 requires every allowlist entry to carry "the phase that converts its command". The
      write-verb scan matches all `gh pr` (40 hits), including read-only `gh pr view`, `list` and
      `checks`. It also matches hits in agents and in protocol skills that no phase converts. None of
      these have a converting phase, so the executor has to invent one. The spec's AC-0.9 asks only
      for "an explicit allowlist with a reason". The plan also does not say how entries are keyed.
      Line-number keys break on any later edit to the roughly 121 hit sites.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:125"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/grounding-hunks.md:94"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/grounding-hunks.md:102"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:305"
    recommendation: >
      Key each classification by (repo-relative path, verb, stripped line text), never by line
      number. Use a closed category set: wc9-allowed, read-only, deferred:<phase>, or no-command with
      a reason. Ask for the converting phase only when a command owns the hit.
  - id: R3-F6
    severity: should-fix
    deviation_class: none
    tasks: [4]
    claim: >
      The routing-guide tests that AC-0.2 runs constrain the new Orca section in ways Task 4 never
      mentions. Any non-ASCII character fails a test (for example an em dash or an arrow copied from
      the spec, which uses both). Some tests slice the guide between fixed headings ("### 3.14 " to
      "## 4. ", and the routing and level-table markers). A section placed inside one of those slices
      can break them. Each failure costs a repair round on Task 4.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/core/test_how_we_work_routing_table.py:341"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/core/test_how_we_work_routing_table.py:290"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:90"
    recommendation: >
      Add to Task 4: "the new section is ASCII only and is appended as a new top-level section after
      the last existing section, outside the level-table and routing markers."
  - id: R3-F7
    severity: minor
    deviation_class: none
    tasks: [5]
    claim: >
      Task 5 hard-codes "no command has an `## Unattended mode` section". From P1 onward, AC-1.1
      needs a positive per-phase list of commands that do have the section. A bare negative assertion
      forces each later phase to rewrite the test's logic instead of extending its data.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:115"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:306"
    recommendation: >
      Write it as a module-level map ACCEPTS_UNATTENDED = {"P0": set()} (cumulative by phase), and
      assert that the set of commands with the section equals the set for the current phase.
  - id: R3-F8
    severity: minor
    deviation_class: none
    tasks: [2, 5]
    claim: >
      The brief template copies the section 3.1 flags of 12 commands, but no test checks those flags
      against the command files. The routing guide already has that kind of check for its notes
      flags. When P1 changes command flags, the template will drift without any test failing.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:58"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/core/test_how_we_work_routing_table.py:258"
    recommendation: >
      In Task 5, assert that every flag token in the template exists in src/superclaude/commands/<name>.md
      for its command, except `--report-dir` and `--unattended`, which are marked "from P1".
  - id: R3-F9
    severity: minor
    deviation_class: none
    tasks: [4]
    claim: >
      The Goal says the routing guide gets an Orca section "in every copy the repo keeps". Task 4
      correctly leaves the core CLAUDE.md copy unchanged, because that copy mirrors only the level
      table. The Goal and the task body disagree.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:15"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:90"
    recommendation: >
      Reword the Goal: "the Orca section is in HOW-WE-WORK.md and its plugin copy; the CLAUDE.md
      level-table copy is unchanged".
  - id: R3-F10
    severity: minor
    deviation_class: none
    tasks: [8]
    claim: >
      Task 8 stages .dev/tasks before the executor writes its last ledger lines and before the
      archive moves the folder to done/. The staged entries then point at stale to-do/ paths. The
      next steps the report must list leave out re-staging .dev/tasks at commit time, which spec
      section 2.3 assigns to the coordinator.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:154"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:90"
    recommendation: >
      Add to the report's next steps: "the coordinator re-runs `git add .dev/tasks` and AC-C4
      immediately before the commit".
  - id: R3-F11
    severity: minor
    deviation_class: none
    tasks: [1, 4]
    claim: >
      Task 1 records no `make verify-sync` baseline, so a failure that already exists would show up
      as an AC-C2 failure in Task 4. The wider test baseline also leaves out tests/docs and
      tests/unit. Both scan every .md file under src/superclaude, so the new core file is covered
      only by a run the plan never makes.
    evidence:
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:35"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:96"
      - "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/docs/test_retired_docs_absent.py:40"
    recommendation: >
      In Task 1, also save `make verify-sync` output, and add tests/docs and tests/unit to the wider
      baseline command and to Task 4's comparison.
self_audit: >
  I read the whole tasklist, the brief, the grounding hunks, the executor rules (SKILL.md:79-97,
  qa.md:40-70 and 276-312) and spec sections 2.1-2.3, 3.1 (rows), 6 and 7. I checked that every
  Constraint is consistent with every task body and acceptance check. I checked task ordering under
  source-order execution, and the dependencies between Tasks 1-2, 3 and 5 (the contract's wording
  versus the test's quoted phrases, and the plugin copy). I checked the Makefile verify-sync scope,
  the core-file tests (test_how_we_work_install.py, test_cli_install.py, test_retired_docs_absent.py)
  and the routing-guide test constraints. The single blocking finding, R3-F1, is a literal conflict
  between a Constraints sentence and a direct instruction in Task 4. QA derives severity
  mechanically from the byte-present quote, and no repair can resolve the conflict, so it can halt
  the run. My confidence is moderate because a lenient reviewer might read the constraint through
  its "no command edits" citation. R3-F2 has the same shape but is easier to defend from spec
  section 2.1's "including its brief template", so I graded it should-fix. I found no defect in
  ordering or in the static-versus-live split, and nothing in the plan prompts the user.
calibration:
  calibrator_model_class: fable
  self_reported_confidence: 0.6
  dimensions: {citation_grounding: 0.95, coverage_completeness: 0.85, deviation_classification_clarity: 0.85, risk_surface_coverage: 0.85, recommendation_actionability: 0.90}
  calibrated_confidence: 0.88
  severity_holds: {R3-F1: "yes", R3-F2: "yes", R3-F3: "yes", R3-F4: "yes", R3-F5: "yes", R3-F6: "yes", R3-F7: "yes", R3-F8: "yes", R3-F9: "yes", R3-F10: "yes", R3-F11: "yes"}
  notes:
    - "All spot-checked citations match: plan lines 15, 21, 22, 35, 45, 58, 61, 69, 74, 90, 96, 104, 115, 125, 154; source.md 90, 139, 220, 305, 306; qa.md 52, 61, 310; Makefile 170/202/228/254/280 (no core section in verify-sync); tests 258, 290, 341; grounding-hunks 94-103; test_retired_docs_absent.py:40."
    - "R3-F1 verified: constraint line 21 says 'no command, skill or agent file'; Task 4 line 90 writes plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md; qa.md:52/61 derive blocking mechanically from a byte-present constraint quote, and the only repair path is a dispute halt. Blocking holds but is conditional on a reviewer reading the constraint literally; constraint line 24 already names 'their plugin copies', which a lenient reviewer would use. Card's 0.6 self-confidence reflects this and is honest."
    - "R3-F1 and R3-F2 share the same mechanism (narrowed constraint vs. task instruction); the card's split grading (blocking vs should-fix) is defended by spec 2.1 'including its brief template' and 2.3's reference to section 3 flags, which is a reasonable distinction but not a sharp one."
    - "R3-F3's archive-block path (qa.md:310 'a later change contradicts it') is real but doubly conditional: Task 1/2 paraphrase AND Task 3 added a plugin copy. should-fix is the right tier."
    - "R3-F3 is labelled deviation_class drift but is an intra-plan inconsistency (Task 5 vs Tasks 1-2), not a departure from source.md; minor classification looseness."
    - "R3-F6 citation test:290 shows fixed-marker ordering/slicing (_LEVEL_END < _OTHER_BEGIN < _ROUTE_BEGIN), not the '### 3.14'/'## 4.' slice the card quotes; the claim stands but that specific quote is not at the cited line."
    - "R3-F5 verified: spec AC-0.9 (source.md:305) requires only 'an explicit allowlist with a reason'; plan line 125 adds 'the phase that converts its command', which has no answer for agent hits or read-only gh pr view/list/checks among the 40 gh pr hits."
    - "Coverage gap: card does not check the install_core_files(target_path=...) signature used in Task 3's AC-0.1 command, nor that /opt/Orca and ~/.config/orca exist for Task 7; both are environment assumptions the plan inherits from the spec."
    - "Self-reported 0.6 is a severity-uncertainty number for R3-F1, not a card-quality number; calibrated 0.88 scores the card's grounding and coverage, which are strong."
