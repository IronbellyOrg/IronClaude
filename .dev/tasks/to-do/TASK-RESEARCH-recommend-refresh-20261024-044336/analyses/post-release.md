# Research: /sc:post-release recommendation alignment

- **Topic type:** Command routing research
- **Scope:** Six-month command history, current protocol, recommendation surfaces, plugin implications and regression coverage
- **Status:** Complete; research only, no files changed
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/post-release.txt`, worker `ab75dfdfe1e3006f7`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Commit `0d3b99c8` dated 2026-07-06 introduced the command-backed interface and `sc-post-release-protocol` package, converting the previous standalone skill into a deprecated compatibility wrapper. This was a substantive entry-point and packaging change, not merely formatting. The current command still mandates the protocol handoff and identifies `/sc:post-release` as the primary surface. Evidence: inspected commit patch; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/post-release.md:60-79`.

[CODE-VERIFIED] Commit `3ae238b1` dated 2026-09-30 deleted the compatibility wrapper, removed `sequential` from command and protocol MCP metadata, and removed the command's promise that the wrapper remained available. Commit `782621f4` dated 2026-10-01 removed `sequential` from protocol telemetry fields. These are alias removal and dependency-contract cleanup, not new release-processing capabilities. Evidence: inspected patches for both commits; current command prohibition at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/post-release.md:75-79`.

### Current command contract

[CODE-VERIFIED] The public input is a release version naming an existing tag. Its only optional flag is `--output`, defaulting to a version-specific testing directory. Ground-up versus additive processing is detected automatically; these are not user-selectable flags. The command covers user documentation, technical documentation, install/deploy scripts with actual validation, and user/sysop human-test guides. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/post-release.md:13-44`.

[CODE-VERIFIED] This is a mutating follow-through command, not a documentation audit or report-only operation. It updates and creates external artifacts, produces a report and manifest, and records install evidence. Its protocol gates writing behind consolidated planning and requires confirmation or standing authorization before commits, pushes, PRs, provisioning, or installs against shared/real targets. Recommendation must disclose these effects without implying that suggesting the command authorizes those actions. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-post-release-protocol/SKILL.md:218-235,328-353`.

[CODE-VERIFIED] Missing version input stops execution. An untagged version requires explicit confirmation before a pre-tag run. Scanning remains anchored to the release tag even when the working tree differs. Prior manifests enable additive processing; this is an incremental-release mechanism, not a documented interrupted-run resume flag. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-post-release-protocol/SKILL.md:65-105`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide reduces this command to “After tagging a release” in Other commands, with no dedicated routing row. Meanwhile, its `document-built` routing row covers technical references, operational guides, README work and API reference. The command therefore has substantially more capability than the guide communicates. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:279,303-325` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/post-release.md:38-44`.

[CODE-VERIFIED] This placement matters procedurally. Recommendation consults Other commands only when no routing row matches. A matched row decides the route and skips semantic ranking and cache lookup. Consequently, a request describing a tagged release's documentation and installation follow-through can be captured by the generic documentation route before this specialized command is considered. This is an identified routing risk, not a claim that an end-to-end recommendation run reproduced it. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:50-61,120-150`.

[CODE-VERIFIED] On unmatched requests, the generic hard-limit fallback can also replace a specialized multi-file operation with implementation planning. Current wording directs larger, longer or riskier work to task-builder. That is current source policy, not the user's desired new policy. Post-release already owns its own planning and execution sequence, so breadth alone should not cause recommend to prepend a generic implementation pipeline. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:148-157` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-post-release-protocol/SKILL.md:317-340`.

[CODE-VERIFIED] The plugin's bundled guide repeats the same minimal Other commands entry. Its recommendation skill supports guide-first matching and missing-step reporting. Tracked-file inspection found no plugin post-release command/protocol package, so a plugin-only installation must not be promised a runnable local command without discovery. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:279`; inspected plugin recommendation contract and tracked-path search.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Add a supporting-task `post-release` row and explanatory subsection to `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`. Match intent such as “bring a tagged release's external surface current” or “validate installation and create release human-test guides.” Use level `-`, `changes_files: yes`, one command step, no mandatory optional flags, and notes requiring the target version and preserving authorization boundaries. Grounding: command contract above; existing eight-column routing contract at lines 301-302.

[UNVERIFIED] **MUST, proposed policy:** Make the release-specific intent more specific than generic document writing, while preserving individual documentation commands for focused requests. Do not route every mention of “release,” “README,” or “testing” here. Paste-ready example, only when that tag and destination were supplied by the user: `/sc:post-release v1.4.1 --output docs/testing/v1.4.1/`. The exact syntax is verified at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/post-release.md:23-36`.

[UNVERIFIED] **MUST, proposed policy:** Preserve dedicated command ownership before applying generic implementation-size escalation. Most actual planned implementation should follow workflow plus implement under the user's new policy; task-builder plus task remains for exceptionally complex, long-running implementation or explicit MDTM inputs. Neither pair should replace post-release merely because it touches many artifacts. Apply this consistently to recommendation's Phase 1 and condensed cold-path instructions, without adding another keyword-routing table.

[CODE-VERIFIED] A guide edit already changes the cache surface hash, and a matched new row bypasses both cache paths. No post-release-specific classifier key is necessary for that route. The surface hash includes guide bytes but only command/skill/agent path names; it does not establish freshness of every delegated protocol's content. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:60-67`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks, grounded in the verified contracts:

1. Tagged-release external-surface follow-through selects post-release, discloses mutation, and retains the supplied version/output.
2. A focused README or operational-guide request stays with its documentation command.
3. Missing version requests clarification rather than inventing a tag.
4. Pre-tag work is not silently treated as ordinary post-release execution.
5. A prior manifest does not generate invented `--additive` or resume flags.
6. Plugin-only absence produces the documented not-installed outcome.
7. A generic implementation request still uses workflow plus implement by default; explicit MDTM execution remains separate.

## Gaps

[CODE-VERIFIED] Existing guide tests explicitly require post-release in Other commands. Moving it requires updating that assertion and adding a stable dedicated routing-row expectation. Existing recommendation tests pin general textual rules, not the release-specific distinction. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:26-81`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-80`.

[UNVERIFIED] No command execution, install validation or recommendation evaluation was performed. Historical tag-resolution ambiguity and prior-tag selection are protocol-hardening follow-ups, not reasons to invent recommendation flags. Negative searches found no explicit post-release handling in recommendation refs, classifier/cold-path prompts, or recommendation hook.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Promote tagged-release follow-through from a vague discovery hint into the existing governing routing table, preserve its full mutating capabilities, and update the plugin guide and routing tests together.

[UNVERIFIED] **SHOULD:** Add focused positive and negative recommendation scenarios covering generic-documentation overlap, missing tags, plugin absence and additive runs.

[UNVERIFIED] **NONE:** No command implementation, new classifier key, duplicate keyword table, direct protocol-skill recommendation, or restored legacy alias is needed.
