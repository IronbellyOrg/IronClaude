# Research: Spec Decomposition
**Topic type:** Spec Decomposition
**Scope:** Map every §1-§19 of merged-requirements.md to concrete build units
**Status:** Complete
**Date:** 2026-05-27
---

## Frontmatter & Provenance Mapping

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| Frontmatter (lines 1-6: name/description/version/allowed-tools) | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (top of file) | Verbatim YAML frontmatter block — name `sc:reflect-protocol`, version 1.0.0, description (the 3-sentence summary), the full allowed-tools list | 0 ref files; copied as-is |
| Lines 8-21 (provenance comments + extended metadata) | `SKILL.md` (immediately under frontmatter, as HTML comments) | Preserve provenance comments (`Base: Variant 2`, merge date, sources, unresolved_conflicts) + extended metadata block | Optional but preserves audit trail per spec convention |
| Line 23 (`# Reflect Protocol`) | `SKILL.md` | H1 title | Verbatim |

---

## §1 Purpose & Core Thesis (lines 25-44)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §1 opening paragraph (line 29) — "Reflection that confirms its own conclusions…" + Mehta citation | `SKILL.md` `## 1. Purpose & Core Thesis` opening | Verbatim paragraph | 0 refs |
| §1 three structural mechanisms (lines 31-35) | `SKILL.md` §1 numbered list (1-3) | Verbatim list with HDEE / LLM-TOPLA / Wisdom of Silicon Crowd / Khan ICML 2024 / Kenton NeurIPS 2024 citations | 0 refs |
| §1 Two modes paragraph (lines 37-40) | `SKILL.md` §1 "Two modes, one protocol" subsection | Verbatim UC-1 and UC-2 bullets with ROI band | 0 refs |
| §1 Hallucination contract (line 42) | `SKILL.md` §1 "Hallucination contract" closing paragraph | Verbatim — Grounded vs Inferred binary, no third bucket | 0 refs (full hallucination guardrails live in §11) |

---

## §2 Triggers (lines 46-58)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §2 opening (line 50) | `SKILL.md` `## 2. Triggers` | "Invoked ONLY by `/sc:reflect` command via `Skill sc:reflect-protocol`. Never invoked directly by users." | 0 refs |
| §2 activation conditions list (lines 52-56) | `SKILL.md` §2 bulleted list | 3 bullets — user runs `/sc:reflect`, auto-trigger from sc:troubleshoot W6/Phase B+D, auto-trigger from sc:task end-of-task hook | 0 refs |
| §2 closing (line 58) | `SKILL.md` §2 footer | "Do NOT invoke this skill directly outside the above paths." | 0 refs |

---

## §3 Required Input + Mode Selection (lines 62-122)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §3 preamble (line 64) | `SKILL.md` `## 3. Required Input + Mode Selection` | "The skill MUST resolve a mode (UC-1 or UC-2) before any wave runs." | 0 refs |
| §3.1 input flag enumeration (lines 70-89) | `SKILL.md` `### 3.1 Inputs` AND `refs/input-resolution.md` `## Flag enumeration` | SKILL.md: complete flag bullet list (20 flags including all `--promote-*`). refs/input-resolution.md duplicates with semantics expansion | Heavy detail; SKILL.md keeps bullet list, refs file expands semantics |
| §3.1 promotion-gate flags sub-bullet (lines 84-89) | `SKILL.md` §3.1 nested bullets + `refs/promotion-adapters.md` `## Flag semantics` | 5 flags: `--no-promote`, `--promote-anyway`, `--promote-dry-run`, `--promote-mode`, `--promote-resume`; refs/promotion-adapters.md expands per-flag behavior | refs/promotion-adapters.md owns adapter+flag detail |
| §3.2 mode selection 6-rule first-match (lines 91-102) | `SKILL.md` `### 3.2 Mode selection` AND `refs/input-resolution.md` `## 6-rule mode selection` | Numbered 6-rule list verbatim + STOP message | refs file repeats with worked examples |
| §3.3 Hard STOP conditions (lines 104-112) | `SKILL.md` `### 3.3 Hard STOP conditions` AND `refs/input-resolution.md` `## STOP conditions` | 5 STOP bullets verbatim | refs file expands rationale |
| §3.4 Environment Prerequisites (lines 114-122) | `SKILL.md` `### 3.4 Environment Prerequisites` AND `refs/input-resolution.md` `## Environment` | SKILL.md cites the §4 Wave 0 routing table by reference; refs/input-resolution.md owns the alias resolution algorithm | Routing table itself stays in §4 Wave 0 (mirrored in refs/input-resolution.md) |

---

