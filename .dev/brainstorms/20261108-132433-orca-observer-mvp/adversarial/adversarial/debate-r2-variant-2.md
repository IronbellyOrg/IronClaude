# Round 2 Rebuttal: Variant 2 (Attention Ledger)

## Rebuttals to Criticisms

Sources: A = `debate-r1-variant-1.md` ("Weaknesses in Variant 2", lines 44-50); C = `debate-r1-variant-3.md` ("Weaknesses in Variant 2", lines 38-42); A-R2 = `debate-r2-variant-1.md`. V2 line numbers refer to `variant-2-opus-analyzer.md`. Three of the twelve criticisms repeat points I conceded in Round 1 (A-3 SIGNALS, A-4 fan-out cap, A-7 and C-3 identity and clocks); for those I say what is now scheduled. Nothing below claims a live Orca capability: message row fields, inbox JSON and `result.count` semantics stay UNVERIFIED, and no command was run for this round.

### A-1. The R1 live screen is mostly a notice (A line 44)

Steelman: until the message row contract verifies, B's largest panel reads `0 rows interpreted`, and the user gets less than A on the same adapter for a period whose length depends on one owner action (V2 decision 5).

Answer: conceded, and I now draw the conclusion I avoided in Round 1. The root-cause argument for B is about how questions are kept and ordered once they can be read. In R1 nothing can be read, so B's headline panel cannot help anyone find a question; it can only state that the source is missing. That statement does not need a 114-column panel. The R1 default screen is A's ledger with A's `COUNTS (source-reported)` strip, and B's gap statement as one fixed line at the top of the question area at every width: `Question rows: source contract UNVERIFIED. 0 rows interpreted. This is not "no questions".` B becomes the default view at the first release whose question-row gate passes, which A-R2 now accepts (A-R2 concession 1).

I also find a defect in my own R1 screen that neither rival named. In live R1, the `SEEN IS NOT RESOLVED` big count (V2 line 33) has no question source, so it would render `0`. That is the "unknown shown as zero" failure the brief forbids. In any release without a verified question source, that count reads `unknown (no question source)`, and the panel is not drawn on the R1 default screen.

### A-2. The proxy panel ranks on an unverified value set and invites the misreading it warns about (A line 45)

Steelman: ranking `WORKER-REPORTED NEXT ACTIONS` by oldest `lastObservedAt` ranks the stalest observation, not the most urgent need, and a panel placed where questions would go implies attention whatever its title says. B lists that misreading as its own risk (V2 line 213).

Answer: conceded. The ranking was the weak part: the oldest observation time measures how long since Orca last reported, which is closer to source staleness than to need, and with A-002 UNVERIFIED it is not even a reliable staleness measure. `projection.nextAction.kind` becomes a verbatim ledger column and a ledger filter, `nextAction present: k of n fetched (page.total T in source)`, labelled `worker-reported, not questions`. A separate panel returns only if a recorded sample shows a value of `nextAction.kind` that means "waiting on a human" (UNVERIFIED), which is the settling fact A-R2 names.

### A-3. Internal contradiction on SIGNALS, and imprecise X-001 wording (A line 46)

