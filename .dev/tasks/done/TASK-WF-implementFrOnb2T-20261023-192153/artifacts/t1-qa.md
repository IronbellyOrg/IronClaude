# T1 spec-compliance QA: "Write the deck page with all 15 slides"

Reviewer: independent per-task spec-compliance reviewer (rubric `~/.claude/skills/sc-implement-protocol/refs/qa.md`). Do not trust the implementer's report; it was not used.

Inputs checked:
- the plan's `## Constraints` and the Task 1 body (plan lines 17-52)
- the deck, `docs/onboarding/ironclaude-onboarding.html`, read in full (398 lines)
- `artifacts/t1-secret-scan.log`
- spec FR-ONB.2 (spec.md:191-207), section 2.4 (spec.md:109-121) and FR-ONB.6 (spec.md:263-270)
- this worktree's guide, `src/superclaude/core/HOW-WE-WORK.md`
- `src/superclaude/commands/` files `recommend.md`, `troubleshoot.md`, `adversarial.md`, `brainstorm.md` and `reflect.md`
- the `sc-troubleshoot-protocol/` file list
- transcript lines T57-61, T71-77, T117-129, T137-147, T157-185, T203-233, T247-267, T492-498, T567-580 and T607-615
- the titles of issues #289 and #290, read with `gh issue view`: both are OPEN; #289 is the worktree and branch protocol, #290 is how team members propose and change skills, commands and agents

Short path names below: `deck` = `docs/onboarding/ironclaude-onboarding.html`, `log` = `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153/artifacts/t1-secret-scan.log`, `guide` = `src/superclaude/core/HOW-WE-WORK.md`.

## Acceptance criteria

### T1.AC1: met

The deck has 15 `<section class="slide">` elements. Their headings are in spec order: T1.AC1@deck:146, :156, :164, :193, :202, :210, :222, :229, :242, :264, :278, :289, :306, :328, :338. Each heading matches its FR-ONB.2 slide name (spec.md:193-207) exactly.

### T1.AC2: unmet

Most statements trace correctly (see the factual check table below). Four do not:

1. **deck:177 is false.** It says "You do not choose models for this: the skill does." In fact `/sc:adversarial` takes `--agents` specs in the format `model[:persona[:"instruction"]]` (`src/superclaude/commands/adversarial.md:45`, `:61`, example at `:90`), and `/sc:brainstorm` takes `--models` (`src/superclaude/commands/brainstorm.md:56`). None of slide 3's FR-ONB.2 sources (T73-75, T205, T219) says this either.
2. **deck:214 states a rule that comes only from the transcript.** The bold, unattributed line reads: "A plan made by an `sc:` command is run by an `sc:` command."
   - Its only source is T145, and the speaker hedged it with "for the most part".
   - The Constraints say transcript lines never supply rules (plan line 23).
   - The guide states only the narrower rule, which the same bullet then repeats: `TASK-WF-*` plans run with `/sc:implement` (guide:218).
   - The guide contradicts the general version. `/sc:roadmap` output runs with `superclaude sprint run` (guide:260). `/sc:troubleshoot --fix --depth deep` and `/sc:auggie-review --depth deep` offer a task file that runs with `/task` (guide:128, :203).
   - The FR-ONB.2 content cell for slide 6 (spec.md:198) does list this sentence, which is probably why it is on the slide. The source order (code, then guide, then transcript) and the "no rules from the transcript" constraint still apply.
3. **deck:172 gives transcript-only advice as an instruction.** "If a command keeps feeling like overkill for your work, say so: that is how the skills get better" comes only from the transcript (T205) and is not attributed as a story. The closest guide rule (guide:241) is about quality checks, not about commands that feel like overkill.
4. **deck:217 has a grammar error (minor; plain-English rule NFR-ONB.5).** In "it assumes you have done your homework or tells it plainly what to plan", "tells" has the wrong subject. T139 says workflow "is going to allow you just to tell it in a prompt".

Attributions the deck gets right:
- Slide 2 gives "about 70%" as an opinion from the meeting (deck:158, T119).
- Stories use `class="story"` and "in the meeting" wording (deck:150, :168, :173, :197, :217, :234, :259, :322).

