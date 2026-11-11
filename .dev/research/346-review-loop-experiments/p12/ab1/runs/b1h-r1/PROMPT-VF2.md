You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r1/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N1
### N1 (blocking, origin=changed; depends on unchanged spec:204)
- Location: `spec:85`, `spec:86` (changed); `spec:204` (AC-1.2, unchanged, quoted because it depends on the changed rows); `spec:159` (P1 lists cleanup-audit and index-repo).
- Quotes: `spec:86`: "Add `--output-dir` for the WC-4 contract in unattended mode". `spec:204`: "7.2 live check on each P1 command with `--unattended --output <dir>`".
- Grading sentence: an implementer who follows `spec:86` gives index-repo an `--output-dir` flag and no `--output` flag. The AC-1.2 run at `spec:204` passes `--output <dir>` to it, the command rejects the flag, and the criterion cannot pass. `spec:62` lists both spellings, but it does not say which one index-repo or cleanup-audit accepts, so the pass depends on a choice the spec does not make. The same holds for cleanup-audit (`spec:85`).

### N2
### N2 (blocking, origin=changed; depends on unchanged WC-11 at spec:69)
- Location: `spec:62` (WC-4, new sentence on file-valued outputs); `spec:69` (WC-11, unchanged: "Two workers in one worktree must never write the same file."); `spec:87` (init-lite `--output <file>`); `spec:90` (tdd `--output <file>`).
- Quote: `spec:62`: "For a command whose output flag names a file (`--output <file>`, as in tdd and init-lite), `<output-dir>` is that file's parent directory [M1]."
- Grading sentence: an implementer who follows `spec:62` writes the contract of every file-valued run to `<parent>/return-contract.yaml`. Two runs whose outputs sit in one directory (for example two init-lite runs with `--output .dev/superclaude/a.md` and `.dev/superclaude/b.md`) write the same contract path. The second run overwrites the first contract. The coordinator then opens a contract that describes the wrong worker, and the first worker's report is lost. WC-11 forbids two workers writing one file, and this rule makes that happen.
- Caveat: that two workers share a worktree is the case WC-11 guards. The `CAPS:115` citation for "workers share the current worktree by default" is UNVERIFIED here: `inventory/orca-capabilities.md:115` says worktrees are not deleted by these verbs and does not state the placement default. The finding does not depend on that premise, because it follows from WC-11's own text.

### N3
### N3 (blocking, origin=changed; regression introduced by the revision of step 6)
- Location: `spec:193` (step 6, changed); `spec:202` (AC-0.4, changed, "steps 1, 2, 5, 6 and 7 pass"); `spec:158` (P0 smoke runs use no output flag); `spec:92` (workflow `--output-dir` arrives in P1). Baseline `base:185` read "only files under the brief's output directory (and the command's documented artifacts) appear."
- Quote: `spec:193`: "for a report-only command, only files under the brief's output directory appear."
- Grading sentence: an implementer who runs AC-0.4 on `/sc:workflow "<small change>" --handoff none` gets a new package at `.dev/tasks/to-do/<id>/` (`spec:92`; `INV-B:52` and `INV-B:272` name that package as the command's output). Step 6 passes only files under "the brief's output directory", and the P0 brief has no output directory for workflow. The step therefore fails on a correct run, and `spec:202` says a failure reopens section 1. `/sc:troubleshoot "<real symptom>"` in P0 has the same problem: its default output is `.dev/troubleshoot/<slug>-<timestamp>/` (`INV-B:242`), and no output flag is passed in P0.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
