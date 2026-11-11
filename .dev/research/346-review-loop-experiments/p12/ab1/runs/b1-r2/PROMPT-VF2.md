You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r2/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r2/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r2/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r2/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N1
### N1. AC-1.2 requires a live `--unattended --output <dir>` check on every P1 command, and `load` is a P1 command that now takes neither (blocking)
- Origin: `changed` (the changed lines `spec:112` and `spec:159` make `load` explicitly outside `--unattended`; the unchanged line `spec:196` depends on them). Experts: Wiegers (traceability), Crispin (acceptance criterion cannot pass), Whittaker (Sequence Attack: run the P1 gate in its stated order).
- Stated texts:
  - `spec:159` (changed): P1 Commands cell lists "load (usage line only)", and the same row says the flag and section go "in every command in sections 3.1 and 3.2 except load".
  - `spec:112` (changed): `load` "gets no `## Unattended mode` section", Report "none", "not as its own Task".
  - `spec:196` (unchanged, AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`", pass condition "all steps pass".
  - `spec:182-183` (7.2 steps 3-4; `spec:182` changed): step 3 needs a `worker_done` whose report path is the contract path WC-4 gives; step 4 runs `test -s <contract>` and a YAML assertion on `status` and `command`.
  - `spec:167`: "A phase passes only when every check in its block and every common check passes."
- Grading sentence: An implementer who follows the stated text as written runs the 7.2 check on `load` with `--unattended --output <dir>` (`spec:196`, because `spec:159` lists `load` as a P1 command), and builds `load` with no `--unattended` flag, no section and no contract (`spec:112`, `spec:159`, `spec:265`). That is wrong because step 4 (`spec:183`) has no contract to open, step 3 has no contract path, so AC-1.2 fails, and by `spec:167` the P1 gate cannot pass; the only way to pass is to give `load` a contract, which `spec:265` rejects.
- Concrete attack (Whittaker, Sequence): state before: P1 edits done, `load` has the usage-line fix only. Steps: dispatch `/sc:load --unattended --output out/`; the worker ends with no report file. State after: `out/return-contract.yaml` absent, `test -s` exits 1, AC-1.2 red, P2 never starts (`spec:154`).

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
