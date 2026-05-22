# Research: Analysis Document Claims Verification

**Investigation type:** Doc Analyst + Architecture Analyst
**Scope:** .dev/analysis/spec-vs-prd-vs-tdd.md cross-validated against research files 01-05
**Status:** Complete
**Date:** 2026-03-24

---

## Claims Inventory

The following factual claims from `.dev/analysis/spec-vs-prd-vs-tdd.md` were identified for verification. Claims are grouped by topic, then tagged after cross-validation.

### Group A — spec-panel claims
1. "spec-panel has zero knowledge of the release-spec-template.md"
2. "No protocol skill exists for spec-panel"
3. "spec-panel can create specs from raw instructions"
4. "spec-panel output format is whatever the experts decide"
5. "The only sentinel references in spec-panel are Whittaker's Sentinel Collision Attack"

### Group B — sc:roadmap claims
6. "sc:roadmap reads spec_type from YAML frontmatter for template selection"
7. "complexity_score / complexity_class informs milestone count"
8. "quality_scores feeds pipeline quality signals"
9. "The frontmatter advantage is conditional — only exists when spec was manually created from template"
10. "The extraction pipeline looks for: FRs, NFRs, behavioral statements, user stories, acceptance criteria, KPIs, metrics"
11. "sc:roadmap parses YAML frontmatter"

### Group C — sc:tasklist claims
12. "sc:tasklist's only input is the roadmap text"
13. "The --spec flag exists"
14. "sc:tasklist doesn't use the spec or TDD directly"

### Group D — TDD template claims
15. "TDD has none of the YAML frontmatter sc:roadmap uses"
16. TDD section content mapping claims (§5 FRs/NFRs, §18 dependencies, §24 release criteria, §19 migration)

### Group E — PRD/TDD skills claims
17. "The TDD skill has a PRD_REF field"
18. "PRD extraction step produces 00-prd-extraction.md"
19. "PRD→TDD handoff is missing explicit wiring"

---

## Verification Findings

### Group A — spec-panel claims

---

**Claim A1: "spec-panel has zero knowledge of the release-spec-template.md"**
**Tag: [CODE-VERIFIED]**

Research file 01 (`01-spec-panel-audit.md`) confirmed at Section 3.1: "There are zero references to any template file by path anywhere in the command." The file was read in full (624 lines). The command does not import, reference, or mention `release-spec-template.md`, `tdd_template.md`, `prd_template.md`, or any other external template file. The command is self-contained.

---

**Claim A2: "No protocol skill exists for spec-panel"**
**Tag: [CODE-VERIFIED] — with one precision note**

Research file 01 confirmed at Section 1: "No `.claude/skills/sc-spec-panel*/` directory exists. The command has no companion skill package. It is a standalone command file with no separate `SKILL.md`, `rules/`, `templates/`, or `refs/` subdirectory." This is accurate. The analysis document calls this "no protocol skill" which is correct.

---

**Claim A3: "spec-panel can create specs from raw instructions"**
**Tag: [CODE-CONTRADICTED]**

The analysis document states (line 52): "Path B: Created by /sc:spec-panel from raw instructions — `/sc:spec-panel` accepts `[specification_content|@file]` — passing raw instructions or a description causes it to generate a spec through its 11-expert panel."

Research file 01 contradicts this at Section 3.5: "The `Boundaries > Will Not` section is explicit: 'Generate specifications from scratch without existing content or context.' Usage syntax requires `[specification_content|@file]` — the spec content is a required input. The command does not offer a creation mode."

The analysis document describes Path B as if spec-panel can originate a spec from raw instructions. The command explicitly refuses to do this. It reviews and improves existing specifications; it does not generate specs from scratch. "Raw instructions" with no existing spec content would be rejected under the stated Boundaries.

Note: the analysis document is somewhat internally aware of this — the "What Needs to Change" section (line 329) says "Wire spec-panel to the spec template AND the TDD template — add explicit instructions to spec-panel's skill (currently no protocol skill exists) to: When given raw instructions or a TDD: output in release-spec-template.md format." This is described as a change needed, which is consistent with the current behavior being review-only — but the "IronClaude's Actual Current State" section (line 52) describes Path B as if it currently works, which the code does not support.