## §4 Wave / Tier Architecture (lines 126-305)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §4 preamble + audit-emit convention (lines 130-131) | `SKILL.md` `## 4. Wave / Tier Architecture` opening | Verbatim — per-step audit emit row shape | 0 refs |
| §4 7-wave fence block (lines 133-175) | `SKILL.md` §4 fenced code block | Verbatim ASCII tree of Waves 0-7 with all sub-steps (0.1-0.9, 1A-1D, 3A-3D, 5.0/5.x, 7.1-7.7) | 0 refs |
| §4 SRP boundary paragraph (line 177) | `SKILL.md` §4 closing | Verbatim "7-wave count is structurally 6 review + 1 mutation" framing | 0 refs |
| §4.0 Step 0.4 input_sha256 tree-snapshot (lines 181-216) | `SKILL.md` `### 4.0 Wave 0 — Detailed step additions` `**Step 0.4**` subsection | Full body: 4-item tree composition, tree-hash algorithm, input-snapshot.yaml shape, drift-detection semantics, backward-compat note | Inline; not extracted to refs |
| §4.0 Step 0.5 env-var alias resolution + routing table (lines 218-232) | `SKILL.md` `**Step 0.5**` subsection AND `refs/input-resolution.md` `## Env routing table` | 4-row routing table (0/1/2/≥3 aliases × `--tier` flag) + telemetry column + grader assertion + zero-aliases-tier2 STOP rationale | Table mirrored in refs/input-resolution.md |
| §4.0 Step 0.6 vendor heterogeneity (lines 234-241) | `SKILL.md` `**Step 0.6**` subsection AND `refs/ops-integration.md` `## Vendor-heterogeneity WARN` | Vendor extraction heuristic + multi/single telemetry + WARN reference; full WARN body in refs/ops-integration.md per §16 row | refs/ops-integration.md owns WARN body |
| §4.0 Step 0.9 budget pre-flight (lines 243-259) | `SKILL.md` `**Step 0.9**` subsection AND `refs/cost-profile.yaml` (machine-readable mirror) | 5-row budget routing table with explicit inclusive/exclusive operators; T1-midpoint=6, T2-midpoint=52 anchors; 1.25× kill threshold | refs/cost-profile.yaml mirrors §15 |
| §4.1 Step 1B.1 zero-task guard (lines 263-265) | `SKILL.md` `### 4.1 Wave 1` `**Step 1B.1**` | Verbatim — UC-1 zero-task STOP with `empty_input` + `coverage_undefined: true` | 0 refs |
| §4.1 Step 1B.2 coverage_undefined route (lines 267-269) | `SKILL.md` `**Step 1B.2**` | Verbatim — zero-IDs route to T2; 0.90 floor cannot pass vacuously | 0 refs |
| §4.1 Step 1B.3 cross-task interaction-effects scan (lines 271-281) | `SKILL.md` `**Step 1B.3**` | Full 5-numbered-step algorithm (symbol overlap → graph → find_referencing_symbols → cross-citation check → synthetic invariant entry) + telemetry contract | Calls out top-30 cap, severity tiers |
| §4.3 Step 3B.0 reviewer-brief packaging (lines 285-293) | `SKILL.md` `### 4.3 Wave 3` `**Step 3B.0**` AND `refs/reviewer-spec.md` `## Brief template` | 3-item brief composition (T1 card slice, grounding hunks, coverage slice); refs/reviewer-spec.md owns brief template body | Detail in refs/reviewer-spec.md |
| §4.5 Step 5.0 sc-adversarial F1/F2/F3 fallback (lines 297-305) | `SKILL.md` `### 4.5 Wave 5` `**Step 5.0**` | Full F1/F2/F3 fallback semantics with audit-loudness contract | 0 refs |

---

## §5 Tier-Decision Rubric (lines 309-396)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §5 preamble (line 313) | `SKILL.md` `## 5. Tier-Decision Rubric (Wave 2)` opening | Verbatim | 0 refs |
| §5.1 Hard overrides table (lines 317-325) | `SKILL.md` `### 5.1 Hard overrides` | 6-row table of overrides | 0 refs |
| §5.2 Rubric inputs (lines 327-338) | `SKILL.md` `### 5.2 Rubric inputs` AND `refs/reflection-rubric.md` `## 5-dimension scoring` | SKILL.md: `C` definition + 5 dimension names + 3 structural signals (S_scope, S_domains, S_dev_density); refs/reflection-rubric.md owns full dimension definitions + scoring rubric | refs/reflection-rubric.md absorbs detail |
| §5.3 Decision logic 8-rule priority table (lines 340-352) | `SKILL.md` `### 5.3 Decision logic` | 8-row priority table (first match wins) + default coverage-floor=0.90 note | 0 refs |
| §5.4 tier_decision.yaml audit artifact (lines 354-373) | `SKILL.md` `### 5.4 tier_decision.yaml` | Full YAML shape (selected_tier, fired_rule_number, composite_score, per_signal_breakdown, escalation_reason) | 0 refs |
| §5.5 Why these thresholds (lines 375-380) | `SKILL.md` `### 5.5 Why these thresholds` | 4-bullet rationale (0.90 ceiling, 0.85 floor, S_dev_density=0.20, regression candidacy) | 0 refs |
| §5.6 Escalation reason logging (lines 382-396) | `SKILL.md` `### 5.6 Escalation reason logging` | YAML shape for escalation_decision | 0 refs |

---

## §6 Modern Serena Tool Usage (lines 400-451)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §6 preamble (line 404) | `SKILL.md` `## 6. Modern Serena Tool Usage` opening | Verbatim — `think_about_*` policy framing | 0 refs |
| §6.1 Mandatory evidence-gathering chain (lines 408-419) | `SKILL.md` `### 6.1 Mandatory evidence-gathering chain` | Verbatim 6-step Serena chain (activate_project → get_symbols_overview → find_symbol → find_referencing_symbols → get_diagnostics_for_file → Re-Read) | 0 refs |
| §6.2 Citation-grounding via re-Read (lines 421-423) | `SKILL.md` `### 6.2 Citation-grounding via re-Read` | Verbatim anti-staleness paragraph + CLAUDE.md S1 reference | 0 refs |
| §6.3 Memory pattern (lines 425-435) | `SKILL.md` `### 6.3 Memory pattern` | Fenced code block of memory key conventions + retention rule (20 entries, 90 days) | 0 refs |
| §6.4 `think_about_*` as scripted checkpoints (lines 437-447) | `SKILL.md` `### 6.4 think_about_* as scripted checkpoints` | 3-row checkpoint table + frontmatter exclusion note | 0 refs |
| §6.5 Fail-open policy (lines 449-451) | `SKILL.md` `### 6.5 Fail-open policy` | Verbatim — Serena calls fail-open per sc-validate-roadmap convention | 0 refs |

---

## §7 Agent Delegation Map (lines 455-501)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §7 preamble (line 459) | `SKILL.md` `## 7. Agent Delegation Map` opening | "Every reusable agent is mapped to a wave; no agent is duplicated inline." | 0 refs |
| §7 main agent table (lines 461-472) | `SKILL.md` §7 table | 11-row agent table (root-cause-analyst, self-review, requirements-analyst, confidence-calibrator, rf-qa, rf-qa-qualitative, audit-validator, evidence-validator, task-builder, socratic-mentor) | 0 refs |
| §7.1 Reviewer composition rules + executor-class exclusion (lines 474-490) | `SKILL.md` `### 7.1 Reviewer composition rules` AND `refs/reviewer-spec.md` `## Composition` | SKILL.md: executor-exclusion rule body + 3-row reviewer rotation table + post-removal logic + Khan judge-class note; refs/reviewer-spec.md owns full template | refs/reviewer-spec.md absorbs template |
| §7.2 No new agents required (lines 492-501) | `SKILL.md` `### 7.2 No new agents required` | 4-bullet rationale (coverage-mapping → requirements-analyst, deviation-classification → taxonomy ref, tasklist-vs-diff → inline, reflection-synthesis → inline) | 0 refs |

