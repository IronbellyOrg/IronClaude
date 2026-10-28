# Research: Repeated review failure evidence deck

**Investigation type:** Cross-case analysis  
**Scope:** Frozen latest 30 top-level session logs and their linked task/review artifacts  
**Status:** Assembly complete from the listed research components; no independent gate verdict claimed  
**Date:** 2026-10-23  
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md`, Codebase Research Agent Prompt; Report Structure consulted for evidence and uncertainty standards  
**Intended output:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md`

**Assembly provenance:** This deck consolidates the existing deck, all six dedicated case reports, five screening reports, the rule map, frozen membership manifest and preserved screening captures. Additional recovered reports, original deep-analysis captures and historical-rule evidence were also read. The dedicated case reports were main-session transcriptions of restricted analysts' returned text, with that authorship limitation recorded in each report. This assembly does not claim a new investigation of every primary source, an independent quality-gate pass, completion of later phases or completion of the overall research task.

---

## Method and Counting Rules

The population is fixed by:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/session-manifest.txt`

It records the latest 30 top-level session files by modification time at the discovery inspection, `2026-10-23T03:25:59Z`. It freezes membership, not every source file's bytes. The current investigation, index 03, is excluded from historical cases and is not a negative control.

### Units must remain separate

| Unit | Definition | Counting boundary |
|---|---|---|
| Session | One top-level JSONL file in the frozen manifest | Nested reviewer logs support that session; they are not additional sampled sessions. |
| Incident | A particular plan-review stage, task or package-final gate | A shared package can contain several distinct incidents. Repeated operator authorizations do not create new tasks. |
| Review-stage result | One returned task verdict, consolidated plan-review result or package-final result | Multiple advocates, calibration rounds, notifications and persisted copies do not create additional review-stage results. |
| Finding | A distinct alleged defect or unmet requirement | Duplicates, non-defect notes, rejected claims and optional hardening are not all confirmed bugs. |
| Repair-to-review transition | An observed unsuccessful review, an applied repair and a subsequent review | A proposed repair, blocked edit, acceptance ruling or unreviewed final amendment does not satisfy this definition. |
| Policy-only re-review | A subsequent review triggered by changed process, without an intervening implementation repair | Kept separate from repair-to-review transitions. |
| Acceptance closure | A human accepts an explained unmet requirement or known defect | Does not turn the original verdict into `compliant` or establish that the defect was repaired. |

A quoted protocol, injected skill, seeded prompt, compacted recap, proposed command or search hit alone is not an observed execution or review failure.

Later findings use six distinguished classifications:

1. Introduced by the fix.
2. Preexisting but missed earlier.
3. Previous finding still unresolved.
4. Changed acceptance criteria or review scope.
5. Unsupported or invalid finding.
6. Unknown.

Before/after evidence is required to attribute a defect to a fix. Sequence alone does not prove introduction. A finding can contain separable subclaims with different classifications. Missing evidence remains visible.

### Selected population versus strict repeated failures

The six selected sessions contain six primary substantive repeated-unsuccessful-review incidents. They are not six identical binary failure loops.

| Subset | Members | Interpretation |
|---|---|---|
| Strict operational repair followed by another unsuccessful review | Oracle Task 12; Orca monitor Task 12; credential follow-up final gate | Three primary incidents have applied delivery/evidence repairs followed by another failed operational review. |
| Repeated verification blocker after evidence-only resubmission | Manual-page Task 6 | Two `cannot-verify` results with unchanged delivered text and unchanged missing render proof. Kept separate from a repair-induced implementation defect. |
| Repeated unsuccessful planning reviews | Orca planning; CI plan regeneration | Raw `partial`/`PARTIAL` statuses and not-ready judgments remain as recorded. They are not relabeled binary `FAIL`. |
| Successful one-repair and operational controls | Separate tasks/packages and screened sessions | Retained as counterevidence; not added to the strict subset. |

These are descriptive classifications within the frozen sample, not a prevalence estimate for real executions, a controlled model comparison or a fleet-wide regression rate.

**Key Takeaways**

- Session, incident, review, finding and transition counts answer different questions.
- The strict operational subset is not enlarged with synthetic logs, unchanged-plan reviews, separate task failures or planning `partial` results.
- Accepted gaps and successful structural checks do not establish repaired behavioral compliance.

---

## Screened Session Inventory

Original full paths are recorded in the frozen manifest. The following table retains every membership slot. Screening findings are navigation and selection evidence; dedicated cases provide the deeper validity and causality analysis.

| Index | Session prefix | Disposition | Reason and supporting source |
|---|---|---|---|
| 01 | `6f744b87` | Selected | Task 6 returns `cannot-verify` twice; separate Task 2 baseline dispute is a control. `scope-01.md`; case 03. |
| 02 | `eabc78ed` | Excluded from target-loop count | Troubleshoot/adversarial diagnosis of PR findings, no target workflow/implementation execution. `screening-recovery-source.txt`, Session 02. |
| 03 | `bbddbf85` | Excluded current investigation | Not independent historical evidence; content deliberately excluded. Manifest and `scope-01.md`. |
| 04 | `43582de1` | Selected | CI plan refactor/regeneration followed by further semantic findings. `scope-01.md`; case 04. |
| 05 | `e002bed2` | Selected | Orca monitor Task 12 has a sustained repair/re-review chain. `scope-01.md`; case 05. |
| 06 | `99d5f896` | Excluded | Proposal comparison and recommendation changes, no target command execution. `screening-recovery-source.txt`, Session 06. |
| 07 | `562ef463` | Excluded | Discovery conversation, no target invocation. `screening-handoffs-source.txt`, Session 07. |
| 08 | `ad0d7890` | Excluded | Brainstorm/evaluation activity, outside the requested command family. Its protocol problems are not these review loops. `screening-handoffs-source.txt`, Session 08. |
| 09 | `15345c19` | Operational control | Seven task reviews compliant. Final review explicitly never ran because overlapping work rewrote the same files. `screening-handoffs-source.txt`, Session 09. |
| 10 | `0d43d44d` | Successful-repair control | Task 4 missing, comment repair, compliant. Separate Task 6 CI evidence gap must not be joined into the same incident. `scope-02.md`. |
| 11 | `428a336e` | Excluded from strict loops | Parallel reviewers assess the same unchanged plan; no applied repair followed by another failure. `scope-02.md`. |
| 12 | `976b97f5` | Excluded | Workflow creation only. Later implementation belongs to another session. `scope-02.md`. |
| 13 | `c444c002` | Related precursor | Plan corrections without a second semantic review; initial package later implemented in index 15. `scope-03.md`. |
| 14 | `10cacee5` | Related precursor | Plan corrections without a second semantic review or implementation in that session. `scope-03.md`. |
| 15 | `0690ee9f` | Selected | Two distinct final-gate packages: initial fail-fix-pass control and follow-up fail-fix-fail-fix-pass incident. `scope-03.md`; case 06. |
| 16 | `97c47129` | Excluded | Feature follow-up correction, PR and cleanup, no target execution. `screening-recovery-source.txt`, Index 16. |
| 17 | `0f6383e1` | Successful-repair control | Real retry-feature implementation: bounded Task 8 repair and separate final-gate repair. Later PR review is another process. `scope-03.md`. |
| 18 | `5290b7ae` | Excluded | Script analysis/PR/troubleshoot, no target execution. Use corrected physical anchors, not earlier Unicode-split line numbers. `screening-recovery-source.txt`, corrected Index 18. |
| 19 | `45eb8186` | Operational control | Tasks 1-9 compliant. Later Task 12 entries in the shared ledger belong to index 05, not this session. `scope-04.md`. |
| 20 | `ac2cd1fd` | Selected | Plan 16 findings, corrected v2, 20 numbered second-review items, targeted partial recheck, unreviewed v4. `scope-04.md`; case 01. |
| 21 | `2a6286d3` | Synthetic exclusion | Mocked retrospective with literal mock counters and no operational tools. `screening-handoffs-source.txt`. |
| 22 | `51f17e6b` | Synthetic exclusion | Mocked phase summary, no operational tools. Same source capture. |
| 23 | `ba18b090` | Synthetic exclusion | Mocked retrospective, no operational tools. Same source capture. |
| 24 | `6d203c97` | Synthetic exclusion | Mocked phase summary, no operational tools. Same source capture. |
| 25 | `105b1734` | Excluded | Session setup only, no tools. `scope-05.md`. |
| 26 | `f597ad3b` | Excluded from target-loop count | Operational reflection, PR and diagnosis activity, but no qualifying target repair loop established. `scope-05.md`. |
| 27 | `a9b88895` | Selected | Oracle Task 12: four findings, three repaired, frozen-input finding retained, authorized correction passes. `scope-05.md`; case 02. |
| 28 | `44709b0f` | Synthetic exclusion | Mocked retrospective, no operational tools. `screening-handoffs-source.txt`. |
| 29 | `8ba23e21` | Synthetic exclusion | Mocked phase summary, no operational tools. Same source capture. |
| 30 | `fda5564b` | Synthetic exclusion | Mocked retrospective, no operational tools. Same source capture. |

Seven sampled files are synthetic. Several others lack a target invocation. Modification-time selection can promote old conversations that were recently touched. Therefore the six selected sessions must not be reported as a measured failure rate among 30 comparable operational runs.

**Key Takeaways**

- All 30 membership slots have a disposition.
- Parallel review, unrelated review systems and synthetic retrospective text are explicitly excluded from strict repair-loop counts.
- Later contents of a shared ledger must not be back-attributed to an earlier session.

---

## Selected Sessions and Incident Deduplication

### Exact primary session paths

All later references to a named log and physical record resolve through this table.

| Named primary log | Absolute path |
|---|---|
| Orca planning log | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl` |
| Oracle log | `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl` |
| Documentation log | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl` |
| CI planning log | `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` |
| Orca monitor log | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl` |
| Credential final-review log | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl` |

### Incident keys

| Selected session | Primary incident and stable deduplication key | Relationship and boundary | Dedicated case |
|---|---|---|---|
| 20, Orca planning | Orca plan review, `orca/designSpec132541/planning` | One planning incident, two full pre-reviews and one targeted review, four plan versions. Later implementation in indexes 19/05 is a distinct stage. | `01-session-ac2cd1fd.md` |
| 27, oracle | Claim-gate oracle, `claim-gate/designV2-132032/T12` | One task, two failed independent reviews and one passing authorized-correction review. Task 11 carryover excluded. | `02-session-a9b88895.md` |
| 01, documentation | Manual-page rendering, `issue358FollowUp210638/T6/render` | One repeated evidence-blocker incident. Task 2 baseline dispute is a separate repair control. | `03-session-6f744b87.md` |
| 04, CI planning | CI refactor, `ci-followup/spec211556+specR1031725/planning` | One plan-family incident across two generated packages. Advocates and calibrators are not independent repair cycles. | `04-session-43582de1.md` |
| 05, monitor | Orca monitor, `orca/designSpec132541/T12` | One implementation incident with multiple fresh-review rounds. Tasks 10/11 and later Task 13 remain separate controls. | `05-session-e002bed2.md` |
| 15, credential finals | Credential follow-up final gate, `review-loop:issue358FollowUp193837:final:20261022` | One strict repeated final-evidence incident. Initial `issue358InTempla151058` final gate is a separate successful-repair control. Later `issue358FollowUp210638` belongs to index 01. | `06-session-0690ee9f.md` |

Case paths resolve under:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/`

