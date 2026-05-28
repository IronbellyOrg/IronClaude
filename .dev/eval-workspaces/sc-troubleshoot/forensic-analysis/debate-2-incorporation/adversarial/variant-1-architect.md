# Variant 1 — Architect Advocate: Incorporation Recommendations

**Voice**: opus:architect — skeptical of complexity that doesn't pay for itself, partial to invariant preservation, sensitive to over-specification.

## Position summary

The two designs solve different problems. Forensic's core architectural moves (orchestrator-as-dispatcher, subprocess pipeline, sprint-runner integration, 8-phase data-flow contracts) are *correct for forensic's workload* and *wrong for v2's workload*. Importing them would not "harden v2" — it would harm v2 by transplanting cost without transplanting benefit. The honest architect's answer is mostly REJECT, with a handful of narrow ADAPT/INCORPORATE that respect v2's existing shape.

## Steelman of forensic's design

Forensic's strongest single move is **orchestrator-as-dispatcher**: by withholding source-reading from the synthesizer, hallucination becomes architecturally impossible rather than behaviorally mitigated. That is a genuinely cleaner invariant than v2's `evidence-validator` post-hoc approach. Forensic's per-phase data-flow contracts make resume trivial and testing schema-driven. Selective git rollback intersected with causal-files is a smart move when the tool *does* apply code. The 3-tier escalation gradient with `escalation_count` is more disciplined than v2's per-invocation isolation.

## Steelman of v2's design

v2's strongest single move is **conditional escalation with skip-on-consensus**. Tier 1 stops on a 1.0-confidence missing-import in ~60s — forensic's lightest tier still pays Phase 0 recon + Phase 2 debate cost regardless. v2's two-agent hallucination contract (`evidence-validator` for grounding + `confidence-calibrator` for anchoring) addresses both the citation-fabrication failure mode AND the agent-self-grading anchoring bias, which forensic's withhold-access approach does not address. The eval audit logs prove the conditional model works in practice.

## Concrete recommendations

### INCORPORATE (3 items — narrow, low-cost, high-leverage)

1. **`test_is_wrong` flag in the v2 return contract** (from C-012)
   - WHY: Diagnosis tools repeatedly conclude "the test expectation is outdated, not the code" — today that conclusion sits in REPORT.md prose and is invisible to callers. A boolean output field makes it actionable. Cost: trivial (one bool, one detection rule).
   - CHANGE: Add `test_is_wrong: bool` to `SKILL.md:37-54` output contract; add detection rule in Wave 5 ("if diagnosis concludes test expectation outdated, set `test_is_wrong: true`"); add to `troubleshoot.md` output surfacing.
   - RISK: Low. Additive field. Existing callers ignore unknown fields.

2. **Per-server MCP concurrency cap (NFR-010 ≤3)** (from C-008)
   - WHY: v2 has no protection against accidentally launching parallel hypothesis agents that each fire 3 Serena queries simultaneously. The wave 3 fan-out can hit 4×3 = 12 simultaneous Serena calls. Forensic's `≤3 simultaneous per server` is a cheap, enforceable-in-prompt cap.
   - CHANGE: Add to Wave 3 "MCP enrichment in parallel" step (`SKILL.md:176-179`): instruction to issue at most 3 simultaneous calls per MCP server; if 4 hypothesis agents are spawned, sequentialise MCP queries per-server within each agent's brief.
   - RISK: Low. Slightly slower in pathological cases; prevents rate-limit incidents.

3. **Schema-conformance test for hypothesis-card template** (subset of C-013)
   - WHY: `refs/hypothesis-card-template.md` is documentation, not enforced. If an agent emits a card missing a required field, downstream consumers (calibrator, validator, adversarial) silently get less. A single pytest reads each card and asserts required headings/fields are present.
   - CHANGE: Add `tests/skills/sc-troubleshoot-protocol/test_hypothesis_card_schema.py` validating the template's required fields. Add it to the `Makefile`'s `make test` target.
   - RISK: Low. One test file. Doesn't touch runtime behavior.

### ADAPT (2 items — forensic's idea, modified to fit v2)

