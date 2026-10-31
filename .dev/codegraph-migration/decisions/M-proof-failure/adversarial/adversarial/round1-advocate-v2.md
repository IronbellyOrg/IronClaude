# Round 1 advocate: Variant 2 (option B, issue only)

Persona: security (vulnerabilities, attack surface, supply chain). Depth quick, single round.

## Position Summary (1-3 sentences)

A failed proof must never leave a mergeable or one-click-from-mergeable artifact whose pin points at bytes nobody verified, and the owner must hear about every failure through a channel that actually reaches them (issues). Variant 2 gets the security floor and the idempotency rule right; it is wrong to deny a fixable diff on a behaviour failure, where the bytes are already verified, so I would ship Variant 3's split with Variant 2's issue as the single notification and idempotency anchor.

## Steelman of V1

Variant 1 is the only option already proven in production: the Coder monitor pushes the bump branch first, then opens a draft PR with a `needs-build-proof` label on FAIL, and its own comment calls draft "the only hard non-mergeable state available" (`context.md` line 4). One artifact holds both the diff and the evidence, so a reviewer sees exactly what would change and can push a fix (for example an `MCP_TOOLS` edit, `install_codegraph.py` line 35) without re-running anything. It has one failure path, which is the cheapest to test (C-007), and the `[proof failed]` title marker (U-005) visibly separates it from routine work. A human always merges and there is no auto-merge (`M-major-versions/context.md` line 5), so the draft really is gated by a person.

## Steelman of V3

Variant 3 matches the artifact to what a person can actually do next (U-003). On an integrity failure there is no code fix, only investigation, so it opens an issue and keeps unverified hashes off every branch. On a behaviour failure the hashes and attestation already passed, so the bytes are trustworthy and the only open question is compatibility; a draft PR gives the reviewer a diff to push an `MCP_TOOLS` or registration-entry fix onto, which Variant 2 cannot. It is also the only variant that defines the infrastructure path at all (U-004), copying Coder's neutral exit so a GitHub outage does not page anyone. It is the only variant that satisfies both focus areas "never merging unverified bytes" and "what a person can do next" at once.

## Strengths Claimed (numbered, with evidence)

1. **The pin is the install-time trust anchor, so unverified hashes on any branch are a loaded gun.** `install_codegraph.py` lines 28-33 hold the 4-entry `SHA256` table; lines 328-330 accept any tarball whose digest equals that table entry; line 361 then tells the user "installed codegraph {VERSION} (SHA-256 verified)". Whatever hashes a failed-integrity branch carries become, once merged, the definition of "verified". On a mismatch the monitor can only write either the SHA256SUMS value (which does not match the tarball) or the computed tarball digest (which upstream did not vouch for, or which failed attestation). Both are unverified. Variant 2 writes neither anywhere: "No branch, no PR" (`variant-2-original.md` line 3).
2. **Nothing one click from mergeable is ever created from failed bytes.** A draft becomes mergeable after one "Ready for review" click, and a merged pin "flows to every Coder workspace through Coder's IronClaude SHA bump" (`M-major-versions/context.md` line 5; diff-analysis X-001). Variant 2's rationale "nothing mergeable is ever created from failed or unverified bytes" (`variant-2-original.md` line 4) holds by construction, not by a reviewer's attention.
3. **Issues reach the owner; that is a verified fact.** "Nobody watches IronClaude Actions run summaries; issue and PR notifications reach the owner" (`context.md` line 4). Draft PR notification parity is UNVERIFIED (A-006). Variant 2 relies only on the verified channel.
4. **It is the only variant with an idempotency rule.** "Open (or comment on, idempotently by title) one issue" (`variant-2-original.md` line 3; diff-analysis U-002, rated High, and C-004). Daily runs append a comment instead of spawning duplicates.
5. **Reproduce commands and run URL make the report actionable without the workflow** (U-001, C-005). A person can rerun the proof locally in the isolated-HOME setup without reading YAML.
6. **No label dependency.** IronClaude has no `needs-codegraph-proof` label (`context.md` line 4); Variant 2 needs none, so it cannot fail on a missing label (A-005).
7. **Smallest write surface on the failure path.** The failure path needs `issues: write` only: no push, no branch, no PR. That removes the A-002 hazard (clobbering human commits) entirely for every failure class.

