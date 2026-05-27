---
name: sc-reflect-protocol
description: "Two-mode tiered reflection protocol — UC-1 pre-execution plan/spec validation and UC-2 post-execution diff-vs-tasklist verification. Tier 1 fast grounded reflection (single agent), Tier 2 parallel heterogeneous reviewers merged via sc-adversarial Mode A, opt-in Tier 3 task-builder remediation. Use this skill whenever the user asks 'does this plan cover X', 'did this work finish', 'verify the diff against the spec', 'review what just got built', or pipes /sc:tasklist (pre-exec) / /sc:task (post-exec) output into reflect."
version: 1.0.0
mcp-servers: [auggie, serena, context7, tavily, sequential]
complexity: advanced
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---

<!-- Extended metadata (for documentation, not parsed):
spec: .dev/eval-workspaces/sc-reflect/SPEC.md
category: orchestration
personas: [analyzer, qa, refactorer, architect]
supersedes: src/superclaude/commands/reflect.md (monolithic, Serena-only, think_about_* surface)
-->

# sc:reflect-protocol — Tiered Two-Mode Reflection

## 1. Triggers

sc:reflect-protocol is invoked only by the `sc:reflect` command via `Skill sc:reflect-protocol` in its `## Activation` section. Never invoked directly by users. The command file is a thin entrypoint; all behavior lives here.

Activation conditions:

- User runs `/sc:reflect [--mode pre|post|auto] [--depth quick|standard|deep] [--scope ...] [--fix] [--output ...]`
- A sibling skill (sc:troubleshoot Wave 6 Phase B, sc:pm) hands off via `Skill sc:reflect-protocol` with structured arguments
- The command was given a tasklist file, a diff range, an artifact directory, or piped input from `/sc:tasklist` (pre-exec contract) or `/sc:task` (post-exec contract)

## 2. Purpose & Skill Boundary

**Owns**: orchestration of a tiered, two-mode reflection workflow that grounds every claim in real code via the modern Serena symbolic surface + auggie codebase retrieval, calibrates confidence independently, merges heterogeneous reviewer verdicts adversarially, and optionally hands off remediation.

**Delegates** (does NOT re-implement):

- Adversarial debate, hybrid scoring, base-selection, refactor-plan, merge-log → `sc:adversarial-protocol` Mode A (`--compare`)
- Confidence re-grading without anchoring → `confidence-calibrator` agent
- File:line citation re-grounding → `evidence-validator` agent
- Root-cause investigation on detected deviations → `root-cause-analyst` agent
- Structural/qualitative QA partitioning over large diffs → `rf-qa` / `rf-qa-qualitative` agents
- Spot-check sampling on ≥20-finding sets → `audit-validator` agent
- Final sanity check on merged verdict → `self-review` agent
- Pre-actionable confidence gate → `confidence-check` skill
- External best-practice / framework doc lookup → `tech-research` skill
- Task file generation for Tier 3 remediation → `task-builder` skill

**The boundary contract**: this skill is an orchestrator. Every artifact it emits is composed from sub-skill/agent outputs. Its own logic is restricted to (a) tier decisioning, (b) mode dispatch, (c) Serena-grounded evidence collection, (d) calibration/validation wiring, and (e) return-contract composition. Any non-trivial scoring, debate, or merge work that appears inline in this SKILL.md is a structural defect to be deleted.

**Pipeline position**:

```
UC-1: (tasklist | spec | PRD) + plan → /sc:reflect --mode pre → coverage+risk verdict → (PASS → execute) | (FAIL → revise plan)
UC-2: (diff | artifact-dir) + tasklist → /sc:reflect --mode post → completion+deviation verdict → (PASS → ship) | (FAIL → Tier 3 task-builder remediation)
```

## 3. Required Input & Mode Selection

The skill auto-detects UC-1 vs UC-2 unless `--mode` is explicit. Auto-detection rules — applied in order, first match wins:

1. `--mode pre|post` present → use literal value. STOP if value is anything else.
2. `--diff` flag or `--commit-range` flag present → `post`.
3. `--scope` resolves to a directory containing modified files (`git diff --name-only HEAD~1..HEAD` overlaps the scope) → `post`.
4. Input arguments include both a tasklist file AND a completed-work artifact directory (`.dev/tasks/done/`, `.dev/releases/current/results/`, etc.) → `post`.
5. Input is a tasklist file OR a spec/PRD/TDD only, with no diff / no done-marker artifacts → `pre`.
6. None of the above resolve → STOP with: `"sc:reflect cannot infer mode. Pass --mode pre (validate a plan) or --mode post (review completed work). Required input: a tasklist/spec file (pre) OR a diff+tasklist pair (post)."`

**STOP conditions (both modes)**:

- Missing both the spec/tasklist file AND any scope/diff input
- `--depth deep` requested with input under 200 tokens (too vague to reward deep cost)
- `--output` path resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (output-policy guard, mirrors sc-adversarial)
- `--mode post` requested without an identifiable tasklist or spec as the reference contract — "did we finish" is undefined without a definition of "done"

**Mode-specific required inputs**:

| Mode | Reference contract | Work artifact |
|------|--------------------|---------------|
| pre  | spec / PRD / TDD / tasklist file | the proposed plan (strategy text, tasklist draft, design doc) |
| post | tasklist OR spec that drove the work | diff (git range, PR number, or modified-files set) + optional task log / commit messages |

## 4. Wave Architecture

```
Wave 0:  Parse + Validate Input + Mode Selection
Wave 1:  Grounding — auggie + serena + memory recall (parallel fan-out)
Wave 2:  Coverage Matrix — UC-1: spec→plan, UC-2: tasklist→diff
Wave 2.5: Tier Decision Gate (refs/tier-rubric.md)
Wave 3:  Tier 1 — Single-agent reflection + confidence-calibrator
         ↓ (rubric escalates)
Wave 4:  Tier 2 — Parallel heterogeneous reviewers (2-3 agents on different model classes)
Wave 5:  Tier 2 Merge — Skill sc:adversarial-protocol --compare
Wave 6:  Evidence Validation — evidence-validator on every file:line
Wave 7:  Synthesis + Report + Return Contract
Wave 8:  Tier 3 — Optional task-builder remediation (only on --fix + UC-2 + user accept)
```

