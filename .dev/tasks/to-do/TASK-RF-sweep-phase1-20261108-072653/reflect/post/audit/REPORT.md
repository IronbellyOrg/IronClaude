# Reflect post-execution report: Issue #339 Phase 1 (orchestrator mode, `superclaude sweep`)

```yaml
contract_version: 1.8.0
status: needs_human_decision
mode: post
tier_reached: 2
confidence_calibrated: 0.67          # mean of the three calibrated reviewer cards (0.65, 0.63, 0.73); the Tier-1 card calibrated at 0.76
citations_total: 122
citations_revalidated: 95
citations_dropped: 1
citations_inferred: 3
citation_budget_policy: sampled
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
run_id: reflect-post-20261112T192600Z-TASK-RF-sweep-phase1
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 95` - size of the semantic re-Read sample (the evidence-validator agent re-Read 100% of D-01, D-04, D-10, D-11 and the verification bullets and about half of the rest). A mechanical script also confirmed that all 122 distinct `path:line` citations exist and that 56 quoted strings sit within 3 lines of their citation.
> - `citations_dropped: 1` - the sample-count: one claim ("byte-identical ... by running") had no logged run behind it; it was moved to the logged inspections (`verify-logs/inspections.yaml`) and reworded. This count gates promotion.
> - `citations_dropped_extrapolated: 1` - `round(1 x (122 / 95))`. Recording-only.
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Verdict

**Merged verdict: PASS-with-deviations. The run needs a user decision before the task can be marked Done.**

- No finding is blocking (adversarial merge, convergence 1.00, 29 of 29 diff points, base variant 3).
- Deviation register: 17 entries: 1 Regression (D-01, contested 2 of 3, medium), 11 Drift (3 medium: D-02, D-03, D-04; 8 minor), 4 Authorized, 1 Necessary.
- Escalation: the Regression and the 11 unauthorized Drift items are unresolved. Under the task's rule (item 14.48) they are escalated to the user and NOT logged as Open Questions. Only the 4 Authorized, the 1 Necessary and the minor notes are appended to `### Open Questions`.
- Why PASS and not FAIL: the one Regression is a departure from a SPEC mechanism (the 8 MiB kill) that no acceptance fixture exercises; all 1788 scoped tests pass, ruff is clean, and the real entrypoint lists `sweep run`. If the user rules the departure acceptable, D-01 becomes Authorized (add a DESIGN section 13 row, total 11) and the register holds no Regression.
- Promotion (Wave 7): not performed. Gate conditions failed: unfinished checklist items 14.48 and 14.49, a Regression and Drift items, grounding gaps, and `needs_human_decision`.

### What was verified by running things (grounded)

- `uv run ruff check` on the touched files: exit 0. `uv run pytest` on `tests/sweep`, `tests/commands/test_sweep_command.py`, `tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`: 1788 passed, exit 0 (`verify-logs/invocations.yaml`).
- `uv run superclaude sweep --help` and `sweep run --help`: exit 0, subcommand and four options listed.
- The two failing `tests/cli/eval/test_claude_process_adapter.py` ruff tests fail with `No module named ruff` in `.venv` (not in the diff); the timing tests pass on an isolated re-run (D-17).
- The diff file regenerates byte-identical from the working tree (721933 bytes, 50 files), no `.claude/` path is staged, the HOW-WE-WORK file and its plugin mirror are byte-identical, and the sweep skill, command, WORKER-CONTRACT and HOW-WE-WORK carry no `src/superclaude/` path (orchestrator read-only git, cmp and grep inspections, outputs recorded in `verify-logs/inspections.yaml` INS-1 to INS-4; `pragmatic.md` was not part of the grep). Reviewer 3 reported the same for the new package and tests (`SuperClaude-Org`: INS-5).
- Input tree hash unchanged between Wave 0 and Wave 5 (779 files): no drift.

### Wave attestation

Tier 2: ensemble = 3 reviewers (sonnet analyzer, haiku qa, opus refactorer; executor class unresolved), per-card blind calibration = done (opus; calibrator diversity degraded because only three model classes resolved), adversarial merge = done (`sc-adversarial-protocol`, Mode A, depth standard), evidence-validator gate = see header counts and `evidence-validation.md`.

## Deviation register

### Deviation D-01 (F-01): Subprocess output is fully buffered and checked after exit; SPEC requires Popen, chunked reads and a kill at 8 MiB

- **Location:** src/superclaude/cli/sweep/probes.py:257-273, src/superclaude/cli/sweep/probes.py:308-316
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC section 8 (merged-requirements.md:286, :296-297); DESIGN 7.1 (:386)
- **Evidence:** "run it with `subprocess.Popen`" (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:286); "proc = subprocess.run(" (src/superclaude/cli/sweep/probes.py:257); "if len(proc.stdout) + len(proc.stderr) > OUTPUT_LIMIT:" (src/superclaude/cli/sweep/probes.py:270); "proc = subprocess.run(" (src/superclaude/cli/sweep/probes.py:308)
- **Classification:** regression (medium, confidence 0.62)
- **Classification rationale:** SPEC section 8 says both seams run subprocess.Popen, read the output in chunks and kill the child once combined output passes 8 MiB. Both seams call subprocess.run(capture_output=True) and test the size only after the child has exited. DESIGN names only the result and has no section 13 row; the tasklist item that chose subprocess.run gives a reason (the test guard only catches subprocess.run) that the guard file contradicts, because it patches Popen and os.system as well. For a runaway child the observable result differs: unavailable 'timeout after N s' instead of call_failed 'output over 8 MiB'. Authorization: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2992 note (13) names the departure but cites only the tasklist item; no DESIGN section 13 row and no owner approval found. contested: V1 and both blind calibrators class this Drift medium (no acceptance fixture fails; SPEC :297 boundary fixtures feed finished outputs and pass). Resolved 2 of 3 (V2, V3 Regression) at 62%. Fallback if the narrow A-002 rule (only a failed acceptance criterion counts) is adopted: Drift medium. Rollback: remove the Regression label and use Drift medium. INV-005: on the first Orca call any call_failed becomes unavailable (src/superclaude/cli/sweep/probes.py:355-357), so 'output over 8 MiB' on call one is reported as unavailable. INV-003: the runaway-child result fails closed for origin (later Orca sources go unscanned).
- **Default remediation:** In src/superclaude/cli/sweep/probes.py replace the two subprocess.run seams (_orca at :257, _git at :308) by subprocess.Popen with stdout and stderr piped, chunked reads, and a kill of the child once combined output passes OUTPUT_LIMIT (8 MiB), returning call_failed 'output over 8 MiB' (and the _git equivalent). If the owner prefers to keep subprocess.run, record the departure as a DESIGN section 13 row (total becomes 11) with owner approval. Verify with a new test in tests/sweep/test_probes_allowlist.py that streams more than 8 MiB from a fake Popen child and asserts the child was killed and the result is call_failed, then run `uv run pytest tests/sweep -q`.

### Deviation D-02 (F-02): NFR-007 'still publish' tests stop at report.render and never exercise publication

