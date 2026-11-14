# R3-B1 gate, verification cycle 1 (rf-qa verifier, report-only)

**Date:** 2026-11-09
**Phase:** fix-cycle verification
**Fix cycle:** 1
**fix_authorization:** false (no file other than this report was written)
**Design file:** `docs/designs/orchestrator-mode.md`, 1025 lines now (Grep `^.*$` count 1025; it was 1023 at cycle 0)
**Inputs read:** `consolidated-findings-cycle0.md`, `fix-log-cycle1.md`, `cycle-ledger.md`, `phase-outputs/test-results/r3-b1-mechanical.md`, research/04 lines 44-56 and 75-140, research/09 Gap 4 (line 139 and summary line 223), the `## Checks` tables of the nine `qa-*-report.md` files, DESIGN lines 1-80, 205-235, 351-520, 518-560, 726-775, 819, 857, 868-904, 965-1025.

Scope note honoured: the R3-B2 several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." (DESIGN line 498) and the transcript outcome for a path-B match that does not join are Phase 3 item 3.1 work and are not graded here.

---

## Findings re-check (F_0)

| Id | Verdict | Evidence (DESIGN, current line numbers) |
|---|---|---|
| R3B1-F1 (MAJOR) `completedAt` shape claim | RESOLVED | `docs/designs/orchestrator-mode.md:889` (15.1 item 4): "the static bundle read gives the SQLite form `YYYY-MM-DD HH:MM:SS` UTC for `dispatchedAt` only; the form of `completedAt` is UNVERIFIED and either that form or ISO 8601 is possible, which 7.2 accepts; `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`". Matches the smallest fix. It agrees with research/04:51 (SQLite form for `dispatched_at` only) and research/04:53 (`completed_at` write not found). Line 470 (7.2) still accepts both forms. The old "present with the shapes the static bundle read gives" wording is gone (Grep for "confirmed by" and "are confirmed" returns nothing; the only hit for "confirms" is the new text at line 498). |
| R3B1-F2 (MAJOR) UNVERIFIED dropped | RESOLVED | `:457` (OrcaObservation row): "names read statically from the Orca 1.4.245 bundle and UNVERIFIED until step 1.0a item 4 (open item 23)". `:498` (worker bullet): "The names behind the three fields come from the static bundle read and are UNVERIFIED until step 1.0a item 4 confirms them (open item 23)". `:995` (open item 23) starts "UNVERIFIED: that `worker-show` ...". All three sites named in the finding are fixed and agree with research/04:128 and 04:130. |
| R3B1-F3 (MAJOR) fixture drops path-B join setup | RESOLVED | `:743`, `test_path_b_window_open_row_joins`: "row D1 with `session_join` pane P, `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, a tab-map entry from P to session S, transcript S with `first_record_ts` 10:05, `collected_start` 12:00: S joins D1, `person_started` is False, S is shown as `orca:D1` with note `joined by pane: latest session of the pane`". Compared with research/04:114: every Given item and the Then are present. |
| R3B1-F4 (MAJOR) parsers have no name, module or signature | RESOLVED | `:390` `def parse_time(value: object) -> datetime \| None` (never raises; used by `read_transcript_tail` and `parse_worker_show`, so by `collect`). `:391` `def parse_worker_show(run: str, list_row: object, show: object \| None) -> OrcaObservation` (never raises; sets the three dispatch fields through `parse_time`). Both sit under `probes.py` in 7.1. `:211` the `probes.py` may-import row lists `datetime`. `:400` the `read_transcript_tail` comment says "times via parse_time". `:470` names `probes.parse_time` as the one function that applies the rule and says both callers use it. `:742` names `probes.read_transcript_tail` (first three fixtures), `probes.parse_worker_show` (last three) and `probes.parse_time`. All five parts of the smallest fix are present. The import boundary still holds: `OrcaObservation` is a `models` type and `probes` may import `models`. |
| R3B1-F5 (MAJOR) timezone of the sweep's own times | RESOLVED | `:470`: "The times the sweep itself creates are aware UTC `datetime` values too: `now`, `collected_start`, `collected_end` and `TranscriptTail.mtime`. `collected_start` is read once at the top of `collect`, before the first Orca call, and `collected_end` once when `collect` returns. A naive value never reaches `classify`." `:456` types `collected_start: datetime`, `collected_end: datetime` (aware UTC). `:743` lead-in: "every time in them is aware UTC". The `TypeError` risk named in the finding (aware `first_record_ts` against a naive `collected_start`) is closed by the written rule. |
| R3B1-F6 (MAJOR) truncated tail proves or disproves session start | RESOLVED | `tail_complete` appears on 7 lines (Grep count): `:60` (GQ-103(3) list), `:400` (reader comment), `:459` (`TranscriptTail` row: True when the read began at byte 0, False when it began later and the first partial line was dropped, every file over 256 KiB), `:498` (window rule), `:742` (first reader fixture says `tail_complete` True, the over-256 KiB fixture says False), `:743` (new classify fixture `test_path_b_incomplete_tail_has_no_session_start`), `:1025` (revision log). `:498`: when the window is observable and `tail_complete` is False, the session start is not observable, no join, the row is could not determine with note `session start not observable: transcript tail only`, and the transcript is None with the same note. `:768` (FR-010 trace) adds "a transcript whose tail is complete". `Dispatch time window not observable` keeps priority: the new sentence starts "When the window is observable but". The note text is distinct from the two existing path-B notes. |
| R3B1-F7 (MAJOR) "four existing test files" | RESOLVED | `:730`: "edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged)". The list at `:748-749` edits exactly three files (`tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`) and marks `test_routing_plugin_parity.py` "unchanged, must pass". Glob confirms all four files exist. |

