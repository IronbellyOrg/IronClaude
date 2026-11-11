# Validation Report — Orca Observer

- **DESIGN.md:** `/home/coder/workspaces/worktrees/Coder/dashboard-bmad/_bmad-output/planning-artifacts/orca-observer/ux-designs/ux-orca-observer-2026-11-08/DESIGN.md`
- **EXPERIENCE.md:** `/home/coder/workspaces/worktrees/Coder/dashboard-bmad/_bmad-output/planning-artifacts/orca-observer/ux-designs/ux-orca-observer-2026-11-08/EXPERIENCE.md`
- **Run at:** 2026-11-08T19:21:33Z

## Overall verdict
The spine pair is a usable contract: every YAML token resolves, every colour is hex, every UJ has a protagonist, numbered steps, a climax and a failure path, and the binding owner decisions (R1 scope, later B/C, read-only, PROPOSED numbers, open questions) are applied consistently. Five real defects remain. UJ-1's timeout failure path contradicts T5. The shrink rule drops the never-dropped gap notice. The T50 fixture label is missing. FR-16's per-cycle snapshot is reduced to an on-demand export. The ledger has no column that can satisfy T20's 'each naming it' worktree rule. Visual-reference hygiene is thin: imports/ is empty, the design-package source path does not resolve from the repo, and no spines-win-on-conflict line exists.

FAIL: five blocking defects. The fixture header string contradicts the spec, a claim about the sources is false, the overrun string is placed against three sources, the state vocabulary omits test-pinned strings, and a PROPOSED row list is labelled spec.

FAIL: three blocking defects, namely a false claim about the design sources (no source states 44 rows), a PARTIAL example that cannot happen under the 5-call cap pinned by T4, and an uncited rule that the plain-text export writes UNKNOWN where the screen writes unknown. The required coverage items are all present and the owner decisions are respected.

## Category verdicts
- Flow coverage — adequate
- Token completeness — adequate
- Component coverage — adequate
- State coverage — adequate
- Visual reference coverage — thin
- Bloat & overspecification — adequate
- Inheritance discipline — adequate
- Shape fit — strong

## Findings by severity

### Critical (0)

### High (2)
**[Flow coverage]** (blocking) — The UJ-1 failure path says that when 'the poll times out three times in a row' the freshness cell turns to `STALE 52s` and 'Nothing becomes failed'. The sources say a timed-out call shows `FAILED (timeout)` (prd.md:181, T5 in acceptance-tests.md:12). 'Never turned into failed' in rendering-rules.md:53 is about values, not the source cell. The spine also never says which word wins when a source is both failed and past 45 s with no success. (§ EXPERIENCE.md § Key Flows > UJ-1 Fleet glance (R1) failure path; § State Patterns > State vocabulary (stale / failed rows))
Fix: Rewrite the failure path so each timeout shows `FAILED (timeout) <age>` and values keep `as of HH:MM:SS`. Add one precedence rule for the freshness cell when FAILED and STALE both apply. If the sources do not decide it, mark the rule PROPOSED or carry it as an open question.

