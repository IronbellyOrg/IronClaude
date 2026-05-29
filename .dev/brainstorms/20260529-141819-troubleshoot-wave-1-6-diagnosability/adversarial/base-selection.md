# Base Selection

## Quantitative Scoring (compact form — full 30-criterion rubric collapsed to dimension subtotals for brevity)

| Variant | Req coverage | Internal consistency | Specificity | Dep completeness | Section coverage | Quant subtotal (weight 0.50) |
|---------|--------------|---------------------|-------------|------------------|------------------|------------------------------|
| V1 architect | 10/10 success criteria addressed | High (no contradictions; cross-refs resolve) | High (line ranges, named fields, tables over prose) | High (every claim cites SKILL.md line, ref-file, or Open Question #) | 13/13 sections | **0.93** |
| V3 devops | 10/10 success criteria addressed | High | High (literal auggie query strings, fallback bash, JSON schemas, 5-task tasklist) | High | 13/13 sections | **0.91** |
| V4 field study | 8/10 (no contract-additions section, no SKILL.md diff sketch — by design, since DISQUALIFIED on settled forks) | High (within its scope) | Highest (literal diff, file paths, line numbers, $-prefixed env vars) | Medium (cites no SKILL.md sections — out of frame) | 7/13 sections (DISQUALIFIED for base) | **0.50** (eligibility-capped due to fork-lock disqualification) |

## Qualitative Scoring (6 dimensions × 5 criteria = 30; abbreviated to per-dimension subtotals)

| Dimension | V1 | V3 | V4 |
|-----------|-----|-----|-----|
| Completeness | 5/5 | 5/5 | 3/5 (no contract / no SKILL.md diff) |
| Correctness | 5/5 | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 | 4/5 (uses its own §-numbering, not seed-brief structure) |
| Clarity | 4/5 | 5/5 | 5/5 |
| Risk Coverage | 5/5 | 5/5 | 5/5 |
| Invariant & Edge Case Coverage | 4/5 (acknowledges Heisenbug at high level) | 4/5 (env-drift between dev/prod called out) | 5/5 (Heisenbug, instrumentation drift, 3-round cap, all 5 risks explicit) |
| **Qualitative subtotal (weight 0.50)** | **0.93** | **0.97** | **0.90** (capped) |

## Combined Scoring

| Variant | Combined | Eligible for base | Notes |
|---------|----------|-------------------|-------|
| V1 architect | **0.93** | ✓ | Strongest on contract design, ref-file changes, SKILL.md diff sketch |
| V3 devops | **0.94** | ✓ | Strongest on audit mechanics, tasklist actionability, query strings |
| V4 field study | **0.70** | ✗ DISQUALIFIED (scope/placement/mechanism fork-lock) | Strongest on temporal-discipline rhetoric, additives, real-world grounding |

## Tiebreaker (V1 vs V3 within 5%)

V1 and V3 are within 1% of each other.

- Level 1 — Debate performance: V3 won 4 of 5 debate axes (Axes 1, 2, 3, 5; Axis 4 was a compromise with V1's position dominant). V3 wins tiebreaker Level 1.

## Selected Base: V3 (devops)

**Selection rationale**: V3 won 4 of 5 disputed axes plus Axis 4 partial credit. V3 also brings the highest-value unique contribution (U-001: complete 5-task worked tasklist with framework detection, fields rationale, Verification, Rollback) which sets the actionability bar for the merged spec. V3's audit mechanics (literal auggie query strings + bash fallback + JSON schemas per branch) are reproducible without further design.

**Strengths to preserve from V3 (base)**:

- 2-branch fan-out (Branch A log-calls + exception piggyback; Branch B log-config)
- Audit card named `diagnosability-context.md` (naming-symmetry with `doc-context.md`)
- 4-field contract addition (no `status` enum extension)
- 5-task worked tasklist format with framework-aware syntax
- Literal auggie query strings + bash fallback per branch
- JSON schema per branch output
- `--diagnosability-handoff` opt-in flag for task-builder packaging

**Strengths to incorporate from V1 (non-base)**:

- **Branch F (symptom-coverage) analytical content** — preserved as orchestrator synthesis logic in `refs/diagnosability-audit.md` Section 4 (NOT a 3rd branch). Cross-references the 3 W's (when/where/why) against Branch A inventory + Branch B reachability.
- **`--depth deep` does NOT force hard-stop** (V1 position) — but with V1+Round-2 refinement: soft-warn is mandatory under `--depth deep` with a prominent banner.
- **`--no-escalate` SHOULD suppress hard-stop** (V1 position) — preserves opt-out symmetry.
- **Comprehensive SKILL.md diff sketch** (V1 had the most detailed line-range-by-line-range plan; adopt verbatim with V3's contract-field set substituted).
- **Stack-trace-self-documents short-circuit** (both V1 and V3 had this; V1's worked-example framing adopted).
- **Hypothesis-card-template note** (V1 only — add one line under `## Grounding gaps` referencing the diagnosability card).

**Strengths to incorporate from V4 (field study, pre-absorbed via seed brief)**:

- **Byte-count metric** for sufficiency assessment
- **Invocation-site-only instrumentation rule** as HARD constraint in the tasklist format
- **3-round patch-loop cap** — addresses Open Question #6
- **Heisenbug fallback** in Risk Register
- **Component-identification step (S0.1)** as explicit first substep in Wave 1.6
- **T4 worked example** in `refs/diagnosability-audit.md`
- **"No hypothesis work in the same turn as an instrumentation patch"** as load-bearing rhetorical rule
- **Bypass-is-logged** discipline for `--no-diagnosability-audit`

**Strengths NOT incorporated** (per fork lock):

- V4 broader scope (CLI flags + OS introspection + doctor commands) — v1.1 follow-up
- V4 pre-Wave-1 placement — placement remains between 1.5 and 1.7
- V4 shell-based discovery mechanism — auggie remains primary
- V4 binary verdict — quaternary verdict (`sufficient | partial | insufficient | unknown`) retained

## Edge-Case-Floor Check

All 3 variants score ≥ 4/5 on Invariant & Edge Case Coverage. No variant is ineligible.

## Final Note on Fork-Lock Application

V4's combined score (0.94 uncapped on its own scope) would have made it a contender for base. The settled-fork lock (user Option A decision, 2026-05-29) disqualifies it because base selection determines the structural shell of the merged spec, and the lock forbids scope/placement/mechanism shifts. V4's additives ARE in the merged spec; V4's structural alternatives are explicitly recorded as the rejected road in the merge log.
