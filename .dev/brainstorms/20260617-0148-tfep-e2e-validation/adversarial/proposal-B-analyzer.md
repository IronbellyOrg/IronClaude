# Proposal B — Deterministic TFEP Troubleshoot Migration E2E Validation

## Distinctive stance

This proposal treats the migration as a docs/protocol contract, not as a conventional test suite. A PASS must be earned by byte-level or count-level probes wherever possible, and any remaining prose judgment must be anchored to exact line tokens that two independent readers must classify the same way.

The suite requires strict 12/12 green: 4 tests × 3 independent runs. A majority rule is explicitly rejected because the suite is validating migration determinism; if one run disagrees with two others, the migration validation is flaky and the overall verdict is FAIL even if the average looks good.

## Global execution and aggregation protocol

### Run layout

Each delegated run writes to an isolated path:

`/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/<test_id>/run-<1|2|3>/`

Each run must create exactly two primary artifacts:

- `verdict.yaml` — machine-readable verdict and normalized observations.
- `evidence.md` — human-readable paper trail with exact commands, exit codes, stdout/stderr excerpts, and anchored findings.

The final aggregator reads only those 12 `verdict.yaml` files and emits:

`/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/aggregate-verdict.yaml`

### Strict reproducibility rule

For each test, the 3 run verdicts must satisfy both:

1. `status: PASS` in all 3 runs.
2. Identical normalized observation digest across all 3 runs after removing only these volatile fields: `run_id`, `started_at_utc`, `ended_at_utc`, `artifact_dir`, `agent_name`, and raw `duration_ms`.

If any normalized digest differs, the test status is `DISAGREE`, and the suite status is `FAIL`, even if all three run-level statuses are `PASS`.

### Suite aggregation rule

`migration_validated: true` iff all 12 run artifacts are present, all 12 have `status: PASS`, and all 4 tests have 3/3 identical normalized observation digests.

Any missing artifact, non-PASS run, malformed schema, or cross-run disagreement yields `migration_validated: false` with `suite_failure_class` set to one of:

- `missing_artifact`
- `schema_invalid`
- `run_failed`
- `cross_run_disagreement`

### Common evidence-artifact schema

Every `verdict.yaml` uses this schema:

```yaml
test_id: <E2E-B1|E2E-B2|E2E-B3|E2E-B4>
test_name: <string>
run_id: <1|2|3>
status: <PASS|FAIL>
started_at_utc: <ISO-8601>
ended_at_utc: <ISO-8601>
artifact_dir: <absolute path>
repo_root: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
source_files:
  - <absolute path>
commands:
  - id: <stable command id>
    command: <exact command string>
    exit_code: <integer>
    stdout_sha256: <hex>
    stderr_sha256: <hex>
    stdout_excerpt_path: <absolute path under artifact_dir>
    stderr_excerpt_path: <absolute path under artifact_dir>
criteria:
  - id: <stable criterion id>
    class: <DETERMINISTIC|JUDGMENT>
    expected: <string>
    observed: <string>
    status: <PASS|FAIL>
    evidence_ref: <command id or file:line anchor>
normalized_observations:
  <stable keys only; no timestamps, no unordered lists>
normalized_observation_digest: <sha256 of canonicalized normalized_observations>
```

Canonicalization rule for `normalized_observation_digest`: sort mapping keys lexicographically, sort unordered lists lexicographically, preserve ordered lists only where order is part of the acceptance criterion, render booleans as lowercase YAML booleans, and omit volatile fields listed above.

### Non-determinism controls

