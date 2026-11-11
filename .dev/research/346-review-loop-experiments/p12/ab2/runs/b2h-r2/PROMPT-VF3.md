You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r2/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r2/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r2/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r2/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### B-2
### B-2. The spec-panel row names a directory flag the command does not accept, and contradicts the spec's own item 15 (blocking, open, origin=changed)
- Quote, spec:120: "add `--output-dir <dir>` (B-2; no output flag exists today, `INV-B:182`; UNVERIFIED item 15 applies if the command already takes a directory flag)".
- Quote, spec:286: "P2 checks it first: if a directory flag exists, the spec-panel row uses that name and adds no second flag (B-2)."
- Evidence: `command.md:460`: "`--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only." `command.md:461`: "`<report-dir>/return-contract.yaml` is written on every outcome." `command.md:23` (Usage): `[--output <file>] [--unattended] [--report-dir <dir>]`. `INV-B:182` says "no path or `--output` flag exists", which `command.md:23` contradicts. `command.md:455` already carries a `## Unattended mode` section, which the spec's row does not mention.
- Grading sentence: an implementer who follows spec:120 gives the spec-panel brief `--output-dir <dir>`; the command accepts no such flag, so without `--report-dir` it is refused before any work and writes no contract (`command.md:460`). That makes WC-4 ("written on every outcome", spec:62) and AC-2.3 (spec:201, "every required flag in the brief") impossible to pass. An implementer who instead follows spec:286 and adds no flag still meets the row at spec:120, which says to add one: the two texts give different answers. A stated text that an acceptance criterion cannot pass is blocking.
- Origin: changed. The revision replaced "a directory flag, not `--output`" with the name `--output-dir`. The text the revision cites to decide the name (item 15, `spec:286`) says it "was not checked in the B-2 revision". The reviewer checked it: the flag exists under another name.
- Status: open. The revision changed the wording but not the defect, so it is not resolved. It is not a regression either.
- Fix to consider: name `--report-dir <dir>` in the row and add no flag. `command.md:461` already gives the contract path `<report-dir>/return-contract.yaml`, which matches WC-4. Correct the "no output flag exists today" clause, which `command.md:23` contradicts. Turn item 15 into a settled statement, or remove it. Caveat: `command.md` stands in for `cmd/spec-panel.md` (see the citation bases above).

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
