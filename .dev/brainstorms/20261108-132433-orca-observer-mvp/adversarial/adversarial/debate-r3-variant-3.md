# Round 3 Final Arguments: Variant 3 (haiku:backend, C Decision Desk)

## Final Position

**I accept V1's DIRECTION-SELECTED gate and V2's owner-list rule, with the changes below. The debate recommends; the human selects.** V1 restores the missing human choice and V2 fixes the filtering rule that lost it (`debate-r3-variant-1.md:5-9`; `debate-r3-variant-2.md:5-10`). INV-019 has a sufficient design remedy in my view, but is not closed in the shared consensus until that remedy is incorporated. No human selection or production permission is claimed here.

My dissent remains: after explicit question-to-evidence links verify, recommend C Decision Desk as the complete decision-focused composition, not automatically a third full screen after A and B. Compare finding an old observed question and inspecting its evidence at all three required widths; links establish feasibility, not the preferred human workflow (`debate-r2-variant-3.md:156`). A wins the immediately useful worker-only preview; B's retained oldest-observed queue belongs in the first live-question release. V1 and V2 instead recommend B as the post-observation default and C later (`debate-r3-variant-1.md:9`; `debate-r3-variant-2.md:12`). Neither recommendation overrides the owner.

**INV-020 changes the agreement, not merely its footnote.** `check --all --run <runId> --json` is a candidate behind QUESTION-OBSERVATION, never a settled Orca contract. Both other advocates now accept that correction (`debate-r3-variant-1.md:14`; `debate-r3-variant-2.md:14`). The baseline verifies handle-scoped non-consuming `--all` and unread-only non-consuming `--peek`, each capped at 100 rows; message-row fields are UNVERIFIED (`../../seed-brief.md:38`). The gate must establish actual target/handle semantics, stable row identity, question type and receiving handle, plus observed latency and burst behavior. A successful targeting sample or low average rate does not establish complete history. Retain `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` after admission. My default remains at most one rotating message-scope read inside the five-child cycle cap (`debate-r2-variant-3.md:157`).

The fixture schema remains PROPOSED, not an Orca API (`../../seed-brief.md:41`). Complete history, cross-host joins, admission/revision-pinned feeds, cost accounting, replay and native deep links remain UNVERIFIED (`../../seed-brief.md:40`). No operational controls, AGPL code copying, live collection or executed test result is introduced by this design argument.

## Response to INV-019

**Accept the finding and the gate.** The issue assigns visual-direction selection to a human before production integration (`../../seed-brief.md:69`). The Round 2 owner list omits it (`convergence-r2.md:132-133`). Agreement about a recommended layout cannot supply the missing human act.

Adopt V1's recorded-selection gate, with success, missing, stale and contradictory cases and a reviewer-checked acceptance item, not a claimed automated test (`debate-r3-variant-1.md:25-34`). My amendments are:

1. **Restore visual direction as owner decision 1.** Record the owner's own dated statement and its location, the default before question observation, the default after observation, and the intended post-link choice or explicit deferral. Agents may accurately reference the owner's statement but may not invent it. Missing selection blocks production integration. An unsupported selection never clears a source gate; use only an explicitly accepted gated fallback, or remain blocked. V1's nearest-gated-view proposal must not become silent permission to substitute a different product (`debate-r3-variant-1.md:27-31`).
2. **Accept V2's owner-list rule without weakening it:** a decision belongs to the owner if only a human can make it, the issue assigns it to a human, or our recommendation departs from a stated issue preference (`debate-r3-variant-2.md:7-10`). Restore stack confirmation, because Rich departs from the issue's Go preference; retain capture permission, acquisition/display/export exposure policy, verified-type classification choices when needed, command naming and any proposed multi-observer restriction. Engineering still verifies contracts, never submits source truth to a vote (`convergence-r2.md:133`; `../../seed-brief.md:70`).
3. **Accept V2's degraded-state walkthrough and fallback date.** Show synthetic best-case and realistically unavailable/partial versions at 160, 116 and 80 columns. State what cannot ship today. A fallback date is a human product-tolerance choice, not an engineering deadline we invent; expiry prompts reconfirmation and never grants automatic permission to change the chosen direction (`debate-r3-variant-2.md:28-40`). Reconfirm a material change outside the owner's recorded fallback. Retain C's task-based discovery-plus-inspection comparison.
4. **Do not silently redefine production integration as every live evidence read.** V1 proposes, and V2 accepts, a boundary that includes any live Orca call outside the fake runner; both label the interpretation UNVERIFIED (`debate-r3-variant-1.md:32`; `debate-r3-variant-2.md:42`). My proposed boundary is first wiring/enabling the observer in the shipped product. Separately authorized read-only contract capture is research, not implicit production integration. The owner must confirm this boundary; pending confirmation use the stricter boundary, offline work only. Neither interpretation is established issue intent.

