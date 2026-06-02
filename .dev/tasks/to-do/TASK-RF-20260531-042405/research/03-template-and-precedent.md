# R3 — MDTM Template Rules + Precedent Phase Shapes + Recurrence Fixture Layout

**Date:** 2026-05-31
**Scope:** Template 02 PART 1 rules that apply to the roadmap-pipeline rewrite task; phase shapes used by similar prior tasks; where the recurrence corpus fixture tree should live.
**Source files cited:**
- `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205L)
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260527-043715-sc-reflect-rebuild/TASK-RF-20260527-043715-sc-reflect-rebuild.md` (657L)
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260527055700-spec-fidelity-canonicalizer/TASK-RF-20260527055700-spec-fidelity-canonicalizer.md` (411L)
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260525-150000/TASK-RF-20260525-150000.md` (556L)
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260526-102600/TASK-RF-20260526-102600.md` (373L)
- `/config/workspace/IronClaude/tests/roadmap/` (64 test files; no `fixtures/` subdir exists today)
- `/config/workspace/IronClaude/tests/roadmap/conftest.py:1-39` (only audit_trail fixture exists)

---

## SECTION 1 — TEMPLATE 02 PART 1 RULES THAT APPLY TO THIS TASK

The roadmap-pipeline rewrite is a multi-phase code-modifying task with discovery, build, test, side-by-side migration, QA gates, and cleanup. Below: every PART 1 rule that materially constrains the task-builder, cited by template section.

### 1.1 Mandatory rule-sections (template:69-650)

| Rule | Where | Application to roadmap rewrite |
|---|---|---|
| **A3 — Granular breakdown** | template:91-96 | One checklist item per file/component/test/contract item. NO bulk "implement R0.1" items. ≈14 phases × multiple per-file items per phase ⇒ ~80-120 checklist items expected. |
| **A4 — Iterative process structure** | template:97-116 | For 9-step tool-write rewrite (R1.4) and per-contract-item CI wiring: pre-enumerate ALL items in initial step, one checklist item each, consolidation step at end. The 14 R1.4 sub-phases (one per LLM step migrated) and 10 Contract items (Contract #1 through #10) MUST be enumerated upfront. |
| **B2 — Six-element self-contained items** | template:142-149 | EVERY item embeds: Context+WHY, Action+WHY, Output spec, "ensuring..." clause, Evidence-on-Failure-Only, explicit completion gate. Forbidden: standalone "read context" items (B5, template:164-184). |
| **B3 — Single paragraph form** | template:150-153 | Each item is ONE paragraph, verbose and explanatory — not bullets/lines. |
| **E1/E2 — Flat checkbox structure, summary LAST** | template:278-348 | NO nested checkboxes. Parent/summary checkboxes ONLY at end of sequence. Use bold `**Step X.Y:**` headers (not checkboxes) for grouping. |
| **E3 — Sequential top-to-bottom only** | template:350-365 | No "go back and update", no forward references. Each phase fully completes before next. |
| **F1 — READ→IDENTIFY→EXECUTE→UPDATE→REPEAT** | template:394-403 | Constrains worker-agent behavior — task-builder doesn't author this loop but each item must be standalone enough for it. |
| **F2a — Item execution discipline** | template:414-430 | Multi-item batches across sessions OK; multi-item execution WITHIN a session is forbidden. Parallel-spawning exception (template:430): consecutive items with independent subagents may be spawned in parallel via multiple Agent calls in one message. |
| **G1-G4 — Headless agent context** | template:457-469 | Worker agents do NOT auto-load CLAUDE.md / RULES.md / file_conventions.md. Embed needed rules directly in items (e.g., "remember: UV-only, no `pip install`"). |
| **I3 — Incremental file modification** | template:511-515 | Explicit "DO NOT attempt entire files at once" required for the 2,800 LOC delta. Save points after major sections (matches sc-reflect-rebuild's Phase 2 "4 sequential Edit passes" pattern at TASK-RF-20260527-043715-sc-reflect-rebuild.md). |
| **I11 — Early status update** | template:569-571 | First checklist item of Phase 1 MUST update frontmatter to "🟠 Doing". |
| **I12 — Verification integrated, NEVER separate** | template:573-578 | NO separate "verify the file" items. Verification goes in "ensuring..." clause of the action item. |
| **I15 — Phase-gate QA enforcement (MANDATORY)** | template:599-607 | Every task with 2+ phases MUST include phase-gate QA. Composition: (1) L6 aggregation item collecting Phase N outputs, (2) rf-qa spawn item, (3) L5 conditional-action for PASS/FAIL. For roadmap rewrite: gates required after R0 acceptance, R1.1, R1.2, R1.3, EACH R1.4 sub-phase (9 step migrations), R1.5, R1.6 — anticipated 14+ QA gates. |
| **I16 — QA fix-cycle ceilings** | template:609-624 | task-integrity gate: max 2 cycles → unresolved → Open Questions. report-validation / research-gate / qualitative gate: max 3 → HALT and escalate. Each fix cycle MUST re-verify all previously-failed items PLUS check for new issues. If issue count rises across cycles, flag as systemic. |
| **I17 — Post-completion validation** | template:626-635 | Before status→Done, run: (a) all `[ ]`→`[x]` check, (b) all output files exist via Glob, (c) blockers have resolution notes, (d) tests pass (code-modifying task). Goes in `## Post-Completion Actions` section. |
| **I18 — Testing requirements for code tasks** | template:637-647 | Task creating/modifying source code MUST include explicit test item: command + pass criteria + results-capture path + B2 self-contained pattern. Use L3 (Test/Execute) pattern. |

