# T1 spec-compliance QA, round 3 (resume after the E-HALT-QA fix): "Write the deck page with all 15 slides"

Reviewer: a fresh per-task spec-compliance subagent, applying the rubric in `~/.claude/skills/sc-implement-protocol/refs/qa.md`. Do not trust the implementer's report: it was not read. I formed my view from the files first, and read `t1-qa.md` and `t1-qa-2.md` only afterwards.

Short names used below:
- `deck` = `docs/onboarding/ironclaude-onboarding.html` (404 lines, read in full)
- `log` = `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153/artifacts/t1-secret-scan.log`
- `guide` = `src/superclaude/core/HOW-WE-WORK.md` (this worktree)
- `spec` = `/home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/spec.md`
- `T<n>` = line n of the transcript `ib-ai-onboarding-pt2-transcript-2026-10-22.txt`

## What I checked

- The plan's Constraints and the full Task 1 body (plan lines 17-52).
- The deck, read in full.
- spec:109-121, :187-207 and :263-270.
- The guide, read in full.
- Command files `recommend.md`, `troubleshoot.md` and `reflect.md`, and the `sc-troubleshoot-protocol/` file list.
- Transcript lines T55-259, T490-500, T565-580 and T605-616.
- The diff against the start snapshot: `git status` shows one untracked directory, `docs/onboarding/`, holding only the deck. Nothing else under `docs/` belongs to this task.
- My own re-run of the key-string and host scan on the current deck.

## Acceptance criteria

### T1.AC1: met

The deck has 15 slide sections. Their `<h2>` headings match the 15 FR-ONB.2 slide names (spec:193-207), in order.

T1.AC1@deck:151, :161, :169, :198, :207, :216, :228, :235, :248, :270, :284, :295, :312, :334, :344

### T1.AC2: unmet

Two statements restate a guide rule in a form the guide does not support. Both are listed under "Factual errors found" below:
- F1 at deck:211
- F2 at deck:279

Everything else traces to its listed source:
- **Transcript material is attributed.** Each transcript-sourced statement is an attributed story (`class="story"`, "in the meeting"): deck:155, :163, :173, :178, :202, :223, :240, :265 and :328.
- **Slide 2.** Its lead (deck:162) sits under the eyebrow "meeting explanation" (deck:160). It matches T221 and T576.
- **The 70% figure.** "About 70%" is given as the meeting's opinion, "not a measured figure" (deck:163, T119).
- **Slide 4.** The ref and progressive-disclosure terms match T171-175 and the `sc-troubleshoot-protocol/refs/` file list (deck:199-200). The thin-command claim matches troubleshoot.md:64 and :82-84.
- **Slides 8, 9, 11, 13, 14 and 15.** Their claims match guide:53, :119, :155, :213-220, :243, :246, :249, :257-263 and :288, and recommend.md:19 and :24.

### T1.AC3: unmet

No section 2.4 statement appears as it was said in the meeting:
- Nothing says `/sc:implement` makes commits (deck:249-265).
- Nothing says `/sc:pr-submit` commits your work (deck:272-279).
- Brainstorm "stops there; you decide the next step" (deck:238, guide:53).
- No plain `/research` command appears; the deck contrasts `/tech-research` with `/sc:research` (deck:239, :322).
- Nothing says the task list was retired.

Parts of slides 5 and 10 match the guide:
- The tie-break sentence matches (deck:208 = guide:9).
- The hard limit now carries its exception (T1.AC3@deck:209 = guide:22).
- The slide 10 steps and push rule match (deck:272-276 = guide:200-206, :244).
- `--monitor 3` is stated as the setting to pass, and the default (deck:276, :279 = guide:206, :269).

Two parts do not match the guide as it reads in this worktree:
- **Slide 5, deck:211:** "Everything else that needs a plan is level 3" (F1).
- **Slide 10, deck:279:** the `--monitor 0` condition drops the guide's "or if you are not sure" case (F2).

### T1.AC4: met

- **Slide 12 meets FR-ONB.6:**
  - "being worked out" appears at deck:295, :301 and :305.
  - Issues #289 and #290 are plain anchors (T1.AC4@deck:301, :305).
  - "ask your lead" is at deck:296.
  - No rule is stated for either topic. The worktree definition (deck:300) is a plain-English term, not a rule.
- **Slide 3** describes model diversity only as what the skills do ("often on different models", deck:182) and names no model to use.
- **Slide 11** says "most under `.dev/`" (deck:286 = guide:238) and states no folder rule.
- **Slide 13** words the trap as all three sentences of guide:243 (deck:327). The subagent sign is a story only (deck:328, T611-613). A grep finds no "stop it", "kill" or "interrupt it" instruction.
- **Other slides:** a grep for worktree, contributing, model and `.dev/` finds no rule on worktrees, contributing, artifact folders or model choice. The hits are deck:163, :182, :251-253 and :286, which are descriptive, and deck:299-305, which is slide 12.

### T1.AC5: met

