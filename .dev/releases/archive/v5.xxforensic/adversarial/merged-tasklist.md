<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (forensic-refactor-handoff.md) -->
<!-- Incorporated: Variant B (tfep-refactoring-context.md) -->
<!-- Invariant resolutions: INV-001, INV-004 -->
<!-- Merge date: 2026-03-19 -->

# Forensic Refactor Tasklist: Quick Mode + Task-Unified Integration

## Constraints (User-Approved Decisions)
<!-- Source: Variant B, Section 9 — merged per Change #9 -->

| Decision | Resolution | Source |
|----------|-----------|--------|
| Artifacts committed to git | Yes | User requirement |
| User notification during TFEP | Autonomous — proceed through all phases, report at end | User requirement |
| CLI code changes needed | None — purely protocol-level | User requirement |
| Naming | TFEP (Test Failure Escalation Protocol) | User approved |
| Threshold: every failure triggers? | No — only actual code bugs above threshold | User requirement |
| Report format | Standalone `tfep-report.md` per escalation | User approved |
| Max escalation iterations | 3 then full stop | Adversarial recommendation |
| "Test is wrong" as valid outcome | Yes — adversarial debate can conclude test expectations are outdated | Brainstorm decision |

## Architectural Principles
<!-- Source: Base (original) — Variant A, Sections 5, 8 -->

- **Core split**: `task-unified` owns **when** forensic is needed; `/sc:forensic` owns **how** forensic is executed
- **Flag model**: Three orthogonal dimensions — `--intent` (debug|qa|regression|auto|triage), `--tier` (light|standard|deep), `--debate-depth` (quick|standard|deep)
- **Profiles**: Forensic modes map to profiles (triage → light tier, investigation → standard tier, full forensic → deep tier)
- **Genericity**: Forensic must remain reusable for roadmap failures, QA, regression triage, release hardening — not task-unified-only
- **Caller-awareness**: `--caller <command>` flag allows forensic to auto-select defaults per invoking context

---

## Phase 1: Immediate Guard (This Sprint)
<!-- Source: Variant B, Section 8 — merged per Change #4 -->

**Goal**: Block ad-hoc fixes immediately. Zero dependency on forensic being built. ~30 lines in SKILL.md.

### Task 1.1: Add TFEP prohibition rule to task-unified protocol
<!-- Source: Base (original, modified) — A S4 + B S3.4 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`
**Scope**: ~30-50 lines addition

Add CRITICAL/VIOLATION-level language:
- [ ] Add "Test Failure Escalation Protocol (TFEP)" section header
- [ ] Add VIOLATION rule: "Agents MUST NOT fix any code in response to test failures without completing the TFEP workflow"
- [ ] Add VIOLATION rule: "Agents MUST NOT modify test expectations to make failing tests pass without adversarial validation"
- [ ] Add VIOLATION rule: "Ad-hoc patches from test output are PROHIBITED"
- [ ] Add permitted exception: "Single ImportError/NameError in test scaffolding just written by agent, affecting <=2 tests, error in test file not implementation"
- [ ] Add permitted exception: "Lint/formatting failures (trivially fixable, unambiguous root cause)"
- [ ] Add permitted exception: "Deprecation warnings (not failures)"
- [ ] Document that "test expectations are wrong" is a valid adversarial outcome, not grounds for direct editing

### Task 1.2: Add escalation trigger detection rules
<!-- Source: Variant B, Section 4 — merged per Change #2 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`
**Scope**: ~20-30 lines addition

Binary entry-gate thresholds (MUST escalate):
- [ ] Any pre-existing test fails (tests that existed before this task and were not modified by the agent)
- [ ] 3 or more new tests fail (indicates systemic issue)
- [ ] Runtime exceptions in implementation code (TypeError, AttributeError, KeyError in code being tested)

Qualitative within-TFEP escalation triggers (escalate from light → standard → deep):
- [ ] Repeated failure (same test cluster fails after fix attempt)
- [ ] Multi-file blast radius from recent changes
- [ ] Low-confidence root cause from adversarial debate
- [ ] Unresolved adversarial outcome (no winner/tie)
- [ ] Second failed retest
- [ ] Cross-domain or non-obvious regression

