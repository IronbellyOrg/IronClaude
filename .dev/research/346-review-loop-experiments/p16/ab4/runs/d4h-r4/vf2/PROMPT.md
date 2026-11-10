You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r4/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### M4
### M4 (open, blocking): AC-0.4 step 4 still has no path for adversarial
- Candidate text: "step 4 is `test -s` on that report" for `/sc:adversarial --compare <two files> --depth quick --output <dir>` (SPEC:206). The P0 form of step 3 also checks "the report path against the command's existing report" (SPEC:194, SPEC:206).
- Grading sentence: An implementer who runs AC-0.4 on adversarial in P0 must pick the file that `test -s` checks, because the spec names none. INV-A:35 and INV-A:60 say the skill "names no filename" and that the contract location has varied between runs. X is wrong because the criterion cannot be evaluated as written for adversarial, and that does not require any assumption beyond the spec's own text.

### N1
### N1 (blocking, origin=changed): AC-1.1 requires P2-P4 commands to have sections in P1
- Quoted text: "the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` ..." (SPEC:207). The "except `load`" clause is the changed part. The rest of the sentence is inherited from BASE:195.
- Conflict: P1 scope (SPEC:159) adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". It adds the section only for the ten 3.1 commands (SPEC:79). Eighteen of the 27 section 3.2 rows are phased P2 to P4 (SPEC:100 auggie-review P2, SPEC:109 implement P4, SPEC:118 roadmap P3, SPEC:124 validate-roadmap P3, and the others in the Phase column at SPEC:99-125). AC-1.1 is a P1 check (SPEC:207), and a phase passes only when every check in its block passes (SPEC:167).
- Grading sentence: An implementer who follows the P1 scope (SPEC:159) adds the flag to auggie-review (SPEC:100) but no `## Unattended mode` section, because P1 scope does not name sections for 3.2 commands. AC-1.1 then fails on auggie-review, so P1 cannot pass. X is wrong because the P1 check requires a section that the P1 scope does not add, and the spec does not say which phase adds it.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