Conceded in Round 1 (X-011, X-001). A-R2's revision closes the remaining gap: a `COUNTS (source-reported)` strip with numbers and denominators, no bars and no health name, and `settled, frozen: unavailable (no source)` as one token. That is the raw `source counts:` line B proposed (V2 line 82) with A's denominators, so I now support keeping it at every width, including 116. On the built layout, two static reads (A's and mine) agree that only the under-116 branch of `layouts/group_a.py` `signal_bridge` keeps the counts line; nobody rendered it, so it stays a static reading.

### A-4. R2 fan-out is not bounded by count (A line 47)

Conceded in Round 1; the shape is now settled by a root-cause argument rather than by load alone. Retention changes what rotation costs. Once a question is observed, the observer keeps it, so a Run that is not read this cycle loses nothing already seen. What can be lost is a question that enters and leaves a Run's latest-100-row window between two reads of that Run. So the real bound is: rotation period per Run, times that Run's message rate, must stay under 100 rows. The message rate is UNVERIFIED. R2 therefore reads `check --all --run <runId> --json` for Runs in rotation under C's total per-cycle subprocess cap, shows each Run's `last read HH:MM` age and a `not read this cycle: k Runs` count, and treats the rate as a gate measurement, not an assumption. Whether `--run <id>` works from an unbound terminal, and which handle receives human-addressed messages, remain UNVERIFIED and part of the R2 gate.

### A-5. The static "`check` never appears" test must be deleted at R2 (A line 48)

Conceded. A string ban on `"check"` is a release-1 guard that breaks by design. Replace T2 with A's template test: argv is built only from a per-release allow-list of templates, and a forbidden set (`--ack`, `--wait`, `--retry-request`, plain `check` without `--peek` or `--all`, any write verb) is rejected before `subprocess` is reached. The forbidden set never shrinks, so that test never has to be removed.

### A-6. Question-type definition placed with the owner (A line 49)

Partly conceded; A-R2 and C have both moved to the split I argued for. Engineering verifies the type field and its value set from real, redacted rows. The owner chooses which verified values mean "a human must answer", and grants permission to capture the sample. If the verified vocabulary has exactly one candidate value, there is nothing for the owner to choose, and that part of V2 decision 6 is deleted.

### A-7 / C-3. Identity and ordering are coarser than C's (A line 50; C line 40)

Conceded in Round 1. The model keys rows by source namespace plus `dispatchId`, keeps liveness and evidence as separate components on their own clocks, shows equal-time contradictions as `conflict`, keeps `order unknown` for untimed rows, and adds A's monotonic cycle number.

### C-1. Retention needs an honest count after eviction (C line 38)

Steelman: disclosing `older retained items dropped: k` (V2 line 218) is not enough if the big open count then falls, because a falling count reads as closure.

Answer: conceded; this was a real gap in V2. The open count may be lowered only by explicit closure evidence. When the cap evicts an item, the count reads `n+? (k evicted, unresolved)`, and the panel title gains `partial`. The evicted items' stable IDs stay in a compact list (ID and first-seen time only) so the export still names them. If even that list hits its bound, the count becomes `unknown (retention exceeded)`.

### C-2. `acting owner: resource.ownerDispatchId` risks a false human join (C line 39)

Conceded. `ownerDispatchId` is a dispatch ID, not a person. The RETAIN CONTEXT line becomes `owner dispatch: <id> (worker-list)` and a separate `human owner: unknown (no source)`. The same rule applies to "requesting orchestrator": it becomes `requesting run` (A's U-006), because the Run-to-orchestrator mapping is not established.

### C-4. Successful polling does not refresh old evidence (C line 41)

Conceded in Round 1 (concession 10 to C). Source freshness and evidence age are two statements: `worker-list OK 4s` in the strip, and each row's `evidence 6m old` as a plain age with no verdict word. A-R2 has withdrawn per-row STALE on the same grounds (A-R2 concession 2), so this point is settled.

### C-5. Selection can drift to a different decision (C line 42)

Steelman: when the selected row disappears, V2 moves the cursor to the next row (V2 line 26). A human reading evidence for one question is then silently looking at another, and on a partial page the "disappearance" may only be non-observation.

Answer: conceded. The cursor stays on a placeholder for the same ID: `selected <id> not in latest read (last seen HH:MM)`, and the inspector keeps the last-known detail qualified `as of HH:MM:SS`. The cursor moves only on a key press. For a retained question the placeholder is unnecessary, because the question itself stays listed.

### Responses to Variant 1's Round 2 positions

- **Default screen (A-R2 concession 1, C-001).** Accepted as stated: A default while no question row can be interpreted; B default once the R2 gate passes; A one key away as the fleet view. A-R2's settling fact is also right: if the owner-permitted sample verifies the row shape before R1 ships, B is the default from the first live release.
- **Proxy panel (A-R2 Remaining Disagreements).** Settled by my concession under A-2.
- **Counts at 116 (A-R2 C-005, X-001).** Settled: the strip is the raw source-counts line with denominators, at every width.
- **Per-row STALE withdrawn, 15 s interval, measured per-call timeout (A-R2 concessions 2 and 8).** These match B's K8 and B's interval; agreed. I keep B's 10 s per-call timeout only as a placeholder until the one measured `worker-list --limit 100` run.
- **R2 fan-out (A-R2 C-002, X-007).** A-R2 records B as "every Run each cycle with a cap of 10". After the argument under A-4, I move to A-R2's rotation under C's cap, with the rotation period bounded by the measured message rate.
- **Retention in the Snapshot layer from the first live-question release; eviction never lowers the total (A-R2 B-1, concession 6).** Agreed; it is B's contract with C's correction.
- **Historical rows hidden by default, message-content exposure opt-in (U-004), no prototype import in production (X-008).** Agreed; the first two were Round 1 concessions, the third is stricter than my provenance gate and costs nothing.
- **X-012.** A-R2 sides with B: question rows ship at R2 with `affected scope unknown`, links later. Agreed.
- **A-002 REJECT.** I move from QUALIFY to REJECT in the same sense A-R2 and C use: the assumption is not shown false, but no verdict may rest on it until the cadence is measured.

## Concessions Added in Round 2

New in this round (Round 1 concessions to A 1-8 and to C 1-10 stand and are not repeated):

1. **R1 default screen is A (C-001).** B's headline panel has no content until a question source verifies, so A's ledger and source-counts strip are the R1 default, with B's gap line fixed at the top. B is the default from the first release whose question-row gate passes.
2. **No zero for an absent question source.** The `SEEN IS NOT RESOLVED` count reads `unknown (no question source)` in any release without one; it is not drawn on the R1 screen. This corrects a defect in V2 line 33.
3. **Proxy panel withdrawn (C-004).** `nextAction.kind` is a verbatim ledger column and a labelled filter, not a panel ranked by observation age.
4. **Counts line at every width (C-005, X-001).** The source-counts strip, numbers and denominators only, stays at 160, 116 and 80.
5. **R2 reads rotate across Runs under one per-cycle cap (C-002, X-007).** The rotation period is bounded by each Run's measured message rate against the 100-row window; per-Run `last read` ages are shown.
6. **Template allow-list replaces the "`check` never appears" string test (U-014, A-5).** The forbidden set never shrinks.
7. **Eviction never lowers the open count (C-010, C-1).** `n+? (k evicted, unresolved)`, panel marked `partial`.
8. **No human-owner join from `ownerDispatchId`, and "run", never "orchestrator" (C-2, U-006).**
9. **Selection holds a placeholder for a missing ID (C-5).** The cursor never retargets on its own.
10. **Height contract adopted without per-panel scrolling (S-005, X-013).** A-R2's reading: which panel shrinks first and each panel's minimum rows, as in C; scrolling stays behind A's Textual switch rule.
11. **C's single-flight atomic publication joins A's two seams (S-010).**
12. **A-002 moves to REJECT** as a design premise.

## Revised Positions

| Topic | Round 1 position | Round 2 position | Why it moved |
|---|---|---|---|
| Combination (C-001) | B screen from R0, A's freshness strip and full ledger in a second list, C's `x/y` line | A screen at R0-R1 with B's gap line on top; **B default from the first release whose question-row gate passes**; A one key away as fleet view; C desk later behind the explicit-link gate | The root cause is about keeping and ordering readable questions; with no readable question, B's panel only states a gap, which one line does as well. |
| R1 question count | `SEEN IS NOT RESOLVED` big count drawn in live R1 | `unknown (no question source)`, not drawn on the R1 screen | With no source it would render `0`, the failure the brief forbids. |
| Proxy (C-004) | Separate panel ranked by oldest `lastObservedAt` | Ledger column plus `nextAction present: k of n fetched` filter, labelled `not questions` | Observation age ranks staleness, not need, and the value set is UNVERIFIED. |
| Counts (C-005) | Raw `result.counts` line, no SIGNALS | Same line as A's `COUNTS (source-reported)` strip at every width, no bars | A-R2 dropped the bars and health name, so the two positions are now the same. |
| R2 message reads (C-002, X-007) | `check --all --run` for every Run each cycle (cap conceded in Round 1) | Rotate Runs under one per-cycle subprocess cap; per-Run `last read` age; rotation period bounded by measured message rate versus the 100-row window | Retention makes an unread Run lose only questions that pass through its window between reads, so the rate, not the Run count, is the binding quantity. |
| Read-only test (U-014) | Static string ban on `"check"`, `--ack`, `--wait` | Template allow-list plus a never-shrinking forbidden set | The string ban breaks by design at R2. |
| Retention cap (C-010) | Cap with `older retained items dropped: k` | Eviction makes the count `n+? (k evicted, unresolved)` and the panel `partial`; only closure evidence lowers it | A dropping count reads as closure. |
| Owner labels | `acting owner: resource.ownerDispatchId`, "requesting orchestrator" | `owner dispatch: <id>`, `human owner: unknown (no source)`, `requesting run` | A dispatch ID is not a person; Run-to-orchestrator is not established. |
| Selection | Moves to the next row when the ID disappears | Placeholder for the same ID, last-known detail `as of` | Silent retargeting during inspection is a wrong-decision risk. |
| Question type (X-009) | Owner or Orca defines it | Engineering verifies the value set; owner chooses among verified values only if more than one qualifies | All three advocates converged on this split. |
| STALE (C-011, X-006, A-002) | Source STALE from poll success; QUALIFY on A-002 | Unchanged design; A-002 moved to REJECT as a premise | No row verdict may rest on an unmeasured cadence. |

What did not change: retention until explicit closure evidence (C-010); oldest-first order for verified questions, untimed last (C-025); the one-verb R1 allow-list (X-002); no number from an unverified `result.count` (X-003); the redacted golden `worker-list` sample with its shape test (U-010); the owner action to capture one redacted `check --all --json` sample (U-012); the fallback rule (U-009), now read in both directions; and the explicit `m` look marker (U-011).

## Updated Per-Point Stances

Levels copied from `diff-analysis.md`. "Changed?" is yes when the preferred variant or the substance of the stance moved from my Round 1 table; a confidence change alone is "no". For A-NNN rows the column holds ACCEPT / QUALIFY / REJECT on the assumption as written.

| ID | Level | Preferred variant | Confidence | Changed? | Reason |
|---|---|---|---|---|---|
| S-001 | L1 | V1 | 0.65 | no | All three advocates agree a titled document with numbered sections is easiest to cite. |
| S-002 | L1 | V2 | 0.55 | no | H3 per width and a split Risks / UNVERIFIED part keep detail findable; uncontested. |
| S-003 | L1 | V1+V2+V3 | 0.9 | no | Same 12-section order in all three. |
| S-004 | L1 | V1+V2 | 0.6 | no | Tables for matrices, bounds and gates; C concedes tables. |
| S-005 | L2 | V1+V2+V3 | 0.6 | yes | A's width matrix for review, B's x/width coordinates for building, C's height contract without per-panel scrolling. |
| S-006 | L2 | V2 | 0.7 | no | AC IDs with numbered tests; all three advocates agree; mapping still to be re-checked against #409. |
| S-007 | L2 | V2+V3 | 0.75 | no | Table with a gate column and the fallback rule, gates named in C's vocabulary with four samples each. |
| S-008 | L2 | V3+V2+V1 | 0.65 | yes | Only true owner choices (C), plus B's sample-capture permission and A's message-content exposure decision. |
| S-009 | L1 | V2 | 0.6 | no | Risks kept apart from UNVERIFIED facts. |
| S-010 | L2 | V1+V2+V3 | 0.7 | yes | A's package and two seams, B's pure renderer signature, C's single-flight atomic publication; no plugin system. |
| S-011 | L1 | V2 | 0.5 | no | A plainly stated self-weakness is the most useful form for a debate. |
| C-001 | L2 | V1+V2+V3 | 0.7 | yes | A default at R0-R1 with B's gap line; B default from the first passed question-row gate; C desk later behind explicit links. |
| C-002 | L2 | V2+V3+V1 | 0.65 | yes | `check --all` per Run (not `--peek`) with retention, rotating Runs under C's cap, A's content-exposure default. |
| C-003 | L3 | V2 | 0.8 | no | `0 rows interpreted. This is not "no questions"`, with no number in the area; A and C now agree. |
| C-004 | L2 | V1+V3 | 0.6 | yes | Conceded: verbatim ledger column and labelled filter (A), never executed or called a question (C); proxy panel withdrawn. |
| C-005 | L2 | V1+V2+V3 | 0.7 | yes | Source counts at every width with denominators (A), no bars or health name (B), never summed with page counts (C). |
| C-006 | L3 | V2+V3+V1 | 0.6 | yes | 15 s interval; C's subprocess, stdout and kill-and-reap caps; A's per-source backoff; per-call timeout after a measured run. |
| C-007 | L3 | V3+V1+V2 | 0.75 | yes | C's per-component clocks and visible conflicts, A's monotonic cycle number, B's `order unknown` flag. |
| C-008 | L3 | V3+V2 | 0.7 | no | Four states per fact plus `n+? (k unknown)` for aggregates. |
| C-009 | L3 | V2+V3 | 0.65 | no | B's explicit `m` baseline with C's first-observation baseline and "not reobserved" rule. |
| C-010 | L3 | V2+V3 | 0.85 | yes | B's retention until closure evidence, plus C's rule that eviction marks the count partial and never lowers it. |
| C-011 | L3 | V2+V3 | 0.7 | no | Source STALE from poll success, evidence age as a separate plain age; A withdrew per-row STALE. |
| C-012 | L2 | V1+V2+V3 | 0.6 | yes | Hidden by default with a count (A), listed with `terminalState` when shown (B), never hide linked evidence for being historical (C). |
| C-013 | L2 | V2+V3 | 0.75 | no | `page.total (source)`, "collected n unique / reported T"; whether it counts historical rows is UNVERIFIED. |
| C-014 | L3 | V2+V3 | 0.7 | no | At most 100 rows per read, not 100 questions; retained items show `no longer in source window`. |
| C-015 | L1 | V2+V1 | 0.55 | no | B's `m` is required; A's `/` and `h` are cheap; C's Tab focus waits for the switch rule. |
| C-016 | L1 | V1 | 0.55 | no | `>` is clearer than `~`, which occurs in paths. |
| C-017 | L1 | V2+V1 | 0.5 | no | ASCII-safe export with full IDs, caveats and denominators; A's `--ascii` box replacement. |
| C-018 | L2 | V1+V3+V2 | 0.6 | yes | A's concrete Textual trigger, C's "do not build both first", B's fallback between default screens. |
| C-019 | L1 | V1+V2 | 0.45 | no | Owner names it; `observe` package either way. |
| C-020 | L3 | V3+V2 | 0.8 | no | Literal text, never Rich markup; sanitizer written in the package; no prototype import; provenance first. |
| C-021 | L2 | V2+V1+V3 | 0.7 | yes | B's fake runner on a redacted golden sample, A's recorded-console harness, C's "synthetic passes cannot clear live gates". |
| C-022 | L3 | V1+V3 | 0.6 | no | `unavailable (no source)` in live mode; literal frozen evidence stays frozen. |
| C-023 | L2 | V2+V3 | 0.6 | no | `cost: no source` / "cost unavailable" are the same disclosure; never `$0`. |
| C-024 | L2 | V2 | 0.6 | no | POSIX interactive plus `--once` text export everywhere; A agrees. |
| C-025 | L2 | V2+V3+V1 | 0.65 | yes | Oldest-first verified age for questions, untimed last (B); stable order for worker rows grouped by run (C, A). |
| X-001 | L2 | V1 | 0.85 | no | Two independent static reads agree only the under-116 branch keeps the counts line; still unrendered. |
| X-002 | L3 | V2 | 0.85 | no | No message verb in R1; A and C agree. |
| X-003 | L3 | V2 | 0.9 | no | No unread count from an unverified `result.count`; A withdrew it. |
| X-004 | L3 | V2+V3 | 0.65 | no | `--cursor` is listed in today's help; add C's repeated/missing-cursor guard with PARTIAL fallback. |
| X-005 | L3 | V3 | 0.8 | no | Source namespace plus `dispatchId`. |
| X-006 | L3 | V2+V3 | 0.7 | no | No per-row threshold until cadence is measured; source STALE from poll success. |
| X-007 | L3 | V3+V2 | 0.7 | yes | One total per-cycle cap; R1 needs at most 3 calls; R2 rotates Runs, bounded by measured message rate. |
| X-008 | L3 | V2+V3 | 0.8 | no | Provenance first; no production import of any prototype module. |
| X-009 | L2 | V3+V2 | 0.7 | yes | Engineering verifies the type value set; the owner chooses among verified values only if more than one qualifies. |
| X-010 | L2 | V1 | 0.65 | no | Hidden by default with a disclosed count. |
| X-011 | L2 | V1 | 0.85 | no | No verified SETTLED field; `unavailable` is the only honest value. |
| X-012 | L2 | V2 | 0.7 | no | Question rows ship with `affected scope unknown`; links later; A and C now agree. |
| X-013 | L2 | V1+V2 | 0.6 | no | B's single-list screen avoids multi-pane focus; A's switch rule governs any later scrolling panes. |
| A-001 | L3 | QUALIFY | 0.7 | no | Only "non-consuming" is verified; one R1 verb limits exposure; a per-verb side-effect check joins each gate. |
| A-002 | L3 | REJECT | 0.75 | yes | Not shown false, but UNVERIFIED as written, so no stale verdict may rest on it until cadence is measured. |
| A-003 | L3 | QUALIFY | 0.7 | no | Golden sample, envelope validation, bounded stdout; capture one real call's stdout before R1. |
| A-004 | L2 | QUALIFY | 0.6 | no | `cell_len` tests plus one manual real-terminal CJK/emoji check. |
| A-005 | L3 | QUALIFY | 0.7 | no | R0 spike of key reader with `Live` redraw, resize and restore; failure fires the Textual rule. |
| A-006 | L2 | QUALIFY | 0.55 | no | Add a render-time measurement on the 100-row fixture at 160 columns. |
| A-007 | L2 | QUALIFY | 0.55 | no | Detect a non-UTF-8 locale and reuse the ASCII box path on screen. |
| A-008 | L3 | QUALIFY | 0.65 | no | Caps are per process; disclose it; preventing several observers is an owner decision. |

## Remaining Disagreements

With A, the disagreements of Round 1 are now settled; what remains is mostly with C, and each item is settled by a measurement or an owner answer, not by argument.

| Point | My position | Contested by | The one fact that would settle it |
|---|---|---|---|
| C-001 default screen after R2 | B's ledger is the default once question rows verify; C's desk is a later view behind the explicit-link gate | C (desk as the product) | Whether a real, redacted `check --all --json` row carries an explicit reference to a `dispatchId` (UNVERIFIED). Without it, C's desk is mostly `affected scope unknown` and cannot be the default. |
| C-001 R1 default | A by default, unless the R2 gate passes before R1 ships | none (agreed with A-R2) | Whether the owner-permitted sample (U-012) verifies the row shape before R1 ships. |
| C-025 / C default selection | The first question shown is the oldest open one by verified creation time | C (selected request, stable dispatch order by default) | None technical: #409's failure is a lost old question, so the default must surface the oldest; C's stable order stays right for evidence rows. |
| X-007 R2 read shape | Rotate all Runs under one per-cycle cap, per-Run `last read` age shown | C (one selected source per cycle) | Measured per-Run message rate against the 100-row window, and measured wall time of one `check --all --run <id> --json` (both UNVERIFIED). If a Run can pass 100 rows within one rotation period, rotation must be faster or the gap disclosed as `coverage unknown`. |
| C-006 per-call timeout | Owner-set after one measured run; 10 s placeholder | C (2 s) | Measured wall time of `worker-list --json --limit 100` on a 287-row source (UNVERIFIED). |
| X-004 continuation | Use `--cursor` as listed in help, with C's guard | C (verify spelling first) | One recorded two-page `worker-list` sample in the golden set; until then R1 falls back to one page plus `PARTIAL` if the second call fails. |
| X-009 who defines "human question" | Engineering verifies; owner chooses only among verified values | C (engineering only, softened) | Whether the verified message type vocabulary has more than one value that could mean "a human must answer". |
| A-008 several observers | QUALIFY: disclose per-process caps; prevention is an owner choice | C (REJECT) | Whether the owner expects more than one observer per human. |
| X-013 Tab focus and per-panel scrolling on Rich | Height contract yes; scrolling and focus behind the Textual rule | C | The R0 spike result for a raw-mode key reader with `Live` redraw, resize and restore. |