**[Adversarial verification 3 of 3 (fresh context)]** (blocking) — The fixture header string contradicts the spec. EXPERIENCE.md:296 puts `synthetic fixture, not live evidence (<variant>)` in the header on every frame, and DESIGN.md:121 uses the same badge text. rendering-rules.md:17 fixes the header: 'Fixture mode always reads `SYNTHETIC FIXTURE <variant>, not Orca data`'. The T50 label (acceptance-tests.md:44, rendering-rules.md:5, release-gates.md:9) is a per-render R0 marking, not the header string. The spine merges the two into one header string that the spec does not define, and calls it 'verbatim'. (§ EXPERIENCE.md:296)
Fix: Make the header read `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17). Keep `synthetic fixture, not live evidence` as the T50 marking on each R0 render (EXPERIENCE.md:64). Update the badge text at DESIGN.md:121 to match, or show both strings and cite each one.


### Medium (25)
**[Flow coverage]** (blocking) — FR-16 (prd.md:86, 235) requires a versioned JSON snapshot written by `export(view)` on each R1 cycle (snapshot-export-schema.md 'Envelope (one per cycle)'; SPEC.md CAP-10). The spine instead attaches the JSON snapshot only to the `e` key and `--once`, and never mentions a per-cycle write. A consumer following the spine would never write the snapshot on its own. (§ EXPERIENCE.md § Information Architecture > Screen inventory row 4; § Key Flows > UJ-4 Export step 2)
Fix: Separate the record export (`e` / `--once`, T27/T48) from the per-cycle snapshot (FR-16). State where and when the snapshot is written, or carry its destination with UX-OQ-4.

**[Flow coverage]** — The R0 owner-review flow leaves out the walkthrough task that the source makes the core of the review: 'find the oldest question and inspect its evidence' (prd.md:463, release-gates.md:9). The climax jumps straight to recording a direction. (§ EXPERIENCE.md § Key Flows > R0 owner review)
Fix: Add a step where the reviewer performs the walkthrough task on each direction's fixture render before recording the selection.

**[Token completeness]** — Several rendered states have no colour token. The freshness strip lists okColor, staleColor, failedColor, notPolledColor and unverifiedColor, but has nothing for `NOT AVAILABLE (orca binary not found)`. There is no token or component for the `terminal too narrow (min 80)` line, `cycle overran (Ns)`, the new-baseline notice, `selected <id> no longer in source window`, or the full PARTIAL sentence on the muted status line (PARTIAL is warn in the COUNTS strip). (§ DESIGN.md frontmatter components.freshness-strip / status-line / ledger-row; § Components)
Fix: Add notAvailableColor (probably warn or bad) to freshness-strip. Give the status line a partialColor and a warnColor. Name the colour of the under-80 notice and the vanished-selection row.

**[Component coverage]** — `{components.status-line}` has a DESIGN row but no EXPERIENCE Component Patterns entry. Its behaviour is spread across the IA, State Patterns and Export: it holds the partial sentence, cycle overrun, new baseline, export result and filter count. There is no rule for which item wins when several apply on one line. (§ EXPERIENCE.md § Component Patterns (missing 'Status line'); DESIGN.md § Components 'Status line')
Fix: Add a Status line pattern with its content list, priority order when items compete, and the fold-into-footer rule from the shrink order.

**[Component coverage]** — `fixture-state-marks` (settledColor, frozenColor) is defined in the YAML but has no row in DESIGN.md § Components and no behaviour rule in EXPERIENCE.md. The fixture FROZEN marker 'no other state overrides' (rendering-rules.md:63) is not specified anywhere in the spines. (§ DESIGN.md frontmatter components.fixture-state-marks; § Components; EXPERIENCE.md § Component Patterns)
Fix: Add a Components row and a behaviour line: fixture-only, the FROZEN marker overrides other states, and live mode shows `unavailable (no source)`.

**[State coverage]** (blocking) — This is a contradiction about which rows are never dropped. 'Rows that never drop' lists header, freshness, COUNTS, the gap notice and the footer, and the gap-notice pattern says it shows 'in every view and at every width'. DESIGN's diagnostic shows 'the rows that are never dropped'. Shrink-order step 4 says the too-small diagnostic 'keeps the header, freshness, COUNTS and footer lines', which leaves out the gap notice. (§ EXPERIENCE.md § Responsive & Platform > PROPOSED shrink order step 4)
Fix: Add the gap notice to step 4, or say 'keeps every never-dropped row'.

**[State coverage]** (blocking) — T20 / prd.md:148 require two sessions that share a `worktreeId` to show as two rows, 'each naming it', and a session with no worktree to show `worktree unknown`. The ledger columns at every width (rendering-rules.md:29, mirrored in the Width bands table) contain no worktree field. The spine repeats 'A missing worktree reads `worktree unknown`' without saying where. As written, the ledger cannot satisfy T20. (§ EXPERIENCE.md § Component Patterns > Ledger; § Responsive & Platform > Width bands)
Fix: Say where the worktree is named (for example, in the inspector only, with T20 checked there), or raise the column-list versus T20 tension as a new UX-OQ.

**[State coverage]** — The discovery probe has no state. The probe is a one-time `skills list --json` check that validates the binary before the first cycle (prd.md glossary, NFR-9). The spine covers 'binary missing' but not 'binary found, probe failed', for example the wrong `orca` (github.com/orca-cli/orca). (§ EXPERIENCE.md § State Patterns > View-level states (R1))
Fix: Add a probe-failed row with the freshness-cell wording, or mark the wording PROPOSED.

**[State coverage]** — Three states are underspecified. (1) In the UJ-3 failure path the inspector 'keeps its last values' after the worker leaves the source window, with no notice on the inspector, so it shows values that are no longer current without saying so. (2) The inspector says nothing about STALE or FAILED source state or `as of`. (3) `--once` has no failure state (poll failure or write failure with no status line, exit code). (§ EXPERIENCE.md § Key Flows > UJ-3 failure path; UJ-4 failure path; § Component Patterns > Inspector)
Fix: Add an inspector notice line, for example `no longer in source window, values as of HH:MM:SS` (PROPOSED). Specify the `--once` failure output and exit code, or mark it PROPOSED.

**[State coverage]** — Fixture gallery (screen 0) is the first deliverable, but its interaction is unspecified. Its keys are not in the keyboard table, and it is not said how the reviewer steps through A/B/C x 160/116/80 x variants (27-case matrix, FR-1), or whether the gallery is an interactive screen or a set of byte-identical text renders (T6). (§ EXPERIENCE.md § Information Architecture row 0; § Interaction Primitives > Keyboard model)
Fix: Add a gallery column or a short section: how a frame is chosen (keys or files), and the frame label.

**[Visual reference coverage]** — No visual reference is in the workspace: imports/ is empty, and there are no mockups or wireframes. The design-package exports are listed only once, in Inspiration. They are not linked inline at the sections they illustrate (Screen 1 composition, Width bands, B geometry, Shapes). (§ EXPERIENCE.md § Inspiration & Anti-patterns; § Information Architecture; § Responsive & Platform; DESIGN.md § Shapes)
Fix: Link each relevant export inline, for example `exports/160/signal-bridge.txt` at the Screen 1 composition and the width bands, and name what each one illustrates. Optionally copy the text exports into imports/.

**[Visual reference coverage]** — No general 'spines win on conflict' statement exists. Precedence is stated only case by case (`>` over the prototype's ellipsis, and the prototype as reference only). (§ EXPERIENCE.md § Foundation or § Inspiration & Anti-patterns)
Fix: Add one sentence: where a design-package export disagrees with these spines, the spines win.

**[Inheritance discipline]** (blocking) — The R0 fixture label required by T50 / FR-1 is missing. The sources require every R0 render to carry 'synthetic fixture, not live evidence' (prd.md:85, 126; rendering-rules.md:5; acceptance-tests.md:44; release-gates.md:9). The spine uses only the header form `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17), says 'Every frame carries' it, and never uses the T50 string. (§ EXPERIENCE.md § Information Architecture row 0; § State Patterns > View-level states 'Fixture'; § Key Flows > R0 owner review step 2)
Fix: Require both strings on R0 renders: the T50 label 'synthetic fixture, not live evidence' and the header badge. Or state where each one appears.

