# Research Notes: Post-R1 roadmap-pipeline brittleness-elimination follow-ups (5 items)

**Date:** 2026-06-03
**Scenario:** A (explicit — goal, scope, files, branch, constraints all given)
**Depth Tier:** Deep (5 follow-up areas, multiple roadmap-pipeline subsystems, ~7800 LOC across target modules)
**Track Count:** 1 (user requested a single Sprint-CLI-compatible MDTM task with phase-gate QA)
**Status:** Complete

**Source of follow-ups:** `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` §"Follow-Up Items Identified" (L1115-1133).

**The 5 requested items (verbatim mapping):**
1. **Area A** — delete stale `tests/integration/test_wiring_pipeline.py` (orphaned `WIRING_GATE` import → pytest collection error). `WIRING_GATE` symbol STAYS in `cli/audit/wiring_gate.py`. (follow-up L1124)
2. **Area B** — generator-side phantom-ID **PREVENTION**: extend the R1.4 tool-write id-check (`render_step_tool_write_with_id_check` in `src/superclaude/cli/roadmap/tool_writer.py`) so generate/merge steps cannot **EMIT** roadmap_ids outside `envelope.spec_ids` at generation time, not merely catch them at the merge gate. (follow-up L1125)
3. **Area C** — opus-architect template-section adherence + spec-fidelity step performance (one ~1192s sub-agent timeout in live E2E). (follow-up L1126)
4. **Area D** — R1.4 markdown-path deletion after 3 consecutive parity-passing release cycles per Vector A. (follow-up L1122)
5. **Area E** — `spec_id_registry.json` dual-write removal + `remediate_parser.py` + MD-family `roadmap_ids` reconciliation. (follow-up L1127, L1128, L1132)

**Constraints (from request):** UV-only; edit `src/superclaude/` only; branch off `integration`; Sprint-CLI-compatible MDTM; phase-gate QA.

---

## EXISTING_FILES