### Review and transition denominators

These counts apply only to each named primary incident, not every review in its session.

| Primary incident | Observed review-stage results | Unsuccessful results, preserving raw meaning | Applied repair followed by review | Separate boundary |
|---|---:|---|---:|---|
| Orca planning | 3 | Two full `partial` results; targeted `PARTIAL` for both selected findings | 2 | Final v4 edits have no subsequent semantic review. |
| Oracle Task 12 | 3 | Two `FAIL`/`missing`; later `PASS`/`compliant` | 2 | Archive authorization blocker is not another task review. |
| Manual-page Task 6 | 2 | Two `cannot-verify` | 1 evidence-only resubmission | Later package FINAL pass follows acceptance, not repaired rendering. |
| CI planning | 2 consolidated plan-review stages | Original not-ready; regenerated `not_ready` with `partial` evidence status | 1 | No implementation observed. |
| Orca monitor Task 12 | 7 | Six noncompliant results and one `compliant` | 5 | `compliant` to fresh `missing` after protocol migration has no intervening repair; count separately. |
| Credential follow-up FINAL | 3 | Two `issues`, then `pass` | 2 evidence-repair transitions | Evidence corrections and rubric change both precede the last pass. |

Finding counts are not summed across these rows. In particular, 20 Orca numbered items, 18 initial CI concerns, 16 later CI merged items, four oracle defects and multiple monitor failure families have different deduplication and validity boundaries.

**Key Takeaways**

- Six selected primary incidents do not mean six independent repositories or six uniform review procedures.
- Review-stage counts are not counts of unique reviewer agents.
- The monitor's migration re-review and human acceptance closures remain outside repair-transition counts.

---

## Chronological Failure, Fix and Resubmission Evidence

### Orca planning: successive repairs changed contracts and dependencies

**Primary package**

`/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/`

| Event | Original physical record and UTC time | Observed evidence |
|---|---|---|
| First completed pre-review | Orca planning log 499, `2026-10-22T14:09:01.093Z` | Sixteen findings, 13 important and three minor; raw status `partial`. |
| Authorized repair | 511, followed by 544 at `15:08:38.839Z` | User authorizes applying findings. A successful whole-file **Write**, not Edit, produces v2. |
| Second completed pre-review | 821, `15:45:18.570Z` | Twenty numbered items; status remains `partial`; two high-severity blockers. |
| Authorized v3 | 824, then 841 at `15:53:15.796Z` | Another whole-file Write applies the next set. |
| Narrowed fresh review | 858 authorization; 874 at `15:56:35.717Z` | Both selected findings remain `PARTIAL`. |
| Final amendment | 889 authorization; 906-934 successful edits | Fifteen targeted edits produce v4. Structural gate passes. |
| Disclosed endpoint | 946, `16:05:53.370Z` | Explicitly says v4 has had no review since the edit. |

The initial cleanup attempt at records 150/151 was blocked; only the retry at 163/164 applied. A blocked attempt is not an applied mutation.

The detailed next-review checklist accepts **14 original plan amendments and marks two partial**, correcting the second report's “13 fixed, three partial” summary. Accepted amendments are not runtime verification. The 20 second-round items include a duplicate sufficiency/meta-item and a concurrency note explicitly classified as not a defect.

**Primary review roots**

- `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/`
- `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/`
- `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v3-targeted-20261022155651/`

**Key Takeaways**

- The planning loop contains real fix-introduced defects, old omissions and incomplete repairs.
- Both full reviews used the same driving-source hash; source-byte changes do not explain their differing findings.
- It stopped through authorized narrowing and an explicitly unreviewed final amendment, not clean semantic convergence.

### Oracle Task 12: three repairs worked while one known fixture defect was retained

**Primary package**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/`

| Event | Original physical record and UTC time | Observed evidence |
|---|---|---|
| Original failure | Oracle log 291, `2026-10-21T21:47:06.709Z` | Four genuine compliance defects, despite 67 default and 78 acceptance tests passing. |
| Restricted repair | 383, `21:49:47.309Z` | Authorizes findings 1-3 only. Explicitly prohibits altering frozen fixture 4, its pins or adding duplicate retention to hide the omission. |
| Actual changes | Builder trace 189-196 and 206-211; parent return 398 | Verification predicates, author contrast and missing-abstraction contrast corrected. |
| Second failure | 450, `22:03:12.606Z` | Confirms the three repairs. Same frozen security record still has default-path false. |
| Authorization changes | 521, `2026-10-22T00:19:07.882Z` | Human authorizes frozen-fixture correction. |
| Bounded correction | 573, 579, 585-586 | One boolean changes, a semantic assertion is added and hash pins are updated. Original fixture retained; prior acceptance evidence superseded. |
| Passing review | 668, `00:26:48.291Z` | Fresh independent `PASS`/`compliant`. |

The builder trace is:

`/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1/subagents/agent-aoracle-builder-6889f23314fbb16e.jsonl`

Full review evidence survives in the package's `artifacts/t12-review-1.md`, `artifacts/t12-review-2.md`, `artifacts/t12-review-authorized.json` and `artifacts/t12-held-back-before-authorization.json`.

**Key Takeaways**

- The second failure was retained known work, not an invented new criterion or predicate regression.
- The original requirement was satisfiable before freeze. The later repair boundary excluded the chosen correction until new authorization.
- Passing test counts established less semantic coverage than the original requirements demanded.

### Manual-page Task 6 and separate baseline control

**Historical package**

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/`

| Event | Original physical record and UTC time | Observed evidence |
|---|---|---|
| Initial manual-page edits | Documentation log 406/408 | Identical sentence added to both pages. |
| Nominal render check | 413-414 | Output discarded; nominal command returns zero. |
| First review | 430, `2026-10-22T21:19:57.564Z` | `cannot-verify`: the command named `man` prints a minimized-image notice, not a render. |
| Evidence-only retry | 433-434; request 443 at `21:20:14.983Z` | Static roff checks added; request explicitly states no text changed. |
| Second review | 450, `21:20:22.606Z` | `cannot-verify (unchanged)`: static proof does not settle the render condition. |
| Escalation guard | 485-486 | Missing task-start HEAD file maps to the guard's `head-moved` category. No actual HEAD movement is thereby proved. |
| Correct acceptance | 498/503/506 | Wrong-task acceptance is rejected; user explicitly accepts Task 6 at `21:22:58.712Z`. |
| Package closure | 527 and 530-531 | FINAL passes and archive succeeds while the rendering gap remains honestly unmet. |

The nominal renderer is a notice script. The preserved evidence reports missing actual rendering tools. The initial zero status is not proof of rendering, and static macro counts do not establish warning-free output. No malformed-page defect was demonstrated.

The separate Task 2 control has this sequence:

| Event | Primary anchor | Adjudication |
|---|---|---|
| Reconstructed baseline after edits | Documentation log 188 | Substitutes HEAD for a test file already dirty before the task. |
| `extra` review | 204, `21:16:03.671Z` | Overbroad supplied diff makes earlier header/key-fanout work appear task-owned. |
| Narrowed diff | 217/222 | Full diff preserved; disputed hunks removed from review input. |
| `compliant` | 234, `21:16:31.439Z` | Historical reviewer explicitly relies on executor's provenance account. |
| Independent case check | Earlier Git tree `f60d2c3…`, reconstructed tree `3c5fdfa…`, later tree `00d8f4a…` | Earlier truthful tree contains the disputed hunks; narrowed diff matches the genuine task delta. |

**Key Takeaways**

- Task 6 repeats an unchanged environmental evidence blocker.
- Task 2 corrects change attribution, not actual extra-scope implementation.
- A final pass with accepted `cannot-verify` is not successful rendering.

### CI plan regeneration: incomplete checking repairs and a graph defect

**Original package**

`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/`

**Regenerated package**

`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/`

| Event | Original physical record and UTC time | Observed evidence |
|---|---|---|
| First review result | CI planning log 623, `2026-10-22T21:46:39.278Z` | Eighteen merged concerns, 10 medium and eight low; not-ready judgment. |
| Refactor authorization | 627, `2026-10-23T03:16:29.302Z` | User authorizes refactor. |
| Source/regeneration | 651/653 and 663/670 | Original specification retained; feedback appended; new package generated. |
| Intermediate claims | 791, 801, 810/821 | Orchestrator initially says every note applied. Calibrator says previous findings were not individually checked; reviewer gives provisional closure/new-finding counts. |
| Original observation boundary | Inspection at `03:41:52.643460Z`, 1,000 rows | Invariant probe still running; no completed second report yet. |
| Later completed review | 1003-1084 | Probe, merge and citation validation complete. |
| Final observed result | 1084, `03:48:11.615Z` | `not_ready`, five medium and 11 low merged items, no high; operational evidence status `partial`. |
| Supplemental observation | `04:02:04.400203Z`, 1,086 rows | No later refactor authorization or implementation observed. |

The regenerated review root is:

`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/`

Its `partial` status reflects two dropped incorrect citations, not a review still running. The report records corrected supporting lines, while retaining the evidence drops.

The original 18 concerns, later 16 merged items and eight second-reviewer entries are overlapping finding inventories. They are not review-cycle counts and must not be added together.

**Key Takeaways**

