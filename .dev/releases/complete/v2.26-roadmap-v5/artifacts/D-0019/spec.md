# D-0019: build_deviation_analysis_prompt()

## Location
`src/superclaude/cli/roadmap/prompts.py`

## Signature
```python
def build_deviation_analysis_prompt(
    spec_fidelity_path: Path,
    debate_path: Path,
    diff_path: Path,
    spec_deviations_path: Path,
    roadmap_a_path: Path,
    roadmap_b_path: Path,
) -> str:
```

## Classification Taxonomy
- PRE_APPROVED → no_action
- INTENTIONAL (routing_intent: superior | preference) → update_spec or no_action
- SLIP → fix_roadmap
- AMBIGUOUS → human_review

## Normative Classification Mapping (FR-078)
| Annotation Class       | Analysis Class | Default Routing  |
|------------------------|---------------|------------------|
| INTENTIONAL_IMPROVEMENT | INTENTIONAL  | update_spec or no_action |
| INTENTIONAL_PREFERENCE  | INTENTIONAL  | no_action        |
| SCOPE_ADDITION          | AMBIGUOUS    | human_review     |
| NOT_DISCUSSED           | SLIP         | fix_roadmap      |

## Routing Table
- fix_roadmap: roadmap must be corrected
- update_spec: spec should be updated to reflect intentional change
- no_action: no action required
- human_review: requires human judgment

## Output Contract
YAML frontmatter (schema_version: "2.25" first):
- schema_version: "2.25"
- total_analyzed: integer
- slip_count: integer
- intentional_count: integer
- pre_approved_count: integer
- ambiguous_count: integer
- routing_fix_roadmap: comma-separated DEV-\d+ IDs
- routing_update_spec: comma-separated DEV-\d+ IDs (or empty)
- routing_no_action: comma-separated DEV-\d+ IDs (or empty)
- routing_human_review: comma-separated DEV-\d+ IDs (or empty)
- analysis_complete: boolean

Body: ## Deviation Analysis with per-DEV-NNN entries including routing_intent and blast radius for INTENTIONAL deviations; ## Spec Update Recommendations for update_spec routed deviations.
