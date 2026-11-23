# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (Round 3 triggered by HIGH invariant INV-019, run sequentially V1, V2, V3)
- Convergence achieved: 100% after Round 2 and after Round 3 under the 2-of-3 rule (57/57); strict 3/3 agreement after Round 3: 88% (50/57). See `convergence-r2.md` and `convergence-r3.md`.
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3
- Source files: `debate-r1-variant-{1,2,3}.md`, `debate-r2-variant-{1,2,3}.md`, `convergence-r2.md`, `invariant-probe.md`

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect)
**Position**: A. Signal Bridge should be the MVP screen for R0-R1 because its largest panel runs on the one verified, paged, non-consuming contract (`orca orchestration worker-list --json`, `result.page.total`, limit 1-100), while B and C center their screens on question rows whose fields are UNVERIFIED. Recommended combination: A screen and A seams for R0-R1, B retention and question ledger as a second view at R2, C decision desk as a third view at R3, with C's gate vocabulary and bounds as the release gates. Already in Round 1 it moves R1 to `worker-list` only.

**Steelman of Variant B**: The issue's failure is a lost human question, caused by recency ordering and by treating reading as handling. Because `--peek` returns only unread messages, a peek-based panel resolves questions by reading them; only B specifies observer-side retention until explicit closure evidence, with a disclosed cap and a test that `m` never lowers the open count. B is also the most disciplined about R1 (one verb, golden sample) and has an honest fallback to A.

**Steelman of Variant C**: The human's job is one decision at a time, and C makes the evidence boundary the product: an association needs explicit-link provenance, and an unknown link set never becomes an empty but complete set. C has the most precise state mechanics (namespace plus `dispatchId` identity, separate clocks with visible equal-time conflicts, four fact states, 8 MiB stdout cap with kill and reap, Rich markup treated as literal) and the most reusable named gate vocabulary.

**Key strengths claimed**:
1. The largest panel runs on verified data today: every ledger, grouping and header field maps to a `worker-list --json` field (variant-1 sections 1 and 3, lines 5-6 and 40-56); B and C concede this.
2. Extension scaffolding: a `src/superclaude/cli/observe/` package, `sources -> Snapshot -> View(snapshot, width)`, exactly two seams (`SourceResult` and a pure view function), sanitizing once at snapshot build (section 7, lines 100-109).
3. The SIGNALS discrepancy is resolved against built code: a static read of `layouts/group_a.py` `signal_bridge` shows only the under-116 branch prints the counts line, so the seed brief's 116 claim is wrong; the prototype's `m.get(key, 0)` shows unknown as 0, which variant 1 replaces with `unavailable` (section 2, line 28; no render was run).
4. Denominators with scope names everywhere, such as `PARTIAL 300 of 412 fetched` and `140 historical hidden (h)` (section 4, lines 66-70).
5. Guards against false claims and rollback: group by `runId` labelled "run", never "orchestrator" (U-006); a monotonic cycle number so a late result cannot roll the screen back (U-001, line 169).
6. Read-only enforced by argument-vector templates and a forbidden set checked before `subprocess`, a test that survives later releases (lines 154-161, T17).
7. Message-content exposure as an owner decision (U-004), a falsifiable Rich-to-Textual switch rule (section 8, lines 141-148) and traceable offline tests T1-T21 (section 10).

**Weaknesses identified in Variant B**:
1. The R1 live screen is mostly a notice plus a proxy list, by B's own words (variant-2 line 107).
2. The proxy panel ranks rows by oldest `lastObservedAt` over an UNVERIFIED `nextAction.kind` value set, inviting the misreading B itself lists as a risk.
3. Internal contradiction on SIGNALS: B excludes "settled" for lack of a mapping, then says A's line can be filled "provided settled is defined" (X-011).
4. R2 fan-out of `check --all --run` per Run has no per-cycle Run cap; T2's static "`check` never appears" test breaks by design at R2; dedup by `dispatchId` alone is coarser than C's key.

