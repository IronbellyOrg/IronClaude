# T5 spec-compliance QA: "Get an independent accuracy review to PASS"

Do not trust the implementer's report. Rubric: `~/.claude/skills/sc-implement-protocol/refs/qa.md`.

- Plan: `.dev/tasks/to-do/TASK-WF-implementFrOnb2T-20261023-192153/TASK-WF-implementFrOnb2T-20261023-192153.md` (Constraints :17-33, Task 5 :105-117).
- Start snapshot: `fb190dedc391b8a44a850545b4a3cbbd32d58cba`. Diff method: snapshot deck copied to `/tmp`, `git diff --no-index` against the current deck. 46 insertions, 42 deletions, all in `docs/onboarding/ironclaude-onboarding.html`. `git diff fb190ded -- . ':!.dev'` shows no other tracked file changed: `HOW-WE-WORK.md`, `CHANGELOG.md`, core `CLAUDE.md` and the test file are byte-identical to the snapshot. Nothing is staged.
- Path shorthand: `deck:N` = `docs/onboarding/ironclaude-onboarding.html` (worktree); `R1:N`, `R2:N`, `R3:N` = `/home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review.md`, `-2.md` and `-3.md`; `guide:N` = worktree `src/superclaude/core/HOW-WE-WORK.md`; `T N` = transcript `/home/coder/workspaces/IronClaude/.dev/research/ib-ai-onboarding-20261022/ib-ai-onboarding-pt2-transcript-2026-10-22.txt`; `A/` = `PKG/artifacts/`.

## Acceptance criteria

- **T5.AC1: met.** Each of the three reports has a claim table with one row per factual claim, giving where it is, the claim, the source checked and the result: R1:11-77 (65 rows), R2:11-77 (65 rows), R3:11-79 (67 rows, S1-S15, D1-D6 and the footer; S14 at R3:74, S15 at R3:75-76, D1 at R3:20, D6 at R3:63).
- **T5.AC2: met (third-FAIL outcome).** R1:159, R2:164 and R3:152 are all `VERDICT: FAIL`. All three reports are kept in `qa/`. The deck is marked not publishable at A/t5-completion-report.md:5 and :13, and that report carries the message to the user. Every finding of every report is fixed in the current deck, including R1-R5, which I checked myself against their sources (table below). The deck's mtime (17:27:24) is after R3 (17:26), which fits fixes made after round 3.
- **T5.AC3: met.** NFR-ONB.5 plain English: R3:140 (R1:145 and R2:150 failed it; both sets of findings are now fixed). NFR-ONB.6 no secrets: R3:142, R2:152, R1:147. FR-ONB.6 slide 12: R3:144. Slide 3 and slide 11 wording: R3:144. Slide 13: R3:71-72, plus R2:158, which confirms "no 'stop it'". I re-checked slide 13 myself: deck:565 is a story only, and a grep of the deck for "stop it" finds nothing. Section 2.4: R3:146.
- **T5.AC4: met.** A/t5-secret-scan.log:2-3 shows the key-string grep with no matches. A/t5-secret-scan.log:4-7 shows no URL hosts outside fonts.googleapis.com, fonts.gstatic.com and github.com, and no bare hostnames.
- **T5.AC5: met.** The report gives the Open Item 3 default at A/t5-completion-report.md:23 and the authority line at :24 (the line is at deck:183 per R3:17). All three report paths are absolute at :9-11. The footer follow-up is at :28-33: commit Part A, update the sha, remove the note, re-run the test, re-check slides 5, 6 and 10 plus the level-ladder and two-planner diagrams (D3 and D4), and re-publish to the same link.
- **T5.AC6: met.** A/t5-tests.log:7 shows "3 passed". I re-ran `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/docs/test_onboarding_deck.py -q -p no:cacheprovider` on the current deck: 3 passed in 0.08s.

Supporting checks:
- A/t5-deck-sha.txt:1 gives `569b3824...fad0`. `sha256sum` of the current deck gives the same value, so the files match.
- A/t5-render/summary.json was written at 17:28:50, after the deck's last write. It shows 15 slides and 6 SVGs at 1280 px and 375 px in both themes, `sw == iw` at 375 px (no horizontal scroll), lowest contrast 5.39 (light) and 5.67 (dark), a 15-page PDF in light and dark, `errors: []`, and network requests only to the page and Google Fonts. A/t5-render/overflow.json is `[]`.

## The 23 findings

