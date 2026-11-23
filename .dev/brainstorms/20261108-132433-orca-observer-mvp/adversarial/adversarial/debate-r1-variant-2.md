# Advocate: Variant 2 (opus:analyzer) - B. Attention Ledger

## Position Summary

B (Attention Ledger) should be the MVP screen, with A's source-freshness strip as its header and C's `x/y shown` overflow line. The argument rests on the root cause of #409, not on which panel is easiest to fill today.

1. **Root cause.** A human question gets lost because chat is ordered by recency and because reading a message is treated as handling it. B is the only direction that makes this failure its primary object: open questions oldest first, and "seen is not resolved" as a rule the count cannot break (V2 §1, lines 5-15; §4, line 84).
2. **The verified help text forces retention.** `check --peek` returns only unread messages (Known Context). Once a coordinator runs plain `check` and `--ack`, the question leaves the peek view whether or not the human answered it. A panel built on `--peek` therefore "resolves" questions when they are read, which is the defect #409 describes. Only observer-side retention until explicit closure evidence avoids this. B specifies that retention; A has none in the MVP (C-010), and C adopts the rule but schedules B-style aging for its Release 3 (V3 lines 141-143).
3. **Honest degradation.** All three need the same UNVERIFIED message row contract for their headline panel. B's live R1 headline states the gap: `Question rows: source contract UNVERIFIED. 0 rows interpreted. This is not "no questions".` (V2 line 31). A fills the same slot with a count whose meaning is UNVERIFIED (X-003). C replaces its whole purpose with "Question source UNVERIFIED".
4. **Smallest trust surface.** B's R0 and R1 run exactly one verb, `worker-list --json` (V2 §9, line 157). No message verb enters the allow-list until its row contract is pinned by a recorded sample (X-002).
5. **A planned exit.** If the message contract never verifies, B says so and falls back to A's screen on the same adapter and renderer by an owner-set deadline (V2 line 130, U-009).

Where B is weak, this debate concedes it: A's live R1 screen shows more today; C's identity key, clock ordering and markup rule are stronger; B's R2 per-Run fan-out has no cap. Those are imported into B below, not argued away.

## Steelman: Variant 1

The strongest case for A (Signal Bridge), stated as its advocate would:

- **Every large panel runs on a verified contract today.** The session ledger, SIGNALS strip and source-freshness panel are all fed by `worker-list --json`, whose fields and paging are verified (V1 §1, lines 5-6; §3, lines 42-52). On day one a supervisor sees the fleet, its denominators and which sources are stale. B's live R1 is mostly a notice plus a proxy list.
- **It shows what nobody asked about.** Stale and unknown workers that no question mentions are visible in A and hidden by design in B and C (V1 line 96). A silent failure in a worker with no open question is still a thing the human must see.
- **Its architecture keeps every option open.** One immutable `Snapshot`, two seams (`SourceResult`, a pure view function), and B and C as later views over the same snapshot (V1 §7, lines 100-109). Choosing A first discards none of B's or C's work.
- **It resolves the PLAN-versus-built discrepancy, and it is right about the build.** I read `layouts/group_a.py` lines 56-82: the `>= 116` and `>= 144` branches draw no counts at all, and only the `< 116` branch keeps the `RUN n SETTLED n UNKNOWN n STALE n` line. A's description (V1 line 28) is exact; the seed brief's "116 and 80 both collapse to one line" is wrong for 116. A then chooses the PLAN's intent and keeps numbers and denominators at every width.
- **Precise safety details.** A monotonic cycle number so a late call cannot roll the screen back (U-001), "run, never orchestrator" (U-006), per-source backoff (U-005), and the only explicit owner decision about message-content exposure from `check --all --terminal` (U-004).

## Steelman: Variant 3

The strongest case for C (Decision Desk), stated as its advocate would:

