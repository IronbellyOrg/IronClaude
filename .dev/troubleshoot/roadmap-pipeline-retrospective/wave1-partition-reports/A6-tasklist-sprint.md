# A6 — Tasklist + Sprint Partition Retrospective

**Partition:** Downstream integration — roadmap → tasklist → sprint hand-offs
**Directories mined:**
- `/config/workspace/IronClaude/.dev/releases/complete/v2.07-tasklist-v1/`
- `/config/workspace/IronClaude/.dev/releases/complete/v2.05-sprint-cli-specification/`
- `/config/workspace/IronClaude/.dev/releases/complete/cliEval/`

**Auggie cross-reference target:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli` (sprint/executor.py, sprint/models.py, sprint/monitor.py)

---

## Findings

### F-A6-001: PARTIAL phase status silently promoted to PASS

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor — phase status determination, downstream consumer of tasklist output)
- **Symptom:** During the v2.07-tasklist-v1 sprint execution, Phase 3 of the 39-task tasklist produced a result file with `status: PARTIAL` (8/9 tasks passed, T03.08 was a STRICT failure). The Claude agent also wrote `EXIT_RECOMMENDATION: CONTINUE`. The sprint runner's `_determine_phase_status()` checked for `EXIT_RECOMMENDATION: CONTINUE` before checking for `status: PARTIAL`, so the phase was classified as PASS in the JSONL telemetry. The retrospective calls this a "telemetry lie."
- **Root cause (claimed):** Ordering bug in `_determine_phase_status()` in `executor.py` (lines 307-352 at the time of the retrospective). CONTINUE token wins over PARTIAL because the dispatch chain inspects EXIT_RECOMMENDATION first.
- **Remediation applied:** Recommendation drafted (P0 IMP-001) — introduce `PhaseStatus.PARTIAL` enum value classified as `is_success = True` (so sprint continues) but distinct in telemetry. Re-order parsing logic to check PARTIAL before CONTINUE. No commit reference in the retrospective; the recommendation is open in the prioritized improvement backlog.
- **Outcome:** Open. The fix was prioritized P0 but the retrospective documents it as a recommendation, not a landed change.
- **Still possible today (Auggie check):** **YES.** `src/superclaude/cli/sprint/executor.py:2125-2137` shows the exact same ordering bug. The branch `has_continue = "EXIT_RECOMMENDATION: CONTINUE" in upper` returns `PhaseStatus.PASS` at line 2130 *before* the regex check for `status: PARTIAL` at line 2136. `src/superclaude/cli/sprint/models.py:211-222` shows the `PhaseStatus` enum contains PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, PASS_MISSING_CHECKPOINT, HALT, TIMEOUT, ERROR, INCOMPLETE, PENDING, RUNNING, SKIPPED — **but no PARTIAL value was ever added.** The v2.07 P0 remediation has not been implemented.
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §1.1, §3.4 (lines 17-49, 270-286)

### F-A6-002: files_changed always 0 in JSONL — regex extraction misses stream-json structured events

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint monitor — sidecar signal extraction)
- **Symptom:** Every phase JSONL entry in v2.07 sprint and every cliEval sprint phase records `"files_changed": 0`. v2.07 Phase 1 created 6 files, Phase 2 modified/created 6 files, Phase 3 ran `make sync-dev` syncing dozens. cliEval phases 4 and 5 also show 0. The execution log is unreliable as a "what changed" signal.
- **Root cause (claimed):** `FILES_CHANGED_PATTERN` regex in `monitor.py` line 28 looks for prose patterns like `modified foo.py` or `created bar.js`. But `claude --print --output-format stream-json` emits structured NDJSON `tool_use` events with file paths in JSON fields (e.g., `event.input.file_path`), not in prose. The regex never fires.
- **Remediation applied:** Recommendation drafted (P1 IMP-002) to add structured extraction for `Write`, `Edit`, `MultiEdit` tool_use events, keeping the regex as fallback. No commit reference.
- **Outcome:** Open. cliEval JSONL from 2026-05-20/21 still shows `"files_changed": 0` on every phase including phase 4 (CLI surface, where many files are written) — confirming the bug persisted at least to May 2026.
- **Still possible today (Auggie check):** **YES.** `src/superclaude/cli/sprint/monitor.py:556-570` shows the regex-only extraction is still the only `files_changed` accumulator. `tool_matches = TOOL_PATTERN.findall(text)` and `file_matches = FILES_CHANGED_PATTERN.findall(text)` operate on text fallback; there is no structured `tool_use` extractor that pulls `input.file_path` from JSON events. The structured `_extract_signals_from_event` path (line 398) does not populate `_seen_files`.
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §1.2 (lines 52-72), `cliEval/execution-log.jsonl` (all phase_complete events show `files_changed: 0`)

### F-A6-003: last_task_id matches cross-phase backreferences via greedy regex

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint monitor — task ID extraction)
- **Symptom:** v2.07 Phase 4 JSONL records `"last_task_id": "T03.08"` — a task ID from Phase 3. Phase 4 tasks are T04.01-T04.10, so this is structurally wrong. The Phase 4 result file textually referenced T03.08 (a pre-existing failure being discussed in the inherited-issues section), and the regex `T\d{2}\.\d{2}` greedily matched it as the "last" task ID.
- **Root cause (claimed):** `TASK_ID_PATTERN` regex in monitor accepts any `T##.##` token regardless of phase context. It takes the last match per polling chunk; backward references to earlier phases beat actual current-phase tasks.
- **Remediation applied:** Recommendation drafted (P2 IMP-006) — phase-scoped filtering: pass `phase.number` to the monitor on reset and only accept IDs where the phase prefix matches. No commit reference.
- **Outcome:** Open. cliEval JSONL is even worse — every phase records `"last_task_id": ""` (empty string), suggesting either (a) the regex now matches nothing in the stream-json output or (b) the reset clears it but extraction never re-populates. Either way the field is uninformative.
- **Still possible today (Auggie check):** **YES.** Auggie did not surface a phase-aware filter in `sprint/monitor.py`. The fact that every cliEval phase records empty `last_task_id` rather than incorrect cross-phase IDs suggests the failure mode shifted from "wrong ID" to "no ID at all" when output-format changed to stream-json — which is the same class of brittleness (text-regex against structured output).
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §1.3 (lines 75-90), `cliEval/execution-log.jsonl` lines 3,5,7,9,11,13,20,22

