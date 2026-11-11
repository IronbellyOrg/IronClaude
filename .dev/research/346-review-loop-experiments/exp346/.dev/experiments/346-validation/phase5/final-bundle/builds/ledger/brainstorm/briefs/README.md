# S1 brief templates for the ledger arm (issue 346, theme ledger)

Source of the originals (read-only, owner-supplied): `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/task-text/`. Each file here keeps its original name. The coordinator's inserted ledger steps, which run every script write between these briefs, are in `ledger-steps/` (see its `README.md`).

## What changed against each original

| File | Change against the original |
|---|---|
| `T05-R1-reviewer-L11-699ae853.txt` | One substitution on the run line: `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed`; every other byte unchanged. |
| `T06-R1-reviser-L10-3bb70411.txt` | Unchanged (byte copy). |
| `T07-R2-reviewer-L11-aff19d65.txt` | The same one substitution on its `(3) run /sc:spec-panel ...` run line; every other byte unchanged, including "any finding of any severity is FAIL". |
| `T08-R2-reviser-L10-66468bab.txt` | Unchanged (byte copy). |
| `T09-R3-reviewer-L11-1c9a7ec8.txt` | The same one substitution on its `(3) run /sc:spec-panel ...` run line; every other byte unchanged, including "any finding of any severity is FAIL". |
| `T10-R3-reviser-L10-458bdc00.txt` | Unchanged (byte copy). In the ledger arm review 3 always ends the loop (PASS or ESCALATE), so T10 is not dispatched, as in Arm B (verbatim briefs T05 to T09). |
| `T09b-sweep-dispatch.txt` | Inserted brief, built from `T09-R3-reviewer-L11-1c9a7ec8.txt` (see below). |

The substituted run line in T05, T07 and T09 reads, in full:

```text
/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture
```

## Owner rulings (2026-11-08)

- The S1 review-3 brief text stays verbatim, including "any finding of any severity is FAIL". Replacing `/sc:spec-panel` with `/sc:spec-panel-ledger` and adding only the arguments the SPEC requires (`--ledger <dir>`, `--revert-unclaimed`) is the variant mechanism, not an edit of the brief text. Reviser briefs stay verbatim.
- A flag in a brief is explicit consent for one scripted edit or revert: `--revert-unclaimed` on the T07 or T09 run line is copied onto the one `begin` the ledger step runs before that review (`ledger-steps/L-begin.txt`) and is never stored.
- Review and reviser sessions never run a script call that writes a file. Every write (`init`, `find`, `answer`, `begin` with its scripted revert, `verify`, `close`, `sweep`) is a coordinator ledger step with its own brief template in `ledger-steps/`. Review and reviser sessions may run only calls that write no file (`status`, `verdict`, `--dry-run`); a reviser may put its answer claims in one `ledger-input` block inside its own disposition file.

## T09b-sweep-dispatch.txt

Used only when the sweep smoke check does not show that a dispatched worker can spawn an Agent-tool subagent and keep sending its 5-minute heartbeat through a subagent run longer than 5 minutes. It is then the sixth dispatch (after `ledger-steps/L-sweep-prepare.txt`, before `ledger-steps/L-sweep-ingest.txt`) and is declared as a deviation. Built from `T09-R3-reviewer-L11-1c9a7ec8.txt` with these parts replaced; everything from "Ownership:" to the end is the T09 text unchanged:

| Replaced in T09 | Replaced by |
|---|---|
| Task number sentence: "Task 9, independent re-review round 3. You did not write or revise the spec; assume defects remain and look for them." | the single run line `Run: /sc:spec-panel-ledger @<sweep copy path> --mode critique --focus requirements,architecture --sweep .` |
| Inputs: "Inputs: the spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, review/spec-panel-round2.md, review/disposition-round2.md, inventories." | (removed; the run line names the only input, the sweep copy) |
| Change list: "Change: (1) for each round-2 finding N1-N13 ... (2) re-read every path:line citation ... (3) run /sc:spec-panel ... for new defects, including any introduced by this revision." | (removed) |
| Output file `.dev/orca-command-refactor/review/spec-panel-round3.md` | `.dev/orca-command-refactor/review/spec-panel-sweep.md` (a placeholder name the coordinator may change); the rest of the T09 Output sentence is kept |

`<sweep copy path>` is the path `sweep --prepare` printed (`ledger-steps/L-sweep-prepare.txt`). The sweep never opens the ledger folder, so the line carries no `--ledger`.

## Values the coordinator fills at dispatch time

As Arm B did (examples: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/arm-b-briefs/filled-flg-r1-T07.txt`, `filled-flg-r1-T08.txt`, `filled-flg-r1-T09.txt`, read-only), these per-replicate values are substituted at dispatch time and are not brief edits:

- finding counts and ids of the replicate's own reports: "24 round-1 findings" (T07); "N1-N13" (T08, T09); "the 2 overstated citations" and "both citations" (T08) and "both overstated citations" (T09), which Arm B filled as "every overstated citation"; and the M1-M14 list, byte count and frozen-copy name of T10 if it were dispatched;
- the repo root `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` (replaced by the replicate's worktree);
- `<sweep copy path>` in `T09b-sweep-dispatch.txt`.
