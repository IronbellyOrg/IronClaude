You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r1/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r1/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r1/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r1/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N2-01
### N2-01 (MAJOR label, blocking): the P0 gate AC-0.4 cannot pass as written, because step 3 requires the WC-4 contract path
- origin=changed (spec:182 is a changed line). Newly discovered in this review. The clause is older: it is unchanged from spec-v1.md:182, and round1 did not name it.
- Texts. spec:182, the step 3 pass condition: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path." spec:194, AC-0.4 P0: "steps 1-3 and 5-7 pass. In P0, since the contract arrives in P1 (F-03): step 4 is `test -s <report>` ...; Step 3's outcome check in P0 reads the outcome from the report's first status line ...". spec:158 defines P0 as "no command edits", and the P0 runs are the "ready" commands with the stated flags, which do not include `--unattended` (spec:81, spec:91). WC-4 writes the contract only "In unattended mode" (spec:62). The file the troubleshoot run writes is `REPORT.md` (spec:91; `.dev/orca-command-refactor/inventory/commands-b.md:242`, "`report_path` (REPORT.md)").
- Sentence. An implementer who runs AC-0.4 in P0 on `/sc:troubleshoot` follows spec:182 as written: the worker's `worker_done --report-path` must be the WC-4 contract path. No such contract exists in P0 (spec:194 says the contract arrives in P1), so the report path is `REPORT.md`, the clause fails, step 3 fails, AC-0.4 fails, and spec:194 says a P0 failure reopens section 1. This is wrong because the spec's own P0 scope (spec:158) makes the clause impossible to meet in the phase that tests the decision.
- Why the spec:194 override does not cover it. spec:194 overrides step 4 (the YAML parse) and the outcome source in step 3. It does not waive the path clause in step 3.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
