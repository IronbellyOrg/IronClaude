# Design package QA

## Scope
Offline visual artifacts only. No live operational integration, performance benchmark or measured user-comprehension test. Review structure follows the approved plan's verification section.

## Automated checks
13 shared fixture and safe-text tests passed before layout integration. Tested scale totals, shared/unmapped worktrees, history separation, partial spend, revision/admission separation, event deduplication, filtering denominators, empty state, injection sanitization, display width, ASCII, no-color and HTML escaping.

Final package suite: 19 tests passed, no skips (including declared cross-owner relationship consistency and source timestamp/age reconciliation), covering 20 designs across 18 scale/scenario cases and four widths (160/144/116/80), with deterministic repeated renders and ASCII checks. The 144 size is tested but is not a primary export. Main export sizes are 160/116/80.

Both sets generated: 20 named concepts, 60 primary colored PNGs plus 60 monochrome PNGs, matching SVG/ANSI/plain/ASCII exports. Export manifests and ANSI-to-plain equivalence passed. Each PDF was parsed independently and contains 10 pages. Offline-gallery JavaScript syntax and DOM-contract simulations passed for ten concepts per set, concept navigation, width/ASCII switching, inspector filtering versus global totals, hold/queue/resume and empty-state disclosure. This is not a real-browser or physical-keyboard test.

Text/semantic accents were checked against the dark background: ink 14.56:1, muted 8.58:1, accent 9.82:1, warning 9.75:1, failed-result 7.63:1, positive observation 10.60:1, frozen 8.99:1. Labels retain meaning without color. Timeline phases use one accent and explicit letters rather than imply review is success or dependency is policy freeze.

## Render inspection
Parent inspected both actual contact sheets and the native 116-column Fleet Quilt PNG. A real clipping defect hid the per-session state behind an ellipsis; minimum cell width was increased and a regression assertion now requires every base session ID followed by its visible state at 160 and 116 columns. First-generation quilt omitted cells/owners and repeated timeline letters were corrected before regeneration. Zero-cost-sample owner rows now say unknown rather than USD 0.00. Actual independent image inspection is recorded below when returned. Contact-sheet inspection alone does not establish readability.

## Independent review
**Verdict: FAIL for the inspected pre-correction snapshots.** The reviewer read all 20 native 160-column color images, both contact sheets and 11 native compact/narrow examples. This is actual image review, not only a brief review. No report file was written by the reviewer; the findings were delivered directly and recorded here.

Blocking findings and the one targeted correction pass:
1. Delta Deck/Watchkeeper reused ledger-style arrangements rather than the promised change lanes and handover summary. Delta Deck now has persistent unresolved context and four event lanes (four columns wide, two-by-two compact, stacked narrow). Watchkeeper now has a large question count and separate handover/source regions.
2. Missing report outcomes were displayed as pending, including unknown-lifecycle sessions. The shared ledger now says not observed unless a result exists.
3. Worktree Atlas lacked explicit branch/base geometry and selected-path peers. It now draws base-to-branch attachments, prioritizes peer worktrees and lists shared-path evidence without a conflict claim.
4. Compact Revision Drift summary overwrote the navigation footer. Its summary now uses a height-relative row; a regression assertion verifies the footer on every layout/scenario/width.

Additional fixes: Fleet Quilt state markers are no longer clipped (all 80 base IDs plus markers required at 160/116); missing test outcomes say unknown; list omission counters now explicitly count text lines. Previously refreshed Budget Engine actual CPU/RSS sample quantities and Quilt missing-owner defects were independently considered closed by the reviewer.

**Final boundary:** all four blocking corrections are in source and regenerated exports, and the 19 automated tests plus both gallery DOM simulations pass. The parent directly read the final wide Delta Deck, Watchkeeper and Worktree Atlas PNGs plus the native 116-column Revision Drift PNG and confirmed the new arrangements and intact navigation footer. No new independent post-correction verdict was requested. Do not describe this as an independent PASS, measured aesthetics success or user approval. No additional review/debate pipeline was started.

## Known limitations
- Source-to-dashboard schema is proposed; fixture fields are not asserted Orca API fields.
- Complete non-consuming message enumeration, remote coverage, usage accounting and admission joins are not verified end-to-end.
- Source and installed worker-contract rollout differ; no automatic interpretation of lifecycle completion as acceptance.
- Five-second readability remains a design goal.
- Real-browser validation was attempted through Playwright; it failed because Chrome was absent at /opt/google/chrome/chrome. No browser was installed. Keyboard/state logic was exercised in the explicit DOM simulation only; actual browser rendering and physical-keyboard use remain unverified.
- Python/Pillow rendering is a prototype tool, not a claim of Bubble Tea runtime behavior. The supplied TUIBBS-scp dependency pins were verified, but its AGPL components were not extracted.
- Previous packs and all unrelated user changes are preserved. Only the isolated .dev/design/orca-observer-20261106 package is authored here.

## Reproduction
Observed commands (run from IronClaude root):

```sh
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/render.py
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/render.py --batch 2
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/tests/test_designs.py
node .dev/design/orca-observer-20261106/tests/test_gallery.cjs
node .dev/design/orca-observer-20261106/tests/test_gallery.cjs .dev/design/orca-observer-20261106/agent-focus/gallery.html
```

Rendering dependency pins: Pillow 13.0.0 and wcwidth 0.9.4. Exact fixture SHA-256 is recorded in each generated manifest. Dependency resolution used UV's isolated environment; no production manifest or system package was changed. PDF page validation used temporary pypdf through UV.
