---
spec_source: spec-cross-framework-deep-analysis.compressed.md
generated: 2026-06-03T02:08:52+00:00
generator: sc-roadmap-requirements-extractor
functional_requirements: 8
nonfunctional_requirements: 6
total_requirements: 14
complexity_score: 0.85
complexity_class: HIGH
domains_detected: [infrastructure, backend, devops, quality-engineering, documentation, architecture]
risks_identified: 10
dependencies_identified: 8
success_criteria_count: 14
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 128.0, started_at: "2026-06-03T02:08:52.066953+00:00", finished_at: "2026-06-03T02:11:00.084288+00:00"}
---

## Functional Requirements

The spec defines 8 top-level functional requirements under feature `FR-XFDA-001`, each mapped to a sprint phase. IDs used verbatim from the spec. "Routes/paths" for this infrastructure spec are CLI invocations and artifact file paths (no HTTP endpoints exist); preserved verbatim where present.

| ID | Title | Phase | Key Acceptance Criteria | Paths / Routes (verbatim) |
|---|---|---|---|---|
| FR-XFDA-001.1 | Updated IronClaude Component Inventory | Phase 1 | All 8 IC component groups inventoried; each entry has verified file paths + interfaces + internal dependencies + extension points; no component without Auggie MCP evidence; component map with ≥8 IC→LW mappings; IC-only components annotated | `artifacts/inventory-ironclaude.md`, `artifacts/component-map.md`; repo `/config/workspace/IronClaude` |
| FR-XFDA-001.2 | llm-workflows Component Inventory (Stable Reference) | Phase 1 | `inventory-llm-workflows.md` produced from known list in `artifacts/prompt.md`; Auggie verification query confirms paths; any missing path flagged + annotated | `artifacts/inventory-llm-workflows.md`, `artifacts/prompt.md`; repo `/config/workspace/llm-workflows` |
| FR-XFDA-001.3 | Per-Component Strategy Extraction (Both Frameworks) | Phases 2 & 3 | IC strategy docs for all 8 groups; LW strategy docs for all 11 components; every strength paired with weakness/cost; all claims backed by file:line Auggie evidence; LW docs note rigorous AND bloated/slow/expensive | `artifacts/strategy-ic-{component}.md` (×8), `artifacts/strategy-lw-{component}.md` (×11) |
| FR-XFDA-001.4 | Cross-Framework Adversarial Comparison | Phase 4 | Minimum 8 comparison pairs debated (enumerated below); each cites file:line from both repos; each produces clear verdict with conditions; "adopt patterns not mass" verified per pair | `artifacts/comparison-{pair}.md` (×8); uses `/sc:adversarial` |
| FR-XFDA-001.5 | Merged Strategy Synthesis | Phase 5 | Covers all Phase 4 component areas; explicit "rigor without bloat" section; "patterns not mass" applied + documented per adopted pattern; discard decisions justified; internally consistent | `artifacts/merged-strategy.md` |
| FR-XFDA-001.6 | Prioritized Improvement Plan | Phase 6 | Per-component plans for all 8 IC groups; each item has file path(s) + change + why + priority (P0–P3) + effort (XS–XL) + dependencies + acceptance criteria; `improve-master.md` has dependency graph; risk per item; new-code vs strengthen-existing distinguished | `artifacts/improve-{component}.md` (×8), `artifacts/improve-master.md` |
| FR-XFDA-001.7 | Adversarial Validation of Improvement Plan | Phase 7 | Pass/fail per item; all file paths verified via Auggie; scope-creep check vs "patterns not mass"; missing-connection check (Phase 5→6); corrected final plan produced | `artifacts/validation-report.md`, `artifacts/final-improve-plan.md` |
| FR-XFDA-001.8 | Artifact Assembly and Consolidated Outputs | Phase 8 | `artifact-index.md` links all artifacts; end-to-end traceability (Phase 1 component → strategy → comparison → merged → improvement); no orphans/dead refs; rigor assessment + sc:roadmap-compatible backlog + sprint summary | `artifacts/artifact-index.md`, `artifacts/rigor-assessment.md`, `artifacts/improvement-backlog.md`, `artifacts/sprint-summary.md` |

