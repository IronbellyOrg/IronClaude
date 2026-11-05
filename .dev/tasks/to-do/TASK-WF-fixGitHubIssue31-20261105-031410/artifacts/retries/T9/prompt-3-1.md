0b3543fbe4c8765d9e8e6be1775ba8b430e9410c
Review one task for spec compliance.

Task brief: ## Task 9: Rewrite the README and script headers for the new rule

Depends on: Task 7

Edit src/superclaude/skills/ccsession-tag/README.md (the Orca section around the launch rules, the question, `CCSESSION_ASK_TIMEOUT`, `CCSESSION_AUTOSTART` and the reopen, roughly lines 205 to 280) and keep the header comments of ccsession and ccsession-orca in step. Document: the one question rule (asked only when there is no task, no name and no resume); the table of launch paths and what each does; auto-names (format, uniqueness, they appear in the saved-session list); the 30-second limit and its override; Ctrl+C cancels with status 130; CCSESSION_NAME and the Claude --name lift; the safety net for a typed line that cannot be a name; print mode and CCSESSION_AUTOSTART=0 staying untagged; the resolved drift that `--fork-session` skips the question as a resume-like option; Claude Agent Teams bypasses ccsession and is the one documented exception and a follow-up. Orchestrators are told to always pass the task or a name in the launch.

