2c6888abf14294be87f1a2a886a6846e78735909
Review one task for spec compliance.

Task brief: ## Task 7: Replace the contributing card on slide s12 and review the deck against the guide

Depends on: Task 1

File: `docs/onboarding/ironclaude-onboarding.html`, slide `s12` (./source.md section 3, component C7).

- Eyebrow: `<b>12</b> · Contributing and open topics · GitHub issues #289 and #290`.
- Heading: `Contributing, and one open topic`.
- Intro sentence: `The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.`
- Replace the second card (the "Contributing rules" card) with this HTML, verbatim:

```
    <div class="card">
      <h3>Contributing rules</h3>
      <p>For now, file an issue; do not open a pull request that changes a skill, command or agent. Before you file, look for an existing tool with <code>/sc:help</code> and <code>/sc:recommend</code>, and note what the outside-plugin search <code>/sc:recommend --plugin</code> returns. Say what is missing or broken, what the searches returned, and which skills you know use it. A future change will need before-and-after evidence, a reviewer's approval and a passing evaluation; that gate is not available yet. The full rule is in the guide, section 4. History: <a href="https://github.com/IronbellyOrg/IronClaude/issues/290">issue #290</a>.</p>
    </div>
```

- The first card (the worktree and branch protocol card) stays byte-identical.
- Do not edit the footer line "Built from HOW-WE-WORK.md at commit ..." in this task (see Constraints); the operator commit-time steps of Task 8 decide whether it moves.

Acceptance criteria:
- The second card block of slide `s12` equals the HTML above byte for byte, and contains "not available yet" and "section 4".
- The new card contains no "being worked out"; the worktree card block is byte-identical to its text in `git show <base>:docs/onboarding/ironclaude-onboarding.html` (`<base>` is the SHA in ./artifacts/base-sha.txt); `git diff -U0 <base>` hunks touch only the eyebrow, heading, intro and second card of slide `s12`.
- In the new card, commands and flags appear inside `<code>` only as `/sc:help`, `/sc:recommend` and `--plugin`, and `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- ./artifacts/deck-slide-review.md lists every slide id of the deck with "consistent" or a one-line mismatch against the guide as edited by Task 1; a mismatch on a slide other than `s12` is recorded there for a follow-up issue and is not edited here.
- This task did not edit the footer line, and the footer still matches the pattern "Built from HOW-WE-WORK.md at commit" followed by 7 to 40 hex digits.

AC ids (source order):
T7.AC1: The second card block of slide `s12` equals the HTML above byte for byte, and contains "not available yet" and "section 4".
T7.AC2: The new card contains no "being worked out"; the worktree card block is byte-identical to its text in `git show <base>:docs/onboarding/ironclaude-onboarding.html` (`<base>` is the SHA in ./artifacts/base-sha.txt); `git diff -U0 <base>` hunks touch only the eyebrow, heading, intro and second card of slide `s12`.
T7.AC3: In the new card, commands and flags appear inside `<code>` only as `/sc:help`, `/sc:recommend` and `--plugin`, and `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
T7.AC4: ./artifacts/deck-slide-review.md lists every slide id of the deck with "consistent" or a one-line mismatch against the guide as edited by Task 1; a mismatch on a slide other than `s12` is recorded there for a follow-up issue and is not edited here.
T7.AC5: This task did not edit the footer line, and the footer still matches the pattern "Built from HOW-WE-WORK.md at commit" followed by 7 to 40 hex digits.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: 2c6888abf14294be87f1a2a886a6846e78735909
Diff against the start snapshot: diff --git a/docs/onboarding/ironclaude-onboarding.html b/docs/onboarding/ironclaude-onboarding.html
index df0797f7b..3fc0a6f6e 100644
--- a/docs/onboarding/ironclaude-onboarding.html
+++ b/docs/onboarding/ironclaude-onboarding.html
@@ -513,9 +513,9 @@
 </section>
 
 <section class="slide" id="s12" aria-labelledby="s12-h">
-  <p class="eyebrow"><b>12</b> · Open topics · GitHub issues #289 and #290</p>
-  <h2 id="s12-h">Being worked out</h2>
-  <p>Two topics came up in the onboarding meeting that the guide does not cover yet. Each has its own issue. Until they are settled, ask your lead.</p>
+  <p class="eyebrow"><b>12</b> · Contributing and open topics · GitHub issues #289 and #290</p>
+  <h2 id="s12-h">Contributing, and one open topic</h2>
+  <p>The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.</p>
   <div class="grid2">
     <div class="card">
       <h3>Worktree and branch protocol</h3>
@@ -524,7 +524,7 @@
     </div>
     <div class="card">
       <h3>Contributing rules</h3>
