# Research: Integration Points
**Topic type:** Integration Points
**Scope:** sc-adversarial-protocol, task-builder, sc-troubleshoot-protocol, sc-task-protocol, sprint CLI executor, confidence-calibrator, evidence-validator, root-cause-analyst, self-review, requirements-analyst, audit-validator, socratic-mentor, rf-qa, rf-qa-qualitative
**Status:** Complete
**Date:** 2026-05-27
---

## Summary

This research extracts the exact invocation shapes reflect must emit (outbound) or accept (inbound) for every downstream/upstream integration boundary. The dominant findings:

1. **sc-adversarial-protocol** has a fully documented Skill-invocation surface + 11-field return contract; reflect's Wave 4 caller must use the literal `--compare` / `--source` / `--depth` / `--focus` / `--output` flag set and consume `merged_output_path` / `convergence_score` / `artifacts_dir` / `status`. The brainstorm protocol's F1-F3 fallback pattern at lines 280-294 IS the canonical template; reflect MUST mirror it (no synthetic-0.5 fallback for empty responses; partial-parse only when merged file exists on disk; F1=retry-quick, F2=abort, F3=write-failed-artifact-and-exit).
2. **task-builder** consumes a 15-field BUILD_REQUEST (per A.9 §785-985); the field set + ordering is M1-frozen. Reflect's remediation-handoff template must emit ALL 15 fields verbatim. EXECUTION_CONTEXT_REQUIREMENTS (API-001-M2) is optional but governed by AUTO/REQUIRED/SUPPRESS semantics.
3. **sc-troubleshoot-protocol** invokes reflect with the literal command surface `/sc:reflect --type task --analyze <task-file>` (Wave 6 Phase B, `SKILL.md:368`) and `/sc:reflect --type task --validate <task-file>` (Wave 6 Phase D, `SKILL.md:370`, `refs/remediation-handoff.md:101`). Reflect MUST accept these `--type` + `--analyze` / `--validate` flag combinations.
4. **sc-task-protocol** has NO reflect integration today — the integration surface is aspirational. The spec's §9.3 row "sc-task-protocol end-of-task hook" defines the inbound consumer-side contract reflect should support: reads `status`, `tier_reached`, `deviation_count_by_class`, `confidence_calibrated`, `needs_human_decision`.
5. **Sprint CLI executor (TurnLedger)** lives at `src/superclaude/cli/sprint/models.py:693`. The §9.3 row pins exact field paths reflect must emit: `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade`. `TurnLedger.available()` lives at `models.py:717`; `minimum_allocation=5` (`models.py:709`) is the value reflect's `--budget-remaining < 5` STOP rule pivots on.
6. **confidence-calibrator** has a fixed 5-input contract: `card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path` (`confidence-calibrator.md:41-45`). Reflect's Wave 1D / 3C invocations must spawn via `Task` with EXACTLY these names.
7. **evidence-validator** has a 4-input contract: `report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec` (`evidence-validator.md:41-44`). Reflect Wave 5 must pass `allow_command_reexec: false` per the v1 default.
8. Other agents (root-cause-analyst, self-review, requirements-analyst, audit-validator, socratic-mentor) follow a generic "spawn prompt with role+context" pattern with no strict input-schema; reflect's invocation strings are free-form for these.

---

## 1. sc-adversarial-protocol — Wave 4 Caller Surface

### File / Anchors
- **SKILL file:** `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
- **Frontmatter name:** `sc:adversarial-protocol` (`SKILL.md:2`)
- **Return contract section:** `SKILL.md:425-461` (MANDATORY, "must write on every invocation")
- **Error matrix:** `SKILL.md:394-423`

### Literal Skill-Invocation Shape (Mode A — `--compare`)

From the spec's command grammar (`SKILL.md:29-33`):

```
/sc:adversarial --compare file1.md,file2.md[,...,fileN.md] [options]
```

And the brainstorm caller's verbatim usage pattern (`sc-brainstorm-protocol/SKILL.md:264-278`):

```
Skill sc-adversarial-protocol with
   --compare <variant1>,<variant2>,...,<variantN>
   --depth <standard | quick | deep>
   --convergence <passthrough, default 0.75>
   --output <output>/adversarial/
   [--blind if flagged]
   [--interactive if flagged]
```

For reflect's Wave 4, the literal invocation reflect must emit is:

```
Skill sc-adversarial-protocol with
  --compare <card1>,<card2>[,<card3>...]
  --depth standard
  --focus correctness,coverage,deviation-classification
  --output <output>/adversarial/
