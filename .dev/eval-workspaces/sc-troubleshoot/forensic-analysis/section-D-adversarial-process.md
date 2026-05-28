# Section D — Adversarial Process

How the `/sc:forensic` design was stress-tested. Two distinct `/sc:adversarial` runs are evidenced in the corpus:

- **Run 1 (Spec Review, 2026-02-28)** — 3 advocate agents (architect, quality-engineer, analyzer) debated 22 spec-improvement proposals grouped A/B/C/D. Output: `proposal-verdicts.md` (one verdict per proposal).
- **Run 2 (Refactor Plan, 2026-03-19)** — 2 advocate agents (architect, analyzer) debated 2 competing refactor proposal variants (forensic-refactor-handoff.md vs tfep-refactoring-context.md). Output: `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-tasklist.md`.

Both runs are entirely meta-process artifacts — the design *itself* used the adversarial protocol it later prescribes.

## Debate Scope — Two Distinct Runs, Two Different Shapes

**Run 1 scope (proposal grading)**: 22 proposals partitioned into 4 topical groups, each group having a defining failure mode:

- **Group A — Schema & Data Integrity** (`group-A-schema-integrity.md:1`): 6 proposals on schema completeness, field alignment, cross-schema consistency. Severity skewed `major` (P-006 through P-010, P-021). Topics: missing `new-tests-manifest.json` schema (`:5-12`), Risk Surface schema/prompt drift (`:14-21`), `progress.json` resume-safety (`:23-30`), stable `domain_id` slugs vs index-based IDs (`:32-39`), exactly-3 fix tier enforcement (`:41-48`), multi-root path provenance (`:50-57`).
- **Group B — Architecture & Feasibility** (`group-B-architecture-feasibility.md:1`): 6 proposals. Two `critical` (P-013 capability fallback `:23-30`, P-015 minimum-domain rule `:41-48`); rest `major`. Topics include orchestrator-source-read invariant violation (`:5-12`), hard token ceiling enforceability (`:14-21`), MCP tool contract reconciliation (`:32-39`), MCP scheduler specification (`:50-57`).
- **Group C — Phase Contracts** (`group-C-phase-contracts.md:1`): 5 proposals. One `critical` (P-001, normative integrity `:5-12`). Topics: `--depth` semantic conflict (`:14-21`), artifact path inconsistencies for `phase-2/adversarial/` (`:23-30`), `phase-3b/fix-selection.md` location (`:32-39`), dry-run phase plan (`:41-48`).
- **Group D — Quality, Security & Edge Cases** (`group-D-quality-security.md:1`): 5 proposals. Topics: zero-hypothesis terminal path (`:5-12`), baseline test artifact (`:14-21`), pipeline exit status model (`:23-30`), `--clean` lifecycle (`:32-39`), artifact-level secret redaction (`:41-48`).

**Run 2 scope (variant selection)**: A 30-difference taxonomy across two strategic-vs-tactical variants — 5 structural diffs, 10 content diffs, 3 contradictions, 8 unique contributions, 4 shared assumptions (`diff-analysis.md:8-12`). Defining axes: flag model (3-axis new flags vs reused `--depth`) `:46`, quick-mode phase behavior tables vs prose `:30`, two-phase implementation strategy vs single-phase `:36`, escalation thresholds (binary vs qualitative) `:32`.

## Variant Differences — Three Advocate Philosophies (Run 1)

Each opus advocate held a distinct "skeptical lens" declared in their header:

- **opus:architect** (`variant-1-opus-architect.md:1-7`): "Architectural soundness, implementation feasibility within Claude Code's actual capabilities, avoiding over-specification" — skeptical of "proposals that add complexity without clear implementation benefit." Championed *minimalism + invariant preservation*. Pushed simpler alternatives: slug instead of UUID/hash for P-009 (`:51-55`), single `--redact-artifacts` flag instead of a redaction policy framework for P-020 (`:108-112`), restrict `--clean` to terminal success without sub-options for P-019 (`:102-106`).
- **opus:quality-engineer** (`variant-2-opus-quality-engineer.md:1-7`): "Testability, determinism, edge case completeness, schema rigor" — skeptical of "proposals that weaken quality gates." Championed *mandatory fields and testable invariants*. Pushed back against the architect's relaxations: wanted all `progress.json` fields mandatory for resume safety (P-008 `:44-47`, 0.90 confidence vs architect's MODIFY), wanted to *retain* hard token ceilings as testable max (P-012 modification `:64-68`), wanted configurable redaction policy not a single flag (P-020 `:106-109`).
- **opus:analyzer** (`variant-3-opus-analyzer.md:1-7`): "Practical impact — which proposals fix real implementation blockers vs theoretical concerns" — skeptical of "proposals that address unlikely scenarios at the cost of spec complexity." Championed *frequency-weighted pragmatism*. Repeatedly cited day-1 implementation pain (P-001 `:11-12`, P-002 `:14-17`, P-004 `:24-27`) and discounted low-frequency scenarios: domain ID drift "theoretically problematic but practically rare" (P-009 `:51-55`), full redaction policy "over-engineering for v1" since secrets are uncommon in forensic targets (P-020 `:109-113`), multi-root provenance only at domain level since most invocations target one root (P-021 `:115-119`).

