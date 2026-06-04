# Research Completeness Verification

**Topic:** Sprint CLI per-task execution + handoff wiring (Stages 0–3)
**Date:** 2026-06-03
**Files analyzed:** 6 (01-file-inventory, 02-patterns-conventions, 03-wiring-seams, 04-test-verification, 05-data-flow, 06-template-and-examples)
**Depth tier:** Deep (implementation-grade wiring research)
**Authoritative spec:** .dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md §6 (HIGH) + §7 (MEDIUM/LOW)

---

## SYNTHESIS finding inventory (the coverage target)

Per §6/§7 the builder must produce evidence-bound items for: **6 HIGH** (H1 isolation per-path merge, H2 corrected Stage-0 gate, H3 task_complete↔task_rerun_complete reconciliation, H4 frozen HandoffRecord schema, H5 resume contract predicate+key+CLI, H6 Stage-3 shared-state inventory + testable env seam + dep-primitive reuse), **7 MEDIUM** (M1 dep-primitive reuse [folded into H6], M2 _jsonl concurrency ordering, M3 per-task prompt composition table, M4 flag+config plumbing, M5 migration/back-compat, M6 heading-regex warn-only global routing, M7 versioned-not-frozen Stage-1 gate), and **5 LOW** (L1 T02.06 reconciliation [folded into Reconciliation note], L2 Stage-4 rollback reword, L3 crash-consistency asymmetry test, L4 remaining test gaps, L5 documentation tasks). Note: Stage 4 (agent-mail) and Stage C (coordinator) are explicitly OUT of the Stage 0–3 track goal; L2/L4(c)/Stage-4 items are deferred-stage and not required to be builder-actionable for this tasklist.

---

## Check 1 — Source files identified with paths + exports + CURRENT line numbers

**PASS (Strong).**

R1 (01-file-inventory) is the authoritative inventory and explicitly states every symbol was "verified by Read with current line numbers" (R1:325). It covers all 8 in-scope files (executor.py, config.py, process.py, logging_.py, checkpoints.py, models.py, rerun_tasks.py, commands.py) with a DEAD-or-LIVE status table (R1:25-39) — the single most load-bearing distinction for a wiring job.

Current-line evidence is consistent and cross-corroborated across files: e.g. `setup_isolation` executor.py:151 (R1:61, R3:39), `_run_task_subprocess` executor.py:1079 (R1:87, R3:142, R5:64), hardcoded `turns_consumed=0` at executor.py:1117-1118 (R1:90, R3:172-179, R4:90-94, R5:110), the fork `if tasks:` at executor.py:1265 (R1:99, R3:240, R5:27). The four files that cite the same symbols agree on line numbers — strong evidence the lines are current, not drifted spec lines. The SYNTHESIS itself warns its own lines drifted +4..+55 (§6 anchor note) and explicitly says "anchor on symbols, not lines"; the research correctly re-derived current lines.

The CRITICAL ATTRIBUTION CORRECTION (R1:9-19) resolves the spec's models.py-vs-config.py confusion with verified line numbers (`SprintConfig` models.py:407, `TurnLedger` models.py:758, `task_output_file` models.py:561, `resume_command` models.py:677). This directly answers checklist item 7.

No gaps. Every wiring-relevant symbol has a path + current line + LIVE/DEAD status.

## Check 2 — Wiring seams concrete enough for per-edit checklist items

**PASS (Strong).**

R3 (03-wiring-seams) gives per-seam current code + required change + cross-effects for all seven named seams:

| Required seam | Covered | Evidence |
|---|---|---|
| setup_isolation per-path merge (H1) | YES | R3 §1 — confirms CONFLICT: setup_isolation's CLAUDE_WORK_DIR=release_dir clobbers Path A's phase-scoped isolation_dir (R3:43-52); gives explicit ADD-only merge code for Path A (R3:62-69) and full-set injection for Path B (R3:76-85); proposes `setup_isolation(config, scope=...)` parameterization (R3:87). |
| build_task_context wiring | YES | R3 §2 — results accumulate at executor.py:965/1066; recommends threading `prior_context=` param into `_run_task_subprocess` (R3:113); notes consumed_upstreams narrowing not yet implemented (R3:116). |
| write_task_complete call site | YES | R3 §3 — exact slot after `results.append` executor.py:1066 (R3:127); flags the BLOCKER that SprintLogger is not in scope (cross-cutting seam R3:12, restated R3:132). |
| _subprocess_factory env seam (H6) | YES | R3 §4 — confirms factory returns tuple directly bypassing build_env (R3:147-150); proposes `_task_env()` helper + `_env_capture` param (R3:154-162); notes #1-PathB and #4 are the same edit (R3:166). |
| turns_consumed capture | YES | R3 §5 — literal 0 at executor.py:1118; capture via stream-json final `result` event num_turns (R3:184-189); flags checking summarizer/OutputMonitor for existing parser. |
| TurnLedger thread-safety | YES | R3 §6 — RMW mutator table (R3:199-207); identifies check-then-act TOCTOU spanning can_launch→debit (R3:209); prescribes atomic `try_launch()` + lock, NOT per-method guards. |
| heading-regex router (M6) | YES | R3 §7 — regex at config.py:380-383, near-miss failure modes enumerated (R3:224); fork at executor.py:1265 via `_parse_phase_tasks` returning None/[]; warn-only fix belongs in `_parse_phase_tasks` with a SEPARATE probe, never widen the extraction regex (R3:242-244). |

