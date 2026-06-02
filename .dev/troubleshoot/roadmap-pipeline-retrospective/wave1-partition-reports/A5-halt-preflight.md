# Partition A5: Halt + Preflight + Accept (failure-mode handling)

**Partition focus:** How the pipeline behaves when it fails — halt semantics, resume
semantics, accept-spec-change deviation, turn-ledger gaps.

**Releases analyzed:**
1. `v2.25.5-PreFlightExecutor` — Pre-sprint Python executor (nested-claude deadlock fix)
2. `v2.25.7-Phase8HaltFix` — Sprint context resilience / isolation / context-exhaustion detection
3. `v2.24.2-Accept-Spec-Change` — Spec-hash sync command + auto-resume cycle
4. `v3.7-turnledger-integration` — TurnLedger wiring, validation, gap-closure

---

## Findings

### F-A5-001: Recursive `claude` subprocess nesting deadlocks entire sprint phase
- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor — phase subprocess launch)
- **Symptom:** Sprint Phase 1 ran 857s, exited 143 (SIGTERM), zero phases completed.
  A nested `claude --print -p "hello"` invocation (PID 283918) hung with 0 bytes
  stdout for 14+ minutes while the outer agent burned six `TaskOutput` polling
  cycles waiting for it.
- **Root cause (claimed):** Outer `claude` subprocess spawned via `Task` tool another
  `claude` process; "recursive `claude` nesting deadlocks due to API contention /
  session detection." Compounding cause: all 5 Phase 1 tasks were EXEMPT-tier
  validation work that did not require an LLM at all — pure shell commands.
- **Remediation applied:** Pre-sprint Python executor (`execute_preflight_phases()`)
  that classifies phases via an `execution_mode` annotation (`python|claude|skip`)
  in the tasklist index, parses `**Command:**` fields, runs them with
  `subprocess.run()`, applies named Python classifiers, and writes a result file
  in the exact format `_determine_phase_status()` expects. Spec
  `sprint-preflight-executor-spec.md`, release v2.25.5.
- **Outcome:** Annotation-based design accepted (score 7.77/10 vs alternatives);
  full mini-executor scope chosen over shell-only (8.15/10) because
  `_subprocess_factory` + `AggregatedPhaseReport` were already structured for it.
- **Still possible today (Auggie check):** NOT CHECKED — fix is annotation-gated;
  any unannotated phase that issues nested `claude` calls can still deadlock,
  but no live regression evidence in the partition.
- **Source artifacts:**
  - `v2.25.5-PreFlightExecutor/sprint-preflight-executor-spec.md` (§1.1, §2.1)

### F-A5-002: Context-exhaustion error on stderr never inspected (defense-in-depth gap)
- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor — phase status determination)
- **Symptom:** Phase 2 of CLI Portify sprint (7 tasks, 192 tests passing) crashed
  at turn 106 while writing the final completion report. Sprint halted at $24.96
  cost despite all implementation work being complete. The Anthropic API returned
  `"Prompt is too long"` exit code 1 — but `detect_prompt_too_long()` scanned
  only stdout NDJSON (`output_path`), missing the stderr surface where the error
  actually landed.
- **Root cause (claimed):** `detect_prompt_too_long()` had no `error_path`
  parameter; `_determine_phase_status()` never passed the error file in even
  when one existed. Compounding cause: `setup_isolation()` had been written
  but was never wired into `execute_sprint()`, so the full ~14K-token
  `tasklist-index.md` was resolvable by every phase subprocess via `@`,
  accelerating exhaustion.
- **Remediation applied:** v2.25.7 PRD shipped 8 changes:
  S3-A (wire isolation), S3-B (env_vars on ClaudeProcess), S3-C (orphan
  isolation cleanup at sprint start), S3-D (`## Sprint Context` prompt header),
  S2-D (extend `detect_prompt_too_long` to scan error_path), S2-E (plumb
  error_file from `_determine_phase_status()`), FIX-1 (`PASS_RECOVERED`
  routed to screen output), FIX-2 (`FailureClassifier` uses
  `config.output_file(phase)` instead of hardcoded path expression).
- **Outcome:** PARTIAL — see F-A5-003 for the runtime-wiring gap that survived
  the initial implementation.
- **Still possible today (Auggie check):** UNKNOWN — NOT CHECKED. v2.25.7
  spec mandates the fix; runtime verification of S2-D coverage on real
  stderr would require a fresh check.
