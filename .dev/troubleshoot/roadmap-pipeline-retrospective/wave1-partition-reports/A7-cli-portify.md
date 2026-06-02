# A7 — CLI Portify Retrospective (v2.15 → v2.25)

**Partition scope:** Six release directories spanning the CLI-portify arc from the original v2.15 skill (inference-only, one-shot code generation) to v2.25, the first generation that successfully shipped a working `superclaude cli-portify` CLI through the roadmap pipeline.

**Generation map:**

| Release | Date | Role in arc | Outcome |
|---|---|---|---|
| v2.15-cli-portify | 2026-03-06 | Initial skill design + first pipeline run | FAILED — pipeline halted on `extraction` gate (preamble contamination); spec quality 3-6/10 |
| v2.18-cli-portify-v2 | 2026-03-08 | Re-spec'd workflow ("v2") run end-to-end through the pipeline | PASSED roadmap pipeline; produced 5-phase tasklist; downstream impl never shipped |
| v2.23-cli-portify-v3 | 2026-03-09 | Workflow evolution from "code-gen one-shot" to "spec-driven planning" | PASSED with remediation — 4 HIGH spec-fidelity deviations discovered + auto-fixed |
| v2.24-cli-portify-cli-v4 | 2026-03-13 | First v4 attempt to actually build the CLI module | spec-fidelity HALTED on `high_severity_count: 3`; 3-debate accepted-deviation workaround |
| v2.24.1-cli-portify-cli-v5 | 2026-03-13/14 | "v5" pivot — input-target gap discovery + brainstorm re-spec | spec-fidelity still produced 2 HIGH deviations; emitted workflow_*.md corrective workflows |
| v2.25-cli-portify-cli | 2026-03-15/16 | Final, successful CLI build | Sprint pipeline shipped; Phase 3 crashed once on "Prompt is too long" but checkpointed and resumed via PRE phase |

This partition is the canonical case study for **"why one workflow needed 5+ pipeline iterations to converge."** The shape of the arc is **not** "the same defect kept recurring." It is "each iteration exposed a different structural defect in the inference-to-deterministic conversion, and the pipeline mechanically halted on whichever was visible at that stage." Five iterations is the minimum number it took for the underlying spec to become well-formed *and* the roadmap to match it *and* the implementation context to fit in a single Claude session.

---

## Findings

### F-A7-01: v2.15 extraction-step preamble contamination (the original pipeline halt that motivated the whole arc)
- **Type:** FAILURE
- **Pipeline step:** extract
- **Symptom:** First real attempt to feed the v2.15 CLI-portify skill through `superclaude roadmap run` halted at the very first step. `extraction.md` failed STRICT-tier gate validation. Of nine root causes adversarially identified, the single most operationally dangerous one was **CLAUDE.md environment contamination of subprocess behavior** (preamble injected by the parent shell environment into the supposedly hermetic Claude subprocess).
- **Root cause (claimed):** Adversarial three-debater consensus, Workstream 5 — nine distinct root causes, of which RC4/RC5/RC7/RC8 are infrastructure-layer (subprocess env not stripped, preamble sanitizer absent, frontmatter parser uses naive `find("\n---")`) and RC1/RC2/RC3 are prompt-layer (format instructions not at attention-proximity, no feedback injection on retry, no preamble warning in prompt). Documented at `session-findings-merged.md:22, 67-167`.
- **Remediation applied:** Three-PR remediation sequence designed (with two solutions deferred): S5 preamble sanitizer + S3 resilient frontmatter parser + S6 subprocess cwd hardening. Projected 95-100% failure reduction.
- **Outcome:** Designed but not landed in this generation — the work was rolled into the v2.18 re-spec.
- **Still possible today (Auggie check):** PARTIALLY MITIGATED. Per `src/superclaude/cli/roadmap/executor.py:1032-1086`, the pipeline now uses **inline embedding** of input files (the `_embed_inputs()` helper at line 531) instead of `--file` flags. Inline embedding sidesteps the cwd/path-handling class of failures from INV-007. However, `_high_severity_count_zero` at `gates.py:192-214` still hard-fails STRICT-tier gates on any single HIGH deviation count > 0 — meaning the *halt mechanism* the v2.15 investigation diagnosed remains intact today.
- **Source artifacts:** `v2.15-cli-portify/session-findings-merged.md`, `v2.15-cli-portify/adversarial/invariant-probe.md`, `v2.15-cli-portify/adversarial/refactor-plan.md`

