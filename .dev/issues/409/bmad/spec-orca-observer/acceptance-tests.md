# Acceptance tests

AC-1..AC-10 are restated from the seed brief. The mapping was re-checked on 2026-11-08 against the issue's acceptance list (issue-409-body.md:77-87) and Proposed Solution (issue-409-body.md:19); the clauses the seed brief did not carry are covered as follows.

| Issue clause | Coverage |
|---|---|
| "elapsed time is not completion percentage" (:84) | T31 |
| "a partial subtotal is not total spend" (:84) | T31 (`cost unavailable`; no subtotal is ever shown) |
| "policy-frozen work remains for explicit human handling" (:84) | T34 |
| "A dirty worktree is not automatically dangerous" (:19) | Out of R1: no verified dirty-worktree source, so no dirty or danger state is ever rendered; no release covers it yet |
| "shared paths do not establish a conflict" (:19) | T20 |
| "inspectable evidence is not admission" (:19) | T15 |
| "stale is not failed" (:19) | T11, T40 |
| "A human selects the visual direction" (:77) | AC-S (reviewer check) |
| "The twenty primary design images and complete package are provided with the issue" (:87) | Issue delivery, not observer behaviour; out of this spec |

**Harness.** Render with `Console(width=W, record=True, color_system=None or "standard")` and read `export_text()`. The adapter runs against a fake runner returning recorded JSON from the redacted golden sample, which is recorded at the first permitted live read (R1, `release-gates.md`); until then (R0) the fake runner returns the synthetic `base` variant. No TTY, no live Orca.