- **Location:** tests/sweep/test_probes_allowlist.py:1144-1147, tests/sweep/test_probes_allowlist.py:1150-1169
- **Mapped tasklist item:** tests/sweep/test_probes_allowlist.py: items ['2.5', '10.3', '14.49']
- **Spec section:** SPEC NFR-007 (:136); DESIGN section 11 test row (:760)
- **Evidence:** "a report is published" (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:136); "full-timeout fakes finish under 120 s and still publish" (docs/designs/orchestrator-mode.md:760); "text = report.render(" (tests/sweep/test_probes_allowlist.py:1144); "def test_every_call_timing_out_still_collects_and_publishes(" (tests/sweep/test_probes_allowlist.py:1150)
- **Classification:** drift (medium, confidence 0.88)
- **Classification rationale:** NFR-007 says a report is published when every probe uses its full timeout, and DESIGN section 11 repeats 'full-timeout fakes finish under 120 s and still publish'. The two tests that carry this (the budget test and test_every_call_timing_out_still_collects_and_publishes) end at report.render; neither calls publication, asserts a report file, a footer or an exit code. Collection and rendering are bounded, publication is not exercised. Nothing shows publication fails, so this is a coverage gap, not a regression. Authorization: none found. V2 labelled this Regression/blocking; calibrated Drift medium; V2 conceded in Round 2. Not carried: the blocking label. Cross-reference fix: V2 cited 'FIN-F19' as the task's id for this item; the calibrator found that points at the wrong item. The task finding is not named here.
- **Default remediation:** Add a test (tests/sweep/test_probes_allowlist.py or tests/sweep/test_cli_contract.py) that calls src/superclaude/cli/sweep/commands.py `_publish(text, output_dir, now)` (defined at commands.py:153), or invokes `sweep run` through click's CliRunner, under the same full-timeout fakes, and asserts the report file exists, ends with 'Report complete' and the JSON/exit code is success. Alternatively rename the two tests so they claim only collection and rendering. Verify with `uv run pytest tests/sweep/test_probes_allowlist.py -k timing_out -q`.

### Deviation D-03 (F-03): Stale approval and blocking-status text in DESIGN and the task Open Questions

- **Location:** docs/designs/orchestrator-mode.md:5, docs/designs/orchestrator-mode.md:7, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3037-3043
- **Mapped tasklist item:** docs/designs/orchestrator-mode.md: items ['1.3', '1.4', '2.1', '2.2', '2.3', '2.4', '2.6', '2.7']
- **Spec section:** DESIGN section 1 Status and Review status (:5-7); task Open Questions (:3037-3043)
- **Evidence:** "Owner approval of the WC-16 text (section 8) is still required." (docs/designs/orchestrator-mode.md:5); "Review status: NOT a clean pass." (docs/designs/orchestrator-mode.md:7); "OWNER DECISION PENDING" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3037); "OWNER DECISION PENDING; blocks the classify step." (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3042)
- **Classification:** drift (medium, confidence 0.85)
- **Classification rationale:** The DESIGN header still says owner approval of the WC-16 text 'is still required' and 'Review status: NOT a clean pass', and still lists R3-B1..R3-B3 as open blocking findings. The task file's Open Questions OQ-2 to OQ-8 still read OWNER DECISION PENDING or PERSON INPUT PENDING (OQ-7 'blocks the classify step') although decision records exist for each. These are current-looking instructions, not labelled history. Authorization: none found. Documentary reconciliation only. V2 accepted in Round 2 that this is not a veto on runtime promotion. The DESIGN edit is a DESIGN change: it needs the owner's decision path (DESIGN is edited by decision, not by a fix agent, per FINAL-GATE-halt-resolution-decision.md:23).
- **Default remediation:** Edit .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3037-3043 so OQ-2..OQ-8 read RESOLVED with their decision-record paths (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-2-GQ-10-report-location-decision.md, OQ-3-GQ-11-rule-id-decision.md, OQ-4-GQ-35-409-pin-decision.md, OQ-5-GQ-61-window-decision.md, OQ-6-GQ-63-done-next-decision.md, OQ-7-D9-signoff-decision.md, OQ-8-run-id-decision.md), and update docs/designs/orchestrator-mode.md lines 5-11 (approval of WC-16 recorded, review status reflects the closed R3-B1..R3-B3 gates). Verify with `grep -n PENDING <task file>` returning no OQ-2..OQ-8 hits and `grep -nE 'still required|NOT a clean pass' docs/designs/orchestrator-mode.md` returning none.

### Deviation D-04 (F-04): Worker-list rows with a missing or empty dispatchId are dropped from rows and invisible to the FR-010 origin guard

- **Location:** src/superclaude/cli/sweep/probes.py:1105-1119, src/superclaude/cli/sweep/classify.py:690-694, src/superclaude/cli/sweep/classify.py:759-762
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC FR-005 (:99) and FR-010 (:104); DESIGN 7.2 (guard cases)
- **Evidence:** "for index, row in enumerate(workers):" (src/superclaude/cli/sweep/probes.py:1105); "name = f"orca worker-list {run} row {index}"" (src/superclaude/cli/sweep/probes.py:1109); "if isinstance(dispatch, str) and dispatch:" (src/superclaude/cli/sweep/probes.py:1115); "listing = source.get(f"orca worker-list {run}")" (src/superclaude/cli/sweep/classify.py:690)
- **Classification:** drift (medium, confidence 0.8)
- **Classification rationale:** _run_rows keeps a row only when dispatchId is a non-empty string (an id failing the regex is kept; a missing, non-string or empty id is dropped) and records a source row named 'orca worker-list <run> row <i>' with unscanned set. _origin_unknown reads only 'orca worker-list <run>' and 'orca task-list <run>', so that source row never makes the guard fail. When every row of a Run is dropped, rows is empty, all four guard flags are False and an unjoined transcript ends as person_started True with the 'origin not proved' note. No test covers it and no decision authorizes it. Authorization: none found. Conditional escalation (INV-001/INV-002): if real Orca emits worker rows without dispatchId (queued or undispatched workers), every recent transcript of that Run becomes a person-started IDLE session and F-04 becomes a wrong-class bug (Regression against FR-010/NFR-008). Needs the owner's decision on the capture. Orchestrator ruling (INV-001): the five list-incomplete cases are the whole of FR-010's enumerated rule (docstring src/superclaude/cli/sweep/classify.py:679), so a dropped row is a completeness-detection gap outside them: Drift medium, not a bug in the enumerated rule. Under path B any other surviving non-ready row already makes earlier_pane True (src/superclaude/cli/sweep/classify.py:739), so the hole is confined to the all-rows-dropped Run.
- **Default remediation:** In src/superclaude/cli/sweep/classify.py `_origin_unknown` (:678-708) treat any unscanned source row whose name starts with 'orca worker-list <run> row ' as an incomplete list for that run (set failed = True, adding NOTE_ORIGIN_CALL_FAILED), then add a test in tests/sweep/test_classify.py (and a probes-side case in tests/sweep/test_probes_allowlist.py) for a Run whose worker-list rows ALL lack a valid dispatchId: the unjoined transcript must be person_started None with an 'origin unknown:' note, never True or Historical. Verify with `uv run pytest tests/sweep/test_classify.py -k fr010 -q`. Before that, capture a live worker-list for a queued or undispatched worker (step 1.0a style, read-only) to settle the escalation condition below.
- **[INFERRED] notes:** [INFERRED] Whether real Orca emits worker rows without a dispatchId is UNVERIFIED: the captured worker-list fixture holds 5 rows and all carry one.

### Deviation D-05 (F-05): A ledger over the limit is searched in the tail only; the head is never read and the test name still says head and tail

