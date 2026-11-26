## Verdict
**still-relevant.** Issue #725, requiring peer-project read-only questions before interrupting a human, is OPEN and had no comments at the live read on 2026-11-24. Its body names no PR. At checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, the complete coordinator section in `src/superclaude/core/HOW-WE-WORK.md:352-362` contains no peer-first rule or its safety limits. Full-file searches of `src/superclaude/core/WORKER-CONTRACT.md` for peer/cross-project/question wording found no matches; section 4 begins with worker-management duties at `:69-92`, not peer contact. The requested question template and receiving-side refusal are missing there. Existing restrictions on outward actions are not delivery of these requirements.

This is not classified in-progress: no issue comment or inspected source establishes implementation underway. Recent local history changes coordinator definitions and approval wording (PR #736, commit `784254002`; PR #735, commit `6fce3651b`; PR #724, commit `f7b6314e4`), but the current rule surfaces still lack the requested feature. Those PR associations come from local commit subjects; their live PR bodies and review status are UNVERIFIED. Static analysis is recorded in `.dev/issuecleanup/g5/725/analyze/analyze-report.md`.

## Complexity and size
**Complexity: medium. Size: M.** The implementation is bounded rules, distribution-copy maintenance and regression tests, but coordinator-launch coverage needs a real builder and owning tests identified across the repository boundary; it is not a one-file wording fix. Estimate assumes no new coordinator subsystem or enforcement hook, both outside the requested core change.

## Priority
**P2.** Missing mandatory information routing causes avoidable human interruptions and leaves the proposed peer-contact boundaries unspecified, but the inspected issue and source establish no outage, data loss or hard blocker to the existing worker/coordinator flow.

## Concrete next steps
The feature is still relevant, not verified partly implemented. The following are concrete implementation steps rather than a claim of current progress:

1. Locate and record every actual coordinator standing-launch builder and its owning output tests. Search of `src/superclaude/commands`, `src/superclaude/skills` and `src/superclaude/cli` found none; `src/superclaude/cli/issue_pipeline/brief.py:1-9,52-80` produces worker Task specs and cannot satisfy coordinator-launch acceptance. The Coder handoff documents standing-prompt ownership at `docs/designs/issue-watcher-zero-setup-coder-handoff.md:11-13,51-53`; actual builder location and output are UNVERIFIED and require authorized follow-up, not invention of a new subsystem.
2. Add all six MUST/MUST NOT rules to the guide's existing Orca section and to the shared coordinator contract, including the reusable question, receiving-side refusal, reporting of question/answer and unverified claims, the three allowed human-fallback reasons, and the unchanged cross-project supervision boundary. Keep `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` aligned. Keep installed/project lookup references valid and do not alter unrelated routing-table content.
3. Extend phrase and negative-mutation checks (`tests/skills/test_worker_contract.py:907-909,1073-1080`), guide checks and actual launch-output tests. Pin MUST-to-may weakening and removal of each safety limit. Preserve the guide ASCII check at `tests/core/test_how_we_work_routing_table.py:329-334`.
4. Record the four unresolved research questions: reliable peer discovery/naming, wake-up behavior, held messages across permission modes, and possible hook enforcement. Do not turn any into an operational guarantee or fixed waiting period. A search of hooks for peer/cross-project/read-only-question text found no match; that does not prove absence of general guard coverage.
5. During the later authorized implementation, run the targeted checks, source-to-dev synchronization and full regression gates specified in the issue. None ran in this review because the brief forbids UV and writes outside this report directory. Shipping and GitHub changes remain with the coordinator after the owner's go.

## Dependencies
- No verified hard dependency on another IronClaude issue, and no verified issue that #725 blocks. Shared-rule and test work can proceed without the broader coordinator or watcher build.
- **Coder #516: launch-surface coordination dependency, not a verified prerequisite to all of #725.** The local handoff assigns the coordinator session and standing prompt to that issue (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:11-13,51-53`). Its actual implementation, present status and whether it already supplies the necessary builder are UNVERIFIED; this task permits GitHub reads only on IronbellyOrg/IronClaude.
- IronClaude #716 and #717 are related scopes, not established hard dependencies. Do not wait for their entire feature sets or expand #725 into them.

## Related issues
- #716 (OPEN at read): next-release coordinator features mined from issue 655. Broader coordinator delivery, not a replacement for the six peer-contact rules.
- #717 (OPEN at read): next-release issue-watcher features. Related operating context, not proof of coordinator prompt coverage.
- #339 (OPEN at read): orchestrator/session-management proposal. `docs/designs/orchestrator-mode.md:1-13` concerns its Phase 1 sweep work, not implementation of this peer-first rule.
- #444 (CLOSED at read): evaluation of sub-orchestrator/coordinator mode. Its comments include older OPEN-status claims; the current state returned by GitHub is CLOSED. Do not copy those historical status claims into the present review.
- Coder #515 (cron) and #516 (coordinator launch/naming): mentioned by #725 and the local Coder handoff. Their live contents and status were not read because the brief allows only the IronClaude repository. UNVERIFIED; they are not declared duplicates.

Read #725 and its empty comments, plus the related IronClaude issue reads above. A shared GitHub API-rate warning appeared during the related reads; no further main-session GitHub reads were made. No state here should be inferred for an issue whose live contents were not read.

## Related PRs
- No PR is named or linked in #725's issue body, and it had no comments. Repository PR searches for `725` and for `peer` plus `coordinator` did not identify an implementing PR; search completeness and the full open-PR inventory are UNVERIFIED. This is not a claim that no PR exists.
- #736 (`784254002`), #735 (`6fce3651b`) and #724 (`f7b6314e4`): adjacent coordinator-definition, per-project ownership and owner-approval changes identified in local source history. None demonstrates peer-first delivery in the current guide/contract. Live PR bodies are UNVERIFIED after the shared rate warning.
- PR #508, returned by the peer/coordinator search, is the merged positive unattended-default change (commit `146be6fc34276c99d4bff89e682472274f71ce8e`), not #725 implementation. PR #628, returned by the numeric search, is an unrelated ccsession performance change and is excluded as a false match.

Required deliverables are findings.md and qa.md in this report directory. Analysis and its return contract/handoff are supporting files. No source, tests, settings, issue, PR, branch or index was modified; only report-directory files were written.
