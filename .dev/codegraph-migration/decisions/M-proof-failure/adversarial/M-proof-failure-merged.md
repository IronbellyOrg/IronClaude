<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (option C, split by failure class) -->
<!-- Merge date: 2026-10-30 -->

# M-proof-failure merged rule: what a failed codegraph proof produces

## 1 Summary

<!-- Source: Base (original, modified) - rule and rationale kept; summary table added from Changes 2, 3, 4 and 5 -->

The monitor sorts every failed proof into one of three classes and gives each class the artifact that matches what a person can do next. An integrity failure (possible tampering) gets an issue only, so unverified hashes never reach a branch. A behaviour failure gets a draft PR on a branch that carries verified hashes, so a person can push a fix onto it. An infrastructure failure stays quiet until it lasts three runs in a row, then opens one issue. Every daily run finds its earlier artifacts by a fixed key and acts only when something changed.

| Failure class | Artifact | Title | Label | Idempotency key |
|---|---|---|---|---|
| Integrity | Issue only. No branch, no PR. Owner assigned. | `codegraph vX.Y.Z: integrity check failed` | none | HTML marker `<!-- codegraph-monitor:vX.Y.Z:integrity -->` |
| Behaviour | Draft PR on `codegraph/bump-vX.Y.Z`. Owner assigned. No issue. | PASS-path PR title plus ` [proof failed: <stage>]` | `needs-codegraph-proof` (best effort) | Branch name `codegraph/bump-vX.Y.Z` |
| Infrastructure (after 3 consecutive runs) | Runs 1 and 2: `::warning::` and step summary only. Run 3: one issue, opened or commented. | `codegraph monitor: cannot reach upstream` | none | HTML marker `<!-- codegraph-monitor:infra -->` |
| PASS (for contrast) | Ready PR on `codegraph/bump-vX.Y.Z` | Title per the PASS path | none | Branch name `codegraph/bump-vX.Y.Z` |

Rationale (base): this matches the artifact to what a person can do next and keeps unverified bytes off branches. Cost (base): more paths to test than option A or B. Section 9 lists them.

## 2 Classify the failure

<!-- Source: Variants 1, 2 and 3 (all three advocates, debate X-003, A-001), merged per Change #1 -->

The classifier is fail closed. When in doubt, the result is integrity. A false alarm costs one issue. A missed tamper costs every workspace.

1. Preflight. `gh api rate_limit` must succeed. If it fails, the run is infrastructure.
2. Download completeness. A download counts as complete only on HTTP 2xx with a byte length equal to the asset `size` from the release API. A fetch error, a timeout or a short download is retried once in the same run. If it fails again, the run is infrastructure.
3. Hash check. A hash mismatch on a complete download is re-downloaded once. A second mismatch is integrity.
4. Attestation. If `gh attestation verify` fails while the preflight succeeded, it is retried once. A second failure is integrity.
5. Proof stages. Install, index, `tools/list` or the print-config drift check failing after integrity passed is behaviour.
6. Anything else. A result that fits none of these rules, or fits more than one, is integrity.

## 3 Integrity failure

<!-- Source: Base (original, modified) - expanded per Change #2 from Variant 2 (option B, U-001, C-005) and debate N-002, N-003 -->

Applies to a hash mismatch or an attestation failure, as decided in section 2.

- Artifact: one issue. No branch, no PR. No hash is written to any file.
- Title: `codegraph vX.Y.Z: integrity check failed`.
- Body:
  - the run URL;
  - the asset name;
  - the expected and the actual hash, or the attestation output;
  - the commands to reproduce the check locally;
  - the idempotency marker `<!-- codegraph-monitor:vX.Y.Z:integrity -->` and the fingerprint (section 6).
- The owner is assigned.
- The monitor never closes this issue. Only a person closes it. This holds on a later pass (section 6) and on a newer release (section 6).
- Rationale (base): a mismatch may be tampering. The pinned table is the install-time trust anchor, and the repo is public, so suspect hashes must never sit on a branch.

## 4 Behaviour failure

<!-- Source: Base (original, modified) - expanded per Change #3 from Variant 1 (option A, S-002, U-005), Variant 2 (option B, report contents) and debate A-005, A-006, N-004 -->

Applies when install, index, `tools/list` or the print-config drift check fails after integrity passed.

- Branch: `codegraph/bump-vX.Y.Z` is pushed only after integrity passed, so it carries verified hashes. If the branch already exists, it is not pushed (section 6).
- Artifact: a DRAFT PR. Draft is the hard non-mergeable state. No separate issue.
- Title: the PASS-path PR title plus ` [proof failed: <stage>]`.
- Body:
  - the failed stage;
  - the log tail;
  - the run URL;
  - the commands to reproduce the proof locally;
  - the fingerprint (section 6).
