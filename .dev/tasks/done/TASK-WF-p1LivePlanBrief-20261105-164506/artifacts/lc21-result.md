# lc21 result: brief guard, case 3: /sc:help is on the never-as-worker list (AC-1.7)

- Worktree setup: PASS (`lc21-worktree.json`, `lc21-branch.txt` = ironbelly/p1-live-guard-case3, `lc21-sync-dev.txt`, `lc21-status-before.txt`; worktree HEAD equals `branch-tip.txt`)
- Section check: not made (case 3 is decided by the command name alone)
- Step 1: PASS (`lc21-step1.txt`: state ready, 38.571 s)
- Step 2: PASS (`lc21-step2-samples.txt`: 1 sample(s), all agentWait=null)
- Step 3 (replaced), conditions of spec 7.3 AC-1.7:
  - `worker_done` has `--outcome failed`: PASS (`lc21-step3.json`, payload `{"taskId":"task_d3ff69bd9a2a","dispatchId":"ctx_284755bb7e4f","outcome":"failed"}`, exactly 1 worker_done; acknowledged in `lc21-step3-ack.json`)
  - no `--report-path`: PASS
  - body starts `guard refused:`: PASS. First words of the body: "guard refused: /sc:help is on the never-as-worker list in ~/.claude/WORKER-CONTRACT.md (section 1, case 3), so it is never dispatched as a worker and has no --u" (expected `guard refused:`)
  - step 2 never shows `agentWait`: PASS (`lc21-step2-samples.txt`)
- Step 4 (replaced): not applicable, so no PASS or FAIL mark of its own: there is no contract to check; the guard refused before any invocation. The command-not-invoked check is in Step 5 and nothing-written in Step 6.
- Step 5: PASS (`lc21-step5.md`; condition 2 replaced by: `/sc:help` was not invoked: PASS; the P0 script crashed on the 0-heartbeat run, counts are in `lc21-session-analysis-supplement.txt`)
- Step 6 (replaced condition: nothing written): PASS (`lc21-step6.md`, `lc21-status-after.txt`, `lc21-index-after.txt`)
- Step 7: PASS (`lc21-step7.txt`)
- Evidence copy: skipped, the guard refused and no report directory was written.
- Remove: PASS (`lc21-remove.json`, `lc21-worktree-list-after.json`, `lc21-head-after.txt`, `lc21-branch-after.txt`)

Overall verdict: PASS

Recording status: complete (verdict recorded, not a task failure)