- **It answers the moment that matters.** When the human is about to answer one question, C shows that question beside only the sessions it affects, so the supervisor reads evidence, not fleet noise (V3 lines 9-14, 119-121). A whole-fleet slice at 100 workers is mostly unrelated rows; a ranked list still leaves the human to gather evidence by hand.
- **It refuses to invent the one link B and A both later need.** An association edge needs explicit-link provenance; a task ID, shared worktree, title match or time proximity is not enough, and an unknown link set never becomes an empty-but-complete set (V3 lines 196-199, U-019). That rule protects the affected-scope criterion better than either rival.
- **Its state mechanics are the most precise.** Identity is source namespace plus `dispatchId` (V3 line 202, X-005), so `--include-remote` cannot merge two hosts' rows. Liveness and evidence are ordered by their own clocks, equal-time conflicts are shown, and future skew never gives a negative age (V3 lines 204-208, U-016). Each optional fact has four states: absent, explicit null, valid, invalid (V3 line 192, U-018).
- **Its bounds are the tightest.** At most five subprocesses, two seconds each, ten seconds and 8 MiB of stdout per cycle, with kill-and-reap and coalesced manual refresh (V3 lines 216-220, U-017). It alone treats external strings as literal text, not Rich markup (V3 line 262, U-020), which closes a Rich-specific injection path.
- **It does not claim an unverified flag.** The continuation argument must be verified before use; without it, collect one page and disclose PARTIAL (V3 lines 51, 131, X-004).
- **Its gate vocabulary is reusable.** OFFLINE-FIXTURE through COMPLETE-MESSAGE-ENUMERATION, each needing success, missing, stale and contradictory samples (V3 lines 125-148, U-015).

## Key Strengths Claimed (cite variant section and line ranges)

All citations are to `variant-2-opus-analyzer.md` (V2).

| # | Strength | Where | Why it matters |
|---|---|---|---|
| K1 | Evidence chain from verified help text to the design: `--peek` shows only unread rows, so a peek-based panel resolves questions on read; only `--all` keeps read rows, capped at 100 | §1 "Evidence chain", lines 11-15 | Derives retention from a verified fact instead of from taste. Neither A nor C states this chain. |
| K2 | "Seen is not resolved" made mechanical: `m` marks looked, the big open count never drops; only explicit closure evidence can lower it, and none exists in the MVP | §2 lines 33, 44-46; §4 line 84; T10-T12 lines 180 | Testable form of the issue's core rule (U-011). |
| K3 | Observer-side retention with `no longer in source window (last seen HH:MM)` and a disclosed 1,000-item cap | §4 line 83; §12 line 218 | The only design that survives the 100-row cap and source loss without dropping a question silently (C-010, C-014). |
| K4 | One-verb R1 allow-list, plus a static test that `--ack`, `"check"` and `--wait` never appear in the adapter | §9 lines 157-160; T1-T3 line 177 | Smallest read-only surface of the three (X-002, U-014). |
| K5 | Golden redacted `worker-list --json` sample with a contract test: missing `result.page` gives `FAILED (shape)`, missing inner field gives `unknown` | §7 line 122; T32 line 187 | Pins the only verified source against drift (U-010) and partly answers A-003. |
| K6 | Honest live empty state and a separately labelled proxy panel, `WORKER-REPORTED NEXT ACTIONS (not questions)`, ranked `by oldest observation, NOT question age`, untimed rows in their own group | §2 lines 31-32; §4 line 85; T9 line 179 | Gives the live screen content before R2 without calling anything a question (U-008). |
| K7 | Counter notation `n+? (k unknown)` so a count with an unknown member never reads as a clean number | §4 line 78 | Applies "unknown is never zero" to aggregates, not only to fields (C-008). |
| K8 | Per-source STALE based on the last successful poll, not on Orca timestamp cadence | §4 line 80; §9 line 165 | Does not depend on the unstated A-002 assumption, so a healthy fleet cannot read STALE everywhere. |
| K9 | R2 gate names the exact evidence needed (a non-empty `check --all` row with ID, type, sender, recipient, creation time, body) and the owner action that unblocks it (permission to capture one redacted sample) | §7 line 123; §11 lines 197-198 | Turns the shared blocker into a named action (U-012, U-013). |
| K10 | Fallback rule: miss the R2 deadline, switch the default screen to A on the same adapter and renderer | §6 line 113; §7 line 130; §11 line 204 | Bounds the cost of being wrong about B to one layout function (U-009). |
| K11 | Self-critique stated plainly: if the message contract never verifies, B becomes "A with different labels" | §6 line 113 | The proposal does not overclaim. |

## Weaknesses in Variant 1

