# Refactoring Plan: Merge into Base (Variant 2)

## Overview

- **Base**: Variant 2 (opus:analyzer, B Attention Ledger), `variant-2-opus-analyzer.md`, selected in `base-selection.md` (0.9430 against V1 0.9412 and V3 0.8345; near tie broken on debate points 44 to 35).
- **Incorporating strengths from**: Variant 1 (opus:architect, A Signal Bridge), Variant 3 (haiku:backend, C Decision Desk), the Round 2 consensus (`convergence-r2.md` lines 83-133) and the Round 3 final arguments (`debate-r3-variant-{1,2,3}.md`).
- **Planned changes**: 32 (3 base fixes, 8 from V1, 9 from V3, 12 from the consensus and Round 3).
- **Risk level**: Medium. Most changes are additive; the riskiest are the default-screen rewrite (Change 21), the release gate table rewrite (Change 22) and the R2 verb rewording (Change 24), because they touch claims about what Orca returns.
- **Preserve unchanged** (base-selection.md lines 180-189): the evidence chain for retention, "seen is not resolved" made mechanical, the one-verb R1 adapter, the gated release table with the A fallback, AC-1 to AC-10 with T1-T32 (renumber only where new tests are added), the risks and UNVERIFIED lists, the denominator wording, and owner decision 5 (sample-capture permission).
- **Evidence rule for the merge**: the design-package schema is PROPOSED, not an Orca API. Only `worker-list --json` (paged, `page.total`, `page.hasMore`, `page.nextCursor`, limit 1-100) and non-consuming `check --peek` / `check --all` (capped at 100 rows) are verified. Every other source stays UNVERIFIED. Unknown is never shown as zero or false. No operational controls.

## Planned Changes

### Change 1: Replace the next-actions proxy panel with a verbatim column (base fix)

- **Source**: base-selection.md item 18; consensus "nextAction.kind is a verbatim column" (convergence-r2.md, Unknowns).
- **Target**: replace. Base section 2 (First buildable slice), the WORKER-REPORTED NEXT ACTIONS panel near base line 32.
- **Rationale**: the panel implied a curated action list the adapter cannot produce; a verbatim `nextAction.kind` column shows only what the source reported, and blank or missing shows "unknown".
- **Integration point**: the ledger column list in section 2; any section 10 test that names the panel is renamed.
- **Risk**: Low.

### Change 2: Add tests for the policy-frozen and empty states (base fix)

- **Source**: base-selection.md item 19.
- **Target**: append. Base section 4 rows near lines 85 (empty) and 87 (policy frozen) gain test IDs; section 10 gains the two tests.
- **Rationale**: the base names both states but no test pins their rendering, so "empty" could regress to "no questions" and "frozen" to blank.
- **Integration point**: section 10 test list, new IDs after T32.
- **Risk**: Low.

### Change 3: Settle one renderer output type (base fix)

- **Source**: base-selection.md item 20; INV-015 response (debate-r3-variant-2.md, MEDIUM section).
- **Target**: restructure. Base section 8 near line 152 and section 10 near line 173.
- **Rationale**: the base describes two output types in two places. The merge states one view model rendered by two renderers (interactive screen and `--once` export), so tests assert on the same view model.
- **Integration point**: section 8 Stack and section 9 Adapter (`observe` package boundary).
- **Risk**: Low.

### Change 4: Counts strip at every supported width (from Variant 1)

- **Source**: variant-1-opus-architect.md, counts strip; base-selection.md item 1; INV-013 response.
- **Target**: insert. Base section 2, above the ledger.
- **Rationale**: all three advocates agreed the source-reported COUNTS strip is the one always-visible summary. The strip is shown at 80 columns and wider; below 80 the screen reads "terminal too narrow" (INV-013). Priority tokens are never truncated (INV-014).
- **Integration point**: section 2 layout; section 10 adds width tests at the listed test widths.
- **Risk**: Low.

### Change 5: Snapshot model with two seams and a monotonic cycle number (from Variant 1)

