# T1 spec-compliance re-QA after the round-3 fix pass: "Write the deck page with all 15 slides"

Reviewer: the same per-task spec-compliance reviewer that wrote `t1-qa-3.md`, applying the rubric in `~/.claude/skills/sc-implement-protocol/refs/qa.md`. Do not trust the implementer's report: the coordinator's change summary was used only to find the edits. I re-read the whole deck (404 lines) and re-checked all seven T1 criteria against the current file, with the same strictness on restated guide rules.

Short names used below:
- `deck` = `docs/onboarding/ironclaude-onboarding.html`
- `log` = `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153/artifacts/t1-secret-scan.log`
- `guide` = `src/superclaude/core/HOW-WE-WORK.md` (this worktree)
- `spec` = `/home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/spec.md`
- `T<n>` = line n of the transcript `ib-ai-onboarding-pt2-transcript-2026-10-22.txt`

The sources are the same as in `t1-qa-3.md`: the plan's Constraints and Task 1, spec:109-121, :187-207 and :263-270, the guide read in full, `recommend.md`, `troubleshoot.md` and `reflect.md`, the `sc-troubleshoot-protocol/` file list, and the transcript lines cited in FR-ONB.2. `git status` still shows only the untracked `docs/onboarding/` directory, holding only the deck.

## Status of the round-3 findings

| # | Finding in t1-qa-3.md | Current deck | Result |
|---|---|---|---|
| F1 | Slide 5 said "Everything else that needs a plan is level 3" (old deck:211), which took in level 6 | deck:211 now reads "Level 3 is the default for any planned change, including work that touches many files or takes more than one session." That is the guide:17 wording ("This is the default for any planned change"), and it no longer contradicts levels 5 and 6 (guide:19-20). | fixed |
| F2 | Slide 10 left out the "or if you are not sure" case for `--monitor 0` (old deck:279) | deck:279 now reads "Without the Augment Code review app on the repository, or if you are not sure it is installed (the repository's Settings &gt; GitHub Apps page lists it), use `--monitor 0`, which only opens the PR." That matches guide:207 and guide:269. | fixed |

Every finding from `t1-qa.md` and `t1-qa-2.md` is still fixed:
- slide 3: deck:178 and :182
- slide 6: deck:220-223
- the guide:243 rule on slides 6 and 13: deck:221 and :327
- the hard-limit exception: deck:209

## Acceptance criteria

### T1.AC1: met

The deck has 15 slide sections. Their `<h2>` headings match the 15 FR-ONB.2 slide names (spec:193-207), in order.

T1.AC1@deck:151, :161, :169, :198, :207, :216, :228, :235, :248, :270, :284, :295, :312, :334, :344

### T1.AC2: met

- Every transcript-sourced statement is an attributed story or explanation:
  - T1.AC2@deck:155 (T569-571)
  - deck:162-163 (T119-121, T221, T576), under the eyebrow "meeting explanation" at deck:160
  - deck:173 (T73-75) and deck:178 (T205)
  - deck:202 (T183)
  - deck:223 (T139-145)
  - deck:240 (T494-496)
  - deck:265 (T253)
  - deck:328 (T611-613)
- Slide 2 gives "about 70%" as "an opinion from the meeting, not a measured figure" (deck:163, T119).
- The guide-sourced statements trace to their sources:

| Deck lines | Source |
|---|---|
| deck:154 | guide:3 |
| deck:182 | guide:154; reflect.md:145 |
| deck:187-190 | guide:238-245 |
| deck:199-200 | troubleshoot.md:64, :82-84; the `sc-troubleshoot-protocol/refs/` list |
| deck:208-211 | guide:9, :17, :18, :22 |
| deck:217-221 | guide:218, :243, :258 |
| deck:229 | guide:51, :95 |
| deck:238-243 | guide:20, :53, :155, :262; recommend.md:19, :24 |
| deck:250-261 | guide:116-119 |
| deck:272-279 | guide:200-207, :244, :269 |
| deck:286-289 | guide:3, :213-220, :238 |
| deck:317-329 | guide:243, :257-263 |
| deck:336-338 | guide:246, :249, :288 |
| deck:349-358 | guide section 1 rows and sections 3.1-3.13 |

- No restated guide rule drops an exception or adds an "only" that the guide lacks. deck:243's "Only for level 6" is listed as an advisory below.

### T1.AC3: met

No statement from section 2.4 appears as it was said in the meeting:
- Nothing says `/sc:implement` commits per task (deck:249-265).
- Nothing says `/sc:pr-submit` commits your work (deck:272-279).
- Brainstorm "stops there; you decide the next step" (deck:238, guide:53).
- No plain `/research` command appears (deck:239, :322).
- Nothing says the task list was retired.