Refs are loaded on-demand per wave, never pre-loaded. Each wave has explicit entry/exit criteria. Token budgets and failure rows live inline with each wave.

### Wave 0 — Parse + Validate Input + Mode Selection

**Preconditions**: command invocation with at least one of the required inputs.

**Steps**:

1. Parse flags. Required (one of): `--scope`, `--diff`, `--commit-range`, or a positional path. Optional: `--mode`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`, `--reviewers N`, `--convergence FLOAT`.
2. Apply mode-selection rules from §3. Cache `mode ∈ {pre, post}` in state.
3. Resolve reference contract path and work artifact path. Read first ~500 lines of each to confirm parseability (frontmatter present, structure recognizable).
4. Compute output slug: `<mode>-<scope-or-contract-slug>-<YYYYMMDDHHMMSS>`. Default `<output-dir>` = `.dev/reflect/<slug>/`.
5. Open audit log; emit machine-readable header:

```
<!-- SC:REFLECT:TARGET
mode: pre | post
depth: quick | standard | deep | auto
reference_contract: <abs-path>
work_artifact: <abs-path-or-none>
scope: <path|symbol|none>
fix_authorized: <bool>
no_escalate: <bool>
reviewers_override: <int|none>
mcps_available: <auggie|serena|context7|tavily|sequential|none>
output_dir: <abs-path>
-->
```

6. Activate Serena project (`mcp__serena__activate_project` → repo root containing `.git/`). Failure is non-fatal (degraded mode flag).

**Exit criteria**: input validated, mode resolved, output dir created, audit log opened. Emit "Wave 0 complete: mode=<mode> depth=<depth>".

### Wave 1 — Grounding (parallel fan-out)

**Goal**: Build the structural map of what the reference contract specifies AND what the work artifact actually touched. Single-turn parallel MCP fan-out.

**Steps** (all issued in one turn):

1. `mcp__auggie__codebase-retrieval` with query: "Find the code involved in `<reference contract title or scope>`. Include functions, modules, and tests directly named by the contract." Scope to `--scope` if set.
2. For each file the reference contract names AND each file in the work artifact (UC-2 only): `mcp__serena__get_symbols_overview` to build the file-level symbol map.
3. For each symbol named in the contract: `mcp__serena__find_symbol` (presence check) + `mcp__serena__find_referencing_symbols` (blast-radius check).
4. `mcp__serena__list_memories` filtered by project slug to recall any prior reflection memories (key prefix `reflection/`).
5. UC-2 only: `git diff --stat <range>` and `git log --oneline <range>` via Bash for the diff structure.

**Fail-open policy**: every Serena/auggie call is fail-open per `sc-validate-roadmap-protocol` pattern. Failure logs `degraded: true` for that source; the wave proceeds. If all of auggie + serena fail, fall back to `Glob` + `Grep` and flag the whole wave `quality_tier: fallback_2`.

**Exit criteria**: grounding artifacts written to `<output-dir>/grounding/` — `auggie.md`, `serena-overview.md`, `serena-references.md` (UC-2: + `diff.txt`, `commits.txt`, `memories.txt`). Emit "Wave 1 complete: grounding_quality_tier=<primary|fallback_1|fallback_2>".

**Token budget**: ≤ 5k Claude tokens (heavy work offloaded to auggie/serena).

### Wave 2 — Coverage Matrix

**Goal**: Compute the structured mapping between the reference contract and the plan (UC-1) or the diff (UC-2). This is the data structure all later waves consume.

**Refs**: load `refs/coverage-matrix-template.md` (defines the matrix shape + classification cells).

**Steps**:

1. Extract atomic requirements from the reference contract (UC-1 + UC-2). Parser rules: numbered bullets, checkboxes, "MUST/SHALL/SHOULD" sentences, acceptance criteria. Each becomes a row with stable ID `R-NNN`.
2. UC-1: extract atomic plan steps from the proposed plan. Each becomes a column `P-NNN`.
   UC-2: extract atomic changes from the diff (per-file or per-symbol, governed by diff size — single-symbol if total change <300 LOC, per-file if larger). Each becomes a column `D-NNN`.
3. For each `R-NNN` × `(P|D)-NNN` cell, mark one of: `covered`, `partial`, `missing`, `n/a`.
4. UC-2 only: classify deviations using the **4-cell deviation taxonomy** (refs/deviation-taxonomy.md):
   - **Authorized expansion** — change present in diff but not in tasklist, AND a same-PR commit message, task-log entry, or sibling tasklist amendment explicitly approves it.
   - **Necessary deviation** — change diverges from tasklist but cites a technical constraint (test failure, library incompatibility, breaking-change discovery) AND the constraint is verifiable in the diff or task log.
   - **Drift** — change present in diff, absent from tasklist, no documented justification.
   - **Regression** — change directly contradicts a tasklist item, spec MUST/SHALL, or prior test.
5. Write `<output-dir>/coverage-matrix.md` (human-readable table) and `<output-dir>/coverage-matrix.json` (machine-readable, consumed by Wave 4 reviewers and Wave 7 synthesis).
6. Compute headline stats: `coverage_pct` (covered + partial × 0.5 / total), `drift_count`, `regression_count`. Cache in state.

**Exit criteria**: both matrix files written, headline stats in state. Emit "Wave 2 complete: coverage=<pct>% drift=<N> regression=<M>".

**Token budget**: ≤ 8k Claude tokens.

### Wave 2.5 — Tier Decision Gate

**Goal**: Decide T1 / T2 / T3 based on the rubric in `refs/tier-rubric.md`. The user never types the tier directly; the rubric chooses.

**Decision logic** (summarized; canonical in `refs/tier-rubric.md`):

| Signal | T1 (single agent) | T2 (parallel + adversarial) | T3 (remediation) |
|--------|-------------------|------------------------------|------------------|
| `--depth quick` OR `--no-escalate` | force | — | — |
| `--depth deep` | — | force | — |
| `--fix` AND `mode=post` AND verdict ≠ PASS | — | — | force after Wave 7 |
| `coverage_pct ≥ 0.95` AND `drift_count = 0` AND `regression_count = 0` AND `len(scope) ≤ 5 files` | stop | — | — |
| `coverage_pct < 0.80` OR `regression_count ≥ 1` | — | escalate | — |
| `drift_count ≥ 3` OR diff > 1000 LOC | — | escalate | — |
| Multi-domain (touches frontend + backend, or code + infra) | — | escalate (even on high coverage) | — |
| Reference contract referenced framework/library and Wave 1 hit auggie/serena `degraded` | — | escalate to recover via tech-research | — |
| Calibrated T1 confidence < 0.85 (computed in Wave 3) | — | escalate retroactively | — |

**Numeric thresholds (canonical)**: coverage 0.95 (T1 floor), 0.80 (T2 trigger); drift 3 (T2 trigger); diff size 1000 LOC (T2 trigger); calibrated confidence 0.85 (retro-escalation); convergence 0.75 (T2 PASS), 0.60 (T2 PARTIAL), <0.60 (T2 FAIL).

**Output**: `tier_planned ∈ {1, 2}` in state plus the literal rubric trigger string in `escalation_reason`.

**Exit criteria**: tier decision logged. Emit "Wave 2.5 complete: tier_planned=<N> escalation_reason=<string|n/a>".

### Wave 3 — Tier 1 Single-Agent Reflection + Calibration

**Goal**: Produce one grounded reflection card with calibrated confidence. Always runs (even when T2 is planned, T1 results feed T2 reviewers).

**Steps**:

1. Spawn the appropriate reflection agent via `Task`:
   - UC-1 → `requirements-analyst` (or `root-cause-analyst` for risk-heavy plans). Agent receives the Wave 1 grounding, the Wave 2 coverage matrix, and `refs/reflection-card-template.md`.
   - UC-2 → `self-review` (cheapest "did we finish" pass for narrow scope) OR `root-cause-analyst` (when deviation_count > 0). The selector is in `refs/tier-rubric.md` §Agent-Selection-T1.
2. The agent produces one reflection card at `<output-dir>/tier1-card.md` with: verdict (PASS|PARTIAL|FAIL), per-row coverage assessment, identified gaps, identified deviations (UC-2), risks, confidence self-report, "if I'm wrong it's probably because…".
3. Spawn `confidence-calibrator` via `Task` with `card_path=<output-dir>/tier1-card.md`, `rubric_path=<skill-dir>/refs/tier-rubric.md`, `card_tier=1`, `output_path=<output-dir>/tier1-calibration.md`. Calibrator does NOT see formation context (anchoring reduced, not eliminated).
4. If calibrated confidence < 0.85 AND `tier_planned == 1` AND `--no-escalate` not set → upgrade `tier_planned` to 2; record `retro_escalation: confidence_below_floor` in audit.

**Fallback rule**: if `confidence-calibrator` agent crashes/times out, inline-calibrate against `refs/tier-rubric.md` and mark `calibration: inline-fallback`. If the reflection agent itself crashes, fall back to inline orchestrator reflection against `refs/reflection-card-template.md` and mark `tier1_source: inline-fallback`. The skill never aborts on agent failure during T1.

**Exit criteria**: T1 card written, calibration written (or inline-fallback marked). Emit "Wave 3 complete: confidence=<x> retro_escalate=<bool>".

**Token budget**: ≤ 6k Claude tokens (excluding the agent subprocess).

### Wave 4 — Tier 2 Parallel Heterogeneous Reviewers

**Goal**: Reduce single-model anchoring by running 2-3 reviewers in parallel on heterogeneous model classes, each with the T1 card visible (so they can agree, extend, or disagree).

**Preconditions**: `tier_planned ≥ 2`. Skipped entirely on T1-only path.

**Reviewer selection** (canonical in `refs/tier-rubric.md` §Reviewer-Matrix):

| Mode | Default reviewer set (N=3) | N=2 fallback (when budget tight) |
|------|----------------------------|-----------------------------------|
| pre  | `requirements-analyst`, `system-architect`, `quality-engineer` | drop `system-architect` |
| post | `rf-qa` (structural), `rf-qa-qualitative` (content), `root-cause-analyst` (deviations) | drop `rf-qa-qualitative` |

**Model rotation**: per `sc-brainstorm-protocol` pattern, rotate across `--models` (default `opus, sonnet, haiku`). For `--depth deep` prefer opus for the first reviewer. The third reviewer (when present) runs on a third model class — explicitly heterogeneous to satisfy the research finding that cross-vendor/cross-model representational diversity outperforms intra-vendor stacks.

**Steps**:

1. Materialize per-reviewer brief packages — each gets: the reference contract, the work artifact, the Wave 2 coverage matrix (both .md and .json), the Wave 1 grounding artifacts, the T1 card, and `refs/reflection-card-template.md`. Write to `<output-dir>/reviewer-briefs/reviewer-<N>.md` for audit.
2. Spawn N reviewers in parallel via `Task` (single message, multiple Task calls). Each agent's `adversarial_stance: true` and `fix_authorization: false` (per memory `feedback_rfqa_adversarial_pattern.md` for rf-qa specifically). Each produces a reflection card at `<output-dir>/tier2-reviewer-<N>-card.md`.
3. **MCP enrichment runs in parallel with reviewer spawn** in the same turn:
   - `mcp__context7__query-docs` when the reference contract names a framework/library and Wave 1 hit `degraded`.
   - `mcp__tavily__tavily-search` (≤2 queries) for best-practice references when UC-1 plan validation needs external grounding. Delegated to `Skill tech-research` instead if `--depth deep`.
   - `mcp__serena__get_diagnostics_for_file` on every touched file (UC-2 only) — drops linter/type errors directly into the matrix.
4. Wait for all reviewers. Spawn `confidence-calibrator` per card in parallel (N more Task calls), each with `card_tier=2`, `output_path=<output-dir>/tier2-reviewer-<N>-calibration.md`.
5. Compute disposition: if all N cards converge on the same verdict and the same top-3 findings (≥66% Jaccard overlap on finding text), tag `consensus`; otherwise tag `competing`.

**Exit criteria**: N reviewer cards + N calibration reports written, disposition recorded. Emit "Wave 4 complete: reviewers=<N> disposition=<consensus|competing>".

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| One reviewer fails | Continue with remaining; record in audit | If < 2 succeed, downgrade to T1 + warn |
| MCP enrichment fails | Skip enrichment for that source; mark `degraded` in audit | None |
| All reviewers converge | Skip Wave 5 (adversarial merge unnecessary); proceed to Wave 6 with consensus card | None |
| All reviewers diverge with no overlap | Proceed to Wave 5; warn `no_strong_consensus` | None |

**Token budget**: ≤ 25k Claude tokens for 3 reviewers, ≤ 17k for 2.

### Wave 5 — Tier 2 Merge via sc:adversarial-protocol

**Goal**: Delegate debate/scoring/merge to the canonical skill. This skill does NOT re-implement any of it.

**Preconditions**: Wave 4 disposition is `competing` OR `--depth deep` (force debate even on consensus, for transparency).

**Steps**:

1. Materialize each tier-2 reviewer card as a standalone candidate verdict file at `<output-dir>/candidate-verdicts/verdict-<N>.md` — self-contained (problem framing, verdict, evidence, risks, proposed actions). Append a `## Coverage Matrix Reference` section embedding the Wave 2 matrix verbatim so debate is matrix-aware (mirrors sc:troubleshoot's doc-context embed trick — no new flag needed on sc:adversarial).
2. Invoke `Skill sc:adversarial-protocol` in Mode A:

```
Skill sc:adversarial-protocol with
  --compare verdict-1.md,verdict-2.md[,verdict-3.md]
  --depth <quick|standard>  (quick if N=2, standard if N=3)
  --focus correctness,coverage,risk
  --convergence <user-passed or 0.75 default>
  --output <output-dir>/adversarial/
```

3. Consume the return contract from sc:adversarial:
   - Empty-response guard: empty/unparseable response → FAIL Wave 5
   - Partial-parse guard: structured but `convergence_score` missing → fallback 0.5 ONLY IF `merged_output_path` exists on disk
   - Missing-file guard: `merged_output_path` must exist before status routing
4. Route on `convergence_score`:
   - ≥ 0.75 → PASS: copy `merged_output_path` to `<output-dir>/merged-verdict.md`
   - ≥ 0.60 → PARTIAL: copy with frontmatter `merge_status: partial`; surface unresolved-conflicts list
   - < 0.60 → FAIL: emit "Reviewers diverged irreconcilably. Re-run with narrower scope or --depth deep." Set final `status: failed`. Skip Wave 6+ (verdict cannot be trusted).
5. Fallback protocol F1/F2/F3 from sc:brainstorm pattern: F1 retry once with reduced depth; F2 abort + emit error; F3 write `<output-dir>/reflect-failed.md` with partial state.

