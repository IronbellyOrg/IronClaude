# BUILD-REQUEST — Durable fix: tool-write schema roadmap_ids ↔ ID family SoT

> Input for `/task-builder`. Captures verified analysis from two background agents
> (concurrent-work analysis + brainstorm) plus a decision-gate grep that **corrected**
> the brainstorm's core assumption. Branch: `refactor/roadmap-pipeline-r0-r1-rewrite`.
> Date: 2026-06-02.

## GOAL
Eliminate the drift between the requirement-ID **source of truth** (`superclaude.contracts.ID_PATTERNS`) and the **tool-write JSON schemas'** `roadmap_ids` regex patterns, in a way that is **durable** (auto-covers future family additions and fails CI on drift) and **does not break** the legitimate tool-write-only families. Concretely:
1. **Add the `MD` family** (`M\d+-D-?\d+`, milestone-prefixed deliverable IDs) to the `roadmap_ids` pattern in all four tool-write schemas — it is genuinely missing and a roadmap using `M{n}-D{nn}` IDs is currently rejected at schema validation in tool-write mode.
2. **Design and establish the correct family-set relationship** (see "DESIGN DECISION" below) so the schemas derive from a single source rather than four hand-maintained, mutually-inconsistent copies.
3. **Reconcile** the four schemas, which currently disagree on the family set.
4. **Rebuild the four guard tests**, which are structurally broken (they passed the MD drift silently).

## WHY
The `MD` family was added to `contracts.ID_PATTERNS` in commit `cf3594d2` (R5 review remediation) and is correctly threaded through the Python markdown path (spec_parser, structural_checkers, id_registry, gates). But the tool-write JSON schemas — authored concurrently in commit `c542b6bf` (R1.4) — hard-code their own `roadmap_ids` regex and omit `MD`. Tool-write mode is currently **non-default** (cutover deferred to R1.6 per commit `44f78a01`), so this is **latent / LOW-MEDIUM severity** — but it must be closed before tool-write cutover, and the broken guard tests give a false sense of safety today.

## VERIFIED ANALYSIS (ground truth — researchers should RE-VERIFY all file:line at build time; line numbers drift on this hot branch)

### The four schemas + their `roadmap_ids` patterns (PERSONALLY VERIFIED this session)
- `src/superclaude/cli/roadmap/templates/tool_schemas/generate.schema.json` (~L140): `^(FR-\d+(?:\.\d+)?|NFR-\d+(?:\.\d+)?|SC-\d+|G-\d+|D-?\d+|DM-\w+|API-\w+|COMP-\w+|TEST-\w+|MIG-\w+|OPS-\w+|OQ-\w+)$`
- `merge.schema.json` (~L156): **same as generate** (a test pins merge==generate).
- `extract.schema.json` (~L134): `^(FR-…|NFR-…|SC-…|G-…|D-?\d+|COMP-\w+|DM-\w+)$` — **omits API/TEST/MIG/OPS/OQ**.
- `extract_tdd.schema.json` (~L218): has DM/API/COMP/TEST/MIG/OPS — **omits OQ**.
- **None of the four contains `MD`.** (verified: `grep 'M\d+-D'` → no hits in any schema.)

### The SoT (PERSONALLY VERIFIED)
- `src/superclaude/contracts/__init__.py` ~L64-77: `ID_PATTERNS` = `MD, FR, NFR, SC, G, D` (6 anchor-free bodies; `MD = r"M\d+-D-?\d+"`, ordered before `D`). Note the **MD⊂D substring trap**: the `D` body `D-?\d+` is a literal substring of the `MD` body `M\d+-D-?\d+`.
- `src/superclaude/tools/arch_lint.py` enforces "no `.py` re-inlines an `ID_PATTERNS` body" but **only scans `.py`** — it never inspects JSON schemas. So JSON drift is unguarded by arch_lint.

### CRITICAL CORRECTION — the extra families are REAL, not removable (PERSONALLY VERIFIED via decision-gate grep)
The brainstorm agent assumed `DM/API/COMP/TEST/MIG/OPS/OQ` were "schema-only speculative extras with zero consumers" and recommended REMOVING them. **That assumption is FALSE.** A grep of `tests/roadmap/` found **55 occurrences** of these families used as real `roadmap_ids` in tool-write fixtures:
- `test_tool_write_step_extract_tdd.py`: `DM-001, API-001, COMP-001, TEST-001, MIG-001, OPS-001` (full set, multiple times)
- `test_tool_write_step_generate.py` / `merge.py`: `COMP-loader, API-render, OPS-metrics, TEST-e2e, OQ-1, DM-config, API-merge, …`
- `OQ-` also in `test_merge_completeness.py`, `test_cosmetic_remediator.py`
The brainstorm only checked the SoT-pattern files (contracts/spec_parser/id_registry/structural_checkers), not the tool-write test fixtures. **REMOVE is OFF** — it would break ~55 test usages.

### The true relationship: SUPERSET, not equality
```
tool-write roadmap_ids families  =  ID_PATTERNS spec families (FR/NFR/SC/G/D/MD)
                                   ∪ tool-write-only families (DM/API/COMP/TEST/MIG/OPS/OQ)
```
The tool-write extract step lets the LLM declare roadmap-internal IDs (components, APIs, tests, migrations, ops, open-questions, data-models) structurally — a deliberately broader universe than the spec-side regex extraction (which only recognizes the 6 `ID_PATTERNS` families). The markdown/regex path (`spec_parser.extract_requirement_ids`, derived from `ID_PATTERNS`) only ever sees the 6 spec families; the tool-write path's broader set is legitimate.