The triangulation worked: architect set ceiling on complexity, QE set floor on rigor, analyzer set lens for what actually ships. All three converged on rejecting **P-022** (MCP scheduler spec) at 0.72–0.78 confidence (`variant-1-opus-architect.md:119-122`, `variant-3-opus-analyzer.md:121-124`) — the strongest cross-perspective signal in the entire corpus.

## Base-Selection Logic (Run 2) — Edge-Case Floor Trumps Scoring

The base-selection rubric in `base-selection.md` uses a **50% quantitative + 50% qualitative** combined score, but the decision turned on an *eligibility floor*, not the score itself:

- **Quantitative** (`:4-15`): 5 weighted metrics (Requirement Coverage 0.30, Internal Consistency 0.25, Specificity 0.15, Dependency 0.15, Section Coverage 0.15). Variant A = 0.860, Variant B = 0.839 — within 2.5%.
- **Qualitative** (`:19-110`): 6 dimensions × 5 binary criteria each (Completeness, Correctness, Structure, Clarity, Risk Coverage, **Invariant & Edge Case Coverage**). Both variants tied at 18/30 = 0.600.
- **Combined**: A = 0.730, B = 0.720, margin 1.0% — within the 5% tiebreaker range (`:135-136`).

But **Variant B scored 0/5 on Invariant & Edge Case Coverage** (`:91`), triggering an explicit "edge case floor" rule: "BELOW FLOOR (ineligible as base variant)" (`:95`). Variant A's 1/5 cleared the floor by a hair. The rationale (`:141-149`): two reasons cited — (1) floor enforcement; (2) Variant A won the two most architecturally consequential debate points (C-001 flag model at 65% and X-001 same-topic contradiction at 60%), both L3 (state-mechanics) decisions.

Decision criteria the team trusted, in priority order: **edge-case eligibility floor > L3 architectural correctness > L2 specificity > L1 presentation**. The floor enforcement explicitly overrode a near-tied score — meaning the team trusted "covers edge cases at all" more than "complete coverage of explicit requirements." This is the inverse of normal scoring instinct and is the most revealing decision in the corpus.

## Debate Transcript — Where Convergence Failed (Run 2)

The debate converged to only **76%** against an 80% threshold (`debate-transcript.md:156`), explicitly NOT_CONVERGED. The blocking finding: "2 HIGH-severity UNADDRESSED invariants (INV-001, INV-004)" (`:158`).

The Round 2.5 invariant probe (`:139-149`) ran a separate check independent of the advocate debate and surfaced 5 invariants neither variant covered:
- **INV-001 (HIGH)**: How to distinguish pre-existing vs agent-written tests without a baseline mechanism.
- **INV-003 (MEDIUM)**: pytest parametrize inflates the "3+ new tests fail" threshold into false positives.
- **INV-004 (HIGH)**: Forensic output → task-unified tasklist insertion format unspecified.
- **INV-005 (MEDIUM)**: Same-failure vs new-failure distinction for escalation.

This invariant probe is the protocol's safety valve: when advocate debate misses something, an orthogonal probe forces resolution. Both HIGH invariants (INV-001, INV-004) were converted directly into new tasks (Change #10, #11 in `merge-log.md:73-85`) — neither came from either advocate. Six debate points remained unresolved at convergence (S-005, C-005, C-006, X-003, A-002, A-003 — `debate-transcript.md:159`), but all were L1/L2 (cosmetic/specificity), not L3 (architecture).

## Merge Log — 11/11 Applied (Run 2)

`merge-log.md:1-12` shows 11 planned changes, 11 applied, 0 failed/skipped. Pattern: base = Variant A (architecture skeleton), 9 incorporations from Variant B (tactical specs), 2 inserts from invariant probe.

What got accepted from each:
- **From Variant A (base, preserved)**: 3-axis flag model, responsibility split, coupling contract, `--caller`/`--trigger` concept, profiles abstraction, genericity preservation requirement (`base-selection.md:151-159`). Explicitly NOT taken from B: the `--depth` overloading approach (`refactor-plan.md:97`, citing X-001 60% A-win).
- **From Variant B (incorporated)**: per-phase behavior table (`merge-log.md:14-20`), binary escalation thresholds (`:22-27`), token budget estimates (`:29-32`), two-phase implementation strategy (`:34-40`), YAML context interface (`:42-46`), section-by-section forensic change mapping (`:48-53`), "test is wrong" as valid outcome (`:55-59`), artifact directory tree (`:61-65`), user-approved decision log (`:67-71`).
- **From invariant probe (new)**: test baseline snapshot mechanism (`:73-78`, Task 1.3), artifact/tasklist insertion format (`:80-85`, Task 2.5).

