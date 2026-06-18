# QA Report — task-qualitative (operational-correctness lens)

**Topic:** TASK-RF-429-recovery-20260615-040144 — 6-phase 429/account-exhaustion recovery
**Date:** 2026-06-15
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: FAIL (1 MINOR finding — see Issues Found)

Net assessment: the task is operationally sound and would execute to a working
implementation. Every load-bearing insertion point, call-site, signature, config
seam, test anchor, and the human-decision/POST-reflect machinery were verified
against current source and match. ONE MINOR drift was found (a stale test-class
NAME in a "read X to mirror it" item) that does not block execution. Per the
rf-qa-qualitative any-issue→FAIL rule, the verdict is FAIL pending that one
correction, but there are zero CRITICAL or IMPORTANT defects.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (every phase runs ruff format --check AND verify-sync AND pytest; none run only `make lint`) | none | PASS | P1 Step2.6 / P2 3.5 / P3 4.8 / P4 5.5 / P5 6.6 / P6 7.4 each have 3 validation items: `uv run pytest …`, `uv run ruff format --check src/ tests/` + `ruff check`, `make verify-sync`. None gated on `make lint` alone. |
| 2 | Project-convention compliance (SoT: edits target src/, never .claude/; verify-sync each phase) | none | PASS | All code edits target `src/superclaude/cli/sprint/*`; docs target `docs/guides/…`; template/KNOWLEDGE at repo root. No `.claude/` edit. Each phase asserts verify-sync exits 0. |
| 3 | Intra-phase execution order (P1 detector core before P2 classifier import; P2 enum before P3 ladder; loop skeleton before dispatch) | none | PASS | Phase deps stated P2←P1, P3←P1+P2, P4 reuses P3 loop, P5 wires P2/P3, P6 emits for P3/P4. Sub-items split "skeleton" then "dispatch" in correct order (Steps 4.3, 5.2). |
| 4 | Function-signature verification (insertion points match real code) | none | PASS | All cited lines verified — see Source-Verification Matrix below. |
| 5 | Module-context analysis (mirror detect_error_max_turns / _classify_transcript / HandoffRecord.from_dict / write_task_complete idioms) | none | PASS | monitor.py detect_error_max_turns 37-61 (OSError-tolerant read); _classify_transcript last-result-overwrite loop 555-574; HandoffRecord.from_dict `.get()` 337-349; logging `_jsonl` lock 299. All mirror targets exist as cited. |
| 6 | Downstream-consumer analysis (failure_class persisted → read by resume/rerun/halt-UX; new TaskResult fields serialized both directions) | none | PASS | to_dict 198-216 + from_dict 218-240 both updated (Steps 3.2); failure_class flows task_results→PhaseResult (executor 1763)→_write_phase_result_json (2691 `task_results`); derivation reads tr.failure_class (1752-1778). aggregate_task_results does not drop TaskResults. |
| 7 | Test validity (scripted factory writes the path the ladder reads; not stubs) | none | PASS | Step 4.7 factory writes `config.task_output_file(phase, task)` — the exact path executor.py:998 reads via `detect_provider_failure(task_output_path)`. Single-session test (5.4) writes `config.output_file(phase)` — the path the single-session loop reads. Both seams real. |
| 8 | Test coverage of primary use case (full re-spawn loop end-to-end via factory) | none | PASS | 7 executor scenarios drive the real loop: single→clean (PASS, resets=1), cooldown-attempt-1 (fast halt, 0 extra), single×cap (halt + persisted halt_reason), single→real-failure (FAIL_TERMINAL), K>1 latch storm, always-429 K=1 cap. |
| 9 | Error-path coverage (torn transcript → NONE; None-safe suggester; no-fabricated-alias halt UX) | none | PASS | detect_provider_failure FileNotFoundError/OSError→NONE + empty-guard (Step 2.4 mirrors 46-52); suggest_alternate_model returns None when no distinct alt (Step 6.1/6.5); halt-UX None-suggested degrades without `--model` (Step 6.2). |
| 10 | Runtime failure-path trace (429 in → detector → policy → status → persistence → halt-UX; no downstream gate breaks) | none | PASS | Data flow holds: per-task path collapses to PhaseStatus.ERROR (1756, FAIL_PROVIDER_EXHAUSTED not in tasks_passed/FAIL_TERMINAL counts at 354/356) → halt_reason derived from per-task failure_class. Single-session short-circuits to PROVIDER_EXHAUSTED before _determine_phase_status (1993). is_failure-gate diagnostic bundle (2103) skipped because PROVIDER_EXHAUSTED ∉ is_failure. |
| 11 | Completion-scope honesty (OQ-1/OQ-2 open questions resolved via PENDING+default, not ignored) | none | PASS | Step 6.1 (OQ-1) writes PENDING + ships option-A os.environ reader, documents option-B not-shipped. Step 7.2 (OQ-2) ships option-(a) filter + PENDING-fallback to live-auto-path. Both honor halt-not-auto-default. |
| 12 | Ambient-dependency completeness (imports, 4-hop flag chain, marker registration, both call sites threaded) | none | PASS | --max-session-resets 4-hop chain verified end-to-end (commands→config→SprintConfig→policy). reset_policy threaded at BOTH K>1 (1134-1145 lock=lock) and K=1 (1337-1348 lock=None). `backward_compat` marker registered (pyproject:131, strict-markers on). |
| 13 | Kwarg sequencing (signature param before kwarg pass; loop skeleton before dispatch) | none | PASS | Step 4.3 adds `reset_policy` param to _run_one_task signature BEFORE Step 4.4 threads it at call sites. Loop-skeleton sub-item precedes detector-dispatch sub-item (4.3, 5.2). |
| 14 | Function-existence claims grep-verified (NO DriftNominator; output_file vs task_output_file both exist) | none | PASS | recovery.py has Nominator(143)/ManualNominator(149)/ReflectReportNominator(164), NO DriftNominator (task correctly notes this). output_file (models:687, 1 arg) and task_output_file (models:693, 2 args) both exist — the single-session vs per-task discriminator is real. |
| 15 | Cross-reference accuracy for templates/anchors (every "read X to mirror" anchor exists) | AX-1 | FAIL | Step 3.4 item-1 cites "existing `TestTaskStatus`/membership tests … (around lines 35-123)" but the class at test_models.py:35-123 is named `TestPhaseStatus`, not `TestTaskStatus`. No class named `TestTaskStatus` exists. Stale citation drift (the membership-test STRUCTURE to mirror does exist in that range). All other anchors verified — see matrix. |

