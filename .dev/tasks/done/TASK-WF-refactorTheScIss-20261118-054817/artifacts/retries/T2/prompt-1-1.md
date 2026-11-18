95e0f2bdc406be3bc071eb2840122f3b7961bd36
Review one task for spec compliance.

Task brief: ## Task 2: Point the skill summary, the contract paragraph and the template at the rule
Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/SKILL.md`: at line 17 replace "`full` (default) also implements without a commit or a push" so the sentence says `worktree` plans and waits for approval and `full` also implements without a commit or a push, and add that with no `--pipeline` the claim picks the level from the issue as `refs/claim.md` Wave 5 says; at line 89 (the Wave 5 summary) add that the wave sets `<L>` from `--pipeline` or the default rule; at line 138 replace "`pipeline_level` holds the level requested in this run, `full` when `--pipeline` was omitted" with the level used in this run, that is the `--pipeline` value or, when it was omitted, the level the default rule picked; keep the `already_launched` sentence. In `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7, replace "to the last step at the default level `full`" with "to the last step at level `full`", and keep "(up to the plan boundary at level `worktree`," and the "or you do after `--pipeline none`" ending. Line 92 (the Wave 8 summary) already ends with "`<L>` is the same level as in Wave 5." and stays unchanged on purpose, although the source names it. Do not add a return-contract field and do not touch the yaml block at lines 123-134.
Acceptance criteria (ids):
T2.AC1: `src/superclaude/skills/sc-issue-protocol/SKILL.md` lines 17 and 138 describe the picked level and no longer call `full` the single default; the yaml block of ten fields is unchanged and `pipeline_level` is still its first line.
T2.AC2: `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7 no longer contains "default level `full`" and still names the plan boundary at level `worktree`.
T2.AC3: `uv run pytest tests/skills/test_issue_protocol.py -k "skill or st10 or contract" -v` passes; `test_default_level_is_full_and_only_worktree_waits_for_a_person` still fails until Task 5, which is expected.
Global constraints: ## Constraints
- The rule is authored once, in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5). `issue.md`, `SKILL.md`, the next-steps template, the docs and the routing guide state the outcome in one sentence, which may name the 16-hour line once per file, and do not restate the order of the rule's checks or its unreadable fallback as a second rule; the full rule lives only in `refs/claim.md`.
- The rule reads three lines of `<D>/issue-summary.md`, which Wave 4 already writes from `templates/issue-summary.md`: `Type`, `Complexity` and `Effort estimate`. A value that is missing or not one of the allowed words counts as unreadable and gives `worktree`.
- No new return-contract field. The claim return contract keeps its ten fields (a test pins them); `pipeline_level` carries the level actually used.
- An `already_launched` re-claim still reports the stored level from the `launch` entry of `worktree.json` or its mirror file; that path is not changed.
- `--submit` still stops with `E-SUBMIT-NEEDS-FULL` when `--pipeline full` is not written out, including when `--pipeline` is omitted. The rule text of that STOP and its quoted message "--submit needs --pipeline full" stay as they are.
- Do not edit `tests/issue_watch/`, `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the launch-level guard text, or the ship-gate and OB-H paragraphs. The issue watcher keeps passing an explicit `--pipeline none` and never reaches the rule.
- Text added to installed skill, command and core files names no `src/superclaude/` path and no git or gh verb that `tests/skills/test_worker_contract.py` audits in new lines.
- Design and user-guide records keep their original text: this change only adds dated "Amended 2026-11-18" notes, and a note on a table row goes inside that row's last cell so the table stays a table.
- The new text is prose that a model follows, so the tests pin its wording and order, not an executable rule. Each task says which words are pinned.
- Never `git add` or `git add -f` any path under `.claude/`; `make sync-dev` writes those copies and they stay unstaged. `claim-handoff-planb` edits some of the same files, so rebase onto `origin/master` before any PR.
Start sha: 95e0f2bdc406be3bc071eb2840122f3b7961bd36
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index 7177638a7..5092d9a7f 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -14,7 +14,7 @@ mcp-servers: [litellm, auggie, codegraph]
 
 Two modes, chosen by the command (`~/.claude/commands/sc/issue.md`), which has already validated the flags:
 
-- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then, unless `--pipeline none` (which creates no worktree, launches no agent and ends after the comments), create or reuse the Orca worktree `issue-<N>`, copy `.dev/issues/<N>/` into it and launch one agent there at the level `--pipeline` names: `worktree` plans and waits for approval, `full` (default) also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Nothing ever merges. This skill never runs a step of `next-steps.md` itself (B2).
+- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then, unless `--pipeline none` (which creates no worktree, launches no agent and ends after the comments), create or reuse the Orca worktree `issue-<N>`, copy `.dev/issues/<N>/` into it and launch one agent there at the level `--pipeline` names: `worktree` plans and waits for approval, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. With no `--pipeline` the claim picks `full` or `worktree` from the issue (the rule is in `refs/claim.md`, Wave 5). Nothing ever merges. This skill never runs a step of `next-steps.md` itself (B2).
 - **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label, and post it. GitHub only: no ClickUp task and no self-assignment (B6).
 
 For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
