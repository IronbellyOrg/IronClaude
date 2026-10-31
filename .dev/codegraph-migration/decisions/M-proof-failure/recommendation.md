# M-proof-failure recommendation: what a failed codegraph proof produces

- Decision: on a failed proof (class 1 integrity, class 2 behaviour), does the release monitor open a draft PR, an issue, or both? (context: `context.md`)
- Method: `/sc:adversarial --compare option-a.md,option-b.md,option-c.md --depth quick`
- Status: success (all 5 steps ran; post-merge validation PASS). Four sub-points settled by the orchestrator and four UNVERIFIED items are flagged for the user.

## Winner

**Option C** (split by failure class) won as the base. The merged rule adds B's re-run rule and report contents, and A's title marker. The answer to the question is: **never both**. An integrity failure gets an issue. A behaviour failure gets a draft PR.

Why: `src/superclaude/cli/install_codegraph.py:328-330` checks a download only against the pinned `SHA256` table; the installer has no attestation or SHA256SUMS check. So the pin is the only trust anchor in every workspace, and the repo is public. Hashes that failed verification must never sit on a branch, even in a draft one click from mergeable. That rules out A for integrity failures. A behaviour failure happens after hashes and attestation passed, so its bytes are verified, and the fix is usually a repo edit (`MCP_TOOLS`, the registration entry). That rules out B's issue-only rule for behaviour failures. The A and B advocates both conceded these points.

## The rule an implementer must follow

The monitor classifies every failure fail closed, then produces exactly one artifact per class. It finds that artifact again on later daily runs by a fixed key and acts only when the failure fingerprint changed. It never pushes to a bump branch that already exists, and it never closes an integrity issue.

- **Classify (fail closed).**
  - `gh api rate_limit` failing, or a download that is still short or erroring after one retry: infrastructure.
  - A complete download (HTTP 2xx, byte length equal to the release API asset `size`) whose hash mismatches twice: integrity.
  - `gh attestation verify` failing twice while the preflight succeeded: integrity.
  - Install, index, `tools/list` or print-config drift failing after integrity passed: behaviour.
  - Anything ambiguous: integrity.
- **Integrity failure: issue only.**
  - No branch, no PR, no hash written anywhere.
  - Title `codegraph vX.Y.Z: integrity check failed`. No label.
  - Body: run URL, asset, expected and actual hash or the attestation output, commands to reproduce locally. Owner assigned.
  - The monitor never closes it; only a person does.
- **Behaviour failure: draft PR only, no issue.**
  - The branch `codegraph/bump-vX.Y.Z` is pushed only after integrity passed, so it carries verified hashes.
  - Title: the PASS-path PR title plus ` [proof failed: <stage>]`.
  - Label `needs-codegraph-proof`: created with `gh label create --force` and applied in a step that cannot fail the run. The draft state is the gate; the label is best effort.
  - Body: stage, log tail, run URL, reproduce commands. Owner assigned.
- **Infrastructure failure.**
  - Each run writes a `::warning::` and a step summary.
  - On the 3rd consecutive infra-failed run, the monitor opens or comments one issue titled `codegraph monitor: cannot reach upstream`. No label.
  - The first run that passes the preflight closes that issue.
- **Idempotency key.**
  - Issues are found by an HTML marker, never by title: `<!-- codegraph-monitor:vX.Y.Z:integrity -->` or `<!-- codegraph-monitor:infra -->`.
  - PRs are found by the branch name `codegraph/bump-vX.Y.Z`.
  - Each artifact stores a fingerprint: class, stage, first error line and branch head SHA. The monitor comments only when the fingerprint changed; otherwise the run is a no-op.
- **Existing branch.** If `codegraph/bump-vX.Y.Z` exists, the monitor never pushes or force-pushes it. It re-proves the branch head and reports by comment.
- **Later pass on the same version.**
  - A behaviour draft is marked ready, and its label and title marker are removed, only if the proof passes at the branch head and that head's `SHA256` table equals the hashes verified in the same run. If the table differs, the PR stays draft and gets a comment.
  - An open integrity issue stays open, and the PASS PR links it.
