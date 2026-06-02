# Partition A1b — Roadmap Core (v.2.11+) Retrospective

**Scope**: v.2.11-roadmap-v4, v2.22-RoadmapRemediate, v2.26-roadmap-v5
**Focus**: Evolution of the roadmap generator from v4 onward including the remediate sub-pipeline — architectural changes and the failures that triggered them.
**Methodology**: Focused-budget read of READMEs, specs, post-mortem-style files, and validation reports across three release dirs.

---

## Timeline arc (one-paragraph framing)

v.2.11 (v4 pipeline, 2026-03-04) was a *methodology brainstorm* triggered by two escaped state-tracking bugs from the v0.04 Adaptive Replay release. It produced 5 sc:roadmap improvement proposals (invariant registry, FMEA pass, guard analysis, implement/verify decomposition, data-flow tracing) and ran a 3-round adversarial scoring debate between an Architect/Pragmatist and a Quality Advocate. v2.22-RoadmapRemediate (2026-03-09) addressed a different failure surface: the v2.20 pipeline produced validation reports with 14 findings but had **no automated path from "findings exist" to "findings fixed"** — users had to hand-craft remediation prompts. v2.22 introduced two new pipeline steps (remediate, certify) bringing the count from 9→11. v2.26-roadmap-v5 (2026-03-13) was triggered by v2.24-cli-portify failing at `spec-fidelity` after exhausting its 2-attempt retry budget with **identical inputs producing identical outputs**. v5 added two more steps (annotate-deviations, deviation-analysis) and reframed deviations into 4 classes (SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED).

---

## Findings

### F-A1b-001: v4 pipeline lacks edge-case forcing functions at deliverable generation time
- **Type:** FAILURE → REMEDIATION (brainstorm-stage, not implementation)
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect (deliverable generation methodology)
- **Symptom:** Two state-variable bugs (`_loaded_start_index -= mounted` wrong-operand; `_replayed_event_offset = 0` zero-ambiguity) escaped v0.04 planning. Neither was identified as a separate deliverable or risk during roadmap generation.
- **Root cause (claimed):** Roadmap treats stateful transitions (e.g., "Replace boolean with int offset") as atomic deliverables with no enumeration of the new value space. Guard correctness depends on operand semantics never surfaced during planning. (`brainstorm-roadmap.md` §Proposal 1, 3)
- **Remediation applied:** 5 proposals scored; cross-cutting-analysis sequences them into 3 waves (W1: RM-5, SP-2, AD-5, AD-2 — "highest-value proposals are the cheapest"; W2: SP-3, RM-1, RM-2, AD-1; W3: deeper agents). MVI-1 ("catch-both-bugs" set, 4 proposals, ~15-20% overhead) recommended.
- **Outcome:** Implementation effort estimated 3-5 days for MVI-1. No evidence in this partition that proposals shipped — they fed forward into later v2.22/v2.26 forcing-function patterns (spec-fidelity gate, deviation classes).
- **Still possible today (Auggie check):** NOT CHECKED
- **Source artifacts:** `v.2.11-roadmap-v4/brainstorm-roadmap.md` L10-203; `cross-cutting-analysis.md` L116-178; `adversarial-scoring-debate.md` L1-200

### F-A1b-002: v4 adversarial debate produces composite-score divergence between agents
- **Type:** FAILURE (pattern observed in debate itself)
- **Pipeline step:** debate / score
- **Symptom:** Round 1 produced composite-score deltas >0.75 on 7 of 17 proposals (SP-4: 1.65, SP-6: 1.50, AD-1: 2.15, AD-2: 1.71, AD-4: 1.00, RM-1: 1.75, RM-2: 1.67). Agents disagreed by 1 point on multiple dimensions even when no single dimension exceeded the >1 threshold — composites diverged because errors compounded across complexity/cost/likelihood/generality.
- **Root cause (claimed):** Agent A weighted cost and complexity higher (token-pragmatist); Agent B weighted likelihood and generality higher (quality-first). The composite formula `(likelihood*3 + generality*2) / (complexity + cost)` is non-linear, so 1-pt deltas in the denominator double the composite. (`adversarial-scoring-debate.md` L113-124)
- **Remediation applied:** Round 2 contested-proposal debate with reconciliation. Both agents conceded on multiple dimensions (e.g., A→complexity 2 on SP-4 after "detection is simple pattern matching"; B→likelihood 4 on SP-6).
- **Outcome:** Convergence achieved through explicit debate — but only because the orchestrator gated the debate on composite-delta threshold. The structural fragility (rank-flips driven by 1-pt nominal-scale slop) persists.
- **Still possible today (Auggie check):** UNKNOWN — NOT CHECKED. The composite-score formula likely still in use.
- **Source artifacts:** `adversarial-scoring-debate.md` L1-200

