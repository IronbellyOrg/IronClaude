---
needs_human_decision: false
status: RESOLVED
---

# WC-16 wait-timeout wording and sweep.md cadence decision (contract gate, cycle 1)

Recorded 2026-11-12 during item 12.14 (QA contract fix cycle 1). This record adds to `OQ-3-GQ-11-rule-id-decision.md`, which approved WC-16 and the DESIGN section 8 text as written; it does not replace it.

## Question put to the owner

The contract gate (`qa/contract/consolidated-findings-cycle0.md`) found two MAJOR defects that the item 12.14 fix agent is not allowed to fix as the plan is written:

- CON-F1: `src/superclaude/commands/sweep.md` line 20 says the coordinator runs `/sc:sweep` "on every wake" with no limit, while WC-16 and the liveness sweep (contract line 110) say at most once every 5 minutes.
- CON-F2: WC-16 says "On every coordinator wake", while the liveness sweep runs "after every wake or timeout"; a quiet timeout, when all workers are silent, could be read as not needing a sweep. WC-16's text is the wording the owner approved in OQ-3, so a change needs the owner's approval.

## Owner decision (current conversation, 2026-11-12)

Option chosen: "Approve both fixes". Exact approved changes:

1. WC-16 (contract line 277), first words: "On every coordinator wake, at most once every 5 minutes, ..." becomes "On every coordinator wake or wait timeout, at most once every 5 minutes, ...". The pinned phrase "On every coordinator wake" stays a substring, so no test pin changes.
2. DESIGN section 8 "**Final text.**" fenced block: the same change, so the contract and DESIGN stay byte-identical.
3. `src/superclaude/commands/sweep.md` line 20: "Explicit only: the coordinator runs `/sc:sweep` on every wake, or a person types it." becomes "Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it."

## Scope of this approval

The fix agent's allowed files are widened to exactly these three places (plus appending a dated re-run note to `phase-outputs/test-results/step-1.17-checks.md`). Nothing else changes: DESIGN row R2 (line 716, which already carries the 5-minute cap), contract lines 110 and 151, every other WC-16 sentence and every test pin stay as they are. The approval covers this one edit; it does not reopen the rest of the OQ-3 text.