- **Newer release.**
  - An older draft is closed as "superseded by vN". Its branch is deleted only if every commit since `master` is the bot's.
  - An older integrity issue gets a link comment and stays open.
- **Order.** Verify, rewrite the pin, prove, then push and open the PR. Unlike Coder, the branch is never pushed before verification.
- **Permissions.** `contents: write`, `pull-requests: write`, `issues: write`. Add `actions: read` if counter Option 1 is chosen.
- **Tests.** There are four terminal outcomes (ready PR, integrity issue, behaviour draft PR, infrastructure warning or escalation issue). A pure classifier and a pure router are tested with `gh` faked: 9 classifier cases and 15 router cases, listed in section 9 of the merged file.

## Scores per option

| Option | Quantitative (50%) | Qualitative (50%, 30-criterion rubric, two passes) | Combined | Debate points won |
|---|---|---|---|---|
| B | 0.854 | 20/30 = 0.667 | **0.760** | 5 |
| C | 0.929 | 17/30 = 0.567 | **0.748** | 9 |
| A | 0.778 | 13/30 = 0.433 | **0.606** | 2 |

B and C are 0.012 apart, inside the 5% tie band. The level-1 tiebreaker (debate points won: C 9, B 5) selected C. The level-2 tiebreaker (correctness criteria) would have tied at 5 against 5. B's rubric lead comes from its card stating a re-run rule and a notification channel. The merge adds both to C, so B's lead does not argue for dropping the behaviour draft PR, and B's own advocate conceded that point. The two rubric passes disagreed on 11 criterion-variant pairs; each was re-scored (`adversarial/adversarial/base-selection.md`).

## Convergence

100% (18 of 18 diff points), status CONVERGED, threshold 80%. Depth was quick, so the debate had one round and no invariant probe. All three advocates chose C's split (S-001, unanimous) and rejected A's integrity draft (C-001, unanimous). Eight sub-points were settled by majority or by the orchestrator (N-001 to N-008 in `adversarial/adversarial/debate-transcript.md`).

## Items flagged for the user

1. **N-001 (orchestrator, 1-1-1 split):** the monitor never pushes to an existing bump branch. This was chosen over `--force-with-lease` against the bot's last SHA, and over "push if every commit is the bot's". It is the simplest rule and matches Coder's "open PR exists or remote branch exists" skip.
2. **N-002 (orchestrator):** an integrity issue is never auto-closed, not by a later pass and not by a newer release.
3. **N-006, counter mechanism (proposal, UNVERIFIED):** two options.
   - Option 1: an infra-failed run ends with a failed job conclusion, and an `if: failure()` step counts 3 failed runs in a row with `gh run list --workflow <file> --limit 3 --json conclusion`. This departs from Coder's neutral exit, and any 3 failing runs in a row escalate.
   - Option 2: keep the neutral exit and store the counter in a small run artifact.
4. **N-007 (orchestrator):** a draft that has human commits is marked ready automatically when the proof passes at its head and its table equals the verified hashes. A person still merges.
5. **Assignee login:** the repo owner is an organisation, so there is no single owner login. Suggestion: a repository variable holding the login.
6. **UNVERIFIED:** whether a draft PR, and an assignment made by the workflow token, notify this owner. Verify on the first real failure.
7. **UNVERIFIED:** how `gh label create --force` and `gh run list --json conclusion` behave with the workflow token. Check with `--help` and a dry run.
8. **Interaction with M-major-versions:** if that decision also produces draft PRs or issues for majors, titles and labels must keep "major review" and "proof failed" apart.

## Paths

- Merged rule: `.dev/codegraph-migration/decisions/M-proof-failure/adversarial/M-proof-failure-merged.md`
- Process artifacts: `.dev/codegraph-migration/decisions/M-proof-failure/adversarial/adversarial/`. This folder holds the variant copies, `diff-analysis.md`, three `round1-advocate-v*.md`, `debate-transcript.md`, `rubric-pass2-reverse.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` and `return-contract.yaml`.
