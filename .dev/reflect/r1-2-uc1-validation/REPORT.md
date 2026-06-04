# sc:reflect UC-1 Pre-Execution Audit — Phase 7 / R1.2 (PipelineEnvelope)

**Mode:** UC-1 (pre-execution coverage/gap audit)
**Tier reached:** 1 (pinned via `--tier 1`)
**Status:** success (with 3 minor recommended additions + 1 type-name ambiguity)
**Calibrated confidence:** 0.92
**Coverage_pct:** 0.92 (22/25 hard-covered, 2 minor partials, 1 ambiguity)
**Best-practice grade:** 4 / 5
**Generated:** 2026-06-01T18:58Z

## Inputs

- **Spec:** `.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md` (225 lines, sha256 `4782e56a`) — §R1.2 + §MVR §1 + §Contract embedded
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` (911 lines, sha256 `207b0f2a`) — Phase 7 at L472-500, Findings stub at L873
- **Phase 7 scope evaluated:** Steps 7.1 / 7.2 / 7.3 / 7.4 + Phase Gates PG7.1 / PG7.2 (lines 476-500)
- **Worktree-of-execution sanity-check:** `/config/workspace/IronClaude-RoadmapRewrite/` HEAD `daa10416` on `refactor/roadmap-pipeline-r0-r1-rewrite`; R0.1 (`id_registry.py`) and R1.1 (`contracts/__init__.py`) deliverables verified; `envelope.py` not yet present (confirms Phase 7 hasn't started).

## Coverage Matrix — §MVR §1 + §R1.2 → Phase 7 Tasklist

| # | Spec requirement | Source | Tasklist coverage | Verdict |
|---|---|---|---|---|
| 1 | New `src/superclaude/cli/roadmap/envelope.py` | §MVR §1 | Step 7.2 (L482) | ✓ |
| 2 | `@dataclass(frozen=True) class PipelineEnvelope` | §MVR §1 | Step 7.2 verbatim | ✓ |
| 3 | Field `release_id: str` | §MVR §1 | Step 7.2 | ✓ |
| 4 | Field `spec_hash: str` | §MVR §1 | Step 7.2 | ✓ |
| 5 | Field `spec_ids: SpecIdRegistry` | §MVR §1 | Step 7.2 + R0.1 absorption | ✓ |
| 6 | Field `artifacts: dict[StepId, ArtifactRef]` | §MVR §1 | Step 7.2 (typed as `dict[str, ArtifactRef]`) | ✓ (mild typing nuance) |
| 7 | Field `findings: list[Finding]` | §MVR §1 | Step 7.2 | ✓ |
| 8 | Field `counts: dict[str, int]` | §MVR §1 | Step 7.2 + Flaw 3 invariant | ✓ |
| 9 | Field `convergence: ConvergenceState \| None` | §MVR §1 | Step 7.2 says "comes from RunMetadata/ConvergenceResult" | ⚠ TYPE-NAME AMBIGUITY |
| 10 | Field `accepted_deviations: list[AcceptedDeviation]` | §MVR §1 | Step 7.2 | ✓ |
| 11 | Persisted as `.<release>/envelope.json` | §MVR §1 | Step 7.1 (design) + Step 7.2 | ✓ |
| 12 | Atomic write (tmpfile + rename) | engineering best-practice | Step 7.2 explicit | ✓ |
| 13 | "every step reads envelope, writes artifact, post-step extracts" | §MVR §1 | Step 7.3 + executor wiring | ✓ |
| 14 | "LLM never writes gate-pass counts directly" | §MVR §1 (Flaw 3 invariant) | Step 7.2 docstring + Step 7.3 design | ✓ |
| 15 | Kills master:§Flaw 3 | §MVR §1 | Step 7.2 docstring cites Flaw 3 | ✓ |
| 16 | Dual-write envelope + markdown for 1 release cycle | §R1.2 | Steps 7.1 / 7.3 / 7.4 + PG7.1 (f) | ✓ |
| 17 | Markdown render-only after cutover | §R1.2 + §MVR §1 | Phase 11 (R1.6) — explicitly deferred | ✓ |
| 18 | Absorb R0.1 `spec_id_registry.json` into `envelope.spec_ids` | §R1.2 sequencing | Step 7.1 plan + Step 7.2 TODO marker | ✓ |
| 19 | Frontmatter/parser consistency (Contract #6) | §Contract | Step 7.3 "do NOT add new parsers" | ✓ |
| 20 | No new `return True` stubs (Contract #5) | §Contract | PG7.1 (g) | ✓ |
| 21 | PRESERVE `convergence.py` public API | §MVR + preserves list | PG7.1 (c) | ✓ |
| 22 | PRESERVE `commands.py` | §MVR §6.3 + CLAUDE.md | PG7.1 (d) | ✓ |
| 23 | PRESERVE `structural_checkers.py` (v3.05 layer) | preserves list (frontmatter L67-70) | not in PG7.1 audit | ⚠ MINOR GAP |
| 24 | Dispatch-reachability for `POST_EXTRACTORS` (Contract #2 spirit) | §Contract #2 | Step 7.4 covers completeness; reachability test absent | ⚠ MODERATE GAP |
| 25 | Field-set drift test (envelope vs §MVR §1) | parallel to R1.1 OQ-1 | not explicit | ⚠ MINOR GAP |

**Hard-covered:** 22/25. **Partial / gap:** 3. **Coverage_pct:** 0.92.

## Unmapped Requirements (none — all §R1.2 mandates trace to a tasklist step)

There are no §R1.2 / §MVR §1 mandates that the tasklist drops entirely. Every requirement either lands in Phase 7 directly or is explicitly deferred to a later phase (R1.6 markdown render-only → Phase 11).

## Gaps + Recommended Additions

### G1 — MODERATE: Dispatch-reachability test missing for `POST_EXTRACTORS`

**What's required:** §Contract item #2 (BUILD-REQUEST L58): *"If the fix adds a new builder, runner, gate, or hook symbol, a test MUST assert the symbol is reachable from a production entry point (`_build_steps()`, `execute_sprint()`, `run_portify()`, `execute_pipeline()`). Mechanism: AST walk + dispatch-graph trace."*

**What the tasklist covers:** Step 7.4 (tasklist L490) requires a test for *"dispatch map completeness (every step in `_build_steps` has an entry)."* This is **map-completeness**, not **reachability from a production entry point**.

**Why it matters:** The POST_EXTRACTORS dispatch map IS a new dispatch mechanism per Contract #2. A future contributor could add an extractor that is never called by `executor.roadmap_run_step` and the map-completeness test would still pass. The Contract #2 "AST walk + dispatch-graph trace" is the right mechanism to catch this.

**Recommended addition:** Insert a sub-bullet in Step 7.4: *"Add a dispatch-reachability test that asserts `POST_EXTRACTORS[step_id]` is invoked from `executor.roadmap_run_step` for every step in `_build_steps()` — AST walk per Contract #2."*

### G2 — MINOR: `structural_checkers.py` not in PG7.1 PRESERVE audit

**What's required:** Tasklist frontmatter (L67-70) lists *preserves* including *v3.05-deterministic-structural-checker-layer*. R1.1 phase-6 closure (L862) confirms `structural_checkers.py` was empty-diff-verified at parent `1c56b50f`.

**What the tasklist covers:** PG7.1 (c) asserts `convergence.py` unchanged; PG7.1 (d) asserts `commands.py` unchanged. **No assertion on `structural_checkers.py`.**

**Why it matters:** R1.2 introduces post-extractors that parse step artifacts. `structural_checkers.py` is a candidate "look-alike" file an over-eager refactor could touch (since both deal with deterministic Python parsing of pipeline outputs). The PRESERVE invariant should be explicitly audited.

**Recommended addition:** Add to PG7.1 verification list: *"(h) `src/superclaude/cli/roadmap/structural_checkers.py` public API unchanged vs parent `daa10416` (v3.05 deterministic-structural-checker-layer per BUILD-REQUEST preserves list)."*

### G3 — MINOR: Field-set drift test (parallel to R1.1 OQ-1)

**What's required:** Phase 6 closure (L868) flagged OQ-1: *"`test_adversarial_return_fields_match_skill_prose` uses set equality on field names; does not catch type drift."* The same shape applies to PipelineEnvelope — a future contributor adding a field to `PipelineEnvelope` outside §MVR §1 should be caught by a test that compares the dataclass `dataclasses.fields()` against the §MVR §1 canonical list.

**What the tasklist covers:** PG7.1 (a) checks "matches §MVR §1 verbatim" via human rf-qa review. **No automated field-set drift test.**

**Recommended addition:** Insert into Step 7.4 test list: *"Field-set conformance test: `set(f.name for f in dataclasses.fields(PipelineEnvelope)) == {'release_id', 'spec_hash', 'spec_ids', 'artifacts', 'findings', 'counts', 'convergence', 'accepted_deviations'}`."*

### A1 — TYPE-NAME AMBIGUITY: `ConvergenceState` does not exist as a class

**What §MVR §1 says (BUILD-REQUEST L97):** `convergence: ConvergenceState | None`.

**What the codebase has** (`/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/convergence.py`, verified at HEAD `daa10416`):
- `class RunMetadata` (L75)
- `class DeviationRegistry` (L91)
- `class ConvergenceResult` (L321)
- `class RegressionResult` (L334)

**What the tasklist Step 7.2 says (L482):** *"`ConvergenceState` import comes from the existing `convergence.RunMetadata`/`ConvergenceResult` types, do NOT redefine."*

**The ambiguity:** Step 7.2 names two candidate types without picking one. `RunMetadata` is per-run metadata (orthogonal to convergence). `ConvergenceResult` is the terminal convergence verdict. Which is the envelope's `convergence` field?

**Recommended resolution before Step 7.2 begins:** Decide explicitly — most likely `convergence: ConvergenceResult | None` (the terminal convergence state, populated post-convergence step; None when convergence step has not yet run). Document the choice in the Step 7.1 design doc (`r1-2-envelope-design.md`) with a 1-line rationale, so PG7.1 (a) "matches §MVR §1 verbatim" can be evaluated against an explicit type binding rather than the literal §MVR string.

**Severity:** ambiguity, not error. Either choice can be made to work, but it should be made once in Step 7.1 (design) and audited once in PG7.1, not deferred to Step 7.2 implementation choices.

## Risk-Surface Notes (non-blocking)

- **File:line drift across worktrees.** Tasklist Step 7.3 cites `executor.roadmap_run_step (L955)`; the function is at **L1021** in RoadmapRewrite HEAD `daa10416` (R0.1 + R1.1 added LOC above it). Step 7.3 implementer should re-grep by function name (`grep -n "^def roadmap_run_step"`), not trust the cited line. The tasklist's "REMEMBER" sections don't call this out — recommend adding a generic "verify line numbers by function name first" note to Phase 7 preamble.
- **OQ-2 from Phase 6** (tuple vs list serialization) directly applies to envelope JSON round-trip. Step 7.4's "round-trip (save→load equality)" test will catch this if fixtures cover both list-valued and dict-valued fields; recommend explicit assertion that `list[Finding]` and `list[AcceptedDeviation]` survive serialize→deserialize as lists (not tuples).
- **R0.1 absorption mechanics.** Step 7.2 marks a TODO for R1.6 deletion of `spec_id_registry.json`; the dual-write phase still produces both `spec_id_registry.json` (R0.1) AND `envelope.json` (R1.2). Step 7.3 should confirm R0.1's sidecar continues to be written during dual-write so existing R0.1 consumers (`gates.py` merge gate) don't break.

## Decision: Proceed with R1.2 (with 3 small additions)

**Strengths of the tasklist for Phase 7:**

1. All 8 §MVR §1 fields enumerated verbatim in Step 7.2.
2. Dual-write strategy is explicit (Step 7.1 design + PG7.1 (f) diff-check).
3. Master:§Flaw 3 invariant ("LLM never writes counts directly") is cited at three points (Step 7.2 docstring, Step 7.3 dispatch design, PG7.1 (a)).
4. PRESERVE invariants for `convergence.py` and `commands.py` are explicit gate items.
5. R0.1 → R1.2 absorption sequencing is explicit and reversible (TODO marker rather than deletion).
6. Atomic write requirement is explicit (Step 7.2).
7. rf-qa task-integrity ADVERSARIAL STANCE invocation (PG7.1) mirrors the Phase 6 pattern that landed clean.

**Required adjustments before executing Phase 7** (light edits, no scope change):

| # | Adjustment | Step affected | Effort |
|---|---|---|---|
| 1 | Resolve `ConvergenceState` type-name to `ConvergenceResult` (or whichever) in Step 7.1 design doc | Step 7.1 | 1 sentence in design doc |
| 2 | Add POST_EXTRACTORS dispatch-reachability test (Contract #2) | Step 7.4 | 1 test function (~30 LOC) |
| 3 | Add `structural_checkers.py` PRESERVE audit | PG7.1 | 1 new sub-bullet (h) |
| 4 | Add field-set drift test | Step 7.4 | 1 test function (~10 LOC) |
| 5 | Add re-grep guidance to Phase 7 preamble | Phase 7 header | 1 sentence note |

None of these block Phase 7 from starting. All can be applied as a single small tasklist edit before the first Step 7.1 spawn, or absorbed into Step 7.4 / PG7.1 by the executor during implementation.

## Grounding Gaps

None. Every claim in this report is backed by either a verified `file:line` re-Read in the spec/tasklist/source files, or by an explicit type-name absence verified against the on-disk `convergence.py` at HEAD `daa10416`.

## Citations

- BUILD-REQUEST §R1.2: `BUILD-REQUEST-roadmap-pipeline-rewrite.md:170`
- BUILD-REQUEST §MVR §1 (PipelineEnvelope shape): `BUILD-REQUEST-roadmap-pipeline-rewrite.md:84-103`
- BUILD-REQUEST §Contract #2 (dispatch-reachability): `BUILD-REQUEST-roadmap-pipeline-rewrite.md:58`
- BUILD-REQUEST §Contract #5 (no `return True` stubs): `BUILD-REQUEST-roadmap-pipeline-rewrite.md:64`
- BUILD-REQUEST §Contract #6 (parser consistency): `BUILD-REQUEST-roadmap-pipeline-rewrite.md:66`
- Tasklist frontmatter preserves list: `TASK-RF-20260531-042405.md:67-70`
- Tasklist Step 7.1: `TASK-RF-20260531-042405.md:476-478`
- Tasklist Step 7.2: `TASK-RF-20260531-042405.md:480-482`
- Tasklist Step 7.3: `TASK-RF-20260531-042405.md:484-486`
- Tasklist Step 7.4: `TASK-RF-20260531-042405.md:488-490`
- Tasklist PG7.1: `TASK-RF-20260531-042405.md:494-496`
- Tasklist PG7.2: `TASK-RF-20260531-042405.md:498-500`
- Phase 6 closure / OQ-1 / OQ-2: `TASK-RF-20260531-042405.md:847-871`
- `convergence.py` class list (no `ConvergenceState`): `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/convergence.py:75, 91, 321, 334`
- `executor.roadmap_run_step` actual line in RoadmapRewrite: `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:1021`
