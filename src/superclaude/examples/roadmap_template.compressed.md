<!-- CONV: Milestone=MLS, milestone=MI1 -->
# Roadmap Output Template

> **Usage**: This template defines the output structure for the roadmap pipeline's
> generate and merge steps. All `{{SC_PLACEHOLDER:*}}` sentinels must be replaced
> during generation. The pipeline produces output conforming to this skeleton.
>
> **Sentinel self-check**: After generation, verify zero remaining sentinels:
> `grep -c '{{SC_PLACEHOLDER:' <output-file>` should return 0.
>
> **Column contract**: Every MI1 deliverable table MUST use the 9-column schema below.
> Do not add, remove, or reorder columns.
>
> **Formatting contract**: Minimize whitespace. Single blank lines between sections.
> No horizontal rules between milestones. No trailing MI1 summary lines.
> AC as terse semicolon-separated conditions.
>
> **Mutual exclusion**: Exactly one of `spec_source` (scalar) or `spec_sources`
> (list) must be present in frontmatter. Never include both. Never omit both.
>
> **Adversarial block**: The `adversarial:` frontmatter block is present ONLY
> when adversarial mode was used. Omit the entire block otherwise.

---

```yaml
---
spec_source: "{{SC_PLACEHOLDER:spec_filename}}"
complexity_score: {{SC_PLACEHOLDER:0.0_to_1.0}}
complexity_class: {{SC_PLACEHOLDER:LOW_or_MEDIUM_or_HIGH}}
primary_persona: {{SC_PLACEHOLDER:persona}}
adversarial: {{SC_PLACEHOLDER:true_or_false}}
base_variant: "{{SC_PLACEHOLDER:variant_id_or_none}}"
variant_scores: "{{SC_PLACEHOLDER:scores_or_none}}"
convergence_score: {{SC_PLACEHOLDER:0.0_to_1.0_or_none}}
debate_rounds: {{SC_PLACEHOLDER:integer_or_none}}
generated: "{{SC_PLACEHOLDER:yyyy_mm_dd}}"
generator: "{{SC_PLACEHOLDER:adversarial_merge_or_single}}"
total_milestones: {{SC_PLACEHOLDER:integer}}
total_task_rows: {{SC_PLACEHOLDER:integer}}
risk_count: {{SC_PLACEHOLDER:integer}}
open_questions: {{SC_PLACEHOLDER:integer}}
domain_distribution:
  frontend: {{SC_PLACEHOLDER:percentage_or_0}}
  backend: {{SC_PLACEHOLDER:percentage_or_0}}
  security: {{SC_PLACEHOLDER:percentage_or_0}}
  performance: {{SC_PLACEHOLDER:percentage_or_0}}
  documentation: {{SC_PLACEHOLDER:percentage_or_0}}
consulting_personas: [{{SC_PLACEHOLDER:persona_list}}]
milestone_count: {{SC_PLACEHOLDER:integer}}
milestone_index:
  - id: M1
    title: "{{SC_PLACEHOLDER:milestone_title}}"
    type: {{SC_PLACEHOLDER:FEATURE_or_IMPROVEMENT_or_DOC_or_TEST_or_MIGRATION_or_SECURITY}}
    priority: {{SC_PLACEHOLDER:P0_or_P1_or_P2_or_P3}}
    dependencies: []
    deliverable_count: {{SC_PLACEHOLDER:integer}}
    risk_level: {{SC_PLACEHOLDER:Low_or_Medium_or_High}}
total_deliverables: {{SC_PLACEHOLDER:integer}}
total_risks: {{SC_PLACEHOLDER:integer}}
estimated_milestones: {{SC_PLACEHOLDER:integer}}
validation_score: {{SC_PLACEHOLDER:0.0_to_1.0}}
validation_status: {{SC_PLACEHOLDER:PASS_or_REVISE_or_REJECT_or_PASS_WITH_WARNINGS_or_SKIPPED}}
---
```

# {{SC_PLACEHOLDER:project_name}} u2014 Project Roadmap

## Executive Summary

{{SC_PLACEHOLDER:executive_summary}}

**Business Impact:** {{SC_PLACEHOLDER:business_impact}}

**Complexity:** {{SC_PLACEHOLDER:complexity_class}} ({{SC_PLACEHOLDER:score}}) u2014 {{SC_PLACEHOLDER:complexity_rationale}}

**Critical path:** {{SC_PLACEHOLDER:critical_path_description}}

**Key architectural decisions:**

- {{SC_PLACEHOLDER:decision_1}}
- {{SC_PLACEHOLDER:decision_2}}
- {{SC_PLACEHOLDER:decision_3}}

**Open risks requiring resolution before M1:**

