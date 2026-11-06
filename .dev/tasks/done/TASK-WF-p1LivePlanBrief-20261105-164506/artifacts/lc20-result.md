# lc20 result: brief guard, case 2: /sc:troubleshoot has no Unattended mode section and the flag is present (AC-1.7)

- Worktree setup: PASS (`lc20-worktree.json`, `lc20-branch.txt` = ironbelly/p1-live-guard-case2, `lc20-sync-dev.txt`, `lc20-status-before.txt`; worktree HEAD equals `branch-tip.txt`)
- Section check: PASS (`lc20-unattended-check.txt`: troubleshoot.md:0 troubleshoot.md:0; expected 0 for both copies)
- Step 1: PASS (`lc20-step1.txt`: state ready, 38.832 s)
- Step 2: PASS (`lc20-step2-samples.txt`: 1 sample(s), all agentWait=null)
- Step 3 (replaced), conditions of spec 7.3 AC-1.7:
  - `worker_done` has `--outcome failed`: PASS (`lc20-step3.json`, payload `{"taskId":"task_6b5b3d8f75d5","dispatchId":"ctx_5aba83649960","outcome":"failed"}`, exactly 1 worker_done; acknowledged in `lc20-step3-ack.json`)
  - no `--report-path`: PASS
  - body starts `guard refused:`: PASS. First words of the body: "guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale). I checked the one Command: line (/sc:tr" (expected `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`)
  - step 2 never shows `agentWait`: PASS (`lc20-step2-samples.txt`)
- Step 4 (replaced): there is no contract to check; the guard refused before any invocation. The command-not-invoked check is in Step 5 and nothing-written in Step 6.
- Step 5: PASS (`lc20-step5.md`; condition 2 replaced by: `/sc:troubleshoot` was not invoked: PASS; the P0 script crashed on the 0-heartbeat run, counts are in `lc20-session-analysis-supplement.txt`)
- Step 6 (replaced condition: nothing written): PASS (`lc20-step6.md`, `lc20-status-after.txt`, `lc20-index-after.txt`)
- Step 7: PASS (`lc20-step7.txt`)
- Evidence copy: skipped, the guard refused and no report directory was written.
- Remove: PASS (`lc20-remove.json`, `lc20-worktree-list-after.json`, `lc20-head-after.txt`, `lc20-branch-after.txt`)

Overall verdict: PASS

Recording status: complete (verdict recorded, not a task failure)
