# Spec Panel Review, Round 3: Orca Worker Contract Spec

review: 3 of 3
mode: critique (re-review) | focus: requirements, architecture
spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
prior findings: .dev/orca-command-refactor/review/spec-panel-round2.md (review: 2 of 3, verdict: FAIL)
baseline: .dev/orca-command-refactor/specs/history/spec-v2-after-round1.md
reviewer: Orca worker task_ab1c8134a19c (did not write or revise the spec)

## 1. Inputs and method

- This is the same interrupted review, resumed from its existing stub. The requested `sc:spec-panel-armb` Skill invocation loaded before the interruption, with critique mode, requirements and architecture focus, round-2 findings and the saved round-1 revision as baseline. No new review cycle was started. The round-2 report's header and final line establish review 2 and FAIL (`R2:3,209`), so this report is review 3.
- Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `R2:N` = `.dev/orca-command-refactor/review/spec-panel-round2.md:N`; `DISP:N` = `.dev/orca-command-refactor/review/disposition-round2.md:N`; `A:N`, `B:N`, `CAPS:N` = the three files `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md` below `.dev/orca-command-refactor/`. `cmd/` = `src/superclaude/commands/`, `sk/` = `src/superclaude/skills/`. These are abbreviations for actual file:line citations, not claims that inventory quotations replace source verification.
- Governing structure: the loaded command's Review Loop and critique-mode output, the seven-column boundary-table template, and the assigned brief's resolution and citation tables. This output was stubbed before source verification and populated in sections. The spec was not edited. The local `.claude/agents/rf-qa.md` is absent (Glob check); Fix Cycle steps were read in `~/.claude/agents/rf-qa.md:384-400`: check correctness, not just presence, and escalate after review 3. Minor-note rechecks requested by the brief are recorded separately from blocking findings (`R2:174-181`).
- Current revision differs from the saved round-2 revision at SPEC:68 and SPEC:158: the fix-audit removed the redundant release citation and reverted the expanded brief-template wording. The disposition therefore does not describe the final file at those two lines (`DISP:26,29`; `review/fix-audit/apply-log.md:1,23`). Review conclusions below use the live spec, not the disposition.
- Non-whitespace changes against the supplied baseline: SPEC:62-64,68,76,83,105,109,114,183-184,195-196,210,235,262,288-290 (observed `diff -w`). New defects are restricted to these lines or quote a changed line that depends on unchanged text. The baseline and current file have 65,568 and 70,488 bytes respectively (observed `wc -c`).
- Panel reasoning uses the command's fixed sequence: Wiegers (requirements), Adzic (examples), Cockburn (actors), Fowler (interfaces), Nygard (failure handling), Whittaker (adversarial probing), Newman (compatibility), Hohpe (message flow), Crispin (boundary-table completeness), Gregory (acceptance clarity), Hightower (operational concerns). These are simulated perspectives in this reviewing context, not claims of separate human or agent reviews.
- Evidence read on 2026-11-09: spec, baseline diff, previous findings, disposition, inventories, cited source ranges and live Orca help/guide output. Read-only verification only: no new worker launched and no implementation tests run. Runtime questions explicitly deferred to the future live checks remain UNVERIFIED (`SPEC:271-290`).


## 2. Resolution table (round-2 blocking findings)

Status measures the original attack against the current spec, not the reviser's assertion. All seven original blocking attacks are resolved. One requested prior minor-note correction is absent from the final spec, as recorded separately below.

