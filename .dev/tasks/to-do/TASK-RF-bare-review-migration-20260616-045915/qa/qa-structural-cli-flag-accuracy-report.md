# QA Report — Synthesis Gate (CLI-flag-accuracy lens)

**Topic:** sc-bare-review SKILL.md migration to `superclaude swarm run --lens bare-review`
**Date:** 2026-06-16
**Phase:** synthesis-gate (structural / CLI-flag accuracy)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Lens:** CLI-flag accuracy — every `swarm run --lens bare-review` flag the SKILL.md names must exist on the post-WS-0 `run_cmd` Click option set, with correct names and defaults.

---

## Overall Verdict: PASS

All 8 flags the SKILL.md documents exist verbatim on the post-WS-0 `run_cmd` Click option set in
`src/superclaude/cli/swarm/commands.py`. No fabricated flags. All three documented defaults
(reviewers 2-4 default 3, target-line-cap 4000, timeout-sec 180) match the code — confirmed against
both the option help strings and the authoritative `bare-review` lens registry entry.

The adversarial hypothesis ("assume ≥5 fabricated/wrong flags") is REJECTED on evidence: zero
fabricated flags found across 8 checks.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `--target` exists on run_cmd | PASS | `commands.py:1351` `@click.option("--target", "target_path", ...)`. SKILL.md L29 names `--target <path>` (REQUIRED). Match. |
| 2 | `--output` exists on run_cmd | PASS | `commands.py:1361` `@click.option("--output", "output_dir", ...)`. SKILL.md L29 names `--output <dir>` (REQUIRED). Match. |
| 3 | `--reviewers` exists + range 2-4 default 3 | PASS | `commands.py:1385` `@click.option("--reviewers", "reviewers", type=int, ...)`; help L1392 states inclusive range `[2, 4]`, L1393-1394 "lens default (3 for bare-review)". Lens default `default_workers=3` at `bare_review.py:61`. SKILL.md L29-30 "`--reviewers <N>` (2-4, default 3)". Match. |
| 4 | `--target-line-cap` exists + default 4000 | PASS | `commands.py:1398` `@click.option("--target-line-cap", "target_line_cap", type=int, ...)`; help L1405 "default 4000", L1406 "lens default (4000 for bare-review)". Lens `default_target_line_cap=4000` at `bare_review.py:62`. SKILL.md L30 "`--target-line-cap <N>` (default 4000)". Match. |
| 5 | `--timeout-sec` exists + default 180 | PASS | `commands.py:1410` `@click.option("--timeout-sec", "timeout_sec", type=int, ...)`; help L1417 "default 180", L1418 "the 180s default is preserved". Lens spec sets `timeout_sec: 180` at `commands.py:789` (`_build_spec_from_lens`). SKILL.md L31 "`--timeout-sec <N>` (default 180)". Match. |
| 6 | `--label` exists on run_cmd | PASS | `commands.py:1422` `@click.option("--label", "label", type=str, ...)`. SKILL.md L31 names `--label <str>`. Match. |
| 7 | `--transport` exists + choices openai_compat/stub | PASS | `commands.py:1373` `@click.option("--transport", "transport_kind", type=click.Choice(list(_TRANSPORT_KINDS)), ...)`; `_TRANSPORT_KINDS = ("openai_compat", "stub")` at `commands.py:489`. SKILL.md L32/L37 use `--transport openai_compat` and `--transport stub`. Match. |
| 8 | `--lens` exists on run_cmd | PASS | `commands.py:1317` `@click.option("--lens", "lens", type=str, ...)`. SKILL.md L29/L35 use `--lens bare-review`. Match. The `bare-review` lens is a registered entry (`bare_review.py:41` `name="bare-review"`). Match. |

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found

None. No fabricated flag, no wrong flag name, no wrong default detected.

## Cross-check notes (defaults source-of-truth)

The SKILL.md documents three defaults as flowing from the lens, not from hardcoded option defaults
(every run_cmd override option is `default=None`, meaning "preserve lens default when omitted"). I
verified the defaults at their real source — the `bare-review` `LensEntry`:

- `src/superclaude/cli/swarm/lenses/bare_review.py:61` → `default_workers=3` (reviewers default 3) ✓
- `src/superclaude/cli/swarm/lenses/bare_review.py:62` → `default_target_line_cap=4000` ✓
- `src/superclaude/cli/swarm/commands.py:789` (`_build_spec_from_lens`) → `"timeout_sec": 180` ✓

The reviewers `[2,4]` bound the SKILL.md states is enforced in the `--reviewers` help text
(`commands.py:1392`) and matches AC-1.4 framing. This is consistent.

## Out-of-scope observations (NOT flag-accuracy failures; documented for completeness)

- run_cmd carries additional flags the SKILL.md does not document: `--stdin` (L1310), `--resume`
  (L1332), `--force-relens` (L1434), `--detached` (L1452), `--auto-inject-guard` (L1470). The
  CLI-flag-accuracy lens checks that documented flags EXIST and are correct (no fabrication); it
  does not require the thin-caller SKILL.md to enumerate every run_cmd flag. Omitting
  resume/detached/stdin from a delegate-only bare-review caller doc is intentional scoping, not an
  accuracy defect. No finding raised.

## Confidence Gate

- Item 1 `--target`: [x] VERIFIED (Read commands.py:1351)
- Item 2 `--output`: [x] VERIFIED (Read commands.py:1361)
- Item 3 `--reviewers`: [x] VERIFIED (Read commands.py:1385 + Grep bare_review.py:61)
- Item 4 `--target-line-cap`: [x] VERIFIED (Read commands.py:1398 + Grep bare_review.py:62)
- Item 5 `--timeout-sec`: [x] VERIFIED (Read commands.py:1410 + Read commands.py:789)
- Item 6 `--label`: [x] VERIFIED (Read commands.py:1422)
- Item 7 `--transport`: [x] VERIFIED (Read commands.py:1373 + commands.py:489)
- Item 8 `--lens`: [x] VERIFIED (Read commands.py:1317 + Grep bare_review.py:41)

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 2 | Glob: 0 | Bash: 2

No web research performed (all claims are intrinsically local — CLI source vs SKILL.md).
Tool-call total (7) is below the 8 documented checks only because two flag pairs share a single
Read page (the run_cmd decorator block, commands.py:1299-1528, covers items 1,2,3,4,5,6,7,8 in one
Read) and the lens-default Grep covers items 3 and 4 jointly. Each check maps to a specific line
anchor cited above — no padding.

## QA Complete
