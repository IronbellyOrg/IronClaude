You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### M1
### M1 (open) and M9 (open): step 3 pass versus AC-0.4
An implementer who follows the step 3 pass text in P0 (.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:182) requires the worker_done report path to be the WC-4 contract path. The WC-4 path is produced only from P1 (:194 says "the contract arrives in P1"). For `/sc:troubleshoot` the existing report is REPORT.md (inventory/commands-b.md:242), which is not that path, so step 3 fails. The P0 row at :194 says step 3 checks the existing report instead. Both texts are stated, they contradict each other, and the P0 gate cannot pass as written for a reader who follows the step text. Blocking under the grading rule for two contradicting texts.

### M9
| M9 | open | Same defect as M1, seen from AC-0.4 (:194). The P0 override is not carried into the step 3 pass text (:182). |
(text of this finding in the prior report)
### M9
#### M9.a, from round1-b.md B3: *B3. [BLOCKING, High] AC-0.4 cannot pass for the three P0 commands.**
- Cites: `S:182` (step 3 path must be "the WC-4 contract path"); `S:183` (step 4 parses YAML with `status` and `command`); `S:194` (AC-0.4 says step 4 "uses the command's existing report file"); `S:62` (WC-4 path `<output-dir>/return-contract.yaml`); `INV-B:242` (troubleshoot writes `REPORT.md`); `INV-B:272` (workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`); `INV-A:35`, `INV-A:60` (adversarial writes under `<output>/adversarial/`).
- Wrong outcome: "An implementer who runs AC-0.4 on `/sc:troubleshoot` gets `REPORT.md`, which is neither the WC-4 path nor YAML, so step 3 and step 4 fail; the same holds for the workflow and adversarial paths." The contract arrives in P1 (`S:194`), so the P0 gate cannot pass.

### M16
### M16 (open): AC-4.2 install check
An implementer whose `/sc:post-release` run executes a real installer that exits before the second ps snapshot, or installs without any long-running process, passes AC-4.2 (:209), because the check looks only for installer or VM processes that are still running. The criterion states "no install", so a passing result is wrong. This is the WC-9 outward-action boundary (:67). The snapshot does not detect the install it claims to check, so the defect from round 1 is only partly repaired.

### N1
### N1 (new, origin=changed): workflow contract path
The workflow row (:92) sends the success contract to `.dev/tasks/to-do/<id>/return-contract.yaml` after creation, while WC-4 (:62) requires one report file, "known before dispatch", written on every outcome, with a subdirectory of `<output-dir>` allowed only when the row names it. The row also says the pre-creation STOP contract goes to `<output-dir>/return-contract.yaml`. An implementer who follows WC-4 for a successful workflow run writes the success contract to `<output-dir>/return-contract.yaml`, while the row says the success contract stays at the package path. The two texts name different files for the same success outcome. Under WC-5 (:63), a worker that checks `<output-dir>` finds no report and sends `--outcome failed`, which is wrong for a successful run. Blocking: two stated texts contradict and a concrete outcome follows. Inventory support: inventory/commands-b.md:272 says the package contract is written only after creation.

### N2
### N2 (new, origin=changed): brainstorm and init-lite in section 3.1 versus P1
Section 3.1 (:76 and :79) lists brainstorm (:84) and init-lite (:87) as "Ready today (10)". Their small-fix column reads "None", and :79 says "The only command changes are the small fixes in the last column". The P1 row now lists brainstorm and init-lite (:159), and AC-1.1 (:195) requires every P1 command to have the `## Unattended mode` section. An implementer who follows 3.1 changes neither command, so AC-1.1 fails at P1 because the section is missing; that is wrong because :195 requires it. The section 3.2 header count (27) and the P1 list (:159) disagree with the 3.1 header count (10). Blocking: two stated texts contradict and an acceptance criterion fails.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
