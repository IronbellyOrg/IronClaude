# Research Notes: sc-persona-research-protocol Skill Creation

**Date:** 2026-04-29
**Scenario:** A (explicit, spec-driven request)
**Depth Tier:** Deep
**Source spec:** `/config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md` (993 lines)
**Best-practices guide:** `/config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (2088 lines)
**Status:** Complete

---

## CONFIRMED INPUTS (post user-confirmation A.3 Step 3)

| Field | Value |
|---|---|
| DOMAIN_NAME | `sc-persona-research-protocol` |
| DOMAIN_SLUG | `sc-persona-research-protocol` |
| OUTPUT_TYPE | distributed (multi-artifact: dossiers + persona TOML blocks + archetype YAMLs + run summary; user-configured paths) |
| REFERENCE_SKILLS | tech-research, skill-creator, task-builder, prd, tdd (5 — Deep tier) |
| AGENT_FILES | `true` — generate `rf-personares-archetype-driven-research-worker` and `rf-personares-discovery-worker` |
| TASK_ID_PREFIX | `TASK-PERSONARES` |
| QA_INTENSITY | full (Deep tier default) |

---

## EXISTING_FILES

### Existing skill corpus (`.claude/skills/`)

| Skill | Lines | TASK_ID_PREFIX | Format type | Use as reference? |
|---|---|---|---|---|
| `tech-research` | 1322 | TASK-RESEARCH | Full 29-section RF | YES — primary structural reference |
| `skill-creator` | 1522 | TASK-SKILLCREATE | Full 29-section RF (meta) | YES — lens-based QA + parallel-agent meta-pattern |
| `task-builder` | n/a | TASK-BUILDER | Full 29-section RF | YES — QA gate orchestration patterns |
| `prd` | n/a | TASK-PRD | Full 29-section RF | YES — template-driven scope discovery |
| `tdd` | n/a | TASK-TDD | Full 29-section RF | YES — template-driven scope discovery |
| `tech-reference` | n/a | TASK-TECHREF | Full 29-section RF | secondary — single-doc output |
| `task` | n/a | n/a | Execution skill | not a generation skill — out of scope |
| `confidence-check` | n/a | n/a | Utility skill | out of scope |
| `sc-cleanup-audit-protocol` | 133 | n/a | Slash-command behavioral protocol (NOT 29-section) | out of scope as structural reference; confirms NOT to follow |
| `sc-pm-protocol` | 178 | n/a | Slash-command behavioral protocol (NOT 29-section) | out of scope as structural reference |
| `sc-roadmap-protocol`, `sc-tasklist-protocol`, `sc-recommend-protocol`, `sc-validate-roadmap-protocol`, `sc-validate-tests-protocol`, `sc-release-split-protocol`, `sc-review-translation-protocol`, `sc-cli-portify-protocol`, `sc-task-unified-protocol`, `sc-adversarial-protocol` | n/a | n/a | Slash-command behavioral protocols | out of scope as structural references |

**Naming convention finding:** `sc-`-prefixed skills can be EITHER short slash-command behavioral protocols (~150 lines) OR full 29-section RF skills. The spec explicitly mandates the latter ("29-section RF format"), so we follow `tech-research` / `skill-creator` / `prd` / `tdd` shape and ignore the short-protocol shape used by other `sc-*-protocol` skills. The skill name retains the `-protocol` suffix per the spec's frontmatter.

### Templates

| Path | Status | Use |
|---|---|---|
| `.claude/templates/documents/skill_template.md` | **MISSING** | Should exist per skill-creator's `${TEMPLATE_BASE}skill_template.md` reference, but does not. Reference skills (especially `tech-research`) act as the de-facto template. |
| `.claude/templates/workflow/02_mdtm_template_complex_task.md` | EXISTS | Template 02 — used by task-builder for the MDTM task file. |
| `.claude/templates/workflow/01_mdtm_template_generic_task.md` | EXISTS | Template 01 — not used (we're using 02 for complex multi-phase work). |

### Spec & guide source files

| Path | Lines | Role |
|---|---|---|
| `/config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md` | 993 | Source-of-truth specification (FRs, architecture, ethics, validation, appendices) |
| `/config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | 2088 | Best-practices guide for SuperClaude commands/skills/agents authoring conventions |

### Existing TASK_ID_PREFIX inventory (for D1 uniqueness check)

`TASK-RESEARCH`, `TASK-SKILLCREATE`, `TASK-BUILDER`, `TASK-PRD`, `TASK-TDD`, `TASK-TECHREF`, `TASK-AUDIT`. Chosen prefix `TASK-PERSONARES` does not collide. ✅

---

## PATTERNS_AND_CONVENTIONS (extracted from reference skill survey)

### Section ordering (29-section RF convention, verified against tech-research line numbers)

