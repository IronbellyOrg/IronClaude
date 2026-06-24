# R5 Reproduction Summary

**Captured:** 2026-06-02 06:58
**Raw output:** `phase-outputs/test-results/r5-repro-output.txt`

## Fixtures Used

### Prescribed identical-set fixture (Step 2.3 as written)
- `r5-repro-spec.md` — `## Requirements`: "Milestone deliverables: M1-D01, M1-D02, M2-D01, M2-D02, M3-D01."
- `r5-repro-roadmap.md` — `## Implementation`: "implementing M1-D01, M1-D02, M2-D01, M2-D02, M3-D01."

**Tokenizer extract (both files):** `{'D': ['D01', 'D02']}` — FIVE distinct milestone deliverables collapse to TWO bare-`D` tokens (`M1-D01`/`M2-D01`/`M3-D01` → `D01`; `M1-D02`/`M2-D02` → `D02`). Milestone scope is destroyed.

**`check_signatures` result:** `total findings: 0`.

**Interpretation:** When spec and roadmap use the SAME milestone IDs, the mis-tokenization is *symmetric* — both collapse to `{D01, D02}`, so they match and no phantom is raised. The defect here is **silent**: 5 distinct deliverables are under-counted to 2 and `M1-D01` vs `M2-D01` are indistinguishable, but no finding surfaces. This is itself a correctness problem (the checker cannot tell milestones apart), but it does not by itself produce the HIGH phantom_id incident.

### Asymmetric milestone probe (surfaces the HIGH phantom_id — the PR #111 incident class)
The real-world FP (PR #111's "51 HIGH phantom_id") arises under spec/roadmap **asymmetry**, which is the normal case (a roadmap enumerates more per-milestone deliverables than the spec's summary):
- Spec `## Requirements`: "Deliverables M1-D01, M2-D01, M3-D01." → extract `{'D': ['D01']}` (all three collapse to D01)
- Roadmap `## Implementation`: "Plan M1-D01, M1-D02, M2-D03." → extract `{'D': ['D01', 'D02', 'D03']}`

**`check_signatures` result:** `total findings: 2`, **HIGH phantom_id count: 2**
```
rule_id=phantom_id severity=HIGH roadmap_quote='D02' spec_quote='[MISSING]'
rule_id=phantom_id severity=HIGH roadmap_quote='D03' spec_quote='[MISSING]'
```

**Interpretation:** `M1-D02` and `M2-D03` are perfectly legitimate milestone-scoped deliverable IDs. The milestone-blind bare-`D` tokenizer strips their `M{n}-` prefix, reads them as bare `D02`/`D03`, finds those tails absent from the spec's collapsed `{D01}`, and raises **2 HIGH `phantom_id` false-positives** (`spec_quote='[MISSING]'`). Scale this to a real roadmap with dozens of `M{n}-D{nn}` deliverables and you reproduce PR #111's 51-HIGH incident exactly.

## Determination

**The false-positive REPRODUCES on the current branch.** The milestone-prefixed `M{n}-D{nn}` IDs are mis-tokenized as bare-`D` requirement IDs, causing (a) silent milestone-scope collapse in the symmetric case and (b) **HIGH `phantom_id` false-positives** in the realistic asymmetric case. This is genuine, evidence-backed, and attributable directly to milestone-ID mis-tokenization (the contracts SoT has no `MD` family). → **Decision input: PROCEED (path b).** The Phase 3 decision artifact will record PROCEED, and the Phase 2.4 scoping determination selects whether the MD family alone suffices or the allowlist port is also needed.
