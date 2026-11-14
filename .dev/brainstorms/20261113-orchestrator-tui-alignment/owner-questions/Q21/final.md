# Q21 final: may the sweep label machine-started sessions separately?

The sweep is the read-only report a coordinator session writes about its workers (issue #339, PR #539, not yet merged). A machine-started session here means a session the issue watcher (the program that starts a claim session for an approved issue) launched, as opposed to one a person opened.

## Debate result

Winner: proposal B ("yes, in Phase 2, reading Orca's agent rows, only after the watcher's first live test shows what they hold"), confidence 78 percent. Agreement: 2 of 3 advocates favoured proposal B overall (the proposal A advocate's own net verdict was "proposal B's process and stop rule, with proposal A's signal as the alternative"); the proposal C advocate held to C but conceded that B's stop rule gives most of C's safety. Point agreement 8 of 10 (80 percent, at the threshold). Deciding evidence: the Orca command B needs, `worktree ps --json`, is already on the owner-signed list of commands the sweep may run (`src/superclaude/cli/sweep/probes.py:55`), so B adds no new input; and B is the only proposal with an explicit "if the recorded fields carry no usable signal, record that and stop" rule, which all three advocates scored best for failure handling.

- **Proposal A (label from the watcher's own record).** Strength: it rests the label on a record the watcher writes on purpose; the debate found that the watcher's store file `dispatch.json` already holds an operation id and launch folder per issue with a checked version number (`src/superclaude/cli/issue_watch/record.py:69-95`). Weakness: it named the wrong input first; the watcher's `status --json` output carries those fields only for entries in state `unknown` (`cycle.py:1308-1323`), its worktree-path fallback would label a person's session as machine-started (the unsafe direction), and it needs a new owner-approved read path.
- **Proposal B (spec's answer).** Strength: no new input, no change to the allowed-command list, gated on a recorded row and a fixture test, explicit stop rule. Weakness: the signal is Orca's free-form `prompt` field, which was empty or not a slash command on all 27 live rows seen (the adjudicated findings file, ADJ, `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` line 162), so "no reliable signal" is a likely outcome; one test row is a sample of one.
- **Proposal C (not now).** Strength: builds nothing on an unmeasured signal, and today's error is the safe one (a watcher session shown as a person's is never messaged; a session with a ccsession tab-map entry already lands as "could not determine": `classify.py:760-767`). Weakness: its trigger (the handoff design, SW-13) has no date, and it silently breaks the dependency row of the later handoff WA-07, which lists the label as a blocker (merged-requirements.md line 309).

## Final recommendation

Yes, in Phase 2, reading Orca's `worktree ps` agent rows only in the shape the watcher's first live test (FU-1) records, with three additions from the debate: (1) the label may only turn "unknown" into "machine-started", never into "person-started", and a missing or unrecognised signal stays "could not determine"; (2) if the recorded row carries no usable signal, the label work stops and records that, and the named alternative is the watcher's versioned store `dispatch.json`, which would need its own owner approval; (3) the blind spot is written into the sweep design now. Confidence 78 percent. Strongest reason: it adds no new input or permission to the sweep and refuses to guess. Equals the spec's recommended answer: partly; the answer is the same, the three additions are new (merged text: `merged-proposal.md`).

## What would change the answer

If FU-1's recorded agent row shows `prompt` and `paneKey` carry nothing usable, proposal A (watcher store) becomes the better route; if FU-1 shows that a watcher launch creates an Orca Run (open item D-A), no label is needed and proposal C wins.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: no
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The answer only permits a reversible, evidence-gated label in a read-only report, adds no command to the sweep's owner-signed list, and the debate converged on it. The one owner-level choice it could lead to (letting the sweep read the watcher's store file) is explicitly left as a separate approval and is not granted here.

## Debate record

- Adversarial folder: `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q21/adversarial/` (diff-analysis.md, round1-advocate-V1/V2/V3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text `Q21/merged-proposal.md`.
- fallback_mode: false (three advocates and the merge executor were spawned as sub-agents; diff analysis, scoring and base selection were done by this worker in the debate-orchestrator role).
- Merge note: the merge executor flagged one wording tension: the cost bullet "a watcher session still shown as a person's" describes today's behaviour for unmatched sessions, while addition (1) limits only what the new label may say. They do not conflict.
