# FR-RSR UC-2 — 3×-Before / 3×-After Comparison

Date: 2026-06-20
Measurement depth: `--depth quick` (Wave 1A tagger→sweep→contract emission is depth-independent;
quick skips only the Tier-2 reviewer ensemble, cutting per-run cost ~3×).
BEFORE skill = pre-strengthening snapshot (`skill-before-strengthening/.claude`, contract 1.6.0).
AFTER skill = strengthened worktree `.claude` (adds the mandatory six-field-emission rule in §9.1/§6.1).
Fixture 39 (dynamic-dispatch) was rewritten to a genuine registry/string-dispatch case for BOTH sides.

## Headline: full-pass (all assertions in a rep pass) across 3 reps

| Case | Verdict path | BEFORE | AFTER |
|------|--------------|--------|-------|
| uc2-surface-positive-control | REACHED | 0/3 | 0/3 |
| uc2-surface-dynamic-dispatch | DEGRADE | 0/3 | 1/3 |
| uc2-surface-test-only-ref | UNREACHED | 0/3 | 0/3 |

## Per-assertion pass counts (passed-reps / 3)

### positive-control (REACHED)
| Assertion | BEFORE | AFTER |
|-----------|--------|-------|
| Reachable surface emits zero unreached symbols (`runtime_surface_unreached == 0`) | 0/3 | 0/3 |
| Reachable positive control does not degrade (`runtime_surface_degraded == false`) | 0/3 | 0/3 |
| No unreached/STOP escalation marker in REPORT (regex_absent) | 3/3 | 3/3 |

### dynamic-dispatch (DEGRADE — rewritten registry fixture)
| Assertion | BEFORE | AFTER |
|-----------|--------|-------|
| Degrades instead of UNREACHED (`runtime_surface_degraded == true`) | 0/3 | 1/3 |
| Never counted as UNREACHED (`runtime_surface_unreached == 0`) | 0/3 | 1/3 |
| No false Regression (regex_absent) | 0/3 | 2/3 |

### test-only-ref (UNREACHED)
| Assertion | BEFORE | AFTER |
|-----------|--------|-------|
| Classified UNREACHED (`runtime_surface_unreached >= 1`) | 0/3 | 0/3 |
| Count invariant `len(unreached_surfaces) == runtime_surface_unreached` | 0/3 | 0/3 |
| Finding surfaced in REPORT (regex_present) | 2/3 | 1/3 |

## Conclusion: prose forcing is necessary but NOT sufficient

The strengthening did not materially move the structured-field assertions. Across all three
quiet-path cases the model continued to emit semantically-correct verdicts under **ad-hoc field
names** instead of the canonical six, even though the strengthened SKILL.md explicitly forbids
exactly those names. Verified the strengthened skill WAS loaded (fixture `.claude` symlink →
worktree, `grep -c "MANDATORY EMISSION"` = 1) — so this is genuine model non-compliance, not a
harness/skill-loading artifact.

Observed ad-hoc field names the model invents on the quiet paths:
- REACHED → `runtime_surface_reachable: true`, `runtime_surface_evidence:`, `verdict: reachable`
- DEGRADE → `surface_reachability_verdict: DEGRADE`, `surface_reachability_explicitly_not: [...]`
- UNREACHED (non-escalating) → `surface_production_reachable: false`, `unreachable_surfaces:`

The ONE place the model reliably emits the canonical field is `runtime_surface_unreached` on the
**escalating** UNREACHED headline (case 37, validated 3/3 earlier) — because that field drives the
§5.3 forbid-STOP pre-filter the model actively engages. On non-escalating/quiet paths it improvises.

The dynamic-dispatch improvement (0/3 → 1/3) is real but (a) largely fixture-driven — the rewrite
to a genuine registry/string-dispatch case made DEGRADE unambiguous so the model now reasons it
correctly — and (b) still inconsistent (1 of 3 reps emits the canonical `runtime_surface_degraded`).

## Recommended fix (structural, not more prose)

Make the LEDGER the source of truth and DERIVE the six contract fields deterministically, instead of
asking the model to hand-emit counterintuitive count/boolean fields:

1. The model already emits a natural reachability verdict per symbol (`REACHED|DEGRADE|UNREACHED`)
   in `runtime-surface-ledger.yaml` (which IS written reliably — see the headline ledger). Treat the
   ledger as authoritative.
2. Add a deterministic normalization step (in the protocol's contract-assembly, or in the grader as
   a derived check) that computes `runtime_surface_unreached`, `runtime_surface_degraded`,
   `unreached_surfaces`, etc. FROM the ledger rows — so the contract fields are mechanical, not
   model-typed.