Open BLOCKING or MAJOR findings from F_0 after this check: 0.

---

## Checks

The 129 check ids of the cycle-0 PASS set (`cycle-ledger.md` row 0), each re-run against the DESIGN as it is on disk now. A check marked PASS here still passes on the fixed file; "(N1)" to "(N4)" point to the notes at the end of this report. Where a check compared DESIGN text with research/04 section 2.2, three departures are intended and required by F_0: the `completedAt` shape claim (F1), the UNVERIFIED wording (F2) and the added `tail_complete` text (F6). They are not counted as failures, because the consolidated findings ordered them and research/04:128 and :130 support them.

### qa-actionability-report (item 2.12)

| Check id | Result | Evidence now |
|---|---|---|
| qa-actionability-report:C1 | PASS | `:470` states that every Orca and transcript time is aware UTC |
| qa-actionability-report:C3 | PASS | `:498` "both ends included" |
| qa-actionability-report:C4 | PASS | `:498` "cut to whole seconds"; `:743` bounds fixture 10:00:00.700, 11:00:00.400, 11:00:01.000 |
| qa-actionability-report:C5 | PASS | `:498` window runs to `collected_start` only for `pending` or `dispatched`; any other status without an end has no window |
| qa-actionability-report:C6 | PASS | `:498`, `:995` and `:743` (`test_path_b_row_without_start_has_no_window`) name the outcome and the note |
| qa-actionability-report:C7 | PASS | `:459`, `:742` over-256 KiB fixture, now also `tail_complete` False |
| qa-actionability-report:C9 | PASS | Edits 1 to 9 present at `:457`, `:459`, `:470`, `:498`, `:400`, `:60`, `:889`, `:995`, `:1025`; cycle 2 row `:1015` reads "earliest `timestamp` in the transcript tail"; intended departures only |
| qa-actionability-report:C10 | PASS | Every fixture at `:742` and `:743` has a Given, a trigger and an expected value |
| qa-actionability-report:C11 | PASS | Window fields are model fields: `:456`, `:457`, `:459`; `classify.py` needs nothing else |
| qa-actionability-report:C12 | PASS | `:400`, `:60`, `:889`, `:995`, `:1025` agree on the field names |
| qa-actionability-report:C13 | PASS | Em-dash 0, TODO or TBD 0, totals at `:821` and `:997`; the snapshot's "1023 lines" is now 1025 (N1) |
| qa-actionability-report:C14 | PASS | `:498` and `:995` give the same note for a no-window row; the new `tail_complete` case is a separate case with its own note |

