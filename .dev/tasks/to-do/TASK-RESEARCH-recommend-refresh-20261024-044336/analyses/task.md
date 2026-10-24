# Research: /sc:task recommendation accuracy

- **Topic type:** Command-specific routing research
- **Scope:** /sc:task changes from 2026-04-24 through 2026-10-24; current recommendation contracts and related execution boundaries.
- **Status:** Research complete; no implementation or execution tests performed.
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/task.txt`, worker `ae791939c4459c177`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Five commits changed the command during the window. The actual patches distinguish formatting from behavior:

- `89df2c11`, 2026-05-22: blank-line normalization only.
- `021f715c`, 2026-05-27: code-fence language labels plus a substantive `Activation` section requiring the protocol skill.
- `300c06a6`, 2026-06-17: command wording changed from “forensic analysis” to “diagnostic escalation”; its delegated protocol substantively replaced `/sc:forensic` with `/sc:troubleshoot`.
- `3ae238b1`, 2026-09-30: removed `sequential` and `magic` from command MCP metadata.
- `5c6a7d91`, 2026-10-22: corrected the protocol reference to its installed location.

Evidence: exact `git log -p` patches for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task.md`.

[CODE-VERIFIED] Delegated changes also matter: `046a03ab`, 2026-10-03 removed Sequential from required-server declarations; `051f39fe`, 2026-10-14 replaced obsolete configuration-document references with the command’s tier rules and installed core documents. The current TFEP contract invokes troubleshoot for diagnosis only, then retains remediation insertion and strict-tier resume inside task-protocol. These are documentation contracts, not runtime results verified here. Evidence: exact patches and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-task-protocol/SKILL.md:209-245`.

### Current command contract

[CODE-VERIFIED] `/sc:task` accepts a job description/operation, optional target, and named controls for strategy, compliance, verification and delegation. The documented tier choices are `STRICT`, `STANDARD`, `LIGHT`, and `EXEMPT`; compliance overrides are checked first. The command requires a machine-readable classification header before tools, directs LIGHT/EXEMPT work to immediate execution, and delegates STANDARD/STRICT execution to `sc:task-protocol`. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task.md:18-25,38-102`.

[CODE-VERIFIED] This is an execution command, not a report-only command or MDTM task-file runner. STANDARD execution includes downstream-impact inspection and “affected tests OR document manual verification”; STRICT adds a verification agent and comprehensive tests. LIGHT has a sanity check rather than formal verification. STRICT requires Serena without fallback. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-task-protocol/SKILL.md:82-133,283-295`.

[CODE-VERIFIED] TFEP freezes implementation on qualifying failures, uses troubleshoot without `--fix`, presents wrong-test and documentation outcomes for user review, and resumes adjudicated remediation with strict compliance. `--no-escalation` defaults to false and explicitly disables that protection. Recommendations must not add this escape hatch automatically. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task.md:44-48`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-task-protocol/SKILL.md:135-245`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide correctly distinguishes `/sc:task` from `/task`: one direct job versus execution of an existing MDTM file. It also correctly routes `TASK-WF-*` plans to `/sc:implement`, never `/task`. The implementing command explicitly refuses to invoke either task executor or import MDTM phase gates. Preserve these boundaries. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:215-216,242-243`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/implement.md:126-142`.

[CODE-CONTRADICTED] The guide’s level-2 promise that STANDARD always runs affected tests overstates its delegated contract: STANDARD expressly permits documented manual verification. Likewise, “skipped checking” is too broad for LIGHT, whose contract includes a sanity check. Replace promises with verification evidence actually returned. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:16`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-task-protocol/SKILL.md:100-129`.

[CODE-VERIFIED] Current recommendation rules preserve the small-change hard limit but over-escalate planned work: the guide selects MDTM for “many files,” “more than one session,” or “must not drift,” while the recommendation skill uses “anything larger, longer, or riskier.” The user’s requested workflow-first policy is a proposed change, not current source behavior. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:304-308`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:148-157`.

[CODE-VERIFIED] Matched guide rows bypass both cache paths and semantic ranking; unmatched requests may receive a cached envelope verbatim. Surface hashing includes discovered paths and guide bytes, not all primitive contents; therefore editing the guide invalidates rows, but editing only a delegated task protocol does not necessarily invalidate a row whose source is the unchanged command. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:58-85`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, desired policy:** retain `/sc:task` as an optional small, direct compliance-aware executor, not the default answer for every implementation keyword. Above the existing direct-change limit, prefer `/sc:workflow` followed by `/sc:implement` for ordinary planned implementation. Reserve MDTM creation for explicitly requested MDTM artifacts or the most complex, long-running workloads needing its documented phase structure. File count, existing specs, resume, and auditability alone must not trigger MDTM.

