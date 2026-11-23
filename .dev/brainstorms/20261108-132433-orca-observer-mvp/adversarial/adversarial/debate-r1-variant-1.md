# Advocate: Variant 1 (opus:architect) - A. Signal Bridge

## Position Summary

A. Signal Bridge is the right MVP **screen** because it is the only direction whose largest panel runs on the one fully verified, paged, non-consuming contract that exists today (`orca orchestration worker-list --json`, `result.page.total`, limit 1-100). B and C both centre the screen on human-question rows whose JSON fields are UNVERIFIED; until those rows are verified, their primary panel is an honest notice and little else (B's own words, variant-2 lines 107 and 113; C's own words, variant-3 lines 29-31 and 112).

The architecture argument matters more than the screen argument. Variant 1 defines the extension scaffolding the merge needs no matter which screen wins: one read-only adapter returning `SourceResult`, one immutable `Snapshot` built once with sanitizing and cell truncation, and views as pure functions of `(Snapshot, width)` (variant-1 lines 100-109). B's `attention` and C's `decision_desk` become extra views over the same snapshot at R2 and R3, so picking A first discards none of their work.

Where I move after reading B and C (stated up front, argued below):

- R1 should not call a message verb. I withdraw `check --peek --run <id>` from the R1 allow-list (X-002) and the `100+ unread` wording that relies on an unverified `result.count` meaning (X-003). R1 is worker-list only, as B and C propose. A's question panel then shows "Question source UNVERIFIED; 0 rows interpreted; not 'no questions'" (C-003, borrowing B's wording).
- Observer-side question retention ("seen is not resolved") is B's contract and should be in the merged design from R2 (C-010).
- C's identity key (source namespace plus `dispatchId`), separate clocks for liveness and evidence, and Rich-markup-as-literal rule are better than mine and should replace them (X-005, U-016, U-020).

What I keep: A as the default screen for R0-R1 with SIGNALS at every width as numbers with denominators (verified against the built code, see X-001), the package/seam decomposition (S-010), the monotonic cycle number (U-001), "run, never orchestrator" (U-006), historical rows hidden by default with a disclosed count, and a falsifiable stack switch rule. The recommended combination is **A screen + A seams for R0-R1, B retention and B question ledger as the second view at R2, C decision desk as the third view at R3, C's gate vocabulary and bounds as the release gates.** This is the mirror of B's own fallback rule (variant-2 line 130): same adapter, same renderer, the default screen is chosen by which contract is verified, not by preference.

## Steelman: Variant 2

The strongest form of B: issue #409's failure mode is not "the fleet is opaque", it is "a human question gets lost". B traces that to two mechanisms, recency ordering and read-equals-handled, and builds the screen against both (variant-2 lines 5, 13-15). Its evidence chain is the best argument in any of the three documents: `--peek` returns only unread messages, so once a coordinator runs plain `check` plus `--ack`, the question leaves the peek view even though nobody answered it. A panel built on `--peek` therefore resolves questions by reading them, which is the defect the issue describes. Only observer-side retention until explicit closure evidence fixes that, and B is the only variant that specifies it, including a cap with disclosure (variant-2 lines 84, 218) and a mechanical test that `m` never lowers the open count (T10-T12, line 180).

B is also the most disciplined about R1: one verb, a static test that `"check"`, `--ack` and `--wait` never appear in the adapter (T2, line 177), a redacted golden sample pinned by a contract test (T32, line 187), and a named owner action that unblocks the headline panel (decision 5, line 197). Its fallback rule (line 130) admits honestly that if the message contract never verifies, A is the better MVP, which makes B robust to being wrong. Read charitably, B's live R1 screen is not empty: it shows the freshness strip, a clearly labelled `WORKER-REPORTED NEXT ACTIONS (not questions)` proxy panel and the source counts line, which is a defensible day-one product.

## Steelman: Variant 3

The strongest form of C: the human's actual job is not to watch a fleet but to make one decision at a time, and the most dangerous thing an observer can do is put a persuasive but unjustified set of "affected sessions" beside a question. C makes the evidence boundary the product: an association edge needs explicit-link provenance, and a task ID, shared worktree, matching title or time proximity is not enough (variant-3 lines 196-199); an unknown link set never becomes an empty-but-complete set. That rule guards the issue's affected-scope criterion better than anything in A or B.

