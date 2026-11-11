You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r4/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r4/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r4/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r4/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### F-1
### F-1 (blocking, CRITICAL). WC-4's contract path rule contradicts the briefs and fixes that the spec itself gives
- Stated texts that disagree:
  - SPEC:62: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:73: "the output directory, so the report path is known before dispatch (WC-4)".
  - SPEC:87 and SPEC:90: init-lite and tdd briefs pass "`--output <file>`" (a file). SPEC:200 (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked` with a non-empty `blocked_question`".
  - SPEC:83: adversarial contract fixed to `<output>/adversarial/return-contract.yaml`, but WC-4 says `<output-dir>/return-contract.yaml`.
  - SPEC:92: workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, and the row passes no output directory. INV-B:272 says that contract is not written for pre-creation stops (`refs/return-contract.md:39`), so the spec's own fix "Write the contract for pre-creation STOPs too" (SPEC:92) has no `<id>` directory to write it into.
  - SPEC:182 and SPEC:183: step 3 requires "its report path is the WC-4 contract path"; step 4 runs `test -s <contract>`.

### F-2
### F-2 (blocking, MAJOR with concrete wrong outcome). AC-1.1 and the P1 scope require a contract for `/sc:load`, which the spec says gets none
- Stated texts that disagree:
  - SPEC:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; same row: "The WC-4 contract in unattended mode".
  - SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - SPEC:76: "Every changed command also gains the `## Unattended mode` section".
  - SPEC:112 (load row): report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:265 (Decision): "a report file would be an unrequested addition".
  - SPEC:154: "Later phases do not start until the earlier phase's checks in section 7 pass."

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
