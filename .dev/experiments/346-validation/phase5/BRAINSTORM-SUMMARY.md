# Phase 5: five brainstorm specs compared (issue 346)

Written 2026-11-08 by the coordinator (Orca run run_58af03dbfa92). Every number below is the team's own prediction written before any run; none is a measurement. All five brainstorms ended `worker_status: partial` (debate gate blocked on high-severity invariants, resolved in the merge, not by agreement).

Specs (read-only, one per worktree): `/home/coder/workspaces/worktrees/IronClaude/bs346-<team>/.dev/brainstorms/346-<team>/SPEC.md`. Dispatch log: `phase5/coordinator-log.md`.

| Team | Variant command | Mechanism | Predicted review-3 critical+major (bar 3 or fewer; control 6.0, Arm B 3.5) | Predicted growth (bar 44.4%) | Team's own risk |
|---|---|---|---|---|---|
| ponytail | spec-panel-ponytail | One audit before review 3: ponytail-review writes per-fix severity/necessity table; a script applies reverts and deletions only | 3.3 (2.9 to 3.6), about 35% chance of meeting the bar | 27% | Auditor must spot surplus words before review 3 does (35-50% capture is assumed, unmeasured) |
| minfix | spec-panel-minfix | Per-finding word budget (minor 0, MAJOR 80, CRITICAL 120), delete-narrow-replace-add order, script reverts over-budget fixes | 3.3 (band 1 to 6), coin flip | 13% (ceiling 21.3%) | Small fixes still create blocking children (flg-r2 F12, 58 words, produced N4) |
| diffgate | spec-panel-diffgate | Script computes re-review surface as a diff; unanchored findings become deferred, never blocking; script derives verdict; refuses reviser hunks not owned by an open blocking finding | 3.0 to 3.5; P(both replicates 3 or fewer) 0.20 to 0.25 | 20-27% | In flg-r1, 4 blocking fixes produced 4 new blockers; this theme cannot lower that without hiding defects |
| stoprule | spec-panel-stoprule | Sealed claims (quote plus concrete outcome), late-found demotion, independent grader confirms blockers, computed verdict | 4.0 on the label proxy (5 and 3), chance of bar about 0.2; script-confirmed count 2.0 | about 20% | Converges by filtering; own filter-only falsifier predicted to fire at about 0.7 |
| ledger | spec-panel-ledger | Script-written finding ledger; review 1 is the only find pass; reviews 2 and 3 only answer rows and check changed text; one final sweep reported, never looped | 5.5 headline (3 to 9); loop-only 3 | 26% | Defects move to the final sweep; fix-induced defects untouched |

## What all five agree on
- The dominant remaining cause is fixes of blocking findings creating new defects (diffgate: 4 fixes, 4 new blockers in flg-r1; minfix: a 58-word fix produced N4; ledger and ponytail say the same). Reviewer-side filters (diffgate, stoprule, ledger) lower the visible count by hiding or relocating findings unless the count rule includes them.
- Only minfix and ponytail act on the fix itself. They compose: minfix limits fix size at write time, ponytail deletes surplus text after round 2.

## Owner decisions that cross teams (defaults used by the specs in brackets)
1. Counting rule: does the success measure count findings the new scripts defer, demote or withdraw as still open? [diffgate counts them in `R3-proxy-all`; ledger publishes the floor beside the bar; stoprule asks]
2. The S1 review-3 brief says "any finding of any severity is FAIL", which conflicts with a computed verdict (427 bullet 7). [ponytail keeps it for comparability; stoprule asks]
3. Consent: is a flag in the brief enough to count as explicit user consent for one scripted edit or revert under 427's no-unconsented-edit rule? [ponytail, ledger and minfix ask]
4. Ponytail placement wording: before review 3 (this spec) or after review 3 (cannot change the registered review-3 count).
5. Stoprule's ablation arm (`spec-panel-stoprule-noscript`): authorize or not.

## Unverified prerequisites (one smoke dispatch settles all)
- Can a dispatched worker run `uv run --no-project python ~/.claude/skills/...` without a permission prompt? (diffgate Q1, minfix)
- Can a dispatched worker load `ponytail:ponytail-review`, and spawn a subagent while heartbeating? (ponytail Q5, ledger Q1)

## Cost note
Ledger's brainstorm used about 3.59M subagent tokens against a 540K estimate (no hard-kill guard). Five workflows, five implementations and five re-runs will be heavy.