```

### Available Flags (`SKILL.md:332-344`)

| Flag | Default | Range / Type |
|------|---------|--------------|
| `--depth` | `standard` | `quick` / `standard` / `deep` |
| `--convergence` | `0.80` | 0.50-0.99 |
| `--interactive` | `false` | flag |
| `--output` | auto-derived | path |
| `--focus` | All | comma-separated |
| `--pipeline` | none | inline / `@path.yaml` |
| `--pipeline-parallel` | 3 | 1-10 |
| `--pipeline-resume` | false | flag |
| `--pipeline-on-error` | `halt` | `halt` / `continue` |
| `--blind` | false | flag |
| `--auto-stop-plateau` | false | flag |

### Return Contract Fields (`SKILL.md:431-443`)

```yaml
merged_output_path: "<path to merged file>"       # null if merge not reached
convergence_score: 0.75                            # float 0.0-1.0, null if debate not reached
artifacts_dir: "<path to adversarial/ directory>"  # always set
status: "success" | "partial" | "failed"
base_variant: "opus:architect"                     # null if not reached
unresolved_conflicts: 2                            # integer
fallback_mode: false                               # bool
failure_stage: null                                # null | "variant_generation" | "debate" | "merge" | "validation" | "transport"
invocation_method: "skill-direct"                  # "skill-direct" | "task-agent" | "manual"
unaddressed_invariants: []                         # list of HIGH-severity items
```

**NOTE ON `artifacts_dir`:** The spec section §9.3 row referenced `adversarial_artifacts_dir` (i.e., the brainstorm telemetry field name), but the canonical return-contract field is literally `artifacts_dir` per `sc-adversarial-protocol/SKILL.md:435,453`. Reflect's caller code must read `artifacts_dir`, not `adversarial_artifacts_dir`. (The brainstorm contract's `adversarial_artifacts_dir` at `return-contract.yaml:8` is a wrapper/rename done by the brainstorm caller.)

### F1/F2/F3 Fallback Semantics (canonical pattern from `sc-brainstorm-protocol/SKILL.md:280-294`)

Reflect MUST mirror this exactly:

```
Empty-response guard: If response is empty or has no parseable structure -> FAIL Wave 4
  (no synthetic 0.5 fallback). Emit: "Adversarial returned empty response - invocation
  likely failed at transport. See sc:adversarial logs."

Partial-parse guard: If response is structured but `convergence_score` missing/unparseable
  -> use fallback `convergence: 0.5` ONLY IF `merged_output_path` is present AND file exists
  on disk. Otherwise FAIL.

Missing-file guard: Verify `merged_output_path` exists via Read. If not -> FAIL.
  This guard runs BEFORE 3-status routing.

3-status routing (only after all guards pass):
  - convergence_score >= 0.65 -> PASS
  - convergence_score >= 0.50 -> PARTIAL (with warning)
  - convergence_score <  0.50 -> FAIL

Fallback protocol (F1-F3):
  - F1 - Skill tool error -> retry once with `--depth quick` and reduced inputs. If retry succeeds, route to consumption.
  - F2 - Retry fails -> abort Wave 4. Emit error with adversarial logs path. Set `status: failed`. Skip downstream waves.
  - F3 - All variants fail mid-generation -> write `<output>/<skill>-failed.md` with partial state for forensic review. Exit.
```

### Pre-condition (`SKILL.md:39-45`)
Output-path policy guard: refuses `--output` under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`. Reflect's chosen output path MUST land under `.dev/` (typically `.dev/eval-workspaces/sc-reflect/` or per-task `.dev/releases/current/<release>/`).

---

## 2. task-builder — Wave 6 (T3) BUILD_REQUEST Shape

### File / Anchors
- **SKILL file:** `src/superclaude/skills/task-builder/SKILL.md`
- **BUILD_REQUEST format section:** `SKILL.md:785-985`
- **Subagent spawn directive:** `SKILL.md:788-790` (`subagent_type: "rf-task-builder"`, `mode: "bypassPermissions"`)

### Literal BUILD_REQUEST Field Set (M1-frozen, 15 fields)

Reflect's `refs/remediation-handoff.md` template MUST emit these exact field names + ordering:

```text
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
    GOAL: [GOAL - what the task file should accomplish when executed]

    WHY: [WHY - context for why this task is needed]

    TASK_ID_PREFIX: TASK-RF

    TEMPLATE: [01 or 02 - orchestrator selected:
      01 = simple task, known inputs/outputs, direct transformation
      02 = complex task requiring discovery, build, test, review phases]

    QA_GATE_REQUIREMENTS: [Default: FINAL_ONLY for Template 01, PER_PHASE for Template 02.
      NONE | FINAL_ONLY | PER_PHASE]

    VALIDATION_REQUIREMENTS: [Specifies validation checklist items the generated task file
      must include. Default: "Standard project validation: lint, type-check, and build must pass."]

    TESTING_REQUIREMENTS: [Options: NONE | UNIT | INTEGRATION | E2E | ALL. Default: infer from GOAL.]

    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2). Values: AUTO (default) | REQUIRED | SUPPRESS.
      AUTO emits when BUILD_REQUEST exposes rollup signal (>=3 distinct named source areas).
      REQUIRED forces emission. SUPPRESS forbids emission.
      Omission implies AUTO.]

    DOCUMENTATION STALENESS WARNINGS:
    [List doc-validator findings, OR write "None found during scope discovery..."]
    Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED].

    RESEARCH DIR: ${TASK_DIR}research/
    Read ALL .md files in this directory for full research findings.
    [list each researcher's topic and file name]

    QUALITY GATE RESULTS:
    The research was reviewed by analyst and QA agents. Their reports are in ${TASK_DIR}qa/:
    - qa/analyst-completeness-report.md
    - qa/qa-research-gate-report.md
    [If gap-fill was needed: gap-fill research is in NN-gap-fill.md]

    OPEN QUESTIONS (could not be resolved by research):
    [List unresolved questions - document as risks/assumptions in the task file, NOT as basis for items]

    REMAINING GAPS (if any - after max gap-fill rounds):
    [List persistent gaps. Document as known limitations.]

    CRITICAL - GRANULARITY REQUIREMENT:
    Per MDTM template rules A3 / A4, create individual checklist items for EVERY file, component, or iteration involved.

    ESCALATION - CRITICAL OVERRIDE:
    Since you are running as a subagent, you have NO team context. Do NOT broadcast TASK_READY,
    use TaskCreate, or use SendMessage. Return the task file path as your final output.

    INCREMENTAL TASK FILE WRITING (MANDATORY - NEVER ONE-SHOT):
    [Incremental Write+Edit protocol - see SKILL.md:910-924]

    EXECUTION CONTEXT BLOCK (OPTIONAL, TASK-LEVEL ROLL-UP):
    [See SKILL.md:926-981 for the 3-emitter contract: References / Source areas / Key constraints]
```