### qa-completeness-report (item 2.11)

| Check id | Result | Evidence now |
|---|---|---|
| qa-completeness-report:C1 | PASS | `:457` row has the three fields and the None rule (UNVERIFIED wording per F2) |
| qa-completeness-report:C2 | PASS | `:459` `first_record_ts` after `last_record_ts`, then `tail_complete` |
| qa-completeness-report:C3 | PASS | `:470` time-parsing paragraph, extended |
| qa-completeness-report:C4 | PASS | `:498` window rule, inclusive, seconds cut, status values, no-window rule, notes; `tail_complete` sentence added |
| qa-completeness-report:C5 | PASS | `:400` comment lists `first_record_ts`, `last_record_ts` and `tail_complete` |
| qa-completeness-report:C6 | PASS | `:60` lists the four names plus `tail_complete` |
| qa-completeness-report:C7 | PASS | `:889` capture text; shape claim corrected per F1; the second capture question is still there |
| qa-completeness-report:C8 | PASS | `:995` item text; "UNVERIFIED:" prefix per F2; behaviour cell unchanged |
| qa-completeness-report:C9 | PASS | `:1025` row and `:1015` m2 wording |
| qa-completeness-report:C10 | PASS | `:742` fixture 1 (`tail_complete` True added) |
| qa-completeness-report:C11 | PASS | `:742` fixture 2 |
| qa-completeness-report:C12 | PASS | `:742` fixture 3 (`tail_complete` False added) |
| qa-completeness-report:C13 | PASS | `:742` fixture 4 |
| qa-completeness-report:C14 | PASS | `:742` fixture 5 |
| qa-completeness-report:C15 | PASS | `:742` fixture 6 |
| qa-completeness-report:C17 | PASS | `:743` fixture 8 |
| qa-completeness-report:C18 | PASS | `:743` fixture 9 |
| qa-completeness-report:C19 | PASS | `:743` fixture 10 |
| qa-completeness-report:C20 | PASS | Grep: dash and `--` 0, TODO or TBD or FIXME 0, `Total: 9 deviations.` at `:821`, `Total: 23 open items.` at `:997` |
| qa-completeness-report:C21 | PASS | Grep for "earliest", "start time", "end time", "time window": remaining hits are definitions, the section 1 status text (`:9`) and cycle log rows; no pre-fix claim that contradicts the rule |
| qa-completeness-report:C22 | PASS | `:768` FR-010 row names `sweep/test_probes_allowlist.py` (the six reader and parser fixtures) |

### qa-crossref-chain-report (item 2.14)

