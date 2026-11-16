<!-- Provenance: produced by /sc:adversarial via sc:reflect Wave 4 -->
<!-- Base: Variant 3 -->

# Merged reviewer card (stage 2 plan, UC-1)

Plan under review: .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md

Citation key (as used in the source cards): `plan` = the plan above; `spec` = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md; `stage1 plan`, `stage3 plan`, `stage 0 plan` = the stage plans of the same program, as cited by the source cards; `SKILL.md` = the file named next to it in the citation.

Grading rule: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format; medium = a real non-blocking weakness, repeated under follow-up candidates.

## Findings

### Blocking

id: MB-1
severity: blocking
claim: Task 8 cannot unambiguously associate safety confirmations with findings across multiple runs. Its confirmation file contains only row ids, but the ledger contract makes those ids run-scoped.
citations: plan:138; plan:141; spec:352
quote: "one row id per line that a later review or the owner confirmed as a safety risk"; "`FU-000001` upward, run-scoped, never reassigned or recycled"
consequence: Two valid runs can both contain FU-000001. A confirmation for that id cannot identify which run's finding was confirmed; matching all occurrences overcounts, while choosing one can miss the confirmed unrouted risk. The required safety-miss result therefore cannot be reliably computed for the multi-run input Task 8 specifies. The fixture acceptance does not require a repeated-id case across runs. Blocking because a required result is ambiguous, not because the fix is expensive.
fix direction: use a `run_id:id` form for confirmations and add a colliding-id test across two runs.
provenance: <!-- Source: Variant 2, R2-1, merged per P-1 -->
debate outcome: Round 1 superior-variant confidence for this point: A1 75, A2 99, A3 55. Round 2: A2 blocking 95; A1 blocking 80 (a one-run fixture passes, real data fails); A3 holds that it is a missing `run_id:id` qualifier (spec:339 carries run_id), a one-line fix, and gave no blocking verdict. The cheap fix does not change the consequence (an ambiguous stage 3 entry number).

id: MB-2
severity: blocking (CONTESTED)
claim: Task 7 requires the answering agents to see only the blind table, excluding the code-supplied context needed for the intended classifier evaluation. Running the supplier afterwards cannot make previously recorded, text-only answers into code-informed answers. The M, C and E answers cannot be code-informed.
citations: plan:28; plan:126; plan:130; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/04-historical/blind-table-1.md:3-5; spec:501; spec:512-516
quote: "The agents see only the blind table"; "they were given the blind table only"; "| ID | Category | Description brief | Context |"; "code does every exact check first ... and passes the result in as state"
consequence: For rows where the supplier can provide a required-item list, constraint lines or verified evidence, the agents still cannot receive those inputs under the stated acceptance criterion. The evaluation would repeat the text-only limitation the plan expressly identifies (plan:28), rather than measure the code-informed classifier; the number the owner reads for the stage 3 go would measure the text-only judge. Blinding labels and consensus is compatible with supplying evidence, but the plan does not permit that enriched input packet.
fix direction: say the agents get the blind table plus the supplier's inputs for that row.
provenance: <!-- Source: Variant 2, R2-2, merged per P-2 -->
debate outcome: CONTESTED, graded by consequence. Round 1 superior-variant confidence: A1 68, A2 96, A3 40. Round 2: A2 blocking 90 (counting inputs at plan:132 shows availability, not that the agents received them; concedes plan:126's parenthetical names forbidden labels only); A1 minor 65 (plan:28 and plan:126/130 do not contradict literally; plan:132 UNSET/NA partly mitigates); A3 wording 40 (plan:126's parenthetical excludes consensus, grade, label and scale map, not code inputs; plan:132 implies the agents saw inputs).