- Timestamps: allowed only in metadata, excluded from normalized digest.
- `rg` ordering: every `rg` command uses `LC_ALL=C` and `--sort path`; acceptance criteria use counts, exact strings, or ordered line-number comparisons, not incidental terminal order.
- LLM judgment: minimized; where unavoidable, the criterion names the exact file:line anchor and exact token(s) to classify.
- Path drift: all prompts and schemas pin the absolute worktree root `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`.
- Shared mutable state: each run writes only to its per-run evidence directory and does not read sibling run outputs.
- Git state noise: read-only commands only; no `git add`, no file edits to migrated files, no generated source changes.
- `make verify-sync` output variance: acceptance is exit code plus stable required/forbidden substrings, not full stdout byte equality.
- Agent prose variation: the PASS/FAIL decision is made from criterion records in `verdict.yaml`; `evidence.md` prose is audit context only.
- Shell locale and environment: use `LC_ALL=C` on grep/ripgrep probes and record command strings verbatim.

---

## E2E-B1 — Residual Backend Cleanliness + Sync Parity

### Outcome dimension

Backend swap is complete and clean.

### Scope

Read-only validation of residual obsolete backend tokens and source/dev-copy parity across:

- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/commands/task.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.claude/`

This test intentionally scopes the bare `forensic` residual sweep to the two task-protocol surfaces because unrelated skills may use generic forensic vocabulary out of migration scope.

### Embedded delegable subagent prompt

```text
You are running E2E-B1 Residual Backend Cleanliness + Sync Parity for the TFEP forensic-to-troubleshoot migration. Work read-only in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend. Create /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2E-B1/run-<RUN_ID>/, where <RUN_ID> is the run number you were assigned. Run the ordered probes exactly as specified in Proposal B, capture stdout/stderr and exit codes, and write verdict.yaml plus evidence.md. PASS only if every listed binary criterion passes. Do not edit files, do not stage files, and do not read sibling run directories.
```

### Ordered probe steps

1. Residual task-surface sweep:
   - Command ID `B1-C1`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict' src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md`
2. Repo-wide obsolete slash-command sweep:
   - Command ID `B1-C2`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '/sc:forensic' src/`
3. Sync parity:
   - Command ID `B1-C3`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && make verify-sync`
4. `.claude` staged-change guard:
   - Command ID `B1-C4`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C git status --porcelain=v1 -- .claude`

### Binary acceptance criteria

| ID | Class | PASS iff |
|---|---|---|
| B1-AC1 | DETERMINISTIC | `B1-C1` exits `1` and stdout is empty, proving zero matches for obsolete task-surface tokens. |
| B1-AC2 | DETERMINISTIC | `B1-C2` exits `1` and stdout is empty, proving zero live `/sc:forensic` command invocations under `src/`. |
| B1-AC3 | DETERMINISTIC | `B1-C3` exits `0`, stdout contains `All components in sync`, and stdout contains neither `DIFFERS` nor `MISSING`. |
| B1-AC4 | DETERMINISTIC | `B1-C4` emits no line whose status column is not `??`; untracked `.claude/` dev-copy noise is ignored, but staged/modified tracked `.claude` changes fail. |

Judgment fraction: 0/4 criteria.

### Evidence-artifact schema additions

`normalized_observations` must include:

```yaml
residual_task_surface_match_count: 0
src_sc_forensic_match_count: 0
verify_sync_exit_code: 0
verify_sync_contains_all_components_in_sync: true
verify_sync_forbidden_tokens_present: false
claude_tracked_change_count: 0
```

Cross-run identity is expected because all values are counts/booleans and `verify-sync` is reduced to stable predicates.

---

## E2E-B2 — TFEP Adapter Wire Contract Identity

### Outcome dimension

Adapter contract integrity across consumer, producer, and report-rendered echo.

### Scope

Read-only validation of the 7-field TFEP wire set across:

- Consumer: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 Step 4/5.
- Producer: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Output Contract and Wave 5 step 4.5.
- Report echo: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` `## TFEP Consumer` block.

Canonical 7-field wire set, in order:

1. `status`
2. `test_is_wrong`
3. `recommended_escalation`
4. `tasklist_insertion_path`
5. `remediation_target`
6. `root_cause_summary`
7. `solution_summary`

### Embedded delegable subagent prompt

