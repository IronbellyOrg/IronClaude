review: 1 of 3

# Merged first review (coordinator; MERGE rule over two independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 2b336029cfd53930e600a5fb4aab93a7c9b0c90caf43f6269f828f85e72a47ee
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 373bbda2cfdc8a4fafe2fd8a2ee838d161c34c9125bf6a496ff3ac7771bcd12a

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M3, M4, M5. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M6 (verifier: AC-2.3 does not say single run, and the row does not say what `--resume <contract>` does after an approval, so "no input can reach succeeded" needs an assumption the text does not state.); M7 (verifier: AC-4.2 says "no authorization flags", not "no pre-tag choice", and WC-4 says "at least", so a skipped-step list is not excluded; the stated failure needs the assumptions that the pre-tag choice is absent and that no extra field is allowed.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md F-1: F-1 [MAJOR, blocking] Acceptance check AC-1.1 requires a contract section on commands that section 3 says get none
Experts: Wiegers (lead, traceability), Adzic (the checkable example fails), Crispin (acceptance test completeness).

Stated texts that contradict:
- Candidate line 195, AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Candidate line 112, `/sc:load` row: report column "none (see note)", "Other required change": "none: use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)". Line 159 repeats it ("load (usage line only)").
- Candidate line 265, Decisions: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- Candidate line 79 (3.1 intro): "The only command changes are the small fixes in the last column"; the `brainstorm` row (line 84) and `init-lite` row (line 87) say "None" in that column. Line 76 says only "changed" commands gain the section, and line 159 gives the P1 command list without brainstorm or init-lite.

Grading sentence: An implementer who follows line 112, line 265 and line 79 as written changes `/sc:load` only in its usage line and leaves `/sc:brainstorm` and `/sc:init-lite` untouched, and builds a Phase 1 whose own acceptance test (AC-1.1, line 195) fails on those three commands, because AC-1.1 requires every command in 3.1-3.2 to carry the section. The implementer who instead satisfies AC-1.1 adds a contract section to `/sc:load`, which line 265 rejects. The text itself offers no way to pass both. Two stated texts contradict, so this is blocking.

Attack (Whittaker, FR-2.2 Divergence): the AC-1.1 quantifier "every command in sections 3.1-3.2" and the per-row "change" column partition the 37 commands differently; the boundary case is the set difference (load, brainstorm, init-lite, plus any other row with "None").

Recommendation: narrow AC-1.1 to the commands whose rows add a section, or have the rows for these three say they gain the section. Prefer narrowing the test (smaller diff).

### M2

#### M2.a, from round1-a.md F-2: F-2 [MAJOR, blocking] WC-4 defines the report path from a coordinator-passed directory, yet several commands take a file, and two acceptance criteria depend on that path
Experts: Cockburn (the coordinator's goal: open the contract), Wiegers (testable and unambiguous), Hohpe (the interface between command and coordinator), Whittaker (FR-2.3 Sentinel Collision: one flag name carries two meanings).

Stated texts:
- Candidate line 62, WC-4: the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Line 73 (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)". Line 182 (7.2 step 3): "its report path is the WC-4 contract path".
- Candidate line 90, `tdd` row: brief must pass "`--output <file>`"; line 87, `init-lite`: "`--output <file>`"; line 120, `spec-panel`: "add `--output`" (the spec-panel `--output` is a file in the same row's evidence at `cmd/spec-panel.md`; UNVERIFIED here); line 200, AC-2.2: "`/sc:tdd "auth" --unattended --output <file>`" must yield a contract with `status: blocked` and a non-empty `blocked_question`.
- Candidate lines 92 and 198, `workflow` row and AC-1.4: the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` and must now also be written "for pre-creation STOPs", where no `<id>` exists yet.

Grading sentence: An implementer who follows WC-4 as written builds the tdd contract at `<file>/return-contract.yaml` (the passed `--output` value is the TDD file, not a directory), and that path cannot exist as a directory entry beside a file of the same name; AC-2.2 and the 7.2 step 3 and step 4 checks then cannot locate or open the contract, so they cannot pass. For `workflow` the stated path needs an `<id>` that a pre-creation STOP does not have, so AC-1.4 has no defined location to check. A stated text that an acceptance criterion cannot pass is blocking.

Recommendation: state one rule for the contract location that covers a file-valued `--output` (for example a sibling file, or a separate `--report-dir` as the already-defined mechanism in other contract writers would suggest) and for workflow's pre-creation case; or have the brief always pass a dedicated directory flag for the contract.

#### M2.b, from round1-b.md B1: B1. CRITICAL (blocking): the contract path rule contradicts every command whose `--output` is a file
- Experts: Wiegers, Adzic, Whittaker (Sentinel Collision / Divergence attack).
- Stated text 1, spec:62 (WC-4): the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the worker passes that path as `--report-path`.
- Stated text 2, spec:90 (tdd, section 3.1): brief passes `--output <file>`; report is "the TDD at `--output`". spec:87 (init-lite): `--output <file>`. spec:120 (spec-panel): "add `--output`". spec:107 (document): "require an explicit output". spec:108 (explain): "write the explanation to a file". Inventory: `INV-B:47` (tdd: "TDD file at `--output`"), `INV-A:55` (init-lite: "`.dev/superclaude/context-audit.md` or `--output`").
- Stated text 3, spec:200 (AC-2.2): the gate-trigger example `/sc:tdd "auth" --unattended --output <file>` must end with "contract `status: blocked` with a non-empty `blocked_question`", and spec:182 step 3 requires "its report path is the WC-4 contract path".
- Grading sentence: an implementer who follows WC-4 as written builds a tdd (and init-lite, spec-panel, document) that writes `<file>/return-contract.yaml` next to a path that is a regular file, or a contract at no defined path, and that is wrong because `--output <file>` names a file, so no `<output-dir>` exists and AC-2.2 (spec:200) and live-check steps 3-4 (spec:182-183) cannot locate or read the contract.
- Concrete attack (Whittaker, Divergence): input `--output .dev/x/tdd.md` -> WC-4 says "directory" -> the contract path is `.dev/x/tdd.md/return-contract.yaml`, which cannot be created when `tdd.md` is a file; the blocked case (a topic-only prompt, which is the AC-2.2 case) produces no TDD, so the path may be missing and the report is unreadable.
- Recommendation: state one rule for file-valued `--output` (for example "the contract goes in the parent directory, or in a separate caller-supplied `--report-dir`") and apply it in WC-4, in the section 3 rows named above and in the AC-2.2 example.
- Priority: High. Quality-impact estimate: removes a path ambiguity that blocks the check on at least 4 of the 37 worker-capable commands.

### M3

#### M3.a, from round1-b.md B2: B2. CRITICAL (blocking): AC-0.4 requires a contract that does not exist in Phase 0
- Experts: Wiegers, Crispin-style testability reading, Nygard.
- Stated text 1, spec:194 (AC-0.4): runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow ... --handoff none` and `/sc:adversarial ...`; "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1".
- Stated text 2, spec:182 (live-check step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Stated text 3, spec:91 and spec:92: troubleshoot's report is `REPORT.md`; workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (id chosen by the command). spec:159 puts the WC-4 contract and the output flags in P1; `INV-B:49` and `INV-B:52` agree that these commands have no `--output` directory today.
- Grading sentence: an implementer who runs AC-0.4 exactly as written gets a troubleshoot worker whose `worker_done --report-path` is `REPORT.md` and whose contract does not exist, so step 3 (spec:182) cannot pass, and AC-0.4 says step 3 must pass; that is two stated texts of the same criterion contradicting each other.
- Related defect inside the same criterion: spec:73 and spec:62 require the output directory to be "known before dispatch", but spec:91-92 list no `--output` for troubleshoot or workflow in "Brief must pass", and workflow's directory depends on a generated `<id>`. The coordinator cannot name the path in the brief, so the "known before dispatch" rule cannot hold for two of the three Phase 0 smoke commands.
- A further inconsistency: spec:83 fixes adversarial's contract name to `<output>/adversarial/return-contract.yaml` while WC-4 says `<output-dir>/return-contract.yaml` (spec:62); the two are the same only if `<output-dir>` is read as `<output>/adversarial`, which no text says.
- Recommendation: make step 3 of the live check read "report path is the command's named report (the WC-4 contract from P1 on)", and list the output directory or the report location the coordinator must read in the "Brief must pass" column for troubleshoot, workflow, reflect, cleanup-audit and index-repo, or state that the coordinator finds it from `worker_done --report-path`.
- Priority: High.

### M4

#### M4.a, from round1-b.md B3: B3. MAJOR (blocking): AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- Experts: Wiegers (traceability), Cockburn.
- Stated text 1, spec:195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Stated text 2, spec:112 (load row): report "none (see note)", resume "n/a", change "none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line", phase "P1 (usage line only)". spec:265 (Decision "`/sc:load` handling"): "a report file would be an unrequested addition". `INV-B:31` ("writes no file; use as a brief step, not a task").
- Stated text 3, spec:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`"; spec:159 lists load in P1; spec:183 (step 4) requires `test -s <contract>` and a parsed `status`.
- Grading sentence: an implementer who follows the load row builds a load.md with only a usage-line fix and no `## Unattended mode` section and no contract, and that is wrong because AC-1.1 requires the section naming `return-contract.yaml` for all of 3.1-3.2 and AC-1.2 step 4 requires a contract file, so both criteria fail for load whichever way it is built (adding the section and file contradicts spec:112 and spec:265).
- Recommendation: exclude load from AC-1.1/AC-1.2 by name, or state that load gets a no-op `## Unattended mode` section and no contract.
- Priority: High.

### M5

#### M5.a, from round1-b.md B4: B4. MAJOR (blocking): AC-2.2 demands a `blocked` contract from P2 commands whose gate does not resolve as blocked
- Experts: Wiegers, Adzic (example consistency), Whittaker (Divergence).
- Stated text 1, spec:200 (AC-2.2): "Gate-trigger run per P2 command ... **Pass:** `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`".
- Stated text 2, spec:160 lists the P2 set: auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot. Their section 3 rows resolve gates as follows:
  - auggie-review (spec:100): the gate is turned off by `--no-post-pr` / `--no-remediation-offer`; nothing blocks.
  - cleanup and improve (spec:103, spec:110): apply only allowed items and list the rest; the run succeeds with deferred items.
  - research (spec:116): `--unattended` pins `--strategy planning`; no blocked outcome.
  - tasklist (spec:122): passes `--unattended` to reflect so the headless rule applies; no blocked outcome.
  - reflect (spec:88): `--remediate` follows the headless auto-accept rule; no blocked outcome.
  - release-split (spec:89) and tdd (spec:90) block only for specific inputs.
- Grading sentence: an implementer who follows the section 3 rows builds auggie-review, cleanup, improve, research, tasklist and reflect that finish `succeeded` under `--unattended` on any input, and that is wrong because AC-2.2 requires every P2 command to produce `worker_done --outcome failed` with `status: blocked` on its gate-trigger run, which those commands have no input for; the criterion cannot pass as written for at least six of the fifteen commands it covers.
- Recommendation: restrict AC-2.2 to the P2 commands whose row says "blocked" (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, tdd, troubleshoot, release-split, and the blocked cases of cli-eval) and give the other commands a "gate removed" check (for example AC-2.4's before/after counts, or a run that shows the default applied and no wait).
- Priority: High.

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M6 (verifier: AC-2.3 does not say single run, and the row does not say what `--resume <contract>` does after an approval, so "no input can reach succeeded" needs an assumption the text does not state.)

#### M6.a, from round1-b.md B5: B5. MAJOR (blocking): AC-2.3 cannot pass for `/sc:cli-portify`
- Experts: Wiegers, Cockburn (goal reachability).
- Stated text 1, spec:201 (AC-2.3): "Happy-path run per P2 command with every required flag in the brief -> 7.2 passes with `--outcome succeeded`".
- Stated text 2, spec:105 (cli-portify row): "each of the three approval gates resolves as blocked with the artifact to review named in the contract"; the only resume is "a `--resume <contract>` flag". No flag, default or caller-supplied value is offered that approves a gate (WC-2 option (a) and (b) are not applied to this command). `INV-A:45` and `INV-A:68` record the three always-on approval gates.
- Grading sentence: an implementer who follows the cli-portify row builds a command that always stops at the first approval gate with `status: blocked`, and that is wrong because AC-2.3 requires a single worker run of every P2 command to end `succeeded`, which no input to this command can reach.
- Recommendation: either name an approval input (for example a pre-approved-phases flag) so one run can finish, or exempt cli-portify from AC-2.3 and give it a two-run check (blocked, then `--resume`).
- Priority: High.

### M7 (verifier: AC-4.2 says "no authorization flags", not "no pre-tag choice", and WC-4 says "at least", so a skipped-step list is not excluded; the stated failure needs the assumptions that the pre-tag choice is absent and that no extra field is allowed.)

#### M7.a, from round1-b.md B6: B6. MAJOR (blocking): AC-4.2 expects skipped-step reporting from a run that the post-release row blocks first
- Experts: Nygard, Wiegers, Whittaker (Sequence attack).
- Stated text 1, spec:113 (post-release row): "require an explicit `--output` and an explicit pre-tag choice, else blocked; VM, real-target install, commit and PR off unless the brief authorizes them".
- Stated text 2, spec:209 (AC-4.2): `/sc:post-release <version> --unattended --output <dir>` "with no authorization flags"; pass: "no install, VM, commit or PR ... the contract lists each skipped outward step".
- Stated text 3, spec:62 (WC-4): the contract fields are `status`, `command`, `report_path`, `artifacts`, and `blocked_question`; there is no field for skipped steps.
- Grading sentence: an implementer who follows the row builds a post-release that, given the AC-2.2 invocation (no pre-tag choice), stops at the pre-tag gate with `status: blocked` and a `blocked_question` before any outward step is reached, and that is wrong because AC-4.2 requires the contract to list "each skipped outward step", a list that neither WC-4 defines nor a blocked run produces.
- Recommendation: add the pre-tag choice to the AC-4.2 command and define the skipped-step field (or reuse `artifacts`/`report_path`), or state that a blocked contract at the pre-tag gate passes the check.
- Priority: High.

## Follow-up candidates

Listed in the two source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M3, M4, M5.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