-      <p>How team members propose or change skills, commands and agents, and what evidence a change needs, is being worked out in <a href="https://github.com/IronbellyOrg/IronClaude/issues/290">issue #290</a>.</p>
+      <p>For now, file an issue; do not open a pull request that changes a skill, command or agent. Before you file, look for an existing tool with <code>/sc:help</code> and <code>/sc:recommend</code>, and note what the outside-plugin search <code>/sc:recommend --plugin</code> returns. Say what is missing or broken, what the searches returned, and which skills you know use it. A future change will need before-and-after evidence, a reviewer's approval and a passing evaluation; that gate is not available yet. The full rule is in the guide, section 4. History: <a href="https://github.com/IronbellyOrg/IronClaude/issues/290">issue #290</a>.</p>
     </div>
   </div>
 </section>

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t7-checks.log (full contents, 26 lines)
# T7 checks

cards in s12: 2
second card equals plan HTML byte for byte: True
contains 'not available yet': True ; contains 'section 4': True
'being worked out' in new card: False ; in whole s12: True
code tokens in new card: ['/sc:help', '/sc:recommend', '/sc:recommend --plugin']
worktree card (first) byte-identical to base: True

## diff hunks (git diff -U0 <base>):
@@ -516,3 +516,3 @@
@@ -527 +527 @@
## s12 line range now:
515:<section class="slide" id="s12" aria-labelledby="s12-h">
532:<section class="slide" id="s13" aria-labelledby="s13-h">
## footer line still matches pattern:
579:  <p>Built from HOW-WE-WORK.md at commit f3c1ef06.</p>
## removed lines:
-  <p class="eyebrow"><b>12</b> · Open topics · GitHub issues #289 and #290</p>
-  <h2 id="s12-h">Being worked out</h2>
-  <p>Two topics came up in the onboarding meeting that the guide does not cover yet. Each has its own issue. Until they
-      <p>How team members propose or change skills, commands and agents, and what evidence a change needs, is being wor
## pytest:
tests/docs/test_onboarding_deck.py ...                                   [100%]

============================== 3 passed in 0.13s ===============================


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/deck-slide-review.md (full contents, 21 lines)
# Deck slide review against the guide as edited by Task 1