- **Location:** src/superclaude/cli/sweep/probes.py:557-569, tests/sweep/test_probes_allowlist.py:1328-1331
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC section 8 byte limits (:295) and FR-020 (:114); DESIGN 2.2 (:62), 7.3 (:548), section 11 (:760)
- **Evidence:** "handle.seek(size - LEDGER_SPLIT)" (src/superclaude/cli/sweep/probes.py:563); "only the last LEDGER_SPLIT bytes are searched" (src/superclaude/cli/sweep/probes.py:561); "the head 512 KiB and the tail 512 KiB are read and the tail is searched" (docs/designs/orchestrator-mode.md:62); "a ledger over 1 MiB is read as head and tail (GQ-105)" (docs/designs/orchestrator-mode.md:760)
- **Classification:** drift (minor, confidence 0.85)
- **Classification rationale:** SPEC FR-020 (line 295) and DESIGN GQ-105 say a ledger over 1 MiB is read as its first 512 KiB and last 512 KiB, with the tail searched for FINAL:. The code seeks to size - LEDGER_SPLIT and reads only the tail, so the head is never read. Both SPEC and DESIGN say only the tail is searched, so the FINAL detection value is identical and no behaviour changes. The test named for head and tail asserts only a tail-derived boolean, so the name claims more than the test shows. Authorization: none found. Lowered from Regression (V3 R3-F4, V2 R2-F5 blocking). Calibrated Drift low (V2 note) and low-to-medium (V3 note); all three advocates settled on Drift minor (85%). Not carried: the Regression label and the blocking label. INV-007: the first line of the tail is always dropped (src/superclaude/cli/sweep/probes.py:565), so when the cut falls exactly on a line start a complete FINAL: line is lost; pinned by test_ledger_tail_drops_a_first_line_that_the_cut_split (test_probes_allowlist.py:1336-1346). Not a defect against SPEC (the tail rule drops up to the first newline).
- **Default remediation:** Either read the head in src/superclaude/cli/sweep/probes.py `_ledger_has_final` (open the file, read LEDGER_SPLIT bytes from offset 0 as well as the tail) or amend DESIGN GQ-105 (docs/designs/orchestrator-mode.md:62, :398, :548, :760) and SPEC line 295 to say tail only; in both cases rename tests/sweep/test_probes_allowlist.py `test_ledger_over_the_limit_is_read_as_head_and_tail` to match what it asserts (for example `..._is_searched_in_the_tail`). Verify with `uv run pytest tests/sweep/test_probes_allowlist.py -k ledger -q`. Treat as a doc and test-name fix; no output changes.

### Deviation D-06 (F-06): _git over-limit reason prints bytes instead of 8 MiB, is pinned by a test, and never reaches the report

