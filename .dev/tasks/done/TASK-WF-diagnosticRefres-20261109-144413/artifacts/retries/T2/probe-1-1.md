c5d741ea37613a64f6604fc4a30c3edb4fd13521
family=verify-sync-not-passing (covers F1.1 of review-1.md)
defect: the task outcome and readiness text claim or imply that read-only sync verification passed while make verify-sync exited non-zero.
command: grep -n -E 'Drift detected|DIFFERS|Error 1' verify-sync.log
before:
22:  ⚠️  DIFFERS: sc-issue-protocol
223:❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
224:make: *** [Makefile:168: verify-sync] Error 1
coupled sites: compatibility-review.json:12,32-33 (verdict and verify_sync_blocks_readiness); the Task 2 ledger complete line; /tmp/orch-status-20261109/exec-441-b.md; the worker_done body.
after: the same three lines remain (22, 223, 224) because the failure is real. No text says it passed: task2-outcome.md and compatibility-review.json:32-33 disclose it, and the owner accepted the gap (Ruling, owner reply 2026-11-10T04:59Z). The verdict stays non-compliant.
family=missing-preinstall-recheck (covers F1.2 of review-1.md)
defect: no saved evidence of the immediate pre-install recheck required by the plan (Task 2, line 43).
command: grep -n -E 'all_prerequisites_unchanged|backup_reverified' guard-before-install.json
before: (guard-before-install.json did not exist; the grep found no file)
coupled sites: selective-install.json (install at 00:18:27Z); compatibility_state.py:374-384 (guard phase); before-rerun.log:1 (last saved check, 00:09:09).
after: 6:  "guard_output_verbatim": "{\"phase\": \"guard\", \"all_prerequisites_unchanged\": true, \"backup_reverified\": true}" (recorded after the fact, as task2-outcome.md says)
family=tasks-not-staged (covers F1.3 of review-1.md)
defect: .dev/tasks artifacts untracked or modified-after-stage.
command: none (git index state, not a grep-form search): re-check item for every later review. Check with git status --short .dev/tasks and git diff --cached --name-only | grep -E '^\.claude/'.
before: 7 untracked artifacts plus AM files (see review-1.md F1.3).
coupled sites: the archive step (re-run git add .dev/tasks afterwards); any ledger edit.
after: after git add .dev/tasks, git status --short .dev/tasks shows no untracked and no AM lines, and the staged .claude/ list is empty.