- Regeneration made substantial repairs but did not close every failure mechanism.
- Optional boundary-file hardening and source-level allowlist tension were initially overstated.
- The graph defect has before/after support; no actual runtime misordering or product-code regression was observed.

### Orca monitor Task 12: seven verdicts, five repairs and a policy reopening

**Workflow**

`/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/workflows/orca-upstream-monitor.yml`

**Package**

`/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/`

| Stage | Primary physical record and UTC time | Observed result |
|---|---|---|
| Initial workflow | Orca monitor log 585, `2026-10-22T19:56:32.313Z` | 640-line workflow; structural checks pass. Behavioral/job-wiring tests are deferred to Task 14. |
| First verdict | 697, `20:10:58.253Z` | `missing`: collectors/error reporting/summaries/provenance. |
| First repair and second verdict | 716-766, then 804 at `20:19:54.643Z` | Prior repairs hold. Preexisting range bug and retained PR-list error propagation remain. |
| Operator repair and third verdict | 820/825/827, then 849 at `20:33:49.079Z` | Original reviewer returns `compliant`. |
| Protocol migration | 874/884/893/902 | Newly loaded migration rule requires fresh operator review before completion. |
| Fourth verdict | 906, `20:46:07.164Z` | `missing`: detect summary, blank notes, absent upper tag, carriage-return handling. |
| Third repair and fifth verdict | 921/937-994, then 1021 at `21:27:34.002Z` | `missing`: early pin-step failures and reproduced argument-size failure, plus related findings. |
| Fourth repair and sixth verdict | 1044/1060 onward, then 1143 at `21:49:17.041Z` | `missing`: checkout fallback, unchecked provenance and output/hardening concerns. |
| Fifth repair and seventh verdict | 1153/1188-1210, then 1240 at `2026-10-23T03:31:41.631Z` | `misunderstood`: selected-release outage classification, unbounded links fallback, trap contamination, newline validation. |
| Original prefix endpoint | 1247, `03:31:57.433Z` | Halt for operator direction. |
| Separate acceptance continuation | 1250 at `03:44:11.059Z`; successful 1261 at `03:44:25.599Z` | Human accepts four defects. Task completes with unchanged `misunderstood`. No eighth Task 12 review. |

The original analyzed prefix is records 1-1247, not a content snapshot at membership-selection time. A later supplement observes growth to 1,437 rows. Its retrospectively calculated prefix hash is not proof of an original-time byte snapshot.

The seven verdicts are six noncompliant and one compliant. The five repair passes are the ordinary repair plus four operator-authorized repairs. The first three verdicts came from the original reviewer; four later verdicts came from fresh reviewers. No Task 12 adviser, retry-ladder or revert records were observed.

Later Task 13 reviews and acceptance belong to a separate task. Through the supplement's boundary, Task 14 had started but no Task 14 reviewer result was observed.

**Key Takeaways**

- Most later findings existed in the original workflow.
- One repair-induced implementation regression is demonstrated: inherited error-trap output contaminates a captured value.
- The compliant result was reopened by a real protocol migration.
- Later completion accepts known defects; it does not verify repair or convert the verdict to compliant.

### Credential final gates: durable evidence and a changed rubric

**Initial package**

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/`

**Follow-up package**

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/`

| Incident | Primary sequence | Changes and outcome |
|---|---|---|
| Initial package, control | Credential log 390 `FINAL: issues`; 396 user reopens evidence; 411 durable comparison; 415 corrected completion; 435 pass/archive | Genuine temporary lint proof had been replaced by a README separator citation. Durable proof establishes 28 before, 28 after and zero changed-line findings. No delivery-file change. |
| Follow-up first FINAL | 1215/1230 show known changed-line lint findings and “no new findings” reinterpretation; 1932 issues; 1938 user “accept and fix”; 1968/1969 corrections | Task QA knowingly softened the literal no-finding-on-changed-line rule without prior acceptance. FINAL applies the original rule and flags evidence pointers. |
| Follow-up second FINAL | Nested reviewer `agent-acf0a51e6992c50ee.jsonl` record 116, `2026-10-22T20:31:27.048Z`; parent 2012 corroborates blank pointer | Task 10 citation was wrong when created at parent 1425. Earlier FINAL missed it. First Task 7 evidence repair also omits the last row. |
| Further correction | Parent 2015/2016 and acknowledgment 2028 | Evidence pointers repaired, delivery digest unchanged. Task 10 correction exceeds the expressly named Tasks 7/8/17 authorization; no intervening new authorization observed. |
| Third FINAL | Different rubric read at nested `agent-a4bfff371c63a6c39.jsonl` record 18; parent 2036 pass/archive | Both corrected evidence and changed policy precede pass. Their separate effects cannot be isolated. |