**[Inheritance discipline]** — The sources say 'the strip shows `cycle overran (Ns)`' (prd.md:275, adapter-contract.md:26, acceptance-tests.md:34). The spine places it on the status line without a PROPOSED label. (§ EXPERIENCE.md § State Patterns > View-level states 'Cycle overrun')
Fix: Put it in the freshness strip as the sources say, or label the status-line placement PROPOSED.

**[Adversarial verification 3 of 3 (fresh context)]** (blocking) — EXPERIENCE.md:54 says 'The spec and PRD never mention the PLAN.md cockpit or the built layout.' That is false. rendering-rules.md:8 says the prototype's '116-column collapse claim does not match the built prototype' (X-001). rendering-rules.md:85 discusses the built Signal Bridge (`_request` in `signal_bridge`; 'its 116- and 80-column builds drop SIGNALS'). (§ EXPERIENCE.md:54)
Fix: Replace the sentence. State that the spec treats the prototype as a visual reference only and records that the built layout departs from it (rendering-rules.md:8, :85). Keep UX-OQ-1 for whether R1 may differ from the cockpit.

**[Adversarial verification 3 of 3 (fresh context)]** (blocking) — EXPERIENCE.md:292 puts `cycle overran (Ns)` 'on the status line'. Three sources put it on the strip: adapter-contract.md:26 ('the strip shows `cycle overran (Ns)`'), prd.md:275 (NFR-7) and T40 (acceptance-tests.md:34). This is wrong behaviour against a pinned acceptance test, and the placement is not labelled PROPOSED. (§ EXPERIENCE.md:292)
Fix: Render `cycle overran (Ns)` in the freshness strip, as the sources require. Cite adapter-contract.md:26 and T40.

