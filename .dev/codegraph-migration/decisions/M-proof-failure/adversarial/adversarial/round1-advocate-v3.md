# Round 1 advocate: Variant 3 (option C, split by failure class)

Persona: qa (edge cases, test coverage, failure scenarios). Depth quick, single round.

## Position Summary (1-3 sentences)

The right artifact depends on whether the bytes were verified: an integrity failure means the hashes cannot be trusted, so it gets an issue and no branch; a behaviour failure means the bytes are verified but the proof broke, so it gets a draft PR a person can push a fix onto. Variant 3 is the only variant that gets both halves right, but as written it is incomplete on infrastructure escalation (X-002), the integrity/infrastructure boundary (X-003) and re-run idempotency (C-004), and I adopt Variant 2's idempotency and report content to close those gaps.

## Steelman of V1

V1 (draft PR with a label) has the strongest real-world evidence of the three: it is the pattern the Coder monitor already runs (`context.md` line 4: "pushes the bump branch first, then opens a ... DRAFT PR with a `needs-build-proof` label on FAIL"). One artifact holds both the diff and the evidence, so the reviewer reads the failure and the change in one place. Draft is, in Coder's own words, "the only hard non-mergeable state available", and a human always merges (`M-major-versions/context.md` line 5), so no bytes reach `master` without a person acting. It has one failure path, which is the smallest GitHub side-effect surface that still gives the reviewer a diff. The "[proof failed]" title marker (U-005) makes the draft visibly different from routine work. For behaviour failures, V1 is exactly right, and V3 copies it.

## Steelman of V2

V2 (issue only) is the simplest safe rule: "nothing mergeable is ever created from failed or unverified bytes" (`option-b.md` line 4). It cannot be wrong about classification because it never classifies: every failure takes the same path, so A-001 and X-003 do not exist for it. Issues reach the owner (`context.md` line 4: "issue and PR notifications reach the owner"), need no new label, and need no `contents: write` on the failure path. It is the only variant with an idempotency rule ("Open (or comment on, idempotently by title) one issue", U-002) and the only one that tells the reader how to act without opening the workflow: run URL plus exact commands to reproduce (U-001). On integrity failures V2 and V3 are identical, and V2 got there with less code.

## Strengths Claimed (numbered, with evidence)

1. **The pinned table is the only integrity anchor in every workspace, so unverified hashes must never sit on a branch.** At install time the installer trusts whatever is in the table: `got = hashlib.sha256(archive.read_bytes()).hexdigest()` / `if got != SHA256[asset]: return _fail("checksum", ...)` (`src/superclaude/cli/install_codegraph.py:328-330`), against the literal table at `:28-33`. If a branch carries the hashes of tampered bytes and is merged, the install check passes for the tampered bytes, and "A merged pin flows to every Coder workspace" (`M-major-versions/context.md` line 5). On an attestation failure the SHA256SUMS file itself may be attacker-controlled, so any hash the monitor writes is untrusted. V3 and V2 keep these bytes off branches; V1 pushes them (its own cost line: "still pushes a branch whose pin points at unverified bytes").
2. **The repo is public, so a pushed branch is a public, checkout-able pin.** The follow-up spec records "The repo is public, default branch `master`" (`specs/followup-codegraph-release-monitor-spec.md` line 25). Under V1, an integrity failure publishes a commit whose `SHA256` table names suspect bytes, reachable by anyone who fetches the branch. A draft state does not hide a branch.
3. **Behaviour failures carry verified bytes, so a draft PR is safe and useful there.** Class 2 only runs after hashes and attestation pass (`M-major-versions/context.md` line 3: download, check hashes, attestation, then rewrite and prove). The likely fixes are small source edits a person can push onto the branch, for example `MCP_TOOLS = "node,search,callers,callees,impact,files,status"` (`install_codegraph.py:35`) when upstream renames a tool, or the registration entry when `--print-config` drifts. V2 forces that person to "re-run the script by hand" (`option-b.md` line 5) and rebuild the diff locally. V3 gives them the diff.
4. **V3 is the only variant that defines infrastructure at all (C-003, U-004).** V1 and V2 are silent, which leaves an implementer to guess whether an API outage opens a draft PR, an issue, or crashes. A guess here is the most frequent path in practice (daily schedule, flaky network), so leaving it undefined is the largest untested surface.
5. **The extra path is cheap to test because routing is a pure decision table.** The class is decided by which stage failed (fetch, verify, prove) plus a small evidence record, and the artifact router is a function of (class, existing artifacts). Both can be table-tested with `gh` faked, the same way the installer tests fake one network function (`_download` is "the one network fake", spec line 17). The GitHub side effects are three calls (issue, draft PR, warning), not three independent programs.

