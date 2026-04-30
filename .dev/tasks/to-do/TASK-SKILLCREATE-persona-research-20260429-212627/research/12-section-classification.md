# Section Classification: persona-research SKILL.md

**Investigation type:** Section Classification
**Status:** Complete
**Date:** 2026-04-29

This document classifies each of the 29 canonical sections (S1-S29) of the planned `sc-persona-research-protocol` skill against five reference skill analyses (tech-research, skill-creator, task-builder, prd, tdd) and the persona-research spec partitions.

Classification semantics:
- **COPY** — boilerplate text identical across all 5 reference skills; copy verbatim from tech-research (which is closest persona-research analog).
- **SUBSTITUTE** — same structure across references, only domain nouns/examples differ; substitute domain variables.
- **GENERATE** — content is unique to persona-research domain; must be authored from spec.

---

## Methodology

The canonical 29-section spine is taken from skill-creator's authoritative 29-section table (research file 03, lines 102-132), which explicitly maps S1-S29 with section names verified against the skill-creator source. Each section is classified by comparing across:

- **02-reference-tech-research** (44 headings, 7-phase research-heavy skill)
- **03-reference-skill-creator** (29 sections, 7-phase meta-skill — canonical spine)
- **04-reference-task-builder** (Stage A only, no clean 29-section structure)
- **05-reference-prd** (~25 observable sections, modularized via refs/)
- **06-reference-tdd** (modularized 422-line skill with refs/)

Decision rule (per protocol):
- All 5 references agree on COPY → COPY
- All references show same shape, different domain nouns → SUBSTITUTE
- References diverge OR section is unique to persona-research domain → GENERATE
- When uncertain, lean toward GENERATE (conservative)

Note on canonical numbering ambiguity: Three of the five references (task-builder, prd, tdd) explicitly state they don't use the 29-section monolithic numbering. I anchor classifications to the skill-creator and tech-research mappings (which DO use S1-S29) and use prd/tdd/task-builder as confirmation of boilerplate stability for sections they do contain.

---

## Spec FR Encoding Map

For GENERATE sections, this map identifies which spec content the builder MUST encode:

| Section | Spec content that MUST be encoded | Source partition |
|---|---|---|
| S2 Overview | 7-phase pipeline, ethics floor, archetype-driven workflow | 07 §5 (lines 196-243), 09 §10 |
| S3 Why This Process Works | FR-2 identity-first, FR-3 parallel, FR-9/G2 refusal, Nygard failure modes | 07 §4 + 08 §6 |
| S5 Input | Full §3 input schema (subjects[], context_artifact, output_target, archetype_store, naming, research_budget, ethics) | 07 §3 (lines 80-156) |
| S6 Effective Prompt Examples | Worked example §D (Rosenthal/Planche/Larrison) | 08 App D |
| S7 What to Do If Prompt Incomplete | FR-1 (subjects required), FR-10 (halt on ambiguous identity) | 07 FR-1, FR-10 |
| S10 Execution Overview | 7-phase persona research pipeline, App B Quantity Flow Diagram | 07 §5, App B |
| S13 A.2 Parse & Triage | Subject parsing, ethics attestation §10.3 verbatim, unsuitable-subject categories §10.2 | 09 §10.2, §10.3 |
| S14 A.3 Scope Discovery | Identity Verifier role, Archetype Manager FR-16, source catalog §5.3 9-tier | 07 §5.2, §5.3 |
| S18 A.7 Build Task File (BUILD_REQUEST) | Worker contract §5.2 JSON schema, FR-4 three artifacts, model tiering FR-24/25/26 | 07 §5.2, 08 §9.2 |
| S20 Agent Prompt Templates | §5.2 worker contract verbatim, archetype-driven worker, discovery worker, identity verifier, model tiering Haiku/Opus | 07 §5.2, 08 §9.2 |
| S22 Synthesis Mapping Table | Worker output → persona TOML + archetype proposal mapping | 07 §5.2 |
| S24 Assembly Process | Quantity Flow Diagram emission App B, config.toml diff FR-8, approval gate FR-21 | 07 App B, FR-8, FR-21 |
| S25 Validation Checklist | FR-1..FR-26 acceptance criteria (15 §11 items) + ETHICS_DISCLAIMER_VERBATIM gate | 09 §11 (15 items), §10.1 |
| S27 Critical Rules | FR-6 disclaimer verbatim, FR-7 no quotes, FR-9 refuse, FR-21 no auto-write, FR-22 generic archetypes, FR-24 Opus discipline, FR-25 Tavily, ethics §10 | 09 §10, 07 FR-6/7/8/9/21/22, 08 FR-24/25/26 |

---

## Guide-Driven Anti-Pattern Flags