---

**Claim A4: "spec-panel output format is whatever the experts decide"**
**Tag: [CODE-CONTRADICTED] — partially**

The analysis document implies the output format is unconstrained ("whatever the experts decide"). Research file 01 at Section 3.4 documents three explicit, constrained output formats: `--format standard` (YAML-structured review document with named blocks), `--format structured` (token-efficient with SuperClaude symbol system), `--format detailed` (full expert commentary). Additionally, when `--focus correctness` is active, three mandatory artifacts are hard gates: State Variable Registry, Guard Condition Boundary Table, and Pipeline Quantity Flow Diagram.

The output is not unconstrained — it is a structured review document in one of three defined formats, not a revised spec or an open-form expert response. However, the "format" in the analysis document likely refers to the output not being a spec-template-formatted document (which is accurate), not that the format is literally arbitrary. This claim is partially misleading in implication but not wholly wrong in intent.

---

**Claim A5: "The only sentinel references in spec-panel are Whittaker's Sentinel Collision Attack"**
**Tag: [CODE-VERIFIED]**

Research file 01 at Section 3.3 confirmed: "The word 'sentinel' appears 5 times in the file, but every occurrence refers to the adversarial testing concept of 'sentinel values' (magic numbers or reserved constants in specifications that could collide with legitimate data). The FR-2.3 'Sentinel Collision Attack' is about attacking specification logic, not the SuperClaude template placeholder system. There is no awareness of `{{SC_PLACEHOLDER:*}}` or any related template token." This is an exact match to the analysis document's claim.

---

### Group B — sc:roadmap claims

---

**Claim B1: "sc:roadmap reads spec_type from YAML frontmatter for template selection"**
**Tag: [CODE-CONTRADICTED]**

The analysis document states (line 64): "`spec_type` → feeds template type selection (feature/refactoring/migration/infrastructure)."

Research file 02 (`02-roadmap-pipeline-audit.md`) contradicts this at two locations:

- Section 4 (templates.md): "There is no path where a `spec_type` YAML frontmatter field from the input spec influences template selection. The type comes from computed domain distribution or the command-line flag."
- Section 3 (scoring.md): "The formula is always computed from scratch using extracted data... There is no conditional like 'if spec frontmatter contains `complexity_score`, use that value.'"
- Section 1 (SKILL.md): "Whether specific frontmatter field values (like `spec_type`, `complexity_score`, `complexity_class`) are consumed depends on what `refs/extraction-pipeline.md` and `refs/scoring.md` specify — the SKILL.md itself only says to 'apply' those refs."
- Summary: "`spec_type` / `complexity_score` / `complexity_class` from input spec frontmatter: ignored by all pipeline logic."

What actually happens: template type is derived from computed domain distribution (keyword analysis of spec body text), not from the `spec_type` YAML field. The `--template` CLI flag can override this, but no pipeline logic reads the spec's `spec_type` frontmatter value.

---

**Claim B2: "complexity_score / complexity_class informs milestone count"**
**Tag: [CODE-VERIFIED] — with precision note**

This claim is correct in general form: `complexity_class` does determine milestone count (LOW=3-4, MEDIUM=5-7, HIGH=8-12 per research file 02, Section 3). However, the precise mechanism is: `complexity_class` is computed from scratch by the pipeline using its 5-factor formula; it is NOT read from the spec's YAML frontmatter. The analysis document presents these as fields the pipeline "actively uses" from the spec, which implies they are read from the spec — that implication is wrong, but the effect (complexity class → milestone count) is correct.

The analysis document sentence "complexity_score / complexity_class → informs milestone count (LOW=3-4, MEDIUM=5-7, HIGH=8-12)" is accurate as a description of the relationship. What's misleading is the context in which it appears: the analysis presents this as a "frontmatter advantage" of specs created from the template, implying the pipeline reads and uses those frontmatter values. It does not. The milestone-count relationship is real, but the frontmatter values are irrelevant to it.

