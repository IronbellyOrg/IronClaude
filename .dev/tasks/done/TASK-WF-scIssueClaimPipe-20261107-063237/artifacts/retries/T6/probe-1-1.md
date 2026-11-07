ed51a97d3a9328a8f1e6f5d5dc9e51c8f4e64d6c
family remedy-after-agent-started: a failure text that tells the user to re-run although an agent is already running
command: grep -n -E "failed, f|\(failed|REMEDY\[" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
before:
741:        return emit(launch_result("failed", [(failed, "no usable worktree record")]))
764:                [(failed, f"could not write the launch record: {exc}")],
789:                [(failed, why)],
813:            (failed, f"agent launched but {RECORD_NAME} was not updated: {exc}")
after:
(the other three W-LAUNCH-FAILED sites run before any agent exists; only the record-update site changed)
