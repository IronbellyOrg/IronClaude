You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### R2-1
### R2-1 (BLOCKING, origin=changed)
- Quoted: AC-0.4 (`orca-worker-contract-spec.md:201`): "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today". Step 3 (`:189`), which AC-0.4 depends on: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Sentence: An implementer who runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` as written must make step 3's outcome match hold. Troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`), and the contract does not exist before P1 (`:201`), so there is no `status` to match. Step 3 cannot pass, and P0 cannot pass.
- Origin: the step 3 text is unchanged from `spec-v1.md`, so the defect is older. It is counted as changed because it quotes the changed AC-0.4 line (`:201`) that depends on it.

### R2-2
### R2-2 (BLOCKING, origin=changed)
- Quoted: WC-4 (`orca-worker-contract-spec.md:62`): "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Against it: the tdd row (`:90`) "`--output <file>`" with report "the TDD at `--output`", and the init-lite row (`:87`) "`--output <file>`". AC-2.2 (`:208`) runs `/sc:tdd "auth" --unattended --output <file>` and checks the contract at `test -s <contract>` (step 4, `:190`).
- Sentence: An implementer who follows WC-4 for `/sc:tdd --unattended --output <file>` must write `<output-dir>/return-contract.yaml`. The flag the brief passes is a file, not a directory, so there is no `<output-dir>` for the coordinator to compute. The contract path is undefined, and AC-2.2 step 4 cannot run for tdd. The same holds for init-lite (`:87`).
- Stated texts that contradict: `:62` (the value is a directory) against `:87` and `:90` (the value is a file).
- Origin: `:62` is changed; `:87` and `:90` are unchanged. The conflict is in `spec-v1.md` at the same rows, so it is an older defect newly found in this review. It is the same class as M10, which named three rows and not these two.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