id: MB-3
severity: blocking
claim: The spec says a possible safety finding graded non-blocking makes the run `worker_status: partial`. Task 5 maps only `follow_up_capture_state: incomplete` to partial. It then says follow-ups never change `succeeded`, with no exception for the safety route. Task 2's `summary` prints exactly three keys, and none of them can carry a safety state. Task 2's "signal that makes the run `partial`" therefore has no consumer in the contract text or tests.
citations: spec:438; plan:56; plan:102; plan:106-107; src/superclaude/core/WORKER-CONTRACT.md:36
quote: spec:438 "A possible safety finding graded non-blocking (GR12) makes the run `worker_status: partial`"; plan:102 "follow-ups alone never change `worker_status` from `succeeded`"
consequence: The only `partial` rule Task 5 adds and tests is the `incomplete` capture case (plan:106-107). A contract written after an unattended safety row can end `succeeded`, which contradicts spec 6.4. Impact today is latent, because no command emits the keys live (plan:138); the omission is baked into the pinned contract text and tests the plan creates, so a later stage that wires an emitter inherits the gap.
fix direction: add the GR12 safety-row to `partial` mapping to the WC-4 bullet (WORKER-CONTRACT.md:36) and add a test for it.
provenance: <!-- Source: Variant 1, R1-2, merged per P-3 -->
debate outcome: Round 2: A1 blocking 70 (no key carries the signal; impact zero today because there is no live emitter); A2 conceded blocking (spec:438 not covered by plan:102/106-107). A3: round 1 superior-variant confidence V1 60; the refactor plan records agreement. Round 1 had A2 saying Task 5 meets REQ-12; reversed in round 2.

id: MB-4
severity: blocking (narrowed)
claim: In phases 3 and 5, the reviewers that feed the consolidation Task 4 passes to `follow-ups write` are not all covered by the five templates Task 4 edits. The two rf-analyst agents per gate use the "Research Analyst Agent Prompt" (not edited), and the rf-qa-qualitative agent per gate has no embedded template, so their findings never carry `rests_on` or `why not blocking`. Two of the five edited templates (Report Validation and Qualitative) are LEGACY and are not used for Phase 6, while the active Research QA and Synthesis QA templates are edited.
citations: plan:88; src/superclaude/skills/tech-research/SKILL.md:480; :487; :507; :819; :848; SKILL.md:479-487; SKILL.md:507-516; SKILL.md:952; SKILL.md:1003; rf-analyst.md:195-202; spec:318; spec:648
quote: plan:88 "Five reviewer prompt templates (Research QA, Synthesis QA, Report Validation QA, Qualitative QA, Lens-Specific QA)"; SKILL.md:487 "Read ALL reports from Step 3.1, consolidate into"; SKILL.md:819 "### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)"; spec:318 "Each reviewer writes every finding with the fields of section 6.2, including `rests_on`"
consequence: Three of five reviewers per gate in phases 3 and 5 never get the fields. Analyst output is bullets under "Compiled Gaps" (rf-analyst.md:195-202): if the parser reads only tables, analyst non-blocking items vanish; if it reads bullets, GR2 refuses them. Either way the phase 3 and 5 ledger volume (a stage 2 exit number) is undercounted. Task 4 and the T9 test check only the five templates, so the gap passes the tests. Blocking only when an analyst or qualitative reviewer supplies non-blocking findings; lite depth runs no analysts (SKILL.md:400, 404).
provenance: <!-- Source: Variant 3, R3-3, merged per P-4 -->
debate outcome: Round 1 superior-variant confidence: A1 55, A2 narrowed 95, A3 75. Round 1 objection (A1): unproven if the run owner supplies the fields; A2 concedes blocking only when an analyst supplies non-blocking findings. Round 2: A3 blocking 65 on the narrowed claim (phases 3 and 5; SKILL.md:952 and :1003 are LEGACY; active templates at :864 and :911; analyst prompt at :819 and qualitative agent at :483, :511 not edited).

### Non-blocking

