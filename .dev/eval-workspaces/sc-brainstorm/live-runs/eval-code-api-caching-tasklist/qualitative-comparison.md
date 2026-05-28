# Qualitative Comparison: eval-code-api-caching-tasklist

**Baseline artifact:** `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-code-api-caching-tasklist/with_skill/outputs/merged-requirements.md`

**Live artifact:** `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-api-caching-tasklist/merged-requirements.md`

**Optional structural context:** `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.json`

## Verdict

**Winner: Baseline** by 7 points (baseline 54/60, live 47/60).

The baseline is substantially more concrete, better provenanced, and more directly implementable. The live artifact is broader and safer as a generic API caching requirements document, especially around tenant/user isolation, purge controls, stale-if-error gating, rollout states, and auditability. However, it regresses on code-level specificity, source traceability, and explicit adversarial synthesis. For a code/API-caching tasklist handoff, the live artifact is useful but less implementation-ready than the baseline.

## Score Table

| Dimension | Baseline | Live | Winner |
|---|---:|---:|---|
| Concreteness | 10 | 7 | Baseline |
| Coverage | 8 | 9 | Live |
| Actionability | 9 | 8 | Baseline |
| Provenance | 10 | 6 | Baseline |
| Adversarial synthesis | 9 | 7 | Baseline |
| Fit to eval intent | 8 | 10 | Live |
| **Total** | **54** | **47** | **Baseline** |

## Dimension Notes and Penalty Arithmetic

### 1. Concreteness

**Baseline: 10/10**

Start at 10.

- No penalty: specifies a Redis-backed FastAPI `RequestCacheMiddleware`, concrete cache key format, explicit TTL defaults, exact invalidation paths, SETNX-based stampede protection, metrics names, canary targets, test counts, and runbook path.
- No penalty: includes implementation locations such as `src/api/middleware/request_cache.py`, `src/api/middleware/cache_invalidation.py`, `src/api/shared/redis.py`, `src/api/services/pricing.py`, and `config/api.yaml`.

Final: 10.

**Live: 7/10**

Start at 10.

- -1.5: deliberately avoids selecting backend, framework, topology, or persistence model, which is defensible in requirements but reduces code-tasklist concreteness.
- -1.0: uses broad mechanisms such as "registry or equivalent control plane" and "another documented mechanism" without implementation shape.
- -0.5: no file/module targets, migration target, cache-key canonical representation, TTL defaults, or metric names.

Final: 7.

### 2. Coverage

**Baseline: 8/10**

Start at 10.

- -1.0: narrows scope to catalog/pricing/feature-flag reference data and does not cover a general endpoint inventory/classification workflow as strongly as the live artifact.
- -0.5: limited explicit treatment of tenant/user/confidential/regulated response classification.
- -0.5: weaker operational coverage for manual purge controls, audit events, rollback states, stale-if-error policy, and data-residency/privacy constraints.

Final: 8.

**Live: 9/10**

Start at 10.

- -0.5: lacks concrete TTL classes, budget values, and implementation targets.
- -0.5: no explicit migration story for existing caches or non-HTTP/background consumers.

Final: 9.

### 3. Actionability

**Baseline: 9/10**

Start at 10.

- -0.5: some assumptions may need validation before work begins, especially stack, endpoints, Redis availability, and specific paths.
- -0.5: it is a requirements artifact rather than an actual tasklist, despite enough detail to convert into tasks easily.

Final: 9.

**Live: 8/10**

Start at 10.

- -1.0: good workstream breakdown but many items remain policy-level and require an implementation-design pass before coding.
- -0.5: acceptance criteria are testable but often generic rather than tied to named endpoints, files, metrics, or exact thresholds beyond p95 improvement/load reduction.
- -0.5: tasklist handoff scope is present, but the merged requirements alone do not contain the actual task decomposition.

Final: 8.

### 4. Provenance

**Baseline: 10/10**

Start at 10.

- No penalty: frontmatter includes adversarial status, proposal count, source proposals, source seed, debate transcript, and agent composition.
- No penalty: each major requirement/risk/open question has a provenance table entry tying it to seed brief questions, proposal sections, or debate tensions.

Final: 10.

**Live: 6/10**

Start at 10.