- The owner is assigned. Assignment gives the notification.
- Label: `needs-codegraph-proof`. It is created with `gh label create --force` and applied in a separate step that cannot fail the run. The label is best effort. The draft state is the gate.
- Purpose (base): a person can push a fix onto the branch, for example an `MCP_TOOLS` or entry change.

## 5 Infrastructure failure

<!-- Source: Base (original, modified) - escalation appended per Change #4 from debate C-003, X-002, N-006 -->

Applies when the preflight fails or a download stays incomplete after its retry (section 2).

- Every infra-failed run writes a `::warning::` and a step summary. The next schedule retries. No hash is used and nothing is pushed. This is the base behaviour and matches Coder.
- Escalation: on the 3rd consecutive infra-failed run, the monitor opens or comments one issue titled `codegraph monitor: cannot reach upstream`, with the marker `<!-- codegraph-monitor:infra -->`. The marker has no version because the version may be unknown when upstream is unreachable.
- Recovery: the first run that passes the preflight closes the infra issue. This is the only issue the monitor closes on its own.
- Reason for escalation: nobody watches IronClaude Actions run summaries (`context.md`), so a lasting outage must reach a person.

### Counter mechanism (proposal, UNVERIFIED, user decides)

<!-- Source: Variant 2 (option B advocate threshold) and orchestrator proposal (debate N-006), merged per Change #4 -->

- Option 1 (default): an infra-failed run still writes the `::warning::` and step summary but ends with a failed job conclusion. An `if: failure()` step counts the consecutive failed runs with `gh run list --workflow <monitor workflow file> --limit 3 --json conclusion`. This needs `actions: read`. It opens or comments the infra issue when the current run and the two before it all failed. The current run is still in progress when the step runs, so its own failure is known from `if: failure()` and the two entries before it supply the rest (UNVERIFIED). Side effect: any 3 consecutive failing runs escalate, including script bugs.
- Option 2: keep Coder's neutral (successful) exit, and keep a counter in a small uploaded run artifact that the next run downloads.
- Option 1 departs from Coder's neutral exit. The base rule above ("neutral exit") holds only if Option 2 is chosen.

## 6 Every daily run: idempotency, existing branch, later pass, newer release

<!-- Source: Variant 2 (option B, C-004, U-002) and Variant 3 (option C advocate, debate A-002, A-003, A-004, N-001..N-008), merged per Changes #5, #6, #7, #8 -->

### 6.1 Idempotency key and re-run rule

<!-- Source: Variant 2 (option B, C-004, U-002), extended by debate N-005, merged per Change #5 -->

- Issues are found by their HTML marker, never by title:
  - integrity: `<!-- codegraph-monitor:vX.Y.Z:integrity -->`;
  - infrastructure: `<!-- codegraph-monitor:infra -->` (section 5).
- PRs are found by the branch name `codegraph/bump-vX.Y.Z`.
- Each artifact stores a fingerprint: class, stage, first error line, and branch head SHA (empty for an integrity issue, which has no branch).
- The monitor comments only when the fingerprint changed. Otherwise the run is a no-op for that artifact.

### 6.2 Never push to an existing bump branch

<!-- Source: Variant 3 (option C advocate rule, debate A-002, N-001, Coder precedent), merged per Change #6 -->

- If `codegraph/bump-vX.Y.Z` exists on `origin`, the monitor never pushes or force-pushes it.
- It checks the branch head out, re-runs the proof there and reports by comment (subject to 6.1).
- Changing the PR state (`gh pr ready`, label, title) is not a push and is allowed under 6.3.
- Deleting a superseded branch under 6.4 is a ref deletion, not a content push, and is the only write the monitor makes to an existing branch.

### 6.3 Later pass on the same version

<!-- Source: Variant 3 (option C advocate guard, debate A-004, N-003, N-007), merged per Change #7 -->

- An open behaviour draft is marked ready (`gh pr ready`), its label removed and its title marker dropped only when both are true:
  - the proof passes at the branch head; and
  - that head's `SHA256` table equals the hashes verified in the same run.
- If the proof passes but the table is not equal, the PR stays draft and gets a comment. The monitor does not push a corrected table (6.2). A person fixes it.
- This applies even when the branch has human commits (N-007, flagged in section 10).
- An earlier integrity issue for the same version stays open. The PASS-path PR body links it.
- A person still merges. Marking ready does not merge.

### 6.4 Newer release supersedes older artifacts

<!-- Source: Variants 1, 2 and 3 (debate A-003, N-002, N-008), merged per Change #8 -->

- An older version's draft PR is closed with the comment "superseded by vN" and a link.
- Its branch is deleted only if every commit since `master` was made by the workflow bot. A branch with any human commit is kept.
- An older integrity issue gets a link comment and stays open (section 3).

## 7 Order of operations

<!-- Source: Variant 3 (option C advocate strength 3, spec fact 5), merged per Change #9 -->

