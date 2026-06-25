# Research 07 — MDTM Template 02 Rules + Catch-Rate Report/Schema Model

**Status: Complete**

Scope: (a) MDTM Template 02 PART 1 builder rules the task-builder must obey; (b) the machine-readable catch-rate report MODEL (dataclass → `to_dict()` → `json.dumps` → JSON-Schema-validated) mirroring `run_report.py` + `summary.schema.json`, including a `backtest_status` field and per-escape MISS/CATCH verdicts; (c) suite-YAML vs parametrized-pytest recommendation for E1–E5.

Task goal under research: **a backtest harness emitting a machine-readable catch-rate report that drives `backtest_status` per NFR-1.**

All citations are `file:line` against the worktree root `/config/workspace/IronClaude/`. Template path abbreviated below as `TEMPLATE` = `.claude/templates/workflow/02_mdtm_template_complex_task.md`.

---

## PART A — MDTM Template 02 PART 1 rules the builder MUST follow

PART 1 (builder-only instructions) spans `TEMPLATE:62-1131`; PART 2 (the emitted task body) starts at `TEMPLATE:1155`. Rule IDs with one-line meanings, grouped as the prompt requested:

### Section A — Core principles (granularity / iteration)
- **A3 COMPLETE GRANULAR BREAKDOWN** (`TEMPLATE:108-112`): one atomic checklist item per file / component / iteration; NO bulk or high-level items; exact paths + measurable outcomes. → For this task: one item per ref/test/harness file, one item per E1–E5 scenario.
- **A4 ITERATIVE PROCESS STRUCTURE** (`TEMPLATE:114-133`): for any multi-item process, pre-enumerate ALL items in a Step X.1, create one item each in X.2, consolidate in X.3. The 5 backtest scenarios E1–E5 map directly onto this enumerate→process-each→consolidate skeleton.

### Section B — Self-contained checklist items (CRITICAL)
- **B1 session-rollover rationale** (`TEMPLATE:151-157`): context from batch 1 is gone by batch 3; standalone "read context" items are useless.
- **B2 SIX MANDATORY ELEMENTS per item** (`TEMPLATE:159-165`): every item is ONE full-paragraph prompt containing (1) Context Reference + WHY, (2) Action + WHY, (3) Output Specification (exact path + content + template), (4) Integrated Verification ("ensuring…" clause, no fabrication, 100% source-derived, document negative evidence), (5) Evidence-on-Failure-Only (log blockers to Task Log), (6) explicit Completion Gate sentence ("This item cannot be marked as done until… Once done, mark this item as complete.").
- **B3 single-paragraph pattern** (`TEMPLATE:167-170`): verbose, explanatory, executable standalone.
- **B5 FORBIDDEN patterns** (`TEMPLATE:181-200`): standalone reads, missing context ref, multi-line/bulleted items, separate verification items, over-granular ("create directory" alone), inter-item REMINDER blocks.
- **B7 key principles** (`TEMPLATE:206-213`): output file IS the success evidence; only log on FAIL/BLOCK; QA handles inter-batch verification.

### Section C — Embedding (NOT separate sections)
- **C1/C2/C3** (`TEMPLATE:223-240`): outputs, success criteria, and verification are EMBEDDED in the item that produces them — never as standalone "Outputs", "Success Criteria", or "Verification Checklist" sections.
- **C4 task completion** (`TEMPLATE:242-247`): handled only by Post-Completion Actions (frontmatter + Execution Log); no "Handoff Protocol" section.

### Section D — Mandatory sections + ordering rule
- **D3 CRITICAL RULE** (`TEMPLATE:286-289`): NO checklist items before Phase 1. Order is Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (first executable items). Context-loading + previous-stage-input reads live IN Phase 1 Steps 1.2–1.4.

