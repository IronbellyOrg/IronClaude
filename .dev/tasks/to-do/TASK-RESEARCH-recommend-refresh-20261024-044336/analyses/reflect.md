# Research: /sc:reflect recommendation refresh

- **Topic type:** Command history and routing-contract comparison
- **Scope:** Six-month history ending 2026-10-24; current reflection, recommendation, guide, plugin, cache and test surfaces
- **Status:** Complete, source-verified research; no implementation or runtime execution
- **Date:** 2026-10-24

## Evidence keys

All paths are absolute.

| Key | File |
|---|---|
| C | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/reflect.md` |
| R | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` |
| G | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` |
| S | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md` |
| P | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/reflect.md` |
| Q | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` |
| H | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py` |
| D | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py` |
| T | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py` |
| U | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py` |

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/reflect.txt`, worker `aefddc94589ec3e48`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-command git patches establish these changes:

- `fd41178b`, 2026-05-08: substantive addition of recommendation re-scrutiny to the earlier Serena-based reflection command.
- `89df2c11`, 2026-05-22: formatting-only blank-line normalization; no semantic delta.
- `021f715c`, 2026-05-27: substantive replacement of the old session/completion reflection surface with pre/post audits, tiered reviewers, blind calibration, evidence validation, deviation classification and promotion.
- `b9724e49` and `80fd3520`, 2026-06-04: exposed verification/onboarding/hierarchy controls and corrected post-mode tasklist wording from required to strongly recommended.
- `3f301ba5`, 2026-06-26: added the reachability-gate rollback flag.
- `156f2829`, 2026-07-01: Tavily tool-name correction.
- `d2cb8377`, 2026-07-05: added the separate detection-contract readiness CLI.
- `3ae238b1`, 2026-09-30, and `782621f4`, 2026-10-01: removed Sequential MCP dependencies/references.
- `3c22b6b4` and `dc9e5609`, 2026-10-16: default remediation changed from task-builder to workflow/implement; subsequent correction adopted managed packages and consumed workflow’s built-in pre-review instead of duplicating it.
- `5c6a7d91`, 2026-10-22: corrected the installed protocol lookup.
- `070399eb`, 2026-10-23: changed readiness wording from “next safe command” to “next command”; no new reflection routing capability.

Evidence: read-only `git log -p` for C, inclusive inventory window.

### Current command contract

[CODE-VERIFIED] Pre-execution mode requires a spec; a tasklist is optional. Post-execution mode requires a diff or task log; tasklist and spec improve context but are not universal prerequisites. New recommendations should use explicit `--mode pre|post`, not resurrect `--type session|completion`. C:23-35,88-99,118-127.

[CODE-VERIFIED] Default depth is `standard`; `quick` confines the audit to Tier 1, while `deep` forces Tier 2. `--tier 2` independently requests the reviewer ensemble. Outputs include a report path, mode, reached tier, calibrated confidence, coverage/deviation results, citation-drop count and promotion verdict. These are verified documentation contracts, not observed execution results. C:98-110,133-146.

[CODE-VERIFIED] Audit-first does not mean entirely mutation-free: post-mode promotion is default-on when its gate passes. `--no-promote` suppresses movement, while report artifacts still get written. Remediation additionally requires `--remediate` and interactive acceptance; the interactive skill builds the corrective artifact but leaves execution to the operator. C:110-116,146; R:13-24.

[CODE-VERIFIED] Remediation follows requested depth, not reviewer escalation: standard/quick use workflow followed by user-run implement; deep uses task-builder followed by user-run task. Workflow’s pre-review is already included. A managed workflow package must never be handed to task. Headless wrapper execution is a distinct contract and must not be substituted for interactive audit-only requests. R:9-24.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The existing guide already routes pre-flight checks to reflect and requires `--no-promote` for post-work confirmation. Preserve both. However, its post row always prints tasklist/spec inputs, whereas the command permits diff-only or task-log-only audits. Its pre row omits spec-only coverage checks. G:321-322 versus C:27-28,92-97.

[CODE-VERIFIED] The guide has no dedicated reflection-remediation or detection-readiness row. Its comparison and general-review rows instead cover adversarial merging, spec critique and multi-model review. These are distinct intents, not substitutes for spec-adherence audits. G:303-325 versus C:73-82,110,144-146.

[CODE-CONTRADICTED] Plugin guidance still says default remediation uses task-builder and task, contradicting the source command’s workflow/implement default. It also retains Sequential MCP prose. P:101,137,152 versus C:110,146. This directly affects recommendation accuracy outside the checkout.

[CODE-VERIFIED] Recommendation matches guide rows before cache dispatch and bypasses both cache paths on a match. Checkout candidates use source precedence; outside a checkout, project copies precede installed copies and plugins. Candidate verification extracts activation handoffs but does not explicitly require proving the delegated protocol is installed. S:41-61,112-135.

[CODE-VERIFIED] Unmatched reflection requests share the classifier’s `adversarial-review` bucket with debate and code review. Dispatch selects a cached row by that key and checks its source bytes, not whether its stored target still fits this request. This creates a concrete possible cross-intent cache-hit failure, not proof that one occurred. Q:63; D:103-136.

[CODE-VERIFIED] Surface hashing covers discovered paths and guide bytes, while per-row validation hashes one selected source file. Editing a delegated reflection reference without changing that source file or guide does not itself change either check. H:63-103; D:116-124.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Extend G section 3.10 and its existing routing table to distinguish pre-coverage, post-adherence, remediation planning and detection readiness. Do not add a second keyword table to recommend. Reuse current mandatory promotion protection and make optional inputs conditional. Grounding: C:23-35,73-82,92-116; G:321-322.

Paste-ready envelopes, retaining unknown user inputs visibly:

- `/sc:reflect --mode pre --spec <spec-path> --tasklist <plan-path>`
- `/sc:reflect --mode pre --spec <spec-path>`
- `/sc:reflect --mode post --diff <baseline-ref-or-diff-path> --no-promote`
- `/sc:reflect --mode post --task-log <execution-log-path> --no-promote`
- `/sc:reflect --mode post --diff <baseline-ref> --tier 2 --remediate --no-promote`
- `superclaude reflect contract-status --repo <owner/repo> --pr <number>`

[UNVERIFIED] **MUST, proposed policy:** For thorough review plus ordinary corrective planning, prefer `--tier 2 --remediate`, not automatically `--depth deep --remediate`: the latter deliberately selects MDTM. Preserve explicitly requested MDTM routing, but do not infer it from file count, multiple sessions, auditability or resume needs. Align G’s broader level rules and S’s fallback rules with the user’s workflow-first direction. Grounding: R:9-24; G:305-308; S:155-157.

[UNVERIFIED] **MUST:** Update P’s remediation description and verify the actual activation dependency before recommending reflect as runnable in a plugin-only installation. Update S’s candidate-verification procedure and its mirrored reference/runbook consistently. Grounding: P:101,137,142-144; S:128-135.

[UNVERIFIED] **SHOULD:** Prevent reflection/debate cache collisions through intent-sensitive validation or cold-path bypass where the existing key loses necessary distinctions. Include consulted activation/ref dependencies in freshness validation. No extra fixed command-keyword mapping is needed. Grounding: Q:63; H:63-103; D:103-136.

### Acceptance/regression scenarios

[UNVERIFIED] Add scenarios proving that:

1. A spec-only coverage request reaches pre-mode without inventing a tasklist.
2. A diff-only or log-only audit preserves `--no-promote` and does not demand an absent spec.
3. A review-only request never gains `--remediate`, implementation or the headless auto-fix wrapper.
4. Ensemble review plus ordinary remediation uses `--tier 2 --remediate`, workflow and implement; deep remediation retains explicit MDTM semantics.
5. Workflow’s existing pre-review is consumed rather than repeated; managed packages never reach task.
6. A cached adversarial-merge answer cannot satisfy a later adherence-audit request.
7. Changing a consulted reflection reference invalidates affected cached guidance.
8. A plugin command whose protocol is unavailable is marked unavailable.
9. Detection readiness invokes the sibling CLI, not normal reflection.

[CODE-VERIFIED] Existing tests pin mandatory post-audit `--no-promote`, and plugin parity checks cover recommend’s tree plus guide. Those assertions do not themselves establish reflect-command parity or behavioral correctness for these new scenarios. T:333-356; U:27-36.

## Gaps

[CODE-VERIFIED] Directory checks and tracked-file queries found no plugin reflection-protocol package at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-reflect-protocol`. Whether a particular installed environment supplies it separately remains unverified.

[CODE-VERIFIED] The recommendation hook is an advisory, fail-open reminder, not mechanical proof of candidate verification. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`:4-13.

[UNVERIFIED] No reflection skill, wrapper, test suite or installed legacy recommend protocol was executed. Runtime reviewer availability, performance and audit completeness are not established by this research.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Broaden reflection routing without converting audit requests into implementation; preserve promotion controls; correct stale plugin remediation guidance; verify activation dependencies; align ordinary remediation with workflow/implement.

[UNVERIFIED] **SHOULD:** Add intent-safe cache handling, dependency freshness and the regression scenarios above.

[UNVERIFIED] **NONE:** No reflection redesign, automatic execution, duplicate keyword table or unsupported workload-capacity claim is needed.
