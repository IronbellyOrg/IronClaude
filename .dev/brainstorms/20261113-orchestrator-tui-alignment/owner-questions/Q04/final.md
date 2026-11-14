# Q4 final: what "TUI Panel" means in the owner's comment on Coder#477

Terms used here: Coder#477 is an open issue in the separate repository `IronbellyOrg/Coder` about a workspace listener; the owner commented on it on 2026-11-13, "Ensure this aligns with Orchestrator and TUI Panel". `superclaude observe` (also called the observer) is the read-only terminal dashboard of Orca workers built for IronClaude issue #409. Its planned later releases are R3 (Decision Desk, a screen for answering coordinator questions) and R4 (reading a remote fleet). TUIBBS is the owner's separate TUI platform on another host. CO-01 is the work item that posts the reply on Coder#477; Q18 is the later question about copying the observer's snapshot to the TUIBBS host.

## Debate result

Winner: a merged answer built on proposal B (name `superclaude observe` without committing to lasting properties), with proposal A's verified present facts added, confidence 64 percent (mean of the three advocates' amended recommendations: 70, 60, 62). Agreement: unmodified, 2 of 3 advocates picked proposal A and 1 picked proposal B; amended, all 3 converged on the same reply line. Every debate point reached at least a 2-of-3 majority (convergence 100 percent); proposal B won 7 points, proposal A 5, proposal C none.

Deciding evidence: `superclaude observe` is the only reading with a built referent and the strongest source support (ADJ Part 2.7, about 70 to 75 percent; the ADJ glossary, line 77, already equates it with "the 'TUI panel' in the owner's wording"). But "single-host" and "read-only" are today's properties: remote fleet is the planned release R4, and whether Decision Desk (R3) writes is UNVERIFIED, so unscoped they could become false in a public reply. And a present-tense "single-host" cannot test the ADJ's close condition for Coder#477, which is about whether the observer "stays" single-host (ADJ line 283).

- **Proposal A (`superclaude observe`; single-host; read-only).** Strength: names the built program in the spec's own line and keeps Q18 at "not yet". Weakness: its properties read as lasting limits and it overstated how it would help Q3 (its advocate conceded both).
- **Proposal B (`superclaude observe` today; no host statement).** Strength: separates the name from release properties, so Q4 does not decide Q3 or Q18 by side effect, and keeps the owner's 2026-11-08 "Background, not deciding" note intact. Weakness: less useful to a Coder#477 reader; "provisional" reads as indecision; it omitted "read-only today", a verified fact.
- **Proposal C (both; a TUIBBS screen planned).** Strength: keeps the TUIBBS sequence visible and would give a narrowed Coder#477 a consumer. Weakness: "planned" has no owner source and contradicts "Background, not deciding"; it would satisfy Q18's own trigger by its wording; the #409 Go-stack lineage it relied on was replaced by the owner with Python plus Rich on 2026-11-08 (ADJ line 187).

## Final recommendation

"TUI Panel" means `superclaude observe`, the #409 dashboard. Post this line on Coder#477 (after you have seen it): "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; later readers, including a possible TUIBBS screen, not decided." Q18 stays at "not yet", and Q3 is decided on its own merits. Confidence 64 percent. Strongest reason: it states only what is true of a built program today, so the public line cannot become false when release R3 or R4 ships.

Equals the spec's recommended answer: partly. Same meaning (`superclaude observe`, TUIBBS a possible later reader), but the debate scoped "single-host" and "read-only" to "today" and added "the #409 dashboard", because the spec's line could read as a lasting limit and would tilt Q3 toward closing Coder#477. The full merged text is `merged-proposal.md`.

## What would change the answer

If the owner meant a TUIBBS screen, or a panel on the Coder side (nobody searched the Coder repository for the phrase; UNVERIFIED), the meaning changes; and an owner statement that a TUIBBS screen is planned would make proposal C right and open Q18.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The question asks what the owner meant by their own words, which only the owner knows; the phrase appears in no owner-written file. The answer is also posted publicly in another repository, so the owner should see the line first.

## Debate record

- Adversarial folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q04/adversarial/`
- fallback_mode: false (three advocate sub-agents and one merge-executor sub-agent were spawned; scoring and the plan were done inline by this worker)