C is also the most precise on state mechanics: identity is source namespace plus `dispatchId` (line 202), which survives `--include-remote` where two hosts could reuse an ID; liveness and evidence are ordered by their own clocks and equal-time conflicts are shown as conflicts, not last-row-wins (lines 204-208); every optional fact has four states, absent, explicit null, valid and invalid (line 192); the per-cycle bound covers memory as well as time (8 MiB stdout, kill and reap, lines 219-220); and external strings are treated as literal text, not Rich markup (line 262), an injection path A and B do not name. Its named gate vocabulary (lines 125-148), each gate needing success, missing, stale and contradictory samples, is the most reusable release-gate scheme of the three. C also refuses to pass `--cursor` until its spelling is verified (line 51), which is the conservative reading of the evidence rules.

## Key Strengths Claimed (cite variant section and line ranges)

1. **The largest panel runs on verified data today.** Section 1 lines 5-6 and section 3 lines 40-56: every ledger, grouping, SIGNALS and header field maps to a `worker-list --json` field from Known Context; value vocabularies are printed verbatim with no good/bad colour because they are not enumerated (line 40). B concedes this point (variant-2 line 107) and C concedes it (variant-3 lines 108-112).
2. **Extension scaffolding that makes the combination cheap.** Section 7 lines 100-109 and 123: package `src/superclaude/cli/observe/` with `sources -> Snapshot -> View(snapshot, width) -> Live | export`; exactly two seams (`SourceResult` and a pure view function); sanitizing and cell truncation happen once at snapshot build, so no later view (B's `attention`, C's `decision_desk`) can forget them. No registry, no config, no abstract bases beyond the two signatures. B names the same seam idea without boundaries (variant-2 line 152); C names a collector and a published view but no package (variant-3 line 176).
3. **The SIGNALS discrepancy is resolved against the built code, not the brief.** Section 2 line 28. I re-read `layouts/group_a.py` `signal_bridge` (lines 59-81): the `>= 160` branch draws SIGNALS; the `>= 144` and `>= 116` branches draw request, sources and ledger with no counts; only the `< 116` branch prints `RUN n SETTLED n UNKNOWN n STALE n`. The seed brief's claim that 116 keeps the line is wrong, and B's line 108 repeats it in part. The same code defaults every bucket with `m.get(key, 0)`, which is the "unknown shown as 0" failure; variant 1 replaces it with `unavailable` (lines 30-34). (Static read only; no render was run.)
4. **Denominators everywhere, with scope names.** Section 4 lines 66-70: `PARTIAL 300 of 412 fetched`, global counts labelled with `scope.source`, filtered counts as `12 shown / 40 match filter / 300 fetched / 412 total`, historical rows `140 historical hidden (h)`.
5. **Guards against false fleet claims.** Line 54 and risk line 227: group by `runId`, label it "run", never "orchestrator"; `ownerDispatchId` is a dispatch ID, not a person (U-006).
6. **Out-of-order safety.** Line 169 and T8 (line 186): each snapshot carries a monotonic cycle number, so a slow call that finishes late cannot roll the screen back (U-001). Neither B nor C states this guard.
7. **Read-only enforced by templates that survive later releases.** Lines 154-161 and T17 (line 195): argument vectors are built only from templates, identifiers are character-checked, and the forbidden set is rejected before `subprocess` is reached. Unlike B's static "the string `check` never appears" test (variant-2 T2, line 177), this test does not have to be deleted at R2 when a message verb is added.
8. **Message-content exposure treated as an owner decision.** Line 161 and decision 6 (line 212): `check --all --terminal` is opt-in per terminal and never exported without a flag (U-004). B's R2 reads `check --all` for every Run with no such control.
9. **Falsifiable stack switch rule.** Section 8 lines 141-148: Rich now; move the view layer to Textual if scrolling panes, multi-pane focus or mouse become needed; Go through a versioned snapshot JSON so sources and sanitizer stay. The rule is concrete enough to fire (it fires on C's own slice, X-013).
10. **Traceable tests.** Section 10 lines 173-201: T1-T21, one per paraphrased criterion, all offline on a recorded console, covering the 8/80 base and the 5/8/10 x 50/80/100 grid at three widths (T2-T3).

## Weaknesses in Variant 2

1. **The R1 live screen is mostly a notice.** B says so itself (line 107: "The live Release 1 B screen is mostly an honest notice plus a proxy list"). The headline panel reads `0 rows interpreted`; the right column's big count has no live items to count. For an unknown period (B's whole plan hinges on owner decision 5, line 197) the user gets less than A on the same adapter.
2. **The proxy panel is built on an unverified value set and invites the misreading B fears.** `WORKER-REPORTED NEXT ACTIONS` ranks rows by oldest `lastObservedAt` (line 32), which ranks the stalest observation, not the most urgent need; the value set of `nextAction.kind` is UNVERIFIED (line 67). B lists "a user reads the proxy panel as questions" as a risk (line 213). Showing `nextAction.kind` verbatim in a ledger column, as A does, gives the same information without a panel whose position implies attention.
3. **Internal contradiction on SIGNALS.** B excludes SIGNALS bars because "settled" has no verified mapping (line 98), then says A's line "can be filled from `worker-list` today ... provided 'settled' is defined" (line 107). That proviso is the missing mapping; A's answer (`unavailable`) is the one consistent with B's own rule (X-011). B also says the 116- and 80-column builds "drop the SIGNALS panel" (line 108) while citing the 80-column line in the sentence before; the code keeps the line only below 116.
4. **R2 fan-out is not bounded by count.** `check --all --run <runId>` "for each Run seen in worker-list" (line 123) has no per-cycle Run cap; B's polling bounds (line 161, decision 10) cover pages only. With 10 Runs this is 13 calls per cycle, the same load B and C criticise in A.
5. **Read-only test that must be torn up.** T2's static test that `"check"` never appears in the adapter (line 177) is a good R1 guard but breaks by design at R2; template allow-lists (A's T17) carry forward.
6. **The question-type definition is placed with the wrong party.** Owner decision 6 (line 198) asks the owner what makes a human question; C is right that verifying the row shape and type field is an engineering obligation against Orca (variant-3 line 282). The owner can only choose among verified types.
7. **Identity and ordering are coarser than C's.** Dedup by `dispatchId` alone (line 163) and one combined timestamp rule share A's weakness under `--include-remote` (X-005).