**Exit criteria**: `merged-verdict.md` produced (PASS|PARTIAL) or run terminated. Emit "Wave 5 complete: convergence=<x> status=<PASS|PARTIAL|FAIL>".

### Wave 6 — Evidence Validation

**Goal**: Re-ground every `file:line` citation in the current best verdict (T1 card on T1-only path, merged-verdict on T2 path). Non-negotiable last gate before any actionable recommendation ships.

**Steps**:

1. Identify the verdict file to validate (T1 card OR merged-verdict).
2. Spawn `evidence-validator` via `Task` with `report_draft_path=<verdict>`, `evidence_section_locator="## Evidence"` (and `## Coverage`, `## Deviations`), `output_path=<output-dir>/evidence-validation.md`, `allow_command_reexec=false`. The agent Reads every cited file:line and drops mismatches.
3. **Citation re-grounding budget policy**: for cards with ≤ 20 citations re-Read all. For cards with > 20 citations, re-Read every HIGH-stakes citation (those tied to `regression` or `drift` rows) plus a random 30% sample of the rest, AND spawn `audit-validator` for a parallel 10% spot-check (per sc-troubleshoot Tier 3 pattern). Surface dropped citations as `Grounding Gaps` in the final report.
4. Apply verdict: remove dropped citations from the verdict file. If any were dropped, set return-contract `status: partial`.
5. **Confidence-check gate** — before emitting any actionable recommendation in Wave 7, invoke `Skill confidence-check` against the post-validation verdict. ≥0.90 → emit recommendation; 0.70-0.89 → emit with explicit alternatives surfaced; <0.70 → emit "needs user input" with the open questions. Per CLAUDE.md global rule 3.

**Fallback**: if `evidence-validator` fails, inline-validate citations in the orchestrator and mark `validator: inline-fallback`. Never ship without validation.

**Exit criteria**: post-validation verdict at `<output-dir>/verdict-validated.md`. Emit "Wave 6 complete: citations_dropped=<N> status=<success|partial>".

### Wave 7 — Synthesis + Report + Return Contract

**Goal**: Produce one final report at `<output-dir>/REPORT.md`, one return-contract YAML, and the chat summary.

**Refs**: load `refs/report-template.md` (UC-1 variant + UC-2 variant).

**Steps**:

1. Compose `REPORT.md` with sections:
   - Header (mode, tier reached, confidence, escalation reason, convergence score)
   - Summary (2-4 sentences)
   - Coverage Matrix (rendered from Wave 2)
   - Verdict (PASS|PARTIAL|FAIL) with reasoning
   - UC-1: Gaps, Risks, Best-Practice Compliance (cite tech-research findings when invoked)
   - UC-2: Deviation Classification (4-cell taxonomy), Unauthorized Drift list, Regression list
   - Evidence (every claim cited file:line, post-validation)
   - Alternative Verdicts Considered (T2 only — losing reviewer cards summarized)
   - Recommended Next Actions (filtered by confidence-check)
   - Grounding Gaps (any dropped citations, degraded MCPs, fallbacks used)