### F-A6-004: JSONL has phase-grain only — no per-task observability

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint logger — telemetry granularity)
- **Symptom:** v2.07 sprint executed 39 tasks across 4 phases. The JSONL contains 4 `phase_complete` events. To know which task failed (T03.08) the operator had to open the phase-3 result markdown by hand. Automated dashboards cannot detect partial failures or per-task durations from JSONL alone.
- **Root cause (claimed):** No `task_complete` event emitter. Result-file per-task tables are not parsed into JSONL.
- **Remediation applied:** Recommendation drafted (P2 IMP-007) — parse result file per-task tables after phase completion, emit `task_complete` events with `{phase, task_id, status, tier, title}`. No commit reference.
- **Outcome:** Open. cliEval JSONL still shows only phase-level events.
- **Still possible today (Auggie check):** **YES.** Auggie's view of `sprint/executor.py` and `sprint/monitor.py` shows phase-grain `phase_complete` emission; no `task_complete` emitter retrieved.
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §1.4 (lines 93-109), `cliEval/execution-log.jsonl`

### F-A6-005: Pre-existing repo failures contaminate phase pass/fail signal

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint runner — task semantics)
- **Symptom:** v2.07 Phase 3 encountered three pre-existing issues that were unrelated to the sprint's own work: `make verify-sync` exit code 2 from `sc-forensic-qa-protocol` drift, `make lint-architecture` exit code 2 from two unrelated lint errors, and the T03.08 `_has_corresponding_command()` bug affecting all `-protocol` skills. Claude correctly diagnosed them as pre-existing, but the non-zero exit codes could have triggered false halts if tasks were structured to exit on first error.
- **Root cause (claimed):** No baseline-failure capture. Tasks have no concept of "delta vs known-bad starting state."
- **Remediation applied:** Recommendation drafted (P1 IMP-003) — pre-flight scan capturing `baseline-failures.json` for `make lint-architecture`, `make verify-sync`, `uv run pytest` before sprint execution; tasks compare delta. No commit reference.
- **Outcome:** Open. cliEval did not encounter this because its phases were greenfield, but the structural gap remains.
- **Still possible today (Auggie check):** UNKNOWN — Auggie did not return a baseline capture module. Tentatively YES (no evidence the recommendation landed).
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §2.4 (lines 169-183)

