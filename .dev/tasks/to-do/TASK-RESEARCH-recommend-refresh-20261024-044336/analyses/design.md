# Research: /sc:design recommendation alignment

- **Topic type:** Command routing and capability research
- **Scope:** Six-month command history, current design contract, recommendation surfaces, plugin consequences, and regression requirements
- **Status:** Complete, source inspection only; no commands executed to validate behavioral claims
- **Date:** 2026-10-24
- **Delivery:** Returned inline because developer instructions prohibit writing report files.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/design.txt`, worker `a4f87fa82264d0ec2`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command has one reachable change in the requested 2026-04-24 through 2026-10-24 window: commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, titled `chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format repo-wide (#74)`. Its actual patch adds blank lines and a trailing newline only. It does not change design types, output formats, approval boundaries, or the implementation handoff. Scope inclusion is therefore formatting-driven, not evidence of newly introduced capabilities. Source: git history and patch for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md`.

### Current command contract

[CODE-VERIFIED] `/sc:design` is self-contained: its complete command file contains no `Activation` section or delegated skill. Its inputs are a target and two documented options: `--type architecture|api|component|database` and `--format diagram|spec|code`. No default values, output-directory flag, depth flag, or resume mechanism are documented. The behavioral contract covers requirements analysis, design, validation, and documentation, not implementation execution. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:12-45`.

[CODE-VERIFIED] `--format code` means component/interface definitions and implementation guidance, not permission to implement a feature. The boundary explicitly prohibits actual implementation code and architecture modification without explicit design approval. The source names diagrams, API specifications, schemas, and interface definitions as outputs, followed by an approved-design handoff to `/sc:implement`. These are documentation contracts, not verified runtime guarantees. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:72-109`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide recognizes design as an optional API-specification drafting step, but attaches it to `feature-existing`, whose actual steps require `/task-builder` and `/task`. It has no standalone design-authoring routing row. Consequently, focused design requests have no explicit matched-row protection from implementation-oriented routes. The command itself supports four design types, not API design alone. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:303-320`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:14-22`.

[CODE-VERIFIED] The guide already distinguishes a focused `/sc:design` draft from a full, researched and reviewed `/tdd`. That distinction should remain; preserving design does not mean replacing dedicated TDD authoring. Its current comparison lists API, component, and schema examples, while the command additionally supports architecture. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:244`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:22-38`.

[CODE-CONTRADICTED] Recommendation flag verification is narrower than this command’s documentation structure. Rule R1 permits flags only from a flag table or `argument-hint`, whereas design documents its valid flags in `Usage` and examples, without either structure. Strict application would reject the guide’s own valid `--type api --format spec` example. The cold-path runbook repeats this restriction. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:237,335-337`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:1-23,64-68`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:200-202`.

[CODE-VERIFIED] Existing routing tests check flag presence anywhere in command source, not specifically in a table or hint. They therefore accept flags that recommendation prose would reject. This is a contract inconsistency, not evidence that a live invocation has already dropped those flags. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:217-255,286-304`.

### Proposed recommendation changes

[UNVERIFIED] **MUST: Add a focused-design route to the governing guide**, then carry it into the plugin guide. Match requests to draft a specific architecture, API, component interface, or database design without requesting implementation. Stop after the requested design deliverable. Keep full template-based technical-document requests with `/tdd`; keep comparison and critique requests with their dedicated commands. This proposal follows the command’s existing boundaries, not a new capability. Target: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`, workflow prose and routing table. Supporting contract: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:12-38,88-109`.

Paste-ready examples grounded in that contract:

```text
/sc:design payment-api --type api --format spec
/sc:design notification-service --type component --format code
/sc:design e-commerce-db --type database --format diagram
/sc:design user-management-system --type architecture --format diagram
```

[UNVERIFIED] **MUST: Make flag verification recognize explicit Usage syntax.** Amend Rule R1, ordered-workflow validation, surface-verification guidance, and the cold-path runbook to accept a flag explicitly documented in the verified command’s Usage syntax, as well as its table or hint. Continue rejecting undocumented names and values. This is preferable to discarding useful design options merely because their documentation uses a different layout. Targets: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:132,237,335-337`, `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:58-60`, and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:145-148,200-202`.

[UNVERIFIED] **MUST: Separate design approval from execution-route selection.** For subsequent implementation requests, apply the user’s desired policy: `/sc:workflow` plus `/sc:implement` for most planned work; `/task-builder` plus `/task` only for the most complex, long-running workloads or explicit MDTM inputs. Neither a design/spec artifact nor file count, multiple sessions, auditability, or resume needs alone should force MDTM. This differs from current `task-file` and `feature-existing` rules and requires coordinated guide changes, not a competing keyword table. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:305-309`.

[CODE-VERIFIED] A guide-matched design route would bypass the recommendation cache and semantic-ranking step while retaining source verification. Guide content changes also participate in the cache fingerprint. Therefore, adding a design classifier key is unnecessary for the matched route. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:50-67`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-94`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed acceptance cases, derived from `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:22,59-109`:

1. A database-diagram request returns design with `--type database --format diagram`, without implementation steps.
2. A component contract request preserves `--format code` but does not authorize production implementation.
3. A full reviewed TDD request retains the dedicated TDD route.
4. An approved ordinary API design followed by “plan implementation” defaults to workflow/implement, not MDTM.
5. An explicit existing MDTM task input retains `/task`.
6. Valid Usage-documented flags survive verification; invented `--depth` or `--output` flags on design are rejected.
7. Matched design routing bypasses stale cache recommendations and verifies the applicable live command source.

## Gaps

[CODE-VERIFIED] Searches found no design-specific recommendation cases in the inspected recommendation test directories. Unrelated filenames named `design.md` and roadmap `/design` compliance examples are false positives, not routing coverage. The inspected routing tests enforce structural and textual properties rather than actual model selection. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:197-255,286-304`.

[CODE-VERIFIED] The plugin design command ends at its boundaries and lacks the source command’s explicit Output/Next Step tail. Its types and formats remain documented. Treat this as a mirror-completeness follow-up, not proof of different execution behavior. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/design.md:88-100`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:102-109`.

[CODE-CONTRADICTED] Recommendation’s assertion that its gate cannot be skipped overstates enforcement: the hook explicitly describes itself as fail-open and exits zero. This does not establish design routing correctness. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md:60`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-13,85`.

## Key Takeaways

[UNVERIFIED] **CHANGE, MUST:** Protect focused design authoring, accept verified Usage-documented flags, and remove automatic MDTM escalation from ordinary approved-design implementation routes. **SHOULD:** Expand guide examples across all four supported design types and add behavior-level regressions. **NONE:** No new design protocol, classifier key, implementation capability, or invented flag is warranted by the formatting-only history. Supporting contract: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/design.md:12-109`.