**FR-XFDA-001.4 comparison pairs (sub-decomposition, from §3 and §4.5):**
| Sub-ID | Pair |
|---|---|
| FR-XFDA-001.4a | roadmap fidelity/certify/remediate gates vs PABLOV + quality-gates |
| FR-XFDA-001.4b | task-unified tier system vs pipeline-orchestration + task-builder |
| FR-XFDA-001.4c | sprint CLI executor vs automated-qa-workflow |
| FR-XFDA-001.4d | adversarial-pipeline vs anti-sycophancy system |
| FR-XFDA-001.4e | pm-agent (confidence/reflexion/self-check) vs anti-hallucination + failure-debugging |
| FR-XFDA-001.4f | quality-agents vs agent-definitions (rf-*) |
| FR-XFDA-001.4g | pipeline-analysis (FMEA/guards/invariants) vs quality-gates + PABLOV (structural) |
| FR-XFDA-001.4h | cleanup-audit-cli vs automated-qa-workflow (audit dimension) |

**Implicit functional behaviors (folded into above, not separately counted):** strict-sequential phase-gate enforcement that halts on missing artifact (FR-XFDA-001.8 / §5.3 / Test §8.3); sprint restart from any phase gate via `--start` (also NFR-XFDA.5); incremental artifact writes for crash resilience (§7).

## Non-Functional Requirements

IDs verbatim from §6. Count = 6 (top-level FR count is 8 — the .4a–.4h are sub-decompositions, not counted).

| ID | Requirement | Target | Measurement |
|---|---|---|---|
| NFR-XFDA.1 | All code-reading tasks use Auggie MCP as primary tool | 100% compliance | R-RULE-01 checkpoint per phase |
| NFR-XFDA.2 | Anti-sycophancy: every strength has a paired weakness | 100% of strength claims | Checkpoint scan per phase |
| NFR-XFDA.3 | All file:line citations verifiable | 100% of citations | Auggie verification in Phase 7 |
| NFR-XFDA.4 | "Adopt patterns not mass" verified for every llm-workflows adoption | 100% of adoption items | Phase 6 + Phase 7 checkpoints |
| NFR-XFDA.5 | Sprint restartable from any phase gate | `--start` flag works | CLI executor resume |
| NFR-XFDA.6 | `improvement-backlog.md` directly consumable by `/sc:roadmap` | Schema compliance | Phase 8 validation |

NFR domain coverage: maintainability/process-integrity (NFR-1,2,4), correctness/verifiability (NFR-3), reliability/resilience (NFR-5), interoperability/schema (NFR-6). No explicit performance/latency or security NFRs (analysis sprint, no production code — see §9).

## Complexity Assessment

**complexity_score: 0.85 — complexity_class: HIGH** (matches spec frontmatter `complexity_score: 0.85 / complexity_class: high`).

Scoring rationale:
- **Breadth (high):** 8 sequential phases producing 35+ artifacts across two repositories (`/config/workspace/IronClaude`, `/config/workspace/llm-workflows`); 19 components compared (8 IC + 11 LW) over 8 adversarial pairs.
- **Orchestration coupling (high):** strict sequential phase-gate contract — each phase gated on prior checkpoint pass; Phases 2/3 parallelizable but both gate Phase 4; cascade risk from a bad Phase 1 inventory.
- **Tooling dependency (high):** hard dependency on Auggie MCP for evidence with a degraded Serena+Grep/Glob fallback; integrates `/sc:adversarial`, sprint CLI, and downstream `/sc:roadmap` + `/sc:tasklist`.
- **Verification burden (high):** 100%-coverage NFRs (citation verifiability, anti-sycophancy pairing, "patterns not mass") demand per-phase checkpoint scans plus a dedicated adversarial validation phase.
- **Mitigating factors (lowers from ~0.9):** zero production code change, no breaking changes, trivial rollback (delete artifacts dir), and a stable (frozen) llm-workflows reference reducing one repo's discovery cost.

Net: deep multi-phase analytical orchestration with strong rigor gates but low blast radius → 0.85 HIGH.

## Architectural Constraints