### Field-Order Constraint
The 15 fields above are M1-frozen at byte level per the EXECUTION_CONTEXT_REQUIREMENTS doc (`SKILL.md:842-844`): "Strictly additive - when absent or AUTO, the M1-frozen 15-field BUILD_REQUEST behavior is preserved byte-identical."

### Agent Identity Reference
Reflect's `refs/remediation-handoff.md` should also document the upstream caller convention that other doc skills use the rf-task-builder **agent** (not skill): "spawn the `rf-task-builder` **agent** via the Agent tool... they use the agent definition at `.claude/agents/rf-task-builder.md`, not this skill" (`task-builder/SKILL.md:84`).

---

## 3. sc-troubleshoot-protocol — REVERSE Caller of Reflect

### File / Anchors
- **SKILL:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- **refs:** `refs/remediation-handoff.md`, `refs/report-template.md`

### Literal Invocation Strings sc-troubleshoot Emits

| Phase | File:line | Literal Command |
|-------|-----------|-----------------|
| Wave 6 Phase B (pre-execution review) | `SKILL.md:368` | `/sc:reflect --type task --analyze` |
| Wave 6 Phase B (alt notation) | `refs/remediation-handoff.md:14` | `/sc:reflect --type task --analyze` against the task file |
| Wave 6 Phase B (full spawn) | `refs/remediation-handoff.md:70` | `Invoke /sc:reflect --type task --analyze <task-file> via Skill (if sc:reflect is available - otherwise fall back to spawning the self-review agent on the task file)` |
| Wave 6 Phase D (post-execution validation) | `SKILL.md:370` | `/sc:reflect --type task --validate` |
| Wave 6 Phase D (alt notation) | `refs/remediation-handoff.md:16` | `After you run /task and report back, run /sc:reflect --type task --validate` |
| Wave 6 Phase D (full spawn) | `refs/remediation-handoff.md:101` | `/sc:reflect --type task --validate <task-file>` |
| Wave 6 user-prompt (Phase C handoff text) | `refs/remediation-handoff.md:89` | `or /sc:reflect --type task --validate <abs-path> for the post-execution gate.` |
| Report-template recommendation | `refs/report-template.md:132` | `Run /sc:reflect --type task --validate <task-file> before committing.` |
| Tool-permission row | `SKILL.md:387` | `Skill - check (task-builder, /sc:reflect)` |

### Reflect Surface Reflect Must Therefore Expose

Reflect's command-grammar MUST accept:

```
/sc:reflect --type task --analyze <task-file-path>
/sc:reflect --type task --validate <task-file-path>
```

These correspond to spec §3 invocation modes (UC-1 pre vs UC-2 post). The current command file at `src/superclaude/commands/reflect.md:22` already shows `[--type task|session|completion] [--analyze] [--validate]` as the grammar, so the contract is already defined; reflect's new skill body must consume it identically.

### Fallback Sequence sc-troubleshoot Expects
From `refs/remediation-handoff.md:70`: "if `sc:reflect` is available - otherwise fall back to spawning the `self-review` agent on the task file". Reflect's contract is therefore: if reflect emits `status: failed` with `failure_stage: transport`, sc-troubleshoot will fall back to `self-review` agent. Reflect's Wave 0 prereq-failure path must therefore exit cleanly with the canonical failure contract.

### sc-troubleshoot's Phase B verdict consumption (`refs/remediation-handoff.md:74-76`)
```
- OK -> proceed to Phase C.
- Recommends refactor -> surface the recommendation; ask the user "refactor or proceed?"
- Blocker -> STOP. Do not advance to Phase C until the user resolves it.
```

For reflect's contract to drive this, it MUST map to the §9.3 row: `status`, `regression_present`, `needs_human_decision`. Specifically:
- `status: success AND regression_present: false` -> OK
- `status: partial OR drift detected` -> "recommends refactor"
- `status: failed OR regression_present: true OR needs_human_decision: true` -> Blocker.

---

## 4. sc-task-protocol — REVERSE Caller (Aspirational)

### File / Anchors
- **SKILL file:** `src/superclaude/skills/sc-task-protocol/SKILL.md`