---

## §8 Cross-Skill Integration (lines 505-536)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §8 preamble (line 509) | `SKILL.md` `## 8. Cross-Skill Integration` opening | Verbatim | 0 refs |
| §8 integration table (lines 511-516) | `SKILL.md` §8 table | 6-row table (sc-adversarial, task-builder, confidence-check, tech-research, evidence-validator, sc-troubleshoot) | 0 refs |
| §8 invocation pattern fenced block (lines 518-526) | `SKILL.md` §8 fenced code block | Verbatim `Skill sc-adversarial-protocol with …` example invocation | 0 refs |
| §8 null convergence_score handling (lines 528-536) | `SKILL.md` §8 closing subsection | F3 path null routing semantics — `merge_method` first, undefined-null guard, promotion-gate impact, sprint executor impact | 0 refs |

---

## §9 Output Contract (lines 540-738)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §9 preamble (line 544) | `SKILL.md` `## 9. Output Contract (Versioned)` opening | "Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline." | 0 refs |
| §9.1 Stable contract YAML (lines 546-655) | `SKILL.md` `### 9.1 Stable contract` | Full verbatim YAML block (~60 fields including contract_version, status, mode, tier_reached, all UC-1/UC-2 specific, hallucination guards, Tier 2 artifacts, Tier 3, asymmetric flags, per_task_verdicts, interaction effects, budget, full promotion section) | Per-flag one-line semantics is implied by line 655 but no separate refs/return-contract.md is listed in §16 — keep semantics inline in SKILL.md |
| §9.2 Telemetry YAML (lines 657-674) | `SKILL.md` `### 9.2 Telemetry` | Verbatim non-stable telemetry block (~13 fields) | 0 refs |
| §9.3 Consumer Field Map table (lines 676-694) | `SKILL.md` `### 9.3 Consumer Field Map` | 9-row consumer table (sc-troubleshoot, sprint executor, sc-task, sc:roadmap, sc:tasklist, task-builder, Wave 7 adapters, CI/grader, meta-eval) + field-deletion guard | 0 refs |
| §9.4 Contract Evolution (lines 696-738) | `SKILL.md` `### 9.4 Contract Evolution` | Versioning rule (patch/minor/major), deprecation policy, consumer migration window, unknown-field tolerance, examples of allowed/breaking changes | 0 refs |

---

## §10 Deviation Taxonomy (lines 742-838)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §10 preamble (lines 746-748) | `SKILL.md` `## 10. Deviation Taxonomy` opening | 4-category framing + literature-gap reference + gold-standard = driving spec | 0 refs |
| §10 scaling >100 hunks (line 750) | `SKILL.md` §10 scaling note AND `refs/deviation-taxonomy.md` `## Aggregation` | Per-file aggregation rule, per-hunk-evidence.yaml auxiliary artifact, telemetry `deviation_aggregation_mode` | refs/deviation-taxonomy.md formalizes aggregation |
| §10.1 Authorized expansion (lines 752-764) | `SKILL.md` `### 10.1 Authorized expansion` AND `refs/deviation-taxonomy.md` `## Authorized` | Definition + 3 detection signals + gold-standard ref + default remediation | refs file expands per category |
| §10.2 Necessary deviation (lines 766-779) | `SKILL.md` `### 10.2 Necessary deviation` AND `refs/deviation-taxonomy.md` `## Necessary` | Same shape | refs file expands |
| §10.3 Drift (lines 781-793) | `SKILL.md` `### 10.3 Drift` AND `refs/deviation-taxonomy.md` `## Drift` | Same shape | refs file expands |
| §10.4 Regression (lines 795-807) | `SKILL.md` `### 10.4 Regression` AND `refs/deviation-taxonomy.md` `## Regression` | Same shape; only class with unconditional Tier 3 + rule 3 escalation | refs file expands |
| §10.5 Classification precedence (lines 809-811) | `SKILL.md` `### 10.5 Classification precedence` | Verbatim — Regression > Drift > Necessary > Authorized | 0 refs |
| §10.6 Grounding Gaps (lines 813-834) | `SKILL.md` `### 10.6 Grounding Gaps` AND `refs/deviation-taxonomy.md` `## Grounding-gaps parallel artifact` | YAML shape with required fields (hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user) + non-empty consequences + structural separateness | refs file expands |
| §10.7 Reporting (line 838) | `SKILL.md` `### 10.7 Reporting` AND `refs/report-template.md` `## Deviation rendering` | Each deviation renders with file:line, mapped tasklist item, spec section, evidence, classification rationale, default remediation, [INFERRED] notes | refs/report-template.md owns full template |

---

## §11 Hallucination Guardrails (lines 842-932)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §11.0 Sufficiency conditional preamble (lines 846-854) | `SKILL.md` `### 11.0 Sufficiency claim is conditional` | 3-gate conditional list + degradation semantics | 0 refs |
| §11.1 Grounded vs Inferred (lines 860-867) | `SKILL.md` `### 11.1 Grounded vs Inferred` | Binary definitions, no third bucket | 0 refs |
| §11.2 Evidence-validator as final gate (lines 869-880) | `SKILL.md` `### 11.2 Evidence-validator as final gate` | 4-rule validator interpretation table + `--no-evidence-validator` semantics + UC-1 zero-citation exception | 0 refs |
| §11.3 Blind calibration disjoint-set (lines 882-904) | `SKILL.md` `### 11.3 Blind calibration` AND `refs/reflection-rubric.md` `## Calibrator selection` | Calibrator-model selection algorithm (pseudocode) + telemetry field + three-way partition (executor/reviewers/calibrator) + grader assertion | refs/reflection-rubric.md formalizes selection |
| §11.4 Heterogeneous reviewer ensemble (lines 906-908) | `SKILL.md` `### 11.4 Heterogeneous reviewer ensemble` | Verbatim — anti-representational-bias rationale, cross-class agreement = evidence | 0 refs |
| §11.5 Citation re-Read window + budget policy (lines 910-928) | `SKILL.md` `### 11.5 Citation re-Read window` | 5-tool-call window + sampling thresholds (20-citation cutoff, 100%/30%/10% sample) + sampled-mode drop accounting (sample-count gates, extrapolated is telemetry) | 0 refs |
| §11.6 Inferred-claim audit (line 932) | `SKILL.md` `### 11.6 Inferred-claim audit` | Verbatim — `citations_inferred > total/2` triggers WARN | 0 refs |