### F-A7-02: v2.15 skill spec quality scored 3-6/10 across all five dimensions
- **Type:** FAILURE
- **Pipeline step:** OTHER (pre-extract — spec authoring quality)
- **Symptom:** Six-perspective expert panel (Wiegers/Fowler/Nygard/Whittaker/Crispin/Adzic) reviewed the original v2.15 `SKILL.md` and produced 15 findings (5 Critical, 7 Major, 3 Minor). Critical findings included: missing CLI command entry point (C1), no generation self-validation (C2), prose-not-contract phase interfaces (C3), **pipeline API drift between refs and live code** (C4 — `semantic checks return tuple[bool,str]` claim vs live `Callable[[str], bool]`), no step conservation guarantee (C5). Quality scores: Requirements completeness 5/10, Architecture soundness 6/10, **Generation correctness 4/10, Testability 3/10, Operational determinism 3/10**.
- **Root cause (claimed):** The original skill was written as a behavioral protocol for a single Claude session executing 4 phases of inference, *not* as a contract-bearing pipeline specification. It described intent in prose ("Must include: component inventory, step graph...") without machine-readable validation criteria. C4 (API drift) is the most operationally dangerous: generated code following the skill's API descriptions would fail at import time because the skill referenced API contracts that didn't match the live pipeline code.
- **Remediation applied:** v2.18 produced a 16-section refactored spec with a live API snapshot mechanism. The refactor was scored 8-9/10 across dimensions but still had 8 gaps (G1-G8).
- **Outcome:** SUPERSEDED. v2.18 used the refactored spec as input to the pipeline successfully.
- **Still possible today (Auggie check):** YES for any new skill being portified. The roadmap pipeline does not gate on input-spec quality before extraction — `extract` is the first step and it operates on whatever spec it receives (`executor.py:2106-2128` shows the merge step prompt accepts arbitrary spec content). If a poorly-formed spec is fed to today's pipeline, the failures bubble up *later* (spec-fidelity HIGH count, anti-instinct violations) rather than being caught upfront.
- **Source artifacts:** `v2.15-cli-portify/session-findings-merged.md` §3.1-3.4

### F-A7-03: v2.18 pipeline ran clean — first end-to-end success
- **Type:** SUCCESS
- **Pipeline step:** extract → generate (×2) → diff → debate → score → merge → test-strategy (5-phase tasklist generated)
- **Symptom:** First documented green run. Total duration 1h 49m. All 5 phases of the sprint-generated tasklist passed on first attempt. Base variant Opus-Architect (score 81) selected over Haiku-Analyzer (74) by 6-criterion weighted scoring (`base-selection.md:22-37`).
- **Root cause (claimed):** N/A — success.
- **Remediation applied:** N/A.
- **Outcome:** Tasklist generated cleanly. The pipeline worked. The downstream *implementation* of the cli-portify code was never carried out in this generation (the workflow evolution to spec-driven planning made the v2.18 output stale before it shipped).
- **Still possible today (Auggie check):** YES — this is the steady-state happy path the current pipeline implements.
- **Source artifacts:** `v2.18-cli-portify-v2/execution-log.md`, `v2.18-cli-portify-v2/base-selection.md`

### F-A7-04: v2.23 spec-fidelity gate emitted 15 deviations on first read; 4 HIGH-severity
- **Type:** FAILURE / REMEDIATION (paired)
- **Pipeline step:** spec-fidelity
- **Symptom:** First time the spec-fidelity gate ran with semantic-check enforcement, it found 4 HIGH + 8 MEDIUM + 3 LOW deviations in the auto-generated `roadmap.md` vs the source `spec-cli-portify-workflow-evolution.md`. HIGH deviations: (DEV-001) 9 return-contract fields missing from roadmap, (DEV-002) user-rejection options treated as open question despite spec defining them — and introduced invalid status enum value `forced`, (DEV-003) Phase 3 entry-criteria gate omitted, (DEV-004) focus-pass expert panel (Fowler/Nygard/Whittaker/Crispin) unspecified.
- **Root cause (claimed):** The two parallel architects (Opus + Haiku) operated from the same spec but each compressed or paraphrased contract-bearing sections differently during the architect-debate-merge stages, with information loss at the merge step. Several deviations (DEV-001, DEV-004) are *omission* of details from the spec; others (DEV-002, DEV-010) are *invention* of new vocabulary (status enum `forced`, `complete`) not present in the spec.
- **Remediation applied:** All 15 deviations auto-fixed per `reflect-merged.md`. Remediation date 2026-03-09. `tasklist_ready: true` after fixes.
- **Outcome:** RESOLVED for v2.23. Demonstrated that the remediation step (running on the spec-fidelity output) can mechanically close most deviation types when given a structured deviation report.
- **Still possible today (Auggie check):** YES. Per `executor.py:2157-2173`, `SPEC_FIDELITY_GATE` remains STRICT-tier with semantic check `high_severity_count_zero`. The remediation step (`Step 11: remediate`, `executor.py:2195-2203`) now exists as a first-class non-LLM deterministic step, formalising what v2.23 did ad-hoc.
- **Source artifacts:** `v2.23-cli-portify-v3/spec-fidelity.md`, `v2.23-cli-portify-v3/reflect-merged.md`

