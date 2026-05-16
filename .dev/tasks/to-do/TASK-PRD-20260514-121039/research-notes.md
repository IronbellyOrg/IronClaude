# Research Notes: Unified /sc:task — Post-Merger Feature PRD (v3.75 RigorflowMerger)

**Date:** 2026-05-14
**Scenario:** A (explicit request: PRD derived from existing RELEASE-SPEC.md)
**Tier:** Lightweight (target 400–800 lines, 2–3 codebase agents, 0 web agents)
**PRD Scope:** Feature PRD
<!-- Feature PRD: S5 (Business Context) abbreviated; S8 (Value Proposition Canvas) SKIPPED per Lightweight tier; S9 (Competitive Analysis) ABBREVIATED (reference Platform PRD); S17 (Legal/Compliance) abbreviated to feature-specific data handling; S18 (Business Requirements) abbreviated to feature-specific cost notes; S22 (Customer Journey Map) SKIPPED per Lightweight; S25 (API Contract Examples) SKIPPED per Lightweight; Appendices SKIPPED per Lightweight first version; Document History SKIPPED per Lightweight first version. -->

**Status:** Complete

---

## EXISTING_FILES

### Primary input artifacts (already produced; PRD draws from these — no fresh exploration needed)

All under `/config/workspace/IronClaude/.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/`:

| Artifact | Purpose | Key content |
|----------|---------|-------------|
| `RELEASE-SPEC.md` (~865 lines + Sev-2 edits) | Canonical release spec for v3.75 | §1.2 verdict matrix (18 candidates), §2 surface contract, §3 protocol changes, §4 naming, §5 test strategy, §6 backward compat & risk, §7 release split (R1+R2 sibling), §8 open questions, §9 acceptance criteria, §10 coverage notes, §11 validation history, Annexes B+C (R3 reference designs) |
| `FINAL-REPORT.md` (11 sections) | Decision-traceable merged report | §1 Scope, §2 Source index, §3 task-unified inventory, §4 /sc:task inventory, §5 Overlap matrix (47 rows), §6 Best-of-breed candidates (13), §7 Risks (18+3), §8 Open questions (14), §9 Prior-art constraints, §10 Shared assumptions (A-001..A-005), §11 TUI Improvement Bundle |
| `context-task-current-state.md` | R7 snapshot of current /sc:task surface | All 8 flags, classification header sentinel, tier rules (STRICT/EXEMPT/LIGHT/STANDARD priority), MCP requirements per tier, TFEP gates, sprint+cleanup_audit integrations |
| `context-task-unified-current-state.md` | R8 snapshot of historical task-unified strengths + v3.7 prior-art | Why no live /sc:task-unified exists, v3.7 N1-N12 rename evidence, lingering carry-overs (sentinel + `--caller task-unified`), tasklist tier-classification.md drift |
| `TUI-ANALYSIS.md` | TUI investigation report | Root-cause diagnosis (per-task path bypasses OutputMonitor; Duration column reads `stall_seconds`; double truncation at 60 chars); 10 proposals P-01..P-10 |
| `TUI-ADVERSARIAL.md` | Top-5 TUI proposals with viability + risks | P-01, P-05, P-02, P-03, P-07; ship order "fireworks landing"; mandatory mitigations (reset-test, INV-004 audit, ANSI pass, layering correction) |
| `wave1-extracts.md` | Verbatim quotes from 6 backlog source files | Sprint-executor comparison + improve + strategy; task-unified-tier comparison + improve + strategy |
| `analyze-report.md` | Wave-4 architectural review | 0 Sev-1, 4 Sev-2, 4 Sev-3 issues; verdict APPROVE WITH NOTES |
| `checkpoint2-reflection.md` | /sc:reflect --type session output | Coverage 11/11; traceability 5/5 spot-checks; verdict PROCEED TO WAVE 3 |
| `checkpoint3-completion.md` | /sc:reflect --type completion output | Section coverage 11/11; flag inventory PASS; TUI top-5 PASS; Sev-2 4/4 PASS; verdict RELEASE-SPEC COMPLETE |

### Live code surface that the PRD describes (post-merger state)

