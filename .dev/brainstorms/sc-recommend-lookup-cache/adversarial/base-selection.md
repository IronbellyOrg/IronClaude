# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 opus | V2 sonnet | V3 haiku |
|---|---|---|---|---|
| Requirement coverage (seed brief constraints) | 0.30 | 0.95 | 0.95 | 0.95 |
| Internal consistency | 0.25 | 0.90 | 0.90 | 0.95 |
| Specificity ratio (concrete vs vague) | 0.15 | 0.75 | 0.85 | **0.95** |
| Dependency completeness (cross-refs to existing patterns) | 0.15 | **0.90** | 0.80 | 0.75 |
| Section coverage | 0.15 | 0.85 | **0.95** | 0.90 |
| **Quant score** | | **0.876** | 0.893 | **0.908** |

## Qualitative Scoring (50% weight, 30-criterion rubric)

| Dimension (5 criteria each) | V1 opus | V2 sonnet | V3 haiku |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 4/5 (intentionally minimal — skips deep scaling-path detail) |
| Correctness | 4/5 | 4/5 | **5/5** (only variant with empirical cost reconstruction) |
| Structure | 5/5 | **5/5** | 4/5 |
| Clarity | 4/5 | 4/5 | **5/5** (most concrete, fewest hedges) |
| Risk Coverage | **5/5** | **5/5** | 4/5 (uses inline LIMIT FLAGs instead of consolidated section) |
| Invariant & Edge Case | 3/5 | 3/5 | **5/5** (catches native-cache anti-pattern; pulls 80%→60-70%) |
| **Qual score** | 26/30 = 0.867 | 26/30 = 0.867 | 27/30 = 0.900 |

Edge-case floor: all variants score ≥ 1/5 on Invariant & Edge Case — none ineligible.

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined |
|---|---|---|---|
| V1 opus:architect | 0.876 | 0.867 | **0.872** |
| V2 sonnet:performance | 0.893 | 0.867 | **0.880** |
| V3 haiku:analyzer | 0.908 | 0.900 | **0.904** |

V3 leads by ~2.4% over V2 (>5% threshold not triggered → no tiebreaker needed).

## Selected Base: Variant 3 (haiku:analyzer)

### Rationale

V3 is the smallest viable proposal anchored in empirical evidence (the 46% Auggie cost finding is the single load-bearing insight no other variant produced). It applies `feedback_prefer_simpler_proposals` more rigorously than V1 or V2 and demonstrates Haiku capability by being itself the Haiku-authored variant.

### Strengths to preserve

- Cost root-cause analysis with per-Phase-0-step breakdown
- "Hot path > 80%" critique pulling the headline number to 60-70%
- "Caching native-tooling recommendations buys nothing" (anti-bloat)
- `[HAIKU LIMIT FLAG]` honesty marker pattern
- Single YAML, 5-field schema, no plugin table at MVP
- "Things This Proposal Does NOT Do" intentional-omissions section

### Strengths to incorporate from V1 (opus:architect)

- **Soft fallback ladder** (U-004): if Haiku-pure fails eval, fallback is Haiku-classify + Opus-pipeline on miss. De-risks the Haiku-only constraint without abandoning it.
- **`classifier_score_hints`** (U-001) — listed in scaling path, not MVP
- **`cache_miss: low_confidence`** signal when top-2 scores within 10% — cheap ambiguity check
- **Cold-path SKILL.md inlining problem** (V1 risk #6): the cold-path Haiku needs a condensed runbook, not the full SKILL body. Critical for not re-introducing the cost.

### Strengths to incorporate from V2 (sonnet:performance)

- **JSONL telemetry schema** (U-009) — load-bearing for the kill-switch decision
- **4K-8K hot-path budget gate** (U-008) — concrete decision criterion
- **Kill switch**: below 60% hit rate after 2 weeks, disable cache and keep instrumentation
- **`prompt_envelope_template` field** (U-005) — store hand-off skeleton in the row so hot path emits without re-deriving
- **Plugin TTL bands** (U-007) — listed in scaling, applies when plugin table arrives
