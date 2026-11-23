# Convergence After Round 2

## Method

- Rule (adversarial protocol): a point is AGREED when all 3 advocates, or at least 2 of 3, back the same superior approach after Round 2; the majority choice is the winner. With no majority the point is UNRESOLVED. Score = agreed points / 57, to 2 decimals. Threshold for this brainstorm: 0.75.
- Agreement is judged on the substance each advocate now supports (including Round 2 concessions), not on which variant label appears in its "Preferred variant" column. An advocate that concedes to another variant's approach counts as backing that approach. Ambiguous stances are counted conservatively (not agreed); none were found ambiguous enough to need that.
- Where all three back the same approach but a numeric parameter or edge-case notation is still open pending a measurement or owner answer, the point counts as agreed and the open parameter is named in the row and in the Emerging Consensus list. These residuals are not separate diff points.
- Inputs read: `diff-analysis.md` (IDs, titles, levels of the 57 S, C, X and A points); `debate-r2-variant-1.md` (Signal Bridge, opus:architect), "Concessions Added in Round 2", "Revised Positions", "Updated Per-Point Stances" and "Remaining Disagreements"; the same sections of `debate-r2-variant-2.md` (Attention Ledger, opus:analyzer) plus its "Responses to Variant 1's Round 2 positions"; the same sections of `debate-r2-variant-3.md` (Decision Desk, haiku:backend) plus its "Responses to the other Round 2 positions". No Round 2 stance said "unchanged from Round 1" without restating it, so the Round 1 files were not needed.
- In the table, A = Signal Bridge (V1), B = Attention Ledger (V2), C = Decision Desk (V3), matching the diff-analysis columns.

## Per-Point Agreement

