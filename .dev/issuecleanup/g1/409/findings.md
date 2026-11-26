# Issue 409: observer dashboard review

Template: coordinator-required fields, structured using `.dev/issuecleanup/g1/362/report-template.md` (Findings template).

## Verdict and evidence
**Verdict: in-progress.** The dashboard is substantially implemented, but the parent explicitly remains open for the outstanding work in [#706](https://github.com/IronbellyOrg/IronClaude/issues/706), as its latest comment of 2026-11-20 states. This verdict means partly delivered, not a claim that someone is currently implementing the remainder.

The old issue body is not a reliable build-status checklist: it still says no observer exists and the direction is unchosen. Both live-question guards are now enabled at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/commands.py:67-70`; merged delivery is independently corroborated by PR #503 (`9e2608b03857c78ab89fc9439c85256d3bd5d989`), #514 (`cd873619957b3fd4235c54f00363664fca28a193`), #577 (`44ff04aeff5ce4bc51cc423a4bf4ffcb59d001cc`), #592 (`3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda`) and visual-parity PR #673 (`b68d5eeaf618a8e33cde55cb660acfdd8f321f67`). GitHub reports #606, the visual-parity subissue, closed; #706 remains open.

**Material correction to #706:** its statement that the size combinations have no tests is too broad. The production observer already has the full 5/8/10-Run by 50/80/100-row by 160/116/80-column rendering matrix at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/observe/test_render.py:99-118` (27 parameter combinations). This checks line/height bounds and counts, not live performance or every difficult-data scenario at every size. The row generator represents Runs, not a verified one-to-one mapping to orchestrator sessions (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/observe/conftest.py:179-204`). Do not rebuild this matrix or use #706's blanket absence claim to size the work.

## Real current state
**Implemented in the checkout:** worker ledger, fixture replay, questions for one named Run, exact dispatch-level Decision Desk linkage, inspector navigation and record/snapshot export. The collector uses a 15-second interval/budget and backoff capped at 60 seconds (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/collector.py:28-34`). Question linkage and its unknown-scope fallback are implemented at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/view.py:888-948`. The screen-only payload rule has a dedicated record test at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/observe/test_export.py:312-326`.

**Still missing from the observer:** the shared sweep source or exhaustive difference contract, human-readable per-session task/done/remaining summaries, issue/PR links and named workflow steps. Source selection is fixture-or-Orca only at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/commands.py:164-170`. Session-open navigation is not implemented: Enter selects the internal inspector, and the complete key handler contains no session-opening effect (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/view.py:1246-1300`). #706 expressly permits a recorded owner ruling to drop or move an item instead of implementing it.

**Decisions and limits:** #706 still requests owner rulings on the data source, supported session navigation/disclosure, recommendation text and watcher-state scope. Remote fleet is separately deferred in #604. This review verified implementation and test definitions on disk, not present-day live operation or runtime test results. The latest merged user-guide and record-only PRs are #708 and #730; they do not fill the remaining feature gaps.

## Concrete next steps
1. Keep #409 open and use #706 as its remaining-work checklist; do not open a duplicate implementation issue. After the owner's go, the coordinator can replace the stale parent status and correct #706's overbroad missing-scale-tests sentence. This worker made no such GitHub edits.
2. Resolve #706's existing source/scope decisions before planning data integration: shared sweep facts versus documented differences, which summary/link/step source is authoritative, session-opening support versus disclosure, recommendations and watcher-state visibility.
3. Implement only the approved missing summaries, links, named steps and navigation/disclosure, with missing-source values explicit. Preserve the read-only boundary and screen-only payload rule.
4. Reuse the existing 27 rendering size/width cases. Add only genuinely missing cross-scenario coverage (uneven ownership, shared/unmapped worktrees, history, duplicates/out-of-order events, stale/missing data at required sizes) and any separately required live timing/coverage evidence. The full cross-scenario acceptance is UNVERIFIED by this quick pass; it must be mapped to existing tests before estimating new cases.
5. Include #706's November 22 comment in that same follow-up: the worker-worktree experiment exception, fixture-only FROZEN marker and same-second export-overwrite documentation. Their requested fixes were read in #706; each guide correction still needs its own source/contract validation before editing.
6. Leave remote fleet work in #604 until its cross-host ownership evidence and owner gate are satisfied. Close #409 only after #706's acceptance is met or its remaining items are explicitly dropped/moved by the owner.

## Complexity and size
**Complexity: complex. Size: L.** Remaining work spans a source-contract decision, observer/sweep alignment, new session-level data and navigation, plus cross-scenario acceptance; the renderer and size matrix already exist, so this is not an XL dashboard rewrite. This estimates the remaining #706 work, excludes deferred remote fleet #604, and is not a measured duration.

## Priority
**P2.** Important for human supervision at the stated scale and blocks closing #409, but the local read-only dashboard is already delivered; no outage, data-loss incident or critical workflow dependency was established. This is a triage recommendation, not a GitHub priority-field change.

## Dependencies
- **Needs #706:** explicit closure dependency from #409's November 20 comment and #706's Done when section. #706 is OPEN with no closing PR references returned by issue view.
- **#606 is satisfied:** visual parity subissue CLOSED, delivered through merged #673. It is not an outstanding blocker.
- **#604 is separate backlog:** remote fleet remains OPEN and explicitly deferred; the latest #409/#706 split does not make it a prerequisite to the remaining local work.
- **#339 and #534:** source/alignment relationships for the sweep and its follow-ups, not verified whole-issue prerequisites. Do not block all #706 work on their completion without a concrete missing-source dependency.
- GitHub's returned structured blockedBy and blocking lists for #409 are empty. No other issue was verified to require #409 as a hard predecessor.