The "two edits collapse into one each" closing note (R3:258) is exactly the kind of guidance that lets a builder write minimal, non-redundant per-edit items. Seams are concrete to the file:line and include the actual replacement code shape. No gaps.

## Check 3 — Test seams + per-stage acceptance approach

**PASS (Strong).**

R4 (04-test-verification) covers every required test surface:
- **Deterministic `_subprocess_factory` pattern** — documented as "Pattern A" with canonical refs test_wiring_integration.py:200-210, test_executor.py:610-618 (R4:25-37).
- **Real-spawn e2e for turn-count** — "Pattern B" via e2e_real/conftest.py `claude_shim`+`real_release` fixtures (R4:39-52); the Stage-0 turn-count test is correctly placed in e2e_real because only the real-spawn path hits the hardcoded-0 line (R4:105). Crucially R4 explains WHY no existing test catches the bug (factory injects synthetic turns, R4:97-98) — the corrected "assert exactly N, not !=0" gate is captured (R4:105, matches §6 H2/Reconciliation).
- **Concurrency/race harness** — §4 honestly corrects the premise (the loop is SEQUENTIAL today, there is NO FileHandoffStore, R4:111-114) and gives the ≥4-writer ≥1000-run JSONL-readback structure (R4:119-122), modeled on test_parallel_15.py:222-238.
- **Benchmark harness** — test_nfr_benchmarks.py (p95) and test_wiring_performance.py templates (R4:124-127).
- **Existing tests that must stay green** — T02.05 isolation probe (test_isolation_layers_probe.py) pins the exact 4-field IsolationLayers API in order (R4:58-59), with the explicit warning that any new isolation field must keep those 4 fields/order or update `_EXPECTED_FIELDS` in lockstep. Plus the per-stage extend/add map (R4 §6) and the strongest backward-compat guardrail (test_backward_compat_regression.py, R4:83). T02.05/T02.06 reconciliation is fully addressed (R4 §5, R4:160).

No gaps. This is the most directly builder-actionable test research.

## Check 4 — Patterns documented with examples

**PASS (Strong).**

R2 (02-patterns-conventions) supplies copy-ready idioms with file:line:
- **Atomic temp+replace** — checkpoints.py:207-210, full idiom + the 5 exact conventions a FileHandoffStore must replicate (R2:18-35).
- **SprintLogger event shape** — `_jsonl` append-mode + `"event"`-first dict + trailing isoformat timestamp (R2:70-96); the full `write_task_rerun_complete` schema table that a new `write_task_complete` must reconcile with, including the field-name divergence `turns`/`duration_sec` vs dataclass `turns_consumed`/`duration_seconds` (R2:120-135).
- **Dataclass/to_dict** — TaskResult as the HandoffRecord template, hand-written dict literal (NOT asdict), enums→.value, datetimes→.isoformat(), matching from_dict round-trip (R2:148-218).
- **click→config plumbing** — the three-layer lockstep (run() param → load_sprint_config kwarg → SprintConfig field) with all option styles (int/bool/dual/Choice) and the SprintConfig field/Literal/property conventions (R2 §4–§5).

No gaps.

## Check 5 — Template-02 rules + TB-Add-1..8 gate requirements captured

**PASS (Strong).**