- **Location:** src/superclaude/cli/sweep/probes.py:316, tests/sweep/test_probes_allowlist.py:1454, src/superclaude/cli/sweep/probes.py:936-937
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC section 8 (:286); DESIGN 7.2 (:513)
- **Evidence:** "`output over 8 MiB`" (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:286); "raise GitCallFailed(f"output over {OUTPUT_LIMIT} bytes")" (src/superclaude/cli/sweep/probes.py:316); "f"output over {OUTPUT_LIMIT // _MIB} MiB"" (src/superclaude/cli/sweep/probes.py:272); "assert str(exc.value) == f"output over {8 * MIB} bytes"" (tests/sweep/test_probes_allowlist.py:1454)
- **Classification:** drift (minor, confidence 0.82)
- **Classification rationale:** SPEC section 8 says the worktree status is unread with the reason 'output over 8 MiB'. _git raises 'output over 8388608 bytes', while _orca prints MiB. The divergent string is pinned by a test. _read_worktree collapses any non-timeout GitCallFailed to 'worktree not readable' (as DESIGN 7.2 prescribes), so users never see either string; the divergence is confined to exception text. Authorization: none found. Absorbs T1 lead DC-12 (added after calibration); no separate finding. The V1 citation for DC-1 (FINAL-GATE...:18-19 as 'open item 6') is not carried; see F-13.
- **Default remediation:** Change src/superclaude/cli/sweep/probes.py:316 to f"output over {OUTPUT_LIMIT // _MIB} MiB" and update the pin at tests/sweep/test_probes_allowlist.py:1454 to the MiB form. Verify with `uv run pytest tests/sweep/test_probes_allowlist.py -k output -q`. Low value if F-01 is fixed first (the Popen rewrite touches the same line).

### Deviation D-07 (F-07): Third per-Run source row and extra model fields beyond DESIGN 7.2 and 7.4

- **Location:** src/superclaude/cli/sweep/probes.py:1033, src/superclaude/cli/sweep/probes.py:1054, src/superclaude/cli/sweep/probes.py:131-133, src/superclaude/cli/sweep/models.py:21-29, models.py:103-104, models.py:147-148
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** DESIGN 7.2 (:449-518) and 7.4 (:597)
- **Evidence:** "ready_name = f"orca task-list --ready {run}"" (src/superclaude/cli/sweep/probes.py:1033); "its own source row named `orca worker-list <run>` and another named `orca task-list <run>`" (docs/designs/orchestrator-mode.md:597); "task-list --ready  R" (docs/designs/orchestrator-mode.md:300); "mtime: datetime | None = None" (src/superclaude/cli/sweep/models.py:104)
- **Classification:** drift (minor, confidence 0.8)
- **Classification rationale:** The code adds a third per-Run source row 'orca task-list --ready <run>' where DESIGN 7.4 names two, plus model fields DESIGN 7.2 does not list: four constants in models.py and SessionRow.freshness_age_s (Drift), and ContractRecord.mtime and OrcaObservation.agent_wait_since (Necessary: they serve the SP-15 age rule and the reserved agent-wait marking). The ready call itself is counted in DESIGN section 6, and classify reads only the two named rows, so behaviour is unchanged. The final-gate owner decision only approves marking the unused fields reserved; the additions are recorded by the task as minor findings, not approved. Authorization: none found. Split by field (Change 4): constants and freshness_age_s are Drift; mtime and agent_wait_since are Necessary. V1's 'authorized' label for R1-F7 is not carried (calibrated overstated: FINAL-GATE :19 approves only the reserved marking). The task records the additions as FIN-F10..F12 (minor). Authorization for freshness_age_s specifically was not found (V1 grounding gap): its consumer in report.py was not located.
- **Default remediation:** Record the additions in DESIGN 7.2 and 7.4 (the third source row name 'orca task-list --ready <run>', share_shows(wanted), ContractRecord.mtime, SessionRow.freshness_age_s, the four constants) through an owner-approved DESIGN edit or a section 13 row, or add a one-line code comment pointing at the task finding that records each. Verify with `grep -n 'task-list --ready' docs/designs/orchestrator-mode.md` showing the 7.4 text names it. No code change needed.

### Deviation D-08 (F-08): The skill says to print 'the standard error line' on exit 1 or 2, but the command can emit several lines

- **Location:** src/superclaude/skills/sc-sweep-protocol/SKILL.md:27, src/superclaude/cli/sweep/commands.py:137-143
- **Mapped tasklist item:** src/superclaude/skills/sc-sweep-protocol/SKILL.md: items ['11.3', '11.4', '11.6', '11.7', '11.8', '11.9', '11.10', '11.11']
- **Spec section:** DESIGN 7.6 (:650-668); SKILL step 5
- **Evidence:** "print the standard error line exactly as it came" (src/superclaude/skills/sc-sweep-protocol/SKILL.md:27); "def _drop_own_temp(tmp: Path) -> tuple[str, ...]:" (src/superclaude/cli/sweep/commands.py:137); "return (f"[sweep publish] left temp file {tmp}",)" (src/superclaude/cli/sweep/commands.py:142); ""On exit 1 or 2, print the standard error line exactly as it came and end the run."," (tests/commands/test_sweep_command.py:446)
- **Classification:** drift (minor, confidence 0.78)
- **Classification rationale:** SKILL.md step 5 tells the agent to print 'the standard error line' on exit 1 or 2. _drop_own_temp can add a second stderr line ('[sweep publish] left temp file ...') after a publication error, and click's own usage errors (exit 2) print a multi-line block, so the singular wording can lead the agent to relay only part of the error. The wording is pinned by a test. Authorization: none found. Weak V3 cite commands.py:219-221 (decorator lines) replaced by the _PublishError second-line cite (commands.py:137-143), per calibration. The task logged it as FIN-F59.
- **Default remediation:** Edit src/superclaude/skills/sc-sweep-protocol/SKILL.md step 5 to 'print the whole standard error exactly as it came' (every line), mirror it to the plugin copy if one exists, and update the pinned sentence at tests/commands/test_sweep_command.py:446. Run `make sync-dev` and `uv run pytest tests/commands/test_sweep_command.py -q`. Stage only the src/ side (never .claude/).

### Deviation D-09 (F-09): Structural debt: the XDG state folder is computed in two places, and two public wrappers have only test callers

- **Location:** src/superclaude/cli/sweep/commands.py:253, src/superclaude/cli/sweep/probes.py:1253-1255, src/superclaude/cli/sweep/probes.py:589-591, src/superclaude/cli/sweep/probes.py:944-947
- **Mapped tasklist item:** src/superclaude/cli/sweep/commands.py: items ['9.1', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10', '9.11']
- **Spec section:** DESIGN 7.1 module table
- **Evidence:** "state = Path(os.environ.get("XDG_STATE_HOME") or (home / ".local" / "state"))" (src/superclaude/cli/sweep/commands.py:253); "os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state")" (src/superclaude/cli/sweep/probes.py:1254); "def read_ledger(path: Path, root: Path | None = None) -> bool | None:" (src/superclaude/cli/sweep/probes.py:589); "def read_worktree(path: Path, budget: Budget) -> tuple[WorktreeState, SourceCoverage]:" (src/superclaude/cli/sweep/probes.py:944)
- **Classification:** drift (minor, confidence 0.78)
- **Classification rationale:** The --output overlap check (commands.py) and the tab-map read (probes.collect) each derive the XDG state folder separately from XDG_STATE_HOME; if one changes, the check would guard a different folder than the one read. read_ledger and read_worktree are public wrappers whose only callers in src are their own definitions (collect uses _read_worktree and the _ledger helpers), so tests exercise a slightly different surface from collect. Authorization: none found. This merge re-checked the caller claim with a search over src: read_ledger and read_worktree appear only at their definitions (src/superclaude/cli/sweep/probes.py:589, :944); _read_worktree is the collect caller (src/superclaude/cli/sweep/probes.py:1247).
- **Default remediation:** Add one helper (for example probes.state_dir()) used by both commands.py:253 and probes.py:1253, and either call read_ledger/read_worktree from collect or point their tests at the helpers collect uses. Verify with `grep -n XDG_STATE_HOME src/superclaude/cli/sweep/*.py` showing one definition and `uv run pytest tests/sweep -q`. Optional cleanup; the task logged it as FIN-F44 and FIN-F48.

### Deviation D-10 (F-10): git status in an Orca-listed worktree can run that worktree's core.fsmonitor command or start the fsmonitor daemon

- **Location:** src/superclaude/cli/sweep/probes.py:304-310, src/superclaude/cli/sweep/probes.py:1-8, CHANGELOG.md:11
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC NFR-001/NFR-002 (:130-131, :285); CHANGELOG entry (CHANGELOG.md:11)
- **Evidence:** "argv = ["git", "--no-optional-locks", "-C", str(cwd), *args]" (src/superclaude/cli/sweep/probes.py:305); "every subprocess is one allowlisted ``git status``" (src/superclaude/cli/sweep/probes.py:6); "stdin=subprocess.DEVNULL," (src/superclaude/cli/sweep/probes.py:262); "proc = subprocess.run(" (src/superclaude/cli/sweep/probes.py:308)
- **Classification:** drift (minor, confidence 0.7)
- **Classification rationale:** The git argv is 'git --no-optional-locks -C <path> status ...' with no '-c core.fsmonitor=false'. Paths come from Orca 'worktree ps'. A repo-local core.fsmonitor setting runs a configured hook or starts the built-in daemon (standard git behaviour, not tested here). That contradicts the module docstring ('every subprocess is one allowlisted git status') and the CHANGELOG claim that the command 'changes nothing in Orca, in git or in any worktree'. No spec line addresses it. _git also passes no stdin=DEVNULL, unlike _orca. Already recorded as a [Low] hardening follow-up and a MINOR safety-gate note. Authorization: none found. Severity lowered from medium to minor (66%): already filed as a [Low] follow-up (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3066) and as MINOR RO-1 in qa/final/qa-readonly-safety-report.md (:13 and :55, re-read); the fix changes a pinned argv and needs an owner note. V1 view: medium. T1 lead DC-4 proposed class 'none'; both V3 and V1 class it Drift, so DC-4 is not carried as 'none'.
- **Default remediation:** In src/superclaude/cli/sweep/probes.py `_git` (:305) add '-c', 'core.fsmonitor=false' after '-C', str(cwd) and pass stdin=subprocess.DEVNULL at :308. This changes the pinned NFR-002 argv (DESIGN section 11, tests/sweep/test_readonly.py), so record an owner note first. Verify with `uv run pytest tests/sweep/test_readonly.py tests/sweep/test_probes_allowlist.py -q`, plus a new real-git test in a tmp_path repo whose config sets core.fsmonitor to a marker script and asserts the script did not run. Follow-up, not a gate.
- **[INFERRED] notes:** [INFERRED] No reviewer or auditor ran it in this audit; the task's own final read-only safety gate reports a reproduction in a private /tmp repo (RO-1, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/final/qa-readonly-safety-report.md:13), so the behaviour is shown by the task's record, not by this audit.

### Deviation D-11 (F-11): Contract and ledger readers accept non-regular files: a FIFO blocks the run and defeats the byte limit

- **Location:** src/superclaude/cli/sweep/probes.py:557-567, src/superclaude/cli/sweep/probes.py:714-720, src/superclaude/cli/sweep/probes.py:837
- **Mapped tasklist item:** src/superclaude/cli/sweep/probes.py: items ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49']
- **Spec section:** SPEC section 8 (:291, NFR-007 :136)
- **Evidence:** "size = os.stat(path).st_size" (src/superclaude/cli/sweep/probes.py:558); "if os.stat(path).st_size > CONTRACT_LIMIT:" (src/superclaude/cli/sweep/probes.py:718); "if not path.is_file():" (src/superclaude/cli/sweep/probes.py:837); "Disk reads are bounded by the byte limits and are not timed." (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:291)
- **Classification:** drift (minor, confidence 0.7)
- **Classification rationale:** The ledger and contract readers apply the byte limit to os.stat().st_size (0 for a FIFO, standard POSIX behaviour, not tested here) and then read with no timeout. A FIFO named progress.md or return-contract.yaml inside a scanned worktree would hang the read-only command until the skill's 120 s Bash timeout. SPEC says disk reads are untimed and bounded only by byte limits, so the spec itself leaves this open. The tab-map reader, a sibling, does check is_file. Authorization: none found. Severity lowered from medium to minor (66%): already a [Low] follow-up (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3066) and MINOR RO-2 in qa/final/qa-readonly-safety-report.md (:14 and :56, re-read: 'readers hang on a FIFO; add a regular-file check'); .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:291 itself says disk reads are untimed (a SPEC gap). V1 view: medium. Citation fix: V3 cited src/superclaude/cli/sweep/probes.py:837 as the transcript reader; calibration found it is the tab-map reader's is_file check. The sibling point still holds and is stated with the correct reader.
- **Default remediation:** In src/superclaude/cli/sweep/probes.py `_ledger_has_final` (:557), the contract reader (:714-720), check stat.S_ISREG(os.stat(path).st_mode) before open() and return the existing unscanned reason (for example 'not a regular file'). Verify with a new test in tests/sweep/test_probes_allowlist.py that creates a FIFO with os.mkfifo in tmp_path under a fake package and asserts the read returns unscanned within a short timeout, then `uv run pytest tests/sweep -q`. Follow-up, not a gate.
- **[INFERRED] notes:** [INFERRED] A 0-byte FIFO passing the st_size check and blocking the read is standard POSIX behaviour that was not run here.

### Deviation D-12 (F-12): JSON report_path and worktree paths go through the Markdown sanitizer; a path containing [ ] \ < > | is not the real path

- **Location:** src/superclaude/cli/sweep/report.py:694, report.py:590-598, report.py:664
- **Mapped tasklist item:** src/superclaude/cli/sweep/report.py: items ['8.12', '10.5', '14.49']
- **Spec section:** SPEC FR-016 (:110); DESIGN 7.4 (:593)
- **Evidence:** ""report_path": sanitize(report_path)," (src/superclaude/cli/sweep/report.py:694); ""path": sanitize(w.path)," (src/superclaude/cli/sweep/report.py:664); "("[", "\\[")," (src/superclaude/cli/sweep/report.py:595); ""report_path": "<absolute path of the published report>"" (docs/designs/orchestrator-mode.md:593)
- **Classification:** drift (minor, confidence 0.6)
- **Classification rationale:** DESIGN defines report_path as the absolute path of the published report. to_json applies sanitize() to it, which rewrites '[' to '\[' and '<' to '&lt;' (and the other listed characters). A checkout path with those characters yields a report_path the skill (step 3) cannot Read, and a JSON consumer receives altered worktree paths. FR-016 targets untrusted text in rendered cells; the path the command publishes is chosen by the tool under <root>/.dev/sweeps/, so low practical impact. Authorization: none found. Severity lowered from medium to minor (62%). V1 view: medium. V3 did not re-read the sanitizer in Round 2; this merge re-read report.py:590-598, :664 and :694 and confirmed the call sites.
- **Default remediation:** In src/superclaude/cli/sweep/report.py `to_json` emit report_path and worktree paths as plain strings (str(report_path), str(w.path)) and keep sanitize() for Markdown cells only. Verify with a new test in tests/sweep/test_report.py that renders JSON for a path containing '[' and '<' and asserts the JSON value equals the real path, then `uv run pytest tests/sweep/test_report.py -q`. The task notes the same point as FID-F9. Follow-up.

### Deviation D-13 (F-13): Rule 5 (working) is inert by owner decision; DESIGN section 13 has no row, SPEC FR-006 is unamended and the report footnote is silent on working

- **Location:** src/superclaude/cli/sweep/classify.py:251-257, src/superclaude/cli/sweep/report.py:42-45, tests/sweep/test_classify.py:368-376, docs/designs/orchestrator-mode.md:491, docs/designs/orchestrator-mode.md:840
- **Mapped tasklist item:** src/superclaude/cli/sweep/classify.py: items ['8.4', '10.2', '14.49']
- **Spec section:** SPEC FR-006 (:100); DESIGN 7.2 (:491), open item 6 (:997), section 13 (:840)
- **Evidence:** "each class name is reached at least once" (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:100); "Rule 5 cannot match in Phase 1 (DESIGN open item 6)" (src/superclaude/cli/sweep/classify.py:252); "return None" (src/superclaude/cli/sweep/classify.py:257); "matched = "fallback" if rule == "working" else rule" (tests/sweep/test_classify.py:368)
- **Classification:** authorized (minor, confidence 0.88)
- **Classification rationale:** SPEC FR-006 says each class name is reached at least once, but Rule 5 returns None unconditionally and the tests expect every class except working. The owner decision 'All 3 approved' (2026-11-12) edited DESIGN lines 491 and 760 so that Rule 5 stays inert until open item 6 closes; DESIGN wins over SPEC under its section 15.2, so the deviation is authorized. DESIGN section 13 was left at 10 rows and SPEC FR-006 was never amended, so the unmet SPEC criterion is recorded only in the decision file. Residual (Drift minor, FIN-F15): the report footnote names only stalled and fenced, so working: 0 carries no caveat. Authorization: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md:13 and :18 (owner: 'All 3 approved'; edits DESIGN :491 and :760). SPEC FR-006 (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:100) was never amended; the owner approved a DESIGN edit only (V2's point, kept visible here even though the class is Authorized). Residual footnote: Drift minor (FIN-F15, tasklist follow-up item at .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3065): SP24_LINE names only stalled and fenced; working: 0 has no caveat.
- **Default remediation:** Extend SP24_LINE in src/superclaude/cli/sweep/report.py:42-45 to name `working` (and the agent-wait source) as not observed until open item 6 closes, update the DESIGN D7 pin and tests/sweep/test_report.py to match, or add a DESIGN section 13 row for the FR-006 deviation (total becomes 11) so the unmet SPEC criterion is recorded where readers look. Verify with `uv run pytest tests/sweep/test_report.py -q` and `grep -n 'working' src/superclaude/cli/sweep/report.py`.

### Deviation D-14 (F-14): Sweep chat-summary exception in pragmatic.md and SKILL.md

- **Location:** docs/designs/orchestrator-mode.md:1050-1052, src/superclaude/skills/sc-sweep-protocol/SKILL.md:43-51
- **Mapped tasklist item:** docs/designs/orchestrator-mode.md: items ['1.3', '1.4', '2.1', '2.2', '2.3', '2.4', '2.6', '2.7']
- **Spec section:** DESIGN scoped addendum (:1050-1052); OQ-6 (b)
- **Evidence:** "## Scoped normative addendum: sweep final chat-summary exception" (docs/designs/orchestrator-mode.md:1050); "The owner chose (b)" (docs/designs/orchestrator-mode.md:1052); "nothing here is exempt and every reply keeps the ordinary formatting" (src/superclaude/skills/sc-sweep-protocol/SKILL.md:49); "The only exception is the sweep chat-summary exception" (src/superclaude/output-styles/pragmatic.md:22)
- **Classification:** authorized (minor, confidence 0.85)
- **Classification rationale:** The owner chose option (b) through the scoped addendum. The skill and the output style state the same five conditions, and SKILL.md falls back to ordinary formatting when the installed output-style copy has no sweep exception, which is the state until the HOME copy is refreshed by reinstall. Authorization: docs/designs/orchestrator-mode.md:1052 (its text says planning only, separate execution authorization required) plus the owner's separate execution authorization recorded verbatim in .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-7.10-style-exception.md:5-12 (owner message 2026-11-11T20:26:41Z: 'Accepted, I accepted, but it reported a decline.  Proceed', which the executor read as the 'Run 7.10 now' option); this audit cannot check that message against the session transcript. INV-013 (Rule 5 inert x output-style exception x exempt reply interaction) was not probed by the fault-finder (UNVERIFIED); no evidence to classify it, so it is left out of the findings.
- **Default remediation:** No change needed to the text. After merge run `superclaude install` so the HOME output-style copy carries the exception, and confirm with `grep -n 'sweep chat-summary exception' ~/.claude/output-styles/pragmatic.md`. Until then every reply keeps ordinary formatting by design.

### Deviation D-15 (F-15): The exempt chat reply omits the Orca outage warning under an explicitly accepted limitation (FIN-F7)

- **Location:** src/superclaude/skills/sc-sweep-protocol/SKILL.md:25-35, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:15-17
- **Mapped tasklist item:** src/superclaude/skills/sc-sweep-protocol/SKILL.md: items ['11.3', '11.4', '11.6', '11.7', '11.8', '11.9', '11.10', '11.11']
- **Spec section:** DESIGN 7.6; FIN-F7 (qa/final/gate-decision.md)
- **Evidence:** "take only `report_path` and `summary`" (src/superclaude/skills/sc-sweep-protocol/SKILL.md:25); "only the summary counts and the report path are printed" (src/superclaude/skills/sc-sweep-protocol/SKILL.md:35); "FIN-F7 is a documented limitation of Phase 1. It is not fixed in this run." (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:15); "Final gate: PASS by owner ruling, open: FIN-F7" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:16)
- **Classification:** authorized (medium, confidence 0.85)
- **Classification rationale:** The skill takes only report_path and summary and permits a counts-and-path-only reply, so the exempt reply does not relay an Orca outage on an exit 0 run. The owner ruled FIN-F7 a documented limitation of Phase 1, not fixed in this run, with follow-up work specified. This is an accepted limitation, not a completed fix; the report at the printed path states the outage and the skill requires reading it first. Authorization: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:15-17. Severity medium (calibrator-supported): a user-visible silence during an Orca outage, accepted by the owner. The owner's recorded words are the executor's own recommended reply pasted back (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:11); authorization is real but not independent of the executor's recommendation.
- **Default remediation:** Make sure FIN-F7 is in the end-of-run follow-up issue with the ruling's fix list (the sweep exception in pragmatic.md at 7 sites, design-addendum.md lines 29 and 37, DESIGN 7.6 :663, skill steps 3 and 4 and their pins). Verify with `gh issue list --repo IronbellyOrg/IronClaude --search FIN-F7` (always with --repo IronbellyOrg/IronClaude) once the issue is filed.

### Deviation D-16 (F-16): HOW-WE-WORK says 'on every wake'; WC-16 says 'on every coordinator wake or wait timeout'

- **Location:** src/superclaude/core/HOW-WE-WORK.md:405, src/superclaude/core/WORKER-CONTRACT.md:277, docs/designs/orchestrator-mode.md:717, docs/designs/orchestrator-mode.md:680
- **Mapped tasklist item:** src/superclaude/core/HOW-WE-WORK.md: items ['1.4', '13.1', '13.2', '13.4', '13.8', '13.9', '13.10', '13.11']
- **Spec section:** DESIGN row R2 (:717) and WC-16 (:680)
- **Evidence:** "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes" (src/superclaude/core/HOW-WE-WORK.md:405); "On every coordinator wake or wait timeout, at most once every 5 minutes" (src/superclaude/core/WORKER-CONTRACT.md:277); "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes" (docs/designs/orchestrator-mode.md:717); "On every coordinator wake or wait timeout, at most once every 5 minutes" (docs/designs/orchestrator-mode.md:680)
- **Classification:** authorized (minor, confidence 0.8)
- **Classification rationale:** Each shipped text copies its DESIGN source word for word: the HOW-WE-WORK bullet is DESIGN row R2 (:717) and WC-16 is DESIGN :680. The wording gap comes from DESIGN itself. The narrower bullet points to WC-16 as the rule, so it does not contradict it. The plugin mirror has the same lines. Authorization: docs/designs/orchestrator-mode.md:717 (and docs/designs/orchestrator-mode.md:680). T1 lead DC-5 proposed Necessary; not adopted. Both texts copy DESIGN verbatim, so the class is Authorized, not Necessary. Open grounding gap carried: byte identity of the two HOW-WE-WORK files was only compared on the sweep lines.
- **Default remediation:** No change required. Optional: when the owner next edits DESIGN R2, add 'or wait timeout' to the HOW-WE-WORK bullet and its plugin copy and verify with `uv run pytest tests/commands/test_routing_plugin_parity.py tests/core/test_how_we_work_routing_table.py -q`.

### Deviation D-17 (F-17): Literal all-green validation was not achieved: three environment-caused test failures and twelve unchanged Markdown files in the format check

- **Location:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md:9-25, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2456, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2470
- **Mapped tasklist item:** unmapped to a diff file (task record or SPEC/DESIGN text)
- **Spec section:** Key Objective 6 (task file :89); item gates (task file :2456, :2470)
- **Evidence:** "3 failed, 25252 passed, 149 skipped, 2 xpassed" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md:9); ".venv/bin/python: No module named ruff" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md:22); "It passed when re-run alone" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md:23); "each recorded as pre-existing or environment-caused" (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md:25)
- **Classification:** necessary (medium, confidence 0.85)
- **Classification rationale:** The saved full run has 3 failed and 25252 passed. Two ruff tests fail because ruff is not an importable module in .venv (a system ruff is on PATH; pyproject pins ruff as a dev dependency this venv lacks), and one timing test failed under machine load and passes when run alone. None of them reads a file the diff changed. The format check also lists 12 Markdown files unchanged at base. The detailed completion gate allows documented failures not caused by the task, so this is qualified completion, not a pass of the full suite. Authorization: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2470. qualified completion, not a pass of the full suite. Environmental causes re-confirmed by the orchestrator (ruff missing from .venv; timing test passes alone, 6 passed on isolated re-run per the T1 card).
- **Default remediation:** Run `make install` so the dev dependency ruff is importable in .venv, then `uv run pytest tests/cli/eval/test_claude_process_adapter.py -k ruff -q` (both should pass), re-run `uv run pytest tests/hooks/test_launch_level_guard.py -k speed -q` on an idle machine, and state in the PR description that the full-suite result is 'qualified completion' with the three ids and causes. The 12 Markdown format-check files are a separate cleanup and are not this task's.

