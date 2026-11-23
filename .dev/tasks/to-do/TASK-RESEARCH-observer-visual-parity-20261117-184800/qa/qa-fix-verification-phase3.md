# QA Report - Phase 3 Fix Verification (fix-cycle 1)

**Topic:** observer visual-parity research, Gate 1 fix verification
**Date:** 2026-11-18
**Phase:** fix-cycle
**Fix cycle:** 1 (fix_authorization: false)

Scope: blocking findings 1 (safe_box ASCII claim, files 03 and 04) and 2 (live screen path addendum, file 02) from `qa/qa-consolidated-findings-phase3.md`.

## Checks

### Check A1. Finding 1 fixed in file 03 (line 194): PASS

- Read 03:194. The false claim is now tagged `[CODE-CONTRADICTED]`, states the correct behaviour, and requires an explicit `box=rich.box.ASCII` under `policy.ascii`. It cross-references file 01 lines 204 and 229, which exist and say the same.
- Independent probe (`uv run python -I`, Rich 15.0.0): `Panel("x")` first line is `'╭──────────────────╮'` for both `safe_box=True` and `safe_box=False`; with `box=box.ASCII` it is `'+------------------+'`. The research claim is true.
- Read `rich/box.py` `substitute` (lines about 75-90): ASCII substitution happens only on `options.ascii_only`; `safe_box` only gates the legacy-Windows table. Matches the claim.
- Read `terminal.py:123` (`safe_box=policy.ascii`) and `tests/observe/test_terminal.py:109,115`: the tests pin only `console.safe_box` values. Matches (cited range 114-116 vs actual 109 and 115 is a moved line number on a true claim: minor, note only).
- Cited test lines `test_render.py:263, :591, :903` and `test_commands.py:131` are ASCII tests (read).

### Check A2. Finding 1 fixed in file 04 (line 147, G-1 row): PASS

- Read 04:147. The claim that `safe_box` "covers only Rich Box objects" is removed from the CODE-VERIFIED text and replaced by a `[CODE-CONTRADICTED]` correction with the same probe result. The `terminal.py:30-34` GLYPHS claim and `terminal.py:133-135` `ascii_safe` claim were re-read in source and are true (GLYPHS has `selected`, `truncate`, `hrule` only).
- Residual search: `safe_box` in files 01 to 05. Remaining mentions are 01:18, 19, 25, 161, 204, 215, 229, 252, 02:14, 03:86, 194, 04:147. Each read; none claims `safe_box` ASCII-izes a Panel. 01:25 says `--ascii` "gives `safe_box=True`", which is correct (attribute value only). No residual false claim.

### Check B1. Finding 2 fixed: file 02 section 9 exists and is true: PASS

Section 9 (lines 159-205) added after Summary, with trace table (7 hops), 4 measurements, 3 capture routes and consequences. I verified each against source and my own probes.

