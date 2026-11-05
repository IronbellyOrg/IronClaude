# T1 spec-compliance re-QA (after the one fix pass): "Write the deck page with all 15 slides"

Reviewer: independent per-task spec-compliance reviewer (rubric `~/.claude/skills/sc-implement-protocol/refs/qa.md`). Do not trust the implementer's report: the fix summary was used only to locate edits. All seven ACs were re-checked against the current files.

## Inputs re-read

- The current deck, `docs/onboarding/ironclaude-onboarding.html`, read in full (404 lines).
- `artifacts/t1-secret-scan.log`, read in full (23 lines, including the appended re-scan at lines 21-23).
- My own re-run, on the current deck, of the tag, heading, key-string and hostname checks.
- Sources: the same as `t1-qa.md`, namely the plan's Constraints and Task 1; spec.md:109-121, :191-207 and :263-270; the worktree guide `src/superclaude/core/HOW-WE-WORK.md`; and the transcript lines cited by FR-ONB.2.

Short names used below:
- `deck` = `docs/onboarding/ironclaude-onboarding.html`
- `log` = `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153/artifacts/t1-secret-scan.log`
- `guide` = `src/superclaude/core/HOW-WE-WORK.md`

## Status of the five first-QA fixes

| # | First-QA finding | Current deck | Result |
|---|---|---|---|
| 1 | Slide 3 said "You do not choose models for this: the skill does", which is false given adversarial.md:45 and brainstorm.md:56. | The sentence is gone. deck:182 now only describes what the skills do ("often on different models"), which the Constraints allow (plan line 27). | fixed |
| 2 | Slide 6 stated "sc: plan run by sc: command" as a rule, sourced only from the transcript. | deck:220 now states the guide rule: TASK-WF-* plans run with `/sc:implement` (guide:218), and a task file runs with `/task` (guide:17, :230). The general version is now an attributed meeting "rule of thumb" in a story (deck:223, from T145). | fixed (see advisory A1) |
| 3 | Slide 3's "say so" was an unattributed instruction. | It is now an attributed story at deck:178 (T205: "if we are finding consistently that they are almost always overkill, then our goal is to make better skills"). It states no contributing rule. | fixed |
| 4 | The guide:243 exception was missing on slides 6 and 13. | deck:327 now quotes all three sentences of guide:243. deck:221 carries the exception and points to slide 13. | fixed |
| 5 | Slide 6 grammar. | deck:223: "It assumes you have done your homework, or lets you tell it plainly in a prompt what to plan." This matches T139. | fixed |

## Acceptance criteria

### T1.AC1: met

The deck has 15 slide sections and 15 `<h2>` headings, in the spec's order:

T1.AC1@deck:151, :161, :169, :198, :207, :216, :228, :235, :248, :270, :284, :295, :312, :334, :344

Each heading matches its FR-ONB.2 slide name (spec.md:193-207) exactly.

### T1.AC2: unmet

The hard-limit sentence added to slide 5 in the fix pass is incomplete in a way that makes it false. deck:209 reads: "if the work needs more than 5 edits or touches more than one source file ..., it must go through a written plan". It stops there.

The guide's hard limit continues: "The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (section 3.7 of the routing guide): commit first and review `git diff` afterwards" (guide:22; procedure at guide:165-168).

Without that sentence, the deck says a folder-wide `/sc:cleanup` or `/sc:improve` run must go through a written plan. The guide says the opposite. This is the same kind of problem as first-QA finding 4: an exception was dropped, so the rule reads stricter than the guide.

Every other factual statement traces to its listed source; the full table is in `t1-qa.md`, and I re-checked it against the current line numbers. Transcript-sourced statements are attributed:
- slide 2's "about 70%" is given as the meeting's opinion (deck:163, T119)
- the stories are at deck:155, :173, :178, :202, :223, :240, :265 and :328

### T1.AC3: unmet (slide 5's hard limit does not match guide section 1)

Slide 5:
- deck:208 matches guide:9.
- deck:211 matches guide:16-17.
- deck:209 does not fully match guide:22, because the exception is missing (see T1.AC2).

Slide 10 matches guide 3.11 and section 4:
- T1.AC3@deck:272-276 match guide:200-206.
- The push rule at deck:275 and deck:279 matches guide:204 and :244.
- deck:279 gives `--monitor 3` as the setting to pass and the default (guide:206, :269), and gives `--monitor 2` and `--monitor 0` as the alternatives (guide:207, :244).

No section 2.4 statement appears as it was said in the meeting:
- Nothing says `/sc:implement` makes commits (deck:249-265).
- Nothing says `/sc:pr-submit` commits your work (deck:272-279).
- Brainstorm "stops there" (deck:238, guide:53).
- No plain `/research` command appears (deck:239, :322).
- Nothing says the task list was retired.