**Resolution:** INV-019 is resolved as a design defect if the merge includes the restored owner decision, recorded-selection acceptance item and non-bypassable gate. It is not evidence that the gate has passed. This advocate file alone neither edits the shared consensus nor supplies the human choice.

## Response to MEDIUM Invariants

All 16 MEDIUM findings are covered below: 14 marked UNADDRESSED and two already ADDRESSED in the probe. These are proposed design fixes and checks, not claims of implementation or passed tests (`invariant-probe.md:8-31`).

| Invariant | Disposition and final response |
|---|---|
| INV-002, backward component time | **Fix.** Keep bounded prior/current readings and show `time regression` or `source/recovery changed`, rather than silently dropping a later observation. Distinguish a genuine backward timestamp from a changed source with a forward timestamp. Keep independent clocks and idempotent repeated-input behavior. Accept the conflict defense in V1/V2, with these labels (`invariant-probe.md:8`; `debate-r3-variant-1.md:40`; `debate-r3-variant-2.md:50`). |
| INV-003, unspecified required fields | **Fix, prefer V2 over V1.** Required proposed worker envelope: object `result`, array `result.workers`, object `result.page` with boolean `hasMore`; each usable worker requires a valid identity. Invalid identity means an explicitly disclosed rejected row, not a fabricated key. Counts, scope, warnings, projection facts and `page.total` are optional: show `reported unknown` and `scope unknown`, never zero. Required-envelope failure keeps last-good data with failure age. Drop-field and wrong-type cases pin this contract (`invariant-probe.md:9`; `debate-r3-variant-1.md:41`; `debate-r3-variant-2.md:51`). |
| INV-004, option-like external values | **Fix.** Accept exact release-specific argv templates, no shell, structural verb checks and pre-runner rejection of leading-hyphen/control-bearing values. Unknown aliases and flags never reach the runner. V1's numeric string bounds and regexes are PROPOSED, not verified Orca formats; do not infer an opaque cursor grammar from one example. Bound its bytes, validate safe argument binding, and admit `--opt=value` only after recording parser support. Unsafe cursor means PARTIAL; unsafe target means no message call. Test hostile values with zero subprocess calls (`invariant-probe.md:10`; `debate-r3-variant-1.md:42-47`). |
| INV-005, drifting page denominators | **Fix.** Use the last page's reported total with its page number, disclose first/last totals when changed, and mark traversal mismatch or empty-page contradiction PARTIAL. Deduplicate identities; a completed traversal is still not an atomic snapshot, even when totals happen to match. Add all three drift/mismatch/empty-page fixtures (`invariant-probe.md:11`; `debate-r3-variant-1.md:48`). |
| INV-007, old active workers beyond cap | **Accepted risk, with V2 mitigation.** Always disclose `older rows may include active workers; not read` when capped. A bounded cache may retain previously observed active rows, labelled last-seen and not reobserved, never current; cache eviction must be disclosed. This cannot recover never-observed rows. An active-first filter remains UNVERIFIED, not a new allow-listed flag (`invariant-probe.md:13`; `debate-r3-variant-2.md:54`). |
| INV-008, unknown displayed as zero | **Fix already agreed; retain it.** No question-source count before observation verification. Show `unknown (no question source)` or omit the numeric slot, not zero (`invariant-probe.md:14`). |
| INV-009, undefined rotation set | **Fix, with an explicit coverage limit.** After target semantics verify, use permissioned, invocation-verified scopes from the disclosed configured set, discovered non-historical worker scopes and retained-question scopes; deduplicate before fair rotation. Include explicitly configured scopes even if only historical rows are visible. Disclose historical-only exclusions, deferred/never-read scopes, changing membership and measured revisit age. An empty set says `message source not read: no eligible scope; coverage unknown`, not no questions. Global scope enumeration remains UNVERIFIED. This extends V1/V2's discovered-active-plus-retained set without pretending discovery is complete (`invariant-probe.md:15`; `debate-r3-variant-1.md:50`; `debate-r3-variant-2.md:55`). |
| INV-013, untested width ranges | **Fix.** Accept V1's range-based strip rule and tests at 80, 81, 115, 116, 117, 143, 144, 159, 160 and 200. Below 80, render an explicit too-narrow diagnostic with a compact coverage record, not a falsely complete dashboard (`invariant-probe.md:19`; `debate-r3-variant-1.md:51`). |
| INV-014, strip truncation and height | **Fix.** Coverage, scope qualification and PARTIAL are mandatory minimum content, ahead of optional panels. Wrap into multiple rows, do not assume exactly two rows suffice for arbitrary values. If the height cannot hold the minimum, show a compact too-small diagnostic rather than hide uncertainty. Full scope IDs stay available in detail/export (`invariant-probe.md:20`; `debate-r3-variant-1.md:52`). |
| INV-015, full-value export versus width bound | **Fix.** Accept one immutable view model with separate screen and record-form renderers. Display-cell bounds apply to the screen. Export is lossless for permitted sanitized values, including full identifiers; it need not fit screen width. Assert full fixture identities in export, independently of screen truncation (`invariant-probe.md:21`; `debate-r3-variant-1.md:53`; `debate-r3-variant-2.md:58`). |
| INV-016, lost NO_COLOR requirement | **Fix.** Any nonempty NO_COLOR, including `yes`, disables color. Test with color capability enabled, compare plain meaning in colored versus uncolored rendering, and require non-color state labels. A harness forced to no color alone is insufficient (`invariant-probe.md:22`; `debate-r3-variant-1.md:54`; `../../seed-brief.md:51`). |
| INV-017, acquisition versus exposure consent | **Fix, strengthen V1/V2.** Permission must cover the actual read scope before invocation, separately from display/export permission. Parse-time dropping cannot undo receipt into the bounded stdout buffer. Never claim unauthorized bodies were never acquired. If a verified metadata-only/narrow read cannot honor acquisition permission, skip the call. Once acquisition is permitted, discard non-display-authorized bodies before model publication; raw output must not enter logs, fixture files or exports. Terminal-attribution fields and Run scoping are UNVERIFIED, so do not automatically substitute Run-wide consent for terminal consent (`invariant-probe.md:23`; `debate-r3-variant-1.md:55`; `debate-r3-variant-2.md:60`; `../../seed-brief.md:38-39`). |
| INV-021, release gates versus runtime coverage | **Fix.** Accept startup fallback to the worker view if no question read has succeeded, subject to the owner's accepted fallback. Never automatically move the human to another view after startup. Show `read k of N eligible scopes; oldest observed among scopes read`, deferred/failed coverage and retained rows throughout runtime failures. A full first rotation still does not prove complete history; membership changes reopen the incomplete-rotation notice (`invariant-probe.md:27`; `debate-r3-variant-1.md:56`; `debate-r3-variant-2.md:61`). |
| INV-022, undefined side-effect test | **Fix, qualify the proposed procedure.** Use V2's quiet authorized scope and repeated before/after observations, with concurrent acknowledgments/heartbeats controlled or explicitly investigated. Message IDs, inbox shape and lease-specific fields are UNVERIFIED: first establish readable identity/state contracts, then compare unread identity sets and the verified worker/liveness/resource fields around each candidate verb. Help and empty-peek `count` alone cannot clear the gate. Unexplained changes keep the verb unadmitted; passed observations establish only tested visible effects, not absence of hidden audit effects. V1/V2's procedure must not promote unread-row IDs or lease timestamps to verified fields (`invariant-probe.md:28`; `debate-r3-variant-1.md:57`; `debate-r3-variant-2.md:62`; `../../seed-brief.md:37-39`). |
| INV-023, missing deadline and stale threshold | **Fix, accept a measured-budget proposal.** Proposed defaults: 15-second cycle budget, at most five calls, at most one message call, and source STALE after 45 seconds without success on a local monotonic clock. Timeouts plus parsing/kill/reap overhead must fit the budget; otherwise read fewer pages and show PARTIAL. An overrun remains single-flight and visible. Each source has its own success age; worker success never refreshes message freshness. Local elapsed ages use monotonic time; remote evidence timestamps remain wall-clock facts, not magically comparable monotonic instants (`invariant-probe.md:29`; `debate-r3-variant-1.md:58`; `debate-r3-variant-2.md:63`). |
| INV-025, omitted-ID bound overflow | **Fix already agreed; close the notation.** When omitted-identity tracking overflows, render `unknown (retention exceeded)` plus the currently retained count. Test the bound, duplicate reappearance, parser/source failure and restart. Neither eviction nor a new session establishes closure (`invariant-probe.md:31`; `debate-r3-variant-1.md:60`). |