**Weaknesses identified in Variant C**:
1. Two of three panels are unknown until two contracts verify, and C's R1 worker preview is an under-specified Signal Bridge (variant-3 lines 29-30, 129).
2. Tab focus plus per-panel scrolling under a 44-row contract is the hardest input job of the three, proposed on Rich, which has no keyboard support (X-013).
3. Bounds of 2 s per subprocess and 10 s per cycle are unmeasured, and one source per cycle leaves rotation across Runs unspecified.
4. Over-conservative on `--cursor` (one page for a 287-row source); acceptance rows have no IDs, no harness is named, and ordering by dispatch ID means nothing to a supervisor.

**Concessions**:
- No message verb in R1: `check --peek --run <id>` is withdrawn (X-002), and so is `100+ unread`, because the meaning of `result.count` is UNVERIFIED (X-003).
- `--peek` is the wrong R2 verb; B's "seen is not resolved" retention belongs in the merged model from R2 (C-002, C-010).
- C's namespace identity, separate clocks, four fact states, Rich-markup-as-literal rule, stdout cap and gate vocabulary are better (X-005, C-007, C-008, U-020, U-017, U-015); B's golden sample pins the source (U-010).
- Sanitizer reuse waits for confirmed provenance (X-008); `cost: unavailable` beats no slot (C-023); STALE at 3 poll intervals rests on unmeasured cadence (X-006, A-002).

### Variant B Advocate (opus:analyzer)
**Position**: B. Attention Ledger should be the MVP screen, with A's source-freshness strip as its header and C's `x/y shown` overflow line. The argument rests on #409's root cause: a question is lost through recency ordering and through reading being treated as handling. B's R0-R1 run one verb (`worker-list --json`), its live R1 headline states the gap ("0 rows interpreted. This is not 'no questions'"), and it has a planned fallback to A's screen if the message contract never verifies (U-009).

**Steelman of Variant A**: Every large panel runs on a verified contract today, so on day one the supervisor sees the fleet, its denominators and its stale sources, including stale and unknown workers nobody asked about. Its one-Snapshot, two-seam architecture keeps B and C open, its X-001 reading of `group_a.py` is exact, and it adds the monotonic cycle number, "run, never orchestrator", per-source backoff and the message-content exposure decision.

**Steelman of Variant C**: It shows one question beside only the sessions it affects and refuses to invent associations without explicit-link provenance (U-019). Its identity, clock and four-state rules are the most precise, its bounds (five subprocesses, 2 s, 10 s, 8 MiB, kill and reap) are the tightest, it treats external strings as literal text, it does not use `--cursor` before verification, and its gate vocabulary is reusable.

**Key strengths claimed**:
1. Evidence chain from verified help text: `--peek` shows only unread rows, so a peek-based panel resolves questions on read; only `--all` keeps read rows, capped at 100 (variant-2 section 1, lines 11-15).
2. "Seen is not resolved" made mechanical: `m` marks an item looked and the open count drops only on explicit closure evidence, none of which exists in the MVP (section 2; section 4, line 84; T10-T12).
3. Observer-side retention with `no longer in source window (last seen HH:MM)` and a disclosed 1,000-item cap (section 4, line 83; section 12, line 218).
4. One-verb R1 allow-list plus a static test that `--ack`, `"check"` and `--wait` never appear (section 9, T1-T3); a redacted golden `worker-list` sample with a shape test (T32, U-010).
5. Counter notation `n+? (k unknown)`, and per-source STALE from the last successful poll rather than Orca timestamp cadence (section 4, lines 78 and 80).
6. The R2 gate names the exact evidence and the owner action that unblocks it (permission to capture one redacted sample, U-012), plus a fallback to A on the same adapter and renderer (sections 7 and 11).