## Grounding Gaps

### Gap G-01

- **Hunk ref:** src/superclaude/cli/sweep/commands.py:214-245 and src/superclaude/cli/main.py:567-569
- **Evidence missing:** static reachability of the click group, the `run` command and the add_command registration cannot be decided from referrers (decorator, registry and packaging degrade oracle, runtime-surface.md section 3 a, b, c)
- **Why not classifiable:** runtime-surface DEGRADE is never UNREACHED and never Regression; supplementary real-entrypoint evidence (`uv run superclaude sweep --help` exit 0 listing `run`) shows the command is registered but not that `sweep run` publishes a report
- **Next evidence needed:** one real `superclaude sweep run` against a named Run (the task did this at item 9.3: artifacts/sweep-live-check-1.4.json); the auditor does not run it because it writes .dev/sweeps/

### Gap G-02

- **Hunk ref:** src/superclaude/cli/sweep/probes.py:298-322
- **Evidence missing:** reuse-auditor verdict mirror-shape, S_reuse 0.68, auggie unavailable (advisory cap)
- **Why not classifiable:** maybe-related, below rung L3
- **Next evidence needed:** none required; advisory

### Gap G-03

- **Hunk ref:** src/superclaude/cli/sweep/commands.py:153-208
- **Evidence missing:** reuse-auditor verdict extract-shared, S_reuse 0.70, auggie unavailable (advisory cap)
- **Why not classifiable:** maybe-related, below rung L3; the only shared atomic helper (src/superclaude/cli/swarm/atomic.py:14) overwrites
- **Next evidence needed:** none required; advisory

