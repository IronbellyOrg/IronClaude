# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5 invariant probe; no Round 3)
- Rounds completed: 2 plus the invariant probe (Round 2.5)
- Convergence achieved: 100 percent of 30 diff points reached an agreed position (28 unanimous, 2 by majority; see the assessment). The invariant gate BLOCKS declaring convergence (one HIGH UNADDRESSED finding, INV-025)
- Convergence threshold: 75 percent (`--convergence 0.75`)
- Focus areas: all
- Advocate count: 3 (opus:architect for V1, sonnet:analyzer for V2, haiku:backend for V3), each an agent that also generated its variant
- Full statements (each advocate file is the complete record; this file is the assembly and the scoring matrix):
  - Round 1: `rounds/round1-advocate-1-opus-architect.md`, `rounds/round1-advocate-2-sonnet-analyzer.md`, `rounds/round1-advocate-3-haiku-backend.md`
  - Round 2 (sequential: V1, then V2, then V3): `rounds/round2-advocate-1-opus-architect.md`, `rounds/round2-advocate-2-sonnet-analyzer.md`, `rounds/round2-advocate-3-haiku-backend.md`
  - Round 2.5: `invariant-probe.md`
  - Qualitative scoring passes: `rounds/qual-pass-1-forward.md`, `rounds/qual-pass-2-reverse.md`

