# Revise 1

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place)
ids repaired: M1, M2, M4, M5, M6 (confirmed in review/round1.md "Reviser brief"). M3 and M7 left alone (verifier-rejected, round1.md "Noted, unactioned").
Not run: spec-panel. No self-awarded PASS.

## Byte accounting

Size before: 57763 bytes. Size after: 58587 bytes. Net +824.

| id | bytes added | bytes deleted |
|---|---|---|
| M1 and M6 (shared edits, counted once; see note) | 340 | 56 |
| M2 | 111 | 73 |
| M4 | 71 | 12 |
| M5 | 537 | 94 |
| total | 1059 | 235 |

Note: M1 and M6 name the same defect (AC-1.1 vs the `load` row, `spec:195` vs `spec:112`), so one set of four edits repairs both; their bytes are counted once under M1/M6. Added/deleted bytes are measured after trimming each replaced string's common prefix and suffix. Check: 57763 + 1059 - 235 = 58587.

## One row per finding

| id | disposition | where applied (spec line numbers are of the revised file) | reason / citation |
|---|---|---|---|
| M1 | applied (narrowed, nothing new added) | Section 3 intro (line 76): "Every changed command except `/sc:load`..."; P1 scope (line 159): the `--unattended` flag limited to 3.1/3.2 commands that section 3 assigns to a phase, except load; AC-1.1 (line 195): asserts the section only for rows with phase P1-P3, excluding load and the unphased brainstorm and init-lite; AC-1.2 (line 196): "except `/sc:load`" | Finding text: brainstorm and init-lite carry "None" small fix and no phase (spec rows 84, 87; phase lists at 158-162), so AC-1.1's "every command" could not pass. Narrowing the assertion to commands with an assigned phase is the narrower of the two recommended edits (round1.md M1.a recommendation). AC-1.2 also excluded load because `test -s` on a contract the load row says is never written (row 112) could not pass. |
| M2 | applied | Section 3.1 adversarial row (line 83): contract path fixed to `<output>/return-contract.yaml`; AC-1.4 (line 198): names that one path | Picks the WC-4 path (spec WC-4, line 62) as the one path, so the 7.2 step 4 `test -s <contract>` (line 183) holds. Evidence of the drift this fixes: `inventory/commands-a.md:60` (two on-disk locations, the second nested `adversarial/adversarial/`). The skill itself names no file (`inventory/commands-a.md:60`, citing `SKILL.md:427,429`; skill file not in workspace, so that citation is UNVERIFIED here). |
| M4 | applied | AC-C5 (line 176): `grep '^-' \| grep -v '^--- a/'` replaces `grep -E '^-[^-]'` | The old regex skips removed lines starting with `-` (a deleted bullet shows as `-- foo`), as demonstrated in round1.md M4.a. The new pipeline prints every removed line except the `--- a/<file>` header. AC-0.3 (line 193) uses the old regex but M4 states it is unaffected (round1.md M4.a, last sentence), so left alone. |
| M5 | applied | WC-4 (line 62): `<output-dir>` is the containing directory when the flag takes a file (tdd, init-lite); fixed or generated directories are named in the section 3 row and the worker reports the path in `--report-path`. cleanup-audit row (line 85): contract at fixed `.claude-audit/return-contract.yaml`. workflow row (line 92): report cell notes the generated id and that the worker reports the path; pre-creation STOPs write the fixed `.dev/tasks/to-do/return-contract.yaml` | Per the recommendation in round1.md M5.a. Evidence: workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml` and does not write it for pre-creation STOPs (`inventory/commands-b.md:272-273`, citing `refs/return-contract.md:3-19,39,41`); cleanup-audit's directory is fixed (`inventory/commands-a.md:42,107`); tdd writes to `--output` as a file (`inventory/commands-b.md:222`). The two fixed paths are choices made here to satisfy "known before dispatch"; parallel workflow pre-creation stops in one worktree would share that file (WC-11 interaction, UNVERIFIED, not addressed as no finding calls for it). |
| M6 | applied together with M1 | Same four edits as M1 (lines 76, 159, 195, 196) | The narrower edit round1.md M6.a prefers: load excluded from AC-1.1, the "none" decision (line 265) kept unchanged. |

## Left alone
Medium and minor findings, M3, M7, and the three source reports' follow-up candidates.
