# Round 3 Final Arguments: Variant 2 (opus:analyzer, B Attention Ledger)

## Final Position

**INV-019 is right, and I accept Variant 1's fix: the visual direction goes back on the owner list as item 1, and a gate DIRECTION-SELECTED blocks production integration until a human has recorded a selection** (`debate-r3-variant-1.md` lines 24-34). The debate produced a recommendation, not a decision. The issue assigns this decision to a human (`../seed-brief.md` line 69: "the issue requires a human selection before production integration"). Two or three advocates agreeing does not meet that criterion.

The root cause matters more than this one omission. S-008 asked "which choices can engineering not settle from evidence?" (`convergence-r2.md` line 22, line 133). That filter looks only at what advocates can settle. It ignores what the issue assigns to a human. Visual direction fails that filter because the advocates agreed on it. It is still an owner decision because the issue says so. The same filter quietly dropped two more items that were on my own owner list: the production stack (`variant-2-opus-analyzer.md` line 194, decision 2) and the fallback deadline (line 204, decision 12). So the fix has to change the rule, not just add one row. An item belongs on the owner list if any of these holds:
1. only a human can make it (sample-capture permission, message-content exposure);
2. the issue assigns it to a human (visual direction);
3. the recommendation departs from a preference the issue states. The issue prefers Go with Bubble Tea v2 (`../seed-brief.md` line 43), and the consensus recommends Python Rich (`convergence-r2.md` line 118), so the stack needs owner confirmation. Whether the issue requires a human sign-off on the stack is UNVERIFIED. Overriding a stated preference without asking repeats the INV-019 failure either way.

The recommendation I now put to the owner is the one stated in `debate-r3-variant-1.md` line 9. My own contribution was the B half. Default while no question row can be interpreted: A's worker ledger with the `COUNTS (source-reported)` strip and B's one-line gap notice. From the first release whose QUESTION-OBSERVATION gate passes: B's attention ledger as the default, with A one key away. Later, behind QUESTION-LINK: C's decision desk. V3's dissent on the post-link default is recorded. The owner may pick this sequence, a single direction, or something else.

**INV-020 (HIGH, ADDRESSED) stays behind the R2 gate.** `check --all --run <runId> --json` is a candidate verb, not a settled one. `convergence-r2.md` line 96 states it as settled and should be reworded, as V1 says (`debate-r3-variant-1.md` line 14). I accept V1's three gate checks: whether `--run` narrows `--all`, which handle receives human-addressed messages, and the measured message rate. I add one correction to my own Round 2 argument. I called "rotation period times message rate under 100 rows" the "real bound" (`debate-r2-variant-2.md` line 27). V3 is right that an average rate is not a completeness proof, because bursts break it (`debate-r2-variant-3.md` line 23). So a passed gate admits the verb, but it never upgrades the label. The question area keeps `bounded best effort: bursts over 100 rows between reads of a Run may be lost`, and it never claims complete coverage. All three checks are UNVERIFIED today.

I dispute none of the 14 MEDIUM invariants. I accept fixes for 13 of them. INV-007 is a disclosed accepted risk, with one partial mitigation. On three rows (INV-003, INV-007, INV-022) I refine V1's fix rather than take it word for word.

## Response to INV-019

**How it happened (evidence chain).**
- All three variants had visual direction as owner decision 1: `variant-2-opus-analyzer.md` line 193 ("Visual direction (required by the issue before production integration)"), plus V1 line 207 and V3 line 127 as cited in `invariant-probe.md` line 25.
- In Round 2 I signed off on S-008 as "Only true owner choices (C), plus B's sample-capture permission and A's message-content exposure decision" (`debate-r2-variant-2.md` line 121). Visual direction, stack and fallback deadline are not in it. I did not flag the drop.
- The convergence list repeats that omission (`convergence-r2.md` line 132). The only human step left for C-001 is an "owner walkthrough" used as a tie-breaker for V3's dissent (line 77), not a recorded selection.
- Result: every engineering gate can pass and production integration can happen with no human choice on record. That fails an issue acceptance criterion at review. HIGH is the right severity.

