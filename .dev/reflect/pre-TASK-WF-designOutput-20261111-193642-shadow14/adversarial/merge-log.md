# Merge Log — Mode A Step 5

Executor: debate-orchestrator (merge executed per refactor-plan.md; merge-executor delegation collapsed into this pass because the plan contained only single-file, low-risk insertions and rewordings — see Execution note).

## Execution note

The refactor plan's 12 actions (R1-R12) were all LOW-risk edits to a single new output file with a fully specified target text; the orchestrator executed them directly rather than spawning a merge-executor agent for a one-file copy-through. No variant content was modified: variant-1/2/3-original.md are byte-identical copies of the three cards.

## Actions applied

- R11/R12 (scaffold): evidence-validator flag header (all findings, per A-003 REJECT + probe IP-2) and provenance key added.
- R1 → MF-1: base C1-F1 claim kept; wording guard applied ("cannot fail mechanically against spec AC6 as written"); C2-F3 green-run detail folded into latent note; C3-F3 AC3 half recorded as dropped duplicate.
- R2 → MF-2: base F4's advisory framing replaced with settled form: contradiction + "Drift, unamended plan" tag, conf .80 (from C3-F1, the carrier); C1-F4 folded with its Round-2 concession noted.
- R3 → MF-3: base F2 recategorized other/advisory → unpassable-check per the panel's tightened A-005 rule; C3-F3 AC1 half folded as corroboration; advocates 1/2 dissent recorded in provenance.
- R4 → MF-4: inserted (new section) from C2-F4, narrowed to "unchecked requirements"; cross-linked to MF-5.
- R5 → MF-5: inserted from C3-F2, missing-requirement + Drift deviation class, conf .70; cross-linked to MF-4 and MF-10.
- R6 → MF-6: inserted from C2-F1, missing-requirement .80, uncontested.
- R7 → MF-7: inserted from C2-F2, traceability `other` .65, with advocate-1's Round-2 narrowing recorded.
- R8 → MF-8: base C1-F3 kept; C3-F4a "no new field" folded in; Grounding-placement gap retained as unique content.
- R9 → MF-9: base C1-F5 reworded per advocate-1's Round-2 concession ("inadequate check, no baseline or scoped diff"); conf .60 unchanged.
- R10 → MF-10: inserted from C3-F4b as candidate Authorized expansion at .45 with validator drop-guard; not Drift.
- Card self-reports preserved verbatim; shared-runtime-model note (C1/C2 both claude-gw-tier1b) added per probe IP-3.

## Changes not made (from refactor-plan.md, all intentional)

N1 no severity raised; N2 no confidence inflation for MF-4/MF-5; N3 calibration blocks not averaged; N4 D3 dissent recorded not resolved by argument; N5 no line re-verification (validator flag instead).

## Verification

- All 12 planned actions applied; 0 partial applications.
- Provenance map check (probe IP-1 fix): 13 originals = MF-1 (C1-F1 + C2-F3, C3-F3a dropped), MF-2 (C3-F1 + C1-F4), MF-3 (C1-F2 + C3-F3b), MF-4 (C2-F4), MF-5 (C3-F2), MF-6 (C2-F1), MF-7 (C2-F2), MF-8 (C1-F3 + C3-F4a), MF-9 (C1-F5), MF-10 (C3-F4b) — count reconciles.
- Category gate check (probe IP-4 fix): `other` survives only on MF-7 and MF-9, matching tightened A-005.
- Severity check: all 10 MINOR, none blocking — matches every card.
- Taxonomy tags: L2 x5 (MF-2, MF-3, MF-6, MF-9, MF-10), L3 x5 (MF-1, MF-4, MF-5, MF-7, MF-8); matches diff-analysis tagging.

## Artifacts

- merged-output.md (../merged-output.md)
- adversarial/variant-{1,2,3}-original.md, diff-analysis.md, debate-transcript.md, invariant-probe.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml
