You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r5/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r5/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r5/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r5/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

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

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