| Prior finding | Severity | Status | Verified resolution in the spec and live evidence |
|---|---|---|---|
| Nested adversarial status (NF1; round-1 F1) | CRITICAL | resolved | SPEC:62-63 preserve the nested `return_contract:` shape and name the nested read; SPEC:183 uses `c = d.get('return_contract', d)` before checking fields. Both `sk/sc-adversarial-protocol/SKILL.md:432-436` and the historical `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:1-5` have that shape. The earlier top-level KeyError attack no longer applies. |
| Missing dry-run spelling (NF2) | MAJOR | resolved | SPEC:62-63,183,262 include both `dry-run` and `dry_run`. Live definitions match: `sk/sc-brainstorm-protocol/SKILL.md:341`, `sk/sc-reflect-protocol/SKILL.md:665`, `sk/sc-cli-portify-protocol/SKILL.md:513`; troubleshoot's `blocked` is acknowledged at `sk/sc-troubleshoot-protocol/SKILL.md:65`. |
| Universal contract location without delivery route (NF3) | MAJOR | resolved (location attack) | SPEC:62,76 supply report-folder, report-file and new `--run-dir` routes, with workflow the sole package-location exception. SPEC:83,105,109,114 and SPEC:196,210 now agree on the contract location. Fixed artifacts need not move with the contract. This resolves the wrong-path attack in R2:169; the added fixed-state retry sentence creates R3-N1 below. |
| Implement overwrites workflow contract (NF4) | MAJOR | resolved | SPEC:62,109 explicitly forbid that overwrite and put implement's contract in its separate run folder. Workflow keeps its package contract (`sk/sc-workflow-protocol/refs/return-contract.md:3`); implement's ledger is the package sibling (`cmd/implement.md:58,65`), and the sibling workflow contract must remain version 1.1 with success/partial (`sk/sc-implement-protocol/refs/managed-workspace.md:10`; `sk/sc-implement-protocol/scripts/archive_workspace.py:322-330`). A blocked implement report no longer replaces the executable plan's contract. |
| No-answer-input gates also told to ask (NF5) | MAJOR | resolved | SPEC:114 makes PR-submit operator halts final, with no ask. SPEC:235 ends the halted worker, then makes any relayed Ruling a new Task with an explicit resume, conditional on the person's decision. This matches SPEC:61's no-answer-input branch. The current Ruling restriction is still accurately stated (`sk/sc-implement-protocol/refs/qa.md:231-240`); the proposed relaxation is not claimed to exist. |
| P1 test gives every command a folder-valued output flag (NF6) | MAJOR | resolved | SPEC:196 now distinguishes folder outputs, init-lite's file output, fixed-location `--run-dir`, and workflow with neither flag; load is excluded. Workflow's rejection remains real (`sk/sc-workflow-protocol/refs/input-parse.md:12`); init-lite is a file path (`cmd/init-lite.md:32`). Those named failing cases are corrected. P1's general requirement supplies output flags for commands lacking them (`SPEC:159`). |
| No deterministic adversarial Phase-0 report (NF7; round-1 F3) | MAJOR | resolved | SPEC:83 now names `<output>/adversarial/merge-log.md`, independently of the still-unfixed contract filename. That file is Step 5's documented output (`sk/sc-adversarial-protocol/SKILL.md:324-327,371-384`) and exists in the observed quick run (`.dev/codegraph-migration/decisions/P3-command-set/adversarial/adversarial/merge-log.md:1-10`). SPEC:182-183,194 can compare a known path. Whether every successful quick run writes it remains explicitly UNVERIFIED pending the Phase-0 smoke test (`SPEC:289`), not fabricated runtime proof. |

### Requested checks of prior minor notes and overstated citations

These retain their original MINOR classification; none is promoted to a blocker merely because it was rechecked.

| Prior note / citation | Current status | Live spec check |
|---|---|---|
| Incorrect workflow source line (M1; C4) | resolved | SPEC:62 now cites `sk/sc-workflow-protocol/refs/return-contract.md:37-39`, which actually states the no-package/no-yaml STOP rule. |
| Receipt cross-reference (M2; C25) | resolved | SPEC:62 now points to step 1, which runs worker-start at SPEC:180. |
| Brief-template completeness (M3) | open as an optional prior note; not applied in final file | SPEC:158 again lists only the section-3.1 flags, while SPEC:73 supplies the full brief contents. The fix-audit intentionally reverted the extra reference (`review/fix-audit/apply-log.md:1`), so DISP:26's claim that the fix is applied is stale. This remains the same inferrable, non-blocking note described at R2:176, not a new blocking finding. |
| Protocol skill invocation check (M4) | resolved | SPEC:184 now also requires the named protocol Skill call. `cmd/adversarial.md:145-149` actually names it and forbids proceeding from the command alone. |
| Partial evidence of Skill-name availability (M5) | resolved as a documentation note, runtime generality UNVERIFIED | SPEC:288 cites R2:8's observed Skill invocation and states that session availability is not proof for all installations; AC-0.4 remains the resolver. This session also loaded `sc:spec-panel-armb` successfully. |
| Release-only source used for four actions (M6; C11) | resolved | SPEC:68 cites CAPS:125 for stop/abandon/retry/release. The redundant CAPS:111 citation is absent in the final file, contrary to DISP:29,37, because the fix-audit removed it (`review/fix-audit/apply-log.md:23`). The remaining source supports the whole claim and matches the current recovery guide's “Stall needs positive evidence” section. |
| Last approval gate has no next phase (M7) | resolved | SPEC:105 names delivery after gate 3 and requires a new resume point per approval gate. Existing gates are at `sk/sc-cli-portify-protocol/SKILL.md:105,152,393`; existing failure resumes are only 3c and 4a (`:526-536,551-566`). Proposed additions are clearly additions. |
| Load included in section assertion (M8) | resolved | SPEC:195 explicitly excludes load, matching its usage-only treatment at SPEC:112,159. |
| Incomplete existing status set (C8) | resolved for the cited correction | SPEC:62-63 now name reflect's hyphenated value, cli-portify's underscored value and troubleshoot's pre-existing blocked value, all supported by the exact source lines listed under NF2 above. |


