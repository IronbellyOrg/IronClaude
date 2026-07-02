# Refactor Plan — Merged Requirements

## Base

Base variant: Variant 2 — Minimal-Risk Contract Creation UX.

## Planned Changes

1. Incorporate shared helper architecture from Variant 1.
   - Target: recommended product behavior and implementation plan.
   - Risk: Low; additive clarification.

2. Incorporate metadata/provenance block from Variant 1.
   - Target: output artifacts and contract fields.
   - Risk: Medium; must remain ignored by classifier unless implemented.

3. Incorporate QA evidence rejection matrix from Variant 3.
   - Target: safe locking policy and validation checklist.
   - Risk: Low; policy-level addition.

4. Resolve decline-evidence tension with v1 warning policy.
   - Target: safe locking policy.
   - Risk: Medium; document that decline defaults are retained but unexercised decline evidence is surfaced.

5. Resolve reflect scope with diagnose/validate-first behavior.
   - Target: recommended behavior and integration.
   - Risk: Low; avoids side-effect creep.

## Changes Not Made

- Did not make `/sc:reflect` the default writer of locked contracts.
- Did not require observed decline evidence for every v1 lock.
- Did not allow automatic monitor resume after contract creation.
- Did not propose modifying the shipped contract to `locked: true`.
