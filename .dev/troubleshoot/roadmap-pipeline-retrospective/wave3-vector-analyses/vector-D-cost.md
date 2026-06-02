# Vector D — Token-Economics Analysis

**Role:** Token-economics engineer
**Source:** wave2-master-report/master-report.md + observable runtime telemetry + `.dev/releases/complete/` artifact corpus (247 MB, 6,052 files, 4,450 markdown)
**Stance:** Cost-driven. Where does token spend disappear? Where would $X of prevention save $Y of cure?

---

## Stage-cost baseline (working model)

To rank failure costs, I anchor on the observed wall-clock runtimes (user-provided) and convert to token-spend bands using Anthropic's stable rule-of-thumb (~30-60 tokens/sec sustained for Claude-CLI subprocess in `_embed_inputs` mode, weighted by input size). The master report does not publish raw token counts per step, so the bands below are **INFERENTIAL** but conservative — calibrated against the v2.13 `_embed_inputs()` shift (master:Pipeline-step #18) which forced all inputs inline.

| Stage | Wall-clock | Inferred token band (input+output) | Cost rank |
|---|---|---|---|
| extract | ~210 s | 15-30 K | LOW |
| generate-opus-architect | ~780 s | 80-150 K | **HIGHEST** |
| generate-sonnet-architect | ~1,320 s | 100-200 K (retry instability per master:Heat-Map row "generate-sonnet" MED) | **HIGHEST** |
| merge | ~500 s | 60-120 K | HIGH |
| debate | ~110 s | 20-40 K | MED |
| score | ~60 s | 8-15 K | LOW |
| **Single full roadmap run** | **~50 min** | **~285-555 K** | — |

Two architect passes + merge dominate (~80% of cost). Any failure that re-runs generate-opus or generate-sonnet pays ~80-200 K per recurrence; failures that only re-run debate/score pay ~30-55 K.

---

### Q1. Re-run cost ranking

The failure modes that drive the most expensive re-runs are the ones whose detection lives **downstream** of the architect stages — because the architect output is the contaminated input every retry feeds back through. The master report's "harden-orchestration-around-broken-comparator" finding (master:§Recurrence-Matrix row 1; A12:F-A12-03) is the cost signature of this asymmetry.