| Point | Level | V1 position (short) | V2 position (short) | V3 position (short) | Agreement (3/3, 2/3, none) | Winner approach | Winning variant(s) |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | Titled doc, numbered sections (V1) | Same (V1) | Same (V1) | 3/3 | H1 title plus numbered sections | V1 |
| S-002 | L1 | H3 per width, split Risks / UNVERIFIED (V2) | Same (V2) | Same (V2) | 3/3 | Depth-3 hierarchy with width and evidence subsections | V2 |
| S-003 | L1 | Shared 12-section order | Same | Same | 3/3 | Keep the shared 12-section sequence | V1+V2+V3 |
| S-004 | L1 | Tables for matrices, bullets for prose (V1+V2) | Same (V1+V2) | Same (V1+V2) | 3/3 | Tables for bounds, gates, matrices; bullets where prose is needed | V1+V2 |
| S-005 | L2 | Width matrix + x/width coords + C height contract, no per-panel scroll | Same | Same | 3/3 | A matrix, B coordinates, C 44-row height contract (drop order, min rows); per-panel scrolling deferred | V1+V2+V3 |
| S-006 | L2 | AC IDs with numbered tests (V2) | Same (V2) | Same (V2) | 3/3 | AC-n plus numbered tests; re-check mapping against #409 | V2 |
| S-007 | L2 | C named gates (4 samples each) in B table with fallback | Same | Same, plus split QUESTION-OBSERVATION from QUESTION-LINK | 3/3 | Gate-column table with fallback rule, gates in C vocabulary; V3's observation/link split is compatible | V3+V2 |
| S-008 | L2 | Only true owner choices + sample permission + content exposure | Same | Engineering verifies; owner grants capture/exposure, chooses among verified types | 3/3 | Short owner list of true choices: sample-capture permission, message-content exposure, choice among verified question types | V3+V2+V1 |
| S-009 | L1 | Risks apart from UNVERIFIED (V2) | Same (V2) | Same (V2) | 3/3 | Separate risks table and UNVERIFIED list | V2 |
| S-010 | L2 | A package + two seams + C single-flight atomic publication | Same, plus B renderer signature | Atomic publication, pure seams, generation guard | 3/3 | `observe` package, `SourceResult` and pure-view seams, one immutable atomically published view, monotonic generation; no plugin system | V1+V3 (+V2 signature) |
| S-011 | L1 | Plain self-weakness (V2) | Same (V2) | Same (V2) | 3/3 | Plainly stated own weakness | V2 |
| C-001 | L2 | A default R0-R1; B ledger default once R2 question gate passes; A as fleet view; C desk third view at R3 | Same (A R1 default with B gap line; B default after gate; C later) | A initial default; B-style preview before links; C preferred complete composition once links verify, not B default | 2/3 | A default while no question row is interpretable; B ledger default from first passed question-row gate; A one key away; C desk later behind explicit-link gate | V1+V2 (V3 dissents on post-link default) |
| C-002 | L2 | `check --all` per Run, retention, rotate Runs under C cap, `not read this cycle` disclosed | Same, plus A content-exposure default | Non-consuming all-rows reads, retention, fair rotation, one message call per cycle, exposure permission | 3/3 | `check --all --run` (not `--peek`) with observer retention, Runs rotated under one per-cycle cap, per-Run last-read age; messages per cycle open pending latency measurement | V2+V3 (+V1) |
| C-003 | L3 | `source UNVERIFIED, 0 rows interpreted, not "no questions"`, no number | Same | Same | 3/3 | Gap statement, no number in the question area | V2+V3 |
| C-004 | L2 | Verbatim ledger column/filter, never executed or called a question | Conceded; proxy panel withdrawn | Same | 3/3 | `nextAction.kind` as a verbatim ledger column and labelled filter, never executed, never a question | V1+V3 |
| C-005 | L2 | `COUNTS (source-reported)` at every width, no bars, never summed | Same | Same | 3/3 | Source-counts strip with scope and denominators at 160/116/80; no bars or health name; never summed with page counts | V1+V2+V3 |
| C-006 | L3 | 15 s interval, C caps, A backoff, per-call timeout measured | Same (10 s placeholder) | Same; no 2 s timeout without evidence | 3/3 | 15 s interval; 5 subprocesses, 8 MiB stdout, kill and reap; per-source backoff; per-call timeout set after one measured run | V2+V3+V1 |
| C-007 | L3 | Per-component clocks, visible conflicts, monotonic cycle | Same plus B `order unknown` | Same | 3/3 | C's independent clocks and visible equal-time conflicts plus A's monotonic cycle number | V3+V1 |
| C-008 | L3 | Four states + `n+? (k unknown)` | Same | Same | 3/3 | absent/null/valid/invalid per fact; `n+? (k unknown)` for aggregates | V3+V2 |
| C-009 | L3 | B `m` baseline + C first-observation baseline, "not reobserved" | Same | Same | 3/3 | Explicit `m` look marker, first observation is baseline, partial page means not reobserved | V2+V3 |
| C-010 | L3 | Retention from first live-question release; eviction makes total partial | Same (`n+? (k evicted, unresolved)`) | Same; adds 1,000-detail bound, bounded omitted-ID tracking, unknown total on overflow | 3/3 | Retain until explicit closure evidence; eviction never lowers the total; overflow notation (partial vs unknown) open | V2+V3 |
| C-011 | L3 | Source STALE from poll success; evidence plain age; per-row STALE withdrawn | Same | Same | 3/3 | Source STALE from collection success; evidence age shown separately, no row verdict | V2+V3 |
| C-012 | L2 | Hidden by default with count; linked evidence never hidden | Same, listed with `terminalState` when shown | Same | 3/3 | Historical rows hidden by default with disclosed count; explicitly linked historical evidence stays visible | V1+V3 |
| C-013 | L2 | `page.total (source)`, collected n / reported T | Same | Same | 3/3 | Source-reported denominator, not the fleet | V2+V3 |
| C-014 | L3 | At most 100 rows per read, not 100 questions; `no longer in source window` | Same | Same | 3/3 | 100-row cap wording plus retained-item window marker | V2+V3 |
| C-015 | L1 | A `/` and `h` plus B `m`; Tab focus deferred | Same | List/detail, filter, mark-looked; multi-panel input deferred | 3/3 | Up/Down, j/k, Enter, Esc, `/`, `h`, `m`, `e`, `q`; Tab panel focus deferred to spike | V1+V2 |
| C-016 | L1 | `>` | `>` | `>` | 3/3 | Trailing `>` marker; full value in detail/export | V1 |
| C-017 | L1 | ASCII-safe export, full IDs/caveats, `--ascii` | Same | ASCII-safe export with IDs, times, denominators, caveats, subject to exposure policy | 3/3 | ASCII-safe text export with full IDs and caveats; A's `--ascii` box replacement (V1, V2) | V1+V2 |
| C-018 | L2 | A Textual trigger + "do not build both first" | Same plus B screen fallback | Spike, else switch, no parallel builds | 3/3 | Rich after a passed spike; falsifiable Textual trigger; never build both | V1+V3 |
| C-019 | L1 | `superclaude observe`, owner names it | Owner names it, `observe` package | Short in-repo observer command | 3/3 | Short in-repo command such as `superclaude observe`; final name from owner | V1 |
| C-020 | L3 | Literal text, sanitizer in package, provenance first | Same, no prototype import | Same | 3/3 | Literal Rich text, own sanitizer, no prototype import | V3+V2 |
| C-021 | L2 | Recorded console + fake runner on golden sample; synthetic cannot clear live gates | Same | Same | 3/3 | Recorded-console harness, fake runner on redacted golden sample, synthetic passes never clear live gates | V1+V2+V3 |
| C-022 | L3 | `unavailable (no source)`; literal frozen stays frozen | Same | Same | 3/3 | No FROZEN number without a field; supplied frozen evidence stays frozen; missing is unknown, never unfrozen | V1+V3 |
| C-023 | L2 | `cost unavailable` / `cost: no source` | Same | Same | 3/3 | Show cost as unavailable, never `$0` | V3+V2 |
| C-024 | L2 | POSIX interactive, text export everywhere | Same, `--once` | Same | 3/3 | POSIX interactive plus `--once` text export on every platform | V2+V1 |
| C-025 | L2 | Stable worker order by run; questions oldest first, untimed last | Same | Same | 3/3 | Oldest verified question first, untimed last; stable worker rows grouped by run; selection anchored to ID | V3+V2+V1 |
| X-001 | L2 | Built layout keeps counts only under 116 (static read) | Same | Accepts A/B's reported static reads, no own render | 3/3 | Built Signal Bridge drops the counts line at 116; the merged design restores a strip at every width; render to confirm | V1 |
| X-002 | L3 | No message verb in R1 | Same | Same | 3/3 | R1 allow-list is `worker-list` only | V2+V3 |
| X-003 | L3 | No unread count from unverified `result.count` | Same | Same | 3/3 | No number from `result.count` until its meaning is verified | V2+V3 |
| X-004 | L3 | Use help-listed `--cursor` with repeat/missing guard and PARTIAL fallback | Same | Same, pinned by multi-page invocation evidence | 3/3 | `--cursor` from help, guard against repeated/missing cursor, fall back to pages read plus `PARTIAL`; record a two-page sample | V2+V3 |
| X-005 | L3 | Source namespace + `dispatchId` | Same | Same | 3/3 | Key by source namespace plus `dispatchId` | V3 |
| X-006 | L3 | No per-row threshold until cadence measured | Same | Same | 3/3 | No row STALE threshold; source STALE from poll success | V2+V3 |
| X-007 | L3 | One total per-cycle cap; R2 rotates Runs | Same, rotation bounded by measured message rate | One rotating message read per cycle within five-child ceiling | 3/3 | One total per-cycle subprocess cap; rotate message reads; expose per-scope ages; message calls per cycle open | V3+V2 |
| X-008 | L3 | Provenance first, no production prototype import | Same | Same | 3/3 | No production import of prototype code; provenance before any reuse | V2+V3 |
| X-009 | L2 | Engineering verifies type; owner picks among verified values | Same (only if more than one qualifies) | Same | 3/3 | Engineering verifies the type vocabulary from real rows; owner chooses among verified candidates | V3+V2 |
| X-010 | L2 | Hidden by default with count | Same | Same, linked evidence not suppressed | 3/3 | Historical rows hidden by default with count | V1 |
| X-011 | L2 | No verified SETTLED field; `unavailable` | Same | Same | 3/3 | SETTLED shows `unavailable` | V1 |
| X-012 | L2 | Question rows at R2 with `affected scope unknown`, links at R3 | Same | Same (QUESTION-OBSERVATION before QUESTION-LINK) | 3/3 | Retained question rows ship before links verify; affected scope shown unknown | V1+V2 |
| X-013 | L2 | Scrolling and Tab focus behind Textual switch rule | Same | Defer scrolling panes; richer interaction needs spike or Textual | 3/3 | Rich MVP has no per-panel scrolling or multi-pane focus; those wait for the spike or Textual | V1 |
| A-001 | L3 | QUALIFY: per-verb side-effect check at each gate | QUALIFY, same | QUALIFY, same | 3/3 | Only non-consuming is verified; check each admitted verb for side effects | V1+V2+V3 |
| A-002 | L3 | REJECT as premise; measure cadence first | REJECT, same | REJECT, same | 3/3 | No stale verdict rests on Orca timestamp cadence until measured | V1+V2+V3 |
| A-003 | L3 | QUALIFY: golden sample, envelope check, bounded stdout | QUALIFY, same | QUALIFY, same plus keep last-good data | 3/3 | Validate one complete JSON envelope, bound stdout, capture a real call before R1 | V1+V2+V3 |
| A-004 | L2 | QUALIFY: plus manual CJK/emoji terminal check | QUALIFY, same | QUALIFY, same | 3/3 | Recorded width tests plus one real-terminal wide-glyph check | V1+V2+V3 |
| A-005 | L3 | QUALIFY: R0 key-reader + `Live` spike | QUALIFY, same | QUALIFY, same | 3/3 | R0 spike of key reader with redraw, resize and restore; failure fires Textual rule | V1+V2+V3 |
| A-006 | L2 | QUALIFY: measure render time | QUALIFY, same | QUALIFY, same | 3/3 | Measure render time on 100-row fixture at 160 columns | V1+V2+V3 |
| A-007 | L2 | QUALIFY: detect non-UTF-8, reuse ASCII path | QUALIFY, same | QUALIFY: declare requirement, ASCII fallback | 3/3 | Non-UTF-8 terminals get the ASCII box path on screen | V1+V2+V3 |
| A-008 | L3 | QUALIFY: disclose per-process caps; prevention is owner choice | QUALIFY, same | REJECT premise; disclosure sufficient, no singleton (calls it mostly terminology) | 2/3 | QUALIFY: caps are per process and disclosed; preventing several observers is an owner decision | V1+V2 |