### F-A6-006: cliEval Phase 4 and Phase 5 hit error exit=1 on first run, recovered only on partial resume

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor — phase execution with --max-turns budget)
- **Symptom:** cliEval first sprint run (2026-05-20 04:40) executed all 6 phases. Phase 4 exited with `"status": "error", "exit_code": 1, "duration_seconds": 12000.33` (3h 20m), Phase 5 similarly `"status": "error", "exit_code": 1, "duration_seconds": 16920.54` (4h 42m). Sprint outcome was `"error"` with phases_passed=4, phases_failed=2. On 2026-05-21 the operator re-ran with `--start 4 --end 5`; Phase 4 then passed in 59m, Phase 5 in 77m. The original 5-6× longer first-run durations indicate context exhaustion or max-turns budget overrun, not a transient failure.
- **Root cause (claimed):** UNDOCUMENTED in cliEval artifacts (no post-mortem written). INFERENTIAL: First-run Phase 4 has 22 tasks and Phase 5 has 28 tasks (per `cliEval/tasklist-index.md` Phase Files table); at `--max-turns 100` per phase with STRICT-heavy tier mix (Phase 5 has STRICT:1+STANDARD:21+EXEMPT:1+LIGHT:5 = 28), the budget is plausibly exhausted. Second run with same tasklist succeeded in ~1/5 the wall-clock, suggesting first run was caught in retries or extended thinking.
- **Remediation applied:** None recorded. Operator manually resumed `--start 4 --end 5`. No fix to the budget model, no max_turns calibration, no per-phase budget formula like the v2.07 retrospective P2 IMP-008 (`max_turns = max(50, tasks_in_phase * 4)`).
- **Outcome:** Workaround (resume) succeeded. Structural cause unaddressed.
- **Still possible today (Auggie check):** YES — IMP-008 max-turns calibration was not implemented per the same retrospective's status; cliEval's first-run failure is direct evidence the brittleness persisted.
- **Source artifacts:** `cliEval/execution-log.jsonl` lines 1-15 (first run, error) vs lines 16-24 (resume, success); `cliEval/execution-log.md`; `cliEval/tasklist-index.md` (Phase Files table showing 28-task phase 5)

### F-A6-007: Phase name extraction emits leading dash artifact ("- Foundation Config Schema DSL Security")

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint config — phase name parsing from tasklist-index.md)
- **Symptom:** Every cliEval JSONL phase event records `"phase_name": "- Foundation Config Schema DSL Security"` (note the leading `"- "`). The Phase Files table in `tasklist-index.md` lists phase names cleanly: `"Foundation Config Schema DSL Security"`. The leading `"- "` indicates the parser captured table-cell content including a bullet/dash marker, or grabbed from a markdown list rather than the table cell.
- **Root cause (claimed):** UNDOCUMENTED. INFERENTIAL: The `# Phase N -- <Name>` heading format used by v3.0 tasklist generator was inconsistent across releases. The cliEval phase files likely use `## Phase N -- <Name>` or a list bullet, and the loader is grabbing `"- <Name>"` instead of `<Name>`.
- **Remediation applied:** None recorded in cliEval artifacts.
- **Outcome:** Cosmetic but persistent across all 6 phases for all 3 sprint attempts. JSONL is the canonical machine-readable log.
- **Still possible today (Auggie check):** UNKNOWN — auggie was not queried for the phase-name extraction path. The leading-dash artifact in May-21 cliEval JSONL is direct evidence it was unaddressed at that date.
- **Source artifacts:** `cliEval/execution-log.jsonl` (all `phase_start`/`phase_complete` events), `cliEval/tasklist-index.md:38-45` (Phase Files table — names are clean there)

### F-A6-008: Deviation analyzer produces 100% false-positive rate via bare-identifier matching