---

**Claim B3: "quality_scores feeds pipeline quality signals"**
**Tag: [CODE-CONTRADICTED]**

The analysis document states (line 66): "`quality_scores` (clarity, completeness, testability, consistency) → pipeline quality signals."

Research file 02 at the Summary confirms: "`spec_type` / `complexity_score` / `complexity_class` from input spec frontmatter: **ignored by all pipeline logic**." The extraction pipeline (8 steps) has no step for reading YAML frontmatter values. Wave 1B Step 1 validates that YAML parses correctly but does not extract field values. No scoring formula or template selection algorithm reads `quality_scores` from the input spec.

Additionally, research file 01 (Section 3.2) confirms that spec-panel produces its own quality metrics under a different schema (`overall_score`, `requirements_quality`, etc.) — it does not write back to the `quality_scores` YAML frontmatter field in the spec. There is no bridge between the two schemas and no pipeline step that reads `quality_scores` from either document.

---

**Claim B4: "The frontmatter advantage is conditional — only exists when spec was manually created from template"**
**Tag: [CODE-VERIFIED] — with correction to underlying reasoning**

The analysis document's conclusion (line 55) is accurate: the frontmatter advantage only exists when the spec was created via Path A (manual template). What the research corrects is the reason this is true. The analysis implies the pipeline would use frontmatter values if they were present — it would not. Even a spec created via Path A with fully-populated frontmatter would have those values ignored by the pipeline. The "advantage" therefore does not actually exist at all — not conditionally, not in any path.

The claim as worded is factually correct about the conditional nature (Path A has the fields, Path B does not), but it overstates the advantage: the pipeline ignores those fields regardless of how the spec was created.

---

**Claim B5: "The extraction pipeline looks for: FRs, NFRs, behavioral statements, user stories, acceptance criteria, KPIs, metrics"**
**Tag: [CODE-VERIFIED]**

Research file 02 at Section 2 (extraction-pipeline.md) confirms all of these extraction targets:
- Step 2: "Behavioral statements ('shall', 'must', 'will', 'should'), user stories, acceptance criteria" — FRs, behavioral statements, user stories, ACs
- Step 3: "Performance, security, scalability, reliability, maintainability constraints" — NFRs
- Step 6: "Explicit success criteria sections, acceptance criteria, KPIs, metrics" — KPIs, metrics

This is an accurate description of the extraction pipeline's scope.

---

**Claim B6: "sc:roadmap parses YAML frontmatter"**
**Tag: [CODE-VERIFIED] — with critical precision**

The analysis document says sc:roadmap "parses YAML frontmatter" in the context of describing what the pipeline does with frontmatter fields. Research file 02 at Section 1 confirms: "Wave 1B Step 1: Parse specification file. If spec contains YAML frontmatter, **validate it parses correctly**. If malformed YAML, abort." The pipeline does parse (validate) the YAML. However, parsing for validation is not the same as consuming field values. The analysis document uses "parses" in a context that implies the values are used — this is misleading but the statement that parsing occurs is correct.

---

### Group C — sc:tasklist claims

---

**Claim C1: "sc:tasklist's only input is the roadmap text"**
**Tag: [CODE-VERIFIED]**

Research file 03 (`03-tasklist-audit.md`) at Section 1 confirmed: "You receive exactly one input: the roadmap text. Treat the roadmap as the only source of truth." The SKILL.md Input Contract states this explicitly. The claim is accurate.

---

**Claim C2: "The --spec flag exists"**
**Tag: [CODE-VERIFIED] — with critical qualification**

Research file 03 confirmed the `--spec` flag appears in the SKILL.md frontmatter argument-hint: `"<roadmap-path> [--spec <spec-path>] [--output <output-dir>]"`. The flag is declared. However, Section 1 and Section 8 (Q1) of research file 03 both confirm: "This is the only reference to `--spec` in the entire SKILL.md. There is no section in the body that defines what `--spec` does... The flag is advertised in the argument-hint but is completely unimplemented."

