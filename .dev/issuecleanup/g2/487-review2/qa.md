VERDICT: PASS
# Independent evidence review: issue 487, review 2

Template: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/468/report-template.md, Review skeleton. First-line binary verdict follows the task's explicit required format.

## Verdict
PASS, with no blocking defects. The revised findings correctly restore the specified process manager and hardening requirement, the prerequisite schema/policy/frozen-assets phase and its exit checks, and the framework-dependent portion of issue #489 with its settled panel configuration. The integrated framework remains unimplemented in the searched checkout, so the still-relevant verdict and gated next-step plan remain supported. Previously recorded non-blocking observations remain notes, not reasons for another fix cycle. Review execution succeeded; this verdict does not resolve the owner's backlog decision or authorize implementation.

## Scope checked
Independent review on 2026-11-24 at checkout HEAD a7ae3dd30fcf88aaab655c37e94e58e121c2d863. Read the live issue #487 body and both comments, both submitted reports, the governing specification's phased plan/acceptance/process-layer decision and panel appendix, current executor/concurrency/exit-code/id/retry implementation, live issue #489 and its owner decisions, and PR #500's merge record. The prior review was read to identify previously blocking rows; revision notes were deliberately not used as evidence. All judgments below come from current source or live read-only GitHub reads, not the reviser's assertions.

Initial source checks confirm the continuing null executor, 15-worker clamp, four exit codes and strict identifier expression. These support the continuing relevance of the framework issue, not a claim that command nesting alone imposes those component restrictions. The codegraph inventory confirms 39 indexed files (24 Python, 15 YAML) and the quoted module symbol counts; it is not a count of every physical file.

### Current-source evidence for the core state

| Claim checked | Evidence and result |
|---|---|
| Default executor is still a stub | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1357-1405: spawn/inject do nothing, observe returns exit 0 with empty streams, and the factory returns that executor. Confirmed. |
| Concurrency maximum remains 15 | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/orchestrator.py:140-142,194-198: default 8, maximum 15, clamped by min. Confirmed. |
| Exactly four canonical exit codes | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/exit_codes.py:21-24: 0, 1, 2, 3. Confirmed. |
| Strict manifest identifiers | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/artifact_layout.py:96-111: strict uppercase-leading manifest expression at line 108, distinct from the more permissive path-safety expression. Confirmed. |
| Lab framework absent from the searched checkout | Glob of lab-named paths under the package found only an unrelated labels document; a source search for the command, module registration and lab group returned no matches. This supports no integrated lab package in this checkout, not absence on every unexamined branch. |
| Specification merged, not implemented by that merge | Live PR #500 is MERGED on 2026-11-11 as ec259f1b718ccdb9f08bba0237bfa47b2b7601a2; its file list adds the spec and experiment artifacts. Local specification history attributes the file to that merge. |
| Original comment's commit ancestry | Local ancestry query for 2813b945 against HEAD was negative; the containing remote-tracking branch is origin/346Claude-ab-experiment-artifacts with tip 0150d187f447352b441a2d475b13402205ca74aa. These are local-ref observations, not a refreshed remote inventory. |

### Reuse and process verification

- /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/claude_process.py:335-365 confirms the process-wide directory change and documented thread race. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/pipeline/process.py:215-218 instead supplies the directory only to the new child. The revised process recommendation matches the real distinction.
- /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/isolation.py:363-409 implements the real isolation record and validates identifiers during construction. Its existence is not proof of unrestricted reuse with the new framework's identifiers; the submitted findings do not claim a completed integration.
- /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/retry.py:118-142 confirms a single extra attempt gated by the MCP-flaky tag and outcome, not HTTP 429 status or timed backoff. This supports the reported limited reuse, not a general absence of every HTTP retry elsewhere.
- The runner lifecycle, warning gate, command clamp and loader import were also read directly. No process or test was executed to turn these static checks into a runtime claim.

## Blocking findings
None. The three previously blocking defects are corrected in substance, verified independently as follows:

1. **Process choice and required hardening:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/487/findings.md:26-27 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/487/analyze/analyze-report.md:35 now select the direct child-process manager, reject the parent-directory-changing adapter and preserve extraction of the companion's hardening as required future work. This matches /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:621-624,631. The current adapter still changes the parent directory, while the direct manager passes a child-specific directory to subprocess creation (source checks recorded below). The next build planner is no longer directed to the rejected adapter, and the safety requirement has not been dropped.
2. **Prerequisite phase and acceptance:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/487/findings.md:34 now starts with schemas, policy validation and frozen assets, including validation and the forbidden-model test before the engine. It retains the subsequent phases and golden replay checks. This agrees with /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:376-405, especially line 398. No prerequisite phase or named acceptance test is omitted from the next-step instruction.
3. **Partial downstream dependency and settled configuration:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/487/findings.md:51,56 now records the framework-dependent policy/panel portion of issue #489, without falsely treating all preparatory work as blocked. Its default panel, optional/off Tier 4, mock/live choices and membership/lane test match the live owner-decision comment at https://github.com/IronbellyOrg/IronClaude/issues/489#issuecomment-6774682023 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:636-640. The live 2026-11-24 issue comment independently supports the partial dependency. No formal GitHub dependency link or fresh live-model probe is claimed.