- **Source artifacts:**
  - `v2.25.7-Phase8HaltFix/v2.25.7-phase8-sprint-context-resilience-prd.md` (§1, §3)

### F-A5-003: T04.02 / FIX-2 fix landed in shape only — runtime path still on legacy fallback
- **Type:** FAILURE (partial remediation)
- **Pipeline step:** OTHER (sprint executor — diagnostics collection)
- **Symptom:** `DiagnosticBundle` was given `config: SprintConfig | None = None`
  and `FailureClassifier.classify()` was updated to use
  `bundle.config.output_file(...)` if config exists — but
  `DiagnosticCollector.collect()` continued to construct `DiagnosticBundle`
  without passing config (`diagnostics.py:88-92`). So the normal runtime
  collection path stayed on the deprecated hardcoded-path fallback. The
  initial T04.02 evidence (D-0014/D-0015) marked complete despite this.
- **Root cause (claimed):** UNDOCUMENTED in the original PRD — surfaced only
  post-hoc by phase-8-partial remediation tasklist. Pattern: keyword-only
  optional parameter added at the receiver but not threaded through the
  caller chain.
- **Remediation applied:** `phase8-partial-task-remediation-tasklist.md`
  RT-01 — pass `config=self.config` from `DiagnosticCollector.collect()`,
  audit every other `DiagnosticBundle(` construction site, add tests
  covering both config-present and config-none paths.
- **Outcome:** Remediated by tasklist; success depends on RT-01 actually
  being executed (file present, evidence of completion not verified
  within budget).
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:**
  - `v2.25.7-Phase8HaltFix/phase8-partial-task-remediation-tasklist.md`
    (Context Summary, Task 1 / RT-01)

### F-A5-004: Cross-phase contract gap — Phase 1 signature drops `-> bool` Phase 2 depends on
- **Type:** FAILURE (caught by spec-fidelity gate)
- **Pipeline step:** spec-fidelity
- **Symptom:** Roadmap-pass-no-report-fix spec-fidelity flagged DEV-002 (HIGH):
  Phase 1 specified `_write_preliminary_result()` signature without an explicit
  return-type contract; Phase 2's `_wrote_preliminary = ...` telemetry depends
  on Phase 1 producing a `-> bool` function. An implementer reading only
  Phase 1 would produce `-> None` and silently break Phase 2.
- **Root cause (claimed):** Roadmap omitted NFR-007 (Option A compliance
  telemetry / return value logging) from Phase 1 exit criteria — the
  return-type contract was named in the spec but not echoed into the
  roadmap's per-phase exit criteria.
- **Remediation applied:** `fix-plan-high.md` Fix 1 — add explicit
  `Return True/False` semantics bullet to Phase 1 implementation steps and
  bind the contract into Phase 1 exit criteria.
- **Outcome:** Fix plan written; recommended ordering DEV-002 → DEV-001 → DEV-003
  because DEV-001's T-005 test ("returns False") only makes sense after the
  return contract is locked in.
- **Still possible today (Auggie check):** NOT CHECKED. Pattern (spec lists
  cross-phase contract; roadmap drops it from per-phase exit criteria) is
  reusable across releases — see F-A5-009.
- **Source artifacts:**
  - `v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/spec-fidelity.md`
    (DEV-001, DEV-002, DEV-003)
  - `v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/fix-plan-high.md` (Fix 1)

### F-A5-005: Spec-hash mismatch on documentation-only edits triggers full 28-min pipeline re-run
- **Type:** FAILURE
- **Pipeline step:** extract / pipeline resume
- **Symptom:** When a spec file was edited to formalize an accepted deviation
  (a documentation sync, not a functional change), `_apply_resume()` saw the
  hash mismatch as a functional spec change, set `force_extract = True`, and
  cascaded a full 28-minute pipeline re-run. All valid upstream outputs
  (roadmap files, debate transcript, diff, etc.) discarded.
- **Root cause (claimed):** `_apply_resume()` (`executor.py:1068-1079`) had
  no way to distinguish "spec updated to match accepted roadmap" from "spec
  requirements genuinely changed." No `auto_accept` parameter on
  `execute_roadmap()`. Sprint runner could not proceed non-interactively
  after deviation acceptance.
