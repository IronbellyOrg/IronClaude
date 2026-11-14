<!-- Provenance: Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14; executor: merge-executor; plan: adversarial/refactor-plan.md (5 changes planned, 5 applied) -->
<!-- Incorporated: Variant 1 advocate (Changes 1, 5), all three advocates A-001 (Change 2), Variant 2 (Change 3), Variant 3 and Variant 1 advocate (Change 4) -->

# Proposal A: a fresh, dedicated capture session on master, not the 409 session

## Answer

<!-- Source: Variant 1 (base), first two sentences unchanged; last sentence replaced per plan Change 3 (Variant 2, C-002; INV-014 authorship) -->
A new top-level agent session, created for this purpose in its own master-based Orca worktree (for example `orca-capture`), runs the read-only capture (XC-03) in wave W1 and, later, the join comparison (XC-04) in wave W3. The 409 session is left alone. The owner runs the seeded test (OB-03) and authors its record, unless the owner names another runner in writing under `GRANT(OB-03,seeded-write)`; the capture session never holds that row.

## What happens next if the owner picks it

<!-- Source: Variant 1 (base) steps 1, 2 and 4 unchanged; step 3 changed per plan Changes 2, 3 and 4; step 5 replaced per plan Change 1 -->
1. The coordinator creates the worktree with `orca worktree create --name orca-capture --base-branch origin/master --agent claude --prompt "<capture task>"` and owns its agent (project rule: every Orca worktree gets an agent; its creator owns it).
2. At W0 intake (XC-10 item (1)) the coordinator records that the new session exists and that its terminal holds no Run (`orchestration run-current` read back). Whether `agent launch` binds a Run is unknown (D-A), so this check is required, not assumed.
3. Under `GRANT(XC-03,live-read)` the session runs XC-03 in one sitting with read commands only and writes the dated capture file.
   <!-- Source: plan Change 2 (all three advocates, A-001) -->
   - XC-03's first recorded step is one `orca orchestration worker-list --run <id> --json` read, from the terminal that holds no Run, of a non-empty Run held by another terminal, with `page.total` recorded next to the unscoped count. Reason: Q-1 fenced only the mailbox read `check --all` (`q1-result.md`), not `worker-list`; whether a Run-less terminal can list another terminal's non-empty Run is UNVERIFIED.
   <!-- Source: plan Change 4 (Variant 3, X-002; Variant 1 advocate Concession 2) -->
   - The session is handed the observer's verified field list (`src/superclaude/cli/observe/parse.py`) and, if the 409 session is alive, may ask it read-only questions about observer fields; the 409 session runs no live Orca command for these items.
   <!-- Source: plan Change 3 (Variant 2, C-002) -->
   - The session holds only the live-read rows for XC-03 and XC-04; it never holds `GRANT(OB-03,seeded-write)`.
4. After PR #539 merges and the sweep is runnable on this host, the same worktree (rebased on the new master) runs XC-04 under `GRANT(XC-04,live-read)` with `superclaude sweep run --run <id>` on master code, recording the report path the sweep writes.
<!-- Source: plan Change 1 (Variant 1 advocate Concession 4), replaces base step 5 -->
5. Before the worktree is removed, the sweep report written under `<root>/.dev/sweeps/` (`sweep/commands.py:235-241`) is copied into the ledger package and the copy path recorded in the XC-04 record. The worktree is removed only after that copy is recorded.

## What it unlocks

<!-- Source: Variant 1 (base), unchanged -->
- XC-03 in W1 and XC-04 in W3 without depending on whether the 409 session is still alive (UNVERIFIED today).
- XC-04 needs master code; the `issue-409-mvp` worktree is on an unmerged branch (`f104ca51a`, `origin/master` not an ancestor: merged-requirements.md line 234), so a master-based worktree fits XC-04 directly.
- No risk to the 409 worktree's unpushed commits and uncommitted records, which must survive until OB-01 (line 264).

## What it costs or risks

<!-- Source: Variant 1 (base) bullet 1 unchanged -->
- A new worktree and agent to create, track and clean up; more coordinator work than reusing an existing session.
<!-- Source: plan Change 5 (Variant 1 advocate Concession 5; merged-requirements.md line 451) -->
- XC-03 alone needs no worktree ("CAP runs no git and no sweep": merged-requirements.md line 451). The worktree's cost is earned at XC-04; creating it for XC-03 too keeps one runner and one record.
<!-- Source: Variant 1 (base) bullet 2, appended per plan Change 4 -->
- The new session has no history with the observer, so it may misread observer output that the 409 session would know. This is reduced, not removed, by the handed field list and the read-only questions to the 409 session in step 3.
<!-- Source: Variant 1 (base), unchanged -->
- If a launched agent's terminal is bound to a Run (D-A), the session must use a different plain terminal or the capture is held.
<!-- Source: Variant 1 (base), updated for consistency with plan Change 1 -->
- The sweep run in XC-04 writes one report file into that worktree's `.dev/sweeps/`; it must be copied into the ledger package before the worktree is removed (step 5), or it is lost with the worktree.

## What stays unresolved

<!-- Source: Variant 1 (base) bullet 1 unchanged; bullet 2 updated for consistency with plan Change 3; bullet 3 added for consistency with plan Change 2 -->
- D-A (does `agent launch` create a Run), which affects step 2.
- Whether the owner names another OB-03 runner in writing; by default the owner runs it.
- Whether a Run-less terminal can list another terminal's non-empty Run (UNVERIFIED until XC-03's first recorded read in step 3).
