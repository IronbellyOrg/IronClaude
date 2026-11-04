e5978887292bc7009b10b8c5e9917dcd8b0ffd42
family=real-home-side-effects
defect form: guide claims Tier C sessions write only session history to the real ~/.claude, while installed hooks write ~/.claude/state and ~/.claude/logs
command: grep -n -i -e "session history" -e "only thing" -e ".claude/state" -e ".claude/logs" -- docs/testing/v5.0.0/user/D05-routing-core-files-issue-templates.md
before:
12:- `/tmp/d05` does not exist (`[ ! -e /tmp/d05 ] && echo OK` prints `OK`). Every file this guide creates is under `/tmp/d05`. No step moves, edits or deletes 
327:Deleting the repository is `[EXTERNAL]` and needs the `delete_repo` scope; if `gh` refuses, run `gh auth refresh -s delete_repo` and repeat, or delete it in
coupled sites: src/superclaude/hooks/hooks.json:18,49; src/superclaude/hooks/scripts/freshness-session-start.sh:8-9; freshness-user-prompt.sh:8-10; auggie-flag-clear.sh:10-12; Step 5/16 checksum scope. Same claim outside this task: D03-codegraph-graph-impact.md:13, D04-session-memory.md:12 (completed tasks; not edited here)
after:
12:- `/tmp/d05` does not exist (`[ ! -e /tmp/d05 ] && echo OK` prints `OK`). Every file this guide creates is under `/tmp/d05`. No step moves, edits or deletes 
327:Deleting the repository is `[EXTERNAL]` and needs the `delete_repo` scope; if `gh` refuses, run `gh auth refresh -s delete_repo` and repeat, or delete it in