## Round 1: Advocate Statements (summary of each position)
- V1 advocate (architect). Claimed: machine state outside git; `start_mode` and `coordinator_autostart` as config keys; `waiting_reapproval` state; owner actions written with the effect of each answer. Conceded: the "unbound and flagged" rule breaks the owner's G2 sentence; crash and idempotency depth is thin (V3 wins); the single adapted PR 686 stage is too large; the sweep fields should ship early (V2); the observer should read `issue-watch status --json` directly. Evidence: master `cycle.py:187-192` keeps the state dir outside git, `cycle.py:1086` launches the claim into the configured worktree.
- V2 advocate (analyzer). Claimed: smallest diff on the claim path (poll claims as built, `cycle.py:1090-1112`); ten mechanical merge checks; the revert dry run; rollback warning that matches the loader (`cycle.py:216-226` rejects unknown keys and any schema version but 1); `wake_enabled`; lane 3 early; NG-2 nuance. Conceded: K14 against S15 (X-003); machine state in the worktree and a tracked go entry (C-002, X-005); thin crash design; 21 stages heavy; D16 over-reach; interface rows 4 and 22 missing.
- V3 advocate (backend). Claimed: separation of an uncertain launch from delivery; ack needs a matching saved state; reuse of the built atomic writer (`pr-a wake.py:269-299`); no real issue before binding is proved (owner's G2 sentence, `issue-pipeline-guard-g2.md:9`); a consumed go is never restored. Conceded: telegraphic prose; plan-check reversal; the read-only claim-session workaround is not isolation; machine state should leave the checkout; the outbox is a design requirement, not a complete transaction.
- Shared assumptions: all three QUALIFIED A-001 (kill-and-resume test needed), A-002 (record the worker worktree path), A-005 (only a person-opened ordinary session runs `/sc:pr-submit` until the depth-0 start is proved and WC:70 and WC:245 are approved); A-003: V1 and V3 QUALIFY, V2 REJECT, same remedy (an interim ledger); A-004: ACCEPT with the correction that several worktrees per repo are normal. No `[OMISSION]` flagged: every advocate answered A-001..A-005.

## Round 2: Rebuttals (new evidence, checked in code)
- V1 (first): planb and master loaders both reject unknown keys and any `schema_version` but 1 (planb `cycle.py:59-72, 223-233`); a version bump only changes the error text. The poll-launched claim runs in `<worktrees>/<repo>/Coordinator` (planb `generate.py:252`, `launch.py:136-157`, `cycle.py:1179`), the same worktree as the standing coordinator, and `_precheck` (`dispatch.py:269-304`) ignores extra files. `/sc:issue --claim` is idempotent for comments and assignment (`refs/claim.md:30, 43, 44, 88-93`) but a re-run repeats Wave 4. D15 line 219 says PR 686 is adapted in place and "not split"; line 220 puts skip reasons and the start-time re-check on planb. D15 puts the worker route at O5 and wake handling at O6. V1 dropped `start_mode` code from the first build and the sweep `watcher` block.
- V2 (second): conceded K14, the tracked go entry, the in-worktree state, the "start the coordinator after the claim" idea, the three watcher PRs, the skill-before-merge bridge; moved S11 content onto planb; confirmed the planb loader; showed built text `refs/claim.md:96` already describes the coordinator adopting a level-none claim; showed master `record.py:440-448, 628` has a 60-minute launched lease and a claimable set that already covers `unknown`.
- V3 (last): conceded the plan-check direction, host paths, state in the worktree; moved the F-bound worker route to O5; showed that the dispatch store has a strict typed schema (a delivery intent needs a store migration, `record.py:168-175, 213-278`), that the cycle holds the lock through its commit (`cycle.py:682-709`, so "release before delivery" needs an explicit post-commit phase), that replay must run even when the normal path skips a claimed entry (`cycle.py:920-921`), that `mark_claimed` accepts a manual claim with no prior entry (`record.py:660-665`), that nothing proves the claim terminal closes after Wave 6, and that D05's staging constant must REFUSE real issues, not flag them. Remaining difference: V3 holds that the planb and PR 686 keys must not all wait until O6 (D15 rows C3 versus C4).

## Round 2.5: Invariant Probe (Step AD-1)
27 findings, 7 ADDRESSED, 20 UNADDRESSED: HIGH 1 (INV-025), MEDIUM 15, LOW 4. Full table in `invariant-probe.md`. HIGH: binding at guard level F does not stop a worker pushing, commenting or merging, because the guard reads command text only (`launch-level-guard.sh:771-772`), the L2 hook refuses only `main` and `master`, `setsid` escapes the job identity check and `gh` writes have no second layer; so the consensus claim "F binding alone satisfies D06" is falsified until a server-side ruleset exists.

## Scoring Matrix

"Winner" is the approach the advocates finally agreed on (final Round 2 tables: V1, V2, V3 sole; HYBRID names the lead parts). Confidence is the mean of the three advocates' stated final confidences, rounded.

| Diff point | Level | Winner | Confidence | Evidence summary |
|---|---|---|---|---|
| S-001 stage granularity | L2 | HYBRID: one PR per stage in D15 order O0..O7; V2's revert dry run and early lane 3; PR 686 one adapted draft | 80% | D15 lines 219-220; V3 rows bundle PRs; 21 stages heavy |
| S-002 owner-action format | L1 | V1 | 90% | each answer with its effect; V3 fragments fail the plain-English rule |
| S-003 diagram | L1 | HYBRID: V1 diagram with V2 status tags and V3 at-least-once paragraph | 80% | tags separate built from proposed |
| S-004 interface table | L1 | HYBRID: V1 complete rows, V2 file:line, V3 validation rules, no host paths | 80% | V2 rows 4 and 22 missing; V3 hard-codes `/home/coder` |
| C-001 who claims | L3 | HYBRID: poll claims as built, coordinator adopts, V3 outbox replay after `claimed`; claim-by switch kept as named reversal | 83% | `cycle.py:1090-1112`, `refs/claim.md:96` |
| C-002 state location | L3 | V1 (machine state outside git; human records on `coordinators`) | 75% | `cycle.py:187-192`; all three accept after Round 2; D15 line 224 "git-ignored" wording noted |
| C-003 binding switch | L3 | V3 (False refuses real-issue workers) | 94% | G2 sentence `issue-pipeline-guard-g2.md:9`; D05 lines 47, 56 |
| C-004 plan-check direction | L2 | V1 and V2 (script is the reference, package copy, parity test) | 89% | D12, D15 R-2; `test_origin_parity.py` precedent |
| C-005 watcher feed | L2 | V2 (observer reads `issue-watch status --json`; sweep untouched) | 84% | `cli.py:165-182`; D11 fixed read list |
| C-006 sweep fields timing | L2 | V2 (early, lane 3) | 85% | D11 lines 18, 20; D14 lane 3 independent |
| C-007 PR 686 slicing | L2 | HYBRID (majority 2 of 3): one adapted PR 686 (D15 219), skip reasons and re-check on planb (D15 220), `owner/name` rekey at O6; V3 adds: each new key's loader support no later than its first reader | 78% | V3 dissent on key timing is a rule the merge adopts |
| C-008 verb-group slicing | L2 | V3 corrected: O4 substrate, O5 merge unit plus F-bound worker route, O6 the rest | 84% | D15 line 18, row D12 |
| C-009 go entry location | L3 | HYBRID: consumable go outside git, quoted words unchanging in `records/`, consumed never restored | 85% | one-shot mutable token must not live in git |
| C-010 crash and idempotency | L3 | V3 (with the built parts marked) | 88% | `record.py:440-448, 628`; new work is wake replay, ack-state match, restart budget |
| C-011 D16 inclusion | L2 | HYBRID: ruleset recommendation (D05, D14) in S0, D16 items as proposals | 76% | D16 VERDICT now exists; owner decides |
| C-012 unsourced numbers | L1 | HYBRID: labelled UNVERIFIED suggestions; built 60-minute lease kept; merge automation off until answered | 71% | `record.py:440-441` |
| C-013 label creation vs NG-2 | L2 | V2 | 82% | person-run init write on a chat go |
| C-014 per-repo keys | L2 | HYBRID: schema 1, widened key list, `coordinator_session`, `wake_enabled`, `coordinator_autostart`; claim-by key reserved; separate store migration | 79% | loaders reject unknown keys |
| C-015 rollback caution | L3 | V2 plus store backup (INV-004) | 90% | `cycle.py:216-226` |
| X-001 claim agent shares the worktree | L3 | HYBRID (majority 2 of 3 on the constraint; mechanism open): real rollout off until a live check; fix is a separate claim worktree or the coordinator claiming; owner picks | 80% | planb `generate.py:252`; claim terminal lifetime UNVERIFIED |
| X-002 unbound real issue | L3 | V3 | 95% | owner's G2 sentence |
| X-003 V2 K14 vs S15 | L3 | V3 wording | 93% | internal contradiction conceded |
| X-004 plan-check source of truth | L2 | V1 and V2 | 90% | D12, D15 R-2 |
| X-005 tracked go entries | L3 | HYBRID: never tracked | 85% | mutable token |
| X-006 sweep reads watcher | L2 | V2 and V3 (no) | 83% | D11 stateless sweep |
| A-001 coordinator survives exhaustion | L3 | QUALIFY: kill-after-`worker_done` resume test | 83% | contract rule S6 |
| A-002 worker has its own worktree | L2 | QUALIFY/REJECT, same remedy: probe records the worker worktree path | 86% | D05: never observed |
| A-003 owner answers have a home | L2 | QUALIFY/REJECT, same remedy: interim ledger, imported later | 78% | no variant named one |
| A-004 one repo, one host | L2 | ACCEPT with correction (several worktrees per repo) | 86% | per-user state, host-local locks |
| A-005 depth-0 coordinator may run `/sc:pr-submit` | L3 | QUALIFY: only person-opened until U3 and WC:70, WC:245 | 89% | D06 line 88 |

Wins used by the tiebreaker (sole or shared): V1 4 (S-002, C-002, C-004, X-004), V2 7 (C-004, C-005, C-006, C-013, C-015, X-004, X-006), V3 5 (C-003, C-008, C-010, X-002, X-003). V2's wins do not enter the tiebreaker because V2 is not in the top two.

## Convergence Assessment
- Points resolved: 30 of 30 (28 unanimous after Round 2, 2 by majority: C-007 and X-001).
- Alignment: 100 percent. Threshold: 75 percent.
- Taxonomy coverage: L1 4 points, L2 14, L3 12, all addressed in both rounds. Gate satisfied (no forced round).
- Invariant gate: 1 HIGH UNADDRESSED (INV-025). Per the gate rule convergence is BLOCKED.
- Status: BLOCKED_BY_INVARIANTS (agreement 100 percent, taxonomy covered, invariant gate not passed). Depth standard has no Round 3, so INV-025 and the 15 MEDIUM findings are carried as binding spec conditions in the refactor plan and the return contract (`unaddressed_invariants`).
- Unresolved points: X-001 (the mechanism that removes the two-agents-one-worktree overlap: separate claim worktree or the coordinator claiming; needs a live probe and an owner choice), C-007 (resolved by the merge rule "loader support no later than the first reader"), INV-025.