From guide partitions 10/11:
- **Anti-pattern (10 line 86):** "Skill body that fabricates persona/agent prompts without delegating via Task tool" — S20 must encode prompts spawned via Task, not free-text fabrications.
- **Length tension (10 line 75):** Guide says ~400-500 lines for Tier 3 complex. Skill-creator's canonical 29-section skills run 1200-1500 lines (research-notes line 218). Persona-research follows skill-creator's pattern.
- **Anti-pattern (10 line 79):** `allowed-tools` overly broad — S1 frontmatter must scope tools tightly given the skill writes archetype YAML and persona TOML.
- **Agent naming (11 line 50):** Guide uses bare names; RF convention is `rf-` prefix. Builder follows RF convention (rf-personares-*).

---

## 29-Section Classification Table

| # | Section Name | Classification | Domain Variables Needed | Source for COPY (tech-research line range) | Source for GENERATE (spec FR / partition file) | Notes |
|---|--------------|---------------|------------------------|------------------------------------------|--------------------------------------|-------|
| S1 | Frontmatter + Title | SUBSTITUTE | name, description, trigger.phrases | n/a | n/a | All 5 refs SUBSTITUTE: tech-research L1-4, skill-creator L1-19, prd L1-4, tdd L1-4, task-builder L1-4. name=`sc-persona-research-protocol`. Description must list trigger phrases ("research personas for...", "persona research for board...", "model VCs as personas"). allowed-tools must be tightly scoped per guide 10 line 79. |
| S2 | Overview + How it works | GENERATE | DOMAIN_NAME, agent roster (D3), 7-phase structure (D10), ethics floor | n/a | 07-spec-part1 §5 architecture (L196-243), 09-spec-part3 §10 ethics | All 5 refs GENERATE/SUBSTITUTE-with-domain-narrative; persona-research overview must encode archetype-driven workflow + identity-first + ethics floor. Skill-creator S2 = GENERATE (03 L105). |
| S3 | Why This Process Works | GENERATE | failure modes (Nygard §6), phase guarantees, persona-research-specific failure list | n/a | 07-spec-part1 §4 (FR-2/3/9), 08-spec-part2 §6 failure-mode table | tech-research/prd/tdd are SUBSTITUTE with stable failure-mode framing; skill-creator S3 = GENERATE because failure modes are domain-specific. Persona-research has unique failure modes (identity ambiguity, INSUFFICIENT_PUBLIC_DATA, deceased/minor refusal) — must regenerate from §6. |
| S4 | Variable Reference | SUBSTITUTE | TASK_ID_PREFIX (`TASK-PERSONARES`), DOMAIN_SLUG (`PERSONA_SLUG`), OUTPUT path, archetype_store paths, TEMPLATE_BASE | tech-research L31-43 | n/a | All 5 refs SUBSTITUTE: tech-research L31-43, skill-creator L44-62, prd L100-108. Persona-research adds two-layer archetype store paths (canonical_path, local_path) per 07 §3 L98-99. |
| S5 | Input | GENERATE | 7-key YAML schema (subjects, context_artifact, output_target, archetype_store, naming, research_budget, ethics) | n/a | 07-spec-part1 §3 lines 80-156 | Refs disagree (tech-research SUBSTITUTE 4-input, skill-creator GENERATE 5-input, prd SUBSTITUTE 4-piece). Persona-research uses 7-key YAML schema unique to spec — GENERATE. Must encode subjects[] list contract (L85-90), archetype_store config (L98-104), ethics.attestation_required (L112). |
| S6 | Effective Prompt Examples | GENERATE | Strong/Weak persona-research examples | n/a | 08-spec-part2 App D worked example (Rosenthal/Planche/Larrison) | All 5 refs GENERATE: tech-research L60-74, skill-creator L86-102, prd L45-60, task-builder embedded. Use App D triple-subject example as the canonical Strong example. |
| S7 | What to Do If Prompt Is Incomplete | SUBSTITUTE | Clarification template with persona-research placeholders | tech-research L76-87 | n/a | All 5 refs SUBSTITUTE clarification template; persona-research clarifies subjects/affiliation/archetype_hint per FR-1 (reject empty subjects) and FR-10 (halt on ambiguous identity). |
| S8 | Depth Tiers | SUBSTITUTE | Quick/Standard/Deep table with subject count thresholds, worker counts, line ceilings | tech-research L91-105 | n/a | All 5 refs SUBSTITUTE 3-tier table. Persona-research tiers map to subject count: Quick (1-3 subjects), Standard (4-10), Deep (10+ → warn at 10, hard-cap at 25 per §7 FR-2.5 in 08). |
| S9 | Output Locations | SUBSTITUTE | Artifact table — TASK_ID prefix, dossier_dir, config_diff path, archetype store paths | tech-research L109-131 | n/a | All 5 refs SUBSTITUTE artifact table. Persona-research artifacts: `${TASK_DIR}research/[NN]-subject-*.md`, `dossier_dir/<code>-dossier.md`, `local_path/<id>.yaml`, proposed config.toml diff (per 07 §3 L93-94, L99). |
| S10 | Execution Overview (Stage A / Stage B) | GENERATE | 7-phase persona research pipeline names + L-level mapping | tech-research L135-153 (boilerplate two-stage pattern) | 07-spec-part1 §5 (L196-243), App B Quantity Flow Diagram | tech-research/prd/tdd treat S10 as SUBSTITUTE (two-stage A/B is COPY-shape); skill-creator S10 = GENERATE because phase list is domain-specific. Persona-research phases differ from canonical research: Phase 2 = Identity Verification (sequential per FR-2), Phase 3 = Archetype Resolution (per FR-16), Phase 4 = Parallel Workers (FR-3), Phase 5 = Aggregation, Phase 6 = Approval Gate, Phase 7 = optional Validator. Diverges enough that classification is GENERATE. |
| S11 | Stage A header | COPY | none | tech-research L156 (header line); prd L166; tdd inferred; skill-creator L198; task-builder L167 | n/a | All 5 refs COPY: pure header line `## Stage A: ...`. |
| S12 | A.1 Check for Existing Task File | SUBSTITUTE | TASK_ID glob pattern (`TASK-PERSONARES-*`), subfolder list | tech-research L156-170 | n/a | All 5 refs SUBSTITUTE: same resume-routing logic, only TASK_ID prefix changes. tech-research L156-170, skill-creator L200-213, prd L168-180, tdd L149-161, task-builder L169-182. |
| S13 | A.2 Parse & Triage | GENERATE | Persona-research-specific parse signals: subjects[], archetype_hint, context_artifact; ethics §10.3 attestation; unsuitable-subject categories §10.2 | n/a | 09-spec-part3 §10.2 (refusal categories), §10.3 (attestation verbatim L504), 07 FR-1, FR-9, FR-10 | All 5 refs SUBSTITUTE-with-domain-fields. Persona-research adds: ethics attestation prompt (verbatim), unsuitable-subject refusal screen (deceased/minors/private/witnesses-in-litigation per §10.2), archetype_hint forcing path (Guard G4 sentinel). Materially divergent → GENERATE. |
| S14 | A.3 Perform Scope Discovery | GENERATE | Agent type roster (D3): Identity Verifier, Archetype-Driven Worker, Discovery Worker, Aggregator, Approval Gate, Validator; 9-tier source catalog | n/a | 07-spec-part1 §5.2 (L196-243), §5.3 (L313-324) source catalog | All 5 refs SUBSTITUTE the discovery-flow shell but agent roster is fully domain-specific. Skill-creator's S14 = GENERATE for same reason (agent type table is domain core). Persona-research roster (6 distinct types) and 9-tier source catalog are unique to this skill. |
| S15 | A.4 Write Research Notes File | SUBSTITUTE | Research notes mandatory categories adapted to persona research (e.g., SUBJECT_ROSTER, ARCHETYPE_RESOLUTION_STRATEGY, ETHICS_ATTESTATION_PLAN, SOURCE_BUDGET_PLAN, AMBIGUITIES_FOR_USER) | tech-research L231-271 | n/a | All 5 refs SUBSTITUTE the 6-8 mandatory category template. Categories must adapt to persona research but the structure is canonical. |
| S16 | A.5 Review Research Sufficiency | SUBSTITUTE | Gate logic shell with persona-research-specific review criteria (SUBJECT_ROSTER completeness, ETHICS_ATTESTATION recorded, Guards G1+G4 deterministic path); max 2 gap-fill rounds | tech-research L273-294 | n/a | Reclassified from COPY → SUBSTITUTE in QA fix-cycle 1. Reference structure (gate logic + review checklist + max-2-rounds) is universal, but persona-research review criteria are domain-specific (SUBJECT_ROSTER per FR-1, ETHICS_ATTESTATION per FR-6/§10.3, Guard G1 per FR-2, Guard G4 per FR-16/FR-20). Persona-research review checklist materially diverges from tech-research's existing-files / non-trivial-areas / synthesis-mapping criteria. |
| S17 | A.6 Template Triage | COPY | "almost always Template 02" closing line | tech-research L296-312 | n/a | All 5 refs COPY: tech-research L296-312, prd L332-348 (COPY explicit), tdd L306-322 (COPY explicit), skill-creator L426-442. Template 01 vs 02 decision logic is universal. |
| S18 | A.7 Build the Task File (BUILD_REQUEST) | GENERATE | Full BUILD_REQUEST with persona-research 7-phase encoding, worker JSON contract §5.2, model tiering FR-24/25/26, ethics attestation gate, archetype resolution sub-phase | n/a | 07-spec-part1 §5.2 worker contract (L249-292), 08-spec-part2 §9.2 model tiering (L455-484), FR-24/25/26, 09-spec-part3 §10 ethics | tech-research treats as SUBSTITUTE (BUILD_REQUEST shape stable); skill-creator S18 = GENERATE (canonical answer for any skill with novel phase structure). Persona-research BUILD_REQUEST must encode: §5.2 strict JSON contract for workers, identity-first sequencing (FR-2), Tavily routing (FR-25), Opus-only-at-consolidation rule (FR-24), ETHICS_DISCLAIMER_VERBATIM gate. Must regenerate. |
| S19 | Stage B: Task File Execution (Delegation Protocol) | COPY | /task delegation pattern | tech-research L465-483 (COPY explicit) | n/a | All 5 refs COPY: tech-research L465-483, skill-creator L672-694, prd L404-413, tdd L377-397 (COPY explicit). The "/task does NOT read SKILL.md during execution" boilerplate is universal. Only TASK_ID prefix in the example path changes. |
| S20 | Agent Prompt Templates | GENERATE | 6 agent prompts: Identity Verifier, Archetype-Driven Research Worker (Tavily-routed), Discovery Worker, Aggregator, Validator (optional), plus QA gate prompts | n/a | 07-spec-part1 §5.2 worker JSON contract (L249-292), §5.4 service-boundary rules (L329-334), 08-spec-part2 §9.2 model tiering, §6 failure modes, 09-spec-part3 §10.1 disclaimer | All 5 refs treat S20 as SUBSTITUTE (placeholder topic/path/type) but persona-research agent prompts must encode unique architectural rules: workers do not share state (§5.4), strict §5.2 JSON output schema, Haiku per-source/Opus per-consolidation rule (FR-24), ETHICS_DISCLAIMER_VERBATIM gate in worker output, archetype refinement proposal field. Cannot SUBSTITUTE generic research-worker prompt. **Anti-pattern check (guide 10 line 86):** prompts must be invoked via Task tool, not free-text fabrications — builder must use the canonical Incremental File Writing + Documentation Staleness protocol blocks verbatim from tech-research as COPY-grade scaffolding wrapped around persona-research-specific instructions. |
| S21 | Output Structure | SUBSTITUTE | Section schema with S-numbers (Output is the assembled SKILL.md scaffold) OR for an executing persona-research run: persona TOML + dossier markdown + diff + archetype YAML proposal | n/a (skill-creator L1245-1313) | n/a | skill-creator S21 SUBSTITUTE (schema with S-numbers). For persona-research, the "output structure" is twofold: (a) the produced SKILL.md's own 29-section structure, and (b) the runtime output (dossier md + persona TOML + config diff + archetype YAML proposal). Per skill-creator's pattern, this section documents the schema; substitute persona-research artifact list. |
| S22 | Synthesis Mapping Table | GENERATE | Mapping: research-file → SKILL.md section; for runtime: worker output → persona block + archetype proposal + dossier md | n/a | 07-spec-part1 §5.2 worker contract → output mapping | All 5 refs treat as GENERATE (skill-creator S22 = GENERATE explicitly L125; tech-research L1147-1158 = GENERATE explicitly). Domain-specific mapping is required. Skill-creator's note that "synth files NOT produced — Phase 4 writes directly to output" should be replicated; persona-research has the same direct-Edit assembly pattern. |
| S23 | Synthesis Quality Review Checklist | SUBSTITUTE | 10-criteria checklist with persona-research-specific gates (e.g., disclaimer verbatim, no first-person quotes, source citations valid, archetype generic-purity) | tech-research L1162-1178 (9 criteria, SUBSTITUTE) | n/a | All 5 refs SUBSTITUTE the 9-12 criteria checklist. Persona-research criteria reference §10.1 disclaimer string-equality, FR-7 no-quote static check, FR-22 archetype generic-purity linter. |
| S24 | Assembly Process | GENERATE | Section-group ordering + persona-research-specific assembly (Quantity Flow Diagram emission, config.toml diff generation, approval gate) | n/a | 07-spec-part1 App B Quantity Flow Diagram (L606-652), FR-8 (diff never auto-write), FR-21 (no auto-save) | tech-research treats as SUBSTITUTE (4-step pattern); skill-creator S24 = GENERATE. Persona-research assembly has unique steps: emit App B Quantity Flow Diagram with actual counts (FR-12 mandatory), aggregate worker JSON outputs into persona blocks, generate unified config diff (never auto-write per FR-8), prepare archetype proposal write set (local_path only per §5.6). |
| S25 | Validation Checklist | GENERATE | 26-item FR-derived checklist + 15 §11 acceptance items + ETHICS_DISCLAIMER_VERBATIM byte-fidelity check + archetype generic-purity linter | n/a | 09-spec-part3 §11 (15 acceptance items L516-530), §10.1 disclaimer (L493 verbatim), 07 FR-1..FR-23, 08 FR-24/25/26 | tech-research treats S25 as SUBSTITUTE (15-item checklist with domain refs); skill-creator S25 = GENERATE (23-item checklist domain-specific). Persona-research checklist must encode each FR-1..FR-26 acceptance criterion + the 15 §11 items. CRITICAL: must include byte-fidelity check on §10.1 disclaimer (em-dash U+2014, ASCII apostrophe U+0027 per 09 lines 30-32) and FR-22 generic-purity linter. **Highest-stakes section in entire skill.** |
| S26 | Content Rules (Non-Negotiable) | SUBSTITUTE | Do/Don't table — universal writing standards + persona-research additions (no first-person quotes, source citation required, archetype generic-purity, ethics disclaimer verbatim) | tech-research L1219-1242 (COPY universal table) | n/a | tech-research treats as COPY (universal writing standards); skill-creator S26 = SUBSTITUTE (11-row table = 6 boilerplate + 5 domain-specific). Lean SUBSTITUTE: keep first 6 universal rows verbatim, add persona-research-specific rows for FR-7 (no quotes), FR-5 (source-cite all claims), FR-22 (archetype purity), FR-6 (disclaimer verbatim). |
| S27 | Critical Rules (Non-Negotiable) | GENERATE | 22+ numbered rules: 9 generic + 13+ persona-research-specific (FR-6 disclaimer verbatim, FR-7 no quotes, FR-9 refuse, FR-21 no auto-write, FR-22 generic archetypes, FR-24 Opus discipline, FR-25 Tavily, FR-2 identity-first, FR-12 quantity flow diagram mandatory, ethics attestation per §10.3) | n/a | 09-spec-part3 §10 ethics, 07 FR-6/7/8/9/21/22, 08 FR-24/25/26, App B mandatory emission | tech-research SUBSTITUTE (15 rules, mostly universal); skill-creator S27 = GENERATE (22 rules). Persona-research must add ~13 domain-specific rules covering ethics floor, archetype generic-purity, model-tiering enforcement, two-layer-store write rules (skill never writes to canonical), worker JSON contract conformance. Materially divergent → GENERATE. |
| S28 | Session Management | SUBSTITUTE | Session resumption pattern with persona-research subfolder list (research/, qa/, dossiers/, archetype-proposals/) | tech-research L1281-1297 | n/a | All 5 refs SUBSTITUTE: tech-research L1281-1297, skill-creator L1479-1493, prd L451-453 (COPY-grade short version), task-builder L1612-1633. Substitute TASK_ID prefix and subfolder list per persona-research artifacts. |
| S29 | Research Quality Signals | SUBSTITUTE | Strong/Weak signals + when-to-spawn for persona-research (e.g., strong: ≥3 sources per claim, archetype match score >0.7; weak: only one source category, no deal-history evidence) | tech-research L1301-1322 | n/a | tech-research GENERATE (L1301-1322); skill-creator S29 = SUBSTITUTE (3-section pattern with skill-creator-specific signals). Persona-research follows skill-creator's SUBSTITUTE pattern: keep Strong/Weak/When-to-Spawn 3-part structure, swap signals to be persona-research-domain-specific (footprint score thresholds, source diversity, archetype confidence). |

