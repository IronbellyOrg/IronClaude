# Diagnosability Tasklist
**Issue**: Agents run orca worktree create without --agent, leaving empty plain terminals
**Verdict**: partial  **Complexity**: trivial  **failing_component**: CLAUDE.md:303-325 (+ Orca create path, external)  **Round**: 1 of 3  **re-run permitted**: unknown  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: ironbelly/fix-flaky-parallel-thread-test  **repro-venue-id**: orca-orchestrator-spawn-session-surface (same defect family as the prior run; digits stripped)

## Emitter search
emitter-search: n/a (no single-expression predicate; the datum is a tab start recorded by Orca, already captured)
emitters-found: 1 (external: ~/.config/orca/logs/daemon.log `startup-command-delivery` rows; in-repo: orca_worktree.py:174 print, which does not carry terminal data)
already-read-files: 3 (daemon.log, transcripts under ~/.claude/projects, `orca terminal list --json` output)
usable-capture-routes: 2 (read-only: daemon.log jq; `orca terminal list --worktree <sel> --json`)
Exclusions: orca_worktree.py create output at :608 is dropped on success (production source; not an edit site).

## Discriminator rows
core-rows=3, pack-rows=0, total-rows=3. comparator: n/a (discriminator-required: no; single producer for the scoped symptom; SAME-ENV yes).
| ID | role | claim | observable | probe | value-if-true | value-if-false | outcome mapping | provenance | state |
|---|---|---|---|---|---|---|---|---|---|
| M-SEED | core | A create without --agent always seeds one plain tab | daemon `hasCommand=false` row 2-3 s after each bare create | jq over daemon.log per worktree name | a false row for every bare-created worktree | no false row | true=consistent, false=refuted | tier1-observation.md N6, N8 | observed: 7 of 7 bare-created worktrees checked show it (consistent) |
| M-REUSE | core | A later launch does not reuse the seeded tab | a separate `hasCommand=true` row after the false row, and the plain tab still separate | jq over daemon.log | separate true row | the false row is the only row and later carries the agent | true=consistent, false=refuted | N8 (5 hand-off worktrees) | observed: 5 of 5 consistent |
| M-CTRL | control | A create whose caller provides the surface seeds no plain tab | no false row | jq over daemon.log | no false row | a false row | true=consistent, false=refuted | N8 (issue-473-claim, issue-331-github-issue-watcher, sc-issue-claim-pipeline-flag) | observed: consistent. issue-473-claim was created by `worker-start --worktree new-top-level --agent claude` (N10). CONTROL-PROOF: yes: /home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:265 (local checkout) |

## Fix candidate
Proposal only, subject to `--fix` and explicit confirmation: tell agents what to do with the seeded tab (see REPORT.md Proposed Fix). Paired verification: rows V-CLOSE and V-JSON below.

Pending fix-verification rows (not diagnosis inputs; need a worktree create, which is a mutation, so they stay pending until authorized):
- V-CLOSE: after a bare create, `orca terminal close --worktree path:<p> --all --json` removes the seeded tab and nothing else; value-if-works: `orca terminal list --worktree path:<p> --json` returns zero terminals and the worktree still appears in `orca worktree list`; value-if-not: a terminal remains or the worktree disappears. Pending: re-run permitted unknown.
- V-JSON: whether a bare `orca worktree create --json` result names the seeded terminal handle (would allow closing exactly that handle). value-if-yes: a `term_` handle in the result; value-if-no: none. Pending: same reason. (N5: the captured tail shows none; head not captured.)

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
None required for diagnosis: the datum is already captured by Orca's daemon log and the transcripts.

## Verification
M-SEED, M-REUSE, M-CTRL are observed from captured files (tier1-observation.md N6, N8). V-CLOSE and V-JSON verify the fix and remain pending.

## Rollback
No instrumentation added.

## Patch-round counter
Identity ironbelly/fix-flaky-parallel-thread-test : orca-orchestrator-spawn-session-surface. Authoritative /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/diagnosability-rounds.json value 1, not incremented (discriminator-required: no). Snapshot: diagnosability-rounds.json in this directory.
