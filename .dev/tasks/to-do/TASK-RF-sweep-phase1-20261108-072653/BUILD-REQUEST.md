# BUILD REQUEST

Source: user
TASK_DIR: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/
TASK_FILE: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
SPEC: docs/designs/orchestrator-mode.md
CLI_MODE: false

GOAL: Build the MDTM task file for issue #339 Phase 1 (orchestrator mode). The task, when run by `/task`, first closes five required design items on `docs/designs/orchestrator-mode.md`, then implements, exactly as that design specifies:
- the read-only, coordinator-only `superclaude sweep run` CLI under `src/superclaude/cli/sweep/`:
  - `__init__.py` with a lazy `__getattr__`;
  - `models.py`;
  - a pure `classify.py`;
  - `probes.py`, with the single `_orca` and `_git` seams and an exact argv allowlist;
  - `report.py`;
  - `commands.py`, a Click group whose `_publish` writes a temp file, fsyncs it and calls `os.link`;
  - deferred registration in `src/superclaude/cli/main.py`, after line 565 on the current base;
- the thin `/sc:sweep` command (`src/superclaude/commands/sweep.md`) and the `sc-sweep-protocol` skill;
- the coordinator-loop contract rule. It is numbered WC-16, not WC-14, because master has WC-14 and WC-15 from PR #434. The rule goes in `src/superclaude/core/WORKER-CONTRACT.md` together with the never-as-worker addition and the contract-test pins;
- the routing and doc rows R1 to R8, and `.dev/sweeps/` in `.gitignore`;
- the tests in `tests/sweep/` and `tests/commands/test_sweep_command.py`.

The design's section 15 maps REPORT steps 1.0a to 1.29.

WHY: Issue #339. The person needs one read-only report that answers "who needs me and what is safe to close" without opening each Claude session. The coordinator chain selected `/task-builder` then `/task`. The requirements are in `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (SPEC). The design is `docs/designs/orchestrator-mode.md` (DESIGN).

TASK_ID_PREFIX: TASK-RF
TEMPLATE: 02
QA_INTENSITY: full
QA_GATE_REQUIREMENTS: PER_PHASE. Apply the task-builder QA encoding rules M3, M4, I19, I20, I21 and I22:
- lens-based rf-qa and rf-qa-qualitative agents, each its own `- [ ]` item with an embedded lens prompt;
- report-only agents first, then a single fix agent, then verification;
- at most 2 fix cycles; minor findings never fail a gate.

Size the gates by output size. research/09-gap-fill.md Gap 5 gives the full-intensity counts: a final-document gate on the 1013-line design needs 8 agents plus domain lenses, and a fidelity gate on the design plus the SPEC needs 3 to 4 agents. Give every gate its own `qa/<gate>/` subfolder so reports are not overwritten (research/06).

VALIDATION_REQUIREMENTS: `make sync-dev`, then `make verify-sync`, `make lint`, `uv run ruff check .`, `uv run ruff format --check src/ tests/`, and `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend`, followed by the full `uv run pytest`. A validation item comes after each implementation phase. Run the step 1.28 primitive-path grep scoped to the new and edited files; it must return 0 (research/09 Gap 3).

TESTING_REQUIREMENTS: UNIT plus one real-git INTEGRATION test. Design section 11 lists the tests; research/05 maps each to its pattern and command.
- `tests/sweep/__init__.py` is required.
- The guard that blocks real subprocess calls must read only each test's own markers (research/05).
- The real-git test copies the repo `.gitignore`.
- No live Orca, ccsession or Claude launch in any test.

EXECUTION_CONTEXT_INSTRUCTION: populate `## Execution Context` with References (this GOAL verbatim, the WHY summary, the SPEC and DESIGN paths), Source areas (module names only, no `file:line`) and Key constraints.

POST_REFLECT_GATE: ENABLED
  TASK_FILE: the TASK_FILE above
  CLI_MODE: false (reflect_post_mode: skill; emit the dedicated-subagent-runner POST item with the runner prompt verbatim)
  SPEC_PATH: docs/designs/orchestrator-mode.md
  DEPTH: deep. The TCS is well above 35: S1 alone counts more than 25 distinct files.
  DIFF: this project commits only when the user asks, so `{BASE}..HEAD` would audit nothing. Add an item right before the POST item that builds a diff file at `${TASK_DIR}reflect/post/phase1.diff`: run `git diff --binary <start base>`, then append `git diff --no-index /dev/null <file>` for each new untracked file the task created (research/09 Gap 6). Fill the runner prompt's `--diff` with that diff-file path. Record this substitution in Open Questions as a deliberate placeholder fill.