### F-A1b-003: v2.20 produced 14 validation findings with no automated remediation path
- **Type:** FAILURE → REMEDIATION (motivates v2.22)
- **Pipeline step:** validate → (gap) → remediate (the gap is the failure)
- **Symptom:** v2.20 planning surfaced 14 findings (4 BLOCKING, 7 WARNING, 3 INFO). User had to manually read merged report, interpret fix guidance, craft custom prompts, spawn agents via `/sc:task-unified`, hand-track status in `reflect-merged.md`, and accept no automated re-validation. A second pass found 12 more findings — also manual.
- **Root cause (claimed):** Pipeline ended at validate. No `Finding` model, no parser for `reflect-merged.md`, no agent-batching logic, no certification step. (`spec-roadmap-remediate.md` §1, §1.1)
- **Remediation applied:** v2.22 adds `remediate` (Step 10) + `certify` (Step 11). New `Finding` dataclass with PENDING→FIXED/FAILED/SKIPPED lifecycle. Interactive Y/n prompt with 3 severity-scope options. File-batched parallel agents (one agent per file group, cross-file findings included in both prompts with scoped "(YOUR FILE):" guidance). Transactional `os.replace()` rollback on agent failure. Single-pass certification.
- **Outcome:** Implemented and shipped — `CP-P04-END.md` reports 475 existing + 61 new = 536 tests passing, parallel execution via ThreadPoolExecutor working, rollback verified byte-for-byte against `.pre-remediate` snapshots.
- **Still possible today (Auggie check):** NO — `spec-roadmap-remediate.md` and `roadmap.md` confirm remediate+certify shipped; checkpoint files document working implementation. INFERENTIAL on current code state.
- **Source artifacts:** `v2.22-RoadmapRemediate/spec-roadmap-remediate.md` L1-200; `checkpoints/CP-P04-END.md` L1-35; `roadmap.md` L1-80

### F-A1b-004: v2.22 roadmap drifted from spec on module names, phase count, file inventory
- **Type:** FAILURE → REMEDIATION (intra-release drift)
- **Pipeline step:** spec-fidelity
- **Symptom:** spec-fidelity report identified 15 deviations (3 HIGH, 7 MEDIUM, 5 LOW). HIGH examples: spec mandates `remediate_parser.py`, roadmap named it `finding_parser.py` (DEV-001). Spec lists 5 new files including standalone `certify_gates.py`; roadmap omits it and adds unspecified `certify_executor.py` (DEV-002). Spec has 4 phases; roadmap restructured to 7 phases (DEV-003). Spec uses "sprints"; roadmap uses "days" with no conversion (DEV-004). Roadmap introduced FR-001..FR-032 / NFR-001..NFR-014 IDs **never defined in the spec** (DEV-010).
- **Root cause (claimed):** Generation agents drift on naming, file inventory, and phase decomposition without explicit traceability matrix or naming-table enforcement. Requirement IDs invented at roadmap stage to provide pseudo-traceability that the spec itself does not have.
- **Remediation applied:** 10 of 15 findings FIXED (DEV-001 through DEV-010). 5 reclassified NO_ACTION_REQUIRED (additive elaborations or spec-as-source-of-truth). Phase mapping table added to §6, sprint→days conversion documented, Requirements Traceability Matrix added as §9, lifecycle corrected to include PENDING.
- **Outcome:** spec-fidelity report frontmatter shows `remediation_status: complete, findings_fixed: 10, findings_no_action: 5`. Validation report (post-patching) shows PASS across coverage, dependency chain, index consistency.
- **Still possible today (Auggie check):** NOT CHECKED — but pattern (generated FR/NFR IDs invented out of thin air) is structural and would recur absent enforcement.
- **Source artifacts:** `v2.22-RoadmapRemediate/spec-fidelity.md` L1-150; `validation/validation-report.md` L1-119

