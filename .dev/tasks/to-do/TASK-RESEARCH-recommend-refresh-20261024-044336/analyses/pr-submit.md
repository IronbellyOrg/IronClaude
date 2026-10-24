# Research: /sc:pr-submit recommendation coverage

- **Topic type:** Command history and routing-contract research
- **Scope:** Changes from 2026-04-24 through 2026-10-24; current recommendation surfaces and delegated protocol
- **Status:** Research complete; no implementation or runtime execution
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/pr-submit.txt`, worker `a5e340ee055120146`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Evidence map

All citations below use these absolute source paths and their live line numbers.

| ID | Source |
|---|---|
| C | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/pr-submit.md` |
| P | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` |
| G | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` |
| R | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md` |
| T | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py` |
| M | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| H | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh` |
| K | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` |

### Historical changes

[CODE-VERIFIED] Read-only history and actual command patches establish substantive evolution, not merely formatting:

- `2c5357c8`, 2026-06-12: introduced PR creation, four autonomy ceilings, bounded remediation, and run-log resume.
- `0f9c8d36`, 2026-06-16: removed repository-specific targeting and fixed resume paths; selected the repository’s actual default base branch.
- `d12cad1d`, 2026-06-17, and `ef30032d`, 2026-06-19: changed the default from 0 to 1, then 2; reduced the default wait from 1800 to 600 seconds.
- `d2cb8377`, 2026-07-05: expanded locked-detection-contract readiness instructions. `4beaa7f1`, 2026-09-20, subsequently removed that mandatory setup gate in favor of shipped identities and an optional local override.
- `7b2fd195`, 2026-09-24: added CI waiting and remediation. `d5200729`, `cd031eda`, and `1d2223ad`, 2026-09-25: clarified attended polling, surfaced CI preflight requirements, and distinguished silent Augment from clean review.
- `3ae238b1`, 2026-09-30: removed Sequential from MCP metadata; this is a dependency-metadata change, not a new routing capability.
- `2165ae25`, 2026-10-22, and `070399eb`, 2026-10-23: established default monitor 3.
- `2916e062`, `87518f8f`, and `3d171809`, 2026-10-23: added explicit `--pr`, made origin resolution primary, removed dead hook references, bound monitoring to the PR head, and restricted pushes to the cycle’s single fix commit.

These patches concern C; current resulting contracts are visible at C:25-85.

### Current command contract

[CODE-VERIFIED] The command opens a PR or attaches using `--pr <N>`. Monitor 0 performs creation only; 1 polls and proposes without edits; 2 fixes and validates locally without committing, pushing, or replying; 3 performs the full bounded remediation loop. Default monitor is 3, default maximum rounds is 2 with a hard cap of 5, polling defaults to 30 seconds with that minimum, timeout defaults to 600 seconds, and silence timeout defaults to 300 seconds. Base defaults to the resolved repository’s default branch. C:25-56; P:189-199.

[CODE-VERIFIED] Recommendations must disclose consequential behavior: monitor 3 can commit fixes, push, reply, resolve, and retrigger review. The protocol preserves operator-pending files, rejects wrong-head and unexpected push-range situations, and forbids force-pushing. At monitor 1 or higher, checkout/head agreement and CI-classifier prerequisites apply. C:28-30,83-85; P:190-199.

[CODE-VERIFIED] Output includes PR URL, status, counters, applied-edit information, and authoritative JSONL run-log path. `--resume` reconstructs state. Polling is attended and session-bound, not a daemon; silence remains `terminal_augment_no_response`, even when subsequent CI checks pass. C:56-58,79-85; P:155-172,225.

[CODE-VERIFIED] Activation is `Skill sc:pr-submit-protocol`. Recommendation output should hand off to the command, not reproduce its state machine or manually orchestrate troubleshoot, pushes, and thread handling. The protocol owns diagnosis dispatch and edit application. C:68-79; P:192-196; R:177-184.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide already captures the important default accurately: section 3.11 recommends monitor 3, explains automatic remediation pushes, permits monitor 2 for inspection before pushing, and recommends monitor 0 when the Augment App is absent or uncertain. The ordinary full review-and-submit route should therefore remain available, not be replaced with generic implementation planning. G:196-205,229.

[CODE-CONTRADICTED] The machine-readable `review-pr` row makes `--monitor 3` unconditional while its own notes prescribe monitor 0 without the App. The recommendation skill requires every mandatory flag and every matched-row step. The contract thus requires incompatible output in the no-App case; merely verifying that `--monitor` exists cannot resolve the conflicting value. Its rigid route can also escalate an explicit local-only request. G:323; R:150,236-239. This is a verified documentation-contract conflict, not a demonstrated runtime failure.

