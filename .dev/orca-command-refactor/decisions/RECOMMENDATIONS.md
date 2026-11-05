# Recommendations on open decisions D1-D5 (worker-contract spec)

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited `SPEC:N`). Decisions are the spec's section 9 (`SPEC:325-354`). Defect IDs from the final diff review are written FDR-D1 to FDR-D7 to keep them apart.
Method: per decision, one position file per option under `.dev/orca-command-refactor/decisions/D<n>/`, then `/sc:adversarial --compare <option files> --depth standard --output .dev/orca-command-refactor/decisions/D<n>/debate`. The original debates were cut off by a restart at about 16:28 UTC on 2026-11-02; each was resumed from its Step 1-3 artifacts on disk (Steps 1-3 not redone) and finished with Steps 4-5.
Status: COMPLETE. This file is an index and summary; each decision's full recommendation, plain-language section and exact spec wording are in `decisions/D<n>/RECOMMENDATION.md`, and the merged positions in `decisions/D<n>/debate/adversarial/merged-output.md`.

## Assumptions
- Fixed constraints applied to every debate as user decisions, not debate points: worktrees are created by Orca at Orca's default paths, never `.dev/worktrees/`; SuperClaude upstream is never pushed to or interacted with; merged PR #343 (only blocking findings fail a review, loops cap at 2 fix cycles); proposed change CR-01 (`changes/CR-01-feature-worktree-hierarchy.md`, feature worktree with conditional child worktrees).
- Every debate ended `BLOCKED_BY_INVARIANTS` on high-severity gaps; the gaps were closed by planned changes in Step 4, not argued in a debate round, which is why each recommendation states medium confidence on its details.
- Every return contract is `partial`. None of the new rules has run live.

## D1. How a command knows it runs without a person
- **Recommended: (c), which extends the spec's (a).** The `--unattended` flag stays the only switch; from Phase 1 the worker session also checks its brief's command lines before running anything and refuses with a named reason (`guard refused: ...`) when they do not fit. Detection (b) stays rejected. Full text: `D1/RECOMMENDATION.md`.
- **Confidence:** high on the choice; medium on the guard's rules (5 high-severity fixes merged by plan; one review of the fixes, not rechecked).
- **In practice:** nothing changes for a person in their own terminal. A wrongly written worker job fails at once with a reason instead of stalling silently while Orca shows it healthy.
- **Spec edits:** W1-W16 in `D1/debate/adversarial/merged-output.md`. W14 overlaps CR-01's rewrite of the live-check worktree (`SPEC:235`) and must be merged with it.

## D2. Who may give a Ruling when /sc:implement halts inside a worker
- **Recommended: (a) plus (c); agrees with the spec and extends it.** Only the person gives a Ruling: resume in their own session (default, and the only route for a dispute halt), or type the Ruling line into the ledger themselves, after which the coordinator checks it read-only and restarts. The coordinator never relays a Ruling ((b) rejected). Full text: `D2/RECOMMENDATION.md`.
- **Confidence:** high on "no relay"; medium on adding (c).
- **Needed regardless:** a coordinator no-retry/freeze rule. Today `SPEC:84` lets the coordinator retry a failed Task; for a Ruling-halted plan that retry would start an operator review by automation, which the protocol forbids (`D2/RECOMMENDATION.md:15`).

## D3. Whether /sc:pr-submit runs as an Orca worker
- **Recommended: (a), amended; the decision matches the spec, the wording changes.** `/sc:pr-submit` is not a worker. Each PR's run happens in one ordinary top-level session in that PR's own child worktree, started only when the person names that PR; several PRs means several sessions. Worker-per-PR (b) is deferred, not rejected. Full text: `D3/RECOMMENDATION.md`.
- **Confidence:** about 90% on the decision, about 70% on who carries the session.
- **"Attended" answered:** in pr-submit's text it means "not detached", not "a person watching" (`SKILL.md:43-45`); a terminal worker qualifies, a chat-surface worker is UNVERIFIED.

## D4. Whether a coordinator's brief may authorize a worker's outward actions (and worker commits)
- **Recommended: (c′); overturns the spec's (a).** No worker does anything that leaves the machine; the coordinator does every push, PR, comment, install and paid run, on `IronbellyOrg/IronClaude` only. Full text: `D4/RECOMMENDATION.md`.
- **Worker commits:** opt-in only. One `git commit --only -- <paths>` at the end of a succeeded Task, when the brief quotes the user's request word for word and the worker is alone in its own Orca child worktree; never a push, never `--no-verify`. Otherwise no commits.
- **Confidence:** high on direction (32 of 32 points agreed); medium on details (`base-selection.md` has 11 unfinished sections; rules not run).

## D5. Whether to raise Orca's nesting depth
- **Recommended: (a), keep depth 1; agrees with the spec.** The spec's reasons and wording are corrected: no setting lets commands call Orca, and the "mechanical backstop" is presumed, not traced. Adds a precondition (the coordinator must be a session the person opened), rule WC-13, and checks AC-0.7 and AC-C6. Full text: `D5/RECOMMENDATION.md`.
- **Confidence:** high (0.827 against 0.694); medium on the safeguards until Phase 0 reads Orca's code.

## How the decisions interact
- **D4 and git ownership agree** (`git-ownership/RECOMMENDATION.md`, option E, 75%): only the coordinator acts outward; workers commit locally only under a quoted grant in their own child worktree. Git ownership adopted D4's wording on the five points where they differed.
- **D3 vs git ownership: one open conflict.** Git ownership keeps an opt-in pr-submit worker per PR (only under D3 (b)) and has the coordinator run pr-submit from the PR-head checkout; D3 rules out the worker and uses a separate session per PR. Under the recommended D3 (a) the opt-in never runs, but the "who runs it" wording must be unified.
- **CR-01 is the placement model for D2, D3, D4 and git ownership**, but it does not say whether a PR comes from the feature branch or from a child worktree's own branch (D3).
- **D2 and CR-01:** a halted `/sc:implement` freezes its worktree; running each implement in its own child avoids freezing the shared feature worktree.
- **D1 and D5** are consistent with all of the above: the flag turns on worker refusals; depth 1 means no worker starts workers.
- **D4 and the `.dev/tasks` rule:** git ownership leaves `.dev/tasks` staging to the coordinator in worker sessions, which interprets the repo's "always staged" rule (`CLAUDE.md:37`); the user must confirm that interpretation.

## Self-Audit
Checked: each `D<n>/RECOMMENDATION.md` and `git-ownership/RECOMMENDATION.md` section 1-3 read directly before summarizing; the git-ownership section 6 comparison against D4; that every per-decision file carries the fixed constraints. Not checked: the citations inside the per-decision files (each had its own citation review), and the merged outputs' spec edits line by line. This summary adds no claims beyond those files.