- **Source**: variant-1-opus-architect.md, snapshot model; base-selection.md item 2.
- **Target**: append. Base section 9 (Adapter).
- **Rationale**: a collector seam (subprocess runner) and a view seam (pure render from a snapshot) let tests drive both with fakes. The monotonic cycle number orders snapshots without trusting wall clocks.
- **Integration point**: section 9, next to the single-flight collector from the consensus (Change 27).
- **Risk**: Low.

### Change 6: Historical rows hidden behind `h` (from Variant 1)

- **Source**: base-selection.md item 3; consensus "Historical rows hidden".
- **Target**: insert. Base section 2 keys and section 5 (Left out).
- **Rationale**: finished workers crowd the ledger; hiding them by default with a visible count and an `h` toggle keeps the attention rows on screen without deleting evidence.
- **Integration point**: section 2 key list.
- **Risk**: Low.

### Change 7: SETTLED and POLICY FROZEN shown as "unavailable" (from Variant 1)

- **Source**: base-selection.md item 4; consensus "SETTLED and FROZEN show unavailable".
- **Target**: replace. Base section 4 rows for those two states.
- **Rationale**: no verified source reports settlement or policy freeze, so they render as "unavailable", never blank or zero.
- **Integration point**: section 4 table and the tests from Change 2.
- **Risk**: Low.

### Change 8: Keys `/ h m e q` plus navigation, with ID-anchored selection (from Variant 1)

- **Source**: base-selection.md item 5; consensus keys "Up/Down, j/k, Enter, Esc, / h m e q".
- **Target**: replace. Base section 2 key list.
- **Rationale**: V1 proposed `r`; the consensus replaced it with `m` (since-last-look marker, Change 15). Selection is anchored to the row ID so a refresh never moves the cursor to a different worker.
- **Integration point**: section 2 keys; section 10 selection-stability test.
- **Risk**: Low.

### Change 9: `>` truncation marker and `--ascii` mode (from Variant 1)

- **Source**: base-selection.md item 6.
- **Target**: append. Base section 2 layout rules and section 8 Stack.
- **Rationale**: a single visible truncation marker that survives ASCII output; non-UTF-8 terminals use the ASCII path.
- **Integration point**: section 8 export rules.
- **Risk**: Low.

### Change 10: Allow-list test with the subprocess patched to fail, and the NO_COLOR tests (from Variant 1)

- **Source**: base-selection.md item 7; INV-016 response.
- **Target**: append. Base section 10.
- **Rationale**: a test runs the adapter with the real subprocess call patched to raise, so any unlisted argv fails loudly. NO_COLOR=yes is tested, and the colour-enabled case is restored (INV-016) so both directions are pinned.
- **Integration point**: section 10 test list, next to the INV-004 argv tests (Change 25).
- **Risk**: Low.

### Change 11: `superclaude observe` placement with the Textual switch rule (from Variant 1)

- **Source**: base-selection.md item 8; consensus Stack.
- **Target**: replace. Base section 8 placement paragraph.
- **Rationale**: the MVP lives in this Python repository as a recommended `superclaude observe` command (name is an owner decision, Change 23). The R0 spike tests a raw key reader with Rich Live; if it fails, switch to Textual. Never build both.
- **Integration point**: section 8 and section 7 R0 row.
- **Risk**: Medium (the command name and the stack are owner-confirmed, not settled).

### Change 12: Four states per fact (from Variant 3)

- **Source**: variant-3-haiku-backend.md; base-selection.md item 9; consensus "4 states per fact".
- **Target**: insert. Base section 4 (Shown as unknown), as the governing rule.
- **Rationale**: every rendered fact is one of known, unknown, unavailable, or stale. Aggregates show `n+? (k unknown)` so an unknown never collapses into zero.
- **Integration point**: section 4 header; section 10 aggregate test.
- **Risk**: Low.

### Change 13: Independent clocks and dedup by namespace plus dispatchId (from Variant 3)