id: MN-1
severity: medium
claim: Tag persistence is unspecified. The plan's flow writes a safety-vocabulary row as a plain follow-up first (Task 4 runs `follow-ups write`, then `follow-ups safety`), and nothing in the plan tests that the `protected-risk-dispute` tag is stored. In addition, a second `write` may reset tags set by `safety` (INV-001).
citations: plan:56; plan:88; plan:138; stage1 plan:196; spec:932; stage1 plan:194; stage1 plan:198-202; plan:61
quote: plan:56 "`safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and prints what it returns"; plan:88 "the run owner writes `${TASK_DIR}qa/follow-ups.md` with `superclaude review follow-ups write` ... then runs `superclaude review follow-ups safety` over the ledger"; plan:138 "the count is the confirmed rows that lack the `protected-risk-dispute` tag"; spec:932 "is written as a plain follow-up instead of `protected-risk-dispute` (GR12)"
consequence: If stage 1's route does not save the tag, a confirmed safety row counts as a safety miss even when `safety` showed it to the person, and `show_user` undercounts; the stage 3 entry "safety misses 0" would be unreachable. Stage 2 `safety` has no `--write` switch and `write` runs before `safety`. None of stage 1 Task 13's acceptance checks (stage1 plan:198-202) tests that the ledger holds the tag. The only idempotence test (plan:61) has no `safety` call between writes. Meetable; the sweep and summary tests use fixtures and will not catch it. The earlier "every real run breaks GR12 by construction" claim is withdrawn.
fix direction: add one acceptance line that the ledger holds the tag after `safety`, including after a second `write`.
provenance: <!-- Source: Variant 3, R3-1 reduced, plus INV-001, merged per P-5 and P-9 -->
debate outcome: A3 round 2 conceded minor 55 (stage1 plan:196 "tags the row"; stage1 plan:194 Task 13 depends on Task 7; plan:125 lets `safety_route.py` import `follow_ups`). A1 round 2 blocking 60 only if Task 2's read of `safety_route.py` shows it does not save the tag. Round 1: A2 qualified 80, A1 58, A3 60. INV-001 is a fault-finder item, MEDIUM, UNADDRESSED, not debated.

id: MN-2
severity: minor
claim: For tech-research reports, the tier lookup `write` depends on is not fully pinned. `write` has no family or scale selector (labels such as IMPORTANT and MINOR appear in other families with different outcomes), and the report tables come in two column layouts. The label-to-outcome pairs and the Severity columns exist, so this is a residual format gap.
citations: plan:56; spec:737; spec:739; stage1 plan:62; src/superclaude/skills/tech-research/SKILL.md:902; plan:26; rf-qa.md:448; rf-qa-qualitative.md:883; SKILL.md:900; spec:744; SKILL.md:1147-1149; plan:29
quote: plan:56 "the tier of a row is the shared outcome that `refs/scale-map.md` gives its native label"; spec:737 "the label is information; the outcome comes from the three conditions"; spec:739 "MINOR: Note"; SKILL.md:902 "Use the full QA report output format from your agent definition."
consequence: The parser must accept `| # | Severity | Section | Finding | Proposed Fix |` and `| # | Severity | Location | Issue | Required Fix |`, and tech-research treats IMPORTANT as blocking (SKILL.md:900) while spec:744 says card_convert maps important to non-blocking. A failed parse sets `capture_state: incomplete` (plan:56), a counted capture failure at the stage 3 entry (plan:29): safe and visible. "Every run partial" is not established. There is no fixture that passes real edited reviewer output through `write`.
fix direction: pin the LABEL=Outcome mapping and both column layouts in a test, and run one fixture derived from the real edited reviewer output format through `write`.
provenance: <!-- Source: Variant 3, R3-2 reduced, merged per P-6 -->
debate outcome: A3 round 2 conceded minor 65; A1 minor 65. Round 1 superior-variant confidence: A1 68, A2 83 (V2, producer-to-parser fixture), A3 65; majority V3.