**Weaknesses identified in Variant A**:
1. Its R1 question panel rests on `check --peek`, the verb that causes the defect, with no retention in the MVP (variant-1 lines 50, 77).
2. `100+ unread` treats `result.count` as an unread total while A's own risk table marks that meaning UNVERIFIED (X-003).
3. R1 widens the allow-list and load to up to 13 subprocesses per cycle for a count of unknown meaning, and `_request` shows `qs[0]`, so source order decides which question is shown.
4. Per-row STALE at 15 s depends on unstated cadence (A-002); dedup by `dispatchId` alone with `--include-remote` in the R1 template (X-005); no provenance gate on the `canvas.py` sanitizer (X-008); SIGNALS headline buckets read `unavailable`.

**Weaknesses identified in Variant C**:
1. Not live until question identity and explicit links arrive together (X-012).
2. Retention is deferred to R3, so "seen is not resolved" is unenforced when questions first go live (variant-3 line 142).
3. One message source per cycle leaves most Runs unobserved, and default order by dispatch ID does not guarantee the oldest question is shown first.
4. An unmeasured 2 s timeout; the owner list omits question-type definition and message-body capture permission; flat, unnumbered format.

**Concessions**:
- To A: A's live R1 shows more verified data; A's X-001 reading is exact; SETTLED has no definition, so `unavailable` is right (X-011). B adopts the monotonic cycle number, "run", per-source backoff, the content-exposure opt-in, historical rows hidden with a count, the `cli/observe/` package and a cap on R2 fan-out.
- To C: B adopts the namespace identity key, separate clocks with visible conflicts, four-state facts, literal-text rendering, the 8 MiB stdout cap with kill and reap, a repeated or missing cursor guard, explicit-link provenance for affected scope, the named gate vocabulary, `unavailable (no source)` for FROZEN and "collection fresh / evidence stale".

### Variant C Advocate (haiku:backend)
**Position**: C. Decision Desk for the complete decision-focused MVP: one selected human question, only explicitly associated dispatch evidence and a bounded list of other observed questions, adopting B's retention invariant and A's collection-status discipline. This is stated as a conditional product choice, not a present live capability: the design schema is PROPOSED, and only paged worker listing and non-consuming message reads capped at 100 rows are verified. Ship a synthetic walkthrough first and a worker-only preview next, and call it a live Decision Desk only after QUESTION-LINK verification; if a useful live screen is needed before that gate, A wins that requirement.

**Steelman of Variant A**: Its worker ledger gives useful live inspection from the verified source before any message schema exists, shows workers nobody asked about and exposes source failure and coverage. Its adapter/model/view separation, monotonic generation guard, fixed-width tests and explicit fallback beyond Rich make it easier to estimate than C.

**Steelman of Variant B**: It addresses lost questions most directly: retain until explicit closure evidence, order by verified original age, and keep looking separate from resolving. It degrades honestly, and its golden sample, fake runner, required-envelope tests and fallback to A form a stronger verification harness than C specifies.

**Key strengths claimed** (proposed observer requirements, not verified Orca fields):
1. Association integrity: explicit-link provenance is required; matching tasks, worktrees, titles or times cannot create an affected-scope edge; unknown stays unknown (variant-3 "Smallest trustworthy read-only adapter", lines 184-199).
2. Independent clocks for liveness and evidence, qualified untimestamped facts and preserved equal-time contradictions (lines 201-210).
3. Idempotent observation: repeated accepted input leaves facts, counts, selection and badges unchanged, and disappearance from a partial page is only non-observation (lines 211-213).
4. Bounded failure behavior: single-flight collection, subprocess, time and output bounds, kill and reap, coalesced refresh, cursor-loop rejection and atomic publication (lines 215-228).
5. Scoped denominators and distinct uncertainty: collection age apart from evidence age, source counts apart from observed counts, row limits apart from question coverage ("Shown as unknown / stale / partial", lines 64-87).
6. Contract-driven release naming, with each gate needing success, missing, stale and contradictory samples; a synthetic walkthrough cannot clear a live gate (lines 125-148).