### Section E — Checklist structure
- **E1 checkbox format** (`TEMPLATE:295-309`): every actionable item is `- [ ]`; FLAT only (no nested/parent checkboxes); `**Step X.Y:**` headers group, never checkboxes.
- **E2 components-first / summary-last** (`TEMPLATE:311-365`): summary/parent checkboxes come AFTER their components; parent-before-children and summary-in-middle are FORBIDDEN.
- **E3 sequential order** (`TEMPLATE:367-383`): top-to-bottom only; no "go back / see below / update section above".
- **E4 formatting** (`TEMPLATE:384-405`): no checkboxes on step-number headings; no REMINDER blocks between items (integrate into the item).

### Section F — Execution (for worker agents; shapes how items are written)
- **F1 five-step loop** (`TEMPLATE:411-420`): READ → IDENTIFY → EXECUTE → UPDATE → REPEAT.
- **F2 prohibited** (`TEMPLATE:422-429`): no multi-item execution, no cross-phase delegation, no skipping phase-gate QA (M3), no skipping post-completion validation (I17). A subagent gets work from a SINGLE checklist item only.
- **F2a item-execution discipline** (`TEMPLATE:431-447`): one item at a time within a session; **parallel-spawning exception** — consecutive same-phase items spawning INDEPENDENT subagents MAY be spawned in one message (relevant: the 5 backtest-scenario items, if independent, may run in parallel).

### Section H — Tool specification
- **H1–H3** (`TEMPLATE:491-497`): default to model tool choice; only name a tool when a specific tool is required (e.g. "use the Bash tool to run `uv run pytest …`"). The L3 test item (below) is where Bash is named.

### Section I — Additional guidelines (the QA-floor / intensity rules)
- **I1 directive language** (`TEMPLATE:516-520`): "YOU MUST" / "DO NOT".
- **I2 extreme granularity** (`TEMPLATE:522-526`).
- **I3 incremental file modification** (`TEMPLATE:528-532`): "DO NOT complete entire files at once."
- **I8 mandatory template usage** (`TEMPLATE:582-591`).
- **I9 / I14 anti-hallucination** (`TEMPLATE:593-597`, `623-633`): 100% source accuracy, document negative evidence, evidence tables for technical claims.
- **I15 PHASE-GATE QA ENFORCEMENT** (`TEMPLATE:635-651`): every task with 2+ phases needs ≥1 phase-gate QA between the primary execution phase and any dependent phase. **PROHIBITION:** 1–2-agent gates rejected. FLOORS — **final/assembled-output gate ≥6 agents (3 rf-qa structural + 3 rf-qa-qualitative content); intermediate gate ≥5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative)**. Gate follows M3, plus M4 if source documents were consumed. Every gate step is an explicit `- [ ]` item; "No QA lives only in prose."
- **I16 verdict + fix cycles** (`TEMPLATE:653-673`): binary PASS/FAIL — ANY issue of ANY severity ⇒ FAIL. Consolidated verdict FAILs if any single agent reports any issue. Max-fix-cycle table (report-validation 3, task-integrity 2, etc.). Serialized fix (I20) mandatory; parallel fix authorization PROHIBITED.
- **I17 POST-COMPLETION VALIDATION** (`TEMPLATE:675-686`): before status→Done: all items `[x]`, all output files exist (Glob), blockers resolved, **tests pass if code modified**, MANDATORY lens-based QA (M3) on final outputs, source-fidelity (M4) when applicable. These items go in `## Post-Completion Actions` BEFORE the frontmatter-update item.
- **I18 TESTING REQUIREMENTS for code-modifying tasks** (`TEMPLATE:688-697`): if the task creates/modifies source code, MUST include ≥1 testing item that (1) names the test command, (2) defines pass criteria, (3) names where results are captured, (4) follows B2; use the **L3 (Test/Execute)** pattern. **Directly governs the backtest-harness task: the harness is Python source, so an `uv run pytest …` L3 item is mandatory.**
- **I19 LENS-BASED QA MINIMUM AGENTS** (`TEMPLATE:699-743`): FULL-intensity floors. Final/assembled-output table by size: `<500 lines → 3+3=6`; `500-1500 → 4+4=8`; `1500-3000 → 5+5=10`; `>3000 → 6+6=12` (`TEMPLATE:706-711`). Standard structural lenses = template-conformance, internal-consistency, evidence-quality, completeness (`TEMPLATE:715-719`). Standard content lenses = actionability, numbers-metrics, crossref-chain, domain-accuracy (`TEMPLATE:721-725`). Adversarial framing required ("Assume ≥N errors…"). Intermediate-gate table (research/synthesis/task-integrity) at `TEMPLATE:731-737`.
- **I20 SERIALIZED FIX AUTHORIZATION** (`TEMPLATE:745-757`): report (all `fix_authorization:false`) → consolidate (`${TASK_DIR}qa/qa-consolidated-findings.md`) → ONE fix agent (`fix_authorization:true`) → verify (≥2 agents). Parallel fix PROHIBITED.
- **I21 SOURCE-DOCUMENT FIDELITY GATE** (`TEMPLATE:759-789`): mandatory when output is derived from source docs (PRD/TDD/roadmap/tech-ref/research/cleanup/etc.); NOT required for pure mechanical transforms or config-only. Checks: semantic coverage, detail preservation, cross-source contradiction, phantom-coverage, operational/compliance completeness. ≥2 agents (3–4 if sources >1000 lines). Runs AFTER M3.
- **I22 QA INTENSITY LEVELS** (`TEMPLATE:793-840`): scales gate counts. **lite** (small <300-line outputs): intermediate 2, final 3 (1 structural+1 content+1 domain), fidelity 1, 1 fix cycle, 1 verifier, no partitioning, double-QA disabled. **standard** (300-1500): intermediate 3, final 7 (3+3+1 domain), fidelity 2, 2 cycles, 2 verifiers. **full** (>1500 / critical): I19/I20/I21 unmodified. Default mapping Quick→lite / Standard→standard / Deep→full; user may override. **Serialized fix (I20) applies at ALL levels.**