## Weaknesses Identified in Others (numbered, with evidence)

1. **V1 puts unverified hashes on a branch on integrity failure.** Its own cost line: "an integrity failure (possible tampering) still pushes a branch whose pin points at unverified bytes; the draft looks like routine work in the PR list" (`variant-1-original.md` line 6). Combined with Strength 1, a single habitual "Ready for review" plus merge turns a tamper signal into a "SHA-256 verified" install on every workspace.
2. **V1 offers the wrong next action for integrity.** A draft PR invites pushing commits; there is no commit that fixes tampering or a re-uploaded asset. The right next step is investigation (compare SHA256SUMS, attestation output, upstream release history), which is an issue's job.
3. **V1 and V3 never say what the next daily run does to an existing branch or PR** (C-004, A-002). A naive re-push or force-push erases the human fix Variant 3 exists to allow.
4. **V3's infrastructure path is silent forever when the failure is persistent** (X-002). An expired token, a changed API or a broken `gh attestation` produces neutral exits that nobody sees, because nobody watches run summaries (`context.md` line 4). From a security view that is a disabled monitor with no alarm, and the pin quietly ages past security fixes upstream.
5. **V3's integrity/infrastructure boundary is undefined** (X-003). A truncated download yields a hash mismatch; `gh attestation verify` exits non-zero when the API is unreachable. If ambiguity resolves toward "infra", a real tamper event becomes a silent neutral exit. That is the worst possible misclassification.
6. **V1 and V3 depend on a label that does not exist** (`context.md` line 4; A-005). `gh pr create --label` with a missing label can fail the step, so the failure report itself can fail.
7. **V1 and V3 assume draft PRs notify like issues** (A-006). Drafts do not request reviews until marked ready; whether this owner gets a notification for a bot-opened draft is UNVERIFIED. An unseen draft is a silent failure.

## Concessions

1. **C-002, behaviour failure: Variant 3 wins.** On a behaviour failure, hashes matched SHA256SUMS and attestation passed, so the branch carries verified bytes. My security objection does not apply there, and Variant 2's cost line is real: "the reviewer has no diff to inspect or push fixes onto (for example a needed `MCP_TOOLS` change); they must re-run the script by hand" (`variant-2-original.md` line 5). A human still merges, so a draft for class 2 adds no supply-chain risk.
2. **C-003 and S-001: Variant 3 wins.** Variant 2 is silent on infrastructure failure; Variant 3 at least defines it.
3. **My idempotency key is flawed.** Keying by title "codegraph vX.Y.Z bump failed: <stage>" breaks when the stage changes between runs (download on day 1, tools/list on day 2) and produces two issues for one version. The key must be the version only, with the stage in the body and comments, plus a hidden marker so title edits by a human do not break the search.
4. **Least privilege is weaker than claimed.** The PASS path needs `contents: write` and `pull-requests: write` anyway, so unless failure reporting runs in a separate job, job-level permissions are the same for all variants.
5. **C-007: one path is cheaper, but the saving is false economy.** Three paths are justified because each class has a different correct next action.

## Shared Assumptions (A-001..A-006, each ACCEPT/REJECT/QUALIFY + reason)

- **A-001 QUALIFY.** Classification is possible but not free; the rule must fail closed: anything ambiguous between integrity and infrastructure is treated as integrity. Rule: before verifying, run an API reachability preflight; a download counts as infra only on an HTTP error, timeout or byte count short of Content-Length; a complete download with a wrong digest is integrity; `gh attestation verify` failing while the preflight succeeded is integrity.
- **A-002 QUALIFY.** It is false by default and must be enforced. Rule: push the bump branch only if it does not exist or its head is the SHA the bot last pushed (recorded in the issue marker), using `--force-with-lease=<branch>:<last-bot-sha>`; otherwise do not touch it and comment "branch has human commits; not updated".
- **A-003 ACCEPT.** Rule: when a newer release is seen, close the older version's failure issue with "superseded by vX.Y.Z" and close its draft PR and delete its branch only if the branch has no human commits; otherwise comment and leave both for the human.
- **A-004 QUALIFY.** Auto-resolve only behaviour failures. Rule: a later PASS on the same version closes a behaviour issue with a link to the ready PR. A version that once failed integrity and later passes (assets changed under the same tag) must not auto-close; open the PR as draft, link the integrity issue, and leave the issue for a human to close.
- **A-005 QUALIFY.** The label does not exist today. Rule: draft is the hard gate and the label is best-effort, so either create it idempotently (`gh label create needs-codegraph-proof --force`) before use or omit it; never let a label failure fail the report. Permissions: `contents: write`, `pull-requests: write`, `issues: write`, no more.
- **A-006 REJECT.** Unverified for this owner, and drafts do not send review requests until marked ready. Rule: never rely on a draft PR alone to notify; every failure that needs a human has an issue, and the issue links the draft.

