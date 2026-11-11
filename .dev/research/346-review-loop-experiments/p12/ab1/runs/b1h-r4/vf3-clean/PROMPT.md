You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf3-clean. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf3-clean/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf3-clean/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf3-clean/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N3
### N3 (blocking, origin=changed): the revised init-lite row makes `--output` a file under `--unattended`, but WC-4 defines `--output` as the output directory
- Location: `candidate:86` (changed line); conflicting text `candidate:62` (WC-4, unchanged); `candidate:73` (2.3, unchanged).
- Stated texts:
  - `candidate:62` (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)." The only exception in WC-4 names a different contract path ("Where section 3 names a different fixed path for a command, that path is the contract path instead"). It does not allow `--output` to name a file.
  - `candidate:73` (2.3): the brief passes "the output directory, so the report path is known before dispatch (WC-4)".
  - `candidate:86`: "`--unattended --output <dir>/context-audit.md` ... (`<dir>` is the WC-4 output directory, so the contract is `<dir>/return-contract.yaml`)". Under this row the value passed by `--output` is a file, not a directory.
- Grading sentence: An implementer who follows `candidate:62` as written takes the value passed by `--output` as `<output-dir>`. For the init-lite brief that value is `<dir>/context-audit.md`, so the contract is written at `<dir>/context-audit.md/return-contract.yaml`. The coordinator opens `<dir>/return-contract.yaml`, as `candidate:86` and `candidate:73` direct it to. It finds no report, and `candidate:63` (WC-5) maps the missing report to `failed` for a run that did its work. Two stated texts contradict each other on what `--output` names for this command, and the only stated exception does not cover it.

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