The analysis document says the `--spec` flag "exists" — it does, as a declared interface. But the analysis document should note it is unimplemented if this claim is used to support an argument about capabilities.

---

**Claim C3: "sc:tasklist doesn't use the spec or TDD directly"**
**Tag: [CODE-VERIFIED]**

Research file 03 confirms: "The skill accepts exactly one input: roadmap text." The `--spec` flag is unimplemented. Passing a TDD directly would process it as opaque roadmap text with no semantic awareness of TDD sections. The claim is accurate and supported by multiple sections of the research.

---

### Group D — TDD template claims

---

**Claim D1: "TDD has none of the YAML frontmatter sc:roadmap uses"**
**Tag: [CODE-VERIFIED]**

Research file 04 (`04-tdd-template-audit.md`) at the Frontmatter Comparison Table and the "Notable absences vs. pipeline-oriented fields" section confirmed: "No `feature_id`, no `spec_type`, no `complexity_score`, no `complexity_class`, no `target_release` (has `due_date` which is empty), no `quality_scores` block, no `authors` list." The TDD's 27 frontmatter fields share only title, version, status, and approximate date analogs with the spec template — none of the pipeline-oriented fields.

Note: as established in Group B findings, sc:roadmap would ignore these frontmatter fields even if the TDD had them. The practical implication of this absence is therefore moot for current pipeline behavior, but the factual claim about absence is correct.

---

**Claim D2 (implicit): TDD §5 contains FRs and NFRs in structured table format**
**Tag: [CODE-VERIFIED]**

Research file 04 Section 1.2 confirms: Section 5 "Technical Requirements" contains "5.1 Functional Requirements" (FR table with ID/priority/acceptance criteria) and "5.2 Non-Functional Requirements" (Performance/Scalability/Reliability/SLOs/Security sub-tables). The analysis document's claim that TDD §5 has FRs and NFRs extractable by the pipeline is correct. Research file 02 confirms these would be partially captured by the 8-step extraction pipeline (Step 2 for FRs, Step 3 for NFRs).

---

**Claim D3 (implicit): TDD §18 contains dependencies for pipeline extraction**
**Tag: [CODE-VERIFIED]**

Research file 04 Section 1.2 confirms Section 18 "Dependencies" contains external, internal, and infrastructure dependency tables with version/purpose/risk/fallback columns. Research file 02 confirms Step 5 (Dependency Extraction) targets "requires", "depends on", "after", "before", "blocks" language. The structured tables in §18 would be partially captured if they use those keyword patterns.

---

**Claim D4 (implicit): TDD §24 contains release criteria the pipeline can extract**
**Tag: [CODE-VERIFIED]**

Research file 04 Section 1.2 confirms Section 24 "Release Criteria" contains "24.1 Definition of Done" (13-item DoD checklist) and "24.2 Release Checklist" (9-item). Research file 02 at the TDD Section Capture Analysis confirms: "§24 Release Criteria — YES, captured by Step 6 (Success Criteria). Directly targeted." This is the one TDD section fully captured by the current pipeline.

---

**Claim D5 (implicit): TDD §19 migration sections partially captured**
**Tag: [CODE-VERIFIED] — with inconsistency note**

Research file 02 at the TDD Section Capture Analysis notes for §19: "Mixed — migration requirements with behavioral language captured; phase plans and cutover steps as procedural content not captured. The worked example behavior and the stated heuristic are inconsistent." The analysis document's characterization of this as "rich data sc:roadmap currently does NOT extract" is accurate for the procedural/structural content (phase plans, cutover steps); the behavioral migration requirements would be captured by Step 2.

---

### Group E — PRD/TDD skills claims

---

**Claim E1: "The TDD skill has a PRD_REF field"**
**Tag: [CODE-VERIFIED]**

