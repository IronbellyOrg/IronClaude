# Issue 468 review
## Verdict and evidence
**still-relevant.** Issue 468 ("orchestration check spam") is OPEN. The requested frequency reduction, heartbeat coalescing and user-answer-based decision resolution are not demonstrated complete; existing dashboard question retention covers only part of the ledger requirement.

Evidence:

- The issue body says no product fix was implemented when it was filed, and the only comment (2026-11-17, status review) says a search of origin/master found no notification producer and no cadence control.
- The original literal searches for "decision ledger", "outstanding decision" and "orchestration message" did not identify a producer, but they missed implemented question retention: `src/superclaude/cli/observe/questions.py:3-11,81-137` retains questions without any closure evidence source, `src/superclaude/cli/observe/collector.py:214-245` integrates it, and `tests/observe/test_questions.py:40-78` covers retention, failed reads and absence from later source windows. These tests were read, not executed.
- `src/superclaude/core/WORKER-CONTRACT.md:7` says the dispatch preamble issued by the running Orca version is the authority for heartbeat cadence, and the contract never copies it. `src/superclaude/core/WORKER-CONTRACT.md:102` still lists `heartbeat` among the wake types of the coordinator's wait, and line 104 says the type filter only decides when the wait wakes, not what the returned batch contains.
- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:961` states the coordinator loop is not a program ("A coordinator program: N/A, not built") and that changing the heartbeat cadence is an Orca setting, not IronClaude code. Line 1746 states nothing in code enforces the contract's cadences.
- No pull request mentions issue 468. A search of all pull requests for "468" returned only pull requests whose numbers happen to contain those digits (411, 82), and neither body references this issue. `git log --all --grep=468` returned nothing about it.
## Real current state
The live issue records an open complaint with an unknown root cause. Producer ownership and whether a fix crosses a repository boundary remain UNVERIFIED; not finding a notification string in source does not identify its owner.

The coordination cadence described here is rule text; partial dashboard question-retention code also exists. The worker contract tells a coordinator session to wait with `orca orchestration check --wait` at a 300000 ms timeout (`src/superclaude/core/WORKER-CONTRACT.md:102`) and to sweep at most once every 5 minutes (`:111`). The technical reference records the Orca heartbeat default as 5 minutes, range 1 to 60, off when null, and marks the value actually running as UNVERIFIED (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1742`). The launch-level guard classifies `orchestration check` as a read-only verb (`src/superclaude/hooks/scripts/launch-level-guard.sh:497`); it does not generate notifications.

The existing question store is an in-memory dashboard component, not automatic coordinator-chat suppression. It retains questions across failed reads and disappearing source rows, but never closes them because it has no closure evidence source (`src/superclaude/cli/observe/questions.py:3-11,81-137`). Durable user-answer resolution and automatic presentation remain UNVERIFIED, not implemented by this store; notification cadence reduction and coalescing are also not established by the inspected evidence.

The analysis written for this review is at `.dev/issuecleanup/g2/468/analyze/analyze-report.md`.
## Concrete next steps
1. Locate the notification producer and current cadence controls before selecting the notification fix's code target. Orca is an investigation candidate because the technical reference cites external Orca files, not a verified owner. Local question-retention reuse can be assessed independently; keep issue 468 as the work item unless verified ownership or an explicit scope decision supports another destination.
2. Record a baseline before changing anything. The issue's own done-when requires the current notification frequency and the measurement window to be written down; neither exists anywhere read for this review.
3. Do not count a longer coordinator wait as the fix. The issue's pick-up note and `src/superclaude/core/WORKER-CONTRACT.md:104` both say the wait's type filter does not control what a delivery contains, so doubling the timeout does not halve heartbeat notifications.
4. Assess reuse of the existing dashboard question store, collector integration and retention tests before designing another store. Determine how actual user answers can supply closure evidence, what durability is needed and how automatic chat output should use that state; retention alone does not meet those requirements.
## Complexity and size
**complex / L, provisional.** The issue combines measured frequency reduction, message coalescing with acknowledgment/replay safety, and actual-user-answer decision resolution. Existing dashboard retention is a reuse candidate, not a complete solution. Root cause, producer ownership, repository boundary and exact effort are UNVERIFIED; confirm the estimate after producer discovery and reuse assessment.
## Priority
**P2, proposed.** The issue reports substantial routine-notification noise during one long-running supervised session, supporting an operator-experience priority recommendation. Multi-run recurrence, feature blockage, message loss, lifecycle accounting and urgent-event latency are UNVERIFIED; preserving urgent decisions and acknowledgments remains an acceptance requirement, not an observed guarantee.
## Dependencies
Needs: identify the notification producer and cadence controls and record a baseline before selecting that fix's code target. Orca source access may be needed if investigation confirms ownership there; that dependency is UNVERIFIED, not a gate on assessing the local question store.