### F-A7-05: v2.24 spec-fidelity HALTED on high_severity_count: 3 — first time the gate actually blocked
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** v2.24 ran 8 steps clean and stopped hard at spec-fidelity. `attempt: 2` recorded (one auto-retry, both attempts FAIL). State file shows `fidelity_status: "fail"`. Three HIGH deviations: (DEV-001) roadmap's Section 4.6 implementation order references pre-DEV-001 flat file layout (modules `tui.py`, `logging_.py`, `diagnostics.py` etc.) but the rest of the roadmap uses the accepted 18-module structure with `monitor.py` and `steps/` subdirectory; (DEV-002) F-007 structural validation requirement for `has_section_12` gate is absent from the roadmap; (DEV-003) SC validation matrix missing explicit test criteria for F-007 structural content validation and F-004 per-iteration independent timeout.
- **Root cause (claimed):** DEV-001 is a **documentation lag artefact** — the roadmap was produced via a valid adversarial debate that converged on a *better* architecture than the spec (`steps/` subdirectory + `executor.py` + `convergence.py` + `resume.py` + `contract.py` + `monitor.py` merging tui/logging/diagnostics), but the spec was never updated. The fidelity gate, lacking any concept of "accepted deviation," reports the mismatch as HIGH. DEV-002/DEV-003 are genuine roadmap omissions.
- **Remediation applied:** A formal "accepted deviation" record (`dev-001-accepted-deviation.md`, 6 sub-decisions, 28KB) was written documenting that DEV-001 is **architecturally superior to the spec** and the spec — not the roadmap — should be updated. DEV-002 and DEV-003 produced patches to `roadmap.md` via `remediation-tasklist.md`.
- **Outcome:** PARTIAL FIX. The structural workaround (accepted-deviation document) is essentially a side-channel telling humans "ignore the gate's HIGH count, this one's intentional." There is no machine-readable way to whitelist a specific deviation, so on every re-run the gate continues to count DEV-001 as HIGH until the spec catches up.
- **Still possible today (Auggie check):** YES — `_high_severity_count_zero` at `gates.py:192-214` strictly checks the literal frontmatter count; no allowlist mechanism exists in the current code for documented-accepted deviations. The architecture-superiority-over-spec failure mode is reproducible whenever the architect-debate produces a better design than the input spec.
- **Source artifacts:** `v2.24-cli-portify-cli-v4/spec-fidelity.md`, `v2.24-cli-portify-cli-v4/dev-001-accepted-deviation.md`, `v2.24-cli-portify-cli-v4/troubleshoot-agent1-artifacts.md`

### F-A7-06: v2.24 had no input-target gap detection — portified the wrong abstraction
- **Type:** FAILURE
- **Pipeline step:** OTHER (post-pipeline discovery)
- **Symptom:** The v2.24 release shipped a working `superclaude cli-portify` CLI module. Post-release analysis (`context-overview.md`) revealed that **the command portifies individual skill directories, not complete SuperClaude workflows.** Three specific gaps: (G1) Input target too narrow — only accepts skill directories with `SKILL.md`, can't accept a command name (`sc:roadmap`) or command file path; (G2) Discovery step only inventories the skill directory — misses commands, agents, agent delegation patterns, cross-skill references; (G3) Subprocess scoping ignores `--add-dir` for component-tree directories.
- **Root cause (claimed):** Spec-inherited gap. The original `portify-release-spec.md` defined the input as "a skill directory containing `SKILL.md`" — which is what v2.24 faithfully implemented. The protocol skill's `analysis-protocol.md` defines a 4-step discovery checklist starting with "Find the Command" — but the Python implementation only performed step 2 ("Find the Skill"). This is **the spec being narrower than its own protocol's description** of the discovery surface.
- **Remediation applied:** v2.24.1 was opened explicitly to fix the input-target gap. A two-approach brainstorm (`brainstorm-approach-a.md` 33KB + `brainstorm-approach-b.md` 37KB) was run, scoring matrix (`scoring-matrix.md` weighting Simplicity 20% / Correctness 25% / Backward-compat 15% / Testability 15% / Consistency 15% / Extensibility 10%) selected Approach A with 7.95 vs 7.00. Three elements from Approach B incorporated (resolution log artifact, `--include-agent` CLI flag, `--save-manifest` CLI flag).
- **Outcome:** v2.24.1 was launched as a remediation release.
- **Still possible today (Auggie check):** UNKNOWN. The current `cli_portify/` module structure is the result of these iterations. The fact that v2.24 shipped without a workflow-level integration test that exercised "portify a real SuperClaude command" rather than "portify a skill directory" is the meta-failure here — and the roadmap pipeline does not enforce that integration tests exist in the input spec at all.
- **Source artifacts:** `v2.24.1-cli-portify-cli-v5/context-overview.md`, `v2.24.1-cli-portify-cli-v5/scoring-matrix.md`, `v2.24.1-cli-portify-cli-v5/brainstorm-approach-a.md`

