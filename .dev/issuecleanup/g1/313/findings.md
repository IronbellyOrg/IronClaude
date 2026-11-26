# Research: Issue 313, tests depending on committed working records

- **Topic type:** Issue status review
- **Scope:** Tests and the committed `.dev/` inputs they read
- **Status:** Complete, static review with disclosed evidence limits
- **Independent review:** PASS, /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/313/qa.md. Its minor deleted-module-size wording note was corrected; no blocking findings.
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md

---

## Findings

### Verdict and evidence
**Verdict: still-relevant.** The issue is partly reduced, not resolved. At reviewed checkout a7ae3dd30fcf88aaab655c37e94e58e121c2d863, four named test files still depend on committed working records; no targeted fix in progress was verified.

[CODE-VERIFIED] Examples are the direct eval-workspace import at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_grader_yaml_root.py:22-30 and the historical routing-package reads at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/test_routing_refresh.py:631-704. These preserve the issue's central failure mechanism regardless of whether today's checkout happens to contain the inputs.

PR #312 already removed the earlier audit checks (merged, commit 3e4d8b250552b03afe642e5673e0878dfd26d9ce). PR #656 subsequently deleted the workflow-vs-task-builder companion test (merged, commit a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6). Both statuses were read with the allowed GitHub commands; the latter deletion was also verified in local git history. The issue and its 2026-11-17 comment predate that second removal.

### Real current state
[CODE-VERIFIED] **Reflect grader:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_grader_yaml_root.py:22-41 loads the committed standalone grader before testing YAML validation. One test remains dependent on that workspace.

[CODE-VERIFIED] **Reflect seeded cases:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_reviewer_finding_parity.py:25-47 reads expected YAML and patch inputs from the committed workspace. Four tests use these inputs; the fifth only compares two constant tool sets and is not implicated.

[CODE-VERIFIED] **Audit folder history:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/audit/test_invariant_preservation_NFR_6_through_10.py:105,163-166,268-309,444-459 uses the checkout's task root for the existence check, two directory-name assertions and a composite verdict. Four tests remain coupled to the live folder history.

[CODE-VERIFIED] **Recommend planning retention:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/test_routing_refresh.py:142-145 locates a frozen task package; lines 631-704 read its specification, inventory and analyst reports. Two tests still enforce planning-record retention rather than only shipped behavior.

**Count:** 11 statically implicated tests remain among the issue's named files, versus its original 20. This is not a current executed failure count or a complete inventory of new dependencies. `git ls-files` confirmed the reflect grader, both reflect case inputs and the recommend specification/inventory are committed.

**Guard:** No dedicated guard against test reads of committed `.dev/` records was found in the searches described under Gaps. The existing hidden-input guard is a different invariant, not the requested prevention mechanism.

### Concrete next steps
1. Move the minimal reflect grader and both seeded cases to test-owned fixtures, update both reflect modules, and remove the working-record dependency. Do not revive the deleted eval companion or move its retired corpus.
2. Remove the two recommend planning-retention checks while preserving independent tests of current routing behavior and its existing test-owned cases.
3. Rework the audit checks to exercise the surviving artifact-layout behavior using `tmp_path`, or delete obsolete assertions if their only contract was the removed task-builder. Update the composite check as well as the standalone checks.
4. Add a guard that rejects actual reads/imports/enumeration of the checkout's committed working records but permits temporary `.dev/` inputs and literal `.dev` strings. Include positive and negative regression cases so a text-only ban cannot masquerade as coverage.
5. Run focused tests and compare full-suite results with and without committed working records in an isolated disposable checkout. Do not delete or move this shared worktree's `.dev/` directory. Update the issue's obsolete count and close only once the guard and behavior checks pass.

### Complexity, size and priority
- **Complexity: medium. Size: M.** Assessment: four surviving test modules need coordinated input/expectation changes, plus a guard that distinguishes committed inputs from valid temporary folders; no shipped feature redesign is required.
- **Priority: P2.** Assessment: cleanup can produce false CI failures and block unrelated maintenance or merges, but the verified problem is test reliability, not a production outage or data-loss defect. A current failing CI run is UNVERIFIED.

### Dependencies, related issues and related PRs
**Dependencies:** The issue's structured `blockedBy`, `blocking`, parent and sub-issue lists are empty. No numbered prerequisite or blocked issue was verified. The practical benefit is unblocking safe cleanup of working records; this is not a claim of a recorded issue dependency.