## Summary

- Agreed: 57 / 57 (55 at 3/3, 2 at 2/3: C-001 and A-008); score **1.00**.
- Unresolved points: none. The two majority points and the open parameters inside agreed points:
  - C-001 (2/3): V3 still prefers its Decision Desk as the complete composition once links verify; V1 and V2 make B's ledger the default after the question-row gate. All three agree A is the R1 default. Settled by a redacted `check --all --json` row showing (or not) an explicit `dispatchId` link, plus an owner walkthrough.
  - A-008 (2/3): verdict label only (V1, V2 QUALIFY; V3 REJECT). All three agree caps are per process, are disclosed, and no singleton service is built.
  - Open parameters inside agreed points (measurement or owner answer, not argument): per-call timeout (C-006); message calls per cycle under the total cap (C-002, X-007); retention overflow notation, partial count vs unknown total when omitted-ID tracking overflows (C-010); a two-page `--cursor` sample (X-004); a real render of `signal_bridge` at 116 (X-001); the R0 interaction spike result (X-013, A-005).
- Coverage of points debated: L1 = 10, L2 = 25, L3 = 22 (total 57; each level > 0).
- Threshold 0.75: **met** (1.00 >= 0.75).

## Emerging Consensus

**Default screen**
- R0-R1 default is A's worker ledger with the source-counts strip and B's one-line question-source gap notice on top (C-001; 3/3 on R1).
- From the first release whose question-row gate passes, B's attention ledger is the default and A's ledger is one key away as the fleet view; C's desk comes later behind the explicit-link gate (C-001; 2/3, V3 dissents on the post-link default). B's fallback rule (U-009) applies in both directions.
- `COUNTS (source-reported)` strip at 160, 116 and 80, numbers and denominators only, no bars or health name, never summed with page-derived counts (C-005, X-001). SETTLED and FROZEN show `unavailable (no source)` (X-011, C-022); cost shows unavailable, never `$0` (C-023).
- Historical rows hidden by default with a disclosed count; explicitly linked historical evidence never hidden (C-012, X-010).
- Label "run", never "orchestrator"; no human-owner join from `ownerDispatchId`.
- Layout: A's width matrix, B's x/width coordinates, C's 44-row height contract (drop order, minimum rows); no per-panel scrolling or multi-pane focus in the Rich MVP (S-005, X-013).
- Keys: Up/Down, j/k, Enter, Esc, `/`, `h`, `m`, `e`, `q`; truncation marker `>` (C-015, C-016).

