You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r4/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N-1
### N-1 (BLOCKING, new, origin=changed): WC-5 keys the default outcome on the contract, but spec:79 has P0 workers report the named file, with no contract yet
- Changed line: `spec:63`. Baseline `baseline:63` read "`--outcome failed` when the report says `failed` or `blocked`, or no report exists". The revision replaced "no report exists" with "when the contract is missing, zero bytes, ...". The subject moved from the report to the contract.
- Text that interacts with it: `spec:79` "the worker reports the named file until Phase 1 adds the contract"; `spec:91` (troubleshoot report is `REPORT.md`); `spec:194` (AC-0.4) "step 4 uses the command's existing report file, since the contract arrives in P1"; `spec:182` (7.2 step 3) "its `--outcome` matches the contract's `status` under WC-5".
- Sentence: "An implementer who follows `spec:63` in P0 for `/sc:troubleshoot`, where `spec:79` and `spec:91` say the worker reports `REPORT.md` and no contract exists until P1, finds the contract missing and sends `--outcome failed` after a completed run, and that is wrong because the run did not fail."
- Whittaker, FR-2.1 (Zero/Empty): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract is absent in a phase where the named report is the deliverable**. Concrete attack: the P0 smoke run of `/sc:troubleshoot "<symptom>"` writes a complete `REPORT.md` and no `return-contract.yaml`; WC-5 selects `failed`; `worker_done --outcome failed` settles the Task as failed; AC-0.4 step 3 (`spec:182`) then has no contract status to compare with. Trace: before = run completed; after = Task failed, and AC-0.4 cannot pass as written."
- Origin: the revision itself. Baseline wording was coherent in P0 because it keyed on the report.
- Severity: MAJOR by text, blocking under the grading rule: a stated text produces a wrong outcome on a clean run, and AC-0.4 (`spec:194`) cannot pass as written.

### N-2
### N-2 (minor, origin=changed): adversarial contract location differs from the location the inventory observed
- `spec:83` now puts the adversarial contract at `<output>/return-contract.yaml`. `INV-A:35` records real runs writing `<output>/adversarial/return-contract.yaml` next to the merged output and the six artifacts under `<output>/adversarial/`. The new location is consistent with WC-4 (`spec:62`) and is a valid choice, but no entry in the spec's `## Decisions` table records the change from the observed path. Minor note.

### N-5
### N-5 (minor, origin=unchanged, quotes changed lines): 7.2 step 3 does not carry the workflow exception
- `spec:182` requires "its report path is the WC-4 contract path". `spec:73` and `spec:92` say the workflow contract path is the package's, learned from `worker_done --report-path`. Step 3 does not say so. Minor note.

### M-1
Medium, carried from round1 and still open on unchanged text: M-1 (WC-1 has no owner or phase, `spec:59`), M-2 (partial maps to succeeded, `spec:63`, `spec:262`, `spec:263`), M-3 (write-then-send order is still not stated, `spec:62` and `spec:63`), M-4 (WC-3 answer path and ask timeout, `spec:61`), M-5 (SA-2 check misses `orca-cli` and uppercase `ORCA`, `spec:172`), M-6 (SA-4 versus section 3 edits, `spec:149`), M-7 (nesting layers, `spec:122`), M-8 (plugin mirror, `spec:279`), M-9 (P0 smoke runs do not test WC-2, `spec:79`, `spec:194`), M-10 (4-minute rule for an iteration over 4 minutes, `spec:68`), M-11 (testability, WC-5 has no automated test, `spec:195`), M-12 (checkpoints undefined, `spec:70`), M-14 (WC-11 and fixed output dirs, `spec:85`, `spec:119`), M-15 (brief template owner and version, `spec:73`, `spec:158`).
Restated from review-loop step 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (N-2 to N-5, M-1 to M-15, the minor notes) are not part of this brief.

### M-15
Medium, carried from round1 and still open on unchanged text: M-1 (WC-1 has no owner or phase, `spec:59`), M-2 (partial maps to succeeded, `spec:63`, `spec:262`, `spec:263`), M-3 (write-then-send order is still not stated, `spec:62` and `spec:63`), M-4 (WC-3 answer path and ask timeout, `spec:61`), M-5 (SA-2 check misses `orca-cli` and uppercase `ORCA`, `spec:172`), M-6 (SA-4 versus section 3 edits, `spec:149`), M-7 (nesting layers, `spec:122`), M-8 (plugin mirror, `spec:279`), M-9 (P0 smoke runs do not test WC-2, `spec:79`, `spec:194`), M-10 (4-minute rule for an iteration over 4 minutes, `spec:68`), M-11 (testability, WC-5 has no automated test, `spec:195`), M-12 (checkpoints undefined, `spec:70`), M-14 (WC-11 and fixed output dirs, `spec:85`, `spec:119`), M-15 (brief template owner and version, `spec:73`, `spec:158`).
Restated from review-loop step 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (N-2 to N-5, M-1 to M-15, the minor notes) are not part of this brief.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