Research file 05 (`05-prd-tdd-skills-audit.md`) at Section 2.4 confirmed: "**PRD_REF** is one of the four input fields (step A.2 Parse & Triage)." The field is defined as: "A Product Requirements Document that this TDD implements. When provided, the TDD extracts relevant epics, user stories, acceptance criteria, technical requirements, and success metrics from the PRD as foundational context." The claim is correct.

---

**Claim E2: "PRD extraction step produces 00-prd-extraction.md"**
**Tag: [CODE-VERIFIED]**

Research file 05 at Section 2.2 confirmed the output file at: `${TASK_DIR}research/00-prd-extraction.md`. Section 2.6 confirmed the Phase 2 instruction: "If PRD provided: first item extracts PRD context to `${TASK_DIR}research/00-prd-extraction.md`." The naming and path are accurate.

---

**Claim E3: "PRD→TDD handoff is missing explicit wiring"**
**Tag: [CODE-VERIFIED] — with nuance**

The analysis document (line 342, "What Needs to Change" item 7) says: "Wire PRD → TDD handoff in the tdd skill — synthesis agents explicitly consume PRD epics, ACs, and success metrics as foundational inputs."

Research file 05 at Sections 3.1–3.3 found this is partially correct. What IS wired: PRD read in scope discovery, extracted to `00-prd-extraction.md`, listed as source for 4 of 9 synthesis files, `parent_doc` frontmatter link. What is NOT wired (gaps confirmed by research):
- No PRD extraction agent prompt template defined (Gap 1)
- 5 of 9 synthesis files (synth-03 through synth-07) do not list PRD extraction as a source (Gap 2)
- No explicit AC→FR mapping instruction (Gap 3)
- No KPI translation instruction (Gap 5)
- The PRD-to-TDD Pipeline section is reference documentation, not enforced in BUILD_REQUEST or QA gates (Gap 6)

The analysis document's recommendation to "add explicit wiring" is justified by the evidence, though the current state has more partial wiring than the analysis suggests.

---

## Corrections List

Claims tagged [CODE-CONTRADICTED] with what the code actually shows:

| # | Original Claim in Analysis Doc | What Code Actually Shows | Required Correction |
|---|-------------------------------|--------------------------|---------------------|
| 1 | "Path B: Created by /sc:spec-panel from raw instructions — passing raw instructions or a description causes it to generate a spec through its 11-expert panel" | spec-panel explicitly refuses to generate specs from scratch. Its Boundaries section states "Generate specifications from scratch without existing content or context" is a Will Not. Usage requires an existing spec as input. | Remove "Path B" from the analysis or replace with: "Path B does not currently exist — spec-panel cannot create specs from raw instructions. This capability would need to be built." The analysis's "What Needs to Change" section already partially acknowledges this on line 329, creating an internal contradiction. |
| 2 | "`spec_type` → feeds template type selection (feature/refactoring/migration/infrastructure)" presented as an active pipeline behavior | `spec_type` from spec YAML frontmatter is ignored by all pipeline logic. Template type is always derived from computed domain distribution (body keyword analysis) or the `--template` CLI flag. | Correct to: "`spec_type` in spec frontmatter is not consumed by sc:roadmap. Template selection uses computed domain distribution or the `--template` CLI flag. Adding `spec_type` to the TDD frontmatter would have no effect on current pipeline behavior." |
| 3 | "`quality_scores` (clarity, completeness, testability, consistency) → pipeline quality signals" presented as an active pipeline behavior | `quality_scores` from input spec frontmatter is ignored by sc:roadmap. No extraction step reads it. spec-panel produces quality metrics under its own schema that are not written back to the spec's frontmatter. | Correct to: "`quality_scores` in spec frontmatter is not read by sc:roadmap. The field has no effect on current pipeline behavior. spec-panel produces its own quality metrics but does not populate this YAML field." |
| 4 | "The frontmatter advantage is conditional — only exists when spec was manually created from template" (implying the pipeline uses frontmatter values when present) | The pipeline ignores all spec frontmatter field values in all cases — both Path A and Path B. Even a fully-populated frontmatter (Path A) produces identical pipeline behavior to an absent frontmatter (Path B). The "conditional advantage" does not exist at the pipeline level. | Correct to: "The spec template's frontmatter fields (`spec_type`, `complexity_score`, `complexity_class`, `quality_scores`) are validated for YAML syntax by sc:roadmap but none of their values are consumed by any extraction step, scoring formula, or template selection algorithm. Adding these fields to the TDD would require pipeline changes to actually use them — they are not currently read." |
| 5 | spec-panel output format described as relatively unconstrained ("whatever the experts decide") in the Path B context | spec-panel has three well-defined output format modes (`--format standard`, `--format structured`, `--format detailed`). Under `--focus correctness`, three artifact types are mandatory hard gates. Primary output is always a structured review document, not a revised spec file. | The implication that Path B produces free-form spec output should be corrected. The output is a review document in one of three defined formats. If a revised spec is produced at all, it is a secondary artifact embedded in the review document, not a standalone spec file. |