3. Keep the prose rule (it's correct and cheap) but stop relying on it as the sole guarantee.

This is a FR-RSR.7 contract-shape change and a design decision for the user; it is the path that
would make the structured-field assertions pass reliably.

## Measurement caveats (disclosed honestly)

1. **`--depth quick` confounds the escalating paths.** Quick pins Tier 1, suppressing the §5.3
   forbid-STOP escalation and §10.6 Grounding-Gap machinery that, at standard depth, lead the model
   to engage the canonical `runtime_surface_unreached` field. Evidence: the headline (37) graded 3/3
   at `--depth standard` (canonical `runtime_surface_unreached: 1`) but 2/3 at `--depth quick`
   (`tier_reached: 1`, field not emitted); degraded-backend (40) graded 4/4 standard vs 2/4 quick.
   So the quick before/after is cleanly valid ONLY for the NON-escalating REACHED (38) and DEGRADE
   (39) cases — which is exactly where the robust "prose insufficient" finding sits. The
   UNREACHED/escalating conclusion is depth-sensitive and should be re-measured at standard depth
   before being treated as final. The BEFORE arm was also quick, so the comparison stays apples-to-apples.

2. **The headline fail-pre fixture telegraphs the requirement.** With the harness contamination
   fixed (no `.claude` symlink on the old run), the v1 baseline STILL does not clean-pass — but
   because the tasklist's Task 3 literally says "ensure production-reachable," even the FR-RSR-free
   v1 skill flags the gap just by reading the tasklist. The original FR-S9-04 incident passed
   *because the reachability requirement was implicit* (green tests + existing symbol). A faithful
   fail-pre fixture must state the surface requirement implicitly (e.g. "user can invoke Spawn from
   /ai") WITHOUT a "make it production-reachable" checklist item, so v1 clean-passes and only the
   FR-RSR skill catches it. As written, the headline is not a pure falsifier.

## Net assessment

- **Robust (depth-independent):** on the REACHED path, prose strengthening did NOT fix field-name
  fidelity — the model emits `runtime_surface_reachable: true` regardless. Core result.
- **Works at standard depth:** the escalating UNREACHED headline emits the canonical field (37 = 3/3
  standard) and degraded-backend behaves (40 = 4/4 standard) when the protocol machinery runs.
- **Two follow-ups before FR-RSR.10 can pass:** (a) derive the six contract fields from the ledger
  deterministically (structural fix for quiet-path improvisation); (b) rewrite the headline tasklist
  to state reachability implicitly so it is a true fail-pre falsifier; then re-measure at standard depth.

## DECISIVE CORRECTION — the ledger is ALSO unreliable (ledger-derivation is not viable)

Post-experiment check of the `runtime-surface-ledger.yaml` across the 9 quiet-path after-runs:
**present in only 1 of 9** (after-r2/dynamic-dispatch). On REACHED/DEGRADE/non-escalating runs the
model writes NO ledger under any name — reachability lives only in REPORT.md prose + the improvised
`contract.yaml` field. So the proposed "derive the six contract fields from the ledger" fix is NOT
viable: the ledger is the very artifact that goes missing.

Root cause (now complete): the LLM only fully engages the structured FR-RSR machinery (ledger +
canonical contract scalars) when there is an ALARMING UNREACHED that ESCALATES (the headline at
standard depth). On quiet paths it does a lighter reflection — correct VERDICT in prose, but no
ledger and improvised scalar names. Neither prose forcing nor ledger-derivation can fix this,
because both depend on the LLM reliably emitting a structured artifact it skips on quiet paths.

**What this means for FR-RSR's architecture:** the TDD framed FR-RSR as "LLM-free, deterministic,"
but it was IMPLEMENTED as SKILL.md prose executed by an LLM. The experiment proves a prose-only
feature cannot deliver the deterministic structured-output guarantee. The only robust fix is a
DETERMINISTIC (Python) implementation of the sweep — tagger + production-caller partition + degrade
oracle + rootwalk → always writes the ledger and the six contract scalars from static analysis,
removing the LLM from the structured-emission path. That is a major re-scope (a code feature, not a
prose feature), well beyond this task's SKILL/refs/eval inventory.

**Good news — the SAFETY GOAL is met at the prose/verdict level:** across every run the skill
reliably caught the unwired/registry/test-only surface and did NOT clean-pass it (the original
FR-S9-04 blind spot — clean-passing an unwired surface — is closed). What is unreliable is the
STRUCTURED CONTRACT MIRROR that downstream consumers (§5.3 pre-filter, sprint executor) read.

Genuine options (user decision):
1. Re-scope FR-RSR's structured fields to ADVISORY; assert the eval on the reliably-emitted REPORT
   prose finding (the skill never clean-passes the unwired surface). Keeps it a prose feature with
   honest, achievable acceptance. Smallest.
2. Implement a deterministic Python sweep (new TDD/task) that always emits the ledger + scalars.
   Largest; the only way the structured contract fields become reliable for consumers.
3. Hybrid: keep the escalating-UNREACHED gate (works at standard depth) as the hard behavior; make
   REACHED/DEGRADE structured fields advisory.

## Artifacts

- before-r{1,2,3}, after-r{1,2,3} iterations under `.dev/eval-workspaces/sc-reflect/iterations/`
- machine comparison: `.dev/eval-workspaces/sc-reflect/iterations-before-after-comparison.json`
- aggregator: `phase-outputs/plans/aggregate_before_after.py`