### Gap G-04

- **Hunk ref:** src/superclaude/cli/sweep/probes.py:377-402
- **Evidence missing:** reuse-auditor verdict mirror-shape, S_reuse 0.67, auggie unavailable (advisory cap)
- **Why not classifiable:** maybe-related, below rung L3
- **Next evidence needed:** none required; advisory

### Gap G-05

- **Hunk ref:** tests/cli/eval/test_claude_process_adapter.py (not in the diff)
- **Evidence missing:** pytest exit 1 on two tests that call `python -m ruff` in .venv (module absent); mapped to Grounding Gap, not Regression, by evidence (taxonomy: unmapped/unrelated exit)
- **Why not classifiable:** failure cause is the environment, no diff file is read by these tests
- **Next evidence needed:** install ruff in the project venv (pyproject.toml pins ruff==0.15.20 as a dev dependency) and re-run

### Gap G-06

- **Hunk ref:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md (item 14.49) and the git index
- **Evidence missing:** final staging outcome: at audit time the work unit holds untracked and staged-then-modified files; item 14.49 (`git add .dev/tasks`) is unfinished; end-of-run staging is approved (.dev/orca-command-refactor/decisions/APPROVED.md:20)
- **Why not classifiable:** a pending process step, not a deviation; the auditor's own audit/ files add to the untracked count
- **Next evidence needed:** after item 14.49, `git status --porcelain -- .dev/tasks` shows no `??` line and `git diff --cached --name-only | grep ^.claude/` prints nothing (the auditor verified the second check now: none staged)

