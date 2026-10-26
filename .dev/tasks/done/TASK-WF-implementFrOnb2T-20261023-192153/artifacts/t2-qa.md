# T2 spec-compliance QA: "Draw the six diagrams as inline SVG"

Reviewer: per-task spec-compliance reviewer (rubric `~/.claude/skills/sc-implement-protocol/refs/qa.md`). Do not trust the implementer's report: every finding below was re-derived from the file, the diff and the sources, not from `t2-checks.log`.

Deck file: `docs/onboarding/ironclaude-onboarding.html` (abbreviated `deck` below; 632 lines).

## Diff scope (verified)

- `git diff --no-index` of the pre-T2 snapshot (`6e0d111e…:docs/onboarding/ironclaude-onboarding.html`) against the current deck: 234 insertions, 6 deletions. The six deletions are the `<!-- Dn diagram (Task 2) -->` placeholder comments. Hunks: deck:110-130 (diagram CSS), deck:153-154 (two print rules), deck:187-227 (D1), deck:264-304 (D2), deck:313-333 (D3), deck:341-377 (D4), deck:389-424 (D5), deck:472-506 (D6).
- The guide and routing surfaces are byte-identical to the snapshot (`HOW-WE-WORK.md`, core `CLAUDE.md`, `CHANGELOG.md`, `prompts.py`, the plugin `HOW-WE-WORK.md` copy, `test_how_we_work_routing_table.py`). The plan constraint at plan:20 holds.

## Acceptance criteria

### T2.AC1: met
Six inline `<svg>` elements, one per required slide, each with a `<title>`; no external image files.
- Slide 2 (s2, deck:182): `<svg>` at deck:188, `<title>` at deck:189.
- Slide 4 (s4, deck:259): deck:265 / deck:266.
- Slide 5 (s5, deck:308): deck:314 / deck:315.
- Slide 6 (s6, deck:337): deck:342 / deck:343.
- Slide 7 (s7, deck:385): deck:390 / deck:391.
- Slide 10 (s10, deck:462): deck:473 / deck:474.
- Each also has a `viewBox` and a `<desc>` (deck:190, 267, 316, 344, 392, 475), as plan:58 asks. Each sits in a `figure.diagram` with `overflow-x: auto` (deck:110) and `width: 100%` (deck:111). A grep for `<img`, `.png`, `.jpg` and `.svg"` finds nothing.

### T2.AC2: met
No literal color in any SVG.
- An awk scan of every `<svg>…</svg>` block for `fill=`, `stroke=`, `style=`, `color`, hex, `rgb` and `hsl` finds nothing (rc=1). Every shape and text element is styled through a `d-*` class only (16 class names, all listed in deck:115-130).
- Every `.d-*` rule uses `var(--token)` only: deck:115-130 (`--surface-2`, `--line`, `--accent-soft`, `--accent`, `--warn-soft`, `--warn`, `--fg`, `--muted`, `--font-*`). Arrow heads use `.d-head` / `.d-head-acc` (deck:123-124).
- The tokens are redefined for both themes (deck:29-40, from T1). The hex values in the print block (deck:144-148) are T1's, not T2's.

### T2.AC3: UNMET (D6)
The commands and step labels in D2 to D5 trace to their sources. One D6 step label states a rule that the guide does not contain:

- **deck:495, D6 box "Merge, when your lead approves".** `HOW-WE-WORK.md` has no rule on merging a PR or on who approves a merge. Its only approval rules cover the push (HOW-WE-WORK.md:206, :244) and the spec (HOW-WE-WORK.md:98). The transcript does not support the label either: lines 275-277 have a partner review and merge, and line 343 says not to merge until "at least two agents" say the PR is good. "Merge" is a spec-mandated D6 step (spec.md:229), but the qualifier "when your lead approves" is a new approval rule written as a guide step. This breaks the AC ("every … step label in … D6 appears in HOW-WE-WORK.md") and plan:28 (the deck does not copy "step lists, flags or paths the guide does not state").
- Accepted as sourced, not counted as failures:
  - D6 "next round: bot reviews again (capped rounds)" (deck:492-493). Spec D6 requires "re-review" (spec.md:229), and the brief points to `src/superclaude/commands/pr-submit.md` for it: `--max-rounds` default 2, hard cap 5 (pr-submit.md:48).
  - D1 contains no command or flag (deck:195-224). This matches `t2-checks.log` "s2 []".

