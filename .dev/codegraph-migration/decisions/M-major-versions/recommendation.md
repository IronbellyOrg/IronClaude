# Recommendation: M-a, do major codegraph versions bump automatically?

- Decision: when the candidate's major number is higher than the pin's (1.x to 2.0.0), what does the monitor do?
- Method: `/sc:adversarial --compare option-a.md,option-b.md,option-c.md --depth quick --output .dev/codegraph-migration/decisions/M-major-versions/adversarial --focus "safety of Phase 3 skills that call codegraph tools,reviewer burden,code paths to test,fit with the user's rule that a human merges"` (Round 1 only; Round 2 and the invariant probe are skipped at quick depth)
- Status: DONE, converged (pipeline status: success, 1 unresolved point flagged below)
- Date: 2026-10-30
- Artifacts: `adversarial/merged-output.md` (merged rule), `adversarial/adversarial/` (diff-analysis, debate-transcript, base-selection, refactor-plan, merge-log, return-contract)

## Winner

Option C (majors get the full automated PR, always as a draft), merged with B's candidate selection, idempotency and link-only notes, and A's single code path.

## Merged rule an implementer must follow

The monitor runs the same verify, rewrite and proof for a new major as for a minor, but always opens the major PR as a draft, even when the proof passes. Release candidates are chosen per major, so 1.x patches keep arriving as ready PRs while a 2.0 draft waits. A human works through the checklist, marks the draft ready and merges it, or closes it to decline. Nothing merges automatically.

- **Tag parsing:** only `vMAJOR.MINOR.PATCH` tags (digits only) count. Prerelease and malformed tags are skipped and the reason is logged.
- **Two candidates per run:** (1) the newest stable release within the pinned major goes to the normal ready-PR path on a passed proof; (2) if a stable release with a higher major exists, the newest one becomes the major candidate. One run can produce both.
- **Major path:** same hashes, `gh attestation verify`, rewrite and isolated-HOME proof. Draft PR always. The body contains the proof log, hashes, the attestation result, a link to the release notes (not the notes text; v1.6.2 notes are 76,281 characters), and a checklist: read the breaking changes; check the Phase 3 skills that call codegraph tools.
- **Title:** `codegraph MAJOR vX.Y.Z: manual review`. The title is the signal. Apply the `codegraph-major` label only if it exists (IronClaude has none today and labels are best-effort).
- **Idempotency:** one fixed branch per target major (for example `codegraph-major-v2`), and likewise one for the within-major bump. Each run rebuilds the branch from current master and updates the existing open PR; it never opens a second one. The rebuild also clears the conflict that appears after a 1.x patch merges.
- **Declined major:** if a person closes the major draft without merging, later runs do not reopen it for that same version; a newer release of that major (for example 2.0.1) opens a draft again.
- **Single pipeline:** one shared code path; the draft flag and title are the only differences. No `--allow-major` manual route.
- **Failed proof:** on either path, follow the M-proof-failure decision, using a title that differs from the `codegraph MAJOR` prefix.
- **Required tests:** major gives a draft even on a passing proof; within-major gives a ready PR; a second run updates and does not duplicate; a prerelease tag is skipped; a 1.x patch still gives a ready PR while a 2.0 draft is open; a closed-unmerged major draft is not reopened for the same version.

## Scores per option

| Option | Quantitative (50%) | Qualitative (50%, out of 30) | Combined | Debate points won |
|--------|--------------------|------------------------------|----------|-------------------|
| A: majors bump like minors (ready PR) | 0.862 | 16 (0.533) | 0.697 | 1 of 14 |
| B: issue only, manual bump | 0.898 | 23 (0.767) | 0.832 | 4 of 14 |
| C: full PR, always draft | 0.984 | 23 (0.767) | **0.875** | **5 of 14** |

C led B by 4.3%. That is under the 5% tie margin, so the tiebreaker on debate points won decided it (5 to 4). A was last: its claim that "the proof plus the human merge is the review" contradicts the verified fact that the proof does not check tool arguments or output format, and its own advocate conceded the point.

## Convergence

- 92.9% (13 of 14 points), threshold 80%: CONVERGED. All three taxonomy levels were covered, and no advocate failed.
- All three advocates, including A's and B's, independently proposed the same merge: C as the base plus B's within-major selection and idempotency.
- Unresolved point C-002: B's "no PR at all" is the stronger barrier, and C's draft is the hard non-mergeable state that keeps the evidence attached. C won because automating the bump beat a manual rerun unanimously (X-002).
- Limits: quick depth means one round and no invariant probe. The two scoring passes were run by the orchestrator in-context, not by independent agents.

## Items flagged for the user

1. **Barrier strength (C-002):** do you accept a draft PR as the gate for majors, or do you want B's stricter rule of no PR until a person asks? The merged rule assumes the draft.
2. **Declined majors:** the rule never reopens a closed-unmerged major draft for the same version. No option stated this; the orchestrator added it to stop repeat drafts on every scheduled run.
3. **Malformed tags:** skipped and logged only. Nobody watches Actions run summaries, so a malformed tag goes unnoticed. The alternative is to open an issue.
4. **Minor releases can also break Phase 3 skills:** codegraph has a single maintainer and its semver discipline is unverified. The proof does not check tool semantics on any path. All three advocates suggested the minor PR body say so. This was left out as outside this decision's scope.
5. **Coordination with M-proof-failure:** if that decision uses draft PRs for failed proofs, its titles must differ from `codegraph MAJOR`. Choose the two titles together.
6. **Unverified:** the GitHub PR body size limit was not checked. Linking the release notes avoids depending on it.