---

## §12 Eval Rubric (lines 936-1076)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §12 preamble (lines 943-945) | `SKILL.md` `## 12. Eval Rubric` opening | Eval workspace path + sc-brainstorm layout reference | 0 refs |
| §12.1 Six grading dimensions table (lines 947-958) | `SKILL.md` `### 12.1 Six grading dimensions` | 6-row table (Citation accuracy, Coverage completeness, Deviation-classification precision, Recommendation actionability, False-positive rate, Regression Recall) with thresholds | 0 refs |
| §12.1 dim #6 asymmetry rationale (line 960) | `SKILL.md` §12.1 closing paragraph | Verbatim — why dim #6 is asymmetric with dim #5 | 0 refs |
| §12.2 Sub-criteria (lines 962-969) | `SKILL.md` `### 12.2 Additional rubric dimensions` | 4-bullet sub-criteria (tier-routing correctness, calibration discipline, tier-escalation-anti-confirmation, T2 vendor heterogeneity) | 0 refs |
| §12.3 Iteration harness table (lines 971-981) | `SKILL.md` `### 12.3 Iteration harness` AND **eval-workspace fixtures** | 3-pilot table (pre-trivial-coverage-gap, post-small-diff-clean, post-large-diff-mixed) + convergence rule (<5% improvement) | Each fixture → separate `.dev/eval-workspaces/sc-reflect/cases/<name>/` directory |
| §12.4 Grader DSL extensions (lines 983-996) | `SKILL.md` `### 12.4 Grader DSL extensions` AND `refs/grader-extensions.md` | 6 semantic types listed (citation_resolves, regex_present/absent, yaml_list_contains, matrix_covers_items, checkpoint_logged, deviation_class_matches); refs/grader-extensions.md owns Python sketches | refs/grader-extensions.md absorbs implementation |
| §12.5 Falsifier eval skeleton (lines 998-1070) | `SKILL.md` `### 12.5 Iteration-3 hardening: falsifier eval case` AND **falsifier-suite skeleton files** | SKILL.md: skeleton layout block + canonical falsifier case YAML + pre_seeding_mechanism block + grader hook description | 4 separate files under `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/`: README.md, T2-converges-on-wrong.yaml (SKELETON), T2-judge-class-collision.yaml (SKELETON), fixtures/spec-with-deliberate-misclassification.md (placeholder) |
| §12.6 Grader model (lines 1072-1076) | `SKILL.md` `### 12.6 Grader model` | Default grader = opus; optional `--jury` for 3-model majority | 0 refs |

---

## §13 Build Path Decision (lines 1080-1112)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §13 preamble (line 1084) | `SKILL.md` `## 13. Build Path Decision` opening | Verbatim — hybrid pick consensus 100% | 0 refs |
| §13.1 Rationale (lines 1086-1092) | `SKILL.md` `### 13.1 Rationale` | 3-numbered rationale (eval-driven, cross-model verification, plugin-override) | 0 refs |
| §13.2 Sequenced build table (lines 1094-1106) | `SKILL.md` `### 13.2 Sequenced build` AND **TASK CHECKLIST itself** | 7-row phase table; phase 1 (hand-author SKILL.md+refs+agent map) AND phase 2 (iteration 1) become the actual task checklist items | This is where the task builder's checklist lives |
| §13.3 What is NOT used (lines 1108-1112) | `SKILL.md` `### 13.3 What is NOT used` | 3 bullets — sprint CLI for build loop, superclaude eval v1, plugin's default sibling workspace | 0 refs |

---

## §14 Error Handling Matrix (lines 1116-1173)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §14 error-handling table (lines 1120-1173) | `SKILL.md` `## 14. Error Handling Matrix` | 41-row table covering: STOP conditions, sc-adversarial F1/F2/F3, missing-skill handling, agent failures (calibrator, evidence-validator, root-cause-analyst, rf-qa, all-T2-fail), merged_output_path missing, input_drift, empty_input, coverage_undefined, alias-routing edges, single-vendor T2, calibrator collision, MCP fallbacks, budget routing, Wave 1B.3 scan failures, Wave 7 scenarios (source disappeared, collision non-identical, collision identical, sha mismatch, adapter unresolved, gate failed, no-promote, promote-anyway-on-failed, cross-fs, alias race, T2+calibrator compound, write_memory fail, audit-log write fail, evidence-validator partial result) | 0 refs |

---