### F-A7-07: v2.24.1 spec-fidelity emitted 2 HIGH + 5 MEDIUM + 3 LOW — gate halted again
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** Second consecutive halt at the same gate. DEV-001: spec defines 7 implementation phases; roadmap consolidates into 5 phases with different groupings — losing the spec's explicit parallelization guidance ("Phases 1-2 can run in parallel") and fragmenting `validate_config.py` ownership across multiple phases. DEV-002: roadmap omits `config.py` modifications entirely — a required modified file from spec §4.2 absent from all roadmap phase task lists.
- **Root cause (claimed):** Same structural mechanism as F-A7-05 — architects' phase reorganization improved coherence at the cost of literal spec fidelity. DEV-002 is a true omission, not a re-architecture: the roadmap's task breakdown never mentions `config.py` even though new CLI options can't propagate without updating `load_portify_config()`.
- **Remediation applied:** Three corrective workflows written: `workflow_portify-roadmap-corrections.md` (15 targeted edits to roadmap.md), `workflow_spec-fidelity-fixes.md`, `workflow_gate-remediation-phase0-decisions.md` (44KB Phase 0 lock-down for gate-system remediation), `workflow_gate-system-remediation-4phases.md` (29KB four-phase remediation of the gate system itself).
- **Outcome:** Remediation produced — but the volume of corrective workflow files (4 in this directory alone) is itself evidence that the spec-fidelity gate's failure mode requires significant manual intervention beyond what the `remediate` step can auto-fix.
- **Still possible today (Auggie check):** YES. The current `executor.py` `_run_convergence_spec_fidelity()` at lines 1290-1477 introduces a convergence engine (max_runs=3) that wraps the deviation-detection / remediation cycle — but the underlying mechanism (gate fails on HIGH count, requires manual or remediation-step intervention) is the same.
- **Source artifacts:** `v2.24.1-cli-portify-cli-v5/spec-fidelity.md`, `v2.24.1-cli-portify-cli-v5/workflow_portify-roadmap-corrections.md`

### F-A7-08: v2.24.1 debate-transcript convergence_score: 0.78 across 2 rounds — productive disagreement
- **Type:** SUCCESS (mechanism-level)
- **Pipeline step:** debate
- **Symptom:** The Haiku-Architect vs Opus-Architect debate ran 2 rounds, achieved 0.78 convergence, and produced explicit Areas of Agreement (5 items) + Remaining Disputes (4 items: Phase 0 value, Model/resolution coupling, Timeline representation, CLI phase isolation). Synthesis recommendation explicitly stated which elements come from A vs B vs are omitted entirely.
- **Root cause (claimed):** N/A — this is the debate step working as designed.
- **Remediation applied:** N/A.
- **Outcome:** SUCCESS. The debate step's output is structured, auditable, and produced a defensible synthesis. This demonstrates the *mechanism* works even when downstream gates fail.
- **Still possible today (Auggie check):** YES — `executor.py` `Step` definition for `debate` still feeds into the score → merge pipeline, with the same convergence-score-bearing structured output expected.
- **Source artifacts:** `v2.24.1-cli-portify-cli-v5/debate-transcript.md`, `v2.24.1-cli-portify-cli-v5/scoring-matrix.md`

### F-A7-09: v2.25 Phase 3 implementation crashed with "Prompt is too long"
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream sprint execution of the tasklist, not the roadmap pipeline itself)
- **Symptom:** Sprint executor running v2.25's Phase 3 tasklist crashed at exit code 1 after 18m47s. Diagnostic report shows `category: crash`, last task ID `T03.10`, 286 events received, output bytes 1,069,418. The final API response was `"Prompt is too long"` — context-window exhaustion on a Sonnet 4.6 turn that had `cache_creation_input_tokens: 4,773,457` and `cache_read_input_tokens: 7,778,929`. Total cost $21.01 for the failed turn.
- **Root cause (claimed):** UNDOCUMENTED at the spec/protocol level. Inferred (INFERENTIAL): the Phase 3 sprint task accumulated context from 12 sequential T03.xx items (T03.01-T03.12) including 40-test executor work, models, registry, process, monitor, tui, return contract, signal handling — each step's output and tests stayed in the session. The crash happened at T03.10 (return contract emission), which had to integrate with every prior step. Cache utilization was high (cache_read 7.7M tokens), so the proximate trigger was likely the cumulative tool-result history exceeding the 200K context window on the final synthesis turn.
- **Remediation applied:** The user's `PRE` phase (`resume-tasklist.md` PRE-001 through PRE-008) verified that the existing Phases 1-3 were complete on disk despite the crash, closed pre-resolved OQs from prior releases (OQ-008 `--file`, OQ-013 PASS_NO_SIGNAL), and resumed from Phase 4. **The work was not lost** — checkpoint files and test outputs persisted to disk before the crash.
- **Outcome:** RECOVERED. Phases 4-11 ran cleanly in a fresh sprint invocation. Total Phase 4-11 duration 1h35m. Roadmap pipeline shipped the CLI module.
- **Still possible today (Auggie check):** YES — the sprint executor does not auto-checkpoint mid-phase or auto-resume mid-phase. The `_LARGE_PROMPT_WARN_BYTES` log warning at `executor.py:1075-1081` warns when composed prompts get large but does not enforce a split. Phases that accumulate 10+ tasks of state in a single Claude session are still at risk on Opus/Sonnet context limits.
- **Source artifacts:** `v2.25-cli-portify-cli/results/phase-3-diagnostic.md`, `v2.25-cli-portify-cli/resume-tasklist.md`

