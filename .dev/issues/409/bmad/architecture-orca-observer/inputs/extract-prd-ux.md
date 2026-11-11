# Extract: PRD + UX inputs for orca-observer architecture

Read-only extract, 2026-11-08. Paths: PRD = `planning-artifacts/orca-observer/prd.md` (P), addendum.md (A); UX = `ux-designs/ux-orca-observer-2026-11-08/` DESIGN.md (D), EXPERIENCE.md (E); spec = `specs/spec-orca-observer/` rendering-rules.md (RR), adapter-contract.md (AC); handoffs = IronClaude `.dev/issues/409/bmad/handoff-step2.md` (H2), handoff-step3.md (H3). Evidence labels are copied as written.
## 1. PRD requirement index

Counts: 18 FR (R0 2, R1 14, R2 1, R3 1), 14 NFR (A:50-51). NFRs apply to every release (P:265).

| ID | Stage | Gist | Line |
|---|---|---|---|
| FR-1 | R0 | Offline fixture replay of A/B/C at 160/116/80, degraded beside each | P:124 |
| FR-2 | R0 | Key-reader spike first; Rich if pass, Textual if fail, never both | P:132 |
| FR-3 | R1 | One ledger row per `worker-list` dispatch, fields shown raw | P:138 |
| FR-4 | R1 | Each row one distinct dispatch; no session/worktree 1:1 assumed | P:144 |
| FR-5 | R1 | Hide/show historical (released or retained) rows | P:151 |
| FR-6 | R1 | One stable view per session; `read k of N Runs` placement open | P:155 |
| FR-7 | R1 | Notice above ledger: questions not observed in R1 | P:162 |
| FR-8 | R1 | Collected vs reported, and in what scope | P:171 |
| FR-9 | R1 | Freshness per fact; stale distinguished from failed | P:178 |
| FR-10 | R1 | Counts never overstate (`n+? (k unknown)`, no bars) | P:185 |
| FR-11 | R1 | Lifecycle, outcome, report, acceptance, tests, approval as separate facts | P:192 |
| FR-12 | R1 | No conclusion beyond evidence (no inferred failure/conflict/admission) | P:198 |
| FR-13 | R1 | Select a row, inspect full evidence; identity-anchored selection | P:209 |
| FR-14 | R1 | Changes since last look, session memory only | P:219 |
| FR-15 | R1 | Plain-text export of the shown view, any platform | P:228 |
| FR-16 | R1 | Versioned additive-only JSON snapshot each cycle (schema PROPOSED) | P:235 |
| FR-17 | R2 | Open human questions retained until closure evidence; seen not resolved | P:244 |
| FR-18 | R3 | Selected question's affected sessions with worker-list evidence | P:256 |
| NFR-1 | all | 160/116/80 legible, `cell_len <= W`; <80 notice; height rule (OQ-14) | P:269 |
| NFR-2 | all | `NO_COLOR=1`/`yes` emits no colour SGR | P:270 |
| NFR-3 | all | `--ascii` replaces box drawing with `+-\|`; plain exports | P:271 |
| NFR-4 | all | No blink (SGR 5/6), no compulsory motion | P:272 |
| NFR-5 | all | Fixed key map, no `r`, no mouse, no key maps to Orca call | P:273 |
| NFR-6 | all | Sanitize CSI/OSC/C1/C0/Cf; literal text; cell-width truncation | P:274 |
| NFR-7 | all | 15 s cycle, <=5 subprocesses, 8 MiB cap, back-off to 60 s | P:275 |
| NFR-8 | all | Deterministic, no LLM loop; same input byte-identical | P:276 |
| NFR-9 | all | Read-only: one argv template plus discovery probe; forbidden set | P:277 |
| NFR-10 | all | No bodies, prompts, file contents, credentials anywhere | P:278 |
| NFR-11 | all | Unknown never 0/false/blank/null; missing binary named | P:279 |
| NFR-12 | all | Key reader restores terminal in `finally`, SIGINT/SIGTERM | P:280 |
| NFR-13 | all | Interactive POSIX only; `--once` everywhere (Windows UNVERIFIED) | P:281 |
| NFR-14 | all | No TUIBBS dependency, no AGPL copy, never import `canvas.py` | P:282 |

