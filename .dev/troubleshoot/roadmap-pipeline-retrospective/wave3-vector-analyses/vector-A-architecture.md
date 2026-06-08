# Vector A — Architecture Critique

**Role:** Senior systems architect — architectural-flaw analysis grounded in the master report and the current `src/superclaude/cli/roadmap/` tree.
**Master report:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave2-master-report/master-report.md`
**Code root:** `src/superclaude/cli/roadmap/` (executor 3,701 LOC; gates 1,441 LOC; convergence 778 LOC; obligation_scanner 825 LOC; structural_checkers 1,069 LOC; fidelity_checker 417 LOC)
**Evidence tier:** discovery — master citations `(master:§N)` / `(A<N>:F-A<N>-<seq>)`; file:line for code; `INFERENTIAL` for synthesis claims beyond direct citation.

---

### Q1 — Current architecture map

The roadmap pipeline is a **markdown-first, gated sequential executor** with a parallel generator fan-out and an opt-in convergence wrapper around a single late-stage gate. The component graph as of `executor.py` is:

```
RoadmapConfig + spec.md
    │
    ▼
[detect_input_type] ──► [extract | extract_tdd]                    (LLM)
    │                          │
    │                          ▼
    │       ┌─────────── extraction.md (markdown + YAML frontmatter)
    │       │
    │       ▼
    ├──► [generate-opus-architect]   ─┐  parallel group
    └──► [generate-sonnet-architect] ─┘  (LLM × 2)
                    │
                    ▼
              [diff] → [debate] → [score] → [merge]                (LLM × 4)
                    │
                    ▼
              [anti-instinct]    ◄── ANTI_INSTINCT_GATE  (pure regex; gates.py:1353)
                    │
                    ▼
              [test-strategy]                                       (LLM)
                    │
                    ▼
   ┌── [_run_convergence_spec_fidelity (max_runs=3)]               (LLM ⊕ Python checkers)
   │      │      gate=None if convergence_enabled else SPEC_FIDELITY_GATE
   │      │                                            (executor.py:2167)
   │      ▼
   │   [deviation-analysis] → DEVIATION_ANALYSIS_GATE
   │      │
   │      ▼
   │   [remediate]                                                  (LLM regenerate-or-patch)
   │      │
   │      ▼
   │   [validate]  (warn-not-fail; A4:F-A4-002)
   │      │
   │      ▼
   │   [wiring-verification] → WIRING_GATE  (AST/import scan; src/-targeted)
   │
   └── build_certify_step()  defined at executor.py:1899
         BUT _build_steps() (executor.py:1947) ends at remediate/validate;
         no `step.id=="certify"` dispatch — confirmed dead code (A11:F-A11-011).