## 3. Citation-check table

Coverage includes every source citation on the 19 changed current-spec lines, not just newly added citation tokens. Repeated occurrences are grouped. `holds` means the live cited span supports its stated role; it is not a claim that the proposed feature already exists. Source ranges were opened directly; inventory pointers were also checked where the spec uses them. Orca help and recovery guide text was re-run live rather than inferred from the inventory's dated quotations.

| # | Where used | Citation re-read | Live result / assessment |
|---|---|---|---|
| C01 | SPEC:62,114 | `cmd/pr-submit.md:55` | Holds: output-dir is the run-log and artifacts directory. |
| C02 | SPEC:62 | `cmd/tdd.md:49`; `cmd/init-lite.md:32` | Hold: final TDD document path and context-audit report path, respectively. File-valued route is supported. |
| C03 | SPEC:62,105 | `cmd/cli-portify.md:23,34` | Holds: existing output is the generated CLI module folder; the usage has no resume flag. A new report-only run-dir and resume input are proposals. |
| C04 | SPEC:62 | `sk/sc-workflow-protocol/refs/input-parse.md:12,20` | Holds: output is retired; package ID is TASK-WF-subject-date-time. |
| C05 | SPEC:62 | `sk/sc-workflow-protocol/refs/return-contract.md:37-39` | Holds: pre-package STOP has no directory and no YAML. Incorrect old line 53 is gone. |
| C06 | SPEC:62 | `sk/sc-adversarial-protocol/SKILL.md:432-436` | Holds: nested return_contract map and success/partial/failed values. |
| C07 | SPEC:62 | `sk/sc-workflow-protocol/refs/return-contract.md:7` | Holds: success/partial/failed. |
| C08 | SPEC:62 | `sk/sc-brainstorm-protocol/SKILL.md:341`; `sk/sc-reflect-protocol/SKILL.md:665` | Hold: both include dry-run. |
| C09 | SPEC:62 | `sk/sc-cli-portify-protocol/SKILL.md:513`; `sk/sc-troubleshoot-protocol/SKILL.md:65` | Hold: dry_run in portify; blocked already in troubleshoot. |
| C10 | SPEC:62-63,262 | `CAPS:72-74,76-77,79`; live `orca orchestration send --help`, Notes | Hold for report-path metadata, two outcomes, active-Dispatch sender and settlement; current guide's Worker obligations and Completion accounting agree. Whether Orca itself validates the file remains UNVERIFIED as CAPS:79 explicitly says; the old categorical clause “Orca does not check the file” is not newly introduced by this revision. The spec still separately lists this assumption at SPEC:274. |
| C11 | SPEC:62 | `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41`; `B:272` | Hold: package contract fields and failed post-creation contract are real. |
| C12 | SPEC:62 | `sk/sc-brainstorm-protocol/SKILL.md:335`; `A:97` | Hold: named YAML file and inline response. |
| C13 | SPEC:64 | `CAPS:116`; live `orca orchestration worker-start --help`, Notes; current recovery guide, Retry, stop, and abandon | Hold: retry names failed Task, does not inherit placement, and preserves the circuit-breaker boundary. The exact quoted failed-Task sentence is still present in live help. |
| C14 | SPEC:64 | `A:35-55`; `B:31-52` (resume columns) | Hold as inventory pointers: fixed checkpoint, implicit ledger resume, pipeline-only adversarial resume, fresh workflow package and other named mechanisms appear there. Direct implementation/cleanup sources were also checked (`cmd/implement.md:57-58`; `sk/sc-cleanup-audit-protocol/SKILL.md:76`; adversarial source in C22). |
| C15 | SPEC:68 | `CAPS:125`; current recovery guide, Stall needs positive evidence | Holds: absence never authorizes stop, abandon, retry or release. The release-only citation has been removed, not misused. |
| C16 | SPEC:68 | `CAPS:130`; current guide, Worker obligations | Holds: guide says heartbeat is liveness, with cadence delegated to the preamble. This actual dispatch preamble specifies five minutes. |
| C17 | SPEC:68,114 | `cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:46-64` | Hold: per-wait wall-clock budget, one foreground poll, bounded wait, repeat. Neither span proves poll runtime; SPEC:283 correctly keeps that UNVERIFIED. |
| C18 | SPEC:68 | `sk/sc-cli-eval-protocol/SKILL.md:151-152`; `A:65` | Hold: timeouts up to 3600 seconds and instructions not to block. Current source launches background Bash plus Monitor at :148-153; no live eval was run. |
| C19 | SPEC:76 | `A:3`; `B:3` | Hold as inventory scope: 21 and 22 listed commands. The inventory result partitions are at A:73 and B's per-command table; the changed paragraph retains their 10/27/6 classification, not a fresh all-command audit. |
| C20 | SPEC:83 | `A:35,60-61`; both historical contract files | Hold: A records two locations. Read `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:1-10` and `.dev/codegraph-migration/decisions/P1-primitive-gap-policy/adversarial/adversarial/return-contract.yaml:1-11` directly; both exist with nested contracts. |
| C21 | SPEC:83 | `sk/sc-adversarial-protocol/SKILL.md:327,371-384,427-429` | Hold: Step 5 merge log is fixed in the artifact tree; return-contract emission is mandatory but these lines give no contract filename. |
| C22 | SPEC:83 | `sk/sc-adversarial-protocol/SKILL.md:605,1908,2806-2833` | Hold: output auto-derives from input directory; noninteractive is default; pipeline-resume is for pipeline mode and validates checksums. |
| C23 | SPEC:105 | `sk/sc-cli-portify-protocol/SKILL.md:105,152,393` | Hold: review before Phase 2, approval before Phase 3, approval before final delivery. The first gate's precise wording is review, not a claim that the source already provides the proposed approval-resume semantics. |
| C24 | SPEC:105 | `sk/sc-cli-portify-protocol/SKILL.md:526-536,551-566` | Hold: 3c/4a existing resumable failure points and their behavior; approval resume points do not already exist. |
| C25 | SPEC:105 | `sk/sc-cli-portify-protocol/SKILL.md:69,170,464-473,517-566,529`; `A:45,68` | Hold: gates, hardcoded in-checkout template, existing identity/quality/resume contract fields and template_failed are real. New resume flag is labelled “add”, not presented as installed behavior. |
| C26 | SPEC:109 | `sk/sc-implement-protocol/refs/qa.md:231-238`; `sk/sc-implement-protocol/SKILL.md:35` | Hold: halt/Ruling/no-Ruling behavior. No invented coordinator acceptance is asserted as current policy. |
| C27 | SPEC:109 | `cmd/implement.md:57-58,65,74` | Hold: matching-ledger resume, managed sibling ledger, command prints ledger path. |
| C28 | SPEC:109 | `sk/sc-implement-protocol/refs/managed-workspace.md:10`; `sk/sc-implement-protocol/scripts/archive_workspace.py:322-326` | Hold: both require workflow contract 1.1, matching slug, success/partial. Script read through codegraph's current-source file view. |
| C29 | SPEC:109 | `A:51,66` | Hold: inventory records halt-path gate and why another agent cannot give a Ruling today. |
| C30 | SPEC:114 | `sk/sc-pr-submit-protocol/SKILL.md:37-39,66-68` | Hold: top-level activation, main session owns outward effects. |
| C31 | SPEC:114 | `sk/sc-pr-submit-protocol/SKILL.md:141,170,189-197,237-246`; `cmd/pr-submit.md:25,39,55-56`; `B:34,87-95` | Hold for explicit monitor ceiling, JSONL resume/log, PR creation, remediation, commit/push/reply, operator HALTs and crash recovery. The summary file and blocked worker contract remain proposed additions. |
| C32 | SPEC:183 | `pyproject.toml:38` | Holds: PyYAML is declared. The nested-field check and both dry-run spellings are present in the actual revised snippet at SPEC:183. |
| C33 | SPEC:184 | `cmd/adversarial.md:146` | Holds: mandatory protocol Skill activation; :148 says command-file-only execution is insufficient. |
| C34 | SPEC:262 | `CAPS:73`; current send help and guide | Holds: only succeeded or failed is accepted as completion outcome. |
| C35 | SPEC:288 | `review/spec-panel.md:162`; `review/spec-panel-round2.md:8` | Hold: round 1 explicitly labels slash-expansion behavior UNVERIFIED and assumes the Skill route; round 2 records the actual Skill call. Prior sessions' skill menus themselves were not independently recoverable: only the reports and this session's actual successful load are evidence, not proof across installations. |
| C36 | SPEC:289 | `.dev/codegraph-migration/decisions/P3-command-set/adversarial/adversarial/merge-log.md` | File exists and was opened, with applied changes and success at :1-10. The spec cites existence, not a line number; :1-10 are supplied here for the reviewed fact. |
| C37 | SPEC:290 | Exact run-dir search over `src/superclaude/commands` and `src/superclaude/skills` | Both dedicated Grep calls found no matches. Proposed flag has no collision in these searched trees today; other installations and future phase-time collisions remain UNVERIFIED as the spec says. |

