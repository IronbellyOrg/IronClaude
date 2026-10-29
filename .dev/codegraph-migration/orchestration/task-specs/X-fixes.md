Task X: apply the two open IMPORTANT defects from the final check, then re-pin the ledgers.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding). Then read `.dev/codegraph-migration/FINAL-SUMMARY.md` section 6 (rows Q-I1 and Q-I2) and the lines it cites.

Target and change:
1. Q-I1 (Phase 1). In `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` Task 12 criterion 3, and in the same command in `.dev/codegraph-migration/specs/phase-1-removal-spec.md` (T10b acceptance) and the package `source.md`: keep only the five memory names (`write_memory|read_memory|list_memories|edit_memory|delete_memory`), add the four `-g` exclusions given in Q-I1's Fix column, and add one sentence that the full-token repo-wide check is Task 15's `acceptance-search.sh`. First run the revised command against today's tree and confirm that every remaining hit is in a file a Task 13-15 step deletes or rewrites (list them in your result); if a hit is not, adjust the exclusions and say why.
2. Q-I2 (Phase 3). In `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` Task 13 criterion 4, and in spec `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` T11 (5) and (6) and the package `source.md`: add `-g '!**/core/CODEGRAPH.md'` to both rg commands.
3. Keep each package's `source.md` byte-identical to its spec (`cmp` must print nothing) and rewrite the `PLAN:` line in each `progress.md` with the new `sha256=` of the plan file and `source_sha256=` of `source.md` (format exactly as the existing line; use `sha256sum`).
4. Update `.dev/codegraph-migration/FINAL-SUMMARY.md` section 6: set Q-I1 and Q-I2 Status to FIXED with a one-line note naming the files changed. Do not change verdicts; the re-check task does that.
5. Write `.dev/codegraph-migration/review/X-fixes-result.md`: what changed (file and line), the `cmp` and `sha256sum` outputs, and the hit list from step 1.

Constraints: edit nothing else. No source edits, no commits, no staging.

Ownership: the two plans, two specs, two `source.md`, two `progress.md`, FINAL-SUMMARY.md section 6 status cells, and X-fixes-result.md.

Observable acceptance: `cmp` of each spec with its `source.md` prints nothing; each `progress.md` PLAN line matches `sha256sum` of its plan and source; both rg commands in Q-I2, run as revised, print no hit in `CODEGRAPH.md` files.
