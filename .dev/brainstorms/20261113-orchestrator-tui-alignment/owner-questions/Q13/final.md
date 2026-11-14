# Q13 final: may the observer use a bare `orca` binary when the sweep never does

Q13 is owner question 13 in the merged requirements (merged-requirements.md:540). Proposal A is "yes, because the observer proves the binary first; record both rules"; proposal B is "no, change the observer to use the sweep's rule"; proposal C is "no ruling; record both rules as facts".

## Debate result

Winner: proposal A, confidence 72 percent. Advocates agreed 2 of 3 on their unassigned pick (the proposal each would choose if not assigned one): two picked A, one picked B narrowly (55 to 60 percent over A). Every scored diff point had a majority, so the debate converged (adversarial/debate-transcript.md).

The evidence that decided it:
- The observer's lookup (`_find_orca`, `src/superclaude/cli/install_user_setup.py:247-270`) tries `orca-ide` first and accepts a candidate only if `skills list --json` lists the `orca-cli` topic; its own docstring says a bare `orca` on Linux is usually the GNOME screen reader, which the probe rejects.
- Because `orca-ide` is tried first, the observer and the sweep read different binaries only when the environment variable `ORCA_CLI_COMMAND` is set (only the sweep honours it, `src/superclaude/cli/sweep/probes.py:201-202`), or when `orca-ide` is missing or fails its probe. On this host the variable is unset and both programs read `orca-ide`. INV-016 (an invariant-probe finding, LOW) found no host where the difference mattered.
- All three advocates agreed the probe proves the program is Orca, not that it is the same Orca the sweep reads. That limit is now stated in the answer.

Proposal A (yes, record both). Strength: no code change, keeps working where `orca` is the Orca command-line shim, gives the contract note (work item XC-05, the planned note on how the observer and the sweep relate) a verdict and a reason a future caller can copy; it is the spec's recommendation. Weakness: the probe does not prove sameness, and it accepts a two-rule state.

Proposal B (align the observer). Strength: the only option that makes both read-only programs read the same binary, which the planned comparison of the observer's dispatch ids with the sweep's row ids (work item XC-04) relies on; it found that a failed or slow `orca-ide` probe makes the observer fall back to `orca` with no log (`install_user_setup.py:257-267`, confirmed). Weakness: changes merged, working code for a divergence never seen, and breaks hosts with only `orca` until a variable is set; its own advocate conceded most of the gain comes from the environment variable, not the bare name.

Proposal C (no ruling). Strength: matches the adjudicated severity ("a note, not a risk row") and the spec's default, and names a detector: record the Orca build string next to each capture. Weakness: gives no rule for the next Orca caller; its own advocate picked A when unassigned.

## Final recommendation

Answer: yes, the observer may fall back to a bare `orca` because it proves the program is Orca before using it; the contract note records both rules, says plainly that the probe does not prove it is the same Orca the sweep reads, records the Orca build string next to each capture, and the owner is asked again if build strings differ, if `ORCA_CLI_COMMAND` is in use, or if the dispatch-id comparison needs one binary. Two follow-up rows are logged, not fixed: the observer accepts a relative path from PATH where the watcher refuses one (`src/superclaude/cli/issue_watch/launch.py:178-196`), and its fallback after a failed `orca-ide` probe is silent. Confidence: 72 percent. Strongest reason: on a normal host both programs already read `orca-ide`, so the bare-name fallback only applies where `orca-ide` is missing, and there the probe is the guard that matters. Equals the spec's recommended answer: yes, with the limit, trigger and follow-ups added (merged-proposal.md).

## What would change the answer

If the owner sets `ORCA_CLI_COMMAND` on any host, or recorded build strings show the observer and the sweep reading different Orca builds, proposal B (one rule for both programs) becomes the better answer.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: no
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The question literally asks the owner to accept, in the contract note, that two programs may resolve the Orca program differently, which is a written acceptance of a known (low) risk about which program gets executed. The stakes are low and the debate converged, so a short yes or no from the owner is enough.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q13/adversarial/
- fallback_mode: false (three spawned advocate sub-agents; diff analysis and merge done by this worker directly, as recorded in return-contract.yaml; protocol skill loaded at Q11 and applied as written)
