# Wave 1 Partition Report — A9: Brainstorm + Convergence + Cleanup-Audit

**Partition focus:** Inputs to the pipeline — brainstorm/convergence quality and how upstream noise propagates to roadmap failures.

**Directories surveyed:**
1. `.dev/releases/complete/v2.21-sc-brainstorm-auggie/`
2. `.dev/releases/complete/roadmap-cli-skill-converge/`
3. `.dev/releases/complete/cleanup-audit-v2-UNIFIED-SPEC/`
4. `.dev/releases/complete/v.1.06-CleanupAudit/`
5. `.dev/releases/complete/v2.20-WorkflowEvolution/`

**Methodology used:** `grep -rli "roadmap" <dir>` enumeration in each directory; Read on every roadmap-touching artifact above 0 bytes, plus all README/findings/phase/forensic/audit/post-mortem/RCA/failure/halt/gate files. Classification of each documented observation into FAILURE / REMEDIATION / SUCCESS. Cross-reference against the current `src/superclaude/cli/roadmap/` implementation was performed inline as evidence permitted (and via stated file:line claims that the v2.20 forensic agents themselves verified).

---

## Findings

### F-A9-001: Brainstorm has no feasibility/codebase-grounding before producing inputs the rest of the pipeline trusts
- **Type:** FAILURE
- **Pipeline step:** extract (upstream — brainstorm feeds spec which feeds extract)
- **Symptom:** The brainstorm stage produces "N strategies, M perspectives" with no constraint extraction from the actual codebase. The pipeline treats textual descriptions as ground truth; ideas that sound impressive but cannot be implemented pass through unchallenged. v2.20 Archive `forensic-diagnostic-report.md:30-48` documents that brainstorm "operates on textual descriptions, not code reality" — Agent 7's phrasing: "Volume of process is not evidence of quality. The process is optimized for *looking thorough* rather than *being thorough*." Every later stage inherits this ungrounded framing.
- **Root cause (claimed):** Brainstorm phase had no Auggie/codebase signal before the v2.21 design effort. v2.21 design-spec.md explicitly identifies the gap: "brainstorming operates on textual descriptions of the codebase rather than the codebase itself".
- **Remediation applied:** v2.21 design-spec.md + tasklist.md added Phase 0 (Codebase Context Loading) with smart-detection signal categories A/B/C and dual Auggie queries (topic + architecture scan). Token budget ~1500-3800 per code-related brainstorm. Fallback path uses Serena + Grep/Glob.
- **Outcome:** Design approved; release status "Planning Complete" as of 2026-03-09. No execution evidence (no results/, no checkpoints/, no phase outputs) in the v2.21 directory — only `design-spec.md` and `tasklist.md`. Cannot confirm the design landed in `src/superclaude/commands/brainstorm.md` from this partition's artifacts.
- **Still possible today (Auggie check):** UNKNOWN — the v2.21 release directory contains design-only artifacts; implementation evidence would live in `src/superclaude/commands/brainstorm.md` frontmatter and Phase 0 prose. Worth verifying as a follow-up.
- **Source artifacts:** `v2.21-sc-brainstorm-auggie/design-spec.md`, `v2.21-sc-brainstorm-auggie/tasklist.md`, `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md`, `v2.20-WorkflowEvolution/Archive/workflow-failure-theories.md`

### F-A9-002: Brainstorm "smart detection" override flags institutionalize the silent-skip failure mode
- **Type:** FAILURE (latent risk in remediation design)
- **Pipeline step:** extract (upstream)
- **Symptom:** v2.21 design-spec §2 (Decision Rule) ends with the explicit instruction: "If uncertain, do NOT trigger. False negatives preferred over token waste." Combined with `--no-codebase` as a first-class flag, this means any brainstorm topic the heuristic misclassifies will silently bypass the codebase loading step that the rest of the v2.21 design treats as the entire point of the release.
- **Root cause (claimed):** Cost optimization framing; the design explicitly trades correctness for token economy. The signal categories A/B/C are heuristic (regex-style verb/noun detection) with no measurement of false-negative rate.
- **Remediation applied:** NONE — false-negative tolerance is the design intent, not an oversight.
- **Outcome:** N/A — design ships as-is. The same "uncertainty defaults to skip" pattern recurs across the pipeline (see F-A9-005 on `_cross_refs_resolve()` returning True; F-A9-013 on `--no-validate` semantics).
- **Still possible today (Auggie check):** YES — by design. This is the kind of "silent degradation under uncertainty" pattern v2.20 Archive forensics flags as Pattern T-003 (Schema drift through passing gates).
- **Source artifacts:** `v2.21-sc-brainstorm-auggie/design-spec.md:79-91` (Decision Rule + override flags)