```

**Data flow (the substrate).** Every step's *input* is a `Path` to a markdown file produced by the prior step, and every step's *output* is another markdown file. Cross-step state — gate-pass signals (`high_severity_count`, `convergence_score`, `undischarged_obligations`, `fingerprint_coverage`, `certified`, `analysis_complete`, `routing_*`, `slip_count`, `ambiguous_deviations`) — flows through **YAML frontmatter at the top of the same markdown artifact** that the LLM produces (`gates.py:168` `_parse_frontmatter`). Every gate is fundamentally `(content: str) -> bool` over that frontmatter, e.g. `_no_ambiguous_deviations` (gates.py:389-412), `_certified_is_true` (gates.py:415-430), `_convergence_score_valid` (gates.py:371-383).

**State model.** There is no typed cross-step state object. The closest thing is:
- **`DeviationRegistry`** (`convergence.py:90-200`) — file-backed JSON sidecar at the spec-fidelity convergence layer *only*; it survives runs within one release but is read by nothing else in the pipeline.
- **`TurnLedger`** — convergence-mode budget accounting (constants `CHECKER_COST=10`, `REMEDIATION_COST=8`, `REGRESSION_VALIDATION_COST=15`, `CONVERGENCE_PASS_CREDIT=5` at `convergence.py:26-29`); also exists only inside the convergence wrapper.
- **`.roadmap-state.json`** — exists per release but is observability/resume metadata, not a typed schema enforced at handoff.

The remaining 12 of 14 pipeline steps share state by *re-parsing the prior step's markdown*. The frontmatter parser is duplicated in two semantically-divergent variants — `_parse_frontmatter` byte-0-strict (`gates.py:168-189`) vs `_check_frontmatter` `re.MULTILINE` — and they disagree on validity (A11:F-A11-010; master:§"Pipeline-step Heat Map"/extract row). The compound-reliability arithmetic is severe: at the historical per-step 0.9 reliability cited in (A2a:F-A2a-001), an 8-step LLM chain delivers 0.9⁸ ≈ 43% all-pass probability.

**Gate model.** Gates are pure-data `GateCriteria` instances (gates.py module-level constants like `ANTI_INSTINCT_GATE = GateCriteria(...)` at gates.py:1353-1375) consisting of required-frontmatter keys plus a list of `SemanticCheck(name, check_fn, failure_message)` tuples whose `check_fn` is always `(content: str) -> bool`. There is **no slot in the GateCriteria contract** for an AST visitor, an importable-callable check, a behavioral assertion, or a code-graph traversal — `GateCriteria` literally cannot express "import the function this artifact claims to register and confirm it is callable from the production entry point" (master:§Flaw 1).

**Citations (≥3 file:line):**
- `executor.py:1899` — `build_certify_step()` builder defined but not added to `_build_steps()` (1947). Direct manifestation of master:§Flaw 1 / (A11:F-A11-011).
- `executor.py:2167` — `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` — convergence path bypasses external gate. (A4:F-A4-003) confirmed live.
- `gates.py:1353-1375` — `ANTI_INSTINCT_GATE` requires `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage` frontmatter keys, AND-composed; no escape valve (master:§Flaw 4 / (A11:F-A11-001)).
- `gates.py:18` — annotated bug `# Pre-existing bug: ambiguous_count/ambiguous_deviations field mismatch (B-1)`; gates.py:389-412 confirms `_no_ambiguous_deviations` reads `ambiguous_deviations` while writer historically emits `ambiguous_count` (A11:F-A11-009 unfixed).
- `fidelity_checker.py:287-303` — `found=True` (fail-open) when `expected_names` empty; the file-level docstring at `fidelity_checker.py:16-20` codifies fail-open as policy ("R-3 Mitigation"). Direct evidence for master:§Flaw 4 silent-skip half.

---

### Q2 — Which of the 5 master-report flaws are truly INHERENT?