| # | Section | tech-research line | Type |
|---|---|---|---|
| S1 | YAML frontmatter + `# Title` | 1-12 | SUBSTITUTE |
| S2 | Overview paragraph + "How it works" | 7-13 | GENERATE |
| S3 | Why This Process Works | 14 | GENERATE (failure modes + phase guarantees) |
| S4 | Variable Reference | (subsection of S3) | SUBSTITUTE |
| S5 | Input | 47 | GENERATE |
| S6 | Effective Prompt Examples | (subsection of S5) | GENERATE |
| S7 | What to Do If the Prompt Is Incomplete | (subsection of S5) | GENERATE |
| S8 | Depth Tiers | 91 | GENERATE |
| S9 | Output Locations | 109 | GENERATE |
| S10 | Execution Overview | 135 | GENERATE |
| S11 | Stage A: Scope Discovery & Task File Creation (header) | 156 | COPY (header only) |
| S12-S18 | A.1-A.7 sub-sections | 156-237 | SUBSTITUTE (boilerplate flow with domain hooks) |
| S19 | Stage B: Task File Execution | 465 | COPY (delegation to /task) |
| S20 | Agent Prompt Templates | 556 | GENERATE (agent prompts + VERBATIM protocol blocks) |
| S21 | Output Structure | 969 | GENERATE (per spec §3 outputs) |
| S22 | Synthesis Mapping Table (Reference) | 1147 | GENERATE |
| S23 | Synthesis Quality Review Checklist | 1162 | GENERATE |
| S24 | Assembly Process | 1182 | GENERATE |
| S25 | Validation Checklist | 1197 | GENERATE (FR-1..FR-26 acceptance) |
| S26 | Content Rules | 1219 | GENERATE (with domain-specific rows for ethics/disclaimer/no-quote-attribution/archetype-purity) |
| S27 | Critical Rules | 1245 | GENERATE (FR-2 sequential identity gate, FR-22 generic-purity, FR-25 Tavily routing) |
| S28 | Session Management | 1281 | COPY (boilerplate) |
| S29 | Research Quality Signals | 1301 | SUBSTITUTE (domain-specific signal lists) |

### Boilerplate vs domain content boundaries

| Boundary | Verbatim? | Source |
|---|---|---|
| Variable Reference table format (TASK_ID, TASK_DIR, RESEARCH, SYNTHESIS, QA, REVIEWS, TEMPLATE_BASE, OUTPUT) | COPY structurally; SUBSTITUTE values | tech-research lines 36-46 |
| Stage A header + A.1-A.7 step labels | COPY labels; SUBSTITUTE inner content | tech-research lines 156-237 |
| Stage B delegation protocol | COPY (with DOMAIN_NAME substituted) | tech-research lines 465-555 |
| Incremental File Writing Protocol block (in agent prompts) | COPY VERBATIM | tech-research lines ~570-595 (in each agent prompt) |
| Documentation Staleness Protocol block | COPY VERBATIM | tech-research lines (research agent prompts) |
| ADVERSARIAL STANCE block (QA agent prompts) | COPY VERBATIM | tech-research / skill-creator QA prompts |
| Critical Rules 1-9 (codebase as source-of-truth, evidence-based, etc.) | COPY VERBATIM | tech-research lines 1245-1280 |
| Critical Rules 10-22 | DOMAIN-EXTEND (skill-creator pattern adds rules 10-22 for skill-specific concerns) | skill-creator lines 1393-1438 |

### Agent type roster conventions

- **rf-task-researcher** (generic) for codebase research
- **rf-analyst** for completeness verification (Phase 3 — research gate)
- **rf-qa** for structural validation (Phase 5)
- **rf-qa-qualitative** for content/qualitative validation (Phase 5/6)
- **rf-assembler** for final consolidation (omitted when incremental Edit-based assembly is used, as in skill-creator Phase 4)
- Domain-specific worker agents are created via **agent-creator** nesting in Phase 7

### QA gate conventions (lens-based, serialized fix authorization)

| Gate | Phase | Min agents (full) | Pattern |
|---|---|---|---|
| Research Completeness | Phase 3 | 6 (2 rf-analyst + 2 rf-qa + 2 rf-qa-qualitative across completeness/cross-validation/evidence-quality/gap-detection/research-depth/research-breadth lenses) | report-only → consolidate → 1 fix agent → 2 verification agents; max 3 cycles |
| Structural + Qualitative | Phase 5 | 6 lens (3 rf-qa structural: template-conformance/internal-consistency/evidence-quality + 3 rf-qa-qualitative content: actionability/domain-accuracy/section-classification-accuracy) + 3 source-fidelity agents (Gate 2.5) | same serialized pattern; max 2 cycles each |
| Final QA | Phase 6 | 6+ lens (2 rf-qa: template-conformance/completeness + 4 rf-qa-qualitative: actionability/numbers-metrics/domain-noun-leakage/section-classification-accuracy) | same; max 2 cycles |

### Multi-phase incremental assembly

Pattern from skill-creator Phase 4 (preferred over rf-assembler one-shot):

1. Sub-phase 1: Create `OUTPUT_PATH` with frontmatter + S1-S4 (Edit append)
2. Sub-phase 2: Append S5-S18 (domain sections)
3. Sub-phase 3: Append S19-S20 (Stage B + Agent Prompt Templates)
4. Sub-phase 4: Append S21-S29 (Output structure + validation + rules)

Rationale: 1300-1500 line target exceeds single-Write limits and we want resumability if a sub-phase fails.

---

## REFERENCE_SKILL_ANALYSIS

### Reference set for Deep tier (5 skills)

| Skill | Why selected | What we extract |
|---|---|---|
| **tech-research** | Closest analog — parallel research, multi-phase, scope discovery, distributed outputs, validation gates | 29-section structure baseline; all boilerplate sections (S11/S12-S18 Stage A flow; S19 Stage B delegation; S28 Session Management); agent prompt protocol blocks (Incremental Writing, Documentation Staleness); Critical Rules 1-9 |
| **skill-creator** | Meta-pattern — lens-based QA, source-fidelity gates, agent-creator nesting, ethics-style content rules | Lens-based QA pattern with serialized fix; agent-creator nesting in Phase 7; multi-phase incremental Edit pattern; Critical Rules 10-22 extensions |
| **task-builder** | QA gate orchestration; rf-analyst/rf-qa/rf-qa-qualitative dispatch | Phase 3 research-gate pattern; structural/qualitative gate ordering; "self-contained checklist item" B2 enforcement |
| **prd** | Template-driven scope discovery; user-confirmation pattern; output to file | A.3 confirmation-prompt format; Stage A research-notes structure; Tier Selection table format |
| **tdd** | Template-driven gen; multi-input handling | Multi-input scope-discovery extraction; cross-references to PRD; phase mapping |

