### ARCH-1 (blocking, CRITICAL, Fowler lead, Whittaker attack W2): WC-4 and WC-6 contradict on where a retry writes

Where: `spec:62` (WC-4), `spec:64` (WC-6), `spec:73` (2.3), the "Fresh dir" cells of `spec:88-91` and `spec:99-125`, `CAPS:80`, `CAPS:90`, `CAPS:116`.

Text as written:
- WC-4: the contract is `<output-dir>/return-contract.yaml`, in the directory the coordinator passed, and the path is "known before dispatch" (`spec:62`, `spec:73`).
- WC-6: a retry worker "must not corrupt the first attempt's output"; a command with no resume flag "writes each run into a fresh output directory so a re-run starts clean" (`spec:64`). About 25 rows say "Fresh dir".
- Orca's own model: a worker that ends `failed` (which is what a `blocked` report maps to, `spec:63`) leaves its Task `failed` and its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`, `CAPS:116`). So a retry after every `blocked` outcome is the normal path the spec designs for. Nothing in section 2.3 or section 7 says the coordinator must pass a new directory on a retry, and no acceptance check exercises `--retry-of`.

Grading check: An implementer who follows the stated text as written builds commands that, when the retry brief repeats the same `--output <dir>`, either write into `<dir>` (overwriting the first attempt's `return-contract.yaml` and artifacts, which WC-6 forbids) or create a new directory (so the contract is not at the path the coordinator knew before dispatch, which WC-4 requires); one of the two requirements must be broken, and the coordinator's step 4 (`test -s <contract>`, `spec:183`) then reads the first attempt's stale `blocked` contract as the retry's result, which is wrong because the retry may have succeeded.

State trace: Task T1, dispatch d1 `--output D` -> `D/return-contract.yaml {status: blocked}`; d2 `--retry-of d1 --output D` -> WC-6 "fresh dir" vs WC-4 "D". If d2 writes `D2/...`, the coordinator reads `D/...` (blocked) and marks a good run failed. Counts: 1 Task, 2 dispatches, 1 expected contract path, 2 real contract files (Quantity Flow Diagram above).

Recommendation (narrowing): in section 2.3 require the coordinator to pass a distinct `<output-dir>` per dispatch (one sentence), and reword WC-6 so "fresh output directory" means "the directory the coordinator passes for that dispatch". Add one retry case to the P2 gate-trigger check (AC-2.2).