```text
You are running E2E-B2 TFEP Adapter Wire Contract Identity. Work read-only in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend. Create /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2E-B2/run-<RUN_ID>/. Validate the exact 7-field TFEP wire set across the task-protocol consumer, troubleshoot Output Contract producer, Wave 5 return-contract emission, and report-template TFEP Consumer echo. Use exact field tokens and enum strings, not paraphrase. Write verdict.yaml and evidence.md. PASS only if every criterion passes. Do not edit files, do not stage files, and do not read sibling run directories.
```

### Ordered probe steps

1. Consumer field anchor:
   - Command ID `B2-C1`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Output Contract fields `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`' src/superclaude/skills/sc-task-protocol/SKILL.md`
2. Consumer composition anchor:
   - Command ID `B2-C2`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Compose the plan body from the adapter fields `remediation_target`, `root_cause_summary`, and `solution_summary`' src/superclaude/skills/sc-task-protocol/SKILL.md`
3. Producer TFEP adapter row count:
   - Command ID `B2-C3`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -c 'TFEP adapter field \(contract v1\.1\.0\+\)' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
4. Producer contract version anchor:
   - Command ID `B2-C4`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Output-contract semver, default `1\.1\.0`' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
5. Producer enum anchors:
   - Command ID `B2-C5`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'enum `none\|retry\|escalate_depth\|halt`|enum `test\|code\|docs\|none`' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
6. Wave 5 emission anchor:
   - Command ID `B2-C6`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'write `<output-dir>/return-contract\.yaml` mapping the Output Contract fields to the TFEP-consumed schema: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
7. Report-template field echo anchors:
   - Command ID `B2-C7`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '^status: <success\|partial\|failed>$|^test_is_wrong: <bool>$|^recommended_escalation: <none\|retry\|escalate_depth\|halt>$|^tasklist_insertion_path: <abs-path\|null>$|^remediation_target: <test\|code\|docs\|none>$|^root_cause_summary: <text>$|^solution_summary: <text>$' src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`

### Binary acceptance criteria

| ID | Class | PASS iff |
|---|---|---|
| B2-AC1 | DETERMINISTIC | `B2-C1` exits `0` and returns exactly one line containing the canonical 7-field wire set in order. |
| B2-AC2 | DETERMINISTIC | `B2-C2` exits `0` and returns exactly one line proving the tasklist composition consumes `remediation_target`, `root_cause_summary`, and `solution_summary`. |
| B2-AC3 | DETERMINISTIC | `B2-C3` exits `0` and stdout is exactly `5`, proving the five newly additive TFEP adapter rows exist in the producer. |
| B2-AC4 | DETERMINISTIC | `B2-C4` exits `0` and returns exactly one line containing default `1.1.0`. |
| B2-AC5 | DETERMINISTIC | `B2-C5` exits `0` and returns exactly two lines: one `recommended_escalation` enum line and one `remediation_target` enum line. |
| B2-AC6 | DETERMINISTIC | `B2-C6` exits `0` and returns exactly one line containing the canonical 7-field write set in order. |
| B2-AC7 | DETERMINISTIC | `B2-C7` exits `0` and returns exactly seven lines whose field names equal the canonical wire set after sorting by the canonical order above; enum tokens byte-match `none|retry|escalate_depth|halt` and `test|code|docs|none`. |

Judgment fraction: 0/7 criteria.

### Evidence-artifact schema additions

`normalized_observations` must include:

```yaml
canonical_wire_set:
  - status
  - test_is_wrong
  - recommended_escalation
  - tasklist_insertion_path
  - remediation_target
  - root_cause_summary
  - solution_summary
consumer_wire_set_present: true
consumer_composition_fields_present: true
producer_tfep_adapter_row_count: 5
contract_version_default: 1.1.0
recommended_escalation_enum: none|retry|escalate_depth|halt
remediation_target_enum: test|code|docs|none
wave5_emission_wire_set_present: true
report_template_wire_set_count: 7
```

Cross-run identity is expected because criteria are exact counts and exact token sets.

---

## E2E-B3 — End-to-End Protocol Chain Resolution

### Outcome dimension

The TFEP protocol chain resolves from trigger through freeze, context creation, troubleshoot dispatch, caller/context ingestion, return-contract emission, deterministic Step 4 branching, tasklist insertion, and resume.

### Scope

Read-only validation of the behavioral chain across:

- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/commands/troubleshoot.md`