1. **The question panel rests on the verb that causes the defect.** A's R1 question source is `check --peek --run <runId>` (V1 lines 50, 114, 158). Per verified help, peek returns only unread rows. Once a coordinator acks, the question leaves A's count even if no human answered. A has no retention in the MVP (V1 line 77; C-010), so A's screen reproduces the "read means handled" failure #409 names. A concedes B's retention contract is the right one (V1 line 93) but does not schedule it.
2. **It displays a number whose meaning it lists as UNVERIFIED.** `100+ unread (cap reached; older rows not visible)` (V1 line 68, T19 line 197) treats `result.count` as an unread total, while A's own risk table says "total unread or rows returned" is UNVERIFIED (V1 line 222). Showing `100+ unread` before that test passes is a fact claim, not a disclosure (X-003).
3. **R1 widens the allow-list and the load before any row is verified.** Up to 3 pages plus 10 peeks every 5 s, 13 subprocesses per cycle (V1 lines 163-165; X-007). The peek output can only be shown as a count of unknown meaning, so the extra load buys little. Whether `--peek --run <id>` works from an unbound terminal is itself UNVERIFIED (V1 line 223).
4. **Recency bias stays on top.** The built `_request` shows one question (`qs[0]`) plus a count (V1 line 92). With 5-10 orchestrators, which question wins the slot depends on source order, which is not verified. That is the recency problem in a new place.
5. **STALE per row depends on an unstated cadence.** A row is STALE when `observedAt` or `lastObservedAt` is older than 3 intervals at 5 s, so 15 s (V1 line 64; X-006). If Orca refreshes those timestamps less often (A-002, UNVERIFIED), every healthy row reads STALE.
6. **Dedup by `dispatchId` alone while offering `--include-remote` in the R1 allow-list template** (V1 line 157, line 169). If two hosts can return the same `dispatchId` (UNVERIFIED), rows merge (X-005). B shares the key weakness but keeps `--include-remote` out of the MVP (V2 line 99).
7. **Missing provenance gate on the sanitizer.** "Base it on the stricter prototype `canvas.py` `sanitize`" with no provenance check (V1 line 171; X-008). The trust-boundary code would rest on an unconfirmed source. Note also that the prototype layouts use `m.get(key, 0)` (`layouts/group_a.py` lines 68, 80), which renders missing counts as `0`; the prototype is a visual reference only, and A says so (V1 line 230).
8. **Fleet SIGNALS has thin live content.** SETTLED and FROZEN print `unavailable` (V1 line 34); the remaining TERMINAL line is `result.counts` (process accounting) and a verdict histogram of unknown vocabulary. That is a panel whose headline buckets are absent, kept at every width.

## Weaknesses in Variant 3

1. **The MVP is not live until two unverified contracts arrive together.** C's first complete live product (Release 2) needs question identity and explicit affected-dispatch references at once (V3 lines 134-139; X-012). Before that, the live screen is "Question source UNVERIFIED" and "Affected scope unknown" (V3 lines 28-31). C calls this honest, and it is, but it means C's own direction delivers nothing distinctive until both gates pass.
2. **Retention is deferred, so "seen is not resolved" is unenforced when questions first go live.** C adopts the invariant (V3 line 116) but places B-style aging and resolution in Release 3 (V3 line 142). Its Release 2 lists "one selected source's non-consuming read per cycle" (V3 line 217). If the source is a peek, the same read-means-handled failure applies. Its test "empty peek does not clear an observed question" (V3 line 258) needs retention that Release 2 does not specify.
3. **One message source per cycle leaves most questions unobserved.** With 5-10 Runs, "other question scopes remain unobserved" (V3 line 218). The "other observed questions x/y" denominator then describes one scope, which makes the bounded panel less informative than its label suggests.
4. **Default selection still depends on source order.** The built `decision_desk` selects `requests[0]` by default (as V2 line 111 reads the prototype), and C's default display order is "stable dispatch ID order unless the human selects an age sort" (V3 line 209). V3 names no age-first default for questions, so the oldest question is not guaranteed to be shown first. The oldest open question is the one most likely to be lost (#409 root cause).
5. **Bounds may be too tight for the verified source, with no evidence either way.** Two seconds per subprocess (V3 line 219) is not tested against a real `worker-list` page of 100 rows; UNVERIFIED. A failing bound shows STALE on a healthy fleet.
6. **Owner-decision list omits decisions that only the owner can make.** C folds "what identifies a human question" into engineering (V3 line 282; X-009). Verifying a field is engineering; deciding which Orca message type means "a human must answer" is a product definition if several types exist. C also omits the permission to capture message bodies, which may hold sensitive content (V2 line 197).
7. **Format.** Twelve unnumbered H1 headings, no title and prose-only build order and risks (S-001, S-004, S-009) are harder to cite and merge.

