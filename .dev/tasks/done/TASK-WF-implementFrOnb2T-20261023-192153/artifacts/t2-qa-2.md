# T2 spec-compliance re-QA (after the one fix pass): "Draw the six diagrams as inline SVG"

Reviewer: the same per-task spec-compliance reviewer as `t2-qa.md` (rubric `~/.claude/skills/sc-implement-protocol/refs/qa.md`). Do not trust the implementer's report: this review re-read all six figures (deck:187-506), the diagram CSS (deck:110-130) and the print rules (deck:153-154) in the current file, re-ran the diff and scans, and re-checked all four ACs, not only the two fixed lines.

Deck file: `docs/onboarding/ironclaude-onboarding.html` (abbreviated `deck` below; still 632 lines).

## Diff scope (re-verified)

- `git diff --no-index` of the pre-T2 snapshot (`6e0d111e…`) against the current deck: 234 insertions, 6 deletions. These are the same hunks as the first QA (deck:110-130, 153-154, 187-227, 264-304, 313-333, 341-377, 389-424, 472-506). The six deletions are the `<!-- Dn diagram (Task 2) -->` placeholders.
- The fix pass changed only deck:300-301 (D2 note) and deck:495 (D6 box). Every other line of the six figures reads exactly as in the first QA.
- `HOW-WE-WORK.md`, core `CLAUDE.md`, `CHANGELOG.md` and `prompts.py` are still byte-identical to the snapshot (plan:20 holds).

## Acceptance criteria

### T2.AC1: met
- One `<svg>` with a `<title>` on each required slide:
  - s2 (deck:182): svg deck:188, title deck:189.
  - s4 (deck:259): deck:265 / :266.
  - s5 (deck:308): deck:314 / :315.
  - s6 (deck:337): deck:342 / :343.
  - s7 (deck:385): deck:390 / :391.
  - s10 (deck:462): deck:473 / :474.
- Each SVG also has a `viewBox` and a `<desc>` (deck:190, 267, 316, 344, 392, 475).
- Each sits in a `figure.diagram` with `overflow-x: auto` (deck:110) and `width: 100%` (deck:111).
- A grep for `<img`, `.png`, `.jpg` and `.svg"` finds nothing (rc=1).

### T2.AC2: met
- Re-scanning every `<svg>…</svg>` block for `fill=`, `stroke=`, `style=`, `color`, hex, `rgb` and `hsl` finds nothing (rc=1).
- All styling goes through `.d-*` classes, and every `.d-*` rule uses `var(--token)` only (deck:115-130). The two new D2 text lines (deck:300-301) and the D6 "Merge" text (deck:495) use the `d-ts` and `d-tb` classes (deck:126, :128).

### T2.AC3: met
- **D6 (fixed):** deck:495 now reads `Merge`, with no approval qualifier. "Merge" is the step that spec D6 requires (spec.md:229), and it no longer states any approval rule, so it no longer conflicts with the guide's approval rules (HOW-WE-WORK.md:206, :244).
- The other D6 labels trace to HOW-WE-WORK.md:206-207 and :244, :269:
  - `/sc:pr-submit --monitor 3` (deck:481)
  - "PR open; review bot posts findings" (deck:484)
  - "Checks each finding; fixes Medium+ and CI" (deck:487)
  - "Pushes the fixes; resolves comments" (deck:490)
  - `--monitor 2` and `--monitor 0` (deck:498-503)
- "next round: bot reviews again (capped rounds)" (deck:492-493) is the spec's "re-review" step (spec.md:229), sourced from pr-submit.md:48 as the brief allows.
- D3 labels (deck:318-330) trace to HOW-WE-WORK.md:15-22.
- D4 labels (deck:349-374) trace to HOW-WE-WORK.md:17-18, :224, :262.
- D5 labels (deck:401-421) trace to HOW-WE-WORK.md:20, :51-52, :80, :95-108, :200-206. The band titles (deck:397-399) are excepted by the AC and come from spec.md:83 and :200-201.
- D2 names (deck:274-299) trace to `troubleshoot.md`:
  - `sc-troubleshoot-protocol`: troubleshoot.md:82.
  - The three agents: troubleshoot.md:99.
  - The four called skills: troubleshoot.md:100.
  - The three ref files: they exist in `sc-troubleshoot-protocol/refs/`.
  - The line counts 214 and 711 match `wc -l`.
