# Issue 393: retry adviser model selection review

Template: ../362/report-template.md, Findings template (coordinator-required fields).

## Verdict and evidence
**Verdict: still-relevant.** Issue #393 remains open and its acceptance condition is not established by current instructions or the inspected tests. The primary model ladder still activates from four nonempty environment variables, while the same file uses the Agent model parameter and records `GPT spawn path: none verified; family-fallback applies`: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185. This session's Agent schema accepts only opus, sonnet, haiku and fable as model arguments.

There is partial mitigation for adviser B, not a complete model-to-launch mapping for all advisers. No active fix was identified by the permitted PR searches, so this is not classified as in-progress merely because earlier PRs changed the ladder. The last five commits touching retry.md still end at PR #518, commit `167184c6b`; PR #385, merge `4eb75698d9d477ad21b515f05d470ece60497a02`, introduced the relevant exported variable names. The analysis report is /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/393/analyze/analyze-report.md.

## Real current state
- **Present:** The retry process obtains two read-only advisers before reverting failed work and saves their answers. Its primary ladder now starts at `T2bModel01`, not the original issue's `T3Model01`; the other rungs are `T2Model02`, `T1Model02` and `T1Model01`. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:71,162-172.
- **Partial:** Adviser B falls back to the strongest reachable model and records the reason when the other family cannot be reached. That clause neither supplies a universal accepted alias mapping nor verifies adviser A, critique and escalation-2 launch choices: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:166-185. Do not turn this into a claim that every run fails or that the entire ladder is protected by B's fallback.
- **Alias routing is not the original issue's old coincidence:** the launcher currently exports access-aware tier aliases with `[1m]` suffixes, rather than pinning opus directly to a fixed underlying model: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/ccsession:1110-1117. PR #391 merged this tier-routing mechanism; merge commit `943246042b04f576831888f946660ce8673335c1`.
- **Checked-in tests are not the requested launch proof:** the policy check pins variable spellings; the archive check accepts saved rung tokens; the family test uses local reference dictionaries and explicitly pins the absence of a verified GPT spawn path. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_model_alias_policy.py:217-228; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_workflow_archive.py:798-830; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_implement_adviser_family.py:14-48,58-85. No test suite or live adviser run was executed in this read-only analysis.
- **Mirrored instructions retain the problem:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185 carries the same selection and fallback rules. The adviser agent has no fixed model to resolve the mismatch: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/implement-retry-adviser.md:1-6.

## Concrete next steps
1. Keep the issue open. Prefer an explicit supported-alias selection rule for every adviser role, including critique and the second escalation, rather than restoring obsolete variable spellings to disable the primary ladder accidentally.
2. Update the canonical retry instructions and plugin mirror. Separate executor-rung recording from the actual adviser launch alias. Check the ledger and its tests, preserving existing saved rung tokens unless a migration is explicitly required. The current ledger field means the executor's rung: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/ledger.md:94-112.
3. Replace name-presence-only acceptance coverage with checks for all primary variables set, partial/unset variables, unavailable other-family models, adviser A/B, critique and escalation 2. Assert every emitted Agent model argument belongs to the accepted alias set and fallback records name what was actually selected.
4. Run a controlled adviser launch before claiming actual named-model or cross-family selection. An alias can be valid while the gateway routes it to a different underlying model; do not promise family fidelity without separate evidence.

## Complexity and size
**Complexity: medium. Size: S.** The smallest fix is bounded instruction and regression-test work across the canonical retry policy, its plugin mirror and supporting ledger/policy tests, but every adviser role and saved-ledger compatibility must agree; it does not require a new dispatcher. Building a cross-provider launch system would be a larger, separate scope.

## Priority
**Priority: P2.** The mismatch weakens recovery after implementation review failures and can prevent the intended stronger or independent advice, but it is on an escalation path, adviser B has a fallback, and no outage, data-loss event or universal run failure was verified. Correct it before relying on retry model diversity or evaluating that diversity in #572; it does not block the entire #571 cleanup release.