### Embedded delegable subagent prompt

```text
You are running E2E-B3 End-to-End Protocol Chain Resolution. Work read-only in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend. Create /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2E-B3/run-<RUN_ID>/. Validate the protocol chain by exact command probes and line-order anchors. You may read the relevant files, but any prose judgment must cite exact file:line anchors and exact tokens. Write verdict.yaml and evidence.md. PASS only if every criterion passes. Do not edit files, do not stage files, and do not read sibling run directories.
```

### Ordered probe steps

1. Diagnostic backend declaration count:
   - Command ID `B3-C1`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '^\*\*Diagnostic backend:\*\* `troubleshoot`' src/superclaude/skills/sc-task-protocol/SKILL.md`
2. Step headings in task-protocol:
   - Command ID `B3-C2`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '^\*\*Step [1-6]:' src/superclaude/skills/sc-task-protocol/SKILL.md`
3. Context path construction and dispatch:
   - Command ID `B3-C3`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Write context to `\{output_dir\}/context\.yaml`|/sc:troubleshoot --caller task-unified --context \{context_path\} --output-dir \{output_dir\} --depth \{depth\}|Pass NO `--fix`' src/superclaude/skills/sc-task-protocol/SKILL.md`
4. Depth mapping and stop cap:
   - Command ID `B3-C4`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '1st TFEP trigger.*--depth standard|2nd TFEP trigger.*--depth deep|systemic failure OR ≥3 new failing tests.*--depth deep|3rd TFEP trigger.*FULL STOP' src/superclaude/skills/sc-task-protocol/SKILL.md`
5. Troubleshoot command advertises `--context` and `--caller`:
   - Command ID `B3-C5`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '`--context`|`--caller`|return-contract\.yaml' src/superclaude/commands/troubleshoot.md`
6. Troubleshoot Wave 0 ingests caller/context and conditions return-contract emission:
   - Command ID `B3-C6`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Optional: `--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`, `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`, `--context`, `--caller`|When `caller=task-unified`, mark Wave 5 to emit `return-contract\.yaml`' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
7. Troubleshoot Wave 5 emits return-contract and returns path:
   - Command ID `B3-C7`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Emit TFEP return-contract|write `<output-dir>/return-contract\.yaml`|return_contract_path|When `caller=task-unified`, `return-contract\.yaml` is written and its path returned' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
8. Step 4 deterministic branch ladder anchors:
   - Command ID `B3-C8`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'first match wins|If `test_is_wrong == true`|If `remediation_target == "docs"`|If `status == "success"`|If `recommended_escalation == "none"`|If `recommended_escalation == "retry"`|If `recommended_escalation == "escalate_depth"`|If `recommended_escalation == "halt" \(or `status == "failed"`\)' src/superclaude/skills/sc-task-protocol/SKILL.md`
9. Step 5/6 insertion and resume anchors:
   - Command ID `B3-C9`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Failure Remediation Plan \(Adjudicated\)|Insert remediation tasks BEFORE existing test/verification tasks|Resume execution with `--compliance strict`|After remediation tasks complete, re-run the original test suite' src/superclaude/skills/sc-task-protocol/SKILL.md`

### Binary acceptance criteria