### F-A7-10: v2.25 reused checkpointed state across release boundaries via PRE phase
- **Type:** SUCCESS / REMEDIATION
- **Pipeline step:** OTHER (sprint-level resume semantics)
- **Symptom:** v2.25's `resume-tasklist.md` opens with an explicit "Cross-Release Conflict Analysis" against four prior releases (v2.24.2, v2.24.5, v2.25.5-PreFlightExecutor, v2.25.5-pass-no-report-fix). PRE-001 confirmed Sprint suite 713 passed / 0 failures. PRE-005 / PRE-006 closed two OQs that had already been resolved by prior releases. PRE-007 amended the live roadmap to replace `--file` with inline embedding (per OQ-008 resolution).
- **Root cause (claimed):** N/A — pattern.
- **Remediation applied:** N/A.
- **Outcome:** SUCCESS. The PRE phase is the *first* documented instance of using cross-release artifact analysis to short-circuit redundant re-investigation. Phase 4-11 ran in 1h35m total because Phases 1-3 stayed on disk and the PRE phase verified them rather than re-running them.
- **Still possible today (Auggie check):** PARTIAL — the resume mechanism in `executor.py` `_apply_resume()` lines 1055-1131 (per the v2.24 troubleshoot doc) re-evaluates gate criteria directly against output files on disk rather than reading the `.roadmap-state.json` step status. This means resume *works* for the roadmap pipeline but PRE-phase-style cross-release amendment is an authored convention, not a pipeline feature.
- **Source artifacts:** `v2.25-cli-portify-cli/resume-tasklist.md`, `v2.25-cli-portify-cli/oq-resolutions.md`

### F-A7-11: v2.25 final pipeline shipped — 8 phases passed in 1h35m
- **Type:** SUCCESS
- **Pipeline step:** All phases 4-11 of the sprint tasklist
- **Symptom:** Sprint execution log shows Phase 4 through Phase 11 all pass status, exit 0. Total duration 1h35m. Outcome: success. Final phase (Phase 11) took 23m59s — the longest single phase — consistent with the integration/validation focus.
- **Root cause (claimed):** N/A — success.
- **Remediation applied:** N/A.
- **Outcome:** SHIPPED. The CLI-portify CLI module is in `src/superclaude/cli/cli_portify/` and exists in current code (per the Auggie cross-references in F-A7-01, F-A7-04, F-A7-05).
- **Still possible today (Auggie check):** YES — the artifacts produced by this run are the reference implementation the current pipeline replicates.
- **Source artifacts:** `v2.25-cli-portify-cli/execution-log.md`, `v2.25-cli-portify-cli/results/phase-3-result.md`

### F-A7-12: --file vs inline embedding — empirical OQ-008 resolution
- **Type:** REMEDIATION
- **Pipeline step:** OTHER (subprocess-invocation primitive)
- **Symptom:** Multiple iterations carried OQ-008 (subprocess `--file` behavior) as an open question. v2.24.5 empirically tested and confirmed that `claude --file <path>` does **not** reliably deliver content to the model — appears to use a cloud-download mechanism rather than local file injection. v2.25 incorporated this as a closed OQ in `oq-resolutions.md`.
- **Root cause (claimed):** `claude --file` is broken for this use case; only inline embedding via `-p` reliably delivers content.
- **Remediation applied:** v2.24.5 replaced `--file` with inline embedding across all executors in `cli/roadmap/` and `cli/tasklist/`. v2.25 PRE-007 enforced this in the v2.25 roadmap amendment.
- **Outcome:** ADOPTED PERMANENTLY. Confirmed today at `executor.py:1033-1086` — "Inline embedding: read input files into the prompt instead of --file flags. --file is broken (cloud download mechanism, not local file injector) so inline embedding is always used regardless of composed prompt size."
- **Still possible today (Auggie check):** NO — this failure mode is closed. The code comment explicitly documents the historical reason.
- **Source artifacts:** `v2.25-cli-portify-cli/oq-resolutions.md`, `v2.25-cli-portify-cli/resume-tasklist.md` PRE-005/PRE-007

### F-A7-13: Wiring-verification gate scanned 10 files, found zero issues — first clean gate of a new type
- **Type:** SUCCESS
- **Pipeline step:** wiring-verification
- **Symptom:** `wiring-verification.md` shows 10 files analyzed / 8 skipped, 0 critical / 0 major / 0 info findings, 0 unwired callable count, 0 orphan module count, 0 unwired registry count. Scan duration 0.1273s. Rollout mode: soft.
- **Root cause (claimed):** N/A — gate working in soft (trailing/observability) mode as designed.
- **Remediation applied:** N/A.
- **Outcome:** SUCCESS. Demonstrates the gate-mode rollout pattern (soft/trailing → blocking) works — wiring-verification was added as `GateMode.TRAILING` per Phase 0 design D-05.
- **Still possible today (Auggie check):** YES — the wiring-verification step is present in the current pipeline; gate-mode separation is alive.
- **Source artifacts:** `v2.24.1-cli-portify-cli-v5/wiring-verification.md`