### 10-Differentiator Domain Model (CONFIRMED)

| # | Differentiator | Confirmed Value | Confidence | Reasoning / Evidence |
|---|---|---|---|---|
| **D1** | TASK_ID_PREFIX | `TASK-PERSONARES` | HIGH | Stripped+truncated DOMAIN_NAME; collision-checked vs existing prefixes (TASK-RESEARCH, TASK-SKILLCREATE, TASK-BUILDER, TASK-PRD, TASK-TDD, TASK-TECHREF, TASK-AUDIT) |
| **D2** | Slug field name | `SUBJECT_SLUG` | HIGH | Spec §3 inputs use `subjects[]` as primary entity; "subject" is the recurring noun across §4 FRs and §5 architecture |
| **D3** | Agent type roster | Identity Verifier (sequential), Archetype Manager (deterministic Python — no LLM), Archetype-Driven Research Worker (parallel), Discovery Worker (parallel, NO_MATCH path), Aggregator, Validator (optional, post-approval) | HIGH | Spec §5.1 component model; §5.2 worker contract; §5.4 service-boundary rules |
| **D4** | Scope classification | A (single named subject) / B (1-N named subjects with optional context_artifact + parallel batch) + 3-tier Quick/Standard/Deep | HIGH | Spec §2 user stories US-1 vs US-2; §7 FR-2.5 batch limits (warn>10, hard-cap 25 unless --force-large-batch) |
| **D5** | Line ceiling | None | HIGH | Output is multi-artifact (dossier + TOML + diff + summary), not navigational. The skill itself targets 1200-1500 lines (Deep tier). |
| **D6** | Output location pattern | distributed — `<dossier_dir>/<code>-dossier.md` (markdown), persona TOML blocks (in unified diff), proposed `archetype.yaml` files (to local store), run summary at `<dossier_dir>/<isodate>-run-summary.json`, three-questions test files. User-configurable paths. | HIGH | Spec §3 inputs/outputs; §9 operational concerns; §9.1 promotion workflow |
| **D7** | QA lens phase names | `personares-{template-conformance, internal-consistency, evidence-quality, actionability, domain-accuracy, section-classification-accuracy, ethics-disclaimer-compliance, identity-verification-flow, archetype-generic-purity, source-fidelity}` | HIGH `[CODE-VERIFIED]` | Standard 6 lenses + 4 domain-specific lenses derived directly from spec FRs verbatim:<br>• FR-2 (spec line 165): "Skill SHALL run identity verification BEFORE deep research for every subject. `identity_verified` must be `true` before the research subagent for that subject is spawned." → `identity-verification-flow` lens.<br>• FR-6 (spec line 169): "Persona descriptions SHALL include the 'modeled on' disclaimer verbatim (§10). String-equality check before the description is written to disk." → `ethics-disclaimer-compliance` lens.<br>• FR-7 (spec line 170): "Persona descriptions SHALL NOT contain first-person quotes attributed to the real person. Static check: no quoted strings preceded by `<Name> said` or `<Name>:` patterns." → folded into `ethics-disclaimer-compliance` lens.<br>• FR-22 (spec line 185): "Archetypes SHALL be generic — they SHALL NOT contain person names, company names, or fund names in their core fields. … Linter rule." → `archetype-generic-purity` lens.<br>• Spec §10 ethics layer (lines 487-509) anchors the broader ethics-disclaimer-compliance lens including §10.1 verbatim disclaimer + §10.2 output discipline. |
| **D8** | Validation requirements | Base 3 (TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION) + 4 domain-specific: ETHICS_DISCLAIMER_VERBATIM (FR-6), NO_FIRST_PERSON_ATTRIBUTION (FR-7), ARCHETYPE_GENERIC_PURITY (FR-22 — linter rule), IDENTITY_VERIFIED_BEFORE_RESEARCH (FR-2 sequential gate); plus output-shape validations: WORKER_JSON_CONTRACT_CONFORMANCE (§5.2), PIPELINE_QUANTITY_FLOW_DIAGRAM_EMITTED (FR-12), GUARD_BOUNDARY_TABLE_EMITTED (§A) | HIGH `[CODE-VERIFIED]` | Each validation requirement traces verbatim to spec §11 Acceptance Criteria (lines 512-530):<br>• ETHICS_DISCLAIMER_VERBATIM ← spec line 518: "The mandatory disclaimer (§10.1) appears verbatim in every produced persona description."<br>• NO_FIRST_PERSON_ATTRIBUTION ← spec FR-7 line 170 + spec §10.2 line 497: "No attributed novel quotes. Persona speaks in patterns…, never in invented direct speech…"<br>• ARCHETYPE_GENERIC_PURITY ← spec line 524: "Archetype generic-purity test: A linter check rejects any archetype containing person names, fund names, or company names in core fields (FR-22)."<br>• IDENTITY_VERIFIED_BEFORE_RESEARCH ← spec FR-2 line 165 (verbatim, see D7).<br>• WORKER_JSON_CONTRACT_CONFORMANCE ← spec §5.2 (lines 232-258 — worker-output JSON contract).<br>• PIPELINE_QUANTITY_FLOW_DIAGRAM_EMITTED ← spec line 522: "Skill emits a non-empty Quantity Flow Diagram and Guard Boundary Table on every run."<br>• GUARD_BOUNDARY_TABLE_EMITTED ← same line 522. |
| **D9** | Additional input fields | 6 extra fields beyond GOAL/WHY/WHERE: `subjects[]` (1-N entries with name/affiliation/role/aliases/archetype_hint), `context_artifact` (optional path), `output_target{dossier_dir, config_diff}`, `archetype_store{canonical_path, local_path, merge_policy, match_threshold:0.7, ambiguity_band:0.10, refinement_mode, promotion_candidates}`, `naming{code_prefix, archetype_companion}`, `research_budget{per_subject_minutes:12, archetype_discovery_minutes:18}`, `ethics{attestation_required:true}` | HIGH | Spec §3 input schema (verbatim) |
| **D10** | Phase structure | 7-phase (default) | HIGH | Phase 1 Preparation (L0) → Phase 2 Reference Skill Analysis / source-spec partitioning (L1) → Phase 3 Research Completeness Verification (L4) → Phase 4 Skeleton Assembly + Domain Generation (L2) → Phase 5 Lens-Based Structural+Qualitative QA + Source-Fidelity Gate (L4) → Phase 6 Lens-Based Final QA (L6) → Phase 7 Present Results + Agent-Creator Nesting (L0) |

