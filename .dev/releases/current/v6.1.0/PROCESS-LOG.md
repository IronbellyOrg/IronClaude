# Process log (6.1.0)

One entry per step, with times and what should change. The 6.0.0 log is `../v6.0.0/PROCESS-LOG.md`.

## Entries

### 1. Assignment and records (2026-11-18 20:57Z to 20:59Z)
- **Step:** GeneralIronFlow relayed Clay's approval ("approved, merge in the proper order, then do the release the same way"; the user also told me to act on it): merge #650, #653, #656, #657 into `integration` in that order with the 6.0.0 rule, then run the 6.1.0 release exactly as 6.0.0 and stop for Clay's final yes before the release PR merges. Created this folder.
- **State found:** #650 targets `integration` and is DIRTY (its own checks green on `e79c8bb80`, Codex completed, the one Augment thread resolved). #653, #656 and #657 are stacked (each targets the previous branch) and CLEAN against their own base. `master` is one merge commit ahead of `integration` (6.0.0). The bundle agent `ic61-part-b-bundle` is rebasing #650.
- **Applied from the 6.0.0 retrospective:** section 1 of `RELEASE-READINESS.md` lists every dependency of the release with an owner or "not in this release". Two items are open for Clay: #641 (gate G9) and the post-release scope.

### 2. Clay added #641 to 6.1.0 (2026-11-18 21:00Z)
- **Step:** GeneralIronFlow relayed Clay's yes for #641 (20:59Z) and merged it into `master` as `89dc403d4` (checked on GitHub: MERGED 20:59:54Z). Post-release scope confirmed as 6.0.0's.
- **Consequence found:** #641 put its changelog entry under `[Unreleased]` on `master`, and #657 cuts the `[6.1.0]` section, so the two edit the same lines. Plan: merge `master` into `integration` after #650 (not while the bundle agent is rebasing #650), then have the agent rebase #653, #656 and #657 onto it; #657 moves the entry into `[6.1.0]` and adds the three user-visible points to the release notes (message sent to the bundle agent).
- **Change next time:** when a pull request is added to a release late, say at once which release files it edits (here the changelog).