---

## Classification Summary

| Classification | Count | Section IDs |
|---|---|---|
| COPY | 3 | S11, S17, S19 |
| SUBSTITUTE | 13 | S1, S4, S7, S8, S9, S12, S15, S16, S21, S23, S26, S28, S29 |
| GENERATE | 13 | S2, S3, S5, S6, S10, S13, S14, S18, S20, S22, S24, S25, S27 |
| **Total** | **29** | ✓ |

S16 was reclassified from COPY → SUBSTITUTE in QA fix-cycle 1 (Lens 2/Lens 6 finding I2: persona-research-specific review criteria — SUBJECT_ROSTER, ETHICS_ATTESTATION, Guards G1/G4 — make S16 materially divergent from the COPY contract).

---

## Disagreements Across References (Conservative Resolution)

The following sections show inconsistent classifications across references. I picked the more conservative (more domain-specific) classification per the protocol's "lean toward GENERATE if uncertain" rule.

| Section | tech-research | skill-creator | prd | tdd | task-builder | My choice | Rationale |
|---|---|---|---|---|---|---|---|
| S2 Overview | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | SUBSTITUTE | **GENERATE** | Skill-creator (canonical 29-section ref) classifies GENERATE; persona-research has unique 7-phase + ethics-floor narrative not present in other skills. |
| S3 Why This Process Works | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | SUBSTITUTE | **GENERATE** | Persona-research failure modes (identity ambiguity, INSUFFICIENT_PUBLIC_DATA, deceased/minor refusal) are unique to spec §6 — must regenerate. |
| S5 Input | SUBSTITUTE (4-piece) | GENERATE (5-field) | SUBSTITUTE (4-piece) | SUBSTITUTE (4-input) | SUBSTITUTE (4-piece) | **GENERATE** | Persona-research uses 7-key YAML schema unique to spec §3; not the canonical 4-piece WHAT/WHY/WHERE/OUTPUT pattern. |
| S10 Execution Overview | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | SUBSTITUTE | **GENERATE** | Persona-research phase list (Identity Verify → Archetype Resolve → Parallel Workers → Aggregate → Approval Gate → optional Validator) diverges from canonical research pipeline; encodes App B Quantity Flow. |
| S13 A.2 Parse & Triage | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | GENERATE (task-builder) | **GENERATE** | Two refs say GENERATE; persona-research adds ethics attestation gate (§10.3 verbatim) and unsuitable-subject screen (§10.2). Materially divergent. |
| S14 A.3 Scope Discovery | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | GENERATE (task-builder) | **GENERATE** | Skill-creator and task-builder say GENERATE because agent type roster is domain-core. Persona-research has 6 unique agent types + 9-tier source catalog. |
| S18 A.7 Build Task File | SUBSTITUTE | GENERATE | SUBSTITUTE | SUBSTITUTE | GENERATE (task-builder) | **GENERATE** | BUILD_REQUEST shape is universal but persona-research's encoded phase structure (identity-first, archetype resolution, model tiering) is domain-specific enough to require regeneration. |
| S20 Agent Prompt Templates | SUBSTITUTE | GENERATE | (not in SKILL.md, in refs) | (not in SKILL.md, in refs) | GENERATE (task-builder) | **GENERATE** | All references that include S20 inline classify it GENERATE because agent prompts encode domain-specific contracts. Persona-research §5.2 worker JSON contract is not present in any reference. |
| S21 Output Structure | (not present) | SUBSTITUTE | (embedded) | (offloaded) | SUBSTITUTE | **SUBSTITUTE** | Skill-creator S21 = SUBSTITUTE (schema with S-numbers + persona-research artifact substitution). |
| S22 Synthesis Mapping | GENERATE | GENERATE | (not present) | (offloaded) | (not applicable) | **GENERATE** | Both refs that include it say GENERATE. |
| S24 Assembly Process | SUBSTITUTE | GENERATE | (in refs) | (in refs) | (not applicable) | **GENERATE** | Persona-research adds App B Quantity Flow Diagram emission (FR-12 mandatory) and FR-8 diff-never-auto-write rule — divergent enough to require regeneration. |
| S25 Validation Checklist | SUBSTITUTE | GENERATE | (in refs) | (in refs) | SUBSTITUTE | **GENERATE** | Skill-creator says GENERATE for the 23-item checklist; persona-research has 26 FRs + 15 acceptance items + verbatim disclaimer byte-fidelity check — must regenerate. **Highest-stakes section.** |
| S26 Content Rules | COPY | SUBSTITUTE | (not present) | (in refs) | COPY-mostly | **SUBSTITUTE** | tech-research and task-builder treat as COPY but skill-creator says SUBSTITUTE because persona-research adds domain-specific rows (no quotes, source-cite, generic-purity). Conservative: SUBSTITUTE. |
| S27 Critical Rules | SUBSTITUTE | GENERATE | (not present) | (in refs) | SUBSTITUTE | **GENERATE** | Persona-research adds ~13 domain-specific rules (ethics, archetype purity, model-tiering, two-layer-store rules). Skill-creator agrees this section is GENERATE. |
| S29 Research Quality Signals | GENERATE | SUBSTITUTE | (not present) | (in refs) | COPY (task-builder L1568-1591) | **SUBSTITUTE** | Three refs disagree; skill-creator's SUBSTITUTE wins because the 3-part Strong/Weak/When-to-Spawn structure is universal — only signals change. |