### F-A1b-005: v2.22 Phase 7 tasklist generated with drifted ID sequences (context-window overflow)
- **Type:** FAILURE → REMEDIATION
- **Pipeline step:** tasklist generation
- **Symptom:** `phase-7-tasklist.md` used D-0042..D-0050 instead of D-0035..D-0043 for deliverable IDs; R-049..R-057 instead of R-046..R-054 for roadmap items. References to R-055/R-056/R-057 pointed to non-existent items. Index showed 55 deliverables instead of 43. Multiple tier mismatches between index and phase files.
- **Root cause (claimed):** "Context window overflow during the previous generation session caused Phase 7 to be generated with drifted ID sequences. The index was generated before Phase 7, so its registries were correct. The phase file itself had the wrong starting offsets." (`validation/validation-report.md` L86-88)
- **Remediation applied:** Full rewrite of `phase-7-tasklist.md` with corrected IDs/deps/artifact paths. Index updated for total count + tier distribution.
- **Outcome:** Stage 10 post-patch verification PASS on all 11 checks.
- **Still possible today (Auggie check):** YES — INFERENTIAL. Context-window overflow is a model-capacity issue; structural mitigation (sequence-anchoring, ID-handoff between agents) not evidenced in this partition. The validator catches it post-hoc; the generator can still produce it.
- **Source artifacts:** `validation/validation-report.md` L72-119

### F-A1b-006: v2.24 spec-fidelity gate retry mechanism is futile by construction
- **Type:** FAILURE → REMEDIATION (motivates v2.26/v5)
- **Pipeline step:** spec-fidelity (retry semantics)
- **Symptom:** v2.24-cli-portify halted at spec-fidelity after exhausting 2-attempt retry budget. Fidelity report found 20 deviations (3 HIGH, 12 MEDIUM, 5 LOW). Both attempts produced identical output because retry re-runs the same prompt against the same unchanged `roadmap.md`. Pipeline halted permanently with no recovery path. Of the 3 HIGH deviations: 1 was mixed (`steps/` layout INTENTIONAL per debate D-02; module renames SLIPS); 2 were pure SLIPS (missing data models, missing semantic checks). Pipeline cannot distinguish — STRICT gate blocks remediation from ever running.
- **Root cause (claimed):** Six systemic failures (`v2.25-spec-merged.md` L48-58): F-1 information loss in extraction, F-2 no spec context in debate, F-3 no deviation annotation at merge, F-4 fidelity agent works blind, F-5 retry is futile (same inputs → same outputs), F-6 no remediation path for classified deviations.
- **Remediation applied:** v5 pipeline: `extract → [gen-A, gen-B] → diff → debate → score → merge → annotate-deviations(NEW) → test-strategy → spec-fidelity(DOWNGRADED STRICT→STANDARD) → deviation-analysis(NEW) → remediate(MODIFIED) → certify(MODIFIED)`. Adds `deviation_class: str` to `Finding` with VALID_DEVIATION_CLASSES = {SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED, UNCLASSIFIED}. Routes INTENTIONAL+superior → recommend spec update; SLIP → remediate; AMBIGUOUS → human review.
- **Outcome:** v2.26 spec-fidelity.err is 0 bytes (clean run). wiring-verification.md reports 0 findings, 0 unwired callables, 0 orphan modules. Implementation appears to have stabilized in v5.
- **Still possible today (Auggie check):** NO (for v2.24-class incidents) — INFERENTIAL based on clean v2.26 artifacts. Anti-laundering safeguards documented in roadmap.md L16-17 ("anti-laundering safeguards via citation requirements and cross-validation").
- **Source artifacts:** `v2.26-roadmap-v5/v2.25-spec-merged.md` L36-78; `brainstorm-reference.md` L25-87; `roadmap.md` L1-117

