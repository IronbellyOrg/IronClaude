---
base_variant: "roadmap-opus-architect"
variant_scores: "A:81 B:79"
---

# Roadmap Variant Evaluation — `roadmap validate`

**Variant A** = `roadmap-opus-architect.compressed.md` (Opus/architect — 6w, linear, executor-folded merge, ~48 deliverables).
**Variant B** = `roadmap-sonnet-architect.compressed.md` (Sonnet/architect — 10w, DAG cross-edges, dedicated semantics milestone, ~70 deliverables).
Debate convergence: **0.74** — the architectural core (20 shared assumptions) was never contested; the fork is milestone packaging, schedule, and contract-lock sequencing.

## 1. Scoring Criteria (derived from the debate)

The debate established that *what gets built* is identical, so criteria target *how it is packaged and sequenced* — exactly the contested surface. Weights reflect how load-bearing each axis was in the transcript.

|#|Criterion|Weight|Debate origin|
|---|---|---|---|
|C1|Architectural soundness / report-semantics seam|20|Divergence 2/3/4/14 — the single largest structural fork|
|C2|Safety-mechanism sequencing (import gate + OQ front-load)|20|Divergence 6/7 — both reached explicit agreement|
|C3|Schedule realism|15|Divergence 1 — unresolved/empirical|
|C4|Risk distribution / blast-radius|15|Divergence 1 + 2 rebuttals (concentration vs distribution)|
|C5|Edge-path & contract coverage (gate-failure, resume, partial-report)|15|Divergence 8 — resolved toward B|
|C6|Granularity appropriateness|15|Divergence 5 — partially resolved, context-dependent|

## 2. Per-Criterion Scores