Nested reviewer paths are under:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/`

The follow-up ledger does not record the second `FINAL: issues`. Its reality comes from the nested conclusion and parent evidence, not a reconstructed historical ledger entry.

Historical delivery-state digests remain unchanged within the respective final-review sequences. That does not mean evidence artifacts and loaded review rules stayed unchanged.

**Key Takeaways**

- The initial package is normal evidence repair, not strict repeated failure.
- The follow-up's second failure is an old evidence defect missed earlier, not a repair-induced delivery bug.
- Final pass is confounded by changed policy and corrected evidence.
- The accepted lint gap and a narrow preexisting manual-page instruction omission prevent treating PASS as proof of universal literal completion.

---

## Cross-Case Transition Matrix

“Strong” below means the assembled case supplies primary before/after artifacts, an explicit recorded action or corroborated reproduction for the narrow claim. It does not mean controlled general causation. “Bounded” marks plan-text, local-reproduction, scope or historical-state limits.

| Transition | Mechanism and causal classification | Primary support | Opposing evidence or limit | Strength |
|---|---|---|---|---|
| Orca plan first review to v2 second review | Local repairs change release eligibility, old-value source, test dependencies and extraction boundaries. Mixed introduced defects, old omissions and incomplete repairs. | Planning log 499 → successful Write 544/545 → 821; historical v1/v2 and both merged finding sets. | Fourteen original amendments accepted; not every later item is new or a defect. No runtime execution. | Strong for identified plan introductions; bounded for behavioral consequences. |
| Orca plan second review to targeted v3 review | Primary validation/state repairs leave secondary paths; v3 also adds unsafe error wording and an ill-defined mutation. | 821 → Write 841 → reviewer 874. | Review deliberately narrowed; absence of an extra mutation alone is not proof of faulty behavior. | Strong for text history; bounded for unexecuted risk. |
| Oracle first to second failed review | Three fixes work; repair authority excludes the fourth frozen-input correction. | Oracle 291 → 383 and builder changes → 450; original fixture and full review files. | Original requirement could have been satisfied before freeze. Not proof all repair routes were mathematically impossible. | Strong. |
| Oracle second failure to passing review | Human permits one-field fixture correction, re-freeze and semantic assertion. | 450 → 521 → 573/579/585-586 → 668. | Historical reviewer lacked a separately preserved full pre-authorization oracle snapshot. No live-model effectiveness result. | Strong for fixture correction; bounded for full-file oracle comparison. |
| Documentation first to second Task 6 review | Static proof resubmitted without a renderer or source change; same criterion remains unverified. | Documentation 430 → 433-434/443 → 450. | No malformed page demonstrated; a working environment could satisfy the criterion. | Strong. |
| CI first to regenerated review | Exemption repaired in status but not hashes; old search-check weakness survives; graph repointing loses ancestors. | CI 623 → 627/651-670 → second plans/review → 1084. | Sequential executor prevents asserted runtime reorder. Optional hardening was initially overstated. | Strong for plan/check defects; no runtime failure observed. |
| Monitor first to second verdict | Error-handling repairs leave PR-list substitution failure; the preexisting equal-tag case is newly demonstrated, while older-pin behavior was already observed as nonblocking and is now treated as a defect. | Monitor 697 → 716-766 → 804; original 585. | Reviewer explicitly says range was already wrong before repair. | Strong. |
| Monitor second to compliant verdict | Range/PR-list corrections accepted by original reviewer. | 804 → 820/825/827 → 849. | Later fresh reviewer finds other old defects; acceptance is not exhaustive correctness. | Strong for observed successful recheck. |
| Monitor compliant to fresh missing | Mid-run migration mandates fresh review, without intervening implementation repair. | 849 → loaded rules 874/884 → dispatch 893 → explanation 902 → 906. | Does not show the new protocol created old implementation defects. | Strong policy-only transition. |
| Monitor fresh failures after third/fourth repairs | Repairs cover individual execution boundaries; larger-input transport repair exposes later preexisting output limits. | 906 → 937-994 → 1021; 1021 → 1060 onward → 1143; original 585. | File transport does not create preexisting unbounded renderer output. Exact thresholds depend on inputs. | Strong for traced boundaries; local reproduction limits apply. |
| Monitor sixth to seventh verdict | Prior fixes leave outage/fallback/newline gaps; an earlier stdout trap regression is finally reproduced. | 1143 → 1188-1210 → 1240; introduction at 759-762, original 585/helper 171. | Trap defect came from first repair, not necessarily the immediately preceding one. Other late gaps were old or broader design requirements. | Strong for trap introduction; mixed for other findings. |
| Credential initial FINAL to pass, control | Lost durable proof is restored and cited correctly. | Credential 390 → 396/411/415 → 435; nested reviewers and archived lint log. | Delivery already met the lint criterion. This is not delivery repair. | Strong. |
| Credential follow-up first to second issues | Accepted lint exception and named pointer repairs leave a preexisting blank Task 10 citation; one repaired range remains incomplete. | 1932 → 1938/1968 → nested second FINAL 116; original bad pointer 1425 and log blank line. | Why first FINAL missed Task 10 is unknown; no delivery change. | Strong for evidence history, unknown for reviewer cognition. |
| Credential second issues to pass | Evidence repair plus changed loaded FINAL policy. | 2015/2016 → historical nested rule reads → 2036. | No controlled same-rubric comparison isolates which change produces pass. | Strong for confounding; separate causal effects unknown. |

### Non-review stopping transitions

| Incident | Observed stop/closure | What must not be inferred |
|---|---|---|
| Orca planning | User authorizes v4 after targeted partial result; no later semantic review | Clean independent pre-review approval. |
| Manual-page Task 6 | Scoped acceptance; complete with `cannot-verify`; package FINAL pass | Successful rendering. |
| Orca monitor Task 12 | Human accepts four defects; complete with `misunderstood` | Eighth review, repaired defects or compliant implementation. |
| CI planning | Completed partial/not-ready result asks for user decision | Authorized second refactor or implementation. |
| Oracle package | Later archive blocker lacks separate ruling | Another failed Task 12 review. |

**Key Takeaways**

- Successful repair, changed review policy and acceptance are visibly different transitions.
- A late-discovered regression may originate several repair rounds earlier.
- Removing one failure can expose another preexisting failure farther along the same path.

---

## Finding-Level Causal Classification

### Six causal classes

| Class | Admission rule | Supported examples | Opposition and limits |
|---|---|---|---|
| Introduced by fix | Earlier state lacks the specific defect; successful logged change introduces the mechanism | Orca release predicate/source/order changes; CI missing ancestors; monitor inherited stdout trap | Newly noticed alone is insufficient. Plan defects are not automatically runtime regressions. |
| Preexisting, missed earlier | Original artifact already contains the later-identified mechanism | Monitor equal-tag/absent-upper-tag paths, output and summary boundaries; CI search assertions; credential blank pointer | Exact reason for the earlier miss often remains unknown. |
| Previous finding unresolved | Same required property remains unmet after repair | Frozen fixture; missing render proof; incomplete tooling exemption; incomplete summary family | A broader family may contain separately discovered paths. Do not label every path the identical finding. |
| Changed criterion or review scope | Actual rubric/input/scope change, or stronger demand beyond original literal requirement | Credential loaded rubric; monitor migration and broader hardening; targeted plan review | Original oracle default-path criterion was not newly invented. |
| Unsupported or invalid | Source disproves attribution, claim withdrawn, duplicate/non-defect or no concrete failing path | Dirty-baseline extra-scope attribution; concurrency removal; duplicate sufficiency; optional hardening overclaims | Useful hardening can remain useful without being an original defect. |
| Unknown | Before/after evidence or causal reasoning is absent | Many reviewer miss explanations; rubric updater; separate effect of rubric change on final pass | Unknown must not be converted into context exhaustion, capability failure or repair causation. |

### Orca planning: later findings and targeted observations

Primary support is the historical source and requirements, logged Writes at Orca planning 544/841, targeted return 874, successful v4 edits 906-934, and the case's complete second-round trace. Each row retains the narrow mechanism and its validity limit.

| Finding | Classification and mechanism | Support and observed response | Opposition/limit; strength |
|---|---|---|---|
| Four-asset refusal moved into early release detection | Introduced specification divergence: release existence and pin-writer eligibility were different predicates | Original source distinguishes them; v2 strengthens early check; v3 restores separation | No runtime execution. Pin-equals-current objection was withdrawn. Strong plan-text chain. |
| Old lock digest changed to deployed-package provenance | Introduced contract substitution, with other old-value gaps unresolved | Companion field table names recipe digest; v2 chooses provenance; v3 enumerates intended sources | Provenance might be a defensible approved design change, but no such change was declared. Strong. |
| Inventory test precedes registration | Introduced acceptance-order defect | New test in Task 13, required route registration in Task 14; actual inventory test rejects missing entry; v3 reorders | Structural/acceptance defect, not observed runner failure. Strong. |
| Renderer tests exclude operations they need | Introduced ambiguity plus incomplete original integration fix | v2 extraction consumes JSON while cap/filter ownership is unclear; v3 assigns ownership and integration checks | No deployed unsafe renderer proved. Strong text history, bounded execution claim. |
| Explicit fetch names an unestablished/wrong remote | Introduced concrete instruction error atop original underspecification | v1 unnamed fetch; v2 names `origin`; v3 adds scratch/upstream setup | No fetch executed. Strong. |
| Validation happens after external use | Preexisting ordering omission | Original decision-stage check follows fetch; v3/v4 add guards | Some source instructions conflict; generic validation presence is not ordering proof. Strong. |
| Candidate/pinned-output checks incomplete | Preexisting test/output ambiguity | Original and v2 lack explicit pinned empty-version behavior and full contrasts; v3 adds cases | Not evidence of an observed faulty dispatch. Bounded. |
| Dispatch flags/manual target untested | Preexisting assignment/test weakness | Instructions name operation but checks do not assert arguments; v3 adds extracted dispatch checks | Test weakness, not demonstrated wrong execution. Bounded. |
| Repository failure versus outage precedence lacks joint fixture | Unresolved/strengthened testing demand | Individual mismatch fixed; combined bad repository plus failed metadata case added later | Individual repair was successful; separate before-fetch contradiction remains. Strong distinction. |
| Release-pruning credentials/environment unasserted | Preexisting test weakness | Source mappings exist; earlier shape tests do not assert them; v3 adds checks | No secret exposure or faulty credential use observed. Bounded. |
| Manual upstream metadata/rejection cases absent | Preexisting interface/testing gap | Original plan lacks explicit manual-tag metadata fetch and rejection cases; v3 supplies them | Plan omission, not failed live lookup. Bounded. |
| Current-pin state cannot express required patch-check path | Preexisting omission plus conflicting source | Source diagram says no-op while behavioral prose requires named nonempty state; v3 adds state | Exact runtime positive control remains unproved. Strong contradiction, bounded runtime conclusion. |
| Shape-check mechanism unspecified | Changed review precision/executability clarification | Later merge rejects unsupported parser proposal and names existing mechanism | Not demonstrated functional regression. Bounded. |
| Toolchain/diagnosis procedure not executed by tests | Old finding partly unresolved | v2 adds procedure and canned rendering; v3 defers actual probe/parser to live acceptance | Not an automated test repair. Strong. |
| Rollback comparison direction not asserted | Incomplete renderer-testing repair | Newly added fixture omits link direction; v3 adds exact link and mutation | Not a newly reversed runtime link. Bounded. |
| Concurrency key concern | Withdrawn/non-defect note | Historical calibration accepts documented support and non-cancellation pairing | No independent present-day platform documentation claim. Strong historical disposition. |
| Base-result comparison lacks recorded baseline | Introduced executable-acceptance gap | New reader checks ask match-base without capture; v3 adds capture | Earlier local failure comparison also existed; no execution claimed. Strong. |
| Logs could be staged | Preexisting advisory hygiene risk | Logs existed originally; later amendment says never stage | Not a behavioral defect; no staging observed. Bounded. |
| PR head undefined by mode | Incomplete old fix plus source tension | Open-only rollback exception repaired; branch definition still ambiguous; v3 names modes | Closed/merged rollback handling was already present. Strong narrowed finding. |
| Sufficiency item | Duplicate/meta-finding | Repeats validation/state/old-value issues | Not another independent defect. Strong deduplication. |
| Secondary collector tags unchecked | Preexisting omission missed by primary-path repair | Targeted return traces additional sources; v4 adds filters/checks | No final independent recheck. Strong text history. |
| Bad-value error echoes untrusted value | Introduced v3 plan risk | v3 explicitly asks to name bad value; v4 changes to input name only | No exploit observed. Strong introduction, bounded security consequence. |
| Annotated-tag URL followed unchecked | Preexisting inherited source contradiction | Source instructs following upstream URL; conflicts with before-use validation; v4 switches to fixed endpoint/digest | No final independent verification. Strong source tension. |
| Missing fetch-level malformed rollback case | Incomplete correction | Decision-script test is too late to establish before-fetch guard; v4 adds case | Test absence alone does not show every invalid input reaches a call. Bounded. |
| Missing guard mutations | Incomplete testing promise/stronger demand | v4 adds candidate/resolver mutations | Existing malformed-input tests may already detect removal. Do not count each absent mutation as a functional bug. Bounded. |
| Downstream dependency explanation absent | Clarification, not established faulty wiring | Existing dependency syntax already connects jobs; v4 adds explanation | No unguarded path demonstrated. Strong rejection of overclaim. |
| State-removal mutation cannot be applied as written | Introduced v3 acceptance instruction defect | Source condition checks nonempty state, not a state list; v4 changes mutation | No final semantic re-review. Strong. |
| Pin/rollback no-op output state unspecified | Incomplete missing-state repair | v4 supplies named state and empty target | Source scope tension remains. Bounded. |
| Exact up-to-date-week live check absent | Unresolved verification limit | v4 retains generic live-expression statement | Not proof workflow runtime is wrong. Bounded. |
| Repository self-check still after fetch | Preexisting unresolved source contradiction | Prefetched-input design and before-any-upstream-call requirement conflict | Final edit does not reconcile them. Strong contradiction. |

### Orca planning: successful original repairs retained

The first review did produce substantial accepted amendments. The case's complete original-repair supplement records all 16; these summaries must not disappear behind the later failures.

| Original repair | Next-review disposition and qualification |
|---|---|
| Filter rollback choices by required assets | Accepted; renderer-test boundary still needed correction. |
| Add rollback format/release checks | Accepted; stronger early predicate introduced a different divergence. |
| Preserve open-only rollback PR exception | Accepted; later mode-specific head definition still needed. |
| Add toolchain/diagnosis procedure and fixtures | Partial; rendering fixtures did not execute real probe/parser. |
| Assign patch digest/candidate computation | Accepted, successful non-recurring repair. |
| Add individual patch-digest mismatch fixture | Accepted; later joint-precedence fixture is a distinct stronger demand. |
| Apply runner/timeout rules to every monitor job | Accepted, successful non-recurring repair. |
| Define pin input validation and target derivation | Accepted; before-fetch placement and early eligibility remain distinct issues. |
| Extract renderer and capture old values | Partial; boundary and old-value source remained problematic. |
| Name companion specification | Accepted, successful discoverability repair. |
| Add local workflow-reader checks | Accepted with ordering/baseline qualifications. |
| Stop between PR stages | Accepted explicit stop/fresh-branch repair. |
| Add test-creation dependencies | Accepted dependency repair. |
| Clarify original line-reference frame | Accepted clarity repair. |
| Run repository self-check in every mode | Accepted; omitted from bad closure summary. Before-fetch contradiction is separate. |
| Verify concurrency support | Accepted; later note is not another defect. |

Primary support: first report and second `prior_fix_check` under the review roots above; historical v2 is the successful content in planning log 544/545. Acceptance here means accepted plan amendment, not executed functionality.

### Oracle: all four original findings

| Finding | Mechanism/classification | Primary support | Opposition/limit; strength |
|---|---|---|---|
| Unverified guard/producer selects rejection | Original valid oracle defect; separate executable predicates omit verification flags before later unproven-evidence row | Builder 65 → corrections 189 onward; full review 1; review 2 confirms fix | Table text was correct, but did not control separate predicates. Strong. |
| Provenance family changes wrong causal factor | Original semantic coverage defect: policy flag varies instead of known/unknown author | Builder 58; original requirement; author/schema contrast added 191-196 | Correct labels/count/one-field difference do not establish required meaning. Strong. |
| Missing-abstraction case remains import-cycle claim | Original semantic omission | Builder 58; requirement distinguishes cases; 206-211 correct consequence and add contrast | Added contrast was required, not extra scope. Strong. |
| Default-path security fixture has false default | Known original defect intentionally retained by repair boundary | Builder 52; preserved fixture 563-628; parent 383/450; one-field change 573 | Original specification not inherently contradictory. No new predicate created the retained fact. Strong. |

Test counts were 67/78 before first review, 74/85 after permitted repair and 74/85 after authorized correction. They are historical run summaries, not tests executed by this assembly. An existing semantic assertion was strengthened without increasing collected-test count.

### CI: retained, introduced, optional and corrected findings

| Finding | Mechanism/classification | Primary support | Opposition/limit; strength |
|---|---|---|---|
| Tooling exemption misses hashes | Incomplete old repair: status accepts a rewritten tooling file while exact hash comparison rejects it | Original/regenerated plans; regenerated lines 37, 183-184 | Requires a baseline-listed tooling file actually to change. No implementation failure observed. Strong plan contradiction. |
| PR search filters/order unasserted | Preexisting missed acceptance weakness | Original search/checks and regenerated 117/128-129; final merged search item | Creation arguments are tested, search arguments are not. No wrong PR suppressed in an observed run. Bounded. |
| Dependency ancestors lost | Introduced graph defect while relaxing serial chain | Original safe chain, repair advice and regenerated dependency lines | Sequential execution still protects runtime order. Suggested replacement chain also needed qualification. Strong structural chain. |
| Stub confinement not mechanically verified | Preexisting missing safeguard made clearer by explicit real-Git forwarding | Original temporary-repository instruction; regenerated 129; completed probe | Correct execution is already instructed to use a temporary repository. No real-repository mutation observed in this case. Bounded. |
| Half-edited advisory meaning passes | Preexisting semantic check weakness surviving repair | Original/regenerated keyword predicates; completed probe counterexample | Repair rejects more old bad edits; it did not make a previously sound check worse. Strong counterexample. |
| Rename/copy handling undefined | Incomplete baseline-parsing repair | Second reviewer, measured debate correction, final low item | Reviewer's original old/new path-order advice was wrong and corrected before application. Strong disposition. |
| Research-file immutability not proved | New repair promise checked only by decision-line cardinality | Original required append; regenerated prohibits append but counts one decision line | No append observed; not loss of previously enforced immutability. Strong check mismatch. |
| Job-name substring rejects “not required” | Preexisting overstrict check | Both plans ban bare substring; second reviewer/calibration | Some supporting reviewer claims were wrong or redundant; core false rejection remains. Strong. |
| Decision serialization ambiguous | Residual machine-format weakness | Final merged finding and regenerated consumer | Not observed incorrect execution. Bounded. |
| Angle-bracket check ambiguous | Repair-era acceptance wording ambiguity | Second-reviewer card/calibration; final merged item | Surrounding intent helps; actual permissive executor interpretation unknown. Bounded. |
| Boundary workflow lacks whole-document comparison | Inherited analogous weakness, later optional hardening | Original finding names sync/test only; debate concession | Not an unapplied original two-file repair. Strong narrowed disposition. |
| Directory-wide workflow allowlist | Inherited source/check mismatch; optional tightening | Both plans, exact-file source scope and directory-level source quality rule | No extra workflow edit observed. Medium specification-violation claim withdrawn. Strong disposition. |
| Literal advisory warning requirement | Substantive defect claim rejected | Appended source requires literal word; regenerated check enforces it | Loose edit instruction retains only low wording alignment. Strong rejection. |
| Nonempty render accepts failure output | Preexisting/residual acceptance weakness | Final item observes identical failure message could satisfy check | No actual failed render execution in this plan case. Bounded. |
| Status flags inconsistent | Residual scope-check weakness | Final merged item | Actual untracked-directory mismatch not observed. Bounded. |
| Leftover line-number frame unstated | Residual evidence/reference ambiguity | Final merged item | Historical/base line references are not current defect locations. Bounded. |
| Coverage matrix omissions/wrong mappings | Review-artifact defects, not missing implementation tasks | Second-reviewer entry and calibration corrections | Exact introduction of each row and earlier miss cause unknown. Do not add as another plan defect. Bounded. |
| Proposed renumbering leaves filenames/hash timing/direct-baseline conflicts | Defective unexecuted remediation proposal | Completed probe and final report | Not an applied second refactor or observed overwrite/hash failure. Strong proposal critique only. |

The four retained low findings about serialization, failure-message rendering, status flags and leftover reference frames have individual before/after and historical-validity dispositions in `04-session-43582de1.md`, Additional retained and withdrawn finding dispositions. That section also accounts for the two withdrawn reviewer claims about the path-filter conclusion and README line 30; both follow the revised source and do not increase the 16 retained merged findings. The external documentation premise is not independently certified here.

The original 18 concerns also received substantial plan-text repairs: anchored checks, stub semantics, preserved sync body, README requirements, decision-line conflict, durable post-merge record, failed-search propagation, fresh-change test setup, sync/test preservation, Markdown command repair, branch/identity setup, parent-pair render selection, path-filter artifact location, accepted leftovers and input definitions. Baseline/tooling and dependency repairs retain the qualifications above. The full 18-row accounting remains in case 04, not replaced by a blanket “regeneration failed.”

### Orca monitor: findings across review rounds

| Finding family | Mechanism/classification | Primary support | Opposition/limit; strength |
|---|---|---|---|
| Older-pin and equal-tag range wrong | Both preexisting, with different discovery histories: older pins observed as nonblocking at 697, unrepaired, then treated as a defect at 804; equal tags newly demonstrated at 804 | Original monitor 585; first review 697; second 804; repair 825 | The broad later “no check noticed” statement is contradicted for older pins by the first review. Neither component is repair-introduced. Strong. |
| Failed PR listing swallowed | Retained original error-propagation family | Original 585 loop substitution; later 804; repair 827 | First fixes held elsewhere. Strong. |
| Missing detect patch summary | Preexisting missed inside-script failure boundary | Original 585; review 906; repair 939 | Later checkout failure is outside this boundary. Strong. |
| Blank notes/compatibility implication | Preexisting whitespace-versus-empty mismatch | Original extraction/renderer; 906; 970/976 | Exact earlier reviewer miss cause unknown. Strong behavior trace. |
| Missing upper tag | Preexisting, surviving narrower range repair | Original walk; 825 handles equal/reversed only; 906/949 | Earlier range repair successful for its cases, not comprehensive. Strong. |
| Carriage-return quote escape | Preexisting formatter limitation | Original quote function/sanitizer; 906; later handling outside byte-exact sanitizer | Initially reasoned, not rendered on GitHub. Bounded. |
| Unused helper/reversed rollback message | Preexisting extra/output defect | Original 585; 906; 945 | Not fix-introduced. Strong text history. |
| Incomplete rerun log | Repair-era evidence gap | Review 906; reviewer independently reruns checks | Missing logged output does not prove checks were never run. Bounded. |
| Early pin gate/token/checkout summary absent | Preexisting missed earlier-step boundary | Original main-step trap; 1021; later always-run summary | Inside-script trap cannot cover preceding steps. Strong. |
| Collector JSON exceeds argument limit | Preexisting reproduced transport defect | Original command arguments; 1021 89-tag fixture; 1060/1062/1064 file transport | Threshold depends on note sizes, not a universal 70/89-tag limit. Strong local reproduction. |
| Electron field lacks its own callout | Preexisting field-specific omission | Original renderer; 1021; field contract | Callout elsewhere does not satisfy requested field location. Strong. |
| Rename overlap misses patched paths | Preexisting exactness gap in suggested command | Original diff command; 1021; 1066 | Source suggested the weaker command itself. Strong source/implementation tension. |
| Detect checkout summary absent | Preexisting missed before-script boundary | Original job; 1143; fallback 1200 | Timeout-specific claim not proved on runner. Strong checkout claim, bounded timeout claim. |
| Provenance hash fields unchecked | Preexisting/incomplete hardening | Original 585 fields; 1143; successful 1188 onward | Initial hook-rejected edits are not applied repairs. Strong. |
| Capitalized security term missed | Preexisting, stronger interpretation | Original lowercase matcher; 1143 | Written pattern does not unambiguously require case-insensitive match. Useful hardening, not certain original violation. Bounded. |
| Security output unbounded | Preexisting design gap exposed after transport repair | Original renderer; 1143 reproduction, 119,057 characters; cap 1196 | Reviewer explicitly says no field-10 cap in plan. Not transport-induced regression. Strong reproduction, bounded original-criterion claim. |
| Very large tag-list argument ceiling | Retained theoretical limit | Review 1143 estimate | Explicitly considered practically unreachable; not weighted like reproduced argument failure. Weak operational evidence. |
| Selected-release failure called outage | Preexisting cross-component defect | Original workflow 585 and helper 171; final 1240 | Earlier helper review passed, but did not cover this integration distinction. Strong. |
| Links-only fallback unbounded | Preexisting retained output-budget gap | Original 585 fallback; 1240 reproduction, 83,415 characters with 420 tags | Field-10 cap did not create this path. Platform limit itself not independently certified here. Strong local reproduction. |
| Error annotation captured as pin value | Proven introduced implementation regression | Successful inherited trap changes 759-762; final 1240 reproduction | Introduced by first repair, discovered much later. Detect's sibling process guard did not protect pin. Strong. |
| Validators accept newline-suffixed values | Retained/incomplete hardening, mixed history | Original hex validator and later similar validators; 1240 rendered provenance path | Shell substitution strips trailing newlines in some other paths; not all cited validators equally reachable. Bounded by demonstrated path. |
| Cosmetics and uncapped additional fields | Preexisting/retained cosmetics or broader design scope | Reviews 906/1021/1143 | Operator later approval does not retroactively make every item an original acceptance failure. Bounded. |

The five reviewing-agent identities and all seven verdicts are mapped in `05-session-e002bed2.md`, Reviewer identity and verdict mapping. The original reviewer `abeae1e32b8eb193b` produced records 697/804/849; `a88a1879f45ea420a`, `a07df47ab3fd3e05e`, `aef3fc4923722198a` and `a023d1421085d4e1e` produced records 906, 1021, 1143 and 1240 respectively. Identity-bearing dispatch results are original records 686, 894, 1010, 1132 and 1229, not event UUIDs.

### Credential finals: evidence errors versus delivery defects

| Finding | Mechanism/classification | Primary support | Opposition/limit; strength |
|---|---|---|---|
| Task 3 cites README separator for lint | Valid historical evidence failure, not delivery defect | Original temporary reviewer proof; parent 332/390; durable correction 411/415 | Lint criterion actually held. Failure valid under then-loaded evidence rule. Strong. |
| Task 6 softens literal lint criterion | Unauthorized criterion relaxation before FINAL | Parent 1215/1230; nested task reviewer acknowledges literal gap; first FINAL | Existing lint findings were preexisting, but literal requirement still unmet until acceptance. Strong. |
| Task 8 citation shifts one line | Genuine later-task movement under old rubric | Task 15 header insertion; first FINAL | Current moved-line-alone policy differs. Not universal evidence failure. Strong historical classification. |
| Task 7 points at wrong section | Original evidence-selection error | Ledger points to refresh description, not required table; first FINAL | Delivery not shown changed. Strong. |
| Task 17 cites incomplete proof | Narrower pointer than claim | First FINAL and preserved evidence | Not necessarily absent underlying work. Strong pointer limitation. |
| Task 10 points to blank line | Preexisting evidence defect missed by first FINAL | Created at parent 1425; log line 10 blank; nested second FINAL 116 | Exact reason earlier audit missed it unknown. No repair-induced delivery defect. Strong. |
| First Task 7 repair misses last row | Incomplete evidence repair | Corrected range ends 56, final row is 57 | Small evidence-range defect, not code regression. Strong. |
| Task 10 repair exceeds named authorization | Observed authority-boundary issue | Acceptance names Tasks 7/8/17; parent 2028 acknowledges overreach | No new authorization observed in intervening sequence. Strong bounded historical finding. |
| Second FINAL absent from ledger | Historical bookkeeping omission | Nested failure and parent corroboration versus archived ledger | Do not silently insert into historical source. Strong. |
| Third FINAL pass follows different rubric | Actual policy change, confounded with fixes | Consecutive nested Read results; captured historical-rule JSON | Updater and separate effect on verdict unknown. Strong change evidence. |
| Narrow manpage task-body omission remains | Preexisting instruction omission, not failed-round cause | Historical tree checked by case analyst | Fan-out described elsewhere; observed PASS is not universal literal compliance. Strong narrowed finding. |

The complete eight-observation accounting is in `06-session-0690ee9f.md`, Complete third-final eight-observation disposition, sourced to nested third-FINAL record 155 and its preserved reads. It also retains observation 4 (accurate but loose overwrite wording), observation 7 (human acceptance exists in an artifact but no required ruling ledger line), and observation 8 (retained restart remark classified accurate by the historical sweep). These are not automatically three additional delivery defects.

**Key Takeaways**

- New discovery is repeatedly distinguishable from new introduction.
- Accepted original repairs remain visible alongside their limitations.
- Review-advice errors and unsupported attributions are part of the evidence, not silently promoted into product defects.

---

## Why Earlier Reviews Missed Later Findings

The cases establish some observable coverage mechanisms. They do not establish general psychological explanations.

| Observable miss mechanism | Concrete support | Opposition, unknowns and strength |
|---|---|---|
| Text coverage credited without required state wiring | Orca first coverage matrix credits the up-to-date patch-check requirement despite original tasks not naming the required state; case 01, coverage-matrix analysis | Direct over-credit for this requirement, not proof every row is wrong. Strong narrow evidence. |
| Temporal requirement reduced to validation presence | Original Orca matrix covers validation but omits complete before-use/before-upstream-call clauses; actual fetch precedes decision validation | Requirement timing, not absence of every validation check. Strong. |
| Source test table weaker than behavioral contract | Orca source test list uses no-op wording and omits individual digest mismatch; first self-audit checks listed tests | Following the list does not prove full behavioral coverage. Strong source mismatch. |
| Labels/cardinality checked instead of required meaning | Oracle counts, one-field contrasts and retention labels pass despite wrong author contrast, wrong consequence and false default-path property | Tests are genuine; assertions prove less than completeness claim. Strong. |
| Executable name/exit status treated as renderer availability | Documentation check discards notice output and records nominal zero status | No malformed page shown; actual environment lacks renderer. Strong. |
| Wrong initial state corrupts change attribution | Task 2 reconstructs baseline from HEAD after dirty-file edits; earlier truthful tree contains disputed hunks | Historical reviewer accepted explanation on trust; case later independently corroborates it. Strong. |
| Remedy targets one operation, not sibling operation | CI creation head/base arguments asserted, search head/base arguments remain unasserted | Explains narrow repair coverage, not why original reviewer failed to inspect search. Strong remedy trace; cognitive cause unknown. |
| One of two independent checks repaired | CI status tooling exemption changes while hash comparison remains exact | No implementation run; concrete conditional check inconsistency. Strong plan evidence. |
| Path-specific error handling leaves other execution boundaries | Monitor inside-script trap, preceding token/gate steps and checkout each require different handling | Shows incomplete coverage family, not why each reviewer overlooked every path. Strong. |
| Later limit masked by earlier failure | Argument transport previously fails before reaching unbounded renderer/fallback | Removing transport limit reveals, rather than creates, later old gaps. Strong traced sequence. |
| Temporary proof lost during ledger handoff | Initial credential task reviewer runs real lint comparison; executor records unrelated README line | Delivery criterion held; durable evidence conversion failed. Strong. |
| Criterion knowingly softened | Credential task reviewer accepts no-new-findings despite literal changed-line rule | Not a lack of available lint information. Strong. |
| Later defect did not yet exist | Orca source substitution/order/remote and monitor trap are created by repair | No initial-review miss needs explaining for absent text. Strong before/after evidence. |
| Earlier miss remains unobservable | Monitor whitespace/formatting examples; credential Task 10 blank pointer; some planning test gaps | “Context exhaustion,” “model weakness,” “inattention” and incentives are not established. Unknown. |

**Key Takeaways**

- The strongest explanations name the exact property checked and the stronger property required.
- Root-cause evidence about code behavior does not automatically explain reviewer cognition.
- Unknown miss reasons stay unknown.

---

## Unsupported Findings and Reviewer Disagreements

| Claim or interpretation | Adjudicated status | Evidence and consequence |
|---|---|---|
| Twenty Orca second-round items are twenty fresh defects | Unsupported aggregation | Duplicate sufficiency item and explicit concurrency non-defect remain in the numbered inventory. |
| Orca second review proves 13 fixed, three partial | Incorrect summary | Detailed checklist supports 14 accepted amendments, two partial; repository self-check was omitted from summary. |
| Pin-equals-current no-op is forbidden | Withdrawn subclaim | Governing source permits it. Separate early four-asset divergence remains valid. |
| Concurrency key must be removed | Withdrawn/non-defect after calibration | Historical merge accepts support and pairing with non-cancellation. No new external syntax claim made here. |
| Every absent mutation is a functional defect | Not established | Existing bad-input fixture may already detect guard removal. Requires concrete uncovered behavior. |
| Missing dependency prose proves unguarded jobs | Not established | Existing job dependency syntax is real wiring evidence. |
| Task 2 performed unrelated header/key-fanout work | False task attribution | Incorrect supplied baseline, independently contradicted by earlier truthful tree. |
| Task 6 rendering unverified means malformed page | Not established | No actual renderer ran. |
| Oracle second reviewer invented default-path condition | False | Original requirement explicitly names a default-path Critical security sink. |
| CI boundary-file comparison was an unapplied original repair | Overclaimed, later conceded | Original whole-document concern names sync/test only; boundary extension becomes optional hardening. |
| CI directory-wide allowance is an unambiguous new medium violation | Overclaimed, later downgraded | Directory-level rule appears in source quality criteria; no extra edit observed. |
| Reviewer's original rename path order is safe advice | Incorrect advice, corrected in debate | Measured record order contradicts original card; corrected before any observed implementation. |
| CI literal advisory-word check is a defect | Substantive claim rejected | Appended source explicitly requires the literal word; only instruction wording alignment remains. |
| CI matrix corrections are missing implementation work | Wrong category | Review bookkeeping errors, not additional task defects. |
| File-backed monitor JSON caused oversized output | Unsupported causation | Unbounded security/fallback existed before transport change. |
| Every monitor late finding violates original AC | Unsupported scope claim | Some cap/matching demands were broader design/hardening matters. |
| Monitor did not run checks because output log is incomplete | Not established | Reviewer rerun passed; incomplete evidence is not fabricated execution proof. |
| Latest credential PASS proves unchanged-rubric convergence | False experimental interpretation | Both evidence and loaded policy change. |
| Ledger verdict count captures every review | False | Missing credential second FINAL and monitor original/intermediate results require transcript recovery. |
| `head-moved` proves HEAD actually moved | Unsupported inference | Missing task-start checkpoint maps to that category in documented guard behavior. |

Reviewer disagreement is not automatically reviewer error. The distinctions above separate source-disproved claims, withdrawn subclaims, stronger useful preferences, valid original failures and unknown causal conclusions.

**Key Takeaways**

- Historical severity and validity need adjudication, not automatic acceptance.
- A corrected review claim is evidence of the review process working, not another implementation regression.
- Optional or speculative concerns cannot inflate confirmed-defect counts.

---

## Counterexamples and Evidence Against Overbroad Explanations

| Control | Observed evidence | What it challenges | Limit |
|---|---|---|---|
| Oracle repairs 1-3 | Second reviewer confirms all three corrected | “Every repair fails” | Frozen fourth finding remains deliberately open. |
| Monitor Tasks 10/11 | `extra`/`missing`, one repair, `compliant` | “Same executor/reviewer arrangement cannot converge” | Accepted helper still misses later integration case. |
| Initial credential final gate | One durable-evidence repair, then pass/archive | “Final evidence loops always repeat” | Old rubric validly required durable proof. |
| Session 10 Task 4 | Missing comment corrected, compliant re-review | “Any failed task review predicts repeated failure” | Original implementation package absent from searched locations; logs/Edit survive. |
| Session 17 Task 8 | Real deviation corrected, passing re-review | “Retry-feature implementation itself was an endless operational ladder” | Later PR reviews are separate development work. |
| Session 17 FINAL | Real restore-basename bug plus evidence defects corrected, then pass | “Every FINAL issue is cosmetic” | Not strict fail-fix-fail. |
| Session 09 | Seven compliant tasks; FINAL never ran | “A predicted failure is an observed failure” | Overlapping writers are a real operational blocker. |
| Session 19 | Nine compliant task reviews | “Later shared-ledger blocks happened in every session using the package” | Later Task 12 belongs to another session. |
| Sessions 13/14 | Authorized plan corrections without semantic re-review | “Every corrected plan has a second failed review” | Unreviewed correction is not clean approval either. |
| Oracle valid pre-freeze design | Required example could have been authored correctly before freeze | “Original requirement was intrinsically impossible” | Later permitted repair excluded changing frozen chosen record. |
| Monitor output limits | Later old defects become reachable after earlier repair | “Later means introduced by immediately preceding fix” | Several output bounds need a separate design decision. |
| Credential final pass | Accepted gap and narrow instruction omission remain | “Observed PASS certifies every literal task instruction” | Pass remains a real observed process outcome. |

Primary controls are preserved in the six case reports, `scope-02.md`, `scope-03.md`, `scope-04.md` and the complete screening captures.

These sessions cluster in few work families and are selected by file modification, not randomized. No controlled old/new protocol comparison establishes fleet-wide regression rate, model capability loss, context exhaustion or insufficient reviewer count.

**Key Takeaways**

- Successful repairs are real counterevidence and must remain in the deck.
- Final review can catch a genuine delivery defect, not only citation problems.
- Integration review can find old defects after apparently successful component review.

---

## Current Versus Historical Rule Map

### Current protocol sources

The dedicated rule-map report compared seven source/installed pairs and reported matching bytes at its inspection. Its conclusions are about executable agent instructions, not proof that every described control was mechanically enforced.

| Rule surface | Current source and installed counterpart | Rule-map finding | Historical boundary |
|---|---|---|---|
| Workflow generation and reflection | `/config/workspace/IronClaude/src/superclaude/skills/sc-workflow-protocol/SKILL.md`; `/config/.claude/skills/sc-workflow-protocol/SKILL.md` | Generation gate and advisory reflection are separate; reflection must not automatically edit/regenerate the plan | User-authorized later plan revision is a separate action. Current text alone does not prove historical loaded bytes. |
| Generation checks | Source/installed `sc-workflow-protocol/refs/quality-gates.md` | Schema and coverage checks do not constitute executable proof of every semantic property | Historical plans passed generation and still received valid semantic findings. |
| Task review | Source/installed `sc-implement-protocol/refs/qa.md` | Original brief, AC, constraints and diff; evidence citations; closed per-task verdicts | Broader “any defect” review expectations must be checked against historical prompts and original criteria. |
| Retry ladder | Source/installed `sc-implement-protocol/refs/retry.md` | Initial attempt, ordinary repair and bounded changed-approach attempts; checkpoint/revert rules | Not a lifetime cap on every operator-authorized continuation. Monitor Task 12 has no observed ladder/adviser/revert records. |
| Ledger and resume | Source/installed `sc-implement-protocol/refs/ledger.md` | Append-only progress, scoped human acceptance, fresh operator review after terminal state | A complete record may honestly retain a noncompliant verdict. Ledger alone can omit real review events. |
| Managed workspace/FINAL | Source/installed `sc-implement-protocol/refs/managed-workspace.md` | Pinned plan/source, join writers, state digest, fresh current-state FINAL, stop archive on issues | Digest excludes some evidence/task-owned artifacts. Non-cooperating writers unsupported. |
| Implementation loop | Source/installed `sc-implement-protocol/SKILL.md` | Connects execution, QA, ledger and retry behavior | Historical version must come from actual loaded contents, not today's file. |

Source prefix for the implementation counterparts is:

`/config/workspace/IronClaude/src/superclaude/skills/`

Installed prefix is:

`/config/.claude/skills/`

The rule-map research is recorded in:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md`