### F-A7-14: Five gens of architecture churn before the data flow stabilized
- **Type:** FAILURE (process-level)
- **Pipeline step:** OTHER (cross-iteration architecture instability)
- **Symptom:** Module-layout decisions changed across every generation. v2.18 used a 5-phase / flat module layout. v2.23 rewrote the entire workflow paradigm ("Workflow Evolution") to replace code-generation with spec-driven planning — entirely different deliverable. v2.24 introduced `steps/` subdirectory + `executor.py` + `convergence.py` + `resume.py` + `contract.py` + merged `monitor.py`. v2.24.1 backed out `resume.py` and `contract.py` (folded into `executor.py`) per DEV-003a/DEV-003b corrections. v2.25 settled on the final layout that shipped.
- **Root cause (claimed):** INFERENTIAL — the absence of a stable architectural anchor across the iterations. Each generation's adversarial debate was free to re-decide module boundaries, and the spec-fidelity gate detected the resulting mismatches as HIGH but couldn't recommend which side was correct.
- **Remediation applied:** The dev-001-accepted-deviation record (F-A7-05) is the first explicit attempt to declare "this is the canonical architecture, update the spec to match." Subsequent generations referenced it. v2.24.1 explicitly backed out parts via TASK-003 / TASK-004 in `workflow_portify-roadmap-corrections.md`.
- **Outcome:** EVENTUALLY STABILIZED in v2.25. The arc demonstrates that 5 generations is the minimum number for a moderately-complex (0.65-0.92 complexity) portification to converge when (a) the input spec needs refinement, (b) the architects are free to re-decide module layout, and (c) no allowlist exists for accepted-deviation handling.
- **Still possible today (Auggie check):** YES — none of the *mechanisms* causing this churn have been removed. The pipeline still permits each architect-debate cycle to re-decide layout; the spec-fidelity gate still hard-fails on HIGH count without an accepted-deviation allowlist.
- **Source artifacts:** `v2.18-cli-portify-v2/roadmap.md`, `v2.23-cli-portify-v3/spec-cli-portify-workflow-evolution.md`, `v2.24-cli-portify-cli-v4/dev-001-accepted-deviation.md`, `v2.24.1-cli-portify-cli-v5/workflow_portify-roadmap-corrections.md`, `v2.25-cli-portify-cli/roadmap.md`

### F-A7-15: Renumbered FR/SC identifiers without traceability table (recurrent)
- **Type:** FAILURE
- **Pipeline step:** generate / merge
- **Symptom:** v2.23 DEV-013 and v2.24.1 DEV-003 both flag the same pattern: the roadmap introduces FR-001..FR-NNN, NFR-001..NFR-NNN, SC-001..SC-NNN identifiers, but the source spec uses FR-060.x / NFR-060.x or FR-PORTIFY-WORKFLOW.x / NFR-WORKFLOW.x. No traceability table maps roadmap IDs back to spec IDs.
- **Root cause (claimed):** The architects renumber requirements as they restructure phases. Without a structural rule "preserve original IDs OR emit traceability table," the gate sees this as deviation. v2.23 DEV-013 was LOW; v2.24.1 DEV-003 was MEDIUM.
- **Remediation applied:** v2.23 added a traceability table; v2.24.1 marked the issue as roadmap-identified rather than spec-required.
- **Outcome:** RECURRENT across generations.
- **Still possible today (Auggie check):** YES — no automated traceability table generation exists in the merge step prompts visible in `executor.py:2106-2128`.
- **Source artifacts:** `v2.23-cli-portify-v3/spec-fidelity.md` (DEV-013), `v2.24.1-cli-portify-cli-v5/spec-fidelity.md` (DEV-003)

### F-A7-16: Phase structure mismatches are the most common HIGH deviation
- **Type:** FAILURE (cross-iteration pattern)
- **Pipeline step:** spec-fidelity
- **Symptom:** v2.23 DEV-005 (parallelization opportunity not reflected), v2.24 DEV-001 (file layout restructure), v2.24.1 DEV-001 (7 phases consolidated to 5), v2.24.1 DEV-002 (`config.py` omitted entirely). The roadmap consistently restructures the spec's phase decomposition.
- **Root cause (claimed):** Architects optimize for *coherent execution units* (e.g., a single PR per phase, single-implementer ownership) while specs optimize for *logical decomposition* (e.g., layered architecture, parallelizable independent work). The two optimisation targets are different and the spec-fidelity gate doesn't have a notion of which is canonical.
- **Remediation applied:** Per-deviation manual remediation in each generation. No structural fix.
- **Outcome:** RECURRENT.
- **Still possible today (Auggie check):** YES — the merge step's prompt (`executor.py:2109-2116`) takes the spec / debate transcript / score / both roadmap variants but provides no constraint to preserve the spec's phase numbering.
- **Source artifacts:** Multiple — `v2.23/spec-fidelity.md` DEV-005, `v2.24/dev-001-accepted-deviation.md`, `v2.24.1/spec-fidelity.md` DEV-001/DEV-002

