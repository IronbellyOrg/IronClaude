# QA Report — Task-Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**ADVERSARIAL STANCE:** assume the builder dropped or misrepresented research findings.

**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md
**Research dir:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/
**Date:** 2026-07-01
**Files analyzed:** 4 research files + research-notes.md + BUILD-REQUEST.md + design.md + merged-requirements.md + the 500-line task file; load-bearing code seams spot-checked against the live tree.

---

## VERDICT: PASS

The task file faithfully reflects every significant research finding. Each consumed seam, every package module, every integration point, every test area, every template/QA constraint, and all three open decisions have a corresponding grounded task item. No task item fabricates actions beyond what research, the design, or the requirements establish. Two minor observations are recorded below as non-blocking hardening notes (the second is intentionally an acceptable design choice, not a defect).

This lens (task-research alignment) is distinct from the two prior task-validation verification reports in `qa/` (structural + content, both PASS), which covered template conformance, operational executability, and seam existence. This report specifically cross-validates the research-to-task coverage axis.

---

## Methodology

1. Read all four research files (01-file-inventory, 02-patterns-integration, 03-validation-tests, 04-template-examples), research-notes.md, and BUILD-REQUEST.md in full.
2. Read the ground-truth design.md and merged-requirements.md in full to establish what the task *must* encode.
3. Read the complete 500-line task file (all 5 phases, 40 numbered steps, 86 checklist items, Task Log).
4. For each research finding category, enumerated the expected task coverage and searched the task file for the corresponding item.
5. Spot-checked every load-bearing code seam the research cites (and the task depends on) against the live tree to rule out inherited fabrication.
6. Confirmed the 16 setup-question IDs, the 9 UX states, and the 12 safe-lock predicates in the task match the source requirements/design verbatim.

---

## Coverage Matrix — Research Finding → Task Item

### 1. Consumed seams (research 01 §"Existing pr_submit files", research 02 §2, design seam table)

| Consumed seam | Research citation | Task item grounding it | Status |
|---|---|---|---|
| `DetectionContract.load()` preserved | 01:41; 02:22; design seam table | Step 2.3 "reuse `_LOCAL_OVERRIDE_REL`, `DetectionContract.load()`, `DetectionContract.from_yaml()`…never changes `DetectionContract.load()` or `for_arming()` behavior"; Key Constraint line 126; QA lens no-side-effect-static-boundary (240) | COVERED |
| `DetectionContract.for_arming()` preserved | 01:42; 02:25; design §10.1 | Step 2.10 "`/sc:pr-submit --monitor >=1` still fail-closes through `for_arming()`"; Step 4.6 "post-lock use of existing `DetectionContract.for_arming()`" | COVERED |
| `classify()` + result literals reused, not duplicated | 01:46; 02:24 | Step 2.7 "dry-runs the existing `classify(evidence.combined_payload, candidate.contract)` seam…classifier logic is not duplicated" | COVERED |
| Local override path `.dev/pr-monitor/detection-contract.locked.md` | 01:41; 02:17 | Step 2.9 "only lock destination is `…/.dev/pr-monitor/detection-contract.locked.md`"; Step 4.5 writer test | COVERED |
| `_LOCAL_OVERRIDE_REL` reuse | 01:41 | Step 2.3 "reuse `_LOCAL_OVERRIDE_REL`" | COVERED |
| T-210 `DetectionContractLocked` unchanged | 02:21; design seam table | Step 2.10 fail-close preserved; Step 4.6 integration test preserves fail-closed; Step 4.1/4.10 do not weaken `test_t210_locked_false_halts` | COVERED |

Live-tree verification (this audit): `DetectionContractLocked` at detection.py:71; `load` at :148 with `require_locked`/`prefer_local_override` params; `for_arming` at :191; `_LOCAL_OVERRIDE_REL = Path(".dev/pr-monitor/detection-contract.locked.md")` at :40; T-210 raise at :184. All seams exist as cited — no inherited fabrication.

### 2. Package decomposition (research 01 §"Design target", design §2)

