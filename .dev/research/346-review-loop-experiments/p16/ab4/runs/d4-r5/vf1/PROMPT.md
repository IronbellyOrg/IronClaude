You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4-r5/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4-r5/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4-r5/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4-r5/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F-1)
### F-1 [MAJOR, blocking] Acceptance check AC-1.1 requires a contract section on commands that section 3 says get none
Stated texts that contradict:
- Candidate line 195, AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Candidate line 112, `/sc:load` row: report column "none (see note)", "Other required change": "none: use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)". Line 159 repeats it ("load (usage line only)").
- Candidate line 265, Decisions: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- Candidate line 79 (3.1 intro): "The only command changes are the small fixes in the last column"; the `brainstorm` row (line 84) and `init-lite` row (line 87) say "None" in that column. Line 76 says only "changed" commands gain the section, and line 159 gives the P1 command list without brainstorm or init-lite.

Grading sentence: An implementer who follows line 112, line 265 and line 79 as written changes `/sc:load` only in its usage line and leaves `/sc:brainstorm` and `/sc:init-lite` untouched, and builds a Phase 1 whose own acceptance test (AC-1.1, line 195) fails on those three commands, because AC-1.1 requires every command in 3.1-3.2 to carry the section. The implementer who instead satisfies AC-1.1 adds a contract section to `/sc:load`, which line 265 rejects. The text itself offers no way to pass both. Two stated texts contradict, so this is blocking.

Attack (Whittaker, FR-2.2 Divergence): the AC-1.1 quantifier "every command in sections 3.1-3.2" and the per-row "change" column partition the 37 commands differently; the boundary case is the set difference (load, brainstorm, init-lite, plus any other row with "None").

### M2

