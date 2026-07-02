# Base Selection (blind scoring)

## Combined scoring (0.50 quant + 0.50 qual)

| Variant (blind) | Identity | Quant | Qual (/30) | Combined | Notes |
|---|---|---|---|---|---|
| A | opus:architect | 0.88 | 26/30 (0.87) | **0.875** | Strongest structure for a design-feeding spec; contract-boundary framing; formal back-compat proof; completeness |
| B | opus:refactorer | 0.86 | 25/30 (0.83) | 0.845 | Sharpest minimalism + "NOT making" ledger + unreachability proof; slightly thinner on test matrix |
| C | haiku:qa | 0.84 | 24/30 (0.80) | 0.820 | Best verification surface (contract table, fixtures, parity); lighter on architectural framing |

- Position-bias dual pass (A,B,C / C,B,A): agreed on ranking; no re-evaluation needed.
- Edge-case floor (Invariant & Edge Case Coverage ≥1/5): all three pass (A 4/5, B 4/5, C 5/5).

## Selected base: Variant A (opus:architect) — combined 0.875

**Rationale:** the merged deliverable feeds `/sc:design`, so the base must carry the strongest
requirements-and-contract skeleton. A provides the detection-contract-as-boundary framing, the two
named consumers, and the `old_match ⊆ new_match` back-compat proof — the load-bearing structure.

**Strengths to preserve (base):** contract-boundary framing; back-compat by construction; sizing;
consumer-chain grounding.

**Strengths to incorporate (non-base):**
- From B (refactorer): the 9-item "CHANGES WE ARE NOT MAKING" ledger; inline-no-helper mandate;
  raw-substring/no-nested-parse (OQ1); timeout unreachability proof + net-2-hunks framing.
- From C (qa): the ~12-row detection-contract table with xfail cells; per-row `resolved_model`
  assertion; is_error:false FP fixture; 4 live/offline parity tests incl. PASS_RECOVERED.
- From invariant-probe: INV-001 FP residual + risk-ledger; INV-004 C5-load-bearing interaction test;
  INV-005 sufficiency branch-trace as the AC1/AC2 backbone.

**Tiebreaker:** not triggered (A leads B by 3% > 5%? margin 0.030 < 0.05 → within tiebreaker band;
Level-1 debate performance: A won C-006 back-compat, tied elsewhere → A confirmed).

**Interactive checkpoint (base selection):** `--interactive` set. Auto-resolved to highest-scoring
base with full harvest of B and C — documented here per protocol default action ("accept
highest-scoring variant"). No genuine either/or decision remained (merge harvests all three), so no
user pause was raised; the substantive decisions were the four locked in Wave-1 Socratic dialogue.
