# Task 2 report: places in WORKER-CONTRACT.md checked against the WC-3 definition

Each place was Read in full before deciding.

| Place (after Task 1 line numbers) | Decision | Reason |
|---|---|---|
| WC-17 plan approval, `src/superclaude/core/WORKER-CONTRACT.md:64` | edited (one sentence added at its end) | Says the approval the coordinator carries is read from GitHub evidence under the issue-pipeline rules and that WC-3 covers Rulings, grant rows and pass records and does not change this mechanism. Plan hash, `check-approval` and ack steps unchanged. |
| "never on silence" list, line 195 ("writes or drafts a Ruling") | unchanged | About what a coordinator never does on silence; it does not state who may confirm. |
| Resume item 2 (hand-back), line 274 | edited (parenthetical added) | A person's explicit hand-back is a confirmation; it now points to the WC-3 definition. |
| Resume item 3 (the Ruling line check, items (1) to (7)), lines 279 to 285 | unchanged | Mechanical checks of the ledger line; they say nothing about the channel of confirmation. Provenance wording lives in refs/ledger.md (Task 4). |
| Issue-pipeline "Plan approval" bullet, line 305 | edited (sentence added at its end) | Says the approval is GitHub evidence accepted by `stage-status`, not the coordinator's word, and that the WC-3 definition leaves this mechanism unchanged. |
| Issue-pipeline "Completion" bullet, line 307 | unchanged | Mentions the grant row only as the control for the `complete` verb; the grant-row rule is pointed to from the "Never" bullet. |
| Issue-pipeline "Never" bullet, line 308 | edited (parenthetical added) | A grant row is recorded from the person's confirmation as WC-3 defines it. |

Open question for the owner (not changed here): whether the GitHub plan-approval path should also accept a dashboard response. It is a separate mechanism from the Ruling, grant row and pass record confirmations that WC-3 covers.
