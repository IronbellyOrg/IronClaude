# lc19 result: brief guard, case 1: /sc:analyze with a report directory and no --unattended (AC-1.7)

- Worktree setup: PASS (`lc19-worktree.json`, `lc19-branch.txt` = ironbelly/p1-live-guard-case1, `lc19-sync-dev.txt`, `lc19-status-before.txt`; worktree HEAD equals `branch-tip.txt`)
- Section check: PASS (`lc19-unattended-check.txt`: analyze.md:1 analyze.md:1; expected 1 for both copies)
- Step 1: PASS (`lc19-step1.txt`: state ready, 39.053 s)
- Step 2: PASS (`lc19-step2-samples.txt`: 1 sample(s), all agentWait=null)
- Step 3 (replaced), conditions of spec 7.3 AC-1.7:
  - `worker_done` has `--outcome failed`: PASS (`lc19-step3.json`, payload `{"taskId":"task_a2c9926b3e81","dispatchId":"ctx_66e1bd720e23","outcome":"failed"}`, exactly 1 worker_done; acknowledged in `lc19-step3-ack.json`)
  - no `--report-path`: PASS
  - body starts `guard refused:`: PASS. First words of the body: "guard refused: brief lacks --unattended. The Command line '/sc:analyze src/superclaude/cli/install_core.py --report-dir .dev/p1-live/guard1/' has no standalone " (expected `guard refused: brief lacks --unattended`)
  - step 2 never shows `agentWait`: PASS (`lc19-step2-samples.txt`)
- Step 4 (replaced): there is no contract to check; the guard refused before any invocation. The command-not-invoked check is in Step 5 and nothing-written in Step 6.
- Step 5: PASS (`lc19-step5.md`; condition 2 replaced by: `/sc:analyze` was not invoked: PASS; the P0 script crashed on the 0-heartbeat run, counts are in `lc19-session-analysis-supplement.txt`)
- Step 6 (replaced condition: nothing written): PASS (`lc19-step6.md`, `lc19-status-after.txt`, `lc19-index-after.txt`)
- Step 7: PASS (`lc19-step7.txt`)
- Evidence copy: skipped, the guard refused and no report directory was written.
- Remove: PASS (`lc19-remove.json`, `lc19-worktree-list-after.json`, `lc19-head-after.txt`, `lc19-branch-after.txt`)

Overall verdict: PASS

Recording status: complete (verdict recorded, not a task failure)