### Task 1.3: Add test baseline snapshot mechanism
<!-- Source: Invariant probe INV-001 — merged per Change #10 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`
**Scope**: ~10-15 lines addition

- [ ] Before implementation begins, task-unified MUST record a test baseline: list of all test files and test function names that exist at task start
- [ ] On failure, classify each failing test as "pre-existing" (in baseline) or "new" (not in baseline)
- [ ] This classification drives the MUST-escalate vs MAY-fix-directly decision
- [ ] Baseline can be captured via `pytest --collect-only -q` or equivalent

### Task 1.4: Add Phase 1 circuit-breaker behavior
<!-- Source: Base (original, modified) — A S10 + B S8 Phase 1 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`
**Scope**: ~15-20 lines addition

When TFEP triggers in Phase 1 (before forensic quick mode exists):
- [ ] Stop testing immediately
- [ ] Freeze implementation (no further code changes)
- [ ] Report to user: what failed, why TFEP was triggered, which threshold rule matched
- [ ] Instruct user: "Run `/sc:forensic --depth quick --mode triage` manually, or use `--no-escalation` to bypass"
- [ ] Do NOT proceed with implementation until user responds

### Task 1.5: Add `--no-escalation` escape hatch to task-unified
<!-- Source: Variant B, Section 3.4 -->

**File**: `src/superclaude/commands/task-unified.md`
**Scope**: ~5-10 lines addition

- [ ] Add `--no-escalation` flag documentation
- [ ] Flag bypasses TFEP triggers and allows agent to proceed with standard behavior
- [ ] Add warning in boundaries: "Using --no-escalation voids TFEP protection"

### Task 1.6: Sync and verify
- [ ] Run `make sync-dev` to propagate changes to `.claude/`
- [ ] Run `make verify-sync` to confirm src/ and .claude/ match
- [ ] Run existing test suite to confirm no regressions

---

## Phase 2: Forensic Spec Refactoring

**Goal**: Add quick/triage mode to forensic spec. Prerequisite: Phase 1 complete.

### Task 2.1: Redesign forensic CLI flag model
<!-- Source: Base (original) — A S11, S12.A -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

- [ ] Replace `--mode debug|qa|regression|auto` with `--intent debug|qa|regression|auto|triage`
- [ ] Add new `--tier light|standard|deep` flag (forensic operating tier)
- [ ] Preserve existing `--depth quick|standard|deep` for adversarial debate depth only
- [ ] Add `--caller <command>` flag for caller-aware default selection
- [ ] Add `--context <file>` flag for caller-provided failure context (YAML)
- [ ] Document flag interaction rules and default cascades
- [ ] Update Section 5 (Command Definition) flag table

### Task 2.2: Define quick mode phase behavior
<!-- Source: Variant B, Section 3.1 — merged per Change #1 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

Add per-phase quick mode behavior to Section 7 (Phase Specifications):

| Phase | Quick Mode | Token Estimate |
|-------|-----------|---------------|
| Phase 0 (Recon) | SKIP — caller provides context via `--context` | 0 |
| Phase 1 (RCA) | 2 agents (fixed), Sonnet, `/sc:troubleshoot` prompts | ~1-2K |
| Phase 2 (Debate-H) | `/sc:adversarial --depth quick` | ~1-2K |
| Phase 3 (Fix) | 2 agents (fixed), `/sc:brainstorm` prompts | ~1-2K |
| Phase 3b (Debate-F) | `/sc:adversarial --depth quick` | ~1K |
| Phase 4 (Implement) | SKIP — returns fix plan to caller | 0 |
| Phase 5 (Validate) | SKIP — caller handles retesting | 0 |
| Phase 6 (Report) | Abbreviated `tfep-report.md` | ~0.5K |

**Total quick mode**: ~5-8K tokens, 4 agents + 2 adversarial rounds = 6 invocations

- [ ] Add "Quick Mode Behavior" subsection to each phase spec
- [ ] Add quick mode column to any phase behavior matrices
- [ ] Specify that Phase 1 agents MUST use `/sc:troubleshoot` prompt prefix
- [ ] Specify that Phase 3 agents MUST use `/sc:brainstorm` prompt prefix
- [ ] Document that quick mode is diagnosis/planning only — no code implementation

### Task 2.3: Define caller-provided context interface
<!-- Source: Variant B, Section 3.3 — merged per Change #5 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

Add to Section 9 (Data Schemas):

```yaml
failure_context:
  test_names: ["test_no_model_when_empty", "test_routing_with_agents"]
  test_files: ["tests/roadmap/test_cli_contract.py"]
  error_output: |
    E   KeyError: None
    tests/roadmap/test_cli_contract.py:85: in test_no_model_when_empty
  expected_behavior: "Tests should pass"
  actual_behavior: "10 tests fail with KeyError: None"
  changes_made:
    - file: "src/superclaude/cli/roadmap/models.py"
      description: "Changed RoadmapConfig defaults"
  task_description: "Add resume/restore capability to roadmap CLI"
  test_baseline: ["list of pre-existing test names from baseline snapshot"]
  escalation_count: 1  # 1st, 2nd, or 3rd TFEP trigger
