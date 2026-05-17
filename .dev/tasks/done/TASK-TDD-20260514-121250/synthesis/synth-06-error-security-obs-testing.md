# TDD §12–§15 — Error Handling, Security, Observability, Testing (synth-06)

**Status:** Complete
**Date:** 2026-05-14
**Component:** task-builder convergence release (FR-CONV.1 .. FR-CONV.6)
**Adaptation note:** This is an **internal agent-framework** change set — no
service, no network surface, no user data. §12–§15 are adapted accordingly:
"errors" are gate FAILs and halt verdicts; "security" is anti-inflation and
hidden-input integrity; "observability" is spawn-log + on-disk gate-report
inspection; "testing" is a synthetic-fixture catalogue keyed per FR. Sources:
research files 03/04/05/07/12/13 and `/qa/research-gate-consolidated.md`
(SC-1..SC-8). SC-4 (per-gate fix-cycle coupling) is discharged in §12.4;
SC-2 (DNSP partial-vs-all-fail) is discharged in §12.1/§12.3.

---

## §12 Error Handling & Edge Cases

This component has no exceptions in the runtime sense — every "error" is a
**gate FAIL**, a **halt verdict**, or a **degraded annotation** emitted into an
on-disk markdown report. The categories below classify each failure surface by
who experiences it (the agent under review, the orchestrator, or the human)
and how it recovers.

### §12.1 Error Categories

| Category | Examples | Agent Experience | Recovery |
|---|---|---|---|
| Structural defects (TB-Add-1..7) | Placeholder item ("TBD"/"TODO"/title-only), DAG cycle, granularity outlier, format mismatch, phase-header count drift | Task-Integrity gate FAILs with an item-ID-naming error (`rf-qa.md` 20-item checklist, items at `rf-qa.md:268-287`; FR-CONV.1 adds TB-Add checks here) | rf-task-builder fix-cycle re-generates the offending item |
| Advisory (TB-Add-2) | Item count outside the recommended bounds | `[ADVISORY]` annotation in the gate report; gate verdict is **not** affected — does NOT FAIL | None — informational only; surfaces in report for human awareness |
| Evidence-binding miss (TB-Add-8) | Bare `Context: src/foo` with no `:N` line anchor; resolves INV-015 | Task-Integrity gate FAILs with a TB-Add-8 error | rf-task-builder adds the `:line` anchor or a justified-absence note |
| Retry oscillation (FR-CONV.5) | `|F_{n+1}| >= |F_n|` (set fails to shrink) or a PASS@N→FAIL@N+1 flip on any item | Fix-cycle loop halts: `[HALT-MONOTONICITY] |F|=<n>` or the verbatim regression message (`research/12-fr5-retry-monotonicity.md` §2) | Manual review — loop exits as a halt verdict; no further QA gate invoked under that counter |
| Partition exhaust (FR-CONV.6) | One partition agent's escalation ladder exhausts (retry-2 / gap-fill-round-3) while ≥1 sibling partition succeeded | Synthetic-dnsp HIGH finding emits into that partition's output stream; N-1 partitions complete normally (`research/13-fr6-dnsp-synthetic.md` §3, §8) | Manual review per the synthetic finding's fixed `recommendation` field |
| All-agents-fail | Zero partitions succeeded across the cohort | No synthetic emits — masking guard; existing `rf-team-lead.md:417` escalation runs instead | 3 fix cycles per phase, then HALT-and-ask-user (`rf-team-lead.md:417`) |

**SC-2 discharge:** The last two rows are mutually exclusive by partition
success-count. Synthetic-dnsp fires **only** in the mixed-outcome regime
(≥1 success AND ≥1 exhaust); zero-success falls through to the
`rf-team-lead.md:417` HALT (`research/07-rf-team-lead-escalation.md` §5–§6).

