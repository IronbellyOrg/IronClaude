# OAG2 qualitative layer, pass 2 (reverse order: Variant 2 first, then Variant 1)

Rubric: 30 binary criteria. Each verdict rests on a quote or section of the variant. Snapshot checked: /home/coder/.cache/ic-snap-20261120/master.

## Variant 2 (position CLAY: no sweep file, titles and links only, end questions exception now)

File: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/variant-2-original.md

| Criterion | Evidence (short quote or section) | Verdict |
|---|---|---|
| C1 requirements | Claim 1-3 map to OA-9, OA-17a, OA-17b; sections Claim, Mechanism, Cited facts (8), What it costs, What it risks, What it gets right | MET |
| C2 edge cases | Fact 1 window mismatch; fact 5 "Rich markup ... pass unchanged and there is no length cap"; fact 7 "listed again as open" | MET |
| C3 dependencies | "Design work for a shared question id before the observer ships"; "WC-16 would need an edit" | MET |
| C4 success criteria | No done-condition or acceptance test anywhere in the paper | NOT MET |
| C5 out of scope | No out-of-scope statement; only "Clay posted no text ... (UNVERIFIED that they hold these views)" | NOT MET |
| K1 no factual errors | Spot checks match (commands.py:99, probes.py:130, collector.py:28-29, classify.py:303-324/922, SKILL.md:61-62, report.py:642-650, common.py:139-141, sanitize.py:1-7, questions.py:9-12, adapter.py:32). Small slip: "cuts cells at 200" is cited to report.py:569-599, but CELL_MAX is at report.py:24 | MET |
| K2 feasible | "Observer: reads Orca on its own cycle, as it does today"; report collects itself | MET |
| K3 terminology | "collection", "window", "report", "observer" used the same way throughout | MET |
| K4 no contradictions | Cost says "the observer keeps its own worker-list read and the sweep's eight classes" right after saying the 90 s sweep "cannot run inside the observer's 15 s cycle", and Mechanism says "Neither is a client of the other"; where the observer gets classes is left unclear | NOT MET |
| K5 claims supported | Each claim tied to a numbered fact; UNVERIFIED items flagged ("No retention rule was found ... UNVERIFIED") | MET |
| S1 ordering | Claim, Mechanism, Facts, Cost, Risk, Gets right | MET |
| S2 hierarchy | All sections at H2, flat lists | MET |
| S3 separation | Cost, Risk and Gets-right are separate sections | MET |
| S4 navigation | Numbered claims and facts; cross-reference "facts 4 and 5", "fact 1" | MET |
| S5 conventions | Claim, mechanism, 8 facts, cost, risk, what it gets right as requested | MET |
| L1 unambiguous | "could differ", "would need" are used with concrete subjects; no "should consider / as appropriate" | MET |
| L2 concrete | File:line cites, "5,000 characters stay 5,000", "90 s", "15 s" | MET |
| L3 section purpose | Each section has a single stated job | MET |
| L4 terms defined | OA-9, OA-17, D11, WC-16, TOPICS.md, "Clay's line" never defined | NOT MET |
| L5 next steps | "Design work for a shared question id before the observer ships" and the three numbered claims as decision points | MET |
| R1 3+ risks with probability and impact | Only two risks ("Readers disagree within a minute", "Titles-only makes the screen a list of links"); no probabilities | NOT MET |
| R2 mitigations | No mitigation given for either risk | NOT MET |
| R3 failure modes and recovery | No recovery path stated | NOT MET |
| R4 external dependency failure | Orca read load is mentioned ("more Orca reads") but no Orca failure case | NOT MET |
| R5 monitoring or validation | None | NOT MET |
| I1 collection boundaries | No empty, one-row or maximum-size collection case (the 5,000 character test is a string, not a collection) | NOT MET |
| I2 cross-component state | Fact 7: observer ledger vs work report "Needs you", "A shared id is the only fix" | MET |
| I3 guard gaps | Fact 5: sanitizer "removes terminal controls only", no markup guard, no length cap; fact 4 no field list | MET |
| I4 count divergence | No off-by-one or inclusive/exclusive case; "stale = last < ctx.window_start" is cited for window difference, not as a boundary bug | NOT MET |
| I5 interaction effects | Fact 1 plus fact 2: window of the producer combined with one checkout root; sweep 90 s vs observer 15 s | MET |

