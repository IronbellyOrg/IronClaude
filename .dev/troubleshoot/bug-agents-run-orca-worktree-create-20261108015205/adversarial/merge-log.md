# Merge Log

## Metadata
- Base: Variant 2 (variant-2-original.md, fix-2)
- Incorporated: Variant 1 (variant-1-original.md, fix-1), Variant 3 (variant-3-original.md, fix-3)
- Plan: refactor-plan.md (7 planned changes, 3 rejected)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: merged-output.md
- Changes applied: 7 of 7
- Status: complete, with 2 warnings (see Post-Merge Validation)
- Timestamp: 2026-11-08T02:16Z

## Changes

### Change 1 — Closing command: `--all` inside guards
- Status: applied
- Target: "Proposed change" step 1 (both installed copies)
- Before: list terminals with `orca terminal list --worktree path:<path> --json`, close the single one with `orca terminal close --terminal <handle>`; "Never use `--all`".
- After: the plan's exact sentence, closing with `orca terminal close --worktree path:<path> --all` right after an own-use bare create.
- Provenance: Variant 1 step 1; Variant 3 bullet

### Change 2 — Keep and tighten guards
- Status: applied (folded into the Change 1 sentence, as planned)
- Before: guards "without a setup script", "before any `agent launch`", "never close terminals in a worktree you did not just create".
- After: "only when you created it with no setup script (`--setup skip` or none configured) and have started nothing in it; never run this on a worktree you did not just create."
- Provenance: Base (Variant 2) guards; Variant 3 "before anything is started there"

### Change 3 — Hand-off routing and exemptions
- Status: applied (in the Change 1 sentence and the project bullet)
- Before: no hand-off routing; no exemptions.
- After: "To hand work to a new Claude session, use `worktree create --agent` instead of a bare create; `/sc:issue` and supervised workers keep their own launch steps." The project bullet carries the same routing and exemptions.
- Provenance: Variant 1 (U-002), Variant 3 (U-007)

### Change 4 — Delivery: reinstall
- Status: applied
- Target: "Proposed change" step 3
- Before: "`make sync-dev`, `make verify-sync`."
- After: the same, followed by the plan's exact sentence about `superclaude update` and install_core.py:70-72.
- Provenance: Variant 1 step 3

### Change 5 — Project rule placement
- Status: applied
- Target: "Proposed change" step 2
- Before: "one bullet after line 310 pointing to that sentence."
- After: one bullet after line 310 with the same command and guards in short form (Variant 3 wording plus the base guards), and one comment line in the example block at :318-324 showing the close after the create.
- Provenance: Variant 3 (U-006)

### Change 6 — Tests
- Status: applied
- Target: "Test plan"
- Before: pinned phrases "`orca terminal close --terminal`" and "before any `agent launch`", an assertion that `--all` is absent from the section, the three-file pytest run, live V-JSON then V-CLOSE with `--terminal`.
- After: pinned phrases "`orca terminal close --worktree`" and "worktree you did not just create" for both copies (12 existing unchanged); a new project CLAUDE.md test for `orca terminal close --worktree`; the `--all`-absent assertion dropped; the same three-file pytest run; "Live V-CLOSE (pending; needs a create)" from Variant 1. The base's live V-JSON/`--terminal` line was dropped because it tests the replaced mechanism.
- Provenance: Variant 1 test; Variant 3 test; Base run list

### Change 7 — Document A-001 and residual risks
- Status: applied
- Target: "Risks"
- Before: three base bullets (late seed registration, "exactly one terminal" misjudgment, longer instruction).
- After: base bullets kept, plus (a) Orca UI re-seed (worktree-activation.ts:275), (b) default tabs closed by `--all` (IronOrca runtime-local-worktree-terminal-startup.ts:187-201; the plan's "startup.ts" short name expanded to the base's full file name), (c) compliance unproven (A-002), (d) Variant 2 dissent on the single-handle close.
- Provenance: all advocates (A-001 QUALIFY, A-002 QUALIFY)

## Post-Merge Validation

### Heading hierarchy
- PASS. One H1 (the required title), six H2 in base order: Problem statement, Proposed change, Evidence, Risks, Test plan, Documented constraints to honor. Two H3 under the last H2, unchanged. No skipped levels.
- Provenance header: all three required comments present. Every H2 carries a `<!-- Source: ... -->` comment.
- "Documented constraints to honor" is verbatim from the base (the section is identical in all three variants).

### Internal references
- PASS with note. "Same diagnosis as Fix 1" in the Problem statement is base text; the section's Source comment resolves "Fix 1" to Variant 1 (variant-1-original.md). "See 'Orca session launches'" in the project bullet points at the section named in step 1.
- Citations are copied only from the variants and the plan. No new file paths or line numbers.

### Contradiction rescan
- PASS for tests: no test assertion contradicts the merged sentence. No `"--all" not in section` assertion remains, and the Test plan no longer pins "`orca terminal close --terminal`" or "before any `agent launch`". Both new pinned phrases ("`orca terminal close --worktree`", "worktree you did not just create") occur in the merged sentence.
- WARN 1 (Risks): base bullets 1-3 describe the replaced list-and-handle mechanism (`terminal list`, "exactly one terminal", "list + judgment + close"). The plan says append, not replace, so they were kept, and the Risks Source comment marks them as written for the replaced mechanism. The late-seed race in bullet 1 still applies to the `--all` close. Orchestrator may choose to drop bullets 2-3 in a later pass.
- WARN 2 (Problem statement): the base sentence that the closing step "must not be able to kill a running setup script, a reused worktree's live sessions, or the agent's own shell" is unchanged. The merged guards (no setup script, nothing started, only a worktree you just created) address those three cases, but default tabs remain uncovered; that gap is stated in Risk (b). No change made, because the plan does not touch this section.

## Summary
| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 7 | 7 | 0 | 0 |
