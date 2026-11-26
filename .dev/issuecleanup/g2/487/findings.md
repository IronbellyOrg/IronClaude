# Issue #487 review: Re-useable Spec-Task Eval Framework

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/487 (OPEN, opened 2026-11-10 by ironbelly, no labels)
- Reviewed: 2026-11-24, against worktree ironbelly/Issuecleanup (HEAD a7ae3dd30)
- Analyze report: .dev/issuecleanup/g2/487/analyze/analyze-report.md

## Verdict

still-relevant

The specification is written and merged, and none of the framework code it asks for exists. Every structural claim the issue makes about the existing eval harness is still true in the code today, so the issue is neither done nor overtaken.

## Evidence

- Spec merged by PR #500 (merge commit ec259f1b718ccdb9f08bba0237bfa47b2b7601a2, 2026-11-11), file `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md` (641 lines, Parts A-E present; the Part E port decision at line 425).
- The comment's cited commit 2813b945 is NOT in this branch's history (it lives on the unmerged branch `346Claude-ab-experiment-artifacts`, remote tip 0150d187); the merged copy came in through the squash/merge of PR #500.
- No `src/superclaude/cli/lab/` and no `lab` module anywhere under `src/superclaude` (checked 2026-11-24). `git log origin/master` since the 2026-11-17 status review shows no commits touching `src/superclaude/cli/eval` or a lab path.
- Production executor is still the documented null stub: `_NullLifecycleExecutor` returns a canned exit code 0 (`src/superclaude/cli/eval/commands.py:1357`, factory at `commands.py:1401`).
- Concurrency still clamped at 15: `RunOrchestrator.MAX_PARALLEL = 15` (`src/superclaude/cli/eval/orchestrator.py:140`, clamp at `orchestrator.py:198`).
- Exit codes still a fixed four-value table: 0, 1, 2, 3 (`src/superclaude/cli/eval/exit_codes.py:21`).
- Eval id regex still closed: `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (`src/superclaude/cli/eval/artifact_layout.py:108`).
- No pull request mentions 487 or the framework (searched PR titles and bodies); nothing is in progress.

## Real current state

- The design is decided on paper: Part E selects a sibling `superclaude lab` package with its own schemas, run store and exit-code mapping, reusing cliEval's isolation, containment, scratch, cancellation, disk-budget and reporting utilities. Its process layer uses `ClaudeProcess(cwd=...)` directly, not `ClaudeProcessAdapter`, whose process-wide `os.chdir` can race under parallel launches (`src/superclaude/cli/eval/claude_process.py:335-365`). Part E also requires extracting the companion's `RestrictedProcess` hardening (stdin-timeout fix, restricted reviewer profile, loopback ingress recording and hash-pinned config gate) into a shared module (`.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:621-624`); that extraction is a build requirement, not verified completed work.
- Reusable pieces that are real, not stubs: `HomeIsolation` (`src/superclaude/cli/eval/isolation.py:363`), direct `ClaudeProcess` with child-specific cwd (`src/superclaude/cli/pipeline/process.py:103,215-218`), `EvalRunner` (`runner.py:712`), `RetryOncePolicy` (`retry.py:93`, covers MCP-flaky specs only, so the spec's claim that HTTP 429 backoff is new code still holds).
- The 2026-11-17 status comment's finding "no framework code is on master" is still accurate.
- Not started. No branch, no module, no partial implementation, so there is no in-progress work to resume.

## Concrete next steps

1. The owner decides whether the headless-Claude backlog rule (the reason #560, #561 and #562 sit on backlog) also covers this framework. The 2026-11-17 review flagged this and it is still unanswered. UNVERIFIED: the text of that backlog rule was not read for this review.
2. If the rule does not cover it, plan the build with `/sc:workflow` from `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md`, starting at P0: task/arm/slots/experiment schemas, policy validation and frozen assets including the audit command/rules, S1 task and defect ledger v1. Require validation and the Fable-ban test before P1 (the engine), then retain P1-P7 and each phase's acceptance tests, including the B16 golden replays (`SPEC-AND-CONTEXT.md:388-405`).

## Complexity

complex. A new top-level command group with a scheduler, three backends, a policy engine, instrumentation, blind scoring, statistics and a ledger factory, specified across 641 lines.

## Size

XL. Nine scoped subsystems (declarative designs, engine, policy, instrumentation, scoring, statistics, automation, spec library, template experiments), and the spec itself estimates 35-40% ported plus 25-30% new.

## Priority

P2. It is the prerequisite for repeating the #346 review-loop experiments cheaply, but it blocks no production code path, and it cannot start until the owner answers the backlog-rule question.

## Dependencies

- Needs: an owner decision on the headless-Claude backlog rule before any build starts (related: #560, #561, #562). No code dependency.
- Blocks: #489's framework-policy and configurable-panel portion. Its live body explicitly requires #346/#487 framework work to be merged and #488 deployed; its owner-decision comment requires a configurable tier list and optional Tier 4 membership switch with a membership/lane test (https://github.com/IronbellyOrg/IronClaude/issues/489#issuecomment-6774682023). This is a partial implementation dependency, not a verified formal GitHub blocked-by link: harness/spec updates can be prepared before the entire framework is finished, as #489's 2026-11-24 review also states.

## Related issues

- #346 (CLOSED): the origin experiments whose hand-run rig this framework would replace.
- #489 (OPEN): "Follow-up to #488: update the eval-framework panel tiers and live alias map for Tier 2b". Partially depends on #487 for executable framework policy and panel configuration. Settled owner requirements: default panel `t1b, t2, t2b, t3`; Tier 4 optional and off by default; tier list and Tier 4 switch kept as configuration; Tier 2b mock Sonnet/live GPT-6.1 Terra; Tier 3 live GLM 5.3; test that toggling Tier 4 changes only panel membership and lane labels (live owner comment linked above; `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:636-640`). These are recorded choices, not newly run live-model probes; current deployed alias resolution is UNVERIFIED here.
- #520 (OPEN) Centralized Review Panel, #531 (OPEN) Shadow Run Module, #549 (OPEN) Review-Panel Merged Efforts, #550 (OPEN) Record, fold in and re-test proven tasklist experiment designs, #552 (OPEN) Issues being classified as blockers too egregiously: each cross-referenced #487 between 2026-11-12 and 2026-11-15. Only titles were read; why each references #487 is UNVERIFIED.
- #290 (OPEN) and #429 (OPEN): cross-referenced #487 on 2026-11-17 and 2026-11-23. The connection is UNVERIFIED from titles alone.
- #560, #561, #562 (all OPEN): eval-run bugs named by the 2026-11-17 status review as the backlog context.

## Related PRs

- #500 (MERGED, 2026-11-11): brought the experiment artifacts and the specification into master. It does not implement the framework.
- No open or closed PR implements `superclaude lab` or references #487.