### §12.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|---|---|---|
| Minimal BUILD_REQUEST (sparse fields) | FR-CONV.2 Execution Context header degrades to References-only | `test_execution_context_minimal_buildrequest` |
| No GOAL-baseline item present | rf-qa-qualitative emits `drift-axis-inactive` annotation; the drift axis is skipped, not marked N/A (Ban-N/A rule, `rf-qa-qualitative.md:93`) | `test_drift_axis_inactive_when_no_goal_baseline` |
| Synthetic-dnsp same dedup-key across cycles | Cross-cycle dedup recognised — NOT a regression (INV-012); prior verdict was FAIL not PASS (`research/13-fr6-dnsp-synthetic.md` §6) | `test_synthetic_dnsp_dedup_not_regression` |
| Fixture-populated `.dev/tasks/done/` (hidden input) | Structural output byte-identical to the empty-`done/` run (NFR-CONV.3) | `test_hidden_input_guard` |
| Sequencing inversion (PR-04 lands before PR-06) | INV-010 dynamic enumeration richens the rf-qa-qualitative checklist automatically once the FR-CONV.1 catalogue activates | `test_sequencing_PR06_before_PR04` |
| 3-cycle `|F| = 5, 5, 5` | Halt at cycle 2 with `[HALT-MONOTONICITY] |F|=5`; cycle 3 not attempted (`research/12-fr5-retry-monotonicity.md` §5) | 3-cycle monotonicity fixture |
| Item 3.2 PASS@1 / FAIL@2 | Halt at cycle 2 with the verbatim regression message, emitted BEFORE the monotonicity guard is consulted | regression fixture |
| Synthetic-dnsp same dedup-key cycles 1+2, other findings shrink | Loop proceeds to cycle 3 — no halt (synthetic counts once per dedup-key; `|F|` still shrinks via other findings) | dedup-no-regression fixture |

### §12.3 Graceful Degradation

| Component Failure | Degraded Experience | Communication |
|---|---|---|
| Execution Context header generation fails (FR-CONV.2) | Header degrades to References-only or is omitted entirely; TB-Add-7 still cross-validates whatever header content exists | rf-task-builder execution log |
| FR-CONV.3 passthrough block missing (Inherited Structural Verdict absent from spawn) | rf-qa-qualitative spawns without an inherited verdict; falls back to current behavior (independent verification only); INV-019 Self-Audit still fires, and the K-003 first-5-runs audit catches the omission | rf-qa-qualitative output report |
| Synthetic-dnsp emission fails inside an exhausted partition agent | The existing all-agents-fail escalation path (`rf-team-lead.md:417`) remains the backstop — a missing synthetic record degrades to the pre-FR-CONV.6 silent-abort behavior, which the HALT guard still catches | rf-team-lead log |

### §12.4 Retry & Recovery Strategies

**SC-4 discharge:** Per-gate fix-cycle limits live in `rf-task-builder.md` I16
(verified at `rf-task-builder.md:334-361` — research-gate 3 / synthesis-gate 2
/ report-validation 3 / task-integrity 2 / any qualitative gate 3), NOT in
`rf-qa.md` (which specifies only the global max of 3 at `rf-qa.md:311`). The
FR-CONV.5 monotonicity and regression halts layer **on top of** these caps and
trip earlier on pathological loops (`research/12-fr5-retry-monotonicity.md` §6).

| Error Type | Retry Strategy | Max Attempts | Backoff |
|---|---|---|---|
| Per-gate fix cycles | I16 per-gate caps (research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3) — `rf-task-builder.md:334-361` | Per-gate cap; terminal action HALT-and-escalate or Open-Questions per gate type | None (cycles run sequentially) |
| Monotonicity guard | If `|F|` shrinks strictly → continue; if `|F_{n+1}| >= |F_n|` → halt. Only consulted when `|F_n| > 0` (gate-PASS termination precedes it) | Per FR-CONV.5 — halt on first non-shrink | N/A |
| Regression detection | Strict — any PASS@N→FAIL@N+1 flip always halts; runs FIRST each cycle, precedence over monotonicity | 0 (halt immediately on detection) | N/A |
| All-agents-fail | `rf-team-lead.md:417` — invoke `/rf:pipeline` with a FIX request, max 3 cycles per phase, then HALT-and-ask-user | 3 | None |

**Composition order per cycle transition** (`research/12-fr5-retry-monotonicity.md`
§2, §6): (1) regression check → (2) monotonicity check → (3) hard-cap check →
(4) proceed to next cycle. No existing rule is removed; the new halts only add
earlier exit paths for the pathological cases. The four/seven separate retry
counters (RESEARCH_NEEDED, MALFORMED, and the five per-gate counters) are
**never collapsed** into shared monotonicity state — `F_n` is tracked per
fix-cycle counter.

---

## §13 Security Considerations

Minimal — this is an internal agent-framework change set with no network
surface, no authentication boundary, and no user data (NFR-CONV.5). The
"security" concerns that do apply are **integrity** concerns: keeping the
adversarial QA posture from being silently weakened, and keeping the build
deterministic against contaminating inputs.