**[Adversarial verification 3 of 3 (fresh context)]** (blocking) — The state vocabulary and view states leave out strings that acceptance tests pin. The failed row (EXPERIENCE.md:280) covers only `FAILED (<exit code or timeout>)`, but T32 (acceptance-tests.md:21) requires `FAILED (shape)` with the last good snapshot kept, and `reported unknown` when `page.total` is absent. Neither file has the T22 row flags `order unknown` and `conflict (time went back)` (acceptance-tests.md:18). The partial row omits `reported T (page k)` (rendering-rules.md:55). The scope header (EXPERIENCE.md:80) omits `one Run only` for `bound` scope (adapter-contract.md:63; risk K4, prd.md:363). The spec requires all of these. (§ EXPERIENCE.md:280)
Fix: Add `FAILED (shape)` (keep the last good snapshot) and `reported unknown` (absent `page.total`) to the failed and partial rows, citing T32. Add `order unknown` and `conflict (time went back)` as row-level flags, citing T22. Add `reported T (page k)`, citing rendering-rules.md:55. Add `one Run only` after `scope=bound` in header line 1, citing adapter-contract.md:63.

**[Adversarial verification 3 of 3 (fresh context)]** (blocking) — EXPERIENCE.md:135-140 heads its list 'Rows that never drop (spec)' and includes header line 1, the freshness strip, the gap notice and the footer. The spec fixes only the COUNTS strip as never dropped (rendering-rules.md:19) and coverage, scope and PARTIAL as minimum content (rendering-rules.md:13, T49). The other rows in the list are design choices presented as spec fact without a citation. (§ EXPERIENCE.md:135)
Fix: Label the list PROPOSED, except the COUNTS strip and coverage/scope/PARTIAL; cite rendering-rules.md:13 and :19 for those.

**[Adversarial verification (fresh context)]** (blocking) — False claim presented as fact: 'no design source states 44'. The design package PLAN.md:57 says 'Wide target around 44-52 rows; compact target around 36-44'. The cited DESIGN-CONTRACT.md:8 and concepts.md:36 do give the 48/42 export heights, but the claim that no design source mentions 44 is wrong, and UX-OQ-2 (EXPERIENCE.md:523) is built on it. (§ EXPERIENCE.md:133 (source: IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106/PLAN.md:57))
Fix: Replace it with: 'The exports are 48 rows (160) and 42 rows (116/80) (DESIGN-CONTRACT.md:8, concepts.md:36). PLAN.md:57 gives targets of 44-52 rows (wide) and 36-44 (compact), and no source defines the 44-row contract's contents (OQ-14).' Update UX-OQ-2 to match.

**[Adversarial verification (fresh context)]** (blocking) — Wrong behaviour versus the acceptance tests. The UJ-1 failure path says that if page.hasMore is still true at the call cap, 'PARTIAL: collected 100 of reported 412' appears. The cap is 5 subprocesses per cycle at 100 rows per page (adapter-contract.md:3, :25), so the cap is reached at 500 collected rows, and T4 pins 'PARTIAL: collected 500 of reported T' (acceptance-tests.md:12; prd.md:175). Under the cap, 412 reported rows are read in full within 5 pages, so the example cannot occur, and an implementer could copy it into a fixture. (§ EXPERIENCE.md:441 (sources: acceptance-tests.md:12, prd.md:175, adapter-contract.md:25))
Fix: Use 'PARTIAL: collected 500 of reported 1240 (newest first; oldest rows not read; long-running active workers may be among them)', or any reported T above 500.

