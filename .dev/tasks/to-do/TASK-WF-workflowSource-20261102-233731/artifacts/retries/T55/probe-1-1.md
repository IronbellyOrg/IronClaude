0d92c6aec57e6078c8c8a913371a83ad54c229bc
family=uncited-expected-result
defect form: an expected-result line with no (source: ...) or code/CHANGELOG citation
command: grep -n -e "^- " -e "^[0-9]\. " -- docs/testing/v5.0.0/user/D08-ccsession.md
before: (reviewer-identified sites) docs/testing/v5.0.0/user/D08-ccsession.md:50 docs/testing/v5.0.0/user/D08-ccsession.md:266 docs/testing/v5.0.0/user/D08-ccsession.md:440 docs/testing/v5.0.0/user/D08-ccsession.md:443
coupled sites: every Expected result block in Steps 1-17 and the edge table
after:
docs/testing/v5.0.0/user/D08-ccsession.md:52
docs/testing/v5.0.0/user/D08-ccsession.md:154
docs/testing/v5.0.0/user/D08-ccsession.md:157
docs/testing/v5.0.0/user/D08-ccsession.md:265
docs/testing/v5.0.0/user/D08-ccsession.md:268
docs/testing/v5.0.0/user/D08-ccsession.md:485
docs/testing/v5.0.0/user/D08-ccsession.md:488
docs/testing/v5.0.0/user/D08-ccsession.md:575

family=false-rationale
defect form: a stated reason for a step that the cited code does not support
command: grep -n -e "because ccsession" -e "lists only" -- docs/testing/v5.0.0/user/D08-ccsession.md
before:
154:- The five `mk` lines print `my work`, `-dash name`, `wt2 task`, `wt3 task` and then `my work-2`: `--sync-name` (the
155:- No other output. The copy runs exactly your installed ccsession; it is copied because ccsession looks for its shim
468:- The help lists only the tiers your `Access:` line in Step 3 allows, `*` on your start tier (source: `models.py:923
coupled sites: src/superclaude/skills/ccsession-tag/ccsession:315-318,383-390,1043-1144,1261-1263
after:
18:  - `c8` also unsets `CLAUDE_CONFIG_DIR`, which would move Claude Code's settings and history out of `$HOME/.claude` 
157:- No other output: `--sync-name` prints the name only when it changed something, and the `git` commands print nothin
513:- The help lists only the tiers your `Access:` line in Step 3 allows, `*` on your start tier (source: `models.py:923

family=real-home-writes
defect form: steps (Tier C, Cleanup) that write under the tester's real ~/.claude
command: grep -n -e "real .HOME" -e "real HOME" -e "~/.claude/" -- docs/testing/v5.0.0/user/D08-ccsession.md
before:
14:- Tier C only: a Coder workspace where `ccsession` already works for you (your `~/.claude/ccsession.env` or workspace
15:- **Where the steps write.** Tier B writes only under `/tmp/d08`: a throwaway `HOME` (`/tmp/d08/home`) holding a copy
16:  - the session names under `~/.claude/projects/-tmp-d08-c-repo/topics/` and Claude Code's own history of the test se
17:  - `~/.claude/cache/gateway-models.json`, rewritten by every launch through the shim (`ccsession:841-896`), and `~/.
18:  - state and log files under `~/.claude/state/` and `~/.claude/logs/`: the hooks that `superclaude install` register
62:grep -c 'ccsession-tag/hooks/session-start.sh' ~/.claude/settings.json
63:grep -c 'ccsession-tag/hooks/session-name.sh' ~/.claude/settings.json
109:cp -r ~/.claude/skills/ccsession-tag /tmp/d08/home/.claude/skills/
400:### Tier C — interactive Claude Code sessions on your real HOME and gateway
417:cat ~/.claude/projects/-tmp-d08-c-repo/topics/'d08 first.txt'
525:What stays in your real `HOME`, like after any session: Claude Code's history of the Tier C sessions in `~/.claude/p
coupled sites: plan Constraints line 26; Preconditions lines 12-18; Tier C intro :400-402; Steps 14-17; Cleanup :512+
after:
14:- Tier C only: a Coder workspace where `ccsession` already works for you (your `~/.claude/ccsession.env` or workspace
19:  - Tier C reads two things from your real `HOME` and writes neither: your installed ccsession skill, which is copied
20:  - The throwaway `HOME` registers only the three ccsession hooks, so the other SuperClaude hooks, which write `~/.cl
64:grep -c 'ccsession-tag/hooks/session-start.sh' ~/.claude/settings.json
65:grep -c 'ccsession-tag/hooks/session-name.sh' ~/.claude/settings.json
111:cp -r ~/.claude/skills/ccsession-tag /tmp/d08/home/.claude/skills/
404:Each step below starts a real Claude Code session (API tokens) through a copy of your installed ccsession, with `HOM
412:grep -s -c '^[^#]*CC_SHIM_PORT=' ~/.claude/ccsession.env
415:cp -r ~/.claude/skills/ccsession-tag /tmp/d08/c-home/.claude/skills/
422:      {"matcher": "startup|resume", "hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/s
425:      {"hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/session-name.sh", "timeout": 5
428:      {"hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/session-name.sh", "timeout": 5
457:ls -d ~/.claude/projects/-tmp-d08-c-repo
462:- `0`, or no output when you have no `~/.claude/ccsession.env`: your env file does not choose the shim port. ccsessi
464:- `HOME=/tmp/d08/c-home`, then `/tmp/d08/c-home/.local/bin/ccsession`, then the path of your Claude Code outside `/t
577:Tiers B and C leave nothing in your real `HOME`: they read your installed skill and your `~/.claude/ccsession.env` a
(all remaining ~/.claude hits are reads in the real HOME, or `~` hook paths written into /tmp/d08/c-home/.claude/settings.json that expand to the throwaway HOME under c8; no step writes under the real ~/.claude)