## Concessions (where A or C is honestly stronger)

Each concession names what B should import.

**To A (Signal Bridge):**

1. **Day-one live value.** A's live R1 shows more verified data than B's. B already borrows A's freshness strip; B should also show A's ledger of all fetched workers (not only those with `nextAction.kind`) in the inspector or a second list, so stale and unknown workers nobody asked about stay visible.
2. **X-001 facts.** I checked `layouts/group_a.py` lines 56-82. A's account is exact: the 116 and 144 branches draw no counts; only the under-116 branch keeps the counts line. B's wording ("116- and 80-column builds also drop the SIGNALS panel", V2 line 108) is true of the panel but omits that 80 keeps a line. A is the more precise source on this point.
3. **X-011.** B said SETTLED could be filled "provided 'settled' is defined" (V2 line 107). No verified definition exists, so A's `unavailable` is correct and B's conditional is not a live option.
4. **Monotonic cycle number** (U-001), **`run`, never `orchestrator`** (U-006), **per-source backoff** (U-005): B should adopt all three. B's no-overlap rule (V2 line 161) prevents most rollbacks but does not name the guard.
5. **Message-content exposure as an owner decision** (U-004). B's R2 reads `check --all` bodies on screen and in export. A's "off by default, never in export without a flag" is the safer default and should govern B's R2.
6. **Bounded R2 fan-out.** B's R2 reads `check --all --run <runId>` "for each Run seen in worker-list" (V2 line 123) with no cap. That is unbounded per-Run fan-out. B should take A's cap of 10 Runs with `not read (cap 10)` disclosure, or C's per-cycle subprocess cap with round-robin across Runs.
7. **Historical rows hidden by default with a count** (X-010). At 287 total versus a live fleet of 50-100, A's `140 historical hidden (h)` gives a quieter 80-column screen; B's T21 rule (listed with `terminalState`, never active) still applies when shown.
8. **Package layout** (S-010, U-002). A's concrete `cli/observe/` tree and `SourceResult` seam are more buildable than B's two named seams.

**To C (Decision Desk):**

1. **Identity key** (X-005). Source namespace plus `dispatchId` costs nothing and removes a merge risk B cannot rule out. Adopt.
2. **Ordering** (C-007, U-016). Ordering liveness and evidence by their own clocks, showing equal-time conflicts, and never a negative age is more precise than B's single "newer timestamp wins". Adopt, keeping B's `order unknown` flag for untimed rows.
3. **Four-state optional facts** (C-008, U-018) and **unknown enum values stay unknown labels**. Adopt; B's `n+? (k unknown)` remains the aggregate form.
4. **Literal text, not Rich markup** (C-020, U-020). B's sanitizer strips control bytes but never says that square-bracket markup in worker text must not be interpreted. Adopt as a test.
5. **Memory and process bounds** (U-017): 8 MiB stdout cap, kill and reap on timeout, coalesced manual refresh. Adopt alongside B's 10 s per-call timeout.
6. **Cursor guard** (X-004). B and A read `--cursor` from `--help` (V2 line 63), which verifies the flag exists, not that a repeated or missing cursor is handled. C's "reject repeated/missing cursors" (V3 line 221) should be added.
7. **Affected-scope provenance** (U-019). When B reaches R4 (decision inspector), C's explicit-link rule governs it.
8. **Named gate vocabulary** (U-015) with success, missing, stale and contradictory samples per gate. B's release table should use these names.
9. **Policy-frozen in live mode** (C-022). B hides the word in live mode (V2 line 87). A slot reading `unavailable (no source)` discloses the gap better than silence.
10. **"Collection fresh / evidence stale"** (C-011). B's per-source STALE is right, but evidence age should be shown next to it as a separate statement, as C does.

## Per-Point Stances

Levels are copied from `diff-analysis.md`. Confidence is this advocate's confidence that the stated preference is right after the concessions above.