4. **Escalation-count gradient for repeat invocations** (adapted from U-004)
   - FORENSIC: 3-tier `EscalationState` (light → standard → halt) tracked in-memory per sprint.
   - ADAPT: v2 is interactive, so in-memory per-sprint doesn't apply. Instead: when a user invokes `/sc:troubleshoot` against the *same scope or stack trace* twice in rapid succession (heuristic: same `--scope` or first 100 chars of issue match a prior audit log within 24h), Wave 0 should:
     - Surface a one-line notice: "Previously diagnosed: see [previous REPORT path]. Auto-escalating to `--depth deep`."
     - Force `--depth deep`.
   - CHANGE: Add detection logic to Wave 0 (`SKILL.md:71-105`). Scan `<output-dir-root>/troubleshoot-*` for matching prior runs; if found, emit notice and elevate depth.
   - WHY: Prevents the user from rediagnosing the same symptom with the same shallow tier. Forensic's escalation gradient solves a real ergonomic problem.
   - RISK: Low-medium. Heuristic match may false-positive on different-but-similar symptoms; the notice is informational so user can override.

5. **Coordinated adversarial fallback chain** (adapted from C-014 / forensic's 3-level chain)
   - FORENSIC: 3-level fallback (retry quick → single Sonnet scoring agent 60s/1000-token cap → emit as-is `debate_status: "skipped"`).
   - ADAPT: v2 today says "Pick highest-confidence Tier 2 fix proposal; note in audit and report header" if `sc:adversarial-protocol` fails. That's one fallback level — not a chain. Adopt forensic's tier-2: spawn a single lightweight scoring agent (quality-engineer with rubric) against the competing fixes with a hard token cap, BEFORE falling all the way back to "pick highest-confidence."
   - CHANGE: Modify `SKILL.md:344` error-handling row for `sc:adversarial-protocol` failure: insert intermediate step (single scoring-agent retry, ≤1000 tokens, 60s timeout), keep current "pick highest-confidence" as final fallback.
   - WHY: Adversarial failures are rare but real; a single-agent scoring pass is much higher signal than confidence-ranking. Cost is small relative to a Tier-2 invocation.
   - RISK: Low. Additive intermediate step in an already-rare failure path.

### REJECT (the rest)

Everything else from the 31-diff catalogue should be REJECTED for v2:

- **Orchestrator-as-dispatcher** (U-003): would force v2 to refactor every Wave 0/1/5 into JSON-summary pipelines; the eval evidence shows v2's reader model produces correct, validated reports. The architectural cleanness is real but the cost of conversion (waves redesigned, agents re-shaped, refs re-routed) buys protection against a failure mode v2 already mitigates behaviorally. The orchestrator-token cap is a non-starter for interactive use.
- **8-phase data-flow pipeline** (C-003): would force v2 to always run all phases. Eval-1 missing-import would have run Phase 0 recon, Phase 1 RCA, Phase 2 debate — instead of stopping at Tier 1 confidence 1.0. Cost destruction with no benefit.
- **Subprocess pipeline** (C-004): would force v2 to abandon in-session Task spawning; v2's `evidence-validator` and `confidence-calibrator` are designed for in-session Task. Migrating to subprocess means refactoring agent files, building a runner, and dropping a working evaluation harness.
- **Sprint-runner integration** (U-002, C-015): v2 has no sprint-runner audience. Forensic's `sprint/tfep.py` solves "phase failed → diagnose → re-launch" — v2's user doesn't have a phase to re-launch.
- **Always-debate** (C-009): would force adversarial cost on consensus diagnoses; eval-3 missing-import had confidence 1.0 — adversarial would add ~30-60k tokens with zero new information.
- **Two-axis `--tier × --depth` mode** (C-010, U-001): adds a knob that controls something v2's conditional escalation already controls. Cognitive overhead for users with no new capability.
- **Heavyweight test infrastructure** (C-013 in full): 10 test files, 58 SC, 6 test types, canned fixtures per phase — v2's eval-workspace pattern is more agile for v2's scope. Adopt the schema-conformance idea (see #3 above) but reject the rest.

## Architectural verdict

v2 is, for its workload, already approximately right. Forensic is, for its workload, also approximately right. Importing forensic's core moves into v2 would make v2 worse, not better. The narrow incorporations above are genuine wins; the rest are workload mismatches dressed up as best practices.

Final confidence: 0.88 — high on the 3 INCORPORATEs (these are small additive wins with strong eval-justified motivation), 0.75 on the 2 ADAPTs (the heuristics need calibration), 0.92 on the REJECT verdicts (the workload mismatch is concrete and demonstrated by the eval evidence).