- **AC-1 Execution model mandate:** sprint must run via the IronClaude sprint CLI with strict-sequential phase gates (no interactive/manual process). (§2.1)
- **AC-2 Scope boundary — IC side:** comparison limited to the quality-enforcement layer (8 named component groups); non-quality commands (brainstorm, design, document, explain, estimate, git, index, load, save, review-translation) are out of scope. (§1.2, §2.1)
- **AC-3 Scope boundary — LW side:** llm-workflows treated as a frozen reference; no re-survey beyond path verification, no implementation changes. (§1.2, §2.1)
- **AC-4 "Adopt patterns not mass" R-RULE:** adopt control logic / validation patterns, never bash/shell implementation machinery; enforced at every checkpoint and in Phase 7. (§2.1, Appendix A)
- **AC-5 Anti-sycophancy R-RULE:** every claimed strength requires a documented paired weakness/cost. (§2.1)
- **AC-6 Evidence mandate (R-RULE-01):** Auggie MCP is the primary code-reading tool; no hallucinated paths; file:line citations required and later verified. (§3, §6)
- **AC-7 Phase-gate contract:** `enforcement: strict_sequential`; no phase starts until prior checkpoint passes; checkpoint format is a pass/fail table per criterion. (§5.3)
- **AC-8 Dual artifact strategy:** produce both the multi-doc traceable set and the consolidated rigor-assessment + improvement-backlog pair. (§2, §2.1)
- **AC-9 Downstream schema contract:** `improvement-backlog.md` must conform to `improvement_backlog_schema` for `/sc:roadmap` ingestion; `final-improve-plan.md` feeds `/sc:tasklist`. (§5.3, §10)
- **AC-10 Restartability:** artifacts written incrementally; sprint resumable via `--start`. (§6, §7, NFR-5)

## Component Inventory

### IronClaude components (scope-bounded, §4.5)
| ID | Name | Source path | Role | Dependencies | Source ref |
|---|---|---|---|---|---|
| COMP-001 | roadmap-pipeline | `cli/roadmap/` (fidelity, remediate, certify, spec_patch, gates, executor) | Roadmap generation + fidelity/remediate/certify quality gates | gates, executor | §4.5 |
| COMP-002 | cleanup-audit-cli | `cli/cleanup_audit/` (gates, anti-lazy, evidence-gate, executor, prompts) | Multi-pass structural repo audit with evidence gates | executor, gates | §4.5 |
| COMP-003 | sprint-executor | `cli/sprint/` (tmux, TUI, KPI, diagnostics, process, logging) | Phase-gated sprint execution + resume | tmux, process, logging | §4.5, §5.1 |
| COMP-004 | pm-agent | `pm_agent/` (confidence, self_check, reflexion, token_budget) | Pre/post-execution confidence, validation, error learning | — | §4.5 |
| COMP-005 | adversarial-pipeline | `.claude/commands/sc/adversarial.md` + `skills/sc-adversarial-protocol/` | Structured adversarial debate/merge | — | §4.5 |
| COMP-006 | task-unified | `.claude/commands/sc/task-unified.md` + `skills/sc-task-unified-protocol/` | Tiered task execution + MCP compliance | — | §4.5 |
| COMP-007 | quality-agents | `agents/` (quality-engineer, root-cause-analyst, pm-agent, requirements-analyst) | Specialized quality/analysis agent definitions | — | §4.5 |
| COMP-008 | pipeline-analysis | `cli/pipeline/` (FMEA, guards, invariants, contracts, dataflow, conflict) | Structural pipeline analysis subsystem | — | §4.5 |
| COMP-009 | pablov (LW) | `.gfdoc/rules/core/ib_agent_core.md` | Programmatic Artifact-Based LLM Output Validation | — | §4.5, App. A |
| COMP-010 | automated-qa-workflow (LW) | `.gfdoc/scripts/automated_qa_workflow.sh` | Automated QA orchestration | — | §4.5 |
| COMP-011 | quality-gates (LW) | `.gfdoc/rules/core/quality_gates.md` | Structured quality gate rules | — | §4.5 |
| COMP-012 | anti-hallucination (LW) | `.gfdoc/rules/core/anti_hallucination_task_completion_rules.md` | Task-completion anti-hallucination rules | — | §4.5 |
| COMP-013 | anti-sycophancy (LW) | `.gfdoc/rules/core/anti_sycophancy.md` + `RISK_PATTERNS_COMPREHENSIVE.md` | 12-pattern risk scoring / anti-sycophancy | — | §1.1, §4.5 |
| COMP-014 | dnsp-protocol (LW) | `.gfdoc/docs/guides/RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md` | Detect-Nudge-Synthesize-Proceed batch recovery | — | §4.5, App. A |
| COMP-015 | session-management (LW) | `.gfdoc/scripts/session_message_counter.sh` + `rollover_context_functions.sh` | Session/context rollover management | — | §4.5 |
| COMP-016 | input-validation (LW) | `.gfdoc/scripts/input_validation.sh` | Input validation | — | §4.5 |
| COMP-017 | pipeline-orchestration (LW) | `.claude/commands/rf/pipeline.md` | Pipeline orchestration command | — | §4.5 |
| COMP-018 | task-builder (LW) | `.claude/commands/rf/taskbuilder.md` | Task builder command | — | §4.5 |
| COMP-019 | agent-definitions (LW) | `.claude/agents/rf-*.md` | rf-* agent definitions | — | §4.5 |