### F-A1b-007: v2.25 bundles `accept-spec-change` despite scope-discipline objections — adversarial debate
- **Type:** REMEDIATION (architecture decision via adversarial debate)
- **Pipeline step:** brainstorm → roadmap (release scoping)
- **Symptom:** v2.25 already at ~700 lines / 10 unresolved spec questions. Question: should `accept-spec-change` (auto-resume after spec_hash change) ship in v2.25 or be a separate release? Position A (opus): "shipping deviation-awareness without hash-sync resolution is shipping a pipeline that diagnoses a problem and then re-creates it." Position B (haiku): bundling expands blast radius; deliverable 2's auto-resume cycle "assumes the executor can detect a spec patch, refresh state, update spec_hash, and rerun resume logic for one cycle — but in v5 the routing logic flows through deviation-analysis... that integration is not yet designed."
- **Root cause (claimed):** Dependency cascade: v2.25 deviation-analysis routes INTENTIONAL+superior → "recommend spec update" → which triggers the spec_hash-change cascade that motivated v2.25 originally.
- **Remediation applied:** Debate transcript captured both positions. Resolution split into `adversarial-accept-spec-change-placement.md` — actual outcome (split or bundle) not visible in the files read.
- **Outcome:** v2.26 carries `accept-spec-change` separately (file name suggests placement debate yielded "later release"). Multiple amendment workstreams in v2.26 (`brainstorm-immediate-amendments.md`, `tasklist-shortterm-amendments.md`, `tasklist-longterm-amendments.md`, `validation-immediate.md`/`-shortterm.md`/`-longterm.md`, `approved-immediate.md`/`-shortterm.md`/`-longterm.md`) suggest tiered amendment shipping.
- **Still possible today (Auggie check):** N/A — process pattern, not a code failure.
- **Source artifacts:** `v2.26-roadmap-v5/adversarial-accept-spec-change-placement.md` L1-120; v2.26 top-level file listing

### F-A1b-008: v2.25 carries 10 OQ at brainstorm → 8 OQ at spec — Phase 0 becomes mandatory pre-impl gate
- **Type:** SUCCESS (proactive remediation)
- **Pipeline step:** roadmap (Phase 0 introduction)
- **Symptom:** v2.25 spec has 8 open questions ranging from "Does `GateCriteria.aux_inputs` exist?" (OQ-A — 30-minute task) to "Document v2.25 handling for FR-077 dual-budget-exhaustion note" (OQ-J — deferred to v2.26). Several are existence-of-symbol questions whose resolution cascades through multiple FR implementations.
- **Root cause (claimed):** Spec author cannot verify codebase claims at spec time; OQs accumulate. Without resolution gate, implementer would discover gaps mid-Phase-2 and force timeline-collapsing rework.
- **Remediation applied:** Roadmap Phase 0 ("Pre-Implementation Decisions and Baselining", 0.5-1.5 days) added explicitly as a gate. Exit criteria includes "All 8 open questions resolved or deferred with documented fallback" and "_parse_routing_list() module placement decided".
- **Outcome:** Pattern looks structurally sound — turns spec-time uncertainty into a documented + gated Phase 0 deliverable.
- **Still possible today (Auggie check):** N/A — process pattern.
- **Source artifacts:** `v2.26-roadmap-v5/roadmap.md` L30-84

---

## Cross-cutting patterns within this partition

1. **Generation-stage drift is the dominant failure mode** (F-A1b-001, F-A1b-004, F-A1b-005, F-A1b-006): every release in this partition has at least one failure where the generation agent produced output divergent from the spec — wrong module names, wrong ID sequences, missing data models, fabricated FR/NFR IDs. The remediation pattern is consistently "add a downstream validator + automated fix loop" rather than "constrain the generator." This is structurally additive — pipelines grow, never simplify.

