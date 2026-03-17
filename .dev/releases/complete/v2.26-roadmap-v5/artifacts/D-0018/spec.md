# D-0018: build_annotate_deviations_prompt()

## Location
`src/superclaude/cli/roadmap/prompts.py`

## Signature
```python
def build_annotate_deviations_prompt(
    spec_file: Path,
    roadmap_path: Path,
    debate_path: Path,
    diff_path: Path,
) -> str:
```

## Classification Taxonomy
- INTENTIONAL_IMPROVEMENT (requires D-XX + round citation)
- INTENTIONAL_PREFERENCE (requires D-XX + round citation)
- SCOPE_ADDITION
- NOT_DISCUSSED (default when evidence absent)

## Anti-Laundering Rules
1. Architectural quality does NOT prove intentionality
2. Citation must reference specific D-XX + round number from debate transcript
3. Unverifiable citations default to NOT_DISCUSSED
4. Conservative bias: over-report NOT_DISCUSSED rather than launder slips

## Output Contract
YAML frontmatter (schema_version: "2.25" first):
- schema_version: "2.25"
- total_annotated: integer
- intentional_improvement_count: integer
- intentional_preference_count: integer
- scope_addition_count: integer
- not_discussed_count: integer
- annotation_complete: boolean

Body: ## Deviation Annotations with DEV-NNN entries containing ID, Classification, Debate Citation, Spec Quote, Roadmap Quote, Rationale.
