# Q5 final: how the observer and the sweep relate

Terms used here: the observer is `superclaude observe`, the read-only terminal dashboard of Orca workers built for issue #409 and merged. The sweep is `superclaude sweep run`, the read-only report a coordinator session produces about its workers (issue #339, PR #539, still open). The contract note is a planned short design document, `docs/designs/observe-sweep-contract.md`, that would record what each program publishes and what their shared words mean. XC-05 drafts it, XC-06 is its comparison test, XC-07 lands it with links; XC-04 is the one planned comparison of real ids between the two programs. Q9 asks whether the sweep's JSON output is ever kept; Q17 asks whether the observer should ever show sweep facts.

## Debate result

Winner: proposal B (keep both programs separate, joined by one written contract note, no runtime link in version 1), confidence 75 percent. Agreement: 3 of 3; all three advocates, including those for the panel and the defer options, recommended B at 75 percent. Convergence 100 percent; B won all 12 decided points.

Deciding evidence: the debate's own verdict was "one short written note, no runtime link in version 1 ... the main product of the debate" (ADJ Part 2.3, line 222); the sweep's JSON is printed to the screen only and every run writes a report and runs `git status` in every worktree (ADJ Part 8, line 808); the observer shows no sweep classes today (ADJ E-06), so there is no on-screen disagreement for a panel to fix yet; and the note's contents are kept stable inside PR #539 by the rule "Add no JSON keys and no files inside #539" (ADJ line 210), so a draft now is cheap.

- **Proposal A (observer panel reading a captured copy of the sweep JSON).** Strength: the only option that puts one classification of a session in front of the person, as the live #409 body still proposes ("If the observer built its own collector, two programs would classify the same session and could disagree", body line 55). Weakness: reverses three debate verdicts; would show sweep data up to 5 minutes old beside observer rows that count as stale after 45 seconds; depends on a join never compared on real ids; empty on a host with no coordinator. Kept as the named later path if Q17 becomes "yes".
- **Proposal B (one contract note).** Strength: fixes today's drift (two files both called "v1", three vocabularies, two Orca allow-lists that disagree on one command) with no change to either program, plus one test that fails when either program changes a shared word without the note. Weakness: documents disagreement rather than removing it; the test guards words, not meanings; the draft may need revising if PR #539's constants change before merge.
- **Proposal C (write nothing yet).** Strength: waits for the one fact the debate could not establish (whether the ids match). Weakness: its own costs admit the draft is cheap now; the note is needed under every surviving option; its trigger depends on two uncertain events with no fallback. Its re-ask trigger was kept.

## Final recommendation

Keep both programs and write one contract note: draft it now on a branch from master, and land it with its comparison test and links after PR #539 merges and the real-id comparison runs. The note's word table states each program's stale threshold. Once the comparison is recorded, ask Q17 (an observer panel for sweep facts) once more; if the answer is then "yes", the panel reads a copy captured from the coordinator's regular pass and never runs the sweep itself. The #409 correction pass records this choice so the #409 body stops proposing the opposite. Confidence 75 percent. Strongest reason: it removes the confusion that exists today without coupling two independently built programs, and every other option still needs the note.

Equals the spec's recommended answer: yes ("One note; keep both programs"), with the debate's additions above. The full merged text is `merged-proposal.md`.

## What would change the answer

If the owner says that one classification of each session on the screen they watch matters more in version 1 than keeping the two programs independent, proposal A (the panel, fed by a captured copy) becomes the better answer.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The debate converged 3 of 3, the answer is a reversible document inside this repository that grants no authority and accepts no risk, and the spec already proceeds on it as the provisional default. The only owner-intent element (whether one on-screen classification matters more) is preserved as a named later question (Q17) rather than decided here.

## Debate record

- Adversarial folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q05/adversarial/`
- fallback_mode: false (three advocate sub-agents and one merge-executor sub-agent were spawned; scoring and the plan were done inline by this worker)