I disagree with none of the MEDIUM findings as defects or disclosed limits. My refinements concern the proposed remedies, especially acquisition permission and unverified observables, not permission to ignore the warnings.

## Remaining Disagreements

| Point ID | V3 position | Other position | Why unresolved |
|---|---|---|---|
| C-001, post-link composition | Recommend C as the complete decision inspection composition, with age-ranked discovery built in; do not mandate three full layouts (`debate-r2-variant-3.md:156`). | V2 retains B default, C later (`debate-r3-variant-2.md:72`). | Human workflow preference is not established by link availability. Owner task walkthrough selects it. |
| C-002 / X-007, message budget | Default to at most one fair rotating message read under the shared five-child cap (`debate-r2-variant-3.md:157`). | A/B leave room for more calls if measurements justify them, as recorded in the prior disagreement (`debate-r2-variant-3.md:157`). | Representative latency/bursts and acceptable worker coverage are UNVERIFIED. Both sides accept bounded best effort, not completeness. |
| S-007, production boundary | Selection gates shipped-product integration; separately authorized evidence research should be distinguishable. Pending owner confirmation, use offline-only work. | V1 includes any live Orca subprocess outside the fake runner; V2 accepts that interpretation (`debate-r3-variant-1.md:32`; `debate-r3-variant-2.md:42`). | The issue's precise boundary is UNVERIFIED. Do not let either interpretation masquerade as issue wording. |
| C-008 / A-003, missing denominator | Align with V2: preserve usable worker data and show `reported unknown`. | V1 makes `page.total` required (`debate-r3-variant-1.md:41`); V2 makes it optional (`debate-r3-variant-2.md:51`). | A missing denominator is a coverage failure, not evidence that all worker identities are unusable. This is a concrete merge choice, not a human preference. |
| C-002 / S-008, exposure scope | Acquisition permission must match the verified read target before the call; display consent alone is insufficient. | A/B discard unauthorized bodies during parsing and propose Run opt-in when terminal attribution is absent (`debate-r3-variant-1.md:55`; `debate-r3-variant-2.md:60`). | Neither Run scope nor terminal-attribution fields are verified. Parse-time filtering cannot prevent prior stdout acquisition. |
| A-001, side-effect observables | Keep message identity and lease-field claims UNVERIFIED until samples establish them; test only named visible effects on a controlled scope. | A/B propose before/after unread IDs and lease/liveness observations, with V2 adding quiet-scope repetition (`debate-r3-variant-1.md:57`; `debate-r3-variant-2.md:62`). | The method is useful, but required observables still need verification and normal heartbeat changes need controls. |
| A-008, fleet-load assumption label | REJECT the premise that a per-process cap proves fleet-wide load; no singleton required (`debate-r2-variant-3.md:160`). | V2 retains QUALIFY and leaves prevention as an owner item (`debate-r3-variant-2.md:78`). | Label disagreement only: caps are per process, disclosed, and any future restriction needs its own decision. |