## 2. Open owner questions OQ-1..OQ-15

Live in P:414-432 (section 12.1, "carried verbatim from SPEC.md; not resolved here", P:416); H2:14 says SPEC.md:99-113; count 15 at A:52. Owner-decision mapping in P:459-472; also carried in E:533. Separate 13 open items OI-1..OI-13 at P:434-453.

- OQ-1 Does the staged choice satisfy DIRECTION-SELECTED; where is the record? (P:418)
- OQ-2 Which production-integration reading applies, 1 or 2? (P:419)
- OQ-3 Final command name (recommended `superclaude observe`)? (P:420)
- OQ-4 Fallback date for QUESTION-OBSERVATION? (P:421)
- OQ-5 Sample capture and acquisition permission for live reads? (P:422)
- OQ-6 Message-content exposure (display vs export)? (P:423)
- OQ-7 What identifies a human question? (P:424)
- OQ-8 Multi-observer restriction? (P:425)
- OQ-9 Licence opinion before any Go screen reads the snapshot? (P:426)
- OQ-10 Does TUIBBS become the staff platform? (P:427)
- OQ-11 Is the write-back boundary change approved? (P:428)
- OQ-12 Authoritative snapshot row order: timestamp vs source newest-first? (P:429)
- OQ-13 `read k of N Runs since start`: B header only or every header? CONTRADICTION (P:430)
- OQ-14 Contents of A width matrix, B coordinates, C 44-row contract? (P:431)
- OQ-15 Which `projection.stage.*` subfield drives change detection; stage.detail/activity in snapshot? (P:432)

## 3. FR-8 and the PARTIAL definition (H2:19-21 asked for this recheck)

- PRD glossary P:88: "Collection states: paging stopped at the per-cycle call cap while `page.hasMore` was still true, or an empty page arrived while reported T was above 0 (`PARTIAL (empty page k)`) ...". P:89 Mismatch: "Traversal finished, but collected n is not reported T: `collected n / reported T (mismatch)`. Not PARTIAL".
- PRD FR-8 P:174: "A finished traversal where collected n differs from reported T renders `collected n / reported T (mismatch)` (rendering-rules.md), pinned by T47." P:175: "At the 5-call cap the screen shows `PARTIAL: collected 500 of reported T` (T4)."
- Spec RR:55: "if `page.hasMore` is still true at the call cap: `PARTIAL: collected n of reported T (newest first; oldest rows not read; long-running active workers may be among them)`. ... Finished traversal with n not T: `collected n / reported T (mismatch)`. `workers=[]` with T above 0 ends as `PARTIAL (empty page k)`."
- Spec AC:15: "Following a cursor goes through a guard that marks the view PARTIAL when the per-cycle cap stops it." (The empty-page trigger is at AC:49, not AC:15.)

**Verdict: CONSISTENT** in meaning: both PARTIAL triggers (cap with `hasMore` true; empty page with T>0) and the separate non-PARTIAL mismatch string match RR:55 and AC:15+49. Exact differences, all textual:
1. P:175 quotes the cap string without RR:55's parenthetical `(newest first; oldest rows not read; long-running active workers may be among them)`; the renderer must emit the full RR:55 string (E:279 does).
2. AC:15 names only the cap trigger; the empty-page trigger lives at AC:49.
3. FR-8 (P:174) also carries R2-only question-area strings inside an R1 requirement (H2:24, minor M6, not acted on).

## 4. UX facts the architecture must honour