| # | Flaw (short) | Master classification | My verdict | "No patch can fix this without changing X" |
|---|---|---|---|---|
| 1 | Artifact-centric gate, no code-reaching terminal link | INHERENT | **INHERENT (confirmed)** | No patch fixes this without changing the **`GateCriteria` + `SemanticCheck` contract** (`gates.py`) to admit non-`(content:str)->bool` predicates — specifically a code-graph predicate accepting `(artifact, source_tree) -> CallGraphAssertion`. Wiring `build_certify_step()` (executor.py:1899) into `_build_steps()` (executor.py:1947) is necessary but *insufficient*: certify itself is another markdown-producing LLM step, not an AST verifier. |
| 2 | Generator/validator asymmetry, no generator-side constraints | INHERENT | **INHERENT (confirmed)** | No patch fixes this without changing **`ClaudeProcess` invocation contract** in `superclaude.cli.pipeline.process` — every `build_*_prompt` in `prompts.py` (85,995 bytes of prose) feeds a raw stdout-captured subprocess. Constraining the generator requires (a) tool-use structured-output enforcement (currently only `MERGE_GATE` uses `_validate_merge_completeness` per A8:F-A8-015), and (b) a generator-bound schema registry that the prompt cannot evade. The 14-step monotonic growth (master:§Exec Summary: 9→11→13→14) is the operational signature. |
| 3 | Cross-step state lives in markdown frontmatter | INHERENT | **INHERENT (confirmed)** | No patch fixes this without changing **the step-handoff substrate**: every `Step` in `pipeline.models` passes `Path` to a `.md` file; `_parse_frontmatter` duplicated at gates.py:168 vs the `re.MULTILINE` variant; `DeviationRegistry` (convergence.py:90) is the only typed sidecar and is scoped to one wrapper. Without a typed `PipelineEnvelope` dataclass at every handoff, every gate keeps trusting the same LLM that wrote the artifact. |
| 4 | Retry without input mutation + silent-skip default | PATCH-FIXABLE (retry-mutation half); INHERENT (silent-skip half) | **MIXED (agree with master)** | Retry-mutation: patch-fixable; v5 deviation-class injection partly closed it (master:§Remediation Taxonomy / Convergence-engine wrapper row). Silent-skip: INHERENT because it is encoded across dozens of policy decisions (`fidelity_checker.py:298 found=True`; `_cross_refs_resolve` warning-only return True at gates.py:88; `gate=None` at executor.py:2167; `validate` warn-not-fail at A4:F-A4-002/022; MEDIUM-non-blocking semantics). No single patch removes the policy without an explicit cross-cutting "loud rejection by default" inversion. |
| 5 | No cross-skill/cross-step contract schema or SoT authority | PATCH-FIXABLE per coupling; INHERENT for meta-flaw | **INHERENT (confirmed)** | No patch fixes this without introducing a **central contract registry module** (e.g. `superclaude.contracts`) that owns identifiers, threshold constants, gate names, return-contract schemas; today these live as duplicated literals across `commands.py`, `gates.py`, `prompts.py`, `obligation_scanner.py` imports from `vocabulary.py` (the *one* hoisted vocabulary, per A2a:F-A2a-003), and skill `.md` prose. The recurrence at (A10:F-A10-003) — release-split 0.7/0.5 vs sc:roadmap 0.6/0.5 thresholds — would be impossible if both imported from one constant. |

**Net:** 4 of 5 (Flaws 1, 2, 3, 5) and half of Flaw 4 (silent-skip) are inherent to the current design. Three of those four (Flaws 1, 3, 5) scope to *cross-cutting state*, which is precisely what makes incremental subsystem replacement insufficient (master:§Verdict). **INFERENTIAL:** my read of the code corroborates the master's REWRITE verdict — I see no architectural seam at which Flaw 1 or Flaw 3 could be replaced without touching the entire step-handoff surface.

---

### Q3 — Design alternatives, per inherent flaw, with prior-art comparison

#### Flaw 1 — Code-reaching terminal link

| Alternative | Prior art | What it buys you | Cost | Verdict |
|---|---|---|---|---|
| **A1a: Add a `code_assertion` field to `GateCriteria`** with a predicate `(artifact, repo_path) -> list[Finding]` invoked alongside `SemanticCheck`. Wire `build_certify_step()` to use it. | Pytest collection hooks; Bazel `genrule` providers; Buck2 rule providers. | Smallest delta: keeps markdown substrate, adds typed AST/import predicate slot. | Requires every gate author to opt-in; certify-as-LLM-step would remain orthogonal. | **Best minimal fix** — directly addresses the master's "no place to insert Link 3". |
| **A1b: Replace executor with LangGraph-style stateful graph** where each node returns a typed payload + side-effects, with an explicit "terminal verification" edge enforced by the graph schema. | LangGraph, Temporal, Inngest. | Forces every step to declare downstream consumers; makes "dead code" graph-theoretically impossible. | Full executor rewrite; loss of the simple `Step` + sequential executor abstraction in `pipeline.models`. | **Right architecture, wrong altitude** for an MVR. |
| **A1c: Dagster-style asset materialization model** where artifacts are typed `Asset`s with materialization checks; "code is callable" is just another asset check. | Dagster `@asset_check`; Prefect Result. | Code and markdown are first-class peers; certify becomes a normal asset check. | Large conceptual import for a CLI tool; Dagster requires a control plane. | Overshoots; useful as inspiration only. |