### 1.2 L1-L6 + M1 handoff patterns that apply (template:711-861)

| Pattern | Where to use in roadmap rewrite |
|---|---|
| **L1 Discovery** (template:737-747) | Phase 1: enumerate all 24 `src/superclaude/cli/roadmap/*.py` files into `phase-outputs/discovery/file-inventory.md`. Phase 6 (R1.1): enumerate all duplicate parsers / fail-open defaults / `return True` stubs into `phase-outputs/discovery/cleanup-targets.md`. |
| **L2 Build-from-Discovery** (template:749-759) | Per-file modification items reference the discovery inventory by path. Example: "Read `phase-outputs/discovery/file-inventory.md` to identify `gates.py:317-383`, then read `gates.py`, then add `GateCriteria.code_assertions` slot at line 317…" |
| **L3 Test/Execute** (template:761-771) | After each R1.4 sub-phase: run side-by-side validation `uv run pytest tests/roadmap/test_tool_write_step_<N>.py -v`. Capture raw output to `phase-outputs/test-results/step-<N>-output.txt` + summary to `phase-outputs/test-results/step-<N>-summary.md`. |
| **L4 Review/QA** (template:773-783) | The rf-qa spawn items in phase gates ARE L4 reviews. Verdict file goes to `phase-outputs/reviews/phase-<N>-rf-qa.md`. |
| **L5 Conditional-Action** (template:785-797) | Per gate: IF verdict=PASS proceed; IF FAIL execute fix cycle (I16 limits). Also for R1.4 cutover criteria — IF 3 consecutive releases match between old/new ⇒ delete old code path; ELSE another release cycle. |
| **L6 Aggregation** (template:799-808) | Final phase: Glob all `phase-outputs/reviews/*.md`, consolidate into `phase-outputs/reports/final-quality-report.md`. Contract items 1-10 acceptance summary. |
| **M1 Phase-gate composite** (template:843-851) | The 3-item sequence (Aggregation + rf-qa spawn + Conditional) inserted between phases. Roadmap rewrite needs 14+ instances. |

### 1.3 Template 02 PART 2 (output file structure) — template:872-1205

Required top-level sections in the generated task file (in order):
- Frontmatter (template:1-44)
- `# [Task Title]` (template:890)
- `## Task Overview` (template:892)
- `## Key Objectives` (template:896)
- `## Prerequisites & Dependencies` (template:904) — Parent task, blocking deps, previous stage outputs, handoff convention, frontmatter protocol
- `## Detailed Task Instructions` (template:954)
- `### Phase 1: Preparation and Setup` (template:1012) — status update + create `phase-outputs/{discovery,test-results,reviews,plans,reports}/` dirs
- `### Phase 2..N` (per-task)
- `### Phase Gate: Quality Verification` (template:1090) — M1 sequences
- `## Post-Completion Actions` (template:1118) — Glob output verification + test re-run + Task Summary + frontmatter→Done
- `## Task Log / Notes 📋` (template:1128) — Task Summary stub, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up Items, Deviations

---

## SECTION 2 — PRECEDENT PHASE SHAPES (what worked for similar large refactors)

### 2.1 TASK-RF-20260527-043715-sc-reflect-rebuild (657L, 25 CREATE + 2 MODIFY files, 7 phases)

