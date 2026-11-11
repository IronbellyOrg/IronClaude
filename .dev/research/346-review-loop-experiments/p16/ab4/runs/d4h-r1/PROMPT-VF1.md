You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r1/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F1)
**F1. The contract path rule in WC-4 cannot be followed by the commands the spec lists.** Severity MAJOR. Grade: blocking. Expert: Wiegers (lead), Cockburn.
- WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`/`--output-dir` (SPEC:62). SPEC:73 says the coordinator's brief gives the report path "so the report path is known before dispatch".
- SPEC:83 (adversarial) requires `<output>/adversarial/return-contract.yaml`, a subfolder. SPEC:87 (init-lite) takes `--output <file>`, not a directory. SPEC:90 (tdd) takes `--output <file>`. SPEC:92 (workflow) has no output flag; its contract lives under `.dev/tasks/to-do/<id>/`. SPEC:85 (cleanup-audit) uses a fixed `.claude-audit/` path. SPEC:105 (cli-portify) leaves the location unnamed.
- Grading sentence: an implementer who follows WC-4 and SPEC:73 has the coordinator open `<output-dir>/return-contract.yaml` for adversarial, but SPEC:83 makes the file `<output-dir>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist.

### M2

#### M2.a (round1-a.md F2)
**F2. The P0 smoke runs use a brief that the contract says must carry `--unattended`, but P0 is before any command accepts that flag.** Severity MAJOR. Grade: blocking. Expert: Cockburn, Adzic.
- SPEC:73 says each Task's brief carries "the exact command line including `--unattended`". SPEC:180 says step 1 uses "the brief per section 2.3".
- SPEC:158 (P0) is "no command edits"; the flag is added in P1 (SPEC:159). AC-0.4 (SPEC:194) runs "the 7.2 live check" on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` with command lines that have no `--unattended`.
- Grading sentence: an implementer who follows AC-0.4 runs the P0 evidence with briefs that SPEC:73 forbids, so the P0 result, which section 1.4 (SPEC:43-44) treats as the test of the decision, is not a test of the contract's briefs.

### M3

#### M3.a (round1-a.md F3)
**F3. WC-5 maps an empty or malformed contract to `succeeded`.** Severity MAJOR. Grade: blocking (FR-8 GAP with a concrete wrong outcome). Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers.
- SPEC:63: `--outcome failed` only "when the report says failed or blocked, or no report exists"; `--outcome succeeded` "otherwise". SPEC:183 (step 4) treats an empty contract (`test -s`) as a failed check.
- Grading sentence: an implementer who follows SPEC:63 as written sends `--outcome succeeded` for a zero-byte contract or for `status: done`, because neither is "failed", "blocked" or "no report"; SPEC:183 says the same file must not pass.

### M4

#### M4.a (round1-a.md F4)
**F4. WC-11 changes default output paths without limiting the change to unattended runs, which contradicts SA-1.** Severity MAJOR. Grade: blocking. Expert: Wiegers (traceability), Fowler.
- WC-11 (SPEC:69): "Default output paths carry a timestamp or the slug the coordinator passes". Only its second clause is scoped to unattended mode.
- SA-1 (SPEC:146): without `--unattended`, "every ... output path ... stays as it is today". The section 3.1 row for index-repo (SPEC:86) uses the fixed `PROJECT_INDEX.md` and resumes with `mode=update`.
- Grading sentence: an implementer who follows SPEC:69 gives standalone `/sc:index-repo` a timestamped default name, which breaks SA-1 as written, and the text does not say that WC-11 is limited to unattended runs.

### M5

#### M5.a (round1-b.md B1)
### B1. AC-0.4 step 4 reads YAML keys from a Markdown report
- Location: SPEC:183 (step 4 asserts `d['status']` and `d['command']` from a YAML load), SPEC:194 (AC-0.4 says step 4 "uses the command's existing report file"). INV-B:49 (`/sc:troubleshoot` writes `REPORT.md`, `report_path`).
- Grading sentence: An implementer who follows AC-0.4 runs step 4 on the troubleshoot `REPORT.md`, which is Markdown, so `yaml.safe_load` returns text or a dict without `status` and `command`, and the step fails on a correct run.

### M6

#### M6.a (round1-b.md B2)
### B2. Step 6 fails whenever the phase's own edits are uncommitted
- Location: SPEC:185 (pass: "only files under the brief's output directory ... appear"), SPEC:158-162 (each phase edits tracked files), SPEC:194, 196, 201 (AC-0.4, AC-1.2, AC-2.3 all depend on step 6). No step in SPEC:180-186 commits or snapshots the tree.
- Grading sentence: An implementer who writes the P0 files (WORKER-CONTRACT.md, the HOW-WE-WORK section, the test file) in the worktree and then runs step 6 as written sees those modified or untracked paths in `git status --short`, which the pass condition does not allow, and the spec gives no step that commits or snapshots first.

### M7

#### M7.a (round1-b.md B3)
### B3. AC-0.4 requires "no Agent-tool wrapper, verified in the step-5 transcript", and step 5 does not test it
- Location: SPEC:194 (AC-0.4 "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"), SPEC:184 (step 5 pass: "no AskUserQuestion call").
- Grading sentence: An implementer who runs step 5 as written searches only for `AskUserQuestion`, so no evidence about an Agent-tool wrapper is produced, and AC-0.4 cannot pass as written.

### M8

#### M8.a (round1-b.md B4)
### B4. AC-2.2 requires `status: blocked` for every P2 command, but six P2 commands have no blocked path
- Location: SPEC:200 (AC-2.2: "contract `status: blocked` with a non-empty `blocked_question`"), SPEC:160 (P2 set), and the rows that resolve without a blocked outcome: SPEC:100 (auggie-review: defaults `--no-post-pr --no-remediation-offer`), SPEC:103 (cleanup: lists unapplied items, does not block), SPEC:110 (improve: same), SPEC:116 (research: pins `--strategy planning`), SPEC:88 (reflect: headless auto-accept, no gate without `--remediate`), SPEC:122 (tasklist: passes `--unattended` down, no gate).
- Grading sentence: An implementer who follows the cleanup row builds a run that applies auto-fix items and lists the rest in the report, so no gate resolves as blocked and AC-2.2 fails because it expects `status: blocked`.

### M9

#### M9.a (round1-b.md B5)
### B5. SA-1 forbids prompt changes without `--unattended`; the roadmap row removes the Y/n prompt unconditionally
- Location: SPEC:146 (SA-1: "every prompt ... stays as it is today" without `--unattended`), SPEC:149 (SA-4 allows fixes that "keep the standalone behaviour or correct a documented defect"), SPEC:118 (roadmap row: "the 'Resume? [Y/n]' prompt is replaced by the explicit resume flag (resume only when passed)", with no `--unattended` qualifier). Source of the prompt: INV-B:40 (`sk/sc-roadmap-protocol/SKILL.md:433-438`, UNVERIFIED in this sandbox).
- Grading sentence: An implementer who follows the roadmap row removes the Y/n prompt for a plain session with no flags, which SA-1 (SPEC:146) forbids, and SA-4 (SPEC:149) permits only as a defect fix, so the two texts contradict each other.

### M10

#### M10.a (round1-b.md B6)
### B6. `load` must write a contract (WC-4, AC-1.1, AC-1.2) but its row and decision say it writes no file
- Location: SPEC:62 (WC-4: contract "written on every outcome" in unattended mode), SPEC:112 (load row: report "none (see note)"), SPEC:159 (P1 includes load), SPEC:195 (AC-1.1 requires `return-contract.yaml` in every section 3.1 and 3.2 command), SPEC:196 (AC-1.2 runs on each P1 command), SPEC:265 (decision: "a report file would be an unrequested addition"). INV-B:65 (load "only loads context into the current session").
- Grading sentence: An implementer who follows the load row writes no contract, and AC-1.1 and AC-1.2 fail for `load`; an implementer who follows WC-4 writes one, which the decision at SPEC:265 forbids, so the two texts contradict each other.

### M11

#### M11.a (round1-b.md B7)
### B7. The workflow contract path conflicts with WC-4 and does not exist for a pre-creation STOP
- Location: SPEC:62 (WC-4: `<output-dir>/return-contract.yaml`, "including stops before any other output exists", and the path is known before dispatch), SPEC:92 (workflow row: `.dev/tasks/to-do/<id>/return-contract.yaml`; "Write the contract for pre-creation STOPs too"), SPEC:198 (AC-1.4). INV-B:272 (`.dev/tasks/to-do/<id>/`; not written for pre-creation STOPs). SPEC:73 (the coordinator must know the path before dispatch).
- Grading sentence: An implementer who follows WC-4 writes a pre-creation STOP contract to `<output-dir>`, but workflow has no output flag in row SPEC:92, and the row's `<id>` directory does not exist before package creation, so the path the coordinator must know before dispatch (SPEC:73) is undefined for that case.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
