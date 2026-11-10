You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N6
### N6 (blocking, origin=unchanged, depends on changed SPEC:206): the adversarial contract path is stated two ways
- Quoted text A (unchanged, WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62; the same text is in BASE:62).
- Quoted text B (unchanged, adversarial row): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", with the brief column "`--output <dir>`" (SPEC:83; same in BASE:83).
- Dependent changed line: "its direct-route check is AC-1.2, which runs after AC-1.4 fixes the filename" (SPEC:206). AC-1.4 (SPEC:210) only greps for "one fixed path" and names no path, so the filename fix is the SPEC:83 row, not AC-1.4.
- Also relevant: the 7.2 step 3 check requires the worker's `--report-path` to be "the WC-4 contract path in P1 and later" (SPEC:194), and AC-1.2 runs that check on each P1 command (SPEC:208), and adversarial is a P1 command (SPEC:83, SPEC:159).
- Grading sentence: An implementer who follows the adversarial row (SPEC:83) as written writes the contract to `<dir>/adversarial/return-contract.yaml`, and that is wrong because WC-4 (SPEC:62) requires `<dir>/return-contract.yaml` and the AC-1.2 step-3 check (SPEC:194) compares the report path with the WC-4 path, so the check fails for that build. An implementer who follows WC-4 instead contradicts the row. Both texts are stated, neither needs an assumption, and they name different files for the same command.
- Evidence the contract location is not settled: INV-A:60 says real runs wrote the contract in two different places, and INV-A:35 says the skill names no filename. Brainstorm, by contrast, uses `<output>/return-contract.yaml` (SPEC:84), which agrees with WC-4.
- Why this was not caught at review 2: the defect sits on unchanged lines (SPEC:62, SPEC:83) and was not in the review-2 diff scope. It is recorded here as a severe defect newly found by this review, and it comes from the baseline (BASE:62, BASE:83).

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
