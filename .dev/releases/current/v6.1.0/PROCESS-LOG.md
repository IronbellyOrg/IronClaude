# Process log (6.1.0)

One entry per step, with times and what should change. The 6.0.0 log is `../v6.0.0/PROCESS-LOG.md`.

## Entries

### 1. Assignment and records (2026-11-18 20:57Z to 20:59Z)
- **Step:** GeneralIronFlow relayed Clay's approval ("approved, merge in the proper order, then do the release the same way"; the user also told me to act on it): merge #650, #653, #656, #657 into `integration` in that order with the 6.0.0 rule, then run the 6.1.0 release exactly as 6.0.0 and stop for Clay's final yes before the release PR merges. Created this folder.
- **State found:** #650 targets `integration` and is DIRTY (its own checks green on `e79c8bb80`, Codex completed, the one Augment thread resolved). #653, #656 and #657 are stacked (each targets the previous branch) and CLEAN against their own base. `master` is one merge commit ahead of `integration` (6.0.0). The bundle agent `ic61-part-b-bundle` is rebasing #650.
- **Applied from the 6.0.0 retrospective:** section 1 of `RELEASE-READINESS.md` lists every dependency of the release with an owner or "not in this release". Two items are open for Clay: #641 (gate G9) and the post-release scope.
