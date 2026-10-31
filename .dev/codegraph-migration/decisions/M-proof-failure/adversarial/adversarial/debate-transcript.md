# Adversarial Debate Transcript (M-proof-failure)

## Metadata

- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (18 of 18 diff points)
- Convergence threshold: 80%
- Focus areas: never merging unverified bytes; what a person can do next; idempotency across daily runs; number of code paths to test
- Advocate count: 3
  - Variant 1 (option A, draft PR with a label): default model, persona architect
  - Variant 2 (option B, issue only): default model, persona security
  - Variant 3 (option C, split by failure class): default model, persona qa
- Omissions: none. Every advocate answered A-001..A-006 with ACCEPT, REJECT or QUALIFY.
- Agent failures: none.

## Round 1: Advocate Statements

Full statements are in `round1-advocate-v1.md`, `round1-advocate-v2.md` and `round1-advocate-v3.md` in this folder. Summaries:

### Variant 1 advocate (option A, architect)

- Position: Coder's draft-PR pattern is the right container for behaviour failures but not for integrity failures. Conceded class 1 against its own variant: `install_codegraph.py:328-330` accepts any download that matches the pinned table, so unverified hashes on a branch are one "Ready for review" click from becoming the trust anchor in every workspace.
- Steelman of B: nothing mergeable is ever created; issues certainly notify. Steelman of C: matches the artifact to the next action.
- Concessions: C-001, X-001 to C; idempotency (C-004) and report content (C-005) to B.
- Proposed additions: download-completeness check before hashing; branch name `codegraph/bump-vX.Y.Z` as the PR key; never push to a branch with non-bot commits; create the label with `--force` and apply it non-fatally; assign the owner.

### Variant 2 advocate (option B, security)

- Position: ship C's split, with B's issue as the place failures are tracked. Conceded C-002: on a behaviour failure the bytes have passed hash and attestation, so a fixable draft PR adds no supply-chain risk.
- Steelman of A: one artifact holds diff plus evidence; proven in Coder. Steelman of C: the only variant that satisfies both "no unverified bytes on a branch" and "a diff to push a fix onto".
- Concessions: C-002, S-001 to C.
- Proposed additions: hidden HTML marker as the idempotency key; fail-closed classification; also open an issue for behaviour failures (the only advocate asking for "both"); infra escalation after 3 consecutive failures; `--force-with-lease` against the bot's last pushed SHA.

### Variant 3 advocate (option C, qa)

- Position: C is the only variant that gets both halves right; as written it is incomplete on X-002 (silent infra), X-003 (integrity vs infra boundary) and C-004 (re-runs), and it adopts B's idempotency and report content to close them.
- Steelman of A: proven Coder pattern, one artifact, smallest side-effect surface. Steelman of B: cannot misclassify because it never classifies; only variant with an idempotency rule.
- Concessions: X-002 and X-003 as written; C-004, C-005 and the raw path count (C-007) to B; the draft PR title to A.
- Evidence added: the repo is public (`specs/followup-codegraph-release-monitor-spec.md` fact 4), so a pushed branch with suspect hashes is publicly fetchable; `default_workflow_permissions: read` (same fact), so the workflow must declare write permissions.
- Proposed additions: never push or force-push an existing branch (re-prove its head instead); never auto-close an integrity issue; mark a draft ready only when the proof passes at the branch head and its `SHA256` table equals this run's verified hashes.

### Orchestrator verification of cited evidence

- `src/superclaude/cli/install_codegraph.py:328-330`: confirmed. The download is checked only against the pinned `SHA256` dict; the file contains no `attestation` or `SHA256SUMS` reference.
- `specs/followup-codegraph-release-monitor-spec.md` facts 4 and the Coder source line: confirmed. The repo is public, `default_workflow_permissions: read`, and Coder's monitor is idempotent by branch name with an "open PR exists or remote branch exists" skip.

## Scoring Matrix

Agreement rule: unanimous or at least 2 of 3 advocates choose the same approach.