id: MN-3
severity: medium
claim: Task 3 reads follow-up ledgers that no task in the plan makes `/sc:implement` write, so in a real `/sc:implement` run the sweep sees no `follow-ups.md`. The fixed line Task 3 prints, that follow-ups "are recorded" (the "recorded and not filed" line), is unconditional and is false in a zero-ledger run.
citations: src/superclaude/skills/sc-implement-protocol/refs/qa.md:209-211; src/superclaude/skills/sc-implement-protocol/refs/ledger.md:60; plan:72; plan:84-88; plan:138; spec:484
quote: plan:72 "over the follow-up ledgers the run's review loops wrote (every `follow-ups.md` under the package folder for a managed package"; spec:484 "`/sc:implement` (exception) | keeps `notes.md`; the ledger holds a pointer row"
consequence: A grep of `src/superclaude/skills/sc-implement-protocol` for "follow-up" finds only `ledger.md:60`, which is about the verdict. Task 4 writes `follow-ups.md` for tech-research only (plan:88); nothing builds the spec's pointer row. Every Task 3 acceptance line is satisfiable because they check text only. The limits at plan:138 say "mostly reports skips" but should say the sweep finds no ledger; stage 3 then adds `--promote` to a call that has no input. Disclosed in part at plan:138 ("shadow ledgers come only from tech-research runs"), no data loss.
fix direction: make the printed line conditional on a ledger being found, and say at plan:138 that the sweep finds no ledger.
provenance: <!-- Source: Variant 1, R1-1 reduced, with Variant 3 follow-up candidate 1, merged per P-7 -->
debate outcome: Graded minor after round 2. A1 conceded a disclosed shadow-stage limit (minor; the unconditional printed line is the residue). A3 round 2 minor 60, reversing her round 1 concession of blocking. Round 1 superior-variant confidence: A1 85, A2 94, A3 75 (V1 found it).

id: MN-4
severity: minor
claim: Task 1's entry check is narrower than the Constraints promise. The Constraints say Task 1 checks that the `classify` command exists; Task 1 imports only three modules and never checks `classify_cmd`/`classifier`, `refs/scale-map.md` (read by Tasks 2 and 4) or `refs/registry.yaml` (read by Task 6). Correction to the "fails after edits" reading: Task 2 checks that command help lists `classify` (plan:59) before the carrier edits, so only the scale-map and registry files can fail late.
citations: plan:20; plan:44; plan:113; plan:126; plan:59; plan:39-44
quote: plan:20 "its modules `follow_ups.py`, `safety_route.py`, `classifier_inputs.py` and the `classify` command exist; Task 1 checks that"; plan:44 "`uv run python -c \"from superclaude.cli.review import follow_ups, safety_route, classifier_inputs\"`"
consequence: If a scale-map or registry file is missing, the run fails at Task 4 or 6 after earlier edits. The failure is loud and causes no data loss.
provenance: <!-- Source: Variant 3, R3-4, with Variant 2 refutation of F3 (plan:59), merged per P-10 -->
debate outcome: A3 round 1 conceded "after edits" overstated (plan:59). Shared assumption A-001 QUALIFY by A1, A2 and A3 (late failure true only for scale-map and registry files, not `classify`). Round 1 superior-variant confidence C-008: A1 80, A2 96, A3 60.

id: MN-5
severity: minor
claim: The plan never says what the "call line" is. Task 3 asks for one paragraph that holds the call and also says "never `--promote` and never `--write`". `SKILL.md` writes paragraphs as one physical line, but Task 3 AC3 and the stage 3 entry check test the line holding the call for the absence of `--promote` and `--write`. A literal executor puts both on one line and fails the AC.
citations: plan:72; plan:79; src/superclaude/skills/sc-implement-protocol/SKILL.md:192; stage3 plan:42
quote: plan:72 "`--kind auto`, never `--promote` and never `--write`"; plan:79 "neither call line holds `--promote` or `--write`"; stage3:42 "shows one call line in each file, and neither line holds `--promote` or `--write`"
consequence: Task 3 AC3, Task 6's mutation test and stage 3's entry check all fail on the plan's own wording if the paragraph follows house style. Task 6 and stage 3 (which adds `--promote` to "those two lines") both assume a distinct call line.
fix direction: state that the command sits on its own line or in a code block.
provenance: <!-- Source: Variant 1, R1-3, merged with Variant 3, R3-5, merged per P-8 -->
debate outcome: Agreed minor by all three advocates (C-009 tie V1/V3: A1 85, A2 95, A3 80).

