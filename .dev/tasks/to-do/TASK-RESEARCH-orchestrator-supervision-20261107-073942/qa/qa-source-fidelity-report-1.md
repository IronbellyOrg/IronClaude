## Source-Document Fidelity Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**QA phase:** source-fidelity (fix authorization: false)
**Source files checked:** 3 (`src/superclaude/core/WORKER-CONTRACT.md` 203 lines, `src/superclaude/core/HOW-WE-WORK.md` 405 lines, `tests/skills/test_worker_contract.py` 2265 lines; total 2873 lines)
**Date:** 2026-11-07

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|------|-------------|----------------|---------|----------|
| 1 | Missing / Distorted | `WORKER-CONTRACT.md:52-55` (WC-3, `ask the coordinator` path) | 2.2 precedence list (report :111-117), classification diagram (:364-379), step 1.3 (:1215) | Rule 1 maps every `worker_status: blocked` contract to "waiting on a person (a)", first match wins, before any Orca liveness check. WC-3 :54 says that under `On a blocked gate: ask the coordinator` the command writes the blocked contract, the worker then asks the **coordinator** (not the person) through Orca `ask`, waits, and re-invokes the command in the same session with the same report directory; "the second run's contract replaces the blocked one whole". So a blocked contract on disk can belong to a live worker that is waiting on the coordinator or already re-running. The report never mentions the `ask the coordinator` policy (report grep for "ask the coordinator" and "re-invo": 0 hits), although `research/06-orca-open-questions.md:30` recorded it. Its only WC-3 reading is "no heartbeat while blocked in `ask`" (:57). Result: the classifier as specified labels a live, re-running worker "waiting on a person". Fix: carry WC-3 :54-55 into Section 2.1 and add a rule-1 condition (for example: rule 1 applies only when the Orca row is settled or the brief policy is `report blocked`; a live row with a blocked contract under `ask the coordinator` gets could not determine or working with a note), plus a fixture in step 1.8. | IMPORTANT |
| 2 | Missing (detail dropped) | `WORKER-CONTRACT.md:125` ("Reading a result", `partial`) | 2.1 table row "Reading a result" (:63), 2.2 rule 6 (:117), diagram rule 6 (:372-374) | Contract :125: for `partial`, dependents do not start until the coordinator has read the contract's `report_path` (the deliverable, not only the contract) and recorded whether the partial deliverable is usable; an unusable one is handled like `failed`, which then feeds the :126 tell-the-person path. The report reduces the "Reading a result" block to "A settled row is 'finished' only after the return contract is read" (:63) and classifies `partial` as plain finished. `research/research-notes.md:200` kept the caveat ("Partial still needs its `report_path` read before a dependent may start"); synthesis dropped it (report grep for "usable" and "report_path.*partial": 0 hits). The WC-14 G5 trigger list (step 1.17) therefore also omits the unusable-partial path. Fix: restore the :125 caveat in row :63 and rule 6, and have the sweep mark `partial` rows as not yet judged usable. | IMPORTANT |
| 3 | Inaccurate (internal inconsistency) | `WORKER-CONTRACT.md` (no rule on report location; scope-01 G7) | 4.x WC-14 clause list item 7 (:427) | Clause 7 reads "the report is a dated local file under `.dev/`, never posted", stating `.dev/` as settled. The same report says the location is an open owner decision (:67 G7/GQ-10; :400 "`.dev/` is a working default, still open"), and the step 1.17 draft text (:1235) correctly omits `.dev/`. Fix: drop "under `.dev/`" from clause 7. | MINOR |
| 4 | Missing (meaning not carried) | `WORKER-CONTRACT.md:156` (fan-in rule) | 2.1 table row "Fan-in" (:65) | The row gives fan-in only as "Insertion point for WC-14". The rule's content (admit only `succeeded` or usable `partial`; blocked/failed inputs re-run as new Tasks or dropped with a reason; at most 10 inputs; merge only with at least 2 admitted) is not summarised anywhere. Only the "fewer than 2" case survives, as a G5 trigger in step 1.17. Phase 1 performs no merges, so the impact is low. | MINOR |
| 5 | Inaccurate (citation range) | `WORKER-CONTRACT.md:77-99` | 2.1 prose (:46) | "the brief (:77-97)": "What the coordinator owes each worker" plus "Brief layout" run :77-99 (layout paragraph ends at :99, worktrees heading at :101). True claim, range short by two lines. | MINOR |
| 6 | Inaccurate (overstated pin) | `tests/skills/test_worker_contract.py:125-128` | 4.1 table row "Worker contract" (:314), 2.1 table header (:48) | The report says WC-2..WC-13 and the coordinator section are "pinned by" the test file and marks the WC-10 rows [CODE-VERIFIED against the contract text and the test file]. `RULE_PHRASES["WC-10"]` pins only "at the cadence its preamble sets" and "split into waits of at most 4 minutes"; the sentence the sweep depends on ("treats a missing heartbeat as absence, never as death ... acts only on Orca's stall proofs", contract :45) is not pinned by any test. The contract text itself is correctly cited; only the implied test protection is overstated. | MINOR |

