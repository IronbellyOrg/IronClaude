# Research Notes: PRD as Supplementary Pipeline Input

**Date:** 2026-03-27
**Scenario:** A (explicit request with clear goals, files, output type)
**Depth Tier:** Standard (pattern is already established by TDD integration; this is incremental)

---

## EXISTING_FILES

### Roadmap CLI (primary targets — will need changes)

| Path | Purpose | Key Exports | ~Lines |
|------|---------|-------------|--------|
| `src/superclaude/cli/roadmap/commands.py` | Click CLI commands for `superclaude roadmap run` | `roadmap_group`, `run`, `validate` | 322 |
| `src/superclaude/cli/roadmap/models.py` | `RoadmapConfig` dataclass with all config fields | `RoadmapConfig`, `AgentSpec`, `ValidateConfig`, `Finding` | 133 |
| `src/superclaude/cli/roadmap/executor.py` | Pipeline orchestration — builds steps, runs them | `execute_roadmap`, `detect_input_type` | ~900 |
| `src/superclaude/cli/roadmap/prompts.py` | All prompt builders for pipeline steps | `build_extract_prompt`, `build_extract_prompt_tdd`, `build_generate_prompt`, `build_diff_prompt`, `build_debate_prompt`, `build_score_prompt`, `build_merge_prompt`, `build_spec_fidelity_prompt`, `build_wiring_verification_prompt`, `build_test_strategy_prompt` | ~600 |
| `src/superclaude/cli/roadmap/gates.py` | Gate definitions for all pipeline steps | Gate constants (EXTRACT_GATE, GENERATE_A_GATE, etc.) | ~300 |

### Tasklist CLI (primary targets — will need changes)

| Path | Purpose | Key Exports | ~Lines |
|------|---------|-------------|--------|
| `src/superclaude/cli/tasklist/commands.py` | Click CLI commands for `superclaude tasklist validate` | `tasklist_group`, `validate` | 130 |
| `src/superclaude/cli/tasklist/models.py` | `TasklistValidateConfig` dataclass | `TasklistValidateConfig` | 26 |
| `src/superclaude/cli/tasklist/executor.py` | Tasklist validation pipeline execution | `execute_tasklist_validate` | ~210 |
| `src/superclaude/cli/tasklist/prompts.py` | Tasklist fidelity prompt builder | `build_tasklist_fidelity_prompt` | 126 |

### Skill/Reference Layer (secondary targets)

| Path | Purpose | ~Lines |
|------|---------|--------|
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Extraction step reference with TDD-conditional steps 9-15 | ~210 |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | Scoring reference with TDD detection rule and 7-factor formula | ~150 |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist generation protocol with TDD supplementary context docs | ~500+ |
| `src/superclaude/commands/spec-panel.md` | Spec-panel command with TDD input detection | ~200 |

### Reference Materials (read-only context)

| Path | Purpose |
|------|---------|
| `src/superclaude/skills/prd/SKILL.md` | PRD authoring skill — defines full PRD structure (~28 sections) |
| `src/superclaude/examples/tdd_template.md` | TDD template — shows which PRD content TDD can hold vs. drops |
| `src/superclaude/skills/tdd/SKILL.md` | TDD skill — PRD extraction agent at lines ~944-978 extracts only 5 sections |

### Prior Research (verified findings — build on, don't re-audit)

| Path | Purpose |
|------|---------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260324-001/RESEARCH-REPORT-prd-tdd-spec-pipeline.md` | Architecture-level findings on PRD/TDD/spec pipeline gaps |
| `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/RESEARCH-REPORT-cli-tdd-integration.md` | CLI-level findings on executor, prompts, gates, modules |
| `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` | Implementation task structure (template for PRD implementation task) |
| `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reports/final-integration-report.md` | TDD integration completion report |

## PATTERNS_AND_CONVENTIONS

### TDD Supplementary Input Pattern (established, to replicate for PRD)

The TDD integration established this exact pattern for adding supplementary inputs:

**1. Model field:** `tdd_file: Path | None = None` on config dataclass
- Roadmap: `RoadmapConfig.tdd_file` in `models.py:115`
- Tasklist: `TasklistValidateConfig.tdd_file` in `models.py:25`

**2. CLI flag:** `--tdd-file` with `type=click.Path(exists=True, path_type=Path)`
- Tasklist: `commands.py:62-66`
- Roadmap: not yet exposed as CLI flag (field exists in model but no `--tdd-file` on `roadmap run`)

**3. Executor wiring:** conditional inclusion in step inputs
- Tasklist: `executor.py:193-194` — `if config.tdd_file is not None: all_inputs.append(config.tdd_file)`
- Roadmap: TDD uses `input_type` routing instead (different pattern — detection + mode branching)

**4. Prompt builder parameter:** optional file parameter with conditional block
- Tasklist: `build_tasklist_fidelity_prompt(..., tdd_file: Path | None = None)` in `prompts.py:20`
- Pattern: `if tdd_file is not None: base += "...Supplementary TDD Validation..."` at `prompts.py:111-123`

**5. Supplementary validation block structure:**
```python
if tdd_file is not None:
    base += (
        "\n\n## Supplementary TDD Validation (when TDD file is provided)\n\n"
        "A Technical Design Document (TDD) is included in the inputs...\n"
        "1. Check X from TDD §Y...\n"
        "2. Check Z from TDD §W...\n"
        "Flag missing coverage as MEDIUM severity deviations."
    )
