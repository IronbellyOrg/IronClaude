# Merge Log: D-P2-23

## Metadata
- Base: Variant 1 (option A, skip the whole CLI-mode reflect gate under --unattended), file `adversarial/variant-1-original.md`
- Incorporated: Variant 2 (option B), strengths only
- Executor: merge-executor
- Plan: `adversarial/refactor-plan.md` (3 planned changes, overall risk Low)
- Output: `merged-decision-D-P2-23.md`
- Changes applied: 3 of 3 (Change #1, Change #2, Change #3), plus the Decision section required by the invocation
- Status: Complete
- Timestamp: 2026-11-07

## Changes Applied

### Change #1: Recovery sentence for the audit option A gives up
- Status: Applied
- Before: the base ended its weakness line with "Claimed weakness: the task loses its independent post-execution audit; the coordinator must run reflect itself." and went straight to "How to judge".
- After: the "Recovery:" sentence from the plan is added right after the "Claimed weakness" line, as a separate block.
- Provenance tag: `<!-- Source: Variant 2 (option B), Claimed strengths - merged per Change #1 -->`
- Validation: text copied from the plan; no repository file touched; consistent with the base weakness line (the coordinator runs reflect).

### Decision section (required by the invocation, not a numbered plan change)
- Status: Applied
- Before: no decision statement in the base.
- After: new H2 "## Decision" before "## How to judge": winner option A, convergence 83.3% (10 of 12), combined score 0.844 vs 0.724, with the one-sentence reason (git add -A refused by WC-9; wrapper has no --unattended so spec 2.1 gives skip-and-record; tdd.md:168 and pinned tests already commit to skip).
- Provenance tag: `<!-- Source: Base (original, modified) - decision summary added per debate-transcript.md Scoring Matrix -->`
- Validation: figures match debate-transcript.md (Convergence Assessment) and base-selection.md (Combined Scoring); reason matches base-selection.md "Selection rationale".

### Change #2: Build time versus run time open item
- Status: Applied
- Before: not present.
- After: first bullet under new H2 "## Open items", from the plan rationale (SKILL.md:410 in build step A.3; gate item at :2237 runs later under /task; paragraph does not say whether the builder omits the item or emits it in skip form).
- Provenance tag: `<!-- Source: Variant 2 (option B), Claimed strengths - merged per Change #2 and Change #3 -->` on the "Open items" section; the bullet is labelled "Change #2".
- Validation: wording limited to the plan; stated as unresolved and unchanged.

### Change #3: Task log versus contract open item
- Status: Applied
- Before: not present.
- After: second bullet under "## Open items", labelled "Change #3" and "UNVERIFIED", from the plan rationale (spec 2.1 "records the skip in its contract" versus SKILL.md:410 and tdd.md:168 "in the task log"; tdd.md:166 artifacts list).
- Provenance tag: same section tag as Change #2 (covers Change #2 and Change #3).
- Validation: UNVERIFIED label kept as in the plan; no new facts added.

## Post-Merge Validation

### Structural
- Heading hierarchy: H1 (title), then H2 "Decision", H2 "Open items", H2 "How to judge (the same for every decision)". Starts at H1, no gaps. PASS.
- Base text preserved: title line, both body paragraphs, "Why skip" paragraph, claimed strengths and weakness lines, and the whole "How to judge" section are unchanged. Each block carries a Source tag. PASS.
- Provenance header: the three required comment lines are first in the file. PASS.

### References
- Internal references: the document makes no cross-references to its own sections, so none can dangle. The "(the same for every decision)" heading text is a label, not a reference. PASS.
- External references (SKILL.md lines, tdd.md:166 and :168, spec sections 2.1 and 3.1, WC-4, WC-9, WC-11, SA-1, SA-4) are carried from the base, the plan and the evidence files; they were not re-checked against the repository in this step (not in scope for the merge). Noted, not a failure.

### Contradictions
- Re-scan of the merged text against Variant 1 and Variant 2 (as summarised in base-selection.md and debate-transcript.md): Recovery sentence agrees with the base weakness line; Decision agrees with the base title ("option A (recommended)") and with both advocates' final recommendation (option A); the open items state gaps and propose no change. No new contradictions. PASS.
- The previously found Variant 2 conflict (X-001, audit completeness versus removing staging) is not carried into the merged text.

## Summary
- Planned: 3 changes, plus the Decision section requested in the invocation
- Applied: 3 of 3 planned, plus the Decision section
- Failed: 0
- Skipped: 0
- Repository files changed: none (only the two output files were written)
- Validation result: structural PASS, references PASS, contradictions PASS
