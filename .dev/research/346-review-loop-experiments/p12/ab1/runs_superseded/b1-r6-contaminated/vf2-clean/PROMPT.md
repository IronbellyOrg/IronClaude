You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r6/vf2-clean. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r6/vf2-clean/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r6/vf2-clean/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r6/vf2-clean/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### N1
### N1 - CRITICAL (blocking) - origin=changed - Wiegers, Crispin, Whittaker (Sequence/Divergence) - AC-0.4 step 4 still cannot pass for the P0 smoke commands
Where it came from: a defect older than the revision (step 4 and the 7.2 YAML assertion are unchanged text, SPEC:183), exposed by the revision's carve-out. It quotes the changed line SPEC:194: "step 4 uses that same file, since the contract arrives in P1 (M2)".
- Stated texts: SPEC:194 (AFTER) makes step 4 run on "the command's existing report file". SPEC:183 (step 4, unchanged) runs `uv run python -c "... d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` and passes only if "both exit 0". The P0 commands' existing report files: troubleshoot `REPORT.md` (SPEC:91; INV-B:242 "`report_path` REPORT.md"; INV-B:249 "`return-contract.yaml` only when `--caller task-unified`"), workflow's contract with `status`, `plan_path`, `reflect_report_path` and no `command` field listed (INV-B:272), adversarial's contract "filename not fixed" (SPEC:83).
- Grading sentence: An implementer who follows the stated text as written runs step 4 of the AC-0.4 live check on troubleshoot's `REPORT.md`, which has no `status` key and no `command` key (it is a markdown report, INV-B:242), so `d['status']` raises and the command exits non-zero; step 4 cannot pass, so AC-0.4 cannot pass, and SPEC:154 ("later phases do not start until the earlier phase's checks ... pass") and SPEC:194 ("a failure here reopens section 1") then fire on a correct run. This is the defect class of M2 at the next step.

### N2
### N2 - CRITICAL (blocking) - origin=changed - Wiegers, Adzic, Fowler - AC-1.2 passes `--output <dir>` to `workflow`, whose contract directory is now `--report-dir`
Where it came from: the revision. It changed WC-4 (SPEC:62) and the workflow row (SPEC:92) to `--report-dir` and edited AC-2.2 (SPEC:200) for tdd, and edited AC-1.2 (SPEC:196) for `load` only, leaving its flag text unchanged.
- Stated texts: SPEC:196 (AFTER): "7.2 live check on each P1 command except `load` (M1, M5) with `--unattended --output <dir>`". `workflow` is a P1 command (SPEC:92, 159). SPEC:62: for `workflow` the `<output-dir>` is the `--report-dir` directory; SPEC:92 brief column: "`--handoff none`; `--report-dir <dir>` (P1)", with no `--output` for workflow (INV-B:52, INV-B:272 name no `--output`). SPEC:182-183: steps 3-4 test "the WC-4 contract path".
- Grading sentence: An implementer who follows the stated text as written runs the AC-1.2 live check for `workflow` with `--output <dir>` and no `--report-dir`; by SPEC:62 the contract goes to the `--report-dir` directory, which was not supplied, so the WC-4 contract path that steps 3 and 4 test does not exist for that run (and a post-creation run writes it only under `.dev/tasks/to-do/<id>/`, SPEC:92 column 3); AC-1.2 cannot pass for `workflow`. The reviser fixed the same clash for tdd in AC-2.2 (SPEC:200) but not here.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