| Path | Role | Purpose in PRD |
|------|------|----------------|
| `src/superclaude/commands/task.md` | Command frontmatter + classification + tier rules | S6 JTBD, S7 personas (invokers), S12 scope, S14 technical req, S16 UX req |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | Skill protocol: per-tier execution, MCP block, TFEP gates | S14 tech req, S20 risk, S21 impl plan |
| `src/superclaude/skills/sc-task-protocol/__init__.py` | Skill registration | S14, S15 |
| `src/superclaude/cli/sprint/process.py` | `ClaudeProcess.build_prompt()` emits `/sc:task Execute all tasks ...` | S11 dependencies, S14 tech req |
| `src/superclaude/cli/sprint/executor.py` | Sprint executor; SE-001 fail-closed; SE-002+003 UID + sub-phase resume; SE-004 ExecutionMode; SE-005 GateFailureSeverity | S14, S20 risks, S21 impl plan |
| `src/superclaude/cli/sprint/tui.py` | TUI rendering (target of TUI top-5 fixes) | S16 UX req, S23 error handling, S24 user interaction |
| `src/superclaude/cli/sprint/monitor.py` | OutputMonitor (target of P-01 keystone fix) | S16, S23 |
| `src/superclaude/cli/sprint/config.py` | Phase config + extraction-time truncation (P-03 fix target) | S16 |
| `src/superclaude/cli/sprint/models.py` | `phase_started_at` + MonitorState (target of P-02 fix) | S14 |
| `src/superclaude/cli/cleanup_audit/prompts.py` | 5 cleanup-audit prompt builders emitting `/sc:task` | S11 dependencies |
| `src/superclaude/core/COMMANDS.md:86-119` | Full flag inventory reference | S12, S14 |
| `src/superclaude/core/ORCHESTRATOR.md:151-213` | Tier classification decision tree | S14 |
| Future: `src/superclaude/skills/sc-task-protocol/audit.py` | NEW in v3.75: audit log foundation + CriticalFailCondition dataclass | S14 tech req, S20 risk (RK-NEW-4/6) |

### Existing PRD stub or template
- Template (schema): `src/superclaude/examples/prd_template.md` (28 numbered sections + Document Info + Completeness Status + Appendices)
- **No existing PRD stub** at `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/PRD.md` — will be created fresh.
- No existing PRD at `docs/docs-product/tech/sc-task/` (output destination per user is the release-artifacts folder, not docs/).

---

## PATTERNS_AND_CONVENTIONS

