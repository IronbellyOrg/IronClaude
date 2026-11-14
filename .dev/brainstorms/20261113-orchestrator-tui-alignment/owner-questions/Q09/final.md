# Q9 final: should the sweep's machine-readable JSON ever be kept, and how

Q9 is owner question 9 of the alignment spec. The sweep (`superclaude sweep run`, the read-only report a coordinator session makes about its workers, issue #339, PR #539) writes one dated Markdown report and then prints one JSON object to the screen (stdout); the JSON is not saved anywhere. NFR-001 is the sweep's rule "a sweep adds exactly one report file", pinned by its design and two tests. SW-11 is the spec's deferred work item for this decision; wave W5 is the spec's "later phases" batch, which it does not schedule.

## Debate result

- Winner: proposal A (not now; when a named reader needs it, capture from stdout first), merged with parts of B and C. Confidence 73 percent (mean of the advocates' verdicts: 75, 70, 75).
- Agreement: 3 of 3. The advocates for B and C both chose A over their own proposals. All ten debate points had a majority; six were unanimous.
- Deciding evidence: nothing reads stored sweep facts today ("Consumer today: the coordinator or a person; no observer consumer", `merged-requirements.md:221`), and the adjudicated review (ADJ, `alignment-findings-adjudicated.md`) keeps v2 (issue #423) and a Coder#477 status record as possible later readers whose field list should come first (its shared assumption A-001, line 361). Checked on 2026-11-14: reports are written to the gitignored `.dev/sweeps/` folder and deleted by hand (`.gitignore:256`; design `docs/designs/orchestrator-mode.md:35`), so no option that relies on the reports is a durable store.

Proposal A (not now; caller capture first in Phase 2; relax NFR-001 only if needed). Strength: changes nothing today, keeps PR #539 as reviewed, and leaves the field list to the first real reader. Weakness: settles nothing, spreads storage rules across callers, and jumped straight to relaxing NFR-001 as its fallback.

Proposal B (embed the JSON in the one dated report). Strength: the only way found to keep the facts without a second file, so NFR-001 survives (unanimous on that point). Weaknesses, verified: appending at the very end breaks a pinned test that requires the report to end with "Report complete" (`tests/sweep/test_cli_contract.py:1476`); the report's text cleaner does not handle backticks (`report.py:569-599`), so worker text could break a fenced block; and it builds a store before any reader exists, inside reports that are not kept. Its own advocate voted A, keeping B's form as the second fallback.

Proposal C (never store it; close SW-11). Strength: removes an open item and keeps the observer and the sweep separate. Weakness: "never" contradicts the review's own candidate readers and the conditional link to v2's first release (`merged-requirements.md:401`), and a rule against callers saving stdout cannot be enforced. Its own advocate voted A, keeping C's idea of writing down now that the JSON has no stored form.

## Final recommendation

Not now. Write one sentence into the planned contract note now: the sweep JSON is a stdout-only reply with no stored form until a named reader asks for it. When a reader (v2, a status record, or the observer if Q17 becomes yes) names its need, try in order: the caller saves stdout; else the sweep embeds the JSON inside its one report, before the "Report complete" line, in a backtick-safe block, with a test that both copies match; and only then a separate file, which relaxes NFR-001. Confidence 73 percent.

Single strongest reason: no reader exists to define what should be kept, where, or for how long, and today's reports are not durable, so storing now buys nothing and closing the door for good contradicts the review.

Equals the spec's recommended answer: yes, with two additions (the stdout-only sentence now, and the embedded-copy step before any NFR-001 change).

## What would change the answer

If a reader is named now (for example v2's first release decides it needs past sweep facts), the Phase 2 work starts immediately, and the embedded-copy form (B, corrected) becomes the likely choice.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences: The recommendation equals the spec's default, changes no code, no rule and nothing in PR #539, and every later step needs its own pull request and trigger. The only owner knowledge involved (whether a reader is coming) is asked again automatically when that reader appears.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q09/adversarial/`
- fallback_mode: false (three advocates spawned in parallel as separate agents; merge by a merge-executor agent; depth quick, Round 1 only)