### T1.AC3: met

No statement from section 2.4 appears as it was said in the meeting:
- Nothing says `/sc:implement` makes commits (deck:243-259).
- Nothing says `/sc:pr-submit` commits your work (deck:266-273).
- Brainstorm "stops there; you decide the next step" (deck:232, guide:53).
- No plain `/research` command appears; the deck contrasts `/tech-research` with `/sc:research` (deck:233, :316).
- Nothing says the task list was retired.

Slide 5 matches guide section 1: deck:203 matches guide:9, and deck:205 matches guide:16-17 (T1.AC3@deck:203).

Slide 10 matches guide 3.11 and section 4:
- deck:266-270 match guide:200-206 (T1.AC3@deck:266).
- deck:269 matches the push rule at guide:204 and :244.
- deck:273 gives `--monitor 3` as both the setting to pass and the default (guide:206, :269), with `--monitor 2` and `--monitor 0` as the alternatives (guide:207, :244).

Advisory: slide 5's text never states the hard limit itself, which is more than 5 edits or more than one source file (guide:22). It relies on diagram D3 (deck:204), which is Task 2's job. Task 2's D3 should label that threshold, not just draw a mark.

### T1.AC4: unmet (partly)

What meets the criterion:
- Slide 12 meets FR-ONB.6. "Being worked out" appears at deck:289, :295 and :299. Issues #289 and #290 are plain links (deck:295, :299). "Ask your lead" is at deck:290. No rule is stated for either topic.
- Slide 11 uses "most under `.dev/`" and states no folder rule (T1.AC4@deck:280; guide:238).
- Slide 13 has no "stop it" instruction, and the sign of a task-builder run is told as a story (deck:322).

What does not:
- **Slide 3 goes beyond describing what the skills do.** deck:177 ("You do not choose models for this: the skill does") is a statement about model choice, and it is false (AC2, item 1).
- **Slides 13 and 6 leave out part of the guide rule.** Slide 13 (deck:321) and slide 6 (deck:215) omit the third sentence of guide:243: "This does not apply when a skill or command the user started runs them as one of its own steps." Because deck:321 says "only", the deck's rule is stricter than the guide's. A `/sc:troubleshoot --fix --depth deep` or `/roadmap` run that calls task-builder as one of its own steps would look like a violation. So the trap is not worded as the section 4 rule.

### T1.AC5: met

