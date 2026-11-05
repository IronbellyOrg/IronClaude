---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-implementFrOnb2T-20261023-192153
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Build, guard and verify the IronClaude onboarding deck (Part B)

Source: ./source.md
Goal: A self-contained HTML onboarding deck at `docs/onboarding/ironclaude-onboarding.html` with the 15 slides and 6 diagrams the spec lists, a test that keeps its commands and flags in line with `src/superclaude/core/HOW-WE-WORK.md`, a render check at phone and desktop width in both themes, and an independent accuracy review that passes, so the operator can publish it as a private artifact.

## Constraints

- The spec is `.dev/releases/backlog/ironclaude-onboarding-deck/spec.md` in the main checkout (`/home/coder/workspaces/IronClaude`), not in this worktree. Scope is FR-ONB.2 to FR-ONB.7, the Part B rows of section 4.1 and NFR-ONB.1 to NFR-ONB.7 in section 5. FR-ONB.1 is already implemented in this worktree; Part C issues are filed as #289 and #290.
- Do not change `src/superclaude/core/HOW-WE-WORK.md` or any routing surface (core `CLAUDE.md`, `sc-recommend` skill and refs, `src/superclaude/cli/recommend/prompts.py`, the `plugins/` copies, routing tests). The deck follows the guide as it reads in this worktree now.
- The guide in this worktree is commit 070399eb (PR #285, merged to master on 2026-10-23) plus the uncommitted, unmerged Part A edits (43 insertions, 28 deletions in `HOW-WE-WORK.md`). The spec defines "Guide" as the guide after Part A (spec.md:189), so the deck is built from that unmerged text; the operator re-checks slides 5, 6 and 10 and diagrams D3 and D4 against the guide as merged before publishing.
- Do not commit, push or publish. Publishing the artifact is done by the operator after this plan completes, and only after the accuracy review in Task 5 is a PASS (FR-ONB.5).
- Source precedence for every deck claim: code, then `HOW-WE-WORK.md`, then the transcript (spec section 2.2). Transcript lines (`/home/coder/workspaces/IronClaude/.dev/research/ib-ai-onboarding-20261022/ib-ai-onboarding-pt2-transcript-2026-10-22.txt`) supply explanations and stories only, never commands, flags or rules. Transcript-only statements are shown as attributed stories ("in the onboarding meeting", "in our experience"); slide 2's "about 70%" is given as the opinion stated in the meeting (transcript line 119), not as a measured fact.
- None of the meeting statements in spec section 2.4 may appear as they were said: `/sc:implement` commits per task; `/sc:pr-submit` commits your work; brainstorm hands off to design automatically; a plain `/research` command exists; the task list is retired. The 2604-line task-builder fact is usable.
- Spec section 2.4's row "`/sc:pr-submit` defaults to `--monitor 3`" (spec.md:118) is superseded on this branch and on master since PR #285: the guide makes `--monitor 3` both the default and the setting to pass (HOW-WE-WORK.md:206, :244, :269). Slide 10 and D6 state `--monitor 3` as the setting to pass, with `--monitor 2` and `--monitor 0` as the alternatives guide 3.11 states (HOW-WE-WORK.md:207). This applies to the Task 1 content and to the Task 5 reviewer brief.
- The spec's D2 asks for five layers including "templates" (spec.md:225), but the real `sc-troubleshoot-protocol` skill has no `templates/` folder; its templates are files inside `refs/` (`refs/report-template.md`, `refs/hypothesis-card-template.md`). D2 therefore shows four layers: command, skill, refs loaded on demand (with the templates drawn as files inside refs/), and agents.
- No slide other than slide 12 states a rule on worktrees, contributing, artifact folders or model choice (FR-ONB.6). Slide 3 may say that the heavier skills check important work twice, with different models, and compare the results (what `/sc:adversarial` and `/sc:reflect` do; guide 3.6 names reviewers "from other AI model families" via `/sc:swarm-wizard`, HOW-WE-WORK.md:156), but it never tells the reader which model to use. Slide 11 uses the guide's wording "most under `.dev/`" (HOW-WE-WORK.md:238) and states no folder rule. Slide 13 words the task-builder trap as the guide section 4 rule (HOW-WE-WORK.md:243), with the "many reviewer subagents appear" sign as a story only and no "stop it" instruction (guide section 4 also says "Let a skill finish", HOW-WE-WORK.md:239).
- The deck names commands only as the guide names them and links to the guide on GitHub for exact usage; it does not copy step lists, flags or paths the guide does not state (spec section 2.2, single source of truth).
- Open Item 3 (whether slides 5 and 10 state that the guide replaces what was said in the meeting) is unanswered. Default for this plan: slides 5 and 10 state only the guide's rule and do not describe what was said in the meeting; the deck carries one general line that the guide is the authority wherever anything else differs. This default is reported to the user at the end (Task 5).
- No secrets, keys, tokens, hostnames or credentials anywhere in the deck (NFR12, NFR-ONB.6). The meeting's Orca and Coder network troubleshooting is excluded. People's first names from the spec's audience split may appear on the track slides; nothing else personal.
- Only one external host is allowed to load in the page: Google Fonts (artifact rules), with real fallback font stacks. No external images or scripts. The only link targets allowed are github.com (guide and issue links).
- Task 5 writes the accuracy review into the main checkout on purpose: the spec names that path (spec.md:257) and its `qa/` folder lives there.
- This plan was amended before its first step from the pre-check report `.dev/reflect/pre-implementFrOnb2T-20261023192341/REPORT.md` (findings M-001 to M-022 applied; M-023, an optional split of Task 1, not applied), as guide 3.10 allows.

## Phase 1: Build the deck

## Task 1: Write the deck page with all 15 slides

Create `docs/onboarding/ironclaude-onboarding.html` (new directory `docs/onboarding/`) as one self-contained page authored to the artifact page contract (no doctype, html, head or body tags; its own `<title>` and `<style>` at the top; color tokens on `:root` with dark-mode redefinitions under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`; explicit body background; side gutter `max(16px, env(safe-area-inset-left/right))`).

Content: the 15 slides of spec FR-ONB.2 (the table at spec lines 191-207), in that order, each built from its listed source and the Constraints above. Read the live guide sections each slide cites before writing it (`src/superclaude/core/HOW-WE-WORK.md` intro at line 3, sections 1, 2, 3.1, 3.2, 3.3, 3.5, 3.6, 3.11, 3.12, 3.13, 4 and 5), plus `src/superclaude/commands/recommend.md` for `--plugin` (slide 8), `src/superclaude/commands/troubleshoot.md` and `src/superclaude/skills/sc-troubleshoot-protocol/` for the real command-to-skill pair on slide 4, and the transcript lines the table cites for explanations. Slide 11 takes "`superclaude update` overwrites installed files" from the guide intro (line 3). Slide 12 (FR-ONB.6) names the worktree and branch protocol and the contributing rules as "being worked out", links https://github.com/IronbellyOrg/IronClaude/issues/289 and https://github.com/IronbellyOrg/IronClaude/issues/290 by number, says to ask your lead until they are settled, and states no rule for either. Terms such as "worktree", "progressive disclosure", "skill", "ref" and "level" are defined in plain English where first used (NFR-ONB.5).

Structure: vertically stacked slide sections that read complete with no script; a small script adds previous and next buttons, arrow-key and Page Up/Down navigation and a slide counter. Each slide shows an eyebrow citing its guide section. Print CSS puts one slide per page, hides navigation controls, and keeps the cheat sheet (slide 15) on one page (NFR-ONB.4). Works at 375 px wide with no horizontal page scroll (NFR-ONB.2). The footer reads "Built from HOW-WE-WORK.md at commit 070399eb" followed by a plain note that the Part A guide changes this deck follows (the level wording, the hard limit, section 3.13 and the default planner) are not yet committed (FR-ONB.7), and links the guide on GitHub. An HTML comment at the top of the file records the maintenance rule of FR-ONB.7: when `HOW-WE-WORK.md` changes in a way a slide depends on, update the deck in the same PR (or file a follow-up issue), update the footer commit and re-publish to the same link.

Acceptance criteria:
- `docs/onboarding/ironclaude-onboarding.html` exists and contains 15 slide sections whose headings match the 15 slide names of spec FR-ONB.2, in order.
- Every factual statement on every slide traces to the source the FR-ONB.2 table lists; transcript-sourced statements are attributed explanations or stories only, and slide 2's "about 70%" is presented as the meeting's stated opinion.
- No statement from spec section 2.4 appears as it was said in the meeting; slides 5 and 10 match the guide as it reads in this worktree (levels and hard limit from guide section 1; review and ship steps and the push rule from guide 3.11 and section 4), and slide 10 states `--monitor 3` as the setting to pass with `--monitor 2` and `--monitor 0` as the alternatives.
- Slide 12 meets FR-ONB.6: both topics marked "being worked out", issues #289 and #290 linked, no rule stated. Slide 3 describes model diversity only as what the skills do and names no model to use; slide 11 uses "most under `.dev/`" and states no folder rule; slide 13 words the trap as the guide section 4 rule with no "stop it" instruction; no other slide states a rule on worktrees, contributing, artifact folders or model choice.
- The page has light and dark token sets in the three-state shape above, a print stylesheet with one slide per page, the footer line "Built from HOW-WE-WORK.md at commit 070399eb" with the note naming the uncommitted Part A changes, and the maintenance-rule comment.
- The only external URLs loaded by the page are Google Fonts; links out (GitHub guide, issues) are plain anchors.
- A search of the file for key-like strings (`sk-`, `ghp_`, `token=`, `password`, `Bearer`, `.coder`, IP addresses) finds nothing, and a scan of every URL and hostname in the file finds only fonts.googleapis.com, fonts.gstatic.com and github.com; the commands and their output are saved to `./artifacts/t1-secret-scan.log`.

## Task 2: Draw the six diagrams as inline SVG

Depends on: Task 1

Add diagrams D1 to D6 of spec FR-ONB.3 (the table at spec lines 222-229) to `docs/onboarding/ironclaude-onboarding.html` as inline SVG on their slides: D1 on slide 2, D2 on slide 4, D3 on slide 5, D4 on slide 6, D5 on slide 7, D6 on slide 10. Each SVG uses only the page's color tokens (`currentColor` or `var(--token)`), has a `viewBox`, a `<title>` and a short text description, scales to the slide width, and sits in its own `overflow-x: auto` container so it never widens the page.

Diagram content and label rules:
- D1 (illustration): one prompt fanning out to five different results, contrasted with two agents plus a debate that merges the best parts. It carries no commands or flags; its labels trace to transcript lines 119-121 and 221-223 as an explanation only.
- D2: the four layers from the Constraints (command, skill, refs loaded on demand with templates drawn as files inside refs/, agents), with skill-to-skill call arrows named from `src/superclaude/commands/troubleshoot.md` line 100 and agents from line 99; its names are checked against those troubleshoot files.
- D3: the six levels from guide section 1 with the hard limit marked between levels 2 and 3.
- D4: `/sc:workflow` to `/sc:implement` (marked default) beside `/task-builder` to `/task` (marked rare, level 4), each with what it leaves on disk as the guide states it.
- D5: the pipeline of guide 3.1, 3.2, 3.3 and 3.11 with the spec-track and execution-track bands overlaid; the band names are titles taken from the spec's audience split, not guide steps.
- D6: open PR, review bot, findings, fixes, re-review, merge, at `--monitor 3` (the setting to pass) with `--monitor 2` (fixes locally, stops before pushing) and `--monitor 0` (only opens the PR) shown as the alternatives guide 3.11 states.

Acceptance criteria:
- Six inline `<svg>` elements exist, one each on slides 2, 4, 5, 6, 7 and 10, each with a `<title>`; the page references no external image files.
- No SVG uses a literal color: every fill and stroke is a token or `currentColor`, so it reads in both themes.
- Every command name and step label in D3, D4, D5 and D6 appears in `src/superclaude/core/HOW-WE-WORK.md` (D5's two band titles excepted); D2's names appear in `src/superclaude/commands/troubleshoot.md` or the `sc-troubleshoot-protocol` file list; D1 contains no command or flag.
- D1 shows the five-runs fan-out beside the two-agents-plus-debate merge; D2 shows the four layers and the skill-to-skill arrows; D3 marks the hard limit between levels 2 and 3; D4 marks `/sc:workflow` with `/sc:implement` as the default and `/task-builder` with `/task` as the rare option; D5 shows both track bands over the guide pipeline; D6 shows `--monitor 3`, `2` and `0` as stated above.

## Phase 2: Guard the deck against drift

## Task 3: Add the single-source claim test and the changelog entry

Depends on: Task 2

Create `tests/docs/test_onboarding_deck.py` (FR-ONB.4), following the style of the existing tests in `tests/docs/` (for example `tests/docs/test_retired_docs_absent.py`): it reads `docs/onboarding/ironclaude-onboarding.html`, extracts with the standard library the text of every `<code>` element and every SVG `<text>`, `<title>` and `<desc>` element, finds every slash command and every `--flag` in that text, and fails naming each one that does not appear in `src/superclaude/core/HOW-WE-WORK.md`, except `--plugin`, which is checked against `src/superclaude/commands/recommend.md` instead. Token rule: a slash command is "/" at the start of the text or after whitespace or an opening bracket or quote, followed by `[a-z][a-z0-9-]*` and an optional `:name` part, and not preceded by a path character (so `.dev/tasks/to-do/<id>/<id>.md` and `src/jobs/runner.py` are not commands); a flag is `--` followed by `[a-z][a-z0-9-]*`. The guide lookup is by whole token, so `/task` is not satisfied by `/task-builder`. It also fails if the footer line matching "Built from HOW-WE-WORK.md at commit <sha>" (a 7 to 40 character hex sha) is missing. Include one check that runs the extraction on in-memory text and proves an unknown slash command, an unknown flag and a missing footer each produce a failure, while a planted path such as `.dev/tasks/to-do/x/x.md` is not flagged. Add a Part B entry to the `CHANGELOG.md` section headed "routing — `/sc:workflow` is the default planner; `/task-builder` is for level 4 only" (line 7, the Part A entry), describing the new deck and test in plain English.

Acceptance criteria:
- `uv run pytest tests/docs/test_onboarding_deck.py -v` passes, output saved to `./artifacts/t3-tests.log`.
- The in-memory check proves an unknown slash command, an unknown flag and a missing footer each produce a failure, and a planted path is not flagged.
- SVG `<text>`, `<title>` and `<desc>` content is scanned as well as `<code>`, and `/task` is matched as a whole token.
- `uv run ruff check tests/docs/test_onboarding_deck.py` and `uv run ruff format --check tests/docs/test_onboarding_deck.py` pass.
- `CHANGELOG.md` has a Part B entry naming `docs/onboarding/ironclaude-onboarding.html` and `tests/docs/test_onboarding_deck.py`, under the line 7 routing heading and above the next `###` heading.

## Phase 3: Verify render and accuracy

## Task 4: Run the render check at phone and desktop width in both themes

Depends on: Task 3

The deck file has no doctype, so served alone it renders in quirks mode while the artifact host adds a standards-mode skeleton. For the render check, generate `./artifacts/render/index.html` by wrapping the deck file's text in a minimal `<!doctype html>` skeleton with a charset and viewport meta (regenerate it from the current deck before every check, so fixes are tested). Serve `./artifacts/render/` with `uv run python -m http.server <free port> --directory <that folder>` run in the background, and stop the server at the end of the task. Use the Playwright browser tools to check spec section 7.3 and NFR-ONB.1 to NFR-ONB.4 and NFR-ONB.7: at 1280 px, step through every slide with the keyboard and confirm all 15 slides and 6 diagrams render with no console errors; at 375 px, confirm no horizontal page scroll (`document.documentElement.scrollWidth <= innerWidth`); render with light and dark color schemes at both widths and confirm text and every diagram are legible in each (body text computed font size at least 14 px at 375 px, and the contrast ratio of the body text and diagram stroke tokens against the background token at least 4.5:1 in each theme); emulate print media and render a PDF (`page.pdf()` through the Playwright run-code tool, or headless Chromium print-to-PDF) and record its page count (one slide per page, cheat sheet on one page); list network requests and confirm only the page itself and Google Fonts are requested; record the file size. Fix any defect found in `docs/onboarding/ironclaude-onboarding.html`, then regenerate the wrapper and re-run the affected check and the Task 3 test. Save screenshots, the PDF and a short findings log under `./artifacts/` (for example `./artifacts/t4-1280-light.png`, `./artifacts/t4-375-dark.png`, `./artifacts/t4-print.pdf`, `./artifacts/t4-render-check.md`).

Acceptance criteria:
- `./artifacts/t4-render-check.md` records, with evidence, each check above as pass, including a per-theme legibility verdict at 1280 px and 375 px with the measured font size and contrast ratios, and lists every defect found and its fix.
- Screenshots exist for 1280 px and 375 px in light and dark themes; the PDF exists and its recorded page count is 15 with the cheat sheet on one page.
- At 375 px the page has no horizontal scroll; the console shows no errors; network requests are only the page and Google Fonts.
- The checks ran on a wrapper regenerated from the final deck, and the deck's navigation script ran in it (keyboard navigation verified).
- The file is well under 16 MB (size recorded).
- `uv run pytest tests/docs/test_onboarding_deck.py` still passes after any fix.

## Task 5: Get an independent accuracy review to PASS

Depends on: Task 4

Spawn a fresh reviewer agent that did not build the deck (FR-ONB.5). Brief it with the deck path, the spec path and sections (FR-ONB.2 table, FR-ONB.3 table, FR-ONB.6, section 2.4, NFR-ONB.5 and NFR-ONB.6), the guide path, the transcript path, the source precedence (code, then guide, then transcript), and the readings in this plan's Constraints: the superseded spec.md:118 row (`--monitor 3` is correct), the four-layer D2, the wording rules for slides 3, 11 and 13, and that transcript-sourced statements are attributed stories checked against the cited transcript lines, not against code. It starts from the assumption that mistakes exist, checks every factual claim on every slide and diagram, and writes `.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review.md` in the main checkout (`/home/coder/workspaces/IronClaude`) with one row per claim (claim, source checked, result) and a binary verdict: any finding of any severity is a FAIL, and a zero-finding PASS includes a self-audit naming what was checked. On FAIL, fix every finding in `docs/onboarding/ironclaude-onboarding.html`, re-run the Task 3 test, and spawn a new fresh reviewer that writes the next report to `.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review-2.md`, then `-3`, keeping every earlier report. Stop after the third report: if `accuracy-review-3.md` is also a FAIL, mark the deck not publishable and report to the user. Re-run the Task 1 key-string and host scan on the final deck and save it to `./artifacts/t5-secret-scan.log`. End with a completion report to the user (in chat and in `./artifacts/t5-completion-report.md`) that states the Open Item 3 default and the added "guide is the authority" line, the absolute paths of every review report, and the footer follow-up: commit Part A first, then update the footer sha to that commit, remove the "not yet committed" note, re-run the Task 3 test, re-check slides 5, 6 and 10 and D3-D4 against the guide as merged, and re-publish to the same link.

Acceptance criteria:
- A report under `.dev/releases/backlog/ironclaude-onboarding-deck/qa/` in the main checkout has one row per factual claim across all 15 slides and 6 diagrams, each with the source checked and a result.
- The latest report's verdict is PASS and includes a self-audit, or, after a third FAIL report, the deck is marked not publishable and the user is told; every earlier FAIL report is kept, and each of its findings is fixed in the deck.
- The reviewer confirms plain English (NFR-ONB.5), no secrets (NFR-ONB.6), slide 12 per FR-ONB.6, the slide 3, 11 and 13 wording rules, and no section 2.4 statement as said in the meeting.
- `./artifacts/t5-secret-scan.log` shows the final deck passes the key-string and host scan.
- `./artifacts/t5-completion-report.md` states the Open Item 3 default, the authority line, every review report path and the footer follow-up steps.
- `uv run pytest tests/docs/test_onboarding_deck.py` passes on the final deck, output saved to `./artifacts/t5-tests.log`.