**Phase shape (precedent A — closest match to roadmap rewrite scale):**
1. Phase 1: Preparation, Frozen Baseline, Skill Package Scaffolding
2. Phase 2: SKILL.md Body Authoring (Incremental — **4 Edit Passes**) + Phase 2 QA Gate (rf-qa task-integrity)
3. Phase 3: Refs Authoring (**11 Refs — One Item per Ref**) + Phase 3 QA Gate (rf-qa task-integrity)
4. Phase 4: Command Rewrite + Bidirectional Skill Link + Phase 4 QA Gate (rf-qa)
5. Phase 5: Eval Workspace Setup + Phase 5 QA Gate (rf-qa-qualitative)
6. Phase 6: Sync & Makefile Targets
7. Phase 7: Final QA, Eval-Quick Smoke, Task Completion + Phase 7 QA Gate (rf-qa-qualitative)

**Effective patterns extracted:**
- **Per-phase QA gate after Phases 2/3/4/5/7** — rf-qa for task-integrity, rf-qa-qualitative for operational/UX-shape validation. Roadmap rewrite should mirror this: rf-qa after every R0/R1 phase that produces verifiable artifacts; rf-qa-qualitative after R1.4 (tool-write rewrite — operational behavior must match).
- **Spawn-prompt pattern with ADVERSARIAL STANCE + fix_authorization: true** — the literal spawn-prompt string is embedded in the QA item. Roadmap rewrite items should reuse this pattern verbatim (matches user memory `feedback_rfqa_adversarial_pattern.md`).
- **Halt-precedence guards in EVERY gate** — byte-exact halt messages `[HALT-MONOTONICITY] |F|=<n>` and `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` Roadmap rewrite gates should include these guards because the rewrite is exactly the kind of multi-cycle refactor where FP count can climb during fix cycles.
- **Splitting large file authoring across 4 sequential Edit-pass items** to stay under tool token limits — directly applicable to `executor.py` (3,701L) modifications in R1.2/R1.6 and to `prompts.py` (1,367L) rewrites in R1.4.
- **One ref = one checklist item** — directly maps to "one tool-write step migration = one checklist item" in R1.4.

### 2.2 TASK-RF-20260527055700-spec-fidelity-canonicalizer (411L, 7 phases, single-module refactor)

**Phase shape (precedent B — smaller but disciplined):**
1. Phase 1: Preparation and Setup
2. Phase 2: Production Code Change 1 — Add helper
3. Phase 3: Production Code Change 2 — Modify phantom_id block + SEVERITY_RULES + FIX_GUIDANCE
4. Phase 4: Test Change 3 — 5 golden-fixture asymmetric-ID unit tests
5. Phase 5: Test Change 4 — Property-based + flatline-halt + cross-cutting integration tests
6. Phase 6: Validation — lint, format, tests
7. Phase 7: Restrictions Audit — verify 7 restrictions hold

**Effective patterns extracted:**
- **Production code changes are SEPARATE phases from test changes** — Phases 2-3 are code; Phases 4-5 are tests. Roadmap rewrite should similarly separate: R0.X / R1.X.code phases vs R0.X.tests / R1.X.tests sub-phases per Contract item.
- **Final "Restrictions Audit" phase** verifies declared invariants still hold — directly applicable to Brittleness-Elimination Contract items #5 (no fragility stubs CI lint), #6 (parser consistency), #7 (retry contract). Roadmap rewrite's final phase should explicitly enumerate ALL 10 contract items as a checklist.

### 2.3 TASK-RF-20260525-150000 (556L, 5 phases + 1 phase gate, single-module refactor with verification re-run)

**Phase shape (precedent C):**
1. Phase 1: Preparation and Discovery
2. Phase 2: Source-Code Refactor (`integration_contracts.py`)
3. Phase 3: Test Fixture Authoring + 7 New Test Methods (`test_integration_contracts.py`)
4. Phase 4: Backward-Compatibility Verification + **Live re-run** (TUIBBS-scp pipeline)
5. Phase 5: Sync, Lint, Documentation
6. Phase Gate: Task-Integrity QA (rf-qa) — terminal gate before completion

**Effective patterns extracted:**
- **Live pipeline re-run as Phase 4** — directly applicable to roadmap rewrite's R1.4 cutover criterion ("3 consecutive matching releases"). Each tool-write step migration should include a live MultiModelSwarm re-run or equivalent.
- **Terminal Phase Gate (not per-phase gates)** — alternative to sc-reflect-rebuild's per-phase pattern; better for scope where only the final state matters. Roadmap rewrite should use BOTH: per-phase gates for the substrate phases (R0.3 contracts, R1.2 envelope) AND a terminal gate for the cleanup phase (R1.6).

### 2.4 TASK-RF-20260526-102600 (373L, 5 phases — minimal canonical shape)