### T2.AC4: met
- D1: five-runs fan-out (deck:196-210) beside two agents → Debate → "Best parts merged" (deck:211-224).
- D2: four layers. Command (deck:272-274), skill (deck:276-278), "Refs, on demand" with `report-template.md` drawn inside refs (deck:281-285), agents (deck:286-290). Four skill-to-skill arrows (deck:291-299).
- D3: dashed hard-limit line and label between level 3 (deck:323-324) and level 2 (deck:327-328), at deck:325-326.
- D4: "DEFAULT · level 3" over `/sc:workflow` → `/sc:implement` (deck:349-361), and "RARE · level 4 only" over `/task-builder` → `/task` (deck:362-374). Each pair shows what it leaves on disk.
- D5: both track bands (deck:396-399) over the seven guide steps (deck:400-419).
- D6: `--monitor 3` (deck:481), `--monitor 2` "makes the fixes locally; stops before pushing" (deck:498-499), `--monitor 0` "only opens the PR" (deck:501-503).

## extra_scope

1. **deck:300-301, D2 "Change one skill and every skill that calls it has to be checked again."** This is an unattributed rule inside the diagram. Its only source is the transcript (line 183: "before you go and start modifying anything, just know that…"), and the transcript may supply explanations only, never rules (plan:23). Slide 4 already carries this point as an attributed story (deck:305), so the diagram restates it as a rule nobody asked for. Fix: drop it, or reword it as a non-imperative fact ("Skills are interconnected: one skill is often used by several others").
2. Minor, not counted: D2 adds line counts "(214 lines)" and "(711 lines)" (deck:273, :277). Both are correct (`wc -l`: troubleshoot.md 214, SKILL.md 711) and harmless.

## misunderstood

None. Note only: `.diagram.wide svg { min-width: 720px }` and `.diagram.mid svg { min-width: 540px }` (deck:112-113) make D1 to D6 scroll inside their own container at 375 px instead of shrinking. The page still does not widen (deck:110), which meets plan:58 "never widens the page". Whether the result is "readable at 375 px" (spec.md:235) is Task 4's render check, not this review.

## Per-diagram label check

Sources: guide = `src/superclaude/core/HOW-WE-WORK.md`; TS = `src/superclaude/commands/troubleshoot.md`; T = transcript `ib-ai-onboarding-pt2-transcript-2026-10-22.txt`.

