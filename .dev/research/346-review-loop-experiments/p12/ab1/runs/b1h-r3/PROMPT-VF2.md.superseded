You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### B1
### B1 (= M8, open). The load row gives a contract that WC-4 does not allow, and the phase rows say the contract is not added
- Origin: changed (spec:112 is on a changed line; spec:268 is on a changed line).
- Issue, three conflicting texts:
  1. WC-4 says the contract "carries at least" `status`, `command`, `report_path` (if any), `artifacts` (every other file written) and, when blocked, `blocked_question` (spec:62). The load row writes "status-only contract ... (`status`, `command`; no `report_path`, as WC-4 allows)" (spec:112). `artifacts` is required by WC-4 and is absent from the row, so the row contradicts WC-4 on a field WC-4 does not make optional.
  2. The Decisions row says the status-only contract "meets WC-4 and AC-1.1" (spec:268). Point 1 shows it does not meet WC-4.
  3. The load row keeps "P1 (usage line only)" (spec:112, Phase column), and the P1 scope lists "load (usage line only)" (spec:159). An implementer who follows P1 adds no Unattended-mode section and no contract for load, so AC-1.1 (spec:196), which requires such a section for every command in 3.1 and 3.2, fails for load.
- Sentence that holds with no further assumption: an implementer who follows the load row writes a contract with `status` and `command` only, and WC-4 (spec:62) says it must also carry `artifacts`; an implementer who follows the P1 phase text adds nothing for load, and AC-1.1 (spec:196) then fails.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
