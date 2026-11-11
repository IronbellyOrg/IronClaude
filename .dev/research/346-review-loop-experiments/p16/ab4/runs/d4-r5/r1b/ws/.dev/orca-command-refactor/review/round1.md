review: 1 of 3

# Spec-panel critique, round 1 (first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none (`baseline: missing`; first review of the full document)
- Lint: `.dev/orca-command-refactor/review/lint-1.md` (sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`), checks REF, findings 0. Its header hash equals the candidate hash above. No lint id exists to confirm or dismiss (`lint-1.md:3-5`).
- Reviewer model actually used: claude-sonnet-5-5
- Panel (critique mode, requirements + architecture focus): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active).
- Scope note: this is one of the two first reviews the prompt file calls for. The MERGE rule is the coordinator's job (`~/.claude/rules/prompts/document_review_loop_prompts.md:36`). Finding ids here are `B1..B6`.
- Evidence rule: only the candidate, the three files under `inventory/`, `README.md` and `lint-1.md` are in the workspace. Every `src/`, `CLAUDE.md`, `EVIDENCE.md`, Orca-guide or `pyproject.toml` citation inside the candidate is UNVERIFIED by this review. The inventory lines the candidate cites for its own claims were read where they are used below.

## Method for the per-criterion check
Each of AC-C1..C5 (spec:172-176), the seven live-check steps (spec:180-186), AC-0.1..0.4 (spec:191-194), AC-1.1..1.4 (spec:195-198), AC-2.1..2.5 (spec:199-203), AC-3.1..3.4 (spec:204-207) and AC-4.1..4.3 (spec:208-210) was walked against the section 2 and section 3 text it covers. The verdict table is in the section "Criterion-by-criterion verdicts". Grading follows the first-review grading check: a finding is blocking only when a sentence of the form "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (two stated texts contradict, or a stated text that an acceptance criterion cannot pass).

=== REQUIREMENTS ANALYSIS ===

### B1. CRITICAL (blocking): the contract path rule contradicts every command whose `--output` is a file
- Experts: Wiegers, Adzic, Whittaker (Sentinel Collision / Divergence attack).
- Stated text 1, spec:62 (WC-4): the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the worker passes that path as `--report-path`.
- Stated text 2, spec:90 (tdd, section 3.1): brief passes `--output <file>`; report is "the TDD at `--output`". spec:87 (init-lite): `--output <file>`. spec:120 (spec-panel): "add `--output`". spec:107 (document): "require an explicit output". spec:108 (explain): "write the explanation to a file". Inventory: `INV-B:47` (tdd: "TDD file at `--output`"), `INV-A:55` (init-lite: "`.dev/superclaude/context-audit.md` or `--output`").
- Stated text 3, spec:200 (AC-2.2): the gate-trigger example `/sc:tdd "auth" --unattended --output <file>` must end with "contract `status: blocked` with a non-empty `blocked_question`", and spec:182 step 3 requires "its report path is the WC-4 contract path".
- Grading sentence: an implementer who follows WC-4 as written builds a tdd (and init-lite, spec-panel, document) that writes `<file>/return-contract.yaml` next to a path that is a regular file, or a contract at no defined path, and that is wrong because `--output <file>` names a file, so no `<output-dir>` exists and AC-2.2 (spec:200) and live-check steps 3-4 (spec:182-183) cannot locate or read the contract.
- Concrete attack (Whittaker, Divergence): input `--output .dev/x/tdd.md` -> WC-4 says "directory" -> the contract path is `.dev/x/tdd.md/return-contract.yaml`, which cannot be created when `tdd.md` is a file; the blocked case (a topic-only prompt, which is the AC-2.2 case) produces no TDD, so the path may be missing and the report is unreadable.
- Recommendation: state one rule for file-valued `--output` (for example "the contract goes in the parent directory, or in a separate caller-supplied `--report-dir`") and apply it in WC-4, in the section 3 rows named above and in the AC-2.2 example.
- Priority: High. Quality-impact estimate: removes a path ambiguity that blocks the check on at least 4 of the 37 worker-capable commands.

### B2. CRITICAL (blocking): AC-0.4 requires a contract that does not exist in Phase 0
- Experts: Wiegers, Crispin-style testability reading, Nygard.
- Stated text 1, spec:194 (AC-0.4): runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow ... --handoff none` and `/sc:adversarial ...`; "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1".
- Stated text 2, spec:182 (live-check step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Stated text 3, spec:91 and spec:92: troubleshoot's report is `REPORT.md`; workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (id chosen by the command). spec:159 puts the WC-4 contract and the output flags in P1; `INV-B:49` and `INV-B:52` agree that these commands have no `--output` directory today.
- Grading sentence: an implementer who runs AC-0.4 exactly as written gets a troubleshoot worker whose `worker_done --report-path` is `REPORT.md` and whose contract does not exist, so step 3 (spec:182) cannot pass, and AC-0.4 says step 3 must pass; that is two stated texts of the same criterion contradicting each other.
- Related defect inside the same criterion: spec:73 and spec:62 require the output directory to be "known before dispatch", but spec:91-92 list no `--output` for troubleshoot or workflow in "Brief must pass", and workflow's directory depends on a generated `<id>`. The coordinator cannot name the path in the brief, so the "known before dispatch" rule cannot hold for two of the three Phase 0 smoke commands.
- A further inconsistency: spec:83 fixes adversarial's contract name to `<output>/adversarial/return-contract.yaml` while WC-4 says `<output-dir>/return-contract.yaml` (spec:62); the two are the same only if `<output-dir>` is read as `<output>/adversarial`, which no text says.
- Recommendation: make step 3 of the live check read "report path is the command's named report (the WC-4 contract from P1 on)", and list the output directory or the report location the coordinator must read in the "Brief must pass" column for troubleshoot, workflow, reflect, cleanup-audit and index-repo, or state that the coordinator finds it from `worker_done --report-path`.
- Priority: High.

### B3. MAJOR (blocking): AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- Experts: Wiegers (traceability), Cockburn.
- Stated text 1, spec:195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Stated text 2, spec:112 (load row): report "none (see note)", resume "n/a", change "none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line", phase "P1 (usage line only)". spec:265 (Decision "`/sc:load` handling"): "a report file would be an unrequested addition". `INV-B:31` ("writes no file; use as a brief step, not a task").
- Stated text 3, spec:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`"; spec:159 lists load in P1; spec:183 (step 4) requires `test -s <contract>` and a parsed `status`.
- Grading sentence: an implementer who follows the load row builds a load.md with only a usage-line fix and no `## Unattended mode` section and no contract, and that is wrong because AC-1.1 requires the section naming `return-contract.yaml` for all of 3.1-3.2 and AC-1.2 step 4 requires a contract file, so both criteria fail for load whichever way it is built (adding the section and file contradicts spec:112 and spec:265).
- Recommendation: exclude load from AC-1.1/AC-1.2 by name, or state that load gets a no-op `## Unattended mode` section and no contract.
- Priority: High.

### B4. MAJOR (blocking): AC-2.2 demands a `blocked` contract from P2 commands whose gate does not resolve as blocked
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

### B5. MAJOR (blocking): AC-2.3 cannot pass for `/sc:cli-portify`
- Experts: Wiegers, Cockburn (goal reachability).
- Stated text 1, spec:201 (AC-2.3): "Happy-path run per P2 command with every required flag in the brief -> 7.2 passes with `--outcome succeeded`".
- Stated text 2, spec:105 (cli-portify row): "each of the three approval gates resolves as blocked with the artifact to review named in the contract"; the only resume is "a `--resume <contract>` flag". No flag, default or caller-supplied value is offered that approves a gate (WC-2 option (a) and (b) are not applied to this command). `INV-A:45` and `INV-A:68` record the three always-on approval gates.
- Grading sentence: an implementer who follows the cli-portify row builds a command that always stops at the first approval gate with `status: blocked`, and that is wrong because AC-2.3 requires a single worker run of every P2 command to end `succeeded`, which no input to this command can reach.
- Recommendation: either name an approval input (for example a pre-approved-phases flag) so one run can finish, or exempt cli-portify from AC-2.3 and give it a two-run check (blocked, then `--resume`).
- Priority: High.

### B6. MAJOR (blocking): AC-4.2 expects skipped-step reporting from a run that the post-release row blocks first
- Experts: Nygard, Wiegers, Whittaker (Sequence attack).
- Stated text 1, spec:113 (post-release row): "require an explicit `--output` and an explicit pre-tag choice, else blocked; VM, real-target install, commit and PR off unless the brief authorizes them".
- Stated text 2, spec:209 (AC-4.2): `/sc:post-release <version> --unattended --output <dir>` "with no authorization flags"; pass: "no install, VM, commit or PR ... the contract lists each skipped outward step".
- Stated text 3, spec:62 (WC-4): the contract fields are `status`, `command`, `report_path`, `artifacts`, and `blocked_question`; there is no field for skipped steps.
- Grading sentence: an implementer who follows the row builds a post-release that, given the AC-2.2 invocation (no pre-tag choice), stops at the pre-tag gate with `status: blocked` and a `blocked_question` before any outward step is reached, and that is wrong because AC-4.2 requires the contract to list "each skipped outward step", a list that neither WC-4 defines nor a blocked run produces.
- Recommendation: add the pre-tag choice to the AC-4.2 command and define the skipped-step field (or reuse `artifacts`/`report_path`), or state that a blocked contract at the pre-tag gate passes the check.
- Priority: High.

=== ARCHITECTURE ANALYSIS ===

No blocking architectural finding. The decision in section 1 (coordinator above, commands as workers, no Orca calls inside commands) is internally consistent with R1-R5 (spec:33-37), SA-2 (spec:147) and WC-7/WC-8 (spec:65-66). The evidence for the decision is stated as incomplete in section 1.4 (spec:41-45), and Phase 0 is the first test of it (spec:158, spec:194). Items below are Medium or minor.

## Criterion-by-criterion verdicts

"Can pass" means the check can pass as written for every command and phase it covers.

| Check | Can pass as written? | Reason (cite) |
|---|---|---|
| AC-C1 (spec:172) | Conditional (Medium M2) | Pre-change tree: passes per E5 (spec:25). It also scans `src/superclaude/core`, where P0 adds the contract and an Orca section (spec:158); whether those texts avoid `orca orchestration ...` is not stated. |
| AC-C2 (spec:173) | Yes | `make verify-sync` is a repo command (CLAUDE.md, not checkable here, UNVERIFIED). |
| AC-C3 (spec:174) | Yes | Baseline-diff design; no assumption of a clean suite. |
| AC-C4 (spec:175) | Yes | Only staged `.claude/` paths. |
| AC-C5 (spec:176) | Conditional (Medium M3) | Passes only if new flags go on new lines; a flag added to a one-line Usage entry shows up as a `-` line. |
| Live step 1 (spec:180) | Yes | Verbs and flags exist in `CAPS:84` (`task-create --spec`), `CAPS:140`; `state: ready` per `CAPS:46`. |
| Live step 2 (spec:181) | Yes for a worker that never asks | A worker that follows WC-3 (spec:61) and uses `ask` may show a wait (Medium M1). |
| Live step 3 (spec:182) | No in P0 (B2); no for file-valued `--output` (B1) | See B1, B2. |
| Live step 4 (spec:183) | No in P0 (B2), no for load (B3), no for file-valued `--output` (B1) | See findings. |
| Live step 5 (spec:184) | Yes (Medium M5 on string matching) | `worker-read --source transcript` exists (`CAPS:131`). |
| Live step 6 (spec:185) | Yes with the "documented artifacts" carve-out | Covers workflow's `.dev/tasks/to-do/<id>/`. |
| Live step 7 (spec:186) | Yes | `CAPS:113`. |
| AC-0.1 (spec:191) | Yes | Pure import check. |
| AC-0.2 (spec:192) | Yes | `cmp` of two files. |
| AC-0.3 (spec:193) | Yes | |
| AC-0.4 (spec:194) | No | B2. |
| AC-1.1 (spec:195) | No for load (B3) | |
| AC-1.2 (spec:196) | No for load (B3), conditional for file-valued `--output` commands (B1) | |
| AC-1.3 (spec:197) | Yes | |
| AC-1.4 (spec:198) | Yes | Matches spec:83, spec:92. |
| AC-2.1 (spec:199) | Yes | |
| AC-2.2 (spec:200) | No | B4, B1. |
| AC-2.3 (spec:201) | No for cli-portify | B5. |
| AC-2.4 (spec:202) | Yes | Counts via `gh api repos/IronbellyOrg/IronClaude/...` (fork-only form). |
| AC-2.5 (spec:203) | Yes (manual) | |
| AC-3.1 (spec:204) | Yes | |
| AC-3.2 (spec:205) | Yes | Matches spec:118. |
| AC-3.3 (spec:206) | Yes | Matches spec:125. |
| AC-3.4 (spec:207) | Yes | Matches spec:119. |
| AC-4.1 (spec:208) | Yes | Matches spec:109. |
| AC-4.2 (spec:209) | No | B6. |
| AC-4.3 (spec:210) | Conditional | Only if D3 allows it; "no single tool call exceeds 240 s" depends on poll-script runtime, which spec:114 and UNVERIFIED item 12 (spec:283) leave open. Not graded blocking because the criterion is already conditional. |

## Guard Condition Boundary Table
The spec states thresholds and guards in WC-10 (4-minute waits), WC-2 (gate resolution), the confidence guard of `/sc:task` (spec:121) and the AC pass conditions. Rows below are the guards where a degenerate input changes an acceptance outcome. Classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 `<output-dir>` | spec:62 | Zero/Empty | `--output` absent | n/a | tdd/spec-panel/document: "require/add an output" (spec:90, 107, 120); troubleshoot/workflow: none stated (spec:91-92) | GAP (B2) |
| WC-4 `<output-dir>` | spec:62 | Legitimate Edge Case | `--output` is a file | false (not a directory) | unspecified | GAP (B1) |
| WC-2(c) blocked | spec:60 | Zero/Empty | blocked before any output exists | true | contract written "including stops before any other output exists" (spec:62) | OK |
| WC-2(c) vs gate removal | spec:60, 200 | Typical | gate resolved by default or flag | no blocked contract | AC-2.2 demands a blocked contract | GAP (B4) |
| WC-10 wait split | spec:68 | Maximum/Overflow | single call over 5 minutes | split to <= 4 minutes | stated; checked only for pr-submit (spec:210) | OK (coverage note M4) |
| WC-10 wait split | spec:68 | Sentinel Value Match | poll-interval or timeout value of exactly 240 s or 300 s | true/false at the boundary | not specified (spec:114 leaves poll runtime UNVERIFIED) | GAP (Medium) |
| `/sc:task` confidence | spec:121 | Typical | below 0.70 | true | blocked | OK |
| `/sc:task` confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | not stated (the row says "below 0.70") | follows inventory text `INV-B:45` "confidence < 0.70" | OK |
| WC-5 outcome mapping | spec:63 | One/Minimal | `partial` | maps to `succeeded` | stated | OK |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | no report exists on a stop before the report step | maps to `failed` | stated | OK |
| `--unattended` on a coordinator-only command | spec:128 | Sentinel Value Match | `--unattended` passed to `/sc:pm` | n/a | "get no `--unattended` mode" (spec:128) but no refusal behavior is defined | GAP (Medium) |

Classes left out: Maximum/Overflow for WC-2 and WC-5 (they take no numeric input).

## Quantity Flow note
Pipeline Dimensional Analysis (FR-17) does not trigger: the spec has a coordinator -> worker -> report chain with one report per Task, not a multi-stage data pipeline whose counts diverge. One count claim was checked: "43 commands = 10 + 27 + 6" (spec:76). The 3.1 table lists 10 rows (spec:83-92), the 3.2 table lists 27 rows (spec:99-125), section 4 lists 6 (spec:132-137). The counts hold.

## Whittaker attack coverage (no further blocking finding)
- Zero/Empty: covered by the guard table; produced B1 and B2.
- Divergence: produced B4 (gate resolved by default versus blocked).
- Sentinel Collision: `--unattended` on a coordinator-only command and the 240 s/300 s boundary (Medium, above).
- Sequence: produced B6 (a gate earlier in the sequence than the step the AC inspects).
- Accumulation: no counter or buffer in scope other than the circuit-breaker count of 3 (`CAPS:116`), which the spec does not depend on.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium
- M1. WC-3 (spec:61) lets a worker with a preamble "instead ask the coordinator once" when a gate would resolve as blocked, while AC-2.2 (spec:200) requires `worker_done --outcome failed` and live step 2 (spec:181) requires `agentWait` to stay null. A worker that follows WC-3 asks instead; the check then fails. This needs the guess that a compliant worker picks the `ask` route, so it is Medium. Fix: say which route AC-2.2 expects, or make the `ask` route a coordinator opt-in in the brief.
- M2. AC-C1 (spec:172) scans `src/superclaude/core`, which P0 extends with the contract and an Orca section for the routing guide (spec:158, spec:150). SA-2 (spec:147) restricts the no-Orca rule to command, skill and agent files and allows a mention "inside the contract file". If either core text names `orca orchestration <verb>`, AC-C1 prints it. Align the scan scope with SA-2, or exclude those two files.
- M3. AC-C5 (spec:176) fails on any `-` line, and SA-4 (spec:149) says edits are additive with "new flags". Adding `--unattended` or an output flag to a one-line Usage entry rewrites that line. The spec never says to put new flags on a new line. Needs a guess about how the implementer edits; Medium.
- M4. Requirements with no acceptance check: WC-3 (ask route and resume by message ID, spec:61), WC-6 (retry safety, spec:64), WC-10 for cli-eval (spec:104; only pr-submit is checked, spec:210), WC-11 for any command except save (spec:69; only AC-3.4), WC-12 (`consumer_fenced`, spec:70). A phase can pass with these unimplemented.
- M5. Live step 5 (spec:184) searches the transcript for `AskUserQuestion`; the command text and the contract both contain that string, so a text match without "call" semantics gives false failures. State that only tool-call entries count.
- M6. Section 6 says "Phases 1-3 need no user decision" (spec:154), yet P1 asks every command in 3.1-3.2 to accept `--unattended` (spec:159), including pr-submit, which D3 (spec:238-242) and section 4 (spec:139) leave undecided. Decide whether pr-submit is exempt from P1.
- M7. "Brief must pass" (spec:81-92) omits the output directory for troubleshoot, workflow, reflect, cleanup-audit and index-repo, although spec:73 says the brief states it. Not blocking on its own because B2 covers the failing criterion.
- M8. Coordinator-only commands "get no `--unattended` mode" (spec:128), but the behavior when a coordinator passes the flag anyway is undefined.
- M9. Citation status: all `src/`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml` and Orca-guide line citations in the candidate (for example spec:11, 22, 52, 62-70, 172-176) cannot be checked in this workspace and are UNVERIFIED. The inventory lines read here match the spec's use of them (`INV-A:35-55`, `INV-B:31-52`, `CAPS:44-47,58-80,84-93,107-116,129-131,140`).

Minor
- n1. The AC-C1 command in spec:172 is written with `\|` inside a table cell; copied raw it breaks `grep -E`. Note the escaping.
- n2. spec:11 says the author re-read 11 locations, and UNVERIFIED item 14 (spec:285) says 9 citation defects were fixed; neither can be rechecked here. Both are provenance notes, not requirements.
- n3. spec:3 names a task id (`task_1376c0449d24`) that the README does not define; harmless.
- n4. Decisions table (spec:255-269) is placed after Open decisions; the README asks for a `## Decisions` section (`README.md:34`), which exists.

## Coverage
Covered: all of sections 1-9, every acceptance criterion (AC-C1..C5, AC-0.1..0.4, AC-1.1..1.4, AC-2.1..2.5, AC-3.1..3.4, AC-4.1..4.3) and all seven live-check steps, against WC-1..WC-12 and the 37 worker-capable commands of section 3 (10 + 27) and the 6 of section 4. Not covered: any `src/`, `CLAUDE.md`, `EVIDENCE.md`, Orca-guide or `pyproject.toml` text (not in the workspace). The follow-up list is for the user to decide on (open an issue or not); the session that ran this review asks once per loop, and this report only records it. No issue was created.

## Reviser brief
Blocking finding ids: B1, B2, B3, B4, B5, B6.
Rules for the reviser (restating the Reviser contract of `/sc:spec-panel`): revise only the text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings (M1-M9, n1-n4) alone. Do not award yourself a PASS.
Findings, each with its quoted texts and stated wrong outcome:
- B1: spec:62 (`<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)") versus spec:90 and spec:87 (`--output <file>`) and spec:200 (`/sc:tdd "auth" --unattended --output <file>` must yield a contract). Wrong outcome: the contract path does not exist when `--output` is a file, so AC-2.2 and live steps 3-4 cannot be run.
- B2: spec:194 ("step 4 uses the command's existing report file, since the contract arrives in P1" while "steps 1-3 ... pass") versus spec:182 ("its report path is the WC-4 contract path"); also spec:91-92 versus spec:73 and spec:62 ("known before dispatch"). Wrong outcome: step 3 cannot pass in Phase 0.
- B3: spec:195 ("every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`") and spec:196 versus spec:112 (load: report "none", "usage line only"). Wrong outcome: AC-1.1 and AC-1.2 cannot pass for load.
- B4: spec:200 ("contract `status: blocked` ... per P2 command") versus spec:100, 103, 110, 116, 122, 88 (gates resolve by default, flag or reuse, not blocked). Wrong outcome: AC-2.2 cannot pass for those commands.
- B5: spec:201 ("Happy-path run per P2 command ... `--outcome succeeded`") versus spec:105 (each of three approval gates resolves as blocked, no approval input). Wrong outcome: AC-2.3 cannot pass for cli-portify.
- B6: spec:209 ("no authorization flags" and "the contract lists each skipped outward step") versus spec:113 (blocked without an explicit pre-tag choice) and spec:62 (no skipped-step field). Wrong outcome: AC-4.2 cannot pass.

verdict: FAIL
