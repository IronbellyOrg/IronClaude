start=06ccf7288c46958c354806c28c54ed8695f301fe tree=f9a8e09099cf9d83ad89dc9d0fe9fa1230ef1524
F1.1 resolved: the blank lines are gone and the `done.json` row now sits directly under the `return-contract.yaml` row in both tables (`docs/swarm/README.md:112-113`, `docs/swarm/command-reference.md:265-266`).

T4.AC1 met. `docs/swarm/README.md:12-14`, `:119-125`, `:127-128`, `command-reference.md:268-277` and `user-guide.md:407-417` describe default publication after the contract and terminal state, with the detached child owning it. They also cover the explicit `false` opt-out and the separate killed marker. Source matches: the foreground path at `src/superclaude/cli/swarm/commands.py:2167-2186` and the resume path at `:2608-2616` both gate on `write_done_sentinel`. A grep of the three files finds no remaining "only kill" or "inline never" statements.

T4.AC2 met. The `done.json` row is in both artifact tables (`README.md:113`, `command-reference.md:266`) with `atomic_write`, `terminal_status` and `contract_path`. Both say completion does not mean every worker succeeded. The default stub count of 13 (`README.md:115-117`) matches `reference-doc-check.txt:221`, which records 13 for the default foreground run.

T4.AC3 met. Early errors, no completed reduction and persistence failure are named as producing no marker (`README.md:123-124`, `command-reference.md:271-273`, `user-guide.md:416-417`). That matches `commands.py:2176-2180`, where the marker needs a contract and an output directory. Resume uses the "effective rehydrated" policy and says an original opt-out is not guaranteed to survive (`README.md:136-138`, `command-reference.md:281-284`). None of the three files claims full detached runtime verification.

T4.AC4 met. `reference-doc-check.txt:222-228` records `25 passed`, exit 0, plus the claim search, table-contiguity checks and link checks. Links in all three files resolve. The diffs touch only the completion passages.

Minor notes (not grading findings):
- `docs/swarm/monitoring-patterns.md:8`, `docs/swarm/observability-procedure.md:23-31`, `:50` and `:104-116` still say `done.json` is not written by a normal run. They sit outside the three files in scope, and the brief says Task 5 owns monitoring and observability.
- `reference-doc-check.txt` holds two appended runs. The first predates the blank-line fix and its line numbers are stale.

Parent: no new findings or checklist yes. Current tables were Read, adjacency and local link checks pass at reference-doc-check.txt:115,163,222; latest pytest outcome is :226. Earlier F2.1 all-no note remains in notes.md for Task 5 to address. The log is append-only evidence, so the earlier line-numbered search remains historical, not a current source citation. Verdict compliant.
