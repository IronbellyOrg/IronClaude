# BUILD-REQUEST: Roadmap Pipeline Brittleness-Elimination Refactor + Rewrite

**Generated:** 2026-05-31
**Source authority:** Retrospective across 64 releases + 77 tasks (262 findings, 159 failures, 61 remediations, 113 brittleness drivers identified)
**Decision verdict:** REWRITE — 4 of 5 architectural flaws classified INHERENT, 3 scope to cross-cutting state
**Workspace:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/`

---

## Goal

Eliminate the architectural and process flaws documented in the retrospective artifacts below. The work is structured as **two phases** so the cheap-but-high-value preflight intervention (R0) can ship before the substrate inversion (R1):

- **R0 — Bridge (1–2 eng-weeks):** Three preflight checks + Brittleness-Elimination Contract CI gates. Caps the top-3 cost drivers without architectural change.
- **R1 — Substrate Rewrite (6–10 eng-weeks):** Typed `PipelineEnvelope` + tool-write generators + `CodeAssertion` gate slot + `verify-implementation` terminal step + `superclaude.contracts` SoT module. ~2,800 LOC delta.

The decision rule (master:§Verdict) resolves to REWRITE because patches address each new failure shape one validator at a time, while the generator/validator asymmetry guarantees new shapes arrive faster than validators can be authored. Documented step-count growth: v4=9 → v2.22=11 → v5=13 → current=14.

## Source authority (read these before authoring the task)

1. **Master report:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave2-master-report/master-report.md` — 7 sections, 961 lines, REWRITE verdict, 5 architectural flaws with evidence chains.
2. **Vector A — Architecture:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-A-architecture.md` — MVR specification (embedded verbatim below as §MVR).
3. **Vector B — Process:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-B-process.md` — process interventions that complement the rewrite (auto-fire sc-reflect UC-1, sc:input-validate preflight).
4. **Vector C — Recurrence:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-C-recurrence.md` — Brittleness-Elimination Contract (embedded verbatim below as §Contract).
5. **Vector D — Cost:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-D-cost.md` — R0 / R1 phasing rationale and token-economics.
6. **Wave 1 partition reports (14):** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A*.md` — primary evidence; cite as `(A<N>:F-A<N>-<seq>)`.

**Hard constraint:** The task-builder MUST NOT invent new requirements. If a checklist item cannot be sourced to one of the 6 file sets above, drop it.

## Decision codification (frontmatter)

The generated task MUST carry these frontmatter fields:

```yaml
category: rewrite           # REWRITE per master:§Verdict + Vector A confirmation
phasing: r0-then-r1         # R0 bridge first, R1 substrate rewrite second
inherent_flaw_count: 4      # master:§Flaw 1, 2, 3, 5 INHERENT; Flaw 4 BOTH
cross_cutting_flaw_count: 3 # Flaws 1, 3, 5 — substrate-level
preserves:                  # what the rewrite carries forward
  - adversarial-debate-mechanism   # master:§Recurrence #18 RESOLVED-FOR-NOW
  - v3.05-deterministic-structural-checker-layer
  - convergence-wrapper-concept
inverts:                    # what the rewrite changes
  - markdown-as-interchange-substrate  # → PipelineEnvelope sidecar JSON
  - content-string-gate-signature      # → GateCriteria + CodeAssertion slot
  - llm-as-black-box-producer          # → tool-write structured outputs
  - implicit-cross-skill-contracts     # → superclaude.contracts SoT module
