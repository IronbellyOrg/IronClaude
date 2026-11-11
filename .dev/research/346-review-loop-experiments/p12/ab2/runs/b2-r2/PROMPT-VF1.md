You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r2/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r2/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r2/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r2/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### B-1
### B-1 (CRITICAL, blocking). WC-4's single contract location contradicts the rows that fix a different location
- Texts:
  - SPEC:62 (WC-4): "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:83 (section 3.1, adversarial, brief passes `--output <dir>`): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)". INV-A:35 shows `<output>` is the `--output` value ("Merged output + 6 artifacts under `<output>/adversarial/`").
  - SPEC:182 (7.2 step 3): "its report path is the WC-4 contract path"; SPEC:183 (step 4): `test -s <contract>`; SPEC:196 (AC-1.2): "all steps pass".
  - Same defect in three more rows: SPEC:90 and SPEC:87 pass `--output <file>` (tdd, init-lite) so no directory is passed, yet AC-2.2 (SPEC:200) uses `/sc:tdd "auth" --unattended --output <file>` and requires a contract; SPEC:92 and INV-B:272 put workflow's contract in `.dev/tasks/to-do/<id>/` where `<id>` is generated, and a pre-creation STOP (the case SPEC:92 adds) has no package directory.
- Grading sentence: An implementer who follows the adversarial row as written writes the contract at `<output>/adversarial/return-contract.yaml`; the coordinator, following WC-4 and section 2.3 (SPEC:73), opens `<output>/return-contract.yaml`, finds no report, and by WC-5 (SPEC:63, "or no report exists") sends `--outcome failed` for a run that succeeded; and acceptance step 4 cannot pass for adversarial, tdd or init-lite as written.

### B-2
### B-2 (CRITICAL, blocking). `load` is required to have no report file and also a contract section
- Texts:
  - SPEC:112 (section 3.2, load): Report column "none (see note)", note "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - SPEC:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" and, in the same row, "load (usage line only)".
  - SPEC:195 (AC-1.1): the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"; SPEC:196 (AC-1.2): a 7.2 live check "on each P1 command", whose step 4 needs a contract file (SPEC:183). `load` is a P1 command (SPEC:159).
- Grading sentence: An implementer who follows the load row and the Decision adds only the usage line, no `## Unattended mode` section and no contract, and X is wrong because AC-1.1 (every command in 3.1-3.2) and AC-1.2 step 4 (`test -s <contract>`) then fail for `load`; an implementer who satisfies AC-1.1 instead adds a section and a contract to `load`, which the row and the Decision say not to do.

### B-3
### B-3 (MAJOR, blocking). The P0 gate cannot pass as written, and a failure "reopens section 1"
- Texts:
  - SPEC:158 (P0): "(no command edits)", smoke runs of `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial`.
  - SPEC:194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1 ... a failure here reopens section 1".
  - SPEC:182 (7.2 step 3), pass condition: "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Grading sentence: An implementer or coordinator who follows AC-0.4 as written runs steps 1-3 for commands that, by SPEC:158, still write no WC-4 contract (troubleshoot's report is `REPORT.md`, SPEC:91), so step 3's pass condition cannot be met, the relaxation names step 4 only, and the stated consequence of failing is to reopen the core decision (section 1) on a false negative.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