**Data adapter**
- R1 allow-list: `worker-list --json --limit 100`, optional `--run`, `--cursor` with a repeated/missing-cursor guard falling back to pages read plus `PARTIAL`; no `--include-remote` until R4; no message verb (X-002, X-004).
- R2 message source: `check --all --run <runId> --json` (not `--peek`), Runs rotated under one total per-cycle subprocess cap, per-Run last-read age shown (C-002, X-007).
- Bounds: 15 s interval; at most 5 subprocesses, 8 MiB stdout per cycle, kill and reap on timeout; per-source backoff to 60 s; per-call timeout set after one measured `worker-list --limit 100` run (C-006).
- Identity key: source namespace plus `dispatchId` (X-005). Ordering: per-component clocks, visible equal-time conflicts, monotonic cycle number (C-007).
- Read-only guarantee: release-specific argv template allow-list with a never-shrinking forbidden set, replacing the static "`check` never appears" string test; a per-verb side-effect check at each gate (U-014, A-001).
- Parse one complete JSON envelope from bounded stdout; keep last-good data on failure (A-003).
- Sanitizer written in the observer package; external strings rendered as literal text, never Rich markup; no production import of prototype code (C-020, X-008).
- Decomposition: `observe` package with `SourceResult` and pure-view seams, one immutable view published atomically by a single-flight collector (S-010).