## Weaknesses Identified in Others (numbered, with evidence)

1. **V1 treats a possible tamper as routine work.** "Integrity failures (class 1) are treated the same way" (`option-a.md` line 4). The draft is one "Ready for review" click from mergeable (X-001), it "looks like routine work in the PR list" (V1's own cost), and the hashes it pins are the exact thing the installer will later trust (`install_codegraph.py:329`). V1's safety claim is a UI state, not a property of the bytes.
2. **V1 depends on a label that does not exist and a mechanism Coder calls best-effort.** IronClaude's labels are "bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix" (`context.md` line 4); Coder calls its label "best-effort". If `gh pr create --label needs-codegraph-proof` fails on a missing label, V1's only failure path fails (A-005). V3 shares this risk on the behaviour path, so I fix it in the merged rule rather than claim immunity.
3. **V1 and V2 both say nothing about infrastructure.** Neither variant mentions class 3, so both inherit X-002 by omission: a persistent token, API or `gh attestation` breakage is undefined and, in practice, silent, because "Nobody watches IronClaude Actions run summaries" (`context.md` line 4).
4. **V2 throws away the most useful thing on a behaviour failure: the diff.** The monitor already rewrote `VERSION` and the four-entry `SHA256` table (`install_codegraph.py:26-33`) with verified hashes. V2 discards that work and asks the reviewer to redo it locally, then open their own PR, which is a second chance for a hand-copied hash error.
5. **V2 conflates "the release is suspect" with "the release changed shape".** A single issue title "bump failed: <stage>" gives a possible tamper and a renamed MCP tool the same visual weight. A reviewer triaging by title cannot tell a security event from a chore.
6. **V1 has no idempotency rule (C-004).** A daily schedule with "push the bump branch" and no rule about existing branches either opens a duplicate PR daily or force-pushes over any human fix. V3 as written has the same gap (conceded below).

## Concessions

- **X-002 (infrastructure never reaches a person): V3 as written is wrong.** "no issue (retries next schedule)" plus "Nobody watches IronClaude Actions run summaries" means an expired token or a changed API is silent forever. V1 and V2 are no better (they say nothing), so no variant wins this point; the merged rule below adds escalation after repeated failures.
- **X-003 (integrity vs infrastructure boundary): V3 as written is undefined.** A truncated download produces a hash mismatch, and `gh attestation verify` exits non-zero when the API is unreachable. V2 wins this point on the original texts, because it never needs the boundary. V3 can only keep its advantage with an explicit, fail-closed classification rule (below).
- **C-004 idempotency: V2 wins.** V2 is the only variant with a rule. V3 adopts it.
- **C-005 report content: V2 wins.** Run URL and reproduce commands (U-001) belong in every failure artifact, including V3's issue and draft PR.
- **S-002 titles: V3 omitted the draft PR title.** V1's "[proof failed]" marker is the better PR title; V3 adopts it.
- **C-007 path count: V2 is cheaper.** V3 adds real test cost (classification, two artifact types, infra escalation). I argue the cost buys C-001 and C-002, but on the raw count V2 wins.
- **Draft PR notification (A-006) is unverified for this owner.** V3 relies on the draft being seen as much as V1 does.

## Shared Assumptions (A-001..A-006, each ACCEPT/REJECT/QUALIFY + reason)

- **A-001 (failure class is detectable at runtime): QUALIFY.** Detectable by stage plus evidence, not by exit codes alone; rule: infrastructure only when the failure is provably transport (HTTP error, timeout, byte count short of the API asset `size`, or `gh api rate_limit` unreachable when attestation fails), each retried once in-run; any remaining hash or attestation failure, or anything ambiguous, is integrity (fail closed: a false alarm costs one issue, a missed tamper costs every workspace).
- **A-002 (re-runs never clobber human commits): REJECT as an assumption, it must be an enforced rule.** Rule: the monitor never force-pushes; if `codegraph/bump-vX.Y.Z` already exists it does not push at all, it re-proves the branch head and only comments or marks ready.
- **A-003 (newer release supersedes older artifacts): QUALIFY.** Rule: an older behaviour draft is closed with a "superseded by vN" comment (branch deleted only if it holds no non-bot commits); an older integrity issue is commented on but never auto-closed, because a past tamper signal still needs a human to explain it.
- **A-004 (same-version later pass resolves the artifact): QUALIFY.** Rule: a behaviour draft is marked ready only when the proof passes at the branch head and the branch's `SHA256` table equals the hashes verified in that same run; an integrity issue is never auto-closed on a later pass, since assets changing under the same tag is itself suspicious; the monitor comments, opens the normal PR, and links the two.
- **A-005 (label and permissions in place): REJECT as an assumption.** The label does not exist (`context.md` line 4) and `default_workflow_permissions: read` (spec line 25); rule: the workflow declares `contents: write`, `pull-requests: write`, `issues: write`, creates the label idempotently before use, and applies it after PR creation as a best-effort step that cannot fail the run.
- **A-006 (draft PRs notify like ready PRs): QUALIFY (UNVERIFIED).** Do not rely on it; rule: assign the owner on every failure artifact (`--assignee` from a repo variable) so the notification comes from assignment, and verify once on the first real run.

## Per-Point Verdicts

| Point | Superior approach | Confidence % | One-line reason |
|---|---|---|---|
| S-001 | V3 | 85 | Integrity and behaviour need different artifacts and infra must be defined; one path forces one of them to be wrong. |
| S-002 | merge of V1+V3 | 70 | Use V1's "[proof failed]" PR marker and V3's distinct "integrity check failed" issue title. |
| C-001 | V2/V3 (tie) | 95 | The pinned table is the only install-time anchor (`install_codegraph.py:328-330`); suspect hashes must not be on a public branch. |
| C-002 | V1/V3 (tie) | 85 | Bytes are verified; the fix is a small source edit a person can push onto the draft. |
| C-003 | V3 (with X-002 fix) | 75 | Only variant that defines infra; neutral-forever must gain escalation. |
| C-004 | V2 | 80 | Only variant with an idempotency rule; extend it to the draft PR. |
| C-005 | V2 | 80 | Run URL plus reproduce commands make any artifact actionable. |
| C-006 | V3 | 65 | Label only on the draft; the draft is the real gate and the label is best-effort. |
| C-007 | V2 | 70 | Fewest paths; V3's extra cost is justified elsewhere but V2 wins the count. |
| X-001 | V2/V3 (tie) | 85 | A draft is one click from mergeable; only keeping suspect bytes off branches is safe. |
| X-002 | merge of V2+V3 | 70 | None handles it; escalate repeated infra failures to one tracking issue. |
| X-003 | V2 (on original texts) | 65 | V2 needs no boundary; V3 regains the point only with a fail-closed classifier. |
| A-001 | merge of V2+V3 | 70 | Classify by stage, retry transport once, default ambiguous to integrity. |
| A-002 | merge of V2+V3 | 80 | Never force-push; existing branch means re-prove and comment only. |
| A-003 | merge of V2+V3 | 65 | Supersede old drafts; never auto-close an integrity issue. |
| A-004 | merge of V2+V3 | 65 | Ready only on pass at branch head with matching verified hashes. |
| A-005 | V2 | 70 | Fewest permissions and no label; V3 must create the label and make it non-fatal. |
| A-006 | V2 | 60 | Issue notification is a stated fact; draft notification is unverified, so assign the owner. |

## Proposed Merged Rule (the rule you would ship if forced to merge; bullets)

- **Classify by stage, fail closed.** Fetch/download failures (HTTP error, timeout, size short of the API asset `size`) and attestation failures while `gh api rate_limit` is unreachable are infrastructure, each after one in-run retry. Any other hash or attestation failure, or anything ambiguous, is integrity. Install, index, `tools/list` or drift failures are behaviour.
- **Integrity: issue only, no branch, no PR.** Title "codegraph vX.Y.Z: integrity check failed"; body has the asset, expected and got hashes or attestation error, run URL and local reproduce commands; owner assigned. Never auto-closed.
- **Behaviour: push `codegraph/bump-vX.Y.Z` once, open a DRAFT PR** titled "codegraph vX.Y.Z [proof failed]: <stage>", owner assigned, label `needs-codegraph-proof` added best-effort, body with stage, log tail, run URL, reproduce commands.
- **Infrastructure: exit with `::warning::` and step summary.** After 3 consecutive infra runs, open or comment one issue "codegraph monitor: cannot reach upstream"; close it on the next run that reaches the API.
- **Idempotency key: version plus class**, found by an HTML marker in the artifact body. Next daily run: comment only if the stage, error or branch head changed; otherwise no-op.
- **Existing branch: never push or force-push.** Re-prove the branch head; on pass with a `SHA256` table equal to this run's verified hashes, mark ready and comment.
- **Newer release:** close older drafts as superseded (keep branches with non-bot commits); comment on, never close, older integrity issues.
- **Permissions:** `contents`, `pull-requests`, `issues: write`; label created idempotently before use.
- **Tests:** classifier table, router table (class by existing artifact state), human-commit branch guard, label-missing tolerance, infra escalation counter.