### Additional inferred values

| Variable | Value | Source |
|---|---|---|
| `DOMAIN_NOUN_PLURAL` | "Persona dossiers / modeled personas" | Spec title |
| `FAILURE_MODE` | "Fabricated quotes attributed to real people; identity confusion (wrong human modeled); insufficient public footprint masked by fabrication; archetype contamination with subject-specific data; auto-write of config without approval" | Spec §6 + §10.2 |
| `TRACE_TARGET` | "Public posture signals (regulatory filings, deal history, on-chain activity, long-form publications, audio/video, social, adjacency leakage, trade press, hostile coverage)" | Spec §5.3 nine-tier source catalog |
| `TRIGGER_PATTERNS` | "research a persona for [name]", "build modeled persona for [name]", "stress-test against [investor name]", "persona dossier for [name] at [firm]", "model board persona on [name]", "/sc:persona-research", "create personas for [list of names]" | Spec §1, §2 |

### Section classification table (reference-skill driven, 29 rows — preview; full classification produced by Phase 2 agents)

| # | Section | Classification | Domain Variables Needed | Notes |
|---|---|---|---|---|
| S1 | Frontmatter + Title | SUBSTITUTE | DOMAIN_NAME, description, trigger phrases | name=`sc-persona-research-protocol` |
| S2 | Overview + How it works | GENERATE | DOMAIN_NAME, agent roster (D3), phase structure (D10) | New text |
| S3 | Why This Process Works | GENERATE | FAILURE_MODE list, phase guarantees | Highlight identity-verify-first, archetype reuse, ethics floor |
| S4 | Variable Reference | SUBSTITUTE | TASK_ID_PREFIX (D1), OUTPUT path | TASK-PERSONARES paths |
| S5 | Input | GENERATE | All D9 extra fields | 7+ subsections |
| S6 | Effective Prompt Examples | GENERATE | TRIGGER_PATTERNS | 3-4 strong + 2 weak examples |
| S7 | Incomplete Prompt | GENERATE | Mandatory clarifications | name+affiliation required, attestation prompt |
| S8 | Depth Tiers | GENERATE | Tier metrics | Quick (1 subject, 12-min budget), Standard (2-3 subjects, parallel), Deep (4+ subjects, full archetype discovery) |
| S9 | Output Locations | GENERATE | All output artifact paths (D6) | Distributed pattern |
| S10 | Execution Overview | GENERATE | Stage A steps, Stage B handoff, 7 phase names | Maps spec §5.1 to phases |
| S11 | Stage A header | COPY | n/a | Header only |
| S12 | A.1 Check existing task file | SUBSTITUTE | TASK_ID_PREFIX | Boilerplate flow |
| S13 | A.2 Parse & Triage | SUBSTITUTE | Domain triage rules (Scenario A/B) | Subject-validation triage |
| S14 | A.3 Scope Discovery | GENERATE | Domain elicitation steps (subject identity verify, archetype scan, attestation gate) | Custom 3-step pipeline |
| S15 | A.4 Write Research Notes | SUBSTITUTE | Notes file format | Boilerplate |
| S16 | A.5 Review Sufficiency | SUBSTITUTE | Quality gate criteria | Boilerplate |
| S17 | A.6 Template Triage | SUBSTITUTE | Always Template 02 | Boilerplate |
| S18 | A.7 Build the Task File | GENERATE | Phase mapping for 7 phases, BUILD_REQUEST template | Largest substitution surface |
| S19 | Stage B: Delegation | COPY | DOMAIN_NAME, TASK_ID_PREFIX | Boilerplate /task delegation |
| S20 | Agent Prompt Templates | GENERATE | Per-agent prompts: Identity Verifier, Archetype Matcher, Research Worker (archetype-driven), Discovery Worker, Aggregator, Validator + 6+3 lens QA prompts | Largest section, ~400 lines |
| S21 | Output Structure | GENERATE | Spec §3 output schema | Dossier markdown + TOML + diff + summary |
| S22 | Synthesis Mapping Table | GENERATE | n/a (incremental Edit assembly — table is reference-only) | Note Phase 4 uses Edit not synth files |
| S23 | Synthesis Quality Review Checklist | GENERATE | 10-12 quality criteria | FR-driven |
| S24 | Assembly Process | GENERATE | Multi-phase incremental Edit steps | 4 sub-phases |
| S25 | Validation Checklist | GENERATE | FR-1..FR-26 + §11 acceptance criteria | ~30+ checkboxes |
| S26 | Content Rules | GENERATE | Boilerplate 6 rows + 4 domain rows: ethics disclaimer verbatim, no first-person attribution, archetype generic purity, source citation requirements | Domain-extended |
| S27 | Critical Rules | GENERATE | Boilerplate 1-9 + 10-22 (skill-creator pattern) + 23-28 domain-specific: identity-verify-first sequential gate, ethics disclaimer non-negotiable, FR-22 generic-purity linter, FR-25 Tavily routing, model-tiering caps Opus token spend, no-fabrication-on-leading-questions hard gate | Domain-extended |
| S28 | Session Management | COPY | TASK_ID_PREFIX | Boilerplate |
| S29 | Research Quality Signals | SUBSTITUTE | Domain quality signals | "Strong: every dossier claim has URL+date" / "Weak: stable_traits without source IDs" |

