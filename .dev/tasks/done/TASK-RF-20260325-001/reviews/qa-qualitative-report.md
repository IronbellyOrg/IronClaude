# QA Report -- Qualitative Content & Logic Review

**Topic:** TASK-RF-20260325-001 (TDD as First-Class Pipeline Input)
**Date:** 2026-03-26
**Phase:** qualitative-review (adversarial cross-file validation)
**Fix cycle:** 1

---

## Overall Verdict: FAIL

## Files Reviewed

1. `src/superclaude/examples/tdd_template.md` -- YAML frontmatter + sentinel self-check
2. `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` -- Steps 9-14 + domain dictionaries
3. `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` -- TDD detection rule + 7-factor formula
4. `src/superclaude/commands/spec-panel.md` -- Steps 6a/6b + TDD Output section
5. `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- Steps 4.1a, 4.4a + Stage 7 validation
6. `src/superclaude/skills/tdd/SKILL.md` -- PRD Extraction Agent + Rules 12-13 + Synthesis Mapping + QA Gate

---

## Items Reviewed

| # | Check | Result | Severity | Evidence |
|---|-------|--------|----------|----------|
| (a) | TDD extraction Steps 9-14 section number accuracy | FAIL | CRITICAL | Step 14 references §8.2 for endpoint tables but endpoint summary table is in §8.1 |
| (b) | Detection rule consistency (scoring.md vs extraction-pipeline.md) | FAIL | CRITICAL | extraction-pipeline has 3 OR conditions; scoring.md has only 2 |
| (c) | 7-factor scoring formula source alignment | FAIL | CRITICAL | `data_model_complexity` references §7 Data Entities but NO extraction step extracts it |
| (d) | Tasklist Step 4.1a key coverage vs extraction-pipeline storage keys | FAIL | IMPORTANT | `api_surface` is extracted in Step 14 but missing from tasklist context loading |
| (e) | Migration phases re-bucketing behavior risk | FAIL | IMPORTANT | Unconditional replacement of heading-based phase buckets is destructive |
| (f) | Sentinel self-check spec-panel flag validity | FAIL | CRITICAL | `--mode` and `--focus` flags exist but `--focus correctness,architecture` uses comma syntax not documented as valid |
| (g) | PRD Extraction Agent CODE-VERIFIED tagging | FAIL | CRITICAL | CODE-VERIFIED/CODE-CONTRADICTED tags applied to PRD content extraction where no code verification occurs |
| (h) | TDD frontmatter fields consumed by pipeline | FAIL | IMPORTANT | scoring.md and extraction-pipeline.md never READ frontmatter field values; they recompute from scratch |
| (i) | Rules 12/13 PRD fallback when PRD_REF is empty | PASS | -- | Rules are synthesis content rules applied only when PRD extraction file exists; synthesis mapping conditionally sources 00-prd-extraction.md |
| (j) | Synthesis Mapping Table fallback for missing 00-prd-extraction.md | FAIL | IMPORTANT | No explicit fallback documented for when synthesis agents reference a nonexistent PRD extraction file |
| (k) | Cross-file section number consistency | PASS | -- | Section numbers are consistent across all 6 files (§10, §14, §15, §19, §24 all match TDD template) |
| (l) | spec_type enum consistency with release-spec-template.md | FAIL | MINOR | TDD template has 7 values; release-spec-template has 4 values; `migration`, `security`, `performance`, `docs` only exist in TDD |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Fixed? |
|---|----------|----------|-------|-------------|--------|
| 1 | CRITICAL | extraction-pipeline.md:194 (Step 14) | Step 14 says "Extract endpoint count from endpoint tables in `## 8. API Specifications` §8.2" but the endpoint summary TABLE (with all endpoints listed) is in §8.1 (API Overview). §8.2 (Endpoint Details) contains individual endpoint detail blocks, not a countable summary table. | Change §8.2 to §8.1 in Step 14 description | YES |
| 2 | CRITICAL | scoring.md:9 vs extraction-pipeline.md:145 | **Detection rule mismatch.** extraction-pipeline.md uses THREE OR conditions: (1) `## 10. Component Inventory` heading, (2) YAML frontmatter type, (3) 20+ section headings. scoring.md uses only TWO: (2) and (3), omitting condition (1). A TDD with `## 10. Component Inventory` but no YAML frontmatter and <20 sections would trigger extraction Steps 9-14 but NOT the 7-factor scoring formula. The pipeline would extract TDD-specific data but then score it with the wrong (standard 5-factor) formula. | Add condition (1) to scoring.md detection rule to match extraction-pipeline.md | YES |
| 3 | CRITICAL | scoring.md:84 | **`data_model_complexity` factor has no extraction step.** The 7-factor formula references "Entity count + relationship count from §7 Data Entities table" but NO extraction step (9-14) extracts data from §7. Steps 9-14 extract from §10, §19, §24, §14, §15, §8. The §7 data is never captured by the extraction pipeline, so the scoring formula cannot compute this factor. | Add Step 15 to extraction-pipeline.md extracting `data_model_complexity` from §7 Data Entities, OR document that this factor is computed on-demand during scoring (not pre-extracted). The former is more consistent with Steps 9-14 pattern. | YES |
| 4 | CRITICAL | tdd_template.md:66 | **Sentinel self-check references invalid flag syntax.** The quality gate command `/sc:spec-panel @<this-tdd-file> --focus correctness,architecture --mode critique` uses comma-separated values for `--focus`. spec-panel.md (line 20) shows `--focus` takes a single value from the enum {requirements, architecture, testing, compliance, correctness}. The Usage line shows `--focus requirements|architecture|testing|compliance|correctness` with pipe delimiters (indicating "one of"), not comma-separated lists. However, the Examples section (line 512) DOES show comma-separated focus: `--focus requirements,architecture`. This is internally inconsistent in spec-panel.md itself, but the comma syntax appears intended. The `--mode critique` flag IS valid (line 167). **The real issue:** the sentinel self-check recommends a quality gate command, but whether comma-separated `--focus` actually works depends on undocumented behavior. | Clarify in spec-panel.md Usage line that `--focus` accepts comma-separated values, matching the example at line 512. Change Usage from `--focus requirements|architecture|testing|compliance|correctness` to `--focus requirements,architecture,...` | YES |
| 5 | CRITICAL | tdd/SKILL.md:976 (PRD Extraction Agent Prompt) | **CODE-VERIFIED tagging on PRD extraction is semantically wrong.** The PRD Extraction Agent extracts structured content FROM a PRD document (requirements, user stories, success metrics, scope). The instruction says "Tag each fact as [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED]." But this agent reads a PRD, not code. PRD facts are product requirements -- they cannot be "code verified" because they describe DESIRED behavior, not EXISTING code. The CODE-VERIFIED tag is appropriate for codebase research agents (which compare docs against actual source code). For PRD extraction, facts are either present in the PRD or not -- there is no code to verify against. | Replace the tagging instruction with: "Tag each extracted item with [PRD-VERIFIED] (directly stated in PRD text with section reference) or [PRD-INFERRED] (derived from PRD context but not explicitly stated)." This preserves the provenance-tracking intent while using semantically correct tags. | YES |
| 6 | IMPORTANT | sc-tasklist-protocol/SKILL.md:146-150 (Step 4.1a) | **`api_surface` missing from tasklist context loading.** extraction-pipeline.md Steps 9-14 store 6 keys: `component_inventory`, `migration_phases`, `release_criteria`, `observability`, `testing_strategy`, `api_surface`. But Step 4.1a only loads 5 keys -- `api_surface` is omitted. This means the tasklist generator cannot generate API-related tasks or validate API coverage, despite the extraction pipeline capturing this data. | Add `api_surface` extraction to Step 4.1a: `- api_surface: scan for ## 8. API Specifications; extract endpoint count from §8.1 API Overview table` | YES |
| 7 | IMPORTANT | sc-tasklist-protocol/SKILL.md:190 (Step 4.4a) | **Migration phase re-bucketing is unconditionally destructive.** The `migration_phases.stages` row says "Re-bucket all tasks using migration phase order" and "Replaces heading-based phase buckets." This means if the TDD has migration phases AND the roadmap has well-structured phase headings, the migration phases completely OVERWRITE the roadmap's phasing. This is dangerous: a roadmap with 5 carefully organized phases would be entirely restructured based on TDD rollout stages (which are typically Canary/Limited/Partial/Full -- deployment stages, not development phases). Deployment rollout stages are NOT development phases. | Change "Replaces heading-based phase buckets" to "Appends migration-phase tasks as a final deployment phase; does NOT replace existing heading-based phase buckets. If migration_phases.stages contains deployment stages (canary, rollout, etc.), create a dedicated 'Deployment & Rollout' phase at the end." | YES |
| 8 | IMPORTANT | scoring.md + extraction-pipeline.md (general) | **TDD frontmatter fields are write-only.** The tdd_template.md adds 8 new frontmatter fields (feature_id, spec_type, complexity_score, complexity_class, target_release, authors, quality_scores, depends_on). Neither scoring.md nor extraction-pipeline.md contains any logic to READ these field values during pipeline processing. The detection rule checks only the `type` field (which existed pre-change). scoring.md always recomputes complexity from scratch. The new fields produce zero pipeline benefit unless downstream tools are modified to read them. spec-panel.md Step 6b DOES read `target_release`, `spec_type`, `feature_id`, and `complexity_score` from TDD frontmatter -- so the fields have value for the spec-panel workflow. But for sc:roadmap, they are inert. | Add a note to tdd_template.md clarifying which pipeline tools consume which frontmatter fields: "complexity_score and complexity_class: computed by sc:roadmap (not read from frontmatter). feature_id, spec_type, target_release: consumed by sc:spec-panel --downstream roadmap." This prevents users from expecting sc:roadmap to use pre-populated values. | YES |
| 9 | IMPORTANT | tdd/SKILL.md:1115-1119 (Synthesis Mapping Table) | **No fallback for missing 00-prd-extraction.md in synthesis mapping.** synth-03 through synth-07 list `00-prd-extraction.md` as a source. But this file only exists if PRD_REF was provided. If a TDD is created without a PRD, synthesis agents for sections 6-15 will attempt to read a nonexistent file. The research notes template (line 274) handles this gracefully: "If no PRD: N/A -- no PRD provided." But the Synthesis Mapping Table does not document what agents should do when `00-prd-extraction.md` is absent. | Add a footnote to the Synthesis Mapping Table: "When 00-prd-extraction.md is absent (no PRD provided), synthesis agents skip PRD-sourced content for that mapping row and note 'PRD source unavailable' in the synthesis file." | YES |
| 10 | MINOR | tdd_template.md:16 vs release-spec-template.md:26 | **spec_type enum divergence.** TDD template defines 7 values: `new_feature | refactoring | migration | infrastructure | security | performance | docs`. release-spec-template defines 4 values: `new_feature | refactoring | portification | infrastructure`. Three values are TDD-only (`migration`, `security`, `performance`, `docs`) and one is release-spec-only (`portification`). When spec-panel Step 6b copies `spec_type` from TDD to a release spec, the value may not be valid for the release-spec schema. | Align the enums. Add `migration | security | performance | docs` to release-spec-template.md OR restrict TDD spec_type to only values valid in both schemas. The former is preferred since TDD types are superset requirements. Also add `portification` to TDD template if it should be valid there. | NO -- deferred (cross-file enum alignment requires release-spec-template owner review) |