| Design-named module | Dedicated task step | Status |
|---|---|---|
| `__init__.py` (facade) | Step 2.1 | COVERED |
| `states.py` (9-state enum) | Step 2.2 | COVERED |
| `diagnosis.py` (`Diagnosis` + `diagnose()`) | Step 2.3 | COVERED |
| `evidence.py` (`EvidenceBundle` + `load_evidence()`) | Step 2.4 | COVERED |
| `questions.py` (`SETUP_QUESTIONS`, 16 IDs) | Step 2.5 | COVERED |
| `candidate.py` (`FieldProvenance`, `CandidateContract`, `derive_candidate()`) | Step 2.6 | COVERED |
| `validation.py` (`CheckResult`, `ValidationReport`, `validate_candidate()`) | Step 2.7 | COVERED |
| `lockgate.py` (`LockGate`, 12 predicates) | Step 2.8 | COVERED |
| `writer.py` (`write_report`, `write_lock`, error model) | Step 2.9 | COVERED |

All 9 design-named modules have a dedicated, single-responsibility creation step. The facade exports (`diagnose`, `load_evidence`, `derive_candidate`, `validate_candidate`, `write_report`, `write_lock`) in Step 2.1 match design §4 verbatim.

Live-tree verification: `src/superclaude/pr_submit/contract_setup/` does not yet exist — correctly a new package, not pre-existing.

### 3. Integration points (research 02 §1-5, design §10)

| Integration point | Research citation | Task item | Status |
|---|---|---|---|
| pr-submit missing-contract halt (better diagnostics, before Monitor arm) | 02:13-17, §6 | Step 2.10 (render diagnosis + canonical sentence, `--monitor 0` unaffected) | COVERED |
| Canonical no-side-effect sentence | 02:70; req §9.5 | Steps 2.10, 3.3, 4.6 encode verbatim "No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed." | COVERED |
| reflect `contract-status` sibling Click command | 02 §4; design §10.3 B1 | Step 3.1 (gated on OQ-2 = `sibling-cli-command`) | COVERED |
| `reflect_group` registration surface (no new top-level wiring) | 02:45 | Step 3.1 uses `@reflect_group.command("contract-status")` | COVERED |
| Lazy import pattern inside command body | 02:44 | Step 3.1 "calls the `contract_setup` facade lazily" | COVERED |
| reflect command/skill doc coherence | 02 §4b; 02:91 | Step 3.2 | COVERED |
| pr-submit command/skill doc coherence | 02 §7 | Step 3.3 | COVERED |
| `make sync-dev && make verify-sync` after source doc edits | 02 §7; 04:54 | Steps 3.4, 5.2c (+ rejection of `.claude/` staging in 5.6) | COVERED |