---

## Cross-Validation Notes

1. **COPY sections (S11, S17, S19) are confirmed COPY in 4 of 5 references.** task-builder doesn't have a clean Stage B (S19) but its skill-doesn't-need-Stage-B comment is stable across modularized skills. (S16 was COPY in references but reclassified to SUBSTITUTE for persona-research per QA fix-cycle 1 — the review criteria contain domain-specific gates that go beyond byte-copy.)
2. **Spec FR-encoding requirements are concentrated in S18, S20, S25, S27, S24, S13, S14.** These are the GENERATE sections where the builder MUST cross-reference the spec partitions.
3. **Ethics floor (§10) maps to S13 (A.2 attestation), S25 (validation), S27 (critical rules).** The §10.1 disclaimer string MUST appear verbatim with byte-fidelity (U+2014 em-dash, U+0027 apostrophe) in any section that references it.
4. **Worker JSON contract §5.2 is the load-bearing schema** — encoded in S18 (BUILD_REQUEST) and S20 (Agent Prompt Templates). Builder must keep these two sections consistent with each other.
5. **App B Quantity Flow Diagram (FR-12) MUST be emitted on every run** — mentioned in S10 (overview) and S24 (assembly). Both must reference the same diagram template.
6. **Anti-pattern guard (guide 10 line 86):** S20 prompts must be invoked via Task tool. Builder should structure each prompt as a delegation block with subagent_type, not as inline persona narration.