### Current State
Grep for `sc:reflect` / `sc-reflect` / `/sc:reflect` in `sc-task-protocol/SKILL.md` returns **ZERO matches**. There is no current reflect-invocation wiring inside sc-task-protocol.

### Spec-Defined Inbound Contract (per `merged-requirements.md:686`)
The §9.3 Consumer Field Map defines what sc-task-protocol's "end-of-task hook" SHOULD do once wired:

| Surface | Load-bearing fields | Routing semantics |
|---------|---------------------|-------------------|
| Inline post-execution | `status`, `tier_reached`, `deviation_count_by_class`, `confidence_calibrated`, `needs_human_decision` | `status: success AND confidence_calibrated >= 0.85` -> mark task done; `deviation_count_by_class.regression > 0` -> escalate to troubleshoot; `needs_human_decision: true` -> surface Grounding Gaps to user. |

### Invocation Shape sc-task-protocol SHOULD Pass (per spec convention)
sc-task-protocol's "Verification Phase" table at `SKILL.md:118-127` routes by compliance tier (STRICT / STANDARD / OPT_OUT). Per `integration-analysis.md:307`, the natural wiring is to extend the STRICT tier:

```
| Compliance Tier | Verification Method                                          | Token Cost     | Timeout       |
|-----------------|--------------------------------------------------------------|----------------|---------------|
| STRICT          | Sub-agent (quality-engineer) + /sc:reflect --mode post       | 3-5K + 10-70K  | 60s + 10min   |
```