Post-merge validation (`:89-105`) rescanned for contradictions and found none — the merger explicitly checked that the merged document didn't reintroduce the `--depth` overloading conflict it had rejected.

## Verdicts — Accept (14), Modify (7), Reject (1) — Run 1

`proposal-verdicts.md:38-42` summarizes: 14 ACCEPT, 7 MODIFY, 1 REJECT — out of 22, achieving 100% convergence in 2 rounds (`:6,154`).

**Top-3 ACCEPT (highest confidence, unanimous)**:
- **P-001** (`:16`, conf 0.96) — Move panel additions from Section 17 commentary into normative sections. All 3 advocates rated this highest-impact: "Non-normative requirements are untestable requirements" (QE, `variant-2-opus-quality-engineer.md:12`). The single highest-impact structural fix.
- **P-004** (`:19`, conf 0.94) — Standardize artifact paths to `phase-2/adversarial/`. Path inconsistencies are "the #1 source of 'it works for me but not for you' bugs" (analyzer, `variant-3-opus-analyzer.md:27`).
- **P-013** (`:28`, conf 0.93) — Capability fallback for model-tier assignment with "requested vs actual tier" logging. Architect called it "the most feasibility-critical proposal" (`variant-1-opus-architect.md:75`); analyzer called it "the most practically impactful feasibility proposal" (`variant-3-opus-analyzer.md:74`).

**Top-3 REJECT/MODIFY signals (what NOT to do)**:
- **P-022 — REJECTED** (`:37`, conf 0.76, only rejection). Specify MCP scheduler behavior (semaphores, backoff, queue ordering). Rejection rationale (`:87-97`): (1) **Framework delegation** — scheduling belongs in MCP.md, not the forensic spec; duplicating creates "maintenance conflicts and potential divergence" (`:91`); (2) **Existing mitigation** — `--concurrency` flag already handles it (`:93`); (3) **Over-specification** — prescribing internal mechanisms is "inappropriate for a requirements specification" (`:95`). A minor FR addendum was accepted instead. The signal: *don't put framework-level concerns into feature specs even when they're nominally relevant*.
- **P-020 — MODIFIED** (`:35`, conf 0.77). Original wanted configurable per-environment redaction policy with secure raw retention flag. Modified down to: agent prompt awareness + single `--redact` flag (default true), defer configurable policy to v2 (`:73-76`). Signal: *don't build enterprise frameworks for v1 when a single flag covers 90% of use cases*.
- **P-019 — MODIFIED** (`:34`, conf 0.78). Original proposed `--clean=archive|delete` sub-options. Modified to binary: clean only on terminal `success`, retain otherwise (`:68-71`). Signal: *don't add CLI sub-options for niche cases when terminal-status gating covers the use case*.

The pattern across all 7 MODIFY verdicts: the spec was systematically *narrowed* from the QE's maximalist initial positions toward simpler v1 defaults, with the architect and analyzer applying drag. Of the 7 modifications, **5 originated as QE-vs-others disagreements** (`:23-37` Dissenting Opinions column) — P-007, P-008, P-012, P-019, P-020 all moderate QE's original maximalism. This is the structural reason the protocol uses 3 advocates rather than 2: the QE consistently pushed comprehensiveness, requiring two counter-voices to triangulate to v1-realistic scope.

---

## Summary

**3 variants' philosophies**: Architect = minimalism + invariant preservation (skeptical of complexity-without-benefit); Quality-Engineer = mandatory fields + testable bounds (skeptical of weakened gates); Analyzer = frequency-weighted pragmatism (skeptical of unlikely-scenario coverage). Of 7 MODIFY verdicts, 5 trace to QE-vs-others disagreements where architect+analyzer triangulated QE's maximalism down to v1-realistic scope.

**Merge winner pattern (Run 2)**: Variant A (architectural skeleton) won as base via the **edge-case floor rule** despite tied combined score (0.730 vs 0.720) — B scored 0/5 on Invariant & Edge Case Coverage, ineligible. A held L3 architectural wins (3-axis flag model, 65% confidence on C-001); B contributed 9 of 11 merged changes as tactical specs (phase tables, token budgets, YAML schemas). Plus 2 new tasks from the invariant probe (INV-001 baseline mechanism, INV-004 tasklist insertion format) that neither advocate caught.

**Top-3 accepts**: P-001 normative integrity (0.96), P-004 path standardization (0.94), P-013 model-tier fallback (0.93). **Top-3 rejects/narrowings**: P-022 MCP scheduler REJECTED (framework delegation, over-spec); P-020 redaction policy NARROWED to single flag; P-019 `--clean` NARROWED to binary terminal-success behavior. The recurring rejection signal: don't put framework concerns in feature specs, and don't ship v1 enterprise configurability when a flag suffices.