Its `[CODE-VERIFIED]` labels mean the analyst inspected the instruction source. This assembly does not independently certify archive helper implementation, detector coverage or historical compliance with today's instructions.

### Observed historical policy changes

| Historical change | Primary captured evidence | Effect and uncertainty |
|---|---|---|
| Monitor one-fix protocol to migration/fresh-review behavior | Monitor log initial rules 42/58; later ledger/rules 874/884; fresh dispatch 893; explanation 902 | Reopens completion after `compliant` 849. Real continuation mechanism, not proof protocol caused old code defects. |
| Credential FINAL old evidence rule | Nested `agent-acf0a51e6992c50ee.jsonl` record 18, `2026-10-22T20:26:30.085Z` | Missing, stale or unverifiable evidence is issues. |
| Credential FINAL revised rule | Nested `agent-a4bfff371c63a6c39.jsonl` record 18, `2026-10-22T20:32:19.277Z` | Moved line number alone is not issues; current evidence and scoped acceptance govern. Acceptance-recording rules also change. |
| Checkpoint absent maps to moved category | Documentation 485-486; monitor Task 13 continuation and historical rule read | Explains recorded guard category without proving actual HEAD movement. |

The historical credential reads are preserved in:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/historical-review-rules.json`

Captured loaded-content hashes are:

- Before: `0b533765d43a7adc90987581892a0bca849cc19a53638b556b6aba62d425d083`
- After: `faff03b7b94ca2b70f9b25c35dcefd52636b7df8f7bf9a110c0a956a78d2e7d5`

The updater is unknown. The credential pass follows both fixes and the revised policy; their separate effects are unknown.

### Protocol weakness versus observed execution violation

| Observation | Proper classification |
|---|---|
| Current ladder has bounded planned attempts but operator resumes can trigger later fresh reviews | Current protocol design boundary, not evidence that monitor exhausted or reset that ladder. |
| Criterion softened without user acceptance | Observed historical execution/authority problem in credential task QA. |
| Plan/source become pinned | Current rule relevant to frozen-task repair authority; historical exact restrictions still require captured evidence. |
| Missing checkpoint halts escalation | Observed guard outcome and snapshot omission, not actual moved HEAD. |
| Changed FINAL policy | Actual historical input change, not inferred from current source differences alone. |
| No stable finding-resolution registry binding future reviewers | Rule-map limitation, not proof that all repeated findings are invalid or all new reviews should be suppressed. |

**Key Takeaways**

- Current rules explain intended behavior; historical loaded bytes establish what an old reviewer actually received.
- The longest selected monitor loop did not demonstrate repeated execution of the current adviser/revert ladder.
- Scope, authority, review policy and evidence state can change independently of delivery code.

---

## Source Inventory and Traceability

### Research components read for this assembly

All package-local entries below resolve under:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/`