**Section classification summary (preview):** COPY=4, SUBSTITUTE=12, GENERATE=13. Phase 2 Section Classifier agent will produce the authoritative table.

---

## RECOMMENDED_OUTPUTS

| Artifact | Path | Format |
|---|---|---|
| Generated SKILL.md | `.temp/skills/sc-persona-research-protocol/SKILL.md` | Markdown, 29-section RF format, target 1200-1500 lines |
| Companion agent: archetype-driven research worker | `.temp/agents/rf-personares-archetype-driven-research-worker.md` | Markdown agent definition |
| Companion agent: discovery worker | `.temp/agents/rf-personares-discovery-worker.md` | Markdown agent definition |
| Pre-flight input validation | `${TASK_DIR}research/00-input-validation.md` | Markdown — preliminary partition planning + path validity checks |
| Canonical reference summary | `${TASK_DIR}research/01-canonical-reference-summary.md` | Markdown — executive summary of canonical 29-section template anchor |
| Reference skill analysis (5 files) | `${TASK_DIR}research/02-reference-tech-research.md`, `03-reference-skill-creator.md`, `04-reference-task-builder.md`, `05-reference-prd.md`, `06-reference-tdd.md` | Markdown research files (note: actual numbering 02-06, not 01-05 as originally planned, due to inserted preliminary files 00 and 01) |
| Spec partition analysis (3 files — spec is 993 lines) | `${TASK_DIR}research/07-spec-part1-frs-architecture.md` (FRs §1-§5 + appendices A-B), `08-spec-part2-failures-validation-ops.md` (§6-§9 + appendix C-D), `09-spec-part3-ethics-acceptance-archetype-schema.md` (§10-§12 + appendix E-F) | Per spec rule 18: 993 lines exceeds single-agent threshold; partition into 3 slices |
| Best-practices guide partition (2 files — guide is 2088 lines) | `${TASK_DIR}research/10-guide-part1-skills.md`, `11-guide-part2-agents-and-commands.md` | Per spec rule 18: 2088 lines mandates partitioning |
| Section classification table | `${TASK_DIR}research/12-section-classification.md` | Authoritative table (depends on 02-11) |
| Phase 3 QA reports (6 lens reports + consolidated + verification) | `${TASK_DIR}qa/qa-research-lens-{1..6}.md`, `qa-research-consolidated-findings.md`, `qa-research-verification.md` | Markdown QA reports |
| Phase 5 QA reports (6 lens + 3 fidelity + consolidated + verification) | `${TASK_DIR}qa/qa-structural-lens-{1..6}.md`, `qa-fidelity-{1..3}.md`, `qa-structural-consolidated-findings.md`, `qa-structural-verification.md` | |
| Phase 6 QA reports (6 lens + consolidated + verification + final report) | `${TASK_DIR}qa/qa-final-lens-{1..6}.md`, `qa-final-consolidated-findings.md`, `qa-final-verification.md`, `final-quality-report.md` | |

---

## SUGGESTED_PHASES

### Phase 1: Preparation (L0 Setup) — sequential

- 1.1 Create output directory `.temp/skills/sc-persona-research-protocol/`
- 1.2 Verify task subdirectories exist (research/, synthesis/, qa/, reviews/)
- 1.3 Read research-notes.md (this file), spec, best-practices guide (paths confirmed), and tech-research SKILL.md as canonical 29-section template stand-in (since `skill_template.md` is missing)
- 1.4 Validate inputs: 10-differentiator model populated; reference skill paths exist; AGENT_FILES=true; spec partition strategy locked
- 1.5 Update task frontmatter to "Doing"

### Phase 2: Reference Skill Analysis & Spec Partitioning (L1 Discovery) — PARALLEL

**Phase 2a: Reference skill analysis (5 parallel agents):**
- 2a.1 Reference Skill Analyst — tech-research → `01-reference-tech-research.md`
- 2a.2 Reference Skill Analyst — skill-creator → `02-reference-skill-creator.md`
- 2a.3 Reference Skill Analyst — task-builder → `03-reference-task-builder.md`
- 2a.4 Reference Skill Analyst — prd → `04-reference-prd.md`
- 2a.5 Reference Skill Analyst — tdd → `05-reference-tdd.md`

**Phase 2b: Spec partition (3 parallel agents — spec is 993 lines, partition by aspect per skill rule 18):**
- 2b.1 Spec Analyst — Part 1 (§0-§5 + Appendix A,B) → `06-spec-part1-frs-architecture.md` (purpose, user stories, inputs/outputs, FR-1..FR-23, architecture, guard tables, quantity flow diagram)
- 2b.2 Spec Analyst — Part 2 (§6-§9 + Appendix C,D) → `07-spec-part2-failures-validation-ops.md` (failure modes, adversarial probes, validation/three-questions test, operational concerns, model tiering, worked example)
- 2b.3 Spec Analyst — Part 3 (§10-§12 + Appendix E,F) → `08-spec-part3-ethics-acceptance-archetype-schema.md` (ethics & disclaimer, acceptance criteria FR-1..FR-26, open questions, archetype YAML schema, matching algorithm)