R6 (06-template-and-examples) covers the template surface thoroughly:
- **Path correction** — real template is `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`; `.claude/templates/workflow/` does NOT exist (R6 §0). This is a real, verified `template_schema_doc` trap.
- **Template-02 structure** — frontmatter, PART-2 section ordering, B2 6-element item pattern, A3/A4, L1–L6 + M1 gate + F2/I15/I16/I17/I18, FORBIDDEN patterns (R6 §1).
- **Concrete example** — TASK-RF-OVM-VERIFICATION-GAP-CLOSURE with real B2 item formatting and M1 QA-gate encoding (R6 §2).
- **TB-Add-1..8** — authoritatively cited from task-builder SKILL.md L1165-1173/L1972-1979 with a per-gate table and the critical TB-Add-7/8 ↔ Execution Context interaction (header = area names with NO paths per NFR-CONV.3; items = file:line citations) (R6 §3).

No gaps.

## Check 6 — Granularity sufficient for per-file / per-wiring-edit / per-test items

**PASS (Adequate-to-Strong).**

The research is granular enough that a builder can write one item per edit:
- Per-edit granularity: R3 names the exact insertion line for each of the 7 seams, and the "two edits collapse into one" notes (R3:166, R3:258) prevent the builder from over-splitting (TB-Add-5 alignment).
- Per-file granularity: R1's symbol-by-symbol table maps each change to a single file + symbol.
- Per-test granularity: R4 §6's per-stage extend/add map names specific new test files (`test_e2e_turn_count.py`, `test_handoff_store.py`, `test_handoff_concurrency.py`, `test_handoff_performance.py`) and the existing files each stage must keep green.

One soft caveat (not a blocker): some seams are inherently multi-edit (H1 touches both Path A merge AND Path B injection AND a setup_isolation signature change; H6 touches `_task_env` + `_env_capture` + the scheduler). The research flags these couplings explicitly, so the builder can decide split-vs-bundle with a justifying comment per TB-Add-5 — the evidence to make that call is present.

## Check 7 — Cross-cutting corrections captured

**PASS (Strong).** Every named correction is present and evidence-bound:

| Correction | Captured | Evidence |
|---|---|---|
| models.py vs config.py attribution | YES | R1:9-19 CRITICAL ATTRIBUTION CORRECTION with verified lines; restated R1:337. |
| SprintLogger not threaded into execute_phase_tasks | YES | R3 cross-cutting seam (R3:12) + R3 §3 BLOCKER (R3:132): signature executor.py:928-941 has no logger param; logger.* calls only in execute_sprint. |
| no FileHandoffStore yet | YES | R4:111-114 (grep → zero matches for FileHandoffStore/HandoffStore/handoff_store) + R5:113; the real surfaces (output files, phase-N-result.json, execution-log.jsonl, dead build_task_context) enumerated. |
| walk_dependencies single-level (not transitive closure) | YES | R5 §3 — explicitly corrects the docstring's "transitive" wording: it is a single-level expand, not a closure (R5:250-253); cross-phase aware via checkpoint fallback (R5:254-259). |
| T02.05/T02.06 reconciliation | YES | R4 §5 — T02.05 = frozen isolation API pin (keep green); T02.06 = the turn-counting dead wire at executor.py:1117 (R4:135-137); "do not silently re-use T02.06" (R4:160). Matches SYNTHESIS Reconciliation note. |

Additional corrections the research surfaced beyond the brief's list (all bonus, all evidence-bound): the SYNTHESIS's own [CORRECTED] markers (task_rerun_complete exists; CLAUDE_SETTINGS_DIR set only in dead code; TaskEntry.dependencies NOT virgin — rerun_tasks consumes it) are independently re-confirmed by R1/R4/R5. The template_schema_doc dead-path trap (R6 §0) is a correction the builder would otherwise propagate from the reference example's own buggy frontmatter (R6:143).

## Check 8 — Unresolved ambiguities documented

**PASS (Adequate).** Open decisions are surfaced where they exist, and they are decisions the builder/spec resolves, not research gaps:
- R3:113-114 — build_task_context wiring: thread-param (recommended) vs compute-in-factory (rejected, with reason). `start_commit` not in scope → pass "" (diff section skipped). Decision surfaced.
- R3:132 — write_task_complete: thread logger (recommended) vs post-hoc loop in execute_sprint (viable, with the tradeoff stated: loses real-time interleave but TaskResult already carries started_at/finished_at). Decision surfaced.
- R3:184-191 / R4:105 — turns parser: check whether summarizer/OutputMonitor already extracts num_turns before writing a new parser. Flagged as a thing-to-verify, not assumed.
- R5:139-151 — "validated successful" predicate: status==PASS is the floor (is_success, models.py:54-56); whether to AND gate_outcome.is_success is surfaced as a choice (matches §6 H5). 
- R4:119-122 — the race test "will FAIL against the current lock-free _jsonl" — correctly framed as the POINT of the Stage-3 gate, not a contradiction.

