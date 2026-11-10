review: 1 of 3

# Merged first review (coordinator; MERGE rule over two independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 92bf2b5c18ede560458a50f5c8b243d0cc219695669278ee46d018c022240593
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 70bcaba9cc6756b379146599a9a34946ecca5351d1e7be0078abd08c95f15c63

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M3, M4, M5, M6, M7, M8, M10, M11. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M9 (verifier: The roadmap row sits in the table column headed "Unattended-mode gate resolution (WC-2)" (97), so the Y/n replacement is scoped to unattended mode and the candidate does not say it applies to a plain session.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md F1: *F1. The contract path rule in WC-4 cannot be followed by the commands the spec lists.** Severity MAJOR. Grade: blocking. Expert: Wiegers (lead), Cockburn.
- WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`/`--output-dir` (SPEC:62). SPEC:73 says the coordinator's brief gives the report path "so the report path is known before dispatch".
- SPEC:83 (adversarial) requires `<output>/adversarial/return-contract.yaml`, a subfolder. SPEC:87 (init-lite) takes `--output <file>`, not a directory. SPEC:90 (tdd) takes `--output <file>`. SPEC:92 (workflow) has no output flag; its contract lives under `.dev/tasks/to-do/<id>/`. SPEC:85 (cleanup-audit) uses a fixed `.claude-audit/` path. SPEC:105 (cli-portify) leaves the location unnamed.
- Grading sentence: an implementer who follows WC-4 and SPEC:73 has the coordinator open `<output-dir>/return-contract.yaml` for adversarial, but SPEC:83 makes the file `<output-dir>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist.
- Recommendation: state one rule per command in a table (path, and whether it is file-valued or directory-valued), or make every command take `--output-dir` and write the contract at its root. Priority: high. Quality impact: consistency.

### M2

#### M2.a, from round1-a.md F2: *F2. The P0 smoke runs use a brief that the contract says must carry `--unattended`, but P0 is before any command accepts that flag.** Severity MAJOR. Grade: blocking. Expert: Cockburn, Adzic.
- SPEC:73 says each Task's brief carries "the exact command line including `--unattended`". SPEC:180 says step 1 uses "the brief per section 2.3".
- SPEC:158 (P0) is "no command edits"; the flag is added in P1 (SPEC:159). AC-0.4 (SPEC:194) runs "the 7.2 live check" on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` with command lines that have no `--unattended`.
- Grading sentence: an implementer who follows AC-0.4 runs the P0 evidence with briefs that SPEC:73 forbids, so the P0 result, which section 1.4 (SPEC:43-44) treats as the test of the decision, is not a test of the contract's briefs.
- Recommendation: say that P0 briefs omit `--unattended` and that P0 evidence tests the Orca launch only, or move the `--unattended` requirement to P1 in SPEC:73 and SPEC:180. Priority: high. Quality impact: consistency, testability.

### M3

#### M3.a, from round1-a.md F3: *F3. WC-5 maps an empty or malformed contract to `succeeded`.** Severity MAJOR. Grade: blocking (FR-8 GAP with a concrete wrong outcome). Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers.
- SPEC:63: `--outcome failed` only "when the report says failed or blocked, or no report exists"; `--outcome succeeded` "otherwise". SPEC:183 (step 4) treats an empty contract (`test -s`) as a failed check.
- Grading sentence: an implementer who follows SPEC:63 as written sends `--outcome succeeded` for a zero-byte contract or for `status: done`, because neither is "failed", "blocked" or "no report"; SPEC:183 says the same file must not pass.
- Recommendation: `succeeded` only for a parsed contract whose status is `succeeded` or `partial`; every other case (missing, empty, unparseable, unknown status) is `failed`. Priority: high. Quality impact: completeness.

### M4

#### M4.a, from round1-a.md F4: *F4. WC-11 changes default output paths without limiting the change to unattended runs, which contradicts SA-1.** Severity MAJOR. Grade: blocking. Expert: Wiegers (traceability), Fowler.
- WC-11 (SPEC:69): "Default output paths carry a timestamp or the slug the coordinator passes". Only its second clause is scoped to unattended mode.
- SA-1 (SPEC:146): without `--unattended`, "every ... output path ... stays as it is today". The section 3.1 row for index-repo (SPEC:86) uses the fixed `PROJECT_INDEX.md` and resumes with `mode=update`.
- Grading sentence: an implementer who follows SPEC:69 gives standalone `/sc:index-repo` a timestamped default name, which breaks SA-1 as written, and the text does not say that WC-11 is limited to unattended runs.
- Recommendation: scope the first clause of WC-11 to unattended runs with a coordinator-passed slug, and state that standalone defaults are unchanged. Priority: high. Quality impact: consistency.

### M5

#### M5.a, from round1-b.md B1: B1. AC-0.4 step 4 reads YAML keys from a Markdown report
- Expert: Adzic (testable examples).
- Location: SPEC:183 (step 4 asserts `d['status']` and `d['command']` from a YAML load), SPEC:194 (AC-0.4 says step 4 "uses the command's existing report file"). INV-B:49 (`/sc:troubleshoot` writes `REPORT.md`, `report_path`).
- Grading sentence: An implementer who follows AC-0.4 runs step 4 on the troubleshoot `REPORT.md`, which is Markdown, so `yaml.safe_load` returns text or a dict without `status` and `command`, and the step fails on a correct run.
- Priority: High. Quality impact: AC-0.4 cannot close Phase 0 as written.
- Recommendation: in P0, split step 4 into "file exists and non-empty" for report files and the YAML field check only for files that are YAML contracts. Confirm whether the workflow contract carries a `command` key (INV-B:272 lists `status`, `plan_path`, `reflect_report_path` only; UNVERIFIED).

### M6

#### M6.a, from round1-b.md B2: B2. Step 6 fails whenever the phase's own edits are uncommitted
- Expert: Adzic.
- Location: SPEC:185 (pass: "only files under the brief's output directory ... appear"), SPEC:158-162 (each phase edits tracked files), SPEC:194, 196, 201 (AC-0.4, AC-1.2, AC-2.3 all depend on step 6). No step in SPEC:180-186 commits or snapshots the tree.
- Grading sentence: An implementer who writes the P0 files (WORKER-CONTRACT.md, the HOW-WE-WORK section, the test file) in the worktree and then runs step 6 as written sees those modified or untracked paths in `git status --short`, which the pass condition does not allow, and the spec gives no step that commits or snapshots first.
- Priority: High. Quality impact: every live check after P0 fails for reasons unrelated to the worker.
- Recommendation: make step 6 compare `git status --short` taken before dispatch with the one taken after, and pass only if the new entries are under the output directory or are documented artifacts.

### M7

#### M7.a, from round1-b.md B3: B3. AC-0.4 requires "no Agent-tool wrapper, verified in the step-5 transcript", and step 5 does not test it
- Expert: Wiegers (criteria must match their verification).
- Location: SPEC:194 (AC-0.4 "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"), SPEC:184 (step 5 pass: "no AskUserQuestion call").
- Grading sentence: An implementer who runs step 5 as written searches only for `AskUserQuestion`, so no evidence about an Agent-tool wrapper is produced, and AC-0.4 cannot pass as written.
- Priority: High. Quality impact: WC-7 (SPEC:65) is untested.
- Recommendation: add to step 5 a pass condition that the transcript has no Agent or Task tool use whose prompt is the `/sc:` command, and say which transcript field to check.

### M8

#### M8.a, from round1-b.md B4: B4. AC-2.2 requires `status: blocked` for every P2 command, but six P2 commands have no blocked path
- Expert: Adzic and Crispin (examples and boundary cases).
- Location: SPEC:200 (AC-2.2: "contract `status: blocked` with a non-empty `blocked_question`"), SPEC:160 (P2 set), and the rows that resolve without a blocked outcome: SPEC:100 (auggie-review: defaults `--no-post-pr --no-remediation-offer`), SPEC:103 (cleanup: lists unapplied items, does not block), SPEC:110 (improve: same), SPEC:116 (research: pins `--strategy planning`), SPEC:88 (reflect: headless auto-accept, no gate without `--remediate`), SPEC:122 (tasklist: passes `--unattended` down, no gate).
- Grading sentence: An implementer who follows the cleanup row builds a run that applies auto-fix items and lists the rest in the report, so no gate resolves as blocked and AC-2.2 fails because it expects `status: blocked`.
- Priority: High. Quality impact: AC-2.2 cannot be satisfied for six of 15 P2 commands, so the phase cannot pass its own check.
- Recommendation: state AC-2.2 as "blocked where the row names a blocked path, otherwise the default is recorded in the contract", and give one trigger input for each command that has a blocked path. Only two of the 15 have inputs now (SPEC:200).

### M10

#### M10.a, from round1-b.md B6: B6. `load` must write a contract (WC-4, AC-1.1, AC-1.2) but its row and decision say it writes no file
- Expert: Wiegers (traceability) and Fowler (interface).
- Location: SPEC:62 (WC-4: contract "written on every outcome" in unattended mode), SPEC:112 (load row: report "none (see note)"), SPEC:159 (P1 includes load), SPEC:195 (AC-1.1 requires `return-contract.yaml` in every section 3.1 and 3.2 command), SPEC:196 (AC-1.2 runs on each P1 command), SPEC:265 (decision: "a report file would be an unrequested addition"). INV-B:65 (load "only loads context into the current session").
- Grading sentence: An implementer who follows the load row writes no contract, and AC-1.1 and AC-1.2 fail for `load`; an implementer who follows WC-4 writes one, which the decision at SPEC:265 forbids, so the two texts contradict each other.
- Priority: High. Quality impact: P1 cannot pass for `load`.
- Recommendation: exempt `load` from WC-4 by name in WC-4 and in AC-1.1 and AC-1.2, or give it a one-line contract. Either way update SPEC:265.

### M11

#### M11.a, from round1-b.md B7: B7. The workflow contract path conflicts with WC-4 and does not exist for a pre-creation STOP
- Expert: Fowler and Hohpe (interfaces and report channels).
- Location: SPEC:62 (WC-4: `<output-dir>/return-contract.yaml`, "including stops before any other output exists", and the path is known before dispatch), SPEC:92 (workflow row: `.dev/tasks/to-do/<id>/return-contract.yaml`; "Write the contract for pre-creation STOPs too"), SPEC:198 (AC-1.4). INV-B:272 (`.dev/tasks/to-do/<id>/`; not written for pre-creation STOPs). SPEC:73 (the coordinator must know the path before dispatch).
- Grading sentence: An implementer who follows WC-4 writes a pre-creation STOP contract to `<output-dir>`, but workflow has no output flag in row SPEC:92, and the row's `<id>` directory does not exist before package creation, so the path the coordinator must know before dispatch (SPEC:73) is undefined for that case.
- Priority: High. Quality impact: a blocked or failed workflow run leaves the coordinator no report to read.
- Recommendation: give workflow a `--output` (or a fixed STOP-contract path) and state which location wins for each outcome.

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M9 (verifier: The roadmap row sits in the table column headed "Unattended-mode gate resolution (WC-2)" (97), so the Y/n replacement is scoped to unattended mode and the candidate does not say it applies to a plain session.)

#### M9.a, from round1-b.md B5: B5. SA-1 forbids prompt changes without `--unattended`; the roadmap row removes the Y/n prompt unconditionally
- Expert: Wiegers (requirement conflict).
- Location: SPEC:146 (SA-1: "every prompt ... stays as it is today" without `--unattended`), SPEC:149 (SA-4 allows fixes that "keep the standalone behaviour or correct a documented defect"), SPEC:118 (roadmap row: "the 'Resume? [Y/n]' prompt is replaced by the explicit resume flag (resume only when passed)", with no `--unattended` qualifier). Source of the prompt: INV-B:40 (`sk/sc-roadmap-protocol/SKILL.md:433-438`, UNVERIFIED in this sandbox).
- Grading sentence: An implementer who follows the roadmap row removes the Y/n prompt for a plain session with no flags, which SA-1 (SPEC:146) forbids, and SA-4 (SPEC:149) permits only as a defect fix, so the two texts contradict each other.
- Priority: High. Quality impact: standalone users lose a prompt they rely on; the SA-1 check (AC-2.5, SPEC:203) would catch it only manually.
- Recommendation: scope the roadmap change to `--unattended`, or name a standalone exception in SA-1 and list each one. The same question applies to the adversarial contract-filename fix (row SPEC:83, a standalone output path under SA-1).

## Follow-up candidates

Listed in the two source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M3, M4, M5, M6, M7, M8, M10, M11.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
