You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N-2
### N-2 | BLOCKING | origin=changed | new, introduced by the N-1 fix at SPEC:62 and SPEC:87
- Location: `SPEC:62`, the F-02 clause "its contract is `<output-stem>.return-contract.yaml` ... where `<output-stem>` is the file name without its extension", and the first sentence of the same paragraph ("the command writes `<output-dir>/return-contract.yaml`"); `SPEC:87` (init-lite, "Contract at `<parent of --output>/<output-stem>.return-contract.yaml`"); `SPEC:69` (WC-11, "Two workers in one worktree must never write the same file"); `SPEC:90` (tdd, `--output <file>`, `INV-B:47`).
- Issue: The name `<output-stem>` drops the extension, so two file outputs in one directory that share a stem get the same contract path. The same paragraph also still states the shared name `return-contract.yaml` for a file-valued output, through `<output-dir>`.
- Grading sentence A: An implementer who follows the F-02 clause of `SPEC:62` as written, running `--output docs/a.md` and then `--output docs/a.txt` in one worktree, writes both contracts to `docs/a.return-contract.yaml`. The second write replaces the first, and the coordinator opens that one path for both `worker_done --report-path` calls (`SPEC:62`, last sentences), so the first worker's outcome is lost. `SPEC:69` forbids two workers writing the same file, so the two stated texts conflict and data is lost. Blocking.
- Grading sentence B: An implementer who follows the first sentence of `SPEC:62`, which gives `<output-dir>/return-contract.yaml` with `<output-dir>` the file's parent directory, writes `docs/return-contract.yaml` for every file-valued run in `docs/`. That is the N-1 collision (`RR:78`) that the revision was meant to remove. The paragraph states both names, so the two statements contradict. Blocking.
- Reachability: the case needs two file-valued outputs in one directory. `SPEC:69` names two workers in one worktree as the parallel case the rule protects, and `SPEC:90` (tdd) and `SPEC:87` (init-lite) are both file-valued. The case is narrower than N-1, but it is the same defect class and the same consequence, so it is graded the same way.

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
