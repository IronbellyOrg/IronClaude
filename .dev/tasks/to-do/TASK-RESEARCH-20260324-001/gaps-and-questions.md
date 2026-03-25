# Gaps and Questions — Consolidated

**Date:** 2026-03-24
**Source:** Research files 01-06

---

## Critical Gaps

- [02] **Frontmatter field `spec_type` — is it ever read anywhere?** The SKILL.md, extraction-pipeline.md, scoring.md, and templates.md contain no reference to reading a `spec_type` field from input spec frontmatter. But the `--template` flag accepts exactly the same values (`feature|quality|docs|security|performance|migration`). Is there an undocumented convention that `spec_type` in the spec frontmatter should be used to auto-populate `--template`? The pipeline as documented does not do this.

- [02] **No Testing or DevOps domain** — The 5-domain keyword dictionaries (Frontend, Backend, Security, Performance, Documentation) have no Testing or Ops domain. TDD sections for §15 Testing Strategy and §25 Operational Readiness have no matching domain, which means requirements from those sections would be scored as Documentation or miscategorized.

- [03] **`--spec` flag is a ghost.** It is declared in the argument-hint but has zero implementation. Any caller passing `--spec` gets silently ignored behavior. This is a meaningful gap if the intent was to allow TDD-enriched task generation.

- [05] Does `00-prd-extraction.md` have a specified format that synthesis agents understand, or does each run produce a different structure depending on which agent invents the extraction?

- [05] Is there an `rf-prd-extractor` agent definition, or is the extraction done by a generic Agent subagent with an ad-hoc prompt? The skill text says "first item extracts PRD context" without specifying the agent type.

---

## Important Gaps

- [01] **"Improve" output ambiguity**: Step 6 of Behavioral Flow says "Create enhanced specification" but the Output section says the result is a "review document." It is unclear whether the panel actually writes a new spec file or embeds the improved content inside the review document. The `Write` tool is listed but no explicit artifact path or file naming convention is defined.

- [01] **quality_scores field gap**: The command produces quality metrics under its own schema (`overall_score`, `requirements_quality`, etc.) but does not produce or consume the `quality_scores` YAML frontmatter field used elsewhere in the pipeline. No bridge exists between the two schemas.

- [02] **"Data Models" tagged FR_BLOCK in worked example but heuristic says OTHER** — The worked example in extraction-pipeline.md tags "Data Models" as `FR_BLOCK` (Section 6, L581-L700), but the relevance-tagging heuristic lists no keyword that would match "Data Models". This is an inconsistency in the ref document. TDD §7 Data Models would be tagged `OTHER` under the stated rules, meaning it gets de-prioritized in chunk assembly.

- [02] **Complexity frontmatter override path missing** — A spec author who knows their project complexity and puts `complexity_class: HIGH` in the spec frontmatter will have that value silently ignored. The pipeline always recomputes. This could be a design gap if the spec author has domain knowledge the formula cannot capture.

- [02] **§19 Migration & Rollout heuristic inconsistency** — The worked example tags "Migration Plan" as `FR_BLOCK` but the heuristic keywords don't include "migration". The actual behavior is ambiguous. If migration sections are tagged `OTHER`, they may be deprioritized in chunk grouping.

- [02] **TDD §10 Component Inventory — inventory lists invisible to pipeline** — Component inventory (new/modified/deleted component tables) is a common TDD pattern. None of the 8 extraction steps target inventory-style structured content. Only behavioral requirements extracted from that section would be captured.

- [03] **`--output` flag is also unimplemented.** TASKLIST_ROOT is always computed from roadmap text, never from a CLI argument. A user who passes `--output` expecting to control output location will be surprised.

- [03] **No TDD-section awareness.** The skill has no structured extraction from §7, §8, §10, §15, §19, or §24. All TDD content that could improve task specificity — API specs, data models, component inventories, test suite names, rollout plans, release gates — is either lost or converted to generic bullet-level tasks.

- [03] **The `--spec` flag's intended semantics are undefined.** Is it meant to enrich tasks from spec content? Provide metadata? Restrict task scope? Override TASKLIST_ROOT? There is no documentation anywhere in the skill files.

- [03] **Validation pipeline (Stages 7–10) validates only against the roadmap.** If a spec/TDD were provided, the validation agents have no instructions to check generated tasks against spec content. The validation loop is roadmap-only.

- [05] When the PRD-to-TDD Pipeline says "every requirement in TDD S5 should trace back to a PRD epic or user story," who enforces this? Currently no QA gate checks it.

- [05] The rf-qa-qualitative agent prompt for the TDD is not provided in SKILL.md — it references "the agent definition." Does the agent definition check PRD traceability, or only general document quality?

- [05] The PRD Phase 7 says "invoke the tdd skill with the PRD as input" — does this automatically set PRD_REF, or does the user need to manually provide the path in the TDD invocation?

---

## Minor Gaps

- [01] **No template awareness**: The command is entirely self-contained. If the project uses `release-spec-template.md` or `tdd_template.md` as structured inputs, `sc:spec-panel` will treat them as opaque text with no special handling of frontmatter or placeholders.

- [01] **sc:tasklist not wired**: Despite the command producing prioritized findings and improvement roadmaps, there is no integration point to `sc:tasklist` to automatically generate tasks from findings.

- [01] **NFR-8 false positive rate**: The spec mentions "Target false positive rate <30% per NFR-8; measurement deferred to Gate B (T05.02)" for the correctness-focus auto-suggestion. NFR-8 and Gate B are referenced but not defined in this file — they presumably live in a separate spec or roadmap document.

- [03] **Acceptance criteria "non-invention constraint" limits TDD value.** If a TDD were passed as the roadmap, the non-invention rule (no inventing file paths, test commands, or acceptance states not implied by the roadmap) would prevent the skill from using schema details or API endpoint tables to write specific acceptance criteria — because it would "invent" repository paths.

- [05] Should `synth-04-data-api.md` read PRD S21.1 user flows to ensure data models support all documented user interactions?