2. Persist memory: `mcp__serena__write_memory` with key `reflection/last-pass-{project-slug}` and key `reflection/deviation-patterns/{project-slug}` (UC-2 only, accumulating patterns over runs). 90-day expiry per validate-roadmap convention. Fail-open.
3. Append audit-log footer:

```
<!-- SC:REFLECT:SUMMARY
mode: pre | post
status: success | partial | failed | dry-run
tier_reached: 1 | 2 | 3
confidence_calibrated: <float>
convergence_score: <float|null>
coverage_pct: <float>
drift_count: <int>
regression_count: <int>
citations_validated: <N>
citations_dropped: <N>
recommendation_count: <N>
duration_sec: <N>
-->
```

4. Write `<output-dir>/return-contract.yaml` (§5).
5. Surface chat summary: 1-paragraph verdict, REPORT.md path, top 3 actionable items, tier reached + confidence, suggested next move (paste-ready per memory `feedback_suggestions_include_prompts.md`).

**Exit criteria**: REPORT.md, return-contract.yaml, memory persisted (or fail-open), chat summary delivered. If `--fix` not set OR mode=pre OR verdict=PASS, STOP and return contract.

### Wave 8 — Tier 3 Remediation Handoff (opt-in)

**Preconditions**: `--fix` set AND `mode == post` AND verdict ∈ {PARTIAL, FAIL} AND user explicitly accepts.

**Steps**:

1. Present remediation offer (template in `refs/remediation-handoff.md`). One yes/no question. Wait.
2. On accept:
   - **Phase A — Build the task file**: invoke `Skill task-builder` with BUILD_REQUEST: GOAL = "Remediate deviations identified in `<REPORT.md>`"; WHY = the Verdict summary; WHERE = each `regression` / `drift` row's cited file(s); TEMPLATE = `bugfix-template` when regressions present, `feature-template` otherwise.
   - **Phase B — Execution gate**: do NOT auto-execute. Surface the task file path and literal command (`/task <path>`) the user can run. Stop here.
3. On decline: return success; report stands.

**Exit criteria**: task file path returned (or decline recorded). Return-contract finalized.

## 5. Return Contract (versioned)

Written to `<output-dir>/return-contract.yaml` AND returned inline as Skill response. Two blocks: stable + telemetry.

### Stable Contract (`contract_version: 1.0`)

```yaml
contract_version: "1.0"
mode: pre | post
status: success | partial | failed | dry-run
tier_reached: 1 | 2 | 3
verdict: PASS | PARTIAL | FAIL
confidence_calibrated: <float 0.0-1.0>
convergence_score: <float 0.0-1.0> | null   # null on T1-only
coverage_pct: <float 0.0-1.0>
drift_count: <int>                           # UC-2 only; 0 for UC-1
regression_count: <int>                      # UC-2 only; 0 for UC-1
report_path: <abs-path>
audit_log_path: <abs-path>
coverage_matrix_path: <abs-path>
merged_verdict_path: <abs-path> | null       # null on T1-only
adversarial_artifacts_dir: <abs-path> | null # null on T1-only
tier2_reviewer_card_paths: [<path>, ...]     # empty on T1-only
escalation_reason: <string> | null
grounding_quality_tier: primary | fallback_1 | fallback_2
citations_dropped: <int>
recommendations: [{action: <string>, confidence: <float>, target_file: <path>|null}, ...]
asymmetric_flags:
  blocked_by_low_confidence: <bool>          # true if confidence-check gated all recs to <0.70
  spec_is_wrong: <bool>                      # UC-2: code is correct, spec doesn't match reality
  user_decision_required: <bool>             # convergence < threshold and no auto-route
task_file_path: <abs-path> | null            # T3 only
remediation_offered: <bool>
remediation_accepted: <bool>
```

### Telemetry Block (`telemetry_version: 1.0`, non-stable)

```yaml
wave_durations_ms:
  wave_0: <ms>
  wave_1: <ms>
  wave_2: <ms>
  wave_2_5: <ms>
  wave_3: <ms>
  wave_4: <ms>
  wave_5: <ms>
  wave_6: <ms>
  wave_7: <ms>
  wave_8: <ms>
token_usage:
  orchestrator: <est>
  reviewers_total: <measured>
  adversarial_total: <from sc-adversarial contract>
reviewer_models: [<model alias>, ...]
mcp_degradations: [{server: <name>, wave: <int>, reason: <string>}]
agent_fallbacks: [{agent: <name>, wave: <int>, reason: <string>}]
memory_keys_written: [<key>, ...]
```

**Composability**: the stable block is intentionally shaped to be consumed by `/sc:task` (post-execution gating), `/sc:pm` (PDCA D-Phase reflection), and CI pipelines (`status` + `verdict` + `regression_count` are sufficient for a pass/fail gate). The asymmetric flags (`spec_is_wrong`, `user_decision_required`) directly mirror sc:troubleshoot's pattern so downstream automation can short-circuit without parsing prose.

## 6. Tier-Decision Rubric Reference

Canonical rubric lives in `refs/tier-rubric.md` (loaded on demand in Wave 2.5 and Wave 3). The rubric defines:

- The 9 scope/complexity signals in §4 Wave 2.5 (depth flag, coverage, drift, regression, scope size, multi-domain, degraded grounding, retro-escalation, dependency on external docs)
- Numeric thresholds: coverage 0.95/0.80, drift 3, regression 1, diff 1000 LOC, confidence 0.85, convergence 0.75/0.60
- Reviewer matrix per mode (UC-1: requirements-analyst + system-architect + quality-engineer; UC-2: rf-qa + rf-qa-qualitative + root-cause-analyst)
- T1 agent selector (UC-1 → requirements-analyst; UC-2 narrow → self-review; UC-2 with deviations → root-cause-analyst)
- The retro-escalation rule (T1 → T2 when calibrated confidence drops below floor)

The rubric is data, not code. It is consumed by the orchestrator AND by `confidence-calibrator` (which re-grades cards against it independently).

## 7. Modern Serena Tool Usage

This skill explicitly does NOT use the legacy `think_about_*` triad. The deprecated/under-leveraged thinking tools are replaced by concrete symbolic + diagnostic operations:

| Legacy reflection moment | Modern Serena replacement | Wave |
|--------------------------|---------------------------|------|
| `think_about_task_adherence` | `find_symbol` + `find_referencing_symbols` on every contract-named symbol; diff against actual touched symbols from `git diff` | Wave 1 + Wave 2 |
| `think_about_collected_information` | `get_symbols_overview` on contract-named files + `list_memories` for session/project context | Wave 1 |
| `think_about_whether_you_are_done` | `get_diagnostics_for_file` on every touched file + Wave 2 coverage matrix + tasklist checkbox completion rate | Wave 2 + Wave 4 |

Per the research (`enrichment/research-deep.md` §1.2), the `think_about_*` tools are CURRENT (not deprecated) but under-leveraged. This skill treats them as optional scripted checkpoints — they MAY be wired into the T1 agent's brief as "if the agent finishes its card and want a meta-cognition pass, it may call `think_about_whether_you_are_done`" — but the load-bearing reflection logic lives entirely on the symbolic surface. The deprecated single-file island in `commands/reflect.md` is replaced wholesale.

**Fail-open policy**: every Serena call is fail-open per `sc-validate-roadmap-protocol`. Missing Serena → fall back to Grep/Glob, log degraded mode, keep going.

**Memory keying convention** (per validate-roadmap): every memory key includes a project slug to avoid cross-project contamination. Keys:

- `reflection/last-pass-{project-slug}` — most recent verdict summary
- `reflection/deviation-patterns/{project-slug}` — accumulated UC-2 drift/regression patterns (90-day TTL)
- `reflection/false-positives/{project-slug}` — verdicts the user explicitly overrode (learning signal)

## 8. Cross-Skill Integration

| Skill / agent | Invoked in | Purpose | What gets passed |
|---------------|------------|---------|------------------|
| `Skill sc:adversarial-protocol` (Mode A) | Wave 5 | Merge N reviewer verdicts; debate + score + merge | `--compare verdict-1.md,verdict-2.md,verdict-3.md` + matrix embed |
| `Skill task-builder` | Wave 8 | Generate MDTM remediation task file | BUILD_REQUEST citing REPORT.md regressions/drift |
| `Skill confidence-check` | Wave 6 | Gate every recommendation before emission | post-validation verdict |
| `Skill tech-research` | Wave 4 (depth=deep) | External best-practice + framework doc lookup | reference contract framework/library names |
| `confidence-calibrator` agent | Wave 3 + Wave 4 | Independent re-grading against rubric | each card + `refs/tier-rubric.md` |
| `evidence-validator` agent | Wave 6 | Re-ground every file:line citation | verdict draft |
| `rf-qa` agent (adversarial_stance=true, fix_authorization=false) | Wave 4 UC-2 | Structural QA partition over diff | per-reviewer brief package |
| `rf-qa-qualitative` agent | Wave 4 UC-2 | Content-level QA on artifacts | per-reviewer brief package |
| `root-cause-analyst` agent | Wave 4 (deviations present) | Investigate why a deviation happened | drift/regression rows from matrix |
| `requirements-analyst` agent | Wave 3 + Wave 4 UC-1 | Spec → plan coverage analysis | reference contract + plan |
| `quality-engineer` agent | Wave 4 UC-1 | Edge-case + risk surfacing on plans | plan + matrix |
| `system-architect` agent | Wave 4 UC-1 (cross-component) | Cross-component coherence check | full grounding + matrix |
| `self-review` agent | Wave 3 UC-2 narrow | Cheap "did we finish" T1 default | grounding + tasklist |
| `audit-validator` agent | Wave 6 (citation count > 20) | 10% spot-check sample | sampled citations |

Every delegation passes through the existing return contract / brief format of the target — this skill does not invent new payload shapes for sub-skills.

## 9. Agent Delegation Map

**Reusable (no new agents required for v1)**:

- `confidence-calibrator` — Wave 3 + Wave 4 (per-card re-grading)
- `evidence-validator` — Wave 6 (citation re-grounding)
- `rf-qa` + `rf-qa-qualitative` — Wave 4 UC-2 (structural + content QA)
- `root-cause-analyst` — Wave 3 UC-2 (deviation investigation) + Wave 4 (cross-domain hypothesis)
- `requirements-analyst` — Wave 3 + Wave 4 UC-1
- `quality-engineer` — Wave 4 UC-1
- `system-architect` — Wave 4 UC-1 (cross-component)
- `self-review` — Wave 3 UC-2 narrow
- `audit-validator` — Wave 6 spot-check
- `refactoring-expert` — optional Wave 4 reviewer when scope includes refactor-heavy changes

**Proposed NEW agents (defer to v1.1 unless adversarial debate insists)**:

- `coverage-mapper` — extracts requirements/tasklist atoms and computes the Wave 2 matrix. Rationale for inline-orchestrator instead: the matrix logic is mechanical (regex + classification) and lives more readably as an inline wave than as a separate agent that re-reads context. **Decision: keep inline in Wave 2 for v1**; promote to agent only if Wave 2 logic bloats beyond ~150 lines.
- `deviation-classifier` — classifies UC-2 deviations into the 4-cell taxonomy. Same rationale: classification rules are mechanical given the matrix + diff + task log. **Decision: keep inline in Wave 2 step 4 for v1**.

The discipline: NEW agents are justified only when (a) the prompt context needs to stay narrower than the orchestrator's, (b) the work is iterative/back-and-forth, OR (c) the work parallelizes across N instances. Matrix computation fails all three tests. Reviewers (which DO parallelize across N) reuse existing agents.

## 10. Eval Rubric

**Location**: `.dev/eval-workspaces/sc-reflect/` (per CLAUDE.md plugin override — NEVER `.claude/skills/sc-reflect-protocol-workspace/`).

**Workspace layout** (mirroring `sc-brainstorm` per `enrichment/codebase-context.md` §4):