## Final Concessions

1. **V1 wins immediate delivery, not the final human decision.** Keep A's worker ledger while question contracts remain unverified. Do not fill C's large request/evidence areas with invented content to claim a distinctive live product. My Round 2 conceded this, and I retain it (`debate-r2-variant-3.md:7-11`).
2. **V2 wins early question retention.** Retained oldest-observed discovery can ship before explicit links. My original all-or-nothing link gate delayed useful discovery unnecessarily; observation and linkage remain separate gates (`debate-r2-variant-3.md:11`, `debate-r2-variant-3.md:35-41`). C is the complete inspection recommendation only when its evidence associations are justified.
3. **V1 wins the missing human-selection safeguard; V2 wins the broader owner-list correction.** I do not defend a majority vote replacing the owner. Adopt the recorded human-selection acceptance item and gate, not a retrospective assertion that a walkthrough implied consent (`debate-r3-variant-1.md:25-33`; `debate-r3-variant-2.md:7-10`).
4. **I accept the concrete deadline/freshness repair, as a proposal to measure.** My prior timeout values were unmeasured; merely promising bounded calls was insufficient. Accept a 15-second total budget and proposed three-interval source stale threshold, with reduced coverage when measured calls cannot fit. These are local collection rules, not remote evidence-health claims (`debate-r2-variant-3.md:19`; `debate-r3-variant-2.md:63`).
5. **The shared model does not require one width-bound output format.** Accept separate full-value record export and terminal rendering, plus a color-enabled NO_COLOR test. Neither full identifiers nor monochrome meaning should depend on a narrow recorded screen (`debate-r3-variant-2.md:58-59`).
6. **C does not justify a custom widget framework.** Keep list/detail inspection for the preview and a real key/redraw/resize/restore spike. Switch stacks under the agreed rule if the complete interaction requires too much custom machinery; do not build both first (`debate-r2-variant-3.md:13-15`).
7. **Carry the low-severity repairs too.** Accept restart/new-baseline disclosure, explicit worker-page budget coupling, stable ties, distinct hidden-versus-not-reobserved placeholders, reversible non-ASCII escapes and fresh expected outputs rather than copying prototype mistakes (`debate-r3-variant-1.md:60`). For question ties use verified source-scoped question identity, not a worker `dispatchId` presumed to identify a message. That message identity remains a gate requirement.