- **Source**: base-selection.md item 10; consensus Identity.
- **Target**: append. Base section 9.
- **Rationale**: each component keeps its own clock; identity is namespace plus dispatchId so two hosts or Runs never merge rows. A clock that goes backwards shows a visible "conflict (time went back)" (INV-002).
- **Integration point**: section 9 identity paragraph.
- **Risk**: Low.

### Change 14: Per-cycle caps that replace base line 161 (from Variant 3)

- **Source**: base-selection.md item 11; consensus Bounds; INV-023 response.
- **Target**: replace. Base section 9 polling paragraph near line 161.
- **Rationale**: the base polling values conflict with the consensus. Merged values: 15 s interval and cycle budget, at most 5 subprocesses per cycle, 8 MiB output cap, backoff to 60 s, per-call timeout measured in R0 (not guessed). Source STALE after 3 missed intervals. The 30 s deadline is withdrawn.
- **Integration point**: section 9; section 10 backoff and STALE tests.
- **Risk**: Medium (per-call timeout value is UNVERIFIED until measured).

### Change 15: Since-last-look baseline with the `m` marker (from Variant 3)

- **Source**: base-selection.md item 12; consensus Retention.
- **Target**: insert. Base section 2.
- **Rationale**: the first observation is the baseline; `m` sets a new mark, and rows changed since the mark are flagged. Gives "what changed while I was away" without event replay (not established).
- **Integration point**: section 2 keys and section 4.
- **Risk**: Low.

### Change 16: Collection freshness separate from evidence freshness (from Variant 3)

- **Source**: base-selection.md item 13.
- **Target**: append. Base section 4.
- **Rationale**: "polled 4 s ago" and "worker last reported 20 min ago" are different facts; STALE on the source is based on poll success only.
- **Integration point**: counts strip (Change 4) and section 4.
- **Risk**: Low.

### Change 17: Overflow denominator excludes the selected item (from Variant 3)

- **Source**: base-selection.md item 14.
- **Target**: replace. Base denominator wording in section 4.
- **Rationale**: "+N more" counts rows not shown, so the selected visible row is never double-counted. Base denominator wording is otherwise preserved.
- **Integration point**: section 4 and section 10 overflow test.
- **Risk**: Low.

### Change 18: Gate vocabulary with four sample kinds (from Variant 3)

- **Source**: base-selection.md item 15; consensus Build order.
- **Target**: restructure. Base section 7 gate table.
- **Rationale**: each gate is passed only by recorded samples of four kinds: success, missing, stale, contradictory. Without all four the gate stays closed.
- **Integration point**: section 7, merged with Change 22.
- **Risk**: Medium.

### Change 19: Literal text rendering plus operational tests (from Variant 3)

- **Source**: base-selection.md item 16; consensus "Sanitizer of our own. Text rendered literally, not as Rich markup".
- **Target**: append. Base sections 9 and 10.
- **Rationale**: worker-supplied text could contain Rich markup or control sequences; our own sanitizer strips control characters and every string is rendered as literal text. Tests cover markup injection, control characters and one CJK width case.
- **Integration point**: section 9 sanitizer; section 10.
- **Risk**: Low.

### Change 20: "Cost unavailable", never $0 (from Variant 3)

- **Source**: base-selection.md item 17; consensus.
- **Target**: insert. Base section 4.
- **Rationale**: cost and usage accounting coverage is not established, so cost renders "unavailable".
- **Integration point**: counts strip and section 4.
- **Risk**: Low.

### Change 21: Default screen stated as a recommendation pending the owner (from the Round 2 consensus, C-001)

