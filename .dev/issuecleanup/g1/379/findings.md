# Issue 379: wrong-repository ClickUp assignment review

Template: coordinator-required fields, using the registered findings structure in `.dev/issuecleanup/g1/362/report-template.md`.

## Verdict and evidence
**Verdict: still-relevant.** Reviewed 2026-11-23 in checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Issue #379 is open, has no assignee and no linked closing PR in the permitted issue read. No completed or partial fix was found in the checked helper or targeted PR searches.

- The helper blob is still `65b8d643123b2ca19c18925558ec6dd8240cee20`, exactly the blob cited in the issue. Local history shows only introducing PR #373, merge commit `6542ca72b145cec1b86eae49eb06d6fac7c7dc67`.
- `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:148-159` still promotes arbitrary description/custom-field URL mentions and bare issue-number title tokens into assignment matches. Lines 200-221 select a unique candidate; lines 232-238 perform the assignment PUT with no authoritative relationship or pairing confirmation.
- The November 17 issue comment says the path was unchanged and cites later claim PRs #583 and #584. Those PRs are merged but address launch approval and issue-pipeline approval, not task identity; the unchanged helper blob independently confirms the defect remains.
- The requested `/sc:analyze` command completed on the narrowest source file. Its evidence and recommendations are in `analyze/analyze-report.md`; its worker contract and handoff are also preserved.

## Real current state
**Implemented and still unsafe:** the helper skips when credentials/workspace are missing; otherwise it reads the token owner, scans workspace pages, prefers URL mentions, falls back to title `#N`, checks uniqueness and adds the assignee. The assignment boundary checks neither the selected task's repository nor an exact confirmed pairing. The CLI does validate the *input* repository and issue URL (`clickup_claim.py:245-258`), which does not establish the identity of the selected ClickUp task.

**Source-derived failure, not a live incident:** with no requested-URL candidate, a sole task titled `OtherRepo #302` whose description links only to another repository's issue 302 becomes `title_number`; after the final empty page, a missing token-owner assignee leads to the PUT. A sole task merely cross-referencing the requested issue URL qualifies under `github_link` as well.

**Existing protections:** multiple candidates in the selected match class, a search that reaches its page cap before an empty page, and failures during the pre-assignment reads return before any assignment PUT. These guards do not reject a sole wrong-identity candidate (`clickup_claim.py:181-240`). An error after the PUT has been sent does not prove the server made no change; this helper provides no rollback guarantee.

**Tests and documentation preserve the old design:** `tests/skills/test_clickup_claim.py:208-239` expects URL-mention matches; lines 259-274 expect title-only assignment. The design explicitly defines these rules (`docs/designs/sc-issue-command.md:327-331`), and the user guide repeats them (`docs/user-guide/commands.md:368`). This is a requested safety-contract change, not an undocumented divergence.

**Not built in this helper:** a native integration-relationship reader, an explicit ClickUp task-ID selection argument, or exact pairing-confirmation handling. Native relationship availability is UNVERIFIED. Existing tests were inspected, not executed; no assignment was attempted.

## Concrete next steps
The issue is not partly fixed in the reviewed helper. Concrete remaining work:

1. Make title tokens and description/custom-field URL mentions discovery-only. Return unresolved/confirmation-required without a PUT when identity is unverified, even for one candidate. Removing only the title fallback would leave the URL cross-reference hazard.
2. Verify whether an available, supported reader exposes an authoritative native GitHub relationship with exact repository and issue identity. Use it only when proven; do not guess a response field or create custom fields.
3. Where authoritative mapping is missing, inaccessible or ambiguous, add an explicit task-ID path with confirmation of the exact issue/task pairing. Reject missing, conflicting or changed pairing evidence before the assignment boundary.
4. Update the helper, claim-protocol invocation/result reporting, existing matching fixtures, design and user documentation together. Preserve uniqueness, incomplete-search, reader-failure and request-error no-write behavior, plus exact issue-number boundaries and the supported URL suffix/case behavior.
5. Cover the issue's full fixture matrix with recorded mock PUT counts: wrong-repository and bare-number candidates, URL cross-references, native linkage, missing/conflicting/changed confirmation, multiple candidates, incomplete pagination and reader failures. A separately authorized smoke test must verify the intended task gains the assignee and unrelated tasks remain unchanged. No live-test authorization is assumed here.

## Complexity and size
**Complexity: medium. Size: M.** The change is localized but must coordinate task identity, confirmation, CLI/protocol results, documentation and a safety-focused mock matrix; native-linkage capability research is the main uncertainty.

## Priority
**Priority: P1 (recommended).** With ClickUp configured, a normal claim can write an assignee to unrelated work without a verified pairing, so the safety fix should precede broader token-enabled claim automation. This is not P0: no outage, observed live misassignment or credential exposure was established, and the path skips without a token/workspace. The two cited no-token claims show those runs skipped, not a measured frequency of all production use.

