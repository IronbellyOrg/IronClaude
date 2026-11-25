# Research: Design package fixture-to-export pipeline (GF-5)
**Investigation type:** Code Tracer
**Scope:** /home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/{render.py,fixtures.py,canvas.py,layouts/group_a.py,layouts/group_b.py,layouts/agent_focus.py,tests/test_designs.py,tests/test_gallery.cjs,README.md}
**Status:** Complete
**Date:** 2026-11-20
---

Gap resolved: GF-5 (qa/qa-research-consolidated-findings.md row GF-5; qa/qa-research-depth-report.md F-4). Gap text: the design package's own fixture-to-export pipeline is untraced (render.py flags, call chain, write_fixtures outputs, --batch 2, tests, README commands).

Path key: PKG = /home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106 (checkout, docs branch docs/409-orca-dashboard-designs, commit 495eb96d1). Line counts (wc -l): render.py 130, fixtures.py 122, canvas.py 122, layouts/group_a.py 230, layouts/group_b.py 224, layouts/agent_focus.py 183, tests/test_designs.py 117, tests/test_gallery.cjs 22, README.md 52. Nothing was run: no renderer, no tests, no node. Only the Read tool plus one read-only `ls`/`head`/`grep` listing of existing artifacts were used.

## 1. render.py command line (PKG/render.py)

Entry guard `if __name__=="__main__":` at render.py:126; whole argparse setup on one line, render.py:127.

| Flag | Definition (render.py:127) | Default | Effect |
|---|---|---|---|
| `--batch` | `type=int, choices=(1,2)` | 1 | selects layout modules (render.py:21) and output folder (render.py:43) |
| `--show` | no type, no default (None) | None | when given, prints one screen and exits; otherwise runs `exports(args.batch)` (render.py:128-130) |
| `--width` | `type=int` | 116 | used only by the `--show` branch (render.py:129); ignored in export mode |

Branches (render.py:128-130):
- `--show <slug>`: `screen(designs(args.batch)[args.show], fixture(), args.width).ansi(no_color="NO_COLOR" in os.environ)`, printed with `end=""`. The `NO_COLOR` test is "variable present in the environment" (any value, including empty). Writes no file and does not call `write_fixtures`. A slug from the other batch raises KeyError (the dict is `designs(args.batch)`); `--width` is not restricted to the three export widths (any int; height rule at render.py:27).
- no `--show`: `exports(args.batch)` (render.py:130).

Module constants: `ROOT=Path(__file__).resolve().parent` (14); `WIDTHS=(160,116,80)` (15); `FONT_PATH`/`BOLD_PATH` = DejaVuSansMono(.ttf/-Bold.ttf) under /usr/share/fonts/truetype/dejavu/ (16-17); `CW,CH,PAD = ImageFont.truetype(FONT_PATH,16).getlength("M"), 20, 20` (18, executed at import time, so importing render.py needs Pillow and that font file; existence of the font on this host was not checked). Imports `PIL.Image/ImageDraw/ImageFont` (10), `canvas.Canvas, PALETTE` (11), `fixtures.fixture, metrics, write_fixtures` (12). Declared dependencies: PKG/requirements.txt = `Pillow==13.0.0`, `wcwidth==0.9.4` (wcwidth is imported by canvas.py:5).

Key Takeaways: three flags only; `--width` matters only with `--show`; export mode always renders widths 160/116/80 and ignores `--width`; font path is hard-coded and read at import.

## 2. Call chain: designs -> screen -> layout -> Canvas -> exports