### Claims verified against the source (no defect)

| # | Report claim (report line) | Source check | Result |
|---|---|---|---|
| V1 | Contract is 203 lines; sections Terms :9, Command-side :26, Worker duties :48, Coordinator :64, WC-6 :68, template :166-203 (:46) | `wc -l`; Read of whole file | Correct |
| V2 | WC-2..WC-13 exist, WC-1 unused, no WC-14 today (:46, :1187) | Read: WC-2,3,4,5,6,7,8,9,10,11,12,13 only | Correct; WC-14 is always framed as "add" / draft (no aspirational claim found) |
| V3 | A grep for poll, re-arm, cron, sweep, expire matches only :45 (:67) | Grep -i on the contract: one hit, :45 | Correct |
| V4 | WC-10 at :45: missing heartbeat is absence, act only on Orca stall proofs (:56, :442, :461, :818, :891, :1578) | Read :45 | Correct meaning; the stall-proof narrowing (Orca `exited` or Orca-observed exit only; transcript-only gives could not determine) is faithful to :45 and :74 |
| V5 | WC-3 no heartbeat while blocked in `ask` (:57, :464) | Read :57 | Correct (but see finding 1 for the omitted :54 path) |
| V6 | WC-5 maps `blocked` and `failed` to Orca `failed` (:58, :176) | Read :58 | Correct |
| V7 | WC-12 fenced worker stops without `worker_done` (:59, :463, :1394) | Read :60 | Correct |
| V8 | WC-6 retry is a new Task, never `--retry-of`, never on `unverifiable` (:60, :431, :462) | Read :70, :73, :74 | Correct |
| V9 | WC-8/WC-13 no fan-out (:54, :431, :465) | Read :39, :61 | Correct |
| V10 | Five refusal conditions at :108 gate "worktree removable" (:357, :395, :467) | Read :108: unmerged commits, open PR, uncommitted changes, unfinished implement ledger, unread report | Correct, exactly five |
| V11 | Freeze :133-136 gives "frozen or blocked by policy"; `E-RESUME-NEEDED` not frozen (:64, :391, step 1.8) | Read :133-138 | Correct |
| V12 | G5 triggers at :126, :127, :129, :134, :156 (:512, :1235) | Read each line | Correct; step 1.17 wording matches each case |
| V13 | Guard refusal = no contract plus `guard refused:` body, nothing ran (:117, :374) | Read :127 | Correct |
| V14 | Foreign ready Task reported to the person (:63, rule 4) | Read :129 | Correct |
| V15 | Insertion points after :156 before :158, or after :129 before :131 (:420, :1235) | Read :154-158, :129-131 | Correct |
| V16 | Clause 8: sweep never performs :74 stop/cancel, :107 merge/remove, WC-6 new Task (:428, :1235) | Read :74, :107 | Correct |
| V17 | Report never posted; git ownership :112, :114; WC-11 naming :46 (:400, :466) | Read :46, :112, :114 | Correct; the report rightly limits WC-11 to the naming rule |
| V18 | Never-as-worker list at :23, 8 entries in `NEVER_AS_WORKER` :245-254, phrase at :86-92 (:53, :449, :1237) | Read test :86-92, :245-254 | Correct (7 named plus pr-submit = 8) |
| V19 | Test named "all_seven" checks 8 entries (:72) | Read test :545-546, :398-404 | Correct |
| V20 | `RULE_PHRASES` :25-237, `# Coordinator rules` at :163 (:71, :1237) | Grep: `RULE_PHRASES = {` :25, comment :163, `}` :237 | Correct |
| V21 | `_check_rule` :388-395 requires identifier and first phrase on one line (:71, :1237) | Read :388-395 | Correct; the proposed WC-14 entry satisfies it |
| V22 | Positive test :540-542, negative test :587-594 (:71) | Grep: decorators :540/:587, defs :541/:588 | Correct |
| V23 | Repo-setup gate `_check_repo_setup_gated` at :446; WC-14 must hold no runnable code spans (:430, :1235) | Read :430-462 (`_REPO_CODE_SPAN_RE` matches `make`/`uv`/script spans) | Correct |
| V24 | `AUDIT_ROOTS` :1090-1094 scans skills, commands, agents (:73, :451) | Read :1090-1094 | Correct |
| V25 | 41 test functions (:74, :578) | Grep `^def test_`: 41 hits | Correct |
| V26 | `_check_never_as_worker` :398-404 called at :545-546; `UNATTENDED_COMMANDS` :379 (:1237) | Read :379, :398-404, :545-546 | Correct |
| V27 | HOW-WE-WORK "Other commands" heading :314, markers :318 and :337 (:239, :1099, :1244) | Grep HOW-WE-WORK | Correct |
| V28 | HOW-WE-WORK level table :11-28 copied to `core/CLAUDE.md:65-82` (:79) | Read HOW-WE-WORK :11, :28; grep CLAUDE.md markers :65, :82 | Correct |
| V29 | ASCII-only test :342-347; `_OTHER_COMMANDS` :27-40; excluded set :299-309 (:80, :1244) | Read `test_how_we_work_routing_table.py` | Correct |
| V30 | Optional Orca-coordination bullet after :403 or :405 (:1244) | Read HOW-WE-WORK :396-405 | Correct; the section points to the contract and the never-as-worker list as the report says |
| V31 | Plugin byte copy check at `test_routing_plugin_parity.py:38`; contract installed by `install_core.py:27` (:46, :78) | Read both lines | Correct |