```

- [ ] Define `failure_context` schema with required and optional fields
- [ ] Add example with realistic values
- [ ] Specify that `--context <file>` reads this YAML from the given path
- [ ] Define validation rules for the context package

### Task 2.4: Define artifact directory structure for quick mode
<!-- Source: Variant B, Section 3.5 — merged per Change #8 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

Add to Section 12 (Checkpoint and Resume):

```
{output_dir}/
  context.md                     # Caller-provided failure context
  phase-1/
    rca-alpha.md                 # Troubleshoot agent A findings
    rca-bravo.md                 # Troubleshoot agent B findings
  phase-2/
    adversarial/                 # Standard adversarial output
      debate-transcript.md
      base-selection.md
  rca-verdict.md                 # Synthesized root cause verdict
  phase-3/
    solution-alpha.md            # Brainstorm agent A proposal
    solution-bravo.md            # Brainstorm agent B proposal
  phase-3b/
    adversarial/                 # Standard adversarial output
      debate-transcript.md
      base-selection.md
  solution-verdict.md            # Synthesized solution verdict
  tfep-report.md                 # Abbreviated final report
  progress.json                  # Checkpoint (reuses existing schema)
```

- [ ] Define directory structure for quick mode
- [ ] Ensure checkpoint schema is compatible with existing forensic resume protocol
- [ ] Document that all artifacts MUST be committed to git

### Task 2.5: Define artifact-to-tasklist insertion format
<!-- Source: Invariant probe INV-004 — merged per Change #11 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

- [ ] Specify exact markdown format for tasklist-compatible remediation entries
- [ ] Format must be parseable by `sc:task-unified` as new task items
- [ ] Include: task description, files to modify, expected outcome, test criteria
- [ ] Document insertion point: before existing test/verification tasks in tasklist
- [ ] Add example of a complete insertion-ready remediation block

### Task 2.6: Define forensic return contract
<!-- Source: Base (original) — A S9 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

Add to Section 15 (Cross-References) or new Section 18:

```yaml
return_contract:
  status: "success|partial|failed"
  root_cause_path: "path/to/rca-verdict.md"
  solution_plan_path: "path/to/solution-verdict.md"
  recommended_resume_mode: "strict"
  recommended_escalation: "none|standard|deep"
  tasklist_insertion_path: "path/to/insertion-block.md"
  requires_user_review: false
  test_is_wrong: false  # true if adversarial concluded test expectations are outdated
  artifacts_dir: "path/to/output_dir/"