- D1 (deck:195-224) contains no command or flag.

### T2.AC4: met
- D1: the five-runs fan-out (deck:196-210) sits beside two agents → Debate → "Best parts merged" (deck:211-224).
- D2: four layers.
  - Command: deck:272-274.
  - Skill: deck:276-278.
  - Refs, with `report-template.md` drawn inside refs: deck:281-285.
  - Agents: deck:286-290.
  - Skill-to-skill arrows: deck:291-299.
- D3: the hard limit is marked between levels 3 and 2 (deck:325-326).
- D4: the DEFAULT pair is at deck:349-361 and the RARE level-4 pair is at deck:362-374.
- D5: both track bands (deck:396-399) are drawn over the seven guide steps (deck:400-419).
- D6: `--monitor 3`, `2` and `0` are at deck:481, :498 and :501.

## extra_scope

None.
- The earlier D2 finding is resolved. deck:300-301 now reads "Skills are interconnected: one skill is often used by several others." That is a non-imperative fact, matching transcript line 183 ("most of these skills are all interconnected and they're all using each other") and the attributed story at deck:305. It states no rule and names no command, so plan:23 is satisfied.
- The D2 line counts (deck:273, :277) are correct and harmless, as noted before.

## misunderstood

None. The note from the first QA still applies: the `min-width` rules (deck:112-113) make the diagrams scroll inside their own container at 375 px instead of shrinking, and the page never widens (deck:110). Readability at 375 px is left to Task 4's render check (spec.md:235).

## Per-diagram label check

| Diagram | Labels (deck lines) | Source | Result |
|---|---|---|---|
| D1 | fan-out and debate labels (195-224) | transcript 119, 221-223 (explanation only) | ok, no command or flag |
| D2 | `/sc:troubleshoot`, `sc-troubleshoot-protocol` (274, 278) | troubleshoot.md:82; skill folder | ok |
| D2 | `triage-checklist.md`, `escalation-rubric.md`, `report-template.md` (283-285) | `sc-troubleshoot-protocol/refs/` listing | ok |
| D2 | `root-cause-analyst`, `confidence-calibrator`, `evidence-validator` (288-290) | troubleshoot.md:99 | ok |
| D2 | `sc:adversarial-protocol`, `sc:workflow-protocol`, `task-builder`, `/sc:reflect` (296-299) | troubleshoot.md:100 | ok |
| D2 | "Skills are interconnected: one skill is often used by several others." (300-301) | transcript 183; deck:305 story | ok (fixed; a fact, not a rule) |
| D3 | levels 1-6, commands, hard limit (318-330) | HOW-WE-WORK.md:15-22 | ok |
| D4 | default pair and disk output (349-361) | HOW-WE-WORK.md:17, :262, :273 | ok |
| D4 | rare level-4 pair and disk output (362-374) | HOW-WE-WORK.md:18, :224, :262 | ok |
| D5 | seven steps and two footnotes (400-421) | HOW-WE-WORK.md:20, :51-52, :80, :95-108, :200-206 | ok |
| D5 | band titles (397-399) | spec.md:83, :200-201 | ok (excepted by the AC) |
| D6 | `--monitor 3` loop steps (481-490) | HOW-WE-WORK.md:206-207, :244, :269 | ok |
| D6 | "next round: bot reviews again (capped rounds)" (492-493) | spec.md:229; pr-submit.md:48 | ok |
| D6 | "Merge" (495) | spec.md:229 (required D6 step) | ok (fixed; no approval rule) |
| D6 | `--monitor 2`, `--monitor 0` (498-503) | HOW-WE-WORK.md:207, :269 | ok |

VERDICT: compliant