| Check id | Result | Evidence now |
|---|---|---|
| qa-crossref-chain-report:C1 | PASS | Section map re-run: 47 `##` and `###` headings, same list as the fix log's Command 1 |
| qa-crossref-chain-report:C2 | PASS | Model names at `:60`, `:400`, `:457`, `:459`, `:498`, `:742`, `:743`, `:1025`; Orca source names at `:457`, `:742`, `:889`, `:995` |
| qa-crossref-chain-report:C3 | PASS | `:60` points to `models.py` (section 7.2); the fields exist at `:457` and `:459` |
| qa-crossref-chain-report:C4 | PASS | `:457` cites section 2.2 path A or B (GQ-108 at `:65`), step 1.0a item 4 (`:889`) and open item 23 (`:995`) |
| qa-crossref-chain-report:C5 | PASS | `:498` cites item 4, item 23, `collected_start` (`:456`), `Budget` `shows=50` (`:367`) |
| qa-crossref-chain-report:C6 | PASS | `:470` "the 'Unknown row schema' bullet below" resolves to `:508`; `:742` "per the unknown row schema rule" resolves to the same bullet |
| qa-crossref-chain-report:C7 | PASS | `:400` comment matches `:459` and the reader fixtures at `:742` |
| qa-crossref-chain-report:C8 | PASS | Arithmetic at `:743` unchanged and correct; the classify row now names 5 fixtures, not 4 (N3) |
| qa-crossref-chain-report:C9 | PASS | `:768` cites `sweep/test_probes_allowlist.py` and "the six reader and parser fixtures" |
| qa-crossref-chain-report:C11 | PASS | `:889` Feeds cell names the path-B time window and open item 23; capture item 13 (`:898`) and open item 22 (`:994`) unchanged |
| qa-crossref-chain-report:C12 | PASS | `:995` "Closed by" item 4 exists; behaviour agrees with `:498`; 23 numbered rows (`:973` to `:995`) |
| qa-crossref-chain-report:C13 | PASS | Edits 1 to 8 present at `:457`, `:459`, `:470`, `:498`, `:400`, `:60`, `:889`, `:995`; only the intended F1, F2, F6 departures |
| qa-crossref-chain-report:C14 | PASS | `:1021` intro cites master `5dc29d23`, which is the newest commit in the session's recent-commit list; row text cites existing sections |
| qa-crossref-chain-report:C16 | PASS | `:1015` reads "the earliest `timestamp` in the transcript tail" |
| qa-crossref-chain-report:C20 | PASS | Totals at `:821` and `:997`; 9 `D` rows; 23 open-item rows; no dash; no TODO or TBD |
| qa-crossref-chain-report:C21 | PASS | The seven mechanical rules still hold on the fixed file (see Mechanical gate re-check); the snapshot file itself is stale (N1) |
| qa-crossref-chain-report:C22 | PASS | `pyproject.toml:16` `requires-python = ">=3.10"`; research/04:50-51 status set and `datetime('now')`; `:470` and `:889` agree |
| qa-crossref-chain-report:C23 | PASS | `:9`, D9 row `:819` and SP-29 row `:857` do not contradict the window wording |

### qa-domain-accuracy-report (item 2.15)

| Check id | Result | Evidence now |
|---|---|---|
| qa-domain-accuracy-report:C1 | PASS | `:470` "`Z` is rewritten to `+00:00` first, because Python 3.10 `datetime.fromisoformat` does not accept `Z`" |
| qa-domain-accuracy-report:C2 | PASS | `:470` SQLite `YYYY-MM-DD HH:MM:SS`, no zone, the form `datetime('now')` writes; research/04:51 |
| qa-domain-accuracy-report:C3 | PASS | `:470` "read as UTC"; the paragraph makes every parsed value aware |
| qa-domain-accuracy-report:C7 | PASS | `:743` bounds fixture arithmetic unchanged: .700 and .400 cut into the window, 11:00:01.000 out |
| qa-domain-accuracy-report:C8 | PASS | `:498` "can only move a session to could not determine or False, never to True"; the new `tail_complete` case also yields neither True nor False |
| qa-domain-accuracy-report:C9 | PASS | `:33` states the ISO 8601 `Z` form of the sample; `:742` fixture 2 uses out-of-file-order timestamps and expects the earliest value |
| qa-domain-accuracy-report:C12 | PASS | `:498` and `:889` use `pending`, `dispatched` for open and the five-value status set; research/04:50 |
| qa-domain-accuracy-report:C14 | PASS | The six reader and parser fixtures and four window fixtures of research/04 section 2.3 and Gap 4 are all in `:742` and `:743` with their Given and Then; the fifth classify fixture and the `tail_complete` expectations are additions required by F6 (N3) |
| qa-domain-accuracy-report:C15 | PASS | `:995` and `:889` agree with research/04 edits 7 and 8 apart from the intended F1 and F2 wording |
| qa-domain-accuracy-report:C16 | PASS | Mechanical claims 2, 3, 6, 7 re-run on the fixed file: `:498` names all four model fields, `:60` lists them, one `Total:` hit each (`:821`, `:997`); line numbers in the snapshot are older (N1) |

### qa-evidence-quality-report (item 2.10)

