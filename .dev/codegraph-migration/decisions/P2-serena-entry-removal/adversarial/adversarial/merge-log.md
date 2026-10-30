# Merge Log

## Metadata
- Base: `variant-2-original.md` (Option B), score 0.898
- Executor: merge-executor (Step 5 of sc:adversarial)
- Plan: `refactor-plan.md`, RP-1 to RP-8, applied in order
- Changes applied: 8 of 8
- Output: `../P2-serena-entry-removal-merged.md` (46 lines; limit: under 50)
- Status: SUCCESS for the merge. The decision carries 2 escalated unmet invariants (INV-001, INV-002), as the debate and plan require.
- Timestamp: 2026-10-29

## Changes Applied

| # | Title | Status | Where it landed in the merged file | Provenance tag |
|---|---|---|---|---|
| RP-1 | Bundle stops Serena in Coder step 2 | APPLIED (replaced base bullet 3, which put it in step 5) | "What Coder must do, and when", bullet 1 | `<!-- Source: RP-1, RP-6 ... -->` on the section head |
| RP-2 | Guard = `codegraph_ready()`, the codegraph phase's own pass check | APPLIED (replaced base "codegraph phase returned success") | "The rule", "When" bullet; INV-010 acceptance noted inline | `<!-- Source: V2 base; RP-2, ... -->` on the section head |
| RP-3 | Remove every user-scope `serena` launcher; Tier R unconditional; env/headers kept and reported | APPLIED (replaced base "Other Tier K shapes stay kept") | "The rule", "What is removed" bullet | same section-head tag |
| RP-4 | Kind-B registration under the same predicate; binary and companions stay; upstream `uninstall` printed; escalated | APPLIED (new bullet) | "The rule", "Same condition" bullet; escalation in "Stated exceptions and escalations" (INV-002) | same section-head tag |
| RP-5 | Re-register hint uses `serena-local` | APPLIED (new bullet) | "The rule", "Messages" bullet | same section-head tag |
| RP-6 | Guarded one-time migration in `startup.sh` in step 2, plus uv tool, markers, alias, health set, handshake proof; step 5 drops the baked binary; Coder confirmations | APPLIED (replaced base bullet 3) | "What Coder must do, and when", bullets 1-4 | `<!-- Source: RP-1, RP-6; migration from V1/V3, guarded per R2 -->` |
| RP-7 | Amend Phase 1, handoff and Phase 2 texts in the same merge | APPLIED (new section) | "Spec amendments in the same merge" | `<!-- Source: RP-7 -->` |
| RP-8 | Acceptance: unit list, layer-2 both branches, Coder boot tests, project-scope `jq -e`, run after every session restart, Coder gated on pin >= merge SHA, stated exceptions | APPLIED (replaced base bullet 5) | "Acceptance checks"; "Stated exceptions and escalations" | `<!-- Source: RP-8; tests from V3/R2, checks from V1 -->` |

Also carried, as the caller required: "When completely absent holds" rewritten to match RP-1/RP-6 (base bullet 4 claimed absence after the slug run, defect X-001); "How this was chosen" with scores, convergence, incorporated strengths and rejected items from `base-selection.md`, `debate-transcript.md` and the plan's "Changes NOT Being Made". The base's Strengths/Weaknesses lines were dropped to fit the line limit; the one weakness still live (overriding part of the Phase 1 provenance rule) is handled by the RP-7 amendments.

## Post-Merge Validation

### Structural integrity
- One H1, seven H2 sections, no deeper levels; order: rule, Coder, timing, spec amendments, acceptance, exceptions, selection. PASS.
- Header comment block: 2 lines (limit 3). Other provenance tags sit on section-head lines only. PASS.
- Line count (`wc -l`): 46. Under 50. PASS.

### Internal references
- `context.md` exists at `decisions/P2-serena-entry-removal/context.md`; the merged file sits one level below it, in `adversarial/`. The intro says "Read `context.md` first", as the base did; the path is relative to the decision folder, not to the merged file. Note, not a failure.
- `adversarial/variant-2-original.md`, `adversarial/refactor-plan.md` and `adversarial/merge-log.md` named in the header all exist relative to the merged file. PASS.
- INV-001, INV-002, INV-010 resolve to rows in `invariant-probe.md`. PASS.
- The base's dangling reference "the Coder 'Done means' check above" (defined only in Option A) is gone; the checks are written out. PASS.

### New contradictions re-scan (merged file vs variants and debate)
- X-001 (base said registration gone after the slug run): removed. The merged file says registrations are gone after `./update.sh` only once the step-2 image has booted. No contradiction.
- Base "Other Tier K shapes stay kept": removed (grep finds no match); replaced by RP-3. No contradiction.
- Option A and Option C put the bundle stop and migration in step 5; the merged file puts them in step 2, guarded. This matches the debate outcome (C-003, C-004 guarded per Round 2), not a new contradiction.
- Option C's provenance-file guard: absent from the rule (grep finds no `ironclaude-provenance`); listed only as rejected. Consistent with X-003.
- Tier R removes the `/usr/local/bin/codebase-memory-mcp` registration unconditionally, while the Coder migration also removes that entry under a guard. Not a contradiction: the Coder step is a backstop for a retire step killed by the 60 s budget (INV-006); the unit test pins the asymmetry (INV-011).
- "Never left with neither" vs removing kind-B codebase-memory: both removals happen only when `codegraph_ready()` is true. Consistent.
- Residual risk from debate Round 2 (B advocate): a later codegraph remove-then-add killed by `timeout 60` after Serena is gone could leave neither until the next boot. Not stated in the merged file because the plan did not list it; it is covered by the Coder confirmation item and Phase 2 §2.9. Recorded here only.
- Result: 0 new contradictions.

## Summary
- Planned: 8
- Applied: 8
- Failed: 0
- Skipped: 0
- Validation failures: 0
- Escalations carried unchanged from the plan: INV-001, INV-002.

## Orchestrator post-merge corrections (2026-10-29)
- Acceptance `jq` replaced with the null-safe form `[(.mcpServers // {}), (.projects // {} | .[] | .mcpServers // {})] | ...`. It was tested on sample JSON (absent keys, project-scope hit) and on the live file, which still has both servers, so it exits 1 as expected.
- "When absent holds" on Coder corrected: the registrations are gone right after `./update.sh`. The step-2 image only stops the re-add.
- Context link changed to `../context.md`. Added the `timeout 60` residual risk from Round 2 (B).
- Final line count of the merged file: 47.