Note the integration-analysis uses `--mode post` (matching reflect's UC-2 grammar in `merged-requirements.md:24`); the legacy command grammar uses `--type task --validate`. Reflect's NEW skill SHOULD accept BOTH the legacy `--type task --validate` form (so existing sc-troubleshoot/sc-auggie-review callers don't break) AND the new `--mode post` form (so sprint/sc-task-protocol can use the canonical UC-2 surface).

---

## 5. Sprint CLI Executor — TurnLedger Consumer

### File / Anchors
- **Sprint executor:** `src/superclaude/cli/sprint/executor.py`
- **TurnLedger model:** `src/superclaude/cli/sprint/models.py:693-776`
- **Imports of TurnLedger:** `executor.py:35`

### TurnLedger Class Structure (`models.py:692-776`)

```python
@dataclass
class TurnLedger:
    initial_budget: int
    consumed: int = 0
    reimbursed: int = 0
    reimbursement_rate: float = 0.8
    minimum_allocation: int = 5             # <-- the §4.0 step 0.9 floor reflect must respect
    minimum_remediation_budget: int = 3
    wiring_turns_used: int = 0
    wiring_turns_credited: int = 0
    wiring_budget_exhausted: int = 0
    wiring_analyses_count: int = 0

    def available(self) -> int:             # models.py:717 - the value reflect's --budget-remaining mirrors
        return self.initial_budget - self.consumed + self.reimbursed

    def debit(self, turns: int) -> None: ...        # models.py:721
    def credit(self, turns: int) -> None: ...       # models.py:727
    def can_launch(self) -> bool: ...               # models.py:733 - uses minimum_allocation=5
    def can_remediate(self) -> bool: ...            # models.py:737 - uses minimum_remediation_budget=3
    def debit_wiring(self, turns: int = 1) -> None: ...
    def credit_wiring(self, turns: int, rate: float | None = None) -> int: ...
    def can_run_wiring_gate(self) -> bool: ...
```

### Reflect <-> TurnLedger Wiring Per Spec §9.3 (`merged-requirements.md:685`)

```
Consumer: superclaude sprint run (executor.py TurnLedger)
Surface:  CLI consumer of return-contract.yaml
Load-bearing fields:
  - status                                        # top-level
  - per_task_verdicts[].status                    # array[].field
  - per_task_verdicts[].per_task_validation_strength
  - per_task_verdicts[].deviation_class
  - budget_forced_tier_downgrade                  # top-level

Routing semantics:
  - status: partial OR failed             -> halts the phase
  - per_task_validation_strength < 0.70   -> flags task for re-execution
  - deviation_class == regression         -> triggers TurnLedger rollback
  - budget_forced_tier_downgrade: true    -> adjusts subsequent reflect-call budget
```

### per_task_verdicts Field Schema (`merged-requirements.md:621-627`)

```yaml
per_task_verdicts:                       # empty list for UC-1 or single-task UC-2
  - task_id: <string>
    status: success | partial | failed
    deviation_class: authorized | necessary | drift | regression | none
    citations_dropped: <int>
    per_task_validation_strength: <float 0.00-1.00>   # P2: calibrated, post-evidence-validator
    evidence_anchor: <abs path or task-log ref>
```

### budget_forced_* Fields Reflect Emits (`merged-requirements.md:634-637`)

```yaml
budget_forced_tier_downgrade: bool   # true when --budget-remaining triggered tier downgrade per §4.0 step 0.9
budget_forced_stop: bool             # true when --budget-remaining < 5 (below TurnLedger.minimum_allocation)
budget_check_skipped: bool           # true when --budget-remaining was not provided
forced_tier: 1 | 2 | null            # populated when budget_forced_tier_downgrade == true
```

### Reflect's --budget-remaining Behavior Table (`merged-requirements.md:251-254`)

| N (budget remaining) | Behavior | Contract Effect |
|----------------------|----------|-----------------|
| `N < 5` (below `TurnLedger.minimum_allocation`) | STOP with `"budget too low for reflect - minimum 5 turns"` | `budget_forced_stop: true` |
| `5 <= N < 6` | Run T1 only with WARN; no T2 even if rubric requests | `budget_forced_tier_downgrade: true`, `forced_tier: 1` |
| `6 <= N < 52` | Allow T1; if rubric escalates AND `N < 65`, downgrade to T1 with WARN | `budget_forced_tier_downgrade: true` only if downgrade applied |
| `N >= 65` | No constraint | `budget_forced_tier_downgrade: false` |

### Sprint Executor Hook Surface (for reflect to be invoked FROM sprint)

| Hook | File:line | Purpose |
|------|-----------|---------|
| `notify_phase_complete` | `executor.py:1605` (call site) / `notify.py:34` (def) | End-of-phase signal - natural reflect-per-phase insertion point |
| `notify_sprint_complete` | `executor.py:1728` (call site) / `notify.py:50` (def) | End-of-sprint signal - natural Wave 7 promotion-gate insertion point |
| `run_post_phase_wiring_hook` | `executor.py:748` (def) / `:1568` (call) | Existing anti-instinct integration_contracts validation - reflect's per-phase hook would parallel this |
| `RetrospectiveGenerator.generate` | `retrospective.py:345` / `executor.py:1679` | Aggregates `phase-N-summary.md` files |

### TurnLedger Construction Site
`executor.py:1199-1200`: `# T01 (BUG-001/P0): Construct TurnLedger for budget tracking ` followed by `ledger = TurnLedger(...)`. The sprint executor passes `ledger` into `execute_phase_tasks(...)` and `execute_sprint(...)`. Reflect-per-phase / reflect-promotion hooks (when added per `integration-analysis.md` Change 1) would receive `ledger` via the same parameter pattern.

---

## 6. confidence-calibrator — Task Invocation Shape

### File / Anchors
- **Agent file:** `src/superclaude/agents/confidence-calibrator.md`
- **Frontmatter:** `name: confidence-calibrator`, `tools: Read`, `model: sonnet`, `maxTurns: 25`, `permissionMode: plan` (`confidence-calibrator.md:1-9`)

### Required Input Fields (`confidence-calibrator.md:41-46`)

```yaml
card_path:     <absolute path to the hypothesis card to score>
rubric_path:   <absolute path to refs/escalation-rubric.md>
card_tier:     1 | 2                       # affects the escalation recommendation
flags_context: {dict with --depth, --no-escalate, --type ...}
output_path:   <where to write the calibration report>
```

### Reflect's Wave 1D / 3C Invocation Shape

Reflect MUST spawn via `Task` with this exact field set:

```
Task with subagent_type="confidence-calibrator",
     prompt: |
       card_path: <abs path>
       rubric_path: <abs path to refs/escalation-rubric.md>
       card_tier: <1 or 2>
       flags_context: {"--depth": "<value>", "--no-escalate": <bool>, "--type": "<task|session|completion>"}
       output_path: <abs path>
```

### Output Format (`confidence-calibrator.md:58-93`)
The calibration report includes per-dimension scores (5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence), self-reported vs calibrated confidence with signed delta, and an escalation verdict (`STOP` / `ESCALATE`) with reason from a closed vocabulary: `none | low_confidence | multi_domain | intermittent | not_reproducible | forced_by_depth_deep | security_caution`.

### Failure Modes Reflect Must Handle (`confidence-calibrator.md:113-118`)
- Subprocess crash / timeout -> orchestrator falls back to inline calibration; logs `calibration: inline-fallback` in audit
- Malformed output -> same as crash
- Truncated card -> agent scores missing dimension 0.0
- Placebo risk -> meta-eval to compare inline vs agent

---

## 7. evidence-validator — Task Invocation Shape

### File / Anchors
- **Agent file:** `src/superclaude/agents/evidence-validator.md`
- **Frontmatter:** `name: evidence-validator`, `tools: Read, Grep, Glob`, `model: sonnet`, `maxTurns: 50`, `permissionMode: plan` (`evidence-validator.md:1-9`)

### Required Input Fields (`evidence-validator.md:40-44`)

```yaml
report_draft_path:        <absolute path to the draft REPORT.md>
evidence_section_locator: <hint about which section contains evidence; typically "## Evidence">
output_path:              <where to write the validation report>
allow_command_reexec:     bool    # Default and recommended: false. v1 of sc:troubleshoot-protocol always passes false.
```

### Reflect's Wave 5 Invocation Shape

Reflect MUST spawn via `Task` with these exact field names and `allow_command_reexec: false`:

```
Task with subagent_type="evidence-validator",
     prompt: |
       report_draft_path: <abs path to draft REPORT.md>
       evidence_section_locator: "## Evidence"
       output_path: <abs path>
       allow_command_reexec: false
```

### Citation Verdict Vocabulary (`evidence-validator.md:55`)
`verified | line-mismatch | file-missing | snippet-mismatch`

### Status Decision Rules (`evidence-validator.md:99-103`)
- `success`: zero dropped citations
- `partial`: at least one dropped citation
- `failed` is decided by orchestrator, NOT the validator

### Failure Modes Reflect Must Handle (`evidence-validator.md:124-129`)
- Subprocess crash/timeout -> orchestrator falls back to inline validation; marks report `partial` with a Grounding Gap entry
- Malformed output -> fallback to inline validation
- Silent-wrong-output -> mitigated only by meta-eval against fixture reports

---

## 8. Other Agents — Task Invocation Shapes

### 8.1 root-cause-analyst (`src/superclaude/agents/root-cause-analyst.md`)

**Frontmatter:** `name: root-cause-analyst`, `category: analysis`. NO `tools` / `model` / `maxTurns` / `permissionMode` lock — uses defaults.

**Triggers (`:8-13`):** complex debugging, multi-component failure, hypothesis testing, root cause identification.

**Input contract:** Free-form spawn prompt - no strict input schema. Reflect's Wave 1C UC-2 invocation (`merged-requirements.md:463`) describes the use:
> `root-cause-analyst | 1C | UC-2 | Investigate any deviation candidate found in Wave 1B; produce hypothesis card with deviation_class field | Inline orchestrator card`

**Outputs (`:30-36`):** Root cause analysis reports with evidence chain, investigation timelines, evidence documentation, problem resolution plans, pattern analysis. Reflect's invocation must request a hypothesis card with the §10 `deviation_class` field.

### 8.2 self-review (`src/superclaude/agents/self-review.md`)

**Frontmatter:** `name: self-review`, `category: quality`. NO tool/model lock.

**Input contract:** Free-form. Operation is documented in body:
1. Review the task summary and implementation diff supplied
2. Confirm test evidence
3. Produce a short checklist-style report (4 mandatory questions: tests, edge cases, requirements, follow-up)
4. Recommend targeted actions

**Reflect's use:** sc-troubleshoot uses self-review as FALLBACK when reflect is unavailable (`refs/remediation-handoff.md:70`). Reflect itself may invoke self-review during Wave 3 reviewer ensemble.

### 8.3 requirements-analyst (`src/superclaude/agents/requirements-analyst.md`)

**Frontmatter:** `name: requirements-analyst`, `category: analysis`. NO tool/model lock.

**Triggers (`:8-13`):** ambiguous project requests, PRD creation, stakeholder analysis, scope definition.

**Input contract:** Free-form spawn prompt. Outputs PRDs, requirements analysis, project specifications, success frameworks, discovery reports.

**Reflect's use:** Wave 3 reviewer (UC-1 spec-evaluation mode) - invoke with the spec under review + heterogeneous-class instruction.

### 8.4 audit-validator (`src/superclaude/agents/audit-validator.md`)

**Frontmatter:** `name: audit-validator`, `tools: Read, Grep, Glob`, `model: sonnet`, `maxTurns: 25`, `permissionMode: plan` (locked, like evidence-validator).

**Input contract (`audit-validator.md:24-33`):**

```
You will receive:
  1. A randomly sampled set of findings to validate (5 findings per 50 files audited = 10% sample rate)
  2. The original batch reports containing the findings
  3. The output file path for your validation report
```

**Sampling rule (`:31-36`):**
- At least 1 DELETE finding (if any exist)
- At least 1 KEEP finding
- At least 1 FLAG/REVIEW finding (if any exist)
- Remaining slots from random selection

**4 verification checks (`:40+`):**
1. Grep Claim Verification
2. (additional checks below this offset)

**Reflect's potential use:** as a Wave 5 secondary validator alongside evidence-validator when audit-style spot-checking is needed (e.g., UC-2 tasklist-completion audit). Not in the primary spec but available.

### 8.5 socratic-mentor (`src/superclaude/agents/socratic-mentor.md`)

**Frontmatter:** `name: socratic-mentor`, `category: communication`. NO tool/model lock.

**Identity:** Educational guide using Socratic method.

**Input contract:** Free-form. Knowledge domains include Clean Code, GoF Design Patterns.

**Reflect's use:** none in the spec. Listed for completeness; reflect does not invoke socratic-mentor.

### 8.6 rf-qa (`src/superclaude/agents/rf-qa.md`)

**Frontmatter (`:1-39`):** `name: rf-qa`, `memory: project`, `permissionMode: bypassPermissions`, broad tool surface (Read, Write, Edit, Bash, Glob, Grep, tavily-search, tavily-extract, WebFetch, WebSearch, NotebookEdit, Agent, Task, TaskOutput, TaskStop, SendMessage, TaskCreate, TaskGet, TaskUpdate, TaskList, TeamCreate, TeamDelete, Skill, AskUserQuestion, EnterPlanMode, ExitPlanMode).

**Input contract - spawn prompt fields (`:42-50`):**

```
- Which QA phase: research-gate | synthesis-gate | report-validation | task-integrity | fix-cycle
- Research directory path AND topic context
- Specific files to verify (or "all files in directory")
- Verification criteria (the checklist to apply)
- Team name for SendMessage (if running in a team context)
- Fix authorization: whether you can fix issues in-place or must report only
- assigned_files: [list of specific file paths]    # OPTIONAL - for parallel partitioning
```

**Reflect's potential use:** as a secondary validator for tasklist-integrity audits in UC-2 mode. Not central to the spec.

### 8.7 rf-qa-qualitative (`src/superclaude/agents/rf-qa-qualitative.md`)

**Frontmatter (`:1-39`):** Same tool/permission surface as rf-qa.

**Input contract - spawn prompt fields (`:42-50`):**

```
- Which QA phase: prd-qualitative | tdd-qualitative | tech-ref-qualitative | ops-guide-qualitative | readme-qualitative | report-qualitative | task-qualitative | doc-qualitative
- Document path to review
- Document type: Product PRD | Feature PRD | Component PRD | Research Report | Tech Reference | ...
- Template path (if applicable)
- Output path for your QA report
- Team name for SendMessage (if running in a team context)
```

**Reflect's potential use:** qualitative review of reflect-generated reports. Not in primary spec path.

---

## 9. §9.3 Consumer Field Map — Full Inbound Contract Map

From `merged-requirements.md:680-692`:

| Consumer | Surface | Load-bearing Fields | Routing Semantics |
|----------|---------|---------------------|-------------------|
| `sc-troubleshoot-protocol` Wave 6 (Phase B/D) | Skill-to-skill invocation | `status`, `tier_reached`, `confidence_calibrated`, `regression_present`, `needs_human_decision` | `status: failed` halts troubleshoot; `regression_present: true` forces Tier-3 troubleshoot path; `needs_human_decision: true` surfaces to user. |
| `superclaude sprint run` (executor.py TurnLedger) | CLI consumer of return-contract.yaml | `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade` | `status: partial OR failed` halts the phase; `per_task_validation_strength < 0.70` flags re-execution; `deviation_class == regression` triggers TurnLedger rollback; `budget_forced_tier_downgrade: true` adjusts subsequent budget. |
| `sc-task-protocol` end-of-task hook | Inline post-execution | `status`, `tier_reached`, `deviation_count_by_class`, `confidence_calibrated`, `needs_human_decision` | `status: success AND confidence_calibrated >= 0.85` -> mark task done; `deviation_count_by_class.regression > 0` -> escalate to troubleshoot; `needs_human_decision: true` -> surface Grounding Gaps. |
| `sc:roadmap` validation gate | Roadmap pipeline post-step | `status`, `coverage_pct`, `unmapped_requirements`, `best_practice_grade` | `coverage_pct < 0.90 OR unmapped_requirements != []` -> roadmap re-runs spec coverage; `best_practice_grade < 3` -> flag for review. |
| `sc:tasklist` generator gate | Tasklist pipeline post-step | `status`, `coverage_pct`, `unmapped_requirements`, `coverage_undefined` | `coverage_undefined: true` -> "spec too sparse"; `coverage_pct < 0.90` -> emit warning. |
| `task-builder` skill | Wave 6 (T3) handoff | `report_path`, `deviation_register_path`, `grounding_gaps_path`, `needs_human_decision` | Reads the three paths to materialize BUILD_REQUEST; `needs_human_decision: true` -> BUILD_REQUEST template prompts for user resolution. |
| Wave 7 promotion adapters (in-skill) | Internal consumer | All 9-condition-gate inputs: `mode`, `status`, `tasklist_completion_pct`, `deviation_count_by_class.{drift,regression}`, `citations_dropped`, `input_drift_detected`, `needs_human_decision`, `user_decision_required`, `convergence_score`, `tier_reached`, frontmatter check | Per §14.5.2 gate; all 9 must pass for mutation; any fail -> `promotion_action: skipped/rejected`. |
| CI (`make reflect-eval` / `make reflect-eval-quick`) | grader.py | All fields under "Per-task verdict array" + `status` + `evidence_validator_ran` + `audit_log_path` | Used to score 6 grading dimensions in §12.1. |
| Meta-eval (`runs.jsonl` aggregator - §15.1) | Cross-run analytics | `status`, `tier_reached`, `wave_durations_ms`, `token_usage`, `convergence_score`, `t2_model_class_diversity`, `t2_vendor_diversity` (telemetry) | Aggregated cross-runs. |

**Field-deletion guard (`merged-requirements.md:694`):** Removing or renaming a field listed in §9.3 is a breaking change requiring contract major-version bump per §9.4.

### Promotion Adapter Fields Reflect Emits (`merged-requirements.md:640-652`)

```yaml
promotion_action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable
promotion_adapter: task | sprint-release | none | null
promotion_source: <abs path> | null
promotion_destination: <abs path> | null
promotion_log_path: <abs path> | null
promotion_gate_passed: bool | null
promotion_skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
promotion_fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
promotion_override_used: --promote-anyway | --promote-resume | null
promotion_rollback_command: <string> | null
promotion_checkpoint_path: <abs path> | null
promotion_cross_fs: bool
promotion_pending: bool
```

---

## 10. Cross-Reference — Reflect Command Surface Already Defined

The legacy reflect command at `src/superclaude/commands/reflect.md:22` already exposes the grammar reflect's new skill body must consume:

```
/sc:reflect [--type task|session|completion] [--analyze] [--validate]
```

And its declared MCP integration (`reflect.md:42-47`):
- Serena MCP: mandatory for reflection
- Reflection tools: `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`
- Memory operations: `read_memory`, `write_memory`, `list_memories`

**Implication:** the new skill MUST keep `--type task --analyze` and `--type task --validate` as accepted forms so `sc-troubleshoot-protocol` (Wave 6 Phase B/D) and `sc-auggie-review-protocol` (Phases C and E at `SKILL.md:324,327`) continue to work without modification. The NEW grammar (`--mode pre|post`, `--budget-remaining`, `--no-promote`, etc.) is additive.

### sc-auggie-review-protocol Caller Surface (parallel to sc-troubleshoot)

From `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:324,327`:

| Phase | Literal Invocation |
|-------|--------------------|
| Phase C | `/sc:reflect --type task --analyze` |
| Phase E | `/sc:reflect --type task --validate` |

From `refs/remediation-handoff.md:30,35,102-112,144-152`: same surface as sc-troubleshoot Phase B/D - the two skills have nearly identical reflect-handoff machinery.

---

## 11. Risks and Gaps

1. **`artifacts_dir` vs `adversarial_artifacts_dir` naming.** Reflect's spec section 9.3 / integration analysis may use the brainstorm-style wrapped name; the canonical sc-adversarial-protocol contract field is `artifacts_dir`. Reflect's caller code MUST read the literal `artifacts_dir` field name from the adversarial return contract.
2. **Dual command grammar.** Reflect's NEW skill must accept BOTH `--type task --analyze` (legacy, used by sc-troubleshoot Phase B + sc-auggie-review Phase C) and `--mode pre` (new, per spec §3). Same for `--validate` / `--mode post`. The §3 grammar is additive; the legacy grammar cannot be removed without breaking sc-troubleshoot + sc-auggie-review.
3. **sc-task-protocol integration aspirational.** No code currently invokes reflect from sc-task-protocol. Reflect can ship its emitter side (the contract fields sc-task-protocol would consume), but the consumer side is a separate sc-task-protocol patch (per `integration-analysis.md` Change recommendations).
4. **TurnLedger consumer side aspirational.** Sprint executor at `executor.py:1605` (post-phase) and `:1728` (post-sprint) does NOT currently invoke reflect. Reflect emits the contract fields TurnLedger would consume (`budget_forced_tier_downgrade`, `per_task_verdicts[]`), but actual TurnLedger reading-side code is also a separate sprint-CLI patch (per `integration-analysis.md` Change 1).
5. **`--budget-remaining` floor precision.** The `5 <= N < 6` band at `merged-requirements.md:252` exists only in integer arithmetic (i.e., only `N=5` lands in this band). Reflect's `--budget-remaining` parser must therefore handle integer values; spec is explicit.
6. **rf-qa input-field flexibility.** rf-qa accepts a broad spawn prompt with no rigid schema (just listed bullet points). Reflect's invocations of rf-qa (if any in qualitative review path) should use the documented field names from `rf-qa.md:42-50`: `Which QA phase`, `Research directory path`, `Specific files to verify`, `Verification criteria`, `Team name`, `Fix authorization`, optionally `assigned_files`.
7. **task-builder BUILD_REQUEST is M1-frozen.** Reflect's `refs/remediation-handoff.md` template must NOT modify the 15-field ordering or names. Adding a 16th field would be an additive change governed by task-builder's own contract evolution, not reflect's.

---

## 12. File Path Index (Absolute)

| Integration Target | Absolute Path |
|--------------------|---------------|
| sc-adversarial-protocol SKILL | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-adversarial-protocol/SKILL.md` |
| sc-brainstorm-protocol SKILL (F1/F2/F3 reference) | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` |
| task-builder SKILL | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/task-builder/SKILL.md` |
| sc-troubleshoot-protocol SKILL | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` |
| sc-troubleshoot-protocol remediation-handoff | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` |
| sc-troubleshoot-protocol report-template | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` |
| sc-auggie-review-protocol SKILL | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` |
| sc-auggie-review-protocol remediation-handoff | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` |
| sc-task-protocol SKILL | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/skills/sc-task-protocol/SKILL.md` |
| Sprint executor | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/cli/sprint/executor.py` |
| TurnLedger model | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/cli/sprint/models.py` (class at :693) |
| confidence-calibrator agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/confidence-calibrator.md` |
| evidence-validator agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/evidence-validator.md` |
| root-cause-analyst agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/root-cause-analyst.md` |
| self-review agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/self-review.md` |
| requirements-analyst agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/requirements-analyst.md` |
| audit-validator agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/audit-validator.md` |
| socratic-mentor agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/socratic-mentor.md` |
| rf-qa agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/rf-qa.md` |
| rf-qa-qualitative agent | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/agents/rf-qa-qualitative.md` |
| integration-analysis.md | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/brainstorms/sc-reflect-rebuild/integration-analysis.md` |
| merged-requirements.md | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` |
| Legacy reflect command (grammar source) | `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/src/superclaude/commands/reflect.md` |
