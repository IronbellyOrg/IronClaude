# Adversarial Debate Transcript: D15 Clay strengths bundle

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe; no Round 3)
- Rounds completed: 2 plus Round 2.5
- Convergence achieved: 89.3% (25 of 28 points), threshold 80%
- Convergence status: BLOCKED_BY_INVARIANTS (4 HIGH UNADDRESSED invariants: INV-001 to INV-004)
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY); 1 fault-finder
- Full round texts (not copied here; authoritative):
  - `rounds/round1-advocate-1-ours.md`, `rounds/round1-advocate-2-clay.md`
  - `rounds/round2-rebuttal-1-ours.md`, `rounds/round2-rebuttal-2-clay.md`
  - `invariant-probe.md` (Round 2.5)

## Round 1: Advocate statements (summary)
- OURS: per-element table (adopt as is, with change, reject, defer). Steelmanned CLAY's interlock argument. Conceded the merge path is one build unit, one verb group is the build home, T1 to T13 plus registers are the test-plan skeleton, and the wake transport is CLAY's. Shared assumptions: A-001 QUALIFY, A-002 QUALIFY, A-003 QUALIFY, A-004 REJECT, A-005 ACCEPT, A-006 ACCEPT, A-007 ACCEPT. No omissions.
- CLAY: withdrew "as built" and conceded C-006, C-009, X-002 and the tier settings. Kept: build the control verbs as one group against one contract, T1 to T13 plus U and K registers as the single test plan, an amendment list for the owner's rules. Shared assumptions: A-001 QUALIFY, A-002 REJECT in part, A-003 QUALIFY, A-004 ACCEPT as a limit, A-005 ACCEPT, A-006 ACCEPT, A-007 QUALIFY. No omissions.

## Round 2: Rebuttals (summary)
- OURS conceded C-001, C-003, C-004, C-005 to HYBRID and X-001 to SPLIT; kept C-006, C-007, C-009, X-002. Named the interlock closure (merge path only). Decided nine gaps G-1 to G-9 that no verdict covered.
- CLAY accepted nearly all concessions; added a shared substrate (runner, `refuse`, JSON contract, state lock) that every verb needs first; added that D01 puts approval back so most T rows need an approval setup step. On the gaps: agreed G-1, G-4, G-5, G-6, G-7, G-8; contested G-2 (plan_tier is not duplicated for `--plan`: `--plan --depth` defaults to quick, so a plain `plan_depth` key is needed), G-3 (mechanism: approval re-application, not a new chat go) and G-9 part 1 (use the notice step, not report line only).

## Round 2.5: Invariant probe
20 findings. UNADDRESSED: 16 (HIGH 4, MEDIUM 11, LOW 1). ADDRESSED: 4. See `invariant-probe.md`.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001, S-002 | Tie | 90% | Same layout and evidence style. |
| C-001 Unit of adoption | HYBRID | 85% | Rule rows per element (OURS); substrate first and merge path as one tested unit (CLAY). Both final positions agree. |
| C-002 Unbuilt verbs | HYBRID | 85% | Design text only (OURS); one group, one contract, D:140 (CLAY). |
| C-003 62-reason table | HYBRID | 90% | Closed pinned table kept; 14 approval reasons back; pin rewritten (`test_audit.py:86-98`). |
| C-004 Wake transport | HYBRID | 90% | CLAY file plus ack; M1, M2 mandatory. |
| C-005 Tiers and hand-back | HYBRID | 75% | Hand-back adopted; tiers as requests; plan key dispute (plan_depth) and G-3 mechanism open. |
| C-006 Contested rules | OURS | 95% | Both sides agree. |
| C-007 Rewrite cost | OURS (tie) | 85% | Rename (D08) and re-home (D07) paid per row either way. |
| C-008 Readiness evidence | HYBRID | 85% | Merged pieces count; unbuilt verbs carry no proof. |
| C-009 Settings home | OURS home, CLAY keys | 90% | `issue-watch.d/<repo>.json`; key names kept. |
| X-001 "never ran live" | SPLIT | 85% | Tie on never ran live; benefit rests on capability gap. |
| X-002 Rewrite multiplies | OURS (tie) | 85% | Same either way. |
| A-001 verdicts as baseline | QUALIFY | 90% | Every row carries "depends on owner decision" where a verdict says so. |
| A-002 per-element classification | QUALIFY | 85% | Holds except the merge path. |
| A-003 carrier PR exists | QUALIFY | 85% | Verb group has no carrier yet; D14 decides PR 686. |
| A-004 verbs bind what they claim | REJECT as "closes", ACCEPT as "narrows" | 95% | D06 item 10 wording rule. |
| A-006 one settings file | ACCEPT | 90% | D07. |
| A-007 rename before merge | ACCEPT | 90% | D08 action 8. |
| G-1 lease comment | Defer | 80% | Trigger absent; needs stale-lease rule if built. |
| G-2 tiers | HYBRID | 65% | `coordinator_tier`, `worker_tier` as requests; `plan_depth` plain key (default is an owner call); efforts wait for U30. |
| G-3 hand-back | Adopt with change | 65% | Round 2 must pass the start gate again; mechanism open (INV-001, INV-002). |
| G-4 naming rule | Owner decision | 80% | 25 of 30 merged PR bodies carry "Generated with". |
| G-5 DQ9 | Typing yes, approving prompts no | 85% | WC:122, WC:137. |
| G-6 N7 interrupt | Reject | 85% | No incident cited; receipt unverifiable (U40). |
| G-7 info streams | Off by default | 85% | U8 unverified. |
| G-8 setup-clone | Reject | 85% | Needs `repos.yaml`, removed by D07. |
| G-9 audit rows, N6 | Adopt with change | 75% | AU5 narrowed; N6 unconditional refusal; escalation channel open. |

## Convergence Assessment
- Points resolved: 25 of 28 (disputed: G-2 plan key, G-3 mechanism, G-9 channel)
- Alignment: 89.3%
- Threshold: 80%
- Status: BLOCKED_BY_INVARIANTS (HIGH UNADDRESSED: INV-001, INV-002, INV-003, INV-004; standard depth has no Round 3, so they become conditions of the merged output)
- Unresolved points: G-2, G-3, G-9 (part 1)
- Taxonomy coverage: L1 (naming, wording: G-4), L2 (structure: C-001, C-009, G-2), L3 (state, guard, concurrency: INV-001 to INV-004, C-004 M1/M2) all covered.
- Process note: the orchestrator wrote the diff analysis, scoring and plan itself; the four advocate rounds and the fault-finder were separate agents.
