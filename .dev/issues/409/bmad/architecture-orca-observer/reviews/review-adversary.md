# Adversary review: orca-observer architecture spine

- Reviewer: independent adversary (incompatible-units lens)
- Spine: `_bmad-output/planning-artifacts/orca-observer/architecture/ARCHITECTURE-SPINE.md`
- Spec: `_bmad-output/specs/spec-orca-observer/` (SPEC, adapter-contract, rendering-rules, snapshot-export-schema, acceptance-tests, release-gates)
- Date: 2026-11-08
- Status: COMPLETE

## Verdict: FAIL

16 blocking, 10 minor. Every blocking finding is a pair of units that each obey every AD as written and still fail to fit together, or a rule that contradicts the spec. The spine is strong on the adapter boundary (AD-3 to AD-5), the sanitizer intent (AD-9) and the snapshot field list (AD-12). It is weak where state lives between cycles, where session state changes without a key, and on who turns in-memory values into the strings that two renderers print.

## Blocking findings

### ADV-01 — No owner for the row set that spans cycles (blocking)

- **Units:** `parse.py` vs `collector.py` vs `view.py`.
- **Divergence:** AD-7 makes `parse` "JSON to `Snapshot`", but also has it flag `conflict (time went back)` and keep "the newer `observedAt`", which needs the previous cycle's rows. AD-8 says a row that drops out "stays, marked `not reobserved`", and a partial cycle "never removes a row". AD-6 gives `CycleResult` only "last good `Snapshot`". `build_view(result, session, clock)` sees one snapshot. Developer P writes `parse(json, previous)` and merges there. Developer C keeps parse pure and merges in the collector. Developer V stores old rows in `Session`. A PARTIAL cycle that succeeds with fewer rows becomes the new "last good" snapshot under C's and V's reading, and rows vanish, which breaks AD-8 and T11, T12 and T41.
- **Fix (new AD):** One `merge(previous: Snapshot | None, pages: list[Page], clock) -> Snapshot` function in `parse.py`, called only by the collector. The `Snapshot` it returns is the cumulative row set for the process: each row carries `last_seen_cycle`, `reobserved: bool`, `order_flag` (`ok`, `order unknown`, `conflict (time went back)`). Rows are never removed by a failed, stale or partial cycle. `CycleResult.snapshot` is always that merged set. `view` and `Session` never hold row data.

### ADV-02 — Page assembly and coverage counters have two possible owners (blocking)

- **Units:** `collector.py` (paging loop) vs `parse.py` (dedup and shape).
- **Divergence:** Coverage needs per-page facts: `reported T1-T2 (changed during read)`, `PARTIAL (empty page k)`, `reported T (page k)`, duplicates across pages. AD-6 puts "coverage counters" in `CycleResult` (collector). AD-7 puts dedup in parse. If parse runs per page, a duplicate split over pages 1 and 2 is never caught. If the collector counts coverage it must read `page.total` from the decoded JSON, so it re-parses fields parse owns.
- **Fix (tighten AD-6 and AD-7):** The collector only fetches and stops at the cap. It hands the ordered list of decoded pages plus a `stopped_by_cap` flag to the single `parse.merge` (ADV-01), which returns the `Snapshot` and a frozen `Coverage` value (collected n, per-page totals, empty-page index, `has_more_at_stop`, duplicate count, unrecognised-key count). `CycleResult` carries that `Coverage` unchanged.

### ADV-03 — Session changes that no key causes have no path; `e` and `q` cannot be pure (blocking)

- **Units:** `view.apply_key` vs the `commands.py` loop vs `view.build_view`.
- **Divergence:** AD-15 says the session changes only through `apply_key(session, key, view) -> Session`. But (a) "the first observation is the baseline" is set without a key; (b) `changed since HH:MM` needs the wall time of `m`, and `apply_key` gets no clock; (c) "a selected row that disappears stays selected" needs a memory of that row; (d) `e` writes a file and `q` quits, which a pure function returning `Session` cannot do. One developer adds `session.export_requested = True` that the loop never reads. Another catches `e` in the loop before `apply_key`. A third has `build_view` treat `baseline is None` as "this is the first cycle", which is true on every cycle because `build_view` cannot return a new session.
- **Fix (tighten AD-15):** Two pure functions in `view.py`: `apply_cycle(session, result, clock) -> Session` (sets the first baseline, updates the last-known row for the selected identity), and `apply_key(session, key, view, clock) -> tuple[Session, Effect]`, where `Effect` is a closed enum `NONE | EXPORT | QUIT`. Only the loop in `commands.py` calls them and performs the effect. `Session` stores `mark_wall_time`.

