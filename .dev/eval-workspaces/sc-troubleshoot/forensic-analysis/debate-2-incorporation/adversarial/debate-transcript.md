# Debate Transcript — Adversarial Run 2 (Incorporation Recommendations)

**Mode**: Mode B inline simulation. 3 advocates (architect / quality-engineer / analyzer) debate which forensic aspects should land in v2.
**Depth**: standard (Round 1 parallel + Round 2 sequential rebuttals + Round 2.5 invariant probe).
**Convergence threshold**: 0.80.
**Focus areas**: workload fit, observed failure modes, cost/leverage, hallucination contract, enforceability.

## Round 1: Parallel Advocate Statements

### Variant 1 (Architect)

Position summary: "Forensic and v2 solve different problems. Most of forensic is wrong for v2's workload. Recommend 3 INCORPORATE (`test_is_wrong`, MCP concurrency cap, hypothesis-card schema test), 2 ADAPT (repeat-failure detection, 3-level adversarial fallback), reject everything else."

Steelman of QE position: "QE will rightly point out that v2's hallucination contract is *behavioral* and the inline-fallback path was exercised in 4 of 8 eval logs. That's a real enforceability gap. The architect concedes that the schema-conformance idea is broader than just hypothesis-card — REPORT.md and audit-log also deserve schemas."

Steelman of analyzer position: "Analyzer will rightly note that several of my ADAPTs (repeat-failure detection, stale-codebase) are mitigations for problems v2 hasn't observed yet. Frequency-weighted, only the ones with observed-or-imminent failure modes should ship first."

Concession: my 2 ADAPTs (repeat-failure detection, coordinated fallback) may be over-scoped for the immediate roadmap. The analyzer's "do the smallest thing that addresses an observed failure mode" framing is the right ordering principle.

### Variant 2 (Quality Engineer)

Position summary: "v2's behavioral contracts are good but under-defended. The eval evidence shows fallbacks firing more than expected. Recommend 5 INCORPORATE (audit-log schema, MCP cap, repeat-failure, JSON schema for output contract, `test_is_wrong`), 3 ADAPT (3-level fallback chain, stale-codebase detection, named degradation modes)."

Steelman of architect position: "Architect is right that workload mismatch dominates the diff. Importing forensic's pipeline topology would be a disaster. I agree with the REJECT majority. My quarrel is with the size of the INCORPORATE list — architect is too conservative."

Steelman of analyzer position: "Analyzer is right that JSON-schema for output contract and named degradation modes are *theoretical* failure-mode mitigations not yet demonstrated in evals. I concede they may belong in a P2 / follow-up list rather than the initial incorporation roadmap."

Concession: my 3 ADAPTs (stale-codebase detection, named degradation modes, full JSON Schema) are defense-in-depth without observed failure modes driving them. Frequency-weighting them down to follow-ups is honest.

### Variant 3 (Analyzer)

Position summary: "Frequency-weight against observed eval failure modes. 4 INCORPORATE (audit-log normalization, `test_is_wrong`, MCP cap, repeat-failure detection), 1 ADAPT (single-agent scoring fallback before 'pick highest-confidence'), reject everything else."

Steelman of architect position: "Architect's REJECT list is well-anchored to workload mismatch. The 3 INCORPORATEs overlap mine (MCP cap, hypothesis-card schema, `test_is_wrong`). Where we differ: architect frames hypothesis-card schema as a single test, I frame audit-log as the higher-leverage schema. Both are right — they're complementary, not competing."

Steelman of QE position: "QE's defense-in-depth instinct is correct in general. The disagreement is *prioritization*. QE wants all 5 INCORPORATE + 3 ADAPT now. I want 4 INCORPORATE + 1 ADAPT now with the rest deferred until eval evidence shows the latent failure mode firing."

Concession: my "wait for failure modes to fire" principle is risk-tolerant. For security-critical fields (`test_is_wrong`), missing the failure mode once is asymmetrically bad. The QE's case for shipping that flag without waiting is sound, and we agree on it.

## Round 1 Scoring Matrix (per-diff verdict)

Using the 31 differences as the diff-point space, augmented by the cross-variant proposals:

| Item / Diff | Architect | QE | Analyzer | Unanimous? | Verdict |
|---|---|---|---|---|---|
| `test_is_wrong` flag (C-012) | INCORPORATE | INCORPORATE | INCORPORATE | YES | INCORPORATE |
| MCP per-server cap (C-008) | INCORPORATE | INCORPORATE | INCORPORATE | YES | INCORPORATE |
| Hypothesis-card schema test (C-013 subset) | INCORPORATE | INCORPORATE | (broader: audit-log) | majority | INCORPORATE |
| Audit-log schema (analyzer's #1; QE's #1 augmented) | (silent) | INCORPORATE | INCORPORATE | majority | INCORPORATE |
| Repeat-failure detection in Wave 0 (U-004 adapted) | ADAPT | INCORPORATE | INCORPORATE | majority lean-INCORPORATE | INCORPORATE |
| 3-level adversarial fallback (C-014) | ADAPT | ADAPT | ADAPT | YES | ADAPT |
| JSON Schema for output contract (QE-only) | (silent / reject) | INCORPORATE | DEFER | split | DEFER |
| Stale-codebase detection (QE-only) | (silent) | ADAPT | REJECT | split | DEFER |
| Named degradation modes (QE-only) | (silent) | ADAPT | DEFER | split | DEFER |
| Orchestrator-as-dispatcher (U-003) | REJECT | REJECT | REJECT | YES | REJECT |
| 8-phase pipeline (C-003) | REJECT | REJECT | REJECT | YES | REJECT |
| Subprocess pipeline (C-004) | REJECT | REJECT | REJECT | YES | REJECT |
| Sprint-runner integration (C-015/U-002) | REJECT | REJECT | REJECT | YES | REJECT |
| Always-debate (C-009) | REJECT | REJECT | REJECT | YES | REJECT |
| `--tier × --depth` 2-axis (C-010/U-001) | REJECT | REJECT | REJECT | YES | REJECT |
| Heavyweight test infra (C-013 full) | REJECT (adopt subset) | REJECT (adopt subset) | REJECT (adopt subset) | YES | REJECT (with schema subset adopted) |
| Token-budget table per phase (C-011) | (silent) | (silent) | REJECT | majority lean-REJECT | REJECT |
| Selective git rollback (forensic FR-TFEP-10) | implicit REJECT | implicit REJECT | REJECT | YES | REJECT |
| Worktree isolation (NFR-008) | implicit REJECT | implicit REJECT | REJECT | YES | REJECT |
| Scope-of-problems (C-001) | REJECT | REJECT | REJECT | YES | REJECT |
| Tier/phase structure (C-003) | REJECT | REJECT | REJECT | YES | REJECT |
| Activation mechanism (C-002) | SHARED (v2 already broader) | SHARED | SHARED | YES | SHARED — v2 better fit |
| Adversarial coupling pattern (C-009) | REJECT | REJECT | REJECT | YES | REJECT — v2 skip-on-consensus better |
| Hallucination contract (C-016 + U-003 + U-005) | SHARED (different approach, equivalent) | partial-ADAPT (`evidence-validator` retry policy) | SHARED | majority SHARED | SHARED — orthogonal |
| Remediation chain (C-017) | REJECT | REJECT | REJECT | YES | REJECT — v2 diagnosis-first is correct |
| Output contract (C-012 minus `test_is_wrong`) | SHARED | partial-ADAPT (JSON Schema) | SHARED | majority SHARED | SHARED |
| Lifecycle/checkpointing (C-018, U-004) | partial-ADAPT (repeat-detect) | partial-ADAPT | partial-ADAPT | YES | ADAPT (repeat-failure detection only) |
| CLI / sprint-runner integration (C-015) | REJECT | REJECT | REJECT | YES | REJECT |
| Refs strategy (S-003, U-006) | SHARED (v2 already lazy) | SHARED | SHARED | YES | SHARED — v2 better |
| Model tiering (C-007) | REJECT | REJECT | REJECT | YES | REJECT — v2 simpler |
| MCP usage by phase (C-008) | INCORPORATE (cap only) | INCORPORATE (cap only) | INCORPORATE (cap only) | YES | INCORPORATE (cap subset) |
| Test strategy (C-013) | INCORPORATE (schema only) | INCORPORATE (broader schemas) | INCORPORATE (audit-log focus) | majority | INCORPORATE (subset) |
| Failure handling (C-014) | ADAPT | ADAPT | ADAPT | YES | ADAPT |
| Shared assumption A-001 (adversarial-as-adjudication) | NO ACTION | NO ACTION | NO ACTION | YES | NO ACTION (acknowledged) |
| Shared assumption A-002 (single Markdown report) | NO ACTION | NO ACTION | NO ACTION | YES | NO ACTION (acknowledged) |

Round 1 convergence: 28 of 33 voting items (85%) reached majority or unanimous agreement. Above the 0.80 threshold.

## Round 2: Sequential Rebuttals

### Architect rebuttal

Reviewing QE's case: agree that audit-log schema is higher-leverage than hypothesis-card alone — concede the broader schema scope. Agree to upgrade my "ADAPT: repeat-failure detection" to INCORPORATE (analyzer's frequency framing is correct — users do re-run, and there's no current mechanism). My JSON Schema concern: it's a complete output-contract rewrite for a problem (caller-side parse breakage) that isn't observed in evals. DEFER vote stands.

Reviewing analyzer's case: agree to drop my coordinated-fallback ADAPT down to "single-agent intermediate retry only" — the 3-level chain is over-engineered for v2's failure surface. Agree that stale-codebase detection without a resume primitive is premature.

Updated architect position: 4 INCORPORATE (test_is_wrong, MCP cap, hypothesis-card schema, audit-log schema), 2 ADAPT (repeat-failure detection — *upgraded* to INCORPORATE; single-agent adversarial fallback — kept as ADAPT). DEFER on JSON Schema. Drop stale-codebase to deferred.

### QE rebuttal

Reviewing architect's case: agree my JSON Schema and named-degradation-modes proposals lack observed failure modes. Concede those to DEFER. The audit-log schema (#1) is the right minimal first step — it's the highest-friction observed gap.

Reviewing analyzer's case: agree that frequency-weighting is the right ordering principle. My 5+3 list compresses to 5 INCORPORATE + 1 ADAPT when DEFERs are pulled out.

Updated QE position: 5 INCORPORATE (audit-log schema, MCP cap, repeat-failure detection, `test_is_wrong`, hypothesis-card/REPORT schema-conformance test), 1 ADAPT (3-level → 2-level adversarial fallback chain). DEFER on JSON Schema, stale-codebase detection, named-degradation modes.

### Analyzer rebuttal

Reviewing architect's case: convergence achieved on the 4 INCORPORATE set. Architect's concession on upgrading repeat-failure to INCORPORATE is the key alignment point — we now agree on all 4 of my original INCORPORATEs.

Reviewing QE's case: QE has dropped JSON Schema, stale-codebase, named-degradation modes to DEFER. That removes the substantive Round 1 disagreement.

Updated analyzer position: unchanged. 4 INCORPORATE + 1 ADAPT.

## Round 2 Convergence Check

| Item | Architect | QE | Analyzer | Verdict |
|---|---|---|---|---|
| `test_is_wrong` | INCORPORATE | INCORPORATE | INCORPORATE | UNANIMOUS INCORPORATE |
| MCP per-server cap | INCORPORATE | INCORPORATE | INCORPORATE | UNANIMOUS INCORPORATE |
| Hypothesis-card schema test | INCORPORATE | INCORPORATE | INCORPORATE (via audit-log inclusion) | UNANIMOUS INCORPORATE |
| Audit-log schema | INCORPORATE | INCORPORATE | INCORPORATE | UNANIMOUS INCORPORATE |
| Repeat-failure detection (Wave 0) | INCORPORATE (upgraded) | INCORPORATE | INCORPORATE | UNANIMOUS INCORPORATE |
| Single-agent adversarial fallback | ADAPT | ADAPT | ADAPT | UNANIMOUS ADAPT |
| JSON Schema for output contract | DEFER | DEFER | DEFER | UNANIMOUS DEFER |
| Stale-codebase detection | DEFER | DEFER | DEFER | UNANIMOUS DEFER |
| Named degradation modes | DEFER | DEFER | DEFER | UNANIMOUS DEFER |
| All REJECTs | REJECT | REJECT | REJECT | UNANIMOUS REJECT |
| Hallucination contract | SHARED-orthogonal | SHARED-orthogonal | SHARED-orthogonal | UNANIMOUS SHARED |
| A-001, A-002 | NO ACTION | NO ACTION | NO ACTION | UNANIMOUS NO ACTION |

Round 2 convergence: 33 of 33 voting items (100%) reached unanimous agreement after rebuttals.

## Round 2.5: Invariant Probe (sufficiency-challenge focus)

**Fault-finder agent**: independent of advocates, runs 6-category checklist against the emerging consensus.

### Category 1 — State variables
- Are we assuming the prior-pass detection (#5) doesn't false-positive on different-but-similar symptoms? **ASSUMED unaddressed**. Mitigation: chat notice + user-overridable. Severity: MEDIUM.

### Category 2 — Guard conditions
- Are we assuming `test_is_wrong` detection rule won't fire on legitimate "fix the test by adjusting the expectation to match a deliberate API change"? **ASSUMED unaddressed**. Mitigation: detection rule should require explicit signal ("the test's expected value is wrong" vs "the test is brittle"). Severity: MEDIUM.

### Category 3 — Count divergence
- MCP cap ≤3 — does the cap count per-server or per-invocation? **ASSUMED ambiguous**. Forensic spec says ≤3 simultaneous per server regardless of `--concurrency` (`forensic-spec.md:2127`). We must specify the same. Severity: LOW.

### Category 4 — Collection boundaries
- What if 4 hypothesis agents × 1 MCP query each = 4 simultaneous, exceeding the ≤3 cap? **ADDRESSED**: agents serialise within their brief.
- What if `repeat_invocation_count` matches a stale prior run from days ago? **UNADDRESSED**: 24-hour TTL on detection (analyzer's #4 spec).

### Category 5 — Interaction effects
- Does repeat-failure detection + `--depth deep` force interact with `--no-escalate`? **UNADDRESSED**. Resolution: `--no-escalate` always wins. Severity: MEDIUM.
- Does `test_is_wrong` interact with `--fix` flow (does the remediation chain do the right thing when the fix is "modify the test")? **UNADDRESSED**. Resolution: yes — task-builder gets the same input regardless. The remediation flow doesn't branch on `test_is_wrong`; only the caller does. Severity: LOW.

### Category 6 — Sufficiency challenge (always-on)
The claim: "incorporating these 5 INCORPORATE + 1 ADAPT *reliably improves* v2's effectiveness for symptom-driven debugging."

- Sufficiency check: is there a downstream condition that, if true, would falsify the claim?
  - **Condition 1 (downstream)**: an `evidence-validator` failure mode that isn't surfaced by `audit-log schema` normalization. If the validator silently degrades (returns success but skipped citations), the schema-normalized audit log won't catch it. **PARTIAL SUFFICIENCY**. The audit-log schema covers format conformance, not content quality. Mitigation: not addressed by this incorporation round. Severity: HIGH if real, MEDIUM in expected probability.
  - **Condition 2 (downstream)**: `test_is_wrong` flag is added but no caller consumes it. **NON-FATAL**: additive, becomes useful when callers want it. Severity: LOW.
  - **Condition 3 (downstream)**: repeat-failure detection's 24h TTL is too narrow for users who re-investigate the same flaky test weekly. **PARTIAL**: misses some legitimate repeats. Mitigation: configurable TTL (defer to follow-up). Severity: LOW.
  - **Condition 4 (downstream)**: MCP cap is enforced in prompt but not in code — an agent could violate it. **PARTIAL**: prompt-only enforcement. Same as forensic. Mitigation: schema-conformance test that asserts MCP-query batching. Severity: MEDIUM.

- Evidence-citation requirement: for each branch above, is there a Stage-1 branch-trace or source enumeration backing the sufficiency claim? **NO BRANCH TRACE**. The evidence is the 8 eval audit logs + the forensic spec. Source enumeration: I have enumerated the 5 INCORPORATE + 1 ADAPT changes against the 8 eval cases and found no observed failure mode that would be missed; but I have not enumerated the *unobserved* failure modes that might fire post-incorporation. **Partial-sufficiency acknowledged**.

### Invariant Probe Summary

| INV-NNN | Category | Assumption | Status | Severity |
|---|---|---|---|---|
| INV-001 | guard_conditions | `test_is_wrong` won't false-fire on deliberate test changes | UNADDRESSED | MEDIUM |
| INV-002 | state_variables | repeat-failure detection won't false-positive | UNADDRESSED | MEDIUM |
| INV-003 | count_divergence | MCP cap counts per-server-simultaneous, not per-invocation | UNADDRESSED | LOW |
| INV-004 | collection_boundaries | 24h TTL boundary for repeat detection | UNADDRESSED | LOW |
| INV-005 | interaction_effects | `--no-escalate` × repeat-failure × `--depth deep` priority | UNADDRESSED | MEDIUM |
| INV-006 | sufficiency_challenge | Incorporation reliably improves v2 (with caveats) | UNADDRESSED | MEDIUM |

No HIGH-severity UNADDRESSED items. Convergence is not BLOCKED by invariant gate.

The 5 MEDIUM items are surfaced in the incorporation report as "implementation gotchas" — they must be addressed in the change spec but they don't block convergence on the incorporation roadmap itself.

## Final convergence: 100% unanimous on incorporation set; 5 MEDIUM invariant items flagged as implementation gotchas

No HIGH-severity invariants block convergence. The incorporation roadmap proceeds.