### Section L — Intra-task handoff patterns (the item "verbs")
Handoff-file convention (`TEMPLATE:909-921`): items write to `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`, persisted across batches.
- **L1 DISCOVERY** (`TEMPLATE:928-938`): explore + write a machine-readable findings file that IS the deliverable for later items.
- **L2 BUILD-FROM-DISCOVERY** (`TEMPLATE:940-950`): read discovery file + source file, then build output.
- **L3 TEST/EXECUTE** (`TEMPLATE:952-962`): run a command, capture BOTH raw output AND a structured summary. **This is the pattern for the pytest/backtest run item (I18).**
- **L4 REVIEW/QA** (`TEMPLATE:964-974`): produce a structured PASS/FAIL verdict with specific findings (never "looks good").
- **L5 CONDITIONAL-ACTION** (`TEMPLATE:976-988`): branch on a prior result file; MUST handle BOTH branches; output file always created. **This is the pattern that sets `backtest_status` (complete vs partial) from the catch-rate report.**
- **L6 AGGREGATION** (`TEMPLATE:990-1000`): Glob-discover prior outputs, consolidate into one report. **This is the pattern that builds the consolidated catch-rate report from the 5 per-escape results.**
- **L7 selection guide + phase structures** (`TEMPLATE:1002-1027`): e.g. "Build → Test → Fix: K1/K2 → L3 → L5"; "Full Lifecycle with QA Gates: L1→L2→**M3**→L3→L5→L4→L6→**M3**".