**Unknown handling**
- Four states per optional fact (absent, null, valid, invalid); aggregates with unknown members as `n+? (k unknown)` (C-008).
- Question area with no verified source: `source UNVERIFIED, 0 rows interpreted, not "no questions"`, no number; `SEEN IS NOT RESOLVED` reads `unknown (no question source)` (C-003).
- No unread count from `result.count` until its meaning is verified (X-003). `page.total` is labelled source-reported, "collected n unique / reported T" (C-013). 100-row cap is "at most 100 rows per read, not 100 questions" (C-014).
- Staleness: source STALE from poll success; evidence age shown as a plain age; no per-row STALE verdict until Orca's timestamp cadence is measured (C-011, X-006, A-002).
- `projection.nextAction.kind` is a verbatim ledger column and labelled filter, never executed, never called a question (C-004).

**Question retention and caps**
- Retain every observed question from the first live-question release until explicit closure evidence; seen is not resolved (C-010).
- Eviction never lowers the open total; it marks the count partial (`n+? (k evicted, unresolved)`). Proposed bound: 1,000 detail records with bounded omitted-ID tracking. Open: whether overflow of the omitted-ID tracking turns the total into unknown (V3) or stays partial (V1, V2).
- Question order: oldest verified creation time first, untimed last; worker rows in stable order grouped by run; selection anchored to ID, placeholder kept when the ID disappears (C-025).
- "Changes since last look": explicit `m` marker, first observation as baseline, partial-page rows "not reobserved" (C-009).

**Stack**
- Python Rich in this repository, POSIX interactive, `--once` ASCII-safe text export on every platform with full IDs, caveats and denominators, plus `--ascii` box replacement (C-017, C-024).
- R0 spike: raw-mode key reader with `Live` redraw, resize and restore. Failure, or a need for scrolling panes or multi-pane focus, fires the Textual switch; never build both (C-018, A-005, X-013).
- Non-UTF-8 terminals get the ASCII box path on screen (A-007); measure render time on the 100-row fixture at 160 columns (A-006).

**Build order**
- Release table with a Gate column and the fallback rule, gates named in C's vocabulary, each needing success, missing, stale and contradictory samples (S-007).
- R0 offline fixture and spike; R1 live worker-list only; R2 retained question rows with verified identity and type, affected scope shown as unknown (QUESTION-OBSERVATION); links and C's desk only after QUESTION-LINK (X-012); `--include-remote` at R4.

**Tests**
- AC IDs with numbered tests, mapping re-checked against #409 (S-006).
- Recorded-console harness (`Console(width=W, record=True, color_system=None)`), fake runner on a redacted golden `worker-list --json` sample with a shape contract test; synthetic passes never clear live gates (C-021, U-010).
- One real-terminal CJK/emoji/combining check alongside cell-width tests (A-004).

**Owner decisions**
- Only true owner choices: permission to capture one redacted `check --all --json` sample; message-content exposure (opt-in per terminal); which verified type values mean "a human must answer" (only if more than one qualifies); whether to prevent several observers per human (S-008, X-009, A-008, U-004, U-012).
- Engineering obligations, not owner votes: JSON shape, cursor syntax, join semantics, type vocabulary verification (X-009).