**Keys and key reader**
- Key map: Up/Down or `j`/`k`, `Enter`, `Esc`, `/`, `h`, `m`, `e`, `q`, `Backspace` (filter), `Ctrl-C` = SIGINT quit (E:309-322; P:273). No `r`, no help key, no mouse; no key maps to an Orca call (T3); unknown keys do nothing (E:324-325).
- Three focus modes, one at a time: ledger, inspector, filter input; in filter mode `j`/`k`/`h`/`m`/`e`/`q` are typed as text (E:313-320, E:327-330). Esc clear-filter / cancel-edit is PROPOSED (E:315).
- Refresh never moves focus or selection, never closes inspector/filter, never clears typed filter text (E:332).
- Key-reader spike is the R0 gate: Rich Live + POSIX termios/tty/select; Textual only if it fails, never both (E:335-337; P:132). Spike criteria are PROPOSED (UX-OQ-6): lone Esc vs arrow sequences within a short timeout; no lost/reordered filter input during redraw; identity-stable selection across reorder; terminal restored on `q`, Ctrl-C, SIGTERM, unhandled exception; resize redraw within one cycle; no flicker at 160/116/80 (E:339-344). Terminal restore in `finally` + SIGINT/SIGTERM (P:280). UX rules unchanged if Textual replaces Rich (E:346).

**Refresh and clock**
- Fixed 15 s cycle, no manual refresh; layout recomputed on every resize and every refresh (E:90, E:324). Cycles never overlap, <=5 subprocesses, back-off to 60 s (P:275).
- STALE after 3 intervals (45 s) with no successful poll, on a local monotonic clock; wall clock only prints `HH:MM` (RR:53; E:278; P:180). Poll age and evidence age separate; no per-row STALE (RR:54; P:182).
- `m` mark is in-memory, per process; first observation is the baseline; restart announces a new baseline (E:348-353; RR:46).
- Repaint in place; no transitions, no auto-scroll (E:355-359).

**Width breakpoints** (E:101-129)
- >=160 full table (9 columns, RR:29); 116-159 line form `<kind> <dispatchId> <liveness.verdict> <age>`; 80-115 short form with ID cut by `>`; <80 `terminal too narrow (min 80)` above COUNTS, denominators still print (E:105-108; P:269). No interpolation between bands (E:129). Column budgets are PROPOSED (E:110-127). Every line `cell_len <= W` (T23), widths in display cells (E:90).
- Height: 44-row budget, 12-row minimum and shrink order are PROPOSED (E:133-163; UX-OQ-2; OQ-14). Spec-fixed only: COUNTS never dropped (RR:19) and coverage/scope/PARTIAL as minimum content (RR:13) (E:135).

**NO_COLOR / ASCII**
- `NO_COLOR=1`/`yes` (non-empty) -> no colour SGR; labels/glyphs/layout unchanged; muted `unknown` -> plain (E:392-394; D:140). Meaning never by colour alone (E:388-391).
- `--ascii`: box glyphs -> `+ - |`, `·` -> `.`, selection `▸` -> `@` (PROPOSED), `>` and `*` unchanged (D:181-193). Other non-ASCII source chars -> `?` after sanitizing (PROPOSED, D:195).
- No SGR 2 (faint), italic, underline, SGR 5/6 (D:147-148). Observer never paints the background (D:111-113). Palette and contrast ratios UNVERIFIED (D:128; E:396; UX-OQ-7). Raw worker fields never coloured good/bad (D:126).

**State words** (E:272-298): `unknown` / `unknown (absent in source)` / `n+? (k unknown)`; `unavailable (no source)`; `STALE <age>` with `as of HH:MM:SS`; PARTIAL forms incl. `reported T (page k)`, `reported T1-T2 (changed during read)`, mismatch, `PARTIAL (empty page k)`, `reported unknown` (T32); `NOT POLLED`, `messages UNVERIFIED (not read)`, `not reobserved`, `selected <id> no longer in source window`; `FAILED (<exit code or timeout>) <age>`, `FAILED (timeout)` (T5), `FAILED (shape)` keeping last good snapshot (T32); `STALE <age>, last poll FAILED (<reason>)` is PROPOSED. Only the source cell fails, never row values (E:281). Missing binary: `worker-list NOT AVAILABLE (orca binary not found)` (E:184, E:292). `cycle overran (Ns)` on the freshness strip (E:293). Row-order flags `order unknown`, `conflict (time went back)` (E:296). Fixture header `SYNTHETIC FIXTURE <variant>, not Orca data` plus separate T50 marking (E:298).

**Empty and loading states**: live empty `worker-list returned 0 workers in scope=<scope>`; fixture `no observed items in this source window; not proof none exist` (T33) (E:288; P:167). Loading: `worker-list NOT POLLED` (spec); header/COUNTS/ledger loading text PROPOSED (E:287). Never `no questions` (P:167).

