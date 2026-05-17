# Extract Prompt Structure Discovery

## (a) Line range
`build_extract_prompt()`: lines 82-158

## (b) 8 existing body sections
1. `## Functional Requirements` (with verbatim ID preservation + sub-decomposition)
2. `## Non-Functional Requirements` (with verbatim ID preservation)
3. `## Complexity Assessment`
4. `## Architectural Constraints`
5. `## Risk Inventory`
6. `## Dependency Inventory`
7. `## Success Criteria`
8. `## Open Questions`

## (c) 13 existing frontmatter fields
spec_source, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode

## (d) Identifier language
"Use the spec's exact requirement identifiers verbatim as primary IDs. Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002). If a spec uses FR-EVAL-001.1, use FR-EVAL-001.1. If a requirement needs sub-decomposition, use suffixes on the original ID (e.g., FR-EVAL-001.1a, FR-EVAL-001.1b). If the spec has no requirement IDs, then use FR-NNN as a fallback."

## (e) Retrospective block pattern
```python
if retrospective_content:
    advisory = (
        "\n\n## Advisory: Areas to Watch (from prior retrospective)\n\n"
        "The following retrospective content is provided as advisory context "
        "only. These are areas to watch during extraction -- they are NOT "
        "additional requirements and MUST NOT be treated as such. Use them "
        "to inform your risk assessment and open questions sections.\n\n"
        f"{retrospective_content}"
    )
    base += advisory
```

## (f) _OUTPUT_FORMAT_BLOCK usage
Appended via string concatenation: `return base + _OUTPUT_FORMAT_BLOCK`
The constant forces YAML frontmatter start — no preamble.

## (g) _INTEGRATION_ENUMERATION_BLOCK / _INTEGRATION_WIRING_DIMENSION
NOT used in build_extract_prompt(). Used only in build_generate_prompt() and build_spec_fidelity_prompt().

## (h) Other module-level constants
- `_DEPTH_INSTRUCTIONS` (dict for debate depth levels)
- `_INTEGRATION_ENUMERATION_BLOCK` (integration point enumeration for roadmap generation)
- `_INTEGRATION_WIRING_DIMENSION` (wiring completeness dimension for fidelity check)
- `_OUTPUT_FORMAT_BLOCK` (YAML frontmatter enforcement)

## 6 new TDD sections (from research/06-tdd-template-structure.md)
1. Data Models and Interfaces — entities, fields, types, constraints, relationships, storage from §7
2. API Specifications — endpoints, methods, paths, auth, params, schemas, errors, versioning from §8
3. Component Inventory — routes, components, hierarchy, state stores/transitions from §9/§10
4. Testing Strategy — test pyramid, test case tables, environment matrix from §15
5. Migration and Rollout Plan — phases, flags, rollout stages, rollback procedures from §19
6. Operational Readiness — runbooks, on-call, capacity, observability from §14/§25