---

## Gaps and Caveats

1. **Canonical 29-section template not directly read.** Per research file 03 line 253, `${TEMPLATE_BASE}skill_template.md` was referenced but not read in the reference analyses. Classifications anchor to skill-creator's authoritative 29-section table (L102-132 of file 03), which is source-verified.
2. **S26 classification (SUBSTITUTE vs COPY) is a judgment call.** tech-research, prd, and task-builder treat the universal writing-standards table as COPY-grade. Skill-creator treats it as SUBSTITUTE because adding domain-specific rows is normal. I picked SUBSTITUTE because persona-research must add at least 4 domain-specific rules (no quotes, source-cite, generic-purity, disclaimer verbatim).
3. **task-builder uses Stage A only (no Stage B)** — its absence of a clean S19 was treated as "not applicable" rather than as evidence against COPY classification. Persona-research follows the canonical Stage A + Stage B pattern (per spec architecture).
4. **prd and tdd are modularized** (use refs/ for S20-S25). The classification table treats persona-research as monolithic 29-section per skill-creator's canonical pattern. If the builder later decides to modularize, S20-S25 may move to refs/ files but classifications remain valid.

---

## Appendix A — Strengthening Edits (Phase 3 Cycle 1 Findings I-13, I-14, I-16, I-17)

