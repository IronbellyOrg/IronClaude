c2f598461e89d9dfb9b915a9e3d27e4f1f3a170b
Review one task for spec compliance.

Task brief: ## Task 1: Record the base commit, add the five rule bullets to guide section 4 and sync the plugin copy

Files: `src/superclaude/core/HOW-WE-WORK.md` and its byte-identical twin `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (./source.md section 3, component C1). Do not touch `src/superclaude/core/CLAUDE.md`.

First, before any edit: if ./artifacts/base-sha.txt does not exist, write the output of `git rev-parse HEAD` to it; if it exists, keep it. Call that SHA `<base>`. Save the heading text of the unedited guide with `git show <base>:src/superclaude/core/HOW-WE-WORK.md | grep '^## '` into ./artifacts/guide-headings-before.txt.

Second, before any tracked file differs from `<base>`: skip this step if ./artifacts/baseline-tests.log exists; otherwise run the 16 test files listed in ./source.md section 5 on the unedited tree with `uv run pytest <files> -q` and save the output to ./artifacts/baseline-tests.log. A test that already fails is recorded, not fixed.

Then insert these five bullets in section 4 after the last existing bullet (the one beginning "A `/sc:` command whose file names a skill") and before the line beginning "Where this guide says", with no new heading:

```
- **Contributing a skill, command or agent to IronClaude itself: file an issue first.** New team members do not open pull requests that add or change a skill, command or agent yet. File an issue with the "Feature request" form ("Suggest an improvement") instead, and say what is missing or broken and why. This covers IronClaude's own skills, commands and agents, not the ones in your project.
- **Look for an existing tool before you propose one.** `/sc:help` lists the commands and skills installed here (not agents). `/sc:recommend "<what you want to do, and why>"` suggests an existing tool, agents included. `/sc:recommend --plugin` searches outside plugins and community skills only, and installs nothing. Put what each search returned, or why it could not run, in your issue.
- **Every proposal issue, however filed, says three things:** what is missing or broken; what the searches above returned, or why one could not run; and which skills, commands or agents you know use the one you want to change, or "not known". No complete list of callers exists yet, so "not known" does not mean there are none.
- **Where changes go (maintainers).** Skill, command and agent files are edited in this repository's `src/superclaude/` and tried locally with `make sync-dev`. They reach users through the installer, which can overwrite local edits.
- **A future change will need evidence, and that gate is not available yet.** When contribution opens, a pull request that changes a skill, command or agent will need before-and-after evidence that the change adds value, not bloat; then a reviewer's approval; then a passing CI evaluation that meets an ROI (value compared with cost) threshold. The metric, the threshold and the approving role are not set, and a green test run does not satisfy this gate. The gate is not available yet; it depends on evaluation work such as issue 487 in IronbellyOrg/IronClaude. A change to one skill can also break the skills that call it.
```

Finally copy the edited guide over the plugin twin.

Acceptance criteria:
- ./artifacts/base-sha.txt holds one 40-character commit SHA that `git cat-file -e` accepts, and ./artifacts/baseline-tests.log exists and ends with the pytest summary line of the run on the unedited tree.
- The five bullets sit between the last existing section 4 bullet and the "Where this guide says" line; the output of `grep '^## '` on the guide equals ./artifacts/guide-headings-before.txt; every `git diff -U0 <base>` hunk for the guide lies between the `## 4.` and `## 5.` lines.
- The section 4 text contains "however filed", "not known", "value compared with cost", "not available yet", "installs nothing", `/sc:help`, `/sc:recommend` and `--plugin`; "issue 487 in IronbellyOrg/IronClaude" occurs exactly once in the guide; the text has no "only after", no percentage and no numeric threshold, and it names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed); the only mention of `src/superclaude` in section 4 is the maintainer bullet.
- `grep -nP '[^\x00-\x7F]'` on the guide and on the plugin twin prints nothing.
- `cmp` of the guide and the plugin twin exits 0, and `git diff --quiet <base> -- src/superclaude/core/CLAUDE.md` exits 0, where `<base>` is the SHA in ./artifacts/base-sha.txt.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/commands/test_worktrees_command.py tests/core/test_claude_md_routing_block.py -q` passes (these read both guide copies: ASCII and `## 4.` boundary, byte-equal twin, removed-phrase and quota scans, dry-run phrase scan, level-table block).