No newly added or changed path:line citation failed its source-location check. Two disposition descriptions differ from the final post-audit spec, explicitly recorded in section 2 rather than silently “verified” from the disposition. No transitive claim that a prior worker checked all installations, or that an inventory quotation proves a live runtime outcome, is made here.


## 4. New findings (changed lines)

**Numbered new findings: none verified.** There are no new CRITICAL, MAJOR or MINOR findings on the changed spec lines. No prior blocking finding is open or regressed. This is not a claim that the unimplemented system runs, or that unchanged areas of the entire spec were re-audited.

### Remaining prior finding, not a new finding

1. **Brief-template completeness (M3), MINOR, non-blocking, origin=unchanged.** Section 6 still describes the Phase-0 brief template as listing only section-3.1 flags (`SPEC:158`), whereas section 2.3 specifies the base folder/file name, outward authorisation and placement as well (`SPEC:73`). This is the same inferrable note recorded at `R2:176`, not a newly discovered wrong execution path. Its optional fix is absent from the actual final file despite `DISP:26` saying it was applied: `review/fix-audit/apply-log.md:1` proves it was intentionally reverted. **Priority: Low.** The correct response is to record that final state accurately, not to promote the note to a blocker or silently demand another spec revision.

### Requirements and architecture synthesis

- **Wiegers, Adzic, Cockburn:** the original failing path examples now have a defined expected report, correct path argument types, and named answer/resume behavior (`SPEC:62-64,83,105,114,183-184,195-196,235`). No new wrong outcome survived checking those changes against the cited sources.
- **Fowler, Nygard, Newman, Hohpe:** existing YAML shape and status spellings are preserved, implement's report no longer shares workflow's contract path, and no-answer gates no longer rely on an ask reply to an ended worker (`SPEC:62-64,109,114,235,262`). The fixed-state retry sentence was tested as a possible contradiction; its explicit per-command-state exception makes that hypothesis insufficient for a defect (boundary table, retry rows).
- **Whittaker, adversarial probes:** Sentinel Collision Attack against nested adversarial status and underscored dry_run no longer breaks the reader (`SPEC:63,183`; `sk/sc-adversarial-protocol/SKILL.md:432-436`; `sk/sc-cli-portify-protocol/SKILL.md:513`). Sequence Attack against blocked implement overwriting workflow's package contract is prevented by the newly separate report route (`SPEC:62,109`; `sk/sc-implement-protocol/refs/managed-workspace.md:10`). Divergence Attack against workflow and init-lite in the universal P1 command line is defeated by the per-command routes (`SPEC:196`; workflow input parser :12 and init-lite command :32). Zero/Empty Attack against the Phase-0 report name now has a defined target and non-empty-file check (`SPEC:83,182-183`). Accumulation Attack against retries produces different contract paths per Dispatch and an explicit fixed-state exception rather than an unmentioned overwrite (`SPEC:64`). These are attacks attempted, not invented findings.
- **Crispin, Gregory, Hightower:** the changed acceptance checks distinguish initial smoke runs, converted command tests and future runtime questions; they do not substitute the disposition for live checks (`SPEC:183-184,195-196,210,288-290`). No implementation or live-worker test result is claimed by this planning-only review.