| Component | Role and retained status |
|---|---|
| `evidence-deck.md` | Existing skeleton and useful populated analysis/correction blocks used as assembly input. |
| `01-session-ac2cd1fd.md` | Complete Orca planning analysis, original-repair accounting and appended primary-identifier supplement. |
| `02-session-a9b88895.md` | Complete oracle analysis, full review/fixture references and identifier join to preserved capture. |
| `03-session-6f744b87.md` | Complete rendering/baseline analysis and appended identifiers. |
| `04-session-43582de1.md` | Complete bounded CI analysis, separately timed completed outcome, complete reviewer dispositions and identifiers. |
| `05-session-e002bed2.md` | Complete monitor analysis, fixed original prefix, separately timed acceptance continuation and identifiers. |
| `06-session-0690ee9f.md` | Complete credential analysis, historical-rule comparison, earlier-miss limitation and identifiers. |
| `scope-01.md` | Completed screening summary for indexes 01-06. |
| `scope-02.md` | Completed screening summary for indexes 07-12 and controls. |
| `scope-03.md` | Completed screening summary for indexes 13-18; corrected raw anchors retained in capture. |
| `scope-04.md` | Completed screening summary for indexes 19-24. Earlier screening count/tool labels are superseded by dedicated case corrections. |
| `scope-05.md` | Completed screening summary for indexes 25-30; resumed provenance checking and full-case handoff now recorded. |
| `scope-rules.md` | Current protocol map, two recovered historical QA loads with hashes and case links, and explicit historical-version limits. |
| `session-manifest.txt` | Immutable membership list and population-selection time. |
| `screening-handoffs-source.txt` | Complete preserved screening handoffs, source fingerprints, timestamps and UUIDs. Raw evidence, not a newly authored gate report. |
| `screening-recovery-source.txt` | Original authored edits and complete recovered screening handoffs, including corrected physical line counting. |
| `scope-01-recovered.md` | Original recovered unfinished report; historical placeholders intentionally preserved there, not copied into completed deck. |
| `scope-03-recovered.md` | Original recovered screening report; later physical-line corrections apply. |
| `deep-handoffs-first-source.txt` | Original deep-analysis returns. Subsequent dedicated case corrections/supplements qualify earlier statements. |
| `deep-handoffs-remaining-source.txt` | Original CI/monitor/credential returns, preserving original observation endpoints. |
| `historical-review-rules.json` | Captured historical tool-result content from consecutive FINAL reviewers, not current global-rule contents. |
| `research-notes.md` | Completed discovery scope, assignment map and planned outputs; planned later artifacts are not completion evidence. |