| Check id | Result | Evidence now |
|---|---|---|
| qa-evidence-quality-report:C1 | PASS | Every edited region was re-read: lines 1-80, 205-235, 351-520, 726-775, 819, 857, 868-904, 965-1025 |
| qa-evidence-quality-report:C2 | PASS | `:457` field names and nesting still trace to research/04:45-46 |
| qa-evidence-quality-report:C3 | PASS | `:457` "None for a row with no `worker-show` result" traces to research/04:54 and the 50-call cap |
| qa-evidence-quality-report:C4 | PASS | `:470` forms trace to research/04:51 and :129 |
| qa-evidence-quality-report:C6 | PASS | Status values and the open-window rule at `:498` and `:889` trace to research/04:50 and :52 |
| qa-evidence-quality-report:C10 | PASS | `:30` and `:457` state 1.4.245; `package.json` value is quoted at `:30` |
| qa-evidence-quality-report:C12 | PASS | Fixtures at `:742` and `:743` use supported shapes; the realism note F19 stays a minor note |
| qa-evidence-quality-report:C13 | PASS | `:1025` row and `:1015` m2 wording |
| qa-evidence-quality-report:C14 | PASS | Only the permitted forward reference to R3-B2 is present (`:498`); `Grep` for R3-B2 finds `:10` and `:498` |

### qa-internal-consistency-report (item 2.9)

| Check id | Result | Evidence now |
|---|---|---|
| qa-internal-consistency-report:C1 | PASS | Four read fields exist in the 7.2 table with the same names and types (`:457`, `:459`) |
| qa-internal-consistency-report:C2 | PASS | Join fields unchanged in the 7.2 table and `:497-:498` |
| qa-internal-consistency-report:C3 | PASS | `:456` now types `collected_start` and `collected_end` as aware UTC `datetime`; the cycle-0 minor note is closed |
| qa-internal-consistency-report:C4 | PASS | `:400` names `first_record_ts` and `last_record_ts` |
| qa-internal-consistency-report:C5 | PASS | `:60` lists the same names as the model |
| qa-internal-consistency-report:C6 | PASS | `:889` names the bundle fields and maps to `:457` |
| qa-internal-consistency-report:C7 | PASS | `:995` names the same fields; its behaviour agrees with `:498` for a no-window row |
| qa-internal-consistency-report:C8 | PASS | `:1025` names the fields; `:1015` m2 wording fixed |
| qa-internal-consistency-report:C9 | PASS | Section 11 (`:742`, `:743`) and section 12 (`:768`) use the model names |
| qa-internal-consistency-report:C10 | PASS | Grep for UNVERIFIED now gives 13 lines (`:49`, `:65`, `:126`, `:457`, `:498`, `:520`, `:607`, `:889`, `:900`, `:956`, `:987`, `:995`, `:1025`); the new ones at `:457`, `:498`, `:889`, `:995`, `:1025` all agree with open item 23 |
| qa-internal-consistency-report:C11 | PASS | `:9` still describes R3-B1 as the open finding, correct until the gate closes |
| qa-internal-consistency-report:C12 | PASS | Edits agree with research/04 section 2.2 except the intended F1, F2, F6 departures |
| qa-internal-consistency-report:C13 | PASS | `:470` forms and the fixture forms at `:742` agree |
| qa-internal-consistency-report:C14 | PASS | `:498` rule agrees with the window fixtures at `:743` (inclusive, seconds cut, status values) |
| qa-internal-consistency-report:C15 | PASS | The counts reproduce (0 dashes, no TODO or TBD, 9 deviations, 23 open items); the file is 1025 lines now (N1) |
| qa-internal-consistency-report:C16 | PASS | None-handling of `dispatch_started`, `dispatch_ended`, `dispatch_status` stated at `:498`; `tail_complete` is a bool, never None |

### qa-numbers-metrics-report (item 2.13)