MANDATORY PHASE ORDER (the coordinator's conditions):
1. Setup (status, start_date).
2. Required design-fix items, all before ANY code task. Each item edits DESIGN and is closed by its own QA gate (report-only lens agents, then a fix agent, then verification). Apply research/04 sections 2 to 5 and research/09 Gap 4, anchoring edits by quoted text because review-3 line numbers are off by 6.
   - R3-B1: the session-to-Dispatch time-window rule reads three time fields the data model lacks. Add Dispatch start (`dispatch.dispatchedAt`), Dispatch end (`dispatch.completedAt`) and the earliest transcript timestamp (`first_record_ts` on `TranscriptTail`). Also add the UTC parsing rule, the inclusive whole-second window, and the 6 + 4 fixtures in sections 11 and 12.
   - R3-B2: two Dispatch rows on one pane give conflicting results and no rule decides. Add the unique-containing-window rule, the two notes `conflict: one pane session matches several Dispatch rows` and `pane moved to a later session`, and 7 fixtures.
   - R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py`. Restore them, add the `origin unknown:` notes, and add the per-Run source row `orca worker-list <run>`.
   - R4: reconcile DESIGN with master (`5dc29d23`). Renumber the design's rule to WC-16 everywhere; the `RULE_PHRASES` key must not collide with WC-14 (research/07). Align the coordinator-loop text with master's section 4 "The sweep" (`WORKER-CONTRACT.md:110`, at most once every 5 minutes, pinned at test :212). Re-anchor every cited line, using research/07 and research/08. Main.py goes after line 565. Record the new constraints: `sweep.md` gets no `## Unattended mode`, `UNATTENDED_EXPECT` stays at 31, and the write-verb classification table is updated. Step 1.16a becomes record-only, because PR #422 is merged.
   - R5, OWNER DECISION PENDING. This is a HALT item; do not resolve it. Master's sweep at `WORKER-CONTRACT.md:110` runs `worktree ps --agent-wait`, but INV-005 sign-off condition 1 allows `worktree ps` only WITHOUT `--agent-wait`. Describe both options:
     - (a) extend the sign-off to `--agent-wait` after a lock check;
     - (b) keep "never" and fix the master contract text in a later PR.
     Encode R5 with the human-gate pattern from research/06: an OQ-n Open Question, a PENDING decision-record item, and a HALT item that sets status to "⚪ Blocked" and stops without ticking until the decision is recorded. It blocks every code task.
3. Pre-implementation gates, each encoded with the same human-gate pattern:
   - step 1.0b: owner decisions GQ-10, GQ-11, GQ-35, GQ-61 and GQ-63, plus the D9 sign-off (research/09 Gap 1). GQ-63 has no recommendation, so state that. D9 blocks the classify step;
   - step 1.0a: the read-only Orca capture against an existing Run named by the person, using ONLY the eight allowlisted templates (DESIGN 15.1);
   - step 1.16a: record-only.
4. Implementation, one item per file, in design section 15 step order. research/01 section D gives the per-file list. Fill the gaps research/01 names:
   - define `ClassifiedRow`;
   - carry the ten #409 dimensions (lifecycle, phase, health, approval, freshness, result, admission, evidence_packet, policy, tests_review) from REPORT:1245 into the report only, per research/09;
   - put the step 1.4a test after the fakes it needs;
   - CHANGELOG uses `### <title>` with `#### Added (<topic>)`;
   - apply R2 before R1, or anchor it by text.
   `test_worker_contract.py` needs FIVE pin edits, including `RULE_PHRASES["never-as-worker"]` at about line 89 (research/03 and research/07).
5. Tests, then validation, then the final QA gate, then the diff-file item, then the POST reflect item, then Update status to Done (anti-orphaning).

DOCUMENTATION STALENESS WARNINGS:
- The branch was fast-forwarded from e8db2fe6 to 5dc29d23. research/01 to research/06 cite the old base. Where they disagree with research/07 and research/08, the latter win. Only the 12 cited files that changed on master were re-anchored; this is an approved deviation, and the research gates were not re-run (coordinator `delivery_b55fdfcd1286`).
- DESIGN still says WC-14 and main.py:561. R4 fixes both. Do not build code items on those values.

RESEARCH DIR: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/. Read ALL nine files:
- 01 file inventory;
- 02 patterns and conventions;
- 03 integration points;
- 04 design fixes R3;
- 05 test and verification;
- 06 template and examples;
- 07 re-anchor, contract side;
- 08 re-anchor, routing side;
- 09 gap fill.

QUALITY GATE RESULTS: the five A.8 reports in `qa/` all said FAIL. research/09 filled their blocking gaps, and research/07 and 08 handled the stale base. Per the coordinator, the gate was not re-run. Treat the minor notes in the five reports as notes.

OPEN QUESTIONS to record in the task file:
- R5 (`--agent-wait`);
- GQ-10, GQ-11, GQ-35, GQ-61, GQ-63 and D9;
- the permission syntax `Bash(...:*)` against `Bash(... *)` (research/02). Keep the design's form unless R4 changes the design and its test together;
- step 1.29, pipx (`pipx run --spec` against `pipx install --force`, which needs owner approval);
- the `policy` dimension against `policy_of`;
- the POST diff-file substitution;
- the things UNVERIFIED until step 1.0a: the live field names and time format, where `completedAt` is written, the join key, and the `page.nextCursor` shape.

HARD CONSTRAINTS:
- `/task` must never commit, push or merge. Include no commit or push item; commits happen only when the user asks.
- Never stage `.claude/` except `settings.json`. Always stage `.dev/tasks/`.
- UV only.
- Installed primitives use `~/.claude/...` paths, never `src/superclaude/...`.
- No live Orca, ccsession or Claude launch in tests. Step 1.0a uses allowlisted read verbs only.
- No item may run the WC-9 lock retry. That work is out of scope and tracked in IronbellyOrg/IronClaude#446; add a note saying so.
- The PR is opened later, only via `/sc:pr-submit --monitor 3`.
- The executor reads files in chunks of at most 150 lines.

GRANULARITY, INCREMENTAL WRITING, ESCALATION: follow the task-builder BUILD_REQUEST rules:
- one item per file or component;
- write the frontmatter and overview first, then append one phase per Edit, then the Task Log;
- no team tools.
Return the task file path as the final output.
