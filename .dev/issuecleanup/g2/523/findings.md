# Issue 523 review

Template: ../450/report-template.md, Findings skeleton; required fields supplied by the coordinator brief.

## Verdict and evidence
**verdict: still-relevant.** Keep the feature request open: adding Ember to ccsession Tier 4 is not implemented in the inspected checkout. Confidence: high for repository state; runtime availability remains UNVERIFIED.

- Reviewed https://github.com/IronbellyOrg/IronClaude/issues/523 on 2026-11-24, including its body, its one returned comment (2026-11-17), empty closing-PR references, and empty formal dependency fields. It remains OPEN.
- Baseline: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/ccsession-models.json:120-126` still lists only T4Model01, T4Model02 and T4Model03. Ember is absent from its picker lists and display overrides at lines 129-178.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_ccsession_tiers.py:85-91,219-222` still supplies and asserts exactly three Tier 4 slots. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:46` still lists Luna, Haiku and Grok without Ember.
- The old claim that Ember is absent everywhere in this repository is now false: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-tiers.default.json:10-19` has Ember in the separate review seat tier5c, but still not in tier4. Related merged PRs #623 (`7f93c0d9f7b72938976127d59a2bf523c06d5e03`) and #660 (`30a6919168de4288c5712b0ffc8531d2716da22c`) do not satisfy this issue's ccsession acceptance criteria.
## Real current state
- **Implemented already:** generic slot-based tier resolution, ordered failover and picker construction. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/models.py:655-677` preserves JSON slot order and rejects missing slots. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:350-369,823-841` builds tier labels from resolved models, then walks the same ordered list and skips models whose own context window is too small. No new tier algorithm or separate Ember profile is needed to meet this issue.
- **Not implemented:** T4Model04 membership, Ember's ccsession picker visibility/display/context metadata, the updated Tier 4 documentation and fixtures, and an Ember-specific ccsession regression test. Source and test searches found no T4Model04 registration; CHANGELOG search found no Ember entry.
- **Separate functionality, not partial completion of this issue:** the review system already names Ember directly as review-seat-5c. That does not add it to ccsession Tier 4, and does not prove the gateway serves it today.
- **Release safety remains material:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/models.py:233-244,260-294,301-308` loads versioned bundled/downloaded data and refreshes the cached JSON. A new referenced slot must exist before rollout: resolution raises at lines 667-669, and tier_access builds every tier at lines 628-632 before filtering. The issue's comment reports PrivateRepoF#503 shipped the slot; that external rollout is UNVERIFIED in this restricted review.
## Concrete next steps
1. Before merging any slot-list change, have the coordinator verify the PrivateRepoF#503 release and relevant workspace defaults contain T4Model04=muse-ember-1.0 and T4Model04_WINDOW=1000000; separately verify a live completion succeeds. This worker did not make that outward call.
2. Update ccsession JSON's tier4 order to [T4Model01, T4Model04, T4Model02, T4Model03], preserving Tier 3 and all existing slot meanings. Add Ember to picker.show, picker.one_million_context and picker.display_overrides, and increment the data version through the existing release convention.
3. Update the review data tier4 list at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-tiers.default.json:10` in the same change, preserving the separate review-seat-5c. Its length must track the new four-slot ccsession tier or the existing consistency test fails (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/review/test_review_panel_live7.py:94-108`).
4. Update slot fixtures/assertions in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_ccsession_tiers.py`, applicable alias-policy and review tests, and README, MODEL-TIERS and CHANGELOG. Cover ordering, picker display/context and tier fallback to Ember; retain missing-slot failure coverage. Run focused tests and the required full suite before release. Keep unknown scores and prices explicitly unknown.
## Complexity and size
**complexity: simple; size: S.** This is a bounded configuration, documentation and regression-test update using existing ordered-slot behavior, with no new routing mechanism; cross-repository rollout verification is a release gate rather than new feature scope.
## Priority
**priority: P2.** An explicitly requested budget-tier option remains unavailable through ccsession Tier 4, but the existing three models remain configured and there is no verified outage or downstream issue blocked by this addition. Unsafe rollout could break all tier resolution, so preserve the Coder-first gate.
## Dependencies
- **Needs:** IronbellyOrg/PrivateRepoF#503, the external additive slot/defaults rollout. Issue 523's 2026-11-17 comment says it is closed and shipped in release 20261112-1 to eight reachable running workspaces. This is historical issue testimony, not a fresh external check: current closure, deployment completeness and live serving are UNVERIFIED because the brief permits GitHub reads only on IronbellyOrg/IronClaude.
- **Blocks:** no formal blocking issues returned by `gh issue view 523 --json blockedBy,blocking,parent,subIssues`; no verified repository-side prerequisite issue remains. Its prose calls #488 a parent, but the formal parent field is null. Neither #489 nor #517 is demonstrated to be a hard dependency.
## Related issues
- #488, the previous tier restructuring request: CLOSED; conceptual parent in the issue prose, not a formal GitHub parent.
- #489, updating eval-framework panel tiers and alias data: OPEN; overlapping review data, not a verified prerequisite.
- #517, tier failover when the first model always thinks: OPEN; shared runtime behavior, not solved by adding this model.
- IronbellyOrg/PrivateRepoF#503, matching workspace slot addition: external dependency described above; not queried under this brief's repository boundary.

Issue titles/states for the three IronClaude issues were freshly read. Their full linked histories were not recursively audited.
## Related PRs
- #518, merged 2026-11-12, previous owner tier decisions: `167184c6ba449ab49b7f2af1dc9f4c9080006bd3`. Its body explicitly says ccsession-models.json was unchanged; it is not Ember completion.
- #614, merged 2026-11-17, planning-only work for the default review panel: `c00caea930e5a0d68b5c89716a396d916ac41d97`. Mentions Ember in a three-model review panel, not ccsession Tier 4.
- #623, merged 2026-11-18, shipped the provisional default review panel: `7f93c0d9f7b72938976127d59a2bf523c06d5e03`.
- #660, merged 2026-11-19, renamed separate review-seat labels: `30a6919168de4288c5712b0ffc8531d2716da22c`. Its body explicitly distinguishes those labels from real gateway tiers.
- No closing PR is recorded for #523. Searches across all PR states for muse-ember, wonsol default, and explicit #523 body references found the related work above but no implementation PR for this request. A loose search for 523 also returned unrelated #199, which is not evidence of completion.
- Coder PR #502 is mentioned in the issue's historical dependency section; its contents and current status are UNVERIFIED under the cross-repository read restriction.
## Verification limits and negative evidence
- **Timeline UNVERIFIED:** `gh issue view 523 --json timelineItems` failed with `Unknown JSON field: timelineItems`. The permitted issue view/list and PR view/list commands exposed body, comments, timestamps, closure and dependency links, but not the complete event timeline. I did not bypass the explicit allowlist with gh api, a browser or another repository.
- No Coder repository, workspace defaults, gateway model-list or completion call was made. Historical claims about deployment and serving are marked UNVERIFIED, not silently promoted to current facts.
- No tests or live ccsession launch were run: this was the requested static architecture review, with no product edits. The test consistency risk is established by reading its assertion, not by observing a failing test.
- Grep searched source and tests for muse-ember and T4Model04, ccsession data/docs for tier4 and Ember, and CHANGELOG for Ember/523. It found Ember only in separate review configuration/tests among the searched production/test paths; no ccsession registration and no Ember changelog entry were found. This is bounded negative evidence, not proof that no unpushed work exists elsewhere.
- Augment default branch main lookup failed; master lookup succeeded but returned historical leads. Local live files, not those excerpts, drove the verdict.
- Source was read from the named baseline checkout. No fetch or remote-branch freshness claim is made. GitHub issue and PR metadata was read live.
- Analysis report: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/523/analyze/analyze-report.md`. All generated files stay within the assigned report directory; no source, issue or PR was changed.
