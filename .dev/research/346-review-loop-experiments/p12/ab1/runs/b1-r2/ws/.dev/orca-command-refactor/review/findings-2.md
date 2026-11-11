### N1
### N1. AC-1.2 requires a live `--unattended --output <dir>` check on every P1 command, and `load` is a P1 command that now takes neither (blocking)
- Origin: `changed` (the changed lines `spec:112` and `spec:159` make `load` explicitly outside `--unattended`; the unchanged line `spec:196` depends on them). Experts: Wiegers (traceability), Crispin (acceptance criterion cannot pass), Whittaker (Sequence Attack: run the P1 gate in its stated order).
- Stated texts:
  - `spec:159` (changed): P1 Commands cell lists "load (usage line only)", and the same row says the flag and section go "in every command in sections 3.1 and 3.2 except load".
  - `spec:112` (changed): `load` "gets no `## Unattended mode` section", Report "none", "not as its own Task".
  - `spec:196` (unchanged, AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`", pass condition "all steps pass".
  - `spec:182-183` (7.2 steps 3-4; `spec:182` changed): step 3 needs a `worker_done` whose report path is the contract path WC-4 gives; step 4 runs `test -s <contract>` and a YAML assertion on `status` and `command`.
  - `spec:167`: "A phase passes only when every check in its block and every common check passes."
- Grading sentence: An implementer who follows the stated text as written runs the 7.2 check on `load` with `--unattended --output <dir>` (`spec:196`, because `spec:159` lists `load` as a P1 command), and builds `load` with no `--unattended` flag, no section and no contract (`spec:112`, `spec:159`, `spec:265`). That is wrong because step 4 (`spec:183`) has no contract to open, step 3 has no contract path, so AC-1.2 fails, and by `spec:167` the P1 gate cannot pass; the only way to pass is to give `load` a contract, which `spec:265` rejects.
- Concrete attack (Whittaker, Sequence): state before: P1 edits done, `load` has the usage-line fix only. Steps: dispatch `/sc:load --unattended --output out/`; the worker ends with no report file. State after: `out/return-contract.yaml` absent, `test -s` exits 1, AC-1.2 red, P2 never starts (`spec:154`).
