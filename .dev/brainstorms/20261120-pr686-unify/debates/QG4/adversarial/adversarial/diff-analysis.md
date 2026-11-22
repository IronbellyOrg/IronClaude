# Diff Analysis: position paper comparison (QG4: build now or reserve)

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant 1 = OURS, the owner's line; Variant 2 = CLAY, Clay's line), Mode A, depth quick
- Total differences found: 17
- Categories: structural (2), content (7), contradictions (3), unique (6), shared assumptions (5)
- Verification note: the analyst re-read the cited lines in the snapshot `/home/coder/.cache/ic-snap-20261120/master` (design lines D:113, D:137, D:749, D:764, D:1117, D:1170, D:1197, D:1298; `WORKER-CONTRACT.md` lines 63, 124, 131-137, 152, 164; `claim.md:43`; `collect.py:200-210`). Results are cited per row.

## Structural Differences
| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Section layout and wording style | Claim, one block per OD, "Cost of No / Risk of No / What it gets right", closing summary of what is kept | Claim, one block per OD, "Risks / What it gets right / Honest limit", closing summary of separable benefits | Low | L1 |
| S-002 | Closing position | Summary states three reserved designs with triggers | Summary concedes OD-7 loses on evidence and keeps three separable benefits | Medium | L2 |

## Content Differences
| # | Topic | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|---|---|---|---|---|
| C-001 | OD-7 answer: build the interrupt verb (`escalate --interrupt`, N7) | No; closed unless the owner asks | Yes, narrowly (escalation first, one caller, one verb) | High | L2 |
| C-002 | OD-7 what the contract says about interrupts | Cites the input-veto line `WORKER-CONTRACT.md:137` as "never interrupt" next to the one S6 exception (`:63`, `:124`) | Says line 137 sits under "Answers and acks" and is not a general rule, S6 proves it | Medium | L2 |
| C-003 | OD-7 what happens after an interrupt | Worker idles; L2 nudge (`:164`) tells it to continue, undoing the interrupt; design has no suppression rule | Same fact listed as a risk that needs a suppression rule added | High | L3 |
| C-004 | OD-8 answer: build the lease comment (`lease post/check`, lowest comment id wins) | No; reserved design with trigger | Yes now | High | L3 |
| C-005 | OD-8 failure of a crashed lease (a lease never edited to `released` keeps the lowest comment id) | Defect of the design as written, no stale-lease rule found | Same defect listed as a risk; no fix offered | High | L3 |
| C-006 | OD-9 answer: switch the three info streams on and list `could_assign` | No; off behind one switch, enable after U8 live capture | Yes now | Medium | L2 |
| C-007 | OD-9 evidence for the streams | `mention` and `affects` are subsets of the report's `involves` search (`collect.py:200-210`); replies unverified (U8) | `could_assign` is new awareness; code written; cost 8 calls of 35 (D:137) | Medium | L2 |

## Contradictions
| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Scope of `WORKER-CONTRACT.md:137` | "The input-veto line says never interrupt" used as contract text against N7 | The line is under "Answers and acks" (heading at `:131`) and governs the typed ack copy only | Medium. Checked: line 137 is the last bullet of the "Answers and acks" block (`:131-138`). CLAY's reading of scope is correct; OURS overstated it. What stays true: no contract text authorizes N7 (D:749, D:764 add it as a new exception) |
| X-002 | Whether a double claim can happen today | "Not possible on the present single-host topology" | "Nothing prevents a second user or host from polling; no code change needed" | Medium. Both are partly right: D:113 layers 1 to 3 cover one host; a second host or user is outside them and is the case layer 4 exists for (D:113). The disagreement is whether that trigger is present (D07 topology says no) |
| X-003 | Strength of the narrow guard (CLAY internal) | n/a | "Narrow guard" (escalation first, one caller) versus its own risks: no receipt (U40, D:1298), nudge undoes it, no incident cited | High for OD-7. The guard limits who may interrupt, not whether an interrupt lands or stays (D:1298, `:164`) |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | OURS | `collect.py:200-210` shows `mention`/`affects` are already collected by `involves` | High |
| U-002 | OURS | Ruling 25 (N7) is among Clay's rulings 23 to 35 (D:1170, D:1197), not an owner decision | Medium |
| U-003 | OURS | Reserved-design form with explicit triggers and build conditions (contract exception, nudge suppression, U40 check; stale-lease rule; U8 capture) | High |
| U-004 | CLAY | D:925-928 lists the five coordinator-spec changes C25 to C29 N7 would need (cost of the "yes") | Medium |
| U-005 | CLAY | Later build costs a migration of persisted names and state steps (`lease_posted`, `claim_started`, D:547) | Medium |
| U-006 | CLAY | Escalation-first ordering rule (write the escalation, send nothing if refused) is worth keeping without the interrupt | High |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | U40 (no Orca receipt for steered versus queued) and U8 (info search replies) stay unverified until a live test; neither paper proposes running them now | Both list them as risks | Decides OD-7 and OD-9 timing | UNSTATED (STATED as a risk, not as a premise) |
| A-002 | An unobserved risk with no present trigger counts as a tie, and a tie goes to the owner's line (weighting rule) | Both accept the "reserve" form as the fallback | Decides OD-8 | STATED in brief |
| A-003 | The design has no stale-lease rule anywhere (grep of `lease` in D shows none) | Both | OD-8 defect claim | UNSTATED; checked by the analyst: lines containing `lease` (D:113, D:510, D:543-547) have no stale, expiry or timeout rule |
| A-004 | The nine-row escalation table of D:749/5.6 is adopted in some form (N7's "major issue" = a row of that table) | Both | OD-7 scope | UNSTATED; D15 OD-5 left the list as an owner decision |
| A-005 | PR 686's info-stream code survives the PR 686 adaptation (D14, adapt in place) so "the code exists" holds | Both | OD-9 cost of keeping versus deleting | UNSTATED |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, C-004, C-005, X-003
- Taxonomy levels covered: L1 (S-001), L2 (S-002, C-001, C-002, C-006, C-007), L3 (C-003, C-004, C-005)
- Similarity check: differences exceed 10 percent of comparable items; debate proceeds.