Subtotals, Variant 2: Completeness 3/5 (C1, C2, C3). Correctness 4/5 (K1, K2, K3, K5). Structure 5/5. Clarity 4/5 (L1, L2, L3, L5). Risk coverage 0/5. Invariant and edge case 3/5 (I2, I3, I5).

**Variant 2 total: 19 / 30**

## Variant 1 (position OURS: sweep saves JSON beside the report, entry text via sanitizer, questions exception labelled)

File: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/variant-1-original.md

| Criterion | Evidence (short quote or section) | Verdict |
|---|---|---|
| C1 requirements | Claim 1-3 map to OA-9, OA-17a, OA-17b; Mechanism, 9 facts, Cost, Risk, Gets right | MET |
| C2 edge cases | Risks: staleness ("a missing or old file is its own state, never 'no sessions'"), window problem, one checkout root | MET |
| C3 dependencies | "contract note docs/designs/observe-sweep-contract.md (unwritten ...)"; "Work item S5"; "the spec must say who passes which --window" | MET |
| C4 success criteria | No acceptance test or done-condition for the saved file or the screen | NOT MET |
| C5 out of scope | Claim 3: "until a shared questions block exists"; fact 8 "ending the exception now needs a design that does not exist yet"; "nothing else about it changes" | MET |
| K1 no factual errors | Spot checks match (commands.py:278 `click.echo(payload)`, `_publish` at 153, probes.py:130, collector.py:28-29, WORKER-CONTRACT.md WC-16 at 287-289 with "at most once every 5 minutes", SKILL.md:61, adapter.py:29/32/34-50/111, observe/commands.py:67,70, report.py:613 `to_json`, classify.py:303-324/922, common.py:139-141, sanitize.py:1-7). The "12 top-level keys" count was not fully counted | MET |
| K2 feasible | "publish a second file with the same stem from the same `to_json` call" on an existing atomic path | MET |
| K3 terminology | "sweep", "report", "observer", "entry text", "exception" used consistently | MET |
| K4 no contradictions | Claim 1 says one file for every reader; risk and "gets right" explain the work report runs `--window` and saves its own file, still one writer path | MET |
| K5 claims supported | Facts 1-9 back each claim; UNVERIFIED flagged on non-consuming read | MET |
| S1 ordering | Claim, Mechanism, Facts, Cost, Risk, Gets right | MET |
| S2 hierarchy | All sections at H2 | MET |
| S3 separation | Cost, Risk, Gets-right distinct | MET |
| S4 navigation | Numbered claims and facts, "(R4)" and "S5" tags, decision references | MET |
| S5 conventions | Required position-paper parts all present | MET |
| L1 unambiguous | Concrete verbs ("The spec must list which entry fields the observer shows") | MET |
| L2 concrete | "`<UTC>-sweep.json`", "15 seconds", "90 seconds", named files and lines | MET |
| L3 section purpose | Each section has one job | MET |
| L4 terms defined | OA-9, OA-17, D11, R4, S5, "JSON v1" used without definition | NOT MET |
| L5 next steps | "The spec must say who passes which `--window`"; "The spec must list which entry fields the observer shows" | MET |
| R1 3+ risks with probability and impact | Four risks named (staleness, window, one root, entry text) with impact, but no probability for any | NOT MET |
| R2 mitigations | Staleness: "the screen shows `observed_at` and an age"; the other three get a spec rule | MET |
| R3 failure modes and recovery | "A missing or old file is its own state, never 'no sessions'"; three states "empty folder, zero rows, could not read" | MET |
| R4 external dependencies | Questions read "not tested live (UNVERIFIED)"; sweep up to 90 s against Orca; "could not read" state | MET |
| R5 monitoring or validation | "shows `observed_at` and an age" plus the distinct stale state | MET |
| I1 collection boundaries | "three states (empty folder, zero rows, could not read) stay distinct" | MET |
| I2 cross-component state | File as the hand-off between sweep, observer and work report; questions panel with its own Orca call | MET |
| I3 guard gaps | Entry text carries `recommend` and `suggested` slots, so "The spec must list which entry fields the observer shows" | MET |
| I4 count divergence | No off-by-one or inclusive/exclusive case | NOT MET |
| I5 interaction effects | Fact 2: sweep 90 s budget against the observer 15 s cycle; window of producer combined with shared file | MET |