```

---

## §Contract — Brittleness-Elimination Contract (verbatim from Vector C Q4)

Any future fix to the roadmap pipeline MUST satisfy all 10 items below to be considered durable. Each is testable as written. **Every R0 and R1 checklist item must cite which contract items it satisfies.**

1. **Recurrence regression fixture.** The fix MUST add ≥1 named fixture to a recurrence corpus that exercises the *specific failure shape* being closed. Fixture path: `tests/roadmap/fixtures/recurrence/<failure-class>/<incident-id>.md` (or equivalent typed format). Test: `pytest tests/roadmap/test_recurrence_regression.py::test_<failure_class>` MUST FAIL on the pre-fix codebase and PASS post-fix.

2. **Dispatch-reachability invariant.** If the fix adds a new builder, runner, gate, or hook symbol, a test MUST assert the symbol is reachable from a production entry point (`_build_steps()`, `execute_sprint()`, `run_portify()`, `execute_pipeline()`). Mechanism: AST walk + dispatch-graph trace. Failure mode targeted: master:§Flaw 1 "written but not wired."

3. **Producer-side constraint preferred over validator addition.** If the fix would otherwise add a downstream validator/gate/check, the PR description MUST contain a "Generator-Constraint Considered" section explaining why a tool-write template / structured-output schema / prompt-pinned invariant on the generator side was insufficient. CI lint blocks merge if section absent on PRs touching `gates.py`, `structural_checkers.py`, or `*_validator.py`. Failure mode: master:§Flaw 2 generator/validator asymmetry.

4. **No silent PASS on empty / wrong-target inputs.** Every gate that consumes a directory, file list, or token set MUST assert `len(input) > 0` before emitting PASS. Test: `tests/roadmap/test_gate_empty_target.py` enumerates every gate symbol and asserts `gate(empty_input).status != PASS`. Failure mode: master:§Recurrence #3 wiring-verification silent PASS.

5. **No `return True` stubs with fragility comments.** A CI lint MUST block merge of any source file containing the pattern `return True\s*(#|""").*fragile|too.*hard|for.*now` in production code paths (`src/superclaude/cli/`). Existing instances flagged for active remediation, not grandfathered. Failure mode: master:§Recurrence #8 `_cross_refs_resolve` perpetual stub.

6. **Frontmatter / parser consistency invariant.** If the fix adds, modifies, or touches a frontmatter parser, a pairwise-consistency test MUST assert all other extant frontmatter parsers in the codebase agree with the new one across the 50+ blob conformance corpus. Mechanism: `tests/roadmap/test_parser_consistency.py`. Failure mode: master:§Recurrence #13 dual-parser disagreement.

7. **Retry-mutates-input contract.** Any code path adding or modifying a retry/loop/convergence step MUST assert `input_state_n != input_state_n+1` between attempts, OR carry a `retry_reason: transient_failure_only` annotation. Test surface: `test_retry_contract.py::test_no_identical_input_retry`. Failure mode: master:§Recurrence #9.

8. **Threshold registry conformance.** Every numeric threshold (severity cutoff, convergence score, retry budget, max_runs) MUST be defined in `src/superclaude/cli/roadmap/thresholds.py` (or equivalent SoT module) and read by skill prose, CLI prompts, and gate code through importable symbols — never as duplicated literals. Test: `tests/roadmap/test_threshold_registry.py` asserts no numeric threshold appears in >1 source location. Failure mode: master:§Recurrence #7 + master:§Flaw 5.

9. **Spec↔Roadmap ID-set containment.** If the fix touches generate / merge / extract / spec-fidelity, a property test on a fixture spec with declared ID set MUST assert `roadmap_id_set ⊆ spec_id_set ∪ accepted_deviation_ids` after full generate-merge. Failure mode: master:§Recurrence #4 fabricated IDs.

10. **Adversarial false-positive corpus for any regex/keyword gate.** If the fix uses a regex or keyword check on LLM-generated prose, the fix MUST add ≥3 known-false-positive fixtures from documented historical recurrences (sourced from `master-report.md` Recurrence Matrix or partition reports). Test: `pytest tests/roadmap/test_<gate>_recurrence.py`. Failure mode: master:§Recurrence #6 anti-instinct vocabulary collisions.

**Pass criterion:** A fix is durable when items 1, 2, 4 are MUST-MET for the specific failure class; items 5, 6, 7, 8 are MUST-MET when touched code matches trigger conditions; items 3, 9, 10 are MUST-MET when the failure class is in scope. CI gates 1, 2, 4, 5 are pipeline-blocking; 3, 6–10 are PR-review-blocking with explicit override-with-reason allowed.

---

## §MVR — Minimum Viable Rewrite Architecture (verbatim from Vector A Q4)

The rewrite **preserves** what works — adversarial debate (master:§Verdict; A8 P3 pattern), the v3.05 deterministic structural-checker layer (`structural_checkers.py`), the convergence wrapper concept (`convergence.py`) — and **inverts the substrate** along four axes. Smallest delta that turns four of the five INHERENT flaws into structurally impossible failure shapes.

### 1. State model — `PipelineEnvelope`

```python
# new: src/superclaude/cli/roadmap/envelope.py
@dataclass(frozen=True)
class PipelineEnvelope:
    """Typed cross-step state. Sidecar JSON; markdown is render-only."""
    release_id: str
    spec_hash: str
    spec_ids: SpecIdRegistry          # {FR: [...], NFR: [...], SC: [...], D: [...]}
    artifacts: dict[StepId, ArtifactRef]   # {step_id: Path + content_hash}
    findings: list[Finding]                # typed, additive across steps
    counts: dict[str, int]                 # gate-pass signals — written by Python, NOT LLM
    convergence: ConvergenceState | None
    accepted_deviations: list[AcceptedDeviation]
```

- Persisted as `.<release>/envelope.json`; every step reads the envelope, writes its artifact, and a *deterministic Python post-step* extracts canonical fields into the envelope. LLM never writes gate-pass counts directly. **Kills master:§Flaw 3.**
- One `_parse_frontmatter` lives in the post-step extractor only; the two divergent variants at `gates.py:168` and `_check_frontmatter` are deleted.

### 2. Gate contract — `GateCriteria` admits code-graph predicates

```python
@dataclass
class GateCriteria:
    required_envelope_fields: list[str]      # was: required_frontmatter_keys
    semantic_checks: list[SemanticCheck]     # (envelope) -> Finding | None
    code_assertions: list[CodeAssertion]     # NEW: (envelope, repo_path) -> Finding | None
```

- `CodeAssertion` instances import-and-call from `src/`, walk AST, check `step.id` appears in a dispatch map. **Kills master:§Flaw 1.**
- Wire `build_certify_step()` (currently `executor.py:1899`, unreached) as the final step; CodeAssertion guarantees no future step ships unwired.

### 3. Generator-constraint mechanism — tool-write at every LLM step

- Every `build_*_prompt` in `prompts.py` is rewritten as a tool definition with a JSON schema. The LLM cannot return free-form markdown for the gate-relevant payload; only the tool's JSON output is consumed.
- The schema for `merge`, `generate-*`, and `remediate` includes a `roadmap_ids` array that MUST be a subset of `envelope.spec_ids ∪ envelope.accepted_deviations`. **Kills master:§Top-3 #3 (phantom IDs)** and is the generator-side constraint master:§Flaw 2 says is missing.
- Markdown artifacts are *rendered from* tool output by a deterministic Jinja template. Markdown becomes presentation, not interchange.

### 4. Terminal verification link — Tasklist → AST

- New step `verify-implementation` runs after `tasklist` (or after `certify` in the roadmap-only path), with a `CodeAssertion`-only gate:
  - For each FR in `envelope.spec_ids[FR]`, the assertion either (a) finds an importable callable matching the spec's name binding, (b) finds it via `fidelity_checker`'s AST scan (`fidelity_checker.py:165-200`), or (c) matches an accepted deviation. No fail-open default (`fidelity_checker.py:287-303` `found=True` is deleted).
  - Failure produces a HIGH `Finding` and halts. **Kills master:§Flaw 1 evidence chain entirely.**

### 5. Contract registry — `superclaude.contracts`

```python
# new: src/superclaude/contracts/__init__.py
ID_PATTERNS = {"FR": r"FR-\d+(?:\.\d+)?", "NFR": r"NFR-\d+", "SC": r"SC-\d+", "D": r"D-?\d+"}
CONVERGENCE_THRESHOLDS = {"sc:roadmap": (0.7, 0.5), "sc:release-split": (0.7, 0.5)}
GATE_FIELD_NAMES = {"deviation_analysis": {"ambiguous": "ambiguous_deviations"}}
RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}
```

- Arch-lint check fails CI if any module redefines a constant a contract owns. **Kills master:§Flaw 5** by collapsing dozens of coupling points.

### Effort envelope (Vector A INFERENTIAL)

- `envelope.py` + post-step extractors: ~600 LOC new; deletes ~150 LOC of duplicate frontmatter parsing.
- `GateCriteria` extension + 14 step migrations: ~400 LOC delta.
- Tool-use rewrite for 9 LLM steps: ~1500 LOC across `prompts.py` (currently 85K) + new schema module.
- `superclaude.contracts` + arch-lint extensions: ~300 LOC.
- **Net: ~2,800 LOC delta** against ~8,200 LOC current pipeline core.

---

## R0 — Bridge phase (1–2 eng-weeks)

Vector D ranks these three as the highest-EV pre-flight checks. They ship before R1 and provide immediate relief.

1. **Spec-ID registry** (Contract item #9). Build `src/superclaude/cli/roadmap/id_registry.py` extracting declared IDs from spec at extract time; merge gate asserts every roadmap ID ∈ extracted set ∪ accepted-deviations. Closes ~7 attempts on Recurrence row #4.

2. **Anti-instinct vocab-lint with allowlist** (Contract item #10). Extend `obligation_scanner.py` (or its config) to accept an inline allowlist for known-safe noun uses (`stub transport`, `stub-worker parallelism test`, etc.). The user's current MultiModelSwarm blocking failure (lines 207/211/213) is the canonical seed case — add it as the first 3 fixtures. Closes ~4 attempts on Recurrence row #6.

3. **Pre-merge contract-schema validator** (Contract item #5 + #8). Build minimal `superclaude.contracts.__init__` module with `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`. Add arch-lint check that fails CI if any of these constants are re-defined elsewhere. Closes ~3 attempts on Recurrence row #7 and the `_cross_refs_resolve` stub class on row #8.

**R0 acceptance:** All 3 land; corresponding Contract items become PR-blocking CI gates; recurrence corpus seeded with the MultiModelSwarm anti-instinct case; the user's currently-blocking pipeline run reaches `anti-instinct PASS` after the allowlist entry is added.

---

## R1 — Substrate rewrite phase (6–10 eng-weeks)

R1 implements the §MVR specification above. Sequencing:

1. **R1.1 — `superclaude.contracts` SoT module.** Already partially scaffolded in R0; extend with full `RETURN_CONTRACTS`, threshold registry, and arch-lint coverage.
2. **R1.2 — `PipelineEnvelope` dataclass + sidecar JSON persistence.** New file + post-step extractors. Migration strategy: dual-write envelope + markdown for one release cycle, then markdown becomes render-only.
3. **R1.3 — `GateCriteria.code_assertions` slot + first `CodeAssertion` implementation.** Use `build_certify_step()` wiring as the proof-of-concept assertion.
4. **R1.4 — Tool-write rewrite for 9 LLM steps.** Largest sub-task; Vector A estimates ~1,500 LOC. Stage one step at a time, run side-by-side against current markdown output for ≥3 releases each before deletion.
5. **R1.5 — `verify-implementation` terminal step.** Wires up the Tasklist → AST link; consumes envelope; final gate.
6. **R1.6 — Migration cleanup.** Delete duplicate frontmatter parsers, `return True` stubs, fail-open defaults.

**R1 acceptance:** All Contract items 1–10 are CI-enforced; pipeline runs on every spec under `.dev/releases/complete/*/spec*.md` without anti-instinct false-positives of the master report's failure-taxonomy classes; recurrence corpus contains ≥1 case per RECURRENT row in master report's Recurrence Matrix.

---

## Scope

- **In:**
  - `src/superclaude/cli/roadmap/` (entire pipeline core)
  - `src/superclaude/contracts/` (new SoT module)
  - `tests/roadmap/` (recurrence corpus, contract gate tests)
  - `src/superclaude/skills/sc-roadmap-protocol/` (skill prose alignment with new envelope/registry)
  - `make lint-architecture` (extend with contract-registry checks)

- **Out:**
  - `src/superclaude/cli/sprint/` and downstream consumers — Vector B's sc:input-validate preflight is a separate concern; queue as follow-up if not already in flight.
  - Tasklist generation internals — already scoring well per A6 ("tasklist generation is the strongest stage").
  - `commands.py` CLI surface — preserved unchanged per Vector A effort envelope.
  - Process changes (auto-fire sc-reflect UC-1) — Vector B recommendations are a parallel work-stream and out of scope here.

## Acceptance gates (R0 + R1 combined)

1. **All Contract items 1–10 enforced as CI gates** (items 1, 2, 4, 5 pipeline-blocking; items 3, 6–10 PR-review-blocking).
2. **All current passing tests in `tests/roadmap/` still pass.**
3. **The pipeline runs on every spec under `.dev/releases/complete/*/spec*.md`** (or the directory's equivalent merged-requirements file) without halting on anti-instinct false-positives of the classes catalogued in master report's failure taxonomy.
4. **Recurrence corpus seeded:** `tests/roadmap/fixtures/recurrence/` contains ≥1 named fixture for every RECURRENT row in master report's Recurrence Matrix (rows #1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 19, 20, 21, 22).
5. **MultiModelSwarm anti-instinct halt resolved.** The user's currently-blocking pipeline run at `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/` succeeds end-to-end after R0.
6. **Step count does not increase.** Per master's "monotonic step growth" thesis, the rewrite consolidates rather than appends — final pipeline step count ≤ current (14).
7. **Zero `return True` fragility stubs remain in `src/superclaude/cli/`.**
8. **`verify-implementation` terminal step is live and wired** — no PR can ship roadmap-pipeline code that fails the dispatch-reachability invariant (Contract #2).

## Evidence

All findings cited in scope come from the 6 source-authority files. Specifically:

- **Master report:** §Executive Summary, §Failure Taxonomy, §Recurrence Matrix, §Pipeline-step Heat Map, §Architectural-flaw Thesis, §Verdict
- **Vector A:** Q1 architecture map (`executor.py:1947-2025`, `gates.py:317-383`, `fidelity_checker.py:289-303`), Q4 MVR (embedded above)
- **Vector B:** Q1 non-architectural failures, Q3 protocol enforcement gaps, Q5 people-flexible vs people-trapped classification
- **Vector C:** Q4 Brittleness-Elimination Contract (embedded above), Q5 coverage map (dangerous Uncovered+Passes quadrant)
- **Vector D:** Q3 early-failure detection ROI (R0 ranking), Q5 cost-effectiveness ranking (R0+R1 phasing)
- **Wave 1 partition reports:** Cited via `(A<N>:F-A<N>-<seq>)` format throughout

**The task-builder MUST NOT invent requirements.** If a checklist item cannot be sourced to one of the above, drop it.

## Notes

- Sync `src/superclaude/` → `.claude/` via `make sync-dev` before any commits (CLAUDE.md absolute rule).
- PR target: `IronbellyOrg/IronClaude` only (CLAUDE.md absolute rule). NEVER `gh pr create` without `--repo IronbellyOrg/IronClaude`.
- NEVER stage `.claude/{skills,commands,agents,hooks,templates}/*` (CLAUDE.md absolute rule).
- This task is large and phased — R0 should land before R1 starts, and R1 should land step-by-step with at-least-one-release-cycle co-existence per migrated step (per Vector A).
- The full retrospective corpus (~430KB across 14 partition reports + master + 4 vectors) lives under `.dev/troubleshoot/roadmap-pipeline-retrospective/` — do NOT delete or move; the recurrence-corpus fixtures (Contract item #1) source from these.
