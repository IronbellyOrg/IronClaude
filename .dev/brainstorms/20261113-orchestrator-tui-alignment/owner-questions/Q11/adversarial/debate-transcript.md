# Adversarial Debate Transcript: Q11

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 82% (9 of 11 scored points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, each a spawned general-purpose sub-agent (Variant 1 persona analyzer, Variant 2 persona architect, Variant 3 persona qa). No agent failures.
- Advocate statements on disk: round1-advocate-V1.md, round1-advocate-V2.md, round1-advocate-V3.md (full text appended below)
- Variant map: Variant 1 = proposal-A (both, now); Variant 2 = proposal-B (sweep summary only until the contract note); Variant 3 = proposal-C (neither yet, park the clause)

## Unassigned picks (each advocate's honest choice if not assigned a variant)
- Advocate V1: Variant 2, plus the V5:217 check (`observe --once --run <run>` from the coordinator terminal) before the observer text ever joins.
- Advocate V2: Variant 2, plus Variant 3's caveat that no 3-to-5-minute cadence is promised until the loop exists, plus Variant 1's Q-1 check as a precondition.
- Advocate V3: Variant 2, plus a ledger note that no loop exists yet so the cadence is not claimed as met.
- Result: 3 of 3 pick Variant 2 when unassigned.

## Orchestrator spot-checks of new evidence raised in Round 1
- seed-brief.md:17 (Advocate V3): re-read. "The owner chose (2026-11-07, via the coordinator) that the first PR delivers only a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout". Confirmed.
- docs/designs/orchestrator-mode.md:603: re-read. The sweep's report file layout "is SPEC section 9 (lines 342-392), copied from #409". So the #409-layout static report already exists as the sweep's report file; the chat reply carries its counts and path. This narrows Variant 1's fidelity advantage (C-005) and supports Variant 2.
- pragmatic.md:23 and :25 (Advocate V3): the exception is per actual `/sc:sweep` invocation; :25 was not re-read by the orchestrator (UNVERIFIED wording, the :23 text was read).

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (agreed) | 90% | Same five sections in all three. |
| C-001 | L2 | 1 | 2 | 3 | unresolved (split on assigned positions) | 50% | Each advocate backed its own content; all three unassigned picks are Variant 2. |
| C-002 | L2 | 2 | 2 | 3 | Variant 2 | 75% | Wait for the note; Variant 1's advocate conceded "now" is weakest. |
| C-003 | L2 | 2 | 2 | 2 | Variant 2 | 92% | Zero edits; section 6.7 already says it (merged-requirements.md:1040). |
| C-004 | L3 | 1 | 3 | 3 | Variant 3 | 70% | WC-16 is a cap, not a schedule; nothing runs a cadence (debate-transcript.md:625 in ADJ debate; question.md fact 10). |
| C-005 | L2 | 1 | 1 | 1 | Variant 1 | 85% | Dashboard-like text is closest to "taking inspiration from #409"; weakened by orchestrator-mode.md:603. |
| X-001 | L3 | 2 | 2 | 2 | Variant 2 | 92% | Do not name `observe` in coordinator rules before the note (variant-5-original.md:222). |
| X-002 | L2 | 1 | 2 | 3 | unresolved (split) | 50% | Whether the per-invocation sweep reply counts as the periodic report. |
| X-003 | L2 | 2 | 2 | 3 | Variant 2 | 75% | Keep 6.7 as written; no gain from editing it. |
| A-001 | L2 | QUALIFY | QUALIFY | QUALIFY | agreed: QUALIFY | 90% | Cheap to reverse for Variants 2 and 3; Variant 1 implies later edits. |
| A-002 | L3 | ACCEPT | QUALIFY | QUALIFY | agreed: QUALIFY | 70% | The note is planned but undated; add a fallback review point. |
| U-001 | n/a | 1 | 1 | 1 | Variant 1 (contribution valid) | 80% | `observe --once` writes no file without `--snapshot` (ADJ E-17). |
| U-002 | n/a | 1 | 1 | 1 | Variant 1 (contribution valid) | 85% | Q-1 risk for the coordinator terminal is UNVERIFIED and must be tested before any observer text joins. |
| U-003 | n/a | 3 | 3 | 3 | Variant 3 (contribution valid) | 77% | The loop is unbuilt; no cadence can be claimed as met. |

## Convergence Assessment
- Points resolved: 9 of 11 (denominator counts S, C, X and A points; U points are contributions, scored but not counted)
- Alignment: 82%
- Threshold: 80%
- Taxonomy coverage: L1 1 point, L2 7 points, L3 3 points; all levels covered
- Invariant gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: C-001, X-002 (both are the core "which report" choice on assigned positions; every advocate's unassigned pick resolves them to Variant 2)

## Round 1: Advocate Statements

The three statements follow verbatim.


---

### Round 1 advocate statement: Variant 1 (both reports, now)

Advocate: Variant 1 (proposal A). Persona: analyzer. Depth: quick, Round 1 only.
Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. "V5" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-5-original.md`. "MR" is `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. MR:748 and MR:1032 are taken from question.md and were not re-read by this advocate.

#### Position summary

Variant 1 is the only answer that gives #339 what it actually asked for: a static report of all agents, sessions and worktrees modelled on #409, not just a count line and a file path. Both programs it names already exist, the observer's one-shot mode writes no file, so it can sit beside the sweep without breaking any rule, and the decision is recorded-only, so the owner loses little by stating the full intent now.

#### Steelman

**Variant 2 (sweep summary only, until the contract note).** Its strongest form: this is the spec's own recommended answer and its default (MR:538), and section 6.7 already says it (MR:1040), so choosing it costs zero edits to the spec, the worker contract, the sweep skill, the output style or the open sweep PR. It keeps one source of truth in chat while the observer and the sweep still use different status words (V5:216 lists the shared word list the contract note must fix: stale, unknown, unavailable, historical and others). It also follows V5's D2 recommendation exactly: "keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet" (V5:222). It is the lowest-risk, most reversible choice, and it honestly states its own gap: "every 3 minutes" is not met and the reply is narrower than #409.

**Variant 3 (neither yet, park the clause).** Its strongest form: no coordinator loop exists to print anything every 3 to 5 minutes (question.md fact 10), and WC-16 is a cap, not a schedule (ADJ:81; `src/superclaude/core/WORKER-CONTRACT.md:109` "at most once every 5 minutes"). Promising a cadence with nothing to run it is a false promise. The owner's stated preference is that automated status shows outstanding decisions only (MR:1040, quoting SEED Batch 2 item 8). Parking avoids picking a format before the contract note fixes a shared word list. It is the most honest about what exists today.

#### Strengths claimed

1. **Fidelity to the issue.** The issue summary says #339 wants "a static report of all agents, sessions and worktrees (modelled on #409) that replaces the usual end-of-message table" (`.dev/issues/339/issue-summary.md:10`), and lists #409 as the design "the static report layout should follow" (same file :26). The sweep's exempt reply prints "only the summary counts and the report path" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:35`, rule at :31-43). Only the observer text is a fleet picture. Variant 1 is the only variant that meets the literal ask (diff C-005).
2. **No new program.** `observe --once` is built: `run_once` collects once, renders a bound-width screen when `--width` is given, prints it, and writes a snapshot only when `--snapshot` is passed (`src/superclaude/cli/observe/commands.py:215-237`). ADJ E-17 says the same and is marked "verified in Round 1" (ADJ:143): "the #339 'static report in chat' ask does not need a new program".
3. **No conflict with the one-report-per-run rule.** NFR-001 says "a sweep adds exactly one report file" (ADJ:83). Because `observe --once` writes nothing without `--snapshot` (commands.py:232-236), it can run between sweeps without adding files (diff U-001).
4. **It is the only variant that can reach the 3-minute end of "3 to 5 minutes".** The sweep is capped at once every 5 minutes (WORKER-CONTRACT.md:109). The observer carries no such cap in the contract, so a 3-minute report is possible only with the observer (diff C-004).
5. **Honest risk statement.** Variant 1 is the only variant that names the Q-1 gate failure (ADJ:87: "an unbound terminal cannot read another terminal's Run ... failed on 2026-11-11") as an open risk for the coordinator's own terminal, and marks it UNVERIFIED (diff U-002). It also names the unmeasured combined load (INV-032) and the word-list mismatch. An owner choosing it chooses with the risks in view.
6. **A cheap way to retire the main risk exists.** The observer has a `--run <runId>` option (commands.py:435-436), and V5 already proposes the owner run `superclaude observe --once --run <run>` (writes nothing without `--snapshot`) to compare dispatch ids with the sweep rows (V5:217). The same run would show whether a coordinator terminal sees its own Run. Whether `--run` from the coordinator's terminal avoids the Q-1 failure is UNVERIFIED.
7. **The owner's first-PR scope paired sweep with the report.** The issue summary records the owner's first-PR scope as "read-only `/sc:sweep` plus static report" (issue-summary.md:28) and budgets "`/sc:sweep` with the static report about 20" hours (:6). The report is a named deliverable, not an afterthought. Variant 1 keeps the sweep reply as half of it and supplies the other half.

#### Weaknesses identified in others

1. **Variant 2 answers a narrower question than #339 asked.** It concedes the reply is "counts plus a path, not a #409-style fleet picture" and that "every 3 minutes" is not met (variant-2-original.md, "What it costs or risks"). So for an undated period (its own words: "'Until the note exists' has no date") the issue's report clause is met only in name. A count line and a path do not usefully "replace the usual end-of-message table"; the person still opens a file.
2. **Variant 2's trigger is outside its control.** It ties the revisit to XC-05, which waits on Q5 and other work (variant-2-original.md). Nothing in Variant 2 makes the reopen happen; it relies on someone adding a line to the contract note.
3. **Variant 3 contradicts the scope the owner already set.** The owner's first-PR scope is "read-only `/sc:sweep` plus static report" (issue-summary.md:28). Parking the report clause drops half of that scope. Variant 3 also says the sweep reply is not the #339 report (diff X-002), which leaves the sweep's chat-summary exception (`src/superclaude/output-styles/pragmatic.md:22-23`) with no stated purpose, a cost Variant 3 itself admits.
4. **Variant 3 adds edits while claiming to wait.** It removes the last sentence of section 6.7 and adds a deferral row to #534 (variant-3-original.md). That is more paperwork than Variant 2 and delivers nothing.
5. **Variant 3 conflates "no loop yet" with "no report yet".** A static report can be printed on demand today (both `/sc:sweep` and `observe --once` exist). The missing loop limits the cadence, not the content. Deciding the content now is still useful so that the loop, when built, is built to it.

#### Concessions

1. Variant 1 implies edits that are not scheduled: section 6.7 wording, and later WC-16, the sweep skill's `allowed-tools` and possibly the output style (variant-1-original.md, "What happens next"). Variant 2 implies none. This is real cost.
2. Variant 1 runs against V5's D2 recommendation not to name `observe` in WC-16 or `allowed-tools` before the contract note (V5:222). The analysis behind D2 (two word lists for the same facts, V5:216) is sound, and Variant 1 does not solve it.
3. The Q-1 failure (ADJ:87) is a genuine unknown. If the coordinator's terminal cannot see its own Run through `observe --once`, half of Variant 1 does not work, and the owner would have stated an answer that has to be walked back.
4. Combined load of observer, sweep and watcher was never measured (INV-032; MR:1032 per question.md limits the coordinator to at most one observer instance).
5. Variant 3 is right that no loop exists to print anything every 3 to 5 minutes (question.md fact 10). Variant 1's cadence benefit is future value only.
6. "Now" is the weakest word in Variant 1. The content choice is strong; the timing is not, because the main risk has a cheap check that has not been run.

#### Shared assumptions

- **A-001** (no work item behind it, so a wrong answer is cheap to reverse): QUALIFY. The ledger record is cheap to reverse (MR:538 "none scheduled"), but Variant 1's answer implies later edits to WC-16, the sweep skill and the output style, and those would not be cheap to reverse once made.
- **A-002** (the contract note XC-05 will be written, so "until the note" is a real trigger): ACCEPT. XC-05 is a planned item in wave W1 (MR:540, row Q13 names XC-05 and W1), so the trigger is real, though it has no date.

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (1 = 2 = 3) | 90% | All three use the same five sections; no structural advantage. |
| C-001 | 1 | 55% | Only "both" gives a fleet picture (issue-summary.md:10) while keeping the sweep reply; the Q-1 risk keeps the margin small. |
| C-002 | 2 | 55% | Waiting for the note avoids two word lists in chat (V5:216); "now" is premature while Q-1 is unchecked. |
| C-003 | 2 | 70% | Zero edits; section 6.7 already says it (MR:1040). |
| C-004 | 1 | 65% | Only the observer can reach the 3-minute end; the sweep is capped at 5 minutes (WORKER-CONTRACT.md:109). |
| C-005 | 1 | 80% | #339 asks for a #409-style report of agents, sessions and worktrees (issue-summary.md:10, :26). |
| X-001 | 2 | 55% | Not naming `observe` until the note follows V5:222; Variant 1 defers the naming to the unbuilt loop, so the gap is small. |
| X-002 | 1 | 60% | The owner's first-PR scope pairs the sweep with the static report (issue-summary.md:28), so the sweep reply is part of it, not all of it. |
| X-003 | 2 | 60% | Keeping 6.7 as written is cheapest and already matches the recorded default (MR:538, MR:1040). |
| U-001 | 1 | 75% | `--once` writes nothing without `--snapshot` (commands.py:232-236), so NFR-001 (ADJ:83) holds. |
| U-002 | 1 | 85% | Only Variant 1 surfaces the Q-1 failure (ADJ:87) as a risk; the other two are silent on it. |
| U-003 | 3 | 70% | The loop is unbuilt (question.md fact 10), so no cadence promise can be kept today. |

#### Overall ranking and unassigned pick

Ranking (best first): Variant 1, Variant 2, Variant 3. Variant 1 wins on what the report should contain (C-001, C-004, C-005, X-002, U-001, U-002); Variant 2 wins on timing and cost (C-002, C-003, X-001, X-003); Variant 3 contributes U-003 but drops half of the owner's stated first-PR scope.

Unassigned pick: honestly, Variant 2, with one addition from Variant 1. Record "sweep summary only until the contract note", and add the V5:217 check (`superclaude observe --once --run <run>` from the coordinator's terminal) to the contract note's work, so that Q-1 is answered before `observe --once` text joins the chat report. That keeps zero edits now and makes Variant 1's content the planned destination rather than an open question.

---

### Round 1 advocate statement: Variant 2 (sweep summary only, until the contract note exists)

Advocate: Variant 2. Persona: architect (structure, dependencies, long-term impact). Depth: quick, Round 1 only.

#### Position summary

Variant 2 is the only answer that matches what is already built, contracted and written into the spec, so it costs zero edits and adds no new dependency between the sweep and the observer before their contract note exists. It keeps one source of facts in chat while the two programs still disagree on words, and it names the exact trigger (the XC-05 note) at which the observer question is reopened.

#### Steelman

**Variant 1 (both reports, now), strongest form.** #339 literally asks for a static report "taking inspiration" from #409 (variant-5-original.md:221), and #409 is the observer, which is already built and merged (ADJ glossary line 77: "Built and merged: release 1 in PR #503, release 2 in PR #514"). `observe --once` is the only no-write static status (debate-transcript.md:904, X-004), so it can run between sweeps without breaking NFR-001's one-report-per-run rule (ADJ line 83), and it is the only way to reach the 3-minute end of "3 to 5 minutes" given the sweep's 5-minute cap (WORKER-CONTRACT.md:109). Variant 1 is the most faithful to the issue text and uses only programs that exist. It is also the only variant that flags the Q-1 risk (ADJ line 87) for the coordinator's own terminal.

**Variant 3 (no recurring report yet; park the clause), strongest form.** Nothing exists to print a report every 3 to 5 minutes: the coordinator loop is unbuilt (question.md fact 10), and WC-16 is "a cap, not a schedule" (ADJ line 81; debate-transcript.md:625 quoting "Phase 1 adds this duty, not a scheduler"). Answering "which report goes in the recurring chat slot" before the slot exists commits to a format early. Variant 3 also lines up with the owner's stated rule for automated output: "Automated status shows only the decision ledger's outstanding owner decisions and held items" (merged-requirements.md:1040, quoting SEED Batch 2 item 8). Parking is the most honest description of the current state.

#### Strengths claimed

1. **Zero edits; the spec already says this.** Section 6.7 reads: "Q11's recommended answer applies to any in-chat report: the sweep summary only, until the note exists" (merged-requirements.md:1040). The Q11 row's recommended answer is the same (merged-requirements.md:538). Variant 2 is the only variant that changes no spec text (diff-analysis C-003, X-003). Variant 1 rewords 6.7; Variant 3 deletes its last sentence.
2. **It matches the shipped skill and output style on this branch.** The sweep skill's "Final reply" is already the one exempt reply: "only the summary counts and the report path are printed" under five conditions (src/superclaude/skills/sc-sweep-protocol/SKILL.md:35-43). The output style carries the same exception (src/superclaude/output-styles/pragmatic.md:22-23). Variant 2 gives that shipped exception its stated purpose; Variant 3 admits it leaves the exception "without a stated purpose in the recurring loop" (variant-3, Costs).
3. **It follows the source debate's recommendation word for word.** V5 D2: "keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet. First step: none in code" (variant-5-original.md:222-223). V5 Q7 repeats it (variant-5-original.md:294). ADJ Part 7 carries the same recommendation (alignment-findings-adjudicated.md:781).
4. **Correct dependency order (architect view).** The contract note (D1, XC-05) is what fixes names, the join key and "one word list (stale, unknown, unavailable, could not determine, historical, frozen, settled ...)" between the two programs (variant-5-original.md:216). Putting both programs' text in one chat report before that note exists couples one reader to two vocabularies. Variant 2 sequences it correctly: note first, then decide whether the observer text joins, and it puts that decision inside the note itself (variant-2, "What happens next", last bullet).
5. **Keeps the observer out of the coordinator's rules while its binding is unproven.** Q-1 failed: "an unbound terminal cannot read another terminal's Run" (ADJ line 87), and whether `observe --once` in the coordinator's own terminal shows its own Run is UNVERIFIED (question.md fact 7). Variant 2 never names `observe` in WC-16 or the skill's tool list, so a negative result on that check costs nothing.
6. **No unmeasured load.** Combined load of observers plus sweep plus watcher was never measured (INV-032; merged-requirements.md:1032 as cited in question.md fact 8, not re-read here). Variant 2 adds no Orca calls per cycle; Variant 1 adds some.
7. **Cheapest to reverse, with an explicit reopen trigger.** If the owner later wants the observer text, adding it after the note is additive. Variant 2 states the trigger (the XC-05 note carries the line); Variant 3's trigger needs two unbuilt things (loop and note), which is a later and less defined reopen point.

#### Weaknesses identified in others

1. **Variant 1 creates edits and couplings nobody scheduled.** By its own account it requires later edits to WC-16, the sweep skill's tool list and the output style (variant-1, "What happens next"), and an observe block "either keeps ordinary formatting or needs its own exception". The current exception is defined only for the sweep skill (pragmatic.md:22-23), so Variant 1 opens a second style exception with no design behind it.
2. **Variant 1 mixes two vocabularies in one report.** It concedes "two programs printing overlapping facts with different words (stale, unknown, historical) before the contract note fixes one word list ... can confuse the reader" (variant-1, Costs; variant-5-original.md:216). That is the exact failure the note exists to prevent.
3. **Variant 1's 3-minute benefit has no runner.** It says the observer "can fill the 3-minute end of 3 to 5 minutes", but the coordinator loop is unbuilt (question.md fact 10). The benefit is real only after a loop exists.
4. **Variant 1 rests on an unverified binding.** Its second half depends on `observe --once` seeing the coordinator's own Run, which is UNVERIFIED after Q-1 failed (ADJ line 87). Variant 1 lists this as a risk but answers "now" regardless.
5. **Variant 3 edits the spec to remove a sentence for no gain.** Graph edge 101 already records Q11 as "Recorded only; they gate no item" (merged-requirements.md:748). Deleting 6.7's last sentence is a spec change with no benefit, since 6.7's first sentence already limits automated status.
6. **Variant 3 does not actually answer the question.** The question asks which report it is (sweep, observe or both); "neither, for now" leaves "Which report ... the clause will mean when it is unparked" unresolved (variant-3, Unresolved). The owner gets no guidance for the first time a coordinator does print a sweep reply in chat.
7. **Variant 3 adds tracking overhead.** It adds a deferral row in #534 and admits "One more deferred item to track" (variant-3, Costs).

#### Concessions

1. Variant 2 is narrower than #339's wording. Counts plus a path is not a #409-style fleet picture; the person must open the report file (variant-2, Costs). Variant 1 wins on fidelity to the issue text (C-005).
2. The "every 3 minutes" end is not met; the 5-minute cap is a cap, not a schedule (WORKER-CONTRACT.md:109; ADJ line 81). Variant 2 does not fix this.
3. "Until the note exists" has no date; the note waits on other work (variant-2, Costs).
4. Variant 3 is right that no loop exists to print anything recurring (U-003), and its framing fits the owner's "decision ledger only" rule for automated status (merged-requirements.md:1040) more cleanly. A counts-and-path reply after every sweep can read as routine status. Variant 2 depends on the sweep reply being the accepted WC-16 output, not routine chatter; V5 D2 supports that reading (variant-5-original.md:222), but the owner has not stated it.
5. Variant 1's U-002 (flagging Q-1 for the coordinator's own terminal) is a useful risk callout that Variant 2 does not make in its own text.

#### Shared assumptions

- **A-001 (no work item, so a wrong answer is cheap to reverse): QUALIFY.** True for Variant 2 (zero edits) and mostly for Variant 3, but Variant 1 implies later edits to WC-16, the skill and the output style, so its reversal cost is not small.
- **A-002 (the contract note will be written, so "until the note" is a real trigger): QUALIFY.** V5 D1 makes the note the "smallest reversible first step" (variant-5-original.md:217), so it is likely, but it is undated; the ledger row should also name a fallback review point (for example when the coordinator loop is built).

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | Tie (2 nominal) | 35% | All three use the same five sections; no structural advantage. |
| C-001 | 2 | 70% | One source of facts in chat until the shared word list exists; matches V5 D2 and spec 6.7. |
| C-002 | 2 | 70% | Reopens on one defined trigger (the note), earlier and clearer than Variant 3's two-condition park. |
| C-003 | 2 | 85% | Only variant with zero spec, contract, skill or style edits (merged-requirements.md:1040 already says it). |
| C-004 | 3 | 60% | Variant 3 is most accurate that nothing runs a cadence; Variant 2 is honest about the cap but still implies a slot. |
| C-005 | 1 | 80% | Dashboard-like text is closest to "taking inspiration from #409". |
| X-001 | 2 | 80% | Keep `observe` out of WC-16 and the skill until the note and the Q-1 binding are settled (variant-5-original.md:222). |
| X-002 | 2 | 65% | The sweep reply is already the contracted WC-16 output with a shipped exception (SKILL.md:35-43). |
| X-003 | 2 | 80% | Keeping 6.7 as written avoids a spec edit with no gain. |
| U-001 | 1 | 70% | Correct and useful fact (no-write observer, X-004 at debate-transcript.md:904); it informs the note's later decision. |
| U-002 | 1 | 85% | The Q-1 risk for the coordinator's own terminal is the highest-value unique point and is UNVERIFIED. |
| U-003 | 3 | 80% | The unbuilt loop is a real constraint the other two underplay. |

#### Overall ranking and unassigned pick

Ranking, best first: Variant 2, Variant 3, Variant 1.

Unassigned pick: I would still pick Variant 2, because it costs nothing, matches the spec, the shipped skill and V5 D2, and keeps the observer decision behind the contract note where its dependencies belong. It is close to Variant 3; the best merged answer is Variant 2's ruling plus Variant 3's caveat that no 3-to-5-minute cadence is promised until the coordinator loop exists, plus Variant 1's Q-1 check listed as a precondition for ever adding the observer text.

---

### Round 1 advocate statement: Variant 3 (no recurring chat report yet; park the clause)

Advocate persona: qa (edge cases, failure scenarios). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`.

#### Position summary

Variant 3 is the only answer that promises nothing the system cannot deliver today: there is no coordinator loop to print anything every 3 to 5 minutes, and the only text allowed to skip the DONE / NEXT table is the reply of an actual, person-assigned `/sc:sweep` run. Parking the clause keeps the coordinator's automated output equal to the decision ledger (section 6.7's first sentence) and defers the "which report" choice to the moment the loop and the contract note make it testable.

#### Steelman

**Variant 1 (both reports, now).** Its strongest case: #339 literally asks for a static report "taking inspiration" from #409 (variant-5-original.md:221), the observer that renders #409's view is built and merged (ADJ glossary line 77), and `observe --once` writes no file, so it is the only status text that can run between sweeps without breaking NFR-001 (debate-transcript.md:904, X-004: "the only no-write static status is `observe --once`"). It is also the only variant that addresses the 3-minute end of "3 to 5 minutes", which the sweep's 5-minute cap (WORKER-CONTRACT.md:109) cannot reach. And it has the strongest support from the owner's own earlier choice: the seed brief records that "the first PR delivers only a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:17). Variant 1 is also honest about its risks (Q-1 UNVERIFIED, word-list clash, unmeasured load).

**Variant 2 (sweep summary only, until the contract note).** Its strongest case: it is the spec's recommended answer and its default (merged-requirements.md:538), it is already written into section 6.7 (merged-requirements.md:1040), and it matches V5's D2 advice word for word ("keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet", variant-5-original.md:222). It needs zero edits anywhere, keeps one source of truth in chat while the two programs use different word lists, and the sweep reply is already the only exempt reply in the output style (pragmatic.md:22-23; sc-sweep-protocol/SKILL.md:31-43). It is the cheapest correct-looking answer.

#### Strengths claimed

1. **It does not promise a cadence that nothing runs.** WC-16 is "a cap, not a schedule" (ADJ glossary line 81) and the transcript records "Phase 1 adds this duty, not a scheduler" (debate-transcript.md:625). WORKER-CONTRACT.md:109 says the sweep runs "after every wake or timeout, at most once every 5 minutes". The question itself states "The coordinator loop that would print a recurring report is unbuilt" (question.md fact 10). Variants 1 and 2 both answer "what goes in the recurring report" when there is no recurring report; Variant 3 is the only one that says so in its answer (variant-3-original.md:15).

2. **It matches the exact scope of the one exempt reply.** The sweep exception applies only when "the session is executing the loaded `sc-sweep-protocol` skill for an actual `/sc:sweep` invocation" and only to "the final successful reply of that skill" (pragmatic.md:23; SKILL.md:38, :43). It also says "There is no general exemption for coordinators, for other skills or for file output" (pragmatic.md:25). Variant 3's wording, "the sweep reply appears only when someone actually runs `/sc:sweep`" (variant-3-original.md:5), is a direct restatement of that rule. Calling that reply "the every-3-to-5-minute static report" (Variant 2) stretches a per-invocation reply into a periodic one the style does not describe.

3. **It keeps automated status equal to the owner's stated preference.** Section 6.7's first sentence limits automated status to "the decision ledger's outstanding owner decisions and held items with their reasons" (merged-requirements.md:1040, quoting SEED Batch 2 item 8). The last sentence of the same paragraph then allows an in-chat sweep summary. Variant 3 removes that internal tension; Variant 2 keeps it; Variant 1 widens it.

4. **It avoids naming a format before the word list exists.** The contract note must fix "one word list (stale, unknown, unavailable, could not determine, historical, frozen, settled, ...)" (variant-5-original.md:216). Choosing either report as the periodic chat report before that note binds the chat to one program's vocabulary. Variant 3 defers the choice until both inputs to it exist.

5. **Failure-scenario coverage is strongest.** QA view of each answer when the loop is later built:
   - Variant 1: the coordinator runs `observe --once` from its own terminal; Q-1 already failed for an unbound terminal (ADJ glossary line 87) and the coordinator-terminal case is UNVERIFIED (question.md fact 7). The chat could show an empty or wrong Run every cycle. Load with observer plus sweep plus watcher was never measured (INV-032, merged-requirements.md:502, as cited by question.md fact 8; not re-read here).
   - Variant 2: "until the note exists" has no date (variant-2-original.md:24), so the interim becomes the permanent answer by default, while the recorded answer claims a 3-to-5-minute report that the cap cannot meet at 3 minutes (variant-2-original.md:23).
   - Variant 3: no new failure path. Nothing new runs; the only risk is unmet scope, which is visible and tracked.

6. **It is cheap to reverse, and reversal is explicit.** No code, contract or skill edit (variant-3-original.md:11). The clause is tracked as a deferred row (variant-3-original.md:9), so it cannot silently drop out, which is the failure mode of Variant 2's undated trigger.

#### Weaknesses identified in others

1. **Variant 1 needs edits nobody has scheduled and one the style forbids by default.** It requires WC-16 and the skill's tool list to name `observe` (variant-1-original.md:11), which is the exact step V5 D2 says not to take yet (variant-5-original.md:222). Its observe block cannot use the sweep exception, since the exception covers only the sweep skill's final reply (pragmatic.md:25 "There is no general exemption for coordinators, for other skills"). So the "static report replacing the end-of-message table" (#339's intent, .dev/issues/339/issue-summary.md) would still carry a DONE / NEXT table for half its content, or need a new style exception to an output style whose current exception already runs to five conditions.

2. **Variant 1 rests on an unverified binding.** Its whole 3-minute advantage depends on `observe --once` showing the coordinator's own Run. Q-1 failed for the unbound case (ADJ line 87) and Variant 1 itself marks the coordinator case UNVERIFIED (variant-1-original.md:21). Recording "both, now" as an owner decision on an unverified premise is the riskiest of the three.

3. **Variant 1 shows two vocabularies side by side.** Before the contract note, "stale", "unknown" and "historical" can mean different things in the two outputs (variant-5-original.md:216; variant-1-original.md:22). A person reading both in one chat block cannot tell which wins.

4. **Variant 2 labels an on-demand reply as a periodic report.** The sweep reply is "counts and report path only" (question.md fact 2), produced only on an actual `/sc:sweep` invocation by an assigned coordinator (pragmatic.md:23). Nothing invokes it periodically today. Recording it as "the static report every 3 to 5 minutes" records a capability the system lacks, and Variant 2 concedes the 3-minute end is not met (variant-2-original.md:23).

5. **Variant 2's trigger may never fire.** "Until the note exists" waits on XC-05 and Q5 (variant-2-original.md:24); the note is unbuilt (question.md fact 6). An undated interim answer recorded in the decision ledger tends to become the final answer without a second owner look.

6. **Variant 2 is a narrow reading of #339.** Counts plus a path is "narrower than #339's 'taking inspiration from #409' wording" (variant-2-original.md:22). It satisfies neither the letter (#409-style picture) nor the cadence, yet records itself as the answer.

#### Concessions

1. **Variant 3 conflicts with a recorded owner scope choice.** The seed brief says the owner chose on 2026-11-07 that the first PR delivers "a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (seed-brief.md:17). Parking the clause defers something the owner put in scope. My best answer is that the first-PR static report may be the sweep's report file rather than an in-chat periodic block, but whether the owner meant the chat block is UNVERIFIED, and this is the strongest argument against Variant 3.
2. **#339's explicit ask is met in no form for now** (variant-3-original.md:21). The person must run a command or open a file to see the fleet.
3. **It edits spec text that already applies the recommended answer.** Dropping section 6.7's last sentence (variant-3-original.md:10) is a change, where Variant 2 needs none.
4. **It adds a deferred item to track** and leaves the sweep exception without a stated role in a loop (variant-3-original.md:22-23).
5. **It contradicts the spec's recommendation and default** (merged-requirements.md:538) and V5 D2, both of which keep the sweep reply as the WC-16 output.

#### Shared assumptions

- **A-001 (no work item, so a wrong answer is cheap to reverse): QUALIFY.** True for code (merged-requirements.md:538, :748 "Recorded only"), but the answer is copied into section 6.7 and the decision ledger, and a recorded owner answer is read as binding by later work, so reversal still costs an owner touch.
- **A-002 (the contract note XC-05 will eventually be written): QUALIFY.** V5 recommends it as the first step (variant-5-original.md:215-217), but it is unbuilt and undated; Variant 3 hedges this by also requiring the loop and by tracking the clause as a deferred row rather than relying on the note alone.

#### Per-point verdicts

| Point | Winner | Confidence | One-line reason |
|---|---|---|---|
| S-001 | Tie (nominal 3) | 50% | All three use the same five sections; no structural edge. |
| C-001 | 3 | 60% | Only Variant 3 matches what exists: no loop, and the sweep reply is per-invocation only (pragmatic.md:23, :25). |
| C-002 | 3 | 60% | Waiting for both the loop and the note avoids an undated interim (V2) and a premature commitment (V1). |
| C-003 | 2 | 75% | Variant 2 needs no edit at all; Variant 3 drops one sentence; Variant 1 needs contract, skill and style edits. |
| C-004 | 3 | 65% | WC-16 is a cap, not a schedule (ADJ line 81; debate-transcript.md:625); not promising a cadence is the honest treatment. |
| C-005 | 1 | 85% | Variant 1 is closest to "taking inspiration from #409" and to the seed-brief scope (seed-brief.md:17). |
| X-001 | 2 | 70% | Variants 2 and 3 agree; Variant 2 states it as a positive rule matching V5 D2 word for word (variant-5-original.md:222). |
| X-002 | 3 | 65% | The sweep reply is exempt only for an actual `/sc:sweep` run (SKILL.md:38, :43), so it is an on-demand reply, not a periodic report. |
| X-003 | 3 | 55% | Removing the last sentence resolves the tension with 6.7's own first sentence (merged-requirements.md:1040). |
| U-001 | 1 | 80% | Correct and useful: `observe --once` is the only no-write static status (debate-transcript.md:904). |
| U-002 | 1 | 85% | Flagging Q-1 as UNVERIFIED (ADJ line 87) is the key risk fact any later choice must test. |
| U-003 | 3 | 75% | The unbuilt loop (question.md fact 10) is the fact the other two answers skip. |

#### Overall ranking and unassigned pick

Ranking (best first): Variant 3, Variant 2, Variant 1.

Variant 3 ranks first on failure-scenario grounds: it is the only answer that records no capability the system lacks. Variant 2 is close behind because it costs nothing and matches the spec, V5 D2 and section 6.7 as written; its flaw is labelling an on-demand reply as a periodic report under an undated trigger. Variant 1 ranks last because it depends on an UNVERIFIED binding (Q-1), needs unscheduled edits including a new style exception, and mixes two vocabularies.

Unassigned pick: honestly, Variant 2. It is the spec's recommendation and default, requires no edit, and the gap between it and Variant 3 is mostly labelling, since neither causes anything to run periodically today. The seed-brief owner choice (seed-brief.md:17) also weighs against parking the clause outright. I would pick Variant 2 with one amendment taken from Variant 3: record in the ledger that no loop exists yet, so the "every 3 to 5 minutes" cadence is not claimed as met.
