# Q13: may the observer use a bare `orca` binary when the sweep never does

## Question (verbatim from the spec row)

merged-requirements.md section 3, row Q13: "Is bare `orca` acceptable for the observer when the sweep says never?"

ADJ Part 7 wording (alignment-findings-adjudicated.md:783): "Is bare `orca` acceptable for the observer when the sweep's rule is \"never bare `orca`\"?"

## Spec's recommended answer

"Yes; the observer validates the binary with `skills list --json`; record in the note" (merged-requirements.md:540). ADJ adds: "The watcher uses the same rule, so only the sweep differs" (alignment-findings-adjudicated.md:783). Origin: V5 Q9 and O-03 (variant-5-original.md:113, :296); R2-V2 section 2 (round2-rebuttal-V2.md:31).

## Default if unanswered

"PLAN INFERENCE: the note records both rules without a verdict" (merged-requirements.md:540).

## What it gates

- XC-05, "Draft the contract note" (merged-requirements.md:453): the planned file `docs/designs/observe-sweep-contract.md` that records how the observer and the sweep relate; one of its listed contents is "binary resolution (Q13)". Wave W1.
- Graph edge 108: "Q5, Q13, Q22, Q23 -> XC-05, DEC, Note content" (merged-requirements.md:755).

## Facts the question depends on

1. Observer and watcher rule: `_find_orca()` tries `orca-ide` then `orca` from PATH and accepts a candidate only if `<candidate> skills list --json` exits 0 and lists a topic named `orca-cli` (`src/superclaude/cli/install_user_setup.py:36,247-270`, re-read 2026-11-14). Its docstring: "On Linux a bare `orca` outside Orca's own terminals is usually the GNOME screen reader, so each candidate must prove it is Orca before use." The observer imports it (`src/superclaude/cli/observe/adapter.py:21,370`); the watcher mirrors it with an extra absolute-path check (`src/superclaude/cli/issue_watch/launch.py:171-178`; round2-rebuttal-V2.md:31).
2. Sweep rule: `$ORCA_CLI_COMMAND` when set, else `orca-ide`, "never bare `orca`" (`src/superclaude/cli/sweep/probes.py:43,201-202`, re-read; design `docs/designs/orchestrator-mode.md:382`). The sweep makes no probe. The sweep's Orca calls are an owner-signed allow-list of 10 exact templates over 7 verbs (NFR-014; ADJ glossary line 84); `skills list --json` is not among the sweep's templates (ADJ line 231 lists the observer's and watcher's use of it, not the sweep's).
3. The observer ignores `ORCA_CLI_COMMAND` (variant-5-original.md:113, O-03; consistent with the code read in fact 1).
4. INV-016 (invariant-probe finding, LOW, ADDRESSED): observer and watcher use `_find_orca`; the sweep differs; "no host with both names was shown" (invariant-probe.md:23).
5. A-009 (UNRESOLVED, 67 percent): two builds of one Orca release are on record; the sweep compares only the text before the first hyphen and cannot tell them apart; the observer records no Orca version (ADJ E-15, line 141). The note is to "record the Orca build string next to each capture" (ADJ line 233).
6. On this host, run 2026-11-14 inside this agent's shell: `which orca` gives `/home/coder/.config/orca/linux-orca-cli-shim/orca` and `which orca-ide` gives `/home/coder/.local/bin/orca-ide`. Whether the two resolve to the same Orca app and build was not checked.
7. ADJ lists the binary-resolution difference as a contract-note row (ADJ line 243): observer "`orca-ide` then `orca`, accepted only if `skills list --json` names `orca-cli`"; sweep "`$ORCA_CLI_COMMAND` else `orca-ide`, never bare `orca`".