## Dependencies
GitHub currently records no blocked-by or blocking issues for #393 (both counts zero). No hard prerequisite was identified for the bounded alias-policy fix. The model-alias issue #384 and tier-layout issue #488 are closed predecessors, not open blockers. Coordinate edits with #572's evaluation of the retry adviser and any #571 work touching the implementation skill; those are ordering/overlap considerations, not verified whole-issue blocking links.

## Related issues
- #384: model aliases for primitives, CLOSED; original parent context for PRs #385 and #391.
- #488: tier-layout changes, CLOSED; PR #518 moved retry rung 0 to `T2bModel01`.
- #572: evaluate agents, OPEN; its body explicitly lists `implement-retry-adviser`, so model-selection assumptions matter to that evaluation.
- #571: cleanup/release plan, OPEN; body keeps the implementation workflow rather than removing this problem. Its older release-plan statements are not treated as current code facts.
- #392: tier failover, mentioned in PR #385's review discussion as a neighboring helper-model concern; its current scope/status were not independently read, so UNVERIFIED.

## Related PRs
- [#385](https://github.com/IronbellyOrg/IronClaude/pull/385): MERGED 2026-11-05; merge `4eb75698d9d477ad21b515f05d470ece60497a02`. The body describes switching to exported variable names. Its review discussion explicitly files #393 for the resulting adviser-launch mismatch.
- [#391](https://github.com/IronbellyOrg/IronClaude/pull/391): MERGED 2026-11-05; merge `943246042b04f576831888f946660ce8673335c1`. Makes nickname routing access-aware in tier mode. Its probe notes explicitly say the Agent-call model parameter was not exercised, so it is not a resolution of #393.
- [#518](https://github.com/IronbellyOrg/IronClaude/pull/518): MERGED 2026-11-12; merge `167184c6ba449ab49b7f2af1dc9f4c9080006bd3`. Changes rung 0 and tests, but retains the missing-GPT-path statement. It does not close #393.
- No active correction was identified by `gh pr list` searches for `393` (all states) and `retry adviser` (open). Results #622 and #152 from the numeric search are not treated as fixes: #622 removes an unrelated command, and #152 predates this issue and concerns swarm. Search coverage is not proof that no PR exists under another title.

## Verification limits and negative evidence
- Read the live issue body, its one returned comment, dates, formal dependency fields, closing-PR references and all three PRs mentioned by the issue/comment (#385, #391, #518), including their bodies and returned comments.
- Available chronology: #393 created 2026-11-05T16:37:43Z; its status-review comment and last update are 2026-11-17T07:12:07Z; it remains open with no closing-PR references. **Full GitHub event timeline: UNVERIFIED.** The permitted `gh issue view --json timelineItems` failed with `Unknown JSON field: timelineItems`; the allowlist does not permit API/browser substitutes. Issue-view metadata and PR merge dates supply only a partial chronology.
- **Runtime results: UNVERIFIED.** No live advisers, proxy requests or tests were run. Static instruction review is enough to show the missing explicit mapping, not to prove how a particular model improvises around it. Workspace defaults and actual current provider routing were not inspected.
- Negative evidence: the narrow source search found no retired `T*_Model` spelling; graph discovery found no files because Markdown is not indexed; the inspected tests validate names/records/local family rules rather than actual adviser launches. The first Augment request used its nonexistent default main branch; explicit master retry succeeded.
- No source edits, local commits, staging or outward GitHub actions were taken. Files were written only in this task's report directory. Initial population edits were refused by the freshness hook until the report stubs were Read; subsequent edits succeeded.
- Evidence is from the current Issuecleanup checkout, not an unperformed fresh fetch of origin/master. Recent local history for retry.md still ends at #518. The final report recommendation is advisory; only the coordinator/owner may change issue state.