id: MN-6
severity: minor
claim: Task 4 tells tech-research to record and not wait "with nobody reachable", but tech-research has no unattended mode, and no rule says when the run owner passes `--unattended` to `follow-ups safety`.
citations: plan:88; plan:102; plan:56; src/superclaude/skills/tech-research/SKILL.md (a case-insensitive grep for `unattended` finds nothing)
quote: plan:88 "with nobody reachable it records and does not wait"; plan:102 "tech-research has no unattended mode and no contract"
consequence: The skill text has no way to choose the unattended branch, so that branch never runs from tech-research. In practice it is always attended, so the skill would always take the person-prompt branch.
fix direction: state the condition, or say tech-research always runs the attended route.
provenance: <!-- Source: Variant 1, R1-5, merged with Variant 3, R3-7, merged per P-8 -->
debate outcome: Agreed minor (C-010 tie: A1 90, A2 90, A3 75). Both source cards confirm the same earlier-card finding F6.

id: MN-7
severity: minor
claim: The printed list needs recorded counts, `show_user` rows first, and the ledger paths. The single sweep call does not produce any of them. Task 2 defines sweep output as the flagged rows and the skipped count. Counts are the job of `summary`, which Task 3 never calls.
citations: plan:56; plan:72
quote: plan:56 "prints the flagged rows (id, deliverable, section) and the skipped count"; plan:72 "the final summary prints the recorded counts, ... the `show_user` rows first"
consequence: The executor must parse `follow-ups.md` by hand, or call `summary`. `summary` is not named, and one call is a pinned count. It is not a failure while no ledger exists (MN-3), but the printed list has no defined producer.
provenance: <!-- Source: Variant 1, R1-4, merged per P-8 -->
debate outcome: A1 conceded minor. A2 round 1: not independently blocking (plan:72 directs the executor to print). Round 1 superior-variant confidence C-011: A1 60, A2 85, A3 50; majority V1, low confidence.

id: MN-8
severity: minor
claim: The Constraints say "after Task 2 two more files mention it", but three files will match `grep -rln "follow_ups"`: `sweep.py` (from Task 1) reads through the stage 1 reader, `follow_ups_cmd.py` is new, and `__init__.py` gains the string "follow_ups_cmd".
citations: plan:27; plan:49; src/superclaude/cli/review/__init__.py:19; stage1 plan:125
quote: plan:27 "after Task 2 two more files mention it"; plan:49 "its only file reads are deliverables and the stage 1 reader"
consequence: Anyone who re-runs the stage 1 acceptance grep will see a count that does not match. No test pins it.
provenance: <!-- Source: Variant 3, R3-6, merged per P-10 -->
debate outcome: Agreed minor (C-013: A1 75, A2 90, A3 75).

id: MN-9
severity: minor
claim: Task 2 gives `safety` a `--judge-answers <file>` option but also says no subcommand calls a judge. Recorded answers can only be read through stage 1's `FixtureJudge`.
citations: plan:56; stage1 plan:146
quote: plan:56 "No subcommand calls `gh`, a network or a judge."
consequence: The ban should name live judges. As written, a strict reading forbids the wiring that `--judge-answers` needs.
fix direction: name live judges in the ban.
provenance: <!-- Source: Variant 3, R3-8, merged per P-10 -->
debate outcome: A3 conceded weak; agreed minor or wording (C-014: A1 45, A2 82, A3 40).

id: MN-10
severity: minor
claim: Task 4's body and its `grep -ci sweep` acceptance check can disagree: the body describes the meaning of a sentence that says there is no sweep, while the acceptance requires that sentence to avoid the word.
citations: plan:88; plan:92
quote: plan:88 vs plan:92 (same as card finding F5/C-012 wording); "Task 4 body and its `grep -ci sweep` check agree"
consequence: A wording tension only. Task 4 AC2 matches its own instruction (no "sweep" in added lines), and both requirements can be satisfied together.
provenance: <!-- Source: Invariant probe, INV-009, merged per P-9 and P-10 -->
debate outcome: Not debated (Round 2.5 fault-finder, LOW, UNADDRESSED). Variant 2 refuted the earlier card's F5 as a defect: "the one sentence that says there is no sweep avoids the word."

id: MN-11
severity: medium
claim: Task 8's acceptance commands may not run as written: `./artifacts/` is package-relative, but the command is run from the repo root, where `./artifacts/` does not exist.
citations: plan:141; plan:33
quote: plan:141 `uv run python ./artifacts/shadow_summary.py --help` from the repo root; `./artifacts/` is package-relative (plan:33) and does not exist at the root
consequence: The Task 8 acceptance command fails or checks the wrong place until the path is corrected.
provenance: <!-- Source: Invariant probe, INV-008, merged per P-9 -->
debate outcome: Not debated (Round 2.5 fault-finder, MEDIUM, UNADDRESSED).