- {{SC_PLACEHOLDER:pre_m1_risk_1}}

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|{{SC_PLACEHOLDER:milestone_id}}|{{SC_PLACEHOLDER:title}}|{{SC_PLACEHOLDER:type}}|{{SC_PLACEHOLDER:priority}}|{{SC_PLACEHOLDER:effort}}|{{SC_PLACEHOLDER:dependencies}}|{{SC_PLACEHOLDER:deliverable_count}}|{{SC_PLACEHOLDER:risk_level}}|

## Dependency Graph

{{SC_PLACEHOLDER:dependency_graph_arrow_notation}}

## M{{SC_PLACEHOLDER:N}}: {{SC_PLACEHOLDER:milestone_name}}

**Objective:** {{SC_PLACEHOLDER:milestone_objective}} | **Duration:** {{SC_PLACEHOLDER:duration_estimate}} | **Entry:** {{SC_PLACEHOLDER:entry_criteria}} | **Exit:** {{SC_PLACEHOLDER:exit_criteria}}

<!-- DELIVERABLE TABLE: 9-column schema. # | ID | Title | Description | Comp | Deps | AC | Eff | Pri.
     #: sequential row number. ID: requirement/entity ID from extraction.
     Title: short noun phrase naming the deliverable.
     Description: explanation of what is being built.
     Comp: system component. Deps: comma-separated prerequisite IDs or dash.
     AC: semicolon-separated terse testable conditions.
     Eff: S/M/L/XL. Pri: P0/P1/P2.
     Every extraction ID = one row. Do NOT merge IDs. -->

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|{{SC_PLACEHOLDER:row_num}}|{{SC_PLACEHOLDER:id}}|{{SC_PLACEHOLDER:title}}|{{SC_PLACEHOLDER:description}}|{{SC_PLACEHOLDER:component}}|{{SC_PLACEHOLDER:deps}}|{{SC_PLACEHOLDER:criteria}}|{{SC_PLACEHOLDER:effort}}|{{SC_PLACEHOLDER:priority}}|

### Integration Points u2014 M{{SC_PLACEHOLDER:N}}

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|{{SC_PLACEHOLDER:artifact}}|{{SC_PLACEHOLDER:type}}|{{SC_PLACEHOLDER:wired}}|{{SC_PLACEHOLDER:owner}}|{{SC_PLACEHOLDER:consumers}}|

### MLS Dependencies

- {{SC_PLACEHOLDER:dependency_or_none}}

### Open Questions u2014 M{{SC_PLACEHOLDER:N}}

<!-- Omit this subsection entirely when the milestone has zero open questions.
     OQ-xxx IDs must NEVER be rows in the 9-column deliverable table above u2014
     they are decisions, not deliverables. OQ-xxx MAY appear in the Deps column
     of deliverable rows that wait on the decision. -->

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|{{SC_PLACEHOLDER:oq_num}}|{{SC_PLACEHOLDER:oq_id}}|{{SC_PLACEHOLDER:question}}|{{SC_PLACEHOLDER:impact}}|{{SC_PLACEHOLDER:owner}}|{{SC_PLACEHOLDER:target}}|

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|{{SC_PLACEHOLDER:risk_num}}|{{SC_PLACEHOLDER:risk}}|{{SC_PLACEHOLDER:severity}}|{{SC_PLACEHOLDER:likelihood}}|{{SC_PLACEHOLDER:impact}}|{{SC_PLACEHOLDER:mitigation}}|{{SC_PLACEHOLDER:owner}}|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|{{SC_PLACEHOLDER:dependency}}|{{SC_PLACEHOLDER:MI1}}|{{SC_PLACEHOLDER:status}}|{{SC_PLACEHOLDER:fallback}}|

### Infrastructure Requirements

- {{SC_PLACEHOLDER:infra_requirement_1}}

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|{{SC_PLACEHOLDER:criterion}}|{{SC_PLACEHOLDER:metric}}|{{SC_PLACEHOLDER:target}}|{{SC_PLACEHOLDER:method}}|{{SC_PLACEHOLDER:MI1}}|

## Decision Summary

<!-- Every row must cite the specific data point that drove the decision u2014 no subjective justifications. -->

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|{{SC_PLACEHOLDER:decision}}|{{SC_PLACEHOLDER:chosen}}|{{SC_PLACEHOLDER:alternatives_with_scores}}|{{SC_PLACEHOLDER:data_driven_rationale}}|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|{{SC_PLACEHOLDER:milestone_num}}|{{SC_PLACEHOLDER:duration}}|{{SC_PLACEHOLDER:start}}|{{SC_PLACEHOLDER:end}}|{{SC_PLACEHOLDER:milestones}}|

**Total estimated duration:** {{SC_PLACEHOLDER:total_duration}}