Slide 5 matches guide section 1:
- the tie-break (deck:208 = guide:9)
- the hard limit and its exception (T1.AC3@deck:209 = guide:22)
- level 4 and the level 3 default (deck:211 = guide:17-18)

Slide 10 matches guide 3.11 and section 4:
- the steps (deck:272-276 = guide:200-206)
- the push rule (deck:275, :279 = guide:204, :244)
- `--monitor 3` as the setting to pass and the default (deck:276, :279 = guide:206, :269)
- `--monitor 2` and `--monitor 0` as the alternatives, the latter with the full condition (deck:279 = guide:207)

### T1.AC4: met

- **Slide 12 meets FR-ONB.6:**
  - "being worked out" is at deck:295, :301 and :305.
  - Issues #289 and #290 are plain anchors (T1.AC4@deck:301, :305).
  - "ask your lead" is at deck:296.
  - No rule is stated for either topic.
- **Slide 3** describes model diversity only as what the skills do and names no model to use (deck:182).
- **Slide 11** says "most under `.dev/`" (deck:286 = guide:238) and states no folder rule.
- **Slide 13** words the trap as the three sentences of guide:243 (deck:327). The subagent sign is a story (deck:328). It has no "stop it" or "interrupt it" instruction. A case-insensitive grep for "kill" hits only the word "skill".
- **Other slides:** a grep for worktree, contributing, model and `.dev/` finds only descriptive hits outside slide 12, at deck:163, :182, :251-252 and :286.

### T1.AC5: met

- **Three-state theme tokens:**
  - light tokens on `:root` (T1.AC5@deck:13-28)
  - dark tokens under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` (deck:29-35)
  - dark tokens again under `:root[data-theme="dark"]` (deck:36-40)
- **Body background** is set explicitly (deck:43).
- **Side gutter** is `max(16px, env(safe-area-inset-*))` (deck:58-59, :73-74, :112-113).
- **No doctype, html or body tag.** A grep finds none. The only `<head`-prefixed tag is `<header>` at deck:138. `<title>` is at deck:7 and `<style>` at deck:12.
- **Print CSS** (deck:121-135):
  - It forces light tokens in all three theme states.
  - It puts one slide per page (deck:130-131).
  - It hides the navigation (deck:128).
  - It compacts the cheat sheet (deck:132-133).
- **Footer:** "Built from HOW-WE-WORK.md at commit 070399eb", followed by the note naming the uncommitted Part A changes (deck:368). The guide link is at deck:369.
- **Maintenance-rule comment:** deck:1-6.

### T1.AC6: met

- Only Google Fonts is loaded (T1.AC6@deck:9-11).
- The github.com links are plain anchors (deck:301, :305, :362, :369).
- There is no `<img>`, no `src=`, no `url(` and no `@import`. The only script is inline (deck:372-404).

### T1.AC7: met

- **The log:**
  - It records the scan commands and their output (T1.AC7@log:2-14, log:16-19).
  - The newest re-scan, after this fix pass, is the last block (log:29-31): no key, token, credential or IP matches, and no hosts outside the allowlist.
- **My own re-run on the current deck agrees:**
  - The key-shaped pattern finds nothing.
  - The only hosts are fonts.googleapis.com (2 hits), fonts.gstatic.com (1) and github.com (4).

## Factual errors found

None.

## extra_scope

None that counts:
- The Home/End keys and the IntersectionObserver counter (deck:389-401) belong to the requested navigation.
- The `claude:viewport-fit-sides` meta tag (deck:8) is part of the artifact contract.
- The comment's mention of the Task 3 test (deck:5) is a note, not behavior.

## misunderstood

None.

## Advisories (not counted in the verdict; carried to Task 5)

- **deck:182, `/sc:reflect`.** "With several independent reviewers" is true only of Tier 2. The default Tier 1 is one grounded card plus a calibrator (reflect.md:144-145).
- **deck:243, "Only for level 6".** This matches guide section 1 and 3.1. Guide:259 uses a looser test for `/tdd`: "when other people will build against the design".
- **deck:287.** It says "re-copies" each skill folder; guide:3 says it "deletes and re-copies". The closing instruction covers what to do.
- **Slide 15.** It gives section numbers plus one guide link (deck:362), where spec:207 asks for "a link to the guide section".
- **log:21-31.** The re-scan blocks record results without their command lines.
- **deck:223.** The attributed "sc:" rule of thumb has exceptions in the guide (guide:128, :203, :260). The authority line at deck:156 covers them.

VERDICT: compliant
