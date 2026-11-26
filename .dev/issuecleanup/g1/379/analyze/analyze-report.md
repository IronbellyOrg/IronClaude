# ClickUp claim architecture analysis

Template: registered analysis structure in `.dev/issuecleanup/g1/362/report-template.md`.

## Scope and grounding
- Command: `/sc:analyze src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/379/analyze`.
- Read-only static review of the 271-line helper, its claim-protocol caller and focused test fixtures. No production source changed and no ClickUp request was made.
- Codegraph: index_state=fresh, checked_at=2026-11-23T23:05:50Z; degraded: graph:unresolved.
- The graph's unrelated `split` callee in an experiment file was rejected as an unresolved edge. Direct source inspection establishes the real string split. The graph identifies the local matching-to-assignment path; source reads confirm it.

## Architecture and metrics
The standalone standard-library helper combines transport, candidate discovery, identity selection and assignment in one file. `main` passes the canonical GitHub issue URL and process environment to `claim`; `claim` gets the token owner, scans workspace task pages, calls `match_rule`, selects one candidate and adds the assignee. The surrounding claim protocol invokes it after GitHub assignment and treats ClickUp operational outcomes as non-fatal.

Measured scope: one 271-line target file, two match classes, three HTTP endpoint roles (user read, task-page read, task update), and one assignment PUT call site. These are static counts, not runtime performance measurements. Impact analysis identifies `match_rule -> claim -> main`; the test file imports the helper dynamically, and the protocol calls it as a script, so those consumers require text inspection as well as graph lookup.

The request boundary validates the supplied repository/issue URL, but the selected task boundary does not prove that the task belongs to that issue. Pagination completeness and uniqueness are enforced before selection; neither establishes repository identity.

## Severity-rated findings
### High: discovery hints silently authorize an unrelated task update

`src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:148-159` treats arbitrary description/custom-field URL mentions as `github_link`, or a title `#N` token as `title_number`. Lines 200-221 choose a sole candidate after complete pagination; lines 232-238 add the token owner without a task/issue pairing confirmation. A sole `OtherRepo #302` task with a conflicting repository URL still matches the title fallback. A cross-reference to the requested URL also qualifies without an authoritative integration relationship. Consequence: assignment of unrelated work.

### Medium: current tests preserve the unsafe contract

`tests/skills/test_clickup_claim.py:208-239` expects description/custom-field URL matching, and lines 259-274 explicitly expect a sole title token to produce `assigned`. These protect the original design rather than the requested safe behavior. A fix that only improves repository parsing at the CLI boundary would not address these task-selection paths.

## Recommendations and roadmap
1. Stop assignment when identity is known only from a title token or arbitrary URL mention; return an explicit unresolved/confirmation-required result with no PUT.
2. Verify whether a supported reader exposes a native integration relationship with exact repository and issue identity. Do not invent an API field or add a custom field as a substitute.
3. When native evidence is unavailable or ambiguous, require an explicit task ID plus confirmation of that exact GitHub issue/task pairing; reject missing, conflicting or changed evidence.
4. Update the shared selection path once, then its test fixtures, claim invocation/result handling and matching documentation. Preserve existing no-write pagination, multiple-match and request-error behavior.
5. Add mock PUT-count checks for the issue's acceptance matrix; reserve live assignment checks for separate explicit authorization.

## Verification limits
This command is static analysis only: no tests, helper execution, credentials, ClickUp reads or writes, or live integration capability checks. Availability and shape of native integration evidence are UNVERIFIED. Security analysis is limited to the assignment-identity boundary; no whole-project security or performance audit was performed. The helper's current blob is `65b8d643123b2ca19c18925558ec6dd8240cee20`, identical to the issue's cited blob; its sole local history entry is merge commit `6542ca72b145cec1b86eae49eb06d6fac7c7dc67` (PR #373).