<!-- task-qualitative phase: Axis column populated per PR-07. `none` = five-axis
lens applied, nothing fired. AX-1 (drift) fired on item 15. BUILD_REQUEST.GOAL
verbatim ("Implement the 6-phase 429/account-exhaustion recovery design in
src/superclaude/cli/sprint/") was supplied in the spawn prompt TRACK GOAL, so
AX-1 drift axis is ACTIVE (no drift-axis-inactive annotation needed). -->

---

## Source-Verification Matrix (every cited insertion point read against current source)

| Task citation | Current source | Match |
|---|---|---|
| monitor.py detect_error_max_turns 37-61 | def at 37, OSError guard 46-52, regex 33-34 | EXACT |
| monitor.py count_turns→OutputMonitor zone (~250/253) | count ends 250, `class OutputMonitor` at 253 | EXACT |
| monitor.py _process_chunk json.loads (~389) | `json.loads(line)` try/except at 388-394 | EXACT |
| models.py TaskStatus 46-66, is_failure 60-66 | TaskStatus 46-66, is_failure tuple 61-66 | EXACT |
| models.py TaskResult last field output_path (~188) | `output_path: str = ""` at 188 | EXACT |
| models.py to_dict 190-216 / from_dict HARD-KEYED 218-240 | to_dict 198-216, from_dict hard-keyed `data["status"]`… 218-240 | EXACT (hard-keyed confirmed) |
| models.py HandoffRecord.from_dict `.get()` 337-349 | `.get()` style 337-350 | EXACT |
| models.py PhaseStatus is_terminal 409-423 / is_success 425-434 / is_failure 436-443 | confirmed; HALT/TIMEOUT/ERROR in BOTH terminal+failure | EXACT |
| models.py PhaseResult recovery_history (~729-753) | dataclass 728, recovery_history 753 | EXACT |
| models.py build_resume_output 1017-1071, resume cmd ~1050, ShadowGateMetrics ~1074 | def 1017, resume cmd 1050, ShadowGateMetrics 1075 | EXACT |
| models.py SprintConfig model ~537 / task_parallelism ~590 / index_path | model 537, task_parallelism 590, index_path 531 | EXACT |
| models.py output_file / task_output_file / phase_result_json | 687 / 693 / 714 | EXACT |
| rerun_tasks.py _classify_transcript 547-593, is_error @580, ladder 582-591 | def 547, is_error 580, ladder 582-593 | EXACT |
| rerun_tasks.py nominate({}) sites 1419/1421/1433, select_default ~1426 | 1419/1421/1433, select_default call 1423-1425 | EXACT |
| rerun_tasks.py select_default_recoverable_tasks(Path) | def at 1134 (reads phase_result_json) | EXACT |
| executor.py _run_one_task subprocess_factory 986-993 | factory branch 986-993 | EXACT |
| executor.py status ladder :1003 (PASS_RECOVERED) / :1012 (_is_transient) / TaskResult 1027-1035 | detect_error_max_turns 1003, _is_transient 1012, TaskResult 1027-1035 | EXACT |
| executor.py K>1 call site 1134-1145 (lock=lock) | _run_one_task call with lock=lock 1134-1145 | EXACT |
| executor.py K=1 call site 1337-1348 (lock=None) | _run_one_task call with lock=None 1337-1348 | EXACT |
| executor.py single-session spawn ~1815 / _determine_phase_status ~1993 | ClaudeProcess 1815, _determine_phase_status call 1993 (def 2751) | EXACT |
| executor.py per-task completion 1752-1781, _write_phase_result_json ~1778 | aggregate 1752, PhaseResult 1757, _write 1778 | EXACT |
| executor.py is_failure diagnostic bundle 2103-2132 | `if status.is_failure:` 2103, bundle 2104-2128, HALTED+break 2130-2132 | EXACT |
| executor.py _write_phase_result_json 2657-2701, payload ~2685-2696 | def 2657, payload 2685-2696 | EXACT |
| commands.py --task-parallelism 202-209 / run() 234-258 / load_sprint_config 337-354 | option 203-204, run 234, param 255, loader call 337, pass 353 | EXACT |
| config.py load_sprint_config 281-298, task_parallelism ~297, SprintConfig(…) ~355-369 | def 281, param 297, SprintConfig 347, pass 368 | EXACT (construct at 347 vs cited 355; pass-through 368 in range) |
| recovery.py Nominator 143 / ManualNominator 149 / ReflectReportNominator 164 (no DriftNominator) | EXACT; no DriftNominator | EXACT |
| logging_.py _jsonl 295-301 (lock), write_task_complete 226-249 | _jsonl 295 + lock 299, write_task_complete 226 | EXACT |
| swarm/config.py T2_MODEL_ENV_PREFIX/T2_MODEL_MAX_SLOTS/_collect_t2_models 57-185 | 57 / 63 / 179 | EXACT |
| scripts/ic ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL | confirmed 61-63 | EXACT |
| test anchors: TestDetectErrorMaxTurns 137; TestPerTaskOrchestration 601; test_execute_sprint_halt 383; TestResumePlanner+helpers 64/71/82/88/100; test_discover_failed_tasks_via_is_error 280; test_resume_command_when_halted 367; test_run_help 31; reflect parity parents[3] | all exist as cited | EXACT (except TestTaskStatus name — see item 15) |
| frontmatter start_commit 59b9e2a2b9f0 == HEAD | HEAD 59b9e2a2 | EXACT |
| pyproject backward_compat marker | registered line 131, strict-markers on | EXACT |

---

## Spawn-Prompt Targeted Concerns (1-7) — Verdicts

1. **Cited insertion points still match real code?** YES — every cited executor.py
   line (986-993/1003/1012/1134-1145/1337-1348/1815/1993/2103-2132/2657-2701),
   models.py line (46-66/218-240/411-423), rerun_tasks.py (547-593/1419-1433),
   and the monitor detector zone were Read and match. The task ALSO defensively
   instructs the executor to "locate by symbol, not line, since discovery may have
   drifted" (Steps 4.3, 4.4, 5.2) — drift-resilient by design. **No item flagged
   as won't-apply-cleanly.**

2. **Per-phase validation correct & sufficient?** YES — all six code-edit phases
   run `uv run ruff format --check src/ tests/` (the CI-separate format gate) AND
   `make verify-sync` AND `uv run pytest tests/sprint/…`. **No phase runs only
   `make lint`** (the trap the prompt flags). Final PC.2 also runs full-suite +
   `ruff format --check` + `ruff check`.

3. **6 executor factory scenarios exercise the loop, and storm bound realistic?**
   YES — `_make_scripted_factory` writes the per-attempt transcript to
   `config.task_output_file(phase, task)` (exactly the path the status ladder
   reads via `detect_provider_failure(task_output_path)` at executor:998/1003),
   and a call counter observes every re-spawn. The K>1 storm-bound assertion is the
   realistic `cap <= total <= cap+(K−1)` AND `total < K×cap` — NOT the over-strict
   `<= cap` (Step 4.7 row 5 explicitly calls out the trap). **Correct.**

4. **Back-compat round-trip targets hard-keyed TaskResult.from_dict?** YES — Step
   3.4 item-2's `test_taskresult_from_dict_old_payload_round_trips` builds an OLD
   dict with no new keys and asserts `TaskResult.from_dict(old)` does not raise.
   Confirmed against source: `TaskResult.from_dict` (218-240) is hard-keyed today
   (`data["status"]`, `data["turns_consumed"]`…), so the test WOULD fail pre-fix
   and pass after the `.get()` migration (Step 3.2 item-3). **Correctly targeted.**

5. **needs_human_decision items (OQ-1 aienv, OQ-2 nominator) PENDING+default,
   never silently ship the alternative?** YES — Step 6.1 (OQ-1) ships option-A
   (os.environ reader, the documented default), documents option-B (file-parser)
   as not-shipped, writes a PENDING note. Step 7.2 (OQ-2) ships option-(a) filter
   in `select_default_recoverable_tasks` with a documented PENDING-fallback to the
   live-auto-path if option-(a) proves non-trivial. Both honor
   `feedback_human_decision_items_must_halt`. **Compliant.**

6. **POST-reflect wrapper preconditions hold?** YES — Step PC.5 does `git add -A`
   BEFORE the shell-out (working tree auditable), guards on
   `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` ( `if [ "${…:-0}" = "1" ]; then … exit 0; fi`
   recursion-breaker), consumes the EXIT CODE (only 0 proceeds; 10/11/2 FAIL→Blocked),
   emits no `--base`/`--reflect`/`--max-turns`/range (wrapper resolves base from
   frontmatter `start_commit`), and does NOT hand-author `reflect_post`. The
   frontmatter `start_commit: "59b9e2a2b9f0"` matches HEAD `59b9e2a2`. It is a
   SINGLE Bash command (no heredoc/multi-line-paste hazard). **Preconditions hold.**

7. **Any verification step exercising a stub instead of the real artifact?** NO —
   all verification steps drive real artifacts: the detector tests load the 6 real
   fixtures + the path wrapper; the executor scenarios drive the real re-spawn loop
   via the factory seam writing the real output path; the resume test runs the real
   `ResumePlanner().plan`; the parity test reads the real guide + real Click group;
   the help test invokes the real `CliRunner`; the no-diagnostic-bundle test checks
   the real filesystem. The task itself bans stub-tests (Step 2.5 item-8 requires
   the subtype-trap test to FAIL against a naive detector; multiple "would FAIL
   against pre-fix" RED→GREEN assertions). **No stub exercised.**

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Task Step 3.4, item 1 (task file line 267) | Stale anchor NAME: item says "Read the existing `TestTaskStatus`/membership tests in `tests/sprint/test_models.py` (around lines 35-123)" but the class at test_models.py:35-123 is named `TestPhaseStatus`, not `TestTaskStatus`; no class named `TestTaskStatus` exists in the file. The *membership-test structure* to mirror (parametrized `is_terminal`/`is_success`/`is_failure` tests) DOES exist in that range, so the executor can still complete the item — it will add new `TaskStatus.FAIL_PROVIDER_EXHAUSTED` membership assertions mirroring the existing pattern. Non-blocking; an executing agent reading the file will find `TestPhaseStatus` and adapt. | Change "existing `TestTaskStatus`/membership tests" to "existing `TestPhaseStatus`/membership tests" (or "the parametrized membership tests in `TestPhaseStatus`") so the cited anchor name matches the real class. The line range (35-123) is correct. |

No CRITICAL or IMPORTANT issues found.

---

## Actions Taken
fix_authorization is **false** — no files modified. Issue documented for the
serialized fixer / task author. (Even were fixing authorized, this finding is
in-scope: Step 3.4 is a checklist item that targets `tests/sprint/test_models.py`,
which is referenced by the task.)

---

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa structural PASS items I relied on (skipped re-checking):**
- Relied on the Inherited Structural Verdict's A.10 B2 self-containment + phase-structure PASS — did NOT re-verify section numbering, frontmatter shape, B2 component presence, or TB-Add structural checks.
- Relied on the verdict's claim that the 4 initial FAILs (XL items 4.3/5.2 split, line-fragility, Step 5.3 false-fork, EC-block file:line) were FIXED — did NOT re-audit the XL-split mechanics or EC-block citation shape as a structural matter.
- Relied on A.10.25 research-alignment PASS (0 gaps) — did NOT re-run research-to-item gap analysis.

**(b) Independent semantic checks where structural PASS was insufficient and my own source-reading was required (≥1, INV-019):**
- **Step 5.3 false-fork — semantic re-read.** Structural PASS only says the fork was "fixed." I Read the current Step 5.3 text (task line 447) AND executor.py:2103-2132 to confirm the fix is *semantically* correct: the item now frames the is_terminal-not-is_failure choice as a FIXED DEFAULT with a documented fallback contingency (not a runtime/build-time fork), and I verified `PhaseStatus.PROVIDER_EXHAUSTED` ∉ `is_failure` (models.py:436-443) genuinely makes `if status.is_failure:` (2103) skip the bundle. Tool evidence: Read models.py:424-443 + executor.py:2095-2132.
- **Insertion-point liveness — semantic re-read.** Structural PASS does not certify that the cited line numbers still match HEAD. I independently Read every cited insertion point (executor 986-993/1003/1012/1134-1145/1337-1348/1815/1993/1752-1781/2103-2132/2657-2701; models 46-66/188/218-240/337-349/409-443/728-753/687-714; rerun_tasks 547-593/1134/1419-1433; recovery 143-164; commands/config/logging via grep) and built the Source-Verification Matrix above. All EXACT. Tool evidence: 9 Read calls + 4 Bash/grep calls.
- **Single-session vs per-task output discriminator — semantic re-read.** The task's load-bearing claim "single-session uses `output_file`, NOT `task_output_file`" is a semantic correctness claim structural QA does not check. I grep-verified both methods exist with the right arities (models.py:687 output_file/1-arg; 693 task_output_file/2-arg) and that executor:998 uses task_output_file on the per-task path. Tool evidence: Bash grep + Read executor 980-1045.

---

## Confidence

**Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

(15 checklist items, all VERIFIED with tool evidence; 14 PASS, 1 FAIL.
confidence = 15/(15−0) × 100 = 100%.)

**Tool engagement:** Read: 12 | Grep: 0 | Glob: 0 | Bash: 5

(Tool calls: 12 Read = task file pages ×5, monitor.py ×2, models.py ×3, rerun_tasks.py ×2, executor.py ×5 [several Reads batched], report re-read ×1 — plus 5 Bash grep batches covering commands/config/logging/swarm/ic/tests/git/markers. Total tool calls (17) ≥ 15 checklist items, so the engagement-minimum is satisfied: every check maps to a specific source read, not padding.)

**Unchecked items:** none.
**Unverifiable items:** none.

---

## Recommendations
1. Apply Issue #1 (rename the stale `TestTaskStatus` anchor to `TestPhaseStatus`
   in Step 3.4 item-1). One-token edit; the line range is already correct.
2. No other action required. The task is operationally executable as written —
   all insertion points, call-sites, signatures, the 4-hop flag chain, the
   single-session/per-task output discriminator, the storm-bound assertion, the
   back-compat round-trip target, the OQ-1/OQ-2 PENDING discipline, and the
   POST-reflect wrapper preconditions are all correct against current source.

## VERDICT: FAIL

1 MINOR finding (stale test-class anchor name in Step 3.4 item-1). Zero CRITICAL,
zero IMPORTANT. Per the rf-qa-qualitative any-issue→FAIL rule the gate is FAIL
until Issue #1 is corrected; operationally the task would still execute to a
working implementation even unfixed (an agent reading the file finds the real
`TestPhaseStatus` class and adapts).

## QA Complete