#### M2.a (round1-a.md F-2)
### F-2 [MAJOR, blocking] WC-4 defines the report path from a coordinator-passed directory, yet several commands take a file, and two acceptance criteria depend on that path
Stated texts:
- Candidate line 62, WC-4: the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Line 73 (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)". Line 182 (7.2 step 3): "its report path is the WC-4 contract path".
- Candidate line 90, `tdd` row: brief must pass "`--output <file>`"; line 87, `init-lite`: "`--output <file>`"; line 120, `spec-panel`: "add `--output`" (the spec-panel `--output` is a file in the same row's evidence at `cmd/spec-panel.md`; UNVERIFIED here); line 200, AC-2.2: "`/sc:tdd "auth" --unattended --output <file>`" must yield a contract with `status: blocked` and a non-empty `blocked_question`.
- Candidate lines 92 and 198, `workflow` row and AC-1.4: the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` and must now also be written "for pre-creation STOPs", where no `<id>` exists yet.

Grading sentence: An implementer who follows WC-4 as written builds the tdd contract at `<file>/return-contract.yaml` (the passed `--output` value is the TDD file, not a directory), and that path cannot exist as a directory entry beside a file of the same name; AC-2.2 and the 7.2 step 3 and step 4 checks then cannot locate or open the contract, so they cannot pass. For `workflow` the stated path needs an `<id>` that a pre-creation STOP does not have, so AC-1.4 has no defined location to check. A stated text that an acceptance criterion cannot pass is blocking.

#### M2.b (round1-b.md B1)
### B1. CRITICAL (blocking): the contract path rule contradicts every command whose `--output` is a file
- Stated text 1, spec:62 (WC-4): the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the worker passes that path as `--report-path`.
- Stated text 2, spec:90 (tdd, section 3.1): brief passes `--output <file>`; report is "the TDD at `--output`". spec:87 (init-lite): `--output <file>`. spec:120 (spec-panel): "add `--output`". spec:107 (document): "require an explicit output". spec:108 (explain): "write the explanation to a file". Inventory: `INV-B:47` (tdd: "TDD file at `--output`"), `INV-A:55` (init-lite: "`.dev/superclaude/context-audit.md` or `--output`").
- Stated text 3, spec:200 (AC-2.2): the gate-trigger example `/sc:tdd "auth" --unattended --output <file>` must end with "contract `status: blocked` with a non-empty `blocked_question`", and spec:182 step 3 requires "its report path is the WC-4 contract path".
- Grading sentence: an implementer who follows WC-4 as written builds a tdd (and init-lite, spec-panel, document) that writes `<file>/return-contract.yaml` next to a path that is a regular file, or a contract at no defined path, and that is wrong because `--output <file>` names a file, so no `<output-dir>` exists and AC-2.2 (spec:200) and live-check steps 3-4 (spec:182-183) cannot locate or read the contract.
- Concrete attack (Whittaker, Divergence): input `--output .dev/x/tdd.md` -> WC-4 says "directory" -> the contract path is `.dev/x/tdd.md/return-contract.yaml`, which cannot be created when `tdd.md` is a file; the blocked case (a topic-only prompt, which is the AC-2.2 case) produces no TDD, so the path may be missing and the report is unreadable.

### M3

#### M3.a (round1-b.md B2)
### B2. CRITICAL (blocking): AC-0.4 requires a contract that does not exist in Phase 0
- Stated text 1, spec:194 (AC-0.4): runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow ... --handoff none` and `/sc:adversarial ...`; "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1".
- Stated text 2, spec:182 (live-check step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Stated text 3, spec:91 and spec:92: troubleshoot's report is `REPORT.md`; workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (id chosen by the command). spec:159 puts the WC-4 contract and the output flags in P1; `INV-B:49` and `INV-B:52` agree that these commands have no `--output` directory today.
- Grading sentence: an implementer who runs AC-0.4 exactly as written gets a troubleshoot worker whose `worker_done --report-path` is `REPORT.md` and whose contract does not exist, so step 3 (spec:182) cannot pass, and AC-0.4 says step 3 must pass; that is two stated texts of the same criterion contradicting each other.
- Related defect inside the same criterion: spec:73 and spec:62 require the output directory to be "known before dispatch", but spec:91-92 list no `--output` for troubleshoot or workflow in "Brief must pass", and workflow's directory depends on a generated `<id>`. The coordinator cannot name the path in the brief, so the "known before dispatch" rule cannot hold for two of the three Phase 0 smoke commands.
- A further inconsistency: spec:83 fixes adversarial's contract name to `<output>/adversarial/return-contract.yaml` while WC-4 says `<output-dir>/return-contract.yaml` (spec:62); the two are the same only if `<output-dir>` is read as `<output>/adversarial`, which no text says.

### M4

#### M4.a (round1-b.md B3)
### B3. MAJOR (blocking): AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- Stated text 1, spec:195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Stated text 2, spec:112 (load row): report "none (see note)", resume "n/a", change "none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line", phase "P1 (usage line only)". spec:265 (Decision "`/sc:load` handling"): "a report file would be an unrequested addition". `INV-B:31` ("writes no file; use as a brief step, not a task").
- Stated text 3, spec:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`"; spec:159 lists load in P1; spec:183 (step 4) requires `test -s <contract>` and a parsed `status`.
- Grading sentence: an implementer who follows the load row builds a load.md with only a usage-line fix and no `## Unattended mode` section and no contract, and that is wrong because AC-1.1 requires the section naming `return-contract.yaml` for all of 3.1-3.2 and AC-1.2 step 4 requires a contract file, so both criteria fail for load whichever way it is built (adding the section and file contradicts spec:112 and spec:265).

### M5

#### M5.a (round1-b.md B4)
### B4. MAJOR (blocking): AC-2.2 demands a `blocked` contract from P2 commands whose gate does not resolve as blocked
- Stated text 1, spec:200 (AC-2.2): "Gate-trigger run per P2 command ... **Pass:** `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`".
- Stated text 2, spec:160 lists the P2 set: auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot. Their section 3 rows resolve gates as follows:
  - auggie-review (spec:100): the gate is turned off by `--no-post-pr` / `--no-remediation-offer`; nothing blocks.
  - cleanup and improve (spec:103, spec:110): apply only allowed items and list the rest; the run succeeds with deferred items.
  - research (spec:116): `--unattended` pins `--strategy planning`; no blocked outcome.
  - tasklist (spec:122): passes `--unattended` to reflect so the headless rule applies; no blocked outcome.
  - reflect (spec:88): `--remediate` follows the headless auto-accept rule; no blocked outcome.
  - release-split (spec:89) and tdd (spec:90) block only for specific inputs.
- Grading sentence: an implementer who follows the section 3 rows builds auggie-review, cleanup, improve, research, tasklist and reflect that finish `succeeded` under `--unattended` on any input, and that is wrong because AC-2.2 requires every P2 command to produce `worker_done --outcome failed` with `status: blocked` on its gate-trigger run, which those commands have no input for; the criterion cannot pass as written for at least six of the fifteen commands it covers.

### M6

#### M6.a (round1-b.md B5)
### B5. MAJOR (blocking): AC-2.3 cannot pass for `/sc:cli-portify`
- Stated text 1, spec:201 (AC-2.3): "Happy-path run per P2 command with every required flag in the brief -> 7.2 passes with `--outcome succeeded`".
- Stated text 2, spec:105 (cli-portify row): "each of the three approval gates resolves as blocked with the artifact to review named in the contract"; the only resume is "a `--resume <contract>` flag". No flag, default or caller-supplied value is offered that approves a gate (WC-2 option (a) and (b) are not applied to this command). `INV-A:45` and `INV-A:68` record the three always-on approval gates.
- Grading sentence: an implementer who follows the cli-portify row builds a command that always stops at the first approval gate with `status: blocked`, and that is wrong because AC-2.3 requires a single worker run of every P2 command to end `succeeded`, which no input to this command can reach.

### M7

#### M7.a (round1-b.md B6)
### B6. MAJOR (blocking): AC-4.2 expects skipped-step reporting from a run that the post-release row blocks first
- Stated text 1, spec:113 (post-release row): "require an explicit `--output` and an explicit pre-tag choice, else blocked; VM, real-target install, commit and PR off unless the brief authorizes them".
- Stated text 2, spec:209 (AC-4.2): `/sc:post-release <version> --unattended --output <dir>` "with no authorization flags"; pass: "no install, VM, commit or PR ... the contract lists each skipped outward step".
- Stated text 3, spec:62 (WC-4): the contract fields are `status`, `command`, `report_path`, `artifacts`, and `blocked_question`; there is no field for skipped steps.
- Grading sentence: an implementer who follows the row builds a post-release that, given the AC-2.2 invocation (no pre-tag choice), stops at the pre-tag gate with `status: blocked` and a `blocked_question` before any outward step is reached, and that is wrong because AC-4.2 requires the contract to list "each skipped outward step", a list that neither WC-4 defines nor a blocked run produces.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
