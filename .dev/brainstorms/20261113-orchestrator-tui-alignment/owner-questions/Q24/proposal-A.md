# Proposal A: a fresh, dedicated capture session on master, not the 409 session

## Answer

A new top-level agent session, created for this purpose in its own master-based Orca worktree (for example `orca-capture`), runs the read-only capture (XC-03) in wave W1 and, later, the join comparison (XC-04) in wave W3. The 409 session is left alone. The seeded test (OB-03) stays with the owner or a session the owner names under its own permission row.

## What happens next if the owner picks it

1. The coordinator creates the worktree with `orca worktree create --name orca-capture --base-branch origin/master --agent claude --prompt "<capture task>"` and owns its agent (project rule: every Orca worktree gets an agent; its creator owns it).
2. At W0 intake (XC-10 item (1)) the coordinator records that the new session exists and that its terminal holds no Run (`orchestration run-current` read back). Whether `agent launch` binds a Run is unknown (D-A), so this check is required, not assumed.
3. Under `GRANT(XC-03,live-read)` the session runs XC-03 in one sitting with read commands only and writes the dated capture file.
4. After PR #539 merges and the sweep is runnable on this host, the same worktree (rebased on the new master) runs XC-04 under `GRANT(XC-04,live-read)` with `superclaude sweep run --run <id>` on master code, recording the report path the sweep writes.
5. The worktree is removed after XC-04 is recorded.

## What it unlocks

- XC-03 in W1 and XC-04 in W3 without depending on whether the 409 session is still alive (UNVERIFIED today).
- XC-04 needs master code; the `issue-409-mvp` worktree is on an unmerged branch (`f104ca51a`, `origin/master` not an ancestor: merged-requirements.md line 234), so a master-based worktree fits XC-04 directly.
- No risk to the 409 worktree's unpushed commits and uncommitted records, which must survive until OB-01 (line 264).

## What it costs or risks

- A new worktree and agent to create, track and clean up; more coordinator work than reusing an existing session.
- The new session has no history with the observer, so it may misread observer output that the 409 session would know.
- If a launched agent's terminal is bound to a Run (D-A), the session must use a different plain terminal or the capture is held.
- The sweep run in XC-04 writes one report file into that worktree's `.dev/sweeps/`.

## What stays unresolved

- D-A (does `agent launch` create a Run), which affects step 2.
- Who runs OB-03; this answer only names the owner's default.