[CODE-VERIFIED] Concrete edit targets are guide section 1, sections 3.2/3.3/5, and routing rows `simple-plan`, `task-file`, and `feature-existing`; recommendation Phase 1 and its delegation heuristic; and the cold-path wording in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:160-175`. Coordinate guide changes with its core CLAUDE copy and plugin guide. The classifier’s `task-file-generation` example also needs an explicit-MDTM boundary rather than treating an unspecified “tasklist” as necessarily MDTM. Its current text is at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:55-79`.

[UNVERIFIED] **MUST, desired examples:** for a supplied small rename request, emit `/sc:task "<exact user-provided rename and matching test change>"`, then require actual test evidence. For ordinary planned work, emit `/sc:workflow "<user-provided goal, constraints and source paths>" --depth quick`, read its printed plan, then `/sc:implement <printed-plan-path>`. For an explicit existing MDTM file, preserve `/task <provided-task-file>`. Keep placeholders visible until supplied; invent no paths.

[CODE-VERIFIED] These examples use documented interfaces. Workflow’s default handoff is non-executing, and its plan boundary explicitly excludes MDTM `/task`. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md:33-40,63-80`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed regression cases:

1. One-source-file rename, three edits: direct edit or `/sc:task`, not MDTM.
2. Rename requiring eight edits: written workflow plan, not direct execution.
3. Ordinary feature across several files and sessions: workflow-first, without unsupported capacity promises.
4. Explicit existing MDTM execution: `/task`, never `/sc:task`.
5. Existing `TASK-WF-*` package resume: `/sc:implement`.
6. STANDARD using manual verification: no claim that tests passed.
7. TFEP failure: no invented forensic command, automatic bypass flag, or duplicated diagnostic protocol.
8. Plugin command present but delegated skill absent: mark unavailable instead of claiming runnable.
9. Matched row: updated policy wins without cache lookup; unmatched cold/native paths retain the same boundary.

## Gaps

[CODE-VERIFIED] Tracked-path inspection found no source `sc-recommend-protocol` directory and no plugin `sc-task-protocol` directory, although `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/task.md:156-161` delegates to that protocol. A globally installed legacy protocol remains at `/config/.claude/skills/sc-recommend-protocol/SKILL.md:20-44`, with obsolete keyword categories. It is not the current recommend activation target.

[CODE-CONTRADICTED] Task’s classification-before-tools rule conflicts with the governing guide’s skill-first rule. Record as a follow-up affecting accurate execution claims; do not resolve it by embedding classification logic in recommendations. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task.md:50-57`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:232`.

[CODE-VERIFIED] The recommendation hook explicitly describes itself as fail-open, not mechanical enforcement. Existing routing tests inspect prose and parity, not the behavioral scenarios above. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:2-13`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-80`.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** align workflow-first policy across guide, recommendation fallbacks, classifier examples, mirrors, and regression scenarios while preserving explicit MDTM inputs.

[UNVERIFIED] **SHOULD:** correct verification promises and verify delegated-skill availability, especially for plugin-only installs.

[UNVERIFIED] **NONE:** no reason to replace `/sc:task`’s internal compliance classifier, add another fixed keyword-routing table, or duplicate TFEP inside recommendation prompts.