### ADV-04 — Change flags omit added and removed rows (spec contradiction) and the baseline has no shape (blocking)

- **Units:** `view.py` (flags) vs `render.py`/`export.py` (count `changed since HH:MM (k)`), and tests.
- **Divergence:** rendering-rules says "Every row **added, removed or changed** ... shows `*` and counts". AD-15 only flags a row when one of four fields differs. One developer counts new rows. Another follows AD-15 and does not. The baseline itself is "in-memory mark baseline" with no type: one stores the `View` rows (display strings), one stores raw `Snapshot` values with the `UNKNOWN` sentinel. These compare differently when a value goes from `UNKNOWN` to `unknown`-looking text.
- **Fix (tighten AD-15):** Baseline type is `Mapping[Identity, tuple[stage.worker, stage.dispatch, nextAction.kind, liveness.verdict]]` taken from the merged `Snapshot` (raw values, sentinel kept). A row is flagged when it is absent from the baseline (added), present in the baseline but not reobserved since the mark (removed, rendered `not reobserved`), or any of the four values differ. The count `k` includes all three kinds.

### ADV-05 — The snapshot is built from a View that depends on the user's filter (blocking)

- **Units:** `export.snapshot_json(view)` vs `view.build_view(result, session, clock)`.
- **Divergence:** The `View` depends on `Session`: filter text, show-historical flag, focus. AD-10 says the `View` carries "the historical-hidden count". An export developer serializes `view.rows`, so a user who typed `/foo` or left historical rows hidden writes a snapshot missing rows. The spec says historical rows "are never deleted from the snapshot", and the snapshot is a per-cycle record, not a screen capture. A view developer may instead keep hidden rows in `view.rows` with a `hidden` flag, and the renderer then shows them.
- **Fix (tighten AD-10 and AD-12):** `View` has two row collections: `all_rows` (every merged row, in snapshot order, independent of `Session`) and `visible_rows` (filter and historical toggle applied, in ledger order). `snapshot_json` reads only `all_rows` and envelope fields; `render` and `record_text` read only `visible_rows`. A test builds the same `CycleResult` with two different sessions and asserts byte-identical `snapshot_json`.

### ADV-06 — The snapshot write has no named caller or trigger (blocking)

- **Units:** `commands.py` loop vs `collector.py` vs `export.py`.
- **Divergence:** The envelope says "one snapshot write per completed cycle". Only `commands` may import `export` (AD-1), and the collector cannot. So the write must come from the loop, which redraws "on a new `CycleResult` or a key" (AD-14). A developer who writes on each redraw writes many files per cycle with the same `cycle`. Nothing says whether a failed cycle writes a snapshot (with `source.status` `ERROR`), whether `--once` or fixture mode write one, or who keeps the write going if the Textual fallback deletes the `Live` loop.
- **Fix (new AD):** The loop keeps `last_written_cycle`. When `result.cycle > last_written_cycle` it calls `snapshot_json` once and the atomic-write helper (if CD-6 has set a destination), on success and failure cycles alike, in live mode only (fixture mode never writes a snapshot file). The rule is part of the loop contract that the Textual fallback must keep.

### ADV-07 — Source status vocabulary differs between the screen and the snapshot, with no owner for the mapping or precedence (blocking)

