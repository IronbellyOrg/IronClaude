# T4 spec-compliance QA: render check at phone and desktop width in both themes

Reviewer: independent per-task spec-compliance reviewer (rubric `~/.claude/skills/sc-implement-protocol/refs/qa.md`). Do not trust the implementer's report: every claim below was re-checked against the artifacts, the deck diff and fresh commands.

Brief: plan `TASK-WF-implementFrOnb2T-20261023-192153.md:91-103` (Task 4 body and AC), `## Constraints` at :17-33; spec `.dev/releases/backlog/ironclaude-onboarding-deck/spec.md:325-331` (NFR-ONB.1 to .4, .7) and :360-367 (section 7.3).
Start snapshot: `d81a5a3cf777e47ce3828ab8626d967d0e3fb183`. Deck diff taken with `git cat-file -p d81a5a3:docs/onboarding/ironclaude-onboarding.html` to `/tmp` and `git diff --no-index` (90 insertions, 72 deletions, one file). Nothing staged.

Paths below: `PKG` = `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153`, `DECK` = `docs/onboarding/ironclaude-onboarding.html` (both relative to the worktree root).

## Independent checks run by this reviewer

| Check | Result |
|---|---|
| `sha256sum DECK` vs `PKG/artifacts/t4-deck-sha.txt:1` | both `c2c03156...07474a4`: match, so the final run used the final deck |
| `PKG/artifacts/render/index.html` contains the current DECK text verbatim | yes; only a 176-byte doctype/charset/viewport skeleton around it |
| Timestamps | DECK 17:01:09, wrapper and sha 17:01:26, render-result 17:02:36, overflow 17:02:37, tests log 17:02:38: all checks after the last deck edit |
| PDF page count, counted by this reviewer (`/Type /Page[^s]` regex over bytes) | `t4-print-light.pdf` 15, `t4-print-dark.pdf` 15 (root `/Count 15`) |
| Contrast recomputed from tokens in `t4-render-result.json` | `--fg`/`--bg` 15.92 light, 15.54 dark; `--line`/`--bg` 4.80 light, 6.22 dark; `--line`/`--surface` 5.45, 5.67 (all >= 4.5) |
| Server stopped | no listener on port 60887, no `http.server` process |
| `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/docs/test_onboarding_deck.py -q -p no:cacheprovider` | 3 passed |
| `tests/docs/test_onboarding_deck.py` vs snapshot | unchanged |
| Screenshots viewed | `t4-375-dark-s10.png` (D6 at 375 px dark: legible, SVG scrolls inside its box, page not widened), `t4-1280-light-s4-svg.png` (D2: labels inside boxes), `t4-1280-light-s5-svg.png` (D3: hard limit between 2 and 3), `t4-1280-light-s7-svg.png` (D5: labels fit), `t4-print-dark-s15.png` (cheat sheet on one page), `t4-print-media-dark.png` (print media from a dark scheme renders light tokens, all 15 slides) |

## Acceptance criteria