| Failure (cite) | Stage(s) re-run on recurrence | Est. tokens per recurrence | Frequency (master evidence) |
|---|---|---|---|
| **Spec-fidelity LLM non-determinism** (master:§Recurrence row 1; A4:F-A4-005 — 5 runs / 4 distinct counts on identical input) | spec-fidelity ×5 (5-vote consensus), and on Run 4 the roadmap was regenerated from scratch → generate-opus + generate-sonnet + merge | **5-vote case: ~75-100 K** (5 × spec-fidelity); **regen case: ~400-500 K** (full re-architect) | ~12 attempts across 8 partitions (master:§Recurrence row 1) |
| **Anti-instinct false-positives halt entire downstream pipeline** (master:§Hot-spot #2; A11:F-A11-001 — every TDD/PRD-enriched run halted) | anti-instinct typically halts → operator either edits roadmap (~30 K spec-fidelity re-run) **or** re-runs from generate to fix vocabulary (~285-555 K full pipeline) | **Edit path: ~30-50 K**; **regen path: ~300-500 K** | ~7 findings across 4 partitions; 4 of 4 enriched-prompt matrix cells FAILED (A11:F-A11-001) |
| **Retry without input mutation** (master:§Flaw-4; A1b:F-A1b-006 — 2-attempt budget burned on identical outputs) | The retried stage (spec-fidelity, remediate, debate) is debited per retry while producing identical work | **Each futile retry burns full stage cost** with zero progress: spec-fidelity ~15-25 K × N; remediate (LLM patch) ~40-80 K × N | ~8 findings across 5 partitions (master:§Failure Tax "Retry/Convergence Logic Without Input Mutation") |
| **Roadmap fabricates/renumbers identifiers** (master:§Recurrence row 4; A1b:F-A1b-004 — FR-001..FR-032 invented) | spec-fidelity flags HIGH → remediate (LLM patch ~50 K) → spec-fidelity re-runs (~20 K) → on failure-to-converge, regenerate from architect | **Best case: ~70-100 K** (remediate + re-fidelity); **worst: ~400-500 K** full regen | ~7 attempts; every release with >5 reqs (master:§Failure-Tax) |
| **Merge drops ~10-15% adversarial findings silently** (master:§Hot-spot #3; A9:F-A9-011) | If detected late by downstream gate, debate is re-run (~30-40 K) and merge re-run (~60-120 K) | **~100-160 K** when detected; typically undetected → ships as latent defect | ~1 finding per release that uses adversarial debate (master:Recurrence row 15) |
| **Wiring-verification scans wrong directory, vacuous PASS** (master:§Recurrence row 3; A4:F-A4-004) | When detected post-release, full re-run of wiring-verification + downstream remediate (~80-120 K) — but typically caught only by post-hoc gap analysis (master:§Flaw-1 cost note) | **In-release: ~80-120 K**; **post-release gap-analysis: ~200-500 K** (entire QA reflection cycle) | ~5 across 4 partitions; recurred across 3 releases before guard landed (master:Hot-Map "wiring-verification") |
| **Frontmatter / preamble parser brittleness** (master:§Failure-Tax "LLM-Output Format Brittleness"; A2a:F-A2a-001 — 1-line preamble halted extract) | Halts at extract; operator strips preamble + re-extracts; if extract output corrupted, re-runs cascade into generate | **Best: ~15-30 K** (re-extract); **cascade: ~150-300 K** if generators re-run | ~10 findings; compound-reliability 0.9⁸ = 43% (master:§Failure-Tax citation A2a:F-A2a-001) |
| **Anti-instinct retry-on-identical-input** (master:§Flaw-4; A12:F-A12-02 — D-family flatline 58→54→54 over 3 runs) | Convergence loop re-runs spec-fidelity + remediate per attempt with no input mutation | **Per loop: ~60-100 K** burned before binary halt | TurnLedger budget exhaustion misread as success (A12:F-A12-02) — operator misdiagnosis amplifies cost |

**Top-3 cost drivers by frequency × per-recurrence cost:**

1. **Spec-fidelity LLM non-determinism** — 12 recurrences × ~75 K avg (5-vote) = **~900 K cumulative**, with worst-case 5 M+ if regeneration triggered. Cost dominates because the recurrence count is highest *and* the 5-vote workaround multiplies per-attempt cost by 5×.
2. **Anti-instinct false-positives** — 7 recurrences × ~200 K (mix of edit and regen) = **~1.4 M cumulative**. The "all 4 enriched matrix cells fail" finding (A11:F-A11-001) tells us this is *the* terminal halt for the dominant input mode (TDD+PRD).
3. **Retry without input mutation** — multiplier on every other failure mode; not standalone but compounds (1) and (2). Master:§Flaw-4 names the v2.24-cli-portify halt as the single incident that drove the entire v5 redesign (A1b:F-A1b-006) — a re-architecture cost of dozens of MTok.

---

### Q2. Dead-output sunk cost

`/config/workspace/IronClaude/.dev/releases/complete/` totals **247 MB across 6,052 files (4,450 markdown)** spanning ~64 release directories. Inferential token-mapping using a conservative 250 tokens/KB for prose markdown (rich tables/frontmatter increase density) and excluding `.git`-style metadata:

| Bucket | Volume | Inferred token cost | Notes |
|---|---|---|---|
| **cliEval/** | 70 MB / 1,005 files | ~17.5 M tokens | Largest single sink. Master:§Failure-Tax / A6:F-A6-008 cites 20 deviations all resolved as NO_ACTION (100% manual-triage); A6:F-A6-013 cites `.roadmap-state.json` `fidelity_status: pass` coexisting with `validation.status: fail`. This entire directory represents an evaluation harness whose findings were rejected at triage — **essentially 100% sunk cost** with reuse only as retrospective evidence. |
| **Spec-fidelity artifacts** | 24 files (across releases) | ~250-500 K | These exist because the gate halted then re-ran (master:§Recurrence row 1: ~12 attempts). Each `spec-fidelity.md` ≈ 10-20 K tokens; multi-version copies (v2.23/, v2.24/, v2.24.1/ each have one) are evidence of retry-without-mutation. |
| **Debate transcripts / adversarial dirs** | 179 files | ~3-5 M tokens | Adversarial debate (master:§Pattern P3) genuinely works — but 179 files implies many were superseded or run multiple times. Master:Heat-Map "debate" cites 0.72 convergence shipped as PASS in v2.13/v2.20 (A9:F-A9-007) → those transcripts ship as advisory-only and are de-facto sunk. |
| **Wiring-verification artifacts** | 22 files | ~150-300 K | Master:§Recurrence row 3 — gate scanned wrong dir, vacuous PASS, then re-ran. Multi-version artifacts in v3.05/, v3.1/, v3.2/, unified-audit-gating-v1.2.1/ represent the same failure shape re-emitted. |
| **Architecture-superior accepted-deviation side-channels** | `dev-001-accepted-deviation.md` appears in both `v2.24/` and `v2.24-cli-portify-cli-v4/` (28 KB each, master:A7:F-A7-05) | ~15-30 K | These are *productive* outputs (humans hand-wrote them) but the *cost* of producing them was avoidable had an allowlist mechanism existed. |
| **Largest superseded releases** (v3.05 7.0 MB / v3.1 6.4 MB / v3.2 / v2.26-roadmap-v5 7.1 MB) | ~25-30 MB combined | ~6-7 M tokens | Each represents a full pipeline arc whose *underlying conclusions* were superseded by the next release (master:§Flaw-2: "pipeline step count grows monotonically v4=9→11→13→14"). Strictly: superseded ≠ dead, but the *re-architecture cost* the next release paid means most of the older artifacts are no longer load-bearing. |

**Sunk-cost estimate (total):** Of the ~247 MB / ~60-70 M-token corpus, I estimate **~25-30 M tokens represent dead-output sunk cost** — work whose conclusions were superseded, manually triaged to NO_ACTION, or were artifact-of-failure rather than artifact-of-progress. cliEval alone is **~17.5 M of that** (1,005 files / 100% NO_ACTION resolution per A6:F-A6-008). At ~$3-15/M tokens depending on model mix, the lower-bound dollar floor is **~$75-450 of generation cost for cliEval alone** — the upper bound on the full superseded corpus is substantially higher when retry/regenerate cycles are included. INFERENTIAL: I have no direct token-cost telemetry; this is order-of-magnitude.

---

### Q3. Early-failure detection ROI

Ranked by **expected value = (per-recurrence token cost saved) × (failure frequency)**. I take the top three intervention points where a cheap pre-flight check (<1 K tokens, fully deterministic) would prevent burning ~80-500 K per failure.

**1. Pre-architect: bidirectional spec-ID registry preflight (EV: ~6-10 M tokens saved across lifecycle)**

- **Trigger:** Before invoking `generate-opus-architect` (~780 s / 80-150 K), parse the spec to build a canonical ID set (FR/NFR/SC/D/IC). Inject this set into the generator's tool-write template as a hard constraint ("you MUST use only IDs from this set, except as DEV-### deviations").
- **Cost:** ~500 tokens to construct the registry; near-zero runtime overhead (Python set).
- **Saves:** Master:§Recurrence row 4 cites ~7 attempts across 6 partitions to remediate fabricated IDs. Each remediation cost ~70-100 K (spec-fidelity + remediate cycle) or up to ~400-500 K when regeneration triggered. EV: **7 × ~150 K = ~1 M tokens per release lifecycle**, scaling with retroactive prevention across the 12 in-flight pipelines that still ship fabricated IDs.
- **Maps to Flaw 2** (master:§Flaw-2) — generator-side constraints absent.

**2. Pre-anti-instinct: vocabulary-collision lint with allowlist (EV: ~3-5 M tokens saved across lifecycle)**

- **Trigger:** Before invoking the anti-instinct gate (the current terminal halt for every TDD+PRD enriched run per A11:F-A11-001), run a 50-line Python lint that flags `\bStrategy\b` matches against section-heading regex, `\bhardcoded\b` matches against parenthetical descriptors, and "scaffold" matches against verb-vs-noun POS context. Emit WARNINGs not BLOCKERs.
- **Cost:** ~200-500 tokens (lint runs locally, no LLM call).
- **Saves:** Master:§Hot-spot #2 — anti-instinct is the highest-frequency *terminal* halt. Each halt either burns ~30-50 K (operator edit) or ~300-500 K (full regen). EV at observed 4-of-4 cell halt rate × ~200 K avg = **~800 K per affected run × ~7+ recurrences = ~5 M+ cumulative**.
- **Maps to Flaw 4** (master:§Flaw-4 silent-skip half) — currently no warning escape valve exists; this intervention adds the "ALLOW-warnings" gate the spec explicitly omits.

**3. Pre-merge: cross-step contract schema validator (EV: ~2-4 M tokens saved across lifecycle)**

- **Trigger:** Before invoking `merge` (~500 s / 60-120 K), validate that adversarial-debate output fields = merge-input fields (Pydantic-style schema). Halt with explicit field-name diff if mismatch.
- **Cost:** ~100-300 tokens (deterministic schema compare).
- **Saves:** Master:§Recurrence row 15 cites ~10-15% adversarial findings drop silently. When this is caught downstream, it triggers re-debate + re-merge (~100-160 K). When uncaught, it ships as latent defect (master:§Flaw-5; A10:F-A10-004 — 4 of 9 fields consumed). EV: **~15% × ~130 K × every merge run** = ~20 K per merge avg × ~50 lifecycle runs = ~1 M direct; latent-defect amplification likely 2-4×.
- **Maps to Flaw 5** (master:§Flaw-5) — missing contract-schema layer.

**Honourable mentions (lower EV but cheap to add):**

- **Pre-extract preamble sanitizer at byte-0** (master:Heat-Map "extract" HIGH; A2a:F-A2a-001): a 5-line regex strip costs ~50 tokens, saves the 0.9⁸ = 43% compound-failure surface and the ~15-30 K of re-extract per occurrence. Already partially landed per master:Hot-Map but the byte-0 parser still co-exists with the MULTILINE one (master:Heat-Map "extract" cites A11:F-A11-010).
- **Pre-flight TurnLedger budget vs. expected work-units** (master:§Flaw-4 silent-skip; A12:F-A12-02): a 20-line check that emits "STRUCTURAL_DEFECT_SUSPECTED" instead of generic "budget exhausted" would prevent the operator misdiagnosis tax — not directly token-saving but prevents the wrong-direction work that follows.

---

### Q4. Input-size sensitivity

The master report contains explicit evidence that brittleness disproportionately affects **larger / enriched input sizes**. Cross-referencing failure data with input-size data:

**Direct evidence (load-bearing citation):**

- **A11:F-A11-001 — "Every TDD/PRD enriched pipeline halts."** All 4 cells of the input matrix FAIL: TDD-only, TDD+PRD, Spec-only, Spec+PRD. The enriched (TDD+PRD) cell shows the worst gate-counter profile (1 undischarged + 4 uncovered + 0.73 coverage), and master:Heat-Map "anti-instinct" labels this HIGH-risk explicitly because the 0.7 threshold drops as input complexity introduces synonym dilution (AUTH_SERVICE_ENABLED, RBAC, CSRF substitute for technical identifiers).
- **A11:F-A11-005 — "4.1× richer TDD+PRD input produces 49% FEWER actionable tasks (44 vs 87)."** This is the canonical input-size brittleness fingerprint: as input *grows*, output *contracts* because the extraction destroys tabular granularity. Master:§Failure-Tax "Cross-Phase Contract & Phase Restructuring Drift" classifies this as MEDIUM-HIGH severity.
- **A11:F-A11-007 — "one-shot stdout capture hits 64k-token fallback cap with no truncation detection."** Larger inputs → more likely to hit the 64K cap → silent truncation → downstream gates pass on incomplete output. Maps to master:Heat-Map "generate-opus-architect" MED risk.
- **A11:F-A11-016 — "TDD+PRD haiku-architect needed 2 attempts where the other 3 runs needed 1 — model-capacity ceiling under enriched-prompt sizes."** Direct citation: enriched prompts induce retry instability.
- **A1b:F-A1b-005 — "Context-window overflow caused Phase 7 ID drift (D-0042..D-0050 instead of D-0035..D-0043)."** v2.22 — large generation triggered ID renumbering silently. Maps to master:§Flaw-2.

**Inferential evidence:**

- The **MultiModelSwarm roadmap** (the user's currently-blocking failure cited in master:§Executive-Summary) is a 14-step pipeline spec — substantially larger than typical specs. The fact that the anti-instinct halt fires on `stub`-as-component-name false positives at lines 207/211/213 is consistent with larger specs introducing more vocabulary surface for regex collisions. **INFERENTIAL** but well-supported by A11:F-A11-002 (more headings → more "Testing Strategy" / "Migration Strategy" matches).
- **TUIBBS v1-MVP** (A12:F-A12-01) — 54 phantom_id HIGHs because the spec had only 3 D-IDs (D1/D3/D5) while the roadmap had 54 (D01..D54). The mismatch is proportional to roadmap size — larger roadmaps → more phantom IDs by linear expansion.

**Counter-evidence:**

- A2a (small specs, single-page extract failures) still hit byte-0 preamble bugs. Format-brittleness affects all sizes; *semantic*-brittleness (anti-instinct, fidelity drift) affects large sizes disproportionately.

**Conclusion:** Brittleness has two regimes. **Format brittleness** (extract preamble, frontmatter) is size-invariant. **Semantic / structural brittleness** (anti-instinct false positives, ID fabrication, phase restructuring, task-count regression) **scales superlinearly with input richness** — bigger inputs hit the gates harder because each gate's vocabulary surface grows with input vocabulary. The MultiModelSwarm halt is a *predictable* instance of this scaling.

---

### Q5. Cost-effectiveness ranking of rewrite alternatives

Vector A's published alternatives are not available at read-time (`wave3-vector-analyses/` is empty). Per the instructions, I reason from master:§Flaw-1 through §Flaw-5 and propose 4 representative architectural alternatives, ranked by **build cost vs steady-state operating cost**. Build-cost band uses engineer-weeks × spend per week as proxy; operating-cost band uses incremental token spend per pipeline run.

| Alt | Description | Build cost | Steady-state op cost | Risk | Rank |
|---|---|---|---|---|---|
| **R1: Tool-write structured-output enforcement at every LLM step + typed sidecar JSON state** | Replace markdown-frontmatter state (master:§Flaw-3) with dataclass + sidecar JSON; every LLM step writes via `tool_use` into a Pydantic-validated template. Generator-side constraints landed mechanically. | **HIGH** (~6-10 eng-weeks; rewrites `_embed_inputs` substrate, every step's `build_*_prompt`, every gate's frontmatter reader) | **LOW** — once landed, tokens per step DROP because preamble brittleness disappears (no re-extract cycles), spec-fidelity gates run on structured data not parsed markdown (no 5-vote consensus needed). Estimated savings: ~30-50% per run vs current. | LOW (architecturally well-understood; structured output is a mature pattern) | **#1 best EV** |
| **R2: Add Tasklist→AST terminal fidelity link (close Link 3)** | Implement the missing code-reaching gate from master:§Flaw-1 — import every tasklist-declared callable, signature-check it, smoke-run it against minimal fixtures. Run as Step 13/14. | **MED** (~3-4 eng-weeks; AST utilities + smoke-fixture harness) | **LOW-MED** — adds ~30-60 s + ~5-10 K tokens per run; saves ~30-50% of remediation token spend per master:§Flaw-1 cost-note (gap-analysis cycles to find CRITICAL bugs that validators marked CLEAN). | LOW (AST checks are deterministic) | **#2** |
| **R3: Central contract registry with bidirectional drift detection in CI** | One source-of-truth module exporting IDs, gate names, thresholds, return-contract shapes. CI step that diffs SKILL.md vs CLI `--help` vs prompt strings vs gate consumers. | **MED** (~4-5 eng-weeks; registry module + CI workflow + diff tooling) | **VERY LOW** — runs in CI only; saves ~17-flag-mismatch class of failures (master:A9:F-A9-003) entirely. Steady-state cost ~0 tokens per run. | LOW (well-established CI pattern) | **#3** |
| **R4: Replace anti-instinct regex with LLM+structural-context analyzer** | Master:§Flaw-2; A2b:F-A2b-006 / V3 coherence-graph and V5 mechanism-taxonomy variants were merge-rejected on cost. Reintroduce one of them — pay LLM call cost on every run in exchange for eliminating false-positive halt class. | **MED-HIGH** (~5-7 eng-weeks; one of the merged-rejected variants resurrected + integration) | **HIGH** — adds 1 LLM call per run (~30-60 K tokens). Saves ~1.4 M cumulative anti-instinct false-positive cost (Q1) but adds ~30 K × every run = ~1.5 M+ over lifecycle. **Roughly break-even on tokens; net win if it eliminates the terminal-halt operator cost.** | MED (Variant V3 was rejected for a reason — the cost grounds may still apply) | **#4** |

**Inferred wildcard (LOW build, HIGH leverage):**

- **R0: Cheap pre-flight checks (Q3 above)** — these aren't architectural rewrites but are the highest-EV intervention available *now*. Build cost: ~1-2 eng-weeks total for all three Q3 interventions. Operating cost: near-zero. **If R1-R4 are all >3 eng-week investments, R0 should be deployed first as the bridge.**

**Cost-effectiveness ranking (build + ongoing combined):**

1. **R1 (typed sidecar + tool-write)** — highest build cost but lowest steady-state. Addresses 3 of 5 flaws (1, 2, 3) simultaneously. The structural inversion the master report's Executive-Summary calls for ("invert the substrate").
2. **R2 (Tasklist→AST)** — moderate build, immediately closes Flaw 1's missing terminal link. Pays for itself in saved gap-analysis cycles within 5-10 release iterations.
3. **R3 (contract registry)** — cheapest steady-state op cost, fully CI-bound, fixes Flaw 5 cleanly. Build is modest.
4. **R0 (pre-flight checks)** — should ship as a bridge layer alongside R1-R3, not as an alternative.
5. **R4 (LLM-based anti-instinct)** — net cost-neutral on tokens; only ranks well if the operator-halt cost is the dominant driver (Q1's anti-instinct row says it is — ~1.4 M cumulative — so R4 may rank higher than #4 in practice).

**Build vs steady-state composite:** R1 + R2 + R3 combined cost ~13-19 eng-weeks; steady-state op cost goes DOWN vs current (because eliminated retry cycles dominate the added gate cost). **The rewrite verdict in master:§Architectural-Flaw-Thesis is cost-justified** — the alternative (continuing to add validators) has a steady-state op cost that grows monotonically with pipeline step count (master:§Flaw-2: 9→11→13→14 steps).

---

## Key recommendation

**Deploy R0 (the three Q3 pre-flight checks) within the next release cycle** while planning R1 (typed sidecar + tool-write) as the architectural rewrite. R0 is ~1-2 eng-weeks and prevents the top-3 cost drivers (spec-fidelity non-determinism, anti-instinct false positives, contract drift) from accumulating during the rewrite window. R1's structural inversion then eliminates the substrate that makes the validators necessary in the first place — converging the pipeline's step-count growth (master:§Flaw-2 v4=9 → current=14) by removing rather than adding gates.