**Weaknesses identified in Variant A**:
1. The `100+ unread` wording outruns its evidence; A's own risk table leaves the meaning UNVERIFIED (variant-1 lines 68, 222).
2. Whole-row precedence by liveness timestamp, with ties broken by page order, can discard newer evidence and settle contradictions arbitrarily (line 169).
3. Early message fan-out (three pages plus ten peeks every 5 s) spends reads before question semantics exist, and missing fields and unexpected types share one sentinel (lines 163-167).
4. Breadth is not affected scope: the broad ledger must not substitute for a proven association.

**Weaknesses identified in Variant B**:
1. Retention eviction must not lower an apparent unresolved total; disclosure alone is not enough (variant-2 line 218).
2. `acting owner: resource.ownerDispatchId` risks a false human join.
3. Its ordering rule mixes clocks, and a fresh poll can visually mask old evidence without a separate evidence-age qualifier.
4. Selection moves to the next row when an item disappears, which can silently retarget an inspection.

**Concessions**:
- A wins earliest useful live delivery; C's question and association contracts are UNVERIFIED, and an empty question frame is not a complete MVP.
- B wins queue discovery, and retention should apply from the first live-question release.
- B wins verification specificity (recorded source, fake runner, numbered acceptance); A wins module clarity.
- Per-panel scrolling and Tab focus trigger A's framework-switch rule and need a Rich spike; C's numeric budgets (2 s timeout, 30 s evidence age) are unmeasured proposals.
- C should adopt A's titled headings, B's criterion and test IDs, a risk table and an explicit platform boundary with a plain-text fallback.

## Round 2: Rebuttals

### Variant A Rebuttal
**Conceded in Round 2** (in addition to the Round 1 concessions):
- Once the R2 question-row gate passes, B's attention ledger becomes the default view, with A's freshness strip as its header and Signal Bridge one key away as the fleet view (C-001).
- SIGNALS is renamed `COUNTS (source-reported)`, loses its bars and shows unfilled buckets as one `unavailable (no source)` token (C-005); no per-row STALE verdict in R1, only source STALE from poll success and row evidence as a plain age (X-006, A-002).
- `--include-remote` leaves the R1 allow-list until R4; four-state facts plus `n+? (k unknown)` replace the single `Missing` sentinel (C-008).
- Eviction never lowers the unresolved total (C-010); questions are oldest first at R2, never `qs[0]` by source order (C-025).
- 15 s poll interval with C's caps (5 subprocesses, 8 MiB stdout, kill and reap) and a per-call timeout set after one measured run (C-006); C's repeated or missing cursor guard (X-004); C's height contract without per-panel scrolling (S-005).
- Engineering verifies question types, and the owner chooses among verified values and grants sample capture (X-009); no production import of prototype code (X-008).

**Held**: the package and two-seam decomposition, now with C's atomic publication (S-010); the monotonic cycle number (U-001); "run, never orchestrator" (U-006); historical rows hidden with a disclosed count (C-012, X-010); the message-content exposure opt-in (U-004); the falsifiable Textual switch rule (C-018, X-013); the X-001 reading of the built layout.

**Remaining disagreements**: C-001 after R2 (B's ledger default, C desk a third view; settled by whether a redacted `check --all --json` row carries an explicit `dispatchId` reference, UNVERIFIED); C-001 at R1 (A default unless the question-row gate passes first); C-004 (proxy as a column, not a panel); C-005 / X-001 (counts strip at 116, settled by a render); X-013 / S-005 (scrolling and focus behind the Textual rule, settled by the R0 spike); C-002 / X-007 (R2 fan-out shape, settled by measured `check --all` wall time); C-006 (per-call timeout); A-008 (QUALIFY against C's REJECT, an owner answer); X-009. B conceded C-004 and C-005 in its own Round 2.