### F-A7-17: Anti-instinct gate / has-section-12 brainstorm gate — structural checks added late in the arc
- **Type:** REMEDIATION
- **Pipeline step:** merge / spec-fidelity
- **Symptom:** v2.24 DEV-002 specifically called out that `has_section_12` (Brainstorm Gap Analysis section presence) was checked only as "heading present" rather than "findings table or zero-gap summary text present." F-007 (Whittaker finding from `panel-report.md`) noted that the brainstorm gate checks heading only, not content structure.
- **Root cause (claimed):** Initial gate design was structural-presence-only; LLMs can produce a section heading without populating the section.
- **Remediation applied:** v2.24's panel-report.md F-007 was marked `[INCORPORATED]` — added structural validation to gate. Per current code (`executor.py:2129-2138`), `anti-instinct` is now a non-LLM deterministic step with its own gate (`ANTI_INSTINCT_GATE`), reflecting the lesson that structural checks must be deterministic, not LLM-judged.
- **Outcome:** ADOPTED. The current pipeline has non-LLM gates (`anti-instinct`, `remediate`, `deviation-analysis` per Phase 0 D-02 of `workflow_gate-remediation-phase0-decisions.md`).
- **Still possible today (Auggie check):** PARTIALLY — `executor.py:979-985` shows anti-instinct runs deterministically via `_run_anti_instinct_audit()`. The pattern is alive.
- **Source artifacts:** `v2.24-cli-portify-cli-v4/panel-report.md` F-007, `v2.24.1-cli-portify-cli-v5/workflow_gate-remediation-phase0-decisions.md` D-01/D-02

### F-A7-18: Convergence engine for spec-fidelity (max_runs=3) — late-arc remediation of the halt-and-die behaviour
- **Type:** REMEDIATION
- **Pipeline step:** spec-fidelity
- **Symptom:** Across v2.15 → v2.24.1 the spec-fidelity gate's failure mode was binary: any HIGH count halts the pipeline, requiring manual or remediate-step intervention. By v2.25 / current code, a convergence engine wraps spec-fidelity in a 3-iteration loop (`_run_convergence_spec_fidelity()` at `executor.py:1290-1477`, max_runs=3).
- **Root cause (claimed):** N/A — design fix.
- **Remediation applied:** Convergence engine introduced. Per the v2.24.1 workflow remediation phase 0 decisions, deviation-analysis became a separate non-LLM deterministic step that aggregates findings from the convergence engine.
- **Outcome:** ADOPTED. The convergence engine is live.
- **Still possible today (Auggie check):** NO — replaced. The halt-and-die behaviour is gone; multi-iteration auto-remediation is the default when `convergence_enabled=True`.
- **Source artifacts:** Auggie-cross-referenced `src/superclaude/cli/roadmap/executor.py:1290-1477`; design rationale in `v2.24.1-cli-portify-cli-v5/workflow_gate-remediation-phase0-decisions.md` D-02/D-05

### F-A7-19: Schema version field absent from early state files — fixed during gate-system remediation
- **Type:** FAILURE
- **Pipeline step:** OTHER (state persistence)
- **Symptom:** v2.24 troubleshoot-agent1 documented the state file schema with `schema_version: 1` at top level. v2.18 base-selection variant-B was "Schema versioning policy as a prerequisite" — Variant A had not included it; per base-selection.md the gap was "A conceded this gap."
- **Root cause (claimed):** Originally not designed in; only added retroactively when adversarial review surfaced the gap.
- **Remediation applied:** Schema versioning added; backward-compatibility rules defined.
- **Outcome:** ADOPTED.
- **Still possible today (Auggie check):** Likely NO — state file shape documented in v2.24 troubleshoot includes `schema_version: 1`. Did not re-verify with auggie.
- **Source artifacts:** `v2.18-cli-portify-v2/base-selection.md` D-12, `v2.24-cli-portify-cli-v4/troubleshoot-agent1-artifacts.md` §2

