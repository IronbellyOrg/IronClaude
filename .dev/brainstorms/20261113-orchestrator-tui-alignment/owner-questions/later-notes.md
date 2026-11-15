# Notes filed for later (owner asked for these to be kept, not acted on)

> **Context for a reader arriving cold.** This file belongs to the "orchestrator, observer and issue watcher alignment" program of the IronClaude repository. **Start with `open-decisions.md` in this folder** for the program, the terms and what is still open.

Local notes only. Nothing here is posted to GitHub. To track one on GitHub, the owner says so and a grant row is written first.

## L-1. A second GitHub account for approvers (filed 2026-11-14, from Q2 Decision 4)

What the owner decided: not necessary for now. The owner keeps one GitHub login on this host and accepts that an agent on this host could apply the approval label as the owner, because every session here acts as that one login.

Why it was raised: the approval flow accepts "an approval label applied by the assignee" as one input. With one login, the coordinator cannot tell the owner's label from one an agent applied. The design's other safeguards still hold: the approval is tied to the plan's hash, the label must come after the plan reply, the plan reply must be unedited since, and every start needs the coordinator's own approval record.

Revisit when any one of these happens:
- a second person or a bot starts acting on the issues this host's watcher claims;
- the watcher's recurring schedule (FU-2) is switched on for issues the owner did not write;
- the approval flow is used on an issue whose text the owner did not write;
- a separate GitHub account becomes cheap (for example a machine account the owner already has).

What changes then: approvers use an account this host's sessions do not hold; approvals from the host's own login are refused (the watcher's follow-up FU-6, per-person checks, is the nearest existing item).

Source: `Q02-approval-flow/final.md`, Decision 4 and failure mode F8.