**Phase 2c: Best-practices guide partition (2 parallel agents — guide is 2088 lines):**
- 2c.1 Guide Analyst — Skills section → `09-guide-part1-skills.md`
- 2c.2 Guide Analyst — Agents + Commands sections → `10-guide-part2-agents-and-commands.md`

**Phase 2d: Section Classification (1 sequential agent — depends on 2a + 2b + 2c outputs):**
- 2d.1 Section Classifier reads files 01-10, produces unified 29-row classification table → `11-section-classification.md`

### Phase 3: Completeness Verification (L4 Review/QA) — 6 lens agents, full intensity

- 3.1 Spawn 6 lens agents in parallel (all `fix_authorization: false`):
  - 3.1a rf-analyst (completeness-verification lens)
  - 3.1b rf-analyst (cross-validation lens)
  - 3.1c rf-qa (evidence-quality lens)
  - 3.1d rf-qa (gap-detection lens)
  - 3.1e rf-qa-qualitative (research-depth lens)
  - 3.1f rf-qa-qualitative (research-breadth lens)
- 3.2 Consolidate 6 reports → `qa-research-consolidated-findings.md`
- 3.3 Spawn 1 fix agent (rf-qa, fix_authorization: true)
- 3.4 Verification round (2 agents: rf-qa evidence-quality + rf-qa-qualitative research-depth)
- VERDICT: PASS → Phase 4. FAIL → repeat 3.3-3.4 (max 3 cycles), unresolved → Open Questions.

### Phase 4: Skeleton Assembly + Domain Generation (L2 Build-from-Discovery) — sequential, incremental Edit

- 4.1 Sub-phase 1: Create `.temp/skills/sc-persona-research-protocol/SKILL.md`; write frontmatter + S1-S4 (boilerplate copy from tech-research with domain noun substitution)
- 4.2 Sub-phase 2: Append S5-S18 (domain-specific Input, Depth Tiers, Output Locations, Execution Overview, Stage A boilerplate + A.7 BUILD_REQUEST customized for the persona-research workflow)
- 4.3 Sub-phase 3: Append S19-S20 (Stage B verbatim + Agent Prompt Templates: Identity Verifier, Archetype Matcher, Archetype-Driven Research Worker, Discovery Worker, Aggregator, Validator, plus 6+3 lens QA prompts; protocol blocks COPIED VERBATIM from tech-research)
- 4.4 Sub-phase 4: Append S21-S29 (Output Structure, Synthesis Mapping ref table, Quality Checklist, Assembly Process, Validation Checklist mapping FR-1..FR-26, Content Rules with 4 domain rows, Critical Rules 1-22 + 23-28 domain extensions, Session Management boilerplate, Research Quality Signals)

### Phase 5: Lens-Based Structural + Qualitative QA + Source-Fidelity Gate (L4) — 6+3 agents

- 5.1 Spawn 6 lens agents in parallel (`fix_authorization: false`):
  - 5.1a rf-qa (template-conformance lens)
  - 5.1b rf-qa (internal-consistency lens)
  - 5.1c rf-qa (evidence-quality lens)
  - 5.1d rf-qa-qualitative (actionability lens)
  - 5.1e rf-qa-qualitative (domain-accuracy lens — checks ethics/FR coverage)
  - 5.1f rf-qa-qualitative (section-classification-accuracy lens)
- 5.2 Consolidate → `qa-structural-consolidated-findings.md`
- 5.3 Fix agent (rf-qa, fix_authorization: true)
- 5.4 Verification round (2 agents)
- VERDICT: PASS → 5.5. FAIL → repeat 5.3-5.4 (max 2 cycles).
- 5.5 Source-Fidelity Gate (3 agents in parallel, all `fix_authorization: false`):
  - 5.5a rf-qa fidelity (reads 5 reference skill files + generated SKILL.md → semantic coverage)
  - 5.5b rf-qa fidelity (reads spec partition files 06-08 + generated SKILL.md → spec FR coverage; verify every FR-1..FR-26 represented)
  - 5.5c rf-qa-qualitative fidelity (reads spec + reference skills + generated SKILL.md → domain-noun leakage; ensure no tech-research / prd / tdd / skill-creator domain nouns leaked into SUBSTITUTE/GENERATE sections)
- 5.6 Consolidate fidelity findings → `qa-fidelity-consolidated.md`
- 5.7 Fix agent + verification (max 2 cycles)

### Phase 6: Lens-Based Final QA (L6 Aggregation) — 6 agents

- 6.1 Spawn 6 lens agents on assembled SKILL.md (`fix_authorization: false`):
  - 6.1a rf-qa (template-conformance lens)
  - 6.1b rf-qa (completeness lens — every spec topic appears in output)
  - 6.1c rf-qa-qualitative (section-classification-accuracy lens — re-verify each label)
  - 6.1d rf-qa-qualitative (actionability lens — agent prompts executable)
  - 6.1e rf-qa-qualitative (numbers-metrics lens — line count 1200-1500, FR coverage 26/26, ceremony minimums met)
  - 6.1f rf-qa-qualitative (domain-noun-leakage lens)
- 6.2 Consolidate → `qa-final-consolidated-findings.md`
- 6.3 Fix agent + verification (max 2 cycles)
- 6.4 Generate `final-quality-report.md`

### Phase 7: Present Results & Agent-Creator Nesting (L0 Closeout) — sequential

