# Check (f) — Naming-Convention Translation Review

**Verdict:** PASS
**Date:** 2026-05-27

## Grep 1: search for `tier2-h<N>` spec shorthand

Command: `grep -nE 'tier2-h[0-9N<]' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

**Output:** *(empty — no matches anywhere in the file)*

Inside the new subsection (L266-L277): **ZERO** `tier2-h<N>` remnants. ✓

## Grep 2: search for the actual `tier2-<agent-name>-*.md` / `tier2-*-*.md` naming

Command: `grep -nE 'tier2-(<agent-name>|\*)-(hypothesis|calibration)\.md' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

**Matches found:**

| Line | In new subsection (L266-L277)? | Context |
|------|------------------------------|---------|
| 259 | no — Wave 3 Step 2 (pre-existing) | `tier2-<agent-name>-hypothesis.md` (the hypothesis-card output path) |
| 263 | no — Wave 3 Step 3.5 (pre-existing) | `tier2-<agent-name>-calibration.md` (the calibration sibling) |
| 270 | **yes** | `tier2-<agent-name>-hypothesis.md` ↔ `tier2-<agent-name>-calibration.md` (translated naming in the first gate bullet) |
| 276 | **yes** | `tier2-*-hypothesis.md` (verification-command iteration) ↔ `*-calibration.md` (verification-command assertion) |

## Scoping confirmation

The naming check is scoped to lines inside the new gate subsection (L266-L277). Within that range:
- ZERO `tier2-h<N>` matches → required ✓
- TWO lines (L270, L276) with the translated `tier2-<agent-name>-*.md` / `tier2-*-*.md` forms → required ✓

The pre-existing references at L259 and L263 (outside the new subsection but using the same actual naming convention) are consistent with the translation — the new subsection's naming MATCHES the surrounding skill's established convention.

## Conclusion

PASS — spec's illustrative `tier2-h<N>-*.md` shorthand has been fully translated to the actual `tier2-<agent-name>-*.md` / `tier2-*-*.md` naming used throughout Wave 3. Zero remnants of the spec shorthand inside the new subsection.