### §13.1 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Anti-inflation rule weakened by FR-CONV.3 — agent cites the inherited structural verdict as evidence instead of doing its own semantic checks | Low | High | INV-019 mandatory Self-Audit listing per phase (`rf-qa-qualitative.md:183-187` pattern) forces a count of *own* verifications; the Prohibited-Behaviors floor at `rf-qa-qualitative.md:766-772` forbids "RELIANCE, not VERIFICATION"; K-003 first-5-runs audit confirms ≥1 semantic check beyond the inherited PASS |
| DNSP synthetic finding masks a real finding — looks like an ordinary fixable issue | Low | Low | Fixed `severity: HIGH` (non-overridable) guarantees gate-level visibility; synthetic findings emit *alongside* real findings, never in place of them (`research/13-fr6-dnsp-synthetic.md` §7 Negative criteria) |
| Hidden-input contamination — fixture-populated `.dev/tasks/done/` or stray files alter build output non-deterministically | Low | Medium | NFR-CONV.3 fixture test (`test_hidden_input_guard`) asserts byte-identical structural output regardless of `.dev/tasks/done/` contents |

### §13.2 Security Controls

| Control | Implementation | Verification |
|---|---|---|
| Input validation | BUILD_REQUEST schema validation performed by rf-task-builder before encoding any checklist items (mandatory-field handling) | Spawn-prompt grep against the generated task file |
| Anti-inflation enforcement | INV-019 Self-Audit listing required in every rf-qa-qualitative phase output; tool-engagement minimum (`rf-qa-qualitative.md:774-775`) — total Read+Grep+Glob calls must be ≥ TOTAL checklist items | K-003 first-5-runs audit + content QA review |
| Hidden-input guard | NFR-CONV.3 fixture test isolates `.dev/tasks/done/` as a non-input | Byte-diff of structural fields between populated-`done/` and empty-`done/` runs |
| Authentication | N/A — internal framework; no auth surface exists or is introduced | N/A |
| Authorization | N/A — internal framework; no privilege boundary exists or is introduced | N/A |

### §13.3 Sensitive Data Handling

N/A — no PII, no credentials, and no new data of any kind is collected,
stored, or transmitted (NFR-CONV.5). All artifacts are markdown task/QA files
written to `.dev/tasks/` under version control.

### §13.4 Data Governance & Compliance

N/A — internal developer tooling, no regulatory scope. No data-retention,
residency, or processing obligations apply to on-disk markdown artifacts in a
git-tracked repository.

---

## §14 Observability & Monitoring

Adapted: this component has no runtime service to monitor. The observability
surfaces are (a) the **spawn-log** the orchestrator writes for each subagent
invocation, (b) the **on-disk gate-output reports** in `${TASK_DIR}qa/` and
`${TASK_DIR}reviews/`, and (c) the **embedded YAML/markdown markers**
(`[HALT-MONOTONICITY]`, regression message, synthetic-dnsp block) that downstream
processes grep for.

### §14.1 Logging

| Log Type | Format | Destination | Retention |
|---|---|---|---|
| rf-task-builder execution log | Text appended to `### Execution Log` section inside `.dev/tasks/to-do/TASK-*/TASK-*.md` | On-disk per task | Indefinite (under git VCS) |
| rf-qa gate reports (4 phases) | Markdown reports per `rf-qa.md:316` Output Format — Research Gate, Synthesis Gate, Report Validation, Task Integrity | `.dev/tasks/to-do/TASK-*/qa/qa-{phase}-{partition-N-of-M}.md` | Indefinite (git) |
| rf-qa-qualitative reports (8 phases) | Markdown reports per `rf-qa-qualitative.md:675-714` Output Format — includes Items Reviewed table with new `Axis` column (FR-CONV.4) | `.dev/tasks/to-do/TASK-*/reviews/` (per Output Format `output_path` field) | Indefinite (git) |
| Synthetic-dnsp findings | Embedded structured block (JSON-or-block per PRD §14.1) inside the partition agent's QA report; five fixed fields + two dedup-control fields | On-disk inside the agent's normal output stream — same channel as real findings (`research/13-fr6-dnsp-synthetic.md` §3) | Indefinite (git) |
| Spawn logs (FR-CONV.6 evidence field) | Per-spawn capture of subagent stdout/stderr — canonicalised path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt` | On-disk | Indefinite (git) — referenced by synthetic-dnsp `evidence` field |

### §14.2 Metrics

These are **offline, post-merge metrics**, not live service metrics. They are
measured by grepping the on-disk reports across a representative set of
BUILD_REQUESTs (NFR-CONV.4: 5 representative BUILD_REQUESTs).

| Metric | Type | Source | Alert Threshold |
|---|---|---|---|
| `synthetic-dnsp emission count` | Counter | grep `"source: synthetic-dnsp"` across rf-analyst / rf-qa / rf-qa-qualitative outputs | >0 in production → human review of which partitions exhausted and why |
| `[HALT-MONOTONICITY] count` | Counter | grep `[HALT-MONOTONICITY]` in fix-loop execution logs | >50% of fix-cycle batches → upstream BUILD_REQUEST defect or systemic agent issue |
| `regression-halt count` | Counter | grep `Regression detected on Item` in fix-loop execution logs | >20% of fix-cycle batches → fix-cycle itself is introducing new defects |
| `Self-Audit coverage` (INV-019) | Gauge (fraction) | grep `## Self-Audit` in rf-qa-qualitative outputs; assert ≥1 semantic check beyond inherited verdict | <100% on the first 5 runs after FR-CONV.3 → K-003 audit-fail (block release) |
| `make verify-sync PASS rate` | Counter | CI step + commit hook | Any FAIL blocks the commit; threshold is 100% |

