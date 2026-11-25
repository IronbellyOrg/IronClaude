# Execution locus card

PRINT-SITE: the issue text itself (a wall-clock report, no log line): "ccsession launch takes 20 seconds and 5-10% of the CPU when session list is large"; the delay is visible in the terminal before the "Session name (...)" prompt appears (ccsession-orca runs `ccsession --ask`, /home/coder/.claude/skills/ccsession-tag/ccsession-orca:204).
RUN-SITE: /home/coder/.claude/skills/ccsession-tag/ccsession:1554-1663 (list_sessions, called with filter=worktree from show_saved inside ask_session_name, ccsession:1680) @ one bash process on this machine (coder workspace, the same machine and user that the report comes from)
SAME-ENV: yes
OBSERVE-VIA: same-shell
re-run permitted: yes (read-only listing, already run; `ccsession --here` and `--list` change no file)