## §14.5 Post-Verdict Promotion Mutation (lines 1176-1367)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §14.5 preamble + SRP boundary (lines 1180-1183) | `SKILL.md` `## 14.5 Post-Verdict Promotion Mutation` opening | Final-QA-gate framing + SRP boundary paragraph | 0 refs |
| §14.5.1 Two registered adapters (lines 1185-1192) | `SKILL.md` `### 14.5.1 Two registered promotion adapters` AND `refs/promotion-adapters.md` `## Adapter table` | 2-row adapter table (task / sprint-release) with source glob, destination, trigger signal; refs/promotion-adapters.md owns full table + operator-added extensions | refs file expands |
| §14.5.2 9-condition strict gate (lines 1194-1218) | `SKILL.md` `### 14.5.2 Default-on with strict 9-condition gate` | 9 numbered conditions (with 5a/5b split + 6a/6b split) + canonical "empty" definition for grounding-gaps + Wave 6 citation-revalidation note | 0 refs |
| §14.5.3 Wave 7 execution fence block (lines 1220-1245) | `SKILL.md` `### 14.5.3 Wave 7 — execution` | Verbatim 7-step Wave 7 fenced block (7.1-7.7 including 7.3.5, 7.3.6) | 0 refs |
| §14.5.4 Override flags table (lines 1247-1255) | `SKILL.md` `### 14.5.4 Override flags` | 5-row flag table (--no-promote, --promote-anyway, --promote-dry-run, --promote-mode, --promote-resume) | 0 refs |
| §14.5.5 Mutation mechanics + collision rules (lines 1257-1303) | `SKILL.md` `### 14.5.5 Mutation mechanics` AND `refs/promotion-adapters.md` `## Mutation mechanics + collision rules` | Move semantics (same-fs atomic, cross-fs non-atomic), promotion-checkpoint.yaml shape, 4-state crash recovery table, --promote-resume flag, promotion-log pre-write, 7-row destination collision rules | refs file owns full body |
| §14.5.6 promotion-log.yaml YAML (lines 1305-1341) | `SKILL.md` `### 14.5.6 Output: promotion-log.yaml` | Full YAML shape (~25 fields including 11-field gate_evaluation block, citation_revalidation_at_promotion, pending, cross_fs_promotion, checkpoint_path, skip_reason, fail_reason, rollback_command) | 0 refs |
| §14.5.7 Acceptance assertions (lines 1343-1363) | `SKILL.md` `### 14.5.7 Acceptance assertions` AND **15 separate fixture files** | SKILL.md: 15-row bulleted assertion list + new grader assertion types (`path_exists`, `path_does_not_exist`) | **15 SEPARATE eval-fixture files** under `.dev/eval-workspaces/sc-reflect/cases/promotion/`: promotion-task-strict-pass, promotion-blocked-by-drift, promotion-blocked-by-frontmatter-missing, promotion-blocked-by-frontmatter-mismatch, promotion-blocked-by-grounding-gaps-empty-list, promotion-blocked-by-null-convergence, promotion-citation-revalidation-after-remediation, promotion-sprint-release-pass, promotion-collision-non-identical, promotion-collision-identical, promotion-no-promote-flag, promotion-promote-anyway-on-partial, promotion-dry-run, promotion-cross-fs-crash-recovery, promotion-log-pre-write-survives-crash (all `.yaml`) |
| §14.5.8 Interaction with §10 (line 1367) | `SKILL.md` `### 14.5.8 Interaction with §10 Deviation Taxonomy` | Verbatim — frontmatter-mismatch is Drift; cond 4 exception note | 0 refs |

---

## §15 Token Cost Profile (lines 1371-1492)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §15 cost-profile table (lines 1375-1379) | `SKILL.md` `## 15. Token Cost Profile` AND `refs/cost-profile.yaml` | 3-row cost table (T1, T2, T3 added) with Auggie/Claude/wall-clock/turn-budget columns | refs/cost-profile.yaml mirrors this as YAML |
| §15 token-to-turn conversion (line 1383) | `SKILL.md` §15 closing | `1 turn ≈ 1k claude-orchestration tokens` conversion + lockstep update rule | 0 refs |
| §15.1 metrics.json schema (lines 1385-1492) | `SKILL.md` `### 15.1 Metrics Export` AND `refs/ops-integration.md` `## Metrics ingestion config` | Full JSON schema (~30 fields), Prometheus/StatsD/OpenTelemetry flattening, counter/gauge/string classification, runs.jsonl append schema, stability guarantee | refs/ops-integration.md owns ingestion config |

---

## §16 Refs Table (lines 1496-1514)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §16 refs table (lines 1500-1512) | `SKILL.md` `## 16. Refs (loaded on-demand per wave)` AND **11 separate ref files** | 11-row table listing each ref with Wave + Purpose columns | See per-ref content roll-up below |

### §16 — Per-ref content roll-up

| Ref file | Consumes content from spec sections | Notes |
|---|---|---|
| `refs/input-resolution.md` | §3.1 flag enumeration, §3.2 6-rule mode selection, §3.3 STOP conditions, §3.4 env prereqs, §4.0 step 0.5 routing table | Wave 0 load |
| `refs/reflection-rubric.md` | §5.2 rubric inputs (5-dimension scoring), §11.3 calibrator selection algorithm | Wave 1D + Wave 3C load |
| `refs/deviation-taxonomy.md` | §10 preamble + scaling rule, §10.1 Authorized, §10.2 Necessary, §10.3 Drift, §10.4 Regression, §10.6 Grounding Gaps, §10.7 reporting | Wave 1B (UC-2) + Wave 5 |
| `refs/coverage-mapping.md` | §5.2 S_dev_density calculation, Wave 1B UC-1 coverage logic (implicit content: bipartite matching, requirement-ID parsing) | Wave 1B (UC-1) load; refs file must define the coverage-mapping algorithm not deeply specified in spec |
| `refs/reviewer-spec.md` | §4.3 Step 3B.0 brief packaging, §7.1 reviewer composition rules + executor-class exclusion + 3-row rotation table | Wave 3A load |
| `refs/report-template.md` | §10.7 deviation rendering, §11.1 Grounded/[INFERRED] tagging, §11.5 budget-policy reporting, §11.6 inferred-claim audit, P4 per-task verdict section (§16 row) | Wave 5 load |
| `refs/remediation-handoff.md` | §7 task-builder Wave 6 row, §8 task-builder integration, §10.3/§10.4 default-remediation guidance | Wave 6 load |
| `refs/ops-integration.md` | §4.0 Step 0.6 vendor-heterogeneity WARN body, §15.1 ingestion config, §17.5 Makefile target table + CI cadence + hook redirect message | build-time load |
| `refs/grader-extensions.md` | §12.4 grader DSL semantic types, §14.5.7 new `path_exists`/`path_does_not_exist` assertion types, §12.5 `falsifier_skeleton_present` assertion | eval-time load |
| `refs/promotion-adapters.md` | §14.5.1 adapter table (full + operator-added), §14.5.4 flag semantics, §14.5.5 mutation mechanics + checkpoint + collision rules + rollback template | Wave 7 load |
| `refs/cost-profile.yaml` | §15 cost-profile table mirrored as machine-readable YAML | pre-invocation load (caller-side) |

---