The governing skill and exact Step 2.13 in the task file were also read. No external lookup, historical plan execution, production edit, Git mutation, deletion, archive or publication was performed for this assembly.

### Preserved primary identifier joins

The appended case supplements retain original physical JSONL records, timestamps and message UUIDs. Phase 2 formatting corrections can shift research-file lines; the stable supplement headings and original source-record frames remain the citation join.

| Case | Identifier supplement | Example original identity |
|---|---|---|
| Orca planning | `01-session-ac2cd1fd.md`, Resume traceability supplement | Record 544, `2026-10-22T15:08:38.839Z`, UUID `1ba7509f-fbb1-401f-bba7-c20d545ef750`. |
| Oracle | `02-session-a9b88895.md`, Resume traceability supplement; `screening-handoffs-source.txt`, positive-case identifiers | Record 450, `2026-10-21T22:03:12.606Z`, UUID `1b13c84b-c798-496a-b980-563962c49e1c`. |
| Documentation | `03-session-6f744b87.md`, Resume traceability supplement | Record 450, `2026-10-22T21:20:22.606Z`, UUID `508ec6fa-75e9-49c8-b95b-4adcb3781edb`. |
| CI planning | `04-session-43582de1.md`, Resume traceability supplement | Record 1084, `2026-10-23T03:48:11.615Z`, UUID `5cc58a86-a38d-4679-8383-7f69a5e8cdfb`. |
| Monitor | `05-session-e002bed2.md`, Resume traceability supplement | Record 1240, `2026-10-23T03:31:41.631Z`, UUID `66e024b2-e8f4-4715-a1b0-180a65521a8b`. |
| Credential finals | `06-session-0690ee9f.md`, Resume traceability supplement | Nested second FINAL record 116, `2026-10-22T20:31:27.048Z`, UUID `375a0903-0c0d-4bd0-94d6-0b1faac37cb4`. |