| Diagram | Label (deck line) | Source | Result |
|---|---|---|---|
| D1 | "One prompt", "Version A-E", "Five different answers; each misses something different" (197-210) | T:221 "five different versions", T:119 "ignored 30% of your instructions" | ok (explanation, no command) |
| D1 | "Two agents, then a debate", "Debate", "Best parts merged" (211-222) | T:221-223 two agents → adversarial debate → "take any value from the loser" | ok |
| D1 | "Cheaper than five runs; the compare step catches what one run missed." (224) | T:221 five agents "way too expensive" | ok |
| D2 | `/sc:troubleshoot` (274), `sc-troubleshoot-protocol` (278) | TS:82 (`Skill sc:troubleshoot-protocol`); skill folder exists | ok |
| D2 | `triage-checklist.md`, `escalation-rubric.md`, `report-template.md` (283-285) | `sc-troubleshoot-protocol/refs/` listing | ok; templates drawn as ref files per plan:26 |
| D2 | `root-cause-analyst`, `confidence-calibrator`, `evidence-validator` (288-290) | TS:99 | ok |
| D2 | `sc:adversarial-protocol`, `sc:workflow-protocol`, `task-builder`, `/sc:reflect` (296-299) | TS:100 | ok |
| D2 | "Change one skill and every skill that calls it has to be checked again." (300-301) | T:183 only; not in the guide | **FAIL**: transcript turned into an unattributed rule (extra_scope 1) |
| D3 | Levels 1-6 names (318-330) | guide:15-20 | ok ("(rare)"/"(default)" per plan:63-64 and guide:17, :262) |
| D3 | `/prd → /tdd → /roadmap`, `/tech-research`, `/task-builder → /task`, `/sc:workflow → /sc:implement`, `/sc:task, or a plain edit`, `ask, or /sc:explain` | guide:15-20 | ok |
| D3 | "Hard limit: more than 5 edits, or more than one source file, needs a written plan" (326) | guide:22 | ok, same strength. The test-file carve-out and the `/sc:cleanup`/`/sc:improve` exception are left out of the label but stated in full beside it (deck:312) |
| D4 | "DEFAULT · level 3"; plan with acceptance criteria per step at `.dev/tasks/to-do/<id>/<id>.md` (349-354) | guide:17, :262 | ok |
| D4 | "progress.md: one line per step; a reviewer checks each step, then a final review; folder moves to done/" (359-361) | guide:17, :273 | ok. The non-Linux archive refusal is left out; that does not loosen a rule |
| D4 | "RARE · level 4 only" (362) | guide:262 "only for level-4 work", guide:224 | ok |
| D4 | `/task-builder` "researches the code and writes a task file: a checklist in .dev/tasks/to-do/" (366-367) | guide:18 | ok |
| D4 | `/task` "reviewer panel after each phase but setup; then tests and a final audit. Takes much longer, costs far more." (372-374) | guide:18, :224 | ok |
| D5 | Shape idea `/sc:brainstorm` "only if vague" (401) | guide:51-52 | ok |
| D5 | Research `/tech-research` "if you need to" (403) | guide:95-96 | ok |
| D5 | Spec "write it; your lead approves it" (405) | guide:98 | ok |
| D5 | Plan `/sc:workflow`, Implement `/sc:implement` (407-409) | guide:101-106 | ok |
| D5 | Review `/code-review`, `/sc:auggie-review` (411); Open PR `/sc:pr-submit` (413) | guide:200-205 | ok. The security review and the push-after-approval step are left out; no rule is restated |
| D5 | Level 6 path `/prd, /tdd, /roadmap, /task per phase` (420) | guide:20, :80 | ok |
| D5 | Level-4 swap to `/task-builder` and `/task` (421) | guide:108 | ok |
| D5 | Bands "Spec track (Gundy, Philippe)", "Execution track (William, Leandro)" (397-399) | spec.md:83, :200-201 | ok (band titles are excepted by the AC) |
| D6 | `/sc:pr-submit --monitor 3` (481) | guide:206, :269 | ok |
| D6 | "PR open; review bot posts findings" (484) | guide:207 | ok |
| D6 | "Checks each finding; fixes Medium+ and CI" (487) | guide:207 | ok |
| D6 | "Pushes the fixes; resolves comments" (490) | guide:207, :244 | ok |
| D6 | "next round: bot reviews again (capped rounds)" (492-493) | spec.md:229 "re-review"; pr-submit.md:48 | ok (source the brief allows) |
| D6 | **"Merge, when your lead approves" (495)** | none in the guide; T:275-277, :343 describe a different merge practice | **FAIL**: T2.AC3; adds a merge-approval rule the guide does not state |
| D6 | `--monitor 2` "makes the fixes locally; stops before pushing" (498-499) | guide:207, :244 | ok |
| D6 | `--monitor 0` "only opens the PR: no review app, or not sure it is installed" (501-503) | guide:207, :269 | ok |

## Fix needed (one fix pass)

1. deck:495: change "Merge, when your lead approves" to a step label that states no approval rule (for example "Merge"), or to wording the guide states.
2. deck:300-301: remove the D2 imperative sentence, or reword it as a non-imperative fact.

VERDICT: missing