- Hop 1: `commands.py:264-274` read; matches (shape :265, group :266, Live :269-271, start :272, update :274).
- Hop 2: `render.py:524-531` read; `Text(line, no_wrap=True, overflow="crop")` in a `Group`, no height clamp. True.
- Hop 3: `terminal.py:110-125` read; no `force_terminal`. True.
- Hops 4-7: read `rich/live.py` (screen alt-screen call about :127, `Screen(renderable) if self._alt_screen` :228, `vertical_overflow="ellipsis"` :68, reset to `"visible"` :161, `Control.home()` in `process_renderables`), `rich/screen.py:38-54` (`render_lines(pad=True)` then `Segment.set_shape(lines, width, height)`), `rich/console.py:1201-1217` (`set_alt_screen` writes only `if self.is_terminal and not self.legacy_windows`). All true.
- Measurement 1 reproduced byte for byte: `'\x1b[?1049h\x1b[H\x1b[?25l\x1b[H\x1b[1;31mL1\x1b[0m        \nL2        \nL3        \x1b[?25h\x1b[?1049l'`. Measurement 2 (height 5, all five lines) reproduced. Measurement 4 reproduced: non-terminal `StringIO` console, `Live(screen=True)` wrote `''`; `Console.print` of 5 lines at height 3 gave 5 newlines.
- Measurement 3 reproduced: `LINES=40 uv run superclaude observe --once --width 80 --fixture base` gave 40 lines (last `shown 28/54 | collected 80 / reported 80`, the two before it the key list and `28/54 shown  +26 more`). Fed to `Live(screen=True)` at height 40 all 40 rows appear; at height 38 the output has 38 rows, the last is `28/54 shown  +26 more`, the key list is gone and no ellipsis row appears. (My first check of "shown line" matched `collected 80` in the header; the last-row evidence settles it: the `shown 28/54 | ...` line is gone.) `vertical_overflow` read `ellipsis` before `stop()`, as the fix log says.
- Height budget claims: `render.py:499-502` (`reserved`, `capacity = max(policy.height - reserved, 1)`) and `render.py:491` (`max(..., 1)` for the inspector body) read; true. `terminal.py:22` `MIN_ROWS = 8` read; true.
- Route B: `pexpect` 4.9.0 installed (verified by `importlib.metadata`). `tests/observe/spike_child.py:64` is `with Live(screen, console=Console(), screen=True, auto_refresh=False)`; true. `grep -rnE 'LiveScreen|run_interactive' tests/observe` returned nothing; `grep -rn 'Live(' tests/observe` returned only `spike_child.py` (docstring line 1 and line 64). True.
- Q5 / issue 606 content (what styled capture of the live path needs, consequence for height budget and footer) is present in 9.3 and 9.4, which is what finding 2 required.

### Check B2. Cross-references added: PASS

02 section 3 Key Takeaways (line 61) points to section 9 and its content matches. 01:234 (item 8) points to 02 section 9 and the description is accurate. 05:76 points to 02 section 9.3 route B and the `pexpect>=4.9` declaration claim is consistent with the installed 4.9.0.

### Check C. Structure of files 01 to 05: PASS

Grep result: each of 01 to 05 has `**Status:** Complete` at line 4, a `## Gaps and Questions` section and a `## Summary` section (01: 225, 250; 02: 141, 155; 03: 222, 241; 04: 211, 240; 05: 131, 149).

### Check D. New blocking issues introduced: none found

- Section 9 in file 02 sits after `## Summary` (line 155), so the file no longer ends with its Summary, and the Summary and Gaps sections do not mention the addendum. Cosmetic structure: MINOR note only. The Key Takeaways at lines 58-61 and 201-204 carry the content.
- 02 section 2 and Summary still say a styled one-shot route uses `getvalue()` (unchanged, the earlier minor "Q5 undecided" note).
- Line-number drift: 03/04 cite `test_terminal.py:114-116` (actual 109 and 115); `rich/live.py:127-128` is about 125-130 in the installed copy. Moved line numbers on true claims: MINOR notes.
- No contradictions between 01, 02, 03, 04, 05 on `safe_box` or on the live path were found.

## Summary
- Checks passed: 6 / 6 (A1, A2, B1, B2, C, D)
- Checks failed: 0
- Blocking findings remaining: 0 (was 2)
- Critical issues: 0; Important: 0; Minor notes: 3 (addendum after Summary; test line range 114-116 vs 109/115; `live.py` line range drift)
- Issues fixed in-place: 0 (fix_authorization false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 02 section 9 after `## Summary` | Addendum placed after Summary | None required |
| 2 | MINOR | 03:194, 04:147 | `test_terminal.py:114-116` should be 109 and 115 | None required |
| 3 | MINOR | 02 section 9.1 hop 4 | `live.py:127-128` is about 125-130 in the installed copy | None required |

## Confidence
Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 14 | Grep: 7 | Glob: 1 | Bash: 5 (Rich probes, observer fixture run, line checks). Web: none used.

## Overall Verdict: PASS (0 remaining blocking findings)

## QA Complete