- **Remediation applied:** v2.24.2 spec — additive design: new module
  `spec_patch.py` (stdlib + PyYAML only, to break circular dependency
  risk with `executor.py`); new CLI command
  `superclaude roadmap accept-spec-change`; two new private functions in
  `executor.py` (`_apply_resume_after_spec_patch()`); `execute_roadmap()`
  gains `auto_accept` keyword param (backward-compatible default). Evidence
  gate: requires at least one `dev-*-accepted-deviation.md` with
  `disposition: ACCEPTED` and `spec_update_required: true`. Recursion guard:
  local counter, max 1 cycle.
- **Outcome:** Tasklist generated (5 phases, 23 tasks, 27 deliverables);
  release marked complete.
- **Still possible today (Auggie check):** NOT CHECKED. Design decisions
  documented include "disk-reread at resume boundary" to prevent stale
  in-memory state. If that re-read is ever bypassed for performance, the
  failure mode returns.
- **Source artifacts:**
  - `v2.24.2-Accept-Spec-Change/release-spec-accept-spec-change.md` (§1, §2)
  - `v2.24.2-Accept-Spec-Change/design-accept-spec-change.md` (§1, §2)
  - `v2.24.2-Accept-Spec-Change/tasklist-index.md`

### F-A5-006: Adversarial validation pass overstates implementation readiness — assumes call sites that don't exist
- **Type:** FAILURE (process flaw)
- **Pipeline step:** debate / adversarial validation
- **Symptom:** The Phase8 cross-spec overlap analysis Step 2 was "not
  implementable as described." It assumed `execute_phase_tasks()` and
  `aggregate_task_results()` were called within `execute_sprint()`, providing
  `task_results` and `remaining` variables. The dual-agent adversarial
  re-review (Variants A architect + B analyzer, blind=true, convergence 95%)
  found `aggregate_task_results()` is NEVER called from `execute_sprint()`;
  the function exists at lines 285-330 but is dead code relative to the main
  execution path. Step 2's "~5 lines" estimate dramatically understated
  implementation effort and cascaded into Steps 3, 6, 9.
- **Root cause (claimed):** Original analysis treated existing API surface as
  proof of wiring — looked up function definitions, did not verify call sites.
  Compounding cause: line-number drift (CBS-1 off-by-one, CBS-2 off-by-one,
  CBS-3 critical correction, CBS-4 4-line truncation in claimed range) —
  the analysis used cached or stale line ranges.
- **Remediation applied:** Adversarial pass emitted explicit corrective
  action: either (a) Step 0 wiring prerequisite (substantial refactor), or
  (b) redesign Step 2 to write a minimal result file from phase-level exit
  code + MonitorState. Variant A independently corroborated via FACT-26 and
  FACT-27.
- **Outcome:** Caught before implementation. The validation is itself the
  defense — but only because the adversarial pass was run on the analysis
  document, not just on the spec.
- **Still possible today (Auggie check):** NOT CHECKED. Pattern (analysis
  documents written without call-site verification) is reusable across any
  release; cited as a brittleness driver below.
- **Source artifacts:**
  - `v2.25.7-Phase8HaltFix/Phase8-SprintContext-cross-spec-overlap-analysis-adversarial/cross-spec-overlap-validation.md`
    (Executive Summary, Impact Cascade, CBS-1..CBS-8, OV-4)

### F-A5-007: v3.7 TurnLedger validation — 10 HIGH coverage findings caught by adversarial merge
- **Type:** REMEDIATION
- **Pipeline step:** spec-fidelity / debate
- **Symptom:** v3.3 TurnLedger Validation single-agent validation initially
  scored D1 at 100% (25/25). Adversarial cross-validation pass (Claude
  Variant A + GPT Variant B + Kimi + Sonnet validators) identified FR-1.19,
  FR-1.20, FR-1.21, FR-2.1a as MISSING from roadmap, correcting D1 to
  88.0%. Cross-validation found two additional spec-roadmap CONFLICTS
  (FR-7.1 schema missing `duration_ms`; FR-7.3 flush-semantics conflict
  session-end-vs-per-test) that BOTH primary agent passes missed.
- **Root cause (claimed):** Primary agents incorrectly marked items
  COVERED that adversarial review showed were absent. Roadmap claimed
  "13 requirements" — actual atomic surface was 47 FRs + 12 SCs + 6
  constraints (65 total). Misleading planning metadata.
- **Remediation applied:** `remediation-tasklist.md` Phase 0 (Roadmap
  Remediation) with TASK-R01..R04+ — surgical roadmap text corrections
  (add `duration_ms` field, change "session end" to "per test", add tasks
  2A.13/2A.14/2A.15/2B.5 for the missing FRs).