- 7.1 Present summary: skill output path, line count, section count (29), FR coverage (26/26 expected), depth tier
- 7.2 AGENT_FILES=true → invoke agent-creator nesting (sequential, NOT parallel — agent-creator is interactive):
  - 7.2a Skill(skill: "agent-creator", args: "agent_name: personares-archetype-driven-research-worker, agent_role: Reads matched archetype source_recipe, fills slot_schema from subject evidence, calls Tavily MCP per source category, uses Haiku for per-source extraction and Opus for cross-source consolidation, emits §5.2 worker-contract JSON, agent_family: research, parent_skill: sc-persona-research-protocol")
  - 7.2b Skill(skill: "agent-creator", args: "agent_name: personares-discovery-worker, agent_role: Same model tiering as archetype-driven worker; broader source sweep using bootstrap generic_public_figure recipe; emits both subject dossier AND proposed archetype.yaml derived from this subject's research; longer budget per archetype_discovery_minutes; agent_family: research, parent_skill: sc-persona-research-protocol")
  - Note: agent-creator adds rf- prefix automatically; do NOT include rf- in agent_name.
  - On per-agent failure: log + continue. SKILL.md remains valid without companion agents.
- 7.3 Offer test-run suggestion: "Test the new skill with `/sc:persona-research subjects: [{name: 'Josh Rosenthal', affiliation: 'Polychain Capital', role: 'Partner'}]`"
- 7.4 Update task frontmatter to "Done"
- 7.5 Write task log entry

---

## TEMPLATE_NOTES

- **MDTM template:** Template 02 (Complex Task) — multi-phase, parallel spawning, conditional flows, quality gates. Path: `.claude/templates/workflow/02_mdtm_template_complex_task.md`.
- **Skill template:** `.claude/templates/documents/skill_template.md` is **MISSING**. The task file must instruct Phase 1 to use `tech-research/SKILL.md` as the canonical 29-section structural reference (it is the longest, most comprehensive reference). All COPY-classified sections should be byte-matched against tech-research's equivalent section.
- **Agent prompt protocol blocks** (Incremental Writing, Documentation Staleness, ADVERSARIAL STANCE, VERDICTS) must be COPIED VERBATIM from tech-research's agent prompts. These four blocks are non-negotiable boilerplate per Critical Rule 15 (skill-creator).
- **Spec partitioning is mandatory** per skill-creator Critical Rule 18: spec is 993 lines (single-agent threshold ~1000 lines). Partitioned by aspect into 3 slices (FRs+architecture / failures+validation+ops / ethics+acceptance+archetype-schema) to give each Phase 2b agent ~330 lines of focused input.
- **Best-practices guide partitioning is mandatory:** guide is 2088 lines, exceeds threshold by 2x. Partition into 2 slices (Skills vs Agents+Commands).

---

## AMBIGUITIES_FOR_USER

These are noted for transparency but are NOT blocking. Phase 4 generation will proceed with the noted defaults; reviewers can change them post-generation.

1. **Skill template missing.** `.claude/templates/documents/skill_template.md` does not exist. Phase 1 will fall back to `tech-research/SKILL.md` as the canonical 29-section structural reference. **Recommendation post-generation:** Promote `tech-research/SKILL.md` to a sanitized `skill_template.md` to fix the systemic gap that will affect future skill-creator runs.

2. **Output location vs spec target.** Spec specifies destination `src/superclaude/skills/sc-persona-research-protocol/`. Skill-creator default writes to `.temp/skills/sc-persona-research-protocol/SKILL.md` per Critical Rule 13 (`.temp/` only at runtime; user copies to `.claude/`/`src/` after review). **Plan:** generate to `.temp/`, then user copies to `src/superclaude/skills/sc-persona-research-protocol/` and runs `make sync-dev`. Recommendation surfaced in Phase 7 summary.

3. **Open Questions in spec §12.** The spec itself has 9 open questions (naming convention, premium-source budget, multi-language posture, matching algorithm v1 vs v2, archetype version conflicts, bootstrap archetypes, deprecation, consumer-agnostic emitter, Tavily fallback). The generated SKILL.md will:
   - Adopt v1 defaults from §F (deterministic keyword-overlap matcher) and §9.2 (Tavily preferred, fallback on first 5xx)
   - List spec-internal open questions as "future-work" in Critical Rules / Operational Concerns sections
   - Defer v2 candidates (embedding similarity, LLM-as-judge tiebreak) to a follow-on skill iteration

4. **Premium-source provider abstraction.** Spec OQ-2 flags PitchBook/Crunchbase as needing paid sources. v1 will treat premium sources as configurable (placeholder fields in source_recipe schema) but not implement adapters — Tavily covers free-tier signal sufficient for FR validation.

5. **Bootstrap archetype YAMLs (spec §"Next Step" + OQ-6).** Spec recommends shipping 4 archetypes in canonical: `generic_public_figure`, `crypto_native_vc`, `gaming_specialist_vc`, `strategic_corporate_exec`. These are out-of-scope for skill-creator (skill-creator generates SKILL.md + companion agents only). Phase 7 summary will surface this as a follow-on user task.

6. **Validator model selection (spec §9.2 / OQ-3 resolved).** Resolved in spec: same model as production party-mode usage. Skill will document this without hardcoding a model ID.

7. **Naming convention for modeled personas (spec OQ-1).** v1 default: `<prefix>-<lastname>-mod` (e.g., `board-rosenthal-mod`). Skill will accept `code_prefix` input and default to `board-`. User can override per-invocation.

---

## SPEC-INTERNAL CONTRADICTIONS TO CARRY FORWARD