---

## Actions Taken

### Fix 1: Step 14 section reference (extraction-pipeline.md)

Changed §8.2 to §8.1 in Step 14 description.

### Fix 2: Detection rule alignment (scoring.md)

Added `## 10. Component Inventory` heading condition to scoring.md detection rule.

### Fix 3: Missing data_model_complexity extraction step (extraction-pipeline.md)

Added Step 15: Data Model Complexity Extraction from §7 Data Entities.

### Fix 4: spec-panel --focus comma syntax (spec-panel.md)

Clarified Usage line to show comma-separated values are accepted.

### Fix 5: PRD Extraction Agent tagging (tdd/SKILL.md)

Replaced CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED with PRD-VERIFIED/PRD-INFERRED tags.

### Fix 6: api_surface in tasklist context loading (sc-tasklist-protocol/SKILL.md)

Added api_surface extraction to Step 4.1a.

### Fix 7: Migration phase re-bucketing (sc-tasklist-protocol/SKILL.md)

Changed destructive replacement to additive deployment phase.

### Fix 8: Frontmatter field consumption documentation (tdd_template.md)

Added clarifying note about which pipeline tools consume which frontmatter fields.

### Fix 9: Synthesis Mapping Table PRD fallback (tdd/SKILL.md)

Added footnote documenting agent behavior when 00-prd-extraction.md is absent.

---

## Summary

- Checks performed: 12
- Checks passed: 2
- Checks failed: 10
- CRITICAL issues: 5
- IMPORTANT issues: 4
- MINOR issues: 1
- Issues fixed in-place: 9
- Issues deferred: 1 (spec_type enum alignment -- requires cross-template coordination)

## Recommendations

1. **Immediate:** All 9 in-place fixes applied. Re-run structural QA to verify fixes did not break section numbering or cross-references.
2. **Deferred (Issue 10):** Align spec_type enums between tdd_template.md and release-spec-template.md. This is a cross-template concern that should be addressed in a separate task.
3. **Process note:** The structural QA reporting zero issues across 5 phases was genuinely suspicious. Structural QA checks section numbers exist and cross-references resolve -- it does NOT check whether section numbers point to the RIGHT content, whether detection rules match across files, or whether extraction steps cover all scoring formula inputs. These are semantic/logic checks that require reading content, not structure.

## QA Complete