### Self-Audit

A zero-new-finding result was challenged rather than assumed. Checked: every prior blocking attack; all eight requested minor-note statuses against the post-audit spec; both overstated citation corrections; every cited source span on the changed spec lines; direct historical nested YAML and both reported contract locations; fixed merge-log location; workflow's parser/STOP rules; implement's sibling-ledger detection and archive contract check; portify's three gates and two existing failure resume points; actual Skill activation requirements; two empty run-dir collision searches; and seven guard groups with 48 input rows. Rejected hypotheses were recorded where they mattered: the fixed-state retry exception is explicit, and a proposed new run-dir flag is not falsely presented as an already installed capability (`SPEC:62,64,105,290`). Remaining runtime gaps stay UNVERIFIED and retain their future acceptance checks (`SPEC:271-290`).


## 5. Guard Condition Boundary Table (guards on changed lines)

Nygard's failure-path lens constructs the table; Crispin's lens checks completeness; Whittaker's lens attacks the exceptional branches. Equivalent repeated guards in WC-4/WC-5 and acceptance checks are grouped and all locations are named. Each guard has at least six populated input rows. Any GAP would generate a MAJOR finding under the command's boundary rule (`~/.claude/commands/sc/spec-panel-armb.md:305-328`). Unchanged guard logic, including the heartbeat exemption whose citation alone changed, is not re-opened.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Contract read and outcome | SPEC:62-63,183,262 | Zero/Empty | No file or missing/empty status | failure | WC-5 sends failed; step 4 rejects a missing file or invalid status | OK |
| Contract read and outcome | SPEC:62-63,183,262 | One/Minimal | Flat status=success, nonempty command | success | Succeeded; step 4 passes | OK |
| Contract read and outcome | SPEC:62-63,183,262 | Typical | succeeded or partial, command present | success | Succeeded; body's first sentence retains actual status | OK |
| Contract read and outcome | SPEC:62-63,183,262 | Maximum/Overflow | Arbitrary unrecognised status | failure | WC-5 sends failed; step 4 rejects | OK |
| Contract read and outcome | SPEC:62-63,183,262 | Sentinel Value Match | dry_run or dry-run requested by brief | success | Succeeded and accepted by step 4 | OK |
| Contract read and outcome | SPEC:62-63,183,262 | Legitimate Edge Case | return_contract.status=partial, nested command | nested read | Read nested fields; succeeded; no top-level KeyError | OK |
| Contract read and outcome | SPEC:62-63,183 | Negative outcome | failed or blocked, command present | failure | Failed; step 4 still accepts the known status as a valid report | OK |
| Contract read and outcome | SPEC:62-63 | Audit edge case | success with verdict=FAIL | completed audit | Outcome succeeded; report verdict preserved | OK |
| Contract route | SPEC:62,76,83,105,109,114,196,210 | Zero/Empty | No report-output flag, fixed artifact location | route 3 | Add run-dir with unattended; only the contract moves | OK |
| Contract route | SPEC:62,196 | One/Minimal | One folder-valued report output | route 1 | Set output to the Dispatch run folder | OK |
| Contract route | SPEC:62,196 | Typical | init-lite or tdd file output | route 2 | Output is a file in run folder; contract is its sibling | OK |
| Contract route | SPEC:62,105 | Maximum/Overflow | cli-portify output names generated code | route 3, not route 1 | Keep code destination; use run-dir for contract | OK |
| Contract route | SPEC:62,196 | Sentinel Value Match | workflow | package exception | No output or run-dir flag; accept generated package contract path | OK |
| Contract route | SPEC:62,109 | Legitimate Edge Case | implement on a managed workflow package | route 3 | Contract outside package; preserve workflow's contract | OK |
| Contract route | SPEC:62,114,210 | Alternate flag | pr-submit output-dir | route 1 | Summary, log and contract share the passed run folder | OK |
| Contract route | SPEC:62 | Flag combination edge | run-dir without unattended | invalid combination | Flag accepted only with unattended | OK |
| Contract route | SPEC:62-63 | Early STOP edge | workflow stops before package creation | exception | No contract; failed completion without a fake report path | OK |
| Contract route | SPEC:83,289 | Phase-0 edge | adversarial successful quick smoke run | existing artifact | Compare merge-log.md; runtime universality explicitly UNVERIFIED until smoke test | OK |
| Retry versus resume | SPEC:64 | Zero/Empty | First attempt left no state | clean retry | New run folder and fresh execution | OK |
| Retry versus resume | SPEC:64 | One/Minimal | Failed report-folder command, new Dispatch | clean retry | New folder leaves earlier output untouched | OK |
| Retry versus resume | SPEC:64 | Typical | Coordinator deliberately creates new Task with prior state and resume flag | resume | Resume first attempt's state by explicit coordinator choice | OK |
| Retry versus resume | SPEC:64 | Maximum/Overflow | Repeated fixed-state retries, nonempty checkpoint | specific fixed-state branch | Each contract is fresh; the paragraph explicitly says fixed-location state continues under retry | OK |
| Retry versus resume | SPEC:64 | Sentinel Value Match | implement finds matching ledger on retry of same Task | specific fixed-state branch | Continue from matching ledger, as its existing resume rule says; the report contract is isolated, not the ledger | OK |
| Retry versus resume | SPEC:64 | Legitimate Edge Case | workflow retry | generated package | New package; no reuse of previous package | OK |
| Approval resume | SPEC:105 | Zero/Empty | No approval supplied at gate 1 | blocked | Write blocked contract naming review artifact | OK |
| Approval resume | SPEC:105 | One/Minimal | Resume blocked contract after gate 1 | approved | New resume point enters Phase 2 | OK |
| Approval resume | SPEC:105 | Typical | Resume blocked contract after gate 2 | approved | New resume point enters Phase 3 | OK |
| Approval resume | SPEC:105 | Maximum/Overflow | Run reaches all three gates | bounded sequence | Initial run plus at most three approval resumes | OK |
| Approval resume | SPEC:105 | Sentinel Value Match | Third gate, no next numbered phase | approved | Continue with final delivery, not a nonexistent next phase | OK |
| Approval resume | SPEC:105 | Legitimate Edge Case | Existing failure resume 3c or 4a | retained | Existing resume fields retained; new approval points added rather than mistaken for these two | OK |
| Final gate and relayed Ruling | SPEC:114,235; dependency SPEC:61 | Zero/Empty | Gate has no named answer input | final for run | No ask; blocked report stands | OK |
| Final gate and relayed Ruling | SPEC:114,235 | One/Minimal | PR-submit operator HALT | final for run | Blocked, no invented answer channel | OK |
| Final gate and relayed Ruling | SPEC:235 | Typical | Person chooses relayed Ruling policy and supplies exact scoped words | new Task | Coordinator starts new Task with those words and resume | OK |
| Final gate and relayed Ruling | SPEC:235 | Maximum/Overflow | Coordinator has no person's Ruling to relay | not authorised | No relayed Ruling; the person's words are the required input | OK |
| Final gate and relayed Ruling | SPEC:235 | Sentinel Value Match | D2 recommended policy keeps current Ruling rule | no relay | Person resumes in their own session per SPEC:234 | OK |
| Final gate and relayed Ruling | SPEC:235 | Legitimate Edge Case | Halted worker has already ended | new Task, not old ask | New worker records verbatim words; settled worker is not revived by an ask reply | OK |
| Protocol invocation evidence | SPEC:184 | Zero/Empty | No command Skill call | reject | Step 5 fails | OK |
| Protocol invocation evidence | SPEC:184 | One/Minimal | Command has no protocol skill and command Skill call is present | accept | No second Skill call required | OK |
| Protocol invocation evidence | SPEC:184 | Typical | Command names a protocol and both Skill calls are present | accept | Step 5 passes if no local prompt call exists | OK |
| Protocol invocation evidence | SPEC:184 | Maximum/Overflow | Many transcript calls, none names required protocol | reject | Unrelated calls do not satisfy the requirement | OK |
| Protocol invocation evidence | SPEC:184 | Sentinel Value Match | Command Skill loaded but named protocol only read as a file | reject | Actual protocol Skill call required | OK |
| Protocol invocation evidence | SPEC:184 | Legitimate Edge Case | Required calls present plus AskUserQuestion | reject | Local prompt still fails the check | OK |
| Conversion-phase eligibility | SPEC:195-196 | Zero/Empty | Later-phase command not converted | exclude | No unattended section yet; P1 test asserts absence | OK |
| Conversion-phase eligibility | SPEC:195-196 | One/Minimal | One converted P1 command | include | Section and live-check assertions apply | OK |
| Conversion-phase eligibility | SPEC:195-196 | Typical | All converted P1 commands | include | Apply per-command path route and live check | OK |
| Conversion-phase eligibility | SPEC:195-196 | Maximum/Overflow | Section-4 coordinator-only command | exclude | Never has an unattended section | OK |
| Conversion-phase eligibility | SPEC:195-196 | Sentinel Value Match | load | exclude | Usage-only fix; no section or standalone live worker test | OK |
| Conversion-phase eligibility | SPEC:195 | Legitimate Edge Case | pr-submit and worker policy not chosen | exclude | No unattended section; later conversion conditional on D3(b) | OK |