### Data models / contracts
| ID | Name | Role | Fields | Source ref |
|---|---|---|---|---|
| DM-001 | improvement_backlog item | Machine-readable backlog row for `/sc:roadmap` ingestion | `id: string` (IC-{component}-{seq}); `component: string`; `title: string`; `priority: enum` (P0,P1,P2,P3); `effort: enum` (XS,S,M,L,XL); `pattern_source: string` (LW pattern or "IC-native"); `rationale: string`; `file_targets: list[string]`; `acceptance_criteria: list[string]`; `risk: string`; `patterns_not_mass_verified: bool` | §5.3 |
| DM-002 | phase_gate_contract | Phase-gate enforcement contract | `enforcement: strict_sequential`; `rule: no_phase_starts_until_prior_checkpoint_passes`; `checkpoint_format: table_with_pass_fail_per_criterion` | §5.3 |
| DM-003 | gate-criteria row | Per-phase gate definition (8 rows) | `phase`; `gate`; `min_artifacts: int`; `semantic_checks: string` | §5.2 |

## Risk Inventory

Risks 1–7 from §7 (probability × impact); R8–R10 from §12 gap analysis (severity).

1. **Auggie MCP unavailable for IronClaude repo** — Prob Low / Impact High → Mitigation: Serena `get_symbols_overview` + Grep/Glob fallback; note limitation in artifacts. **Severity: HIGH.**
2. **Auggie MCP unavailable for llm-workflows repo** — Low / High → same fallback; LW inventory partially known from `prompt.md`. **Severity: HIGH.**
3. **llm-workflows paths changed since `prompt.md`** — Medium / Medium → Phase 1 T01.02 verifies all LW paths; flag + annotate missing. **Severity: MEDIUM.**
4. **Comparison pairs produce inconclusive verdicts** — Medium / Medium → require explicit "no clear winner" verdict with rationale rather than forcing a conclusion. **Severity: MEDIUM.**
5. **Phase 6 plans drift into implementation mass** — Medium / High → "patterns not mass" R-RULE at checkpoint + Phase 7 adversarial check. **Severity: HIGH.**
6. **Sprint crashes mid-phase (as in original run, exit -9)** — Low / Medium → phase-gate checkpoints enable `--start` resume; incremental artifact writes. **Severity: MEDIUM.**
7. **IC component inventory incomplete (fast-moving codebase)** — Medium / Medium → broad Auggie queries; Phase 7 cross-checks all file refs. **Severity: MEDIUM.**
8. **GAP-1: LW path validity not pre-verified — could waste Phase 1 effort** — affects FR-XFDA-001.2; mitigated by Phase 1 T01.02. **Severity: MEDIUM.**
9. **GAP-2: no explicit handling for a "discard both" comparison verdict feeding Phase 6** — affects FR-XFDA-001.6; accepted: "discard both" is a valid Phase 5 outcome documented as "no adoption; why." **Severity: LOW.**
10. **GAP-3: `improvement-backlog.md` schema unvalidated by existing test tooling** — affects §5.3/§8; accepted risk, manual review in Phase 8. **Severity: MEDIUM.**

## Dependency Inventory

External dependencies, services, and integration points (count = 8):