AC ids (source order):
T1.AC1: ./artifacts/base-sha.txt holds one 40-character commit SHA that `git cat-file -e` accepts, and ./artifacts/baseline-tests.log exists and ends with the pytest summary line of the run on the unedited tree.
T1.AC2: The five bullets sit between the last existing section 4 bullet and the "Where this guide says" line; the output of `grep '^## '` on the guide equals ./artifacts/guide-headings-before.txt; every `git diff -U0 <base>` hunk for the guide lies between the `## 4.` and `## 5.` lines.
T1.AC3: The section 4 text contains "however filed", "not known", "value compared with cost", "not available yet", "installs nothing", `/sc:help`, `/sc:recommend` and `--plugin`; "issue 487 in IronbellyOrg/IronClaude" occurs exactly once in the guide; the text has no "only after", no percentage and no numeric threshold, and it names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed); the only mention of `src/superclaude` in section 4 is the maintainer bullet.
T1.AC4: `grep -nP '[^\x00-\x7F]'` on the guide and on the plugin twin prints nothing.
T1.AC5: `cmp` of the guide and the plugin twin exits 0, and `git diff --quiet <base> -- src/superclaude/core/CLAUDE.md` exits 0, where `<base>` is the SHA in ./artifacts/base-sha.txt.
T1.AC6: `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/commands/test_worktrees_command.py tests/core/test_claude_md_routing_block.py -q` passes (these read both guide copies: ASCII and `## 4.` boundary, byte-equal twin, removed-phrase and quota scans, dry-run phrase scan, level-table block).
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: c2f598461e89d9dfb9b915a9e3d27e4f1f3a170b
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index 7f3147b4c..d6eefeabf 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -259,6 +259,11 @@ If evaluation intent is ambiguous, ask whether the user wants a new suite or a s
 - **Do only what was asked.** If you think something else should change, suggest it instead of doing it.
 - **When unsure which tool to use,** run `/sc:recommend "<what you want to do, and why>"` or ask your lead before starting anything large.
 - **A `/sc:` command whose file names a skill starts by loading that skill.** If Claude answers such a command without loading it, start a new chat and run the command again. Commands whose file names no skill (for example `/sc:help`, `/sc:explain`, `/sc:test`) run from their own file, so no skill load is expected.
+- **Contributing a skill, command or agent to IronClaude itself: file an issue first.** New team members do not open pull requests that add or change a skill, command or agent yet. File an issue with the "Feature request" form ("Suggest an improvement") instead, and say what is missing or broken and why. This covers IronClaude's own skills, commands and agents, not the ones in your project.
+- **Look for an existing tool before you propose one.** `/sc:help` lists the commands and skills installed here (not agents). `/sc:recommend "<what you want to do, and why>"` suggests an existing tool, agents included. `/sc:recommend --plugin` searches outside plugins and community skills only, and installs nothing. Put what each search returned, or why it could not run, in your issue.
+- **Every proposal issue, however filed, says three things:** what is missing or broken; what the searches above returned, or why one could not run; and which skills, commands or agents you know use the one you want to change, or "not known". No complete list of callers exists yet, so "not known" does not mean there are none.
+- **Where changes go (maintainers).** Skill, command and agent files are edited in this repository's `src/superclaude/` and tried locally with `make sync-dev`. They reach users through the installer, which can overwrite local edits.
+- **A future change will need evidence, and that gate is not available yet.** When contribution opens, a pull request that changes a skill, command or agent will need before-and-after evidence that the change adds value, not bloat; then a reviewer's approval; then a passing CI evaluation that meets an ROI (value compared with cost) threshold. The metric, the threshold and the approving role are not set, and a green test run does not satisfy this gate. The gate is not available yet; it depends on evaluation work such as issue 487 in IronbellyOrg/IronClaude. A change to one skill can also break the skills that call it.
 
 Where this guide says "your lead", read "yourself" if you work alone.
 
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index 7f3147b4c..d6eefeabf 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -259,6 +259,11 @@ If evaluation intent is ambiguous, ask whether the user wants a new suite or a s
 - **Do only what was asked.** If you think something else should change, suggest it instead of doing it.
 - **When unsure which tool to use,** run `/sc:recommend "<what you want to do, and why>"` or ask your lead before starting anything large.
 - **A `/sc:` command whose file names a skill starts by loading that skill.** If Claude answers such a command without loading it, start a new chat and run the command again. Commands whose file names no skill (for example `/sc:help`, `/sc:explain`, `/sc:test`) run from their own file, so no skill load is expected.
