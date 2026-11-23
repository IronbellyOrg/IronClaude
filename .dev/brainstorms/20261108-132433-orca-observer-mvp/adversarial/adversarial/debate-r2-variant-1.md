# Round 2 Rebuttal: Variant 1 (Signal Bridge)

## Rebuttals to Criticisms

Sources: B = `debate-r1-variant-2.md` ("Weaknesses in Variant 1", lines 56-63); C = `debate-r1-variant-3.md` ("Weaknesses in Variant 1", lines 31-35). V1 line numbers refer to `variant-1-opus-architect.md`. Five of the thirteen criticisms repeat points I already conceded in Round 1 (X-002, X-003, X-008, C-007, C-010); for those I say what is now scheduled, not argue again.

### B-1. The question panel rests on `--peek`, the verb that causes the defect, and retention is not scheduled (B line 56)

Steelman: the issue's failure is "read means handled". A panel fed by `--peek` shows a question only until someone acks it, so A's R1 screen would reproduce the defect, and a concession without a release slot is not a design.

Answer: conceded in Round 1 (my R1 lines 63-66); B is right that I did not give it a slot. It now has one. R1 calls no message verb. Observer-side retention is a Snapshot-layer rule from the **first release that shows a live question row** (R2), not a later view, so every view (A's question area, B's ledger, C's desk) inherits it. I add C's correction to B (C line 38): when the retention cap evicts an item, the unresolved total becomes `partial` or `n+? (k evicted)`; it is never lowered as if the item were closed.

### B-2. `100+ unread` shows a number whose meaning is UNVERIFIED (B line 57; C-1, C line 31)

Conceded in Round 1. Nothing to rebut. The R1 question area reads `Question source UNVERIFIED; 0 rows interpreted; this is not "no questions"`. T19 is deleted; its replacement asserts that no number appears in the question area while the message contract is UNVERIFIED.

### B-3 / C-3. R1 widens the allow-list and the load for count-only output (B line 58; C line 33)

Conceded in Round 1. R1 is now at most 3 `worker-list` calls per cycle. One correction to the record: the extra 10 calls bought nothing *because* the only thing they could show was a count of unknown meaning; that is the reason, not the load itself, and it is why a call cap returns at R2 when rows mean something.

### B-4. Recency bias stays on top: `_request` shows `qs[0]` (B line 59)

Steelman: with 5-10 orchestrators, which question takes the single slot depends on source order, which is UNVERIFIED. That moves the recency problem; it does not remove it.

Answer: correct about the built prototype, and I said so myself (V1 line 92). It has no effect on R1, where there are no question rows. It does constrain R2, and I accept B's rule there: when question rows are verified, the question area is ordered oldest first by verified creation time, untimed questions in their own last group (B's C-025), with C's `x/y other questions shown` line under it. The built `_request` is a visual reference only; the production question area is not `qs[0]`.

### B-5. Per-row STALE depends on an unstated Orca timestamp cadence (B line 60)

Steelman: if Orca refreshes `observedAt` less often than 15 s, every healthy row reads STALE, and the signal becomes noise exactly when the supervisor needs it.

Answer: conceded further than in Round 1. In Round 1 I only moved the threshold to an owner-set value (X-006). That still rests on A-002. I now withdraw the per-row `STALE` tag from R1 entirely. R1 shows source STALE from poll success (B, K8) and shows each row's evidence age as a plain age, `evidence 4m old`, with no verdict word (C's "collection fresh / evidence stale"). A per-row STALE verdict returns only after Orca's update cadence is measured from recorded samples.

### B-6. Dedup by `dispatchId` alone while `--include-remote` sits in the R1 template (B line 61)

Steelman: an allow-list that can produce `--include-remote` is an allow-list that can merge two hosts' rows under a key that may collide.

Answer: partly wrong on the facts, right on the remedy. V1 kept `--include-remote` off by default, with `scope: local only` in the header (V1 lines 54 and 226), so the merge was not reachable without an explicit opt-in. But an opt-in in R1 for a capability gated at R4 is scope I should not have offered. `--include-remote` leaves the R1 template; it returns at R4 with C's namespace key, which I adopted in Round 1 (X-005).