- -1.5: no `## Provenance` section; the structural validator also flags this absence.
- -1.0: inline HTML comments name base/incorporated variants but do not trace each requirement to source proposals or debate tensions.
- -1.0: frontmatter has contract/status/convergence but omits `spec_type` and `adversarial_status` expected by the iteration-2 structural checks.
- -0.5: structural context shows missing `agent_spec` persona/model metadata in `return-contract.yaml`, reducing auditability even though artifacts exist.

Final: 6.

### 5. Adversarial Synthesis

**Baseline: 9/10**

Start at 10.

- -0.5: mostly presents resolved consensus; it preserves only a few open disagreements such as cache headers and body-in-GET keying.
- -0.5: some risks read as clean mitigations rather than preserving the full tradeoff space.

Final: 9.

**Live: 7/10**

Start at 10.

- -1.0: has evidence of adversarial merge in comments and convergence metadata, but little visible debate/tension resolution in the body.
- -1.0: lacks detailed requirement-by-requirement synthesis provenance.
- -1.0: broad safety framing may reflect synthesis, but it does not show how competing proposals were reconciled or rejected.

Final: 7.

### 6. Fit to Eval Intent

**Baseline: 8/10**

Start at 10.

- -1.0: strong fit for a code implementation brief, but less fit for a `tasklist` handoff because it does not include tasklist workstreams or handoff metadata.
- -1.0: assumes a specific target system and endpoints; if the eval intent is generic "add caching to API endpoints," those assumptions may overfit.

Final: 8.

**Live: 10/10**

Start at 10.

- No penalty: directly targets "add caching to API endpoints" at a requirements level, includes policy registry, endpoint inventory, rollout, purge, observability, resilience, and a dedicated tasklist handoff scope.
- No penalty: optional structural context confirms `handoff_action = tasklist` and a `handoff/tasklist-index.md` artifact exists.

Final: 10.

## Top 3 Regressions in Live vs Baseline

1. **Implementation specificity regressed.** Baseline identifies concrete backend/framework choices, cache key shape, TTL defaults, module paths, metrics names, and test quantities. Live intentionally remains backend/framework agnostic and therefore gives the tasklist generator less code-level material.
2. **Provenance/audit trail regressed.** Baseline has explicit frontmatter plus a detailed provenance table mapping requirements to seed/debate/proposals. Live only has top comments and contract frontmatter, and the structural context flags no Provenance section.
3. **Visible adversarial synthesis regressed.** Baseline exposes debate tensions and preserved open questions. Live says it incorporated variants but does not show tension-level synthesis or why alternatives were accepted/rejected.

## Top 3 Improvements in Live vs Baseline

1. **Security and isolation coverage improved.** Live explicitly covers tenant-scoped, user-scoped, confidential, regulated, auth/session, secret-bearing, authorization, and data leakage concerns.
2. **Operational controls improved.** Live adds manual purge by scope, rollout/rollback states, policy versioning, stale-if-error gating, audit events, and operator disablement without deployment.
3. **General API-caching applicability improved.** Live avoids overfitting to catalog/pricing/flags and frames an endpoint inventory/classification process suitable for a broader API layer rollout.

## Structural Failure Interpretation

The structural failures are **mixed**:

- **Real quality regressions:** missing `## Provenance` in the live merged requirements is a genuine quality regression because it materially weakens traceability. The apparent zero-item Risks failure is also quality-relevant to the evaluator, though the live artifact does contain a risk table; the failure likely comes from the structural checker expecting enumerated risk items rather than table rows.
- **Metadata/parameter mismatches:** missing `agent_spec` persona/model aliases in `return-contract.yaml` are primarily metadata contract regressions, not direct content-quality failures in the merged requirements. The live artifact itself includes comments showing base/incorporated variants and frontmatter showing proposal count/convergence.
- **Not a content absence:** functional, non-functional, acceptance, open-question, artifact-completeness, handoff, and adversarial-directory checks pass in the structural context, so the live run is complete enough for qualitative review despite metadata misses.

## Is `/sc:adversarial --depth quick` Warranted?

**No.** A quick adversarial rerun is not warranted for this comparison.

Reason: there is no unresolved qualitative tie, contradictory evidence, or high-stakes ambiguity. The tradeoff is clear: baseline wins implementation-readiness/provenance; live wins generic coverage and tasklist-fit. The live weaknesses are specific remediations rather than a dispute needing adversarial arbitration: add a provenance section, make risks enumerator-compatible or update the checker, and enrich the tasklist handoff with concrete backend/file/metric decisions if the eval expects code-level detail.