**[Adversarial verification (fresh context)]** (blocking) — Uncited rule that contradicts the document's own export rule. UJ-4 says the plain-text export writes missing values as the string 'UNKNOWN'. The UNKNOWN-string rule belongs to the JSON snapshot (snapshot-export-schema.md:10; prd.md:237). The text export is 'exactly the view on screen' (prd.md:46, prd.md:68), the screen shows the literal 'unknown' (rendering-rules.md:51), and EXPERIENCE.md:267 itself says the export has the same content as the screen. No source gives the text export an uppercase sentinel. (§ EXPERIENCE.md:469 (vs EXPERIENCE.md:267; sources: snapshot-export-schema.md:10, prd.md:46, rendering-rules.md:51))
Fix: Say that the text export writes missing values exactly as the screen does ('unknown', or 'unknown (absent in source)' for inspector fields), and keep 'UNKNOWN' only for the JSON snapshot.

**[Adversarial verification (fresh context)]** — A source contradiction is resolved without being flagged. rendering-rules.md:17 says the fixture header reads 'SYNTHETIC FIXTURE <variant>, not Orca data', while T50 and the PRD (acceptance-tests.md:44; prd.md:85, :126) say 'synthetic fixture, not live evidence'. The UX builds a hybrid, 'synthetic fixture, not live evidence (<variant>)', and calls it 'the T50 label, verbatim', without recording that the spec's own header string differs. It satisfies T50, but it silently overrides the spec header string. (§ EXPERIENCE.md:215 (also :64, :296, :490))
Fix: Add a UX-OQ (or cite it as a CONTRADICTION) naming both strings, and keep the T50 substring as the minimum.

**[Adversarial verification (fresh context)]** — The PROPOSED default for worktree naming fails T20 as written. T20 and FR-4 need a rendered screen in which two rows sharing a worktreeId each name it, and a row with no worktree shows 'worktree unknown' (acceptance-tests.md:17; prd.md:148). The UX puts the worktree only in the inspector and the export, yet EXPERIENCE.md:241 still says 'A missing worktree reads worktree unknown' in the ledger section, with no ledger cell to hold it. It is correctly raised as UX-OQ-8, so it is not blocking. (§ EXPERIENCE.md:241-242, EXPERIENCE.md:529)
Fix: State in UX-OQ-8 that the PROPOSED inspector-only option does not satisfy T20 as worded, and move the 'worktree unknown' sentence to the inspector and export rules.

**[Adversarial verification (fresh context)]** — The PROPOSED --ascii replacement of every non-ASCII source character with '?' breaks 'full IDs in the selected detail' and the copy-the-ID climax (UJ-3) for any CJK or emoji ID, and it is not limited to the screen. That is a loss in the inspector and possibly the export, which T24/T27 require to be full. (§ DESIGN.md:195)
Fix: Limit the '?' replacement to cut list cells on screen, and show non-ASCII characters in the inspector and export as an unambiguous escape (for example U+XXXX), or leave the export unaffected by --ascii.

**[Adversarial verification (fresh context)]** — The 80-115 column restatement of B omits the spec's invariant lines 'Questions stay until explicit resolution.' and 'No reply observed is not delivery failure.', which rendering-rules.md:42 says stay. The B shrink order (EXPERIENCE.md:165-168) also does not protect them. (§ EXPERIENCE.md:177)
Fix: Add the two invariant lines to the 80-115 row, and list them among B's never-dropped lines.


### Low (22)
**[Flow coverage]** — The R2/R3 labels that FR-17/FR-18 require are missing from the B/C flow and screens: 'bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions' (rendering-rules.md:37) and 'affected scope unknown' (FR-18). (§ EXPERIENCE.md § Key Flows > UJ-5; § Information Architecture rows 5 and 7)
Fix: Add the two labels to the UJ-5 steps and failure path. They are later-release requirements, so a one-line mention is enough.

**[Token completeness]** — No light/dark pair is given. The observer draws on the terminal's background, and the spine labels the light-theme contrast risk PROPOSED. Contrast for `{colors.line}` (#526c80, borders) is not stated; it computes to about 3.2:1 on #101820, which is enough for non-text. The selected row's reverse-video contrast, and how the accent cursor looks inside reverse video, are not stated. (§ DESIGN.md § Colors (contrast table); components.ledger-row-selected)
Fix: Add a `line` row to the contrast table (non-text 3:1 target). Say whether the accent cursor glyph is drawn inside or outside the reverse-video span.