### B-7. No provenance gate on the `canvas.py` sanitizer (B line 62)

Conceded in Round 1. I go one step further with C (X-008): no production import of any prototype module. The sanitizer is written in the observer package against the enumerated classes in V1 line 171; `canvas.py` may be read as a reference only after its provenance is confirmed.

### B-8. SIGNALS has thin live content (B line 63)

Steelman: SETTLED and FROZEN read `unavailable`, TERMINAL is process accounting, and LIVENESS is a histogram of an unenumerated vocabulary. A panel whose headline buckets are empty, kept at every width, promises a fleet-health reading the data cannot give.

Answer: this is the strongest criticism of A and I accept most of it. What is left in the strip is not health; it is denominators and source-reported counts. That content is worth every width, because it is what the issue says must be disclosed (`16 of 287`, `scope bound`). The name and the bars are not. Revision: in the MVP the strip is titled `COUNTS (source-reported)`, it has no bars at any width, and the unfilled buckets collapse to one token, `settled, frozen: unavailable (no source)`, so they still show as unknown rather than vanishing (C-022). Where B and I still differ is only whether this line is kept at 116 columns; I keep it there because the built 116 branch drops the only denominator on the screen (X-001).

### C-2. Whole-row precedence can discard newer evidence; ties break by page order (C line 32)

Conceded in Round 1 (C-007). The model keeps liveness and evidence as separate components, each replaced only by a newer value on its own clock; an equal-time contradiction is shown as `conflict` and not resolved by page order. The monotonic cycle number stays as an additional guard against a late cycle.

### C-4. Missing fields and unexpected types map to one sentinel (C line 34)

Steelman: absent, explicit null and invalid are different contract failures; collapsing them hides source drift, which is the thing a golden-sample test is meant to catch.

Answer: correct, and V1 line 167 did collapse them into `Missing`. The model now carries four states per optional fact (absent, null, valid, invalid). The screen may still print `unknown` in a narrow cell, but detail shows which non-valid state it is, and an `invalid` value keeps its raw (sanitized) text in detail.

### C-5. Breadth is not affected scope (C line 35)

Steelman: at 100 workers, most ledger rows are unrelated to any question, and a supervisor may read proximity on the screen as relevance.

Answer: agreed on the principle, rejected as a weakness of the R1 screen. A never labels any subset of the ledger as "affected", and V1 line 231 already lists the noise as a design risk. The ledger answers a different, verified question: what state each fetched dispatch is in, and how much of the source was read. The rule I take from C is mechanical: no view may place a worker under a question, or highlight it beside one, without an explicit-link edge (U-019). Grouping by run is labelled "run", which makes no claim about any question.

### Answers to the rebuttals of my Round 1 criticisms

- **B's proxy panel (my R1 weakness 2).** B keeps it, titled `not questions` (B C-004). The title answers the misreading risk only partly: position on the screen still implies attention. I hold the verbatim ledger column as the R1 form and accept a labelled proxy list only as a filter of the ledger, not a headline panel (see Remaining Disagreements).
- **B's R2 fan-out (my R1 weakness 4).** B conceded a cap (B concession 6). Settled.
- **B on X-009.** B argues that choosing which verified message type means "a human must answer" is a product definition. That is fair if more than one verified type could qualify; it is the same split C now states (C line 54). I move to it.
- **B on X-012.** B says a retained, oldest-first question list is useful before affected-scope links exist, and C now agrees that individual questions with missing links show unknown scope (C X-012). This matches A's own R2/R3 split; I side with B against C's original "both contracts together".
- **C on X-001.** C calls the 116-column behaviour "disputed, not verified here". B independently read `layouts/group_a.py` lines 74-81 and reached the same reading as mine. Two static reads agree; no render was run by anyone, so the claim stays "static read" until the render in diff-analysis X-001 is done.
- **C on C-001.** C concedes that if the immediate requirement is a useful live screen before the question-link gate, V1 wins (C line 6). B concedes day-one live value (B concession 1). Both concessions are about R1; the real dispute is the default screen after R2, which I address under Revised Positions.

## Concessions Added in Round 2

New in this round (Round 1 concessions 1-11 stand and are not repeated):