| Check id | Result | Evidence now |
|---|---|---|
| qa-numbers-metrics-report:C1 | PASS | Six named fixtures in the `test_probes_allowlist.py` cell (`:742`); "the six reader and parser fixtures" at `:768` |
| qa-numbers-metrics-report:C2 | PASS | The `test_classify.py` cell (`:743`) names 5 R3-B1 window fixtures now (F6 added one); no DESIGN sentence states a count of four window fixtures; the only count word found is "four cases" at `:501`, which counts guard cases (N3) |
| qa-numbers-metrics-report:C3 | PASS | 9 `D` rows by Grep; `Total: 9 deviations.` at `:821` |
| qa-numbers-metrics-report:C4 | PASS | 23 numbered rows (`:973` to `:995`); `Total: 23 open items.` at `:997` |
| qa-numbers-metrics-report:C5 | PASS | 256 KiB at `:317`, `:400`, `:459`, `:513`, `:546` (`256 * 1024`), `:742`, `:991`, `:1017`; no other value |
| qa-numbers-metrics-report:C6 | PASS | Grep for em-dash, en-dash and ` -- ` gives 0 |
| qa-numbers-metrics-report:C7 | PASS | Per-section rule of item 2.7 holds on the fixed file: 7.2 (`:457`, `:459`), 2.2 (`:60`) and 18 (`:1025`) hold all four model names; 7.1 holds `first_record_ts` (`:400`); 11 holds all four (`:742`, `:743`); 15.1 (`:889`) and 17 (`:995`) hold the three source names. The snapshot's cell values differ from the fixed file (N1) |
| qa-numbers-metrics-report:C8 | PASS | The seven mechanical rules reproduce on the fixed file (see Mechanical gate re-check); snapshot line numbers are older (N1) |
| qa-numbers-metrics-report:C9 | PASS | Fixture values at `:742` and `:743` still equal research/04 section 2.3 |
| qa-numbers-metrics-report:C10 | PASS | Window arithmetic at `:743` unchanged |
| qa-numbers-metrics-report:C11 | PASS | "all three are None" (`:457`), "the three fields" (`:498`), three source names at `:889` and `:995` |
| qa-numbers-metrics-report:C12 | PASS | 9 rules (`:478` to `:486`), 13 capture items (`:886` to `:898`), 8 templates and 7 verbs (`:534`), 4 join-incomplete cases (`:501`, `:768`), 7 new test files (conftest plus six, `:730`, `:741` to `:746`), 3 blocking findings (`:7`), 23 open items |
| qa-numbers-metrics-report:C13 | PASS | `:743` FR-008, FR-009 and FR-010 counts untouched |
| qa-numbers-metrics-report:C14 | PASS | Section 8 text unchanged by the fix (`:682` "giving 9" present) |
| qa-numbers-metrics-report:C16 | PASS | New text (`:390`, `:391`, `:400`, `:457`, `:459`, `:470`, `:498`, `:742`, `:743`, `:889`, `:995`, `:1025`) points to sections by name, never to a DESIGN line number |
| qa-numbers-metrics-report:C18 | PASS | `pyproject.toml:16` `requires-python = ">=3.10"`; `:470` Python 3.10 `Z` claim |

### qa-spec-fidelity-report (item 2.16)

| Check id | Result | Evidence now |
|---|---|---|
| qa-spec-fidelity-report:C1 | PASS | `ALLOWED_ORCA` at `:525` to `:534`: 8 templates, 7 verbs, unchanged |
| qa-spec-fidelity-report:C2 | PASS | `FORBIDDEN_TOKENS` at `:536` unchanged; `parse_worker_show` and `parse_time` add no verb, flag or token |
| qa-spec-fidelity-report:C3 | PASS | `parse_worker_show` takes the `worker-list` row and the `worker-show` result (existing templates `:527`, `:528`); `first_record_ts` still comes from the transcript read (`:400`) |
| qa-spec-fidelity-report:C4 | PASS | D9 row `:819` not weakened; its sentences about path B stay true |
| qa-spec-fidelity-report:C5 | PASS | FR-010 guard text at `:499` to `:501` unchanged |
| qa-spec-fidelity-report:C6 | PASS | SP-29 row `:857`; path B yields False or None, never True (`:498`) |
| qa-spec-fidelity-report:C7 | PASS | Edits 1 to 9 match research/04 lines 87-95 apart from the intended F1, F2, F6 changes |
| qa-spec-fidelity-report:C9 | PASS | Names exist in the 1.4.245 bundle per research/04:45-46; DESIGN keeps them UNVERIFIED live |
| qa-spec-fidelity-report:C10 | PASS | `pending`, `dispatched` match research/04:50 |
| qa-spec-fidelity-report:C11 | PASS | Section 7.4 (`:558` to `:594`) is not named by any fix-log row; `tail_complete` is a model field only |
| qa-spec-fidelity-report:C12 | PASS | `:821`, `:997`, 0 dashes, no TODO or TBD |
| qa-spec-fidelity-report:C13 | PASS | Only the forward reference to R3-B2 (`:498`); `### Fix cycle 3` holds one row (`:1025`); the new `tail_complete` sentence is R3-B1 content (F6) |
| qa-spec-fidelity-report:C14 | PASS | `:768` FR-010 trace and the Covers cell at `:742` carry the Gap 4 recommendation |