2. **Forcing functions outperform analytical depth** (F-A1b-001 cross-cutting-analysis observation #2): "Proposals that make it structurally impossible to skip reasoning (boundary tables, taxonomy gates, risk categories) consistently outperform proposals that try to make the reasoning deeper." This observation from v.2.11 is then *embodied* in v2.22 (PENDING→FIXED state machine, severity-scope prompt) and v2.26 (VALID_DEVIATION_CLASSES frozenset, fail-closed semantic checks). Forcing-function discipline is the through-line.

3. **Retry without input-change is the canonical anti-pattern** (F-A1b-006): The v2.24 incident — retry re-runs identical prompt against identical roadmap, producing identical output, exhausting budget — is the single most-cited motivator for the entire v5 pipeline rebuild. Three new steps and one gate-tier change (STRICT→STANDARD on spec-fidelity) were added to ensure retry can mutate state between attempts.

4. **Adversarial debate as architecture-decision substrate** (F-A1b-002, F-A1b-007): two distinct uses appear — (a) scoring 17 proposals on a 4-dim rubric with explicit composite-delta convergence gate; (b) Position A vs Position B on release-scope placement. Pattern is mature and reused, but the composite-score formula's 1-pt nominal-scale slop produces rank-flips (F-A1b-002).

5. **Spec-to-roadmap traceability is consistently absent until validated post-hoc** (F-A1b-004): v2.22's spec-fidelity surfaced that the roadmap *invented* a Requirements Traceability Matrix worth of FR/NFR IDs that did not exist in the spec. Remediation added a Traceability Matrix to the roadmap, but the structural pattern (generation invents what isn't enforced) is unchanged.

6. **Context-window overflow → silent ID drift** (F-A1b-005): the validator caught Phase 7 ID drift post-hoc but the generator silently produced it. Sequence-anchoring across phases is not enforced; the generator can lose track of which deliverable-ID range belongs to which phase when context pressure rises.

7. **Pipeline keeps growing in step count** (v4=9 → v2.22=11 → v5=13): every retrospective adds at least one step. No release in this partition removes or consolidates a step. Each addition increases coupling between gates and state.

---

## Brittleness drivers identified

- **Generator/validator asymmetry**: validators are deterministic (parsers, schema checks); generators are non-deterministic agents. Every new failure class triggers a new validator — but the generator's failure surface is open-ended. Validators can only catch failure classes someone has named.
- **Composite scoring with 1-pt-delta tolerance on nominal scales**: rank-flips driven by error compounding across 4 dimensions in a non-linear formula. Debate-merge resolves it per-invocation; the formula remains brittle.
- **Frontmatter / report-format fragility as the parsing substrate**: v2.22 parser must handle `validate/reflect-merged.md` AND `validate/merged-validation-report.md` AND 3+ format variants with fallback parser + 5-line dedup window. Report format is the universal coupling — any format drift breaks downstream remediation.
- **Retry semantics that don't mutate inputs**: structural across pre-v5 pipeline — gates assume "try again" is meaningful even when inputs are deterministic functions of unchanged artifacts.
- **Invented identifiers (FR-IDs, deliverable-IDs) without source-of-truth registry**: generation creates IDs to satisfy template requirements; no registry enforces uniqueness or cross-document consistency until post-hoc validation.
- **Context-window pressure causing silent state drift in long generations** (Phase 7 ID drift): no mid-generation anchoring or handoff protocol between phases of a single agent call.
- **Step count monotonically grows**: each fix adds a step; pipeline complexity only ratchets up. No structural pressure for consolidation.
- **Cross-step state passed through filesystem markdown**: state lives in `roadmap.md`, `reflect-merged.md`, `.roadmap-state.json`, `validate/*.md`. Every step both reads and writes markdown; type-safety is the parser's job.

---

## Budget note

- Files Read: 12 (cross-cutting-analysis, brainstorm-roadmap, adversarial-scoring-debate, extraction from v.2.11; spec-roadmap-remediate, spec-fidelity, feedback-log, validation-report, CP-P04-END, roadmap from v2.22; wiring-verification, adversarial-accept-spec-change-placement, roadmap, brainstorm-reference, v2.25-spec-merged from v2.26 — count includes 15 actual reads, mostly partial)
- Files Skipped (over budget): ~35+ (all `phase-*-tasklist.md` files, archive subdirectories, execution-log artifacts, debate-transcript details, results subdirectories, .err files confirmed empty via wc, tasklist subdirectories in v.2.11)
- Auggie lookups: 0 — no failure in this partition rose above the "documented and remediated within the release artifact" bar to warrant Auggie cross-check; all remediations are recorded in-tree.