1. Verify: hashes and attestation (section 2).
2. Rewrite the pin in the work tree.
3. Prove in an isolated HOME.
4. Push the branch and open the PR only if integrity passed, and only if the branch does not already exist (6.2).

Unlike Coder, the branch is not pushed before verification.

## 8 Permissions

<!-- Source: Variants 1, 2 and 3 (debate A-005, spec fact 4 `default_workflow_permissions: read`), merged per Change #10 -->

The repository default token is read only, so the workflow declares:

- `contents: write`
- `pull-requests: write`
- `issues: write`
- `actions: read`, only if Option 1 of the counter mechanism (section 5) is chosen.

## 9 Paths to test

<!-- Source: Base (original, modified) - cost line expanded with Variant 2 (option B advocate test list), merged per Change #11 -->

There are four terminal outcomes:

1. PASS: ready PR.
2. Integrity: issue.
3. Behaviour: draft PR.
4. Infrastructure: warning, or the escalation issue on the 3rd consecutive run.

They are driven by a pure classifier and a pure router. The router inputs are the class, the existing artifacts, the branch authorship and the fingerprint. Both are tested with named table cases, with `gh` faked.

### 9.1 Classifier cases

<!-- Source: Variants 1, 2 and 3 (classifier rules), merged per Changes #1, #11 -->

| Case | Expected |
|---|---|
| complete download and matching hash | pass |
| short download | infrastructure |
| HTTP error | infrastructure |
| mismatch, then match on re-download | pass |
| mismatch twice | integrity |
| attestation fails twice with preflight OK | integrity |
| preflight fails | infrastructure |
| ambiguous input | integrity |
| proof stage failure after integrity passed | behaviour |

### 9.2 Router cases

<!-- Source: Variants 2 and 3 (router rules), merged per Changes #2 to #8, #11 -->

| Case | Expected |
|---|---|
| integrity, no issue | opens one issue |
| integrity, issue with the same fingerprint | no-op |
| integrity, issue with a changed fingerprint | comments |
| behaviour, no branch | pushes the branch and opens a draft PR |
| behaviour, existing branch | never pushes; re-proves the head |
| later pass, hash table equal | marks ready |
| later pass, hash table unequal | stays draft and comments |
| newer release, bot-only draft | closes the draft and deletes its branch |
| newer release, branch with human commits | closes the draft and keeps the branch |
| newer release, older integrity issue | comments and keeps the issue open |
| infra runs 1 and 2 | open nothing |
| infra run 3 | opens or comments the infra issue |
| first run passing the preflight | closes the infra issue |
| label creation fails | run does not fail |
| PASS while an integrity issue is open | PR body links the issue |

## 10 Items for the user

<!-- Source: Variants 1, 2 and 3 (orchestrator-settled N-001, N-002, N-006, N-007 and UNVERIFIED items), merged per Change #12 -->

1. N-001: never push an existing branch. Chosen over `--force-with-lease` against the bot's last SHA and over "push if all commits are the bot's". Settled by the orchestrator on a 1-1-1 split.
2. N-002: integrity issues are never auto-closed, not even by a newer release. Settled by the orchestrator.
3. N-006: the counter mechanism for infra escalation. Option 1 (failed conclusion plus `gh run list`) or Option 2 (neutral exit plus a run artifact counter). See section 5.
4. N-007: a draft that has human commits is marked ready automatically when the proof passes at its head and its table equals the verified hashes. Settled by the orchestrator.
5. Which login to assign. The repo owner is an organisation, so there is no single owner login. Suggestion: a repository variable that holds the assignee login.
6. UNVERIFIED: whether a draft PR notifies the assignee, and whether assignment sends a notification for this owner. Verify on the first real failure.
7. UNVERIFIED: how `gh label create --force` and `gh run list --json conclusion` behave with the workflow token. Check with `--help` and a dry run.
8. Interaction with decision M-major-versions: if major versions also produce draft PRs or issues, the title and label must keep the two meanings apart.

## 11 Rejected alternatives

<!-- Source: Base (original, modified) - records the rejected non-base positions from refactor-plan.md "Changes NOT Being Made" -->

- C-001 (V1): integrity failure pushes a branch and opens a draft PR. Rejected: the pinned table is the trust anchor and the repo is public.
- C-002 (V2): behaviour failure gets an issue only. Rejected: the bytes are verified and a person needs a branch to fix.
- N-004 (V2 advocate): behaviour failure gets both an issue and a draft PR. Rejected: one artifact per failure; assignment notifies.
- N-005 (V2 advocate): comment on every daily re-run. Rejected: daily duplicate comments are noise.
- N-001 (V2 and V1 advocates): `--force-with-lease`, or push when all commits are the bot's. Rejected: no SHA bookkeeping; Coder's skip precedent.
- N-006 (V1 advocate): open or comment the infra issue on every infra failure. Rejected: a one-day outage should not notify.