```

### Key Design Decision: PRD is supplementary, not a mode

Unlike TDD which added `--input-type auto|tdd|spec` and `detect_input_type()` for mode switching, PRD should follow the simpler tasklist TDD pattern:
- Optional `--prd-file` flag
- Conditional prompt enrichment blocks
- No `input_type` mode changes
- No `detect_input_type()` changes
- No dedicated `build_extract_prompt_prd()`

### Prompt builder inventory (roadmap)

10 prompt builders exist in `prompts.py`. PRD enrichment candidates:

| Builder | PRD Value | Priority |
|---------|-----------|----------|
| `build_extract_prompt()` | HIGH — add business context extraction | P1 |
| `build_extract_prompt_tdd()` | MEDIUM — add PRD context when both TDD+PRD provided | P2 |
| `build_generate_prompt()` | HIGH — add value-based prioritization | P1 |
| `build_spec_fidelity_prompt()` | HIGH — add PRD comparison dimensions | P1 |
| `build_test_strategy_prompt()` | HIGH — add persona/KPI/journey tests | P1 |
| `build_diff_prompt()` | LOW — variant comparison, PRD adds minor value | P3 |
| `build_debate_prompt()` | LOW — debate framing, PRD adds minor value | P3 |
| `build_score_prompt()` | MEDIUM — scoring criteria enrichment | P2 |
| `build_merge_prompt()` | LOW — merge instructions, PRD adds minor value | P3 |
| `build_wiring_verification_prompt()` | NONE — pure code verification | Skip |

## SOLUTION_RESEARCH

### Approach: Replicate tasklist TDD supplementary pattern

This is not a design decision — the research prompt specifies this approach explicitly. The implementation mirrors the established TDD supplementary input pattern.

**PRD content value mapping (from research prompt analysis):**

| Pipeline Touchpoint | PRD Sections That Add Value | Enrichment Type |
|--------------------|-----------------------------|-----------------|
| Extraction | Business rationale, personas, JTBD, success metrics, scope boundaries, compliance | Supplementary context block appended to extract prompt |
| Generate | All of above — shapes prioritization and phasing | Supplementary instructions in generate prompt |
| Spec-fidelity | Business objectives, personas, KPIs, scope, stakeholder needs, compliance | New comparison dimensions |
| Test-strategy | Personas, customer journeys, KPIs, edge cases, compliance | Supplementary acceptance/validation criteria |
| Tasklist-fidelity | Persona flows, KPI instrumentation, stakeholder/compliance tasks, UX flows | New supplementary validation block (mirrors TDD pattern) |
| Diff/debate/score/merge | Business alignment, persona coverage | Lower priority — minor enrichment |

### Interaction model (PRD + TDD together)

Four scenarios:
1. Neither provided → existing behavior, no change
2. Only TDD provided → existing behavior, no change
3. Only PRD provided → supplementary PRD blocks activate in relevant prompts
4. Both PRD + TDD provided → both supplementary blocks activate; PRD provides "why/who" context, TDD provides "how/what" context

## RECOMMENDED_OUTPUTS

### Research files (5 agents)

| File | Topic | Agent Type |
|------|-------|-----------|
| `research/01-roadmap-cli-integration-points.md` | Where `--prd-file` connects in roadmap commands, models, executor | Code Tracer |
| `research/02-prompt-enrichment-mapping.md` | What supplementary PRD text to add to each prompt builder | Code Tracer + Doc Analyst |
| `research/03-tasklist-integration-points.md` | Where `--prd-file` connects in tasklist commands, models, executor, prompts | Code Tracer |
| `research/04-skill-reference-layer.md` | PRD-aware updates to extraction-pipeline.md, scoring.md, SKILL.md, spec-panel.md | Doc Analyst |
| `research/05-prd-content-analysis.md` | Which PRD sections are most pipeline-relevant, what content to extract | Architecture Analyst |

### Web research (1 topic — optional)

| File | Topic |
|------|-------|
| `research/web-01-prd-driven-roadmapping.md` | Industry patterns for PRD-informed technical roadmapping and prioritization |

### Synthesis files (6)

| File | Report Sections | Source Research |
|------|----------------|----------------|
| `synthesis/synth-01-problem-current-state.md` | S1 Problem Statement, S2 Current State | 01, 02, 03, 04, 05 |
| `synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis | All research files |
| `synthesis/synth-03-external-findings.md` | S5 External Research | web-01 |
| `synthesis/synth-04-options-recommendation.md` | S6 Options, S7 Recommendation | All research files |
| `synthesis/synth-05-implementation-plan.md` | S8 Implementation Plan | 01, 02, 03, 04 |
| `synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail | All files |

### Final report

`RESEARCH-REPORT-prd-pipeline-integration.md`

## SUGGESTED_PHASES

### Phase 2: Deep Investigation (5 parallel agents)

**Agent 1 — Roadmap CLI Integration Points**
- Type: Code Tracer
- Files: `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/roadmap/models.py`, `src/superclaude/cli/roadmap/executor.py`
- Output: `research/01-roadmap-cli-integration-points.md`
- Questions: Exactly where does `config.tdd_file` flow in executor? Where would `config.prd_file` need to be included in step inputs? Which `_build_steps()` entries need `prd_file` in their inputs? Does `detect_input_type()` need any changes (answer should be no)?

**Agent 2 — Prompt Enrichment Mapping**
- Type: Code Tracer + Doc Analyst
- Files: `src/superclaude/cli/roadmap/prompts.py` (full read), prior TDD research report for context
- Output: `research/02-prompt-enrichment-mapping.md`
- Questions: For each of the 10 prompt builders, what exact supplementary PRD text should be appended? What parameters need to change? What PRD sections map to what prompt enrichment? Draft the actual supplementary blocks.

**Agent 3 — Tasklist Integration Points**
- Type: Code Tracer
- Files: `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/models.py`, `src/superclaude/cli/tasklist/executor.py`, `src/superclaude/cli/tasklist/prompts.py`
- Output: `research/03-tasklist-integration-points.md`
- Questions: Exactly how was `--tdd-file` wired in? Replicate the exact pattern for `--prd-file`. What supplementary PRD validation checks should the tasklist prompt include?

**Agent 4 — Skill/Reference Layer**
- Type: Doc Analyst
- Files: `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`, `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, `src/superclaude/commands/spec-panel.md`
- Output: `research/04-skill-reference-layer.md`
- Questions: What conditional PRD-supplementary steps should be added to extraction-pipeline.md (mirroring TDD steps 9-15)? Should scoring.md gain PRD-derived factors? What should tasklist SKILL.md document for PRD supplementary context? Does spec-panel need PRD-aware behavior?