- **Type:** FAILURE
- **Pipeline step:** deviation-analysis
- **Symptom:** cliEval's pipeline emitted 20 deviations against the spec↔roadmap manifest. All 20 were resolved as `NO_ACTION` (analyzer false-positives) during manual triage. Two distinct analyzer bugs: (a) bare-name string match against roadmap.md missed qualified references inside backtick-quoted comma-separated lists in deliverable cells (11 `ExpectDSL` predicate helpers were verbatim in `roadmap.md:77` but missed), and (b) phantom ID extraction regex generated IDs `D-1, D12, D3, D5, D6` that did not exist in roadmap.md (only `D-5` and `D-8` exist as ADR labels).
- **Root cause (claimed):** Analyzer not implemented; placeholder regex shipped. Decisions.md#D-9 institutes manual-triage policy.
- **Remediation applied:** Manual maintainer triage on 2026-05-19; deviation-triage.md documents per-deviation evidence. Backlog item `pipeline-classifier-implementation` filed.
- **Outcome:** Workaround (manual triage) succeeded for this release. Underlying analyzer bug remains. Subsequent releases either bypass the gate or re-spend manual review.
- **Still possible today (Auggie check):** YES — `cliEval/spec-deviations.md` notes "deviation classification is not yet implemented in the pipeline." Until the classifier ships, every release with non-trivial spec/roadmap symbol surfaces will produce false positives.
- **Source artifacts:** `cliEval/spec-deviations.md`, `cliEval/deviation-triage.md` (full per-deviation evidence), `cliEval/remediation-tasklist.md` (all 20 entries marked `RESOLVED → NO_ACTION`), `cliEval/.roadmap-state.json:114-117` (`validation.status: "fail"` was the only blocker)

### F-A6-009: Manual roadmap remediation needed to satisfy false-positive deviation gate

- **Type:** REMEDIATION
- **Pipeline step:** remediate
- **Symptom:** Even after triage resolved all 20 as `NO_ACTION`, the operator chose to edit `roadmap.md` to *also* satisfy the analyzer — adding all 11 predicate helpers to COMP-010 ExpectDSL interface AC, adding 4 spec file references to COMP-014 + External Dependencies, and removing/rephrasing 5 D-N ID references. This was preventive hardening against re-running the gate.
- **Root cause (claimed):** Analyzer bug forces semantic noise into the roadmap to silence false positives. Documented in `remediate-roadmap.md`.
- **Remediation applied:** Roadmap edits applied 2026-05-19 by maintainer (RyanW).
- **Outcome:** Roadmap now passes analyzer; tasklist generation proceeded. But this is "fitting the spec to the bug," which is a hidden tax on every release until the classifier ships.
- **Still possible today (Auggie check):** YES — see F-A6-008.
- **Source artifacts:** `cliEval/remediate-roadmap.md`, `cliEval/deviation-triage.md` §"Follow-Up Recommendations"

### F-A6-010: Wiring-verification gate emits 7 major "orphan module" findings but is non-blocking

- **Type:** FAILURE
- **Pipeline step:** wiring-verification
- **Symptom:** cliEval `wiring-verification.md` reports 7 modules under `cli/cli_portify/steps/` (analyze_workflow, brainstorm_gaps, design_pipeline, discover_components, panel_review, synthesize_spec, validate_config) as having zero inbound imports per AST-only analysis. Severity is `major`, count is 7, but `blocking_findings: 0` because rollout_mode is `soft`. The gate does not actually stop the pipeline.
- **Root cause (claimed):** AST plugin not loaded — the analyzer cannot see dynamic imports / runtime wiring used by the `cli_portify` step registry. Diagnosed in the report's "Evidence and Limitations" section.
- **Remediation applied:** None — `rollout_mode: soft` is configured; findings remain noise.
- **Outcome:** Noise. Genuine orphans (real dead code) will be lost in the 7-row haystack on every release. The gate's signal-to-noise ratio is approximately zero until dynamic-import support lands or whitelist/suppression catches the steps directory.
- **Still possible today (Auggie check):** YES — wiring-verification.md is a snapshot of the soft-mode gate output; no fix recorded.
- **Source artifacts:** `cliEval/wiring-verification.md`

### F-A6-011: Tasklist-quality v2.08 audit confirms v3.0 generator is production-ready (success case)