- **Canonical command surface invariant (v3.7 hard constraint):** `/sc:task` is the only canonical name. No live `/sc:task-unified`. Carry-over strings (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`, `--caller task-unified`) preserved verbatim until A-005 forensic-consumer audit clears them in R3.
- **Tier-first dispatch (orthogonal axes):** Strategy × Compliance. Compliance auto-classifies via priority order STRICT > EXEMPT > LIGHT > STANDARD with confidence scoring; <0.70 → BLOCKED (new in v3.75) requires explicit re-invocation.
- **Skill split:** command performs classification (TEXT-ONLY, no tool use); skill performs execution (STANDARD/STRICT only); LIGHT/EXEMPT execute directly without Skill invocation.
- **MCP requirements by tier (post-merger formalized):** STRICT requires Sequential + Serena (NO fallback). STANDARD requires Sequential + Context7 (fallback allowed). LIGHT/EXEMPT none.
- **CRITICAL FAIL conditions (new, STRICT-only):** MCP missing → FAIL; output absent after max_turns → FAIL; classification header absent → FAIL.
- **Audit log (new, Q11):** `audit.py` writes daily-rotated JSONL; CriticalFailCondition dataclass lives there.
- **Sprint→task contract:** Sprint executor emits `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic`.
- **TUI render conventions:** `rich.Live(refresh_per_second=2)`; per-task path is the modern path (vs freeform). Post-P-01 wiring, `OutputMonitor` runs on per-task path.
- **Test baseline (regression boundary):** 921 passed / 57 failed sprint suite; 125/125 TUI Waves 1-2 + tmux + summarizer + retrospective; 16/16 `test_process.py::TestClaudeProcess`.
- **Naming consolidation guard:** canonical-form-agnostic preservation tests (existence + structure only, no literal substring) so R3 rename remains a constant-only change.

---

## FEATURE_ANALYSIS

Post-merger /sc:task surfaces these features:

1. **Auto-classification with confidence scoring** (existing — preserved) — 4-tier priority STRICT > EXEMPT > LIGHT > STANDARD, keyword + context boosters + compound overrides.
2. **BLOCKED state for low-confidence** (NEW, TU-004) — additive TIER enum value; deterministic halt; explicit re-invocation required.
3. **CRITICAL FAIL conditions for STRICT** (NEW, TU-001) — three conditions enforce unconditional failure.
4. **Six universal quality principles NFR** (NEW, TU-003) — Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy. Bound to STANDARD/STRICT verification agents.
5. **Mandatory completion checklist** (NEW, TU-007 — gated on LW-source verification) — STRICT/STANDARD tasks must satisfy canonical conditions before returning `complete`.
6. **Audit log infrastructure** (NEW, Q11) — `audit.py` module + daily-rotated JSONL.
7. **TFEP test-failure escalation** (existing — preserved) — prohibits ad-hoc fixes; `/sc:forensic` invocation tiers.
8. **STRICT MCP circuit breaker** (existing — preserved) — STRICT blocks on Sequential+Serena unavailability.
9. **Sprint runtime fail-closed gate** (NEW, SE-001) — empty output → `(False, 'empty output file')` instead of soft PASS.
10. **Per-task UID + sub-phase resume** (NEW, SE-002+SE-003 paired) — stable `task_uid: f"{phase_id}-{task_index:04d}"`; `--start N` resumes at first non-DONE task within phase.
11. **ExecutionMode enum** (NEW, SE-004) — NORMAL / INCOMPLETE_RESUME / CORRECTION.
12. **GateFailureSeverity enum** (NEW, SE-005) — SEV1_BLOCK / SEV2_CYCLE / SEV3_ADVISORY (Q9 (c) maps TFEP → Sev).
13. **TUI improvements** (NEW, P-05 + P-02 + P-03+P-07 + P-01) — spinner, elapsed-since-phase-start Duration, width-aware truncation, OutputMonitor on per-task path.

Deferred (not in v3.75; documented in PRD as "Future / Out of scope"):
- TU-002 output-type axis (R3)
- TU-005 SoT YAML (R3)
- TU-006 skill sub-files (R3)
- Q1 sentinel rename (R3, gated on A-005)
- Q2 forensic-caller rename (R3, gated on A-005)
- SE-006 auto-diagnostic threshold (R4, gated on RK-OOS-3)
- P-04, P-06, P-08, P-09, P-10 TUI proposals (next waves)

---

## RECOMMENDED_OUTPUTS

| Output | Path |
|--------|------|
| Research notes (this file) | `.dev/tasks/to-do/TASK-PRD-20260514-121039/research-notes.md` |
| R-01 features + user flows | `.dev/tasks/to-do/TASK-PRD-20260514-121039/research/01-features-and-user-flows.md` |
| R-02 architecture + integration | `.dev/tasks/to-do/TASK-PRD-20260514-121039/research/02-architecture-and-integration.md` |
| R-03 sprint runtime + TUI UX | `.dev/tasks/to-do/TASK-PRD-20260514-121039/research/03-sprint-and-tui-ux.md` |
| Synthesis 01 — features/UX template sections | `.dev/tasks/to-do/TASK-PRD-20260514-121039/synthesis/synth-01-features-ux.md` |
| Synthesis 02 — architecture/dependencies template sections | `.dev/tasks/to-do/TASK-PRD-20260514-121039/synthesis/synth-02-architecture.md` |
| Synthesis 03 — sprint/TUI template sections | `.dev/tasks/to-do/TASK-PRD-20260514-121039/synthesis/synth-03-sprint-tui.md` |
| Gaps & questions log | `.dev/tasks/to-do/TASK-PRD-20260514-121039/gaps-and-questions.md` |
| QA: research gate | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/qa-research-gate-report.md` |
| Analyst: completeness | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/analyst-completeness-report.md` |
| Analyst: synthesis review | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/analyst-synthesis-review.md` |
| QA: synthesis gate | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/qa-synthesis-gate-report.md` |
| QA: report validation (post-assembly) | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/qa-report-validation.md` |
| QA: qualitative review (post-assembly) | `.dev/tasks/to-do/TASK-PRD-20260514-121039/qa/qa-qualitative-review.md` |
| **FINAL PRD (canonical)** | `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/PRD.md` |

---

## SUGGESTED_PHASES

### Phase 1: Preparation
- Confirm Feature PRD scope, Lightweight tier.
- Read prd_template.md (28-section schema).
- Confirm RELEASE-SPEC.md, FINAL-REPORT.md, both context-*.md, TUI-ANALYSIS.md, TUI-ADVERSARIAL.md exist and are current.
- Verify no existing PRD stub at `artifacts/PRD.md`.

### Phase 2: Deep Investigation (3 parallel codebase agents)

**R-01 — Feature inventory + user flows (Feature Analyst)**
- Inputs: `artifacts/RELEASE-SPEC.md`, `artifacts/FINAL-REPORT.md`, `artifacts/context-task-current-state.md`
- Live code: `src/superclaude/commands/task.md`, `src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/superclaude/core/COMMANDS.md`, `src/superclaude/core/ORCHESTRATOR.md`
- Produces: full feature inventory, user invocation flows for each tier (STRICT/STANDARD/LIGHT/EXEMPT/BLOCKED), invoker personas (sprint executor, cleanup-audit, end user), classification header schema, scope statement, success metrics.
- Output: `research/01-features-and-user-flows.md`
- Synthesis sections: S6 JTBD, S7 Personas, S10 Assumptions, S12 Scope, S13 Open Questions, S16 UX Req, S19 Success Metrics.

**R-02 — Architecture + integration surfaces (Architecture Analyst)**
- Inputs: `artifacts/RELEASE-SPEC.md` §§2-3, `artifacts/FINAL-REPORT.md` §6, `artifacts/context-task-current-state.md`
- Live code: `src/superclaude/commands/task.md`, `src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/superclaude/cli/sprint/process.py`, `src/superclaude/cli/cleanup_audit/prompts.py`, future `audit.py` spec from RELEASE-SPEC §3.3
- Produces: command-skill split, audit.py contract (CriticalFailCondition + JSONL daily-rotated), MCP requirements matrix per tier (with circuit breaker semantics), TFEP/forensic invocation flow, sprint + cleanup-audit integration surfaces, dependency graph, technology stack.
- Output: `research/02-architecture-and-integration.md`
- Synthesis sections: S11 Dependencies, S14 Technical Req, S15 Tech Stack, S17 Legal/Compliance (abbreviated to audit log + data handling), S20 Risk Analysis, S21 Implementation Plan, S26 Contributors.

**R-03 — Sprint runtime + TUI UX post-merger (UX Investigator)**
- Inputs: `artifacts/RELEASE-SPEC.md` §1.2 SE rows + §5.4 + §7.1.1, `artifacts/TUI-ANALYSIS.md`, `artifacts/TUI-ADVERSARIAL.md`
- Live code: `src/superclaude/cli/sprint/executor.py`, `tui.py`, `monitor.py`, `config.py`, `models.py`
- Produces: SE-001..005 behavioral change inventory; TUI top-5 acceptance criteria + ship order; error/edge cases (empty output, missing checkpoint, TUI hang, prompt cut-off, partial result resume); user interaction patterns (RUNNING spinner, Duration column, width-aware truncation).
- Output: `research/03-sprint-and-tui-ux.md`
- Synthesis sections: S16 UX Req, S23 Error Handling & Edge Cases, S24 User Interaction & Design, S20 Risk (TUI-specific risks RK-TUI-01..05), S21 Implementation Plan (TUI sub-section).

### Phase 3: Completeness Verification (parallel: rf-analyst + rf-qa)
- rf-analyst completeness check across R-01/02/03 → `qa/analyst-completeness-report.md`
- rf-qa research-gate evidence quality check → `qa/qa-research-gate-report.md`
- Address any blocking gaps before Phase 4.

### Phase 4: Web Research (SKIPPED — 0 web agents at Lightweight tier; internal feature with sufficient internal context)

If gaps surface during R-01..R-03 that require external context (e.g., comparison to industry CI/CD task-tiering, market context for STRICT/STANDARD verification overhead), spawn 1 web research agent. **Default: skip.**

### Phase 5: Synthesis + Analyst + QA Synthesis Gate
- 3 synthesis agents (parallelizable) consume research → produce template-aligned sections.
- rf-analyst synthesis review + rf-qa synthesis gate (parallel).

### Phase 6: Assembly
- rf-assembler produces `artifacts/PRD.md` from synthesis files + prd_template.md schema.
- rf-qa report-validation (structural).
- rf-qa-qualitative review (content-level: scoping, flow, realism, contradictions, audience appropriateness).

### Phase 7: Present to User & Complete Task
- Deliver `artifacts/PRD.md`.
- Move task file to `.dev/tasks/done/`.
- Offer companion docs (TDD, tech reference) per project convention.

---

## TEMPLATE_NOTES

**Use Template 02 (Complex Task)** — multi-phase work with parallel agents, QA gates, conditional flows. Confirmed by the skill's guidance: "For PRD creation, the answer is almost always Template 02."

Skip per Lightweight tier (first version of PRD): S8 Value Proposition Canvas, S22 Customer Journey Map, S25 API Contract Examples, Appendices, Document History.

Abbreviate per Feature PRD (vs Platform PRD): S5 Business Context, S9 Competitive Analysis, S17 Legal/Compliance, S18 Business Requirements. Add a single-sentence pointer to a future Platform PRD for full coverage.

Embed in BUILD_REQUEST: tier=Lightweight; scope=Feature PRD; output path; explicit "skip web research at Lightweight" guidance; explicit list of 13 features for synthesis-mapping cross-validation; explicit list of 28 template sections with which to MAP / SKIP / ABBREVIATE per row.

---

## AMBIGUITIES_FOR_USER

None — intent is clear from the user's three answers (Feature PRD post-merger, output path `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/PRD.md`, Lightweight tier). All major scope decisions are resolved upfront.

**Notes (informational, not blocking):**
- TU-007 canonical condition list is `[inference]` in RELEASE-SPEC §3.6 KNOWN GAP. PRD will document the placeholder six-condition list with the same `[inference]` tag.
- TU-004 behavioral break impact "5-10% of `--compliance auto` users" is `[inference]` (no telemetry). PRD will preserve the tag.
- Carry-over sentinel rename (Q1/Q2) is DEFER-GATED on A-005. PRD will document the carry-over and the deferral, NOT propose a rename.
- All [inference] tags in the RELEASE-SPEC propagate into the PRD.