## Per-Point Final Positions

All 57 point IDs in `convergence-r2.md:15-71` appear exactly once below. Winner means my final preferred contribution, not human approval or a claim that source gates passed. `yes` accepts the Round 2 winning approach with the concrete invariant repairs above; `no` changes a settled recommendation, adds a missing mandatory gate/decision, or retains dissent. References in each row identify the Round 2 baseline, not evidence that new proposals already existed there. Gate/owner changes follow V1's selection safeguard and V2's corrected owner rule (`debate-r3-variant-2.md:7-10`).

| Point ID | Winner variant | Agrees with R2 consensus (yes/no) |
|---|---|---|
| S-001 | V1 (`convergence-r2.md:15`) | yes |
| S-002 | V2 (`convergence-r2.md:16`) | yes |
| S-003 | V1+V2+V3 (`convergence-r2.md:17`) | yes |
| S-004 | V1+V2 (`convergence-r2.md:18`) | yes |
| S-005 | V1+V2+V3, protect coverage minimum (`convergence-r2.md:19`) | yes |
| S-006 | V2, add human-selection acceptance item (`convergence-r2.md:20`) | yes |
| S-007 | V3+V2 gate table, plus V1 human-selection gate (`convergence-r2.md:21`) | no |
| S-008 | V2 owner rule + V1 selection gate + V3 acquisition distinction (`convergence-r2.md:22`) | no |
| S-009 | V2 (`convergence-r2.md:23`) | yes |
| S-010 | V1+V3, V2 pure-view signature; two renderers (`convergence-r2.md:24`) | yes |
| S-011 | V2 (`convergence-r2.md:25`) | yes |
| C-001 | V1 worker preview; V2 pre-link queue; V3 post-link composition recommended to owner (`convergence-r2.md:26`) | no |
| C-002 | V3 conditional target/one-read budget + V2 retention, never settled Run scoping (`convergence-r2.md:27`) | no |
| C-003 | V2+V3 (`convergence-r2.md:28`) | yes |
| C-004 | V1+V3 (`convergence-r2.md:29`) | yes |
| C-005 | V1+V2+V3, coverage strip across ranges (`convergence-r2.md:30`) | yes |
| C-006 | V1+V2+V3 bounds, plus restored total deadline (`convergence-r2.md:31`) | no |
| C-007 | V3+V1, add visible backward-time/source conflicts (`convergence-r2.md:32`) | yes |
| C-008 | V3+V2, denominator optional (`convergence-r2.md:33`) | yes |
| C-009 | V2+V3 (`convergence-r2.md:34`) | yes |
| C-010 | V2+V3, settle unknown total on omitted-ID overflow (`convergence-r2.md:35`) | yes |
| C-011 | V2+V3, per-source monotonic collection ages (`convergence-r2.md:36`) | yes |
| C-012 | V1+V3 (`convergence-r2.md:37`) | yes |
| C-013 | V2+V3, disclose page drift/mismatch (`convergence-r2.md:38`) | yes |
| C-014 | V2+V3 (`convergence-r2.md:39`) | yes |
| C-015 | V1+V2 (`convergence-r2.md:40`) | yes |
| C-016 | V1 (`convergence-r2.md:41`) | yes |
| C-017 | V1+V2, record export retains permitted values (`convergence-r2.md:42`) | yes |
| C-018 | V1+V3, stack choice subject to owner confirmation (`convergence-r2.md:43`) | yes |
| C-019 | V1, final name from owner (`convergence-r2.md:44`) | yes |
| C-020 | V3+V2 (`convergence-r2.md:45`) | yes |
| C-021 | V1+V2+V3, restore color-enabled NO_COLOR coverage (`convergence-r2.md:46`) | yes |
| C-022 | V1+V3 (`convergence-r2.md:47`) | yes |
| C-023 | V3+V2 (`convergence-r2.md:48`) | yes |
| C-024 | V2+V1 (`convergence-r2.md:49`) | yes |
| C-025 | V3+V2+V1, explicit stable identity tie-breaks (`convergence-r2.md:50`) | yes |
| X-001 | V1 reported layout evidence; no independent render claimed (`convergence-r2.md:51`) | yes |
| X-002 | V2+V3 (`convergence-r2.md:52`) | yes |
| X-003 | V2+V3 (`convergence-r2.md:53`) | yes |
| X-004 | V2+V3, continuation invocation still gated (`convergence-r2.md:54`) | yes |
| X-005 | V3, worker identity only, not invented message identity (`convergence-r2.md:55`) | yes |
| X-006 | V2+V3 (`convergence-r2.md:56`) | yes |
| X-007 | V3 one-message-call proposal under common cap (`convergence-r2.md:57`) | no |
| X-008 | V2+V3 (`convergence-r2.md:58`) | yes |
| X-009 | V3+V2 (`convergence-r2.md:59`) | yes |
| X-010 | V1 (`convergence-r2.md:60`) | yes |
| X-011 | V1 (`convergence-r2.md:61`) | yes |
| X-012 | V1+V2 observation-before-link sequencing (`convergence-r2.md:62`) | yes |
| X-013 | V1 interaction scope (`convergence-r2.md:63`) | yes |
| A-001 | V1+V2+V3 QUALIFY; observable-specific side-effect admission (`convergence-r2.md:64`) | yes |
| A-002 | V1+V2+V3 REJECT unmeasured remote cadence premise (`convergence-r2.md:65`) | yes |
| A-003 | V1+V2+V3 QUALIFY, with V2 optional denominator (`convergence-r2.md:66`) | yes |
| A-004 | V1+V2+V3 QUALIFY (`convergence-r2.md:67`) | yes |
| A-005 | V1+V2+V3 QUALIFY (`convergence-r2.md:68`) | yes |
| A-006 | V1+V2+V3 QUALIFY (`convergence-r2.md:69`) | yes |
| A-007 | V1+V2+V3 QUALIFY (`convergence-r2.md:70`) | yes |
| A-008 | V3 REJECT fleet-load guarantee premise, shared per-process disclosure (`convergence-r2.md:71`) | no |

Design only. No code, runtime tests, live source capture, publication, push or operational action was performed.