- **Type:** SUCCESS
- **Pipeline step:** OTHER (tasklist generation — protocol compliance)
- **Symptom:** v2.08 RoadmapCLI release tasklist scored 9.20/10 weighted across 10 quality dimensions, with 100% protocol compliance against `sc:tasklist-protocol v3.0` (all 17 self-checks pass, all applicable specification requirements met). v2.07-tasklist-v1 calibrated to 9.10/10. The v3.0 multi-file bundle format (literal filenames in Phase Files table, `# Phase N -- <Name>` headings, end-of-phase checkpoints) is the single largest improvement over prior generations (4.5 → 7.0 → 9.5 on Structure dimension).
- **Root cause (claimed):** Generator v3.0 + protocol enforcement (triple-registry R-### → T<PP>.<TT> → D-####, deterministic effort/risk scoring, tier classification with compound-phrase priority, Sprint CLI-compatible heading regex).
- **Remediation applied:** N/A (success).
- **Outcome:** Two consecutive releases (v2.07, v2.08) score >9.0/10. Tasklist format is solved for the canonical case.
- **Still possible today (Auggie check):** N/A.
- **Source artifacts:** `v2.07-tasklist-v1/tasklist-quality-comparison-v2.08.md` (final rankings table, calibrated scores)

### F-A6-012: Adversarial debate pipeline successfully reshapes spec proposals (success case)

- **Type:** SUCCESS
- **Pipeline step:** debate, score, merge (sc:adversarial)
- **Symptom:** v2.07-tasklist-v1's 5-strategy refactor plan went through structured adversarial debate (Opus advocate vs Haiku critic, then cross-variant comparison). Strategy 1 (Stage-Gated Contract) converged at 91% with combined score 8.02/10, adopted with modifications M1-M5. Strategy 2 was reduced in scope (full error taxonomy deferred to v1.1). Strategy 3 was reduced from 4 criteria to 3 (session-start executability deferred). Strategy 4 was reframed to tighten existing fields rather than add new ones. Strategy 5 was unified at checks 9-17. No strategy was fully rejected; all received conditional acceptance with scope narrowing. cliEval similarly converged: base-selection.md picked Opus (82/100) over Haiku (74/100) with 8 cherry-picked improvements from Haiku integrated (I1-I8).
- **Root cause (claimed):** N/A (success).
- **Remediation applied:** N/A.
- **Outcome:** Final unified refactor plan landed at `v2.07-tasklist-v1/final-unified-refactor-plan.md` with provenance comments tracing every change to its debate origin. The 5-step debate (diff → debate → scoring → refactor → merge) produced implementation-ready patches.
- **Still possible today (Auggie check):** N/A.
- **Source artifacts:** `v2.07-tasklist-v1/final-unified-refactor-plan.md`, `v2.07-tasklist-v1/adversarial/strategy1-stage-gated-contract/adversarial-final-report.md`, `cliEval/base-selection.md`, `cliEval/diff-analysis.md`

### F-A6-013: cliEval pipeline survives end-to-end without halt despite failed validation gate

- **Type:** SUCCESS / FAILURE-MIXED
- **Pipeline step:** extract → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate
- **Symptom:** cliEval `.roadmap-state.json` records every pipeline step (extract, generate-opus-architect, generate-haiku-architect, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate) as `"status": "PASS"` on first attempt. But `fidelity_status: "pass"` coexists with `validation.status: "fail"` (timestamp 2026-05-18T19:47:24). The fail is the deviation-analysis 20-false-positive blocker that was later triaged.
- **Root cause (claimed):** State machine separates per-step status (each step "completed") from gate validation status (the final pass/fail). When a step completes but its output triggers a downstream gate failure, only the gate fails, not the step. This is logically correct but operationally confusing because `state.json` shows "all PASS" yet validation is "fail."
- **Remediation applied:** Manual triage closed the validation.fail; `.roadmap-state.json:114-117` was left at `"fail"` per the triage report's note ("`.roadmap-state.json` is NOT edited in this turn").
- **Outcome:** Pipeline executed; release shipped after manual intervention. But state file misrepresents reality: every reader of `.roadmap-state.json` will see `validation.fail` even though the release was approved.
- **Still possible today (Auggie check):** YES — see F-A6-008/F-A6-009.
- **Source artifacts:** `cliEval/.roadmap-state.json`, `cliEval/spec-fidelity.md` (validation_complete: true, tasklist_ready: true)

### F-A6-014: Anti-instinct audit reports 84% fingerprint coverage with 13 missing tokens

- **Type:** FAILURE
- **Pipeline step:** anti-instinct
- **Symptom:** cliEval `anti-instinct-audit.md` shows `fingerprint_coverage: 0.84` (69 of 82 fingerprints found). 13 fingerprints were missing: `CLAUDE_WORK_DIR, GIT_CEILING_DIRECTORIES, CLAUDE_PLUGIN_DIR, CLAUDE_SETTINGS_DIR, PtySession, DRAFT, OPTIONS, CROSSED, XDG_, SIGKILL, MAJOR, MODIFIED, REUSED`. `undischarged_obligations: 0`, `uncovered_contracts: 0` (because `total_obligations: 0` and `total_contracts: 0` — the obligation/contract scanners detected nothing to scan).
- **Root cause (claimed):** UNDOCUMENTED. INFERENTIAL: Several missing tokens (`DRAFT`, `OPTIONS`, `CROSSED`, `MAJOR`, `MODIFIED`, `REUSED`) look like ALL-CAPS common-English false-positive fingerprints — the fingerprinter is matching prose words as if they were code identifiers. Other tokens (`CLAUDE_WORK_DIR`, `XDG_`, `SIGKILL`) are valid identifiers from the spec that the roadmap legitimately did not need to mention. Either way, 0.84 is below 1.0 but the gate did not block.
- **Remediation applied:** None recorded.
- **Outcome:** Audit passed (no obligations/contracts to scan). Fingerprint gap unaddressed.
- **Still possible today (Auggie check):** YES (no fingerprinter fix evident).
- **Source artifacts:** `cliEval/anti-instinct-audit.md`

### F-A6-015: v3.0 tasklist generator forced upgrade path required full upgrade-review study

- **Type:** REMEDIATION
- **Pipeline step:** OTHER (tasklist generator versioning)
- **Symptom:** Prior to v3.0, two competing prompts existed: Prompt A (v2.0, conversation-generated, multi-output) and Prompt B (v2.1, `upgrade.md`, deterministic + safety-focused). A formal `tasklist-upgrade-review.md` scored them across 8 dimensions; Prompt B won 65/80 vs 50/80 on the strength of Determinism (+4), Safety (+6), Traceability (+5), Clarity (+2), Maintainability (+2). Hybrid recommendations were drafted to backfill A's execution-readiness features (Pre-Flight, Resume, "If Blocked", Task Types, Parallel notation) into B.
- **Root cause (claimed):** Generator generation jumps require explicit auditing because prompt features overlap in non-comparable ways. Without the review, picking the wrong base would have either lost safety (had we kept A) or lost execution-readiness (had we kept B vanilla).
- **Remediation applied:** Review concluded with the hybrid recommendation that became v3.0 multi-file bundle. v3.0 includes traceability + safety + multi-file structure.
- **Outcome:** v3.0 generator powers v2.07/v2.08 releases scoring >9.0/10 (see F-A6-011). Upgrade succeeded.
- **Still possible today (Auggie check):** N/A (success).
- **Source artifacts:** `v2.07-tasklist-v1/tasklist-upgrade-review.md`

### F-A6-016: Three-attempt convergence before successful v2.07 sprint run

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint runner — pre-success failed attempts)
- **Symptom:** v2.07 retrospective records three attempts before the successful 23-minute run: 02:44 (killed, exit -9), 02:53 (2-turn test), 02:55 (2-turn test). The successful run was at 10:54. Test runs are intentional; the killed run at 02:44 is the failure.
- **Root cause (claimed):** UNDOCUMENTED in v2.07 retrospective beyond the observation that "exit -9" indicates SIGKILL (likely OOM or operator interrupt). Recommendation: track run attempt counts as metadata.
- **Remediation applied:** None implemented.
- **Outcome:** Successful 4th run masked the earlier crash. No telemetry exists to distinguish "intentional --max-turns test" from "OOM-killed real attempt."
- **Still possible today (Auggie check):** UNKNOWN — auggie did not surface attempt-count tracking in `sprint/executor.py`. Tentatively YES.
- **Source artifacts:** `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md` §"Key Observations" #5 (lines 302-303)