| ID | Class | PASS iff |
|---|---|---|
| B3-AC1 | DETERMINISTIC | `B3-C1` returns exactly one declaration line. |
| B3-AC2 | DETERMINISTIC | `B3-C2` returns exactly six lines with step numbers `1,2,3,4,5,6` in strictly increasing line-number order. |
| B3-AC3 | DETERMINISTIC | `B3-C3` returns exactly three anchors: context write, dispatch string, and `Pass NO --fix`; dispatch string contains `/sc:troubleshoot`, `--caller task-unified`, `--context {context_path}`, `--output-dir {output_dir}`, and `--depth {depth}`. |
| B3-AC4 | DETERMINISTIC | `B3-C4` returns anchors for standard first trigger, deep second trigger, deep systemic/≥3-new trigger, and third-trigger FULL STOP. |
| B3-AC5 | DETERMINISTIC | `B3-C5` returns command-surface anchors for both `--context` and `--caller`, plus the on-return surface of `return-contract.yaml`. |
| B3-AC6 | DETERMINISTIC | `B3-C6` returns anchors proving Wave 0 parses `--context`/`--caller` and marks Wave 5 to emit `return-contract.yaml` when `caller=task-unified`. |
| B3-AC7 | DETERMINISTIC | `B3-C7` returns anchors proving Wave 5 writes `<output-dir>/return-contract.yaml`, records `return_contract_path`, and returns the path for `caller=task-unified`. |
| B3-AC8 | DETERMINISTIC | `B3-C8` returns exactly eight ladder anchors in this order: first-match-wins note, `test_is_wrong`, `remediation_target == "docs"`, `status == "success"`, `recommended_escalation == "none"`, `retry`, `escalate_depth`, `halt/status failed`. |
| B3-AC9 | DETERMINISTIC | `B3-C9` returns all four insertion/resume anchors: adjudicated heading, insert-before-test/verification rule, `--compliance strict` resume, and original test-suite rerun. |
| B3-AC10 | JUDGMENT ANCHORED | The agent states one bounded conclusion: the anchored chain is continuous because every consumer output required by an earlier step has a later producer/ingester anchor. This judgment must cite only `B3-C3`, `B3-C6`, `B3-C7`, and `B3-C8`; no unstated protocol inference is allowed. |

Judgment fraction: 1/10 criteria. The only judgment is anchored to exact command IDs and exact line tokens; if any anchor is absent, the deterministic criteria already fail.

### Evidence-artifact schema additions

`normalized_observations` must include:

```yaml
backend_declaration_count: 1
step_numbers_in_order: [1, 2, 3, 4, 5, 6]
dispatch_has_troubleshoot: true
dispatch_has_caller_task_unified: true
dispatch_has_context_path: true
dispatch_has_output_dir: true
dispatch_has_depth_placeholder: true
dispatch_has_no_fix_prohibition: true
depth_mapping_complete: true
command_surface_context_and_caller: true
wave0_context_and_caller_ingestion: true
wave5_return_contract_emission: true
branch_ladder_order:
  - first_match_wins
  - test_is_wrong
  - remediation_target_docs
  - status_success
  - recommended_escalation_none
  - recommended_escalation_retry
  - recommended_escalation_escalate_depth
  - recommended_escalation_halt_or_status_failed
insertion_resume_complete: true
anchored_chain_judgment: true
```

Cross-run identity is expected because the line anchors, counts, and canonical ordered lists are stable.

---

## E2E-B4 — Safety Invariants + Remediation Ownership

### Outcome dimension

Safety invariants are preserved: freeze semantics, diagnosis-only troubleshoot invocation, asymmetric-cost gates, backend-neutral swap boundary, and incident reporting rebound to troubleshoot artifacts.

### Scope

Read-only validation across:

- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`

### Embedded delegable subagent prompt

```text
You are running E2E-B4 Safety Invariants + Remediation Ownership. Work read-only in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend. Create /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2E-B4/run-<RUN_ID>/. Validate freeze preservation, diagnosis-only dispatch with no --fix, asymmetric-cost human-review gates, backend-neutral swap boundary, and incident reporting rebound to troubleshoot artifacts. Use exact line/token anchors and write verdict.yaml plus evidence.md. PASS only if every criterion passes. Do not edit files, do not stage files, and do not read sibling run directories.
```

### Ordered probe steps

1. Freeze block current anchors:
   - Command ID `B4-C1`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '^\*\*Step 1: Halt and freeze\*\*$|^1\. \*\*STOP\*\* testing immediately\.$|^2\. \*\*FREEZE\*\* implementation — no further code changes permitted\.$' src/superclaude/skills/sc-task-protocol/SKILL.md`