| Finding | Source checked by this QA | Fixed? | Current deck line |
|---|---|---|---|
| F1 `/sc:reflect` overstated | R1:83-87; R2:135; R3:119 | fixed | deck:250 |
| F2 D3 hard limit drops exceptions | guide:22 (test-file and cleanup/improve exceptions) | fixed (test-file part at deck:333; cleanup/improve part as R2 at deck:339) | deck:333, deck:339 |
| F3 D4 always "moves to done/" | guide:17, guide:271 | fixed | deck:352, deck:369 |
| F4 "sc: follows sc:" stated as a rule | T 145, T 147; guide:218 | fixed | deck:390 |
| F5 D5 level 6 drops "a new component" | guide:20 | fixed | deck:428 |
| F6 "Only" on `/prd` and `/tdd` | guide:20, guide:259 | fixed | deck:445 |
| F7 D6 "Merge" box implies pr-submit merges | R1:119-123; R3:125 | fixed ("Clean: ready to merge", desc "It never merges the PR.") | deck:504, deck:483 |
| F8 "re-copies" drops "deletes" | guide:3 | fixed | deck:524 |
| F9 no link per guide section | R3:76 (anchors match guide headings) | fixed | deck:586-595 (e.g. deck:589) |
| F10 PRD, TDD, CI, harness undefined | guide:55, guide:63 | fixed | deck:341, deck:478, deck:241 |
| N1 D2 names `root-cause-analyst` | R2:81-85; R3:32 | fixed (`troubleshoot-analyst`) | deck:294 |
| N2 hedge on the wrong half | T 145 (no hedge), T 147 ("for the most part") | fixed | deck:390 |
| N3 pr-submit bullet drops Medium+ | guide:207, guide:269 | fixed | deck:478 |
| N4 "The guide's rules" read as complete; quality-check rule missing | guide:241 | fixed | deck:253, deck:257 |
| N5 "no written rule yet" overstated | R2:105-109 | fixed | deck:533 |
| N6 PR never expanded | guide:198 | fixed | deck:396 |
| N7 QA, subagents undefined | T 611-613 (per R3:72) | fixed | deck:565 |
| N8 acceptance criteria undefined at first use | guide:17 | fixed | deck:348 (before first D4 use at deck:361) |
| R1 slide 1 story adds "set it going and trust what comes back" | T 569 (no such words); a transcript grep for "set it going\|trust what" finds nothing | fixed (sentence ends at "over a long run.") | deck:182 |
| R2 D3 drops the `/sc:cleanup`/`/sc:improve` exception | guide:22 ("The one exception is `/sc:cleanup` and `/sc:improve` run on a folder") | fixed in the D3 caption, which R3:93 allows | deck:339 |
| R3 slide 8 drops the level-4 exception | guide:108 ("If the feature is level-4-sized ... build and run a task file instead (3.13)") | fixed | deck:445 |
| R4 90% story drops whose work | T 205 ("if I look at my work over the last two or three weeks ... 90% of it") | fixed ("the speaker said about 90% of their own recent work") | deck:246 |
| R5 caption cites only 3.2 | guide:91-108 (3.2 has no brainstorm step) | fixed (exact wording R3:111 proposed) | deck:431 |

All 23 are fixed. R1-R5 have not yet been re-checked by an independent reviewer. A/t5-completion-report.md:11 says so, and FR-ONB.5 still blocks publishing until a review passes.

## extra_scope

None. Every hunk in the diff traces to a finding or to a change that NFR-ONB.5 or the Constraints require:
- Removed the internal "D1"-"D6" labels from the SVG titles and captions (deck:193, :230, :272, :309, :322→325, :339, :351→355, :384, :399, :431, :482→486, :514). These change no fact. NFR-ONB.5 (spec.md:329) requires "No unexplained internal codes", so the removal is needed. A grep of the deck for `D[1-6][.:]` now finds nothing.
- Defined "tokens" (deck:240) and "spec" (deck:319, right after the first use at deck:318). NFR-ONB.5 requires jargon to be defined at first use. R3:140 lists both as defined.
- Removed "a person does that" (who merges) from D6. The guide does not state who merges (guide 3.11 ends at opening the PR), so the deck may not state it either (Constraints :28, single source). A rule about who merges would also be a contributing rule, which Constraints :27 allows only on slide 12. F7 stays fixed (deck:483, :504; R3:125).
- The harness gloss (deck:241) is worded slightly differently from R1's proposal but traces to F10.

## misunderstood

None. The task's stop rule after three FAIL reports is followed: the deck is marked not publishable and no fourth review was started (A/t5-completion-report.md:5, :13). Fixing R1-R5 does not change that outcome.

VERDICT: compliant
