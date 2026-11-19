# PNG route (spec step 0.4)

Result: FAIL. The text and ANSI tier is the gate for this work.

- Date: 2026-11-18.
- Attempt: `mcp__plugin_playwright_playwright__browser_navigate` to a `file://` URL of `ledger.16.html` (the harness capture at width 160, folder `iter-1/160/` of the Phase 1 gate output).
- Tool answer: `Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome. Run "npx playwright install chrome"`. No browser is installed in this workspace.
- Font: `DejaVu Sans Mono` is installed (`/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf`), but its coverage of the mockup glyphs stays untested because no page could be rendered. Viewport: none was set, since the browser never started.
- Decision: no dependency is added (owner decision D-10 default: no new PNG renderer). In the gate (spec section 8, step 3) the reviewer compares the `.txt` and `.ansi` files with the mockup text and ANSI exports, and uses the mockup PNGs as the visual reference. Installing a browser (`npx playwright install chrome`, or a tool such as `freeze`) needs a separate owner approval first.