```

- [ ] Define return contract schema
- [ ] Ensure compatibility with task-unified's consumption pattern
- [ ] Include `test_is_wrong` field per Change #7
- [ ] Document all field types and valid values

### Task 2.7: Update forensic spec requirements
<!-- Source: Variant B, Section 6 — merged per Change #6 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

- [ ] Section 3 (Requirements): Expand FR-038 description to clarify `--depth` controls adversarial depth only
- [ ] Section 3: Add new FR for `--tier light|standard|deep`
- [ ] Section 3: Add new FR for `--intent triage`
- [ ] Section 3: Add new FR for `--context <file>`
- [ ] Section 3: Add new FR for `--caller <command>`
- [ ] Section 10 (Model Tier Matrix): Add quick mode column — Sonnet for all 4 agents
- [ ] Section 13 (Output Templates): Add abbreviated `tfep-report.md` template
- [ ] Section 16 (Quality Attributes): Add quick mode token budget (~5-8K)

### Task 2.8: Add escalation gradient to forensic spec
<!-- Source: Base (original) + Variant B — A S10 + B S4 -->

**File**: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

```
1st TFEP trigger  -> /sc:forensic --tier light --intent triage   (~5-8K tokens)
2nd TFEP trigger  -> /sc:forensic --tier standard                (~15-20K tokens)
3rd TFEP trigger  -> FULL STOP. Report to user. Do not attempt further.
```

- [ ] Document escalation gradient with token estimates
- [ ] Define what constitutes "same failure" vs "new failure" for escalation counting
- [ ] Specify that forensic's return contract includes `recommended_escalation` for next attempt

---

## Phase 3: Full Integration (After Forensic Quick Mode Ships)

**Goal**: Wire task-unified to automatically invoke forensic. Prerequisite: Phase 2 complete.

### Task 3.1: Update task-unified to auto-invoke forensic
<!-- Source: Base (original) — A S10 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

Replace Phase 1 manual fallback with automatic invocation:
- [ ] On TFEP trigger, invoke `/sc:forensic --tier light --intent triage --caller task-unified --context <context-file>`
- [ ] Construct failure_context YAML from current task state and test results
- [ ] Include test baseline in context package
- [ ] Consume forensic return contract
- [ ] If `test_is_wrong == true`: present to user for review, do not auto-fix test
- [ ] If `status == "success"`: insert remediation plan into tasklist, resume `--compliance strict`
- [ ] If `status == "partial"` or `recommended_escalation != "none"`: escalate per gradient
- [ ] If `status == "failed"`: report to user, halt

### Task 3.2: Add tasklist insertion logic
<!-- Source: Base (original) + INV-004 resolution -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

- [ ] Parse forensic's `tasklist_insertion_path` artifact
- [ ] Insert remediation tasks before existing test/verification tasks
- [ ] Add `## Failure Remediation Plan (Adjudicated)` heading
- [ ] Preserve original tasklist structure — append, don't replace

### Task 3.3: Add TFEP incident reporting
<!-- Source: Variant B, Section 3.4 -->

**File**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

- [ ] After each TFEP resolution (success or escalation), produce `tfep-incident-report.md`
- [ ] Include: trigger reason, escalation count, root cause verdict, solution verdict, outcome
- [ ] Commit report to git alongside other artifacts

### Task 3.4: Sync, verify, and test
- [ ] Run `make sync-dev` to propagate all changes
- [ ] Run `make verify-sync`
- [ ] Write integration test: simulate test failure → verify TFEP triggers → verify artifacts produced
- [ ] Write unit test: verify escalation threshold classification logic
- [ ] Run full test suite

---

## Cross-References

| Document | Path | Relevance |
|----------|------|-----------|
| Forensic spec (primary target) | `.dev/releases/backlog/v5.xxforensic/forensic-spec.md` | Phase 2 refactoring target |
| Task-unified protocol (secondary target) | `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Phase 1 + Phase 3 changes |
| Task-unified command | `src/superclaude/commands/task-unified.md` | Task 1.5 (--no-escalation flag) |
| Troubleshoot command | `src/superclaude/commands/troubleshoot.md` | Dependency: RCA agents use this |
| Brainstorm command | `src/superclaude/commands/brainstorm.md` | Dependency: solution agents use this |
| Adversarial protocol | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | Dependency: invoked for RCA + solution debates |
| Forensic exploration | `.dev/releases/backlog/v5.xxforensic/forensic-explore.md` | Background context |