### 2.1 designs(batch=1) (render.py:20-24)
- `modules=("layouts.group_a","layouts.group_b") if batch==1 else ("layouts.agent_focus",)` (21); `importlib.import_module(name).DESIGNS` merged with `result.update` in tuple order (22-23). Result order = dict insertion order: group_a's five then group_b's five (batch 1); agent_focus's ten (batch 2).
- Layout module registries (each a `DESIGNS` dict, value keys name/question/omits/tradeoff/data/missing/render):
  - layouts/group_a.py: `DESIGNS` at 224-230; 5 entries (225-229): signal-bridge -> `signal_bridge` (def 56), fleet-quilt -> `fleet_quilt` (103), time-loom -> `time_loom` (133), worktree-atlas -> `worktree_atlas` (163), decision-desk -> `decision_desk` (195). Docstring line 1: "Five offline observation compositions".
  - layouts/group_b.py: `DESIGNS` at 218-224; 5 entries (219-223) built with `dict(...)`: proof-gate -> `proof_gate` (def 29), budget-engine -> `budget_engine` (68), relay-map -> `relay_map` (123), delta-deck -> `delta_deck` (163), watchkeeper -> `watchkeeper` (188).
  - layouts/agent_focus.py: `DESIGNS={}` (171) filled by one loop `for slug,name,fn,q,omits in [...]` (172-182) with 10 tuples; the loop body (183) builds `{"name","render":fn,"question","omits","tradeoff","data","missing"}` where tradeoff/data/missing are the same three constant strings for all ten. Slugs: leverage-board (def 26), attention-ledger (41), handoff-switchboard (55), loop-detector (70), collision-lens (88), outcome-ledger (105), revision-drift (116), mission-pulse (129), owner-load (143), shift-brief (156 `shift`).
  - Layout-module imports: agent_focus.py:2-3 imports only `canvas.selected_summary` and `fixtures.metrics`; group_a.py and group_b.py have no import lines (lines 1-3 are docstring and blank). So set 2 does not reuse set 1's layout functions (matches README.md:15).

### 2.2 screen(spec, f, width, ascii_mode=False) (render.py:26-29)
- `c=Canvas(width, 48 if width>=144 else 42, ascii_mode)` (27): height 48 for 160, 42 for 116 and 80 (and 144 in the tests).
- `spec["render"](c, f, metrics(f))` (28): every layout function has the signature `(c, f, m)`; `m=metrics(f)` is the aggregate dict (fixtures.py:98-111). Returns the Canvas (29).

### 2.3 Canvas (canvas.py)
- `Canvas.__init__(width,height=48,ascii_mode=False)` (32-37): grids `cells` (space), `colors` ("ink"), `weights` (False); lists `regions`, `details`, `clipped`.
- Drawing primitives: `text` (38-55, asserts in-bounds and `color in PALETTE`, sanitizes, clips via `clip`, wide-char aware via `wcwidth`), `line` (56), `panel` (57-64), `lines` (65-68), `bar` (69-72), `header` (73-77; writes "SYNTHETIC · READ ONLY" at 75), `footer` (78-81; footer text starts "j/k select", asserted by the tests), module function `selected_summary` (117-122).
- `sanitize` (10-17) strips OSC/DCS/CSI/other escapes and Cc/Cf/Cs characters; `clip` (19-29) truncates by display width, with ASCII fallback (`ASCII_MAP`, line 8, applied when `ascii_mode`).
- `PALETTE` (7): ten named colors (bg, panel, ink, muted, line, accent, warn, bad, good, frozen).
- Export renderers on Canvas: `plain()` (82) text rows; `ansi(no_color=False)` (83-96) 24-bit SGR runs per row, `no_color` returns `plain()`; `html()` (97-108) `<span class="c-<color>[ strong]">` runs; `svg(cw=10,ch=20)` (109-114) one `<text>` per non-blank cell on `PALETTE["bg"]` rect.
- PNG is not a Canvas method: `image(c,no_color=False)` in render.py:31-39 draws each non-blank cell with DejaVu (bold when `weights`), fill `PALETTE["ink"]` if `no_color` else `PALETTE[c.colors[y][x]]`; image size `(round(c.w*CW+2*PAD), c.h*CH+2*PAD)`.

Key Takeaways: one `Canvas` per (design, width, ascii?) feeds every export; the layout function is the only place content is composed; batch 1 and batch 2 differ only in which `DESIGNS` modules `designs()` imports.

## 3. exports(batch=1) step by step (render.py:41-74)

1. `write_fixtures(ROOT)` (42) always first, for both batches; it writes into ROOT, not `out` (see section 5).
2. `out = ROOT if batch==1 else ROOT/"agent-focus"` (43); `out.mkdir(exist_ok=True)` (44). Note: not `parents=True`; ROOT exists, so fine.
3. `ds=designs(batch); f=fixture(); manifest={"synthetic":True,"as_of":f["as_of"],"batch":batch,"widths":WIDTHS,"concepts":[]}` (45); `pages=[]` (46).
4. For each `slug,spec` in `ds` (47): `entry` = spec minus the `render` key, plus `slug` and an empty `exports` dict (48). For each width in `WIDTHS` (49):
   - `folder = out/"exports"/str(width)`, `mkdir(parents=True, exist_ok=True)` (50).
   - `c=screen(spec,f,width)` (colored canvas) and `ac=screen(spec,f,width,True)` (ASCII-mode canvas), `prefix=folder/slug` (51).
   - Six files per (design, width), by suffix:

| Suffix | Written by | Line |
|---|---|---|
| `.txt` | `prefix.with_suffix(".txt").write_text(c.plain())` | 52 |
| `.ascii.txt` | `prefix.with_suffix(".ascii.txt").write_text(ac.plain())` (ASCII-mode canvas) | 53 |
| `.ansi` | `...write_text(c.ansi())` | 54 |
| `.svg` | `...write_text(c.svg(cw=CW,ch=CH))` | 55 |
| `.png` | `im=image(c); im.save(prefix.with_suffix(".png"))` | 56 |
| `.mono.png` | `image(c,True).save(folder/(slug+".mono.png"))` | 57 |

   - `entry["exports"][str(width)] = str(prefix.relative_to(out))` (58), e.g. `exports/160/signal-bridge` (no suffix).
   - Only at width 160: `pages.append((slug, spec["name"], im))` (59) (the colored PNG).
   - After the width loop: `manifest["concepts"].append(entry)` (60).
5. Contact sheet (61-68): `thumb_w=800; thumb_h=round(pages[0][2].height*thumb_w/pages[0][2].width)` (61); canvas `Image.new("RGB",(thumb_w*2,(thumb_h+40)*((len(pages)+1)//2)),PALETTE["bg"])` (62) = 2 columns, rows = ceil(pages/2); per page title in DejaVu Bold 18 at (x+16,y+8) and the 160-width PNG resized (LANCZOS) to 800 wide at (x,y+40), cell `x=i%2*thumb_w`, `y=i//2*(thumb_h+40)` (63-67); saved to `out/"contact-sheet.png"` (68).
6. Portfolio (69-70): `pdf_pages=[im.convert("RGB") ...]` from the same 160-width `pages`; `pdf_pages[0].save(out/"portfolio.pdf", save_all=True, append_images=pdf_pages[1:], resolution=120, creationDate=time.gmtime(0), modDate=time.gmtime(0), title="Synthetic Orca observation designs")`. Fixed creation/modification dates (epoch) are passed, so the PDF carries no wall-clock timestamp from these two fields.
7. Manifest (71-72): `manifest["fixture_sha256"]=sha256(ROOT/"fixture.json" bytes)`; `(out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")`. The hash file is always ROOT/fixture.json, also in batch 2.
8. `build_gallery(out,ds)` (73), then prints `Rendered {len(ds)} designs x {len(WIDTHS)} widths into {out}` (74).

Per-run file counts derived from the code (not observed by running): per batch 10 designs x 3 widths x 6 suffixes = 180 export files, plus contact-sheet.png, portfolio.pdf, manifest.json, gallery.html. On disk the checked-in `exports/160` and `agent-focus/exports/160` each list 60 files (10 x 6), matching.

Key Takeaways: the order is exports -> contact sheet -> PDF -> manifest -> gallery; contact sheet and PDF use only the width-160 colored PNGs; the manifest is written after the contact sheet and PDF and records the fixture hash.

## 4. build_gallery(out, ds) (render.py:77-124)

