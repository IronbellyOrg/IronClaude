# Q15 final: must v2 ever deliver a course correction to a session that is not an Orca worker

Q15 is owner question 15 in the merged requirements (merged-requirements.md:542). v2 means issue #423, Orchestrator v2, a planned advisory knowledge layer that is not built. An Orca worker is an agent session started through Orca (the local agent-orchestration app) for one task; non-worker sessions are person-started sessions, sessions the issue watcher launches, and sessions with no Orca Run. Proposal A is "never, as a standing rule for every program"; proposal B is "report only for v2; any wider delivery is a later, separate decision"; proposal C is "yes eventually, behind the #339 trust layer".

## Debate result

Winner: proposal B, confidence 82 percent. Advocates agreed 3 of 3 on their unassigned pick (the proposal each would choose if not assigned one): all three picked B. At the level of individual diff points the debate reached 73 percent, below the 80 percent threshold, because each advocate kept its own long-term direction on three points (C-001, C-004, X-001 in adversarial/debate-transcript.md); per the protocol the base was force-selected by score, and the return contract records status "partial".

The evidence that decided it:
- The contract already says person-started sessions "are never messaged" (src/superclaude/core/WORKER-CONTRACT.md:288), and workers receive coordinator follow-ups only by pulling them (WC-12, WORKER-CONTRACT.md:61).
- No channel into a person-started or watcher-launched session is known (question.md fact 10), and signing does not stop poisoned content (#339 comment 2, "encryption alone is not enough", adjudicated findings line 295).
- If v2 relayed to agents, the unbuilt #339 trust layer would become a v2 prerequisite (adjudicated findings line 699); report-only keeps it off v2's path.
- All three advocates agreed (point X-002) that an answer about v2 should not bind future designs nobody has researched.

Proposal A (never, standing rule). Strength: removes the attack surface for good and turns the contract's "never messaged" into a rule. Weakness: binds "any later automated program" beyond the question; same first-release behaviour as B; its own advocate picked B.

Proposal B (report only). Strength: the adjudicated answer and the default; same first-release safety as A; no new channel or signing scheme; most reversible. Weakness: states no condition for reopening and leaves unattended watcher-launched sessions without automatic correction; both are fixed in the merged answer.

Proposal C (yes eventually). Strength: keeps #423's purpose ("relay them to affected agents", round2-rebuttal-V4.md:68) and names the real gap, unattended watcher-launched sessions. Weakness: commits to a channel that is not known to exist, into sessions the contract says are never messaged, and lengthens v2's path; its own advocate picked B.

## Final recommendation

Answer: v2 reports to the person or the coordinator only and delivers nothing into a non-worker session; for a worker, v2 hands the correction to the coordinator, which decides whether to send a pulled follow-up. The question is reopened only when a delivery channel is named, a threat model for poisoned content exists, it is decided whether a person approves each correction, and Q16 (one grant vocabulary and audit format) is answered. The v2 design shapes its typed fields and audit record so a later delivery release would not need a store migration, and records unattended watcher-launched sessions as the known open case. Confidence: 82 percent. Strongest reason: it gives exactly the same safety as "never" for every release actually planned, without committing the long-term direction before the channel and threat model are known. Equals the spec's recommended answer: yes, with a reopening condition and two design notes added (merged-proposal.md).

## What would change the answer

If a safe delivery channel is found and the owner wants unattended watcher-launched sessions corrected without a person, proposal C becomes the better long-term answer; if the owner wants the boundary closed permanently, proposal A.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The question sits on a trust boundary (whether any program may push content into a person's own session), and the recommended answer narrows a goal stated in the owner's issue #423. All three advocates picked the same answer, so the owner can confirm in one line, though point-level agreement was 73 percent.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q15/adversarial/
- fallback_mode: false (three spawned advocate sub-agents; diff analysis and merge done by this worker directly, as recorded in return-contract.yaml; protocol skill loaded at Q11 and applied as written)
