# Calibration — R2-sonnet-qa (blind re-grade)

**Calibrator:** opus (claude-opus-4-8) per §11.3 fallback (disjoint set empty; degraded calibrator_diversity).
**Reviewer card:** `card-2-sonnet-qa.md`
**Stance:** Blind — calibrator received reviewer card only; no upstream investigative trail, no other reviewer cards.

## Per-dimension scores

### 1. Citation grounding — 4.5/5
Spot-checked 5 of the reviewer's citations against current code: `SemanticCheck`/`GateCriteria` at `pipeline/models.py:81-105` matches; `_check_frontmatter` at `pipeline/gates.py:91-128` matches; `build_certify_step` at `roadmap/executor.py:1899-1944` matches; `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` at `roadmap/executor.py:2167` matches; `fidelity_checker.py:287-303` and `314-337` fail-open blocks match. All five land on the exact symbols/lines the reviewer claims — calibrated up from reviewer's self-4/5 because spot-check hit-rate was 5/5 with no semantic distortion in the matched regions.

### 2. Coverage completeness — 4/5
The coverage matrix is unusually thorough (12 requirement rows, each with concrete checklist-item ranges and per-phase QA gates), and the 0.90 coverage_pct claim is justified by the matrix the reviewer shows (all R0/R1 phases mapped). Calibrated down slightly from reviewer's 4.5/5 because the reviewer concedes line-818 dual-write remnants and Phase-5/Phase-13 CI inconsistency, both of which are coverage-quality defects (not pure deviation defects) that the matrix does not penalize.

### 3. Deviation-classification clarity — 3.5/5
Severity assignments are defensible: C1 (parser canonicalization contradicting MVR substrate-inversion intent) is correctly Critical because it preserves the exact pathology the rewrite exists to eliminate; H1 (CI classification flip in Phase 5 vs Phase 13) is correctly High because worker agents execute Phase 5 first and would wire CI wrong; H2/H3 are appropriately High (cutover honesty + dual-contract risk). M-tier is reasonable. Holding at 3.5/5 (matching reviewer's self-score) because no Critical-vs-High boundary is sharply justified — C1 could equally be argued as High since the rewrite still produces an envelope and the parser is an export contract, not the substrate itself.

### 4. Risk surface coverage — 4/5
The review explicitly maps all 5 master architectural flaws to tasklist coverage with a flaw-vs-coverage table, and connects findings (especially C1) back to Flaw 3 (markdown-as-state). The PRESERVE-target audit covers all three named files (`commands.py`, `structural_checkers.py`, `convergence.py`) with line citations. This is exactly the brittleness-driver coverage the rubric rewards — not surface lint. Held at 4/5 (matching reviewer) because Flaw 2 (generator/validator asymmetry) coverage leans on Step 9.12's >=3-release cadence without auditing whether the producer-side schema rejection is actually wired before the consumer-side migration, which is the asymmetry's load-bearing seam.

### 5. Recommendation actionability — 4.5/5
Five concrete pre-execution edits listed, each tied to a specific step number (Steps 10/11.2/12.3, 5.1, 9.11, 13.1/13.2, log entries 756-764). The verdict (refactor-then-ship, do not re-author) is unambiguous and gives the next agent a clear branch. Calibrated up from reviewer's 4/5 because the recommendation includes both the fix (rewrite parser plan to envelope-only) and the fallback (mark legacy parser as out-of-roadmap-gate-path) for #1, which is the actionability bar the rubric rewards.

## Calibrated confidence

Arithmetic mean: (4.5 + 4.0 + 3.5 + 4.0 + 4.5) / 5 = **4.1 / 5 = 0.82**

## Verdict after calibration

**PARTIAL — refactor-then-ship.**

Calibration confirms the reviewer's PARTIAL verdict. The 5/5 citation spot-check rate and the substantive C1+H1+H2+H3 findings (each grounded in real BUILD-REQUEST §MVR / §Contract criteria and verified against current code) rule out PASS. The findings are localized to ~5 concrete edit sites rather than a structural re-authoring need, which rules out FAIL. The reviewer's verdict is well-calibrated; calibrated_confidence 0.82 reflects high (but not maximal) trust because Risk Surface Coverage and Deviation-classification clarity have small unjustified seams (Flaw-2 producer-schema wiring depth, C1-vs-H1 boundary).

The 0-finding suspicion clause from the instructions does not apply: this reviewer found 1 Critical, 3 High, 3 Medium, totaling 7 findings on the 831-line tasklist — appropriate signal-to-noise for a tasklist of that size with known MVR substrate-inversion intent.