Subtotals, Variant 1: Completeness 4/5 (C1, C2, C3, C5). Correctness 5/5. Structure 5/5. Clarity 4/5 (L1, L2, L3, L5). Risk coverage 4/5 (R2, R3, R4, R5). Invariant and edge case 4/5 (I1, I2, I3, I5).

**Variant 1 total: 26 / 30**

## Citations spot checked against the snapshot

Snapshot root: /home/coder/.cache/ic-snap-20261120/master/src/superclaude

| Variant | Citation | Result |
|---|---|---|
| V2 | cli/sweep/commands.py:99 `_check_output` | Confirmed (function defined there) |
| V2 | cli/sweep/classify.py:303-324 and :922 `stale = last < ctx.window_start` | Confirmed |
| V2 | skills/sc-sweep-protocol/SKILL.md:61-62 Will Not list | Confirmed ("Recommend anything" at 61, "Edit, stage or delete a file" at 62) |
| V2 | cli/sweep/report.py:642-650 `rows[].evidence` | Confirmed |
| V2 | skills/agent-work-report/scripts/common.py:139-141 `recommend`, `needs`, `how` slots | Confirmed |
| V2 | cli/observe/sanitize.py:1-7 docstring on markup | Confirmed |
| V2 | cli/observe/questions.py:9-12 "listed again as open" | Confirmed |
| V2 | cli/observe/adapter.py:32 question template | Confirmed |
| V2 | cli/sweep/probes.py:130 and cli/observe/collector.py:28-29 | Confirmed (90.0 and 15.0) |
| V2 | cli/sweep/report.py:569-599 "cuts cells at 200" | Mostly confirmed: escape list and control stripping are there; the 200 cut is `CELL_MAX` at report.py:24, outside the cited range. Minor, not counted as a wrong citation |
| V1 | cli/sweep/commands.py:278 `click.echo(payload)` | Confirmed |
| V1 | cli/sweep/commands.py:153-193 `_publish` | Confirmed at start (153 defines `_publish`; atomic temp-then-link pattern per docstring) |
| V1 | cli/sweep/probes.py:130 and cli/observe/collector.py:28-29 | Confirmed |
| V1 | core/WORKER-CONTRACT.md:287-289 WC-16 | Confirmed (heading at 287, "at most once every 5 minutes" at 289) |
| V1 | skills/sc-sweep-protocol/SKILL.md:61 | Confirmed |
| V1 | cli/observe/adapter.py:29, :32, :34-50, :111 | Confirmed (worker-list template, question template, forbidden set with `--ack --wait --peek send reply`, `_is_question_shape`) |
| V1 | cli/observe/commands.py:67,70 gates `True` | Confirmed (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`) |
| V1 | cli/sweep/report.py:613-640 JSON v1 object | Confirmed start of `to_json` at 613; the exact "12 top-level keys" was not fully counted (7 listed through `sources`, more follow) |
| V1 | cli/sweep/classify.py:303-324, :922 | Confirmed |
| V1 | common.py:139-141 and sanitize.py:1-7 | Confirmed |

No cited line in either paper was found wrong. Claims that point to D11/VERDICT.md, TOPICS.md, the tech reference, and the authors' own sanitizer runs were not checked (outside the snapshot or not allowed to read).