- **T4.AC1 met.** Findings log records every check of plan :95 as pass with evidence: 15 slides / 6 diagrams `PKG/artifacts/t4-render-check.md:11`, keyboard `:12`, console `:13`, 375 px scroll `:14`, diagrams at 375 `:15`, per-theme legibility at 1280 and 375 with font sizes (17/16 px body, 18.4 px lead) and contrast (min 5.39 light, 5.67 dark) `:16`, print `:19-20`, network `:21`, size `:22`, test `:23`; defects and fixes `:27-38`. Raw values: `PKG/artifacts/t4-render-summary.json:24-163` (per run width/scheme, `font`, `para`, `minContrast`). Note: the log's stroke-token ratio is `--line` on `--surface`, not literally on `--bg`; this reviewer's recomputation of `--line` on `--bg` (4.80 light, 6.22 dark) also passes, so the AC's measured threshold holds.
- **T4.AC2 met.** Full-page screenshots `PKG/artifacts/t4-1280-light.png`, `t4-1280-dark.png`, `t4-375-light.png`, `t4-375-dark.png` exist (listed at `PKG/artifacts/t4-render-check.md:25`, produced by `PKG/artifacts/render/render.mjs:66-67`). PDFs exist; recorded page count 15 at `PKG/artifacts/t4-render-summary.json:2-3` and `PKG/artifacts/t4-render-check.md:19`, independently confirmed as 15 each. One slide per page follows from 15 forced breaks (`DECK:155-156`) giving exactly 15 pages, so the cheat sheet (slide 15) sits on one page; confirmed visually in `t4-print-dark-s15.png`.
- **T4.AC3 met.** 375 px: `sw` 375 = `iw` 375 in light and dark (`PKG/artifacts/t4-render-summary.json:99-100`, `:134-135`). Console errors: `"errors": []` (`PKG/artifacts/t4-render-summary.json:22`; collected by `render.mjs:27-28` from console and pageerror in all four configurations). Network: only `127.0.0.1:60887/index.html`, `fonts.googleapis.com`, `fonts.gstatic.com` (`PKG/artifacts/t4-render-summary.json:14-21`; collected by `render.mjs:29`).
- **T4.AC4 met.** Wrapper regenerated from the final deck: `PKG/artifacts/render/index.html` contains the exact DECK text, DECK sha256 matches `PKG/artifacts/t4-deck-sha.txt:1`, and every result file post-dates the last deck edit. Navigation script ran: End -> "15 / 15", Home -> "1 / 15", 14 ArrowRight steps "2 / 15" .. "15 / 15", Next button, manual top -> "1 / 15" in all four configurations (`PKG/artifacts/t4-render-summary.json:35-57`; driver `render.mjs:50-64`).
- **T4.AC5 met.** 49,470 bytes recorded (`PKG/artifacts/t4-render-check.md:22`, `t4-render-result.json` `file_bytes`), equal to `wc -c DECK`; spec target `spec.md:331`.
- **T4.AC6 met.** `PKG/artifacts/t4-tests.log:1` "3 passed"; re-run by this reviewer on the final deck: 3 passed.

## Diff audit (each deck change mapped to a logged defect)

| Deck change (current lines) | Logged defect |
|---|---|
| `--line` light/dark/print tokens `DECK:19`, `:32`, `:38`, `:149` | #1 stroke contrast (`t4-render-check.md:31`) |
| `.diagram.wide/.mid` min-width 980/640 `DECK:115-116` | #2 diagram text too small on phones (`:32`) |
| Counter script: `lockUntil`, `fromScroll`, scroll/scrollend listeners replacing the IntersectionObserver `DECK:610-648` | #3 counter drift on jumps (`:33`) |
| `code` `white-space: nowrap`, `code.long`, `.nw` `DECK:53-57`; `class="long"` spans on the three long snippets `DECK:438`, `:449`, `:569` | #4 inline code split mid-flag (`:34`) |
| `.d-tm-s` `DECK:131`; D5 relayout, viewBox 1170 `DECK:394-423`; D1 caption shortened `DECK:228` and "Best parts / merged" nudged down 6 px | #5 D5 overflow, D1 caption clipped (`:35`) |
| D2 box sizes, arrow targets, label positions `DECK:284-305` | #6 D2 overflow (`:36`) |
| D6 loop label moved left, right-anchored `DECK:496-498` | #7 D6 label collision (`:37`) |

No change outside these seven defects. The D1 caption edit drops the clause "Cheaper than five runs;": a wording removal, not an added claim, made to fix the logged clipping, so it needs no new source. No other file in the touched set changed (the claim test is byte-identical to the snapshot; the routing surfaces in `git status` were already modified before T4 and are Part A work).

## Method deviation (Playwright MCP vs script)

The plan says "Use the Playwright browser tools" (plan :95). The MCP tool failed to start (`t4-render-check.md:5`); the implementer drove the same Playwright engine (Chromium) from `PKG/artifacts/render/render.mjs` and `overflow.mjs`, which are saved and readable. Every observable the AC asks for (viewport widths, `colorScheme` emulation `render.mjs:24`, keyboard presses `:50-60`, console capture `:27-28`, network capture `:29`, print media plus `page.pdf()` `:78-79`, screenshots) is produced by the same engine and recorded. The plan itself permits `page.pdf()` or headless Chromium print. This meets the AC's observable requirements; not a misunderstanding.

## Minor observations (not AC failures)

- `t4-print-dark-s15.png` (16:59) predates the final deck edit (17:01:09); the cheat-sheet-on-one-page claim still holds from the final 15-page PDFs (17:02).
- The 375 px element screenshots show the sticky topbar overlapping the slide top; that is a capture artifact of element screenshots under a sticky header, not a page defect.
- Light `--line` on `--surface-2` is 4.38:1 (below 4.5); the AC measures against the background token only, where it is 4.80, so this is outside the AC.

## extra_scope

none

## misunderstood

none

VERDICT: compliant
