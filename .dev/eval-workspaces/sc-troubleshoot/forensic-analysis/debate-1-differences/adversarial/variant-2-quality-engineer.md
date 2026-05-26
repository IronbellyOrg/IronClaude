# Variant 2 — Quality-Engineer Advocate Card

**Stance**: testability / determinism / edge-case-completeness / schema-rigor framing
**Output**: catalogue of differences in evidence/validation/test infrastructure
**Mandate**: surface differences that shape verification fidelity; debate-relevant for evidence-grounding and falsifiability

## Position summary

The two designs diverge most sharply on *how a claim becomes evidence*. The forensic design treats evidence as a schema obligation: every hypothesis MUST have `file:line` excerpts (`forensic-spec.md:1906-1915`), the Hypothesis Finding Schema is normative, Phase 6 reads only 6 summary artifacts (architectural restriction), and the test strategy gates 58 success criteria SC-001-SC-058 at M6. The v2 bundle treats evidence as a *post-hoc* validation: agents produce hypothesis cards with self-reported confidence; an independent `confidence-calibrator` re-grades each card against the 5-dimension rubric (stripped of formation context); a dedicated `evidence-validator` agent re-Reads every cited line and drops mismatches before REPORT.md ships. Both are evidence-first regimes, but they enforce it differently — schema-up-front vs validator-at-the-end.

## Steelman of the forensic design (Variant A)

The strongest version of forensic's evidence approach is the architectural hallucination contract: by construction, the Opus orchestrator cannot fabricate a `file:line` reference because it physically never reads source code — only the summary artifacts Phase 6 is allowed to consume. That is a stronger guarantee than v2's after-the-fact validation, because it removes the *opportunity* for hallucination rather than detecting it. The 100%-evidence-coverage + 100%-falsifiability requirements (`forensic-spec.md:1906-1915`) are also testable in a way v2's "every claim must cite a real `file:line`" is not — forensic's contract has measurable acceptance criteria; v2's contract has a validator agent that might fail.

The forensic test strategy is also explicit in a way v2 isn't. 10 test files (D6.1-D6.13), 6 test types (Smoke/Integration/Edge case/Schema conformance/Security/Manual review), single 5-file synthetic Python fixture engineered to produce ≥2 domains and observable Phase 0 output, canned artifacts per phase boundary at `tests/sprint/forensic/fixtures/canned_artifacts/{phase0,phase2,phase4}_output/`. v2 has eval workspaces but no roadmap test-strategy document, no schema conformance tests against the Hypothesis Card Template, no canned-artifact fixtures.

## QE-relevant differences I am championing as significant

1. **Hallucination contract shape (C-016, U-003) — L3.** Forensic enforces hallucination resistance by *withholding access*: the orchestrator can't lie about `file:line` because it never sees the file. v2 enforces hallucination resistance by *post-hoc validation*: the `evidence-validator` agent independently re-Reads every cited line and drops mismatches. The forensic contract is stronger in steady state (no validator-failure path) but more rigid; the v2 contract is more flexible (the orchestrator can read for synthesis) but trusts the validator path.

2. **Evidence-validator vs no-equivalent (U-005, C-016) — L3.** v2 has a *dedicated agent file* at `src/superclaude/agents/evidence-validator.md`. It has its own model pin (sonnet), permissions (Read/Grep/Glob only — no Bash, no Write to source), and explicit instructions to "drop, not confirm." Forensic does not have a structural analog — its evidence checks are baked into the schema obligations of Phase 1/3 outputs and the Phase 6 dispatcher constraint. v2's approach is more testable (the agent can be unit-tested against fixture reports with known-good/known-bad citations); forensic's is more constraint-based.

3. **Confidence calibration (U-005) — L2.** v2 has a *dedicated `confidence-calibrator` agent*. It re-grades every hypothesis card against the 5-dimension rubric in a context stripped of the hypothesis-formation trail. This is an explicit anchoring-bias mitigation — the calibrator is told the card's self-reported confidence is "a signal, not a number." Forensic doesn't have this layer at all; calibration happens *inside* the adversarial debate's 25-criterion rubric (`forensic-spec.md:2174-2175`).

4. **Test strategy scope (C-013) — L2.** Forensic's 58 success criteria at M6 with 10 test files and per-phase canned-artifact fixtures is a substantially more rigorous test infrastructure than v2's eval-workspace approach. Forensic also gates everything at M6 — no upstream gating. v2's tests are mixed in with the regular project test suite under `tests/` (no special gating).

5. **Schema rigor (C-012) — L2.** Forensic specifies a normative Hypothesis Finding Schema (id pattern `H-\d+-\d+`, evidence as `file:line` excerpts list with quoted snippets, confidence float, falsification criterion, severity enum, category enum). v2 specifies a Hypothesis Card *Template* (Markdown structure) with worked examples, but no machine-parseable schema. Schema vs template is a real divergence — schema is testable for conformance; templates are guidelines.

6. **Falsifiability requirement (C-016) — L3.** Forensic requires every hypothesis to carry a falsification criterion (`forensic-spec.md:1906-1915`). v2's hypothesis-card template includes "If I'm wrong, it's probably because..." (a *next-most-likely* — different semantics from falsifiability). The former is Popperian; the latter is more like a hedge.

7. **Skipped-debate accounting (C-014, C-009).** Forensic's three-level adversarial fallback explicitly emits `debate_status: "skipped"` when the debate is force-aborted (L3 path). v2 skips the debate silently when Wave 3 produces only 1 viable fix or all converge (no special status emitted). The forensic approach has better observability for "no debate was held."

## Concessions

- v2's `evidence-validator` is unambiguously a quality-control gain over self-checking; forensic doesn't have an equivalent in-pipeline.
- v2's "if a citation doesn't survive, the report status drops to `partial`" surface is more honest about what the user can trust than forensic's "100% coverage required" requirement (which forensic can require but can't directly enforce at runtime).
- The lazy-ref-loading + per-wave entry/exit criteria + machine-readable audit header/footer (`SC:TROUBLESHOOT:TARGET`/`SUMMARY` HTML-comment blocks) is a tighter observability surface than forensic's `progress.json` for many testing scenarios.

## If my framing is wrong, it's probably because

I am treating both designs as commensurable on evidence rigor when in fact they sit at different points on the cost-vs-thoroughness curve. Forensic's heavyweight schema infrastructure is appropriate for the project-wide-sweep case it targets; v2's lighter validator+calibrator pair is appropriate for the per-symptom case it targets. Comparing their evidence regimes as if they were competing for the same workload is the wrong axis.
