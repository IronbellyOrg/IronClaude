You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N2
### N2 (blocking, open, origin=changed; spec:62)
- Location: `spec:62` (WC-4, changed). Depends on `spec:69` (WC-11, unchanged: "Two workers in one worktree must never write the same file.").
- Quote, spec:62: "where `<parent>` is that file's parent directory and `<stem>` is its file name without its extension, so two runs whose files share a parent directory write two contracts [M1, N2]."
- Grading sentence: an implementer who follows `spec:62` as written runs `--output .dev/superclaude/a.md` for one command and `--output .dev/superclaude/a.txt` for another (both accept a file, `spec:87` and `spec:90`). Both contracts go to `.dev/superclaude/a.return-contract.yaml`. The second run overwrites the first, so the coordinator opens a contract that describes the wrong worker, and the first worker's report is lost. The sentence that says files sharing a parent directory write two contracts is false for this pair, so the stated text contradicts its own rule. No further assumption is needed for the overwrite; the input pair is the only premise, and the rule gives it no exception.
- Scope of the premise: no command in section 3 writes two extensions today. The defect is reached only through the choice of inputs, which is why this is graded with the same weight as review 2's N2 (a wrong contract read and a lost report), not as a Medium warning.

### N4
### N4 (blocking, new, origin=changed; spec:204)
- Location: `spec:204` (AC-1.2, changed). Depends on `spec:112` (load row, unchanged), `spec:159` (P1 list, unchanged), `spec:186-188` (7.2 live check, unchanged), and the section 3 rows for the P1 commands (`spec:101-125`, unchanged).
- Quotes:
  - `spec:204`: "7.2 live check on each P1 command with `--unattended` and the one output flag section 3 names for it (`--output-dir <dir>` for cleanup-audit, index-repo and workflow; `--output <dir>` for the others)".
  - `spec:112`: "| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; ... | P1 (usage line only) |".
  - `spec:159`: P1 "Commands" column lists "analyze, build, business-panel, design, document, explain, index, test, load (usage line only)".
  - `spec:188`: 7.2 step 1 is "`ORCA orchestration task-create --spec ...`, then `ORCA orchestration worker-start ...`", run "For each command under test".
- Grading sentence: an implementer who follows `spec:204` as written dispatches `/sc:load --unattended --output <dir>` as its own Task (7.2 step 1), which `spec:112` forbids ("not as its own Task"). Section 3 names no output flag and no report file for load (`spec:112` "none"), so there is no `--output <dir>` to pass and no contract for the step-4 `test -s <contract>` (`spec:191`) to test. Two stated texts contradict each other, and the criterion cannot pass as written. Both points hold with no further assumption. `INV-B:31` and `INV-B:65` say load "writes no file; use as a brief step, not a task", and `INV-B:293` lists `/sc:load` among commands with no single report file, so the inventory agrees with `spec:112`.
- Origin note: the contradiction is also in spec-v2 (`base:204` names the same P1 set and "each P1 command"). Review 2 checked only the changed lines and did not raise it. It is graded here because `spec:204` is a changed line that carries it, and the new "one output flag section 3 names for it" clause depends on the same row.

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