## §17 Boundaries (lines 1518-1567)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §17 Will list (lines 1524-1543) | `SKILL.md` `## 17. Boundaries` `### Will` | ~17-bullet Will list (T1 always, auto-escalate, heterogeneous reviewers, Serena chain, evidence-validator gate, 4-cat taxonomy, grounding-gaps, Grounded/[INFERRED], CLAUDE.md rules, fail-open MCPs, Serena memory persist, sc-adversarial delegation, Wave 7 promotion, promotion-log forensic, collision refuse, per-task verdicts, interaction-effects scan, budget hints, cost-profile ref) | 0 refs |
| §17 Will Not list (lines 1545-1567) | `SKILL.md` §17 `### Will Not` | ~20-bullet Will Not list (recursive, agent self-confidence, ship without evidence-validator, auto-execute T3, auto-commit, silently-downgrade missing skills, executor commit-msg = gold standard, skip heterogeneous, confirm conclusions, think_about_* load-bearing, .claude/ paths, auto-promote partial/failed, promote without frontmatter agreement, auto-overwrite collision, auto-rollback, git add post-promotion, tasklist_aggregate enum, separate validation_strength field, stream per-task verdicts, cross-tasklist memory, caller-side credit policy) | 0 refs |

---

## §17.5 Ops Integration (lines 1571-1589)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §17.5 preamble (line 1575) | `SKILL.md` `## 17.5 Ops Integration` opening | Reference to refs/ops-integration.md | 0 refs |
| §17.5 `-f` rule (line 1577) | `SKILL.md` §17.5 paragraph + `refs/ops-integration.md` `## -f rule` | Verbatim CLAUDE.md ABSOLUTE rule reference | refs file owns full body |
| §17.5 PreToolUse hook awareness (line 1579) | `SKILL.md` §17.5 + `refs/ops-integration.md` `## Hook redirect` | Workspace-location enforcement | refs file owns full body |
| §17.5 sync-dev/verify-sync workflow (lines 1581-1587) | `SKILL.md` §17.5 + `refs/ops-integration.md` `## sync workflow` | 5-step workflow | refs file expands |
| §17.5 CI cadence (line 1589) | `SKILL.md` §17.5 + `refs/ops-integration.md` `## CI cadence + Makefile targets` | `make reflect-eval-quick` on PR + `make reflect-eval` on RC + Makefile target list | refs file owns full table |

---

## §17.6 Testability Map (lines 1593-1627)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §17.6 testability map table (lines 1599-1625) | `SKILL.md` `## 17.6 Testability Map` | ~28-row protocol-decision → eval-assertion table | 0 refs |
| §17.6 closing paragraph (line 1627) | `SKILL.md` §17.6 footer | Verbatim — orphan-rule + merge-executor verification | **[INFORMATIONAL-NO-BUILD-UNIT]** — recording claim about eval workspace coverage; no separate file follows |

---

## §17.7 Kill List (lines 1631-1647)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §17.7 6-item kill list (lines 1635-1647) | `SKILL.md` `## 17.7 Kill List — Features Deliberately Excluded` | 6 numbered entries (coverage-mapper agent, deviation-classifier agent, streaming dialogue, persistent KG, multi-model T1, 5th unknown deviation cat) each with why-rejected + what-replaces-it | 0 refs |

---

## §18 Spec Reference (lines 1651-1655)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §18 spec ref (line 1655) | `SKILL.md` `## 18. Spec Reference` AND `.dev/eval-workspaces/sc-reflect/SPEC.md` | SKILL.md cites SPEC.md path; SPEC.md is **a separate file** authored alongside SKILL.md per skill-creator iteration-1 protocol. SPEC.md content = design rationale + acceptance criteria + iteration history | SPEC.md is a standalone build unit |

---

## §19 v1.1 Deferred Hardening (lines 1659-1706)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §19 preamble (line 1663) | `SKILL.md` `## 19. v1.1 Deferred Hardening` opening | 2-HIGH-invariant deferral framing | 0 refs |
| §19.1 INV-021 vendor heterogeneity v1.1 (lines 1665-1671) | `SKILL.md` `### 19.1 INV-021` | v1.0 posture + v1.1 candidate hardening + why deferred | 0 refs |
| §19.2 INV-023 sufficiency v1.1 (lines 1673-1682) | `SKILL.md` `### 19.2 INV-023` | v1.0 conditional posture + v1.1 hardening branches (≥80% pass / ≥20% fail) | 0 refs |
| §19.3 Auto-rollback carryover (lines 1684-1690) | `SKILL.md` `### 19.3 Auto-rollback` | v1.0 operator-driven; v1.1 candidate auto-rollback path | 0 refs |
| §19.4 Streaming per-task verdict (lines 1692-1698) | `SKILL.md` `### 19.4 Streaming per-task verdict` | v1.0 batch-emit; v1.1 candidate streaming if consumer materializes | 0 refs |
| §19.5 Cross-tasklist memory (lines 1700-1706) | `SKILL.md` `### 19.5 Cross-tasklist memory` | v1.0 per-project; v1.1 candidate cross-template/cross-agent | 0 refs |

---

## Command File (NEW shape)

| Spec section | Target file | Content unit | Notes |
|---|---|---|---|
| §3.1 flag enumeration | `src/superclaude/commands/reflect.md` | Short command body delegating to `Skill sc-reflect-protocol` via the canonical 20-flag enumeration from §3.1 (mode, spec, tasklist, diff, commit-range, scope, task-log, depth, tier, reviewers, output, coverage-floor, no-mcp, no-evidence-validator, remediate, budget-remaining, no-promote, promote-anyway, promote-dry-run, promote-mode, promote-resume) | NEW shape replaces legacy `think_about_*` surface (see frontmatter `supersedes` line 20) |

---

## Eval Workspace File-by-File Checklist (decomposed from §13.2 phase 1 + §12.3 + §12.5 + §14.5.7)