Boundary gate complete: seven guard groups, 48 populated rows, no GAP or blank behavior cell. The fixed-state retry branch was challenged against the general clean-retry wording, but not raised as a defect: the new sentence explicitly defines that exception and cites each command's resume rule (SPEC:64; `cmd/implement.md:57-58`; `sk/sc-cleanup-audit-protocol/SKILL.md:76`). The phase-0 inventory and rollout partition are classifications of commands, not a new multi-stage count-changing data pipeline; the changed lines do not activate the command's quantity-flow diagram rule.


## 6. Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Review continuity | Resume existing stub; restart from round 1 | Resumed the same review-3 assignment and baseline. The explicit user instruction after the interruption forbids restarting or editing the spec. No model-setting action was taken by this worker. |
| Authoritative final text | Disposition's applied claims; live post-audit spec | Live spec wins. The audit log explains why two disposition descriptions are stale, so no unresolved source conflict is silently papered over (`DISP:26,29`; `SPEC:68,158`; `review/fix-audit/apply-log.md:1,23`). |
| Prior minor-note checks | Skip them per ordinary command loop; inspect the eight explicitly requested statuses | The task explicitly asks for all eight. They remain minor and are not promoted to blocking. M3 is recorded as open/optional, rather than falsely reported resolved. |
| Binary verdict | Ordinary command rule permits PASS with minor notes; assigned task says any finding of any severity is FAIL | Apply the assignment's explicit stricter final verdict to the still-open prior M3 note. This changes no severity: **zero blocking findings remain**. The ordinary command grading is retained, so the report does not invent a blocker or ask for a minor-only fix cycle. The final FAIL is the task-specific zero-findings threshold, not a claim of an unresolved architectural failure. |
| New-finding scope | Re-audit unchanged text; changed lines and dependencies only | Used the requested baseline. The only remaining minor note is labelled unchanged and prior, not repackaged as a new blocking defect (`R2:176`; command Review Loop at `~/.claude/commands/sc/spec-panel-armb.md:260-262`). |
| Output and publication | Assigned Markdown file only; extra reports/pages | Only the assigned file was written, incrementally. No external page was published, no implementation files were edited, and no git mutation was made. The task names a local file as the deliverable and forbids other output ownership. |