### The broken guard tests (from brainstorm agent — RE-VERIFY)
Four tests already exist to catch exactly this drift and silently passed it:
- `tests/roadmap/test_tool_write_step_{extract,extract_tdd,generate,merge}.py` — `test_*_schema_id_pattern_matches_contracts` (e.g. extract ~L129-144).
- Bug 1: they iterate a **frozen literal tuple** `("FR","NFR","SC","G","D")` (e.g. ~L140), NOT `ID_PATTERNS.keys()` → `MD` was never checked.
- Bug 2: they use **substring containment** (`ID_PATTERNS[family] in pattern`), one-directional. Because `D-?\d+ ⊂ M\d+-D-?\d+`, even a naive "loop the keys" fix would FALSELY PASS for MD. **The fix must use exact/arm-level matching, not substring.**
- `test_merge_schema_matches_generate_id_pattern` (~merge L271-280) pins merge==generate but nothing pins extract/extract_tdd.

### Runtime wiring (from brainstorm agent — RE-VERIFY at build time)
- `src/superclaude/cli/roadmap/tool_writer.py`: `load_schema` (~L67-91, `json.loads`), `validate_tool_output` (~L94+) runs BEFORE the Contract #3 subset gate `validate_id_subset` (~L344-370) inside `render_step_tool_write_with_id_check` (~L455-495).
- `src/superclaude/cli/roadmap/executor.py` ~L1288 wires the id-checked tool-write render for generate/merge.

## DESIGN DECISION (the task must resolve this, with evidence)
Where should the **tool-write-only family set** live so the schemas can derive from a single source? Options the task should evaluate and pick (default lean: a dedicated SoT constant, NOT polluting `ID_PATTERNS`):
- **(a) Separate SoT constant** in `superclaude.contracts` (e.g. `TOOL_WRITE_EXTRA_ID_FAMILIES` or `ROADMAP_ID_FAMILIES`), with a helper `roadmap_ids_pattern() = "^(" + "|".join(ID_PATTERNS.values() ∪ extras) + ")$"`. Schemas derive from this; spec-side regex extraction keeps using only `ID_PATTERNS`. Keeps the spec/tool-write universes correctly distinct.
- **(b) Promote the extras into `ID_PATTERNS`** — REJECT unless a maintainer confirms these are spec-extractable families (they are NOT today; promoting would pull COMP/API/etc. into `spec_parser` regex extraction, changing markdown-path behavior). Document why rejected.
- Also decide: are the per-schema differences (extract omits API/TEST/MIG/OPS/OQ; extract_tdd omits OQ) **intentional per step semantics** or **drift**? Investigate via the schema `$comment` fields + git blame `c542b6bf`. If intentional, the derivation must be per-step-aware; if drift, unify all four.

## REQUIRED WORK (task phases should cover)
1. Investigate + decide the family-SoT design (the DESIGN DECISION above) and the intentional-vs-drift question for the per-schema differences. Write a decision artifact.
2. Add the family-set SoT (per the decision) to `superclaude.contracts`, with a `roadmap_ids_pattern()` (or per-step variant) assembler; export in `__all__`. Handle the anchor-free→`^(…)$` wrap deterministically; preserve MD-before-D ordering.
3. Regenerate the `roadmap_ids.items.pattern` in all four schemas from the assembler (this is where `MD` lands), reconciling per the decision (unify, or keep per-step sets if intentional).
4. Rebuild the four `test_*_schema_id_pattern_matches_contracts` guard tests: iterate the live family set (not a frozen tuple), assert **arm-level / exact** match (not substring) so the MD⊂D trap can't recur, and add an explicit regression asserting `MD` is present as its OWN alternation arm. Keep/extend the merge==generate pin to cover all four as appropriate.
5. Verify: `uv run pytest tests/roadmap/ -k tool_write` (all green, the 55 extra-family usages still pass), `make lint-architecture` exit 0, `make verify-sync` clean, and a positive check that a tool-write `roadmap_ids` containing `M1-D01` now validates.

## ACCEPTANCE CRITERIA
- All four schemas' `roadmap_ids` pattern includes the `MD` family (a `M1-D01` roadmap_id validates in tool-write mode).
- The four tool-write-only families remain supported (the 55 existing fixture usages still pass — zero test regressions).
- The schema patterns derive from a single SoT (no more four hand-maintained copies); a CI guard fails on future SoT/schema drift and uses exact/arm-level matching (immune to the MD⊂D substring trap), iterating the live family set.
- The per-schema-difference question is resolved with evidence (intentional → per-step derivation documented; drift → unified).
- `make lint-architecture` exit 0; `make verify-sync` clean; full roadmap-suite delta shows no new failures.

## REPO DISCIPLINE
- `src/superclaude/` is SoT. The tool-write schemas live under `src/superclaude/cli/roadmap/templates/tool_schemas/` — **NOT** a `make sync-dev` target (sync-dev covers skills/agents/commands/hooks/templates-workflow, not `cli/`), so no `.claude/` mirror is involved; **never stage `.claude/`** regardless.
- UV only (`uv run pytest …`). Stay on branch `refactor/roadmap-pipeline-r0-r1-rewrite`; never commit to master.
- Contract #8: the `MD` (and any) ID-pattern body must remain defined only in `superclaude.contracts` — never re-inlined as a literal in a `.py` consumer (arch_lint Rule 2). The schema patterns are JSON (arch_lint doesn't cover them — that's the gap this task closes via the guard tests).

## OUT OF SCOPE
- The ~57 pre-existing `tests/sprint/test_tui_monitor.py` / `test_watchdog.py` failures (separate issue).
- The markdown/regex spec-extraction path (already correct for MD).
- Tool-write cutover itself (R1.6).