These joins are evidence locators, not additional events or fresh causal investigations.

### Immutable capture and observation boundaries

| Source | Boundary preserved |
|---|---|
| Manifest | Membership chosen at `2026-10-23T03:25:59Z`; no byte freeze implied. |
| Orca planning | Historical four versions reconstructed from actual successful writes/edits; final v4 explicitly unreviewed. |
| CI initial analysis | Inspection `03:41:52.643460Z`, 1,000 rows, probe still running. |
| CI supplement | Inspection `04:02:04.400203Z`, 1,086 rows; second review complete as partial/not-ready. |
| Monitor original analysis | Prefix 1-1247 ends `03:31:57.433Z`, blocked after seventh verdict. |
| Monitor supplement | Inspection `04:03:52.359004Z`, 1,437 rows; Task 12 acceptance closure and separate Task 13 continuation. |
| Recovered screening | Original embedded Unicode splitting errors retained and corrected by physical-newline anchors in recovery capture. |
| Historical rules | Exact old/new loaded contents, not reconstructed from today's installed file. |

Earlier raw captures are not rewritten to hide later knowledge. Later case supplements qualify original endpoints explicitly.

**Key Takeaways**

- Every required component and additional relevant research file is inventoried.
- Primary identifiers survive through stable supplements rather than repeated case investigation.
- Original captures and intermediate reports remain historical evidence even where later corrections supersede their summaries.

---

## Key Takeaways

- There is no single uniform failure loop. The sample contains repair-introduced defects, progressive discovery of old defects, intentionally retained blockers, changed review policy, incomplete evidence repairs and incorrect change attribution.
- Passing structure or tests repeatedly proves less than the behavioral criterion. The gaps are concrete: ordering, integration, fixture semantics, argument checks, execution boundaries and durable evidence.
- Some repair proposals cross dependencies or data flows and introduce real faults. Other repairs work but leave a frozen or environmental blocker unchanged.
- The longest monitor chain includes one actual implementation regression, many preexisting defects and a protocol-mandated reopening. It is not evidence of an unbounded automatic adviser/revert ladder.
- Repeated evidence-only FINAL failures occur with unchanged delivery digests. Those digests do not establish unchanged evidence artifacts or review policy.
- Review claims themselves require validation. Duplicates, optional hardening, withdrawn subclaims and false baseline attribution cannot be counted as fresh confirmed defects.
- Human acceptance is a real stopping mechanism. It preserves an unmet verdict honestly; it does not prove repaired behavior.
- The sample supports case-specific mechanisms. It does not establish a fleet-wide rate or a general explanation based on model capability, context exhaustion or reviewer count.

---

## Gaps and Questions

| Question or limitation | Impact | Evidence-constrained next check |
|---|---|---|
| Why did particular earlier reviewers miss valid old defects? | Limits claims about reviewer cognition | Use existing coverage/probe traces where available. Otherwise retain unknown; later discovery alone does not resolve it. |
| Who changed the installed credential FINAL rubric? | Cannot attribute policy update to an actor | Existing captured reads prove change, not authorship. Additional attribution would require separate historical evidence. |
| Would credential evidence repair pass under the unchanged old rubric? | Prevents isolating policy effect | No controlled same-input/same-rubric comparison was observed. Do not invent one. |
| What is the final semantic quality of Orca plan v4? | Unreviewed endpoint | No independent post-v4 review is in this incident. Structural pass is insufficient. |
| Did CI hash/search/confinement weaknesses fail in execution? | Plan risk is not observed product failure | No implementation run was observed within the declared windows. |
| Did actual runner cancellation/timeout/permissions behave as predicted? | Local review does not prove platform execution | Not established by these reproductions; no workflow run authorized here. |
| Do manual pages render without warnings? | Accepted criterion remains unverified | No real renderer result in the observed evidence. |
| Were accepted monitor defects subsequently repaired? | Acceptance is not repair proof | The inspected continuation accepts them; no eighth Task 12 review establishes repair. |
| Are output-size thresholds general limits? | Prevents misleading fixed tag counts | Fixture contents determine sizes; the source's quoted platform body limit was itself unverified. |
| Does the final oracle prove model effectiveness? | Deterministic validation is not live behavior | No live-model effectiveness claim supported. |
| Is historical oracle full-file state independently byte-compared? | Limits scope of authorized-review validation | Fixture comparison is strong; historical reviewer lacked a separately preserved full earlier oracle snapshot. |
| Are excluded sessions universally free of nested target activity? | Bounds negative claims | Screening covers actual top-level invocations and selected linked reviewers, not every arbitrary nested log. |
| Is every durable pointer semantically sound once nonblank? | Mechanical existence checks are weaker than meaning | A nonblank target can still fail to support the associated criterion. |
| Is today's helper enforcement independently certified? | Current protocol text is not implementation proof | Rule-map analyst did not inspect/run every helper. This assembly makes no detector claim. |
| Are live source bytes unchanged since each case observation? | Historical reproducibility boundary | Use declared fingerprints/prefixes; membership freeze alone is not a content snapshot. |

No missing history is filled with a generic explanation or fabricated event. Proposed checks above are not executed remediation or authorization to run investigated plans.

---

## Stale Documentation Found

The following historical evidence problems are established:

- Moved or wrong ledger citations, including a genuinely shifted startup line and citations wrong at creation.
- A blank cited lint-log line.
- Temporary proof not preserved in the durable handoff.
- Internally inconsistent review closure summaries.
- Condensed findings that omit details retained in original returned reviews.
- Ledger omission of a real second failed FINAL.
- Shared live ledgers containing events later than a selected session's endpoint.
- Original screening summaries whose pending or provisional observations were later resolved in separately timed case supplements.
- Different loaded review rules from the same installed path during one incident.

These are not a blanket claim that current production documentation remains defective. Current source/installed agreement at inspection cannot establish historical executed bytes. Intentionally historical line references and preserved raw recovery placeholders are not silently converted into current defect inventories.

---

<!-- phase3-correction: consolidated-accounting -->
## Research-gate correction accounting

This section retains the substantive corrections already present in the earlier deck. It does not certify a research gate, verification cycle or later task phase.

- **Orca planning:** All 16 original repairs have individual traces, including successful non-recurring fixes. Detailed closure is 14 accepted plan amendments and two partial, not 13/three and not runtime verification. Record 150 was blocked by 151; retry 163 succeeded at 164. V2 was a whole-file Write.
- **CI planning:** All eight second-reviewer entries have dispositions, including corrected advice, rejected subclaims, optional hardening and matrix-only corrections. They overlap the final merged findings and are not eight added defects. The completed second review is observed later as partial evidence status and `not_ready`, five medium and 11 low items.
- **Monitor:** Membership freeze is not content freeze. Original prefix 1-1247 ends at `03:31:57.433Z`; its retrospectively computed fingerprint is not an original-time snapshot. Later completion accepts known defects with the same `misunderstood` verdict. No eighth Task 12 review is created.
- **Credential finals:** The second failed FINAL is preserved from the nested source without rewriting the historical ledger. The blank Task 10 pointer predates the first FINAL; the reason it was missed remains unknown.
- **Earlier misses:** Unexplained reviewer misses remain unknown. A proven implementation mechanism does not establish a cognitive explanation.
- **Screening corrections:** Dedicated cases supersede earlier provisional counts, tool labels and pending endpoints without altering immutable source captures.
- **Workflow status:** This deck assembly does not infer completion of the overall task from recovered debate artifacts, existing report files or narrative claims. Gate reconciliation belongs to the task's independent process.

---

## Summary

The fixed 30-file membership yielded six selected primary substantive repeated-review cases, with separate successful-repair and operational controls. Three primary cases meet the stricter operational repair-then-another-unsuccessful-review definition; the manual-page case repeats an unchanged verification blocker, and two planning cases retain their actual partial/not-ready statuses. The cases establish a mixture of incomplete fixes, old defects discovered later, real fix-induced changes, frozen authority limits, evidence-handling errors and changed review policy.

The CI second review is observed complete as `not_ready` with partial evidence status. Orca monitor Task 12 later completes through explicit human acceptance while retaining `misunderstood`. Credential FINAL passes after both evidence repairs and a changed rubric. None of those outcomes is proof of universal implementation correctness.

The deck preserves all 30 dispositions, primary incident boundaries, per-case chronologies, finding-level classifications, opposing evidence, successful controls, historical/current rule distinctions and original observation limits. It does not claim that later quality gates, final report validation or the overall research task have completed.

| Status | Result |
|---|---|
| DONE | Assembled the evidence deck text from every required component and discovered research capture, preserving correction history and uncertainty. |
| NEXT | Persist this exact returned deck at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md`; task-state changes and independent gate decisions remain with the parent process. |


## Parent Persistence Record (2026-10-23)

The main session persisted the complete exact assembler return above directly from `dfade920-dc5e-4a04-9498-211d9f08715d/subagents/agent-afinish-evidence-deck-2cbc1383095354aa.jsonl`, without an inline body dump. Before this provenance addition, the decoded final text matched the 889-line persisted body exactly, all 30 inventory rows were checked in order, and no unresolved placeholder was found. The producer's closing NEXT row records its original text-only handoff, not an outstanding persistence action. Assembly is complete; independent Phase 2 and later research gates are not yet passed.