## Weaknesses in Variant 3

1. **Two of three panels are unknown until two contracts verify.** In live mode the request reads "Question source UNVERIFIED" and the evidence panel "Affected scope unknown" (lines 29-30); the full desk needs QUESTION-LINK (line 134). C concedes A ships a more useful worker-only live view sooner (line 112). C's R1 "worker-only live evidence preview" (line 129) is a less developed Signal Bridge with no specified layout.
2. **The heaviest input surface on the weakest input stack.** Tab panel focus plus per-panel vertical scrolling under a 44-row contract (lines 16-25) is the hardest key-handling job of the three, proposed on Rich, which has no keyboard support. That is the case where the A-005 assumption is most likely to fail; under variant 1's switch rule it fires at R0 (X-013).
3. **Bounds are tight and unmeasured.** Two seconds per subprocess and ten seconds per cycle (line 219) are not grounded in any measured `worker-list` latency at 100 rows (UNVERIFIED); a slow but healthy Orca would read STALE on every cycle. After the message gate, "one selected source's non-consuming read per cycle" (line 217) leaves the rotation across 5-10 Runs unspecified, so per-Run question freshness is undefined.
4. **Over-conservative on `--cursor`.** C refuses continuation until the spelling is verified (line 51), so R1 is one page (100 rows) for a 287-row source. B read `--cursor` from `--help` today (variant-2 line 63). The right answer is a cheap R1 gate check, not a single-page MVP (X-004).
5. **Weaker traceability and no harness.** Acceptance rows have no IDs and the 14 additional obligations are unnumbered (lines 236-267); no rendering harness is named (C-021), so the merge cannot tell which test pins which rule.
6. **Default ordering by dispatch ID** (line 209) is stable but carries no meaning for a supervisor; grouping by Run (labelled "run") with stable order inside the group keeps the stability and adds orientation.

