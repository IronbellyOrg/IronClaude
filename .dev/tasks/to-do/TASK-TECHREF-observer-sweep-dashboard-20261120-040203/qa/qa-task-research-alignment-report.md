# QA Report: task-integrity / task-research-alignment

**Task file:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/TASK-TECHREF-observer-sweep-dashboard-20261120-040203.md
**Lens:** task-research-alignment (adversarial)
**Date:** 2026-11-20
**Status:** Complete
**Inputs read:** the task file (Phases 1-7, Open Questions, Task Log), research-notes.md, BUILD-REQUEST.md, scope/01-observe.md, scope/02-sweep.md, scope/03-agent-work-report.md, scope/04-dashboard-design.md.
**Method:** Read every scope file and mapped each key finding, UNVERIFIED item, contradiction, Phase-1 limit and proposed agent assignment to a task item by reading the prompt text and by token counts on the task file. Existence of cited paths and line anchors checked against the snapshot `/home/coder/.cache/ic-snap-20261120/master`, the checkout, and `git ls-tree origin/master` (read-only). Nothing was run and nothing outside this report was written.

---

## 1. Summary of result

No blocking finding. No fabricated path or line anchor. R1-R6, the seven synthesis files, the owner's WHY, the C8 handling and the "do not recommend a unification" constraint all line up with research-notes.md and BUILD-REQUEST.md. The weaknesses are alignment gaps against the scope files: one cross-subject relationship (sweep report layout comes from the #409 package) and one evidence source set (integration-gap closure) are not routed to any agent, and the R6 prompt uses undefined labels. All are cheap to fix in the task file before execution.

