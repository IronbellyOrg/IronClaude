# Phase 1 — Cross-Bucket Consistency Notes

Phase 1 Step 1.3 advisory log. Discrepancies flagged here are not blockers; they refine Phase 2/3 framing so contradictory facts surface as ambiguities rather than silent overrides.

## Bucket presence

| Bucket | File | Status | evidence_status |
|--------|------|--------|-----------------|
| A — sc-tasklist skill | `context-digests/A-sc-tasklist-skill.md` | present | complete |
| B — sc-tasklist CLI/command | `context-digests/B-sc-tasklist-cli.md` | present | complete |
| C — task-builder skill | `context-digests/C-task-builder.md` | present | complete |
| D — rf-agents | `context-digests/D-rf-agents.md` | present | complete |
| E — sc-adversarial protocol | `context-digests/E-adversarial.md` | present | partial (prompt-vs-skill scoring rubric discrepancy noted) |
| F — output schemas | `context-digests/F-output-schemas.md` | present | complete |

Phase 1 G3 gate: **PASS** — Buckets A–E all PASS (E has an advisory partial note that does not affect Phase 4 invocation); F also complete.

## Cross-bucket discrepancies (advisory only — resolve at consumption point)

### CB-1. Adversarial scoring rubric (Bucket E note)
- **Source prompt assumption**: "5 focus areas, 1-10 scale, max 50/proposal" (used by orchestration spec when drafting Phase 4 expectations).
- **Bucket E actual finding**: 50/50 hybrid — 5 quantitative metrics PLUS 30-criterion binary qualitative rubric. Convergence formula is `agreed_points / total_diff_points`, gated additionally by taxonomy coverage AND zero HIGH-severity unaddressed invariants.
- **Disposition**: orchestrator follows the skill's actual contract per G5 (no flag invention; flag values/semantics come from source). Phase 4 will pass `--convergence 0.80` as documented; status interpretation will follow `passed | partial | failed` from the return contract, not a derived 50-point ceiling.

### CB-2. CLI patch/verify advertised but not implemented (Bucket B finding)
- **Bucket B finding**: `commands/tasklist.md:14` advertises "patches any drift, and verifies corrections" but the Python CLI provides no patch/verify orchestration; Python only runs `tasklist-fidelity` step.
- **Bucket A finding**: SKILL.md Stage 9 delegates patching to `sc:task-unified`; Stages 9-10 are skill-prompt-driven, not Python-driven.
- **Disposition**: this is internally consistent — Python validates fidelity; patching lives in skill body via sc:task-unified delegation. No conflict. Phase 3 proposals targeting "patch loop" mechanics must target the skill body, not the Python CLI.

### CB-3. task-builder quality-gate count (Bucket C finding)
- **Bucket A finding**: sc:tasklist has a single 17-point pre-write quality gate (SKILL.md:983-1032 in Bucket A digest).
- **Bucket C finding**: task-builder has 4 distinct gate stages with checklists of 7/9/9/15 items (and 18 Critical Rules) — no single "17-check" list to compare 1:1.
- **Disposition**: proposals that propose to "import the 17-point gate" must explicitly map which sc:tasklist checks land in which task-builder gate stage. Treated as CASE-D (partial coverage on both sides) for any gate-related proposal — Phase 3 must classify per-check, not in bulk.

### CB-4. Tier-classification model (Bucket A vs Bucket C)
- **Bucket A**: deterministic 4-tier (STANDARD/LIGHT/STRICT/EXEMPT) with priority STRICT > EXEMPT > LIGHT > STANDARD, keyword scoring + compound-phrase overrides + context boosters + confidence formula (SKILL.md:385-391, 510-575).
- **Bucket C**: rule-based 3-tier (Quick/Standard/Deep) determining researcher counts (3 / 4-5 / 6-8). No numeric algorithm.
- **Disposition**: not directly portable; the two systems classify different things (artifact compliance vs research depth). Phase 3 proposals must explicitly state which tier model they target. Treated as CASE-A candidate (task-builder's invariant: research depth, not artifact compliance) for any "tier classification" proposal.

### CB-5. Determinism scope (Bucket A vs Bucket C)
- **Bucket A**: explicit determinism guarantee — same roadmap → same output, with appearance-order IDs, explicit tiebreakers, no roadmap-text leakage rules (Bucket A "load-bearing behaviors" section).
- **Bucket C**: no determinism claim; explicit non-determinism via parallel agents and exploratory research (Bucket C: "evidence_status: complete; determinism: not claimed").
- **Disposition**: any proposal that introduces determinism into task-builder must declare scope per G5 — e.g., "frontmatter-stable" or "ID-stable" — not blanket determinism. This is precisely FINAL-REPORT §6.2 F4's "hidden input" framing applied in reverse.

### CB-6. Traceability matrix presence
- **Bucket A**: full R-### → T<PP>.<TT> → D-#### chain, surfaced in artifacts (SKILL.md:596-600, 703-706).
- **Bucket C**: explicit silence — task-builder does NOT produce a traceability matrix or roadmap-item-to-task chain.
- **Disposition**: this is a clean CASE-B candidate (sc:tasklist additive, task-builder silent) unless adding a matrix violates the self-contained-item invariant or evidence-bound-item invariant. Phase 3 must check.

## Conclusion

No blocking inconsistencies. Five advisory notes (CB-1 through CB-6) refine Phase 2 matrix construction and Phase 3 proposal framing. The orchestrator proceeds to Phase 2.
