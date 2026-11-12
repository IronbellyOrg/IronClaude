# Handoff: step 3, bmad-ux (CU, headless), orca-observer
**Outputs:** `ux-orca-observer/` here, identical to Coder `_bmad-output/planning-artifacts/orca-observer/ux-designs/ux-orca-observer-2026-11-08/`. Files: DESIGN.md, EXPERIENCE.md, .memlog.md (22 entries), .working/, review-rubric.{json,md}, review-adversarial.json, review-adversarial-3.json, validation-report.{html,md}. Both spines are still `status: draft`; 5 blockers are open.

**What the spec locks:**
- R1 is the Signal Bridge worker ledger on `worker-list`, with the gap notice "question source UNVERIFIED". The ledger layout is flagged open.
- Bands are 160/116/80 columns, with a notice below 80. The 44-row budget, the 12-row minimum and the shrink order are PROPOSED.
- The key model and focus sit behind the key-reader spike gate. `NO_COLOR` and `--ascii` fallbacks exist for every glyph.
- State words: unknown, stale, partial, not-observed and failed, never 0 or false. A timeout shows `FAILED (timeout)` (T5).
- A cut cell ends in `>`. Untrusted text is sanitized and shown literally. The inspector shows full IDs. Nothing blinks.
- The per-cycle `export(view)` JSON snapshot is separate from the `e`/`--once` text export.
- Write-back is a future section with no R1 controls. Images are cited only through their .txt exports.

**Screens (9):** R0 fixture gallery; R1 ledger, inspector, too-small diagnostic, text export; B Attention Ledger, question inspector; C Decision Desk, affected-session inspector.

**Open questions:** UX-OQ-1 to UX-OQ-8. They include the export and snapshot paths (4), the cursor glyph against `>` (5), the palette taken from the prototype only (7), and T20 worktree naming with no worktree column (8). The PRD's OQ/OI items are carried as written.

**Validation:** 21 findings, 5 of them blocking, all fixed in cycle 1. Visual reference coverage was rated "thin". The rendered report lists every review's findings as recorded, including those later fixed.

**Review 2 (fresh context):** FAIL, 3 blocking. All 3 were fixed in cycle 2: the PARTIAL example now matches the 5-call cap (T4); the 44-row claim now cites design PLAN.md:57; the text export writes `unknown`.

**Review 3 of 3 (fresh context): FAIL, 5 blocking and 8 minor. All 5 are OPEN because the review cap is reached:**
1. The fixture header must read `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17). The T50 label is a separate marking on each R0 render. My cycle-1 fix wrongly merged the two, at EXPERIENCE.md:64/215/296/490 and DESIGN.md:121.
2. EXPERIENCE.md:54 says the spec and PRD never mention the PLAN.md cockpit. That is false: rendering-rules.md:8 mentions it.
3. `cycle overran (Ns)` belongs on the freshness strip, not the status line (EXPERIENCE.md:292). Sources: adapter-contract.md:26, NFR-7, T40.
4. The state tables leave out `FAILED (shape)`, `reported unknown` (T32) and the T22 flags `order unknown` and `conflict (time went back)`.
5. EXPERIENCE.md:135 labels the never-drop list "spec", but the spec fixes only COUNTS; the other rows are PROPOSED.

**UNVERIFIED or not done:** the contrast ratios (from QA.md:13), the palette and the per-call timeout (OI-1) are UNVERIFIED. The 5 blockers above are unfixed. No epics, stories or tasks were made. Nothing was committed.

## Fix-only pass (owner decision 2026-11-08)

The owner decided "stop and fix UX first". The 5 blocking findings of review-adversarial-3.json were fixed by text edit in EXPERIENCE.md and DESIGN.md. They were **NOT re-reviewed**: no review, validation, adversarial pass or BMAD skill was run after the edits. Evidence per finding (file:line before and after, source file:line, grep/diff proof) is in `ux-orca-observer/fix-log.md`; `.memlog.md` now has 27 entries (5 added, one per fix).

1. Fixture header: fixed. It now reads `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17); the T50 marking stays a separate per-render marking (acceptance-tests.md:44).
2. EXPERIENCE.md:54: fixed; the finding was only partly correct. The "built layout" half was false (rendering-rules.md:8, :85) and is corrected. The "PLAN.md cockpit" half was true (no spec or PRD line names it) and is kept. Item 2 above misstates this: rendering-rules.md:8 mentions the built prototype, not the cockpit.
3. `cycle overran (Ns)`: fixed; moved to the freshness strip (adapter-contract.md:26, T40). The dispatch brief worded this finding the other way round; the sources were followed.
4. State strings: fixed. Added `FAILED (shape)` with the last good snapshot kept and `reported unknown` (T32), `order unknown` and `conflict (time went back)` (T22), `reported T (page k)` (rendering-rules.md:55) and `one Run only` after `bound` (adapter-contract.md:63).
5. Never-drop list: fixed. Only COUNTS (rendering-rules.md:19) and coverage/scope/PARTIAL (rendering-rules.md:13) cite the spec; the other rows are PROPOSED.

**Still open:**
- the 8 minor findings of review-adversarial-3.json (untouched);
- UX-OQ-1 to UX-OQ-8, and the PRD's OQ/OI items (unchanged, unresolved);
- the contrast ratios, the palette and the per-call timeout (OI-1), still UNVERIFIED;
- both spines still `status: draft`. Nothing was committed or pushed.