| File | Source spec section(s) | Notes |
|---|---|---|
| `.dev/eval-workspaces/sc-reflect/SPEC.md` | §18 + §13.2 phase 1 (hand-author) | Design rationale + acceptance criteria + iteration history |
| `.dev/eval-workspaces/sc-reflect/evals/evals.json` | §12.3 (3 pilot evals) + §13.2 phase 2 | Scaffolded JSON listing the 3 pilot evals — UC-1 + 2× UC-2 |
| `.dev/eval-workspaces/sc-reflect/iterations/iteration-1/` (empty skeleton dir) | §13.2 phase 2 + §12.3 | Empty directory; populated by skill-creator run_loop.py |
| `.dev/eval-workspaces/sc-reflect/grader.py` | §12.4 + §14.5.7 + `refs/grader-extensions.md` | Copy from `.dev/eval-workspaces/sc-brainstorm/grader.py` and extend per refs/grader-extensions.md (semantic types) and §14.5.7 (path_exists, path_does_not_exist) |
| `.dev/eval-workspaces/sc-reflect/aggregate_iteration.py` | §13.2 phase 2 (iteration harness) | Copy verbatim from sc-brainstorm/aggregate_iteration.py |
| `.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md` | §12 preamble (line 945) "frozen baseline = current `src/superclaude/commands/reflect.md`" | Frozen copy of legacy reflect.md for baseline-vs-new comparison |
| `.dev/eval-workspaces/sc-reflect/cases/pre-trivial-coverage-gap/` (dir + fixtures) | §12.3 row 1 | UC-1 fixture: 8-spec, tasklist missing 2/8 → coverage_pct=0.75 |
| `.dev/eval-workspaces/sc-reflect/cases/post-small-diff-clean/` (dir + fixtures) | §12.3 row 2 | UC-2 fixture: 3-file clean diff |
| `.dev/eval-workspaces/sc-reflect/cases/post-large-diff-mixed/` (dir + fixtures) | §12.3 row 3 | UC-2 fixture: 15-file diff with 1R+2D+1N+1A |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/README.md` | §12.5 falsifier-suite layout | Describes sufficiency-claim contract |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-converges-on-wrong.yaml` (SKELETON) | §12.5 canonical falsifier YAML | v1.0 ships `status: skeleton-pending-iteration-3-fixture` |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-judge-class-collision.yaml` (SKELETON) | §12.5 layout | Khan ICML 2024 violation case (judge in reviewer pool); SKELETON status |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md` | §12.5 placeholder | v1.0 placeholder; iteration-3 populates |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-task-strict-pass.yaml` | §14.5.7 bullet 1 | All 9 gates pass → action: moved |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-blocked-by-drift.yaml` | §14.5.7 bullet 2 | 1 Drift → action: rejected |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-blocked-by-frontmatter-missing.yaml` | §14.5.7 bullet 3 | No `status` field → frontmatter_present: fail |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-blocked-by-frontmatter-mismatch.yaml` | §14.5.7 bullet 4 | reflect=done, frontmatter=in-progress → frontmatter_status_matches: fail |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-blocked-by-grounding-gaps-empty-list.yaml` | §14.5.7 bullet 5 | Exercises C1 "empty" definition both ways |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-blocked-by-null-convergence.yaml` | §14.5.7 bullet 6 | T2 + convergence=null → adversarial_result_present: fail |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-citation-revalidation-after-remediation.yaml` | §14.5.7 bullet 7 | Wave 6 mutates cited file → 7.2 recomputes citations_dropped |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-sprint-release-pass.yaml` | §14.5.7 bullet 8 | sprint-release adapter destination + parent creation |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-collision-non-identical.yaml` | §14.5.7 bullet 9 | Differing destination → rejected with diff capture |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-collision-identical.yaml` | §14.5.7 bullet 10 | Idempotent → already-promoted |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-no-promote-flag.yaml` | §14.5.7 bullet 11 | --no-promote → skipped, user-flag |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-promote-anyway-on-partial.yaml` | §14.5.7 bullet 12 | --promote-anyway on partial → moved |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-dry-run.yaml` | §14.5.7 bullet 13 | --promote-dry-run → dry-run, no mutation |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-cross-fs-crash-recovery.yaml` | §14.5.7 bullet 14 | Cross-fs crash + --promote-resume → action: resumed |
| `.dev/eval-workspaces/sc-reflect/cases/promotion/promotion-log-pre-write-survives-crash.yaml` | §14.5.7 bullet 15 | Crash between 7.4 and 7.6 → reconciliation on next invocation |

---

## Makefile Targets (decomposed from §17.5)

| Target | Source spec section | Notes |
|---|---|---|
| `make reflect-eval` | §17.5 CI cadence + §16 refs/ops-integration.md row | Full eval ~2 min on RC branches |
| `make reflect-eval-quick` | §17.5 CI cadence | 3-pilot subset <30s on every PR |
| `make sync-cost-profile` | §16 refs/cost-profile.yaml row "Updated in lockstep with §15 by a `make sync-cost-profile` target" | Updates refs/cost-profile.yaml from §15 table |
| `make lint-architecture` | §17.5 workflow step 4 "Run `make lint-architecture` to confirm bidirectional command↔skill link + frontmatter completeness" | Checks command↔skill link + frontmatter completeness |

(Plus existing targets — `make sync-dev`, `make verify-sync`, `make lint`, `make test`, `make eval-skill SKILL=sc-reflect-protocol` — referenced by §17.5 but pre-existing; not net-new build units.)

---

## Informational / No-Build-Unit sections

| Spec section | Why no separate file lands | Notes |
|---|---|---|
| §17.6 closing paragraph (line 1627) | Recording claim about merge-executor verification of testability-map coverage; no file artifact follows | **[INFORMATIONAL-NO-BUILD-UNIT]** |
| §19 v1.1 deferred candidate-hardening paragraphs (§§19.1-19.5 "v1.1 candidate hardening" sub-blocks) | Each entry documents *future* v1.1 hardening; nothing materially built in v1.0 beyond the §11.0 conditional language + skeleton files. v1.0 posture lines are covered by §11.0 + §12.5 mappings above. | **[INFORMATIONAL-NO-BUILD-UNIT]** for the candidate-hardening paragraphs themselves |
| §13.3 What is NOT used (lines 1108-1112) | Negative-space claim — declares what is *not* used; no file lands from this | Content lands in SKILL.md as documentation; no separate artifact |
| §17.7 Kill List | Negative-space claims — documents rejected features; no file lands beyond SKILL.md prose | Content lands in SKILL.md |
| Provenance HTML comments (e.g., lines 25-26, 46-47) | Source-attribution comments; optional in SKILL.md; preserve for audit trail | **[INFORMATIONAL-NO-BUILD-UNIT]** if dropped — recommended to preserve in SKILL.md for traceability |

---

## SKILL.md Target Outline (distilled from §1-§19, anticipated 800-1500 lines)

