# Merge Log: Q32

## Metadata

- Base: Variant 2 (proposal-B), `adversarial/variant-2-original.md`
- Executor: merge-executor agent
- Changes applied: 4 of 4
- Status: success
- Timestamp: 2026-11-14
- Output: `merged-output.md`

## Changes Applied

### Change 1: Guard the uncommitted gap

- Status: applied
- Source: round1-advocate-2.md, Shared assumption responses, A-002
- Target: "What happens next if the owner picks it" (new last bullet) and "What it costs or risks" first bullet (one sentence appended)
- Before: "What happens next" had three bullets with no guard on the worktree. The first risk bullet ended "The spec does not measure how long that gap is (UNVERIFIED)."
- After: new bullet, verbatim from the plan's integration point: "The coordinator does not remove, clean or reuse a worker's worktree until its PR session has committed the change; this guard is not yet written in the spec as a general rule, so it is recorded in the ledger with Q32's answer." The first risk bullet gains: "The guard under "What happens next if the owner picks it" bounds this risk until the spec states it as a general rule."
- Provenance tag: `<!-- Source: Variant 2 advocate concession (A-002) with Change #1 -->` on the new bullet; `<!-- Source: Base (original, modified) with Change #1 -->` on the costs section
- Validation: the plan gives one integration sentence but targets two places; the appended risk sentence only points back to that guard and adds no new claim. The guard is marked as not yet a general spec rule, matching the advocate's UNVERIFIED note.

### Change 2: Door stays open per Task

- Status: applied
- Source: Variant 1, "Answer" and "What it unlocks"
- Target: "What stays unresolved" (new bullet, third)
- Before: two bullets (wait length; later programs).
- After: adds "If the owner later wants a checkpoint commit for one specific Task, that Task can get its own owner sentence and grant, which meets WC-9 strictly."
- Provenance tag: `<!-- Source: Variant 1 with Change #2 -->`
- Validation: wording matches the plan's integration point exactly; does not change the "no" answer.

### Change 3: Stronger "yes" sentence for reference

- Status: applied
- Source: round1-advocate-3.md, Concessions (item-list sentence)
- Target: "What stays unresolved" (new bullet, fourth)
- Before: as after Change 2.
- After: adds "If the owner prefers yes after all, a sentence naming all nine work items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07) lets each brief quote it unchanged; whether that meets WC-9's 'for that Task' is UNVERIFIED."
- Provenance tag: `<!-- Source: Variant 3 with Change #3 -->`
- Validation: wording matches the plan; nine IDs listed, count matches "nine".

### Change 4: Citation fix

- Status: applied
- Source: round1-advocate-1.md, Weaknesses identified in Variant 2
- Target: "What happens next if the owner picks it", second bullet
- Before: `WORKER-CONTRACT.md:42`
- After: `WORKER-CONTRACT.md:44`
- Provenance tag: `<!-- Source: Base (original, modified) with Change #4 -->`
- Validation: a search of `src/superclaude/core/WORKER-CONTRACT.md` found the quoted "never runs `git add`" sentence at line 44.

## Post-Merge Validation

### Structural Integrity

- One H1 and the base's five H2 headings, in the base's order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No heading levels skipped.
- Provenance header (3 comments) present; each section and each changed block carries a Source comment.
- No em dashes or en dashes in the merged document (search returned 0).

### Internal References

- The appended risk sentence names "What happens next if the owner picks it", which exists and holds the guard bullet: resolves.
- `WORKER-CONTRACT.md:44` now points at the quoted sentence. `WORKER-CONTRACT.md:244` and `:245` were not in the plan and are unchanged.
- Spec references (line 1070, 6.4 rule 14, WC-9, INV-001) unchanged from base.

### Contradiction Re-Scan

- The answer stays "no" for this program. Change 2 describes a later per-Task grant and Change 3 a "yes" sentence, both under "What stays unresolved" as conditional options, so they do not contradict the answer or the statement that the grant table never holds a worker commit row in this program.
- The guard (Change 1) adds a coordinator duty and does not conflict with "the PR session gets exclusive use of the worktree".
- The risk bullet still says a stray checkout could lose the change; the guard covers remove, clean and reuse only, so the two statements are consistent. No new contradictions found.

## Summary

All 4 planned changes were applied in plan order to Variant 2 with provenance tags. Structure, references and consistency checks passed. One judgment call: Change 1's second target (one sentence appended to the first risk bullet) had no exact wording in the plan, so the added sentence only refers back to the guard bullet.
