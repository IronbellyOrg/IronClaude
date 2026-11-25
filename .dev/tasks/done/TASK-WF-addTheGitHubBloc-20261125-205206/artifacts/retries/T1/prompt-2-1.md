d95df19b94c424a6b43ad5253478c032ab263523
Review one task for spec compliance.

Task brief: ## Task 1: Add the blocker check to Wave 2 and its output line in refs/claim.md

Edit `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, the section `## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)`. Its items 1 to 4 are the pull request, closed and assignee checks and item 5 remembers earlier comment IDs. Insert a new item 5 after item 4 and renumber the old item 5 to 6. The new item is a read-only check: run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == "open") | "#\(.number) \(.html_url)"'`. Apply these outcomes in this order. First, any output line matching `^#[0-9]+ https://` is an open blocker whatever the exit status, and the claim STOPs `E-BLOCKED` with the message "Issue #N is blocked by open issue(s): <each #number and link>; not claimed." Second, otherwise a non-zero exit (for example no access or an endpoint that is not served) or any output that does not match means the check could not run: continue as today and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output. Third, otherwise there are no open blockers (none, or only closed ones, print nothing): continue as today. The item says it runs for a re-claim and for every `--pipeline` value. Change the sentence that opens the section from "every STOP here makes no GitHub or ClickUp write (B9)" to "every STOP here makes no GitHub, ClickUp or Orca write (B9)". In `## Final output`, extend item 4 (the warnings item) with the sentence: when the Wave 2 blocker check could not run, print the held `Blocker check: could not run (<reason>); the claim went ahead without it.` line, also for `--pipeline none`. Leave Waves 3 to 8 and the "Coordinator handoff" paragraph unchanged.

Acceptance criteria (ids added by the orchestrator):
- T1.AC1: `## Wave 2` in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` contains `repos/<R>/issues/<N>/dependencies/blocked_by` and `E-BLOCKED`, and that item sits after the closed-issue item and the assignee item and before `## Wave 3`.
- T1.AC2: `## Wave 3` still holds the only `--add-assignee` call and does not mention `dependencies/blocked_by`.
- T1.AC3: The Wave 2 item states all three outcomes: an open blocker stops with `E-BLOCKED` naming each one, none or only closed continues as today, and an unreadable list continues and is reported in the final output.
- T1.AC4: `## Final output` carries the `Blocker check: could not run` line rule.
- T1.AC5: `grep -n "src/superclaude/" src/superclaude/skills/sc-issue-protocol/refs/claim.md` prints nothing and `grep -n "gh api" src/superclaude/skills/sc-issue-protocol/refs/claim.md` shows only `repos/<R>/...` or `user` paths.
Global constraints: ## Constraints

- Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour.
- Edit only the canonical files under `src/superclaude/`, the plugin guide copy and the tests. Do not edit or stage anything under `.claude/`; the generated copies come from `make sync-dev`.
- Inside the skill files and the command file under `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/commands/issue.md`, never write the text `src/superclaude/` (two existing tests forbid it), never write `{owner}/{repo}`, and keep every `gh api` path spelled `repos/<R>/...`.
- Do not touch the paragraph that begins "Coordinator handoff for `--pipeline none`:"; it must stay identical in `refs/claim.md`, `SKILL.md` and `commands/issue.md`.
- Do not add fields to the claim return contract in `SKILL.md`; a test pins its exact keys. A failed read is reported as one line of the final output.
- `SKILL.md` must stay under 500 lines.
Start sha: d95df19b94c424a6b43ad5253478c032ab263523
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 55135bc9b..d229752dd 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -35,13 +35,14 @@ Worker returns no file or an empty one: retry that worker once, then STOP `E-WOR
 
 ## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)
 
-Checked in this order; every STOP here makes no GitHub or ClickUp write (B9):
+Checked in this order; every STOP here makes no GitHub, ClickUp or Orca write (B9):
 
 1. `is_pull_request` is true -> STOP `E-NOT-AN-ISSUE`: "#N is a pull request, not an issue; not claimed."
 2. `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed."
 3. Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed."
 4. Already assigned to the current login -> continue (re-claim is allowed and idempotent).
