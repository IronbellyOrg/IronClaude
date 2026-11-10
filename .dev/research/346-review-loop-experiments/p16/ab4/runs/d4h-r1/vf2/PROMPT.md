You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### M1
| M1 | open (deferred part) | :62, :83, :92 now name the paths; cli-portify is still unnamed at :62 and :105 | revise1.md:71 leaves the cli-portify location to P2. The reviser's deferral counts as open. |
(text of this finding in the prior report)
### M1
#### M1.a, from round1-a.md F1: *F1. The contract path rule in WC-4 cannot be followed by the commands the spec lists.** Severity MAJOR. Grade: blocking. Expert: Wiegers (lead), Cockburn.
- WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`/`--output-dir` (SPEC:62). SPEC:73 says the coordinator's brief gives the report path "so the report path is known before dispatch".
- SPEC:83 (adversarial) requires `<output>/adversarial/return-contract.yaml`, a subfolder. SPEC:87 (init-lite) takes `--output <file>`, not a directory. SPEC:90 (tdd) takes `--output <file>`. SPEC:92 (workflow) has no output flag; its contract lives under `.dev/tasks/to-do/<id>/`. SPEC:85 (cleanup-audit) uses a fixed `.claude-audit/` path. SPEC:105 (cli-portify) leaves the location unnamed.
- Grading sentence: an implementer who follows WC-4 and SPEC:73 has the coordinator open `<output-dir>/return-contract.yaml` for adversarial, but SPEC:83 makes the file `<output-dir>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
