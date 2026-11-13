# Refactor Plan (Step 4)

Base: Variant 1 (analyzer card). Approval: auto-approved (non-interactive).

## Planned Changes
1. Title the merged verdict "UC-1 plan-fidelity findings (no deviation classes)" — V1 position, unanimous X-001; V3's headless-AUTO-FIX rationale recorded.
2. Wording-attribution finding (MF-1): keep V1's per-field breakdown as body; set severity MEDIUM; apply probe INV-002 (returns-nothing fallback explicit in 3 of 4 reference agents; reuse-auditor.md:50 unnamed), INV-003 ("two freshness-gate families", not "two versions"), INV-006 (severity rationale = false provenance + coherence, NOT behavioral loss; ~/.claude/CODEGRAPH.md:32,70,76 preserves the effective fallback by reference). V2's attribution-not-inclusion line kept.
3. AC-strength finding (MF-2, LOW): V2 body (token counts + diff shape), V1 rider (checked_at/worktree_root never required), V3 F4 folded (unnamed agent-file tests), INV-001 correction (ACs also constrain diff shape and tools line — the gap is no exact-text assertion).
4. Spec-contradiction finding (MF-3, LOW): V1 U-003 verbatim (root cause; tasklist resolves silently).
5. List-style finding (MF-4, LOW): V3 U-002 (numbered bold-label lists; executor invented "6. **Use Codegraph Safely**").
6. Advisory note (ADV-1): V3 plugin mirror with own new evidence (mirror predates plan; reference agents absent from mirror entirely; build-plugin ships mirror verbatim) — unanimous (b) out-of-scope-as-finding; action: decide whether plugins/superclaude/agents must mirror src/superclaude/agents.
7. Coverage statement: 3/3 union rows covered; INF-002 labeled "verified outside grounding root" (main checkout, orchestrator).

## Changes NOT Being Made
- V2's Drift/Regression counts: rejected (unanimous; UC-2 semantics in a UC-1 audit; headless AUTO-FIX hazard).
- Behavioral-loss severity rationale for MF-1: rejected per INV-006.
- Plugin mirror as a blocking finding: rejected (unanimous (b)); pre-existing gap, spec never names plugins/.

## Risk Summary
All changes additive to base card text; no structural risk. Merged verdict feeds reflect Wave 5 evidence-validator; every citation re-checked there.
