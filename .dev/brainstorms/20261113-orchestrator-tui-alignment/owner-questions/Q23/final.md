# Q23 final: is a `reclaimable` worker live, historical or its own state?

`reclaimable` is one of the states Orca (the local app that runs agent workers) reports for a worker. The observer (`superclaude observe`, the built read-only dashboard of Orca workers) hides only `released` and `retained` workers by default (`src/superclaude/cli/observe/view.py:35`), so reclaimable workers stay on its default screen. The answer goes into the mapping table of shared words in the contract note between the observer and the sweep (work item XC-05) and is a prerequisite of the observer's guard-flip PR (OB-06, the change that turns on its coordinator-questions read).

## Debate result

Winner: proposal C ("its own state, shown with Orca's word, until its meaning is known"), confidence 75 percent. Agreement: 2 of 3 advocates judged C best overall; the proposal A advocate itself chose C now and A as a follow-up; the proposal B advocate preferred B amended with C's reopen step. Point agreement 8 of 9 (89 percent). C scored 0.925 against A's 0.897 and won on the tiebreaker of debate points.

Deciding evidence: (1) Orca's definition of `reclaimable` is in no file read (negative evidence: search of `src/`, `docs/`, `.dev/issues/409` on 2026-11-14). (2) The observer's own recorded sample (`src/superclaude/cli/observe/fixtures/golden-success.json`, "one redacted live worker-list read", checked 2026-11-14) shows all 9 reclaimable workers with a finished task, resources still held (`releaseState: not_requested`), next action `release`, and liveness `unverifiable`. (3) The observer's hide rule looks only at the state, not at liveness (`view.py:363-366`), so hiding the state would hide a worker even if it were still running.

- **Proposal A (historical, hide it).** Strength: a default view that shows working workers; at the probe there were 27 reclaimable and 0 active (invariant probe INV-023). Weakness: hides possibly-running workers on an unconfirmed meaning and needs a code change.
- **Proposal B (live side, keep as built).** Strength: no code change; held resources stay in front of a person, matching next action `release`. Weakness: the word "live" is wrong for a finished task (its advocate conceded); the crowded view stays.
- **Proposal C (own state).** Strength: claims nothing the evidence does not show; already how the built observer treats any other state; no code change. Weakness: does not fix the crowded view and needs a real trigger to reopen.

## Final recommendation

Record `reclaimable` as its own state, shown with Orca's word, neither live nor historical, with the sample facts written next to it as observations; apply the same rule to `release_pending` and `release_unknown`. Reopen it through the shared read-only Orca capture (XC-03, wave W1): add Orca's help text for terminal states and one detail read of one reclaimable worker. If that shows release is automatic and the session has exited, hide it with the historical workers (proposal A); if release needs a person, label it "not historical: awaiting release" (proposal B). Confidence 75 percent. Strongest reason: it is correct whether or not a reclaimable worker's session has exited, and costs nothing now. Equals the spec's recommended answer: yes, with a named reopen step added (merged text: `merged-proposal.md`).

## What would change the answer

One Orca read showing what `reclaimable` means: if it confirms the session has exited and release is automatic, proposal A becomes better; if release needs a person, proposal B's wording becomes better.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: no
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The recommended answer equals the spec's default, changes no code and is reversed by editing one table row, and the debate converged on it. The real open fact is Orca's definition, which a read-only capture settles, not the owner's taste.

## Follow-up candidate found during the debate (out of scope for Q23, not acted on)

In the same fixture, 2 workers in state `retained` have `workerState: ready` and `dispatchStatus: dispatched`, which looks unfinished, and the observer hides `retained` workers by default (`view.py:35`). If that sample is representative, the observer may hide workers that have not finished. One sample only; worth its own check.

## Debate record

- Adversarial folder: `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q23/adversarial/` (diff-analysis.md, round1-advocate-V1/V2/V3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text `Q23/merged-proposal.md`.
- fallback_mode: false (three advocates and the merge executor were spawned as sub-agents; diff analysis, scoring and base selection were done by this worker in the debate-orchestrator role).
