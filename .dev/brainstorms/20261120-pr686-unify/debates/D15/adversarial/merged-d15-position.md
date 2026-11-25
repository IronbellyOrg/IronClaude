<!-- Provenance: merged-d15-position.md, produced 2026-11-20 by merge-executor for debate D15. Base: Variant 1 (OURS position paper, variant-1-original.md). Merged in: Variant 2 (CLAY) elements per refactor-plan.md Changes #1 to #5; gap decisions G-1 to G-9 from rounds/round2-rebuttal-1-ours.md and rounds/round2-rebuttal-2-clay.md; fault-finder conditions from invariant-probe.md. Source folder: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/adversarial/ . The per-element Clay table is NOT in this file: it is authored once in VERDICT.md. -->

# D15 merged position: Clay strengths bundle, what to adopt and how

Debate status (from debate-transcript.md): convergence 89.3 percent (25 of 28 points), threshold 80 percent, status BLOCKED_BY_INVARIANTS. Standard depth has no Round 3, so the four HIGH invariants become mandatory conditions of this document (section (f)). Base selected: Variant 1 (OURS), combined score 0.829 against 0.760 for Variant 2; these are single-evaluator estimates (base-selection.md).

The element-by-element table (every Clay element, its outcome, its change, its carrier) is authored once in the D15 VERDICT.md and is not repeated here. This file holds the principles, build order, test plan, gap decisions, invariant conditions and open owner questions that the table rests on.