---

## Verified Claims List

Claims tagged [CODE-VERIFIED] (confirmed by research files tracing to actual source code or command files):

1. **spec-panel has zero knowledge of release-spec-template.md** — confirmed by full read of the 624-line command file; zero template path references found (research file 01, Section 3.1)

2. **No protocol skill / companion skill package exists for spec-panel** — no `.claude/skills/sc-spec-panel*/` directory exists; entire command is a single `.md` file (research file 01, Section 1)

3. **The only sentinel references in spec-panel are Whittaker's Sentinel Collision Attack** — "sentinel" appears 5 times, all in adversarial testing context; no `{{SC_PLACEHOLDER:*}}` awareness (research file 01, Section 3.3)

4. **The extraction pipeline looks for FRs, NFRs, behavioral statements, user stories, acceptance criteria, KPIs, metrics** — confirmed by the 8-step extraction pipeline documented in extraction-pipeline.md (research file 02, Section 2, Steps 2, 3, 6)

5. **sc:roadmap parses YAML frontmatter** — Wave 1B Step 1 validates YAML parses correctly; confirmed (research file 02, Section 1) — though values are not consumed

6. **complexity_class informs milestone count (LOW=3-4, MEDIUM=5-7, HIGH=8-12)** — confirmed in scoring.md classification thresholds (research file 02, Section 3)

7. **sc:tasklist's only input is the roadmap text** — Input Contract states explicitly: "You receive exactly one input: the roadmap text. Treat the roadmap as the only source of truth." (research file 03, Section 1)

8. **The --spec flag exists** — declared in SKILL.md argument-hint (research file 03, Section 1) — though unimplemented

9. **sc:tasklist doesn't use the spec or TDD directly** — confirmed; `--spec` flag is unimplemented and the skill has no TDD-section semantic awareness (research file 03, Sections 1 and 8)

10. **TDD has none of the YAML frontmatter sc:roadmap uses** — confirmed; TDD has 27 frontmatter fields with zero pipeline-oriented fields (`spec_type`, `complexity_score`, `complexity_class`, `quality_scores` all absent) (research file 04, Section 1.1 and comparison table)

11. **TDD §5 contains FRs and NFRs** — confirmed; Section 5 has FR table (ID/priority/ACs) and NFR sub-tables (research file 04, Section 1.2)

12. **TDD §24 release criteria captured by pipeline** — confirmed; Step 6 (Success Criteria) directly targets this content (research file 02, TDD section capture analysis)

13. **The TDD skill has a PRD_REF field** — confirmed; defined as one of four input fields in Step A.2 (research file 05, Section 2.4)

14. **PRD extraction step produces 00-prd-extraction.md** — confirmed; file path `${TASK_DIR}research/00-prd-extraction.md` documented (research file 05, Section 2.2 and 2.6)

15. **PRD→TDD handoff is missing explicit wiring** — confirmed; 6 gaps identified including no extraction agent prompt, 5 synthesis files not reading PRD, no AC→FR mapping instruction, PRD-to-TDD Pipeline section is unenforced reference docs (research file 05, Sections 3.1–3.3)