### Area A — stale test deletion
- `tests/integration/test_wiring_pipeline.py` (13488 bytes, ~310 lines) — **TO DELETE**. Line 28: `from superclaude.cli.roadmap.gates import ALL_GATES, WIRING_GATE`. **Confirmed collection error**: `ImportError: cannot import name 'WIRING_GATE' from 'superclaude.cli.roadmap.gates'`. Also imports/uses `gate_passed`, `ALL_GATES`.
- `src/superclaude/cli/audit/wiring_gate.py` (line 1024: `WIRING_GATE = GateCriteria(...)`) — **PRESERVE**. The symbol intentionally lives here, NOT in `roadmap/gates.py`.
- `src/superclaude/cli/roadmap/gates.py` (1585 lines) — confirmed it does NOT export `WIRING_GATE` (that's the source of the orphaned import). Exports `ALL_GATES`, `gate_passed`.

### Area B — generation-time phantom-ID prevention
- `src/superclaude/cli/roadmap/tool_writer.py` (496 lines):
  - `validate_id_subset(roadmap_ids, spec_ids, accepted_deviations)` (~L346) — current invariant `roadmap_ids ⊆ set(spec_ids) ∪ set(accepted_deviations)`. Returns id_errors list.
  - `render_step_tool_write_with_id_check(...)` (~L455) — calls validate_id_subset; **skips check when spec_ids is empty/falsy** (L474-487, identity short-circuit). This is the merge-gate catch point.
  - `render_step_tool_write(...)` (~L421) — PLAIN render, no id-check.
  - `render_tool_output(tool_output, template_path)` (L120).
- `src/superclaude/cli/roadmap/envelope.py` (726 lines): `PipelineEnvelope.spec_ids: SpecIdRegistry` (L197); `envelope.spec_ids` is the SoT universe of allowed IDs.
- `src/superclaude/cli/roadmap/executor.py` (4266 lines): generate steps at L2515-2553 (`generate-{agent_a.id}` / `generate-{agent_b.id}`, `tool_write=config.tool_write_generate`); merge step at ~L2612 (`tool_write=config.tool_write_merge`). The render dispatch is L1237-1310 (`render_step_tool_write_with_id_check` at L1290 for id-check steps, `render_step_tool_write` at L1298 for plain).
- `src/superclaude/cli/roadmap/id_registry.py` (194 lines): `SpecIdRegistry` dataclass with `fr_ids/nfr_ids/sc_ids/g_ids/d_ids/md_ids` families; `build_id_registry()`.

### Area C — opus-architect adherence + spec-fidelity perf
- **"opus-architect" is NOT an agent `.md` file** — it is `AgentSpec(model="opus", persona="architect")`, parsed via `AgentSpec.parse("opus:architect")` (`models.py` L79-105). It is the DEFAULT generate agent (`commands.py` L434 `default="opus:architect"`). `.id` → `"opus-architect"` (filename slug, models.py L89).
- `src/superclaude/cli/roadmap/prompts.py`: `build_generate_prompt(...)`, `build_spec_fidelity_prompt(...)` (L388+). "template-section adherence" = generate step's roadmap-template section structure (the generate Step uses `tool_write_mode=_roadmap_template is not None`, `template_path=_roadmap_template`, executor L2531/2550).
- **Timeouts (executor.py):** generate steps `timeout_seconds=900` (L2525/2544); spec-fidelity step `timeout_seconds=600` (L2674), `retry_limit=1`. The observed **1192s** sub-agent timeout EXCEEDS both → the item is timeout/perf tuning + template-adherence improvement. Genuinely "Low" priority + partly diagnostic.
- `src/superclaude/cli/roadmap/fidelity_checker.py`, `convergence.py`, `semantic_layer.py` — spec-fidelity machinery (PRESERVE convergence path: `_run_convergence_spec_fidelity`).

### Area D + E — dual-write removal / markdown deletion / registry reconciliation
- `src/superclaude/cli/roadmap/models.py` (155 lines): **12 `tool_write_*` flags** (L127-155), ALL `default False` (markdown path is production). Each comment: "until cutover per Vector A >=3 release cycles."
- **No parity-cycle counter exists in code** — Vector A's "3 consecutive parity-passing release cycles" is an OUT-OF-BAND release-process gate (release notes / changelog), not a code-tracked counter. **Critical for items D/E scoping.**
- `src/superclaude/cli/roadmap/remediate_parser.py` (391 lines) — research/01 §A.6 (prior task) marks it a tool-write-collapse target; deletion deferred until R1.4 remediation cutover.
- `src/superclaude/cli/roadmap/remediate.py` — consumer of remediate_parser.
- `spec_id_registry.json` — written during dual-write (envelope.py L19-29, L146-150). `SpecIdRegistry` (id_registry.py) is the in-envelope replacement (R0.1 absorption). Dual-write = both `spec_id_registry.json` file AND `envelope.spec_ids` written; identical content.
- **MD-family reconciliation:** `md_ids` family (id_registry.py L89, L102, L128, L173 `families.get("MD")`; envelope.py L387-388 with `.get("md_ids", ())` back-compat). Prior task commit `8fd0edc9 fix(roadmap): close tool-write schema roadmap_ids MD-family drift via per-step contracts SoT` — MD-family drift was partially addressed; reconciliation completes it.

### Constraint surfaces
- `CLAUDE.md` — UV-only; `src/superclaude/` is SoT → `make sync-dev` → `.claude/`; `make verify-sync`; never commit `.claude/`; branch discipline.
- `pyproject.toml` / `Makefile` — `make test`, `make lint`, `uv run pytest`.

---

## PATTERNS_AND_CONVENTIONS

- **Config flags:** `models.py` `RoadmapConfig`-style dataclass; `tool_write_*: bool = False` with inline cutover comment. Removing dual-write = remove flag + remove the `if config.tool_write_X:` branch in executor + collapse to single path.
- **Step construction:** `executor.py` builds `Step(id=..., prompt=build_X_prompt(...), output_file=..., gate=X_GATE, timeout_seconds=N, retry_limit=1, tool_write_mode=..., template_path=...)`.
- **Gate definitions:** `gates.py` `X_GATE = GateCriteria(...)`; `gate_passed(report_path, GATE)` returns `(bool, reason)`.
- **Phantom-ID invariant:** `roadmap_ids ⊆ spec_ids ∪ accepted_deviations`; errors are raised/collected as `id_errors`, message form `f"roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations"`.
- **Error style:** functions return error-lists (not exceptions) for gate-style checks; raise for programmer errors.
- **Tests:** `tests/roadmap/` (pytest), `tests/integration/`, `tests/contracts/`. UV-only: `uv run pytest tests/roadmap/ -v`. Fixtures under `tests/roadmap/fixtures/`.
- **Dual-write doc anchors:** envelope.py module docstring documents the dual-write phase + cutover (R1.2 → R1.6). Comments cite "Vector A", "R1.4", "R1.6", "Contract #N".

---

## GAPS_AND_QUESTIONS (for researchers to resolve)

1. **Area A:** Confirm `test_wiring_pipeline.py` has NO unique coverage that must be re-homed before deletion (is `gate_passed(WIRING_GATE)` exercised by any OTHER live test, e.g. under `tests/` for `cli/audit/wiring_gate.py`?). Confirm nothing else imports the file.
2. **Area B:** Identify EXACTLY which generate/merge code paths can emit roadmap_ids WITHOUT passing through `validate_id_subset` at generation time. Is the gap (a) the `if spec_ids:` empty-skip short-circuit, (b) the non-tool-write markdown path having no id-check at all, or (c) some generate sub-path not wired to `render_step_tool_write_with_id_check`? Determine what "PREVENT at generation for all steps" concretely requires.
3. **Area B:** Does prevention belong in the prompt (instructing the agent), in the render/validate layer (reject at write), or both? What's testable deterministically?
4. **Area C:** What was the 1192s timeout's step (generate vs spec-fidelity)? Is the fix a timeout bump, a retry, prompt-template-adherence hardening, or model/persona change? Is any of this concretely actionable now, or is it investigation-only?
5. **Area D/E (CRITICAL):** Determine the cutover precondition state. Since no code counter exists, HOW does the task verify "3 consecutive parity-passing release cycles"? Where are parity results recorded (`.dev/releases/`, changelog, release docs)? **If the precondition is unmet, items D and E must HALT (write PENDING) rather than delete production code.** Researchers MUST establish current parity-cycle state with evidence.
6. **Area E:** Map ALL consumers of `spec_id_registry.json` (writers + readers) so dual-write removal doesn't strand a reader. Map `remediate_parser.py` consumers. Define exactly what "MD-family roadmap_ids reconciliation" residual work remains after commit `8fd0edc9`.
7. **Sprint-CLI compat:** Confirm the exact frontmatter + structure that makes the MDTM "Sprint-CLI-compatible" (`task_type`, phase IDs, `superclaude sprint run` expectations).

---

## RECOMMENDED_OUTPUTS (researcher → file)

- `research/01-file-inventory-area-a.md` — full inventory of 5 areas' files + Area A deletion specifics (orphan-import proof, no-other-consumer proof, WIRING_GATE preservation).
- `research/02-patterns-conventions.md` — roadmap pipeline code conventions, flag/Step/gate/error patterns, test conventions.
- `research/03-area-b-generation-phantom-id.md` — tool_writer id-check internals, executor generate/merge wiring, the precise prevention gap + recommended fix shape + testability.
- `research/04-area-c-opus-architect-fidelity-perf.md` — AgentSpec opus:architect, generate template-section adherence, spec-fidelity timeout/perf, the 1192s incident, what's actionable.
- `research/05-area-de-dualwrite-vectorA-registry.md` — dual-write architecture, 12 flags, Vector A parity-cycle state (EVIDENCE), markdown-path deletion preconditions, spec_id_registry.json consumers, remediate_parser.py consumers, MD-family residual reconciliation. **Must produce a precondition verdict.**
- `research/06-template-examples-sprintcli.md` — MDTM template 02 PART 1 rules (A3/A4/B2), prior TASK-RF examples, Sprint-CLI-compat requirements, phase-gate QA pattern.
- `research/07-test-verification.md` — `tests/roadmap/` suite inventory, test/fixture patterns, how to deterministically test generation-time phantom-ID prevention + the deletion + registry changes, UV pytest commands.

---

## SUGGESTED_PHASES (7 researchers, all parallel, Deep tier)

- **R1 — File Inventory + Area A** | scope: all 5 areas' file paths/exports + `tests/integration/test_wiring_pipeline.py`, `cli/audit/wiring_gate.py`, `cli/roadmap/gates.py` | output: `research/01-file-inventory-area-a.md` | others cover: B internals (R3), patterns (R2).
- **R2 — Patterns & Conventions** | scope: `models.py`, `executor.py` Step builders, `gates.py`, `tool_writer.py`, test layout | output: `research/02-patterns-conventions.md` | others cover: inventory (R1), B-deep (R3).
- **R3 — Integration/Data-flow: Area B** | scope: `tool_writer.py` (validate_id_subset, render_*), `executor.py` L1237-1320 + L2515-2620, `envelope.py` spec_ids, `id_registry.py` | output: `research/03-area-b-generation-phantom-id.md` | others cover: patterns (R2), tests (R7).
- **R4 — Integration/Data-flow: Area C** | scope: `models.py` AgentSpec, `commands.py` defaults, `prompts.py` generate/spec-fidelity prompts, `executor.py` timeouts, `fidelity_checker.py`/`convergence.py`/`semantic_layer.py` | output: `research/04-area-c-opus-architect-fidelity-perf.md` | others cover: B (R3), D/E (R5).
- **R5 — Integration/Data-flow + Doc-Cross-Validator: Areas D+E** | scope: dual-write (`envelope.py` docstring, `models.py` flags), `spec_id_registry.json`, `remediate_parser.py`/`remediate.py`, `id_registry.py` md_ids, `.dev/releases/`, changelog/release docs for parity-cycle state | output: `research/05-area-de-dualwrite-vectorA-registry.md` | others cover: B (R3), C (R4). **Must tag Vector-A parity-state claims [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED].**
- **R6 — Template & Examples** | scope: `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1, prior `TASK-RF-20260531-042405.md` structure, Sprint-CLI compat (`superclaude sprint` CLI + frontmatter), phase-gate QA | output: `research/06-template-examples-sprintcli.md` | others cover: tests (R7).
- **R7 — Test & Verification** | scope: `tests/roadmap/` + `tests/integration/` + `tests/contracts/` inventory, fixtures, how to test each of the 5 areas, UV pytest commands, CI gates | output: `research/07-test-verification.md` | others cover: patterns (R2), inventory (R1).

---

## TEMPLATE_NOTES

- **Template:** 02 (Complex Task). Justification: requires discovery (B prevention gap, D/E precondition state, C diagnosis), build, test, and phase-gate QA — multi-phase with conditional flows (D/E HALT-on-unmet-precondition).
- **Tier:** Deep — 5 areas, multiple subsystems, ~7800 LOC, destructive-precondition items.
- **MDTM features to use:** A3 (Complete Granular Breakdown — one item per file/change), A4 (iterative), B2 (self-contained items), phase-gate QA items (rf-qa / pytest), anti-orphaning (completion items in final phase).
- **QA_GATE_REQUIREMENTS:** PER_PHASE (user asked for phase-gate QA).
- **TESTING_REQUIREMENTS:** UNIT minimum + INTEGRATION (Area B prevention needs a deterministic regression test; deletion needs a collection-passes check; registry changes need parser-consistency tests).
- **VALIDATION_REQUIREMENTS:** `uv run pytest` (no collection errors), `make lint`, `make sync-dev` + `make verify-sync` if any `.claude/`-mirrored source changes (none expected — all edits are `src/superclaude/cli/roadmap` + `tests/`, not skills/agents, but verify), branch = `integration`.

---

## AMBIGUITIES_FOR_USER

1. **Items D & E are precondition-gated (Vector A: 3 consecutive parity-passing release cycles), and current evidence shows the cutover gate is NOT met** (all 12 `tool_write_*` flags default `False` = markdown path still production; no parity-cycle counter in code; prior follow-up notes mark D/E "DEFERRED until cutover"). **Resolution chosen (no blocking question needed):** the task encodes D and E as **precondition-check-then-HALT** items — an early item verifies the 3-parity-cycle cutover state from release records; if unmet, the dependent deletion/removal items write a PENDING marker to the Task Log and HALT rather than delete production code (honors the "human-decision items must HALT, not auto-default" rule). If parity IS met, the same gate passes and deletion proceeds. This design satisfies both possible intents without destroying production paths prematurely. The user can override at review time if they want unconditional deletion.
2. **Item C is partly diagnostic** — the 1192s timeout fix may be a timeout bump, retry, or template-adherence hardening; concrete change depends on R4's diagnosis. The task will include an investigation item that gates the concrete fix; if no safe deterministic fix is identifiable, C reduces to a tuning item (raise the relevant `timeout_seconds`) + a documented follow-up. This is "Low" priority per the source.
3. Otherwise intent is clear from the request and codebase context.
