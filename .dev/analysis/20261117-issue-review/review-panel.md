# Cluster review-panel, status review 2026-11-17

Comment base: https://github.com/IronbellyOrg/IronClaude/issues/<n>#issuecomment-<id>. Drafts are in `/home/coder/workspaces/IronClaude/.dev/analysis/20261117-issue-review/drafts/<n>.md`.

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 520 | [FEATURE] Centralized Review Panel | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/520#issuecomment-6941354298 | Body still calls #519 unmerged; #519 merged 2026-11-12; plan carried on #549 |
| 525 | Review Cluster Pairs Same Problem - PR519 (parent) | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/525#issuecomment-6941354846 | 0 of 5 children done, no answers, no later PR resolves the pairs |
| 526 | ... P01-P10 | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/526#issuecomment-6941355490 | No assignee, no comments, ANSWER lines blank on origin/master |
| 527 | ... P11-P20 | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/527#issuecomment-6941356028 | Same |
| 528 | ... P21-P30 | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/528#issuecomment-6941356487 | Same |
| 529 | ... P31-P40 | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/529#issuecomment-6941356965 | Same |
| 530 | ... P41-P50 | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/530#issuecomment-6941357518 | Same |
| 531 | [FEATURE] Shadow Run Module | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/531#issuecomment-6941358074 | No module PR; #581 added a combos experiment only |
| 549 | [FEATURE] Review-Panel Merged Efforts | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/549#issuecomment-6941358683 | Owner notes 11-14 and 11-15; plan not yet written |
| 552 | [FEATURE] Issues classified as blockers too egregiously | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/552#issuecomment-6941359303 | #581 and #582 merged (stages 0, 1, 3); stage 4 awaits owner go |
| 346 | Document review loops do not converge | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/346#issuecomment-6941359956 | #477-#484, #490-#492, #498, #582 merged; no convergence rerun found |
| 376 | sc:adversarial scoring mixes 25 and 30 criteria | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/376#issuecomment-6941360566 | origin/master SKILL.md:1757,1760, artifact-templates.md:201, debate-protocol.md:192 still say 25 |

## Close candidates

None. The five children #526 to #530 and parent #525 are not done; if the owner decides the hand check is no longer wanted after the merged shadow runs, they could be closed as superseded (owner call, see question 2).

## Owner questions

1. #346: Close as delivered (text and prompt fixes plus #582), with spec-panel retirement and a convergence re-test tracked separately, or keep open until a re-test shows a loop converging?
2. #525 family (raised as a next step, not a verdict): is the 50-pair hand check still wanted now that the shadow stage is merged, and does any promotion stage depend on it? UNVERIFIED which stage needs it.
