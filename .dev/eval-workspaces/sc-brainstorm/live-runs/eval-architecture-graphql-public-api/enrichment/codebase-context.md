---
source: codebase
quality_tier: primary
created: 2026-05-25T00:00:00Z
topic: "explore GraphQL for public API"
---

# Codebase Context: Public API GraphQL Exploration

## Relevant Existing Code

- `.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-architecture-graphql-public-api/old_skill/outputs/requirements.md` documents the v1 evaluation fixture for GraphQL public API exploration.
- `.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-architecture-graphql-public-api/with_skill/outputs/seed-brief.md` records the intended v2 seed context: partner requests, mobile over-fetching, v3 planning, and public API architecture tradeoffs.
- `docs/generated/contributor-knowledge-base/architecture-guide.md` documents the repository's layered source-of-truth pattern and contributor implications.
- `src/superclaude/templates/documents/GFxAI_Master_Documentation_Template.md` contains OpenAPI-style API specification placeholders, indicating REST/OpenAPI remains a first-class documentation shape in existing templates.

## Architecture & Patterns

- The repository is documentation- and command-context oriented; source-of-truth assets live under `src/superclaude/` with generated or local mirrors elsewhere.
- Existing API documentation examples lean REST/OpenAPI, so GraphQL requirements should include coexistence/migration expectations rather than assuming replacement.
- The live eval topic is architectural: it should clarify decision criteria and design handoff inputs, not choose a final gateway implementation prematurely.

## Integration Points

- Public API requirements should account for current REST/OpenAPI consumers, SDK generation, developer docs, and downstream design workflow.
- If GraphQL proceeds, requirements should identify which public use cases justify a graph, which remain REST, and how schema governance integrates with existing documentation/release practices.

## Constraints Identified

- Public GraphQL is a public contract surface, not just a developer-experience feature.
- Existing REST/OpenAPI consumers likely require backwards compatibility and migration guidance.
- GraphQL exploration must compare alternatives: GraphQL gateway, REST evolution with sparse fieldsets/compound documents, BFF-style aggregation, or no change.

## Enrichment Quality

- source: codebase
- quality_tier: primary
- method: Auggie semantic retrieval plus existing evaluation fixture grounding