### T1.AC4: met

- Slide 12 meets FR-ONB.6:
  - "being worked out" appears at deck:295, :301 and :305.
  - Issues #289 and #290 are plain links (deck:301, :305); both issues are open, and their titles match their topics.
  - "ask your lead" is at deck:296.
  - No rule is stated for either topic (T1.AC4@deck:296-306).
- Slide 3 describes model diversity only as what the skills do and names no model to use (deck:182).
- Slide 11 uses "most under `.dev/`" and states no folder rule (deck:286, guide:238).
- Slide 13 words the trap as the guide section 4 rule, all three sentences (deck:327 = guide:243). The "many subagents" sign is a story (deck:328). A grep for "stop it", "kill it" and "interrupt it" finds nothing.
- A grep for worktree, contributing and model wording finds no rule on worktrees, contributing, artifact folders or model choice on any other slide. The hits are deck:163, :182 and :252 (descriptive) and deck:299-305 (slide 12).

### T1.AC5: met

- Light tokens on `:root` (T1.AC5@deck:13-28).
- Dark tokens under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` (deck:29-35), and again under `:root[data-theme="dark"]` (deck:36-40).
- Explicit body background (deck:43).
- Gutter `max(16px, env(safe-area-inset-*))` (deck:58-59, :73-74, :112-113).
- No doctype, html, head or body tag. The grep finds only `<header>` at deck:138. `<title>` is at deck:7 and `<style>` at deck:12.
- Print CSS (deck:121-135):
  - It forces light tokens for all three theme states (deck:122-126). The selector specificities are equal to the screen rules, and the print block comes later in the file, so it wins.
  - One slide per page (deck:130-131).
  - The navigation is hidden (deck:128).
  - The cheat sheet is compacted (deck:132-133).
- Footer: "Built from HOW-WE-WORK.md at commit 070399eb", plus the note naming the uncommitted Part A changes (deck:368). The guide link is at deck:369.
- Maintenance-rule comment (deck:1-6).

### T1.AC6: met

- Only Google Fonts is loaded (T1.AC6@deck:9-11).
- The github.com links are plain anchors (deck:301, :305, :362, :369).
- There are no `<img>` tags and no external `<script src>`. The only script is inline (deck:372-404).

### T1.AC7: met

- The log records the key-string and host commands and their output (T1.AC7@log:2-14, log:16-19). The appended re-scan for the fixed deck is at log:21-23.
- The appended block records only results, not the command lines. The earlier commands at log:9 and log:17 are the ones it repeats.
- My own re-run on the current deck agrees:
  - The key-shaped pattern finds no match.
  - The only hostnames are fonts.googleapis.com (deck:9, :11), fonts.gstatic.com (deck:10) and github.com (deck:301, :305, :362, :369).

## extra_scope

None that matters:
- The print token override (deck:122-126) supports the print requirement of NFR-ONB.4.
- The Home/End keys and the IntersectionObserver counter (deck:389-401) are part of the requested navigation.

## misunderstood

None.

## Factual errors found

| Slide | Claim | Source | Problem |
|---|---|---|---|
| 5 | "if the work needs more than 5 edits or touches more than one source file ..., it must go through a written plan" (deck:209) | guide:22, :165-168 | It leaves out the guide's one exception: `/sc:cleanup` and `/sc:improve` run on a folder (commit first, review `git diff`). As written, the slide contradicts guide 3.7. |

## Advisories (not counted in the verdict)

- **A1. deck:223.** The meeting's rule of thumb ("a plan made by an `sc:` command is followed up by an `sc:` command") is now correctly attributed, and the guide's own rule comes first (deck:220). It still has exceptions in the guide:
  - `/sc:roadmap` work ends with `superclaude sprint run` (guide:260).
  - `/sc:troubleshoot --fix --depth deep` and `/sc:auggie-review --depth deep` offer a task file that runs with `/task` (guide:128, :203).
  The authority line (deck:156) covers this, but the Task 5 reviewer may raise it.
- **A2. Slide 15.** It gives section numbers plus one guide link (deck:362), where spec.md:207 says "a link to the guide section".
- **A3. log:21-23.** The re-scan block should repeat the exact commands it ran, so the log stands on its own.

## Fix needed

Add the guide's exception after the hard-limit sentence at deck:209. For example: "The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (guide 3.7): commit first and review `git diff` afterwards."

Both command names are already in the guide, so the Task 3 claim test still passes.

## Halt status

This is the single re-QA that qa.md allows. The verdict is still not `compliant`, so the halt table applies: `E-HALT-QA`. Next steps are `fix`, `ruling` or `resume`. The one-sentence fix above would resolve the only unmet item.

VERDICT: missing