**Fix: accept V1's DIRECTION-SELECTED gate (`debate-r3-variant-1.md` lines 26-31), with three amendments.**

1. **The owner chooses from honest renders, not only best-case ones.** V1's input to the owner is R0 recorded-console renders of A, B and C at 160, 116 and 80 columns from the redacted golden fixture, each marked "synthetic fixture, not live evidence" (line 28). That is necessary but not enough. A synthetic B ledger is full of questions that no live source can supply today, and a synthetic C desk has links that nothing verifies. An owner who picks from those renders is picking the best case. So each direction is also rendered in the state it will really ship in:
   - A and B at R1: the gap notice `Question rows: source contract UNVERIFIED. 0 rows interpreted. This is not "no questions".` (`debate-r2-variant-2.md` line 11);
   - B at R2: the header `read k of N Runs since start; oldest among Runs read`, the `bounded best effort` label, and `affected scope unknown`;
   - C before QUESTION-LINK: a desk whose affected scope reads `affected scope unknown`.

   V3's comparison task is part of the walkthrough: find the oldest observed question and inspect its evidence, at all three widths (`debate-r2-variant-3.md` line 156). This is where V3 is stronger than me. It makes the choice about the human's task, not about how the screen looks.
2. **The selection record has three parts.** A dated owner statement, written by the owner and never by an agent (V1 line 27), naming:
   - (a) the default view while no question row can be interpreted;
   - (b) the default view after QUESTION-OBSERVATION passes;
   - (c) a fallback date. If QUESTION-OBSERVATION has not passed by that date, the owner re-confirms (b). This restores my decision 12 (`variant-2-opus-analyzer.md` line 204). It covers the risk I named myself: "B's headline panel stays empty, and the product becomes a relabelled A" (line 212).

   The stack confirmation (Python Rich against the issue's Go preference) and the command name (already an owner item under C-019, `convergence-r2.md` line 44, but missing from the line 132 list) go in the same record, so the owner makes one visit.
3. **One more re-confirm trigger.** V1's "Stale" rule asks for re-confirmation when a later gate changes what a direction can show (line 30). Add: the fallback date passes with QUESTION-OBSERVATION still open. The default the owner picked for (b) has then not arrived. Carrying the selection forward in silence would be the INV-019 failure again, one level down.

**Production integration.** I accept V1's interpretation as a proposal for the owner to confirm: the first change that registers the command in the shipped CLI, or that runs a live Orca subprocess outside the fake runner (V1 line 32). Whether this matches the issue's intent is UNVERIFIED. One consequence should be stated plainly: R1 (live `worker-list`) cannot start before the selection. That is cheap, because the renders the owner needs come from R0, and the S-010 seams keep the adapter, model, retention and sanitizer independent of the direction (V1 line 11).

**AC addition.** I accept V1's item "owner visual-direction selection recorded (date, option, who)" (line 33), checked by a reviewer at the release gate. It is never an automated test, and it is never reported as a test pass.

## Response to MEDIUM Invariants

This covers the 14 UNADDRESSED MEDIUM rows of `invariant-probe.md` (lines 8-29), one line each. "V1 fix" means `debate-r3-variant-1.md` lines 40-58.

- **INV-002, fix proposed (accept V1 fix).** My T22 ("an older `observedAt` never overwrites a newer one", `variant-2-opus-analyzer.md` line 184) is the rule that causes the silent drop. Fix: a backward timestamp, or a changed `liveness.source` or `resource.recoveryAttemptCount`, renders `conflict (time went back)` with both readings kept in detail. Only a strictly newer value on the same clock and source replaces silently.
- **INV-003, fix proposed (V1 fix, refined).** The required set is `result`, `result.workers` (array) and `result.page.hasMore`. A failure there marks the cycle `FAILED (shape)` and keeps the last-good ledger. I drop my own requirement on `result.scope` (`variant-2-opus-analyzer.md` line 162): a missing scope renders `scope unknown`, and the strip must then not read as fleet-wide. I also make `page.total` optional, against V1 line 41: a missing denominator renders `reported unknown`. Losing the whole verified ledger over one missing count contradicts "absent optional facts remain unknown". Each optional field gets a drop test, and no dropped field ever renders `0`.
- **INV-004, fix proposed (accept V1 fix).** Flags must match the release template exactly. The forbidden set also matches by prefix. `runId` and `nextCursor` get format checks, and a value is bound to its flag as `--opt=value` only if Orca accepts that form (UNVERIFIED, to be checked by one recorded call per flag). A value that starts with `-` is otherwise rejected. A fake runner that fails if it is reached proves zero subprocess calls for hostile values. This is the most important MEDIUM row.
- **INV-005, fix proposed (accept V1 fix).** It matches my `PARTIAL (total changed during read)` (`variant-2-opus-analyzer.md` line 164). Add `reported T1-T2 (changed during read)`, `collected n / reported T (mismatch)` when `hasMore=false` but n differs from T, and `PARTIAL (empty page k)`.
- **INV-007, accepted risk with reason, plus a partial mitigation.** No active-first filter is verified in today's help (`convergence-r2.md` line 95), so the recency bias stays, made visible rather than solved. The PARTIAL line `oldest rows not read; long-running active workers may be among them` goes on the strip at every width, not only in detail, because this is #409's own failure appearing in the worker ledger. Mitigation, reusing C-009's "not reobserved" rule (`convergence-r2.md` line 115): an active row seen earlier in this session that falls beyond the page cap stays listed as `last seen HH:MM, beyond page cap, not reobserved`, never as current. This does not help rows never seen since start-up, which is the residual risk. Add an UNVERIFIED item: does `worker-list` offer a state filter?
- **INV-009, fix proposed (accept V1 fix).** The rotation set is the Runs with a non-historical row plus the Runs holding a retained open question. Historical-only Runs are left out with a disclosed count. An empty set reads `message source not read this cycle (no Run in rotation)`. Add a measured `revisit ~Ns (k Runs)` token, so the growth in revisit time the probe names is visible.
- **INV-013, fix proposed (accept V1 fix).** The strip is present at every width of 80 columns or more. Tests run at 80, 81, 115, 116, 117, 143, 144, 159, 160 and 200, which includes the built 144 branch. Under 80 columns the screen shows `terminal too narrow (min 80)` and still prints the denominators.
- **INV-014, fix proposed (accept V1 fix).** Priority tokens (`collected n / reported T`, `PARTIAL`, scope) are never truncated. The strip wraps before it cuts anything, `>` applies only to low-priority tokens, and the strip is a minimum row in the 44-row height contract.
- **INV-015, fix proposed (accept V1 fix).** My T23 (`cell_len <= W` on "every exported line", `variant-2-opus-analyzer.md` line 185) is half the cause. The fix is one view model with two renderers: a width-bound screen render (T23 applies only there) and a record-form `export(view)` with full IDs, which has its own test that every fixture ID appears whole.
- **INV-016, fix proposed (accept V1 fix).** My variant already had it: T26 tests `NO_COLOR=1` and `NO_COLOR=yes`, and the harness ran `color_system=None or "standard"` (`variant-2-opus-analyzer.md` lines 173, 185). The consensus narrowed it to `None` (`convergence-r2.md` line 128). Restore a colour-enabled run that asserts no colour segments under NO_COLOR, and that the plain text of the coloured render equals the NO_COLOR render.
- **INV-017, fix proposed (accept V1 fix).** The adapter drops the bodies of terminals that are not opted in at parse time. They are never in the model and never in `--once` export; only ID, type and time are kept. If rows carry no terminal field (UNVERIFIED), the opt-in becomes per Run and the prompt says so. This does not weaken question detection, because the type must come from a verified field, never from body text (`variant-2-opus-analyzer.md` line 198).
- **INV-021, fix proposed (accept V1 fix).** My R2 line "the fallback rule (U-009), now read in both directions" (`debate-r2-variant-2.md` line 106) was a release-time rule only. Add: the default view is chosen at start-up from the runtime state of the question source, and it never switches automatically mid-session. The B header reads `read k of N Runs since start; oldest among Runs read` until the first full rotation. A runtime failure titles the ledger `question source FAILED` or `STALE` and keeps the retained rows.
- **INV-022, fix proposed (V1 fix, refined).** Take before and after readings of `check --peek` unread IDs (verified non-consuming) and of `worker-list` lease, liveness and `observedAt` around one call of the verb under test. Refinement: a coordinator acking or a worker heartbeating between the two readings would cause a false failure, or hide a real one. So the sample is taken on a quiet scope, repeated at least twice, and any difference not explained by new IDs is investigated, never averaged away. Help text alone never passes.
- **INV-023, fix proposed (accept V1 fix).** The cycle budget equals the interval (15 s). The per-call timeout times the calls in a cycle must fit inside it, or fewer pages are read and PARTIAL is shown. STALE comes after 3 intervals with no successful `worker-list`, on a monotonic clock. That is my original "3 missed intervals" rule (`variant-2-opus-analyzer.md` line 165), which the consensus dropped. My 30 s deadline over a 15 s interval (line 161) is withdrawn. The budget makes the INV-006 coupling explicit: the pages per cycle follow from the measured timeout.

## Remaining Disagreements

No point remains for the advocates to settle by argument. Each row below goes to the owner, to a measurement, or is a small wording difference from V1's Round 3 text.

| Point ID | Final position | Evidence |
|---|---|---|
| S-008 (owner-list rule) | The rule should be "human-only, OR assigned to a human by the issue, OR departing from a stated issue preference", not just "engineering cannot settle it". Visual direction is item 1. Stack confirmation and command name join it in the DIRECTION-SELECTED record. | `convergence-r2.md` line 133 (engineering-obligation filter); line 132 (list without direction, stack or name); `../seed-brief.md` line 43 ("Issue prefers Go with Bubble Tea v2"), line 69; `convergence-r2.md` line 44 (C-019 "final name from owner") |
| C-001 (post-link default, B vs C) | Recommend B as the default after QUESTION-OBSERVATION, with C as a later view. The owner decides, using V3's task-based walkthrough. Steelman of V3: once links verify, one screen for discovery plus inspection may beat a ledger plus a detail. That depends on explicit `dispatchId` links in real rows, which is UNVERIFIED. | `debate-r2-variant-2.md` line 178; `debate-r2-variant-3.md` line 156 ("link availability alone establishes feasibility, not preferred workflow") |
| DIRECTION-SELECTED inputs | Renders must include each direction's shipped, degraded state (gap notice, `read k of N Runs`, `affected scope unknown`), not only synthetic best cases. The record also carries a fallback date. | `debate-r3-variant-1.md` line 28 (synthetic renders only); `variant-2-opus-analyzer.md` lines 204, 212 |
| INV-020 / C-002 coverage label | A passed QUESTION-OBSERVATION admits the verb but never yields "complete". The label stays `bounded best effort`. I withdraw "rate is the real bound". | `debate-r2-variant-2.md` line 27; `debate-r2-variant-3.md` line 23 ("not a completeness proof: bursts ... can still lose unseen rows") |
| INV-003 required set | `page.total` is optional (`reported unknown`). V1 makes it required. | `debate-r3-variant-1.md` line 41; `invariant-probe.md` line 9 |
| INV-022 procedure | Before/after readings on a quiet scope, repeated, with unexplained differences investigated. V1's single before/after pair can be confounded by concurrent coordinator activity. | `debate-r3-variant-1.md` line 57 |
| INV-007 mitigation | Keep session-seen active rows beyond the page cap as `not reobserved`, in addition to V1's disclosure. | `debate-r3-variant-1.md` line 49; `convergence-r2.md` line 115 |
| A-008 (label) | QUALIFY. The substance is shared by all three (per-process caps, disclosed, no singleton). Whether to prevent several observers is an owner item. | `debate-r2-variant-2.md` line 185; `convergence-r2.md` line 78 |

## Final Concessions

New in Round 3. My Round 1 and Round 2 concessions stand.

1. **INV-019 and S-008.** My variant listed visual direction, stack and fallback deadline as owner decisions 1, 2 and 12 (`variant-2-opus-analyzer.md` lines 193, 194, 204). In Round 2 I agreed to an owner list without any of them (`debate-r2-variant-2.md` line 121). All three are restored.
2. **C-001 status.** In Round 2 I wrote "B default from the first release whose question-row gate passes" as a design fact (`debate-r2-variant-2.md` line 94). It is now a recommendation to the owner.
3. **Coverage argument.** V3 is stronger: a measured average message rate does not prove completeness (`debate-r2-variant-3.md` line 23). I withdraw "the real bound" (`debate-r2-variant-2.md` line 27).
4. **INV-002.** My T22 rule (`variant-2-opus-analyzer.md` line 184) drops backward-time readings silently. It is replaced by a visible conflict.
5. **INV-003.** I required `result.scope` (`variant-2-opus-analyzer.md` line 162). It becomes an optional fact rendered `scope unknown`.
6. **INV-015.** My T23 applied the width bound to export lines (line 185). It now applies to the screen render only.
7. **INV-021.** "The fallback rule ... in both directions" (`debate-r2-variant-2.md` line 106) covered releases, not runtime. Runtime start-up selection and the `read k of N Runs` header are added.
8. **Where V1 is stronger.** V1's Round 3 file did the harder work first. It has a complete gate definition with missing, stale and contradictory cases, and concrete argv-safety layers. Most of my MEDIUM responses adopt it. My additions are refinements, not alternatives.

## Per-Point Final Positions

| Point ID | Winner variant | Agrees with R2 consensus |
|---|---|---|
| C-001 | V1+V2 sequence as the advocates' recommendation, V3 dissent recorded; the final choice is the owner's under DIRECTION-SELECTED | no (same substance; the advocates did not settle it) |
| A-008 | V1+V2 (QUALIFY); V3 shares the substance | yes |
| S-008 | V1+V2+V3 original owner lists, plus the Round 2 items, under the three-part inclusion rule (V2) | no |
| S-007 | V3+V2 gate table plus DIRECTION-SELECTED (V1), with degraded-state renders and a fallback date (V2) | no |
| C-002 / X-007 | V2+V3, with the verb kept behind QUESTION-OBSERVATION and the label `bounded best effort` (V3) | no (wording of line 96) |
| C-006 / C-011 | V2+V1: cycle budget equals the interval, STALE after 3 intervals on a monotonic clock | no (restores a threshold the consensus dropped) |
| C-007 | V3+V1, plus visible backward-time conflicts | yes |
| C-008 / U-010 | V3+V2, required set `result`, `result.workers`, `page.hasMore`; `page.total` and `scope` optional | yes (fills an open detail) |
| C-010 | V2+V3, `unknown (retention exceeded)` on omitted-ID overflow | yes (closes the open parameter) |
| C-013 | V2+V3, plus changed-total, mismatch and empty-page notation | yes |
| C-017 | V1+V2, with a separate record-form export renderer | no |
| C-021 | V1+V2+V3, plus a colour-enabled NO_COLOR run | no (restores NO_COLOR) |
| A-001 | V1+V2+V3 QUALIFY, with a defined before/after procedure on a quiet, repeated sample | yes (defines the method) |