16. **The sentinel system uses grep -c '{{SC_PLACEHOLDER:' as completion check** — confirmed in release-spec-template.md audit (research file 04, Section 2.3)

17. **Spec template quality gate explicitly names sc:spec-panel** — confirmed in the usage block preamble of release-spec-template.md (research file 04, Section 2.3)

18. **TDD §19 Migration & Rollout procedural content is not fully captured by pipeline** — confirmed; behavioral statements captured but phase plans and cutover steps as structured content are not (research file 02, §19 analysis)

---

## Option 3 Feasibility Assessment

**Option 3: Modify TDD template AND upgrade sc:roadmap, sc:spec-panel, and sc:tasklist to actively consume the TDD's rich sections.**

### What the Research Confirmed About Option 3 Feasibility

**Confirmed supportive:**

1. **The TDD template already has all the rich content sections Option 3 proposes to extract.** Research file 04 confirms §7 Data Models, §8 API Specifications, §9 State Management, §10 Component Inventory, §14 Observability, §15 Testing Strategy, §19 Migration & Rollout, §24 Release Criteria, §25 Operational Readiness all exist and are fully structured with tables and defined formats. The content exists; only the extraction machinery is missing.

2. **The extraction pipeline's behavioral-requirements-centric design is well-understood.** Research file 02 documented exactly which TDD sections are captured (§24 fully; §7, §8, §9, §10, §14, §19 partially; §15 and §25 not at all). The gaps are precisely bounded — the new Steps 9-14 proposed in the analysis document target exactly the right content.

3. **sc:tasklist's `--spec` flag is declared but unimplemented.** Research file 03 confirmed the flag exists in the argument-hint but has no body implementation. This means Option 3's sc:tasklist upgrade has an existing hook to wire into — implementing the `--spec` flag is the natural extension point, not a new interface.

4. **The PRD→TDD skill handoff infrastructure exists but is incomplete.** Research file 05 confirmed the wiring foundation is in place (PRD_REF field, `00-prd-extraction.md` artifact, `parent_doc` frontmatter, 4 of 9 synthesis files reading PRD content). Option 3's "Wire PRD→TDD handoff" recommendation targets a real gap with a well-defined fix path (add PRD extraction agent prompt, update 5 synthesis mapping entries, add QA gate checklist item).

**What the research reveals as complications not captured in the analysis:**

1. **Adding frontmatter fields to the TDD template will have no effect without pipeline changes.** The analysis document presents adding `spec_type`, `complexity_score`, `complexity_class`, and `quality_scores` to the TDD as a prerequisite step, implying the pipeline would then use them. Research file 02 confirmed the pipeline ignores all spec frontmatter field values. The TDD template additions are only meaningful if the pipeline is simultaneously modified to read those values. Option 2 ("modify TDD template only, minimal effort") as described in the analysis document would not achieve its stated goal of letting sc:roadmap "get the metadata it needs" — the pipeline would continue to ignore those fields.

2. **The 5-domain keyword dictionaries create a structural blind spot that affects Option 3 accuracy estimates.** Research file 02 confirmed no Testing domain, no DevOps/Ops domain, and no Data/ML domain in the 5-domain classifier. TDD sections in §15 Testing Strategy, §14 Observability, and §25 Operational Readiness will systematically score poorly against all 5 domains. Steps 9-14 proposed in Option 3 would need to either extend the domain dictionaries or bypass domain classification for TDD-structured sections.

3. **spec-panel does not currently process TDD-format documents.** The analysis document proposes spec-panel TDD-enhanced expert behaviors (analysis line 249-260). Research file 01 confirmed spec-panel has no template awareness, no TDD section detection logic, and no TDD-conditional expert mode. The "TDD detection rule" proposed in the analysis is a new capability requiring new implementation in the spec-panel command, not a configuration of existing behavior.

