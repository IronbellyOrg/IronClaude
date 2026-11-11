You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N-1
### N-1 | BLOCKING | origin=changed | new, introduced by the F-02 fix at SPEC:62
- Location: `SPEC:62` (WC-4, sentence "F-02: a file-valued output ... uses the file's parent directory as `<output-dir>`"); `SPEC:87` (init-lite row, "Contract at `<parent of --output>/return-contract.yaml`"); `SPEC:69` (WC-11, "Two workers in one worktree must never write the same file").
- Issue: For a file-valued output, the contract name is fixed (`return-contract.yaml`) and only the parent directory varies. Every file-valued run in the same directory therefore writes the same contract path.
- Grading sentence: An implementer who follows `SPEC:62` for two `init-lite` runs in one worktree, `--output docs/a.md` and `--output docs/b.md` (`SPEC:87` says the brief passes `--output`), writes both contracts to `docs/return-contract.yaml`. The second write replaces the first. The coordinator opens that one path for both `worker_done` messages, so the first worker's outcome is lost. `SPEC:69` forbids two workers writing the same file, and `SPEC:64` (WC-6) forbids a retry from corrupting the first attempt's output. The fresh `--output` per attempt in `SPEC:87` does not change the contract path. Two stated texts conflict, and data is lost. Blocking.
- Same case for tdd: `SPEC:90` and `INV-B:47` give `--output <file>` for tdd, so two tdd runs into `docs/` collide the same way.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