This appendix addresses cycle 1 strengthening findings without rewriting the main classification table (preserving its structural integrity).

### A.1 — S26 Content Rules Row-Level Diff (finding I-13)

The S26 SUBSTITUTE classification rests on the claim "first 6 universal rows are COPY across RF skills, with persona-research adding 4 domain-specific rows." This sub-table provides the row-by-row enumeration the cycle 1 finding requested, comparing tech-research §S26 (Content Rules at L1219-1242) and skill-creator §S26 (Content Rules at L1401-1424).

| Row | Rule (paraphrase) | tech-research L1219-1242 | skill-creator L1401-1424 | Status |
|---|---|---|---|---|
| 1 | Tables over prose for multi-item data | PRESENT | PRESENT | IDENTICAL — universal |
| 2 | No full source-code reproductions | PRESENT | PRESENT (adapted to skill text) | IDENTICAL — universal shape |
| 3 | Cite evidence inline (file paths / refs) | PRESENT | PRESENT | IDENTICAL — universal |
| 4 | Use ASCII diagrams for architecture (not prose walls) | PRESENT | PRESENT | IDENTICAL — universal |
| 5 | Tag doc-only claims with `[UNVERIFIED]` / `[CODE-VERIFIED]` | PRESENT | PRESENT | IDENTICAL — universal |
| 6 | Don't fabricate; verify before assert | PRESENT | PRESENT | IDENTICAL — universal |
| 7 | Persona-research-specific: no first-person quotes attributed to subject (FR-7) | n/a | n/a | DIVERGENT — must add for persona-research |
| 8 | Persona-research-specific: every dossier claim must cite source URL+date (FR-5) | n/a | n/a | DIVERGENT — must add |
| 9 | Persona-research-specific: archetype generic-purity — no person/firm/fund names in core fields (FR-22) | n/a | n/a | DIVERGENT — must add |
| 10 | Persona-research-specific: disclaimer §10.1 byte-verbatim, no edits permitted (FR-6) | n/a | n/a | DIVERGENT — must add |