- Light color tokens are on `:root` (T1.AC5@deck:13-28).
- Dark tokens are set under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` (deck:29-35), and again under `:root[data-theme="dark"]` (deck:36-40).
- The body background is set explicitly (deck:43).
- The side gutter is `max(16px, env(safe-area-inset-*))` (deck:58-59, :73-74, :112-113).
- The file has no doctype, html, head or body tags; a grep for them found only `<header>`. `<title>` is at deck:7 and `<style>` at deck:12.
- The print stylesheet puts one slide per page, hides the navigation and shrinks the cheat sheet to fit (deck:121-130).
- The footer line reads "Built from HOW-WE-WORK.md at commit 070399eb", and the note after it names the uncommitted Part A changes (deck:362). 070399eb is the worktree's HEAD. The guide link is at deck:363.
- The maintenance-rule comment is at deck:1-6.

### T1.AC6: met

- The only external resource loaded is Google Fonts (T1.AC6@deck:9-11).
- The github.com links are plain `<a href>` elements (deck:295, :299, :356, :363).
- There are no `<img>` tags and no external scripts; the one script is inline (deck:366-398).

### T1.AC7: met

The log records the scan commands and their output (T1.AC7@log:2-8, log:9-14, log:16-19):
- The first, literal `sk-` grep matched only the word `task-builder`, which is a false positive (log:3-8).
- The re-run with a pattern shaped like a real key found nothing (log:17-18).
- The only hosts found are fonts.googleapis.com, fonts.gstatic.com and github.com (log:10-14).

My own scan of the deck for bare hostnames agrees: hosts appear only at deck:9-11, :295, :299, :356 and :363.

## Factual check table (claims checked beyond the findings above)

| Slide | Claim (deck line) | Source checked | Result |
|---|---|---|---|
| 1 | IronClaude is lessons learned wrapped into skills, for reliable, repeatable output (147, 150) | T569, T571 | ok (attributed at 150) |
| 1 | `superclaude install` copies the guide to `~/.claude/HOW-WE-WORK.md`; keep it open (149) | guide:3 | ok |
| 2 | Five runs give five versions, and each skips something different (157) | T221, T576; the eyebrow at 155 marks the slide as a meeting explanation | ok |
| 3 | The guide's rule list (182-185) | guide:238, :239-240, :242, :245 | ok |
| 3 | `/sc:adversarial` runs the debate; `/sc:reflect` checks finished work with several independent reviewers (177) | guide:154; reflect.md:3, :145 | ok (true of Tier 2) |
| 4 | A thin command points to the skill, and refs load only when needed (194-195) | troubleshoot.md:82; sc-troubleshoot-protocol SKILL.md:124-126, :503 | ok |
| 4 | Skills are interconnected (197) | T183, attributed | ok |
| 6 | `/sc:workflow` + `/sc:implement` is the default and the other pair is rare, for level 4 (211); `TASK-WF-*` plans run with `/sc:implement` (214) | guide:258, :218 | ok |
| 7 | Brainstorm only if the idea is vague; research only if needed (223) | guide:51, :95 | ok |
| 8 | Brainstorm, `/tech-research` vs `/sc:research`, `/sc:recommend --plugin`, `/sc:spec-panel`, `/prd` and `/tdd` only at level 6 (232-237) | guide:53, :262, :155, :20, section 3.2; recommend.md:19, :24 | ok |
| 9 | Read the plan, the run path, the retry ladder, resuming, and the three stop codes (244-258) | guide:116-119, :17 | ok |
| 11 | `superclaude update` overwrites, keeps no backup, and re-copies skill folders (281) | guide:3 | ok |
| 11 | `/ccsession-tag` and `ccsession`; re-run on the work's files; `/sc:save` and `/sc:load` do not resume (282-283) | guide:213, :215-220 | ok |
| 13 | The seven look-alike command pairs (311-317) | guide:257-263 | ok |
| 14 | `/sc:recommend`, `/sc:help`, ask your lead, read "your lead" as yourself if you work alone (330-332) | guide:246, :249, :288 | ok |
| 15 | The ten cheat-sheet rows and their section numbers (343-352) | guide section 1 rows, sections 3.1-3.13 | ok |

## extra_scope

None that matters:
- Home/End keys (deck:383-384) and the IntersectionObserver that keeps the counter in sync (deck:386-396) belong to the navigation script the task asked for.
- The `claude:viewport-fit-sides` meta tag (deck:8) is part of the artifact page contract.
- The comment's mention of the Task 3 test (deck:5) is a note, not behavior.

## misunderstood

None.

## Advisories (not counted in the verdict)

- Slide 15 gives guide section numbers plus one link to the guide (deck:356). Spec.md:207 asks for "a link to the guide section"; a link on each row would follow it more literally.
- Printing from a dark system theme: the print CSS sets the body to #fff/#000 (deck:122), but `.story` text (`--muted`), `.term b` and links (`--accent`) keep their dark-theme light colors on white paper. Task 4's print check should look at this.
- Slide 5's hard limit depends on D3 (see T1.AC3).

## Fixes required (one fix pass)

1. deck:177: remove or correct "You do not choose models for this: the skill does." Describe only what the skills do.
2. deck:214: replace the general bold rule with the guide's rule (guide:218), or present it as an attributed rule of thumb from the meeting rather than a rule.
3. deck:172: attribute the "say so" advice as a meeting story, or tie it to the wording of guide:241.
4. deck:321 and deck:215: add the exception from guide:243, that the rule does not apply when a skill or command the user started runs them as one of its own steps.
5. deck:217: fix the grammar, for example "...or lets you tell it plainly what to plan".

VERDICT: missing