-5. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).
+5. Blocker check (read only; it runs before the first write of Wave 3): run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == "open") | "#\(.number) \(.html_url)"'`. Apply the outcomes in this order. First, any output line that matches `^#[0-9]+ https://` is an open blocker, whatever the exit status: STOP `E-BLOCKED`: "Issue #N is blocked by open issue(s): <each #number and link>; not claimed." Second, otherwise a non-zero exit (for example no access or an endpoint that is not served) or any output that does not match means the check could not run: continue, and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output. Third, otherwise there are no open blockers (no output, or only closed ones): continue as today. The check applies to a re-claim and to every `--pipeline` value.
+6. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).
 
 ## Wave 3: assign (orchestrator)
 
@@ -146,5 +147,5 @@ Print, in this order:
    - `already_launched`: "agent already launched at <launched_at>" plus the script's `detail`, which names the two files that hold the `launch` entry (`<D>/worktree.json` and a file in the worktree's git directory); the user removes the entry from both to launch again. In place of the Wave 5 `Level:` line print `Level: <stored level> (stored)`, read from the `launch` entry of `<D>/worktree.json` or, when that file has none, from the mirror file the script's `detail` names; the stored level wins over the level picked in Wave 5.
    - Failed worktree (Wave 7 `status` `failed`) or failed launch (`status` `failed`): print no `Level:` line; the launch result and the warnings below name the failure.
    - `--pipeline none`: "No worktree created and no agent launched. Open .dev/issues/<N>/next-steps.md in this checkout and run its commands in your own session."
-4. Every warning, the worktree one first (print the Wave 7 `warning` as `worktree_warning: <code>`, so an unattended run shows it): the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook.
+4. Every warning, the worktree one first (print the Wave 7 `warning` as `worktree_warning: <code>`, so an unattended run shows it): the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook. When the Wave 2 blocker check could not run, also print the held `Blocker check: could not run (<reason>); the claim went ahead without it.` line, for `--pipeline none` too.
 5. The return contract (`SKILL.md`) and STOP.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 47c4a4472..d229752dd 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -41,7 +41,7 @@ Checked in this order; every STOP here makes no GitHub, ClickUp or Orca write (B
 2. `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed."
 3. Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed."
 4. Already assigned to the current login -> continue (re-claim is allowed and idempotent).
-5. Blocker check (read only; it runs before the first write of Wave 3): run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == "open") | "#\(.number) \(.html_url)"'`. Apply the outcomes in this order. First, any output line that matches `^#[0-9]+ https://` is an open blocker, whatever the exit status: STOP `E-BLOCKED`: "Issue #N is blocked by open issue(s): <each #number and link>; not claimed." Second, otherwise a non-zero exit (for example no access or an endpoint that is not served) or any output that does not match means the check could not run: continue, and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output; if a later STOP ends the claim, print the held line before the STOP code and its message. Third, otherwise there are no open blockers (no output, or only closed ones): continue as today. The check applies to a re-claim and to every `--pipeline` value.
+5. Blocker check (read only; it runs before the first write of Wave 3): run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == "open") | "#\(.number) \(.html_url)"'`. Apply the outcomes in this order. First, any output line that matches `^#[0-9]+ https://` is an open blocker, whatever the exit status: STOP `E-BLOCKED`: "Issue #N is blocked by open issue(s): <each #number and link>; not claimed." Second, otherwise a non-zero exit (for example no access or an endpoint that is not served) or any output that does not match means the check could not run: continue, and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output. Third, otherwise there are no open blockers (no output, or only closed ones): continue as today. The check applies to a re-claim and to every `--pipeline` value.
 6. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).
 
 ## Wave 3: assign (orchestrator)
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-issue-protocol/refs/claim.md:44 anchor="Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour." chk=n,n,n,y family=scope-addition fix=Delete the clause "; if a later STOP ends the claim, print the held line before the STOP code and its message" from item 5 covers="Change only what the source asks" first=A1 origin=new: Item 5 adds a rule the brief does not contain: when a later STOP ends the claim the held line is printed before that STOP; the brief says only to hold the line for the final output.
Saved-probe re-check hit locations (may be empty): probe-1-1: grep -n -F -e 'later STOP' refs/claim.md: 0 hits

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
