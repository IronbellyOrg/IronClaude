You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r1/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r1/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r1/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r1/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### F1
### F1 (blocking) - AC-1.1 and the P1 scope cannot be satisfied alongside D3(a), the load row and the phase order
- Texts, all in the candidate:
  - AC-1.1 (S:195): the P1 test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
  - P1 scope (S:159): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
  - `/sc:pr-submit` is in section 3.2 (S:114), but D3(a), the recommended option, says "no pr-submit changes in Phase 4" (S:240), and S:139 says it "stays a worker candidate only if the user accepts open decision D3".
  - `/sc:load` is in section 3.2 with "Report (WC-4): none (see note)" and "use it as a step inside another worker's brief, not as its own Task" (S:112), and its phase is "P1 (usage line only)".
  - Phase order: "Later phases do not start until the earlier phase's checks in section 7 pass" (S:154); P4 "waits for answers to D2-D4" (S:154, S:162); gate resolution for auggie-review, cleanup, task, tasklist and the other P2 commands is assigned to P2 (S:100-122, S:160).
- Grading sentence: An implementer who follows S:195 and S:159 builds a P1 in which pr-submit, load, implement and post-release (and every P2 command) already carry a `## Unattended mode` section naming `return-contract.yaml` and accept `--unattended`, and X is wrong because S:240 says pr-submit gets no changes under the recommended D3(a), S:112 gives load no report, and S:60 and S:67 say a command under `--unattended` never prompts and never posts, yet between P1 and P2 `/sc:auggie-review <PR> --unattended` would still post to GitHub and offer remediation (INV-A:38) and `/sc:cleanup --unattended` would still prompt for approval (INV-A:43). The check AC-1.1 also cannot pass without that wrong build, which means P1 cannot be closed and S:154 blocks every later phase.

### F2
### F2 (blocking) - WC-4's contract path contradicts the adversarial row, the workflow row and the live-check pass condition
- Texts:
  - WC-4 (S:62): the command writes "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the report file is "known before dispatch".
  - Section 2.3 (S:73): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
  - Adversarial row (S:83): the brief passes `--output <dir>` and the small fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"; AC-1.4 (S:198) checks that "adversarial names one fixed path". INV-A:60 confirms the two real nested locations that exist today.
  - Workflow row (S:92): the contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, a package directory the command generates (INV-B:272-273 "never overwrites or reuses an existing package"); the brief passes no directory.
  - Live check step 3 (S:182): pass requires "its report path is the WC-4 contract path".
- Grading sentence: An implementer who follows WC-4 builds adversarial writing `<dir>/return-contract.yaml`, and X is wrong because S:83 and AC-1.4 (S:198) require `<dir>/adversarial/return-contract.yaml`; an implementer who follows S:83 builds the nested path and then S:182 cannot pass, because the nested file is not "the WC-4 contract path". For workflow the generated `<id>` directory is not a directory the coordinator passed, so "known before dispatch" (S:62, S:73) cannot hold.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