**Fixture variants:** `base`, `uneven`, `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, `injection`.

| AC | Requirement | Tests |
|---|---|---|
| AC-1 | Read-only, no consuming check | T1: across every adapter path, argv equals one exact template (`adapter-contract.md`): the `worker-list` template per cycle, plus at most one `skills list --json` discovery probe per candidate (at most two) before the first cycle, intercepted by patching the `subprocess.run` that `_find_orca()` calls. T2: static test that `--ack`, `--wait`, `--retry-request`, `--peek` and `run-use` appear in the adapter module only inside the forbidden set, and `check` appears only there and in the one R2 message template. T3: no key maps to an Orca call. |
| AC-2 | Deterministic, bounded collection | T4: a fake always returning `hasMore=true` stops at the 5-call cap and renders `PARTIAL: collected 500 of reported T`. T5: a fake sleeping past a configured per-call timeout injected into the fake runner (the real value is measured at the first permitted live read) shows `FAILED (timeout)`; the cycle ends within the 15 s budget. T6: same input renders byte-identical text twice. |
| AC-3 | Attention items, reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs. T8: after `m`, a fixture step changing one `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)`. T9: live mode with no message source shows `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` (`rendering-rules.md`) and titles the ledger `worker-reported, not questions`. |
| AC-4 | Seen is not resolved | T10: `m` on every item leaves the open count unchanged. T11: `source-loss` keeps the open count and every retained item; nothing becomes resolved or failed. T12: an item missing next cycle stays, marked `no longer in source window`. |
| AC-5 | Separate lifecycle, outcome, report, acceptance, tests, approval; unknown never 0/false | T13: `missing-fields` renders `unknown` for every absent field; `0`/`false` never stand in (asserted per field). T14: `terminalState=released` with `outcome` absent never renders `done`, `complete` or `settled`. T15: report, acceptance, tests and approval each render `unavailable (no source)` live; no row or inspector ever renders `admitted` from evidence fields (inspectable evidence is not admission). |
| AC-6 | Filtered and global counts with denominators; 100-row cap disclosed | T16: matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders); every count line matches `k of n`, every hidden overflow shows `x/y shown` with y = fixture total. T17: `uneven` per-owner counts sum to the global count. T18: `page.total=287` with 100 rows shows `collected 100 / reported 287`, never `287 workers`; `page.total` absent shows `reported unknown`. T19 (R2, no longer a placeholder; fake-runner test with `--questions` on): the question panel title contains `at most 100 rows per read, not 100 questions` and `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`. |
| AC-7 | No one-to-one session/worktree assumption | T20: `shared-unmapped` shows two sessions sharing one worktree as two rows; opening the inspector on each shows the same `resource.worktreeId`, and the inspector of the session with no worktree shows `unknown (absent in source)` for it; no count divides one by the other, and no `conflict` label appears for the shared worktree. |
| AC-8 | Historical records, duplicates, out-of-order | T21: released/retained rows hidden by default with `k historical hidden (h)`; after `h` listed with `terminalState`, not counted active; a row with absent or any other `terminalState` is always shown with its raw value (or `unknown`) and not counted active. T22: `duplicate-out-of-order` shows `k duplicate rows ignored`; an older `observedAt` never overwrites a newer one; a row missing both timestamps is flagged `order unknown`; a backward timestamp shows `conflict (time went back)`. |
| AC-9 | Widths, keyboard, NO_COLOR, export, full IDs, no blink | T23: at 160/116/80 every screen line has `cell_len <= W`. T24: `long-identifiers` truncates with `>` in lists; inspector shows the full ID. T25: reorder between cycles keeps selection on the same row ID. T26: `NO_COLOR=1` and `NO_COLOR=yes` emit no SGR colour; meaning stays readable as words. T27: `e`/`--once` writes the record export: no ESC byte, full IDs, no truncation. T28: SGR 5/6 (blink) never appears. |
| AC-10 | Sanitize untrusted text; cell-width truncation | T29: `injection` (CSI, OSC 8 hyperlink, unterminated OSC, 8-bit C1 `\x9b`, BEL, bidi Cf such as U+202E, terminal title set) leaves no ESC, C1 or Cf byte in render or export. T30: CJK/emoji identifiers truncate by cells; no overflow, no split double-width char. T31: cost renders `cost unavailable`, never `$0`; no progress from tokens or activity; elapsed time renders only as a plain age, never as a completion percentage. |
| Contract | worker-list shape | T32: redacted golden `worker-list --json` sample parses. Removing `result`, `result.workers` or `result.page.hasMore` gives `FAILED (shape)` with last good snapshot kept; removing `result.scope` shows `scope unknown`; removing `page.total` shows `reported unknown`; removing an inner `projection.*` field gives `unknown`, not an error. `result.workers` not a list, `result.page.hasMore` not a boolean (for example the string `"false"`), or either set to JSON `null`, gives `FAILED (shape)`. `hasMore=true` with `nextCursor` absent, empty or repeated gives `PARTIAL (cursor missing or not advancing, page k)`; a cursor rejected by the argv guard gives `PARTIAL (cursor rejected, page k)`. |

## Tests after T32

| Test | Pins | AC |
|---|---|---|
| T33 | `empty` renders `no observed items in this source window; not proof none exist`, never `no questions`. | AC-3 |
| T34 | Fixture mode renders `FROZEN`; live mode renders SETTLED and POLICY FROZEN as `unavailable (no source)`, never blank or zero. | AC-5 |
| T35 | COUNTS strip appears at 80, 116 and 160; priority tokens never truncated; below 80 reads `terminal too narrow (min 80)` and still shows the question-source gap notice. | AC-9 |
| T36 | Real subprocess call patched to raise so any unlisted argv fails loudly; `NO_COLOR=yes` and colour-enabled cases both pinned. | AC-1, AC-9 |
| T37 | Argv validation rejects a value starting with `-`, a malformed `runId` and every forbidden prefix; the fake runner fails on an unlisted argv. | AC-1 |
| T38 | Aggregate with k unknown members renders `n+? (k unknown)`, never a clean `n`. | AC-5 |
| T39 | Same `dispatchId` from two fake sources whose validated Orca CLIs resolve to different absolute paths (different source namespaces) stays two rows. | AC-8 |
| T40 | Fake monotonic clock: STALE at 45 s without success, unaffected by wall-clock jumps; backoff caps at 60 s; overrunning call killed and strip shows `cycle overran (Ns)`. | AC-2 |
| T41 | First observation is the baseline with no change flags; a row dropping out shows `not reobserved`. | AC-3 |
| T42 | Successful poll with old worker evidence shows poll age and evidence age separately and does not mark the source STALE. | AC-5 |
| T43 | With the selected row visible and others hidden, `+N more` excludes the selected row. | AC-6 |
| T44 | Worker text containing Rich markup (e.g. `[bold]`) renders literally. | AC-10 |
| T45 | Default view chosen at start-up, never switches mid-session; header shows `read k of N Runs since start` (which views carry it is an open question, `SPEC.md`). | AC-3 |
| T46 | For the one named Run, at 1,001 retained questions (distinct Run plus `message.id`), eviction does not lower the open total; the count reads `unknown (retention exceeded)` with 1,000 retained; oldest first. Test file: `tests/observe/test_questions.py` and `test_view.py`. | AC-4 |
| T47 | With `--questions` off, and before QUESTION-OBSERVATION passes, the question area reads `source UNVERIFIED, 0 rows interpreted, not "no questions"` and the output is byte-identical to release 1; no count from `result.count`; `changed during read` and mismatch notes render per `rendering-rules.md`. Test file: `tests/observe/test_view.py`. | AC-3, AC-6 |
| T48 | Screen renderer and record export read the same view model; an ID truncated with `>` on screen appears in full in the export. | AC-9 |
| T49 | When height cannot hold coverage, scope, PARTIAL and the question-source gap notice ahead of optional panels, a too-small diagnostic shows and still carries the gap notice. | AC-9 |
| T50 | R0 renders of A, B, C at 160/116/80 each carry "synthetic fixture, not live evidence" with a degraded version beside each. | AC-S input |
| T51 | R2, no longer a placeholder (`tests/observe/test_question_quiet_scope.py`): a stateful fake Orca backend over the probe shapes first establishes readable identity (every row has a `msg_` id, a Run id and a created time), then repeated reads on a quiet scope return identical question ids, order and an unchanged fake mailbox state; a consuming fake makes the companion test fail; a pass covers only the visible effects tested, as the Run's owner on a probe Run, and says nothing about a non-owner reader (Q-1) (INV-022). | AC-1 |
| T52 | With the recorded `consumer_fenced` (exit status 1) and `no_active_terminal` error envelopes, the question source is `FAILED` with code `consumer-fenced` or `no-active-terminal`, the panel says `this terminal does not hold the named Run; the observer never binds to a Run`, the worker-list state is unchanged and retained questions stay. Test file: `test_adapter.py`, `test_collector.py`, `test_view.py`. | AC-4, AC-5 |
| T53 | The fake runner receives exactly the R2 message argv `(orca, orchestration, check, --all, --types, question, --run, <runId>, --json)`; `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, `inbox`, plain `check`, `check --peek`, an unfiltered `check --all` and the template without `--run` are rejected before any call. Test file: `test_adapter.py`. | AC-1 |
| T54 | A 100-row reply (the recorded-shape cap fixture) shows `window full: older questions may be missing` with the disclosure label; a 99-row reply does not; a moved window keeps dropped questions as `no longer in source window`; no total is taken from `result.count`. Test file: `test_question_cap.py`. | AC-6, AC-4 |
| T55 | The four recorded redacted samples of the message read (success, missing, stale, contradictory) are each pinned in a contract test: success parses to the expected rows, missing gives `FAILED` with retained questions kept, stale shows `STALE` after 45 s on the monotonic clock, contradictory rows are dropped and counted. Test file: `test_golden_contract.py` and `test_fixtures.py`. | AC-4, AC-5 |
| T56 | While the gate guard constant is off, `--questions` exits non-zero with `question read not enabled: QUESTION-OBSERVATION has not passed` and makes no Orca call, not even discovery. Test file: `test_commands.py`. | AC-1 |

## Snapshot schema test (CAP-10, recorded owner decision 2)

- Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an unknown `schemaVersion` major; asserts missing values are the string `UNKNOWN`; asserts no message bodies, prompts, file contents or credentials. Test ID not yet assigned.

## Reviewer-checked and manual (never reported as automated tests)

- **AC-S:** a reviewer checks the owner's dated selection record exists and names the date, option, who decided, where the owner's statement lives, the pre-observation default, the post-observation default, the post-link choice or deferral, the fallback date, the stack confirmation, the command name and the confirmed production-integration reading (`release-gates.md`). No agent writes the record.
- **Manual CJK check:** one run in a real terminal confirms cell truncation of a CJK identifier as T30 asserts headlessly; reported as a manual check, not a test pass.