1. **Auggie MCP** — primary code-reading/evidence tool for both repos (R-RULE-01, NFR-1,3); hard dependency with fallback. (§3, §6, §7)
2. **Serena MCP** — fallback discovery (`get_symbols_overview`) when Auggie unavailable. (§7)
3. **Grep/Glob tooling** — secondary fallback for code discovery. (§7)
4. **superclaude sprint CLI executor** — runs the phase-gated sprint; provides `--start/--end` resume + `--permission-flag`. (§5.1, COMP-003)
5. **`/sc:adversarial`** — adversarial debate engine used in Phase 4 comparisons. (FR-XFDA-001.4)
6. **`/sc:roadmap`** — downstream consumer of `improvement-backlog.md` (v3.0 roadmap). (§10, NFR-6)
7. **`/sc:tasklist`** — downstream consumer of `final-improve-plan.md` for implementation sequencing. (§10)
8. **External repositories** — `/config/workspace/IronClaude` (target) and `/config/workspace/llm-workflows` (frozen reference). (§1, §4.5)

Reference inputs (not runtime deps): `artifacts/prompt.md` (LW component list / stable reference), `.dev/releases/backlog/2.25-roadmap-v5/v2.25-spec-merged.md` (rigor-gap evidence), `src/superclaude/examples/release-spec-template.md` (spec template). (Appendix B)

## Success Criteria

Measurable criteria (count = 14): 8 phase gates (§5.2) + 6 NFR targets (§6).

**Phase gates (§5.2) — sprint halts if any criterion fails:**
1. Phase 1: `component-map.md` produced; ≥3 artifacts (2 inventories + map); ≥8 cross-framework mappings; ≥8 IC components; ≥11 LW components.
2. Phase 2: all 8 `strategy-ic-*.md`; each has strength + weakness section.
3. Phase 3: all 11 `strategy-lw-*.md`; each has rigorous AND bloat/cost section.
4. Phase 4: all 8 `comparison-*.md`; each has verdict + file:line evidence.
5. Phase 5: `merged-strategy.md`; has "rigor without bloat" section; no component area orphaned.
6. Phase 6: 9 plans (8 component + master); each item has P-tier + effort + file path; "patterns not mass" verified.
7. Phase 7: `validation-report.md` + `final-improve-plan.md`; pass/fail per item; final plan corrects all failures.
8. Phase 8: 4 consolidated outputs (index + assessment + backlog + summary); `improvement-backlog.md` is sc:roadmap-compatible.

**NFR targets (§6):** 9. Auggie primary 100%; 10. anti-sycophancy pairing 100%; 11. citation verifiability 100%; 12. "patterns not mass" verified 100% of adoptions; 13. `--start` resume works; 14. backlog schema-compliant for `/sc:roadmap`.

**End-to-end success (§8.3):** full sprint produces all 35+ artifacts; phase-gate enforcement halts on a manually deleted required artifact with a clear error; 2 human-reviewed comparison docs each carry non-trivial verdicts with dual-repo file:line evidence; `improvement-backlog.md` ingests into `/sc:roadmap` without schema errors.

## Open Questions

From §11 (open items) plus extraction-surfaced ambiguities:

1. **OI-1:** Do llm-workflows paths in `prompt.md` still match the current repo? — Medium; resolved in Phase 1 execution (T01.02).
2. **OI-2:** Treat pipeline-analysis (FMEA/guards/invariants) as one component group or split into sub-components for comparison? — Low; affects comparison granularity; resolve before Phase 2. (Relates to COMP-008.)
3. **OI-3:** Does `FR-XFDA-001` need registration in an FR registry for v3.0 planning? — Low; administrative; resolve before roadmap generation.
4. **Extraction note:** §4.1 says artifacts land under `.dev/releases/current/cross-framework-deep-analysis/` but FR text cites bare `artifacts/...` paths — confirm the canonical artifact root before sprint launch.
5. **Extraction note:** "≥8 comparison pairs" vs exactly 8 enumerated (§3 / §4.5) — confirm whether additional ad-hoc pairs are permitted or 8 is the fixed set.
6. **Extraction note:** Counts of "35+ artifacts" (§8.3) are approximate; the deterministic per-phase minimums in §5.2 should govern gate enforcement.