s1: mismatch: deck line 181 says the guide "holds the exact commands and flags. The one exception is `--plugin` on slide 8, which comes from the `/sc:recommend` command file", but the new section 4 bullet at guide line 263 now names `/sc:recommend --plugin` itself, and slide 12 (deck line 527) also shows `--plugin`, so the stated exception no longer holds (the footer at deck line 580 makes the same claim; slide 8's exact form with a `"<goal>"` argument is still not in the guide); the rest of the slide (lines 179-183: what the guide is for, `superclaude install` copying it to `~/.claude/HOW-WE-WORK.md`) was checked against guide line 3 and is consistent.
s2: consistent (checked: lines 187-231; the slide makes no command, flag, section or rule claim from the guide, only meeting opinions labelled as such, and nothing in it contradicts the guide).
s3: consistent (checked: eyebrow line 235; the section 4 rule list at lines 255-259 against guide lines 253-257 and 259; `/sc:adversarial` at line 250 against guide lines 148-150; `/sc:reflect` at line 250 against guide lines 185-189: the guide does not say when reflect brings in several reviewers (it names `--tier 2` at line 189), so "when it is not confident or you ask for a deep check" is not covered by the guide but not contradicted; the meeting stories at lines 241 and 246 were not checked, as the guide does not cover them).
s4: mismatch: deck line 268 says "A command is a thin front door. It tells you and the agent how to use the skill and where the skill lives. The skill holds the actual pipeline.", but guide line 261 says commands whose file names no skill (for example `/sc:help`, `/sc:explain`, `/sc:test`) run from their own file with no skill load; the example `/sc:troubleshoot` itself matches guide 3.4 (line 121); not checked: the line counts 214 and 711 and the ref, agent and called-skill names in the diagram (lines 279-305), which the guide does not list.
s5: consistent (checked: eyebrow line 315; intro line 317 against guide line 9; hard limit at line 318 and diagram lines 327-329 against guide line 19; spec definition line 319 against guide line 95; level commands at lines 325, 331 and 333 against guide lines 15-17; line 337 against guide lines 17 and 21 and 3.1 steps 7-8 at guide lines 74-78).
s6: consistent (checked: lines 343-344 against guide line 17; diagram lines 353-365 (plan path, `progress.md`, final independent review, move to `done/` on Linux only) against guide lines 17 and 284; the `TASK-WF-*` rule at line 370 against guide line 219; the existing-plan rule at line 372 against guide line 23; the meeting remark that the task builder "has since been removed" (line 372) is not a guide claim: the guide does not say it was removed and names "task-builder" only in a "no ... task-builder" note at line 349; no `task-builder` skill exists under `src/superclaude/skills/`).
s7: mismatch: deck lines 382 and 400-403 put "Review: automatic on the PR" as the step before "Open PR: `/sc:pr-submit`" ("Seven steps in order ... review, open the PR"), but guide 3.11 lines 201-206 have `/sc:pr-submit` open the PR first and only then wait for the review App, and guide line 204 says the App can be absent (monitor 0), so that review neither comes before the PR nor is always automatic; the check the guide does put before shipping is the plan's compliance results and final review (guide line 80); the rest of the slide (lines 378, 391-399 and 410-411) was checked against guide lines 50-54, 74-78 and 92-103 and is consistent.
s8: consistent (checked: `/sc:brainstorm` at line 422 against guide line 54; `/sc:analyze` versus `/sc:research` at line 423 against guide lines 138-139; `/sc:recommend "<goal>" --plugin` at line 424 against new guide line 263 (the guide's form has no goal argument, not a contradiction); `/sc:spec-panel` at line 425 against guide line 60; the full-specification rule at line 427 against guide 3.1 (line 50) and 3.2 (lines 95-98); eyebrow line 418).
s9: consistent (checked: lines 434-437 against guide lines 17, 111-114 and 219; the stop-code table at lines 443-445 (`E-HALT-QA`, `E-RESUME-NEEDED`, `E-PLAN-CHANGED`) against guide line 114; eyebrow line 431).
s10: consistent (checked: the review-only command and flags at line 455 against guide line 193; the shipping order at lines 457-460 against guide lines 199-202 and 258; monitor ceilings 0 to 3 in diagram lines 465-498 and text line 502 against guide lines 202-208 and 282; the push rule at line 502 against guide line 258; the stronger-project-rule conflict at line 502 against guide line 208; the "Medium severity or higher" threshold and the name "Augment Code review app" (lines 465, 477, 502) are not in the guide, which says only "review App", and are not contradicted by it).
s11: consistent (checked: line 509 against guide line 253; the `superclaude update` card at line 510 against guide line 3; ccsession resume at line 511 against guide lines 212-219: the slide's "from a terminal in the same folder" is narrower than guide line 214's "any worktree or copy of the same repo (outside git, the same folder)" but still true; eyebrow line 506).
s12: mismatch: card 1 at deck line 523 (with the second half of intro line 518) says when a session gets its own worktree, "where they live and how they are named is being worked out in issue #289", but guide line 366 (Orca coordination section) already says feature and child worktrees are created by Orca at its default paths, not under `.dev/worktrees/`, and guide line 304 already answers item 4 of issue 289 (when to remove a worktree); today's edits were checked against the new section 4 bullets and are consistent: eyebrow line 516, heading line 517, intro line 518 ("The contributing rules are settled for now"), and card 2 at line 527 against guide lines 262-266 (file an issue, no pull request yet, `/sc:help`, `/sc:recommend`, `/sc:recommend --plugin`, the three things an issue says, the future before-and-after evidence, reviewer approval and evaluation gate that is not available yet, "section 4"); card 2's differences are omissions, not contradictions: it says a pull request that "changes" where guide line 262 says "add or change", and it leaves out the "Feature request" form and the IronClaude-only scope (line 262) and the "or why one could not run" and "not known" parts (lines 263-264).
s13: consistent (checked: the look-alike row at line 539 against guide line 276; eyebrow line 533 cites sections 1 and 3.12, which exist, though the slide now draws only on section 5; the meeting story at line 543 ("The sign ...") has no guide counterpart and no referent left on the slide; neither is contradicted by the guide).
s14: consistent (checked: `/sc:recommend "<what you want to do, and why>"` at line 550 against guide line 260; `/sc:help` "lists the installed commands and skills and shows the three levels" at line 551 against guide lines 229 and 263 and the three-row level table at guide lines 13-17, which `/sc:help` prints verbatim per `src/superclaude/commands/help.md` line 73; that command file itself still calls it "the six process levels" at its lines 3, 65, 73 and 103, a stale label outside the guide, not a deck mismatch; "your lead" at line 552 against guide lines 260 and 268).
s15: consistent (checked: all seven rows at lines 563-569 against guide lines 15-17, 107, 116, 121, 193, 199-208, 214-219, 260 and 263; every link anchor on lines 563-569 matches a guide heading by GitHub's slug rule: `#1-how-much-process-does-this-job-need` (guide line 7), `#32-add-a-feature-to-an-existing-system-no-prd-needed` (line 88), `#33-make-a-small-well-defined-change` (line 105), `#34-fix-a-bug` (line 118), `#35-investigate-how-something-works-or-whether-an-idea-is-feasible` (line 134), `#311-review-only-or-deliberately-ship-and-open-a-pull-request` (line 191), `#312-resume-after-a-crash-or-a-lost-session` (line 210), `#4-rules-everyone-follows` (line 251); the full-guide link and installed path at line 573 against guide line 3).

## Footer

The footer line `Built from HOW-WE-WORK.md at commit f3c1ef06` exists, on deck line 579 (written with a closing period); its value was not judged.


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: HTML deck, no call edges; Grep floor: tests/docs/test_onboarding_deck.py reads the deck (3 passed, see t7-checks.log); the slide-by-slide review against the guide is ./artifacts/deck-slide-review.md

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty):

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