| Diff Point | Level | V1 adv. | V2 adv. | V3 adv. | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L2 | V3 | V3 | V3 | V3 | 95% | Unanimous; one failure path forces either unverified bytes on a branch or no diff to fix; V1 conceded. |
| S-002 | L1 | V1+V2 | V2+V3 | V1+V3 | merge (V1 PR marker + V3 integrity title) | 65% | Two of three keep V1's "[proof failed]" PR marker; two of three keep V3's distinct integrity title. |
| C-001 | L3 | V3 | V3 (=V2) | V2/V3 | V3 (=V2) | 95% | Unanimous; pinned table is the install-time trust anchor (`install_codegraph.py:328-330`); V1 conceded. |
| C-002 | L2 | V3 | V3 | V1/V3 | V3 (=V1) | 90% | Unanimous; bytes already verified; fixes are repo edits (`MCP_TOOLS`, entry); V2 conceded. |
| C-003 | L3 | V3+esc. | V3+V2 | V3+esc. | V3 plus escalation | 85% | Unanimous that only V3 defines infra and that a lasting outage must reach a person. |
| C-004 | L3 | V2 ext. | V2 | V2 | V2 (extended to PRs) | 90% | Unanimous; only V2 has a re-run rule; V3 conceded. |
| C-005 | L2 | V2 | V2 | V2 | V2 | 90% | Unanimous; run URL plus reproduce commands; V3 conceded. |
| C-006 | L2 | V1/V3+create | V3 | V3 | V3 (label best-effort, created idempotently) | 80% | Unanimous that draft is the gate and the label must not be able to fail the run. |
| C-007 | L2 | V3+helpers | V3 | V2 | V3 | 65% | Majority; V3 advocate conceded the raw count to V2, the other two judged the extra paths worth their cost when built on shared helpers. |
| X-001 | L3 | V3 | V2/V3 | V2/V3 | V2/V3 position | 90% | Unanimous; a draft is one click from mergeable, so suspect bytes must stay off branches. |
| X-002 | L3 | V3+esc. | V2+V3 | V2+V3 | merge (escalate repeated infra failures to one issue) | 80% | Unanimous that silent-forever is wrong; V3 conceded. |
| X-003 | L3 | V3+fail closed | merge fail closed | V2 (as written) | merge (fail-closed classifier) | 75% | Unanimous on the resolution; V3 conceded it is undefined as written. |
| A-001 | L3 | QUALIFY | QUALIFY | QUALIFY | merge (stage plus completeness check, one retry, ambiguous = integrity) | 85% | Unanimous QUALIFY with compatible rules. |
| A-002 | L3 | ACCEPT as rule | QUALIFY | REJECT as assumption | merge (enforced rule: never overwrite non-bot commits) | 85% | Unanimous that it must be an enforced rule; mechanism split 1-1-1 (see N-001). |
| A-003 | L3 | QUALIFY | ACCEPT | QUALIFY | merge (supersede bot-only artifacts) | 75% | Unanimous on bot-only supersede; integrity-issue closing split (see N-002). |
| A-004 | L3 | ACCEPT | QUALIFY | QUALIFY | merge (later pass resolves behaviour artifact; integrity issue stays open) | 75% | Majority (V2, V3) that integrity issues are never auto-closed (see N-003). |
| A-005 | L2 | REJECT | QUALIFY | REJECT | merge (create label, non-fatal, declare permissions) | 90% | Unanimous; the label does not exist and default token permissions are read. |
| A-006 | L2 | QUALIFY | REJECT | QUALIFY | merge (assign the owner on every failure artifact) | 70% | Majority (V1, V3) assign the owner; V2 wanted an extra issue (see N-004). |

Points won, sole or shared, over S, C and X points (X-003 and the A points are merged resolutions with no original-text winner and are not counted): V3 = 9 (S-001, S-002, C-001, C-002, C-003, C-006, C-007, X-001, X-002), V2 = 5 (C-001, C-004, C-005, X-001, X-002), V1 = 2 (S-002, C-002).

### Sub-points settled by majority or by the orchestrator (flag for user review)

| ID | Sub-point | V1 adv. | V2 adv. | V3 adv. | Settled as | How |
|---|---|---|---|---|---|---|
| N-001 | How re-runs avoid clobbering human commits | push only if every commit since `master` is the bot's | `--force-with-lease` against the bot's last pushed SHA | never push to an existing branch; re-prove its head | Never push to an existing `codegraph/bump-vX.Y.Z`; re-prove its head and report | Orchestrator (1-1-1 split): the simplest rule, no SHA bookkeeping, and the same skip Coder uses ("open PR exists or remote branch exists"). |
| N-002 | Does a newer release close an older integrity issue? | close if bot-only | close as superseded | comment, never close | Comment and link; never auto-close | Orchestrator: the V2 advocate's own A-004 answer says integrity issues are not auto-closed, so 2 of 3 positions agree an integrity signal needs a person; also one rule instead of two. |
| N-003 | Same version, earlier integrity failure, later full pass | close issue, ready PR | draft PR, issue stays open | ready PR, link issue, issue stays open | Normal ready PR whose body links the open integrity issue; issue stays open | Majority: ready PR (V1, V3); issue stays open (V2, V3). |
| N-004 | Does a behaviour failure also get an issue ("both")? | no, assign owner | yes, issue plus draft | no, assign owner | No issue; draft PR with the owner assigned | Majority (V1, V3). |
| N-005 | Daily re-run with the same failure | comment only on change | comment every run | comment only on change | Comment only when the failure fingerprint changes | Majority (V1, V3). |
| N-006 | Infra escalation threshold and counter | open/comment on each infra failure | after 3 in a row | after 3 in a row | After 3 consecutive infra-failed runs; counter mechanism proposed by orchestrator | Majority (V2, V3) on the threshold; no advocate gave a counter that works with a neutral exit (see recommendation flags). |
| N-007 | Draft with human commits, later proof passes at its head | remove label, comment, person marks ready | (silent) | mark ready if table equals verified hashes | Mark ready only when the branch head passes the proof and its `SHA256` table equals this run's verified hashes | Orchestrator: V3's guard covers V1's concern (the bytes and behaviour at that exact head are proven) and keeps one path. |
| N-008 | Newer release, older behaviour draft | close, delete bot-only branch | close, delete branch if no human commits | close, keep branches with human commits | Close as superseded with a link; delete the branch only if it has no non-bot commits | Unanimous. |

## Convergence Assessment

- Points resolved: 18 of 18
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage gate: passed (L1 = 1 point, L2 = 7, L3 = 10; all levels debated)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: none. Eight sub-points (N-001..N-008) were settled by majority or by the orchestrator and are flagged for user review.
