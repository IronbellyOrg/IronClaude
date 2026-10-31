# Refactoring Plan (M-proof-failure)

## Overview

- Base variant: Variant 3 (option C, split by failure class)
- Incorporated variants: Variant 2 (option B), Variant 1 (option A), plus debate resolutions (A-001..A-006, N-001..N-008)
- Planned changes: 12
- Rejected changes: 6
- Overall risk: Medium (the base's three paths are kept; most changes add guards and re-run rules)
- Output: `../M-proof-failure-merged.md` (in the `adversarial/` folder one level up)

## Planned Changes

### Change 1: Fail-closed classifier (resolves X-003, A-001)
- Source: debate, all three advocates (QUALIFY on A-001 with compatible rules)
- Target: new first section "Classify the failure", before the per-class rules
- Integration: insert
- Content:
  - Preflight: `gh api rate_limit` must succeed, or the run is infrastructure.
  - A download counts as complete only on HTTP 2xx with a byte length equal to the asset `size` from the release API. A fetch error, timeout or short download is infrastructure after one in-run retry.
  - A hash mismatch on a complete download is re-downloaded once. A second mismatch is integrity.
  - `gh attestation verify` failing while the preflight succeeded is retried once. A second failure is integrity.
  - Install, index, `tools/list` or print-config drift failing after integrity passed is behaviour.
  - Anything that fits none of these, or fits more than one, is integrity (fail closed).
- Rationale: debate X-003 (75%), A-001 (85%). A false alarm costs one issue; a missed tamper costs every workspace.
- Risk: Low (additive)

### Change 2: Integrity issue contents, assignment, never auto-closed
- Source: V2 (U-001, C-005); debate N-002, N-003
- Target: base "Integrity failure" bullet
- Integration: replace (expand)
- Content: title "codegraph vX.Y.Z: integrity check failed"; body has the run URL, the asset, the expected and actual hash or the attestation output, the commands to reproduce locally, and the idempotency marker; owner assigned. No branch, no PR, no hashes written to any file. The monitor never closes this issue.
- Rationale: C-005 (90%), N-002 (orchestrator), N-003 (majority)
- Risk: Low

### Change 3: Behaviour draft PR details
- Source: base plus V1 (S-002 marker, U-005) plus V2 (report contents) plus debate A-005, A-006, N-004
- Target: base "Behaviour failure" bullet
- Integration: replace (expand)
- Content: the branch `codegraph/bump-vX.Y.Z` is pushed only after integrity passed, so it carries verified hashes. Draft PR title = the PASS-path PR title plus " [proof failed: <stage>]". The body holds the stage, the log tail, the run URL and the reproduce commands. Owner assigned. Label `needs-codegraph-proof` is created with `gh label create --force` and applied in a separate step that cannot fail the run. No separate issue.
- Rationale: C-002 (90%), S-002 (65%), C-006 (80%), A-005 (90%), A-006 and N-004 (majority)
- Risk: Low

### Change 4: Infrastructure escalation (resolves X-002)
- Source: debate C-003, X-002, N-006
- Target: base "Infrastructure failure" bullet
- Integration: append
- Content: keep the neutral handling (`::warning::` plus step summary, retry next schedule). On the 3rd consecutive infra-failed run, open or comment one issue "codegraph monitor: cannot reach upstream" (marker `codegraph-monitor:infra`); the next run that passes the preflight closes it. The counter mechanism is an orchestrator proposal, flagged for the user.
- Rationale: X-002 (80%); `context.md`: "Nobody watches IronClaude Actions run summaries".
- Risk: Medium (needs state across runs)

### Change 5: Idempotency key and re-run rule
- Source: V2 (C-004, U-002), extended by the V1 and V3 advocates; N-005
- Target: new section "Every daily run"
- Integration: insert
- Content: issues are found by an HTML marker `<!-- codegraph-monitor:vX.Y.Z:<class> -->` (class = integrity or infra), not by title. PRs are found by the branch name `codegraph/bump-vX.Y.Z`. Each artifact stores a fingerprint (class, stage, first error line, branch head SHA). The monitor comments only when the fingerprint changed; otherwise the run is a no-op for that artifact.
- Rationale: C-004 (90%), N-005 (majority)
- Risk: Low

### Change 6: Never push to an existing bump branch
- Source: debate A-002, N-001 (V3 advocate's rule; Coder precedent)
- Target: "Every daily run"
- Integration: insert
- Content: if `codegraph/bump-vX.Y.Z` exists on `origin`, the monitor never pushes or force-pushes it. It checks the branch head out, re-runs the proof there and reports by comment.
- Rationale: A-002 (85%); Coder skips when "open PR exists or remote branch exists"
- Risk: Low

### Change 7: Later pass on the same version
- Source: debate A-004, N-003, N-007
- Target: "Every daily run"
- Integration: insert
- Content: an open behaviour draft is marked ready (`gh pr ready`), its label removed and its title marker dropped only when the proof passes at the branch head and that head's `SHA256` table equals the hashes verified in the same run. An earlier integrity issue for the same version stays open; the PASS-path PR body links it.
- Risk: Medium (interaction between the PASS path and open artifacts)

### Change 8: Newer release supersedes older artifacts
- Source: debate A-003, N-002, N-008
- Target: "Every daily run"
- Integration: insert
- Content: an older version's draft PR is closed with "superseded by vN" and a link. Its branch is deleted only if every commit since `master` was made by the workflow bot. An older integrity issue gets a link comment and stays open.
- Risk: Low

### Change 9: Order of operations
- Source: debate (V3 advocate strength 3; spec fact 5 about dispatching `test.yml` on the bump branch)
- Target: new section "Order of operations"
- Integration: insert
- Content: verify (hashes, attestation) -> rewrite the pin in the work tree -> prove in an isolated HOME -> push the branch and open the PR only if integrity passed. Unlike Coder, the branch is not pushed before verification.
- Risk: Low

### Change 10: Permissions
- Source: debate A-005; spec fact 4 (`default_workflow_permissions: read`)
- Target: new section "Permissions"
- Integration: insert
- Content: `contents: write`, `pull-requests: write`, `issues: write`; plus `actions: read` only if the run-history counter in Change 4 is chosen.
- Risk: Low

### Change 11: Tests (number of code paths)
- Source: V3 cost line; V3 advocate strength 5; V2 advocate test list
- Target: new section "Paths to test"
- Integration: insert
- Content: a pure classifier and a pure router (inputs: class, existing artifacts, branch authorship, fingerprint) with table tests and `gh` faked. Name each test case.
- Risk: Low

### Change 12: Items for the user
- Source: orchestrator (N-001, N-002, N-006, N-007 settled by orchestrator; UNVERIFIED items)
- Target: new final section
- Integration: append
- Risk: Low

## Base Weaknesses Addressed

| Issue in base | Better variant | Fix |
|---|---|---|
| Integrity and infra boundary undefined (X-003) | V2 (needs no boundary) | Change 1 fail-closed classifier |
| Infra silent forever (X-002) | none; debate merge | Change 4 escalation |
| No re-run rule (C-004) | V2 | Changes 5, 6, 7, 8 |
| Report lacks run URL and reproduce commands (C-005) | V2 | Changes 2, 3 |
| Draft PR title missing (S-002) | V1 | Change 3 |
| Label assumed to exist (A-005) | debate | Changes 3, 10 |

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001 | V1: integrity failure pushes a branch and opens a draft PR | Unanimous against (95%). The pinned table is the install-time trust anchor (`install_codegraph.py:328-330`), and the repo is public. |
| C-002 | V2: behaviour failure gets an issue only | Unanimous against (90%); the bytes are verified, and a person needs a branch to push a fix onto. |
| N-004 | V2 advocate: behaviour failure gets both an issue and a draft PR | Majority against. One artifact per failure; owner assignment gives the notification. |
| N-005 | V2 advocate: comment on every daily re-run | Majority against; daily duplicate comments are noise. |
| N-001 | V2 advocate: `--force-with-lease` against the bot's last SHA; V1 advocate: push if all commits are the bot's | Orchestrator chose "never push an existing branch": no SHA bookkeeping, and Coder's precedent. |
| N-006 | V1 advocate: open or comment on the infra issue on every infra failure | Majority against; a one-day outage should not notify. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 4 | Medium | Needs a counter across runs; mechanism not verified | Drop escalation, keep neutral exit (base behaviour) |
| 7 | Medium | Wrongly marking a draft ready would remove the hard gate | Guarded by the proof at the head plus the hash equality check; a human still merges |
| all others | Low | Additive rules | Remove the rule |

## Review Status

- Approval: auto-approved (non-interactive)
- Timestamp: 2026-10-30