Notation. "Dnn" is the verdict `debates/Dnn/VERDICT.md` under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. "D:nnn" is a line of `docs/designs/orchestrator.md` in the snapshot `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same snapshot. "pr-a" is the export of PR 686 (Clay's branch that carries the issue-watch coordinator code) and "pr-p" is the export of PR 690 (adds `--plan` and `--remaining` to `/sc:issue`), both under `/home/coder/.cache/ic-snap-20261120/`. "INV-nnn" is a finding of invariant-probe.md. "Clay" is the account `clayphi`; the repository owner is `ironbelly`. Weighting rule: OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS; a clear separable CLAY benefit is a HYBRID. Anything not read by the writers of the source files is marked UNVERIFIED.

## (a) Merged position in 8 lines

<!-- Source: Base (original) claim and mechanism, with Variant 2 elements merged per Changes #1 to #5 (summary section; every line is carried from sections (b) to (i)) -->

1. Unit of adoption: every rule row is decided per element and OURS decides it under the weighting rule; the element table with carrier PRs is authored once in the D15 VERDICT.md (C-001 HYBRID, C-006 OURS).
2. Build home: Clay's control verbs are built once as one group against one JSON contract (D:140), in this order: substrate, then the merge path as one tested unit, then the other verbs in any order (C-001 and C-002 HYBRID).
3. What stays OURS: approval as the start gate, no assignment-only trigger, no standing `pr.merge` or `issue.close` grant, launch guard required, poll writes no labels, no registry repo or `repos.yaml`, a person's typed go for every merge; per-repo settings live in `~/.config/superclaude/issue-watch.d/<repo>.json` with Clay's key names (C-006, C-009).
4. Taken from Clay with a change: the closed pinned reasons table (14 approval reasons back, pin rewritten), the wake file plus acknowledgment with defects M1 and M2 fixed, in-flight cap and guarded restart, hand-back with the start gate run again at round 2, tier keys as requests only (C-003, C-004, C-005).
5. Test plan: T1 to T13 plus the U and K registers are the skeleton of one live-test plan (13 T, 60 U and 28 K rows, 101 in all, per INV-009); six rows get a logic rewrite (T1, T3, T4, T8, T10, T11), T12 is rewritten for hand-back, and rows that start a worker get a setup step that approves the throwaway issue.
6. Nine gaps no verdict decided: lease comment deferred, approving permission prompts rejected, `escalate --interrupt` rejected, `setup-clone` rejected, info streams off by default, N6 an unconditional refusal, AU5 narrowed, tiers and hand-back adopted with change, naming rule scope left to the owner (G-1 to G-9).
7. Wording: every control "narrows" and never "closes"; each control is written with its falsifiers (INV-015, INV-016, INV-018, INV-019).
8. Status: BLOCKED_BY_INVARIANTS until the four HIGH conditions C-INV-1 to C-INV-4 are accepted as conditions of the build (they are new requirements with no Clay or owner source); 13 owner questions are open in section (h), each with a default only where a source gives one.

## (b) Rules that stay OURS

<!-- Source: Base (original), variant-1-original.md Claim, "What it gets right" and per-element outcomes; confirmed by both Round 2 files (C-006 OURS, C-007 and X-002 tie to OURS, C-009 OURS on the home); Variant 2 contributed only the agreement (it withdrew "as built" and conceded C-006, C-009, X-002) -->

Both sides agree on this list (C-006, C-009). A row the owner has not ruled on defaults to OURS under the weighting rule.

| # | Rule that stays | Source | Limit or note |
|---|---|---|---|
| 1 | Approval is the gate that starts work. An assignment alone never starts work. A hand-back round 2 or later passes the same gate again. | D01; G-3 | Mechanism for round 2 is open, see (e) G-3 and (f) C-INV-1, C-INV-2. |
| 2 | Level none, and the launch guard is required and staged for the workers the coordinator starts. | D05 item 1 | The guard narrows honest drift only; falsifiers in (g). |
| 3 | A merge needs a person's typed go, bound to the head and the question key. The merge gate runs twice, a new gate reason "no recorded merge go" is added, the merge is pinned to the head. Nothing merges alone. | D06 items 1 to 3, D04 item 6 | The go check cannot tell a person from a script (INV-015, see (g)). |
| 4 | No standing `pr.merge` grant and no standing `issue.close` grant. The only standing grants are `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` and `issue.hold`. | D04 item 5, D06 item 8 | The default of a fresh install is not settled (INV-012, OD-11). Post-merge close authority is open (C-INV-4, OD-10). |
| 5 | The poll writes no labels. The NG-2 rule stays. `hold:backlog` is set by a person and the poll only reads it. | D09 item 3, D01 | Poll label writing is deferred; it changes only if the owner enables it. |
| 6 | No registry repo, no `orchestrators.json`, no `repos.yaml`. Per-repo settings live in `~/.config/superclaude/issue-watch.d/<repo>.json` with a `merge` block holding Clay's key names: `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`. The role is read live at merge time. | D07 items 2 and 5 | The config directory is not tamper-protected (C-INV-3, OD-12). |
| 7 | Workers do not run `/sc:pr-submit`. The route called ADD1 in the design is not adopted. | D06 item 5 | none |
| 8 | Names change from `orchestrator` to `coordinator` before PR 686 merges: wire strings, mailbox kind, `orchestrator_tier`, `.orchestrator/`, golden fixture, typed line, verb group. | D08 action 8 | The cost is the same for both lines (X-002), and grows after the merge. |
| 9 | The coordinator may type nudges into worker terminals under the extra safety conditions (prompt on the current screen, 60 seconds quiet with an empty draft, screen re-read before sending, exact key logged). It never answers a permission prompt. | G-5; WC:122, WC:137 | A closed list of approvable prompt classes is a possible later owner decision, not open now. |
| 10 | The coordinator never tags or publishes a release (N6 is an unconditional refusal). | G-9 part 2 | Owner confirmation is asked in OD-6. |
| 11 | The cap of 5 notices stays a proposal with its key at the default 0 until the owner rules. The nine-row reasons list is an inventory, not a rule. | D11, D06 item 11 | The design contradicts itself on whether ruling 39 is settled (D:1177 against D:686 and D:877); either way it is Clay's ruling, not the owner's. |
| 12 | The verdicts D01 to D13 are recommendations, not owner rulings. Each row that a verdict marks "depends on owner decision" carries that line. | A-001 QUALIFY | D01 R19, D04 R9 and R10 and the D06 amendments wait for the owner's word in chat. |
| 13 | Not built: the lease comment, `orca project setup-clone`, `escalate --interrupt`. | G-1, G-8, G-6 | Decisions in (e). |

## (c) Build order

<!-- Source: Variant 2, round2-rebuttal-2-clay.md A3.1 (substrate first, merge path one tested unit, other verbs separable), merged per Change #1; chain of work (rules and docs first, then built code, then unbuilt verbs, then live tests) from Base (original) Mechanism; merge-path members from round2-rebuttal-1-ours.md A1 W1; INV-006 and INV-010 added from invariant-probe.md -->

Both final positions agree on this shape: substrate first, then the merge path as one tested unit, then the other verbs in any order (C-001 HYBRID). The verbs share one group and one JSON contract (D:140), so they are written once. Nine of the twelve verbs listed at D:510 already have a verdict that adopts them in changed form: `wake-check`, `wake-ack` (D10 items 1 to 3), `state` (D07 item 7), `merge-gate` (D06 item 2), `plan-check` (D01 item 2), `repos` (D07 item 5, D04 item 7), `answer-check` (D04, D06 item 9), `audit` (D05), `report-entry` (D11). The other three (`lease`, `escalate`, `handback`) are decided in section (e): `lease` deferred (G-1), `escalate` without `--interrupt` (G-6, G-9), `handback` adopted with change (G-3). These verbs are design text: `escalate`, `merge-gate`, `answer-check` and `asks.json` exist in none of master, pr-a or pr-p (D11, D06 Unverified). Adoption therefore means writing them.

**Stage 0. Rules and doc fixes first.** The names change (D08 action 8), the settings home is fixed (D07), the grants and refusal text are amended, and the wording rule of section (g) is applied. The rename must land before PR 686 merges (D08 action 8); the other doc fixes come first because the owner's chain puts rules and doc fixes before code. The work is keyed to files and rows, not to a carrier PR, because the verb group has no carrier PR yet (A-003), D14 has not decided PR 686's fate, and D03 item 3 says that reverting PR 682 (Clay's merged deletion of the owner's issue pipeline) together with merging PR 686 gives a broken tree (`superclaude --help` crashes, 29 test modules fail at collection).

**Stage 1. Substrate (built once, early).** Every verb needs all five parts.

| Part | What it is | Source |
|---|---|---|
| Runner | The runner every verb uses; it refuses a listed argv, exits 2 and logs the reason. | D:1117 |
| `refuse(argv)` | One function through which every `gh`, `git` and `orca` call of a verb passes. Two of its edges are removed by decisions in (e): the N6 `answer_ref` pass path (G-9 part 2) and the N7 `caller` branch (G-6). | D:767 |
| JSON contract | Every verb prints one JSON contract. | D:140 |
| State lock | One lock used by `escalate` (the `asks.json` file), `handback` ("under the state lock", D:613), routing (D:318) and `state`. | round2-rebuttal-2-clay.md A3.1 |
| State-folder path map | One agreed home for the state file, wake store, acknowledgment, audit log, handback files, `asks.json` and the state lock, after the registry repo goes. | INV-006 |

The path map is a mandatory part of this stage because every one of those files is anchored on `<orchestrator-repo>/.orchestrator/` in the design, a folder D07 item 2 deletes and D08 item 8 renames (INV-006, see the spec line in (f)).

**Stage 2. Merge path as one tested unit.** These parts lean on each other and are built and tested together (D06 item 8, D04 item 6; both sides agree). The interlock closure is exactly this set, not all twelve verbs.

- The merge verb that demands the go entry. `E-NO-GRANT` does not see a raw `gh pr merge`, so the merge must go through one verb. The 12-verb list at D:510 has no merge verb, so the verb is named here and counted in the verb total (INV-010).
- The go entry and `answer-check` with the owner identity as a parameter.
- `merge-gate` with its 13 reasons plus "no recorded merge go", run twice, with the head-pinned merge.
- The merge-time reviewer hold: owner-set `reviewers` list, re-trigger on the final head, 60 minutes (UNVERIFIED).
- `E-NO-GRANT` without `pr.merge` and `issue.close` in the grants.
- The `repos` guard: grants, `reach_daily_max` and `merge_safety_files` change only with an accepted `--answer-ref`.
- T13, which pins the merge-gate reasons and the `answer-check` question key together (D:1141).
- The post-merge close authority (C-INV-4) is decided with this unit, because the go entry is defined today only for merges.

**Stage 3. Other verbs, separable, any order after Stage 1.** `wake-check` and `wake-ack` with M1 and M2 fixed (the acknowledgment only after the state file exists; an abandoned wake recoverable, see INV-011), `state`, `plan-check` (placeholder rule, runs before approval, one definition in `plan_body.py check`), `report-entry`, `audit` AU1 to AU8 with AU5 narrowed, `handback` (with C-INV-1 and C-INV-2), `escalate` (notice step as D11 adopts it, no interrupt), the in-flight cap and guarded restart (D07 items 3 and 4; limits table INV-008). PR 690 (`--plan`, `--remaining`) is kept with four changes: a fence-aware heading count, one definition of "passes", the caller named, the live head confirmed (D12 item 2). The lease verb is not built.

**Stage 4. Live tests last.** The plan is in section (d). A guard against accidental landing of a contested rule, accepted by both sides: no row lands without its named amendment and a failing-then-passing test. Example: the NG-2 test in `pr-a/tests/issue_watch/test_security_invariants.py:12` pins three label calls, and D09 changes it from three calls to two.

## (d) Test plan

<!-- Source: Variant 2 (CLAY) T1 to T13 plus U and K registers as skeleton, merged per Change #2; six logic rewrites and the T12 and T13 additions from Base (original) round2-rebuttal-1-ours.md A1 W3 and G-3, G-9, with the setup-step edit from round2-rebuttal-2-clay.md A3.2; counts from invariant-probe.md INV-009 -->

**Base.** One live-test plan: tests T1 to T13 (D:1123 to D:1141), the U register of what is unproven and the K register of risks, kept whole. Both sides agree it is a skeleton and not "as built". OURS had no coordinator-layer plan of its own that CLAY could find (UNVERIFIED that the owner has none outside the verdicts).

**Counts, as in INV-009.** 13 T rows, 60 U rows, 28 K rows, 101 in all, from a grep of `^\| T`, `^\| U` and `^\| K` in `orchestrator.md` (that grep is the probe's, not re-run here). The earlier figures are wrong: Round 1 OURS said 80 (a grep that misses T10 to T13 and K12 onward) and Round 1 CLAY said 60 U and 11 K.

**Row by row.**

| Row | Change | Reason |
|---|---|---|
| T1 | Logic rewrite, plus setup step | Uses two orgs and a listed repo with `repos.yaml`, which D07 removes. |
| T2 | Rename (D08), plus setup step | Starts a worker. What T2 tests is not restated in the round files. |
| T3 | Logic rewrite | Expects `repo_not_listed` and a repo with `clone_parent`; D07 removes them and G-8 rejects `setup-clone`. First case dropped; the skip reason becomes `no_checkout`. |
| T4 | Logic rewrite | Tests two orchestrators and the lease; D07 gives one coordinator and G-1 defers the lease. |
| T5, T6, T7, T9 | Rename (D08), plus setup step | Start a worker. What each tests is not restated in the round files. |
| T8 | Logic rewrite | Expects an autonomous merge of a clean PR; D06 item 1 needs a person's go. |
| T10 | Logic rewrite, plus setup step | The poll starts coordinator 2; D07 has one coordinator. |
| T11 | Logic rewrite, plus setup step | The poll writes `hold:plan` labels; D09 and the NG-2 rule forbid it. |
| T12 | Rewrite for hand-back, plus setup step | Sub-cases (e), (h), (i), (j), (k) and (l) start a round with no person step (D:1140); G-3 adds the re-approval step. Case (m) is the `Fixes` line that makes GitHub close the issue at the merge (see C-INV-4 and INV-017). |
| T13 | Rename (D08), plus new cases | Add the conflict-marker banner case beside case (e) (G-9); the new gate reason "no recorded merge go" (D04 item 6) must also appear in its pin of the gate reasons (this follows from the new reason; the round files do not state it); keep the pin of merge-gate reasons together with the `answer-check` question key. |

**Totals.** Six logic rewrites named by both sides (T1, T3, T4, T8, T10, T11); T12 is a seventh rewrite found by INV-009. Setup-step rows: T1, T2, T5, T6, T7, T9, T10, T11, T12, which is every row that starts a worker (round2-rebuttal-2-clay.md A3.2). The count of setup edits is not exact (UNVERIFIED, CLAY says so itself).

**The setup step.** After the throwaway issue has its plan, the test approves it (D01 item 5 ordering: plan first, approval after). D01 puts the approval gate back, so "assigned to the user" no longer starts work. Two further changes touch how a worker is started and are setup edits, not logic rewrites: the launch-guard marker and preflight (D05) and the Full Submit route for the pull request (D06 item 5).

**Registers.** The U register is adopted whole as the list of what is unproven. Entries that the sources tie to a live check:

- U5, the mailbox send from outside a Run (D10 item 13).
- U25, session detection and the `orca agent launch` tag (D10 item 13, D07 item 4).
- U3, the terminal plus `ccsession` start at depth 0 (D06).
- U28, the worker tier path `worker-start --model <picker id>` (D:726).
- U30, which effort levels `worker-start` accepts (D:1288).
- U40, the missing receipt that tells "steered" from "queued".
- U42, the open hook for commands outside the verbs.
- U8, the replies of the three info search streams.
- U54, the measurement of the last 50 issue titles against the naming deny list.
- U2 with K17, closeout callable from inside a wave.

The K register carries K11, K12, K14 and K16, which CLAY names as the risk entries a live test plans against (their text is not restated in the round files, UNVERIFIED here), K22 (`refuse` sees only commands the verbs run) and K23 (the plan check proves presence only).

**The reasons table pin.** The closed, pinned reasons table is adopted in form (a kind and an exit code per reason; `ack_not_observed` and `attempts_exhausted` exit 7). The pin at `pr-a/tests/issue_watch/test_audit.py:86-98` is rewritten: the 14 approval reasons D01 needs come back (`not_approved`, `approval_before_trigger`, `edited_after_approval`, `project_mismatch`, `edits_unreadable`, `marker_unreadable` and others), `plan_incomplete` and `held_backlog` are added (D01), and `coordinator_full` and `name_collision` are added (D07). The current pin is `59 - 14 - 5 + 5 + 17 == 62`. The new total is not stated by any source and must be recomputed from the final set (INV-007); the spec line is in (f).

## (e) Decisions on gaps G-1 to G-9

<!-- Source: Variant 1 (round2-rebuttal-1-ours.md Task B) and Variant 2 (round2-rebuttal-2-clay.md Task B), merged per Change #3; where the two disagree both positions are stated with the recommended default; recommended defaults follow refactor-plan.md "Changes NOT Being Made" -->

These nine design rows had no verdict. Both Round 2 files decided them. Agreed outcomes need only a note; the disputes are G-2 (the plan key), G-3 (the mechanism) and G-9 part 1 (the channel).

**G-1. Lease comment (DQ3 layer 4, D:113, D:543 to D:547).** Outcome: defer; record it as "reserved design, not built" with the trigger "a second host or a second user runs a poll". Reason: the race is real, because master's claim lets the same login re-claim an issue (`refs/claim.md` Wave 2, known only as quoted in the design), but the design says the lease matters only for two hosts, two users, a hand-run `--take` or a restored store; D07 has one dispatcher on one host; no double claim is cited; the owner's line already has Q26 claim files and the claim-marker guard (MR-2). CLAY adds a defect: a lease whose owner crashed before editing it to `released` keeps the lowest comment id and would wedge the issue, and no stale-lease rule was found (UNVERIFIED that none exists elsewhere). Change: move the layer to a "reserved, not built" list, rename the marker to `sc:coordinator:lease` (D08), rewrite T4; if ever built, add a stale-lease rule. The start re-check already runs before the lease in the design (D:543, D:547); the D01 amendment widens it to approval, `unchanged_since` and Status (MR-1). Owner decision: OD-8, default no. Both sides agree.

**G-2. Tier settings (5.8, D:720 to D:734).** Outcome: adopt with change. Keep `coordinator_tier` (renamed from `orchestrator_tier`; the `--tier` option exists in master at `ccsession:1001-1010` and master `launch.py` has no tier text) and `worker_tier` as requests, not facts, until U28 passes and the effective tier is recorded. The effort keys wait for U30. Disagreement: OURS drops `plan_tier` because `/sc:issue` already routes work by complexity (`refs/tiers.md`). CLAY shows this holds for claim and create but not for `--plan`: `--plan` takes `--depth quick|standard|deep` with default `quick`, the depth picks the worker (quick `issue-worker-t3`, standard `issue-worker-t2`, deep `issue-worker-t1`, pr-p `refs/plan.md:56-60`), and nothing picks the depth from complexity, so without a key the plan call falls to the cheapest worker, against goal G6 (D:60). OURS is right that `plan_tier` as designed would need a tier-to-depth table that does not exist. Merged outcome (per the plan): replace `plan_tier` with one plain key, `plan_depth`, passed straight to `--depth`; no tier-name table. Recommended default value: unset, which behaves as `quick`, the `--plan` default and the same as OURS' no-key outcome; the weighting rule gives a tie to OURS. This recommendation is the merge's, not a source's. The cost of it is stated: `quick` runs the cheapest planner, which is the opposite of G6; Clay's own default tier implies `deep`. Change: rename the key and field, move the format from `repos.yaml` to the per-repo JSON, keep the `TIER_ORDER` fallback and `parse_tiers`, remove the effort keys from the parser. Owner decision: OD-1 (default of `plan_depth`).

**G-3. Hand-back loop (wave 8, D:603 to D:620, `HANDBACK_MAX`).** Outcome: adopt with change. The producer is on master (closeout prints `issue.handback: remaining`, `sc-closeout-protocol/refs/result.md:40-47`); the consumer is the `handback` verb, unbuilt, and PR 690's `--remaining` has no first caller yet. `HANDBACK_MAX` = 3 (four rounds) is labelled "this design's value, not measured" (D:612). The old worker must be final before a new round (D:614, consistent with WC:157). Both sides agree round 2 must pass the D01 start gate again, because the re-plan edits the body, which voids the approval (`predicates.py:249-259`, D01 item 5), and the design re-enters at wave 2 and says wave 1 "is not run again" (D:615). Disagreement on mechanism: OURS wanted a recorded go in chat per later round, bound to issue, round and a hash of the remaining file, checked by `answer-check`, with a new waiting step `handback_awaiting_go`. CLAY objected that this is a second mechanism with no source, that D01's gate is the approval label set by an allowed approver, and that `answer-check` cannot tell a person from a script. The plan rejects the chat go: the start gate decides. Two options remain for the owner. (a) Re-plan the body and the person re-applies the approval before round 2 (default; OURS and CLAY both call it the safe default). (b) Leave the body alone: the remaining list travels in the handoff round block (D:619) and in a comment, since `unchanged_since` ignores comments by the watcher's own login; cost: the body does not show "Done so far / Remaining" and `--remaining` still has no caller; UNVERIFIED whether round-2 closeout done-checks behave when the body keeps the original criteria. Either way the invariant conditions C-INV-1 and C-INV-2 apply: the waiting issue must not hold a place in flight forever, and something must wake the coordinator after re-approval. Change: new `handback` verb with stop reasons `cap`, `no_progress`, `no_remaining`; rewrite D:610 to D:620 so a round after the first waits for the start gate; rewrite T12. Owner decision: OD-2.

**G-4. Naming rule (5.12, D:830 to D:847).** Outcome: adopt with change; the owner sets the scope. The rule forbids model ids, agent product names and "generated with" lines in anything the coordinator or a worker writes where a person reads it; the commit trailer stays (ruling 39). It collides with practice: 25 of the last 30 merged PR bodies in `IronbellyOrg/IronClaude` contain "Generated with" (both sides re-ran the count) while a grep of `src/superclaude` and `docs` finds the phrase only in the design file (OURS), so the lines come from the sessions' tools and not from owner files. The design calls this "owner ruling 15" but defines the owner as Clay (D:3, D:11). The enforcement is already scope B: `names_check` runs in the writer verbs `report-entry` and `escalate` and in tests, and a worker's PR body "cannot be scanned before it is written" (D:847). Options: (A) as written; (B) scan only the coordinator's own writers and leave workers' PR-body practice alone; (C) no naming rule (CLAY's addition). Recommended default: B, which matches what the design can enforce, with U54 (the 50-title measurement) run before the scan is enabled. A measurement from OURS: of the last 50 issue titles one holds "IronClaude" and six hold "Jev"; whether a deny list would trip on them is unknown because the deny-list data is not written. Open risk found later: scope B puts the scan on the two writers that carry safety escalations (INV-013). Owner decision: OD-3, and OD-4 for the refused-escalation case.

**G-5. DQ9, typing into worker terminals and approving prompts (D:119, D:573, D:752).** Outcome: adopt the typing with its safety rules, reject approving permission prompts. Both sides agree. Reason: WC:122 (state S4, "never answer the prompt") and WC:137 ("never type into a busy, S11 or S4 session; never answer a person prompt") forbid it. CLAY corrects one reading: WC:188 is the "Never on silence" list and forbids acting on silence, so the load-bearing lines are WC:122 and WC:137. No coordinator-only exception exists in the text: ADD1 (D:135) is not adopted (D06 item 5), and D06 item 7 puts a script-started coordinator under the same section. No measured count of prompts exists; ccsession sessions run with the permission bypass unless `CCSESSION_PERMISSIONS=default` is set, and whether Orca `--agent claude` workers do is UNVERIFIED. Change: keep FR-24 rules 1, 2, 3 and 5 as conditions on typed nudges; remove the approval rules 4 to 7 (the S4 line may name which escalation row the prompt's action falls under, with no key sent); drop approval cases from the typing tests. Owner decision: none now; a closed list of approvable prompt classes is a possible later one.

**G-6. N7 `escalate --interrupt` (D:749, D:764, D:767).** Outcome: reject for the first build; closed unless the owner asks. Both sides agree on the outcome and differ on one reason. OURS said N7 reverses a contract rule ("never interrupt", WC:137). CLAY shows that line governs the typed acknowledgment copy and that the S6 row already interrupts under the WC-14 exception (WC:63, WC:124), so N7 adds a second interrupt case with no contract text behind it. Reasons both accept: no incident is cited; Orca gives no receipt that separates "steered" from "queued" (U40); ruling 25 is Clay's. CLAY adds one that OURS missed: after an interrupt the next sweep sees an idle worker and the L2 nudge text (WC:164) tells it to continue, which undoes the interrupt, and no suppression rule was found (UNVERIFIED outside the lines read). Kept: the rule that `escalate` writes the escalation first and sends nothing if it is refused. Change: delete the "Interrupt a worker, in one case" row (D:749), remove the exception from N7 (D:764), remove `--interrupt` from the verb list (D:140, D:510), do not apply C25 to C29. If ever asked for: a contract exception written like S6's, a rule suppressing the L2 nudge, and the U40 check. Owner decision: OD-7, default no.

**G-7. DQ13 information entries and ADD3 info streams (D:123, D:137, D:184, D:254).** Outcome: adopt with change, off by default. Both sides agree. `mention` and `affects` are subsets of what the report's collector already gathers (`collect.py:199-218`, one `gh search issues --owner <org> --involves <person>` per pass); only `could_assign` is new. The code is written in pr-a (`github.py:165-176`), so it stays behind one switch that is off and fails open, the same switch as D07 item 6. The replies of the three streams are UNVERIFIED (U8) and CLAY notes the fixtures are of assumed shape, so off is also the evidence-based default. `mention` and `affects` are not written as entries. Enable only after the U8 live capture. Owner decision: OD-9, default no.

**G-8. DQ4 `orca project setup-clone` (D:114, D:544, D:762).** Outcome: reject; keep the origin check (`check_origin`). Both sides agree. It rests on `repos.yaml` and `clone_parent`, which D07 removes, and on "since approvals are broad" from the coordinator spec (FR-8, Q12; UNVERIFIED, not read), which does not carry over because D01 approvals are per issue. D:762 puts `setup-clone` in the N5 class (machine or VM lifecycle). pr-a has `clone_parent` (`repos.py:79`, `:350`) and the `missing` state (`cycle.py:1226`) but no `setup-clone` call. Change: remove `clone_parent`, make `cycle.py:1226` give `no_checkout` as a visible skip reason, drop T3's first case, replace DQ4 with "a repo with no checkout is skipped with a visible reason; a person adds the project to Orca", strike the exception from N5. Owner decision: none now; if the repo count grows, a recorded authorization per repo before any clone.

**G-9. Audit escalation rows (AU4a, AU4c, AU5; D:825) and N6 (D:763).** Outcome: adopt with change. AU4a (merged over a change request) and AU4c (merged with an unresolved thread) fire only for a merge made outside the gate, because the gate refuses `changes_requested` and `threads_open` (D06 item 3); the audit is the only detector for that case. AU5 is narrowed: a line starting `<<<<<<< ` or `>>>>>>> ` always counts; a bare `=======` counts only when an opener or closer is among the added lines of the same file, because the only seven-equals line found in master is `src/superclaude/cli/swarm/tmux.py:9` (OURS calls it a banner, CLAY a reStructuredText underline) and no `<<<<<<< ` line was found in the markdown of `src` and `docs` (OURS) or at line start in `src`, `tests` and `docs` (CLAY). T13 case (e) gets a banner case. Part 1 disagreement, the channel: OURS said the escalation goes only into the report entry until the owner rules on the nine-row list and the notice cap; CLAY said that is stricter than the verdicts, because D11 adopts the nine-row table in the notice step with the cap key at default 0, the notice channel already exists in the report skill, and a line in a living report waits until someone opens it. Merged outcome (per the plan): the entry lines (D:825 item 2) plus the notice step as D11 adopts it, cap key at its default 0, no gate, warnings never reach a person, no new channel built. Cost found later: default 0 means no cap (INV-014). Part 2, N6: both agree it becomes an unconditional refusal with no `answer_ref` pass path in `limits.py`, because the pass path would route the most irreversible action through a check that cannot tell a person from a script (D06 item 9). A test scans the coordinator skill and refs for `git tag`, `git push origin <tag>`, `gh release create` and package uploads outside "Will Not Do" and the denylist file (D:769's own remedy). Merging a release PR stays an ordinary merge with a go. Change: delete the D:751 row, rewrite D:763, drop the N6 sentence from D:767. Owner decisions: OD-5 (channel) and OD-6 (never tags or publishes).

## (f) Mandatory conditions from the invariant probe

<!-- Source: invariant-probe.md (Round 2.5 fault-finder), merged per Change #4. These are new requirements: no Clay or owner source states them. They are recommendations of the fault-finder, carried as conditions because standard depth has no Round 3 and the status is BLOCKED_BY_INVARIANTS. -->

### HIGH conditions (UNADDRESSED in all four Round 1 and Round 2 texts)

Each condition has a statement a test can check. Where the probe offers two ways out, both are listed and the choice is an owner question in (h).

**C-INV-1 (INV-001). A waiting hand-back does not block the repo.** A hand-back round 2 or later waits for the person to re-approve, because the re-plan voids the approval (`predicates.py:249-259`). The design keeps that issue `in_progress` and counted in flight between rounds (D:616), and the cap `max_in_flight` defaults to 3 (`pr-a repos.py:54`, range 1 to 10 at `:255-259`). Nothing frees the place: D07 item 3 says the closing writer and expiry are "not yet designed", `--take` refuses an `in_progress` file with `already_dispatched` (D:708), and the only exits are `stopped` or a re-approval.
- Testable statement: a hand-back issue in the waiting step is either (i) not counted in `max_in_flight`, or (ii) moved to `stopped` with a named reason after an expiry, so that with three issues waiting for re-approval a new issue of the same repo is not refused with `coordinator_full`. The expiry length is not given by any source (OD-13).
- Second test: a coordinator restart (the rule that resumes every `in_progress` file, D07 item 4) does not start a worker for a waiting issue before the start gate passes; and the effect of `--take` on a waiting file is stated.

**C-INV-2 (INV-002). Something wakes the coordinator after the person re-approves.** The poll never wakes an issue whose store entry is not `failed` (`pr-a cycle.py:993-994`, "already woken, acknowledged or abandoned: never woken again"). The hourly check reads only `state,assignees` (D:571) and wave 1 "is not run again" at a hand-back (D:615), so the start re-check (MR-1) has no place to run at round 2. CLAY's statement that the issue "shows the skip reason" `edited_after_approval` is produced by the poll's `_examine` path, which is not reached for an acknowledged entry. Option (b) of G-3 (body left alone) avoids the wait but still needs the re-check after `replan` and before wave 4 (D:547, D:619).
- Testable statement: with an acknowledged entry whose approval is re-applied after the re-plan, the start re-check (approval present, `unchanged_since`, Status, `hold:backlog`, `plan_check`) runs and round 2 starts only after it passes; with the approval not re-applied, round 2 does not start and the person is told why. The re-check lives either in the coordinator (reading approval events itself) or in a poll path that wakes a waiting hand-back issue; the spec names which.

**C-INV-3 (INV-003). The per-repo config is tamper-protected or the controls it shapes fail closed.** The guard binds only the verb. D:688 says the keys "may live in a file the orchestrator itself edits ... guarded by the verb and by a test"; D07 item 5 says the config directory "is not tamper-protected" (`launch.py` lines 48 to 53, UNVERIFIED here); D04 item 7 requires the file to sit outside the orchestrator's write reach or be guarded by a hook. `refuse(argv)` sees only commands the verbs run (D:769, U42 open), so a direct edit of `~/.config/superclaude/issue-watch.d/<repo>.json` is not refused. The parser accepts weakening values: `merge_safety_files: []` means no hold (`pr-a repos.py:242-252`), `reviewers: "none"` becomes an empty tuple (`:227-231`), a bad `reach_daily_max` becomes 0, which means no cap (`:262-269`). What `review_none_present` does with an empty reviewers list is not stated (D:582, D06 item 4).
- Testable statement: a direct write (editor or shell) of one of those weakening values either is refused (the file sits outside the coordinator's write reach, or a hook blocks it), or does not weaken the control: with `merge_safety_files: []`, `reviewers` empty or a malformed `reach_daily_max`, the merge gate and the cap behave as the strict reading and the person is told, instead of passing. The result for an empty reviewers list is stated. The default 0 of `reach_daily_max` stays a separate owner decision (D11); only a malformed value must not be read as 0. Choice between protecting the file and failing closed (or both): OD-12.

**C-INV-4 (INV-004). The post-merge close has a stated authority.** D:799 says closeout's writes fall under the grants `issue.close` and `issue.comment`; D:605 makes closeout the single writer that closes the issue; D13 item 1 says its writes need a named grant. The rule rejects a standing `issue.close` (D04 item 5 releases it only per PR by a typed go), but the go entry is defined only for merges. After every merge wave 8 therefore either cannot close (two failed attempts give `closeout_failed`, state `escalated`, a row 9 escalation, D:605, T12 (a)) or closes without the go. Also, a PR body that says `Fixes` makes GitHub close the issue at the merge with no coordinator write (T12 (m), D:1140), and ruling 38 leaves the choice to the worker's own reading of the remaining list (D:619).
- Testable statement: wave 8 closes an issue only under a recorded authority, either (i) a go entry that covers the close as well as the merge, or (ii) an explicit closeout grant for `issue.close` recorded in chat; with neither, the issue stays open and the person is told, so that the failure path (two failed attempts give `closeout_failed` and a row 9 escalation, D:605) is not what every normal merge runs into. The spec states the `Fixes` bypass as a known limit (GitHub closes at the merge when the PR body says `Fixes`). Choice between (i) and (ii): OD-10.

### MEDIUM items as spec lines (INV-005 to INV-014, INV-016, INV-017)

The probe rates INV-009 LOW; it is included because the dispatch brief lists the range. Each row is a line the unified spec must carry.

| ID | Spec line the unified spec must carry | Check | Decision |
|---|---|---|---|
| INV-005 | Re-approval after a re-plan is a second gate only if three things hold, and the spec states them. (1) The approval is the latest `labeled` event (`predicates.py:200-215`); if the label is still on, a new approval needs unlabel then label, and an equal timestamp counts as changed (`:257-258`). (2) The Status allow-list (Research, Spec, Plan, Debug; D01 item 1c) still holds after round 1 merged. (3) The check accepts any actor id in `approvers` (`:216-223`) and the coordinator shares the owner's login (accepted risk L-1); no pattern in D:758 to D:765 blocks `gh issue edit --add-label issue-watch:approved`, so the agent that edited the body can re-approve its own plan. | Either a `refuse` pattern for that label command, or a stated limit line in the "narrows" wording. | Open: block or accept (not decided in any source). |
| INV-006 | One state-folder path map after the registry repo goes: state file, wake store, acknowledgment, audit log, handback files, `asks.json`, state lock. All are anchored on `<orchestrator-repo>/.orchestrator/` today (D:702, D:538, D:565, D:613, D:686, D:827 and the wake store of D10 item 1). The spec says who reads and who writes (the cron child cycle reads the state files read-only to count in-flight, D:702, while the coordinator session writes them), what replaces the per-`<short>` key of the `asks.json` count (D07 removes it), and whether the folder is gitignored inside the `Coordinator` worktree so `git add -A` cannot publish go entries or wake files. | The path map exists before Stage 2 of (c); a test asserts the folder is ignored by git. | Spec decision. |
| INV-007 | The reasons table is closed and pinned, and its final size and names are fixed. The pin is `59 - 14 - 5 + 5 + 17 == 62` (`test_audit.py:98`). Adding back 14, adding `coordinator_full`, `name_collision`, `no_checkout`, and removing what D07 deletes (`registry_invalid` at `audit.py:48`, `repo_not_listed` at `audit.py:89` and `cli.py:214`) gives a total no source states. One reason has three names: `held_incomplete` (`audit.py:92`, kept), `plan_incomplete` (D01) and `plan_missing` (D:543, `E-HELD`); the dashboard reads these names (D01 Implications). | One name per reason; the pin recomputed from the final set, not copied. | Spec decision. |
| INV-008 | One limits table lists every "3" and says which counter wins and when it resets. Wake: 3 deliveries in total (`wake.py:468`, `record.py:588`, 10-minute backoff at `:591`). A second counter `MAX_ATTEMPTS = 3` for failed entries (`record.py:585`). Restart: "bounded, 3 attempts, counter kept in the store" (D07 item 4) against "counts as delivery attempt 1" (D:710), so whether they share a counter is open. Hand-back: `HANDBACK_MAX` 3 gives 4 rounds (D:612). Cap: `max_in_flight` default 3 (`pr-a repos.py:54`) against D07 item 8, which holds the cap at 1 until claim agents get their own worktree. New coordinator ids per day: 6 (D:706, `DAY_CAP`). | A test per counter; the table names the winner. | Spec decision. |
| INV-009 | The plan size the owner accepts is stated: 13 T, 60 U, 28 K rows (101), six logic rewrites plus T12, setup steps on the rows that start a worker (section (d)). | Counts match section (d). | Handled in (d). |
| INV-010 | The verb list says which verb carries the merge. The twelve at D:510 include `lease` (deferred) and the `escalate --interrupt` option (rejected) and have no merge verb. D06 item 8 and D04 item 6 require one verb that demands the go entry, while D:588 still has wave 7 run `gh pr merge` as a plain command. D:513 separately says the group "gains four verbs". The spec lists the verbs to build and their count. | One list, one count; wave 7 calls the merge verb. | Spec decision. |
| INV-011 | Abandoned wakes are recoverable (M2) and the spec names who recovers them. D10 item 11 offers two ways: retarget to the next orchestrator of the repo with a new wake id, or keep the abandoned wake visible to a named reader. With one project-local coordinator (D07 items 1 and 2) the first has no target and D:706 forbids it (a re-route could deliver the same issue twice). The second needs a named reader, and the party that never acknowledged is the coordinator. `_examine` never wakes an abandoned entry (`cycle.py:993-994`) and the in-flight count includes only `pending`, `woken` and `unknown` entries (D:702), so a recovered abandoned wake sits outside the cap. | A named reader and a count rule. | Open: no source names the reader. |
| INV-012 | The default `grants` of a new install is chosen. D04 item 7 says an absent or malformed `grants` gives no grants (`pr-a repos.py:295`); D04's action row says to set the default to the four standing entries. With none, a fresh install refuses the plan call's body write and every `issue.hold` or `issue.comment` write with `E-NO-GRANT` (D:1100); with four, they are granted without an owner record, against the order that grants hold only duties recorded in chat (D06 item 8). | One default, stated; the install test matches it. | Open: OD-11. |
| INV-013 | The naming rule never blocks a mandatory escalation silently. Both writers refuse (exit 2, nothing written) any text failing `names_check` (D:847, D:684). The merge-safety escalation lists "the files that matched" (D:599) and IronClaude's default list contains `.claude/settings.json` (D:595); the deny list holds product names and `claude-...` patterns (D:832). Backtick spans, link titles and quoted fences are skipped (D:847); whether the escalation template fences paths is UNVERIFIED. The spec says whether a refused escalation fails open (written anyway) or closed (the person is never told and the hold stays on silently). | A test: a merge-safety escalation listing `.claude/settings.json` is written or visibly fails, never silent. | Open: OD-4. |
| INV-014 | The gate and the audit leave no unstated gap. AU4a and AU4c fire only for merges outside the gate (D:812, D:814). AU5 (conflict markers) is not held by the gate (D:815, "Already held by the merge gate? no") and T13 (e) expects it on a merged PR (D:1141). A conflict marker passes all 13 gate reasons, so a go on `merge_ok: true` can land it on an unprotected `master` (D01 point 3, `protected: false`) and the escalation comes after the fact, with `reach_daily_max` at 0, which means no cap (`repos.py:262-269`). | Either a pre-merge conflict-marker check in the gate, or the post-merge-only limit stated in the "narrows" wording. | Open: add the check or state the limit. |
| INV-016 | The merge gate wording lists its falsifiers. See section (g). | Wording check in (g). | Handled in (g). |
| INV-017 | The hand-back loop is written as "narrows unfinished work", with the falsifiers: a worker PR that says `Fixes` instead of `Refs` makes GitHub close the issue at the merge, the closeout answers `already_closed`, the loop never starts and nothing reopens it (T12 (m), D:1140); a `left_open` answer needs closeout callable from inside a wave (U2, K17) with `issue.close` authority (C-INV-4); `no_progress` compares text lines after trimming and case folding (D:612), so a worker that rewords criteria continues the loop while real progress with unchanged wording stops it; the cap of 3 is unmeasured by the design's own words (D:612). | Wording check; T12 case (m). | Handled in the wording. |

## (g) Wording rule: every control "narrows"

<!-- Source: Base (original) "narrows, never closes" wording (A-004, D06 item 10), with the falsifiers of INV-015, INV-016, INV-018, INV-019 from invariant-probe.md, merged per Change #5. INV-015, INV-018 and INV-019 are marked ADDRESSED by the probe because the limits are already stated in D06 and D05; INV-016 is UNADDRESSED because the specific falsifiers were not listed. -->

**The rule.** The unified spec, the element table and every skill or command text write each control as "narrows X" and never as "closes X" or "prevents X". Each control is followed by the cases that defeat it. A line that claims a control closes a risk fails review. Both sides accepted this (A-004: OURS REJECT as "closes", CLAY ACCEPT as a limit; D06 item 10).

| Control | Write it as | Falsifiers (what still gets through) | Source |
|---|---|---|---|
| `answer-check` plus a recorded go (INV-015) | Narrows a mistyped or stale go. Does not close a spoofed go. | It validates entry, question key, head sha and freshness only (D06 item 9). `--source <session or clickup-dm>` is a caller-supplied argument (D:694). The terminal accepts `orca terminal send` (D:112). The login is shared (D04 owner-answers line 162). Any process with terminal access, or the coordinator writing the go entry itself, produces an accepted entry. | INV-015, D06, D04 |
| Merge gate run twice plus `--match-head-commit` (INV-016) | Narrows an unsafe merge of a head the person did not see. Does not close unsafe merges. | (1) The gate reads `merge_safety_files` and `reviewers` from the tamperable config (C-INV-3). (2) `--match-head-commit` pins the head only (D:588); the base can advance between the second gate run and the merge, and `master` has no protection (D01 point 3, D:118: `maintain` rights). (3) The coordinator's own shell can run `gh pr merge` directly: `refuse` sees only verb commands (D:769), the launch guard has no merge level and cannot bind the coordinator (D05, LD:32), and a hook for it is open (U42); the audit finds it only afterwards. (4) AU5 is post-merge only (INV-014). | INV-016 |
| Required, staged launch guard (INV-018) | Narrows honest drift of started workers ("mitigates K12 for honest drift", D05). Does not close K12. | A script run (`bash ./push.sh`) passes every gate (D05's own INV-034). Only `master` and `main` are covered, so `integration` is open (D05's INV-019). Binding is keyed on one session id (D05's INV-003). A missing `jq` fails closed only for bound sessions. A server-side rule is the only full control, and `master` has `protected: false` (D01). | INV-018, D05 item 4 and its Unverified list |
| `plan_check` before approval (INV-019) | Narrows an issue with no plan at all. Does not prove the plan is good. | It proves presence, not quality (D12 condition S2, risk K23, D:1245). A thin or copied plan passes, including a round 2 body whose "Done so far" list is copied. The person's approval is the only quality gate, which is why INV-005 matters. | INV-019, D12 |
| `refuse(argv)` | Narrows the commands the verbs run. Does not bind the coordinator's other commands. | It sees only commands that verbs run (D:769, K22, U42 open). A direct edit or shell write is not refused (C-INV-3). | D04, D05, D06 |
| `E-NO-GRANT` | Narrows the writes the verbs make. | It does not see a raw `gh pr merge` (D06 INV-011) and covers at most 2 of 6 grant entries (D04 INV-006). | D04, D06 |
| Hand-back loop (INV-017) | Narrows unfinished work after a merge. Does not ensure it gets finished. | See the INV-017 row in (f): `Fixes` against `Refs`, closeout callability, `no_progress` by text lines, cap 3 unmeasured. | INV-017 |

**Check for the spec.** A grep of the final spec and element table for "closes", "prevents" and "ensures" next to any control in this table finds only negated uses ("does not close"). Not run here because the spec does not exist yet.

## (h) Open owner decisions

<!-- Source: Variant 1 and Variant 2 Round 2 "owner decision" lines (G-1 to G-9) merged per Change #3, plus the open choices of invariant-probe.md merged per Change #4. Answers are given in chat and recorded by the agent; no file is asked of the owner. -->

Thirteen questions. A default is shown only where a source gives one; "no default" means the sources leave the choice open. Every unanswered question resolves under the weighting rule (a tie goes to OURS).

**OD-1 (G-2). What is the default `plan_depth` for the plan call?**
- `quick`: the cheapest planner (`issue-worker-t3`); the same as the `--plan` default and as no key at all. Recommended by the merge as the tie-break; it runs against goal G6 (stronger models plan).
- `standard`: planner `issue-worker-t2`.
- `deep`: planner `issue-worker-t1`; the value Clay's default tier implies.

**OD-2 (G-3). How does hand-back round 2 and later start?**
- (a) Re-plan the body and the person re-applies the approval first (default). Safe; costs a person step per round and needs C-INV-1 and C-INV-2.
- (b) Leave the body alone; the remaining list travels in the handoff round block and a comment. No person step at round start; the body shows no "Done so far / Remaining", and `--remaining` still has no caller.
- A separate chat go per round is not offered (the plan rejects it).

**OD-3 (G-4). What is the scope of the naming rule?**
- A: as written; no attribution lines in PR bodies, comments or report entries; commit trailer allowed.
- B: scan only the coordinator's own writers (`report-entry`, `escalate`); workers' PR bodies keep current practice (default recommended by both sides). Run U54 first.
- C: no naming rule.

**OD-4 (INV-013). If the name check refuses a mandatory escalation, what happens?**
- Fail open: the escalation is written anyway; the rule is bypassed for that text.
- Fail closed: nothing is written; unless something else tells the person, the hold stays on silently.

**OD-5 (G-9 part 1). How does an audit escalation (AU4a, AU4c, AU5) reach the person?**
- Entry lines plus the notice step as D11 adopts it, cap key at its default 0 (the plan's choice; 0 means no cap, INV-014).
- Entry lines only, until the owner rules on the nine-row list and the notice cap (OURS' original line).

**OD-6 (G-9 part 2). Does the coordinator never tag or publish a release?**
- Yes (default): N6 stays an unconditional refusal; releases are run by a person or the release flow.
- No: an `answer_ref` pass path comes back, which routes the most irreversible action through a check that cannot tell a person from a script.

**OD-7 (G-6). May the coordinator ever interrupt a running worker besides context exhaustion?**
- No (default): `escalate --interrupt` is not built.
- Yes: needs a contract exception written like S6's, a rule that suppresses the L2 nudge afterwards, and the U40 receipt check.

**OD-8 (G-1). Build the lease comment before a second host or user runs a poll?**
- No (default): reserved design, not built.
- Yes: one `coordinator lease post|check` verb, a stale-lease rule, a renamed marker, T4 rewritten.

**OD-9 (G-7). Should the report list newly assignable issues (`could_assign`)?**
- No (default): the info streams stay off.
- Yes: switch the streams on after the U8 live capture; adds about 8 calls a cycle against a budget of 35.

**OD-10 (C-INV-4). What authorizes the post-merge close of the issue?**
- The go entry covers the close as well as the merge, per PR.
- An explicit closeout grant for `issue.close`, recorded in chat (not a standing grant).
- In both cases a `Fixes` line in the PR body still closes the issue at the merge with no coordinator write.

**OD-11 (INV-012). What are the default `grants` of a fresh install?**
- Empty: a fresh install refuses the plan call's body write and every `issue.hold` or `issue.comment` write until the owner records a grant.
- The four standing entries: they work at once but are granted without an owner record.

**OD-12 (C-INV-3). How is the per-repo config protected?**
- Put the file outside the coordinator's write reach or guard it with a hook (D04 item 7).
- Make the controls fail closed on weakening values (`merge_safety_files: []`, empty `reviewers`, malformed `reach_daily_max`).
- Both: the file is protected and the controls still fail closed.

**OD-13 (C-INV-1). How does a hand-back that waits for re-approval stop holding a place in flight?**
- Exclude the waiting step from the `max_in_flight` count.
- Keep it counted and give it an expiry; the expiry length is not given by any source and the owner sets it.

## (i) Unresolved points and Unverified list

<!-- Source: debate-transcript.md (convergence, unresolved points), base-selection.md (scoring limit), the "What I could not verify" lists of round2-rebuttal-1-ours.md and round2-rebuttal-2-clay.md, and the UNVERIFIED marks of invariant-probe.md and the Round 1 files; merged per Changes #2 to #4 -->

### Unresolved points

1. **Convergence is BLOCKED_BY_INVARIANTS.** 25 of 28 points converged (89.3 percent, threshold 80 percent). Disputed: G-2 (the plan key, resolved by the plan to a plain `plan_depth` key, default still open: OD-1), G-3 (mechanism, resolved by the plan to the start gate, option (a) or (b) open: OD-2) and G-9 part 1 (the channel, resolved by the plan to the notice step: OD-5). HIGH invariants INV-001 to INV-004 are carried as C-INV-1 to C-INV-4 because there is no Round 3.
2. **The four HIGH conditions are new requirements.** No Clay or owner source states them. Their wording is the fault-finder's and the merge's; the owner may accept, change or drop them.
3. **The verdicts are recommendations.** D01 R19, D04 R9 and R10 and the D06 amendments wait for the owner's word in chat (A-001). If the owner flips one, the rows that depend on it change.
4. **No carrier for the verb group.** The verb group has no carrier PR (A-003). D14 decides the fate of PR 686. The element table is keyed to files and rows so it survives either outcome.
5. **Three conflicting numbers still need one spec decision each:** the final size of the reasons table (INV-007), which of the "3" counters wins (INV-008) and the verb count with the merge verb (INV-010).
6. **Open spec choices with no source answer:** who recovers an abandoned wake (INV-011), whether the approval-label command is blocked (INV-005), whether AU5 gets a pre-merge check (INV-014), the state-folder path map and gitignore status (INV-006).
7. **Base selection scores are single-evaluator estimates.** The dual-pass position-bias run was not done by an independent agent (base-selection.md). The orchestrator wrote the diff analysis, scoring and plan itself; the four advocate rounds and the fault-finder were separate agents (debate-transcript.md).
8. **Plan order against the dispatch brief.** The plan grouped the HIGH invariants into three conditions; this document uses four (see merge-log.md, Change #4).
9. **Already addressed in the probe, no condition needed:** INV-015, INV-018 and INV-019 (limits stated, carried into (g)) and INV-020 (acknowledging only after the state file exists is safe with exclusive create, because a crash between the two makes the next delivery find the file, classed `already_claimed`, D:536 and D:538, D10 item 10).

### Unverified list

Items no writer of the source files could verify, kept as stated in them.

- The coordinator spec (IronFlow, outside this repository): rows FR-8, FR-10, FR-23, FR-24, Q12 and the amendments C25 to C29.
- Behavior and numbers: the worker tier path through `worker-start --model <picker id>` (U28, D:726); which effort levels `worker-start` accepts (U30); the mailbox send from outside a Run (U5); session detection (U25); the missing Orca receipt (U40); the open hook for commands outside the verbs (U42); the replies of the info search streams (U8); `HANDBACK_MAX` = 3, which D:612 calls "this design's value, not measured"; the 60-minute reviewer re-trigger.
- The cap of 5 notices: D:1177 says "not ruled on; open", while D:686 and D:877 say "settled as recommended" (ruling 39). Either way it is Clay's ruling.
- Counts: the INV-009 grep counts (13, 60, 28) were not re-run here; the number of rows that need the setup step; the size of the "same three or four edits" CLAY says repeat across rows; the number of merged PR bodies with "Generated with" beyond the last 30.
- Code and text not read: `refs/claim.md` Wave 2 beyond what the design quotes; `launch.py` lines 48 to 53 in the owner's worktree (config directory not tamper-protected, taken from D07 item 5); D:300 to D:420 (so completeness of the amendment list is not certified); whether `handback` exists in pr-a or pr-p (only master was searched); whether the escalation template fences paths (INV-013); any stale-lease or interrupt-suppression rule outside the lines read; Q26's exact text; the owner's unpushed plan rows R9, R17, R23, R25 and R33.
- Environment: whether Orca `--agent claude` workers run with the permission bypass; whether round-2 closeout done-checks behave when the body keeps the original full criteria (option (b) of G-3); whether the "Jev" and "IronClaude" issue titles would trip a deny list (the deny-list data is not written).
- History: the merge timings of PR 681 (Clay's merged design text) and PR 682, and the absence of an `ironbelly` approval on PR 681, were taken from D03 and FULL-REPORT.md and not re-checked; whether the owner has a coordinator-layer test plan outside the verdicts.
- Verb existence: `escalate`, `merge-gate`, `answer-check` and `asks.json` were searched for in `src/` of master, pr-a and pr-p only (D06 Unverified); they do not exist there.