No new blocking defect was found in the still-relevant verdict, broad effort estimates, proposed priority or required deliverables. This is a review of the findings, not acceptance that the framework is built or authorization to start it.

## Follow-up candidates and notes
### Estimates and disposition

- **Still-relevant:** supported by the existing specification, absent integrated lab command/package in this checkout and still-unwired production executor. The live issue's acceptance requires an integrated scheduler, policy, scoring/replay, accounting and automation, not merely a merged design document. No evidence read establishes that acceptance is complete.
- **Complex / XL:** defensible broad reviewer estimates, not verified GitHub project fields or measured duration. The live issue contains nine scope areas, multiple backends and explicit integration/acceptance requirements. The quoted 35-40% experiment port and 25-30% new-code shares are rough judgments in the specification, not measured productivity. They do not establish a precise completion date.
- **P2:** a reasonable recommendation for an experiment/review tool rather than a production outage. The report correctly retains the existing owner gate instead of treating this review as permission to build. No owner-set priority field was independently established.
- **Completeness:** both required reviewed inputs exist and supply the verdict, current state, next steps, effort/priority proposals, dependencies and related work. The revised next steps point to the complete specification and retain all phased acceptance tests. A short issue-cleanup finding need not duplicate every specification requirement to be complete.

### Previously recorded non-blocking observations, retained without a new fix request

The first review already recorded the false no-recent-eval-change statement, overly broad claims of no branch/in-progress work, command-nesting inheritance overstatement, graph-inventory/count limitations and citation precision. These do not become new blockers in review 2 and do not trigger another revision cycle. The current independently checked runtime and specification evidence, not those claims, supports this PASS. In particular, neither a no-match PR search nor a missing local lab directory proves global absence of implementation work; that global claim remains UNVERIFIED. No new medium follow-up candidate was identified.

### Other claim checks and bounded uncertainty

- Live issue listing confirms #346 CLOSED and #489, #520, #531, #549, #550, #552, #290, #429, #560, #561 and #562 OPEN, with titles matching the submitted report. Exact event-timeline cross-reference dates and the detailed relationships beyond #489 are UNVERIFIED. The findings already flag their unexplored relationships.
- PR searches for the quoted issue reference and lab command returned no matches; the Spec-Task search returned unrelated merged PR #76, which was rejected as evidence. These results support only the searched scope, not the absolute no-PR/no-branch claims.
- The backlog-rule text itself and its applicability to this framework are UNVERIFIED in this review. The live #487 status comment explicitly leaves that applicability unresolved, so preserving the owner decision is accurate. No model alias was probed; current deployed model resolution is UNVERIFIED.
- Graph-dependent totals (28/9/9), the six-module exit-code consumer count and the earlier analysis run's exact timestamp/provenance are UNVERIFIED here. The current graph inventory and symbol counts were checked, and a direct manifest read confirms a closed root object while its defaults object permits extra fields. None of these ancillary metrics is an acceptance check for the reviewed next-step plan.

## Verification limits and negative evidence
- Scope was evidence review only. No submitted findings, analysis, implementation, test, fixture, configuration, export or caller was changed. Only the three assigned review-output files were written inside this task's report directory. No staging, commit, fetch, push, GitHub post or issue/PR edit was performed.
- All GitHub reads used only issue view/list and PR view/list with the fork named explicitly. Issue #487 and both comments were read in full, including a final refresh; its creation date, author, OPEN state and empty labels match the findings. Related issue #489's body and all returned comments were read. No GitHub event timeline was available through these reads, so cross-reference event dates remain UNVERIFIED.
- No uv, pip, Python, test runner, install, codegraph initialization, external model run or environment creation was run. The prohibition on writes outside the assigned report directory was preserved. Runtime correctness, all-branch absence, deployed alias resolution and the backlog rule's applicability were not established by these static checks.
- Read-only codegraph status reported zero changed files; the graph was used for locating code and checking indexed inventory/symbol counts. Source content was read directly before authoring the cited claims. The prior report's graph timestamp is not evidence of current freshness.
- Negative searches: lab-named package paths and lab-command/registration source search found no implementation; quoted #487 and lab-command PR searches returned empty arrays; the framework-title PR search found unrelated #76. These are bounded negative evidence, not proof of global absence. Local ancestry inspection did not find the original comment's commit in HEAD; no remote refs were refreshed.
- Tool recovery: the first report Edit was rejected by the freshness hook because a new Write had not registered as a Read. A tracked Read was made and the same intended Edit then succeeded. No bypass or alternative editing mechanism was used.
- No coordinator follow-up required acknowledgment during the completed checks. No helper worker was started. The mandatory return contract and short handoff accompany this report; the coordinator must read the files before acting on this verdict.