## Related issues
Direct: [#706](https://github.com/IronbellyOrg/IronClaude/issues/706) (remaining local capabilities, acceptance and three guide fixes), [#606](https://github.com/IronbellyOrg/IronClaude/issues/606) (completed visual parity), [#604](https://github.com/IronbellyOrg/IronClaude/issues/604) (deferred remote fleet).

Mentioned context in #409, not asserted as hard blockers: #339 (agent-facing supervision), #534 (sweep follow-ups), #589 (fresh-question read evidence), #444 (sub-orchestrator evaluation), #423 (later orchestration), #331/#450 (watcher implementation/rollout) and #394 (launch-level enforcement). Their present full implementation state was not re-audited here. The issue also mentions Coder#477 (listener/registration) and Coder#195 (prior pairing work); those other-repository issues were not accessed because the brief restricts GitHub reads to IronbellyOrg/IronClaude.

The parent explicitly says #326, #320, #315 and #323 were searched previously but not confirmed related. This review does not promote those weak associations to dependencies.

## Related PRs
All rows below were read directly with `gh pr view --repo IronbellyOrg/IronClaude`; GitHub reports each MERGED. Dates are merge dates, not inferred from issue prose.

| PR | Verified contribution | Merge date | Merge commit |
|---|---|---|---|
| #503 | Release 1 worker ledger and observer package | 2026-11-11 | `9e2608b03857c78ab89fc9439c85256d3bd5d989` |
| #514 | Release 2 one-Run questions, initially disabled | 2026-11-12 | `cd873619957b3fd4235c54f00363664fca28a193` |
| #577 | Enabled questions and recorded direction choice | 2026-11-17 | `44ff04aeff5ce4bc51cc423a4bf4ffcb59d001cc` |
| #586 | Documentation of live probe and synthetic load observations | 2026-11-17 | `a98541153ad973d14fbf0613c8af7325acea8208` |
| #592 | Release 3 question text, dispatch join, Decision Desk | 2026-11-17 | `3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda` |
| #598 | Owner's screen-only payload-text decision | 2026-11-17 | `10f6ec670bf55f0fe768be8e0ef2067d5c5d879e` |
| #673 | Visual parity for #606 | 2026-11-19 | `b68d5eeaf618a8e33cde55cb660acfdd8f321f67` |
| #708 | Observer/orchestrator user guides; not remaining capability implementation | 2026-11-20 | `52d371e2c20a32a4c17613108daa7f0a295baa36` |
| #730 | Preserved existing research and review records, no source changes | 2026-11-23 | `98879e631e6d7986d14c0dc94720007cbb2fde0b` |

Also read the issue's contextual PRs: #532 (supervision technical reference, `05b78d4d351259b798e5794af58626a4d9cbd693`), #539 (sweep Phase 1, `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`), #541 (old test blocker fixed, `0406ef5b01f2e79c88100d32f01df4ebf2395646`), #591 (watcher-to-coordinator handoff, `6af80d6c04f74d7c1db196f467e09c1d937d5503`) and #447/#448 (watcher baseline and fixes, `4c93b6c7397e91b680b0306e99f32835bc364611` / `ce660825856185aa043f65dad34128e1a238b720`). Their merge does not imply the observer reads sweep data or shows watcher state.

A bounded PR-list search for 409 and 706 found no additional pending capability PR; text-search completeness and unseen timeline cross-references remain UNVERIFIED.

## Verification limits and negative evidence
- Reviewed on 2026-11-23 in the assigned feature worktree. The required `/sc:analyze` ran at the top level through the Skill tool, with quick architecture scope and unattended mode. Its report is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/409/analyze/analyze-report.md`.
- GitHub evidence: read the whole #409 body, all nine returned comments (2026-11-06 through 2026-11-20), closure references and structured dependencies, plus #706 and its November 22 follow-up, #604, #606 and the PRs listed above. Full timeline events are **UNVERIFIED**: installed `gh issue view` exposes no timeline JSON field, and the brief permits no `gh api` or browser route. Do not interpret this report as a complete label/assignment/cross-reference event audit.
- Initial GitHub view failed because this CLI refuses `--comments` together with `--json`; the retry used the supported JSON comments field and succeeded. The project command copy was absent; the installed copy has Unattended mode, so the guard passed. Augment's initial main-branch lookup failed; its master retry succeeded. The graph caller query was truncated and reported as such.
- Search floor: inspected observer source model, source builder, adapter allowlist and complete key handler, and searched observer Python/tests for sweep, GitHub, summaries, issue/PR URLs, named steps and session-open support. Stage-detail strings are not evidence of named workflow steps. Existing fixture and matrix tests are not absent just because the issue says so.
- No observer execution, tests, benchmarks, production-read measurement or render gate was run. Present test pass/fail status and full cross-scenario scale acceptance are **UNVERIFIED**; historical PR test counts are not represented as fresh results.
- The design branch's current ancestry and whether every historical attachment remains downloadable are **UNVERIFIED**. The merged #730 research-record preservation is verified but does not establish that the entire separate design branch merged.
- GitHub remained read-only. No code, index, commits, issue fields, comments, labels or PRs were changed; outputs are confined to this task's report directory. No issue closure is authorized by this report.