@@ -86,7 +86,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
 4. **Wave 3, assign.** `gh issue edit <N> --repo <R> --add-assignee @me` (failure STOP `E-ASSIGN-FAILED`, before ClickUp and any comment), then `scripts/clickup_claim.py` with stdout to `<D>/clickup.json`; every ClickUp outcome except an argument error is non-fatal.
 5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/issue-summary.md` (effort in hours) and, when out of date, the analysis report as `<D>/analysis/analyze-<scope>.md` (`<scope>` in this file name is the last segment of the main path the issue touches). No file under `<D>/analysis/` has a name that starts with analysis, report, summary or findings.
-6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
+6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. This wave also sets the level `<L>`: the `--pipeline` value or, when it was omitted, the level the default rule of `refs/claim.md` picks from the issue. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8, except for `--pipeline none`, which ends the claim here (print the final output and the return contract). A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** Not for `--pipeline none`. `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
 9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when the guard is missing or not effective (no agent starts and no launch record is written); otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook, installs the L2 pre-push hook in the clone's shared hooks directory (`install_l2`) and adds the warning `W-L2-ABSENT` when that hook is not in effect (the launch still goes ahead: the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`, so this stays a warning). The agent, not this skill, runs the steps. Ship gate: no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP. `<L>` is the same level as in Wave 5.
@@ -135,7 +135,7 @@ enforcement_hook: installed | missing | null
 
 For `--pipeline none` no worktree is created: `worktree_status` is `not_requested` and `worktree_path`, `worktree_branch`, `worktree_match_key` and `worktree_warning` are `null`. `launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` reports the IR-4 preflight of the launch: `installed` means it passed (also when the launch then failed), `missing` means it failed and the launch was refused (`launch_status` `failed`, `launch_warning` `W-ENFORCEMENT-ABSENT`, no agent started), and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). `launch_warning` is the first launch code: a `launched` claim without an L2 pre-push layer carries `W-LAUNCH-NOT-CCSESSION` there when that also applies, else `W-L2-ABSENT`. The claim `status` stays `success` through any worktree or launch warning.
 
-`pipeline_level` holds the level requested in this run, `full` when `--pipeline` was omitted. An `already_launched` result keeps the level its running agent was launched with: read it from the `launch` entry of `.dev/issues/<N>/worktree.json` or, when that file has none (a re-claim from inside the worktree), from the mirror file the helper's detail names, because the helper's `already_launched` output carries no level (both hold `{level, submit, at}`).
+`pipeline_level` holds the level used in this run: the `--pipeline` value or, when it was omitted, the level the default rule of `refs/claim.md` (Wave 5) picked. An `already_launched` result keeps the level its running agent was launched with: read it from the `launch` entry of `.dev/issues/<N>/worktree.json` or, when that file has none (a re-claim from inside the worktree), from the mirror file the helper's detail names, because the helper's `already_launched` output carries no level (both hold `{level, submit, at}`).
 
 Coordinator handoff for `--pipeline none`: the claim leaves its files in the checkout that ran it. When a coordinator owns the issue, it runs the `worktree` step of `orca_worktree.py` (the repository, the issue number, the base branch and that folder as its arguments) and then `worker-start --worktree path:<the printed path>`. The script creates the worktree with no agent, because it must copy `.dev/issues/<N>/` into the worktree before any agent starts (a create that carries an agent would start that agent before the copy), and it closes the plain first tab Orca opens, so the coordinator must run `worker-start` straight after it, which supplies the agent. If the coordinator is down or stops between the script and `worker-start`, the worktree stays empty, with no agent and no terminal, and nothing runs in it. On its next wake the coordinator finds its adoption row still `reserved`: a start may or may not have happened, so it never starts again by itself. It reads `worker-list`; a worker in that worktree settles the row as `started` with its Dispatch id, and with no worker the row stays for a person to settle. A later worktree step for the same issue reuses the existing worktree through the script's reuse lookup (marker, record, basename, branch) instead of creating a second `issue-<N>`. A person sees such a worktree in `orca worktree ps` with an empty `agents` list and can start the coordinator or remove the worktree with `orca worktree rm`.
 
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
index c505fa770..abce19621 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
@@ -4,7 +4,7 @@
 
 Plan boundary: after step <K>
 
-Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at level `worktree`, to the last step at the default level `full`), or you do after `--pipeline none`.
+Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at level `worktree`, to the last step at level `full`), or you do after `--pipeline none`.
 
 1. `<command with its flags>`
    - Input: `@.dev/issues/<N>/issue-summary.md`


Codegraph context
index_state: fresh
checked_at: 2026-11-18T06:18:32Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

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