Acceptance criteria:
- T9.AC1: README.md contains each of the listed topics, no sentence still says Enter, Ctrl+C or a timeout start an untagged session in Orca, and the `--fork-session` statement matches the code.
- T9.AC2: `grep -rn 'src/superclaude' src/superclaude/skills/ccsession-tag` shows no new reference to a source-tree path.
Global constraints: 
- Scope is the IronClaude part of issue 315 only: src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/ccsession-orca, their tests and docs. The Coder repo (New Terminal hook, the claude wrapper handoff) is out of scope and is not touched.
- Build on master. Never rebase on or merge origin/clayphi/433-ccsession-orca-resume; its work is already in master through pull request 355 and it must not be pushed to or edited.
- The pull request 355 tab reopen in ccsession-orca keeps running first, under the same conditions as today (terminal, CCSESSION_AUTOSTART not 0, no resume option, ORCA_PANE_KEY set, only Orca's own options), ahead of the question and ahead of the auto-name.
- The typed prompt is never read as a label. A line typed at the question is a name unless it cannot be one (control character, more than one line, or over 245 bytes); normal lines, spaces included, stay names. No other input guessing.
- Decisions taken by the plan author where the source is silent, to be reported to the owner: CCSESSION_AUTOSTART=0 keeps meaning a plain untagged start with no question and no auto-name; print-mode launches (-p, --print) stay untagged because they are not interactive sessions; resume-like launches (--resume, -r, --continue, -c, --fork-session, --from-pr) keep their own session and get no label; CCSESSION_NAME is the supported explicit name and is read by ccsession-orca, while a Claude --name or -n in Orca's arguments is NOT lifted: it passes through to Claude unchanged and counts as a name carried (no question, no auto-name). This replaces the earlier lift decision (see the amendments below).
- Claude Agent Teams stays the one documented exception: it is documented and listed as a follow-up, not changed.
- All tests run only in throwaway HOME directories under the pytest tmp_path, with the fake Claude binary of the existing harness. Never touch the live ~/.claude or the live ccsession shim. Edit src/superclaude files only; never stage .claude/ mirrors except .claude/settings.json.
- Amendments from the advisory review, resolved before execution (source: .dev/reflect/pre-fixGitHubIssue31-20261105031639/adversarial/merged-verdict.yaml; they apply to every task and win over any task text that conflicts with them):
- RN-1: an invalid CCSESSION_NAME, an empty or failing --auto-name result (control character, over 245 bytes, a folder name with a leading dot or 4-byte characters, an unwritable topics directory) or an unexpected --ask status never stops Claude from starting. Fallback order: drop the bad name with a stderr warning, then auto-name, then a plain untagged start; ccsession-orca never exits 2 for these. A name equal to a saved label never silently resumes that conversation. Tests in Tasks 3, 4 and 7: leading-dot folder, name with a tab, 300-character CCSESSION_NAME, name equal to a saved label, failing --auto-name; each reaches the fake Claude.
- RN-2: Claude --name/-n/--name= in Orca's arguments is not lifted (Task 3 criterion 2 and the Task 7 --name case change accordingly): such a launch counts as name-carried and passes unchanged. CCSESSION_NAME is validated (RN-1) and unset before every exec.
- RN-3: --auto-name is dispatched in the early fast-path case of ccsession (before the main argument loop, after ensure_names_migrated), not next to --ask; tests for the texts --model, --claude-args, --shim and --tier=x.
- RN-4: Task 5 also updates test_orca_a_new_tab_or_a_rerun_is_still_asked and test_orca_relaunch_whose_conversation_is_gone_is_asked (Enter now auto-names), rewrites test_orca_invalid_name_asks_again, drops the "the prompt" argument from the Ctrl+C line-mode test, changes test_orca_saved_name_is_listed_and_resumes_before_the_prompt to the `--name demo "fix it"` form, and adds CCSESSION_NAME to the environment exclusion lists in tests/unit/test_ccsession_tag.py and tests/unit/test_ccsession_tiers.py. "Keep as they are" applies only to reopen tests that do not press Enter.
- RN-5: the typed line is read with IFS= read -r and tested raw for control characters and the 245-byte rule before any trimming; an exit-3 message that starts with "-" is passed after "--"; tests for a leading tab, a trailing tab, a mid-line tab, "- a list" and "--version".
- RN-6: ccsession-orca unsets CCSESSION_ASK_TIMEOUT and CCSESSION_NAME before the final exec (the one-second timeout test sets the variable while Claude's recorded environment must not contain it).
- RN-7: the Task 3 classification covers --session-id=*, --prefill=* and --name=*, a trailing --name with no value, and treats the values of known value-taking options (--model, --permission-mode, --add-dir, --allowedTools, --mcp-config) as non-positional; unknown options fail safe (counted as a task); one test per form.
- RN-8: a test runs ccsession --ask with CCSESSION_ASK_TIMEOUT=2 and asserts the hint reads "auto-named after 2s", next to the default-hint test, so a default left unlimited fails.
- RN-9: the auto-name carries seconds or a short random part, folder name and task words are cut first so the stamp is kept, and two --auto-name calls in the same minute with no saved topic give different labels.
- RN-10: the executor writes ./artifacts/launch-paths.md from the final pytest output; no test writes outside tmp_path.
- RN-11: ccsession-orca passes the auto-name hint; the default hint of ask_session_name stays as today for other callers; the Task 11 handoff states that the 30 s default now also applies to the Coder New Terminal hook and that the dependency on orchestrators passing a task or name is documented, not enforced.
- RN-12: the Task 9 criterion also pins the --session-id statement in README.md.
Start sha: 0b3543fbe4c8765d9e8e6be1775ba8b430e9410c
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/README.md b/src/superclaude/skills/ccsession-tag/README.md
index 9e6705bc..779ee135 100644
--- a/src/superclaude/skills/ccsession-tag/README.md
+++ b/src/superclaude/skills/ccsession-tag/README.md
@@ -220,29 +220,113 @@ example:
 /home/coder/.local/bin/ccsession-orca
 ```
 
-Orca accepts one executable there, with no arguments. Each Orca launch then:
-
-- Lists this worktree's saved sessions (as `ccsession --here` does; `*` lists
-  every worktree's) and asks
-  `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`. A name
-  starts or resumes that session; Enter, Ctrl+C, or no answer within 30
-  seconds starts an untagged one, so the tab never ends at a dead prompt. A
-  name that is not a valid label (too long, or holding a control character)
-  is asked again. Any other name works, one starting with `-` too
-  (it is passed on as `--name`).
-- Reopens the tab's own session without asking when Orca relaunches the tab
-  after a workspace restart (see below).
-- Skips the question when Orca resumes or continues a session
-  (`--resume <id>`, `--fork-session`, `--continue`), when there is no terminal,
-  when keys were already typed into the tab, or when `CCSESSION_AUTOSTART=0`.
-- Runs through the shim, and passes Orca's own arguments (its prompt,
-  `--prefill <text>`, resume flags) to Claude Code unchanged, after
-  ccsession's `--claude-args`, so a prompt is never read as a session name.
-
-Orca also uses this command for supervised workers (`orca orchestration
-worker-start`), and fails a worker whose Claude is not ready within 60 seconds.
-The 30-second limit keeps those workers starting. Change it with
-`CCSESSION_ASK_TIMEOUT=<seconds>` (`0` waits for ever).
+Orca accepts one executable there, with no arguments. Each Orca launch then
+runs through the shim and passes Orca's own arguments (its prompt,
+`--prefill <text>`, resume flags) to Claude Code unchanged, after ccsession's
+`--claude-args`, so a prompt is never read as a session name.
+
+#### The one question rule
+
+The session-name question is asked **only when Claude starts with no task, no
+name and no resume**, and someone can answer it (stdin, stdout and standard
+error are all a terminal, and `CCSESSION_AUTOSTART` is not `0`). The question lists this
+worktree's saved sessions (as `ccsession --here` does; `*` lists every
+worktree's) and reads:
+
+```
+Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):
+```
+
+- **A name** starts or resumes the session of that name. Spaces are fine, and
+  a name starting with `-` is passed on as `--name`.
+- **Enter**, or no answer within the time limit, starts the session under an
+  automatic name (below), so with the default limit the tab does not wait at
+  the prompt for ever.
+- **Ctrl+C** cancels: `ccsession-orca` exits with status 130 and Claude is not
+  started, so you are back at the shell.
+- **Text that cannot be a name** is not an error and not a name. A line that
+  holds a control character (a tab), is too long to save as a name (more than
+  245 bytes of file name, where each `/` or `%`, and a leading `.`, count as 3
+  bytes), or is several lines pasted becomes Claude's first message (after `--` when it starts with
+  `-`), and the session is auto-named from its first words. A normal line,
+  spaces included, stays a name.
+
+What each launch does:
+
+| Launch | Question | Name Claude gets |
+|---|---|---|
+| The Claude button, a plain relaunch of a new tab | Asked | The name typed; an automatic name on Enter, on the time limit, or on keys typed ahead (no question then) |
+| A prompt, `--prefill <text>`, or `--session-id <id>` (an agent or worktree launch) | No | An automatic name made from the prompt's first words (from the folder and a stamp alone when there is no prompt text, as with `--session-id`); Orca's arguments reach Claude unchanged and in their own order |
+| `CCSESSION_NAME=<name>` in the environment (a worker start) | No | That name (see below) |
+| Claude's own `--name`, `-n` or `--name=` | No | Left for Claude as given; nothing is added |
+| `--resume`, `-r`, `--continue`, `-c`, `--fork-session`, `--from-pr` | No | None: the session names itself |
+| A tab Orca relaunches after a restart, with a recorded session | No | The tab's own session is reopened (below) |
+| No terminal and no task or name (a worker start with nothing given) | No (nobody to ask) | An automatic name |
+| `-p` / `--print` (print mode) | No | None: the run is untagged |
+| `CCSESSION_AUTOSTART=0` | No | None: the launch is untagged |
+| `--version`, `--help`, and Claude's own subcommands (`mcp`, `doctor`, `update`...) | No | None: they start no session |
+
+The rows above describe a launch with no `CCSESSION_NAME`. A valid
+`CCSESSION_NAME` is an explicit instruction and names the session whatever the
+launch is (it is passed as `--name` even with `-p` or `CCSESSION_AUTOSTART=0`),
+so set it only on a launch that starts a new session.
+
+`--fork-session` and `--from-pr` are resume options like `--resume`, so they
+skip the question and get no name. `--session-id` starts a new session under an
+id you choose: it carries a task, so it skips the question and is auto-named.
+
+#### Automatic names
+
+A launch that needs a name and was given none gets one from
+`ccsession --auto-name [<task text>]`:
+`<folder>-<up to four words of the task>-<MMDD-HHMMSS>-<4 hex digits>`, for
+example `my-repo-fix-the-login-bug-1105-091530-3a7f`. The folder is cut to 20
+characters and each word to 12, and only letters, digits and hyphens are kept,
+so whatever the text holds (quotes, `$(...)`, a path, control characters) the
+label is one safe, valid name, well under the 245-byte limit. It is checked
+against the names already saved for this repo (a saved name resumes its
+session), and the stamp ends in a random part, so launches do not share one in
+practice: a label that matches a saved name gets `-2`, then `-3`. A name is
+saved only when the session starts, so two launches in the same second rely on
+the random part. If the name list
+cannot be written, no name is made and Claude starts untagged: a launch never
+stops here. The name is Claude Code's name for the session too, and joins
+`ccsession --here` once the session has started and the hooks have recorded it.
+
+#### Time limit
+
+The question gives up after 30 seconds. Orca fails a supervised worker whose
+Claude is not ready within 60 seconds, so a worker that was started with
+neither a task nor a name still starts. Change the limit with
+`CCSESSION_ASK_TIMEOUT=<seconds>` (`0` waits for ever, and the hint then drops
+the time). The limit lives inside the question itself (`ccsession --ask`), so
+every caller of `--ask` has it, not only `ccsession-orca`. `ccsession-orca`
+removes both this limit and `CCSESSION_NAME` from the environment it starts
+Claude Code with; a plain `ccsession` run leaves its environment as it is.
+
+#### `CCSESSION_NAME`: how an orchestrator names a session
+
+Set `CCSESSION_NAME=<name>` in the launch environment to name a session
+without a prompt. A valid name (the rules above) is used as the session's name
+and nothing is asked. An invalid one (a control character, or too long to save) is dropped with a
+warning on standard error, and the launch is then handled as if none was
+given: Claude still starts. A name equal to a saved label of this repo resumes
+that session, with a visible `Resuming '<name>'` line, while its conversation
+is still saved; if the conversation is gone, a new session starts under that
+name. A launch with a valid
+`CCSESSION_NAME` is never treated as a relaunch to reopen.
+
+**Orchestrators should always pass the task or a name in the launch** (a prompt
+argument, or `CCSESSION_NAME`). Without either, on a terminal the worker waits
+for the question until the time limit; with no terminal it is auto-named at
+once.
+
+#### Known exception
+
+Claude Agent Teams starts its teammates from inside Claude Code, without
+running `ccsession-orca`, so ccsession cannot name those sessions or ask about
+them. This is the one launch path this command does not cover. It is listed as
+a follow-up to issue 315.
 
 ### Reopening a tab after a restart
 
@@ -261,20 +345,35 @@ ran. So the tab reopens its own session instead of asking:
   the tab's recorded session is still saved, was started in this same folder
   and ran in another terminal (Orca relaunched the tab), it resumes that
   session: by its name when it has one in this repo's list, else by its id.
-- Everything else is unchanged. A new tab or split pane has no record and is
-  asked. A launch with a prompt, `--prefill`, a name or a session choice
-  (`--resume`, `--continue`, `--session-id`, `--fork-session`) behaves as
-  before. Running `ccsession-orca` again by hand in the same terminal is
-  asked. A session whose conversation was deleted, or that was started in
-  another folder, falls back to the question.
+- The reopen runs first, before the question and before any automatic name.
+  Everything else follows the one question rule above. A new tab or split pane
+  has no record and is asked. A launch with a prompt, `--prefill`, a name
+  (`CCSESSION_NAME` or Claude's `--name`) or a session choice (`--resume`,
+  `--continue`, `--session-id`, `--fork-session`, `--from-pr`) never reopens:
+  it is named, or resumed, as described above. Running `ccsession-orca` again
+  by hand in the same terminal is asked. A session whose conversation was
+  deleted, or that was started in another folder, falls back to the question.
 - A session belongs to one tab: when another tab opens it, the first tab
   forgets it, so two tabs never reopen the same session.
 
 The question itself is `ccsession --ask [<hint>]`: it prints the list and the
-question on the terminal and only the chosen name on standard output (empty
-for untagged). It exits 1 when it did not ask (no terminal, or keys already
-waiting), got no answer within `CCSESSION_ASK_TIMEOUT` seconds (unset or `0`:
-no limit), or input ended, and 130 on Ctrl+C.
+question on the terminal and only the answer on standard output. A `@LIMIT@`
+in the hint becomes the time limit in seconds. When there is no limit, a hint
+written as `<text>; <text with @LIMIT@>` loses its `; ...@LIMIT@...` part; a
+`@LIMIT@` anywhere else is left as written. Without a hint the question reads
+`Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s):`,
+for callers where an empty answer means an untagged session. Exit status:
+
+- `0`: a name, or an empty line for a blank answer (Enter);
+- `1`: it did not ask (no terminal, or keys already waiting), got no answer
+  within `CCSESSION_ASK_TIMEOUT` seconds (default `30`; `0` or a value that is
+  not a number: no limit), or input ended;
+- `3`: the typed text cannot be a name (a control character, over 245 bytes, or
+  several lines pasted; the 245-byte rule is the one above). It is printed as
+  typed, as a first message for Claude;
+- `130`: Ctrl+C.
+
+`ccsession --check-name <name>` exits 0 when the name is valid, else 1.
 
 ### Tab title in Orca
 
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/src/superclaude/skills/ccsession-tag/README.md b/src/superclaude/skills/ccsession-tag/README.md
index ed46c258..779ee135 100644
--- a/src/superclaude/skills/ccsession-tag/README.md
+++ b/src/superclaude/skills/ccsession-tag/README.md
@@ -228,8 +228,8 @@ runs through the shim and passes Orca's own arguments (its prompt,
 #### The one question rule
 
 The session-name question is asked **only when Claude starts with no task, no
-name and no resume**, and someone can answer it (stdin and stdout are a
-terminal, and `CCSESSION_AUTOSTART` is not `0`). The question lists this
+name and no resume**, and someone can answer it (stdin, stdout and standard
+error are all a terminal, and `CCSESSION_AUTOSTART` is not `0`). The question lists this
 worktree's saved sessions (as `ccsession --here` does; `*` lists every
 worktree's) and reads:
 
@@ -240,7 +240,8 @@ Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):
 - **A name** starts or resumes the session of that name. Spaces are fine, and
   a name starting with `-` is passed on as `--name`.
 - **Enter**, or no answer within the time limit, starts the session under an
-  automatic name (below). The tab never ends at a dead prompt.
+  automatic name (below), so with the default limit the tab does not wait at
+  the prompt for ever.
 - **Ctrl+C** cancels: `ccsession-orca` exits with status 130 and Claude is not
   started, so you are back at the shell.
 - **Text that cannot be a name** is not an error and not a name. A line that
@@ -255,7 +256,7 @@ What each launch does:
 | Launch | Question | Name Claude gets |
 |---|---|---|
 | The Claude button, a plain relaunch of a new tab | Asked | The name typed; an automatic name on Enter, on the time limit, or on keys typed ahead (no question then) |
-| A prompt, `--prefill <text>`, or `--session-id <id>` (an agent or worktree launch) | No | An automatic name made from the prompt's first words (from the folder and a stamp alone when there is no prompt text, as with `--session-id`); the prompt is Claude's last argument |
+| A prompt, `--prefill <text>`, or `--session-id <id>` (an agent or worktree launch) | No | An automatic name made from the prompt's first words (from the folder and a stamp alone when there is no prompt text, as with `--session-id`); Orca's arguments reach Claude unchanged and in their own order |
 | `CCSESSION_NAME=<name>` in the environment (a worker start) | No | That name (see below) |
 | Claude's own `--name`, `-n` or `--name=` | No | Left for Claude as given; nothing is added |
 | `--resume`, `-r`, `--continue`, `-c`, `--fork-session`, `--from-pr` | No | None: the session names itself |
@@ -282,9 +283,12 @@ A launch that needs a name and was given none gets one from
 example `my-repo-fix-the-login-bug-1105-091530-3a7f`. The folder is cut to 20
 characters and each word to 12, and only letters, digits and hyphens are kept,
 so whatever the text holds (quotes, `$(...)`, a path, control characters) the
-label is one safe, valid name, well under the 245-byte limit. It is never a
-name already saved for this repo (a saved name resumes its session), so two
-launches never share one: a clash gets `-2`, then `-3`. If the name list
+label is one safe, valid name, well under the 245-byte limit. It is checked
+against the names already saved for this repo (a saved name resumes its
+session), and the stamp ends in a random part, so launches do not share one in
+practice: a label that matches a saved name gets `-2`, then `-3`. A name is
+saved only when the session starts, so two launches in the same second rely on
+the random part. If the name list
 cannot be written, no name is made and Claude starts untagged: a launch never
 stops here. The name is Claude Code's name for the session too, and joins
 `ccsession --here` once the session has started and the hooks have recorded it.
@@ -296,8 +300,9 @@ Claude is not ready within 60 seconds, so a worker that was started with
 neither a task nor a name still starts. Change the limit with
 `CCSESSION_ASK_TIMEOUT=<seconds>` (`0` waits for ever, and the hint then drops
 the time). The limit lives inside the question itself (`ccsession --ask`), so
-every caller of `--ask` has it, not only `ccsession-orca`. Neither this limit
-nor `CCSESSION_NAME` is passed on to Claude Code.
+every caller of `--ask` has it, not only `ccsession-orca`. `ccsession-orca`
+removes both this limit and `CCSESSION_NAME` from the environment it starts
+Claude Code with; a plain `ccsession` run leaves its environment as it is.
 
 #### `CCSESSION_NAME`: how an orchestrator names a session
 
@@ -306,7 +311,9 @@ without a prompt. A valid name (the rules above) is used as the session's name
 and nothing is asked. An invalid one (a control character, or too long to save) is dropped with a
 warning on standard error, and the launch is then handled as if none was
 given: Claude still starts. A name equal to a saved label of this repo resumes
-that session, with a visible `Resuming '<name>'` line. A launch with a valid
+that session, with a visible `Resuming '<name>'` line, while its conversation
+is still saved; if the conversation is gone, a new session starts under that
+name. A launch with a valid
 `CCSESSION_NAME` is never treated as a relaunch to reopen.
 
 **Orchestrators should always pass the task or a name in the launch** (a prompt
@@ -351,8 +358,9 @@ ran. So the tab reopens its own session instead of asking:
 
 The question itself is `ccsession --ask [<hint>]`: it prints the list and the
 question on the terminal and only the answer on standard output. A `@LIMIT@`
-in the hint becomes the time limit in seconds (the part of the hint naming the
-limit is dropped when there is none). Without a hint the question reads
+in the hint becomes the time limit in seconds. When there is no limit, a hint
+written as `<text>; <text with @LIMIT@>` loses its `; ...@LIMIT@...` part; a
+`@LIMIT@` anywhere else is left as written. Without a hint the question reads
 `Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s):`,
 for callers where an empty answer means an untagged session. Exit status:
 
Earlier blocking findings of this start (empty on the first review): F2.1 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:258 anchor=src/superclaude/skills/ccsession-tag/ccsession-orca:246 chk=n,y,n,n family=readme-universal-claim fix=drop "the prompt is Claude's last argument" first=A2 origin=new: Orca's arguments keep their own order; only a typed message is appended last.
F2.2 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:299 anchor=src/superclaude/skills/ccsession-tag/ccsession:1853 chk=n,y,n,n family=readme-universal-claim fix=say ccsession-orca removes both first=A2 origin=new: a direct ccsession run passes both variables on.
F2.3 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:353 anchor=src/superclaude/skills/ccsession-tag/ccsession:1556 chk=n,y,n,n family=readme-universal-claim fix=describe the "; ...@LIMIT@..." form only first=A2 origin=new: a @LIMIT@ outside a "; " part is left as written.
F2.4 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:232 anchor=src/superclaude/skills/ccsession-tag/ccsession:1499 chk=n,y,n,n family=readme-universal-claim fix=add standard error first=A2 origin=new: --ask also needs standard error on a terminal.
F2.5 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:308 anchor=src/superclaude/skills/ccsession-tag/ccsession:1824-1827 chk=n,y,n,n family=readme-universal-claim fix=add the conversation-gone case first=A2 origin=new: a saved name whose conversation is gone starts a new session.
F2.6 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:286 anchor=src/superclaude/skills/ccsession-tag/ccsession:1818-1821 chk=n,y,n,n family=readme-universal-claim fix=drop "never" first=A2 origin=new: the label is checked against saved files only, the name is saved by the hook, the loop stops at -99.
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