### F-A9-003: Skill ↔ CLI divergence in roadmap commands — 17 flag mismatches verified
- **Type:** FAILURE (drift propagates into roadmap CLI surface area)
- **Pipeline step:** OTHER (skill/command convergence — upstream of all CLI step execution)
- **Symptom:** `commands/roadmap.md` exposed 6 inference-only flags (`--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, `--persona/-p`) that the CLI does not implement; the CLI exposed 11 flags (`--no-convergence`, `--input-type`, `--tdd-file`, `--prd-file`, `--no-compress`, `--allow-regeneration`, `--resume`, `--max-turns`, `--retrospective`, `--model`, `--debug`) the command file did not document. Default output dir documented as `.dev/releases/current/<spec-name>/` while CLI uses `input_files[0].parent`. Same drift on `validate-roadmap.md` (7 inference-only flags; 3 CLI-only flags; `name: validate-roadmap` missing `sc:` prefix; output-dir `validation/` documented vs CLI `validate/`; NFR-006 exit-0 not documented).
- **Root cause (claimed):** Skills and slash commands evolved as a "parallel inference surface" without an authoritative crosswalk back to the CLI. `release-scope.md:32-39` frames the decision as Option 1 (CLI-mirroring) vs Option 2 (parallel surface).
- **Remediation applied:** `design-decision.md:29-41` records a mixed posture: Option 1 for command/reference surfaces (B-1, B-2, B-3 hybrid, B-4–B-8); Option 2 for the deep-validation skill (B-9 disclaimer-only). Source edits landed across B-1 → B-8 with `make sync-dev`; B-12 (sync refresh) closed with three-way md5 parity proof at `evidence.md:108-153` (per `CP-P05-END.md:54-57`).
- **Outcome:** Release Phase 5 PASS. 68-test regression confirms `/sc:roadmap` `--dry-run` + `/sc:validate-roadmap` `--help` surface match the post-B-2 four-flag CLI surface (`CP-P05-END.md:64-70`).
- **Still possible today (Auggie check):** YES — the convergence release closed *this round* of drift. The structural condition (skill files reading like a parallel design, no automated `--help` ↔ command-file drift detection — `solutions.md` Solution 3 for B-1 explicitly rejected as over-engineered for two files) means drift will reappear the next time CLI flags evolve without a doc-sync gate.
- **Source artifacts:** `roadmap-cli-skill-converge/release-scope.md`, `roadmap-cli-skill-converge/verification.md`, `roadmap-cli-skill-converge/design-decision.md`, `roadmap-cli-skill-converge/checkpoints/CP-P05-END.md`, `roadmap-cli-skill-converge/solutions.md`

### F-A9-004: Skill taxonomy described 5 waves; CLI ships 14 named steps — 6 step names absent entirely from `SKILL.md`
- **Type:** FAILURE
- **Pipeline step:** OTHER (cross-cutting — taxonomy mismatch between skill instructions and CLI executor)
- **Symptom:** `verification.md:84` — `SKILL.md:84-260` lists Waves 0–4 + Post-Wave; `cli/roadmap/executor.py:2156-2170` `_get_all_step_ids` enumerates 14 step IDs: `extract → generate-{a} → generate-{b} → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → certify`. Six step names — `anti-instinct, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify` — appeared NOWHERE in the skill file. Thresholds in skill (`convergence_score ≥ 0.6 → PASS`, validation `≥ 85% → PASS`) had no counterpart in CLI gate criteria (which only validate score is parseable + in `[0.0, 1.0]`).
- **Root cause (claimed):** Skill predates CLI's later step additions (anti-instinct, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify all shipped with subsequent roadmap-CLI releases including v2.20). No mechanism existed to invalidate the skill's wave taxonomy when CLI steps were added.
- **Remediation applied:** B-3 Solution 3 (hybrid) chosen — keep Wave pedagogy as orchestration, add 14-step CLI crosswalk inside each Wave, reframe thresholds as inference-only heuristics, include cosmetic-gate auto-remediation lane (`design-decision.md:33`).
- **Outcome:** B-3 landed in Phase 2 source edits (`CP-P05-END.md:140-149` — Phase 2 = B-3 through B-8). Whether the crosswalk is internally consistent post-edit is asserted in the closeout but not independently re-verified in the artifacts I read.
- **Still possible today (Auggie check):** YES — the same condition (CLI steps evolve independently of skill prose) recreates the drift the moment a new step ID is added to `_get_all_step_ids`. No structural mechanism (e.g., a test asserting skill mentions every CLI step ID) was added by this release.
- **Source artifacts:** `roadmap-cli-skill-converge/verification.md:76-88`, `roadmap-cli-skill-converge/solutions.md:87-118`, `roadmap-cli-skill-converge/design-decision.md:33`, `roadmap-cli-skill-converge/checkpoints/CP-P05-END.md`

### F-A9-005: `_cross_refs_resolve()` in `roadmap/gates.py` unconditionally returned True for an extended period
- **Type:** FAILURE
- **Pipeline step:** merge (gate check)
- **Symptom:** v2.20 spec-fidelity-gap-analysis-merged.md §3.2: "`_cross_refs_resolve()` in MERGE_GATE currently **always returns True** — the cross-reference check is non-enforcing." v2.20 Archive `forensic-diagnostic-report.md:213-217` cites Agent 6: "`_cross_refs_resolve()` finds cross-references, iterates over them, but unconditionally returns True. The comment says: `# Don't fail on this — it's too fragile for now`." A roadmap with one bullet and 99 lines of placeholder prose would pass the `_has_actionable_content()` semantic check as well.
- **Root cause (claimed):** "Too fragile for now" — the gate was committed as a known-broken stub, and no mechanism (issue tracker, FIXME audit gate, test asserting the function returns False on a malformed input) prevented it from staying broken.
- **Remediation applied:** v2.20 roadmap FR-019 — "`_cross_refs_resolve()` changed from always-return-True to actual validation: extract heading anchors, find cross-references, return False if any reference targets a non-existent heading." Rollout warning-first per OQ-001 resolution. FR-018 separately promotes REFLECT_GATE from STANDARD to STRICT so its semantic checks actually execute.
- **Outcome:** v2.20 roadmap landed Phase 1 fixes; the v2.20 forensic Archive `workflow-failure-theories.md:1-40` was the *driver* for this remediation and `spec-fidelity-gap-analysis-merged.md` records the v2.19 case study (4 deviations, 3 of 4 originating at roadmap layer) that justified shipping a proper fidelity gate at all.
- **Still possible today (Auggie check):** YES at pattern level — the structural condition that allowed "TODO/fragile stubs in shipping gates" exists wherever gates are added without an end-to-end test that produces a known-invalid input and asserts gate rejection.
- **Source artifacts:** `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md:213-217`, `v2.20-WorkflowEvolution/Archive/spec-fidelity-gap-analysis-merged.md`, `v2.20-WorkflowEvolution/roadmap.md` (Phase 1 deliverables FR-018, FR-019), `v2.20-WorkflowEvolution/extraction.md:88-98`

### F-A9-006: v2.19 case study — 75% of post-implementation deviations originated at the roadmap level, propagated through tasklist and execution undetected
- **Type:** FAILURE (validation gap)
- **Pipeline step:** merge → tasklist → execution (handoff)
- **Symptom:** v2.20 `spec-fidelity-gap-analysis-merged.md` Table 2.2 — 4 deviations between `superclaude roadmap validate` spec and built implementation; root cause analysis traced 3 of 4 (75%) back to the roadmap generation step: `ValidateConfig` missing 4 path fields, `build_reflect_prompt` missing `agent` param, `build_adversarial_merge_prompt` renamed + `roadmap_file` dropped. Table 2.4 — full pipeline deviation counts: Spec → Roadmap 29 deviations (5 HIGH, 12 MEDIUM, 12 LOW); Roadmap → Tasklist 15 (3/6/6); Tasklist → Implementation 1. Most damaging: `build_reflect_prompt` accepts 3 parameters that are NEVER interpolated into the prompt text — multi-agent validation in v2.19 was running *identical prompts on different models*, reducing the supposed adversarial value to "multi-model labeling theater."
- **Root cause (claimed):** No spec-fidelity gate existed at any pipeline boundary. Roadmap simplifications, renames, and field drops were never compared against the spec text before being passed to tasklist generation.
- **Remediation applied:** v2.20 roadmap implements `SPEC_FIDELITY_GATE` (STRICT, blocks on `high_severity_count > 0`) and `TASKLIST_FIDELITY_GATE` (STRICT, blocks on HIGH-severity) using the 7-column FidelityDeviation schema. Per `extraction.md` FR-001–FR-031 and `roadmap.md` Phase 2 deliverables. Severity definitions are embedded directly in the prompt to reduce LLM classification drift (RSK-007).
- **Outcome:** Gates designed and roadmap signed off at convergence 0.72 (`roadmap.md` frontmatter line 5). Whether the gates actually catch HIGH-severity deviations in production, vs. being defeated by LLM under-reporting severity, is a known residual risk (RSK-007) flagged in v2.20 but not measured here.
- **Still possible today (Auggie check):** YES — the gate exists but its efficacy depends entirely on the LLM agent honestly reporting `high_severity_count`. The base failure mode (silent context loss through handoffs) is structural; the gate is a single, LLM-trust-dependent check.
- **Source artifacts:** `v2.20-WorkflowEvolution/Archive/spec-fidelity-gap-analysis-merged.md` §2 (case study), `v2.20-WorkflowEvolution/extraction.md` FR-001–FR-031, `v2.20-WorkflowEvolution/roadmap.md` Phase 2, `v2.20-WorkflowEvolution/diff-analysis.md`

### F-A9-007: v2.20 debate convergence score 0.72 — below high-confidence threshold but release shipped
- **Type:** FAILURE (process)
- **Pipeline step:** debate / score
- **Symptom:** `v2.20-WorkflowEvolution/roadmap.md:6` — `convergence_score: 0.72`, `rounds_completed: 3`, `variant_scores: A:82 B:63`. v2.20 Archive `forensic-diagnostic-report.md:107-110` flags this as a pattern: "v2.13 Pipeline Unification, frontmatter: `convergence: 0.72` — below the typical 0.85+ threshold for high confidence, yet the release proceeded." v2.20 reproduces it. `debate-transcript.md` Round 3 "Remaining Disagreements" section lists 4 unresolved disputes (phase count/structure, timeline 5 vs 5.5-6.0 weeks, dedicated testing phase, decision formality) that the convergence math glosses over.
- **Root cause (claimed):** CLI gates only validate `convergence_score ∈ [0.0, 1.0]` (validity check, not pass threshold). Skill-side prose mentioned thresholds (`≥ 0.6 → PASS`, `≥ 0.5 → PARTIAL`) but `roadmap-cli-skill-converge/verification.md:84` confirms these are skill-only and have no CLI gate enforcement. So a 0.72 score that the skill would call "passing partial" is treated as "PASS" by the gate.
- **Remediation applied:** NONE explicitly. The roadmap-cli-skill-converge B-3 hybrid solution reframes the skill thresholds as "inference heuristics only" but does not introduce a CLI-side convergence threshold. The structural condition persists.
- **Outcome:** v2.20 shipped at 0.72. Whether the unresolved disagreements (e.g., timeline realism) materially affected execution is not visible in this partition's artifacts.
- **Still possible today (Auggie check):** YES — `cli/roadmap/gates.py` does not gate on convergence threshold; it only validates the score parses. The v2.20 Archive `forensic-diagnostic-report.md:104-110` framing as Agent 6: "`_convergence_score_valid()` checks only that the value parses as a float in [0.0, 1.0]. The LLM can write `convergence_score: 0.5` with no relationship to the actual debate content" — remains the architectural state.
- **Source artifacts:** `v2.20-WorkflowEvolution/roadmap.md:1-9`, `v2.20-WorkflowEvolution/debate-transcript.md:118-127`, `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md:88-117`, `roadmap-cli-skill-converge/verification.md:80-88`

### F-A9-008: Schema drift through passing gates — extraction schema went from 17+ fields to 3
- **Type:** FAILURE
- **Pipeline step:** extract → generate
- **Symptom:** v2.20 Archive `forensic-diagnostic-report.md:130-135` cites v2.19 Reliability Spec §1.2: "The current CLI extract prompt requests only 3 fields (`functional_requirements`, `complexity_score`, `complexity_class`) and the gate validates only those 3... downstream generate, diff, and merge steps that were designed against the rich extraction schema receive a thin one." The gate adapted to the reduced schema and reported PASS throughout.
- **Root cause (claimed):** No "contract preservation" check between the protocol-side schema definition (`refs/extraction-pipeline.md` 8-step pipeline) and the CLI-side `build_extract_prompt` single-call output. Schema drift was invisible because the gate validates the *current* extraction shape, not the *intended* one.
- **Remediation applied:** v2.20's spec-fidelity gate addresses the *spec → roadmap* boundary but not the *protocol-doc → CLI-prompt* boundary that produced this drift. roadmap-cli-skill-converge B-7 collapsed `refs/extraction-pipeline.md` from the 8-step model to mirror the single CLI prompt — this fixes the doc, not the underlying issue that schema drift can recur.
- **Outcome:** B-7 closed (Phase 2 of converge release). Extraction schema is what the CLI produces; documentation now describes that. The original v2.20 forensic insight — that the schema shrank silently — is structurally still possible the next time someone simplifies a prompt.
- **Still possible today (Auggie check):** YES — verifiable in `cli/roadmap/prompts.py:180` (`build_extract_prompt`) per `verification.md:142-146`. The prompt is what the LLM is asked for; no test asserts the produced extraction.md frontmatter contains the historical 17+ fields.
- **Source artifacts:** `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md:130-135`, `v2.20-WorkflowEvolution/extraction.md:8-13` (only 3-4 frontmatter fields beyond metadata), `roadmap-cli-skill-converge/verification.md:138-147`, `roadmap-cli-skill-converge/solutions.md` B-7

### F-A9-009: Cleanup-audit v2 spec-fidelity gate PASSED with 8 MEDIUM/LOW deviations but produced operational sequencing problems
- **Type:** FAILURE (gate semantic blind spot — partial)
- **Pipeline step:** spec-fidelity
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/spec-fidelity.md` frontmatter: `high_severity_count: 0, medium_severity_count: 5, low_severity_count: 3, total_deviations: 8, tasklist_ready: true`. The 5 MEDIUMs include DEV-004 ("Subagent failure handling deferred to Phase 4 but must be operational from Phase 1") and DEV-005 ("Budget controls validated in Phase 4 but implemented in Phase 3 — creates validation gap for Phases 0-2"). Both are sequencing/cross-cutting infrastructure issues that materially affect whether earlier phases can even execute. The gate marked the roadmap "tasklist_ready" anyway because the boolean derivation only requires `high_severity_count == 0 AND validation_complete == true`.
- **Root cause (claimed):** The 7-column FidelityDeviation severity definitions (FR-023) classify "Functional requirement missing, signature changed, constraint dropped, API contract broken" as HIGH but treat "Requirement simplified, parameter renamed, NFR softened" as MEDIUM. Cross-cutting infrastructure deferred to a later phase falls into the MEDIUM bucket and does not block — even when it leaves earlier phases without failure recovery.
- **Remediation applied:** NONE in this release. v2.20 roadmap §2 OQ-005 explicitly defers the question: "Only HIGH-severity deviations block in v2.20. MEDIUM severity is logged but non-blocking. Revisit MEDIUM-blocks policy in v2.21." The merge spec also opened OI-051-5: "Should MEDIUM severity become blocking for certain deviation categories (e.g., fabricated traceability IDs per Gap Analysis TD-001)?"
- **Outcome:** `cleanup-audit-v2-UNIFIED-SPEC/.roadmap-state.json:47` — `fidelity_status: pass`, validation skipped. Tasklist generation proceeded with the sequencing issues unresolved at roadmap level.
- **Still possible today (Auggie check):** YES — the MEDIUM-non-blocking policy is by design and the OQ-005 follow-up has no resolution in artifacts I read.
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/spec-fidelity.md`, `cleanup-audit-v2-UNIFIED-SPEC/.roadmap-state.json:47-51`, `v2.20-WorkflowEvolution/roadmap.md` §2 (OQ-005), `v2.20-WorkflowEvolution/adversarial/refactor-plan.md` Change 7 (OI-051-5)

### F-A9-010: `wiring-verification` gate ran soft-mode with 0 findings on a directory that had not yet been implemented
- **Type:** FAILURE (gate trivially passes when target is empty/un-implemented)
- **Pipeline step:** wiring-verification
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/wiring-verification.md` frontmatter: `target_dir: /config/workspace/IronClaude/.dev/releases/complete, files_analyzed: 10, files_skipped: 8, rollout_mode: soft, total_findings: 0, blocking_findings: 0`. The gate pointed at the release-history directory (`.dev/releases/complete`), NOT the cleanup-audit implementation. With nothing to analyze, the gate trivially passed. The "Recommended Remediation" section reads: "No remediation needed — all checks pass."
- **Root cause (claimed):** UNDOCUMENTED — the `target_dir` field in the produced gate output points at a directory that is the wrong scope for a cleanup-audit roadmap. Whether this is a configuration bug, a default-fallback, or intentional is not explained inside the artifact.
- **Remediation applied:** NONE — the gate marked PASS and the pipeline continued.
- **Outcome:** `cleanup-audit-v2-UNIFIED-SPEC/.roadmap-state.json:42` — `wiring-verification.status: PASS, attempt: 1`. The gate's own evidence notes: "Analysis uses AST-based static analysis; dynamic imports and runtime wiring are not detected. Alias resolution is limited to direct name references."
- **Still possible today (Auggie check):** YES — this is structurally identical to the v2.20 forensic finding that semantic checks pass on empty/minimal input. The gate has no precondition that target_dir contains the artifact-under-validation.
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/wiring-verification.md`, `cleanup-audit-v2-UNIFIED-SPEC/.roadmap-state.json:39-46`

### F-A9-011: Adversarial stage drops 10-15% of findings silently; no downstream tracking
- **Type:** FAILURE
- **Pipeline step:** debate → merge
- **Symptom:** v2.20 Archive `forensic-diagnostic-report.md:100-106` cites v2.07 Retrospective §4.5: "~85-90% of adversarial conclusions were incorporated. Notable omissions: Strategy 2's 6-field structured error format was simplified to 2-field; Three v1.1 forward/deferral notes were not documented." `workflow-failure-theories.md` Stage 3 evidence: "Strategy 3's fourth standalone criterion ('session-start executable') was dropped." Convergence score does not reflect findings dropped — it reflects agreement *among the remaining points*.
- **Root cause (claimed):** Merge step has no "every adversarial finding either ships or is explicitly deferred" invariant. Refactor plans cite "Changes Not Being Made" sections (see `cleanup-audit-v2-UNIFIED-SPEC/adversarial/refactor-plan.md:42-44` and `v2.20-WorkflowEvolution/adversarial/refactor-plan.md` "Changes NOT Being Made") but those represent *intentional* omissions; *unintentional* drops have no audit trail.
- **Remediation applied:** Partial — refactor-plan template now includes "Changes Not Being Made" sections (cleanup-audit-v2 `refactor-plan.md:42-44`; v2.20 `refactor-plan.md` end). This catches intentional drops but does not detect unintentional ones.
- **Outcome:** Pattern recurs across releases (v2.07, v2.13, v2.20 all cite it). No mechanism delivered that compares debate-transcript findings against merged-roadmap content for completeness.
- **Still possible today (Auggie check):** YES — `cli/roadmap/prompts.py:build_debate_prompt` (per `verification.md:158`) is a single-shot prompt builder with no post-debate finding-coverage check.
- **Source artifacts:** `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md:100-106`, `v2.20-WorkflowEvolution/Archive/workflow-failure-theories.md` Stage 3, `cleanup-audit-v2-UNIFIED-SPEC/adversarial/refactor-plan.md:42-44`, `v2.20-WorkflowEvolution/adversarial/refactor-plan.md`

### F-A9-012: Adversarial debate at convergence 0.86 for cleanup-audit-v2, but unique-contribution items risked being dropped — only refactor-plan captured them
- **Type:** SUCCESS (mechanism worked) / latent risk (mechanism is fragile)
- **Pipeline step:** debate → merge
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/adversarial/debate-transcript.md:8-10` — convergence 0.86, threshold 0.80, 6 of 6 points resolved. `diff-analysis.md` unique contributions: U-001 Variant 2's per-milestone AC mapping (assessed High), U-002 Variant 1's context-window pressure risk callout (assessed Medium). `refactor-plan.md` Changes 1–5 each cite a source variant and a target location — the explicit "preserve this unique contribution" mechanism *worked* for these.
- **Root cause (claimed):** The diff → debate → refactor-plan chain functions when the diff stage successfully enumerates unique contributions. The cleanup-audit-v2 debate had only 6 differences and 3 advocates (haiku, sonnet, opus); the small surface area made it tractable. Larger-surface debates (v2.20 with 14 D-XX points) may surface unique contributions less reliably.
- **Remediation applied:** N/A — this is a case of the existing mechanism working as designed.
- **Outcome:** All 5 planned changes auto-approved; risk graded Medium overall; "no replacement of AC mapping with high-level-only summary" explicit in "Changes Not Being Made". Roadmap completed at convergence 1.0 (`cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:7`).
- **Still possible today (Auggie check):** SUCCESS path verified per `verification.md:155-161` — the debate/score/merge step IDs all exist in `_get_all_step_ids` at `executor.py:2156-2170`. The fragility is unmeasured.
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/adversarial/debate-transcript.md`, `cleanup-audit-v2-UNIFIED-SPEC/adversarial/diff-analysis.md`, `cleanup-audit-v2-UNIFIED-SPEC/adversarial/refactor-plan.md`, `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:1-9`

### F-A9-013: `--no-validate` flag semantics confused between "skip validation pipeline" and "skip spec-fidelity step"
- **Type:** REMEDIATION (preemptive)
- **Pipeline step:** spec-fidelity (gate bypass)
- **Symptom:** v2.20 FR-010: "Existing `--no-validate` flag skips only the validate pipeline, not spec-fidelity (spec-fidelity is a generation quality gate)." The risk was that an operator running `--no-validate` to skip the post-pipeline `validate` subcommand would also accidentally skip the spec-fidelity step that runs *inside* the main `roadmap run` pipeline. The two flags share a verbal namespace ("validate") despite addressing different lifecycle stages.
- **Root cause (claimed):** Flag-name overlap between pipeline-internal validation gates and post-pipeline validation subcommand.
- **Remediation applied:** FR-010 makes the bypass behavior explicit: spec-fidelity runs regardless of `--no-validate`. Acceptance criterion AC-005 enforces this in tests (per `roadmap.md` Phase 2 deliverable 3).
- **Outcome:** v2.20 roadmap Phase 2 ships the bypass-protection logic. Whether the actual CLI implementation honors this is unverified in this partition (would need to check `cli/roadmap/commands.py` for the `--no-validate` branch).
- **Still possible today (Auggie check):** UNKNOWN — verification would need `cli/roadmap/commands.py` flow against the v2.20 FR-010 spec. The convergence release verified the `--no-validate` flag exists in CLI (`verification.md:43`) but did not verify its bypass semantics around spec-fidelity.
- **Source artifacts:** `v2.20-WorkflowEvolution/extraction.md` FR-010, `v2.20-WorkflowEvolution/roadmap.md` Phase 2 §3

### F-A9-014: Retrospective findings post-date the next spec — workflow plans forward, learns backward
- **Type:** FAILURE
- **Pipeline step:** extract (upstream — retrospective injection)
- **Symptom:** v2.20 Archive `forensic-diagnostic-report.md:147-156`: "The v2.07 retrospective was dated 2026-03-05. The merged spec is dated 2026-03-04. The spec **predates** the retrospective — meaning the retrospective findings could not have been incorporated by timeline." Concretely: v2.07 retrospective flagged "PARTIAL silently promoted to PASS" as P0; v2.08 merged spec's `StepStatus` enum has PASS|FAIL|TIMEOUT|SKIPPED|CANCELLED|PENDING with no PARTIAL.
- **Root cause (claimed):** Brainstorm/extract phases consume retrospectives as optional "known issues" text but have no mechanism to halt spec emission until the latest retrospective findings have been processed. The cadence of retrospective production was slower than the cadence of next-spec production.
- **Remediation applied:** v2.20 FR-027–FR-029 add `--retrospective` flag to `roadmap run` and a `retrospective_content` parameter to `build_extract_prompt`. If a retrospective file exists, the extraction prompt includes a "Known Issues from Prior Releases" section.
- **Outcome:** Mechanism delivered. The mechanism still relies on the *operator* pointing `--retrospective` at the right file at the right time; nothing structurally couples the retrospective production cycle to the next spec generation cycle. The fix is necessary but not sufficient.
- **Still possible today (Auggie check):** YES partially — the flag exists per `verification.md:43` (`--retrospective` listed). The deeper coupling (no spec ships until last retrospective is processed) was not implemented.
- **Source artifacts:** `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md:147-156`, `v2.20-WorkflowEvolution/extraction.md` FR-027–FR-029, `v2.20-WorkflowEvolution/Archive/workflow-failure-theories.md` Theory 5

### F-A9-015: Cleanup-audit v1 (v.1.06) shipped without the validation infrastructure that v2 would later need to retrofit
- **Type:** FAILURE (cascade — v1 design omitted validation, requiring v2 unification)
- **Pipeline step:** OTHER (cross-release pattern)
- **Symptom:** `v.1.06-CleanupAudit/sc-cleanup-audit-roadmap.md` shipped 22 deliverables, 6 milestones, 82 tasks. The v2 extraction `cleanup-audit-v2-UNIFIED-SPEC/extraction.md` later documents that v1 "produced 12 per-file profiles from 5,857 files (99.8% miss rate) and failed to implement its own spec promises (coverage tracking, checkpointing, evidence-gated classification, spot-check validation)." `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:20-29` Phase 0 of v2 was explicitly named "Enforce Existing v1 Spec (Critical Foundation) — close the spec-implementation gap, implement every v1 promise before adding new capabilities."
- **Root cause (claimed):** v1 design (`v.1.06-CleanupAudit/research/refactor-plan.md`) treated the skill/agent decomposition as the architecture concern. It did not include validation infrastructure (coverage manifests, checkpointing, spot-check validation) as P0 milestones — those were promised in the v1 spec text but never structurally guaranteed.
- **Remediation applied:** v2 UNIFIED-SPEC is itself the remediation. The 4-wave adversarial merge (`cleanup-audit-v2-UNIFIED-SPEC.md` headers) explicitly resolved 22 conflicts across 45 topics. v2 roadmap Phase 0 enforces v1's unmet promises before adding anything new.
- **Outcome:** v2 roadmap shipped at convergence 1.0 (`roadmap.md:7`). Spec-fidelity at PASS (8 deviations, 0 HIGH). Whether the v2 implementation closes the 99.8% miss rate is not verifiable from this partition's artifacts (no implementation evidence in `cleanup-audit-v2-UNIFIED-SPEC/`).
- **Still possible today (Auggie check):** YES — the pattern (ship-without-validation-infrastructure, retrofit-later) is not blocked by any pipeline mechanism. Releases can still defer validation infrastructure to "future work."
- **Source artifacts:** `v.1.06-CleanupAudit/sc-cleanup-audit-roadmap.md`, `v.1.06-CleanupAudit/research/refactor-plan.md`, `cleanup-audit-v2-UNIFIED-SPEC/extraction.md:21-23`, `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:10-37`

### F-A9-016: Cleanup-audit-v2 convergence 1.0 reached with only 6 diff points and 3 advocates — small surface area
- **Type:** SUCCESS (with caveat)
- **Pipeline step:** debate / score / merge
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:7` records `convergence_score: 1.0`. The `diff-analysis.md` enumerates 6 differences (2 structural + 2 content + 0 contradictions + 2 unique), all severity Low/Medium except C-001 (AC traceability, severity High). 3 advocates, 2 rounds.
- **Root cause (claimed):** The roadmap inputs were already converged after a 4-wave adversarial merge of the *spec* itself (`extraction.md:14` cites "extraction_mode: chunked (4 chunks)" of the UNIFIED-SPEC). The roadmap-level debate had little left to disagree about because upstream convergence had already happened.
- **Remediation applied:** N/A — this is a case of upstream convergence reducing downstream debate surface.
- **Outcome:** Roadmap shipped, spec-fidelity PASS. The 1.0 score is structurally valid per the gate (`verification.md:84` — gate only requires the score be parseable + in `[0.0, 1.0]`). The caveat: in v2.20 the same level of upstream convergence was NOT achieved (debate-transcript explicitly notes 4 remaining disagreements at round 3), and the convergence score fell to 0.72.
- **Still possible today (Auggie check):** YES — depends entirely on input quality, which the pipeline does not gate.
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:1-9`, `cleanup-audit-v2-UNIFIED-SPEC/adversarial/diff-analysis.md`, `cleanup-audit-v2-UNIFIED-SPEC/extraction.md:14`

### F-A9-017: Brainstorm Auggie integration designs token budget but never measures recall/precision of signal detection
- **Type:** FAILURE (latent)
- **Pipeline step:** extract (upstream)
- **Symptom:** v2.21 `design-spec.md` §6 publishes token budget: detection logic ~50, Auggie query 1 ~500-1500, Auggie query 2 ~500-1500, briefing ~500-800, total ~1500-3800 per code-related brainstorm. There is no corresponding measurement plan for:
  - false-positive rate (brainstorm topic falsely classified as code-related — token waste)
  - false-negative rate (code topic classified as non-code — codebase context skipped silently, F-A9-002)
  - briefing utility (does Phase 1 Socratic dialogue actually reference the briefing content?)
- **Root cause (claimed):** Cost optimization framing dominates the design. The Success Criteria section of `tasklist.md` checks frontmatter mentions auggie-mcp, sections exist, sync passes, no test regressions — all structural. No semantic check on whether the integration improves brainstorm outcomes.
- **Remediation applied:** NONE — measurement plan absent from `tasklist.md`.
- **Outcome:** Cannot evaluate — the v2.21 release directory has no execution evidence (no results, no checkpoints, no signal-detection metrics).
- **Still possible today (Auggie check):** YES — by design.
- **Source artifacts:** `v2.21-sc-brainstorm-auggie/design-spec.md` §6 + §7, `v2.21-sc-brainstorm-auggie/tasklist.md` Success Criteria

### F-A9-018: Cleanup-audit v2 lists token budget estimates as "UNVALIDATED" but ships with them anyway
- **Type:** FAILURE (acknowledged)
- **Pipeline step:** merge (roadmap)
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:16` — "All token budget estimates are **UNVALIDATED** and require empirical benchmarking before use." Phase 0 estimated effort: "UNVALIDATED — benchmark by implementing checkpointing first, then extrapolate." Multiple "UNVALIDATED" markers persist across Phase 0–4 effort estimates.
- **Root cause (claimed):** Roadmap shipped with effort/budget estimates that the authors explicitly flagged as guesses. No gate blocks on "UNVALIDATED" markers in the roadmap output.
- **Remediation applied:** Honesty was applied (markers are visible). No mechanism converts "UNVALIDATED" into a blocking finding.
- **Outcome:** Roadmap shipped with UNVALIDATED markers intact. Spec-fidelity gate did not flag them (the deviation report focuses on spec-to-roadmap content differences, not on validation-readiness of the roadmap's own estimates).
- **Still possible today (Auggie check):** YES — no gate criterion checks for "UNVALIDATED" / "TBD" / "TODO" content in roadmap output. Same structural condition that allowed `_cross_refs_resolve()` to ship as a TODO stub (F-A9-005).
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/roadmap.md:16, 37`

### F-A9-019: B-11 (global-install gap) claim was REFUTED by verification — false-positive in `/sc:analyze` input
- **Type:** SUCCESS (verification mechanism caught a false positive)
- **Pipeline step:** OTHER (upstream analyze → release-scope)
- **Symptom:** `roadmap-cli-skill-converge/release-scope.md` B-11 claimed both skills were missing from `/config/.claude/skills/`. `verification.md:193-207` independently verified the claim by running `ls` and `md5sum`: both skills are present and byte-identical to src and repo-local `.claude/`. Verifier notes flag this explicitly: "The scope-doc statement 'The global location /config/.claude/skills/ does not contain either skill' is false as of 2026-05-15."
- **Root cause (claimed):** The upstream `/sc:analyze` pass produced an analyzer-side error or stale-snapshot error; the verification pass caught it.
- **Remediation applied:** `design-decision.md` "Explicit exclusions": "B-11 is excluded from this decision because `verification.md:193-207` refuted the global-install gap." Release-scope item closed without source edit.
- **Outcome:** B-11 excluded. The verification step prevented a remediation pass that would have invented a "global install workstream" for an issue that did not exist.
- **Still possible today (Auggie check):** SUCCESS path verified — verification.md is the structural defence here. Without it, B-11 would have triggered phantom work.
- **Source artifacts:** `roadmap-cli-skill-converge/release-scope.md` B-11, `roadmap-cli-skill-converge/verification.md:193-207`, `roadmap-cli-skill-converge/design-decision.md` (Explicit exclusions)

### F-A9-020: B-4 verification surfaced PRD-detection algorithm omission that scope-doc framing understated
- **Type:** REMEDIATION (verification step found an additional gap)
- **Pipeline step:** OTHER (extract — PRD/TDD detection)
- **Symptom:** `verification.md:92-106` — `refs/scoring.md:18` claims algorithm match with `executor.py:detect_input_type()`. Reality: `executor.py:73-148` checks PRD signals FIRST (5 PRD signals, threshold ≥5 returns "prd"), THEN TDD signals. The skill ref describes TDD-detection but its presentation order omits that PRD is checked first in CLI. PRD-detection rule was not documented at all even though the CLI implements it.
- **Root cause (claimed):** Skill ref drifted as PRD detection was added to the CLI; no doc-sync gate.
- **Remediation applied:** B-4 Option 1 chosen — re-derive scoring from `executor.py:73-148`, add §0 "PRD Detection (checked first)" with the 5 PRD signals, update line-18 cross-reference (`design-decision.md:34`).
- **Outcome:** Closed in Phase 2 of the converge release.
- **Still possible today (Auggie check):** YES — verifiable at `cli/roadmap/executor.py:73-148` per `verification.md`. The fix is current; the structural condition (no gate catches future drift) persists.
- **Source artifacts:** `roadmap-cli-skill-converge/verification.md:92-106`, `roadmap-cli-skill-converge/design-decision.md:34`, `roadmap-cli-skill-converge/solutions.md` B-4

### F-A9-021: Roadmap-cli-skill-converge release executed all phases to PASS — sync-and-verify model worked
- **Type:** SUCCESS
- **Pipeline step:** OTHER (full release closeout)
- **Symptom:** `CP-P05-END.md` documents 5/5 phases closed (Phase 1 B-1/B-2 commands; Phase 2 B-3-B-8 skill refs; Phase 3 B-9 disclaimer; Phase 4 B-10 deferral decision; Phase 5 B-12 sync + parity + regression). 68 tests passing across `/sc:roadmap` + `/sc:validate-roadmap` regression. `make verify-sync` exits 0 with "All components in sync."
- **Root cause (claimed):** N/A — success path.
- **Remediation applied:** N/A.
- **Outcome:** Release shipped with three-way md5 parity (`af661e03f8cf3db1990b53a1165f5ef2` for roadmap.md, `02b76e3a1ba62a9a29152fab18acd70b` for validate-roadmap.md) across `src/`, `.claude/`, `/config/.claude/`.
- **Still possible today (Auggie check):** SUCCESS path. The structural drift will recur unless a `--help`-driven sync test is added (B-1 Solution 3 was explicitly rejected as over-engineered).
- **Source artifacts:** `roadmap-cli-skill-converge/checkpoints/CP-P05-END.md`, `roadmap-cli-skill-converge/manifest.json`

### F-A9-022: Cleanup-audit-v2 spec-fidelity gate worked as designed — produced a deviation report with concrete recommendations
- **Type:** SUCCESS (mechanism)
- **Pipeline step:** spec-fidelity
- **Symptom:** `cleanup-audit-v2-UNIFIED-SPEC/spec-fidelity.md` is a well-formed 7-column deviation table with 8 deviations, each with ID/Severity/Deviation/Spec Quote/Roadmap Quote/Impact/Recommended Correction. Recommendations are specific and actionable (e.g., DEV-005: "Split budget controls: basic token tracking and `--budget` ceiling enforcement in Phase 0, graceful degradation logic in Phase 3 as currently placed").
- **Root cause (claimed):** N/A — success.
- **Remediation applied:** N/A.
- **Outcome:** Frontmatter `tasklist_ready: true`, `validation_complete: true`. Mechanism produced the artifact shape v2.20 designed for.
- **Still possible today (Auggie check):** SUCCESS path — gate definition exists per v2.20 FR-005, FR-006. The gate's recall (does it catch every HIGH-severity case?) was not measured.
- **Source artifacts:** `cleanup-audit-v2-UNIFIED-SPEC/spec-fidelity.md`

### F-A9-023: v2.20 adversarial-forensic-validation second-pass produced the foundational `forensic-foundation-validated.md` that drove v2.20 spec design
- **Type:** SUCCESS (compound mechanism)
- **Pipeline step:** OTHER (meta — adversarial-of-adversarial)
- **Symptom:** `v2.20-WorkflowEvolution/adversarial-forensic-validation/forensic-foundation-validated.md` is a merged synthesis of 4 peer artifacts (original 3 analyses + prior merged foundation, treated as co-equal peers). It produced 6 validated findings (F-001 through F-006), 4 theory items, 3 unresolved conflicts, and 4 hidden assumptions. The validation step explicitly noted T-004: "Prior synthesis can itself become a lossy compression layer — that's why the prior foundation was treated as a peer artifact rather than an authority."
- **Root cause (claimed):** N/A — this is the mechanism functioning correctly.
- **Remediation applied:** N/A — the validation output then drove v2.20's spec/extraction/roadmap.
- **Outcome:** v2.20 inherited a well-structured driver document. Whether v2.20's implementation closed the F-001 through F-006 gaps is partially answered (gates fixed) and partially not (the deeper category error T-001 remains unresolved as theory).
- **Still possible today (Auggie check):** SUCCESS path. The forensic-validation-of-forensic pattern is reusable but expensive; no evidence it has been re-run since.
- **Source artifacts:** `v2.20-WorkflowEvolution/adversarial-forensic-validation/forensic-foundation-validated.md`, `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md`

---

## Cross-cutting patterns within this partition

- **P1. Structural/format validation systematically substitutes for semantic validation across every pipeline boundary** — F-A9-005 (`_cross_refs_resolve` always-true), F-A9-010 (wiring-verification passes on wrong target_dir), F-A9-007 (convergence score gate only checks it parses), F-A9-018 (UNVALIDATED markers ship without gate intervention) all share the same architecture: gates check syntax, not meaning. v2.20 forensic foundation Finding F-001 names this directly.

- **P2. Skill/protocol documentation drifts silently from the CLI it claims to describe** — F-A9-003 (17 flag mismatches), F-A9-004 (5 waves vs 14 CLI steps), F-A9-008 (8-step extraction doc vs single CLI prompt), F-A9-020 (PRD detection algorithm absent from scoring.md) are four manifestations of the same condition: no automated `--help` ↔ skill-prose drift detection. The convergence release closed *this round*; the structural drift condition persists.

- **P3. "Tolerate uncertainty by silently skipping" is encoded as a design choice at multiple layers** — F-A9-002 (`/sc:brainstorm` smart detection defaults to skip on uncertainty), F-A9-013 (`--no-validate` ambiguity around spec-fidelity), F-A9-005 ("too fragile for now" returns True), and F-A9-009 (MEDIUM-severity deviations are non-blocking by policy) all institutionalize false-negative tolerance. The cumulative effect is that the failure mode of choice is silent degradation rather than loud rejection.

- **P4. Convergence scores below high-confidence thresholds ship as PASS because no gate enforces the threshold** — F-A9-007 (v2.20 at 0.72) and F-A9-012 (cleanup-audit-v2 at 0.86 vs 0.80 threshold) both indicate the convergence float is treated as a process metric, not a gate criterion. v2.13 (cited in F-A9-007 evidence) also shipped at 0.72.

- **P5. The pipeline learns backward but plans forward — retrospective findings post-date the next spec they should have constrained** — F-A9-014 (v2.07 retrospective dated 2026-03-05 vs v2.08 spec dated 2026-03-04, then `PARTIAL` status reproduced in the omitted enum) and F-A9-015 (v1 ships without validation; v2 must retrofit it) both show temporal disconnect between discovery and prevention. The v2.20 `--retrospective` flag is necessary but not sufficient — nothing structurally couples retrospective cadence to next-spec cadence.

- **P6. Cross-cutting infrastructure deferred to later phases creates validation gaps in earlier phases that no gate catches** — F-A9-009 specifically (DEV-004 subagent failure handling deferred to Phase 4; DEV-005 budget controls validated Phase 4 but implemented Phase 3) and F-A9-018 (UNVALIDATED estimates) both classify as MEDIUM and pass the spec-fidelity gate. The sequencing failure mode is well below the gate's HIGH-severity blocking threshold.

- **P7. Adversarial debate findings are partially incorporated downstream with no completeness check** — F-A9-011 (~85-90% incorporation, v2.07/v2.13/v2.20 all cite it) plus F-A9-012 (refactor-plan "Changes Not Being Made" catches *intentional* drops only). The merge step has no "every finding either ships or is explicitly deferred" invariant.

## Brittleness drivers identified

- **D1. No automated CLI ↔ docs drift detection.** Skill prose and `*.md` command files describe a flag set and pipeline taxonomy maintained independently of `cli/roadmap/commands.py` argparse definitions and `_get_all_step_ids`. No gate, test, or CI check converts a CLI change into a doc-update obligation. Drift is detected only by manual `/sc:analyze` passes (F-A9-003, F-A9-004, F-A9-008, F-A9-020). Even after the convergence release closed this round, the structural condition is intact.

- **D2. Gate framework allows shipping known-broken stubs with TODO comments.** `_cross_refs_resolve()` returning True with a "too fragile for now" comment shipped to production. Nothing in the gate-registration or CI pipeline prevents a stub-return from satisfying the gate API contract. This is the same condition that allows UNVALIDATED markers to coexist with PASS status (F-A9-005, F-A9-010, F-A9-018).

- **D3. Gate semantic checks validate float ranges, frontmatter key presence, and minimum line counts; they have no callable for "semantic agreement with input."** `_convergence_score_valid()` checks `[0.0, 1.0]`. `_has_actionable_content()` checks for any bullet/numbered item. `_high_severity_count_zero()` (v2.20) trusts the LLM's count. No gate compares produced content against source content beyond shape-matching (F-A9-005, F-A9-007, F-A9-010, F-A9-011).

- **D4. Severity classification is LLM-self-reported with no calibration mechanism.** `SPEC_FIDELITY_GATE` blocks on `high_severity_count > 0`, but the LLM both *classifies* and *counts* severity. A model that under-classifies a deviation as MEDIUM (e.g., DEV-004 in cleanup-audit-v2) passes the gate. The v2.20 design explicitly notes RSK-007 (severity classification drift) but does not solve it — only embeds severity definitions in the prompt as a partial mitigation (F-A9-009).

- **D5. `--no-codebase`, `--no-validate`, `--no-convergence`, `--strict-no-remediation` flags expose silent-skip surfaces at every pipeline stage.** The 2026-05-25 update-sweep in `design-decision.md` notes that even the convergence release added `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` / `--strict-no-remediation`. The product surface treats "let the operator turn off validation" as a first-class feature; the structural mechanism that converts those flags into auditable bypasses (e.g., logging which gate was bypassed in `.roadmap-state.json`) is unverified (F-A9-002, F-A9-013).

- **D6. The retrospective loop's temporal coupling is operator-mediated, not pipeline-enforced.** The `--retrospective` flag (F-A9-014) lets an operator inject prior findings, but no pipeline check halts spec emission until the latest retrospective has been ingested. The cross-release pattern (v1 → v2 cleanup-audit retrofit; v2.07 retrospective vs v2.08 spec) keeps recurring because cadence misalignment is structural (F-A9-014, F-A9-015).

- **D7. Brainstorm/extract upstream has no codebase-grounding requirement before downstream consumes its output.** v2.21 designed Phase 0 Auggie integration but framed it as opt-in/heuristic with explicit `--no-codebase`. The category of "spec written without ever consulting the code it describes" remains a valid pipeline input — and that spec then drives 41-deliverable roadmaps and 5-phase tasklists, none of which independently verify the spec's codebase claims (F-A9-001, F-A9-002, F-A9-017).

- **D8. Per-release verification mechanisms (`verification.md`) caught false positives — but they are not pipeline gates; they are bespoke release artifacts that may or may not be produced next time.** F-A9-019 (B-11 REFUTED) and F-A9-020 (B-4 PRD-detection gap surfaced) are successes of the verification step. The structural risk is that `verification.md` is not a required gate output — releases that skip it lose the false-positive defence and the additional-gap surface.