- **Light tokens** are on `:root` (T1.AC5@deck:13-28).
- **Dark tokens** are set under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` (deck:29-35), and again under `:root[data-theme="dark"]` (deck:36-40).
- **Body background** is set explicitly (deck:43).
- **Side gutter** is `max(16px, env(safe-area-inset-*))` (deck:58-59, :73-74, :112-113).
- **No doctype, html, head or body tag.** The grep's only hit is `<header>` at deck:138. `<title>` is at deck:7 and `<style>` at deck:12.
- **Print CSS** (deck:121-135):
  - It forces light tokens in all three theme states.
  - It puts one slide per page (deck:130-131) and hides the navigation (deck:128).
  - It compacts the cheat sheet (deck:132-133).
- **Footer:** "Built from HOW-WE-WORK.md at commit 070399eb", followed by the note naming the uncommitted Part A changes (deck:368). The guide link is at deck:369.
- **Maintenance-rule comment:** deck:1-6.

### T1.AC6: met

- Only Google Fonts is loaded (T1.AC6@deck:9-11).
- The github.com links are plain anchors (deck:301, :305, :362, :369).
- There is no `<img>`, no `src=`, no `url(` and no `@import`. The only script is inline (deck:372-404).

### T1.AC7: met

- The log records the commands and their output (T1.AC7@log:2-14, log:16-19). The latest re-scan, after the resume fix, is at log:25-27.
- My own re-run on the current deck agrees:
  - The key-shaped pattern finds nothing.
  - Every `sk-` hit is inside `task-builder`.
  - The only hosts are fonts.googleapis.com (2 hits), fonts.gstatic.com (1) and github.com (4).
- Advisory, still open: the re-scan blocks at log:21-27 record results only, not the command lines they ran.

## Factual errors found

| # | Slide | Deck text | Source | Problem |
|---|---|---|---|---|
| F1 | 5 | "Everything else that needs a plan is level 3, including work that touches many files or takes more than one session." (deck:211) | guide:17 ("This is the default for any planned change"), guide:19-20 (levels 5 and 6), guide:258 | The guide calls level 3 the default for planned work. It does not make level 3 everything except level 4. Level 6 work is planned with `/prd`, `/tdd` and `/roadmap`, and its task files run with `/task` (guide:20, 3.1). Level 5 sends a level-4-sized build to `/task-builder` (guide:19). The deck sentence takes in level 6 and so contradicts the six-level table it introduces. It is a dropped exception of the kind the brief names. Fix: "Level 3 is the default for any other planned change, including work that touches many files or takes more than one session." That is the guide:17 wording. |
| F2 | 10 | "Without the Augment Code review app on the repository, use `--monitor 0`." (deck:279) | guide:207 ("Without it, or if you are not sure the app is installed (the repository's Settings > GitHub Apps page lists it), use `--monitor 0`"); guide:269 | The deck drops the "or if you are not sure" case. A reader who is unsure would follow "always pass `--monitor 3`", which makes the rule stricter than the guide. Fix: "Without the Augment Code review app on the repository, or if you are not sure it is installed, use `--monitor 0`." Task 2's D6 should use the same wording. |

## Status of earlier findings

| Source | Finding | Status now |
|---|---|---|
| t1-qa.md #1 | Slide 3: "You do not choose models for this: the skill does" was false | fixed. The sentence is gone; deck:182 only describes what the skills do. |
| t1-qa.md #2 | Slide 6: the transcript-only "sc: plan run by sc: command" rule | fixed. deck:220 now gives the guide rule (guide:218), and the general form is an attributed story at deck:223. |
| t1-qa.md #3 | Slide 3: the unattributed "say so" advice | fixed. It is now an attributed story at deck:178 (T205). |
| t1-qa.md #4 | Slides 6 and 13 lacked the guide:243 exemption | fixed. deck:327 has all three sentences of guide:243, and deck:221 carries the exemption. |
| t1-qa.md #5 | Slide 6 grammar | fixed (deck:223). |
| t1-qa-2.md | Slide 5's hard limit dropped the `/sc:cleanup` and `/sc:improve` folder exception | fixed (deck:209 = guide:22). |
| t1-qa-2.md A1 | The attributed "sc:" rule of thumb has guide exceptions | open advisory. It is attributed, and the authority line at deck:156 covers it. |
| t1-qa-2.md A2, t1-qa.md advisory | Slide 15 gives section numbers, not "a link to the guide section" (spec:207) | open advisory. There is one guide link (deck:362). |
| t1-qa-2.md A3 | The re-scan blocks lack command lines | open advisory (log:21-27). |
| t1-qa.md advisory | Print from a dark system theme | addressed. The print block forces light tokens (deck:122-126). |

## extra_scope

None that counts:
- Home/End keys and the IntersectionObserver counter (deck:389-401) belong to the requested navigation.
- The `claude:viewport-fit-sides` meta tag (deck:8) is part of the artifact contract.
- The comment's mention of the Task 3 test (deck:5) is a note, not behavior.

## misunderstood

None.

## Advisories (not counted in the verdict)

- **deck:182, `/sc:reflect`.** It "checks finished work with several independent reviewers". That is true only of Tier 2. The default Tier 1 is one grounded card plus a calibrator (reflect.md:144-145). "With independent reviewers" would be safer.
- **deck:243, "Only for level 6".** This matches guide section 1 and 3.1. Guide:259, however, says to use `/tdd` "when other people will build against the design", which is a looser test. The Task 5 reviewer may question the added "Only".
- **Slide 3's rule card (deck:185-191) uses guide section 4.** That is not one of slide 3's FR-ONB.2 sources (T73-75, T205, T219). The content is accurate, the eyebrow cites section 4, and the guide outranks the transcript.
- **deck:287** says `superclaude update` "re-copies" each skill folder. Guide:3 says it "deletes and re-copies", so files you added there are lost. The closing instruction covers what to do.

## Fixes required

1. deck:211: replace "Everything else that needs a plan is level 3" with the guide:17 wording, as F1 gives.
2. deck:279: add "or if you are not sure it is installed" to the `--monitor 0` condition, as F2 gives.

VERDICT: missing