## Dependencies
- **Needs:** no numbered prerequisite established. Capability verification for native ClickUp/GitHub linkage is an implementation prerequisite, not a verified separate issue.
- **Blocks:** no formal blocking issue recorded. GitHub's `blockedBy`, `blocking` and sub-issue lists are empty for #379. Safe token-enabled automatic ClickUp assignment should depend on this fix as a recommendation, not as a claimed existing tracker dependency.
- Original feature #302 is already closed; it supplies context, not an unresolved prerequisite. No dependency on launch approval PRs #583/#584 was found.

## Related issues
- [#302, original issue-command feature](https://github.com/IronbellyOrg/IronClaude/issues/302): closed by PR #373; requested assignment of the corresponding ClickUp entity.
- [#394, claim-launched agent enforcement hook](https://github.com/IronbellyOrg/IronClaude/issues/394): closed; its claim comment reports `ClickUp: skipped (no_token)`. Cited in #379's November 17 review as usage evidence, not a matching fix.
- [#450, issue-watcher rollout](https://github.com/IronbellyOrg/IronClaude/issues/450): open; its claim comment likewise reports `skipped (no_token)`. Operationally adjacent, but no formal dependency on #379 was recorded.
- The broader `ClickUp in:title,body` issue search found other orchestration/reporting issues; none was established as a replacement for #379. Those broader matches were not treated as dependencies.

## Related PRs
- [#373, introduced the issue command and ClickUp helper](https://github.com/IronbellyOrg/IronClaude/pull/373): merged 2026-11-04, commit `6542ca72b145cec1b86eae49eb06d6fac7c7dc67`. Its body reports the ClickUp smoke claim and assigned-to-someone-else case still pending; merge is not evidence that live checks later passed.
- [#388, documented ClickUp settings/matching](https://github.com/IronbellyOrg/IronClaude/pull/388): merged 2026-11-05, commit `901f118124a575f74b17b0a2d1e0632fe8fa6ca9`. Documentation only, not an identity fix.
- [#425, claim launch-pipeline flags](https://github.com/IronbellyOrg/IronClaude/pull/425): merged 2026-11-07, commit `f8305000b86af1894e1632f76462a10db589db64`. Claim launch behavior, not a ClickUp matching change.
- [#583, removed bare-approved launch release](https://github.com/IronbellyOrg/IronClaude/pull/583): merged 2026-11-17, commit `d32465f21b103e52d9e620bafb528c2ac7c46fbc`. The relevant file list changes claim instructions and launch prompts, not the helper.
- [#584, issue-pipeline approval core](https://github.com/IronbellyOrg/IronClaude/pull/584): merged 2026-11-17, commit `b6d038a30c15ebeab5797c7b039500ee5dc6bb63`. Approval plumbing, not matching.
- [#690, issue planning mode](https://github.com/IronbellyOrg/IronClaude/pull/690): closed without merge. It describes no ClickUp call in the new plan mode and no helper change; it does not fix #379.
- No open matching fix was returned by the targeted `clickup_claim`, `wrong-repository` and `title_number` PR search. The broad numeric `379` search returned unrelated results, not proof of a fix.

## Verification limits and negative evidence
- **Full GitHub event timeline: UNVERIFIED.** The allowed `gh issue view/list` and `gh pr view/list` reads expose issue body, comments, timestamps, current relationships and PR metadata, but `gh issue view --help` lists no timeline/events field. No forbidden `gh api`, browser read or outward action was used to fill the gap. Available chronology: issue created 2026-11-04T22:17:23Z; one visible review comment 2026-11-17T07:09:32Z; that is also the returned issue `updatedAt`. This is not a complete event history.
- Read issue #379's full body and its one returned comment, the body/comments/review summaries of introducing PR #373, and body/state/relevant file metadata for later PRs #388, #425, #583, #584 and #690. Full later PR discussion threads and inline review threads are UNVERIFIED; searches are bounded discovery, not exhaustive timeline traversal.
- **Runtime and live capability: UNVERIFIED.** No existing tests or helper code were executed, no mock PUT experiment was performed, no ClickUp credentials were inspected and no ClickUp read/write or smoke assignment occurred. Existing fixtures were inspected statically. The issue's example remains source-derived, not an observed live incident.
- **Newest remote source: UNVERIFIED.** Source claims apply to the reviewed checkout commit and on-disk helper blob. No fetch, pull or other remote git operation was run; live issue/PR metadata was read using the explicitly pinned fork only.
- No native integration schema was invented, no issue or PR was edited/commented/labeled/closed/linked, and no source change, staging or commit was made. Report writes are confined to this task's report directory.
- Recovery note: initial edits to the analysis stub were blocked by the freshness hook; a tracked Read followed by ordinary Edit calls resolved it. No bypass or alternative write path was used.
- The analysis completed, but full requested history coverage is partial because the permitted reader cannot expose the event timeline. The enclosing worker contract records `partial` so the coordinator can decide whether this report is sufficient.