**Related issues:** #647 (6.1.0 bundle-removal work) and #571 (parent removal plan) are context cited by merged PR #656, which removed one of this issue's targets. They are not prerequisites for the remaining fix. Their present issue states and acceptance criteria were not inspected (UNVERIFIED). The issue search found no verified duplicate of #313.

**Related PRs, all verified merged through `gh pr view --repo IronbellyOrg/IronClaude`:**

| PR | Relation | Verified merge commit |
|---|---|---|
| [#306](https://github.com/IronbellyOrg/IronClaude/pull/306) | Historical cleanup named as a trigger in the issue | e561d3403784fac0be7062102a14120ce4fe4d17 |
| [#308](https://github.com/IronbellyOrg/IronClaude/pull/308) | Second historical cleanup named as a trigger | 22eaa0c7c638639e460a1f8c8feb54c1bf447a0c |
| [#312](https://github.com/IronbellyOrg/IronClaude/pull/312) | Removed the earlier historical audit checks; did not settle the follow-up | 3e4d8b250552b03afe642e5673e0878dfd26d9ce |
| [#656](https://github.com/IronbellyOrg/IronClaude/pull/656) | Deleted the eval companion containing the nine dependencies listed in the original issue, and retired its suite | a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6 |
| [#664](https://github.com/IronbellyOrg/IronClaude/pull/664) | Delivered the 6.1.0 removal bundle | 64dfc0e8622281a56d6c4e6826c63d50c6959da8 |
| [#539](https://github.com/IronbellyOrg/IronClaude/pull/539) | Mentioned in the status comment as feature history; read-only sweep feature, not this cleanup | 4d3c0b126151789bd0cb5b481b10f572a0c4e6b7 |
| [#411](https://github.com/IronbellyOrg/IronClaude/pull/411) | Mentioned feature history: unattended worker contract | cb8f2f81ab7d99c51bcfe81fec8e200b52cf2c86 |
| [#373](https://github.com/IronbellyOrg/IronClaude/pull/373) | Mentioned feature history: issue command | 6542ca72b145cec1b86eae49eb06d6fac7c7dc67 |

No open PR was returned by the scoped search for `.dev` and test; no closing PR is recorded on issue #313. This search does not prove that unlinked or differently worded work does not exist.

## Gaps

- **UNVERIFIED: complete issue event timeline.** The issue body, its one returned comment, created/updated/closed metadata, state, dependency fields and closing-PR field were read. The permitted `gh issue view ... --json timelineItems` request failed with `Unknown JSON field: "timelineItems"`. The brief permits only issue/pr view/list on GitHub, so no API, browser, or broader GitHub command was used to fetch timeline-only events. No historical event sequence beyond the returned records is claimed.
- **UNVERIFIED: original 2026-10-27 experiment and current failure count.** The original CI run and reporter-only experiment directory were not inspected or reproduced. No tests ran under this static analysis command, and the shared `.dev/` tree was not moved or deleted.
- **Guard negative evidence:** a suite-wide filename/content scan found 115 Python files mentioning `.dev` (not 115 violations). Searches for committed-record/dependency/planning phrases returned no prevention guard; guard-named tests and the shared conftest were inspected. The hidden-input guard checks a different behavior. A detector implemented under an unexpected name or without these terms remains UNVERIFIED; no exhaustive absence claim is made.
- **Scope of count:** inspected the issue's named modules; did not trace every `.dev` string in all 115 files. Additional post-issue dependencies remain UNVERIFIED.
- **Lookup correction:** an initial tracked-file query used an incorrect recommend package spelling and returned no package hits. After reading the module's `_PACKAGE` value, the corrected query verified its committed specification and inventory; the empty first result was not treated as absence.
- **Tool recovery:** the edit hook rejected the first attempt to populate the just-created analysis stub until it was explicitly Read. Both stubs were then Read and populated through Edit; no bypass or source changes occurred.
- **No implementation:** no guard was added and no tests were changed. The report and supporting command/handoff/review records are the only writes.

## Key Takeaways

Keep #313 open as still-relevant, medium complexity, M size and P2 priority. The smaller complete fix covers the surviving reflect, audit and recommend dependencies plus prevention; the retired eval comparison needs no new work. The timeline limitation and unexecuted failure count do not erase the directly verified dependency defects.