### F-A7-20: Five generations is the minimum because of compounded design surface, not because of bug recurrence
- **Type:** FAILURE (meta-pattern)
- **Pipeline step:** N/A (cross-cutting)
- **Symptom:** Each iteration's "halt" had a different proximate cause: v2.15 = preamble contamination, v2.18 = none (success), v2.23 = 4 HIGH fidelity deviations (paradigm shift to spec-driven planning), v2.24 = architecture-superiority-over-spec, v2.24.1 = phase restructure + omitted file, v2.25 = context-window exhaustion (sprint-level, not roadmap-level). **Each cause was different.** The mechanism that made all 5 visible is the same: hard-gate enforcement on a single quality dimension at a time, with no upstream conditioning of the input spec.
- **Root cause (claimed):** INFERENTIAL. The arc reveals that the inference-to-deterministic conversion has at least 5 independent failure surfaces: (1) input-spec quality, (2) parallel-architect divergence at debate/merge, (3) phase-restructure vs spec-fidelity, (4) accepted-architectural-deviation handling, (5) downstream-execution context limits. Each surface is gated independently; no single iteration can prove convergence on all 5 simultaneously, so iteration N can only address surfaces 1..K visible at that point.
- **Remediation applied:** Successive iterations addressed surfaces 1-5 one at a time. v2.25 was the first generation where all 5 surfaces had been remediated *to some degree* — and even then it took a Phase 3 crash + PRE-phase recovery to ship.
- **Outcome:** SUPERSEDED — but the meta-lesson is structural.
- **Still possible today (Auggie check):** YES — none of the 5 surfaces have been *eliminated*; each has only been *mitigated*. A new sufficiently-complex workflow could plausibly require 3-5 iterations again under the current pipeline.
- **Source artifacts:** ALL six directories; this is the synthesis finding.

---

## Cross-cutting patterns within this partition

- **The spec-fidelity gate's binary-halt enforcement is the single highest-frequency failure surface in this arc** — at least 3 of 5 generations halted on it (F-A7-04, F-A7-05, F-A7-07), and the failure cause was different each time (omission, accepted-deviation, phase-restructure).
- **Architecture-superiority-over-spec is a recurrent class of "false-positive HIGH deviation"** — the adversarial debate at the merge step can legitimately produce a better design than the input spec, and the spec-fidelity gate has no allowlist mechanism to recognize this (F-A7-05, F-A7-16, F-A7-14).
- **Phase restructure is the most common deviation across generations** — architects re-decompose phases for coherent-execution-unit reasons while specs decompose for logical-architecture reasons, and the fidelity gate can't recognize either as canonical (F-A7-04, F-A7-05, F-A7-07, F-A7-16).
- **Renumbering of FR/NFR/SC identifiers without traceability tables is a recurrent paper-cut MEDIUM/LOW deviation** that the pipeline never structurally prevents (F-A7-15, surfaces in F-A7-04 / F-A7-07).
- **Downstream sprint execution has its own independent failure surfaces** — context-window exhaustion on a 12-task phase is an orthogonal failure mode that the roadmap pipeline can't predict or mitigate (F-A7-09, F-A7-10).
- **Cross-release / cross-iteration knowledge transfer is currently an authored convention, not a pipeline feature** — the PRE-phase pattern in v2.25 manually folded in OQ resolutions from four prior releases (F-A7-10, F-A7-12).
- **Successful remediation patterns get adopted as first-class pipeline steps over time** — `remediate`, `certify`, `anti-instinct`, `deviation-analysis`, `wiring-verification` all started as workaround patterns before being formalised (F-A7-17, F-A7-18, F-A7-19, F-A7-13).

## Brittleness drivers identified

- **Hard-gate enforcement on a single integer threshold (`high_severity_count == 0`) without an accepted-deviation allowlist** — `gates.py:192-214` strictly checks the literal count; there is no machine-readable way to whitelist a specific DEV-NNN as architecturally-superior-to-spec, so any improvement the architects make over the input spec is mechanically reported as a fidelity failure forever.
- **No upstream input-spec quality gate before extract** — the pipeline accepts any spec at `extract` and reveals quality problems downstream at fidelity / anti-instinct. The v2.15 6-perspective panel review was authored manually; nothing equivalent runs automatically inside the pipeline.
- **Merge-step prompt has no structural constraint to preserve spec phase numbering, file layout, or requirement IDs** — `executor.py:2106-2128`. Each adversarial debate is free to renumber, restructure, and relabel, producing fidelity deviations that are technically "improvements" but mechanically count as HIGH.
- **No machine-readable contract between the protocol skill's discovery checklist and the implementation** — v2.24's input-target gap (F-A7-06) was caused by the skill defining a 4-step discovery checklist while the Python implementation only performed step 2. The pipeline doesn't gate on "all skill-defined discovery steps have corresponding implementation."
- **Sprint executor does not auto-checkpoint or auto-resume mid-phase** — F-A7-09's 18m47s Phase 3 work was recovered only because the *user* wrote a PRE-phase tasklist; the sprint executor itself crashed and emitted no resume artifact at mid-phase granularity.
- **Cross-release artifact / OQ propagation is authored, not derived** — PRE-005/PRE-006/PRE-007/PRE-008 in v2.25's resume-tasklist had to be manually written. No tooling examines prior releases for "have we already resolved this OQ?"
- **The `--file` subprocess flag was assumed-working across all iterations until v2.24.5 empirically proved it broken** — F-A7-12. The pipeline had no canary or smoke-test catching this; only ad-hoc empirical investigation revealed the silent-failure mode.
