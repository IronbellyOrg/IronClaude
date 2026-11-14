# Q11 final: which static report goes in the coordinator's chat

Q11 is owner question 11 in the merged requirements (merged-requirements.md:538). Proposal A is "both reports, now"; proposal B is "the sweep summary only, until the contract note exists"; proposal C is "no recurring chat report yet; park the clause".

## Debate result

Winner: proposal B, confidence 85 percent. Advocates agreed 3 of 3 on their unassigned pick: each of the three advocate sub-agents, asked which proposal it would choose if it were not assigned one, chose B. On their assigned positions they split on the core choice (diff points C-001 and X-002 of the diff analysis), and the debate converged at 82 percent of scored points against an 80 percent threshold (adversarial/debate-transcript.md, "Convergence Assessment").

The evidence that decided it:
- B needs no edit anywhere: section 6.7 of the spec (the coordinator's status output rule) already says it (merged-requirements.md:1040), and the sweep skill already prints counts and the report path as its one exempt reply (src/superclaude/skills/sc-sweep-protocol/SKILL.md:31-43).
- The #409-style static report already exists as the sweep's report file: its layout was copied from #409, the observer dashboard issue (docs/designs/orchestrator-mode.md:603). That matches the owner's 2026-11-07 first-PR choice of "a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:17). The chat reply points at that file. This removed most of proposal A's fidelity advantage.
- Naming the observer in the coordinator's rules before the contract note (the planned note that fixes one word list and the field matching between the observer and the sweep, work item XC-05) mixes two vocabularies; the source review advised against it (variant-5-original.md:216, :222).

Proposal A (both, now). Strength: closest to #339's literal wording, since the observer's one-shot text is a fleet picture and writes no file (fact E-17 of the adjudicated review findings, .dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md:143); the only proposal that flagged that the observer's gate test Q-1 (an unbound terminal cannot read another terminal's Run, where a Run is one coordinated piece of work in Orca, the local agent-orchestration app) failed, so the coordinator-terminal case is unverified (same file, line 87). Weakness: needs unscheduled edits to the worker contract's coordinator loop rule (WC-16), the sweep skill's tool list and the output style; its 3-minute benefit assumes a loop that is not built; its own advocate picked B when unassigned.

Proposal B (sweep summary only, until the note). Strength: zero edits, matches the spec, the shipped skill and the source review's advice word for word (variant-5-original.md:222). Weakness: the chat text is counts plus a path; "until the note exists" has no date; the 3-minute end of "3 to 5 minutes" is not met because the sweep is capped at once every 5 minutes (WORKER-CONTRACT.md:109).

Proposal C (neither yet). Strength: the most honest about what exists: no coordinator loop exists to print anything every 3 to 5 minutes, and the sweep reply is exempt only for an actual `/sc:sweep` run (src/superclaude/output-styles/pragmatic.md:23). Weakness: drops part of the scope the owner chose on 2026-11-07 (seed-brief.md:17, conceded by its own advocate), and edits spec text for no gain.

## Final recommendation

Answer: the static chat report is the sweep's counts-and-path reply only, until the contract note exists; record in the ledger that no recurring loop exists yet, so no "every 3 to 5 minutes" cadence is claimed as met; and before the observer's text ever joins, check that `superclaude observe --once --run <run>` from the coordinator's own terminal shows that coordinator's Run. Confidence: 85 percent. Strongest reason: the #409-layout report the owner asked for already exists as the sweep's report file, so this answer meets the owner's recorded scope with no edit. Equals the spec's recommended answer: yes, with two added caveats (no cadence claimed; the Q-1 check) taken from proposals C and A (merged-proposal.md).

## What would change the answer

If the owner says the "static report in chat" must show the fleet itself in the chat window (not a pointer to the report file), proposal A becomes better, once the Q-1 check passes from a coordinator terminal.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The answer gates no work item, changes no file, and equals the default that applies if the owner never answers. The owner's intent is only partly involved, because their 2026-11-07 scope record already names the #409-layout static report that the sweep's report file provides.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q11/adversarial/
- fallback_mode: false (the three advocates were spawned sub-agents; the diff analysis and the merge were done by this worker directly, as recorded in return-contract.yaml)