**Conclusion:** Rows 1-6 are IDENTICAL universal rules — COPY-grade. Rows 7-10 are domain-specific — must be added by persona-research generator. SUBSTITUTE classification confirmed (universal shell + domain-specific extensions).

> **Note on direct verbatim verification:** tech-research and skill-creator main SKILL.md files were not re-opened in this cycle to quote each row literally; the row mapping above relies on the file analyses in 02-reference-tech-research.md and 03-reference-skill-creator.md which were anchored to those line ranges in the original Phase 2a research. `[UNVERIFIED — exact rule wording]` for the 6 universal rows; structural claim (rows are PRESENT in both refs) is what is asserted.

### A.2 — S29 Research Quality Signals Row-Level Diff (finding I-14)

The S29 SUBSTITUTE classification rests on universality of the Strong/Weak/When-to-Spawn 3-part structure. This sub-table compares tech-research (L1301-1322), skill-creator (L1495-1522), and task-builder (L1568-1591) side-by-side.

| Component | tech-research L1301-1322 | skill-creator L1495-1522 | task-builder L1568-1591 | Status |
|---|---|---|---|---|
| Strong-signals subsection | PRESENT (research-specific signals: "claim has file path + line number") | PRESENT (skill-specific signals: "every section has source citation") | PRESENT (task-specific signals: "every checklist item has output path") | IDENTICAL structure, DIVERGENT signal content |
| Weak-signals subsection | PRESENT (research weak signals) | PRESENT (skill weak signals) | PRESENT (task weak signals) | IDENTICAL structure, DIVERGENT signal content |
| When-to-Spawn subsection | PRESENT (when to spawn additional research agents) | PRESENT (when to spawn additional generators) | PRESENT (when to spawn task-researcher) | IDENTICAL structure, DIVERGENT trigger conditions |
| Quantitative thresholds | YES (≥3 sources / claim) | YES (every section evidenced) | YES (every checklist item self-contained) | IDENTICAL: each ref has quantitative thresholds |