The following contradictions exist *within the source spec itself* (`/config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md`). They CANNOT be silently resolved by the skill-creator — Phase 4 must encode them in the generated SKILL.md as Open Questions / Critical Rules with explicit "spec-says-X-here-but-Y-there" framing. These were surfaced by Phase 3 cycle 1 cross-validation findings C-1, C-2, C-3.

### SC-1 — Disclaimer text drift between spec §10.1 and Appendix E (cycle 1 finding C-1)

**Spec evidence (verbatim):**
- **§10.1 line 493:** Single line. `Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.`
- **Appendix E lines 850-854 (per 09-spec-part3 §8a):** Multi-line block scalar using YAML slot bindings `{name}, {role} at {firm_name}` instead of `[Name, Affiliation]`.

**Implication for FR-6 / §11 #3 byte-fidelity test:** The acceptance test "the mandatory disclaimer (§10.1) appears verbatim in every produced persona description" cannot be passed if Appendix E's slot-substituted version is what the skill emits. Either §10.1 is canonical (Appendix E template must be discarded or treated as a slot-binding source), or Appendix E is canonical (§11 #3 must be reworded).

**Carry-forward action:** Phase 4 must encode this as an Open Question in the generated SKILL.md (S25 Validation Checklist + S27 Critical Rules) and document the resolution v1 defaults to §10.1 verbatim, with Appendix E's `{name}/{role}/{firm_name}` slots substituted INTO the §10.1 string at runtime. Do NOT silently pick one version.

### SC-2 — FR-9 unsuitable-subject categories (3) vs §10.2 (4) (cycle 1 finding C-2)

**Spec evidence (verbatim):**
- **FR-9 line 172 (per 07-spec-part1):** "Skill SHALL detect and refuse subjects who are deceased, minors, or non-public private individuals." — THREE categories.
- **§10.2 line 499 (per 09-spec-part3):** "Refuse on unsuitable subjects. Deceased, minors, private individuals, witnesses in active litigation: refuse (FR-9)." — FOUR categories (adds "witnesses in active litigation").

**Implication:** §11 #6 (line 521) tests only deceased-subject and minor-subject fixtures, not private-individual or witness-in-active-litigation. FR-9's per-row acceptance criterion does not require detection of witnesses-in-active-litigation. Either §10.2 over-specifies the policy floor, or FR-9 under-specifies the implementation requirement.

**Carry-forward action:** Phase 4 must encode the BROADER §10.2 set (4 categories) as the policy floor in S25 Validation Checklist and S27 Critical Rules. Document that FR-9's narrower 3-category list is the contradicted source. Surface this as an Open Question / Critical Rule note: "Skill enforces 4-category refusal per §10.2 broader floor, even though FR-9 names only 3."

### SC-3 — FR-24/FR-25/FR-26 introduced in §9.2 but absent from spec's §4 FR table (cycle 1 finding C-3)

**Spec evidence (verbatim):**
- **§4 FR table (lines 165-185):** enumerates FR-1 through FR-23.
- **§9.2 (lines 472-474, per 08-spec-part2 lines 238-240):**
  - "**FR-24:** Workers MUST NOT call Opus for per-source processing." — defined here, not in §4.
  - "**FR-25:** Web searches MUST route through Tavily MCP when Tavily is configured." — defined here.
  - "**FR-26:** The run summary MUST report token spend per model tier..." — defined here.

**Implication:** §11 #1 (line 516) says "FR-1 through FR-23 all pass (per-FR acceptance criteria above)" — this misses FR-24/25/26 entirely. §11 #12 (line 527) and #13 (line 528) DO test FR-24/25/26 explicitly, but the §4 table is the FR registry and is silent on them. A reader looking at §4 alone would not know FR-24/25/26 exist.

**Carry-forward action:** Phase 4 must encode all 26 FRs in the generated SKILL.md S25 Validation Checklist with explicit references showing FR-1..FR-23 are defined in §4 while FR-24/25/26 are introduced in §9.2 (lines 472-474). Document this as an Open Question / spec-correction recommendation. The generated skill's checklist must NOT mirror the §4-only enumeration; it must enumerate all 26 with their respective spec line references.

---

## SYNTHESIS MAPPING (research files → output sections)

| Research files | Output sections |
|---|---|
| 01-05 (reference skill analyses) | S1-S4 (frontmatter, title, why, variable ref); S11 (Stage A header); S19 (Stage B); S22 (synthesis mapping table); S28 (session management); core protocol blocks in S20 |
| 06-08 (spec partitions) | S2 (overview), S3 (why), S5 (input fields), S6-S7 (prompts), S8 (depth tiers), S9 (output locations), S10 (execution overview), S14 (A.3 scope discovery), S18 (A.7 BUILD_REQUEST), S20 (domain agent prompts: Identity Verifier, Archetype Matcher, Research Worker, Discovery Worker, Aggregator, Validator), S21 (output structure), S25 (validation checklist mapping FR-1..FR-26), S26 (content rules — domain-extended), S27 (critical rules 23-28 — domain extensions), S29 (research quality signals) |
| 09-10 (best-practices guide partitions) | S2 (overview tone), S20 (agent prompt conventions), S26 (content rules — sanity-check vs guide), S27 (critical rules — sanity-check), S25 (validation checklist — sanity-check) |
| 11 (section classification table) | Authoritative source for ALL sub-phases of Phase 4; every Phase 4 sub-phase reads this file before writing |

---

## NEXT-STEP HANDOFF NOTE

Research notes status: **Complete**. Skill-creator A.5 review gate passes (10-differentiator model populated with HIGH confidence; 5 reference skills identified; spec partitioning strategy locked; AGENT_FILES roster defined; ambiguities documented).

Proceed to A.6 (template triage — Template 02 confirmed) and A.7 (write BUILD-REQUEST.md and invoke `/task-builder`).