### §14.3 Tracing

N/A — the rf-* subagent stack is a **single-process spawning model** (no
distributed coordination). Each subagent runs in the same Claude Code session
under the Agent tool; there is no cross-process trace context to propagate.
Causality between spawn-events and gate-verdicts is recovered offline by
reading the execution log + spawn-log + gate-report chain in
`.dev/tasks/to-do/TASK-*/`.

### §14.4 Alerts

N/A in v3.9 (initial convergence release). Post-merge metrics are measured
offline on the 5 representative BUILD_REQUESTs per NFR-CONV.4. Live alerting
on the metrics above is out of scope and is deferred — there is no operations
team consuming alerts and no SLA on the offline framework artifacts.

---

## §15 Testing Strategy

The change set is **agent-instruction text** (skill SKILL.md + rf-* agent
`.md` files), not executable code paths. The test strategy is therefore
**synthetic-fixture-driven**: each FR-CONV.X acceptance criterion is verified
by a fixture that exercises the new instruction surface and asserts on a
grep-able / byte-diffable marker in the produced artifact.

### §15.1 Test Pyramid (adapted)

| Level | Coverage Target | Tools | Responsibility |
|---|---|---|---|
| Synthetic Fixtures (per-FR) | 100% AC coverage — every FR-CONV.X acceptance criterion has a fixture | Custom fixtures under the test directory (or `.dev/releases/current/task-builder-merge/state/`); `uv run pytest` | Engineering |
| Integration Tests (cross-FR composition) | INV-010 (dynamic enumeration) + INV-012 (cross-cycle dedup) + INV-019 (Self-Audit) composition paths | Custom multi-FR fixtures | Engineering |
| E2E Tests | Full A.1–A.11 task-builder pipeline on a realistic BUILD_REQUEST | Custom fixture BUILD_REQUEST fed through the whole pipeline | Engineering |
| Manual Audit | K-003 first-5-runs of rf-qa-qualitative after FR-CONV.3 lands — confirm anti-inflation rule not weakened | Human review | QA Lead |

### §15.2 Synthetic Fixture Catalogue (per FR-CONV.X)

