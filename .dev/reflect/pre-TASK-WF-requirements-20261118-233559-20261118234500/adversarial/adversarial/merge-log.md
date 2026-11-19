# Merge log

Base: variant-3-original.md. Plan: refactor-plan.md. Output: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261118-233559-20261118234500/adversarial/merged-output.md

| Change | Source | Action | Validation |
|---|---|---|---|
| M-1 | V2 QA-3 | Added as blocking, text from plan | Severity and file:line match plan |
| M-2 | V2 QA-4 | Added as blocking | Match |
| M-3 | V3 F3 + V2 QA-1 | Replaced V3 F3 with plan wording | Match |
| M-4 | V1 F1, V3 F4, V2 QA-6 | Added medium | Match |
| M-5 | V3 F1 narrowed | Replaced V3 F1 (blocking) with plan's medium | Severity changed per plan |
| M-6 | V3 F2 narrowed, V2 QA-2 | Replaced V3 F2 (blocking) with plan's medium | Severity changed per plan |
| M-7 | V1 F4, V3 F6 | Added medium (V3 F6 was a note) | Per plan |
| M-8 | V3 F7 | Kept medium | Match |
| M-9 | V1 F7 | Added medium | Match |
| M-10 | V1 F2 | Added medium; R20 not a gap | Match |
| M-11 | V3 F8 | Kept medium, INFERRED mark kept | Match |
| M-12 | V1/V2/V3 minor | Added as note; V3 F9 folded in | Match |
| Refuted items | plan "Changes not made" | Section added | Two items noted |

Structure kept from V3: verdict, findings, no-finding list, not-checked list. One section added for the two refuted items.

Provenance: an HTML Source comment sits on every finding and section.

Deviations and escalations:
- The plan gives no requirement row for M-1, M-2, M-7, M-9, M-11, so the merged text says "not named in the plan" rather than inventing one.
- Verdict line recomputed: 3 blocking (M-1 to M-3), 8 medium, 1 note. V3's original "3 blocking" referred to different findings (F1, F2, F3); F1 and F2 are now medium per the plan.
- No findings added; no severity or file:line altered.

Contradiction re-scan: none found. Every register entry cites only references that the plan gives.