1. **Default screen after R2 (C-001).** Once the R2 question-row gate passes, the default view should be B's attention ledger, with A's freshness strip as its header and A's Signal Bridge one key away as the fleet view. The issue's root cause is a lost human question; A is the better default only while no question row can be interpreted. This is B's own fallback rule (U-009) run in the other direction, on the same adapter and renderer.
2. **No per-row STALE verdict in R1 (B-5, X-006, A-002).** Source STALE from poll success; row evidence shown as an age only.
3. **SIGNALS is renamed and loses its bars (B-8, C-005).** `COUNTS (source-reported)`, numbers and denominators only; unfilled buckets as one `unavailable (no source)` token.
4. **`--include-remote` leaves the R1 allow-list (B-6).** Returns at R4 with the namespace key.
5. **Four-state facts replace V1's single `Missing` (C-4, C-008).** With B's aggregate notation `n+? (k unknown)` for counts that include unknown members.
6. **Retention eviction never lowers the unresolved total (C on B, C-010).** Eviction makes the total `partial`; only explicit closure evidence lowers it.
7. **Oldest-first question order at R2 (B-4, C-025).** The question area never takes `qs[0]` by source order.
8. **Poll interval default 15 s, not 5 s (C-006).** B and C both chose 15 s; my 5 s rested on no measured latency or cadence. Keep A's per-source backoff (U-005) and C's caps (5 subprocesses, 8 MiB stdout, kill and reap); the per-call timeout is owner-set after one measured `worker-list --limit 100` run.
9. **Cursor guard (X-004).** `--cursor` is listed in today's help (B), which shows the flag exists; C's rule to reject a repeated or missing `nextCursor`, falling back to the pages already read plus `PARTIAL`, is added to the R1 adapter.
10. **Height contract (S-005).** C's 44-row contract answers a real gap: which panel shrinks first on a short terminal. I adopt the contract (drop order and minimum rows per panel) but not per-panel scrolling, which stays behind the Textual switch rule.
11. **Engineering versus owner on question type (X-009).** Engineering verifies the type field and its values from real rows; the owner chooses which verified values mean "a human must answer" and grants permission to capture a redacted sample (B decision 5, U-012).
12. **No prototype import in production (X-008).** Stronger than Round 1's provenance gate.

## Revised Positions

What changed since Round 1, and why:

| Topic | Round 1 position | Round 2 position | Why it moved |
|---|---|---|---|
| Combination (C-001) | A screen and seams R0-R1; B ledger as a second view at R2; C desk as a third view at R3 | A screen and seams R0-R1; **B ledger becomes the default view** once the R2 question-row gate passes; A stays as the fleet view; C desk at R3 behind the explicit-link gate | B's root-cause argument holds once rows can be read; A's case was only ever "verified data today". Both rivals concede A for R1, so R1 is settled and the question was the default after R2. |
| Fleet strip (C-005, B-8) | SIGNALS panel at every width, bars optional | `COUNTS (source-reported)` strip at every width, no bars, unfilled buckets as one `unavailable` token | The headline buckets have no source; the name promised health the data cannot give. |
| Row staleness (C-011, X-006) | Per-row STALE at an owner-set threshold | No per-row STALE verdict until Orca's timestamp cadence is measured; source STALE from poll success; row evidence as a plain age | Any threshold still rested on A-002, which no one can check without recorded samples. |
| R1 allow-list | worker-list only (from Round 1), but template still allowed `--include-remote` | worker-list only, `--limit 100`, optional `--run`, `--cursor` with a repeat/missing guard; no `--include-remote` | Cross-host rows are an R4 capability. |
| Polling defaults (C-006) | 5 s interval, 10 s per call, 25 s per cycle | 15 s interval; C's subprocess and stdout caps; per-call timeout set after one measured run; A's per-source backoff kept | 5 s was not grounded; B and C agreed on 15 s. |
| Fact states (C-008) | `absent` versus `empty` | absent / null / valid / invalid, plus `n+? (k unknown)` for aggregates | C showed V1 line 167 collapsed three contract failures into one. |
| Question order at R2 (C-025) | Silent | Oldest first by verified creation time, untimed last, C's `x/y shown` line | B showed the built `qs[0]` slot is recency by another name. |
| Release order of rows and links (X-012) | Rows at R2, links at R3 (with C's identity-and-type precondition) | Same, now argued with B against C's original "both together": rows ship with `affected scope unknown` | C's Round 1 stance already moved to this. |
| Owner decisions (X-009, S-008) | Question identification is engineering only | Engineering verifies the type vocabulary; owner picks which verified values mean "human must answer" and grants sample-capture permission | B's distinction between verifying a field and defining a product term is correct. |
| Sanitizer (X-008) | Reuse `canvas.py` after provenance check | Write in the observer package; no production import of any prototype module | C's rule is stricter and costs nothing. |

What did not change: the package and two-seam decomposition (S-010), with C's single-flight atomic publication added; the monotonic cycle number (U-001); "run, never orchestrator" (U-006); historical rows hidden by default with a disclosed count (C-012, X-010; both rivals agreed); the message-content exposure opt-in (U-004); the falsifiable Textual switch rule (C-018, X-013); and the X-001 reading of the built layout.

## Updated Per-Point Stances

Levels copied from `diff-analysis.md`. "Changed?" is yes when the preferred variant or the substance of the stance moved from my Round 1 table; a confidence change alone is "no". For A-NNN rows the column holds ACCEPT / QUALIFY / REJECT on the assumption as written.

| ID | Level | Preferred variant | Confidence | Changed? | Reason |
|---|---|---|---|---|---|
| S-001 | L1 | V1 | 0.65 | no | All three advocates agree a titled document with numbered sections is easiest to cite. |
| S-002 | L1 | V2 | 0.55 | no | H3 per width and the split Risks / UNVERIFIED parts aid navigation; uncontested. |
| S-003 | L1 | V1+V2+V3 | 0.9 | no | Same 12-section order in all three. |
| S-004 | L1 | V1+V2 | 0.6 | yes | B's bullets where prose is needed plus A's tables for matrices; C concedes tables. |
| S-005 | L2 | V1+V2+V3 | 0.6 | yes | A's width matrix, B's x/width coordinates, and C's height contract (drop order, minimum rows) without per-panel scrolling. |
| S-006 | L2 | V2 | 0.7 | no | AC IDs with numbered tests; all three advocates agree. |
| S-007 | L2 | V3+V2 | 0.75 | yes | C's named gates with four samples each, in B's table with its fallback rule; A's Gate column is the same shape as B's. |
| S-008 | L2 | V3+V2+V1 | 0.65 | yes | Only true owner choices (C), plus B's sample-capture permission and A's message-content exposure decision. |
| S-009 | L1 | V2 | 0.6 | no | Risks kept apart from UNVERIFIED facts; uncontested. |
| S-010 | L2 | V1+V3 | 0.85 | yes | A's package and two seams, plus C's single-flight atomic publication of one immutable view; no plugin system. |
| S-011 | L1 | V2 | 0.5 | yes | B's plain self-weakness is the most useful form for a debate; A's checked concessions are a close second. |
| C-001 | L2 | V1+V2+V3 | 0.7 | yes | A screen R0-R1; B ledger becomes the default once R2 rows verify, A stays as fleet view; C desk at R3 behind the explicit-link gate. |
| C-002 | L2 | V2+V3 | 0.7 | no | `check --all` per Run (not `--peek`) with retention, under C's per-cycle call cap, rotating Runs with a disclosed `not read this cycle` count. |
| C-003 | L3 | V2+V3 | 0.8 | no | `source UNVERIFIED, 0 rows interpreted, not "no questions"`; no number in the area. |
| C-004 | L2 | V1+V3 | 0.55 | yes | `nextAction.kind` verbatim in the ledger and detail, never executed or called a question (C); a labelled proxy list only as a ledger filter, not a headline panel. |
| C-005 | L2 | V1+V2+V3 | 0.65 | yes | Source counts at every width with scope and denominators (A), no bars or health name (B), never summed with page counts (C). |
| C-006 | L3 | V2+V3 | 0.65 | yes | 15 s interval (B, C); C's subprocess, stdout and kill-and-reap caps; A's per-source backoff; per-call timeout set after a measured run. |
| C-007 | L3 | V3+V1 | 0.8 | no | Per-component clocks and visible equal-time conflicts, plus A's monotonic cycle number. |
| C-008 | L3 | V3+V2 | 0.75 | yes | Four states per fact (C) plus B's `n+? (k unknown)` aggregate notation; replaces V1's single `Missing`. |
| C-009 | L3 | V2+V3 | 0.65 | no | B's explicit `m` baseline with C's first-observation baseline and "not reobserved" rule. |
| C-010 | L3 | V2+V3 | 0.85 | yes | B's retention from the first live-question release; C's rule that eviction makes the total partial, never lower. |
| C-011 | L3 | V2+V3 | 0.7 | yes | Source STALE from poll success (B), evidence age as a separate statement (C); A's per-row STALE withdrawn until cadence is measured. |
| C-012 | L2 | V1+V3 | 0.65 | yes | Hidden by default with a disclosed count (A); never hide explicitly linked evidence for being historical (C). |
| C-013 | L2 | V2+V3 | 0.75 | no | `page.total (source)`; "collected n unique / reported T"; not the fleet. |
| C-014 | L3 | V2+V3 | 0.75 | no | At most 100 rows per read, not 100 questions; retained items show `no longer in source window`. |
| C-015 | L1 | V1+V2 | 0.55 | no | A's `/` and `h` plus B's `m`; C's Tab focus waits for the switch rule. |
| C-016 | L1 | V1 | 0.5 | no | `>` (B and C agree the glyph is secondary; B notes `~` occurs in paths). |
| C-017 | L1 | V1+V2 | 0.55 | no | ASCII-safe export with full IDs, caveats and denominators; A's `--ascii` box replacement. |
| C-018 | L2 | V1+V3 | 0.65 | no | A's concrete Textual trigger plus C's "do not build both first"; C now concedes the spike before committing to Rich. |
| C-019 | L1 | V1 | 0.45 | no | Short `superclaude observe`; owner names it. |
| C-020 | L3 | V3+V2 | 0.8 | no | Literal text, never Rich markup; sanitizer written in the package; provenance before any reference use. |
| C-021 | L2 | V1+V2 | 0.7 | no | Recorded-console harness plus B's fake runner on a redacted golden sample; C's "synthetic passes cannot clear live gates". |
| C-022 | L3 | V1+V3 | 0.65 | no | `unavailable (no source)` until a field exists; literal frozen evidence stays frozen. |
| C-023 | L2 | V3+V2 | 0.6 | yes | `cost unavailable` / `cost: no source`; both labels are the same disclosure, V1's absent slot is not. |
| C-024 | L2 | V1+V2 | 0.65 | no | POSIX interactive, text export everywhere; B's `--once` names the path. |
| C-025 | L2 | V3+V2+V1 | 0.65 | yes | Stable order for worker rows grouped by run (C, A); oldest-first verified age for questions, untimed last (B). |
| X-001 | L2 | V1 | 0.85 | no | Two independent static reads (A, B) agree: only the under-116 branch keeps the counts line; still unrendered. |
| X-002 | L3 | V2+V3 | 0.85 | no | No message verb in R1. |
| X-003 | L3 | V2+V3 | 0.9 | no | No unread count from an unverified `result.count`. |
| X-004 | L3 | V2+V3 | 0.65 | yes | Use `--cursor` as listed in today's help (B) with C's repeated/missing-cursor guard and PARTIAL fallback. |
| X-005 | L3 | V3 | 0.8 | no | Source namespace plus `dispatchId`. |
| X-006 | L3 | V2+V3 | 0.65 | yes | No per-row STALE threshold until cadence is measured; source STALE from poll success, evidence age shown separately. |
| X-007 | L3 | V3 | 0.75 | no | A total per-cycle subprocess cap; R1 needs at most 3 calls, R2 rotates Runs under the cap. |
| X-008 | L3 | V2+V3 | 0.8 | yes | Provenance first (B) and no production import of prototype code (C). |
| X-009 | L2 | V3+V2 | 0.65 | yes | Engineering verifies the type field from real rows; the owner chooses which verified values mean "human must answer". |
| X-010 | L2 | V1 | 0.65 | no | Hidden by default with a disclosed count; B concedes. |
| X-011 | L2 | V1 | 0.85 | no | No verified SETTLED field; B concedes. |
| X-012 | L2 | V1+V2 | 0.65 | yes | Question rows at R2 with verified identity and type, affected scope shown as unknown until links verify at R3. |
| X-013 | L2 | V1 | 0.65 | no | C's Tab focus and per-panel scrolling cross A's switch rule; C concedes the spike. |
| A-001 | L3 | QUALIFY | 0.7 | no | Only "non-consuming" is verified; R1's single verb limits exposure; a per-verb side-effect check joins each gate. |
| A-002 | L3 | REJECT | 0.75 | yes | Unverified as written, so no stale verdict may rest on it; measure cadence from recorded samples first. |
| A-003 | L3 | QUALIFY | 0.7 | no | Golden sample, envelope validation and bounded stdout; capture a real call's stdout before R1. |
| A-004 | L2 | QUALIFY | 0.6 | no | Recorded-console tests plus one manual real-terminal CJK/emoji check. |
| A-005 | L3 | QUALIFY | 0.7 | no | R0 spike of key reader with `Live` redraw, resize and restore; failure fires the Textual rule. |
| A-006 | L2 | QUALIFY | 0.6 | yes | Moved from ACCEPT: add a render-time measurement on the 100-row fixture at 160 columns, as B and C ask. |
| A-007 | L2 | QUALIFY | 0.55 | no | Detect a non-UTF-8 locale and reuse the ASCII box path on screen. |
| A-008 | L3 | QUALIFY | 0.65 | no | Caps are per process; disclose it; whether to prevent several observers is an owner decision. |

## Remaining Disagreements

| Point | My position | Contested by | The one fact that would settle it |
|---|---|---|---|
| C-001 default screen after R2 | B's ledger is the default once rows verify; C's desk is a third view at R3 | C (desk as the product) | Whether a real, redacted `check --all --json` row carries an explicit reference to a `dispatchId` (UNVERIFIED). If it does not, C's desk is mostly "affected scope unknown" and cannot be the default. |
| C-001 default screen at R1 | A is the default while no question row can be interpreted | B (B screen with a notice from R1) | Whether the R2 question-row gate can pass before R1 ships: if the owner-permitted sample (U-012) verifies the row shape first, the R1 default is moot and B is default from the first live release. |
| C-004 proxy panel | `nextAction.kind` as a ledger column and filter, not a headline panel | B (labelled proxy panel) | The value set of `projection.nextAction.kind` from a recorded sample (UNVERIFIED): if any value means "waiting on a human", a labelled panel earns its position; if none does, it is ranked noise. |
| C-005 / X-001 counts line at 116 columns | Keep the source-counts strip at every width | B (raw line, no strip at 116), C (calls the built behaviour disputed) | Render `layouts/group_a.py` `signal_bridge` at width 116 and search for `SETTLED`: absence confirms the built layout drops the only denominator at 116. |
| X-013 / S-005 per-panel scrolling and Tab focus on Rich | Height contract yes, scrolling and focus behind the Textual switch rule | C | The R0 spike result: a raw-mode key reader with `Live` redraw, resize and restore that handles Tab focus and per-panel scroll in a small, tested module, or does not. |
| C-002 / X-007 R2 message fan-out shape | `check --all` per Run, rotating Runs under C's per-cycle cap, with `not read this cycle` disclosed | B (every Run each cycle with a cap of 10), C (one selected source per cycle) | Measured wall time of one `check --all --run <id> --json` at 100 rows (UNVERIFIED): if 10 fit inside the cycle budget, B's every-Run read is affordable; if not, rotation is required. |
| C-006 per-call timeout | Owner-set after measurement; C's 2 s is too tight to adopt blind | C | Measured wall time of `worker-list --json --limit 100` on a 287-row source (UNVERIFIED). |
| A-008 several observers per human | QUALIFY: disclose per-process caps; prevention is an owner choice | C (REJECT) | Whether the owner expects more than one observer per human (an owner answer, not a technical one). |
| X-009 who defines "human question" | Engineering verifies types; owner chooses among verified values | C (engineering only, softened in R1) | Whether the verified message type vocabulary contains more than one value that could mean "a human must answer". If exactly one, there is nothing for the owner to choose. |