| Fixture | FR | Verifies | Verdict / Assertion |
|---|---|---|---|
| `test_placeholder_tb_add_1` | FR-CONV.1 | TB-Add-1 fires on a "TBD"/"TODO"/title-only checklist item | TB-Add-1 emits an item-ID-naming error; gate FAILs |
| `test_dag_cycle_tb_add_4` | FR-CONV.1 | TB-Add-4 fires on a circular intra-/inter-phase dependency | TB-Add-4 emits; gate FAILs |
| `test_evidence_bound_tb_add_8` | FR-CONV.1 | TB-Add-8 fires on a bare `Context: src/foo` with no `:N` anchor (INV-015) | FAIL without anchor; with `Context: src/foo:42` it passes |
| `test_execution_context_full` | FR-CONV.2 | The 3-labeled-line Execution Context block is present in the generated MDTM task file | grep matches all 3 labeled lines |
| `test_execution_context_minimal_buildrequest` | FR-CONV.2 | Minimal/sparse BUILD_REQUEST degrades the header to References-only | grep matches the degraded References-only form |
| `test_execution_context_no_file_paths` | FR-CONV.2 | `grep -E "src/|/.*:[0-9]+"` against the header block returns zero (header carries no raw line-anchored paths) | grep returns 0 |
| `test_inherited_verdict_present` | FR-CONV.3 | `## Inherited Structural Verdict` block appears in the rf-qa-qualitative spawn prompt | grep matches the block header |
| `test_inherited_verdict_freshness_inv_002` | FR-CONV.3 | 2-cycle fixture — cycle-2 spawn shows the cycle-2 structural verdict, not a stale cycle-1 verdict | byte-diff of cycle-1 vs cycle-2 spawn prompts |
| `test_self_audit_inv_019` | FR-CONV.3 | rf-qa-qualitative output contains `## Self-Audit` with ≥1 documented semantic check beyond the inherited verdict | grep + content inspection |
| `test_dynamic_enumeration_inv_010` | FR-CONV.3 | When the FR-CONV.1 TB-Add catalogue grows, the rf-qa-qualitative checklist auto-richens to reference it | structural diff of the checklist before/after catalogue growth |
| `test_five_axes_overlay` | FR-CONV.4 | `## Five Adversarial Axes` header appears BEFORE the immutable 15-item task-qualitative checklist (`rf-qa-qualitative.md:527`) | grep ordering assertion |
| `test_axis_column_populated` | FR-CONV.4 | The Items Reviewed table (`rf-qa-qualitative.md:675-714`) carries a non-empty `Axis` value on every row | parse table, assert no empty `Axis` cell |
| `test_drift_axis_inactive_when_no_goal_baseline` | FR-CONV.4 | No GOAL-baseline item present → `drift-axis-inactive` annotation emitted (not N/A) | grep matches the annotation |
| `test_severity_floor_unweakened` | FR-CONV.4 | The rf-qa-qualitative severity floor (Critical Rule 6, `rf-qa-qualitative.md:789` — contradictions always IMPORTANT/CRITICAL) is unchanged | byte-diff of the Critical Rules block |
| `test_monotonicity_halt_F_5_5_5` | FR-CONV.5 | 3-cycle `|F| = 5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY] |F|=5`; cycle 3 not attempted | grep halt message + assert no cycle-3 log |
| `test_regression_halt_pass1_fail2` | FR-CONV.5 | Item 3.2 PASS@1 / FAIL@2 halts with the verbatim regression message, emitted BEFORE the monotonicity check | grep message + ordering assertion |
| `test_slow_shrink_continues` | FR-CONV.5 | `|F| = 5, 4` continues — strict shrink holds; the rejected X-003 slow-convergence threshold is NOT triggered | execution log shows cycle continues |
| `test_dnsp_twice_exhaust` | FR-CONV.6 | A partition fixture that times out twice emits a synthetic-dnsp finding with all 5 fixed fields (`severity`, `source`, `affected_range`, `evidence`, `recommendation`) | parse the YAML/block, assert all 5 fields populated |
| `test_dnsp_dedup_collapse` | FR-CONV.6 | Two identical-`dedup_key` synthetic findings collapse into one record with `found_n_times=2` | parse merged YAML, assert cardinality 1 + `found_n_times` |
| `test_dnsp_all_agents_fail_bypass` | FR-CONV.6 | Zero partitions succeeded → no synthetic emits; the existing `rf-team-lead.md:417` escalation activates instead | execution log shows HALT path, no synthetic block |
| `test_dnsp_does_not_serialize_cohort` | FR-CONV.6 + NFR-CONV.10 | On one partition's escalation exhaust, the N-1 sibling partitions continue concurrently to completion (parallel-research invariant / INV-021) | spawn-log timing — N-1 partitions overlap the exhausted partition's synthesis |
| `test_synthetic_dnsp_dedup_not_regression` | FR-CONV.5 + FR-CONV.6 + INV-012 | A synthetic finding with the same `dedup_key` in cycles 1+2 (other findings shrinking) proceeds to cycle 3 — no regression halt | execution log shows cycle 3 attempted |
| `test_hidden_input_guard` | NFR-CONV.3 | Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs the empty-`done/` baseline | byte-diff of structural fields |
| `test_sequencing_PR06_before_PR04` | INV-010 | If PR-04 (FR-CONV.3) lands before PR-06 (FR-CONV.1), out of the canonical order, dynamic enumeration still richens once the catalogue activates | structural assertion on the enriched checklist |
| `test_invariant_preservation_NFR_6_through_10` | NFR-CONV.6..10 | All 5 invariants (self-contained-item, strictly-additive, hidden-input, offline-metrics, parallel-research) preserved per the Negative Criteria | composite fixture exercising each invariant surface |

### §15.3 Test Environments

Local development via UV (`uv run pytest`, `uv run pytest tests/path/ -v`)
plus CI (GitHub Actions invoking `make test`). No external services, no
containers, no network — all fixtures are self-contained markdown inputs and
grep/byte-diff assertions. `make verify-sync` runs in CI to confirm
`src/superclaude/` and `.claude/` agree before the suite executes.

---

**Status:** Complete