Blocks: nothing found. No open issue states that it waits on 468.

Related, not blocking: issue 423 concerns proactive cross-workspace knowledge sharing in a later release, and issue 339 is the parent feature area. Issue 423 does not establish notification spam or decision-ledger behavior as accepted scope; retain issue 468 as the work item. Neither lists 468 as a dependency.
## Related issues
- 431, closed 2026-11-17. The weak-alive-check bug. Its liveness rules were merged and the issue was closed with the monitor work left under 423. The 2026-11-17 review of 468 named it as related because both concern what a coordinator does with routine signals.
- 339, open. The orchestrator feature, "run and manage all sessions within a worktree". A backlog review on 2026-11-23 graded it in-progress, complex, L, P1. This is the feature area 468 sits inside.
- 423, open. The orchestrator v2 proposal covers proactive cross-workspace knowledge sharing, explicitly excludes v1 work and follows v1 completion. Its live body does not establish it as the destination for issue 468's notification or question-ledger fix.
- 409, open. The terminal dashboard proposal for managing orchestration at scale. Named in 339's body as inspiration for a static report; adjacent, not the same complaint.
## Related PRs
None reference issue 468.

Checked: `gh pr list --repo IronbellyOrg/IronClaude --state all --search 468` returned pull requests 411 and 82, both merged, and neither body mentions issue 468 (the search matched the digits inside other numbers). `git log --all --grep=468` returned no commit about this issue. The worker contract's liveness section arrived through pull request 434 (merged 2026-11-08, "docs(orca): add the v1 worker-liveness rules to the worker contract"). It references issue 431, not 468, and its body does not contain 468. It predates this complaint's framing and changed rule text only.
## Verification limits and negative evidence
- Original analysis-package completeness is blocked: its contract declares succeeded but lists no command handoff, and the targeted inventory under `.dev/issuecleanup/g2/468/` contains none. Original Task/Dispatch provenance is UNVERIFIED from the supplied files. The producing worker or coordinator must reconcile the missing handoff from actual dispatch evidence and list it in the original contract; this revision's handoff is not a substitute.
- The Orca source was not opened. Producer ownership, repository boundary, cadence controls and running heartbeat value remain UNVERIFIED; the negative literal searches do not prove absence of behavior anywhere in IronClaude or establish an external owner.
- No notification frequency was measured, so the "half the baseline" target has no baseline.
- The technical reference's citations of Orca files are second-hand: the reference was read, the files it cites were not.
- Issue and pull request searches used `gh issue view`, `gh issue list` and `gh pr list` with `--repo IronbellyOrg/IronClaude` on 2026-11-24. A pull request that references 468 without the digits 468 in its title or body would not have been returned; none was found another way.
- Codegraph: index_state=fresh, checked_at=2026-11-24T02:38:29Z; degraded: none. The target file is markdown, which the index does not cover, so the code-graph lookup added no symbols and the Grep and Read results are the evidence.
