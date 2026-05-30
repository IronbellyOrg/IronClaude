# Refactor Plan — Merge V2 Strengths Into V1 Base

**Base**: V1 (pr86-substrate FINAL-MERGED-CAUSES.md, 269 lines)
**Source of patches**: V2 (T4-substrate FINAL-MERGED-CAUSES.md, 139 lines)

## Planned Changes (incorporating V2 strengths)

### Change #1 — Promote calibrator-non-execution to top-cause status (HIGH priority)

- **Source**: V2 §1 "#1 Calibrator non-execution" (variant-2 lines 19-30)
- **Target**: Insert as NEW §M0 in V1, BEFORE M1; also update §"Top root causes" ranking
- **Rationale**: Substrate divergence (X-001) is THE diagnostic finding of cross-environment comparison. V1 implicitly assumed calibrator ran; on T4 substrate it did not. Both failure modes are real; merged output must cover both.
- **Integration approach**: Add new mechanism M0 at the top of the mechanism stack with substrate-tagging: "M0 applies to T4-shaped substrates where the calibrator was never invoked. M1-M4 apply to pr86-shaped substrates where the calibrator ran but its output was flawed."
- **Risk level**: Low — purely additive, no contradictions with V1's existing mechanisms.

### Change #2 — Add V2's agent-domain mismatch as new cause (MEDIUM priority)

- **Source**: V2 §1 "#5 Agent-domain mismatch" (variant-2 lines 71-82)
- **Target**: Insert as new §M5 in V1 between M4 and "Cross-mechanism implications"
- **Rationale**: V1 entirely misses the assignment-layer failure mode (refactoring-expert assigned a runtime CLI-dispatch hypothesis). This is a structurally-distinct failure class — neither rubric-math nor calibrator-execution; an upstream agent-assignment defect.
- **Integration approach**: New §M5 with V2's evidence (refactoring-expert.md focus areas + the static work-product H3 produced); mark as upstream of M1/M2 (assignment defect predates rubric scoring).
- **Risk level**: Low.

### Change #3 — Adopt V2's layer taxonomy as annotative axis (LOW priority)

- **Source**: V2 throughout (audit / generation / design / assignment layer tags)
- **Target**: Annotate each existing V1 mechanism with its layer tag
- **Rationale**: Layer taxonomy gives a clean conceptual frame for prioritizing fixes (V1 mixes mechanism-layer with fix-layer). Adopting layer tags as an additional axis preserves V1's mechanism depth while gaining V2's prioritization clarity.
- **Integration approach**: Per mechanism, add a single-line layer tag (e.g., "M1 (generation layer): arithmetic-mean dilution"; "M0 (audit layer): calibrator non-execution"; "M5 (assignment layer): agent-domain mismatch").
- **Risk level**: Very low (annotation only).

### Change #4 — Add V2's INV-002 partial-calibration open invariant (MEDIUM priority)

- **Source**: V2 §2 "INV-002 — Partial-calibration handling (UNADDRESSED)" (variant-2 lines 94-98)
- **Target**: Append to V1's "Cross-mechanism implications" as a new bullet, OR add to a new "Open invariants" section
- **Rationale**: This is an UNADDRESSED edge case that affects mixed-execution states (some cards calibrated, some not) — a real risk surface neither variant resolves.
- **Integration approach**: New bullet under "Cross-mechanism implications" titled "Open invariant — partial calibration", citing V2's evidence and proposing the verification step.
- **Risk level**: Low.

### Change #5 — Promote A-001 from unstated to explicit shared assumption (MEDIUM priority)

- **Source**: V2 §5 "A-α — Rubric/calibrator is the right layer to fix" (variant-2 lines 132-133)
- **Target**: Add new §"Shared Assumptions (Limits of This Analysis)" at the end of V1, mirroring V2's §5
- **Rationale**: V1 leaves this entirely unstated. V2 names it. If the right fix is an upstream verification-gate (runtime-output-required-before-confidence-eligible) rather than rubric tweaks, both merges are recommending the wrong layer. Naming this shared assumption is mandatory epistemic hygiene.
- **Integration approach**: New section with V2's four shared assumptions (A-α, A-β, A-γ, A-δ) verbatim, tagged as "Shared assumptions inherited from V2 — V1 omitted these."
- **Risk level**: Low.

### Change #6 — Add Cross-environment synthesis section (HIGH priority — task-specific)

- **Source**: synthesized from this debate + diff-analysis
- **Target**: Append as final §"Cross-Environment Synthesis" before the existing "Synthesis addendum"
- **Rationale**: The task description explicitly requires this if the skill's merged output doesn't surface convergence/substrate-sensitivity/confidence-calibration/numeric-specifics. The skill protocol does not natively produce a cross-environment section, so this is mandatory.
- **Integration approach**: New section with five sub-bullets:
  1. **Convergence on causes** — which top-N appear in both?
  2. **Substrate-sensitivity** — which causes are substrate-specific?
  3. **Confidence calibration delta** — per-cause confidence comparison
  4. **Numeric specifics** — does each environment cite arithmetic?
  5. **Convergence strength assessment** — STRONG/MODERATE/WEAK
- **Risk level**: Low — purely additive.

## Changes NOT Being Made (transparency)

- **NOT replacing V1's M1 (arithmetic-mean dilution) with V2's A-δ shared-assumption treatment.** V1's primary-cause treatment is correct on the pr86 substrate where the arithmetic is observable. V2's demotion is correct on the T4 substrate where calibration didn't run. Substrate-aware framing preserves both.
- **NOT replacing V1's M3 composite (M3a/M3b/M3c) with V2's flat #3 verdict-asymmetry.** V1's three-sub-mechanism decomposition surfaces two independently-deployable fixes (falsification-standard field; dual-instance-minimum) that V2's flat treatment loses.
- **NOT adopting V2's [0.30, 0.85] likelihood cap.** V1's 0.89 for M1 is justified by directly-observable arithmetic on disk. Imposing V2's cap retroactively would weaken evidence-based confidence assignment.
- **NOT adopting V2's terse style globally.** V1's depth is the dominant value-add of the pr86-substrate run; flattening it loses material.

## Review

Auto-approved (no `--interactive` flag).
