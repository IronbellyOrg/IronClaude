You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r2/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r2/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r2/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r2/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N5
### N5 (blocking, MAJOR): P1 accepts `--unattended` on gated commands that still prompt
- Origin: changed. Candidate `:159` is changed; the "accepted by every command in sections 3.1 and 3.2" clause is inherited from baseline `:159` and was not raised in round 1 (it was a defect of the same kind as M3, which covered only outward defaults).
- Texts that contradict: WC-2 `:60`, "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer"; against P1 `:159`, which accepts the flag on every command in sections 3.1 and 3.2 except the four outward-default commands, and section 2.3 `:73`, which passes `--unattended` "from P1 on".
- Gates still on the default path until P2 or later: tdd (`:90`, topic-only clarification), release-split (`:89`), troubleshoot (`:91`, `--depth deep` STOP), cli-eval (`:104`, the suite menu; `inventory/commands-a.md:44` gives its AskUserQuestion as "Yes"), cli-portify (`:105`), recommend (`:115`), review-translation (`:117`), roadmap (`:118`, "Resume? [Y/n]"), spec-panel (`:120`).
- Grading sentence: an implementer who follows P1 and section 2.3 dispatches `/sc:tdd "<topic>" --unattended --output <file>` in P1. The topic-only clarification still asks, and the row resolves it as blocked only in P2 (`:90`). The worker waits on a prompt and sends no `worker_done`, which WC-2 says must not happen under `--unattended`.
- Blocking: two stated texts contradict (`:60` and `:159`), and the outcome is a concrete stall.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
