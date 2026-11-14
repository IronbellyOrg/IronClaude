# Proposal C: not now; name the blind spot in the docs and decide the label together with the watcher handoff design

## Answer

No label for now. The sweep keeps today's behaviour for sessions with no Orca Run, and both programs' documents say plainly that a Run-less session may have been started by the issue watcher and the sweep cannot tell. The labelling question is reopened only when the design of the watcher-to-orchestrator handoff (work item SW-13, the #444 sub-orchestrator evaluation) is accepted.

## What happens next if the owner picks it

1. SW-10 (the label work item) is recorded as "not scheduled: owner answer Q21 = not now" in the #534 follow-up table, with the reopen trigger "SW-13 design accepted".
2. The contract note draft (XC-05) and the sweep design keep the sentence ADJ already asks for: "Run-less sessions (watcher-launched, person-started) are not observable by either program today" (ADJ lines 227, 242), plus one sentence that the sweep may show a watcher session as a person's session.
3. FU-1 still records its item (e) (the agent row), so the evidence exists when the question is reopened; nothing is built on it yet.
4. When SW-13 is designed, it chooses between a label and binding the handed-off session to a Run. WA-07's item (3) already allows either ("visible to the sweep as a labelled row (SW-10) or bound to a Run", merged-requirements.md line 309).

## What it unlocks

- No code on a signal nobody has measured: D-B (does `prompt` hold the claim) is unresolved, and on 27 live rows `prompt` was empty or not a slash command (ADJ line 162).
- Avoids building a label that the handoff design may make unnecessary: if the handoff binds the session to a Run, the sweep already sees it as a worker.
- Wave W4 has one item fewer; no change to the allow-list.

## What it costs or risks

- Until SW-13, a watcher session can appear in the sweep as a person's session (the "person_active" rule fires when `person_started` is true and the transcript is recent: `classify.py:302-315`). The error direction is the safer one, because person sessions are never messaged (WC-16), but a person reading the report may be misled about who started a session.
- WA-07 loses one of its two routes until the question is reopened, so the handoff design must either bind to a Run or reopen Q21.
- The question returns later, and the person answering it then may not have this context.

## What stays unresolved

- D-B and D-A, recorded by FU-1 but not acted on.
- Whether a label is needed at all; decided with SW-13.
