# Spec panel round 3: independent re-review

## Method and scope
- Independent reviewer: this session did not write or revise the spec. Date: 2026-11-09. Task: `task_ea3ff6bef23f`, dispatch `ctx_2b66a22b09d6`.
- Invocation executed through the Skill tool: `/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`; it loaded `sc-review-ledger`. Its Setup and Verify rules govern this review (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:258-265`). The structure derives from its Report rule, critique format, and boundary-table template (`:121,262,314-331`), extended with the brief's requested tables.
- `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `round2:N` = `.dev/orca-command-refactor/review/spec-panel-round2.md:N`; `plan:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/plan-r3.md:N`. `cmd/`, `sk/`, `CAPS`, `INV-A`, and `INV-B` expand as in `spec:8-9`.
- Read the binding README first (`.dev/orca-command-refactor/README.md:3,29-38`), both inventories, round-2 review and disposition, the live spec, and both halves of all six revision hunks (`plan:16-209`). The new-defect pass is limited to those hunks under the ledger Verify rule. Already-filed deferred findings are accounted for, not duplicated as new rows.
- Read-only ledger `status` returned phase `verify`, 12 rows to answer, intact snapshots, and live/snapshot SHA-256 `030b7a941cd3498bf3c568232ae039ba2e267bd99c86417708f47add4d6a4e0c`, matching the script-produced plan (`plan:1-4,212-223`). The coordinator owns every ledger write (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:258`).
- Orca resolved as `orca`: neither executable-override variable was set and the terminal handle matched this dispatch. `orca --version` returned `1.4.245-aidev02.780594c521aa`; inventory quotations record older `1.4.237` output (`CAPS:8-23`), so current guide/help checks validate behavior, not historical output-line identity.
- Created this report as a header/section stub and populated it incrementally. Only this report is writable; no spec, ledger, source, tests, mirrors, settings, or external records are changed (`.dev/orca-command-refactor/README.md:30-38`; assignment ownership). No implementation or live acceptance runs are claimed.

## 1. Resolution table
Judgments below are from the live spec, not from the disposition's claim of a fix. Deferred rows are not regraded or answered in the machine input: the ledger forbids it (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:264-265`). “Unresolved, deferred” does not mean fixed or factually disproven.

| Finding | Live spec evidence and verification | Resolution |
|---|---|---|
| R18: missing report flag and path type | `spec:63` makes newly added output/report flags directory-valued, supplies `--report-dir <dir>` to otherwise flagless worker commands, and explicitly assigns them to the first report phase; `spec:162` includes later-phase commands. File-valued tdd/init-lite flags remain separate (`cmd/tdd.md:49`; `cmd/init-lite.md:32`). | Resolved as a requirement. The generic live-check invocation remains a separate problem, new finding 2. |
| R19: task diagnostic separation assigned to the wrong phase | `spec:93` now explicitly assigns the task-side directory change to the gate-conversion phase, uses `<report-dir>/tfep-<n>/`, and blocks task before that phase. The source trigger count is `sk/sc-task-protocol/SKILL.md:204`, with context/invocation/consumer at `:206,216,220`. | Resolved. Parent report and diagnostic adapter no longer need the same path. Current source derivation is correctly UNVERIFIED. |
| R20: ready-command count versus mode-row count | `spec:80` still says ten; `spec:85-95` contains eleven rows, one being troubleshoot's diagnostic mode. | Unresolved, deferred MINOR. No new row or grade. |
| R21: answered clarification contradicts blocked gate test | `spec:61` now requires an explicit brief offer of coordinator answers; the gate-trigger tests specifically use briefs without that offer. The blocked result in `spec:203` follows deterministically. | Resolved. Flagless answers can still enter the main input on ordinary answered runs. |
| R22: later-phase commands lack a report path in the first report phase | `spec:162` now gives that phase every missing report flag, explicitly including research, task, recommend, spec-panel, cleanup and improve; `spec:63` defines the path rules. | Resolved for the stated missing-path failure. Its edited rollout rule still exposes save before its safety conversion, new finding 3. |
| R23: exactly 240 seconds allowed and forbidden | `spec:70` explicitly allows exactly 240 seconds and forbids longer calls, matching `spec:107,213`. | Resolved. The old and new sides were compared (`plan:169-175`). |
| R24: no total bound on acceptance waiting | `spec:70` adds a required expected-runtime budget, limits every step-3 wait to remaining budget, fails the live check and escalates on expiry, and preserves the Dispatch. The positive-exit and absence rules match `CAPS:125-126` and current recovery guidance. | Resolved as a requirement. It limits the acceptance wait, not the worker's lifetime; no destructive recovery is inferred from silence. |
| R25: baseline artifacts excluded from file accounting | `spec:188` now admits the directory holding the accepted existing report and its path fields in the baseline phase. This covers troubleshoot's default run directory and workflow's package, but not workflow's nested reflect directory beyond the single named `REPORT.md` (`sk/sc-workflow-protocol/SKILL.md:58`; `refs/return-contract.md:17`). | Partly resolved, still OPEN: workflow's mandatory nested `audit.log` and `return-contract.yaml` remain outside the allowance, new finding 1. |
| R26: wrong deletion-statistic record | `spec:179` still records `1 1` for deletion; a read-only full-file deletion comparison in this session returned `0 185` for `cmd/tdd.md` against `/dev/null`. The one-bullet historical run itself is not available. | Unresolved, deferred MINOR; zero additions is consistent with a pure deletion, not `1 1`. |
| R27: common transcript check misses Skill invocation | `spec:187` still checks only `AskUserQuestion`; the explicit invocation check is in baseline-only `spec:197`, although the requirement is `spec:67`. | Unresolved, deferred MAJOR, outside the edited hunks. Not silently treated as minor or fixed. |
| R28: absent wait observation passes as no wait | `spec:184` still accepts “never non-null”; current `orca orchestration worker-show --help` Notes explicitly say absence never means the worker is not waiting (`CAPS:129`). | Unresolved, deferred MAJOR, outside the edited hunks. |
| R29: old deletion grep remains | `spec:196` still prints the old grep; `spec:179` overrides it with the deletion count. | Unresolved, deferred MINOR. |
| R30: workflow pre-creation contract check remains ambiguous | `spec:201` still says “workflow states the contract is written for pre-creation STOPs”; the package contract is not written then (`sk/sc-workflow-protocol/refs/return-contract.md:39`), while `spec:95` adds a separate worker contract. | Unresolved, deferred MINOR. The global override makes the intended reading inferable. |
| R31: static filename assertion omits the separate worker filename | `spec:198` still tests only `return-contract.yaml`; `spec:63` requires `worker-contract.yaml` for existing-contract commands. | Unresolved, deferred MINOR. |
| R32: adversarial's existing filename overstated | `spec:63` still lists adversarial as already writing a file named `return-contract.yaml`; its live contract section requires a write but supplies no filename (`sk/sc-adversarial-protocol/SKILL.md:425-445`), consistent with `spec:85`. | Unresolved, deferred MINOR. The status-vocabulary citation is valid, the filename assertion is overstated. |
| R33: stale report-path gloss and design decision | `spec:78,264` still describe only `return-contract.yaml`; `spec:63` overrides that with the separate worker filename and file-output rule. | Unresolved, deferred MINOR. |

### Previously verified rows touched again
The script plan also requires these five answers because their text was touched (`plan:8-90`), not because their prior findings may be reopened without evidence.

| Row | Check of the new text | Answer |
|---|---|---|
| R2: preserve existing status readers | The separate `worker-contract.yaml` clause survives at `spec:63`; the original `success` consumers at `sk/sc-implement-protocol/refs/managed-workspace.md:10`, `sk/sc-reflect-protocol/refs/remediation-handoff.md:75`, and `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77` remain compatible. | Resolved; no regression of this status-separation rule. |
| R8: deliver flagless answers and retain the report path | `spec:61` still folds flagless answers into main input and retains the output flag. `cmd/task.md:93`, `cmd/recommend.md:44`, and `sk/tdd/SKILL.md:52-61` support the gate examples. | Resolved. |
| R9: suppress auggie-review's default posting before conversion | `spec:162` retains the early blocked-report rule; default posting is real (`cmd/auggie-review.md:51`). | Resolved for outward posting. New finding 3 covers a different rollout category. |
| R11: 300-second blocking call and unproven subagent heartbeat | `spec:70` forbids 300 seconds, explicitly marks long-subagent heartbeat UNVERIFIED, records it in baseline tests, and adds the expected-runtime budget. | Resolved for the stated wrong outcome; the source does not claim heartbeat continuity is proven. |
| R12: unrelated dirty files and simultaneous staging workers | `spec:188` keeps the before/after status baseline and the staging-worker isolation rule. P0 nested outputs still fail under the separate R25 allowance. | Resolved for unrelated pre-existing files and staging isolation; new finding 1 is attached to R25. |

## 2. Citation-check table
Scope: every `path:line` reference on the six changed lines, including unchanged citations carried by those lines, plus every round-2 citation/evidence overstatement discussed in the disposition. Sources were directly read in this session; no source fact below is accepted merely because the disposition says it passed. Repeated references are grouped; `OK` validates the cited assertion, not every requirement built around it.

| # | Spec location | Citation or new factual premise | Direct read and result |
|---|---|---|---|
| 1 | `spec:61` | `CAPS:58-61` | OK. These lines quote blocking ask, owning-Run default, pending-on-timeout and no local prompt. Current `orca orchestration ask --help` repeats the owning-Run default and pending-question resume rule. |
| 2 | `spec:61` | `CAPS:64` | OK. The inventory quotes the heartbeat exclusion while blocked in ask/check; current `orca skills get orchestration --reference worker-contract`, Heartbeat section, repeats it. |
| 3 | `spec:61` | `cmd/task.md:93` | OK. Exact confidence-below-0.70 override question with `--compliance [tier]`. |
| 4 | `spec:61` | `cmd/recommend.md:44` | OK. Ends with asking one question and stopping when the objective remains ambiguous. |
| 5 | `spec:61` | `sk/tdd/SKILL.md:52-61` | OK. Topic/vague-input clarification is required; item 1 must be clearly answered before proceeding. |
| 6 | `spec:63` | `cmd/tdd.md:49` | OK. `--output` is the final TDD document path, not a directory. |
| 7 | `spec:63` | `cmd/init-lite.md:32` | OK. Default is a Markdown filename; the flag is the report output path. |
| 8 | `spec:63` | `sk/sc-workflow-protocol/refs/return-contract.md:7` | OK. Existing status values are success, partial and failed. |
| 9 | `spec:63` | `sk/sc-brainstorm-protocol/SKILL.md:341` | OK. Existing values include success, partial, failed and dry-run; the filename itself is established at `:335`. |
| 10 | `spec:63` | `sk/sc-adversarial-protocol/SKILL.md:436` | OK for `status: success` and its alternatives. NOT evidence of the filename: the surrounding required contract `:425-445` names no file. The pre-existing overstatement remains R32. |
| 11 | `spec:63` | `sk/sc-reflect-protocol/SKILL.md:665` | OK. Existing success/partial/failed/dry-run vocabulary; `:659` fixes its contract filename. |
| 12 | `spec:63,93` | `sk/sc-troubleshoot-protocol/SKILL.md:560` | OK. Conditional `caller=task-unified`, exact `return-contract.yaml` path, seven consumed fields and success/partial/blocked/failed values. |
| 13 | `spec:63` | `sk/sc-implement-protocol/refs/managed-workspace.md:10` | OK. Sibling workflow contract must be version 1.1 with success or partial status. |
| 14 | `spec:63` | `sk/sc-reflect-protocol/refs/remediation-handoff.md:75` | OK. Reads package return contract and branches on `status: success`. |
| 15 | `spec:63` | `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77` | OK. Reads the package contract, success status and package-relative plan path; passing workflow `--output` is forbidden. |
| 16 | `spec:63,93` | `sk/sc-task-protocol/SKILL.md:206,216,220` | OK. Writes context, invokes troubleshoot with `--output-dir`, reads the seven-field adapter at that directory. Full-file search for `output_dir` finds only those three uses, no definition: the new UNVERIFIED statement is accurate. |
| 17 | `spec:63` | No existing `--output`/`--report` flag on research, task, recommend, save, implement, validate-roadmap | OK. Direct reads of `cmd/research.md`, `cmd/recommend.md`, `cmd/save.md`, `cmd/implement.md`, `cmd/validate-roadmap.md` plus whole-file flag search of `cmd/task.md`. Relevant interface locations: research `:25`, recommend `:30-38`, save `:22`, implement `:51-61`, validate-roadmap `:27-34`, task classification `:93-102`. Validate-roadmap's positional OUTPUT_DIR is real (`:18-25`) but is not such a flag; the spec adds a separate report-directory flag. |
| 18 | `spec:63` | Generated research report; implement progress ledger | OK. `cmd/research.md:103,134` gives generated report names; `cmd/implement.md:58,74` gives the ledger and printed path. New report-directory behavior is a proposal, not a claim these flags exist today. |
| 19 | `spec:63` | Workflow `--output` retired | OK. `sk/sc-workflow-protocol/SKILL.md:24` says E-LEGACY; `refs/return-contract.md:39` includes it among pre-creation STOPs. |
| 20 | `spec:70` | `/home/coder/.claude/commands/sc/spec-panel-ledger.md:261` | OK. Exact installed Sweep rule requires a recorded worker/subagent heartbeat smoke check longer than five minutes before using that route. It is evidence of an unproven prerequisite, not evidence the smoke check passed. |
| 21 | `spec:70` | `CAPS:122-123` | OK. Read both lines and current compact orchestration guide, Authority and safety floor: fleet verdict versus PTY liveness; a live terminal can hold a stuck agent. Detection of a stuck running subagent is still correctly UNVERIFIED. |
| 22 | `spec:70` | `CAPS:125-126` | OK. Current `orca skills get orchestration --reference recovery-and-cleanup`, Stall needs positive evidence section, repeats positive stopped-agent evidence and forbids stop/abandon/retry/release from absence alone. The new acceptance-budget expiry is not presented as Orca's own process timeout. |
| 23 | `spec:70` | `CAPS:130` | OK. Heartbeats prove liveness, not progress; five-minute cadence is attributed to the dispatch preamble, not the guide. This assignment's preamble provides that cadence too. |
| 24 | `spec:70` | `cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:46-64` | OK. 600-second per-wait wall-clock budget and repeated foreground poll/classify/bounded-wait iterations; not one mandated 600-second tool call. |
| 25 | `spec:70` | `sk/sc-cli-eval-protocol/SKILL.md:151-152` through `INV-A:65` | OK. Up to 3600-second per-eval timeout. Important limit: source `:148-153` ALREADY launches a background job and Monitor and says not to block; the 3600-second process timeout is not proof of a 3600-second foreground call. |
| 26 | `spec:93` | Trigger count called `escalation_count` | OK. Direct source `sk/sc-task-protocol/SKILL.md:204` defines TFEP trigger 1, 2 or 3; `:229-230` increments it. The proposed nested directory uses that existing concept, not a fabricated variable. |
| 27 | `spec:162` | `cmd/auggie-review.md:51` | OK. PR posting defaults on, with no confirmation prompt. |
| 28 | `spec:188` | `cmd/troubleshoot.md:56` | OK. Generated default output directory contains REPORT.md, cards, proposals, adversarial artifacts and audit log. |
| 29 | `spec:188` | `sk/sc-workflow-protocol/refs/return-contract.md:3-19` | OK for package location, package-relative plan/source paths and absolute reflect report path. It does NOT list all files in reflect's own directory; that missing coverage is new finding 1. |
| 30 | `spec:188` | `sk/sc-workflow-protocol/SKILL.md:28` | OK as an instruction to stage all `.dev/tasks`, packages and artifacts. Whether a historical session actually ran git add is not established; the isolation rule is conservative for commands following this instruction. |
| 31 | `spec:188` | `CAPS:115` | OK. Current `orca skills get orchestration --reference placement-and-remote`, Placement choices section, permits worktree isolation for concrete filesystem/checkout conflicts and otherwise prefers sharing. |

### Round-2 overstated or wrong evidence
| Round-2 item | Actual state in the spec | Result |
|---|---|---|
| Adversarial filename assertion (`round2:44,124`) | Unchanged at `spec:63`; status citation holds, filename claim does not follow from `sk/sc-adversarial-protocol/SKILL.md:425-445`. | Still overstated, deferred R32. |
| Pure-deletion test record (`round2:60,118`) | Unchanged `1 1` at `spec:179`. Read-only `git diff --numstat --no-index -- src/superclaude/commands/tdd.md /dev/null` printed `0 185`, demonstrating the zero-addition side of a pure deletion without making a scratch file. | Still wrong for a pure deletion, deferred R26. The exact historical one-bullet execution is UNVERIFIED, not silently re-created. |
| Process liveness treated as stalled-subagent detection (`round2:77,116`) | `spec:70` now explicitly disclaims that inference and uses expected-runtime expiry only to fail the acceptance check/escalate while preserving the worker. | Overreach removed. Current guide still forbids destructive recovery from absence. |
| Assumed task `--output` and equal diagnostic directory (`round2:81`) | `spec:63` now proposes `--report-dir`; `spec:93` names a distinct nested diagnostic directory and marks existing derivation UNVERIFIED. | Overreach removed from the proposed interface; no observed current collision is claimed. |
| Assumed baseline report needed future worker-contract fields (`round2:82,194`) | `spec:188` accepts existing path fields and the report's directory. | Field-name assumption removed, but transitive reflect artifacts remain excluded: new finding 1. |

Failed/limited verification attempts: the first environment probe returned exit 1 because the two optional executable override variables were absent, while printing the matching terminal handle; this is not an Orca runtime failure. The first Edit was blocked because the hook required an explicit tracked Read of the newly written stub; the file was read and the same edit succeeded. No failed source lookup was replaced by an invented source.

## 3. Expert critique and new findings
The following is the command's simulated expert analysis, not a claim that eleven external people or agents were consulted (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:91,97-111,470`). Findings are numbered once and reused across perspectives.

### Panel sequence
1. **Wiegers, requirements:** directory-versus-file report rules and fallback directory now close the missing-path requirement (`spec:63`); the first report-phase live test still demands a flag that workflow rejects (`spec:95,199`), finding 2.
2. **Adzic, examples:** a bare tdd topic with no coordinator-answer offer now deterministically ends blocked (`spec:61,203`). A successful baseline workflow, however, necessarily invokes reflect before its package contract and therefore creates more files than the revised allowance admits (`sk/sc-workflow-protocol/SKILL.md:58`), finding 1.
3. **Cockburn, actors:** task owns the parent report and diagnostic directory assignment; troubleshoot owns its separate adapter; only the task worker reports lifecycle completion (`spec:93`). The revised assignment removes the phase-owner mismatch.
4. **Fowler, interfaces:** the nested report path is not an exhaustive artifact manifest. Workflow exposes reflect's REPORT.md, not all sibling files (`sk/sc-workflow-protocol/refs/return-contract.md:17`); a path field cannot silently mean the entire transitive output tree, finding 1.
5. **Nygard, failure modes:** expected-runtime expiry now fails acceptance and escalates without treating silence as proof of exit (`spec:70`; `CAPS:125-126`). The early rollout still enables shared-memory writes before their conversion, finding 3.
6. **Whittaker, adversarial:** the sequence and divergence attacks below break baseline acceptance and parallel-write safety even if each local command follows its own instructions, findings 1 and 3.
7. **Newman, evolution:** output flags exist early enough for later-phase blocked reports, but “every other command runs normally” must not enable commands whose non-gate safety change is still pending (`spec:162,164`), finding 3.
8. **Hohpe, message flow:** no duplicate ask is introduced: the worker resumes the original message and report path (`spec:61`; current `orca orchestration ask --help`). Existing deferred observation/Skill-check defects remain in the resolution table, not new duplicate findings.
9. **Crispin, testing:** the inclusive 240-second boundary is consistent (`spec:70,107,213`). The boundary table below identifies the remaining acceptance and phase-availability failures.
10. **Gregory, quality practice:** neither a disposition's fixed claim nor the fact a row is deferred is evidence the complete spec passes; R25 remains open and R27/R28 remain deferred MAJOR (`spec:184,187-188`; `round2:227,229-230`).
11. **Hightower, operations:** preserving a live Dispatch at expected-runtime expiry is a safe escalation, not permission to release it (`spec:70`; `CAPS:125`). No runtime settings or implementation are changed in this review.

### Numbered new findings

#### 1. Baseline workflow still fails artifact accounting on its nested reflection outputs
- **Severity:** MAJOR, blocking. **Section:** 7.2 step 6 and baseline acceptance. **Expert:** Fowler/Adzic/Whittaker. **Priority:** High. **Impact:** a normal successful baseline workflow is rejected, preventing later rollout (`spec:157,188,197`). **Parent:** R25; anchor inside revised hunk c2#6 (`plan:195-209`).
- **Evidence:** workflow must invoke reflect with default other flags before writing its own contract (`sk/sc-workflow-protocol/SKILL.md:58`). Reflect defaults to `.dev/reflect/<mode>-<slug>-<ts>/` (`cmd/reflect.md:101`), writes a per-step `audit.log` (`sk/sc-reflect-protocol/SKILL.md:136`) and writes its own `return-contract.yaml` (`:659`). The workflow package contract exposes only `reflect_report_path` to REPORT.md, not that directory, log or child contract (`sk/sc-workflow-protocol/refs/return-contract.md:3-19`). The revised exception accepts the directory holding the report accepted in step 3, which for workflow is the package's contract, not reflect's report (`spec:188,197`).
- **Concrete attack:** I can break this specification by a **Sequence Attack**. The artifact-accounting invariant at **7.2 step 6** fails when **the baseline workflow's mandatory reflection succeeds**. Before: clean worktree, one workflow task. After: the package appears under `.dev/tasks/to-do/<id>/` and reflect writes a separate run directory; step 3 accepts the package's `return-contract.yaml`. The package and the exact external REPORT.md path are allowed, but the new external `audit.log` and reflect `return-contract.yaml` match none of step 6's allowed paths. They are created by the same worker, not another concurrently dispatched worker with its own worker report. Acceptance fails despite correct command behavior.
- **Recommendation:** make the baseline exception account for the output directory of each nested report it references, or obtain an explicit transitive artifact list. Do not weaken the later-phase worker-report requirement. R25 is not fully resolved; this child isolates the missed nested case rather than repeating the already-fixed package-directory case.
- **Evidence strength:** static, source-backed required writes; an actual baseline run was not authorized, so no runtime outcome is claimed.

#### 2. The first report-phase live check still passes workflow a retired output flag
- **Severity:** MAJOR, blocking by the task's acceptance rule; ledger admission is outside the edited hunks. **Section:** 7.3, first report-phase live check. **Expert:** Wiegers/Crispin. **Priority:** High. **Impact:** the prescribed check rejects a conforming workflow before work starts. **Parent:** none; anchor `spec:199`.
- **Evidence:** the check explicitly runs each command with `--unattended --output <dir>` (`spec:199`); workflow is among that phase's fixes (`spec:162`), and its row explicitly says never `--output`, use `--report-dir` (`spec:95`). The source refuses the retired flag with E-LEGACY (`sk/sc-workflow-protocol/SKILL.md:24`; `refs/return-contract.md:39`). The current revision adds flags selectively, not a universal `--output` alias (`spec:63`). The disposition itself discloses this uncorrected gap (`.dev/orca-command-refactor/review/disposition-round2.md:56`).
- **Concrete example:** follow the check literally for workflow. It correctly rejects `--output`; returning failed accurately describes the rejection, but cannot satisfy the requested successful normal run. Allowing the flag to pass would instead violate the explicit retired-flag rule. No override at the check says to substitute the command's own output flag.
- **Recommendation:** specify the command-specific flag and resolved contract path in this acceptance check, with workflow using `--report-dir`. Keep the retired-flag refusal intact. This is not R18 repeated: the report path is now defined, but the executable acceptance invocation is still wrong.

#### 3. Early unattended save runs can overwrite shared memory before its safety phase
- **Severity:** MAJOR, blocking; boundary rule FR-8. **Section:** 6, first report-phase rollout rule, with 2.2 parallel-write rule and 3.2 save. **Expert:** Nygard/Newman/Whittaker. **Priority:** High. **Impact:** two workers can replace each other's whole-session memory. **Parent:** R22; anchor inside revised hunk c2#5 (`plan:144-158`).
- **Evidence:** the revised first report-phase rule accepts unattended mode for every section-3 command, adds its missing report flag, blocks only later gate/outward-default conversions, and says “Every other command runs normally under the flag” (`spec:162`). Save has neither a person gate nor an outward default; its per-session-only conversion is explicitly assigned to the later shared-state phase (`spec:122,164`). Today single-owner keys are overwritten whole (`cmd/save.md:42-45`). That interim behavior contradicts the no-shared-file-write requirement (`spec:71`).
- **Concrete attack:** I can break this specification by a **Divergence Attack**. The parallel-write invariant at **WC-11** fails when **save is enabled in the report-only phase but its later shared-state conversion has not shipped**. Before: worker A and worker B have separate report directories but share one memory store. Both run save with unattended mode. The gate/outward predicate is false, so the early rule runs normal save; A writes `last_session.md`, then B overwrites the same file. Different worker-contract locations do not isolate the actual memory write. The later shared-state phase would prevent this, but the earlier phase is specified as independently useful (`spec:157`).
- **Recommendation:** keep unattended save blocked until its per-session-only writer is implemented, or explicitly move that safety conversion into the first report phase. Adding the report flag alone is not enough. R22's missing-path failure is resolved, but its edited rollout row still carries this different unsafe case.

No new MINOR findings are introduced. The nine already-deferred round-2 findings remain exactly as recorded in the resolution table; two of those nine are MAJOR, not cosmetic.

## 4. Guard Condition Boundary Table
This Verify pass enumerates the guards present in the six changed hunks, not an unauthorized new whole-document sweep (`plan:16-209`; `/home/coder/.claude/commands/sc/spec-panel-ledger.md:260,310-331`). Every GAP maps to a numbered MAJOR finding above. `OK` means the new text gives the behavior, not that an implementation was run.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Coordinator answers | `spec:61` | Zero/Empty | Brief offers no answers | No ask route | Write blocked report and finish failed | OK |
| Coordinator answers | `spec:61` | One/Minimal | Brief offers answers, one clarification | Ask route available | Ask once; use answer to rerun | OK |
| Coordinator answers | `spec:61` | Typical | Flagless tdd component question | Main-input route | Put answer in component input; retain report flag | OK |
| Coordinator answers | `spec:61` | Maximum/Overflow | Repeated ask timeout | Resume branch | Reuse original message ID, not a new question | OK |
| Coordinator answers | `spec:61` | Sentinel Value Match | Person-only Ruling under keep-rule option | Ask route forbidden | Finish blocked, no agent approval | OK |
| Coordinator answers | `spec:61,203` | Legitimate Edge Case | Gate-trigger acceptance brief | No answer offer | Required blocked outcome remains deterministic | OK |
| Report path selection | `spec:63` | Zero/Empty | Research has no current output flag | Fallback flag | Add report-dir in first report phase | OK |
| Report path selection | `spec:63` | One/Minimal | A newly added report/output flag | Directory branch | dir/return-contract.yaml | OK |
| Report path selection | `spec:63` | Typical | tdd output is final.md | File branch | final.md.return-contract.yaml | OK |
| Report path selection | `spec:63` | Maximum/Overflow | Existing success-vocabulary contract | Separate-schema branch | Preserve existing file; worker-contract.yaml separately | OK |
| Report path selection | `spec:63,95` | Sentinel Value Match | Workflow report-dir | Retired output bypassed | Report-dir/worker-contract.yaml | OK |
| Report path selection | `spec:199` | Legitimate Edge Case | Workflow invoked exactly by generic live check | Retired flag rejected | E-LEGACY instead of required successful check | GAP, finding 2 |
| TFEP directory count | `spec:93` | Zero/Empty | Task before gate-conversion phase | Early block | No TFEP directory or invocation | OK |
| TFEP directory count | `spec:93`; source `sk/sc-task-protocol/SKILL.md:204` | One/Minimal | First diagnostic trigger | n=1 | Nested tfep-1 directory, separate parent contract | OK |
| TFEP directory count | `spec:93` | Typical | Second diagnostic trigger | n=2 | Nested tfep-2 directory, separate from trigger 1 | OK |
| TFEP directory count | `spec:93,124`; source `sk/sc-task-protocol/SKILL.md:214` | Maximum/Overflow | Third trigger | FULL STOP converted to blocked | Parent task reports blocked; no further fixes | OK |
| TFEP directory count | `spec:93` | Sentinel Value Match | Parent and adapter both named return-contract.yaml | Different directories | Parent report and child adapter cannot collide | OK |
| TFEP directory count | `spec:93` | Legitimate Edge Case | Child diagnosis reports failure | Parent owns lifecycle | Task consumes child result; child does not send worker_done | OK |
| Single blocking-call limit | `spec:70` | Zero/Empty | 0 seconds elapsed | Allowed | No limit violation | OK |
| Single blocking-call limit | `spec:70` | One/Minimal | 1-second poll | Allowed | Return control for later heartbeat | OK |
| Single blocking-call limit | `spec:70` | Typical | 200-second wait | Allowed | Within 240-second maximum | OK |
| Single blocking-call limit | `spec:70` | Maximum/Overflow | 3600-second foreground wait | Forbidden | Split into bounded waits | OK |
| Single blocking-call limit | `spec:70` | Sentinel Value Match | Exactly 240 seconds | Allowed | Explicit inclusive maximum | OK |
| Single blocking-call limit | `spec:70,197` | Legitimate Edge Case | Long subagent run, heartbeat continuity unknown | Do not infer hang from gap | Record smoke evidence; runtime budget governs acceptance | OK, capability UNVERIFIED |
| Expected-runtime budget | `spec:70` | Zero/Empty | Required budget missing from brief | Brief incomplete | Does not meet the explicit brief requirement | OK |
| Expected-runtime budget | `spec:70` | One/Minimal | 1 ms remains | Poll shortened | Use remaining time, not 900000 ms | OK |
| Expected-runtime budget | `spec:70` | Typical | 600000 ms remains | Shorter-of branch | Wait at most 600000 ms | OK |
| Expected-runtime budget | `spec:70` | Maximum/Overflow | 1800000 ms remains | Poll cap branch | At most 900000 ms for this wait | OK |
| Expected-runtime budget | `spec:70` | Sentinel Value Match | Budget expires without settlement | Acceptance fails | Read transcript and escalate; preserve Dispatch | OK |
| Expected-runtime budget | `spec:70` | Legitimate Edge Case | Positive proof of exit before budget | Early evidence branch | Leave waiting on the positive evidence, not silence | OK |
| Phase enablement | `spec:162` | Zero/Empty | No pending gate/outward conversion | Normal branch | Runs normally in first report phase | OK for converted safe commands |
| Phase enablement | `spec:162` | One/Minimal | Analyze with new directory output flag | Normal branch | Produce report and worker contract | OK |
| Phase enablement | `spec:162` | Typical | Auggie-review before its conversion | Blocked branch | Write known-path blocked report; no PR post | OK |
| Phase enablement | `spec:162` | Maximum/Overflow | Multiple later conversions pending | Blocked branch | Do no command work beyond early report | OK |
| Phase enablement | `spec:162` | Sentinel Value Match | P2 command whose report flag was originally P2 | First phase now owns flag | Known-path blocked report exists before P2 | OK |
| Phase enablement | `spec:122,162,164` | Legitimate Edge Case | Save before P3; no gate or outward default | Normal branch despite pending shared-state change | Existing whole-key overwrite remains possible | GAP, finding 3 |
| New-path accounting | `spec:188` | Zero/Empty | No status lines added since baseline | No new paths | Pass accounting check | OK |
| New-path accounting | `spec:188` | One/Minimal | P0 troubleshoot audit.log beside accepted REPORT.md | P0 report-directory branch | Allow documented run directory | OK |
| New-path accounting | `spec:188` | Typical | P0 workflow source.md beside accepted package contract | P0 report-directory branch | Allow generated package files | OK |
| New-path accounting | `spec:188` | Maximum/Overflow | Later-phase writes outside output/report artifacts | No permitted branch | Fail check, not a broadened P0 exemption | OK |
| New-path accounting | `spec:188` | Sentinel Value Match | P0 workflow reflect_report_path names external REPORT.md | Exact path allowed | Allow that file; no recursive manifest inference | OK |
| New-path accounting | `spec:188` | Legitimate Edge Case | External reflect audit.log and child return-contract.yaml | Neither named nor in accepted report's directory | Required nested outputs rejected | GAP, finding 1 |
| Baseline and concurrent writes | `spec:188` | Zero/Empty | No other worker or dirty baseline | This-worker accounting | Compare only this run's new paths | OK |
| Baseline and concurrent writes | `spec:188` | One/Minimal | One earlier untracked file | Baseline branch | Ignore earlier status line | OK |
| Baseline and concurrent writes | `spec:188` | Typical | Concurrent worker has explicit worker-report artifacts | Other-worker branch | Allow paths its report names | OK |
| Baseline and concurrent writes | `spec:188` | Maximum/Overflow | Two simultaneous commands stage task packages | Unsafe-sharing branch | Coordinator places one separately | OK |
| Baseline and concurrent writes | `spec:188` | Sentinel Value Match | Tracked file already modified before baseline | Explicit exclusion | This status-only check does not recheck that file | OK, limited check |
| Baseline and concurrent writes | `spec:188` | Legitimate Edge Case | Both nested reflect and workflow belong to same worker | Other-worker branch does not apply | Use new-path accounting; nested artifacts still excluded | GAP, finding 1 |

Quantity-flow check: the revised rules route one task report to one lifecycle outcome; TFEP adds an isolated child adapter but does not add another Orca completion (`spec:93`). No changed hunk introduces filtering or count-changing transformation of a collection, so the command's conditional Quantity Flow Diagram trigger is not met (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:348-350`).

## 5. Verdict
**FAIL.**

- Of R18-R33, six authorized fixes resolve their original wrong outcome; R25 remains open because the baseline workflow's nested outputs still fail file accounting. Nine deferred rows remain unresolved, including the two outside-hunk MAJOR findings R27 and R28. These conclusions come from the live spec and sources in sections 1-2, not the disposition.
- Three numbered new MAJOR findings: nested baseline outputs rejected (inside revised step 6), a retired workflow flag in the normal live check (outside the hunks), and unattended save enabled before its shared-write safety change (inside the revised rollout row). Each has a concrete failure trace and source citations in section 3.
- All path:line citations on the six changed lines were re-read, grouped in 31 citation-check entries. The old adversarial filename overstatement and pure-deletion record remain unresolved, not quietly accepted.
- Read-only `verify --dry-run` returned `ok: true`, 12 accepted answers, three proposed rows R34-R36 (N1-N3), 36 total rows, 22 blocking rows, 19 verified, 3 open in-scope blocking rows, 14 deferred, and `X: 0`. It would write `inputs/r3-verify.json`, but did not: the `dry_run: true` receipt is validation only. Its pre-close `loop_decision: CONTINUE` is not a final verdict; the coordinator's writing `close` step computes and appends that decision. The command's cap requires escalation when this final review closes with open blocking findings (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:263`).
- No PASS Self-Audit is asserted because the verdict is FAIL. The tables state the inspected surface and limitations explicitly. No fourth review or extra fix cycle is authorized here; the coordinator must close and follow the capped-loop escalation and independent sweep rules (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:261-263`).

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Review scope | New whole-document search; changed-hunk verification with accounting of all requested old findings | The loaded command's Verify rule limits the new-defect pass to both sides of current hunks; any independently encountered outside defect is still filed (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:260`). The generic invocation defect was explicitly disclosed in the reviser gaps (`plan:218`). |
| Ledger ownership | Ingest answers directly; validate without writes | Only this report is writable. Run status and verify --dry-run; the coordinator runs verify and close (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:258,265`). |
| Previously deferred rows | Treat as resolved; duplicate them as new; account for them without answering/regrading | Deferral does not resolve a defect, and deferred rows are unanswerable (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:264-265`). The resolution table covers the requested range without changing script-owned state. |
| R25 answer | Resolved because the workflow package now fits; open because its mandatory nested reflection still fails | Open: the same baseline acceptance check still rejects a normal required output path, with the newly isolated nested case documented as N1 (`spec:188,197`; `sk/sc-workflow-protocol/SKILL.md:58`). |
| New-save defect location | File only against unchanged save row; anchor the edited rollout predicate | The writer remains intentionally unchanged until P3; the edited enablement rule is what makes its unsafe normal behavior reachable earlier (`spec:122,162,164`; `cmd/save.md:44`). |
| Runtime proof | Launch smoke workers; inspect source and mark runtime unverified | Planning-only ownership does not authorize live worker runs or extra writes (`.dev/orca-command-refactor/README.md:6,30-31`). The required-write counterexamples are source-backed, not claims of observed runtime failure. |
| Task completion versus spec verdict | Send failed because the reviewed spec fails; send succeeded because the assigned review is complete | The requested review is complete and produces a FAIL report. Worker outcome describes completion of this review task, not approval of the spec (`spec:64`; dispatch completion instructions). |

## UNVERIFIED items
1. Direct command runs, long-subagent heartbeat continuity, and actual process behavior in this planning-only pass: no smoke workers or acceptance tests were launched (`spec:70,197`; `.dev/orca-command-refactor/README.md:6,30`). Findings 1-3 concern specified/source-required behavior, not fabricated runtime observations.
2. Whether a stuck running subagent changes Orca's fleet liveness verdict. The revised spec explicitly does not rely on that answer (`spec:70`; `CAPS:122-126`).
3. Task's current diagnostic `output_dir` derivation. The direct whole-file search found only the three uses (`sk/sc-task-protocol/SKILL.md:206,216,220`); the new spec properly calls it UNVERIFIED (`spec:93`).
4. The exact historical single-bullet deletion test behind `spec:179`: no saved execution evidence was provided. This review's read-only whole-file deletion comparison demonstrates zero additions but does not pretend to reproduce the historical run.
5. Historical 1.4.237 guide output line numbering is not re-created. The inventory records that historical version (`CAPS:8`); current 1.4.245 help and guides were read to confirm the behavior, and no runtime or settings downgrade was made.
6. The coordinator's final close/sweep result has not happened in this worker. Dry-run validation is not ledger ingestion or a final script verdict (`/home/coder/.claude/commands/sc/spec-panel-ledger.md:258,261-263`).

## Ledger input
Exactly one answer per script-plan row. Deferred R20 and R26-R33 are intentionally not answer objects. The new artifact-accounting case is attached to R25; the unsafe early-save case is attached to R22; the generic live-check flag mismatch has no parent and sits outside the current hunks. The coordinator, not this worker, ingests this block and closes the review.

```ledger-input
{
  "answers": [
    {"row":"R2","result":"resolved","evidence":"The WC-4 `status` values therefore never replace an existing `success`, and two schemas never share one path.","touched_ok":"yes"},
    {"row":"R8","result":"resolved","evidence":"when the gate has no flag, the answer is folded into the command's main input","touched_ok":"yes"},
    {"row":"R9","result":"resolved","evidence":"does nothing under `--unattended` until its own phase except write its WC-4 report with `status: blocked`","touched_ok":"yes"},
    {"row":"R11","result":"resolved","evidence":"a call of exactly 240 s is allowed, a longer one is not","touched_ok":"yes"},
    {"row":"R12","result":"resolved","evidence":"lines already present before step 1 are ignored","touched_ok":"yes"},
    {"row":"R18","result":"resolved","evidence":"takes `--report-dir <dir>` under `--unattended`","touched_ok":"yes"},
    {"row":"R19","result":"resolved","evidence":"The `/sc:task` side is a P2 change","touched_ok":"yes"},
    {"row":"R21","result":"resolved","evidence":"AC-2.2's gate-trigger runs use a brief that does not offer answers","touched_ok":"yes"},
    {"row":"R22","result":"resolved","evidence":"the WC-4a report flag on every P2-P4 command that lacks one","touched_ok":"no","reason":"The missing-path duty is fixed, but the edited enablement predicate only blocks pending gates/outward defaults, leaving save's P3 shared-state conversion unprotected in P1 (N3)."},
    {"row":"R23","result":"resolved","evidence":"a call of exactly 240 s is allowed, a longer one is not","touched_ok":"yes"},
    {"row":"R24","result":"resolved","evidence":"at expiry the live check fails and the coordinator escalates while preserving the Dispatch","touched_ok":"yes"},
    {"row":"R25","result":"open","evidence":"a path under the run-specific output directory that holds the existing report step 3 accepted","touched_ok":"no","reason":"This admits workflow's package but not audit.log and return-contract.yaml in the mandatory nested reflect output directory; workflow's package contract names only reflect's REPORT.md. P0 step 6 still fails (N1)."}
  ],
  "new_rows": [
    {"label":"N1","grade":"MAJOR","rule":"FR-8","wrong_outcome":"A P0 workflow with a successful mandatory reflect writes audit.log and return-contract.yaml outside the workflow package. Step 3 accepts the package contract, whose reflect_report_path names only REPORT.md, so step 6 rejects the other mandatory nested files and the baseline phase cannot pass.","anchor":"a path under the run-specific output directory that holds the existing report step 3 accepted","finding":"The P0 artifact allowance misses nested reflect outputs: sk/sc-workflow-protocol/SKILL.md:58 invokes reflect with defaults; cmd/reflect.md:101 chooses a separate directory; sk/sc-reflect-protocol/SKILL.md:136,659 mandates log and contract; workflow refs/return-contract.md:17 exposes only REPORT.md. Spec:188,197.","side":"new","parent":"R25"},
    {"label":"N2","grade":"MAJOR","rule":"AC-1.2","wrong_outcome":"Following the P1 live check literally invokes workflow with --output, which is retired and correctly returns E-LEGACY, so the prescribed normal live check cannot pass without violating the workflow flag contract.","anchor":"7.2 live check on each P1 command with `--unattended --output <dir>`","finding":"Spec:199 demands a uniform output flag, but workflow is a P1 command (spec:162) whose row requires --report-dir and forbids --output (spec:95); sk/sc-workflow-protocol/SKILL.md:24 and refs/return-contract.md:39 confirm the rejection.","side":"new"},
    {"label":"N3","grade":"MAJOR","rule":"FR-8","wrong_outcome":"Before P3, P1 enables unattended save normally because it has no pending human gate or outward default. Two workers with separate report directories can then overwrite the same last_session.md whole, violating WC-11 before save's per-session-only conversion ships.","anchor":"Every other command runs normally under the flag.","finding":"Spec:162 blocks only gates/outward defaults yet enables all other commands. Save's shared-state conversion remains P3 (spec:122,164); cmd/save.md:42-45 writes one shared store and overwrites single-owner keys. Spec:71 forbids those concurrent writes.","side":"new","parent":"R22"}
  ]
}
```

<!-- review-ledger tail: written by review_ledger.py close; do not edit -->
## Review ledger

review: 3 of 3

| id | grade | rule | blocking | status | scope | anchor |
|---|---|---|---|---|---|---|
| R1 | MAJOR | WC-4 | yes | verified | in | Write the contract for pre-creation STOPs too |
| R2 | MAJOR | FR-8 | yes | verified | in | Commands that already write a contract keep their fields and add the missing ones. |
| R3 | MAJOR | FR-8 | yes | verified | in | `REPORT.md` (`report_path`) |
| R4 | MAJOR | WC-4 | yes | verified | in | where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) |
| R5 | MAJOR | WC-4 | yes | verified | in | Fix the contract filename to `<output>/adversarial/return-contract.yaml` |
| R6 | MAJOR | AC-0.4 | yes | verified | in | step 4 uses the command's existing report file, since the contract arrives in P1 |
| R7 | MAJOR | WC-6 | yes | verified | in | writes each run into a fresh output directory so a re-run starts clean |
| R8 | MAJOR | WC-3 | yes | verified | in | then re-invoke or resume the command with the answer as a flag |
| R9 | MAJOR | WC-9 | yes | verified | in | (a no-op where a command has no gate) |
| R10 | MAJOR | WC-7 | yes | verified | in | it never wraps the command in an Agent-tool subagent |
| R11 | MAJOR | FR-8 | yes | verified | in | A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) |
| R12 | MAJOR | WC-11 | yes | verified | in | only files under the brief's output directory (and the command's documented artifacts) appear |
| R13 | MAJOR | SA-4 | yes | verified | in | src/superclaude/commands/<name>.md |
| R14 | MINOR |  | no | deferred | in | The first sentence of the body states the report's status and verdict. |
| R15 | MINOR |  | no | deferred | in | Launch setup, not commands |
| R16 | MINOR |  | no | deferred | in | Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. |
| R17 | MINOR |  | no | deferred | in | prints nothing (SA-2, WC-8) |
| R18 | MAJOR | WC-4 | yes | verified | in | A command with no output flag uses the report flag its section 3 row names |
| R19 | MAJOR | FR-8 | yes | verified | in | `/sc:task` gives TFEP an `<output-dir>` other than the task worker's own WC-4 directory |
| R20 | MINOR |  | no | deferred | outside | ### 3.1 Ready today (10) |
| R21 | MAJOR | WC-3 | yes | verified | in | which is the route for `/sc:recommend`'s one clarifying question and `/sc:tdd`'s topic clarification |
| R22 | MAJOR | WC-9 | yes | verified | in | so no prompt and no outward default can run early |
| R23 | MAJOR | FR-8 | yes | verified | in | (one 300 s call is therefore not allowed) |
| R24 | MAJOR | WC-10 | yes | verified | in | the coordinator does not treat a heartbeat gap during a worker's subagent fan-out as a hang by itself |
| R25 | MAJOR | AC-0.4 | yes | open | in | a path in this worker's WC-4 report (`report_path`, `artifacts`) |
| R26 | MINOR |  | no | deferred | in | while `--numstat` printed `1 1` |
| R27 | MAJOR | WC-7a | no | deferred | outside | search the transcript for `AskUserQuestion` |
| R28 | MAJOR | 7.2 | no | deferred | outside | `observation.agentWait` is never non-null |
| R29 | MINOR |  | no | deferred | outside | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md |
| R30 | MINOR |  | no | deferred | outside | workflow states the contract is written for pre-creation STOPs |
| R31 | MINOR |  | no | deferred | outside | naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` |
| R32 | MINOR |  | no | deferred | in | (today adversarial, brainstorm, reflect, workflow, and troubleshoot when `--caller task-unified`) |
| R33 | MINOR |  | no | deferred | outside | "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. |
| R34 | MAJOR | FR-8 | yes | open | in | a path under the run-specific output directory that holds the existing report step 3 accepted |
| R35 | MAJOR | AC-1.2 | no | deferred | outside | 7.2 live check on each P1 command with `--unattended --output <dir>` |
| R36 | MAJOR | FR-8 | yes | open | in | Every other command runs normally under the flag. |

loop_decision: ESCALATE (U=3, X=0, I=true)
loop: ESCALATE (sweep pending)