+- **Contributing a skill, command or agent to IronClaude itself: file an issue first.** New team members do not open pull requests that add or change a skill, command or agent yet. File an issue with the "Feature request" form ("Suggest an improvement") instead, and say what is missing or broken and why. This covers IronClaude's own skills, commands and agents, not the ones in your project.
+- **Look for an existing tool before you propose one.** `/sc:help` lists the commands and skills installed here (not agents). `/sc:recommend "<what you want to do, and why>"` suggests an existing tool, agents included. `/sc:recommend --plugin` searches outside plugins and community skills only, and installs nothing. Put what each search returned, or why it could not run, in your issue.
+- **Every proposal issue, however filed, says three things:** what is missing or broken; what the searches above returned, or why one could not run; and which skills, commands or agents you know use the one you want to change, or "not known". No complete list of callers exists yet, so "not known" does not mean there are none.
+- **Where changes go (maintainers).** Skill, command and agent files are edited in this repository's `src/superclaude/` and tried locally with `make sync-dev`. They reach users through the installer, which can overwrite local edits.
+- **A future change will need evidence, and that gate is not available yet.** When contribution opens, a pull request that changes a skill, command or agent will need before-and-after evidence that the change adds value, not bloat; then a reviewer's approval; then a passing CI evaluation that meets an ROI (value compared with cost) threshold. The metric, the threshold and the approving role are not set, and a green test run does not satisfy this gate. The gate is not available yet; it depends on evaluation work such as issue 487 in IronbellyOrg/IronClaude. A change to one skill can also break the skills that call it.
 
 Where this guide says "your lead", read "yourself" if you work alone.
 

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/base-sha.txt (full contents, 1 lines)
3cf7e22597a0aa8e35860a5860542dcc1bd82c82


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/guide-headings-before.txt (full contents, 8 lines)
## 1. How much process does this job need?
## 2. How to write a request
## 3. Workflows
## 4. Rules everyone follows
## 5. Easy mix-ups and surprising defaults
## Other commands
## Routing table
## Orca coordination


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/baseline-tests.log (full contents, 36 lines)
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-290
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collected 647 items

tests/unit/test_cli_install.py ......................................... [  6%]
.....................................................                    [ 14%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 17%]
......                                                                   [ 18%]
tests/skills/test_spec_panel_review_loop.py ............................ [ 23%]
................                                                         [ 25%]
tests/skills/test_issue_protocol.py .................................... [ 31%]
........................................................................ [ 42%]
........................................................................ [ 53%]
.....                                                                    [ 54%]
tests/skills/test_review_brief_placement.py .....                        [ 54%]
tests/skills/test_review_prompt_overrides.py ........................... [ 59%]
...                                                                      [ 59%]
tests/recommend/test_routing_refresh.py ................................ [ 64%]
........................................................................ [ 75%]
.......................................                                  [ 81%]
tests/recommend/test_cache.py ...............                            [ 83%]
tests/docs/test_onboarding_deck.py ...                                   [ 84%]
tests/commands/test_routing_plugin_parity.py .....                       [ 85%]
tests/commands/test_worktrees_command.py ............                    [ 87%]
tests/core/test_claude_md_routing_block.py ......                        [ 87%]
tests/core/test_default_branch_agreement.py .                            [ 88%]
tests/core/test_how_we_work_routing_table.py ........................... [ 92%]
...................................                                      [ 97%]
tests/commands/test_help_command.py ......                               [ 98%]
tests/cli/test_how_we_work_install.py .........                          [100%]

============================= 647 passed in 4.82s ==============================


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t1-tests.log (full contents, 17 lines)
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-290
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collected 115 items

tests/core/test_how_we_work_routing_table.py ........................... [ 23%]
...................................                                      [ 53%]
tests/commands/test_routing_plugin_parity.py .....                       [ 58%]
tests/skills/test_review_prompt_overrides.py ........................... [ 81%]
...                                                                      [ 84%]
tests/commands/test_worktrees_command.py ............                    [ 94%]
tests/core/test_claude_md_routing_block.py ......                        [100%]

============================= 115 passed in 0.90s ==============================


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: Markdown has no call edges; Grep floor: the edited guide is read by the 16 test files of source.md section 5 (the five that read both copies passed, see t1-tests.log); no other dependent is changed

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
