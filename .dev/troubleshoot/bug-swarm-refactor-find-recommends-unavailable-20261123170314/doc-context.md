# Documentation Context Card

**Generated**: 2026-11-23T17:07:01Z
**Wave**: 1.5
**Scope**: (none); localized swarm recommendation path

## Release context
- Release: v5.0.0 historical post-release documentation.
- Artifacts: .dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md and scan/A2-feature-user-docs.md.
- Summary: CONSOLIDATED-PLAN.md:634-650 explicitly parks this same unavailable-command finding outside the historical documentation run. That old scope restriction is not authority for this session; the current request authorizes diagnosis only. No governing PRD/TDD was found in the requested current/complete release locations.
- Confidence: 0.95 (branch retrieval score, not diagnosis calibration).

## Architectural docs consulted
- docs/swarm/lens-catalog.md: current by mtime/header rubric; :25 and :49 repeat the stale recommendation. Code wins over this descriptive duplication; update those references with a future fix.
- docs/dev/lens-contribution-policy.md: current; :287-292 requires an existing downstream command, :317-334 requires compatible substitutions and flags. :294-302 explains recommendation is never executed automatically.
- docs/swarm/command-reference.md: current; branch B reports artifact and resume documentation. No new report claim relies on its unverified resume assertion.
- All three doc mtimes and affected-code mtimes were 1795451558. Equal checkout mtimes satisfy the rubric, not historical review-date proof. No stale status/last-reviewed marker was found.

## Restrictions / decisions that constrain the fix
- docs/dev/lens-contribution-policy.md:287-292: `recommended_next_command_template` MUST reference a downstream command, skill or CLI that exists today.
- src/superclaude/cli/swarm/lenses/_validate.py:398-401: suspect=False forbids {suspect_files}; do not solve file-list reuse by violating that coupling.
- docs/dev/lens-contribution-policy.md:294-302: recommendations are suggestions, never auto-executed.
- docs/swarm/lens-catalog.md:8-11: recipes preserve findings; cross-worker comparison belongs downstream.
- Full semantic restriction inventory, including historical compressed requirements and exact preservation clauses, is retained in wave1_5-branch-C.md.

## Re-frame signals
- The catalog mirrors the defect, while the contribution policy explicitly rejects unavailable commands and unsupported flag combinations. This is a code/configuration defect with documentation duplication, not intended correct behavior.
- The historical suggestion that built-in /code-review is intended is not verified replacement guidance. The installed /sc:adversarial contract accepts actual comma-separated report files for comparison, not automatic source modification.
- Preserve experimental status, suspect=False, report bodies and the suggestion-only boundary. Current diagnosis does not authorize implementation or publication.