Live-tree verification: `reflect_group` at commands.py:48; `run` subcommand at :76/:180 (tasklist positional arg at :79 — confirms the task's claim that contract-status must run without a tasklist); `main.py` registers `reflect_group` as `reflect` at :440-442. All integration surfaces exist as cited.

### 4. Tests (research 03, design §12)

| Research-03 test area | Task test module | Status |
|---|---|---|
| §1 diagnosis + state classification | Step 4.1 `test_contract_setup_diagnosis.py` | COVERED |
| §2 candidate derivation + 16 questions | Step 4.2 `test_contract_setup_questions.py` (16 IDs asserted in order) | COVERED |
| §3 validation report + redaction | Step 4.4 `test_contract_setup_validation.py` | COVERED |
| §4 omitted-surface + cross-PR/staleness | Step 4.3 `test_contract_setup_evidence.py` (omitted-surface distinctness, cross-PR shape-only, stale) | COVERED |
| §5 safe writer + no shipped/.claude writes | Step 4.5 `test_contract_setup_writer.py` | COVERED |
| §6 pr-submit halt integration | Step 4.6 `test_contract_setup_pr_submit_integration.py` | COVERED |
| §7 reflect contract-status CLI | Step 4.7 `test_contract_status_cli.py` + docs parity | COVERED |
| Existing regression pack (T-210, monitor-arm, autonomy, validation-gate) | Steps 4.10, 4.8 | COVERED |

All 7 new test modules map 1:1 to research-03 recommended test files. Live-tree check confirms none pre-exist and all referenced existing tests (`test_detection_contract.py`, `test_monitor_arm.py`, `test_autonomy_gates.py`, `test_validation_gate.py`, `test_cli_smoke.py`, `test_docs_cli_parity.py`) do exist.

### 5. Template / QA constraints (research 04, BUILD-REQUEST)

| Constraint | Source | Task encoding | Status |
|---|---|---|---|
| Template 02 (complex) | 04 §"Template 02 required structure"; BUILD-REQUEST TEMPLATE:02 | frontmatter `template: "02-complex-task"`, `template_schema_doc` → source-of-truth 02 template | COVERED |
| B2 self-contained single-paragraph items | 04:22 | Every actionable checkbox is a B2 paragraph with context/action/output/verification/completion-gate (verified across body) | COVERED |
| Per-phase lens-based QA gates + serialized fix authorization | 04:30-34; BUILD-REQUEST QA_INTENSITY:full, QA_GATE_REQUIREMENTS:PER_PHASE | Each phase has lens-spawn → consolidate → decide-fix → single fix agent (`fix_authorization: true`) → structural verify → content verify → gate PASS | COVERED |
| Flat post-reflect wrapper, penultimate before Done | 04:39-41; BUILD-REQUEST POST_REFLECT_GATE:ENABLED | Step 5.6 (`superclaude reflect run … --depth deep --fix --promote`, recursion breaker, no `--base`/range) immediately before Step 5.7 Done | COVERED |
| `/task <abs path>`, never `/sc:task` | 04:53; BUILD-REQUEST | Execution Command section line 144; QA lenses forbid `/sc:task` routing | COVERED |
| Source-of-truth `src/` first, never stage `.claude/` | 04:54; CLAUDE.md ABSOLUTE RULE | Steps 3.4, 5.6 (explicit per-path staging + `.claude/`-staged rejection grep) | COVERED |
| Stage new files before post-reflect | 04:78 | Step 5.6 stages explicit task-relevant paths before wrapper shell-out | COVERED |
| UV-only, scoped ruff | 03 §"UV-only validation commands"; BUILD-REQUEST | Steps 4.8-4.11, 5.2/5.2b (all `uv run`; ruff scoped to changed trees only) | COVERED |

### 6. Open decisions (research-notes GAPS, design §14, BUILD-REQUEST OPEN QUESTIONS)

| OQ | Recommended default | Task gate item | HALT-before-dependent wiring | Status |
|---|---|---|---|---|
| OQ-1 helper granularity | package | Step 1.3 | PENDING → "HALT before Phase 2 dependent implementation" | COVERED |
| OQ-2 reflect surface | sibling-cli-command | Step 1.4 | PENDING → "HALT before Phase 3 dependent implementation" | COVERED |
| OQ-3 live capture | file-based-v1-only | Step 1.5 | PENDING → "HALT before evidence implementation" | COVERED |

All three open decisions are encoded as Phase-1 `needs_human_decision` gates with explicit PENDING→HALT semantics, and each dependent phase (2←OQ-1, 3←OQ-2, evidence←OQ-3) re-confirms its gating OQ is non-PENDING before proceeding (Steps 2.1, 2.4, 3.1). No recommended default is silently auto-applied — the Phase-1 QA gate (decision-gate-structure lens) explicitly FAILs if "any dependent phase could proceed without a non-PENDING decision or any default is silently auto-applied."

---

## Fabricated / Ungrounded Action Check

Searched every task action for claims not grounded in research/design/requirements:

- **No phantom modules**: every Python module the task creates is named in design §2's package tree.
- **No phantom symbols**: every facade export, dataclass, and function name traces to design §3-§4.
- **No phantom file paths**: every existing-file reference (detection.py, classifier.py, reflect/commands.py, command/skill docs, existing tests, template 02) verified to exist in the live tree.
- **No phantom CLI surface**: `reflect_group` and its `run` subcommand exist; the task adds a sibling, matching research-02 §4's recommendation and the existing registration pattern in main.py:440-442.
- **No invented acceptance criteria**: the 16 setup-question IDs, 9 UX states, 12 safe-lock predicates, and canonical sentence all match merged-requirements §3/§4/§6/§9 and design §3.1/§6/§7 verbatim.
- **Error model**: `ContractSetupRefused` / `EvidenceUnreadable` / `ContractSetupError` (Step 2.9) trace directly to design §11.
- **Shipped contract invariant**: research 02:8 + design §1 non-goal "shipped ref stays `locked:false`" → encoded in Steps 2.2/2.9/4.5 and the structure-check assertion. Live check confirms shipped ref is `locked: false` (refs/detection-contract.md:29).
- **`.dev/pr-monitor/` gitignored**: design §9 cites `.gitignore:243`; live check confirms `.dev/pr-monitor/` at .gitignore:243.

No fabricated actions found.

---

## Observations (non-blocking)

### O-1 (MINOR): No dedicated static grep-style no-side-effect test module

Research-01 line 118 recommends a dedicated `test_contract_setup_no_side_effects.py` — "grep-style guard that setup paths do not arm Monitor or call push/reply/resolve/retrigger… mirrors the design's critical invariant test at design.md:559-561." Design §12 explicitly calls `test_no_monitor_side_effects` the "critical invariant test."

The task does **not** create a standalone static-grep test module. Instead it distributes the invariant across: (a) the Phase-2 `no-side-effect-static-boundary` QA lens (line 240), (b) recorder-seam zero-call assertions in Steps 4.5/4.6, and (c) the Phase-4 `no-side-effect-test-strength` qualitative lens (line 350). This is a defensible alternative coverage strategy (runtime recorder assertions are arguably stronger than static grep), and the Phase-4 acceptance-traceability lens does not list a static-grep test among its required predicates — so this is not a gap that fails any encoded gate. Flagged only because research named a dedicated module and the task chose a different shape without noting the deviation. **Not blocking** — coverage of the invariant is present, just not as a standalone file.

### O-2 (INFORMATIONAL): OQ-1 single-module branch has no explicit adaptation item

If OQ-1 resolves to `single-module` rather than `package`, the task handles it only via a conditional clause in the Phase-2 preamble ("if OQ-1 records `single-module`, adapt the same facade/API into the approved module shape and log the deviation"). There is no separate per-module-creation step for the single-module shape. This is the correct design choice (the recommended default is `package`, and duplicating 9 steps for an alternative branch would violate B2/single-responsibility), and the deviation-logging path is explicit. Recorded for completeness; **not a defect**.

---

## Cross-Reference Integrity

- Every OQ decision unblocks the correct phase (1.3→Phase 2; 1.4→Phase 3; 1.5→evidence steps). Verified via the HALT clauses and the confirm-OQ-non-PENDING preconditions in Steps 2.1/2.4/3.1.
- Producer-before-consumer chains hold intra-phase: Step 2.8 (lockgate.py) precedes Step 2.9 (writer.py calls `LockGate.evaluate`); Steps 4.1-4.7 read the Phase-2 modules they test.
- Inter-phase gating: each phase's final gate requires both structural + content verification PASS before the next phase starts.
- The 12 safe-lock predicates (design §7) are encoded in Step 2.8 and asserted by the Phase-4 acceptance-traceability lens (line 348, "every one of the 12 safe-lock preconditions has at least one dedicated test") and the final crossref-chain lens (line 390, "the 12 safe-lock predicates each have a code+test anchor").

---

## Summary

- Research findings with expected task coverage: 6 categories, 40+ discrete findings
- Findings with a corresponding grounded task item: **all**
- Findings dropped or misrepresented: **0**
- Task items fabricating actions not grounded in research/design/requirements: **0**
- Non-blocking observations: 2 (O-1 dedicated static-grep module absent but invariant covered elsewhere; O-2 single-module branch handled by conditional, correct as designed)

## VERDICT: PASS

The task file is a faithful, complete translation of the research findings into executable task items, with no detectable dropped or misrepresented research and no fabricated actions.