### qa-template-conformance-report (item 2.8)

| Check id | Result | Evidence now |
|---|---|---|
| qa-template-conformance-report:C1 | PASS | Regex for a 4-cell row matches the GQ-103(3) row at `:60` exactly once |
| qa-template-conformance-report:C2 | PASS | Row `:457` matches the 2-cell regex with `\|` escapes intact |
| qa-template-conformance-report:C3 | PASS | Row `:459` matches the 2-cell regex with `\|` escapes intact |
| qa-template-conformance-report:C4 | PASS | Rows `:742` and `:743` both match the 3-cell regex (count 2) |
| qa-template-conformance-report:C5 | PASS | Row `:889` matches the 3-cell shape; row `:995` matches the 4-cell shape |
| qa-template-conformance-report:C6 | PASS | `:1022` blank, `:1023` header, `:1024` separator, `:1025` one 3-cell row; same layout as cycle 2 (`:1011` to `:1017`) |
| qa-template-conformance-report:C7 | PASS | `:1021` intro unchanged; cycle-0 note m1 stays a minor note |
| qa-template-conformance-report:C8 | PASS | Section map: 47 headings, same text as before, `### Fix cycle 3` is the last; no numbered heading added or renumbered |
| qa-template-conformance-report:C9 | PASS | Dash and ` -- ` count 0 |
| qa-template-conformance-report:C10 | PASS | TODO, TBD, FIXME, case-insensitive: 0 |
| qa-template-conformance-report:C11 | PASS | Marketing-word Grep (robust, seamless, powerful, comprehensive, leverage, elegant, holistic, cutting-edge, best-in-class): no hits |
| qa-template-conformance-report:C12 | PASS | New text uses short declarative sentences and no DESIGN line-number cross-references; the long sentence at `:470` is minor note F14 |
| qa-template-conformance-report:C13 | PASS | All nine edits at their anchors; fixtures named at `:742` and `:743`; FR-010 row `:768` |
| qa-template-conformance-report:C14 | PASS | Totals at `:821` and `:997` |

Check count: 129 of 129 PASS. The 136 items verified in total are these 129 checks plus the 7 findings above.

---

## Mechanical gate re-check (item 2.7 rules against the fixed file)

| Rule | Result on the fixed file |
|---|---|
| (1) Per-section matrix | 7.2 (`:457`, `:459`), 2.2 (`:60`) and 18 (`:1025`) each hold `first_record_ts`, `dispatch_started`, `dispatch_ended`, `dispatch_status`; 7.1 holds `first_record_ts` (`:400`); 11 holds all four (`:742`, `:743`); 15.1 (`:889`) and 17 (`:995`) hold `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status`. Holds. |
| (2) Worker bullet names the four fields | `:498`. Holds. |
| (3) GQ-103(3) lists the four names | `:60`. Holds. |
| (4) Em-dash count 0 | Grep gives 0 (also 0 for en-dash and ` -- `). Holds. |
| (5) No TODO or TBD | Grep gives 0 (case-insensitive, also FIXME). Holds. |
| (6) One `Total: 9 deviations.` | `:821`. Holds. |
| (7) One `Total: 23 open items.` | `:997`. Holds. |

External facts re-checked in the installed bundle `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`: one line carries `dispatchedAt:<x>.dispatched_at,completedAt:<x>.completed_at` (supports spec-fidelity C9 and evidence C2), and 50 lines carry `'pending', 'dispatched'` (supports domain C12 and spec-fidelity C10). The live `worker-show` output stays UNVERIFIED, as the DESIGN now says.