- **Outcome:** Final wiring-verification artifact reports PASS — 12/12 SCs
  green, 4,770 tests passed, 0 new regressions, 21/21 FR-1 wiring points
  covered, 74 audit-trail JSONL records. NO_GO became GO after Phase 0
  remediation closed the gaps.
- **Still possible today (Auggie check):** NOT CHECKED. The success mode
  required the adversarial merge; without it, the single-agent NO_GO
  would have shipped as a false GO.
- **Source artifacts:**
  - `v3.7-turnledger-integration/validation-comparison/merged-consolidated-report.md`
    (Executive Summary, Coverage by Domain, GAP-H001..GAP-H008)
  - `v3.7-turnledger-integration/v3.7-TurnLedger-Validation/remediation-tasklist.md`
    (Phase 0, TASK-R01..R04)
  - `v3.7-turnledger-integration/v3.3-wiring-verification-final.md` (§1, §2)

### F-A5-008: Embed-guard dead zone — guard above kernel limit causes unrecoverable OSError
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** Roadmap pipeline crashed with `OSError: [Errno 7] Argument
  list too long` at spec-fidelity when combined input files exceeded 128 KB.
  Pipeline halted with no recovery. `--file` fallback "likely broken (80%
  confidence)" — passes bare paths but `claude --help` documents
  `file_id:relative_path` format.
- **Root cause (claimed):** `_EMBED_SIZE_LIMIT = 200 * 1024  # 100 KB` —
  comment/value mismatch (`executor.py:54`). Guard set above Linux kernel's
  `MAX_ARG_STRLEN = 128 KB`, creating a 72 KB dead zone where content
  passed the guard but crashed `subprocess.Popen`. Test
  `test_100kb_guard_fallback` mocked subprocess — zero integration coverage
  of the real fallback path.
- **Remediation applied:** v2.25.1 spec — derive `_EMBED_SIZE_LIMIT` from
  `MAX_ARG_STRLEN` instead of magic constant; measure full composed `-p`
  argument; validate `--file` fallback empirically (Phase 0); fix it in all
  executors if broken (Phase 1.5).
- **Outcome:** Spec drafted; cited as upstream context for the v2.25.7
  Phase 8 work. Outcome of v2.25.1 itself not verifiable within partition.
- **Still possible today (Auggie check):** NOT CHECKED. Dead-zone pattern
  (validator threshold > true OS/runtime limit) reusable across any
  resource-bound guard.
- **Source artifacts:**
  - `v2.25.7-Phase8HaltFix/v2.25.1-arg-too-long-spec.md` (§1, §2)

### F-A5-009: Roadmap renumbers spec acceptance criteria — traceability gap
- **Type:** FAILURE (caught by spec-fidelity gate)
- **Pipeline step:** spec-fidelity
- **Symptom:** Roadmap introduced `SC-009b` (new success criterion not
  present in spec §9) and renumbered several criteria. SC-006 in roadmap
  mapped to "Zero-byte file overwritten" while SC-006 in spec mapped to
  TIMEOUT/ERROR/INCOMPLETE/PASS_RECOVERED. Validators cross-referencing
  roadmap SC table against spec §9 could not match. Additionally roadmap
  referenced `FR-008` for an ordering invariant — but `FR-008` does not
  exist in the spec; the ordering invariant lives inside FR-001 and FR-002.
- **Root cause (claimed):** Roadmap generator (or human editor) invented
  new identifiers / renumbered without preserving spec IDs as a stable
  contract.
- **Remediation applied:** Spec-fidelity report DEV-003 (HIGH), DEV-004
  (MEDIUM) recommended exact corrections — align SC IDs with spec §9,
  document SC-009b as architecturally-derived (from §5 Implication 9) not
  a new spec requirement, replace `FR-008` with `(FR-001 ordering invariant)`.
- **Outcome:** Caught at the spec-fidelity gate before merge.
- **Still possible today (Auggie check):** NOT CHECKED. Spec-fidelity
  catches this pattern only when the gate runs and is read; the underlying
  generator behavior that emits the renumbering is not addressed here.
- **Source artifacts:**
  - `v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/spec-fidelity.md`
    (DEV-003, DEV-004)

---

## Cross-cutting patterns within this partition