2. Freeze baseline anchors:
   - Command ID `B4-C2`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '^\*\*Step 1: Halt and freeze\*\*$|^1\. \*\*STOP\*\* testing immediately\.$|^2\. \*\*FREEZE\*\* implementation — no further code changes permitted\.$' .dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`
3. Diagnosis-only dispatch and remediation ownership:
   - Command ID `B4-C3`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Pass NO `--fix`|TFEP invokes troubleshoot for DIAGNOSIS ONLY|task-protocol owns this insertion and the Step 6 resume|NO --fix' src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
4. §4.5 dispatch line containing forbidden `--fix` check:
   - Command ID `B4-C4`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path '/sc:troubleshoot --caller task-unified --context \{context_path\} --output-dir \{output_dir\} --depth \{depth\}.*--fix' src/superclaude/skills/sc-task-protocol/SKILL.md`
5. Asymmetric-cost gates in task-protocol consumer:
   - Command ID `B4-C5`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'asymmetric-cost gates \(`test_is_wrong`, `remediation_target == "docs"`\) are checked first|If `test_is_wrong == true`: Present to user for review\. Do NOT auto-fix tests\.|If `remediation_target == "docs"`: present to user for spec/stakeholder review\. Do NOT auto-insert a code remediation\.' src/superclaude/skills/sc-task-protocol/SKILL.md`
6. Asymmetric-cost rendering rules in troubleshoot report template:
   - Command ID `B4-C6`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'When `test_is_wrong=true`|The asymmetric cost of this flag is the entire reason it exists|When `Behavior is documented: true`|a code change would regress the documented contract|Files that MUST NOT change' src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
7. Backend-neutral swap boundary:
   - Command ID `B4-C7`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string|Diagnostic backend declaration' src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
8. Incident reporting rebound to troubleshoot artifacts:
   - Command ID `B4-C8`
   - `cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && LC_ALL=C rg -n --sort path 'Diagnostic artifacts.*troubleshoot `report_path` \(REPORT\.md\), `audit_log_path` \(audit\.log\)' src/superclaude/skills/sc-task-protocol/SKILL.md`

### Binary acceptance criteria

| ID | Class | PASS iff |
|---|---|---|
| B4-AC1 | DETERMINISTIC | `B4-C1` returns exactly three current freeze-block lines: heading, STOP line, FREEZE line. |
| B4-AC2 | DETERMINISTIC | `B4-C2` returns exactly three baseline freeze-block lines with the same three line texts as `B4-C1` after removing file path and line number prefixes. |
| B4-AC3 | DETERMINISTIC | `B4-C3` returns anchors for `Pass NO --fix`, `DIAGNOSIS ONLY`, and task-protocol-owned insertion/resume. |
| B4-AC4 | DETERMINISTIC | `B4-C4` exits `1` and stdout is empty, proving the exact Step 3 dispatch line does not include `--fix`. |
| B4-AC5 | DETERMINISTIC | `B4-C5` returns exactly three task-protocol asymmetric gate anchors, including both human-review/do-not-auto statements. |
| B4-AC6 | DETERMINISTIC | `B4-C6` returns at least five report-template safety anchors: `test_is_wrong=true`, asymmetric-cost rationale, `Behavior is documented: true`, documented-contract regression warning, and `Files that MUST NOT change`. |
| B4-AC7 | JUDGMENT ANCHORED | The agent states that the backend-neutral swap boundary is explicitly declared, citing the exact token `swapping the backend changes only this declaration and the invocation string`. This is a bounded classification of one quoted line, not an architectural inference. |
| B4-AC8 | DETERMINISTIC | `B4-C8` returns exactly one incident-report line sourcing diagnostic artifacts from troubleshoot `REPORT.md` and `audit.log`. |

Judgment fraction: 1/8 criteria. The only judgment is anchored to a quoted backend-neutrality token.

### Evidence-artifact schema additions

`normalized_observations` must include:

```yaml
freeze_current_lines:
  - "**Step 1: Halt and freeze**"
  - "1. **STOP** testing immediately."
  - "2. **FREEZE** implementation — no further code changes permitted."
