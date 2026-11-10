You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N-6
### N-6 (BLOCKING, new, origin=changed): WC-5 gives a clean P0 run no permitted outcome, so the AC-0.4 outcome check cannot pass
- Changed text: `spec:63` WC-5, "`--outcome failed` when the report says `failed` or `blocked`; in P0, when the named report is missing or zero bytes (N-1); ... `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`". Changed text: `spec:182` (7.2 step 3), "its `--outcome` matches the contract's `status` under WC-5 (from P1) or the named report under WC-5 (P0, N-1)".
- Dependent text: `spec:79` ("the worker reports the named file until Phase 1 adds the contract"); `spec:91` (`troubleshoot`: `REPORT.md`, `report_path`); `spec:194` (AC-0.4: "steps 1-3 and 5-7 pass"); `spec:158` (P0 smoke runs carry no contract).
- Sentence: "An implementer who follows `spec:63` as written in P0 for `/sc:troubleshoot`, whose named `REPORT.md` is complete (`spec:91`, `spec:79`), finds that the failed branch does not apply, since the report is neither missing nor zero bytes, and that the succeeded branch requires a parsed `status`, which P0 does not produce. So `spec:63` permits no outcome for that run. That is wrong because `spec:63` also requires exactly one `worker_done`, and AC-0.4 step 3 (`spec:182`, `spec:194`) requires the outcome to match."
- Why it is blocking: two stated texts contradict for the same clean P0 run (`spec:63` against `spec:182` and `spec:194`), and an acceptance criterion cannot pass as written. The grading rule names both cases. `spec:201` (AC-2.3) shows that `--outcome succeeded` is the intended clean-run outcome, but only in P2 with a contract, so it does not cover P0.
- Attack (Whittaker, FR-2.2 Divergence): "I can break this specification by **Divergence Attack**. The invariant at **WC-5 (spec:63)** fails when **the P0 named report is present and non-empty**. Concrete attack: the P0 smoke run of `/sc:troubleshoot "<symptom>"` writes a complete `REPORT.md` and no contract; the failed branch does not fire; the succeeded branch needs a parsed status that P0 does not produce; the worker sends no outcome, or sends one the text forbids. Trace: before the N-1 revision = `failed` (wrong); after = no permitted outcome (wrong)."
- Origin: the revision after round2. It added a P0 failed clause to `spec:63` and no P0 success clause.

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