### Summary

- Files checked: 3 (2873 lines), plus the cited lines of `install_core.py`, `test_routing_plugin_parity.py`, `test_claude_md_routing_block.py`, `test_how_we_work_routing_table.py`, `core/CLAUDE.md`, and `research/research-notes.md:186-204`, `research/06-orca-open-questions.md:30` for provenance.
- Claims verified: 31 confirmed correct (V1-V31) plus 6 found defective; 37 report claims checked against cited lines.
- Fidelity issues: 6 (CRITICAL 0, IMPORTANT 2, MINOR 4).
  - IMPORTANT 1: the WC-3 `ask the coordinator` path (:54) is absent, so classifier rule 1 mislabels a live, re-running worker whose transient blocked contract is still on disk.
  - IMPORTANT 2: the `partial` rule of "Reading a result" (:125) was dropped during synthesis although the research kept it.
  - MINOR: `.dev/` stated as settled in WC-14 clause 7; fan-in meaning not summarised; brief range :77-97 should be :77-99; WC-10's absence sentence implied to be test-pinned when it is not.
- Aspirational claims: none. WC-14 is consistently presented as a rule to add, with draft wording and an open ID decision (GQ-11).
- Confidence: Verified: 5/5 checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 6 | Grep: 9 | Glob: 0 | Bash: 7 (no web research).

Verdict: FAIL