### Section M — Phase-gate composite patterns
- **M1 LEGACY single-agent** (`TEMPLATE:1034-1045`): DEPRECATED; new task files MUST NOT use it.
- **M3 LENS-BASED QA SEQUENCE** (`TEMPLATE:1059-1096`): mandatory 8-step gate — Step1 aggregate (L6); Step2 structural-lens agents PARALLEL `fix_authorization:false` → `${TASK_DIR}qa/qa-structural-[lens]-report.md`; Step3 content-lens agents PARALLEL → `qa-content-[lens]-report.md`; Step4 domain lenses (if any); Step5 consolidate → `qa-consolidated-findings.md`; Step6 ONE fix agent `fix_authorization:true`; Step7 verification ≥2; Step8 conditional proceed / repeat (max cycles per I16). EVERY step is an explicit `- [ ]` item; do NOT collapse.
- **M4 SOURCE-DOCUMENT FIDELITY GATE** (`TEMPLATE:1098-1121`): runs AFTER M3 when I21 applies; Step1 identify sources (explicit, not discovered); Step2 fidelity agents PARALLEL (each reads assigned source range + FULL output); Step3 cross-source contradiction agent (multi-source only); Step4 consolidate; Step5 fix agent; Step6 verify. Reports `qa-source-fidelity-report-[N].md`.