```
.dev/eval-workspaces/sc-reflect/
├── SPEC.md
├── grader.py                       # extends sc-brainstorm's grader.py with citation_resolves + grep_regex
├── aggregate_iteration.py
├── evals/
│   └── evals.json                  # pilot 3 cases, expanding to 12+
├── iterations/
│   ├── iteration-1/                # 3 pilot cases
│   └── iteration-2/                # 12 cases, depth + tier + mode variation
└── skill-snapshot/
    └── reflect-v1.md               # frozen commands/reflect.md baseline for A/B
```

**Pilot eval matrix (iteration-1, 3 cases)**:

1. UC-1 small (single-file plan, narrow scope) — expect T1 PASS
2. UC-2 small-diff (one tasklist, <300 LOC diff, no deviations) — expect T1 PASS
3. UC-2 large-diff (multi-file diff, deliberate seeded drift) — expect T2 PARTIAL/FAIL

**Expansion matrix (iteration-2, 12 cases)**: cross `mode × depth × tier × scope_kind`:

- modes: pre, post
- depths: quick, standard, deep
- tier expectations: 1, 2, 3
- scope kinds: narrow-single-file, mid-multi-file, broad-multi-domain

**Rubric dimensions (6, all 0-5 per Anthropic 2026 grading-scale paper for highest human-LLM ICC)**:

| Dimension | What it measures | Threshold to ship |
|-----------|------------------|-------------------|
| Citation accuracy | every file:line claim resolves; no fabricated lines | ≥ 4.0 average |
| Coverage completeness | matrix correctly maps every R-NNN to its P/D-NNN counterpart | ≥ 4.0 average |
| Deviation-classification precision | UC-2 4-cell taxonomy assignments match human gold-label | ≥ 4.0 average (only on UC-2 cases) |
| Tier-decision correctness | Wave 2.5 routes to expected tier per seeded scope | ≥ 4.5 average (rubric is mechanical, expect high) |
| Recommendation actionability | every recommendation has a target file + concrete next step | ≥ 3.5 average |
| Best-practice compliance | UC-1 recommendations cite external references when framework/library is named | ≥ 3.5 average (only on UC-1 cases naming a framework) |

**Acceptance thresholds (per the research §5.5)**:

- Tier 1 fast-path: ≥80% assertion pass rate, <5s wall-clock for orchestrator portion (excludes agent subprocesses)
- Tier 2 multi-agent: ≥90% assertion pass rate, debate transcript shows real disagreement-then-convergence (not echo chamber)
- Iteration acceptance: ship at iteration N if iteration N+1 vs N improvement is <5% absolute on held-out test set (Anthropic 60/40 train/test default)

**Grader assertion DSL extensions** (extending `sc-brainstorm/grader.py`):

- `citation_resolves` — every `path:line` reference in the verdict resolves to a real line in a real file (semantic, requires file I/O)
- `grep_regex` — section text matches a regex (mechanical pattern check, e.g., "Verdict: PASS|PARTIAL|FAIL appears in verdict section")
- `matrix_cells_classified` — coverage-matrix.json has no `unclassified` cells

**Judge model**: per the research §5.6, the grader MUST be a different (and typically more capable) model class than the model running the skill. If sc:reflect Tier 1 ran on Sonnet, grader runs on Opus. If Tier 2 ran heterogeneous Sonnet+Haiku+Qwen, grader runs Opus solo. This avoids positional bias (IJCNLP 2025 highest-impact bias) + self-enhancement bias.

## 11. Build Path Decision

**Pick: hybrid — skill-creator plugin for the draft/iterate loop, then sprint CLI for production execution against tasklists.**

**Rationale**:

- **Why NOT pure Sprint CLI**: Sprint CLI (`src/superclaude/cli/sprint/`) is the production execution path for a built skill, not a build path. It runs Claude Code as a subprocess against tasklists with phase gates, anti-instinct hooks, KPI tracking. That fits AFTER the skill stabilizes — it's the wrong tool for the eval-driven draft→test→rewrite loop.
- **Why NOT pure skill-creator**: skill-creator's iteration loop (`run_loop.py`, `eval-viewer/generate_review.py`, comparator/grader/analyzer sub-agents) is excellent for early-stage refinement BUT its default sibling-workspace location is forbidden by CLAUDE.md (PreToolUse hook redirects + `.gitignore` blocks commits). Workspace MUST land at `.dev/eval-workspaces/sc-reflect/`.
- **Why hybrid wins**: use skill-creator (with workspace forcibly redirected to `.dev/eval-workspaces/sc-reflect/`) for iterations 1-3 of the draft+eval+improve loop. The sc-brainstorm workspace's `grader.py` pattern is the deterministic assertion gate — copy it, extend it with `citation_resolves` + `grep_regex` + `matrix_cells_classified`. Once eval scores stabilize at the §10 thresholds, freeze the skill, ship a tasklist that exercises it across real reflection tasks, and run that tasklist via `superclaude sprint run` to validate at production scale. The `superclaude eval` CLI (`src/superclaude/cli/eval/`) is deferred to v1.1 — it's PTY-isolated infrastructure-scale eval, overkill for v1.

**Build sequence**:

1. Author `src/superclaude/skills/sc-reflect-protocol/SKILL.md` + `refs/` (this document is the v1 draft).
2. Author `src/superclaude/commands/reflect.md` as a thin entrypoint that calls `Skill sc:reflect-protocol`.
3. Snapshot the legacy `src/superclaude/commands/reflect.md` (current 112-line file) to `.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md` as the A/B baseline.
4. Build the 3 pilot evals in `.dev/eval-workspaces/sc-reflect/iterations/iteration-1/`.
5. Run `make sync-dev` → `make verify-sync`. Run iteration-1 via skill-creator's `run_loop.py` (workspace redirected).
6. Iterate to ≥80% on iteration-1 assertions.
7. Expand to iteration-2 (12-case matrix). Iterate to ≥90% on T2 cases, ≥80% on T1.
8. Freeze v1.0.0. Ship.
9. Post-ship: author a real reflection tasklist + `superclaude sprint run` it against real PRs in IronbellyOrg/IronClaude to validate production behavior.

