# Substantive Differences: `/sc:forensic` design vs `sc:troubleshoot` v2 bundle

**Mode**: differences-only — this is a divergence catalogue, not a winner-picking exercise.
**Inputs**:
- Variant A — `.dev/eval-workspaces/sc-troubleshoot/forensic-analysis/forensic-breakdown.md` (713 lines, 20 sections)
- Variant B — v2 bundle: `src/superclaude/commands/troubleshoot.md` (229 lines) + `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (373 lines) + 5 refs + 2 agent files (`evidence-validator.md`, `confidence-calibrator.md`)

**Output**: ranked divergence catalogue across 4 significance tiers + shared-assumptions tail. 31 substantive differences identified (S: 5, C: 18, X: 0, U: 6, A: 2). No contradictions, because these are two designs of *different* artifacts — they don't disagree, they diverge.

## Steelman of both designs

The forensic design and the v2 bundle each target a different workload. Forensic optimises for project-wide investigation with multi-phase data-flow contracts, subprocess isolation, strict orchestrator-as-dispatcher discipline, and sprint-runner integration on TFEP escalation. v2 optimises for symptom-driven diagnosis with tiered in-session escalation, interactive remediation, and an aggressive auto-activation surface. The differences below are choices about which problem to solve, not flaws in either solution.

---

## Differences ranked by significance

Significance = how much this divergence shapes the design's behavior or how a user / caller experiences it. Tier 1 (behavior-shaping) propagates the most into user-facing outcomes; Tier 4 (instrumentation) propagates the least but matters long-term.

### Tier 1 — behavior-shaping (highest day-1 user-visible impact)

#### 1. Scope of problems addressed (C-001, L2)

- **Forensic**: generic project-wide forensic QA/debug pipeline; auto-discovers 3-10 investigation domains across the codebase (`forensic-spec.md:48-51`); also auto-invoked by `task-unified` on TFEP failing-test escalation.
- **v2**: symptom-driven diagnosis of a single reported issue (bug/build/performance/deployment/security/test); STOPs if neither an issue description nor `--scope` is provided.
- **Divergence**: a user invoking forensic with no symptom gets a project-wide sweep; a user invoking v2 the same way is rejected. The two tools answer different questions.

#### 2. Tier / phase structure (C-003, L2)

- **Forensic**: 8 numbered phases bound by data-flow contracts — Phase 0 Recon → Phase 1 RCA → Phase 2 Hypothesis Debate → Phase 3 Fix Proposals → Phase 3b Fix Debate → Phase 4 Implementation → Phase 5 Validation → Phase 6 Final Report.
- **v2**: 3 tiers expressed as 7 waves bound by conditional escalation gates — Wave 0 Parse → Wave 1 Tier 1 Triage → Wave 2 Confidence Gate → Wave 3 Tier 2 Hypotheses → Wave 4 Tier 2 Adversarial → Wave 5 Synthesis+Report → Wave 6 Tier 3 Remediation.
- **Divergence**: phases-as-data-flow vs waves-as-escalation-gates. Forensic always runs all phases applicable to its tier; v2's later waves are conditional on rubric / `--fix` / user-accept.

#### 3. Remediation chain (C-017, L2)

- **Forensic**: produces `tasklist-insertion.md` for `sc:task-unified --compliance strict` to *re-execute* the failing phase; remediation tasks use `T{XX}.50+` IDs to avoid collision with original `T{XX}.01-20`; resume prompt skips already-completed tasks and adds git-diff context; selective git rollback before re-launch.
- **v2**: interactive — `task-builder` produces an MDTM task file → `/sc:reflect --type task --analyze` reviews it → user runs `/task <path>` themselves (never the skill) → `/sc:reflect --type task --validate` is the pre-commit gate. Diagnosis-first by default. No automatic re-launch. No git rollback (changes never auto-applied).
- **Divergence**: automated loop-back into execution vs hand-off to user-initiated execution loop.

#### 4. Output contract (C-012, L1/L2)

- **Forensic**: `final-report.md` from Phase 6 + per-phase manifests + (TFEP path) `tfep-report.md` + `tasklist-insertion.md`; YAML return contract with `status`, `root_cause_path`, `solution_plan_path`, `tasklist_insertion_path`, `recommended_resume_mode`, `recommended_escalation`, `requires_user_review`, and the unique `test_is_wrong` critical flag (when the debate concludes the test expectations are outdated, caller MUST present to user) (`forensic-spec.md:1953-1984`).
- **v2**: `REPORT.md` always + `audit.log` + structured return dict (`status`, `tier_reached`, `report_path`, `audit_log_path`, `confidence`, `escalation_reason`, `hypothesis_cards`, `adversarial_artifacts_dir`, `task_file_path`, `remediation_offered`, `remediation_accepted`); machine-readable HTML-comment audit blocks (`SC:TROUBLESHOOT:TARGET` header, `SC:TROUBLESHOOT:SUMMARY` footer).
- **Divergence**: forensic ships a YAML contract with `test_is_wrong`; v2 ships a Python-dict contract with `tier_reached` + `escalation_reason`. `test_is_wrong` is genuinely forensic-only.

#### 5. Hallucination contract (C-016 + U-003 + U-005, L3 — paired difference)

- **Forensic** (withhold access): orchestrator-as-dispatcher prohibition — Opus orchestrator NEVER reads source code, capped at ≤8,000 tokens across the whole pipeline (`forensic-spec.md:215-216` NFR-001, `:309-322`); Phase 6 reads only 6 summary artifacts (`dependency-graph.md:226-232`). Hallucination resistance is *architectural*: the synthesizer can't fabricate a `file:line` because it doesn't have the file.
- **v2** (post-hoc validation): dedicated `evidence-validator` agent (`src/superclaude/agents/evidence-validator.md`) independently re-Reads every cited `file:line` in the draft report and drops mismatches before REPORT.md ships; if any dropped, REPORT goes `partial` with a Grounding Gaps section. Hallucination resistance is *behavioural*: the validator catches what the orchestrator might have fabricated.
- **Divergence**: same goal (no fabricated citations), opposite mechanism (withhold access vs post-hoc validate). Forensic is stronger in steady state (no validator-failure path); v2 is more testable (the validator can be unit-tested against fixture reports). v2 also adds a paired `confidence-calibrator` agent for re-grading hypothesis-card confidence (stripped-context anchoring-bias mitigation) — forensic doesn't have an equivalent layer.

### Tier 2 — integration-shaping (how callers wire the tool)

#### 6. Adversarial coupling pattern (C-009, L3)

- **Forensic**: fully delegates Phase 2 (hypothesis debate, `--depth deep`) and Phase 3b (fix debate, `--depth standard`) to `sc:adversarial`. Phase 3b `fix-selection.md` is designated the PRIMARY decision point.
- **v2**: invokes `sc:adversarial-protocol` only in Wave 4, only when ≥2 competing fixes survive Wave 3. On consensus, debate is SKIPPED to avoid token waste. Depth chosen between quick (same-diagnosis variants) and standard.
- **Divergence**: always-debate (cost predictability, design certainty) vs maybe-debate (token thrift, signal-already-converged).

#### 7. Activation mechanism (C-002, L2)

- **Forensic**: command file → mandatory `sc:forensic-protocol` skill pre-step; auto-invoked by `task-unified` on TFEP escalation; explicit `--caller` flag.
- **v2**: substantially broader auto-activation — symptom keywords ("why is X broken", "this used to work", "something's off with"), pasted stack traces, exception names (`NameError`/`TypeError`/`ImportError`), CI log fragments, profiler readouts; explicit `/sc:troubleshoot`; programmatic skill invocation. Deliberately "pushy because the most common reason users skip a debugging tool is they don't know it would help."
- **Divergence**: explicit-invocation surface vs aggressive-keyword-trigger surface.

#### 8. Two-axis vs single-axis mode (C-010 + U-001, L2)

- **Forensic**: two orthogonal axes — `--tier light|standard|deep` controls pipeline scope (which phases execute, agent count); `--depth quick|standard|deep` controls adversarial debate depth only. Both valid together: `--tier light --depth deep`, `--tier standard --depth quick`, etc. (`forensic-spec.md:108-110`, `:199-202`).
- **v2**: single axis — `--depth quick|standard|deep` controls escalation only (Tier 1 cap / rubric-driven / force Tier 2). No pipeline-scope flag.
- **Divergence**: forensic decouples "how much work" from "how rigorous the debate"; v2 collapses both into one knob.

#### 9. Test strategy (C-013, L2 — long-term behavior-shaping)

- **Forensic**: 10 test files (D6.1-D6.13) gated at M6; 6 test types (Smoke per-phase, Integration, Edge case, Schema conformance, Security, Manual review); single 5-file synthetic Python fixture engineered for ≥2 domains and observable Phase 0 output; canned-artifact fixtures per phase boundary at `tests/sprint/forensic/fixtures/canned_artifacts/{phase0,phase2,phase4}_output/`; 58 success criteria SC-001-SC-058.
- **v2**: eval workspaces under `.dev/eval-workspaces/sc-troubleshoot/`; no roadmap test-strategy doc; tests integrate with the regular project pytest suite; no schema-conformance test set for the hypothesis-card template.
- **Divergence**: heavyweight gated test infrastructure vs eval-workspace pattern. Invisible day-1; shapes maintenance and contribution velocity.

#### 10. Failure handling / fallback chain (C-014, L2/L3)

- **Forensic**: *coordinated* three-level adversarial fallback (retry `--depth quick` → spawn single Sonnet scoring agent 60s/1000-token cap → emit findings as-is with `debate_status: "skipped"`). Per-phase token-overrun static rules + `budget_status` field on `progress.json`. Four MCP graceful-degradation levels (Full → Reduced precision → Reduced depth → Minimal). Subprocess SIGTERM→SIGKILL. Selective git rollback via `git diff --name-only {baseline}` intersected with `rca-verdict.md` causal files.
- **v2**: *per-component* error matrix — 10 distinct rows in skill's Error Handling section (all MCPs unavailable, auggie unavailable, root-cause-analyst fails, all Tier 2 agents fail, sc:adversarial fails, self-review blocker, task-builder unavailable, user declines, evidence-validator fails, confidence-calibrator fails). Each row pairs a behavior with an inline fallback.
- **Divergence**: coordinated chain (single fallback strategy across components) vs per-component matrix (each component has its own fallback). Forensic has a unified retreat order; v2 fails gracefully at each layer independently.

### Tier 3 — infrastructure-shaping (Cluster A: subprocess-pipeline + dispatcher design)

The five differences in this tier are all downstream of one decision: forensic chose to ship a subprocess-pipeline + dispatcher-orchestrator + sprint-runner integration; v2 chose an in-session command + skill + agents bundle. Treat as a cluster.

#### 11. Execution model (C-004, L3 — Cluster A root)

- **Forensic**: each "agent" in the pipeline is a separate `claude --print --verbose -p <prompt>` SUBPROCESS spawned by `ForensicOrchestrator` (no IPC — runner cannot send data to a live Claude subprocess). Inter-phase contracts via files on disk. Parallelism via `concurrent.futures.ThreadPoolExecutor(max_workers=len(names))`.
- **v2**: all agents spawned in-session via the `Task` tool; in-session `Skill` invocation for `sc:adversarial-protocol`, `task-builder`, `/sc:reflect`. Parallelism via single-message multi-Task blocks.
- **Divergence**: file-IPC subprocess pipeline vs in-session Task dispatch. Drives every other Cluster A difference.

#### 12. Orchestrator role (C-005, L3 — Cluster A)

- **Forensic**: strict dispatcher — Opus orchestrator NEVER reads source; capped ≤8k tokens total across the pipeline; only consumes structured JSON summaries and Markdown selection files.
- **v2**: participant orchestrator — Claude reads files itself in Waves 0/1/5; runs MCP queries directly; spawns sub-agents via Task; validates `file:line` citations (with `evidence-validator` agent or inline fallback); no formal orchestrator-token cap.
- **Divergence**: dispatcher discipline vs participant-with-validator. Paired with #5 (hallucination contract) — same problem, opposite solutions.

#### 13. CLI / sprint-runner integration (C-015 + U-002, L2 — Cluster A)

- **Forensic**: new `src/superclaude/cli/sprint/tfep.py` module (~450 lines) containing `ForensicOrchestrator`, `EscalationState`, `perform_rollback`, `inject_remediation_tasks`, `write_incident_report`; modifies `executor.py`, `process.py`, `monitor.py`, `models.py`, `commands.py`, `diagnostics.py`; new flags `--tfep-model`, `--tfep-agents`, `--tfep-budget-multiplier`; new `PhaseStatus.TFEP_HALT`; NDJSON marker detection (`TFEP_TRIGGERED`/`TFEP_RESOLVED`/`TFEP_ESCALATED`); `EXIT_RECOMMENDATION: TFEP_HALT` result-file marker.
- **v2**: zero CLI integration — bundle is exclusively a Claude Code skill+command surface. No `monitor.py` NDJSON scanning. No `claude --print` subprocess pattern. No sprint-runner phase loop branch.
- **Divergence**: forensic adds a runtime; v2 ships an interactive surface only.

#### 14. Agent inventory (C-006, L2)

- **Forensic**: subprocess agents per phase (Phase 0 = 3 Haiku; Phase 1 = N Haiku/Sonnet risk-tiered; Phase 2/3b adversarial-protocol advocates; Phase 3 = M Sonnet; Phase 4 = specialist Sonnet + quality-engineer Sonnet; Phase 5 = Haiku + 2 Sonnet; Phase 6 = Opus orchestrator). Light tier = 2-4 Sonnet only. Zero new `src/superclaude/agents/` files.
- **v2**: in-session Task agents drawn from `root-cause-analyst`, `confidence-calibrator`, `evidence-validator` (two NEW dedicated agent files), `self-review`, plus 2-4 specialists from {`quality-engineer`, `performance-engineer`, `security-engineer`, `devops-architect`, `refactoring-expert`, `system-architect`}.
- **Divergence**: subprocess-prefixed slash-command agents (no agent file additions) vs in-session Task agents with two new addressable agent files.

#### 15. Lifecycle / checkpointing (C-018 + U-004, L2)

- **Forensic**: every phase writes artifacts; `progress.json` self-describing (every recoverable state explicitly encoded — CCF-4); stale-codebase detection via `git rev-parse HEAD` on resume; `--resume` and `--dry-run` modes; checkpoint pattern borrowed from `sc:cleanup-audit-protocol`. Explicit 3-tier escalation gradient (light → standard → halt) with `escalation_count` tracking and `--tfep-budget-multiplier` (default 1.5, range 1.0-3.0).
- **v2**: output dir under `.dev/troubleshoot/<slug>-<timestamp>/` holds all artifacts; no formal checkpoint primitive; re-running creates a new slug+timestamp dir; no `--resume` / `--dry-run`.
- **Divergence**: resumable batch pipeline vs fresh-run-per-invocation. Matches their workload assumptions (forensic long-running multi-phase; v2 interactive 1-15 min).

### Tier 4 — instrumentation-shaping (lowest immediate user impact)

#### 16. Model tiering (C-007, L1)

- **Forensic**: explicit decision matrix — Haiku (recon/lint Phase 0/1-low-risk/5a); Sonnet (deep analysis/fixes/tests/validation); Opus (synthesis/coordination only — Phase 0 domain synthesis, Phase 2/3b debate-orchestrator, Phase 6 final report). Light tier collapses to Sonnet-only.
- **v2**: per-agent default models (sonnet for the two new agent files); `--models <tier:model,...>` override (e.g. `tier1:sonnet,hypothesis:opus`); no Haiku tier, no Opus orchestrator pin.

#### 17. MCP usage by phase (C-008, L1/L2)

- **Forensic**: explicit per-phase MCP routing table (Serena Phase 0/1/4; Context7 Phase 0/1/4; Sequential Phase 1/2/3); per-server concurrency cap NFR-010 ≤3; prompt-based per-agent MCP budgets (Phase 1: 3 Serena + 1 Context7 per domain; Phase 4a: 5 Serena + 2 Context7 per fix); `--concurrency` default 5.
- **v2**: per-tier MCP coverage (auggie + serena every tier for in-repo grounding; context7 + tavily Tier 2 only; sequential Tier 2 synthesis only); tavily rate-cap ≤2 queries/invocation; no per-server concurrency cap. `auggie` is the Tier-1 retrieval workhorse — explicitly cited as "free / low-cost tier" offloading the Claude token budget.

#### 18. Token budget profile (C-011, L1)

- **Forensic**: per-phase budget table — Phase 0 ≤500, Phase 1 ≤1000, Phase 2 ≤500, Phase 3 = 0, Phase 3b ≤800, Phase 4 = 0, Phase 5 = 0, Phase 6 ≤2000; orchestrator pinned ≤8k total. Light tier total ~5-8k vs standard ~50-60k.
- **v2**: per-tier target band — Tier 1 ~3-6k Claude (+ auggie 2-5k offloaded); Tier 2 no-adversarial 15-30k; Tier 2 + adversarial 30-60k; Tier 3 +20-40k. Budgets are targets, not hard caps.

#### 19. Refs strategy (S-003 + U-006, L1)

- **Forensic**: all design content inline in `forensic-breakdown.md` + 29 source files in `.dev/releases/backlog/v5.xxforensic/`; no on-demand load contract.
- **v2**: skill loads `refs/*.md` lazily per wave — `escalation-rubric.md` (W2 + W1 calibration), `triage-checklist.md` (W1), `hypothesis-card-template.md` (W1+W3), `report-template.md` (W5), `remediation-handoff.md` (W6). Never pre-loaded.
- **Divergence**: monolithic spec vs lazy-per-wave refs.

---

## Shared unstated assumptions

Both designs depend on these preconditions but neither artifact justifies them. The Round 2.5 invariant probe verified absence from both source artifacts' justification trails.

- **A-001 — Adversarial debate is the right adjudication primitive for competing hypotheses/fixes.** Both delegate competing-fix selection to `sc:adversarial-protocol`'s 5-step pipeline. Neither artifact compares against alternatives (voting, ranking-only, human pick, ensemble averaging). HIGH impact — the choice of adjudication mechanism shapes every Phase 2/3b (forensic) and every Wave 4 (v2) outcome.

- **A-002 — A single static Markdown report is the right terminal artifact.** Both terminate at one Markdown file consumed by user or caller. Neither artifact evaluates alternatives (streaming diff, notebook, issue draft, structured JSON only). MEDIUM impact — shapes how downstream tooling consumes the output.

---

## Index of all 31 substantive differences (per diff-analysis.md)

| ID | Title | Tier | L | Cluster |
|----|-------|------|---|---------|
| S-001 | Top-level shape (single doc vs multi-file bundle) | T1 | — | — |
| S-002 | Section count for spec content | T1 | — | — |
| S-003 | Refs strategy (monolithic vs lazy-per-wave) | T4 | L1 | — |
| S-004 | Authored layering | T2 | — | — |
| S-005 | Document type (analysis vs implementation) | T4 | — | — |
| C-001 | Scope of problems | T1 | L2 | — |
| C-002 | Activation mechanism | T2 | L2 | — |
| C-003 | Tier / phase structure | T1 | L2 | — |
| C-004 | Execution model | T3 | L3 | A |
| C-005 | Orchestrator role | T3 | L3 | A |
| C-006 | Agent inventory | T3 | L2 | A |
| C-007 | Model tiering | T4 | L1 | — |
| C-008 | MCP usage by phase | T4 | L1/L2 | — |
| C-009 | Adversarial coupling pattern | T2 | L3 | — |
| C-010 | Two-axis vs single-axis mode | T2 | L2 | — |
| C-011 | Token budget profile | T4 | L1 | — |
| C-012 | Output contract | T1 | L1/L2 | — |
| C-013 | Test strategy | T2 | L2 | — |
| C-014 | Failure handling / fallbacks | T2 | L2/L3 | — |
| C-015 | CLI / sprint-runner integration | T3 | L2 | A |
| C-016 | Hallucination contract (paired with U-003/U-005) | T1 | L3 | — |
| C-017 | Remediation chain | T1 | L2 | — |
| C-018 | Lifecycle / checkpointing | T3 | L2 | — |
| U-001 | `--tier × --depth` two-axis mode (forensic-only) | T2 | L2 | — |
| U-002 | sprint/tfep.py CLI module (forensic-only) | T3 | L2 | A |
| U-003 | Orchestrator-as-dispatcher prohibition (forensic-only) | T1 | L3 | A |
| U-004 | 3-tier escalation gradient (forensic-only) | T3 | L2 | — |
| U-005 | Evidence-validator + confidence-calibrator agent files (v2-only) | T1 | L3 | — |
| U-006 | Lazy ref loading per wave (v2-only) | T4 | L1 | — |
| A-001 | Shared assumption: adversarial-debate-as-adjudication (UNSTATED) | shared | — | — |
| A-002 | Shared assumption: static-Markdown-report (UNSTATED) | shared | — | — |

L = taxonomy level (L1 surface / L2 structural / L3 state-mechanics). Cluster A = subprocess-pipeline + dispatcher-orchestrator + sprint-integration design cluster.

---

## Convergence statement

This catalogue is the result of a 3-advocate adversarial debate (architect / quality-engineer / analyzer) at `--depth standard` with a Round 2.5 sufficiency-challenge invariant probe. 24 of 26 substantive diff points reached agreement on category and significance (92% — above the 80% convergence threshold). The two unresolved nuances are: (a) exact ranking of C-013 test-strategy divergence (QE Tier 1 vs Architect+Analyzer Tier 2 — split-resolved by adopting Tier 2 placement + QE's long-term framing); (b) exact severity of C-014 failure-handling divergence (Analyzer Round 2 reframe accepted, severity upgraded to High in this merged output).