freeze_baseline_lines_match_current: true
dispatch_no_fix_exact_line_has_forbidden_fix: false
diagnosis_only_anchor_present: true
remediation_ownership_task_protocol: true
asymmetric_task_protocol_gate_count: 3
report_template_safety_anchor_min_count_met: true
backend_neutral_boundary_anchored: true
incident_artifacts_rebound_to_troubleshoot: true
```

Cross-run identity is expected because the test compares exact line texts, exact absence of forbidden tokens, and fixed anchor booleans.

---

## Aggregator specification

### Embedded delegable aggregator prompt

```text
You are aggregating Proposal B TFEP migration e2e evidence. Work read-only in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend. Read the 12 verdict.yaml files under /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2E-B{1,2,3,4}/run-{1,2,3}/. Do not re-run tests and do not average results. Validate schema, remove only approved volatile fields from each normalized digest comparison, require all 12 PASS, and require 3/3 identical normalized observation digests per test. Write aggregate-verdict.yaml and aggregate-report.md. migration_validated is true only under strict 12/12-green and no cross-run disagreement.
```

### Aggregator output schema

```yaml
suite: tfep-troubleshoot-migration-e2e
policy: strict_12_of_12_green_no_disagreement
migration_validated: <true|false>
suite_failure_class: <none|missing_artifact|schema_invalid|run_failed|cross_run_disagreement>
tests:
  E2E-B1:
    runs_present: 3
    pass_count: <0-3>
    normalized_digests: [<hex>, <hex>, <hex>]
    cross_run_agreement: <true|false>
    status: <PASS|FAIL|DISAGREE>
  E2E-B2:
    runs_present: 3
    pass_count: <0-3>
    normalized_digests: [<hex>, <hex>, <hex>]
    cross_run_agreement: <true|false>
    status: <PASS|FAIL|DISAGREE>
  E2E-B3:
    runs_present: 3
    pass_count: <0-3>
    normalized_digests: [<hex>, <hex>, <hex>]
    cross_run_agreement: <true|false>
    status: <PASS|FAIL|DISAGREE>
  E2E-B4:
    runs_present: 3
    pass_count: <0-3>
    normalized_digests: [<hex>, <hex>, <hex>]
    cross_run_agreement: <true|false>
    status: <PASS|FAIL|DISAGREE>
```

### Why strict 12/12 beats majority

The suite's purpose is not to estimate probabilistic confidence; it is to prove that a prose/protocol migration can be validated reproducibly by independent agents. Majority voting would hide exactly the class of defect this proposal is designed to expose: a verdict whose inputs or criteria are loose enough that one run reaches a different result. Any 2/3 split means at least one of the migration, the test design, or the evidence extraction is non-deterministic; the correct migration verdict is therefore not validated.

## Summary of non-determinism eliminated

1. Naive full-output diffs fail on timestamps and command durations; this design digests only normalized observations.
2. Naive `rg` probes can rely on incidental output order; this design uses `LC_ALL=C`, `--sort path`, counts, and canonical lists.
3. Naive LLM protocol-trace tests can become opinion polls; this design reduces judgment to 2 bounded criteria across 29 total criteria, each tied to quoted tokens.
4. Naive artifact paths can drift by current working directory; this design pins every path to the absolute worktree root.
5. Naive evidence reports can pass despite partial artifacts; this design treats missing schema fields, missing run files, and cross-run disagreement as hard suite failures.
6. Naive backend-cleanliness sweeps can fail on unrelated historical/generic vocabulary; this design scopes bare `forensic` checks to the two live task-protocol surfaces while still sweeping `/sc:forensic` across all `src/`.