## 12. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Empty input (no contract + no scope) | STOP with usage hint | None |
| Mode auto-detection fails | STOP asking user for `--mode` | None |
| Reference contract unparseable (no recognizable structure) | STOP with parser error + first-100-char preview | None |
| `sc:adversarial-protocol` skill missing | STOP with install instruction | None |
| `task-builder` missing on `--fix` request | STOP requiring user to choose alternate handoff | None |
| All MCPs unavailable | Run `--no-mcp` mode; warn user that grounding is degraded; native tools only | None |
| Auggie unavailable (others OK) | Fall back to Serena + Grep/Glob; mark grounding `fallback_1` | None |
| Serena unavailable (others OK) | Fall back to Grep/Glob; mark grounding `fallback_2`; skip diagnostics step | None |
| Wave 4 reviewer subprocess fails | Continue with remaining reviewers; if <2 succeed, downgrade to T1 + warn in report | None |
| All Wave 4 reviewers fail | Downgrade to T1 result; report `partial`; recommend rerun with smaller scope | None |
| `sc:adversarial` returns empty/unparseable | FAIL Wave 5 (no synthetic 0.5 fallback) | None |
| `sc:adversarial` returns missing convergence_score, valid merged_output_path | PARTIAL with 0.5 fallback + warning | Continue to Wave 6 |
| `sc:adversarial` `merged_output_path` non-existent | FAIL (file guard before status routing) | None |
| `sc:adversarial` convergence < 0.60 | FAIL Wave 5; final status `failed`; skip Wave 6+ | None |
| `evidence-validator` fails | Inline-validate citations in orchestrator; mark `validator: inline-fallback`; set status `partial` | None |
| `confidence-calibrator` fails for any card | Inline-calibrate against rubric; mark `calibration: inline-fallback`; never block escalation on missing calibration | None |
| `confidence-check` returns <0.70 on all recommendations | Surface recommendations as "needs user input"; do NOT auto-emit | User clarifies, rerun |
| Memory write fails (Serena down) | Fail-open; skip persistence; log degraded | None |
| `--output` under `.claude/skills/`/`.claude/agents/`/`.claude/commands/` | STOP with output-policy violation message | None (mirrors sc-adversarial guard) |
| Mid-Wave-4 token usage > 1.25 × estimate | Hard abort with partial-state preservation at `<output-dir>/reflect-failed.md` | `--resume-from` to retry |
| User declines Wave 8 remediation offer | Return success; report stands | None |

## 13. Token Cost Profile

| Tier reached | Auggie tokens (offloaded) | Claude tokens (orchestrator + agents) | Wall clock |
|--------------|---------------------------|----------------------------------------|------------|
| T1 only (UC-1 narrow) | ~2-4k | ~5-9k | 1-3 min |
| T1 only (UC-2 small-diff) | ~3-6k | ~6-11k | 2-4 min |
| T2 (no adversarial — consensus) | ~8-18k | ~20-40k | 4-8 min |
| T2 (with adversarial) | ~12-25k | ~40-80k | 8-15 min |
| T3 added | +0 | +20-40k (task-builder) | +5-10 min |

These are targets. Heavy retrieval is offloaded to auggie (free / low-cost tier). Claude tokens are the constrained resource. Wave 2.5's rubric exists specifically to keep T1-only on the common case inside the 6-11k Claude band.

## 14. Refs

| File | When loaded |
|------|-------------|
| `refs/tier-rubric.md` | Wave 2.5 (tier decision) + Wave 3 (calibration) |
| `refs/coverage-matrix-template.md` | Wave 2 |
| `refs/deviation-taxonomy.md` | Wave 2 step 4 (UC-2 only) |
| `refs/reflection-card-template.md` | Wave 3 + Wave 4 (per-reviewer brief) |
| `refs/report-template.md` | Wave 7 |
| `refs/remediation-handoff.md` | Wave 8 |

Each ref is loaded only by the wave that needs it. Do not pre-load.

## 15. Will Do / Will Not Do

**Will**:

- Auto-detect UC-1 vs UC-2 from input shape; respect `--mode` override
- Always run grounding (Wave 1) + coverage matrix (Wave 2) before tier decisioning
- Decide tier via rubric, never by user-typed depth alone
- Run T1 even when T2 is planned (T1 output feeds T2 reviewers)
- Spawn 2-3 heterogeneous reviewers on different model classes for T2
- Delegate ALL debate/scoring/merge to `Skill sc:adversarial-protocol` Mode A
- Re-ground every `file:line` citation via `evidence-validator` before any recommendation ships
- Gate every actionable recommendation through `confidence-check` (≥0.90 / 0.70-0.89 / <0.70)
- Persist learning via `mcp__serena__write_memory` with project-slug-keyed keys
- Write source-of-truth at `src/superclaude/skills/sc-reflect-protocol/`; eval workspace at `.dev/eval-workspaces/sc-reflect/`

**Will Not**:

- Re-implement debate, scoring, base-selection, refactor-plan, or merge logic (delegated to sc-adversarial)
- Use the legacy `think_about_*` Serena triad as load-bearing reflection logic
- Author NEW agents for v1 (coverage-mapper, deviation-classifier — deferred unless adversarial debate insists)
- Auto-execute Tier 3 task files — `/task <path>` is always user-initiated
- Auto-commit after T3 — sc:reflect post-validation is a separate user-initiated invocation
- Apply code changes (only emits reports + handoff task files; never edits production code)
- Silently downgrade on missing handoff skills (STOPs and asks user)
- Trust agent-reported confidence without `confidence-calibrator` re-grading (or inline fallback)
- Ship a verdict whose citations haven't passed `evidence-validator`
- Write any artifact under `.claude/skills/`/`.claude/agents/`/`.claude/commands/` (output-policy guard)
- Use `--no-verify` or pivot to bypass freshness/sync hooks (per memory `feedback_no_strategy_pivot_to_avoid_hooks.md`)

## 16. Spec Reference

Full spec at `.dev/eval-workspaces/sc-reflect/SPEC.md` (to be authored from this draft + the seed-brief + the adversarial-merged variant). This SKILL.md is the working protocol; the spec is the design rationale + acceptance criteria + frozen test cases.