### Variant B Rebuttal
**Conceded in Round 2** (in addition to the Round 1 concessions):
- The R1 default screen is A, with B's gap line fixed at the top; B becomes the default from the first release whose question-row gate passes (C-001).
- The `SEEN IS NOT RESOLVED` count reads `unknown (no question source)` and is not drawn in R1, correcting a defect at variant-2 line 33.
- The proxy panel is withdrawn: `nextAction.kind` becomes a verbatim ledger column and a labelled filter (C-004); the counts strip stays at 160, 116 and 80 (C-005, X-001).
- R2 reads rotate across Runs under one per-cycle cap with per-Run `last read` ages (C-002, X-007); a template allow-list replaces the string ban (U-014).
- Eviction shows `n+? (k evicted, unresolved)` and marks the panel `partial` (C-010); no human-owner join from `ownerDispatchId`, and `requesting run` (U-006); selection holds a placeholder for a missing ID.
- Height contract without per-panel scrolling (S-005, X-013); C's atomic publication joins A's seams (S-010); A-002 moves to REJECT.

**Held**: retention until explicit closure evidence (C-010); oldest-first verified questions, untimed last (C-025); the one-verb R1 allow-list (X-002); no number from an unverified `result.count` (X-003); the redacted golden sample (U-010); the owner action to capture one redacted `check --all --json` sample (U-012); the fallback rule, now read in both directions (U-009); the explicit `m` look marker (U-011).

