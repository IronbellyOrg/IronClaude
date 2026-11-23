# Web Research 02: Zellij and Terminal-to-Image Capture

Topic: (A) Zellij 0.44.x layouts, floating panes, dump-screen, theming, detection, colour; (B) offline terminal-output-to-image tools for an automated compare loop.
Date: 2026-11-17
Status: Complete

## What we already know (from codebase)

1. Zellij 0.44.2 installed at /usr/local/bin/zellij; minimal config; ANSI-16 theme (aidev02); layouts agent.kdl and default.kdl. Help lists floating panes, `dump-screen --ansi`, `--layout-string`; none exercised.
2. Offline render tools: Rich 15.0.0 (export_svg, export_html). PIL, cairosvg, pyte, playwright, fontTools, chromium, rsvg-convert, inkscape, ImageMagick all absent. node 24 present. pexpect 4.9.0 present. Playwright MCP browser exists only in the Claude session.
3. render_current.py writes per-width text/ANSI for three screens via emit(), but uses export_text(styles=True), which ignores NO_COLOR and 16-colour downgrade.
4. Mockup PNGs exist per width; a Claude agent can view PNGs with Read.
5. unzip not installed (Python zipfile used).

## Part A: Zellij findings

### A1. Layout files, floating panes, commands in layouts
- Source: https://zellij.dev/documentation/creating-a-layout.html (official docs, reliability: highest)
- A `floating_panes` node can sit at the layout root or inside a `tab`; its child `pane` nodes take `x`, `y`, `width`, `height` as fixed character counts or percentages (percentages recommended when terminal size is unknown). Example from the docs: `layout { floating_panes { pane command="ls"  pane { x 1 y "10%" width 200 height "50%" } } }`. Floating panes cannot have children or `split_direction`. `tab ... hide_floating_panes=true` starts them hidden.
- Source: https://zellij.dev/documentation/layouts.html : `zellij --layout /path/file.kdl`; default `default.kdl` in the config `layouts` dir; bare layout names resolve from that dir. KDL is the config language.
- Source: https://zellij.dev/documentation/swap-layouts.html : `swap_floating_layout` / `swap_tiled_layout` with `max_panes`, `min_panes`, `exact_panes` constraints.
- Command panes in layouts: `pane command="htop"` (layouts.html example) and `pane command="cargo" { args "test" }` (https://zellij.dev/documentation/layout-examples). Features page (https://zellij.dev/features) says command panes show exit code and can be re-run with Enter or started suspended (`start_suspended`).
- Relevance: MEDIUM. Matches our local layouts (agent.kdl, default.kdl) and `--layout` help text; nothing contradicts local findings. A floating observer pane is declarable in a layout, but the observer does not need it to work standalone.

### A2. dump-screen
- Sources: https://zellij.dev/documentation/cli-actions.html and https://zellij.dev/documentation/programmatic-control.html (official, highest)
- `zellij action dump-screen` dumps a pane viewport to STDOUT or `--path FILE`. Options: `-f/--full` (scrollback), `-p/--pane-id <id>` (e.g. terminal_3; default focused pane), `-a/--ansi` (preserve colour and styling; cursor movement is not kept because the output is already rendered into lines). Default output strips ANSI.
- Source: https://zellij.dev/documentation/cli-recipes.html : sessions can be driven headless: `zellij attach --create-background`, then `zellij --session NAME action dump-screen --pane-id terminal_1 --full`, `new-pane`, `paste`, `send-keys --pane-id ... "Enter"`, `list-panes --json`. Source https://zellij.dev/news/remote-sessions-windows-cli (0.44.0 release notes): `list-panes`, `send-keys`, `dump-screen` for any pane in any session were added in 0.44.
- Relevance: HIGH for Q6. Confirms the local help text. A Zellij-based capture test could run the observer in a background session and dump its pane with `--ansi`, with no PTY emulator library. NOT exercised locally. It yields ANSI text, not an image, so it still needs a text-to-image step (Part B). Zellij re-renders pane cells itself (and applies its theme to ANSI-16 colours), so a dump is not a byte-for-byte copy of what the observer printed; that is an inference from how a multiplexer works, not a statement found in the docs.

### A3. Tab bar, status bar, compact bar
- Sources: https://zellij.dev/documentation/layout-examples , https://zellij.dev/documentation/plugin-aliases.html (official, highest)
- A layout draws bars with `pane size=1 borderless=true { plugin location="zellij:tab-bar" }` (status-bar uses size=2; compact-bar is one line). `default_tab_template { children ... }` puts them on every tab. Docs state the three bars are now one built-in plugin `zellij:bars` with a `role` setting; the old `zellij:tab-bar` URLs still work.
- Community: zjstatus (a wasm status-bar plugin) is used for custom bars, example at https://haseebmajid.dev/posts/2024-07-26-how-i-configured-zellij-status-bar (blog, reliability: medium).
- Relevance: MEDIUM. Our observer draws its own header/footer; Zellij bars are chrome outside it and would not count toward parity with the mockup PNGs unless the mockups include them (unverified here).

### A4. Themes
- Sources: https://zellij.dev/documentation/themes.html , https://zellij.dev/documentation/legacy-themes.html (official, highest)
- Themes are KDL `themes { name { ... } }` nodes, in the main config or a themes directory; selected with `theme "name"`. The new spec uses UI-component nodes (e.g. `ribbon_unselected { base .. background .. emphasis_0 .. }`); the legacy spec (`fg bg black red green ... orange`) is still supported and accepts truecolor RGB triples, 256-colour indexes or hex strings. `theme_dark`/`theme_light` switch automatically when the host terminal reports its colour scheme (needs both set).
- Relevance: MEDIUM. Local theme aidev02 is ANSI-16. Theme only styles Zellij's own chrome (bars, frames); it does not recolour the observer's output except that ANSI-16 indexes may map through the host terminal palette (inference, not in docs).

### A5. Can an application detect it is inside Zellij?
- Source: https://zellij.dev/documentation/nested-sessions.html (official, highest): "Guest sessions detect that they are nested by way of the `ZELLIJ` environment variable, which Zellij sets in all the panes it opens."
- Source: https://github.com/zellij-org/zellij/issues/3637 (issue thread, reliability: medium) shows `ZELLIJ_PANE_ID` and `ZELLIJ_SESSION_NAME` are also set in pane shells.
- Third-party example: https://operator.untra.io/getting-started/sessions/zellij requires `ZELLIJ` to be set (blog/docs, medium).
- Caveat from the issue above: a subshell that changes TMPDIR can lose the session, so detection by env var is reliable but CLI control from inside is not always.
- Relevance: HIGH for Q6. The observer can read `ZELLIJ` and behave identically either way; it must not require it.

### A6. 256-colour and truecolor behaviour
- No Zellij documentation page found in this search that states how Zellij downgrades or passes through truecolor and 256-colour output. Not confirmed. Searches returned only theme-spec pages (legacy-themes.html shows truecolor, 256 and hex theme formats).
- General background (blog, medium): https://marvinh.dev/blog/terminal-colors : detect truecolor by `COLORTERM` = `24bit` or `truecolor`; 256-colour by `$TERM` ending in `256color`.
- Relevance: MEDIUM. For Q6, whether Zellij preserves truecolor must be verified locally with a live session (`zellij attach --create-background`, print a gradient, `dump-screen --ansi`). Our 16-colour design avoids the question.

### A7. Version discrepancy
- https://zellij.dev/news/terminal-inbox-session-previews (official, highest) announces Zellij 0.46.0 dated 2026-11-11. Local install is 0.44.2 (verified locally, source of truth). Nested sessions are documented as since 0.45.0; the programmatic dump-screen/list-panes/send-keys CLI is documented as new in 0.44.0, so those 0.44 features are present locally. Docs at zellij.dev reflect the latest version, so some pages (for example `--pane-id` on every action, or `zellij:bars`) may describe newer behaviour than 0.44.2; check `zellij action dump-screen --help` locally before relying on a flag.
- Relevance: HIGH (the documentation may be ahead of the installed binary).

## Part B: Offline terminal-to-image findings

### B1. Rich export_svg / export_html (already installed locally: Rich 15.0.0)
- Source: https://rich.readthedocs.io/en/latest/console.html and https://rich.readthedocs.io/en/stable/reference/console.html (official docs for 14.1.0; local is 15.0.0, so details may differ) (reliability: highest)
- `Console(record=True)` is required; then `export_text()`, `export_svg()`, `export_html()` or `save_*`. `export_svg(theme=...)` accepts a theme from `rich.terminal_theme` (e.g. MONOKAI); `export_html(theme, clear, code_format, inline_styles)` also exists. Recording keeps what was printed, so a render driven through a Console with `color_system` forced (for example `"standard"` for 16 colours, or `None` for NO_COLOR) should record the downgraded styles. This is an inference from the docs; not tested locally.
- Source: https://github.com/Textualize/rich/issues/2153 (GitHub issue, reliability: medium-high, from Rich 12.1.0 in 2022): Rich SVG output works fully only in Chromium-based browsers; `rsvg-convert` and ImageMagick `convert` fail to give usable output; the SVG uses `foreignObject` and a `@font-face` for Fira Code with `local()` plus remote URLs. The issue was reported closed; the reason for closing was not shown in the extract, so whether Rich 15 changed this is UNVERIFIED.
- Relevance: HIGH for Q3. Matches the local finding that `rsvg-convert`/`cairosvg` are absent, and warns that installing them may not help for Rich SVG. SVG-to-PNG needs a real browser engine. Also the font URLs are remote: offline rendering relies on a locally installed monospace font (`local()` match) or a fallback, which affects glyph widths.

### B2. Playwright browser as rasteriser
- Source: https://snapshotflow.com/blog/playwright-screenshot and https://www.scrapingbee.com/webscraping-questions/playwright/how-to-take-screenshot-with-playwright (blogs, reliability: medium). `page.screenshot(path="x.png")` captures the viewport; `full_page=True` captures the whole document; `locator.screenshot()` captures one element; omitting `path` returns bytes. Viewport size is settable. Python install is `playwright install chromium` (downloads a browser; not offline-friendly on first run).
- No source found that explicitly states screenshotting a `file://` SVG; navigating a browser to a local SVG or HTML file and capturing it is standard browser behaviour (inference).
- Local fact (source of truth): Playwright is not installed in the repo environment; the Playwright MCP browser exists only inside the Claude session. So a Claude reviewer session could open the exported SVG/HTML via the MCP browser and screenshot it, but a repo-level CI script cannot depend on that.
- Relevance: HIGH for Q3. Workable in an interactive Claude session (the compare loop is run by a Claude agent), not in plain CI.

### B3. freeze (charmbracelet)
- Sources: https://github.com/charmbracelet/freeze (official repo, reliability: high); https://www.getclaudeskills.com/skills/terminal-screenshot-daymade (third-party skill page, reliability: low-medium)
- Renders code or ANSI output to PNG, SVG or WebP (`-o out.png`; default out.svg or stdout when piped). Defaults: font JetBrains Mono 14px, line height 1.2; `--font.file` embeds a TTF/WOFF/WOFF2 font; options include `--window`, `--padding`, `--margin`, `--background`, `--height`. Install: Homebrew, packages for Debian and RPM, binaries for Linux/macOS/Windows, or `go install github.com/charmbracelet/freeze@latest`. Supports `--execute` to run a command.
- Third-party guidance: capture ANSI in a normal shell first and render second; `--execute` runs the command in freeze's child pty where tools may detect a reduced environment and drop colour. Also warns that `brew install freeze` may install an unrelated cask of the same name (single source, unverified).
- Not confirmed in this search: licence type (a LICENSE file exists in the repo listing), exact PNG rasteriser used, behaviour with ANSI input files in detail.
- Install cost: one static Go binary, but it is absent locally and needs network access to install (go toolchain presence not checked). Offline CI suitability: yes after the binary is vendored or pre-installed. It adds window chrome and padding by default, which would need disabling to compare against a mockup.
- Relevance: MEDIUM-HIGH. Best single-tool ANSI to PNG option if an extra binary is allowed; does not fit the "no new tools" constraint.

### B4. pyte
- Sources: https://pyte.readthedocs.io (official docs, reliability: high); https://cefboud.com/posts/terminals-pty-tty-pyte (blog, medium)
- Pure-Python in-memory VTXXX terminal emulator: `Screen(cols, rows)` and `Stream`; feed ANSI bytes, then read each cell's character and attributes. Docs list use cases: screen-scraping terminal apps and building terminal emulators. The blog shows converting the screen buffer to HTML. It does not make images by itself; an image library or the browser is still needed.
- Combined with local `pexpect` it can run the observer in a PTY at a fixed size and capture the screen exactly as a terminal would show it, including cursor-addressed output (alt-screen apps). Licence not confirmed in this search (not verified). Absent locally.
- Relevance: MEDIUM. Useful only if the observer uses live cursor control; `render_current.py` renders through Rich directly, which already avoids a PTY.

### B5. aha, ansi2html, termshot
- aha: https://github.com/theZiz/aha (repo, reliability: high): converts ANSI escapes to HTML; e.g. `... | aha --black --title "..." > out.htm`. Licence not confirmed here.
- ansi2html: https://github.com/pycontribs/ansi2html (repo history shows the licence was changed to LGPLv3+ in Nov 2017).
- Both produce HTML that still needs a browser to become an image. Rich `export_html` already gives HTML without a new dependency.
- termshot: no source found in this search; not assessed.
- Relevance: LOW (redundant with Rich export_html).

### B6. SVG to PNG without a browser (cairosvg, rsvg-convert)
- Source: https://www.twilio.com/en-us/blog/developers/tutorials/product/sending-svg-images-sms-whatsapp-python-cairosvg (blog, medium): `pip install cairosvg`; `cairosvg.svg2png(url=..., parent_width=..., parent_height=...)`. https://phauer.com/2018/install-cairo-cairosvg-alpine-docker (blog, medium): CairoSVG needs the Cairo system library and Pillow; installing it in slim containers needs extra OS packages.
- Combined with B1: Rich SVG relies on `foreignObject`/`@font-face`, which non-browser rasterisers do not support, so cairosvg and rsvg-convert are unlikely to produce a usable image from `export_svg` (inference from issue #2153, which tested rsvg-convert and ImageMagick, not cairosvg).
- Relevance: MEDIUM (negative finding). Do not plan on these without a test on a real Rich export.

### B7. How an AI reviewer compares a render to a mockup PNG
- Local fact: Claude agents view PNG files with the Read tool (source of truth). No external source was needed. Findings from sources that bear on it: PNG output must be fixed-size per width (Playwright viewport, freeze `--width/--height` flags are not listed in the extract; viewport size is settable in Playwright), and fonts must be the same between runs, otherwise reviewer scoring varies on glyph metrics rather than design (inference).
- A text-based comparison path avoids images altogether: Zellij `dump-screen --ansi` (A2) or Rich `export_text` give per-cell text and styles that a script or reviewer can diff; an image is then needed only for the mockup-versus-render visual score.
- Relevance: HIGH for Q3.

### B8. Discrepancy and gap notes
- Local `render_current.py` uses `export_text(styles=True)`; Rich docs show `export_text` takes `clear` and `styles` and records what the Console emitted. If the recording Console is created with a forced colour system, the export should carry the downgrade; the existing issue is likely that the Console used for recording is not configured for NO_COLOR/16-colour (inference, needs local test).
- Not found: any documented way to rasterise Rich SVG to PNG offline without a browser; Zellij documentation on truecolor/256-colour downgrade; confirmed licences for freeze, pyte, aha and cairosvg.

## Key External Findings

- Zellij 0.44 CLI can drive a headless session (`attach --create-background`, `new-pane`, `send-keys`, `dump-screen --ansi`), so a Zellij capture is possible without a PTY library, but it yields ANSI text, not an image (HIGH).
- Zellij sets the `ZELLIJ` environment variable (plus `ZELLIJ_PANE_ID`, `ZELLIJ_SESSION_NAME`) in every pane, so the observer can detect Zellij and must not require it (HIGH).
- Floating panes are declared in a layout with a `floating_panes { pane ... x y width height }` node; bars come from `plugin location="zellij:tab-bar|status-bar|compact-bar"`; themes are KDL `themes {}` nodes and only style Zellij chrome (HIGH/MEDIUM).
- Zellij docs are newer than the local binary: 0.46.0 was announced 2026-11-11, local is 0.44.2; some documented flags may not exist locally (HIGH).
- Rich SVG export is browser-only in practice: `rsvg-convert` and ImageMagick failed on it in a Rich issue (`foreignObject`, remote `@font-face`); cairosvg is untested for it (HIGH).
- Playwright can screenshot a page at a set viewport, to a file or bytes; it needs a downloaded browser (CI) or the Claude-session MCP browser (interactive) (HIGH/MEDIUM).
- freeze is the simplest ANSI to PNG tool but is an extra binary that is not installed (MEDIUM-HIGH).
- No source found for Zellij colour-depth handling or for several licences (gap).

## Recommendations from External Research

1. Q3 harness: keep Rich as the single renderer. Record with a Console configured per case (truecolor, 256, 16-colour, NO_COLOR, ASCII) so the exported text/ANSI/HTML reflects the real downgrade, then convert to PNG in the Claude session by opening the Rich `export_html` (or `export_svg`) file in the Playwright MCP browser at a fixed viewport matching the mockup width. Test this path once on a real observer render before committing the spec to it (not verified here).
2. Do not plan on `cairosvg` or `rsvg-convert` for Rich SVG until tested; the Rich issue suggests failure. If a repo-level (non-Claude) PNG step is required, the lowest-friction extra is freeze with a vendored binary, or Playwright with `playwright install chromium`; both need approval and network at install time.
3. Add a text-first compare tier that needs no image: per-width ANSI/plain text from `render_current.py`, with a structural check (widths, line counts, presence of key labels, NO_COLOR has no escapes, ASCII has no non-ASCII), and use the image render only for the reviewer's visual score against the mockup PNGs. Keep the same installed monospace font between runs so scores are stable.
4. Q6 Zellij: GO conditional. The observer can stay standalone (read `ZELLIJ` only as an optional hint, never a requirement), stays read-only, and all widths/NO_COLOR/ASCII keep working because Zellij only wraps it in a pane. Use Zellij for an optional layout (floating or tiled observer pane) and optionally as a second capture method (`dump-screen --ansi`) in a manual check. Do not make Zellij a dependency of the render gate.
5. Before relying on any Zellij docs claim, run `zellij action dump-screen --help`, `zellij action new-pane --help` and a one-off background session test on 0.44.2, because the docs describe a newer release. Also test truecolor and 256-colour pass-through locally since no source covered it.
6. Treat the licence gaps as open: confirm the licence of any tool chosen (freeze, pyte, cairosvg, aha) before adding it; ansi2html is LGPLv3+.

Status: Complete