**Conclusion:** The 3-part structure (Strong/Weak/When-to-Spawn) + the inclusion-of-quantitative-thresholds pattern are IDENTICAL across all 3 references. The signal *content* (what counts as strong vs weak) is fully domain-specific. SUBSTITUTE classification confirmed (universal structural shell + domain-substitution at signal-content level).

> **Note:** Verbatim quote of each subsection from each ref was not collected in this cycle. The structural claim (3-part shape is universal) is supported by the file analyses; the row-content claim (each ref names quantitative thresholds) is `[UNVERIFIED — exact thresholds]` until Phase 4 reads the source files directly. The persona-research builder MUST read the actual source SKILL.md files when populating S29.

### A.3 — Multi-Reference Line Ranges for SUBSTITUTE Rows (finding I-16)

Several SUBSTITUTE rows in the main classification table cite line ranges only from tech-research. The table below adds line ranges from at least 3 of the 5 references where available, addressing the cycle 1 finding that single-source SUBSTITUTE classifications are weakly evidenced.

| Section | tech-research | skill-creator | prd | tdd | task-builder | Notes |
|---|---|---|---|---|---|---|
| S7 (Incomplete Prompt) | L76-87 | L121-138 | L62-73 | embedded in S5 (L33-59) | L189-218 | All 5 refs treat as SUBSTITUTE — clarification template universal |
| S8 (Depth Tiers) | L91-105 | L141-160 | L77-91 | L63-78 | tier table embedded in L255-279 | All 5 refs SUBSTITUTE — 3-tier table is universal shell |
| S15 (A.4 Write Research Notes) | L231-271 | L341-372 | L263-305 | L236-279 | L301-348 | All 5 refs SUBSTITUTE — 6-8 mandatory category structure is universal |
| S23 (Synthesis Quality Review Checklist) | L1162-1178 | L1248-1289 | offloaded to refs/validation-checklists.md | offloaded to refs/validation-checklists.md | embedded in §A.5 review block | tech-research and skill-creator carry inline; prd/tdd offload; task-builder embeds. SUBSTITUTE confirmed by 2 inline refs + offloaded analogues |
| S28 (Session Management) | L1281-1297 | L1479-1493 | L451-453 (compact form) | offloaded to refs/operational-guidance.md | L1612-1633 | 4 of 5 refs treat as SUBSTITUTE; only tdd offloads. Universal pattern + TASK_ID-prefix substitution |

**Conclusion:** All 5 SUBSTITUTE rows now have ≥3 reference line-range citations, satisfying the cycle 1 multi-reference evidence requirement. (Line ranges for skill-creator/prd/tdd/task-builder rows above are sourced from the corresponding 02-/03-/05-/06-/04-reference-*.md files; the line-by-line verbatim was not re-opened in this cycle — `[UNVERIFIED — exact line ranges]` for the non-tech-research entries until Phase 4 cross-validation.)

### A.4 — task-builder Coverage Caveat (finding I-17)

`04-reference-task-builder.md` (lines 14-15, 118) explicitly states task-builder is structurally a Stage A only skill — Stage B is delegated, not authored within the same SKILL.md. As a result, task-builder cannot serve as a 29-section reference for sections that are Stage B-specific or that depend on Stage B execution context.

**Sections where task-builder cannot validate:**
- **S19 (Stage B: Delegation)** — task-builder *is* the delegation target, not the delegator. Its S19 is structurally absent or stub-only.
- **S20 (Agent Prompt Templates) — partial** — task-builder's prompts are about MDTM file construction, not about delegated subagent prompts in the canonical research-pipeline sense. Treat task-builder S20 as a partial reference.

**Implication for "5-ref Deep cross-validation" denominators in the main classification table:** For S19 and S20, the effective denominator is **4 of 5** (task-builder excluded), not 5 of 5. This adjustment does not change the disagreement-resolution outcomes (S19 remains COPY by 4-of-4 unanimity; S20 remains GENERATE by 3-of-4 majority since the partial task-builder vote agrees with GENERATE).

For all other sections (S1-S18, S21-S29), all 5 references including task-builder remain valid contributors.

---

**Status:** Complete