These are all resolvable from the SYNTHESIS §6/§7 decisions (which the research cross-references). No silent unknowns that would block authoring.

---

## Per-finding coverage matrix (§6/§7 → research evidence)

The decisive test for this gate: can a builder write concrete evidence-bound items for ALL of Stages 0–3 covering every in-scope finding? Mapping each finding to its supporting research:

| Finding | Stage | Builder-actionable? | Supporting research |
|---|---|---|---|
| H1 isolation per-path merge | 0 | YES | R3 §1 (merge code both paths), R1:59-62/106, R5:61-79 |
| H2 corrected Stage-0 gate (serial smoke + concurrent repro) | 0 | YES | R4 §3 (turn-count e2e), R4:58-59 (isolation probe stays green); concurrent-repro harness R4 §4c |
| H3 task_complete ↔ task_rerun_complete reconciliation | 0/1 | YES | R2 §2c (full rerun schema + field-name divergence), R3 §3, R1:180-181 |
| H4 frozen HandoffRecord schema | 1 | YES | R2 §3 (TaskResult.to_dict template + from_dict round-trip), R5:165-178 (what JSON already carries), §6 H4 gives the literal dataclass |
| H5 resume contract (predicate+key+CLI) | 2 | YES | R5 §2 (predicate is_success, write/read seams, no per-task skip-list today), R1:240-248 (resume_command phase-granular), §6 H5 gives key form |
| H6 shared-state inventory + env seam + dep reuse | 3 | YES | R3 §4 (_env_capture seam), R3 §6 (TurnLedger TOCTOU), R5 §3 (walk_dependencies/_dependencies_of reuse), §6 H6 lists the shared-state set |
| M1 dep-primitive reuse | 3 | YES | R5 §3 (the exact `_dependencies_of`/`_is_satisfied` shapes to reuse) |
| M2 _jsonl concurrency ordering | 1→3 | YES | R3:136 (lock-free), R4:114 (no fcntl/flock), R3 §6 |
| M3 per-task prompt composition | 1 | YES | R3 §2 (build_task_context supplies sections), R1:146-148 (build_prompt is whole-phase), §7 M3 gives the section table |
| M4 flag + config plumbing | 1/3 | YES | R2 §4 (three-layer click→config lockstep), R1:296-319 (run() has no per-task flag) |
| M5 migration / back-compat | 1/2 | YES | R4:83 (backward-compat-regression guardrail: events inert on non-handoff sprint), R5:194-201 |
| M6 heading-regex warn-only global routing | 1 | YES | R3 §7 (separate probe, never widen extraction regex; regression corpus over Path-A phases) |
| M7 versioned-not-frozen Stage-1 gate | 1 | YES | R2 §3c (from_dict .get back-compat), H4 schema_version field; migration test approach in R4 |
| L1 T02.06 reconciliation | 0 | YES | R4 §5 |
| L3 crash-consistency asymmetry test | 1/2 | YES | R3:136 (crash between handoff write and _jsonl append → resume treats handoff file as authoritative) |
| L5 documentation tasks | per-stage | YES | R6 template covers docs/changelog sub-task placement (I-rules); surface list from R2 §4 |
| L2 Stage-4 rollback reword | 4 (OUT) | N/A | Out of Stage 0–3 track goal |
| L4(c) Stage-4 mail failover | 4 (OUT) | N/A | Out of Stage 0–3 track goal |
| L4(a) wall-clock baseline | 3 | YES | R4 §4d (nfr_benchmarks p95 template) |
| L4(b) DAG+resume in-flight-at-kill | 3 | YES | R5 §2 (skip decision seam) + R5 §3 (dependents must not launch) |

**Every in-scope finding (all 6 HIGH, all 7 MEDIUM, the in-scope LOWs) has concrete file:line-bound supporting research.** Nothing blocks a builder from authoring Stages 0–3.

## Contradictions Found

**None material.** Cross-file claims are consistent. Two apparent tensions, both reconciled rather than contradictory:

1. **Path A/B lettering.** R1/R3/R5 all note the SYNTHESIS §6-H1 lettering is "opposite of intuitive" (Path A = the per-phase *fallback*; Path B = the per-task primary), and R3:10 + R5:17/71 explicitly state which concrete branch each letter maps to. R3 follows the SYNTHESIS letter convention (A=per-phase, B=per-task); R5 §1 header says "Path A (per-task) vs Path B (single proc)" in its title line (R5:17) which is the REVERSE of R3, but R5's body immediately and correctly maps "Path A = the `if tasks:` per-task branch" (R5:27-38) and "Path B — single ClaudeProcess" (R5:71). So R5's title line uses the inverted lettering while its body uses the SYNTHESIS lettering. **This is a labelling inconsistency between R3 and R5's title, NOT a factual contradiction** — both agree on the underlying code (per-task branch at executor.py:1265, single-proc fallback at 1309). FLAG for the builder: anchor items on the concrete branch/symbol (`if tasks:` at executor.py:1265, `_run_task_subprocess`) and the line number, never on the bare letter "A"/"B", because the two research files letter them oppositely.

2. **"transitive" wording.** SYNTHESIS §5 and rerun_tasks docstring say walk_dependencies is "transitive"; R5 §3 corrects this to single-level-expand. Not a research contradiction — R5 is correcting the source, and flags it explicitly (R5:250-253).

## Depth Assessment

**Expected depth:** Deep (implementation-grade wiring research feeding a Template-02 per-edit tasklist).

**Actual depth achieved:** Deep, met. Evidence: data-flow traces end-to-end (R5 §1 fork → §2 handoff write/read → §3 dependency walk → §4 ledger touch-order), integration-point mapping with replacement code (R3), per-stage test seams with existing-test-must-stay-green analysis (R4), and pattern extraction with copy-ready idioms (R2). The DEAD-vs-LIVE distinction (R1) is exactly the depth a wiring (not greenfield) task needs.

**Missing depth elements:** None that block authoring. Two items are appropriately flagged as verify-during-build rather than pre-resolved (existence of a num_turns parser in summarizer/OutputMonitor; whether to AND gate_outcome into the resume predicate) — these are implementation decisions, not research gaps.

---

## Compiled Gaps

### Critical Gaps (block synthesis/authoring)
- **None.**

### Important Gaps (affect quality)
- **None.** (The Path A/B lettering tension is a labelling note, mitigated by anchoring on symbols/lines — see Contradictions #1.)

### Minor Gaps (note, do not block)
- **R2 frontmatter says "Status: In Progress" at line 4 but "Status: Complete" at the end (line 349).** Cosmetic header staleness — the file IS complete (all 5 sections present with a full Summary). Builder/orchestrator may ignore; flagged per checklist item 4 (completeness header check).
- **Path A/B lettering divergence between R3 and R5's title line** (Contradictions #1). Mitigation: builder anchors on `if tasks:` (executor.py:1265) / `_run_task_subprocess` symbols, not the letter.
- **num_turns parser existence** (R3:189, R4: implied) — flagged as verify-during-build. Builder should add an item to grep summarizer/OutputMonitor before writing a new parser, to honor scope discipline.

## Recommendations

1. **Proceed to tasklist authoring.** All eight completeness checks PASS; every in-scope §6/§7 finding has concrete file:line-bound research.
2. **In the tasklist, anchor every wiring item on a symbol + current line, never on the bare Path "A"/"B" letter** — R3 and R5 letter the two paths oppositely in places. Use `if tasks:` @ executor.py:1265 (per-task) and the single-proc fallback @ executor.py:1309 with the symbol names.
3. **Add a verify-first item for the num_turns parser** (grep summarizer/OutputMonitor) before the Stage-0 turn-count capture item, so the builder doesn't duplicate an existing parser.
4. **Set `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"`** — do NOT copy the reference example's dead `.claude/templates/...` path (R6 §0/§2a).
5. **Keep T02.05 isolation probe green** — any new IsolationLayers field must keep the 4 fields in order or update `_EXPECTED_FIELDS` in lockstep (R4:58-59); add this as an explicit acceptance note on the H1 item.
6. **Honor the TB-Add-7/8 split** — Execution Context header = source-area NAMES with no paths; per-item Context = full file:line citations (R6 §3a).

---

## VERDICT: PASS

All 6 research files are complete and evidence-bound. All eight completeness checks PASS. The research collectively enables a builder to write concrete, file:line-anchored Template-02 items for **all of Stages 0, 1, 2, 3**, covering **all 6 HIGH (H1–H6), all 7 MEDIUM (M1–M7), and the in-scope LOW findings** of SYNTHESIS §6/§7. No critical or important gaps. Three minor, non-blocking notes recorded above (R2 header staleness; Path A/B lettering — anchor on symbols; num_turns parser — verify before building).