**R1 notice** (E:378-384; P:164): `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` above the ledger in every view and width until QUESTION-OBSERVATION passes and the source has succeeded in this process; no number, nothing from `result.count`. Freshness strip carries `messages UNVERIFIED (not read)` (P:166; E:81).

**Untrusted text** (E:361-376; P:274): all Orca/worker text (stage detail, outcome, kind, IDs, stderr) sanitized before render (CSI/OSC terminated and unterminated, C1, bare C0 except inspector newline, Cf); same sanitized string feeds screen and export; never parsed as Rich markup (`[bold]x[/bold]` prints literally, T44, T29); labelled `worker-reported`; `nextAction.kind` verbatim, only as a labelled local filter; full IDs in inspector and export; cuts never split a wide char (E:305); no bodies/secrets.

**Exports**: `e`/`--once` text export = same view model, no ESC bytes, full IDs, no truncation (T27, T48); JSON snapshot written by `export(view)` every R1 cycle, no key press; destinations unspecified (E:68; E:265-268; UX-OQ-4). Inspector is a full-screen replacement, not a pane; no per-panel scrolling (E:250-252; D:173; E:329).

## 5. UX open questions (E:524-531)

- UX-OQ-1 R1 composition matches neither PLAN.md cockpit nor built `group_a.py`; confirmed look? (E:524)
- UX-OQ-2 Minimum height and drop order vs 48/42-row exports (part of OQ-14) (E:525)
- UX-OQ-3 Which key moves between B and A's ledger? None in spec (E:526)
- UX-OQ-4 Paths/naming of text export and JSON snapshot; message wording (E:527)
- UX-OQ-5 Truncation glyph `>` vs prototype `…`/`~` (E:528)
- UX-OQ-6 Key-reader spike has no spec pass/fail criteria (E:529)
- UX-OQ-7 Palette exists only in prototype `canvas.py:7`; owner to confirm (E:530)
- UX-OQ-8 T20 shared `worktreeId`: must the ledger row name it? (E:531)

## 6. Handoff flags: unverified, dropped, fixed-by-edit and not re-reviewed

PRD (H2):
- Adversarial review 2 FAIL with 2 blocking; B1 (FR-8 mismatch string) and B2 (glossary PARTIAL) fixed in fix cycle 2 and NOT re-verified by a further review (H2:18-21). Section 3 above rechecks them: CONSISTENT.
- 13 adversarial minors M1-M13 and 11 validation minors not acted on; watch M12 (JTBD-4 "exactly the view on screen" vs lossless export CAP-9/T48) and M6 (R2 strings in R1 FR-8) (H2:24).
- 4 prose fixes skipped: proof-list split (could change the gate), "summary decision" renumbering x2 (OI-11), V1/V3 definitions (H2:25).
- `reason unknown` (FR-17/18, A7/A8) is a PRD-added string, not in the spec (H2:26).
- NFR-13 Windows UNVERIFIED until T27 runs on Windows; NFR-1 numeric height blocked on OQ-14 (H2:27).

UX (H3):
- Review 3 of 3 FAIL, 5 blocking; all 5 fixed by text edit in a fix-only pass and **NOT re-reviewed** (no review, validation or BMAD skill run after) (H3:21, H3:30-32). Evidence in `ux-orca-observer/fix-log.md` (H3:32). Fixed items: fixture header vs T50 marking (H3:34); E:54 PLAN.md-cockpit claim, finding only partly correct (H3:35); `cycle overran (Ns)` moved to freshness strip (H3:36); state strings added (H3:37); never-drop list relabelled PROPOSED (H3:38).
- 8 minor findings of review-adversarial-3.json untouched (H3:41).
- Contrast ratios, palette and per-call timeout (OI-1) UNVERIFIED (H3:28, H3:43).
- Visual reference coverage rated "thin" (H3:17). Both spines still `status: draft` (H3:2, H3:44). Ledger layout flagged open (H3:5).
- 44-row budget, 12-row minimum, shrink order PROPOSED (H3:6). Nothing committed in either step (H2:28; H3:44).