#### Flaw 2 — Generator/validator asymmetry

| Alternative | Prior art | What it buys you | Cost | Verdict |
|---|---|---|---|---|
| **A2a: Tool-use structured-output enforcement at every LLM step** (every `build_*_prompt` writes through a JSON-schema-validated tool call, like `MERGE_GATE` already does per A8:F-A8-015). | OpenAI/Anthropic structured-outputs; Instructor; Pydantic AI. | Generator can no longer fabricate IDs (Flaw 3 in master:§Top-3 #3) — the tool's JSON schema is the constraint. | Requires rewriting all 9 LLM step prompts; LLM may refuse-or-truncate under schema. | **Best leverage** — turns master:§Top-3 #3 "Roadmap fabricates IDs" from RECURRENT into structurally impossible. |
| **A2b: Generator-bound vocabulary/ID set passed as constraint** (extract step emits canonical `{FR, NFR, SC, D}` ID set; merge gate enforces `roadmap_ids ⊆ spec_ids ∪ accepted_deviations`). | Hugging Face `constrained_decoding`; GBNF grammars in `llama.cpp`. | Bidirectional registry kills phantom-ID class (master:§Top-3 #3, ~7 recurrences). | Requires shared registry module + decode-time enforcement (cloud LLMs lack token-level constraint). | Implementable as a *gate-time* check today; A2a + A2b together are complementary. |
| **A2c: FSM-style generator step typing** — each step declares pre/post invariants over the structured state, executor refuses transition unless invariants hold. | Akka FSM; Erlang `gen_statem`; XState. | Strong type-discipline on transitions; impossible to ship a frontmatter-key mismatch like (A11:F-A11-009). | Heavy framework cost vs Python's simple `Step` list. | Useful conceptual frame; implement as dataclass invariants, not full FSM. |

#### Flaw 3 — Markdown-frontmatter cross-step state

| Alternative | Prior art | What it buys you | Cost | Verdict |
|---|---|---|---|---|
| **A3a: Typed `PipelineEnvelope` dataclass + sidecar JSON** at every handoff; LLM still writes markdown, but a deterministic Python post-step extracts typed fields into the envelope and gates consume only the envelope. | Apache Beam `PCollection`; Kafka schema registry; Materialize record types. | Eliminates two-parser disagreement (A11:F-A11-010), eliminates LLM-self-reporting of gate-pass signals, makes counts queryable. | Need a deterministic markdown→typed extractor (this is the asymmetric-extractor problem the master surfaces in master:§Flaw 5 / (A12:F-A12-01)). | **Minimum required for rewrite.** The sidecar JSON IS the substrate inversion the master recommends. |
| **A3b: SQLite/embedded-DB cross-step state** with rich queries (run history, registry, threshold lookups, finding lineage). | Dagster's `DagsterInstance`; LangSmith trace store. | Cross-cutting queries become trivial; convergence + registry collapse into one store. | Operational complexity; debugging needs sql tooling vs `cat *.md`. | Overkill for solo CLI use; revisit if multi-release analytics become a goal. |
| **A3c: Actor-model in-memory state per release** (each step is an actor with typed mailboxes; markdown is render-only output, not the substrate). | Akka, Pony, Pykka. | State + concurrency model unified. | Wrong concurrency cost for a sequential pipeline. | Discard. |

#### Flaw 5 — No central contract registry

| Alternative | Prior art | What it buys you | Cost | Verdict |
|---|---|---|---|---|
| **A5a: `superclaude.contracts` module** — single source of truth for identifier patterns, threshold constants, gate field names, return-contract dataclasses; CI lint fails if any file defines a constant a contract exists for. | Python `Protocol` classes; `pydantic` model registries; Bazel `proto_library`. | The 17-flag mismatch (A9:F-A9-003) and 0.7/0.5 vs 0.6/0.5 drift (A10:F-A10-003) become CI errors. | Requires an arch-lint check (already partially exists via `make lint-architecture` per A3:F-A3-05). | **Best minimal fix.** |
| **A5b: Skill ↔ CLI bidirectional codegen** — generate both `commands.py` Click definitions and the `commands/*.md` skill prose from one YAML spec. | Cobra (Go), Click + `click-completion`; OpenAPI codegen. | Drift becomes mechanically impossible. | Heavier toolchain; templating cost. | Worth it long-term; not needed for minimum viable rewrite. |

---

### Q4 — Minimum viable rewrite architecture

The rewrite **preserves** what works — adversarial debate (master:§Verdict; A8 P3 pattern), the v3.05 deterministic structural-checker layer (`structural_checkers.py`), the convergence wrapper concept (`convergence.py`) — and **inverts the substrate** along four axes. The goal is the *smallest* delta that turns four of the five INHERENT flaws into structurally impossible failure shapes.

#### 1. State model — `PipelineEnvelope`

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

- Persisted as `.<release>/envelope.json`; every step reads the envelope, writes its artifact, and a *deterministic Python post-step* extracts canonical fields into the envelope. **LLM never writes gate-pass counts directly** — kills master:§Flaw 3.
- One `_parse_frontmatter` lives in the post-step extractor only; the two divergent variants at `gates.py:168` and `_check_frontmatter` are deleted.

#### 2. Gate contract — `GateCriteria` admits code-graph predicates

```python
@dataclass
class GateCriteria:
    required_envelope_fields: list[str]      # was: required_frontmatter_keys
    semantic_checks: list[SemanticCheck]     # (envelope) -> Finding | None
    code_assertions: list[CodeAssertion]     # NEW: (envelope, repo_path) -> Finding | None
```

- `CodeAssertion` instances import-and-call from `src/`, walk AST, check `step.id` appears in a dispatch map. The "is `build_certify_step()` actually wired?" question becomes a deterministic test the gate runs, not a post-hoc audit. **Kills master:§Flaw 1** by adding the missing slot.
- Wire `build_certify_step()` (currently executor.py:1899, unreached) as the final step; CodeAssertion guarantees no future step ships unwired.

#### 3. Generator-constraint mechanism — tool-write at every LLM step

- Every `build_*_prompt` in `prompts.py` is rewritten as a tool definition with a JSON schema. The LLM cannot return free-form markdown for the gate-relevant payload; only the tool's JSON output is consumed.
- The schema for `merge`, `generate-*`, and `remediate` includes a `roadmap_ids` array that MUST be a subset of `envelope.spec_ids ∪ envelope.accepted_deviations`. **Kills master:§Top-3 #3 (phantom IDs).** This is the generator-side constraint master:§Flaw 2 says is missing.
- Markdown artifacts are *rendered from* the tool output by a deterministic Jinja template. Markdown becomes a presentation layer, not an interchange substrate.

#### 4. Terminal verification link — Tasklist → AST

- New step `verify-implementation` runs after `tasklist` (or after `certify` in the roadmap-only path), with a `CodeAssertion`-only gate:
  - For each FR in `envelope.spec_ids[FR]`, the assertion either (a) finds an importable callable matching the spec's name binding, (b) finds it via `fidelity_checker`'s AST scan (`fidelity_checker.py:165-200`), or (c) matches an accepted deviation. No fail-open default (`fidelity_checker.py:287-303` `found=True` is deleted).
  - Failure produces a HIGH `Finding` and halts. **Kills master:§Flaw 1 evidence chain entirely** — wiring-verification's wrong-directory bug recurrence (A4:F-A4-004) becomes a unit test of the assertion, not an inline guard.

#### 5. Contract registry — `superclaude.contracts`

```python
# new: src/superclaude/contracts/__init__.py
ID_PATTERNS = {"FR": r"FR-\d+(?:\.\d+)?", "NFR": r"NFR-\d+", "SC": r"SC-\d+", "D": r"D-?\d+"}
CONVERGENCE_THRESHOLDS = {"sc:roadmap": (0.7, 0.5), "sc:release-split": (0.7, 0.5)}  # canonicalized
GATE_FIELD_NAMES = {"deviation_analysis": {"ambiguous": "ambiguous_deviations"}}  # one truth
RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}  # dataclass schema
```

- Arch-lint check (extension of existing `make lint-architecture` per A3:F-A3-05) fails CI if any module redefines a constant a contract owns. **Kills master:§Flaw 5** by collapsing dozens of coupling points.

#### Effort envelope (INFERENTIAL)

- `envelope.py` + post-step extractors: ~600 LOC new; deletes ~150 LOC of duplicate frontmatter parsing.
- `GateCriteria` extension + 14 step migrations: ~400 LOC delta.
- Tool-use rewrite for 9 LLM steps: largest chunk, ~1500 LOC across `prompts.py` (currently 85K) + new schema module.
- `superclaude.contracts` + arch-lint extensions: ~300 LOC.
- Net: ~2,800 LOC delta against ~8,200 LOC current pipeline core. Order-of-magnitude rewrite of the substrate without touching `commands.py` CLI surface or `superclaude.cli.pipeline.executor` orchestration kernel.

---

### Q5 — Brittleness-proof test/eval strategy

The current pipeline's brittleness is invisible in unit tests because every gate is `(content:str) -> bool` and unit tests pass curated content. The rewrite's correctness claim is *structural* ("no future failure shape can recur"), so the test strategy must verify the *absence of degrees of freedom*, not just the presence of correct outputs.

#### Regression-corpus seed cases

Build a fixture set keyed by the 16 failure classes in master:§Failure Taxonomy. Each fixture is a `(spec.md, roadmap.md_with_planted_defect, expected_finding)` triple. Minimum seed list (one per master class):

| Seed | Source class | Planted defect | Expected outcome |
|---|---|---|---|
| `seed-01-vacuous-pass-wrong-dir` | Gate Bypass | wiring runs against `.dev/releases/` markdown | HIGH `wrong_target` finding (was: silent PASS — A2b:F-A2b-002) |
| `seed-02-dead-code-certify` | Wired-but-Inert | `build_certify_step()` defined but not in `_build_steps()` | `CodeAssertion` failure at unit-test time (was: shipped — A11:F-A11-011) |
| `seed-03-byte0-preamble` | LLM-Output Format | extraction artifact has 1-line preamble before `---` | post-step extractor tolerates, envelope still valid (was: halt — A2a:F-A2a-001) |
| `seed-04-phantom-FR` | Spec→Roadmap Drift | roadmap names `FR-099` not in spec | tool-write rejects at generation; if forced, gate fails with `phantom_id` (was: shipped through merge — A1b:F-A1b-004) |
| `seed-05-Strategy-heading` | Anti-Instinct FP | section heading "## Testing Strategy" | Layer 5 demotion already in `obligation_scanner.py:137`; assert MEDIUM not HIGH (was: HIGH halt — A11:F-A11-002) |
| `seed-06-D1-vs-D01` | Asymmetric Extractor | spec `D1`, roadmap `D01` | canonicalizer matches; no phantom (was: 54 phantoms — A12:F-A12-01) |
| `seed-07-vacuous-skip` | Silent Skip | `_cross_refs_resolve` returns True with unresolved refs | gate now LOUD: unresolved emits HIGH (was: warning-only — A9:F-A9-005) |
| `seed-08-field-mismatch` | Severity Calibration | writer emits `ambiguous_count`, gate reads `ambiguous_deviations` | contract-registry CI lint fires *at commit time* (was: shipped pre-existing bug — A11:F-A11-009) |
| `seed-09-multi-vote-non-determinism` | LLM Non-Determinism | same spec, 5 runs | counts come from deterministic Python on envelope, NOT LLM; variance == 0 (was: 5 distinct counts — A4:F-A4-005) |
| `seed-10-impl-gap` | Spec-fidelity terminal | spec defines `FR-001 calls foo()`, no `foo` in `src/` | `verify-implementation` HIGH finding (was: shipped clean — A2b:F-A2b-004) |

#### Drift-detection harness

A nightly CI job that exercises **contract drift**, not feature regression:

1. **Schema diff.** Snapshot the JSON schema of every tool-write step. Any change to `roadmap_ids`, `convergence_score`, `ambiguous_deviations` requires explicit version bump + migration; bare schema delta fails CI. Catches the (A11:F-A11-009) field-name-rot class structurally.
2. **Registry-coverage check.** Walk all `*.py` and `commands/*.md`, regex for integer thresholds and identifier patterns; assert each match either (a) imports from `superclaude.contracts` or (b) is whitelisted. Catches (A10:F-A10-003) class.
3. **Dead-code call-graph check.** Static import graph over `executor.py`; assert every `build_*_step` function appears as a value in some `_build_steps()` branch. Catches (A11:F-A11-011) and (A10:F-A10-019) class.
4. **Frontmatter-parser uniqueness.** Static check: assert exactly one definition of `_parse_frontmatter` exists in the repo (currently two divergent ones). Catches (A11:F-A11-010).
5. **Vacuous-pass tripwire.** For every gate, assert `files_analyzed > 0` (or equivalent input-non-empty assertion) is in the gate's predicate or its caller. Catches the entire master:§Recurrence Matrix row #3 class.

#### End-to-end smoke contract

A single committed smoke pipeline that runs nightly on a *known-good* fixture (`tests/fixtures/smoke-spec.md` + `tests/fixtures/smoke-codebase/`):

- **Determinism gate.** Run twice; assert envelope JSON files are byte-identical except for `timestamp` fields. Variance > 0 fails the build. The 5-runs-4-counts incident (A4:F-A4-005) would have fired here on the first PR.
- **Terminal-link gate.** Smoke fixture's roadmap names `FR-001..FR-005` mapping to real callables in `tests/fixtures/smoke-codebase/`. `verify-implementation` MUST find all five via AST; planted-defect mutant (remove `foo`) MUST halt. Direct test of master:§Flaw 1 closure.
- **Generator-constraint gate.** Inject a prompt-perturbation that asks the LLM to invent `FR-099`; assert tool-write rejects (schema violation), pipeline halts before merge. Direct test of master:§Flaw 2 closure.
- **Loud-rejection gate.** Mutant fixture where `_cross_refs_resolve` would warning-only; assert pipeline now HALTS, exit code non-zero. Direct test of master:§Flaw 4 silent-skip closure.
- **Contract-registry gate.** Mutant `commands/sc/release-split.md` declaring threshold `0.6/0.5`; assert CI fails because `superclaude.contracts.CONVERGENCE_THRESHOLDS` is the SoT. Direct test of master:§Flaw 5 closure.

#### Coverage claim

If the 10 regression seeds + 5 drift checks + 5 smoke gates all pass on a release candidate, that release CANNOT exhibit any of the 22 recurrence-matrix failure classes in their structural form — the substrate inversion has removed the degree of freedom. **INFERENTIAL:** new failure *content* (new FP regex collisions, new generator hallucinations) is still possible; what is gone is the *class* — silent-skip cannot exist where the gate has no fail-open path, dead code cannot exist where call-graph CI enforces wiring, phantom IDs cannot exist where tool-write schemas constrain the namespace. That is the structural-brittleness-elimination claim the rewrite is meant to satisfy, and the test strategy above is what would prove it.

---

**Summary verdict (architecture vector):** Concur with master:§Verdict REWRITE. The five flaws are not coincident bugs; they are consequences of three substrate choices — markdown-as-interchange (Flaw 3), `(content:str)->bool` gate signature (Flaw 1), LLM-as-black-box-producer (Flaw 2) — coupled by the absence of a contract registry (Flaw 5). Patching individual instances has produced the documented 9→11→13→14 monotonic step growth without reducing the failure surface. The minimum viable rewrite above changes exactly those three substrates and adds the registry; the test strategy above is what would prove the rewrite eliminates the *class* of failure, not just specific instances.