| ID | Level | Preferred variant | Confidence | One-line reason |
|---|---|---|---|---|
| S-001 | L1 | V1 | 0.6 | A titled H1 with numbered H2 sections is easiest to cite in the merge; B is equivalent, C has no title. |
| S-002 | L1 | V2 | 0.5 | One H3 per width and a split Risks/UNVERIFIED part keep detail findable; depth 3 is enough. |
| S-003 | L1 | V1+V2+V3 | 0.9 | All three share the same 12-section order; nothing to choose. |
| S-004 | L1 | V1+V2 | 0.55 | Tables carry denominators and gates better than C's one-line prose; A is densest, B mixes bullets where prose is needed. |
| S-005 | L2 | V2+V3 | 0.55 | B's x/width coordinates (`right = width - 43`) are buildable; C's 44-row height contract fills a gap no one else covers. |
| S-006 | L2 | V2 | 0.65 | AC IDs plus a separate Contract row (T32) make traceability and source drift testable; still to be re-checked against #409 text. |
| S-007 | L2 | V2+V3 | 0.7 | B's table with a gate column and fallback rule, using C's named gate vocabulary for each row. |
| S-008 | L2 | V2+V3 | 0.55 | B's list covers real owner calls (message-capture permission, fallback deadline); C's note correctly moves pure verification out of it. |
| S-009 | L1 | V2 | 0.6 | Separating risks from UNVERIFIED items stops an unknown being read as a managed risk. |
| S-010 | L2 | V1+V2 | 0.65 | A's concrete `cli/observe/` tree and `SourceResult` seam plus B's pure `(model, width, color) -> list[str]` renderer. |
| S-011 | L1 | V2 | 0.5 | B ends with its own weakness stated plainly, the most useful form for a debate. |
| C-001 | L2 | V2 | 0.65 | B screen + A freshness strip (and A's full ledger in a second list) + C's x/y line; root cause is lost questions, not fleet state. |
| C-002 | L2 | V2+V1 | 0.6 | `check --all --run` keeps read rows (peek does not), but needs A's per-Run cap and A's content-exposure default. |
| C-003 | L3 | V2 | 0.75 | `0 rows interpreted. This is not "no questions"` states the gap without a number of unknown meaning. |
| C-004 | L2 | V2+V3 | 0.6 | Proxy panel is useful live content if titled `not questions`; C's "never execute `nextAction.kind`" guard applies. |
| C-005 | L2 | V2+V3 | 0.7 | Raw `result.counts` labelled source-reported with `scope.source`, never summed with page counts; no bars without a settled mapping. |
| C-006 | L3 | V2+V3 | 0.55 | B's 15 s / 3 pages / 10 s per call, plus C's 8 MiB cap, kill-and-reap and coalesced refresh; C's 2 s per call is untested. |
| C-007 | L3 | V3+V2 | 0.65 | C's per-clock ordering and visible equal-time conflicts, keeping B's `order unknown` flag for untimed rows. |
| C-008 | L3 | V3+V2 | 0.6 | C's four states per optional fact plus B's `n+? (k unknown)` aggregate notation. |
| C-009 | L3 | V2+V3 | 0.65 | B's explicit `m` snapshot makes the change set user-defined; C's "first observation is baseline" and "not reobserved" rules close edge cases. |
| C-010 | L3 | V2 | 0.8 | Peek drops acked rows, so only observer-side retention until closure evidence prevents read-means-handled; A and C both concede the rule. |
| C-011 | L3 | V2+V3 | 0.6 | Per-source STALE from last successful poll (B), with evidence age shown separately as "collection fresh / evidence stale" (C). |
| C-012 | L2 | V1+V2 | 0.6 | Hidden by default with a disclosed count (A); when shown, listed with `terminalState` and never counted active (B). |
| C-013 | L2 | V2+V3 | 0.7 | Label `page.total (source)` and never call it workers or the fleet; whether it counts historical rows is UNVERIFIED. |
| C-014 | L3 | V2+V3 | 0.65 | `latest <=100 rows per Run observed` plus C's "100 rows are not 100 questions"; retained items show `no longer in source window`. |
| C-015 | L1 | V2+V1 | 0.5 | B's `m` is required for seen-is-not-resolved; A's `/` filter and `h` toggle are cheap and support C-012. |
| C-016 | L1 | V1 | 0.55 | `~` occurs in paths and could read as part of an identifier; `>` is a clearer ASCII truncation marker. |
| C-017 | L1 | V2+V1 | 0.5 | ASCII-safe text by default (B), with A's `--ascii` box replacement for the screen-like export. |
| C-018 | L2 | V2+V3 | 0.6 | Rich now; Textual only on a measured key-reader failure; Go only if the owner funds it; B's fallback to A's layout covers the contract risk. |
| C-019 | L1 | V1+V2 | 0.45 | Owner choice; A's `observe` package is concrete, B's `orca observe` name scopes it; either is fine. |
| C-020 | L3 | V3+V2 | 0.75 | Treat external strings as literal text, not Rich markup (C), and reuse `canvas.py` logic only after provenance is confirmed (B). |
| C-021 | L2 | V2 | 0.7 | Fake runner on a recorded, redacted golden sample tests the adapter as well as the renderer; mapping still needs a #409 re-check. |
| C-022 | L3 | V1+V3 | 0.6 | Live mode should show a frozen slot as `unavailable (no source)`, not omit the word as B does; literal frozen evidence stays frozen. |
| C-023 | L2 | V2+V3 | 0.55 | An explicit `cost: no source` / "cost unavailable" discloses the gap; A's absent slot hides that cost was considered. |
| C-024 | L2 | V2 | 0.6 | POSIX interactive plus `--once` text export everywhere; same substance as A, C is silent. |
| C-025 | L2 | V2 | 0.7 | Oldest-first questions target the root cause; selection is keyed by ID, so reordering does not move the cursor. |
| X-001 | L2 | V1 | 0.85 | `layouts/group_a.py` lines 74-81: the 116 branch draws no counts, only the under-116 branch keeps the line; A's account is exact. |
| X-002 | L3 | V2 | 0.8 | No message verb in R1: peek output can only be a count of UNVERIFIED meaning, and it widens the allow-list and load. |
| X-003 | L3 | V2 | 0.85 | `result.count` meaning is UNVERIFIED in A's own risk table; showing `100+ unread` before the test is a fact claim. |
| X-004 | L3 | V2+V3 | 0.6 | `--cursor` is listed in today's help, so use it (B), with C's guard against repeated or missing cursors and one-page fallback. |
| X-005 | L3 | V3 | 0.75 | Source namespace plus `dispatchId` is free and removes a cross-host merge risk that is UNVERIFIED either way. |
| X-006 | L3 | V2+V3 | 0.65 | STALE from poll success does not rest on Orca's timestamp cadence (A-002); evidence age shown separately as C does. |
| X-007 | L3 | V2+V3 | 0.6 | B's R1 needs at most 3 calls; take C's stdout cap and reap; A's 13 calls per cycle are not justified by count-only output. |
| X-008 | L3 | V2+V3 | 0.7 | Write the sanitizer in the observer package; use `canvas.py` as a spec only after its provenance in this MIT repo is confirmed. |
| X-009 | L2 | V2 | 0.55 | Verifying fields is engineering, but choosing which message type means "a human must answer" is a product definition the owner or Orca must give. |
| X-010 | L2 | V1 | 0.6 | Hidden by default with a disclosed count gives a quieter screen; B's T21 rules still apply when the toggle shows them. |
| X-011 | L2 | V1 | 0.8 | No verified field defines "settled"; `unavailable` is the only honest live value. |
| X-012 | L2 | V2 | 0.7 | A retained, oldest-first question list is useful without affected-scope links; waiting for both contracts delays the root-cause fix. |
| X-013 | L2 | V2+V1 | 0.55 | B's single-list screen avoids multi-pane focus in the MVP; keep A's switch rule if a later release needs scrolling panes. |
| A-001 | L3 | QUALIFY | 0.7 | Only "non-consuming" is verified; B's R1 uses one verb, which shrinks exposure; add a gate that confirms no side effect for each verb. |
| A-002 | L3 | QUALIFY | 0.75 | Base STALE on poll success, show evidence timestamps as ages only, and add per-row STALE after Orca's update cadence is verified. |
| A-003 | L3 | QUALIFY | 0.7 | B's golden sample and `FAILED (shape)` contract test (T32) check it; capture stdout of a real call before R1 to confirm one document. |
| A-004 | L2 | QUALIFY | 0.6 | `cell_len` tests are a proxy; keep them, and add a manual check on at least one real terminal with CJK and emoji before R1. |
| A-005 | L3 | QUALIFY | 0.65 | Unproven; make a key-reader plus `Live` redraw spike part of R0 with terminal restore tests, Textual as the named fallback. |
| A-006 | L2 | QUALIFY | 0.55 | Probably true at 300 rows, but add a render-time budget test on the 100-session fixture at 160 columns. |
| A-007 | L2 | QUALIFY | 0.55 | Detect a non-UTF-8 locale and fall back to ASCII box drawing on screen, reusing the export's ASCII path. |
| A-008 | L3 | QUALIFY | 0.6 | State the bounds as per process and disclose it; whether several observers per human must be prevented is an owner decision. |