- **Source**: convergence-r2.md Emerging Consensus, Default screen; C-001 (agreed 2 of 3); INV-021 response (debate-r3-variant-2.md).
- **Target**: replace. Base section 1 Summary and section 2 opening.
- **Rationale**: recommended default: while no question rows can be read (R0-R1), A's worker ledger plus the COUNTS strip plus B's question-gap notice; after QUESTION-OBSERVATION passes, B's Attention Ledger; C's Decision Desk only behind QUESTION-LINK. The default view is chosen at start-up and never switches mid-session; the header shows `read k of N Runs`. The section states this is a recommendation and the owner's selection record (Change 23) decides it. V3's dissent is recorded (see Changes NOT Being Made).
- **Integration point**: sections 1, 2 and 6 (Where A and C are stronger).
- **Risk**: Medium (contradicts the base's "B from day one" framing; must not leave both framings).

### Change 22: Release gate table with the DIRECTION-SELECTED gate first (from the consensus and Round 3)

- **Source**: convergence-r2.md Build order; debate-r3-variant-1.md lines 26-31 (DIRECTION-SELECTED); debate-r3-variant-2.md Response to INV-019.
- **Target**: restructure. Base section 7 Build order.
- **Rationale**: order: R0 (redacted golden fixture, Rich Live key-reader spike, render timing, and the A/B/C renders at 160, 116 and 80 columns marked "synthetic fixture, not live evidence"), then the DIRECTION-SELECTED gate (missing: no production integration, R0 continues; stale: a later gate that changes what a direction can show triggers a re-confirm; contradictory: a selection whose data gate has not passed ships the nearest gated view with the reason on screen, and a gate is never bypassed to honour a selection), then R1 (worker-list adapter, ledger, strip), R2 (questions, only after QUESTION-OBSERVATION passes), R3 (links and C's desk, only after QUESTION-LINK), R4 (`--include-remote`, cross-host). Each data gate uses the four sample kinds (Change 18). R1 cannot start before the selection record, which is cheap to produce. An optional second owner confirmation at QUESTION-LINK for the post-link default (B or C) is the owner's call. The base's A fallback is preserved: if a gate fails, the screen stays on the previous release's view.
- **Integration point**: section 7, sections 3 and 11.
- **Risk**: Medium.

### Change 23: Restore the owner decisions and add the owner-list rule (Round 3, INV-019)

- **Source**: invariant-probe.md INV-019 (HIGH); debate-r3-variant-1.md lines 26-33; debate-r3-variant-2.md amendments 1-3 and owner-list rule.
- **Target**: restructure. Base section 11 Owner decisions.
- **Rationale**: the R2 consensus list dropped decisions the issue gives to a human. Rule: a decision goes to the owner if only a human can decide it, the issue assigns it to a human, or the recommendation departs from a preference the issue states. Decision 1 becomes a dated selection record written by the owner, never an agent, naming (a) the default while no question rows exist, (b) the default after QUESTION-OBSERVATION, (c) a fallback date, plus stack confirmation (Python Rich against the issue's stated Go Bubble Tea v2 preference) and the command name. The owner reviews renders of each direction in its shipped, degraded state (gap notice, `read k of N Runs since start`, "bounded best effort", "affected scope unknown") at 160, 116 and 80 columns, with the walkthrough task "find the oldest question and inspect its evidence". A re-confirm trigger fires when the fallback date passes. The remaining decisions stay: sample-capture permission (base decision 5, preserved), message-content exposure, accepted `type` values, multiple observers. A new AC checks that the selection record exists; a reviewer checks it, never an automated test.
- **Integration point**: section 11, section 7 DIRECTION-SELECTED gate, section 10 new AC.
- **Risk**: Low.

### Change 24: Reword the R2 question verb as a candidate (INV-020)

- **Source**: invariant-probe.md INV-020; convergence-r2.md line 96.
- **Target**: replace. Every place that states R2 "uses" `check --all --run <runId> --json` (base sections 3 and 7).
- **Rationale**: the verb is a candidate behind QUESTION-OBSERVATION, which needs three UNVERIFIED proofs: (a) `--run` narrows results, shown with at least 2 Runs; (b) which handle receives the messages; (c) message rate times the poll period stays under the 100-row cap. Even then the label is "bounded best effort", because a measured rate does not prove completeness. Message row fields and the inbox JSON shape stay UNVERIFIED. Plain `check` (which consumes) is forbidden.
- **Integration point**: sections 3, 7, 12 UNVERIFIED list.
- **Risk**: Medium.

### Change 25: argv validation hardening (INV-004)

- **Source**: debate-r3-variant-2.md INV-004 response; consensus "argv allow-list with a forbidden set that never shrinks".
- **Target**: append. Base section 9 and section 10.
- **Rationale**: exact template flags only; a prefix-matched forbidden set; format checks on runId and cursor; reject any value that starts with `-`; `--opt=value` form only if Orca accepts it (UNVERIFIED, so the default is separate arguments); a fake runner that fails the test if reached with an unlisted argv. R1 allow-list: `worker-list --json --limit 100`, optional `--run`, `--cursor` with a guard that marks the view PARTIAL; no `--include-remote` until R4.
- **Integration point**: section 9 adapter; section 10 next to Change 10.
- **Risk**: Low.

### Change 26: Question retention rules (from the consensus)

- **Source**: convergence-r2.md Retention.
- **Target**: append. Base section 9, beside the preserved evidence chain.
- **Rationale**: keep each question until closure evidence is seen; bound 1,000 records; eviction never lowers the reported total; overflow is open (shown as unknown or partial, never closed); questions list oldest first.
- **Integration point**: section 9; section 10 eviction test.
- **Risk**: Low.

### Change 27: Adapter structure and the required fields (from the consensus, INV-003)

- **Source**: convergence-r2.md Data adapter; debate-r3-variant-2.md INV-003 response.
- **Target**: restructure. Base section 9.
- **Rationale**: an `observe` package with a SourceResult type and a pure view; a single-flight collector publishes each snapshot atomically; parse exactly one JSON envelope per call and keep the last good data on failure. Required fields: `result`, `result.workers`, `page.hasMore`. Optional: `scope` (else "scope unknown") and `page.total` (else "reported unknown"). V1 wanted `page.total` required: recorded as an open disagreement in section 12.
- **Integration point**: section 9 and section 12.
- **Risk**: Low.

### Change 28: Question-area wording and counting rules (from the consensus, INV-005, INV-009)

- **Source**: convergence-r2.md Unknowns; debate-r3-variant-2.md INV-005 and INV-009 responses.
- **Target**: replace. Base section 4 question-area text.
- **Rationale**: before R2 the area reads "source UNVERIFIED, 0 rows interpreted, not 'no questions'". Never derive a count from `result.count`; show "collected n unique / reported T". 100 rows means 100 rows, not 100 questions. A row that changed while being read shows a "changed during read" note; a count mismatch shows a mismatch note (INV-005). Rows that cannot all fit rotate, with a `revisit ~Ns` token (INV-009).
- **Integration point**: section 4; section 10.
- **Risk**: Low.

### Change 29: Accepted risks and privacy rules (INV-007, INV-017, INV-022)

- **Source**: debate-r3-variant-2.md responses to INV-007, INV-017, INV-022.
- **Target**: append. Base section 12 Risks and section 9.
- **Rationale**: INV-007 is an accepted risk: rows seen this session that drop out of the source stay listed as "not reobserved", and the strip discloses it; whether a state filter exists is UNVERIFIED. INV-017: message bodies from terminals that have not opted in are dropped before rendering. INV-022: the R2 gate takes repeated before-and-after readings on a quiet scope to show the non-consuming check really does not consume.
- **Integration point**: sections 9, 7 and 12.
- **Risk**: Low.

### Change 30: Acceptance tests mapped to the issue's criteria (from the consensus)

- **Source**: convergence-r2.md Tests.
- **Target**: append. Base section 10.
- **Rationale**: every AC ID maps to named tests; tests use a recorded console and a fake runner fed with a golden sample; one CJK width test. New tests from Changes 2, 4, 10, 14, 19, 25, 26 and 28 are added after T32. The selection-record AC (Change 23) is listed as reviewer-checked.
- **Integration point**: section 10.
- **Risk**: Low.

### Change 31: Define "production integration" (Round 3, Variant 1)

- **Source**: debate-r3-variant-1.md line 32.
- **Target**: insert. Base section 7, beside the DIRECTION-SELECTED gate.
- **Rationale**: "production integration" is the first change that registers `superclaude observe` in the shipped CLI, or lets the adapter run a live Orca subprocess outside the fake runner. R0 (offline fixture, spike, renders) is design material and may come before the selection record; production integration may not. This reading is V1's interpretation and is UNVERIFIED as the issue's intent, so the owner confirms it in the selection record.
- **Integration point**: section 7.
- **Risk**: Low.

### Change 32: Variant 3 Round 3 final concessions

- **Source**: debate-r3-variant-3.md lines 15-24 (INV-019 amendments), lines 30-47 (MEDIUM table), lines 51-61 (remaining disagreements), lines 63-71 (concessions).
- **Target**: modify. Base sections 7, 9, 10, 11 and 12, layered on Changes 14, 22, 23, 25, 27, 29 and 31.
- **Rationale**: V3 accepts the DIRECTION-SELECTED gate and the owner-list rule, and adds these refinements, each adopted unless noted:
  1. The selection record also holds the owner's location of the statement, the pre-observation default, the post-observation default, and the post-link choice or an explicit deferral. Agents may cite the owner's statement but never write it. An unsupported selection never clears a source gate (narrows Change 22's "contradictory" rule: ship only an owner-accepted gated fallback, or stay blocked).
  2. The R0 renders include realistically degraded versions (unavailable, PARTIAL) beside the synthetic best case, at 160, 116 and 80 columns, plus C's find-the-oldest-question-and-inspect-its-evidence task. The fallback date is the owner's product-tolerance choice; expiry prompts re-confirmation and never grants permission to switch direction.
  3. "Production integration" boundary: V3 proposes "first wiring or enabling the observer in the shipped product", with separately authorized read-only capture counted as research. Not adopted as the rule; recorded beside Change 31 as a second UNVERIFIED reading. Until the owner confirms one, the stricter reading (offline work only) applies, which all three advocates accept.
  4. Acquisition permission (INV-017, strengthens Change 29): permission must cover the actual read scope before the call, separately from display and export permission. Parse-time dropping cannot undo receipt into the stdout buffer, so the document never claims unauthorized bodies were not acquired. If a narrow read cannot honor the permission, the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
  5. Side-effect test observables (INV-022, qualifies Change 29): message IDs, inbox shape and lease fields are UNVERIFIED, so the quiet-scope test first establishes readable identity fields; help text and an empty peek `count` alone cannot clear the gate; a pass covers only the visible effects tested.
  6. Argv (INV-004, qualifies Change 25): V1's numeric bounds and regexes are PROPOSED, not verified Orca formats; the cursor is bounded by bytes and safe binding, not by an inferred grammar; `--opt=value` only after parser support is recorded.
  7. Freshness (INV-023, aligns Change 14): STALE after 45 s without success on a local monotonic clock (3 intervals of 15 s); at most one message call per cycle inside the five-call cap is V3's default and stays an open budget point (C-002 / X-007).
  8. Rotation set (INV-009): permissioned scopes from the configured set, discovered non-historical worker scopes and retained-question scopes, deduplicated; an empty set reads "message source not read: no eligible scope; coverage unknown".
  9. Height (INV-014): coverage, scope and PARTIAL are minimum content ahead of optional panels; if the height cannot hold them, show a too-small diagnostic.
  10. Overflow (INV-025): `unknown (retention exceeded)` plus the retained count.
  11. Question ties use verified source-scoped question identity, never a worker `dispatchId`; that identity remains a QUESTION-OBSERVATION gate requirement.
  12. V3 aligns with base on optional `page.total` (C-008 / A-003), leaving V1 alone in the INV-003 disagreement.
  13. V3 keeps its C-001 dissent (C as the post-link inspection composition) and its A-008 label disagreement (REJECT, not QUALIFY); both are recorded in section 12, not applied.
- **Integration point**: section 7 (items 1-3, 7), section 9 (items 4, 6, 8, 11), section 10 (items 2, 5, 9, 10), section 11 (items 1-3), section 12 (items 3, 12, 13).
- **Risk**: Low. The items narrow or qualify earlier changes; none changes the build order or the recommended direction.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| Default screen after QUESTION-LINK (C-001, agreed 2 of 3) | V3: C's Decision Desk becomes the default once explicit-link rows exist | Two advocates hold that B's ledger stays the default and C's desk is a view behind the link gate. Recorded as V3's dissent; the owner's selection record (Change 23) can still pick C, and the optional QUESTION-LINK re-confirm exists for exactly this choice. |
| Required `page.total` (INV-003) | V1: `page.total` is a required field; a response without it is rejected | Base keeps it optional and renders "reported unknown". Rejecting the whole envelope would hide the workers that were returned. Recorded as an open disagreement. |
| Signal Bridge collapse widths (X-001) | V1 / seed brief: Signal Bridge collapses at 116 and 80 columns as in the brief | The built prototype does not match the brief's collapse claim, and the prototype is a visual reference only. The merged width rules come from the consensus (A's width matrix, B's coordinates, C's 44-row contract), not from the prototype. |
| Go Bubble Tea v2 as the MVP stack | Issue preference: Go with Bubble Tea v2, Lip Gloss v2, Bubbles v2 (MIT) | Kept Python Rich for the MVP because the repository is Python, Rich 15.0.0 is already a dependency, and it gives the best text export; Go adds a toolchain and binary pipeline, and teatest/v2 is untagged. Because this departs from the issue's stated preference, it is an owner decision (Change 23), not a settled choice. |
| Textual as the first stack | V1 alternative: start on Textual 8.2.8 | Kept as the fallback only if the R0 key-reader spike fails; Textual carries medium maintenance risk and its plain-text export is UNVERIFIED. Never build both. |
| `r` refresh key | V1: `r` forces a refresh | Replaced by `m` (since-last-look marker); refresh is on the fixed 15 s cycle, so a manual refresh key adds a second polling path. |
| 30 s collection deadline | Earlier base value | Withdrawn in Round 3 (INV-023); the 15 s cycle budget and STALE after 3 intervals replace it. |
| Measured message rate as proof of completeness | V2 R2 (debate-r2-variant-2.md line 27): "the real bound is: rotation period per Run, times that Run's message rate, must stay under 100 rows" | A measured average rate does not prove completeness (V3, debate-r2-variant-3.md line 23); V2 withdrew "the real bound" in Round 3 (debate-r3-variant-2.md line 86). The label stays "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". |
| Operational controls (approve, retry, terminate) | Design-package mock-ups show action buttons | Excluded by the brief: the observer is read-only. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1-3 | Low | A stale panel name or second output type survives in one section | Re-scan sections 2, 8, 10 for the old names |
| 4-10 | Low | Width, key or test text disagrees between sections 2 and 10 | Align section 10 to section 2 |
| 11 | Medium | Command name or stack reads as settled | Mark both as owner decisions in sections 8 and 11 |
| 12-13, 15-17, 19-20 | Low | An unknown renders as zero or blank in one table row | Re-scan section 4 for any zero default |
| 14 | Medium | Old base line 161 values left beside the new ones | Delete the old values; keep only the consensus bounds |
| 18, 22 | Medium | Gate table loses the A fallback or the four sample kinds | Restore from base section 7 and Change 18 |
| 21 | Medium | Document states both "B from day one" and the staged default | Keep only the staged recommendation, marked pending owner |
| 23 | Low | Stack, fallback date or command name missing from the owner list | Re-check section 11 against the owner-list rule |
| 24 | Medium | A sentence still says R2 "uses" `check --all --run` as available | Grep the merged output for `check --all` and reword each hit |
| 25-31 | Low | One hardening rule missing from section 9 or 10 | Add from this plan |
| 32 | Low | V3 concessions contradict the merged default | Record as dissent in section 12 |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved
- Approved by: auto (non-interactive run; no `--interactive` flag)
- Approval timestamp: 2026-11-08T14:50:00+00:00