### Gap G-07

- **Hunk ref:** src/superclaude/cli/sweep/probes.py:1192-1203
- **Evidence missing:** whether `orca worktree ps` lists worktrees of other repositories (git status would then run outside this checkout's worktrees)
- **Why not classifiable:** DESIGN :292 authorizes each distinct canonical path from worktree ps; Orca's scope was not captured
- **Next evidence needed:** a step 1.0a style capture of `worktree ps --json` on a host with two repositories

### Gap G-08

- **Hunk ref:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md:1071
- **Evidence missing:** which instruction wins when task item 7.16 restricts Run substitutions and DESIGN :995 requires the unknown-Run task-list error shape (the capture records the extra read as its own deviation)
- **Why not classifiable:** competing instructions, both documented
- **Next evidence needed:** owner ruling on instruction precedence, or confirmation that the capture's own deviation record is accepted

### Gap G-09

- **Hunk ref:** src/superclaude/output-styles/pragmatic.md:19-26 and src/superclaude/skills/sc-sweep-protocol/SKILL.md:35-41
- **Evidence missing:** adherence of the exempt reply to the five conditions was not checked condition by condition, and the interaction of inert Rule 5, the style exception and the exempt reply was not probed (invariant INV-013 UNVERIFIED)
- **Why not classifiable:** no behaviour evidence either way; the canonical tests prove instruction text only (task file :3101)
- **Next evidence needed:** compare the five conditions in pragmatic.md with SKILL.md steps 3-4 line by line, then reinstall the output style and run one real /sc:sweep

## Per-Task Verdicts

Per-phase roll-up of the 355-item tasklist (353 ticked; open: 14.48, which is this audit, and 14.49). The tasklist is far too large for one entry per item, so each entry covers a phase group and lists the findings that touch it.

### Task Phases 2-6 (design fixes R3-B1, R3-B2, R3-B3, R4, R5)

- **Status:** partial
- **Deviation class:** drift (highest of F-03)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-03 in merged-verdict.yaml

### Task Phase 7 (owner decisions, pre-implementation gates, pragmatic.md exception)

- **Status:** success
- **Deviation class:** authorized (highest of F-14)
- **Citations dropped:** 0
- **Per-task validation strength:** strong
- **Evidence anchor:** see F-14 in merged-verdict.yaml

### Task Phase 8 (core package: models, classify, probes)

- **Status:** regression
- **Deviation class:** regression (highest of F-01, F-04, F-05, F-06, F-07, F-10, F-11, F-13)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-01, F-04, F-05, F-06, F-07, F-10, F-11, F-13 in merged-verdict.yaml

### Task Phase 9 (CLI shell, commands.py, main.py registration)

- **Status:** partial
- **Deviation class:** drift (highest of F-09, F-12)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-09, F-12 in merged-verdict.yaml

### Task Phase 10 (sweep tests)

- **Status:** partial
- **Deviation class:** drift (highest of F-02, F-05)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-02, F-05 in merged-verdict.yaml

### Task Phase 11 (command and skill surface)

- **Status:** partial
- **Deviation class:** drift (highest of F-08, F-14)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-08, F-14 in merged-verdict.yaml

### Task Phase 12 (WC-16 and never-as-worker)

- **Status:** success
- **Deviation class:** authorized (highest of F-16)
- **Citations dropped:** 0
- **Per-task validation strength:** strong
- **Evidence anchor:** see F-16 in merged-verdict.yaml

### Task Phase 13 (routing and documentation rows R1-R8)

- **Status:** success
- **Deviation class:** authorized (highest of F-16)
- **Citations dropped:** 0
- **Per-task validation strength:** strong
- **Evidence anchor:** see F-16 in merged-verdict.yaml

### Task Phase 14 (final validation, gates, diff file)

- **Status:** partial
- **Deviation class:** necessary (highest of F-15, F-17)
- **Citations dropped:** 0
- **Per-task validation strength:** weak
- **Evidence anchor:** see F-15, F-17 in merged-verdict.yaml

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 122` = 0.02

## Recommendations

### Recommendation R-001: Subprocess output is fully buffered and checked after exit; SPEC requires Popen, chunked r

- **File:** src/superclaude/cli/sweep/probes.py
- **Change:** In src/superclaude/cli/sweep/probes.py replace the two subprocess.run seams (_orca at :257, _git at :308) by subprocess.Popen with stdout and stderr piped, chunked reads, and a kill of the child once combined output passes OUTPUT_LIMIT (8 MiB), returning call_failed 'output over 8 MiB' (and the _git equivalent).
- **Verifier:** Verify with a new test in tests/sweep/test_probes_allowlist.
- **Linked deviation(s):** D-01
- **Priority:** P0

### Recommendation R-002: NFR-007 'still publish' tests stop at report.render and never exercise publication

- **File:** tests/sweep/test_probes_allowlist.py
- **Change:** Add a test (tests/sweep/test_probes_allowlist.py or tests/sweep/test_cli_contract.py) that calls src/superclaude/cli/sweep/commands.py `_publish(text, output_dir, now)` (defined at commands.py:153), or invokes `sweep run` through click's CliRunner, under the same full-timeout fakes, and asserts the report file exists, ends with 'Report complete' and the JSON/exit code is success.
- **Verifier:** Verify with `uv run pytest tests/sweep/test_probes_allowlist.
- **Linked deviation(s):** D-02
- **Priority:** P1

### Recommendation R-003: Stale approval and blocking-status text in DESIGN and the task Open Questions

- **File:** docs/designs/orchestrator-mode.md
- **Change:** Edit .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3037-3043 so OQ-2..OQ-8 read RESOLVED with their decision-record paths (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-2-GQ-10-report-location-decision.md, OQ-3-GQ-11-rule-id-decision.md, OQ-4-GQ-35-409-pin-decision.md, OQ-5-GQ-61-window-decision.md, OQ-6-GQ-63-done-next-decision.md, OQ-7-D9-signoff-decision.md, OQ-8-run-id-decision.md), and update docs/designs/orchestrator-mode.md lines 5-11 (approval of WC-16 recorded, review status reflects the closed R3-B1..R3-B3 gates).
- **Verifier:** Verify with `grep -n PENDING <task file>` returning no OQ-2.
- **Linked deviation(s):** D-03
- **Priority:** P1

### Recommendation R-004: Worker-list rows with a missing or empty dispatchId are dropped from rows and invisible to

- **File:** src/superclaude/cli/sweep/classify.py
- **Change:** In src/superclaude/cli/sweep/classify.py `_origin_unknown` (:678-708) treat any unscanned source row whose name starts with 'orca worker-list <run> row ' as an incomplete list for that run (set failed = True, adding NOTE_ORIGIN_CALL_FAILED), then add a test in tests/sweep/test_classify.py (and a probes-side case in tests/sweep/test_probes_allowlist.py) for a Run whose worker-list rows ALL lack a valid dispatchId: the unjoined transcript must be person_started None with an 'origin unknown:' note, never True or Historical.
- **Verifier:** Verify with `uv run pytest tests/sweep/test_classify.
- **Linked deviation(s):** D-04
- **Priority:** P1

### Recommendation R-005: A ledger over the limit is searched in the tail only; the head is never read and the test 

- **File:** tests/sweep/test_probes_allowlist.py
- **Change:** Either read the head in src/superclaude/cli/sweep/probes.py `_ledger_has_final` (open the file, read LEDGER_SPLIT bytes from offset 0 as well as the tail) or amend DESIGN GQ-105 (docs/designs/orchestrator-mode.md:62, :398, :548, :760) and SPEC line 295 to say tail only; in both cases rename tests/sweep/test_probes_allowlist.py `test_ledger_over_the_limit_is_read_as_head_and_tail` to match what it asserts (for example `..._is_searched_in_the_tail`).
- **Verifier:** Verify with `uv run pytest tests/sweep/test_probes_allowlist.
- **Linked deviation(s):** D-05
- **Priority:** P2

### Recommendation R-006: _git over-limit reason prints bytes instead of 8 MiB, is pinned by a test, and never reach

- **File:** tests/sweep/test_probes_allowlist.py
- **Change:** Change src/superclaude/cli/sweep/probes.py:316 to f"output over {OUTPUT_LIMIT // _MIB} MiB" and update the pin at tests/sweep/test_probes_allowlist.py:1454 to the MiB form.
- **Verifier:** Verify with `uv run pytest tests/sweep/test_probes_allowlist.
- **Linked deviation(s):** D-06
- **Priority:** P2

### Recommendation R-007: Third per-Run source row and extra model fields beyond DESIGN 7.2 and 7.4

- **File:** docs/designs/orchestrator-mode.md
- **Change:** Record the additions in DESIGN 7.2 and 7.4 (the third source row name 'orca task-list --ready <run>', share_shows(wanted), ContractRecord.mtime, SessionRow.freshness_age_s, the four constants) through an owner-approved DESIGN edit or a section 13 row, or add a one-line code comment pointing at the task finding that records each.
- **Verifier:** Verify with `grep -n 'task-list --ready' docs/designs/orchestrator-mode.
- **Linked deviation(s):** D-07
- **Priority:** P2

### Recommendation R-008: The skill says to print 'the standard error line' on exit 1 or 2, but the command can emit

- **File:** src/superclaude/skills/sc-sweep-protocol/SKILL.md
- **Change:** Edit src/superclaude/skills/sc-sweep-protocol/SKILL.md step 5 to 'print the whole standard error exactly as it came' (every line), mirror it to the plugin copy if one exists, and update the pinned sentence at tests/commands/test_sweep_command.py:446.
- **Verifier:** `uv run pytest tests/commands/test_sweep_command.py -q`
- **Linked deviation(s):** D-08
- **Priority:** P2

### Recommendation R-009: Structural debt: the XDG state folder is computed in two places, and two public wrappers h

- **File:** src/superclaude/cli/sweep/
- **Change:** Add one helper (for example probes.state_dir()) used by both commands.py:253 and probes.py:1253, and either call read_ledger/read_worktree from collect or point their tests at the helpers collect uses.
- **Verifier:** Verify with `grep -n XDG_STATE_HOME src/superclaude/cli/sweep/*.
- **Linked deviation(s):** D-09
- **Priority:** P2

### Recommendation R-010: git status in an Orca-listed worktree can run that worktree's core.fsmonitor command or st

- **File:** tests/sweep/test_readonly.py
- **Change:** In src/superclaude/cli/sweep/probes.py `_git` (:305) add '-c', 'core.fsmonitor=false' after '-C', str(cwd) and pass stdin=subprocess.DEVNULL at :308.
- **Verifier:** Verify with `uv run pytest tests/sweep/test_readonly.
- **Linked deviation(s):** D-10
- **Priority:** P2

### Recommendation R-011: Contract and ledger readers accept non-regular files: a FIFO blocks the run and defeats th

- **File:** tests/sweep/test_probes_allowlist.py
- **Change:** In src/superclaude/cli/sweep/probes.py `_ledger_has_final` (:557), the contract reader (:714-720), check stat.S_ISREG(os.stat(path).st_mode) before open() and return the existing unscanned reason (for example 'not a regular file').
- **Verifier:** Verify with a new test in tests/sweep/test_probes_allowlist.
- **Linked deviation(s):** D-11
- **Priority:** P2

### Recommendation R-012: JSON report_path and worktree paths go through the Markdown sanitizer; a path containing [

- **File:** src/superclaude/cli/sweep/report.py
- **Change:** In src/superclaude/cli/sweep/report.py `to_json` emit report_path and worktree paths as plain strings (str(report_path), str(w.path)) and keep sanitize() for Markdown cells only.
- **Verifier:** Verify with a new test in tests/sweep/test_report.
- **Linked deviation(s):** D-12
- **Priority:** P2

### Recommendation R-013: The exempt chat reply omits the Orca outage warning under an explicitly accepted limitatio

- **File:** n/a
- **Change:** Make sure FIN-F7 is in the end-of-run follow-up issue with the ruling's fix list (the sweep exception in pragmatic.md at 7 sites, design-addendum.md lines 29 and 37, DESIGN 7.6 :663, skill steps 3 and 4 and their pins).
- **Verifier:** Verify with `gh issue list --repo IronbellyOrg/IronClaude --search FIN-F7` (always with --repo IronbellyOrg/IronClaude) once the issue is filed.
- **Linked deviation(s):** D-15
- **Priority:** P2

### Recommendation R-014: Literal all-green validation was not achieved: three environment-caused test failures and 

- **File:** tests/cli/eval/test_claude_process_adapter.py
- **Change:** Run `make install` so the dev dependency ruff is importable in .venv, then `uv run pytest tests/cli/eval/test_claude_process_adapter.py -k ruff -q` (both should pass), re-run `uv run pytest tests/hooks/test_launch_level_guard.py -k speed -q` on an idle machine, and state in the PR description that the full-suite result is 'qualified completion' with the three ids and causes.
- **Verifier:** `uv run pytest tests/cli/eval/test_claude_process_adapter.py -k ruff -q`
- **Linked deviation(s):** D-17
- **Priority:** P2

## Remediation (Tier 3, Wave 6)

- `remediation_offered: true`, `remediation_accepted: null`, route: MDTM (`--remediate --depth deep`).
- Not run: the Tier 3 chain needs the user's yes or no ("Proceed with task-builder?") and this run is a non-interactive worker with no user on the line. A message from the coordinating session is not the user's answer. Nothing was authored, no handoff memory file was written, `remediation_task_path: null`, `remediation_plan_path: null`.
- Eligible for remediation: 1 Regression-class item (D-01) and 11 Drift-class items (D-02 to D-12). `needs_human_decision: true`.
- To proceed, the user answers yes and the coordinator runs the route in `refs/remediation-handoff.md` (task-builder builds the MDTM task, the user runs `/task <path>`). Reflect never runs `/task` itself.

## Open Questions

- Appended to the task file: the Authorized and Necessary items and the minor notes only (see the end of this run).
- Escalated to the user, not logged: D-01 (class and fix), D-04 (escalation condition: a live capture of worker rows without a dispatchId), D-03 (reconcile stale approval text), the other unauthorized Drift items D-02 and D-05 to D-12, and Grounding Gap G-08 (instruction precedence for the unknown-Run capture).
