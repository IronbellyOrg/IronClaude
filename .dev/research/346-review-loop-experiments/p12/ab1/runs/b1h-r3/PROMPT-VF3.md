You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r3/vf3/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### R2-1
| R2-1 | blocking | **open** (partial repair) | Workflow and troubleshoot are repaired. The step-3 rule for adversarial (`spec:189`, `spec:201`) takes its file from "its existing contract file", which the spec never names. The adversarial row says "filename not fixed" (`spec:83`), and the inventory records two layouts (`INV-A:35`). The same root cause as M6 below. |
(text of this finding in the prior report)
### R2-1 (BLOCKING, origin=changed)
- Quoted: AC-0.4 (`orca-worker-contract-spec.md:201`): "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today". Step 3 (`:189`), which AC-0.4 depends on: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Sentence: An implementer who runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` as written must make step 3's outcome match hold. Troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`), and the contract does not exist before P1 (`:201`), so there is no `status` to match. Step 3 cannot pass, and P0 cannot pass.
- Origin: the step 3 text is unchanged from `spec-v1.md`, so the defect is older. It is counted as changed because it quotes the changed AC-0.4 line (`:201`) that depends on it.

### M6
### M6 (regressed, BLOCKING; origin=unchanged step 4, depends on changed `spec:201` step 3)
- Quoted: `spec:201`, adversarial step 4: "`adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`)". Step 3 at `spec:189` and `spec:201` uses the same file: "its report path is that file".
- Sentence: An implementer who runs AC-0.4 on `/sc:adversarial --compare <two files> --depth quick --output <dir>` as written must run `test -s` on "its existing contract file". The spec names no path (`spec:83`: "filename not fixed"). The inventory records two layouts (`INV-A:35`). The check tests either the wrong file or no file, so step 4 and the step-3 rule built on it cannot pass as written.
- Note: `spec:83` gives the adversarial row's P1 fix as `<output>/return-contract.yaml`. That is P1, and P0 runs before it (`spec:158`).

Write your full reply to .dev/orca-command-refactor/review/verify-3.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
