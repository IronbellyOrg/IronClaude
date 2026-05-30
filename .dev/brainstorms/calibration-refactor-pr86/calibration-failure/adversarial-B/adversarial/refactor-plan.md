# Refactoring Plan — Merge of A/B/C Theories into Unified Output

Base: **Variant B** (sc:reflect-degraded; combined 0.983)

## Plan

### Change 1 — Adopt B's three core theories as M1/M2/M3
- **Source**: B B1/B2/B3
- **Target**: Merged §2 "Three Theories"
- **Rationale**: B has the highest per-theory confidences and cleanest equation-shaped fixes (base-selection §Combined Score)
- **Integration approach**: Direct adoption with theory names neutralized to M1/M2/M3
- **Risk**: Low

### Change 2 — Add C2 (eval suite silent-green) as Theory M4
- **Source**: Variant C, Theory C2
- **Target**: Merged §2, new theory M4 after M3
- **Rationale**: Unique non-rubric guardrail mechanism (debate U-001 winner at 1.0 confidence); pin-test prescription is mechanically enforceable
- **Integration approach**: Add as fourth theory clearly labeled "GUARDRAIL" tier to distinguish from M1-M3 mechanism theories
- **Risk**: Low

### Change 3 — Add A's cross-theory implications section
- **Source**: Variant A, "Cross-theory implications" (lines 88-94)
- **Target**: Merged §3 "Cross-theory implications"
- **Rationale**: Unique multiplicative-compounding insight (T1×T2) and T3-upstream framing (debate U-003 winner at 1.0)
- **Integration approach**: Adopt verbatim structure; update theory IDs from T/B/C to M1-M4
- **Risk**: Low

### Change 4 — Strengthen substrate-vs-H3 fidelity caveat from A
- **Source**: Variant A, final bullet of cross-theory section
- **Target**: Merged §4 "Grounding caveat"
- **Rationale**: A's framing of the inference gap (pr86 0.90/0.60 vs H3 0.95) is most explicit; shared assumption A-001 demands prominent flagging
- **Integration approach**: Promote from a bullet to its own §4 section
- **Risk**: Low (improves epistemic honesty)

### Change 5 — Preserve B's honest §1 channel-degradation note (abbreviated)
- **Source**: Variant B, §1
- **Target**: Merged §5 "Methodology note"
- **Rationale**: High-integrity meta-signal; tells downstream consumers this is a 3-channel degraded merge, not a single-tool-validated result
- **Integration approach**: Compress to 3-4 sentences citing each channel's actual ground state
- **Risk**: Low

## Changes NOT being made

- **A's T3 (stripped-context)**: Lowest-confidence T3 across variants; B's verdict-direction (B3 → M3) supersedes
- **C's T3 (anchoring leak)**: At 0.45 confidence, below useful threshold; mechanism partially absorbed into M3
- **C's tier-landing narrative §3**: Useful for debugging C's pipeline but not load-bearing for the merged answer
- **B's reflection-protocol verbatim quote**: Out-of-band detail for the merged answer