```
# Reflect Protocol
## 1. Purpose & Core Thesis                                  (§1 — ~30 lines)
## 2. Triggers                                               (§2 — ~10 lines)
## 3. Required Input + Mode Selection                        (§3 — ~80 lines)
   ### 3.1 Inputs                                            (§3.1 — flag list)
   ### 3.2 Mode selection                                    (§3.2 — 6-rule)
   ### 3.3 Hard STOP conditions                              (§3.3)
   ### 3.4 Environment Prerequisites                         (§3.4)
## 4. Wave / Tier Architecture                               (§4 — ~150 lines)
   (fence block + Step 0.4/0.5/0.6/0.9 + Step 1B.1/1B.2/1B.3 + 3B.0 + 5.0)
## 5. Tier-Decision Rubric                                   (§5 — ~80 lines)
   ### 5.1 Hard overrides
   ### 5.2 Rubric inputs
   ### 5.3 Decision logic
   ### 5.4 tier_decision.yaml audit artifact
   ### 5.5 Why these thresholds
   ### 5.6 Escalation reason logging
## 6. Modern Serena Tool Usage                               (§6 — ~50 lines)
## 7. Agent Delegation Map                                   (§7 — ~50 lines)
   ### 7.1 Reviewer composition rules
   ### 7.2 No new agents required
## 8. Cross-Skill Integration                                (§8 — ~40 lines)
## 9. Output Contract (Versioned)                            (§9 — ~200 lines)
   ### 9.1 Stable contract
   ### 9.2 Telemetry
   ### 9.3 Consumer Field Map
   ### 9.4 Contract Evolution
## 10. Deviation Taxonomy                                    (§10 — ~80 lines)
   ### 10.1-10.7
## 11. Hallucination Guardrails                              (§11 — ~70 lines)
   ### 11.0-11.6
## 12. Eval Rubric                                           (§12 — ~120 lines)
   ### 12.1-12.6 (includes falsifier skeleton block)
## 13. Build Path Decision                                   (§13 — ~30 lines)
## 14. Error Handling Matrix                                 (§14 — ~60 lines)
## 14.5 Post-Verdict Promotion Mutation                      (§14.5 — ~180 lines)
   ### 14.5.1-14.5.8
## 15. Token Cost Profile                                    (§15 — ~120 lines)
   ### 15.1 Metrics Export
## 16. Refs (loaded on-demand per wave)                      (§16 — ~20 lines, table)
## 17. Boundaries                                            (§17 — ~50 lines)
## 17.5 Ops Integration                                      (§17.5 — ~20 lines)
## 17.6 Testability Map                                      (§17.6 — ~40 lines)
## 17.7 Kill List                                            (§17.7 — ~25 lines)
## 18. Spec Reference                                        (§18 — ~5 lines)
## 19. v1.1 Deferred Hardening                               (§19 — ~50 lines)
   ### 19.1-19.5
```

Target line count: ~1500 lines (refs absorb heavy detail — adapters/mechanics/grader/etc.)

---

## Summary

**Total build units identified: 41 distinct file-level build units** (counting each file as 1 build unit; SKILL.md absorbs ~75 mapped content-rows internally).

Breakdown:
- **SKILL.md**: 1 file (with ~19 top-level sections + ~50 subsections — ~75 spec→SKILL.md content-row mappings)
- **Command file**: 1 (`src/superclaude/commands/reflect.md` — new shape per §3.1 flag enumeration)
- **Refs**: 11 (per §16 — `input-resolution.md`, `reflection-rubric.md`, `deviation-taxonomy.md`, `coverage-mapping.md`, `reviewer-spec.md`, `report-template.md`, `remediation-handoff.md`, `ops-integration.md`, `grader-extensions.md`, `promotion-adapters.md`, `cost-profile.yaml`)
- **SPEC.md** (eval-workspace): 1 (`.dev/eval-workspaces/sc-reflect/SPEC.md` per §18 + §13.2)
- **Eval-workspace infrastructure**: 5 (`evals.json`, `iterations/iteration-1/` dir, `grader.py`, `aggregate_iteration.py`, `skill-snapshot/reflect-v1.md`)
- **Pilot eval-case directories**: 3 (per §12.3 — `pre-trivial-coverage-gap`, `post-small-diff-clean`, `post-large-diff-mixed`)
- **Falsifier-suite files**: 4 (per §12.5 — README.md + 2× SKELETON yaml + placeholder spec md)
- **Promotion eval-fixture files**: 15 (per §14.5.7 — counted 15 bullets including promotion-log-pre-write-survives-crash; spec text lists 15 bulleted assertions in total)

**Makefile targets**: 4 net-new (not files but Makefile edits — `reflect-eval`, `reflect-eval-quick`, `sync-cost-profile`, `lint-architecture`)

**Spec sections producing no separate build unit (informational only):** §17.6 closing paragraph, §§19.1-19.5 "v1.1 candidate hardening" sub-blocks, §13.3 What is NOT used, §17.7 Kill List, provenance HTML comments — all land into SKILL.md text only, produce no separate file artifact.

**Cross-mapped key observations:**
- §3.4 cites §4 Wave 0 routing table; routing table itself lives in §4.0 Step 0.5 (mirrored in refs/input-resolution.md).
- §15 cost-profile table and refs/cost-profile.yaml MUST stay in lockstep via `make sync-cost-profile`.
- §14.5.7 produces **15** separate fixture files under `.dev/eval-workspaces/sc-reflect/cases/promotion/` — each fixture is independently testable per gate_evaluation field combinations. (Task-builder researcher preamble said "14 fixtures"; recount against spec text identifies 15 bullets including the trailing `promotion-log-pre-write-survives-crash`.)
- §12.5 falsifier-suite ships as SKELETONs in v1.0 (per W-A8 fix), promoted to `status: active` in iteration-3.
- The `coverage-mapping.md` ref is the only ref whose algorithm is *not* deeply specified in the spec — refs/coverage-mapping.md must define the bipartite matching + requirement-ID parsing algorithm called out implicitly by §5.2 S_dev_density definition; researcher 02/07 conventions for ref structure apply.
- §9.1 contract YAML implies a `refs/return-contract.md` (line 655 "Each flag has a one-line semantics description in refs/return-contract.md") but §16 refs table does NOT list this file. Treat as either (a) inline semantics in SKILL.md §9.1, or (b) implicit additional ref. Default to (a) per spec discipline (don't add files not in §16 table).