**[Component coverage]** — The names drift between the files. EXPERIENCE calls the gutter component 'Row gutter', while DESIGN uses 'Selected row' and 'Change mark'. EXPERIENCE has an 'Export' pattern with no DESIGN row. The filter prompt in the footer has no visual spec. The B/C components (OPEN HUMAN QUESTIONS panel, SEEN IS NOT RESOLVED, RETAIN CONTEXT, question inspector, Decision Desk) have no rows, even though R0 renders B and C. (§ DESIGN.md § Components; EXPERIENCE.md § Component Patterns)
Fix: Use one component name in both files. Add one line saying that B/C component specs are deferred and that R0 renders them from the design-package exports.

**[Bloat & overspecification]** — The contrast ratios appear twice, in the DESIGN.md Colors table and again in EXPERIENCE.md Accessibility Floor (7.63-14.56:1), which is a drift risk. 'Which Signal Bridge is R1' is a decision rationale that duplicates UX-OQ-1. (§ EXPERIENCE.md § Accessibility Floor > Contrast; § Foundation > Which Signal Bridge is R1)
Fix: In Accessibility Floor, refer to DESIGN.md § Colors instead of restating the numbers. Shorten the Signal Bridge table to its mapping column.

**[Inheritance discipline]** — The last `sources` entry (`IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106/`) does not resolve from the repo root. The package is at /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/... in another repository. Two UJ names are not verbatim: 'UJ-4 Export (R1)' should be 'Export (R1, any platform)', and 'UJ-5 Find the oldest question (B, then C; gated)' should be '(R2/R3, gated)'. (§ EXPERIENCE.md frontmatter sources; § Key Flows headings UJ-4, UJ-5)
Fix: Anchor the cross-repo path (repo name plus commit, or an absolute workspace path) and use the PRD journey names verbatim.

**[Shape fit]** — Responsive & Platform comes directly after IA, where the example places it after Accessibility Floor. The order is defensible because the width bands are the main layout input, but it differs from the examples. (§ EXPERIENCE.md § Responsive & Platform)
Fix: Optional: move it after Accessibility Floor, or leave it as is. Not load-bearing.

**[Adversarial verification 3 of 3 (fresh context)]** — The worker inspector does not show `n unrecognised keys` (adapter-contract.md:38). It also does not show the per-process cap disclosure ('caps are per observer process, and help and the inspector say so', adapter-contract.md:62). (§ EXPERIENCE.md:249)
Fix: Add both lines to the inspector anatomy and cite adapter-contract.md:38 and :62.

**[Adversarial verification 3 of 3 (fresh context)]** — B's 80-column description leaves out its invariant lines, 'Questions stay until explicit resolution.' and 'No reply observed is not delivery failure.' (rendering-rules.md:42). The R0 degraded variants also leave out 'affected scope unknown' (release-gates.md:9) and `reason unknown` (prd.md:260). (§ EXPERIENCE.md:177)
Fix: Add the invariant lines to B at 80 columns, and the two degraded strings to the R0 fixture variants.

**[Adversarial verification 3 of 3 (fresh context)]** — DESIGN.md:193 justifies the `@` ASCII cursor by citing EXPERIENCE.md UX-OQ-5, but that open question is about something else, so the citation does not support the claim. (§ DESIGN.md:193)
Fix: Cite rendering-rules.md:24 (the `>` truncation marker) for the reason, and use the correct UX-OQ ID, or add a new one for the cursor glyph.

**[Adversarial verification 3 of 3 (fresh context)]** — The two files word the NO_COLOR rule differently. DESIGN.md:140 says 'set to a non-empty value', and EXPERIENCE.md's Accessibility Floor phrases it another way. T26 (acceptance-tests.md:19) pins `NO_COLOR=1` and `NO_COLOR=yes`. (§ DESIGN.md:140)
Fix: Use one wording in both files and cite T26.

**[Adversarial verification 3 of 3 (fresh context)]** — The PROPOSED loading state shows COUNTS `collected 0 / reported unknown` before any poll. No poll has run yet, so `collected 0` can read as an observation. (§ EXPERIENCE.md:286)
Fix: Show `collected unknown (not yet polled)`, or explain why 0 is accurate before the first poll.

**[Adversarial verification 3 of 3 (fresh context)]** — The historical-rows behaviour leaves out the rule that 'historical evidence explicitly linked to a shown item is never hidden' (rendering-rules.md:22). (§ EXPERIENCE.md:239)
Fix: Add the rule and cite rendering-rules.md:22.