**Agent 5 — PRD Content Analysis**
- Type: Architecture Analyst
- Files: `src/superclaude/skills/prd/SKILL.md`, `src/superclaude/examples/tdd_template.md`, `src/superclaude/skills/tdd/SKILL.md` (lines ~944-978 for PRD extraction)
- Output: `research/05-prd-content-analysis.md`
- Questions: Which PRD sections are most pipeline-relevant? Map each to the pipeline touchpoint where it adds value. What content survives into TDD vs. what is lost? What's the minimal set of PRD sections the pipeline should extract/reference?

### Phase 3: Research Completeness Verification

- Spawn rf-analyst (completeness-verification) + rf-qa (research-gate) in parallel
- 5 research files — below threshold for partitioning
- Output: `qa/analyst-completeness-report.md`, `qa/qa-research-gate-report.md`

### Phase 4: Web Research (1 agent)

**Web Agent 1 — PRD-Driven Roadmapping Patterns**
- Topic: How do product-led engineering teams use PRD content to inform technical roadmap prioritization? Best practices for value-based phasing.
- Context: Our pipeline generates roadmaps from TDD/spec inputs. We want to enrich with PRD business context without turning the engineering roadmap into a product roadmap.
- Output: `research/web-01-prd-driven-roadmapping.md`

### Phase 5: Synthesis (6 parallel agents) + Synthesis QA Gate

Standard mapping per RECOMMENDED_OUTPUTS table above.
- Spawn rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true) after synthesis
- 6 synthesis files — above threshold for partitioning (>4), spawn 2 analyst + 2 QA instances

### Phase 6: Assembly & Validation

- rf-assembler → rf-qa (report-validation) → rf-qa-qualitative (report-qualitative)
- Output: `RESEARCH-REPORT-prd-pipeline-integration.md`

### Phase 7: Present to User

- Summary, key findings, recommendation, open questions
- Offer tech-reference skill follow-up

## TEMPLATE_NOTES

Template 02 (Complex Task) — tech-research always uses this. Phases map directly: discovery → parallel research → QA gate → web research → synthesis + QA → assembly + validation → presentation.

## AMBIGUITIES_FOR_USER

None — intent is clear from the research prompt and codebase context. The research prompt explicitly specifies:
- Supplementary only, no new input mode
- Follow TDD integration pattern exactly
- Backward compatible
- PRD content labeled as "product context for planning enrichment"
- Concise supplementary blocks, not full prompt rewrites