### PART 2 structural anchors the builder emits
- **`## Execution Context` section requirement** (`TEMPLATE:1193-1221`): the builder MUST populate this in every generated task file before marking it ready. Sub-sections (each currently a `[placeholder: builder populates]`): **References** (`:1197-1199`), **Source Areas** (`:1201-1203`), **Key Constraints** (`:1205-1207` — QA intensity, scope limits, blockers, prohibitions), **Handoff File Convention** (`:1209-1221`), **Frontmatter Update Protocol** (`:1223-1231`). The sibling task carries this populated.
- **Anti-orphaning**: enforced by the combination of D3 (no items before Phase 1), E1/E2/E3 (flat, forward-only, summary-last — no item references a checkbox that doesn't exist before it), and I15/M3 "no QA in prose" (every gate agent is a real `- [ ]` item, never an orphan reference). Every output a B2 item declares must be created by that same item — no dangling "to be produced later" references.

### Frontmatter (PART 1 top, `TEMPLATE:1-61`) the builder fills
`id`, `title`, `description`, `version`, `status` ("🟡 To Do"), `type`, `priority`, dates, `spec_path` (driving spec; A.2), `reflect_pre` block (`verdict/coverage_pct/depth/tcs/run_id/report/reviewed_at`; populated at A.10.7), `reflect_post` (executor-set), `related_docs`, `template_schema_doc`, `task_type: static`. The sibling `TASK-RF-troubleshoot-hardening-20260611-023739.md:1-62` is a fully-populated real example (note `reflect_pre.verdict: pass`, `template_schema_doc: .claude/templates/workflow/02_mdtm_template_complex_task.md`).

---

## PART B — The catch-rate-report MODEL (dataclass → to_dict → json → JSON-Schema)

### The reference pattern (run_report.py + summary.schema.json + models.py)
The cliEval reporter is the canonical "machine-readable report" pattern in this repo. The full chain:

1. **Frozen dataclasses with explicit field-order tuples.** `RunSummary` (`src/superclaude/cli/eval/models.py:835-903`) is `@dataclass(frozen=True)`; its field order is duplicated in a module-level tuple `_RUN_SUMMARY_FIELDS` (`models.py:820-832`). Same idiom for `RunCounts` (`models.py:742-770` + `_RUN_COUNTS_FIELDS`) and `RunTotals` (`models.py:794-810` + `_RUN_TOTALS_FIELDS` at `:784-791`).
2. **`__post_init__` enforces internal invariants at construction.** `RunSummary.__post_init__` (`models.py:905-921`) raises `ValueError` if `kept_plus_skipped_equals_n_prime` disagrees with the actual arithmetic `kept_k + skipped_s == expanded_n_prime` — a misreporting producer fails loudly.
3. **`to_dict()` builds an explicit ordered dict from the field tuple, recursing via nested `to_dict()`.** `RunSummary.to_dict` (`models.py:923-946`) iterates `_RUN_SUMMARY_FIELDS`, unwraps `counts`/`totals` via their `.to_dict()`, maps `evals` to `[item.to_dict() for item in value]`, shallow-copies `artifacts`. Ordering is stable regardless of Python version.
4. **A renderer wraps `to_dict()` and serializes once.** `render_summary_json` (`run_report.py:233-246`): calls `_check_invariant(summary)` first, then `json.dumps(summary.to_dict(), indent=2, ensure_ascii=False) + "\n"` with `sort_keys=False` (preserves declaration order; trailing newline = POSIX text convention). YAML sibling `render_summary_yaml` (`run_report.py:339-363`) reuses the same `to_dict()`.
5. **A cross-model invariant guard fires BEFORE any write.** `ReporterContractViolation` (`run_report.py:67-93`) + `_check_invariant` (`run_report.py:96-108`) enforce `len(evals) == counts.expanded_n_prime` (FR-RPT1); the violation maps to exit code 2 (`REPORTER_CONTRACT_VIOLATION_EXIT_CODE = _exit_codes.USAGE_ERROR`, `run_report.py:56`). Called at the top of every renderer (`run_report.py:161,244,276,356`) and the writer (`run_report.py:438`) so a partial/contradictory artifact is never left on disk.
6. **The writer emits the artifact set.** `write_aggregated_report` (`run_report.py:413-439`) → `_write_artifact_set` (`run_report.py:366-410`) writes `summary.md`, `summary.json`, `summary.yaml` (+ optional `junit.xml`), returns an artifact-name→Path mapping.
7. **The JSON-Schema lives next to the writer and is loaded via `importlib.resources`.** `summary.schema.json` (`src/superclaude/cli/eval/schemas/summary.schema.json`) declares `$schema: draft/2020-12`, `$id`, `required`, `additionalProperties`, and a `$defs` block of reusable sub-objects (`runCounts`, `runTotals`, `evalOutcome`, `evalStatus` enum, `expectResult`, `expectFailure`). `load_summary_schema()` (`schemas/__init__.py:30-44`) returns the parsed mapping from the package (wheel-safe).
8. **A fidelity test validates real producer output against the schema.** `tests/cli/eval/test_reporter_contract.py:360-394` (`test_reporter_json_validates_against_summary_schema`) builds a `RunSummary` covering PASS/SKIPPED/FAIL/ERRORED rows, validates BOTH the in-memory `reporter.to_json()` payload AND the on-disk file via `Draft202012Validator` (imported `:48`), and asserts they are byte-identical. `tests/cli/eval/test_summary_schema.py` validates the schema document itself.

### How to model the catch-rate report (recommended shape)
Mirror the above one-to-one. NFR-1 (per sibling `research/07-release-spec-structure.md:372` and `:162`) demands: replay each E1–E5 escape against the built gates; production-facing signoff stays **advisory** until `backtest_status == complete`; the report must separate the run-level H0-H5 verdict from the E1-E5 catch-rate coverage (`research/07:230,238`).

Proposed dataclass tree (one new module, e.g. `src/superclaude/cli/eval/backtest_report.py` or a `catch_rate.py` model + writer pair, following the models.py/run_report.py split):

```
@dataclass(frozen=True)
class EscapeResult:                # one per E1..E5
    escape_id: str                 # "E1".."E5" — regex-guarded like evalIdString
    wave: str                      # H1..H5 mapping (research/07:411-415)
    verdict: str                   # "CATCH" | "MISS"  (binary, per-escape)
    negative_witness: bool         # pre-fix FAIL observed (anti-vacuous)
    card_path: str | None          # cited passing wave/card (anti-inflation; research/07:160)
    detail: str                    # one-line evidence
    # -> EscapeResult.to_dict() via _ESCAPE_RESULT_FIELDS tuple

@dataclass(frozen=True)
class CatchRateReport:
    run_id: str
    generated_at: str              # ISO-8601 str (round-trips through JSON)
    contract_version: str          # additive-evolution tag (mirrors manifest_version)
    backtest_status: str           # "not_run" | "partial" | "complete"  (NFR-1 driver)
    total_escapes: int             # 5
    caught: int
    missed: int
    catch_rate: float              # caught / total_escapes
    escapes: tuple[EscapeResult, ...] = ()
    # __post_init__: assert caught + missed == total_escapes == len(escapes);
    #   assert backtest_status == _derive_status(escapes)  (loud ValueError on mismatch)
    # to_dict(): explicit ordered dict from _CATCH_RATE_FIELDS, escapes -> [e.to_dict()]
```

`backtest_status` derivation rule (encode in `__post_init__` + a `_derive_status` helper, mirroring `kept_plus_skipped_equals_n_prime`):
- `not_run` — `len(escapes) == 0` (no replay attempted).
- `partial` — some but not all E1–E5 replayed, OR any `MISS`, OR any missing negative witness.
- `complete` — all 5 replayed AND all `verdict == CATCH` AND all have a `negative_witness` AND a cited `card_path` (the 100%-would-have-caught bar, `research/07:372`).

Writer + invariant guard (mirror `run_report.py`):
- `class CatchRateContractViolation(RuntimeError)` analogous to `ReporterContractViolation`, raised when `caught + missed != total_escapes` or `len(escapes) != total_escapes`, mapping to the same `exit_codes.USAGE_ERROR` (exit 2).
- `render_catch_rate_json(report) -> str`: `_check(report)`, then `json.dumps(report.to_dict(), indent=2, ensure_ascii=False, sort_keys=False) + "\n"`.
- `write_catch_rate_report(report, output_dir, *, emit_md=True)`: writes `catch-rate.json` (+ optional human `catch-rate.md` mirroring `render_summary_markdown` with a per-escape `| Escape | Wave | Verdict | Witness | Card |` table and a headline `## Catch rate: X/5 (status)`).

JSON-Schema (`src/superclaude/cli/eval/schemas/catch_rate.schema.json`, loaded by a `load_catch_rate_schema()` added to `schemas/__init__.py:24` `__all__`), mirroring `summary.schema.json`:
- top-level `required`: `["run_id","generated_at","contract_version","backtest_status","total_escapes","caught","missed","catch_rate","escapes"]`, `additionalProperties: true` (matches summary's forward-compat choice at `summary.schema.json:18`).
- `backtest_status`: a `$defs` enum `{"enum": ["not_run","partial","complete"]}` — exactly the pattern of `evalStatus` (`summary.schema.json:73-86`). This is how the enum is encoded + schema-validated.
- per-escape `verdict`: a `$defs` enum `{"enum": ["CATCH","MISS"]}` (the MISS/CATCH encoding). `escape_id`: reuse the `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` from `suite.schema.json:65-68` for path-traversal safety.
- `escapes`: `{"type":"array","items":{"$ref":"#/$defs/escapeResult"}}`; `escapeResult` `$def` with `required` = the EscapeResult fields, `additionalProperties: false` (matches `evalOutcome` at `summary.schema.json:160`).
- `catch_rate`: `{"type":"number","minimum":0,"maximum":1}`; the integer counts `{"type":"integer","minimum":0}`.

Fidelity test (mirror `test_reporter_contract.py:360-394`): build a `CatchRateReport` with a mix of CATCH/MISS rows, validate both the in-memory `render_catch_rate_json` payload and the on-disk file against `load_catch_rate_schema()` via `Draft202012Validator`, assert they match, and assert each `backtest_status` value drives the documented advisory/complete behavior.

**Why this shape:** it is the repo's already-blessed, already-tested contract idiom (frozen dataclass + field-order tuple + `__post_init__` invariant + `to_dict()` + single `json.dumps` + sibling JSON-Schema + `importlib.resources` loader + `Draft202012Validator` fidelity test). Reusing it gives the catch-rate report the same loud-fail, byte-stable, schema-validated guarantees the summary report has, and lets the harness's L3/L5 task items assert against a real schema rather than ad-hoc string checks.

---

## PART C — E1–E5: suite YAML vs parametrized pytest? → RECOMMENDATION: parametrized pytest (E2E backtest), NOT a suite YAML

**Recommendation: declare E1–E5 as parametrized pytest E2E backtest cases that exercise the built H1–H5 gates, NOT as a cliEval `suites/*.yaml` manifest.** Rationale, evidence-based:

1. **The sibling task already does exactly this and it passed its PRE reflect gate.** The companion `TASK-RF-troubleshoot-hardening-20260611-023739` describes its test scope as "13 unit + 5 integration + **6 E2E backtest scenarios**" (`…023739.md:4`) and its research enumerates the 5 escapes E1–E5 as `§8.3 Manual / E2E Backtest Scenarios` to be "encoded as documented scenarios/fixtures" (`research/08-v1.1.0-deliverable-reconciliation.md:83`), with the verbatim scenario table at `research/07-release-spec-structure.md:408-415` (E1→H1, E2→H3, E3→H3, E4→H2, E5→H4) and NFR-1 mapped to integration test `test_backtest_status_keeps_pipeline_health_advisory_until_complete` + the §8.3 E1–E5 set (`research/07:445`). That precedent is the strongest signal: this evals-160018 task is the harness that PRODUCES the machine-readable catch-rate report those scenarios feed.

2. **cliEval suite YAML is the wrong contract surface for in-process gate replay.** `suite.schema.json` (`suite.schema.json:1-161`) models *subprocess/CLI* evals: each `evalEntry` runs an external command (`inputs[].prompt`), captures PTY stdout, and asserts via `expects[].stdout/exit_code` (see the worked example `suites/task_classification_contract.yaml:47-97`, which spawns `/sc:task "…"` in an ephemeral HOME). E1–E5 backtests instead need to **import the built H-gate functions and assert their PASS/FAIL behavior pre- and post-fix** (negative witness then positive) — e.g. `research/07:411` "Replay headless PRD `--spec` with local-path `--file` against H1 → H1 FAIL pre-fix, PASS post-fix". That is in-process Python assertion logic, not a stdout-contains check on a subprocess. A suite YAML can't express "FAIL until `K_swept == K_true`" (E3, `research/07:413`) or "H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers classified" (E4, `research/07:414`).

3. **`pytest.mark.parametrize` over a tuple of escape specs is the idiomatic match** for "run the same replay-and-assert procedure across 5 scenarios" and lets each case both (a) assert the gate verdict and (b) emit one `EscapeResult` into the `CatchRateReport`. A session-scoped fixture (or a final aggregation test) collects the 5 `EscapeResult`s, builds the `CatchRateReport`, writes `catch-rate.json` via the writer, and asserts `backtest_status`. This satisfies I18 (`TEMPLATE:688-697`) — the L3 test item runs `uv run pytest tests/…/test_backtest_catch_rate.py -v` — and L5/L6 (`TEMPLATE:976-1000`) — aggregate the 5 results, branch `backtest_status` to `complete`/`partial`.

4. **The catch-rate report is the machine-readable artifact, replacing what a suite `summary.json` would give you.** Because the harness emits its OWN schema-validated `catch-rate.json` (PART B), there is no need to borrow cliEval's `summary.json`. The two are complementary: cliEval validates *command contracts* via subprocess; the backtest harness validates *gate-mechanism catch rate* via in-process replay and emits a parallel-but-distinct contract.

**Caveat / when a suite YAML WOULD be right:** if any of E1–E5 is genuinely a black-box CLI invocation whose only observable is stdout/exit-code (e.g. an E1 that literally shells out to `superclaude roadmap run --spec … --file …` and asserts the headless exit behavior), THAT single scenario could legitimately be a 1-eval suite YAML reusing the cliEval runner. But the catch-rate roll-up (`caught/missed/backtest_status`) still belongs in the pytest aggregation + `CatchRateReport`, because cliEval's `RunTotals` has no MISS/CATCH or `backtest_status` notion. Net: parametrized pytest for the harness + report; reserve suite YAML only for any pure-subprocess escape, never for the catch-rate aggregation.

---

## Summary for the builder
- **Template rules to honor:** A3/A4 (one item per file/scenario, enumerate→process→consolidate), B2 6-element self-contained paragraphs + Completion Gate, C1–C4 (embed outputs/criteria/verification), D3 (no items before Phase 1), E1–E4 (flat, forward-only, summary-last, no orphan refs), F2a parallel-spawn exception (independent E1–E5 items), H3 (name Bash only for the pytest item), I3 incremental writes, I8/I9/I14 anti-hallucination, **I18 mandatory L3 testing item (harness is code)**, I15/I16/I19/I20/M3 phase-gate QA floors (final ≥6, intermediate ≥5; serialized fix), I21/M4 fidelity gate (applies — outputs derive from the RELEASE-SPEC), I22 intensity scaling, and a fully-populated `## Execution Context` (`TEMPLATE:1193-1221`).
- **Report model:** new frozen dataclasses `CatchRateReport` + `EscapeResult` with field-order tuples, `__post_init__` invariant (counts + `backtest_status` derivation), `to_dict()`, a `render_catch_rate_json` doing one `json.dumps(..., sort_keys=False) + "\n"`, a `CatchRateContractViolation` guard mapped to exit 2, a sibling `catch_rate.schema.json` (draft 2020-12) with `backtest_status` enum `not_run|partial|complete` + per-escape `verdict` enum `CATCH|MISS`, loaded via a `load_catch_rate_schema()` in `schemas/__init__.py`, and a `Draft202012Validator` fidelity test on both in-memory + on-disk payloads. This is a 1:1 mirror of `models.py` + `run_report.py` + `summary.schema.json` + `test_reporter_contract.py`.
- **E1–E5 encoding:** parametrized pytest E2E backtest (matches sibling precedent + in-process gate-replay semantics), aggregated into the `CatchRateReport`; suite YAML only if a specific escape is a pure subprocess/stdout contract.

### Key citations
- `TEMPLATE` = `.claude/templates/workflow/02_mdtm_template_complex_task.md`: PART 1 `:62-1131`; A3 `:108`, A4 `:114`, B2 `:159`, B5 `:181`, C1–C4 `:223-247`, D3 `:286`, E1 `:295`, E2 `:311`, F2 `:422`, F2a `:431-447`, I15 `:635`, I16 `:653`, I17 `:675`, I18 `:688`, I19 `:699-743`, I20 `:745`, I21 `:759`, I22 `:793-840`, L1–L6 `:928-1000`, M3 `:1059-1096`, M4 `:1098-1121`; Execution Context `:1193-1221`.
- `src/superclaude/cli/eval/models.py`: `RunSummary` `:835-946`, `_RUN_SUMMARY_FIELDS` `:820-832`, `RunCounts` `:742-780`, `RunTotals` `:794-815`, `__post_init__` invariant `:905-921`, `to_dict` `:923-946`.
- `src/superclaude/cli/eval/run_report.py`: `ReporterContractViolation` `:67-93`, `_check_invariant` `:96-108`, exit-code const `:56`, `render_summary_json` `:233-246`, `_write_artifact_set` `:366-410`, `write_aggregated_report` `:413-439`.
- `src/superclaude/cli/eval/schemas/summary.schema.json`: top-level `:1-71`, `evalStatus` enum `:73-86`, `runCounts` `:87-124`, `evalOutcome` `:146-200`.
- `src/superclaude/cli/eval/schemas/__init__.py`: `load_summary_schema` `:30-44`.
- `src/superclaude/cli/eval/suites/suite.schema.json`: `evalEntry` `:124-159`, `evalIdString` regex `:65-68`, `parameterize` `:147-152`.
- `src/superclaude/cli/eval/suites/task_classification_contract.yaml`: subprocess-eval example `:47-97`.
- `tests/cli/eval/test_reporter_contract.py`: schema-fidelity test `:360-394`, `Draft202012Validator` import `:48`.
- Sibling task: `…20260611-023739.md:4` (test-scope line), `:1-62` (populated frontmatter); research `07-release-spec-structure.md:160,162,230,238,372,408-415,445`; `08-v1.1.0-deliverable-reconciliation.md:39,80,83`.