## Per-Point Verdicts

| Point | Superior approach | Confidence % | One-line reason |
|---|---|---|---|
| S-001 | V3 | 85 | Each class has a different safe next action; one path cannot fit all three. |
| S-002 | merge of V2+V3 | 70 | Title keyed by version only ("codegraph vX.Y.Z: proof failed (<class>)"); stage goes in the body. |
| C-001 | V3 (same as V2) | 95 | Unverified hashes become the install-time trust anchor (`install_codegraph.py` 328-330); keep them off branches. |
| C-002 | V3 | 80 | Bytes are verified on a behaviour failure, so a fixable draft adds value with no supply-chain risk. |
| C-003 | merge of V3+V2 | 80 | Neutral exit for transient outages, but escalate to an issue when it persists. |
| C-004 | V2 | 85 | Only V2 states a rule; fix its key to version-only plus a hidden marker. |
| C-005 | V2 | 80 | Run URL and local reproduce commands make any artifact actionable. |
| C-006 | V3 | 60 | Label is useful on the draft but must be created idempotently or skipped; draft is the real gate. |
| C-007 | V3 | 70 | Three paths cost more tests but each guards a distinct failure mode. |
| X-001 | V2 (= V3) | 90 | A draft is one click from mergeable; it is not a safe container for unverified bytes. |
| X-002 | merge of V3+V2 | 80 | Persistent infra failure disables the monitor silently; escalate to an issue after 3 consecutive runs. |
| X-003 | merge (fail closed) | 75 | Ambiguous integrity vs infra is treated as integrity; a false alarm costs one issue, a miss costs a tamper. |
| A-001 | QUALIFY | 75 | Detectable with a preflight and fail-closed classification. |
| A-002 | QUALIFY | 85 | Enforce with force-with-lease against the bot's last SHA. |
| A-003 | ACCEPT | 80 | Supersede older artifacts, sparing branches with human commits. |
| A-004 | QUALIFY | 75 | Auto-close behaviour issues on pass; never auto-close integrity issues. |
| A-005 | QUALIFY | 80 | Label missing today; create idempotently or omit. |
| A-006 | REJECT | 70 | Unverified; anchor notification on issues. |

## Proposed Merged Rule (the rule you would ship if forced to merge; bullets)

- **One tracking issue per version is the anchor for every class.** Title "codegraph vX.Y.Z: proof failed (<class>)", hidden body marker `<!-- codegraph-monitor:vX.Y.Z -->`, found by marker; daily reruns comment (run URL, stage, log tail, reproduce commands) instead of opening duplicates.
- **Class 1 integrity:** issue only. No branch, no PR, no hashes written anywhere. Ambiguous integrity vs infra is classified as integrity (fail closed).
- **Class 2 behaviour:** issue plus a DRAFT PR titled "codegraph vX.Y.Z bump [proof failed: <stage>]", label `needs-codegraph-proof` created idempotently (best-effort), issue links the draft. Push only if the branch is absent or its head is the bot's last SHA (`--force-with-lease`); otherwise comment and leave it.
- **Class 3 infrastructure:** neutral exit, step summary, `::warning::`. After 3 consecutive infra runs, open or comment the issue "codegraph monitor: infrastructure failing".
- **Later pass, same version:** behaviour issue closes with a link to the ready PR. After a prior integrity failure, open the PR as draft, link the issue, leave it for a human.
- **Newer release:** close the older issue as superseded; close the older draft and delete its branch only if it has no human commits.
- **Tests:** PASS, integrity, behaviour, infra-transient, infra-escalation, rerun-dedup, human-commit guard, supersede.