**Remaining disagreements**: B states its Round 1 disagreements with A are settled. With C: C-001 after R2 (same settling fact as A); C-025 (the first question shown must be the oldest; no technical fact settles it); X-007 (rotate all Runs against C's one selected source; settled by measured per-Run message rate and `check --all` wall time, both UNVERIFIED); C-006 (10 s placeholder against 2 s); X-004 (help-listed `--cursor` with guard against verifying first; settled by a recorded two-page sample); X-009; A-008; X-013.

### Variant C Rebuttal
**Conceded in Round 2** (in addition to the Round 1 concessions):
- A is the initial worker-only live default; the synthetic C walkthrough stays separate (C-001).
- Question readability is split from affected links: a new proposed observer gate, QUESTION-OBSERVATION, comes before QUESTION-LINK, so retained question rows can ship while links stay UNVERIFIED (X-012).
- Fair scope rotation replaces selection-bound reads, keeping one message read per cycle and the five-child ceiling, with revisit ages shown (C-002, X-007).
- The fixed row-age STALE verdict is withdrawn; evidence shows a plain age and collection freshness stays separate (C-011, X-006).
- Retention is bounded now: a proposed 1,000 detail records, bounded omitted-ID tracking and unknown totals on overflow; eviction is not closure (C-010).
- Preview interaction is reduced to one list/detail flow, with scrolling panes deferred behind the Rich spike or Textual (S-005, C-015, X-013); compact source disclosures at every width (C-005); X-001 is qualified as two agreeing static reads that C did not verify independently.
- No 2 s timeout or 10 s deadline becomes a default without representative evidence (C-006).

**Held** (non-negotiable): scoped identity; independent component clocks with visible equal-time conflict; idempotent accepted input; partial-page non-observation is not deletion; unknown is never zero or false; explicit associations only; no operational controls, AGPL code, production prototype imports or synthetic-to-live transition. Every gate is an observer requirement, not an Orca endpoint, and no sample was collected.

**Remaining disagreements**: C-001 after links verify (C's composition may serve discovery and inspection as one; settled by permissioned samples plus an owner walkthrough at all three widths); C-002 / X-007 (one rotating message read per cycle against possibly more calls; settled by latency and burst observations); retention totals under C-010 (retained count and unresolved total differ, unknown on overflow; settled by contract tests); X-013 (full C interaction may justify Textual; settled by a real-terminal spike); A-008 (REJECT against QUALIFY, mostly terminology). C states no remaining disagreement on first-release retention, zero versus unknown, clocks, literal rendering, initial oldest-observed order, explicit links, capture permission or component separation.

## Round 3: Final Arguments (if applicable)

Round 3 ran because the invariant probe (`invariant-probe.md`) found INV-019 (HIGH): the human selection of the visual direction, which the issue requires before production integration, had dropped out of the Round 2 owner list. Advocates wrote in order V1, V2, V3; each saw the earlier Round 3 files. Full text: `debate-r3-variant-{1,2,3}.md`.

### Variant A Final Argument (`debate-r3-variant-1.md`)
**Final position**: visual direction is restored as owner decision 1, with a hard gate DIRECTION-SELECTED before production integration. The A, then B, then C sequence is the advocates' recommendation, not a decision. INV-020 is carried: `check --all --run <runId> --json` is a candidate verb behind QUESTION-OBSERVATION, with three UNVERIFIED checks (does `--run` narrow `--all`; which handle receives human-addressed messages; measured message rate). Overflow notation closed as `unknown (retention exceeded)`.

**New concessions**: signed off the incomplete owner list in Round 2 (INV-019); "B ledger becomes the default" withdrawn as a fact; C-010 overflow; INV-004 whole-token argv guard replaced by exact-match templates and value checks; INV-015 export becomes its own renderer; INV-021 runtime start-up choice and `read k of N Runs` header; INV-016 NO_COLOR restored.

**Remaining**: C-001 post-link default (owner); A-008 label (word choice); `page.total` required (INV-003).

### Variant B Final Argument (`debate-r3-variant-2.md`)
**Final position**: accepts V1's gate. Changes the owner-list rule: an item belongs there if only a human can decide it, the issue assigns it to a human, or the recommendation departs from a preference the issue states. This restores visual direction, stack confirmation (Rich against the issue's Go preference) and the fallback deadline. Withdraws "rotation period times rate is the real bound": a passed gate admits the verb but never upgrades the question-area label above `bounded best effort`.

**New concessions**: INV-019 and S-008; C-001 is a recommendation; coverage argument; INV-002 backward-time readings become a visible conflict; INV-003 `result.scope` optional; INV-015 width bound applies to screen only; INV-021 runtime selection; "V1 is stronger" on gate definition and argv layers.

**Remaining**: `page.total` optional (against V1); INV-022 quiet-scope repeated readings; INV-007 keep session-seen active rows as `not reobserved`; degraded renders and a fallback date in the DIRECTION-SELECTED inputs; A-008 QUALIFY.

### Variant C Final Argument (`debate-r3-variant-3.md`)
**Final position**: accepts V1's gate and V2's owner-list rule. Adds: the selection record holds location, defaults before and after QUESTION-OBSERVATION and the post-link choice or a deferral; an unsupported selection never clears a source gate; renders at 160, 116 and 80 columns with degraded versions and a find-and-inspect task; the fallback date is the owner's; acquisition permission is checked before a message call (INV-017); side-effect observables are UNVERIFIED (INV-022); 15 s cycle, at most 5 calls, at most 1 message call per cycle, STALE at 45 s monotonic (INV-023).

**Remaining** (7 points marked "no" of 57): S-007 production boundary read as "first wiring into the shipped product" (stricter reading applies until the owner confirms); S-008 acquisition scope; C-001 recommends C as the post-link composition; C-002 and X-007 one message call per cycle; C-006 timing; A-008 REJECT.

**Closing statement**: "Design only. No code, runtime tests, live source capture, publication, push or operational action was performed."

## Scoring Matrix

Winner names the variant(s) whose approach the advocates agreed on after Round 2 (A = Signal Bridge, B = Attention Ledger, C = Decision Desk), taken from `convergence-r2.md`. Confidence: 3/3 agreement scores 95%, or 90% where a parameter still waits on a measurement or owner answer; 2/3 agreement scores 65%.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | A | 95% | All three: H1 title plus numbered sections. |
| S-002 | B | 95% | Depth-3 hierarchy with width and evidence subsections. |
| S-003 | A+B+C | 95% | Keep the shared 12-section order; nothing to resolve. |
| S-004 | A+B | 95% | Tables for bounds, gates and matrices; bullets where prose is needed. |
| S-005 | A+B+C | 95% | A width matrix, B coordinates, C 44-row height contract; per-panel scrolling deferred. |
| S-006 | B | 90% | AC-n IDs with numbered tests; mapping to #409 still to be re-checked. |
| S-007 | C+B | 95% | Gate-column table with B's fallback rule, gates in C's vocabulary with four samples each. |
| S-008 | C+B+A | 95% | Owner list limited to sample-capture permission, content exposure and choice among verified question types. |
| S-009 | B | 95% | Separate risks table and UNVERIFIED list. |
| S-010 | A+C (+B signature) | 95% | `observe` package, two pure seams, one atomically published view, monotonic generation; no plugin system. |
| S-011 | B | 95% | Plainly stated own weakness. |
| C-001 | Merged (A R0-R1, B after question-row gate, C later) | 65% | 2 of 3 split: A and B make B's ledger the default once the question-row gate passes; C dissents and prefers its desk as the complete composition once links verify. |
| C-002 | B+C (+A) | 90% | `check --all --run`, not `--peek`, with retention and Runs rotated under one cap; messages per cycle wait on latency measurement. |
| C-003 | B+C | 95% | Gap statement and no number in the question area. |
| C-004 | A+C | 95% | `nextAction.kind` as a verbatim ledger column and filter, never a question; B withdrew its proxy panel. |
| C-005 | A+B+C | 95% | Source-counts strip with scope and denominators at 160/116/80; no bars or health name; never summed. |
| C-006 | B+C+A | 90% | 15 s interval, 5 subprocesses, 8 MiB stdout, kill and reap, backoff; per-call timeout set after one measured run. |
| C-007 | C+A | 95% | Independent clocks with visible equal-time conflicts plus the monotonic cycle number. |
| C-008 | C+B | 95% | Four states per fact; `n+? (k unknown)` for aggregates. |
| C-009 | B+C | 95% | Explicit `m` look marker; first observation is the baseline; a partial page means not reobserved. |
| C-010 | B+C | 90% | Retain until explicit closure evidence; eviction never lowers the total; overflow notation (partial or unknown) open. |
| C-011 | B+C | 95% | Source STALE from collection success; evidence age shown separately, no row verdict. |
| C-012 | A+C | 95% | Historical rows hidden by default with a disclosed count; explicitly linked historical evidence stays visible. |
| C-013 | B+C | 95% | `page.total (source)` is a source-reported denominator, not the fleet. |
| C-014 | B+C | 95% | At most 100 rows per read, not 100 questions, plus a `no longer in source window` marker. |
| C-015 | A+B | 95% | List/detail keys plus `/`, `h`, `m`, `e`, `q`; Tab panel focus deferred to the spike. |
| C-016 | A | 95% | Trailing `>` marker; full value in detail and export. |
| C-017 | A+B | 95% | ASCII-safe export with full IDs and caveats; A's `--ascii` box replacement. |
| C-018 | A+C | 95% | Rich after a passed spike; falsifiable Textual trigger; never build both. |
| C-019 | A | 90% | Short in-repo command such as `superclaude observe`; final name from the owner. |
| C-020 | C+B | 95% | Literal Rich text, own sanitizer, no prototype import. |
| C-021 | A+B+C | 95% | Recorded-console harness and fake runner on a redacted golden sample; synthetic passes never clear live gates. |
| C-022 | A+C | 95% | No FROZEN number without a field; missing is unknown, never unfrozen. |
| C-023 | C+B | 95% | Cost shown as unavailable, never `$0`. |
| C-024 | B+A | 95% | POSIX interactive plus `--once` text export on every platform. |
| C-025 | C+B+A | 95% | Oldest verified question first, untimed last; stable worker rows grouped by run; selection anchored to ID. |
| X-001 | A | 90% | A and B static reads: built layout drops the counts line at 116; merged design keeps a strip at every width; no render run yet. |
| X-002 | B+C | 95% | R1 allow-list is `worker-list` only. |
| X-003 | B+C | 95% | No number from `result.count` until its meaning is verified. |
| X-004 | B+C | 90% | Help-listed `--cursor` with a repeat/missing guard and `PARTIAL` fallback; a two-page sample is still to be recorded. |
| X-005 | C | 95% | Key rows by source namespace plus `dispatchId`. |
| X-006 | B+C | 95% | No row STALE threshold; source STALE from poll success. |
| X-007 | C+B | 90% | One total per-cycle subprocess cap; rotating message reads with per-scope ages; message calls per cycle open. |
| X-008 | B+C | 95% | No production import of prototype code; provenance before any reuse. |
| X-009 | C+B | 95% | Engineering verifies the type vocabulary from real rows; the owner chooses among verified candidates. |
| X-010 | A | 95% | Historical rows hidden by default with a count. |
| X-011 | A | 95% | SETTLED shows `unavailable`; no verified field defines it. |
| X-012 | A+B | 95% | Retained question rows ship before links verify, with affected scope shown as unknown. |
| X-013 | A | 95% | No per-panel scrolling or multi-pane focus in the Rich MVP; those wait for the spike or Textual. |
| A-001 | A+B+C | 95% | QUALIFY: only non-consuming is verified; check each admitted verb for side effects. |
| A-002 | A+B+C | 95% | REJECT as a premise: no stale verdict rests on Orca timestamp cadence until it is measured. |
| A-003 | A+B+C | 95% | QUALIFY: validate one complete JSON envelope, bound stdout, capture a real call before R1. |
| A-004 | A+B+C | 95% | QUALIFY: recorded width tests plus one real-terminal wide-glyph check. |
| A-005 | A+B+C | 95% | QUALIFY: R0 key-reader spike with redraw, resize and restore; failure fires the Textual rule. |
| A-006 | A+B+C | 95% | QUALIFY: measure render time on a 100-row fixture at 160 columns. |
| A-007 | A+B+C | 95% | QUALIFY: non-UTF-8 terminals get the ASCII box path on screen. |
| A-008 | A+B (QUALIFY) | 65% | 2 of 3 split: A and B QUALIFY (per-process caps disclosed, preventing several observers is an owner decision); C REJECTs the premise and calls the difference mostly terminology. |

## Convergence Assessment

- Points resolved (2-of-3 rule): 57 of 57 after Round 2 (`convergence-r2.md`) and after Round 3 (`convergence-r3.md`).
- Strict 3/3 agreement after Round 3: 50 of 57 (88%).
- Alignment: 100% under the 2-of-3 rule; threshold 75%: **MET** under both counts. No force-select.
- Note: the Scoring Matrix above reflects the Round 2 winners. Round 3 changes that override it: C-001 becomes a recommendation pending owner decision 1 (DIRECTION-SELECTED gate); S-007 gains that gate; S-008 uses V2's owner-list rule; C-002 and X-007 present `check --all --run` as a candidate verb only; C-006 restores the 15 s cycle and STALE after 45 s; C-010 overflow is `unknown (retention exceeded)`; C-017 export is a separate renderer. Details: `convergence-r3.md` "Changes to the Round 2 Consensus".
- Unresolved points (2 of 3 only, carried as dissents or open parameters): S-007 production-boundary reading (owner); C-001 post-link default (owner); C-002 and X-007 message calls per cycle (measurement); C-008 and A-003 `page.total` required or optional (merge chooses optional, V1 dissent); A-008 label (merge uses QUALIFY, V3 dissent).
- Unaddressed HIGH invariants: none (INV-019 resolved in design, its gate not yet passed; INV-020 resolved by wording).
