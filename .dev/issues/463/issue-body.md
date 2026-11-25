<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Research intelligent decision-model-based selection of the model and effort for a session, as a follow-on to the Opus-default and Tier1b-default investigation.

## Problem Statement

Investigate how to choose the right model and effort for a session and whether existing routers can work with the session and proxy setup.

## User Story

As a session user, I want informed model and effort selection, so that the appropriate model is chosen for my session.

## Proposed Solution

Research existing model and effort routers before choosing a design. Consider Jev as a candidate decision model, but first verify its identity and capabilities. Examine the user-provided example https://github.com/alex4o/cliproxy-effort-router and find other relevant examples; its compatibility and implementation here are not established.

## Acceptance Criteria

- [ ] Produce a source-backed comparison of the provided example and other relevant routers, including their model and effort selection capabilities and any unknowns.
- [ ] Verify what Jev is and assess its capabilities as a candidate, or document why that remains unknown.
- [ ] Identify existing session, model configuration, and proxy integration points and assess compatibility and feasibility using evidence.
- [ ] Provide a reasoned recommendation and outstanding questions before any implementation or design choice.

## Out of Scope

Implementation and choosing a design before the research is complete.

## Components Affected (from `/sc:analyze`)

Potential investigation points, not a settled implementation scope:
- `src/superclaude/skills/ccsession-tag/ccsession` — session model and tier selection, and local proxy setup.
- `src/superclaude/skills/ccsession-tag/ccsession.env.example` — example session proxy configuration.
- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` — model aliases and tier request forwarding.
- `src/superclaude/skills/ccsession-tag/ccsession-models.json` — model profile data.

Quick static pass only; codegraph and auggie tools were unavailable, so Glob, Grep and Read were used. Compatibility and effort-routing behavior remain to be researched.

## Related Issues/PRs

Not known yet

<!-- sc:issue:create template=issue-feature-simple -->