**Phase shape (precedent D — baseline):**
1. Phase 1: Preparation and Setup
2. Phase 2: Implementation
3. Phase 3: Testing & Verification
4. Phase 4: Final QA Gate
5. Phase 5: Post-Completion

**Application:** This is the minimal viable shape. The roadmap rewrite is too large for it — but EACH sub-phase within R0.1, R0.2, R0.3, R1.1, etc. internally follows this 5-step rhythm (Prep → Implement → Test → Gate → Post).

### 2.5 Recommended composite phase shape for roadmap rewrite

Combining precedents A+B+C: ~14 top-level phases, with each major R-phase containing internal (Implementation + Test + QA Gate) sub-structure. Final phase = Restrictions Audit + Terminal QA Gate. Estimated final task file: **1,500-2,500 lines** (above sc-reflect's 657L because of larger LOC delta and more Contract items, but bounded by template discipline).

**Migration/cutover sequencing pattern (from precedent C + Vector A "stage one step at a time, side-by-side ≥3 releases"):**
- Each R1.4 sub-phase: (a) implement tool-write version, (b) dual-write with markdown for 1 release, (c) compare outputs in CI (`test_tool_write_step_<N>_parity.py`), (d) repeat for 2 more releases, (e) IF all 3 parity checks PASS, delete markdown path, ELSE another release cycle (L5 conditional).

---

## SECTION 3 — RECURRENCE CORPUS FIXTURE TREE (Contract #1)

### 3.1 Current state of `tests/roadmap/`

- **64 test files** at `tests/roadmap/*.py` (LOC ≈ 28,036 per research-notes.md).
- **Only one fixture-loading subdir:** none. `find tests/roadmap/ -maxdepth 2 -type d` returns only `tests/roadmap/` itself and `__pycache__/`.
- **conftest.py is minimal** — `tests/roadmap/conftest.py:1-39` only registers a session-scoped `audit_trail` fixture re-exported from elsewhere. No fixture directories, no fixture-loading helpers.
- **Existing eval-style tests** (`test_eval_convergence_multirun.py`, `test_eval_finding_lifecycle.py`, `test_eval_gate_ordering.py`, `test_eval_gate_rejection.py`) construct test inputs inline rather than loading from a fixture corpus.

**Verdict:** The recurrence corpus directory tree per Contract #1 is **NEW**. No precedent fixture-directory layout exists in `tests/roadmap/` to mirror.

### 3.2 Proposed recurrence corpus tree

Recommended layout under `tests/roadmap/fixtures/recurrence/`, keyed by failure class (master report rows #1-22):

```
tests/roadmap/fixtures/recurrence/
├── README.md                          # how to add a new recurrence case + naming convention
├── anti_instinct/
│   ├── multimodelswarm_fp_case.md     # the canonical MultiModelSwarm false positive (recurrence #6)
│   ├── multimodelswarm_fp_case.expected.json  # expected scanner output (zero findings post-fix)
│   ├── valid_obligation_case.md       # a true obligation that MUST be flagged
│   └── valid_obligation_case.expected.json
├── spec_fidelity/
│   ├── phantom_id_asymmetric_case.md
│   ├── phantom_id_asymmetric_case.expected.json
│   ├── fail_open_default_case.md      # case that previously fail-opened (master:§Flaw 4)
│   └── fail_open_default_case.expected.json
├── frontmatter_parser/
│   ├── disagreeing_parsers_case.md    # input that exposed _parse_frontmatter vs _check_frontmatter disagreement (Contract #6)
│   └── disagreeing_parsers_case.expected.json
├── retry_contract/
│   ├── retry_loop_no_terminal_case.md # case that exposed non-terminating retry (Contract #7)
│   └── retry_loop_no_terminal_case.expected.json
├── threshold_registry/
│   ├── duplicate_threshold_case.py    # case that exposed duplicate threshold definition (Contract #8)
│   └── duplicate_threshold_case.expected.json
└── id_containment/
    ├── spec_roadmap_drift_case.md     # case where roadmap IDs drifted from spec (Contract #9)
    └── spec_roadmap_drift_case.expected.json
```

**Naming convention rationale:**
- `<failure_class>/<case_name>.<ext>` — directory by failure class makes it trivial to add new cases per class (Contract #1 requires ≥1 case per recurrent failure; this lets future incidents add a 2nd, 3rd case without restructuring).
- `<case_name>.expected.json` paired with each input — pytest test reads input, runs through pipeline, asserts equality with expected. Mirrors the golden-fixture pattern from TASK-RF-20260527055700-spec-fidelity-canonicalizer.md Phase 4 ("5 golden-fixture asymmetric-ID unit tests").
- `README.md` at root documents the "add a recurrence case" workflow so future incidents land here automatically.

### 3.3 Existing fixture pattern to follow

The closest existing fixture pattern in the codebase is **NOT** under `tests/roadmap/` but the golden-fixture-test pattern used in TASK-RF-20260527055700-spec-fidelity-canonicalizer (Phase 4: "Test Change 3 — Add 5 golden-fixture asymmetric-ID unit tests" — test file at `tests/roadmap/test_structural_checkers.py`'s `TestSignaturesChecker` class, per execution-log line `[2026-05-27 06:43]`). These tests construct input/expected pairs **inline** today.

The recurrence corpus migrates that inline pattern to **disk-backed fixtures** so:
1. Fixtures are visible/diffable independently of test code.
2. Non-engineers can add cases without touching pytest code.
3. The same fixture can be loaded by multiple test files (e.g., a parser-disagreement fixture loaded by both `test_parser_consistency.py` and `test_recurrence_regression.py`).

### 3.4 Loader pattern (recommended for `tests/roadmap/conftest.py` extension)

Add to existing `tests/roadmap/conftest.py:1-39` a new session-scoped fixture:

```python
@pytest.fixture(scope="session")
def recurrence_corpus_dir():
    """Path to tests/roadmap/fixtures/recurrence/ — base for all recurrence cases."""
    return Path(__file__).parent / "fixtures" / "recurrence"

@pytest.fixture
def recurrence_case(request, recurrence_corpus_dir):
    """Parametrized: load (input_path, expected_json) for a given case id."""
    failure_class, case_name = request.param
    return (
        recurrence_corpus_dir / failure_class / f"{case_name}.md",
        json.loads((recurrence_corpus_dir / failure_class / f"{case_name}.expected.json").read_text()),
    )
```

Tests then use `@pytest.mark.parametrize("recurrence_case", [("anti_instinct", "multimodelswarm_fp_case"), ...], indirect=True)`.

This loader pattern is consistent with `conftest.py:28-37`'s session-scoped fixture style.

---

## SECTION 4 — SUMMARY HANDOFF TO TASK-BUILDER

**Template selection:** Template 02 (Complex) — confirmed correct. Granularity, handoff patterns, QA gates, code-modifying scope all require it.

**Anticipated final shape:**
- **Phases:** ~14 (per research-notes.md SUGGESTED_PHASES enumeration)
- **Checklist items:** ~80-120 (per phase: 5-12 implementation items + 1 aggregation + 1 rf-qa spawn + 1 conditional)
- **QA gates:** ~14 (one per R-phase + terminal + R1.4 sub-phase gates)
- **Test files to create:** 9 per research-notes.md (test_recurrence_regression.py through test_anti_instinct_recurrence.py)
- **Fixture directory:** NEW at `tests/roadmap/fixtures/recurrence/` with 6 failure-class subdirs (anti_instinct, spec_fidelity, frontmatter_parser, retry_contract, threshold_registry, id_containment) — naming + loader pattern documented in §3 above.
- **Final task file size:** 1,500-2,500 lines (between sc-reflect-rebuild's 657L and the absolute Template 02 size ceiling)

**Critical rules to enforce in EVERY item:**
- B2 6-element self-contained prompt with single-paragraph form
- Explicit completion gate `Once done, mark this item as complete.`
- "ensuring..." verification clause (NEVER a separate verification item)
- Error handling: `If unable to complete due to <X>, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete.`
- For QA-gate items: ADVERSARIAL STANCE + fix_authorization: true + halt-precedence guards (regression check → monotonicity → cap)
- For code-modifying items: explicit "UV-only" reminder where needed (worker agents lack CLAUDE.md context per G1)
- For `.claude/` paths: explicit "NEVER stage `.claude/{skills,commands,agents,hooks,templates}/`; edits go to `src/superclaude/` then `make sync-dev`" reminder where roadmap protocol skill prose is touched (Phase 12 per research-notes.md)

**Open question to flag:** Recurrence corpus seeding source. Contract #1 requires ≥1 fixture per RECURRENT failure (master:§Recurrence rows #1-22). The task should enumerate which of the 22 recurrence rows seed which fixture file, OR defer that mapping to the first item of the recurrence-corpus phase (which would scan master report and produce the seeding inventory as a discovery output). RECOMMEND: defer to discovery item — keeps the task definition lean and lets the worker agent derive the mapping from master report at execution time. This matches research-notes.md GAP #5.