---

## New BLOCKING or MAJOR findings

None. Every fix was read for new defects, not only for presence. Checked and found sound: the new `parse_time` and `parse_worker_show` signatures sit inside the existing `probes -> models` import direction (`:211`, `:215`) and add no Orca template; `parse_worker_show` honours the existing "`worker-show` value wins" rule (`:509`); the `tail_complete` rule runs only after the window is found observable, so `Dispatch time window not observable` (open item 23, `:995`) still holds as the only outcome until step 1.0a closes; the new fixture `test_path_b_incomplete_tail_has_no_session_start` (`:743`) uses a window (10:00:00 to 11:00:00) and a `first_record_ts` (10:30:00) that would otherwise join, so it tests the new rule and nothing else; table shapes of every edited row are intact (regex check above).

## Notes (MINOR; recorded, not graded, not rechecked later)

| Id | Note | Where |
|---|---|---|
| N1 | `phase-outputs/test-results/r3-b1-mechanical.md` is a pre-fix snapshot: it says "1023 lines" and its line numbers (398, 455, 457, 496, 740, 741, 887, 993, 1023) and some matrix cells (for example 7.1 `dispatch_started` 0, now 1 because of `parse_worker_show` at `:391`) no longer match the 1025-line file. The seven rules it tests all still hold (table above) and the fix log's "Orchestrator re-check" supersedes it. A moved line number on a true claim is minor; no re-run is needed. | `r3-b1-mechanical.md:3`, `:59-77`, `:105-113` |
| N2 | The D9 row (`:819`) and SP-29 row (`:857`) say a path-B join "also needs the Dispatch row's time window" but do not mention that the transcript tail must be complete. `:498` and the FR-010 trace row (`:768`) do. Not a contradiction. | `:819`, `:857` |
| N3 | The R3-B1 classify fixtures are 5 now (F6 added one on purpose); research/09 Gap 4 and cycle-0 reports counted 4. No DESIGN text states the old count. Item 3.1 adds the R3-B2 and R3-B3 fixtures to the same cell, so its own count must start from 5. | `:743`, `research/09-gap-fill.md:223` |
| N4 | `:498` now says the transcript is None with note `session start not observable: transcript tail only` for the incomplete-tail case. Item 3.1 writes the general transcript outcome for a path-B match that does not join; it must keep this sentence and not contradict it. | `:498`, item 3.1 |
| N5 | Cycle-0 minor findings R3B1-F8 to R3B1-F24 are left as notes by design. F17 and F18 are partly overlapped by the F1 and F2 edits. Merged minor items that the F4 and F5 edits also closed: the `datetime` may-import row (`:211`) and the untyped `collected_start` (`:456`). F13 (the Fix cycle 3 intro wording) remains open as a note. | per cycle-0 list |

## Cycle accounting

| Cycle | PASS set size | F set | \|F\| | Outcome |
|---|---|---|---|---|
| 0 | 129 | R3B1-F1 to R3B1-F7 | 7 | consolidated |
| 1 (this report) | 129 of 129 still PASS | none | 0 | all 7 RESOLVED |

Regression check (runs first): no check in the cycle-0 PASS set fails now, so no regression halt. Monotonicity: \|F_1\| = 0 < \|F_0\| = 7, so no `[HALT-MONOTONICITY]`.

## Confidence

**Confidence:** Verified: 136/136 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 24 | Grep: 36 | Glob: 2 | Bash: 0. Edit and Write calls touched only this report.
Items marked VERIFIED rest on a tool call against the current DESIGN, on research/04, research/09, `pyproject.toml` or the installed Orca bundle, not on the earlier reports. The `git merge-base` ancestry check of `5dc29d23` (crossref C14) was not re-run; the DESIGN text it checks (`:1021`) is unchanged and `5dc29d23` is the newest commit in the session's recent-commit list, so it is an ancestor of HEAD.

Verdict: PASS
Blocking count: 0