[CODE-VERIFIED] Existing-PR attachment and PR-monitor recovery are missing from the guide’s routing coverage. `review-pr` names creation inputs only; generic `resume` offers task execution or workflow-plan execution, although the command explicitly provides `--pr` and `--resume`. A PR-monitor interruption is not evidence that an MDTM task must be created. G:323-324; C:53-56.

[CODE-VERIFIED] Tests pin unconditional monitor 3 rather than conditional autonomy selection. Plugin guide rows carry the same creation and resume limitations. Fixing only recommendation prose would leave governing guide data, tests, and plugin recommendations inconsistent. T:333-356; M:323-324.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed specification:** Update G section 3.11, section 5, and `review-pr`, together with the corresponding M sections. Keep monitor 3 as the normal full-loop default, but make no-App/open-only and explicit lower-autonomy choices unambiguous, mutually exclusive branches. Never emit two monitor values. Respect stronger project policies; report a policy conflict rather than silently escalating authority. Grounded example for an expressly creation-only request:

`/sc:pr-submit --monitor 0 --head <branch> --title "<title>" --body "<body>"`

Supported inputs: C:35,46-54.

[UNVERIFIED] **MUST, proposed specification:** Extend the existing canonical guide, not a second keyword table, to distinguish the full pre-PR review sequence from attaching to an existing PR. Preserve already-completed prerequisites instead of forcing PR recreation or unrelated planning. For a user requesting proposals without edits:

`/sc:pr-submit --monitor 1 --pr 42`

For local fixes without publication:

`/sc:pr-submit --monitor 2 --pr 42`

Supported contracts: C:36-37,53; P:189,194-195.

[UNVERIFIED] **SHOULD, proposed specification:** Extend G section 3.12 and its resume coverage to recognize a supplied PR-monitor run log and recommend `/sc:pr-submit --resume <absolute-run-log-path>`, preserving the verified requested ceiling rather than treating “resume” as synonymous with `/task`. Leave unknown paths as placeholders. C:39,56; R:238.

[UNVERIFIED] **MUST, proposed specification:** Update R’s matched-row and mandatory-flag rules to honor documented conditional branches and explicit mutation ceilings. Update T so it verifies monitor 3 for the ordinary full-loop case, plus lower-ceiling exceptions, rather than requiring 3 universally. No PR-submit implementation changes are required by these routing findings.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed contract-level tests and evaluation cases:

1. Full review-and-submit, App available: preserve review order and explicit monitor 3; disclose automated remediation publication.
2. Open only or App absent: emit exactly monitor 0, without claiming review or CI remediation.
3. Existing PR 42, no edits: emit monitor 1 with `--pr 42`; do not recreate the PR.
4. Existing PR, inspect fixes first: emit monitor 2, never promise commit/push/reply.
5. Supplied monitor JSONL: recommend command-specific resume, not `/task`, `/sc:implement`, or task-builder.
6. Head mismatch: preserve the command’s halt boundary; never recommend force-push or closing a correctly targeted PR merely because its head differs.
7. Plugin-only installation lacking the command: mark it not installed instead of presenting it as runnable.

These expected outcomes derive from C:28-56,85; P:189-199; R:135,150.

## Gaps

[CODE-VERIFIED] Negative searches found no command-specific PR-submit entries in recommendation refs or classifier vocabulary. K:50-68 permits unknown requests to fall through to discovery. Matched guide workflows already bypass cache, so a new fixed keyword table or classifier category is not justified merely to address this command.

[CODE-VERIFIED] Tracked-file inspection found recommendation plugin assets but no plugin PR-submit command/protocol. Missing-command degradation must remain explicit. The globally installed legacy protocol exists at `/config/.claude/skills/sc-recommend-protocol/SKILL.md`, but no corresponding tracked source directory exists; it is not the current recommend command’s activation target.

[CODE-VERIFIED] H:4-13 explicitly describes a fail-open reminder, not mechanical enforcement. Recommendation assurance must not rely on a claim that this hook prevents incorrect routing.

[UNVERIFIED] No live PR, bot review, cache execution, or remediation test was run. Actual model behavior under conflicting guide instructions remains unmeasured.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Resolve monitor-value conflicts, preserve explicit autonomy limits, cover existing PR attachment, and align guide, recommendation contract, plugin guide, and regression expectations.

[UNVERIFIED] **SHOULD:** Add PR-monitor-specific resume coverage and concise prerequisite/safety disclosures.

[UNVERIFIED] **NONE:** No new keyword routing table, mandatory detection-lock setup, daemon promise, or PR implementation expansion. The requested preference for workflow plus implement governs general planned implementation; it should not displace this dedicated PR lifecycle command.