- **Units:** `collector.py` (status) vs `view.py` vs `render.py` vs `export.py`.
- **Divergence:** The screen shows `OK`, `STALE`, `FAILED (...)`, `NOT POLLED`, `NOT AVAILABLE`. The snapshot allows `OK`, `STALE`, `ERROR`, `UNKNOWN`. A cycle that failed 60 s after the last success is both STALE and FAILED: render may show `FAILED (exit 2) 1m` while export writes `STALE`. Before the first cycle, and when discovery returns `None` ("no cycle starts"), there is no `CycleResult`: one developer passes `None` to `build_view`, another publishes a placeholder result. `source.error` must be a short code, but `SourceResult` only defines "a sanitized diagnostic".
- **Fix (new AD):** `CycleResult` always exists (a `NOT_POLLED` result is published at start; discovery failure publishes `NOT_AVAILABLE`). `SourceResult` carries `code` (closed enum: `exit:<n>`, `timeout`, `shape`, `json`, `output-cap`, `not-found`) separately from the 2 KiB diagnostic. `view.py` alone derives one `SourceState` enum with fixed precedence (`NOT_AVAILABLE` > `NOT_POLLED` > `STALE` > `FAILED` > `OK`, or the owner's chosen order) and one table mapping it to the snapshot enum (`FAILED`→`ERROR`, `NOT_POLLED` and `NOT_AVAILABLE`→`UNKNOWN`).

### ADV-08 — Staleness and ages have two owners, and the clock rules contradict each other (blocking)

- **Units:** `collector.py` vs `view.py`; `tests/observe/conftest.py`.
- **Divergence:** AD-6 says the collector decides STALE. AD-10 gives `build_view` a clock. If the collector stamps STALE into `CycleResult`, nothing changes between publishes; after a failure the backoff may wait up to 60 s, so a source that crosses 45 s shows `OK` or `FAILED` until the next publish, and T40 fails. Separately, AD-6 says "`time.monotonic()` only", which a literal reader calls directly, so the T40 fake clock cannot drive it. Conventions say "ages use `time.monotonic()`", but the evidence age (T42) is the gap between now and Orca's ISO `evidence.lastObservedAt`, which needs wall time.
- **Fix (tighten AD-6, AD-10 and Conventions):** `CycleResult` carries `last_success_mono` and `last_success_wall`, never a STALE flag. `view.py` alone computes poll age and STALE from `clock.monotonic()`, and evidence age from `clock.wall()` minus the parsed source timestamp. The collector reads time only through the injected clock object. The age rule in Conventions becomes: poll ages and staleness use the monotonic clock; evidence ages use the wall clock.

### ADV-09 — The `UNKNOWN` sentinel crosses into modules that may not import it (blocking)

- **Units:** `parse.py` (owns `UNKNOWN`) vs `render.py` and `export.py` (allowed imports: `view`, `terminal` only).
- **Divergence:** AD-10 calls `View` "display-ready". If `view` converts the sentinel to `"unknown"`, `snapshot_json` cannot tell a missing value from a source value that is literally the text `unknown`, and cannot write `UNKNOWN`. If `View` keeps the sentinel, render and export must compare against `parse.UNKNOWN`, and AD-1 forbids that import ("nothing else"). Spec wording also varies by place: `unknown`, `unknown (absent in source)` in the inspector, `worktree unknown`, `reported unknown`, `scope unknown`. A source value that is literally the string `UNKNOWN` is indistinguishable from a missing one in the snapshot.
- **Fix (tighten AD-1 and AD-10):** `view.py` re-exports `UNKNOWN` (or `View` fields use a typed `Value = Known(str) | Unknown`), and render and export test it only through `view`. `export.py` alone maps `Unknown` to the JSON string `"UNKNOWN"`; `view.py` alone maps it to each place-specific screen word. Record the collision as a known limitation, or add an `unknownFields` list to the row as an optional v1 field.

### ADV-10 — Every status literal is "defined once in the module that renders it", and two modules render it (blocking)

- **Units:** `render.py` vs `export.record_text`.
- **Divergence:** The gap notice, freshness cells, the coverage and PARTIAL strings, `not reobserved`, `k historical hidden (h)`, `unavailable (no source)` and `cost unavailable` appear on screen and in the text record. Under the Conventions row both modules define them, so two copies drift. T48 then compares two hand-typed strings.
- **Fix (tighten Conventions):** Spec literals live once in `view.py` (or a `strings.py` that only `view` imports), and `View` carries the final text of every status line. Renderers only lay out and truncate; they never build a spec sentence. Tests assert against the single constant.

### ADV-11 — Ledger order is assigned to no module, and the spec wants screen and snapshot orders to differ (blocking)

- **Units:** `parse.py` (flags order), `view.py` (one row tree), `export.py` (AD-12 sort).
- **Divergence:** rendering-rules: the ledger is "in source order". AD-12: the snapshot is sorted by timestamp. The spine never states the ledger order. A view developer building "one view model" (AD-10) sorts once by timestamp, so the screen breaks the spec. "Source order" is also undefined across five pages plus retained `not reobserved` rows from earlier cycles. CD-3 says the sort "moves to the screen only" if the owner picks the other order, but no module owns the sort today.
- **Fix (new AD):** `parse.merge` assigns each row a `source_rank` (page index, then position; retained rows keep their last rank and sort after reobserved rows). `view.py` alone owns both orders: `visible_rows` by `source_rank`, `all_rows` by the AD-12 timestamp key. `export.py` never sorts. CD-3 then swaps which key `all_rows` uses.

### ADV-12 — The `Key` type has no permitted owner (blocking)

- **Units:** `keys.py` (decodes keys) vs `view.apply_key` (consumes them).
- **Divergence:** `apply_key(session, key, view)` lives in `view.py` and needs the `Key` type. `keys.py` defines `read() -> Key`. AD-1 has no `view → keys` edge, and AD-14 deletes `keys.py` if the spike fails while also saying `view` "does not change". A view developer imports from `keys` (breaks AD-1); a keys developer defines its own `Key` and `view` defines another (two owners of one entity).
- **Fix (tighten AD-14 and AD-15):** `Key` (a closed enum of logical keys, plus `Text(char)` for filter mode) is defined in `view.py`. `keys.py`, and the Textual adapter if the spike fails, translate raw input into `view.Key`. Add `keys → view` to the AD-1 diagram.

### ADV-13 — `commands.py` needs modules the import diagram forbids, and fixture/live switching has no seam (blocking)

- **Units:** `commands.py` vs `adapter.py`, `parse.py` (fixture loader) and `collector.py`.
- **Divergence:** The production `Runner` must be built and handed to the collector (tests inject a fake), and discovery must run before the first cycle. Neither fits a `commands → collector` edge unless the collector builds the runner itself, which makes injection a collector constructor detail no AD names. The fixture loader is in `parse.py`, but only `collector` may import `parse`. The header needs `mode=fixture|live` and `SYNTHETIC FIXTURE <variant>`, which no `CycleResult` field carries. One developer runs fixtures through the collector with a fake runner; another loads fixtures straight into `build_view`. Fixture-only fields (questions for B and C) have no place in `Snapshot`. `--once` needs one synchronous cycle, and no collector API offers it.
- **Fix (new AD):** `collector.py` exposes `Collector(source: CycleSource, clock)` with `start()`, `latest()` and `run_once() -> CycleResult`. `CycleSource` has two implementations: `LiveSource(runner)` (adapter plus parse) and `FixtureSource(variant)` (parse fixture loader). `commands` builds one of them and gets the runner from `adapter.production_runner()`. Add `commands → adapter` (factory and discovery only) to the diagram. `CycleResult` carries `mode`, `variant` and an optional `fixture_extras` group.

### ADV-14 — Discovery runs outside the `Runner` seam, so the tests and the argv log cannot see it (blocking)

- **Units:** `adapter.py` (calls `_find_orca()` "as is") vs `tests/observe/conftest.py` (patches `subprocess.Popen`/`run` to raise, T36) and T1 and the success signal.
- **Divergence:** `_find_orca()` runs its own `subprocess.run`. With AD-16's guard in place it raises in every test, so discovery always fails, or each test patches `_find_orca`, which T1 ("argv equals ... plus the one-time `skills list --json` discovery probe") then cannot check. The success signal's "argv log shows ... the one discovery probe" cannot hold because the probe never passes through the logging `Runner` or the forbidden-prefix guard of AD-4.
- **Fix (tighten AD-3):** `adapter.py` takes discovery as an injected callable, `Discover = Callable[[], str | None]`, defaulting to `_find_orca`. Tests inject a fake that records the probe argv into the same argv log. State that the discovery probe is outside the 8 MiB and killpg guarantees of AD-5 until the owner approves moving the helper.

### ADV-15 — "Newline only for the inspector" cannot be decided where sanitizing happens (blocking)

- **Units:** `parse.py` (calls the sanitizer once, AD-9) vs `render.py` (ledger cells) and `export.record_text`.
- **Divergence:** parse does not know which field will reach the inspector. If it keeps newlines, a worker can put `\n` in `nextAction.kind` or `dispatchId` and forge an extra ledger line on screen, or a fake row in the text record (a line-injection that the ESC-byte checks of T29 miss). If it strips them, the inspector loses them. Two compliant developers pick opposite sides.
- **Fix (tighten AD-9):** parse sanitizes with newline kept, but only for a fixed list of inspector-only fields (`stage.detail`, `stage.activity`, the stderr diagnostic). Every other field has newline removed. `view.py` builds list and record cells only from newline-free fields, and a test feeds `\n` into `dispatchId` and asserts one record line per row.

### ADV-16 — `--once` printed through a Rich `Console` will emit ESC bytes (blocking)

- **Units:** `commands.py` (prints `record_text` to stdout through `make_console`, the only allowed `Console` builder) vs `export.py` (assumes a raw string) and T27.
- **Divergence:** `Console.print` highlights by default, so numbers and UUIDs in the record get SGR colour on a colour terminal, which breaks "no ESC byte". `markup=False` (AD-9) does not turn off the highlighter. On a non-UTF-8 stdout, CJK worker text raises `UnicodeEncodeError`, and only `terminal.py` may read the encoding.
- **Fix (tighten AD-11 and AD-13):** `--once` and file exports write `record_text` bytes directly (`sys.stdout.write` / the atomic helper), never through a `Console`. `make_console` always sets `highlight=False`. `terminal.py` exposes `output_encoding()` and `commands` encodes with `errors="replace"` when it is not UTF-8.

## Minor findings

| ID | Units | Divergence | AD to add or tighten |
| --- | --- | --- | --- |
| ADV-17 | `terminal.make_console` vs `conftest` console factory | AD-16 needs `record=True`; the `make_console(policy, file=None)` signature has no such parameter. Making every console record grows an unbounded buffer under `Live` for hours. | Add `record: bool = False` to `make_console`; production never sets it. |
| ADV-18 | `render.py` vs spec | Spec: below 80 columns the too-narrow message sits above the COUNTS strip and the denominators still print. AD-13 states only the message. | AD-13: below 80, render the diagnostic plus the COUNTS strip, wrapped. |
| ADV-19 | `parse.py` vs inspector | AD-7 "unexpected keys are counted, not shown"; spec shows `n unrecognised keys` in the inspector. | AD-7: the count is per row and shown in the inspector. |
| ADV-20 | `fixtures/` vs CD-9 | AD-16 uses "the redacted golden sample" in every test; CD-9's default is no live-captured sample. | State that R0 uses a synthetic golden sample shaped like `worker-list` until OQ-5 permits a captured one. |
| ADV-21 | `view.py` | Local `HH:MM:SS` depends on the process time zone, which is global state inside a "pure" function. | The injected clock supplies the time zone or a `to_local()` method. |
| ADV-22 | `export.py` vs `parse.py` | `result.counts` is optional; absent becomes `UNKNOWN` (a string) where the schema expects a map. The screen token names four fixed keys while the snapshot passes the map through. | Schema: `counts` is `object` or `"UNKNOWN"`; the screen lists source keys in source order. |
| ADV-23 | `render.py` vs `view.py` | `x/y shown` and `+N more` depend on height (render), but AD-10 puts "counts with denominators" in `View`; `record_text` has no height. | `View` carries `visible_rows` counts; render alone computes height overflow; record never prints `+N more`. |
| ADV-24 | `view.py` | Spec: "historical evidence explicitly linked to a shown item is never hidden" is not in any AD. | Add to AD-15 or AD-10 (no-op in R1, needed by R3 links). |
| ADV-25 | `commands.py` vs `keys.py` | The loop learns of a new `CycleResult` only when `keys.read(timeout)` returns; the SIGINT handler restores the terminal but no AD says who exits. | Fix `read` timeout at or below 250 ms; the keys handler restores and re-raises `KeyboardInterrupt`; the loop exits. |
| ADV-26 | `adapter.py` vs `export.py` | AD-12 `source.error` is "a short code" but `SourceResult` defines only a diagnostic. | Covered by ADV-07's `code` field; listed so the schema test asserts the closed code set. |

## Spec contradictions found

- ADV-04: change flags must include added and removed rows (rendering-rules "Changes since last look").
- ADV-05: hidden historical rows are "never deleted from the snapshot", but a session-dependent `View` drops them.
- ADV-11: the ledger keeps source order; nothing in the spine keeps it.
- ADV-18: the COUNTS strip must still print below 80 columns.

## What holds up

AD-4 and AD-5 leave no room for a second subprocess path in the observer's own code. AD-12's field list matches `snapshot-export-schema.md` exactly, including the withheld fields. AD-17 and AD-18 close the write-back and TUIBBS questions cleanly. AD-13 gives a single owner for colour, ASCII and width.