## Concessions (where B or C is honestly stronger)

1. **No message verb in R1 (B and C, X-002).** Variant 1 put `check --peek --run <id>` in R1 while its own risk table marks the meaning of `result.count` and the unbound-terminal call UNVERIFIED (variant-1 lines 222-223). I withdraw it: R1 is worker-list only, and the A question panel reads `Question source UNVERIFIED; 0 rows interpreted; this is not "no questions"`.
2. **`100+ unread` is withdrawn (X-003).** It interprets an unverified field. Unknown stays unknown.
3. **`--peek` is the wrong R2 verb (B, C-002).** B's evidence chain (variant-2 line 13) shows that peek drops a question once a coordinator reads it. R2 should read `check --all` per Run with observer-side retention, under a per-cycle call cap taken from C.
4. **"Seen is not resolved" retention (B, C-010).** Variant 1 had none. B's contract (retain until explicit closure evidence; no key, timer or source loss lowers the open count; disclosed cap) belongs in the merged model at R2, held in the Snapshot layer so every view inherits it.
5. **Identity, clocks and fact states (C, X-005, C-007, C-008).** Key rows by source namespace plus `dispatchId`; order liveness and evidence by their own clocks; show equal-time conflicts; four states per optional fact. Variant 1's monotonic cycle number stays as an additional guard.
6. **Sanitizer provenance and Rich markup (B and C, X-008, U-020).** `git log` shows `canvas.py` entered this repo in commit 495eb96d (2026-11-06, the #409 design package); that shows where it was committed, not that it was not derived from TUIBBS-scp. Reuse waits for confirmed provenance, and all external strings are passed to Rich as literal text, never markup.
7. **Bounding and contract pinning (B and C, U-010, U-017).** B's redacted golden worker-list sample with a shape test, and C's 8 MiB stdout cap with kill and reap, are better than anything in variant 1.
8. **Gate vocabulary (C, U-015).** Variant 1's release table should keep its Gate column but name gates with C's vocabulary and C's rule that each gate needs success, missing, stale and contradictory samples.
9. **Moment of decision (C) and queue review (B).** For answering one chosen question, C's desk is the better screen; for finding the oldest of many open questions, B's ledger is. A answers "what is happening across my fleet". That is why the combination adds B and C as views when their contracts verify, rather than claiming A covers their jobs.
10. **Cost slot (B and C, C-023).** An explicit `cost: unavailable` is a clearer disclosure than variant 1's "no slot at all".
11. **Stale threshold (C, X-006).** Tying STALE to 3 poll intervals made it 15 s at a 5 s interval, which will flag healthy rows if Orca updates timestamps less often (A-002). The threshold should be a separate owner-set value, set after the cadence is measured.

## Per-Point Stances

| ID | Level | Preferred variant | Confidence | One-line reason |
|---|---|---|---|---|
| S-001 | L1 | V1 | 0.6 | A titled document with numbered sections is easiest for the merge to cite; C's 12 H1s lose the title. |
| S-002 | L1 | V2 | 0.5 | B's H3 split (per width, risks vs UNVERIFIED) aids navigation; A's depth 2 is adequate but flatter. |
| S-003 | L1 | V1+V2+V3 | 0.9 | All three use the same 12-section order; no difference to resolve. |
| S-004 | L1 | V1 | 0.6 | Dense tables suit matrices (panels x widths, releases x gates); C's one-line prose hides structure. |
| S-005 | L2 | V1+V2 | 0.6 | A's panel-by-width matrix for review plus B's x/width coordinates for implementation; C's 44-row scroll contract is premature on Rich. |
| S-006 | L2 | V2 | 0.6 | B's AC-ID grouping with numbered tests is the best traceability; A's T1-T21 map into it; C's rows have no IDs. |
| S-007 | L2 | V1+V3 | 0.75 | Keep A's table with a Gate column, but name gates with C's vocabulary and its four-sample rule. |
| S-008 | L2 | V1+V3 | 0.6 | List only true owner choices (C's rule) but keep A's message-content exposure decision, which is genuinely the owner's. |
| S-009 | L1 | V2 | 0.55 | Separating risks from UNVERIFIED facts is clearer than A's single mixed table. |
| S-010 | L2 | V1 | 0.85 | Explicit package and exactly two seams make B and C cheap later views and keep sanitizing in one place. |
| S-011 | L1 | V1 | 0.5 | A checked each concession against built layouts; all three are honest, so stakes are low. |
| C-001 | L2 | V1+V2+V3 | 0.65 | A screen and seams for R0-R1; B ledger and retention as a second view at R2; C desk as a third view at R3; default screen follows verified contracts. |
| C-002 | L2 | V2+V3 | 0.7 | B shows `--peek` loses read-but-unanswered questions, so R2 uses `check --all` per Run with retention, under C's per-cycle call cap. |
| C-003 | L3 | V2+V3 | 0.75 | Before rows verify, say "source UNVERIFIED, 0 rows interpreted, not 'no questions'"; A's count line interprets an unverified field. |
| C-004 | L2 | V1 | 0.6 | Show `nextAction.kind` verbatim in the ledger; a panel ranked on an unverified value set invites the misreading B lists as a risk. |
| C-005 | L2 | V1+V3 | 0.7 | Keep SIGNALS numbers at every width, labelled source-reported with `scope.source` and never summed with page counts (C's rule). |
| C-006 | L3 | V1+V3 | 0.6 | Use C's total-calls-per-cycle and stdout caps with A's per-source backoff; exact timeouts and interval are unmeasured and owner-set. |
| C-007 | L3 | V3+V1 | 0.75 | C's namespace key and separate clocks with visible conflicts, plus A's monotonic cycle number against late results. |
| C-008 | L3 | V3 | 0.7 | UNKNOWN vs UNAVAILABLE and four states per fact subsume A's absent/empty split. |
| C-009 | L3 | V2+V3 | 0.6 | B's explicit `m` look marker with C's baseline and "not reobserved" rules beats A's implicit per-row seen marker. |
| C-010 | L3 | V2 | 0.85 | B's retention until explicit closure evidence is the only design that stops reading from resolving a question. |
| C-011 | L3 | V1+V3 | 0.6 | Keep A's per-row and per-source stale split, add C's "collection fresh / evidence stale" wording; threshold set after A-002 is measured. |
| C-012 | L2 | V1 | 0.6 | Hide historical rows by default with a disclosed count and toggle; counts unchanged, so nothing is concealed and the 80-column screen stays on live rows. |
| C-013 | L2 | V2+V3 | 0.7 | Label it `page.total (source)` and say "collected n unique / reported T"; whether it includes historical dispatches is UNVERIFIED. |
| C-014 | L3 | V2+V3 | 0.7 | "At most 100 message rows per read; coverage unknown" plus B's "no longer in source window"; A's unread wording is withdrawn. |
| C-015 | L1 | V1+V2 | 0.55 | A's `/` filter and `h` toggle are needed at 100 rows; add B's `m` look key. |
| C-016 | L1 | V1 | 0.4 | `>` reads as "continues"; either marker is fine if documented and tested. |
| C-017 | L1 | V1+V2 | 0.55 | ASCII-safe text export for all, with A's `--ascii` box replacement as the cheap path to the ASCII requirement. |
| C-018 | L2 | V1+V3 | 0.6 | A's concrete Textual trigger plus C's "do not build both first"; Go via the snapshot seam only if the owner funds it. |
| C-019 | L1 | V1 | 0.45 | Short `superclaude observe` in its own package; the final name is the owner's either way. |
| C-020 | L3 | V3+V2 | 0.75 | Strict sanitizer at snapshot build with A's enumerated classes, B's provenance precondition and C's Rich-markup-as-literal rule. |
| C-021 | L2 | V1+V2 | 0.7 | A's recorded-console harness plus B's fake runner on recorded JSON; adopt C's "synthetic passes cannot clear live gates". |
| C-022 | L3 | V1+V3 | 0.6 | FROZEN slot reads `unavailable` until a field exists; C's "literal frozen stays frozen" applies once one does. |
| C-023 | L2 | V3 | 0.55 | An explicit `cost unavailable` discloses better than no slot; concession against variant 1. |
| C-024 | L2 | V1+V2 | 0.65 | POSIX interactive, text export on every platform; A and B agree, B's `--once` names the path. |
| C-025 | L2 | V3+V1 | 0.55 | Stable order by default (C), grouped by run, missing ages last; A was silent and should not have been. |
| X-001 | L2 | V1 | 0.85 | Static read of `group_a.py` lines 59-81: the 116 and 144 branches print no counts; only below 116 keeps the RUN line; the seed brief is wrong (render not run). |
| X-002 | L3 | V2+V3 | 0.8 | Concede: no message verb in R1 while row schema, `result.count` meaning and unbound-terminal use are UNVERIFIED. |
| X-003 | L3 | V2+V3 | 0.85 | Concede: an unverified `result.count` must not be shown as an unread count. |
| X-004 | L3 | V1+V3 | 0.6 | Make "`--cursor` listed in `worker-list --help`" an R1 gate check; if it fails, one page plus PARTIAL (C's fallback). |
| X-005 | L3 | V3 | 0.8 | Source namespace plus `dispatchId` costs nothing and prevents cross-host merges under `--include-remote`. |
| X-006 | L3 | V3 | 0.55 | A fixed owner-set budget beats a multiple of the poll interval; all three values are unmeasured until A-002 is checked. |
| X-007 | L3 | V3 | 0.7 | A total per-cycle subprocess cap is the right shape; A's 13-call fan-out goes away with the R1 peek. |
| X-008 | L3 | V2 | 0.75 | Provenance must be confirmed before reuse; git history shows only that `canvas.py` was committed here in 495eb96d. |
| X-009 | L2 | V1+V3 | 0.7 | Identifying a human question is verified from real rows (engineering, A's R2 gate); the owner only chooses among verified types. |
| X-010 | L2 | V1 | 0.6 | Hidden with `140 historical hidden (h)` keeps the base screen on live rows without dropping any count. |
| X-011 | L2 | V1 | 0.8 | No verified field defines SETTLED; B's "provided settled is defined" is the missing mapping, and B's own line 98 excludes it. |
| X-012 | L2 | V1+V3 | 0.65 | Live question rows need verified identity and type first (C); affected scope may show unknown until links verify (C line 138, A's R3). |
| X-013 | L2 | V1 | 0.6 | Tab focus plus per-panel scrolling is exactly what Rich lacks; under A's rule C's slice needs Textual, which counts against C's slice on Rich. |
| A-001 | L3 | QUALIFY | 0.7 | Only "non-consuming" is verified; label other side effects UNVERIFIED and limit exposure by keeping R1 to `worker-list` only. |
| A-002 | L3 | QUALIFY | 0.75 | Measure Orca's timestamp cadence from recorded samples before fixing any STALE threshold; until then STALE means "older than X", not unhealthy. |
| A-003 | L3 | QUALIFY | 0.65 | Plausible but unproven; pin with the golden sample and a test that extra stdout lines yield `unparsable`, keeping last-known values. |
| A-004 | L2 | QUALIFY | 0.6 | Recorded-console tests prove Rich's model, not the terminal; add a manual CJK/emoji check in real terminals at R0 acceptance. |
| A-005 | L3 | QUALIFY | 0.7 | Run an R0 spike of the key reader alongside `Live` redraw with terminal restore; its failure is the Textual switch trigger. |
| A-006 | L2 | ACCEPT | 0.6 | 100-300 rows per refresh is low risk for Rich; record render time in R0 tests rather than budget it. |
| A-007 | L2 | QUALIFY | 0.55 | Detect a non-UTF-8 locale and reuse the `--ascii` box replacement on screen, which the export path already needs. |
| A-008 | L3 | QUALIFY | 0.65 | Caps are per process; disclose this in help and the header, and list "one observer per human" as an owner decision rather than build a cross-process lock. |