id: MN-12
severity: medium
claim: An empty `--confirmed-misses` file prints a bare 0, and the stage 3 entry accepts it. The assumption that a confirmation file means rows were reviewed is not guarded.
citations: plan:138; stage3 plan:49
quote: plan:138 prints "not computable" only when the file is absent; an empty file prints a bare 0; stage 3 plan:49 accepts "safety misses 0 (not "not computable")"
consequence: A run with no confirmations reviewed reaches the stage 3 entry with a safety-miss figure of 0 that reads as a pass.
provenance: <!-- Source: Invariant probe, INV-003, merged per P-9 -->
debate outcome: Not debated (Round 2.5 fault-finder, MEDIUM, UNADDRESSED).

id: MN-13
severity: medium
claim: Zero ledgers, zero runs and empty sets have no stated handling. There is no divisor guard or "not computable" convention for the share, and no empty-input test; Task 7 sets may lack enough rows for kappa, recall or the kind split.
citations: plan:56; plan:126; plan:138; plan:141; stage 0 plan:96
quote: plan:56 sweep exit rule for zero ledgers unstated; plan:138 share has no divisor guard; plan:141 no empty-input test; stage 0 plan:96 fresh set of 17; plan:126 figures with no "not computable" convention
consequence: A zero-ledger or small-set run can divide by zero or print a figure that looks computed.
provenance: <!-- Source: Invariant probe, INV-004 and INV-005, merged per P-9 -->
debate outcome: Not debated (Round 2.5 fault-finder, MEDIUM, UNADDRESSED).

id: MN-14
severity: medium
claim: `capture_state: incomplete` may not survive a later successful `write`: the spec has a single header value, and the summary test covers only the unreadable-report case.
citations: spec:345; plan:56; plan:62
quote: spec:345 single header value; plan:56; summary test plan:62 covers only the unreadable-report case
consequence: A capture failure can be reset to complete by a later write, so a run that lost rows reports a clean capture state.
provenance: <!-- Source: Invariant probe, INV-002, merged per P-9 -->
debate outcome: Not debated (Round 2.5 fault-finder, MEDIUM, UNADDRESSED).

id: MN-15
severity: minor
claim: Three low-severity probe items. (INV-006) Stage 3 may not find stage 2's paragraph title and "never --promote" words. (INV-007) The tech-research source-fidelity and anti-omission reviewers get no field, and stage 1 makes the registry tuple ten. (INV-010) Task 3's placement check does not force the call after `FINAL: pass`.
citations: stage3 plan:177; plan:77-82; src/superclaude/skills/tech-research/SKILL.md:1164; SKILL.md:1207; managed-workspace.md:56; managed-workspace.md:58-60; managed-workspace.md:62; plan:78
quote: stage 3 plan:177; Task 3 acceptance (plan:77-82) and Task 6 test do not pin the title or words; tech-research SKILL.md:1164 source-fidelity and :1207 anti-omission reviewers get no field; managed-workspace.md:56 step 5, :58-60 FINAL block, :62 step 6; plan:78 only requires "after the step 5 line and before the step 6 line"
consequence: Stage 3 may not find the paragraph it edits; two more tech-research reviewers produce rows without the fields; the call could sit inside or before the FINAL block while still passing the placement check.
provenance: <!-- Source: Invariant probe, INV-006, INV-007, INV-010, merged per P-9 -->
debate outcome: Not debated (Round 2.5 fault-finder, LOW, UNADDRESSED).

