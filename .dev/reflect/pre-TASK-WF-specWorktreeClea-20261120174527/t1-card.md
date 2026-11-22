# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-fallback (the orchestrator wrote this card; the plan author is also the executor class, so this card is the part most exposed to self-confirmation and is the reason Tier 2 follows)

Spec: ./source.md (snapshot of the issue 687 spec, 381 lines). Tasklist: TASK-WF-specWorktreeClea-20261120-173546.md (20 tasks, 8 phases, depth deep).

## Coverage

- Pass 1 (labeled IDs by `ID_REGEX`): 0 parsed requirements. The spec labels nothing as R-n, REQ-n, SPEC-n or T-n.
- Pass 2 (quote-pinned inference): 82 inferred rows (`coverage-matrix.md`). Every quote was checked verbatim against its cited line by `artifacts/coverage_match.py`.
- Containment match (threshold 0.6, deterministic): 74 of 82 matched, `coverage_pct_union` 0.9024, `coverage_pct` null (parsed-only is undefined), `S_dev_density` 0.0976.
- Unmapped by the lexical rule: INF-026 (command, not a skill), INF-028 (precheck exits non-zero), INF-035 (first week report only), INF-042 (rule 5 "nothing unsaved"), INF-045 (rule 8 not pinned), INF-048 (never `git worktree prune`), INF-058 (never overwrite a folder), INF-079 (registered where the repo lists commands). The orchestrator believes each is covered in substance (Tasks 14, 18, 18, 6, 6, 2, 9, 15) but the rule is lexical and this belief is unchecked by anyone else.

## Structural signals

- S_scope 20 tasks, S_domains 5 (code, tests, docs, config, infra-like automation), S_dev_density 0.0976.
- Step 1B.2b fired: `inferred_count` 82 is greater than `parsed_count` 0, so `coverage_degraded: parsed-sparse` forbids the Tier 1 stop. Tier 2 is routed by the table-wide pre-filter and by rule 4 (S_domains at least 3).

## Self-identified risks (the orchestrator's own doubts about its plan)

- R1 Order and dependencies. Task 5 (GitHub facts) needs the Orca record from Task 3 and the git record from Task 4; Task 7 (test support) is placed after Task 6 although the fixtures it builds are used by Tasks 3 to 5 only in their acceptance criteria. A reviewer should check that no task's acceptance criteria depend on something a later task creates.
- R2 Scaffolding. Task 2 tells the executor to leave the four verb bodies as stubs that exit 64 until Tasks 11 and 12. The plan says nothing ships as a stub; check that Task 12 really replaces every stub and that its acceptance criteria prove it.
- R3 Safety. The user's run-level safety rule forbids any real removal, any real automation and any push to the evidence repo. Task 1 runs `branch-landed.sh` (which runs `git fetch`) on a real repository and Task 20 runs the script against the real workspace (which runs the same check per worktree through `gh` and `git fetch`). Check whether those are consistent with "dry run only" and with the Constraints section.
- R4 Unbuilt requirement. The spec says `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" with no format. The plan records it as not built (Constraints, Task 12). Check this is an honest reading and not a silent drop.
- R5 Decisions made by the plan where the spec is silent: `/sc:worktrees` on the never-as-worker list (Task 16), the stop outside an IronClaude checkout (Task 14), the default `--out` folder, `/sc:closeout` untouched, the run-evidence pointer prepared as text only (Task 19). Check each for a hidden conflict with a spec section or a pinned test.
- R6 The "never delete a file" constraint (no `unlink`, no `rmtree`, flock lock files left in place, failed scratch folders left in the evidence clone). Check it does not make a spec requirement impossible (for example the archive step 2 "build the folder in a scratch folder" and step 7 repeat runs).
- R7 Test count. The spec asks for about 35 cases in four groups; the plan spreads them over Tasks 7, 8, 10, 13, 18. Check that every bullet of source section 9 lands in some task's body or acceptance criteria.
- R8 Hand-written fixtures for `orca` replies (Task 7) may not match the real Orca output; the only real check is the dry run in Task 20.

## Recommendation

Hand the plan to `/sc:implement` only after a reviewer has confirmed R1, R3 and R7. No change to the plan has been made from this card.

calibration: pending (blind calibration runs in Wave 1D)
