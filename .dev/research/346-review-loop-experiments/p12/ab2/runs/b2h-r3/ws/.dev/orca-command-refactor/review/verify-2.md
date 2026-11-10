# Verification 2: N-1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `bfe20373dae030b64d0ab846cde01958172f4f46786bcfbad746ac335c6b4df6`

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| N-1 | SPEC:62 (WC-4): "F-02: a file-valued output (`--output <file>`, as in tdd and init-lite; `INV-B:47`, `INV-A:55`) uses the file's parent directory as `<output-dir>`." Same line: the contract is "`<output-dir>/return-contract.yaml`", and "The worker passes the contract path as `worker_done --report-path`". SPEC:87 (init-lite): "Contract at `<parent of --output>/return-contract.yaml` (P1; F-02, F-04)" and "Fresh `--output` per attempt under `--unattended` (WC-6, F-03)". SPEC:69 (WC-11): "Two workers in one worktree must never write the same file." SPEC:64 (WC-6): "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output." SPEC:90 (tdd): "`--output <file>`". | yes | yes | confirm | Two init-lite runs `--output docs/a.md` and `--output docs/b.md` both resolve to `docs/return-contract.yaml` by SPEC:62 and SPEC:87, and both `worker_done` messages carry that one path, so the second write replaces the first contract. That conflicts with the candidate's own WC-11 rule (SPEC:69), and the spec has no rule that gives the contracts distinct names. The data-loss step needs only the ordinary overwrite of one file. The WC-6 cite is a stated rule about "output", not the contract, so it is supporting only. The tdd case follows the same way from SPEC:90 and WC-4. The fixed `--output` in SPEC:87 does not change the contract path while the directory stays the same, which the finding states correctly. |

confirmed: N-1