## Refuted or withdrawn
- Variant 2 R2-3 (coverage matrix omits requirement-bearing spans): withdrawn by its advocate as a plan defect (traceability only); the by-hand disposition shows no requirement missing.
- Earlier-card F5 (Task 4 body vs `grep -ci sweep`): not a defect per Variant 2, "The body describes the meaning of the sentence, not mandatory literal wording"; kept only as the wording tension MN-10.
- Earlier-card F7 (carrier move vs earlier halt-offer instructions): not an execution-blocking contradiction per Variant 2; Revision 2 moves the carrier and drops the earlier halt-offer instructions as identifiable amendments (source.md:27-29).
- Variant 3 R3-1 "by construction" claim (every real run breaks GR12 and fails T17): withdrawn by its advocate A3; reduced to MN-1.

## Checked, no defect
- Registration: `__init__.py:19-36` optional tuple plus add_command; `follow-ups` does not clash with panel, merge, ledger, telemetry, cluster, verify, manifest; `tests/review/test_review_cli.py:44-49` checks only four names.
- tech-research targets exist: five prompt headings (SKILL.md:859, 906, 950, 1001, 1048), three consolidation items (487, 516, 549), Output Locations table (129-150), "INDEPENDENT STANCE ... no minimum count" (1063); exactly two full cap sentences (490, 555), phase 5 says only "then HALT" (519).
- Add-only edits keep the pins: `test_lens_prompts_state_no_minimum_count` (test_review_prompt_overrides.py:271-283), NO_CONDITIONAL_PASS (test_review_severity_rule.py:344-359), banned phrases (112-125), F1-F6 sweep patterns (398-405), at-cap clauses (215-219); multi-line pin S-106 (fixtures/review_severity_sweep_edits.yaml:877-878) holds if the new paragraph is not placed between the Synthesis QA PASS and FAIL lines.
- Task 4 AC2 (no "sweep" in added lines) matches its own instruction; `test_review_severity_mapping.py` reads only pragmatic.md and spec-panel.md.
- Static scan regex (test_implement_severity_static.py:296) does not match "STOP"; the allow-list pins steps 2, 3 and 6 (331-333).
- Archive digest skips `./artifacts/` paths (archive_workspace.py:396-405), so the sweep record does not make FINAL stale.
- pragmatic.md:225 holds the sentence Task 6 pins; stage 3 line 134 expects the Task 6 skip once the row is v2.
- Stage 3 consumes sweep.py, follow_ups_cmd.py, test_review_sweep.py, test_review_brief_rests_on.py, test_implement_follow_up_sweep.py (stage3:41) and one call line per file (stage3:42); Tasks 3 and 6 produce all of these.

## Follow-up candidates
Medium items from the register, repeated by id:
- MN-1: add an acceptance line that the ledger holds the `protected-risk-dispute` tag after `safety` and after a second `write`.
- MN-3: make the printed "recorded and not filed" line conditional, and say at plan:138 that the sweep finds no ledger in a `/sc:implement` run.
- MN-11: fix the Task 8 acceptance commands so `./artifacts/` resolves from the repo root (plan:141).
- MN-12: make an empty `--confirmed-misses` file print "not computable", not a bare 0 (plan:138).
- MN-13: define a no-divisor and "not computable" convention for zero ledgers, zero runs and empty Task 7 sets, with an empty-input test.
- MN-14: add a test that `capture_state: incomplete` survives a later successful `write` (plan:56, plan:62).

verdict: NEEDS-REVISION (4 blocking: MB-1, MB-2, MB-3, MB-4)
convergence_score: 0.90 (19 of 21 diff points agreed; C-004 and C-005 split)

## Evidence validation postscript (orchestrator, after the evidence-validator gate; the findings above are unchanged)
- 125 citations re-read, 2 dropped: MN-11 (the "run from the repo root" premise is an inference the plan does not state; treat MN-11 as [INFERRED], recorded in grounding-gaps.yaml) and MN-8 (the "three files" count is not supported by stage1 plan:125; the direction, that plan:27 "two more files" is too low, holds).
- All citations and quotes of MB-1 to MB-4 verified. Two line-drift corrections: Output Locations table rows are 133-152 (heading 129); archive_workspace.py skip logic is at 395-401 and the digest call at 404-405.
- Final register after the gate: 4 blocking (MB-1 to MB-4), 14 non-blocking grounded (MN-1 to MN-10, MN-12 to MN-15, with MN-8 reworded as above), 1 dropped to Grounding Gaps (MN-11).
