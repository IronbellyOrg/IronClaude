### F-01
### F-01 (CRITICAL, blocking): P0 acceptance check AC-0.4 cannot pass, and P0 gates every later phase
- Quoted texts and locations:
  - `spec:158`: P0 is "(no command edits)".
  - `spec:154`: "Later phases do not start until the earlier phase's checks in section 7 pass."
  - `spec:182` (7.2 step 3) pass condition: "exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
  - `spec:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
  - `spec:91-92`: the P0 commands report `REPORT.md` (troubleshoot) and `.dev/tasks/to-do/<id>/return-contract.yaml` (workflow); `INV-B:242` says troubleshoot writes `return-contract.yaml` only with `--caller task-unified`.
- Grading sentence: An implementer who follows AC-0.4 and step 3 as written runs the three P0 smoke runs on unedited commands, and the check can never pass, because step 3 is required to pass and demands a WC-4 contract and a contract `status` that P0 commands do not write until P1; only step 4 is carved out. Since `spec:154` forbids starting P1 until P0 passes, the whole rollout is blocked, and `spec:194` says a failure "reopens section 1".

### F-02
### F-02 (CRITICAL, blocking): AC-1.1 requires an `## Unattended mode` section naming `return-contract.yaml` in commands the spec says get no contract or no change
- Quoted texts and locations:
  - `spec:195` (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:112`: load row: report "none (see note)", resume "n/a", "P1 (usage line only)".
  - `spec:265` (Decisions): load: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - `spec:79`: 3.1 intro: "The only command changes are the small fixes in the last column"; `spec:84` and `spec:87` give "None" for brainstorm and init-lite.
- Grading sentence: An implementer who follows AC-1.1 as written adds an `## Unattended mode` section naming `return-contract.yaml` to `load.md` (and to brainstorm and init-lite), and that is wrong because the same document says load gets no report file and only a usage-line fix, and that the ready commands change only through the "small fix" column; if the implementer follows those rows instead, AC-1.1 fails. The two stated texts cannot both be satisfied.

### F-03
### F-03 (CRITICAL, blocking): WC-4 fixes one contract path, but the adversarial and workflow rows and the live check use other paths
- Quoted texts and locations:
  - `spec:62` (WC-4): the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - `spec:83`: adversarial: brief passes `--output <dir>`; fix is "the contract filename to `<output>/adversarial/return-contract.yaml`"; `spec:198` (AC-1.4) checks that adversarial "names one fixed path".
  - `spec:92`: workflow: brief passes `--handoff none` (no output flag); report is `.dev/tasks/to-do/<id>/return-contract.yaml`, an id the command generates.
  - `spec:182` (step 3) and `spec:196` (AC-1.2): the worker's report path must be "the WC-4 contract path" for each P1 command.
- Grading sentence: An implementer who follows WC-4 puts adversarial's contract at `<dir>/return-contract.yaml`, while the adversarial row and AC-1.4 put it at `<dir>/adversarial/return-contract.yaml`; for workflow there is no coordinator-passed directory at all and the id is created by the command. AC-1.2 step 3 then requires the worker's report path to equal the WC-4 path, which one of the two stated paths cannot meet. Two stated texts contradict each other on the path of the same file, and the file's path is what the coordinator opens (`spec:62`, `spec:73`).
