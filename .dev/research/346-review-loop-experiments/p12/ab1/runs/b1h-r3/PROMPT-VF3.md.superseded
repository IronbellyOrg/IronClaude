You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### B2
### B2 (new in round 3, blocking, origin=changed). The load row forbids the Task that AC-1.2 requires for load
- Origin: changed. The row quotes the changed line spec:112; the conflicting AC-1.2 is unchanged (spec:197). The same two texts are also in the baseline (`spec-v2.md:112` and `spec-v2.md:197`), so this is older than the round-3 edit and was not raised in round 2. Recorded now under the rule to record a severe defect found in re-review even if older.
- Stated texts:
  1. spec:112, load row: "use it as a step inside another worker's brief, not as its own Task".
  2. spec:159 (P1 scope) puts `load` in P1; spec:196 (AC-1.1) and spec:197 (AC-1.2) apply to "each P1 command", and AC-1.2 is "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass".
  3. spec:179-180 (7.2): "For each command under test, the coordinator runs: 1. `ORCA orchestration task-create --spec "<brief per section 2.3>"`, then `worker-start`". Step 3 (spec:182) requires one `worker_done` whose report path is the WC-4 contract path.
  4. spec:167: "A phase passes only when every check in its block and every common check passes."
- Sentence that holds with no further assumption: an implementer who follows the load row never creates a Task for `/sc:load` (spec:112); AC-1.2 requires a 7.2 run on `load`, and 7.2 step 1 (spec:180) creates a Task for each command under test; so AC-1.2 cannot pass for `load` as written, and P1 cannot pass (spec:167).
- Grading: a stated text that an acceptance criterion cannot pass, and two stated texts that contradict each other, are both blocking under `command.md` Review Loop item 2 and the FIRST-REVIEW grading check (prompts file line 33).

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