- Scenarios (79-80): `scenarios={"base":fixture()}` then every `ROOT/"scenarios"/*.json` in sorted order, key = file stem, value = parsed JSON. Because `write_fixtures` runs first, ROOT/scenarios holds 18 files, so 19 scenarios (base + 18); on disk `scenarios/` holds 18 files.
- Frames (81-85): for each scenario, each design, each width in `WIDTHS`: `{"html": screen(spec,f,w).html(), "ascii": screen(spec,f,w,True).plain()}`. Comment at 78: every selectable scenario has separately composed screens, no rescaling. Derived work: 19 x 10 x 3 = 570 frame pairs = 1,140 Canvas builds per gallery.
- `metadata` = spec minus `render` per slug (86). `payload=json.dumps({"frames","scenarios","designs"},ensure_ascii=True).replace("<","\\u003c")` (87) (script-tag safe).
- CSS string (88-91) with `.c-<palette key>` color classes from `PALETTE`. HTML template (92-123): single self-contained page titled "Orca Observation Studio"; payload embedded in `<script id="data" type="application/json">` (100); inline JS (100-122) handles design switching, width select, no-color checkbox (CSS class toggle, no second render), ASCII checkbox, hold/queue/resume, owner/search inspector filter; footer links (99) to `portfolio.pdf`, `contact-sheet.png`, `manifest.json` (relative to the gallery file's folder). Owner select options O01..O10 are generated for `i in 1..10` (119).
- Written to `out/"gallery.html"` (124), so batch 2 produces `agent-focus/gallery.html`.
- Not produced by render.py (no write call in render.py): PKG/index.html, PREVIEWS.md, QA.md, PLAN.md, DESIGN-CONTRACT.md, README.md, concepts.md, data-dictionary.md, integration-gaps.md, sources.json. They exist in the folder but were authored outside this renderer (author of each not traced here).

Key Takeaways: gallery.html is the last artifact and embeds every scenario at every width as pre-rendered HTML plus ASCII; it fetches nothing and has no polling (also asserted by tests/test_gallery.cjs:21).

## 5. fixtures.py: fixture, metrics, write_fixtures

- `fixture(owners=8, count=80, variant="base")` (11-87): asserts `owners in (5,8,10)` and `count in (50,80,100)` (12); `STAMP="2026-11-06T08:00:00Z"` (6) is `as_of`; builds `sources` (5 ids with observed_at/age_s/coverage), `orchestrators` (names from `NAMES`, missions from `MISSIONS`, lines 7-8), `sessions`, `worktrees` (loop 22-47), `requests` (3, lines 50-57), `edges` (3, 58-60), `events` (4, 61-64), `previous` (65), `scope`. Fully deterministic: no clock, environment or network reads (docstring line 1).
- Variants applied after the base build (66-86): `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, plus `uneven` (handled in the owner assignment at 24-25) and `injection` (86, an escape-sequence label).
- `normalize_events(events)` (90-95): keep the highest `seq` per event id, sorted by `(seq,id)`.
- `metrics(f, owner=None)` (98-111): returns the aggregate dict (keys: sessions, total, global_total, historical, worktrees, inventory_worktrees, unmapped, running, settled, unknown, stale, failed, frozen, admitted, cost, cost_measured, affected, events). Historical sessions are excluded from totals.
- `write_fixtures(root)` (114-122):
  - Input: `root` (render.py passes ROOT). Creates `root/"scenarios"` with `mkdir(exist_ok=True)` (115).
  - Output 1: `root/"fixture.json"` = `json.dumps(fixture(),indent=2)+"\n"` (116) (base: 8 owners, 80 sessions).
  - Output 2: nine named-variant files `scenarios/<variant>.json` (117-119): uneven, shared-unmapped, historical, long-identifiers, source-loss, missing-fields, duplicate-out-of-order, empty, injection.
  - Output 3: nine scale files `scenarios/scale-<owners>-<count>.json` for owners in (5,8,10) x count in (50,80,100) (120-122).
  - Total: 1 + 9 + 9 = 19 files; 18 of them in `scenarios/` (confirmed by `ls`: 18 files present), `fixture.json` at the package root.
- Both batches call it (render.py:42), so `--batch 2` rewrites ROOT/fixture.json and ROOT/scenarios/ (not `agent-focus/`), and batch 2's gallery reads ROOT/scenarios (render.py:80).

Key Takeaways: one function writes all scenario inputs, and it runs on every export; the scenario file set (18) equals the gallery's selectable scenarios minus `base`.

## 6. What `--batch 2` changes

Exactly two switches, both keyed on `batch`:
1. `designs(2)` returns `layouts.agent_focus.DESIGNS` (10 designs: leverage-board ... shift-brief) instead of group_a + group_b (render.py:21).
2. `out = ROOT/"agent-focus"` (render.py:43): `exports/<width>/<slug>.<suffix>`, `contact-sheet.png`, `portfolio.pdf`, `manifest.json` (with `"batch": 2`, render.py:45) and `gallery.html` are all written under `PKG/agent-focus/` instead of PKG.

Unchanged by batch: fixture (`fixture()`), WIDTHS, Canvas and image code, the `fixture.json`/`scenarios/` location (ROOT), `fixture_sha256` source. Observed on disk (listing only): `agent-focus/` contains `contact-sheet.png, exports/, gallery.html, manifest.json, portfolio.pdf`; both manifests show `"batch"` 1 and 2 and the same `fixture_sha256` `1f17a907...bd42e4`; slugs in `manifest.json` = the five group_a + five group_b slugs; slugs in `agent-focus/manifest.json` = the ten agent_focus slugs. Existing files' mtimes show 2026-11-06 (11:45) for both batches. With `--show` the flag selects which registry the slug is looked up in (render.py:129).

Key Takeaways: `--batch 2` = a different layout module and a different output folder; nothing else.

## 7. Test entries

### 7.1 tests/test_designs.py (117 lines; stdlib `unittest`; `unittest.main(verbosity=2)` at 117)
- Header: `ROOT=Path(__file__).resolve().parents[1]`, `sys.path.insert(0,str(ROOT))` (8-9), imports `fixture, metrics, normalize_events`, `Canvas, clip, sanitize`, `render.designs, render.screen` (10-12). Importing `render` requires Pillow and the DejaVu font (render.py:10, 18).
- 19 test methods in three classes:
  - `Semantics` (14-58), 10 tests: test_scale_matrix, test_declared_relationships, test_source_age_matches_timestamp, test_mapping_not_assumed, test_history_separate, test_evidence_is_not_admission, test_partial_subtotal, test_events_idempotent, test_filter_denominators, test_empty. Fixture-data only.
  - `SafeText` (60-74), 5 tests: test_control_injection, test_width, test_ascii, test_no_color, test_html_escape.
  - `Layouts` (76-115), 4 tests: test_all_scenarios_widths (77-90: 9 scale cases + 9 variants = 18 fixtures x 20 designs (`{**designs(),**designs(2)}`, asserted len 20 at 80) x widths 160/144/116/80, checking every line's display width == width, "SYNTHETIC" present, no ESC, second-to-last line starts with "j/k select", determinism (same output twice), ASCII output `isascii()`); test_quilt_identifiable_base (91-96); test_cost_missing_is_not_zero (97-103); test_export_manifest (104-115).
- `test_export_manifest` (104-115) is the only test that reads generated artifacts: for roots `ROOT` and `ROOT/'agent-focus'` it asserts `manifest.json` exists, `len(concepts)==10`, for each concept and width 160/116/80 the files `.txt .ascii.txt .ansi .png .svg` exist (line 112; `.mono.png` is not checked), the `.ansi` text with SGR codes stripped equals the `.txt` text (114), and `portfolio.pdf` starts with `%PDF` (115). It does not check `contact-sheet.png`, `gallery.html` or `fixture_sha256`. It requires both batches to have been generated first (assert message "Exports missing").
- The tests call `screen`/`designs` directly; they never call `exports()` or `write_fixtures`, so they write nothing.

### 7.2 tests/test_gallery.cjs (22 lines; Node, stdlib only: fs, vm, assert, path)
- File under test: `process.argv[2]` or `../gallery.html` relative to the test folder (3). Extracts the JSON payload (5) and the inline script (6, regex relies on `</script><script>` in render.py's template at line 100) and runs the script in a `vm` context with a hand-built DOM stub (8-12); not a browser test (comment line 1).
- Assertions (13-21): ten concept buttons; "SYNTHETIC" in the screen; ArrowRight changes the title; width 80 and ASCII mode; owner O01 filter shows "10 inspector records / 80 global records"; hold/queue/resume messages; scenario `empty` shows "not an all-clear"; no `fetch(` and no `setInterval(` in the HTML. Prints a PASS line (22).

Key Takeaways: Python tests cover fixtures, sanitizing, layout geometry and export presence; Node test covers the gallery's DOM contract only; neither test regenerates anything.

## 8. README.md commands (PKG/README.md:24-26 plus 27-28) - NOT RUN

README.md:19-29 "Reproduce", "From the IronClaude root" (21):

| README line | Command (as documented) | What the code does | Status |
|---|---|---|---|
| 24 | `uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/render.py` | batch 1 `exports(1)`: writes into PKG (fixture.json, scenarios/, exports/, contact-sheet.png, portfolio.pdf, manifest.json, gallery.html) | not run |
| 25 | same, with `render.py --batch 2` | batch 2 `exports(2)`: writes into PKG/agent-focus/ (plus rewrites ROOT fixture.json and scenarios/) | not run |
| 26 | same, with `tests/test_designs.py` | runs the 19 unittest tests (7.1); needs both batches generated for test_export_manifest | not run |
| 27 | `node .dev/design/orca-observer-20261106/tests/test_gallery.cjs` | gallery test on PKG/gallery.html (not part of lines 24-26) | not run |
| 28 | `node ... tests/test_gallery.cjs .dev/design/orca-observer-20261106/agent-focus/gallery.html` | same on batch-2 gallery (not part of lines 24-26) | not run |

README.md:31 documents `render.py --show <concept-slug> --width 116`, slugs listed in manifest.json, `NO_COLOR=1` disables ANSI: **[CODE-VERIFIED]** at render.py:127-129 (`--width` default 116; NO_COLOR presence check at 129).

Doc claims checked against code:
- README.md:15 "Set 2 share the fixture and renderer, not the first set's layout functions; exports, gallery and PDF live under agent-focus/": **[CODE-VERIFIED]** agent_focus.py:2-3 imports, render.py:43, folder listing.
- README.md:17 "Designs render separately at 160, 116 and 80": **[CODE-VERIFIED]** render.py:15, 49.
- README.md:9 "both PDF portfolios": **[CODE-VERIFIED]** render.py:70 with both batches; files present on disk.
- README.md:33 "Open gallery.html directly from disk. No web server, network fetch or CDN": **[CODE-VERIFIED]** the page embeds its data (render.py:100) and the Node test asserts no `fetch(`/`setInterval(` (test_gallery.cjs:21).
- README.md:37 "eight orchestrators, 80 current sessions and 80 mapped worktrees": **[CODE-VERIFIED]** fixtures.py:11 defaults and loop 22-47; test_designs.py:20.
- README.md:44 "Previous prototype files are preserved unchanged": **[UNVERIFIED]** not traceable in the six code files (a statement about earlier packages; no code or git comparison made here).

Key Takeaways: three documented commands at README.md:24-26 map one-to-one to `render.py`, `render.py --batch 2`, `tests/test_designs.py`; the two `node` commands sit at 27-28. All five documented as "from the IronClaude root", none run here.

## 9. End-to-end data-flow summary (hop list)

`render.py` CLI (127) -> `exports(batch)` (41) -> `write_fixtures(ROOT)` (fixtures.py:114) writes `fixture.json` + `scenarios/*.json` -> `designs(batch)` (20) imports `layouts.*.DESIGNS` -> `fixture()` (fixtures.py:11) -> per design x width: `screen()` (26) -> `Canvas(...)` (canvas.py:32) -> `spec["render"](c,f,metrics(f))` (layout fn) -> `Canvas.plain/ansi/svg` and `image()` -> six files under `<out>/exports/<width>/` -> 160-width PNGs -> `contact-sheet.png` (68) and `portfolio.pdf` (70) -> sha256 of `fixture.json` + `manifest.json` (72) -> `build_gallery()` (77) re-reads `scenarios/*.json`, rebuilds Canvases for every scenario, writes `gallery.html` (124).

## 10. Defect-candidate check (C8)
No in-scope capability that a spec or design names as shipped was found unwired in this package's pipeline: every documented output (README.md:9, 15-17, 24-28) has a writing call in render.py. No DEFECT-CANDIDATE recorded for the package pipeline. Facts to note, not defects: `--width` is silently ignored in export mode (render.py:127-130); test_export_manifest does not check `.mono.png`, contact sheet, gallery or hash (test_designs.py:112-115); batch 2 rewrites ROOT fixture.json/scenarios (render.py:42).

## Gaps and Questions
1. Nothing was executed, so file contents of generated artifacts (sizes, pixel dimensions, whether regenerating reproduces the checked-in bytes, PDF determinism beyond the two date fields) are not verified. Checked only: existence, names and counts via a read-only listing, and manifest headers/slug lists.
2. Font file `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` existence on this host was not checked (import-time dependency, render.py:16-18).
3. Authorship/generation path of PKG/index.html, PREVIEWS.md, QA.md and the other non-renderer files is not traced (no writer in render.py).
4. Whether the checked-in artifacts were produced by the current render.py (same bytes) is unverified; mtimes (2026-11-06 11:45) only show they were written together.
5. README.md:44 "Previous prototype files are preserved unchanged" is [UNVERIFIED].

## Stale Documentation Found
None found for the commands at README.md:24-28 and the `--show` instructions at README.md:31; every checked README claim is [CODE-VERIFIED] except README.md:44 [UNVERIFIED]. (No **[STALE DOC]** items.)

## Summary
The package pipeline is `render.py [--batch 1|2] [--show SLUG] [--width N]` -> `exports()` -> `write_fixtures` -> per-design/per-width `screen` -> `Canvas` -> six export files -> contact sheet and PDF from the 160-width PNGs -> manifest with fixture hash -> `build_gallery` (19 scenarios x 10 designs x 3 widths). `--batch 2` swaps the registry to `layouts/agent_focus.py` and the output folder to `agent-focus/`. Tests: 19 unittest tests in tests/test_designs.py plus the Node DOM test in tests/test_gallery.cjs. README commands at lines 24-26 documented, not run.