| ID | Severity | One line |
|---|---|---|
| F1 | Medium | Sweep report layout and "ten #409 dimensions" derive from the #409 package (scope/04 s4 item 8); not routed to any agent or section |
| F2 | Medium | R6 has no input set to settle integration-gaps items 1-6 "now" (adapter-contract.md, snapshot-export-schema.md, live-test-guide.md, PR #586/#589 live reads) |
| F3 | Medium | R6 and synth-05 use S1-S11, R1-R11, C1-C5 labels defined only in scope/04; prompt names only C1-C3; C4/C5 and rule text not embedded |
| F4 | Medium | The 2026-11-11 reviewer asks (PR/issue links, plain-English summary, session-open link, step flow) are not routed to R6 or to the overlap picture against agent-work-report |
| F5 | Note | synth-01 "overlaps" list omits scope/03 overlaps 4-7 (held work, recommendation posture, cadence/audience, item scope) |
| F6 | Note | Several small UNVERIFIED / stale items from scopes 02 and 03 are not named in any prompt |
| F7 | Note | R4 does not list `output-styles/pragmatic.md` although its topic names the exempt reply |
| F8 | Note | Issue-watcher side of Clay's design (wake.py / hold.py absent) only reached via an `orchestrator_repo` grep |

---

## 2. Checklist results

### 2.1 Checklist item 1: scope findings and open items versus task items

| Scope finding / open item | Where acted on in the task file | Status |
|---|---|---|
| scope/01: R2/R3 gates `QUESTION_GATE_PASSED`/`QUESTION_LINK_PASSED` True, gate records not in snapshot | R1 and R2 prompts (R2 reads gate records with `git show origin/master:`), synth-03 5.2, C8 clause in R1/R2 | Covered |
| scope/01: `check --all --types question` non-acknowledging UNVERIFIED | R1 topic (settle from code/tests or leave UNVERIFIED and say what would settle it); synth-07 UNVERIFIED list | Covered |
| scope/01: snapshot drops resource.*, workspace.*, stage.activity/detail | R1 ("list every field the code drops or adds"), synth-03 5.1 | Covered |
| scope/01: no in-repo consumer of snapshot.json; no agent/command calls observer | R2 topic, synth-03 5.2, synth-06 8.2 | Covered |
| scope/01: docs gaps (cli-groups.md:40-54, README.md:136, no CHANGELOG, post-release-report) | R2 topic and file list, synth-03 5.2 ("what the docs lack") | Covered |
| scope/01: exit codes derived, "UNVERIFIED by running" items | R2 asks an exit-code table cited to code; no instruction to tag the click-default / no-Orca-CLI exit codes as UNVERIFIED because the code may not be run | Weak (Note, see F6) |
| scope/02: stalled (proved) and fenced cannot fire (no producer) | Key Objective 3; R3 mandatory "C8 candidate analysis"; R4; Gate 1 analyst item 8; synth-04 5.3; synth-07 C8 subsection; Gate 3 crossref-chain; Gate 4 agent 1 | Covered (verified in snapshot: only models.py:108-109 defaults; SP24_LINE at report.py:42-45) |
| scope/02: Safe to close / Removable never yes | R3 ("apply the same test"), R4, synth-04, synth-07 | Covered |
| scope/02: ready-Task creator, remote hosts, Orca messages, agentWait non-null, agent_wait_since | R4 C8 clause names the first five; `agent_wait_since` is not named | Covered (minor omission) |
| scope/02: orchestrator-mode.md:27 CODE-CONTRADICTED | research-notes, BUILD-REQUEST, R3 prompt (own verification), synth-07 | Covered |
| scope/02: design section 17 open items, some closed | R4 topic | Covered |
| scope/02: WC-16 vs coordinator's own liveness sweep, WC-10, never-as-worker, HOW-WE-WORK rows, exempt reply, cadence | R4 topic, synth-04 5.4, synth-01 2.1 diagram | Covered |
| scope/02: who consumes `.dev/sweeps` (only skill, coordinator prose, person) | R4 ("Grep the whole snapshot"), synth-04 | Covered |
| scope/02: `_guard` / person_started reading "not tested: UNVERIFIED" | R3 topic (path A/B, `_guard`, which test proves) | Covered |
| scope/02: sweep report layout copied from #409 (orchestrator-mode.md:609), `models.py:162` ten dimensions | not present (0 hits for "dimensions", "Shift Brief", "#539") | GAP, F1 |
| scope/02: Phase 2 `/sc:close` (design line 217), closeout.md relation UNVERIFIED; classify.py:693-695 known gap; lock-risk line pinned to 1.4.245 | not named | Note, F6 |
| scope/03: orchestrator design-only; no writer of living-report entries | Key Objective 3; R5 C8 clause; synth-05; synth-07 candidate list; Gate 4 agent 2 | Covered |
| scope/03: `orchestrator_repo` (SKILL.md:14) unread by cli/issue_watch; who sets it UNVERIFIED | research-notes, BUILD-REQUEST, R5, synth-05, synth-07 | Covered (verified: only agent-work-report/scripts/common.py references it in snapshot py files) |
| scope/03: unreferenced `qa-report-template.md` | R5, synth-07 | Covered |
| scope/03: Orca automations and `.dev/coordinator/` contents live outside repo, UNVERIFIED | R5, synth-07, Open Questions | Covered |
| scope/03: U17/U38 design unknowns | R5 file list names U17/U38 sections; no instruction to report their status | Weak (Note, F6) |
| scope/03: PR C = this skill, PR B = package with `report-entry`; PRs after 61ac2c2e6 | R5 (`gh pr list --repo IronbellyOrg/IronClaude --search orchestrator`) | Covered |
| scope/03: overlaps 1-3 (status vocabularies, "waits on a person", transcript joins) | synth-01 2.5 overlaps table | Covered |
| scope/03: overlaps 4-7 (held work, outputs/recommendation posture, cadence/audience, item scope) | only via the free-text "overlaps" matrix column | Note, F5 |
| scope/03: SKILL.md:12 spec path not in repo; `hourly` dead path; system python3 / `python -m http.server` vs UV rule | not named | Note, F6 |
| scope/03: three separate Orca binary choices; separate sanitizers | synth-01 2.5, synth-06 8.1, synth-07 s12 | Covered |
| scope/04: 20 designs, 18 scenarios, 360 exports, proposed fixture schema not Orca API | R6, synth-05 5.6 | Covered |
| scope/04: untracked local-only research folder | stated in every prompt, R6, synth-01/02/05, Gate 3, Gate 4 | Covered |
| scope/04: package on origin/master via PR #503 though branch unmerged (C2) | research-notes, BUILD-REQUEST, R6 (git diff check), synth-05, synth-07 | Covered |
| scope/04: C1 (issue body stale), C3 (Bubble Tea vs Rich), C4 (actions), C5 (405 vs 406 files) | C1-C3 spelled out in R6; C4 appears in synth-07 (mockup actions, "next inspection"); C5 not spelled out anywhere | Partly, F3 |
| scope/04: integration-gaps items 1-6 closed/partly/open now; real vs assumed Orca fields | R6 topic and acceptance clause; synth-05 | Covered as a deliverable, but input set missing, F2 |
| scope/04: QA FAIL then corrections without new verdict; no design chosen | R6, synth-05 | Covered |
| scope/04: "observer reads sweep JSON" unbuilt direction | R6 topic | Covered |
| scope/04: reviewer asks (PR/issue links, step flow, plain-English summary, session-open link) | not present | GAP, F4 |
| scope/04: S1-S11 / R1-R11 rules trace, fixture-name parity, GitHub/ClickUp not read by design | R6 | Covered (labels undefined, F3) |

### 2.2 Checklist item 2: R1-R6 versus research-notes SUGGESTED_PHASES

All six match on output file name, type, topic and file list (Steps 2.1-2.6 versus the research-notes table rows R1-R6). The task file is a strict superset of the research-notes file lists:
- R1 adds `test_questions.py`, `test_export.py`; R2 adds `test_keys_spike.py`, `test_registration.py`, `test_height_budget.py`, `main.py` registration; R4 adds `test_cli_registration.py`, `test_report.py`, design section 17; all added files exist in the snapshot (checked).
- R6 matches the research-notes row exactly, including the `git show origin/master:` files (SPEC, rendering-rules, release-gates, unverified-register, REDESIGN-SPEC; all verified present with `git ls-tree origin/master`), `gh issue view 409`, and the local-only research folder.
- Gaps against the scope proposals for R6 are in F2-F4 (the research-notes row itself omits them, so the builder followed the notes faithfully; the omission is in the notes).

### 2.3 Checklist item 3: synthesis mapping and the owner's WHY

Mapping versus research-notes RECOMMENDED_OUTPUTS is exact:

| Synth file | research-notes | Task Step 5.1 item | Match |
|---|---|---|---|
| synth-01-overview-architecture | Sections 1, 2 incl. family-at-a-glance matrix and relationship diagram | Sections 1, 2 plus subsection 2.5 matrix | Yes |
| synth-02-directory-dataflow | 3, 4 | 3, 4 (4.1-4.3) | Yes |
| synth-03-subsystem-observer | 5.1-5.2 | 5.1-5.2 | Yes |
| synth-04-subsystem-sweep | 5.3-5.4 | 5.3-5.4 | Yes |
| synth-05-subsystem-work-report-dashboard | 5.5-5.6 | 5.5-5.6 | Yes |
| synth-06-integration-config-perf | 6 (N/A), 7 (N/A), 8, 9, 10, 11 | 6-11 with N/A rationale for 6 and 7 | Yes |
| synth-07-conventions-extension-debt | 12, 13, 14, 15, 16 | 12-16 plus provenance appendix text | Yes |

Owner's WHY coverage: data sources (2.5 matrix column, 4.2), output formats and where written (matrix, 3, 8.2 formats and schemas), live versus designed (matrix column "built / partially built / designed only", 5.5 built-vs-designed table, DESIGNED boxes in 2.1), consumers (matrix column, 8.2 who-reads-what matrix, 5.4 consumers), overlaps (2.5 overlaps table), relation to WC-16 (2.1 diagram, 5.4 binding), what is read from Orca versus written (8.1 verb inventory, 8.2 matrix), built versus designed (5.5, 5.6, 14). The cross-subject comparison matrix is a named, protected deliverable (Key Objective 2, Step 5.1 item 1, assembler, Gate 3 crossref-chain, Gate 4). Section 13.1 carries the "unification touch points" as facts. Covered. The only shortfall is the content of the overlaps (F5, F1, F4).

### 2.4 Checklist item 4: path and anchor spot-check (fabrication)

Method: extracted all 36 snapshot paths and 97 checkout paths from the task file and tested existence; then read specific line anchors. Every path that is not a to-be-created output exists. The files reported missing by the sweep are all outputs created during execution (research/, synthesis/, qa/, reviews/, gaps-and-questions.md, the final reference); none is a source path.

| # | Anchor in task/research-notes | Check against snapshot or origin/master | Result |
|---|---|---|---|
| 1 | `install_user_setup.py` `_find_orca` about 247-270 | `def _find_orca() -> str or None` at line 247 | OK |
| 2 | `main.py:590-592` observer registration | import at 590, `add_command(observe_group, name="observe")` at 592 | OK |
| 3 | `commands.py:67` / `:70` gate constants | both `= True` at 67 and 70 | OK |
| 4 | `parse.py:43` UNKNOWN sentinel | `UNKNOWN: Any = _Unknown()` at 43 | OK |
| 5 | `.gitignore:255-256` | comment plus `.dev/sweeps/` | OK |
| 6 | `classify.py` `RULES` about 345 | `RULES: tuple[Rule, ...] = (` at 345 | OK |
| 7 | `probes.py:226` `check_orca_argv` | def at 226 | OK |
| 8 | WORKER-CONTRACT.md WC-16 at 287-289 | heading and cadence text at 287-289 | OK |
| 9 | HOW-WE-WORK.md rows at 298, 359 | `/sc:sweep` routing row and coordinator bullet | OK |
| 10 | `settle.sh:1037-1042` | `superclaude orchestrator report-entry --help` guard and `ENTRY escalated ... surface_absent` | OK |
| 11 | `report.py:42-45` SP24_LINE | "Stalled and fenced are not observed in Phase 1..." | OK |
| 12 | `models.py:108-109` defaults | `worker_done_seen: bool or None = None`; `fenced_evidence: str = "unreadable"`; no other assignment in src | OK (supports the C8 premise) |
| 13 | `orchestrator-mode.md:27` | "`src/superclaude/cli/sweep/` does not exist yet." | OK (the CODE-CONTRADICTED claim is real) |
| 14 | `sc-closeout-protocol/scripts/settle.sh`, `agent-work-report/templates/qa-report-template.md`, `output-styles/pragmatic.md`, `cli/issue_watch/` | all exist | OK |
| 15 | origin/master-only `.dev/issues/409/bmad/spec-orca-observer/{SPEC,rendering-rules,release-gates,unverified-register}.md` and `visual-parity/REDESIGN-SPEC.md` | all present in `git ls-tree origin/master` | OK |
| 16 | `sweep.md:16` and `SKILL.md:26` cited as Phase 1 limit candidates | line 16 of sweep.md discusses Safe to close / Removable / Next inspection (limit text follows); line 26 of the skill prints counts with the lower-bound note | Plausible; agents are told to quote and cite, not to trust |
| 17 | "orchestrator-mode.md Phase 1 limits" | no heading with that exact string in the design doc | Not a fabricated path; the prompt calls it a candidate to check. Agents may not find a section by that name (Note) |
| 18 | `orchestrator_repo` only in AWR scripts | `grep -l` over snapshot py files returns only `agent-work-report/scripts/common.py` | OK (supports the UNVERIFIED claim) |

No fabricated path, no wrong anchor. The only soft spot is item 17.

### 2.5 Checklist item 5: dependency and ordering

Phase 1 -> Phase 2 (six independent agents, parallel) -> Gate 1 (three lenses, serialized fix protocol, max 2 cycles) -> gaps-and-questions.md (Step 3.8) -> Phase 4 skip decision -> Phase 5 (seven synth agents all read finished research plus gaps-and-questions.md and gap-fill files) -> Gate 2 (partitioned 01-04 / 05-07) -> Phase 6 assembly (reads all seven synth files) -> Gate 3 -> Gate 4 -> Phase 7. Synthesis dependencies are respected: synth-06 and synth-07 read all six research files; synth-03/04/05 read only their pairs; synth-02 reads five plus 02. Gate 4 reads the assembled reference. No ordering defect found. One soft dependency: R6's integration-gap status (F2) and the Section 14 contradictions rely on R2/R5/R6 findings being consistent; Gate 1 cross-reference check (item 5) covers that.

### 2.6 Checklist item 6: C8 and neutrality

- C8: the `stalled (proved)` / `fenced` candidate is handled in R3 (dedicated mandatory section, quote the declaring line, code evidence, cited decision or the exact words "remediation task not created (read-only brief); flagged for the owner"), R4, Gate 1 analyst checklist item 8, synth-01 (pointer only), synth-03/04/05/07, Gate 3 crossref-chain and Gate 4 agent 1 (stalled/fenced) and agent 2 (living-report writer). The task does not pre-decide the outcome: it lists the possible on-record decisions (sweep.md:16, SKILL.md:26, report.py:42-45, design Phase 1 limits) as candidates for the agents to quote or reject. That matches research-notes line 86 and BUILD-REQUEST NO_DOCS_CLOSE_DEFECT. Correct.
- The "do not recommend a unification" constraint is in the Task Overview, Key Constraints, every research prompt (R1-R6), synth-01 to synth-07, the assembler, Gate 2 neutrality checks (Steps 5.3 items), Gate 3 actionability and domain-accuracy lenses, and Gate 4. Correct.
- Gap-fill and verification items inherit the same wording (checked by token counts: DEFECT-CANDIDATE appears in 30 lines).

---

## 3. Findings

### F1 (Medium): sweep report layout derives from the #409 package; not routed anywhere

- **Scope evidence:** scope/04-dashboard-design.md section 4 item 8: `docs/designs/orchestrator-mode.md:609` "layout is SPEC section 9 ..., copied from #409 at `495eb96d` because #409 is unmerged"; `:463/:1018` "the ten #409 dimensions"; `sweep/models.py:162` "The #409 dimensions, nine fields (OQ-11)"; live issue body line 21 "The sweep report in PR #539 is laid out from this issue's design package (the header, the Attention Ledger and the Shift Brief views, and the ten per-session dimensions)". I confirmed line 609 of the design doc in the snapshot.
- **Task evidence:** the task file has 0 hits for "dimensions", "Shift Brief" and "#539"; R3 reads only design sections 7.2 and 12-14; R4 reads section 17; R6 and synth-05 5.6 frame the package's relationship as package-to-observer only. research-notes.md also omits it (FEATURE_ANALYSIS item 4 mentions only the observer), so the builder followed the notes, but the scope finding is dropped.
- **Why it matters:** the owner's question is overlap in purpose among the family. Two tools (observer via #606/#673, sweep via #539) already take their layout and semantic dimensions from the same design package, and the sweep pins a commit that is not reachable from master (C2). That is a cross-subject fact the Section 2.5 matrix and 5.6 should carry.
- **Remediation:** add to R6 topic (and R3 or R4) "which parts of the sweep report layout and the per-session dimensions come from the package: orchestrator-mode.md:609, :463, :1018; sweep/models.py:162; report.py sections 7 (ten dimensions) and 10 (Shift Brief); which dimensions the classifier actually sets (SessionRow defaults `unknown` for Phase/Approval/Admission/Evidence packet, models.py:164-173; Tests/review prints `unavailable`, report.py:401)", and add one clause to synth-05 5.6 and the synth-01 matrix "overlaps" cell. Also add the dimensions the sweep leaves permanently unknown to the C8 candidate list review (they are report columns declared by the design but never set).

### F2 (Medium): R6 has no evidence set for "closed / partly / open now" on integration-gaps items 1-6

- **Scope evidence:** scope/04 section 6, Agent B: inputs "adapter-contract.md, snapshot-export-schema.md, observe/adapter.py + collector.py + questions.py ..., PR #586/#589 live tests (41 questions read twice, burst loss 30 of ~415), sweep collection (orchestrator-mode.md section 7.4 JSON schema)".
- **Task evidence:** R6 requires a status table for items 1-6 and "which Orca fields are real versus assumed", but its file list names only SPEC, rendering-rules, release-gates, unverified-register and REDESIGN-SPEC. 0 hits for "586", "589", "adapter-contract", "snapshot-export-schema". Those two spec files and `.dev/issues/409/live-test-guide.md` and `owner-pass-record-20261112.md` exist on origin/master (`git ls-tree` checked). R2 covers PRs #503, #514, #577, #592, #598, #673 but not #586/#589.
- **Why it matters:** items 1 (non-consuming message enumeration beyond the 100-row view), 5 (replay) and the "real versus assumed Orca fields" question can only be settled from the live-read records. Without them the agent will either mark everything open or infer from code alone.
- **Remediation:** extend R6's file list with the two bmad spec files, `live-test-guide.md`, `owner-pass-record-20261112.md`, `owner-decisions-and-risks.md` (all verified present on origin/master), add `gh pr view 586 589 --repo IronbellyOrg/IronClaude` (read-only), and add `docs/designs/orchestrator-mode.md` section 7.4 for the sweep's captured Orca shapes.

### F3 (Medium): undefined labels S1-S11, R1-R11, C1-C5 in R6 and synth-05

- **Evidence:** R6 (Step 2.6) says "semantic rules S1-S11 and R1-R11 traced against the shipped observer" and "contradictions C1-C5 settled ... including the three known ones". The labels are defined only in scope/04 sections 4-5. research-notes.md defines neither the labels nor the rule text. R6 names C1-C3 in prose; C4 (research mockups propose reply/ack/resolve versus the package ban versus the sweep "next inspection" line) and C5 (405 versus 406 file count in local versus posted issue text) are not described in the prompt. synth-05 (Step 5.1 item 5) repeats the labels. "R1-R11" also collides with the research-agent labels R1-R6 in the same task file.
- **Risk:** the Phase 2 B2 self-contained pattern is broken; if R6 does not open scope/04 (the prompt calls it only a "starting map") the rule trace has no list to trace, and synth-05 cannot expand labels it never saw if the R6 file does not define them.
- **Remediation:** in R6 either embed the 11 S rules and 11 R rules (one line each, with the scope/04 citations) or instruct "read scope/04 sections 4 and 5 first and define every label in your output table"; add one line each for C4 and C5; rename the research-derived rules (for example RR1-RR11) to avoid the clash with agent labels, or state the clash.

### F4 (Medium): reviewer asks (PR/issue links, plain-English summary, session-open link, step flow) not routed

- **Scope evidence:** scope/04 section 2.5 and section 4 and section 6 Agent A (2): the 2026-11-11 reviewer comment (clayphi) wants a plain-English task summary, done/left, "needs me", PR/issue links, step-flow colours, click-to-open session; these need data the fixture lacks (issue body "Alignment decisions" item 3, live body line 114); Agent A should list the package ideas absent from the observer.
- **Task evidence:** 0 hits for "step flow", "plain-English", "session-open". R6 asks only whether any shipped component reads GitHub or ClickUp.
- **Why it matters:** these asks are what agent-work-report already provides (GitHub and ClickUp joins, plain-language summaries, session links). This is the clearest purpose overlap between the report skill and the dashboard direction, and it is a stated user ask on the record.
- **Remediation:** add to R6: "list the reviewer asks from the issue 409 comment of 2026-11-11 and mark, for each, whether the package fixture, the shipped observer, the sweep, or agent-work-report provides the data". Mention it in the synth-01 overlaps table.

### F5 (Note): overlaps list in synth-01 omits scope/03 overlaps 4-7

synth-01 (Step 5.1 item 1) enumerates five overlaps: status vocabularies, "waits on a person", terminal-to-transcript join keys, sanitizers, Orca binary choices. scope/03 section 6 also lists: held work versus sessions (exclude.py drops sessions an orchestrator entry names; the sweep has no such concept), recommendation posture (the sweep "adds no recommendation", AWR's model writes recommendations, suggested priorities and "Needs you" options), cadence and audience (weekday 07:00 push to one person versus on-demand versus a 15 s poll), and item scope (AWR joins GitHub and ClickUp, sweep and observer read Orca only). The matrix columns "consumers" and "data sources" can absorb the last two, but "held work" and "recommendation posture" have no home. Add them to the overlaps table clause.

### F6 (Note): small UNVERIFIED and stale items not named in any prompt

Section 14's rule ("every UNVERIFIED / CODE-CONTRADICTED / STALE DOC item from every research file") only catches these if the R agents surface them. Items from the scope files that no prompt names: (a) AWR SKILL.md:12 cites `.dev/specs/SPEC-AGENT-WORK-COORDINATOR-20261027.md`, not in this repo; (b) `hourly` mode and `time_budget_minutes.hourly` are dead paths (waker.py:8, 216-220; config.json:10); (c) AWR runs under system `python3` and starts `python -m http.server` (page.py:322 confirmed) in a repo whose rule is UV-only, stated in scope/03 as an observation not a recommendation; (d) design unknowns U17 and U38 (R5's file list names the sections but not the status question); (e) sweep Phase 2 `/sc:close` (orchestrator-mode.md line 217) and the unverified relation to `commands/closeout.md`; (f) classify.py:693-695 "Known gap" (a worker-list row without a Dispatch id is dropped); (g) the "Orca lock risk: unlikely" line pinned to version 1.4.245 (report.py:23); (h) observer exit codes marked "UNVERIFIED by running" in scope/01 cannot be checked because the task forbids running code, and R2 is not told to tag those two as UNVERIFIED. None blocks the document; most are one-clause additions to R3/R4/R5.

### F7 (Note): `output-styles/pragmatic.md` not in R4's file list

scope/02 Agent B lists `output-styles/pragmatic.md` (the chat-summary exemption is mirrored at line 23). R4's topic names "the pragmatic output-style exempt reply rule" but its file list does not include the file; the file exists in the snapshot at `src/superclaude/output-styles/pragmatic.md`. Add it.

### F8 (Note): issue-watcher side of Clay's design only reached by a grep

The owner's WHY describes an orchestrator "woken by the issue watcher". scope/03 section 0 and section 5 record that `wake.py` and `hold.py` are absent from `cli/issue_watch/` (orchestrator.md:432 says wake.py is meant to duplicate about 100 lines of orca_term.py). The task has 0 hits for "wake.py" and "hold.py"; R5 only greps `cli/issue_watch` for `orchestrator_repo`. R5's built-versus-designed table will probably include the wake path through the design sections it reads (5.4, 6.4, 8.1-8.2), so this is a Note. Add "list which files of `cli/issue_watch/` exist and which designed files (wake.py, hold.py) are absent" to R5.

---

## 4. Things checked and found aligned (no finding)

- Phase 2 prompts embed the GLOBAL AGENT RULES verbatim, the incremental-writing protocol, the documentation staleness protocol and the C8 clause with the read-only override.
- Every `gh` call in the task file is read-only and carries `--repo IronbellyOrg/IronClaude`; no `git fetch/pull/push/remote` and no SuperClaude-Org interaction instruction anywhere (46 mentions of SuperClaude-Org are all in prohibitions).
- The untracked, local-only research folder is labelled in R1-R6, synth-01/02/05, Gate 3 and Gate 4 prompts.
- The research-notes known contradictions (orchestrator-mode.md:27; issue 409 body versus banner versus comment; package on master via PR #503; Bubble Tea versus Python/Rich; actions; AWR `orchestrator_repo`; `qa-report-template.md`) all appear in R-prompts and in synth-07's Section 14 list, together with the UNVERIFIED items (Orca automations, `.dev/coordinator/`, `orchestrator_repo` setter, question non-acknowledging claim).
- The Phase-1-not-observed sweep classes and `Safe to close` / `Removable` are covered (see 2.6).
- The orchestrator being design-only is a stated fact in Key Objective 3, R5, synth-01 Section 1, synth-05 5.5 and Gate 4 agent 2.

---

## 5. Verdict

No blocking finding: no required deliverable is absent in substance, no fabricated path or anchor, no scope or safety-boundary risk. Four Medium alignment gaps (F1-F4) concentrate in the R6 assignment and the overlap picture and should be fixed in the task file before execution; they are small edits (a few clauses and file paths). Four Notes (F5-F8) are optional.

VERDICT: PASS