## 7. Escalation (review 3 of 3)

**Result:** all seven round-2 blocking findings resolved; seven of eight minor corrections present or substantively resolved; M3 remains an optional prior MINOR note after an intentional revert. Both previously overstated citation uses are corrected. No new finding survived the changed-line critique. Sections 2-5 contain the evidence and completed boundary table.

**Final verdict under the assigned zero-findings rule: FAIL**, solely because M3 remains recorded/open. **Blocking findings: none.** This must not be handed off as “an architectural blocker remains” or used to demand a fourth review. Under the command's ordinary minor-notes grading the same evidence would permit PASS; the stricter task threshold is disclosed rather than quietly substituted or satisfied by upgrading M3's severity.

**Next owner:** the coordinator should reconcile its disposition record with the final post-audit file and report this minor-only gate outcome to the user. Do not start another fix/review cycle: this is review 3 of 3 (`~/.claude/commands/sc/spec-panel-armb.md:259-262`). No Reviser brief is emitted at the cap. The spec and disposition were left untouched.

**Observed report sanity check:** a read-only `uv run --no-project python -I -c` check passed: all placeholders filled, seven guard groups with 48 complete seven-column rows, one review-3 header and a final binary verdict. The spec's SHA-256 remained `2d74ef94e35ad1f5762ec1e118aec05de6759321cf3bdfff852ab653ebff0509`, matching the final fix-audit hash (`review/fix-audit/apply-log.md:26`); `git diff --name-only` was empty. This validates report structure and unchanged spec bytes, not the spec's future runtime behavior.

**UNVERIFIED / not run:** no new live Orca worker, command execution smoke test or implementation test; cross-installation Skill availability, universal quick-run merge-log production, receipt fields and all other declared future runtime checks remain unproven (`SPEC:271-290`). This is a finished planning review report, not completed implementation or runtime acceptance.

verdict: FAIL