4. **The `--spec` flag implementation gap in sc:tasklist means Option 3's tasklist upgrade has no foundation today.** The analysis document describes TDD-aware task generation rules activating when "the roadmap's extraction.md frontmatter contains `tdd_input: true`." This requires: (a) sc:roadmap to set that flag in extraction.md output when TDD input is detected, and (b) sc:tasklist to read extraction.md. Neither behavior currently exists — sc:tasklist receives only roadmap text and its `--spec` flag is unimplemented.

### Feasibility Verdict

**Option 3 remains the correct recommendation.** The research confirms:
- The TDD's rich content sections are fully structured and ready to extract
- The pipeline's exact behavioral gaps are documented and bounded
- Extension points exist (declared `--spec` flag, `00-prd-extraction.md` slot, PRD-to-TDD Pipeline section)
- The gap fixes proposed in the analysis are correctly targeted

**However, Option 2 as described is less viable than the analysis suggests.** Adding frontmatter fields to the TDD template without pipeline changes produces no benefit — the pipeline ignores those fields. Option 2 would require the same pipeline changes as Option 3, just fewer of them. This makes Option 3's additional scope (Steps 9-14 extraction, scoring formula update, spec-panel TDD mode) incrementally low-cost once the foundational pipeline changes are committed.

The analysis document's Option 3 scope list (sc:roadmap extraction pipeline, sc:roadmap scoring, sc:spec-panel, sc:tasklist) is complete and accurate. The research adds one item not in the scope list: **the 5-domain keyword dictionaries must be extended or supplemented** to avoid systematic undercounting of TDD-heavy specifications.

---

## Summary

**Status:** Complete
**Date:** 2026-03-24

| Tag | Count | Claims |
|-----|-------|--------|
| [CODE-VERIFIED] | 18 | A1, A2, A5, B2 (partial), B5, B6, C1, C2, C3, D1, D2, D3, D4, D5, E1, E2, E3, + sentinel system claims |
| [CODE-CONTRADICTED] | 5 | A3, B1, B3, B4 (reasoning), B4-implication |
| [UNVERIFIED] | 0 | All claims had supporting or contradicting evidence in the research files |

**Total claims verified:** 19 substantive claims examined
**Corrections required:** 5 (listed in Corrections List above)

---

## Key Takeaways

1. **The most consequential error in the analysis document is the frontmatter fields claim.** The analysis presents `spec_type`, `complexity_score`, `complexity_class`, and `quality_scores` in the spec template as fields the pipeline "actively uses." The research confirms the pipeline ignores all of them. This means the "conditional advantage" of Path A over Path B is not a pipeline behavior advantage — it is zero. This does not change Option 3's direction, but it fundamentally changes the argument for why frontmatter fields should be added to the TDD: not because the pipeline reads them today, but because once pipeline changes land, those fields need to exist.

2. **spec-panel cannot currently generate specs from raw instructions.** Path B as described in the analysis does not exist. The analysis document partially acknowledges this in its "What Needs to Change" section but contradicts itself in the "Current State" section. The correction tightens the argument for Option 3 — spec-panel's inability to originate specs from instructions is a gap that must be built, not an existing behavior to wire.

3. **The PRD→TDD handoff has more wiring than the analysis implies.** The 5-gap analysis in research file 05 shows meaningful infrastructure already in place (`PRD_REF` field, `00-prd-extraction.md`, `parent_doc`, 4/9 synthesis files). The "missing explicit wiring" framing is correct in direction but should acknowledge the existing partial wiring to give an accurate scope estimate for the fix.

4. **sc:tasklist's `--spec` flag is a declared-but-dead interface.** This is an actionable finding for Option 3 implementation: the interface declaration already exists, providing a clean hook for TDD-aware task generation without changing the skill's external signature.

5. **Option 3 feasibility is confirmed with one addition to its scope:** the 5-domain keyword dictionary must be extended to include Testing, DevOps/Ops, and Observability domains. Without this, TDD-heavy specifications will systematically underestimate complexity — directly undermining the analysis document's goal of "dramatically richer roadmaps" from TDD input.