|Criterion|A|B|Evidence|
|---|---|---|---|
|C1 Seam/architecture|88|74|A's executor-folded merge "co-locates logic with its producer"; the convergence synthesis explicitly adopts A's structure ("implement merge semantics co-located with the executor"). A's unrebutted rebuttal showed B's dedicated M4 *creates* the hand-off seam — B's M2 executor (COMP-001) emits a report whose semantics finalize two milestones later in M4 (FR-050.6/050.7), the exact late-churn risk B claims to avoid.|
|C2 Safety sequencing|85|80|A builds the NFR-050.2 import-scan as a day-one CI gate in M1 (deliverable #9); B conceded this is "strictly better" and deferred its own to M5 (TEST-010). Offsetting: OQ front-loading resolved *toward* B (all OQ-001..007 before M2 exit), but A already front-loads type contracts + OQ-001, narrowing the gap.|
|C3 Schedule realism|78|72|A correct that uniform 2w blocks over-bill 1-week surfaces (M1 config, M4 CLI plumbing) — "buffer disguised as scope." B correct that A's 2-week M3 has zero downstream slack in a linear chain. Synthesis (~7-8w, effort-sized executor + explicit slack) lands nearer A's effort-sizing principle than B's uniform padding.|
|C4 Risk distribution|74|84|B's clean rebuttal: A's M3 owns "the feature's highest-error surface *and* its tightest schedule" (executor + merge + count-recalc + agreement table folded into one 2w milestone with no slack). B's uniform schedule + dedicated semantics milestone distributes the blast radius A concentrated.|
|C5 Edge/contract coverage|75|88|B's OPS-003 + TEST-013 make gate-failure artifact policy a *tested* unit; A's rebuttal conceded only that the decision matters, leaving it as an M3 risk note — "a risk note is not testable" stood unrebutted. B also adds COMP-016 (resume dispatcher) and R-010 (resume/gate-failure edge coverage); A covers resume only via FR-050.4a.|
|C6 Granularity|82|80|Team-shape-dependent. A's ~48 is right for a senior implementer; resolver boundaries (COMP-009/010/011) are inferable. B's ~70 lowers ambiguity for parallel/junior teams but A's unrebutted point — B double-counts resolver *decisions* as both OQ resolution and tracked components — slightly inflates B's set. Near-tie, marginal edge to A on signal-to-overhead.|

## 3. Overall Scores

|Variant|C1·.20|C2·.20|C3·.15|C4·.15|C5·.15|C6·.15|Total|
|---|---|---|---|---|---|---|---|
|A|17.6|17.0|11.7|11.1|11.25|12.3|**80.9 → 81**|
|B|14.8|16.0|10.8|12.6|13.2|12.0|**79.4 → 79**|

**Justification:** The 2-point spread mirrors the 0.74 convergence — these are not competing designs but competing *packagings* of one design. A wins the two highest-weighted axes (C1 architecture, C2 safety sequencing), both of which the debate resolved in A's direction (synthesis adopts A's co-location; B conceded A's import gate). B wins C4 and C5, which are real and become the merge graft-list rather than disqualifiers.

## 4. Base Variant Selection — Variant A

Variant A is selected as the merge base on three evidence-grounded grounds:

1. **The convergence synthesis adopts A's structure.** On the largest structural fork, the reconciling move is "freeze the report+merge *contract* in M1/M2 (B's contract-lock) but implement merge semantics co-located with the executor (A's seam-minimization)." The *implementation skeleton* that survives is A's; B's contribution is timing, which grafts onto A cleanly.
2. **A holds a strictly-dominant, conceded safety win.** B explicitly conceded the day-one import gate ("strictly better… no schedule cost"). A's skeleton already encodes it (M1 #9); B's must be moved earlier to match A.
3. **Additive-correction asymmetry.** A's gaps (C4/C5) are filled by *adding* explicitness — tracked deliverables, slack, edge tests — onto a structurally-correct lean skeleton. B's gaps (C1) require *restructuring* the milestone boundary. Adding to a correct skeleton is lower-risk than rebuilding B's seam.

## 5. Improvements to Graft from Variant B

Incorporate the following B-side elements into the A base during merge (each maps to a debate-resolved or B-favored point):

1. **Gate-failure artifact policy as a tracked, tested unit** (Divergence 8, resolved toward B): promote A's M3 Risk #1 note into explicit deliverables modeled on B's **OPS-003** (gate-failure artifact policy → `tasklist_ready` value for missing/partial report) + **TEST-013** (malformed-output warn-and-continue test). Resolves OQ-007 as shipped behavior, not mitigation.
2. **OQ front-loading** (Divergence 6, resolved toward B): tighten A's "just-in-time" OQ stance — resolve contract-defining OQ-001/004/005/007 before the M3 executor milestone (per B's M1 exit criterion), while leaving genuinely local OQ-002/006 in place. Adopt *both* safety mechanisms early, the debate's predicted strongest synthesis.
3. **Explicit resume/edge coverage** (B C5 win): add B's **COMP-016** (resume validation dispatcher) and **R-010** (resume/gate-failure edge-path test coverage) to A's M5, since A's resume handling is implicit in FR-050.4a only.
4. **Executor blast-radius slack** (Divergence 1 synthesis): keep A's effort-sizing but apply B's distribution insight — give A's M3 executor block explicit sized slack (target ~7-8w total, not A's slack-free 6w), since M3 owns the highest-error surface.
5. **Defined P1 descoping lever** (Divergence 11, B's unrebutted point): A's slack-free schedule "most needs the P1 descoping lever it refuses to define." Adopt B's **P1 classification of FR-050.5e/5f (WARNING dims) + DM-007** as an explicit, documented descoping lever — flagged as a product release-criticality decision, not silently applied.
6. **Selective resolver explicitness** (Divergence 5, team-shape hedge): if the implementing team is parallel/junior, surface B's **COMP-009 (filename resolver)** and **COMP-010 (model-precedence resolver)** as tracked deliverables tied to OQ-001/OQ-004 outputs — avoiding B's double-count by binding them to the OQ resolution rather than listing them independently.

Items 1, 2, and 3 are debate-resolved and should be incorporated unconditionally. Items 4, 5, and 6 are flagged for the product/team-velocity decisions the debate explicitly could not close.
