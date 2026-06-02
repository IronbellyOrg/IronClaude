# Debate Transcript — Proposal A vs Proposal B

## Metadata
- Depth: standard (Round 1 positions + Round 2.5 independent fault-finder invariant probe)
- Convergence: 1.00 (both the analysis and the independent fault-finder converge on A-with-modifications)
- Fault-finder: independent agent, adversarial stance, zero-trust source verification (agentId a0ecff291e90d2dec)

## Round 1 — Positions

### Advocate A (relocate one canonical parser)
- Strength: zero dispatch change; satisfies Contract #6 (one parser → no divergence) and §MVR §1 (cross-step state via envelope) with the smallest possible blast radius.
- Steelman of B: if MANY checks needed a prior step's frontmatter at gate time, a shared envelope-aware dispatch would be the clean substrate.
- Critique of B: the antecedent is false — the 24 checks validate their own file; B's shared-substrate widening is unjustified and infeasible without generic-pipeline surgery.

### Advocate B (thread envelope into dispatch)
- Strength: most literal satisfaction of 11.2(d) "consumers read envelope.frontmatter, no re-parsing."
- Steelman of A: A's in-gate checks still parse markdown, technically not "dependency injection."
- Concession: requires widening a shared dataclass (8 modules) + changing the generic gate dispatch (shared w/ sprint) + a control-flow reorder.

## Round 2.5 — Independent Fault-Finder Invariant Probe (the decisive pass)

Verified against real source (file:line), not the proposal docs:

| INV | Category | Finding | Status | Severity |
|---|---|---|---|---|
| INV-001 | state_variables | At gate time the envelope reaches no semantic check (`pipeline/gates.py:84`; `pipeline/executor.py:267` passes none; `execute_pipeline` L63 has no envelope param) | confirms B infeasible-as-local | HIGH (vs B) |
| INV-002 | guard_conditions | `code_assertions` skipped entirely when envelope is None (`gates.py:94-98`); only CodeAssertion gets envelope (`gates.py:100`) | tier separation real | HIGH (vs B) |
| INV-003 | collection_boundaries | All 24 `_parse_frontmatter` callsites validate the file being gated; 9 sampled (incl. the cross-gate-sounding `_deviation_counts_reconciled` → cross-FIELD within same artifact, not cross-step). **Zero need cross-step state.** | A sufficient | HIGH (vs B) |
| INV-004 | interaction_effects | `SemanticCheck(` constructed **63×** across **8 modules**; sprint uses `gate_passed` (`sprint/executor.py:834,842`) | B blast radius = 8 modules + sprint | HIGH (vs B) |
| INV-005 | sufficiency_challenge | **Falsifying condition FOUND:** adding `frontmatter` field breaks `tests/roadmap/test_pipeline_envelope.py:312` (8-field §MVR §1 canon); envelope `frozen=True`; **zero `envelope.frontmatter` consumers**. Indicts A-step-2 AND B-step-6 AND task Step 11.2(a). | A can shed it; B cannot | HIGH (both, but removable only from A) |

### Fault-finder verdict (verbatim summary)
"A-with-modifications. Confidence 88/100. DROP A's step 2 (the frontmatter field) — unnecessary (24 checks parse their own content), zero consumers, breaks the 8-field test. Keep the parser-function relocation, the 24-callsite repoint, the duplicate-parser deletions, the consistency test, and the CodeAssertion escape hatch. Zero of the 24 need cross-step state, so the entire justification for B evaporates; B is unjustified blast radius coupled to the same illegal field it cannot shed."

### Independent re-verification by orchestrator (zero-trust)
Confirmed `test_field_set_matches_mvr_section_1` body asserts exactly the 8 canonical fields (`test_pipeline_envelope.py:312-329`); `PipelineEnvelope` `@dataclass(frozen=True)` (`envelope.py:127`); `grep -rn "\.frontmatter" src/superclaude/cli/` → 0 consumers.

## Scoring Matrix (per diff point)

| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001..S-004 (dispatch/ordering/substrate) | A | 95% | INV-001/002/004 — B touches 8 modules + sprint + generic executor |
| S-005 (in-gate data source) | A | 90% | INV-003 — all 24 are local self-validators |
| A-001 (frontmatter field) | NEITHER (drop it) | 95% | INV-005 — breaks test_pipeline_envelope.py:312; zero consumers |
| Tier model fit | A | 92% | INV-002 — CodeAssertion is the sanctioned envelope-aware tier |

## Convergence Assessment
- All taxonomy levels covered (L1 wording, L2 architecture/dispatch, L3 state/guard/sufficiency).
- HIGH-severity UNADDRESSED invariants against the WINNER (A′): none. The one HIGH finding (INV-005) is RESOLVED by dropping the field from A.
- Status: CONVERGED on **A′ = Proposal A minus the envelope `frontmatter` field**.
