# T4 render check: docs/onboarding/ironclaude-onboarding.html

- Date: 2026-10-26. Deck sha256 at the final check: see `./t4-deck-sha.txt`.
- Method: the deck has no doctype, so `./render/index.html` wraps the deck file's text in a minimal `<!doctype html>` skeleton (charset + viewport meta), regenerated from the current deck before every run. It was served from inside `./render` with `uv run --no-project python -m http.server 60887 --bind 127.0.0.1` (background; stopped at the end of the task).
- Browser: the Playwright MCP browser tool failed to start ("Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome"). The same Playwright engine was used through a throwaway script (`playwright@1.64.1` installed in `/tmp/onb-render`, outside the repo) with the already-downloaded Chromium build v1248 (Chrome for Testing 156). Scripts are copied to `./render/render.mjs` and `./render/overflow.mjs`. Raw results: `./t4-render-result.json`, `./t4-render-summary.json`, `./t4-overflow.json`.

## Results (final run)

| Check | Evidence | Result |
|---|---|---|
| 1280 px: 15 slides, 6 diagrams render | t4-render-summary.json runs[0..1]: slides 15, svgs 6 | pass |
| Keyboard and button navigation | End -> "15 / 15", Home -> "1 / 15", 14 x ArrowRight -> "2 / 15" ... "15 / 15", Next button steps, manual scroll to top -> "1 / 15" (all four configurations); proves the navigation script runs in the regenerated wrapper | pass |
| Console errors | `errors: []` in all four configurations | pass |
| 375 px: no horizontal page scroll | scrollWidth 375 = innerWidth 375 (light and dark) | pass |
| Diagrams at 375 px | each SVG keeps a minimum width (640 px; D5 980 px) and scrolls inside its own `overflow-x: auto` box; screenshots `t4-375-light-s5.png`, `t4-375-dark-s5.png`, `t4-375-light-s10.png`, `t4-375-dark-s10.png` show legible labels | pass |
| Legibility, light and dark, 1280 and 375 | body paragraph font 17 px (1280) and 16 px (375), lead 18.4 px (>= 14 px); lowest token contrast 5.39:1 light and 5.67:1 dark over 12 pairs (body text, muted, accent, warn, and the diagram stroke token `--line` against their backgrounds; full table in t4-render-result.json) (>= 4.5:1) | pass |
| Diagram labels fit their boxes | `t4-overflow.json`: `[]` (every SVG `<text>` checked against its enclosing box and the viewBox at 1280 px) | pass |
| Inline code never splits mid-token | `split: []` in all four configurations (no short `<code>` or protected span renders on two lines) | pass |
| Print: one slide per page | `t4-print-light.pdf` and `t4-print-dark.pdf`: 15 pages each (A4, 14 mm margins) for 15 forced page breaks, so every slide, including the cheat sheet with the footer, sits on exactly one page; `t4-print-dark-s15.png` shows the cheat sheet page | pass |
| Print colors from a dark system theme | print-media tokens resolve to `--fg #000000`, `--muted #3a4651` in both schemes | pass |
| Network | only the page, fonts.googleapis.com and fonts.gstatic.com | pass |
| File size | 49,470 bytes (well under 16 MB) | pass |
| Claim test after fixes | `t4-tests.log`: 3 passed | pass |

Screenshots: `t4-1280-light.png`, `t4-1280-dark.png`, `t4-375-light.png`, `t4-375-dark.png` (full page), per-diagram `t4-1280-light-s{2,4,5,6,7,10}-svg.png`, print media `t4-print-media-light.png`, `t4-print-media-dark.png`.

## Defects found and fixed in the deck

| # | Defect | Fix |
|---|---|---|
| 1 | Diagram stroke token `--line` contrast 2.46:1 (light) and 3.13:1 (dark), below 4.5:1 | `--line` set to #5f6b77 (light, 5.45:1) and #8796a5 (dark, 5.67:1); print value #5f6b77 |
| 2 | Diagram text too small when scaled on phones | minimum diagram widths raised (640 px; D5 980 px), scrolling inside their own boxes |
| 3 | Slide counter drifted on jumps (End showed "13 / 15", Home "2 / 15") because a scroll observer overwrote the target mid-animation | counter now computed from slide positions on scroll, a jump keeps its target until its scroll ends, and the page bottom maps to the last slide |
| 4 | Inline code split mid-flag on phones ("--" / "monitor 3") | short `<code>` is `white-space: nowrap`; the three long snippets wrap only at spaces with each word protected |
| 5 | D5 command labels overflowed their boxes; D1 right caption clipped | D5 relaid out with wider boxes (154 px) and a smaller mono size; D1 caption shortened |
| 6 | D2 file and agent names overflowed their boxes | D2 boxes resized, call-arrow targets moved so arrows clear the agents box |
| 7 | D6 loop label ran into the "Pushes the fixes" box | label moved left of the return arrow |
| (measurement) | First run measured the eyebrow label (12.8 px) as body text | script now measures the lead and a body paragraph |
