ce3de5bf51645af4fec06ed1852e9c360d6566d7
Review one task for spec compliance.

Task brief: ## Task 3: Update the slide 12 heading, eyebrow and introduction and the footer hash in docs/onboarding/ironclaude-onboarding.html

In `docs/onboarding/ironclaude-onboarding.html`, slide `s12` (lines about 515 to 530): change the eyebrow line (`<p class="eyebrow"><b>12</b> · Contributing and open topics · GitHub issues #289 and #290</p>`) to `<p class="eyebrow"><b>12</b> · Contributing and worktrees · HOW-WE-WORK "Worktrees and branches", GitHub issue #290</p>`, keeping the middle-dot characters the line already uses; change the heading `Contributing, and one open topic` to `Contributing and worktrees`; change the introduction paragraph (`The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.`) to `Both rules are settled. The worktree rule is the left card and the guide section "Worktrees and branches"; the contributing rule is the right card, with its history in issue #290. If a case is not covered, ask your lead.` Keep the `Worktree and branch protocol` card and the `Contributing rules` card, including the link to issue 290, unchanged. Change the build footer `Built from HOW-WE-WORK.md at commit a98d7b42.` so that the hash is the output of `git rev-parse --short=8 HEAD` taken at the time of the edit (the commit before this change). No other line of the file changes.

Acceptance criteria:
T3.AC1: `grep -c -E 'one open topic|still open in its own issue|issues #289 and #290|open topics' docs/onboarding/ironclaude-onboarding.html` prints 0.
T3.AC2: (MB-1) The introduction paragraph of slide `s12` in `docs/onboarding/ironclaude-onboarding.html` is exactly `Both rules are settled. The worktree rule is the left card and the guide section "Worktrees and branches"; the contributing rule is the right card, with its history in issue #290. If a case is not covered, ask your lead.`, and the old sentence `the worktree topic is still open in its own issue` no longer occurs in the file.
T3.AC3: The file contains `Contributing and worktrees` (heading and eyebrow), the `Worktree and branch protocol` card, the `Contributing rules` card and `https://github.com/IronbellyOrg/IronClaude/issues/290`.
T3.AC4: The footer matches `Built from HOW-WE-WORK\.md at commit [0-9a-f]{8}\.` and the hash equals `git rev-parse --short=8 HEAD` at that moment.
T3.AC5: `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: ce3de5bf51645af4fec06ed1852e9c360d6566d7
Diff against the start snapshot: --- a/docs/onboarding/ironclaude-onboarding.html
+++ b/docs/onboarding/ironclaude-onboarding.html
@@ -513,9 +513,9 @@
 </section>
 
 <section class="slide" id="s12" aria-labelledby="s12-h">
-  <p class="eyebrow"><b>12</b> · Contributing and open topics · GitHub issues #289 and #290</p>
-  <h2 id="s12-h">Contributing, and one open topic</h2>
-  <p>The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.</p>
+  <p class="eyebrow"><b>12</b> · Contributing and worktrees · HOW-WE-WORK "Worktrees and branches", GitHub issue #290</p>
+  <h2 id="s12-h">Contributing and worktrees</h2>
+  <p>Both rules are settled. The worktree rule is the left card and the guide section "Worktrees and branches"; the contributing rule is the right card, with its history in issue #290. If a case is not covered, ask your lead.</p>
   <div class="grid2">
     <div class="card">
       <h3>Worktree and branch protocol</h3>
@@ -576,7 +576,7 @@
 </main>
 
 <footer>
-  <p>Built from HOW-WE-WORK.md at commit a98d7b42.</p>
+  <p>Built from HOW-WE-WORK.md at commit 4ce9f14b.</p>
   <p>Source of truth for every command and flag: <a href="https://github.com/IronbellyOrg/IronClaude/blob/master/src/superclaude/core/HOW-WE-WORK.md">HOW-WE-WORK.md</a>, except <code>--plugin</code>, which comes from the <a href="https://github.com/IronbellyOrg/IronClaude/blob/master/src/superclaude/commands/recommend.md"><code>/sc:recommend</code> command file</a>.</p>
 </footer>
 


Codegraph context
index_state: fresh
checked_at: 2026-11-26T17:40:41Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope

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