1. **Receiver-only wiring (caller chain unthreaded).** A new optional/keyword
   parameter is added at the receiver and tests pass against synthetic
   callers, but the real-world caller chain never threads the value through.
   Result: the legacy/fallback path stays live in production. Findings:
   F-A5-003 (DiagnosticBundle.config), implicit risk in F-A5-002's S3-A
   isolation wiring.

2. **Single-agent validation overstates coverage; adversarial merge surfaces
   real gaps.** Primary agents mark items COVERED that adversarial review
   shows MISSING or CONFLICTING. Findings: F-A5-006 (Step 2 not implementable),
   F-A5-007 (4 MISSING FRs + 2 CONFLICTS surfaced only via adversarial
   merge of two independent runs).

3. **Validator threshold misaligned with real runtime/OS limit.** The guard
   measures the wrong thing or is set above the actual hard limit, creating
   a dead zone where validation passes but execution crashes. Findings:
   F-A5-008 (embed-guard 72 KB dead zone), F-A5-002 (detect_prompt_too_long
   inspected wrong stream).

4. **Cross-phase contracts dropped from per-phase exit criteria.** Spec names
   a contract (return type, sentinel string, telemetry boolean) that must
   hold across phases; roadmap copies it into only ONE phase's body and omits
   it from exit criteria. Implementer reading the other phase in isolation
   produces a broken signature. Findings: F-A5-004 (DEV-002 `-> bool`),
   DEV-005 (NFR-006 sentinel comment), DEV-007 (Phase 3 `as_posix()`
   weakened to "POSIX separators").

5. **Hash-based change detection conflates documentation sync with semantic
   change.** Treating any spec file hash mismatch as a functional change
   forces a full re-run, discarding valid upstream artifacts. Findings:
   F-A5-005 (spec_hash mismatch → 28-min cascade re-run).

6. **Nested same-tool subprocesses deadlock.** Subprocess-spawning tools that
   invoke themselves recursively (here, `claude` from inside `claude`) hang.
   Defense is to identify pure deterministic work and route it through a
   non-LLM executor before the LLM subprocess loop begins. Findings:
   F-A5-001 (preflight Python executor).

7. **Spec-ID renumbering destroys traceability.** Roadmap-side renumbering
   or invention of identifiers (SC-009b, FR-008) breaks cross-references
   that downstream tools and reviewers rely on. Findings: F-A5-009.

## Brittleness drivers identified

- **Optional keyword-only parameters with backward-compatible None defaults.**
  Pattern enables shipping a fix in shape without forcing call sites to
  adopt it. F-A5-003 shows the failure mode: the legacy path stays live;
  the new path is reachable only from explicit test construction.
- **Single-agent validation as the only gate.** Without adversarial merge
  (Claude × GPT × Kimi × Sonnet variants, blind=true), HIGH-severity coverage
  gaps reliably escape. F-A5-007 quantifies the delta: 10 HIGH findings
  surfaced only after the merge pass.
- **Magic constants drifted from intent comments.** `_EMBED_SIZE_LIMIT = 200 * 1024  # 100 KB`
  is value/comment mismatch with no enforcement. F-A5-008 derived the
  constant from `MAX_ARG_STRLEN` as the only stable fix.
- **`detect_*()` functions that scan only one stream.** Defense-in-depth gap
  by construction — the error surface (stderr) is never inspected.
  F-A5-002 required both extending the function AND plumbing the file from
  the call site (two separate fixes, S2-D + S2-E).
- **Validation-document analysis lines pasted from prior versions** without
  re-grepping the current file. Off-by-one and 4-line truncation noted in
  F-A5-006 across CBS-1..CBS-4.
- **Hash-based resume with no semantic distinction.** Resume logic treats
  spec hash as a black box. F-A5-005 fix introduces an evidence-gated
  CLI command (`accept-spec-change`) that requires a deviation record
  with `spec_update_required: true` before mutating state — semantic
  authorization replaces binary hash equality.
- **Roadmap-generator-side renumbering and invented IDs** (F-A5-009).
  Generator behavior is not under spec-fidelity gate's authority; the
  gate catches the artifact but not the cause.

## Budget note

- Files Read: 14 (lists/grep helpers excluded)
- Files Skipped (over budget): >60 (debate transcripts, per-phase tasklists,
  validation/archive/agent-CC*/agent-D* sub-reports across v3.7,
  diff-analysis.md, roadmap-{opus,haiku}-architect outputs, execution-logs)
- Auggie lookups: 0 (no failure rose to the bar — every finding had
  in-partition spec-and-fix paper trail sufficient for the discovery tier)
