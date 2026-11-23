# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (maximum for depth standard; Round 2.5 invariant probe is run by another agent and is not part of this file)
- Convergence achieved: 87.9% (51 of 58 diff points; see Convergence Assessment for the counting rule and two alternative counts)
- Convergence threshold: 80%
- Focus areas: fit to the nine CONTEXT.md questions, AI-agent parallelism, CI and review load, ref-name conflicts, rollback
- Advocate count: 4
- Mode: A (`--compare`), four variants. Source of diff ids: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261123-branching-strategy/adversarial/diff-analysis.md`
- Assembled: 2026-11-23, from `round1-advocate-1.md` to `round1-advocate-4.md` and `round2-advocate-1.md` to `round2-advocate-4.md` in the same folder

### Advocate key
| Advocate | Variant | Persona | Variant title |
|----------|---------|---------|---------------|
| adv-1 (A1) | V1 | architect | release line with story branches (owner's model) |
| adv-2 (A2) | V2 | analyzer | trunk based, dark landing into `integration` |
| adv-3 (A3) | V3 | backend | release train, PR-gated batch |
| adv-4 (A4) | V4 | qa | GFxAI approach adapted |

### Citation style used by the advocates
A1-W2 = advocate 1 Round 1 weakness 2; A3-S2 = advocate 3 strength 2; A4-C1 = advocate 4 concession 1; A1R2-6 = advocate 1 Round 2 section 1 point 6; N, E, M numbers are the Round 2 evidence items of advocates 2, 3 and 4. R1-S, R1-C, R1-E = an advocate's own Round 1 strength, concession, evidence item.

## Round 1: Advocate Statements

### Variant 1 Advocate (adv-1, architect persona)
**Position**: V1 is the only proposal whose base line has a single writer (the coordinator), whose rollback unit is one merge commit on `master`, and which needs no new repository configuration, no new owner decision and no unverified bot behaviour before the first story can start. Its real weakness is that nothing but the coordinator's local suite looks at the code until one release-sized pull request; the advocate says this is bounded by a story-count cap and a one-week limit.

**Steelman of the other variants**:
- V2: research points one way (S1 two-day branches, S6 DORA one-week batch limit, S8 Fowler); CI plus both bots on every small slice (C-007); CI on the real `integration` is "the strongest guard" (C-011); no `test.yml` edit; Clay's habit scaled up (Q8); finest rollback grain down to flag-off (C-022); no long-lived branch (C-013).
- V3: keeps batch isolation and still gives every story CI and both reviewers, so the roll-up is "mostly an integration check"; names its costs (Open decisions A, B, C; U-012); time-boxed train with floating scope (U-010); throwaway test PR (U-013); follows the documented flow `master <- integration <- feature`; `dash1.3-sync<N>` branch (U-011).
- V4: only proposal with evidence from a real team (GFxAI layout side by side, C-001); PR #147 size warning (U-015); provenance marks (U-014); "AI Agent: Merge to Main no" (U-017); squash gives one commit per story (C-005); full tier gate at the release PR (U-018).

**Key strengths claimed**:
1. Single writer on the base line: only the coordinator moves `dash1.3/release`; serial merges by construction (S21; V1 Q2 versus V2 Q2).
2. Maps one to one onto the worker contract (CONTEXT line 9); fewest dependencies (C-006).
3. Zero changes outside the branch layout: no `test.yml` edit, no ruleset entry, no bot-behaviour assumption (A-012), no auto-delete setting; its five UNVERIFIED items are lookups, not changes (C-007, A-008, A-013).
4. Smallest owner and CI load per release: one PR, one CI run, one bot pass, one click (CONTEXT line 16; A-003).
5. Blast radius contained until the end; V2 itself lists `integration` going red as risk 3.
6. The release is one revertable unit on `master` and Clay's work is not inside it (V1 Q3; V2 Q9; V3 C-018).
7. Honours the owner's stated model and the ledger convention (CONTEXT lines 7 and 14; C-002, C-003, C-020, X-009).
8. No back-port step for hotfixes (V1 Q6; C-015).
9. The right guards for AI parallelism, cheaply: `git merge-tree` trial merge (U-001), path claims against open `integration` PRs (U-003), per-story digest in the release PR body (U-002).
10. Story-level merge commits keep the AI audit trail; squash (V2, V4) loses the per-task trail.
11. Naming: `git branch --list 'dash1.3/*'` shows one release and its stories (U-004); the advocate does not claim this beats flat names.

**Weaknesses identified in the others**:
- V2:
  1. The owner is the single merge lane (V2 section 5, risk 1; CONTEXT line 16; C-004, A-003; S19).
  2. No home for the progress ledger (V2 Q7; C-020).
  3. Dark landing is unproven in this code (V2 Q5; U-009; S20, risk 6).
  4. Shipping is coupled to Clay's state (V2 Q4; C-018; X-003; risks 3 and 4).
  5. Whole-release rollback is worse than it looks: the promotion revert also removes Clay's work (C-022).
  6. Duplicated review: V2 Q4 "the second review is mostly duplicated effort".
- V3:
  7. Asks for everything V1 asks plus three owner decisions (A, B, C) before story one (C-006, C-007, A-013, A-014).
  8. Per-story CI and review rest on unverified third parties (V3 risks 5 and 6; A-008, A-011, A-012).
  9. Stacks are weak: CI does not run on a PR whose base is a story branch (X-010).
  10. Couples the release to the promotion cadence and inherits red state at the cut (V3 risks 3 and 4; Q3; C-008).
  11. Moves the owner's planning base to `integration` (V3 Q8; X-009).
  12. Landing in `integration` departs from the owner's model (C-003, X-002).
- V4:
  13. Contradicts itself on `integration`: Q8 "does not pass through" versus Q3 merging `integration` in (X-003, X-008, A-017).
  14. Contradicts itself on when CI runs (X-008).
  15. Most of what V4 adds to V1 is the part with the weakest fit (PR per story, squash, merging `integration` in); the rest is documentation.
  16. Evidence base thinner than it looks: draft "Pending team review", "no rollback rule", "no flag policy", rebase-only reversed (C-009, X-007); PR #147 argues against "Weeks-months".
  17. Three-level names add ref-conflict surface (C-001).

**Concessions**:
1. Review size is V1's worst risk and the evidence is against it (S6, S19, PR #147); the story-count cap, digest (U-002) and split after about a week are mitigations, not a cure. C-021 goes against V1.
2. Nothing outside the coordinator's local suite sees the code until the end; C-007 and C-011 detection latency go against V1.
3. Finest rollback grain belongs to V2 (C-022).
4. Flat names (V2, V3) are more robust than V1's folder names; C-001 is a tie at best.
5. V1 bypasses `integration`, the documented flow in CLAUDE.md; collisions with Clay show late at the sync PR.
6. V1 is the most coordinator-dependent proposal (A-002).
7. V3's time-boxed floating scope (U-010) is better than V1's justification; also U-013, U-012 and U-014 are better practice.
8. Squash gives simpler single-parent reverts (C-005).
9. A `dash/1.3` tag could be ambiguous with a branch of that name; would accept a hyphen (C-024).
10. The long-lived branch is justified only by the owner's model and a hard time cap; if the cap cannot be kept, fall back to V3.

**Shared assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 QUALIFY; A-006 QUALIFY; A-007 QUALIFY; A-008 ACCEPT; A-009 QUALIFY; A-010 QUALIFY; A-011 ACCEPT; A-012 ACCEPT; A-013 ACCEPT; A-014 QUALIFY; A-015 QUALIFY; A-016 QUALIFY; A-017 REJECT (false by git mechanics).

**Diff points claimed**:
- Wins: C-002 and X-001; C-003 and X-002; C-008, X-003, A-017; C-018; C-020 and X-009; C-015; C-009 and X-007; C-005 and X-004 (contested); C-004, C-006, X-005 (contested); C-022 at release level; U-001, U-002, U-003.
- Draws or contested: C-001; C-010; C-011 (split); C-012, C-013, X-006 (wins against V2, loses to V3's time box; should adopt U-010); C-014, C-016, C-017, C-019, C-023, C-025 (no meaningful difference).
- Losses accepted: C-007; C-021; X-008 (no point either way); C-024; U-006 to U-009; U-010 to U-013; U-014, U-015, U-018 (worth importing).

### Variant 2 Advocate (adv-2, analyzer persona)
**Position**: V2 is the only proposal in which every unit of AI work is checked by CI and both automatic reviewers against the real shared line, on a small diff, with no workflow edit, no new merge authority and no long-lived branch to keep current. The advocate states its price: the owner clicks merge on every slice and the ledger convention (CONTEXT line 14) has no branch to live on. Claims wins on CI and review fit, collision-detection latency, rollback granularity, ref-name robustness and flow; concedes owner effort, the ledger and isolation from Clay.

**Steelman of the other variants**:
- V1: the owner's own model made precise (CONTEXT line 7); changes nothing (no workflow edit, setting or merge authority); one owner decision per release; `--no-ff` keeps a story boundary for `git revert -m 1`; `git merge-tree` trial merge (U-001) and path-claim comparison (U-003); keeps Clay's unreleased work out of the release PR (C-018, X-003); honest about its weak point; respects owner merge capacity (A-003).
- V3: best of the three alternatives; keeps the batch and still gives each story CI and both reviewers; keeps ledger and `.dev/` on a branch (C-020); time-boxed floating scope (U-010); `dash1.3-sync<N>` (U-011); open decisions A, B, C (U-012); throwaway test PR (U-013); lands on `integration`, Clay's lane.
- V4: only evidence from the owner's own organisation; provenance marks (U-014); real-history evidence (U-015: PR #147, 34 commits, 1,384 files, +242,976 lines, six stale `backup/...` branches, stale `release/v0.1`); "AI Agent: Merge to Main no" (U-017); full release gate (U-018); beta freeze; `hotfix/` prefix; lowers adoption friction.

**Key strengths claimed**:
1. Every unit gets CI and both reviewers against the real shared line with zero configuration change: slices open with `--base integration`, which already triggers (C-007; CONTEXT line 11; V2 Q2).
2. The CI trigger cannot be silently disabled by the Orca prefix because the `pull_request` filter matches the base branch (V3 risk 5; A-011; S11).
3. Shortest collision-detection latency: the collision shows as a red check on the causing PR against the real `integration` (C-011).
4. Finest rollback unit and cheapest rollback: one squash commit per slice, flag-off for dark features (C-005, C-022, Q9).
5. Ref-name robustness by construction: a flat name is a leaf with no folder part (C-001); V1 risk 4 and V4's folder dependence are exposed.
6. Smallest batch, shortest lead time, no accumulating work in progress (C-013, C-021; S1, S6, S8; S19 is vendor data and flagged as such).
7. No serial coordinator lane in the merge path (A-002, A-004, C-010; A-010 full local suite is serial in V1).
8. Respects the standing rules without negotiating any: "nothing is merged by an agent", `/sc:pr-submit`, no rebase of a published branch, no CI config change (A-014; C-006, X-005).
9. The release is a decision, not a branch: no line to keep current (C-002, C-008, C-013).
10. Uses the documented flow `master <- integration <- feature` of CLAUDE.md (C-003).
11. Honest unknowns with a first test attached (U-009; V3's U-013 is compatible).

**Weaknesses identified in the others**:
- V1:
  1. Isolation is deferred, not removed: the Clay collision shows late in the `master` into `integration` sync PR (C-018, X-003, C-003; V1 Q8).
  2. Quality gate is one machine and one person until the end (C-007, C-011; V1 Q2 and section 5).
  3. One large PR at the end (C-021, A-003; U-002 digest does not reduce what the bots analyse; PR #147; S19 vendor data).
  4. Self-conditional justification: "This proposal only holds if release branches stay days, not weeks" (C-013, X-006; A-016).
  5. Local merges leave no reviewable record outside the ledger; no early look for the owner (V1 section 5, risk 6).
  6. Merge-in housekeeping and a rebase-forbidden long line (C-008, C-009).
- V3:
  7. Needs a workflow edit and a prefix check that V2 does not (C-007, A-008, A-011, A-013; V3 section 5 and risk 5).
  8. Needs a merge-authority decision to be useful (X-005, A-014, C-006; V3 Q2 and risk 1).
  9. The train inherits `integration`'s state at the cut and drifts afterwards; planning base moves (C-002, C-008, X-009; V3 risk 3, Q3, Q8).
  10. Clay collisions surface later than in V2 (C-011; V3 Q8).
  11. Stacking is weak and unusable under current CI (C-025, X-010).
  12. A train is a long-lived branch with a time box the owner has not chosen (C-013; Open decision B; V3 Q5).
- V4:
  13. Internal contradictions (X-003, X-008, A-017).
  14. The "decided approach" is mostly adaptation: Q3, Q5 UNSPECIFIED, Q7 mostly MY ADAPTATION, Q8 adaptation, Q9 UNSPECIFIED; source rules replaced in Q2.
  15. The source is a draft ("Pending team review") and its practice evidence is cautionary (U-015).
  16. Needs the same `test.yml` edit as V3 (C-007, A-008) and has no rollback rule (C-022).
  17. Whole release in one PR again (C-021).
- Shared:
  18. Revert-then-re-merge is an unverified trap in V1 and V3 (V1 risk 5, V3 Q9; C-022); V2 fixes forward, flips the flag or re-cuts.

**Concessions**:
1. Owner merge load (A-003, C-006): "the heaviest merge load of the three"; most likely failure is a queue of ready slices waiting for the owner (V2 risk 1); no variant has a per-day capacity figure.
2. The ledger has no home (C-020, X-009); one candidate fix (a small record file per slice), labelled UNVERIFIED.
3. Isolation from Clay (C-018, X-003): V2 cannot ship the dashboard without Clay's merged work (V2 risks 3 and 4).
4. Dark landing is unproven in this codebase (U-009, C-012); V3's "not in the train" answer (U-010) may beat V2 for stories that cannot land dark.
5. Duplicated second review at promotion (C-021).
6. Story-level revert is more work: k slice commits, k reverts (C-005).
7. Planning base for release n+1 is not stated in V2 (X-009).
8. Merge-method and branch-deletion settings are unchecked (A-006; S12).
9. Per-slice cost: more CI minutes and review events per release than V1.

**Shared assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 QUALIFY; A-006 QUALIFY; A-007 QUALIFY; A-008 QUALIFY; A-009 QUALIFY; A-010 QUALIFY; A-011 ACCEPT; A-012 ACCEPT; A-013 ACCEPT; A-014 QUALIFY; A-015 ACCEPT; A-016 QUALIFY; A-017 REJECT (standard git behaviour; not re-tested in a scratch repo).

**Diff points claimed**:
- Wins: C-007; C-011; C-008; C-010; C-005 and C-022 (granularity and avoiding the revert-then-re-merge trap, not whole-story revert); C-001 (narrow, robustness); C-013 and X-006; C-003 (over V1 and V4, tie with V3); X-001; X-003 and A-017 (against V4, tie with V1); X-007 (tie with V4); X-008 (by default); X-010; U-006, U-007, U-008, U-009.
- Concedes or shares: C-006 and X-005 (V1 wins on owner effort); C-012 (V1 and V3 beat V2 on certainty); C-018 and X-003 (V1); C-020 and X-009 (V1, V3 second); C-021; C-002 (draw V2 and V3); C-004 and C-014 (V2 best for review size, V1 for owner effort).
- No decisive difference: C-009, C-015, C-016, C-017, C-019, C-023, C-024, C-025, S-001 to S-006.
- Would carry into a merged proposal: U-010 (as the fallback for a story that cannot land dark), U-013, U-003.

### Variant 3 Advocate (adv-3, backend persona)
**Position**: V3 is the only variant that keeps the owner's batch (nothing half-built reaches shared branches) while giving every story an outside check (CI plus Augment plus Codex) against the real batch tip, and it contains the cost of a failure to a private branch (`train/*`) instead of the shared trunk (V2) or an unchecked local branch (V1). Stated price: one `test.yml` edit, a merge-authority decision (Open decision A) and a double review at the roll-up. V4 is closest but is V3 without the parts that make it internally consistent (C-007, X-003, X-008, A-017).

**Steelman of the other variants**:
- V1: the owner's own model made exact; asks the least of the repository (no workflow edit, no merge-authority rule, no change to the BMAD planning base C-020, no back-port inside the release C-015); keeps Clay's unreleased `integration` work out of the release PR (X-003); two guards V3 lacks (U-001, U-002); honest about its limit.
- V2: best evidence base (S1, S2, S6, S8); collisions show at once in CI (C-011); no long-lived branch and no workflow edit (C-007); finest rollback (C-022); matches Clay's habit (Q8); slicing with a switch-on slice (U-006); names its own costs including the ledger (C-020).
- V4: decided approach from the owner's own organisation; provenance marks (U-014); collision-proof names by folder separation (C-001); PR #147 evidence (U-015); no-merge-right guard (U-017); full-tier release gate (U-018); squash into the release gives a plain one-commit revert per story.

**Key strengths claimed**:
1. Every story is checked against the real batch tip by something outside the coordinator; detection latency is one merge in V3 versus the whole release in V1 (C-004, C-007, C-011).
2. Bulkhead for merge authority and breakage: the owner rule is relaxed only for PRs into `train/*`, after green CI and settled reviewers; the owner keeps the click that puts code on a shared branch (C-006, X-005). A red `integration` does not stall a train (V2 risk 3).
3. A collision with Clay is found before anything reaches `master` (C-003, C-018, Q8); V1 Q8 admits the collision "shows up in that sync pull request, late".
4. Self-consistent with every fact in CONTEXT.md: merge not rebase (X-007), no folder/leaf clash, `dash1.3-sync<N>` for the one conflict nobody else routes (U-011, C-010); V4 breaks itself in three places (X-003, X-008, C-002).
5. Batch size bounded by time, so no flags and no flag debt; "The scope floats, the time does not" (C-012, C-013, U-010); the only explicit exit ladder (V1 falls back to V3, V3 falls back to V2).
6. Layered rollback with preserved story boundaries: story out of train, train out of `integration`, promotion out of `master`; "Prefer a fix train" avoids the reverted-merge trap (UNVERIFIED general git behaviour) (C-005, C-022).
7. Small-diff review load with a stated cost: roll-up is "mostly an integration check" (C-021; S6, S19).
8. Fail-safe validation of its own riskiest assumption: open one throwaway test PR first because a wrong filter leaves story PRs with no CI "while everyone assumes they have it" (U-013, risk 5, A-008, A-011).
9. Ledger and `.dev/` records stay on the batch branch (C-020); only the BMAD planning base moves (X-009).
10. Explicit decision interface: Open decisions A, B, C (U-012).

**Weaknesses identified in the others**:
- V1:
  1. No external gate and no durable state until the end: "Nothing is pushed for review until the release is complete"; no backup-push step; an untracked `.dev/worktree-archives/` shows worktrees get archived (C-004, C-007, A-005).
  2. Big-batch landing is V1's own named top risk; V1 Q5 says "switch to Proposal 3" (C-021).
  3. It moves the Clay coupling to after the release is on `master`; A-015 sync owner UNVERIFIED (C-018, X-003).
  4. Reverts of dependent stories are manual with no CI backing (U-005).
- V2:
  5. The owner is the throughput limit: "The merge is the owner's button, not the coordinator's"; 15 to 60 PRs per burst (C-006, A-003).
  6. Half-built work sits on a shared branch that anyone can promote (C-012, C-018).
  7. Dark landing is unproven here and costs state (C-012, U-009; U-008, S20).
  8. No home for the ledger: "the biggest process cost of this proposal" (C-020).
  9. Squash plus per-slice PRs make the dashboard's history inseparable from Clay's (C-005).
- V4:
  10. Contradicts itself on `integration`: Q8 and Q4 "Not through `integration`" versus Q3 merging it in (X-003, A-017, C-018).
  11. Contradicts itself on when CI runs (X-008, C-007).
  12. The base of the release line is undefined (C-002, X-001).
  13. No rollback, conflict-prevention design or clean-up rule from the source (C-022, C-023, C-011); source is a draft for whole-feature branches (C-014) and rebase-only (C-009).
  14. Adopts the landing shape its own evidence condemns: PR #147 was a release-sized landing, yet V4 lands one whole-release PR (C-021; U-018).

**Concessions**:
1. Decision A is a hard dependency: without it V3 stalls behind the owner like V2 (V3 risk 1).
2. Double review: each change is reviewed at the story PR and again as a roll-up; whether the roll-up pass is mostly noise is UNVERIFIED.
3. Clay coupling is accepted, not avoided (C-018); V3 inherits red or half-done state at the cut (V3 risks 3 and 4).
4. Merge-in load against a fast-moving `integration` is V3's main weekly cost; fine at two stories, degrades beyond about four (A-004).
5. `master`-first fixes need a back-port (C-015, C-019).
6. BMAD planning base moves from `master` to `integration` (X-009, C-020).
7. Squash is simpler to re-merge after a revert (C-005).
8. V2 has the stronger published evidence base and the finest rollback (C-022).
9. Flat story names group worse than V1's sibling layout (U-004, C-001).
10. Per-story `/sc:pr-submit` sessions are costly: one top-level session per story.
11. Things to adopt from others: V1's U-001 and U-002; V4's provenance habit (U-014), explicit stale-branch clean-up rule (C-023, U-015) and no-merge-right framing (U-017).
12. Open items: reviewer behaviour on `train/*` bases (A-012); which workflow-file version GitHub reads for `pull_request` (UNVERIFIED); whether merge commits are enabled.

**Shared assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 QUALIFY; A-006 QUALIFY; A-007 QUALIFY; A-008 QUALIFY; A-009 QUALIFY; A-010 QUALIFY; A-011 QUALIFY; A-012 QUALIFY; A-013 QUALIFY; A-014 QUALIFY; A-015 ACCEPT; A-016 ACCEPT; A-017 REJECT (merging `integration` puts Clay's commits into the PR to `master`).

**Diff points claimed**:
- Clear wins: C-004; C-006 and X-005; C-010; C-012, C-013, X-006; C-019; C-025 and X-010; X-008; X-003 and A-017; U-010, U-011, U-012, U-013.
- Win against some variants, not all: C-001 (tie with V2, better than V1 and V4, loses to V1 on browsability); C-002 and X-001 (beats V4's silence, does not claim over V1); C-003 and X-002 (conceding the coupling C-018); C-007 (beats V1, ties V4, loses to V2); C-008 (beats V4); C-009 and X-007 (tie with V1, V2; beats V4); C-011 (equal to V2, ahead of V1, V4); C-021 (ahead of V1, V4; equal to V2); C-022 (ahead of V1, V4 on layers, behind V2 on flag-off); C-005 and X-004 (split, no win claimed); C-014, C-016, C-017, C-023, C-024 (tie; on C-023 V4's explicit stale-branch rule is better).
- Losses conceded: C-015 (to V1); C-018 (to V1); C-020 and X-009 (to V1; V3 beats V2); S-002, U-014, U-015 (to V4); U-001, U-002 (V1) and U-006 (V2) are better ideas.
- Structural: S-005 and S-001 claimed (Open decisions section); S-002 conceded to V4; S-003, S-004, S-006 are formatting and not claimed.

### Variant 4 Advocate (adv-4, qa persona)
**Position**: Variant 4 is "the right skeleton and the wrong first draft". The skeleton (a `release/<rel>` branch in a different folder from the `<rel>/<kind>/NN-slug` work branches; stories squashed into the release line; one merge-commit PR into `master`; hotfixes from `master`; explicit clean-up and revert rule) survives every failure scenario the advocate built from this repository's history. Two defects of the draft are conceded (PR per story; merging `integration` into the release). The advocate defends "original plus the seven named changes in `gfxai-fit.md`, minus the `integration` merge", which converges on V1 with four differences: the folder layout, squash instead of `--no-ff`, a beta freeze and a release-PR acceptance gate. Source status: GFxAI document "version 1.0", `status: "To Do"`, "Pending team review", Release and Tagging section "To Do (No prework)"; the 2026-05-19 decision that amends it was never applied; about 30 of the last 40 merged GFxAI PRs go straight to `master`.

**Steelman of the other variants**:
- V1: the owner's model made exact; no change to CI, settings or worker contract; keeps ledger on the release branch (CONTEXT line 14) and planning on `master` (X-009); alone sees the Clay hazard (V1 Q3, confirmed by E3); trial merge (U-001), path claims (U-003), digest (U-002); honest about its weak point.
- V2: best evidence base (DORA, trunk-based, Fowler); "partial rollback is easy, which is the best rollback story of the three proposals" (C-022); CI and both bots on every slice against real `integration` (C-011); no workflow edit; repository support: observer work #409 shipped as PRs "release 1" (#503) and "release 2" (#514); owner lands about 6 commits a day on `master` (E5); honest about the ledger.
- V3: batch isolation plus per-change CI and review; floating scope (U-010); raises the three owner decisions (U-012); throwaway test PR (U-013); lands where Clay lands; 6.0.0 (#640) and 6.1.0 (#664) both travelled `integration` to `master` (E4).

**Key strengths claimed**:
1. The folder layout gives a ref-name rule that is checked, not hoped for: `release/dash1.3`, `dash1.3/story/01-x`, `dash1.3/bugfix/02-y`, `hotfix/5-z` coexist, also under an `ironbelly/` prefix; a bare `dash1.3` or `release` fails loudly (Q1, C-001; E1). Scope: flat names are even safer; V4 wins on grouping and convention, not robustness.
2. Squash into the release line, merge commit into `master`: the only branching incident in recent history is a merge-method mistake (#658 squash-merged by mistake, reverted by #662, redone as #664) (Q2, Q4, C-005, X-004; E4). Squash also removes the `--no-ff` revert-then-redo trap (E2: `CONFLICT (modify/delete)`).
3. A cheap bisect and a plain revert unit: one squash commit per story, about 4 bisect steps for 16 stories, plain `git revert <sha>` (Q9, C-022).
4. A freeze and an acceptance gate the other three lack: beta freeze (Q6) and full test tiers, two approvals and sign-off (Q4); compensating control for A-005 (C-016, U-018).
5. Hotfix and landing rules match what the maintainers already do: straight into `master`, then `master` merged back into `integration`; five "merge master into integration" commits by clayphi 2026-11-17 to 11-19 (Q4, Q6, Q8; E4).
6. An explicit clean-up rule: `delete_branch_on_merge` is false and there are 170 remote branches (E6); V2 and V3 rely on auto-delete, marked UNVERIFIED by them (Q7, C-023).
7. Auditable provenance: every rule tagged FROM SOURCE, FROM PRACTICE, MY ADAPTATION or UNSPECIFIED (S-002, U-014).
8. Real long-lived-branch evidence weighed both ways: GFxAI `feat/OntRAG` merged `master` in twice and still landed as #147 (34 commits, 1,384 files, +242,976 lines, "file-level rejections"); but that branch ran for months with no size cap, and this repository's #640 (1,146 files) and #664 (181 files) landed as single PRs and stayed; the lesson supports a size cap and a digest, not a ban on a release line (C-021, U-015).
9. Failure scenarios handled with a stated rule (table): bad story after merge; coordinator dies mid-merge; hotfix lands while the release is open; release PR merged with the wrong method; release fails on `master`; Clay's open `integration` PR touches dashboard files.

**Weaknesses identified in the others** (items marked "shared" also hit V4):
1. V1: `--no-ff` story merges plant the revert-then-redo trap (C-005, C-022, U-005; E2); V1 mitigates with reverse-order reverts but does not say how a reverted story is redone.
2. V1: nothing is pushed until the release is complete, a single point of failure; the new worktree-removal tool (#711) may touch an unpushed release worktree (UNVERIFIED) (C-004). The forward-only push fix applies to V4 too and is adopted.
3. V1: no freeze or acceptance gate (C-016).
4. V2: the ledger has no home and the release is not what the owner described (C-020, X-009; CONTEXT lines 7 and 14).
5. V2 and V3: cut from `integration`, which is behind `master` (`24 2` in E4) (C-002, X-001).
6. V2 and V3: the landing carries everything in `integration`; the dashboard release is hostage to any red change there (C-003, C-018, X-002, X-003).
7. V2: dark landing is unproven here and the cherry-pick rule has its own duplicate-patch noise (C-012, C-015).
8. V3: the `test.yml` edit must land before the first story PR (E7: filter is `[master, integration]`) and merge authority is unresolved; planning base moves (C-007, A-008, A-014, X-005, X-009).
9. V3: every story gets two bot reviews and then the roll-up gets two more (C-021, V3 risk 2).
10. Shared, V1 and V4: one large release PR (C-021); takes V1's story cap and digest as mitigations.
11. Shared, V1 and V4: no CI before the release PR (C-007); `workflow_dispatch` in `test.yml` is a candidate mitigation (UNVERIFIED by a run).

**Concessions**:
1. PR per story is indefensible here (C-004, C-007, X-008): `test.yml` runs `pull_request` only for `master` and `integration`; `gfxai-fit.md` named change 1 already replaces it with local squash merges, which makes V4 inherit V1's no-CI-until-the-end weakness.
2. Merging `integration` into the release is wrong (X-003, C-018, A-017); drop it, merge `master` only, compare path claims with open `integration` PRs, merge `master` into `integration` after landing.
3. Base branch not stated (X-001, C-002); cut `release/dash1.3` from `master`.
4. Ledger and planning base not addressed (C-020, X-009); adopt V1.
5. Flat names are more robust and V4 adds surface (three levels; `hotfix/` and `bugfix` are new prefixes where the repository already uses `fix/`, `feature/`, `docs/`) (C-001, A-007).
6. "Cherry-pick or merge" for hotfixes is worse than V1's rule (C-015); drop the cherry-pick option.
7. No cap on how long the release line lives (C-013, X-006); adopt V1's days-not-weeks rule and fallback.
8. Squash loses story tips (C-005); judged smaller than the revert-then-redo trap, but the owner's call.
9. Source rules that do not transfer: two approvers, Tier 1/2/3, five environments, owner force-push, feature branch equals whole feature (S-005); every parallel-AI rule in V4 is the advocate's adaptation (A-001, A-002).
10. Pedigree: the document was never reviewed or applied by its own repository; the debate should not weigh it as precedent.

**Shared assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 REJECT; A-006 ACCEPT (all three merge methods enabled); A-007 QUALIFY; A-008 QUALIFY; A-009 QUALIFY; A-010 QUALIFY; A-011 QUALIFY; A-012 QUALIFY; A-013 QUALIFY; A-014 QUALIFY; A-015 ACCEPT; A-016 QUALIFY; A-017 REJECT (tested: `git diff master...release/dash1.3` lists the `integration` commit's file).

**Diff points claimed** (with V4 meaning V4 plus the named changes):
- Win: C-005 and X-004 (against V1 and V3, tie V2); C-022 (against V1 and V3; V2 wins flag-off granularity); C-016 and U-018; C-023 (against V2 and V3, tie V1); C-003 and X-002 (against V2 and V3, tie V1); C-002 and X-001 (against V2 and V3, conditional on V4 saying "cut from `master`"); S-002, U-014, U-015, U-016 (auditability).
- Tie: C-019 (with V1); C-004 and C-006 (with V1 after named change 1); C-009 and X-007.
- Partial: C-001 (wins over V1 on grouping and one `release/**` pattern; loses to V2, V3 on robustness and depth).
- Lose: C-007, C-011, X-008; C-018, X-003, A-017; C-020, X-009; C-013, X-006; C-015; C-021, S-003, S-005.

**Evidence log (Round 1)**: E1 ref names in a scratch repo; E2 revert then redo (merge-commit route conflicts, squash route clean); E3 `integration` merged into the release line (`git diff --stat master...release/dash1.3` lists `clay.txt`); E4 repository history (`24 2`; #640, #658, #662, #664; five sync commits by clayphi; #503 and #514); E5 merge rate (128 Ironbelly, 52 clayphi, 5 coder authored commits on `master` since 2026-11-01); E6 settings (squash, merge commit, rebase all allowed; `delete_branch_on_merge` false; 170 remote heads); E7 `test.yml` lines 3 to 8 (`[master, integration]`, plus `workflow_dispatch`). Not checked: Orca `--branch` prefix behaviour, `/sc:worktrees` on unpushed worktrees, bot behaviour on non-default bases, rulesets, dashboard test coverage, the GFxAI repository.

## Round 2: Rebuttals

### Variant 1 Rebuttal (adv-1, architect persona)
**Response to criticisms of Variant 1 (A1R2 section 1)**:

Conceded in full:
1. Nothing is pushed, so the release line is a single local copy (A3-W1, A4-W2). Fix adopted: the coordinator pushes `release/<rel>` forward-only after each story merge, as a backup and not a review request; this also answers A2-W5 (GitHub's branch compare page shows the release against `master`).
2. No freeze rule (A4-W3, A4-S4). Adopted: once the planned stories are merged, only `fix-` branches enter until the PR is merged.
3. Revert-then-redo needs a stated procedure (A4-W1, A4-S2). Scratch run: direct re-merge after `git revert -m 1` stops with `DU s.txt`; reverting the revert first, then merging the fixed branch, is clean. V1's risk 5 was a missing procedure, not a structural defect; rule adopted; does not move on C-005.
4. A wrong merge click on the release PR is a real risk (A4 E4; #658, #662, #664). Adopted: the PR body says "merge commit only" and the closeout check reads the merge method.
5. Review size and no outside gate (A2-W2, A2-W3, A3-W2, own R1 concessions 1 and 2). Stands; narrowed by two facts: this repository's promotions are already release-sized, and `test.yml` has an unconditional `workflow_dispatch:` (UNVERIFIED by a real run; needs the owner's nod).

Contested, with counter-evidence:
6. "Isolation is deferred, not removed" (A2-W1, A3-W3): the collision does not land on production; the sync happens on a sync branch and the combination first exists on `integration`; adds read-only `git merge-tree` of the release tip against `origin/integration` (extends U-001, U-003).
7. "One large pull request" (A2-W3, A4-W10): #640 and #664 landed as single large PRs and stayed; the failure was the merge click; the promotion is large in V2 and V3 too.
8. "Self-conditional justification" (A2-W4): every variant states a fallback trigger; a stated exit is design hygiene; takes V3's floating scope.
9. "Merge-in housekeeping and a rebase-forbidden line" (A2-W6): V2 moves the same work onto every slice branch.
10. "Documented flow is `master <- integration <- feature`" (A2-S10, A3-S3): conceded as a departure (R1 concession 5); `master` is 26 commits ahead of `integration`, maintainers sync by hand, a wrong-method promotion already happened (#658).
11. "No per-story record; the bots never see a story" (A2-W5): accepted as cost.
12. "Reverts of dependent stories are manual with no CI" (A3-W4): manual in every variant; dispatch supplies CI on request.
13. "The coordinator is a single point of failure" (A3's A-002 row; own R1 concession 6): the push plus ledger lines before and after each merge let a successor resume.
14. "V1 relaxes the merge-owner rule with no external check" (A3 A-014 reason): true; V1's ask is a smaller authority class (local, reversible, like the worker contract's child-into-feature merge); A3 concedes V3 is no better than V2 without Decision A (A3-C1).

**Updated assessment of the other variants**:
- V2: did not change on the four structural points (owner as lane, ledger, dark landing, Clay coupling), all conceded by A2 (A2-C1 to A2-C4). Changed partly: withdraws "throttled" as a flat claim after A4's E5 (about 6 commits a day). A2-S2 is right (V2's CI trigger keys on the base branch; V1 shares the immunity). A2-S3 and A2-S7 are partly met by V1 now but still weaker than CI on every slice; not a draw. A2-W points 2 and 5 have force.
- V3: A3 settled Decision A as a hard dependency (A3-C1), back-port (A3-C5), planning base (A3-C6), per-story session (A3-C10), CI minutes (A3-C4); A3 could not confirm where GitHub reads the workflow file (A3-C12). A3-S2 (bulkhead) is the strongest argument but costs three owner decisions and a workflow edit. Takes from V3: U-010, U-013, U-012. V3 as "reversible middle rung" is fair.
- V4: A4 dropped PR per story (A4-C1), merging `integration` (A4-C2), no base (A4-C3), ledger and planning base (A4-C4), long-lived cap (A4-C7), cherry-pick (A4-C6). Of the four remaining differences, takes the freeze, the `release/<rel>` folder and a reduced acceptance gate; does not give up `--no-ff` (close call, the owner's). A4's #658 evidence has more weight than first given.

**New evidence (all read-only, 2026-11-23)**:
1. Re-merge after reverting a story merge (scratch repo): direct re-merge conflicts (`DU s.txt`); revert the revert first, then merge: clean, both the story and the fix present.
2. `test.yml` lines 3 to 8: `push` and `pull_request` for `[master, integration]` and an unconditional `workflow_dispatch:`; no job gated on the event name (UNVERIFIED by a real run).
3. Merge settings: `allow_merge_commit`, `allow_squash_merge`, `allow_rebase_merge` true; `delete_branch_on_merge` false (settles A-006).
4. No remote heads named `release/*` or `dash*`.
5. `git rev-list --left-right --count origin/master...origin/integration` printed `26 2`.
6. From A4 E4, used as an argument: #640 (1,146 files) and #664 (181 files) are release-sized PRs that landed.

**Combined design, question by question** (base V1; condensed):
- Q1 Names: `release/dash1.3` [V4 folder]; stories `dash1.3/s04-slug`, in-release fixes `dash1.3/fix-01-slug` [V1]; shipped-code fix `fix/<issue>-<slug>`; tag `dash-1.3` [V4]; invariant: no branch named `dash1.3` or `release` alone; throwaway `orca worktree create --branch` first [V3 U-013] (A-007, A-011 check).
- Q2 Story merge: local, coordinator, `--no-ff`, one story at a time; path claims and `git merge-tree` trial [U-001, U-003] before; tests, ledger line before and after, forward-only push after; optional `workflow_dispatch` on the pushed line (owner to approve; UNVERIFIED); no PR per story; if the owner wants per-story bot review, move that release to V3.
- Q3 Staying current: merge `origin/master` in at start, between stories and before the PR; never `integration`; `git merge-tree` against `origin/integration` at each merge-in; path claims against open `integration` PRs [U-003].
- Q4 Landing: one PR `release/dash1.3` into `master` by `/sc:pr-submit --monitor 3 --base master`; body "Merge this pull request with a merge commit, not squash", digest [U-002], path classes [A-009]; freeze after the last planned story; story-count cap set at planning.
- Q5 Flags and justification: no flags; days not weeks, one week at most [V1]; floating scope at the cap [V3 U-010]; if caps are missed move to V3, then V2 slicing.
- Q6 Hotfixes: `fix/<issue>-<slug>` from `master`, picked up at the next merge-in, no cherry-pick; in-release fix `dash1.3/fix-NN-slug`; 1.1 and 1.105 are ordinary release lines; a one-story release is a plain `fix/` or `feat/` PR [V1].
- Q7 Clean-up: story branch and worktree removed after ledger entry and push; release line deleted (local and remote) after owner merge and open sync PR, explicit because `delete_branch_on_merge` is false; tag; `.dev/` and `sprint-status.yaml` on the line.
- Q8 Fit with Clay: unchanged during the release; after landing the coordinator opens the `master` into `integration` sync; clean-up waits for it.
- Q9 Rollback: `git revert -m 1` or fix forward; to return a reverted story revert the revert first; dependent stories in reverse order; release failure: revert PR of the release merge commit through `/sc:pr-submit`, prefer a bug-fix release line; method mistake handled by Q4 text and closeout check.

**Positions stated in the Round 2 table (winner, confidence)**: C-001 Combined (V4 release folder, V1 story names) 60; C-002 and X-001 V1 (and V4 once it says so) 85; C-003 and X-002 V1 and V4 75; C-004 V1 60; C-005 and X-004 V1 narrowly 55; C-006 and X-005 V1 60; C-007 V2 70; C-008 V1 80; C-009 and X-007 V1 70; C-010 split V1 and V3 50; C-011 split (V2 and V3 on latency, V1 on pre-merge guards) 65; C-012 V1 with V3's rule 65; C-013 and X-006 combined (V1 line, V3 time box) 65; C-015 V1 85; C-016 V4 75; C-018 V1 85; C-019 V1 and V4 55; C-020 and X-009 V1 90; C-021 V2 and V3 60; C-022 V1 at release level, V2 at slice level 65; C-023 V1 and V4 85; C-024 V4 55; X-003 and A-017 V1 95; U-001 to U-003 keep 80; U-010, U-012, U-013 adopt 75; U-014, U-015, U-017 adopt 65; U-018 V4 in part 50; U-006 to U-009 V2, not adopted in the base 60; A-006 ACCEPT (changed from QUALIFY) 95; A-008, A-012, A-013 ACCEPT unchanged 80; A-005, A-010 QUALIFY unchanged 70; A-003 QUALIFY updated 65. Not contested by A1: S-001 to S-006, C-014, C-017, C-025, X-008, X-010.

### Variant 2 Rebuttal (adv-2, analyzer persona)
**Response to criticisms of Variant 2 (A2R2 section 1)**:

Conceded because the evidence forces it:
1. `integration` is not the live trunk today (A4-W5; own R1-S10 withdrawn). N1 and N3: no merged PR into `integration` since 2026-11-19, 26 commits on `master` it lacks, 18 of them the owner's; the owner's practice is direct PRs to `master`. The "documented flow" argument (R1-S10) is withdrawn.
2. No home for the ledger (A1-W2, A3-W8, A4-W4). Conceded in full; C-020 and X-009 go to V1; own R1-C2 per-slice record file not needed once a release line holds the ledger.
3. Dark landing is unproven (A1-W3, A3-W7). Conceded; the combined design does not depend on it.
4. Shipping is tied to Clay's promotions (A1-W4, A3-W6, A4-W6). N2: Clay promoted `integration` twice in about 36 hours (#640 merged 2026-11-18 16:30, #664 merged 2026-11-19 01:47) at his own timing; "dark by construction" would be a hard requirement.
5. Release-level rollback (A1-W5, A3-W9). The promotion merge commit holds all unpromoted `integration` work; C-022 at release level goes to V1; slice-level undo kept.
6. Clean-up by auto-delete (A4-S6; A1R2 section 3 item 3). N8 shows `delete_branch_on_merge` is off; C-023 goes to V1 and V4.
7. The owner is the lane (A1-W1, A3-W5), load now measured. Keeps R1-C1. N1: owner PRs merge at about 5.7 a day, median 90 minutes open; Clay's slice PRs median 24 minutes; load is inside the demonstrated rate; A1R2 withdrew "throttled"; counts include record-only PRs and are largely self-authored.
8. Own R1 weakness 1 against V1 was wrong in part (A1R2-6): the Clay collision lands on a sync branch and then on `integration`, not on `master`; withdrawn.

Contested, with evidence:
9. Cherry-pick duplicate noise (A4-W7). N7: real only when `integration` later edits the same lines (case 2 conflicted, case 1 clean); low cost; not needed in the combined design.
10. Duplicated second review (A1-W6). N2: promotions merge in 17 to 43 minutes; N4: the 23 slice PRs each got Augment, Codex and CI (sample of 4); a fast merge of a 181 or 1,146 file diff is not evidence it was read (answers A1R2-7).
11. "Merge-in work is higher in V2 because it is per slice" (A1R2-9). UNVERIFIED either way; nobody measured conflict rates.
12. Squash makes dashboard history inseparable from Clay's (A3-W9). True for revert as one object; findable by story id and `git log --grep`; a cost, not a defect.

Not contested: V2 is a counter-proposal to the owner's model (A4-W4); for Round 2 the model and the five constraints are fixed, so V2 is judged by which of its pieces survive them.

**Updated assessment of the other variants**:
- V1 (after A1's rebuttal): changed mind on landing and base (C-002, X-001, C-003, X-002 to V1); adopted fixes are real improvements (forward-only push A1R2-1, freeze A1R2-2, revert-the-revert A1R2-3, merge-method guard A1R2-4, `git merge-tree` against `origin/integration` A1R2-6). Did not change: V1 still has no bot review of any story; `workflow_dispatch` narrows C-007 and C-011 but does not close them; A1R2-7 reads the promotion record as reassurance, N2 reads it as evidence a roll-up is a rubber stamp; "one owner nod buys part of the same gate" is a hypothesis until run.
- V3 (after A3's Round 1): A3 conceded Decision A as a hard dependency (A3-C1), CI growth with waiting stories (A3-C4), per-story top-level `/sc:pr-submit` sessions (A3-C10), and could not confirm where GitHub reads the workflow file (A3-C12). V3 does not fit the constraint set as given (CI only for PRs into `master` or `integration`). Takes U-010, U-012, U-013. A3-S2 (bulkhead) is the best argument for V3 but still needs the `test.yml` edit and a new merge authority.
- V4 (after A4's Round 1): accepts A4's reading that V4 is V1 plus a `release/` folder, squash, a freeze and an acceptance gate (A4-C1 to A4-C7 dropped the rest). A4's evidence log is the most useful new Round 1 material (#658, delete-on-merge off, `workflow_dispatch`); A4-C5's worry about three-level names has a concrete mechanism (N5).
- V2 (own variant): as a standalone proposal V2 does not fit (needs a live `integration` trunk, a ledger home, a tested dark-landing practice); keeps the strongest evidence-based pieces: per-change outside review and CI with no config edit, slice-level undo, flat names, cut late and keep short.

**New evidence (read-only, 2026-11-23)**:
- N1 Where merged PRs go since 2026-11-01: 23 PRs into `integration` (all clayphi; median 23.6 minutes; median 51 files, p90 101); newest merged 2026-11-19 03:35 (#667); 155 PRs into `master` (130 ironbelly, 25 clayphi; median 89.9 minutes; median 37 files, p90 334); 0 of the owner's 130 went through `integration`.
- N2 Promotion review times: #640 (1,146 files) 43 minutes; #658 (181 files, mistaken squash) 17 minutes; #664 (181 files) 27 minutes.
- N3 `integration` against `master`: 26 commits on `master` it lacks, 2 on `integration` that `master` lacks; of the 26, 18 by Ironbelly and 8 by clayphi.
- N4 Bots and CI: Augment and Codex both appear, with six check runs, on four `integration` PRs (#639, #650, #656, #667) and three `master` PRs (#664, #673, #728); nothing on other bases; #686 and #690 draft behaviour inconclusive.
- N5 Branch names the owner's sessions produce: 49 remote branches start with `ironbelly/`; exact names without the prefix also occur (#730, #688, #660); whether `--branch` keeps the exact name is UNVERIFIED.
- N6 `test.yml` has `pull_request` (line 6) and an unconditional `workflow_dispatch:` (line 8); no `if:` tests the event name or draft flag; `pr-submit.md` line 94: draft behaviour of Augment, Codex and CI is "unverified until the owner's run on a disposable PR; do not rely on it"; no open-as-draft flag.
- N7 Cherry-pick duplicate test (scratch repo): case 1 clean, case 2 conflicts when `integration` edited the same line again.
- N8 Settings: `delete_branch_on_merge` false; squash, merge commit and rebase all allowed.

**Combined design, question by question** (base: owner's model as A1 laid it out; condensed):
- Q1 Names: `release/dash1.3`; stories flat `dash1.3-s04-<slug>`; in-release fix `dash1.3-fix01-<slug>`; shipped-code fix `fix/<issue>-<slug>`; tag `dash-1.3`. Reason for flat: Orca names a branch `ironbelly/<worktree name>` (N5); a worktree called `dash1.3` gives `ironbelly/dash1.3`, then `ironbelly/dash1.3/s04-...` fails with "cannot lock ref" (CONTEXT line 8); listing `git branch --list '*dash1.3-*'`; throwaway `orca worktree create --branch` first [U-013].
- Q2 Story merge: local, coordinator, `--no-ff`, one at a time; path claims and `git merge-tree` trial [U-001, U-003]; tests, ledger line, forward-only push [A1R2-1]; outside gate: `workflow_dispatch` on the pushed line after each story merge with the owner's standing approval; to test once on a disposable PR: whether a hand-opened draft release PR gives CI on each push and bot review, and whether the bots react to a draft at all (UNVERIFIED).
- Q3 Staying current: V1 unchanged plus `git merge-tree` against `origin/integration`; do not use `integration` as a base (26 behind).
- Q4 Landing: one PR to `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit only in the body, closeout checks; digest [U-002]; freeze [V4]; cap: about six stories, roughly 300 files, without `.dev/` records (inference from N1, not a measured limit).
- Q5 Flags and justification: two lanes decided at planning. Feature releases: release line, hard time box, floating scope [U-010], no flags, slice stories that cannot finish [U-006 adapted]. Bug-fix (1.1) and test-only (1.105) releases: no release line, small PRs straight into the default branch as the owner already does for 130 of the last 155 `master` PRs (N1). Third rung only if the box is missed twice: dark-by-construction slices as direct PRs after the V2 pilot (U-009).
- Q6 Hotfixes: V1 unchanged, no cherry-pick (N7); in-line fix `dash1.3-fix<NN>-<slug>`.
- Q7 Clean-up: explicit deletion (N8); `.dev/` and `sprint-status.yaml` stay on the line.
- Q8 Fit with Clay: V1; new fact for the owner: `integration` has had no merged PR for four days and is 26 behind, so the first sync carries 26 commits not the release's doing; whether `integration` is still the branch Clay works from is a question for the owner.
- Q9 Rollback: V1 (revert `-m 1`, revert the revert first, revert PR of the release merge commit, then a fix line); slice-level undo and flag-off only in the third rung.
- Owner decides: (1) confirm local coordinator merges (CONTEXT line 11); (2) story-count cap; (3) approve CI minutes for a dispatch run after each story merge; (4) say whether `integration` is still in use.

**Positions stated in the Round 2 table (winner, confidence)**: C-001 V2/V3 flat story names with V4/V1 `release/` folder 70; C-002 and X-001 V1 (master) 85; C-003 and X-002 V1 70; C-004 V1 65; C-005 and X-004 no winner (V1 `--no-ff` locally) 50; C-006 and X-005 V1 60; C-007 V2 70; C-008 V1 75; C-009 and X-007 V1 70; C-010 V1 with V3's sync branch unused 55; C-011 V2 65; C-012 V1 and V3 (no flags) 70; C-013 and X-006 combined (V1 line, V3 time box, hard cap) 65; C-015 V1 85; C-016 V4 70; C-018, X-003, A-017 V1 90; C-019 V1 and V4 55; C-020 and X-009 V1 90; C-021 V2/V3 on review quality, the cap is the control in V1 60; C-022 V1 at release level, V2 at slice level 65; C-023 V1 and V4 85; U-006 V2 adapted as a planning rule 60; U-007 V2 in spirit only 40; U-008 and U-009 third rung only 55; U-010, U-012, U-013 V3 adopt 80; U-001 to U-003 V1 adopt 80; A-003 QUALIFY updated 65; A-005 QUALIFY unchanged 70; A-006 ACCEPT (changed from QUALIFY) 95; A-008 and A-012 ACCEPT for V3 and V4 only 80; A-015 QUALIFY 60. Not contested by A2: S-001 to S-006, C-014, C-017, C-024, C-025, X-008, X-010. Net statement: holds C-007, C-011 and the slice-level half of C-022; concedes C-002, C-003, C-004, C-012, C-015, C-018, C-020, C-023 and X-001 to X-003.

### Variant 3 Rebuttal (adv-3, backend persona)
**Response to criticisms of Variant 3 (A3R2 section 1)**:

Conceded because the evidence forces it:
1. Cut from `integration` and landing through it are wrong for this repository (A1-W12, A4-W5, A4-W6, A2R2 point 1; C-002, C-003, X-001, X-002). E1: `integration` is 26 behind and 2 ahead of `master`, 24 PRs in its life against 460 into `master`; none merged since 2026-11-19 (A2 N1). Withdraws R1-S3 and half of R1-S2; C-002, C-003, X-001, X-002 go to V1; also removes the X-009 planning-base cost (R1-C6).
2. "V1 fails on production, V3 fails in a cheap place" (R1-S3, R1-W3) was overstated (A1R2-6): the sync happens on a sync branch and then on `integration`. Withdrawn.
3. Durability of V1 (R1-W1). A1R2-1 adopts a forward-only push of the release line; no longer a V3 advantage.
4. The package of three owner decisions is too much (A1-W7, A2-W7). Decision A (merge authority over GitHub PRs) is avoidable (see 12); Decision C (edit `test.yml`) is needed only if CI, not only bots, is wanted on story PRs; only Decision B (time box) stays.
5. Clean-up (R1-C, A4-S6, A2R2 point 6; C-023). The Q7 reliance on auto-delete is off; explicit deletion is mandatory. Conceded to V1 and V4.
6. Merge commits "avoid the reverted-merge trap" (R1-S6). Only flagged UNVERIFIED; A4 E2 and A1R2 section 3 item 1 show the trap is real and the remedy works; V3 holds no advantage; C-005 no winner from A3.
7. Stacks (A1-W9, C-025, X-010). Weak under current CI; with local merges there is nothing to stack. Dropped.
8. Review load of two bot passes per story plus roll-up (A4-W9, A2-W10). The largest real V3 cost; answered by making per-story PRs selective.
9. The time box is unset (A2-W12). True; a measured starting point is given in Q5; the owner sets it.

Contested, with evidence:
10. "Per-story CI and review rest on unverified third parties" (A1-W8, A1R2 point 5). The bot half is verified in this repository: both bots reviewed 5 of 5 story PRs into a batch branch (E2); the CI half is verified absent (0 checks), exactly R1 risk 5. A1's "no better than V1 until the throwaway passes" is false for bots.
11. "A roll-up of 181 or 1,146 files merges in 17 to 43 minutes, so reviewers take roll-ups" (A1R2 point 7 against A2R2 point 10). Sides with A2: a fast merge of a huge diff shows it was not read; E3 and E4: per-story review produced a follow-up fix before any roll-up (#490 then #491), while ten unreviewed story PRs of `feat/tdd-spec-merge` ended in one 2,089-file landing (#31).
12. "V3 asks for authority to merge GitHub PRs; V1's ask is smaller" (A1R2 point 14, section 5 C-006). Right about authority class, wrong that it forces Decision A: the story worker runs `/sc:pr-submit --monitor 3 --base release/dash1.3` for review only; when the bots settle, the coordinator merges locally with `--no-ff` and pushes; GitHub marks the PR merged when its head commits become reachable from the base (UNVERIFIED here; one throwaway test settles it).
13. "V3 couples the release to promotion cadence" (A1-W10). True of V3 as written; moot once the line is cut from and lands on `master`; the weekly merge-in cost becomes `master` merge-ins, which A1 also pays.
14. "Isolation is a bulkhead only if Clay promotes at his own timing" (A2R2 point 4). Agrees with N2's facts; that is an argument against V2 and supports a private release line, shared by V3 and V1.

**Updated assessment of the other variants**:
- V1: changed mind on base and landing (`master`, one PR, merge commit), forward-only push (A1R2-1), freeze (A1R2-2), merge-method guard (A1R2-4), `git merge-tree` against `origin/integration` (A1R2-6), never re-merge a reverted story branch directly (A1R2 section 3 item 1); V1 plus these is the right base. Did not change: V1 has no outside review of any single story (E2 shows the bots do review story PRs into a batch branch); A1R2 point 7 treats past large roll-ups as reassurance, E4 reads the other way; a 25-file, 4,636-line story (#490) is thin to gate on the coordinator's run.
- V2: changed mind: not a candidate base (`integration` not a live trunk, no ledger home, dark landing unproven; A2 conceded all of it). Did not change: V2 is still the only variant with per-change CI and bots with no configuration.
- V4: changed mind: A4 reduced V4 to V1 plus four items; takes the freeze (C-016), the explicit clean-up rule with the forward-only push (C-023) and `release/<rel>` as one pattern; U-017's wording is the clean statement of the owner rule (the coordinator never merges into `master`; the local merge into the release line is a separate class). Did not change: squash is not clearly better for local coordinator merges (A4-S2); `--no-ff` keeps per-task commits (A1-S10); the owner's call.
- Jointly settled by the Round 1 and Round 2 statements: A-017 is rejected by all four (X-003: V1 right); ledger and planning base stay with V1 (C-020, X-009); hotfixes need no back-port step (C-015); all three merge methods are enabled and auto-delete is off (A-006, C-023); open items: bot and CI treatment of story PRs, merge method for stories, the story cap.

**New evidence (read-only, 2026-11-23)**:
- E1 This repository's 506 PRs: base `master` 460, `integration` 24, 22 others (`feat/tdd-spec-merge` 10, `346Claude-integration` 5, and one each for six other bases); the V3 shape has been used twice; `26 2`.
- E2 PRs #484, #490, #491, #492, #493 into `346Claude-integration`: 0 check runs on each; Augment reviewed all five; Codex left a review or comment on all five; sizes 5 to 25 files, +83 to +4,636 lines. Settles A-012 for non-default bases here; confirms A-008 and R1 risk 5.
- E3 #490 (25 files, +4,636) merged 2026-11-11 03:12; #491 "fix(review): address #490 review findings" merged 05:46 the same day; severity of the findings not read (UNVERIFIED).
- E4 #497 (`346Claude-integration` into `master`, 58 files, +6,162) CLOSED, reason UNVERIFIED; #31 (`feat/tdd-spec-merge` into `master`) 2,089 files, +318,059, merged 2026-05-12 after ten story PRs; four sampled story PRs have zero checks, reviews and comments.
- E5 #474 shows 6 passing checks but its base was changed to `346GPT-integration` after opening; not counted as evidence that CI runs on a batch base.
- E6 `test.yml` at `80f361804` (2026-11-05, #402): `push` and `pull_request` for `[master, integration]` plus unconditional `workflow_dispatch:`.
- E7 Where GitHub reads the workflow file for a `pull_request` run: secondary sources (Mergify page, a GitHub community thread) say the merge commit or `github.sha`; GitHub's own events page did not state it; UNVERIFIED; one throwaway PR settles it.

**Combined design, question by question** (base V1; condensed):
- Q1 Names: `release/dash1.3`; stories flat `dash1.3-s04-<slug>`; in-release fix `dash1.3-fix<NN>-<slug>`; shipped-code fix `fix/<issue>-<slug>`; tag `dash-1.3`; drops `train/`; reason for flat: `ironbelly/<worktree name>` plus the owner's token `dash1.3` reproduces CONTEXT line 8 for folder-style stories (49 remote branches have the prefix, A2 N5); filters on `release/**` must also match `*/release/*` if the prefix is added; throwaway create first [U-013].
- Q2 Story merge: default as V1 (local `--no-ff`, path claims and `git merge-tree`, ledger before and after, forward-only push). Optional V3 layer chosen at planning per story: a review-only story PR (`/sc:pr-submit --monitor 3 --base release/dash1.3`); the coordinator merges locally when the bots settle (merged-by-push UNVERIFIED); removes Decision A; suggested threshold about 15 files or 1,000 added lines (not a measurement; #490 was 25 files, +4,636 and produced #491; #484 was 8 files, +217). CI for those story PRs by route (a) a one-line `branches` edit as the first commit on the release line (E7, UNVERIFIED) or route (b) `workflow_dispatch` on the pushed line (E6); owner picks. Conflicts as V1; `dash1.3-sync<N>` kept in reserve.
- Q3 Staying current: merge `origin/master` in; never `integration`; `git merge-tree` against `origin/integration`; path claims vs open `integration` PRs.
- Q4 Landing: one PR to `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit only in the body, method checked at closeout [#658]; digest [U-002]; freeze [V4]; where stories had review-only PRs the release PR's bot pass is the second look, which is why the PR layer is selective.
- Q5 Flags and justification: no flags; time box with floating scope [U-010]; starting numbers about six stories or seven days, whichever first; ladder: if missed twice, per-story PRs for every story; then slicing and direct PRs (V2 third rung after its pilot U-009). Bug-fix (1.1) and test-only (1.105) releases: A2R2's rule fits: small direct PRs into `master`, no line, when there is no behaviour to isolate.
- Q6 Hotfixes: V1 unchanged; no cherry-pick, no back-port step; in-release bug `dash1.3-fix<NN>-<slug>`.
- Q7 Clean-up: explicit deletion; story branch and worktree after ledger and push; line, worktree and remote branch after owner merge and open sync PR; tag; `.dev/` and `sprint-status.yaml` on the line; story tip reachable as second parent.
- Q8 Fit with Clay: V1 unchanged; asks the owner whether `integration` is still the branch Clay works from (24 PRs in its life, none merged since 2026-11-19).
- Q9 Rollback: `git revert -m 1`; revert the revert first before returning a story; a PR-reviewed story keeps its PR record; release failure: revert PR of the release merge commit, prefer a fix line.
- Owner decides: (1) confirm local coordinator merges (CONTEXT line 11); (2) story cap and time box; (3) whether to use review-only story PRs, with which size or risk rule, and whether CI on them is by a first-commit edit or by dispatch; (4) is `integration` still in use.

**Positions stated in the Round 2 table (winner, confidence)**: C-001 combined (V4/V1 `release/<rel>` folder, V2/V3 flat stories) 70; C-002 and X-001 V1 90; C-003 and X-002 V1 85; C-004 V1 default, V3 review-only PR as optional layer 60; C-005 and X-004 no winner (owner's call) 50; C-006 and X-005 V1 65; C-007 V2 for CI, V3 layer for bots, tie otherwise 60; C-008 V1 85; C-009 and X-007 V1/V3 (merge only) 75; C-010 V1 60; C-011 V2 for CI latency, V1 pre-merge guards, V3 layer adds bots 60; C-012 V1 with V3's time box 75; C-013 and X-006 combined (V1 line, V3 time box and ladder) 75; C-015 V1 85; C-016 V4 70; C-018 and X-003 V1 90; C-019 V1 and V4 55; C-020 and X-009 V1 90; C-021 V3 layer on selected stories plus V1's cap and digest 60; C-022 V1 at release level, V2 at slice level 65; C-023 V1 and V4 90; C-024 V4 55; C-025 and X-010 no winner; U-001 to U-003 V1 adopt 80; U-010 adopt 85; U-011 reserve only 60; U-012 adopt 80; U-013 adopt 90; U-014, U-015, U-017 V4 adopt 65; U-006 to U-009 V2 third rung only 55; A-008 QUALIFY improved 60; A-012 ACCEPT (changed from QUALIFY) 90; A-013 QUALIFY 75; A-014 QUALIFY narrowed 65; A-006 ACCEPT (changed from QUALIFY) 95; A-004 QUALIFY unchanged 65. Not contested by A3 any longer: S-001 to S-006, C-014, C-016, C-017; X-008 not contested.

### Variant 4 Rebuttal (adv-4, qa persona)
**Response to criticisms of Variant 4 (A4R2 section 1)**:

Settled, no further defence (already conceded in R1-C1 to R1-C4 and agreed by all four):
1. Merging `integration` into the release (A1-W13, A2-W13, A3-W10; X-003, C-018, A-017). Wrong; R1-E3 tested it; A1, A2, A3 all reject A-017.
2. When CI runs, X-008 (A1-W14, A2-W13, A3-W11) and the undefined base (A3-W12; C-002, X-001). Closed by dropping PR per story (gfxai-fit named change 1, R1-C1) and by "cut from `master`" (R1-C3).
3. Ledger and planning base (C-020, X-009), the long-lived cap (C-013), cherry-pick hotfixes (C-015). Conceded in R1-C4, R1-C7, R1-C6; A1R2, A2R2, A3R2 all adopt V1's version.

Conceded now because the new evidence forces it:
4. Three-level story names (A1-W17, A2R2 Q1, A3R2 Q1; C-001, A-007, A-011). M1: a worktree without `--branch` gets the prefixed default; `worker-start` has no `--branch` (CONTEXT line 12); a worktree named `dash1.3` gets `ironbelly/dash1.3`, after which `ironbelly/dash1.3/story/01-x` can never be created. Withdraws R1-S1 for story branches; keeps only the `release/<rel>` folder for the release line.
5. Squash into the release line (A1-S10, A1R2 section 5 C-005; C-005, X-004). Withdraws R1-S2's differentiator and R1-S3: (a) A1R2 section 3 item 1 shows revert-the-revert is clean, so the `--no-ff` trap was a missing procedure; (b) M5: `git bisect --first-parent` over six `--no-ff` story merges names `merge s4` as first bad commit; (c) A3R2's review-only story PR layer needs the local merge to be a merge commit for GitHub to show the PR merged (UNVERIFIED for a local squash); (d) M6: the cleanup tool keys on its own PR being merged. Keeps: merge commit only for the release PR, and plain `git revert <sha>` is marginally simpler than `-m 1`. C-005 is a tie, leaning `--no-ff`.
6. Release-sized review is the shape with in-repo evidence against it (A3-W14, A3R2 E4, A2-W15, A2R2 point 10; C-021, C-007). M9: #31 has 2,089 files, 0 reviews, 0 comments; the claim that its ten story PRs had no checks or reviews is A3's sample, not re-checked. Gives up the weight on R1-S8(b): promotions merged in 43, 17 and 27 minutes (A2 N2); a fast merge proves nothing broke, not that anyone read it. What stays: the lesson supports a story cap, a digest and an extra outside gate, not a ban on a release line.
7. "Closeout checks the merge method" (R1 strength table, R1 failure table row 4; A1R2 point 4 adopted it). Written as if it existed; M4: `branch-landed.sh` is squash-safe and reads `mergeCommit` and `baseRefName`; no assertion about the merge method; a two-parent check is new work. Retracted.
8. `/sc:worktrees` could remove an unpushed release worktree (R1-W2). Retracted; M6: removal requires its own PR merged and about six other conditions, every step fails closed. The forward-only push stays as a backup against disk loss or a manual `orca worktree rm`.

Contested, with counter-evidence:
9. "V4 adds mostly weak-fit pieces to V1" (A1-W15). Right about the original text, wrong about the surviving parts: the `release/<rel>` folder, the freeze, the explicit clean-up rule with delete step, the provenance marks, all adopted by the others.
10. "Provenance marks are documentation, not substance" (A1-W15). M7: nothing technical enforces any branching rule (no rulesets, `master` and `integration` unprotected), so seeing which rules rest on evidence is substance.
11. The thin source (A2-W14, A2-W15, A3-W13). Conceded in R1-C9 and R1-C10; unchanged; no weight asked for the GFxAI pedigree.

**Updated assessment of the other variants**:
- V1 (base of every combined design): adopts four of A1R2's additions (forward-only push A1R2-1, freeze A1R2-2, merge-method sentence A1R2-4 with the check as new work, never re-merge a reverted story branch directly); A1R2-6 right that the Clay collision lands on a sync branch then `integration`, and `git merge-tree` against `origin/integration` is the best cheap early warning. Changed mind against V1: A1R2 point 7 reads 17 to 43 minute promotions as reviewers taking roll-ups; sides with A2R2 point 10 and A3R2 point 11 (rubber stamp); V1's real review control is the cap, the digest and an outside gate. Did not change: V1 has no outside look at a single story unless the owner approves a dispatch run or a review-only PR.
- V2: `integration` is not a live trunk (M11: newest commit on `origin/integration` is #667, 2026-11-18 21:35 -0600); V2 as a base is out. Takes two pieces: spec-time classification of shared files and independent shippability (U-006, planning rule only) and judging every change by something other than the coordinator. Did not change: C-007 and C-011 stay V2's on detection latency. Disagrees with A2R2 Q2's hand-opened draft release PR: `/sc:pr-submit` has no open-as-draft flag, its guard flips drafts to ready (M10), the owner's rule is that PRs open only through `/sc:pr-submit`, draft behaviour of the bots is "unverified". A2R2 Q5 two lanes is reasonable but departs from CONTEXT line 7; put the test-only case to the owner as a question.
- V3: the best new idea of Round 2 is A3R2 Q2, the optional review-only story PR; M8 verifies its premise (bots reviewed PRs on non-default batch bases #484, #490, #491; #491 is the follow-up fix for #490). Price: no CI on those PRs, a top-level `/sc:pr-submit` session per story (A3-C10), two bot passes on top of the roll-up. Two cautions: (a) it needs the local merge to be a merge commit; (b) after the coordinator merges story A locally, story B's open PR has a moved base and `/sc:pr-submit` resolves that only as one merge commit of the recorded base tip pushed fast-forward (SKILL.md line 337), so the line must be pushed first. A3R2 route (a) (workflow edit as first commit) rests on two secondary sources (A3R2 E7, UNVERIFIED); route (b) `workflow_dispatch` has an in-repo precedent (M2) and should be the default.
- V4 (own variant, summary after two rounds): left in the combined design: the `release/<rel>` folder, beta freeze, explicit clean-up and delete-the-remote-branch rule, merge-method rule for the release PR, a fix-forward rule for hotfixes, the provenance marks. Not left: PR per story, the `integration` merge, squash, three-level names, the source's tiers and approvers, any claim that GFxAI pedigree counts as precedent.

**New evidence (read-only, 2026-11-23)**:
- M1 `orca worktree create --branch` (Orca 1.4.245 help): "Git branch name to use instead of the prefixed default"; with `--branch` the name is exact and unprefixed; "a taken name gets a numeric suffix", so read back the real name; whether a ref-conflicting name counts as "taken" is UNVERIFIED.
- M2 `workflow_dispatch` has already run on a non-listed branch: two runs on 2026-11-05 on `ci/parallel-python310-tests`, both success, 4 min 7 s and 5 min 1 s.
- M3 CI wall time of the last 40 `pull_request` runs: 31 succeeded; min 7.0, median 9.2, max 12.6 minutes; local suite time still unmeasured.
- M4 Closeout: `branch-landed.sh` is "Squash-safe", reads `mergeCommit`, `mergedBy`, `baseRefName`; no merge-method assertion anywhere in the closeout skill.
- M5 First-parent bisect over `--no-ff` story merges (scratch repo): reports "merge s4"; first-parent log 7 entries versus 26.
- M6 `scripts/worktree_cleanup.py`: a worktree is removed only when all eight rules hold (own PR merged, nothing added after it, issues closed, nothing unsaved, and others); fails closed; cannot remove an unmerged release worktree; a story worktree with no PR is kept, so local-merge designs need explicit removal; a review-only story PR can be retired only if GitHub shows it MERGED.
- M7 No rulesets; `master` unprotected (404); `integration` `protected: false`.
- M8 PRs #484, #490, #491 (base `346Claude-integration`): Augment and Codex reviewed #484 and #490, Augment on #491; `statusCheckRollup` length 0 on all three; #491 is the follow-up to #490.
- M9 #31 re-checked: base `master`, 2,089 files, merged 2026-05-12, 0 reviews, 0 comments; one grep found no revert (weak evidence of no harm).
- M10 `/sc:pr-submit`: no open-as-draft flag; at `--monitor 3` the guard turns the PR into a draft during a fix cycle and marks it ready afterwards; line 94: draft behaviour "unverified ... do not rely on it".
- M11 `integration` recency: newest commit `141e97fec` by clayphi, 2026-11-18 21:35 -0600 (#667); `master` has 26 commits `integration` lacks and `integration` has 2 `master` lacks.

**Combined design, question by question** (base V1; "(new)" marks a piece none of the four variants had; condensed):
- Q1 Names: `release/dash1.3`; stories flat `dash1.3-s04-<slug>`; in-release fix `dash1.3-fix01-<slug>`; docs-only `dash1.3-docs01-<slug>`; shipped-code fix `fix/<issue>-<slug>`; tag `dash-1.3`; invariant: no branch named exactly `release`; create with `orca worktree create --name <n> --branch <exact name> --base-branch <ref> --parent-worktree <selector> --agent claude` and read back the real name (new); a future 1.10 written 1.100; throwaway create first [U-013].
- Q2 Story merge: local, coordinator, `--no-ff`, one story at a time; path claims, shared-file list (`CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md`, docs index files; coordinator-owned or first foundation story; from the #662 stat), `git merge-tree` trial; after: targeted tests, ledger line before and after, forward-only push. Outside gate 1 (default, no workflow edit): `workflow_dispatch` on the pushed line after a story touching shared or risky paths and always on the final tip (M2, about 9 minutes each, M3; owner's nod for CI minutes). Outside gate 2 (optional per story): review-only story PR [A3R2 Q2]; threshold suggestion consistent with #490 versus #484, not measured. Conflicts as V1; parallelism two stories; re-open above about four.
- Q3 Staying current: merge `origin/master` in at start, between stories (never mid-merge) and before the PR; never `integration`; `git merge-tree` against `origin/integration`; path claims vs open `integration` PRs.
- Q4 Landing: one PR by `/sc:pr-submit --monitor 3 --base master`, "Merge this pull request with a merge commit, not squash", digest, path classes; closeout two-parent check (new, needs building); acceptance gate reduced from V4's tiers: freeze, green dispatch run on the final tip, full local suite, the owner; no two-approver rule; size controls are the cap and the optional story PRs; include the release PR in the throwaway test list because of the draft guard (M10).
- Q5 Flags and justification: no flags; time box with floating scope; starting numbers about six stories or seven days (estimates, not measurements); ladder: review-only PRs for every story, then dark-by-construction slices after a pilot; one-story release skips the line; whether a test-only release (1.105) may do the same is a question for the owner.
- Q6 Hotfixes: `fix/<issue>-<slug>` from `master`, picked up at the next merge-in, no cherry-pick; in-line fix `dash1.3-fix01-<slug>`; freeze after the last planned story; 1.1 bug-fix releases are ordinary lines.
- Q7 Clean-up: the coordinator removes story worktrees and any pushed story branch explicitly (M6; `delete_branch_on_merge` false) (new); release line deleted after owner merge and open sync PR, tag `dash-1.3`; records stay on the line.
- Q8 Fit with Clay: unchanged during the release; the coordinator opens the `master` into `integration` sync (five such commits by clayphi 2026-11-17 to 11-19); asks whether `integration` is still the branch Clay works from (M11).
- Q9 Rollback: `git revert -m 1` or fix forward; never merge a reverted story branch directly (revert the revert first); dependent stories in reverse order; `git bisect --first-parent` (M5, new); release failure: revert PR of the release merge commit, prefer a bug-fix line (#662 then #664 precedent); wrong merge method handled by the Q4 sentence and the two-parent check (M7: nothing can stop the click).
- Owner decides: (1) confirm local coordinator merges into the release line; (2) story cap and time box; (3) CI minutes for dispatch runs, and whether review-only story PRs are wanted and above what size; (4) is `integration` still in use; (5) story merge method, `--no-ff` (A4's lean) or squash.
- Throwaway tests before the first release: (a) `--branch` keeps the exact name, and behaviour for a ref-conflicting name; (b) a review-only story PR against `release/...`: both bots review, GitHub shows it merged after a local `--no-ff` merge and push; (c) the release PR at `--monitor 3` with the draft guard; (d) one dispatch run on the pushed line; (e) the two-parent check in closeout.

**Positions stated in the Round 2 diff-point table (winner, confidence)**: C-001 combined (V4 `release/<rel>` folder, V2/V3 flat stories) 70 (changed from R1 "partial"); C-002 and X-001 V1, V4 once it says so 90; C-003 and X-002 V1 (V4 agrees) 85; C-004 V1 default, V3 optional review-only PR layer 60; C-005 and X-004 no winner, leans `--no-ff` 55 (changed from R1 "win"); C-006 and X-005 V1 65; C-007 V2 for CI latency, combined dispatch plus V3 review-only layer for bots 60; C-008 V1 85; C-009 and X-007 V1 (merge only) 75; C-010 V1 60; C-011 V2 on latency, V1 guards before the merge, V3 layer adds bots 60; C-012 V1 with V3 time box 75; C-013 and X-006 combined (V1 line, V3 time box and ladder) 75; C-014 V1 70; C-015 V1 85; C-016 V4 80; C-018 V1 90; C-019 V1 and V4 60; C-020 and X-009 V1 90; C-021 combined (V1 cap and digest, V3 optional story PRs; V2/V3 win per-unit review) 60; C-022 V1 at release and story level, V2 at slice level 65 (changed from R1); C-023 V4 and V1 85; C-024 V4 55; C-025 and X-010 no winner; X-008 resolved; U-001 to U-003 V1 adopt 80; U-006 V2 as a planning rule only 55; U-010 to U-013 V3 adopt 85; U-014 and U-015 V4 adopt 65; U-016 flat form only 50; U-017 V4 as wording 55; U-018 V4 reduced 55; S-002 V4 55; S-003 and S-005 V1, V2, V3 80 (conceded). Assumptions: A-001 QUALIFY 70; A-002 QUALIFY 70; A-003 QUALIFY 65; A-004 QUALIFY 65; A-005 REJECT 70; A-006 ACCEPT 95; A-007 QUALIFY 65; A-008 QUALIFY 60; A-009 QUALIFY 65; A-010 QUALIFY 70; A-011 QUALIFY 75; A-012 ACCEPT (changed from R1 QUALIFY) 90; A-013 QUALIFY 70; A-014 QUALIFY 65; A-015 ACCEPT 80; A-016 QUALIFY 65; A-017 REJECT 95.

**A4R2 section 6: points where all four advocates now agree (as stated by A4)**: 1. Base `master`; one PR into `master` through `/sc:pr-submit --monitor 3 --base master` (C-002, X-001, C-003, X-002). 2. `integration` never merged into the release line (X-003, C-018, A-017). 3. Merge `master` only, never rebase after first push, `git merge-tree` against `origin/integration` (C-008, C-009, X-007, U-001, U-003). 4. Ledger and `.dev/` records on the release line; planning starts from `master` (C-020, X-009). 5. Hotfixes `fix/<issue>-<slug>` from `master`, no cherry-pick (C-015). 6. Freeze after the last planned story (C-016). 7. Explicit clean-up including the remote branch (C-023, A-006 ACCEPT). 8. Forward-only push of the release line after each story merge. 9. Release line `release/<rel>`; tag `dash-1.3`; shipped-code fix on `fix/` (C-001 for the release line, C-024). 10. Revert-then-redo needs a stated procedure (C-005 trap, C-022). 11. No flags in the base; time box with floating scope; ladder to per-story PRs then V2 slicing (C-012, C-013, X-006, U-010). 12. Adopt U-001 to U-003, U-010, U-012, U-013, U-014, U-015; U-006 to U-009 third-rung only. 13. X-008 resolved; C-025 and X-010 dropped. 14. A-017 REJECT, A-006 ACCEPT, A-012 ACCEPT, A-005 and A-010 QUALIFY. 15. Local coordinator merges need the owner's explicit confirmation in chat (A-014).

**A4R2 section 7: points still contested (as stated by A4)**: 1. Story branch shape (C-001): A1R2 keeps `dash1.3/s04-slug`; A2R2, A3R2 and A4 use flat names; a throwaway create settles the prefix. 2. Story merge method (C-005, X-004): A1R2 leans `--no-ff` (55), A2R2 and A3R2 no winner (50), A4 leans `--no-ff` (55); the owner's call. 3. How much outside gate a story gets (C-004, C-007, C-011, C-021): A1R2 dispatch on request; A2R2 dispatch after each story plus a hand-opened draft PR to be tested; A3R2 dispatch plus an optional review-only PR and a first-commit workflow edit; A4 dispatch default plus the optional review-only layer, rejecting the hand-opened draft PR; three tests decide. 4. Numbers for the cap and time box: A2R2 and A3R2 about six stories or seven days; A1R2 and A4 owner decides. 5. Whether 1.1 and 1.105 releases need a line (C-017): A2R2 and A3R2 no line; A1R2 and A4 ordinary lines with a one-story skip, test-only as an owner question. 6. Who runs the `master` into `integration` sync (C-019, A-015) and whether `integration` is in use. 7. Release PR acceptance gate content (U-018). 8. Where the workflow file is read for a `pull_request` run (A-008). 9. Who may merge a review-only story PR (A-014): the coordinator locally, never by a click (A3R2, A4) against the owner by click. 10. Value of the GFxAI pedigree (U-015, U-014): A4 gives no weight; A1R2 gives U-014 and U-015 65; A3R2 the same.

## Scoring Matrix

### How to read the matrix
- Columns 1 to 4 follow the template (Diff Point, Winner, Confidence, Evidence Summary). The extra columns give the taxonomy level, each advocate's stated position in Round 1 and Round 2 (order A1 / A2 / A3 / A4), and the agreement class.
- Position codes: V1 to V4 = that variant; "comb" = a combined design (parts named); "tie" = the advocate said there is no decisive difference; "conc" = the advocate conceded the point (to the variant named); "n/s" = no stated position; "n/r" = not restated in Round 2 (assumption rows only: the Round 1 verdict stands and is used as the latest position, because Round 2 did not retract it). For A rows the position is the verdict ACCEPT, REJECT or QUALIFY, and the "winner" is the consensus verdict, not a variant.
- Agreement is computed on each advocate's latest stated position (Round 2 if stated, else Round 1). Classes: Unanimous (all four name the same winner or verdict), Majority (at least three of four), No-contest (no latest position names a contested winner; at most two advocates name a winner and none dissents), Split (anything else, unresolved, confidence 50).
- Confidence follows the protocol: 90 to 100 unanimous with strong evidence, 70 to 89 clear majority, 50 to 69 contested or slight edge, split = 50, +10 when a losing advocate conceded, never 100 unless every advocate conceded (not used here).

Separator inside the R1 and R2 columns is a semicolon, in the order A1 ; A2 ; A3 ; A4.

### Structural points (S-001 to S-006)

| Diff Point | Winner | Confidence | Evidence Summary | Level | R1 (A1 ; A2 ; A3 ; A4) | R2 (A1 ; A2 ; A3 ; A4) | Agreement |
|------------|--------|------------|------------------|-------|------------------------|------------------------|-----------|
| S-001 | none (tie) | 55% | Nobody contests document organization. A3 claimed V3's Open decisions section in R1 (with S-005) and no longer contests it in R2. | L2 | n/s ; tie ; V3 ; n/s | not contested ; not contested ; not contested ; n/s | No-contest |
| S-002 | V4 (uncontested) | 60% | A3 conceded S-002 to V4 in R1 and A4 claims it: the marks show which rules rest on evidence, which matters because nothing enforces the rules (A4 M7). A1 and A3 adopt U-014 in the merged text. | L2 | n/s ; tie ; conc V4 ; V4 | not contested ; not contested ; not contested ; V4 55 | No-contest |
| S-003 | V1, V2, V3 (have a diagram; V4 has none) | 65% | A4 conceded in R1 and R2 (80). Others do not contest. | L1 | n/s ; tie ; not claimed ; conc V1 V2 V3 | not contested ; not contested ; not contested ; conc V1 V2 V3 80 | No-contest |
| S-004 | none (tie) | 55% | Formatting only. A3 marks it not claimed; nobody claims a win. | L1 | n/s ; tie ; not claimed ; n/s | not contested ; not contested ; not contested ; n/s | No-contest |
| S-005 | V1, V2, V3 (costs, risks, favours sections; V3 adds Open decisions) | 65% | A4 conceded in R1 and R2 (80). A3's R1 claim was withdrawn. All four adopt U-012 (open-decisions list) in their Round 2 designs. | L2 | n/s ; tie ; V3 ; conc V1 V2 V3 | not contested ; not contested ; not contested ; conc V1 V2 V3 80 | No-contest |
| S-006 | none (tie) | 55% | Heading style only. A3 marks it not claimed; nobody claims a win. | L1 | n/s ; tie ; not claimed ; n/s | not contested ; not contested ; not contested ; n/s | No-contest |

### Content points (C-001 to C-025)

| Diff Point | Winner | Confidence | Evidence Summary | Level | R1 (A1 ; A2 ; A3 ; A4) | R2 (A1 ; A2 ; A3 ; A4) | Agreement |
|------------|--------|------------|------------------|-------|------------------------|------------------------|-----------|
| C-001 | combined: `release/<rel>` folder (V4) plus flat story names (V2, V3) | 72% | A2, A3, A4 converge on it in R2: Orca names a branch `ironbelly/<worktree name>`, so a worktree called `dash1.3` blocks `ironbelly/dash1.3/s04-...` with the "cannot lock ref" error (A4 M1, A2 N5, CONTEXT line 8); A4 E1 shows folders coexist when nobody creates the bare token. A1 keeps `dash1.3/s04-slug` story folders (60). | L3 | tie ; V2 (resilience, narrow) ; tie with V2, better than V1 and V4 ; partial (wins on grouping over V1, loses to V2 V3 on robustness) | comb (V4 release folder, V1 story names) 60 ; comb (V4 release folder, V2 V3 flat) 70 ; comb (V4 V1 release folder, V2 V3 flat) 70 ; comb (V4 release folder, V2 V3 flat) 70 | Majority (3 of 4) |
| C-002 | V1 (cut from `master`) | 95% | All four agree in R2; A2 and A3 conceded. `master` is 26 commits ahead of `integration`, which has had no merged PR since 2026-11-19 (A1R2 item 5, A2 N1 and N3, A3 E1, A4 M11). | L2 | V1 ; draw V2 V3 ; V3 over V4, no claim over V1 ; V1 or V4 (conditional on V4 saying so) | V1 85 ; conc V1 85 ; conc V1 90 ; V1 90 | Unanimous |
| C-003 | V1 (one PR into `master`) | 92% | A2 and A3 withdrew the landing through `integration` after the data (0 of the owner's 130 PRs went through it, A2 N1); V4 agrees with V1. Reason of the owner's model (CONTEXT line 7). | L2 | V1 (V4 agrees) ; V2 (V3 tie) ; V3 (conceding C-018) ; V1 (tie V4) | V1 and V4 75 ; V1 70 ; V1 85 ; V1 85 | Unanimous |
| C-004 | V1 default (local coordinator merge); V3 review-only story PR as optional layer | 72% | All four keep the local `--no-ff` merge as the default in R2. A3 and A4 add an optional review-only story PR (bots reviewed non-default bases, A3 E2, A4 M8); A1 and A2 do not adopt it. The optional-layer question stays open under C-007 and C-021. | L2 | V1 ; no winner (V2 best for review size, V1 for owner effort) ; V3 ; tie V1 (after named change 1) | V1 60 ; V1 65 ; V1 default plus V3 optional layer 60 ; V1 default plus V3 optional layer 60 | Unanimous (on the default) |
| C-005 | unresolved (owner's call; design default `--no-ff`) | 50% | A1 narrowly V1 (55); A2 and A3 no winner (50); A4 no winner, leaning `--no-ff` (55). Trap and remedy both verified (A4 E2, A1R2 item 3.1: revert the revert first); `git bisect --first-parent` gives story-level granularity (A4 M5); squash keeps a simpler revert. | L3 | V1 (`--no-ff`) ; claims slice granularity and trap avoidance (V2) ; no win ; V4 (squash) | V1 narrowly 55 ; no winner (V1 `--no-ff` locally adequate) 50 ; no winner, owner's call 50 ; no winner, leans `--no-ff` 55 | Split |
| C-006 | V1 (coordinator merges locally; owner confirms in chat) | 75% | All four V1 in R2 (60 to 65): local merge into a pushed line is a smaller authority class than merging GitHub PRs. Owner confirmation still required (A-014; CONTEXT line 11 "to be confirmed"). | L3 | V1 ; V1 (owner effort; V2 wins only rule consistency) ; V3 ; tie V1 (after named change 1) | V1 60 ; V1 60 ; V1 65 ; V1 65 | Unanimous |
| C-007 | V2 (best per-change CI and reviewer coverage) | 72% | All four name V2 for per-change CI in R2; A3 and A4 add that the design uses dispatch runs plus an optional review-only PR for the bots (bots verified on non-default bases but no CI there: A3 E2, A4 M8; dispatch precedent A4 M2, about 9 minutes A4 M3). How much outside gate a story gets stays open. | L2 | conc V2 (and V3) ; V2 ; V2 for CI (beats V1, ties V4) ; conc V2 V3 | V2 70 ; V2 70 ; V2 for CI, V3 layer for bots 60 ; V2 for CI latency, dispatch plus V3 layer for bots 60 | Unanimous (with qualification) |
| C-008 | V1 (merge `master` only) | 90% | All four V1; V4 conceded the `integration` merge, A2 and A3 withdrew theirs. | L3 | V1 ; V2 (no long-lived line) ; V3 beats V4, V1 coherent ; master-only (conc 2) | V1 80 ; V1 75 ; V1 85 ; V1 85 | Unanimous |
| C-009 | V1 (merge only, no carve-out) | 82% | All four converge on merge only after publication; low stakes. | L3 | V1 ; tie ; tie V1 V2, beats V4 ; tie | V1 70 ; V1 70 ; V1 or V3 (merge only) 75 ; V1 75 | Unanimous |
| C-010 | V1 (coordinator stops, story worker merges the line tip and re-gates) | 66% | A2, A3, A4 V1 in R2 once `integration` is not merged in (no train-versus-`integration` conflict to route). A1 splits V1 and V3 (50), keeping V3's sync branch (U-011) as a reserve. | L3 | draw (close) ; V2 ; V3 ; n/s | split V1 V3 50 ; V1 (sync branch unused) 55 ; V1 60 ; V1 60 | Majority (3 of 4) |
| C-011 | combined: V2 on detection latency, V1 on pre-merge guards (V3 layer adds bots) | 68% | A1, A3, A4 state this combination; A2 names V2 for latency and says V1's guards reduce but do not remove the gap. The suite behind all of them is the same (A-005). | L3 | split (V1 guards pre-merge, V2 V3 CI post-merge) ; V2 ; V3 (equal V2, ahead of V1 V4) ; lose (V2 V3 get CI) | split V2 V3 latency, V1 guards 65 ; V2 65 ; V2 latency, V1 guards, V3 bots 60 ; V2 latency, V1 guards, V3 bots 60 | Majority (3 of 4) |
| C-012 | V1 (no flags) with V3's time box | 85% | All four; A2 conceded (a dark slice on `integration` can ship at Clay's promotion timing, A2 N2; dark landing unproven). | L2 | V1 over V2, V3 rule better ; conc V1 V3 on certainty, V2 on speed ; V3 ; n/s (V2 weakness 7) | V1 with V3 rule 65 ; V1 and V3 (no flags) 70 ; V1 with V3 time box 75 ; V1 with V3 time box 75 | Unanimous |
| C-013 | combined: V1 line, V3 time box and ladder, hard cap | 86% | All four combined; A4 conceded (no cap in V4) and A2 conceded (V2's no-long-line does not fit the owner's model). Starting numbers (about six stories or seven days) are estimates, not measurements. | L2 | V1 conditional (days, not weeks) ; V2 ; V3 ; lose as written | comb 65 ; comb 65 ; comb 75 ; comb 75 | Unanimous |
| C-014 | V1 (one story, one branch, one worktree), uncontested | 65% | Only A4 names a winner in R2 (70); A1, A2, A3 do not contest. | L2 | no meaningful difference ; no winner (V2 best review size, V1 owner effort) ; tie ; n/s | not contested ; not contested ; not contested ; V1 70 | No-contest |
| C-015 | V1 (no cherry-pick, no back-port step) | 93% | A3 and A4 conceded in R1, A2 in R2 (the cherry-pick path can conflict later, A2 N7). | L3 | V1 ; tie ; conc V1 ; conc V1 | V1 85 ; V1 85 ; V1 85 ; V1 85 | Unanimous |
| C-016 | V4 (freeze after the last planned story; only `-fix` branches) | 90% | Adopted by all four in R2 after A4's R1 argument; costs the coordinator one refusal rule. | L3 | tie ; tie ; tie ; V4 | V4 75 ; V4 70 ; V4 70 ; V4 80 | Unanimous |
| C-017 | unresolved | 50% | A1 and A4 keep 1.1 and 1.105 as ordinary release lines with a one-story skip (A4 asks the owner about test-only); A2 and A3 propose no line for bug-fix and test-only releases (small direct PRs into `master`). A1, A2, A3 list C-017 as not contested while their designs differ; A4 section 7 item 5 lists it as contested. | L2 | tie ; tie ; tie ; n/s | ordinary line, one-story skip ; direct PRs, no line (two lanes) ; direct PRs, no line ; ordinary line, test-only an owner question | Split |
| C-018 | V1 (keeps Clay's unreleased work out of the release PR) | 96% | All four; A2, A3, A4 conceded; mechanic tested by A4 E3. | L3 | V1 ; conc V1 ; conc V1 ; conc V1 | V1 85 ; V1 90 ; V1 90 ; V1 90 | Unanimous |
| C-019 | V1 and V4 (the sync is the price of landing on `master`) | 62% | All four in R2; who runs the `master` into `integration` sync is UNVERIFIED (A-015). A3's R1 claim for V3 (smallest obligation) was dropped. | L3 | tie ; tie ; V3 ; tie V1 | V1 and V4 55 ; V1 and V4 55 ; V1 and V4 55 ; V1 and V4 60 | Unanimous |
| C-020 | V1 (ledger and `.dev/` on the release line) | 96% | Conceded by A2, A3, A4 in R1; planning of release n+1 starts from `master`. | L2 | V1 ; conc V1 (V3 second) ; conc V1 ; conc V1 | V1 90 ; V1 90 ; V1 90 ; V1 90 | Unanimous |
| C-021 | combined: V2 and V3 win per-unit review, V1 cap and digest as the control, optional V3 story PRs | 70% | All four name V2 and V3 on per-unit review and keep V1's cap and digest; roll-up merge times of 17 to 43 minutes show depth is not there (A2 N2, A3 E3 and E4, A4 M9). A1 and A4 concede V1 and V4's release-size weakness. | L2 | conc V2 V3 ; V2 V3 beat V1 V4 (tie on roll-up) ; V3 (ahead of V1 V4, equal V2) ; conc V2 V3 | V2 and V3 60 ; V2 V3 on review quality, cap is V1's control 60 ; V3 layer on selected stories plus V1 cap and digest 60 ; comb (V1 cap and digest, V3 optional story PRs) 60 | Unanimous |
| C-022 | V1 at release and story level, V2 at slice level | 78% | All four; A4 withdrew its R1 squash edge. Slice-level undo and flag-off exist only on the third rung. | L3 | V1 at release level, V3 story draw, V2 slice ; V2 (slice granularity, avoids re-merge trap) ; ahead of V1 V4 on layers, behind V2 ; V4 (V2 wins flag-off) | V1 release, V2 slice 65 ; V1 release, V2 slice 65 ; V1 release, V2 slice 65 ; V1 release and story, V2 slice 65 | Unanimous |
| C-023 | V1 and V4 (explicit deletion) | 92% | `delete_branch_on_merge` is false (A4 E6, A1R2 item 3.3, A2 N8); V2 and V3 conceded their reliance on auto-delete. | L2 | tie ; tie ; tie (V4 rule better than V3's setting) ; V4 (tie V1) | V1 and V4 85 ; V1 and V4 85 ; V1 and V4 90 ; V4 and V1 85 | Unanimous |
| C-024 | V4 (`dash-1.3`) | 72% | Same value as V1's `dash/1.3` without a `dash/` folder; trivial. A2 uses `dash-1.3` in its Q1 design and lists C-024 as not contested. | L1 | V4 (slightly safer) ; tie ; tie ; n/s | V4 55 ; not contested ; V4 55 ; V4 55 | Majority (3 of 4) |
| C-025 | none (moot under local merges) | 75% | Nobody names a winner in R2: nothing is stacked when story merges are local. | L2 | no meaningful difference ; no decisive difference ; V3 (only stated stack policy) ; n/s | not contested ; not contested ; no winner (dropped) ; no winner | No-contest |

### Contradiction points (X-001 to X-010)

| Diff Point | Winner | Confidence | Evidence Summary | Level | R1 (A1 ; A2 ; A3 ; A4) | R2 (A1 ; A2 ; A3 ; A4) | Agreement |
|------------|--------|------------|------------------|-------|------------------------|------------------------|-----------|
| X-001 | V1 (base `master`) | 95% | Same evidence and positions as C-002: all four agree in R2, A2 and A3 conceded, `master` 26 ahead and `integration` quiet since 2026-11-19. | L2 | V1 ; V2 (cut from `integration` agrees with the documented flow) ; V3 beats V4's silence, no claim over V1 ; V1 or V4 (conditional) | V1 85 ; conc V1 85 ; conc V1 90 ; V1 90 | Unanimous |
| X-002 | V1 (direct landing into `master`) | 92% | Same evidence and positions as C-003: A2 and A3 withdrew the landing through `integration`; V4 agrees with V1. | L2 | V1 ; V2 (V3) ; V3 ; V1 (tie V4) | V1 and V4 75 ; V1 70 ; V1 85 ; V1 85 | Unanimous |
| X-003 | V1 (`integration` is not merged into the release line) | 97% | A4 E3 scratch test: `git diff --stat master...release/dash1.3` lists the `integration` commit's file. A4 conceded; A2 and A3 conceded to V1 on C-018 and X-003. | L3 | V1 (V4 contradicts itself) ; V1 and V2 consistent, V4 not (tie with V1) ; V3 consistent, V4 not (C-018 to V1) ; conc V1 | V1 95 ; V1 90 ; V1 90 ; V1 90 | Unanimous |
| X-004 | unresolved (owner's call; design default `--no-ff`) | 50% | Same evidence and positions as C-005. | L3 | V1 ; no claim ; split, no win ; V4 (win over V1 and V3, tie V2) | V1 narrowly 55 ; no winner 50 ; no winner 50 ; no winner, leans `--no-ff` 55 | Split |
| X-005 | V1 (coordinator merges locally; owner confirms in chat) | 75% | Same evidence and positions as C-006. | L3 | V1 ; V1 (owner effort) ; V3 ; tie V1 | V1 60 ; V1 60 ; V1 65 ; V1 65 | Unanimous |
| X-006 | combined: V1 line, V3 time box and ladder | 86% | Same evidence and positions as C-013. | L2 | V1 conditional (loses to V3's time box) ; V2 ; V3 ; lose as written | comb 65 ; comb 65 ; comb 75 ; comb 75 | Unanimous |
| X-007 | V1 (merge only, no carve-out) | 82% | Same evidence and positions as C-009; the Round 2 rows of all four pick V1's merge-only rule. | L3 | V1 ; tie with V4 (V1 V3 stricter) ; tie with V1 V2, beats V4 ; tie | V1 70 ; V1 70 ; V1 or V3 75 ; V1 75 | Unanimous |
| X-008 | none (V4 as written lost; resolved by dropping PR per story) | 85% | A4 conceded the contradiction (A4-C1) and resolved it with gfxai-fit named change 1; the others no longer contest it. | L3 | no point either way ; V2 (by default) ; V3 (V3 consistent, V4 not) ; conc (lose) | not contested ; not contested ; not contested ; resolved | No-contest |
| X-009 | V1 (planning of n+1 starts from `master`) | 96% | Same evidence and positions as C-020; cutting from `master` also removes V3's planning-base cost. | L2 | V1 ; conc V1 (V2 silent) ; conc V1 (V3 changes it) ; conc V1 | V1 90 ; V1 90 ; V1 90 ; V1 90 | Unanimous |
| X-010 | none (moot under local merges) | 75% | A2 and A3 withdrew their R1 claims; nobody names a winner in R2. | L2 | n/s ; V2 ("do not stack") ; V3 (stack policy) ; n/s | not contested ; not contested ; no winner (dropped) ; no winner | No-contest |

### Shared-assumption points (A-001 to A-017)

For these rows the "Winner" column holds the consensus verdict. R2 "n/r" means the advocate did not restate the verdict in Round 2, so the Round 1 verdict is the latest stated position. Abbreviations: Q = QUALIFY, ACC = ACCEPT, REJ = REJECT.

| Diff Point | Winner (verdict) | Confidence | Evidence Summary | Level | R1 (A1 ; A2 ; A3 ; A4) | R2 (A1 ; A2 ; A3 ; A4) | Agreement |
|------------|------------------|------------|------------------|-------|------------------------|------------------------|-----------|
| A-001 | QUALIFY | 88% | Disjoint path claims are necessary, not sufficient; partitionability of the dashboard stories is untested; A4 adds a shared-file list taken from the #662 stat. | L3 | Q ; Q ; Q ; Q | n/r ; n/r ; n/r ; Q 70 | Unanimous |
| A-002 | QUALIFY | 86% | Ledger line before and after each merge plus a forward-only push of the line let a successor coordinator resume (A1R2-1, A4). | L3 | Q ; Q ; Q ; Q | n/r ; n/r ; n/r ; Q 70 | Unanimous |
| A-003 | QUALIFY | 88% | The owner lands about 5.7 merged PRs a day (A2 N1; A4 E5), so click volume is not impossible; one large read is a different load. | L3 | Q ; Q ; Q ; Q | Q (updated) 65 ; Q (updated) 65 ; n/r ; Q 65 | Unanimous |
| A-004 | QUALIFY | 88% | Two parallel stories fit one serial lane; re-open the design above about four. | L3 | Q ; Q ; Q ; Q | n/r ; n/r ; Q 65 ; Q 65 | Unanimous |
| A-005 | QUALIFY | 78% | A4 says REJECT as a premise but agrees with the others' wording "necessary, not sufficient"; dashboard test coverage is unmeasured by anyone. | L3 | Q ; Q ; Q ; REJ | Q 70 ; Q 70 ; n/r ; REJ 70 | Majority (3 of 4) |
| A-006 | ACCEPT | 96% | Verified by `gh api`: squash, merge commit and rebase are all allowed (A4 E6, A1R2 item 3.3, A2 N8); nothing stops a wrong click (#658; A4 M7: no rulesets). | L2 | Q ; Q ; Q ; ACC | ACC (changed) 95 ; ACC (changed) 95 ; ACC (changed) 95 ; ACC 95 | Unanimous |
| A-007 | QUALIFY | 88% | One throwaway `orca worktree create --branch` settles name handling; A4 M1 documents exact-name behaviour with `--branch`. | L2 | Q ; Q ; Q ; Q | n/r ; n/r ; n/r ; Q 65 | Unanimous |
| A-008 | unresolved (A1, A2 ACCEPT; A3, A4 QUALIFY) | 50% | A1 and A2 accept it as a V3 and V4 only dependency; A3 and A4 qualify because the default route (dispatch) avoids the question. Where GitHub reads the workflow file for a `pull_request` run is UNVERIFIED (A3 E7, secondary sources). | L2 | ACC ; Q ; Q ; Q | ACC 80 ; ACC (V3 and V4 only, changed) 80 ; Q (improved) 60 ; Q 60 | Split |
| A-009 | QUALIFY | 88% | Path classes and the digest in the release PR body; whether the bots can skip `.dev/**` is UNVERIFIED. | L2 | Q ; Q ; Q ; Q | n/r ; n/r ; n/r ; Q 65 | Unanimous |
| A-010 | QUALIFY | 88% | CI wall time median 9.2 minutes (A4 M3); the local suite time is unmeasured. | L2 | Q ; Q ; Q ; Q | Q 70 ; n/r ; n/r ; Q 70 | Unanimous |
| A-011 | unresolved (A1, A2 ACCEPT; A3, A4 QUALIFY) | 50% | Verdicts split 2 to 2 and only A4 restated one in R2 (Q 75), but the substance converges: all four plan one throwaway `orca worktree create --branch` check, and A4 M1 reports `--branch` gives the exact name and "a taken name gets a numeric suffix". | L2 | ACC ; ACC ; Q ; Q | n/r (plans the throwaway check) ; n/r ; n/r ; Q 75 | Split |
| A-012 | ACCEPT | 96% | Verified in this repository: Augment and Codex reviewed PRs into the non-default `346Claude-integration` base (#484, #490, #491; also #492, #493 per A3); CI did not run there (A3 E2, A4 M8). | L2 | ACC ; ACC ; Q ; Q | ACC 80 ; ACC (V3 and V4 only) 80 ; ACC (changed) 90 ; ACC (changed) 90 | Unanimous |
| A-013 | unresolved (A1, A2 ACCEPT; A3, A4 QUALIFY) | 50% | A1 and A2 treat the `test.yml` edit as an open owner decision for V3 and V4; A3 and A4 say the default route (dispatch) needs no edit, so it matters only if CI on story PRs is wanted. | L2 | ACC ; ACC ; Q ; Q | ACC 80 ; n/r ; Q 75 ; Q 70 | Split |
| A-014 | QUALIFY | 88% | Needed only for local merges into the release line; the owner confirms in chat (CONTEXT line 11 "to be confirmed"). | L3 | Q ; Q ; Q ; Q | n/r ; n/r ; Q (narrowed) 65 ; Q 65 | Unanimous |
| A-015 | unresolved (A1, A2 QUALIFY; A3, A4 ACCEPT) | 50% | Substance converges (assign the sync explicitly for dashboard releases; who does it today is UNVERIFIED; A4 E4 lists five manual sync commits by clayphi 2026-11-17 to 11-19) but verdicts split 2 to 2 after A2 changed ACCEPT to QUALIFY in R2. | L3 | Q ; ACC ; ACC ; ACC | n/r ; Q (changed) 60 ; n/r ; ACC 80 | Split |
| A-016 | QUALIFY | 78% | Review is the bottleneck, but PR count, merge method (#658) and merge speed also matter (A1, A4). | L2 | Q ; Q ; ACC ; Q | n/r ; n/r ; n/r ; Q 65 | Majority (3 of 4) |
| A-017 | REJECT | 97% | A4 E3 scratch test: merging `integration` into the release line puts its commits in the PR to `master`. All four reject; V4's own advocate conceded. | L3 | REJ ; REJ ; REJ ; REJ | REJ 95 ; REJ 90 ; REJ (stated in section 2) ; REJ 95 | Unanimous |

### Unique contributions (U-001 to U-018): keep or drop

U points are contributions, not competing positions, so the "Winner" column holds the verdict (Keep, Keep reduced, Fallback only, Drop). They are scored but are not part of the convergence denominator (the protocol formula counts S, C, X and A points only). Round 1 "adopt" means the advocate said the other variant's idea should be imported into a merged proposal.

| Diff Point | Verdict | Confidence | Evidence Summary | Level | R1 (A1 ; A2 ; A3 ; A4) | R2 (A1 ; A2 ; A3 ; A4) | Agreement |
|------------|---------|------------|------------------|-------|------------------------|------------------------|-----------|
| U-001 | Keep | 92% | `git merge-tree` trial before each story merge; A1R2 extends it to a run against `origin/integration` at each `master` merge-in. | L3 | keep (own) ; n/s ; adopt ; adopt | keep 80 ; adopt 80 ; adopt 80 ; adopt 80 | Unanimous |
| U-002 | Keep | 92% | Per-story digest in the release PR body, as the control for release size. | L2 | keep (own) ; n/s ; adopt ; adopt | keep 80 ; adopt 80 ; adopt 80 ; adopt 80 | Unanimous |
| U-003 | Keep | 93% | Path-claim comparison against open `integration` PRs at release start; early warning for Clay collisions. | L3 | keep (own) ; carry ; n/s ; adopt | keep 80 ; adopt 80 ; adopt 80 ; adopt 80 | Unanimous |
| U-004 | Drop | 65% | A2, A3, A4 use `release/` plus flat story names in R2; A1 keeps `dash1.3/s04-slug` story folders. A1 R1 called it a low value plus; A3 R1 conceded flat names group worse. | L1 | low plus, not claimed ; n/s ; conc flat names group worse ; n/s | keeps story folders ; flat stories, `release/` folder only ; flat stories, `release/` folder only ; flat stories, `release/` folder only | Majority (3 of 4) |
| U-005 | Keep | 65% | Reverse-order revert of dependent stories appears in A1R2 Q9 and A4R2 Q9; A2 and A3 do not address it. | L3 | keep (own) ; n/s ; criticised as manual (A3-W4) ; n/s | keep (Q9) ; n/s ; n/s ; keep (Q9) | No-contest |
| U-006 | Keep reduced (planning rule; third-rung fallback) | 60% | All four keep it only as a spec-time planning rule or as the third-rung fallback, not as base design. | L2 | not needed in V1 ; keep ; better idea than V3's, conceded ; n/s | fallback (third rung) 60 ; planning rule 60 ; third rung only 55 ; planning rule only 55 | Unanimous |
| U-007 | Drop from base (fallback only) | 60% | A1 and A3 group it with the third rung; A2 keeps it "in spirit only" (40); the cap and time box carry the "keep the line short" intent. | L3 | n/s (group loss) ; keep ; n/s ; n/s | not adopted in base 60 ; in spirit only 40 ; third rung only 55 ; n/s | Majority (3 of 4) |
| U-008 | Fallback only | 60% | Flag retirement matters only if dark landing is used, which is the third rung. | L2 | n/s (group loss) ; keep ; n/s ; n/s | third rung (group) 60 ; third rung only 55 ; third rung only (group) 55 ; n/s | Majority (3 of 4) |
| U-009 | Fallback only (pilot first) | 65% | All four: the pilot comes before any dark landing; A4 Q5 ladder says "only after a pilot". | L2 | n/s (group loss) ; keep (extended by U-013) ; n/s (criticises dark landing as unproven) ; n/s | third rung (group) 60 ; third rung only 55 ; after a pilot 55 ; ladder: only after a pilot | Unanimous |
| U-010 | Keep | 95% | Time box with floating scope adopted by all four in R2; A1 conceded it is better than V1's justification. | L2 | adopt (conc 7) ; carry (as fallback) ; keep ; n/s | adopt 75 ; adopt 80 ; adopt 85 ; adopt 85 | Unanimous |
| U-011 | Fallback only (reserve) | 70% | `dash1.3-sync<N>` is needed only if `integration` is merged into the line, which no one now does. | L2 | not needed in V1 ; n/s ; keep ; n/s | not needed while no `integration` merge-in ; unused ; reserve only 60 ; reserve only | Unanimous |
| U-012 | Keep | 92% | One owner decision list, appended to each Round 2 design. | L2 | adopt (conc 7) ; n/s ; keep ; n/s | adopt 75 ; adopt 80 ; adopt 80 ; adopt 85 | Unanimous |
| U-013 | Keep | 96% | Throwaway test before relying on a prefix, CI filter or merged-by-push state; A3 counts three jobs for it, A4 five. | L3 | adopt (conc 7) ; carry ; keep (load-bearing) ; adopt | adopt 75 ; adopt 80 ; adopt 90 ; adopt 85 | Unanimous |
| U-014 | Keep | 78% | Provenance marks adopted in the merged text by A1, A3, A4; A2 does not state a position on it in R2. | L2 | adopt (conc 7) ; n/s ; conc to V4 ; claims | adopt 65 ; n/s ; adopt 65 ; adopt 65 | Majority (3 of 4) |
| U-015 | Keep (as size evidence, no precedent weight) | 72% | PR #147 plus in-repo #640, #664, #31 as size evidence; A4 asks that the GFxAI pedigree not be weighed as precedent. | L2 | adopt (PR #147 as the size warning) ; n/s ; conc to V4 ; claims (weighed both ways) | adopt 65 ; n/s ; adopt 65 ; adopt 65 | Majority (3 of 4) |
| U-016 | Drop (folder form); flat names carry the kind | 55% | Only A4 states a position (flat form only, 50); A2, A3, A4 designs use `dash1.3-fix01-...` and `fix/` with no `story/bugfix/docs` folders or `hotfix/` prefix; A1's design uses `dash1.3/fix-01-slug`. | L1 | n/s ; n/s ; n/s ; claims (auditability); concession 5 drops the new prefixes | n/s ; n/s ; n/s ; flat form only 50 | No-contest |
| U-017 | Keep (as wording of what the owner rule forbids) | 72% | A1R2, A3R2, A4R2 adopt it as wording: the coordinator never merges into `master`; a local merge into the release line is a separate class. | L3 | n/s ; n/s ; adopt (conc 11) ; claims | adopt 65 ; n/s ; adopt 65 ; adopt (as wording) 55 | Majority (3 of 4) |
| U-018 | Keep reduced (full local suite, PR CI and bots, owner; plus a green dispatch run per A4) | 58% | A1 and A4 agree on the reduced gate; GFxAI tiers and two approvers do not transfer (A4-C9). A2 and A3 state no position. | L2 | adopt ("worth importing") ; n/s ; n/s ; claims | V4 in part 50 ; n/s ; n/s ; V4 reduced 55 | No-contest |

## Convergence Assessment

- Points resolved: 51 of 58
- Alignment: 87.9%
- Threshold: 80%
- Status: CONVERGED (diff-point gate and taxonomy-coverage gate pass; the invariant-probe gate is run by another agent and is not evaluated in this file, so a HIGH-severity UNADDRESSED invariant there would change the status to BLOCKED_BY_INVARIANTS)
- Unresolved points: C-005, C-017, X-004, A-008, A-011, A-013, A-015

### Counting rule
- Denominator (protocol formula `count(S) + count(C) + count(X) + count(A)`): 6 + 25 + 10 + 17 = 58. All 17 assumptions are included because all four advocates answered all 17 in Round 1. The 18 U points are scored above as keep or drop and are outside the denominator.
- Agreement is computed on each advocate's latest stated position. Agreed = Unanimous 35 + Majority (at least 3 of 4) 6 + No-contest 10 = 51. Split = 7.
- No-contest means no latest position names a contested winner (at most two advocates name a winner and none dissents). These 10 points are S-001 to S-006, C-014, C-025, X-008, X-010. They are counted as agreed in the headline because nobody disagrees on them.
- Two alternative counts, for transparency:
  - Excluding the 10 no-contest points from both numerator and denominator: 41 of 48 = 85.4% (still above 80%).
  - Counting the 10 no-contest points as not agreed: 41 of 58 = 70.7% (below 80%). Not used: absence of a contest is not disagreement.
  - Including the 18 U points (all scored without a split) in both: 69 of 76 = 90.8%.
- Round 1 agreement was not scored separately. The Round 1 positions are in the matrix. The debate stopped because depth standard allows two rounds; Round 3 was not run.

### Coverage per category
| Category | Points | Agreed | Unanimous | Majority | No-contest | Split |
|----------|--------|--------|-----------|----------|------------|-------|
| S (structural) | 6 | 6 | 0 | 0 | 6 | 0 |
| C (content) | 25 | 23 | 17 | 4 | 2 | 2 |
| X (contradiction) | 10 | 9 | 7 | 0 | 2 | 1 |
| A (shared assumption) | 17 | 13 | 11 | 2 | 0 | 4 |
| Total | 58 | 51 | 35 | 6 | 10 | 7 |

### Taxonomy coverage gate (each level needs at least one point addressed)
| Level | Points in the denominator | Addressed (at least one stated position) | Agreed | Unresolved |
|-------|---------------------------|------------------------------------------|--------|------------|
| L1 surface | 4 (S-003, S-004, S-006, C-024) | 4 | 4 | 0 |
| L2 structural | 29 | 29 | 25 | 4 (C-017, A-008, A-011, A-013) |
| L3 state mechanics | 25 | 25 | 22 | 3 (C-005, X-004, A-015) |
| Total | 58 | 58 | 51 | 7 |

All three levels are covered, so the gate passes. Note on L1: the four L1 points are three formatting points that nobody contested (S-003 has a concession by A4) and the tag-name point C-024 (3 of 4 name V4's `dash-1.3`). U-004 and U-016 are the other two L1 tags and are scored outside the denominator.

### Unresolved points
| Point | Level | What separates the advocates (latest positions) |
|-------|-------|-------------------------------------------------|
| C-005 | L3 | Story merge method: A1 narrowly V1 `--no-ff` (55); A2 and A3 no winner (50); A4 no winner, leans `--no-ff` (55). Owner's call (A4 decision 5). |
| X-004 | L3 | Same contradiction as C-005 (merge method into the batch line). |
| C-017 | L2 | Special releases: A1 and A4 keep 1.1 and 1.105 as ordinary release lines with a one-story skip (A4 asks the owner about test-only); A2 and A3 propose no line for bug-fix and test-only releases. |
| A-008 | L2 | Whether the CI-trigger edit reaches the workflow file GitHub reads in time: A1 and A2 ACCEPT (V3 and V4 only); A3 and A4 QUALIFY (the dispatch default avoids it; the file version GitHub reads is UNVERIFIED). |
| A-011 | L2 | Orca `--branch` name behaviour: A1 and A2 ACCEPT; A3 and A4 QUALIFY. All four plan the same throwaway check. |
| A-013 | L2 | Owner accepts editing the `test.yml` triggers: A1 and A2 ACCEPT; A3 and A4 QUALIFY (only needed if CI on story PRs is wanted). |
| A-015 | L3 | Someone runs the `master` into `integration` sync: A1 and A2 QUALIFY; A3 and A4 ACCEPT. All four say to assign it explicitly; who does it today is UNVERIFIED. |

### Oscillation notes
- No point flipped back and forth across the two rounds.
- Two points moved from a Round 1 majority to a Round 2 split because one advocate changed its verdict:
  - A-008: Round 1 ACCEPT ; QUALIFY ; QUALIFY ; QUALIFY (majority QUALIFY). In Round 2 A2 changed QUALIFY to ACCEPT ("V3 and V4 only"), giving 2 to 2.
  - A-015: Round 1 QUALIFY ; ACCEPT ; ACCEPT ; ACCEPT (majority ACCEPT). In Round 2 A2 changed ACCEPT to QUALIFY (60), giving 2 to 2.
- One point opened a contest in Round 2: C-017 had no claimed winner in Round 1 (all tie or no stated position); in Round 2 the combined designs of A2 and A3 (two lanes) differ from those of A1 and A4 (ordinary lines), although A1, A2 and A3 each list the point as not contested.
- Winner flips that resolved toward agreement (not oscillation under the protocol):
  - A2 and A3 moved to V1 on C-002, X-001, C-003, X-002 and C-008; A3 moved from V3 to V1 on C-004, C-010, C-019 and C-012 (V1 with V3's time box); A2 moved from V2 to V1 on C-010.
  - A2, A3 and A4 moved to a combined answer on C-001 (A2 from V2, A3 from tie with V2, A4 from partial) and on C-013 and X-006 (A2 from V2, A3 from V3, A4 from lose as written).
  - A4 moved from V4 to V1 on C-022 and from V4 to no winner on C-005 and X-004; A2 moved from a V2 granularity claim to no winner on C-005 (on X-004 A2 claimed nothing in Round 1).
  - C-016 moved from ties (A1, A2, A3) and a V4 claim (A4) in Round 1 to V4 in all four Round 2 positions.
  - Verdict changes on assumptions: A-006 QUALIFY to ACCEPT for A1, A2, A3 (A4 already ACCEPT); A-012 QUALIFY to ACCEPT for A3 and A4.
  - Round 1 claims withdrawn without a replacement winner: S-001 and S-005 (A3), X-010 and C-025 (A2, A3).

### Open design questions inside points counted as agreed (not counted as unresolved)
These are the sub-questions the advocates themselves list as still open (A4R2 section 7) while agreeing on the winner of the diff point above them: how much outside gate a story gets (C-004, C-007, C-011, C-021: dispatch only, plus an optional review-only story PR, or a hand-opened draft PR, which A4 rejects); the numeric story cap and time box (estimates only); the release-PR acceptance gate content (U-018); who runs the `master` into `integration` sync and whether `integration` is still in use (C-019, A-015); who may merge a review-only story PR (A-014); and the owner's confirmation in chat of local coordinator merges into the release line (CONTEXT line 11 "to be confirmed").