### F-A6-017: cliEval generated 143 tasks (117 regular + 26 checkpoints) on first attempt — generator scales

- **Type:** SUCCESS
- **Pipeline step:** OTHER (tasklist generation — high-complexity scale)
- **Symptom:** cliEval's `tasklist-index.md` declares 143 total tasks across 6 phases with complete R-001..R-116 roadmap registry, D-#### deliverable registry, and traceability matrix. Generated successfully on first attempt by Generator v4.0. Phase distribution: P1 (27 tasks), P2 (27), P3 (23), P4 (22), P5 (28), P6 (16). All phases use literal `phase-N-tasklist.md` filenames and `STRICT/STANDARD/EXEMPT/LIGHT` tier distributions.
- **Root cause (claimed):** N/A (success).
- **Remediation applied:** N/A.
- **Outcome:** v4.0 generator handles 116-deliverable HIGH-complexity input cleanly.
- **Still possible today (Auggie check):** N/A.
- **Source artifacts:** `cliEval/tasklist-index.md` (Metadata + Phase Files + Roadmap Item Registry)

### F-A6-018: Sprint-cli specification's extracted FRs cover 38 requirements but ship in monolithic tasklist (regression vs v2.07)

- **Type:** FAILURE
- **Pipeline step:** OTHER (tasklist generation — Sprint CLI compatibility regression)
- **Symptom:** v2.05-sprint-cli-specification produced a single `tasklist/tasklist.md` (monolithic file, generator v2.2) with 35 tasks for 42 roadmap items. The tasklist-quality-comparison-v2.08 audit scored this Structure dimension at 4/10 (later calibrated to 5) — it is NOT a multi-file bundle, has no Phase Files table with literal filenames, and Sprint CLI would not discover phases via regex. The content scores were excellent (Validation 10/10, Traceability 10/10, Acceptance Criteria 9/10), but the structure regression made it non-executable by the Sprint CLI.
- **Root cause (claimed):** Generator v2.2 (which powered v2.05) predated the `sc:tasklist-protocol v3.0` multi-file bundle format. The Sprint CLI compatibility constraint was added afterward.
- **Remediation applied:** Generator v3.0 (Section 6 of `sc-tasklist-command-spec-v1.0.md`) made multi-file bundle mandatory. Subsequent releases use phase-N-tasklist.md naming.
- **Outcome:** Resolved at the format level. v2.05 itself was never sprint-executable as-shipped.
- **Still possible today (Auggie check):** NO — v3.0 protocol is now enforced via the §8 Sprint Compatibility Self-Check (file emission with literal filenames is check #5/8). Earlier formats cannot pass.
- **Source artifacts:** `v2.05-sprint-cli-specification/tasklist/tasklist.md` (monolithic), `v2.07-tasklist-v1/tasklist-quality-comparison-v2.08.md` §"Release Assessments" #2

### F-A6-019: Strategy 1 debate identified circular self-validation as fundamental skill limitation

- **Type:** REMEDIATION
- **Pipeline step:** OTHER (skill-level vs runtime-level validation boundary)
- **Symptom:** During Strategy 1 adversarial debate (Stage-Gated Generation Contract), the strongest objection (A1) was that LLM skills cannot enforce halt semantics with certainty — "A SKILL.md is a prompt-based instruction set interpreted by an LLM. There is no deterministic runtime that enforces stage boundaries." The debate resolved by adopting a hybrid: structural gates (deterministic predicates — field presence, ID format, file existence) check minimal viability; semantic gates (content quality) are TodoWrite-observed but advisory.
- **Root cause (claimed):** Architectural limitation, not a bug. The skill layer cannot self-validate semantic correctness because the same model produces and validates.
- **Remediation applied:** Hybrid gating language adopted in `final-unified-refactor-plan.md` Strategy 1. Pure halt-on-failure was rejected; pure observability-only was also rejected.
- **Outcome:** Honest scope boundary documented. v1.1 deferred items include "Per-stage halt-on-failure for semantic properties" with note "needs external validator."
- **Still possible today (Auggie check):** N/A (this is an architectural decision, not a bug).
- **Source artifacts:** `v2.07-tasklist-v1/adversarial/strategy1-stage-gated-contract/adversarial-final-report.md` §Deliverable 2 (A1), `v2.07-tasklist-v1/final-unified-refactor-plan.md` §"What was rejected"

---

## Cross-cutting patterns within this partition

- **Telemetry is text-regex-based against structured stream-json output, producing silent data loss across multiple signals** (F-A6-001 PARTIAL token ordering, F-A6-002 files_changed pattern, F-A6-003 last_task_id phase scope) — every one of these breaks the same way: regex against prose when the underlying source is now structured NDJSON.
- **The roadmap→tasklist→sprint pipeline routinely ships releases via manual workarounds rather than passing gates cleanly** (F-A6-008 deviation analyzer, F-A6-009 manual roadmap edits, F-A6-013 state.json validation=fail despite shipped release, F-A6-016 three-attempt sprint convergence) — operator labor masks structural brittleness.
- **High-priority remediations identified in retrospectives do not land** (F-A6-001 P0 IMP-001, F-A6-002 P1 IMP-002, F-A6-004 P2 IMP-007 all still present in current code per auggie cross-reference) — the gap between "documented fix" and "implemented fix" is the dominant brittleness vector.
- **Tasklist generation is the strongest stage; sprint execution is the weakest** (F-A6-011 v3.0 generator hits 9.20/10 quality, F-A6-017 v4.0 scales to 143 tasks cleanly, vs F-A6-006 cliEval phases 4-5 erroring out, F-A6-007 phase-name parsing artifact, F-A6-001/002/003/004 telemetry bugs) — the upstream→downstream coupling fails because the downstream consumer (sprint) cannot reliably interpret the upstream artifact.
- **Adversarial debate consistently improves spec proposals through conditional acceptance with scope reduction** (F-A6-012, F-A6-019) — no strategy is rejected outright; instead the merge process narrows scope to preserve parity constraints while landing the reliability improvements. This is the partition's most-functional sub-pipeline.
- **Gates exist in soft/shadow mode and produce noise without action** (F-A6-010 wiring-verification 7 major findings non-blocking, F-A6-014 anti-instinct 0.84 coverage non-blocking, F-A6-013 validation.fail non-blocking after manual triage) — gates that don't gate are decorative.
- **Pre-existing repository state contaminates phase pass/fail semantics with no baseline-capture mechanism** (F-A6-005, also implicitly F-A6-006 where ambient context exhaustion is indistinguishable from real failure) — without a "delta vs known-bad" model, every release manually adjudicates pre-existing noise.

## Brittleness drivers identified

- **No PARTIAL terminal state in the phase status model.** `PhaseStatus` enum (sprint/models.py:211-222) has only PASS, PASS_*, HALT, TIMEOUT, ERROR, INCOMPLETE, plus run-lifecycle states. Without a PARTIAL value, the executor must collapse "8 of 9 tasks passed" into either PASS (silent data loss) or HALT (sprint stops on every minor failure). The v2.07 P0 recommendation to add PARTIAL was never implemented.
- **Result-file parsing uses linear token search with first-match-wins ordering rather than a typed schema.** `_determine_phase_status()` (executor.py:2113-2138) sequentially checks for HALT, CONTINUE, PASS, FAIL, PARTIAL tokens in a single text scan. Token ordering determines outcome. There is no structured frontmatter parser that yields a typed `result_status` field.
- **Monitor signal extraction is text-regex-only with no structured tool_use event path.** `monitor.py:556-570` operates on text fallback (`TOOL_PATTERN.findall(text)`, `FILES_CHANGED_PATTERN.findall(text)`). Structured `_extract_signals_from_event()` exists but does not populate `_seen_files` from JSON `input.file_path`. Every signal that lives in stream-json structure is invisible to the monitor.
- **No baseline-failure capture before sprint execution.** Phases inherit ambient repository failures (lint, verify-sync, test) with no "delta vs known-bad" reference. Every release manually distinguishes pre-existing from sprint-introduced failures.
- **Pipeline gates ship in `soft`/`shadow` mode by default.** wiring-verification rollout_mode=soft, anti-instinct fingerprint_coverage threshold not enforced, deviation-analysis NO_ACTION dominates the disposition counts. Gates that observe without blocking accumulate noise and lose operator trust.
- **Deviation analyzer placeholder ships before implementation lands.** `cliEval/spec-deviations.md:10` openly states "deviation classification is not yet implemented in the pipeline" — the gate runs anyway with a bare-identifier regex that produces 100% false positives, forcing manual triage on every release.
- **No turn-budget calibration model.** `--max-turns 100` is a flat per-phase budget. Phases vary from 16 to 28 tasks (cliEval) without proportional budget. The v2.07 retrospective recommended `max_turns = max(50, tasks_in_phase * 4)`; not implemented; cliEval Phase 5 (28 tasks) error-exited on the budgeted run.
- **The `.roadmap-state.json` state file conflates step completion with gate validation.** `fidelity_status: "pass"` and `validation.status: "fail"` can coexist; manual triage closes the gate but does not update the state. Readers cannot tell from state.json whether the release actually shipped.
- **Skill-layer self-validation is architecturally impossible (single-model circular check) but the spec text repeatedly proposes it.** The Strategy 1 debate (F-A6-019) honestly named this limit; the v1.1 deferred list includes "Per-stage halt-on-failure for semantic properties — needs external validator." Until an external validator exists, every "the skill will validate" recommendation is aspirational.
- **Run-attempt history is not preserved.** Killed runs (exit -9, OOM) and intentional 2-turn tests are visually indistinguishable in the JSONL stream. Without attempt metadata, "what really happened" requires correlating timestamps with operator memory.
- **Phase-name extraction parses table cells with embedded markdown artifacts** (leading `"- "` dash) instead of using the `# Phase N -- <Name>` heading regex. Same brittleness class as F-A6-002/003: parser-against-prose where the canonical source is structured.
