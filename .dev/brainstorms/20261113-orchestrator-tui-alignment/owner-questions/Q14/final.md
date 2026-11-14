# Q14 final: what "#339 is complete" means for the start gate of issue #423

Q14 is owner question 14 in the merged requirements (merged-requirements.md:541). Issue #423 is Orchestrator v2, a planned advisory knowledge layer that is not built; its body says it starts "after #339 is complete". Issue #339 is Orchestrator mode; its Phase 1, the read-only sweep, is open as PR #539. Proposal A is "PR #539 merged; the live capture gates only the v2 features that read live values"; proposal B is "PR #539 merged, the capture recorded, and the sweep's `working` class restored in code"; proposal C is "PR #539 merged plus the capture recorded".

## Debate result

Winner: proposal C, confidence 80 percent. Advocates agreed 3 of 3 on their unassigned pick (the proposal each would choose if not assigned one): all three picked C. The debate converged at 82 percent of scored points against an 80 percent threshold; the two unresolved points (the role of the capture and whether design should wait for live values) were split only on assigned positions (adversarial/debate-transcript.md).

The evidence that decided it:
- The shared capture (work item XC-03, a one-time read-only record of live Orca values) is a record; restoring the `working` class is a later code change. The spec's weak point W5 says "The gate as worded conflates a record with a code change" (merged-requirements.md:415), and the adjudicated findings say the capture "unblocks" the class (alignment-findings-adjudicated.md:335).
- Proposal C needs no spec change: the gate check V2-02 already says "if Q14 means \"capture recorded\", (2) suffices" (merged-requirements.md:399), and the class-restore item SW-14 is already conditional (merged-requirements.md:203).
- The sweep's `working` rule is switched off today because the live field names were never captured (src/superclaude/cli/sweep/classify.py:251-257), so the capture is what v2's design actually needs.

Proposal A (merge only). Strength: the only gate a missing Orca session cannot stall; the Orca app was unreachable on 2026-11-13 (merged-requirements.md:604). Weakness: its per-feature gate needs a list of live-value fields that only the gated design would produce, and it risks rework when the capture contradicts assumptions; its own advocate picked C.

Proposal B (class restored in code). Strength: the only gate proved by a passing test, and the most literal reading of the adjudicated wording; it names the real risk that the capture may show the `working` rule cannot be built. Weakness: puts a code PR, a grant and a possible sweep redesign on a planning gate for an advisory layer; its own advocate picked C.

Proposal C (merge plus capture recorded). Strength: the spec's default; a gate a dated ledger entry can check; v2 designed with real live values. Weakness: still waits on a live capture, and v2 may launch while the sweep shows working sessions as "could not determine".

## Final recommendation

Answer: "#339 is complete" for #423 means PR #539 merged and the #534 shared capture recorded; restoring the `working` class is not part of the gate; `/sc:close`, resume and the trust layer are prerequisites only if the v2 brainstorm decides v2 relays to agents. The dated gate entry also states whether the recorded values are enough to build the `working` rule. Optionally, the owner may set a date after which, if the capture still cannot run, the gate drops to "PR #539 merged" with live-value fields marked pending. Confidence: 80 percent. Strongest reason: the capture is what v2's design needs, and gating on a record rather than a code change keeps the check simple and matches the spec as written. Equals the spec's recommended answer: yes (its default reading), with the sufficiency statement and the optional fallback added (merged-proposal.md).

## What would change the answer

If the capture shows the `working` rule cannot be built from what Orca exposes, proposal B's concern becomes real and the owner may want v2 to wait for a sweep redesign; if Orca stays unreachable for a long time, proposal A's merge-only gate becomes the practical choice.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer interprets the gate wording in the owner's own issue and sets when a whole program phase may start, and only the owner knows what they meant by "complete" and whether to set a fallback date. The debate converged 3 of 3, so the owner can confirm in one line.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q14/adversarial/
- fallback_mode: false (three spawned advocate sub-agents; diff analysis and merge done by this worker directly, as recorded in return-contract.yaml; protocol skill loaded at Q11 and applied as written)