**[Adversarial verification 3 of 3 (fresh context)]** — The keyboard table gives `m` and `e` in the inspector as 'same as ledger'. The spec defines the keys only globally (rendering-rules.md:20) and does not say they work inside the inspector, but these entries are not marked PROPOSED. (§ EXPERIENCE.md:316)
Fix: Mark the inspector entries for `m` and `e` PROPOSED.

**[Adversarial verification 3 of 3 (fresh context)]** — 'OQ-B/C' is not an ID in prd.md's open-question list (prd.md:414-453). (§ EXPERIENCE.md:71)
Fix: Replace it with the real OQ or OI number for the post-link default, or with UX-OQ-n.

**[Adversarial verification (fresh context)]** — The state vocabulary's 'exact rendering' for failed lists only 'FAILED (<exit code or timeout>)'. T32 pins 'FAILED (shape)' (acceptance-tests.md:21), and adapter-contract.md:50 counts invalid JSON as a failure. The row-level states 'order unknown' and 'conflict (time went back)' (T22) and the inspector's 'n unrecognised keys' (adapter-contract.md:38) are also missing. (§ EXPERIENCE.md:280)
Fix: Add FAILED (shape), the T22 row flags and the unrecognised-keys line to the vocabulary and the inspector field list.

**[Adversarial verification (fresh context)]** — The PROPOSED loading state shows 'collected 0 / reported unknown' before any poll. It is honest because of the unknown denominator, but it is the one place a not-observed state renders as 0, against the stance at EXPERIENCE.md:33. (§ EXPERIENCE.md:286)
Fix: Use 'collected none yet / reported unknown (not yet polled)', or keep it and say explicitly why it does not breach NFR-11.

**[Adversarial verification (fresh context)]** — The full PARTIAL sentence is said never to be cut (EXPERIENCE.md:441), but it sits on a one-row status line that folds into the footer when height falls (EXPERIENCE.md:161). At 80 columns the sentence (about 110 cells) cannot fit on one row. Only the PARTIAL token is spec-protected (rendering-rules.md:19). (§ EXPERIENCE.md:288, EXPERIENCE.md:441)
Fix: Say that the PARTIAL token in COUNTS is never cut and that the full sentence wraps, or is complete in the inspector or export.

**[Adversarial verification (fresh context)]** — The footer anatomy has 'a light rule, then the key list' (two rows), but the 44-row budget gives the footer one row (row 44), after the ledger frame bottom at row 43. (§ DESIGN.md:211 vs EXPERIENCE.md:156-157)
Fix: State that the ledger frame bottom doubles as the footer rule, or add a row to the budget.

**[Adversarial verification (fresh context)]** — The freshness-strip colours do not cover the 'NOT AVAILABLE (orca binary not found)' state, which EXPERIENCE.md:184 and :291 use. (§ DESIGN.md:202 (and DESIGN.md:46-52))
Fix: Give NOT AVAILABLE a token (warn or bad), alongside its word.

**[Adversarial verification (fresh context)]** — There is no help key, yet the voice table and the spec need help text ('a completed Task can still own a live terminal', rendering-rules.md:52; the per-process caps note in help, adapter-contract.md:62). The UX never says where help text is shown. (§ EXPERIENCE.md:202, EXPERIENCE.md:322)
Fix: Name the surface that carries help text (for example the inspector or the --help output), or record it as an open question.

**[Adversarial verification (fresh context)]** — The keyboard table is headed 'spec, rendering-rules.md:20', but it includes entries the spec does not list (Ctrl-C, Backspace, and the inspector's m/e/q behaviour) without a PROPOSED label. (§ EXPERIENCE.md:307-320)
Fix: Mark the non-spec rows PROPOSED.

**[Adversarial verification (fresh context)]** — Citation drift: FR-16 is cited as prd.md:86, which is the glossary row; FR-16 is at prd.md:235. The statement that '--once ... writes one snapshot' is an inference with no source. (§ EXPERIENCE.md:68, EXPERIENCE.md:469)
Fix: Cite prd.md:235, and mark the --once snapshot behaviour PROPOSED.


## Reviewer files
- `review-rubric.md`
- `review-adversarial-3.json`
- `review-adversarial.json`
