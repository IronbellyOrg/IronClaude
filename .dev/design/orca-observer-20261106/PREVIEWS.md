# Orca observer: twenty rendered design concepts

**Synthetic, observation-only design prototypes for Stably.ai Orca.** No live integration or operational controls. The human chooses the visual direction before production implementation.

[Issue #409](https://github.com/IronbellyOrg/IronClaude/issues/409) · [Package guide](README.md) · [Design comparison](concepts.md) · [QA and review limitations](QA.md) · [Source ledger](sources.json) · [Data dictionary](data-dictionary.md)

**Offline galleries:** download the complete package ZIP linked from issue #409, extract it and open `index.html`. GitHub displays HTML source; it does not run these galleries in the repository viewer.

[First PDF portfolio](portfolio.pdf) · [Additional agent-supervision PDF](agent-focus/portfolio.pdf)

## First set: observation companions

![Observation concepts contact sheet](contact-sheet.png)

### 1. Signal Bridge
Who needs attention, what work is affected, and how fresh is the observation?

![Signal Bridge](exports/160/signal-bridge.png)

### 2. Fleet Quilt
Stable orchestrator territories containing individually identifiable session cells.

![Fleet Quilt](exports/160/fleet-quilt.png)

### 3. Time Loom
Shared-axis lanes distinguish work, review, queueing, dependency waits and observation gaps.

![Time Loom](exports/160/time-loom.png)

### 4. Worktree Atlas
Recorded base/branch attachments and selected-path peers without declaring unproven conflicts.

![Worktree Atlas](exports/160/worktree-atlas.png)

### 5. Decision Desk
A selected human question beside the affected sessions and their evidence.

![Decision Desk](exports/160/decision-desk.png)

### 6. Proof Gate
Revision-pinned checks, missing evidence and result admission remain separate.

![Proof Gate](exports/160/proof-gate.png)

### 7. Budget Engine
Measured spend subtotals and resource samples with explicit units and incomplete coverage.

![Budget Engine](exports/160/budget-engine.png)

### 8. Relay Map
Purposeful cables represent declared dependencies with evidence references.

![Relay Map](exports/160/relay-map.png)

### 9. Delta Deck
Unresolved context stays visible above new, worsened, resolved and unchanged event lanes.

![Delta Deck](exports/160/delta-deck.png)

### 10. Watchkeeper
A quiet human handover summary with explicit unknowns and source ages.

![Watchkeeper](exports/160/watchkeeper.png)

## Second set: staying on top of the agents

![Agent supervision contact sheet](agent-focus/contact-sheet.png)

### 11. Leverage Board
Which answer has the widest declared downstream effect?

![Leverage Board](agent-focus/exports/160/leverage-board.png)

### 12. Attention Ledger
Which human questions are still unanswered, and who owns the next move?

![Attention Ledger](agent-focus/exports/160/attention-ledger.png)

### 13. Handoff Switchboard
Which orchestrator handoffs carry dependencies?

![Handoff Switchboard](agent-focus/exports/160/handoff-switchboard.png)

### 14. Loop Detector
Where does authoritative attempt history report repeated retries?

![Loop Detector](agent-focus/exports/160/loop-detector.png)

### 15. Collision Lens
Which isolated worktrees touch the same paths and warrant inspection?

![Collision Lens](agent-focus/exports/160/collision-lens.png)

### 16. Outcome Ledger
Did an assignment finish, produce an inspectable report, or receive admission?

![Outcome Ledger](agent-focus/exports/160/outcome-ledger.png)

### 17. Revision Drift
Which checks refer to a revision that is no longer current?

![Revision Drift](agent-focus/exports/160/revision-drift.png)

### 18. Mission Pulse
Which missions show recorded outcomes rather than activity alone?

![Mission Pulse](agent-focus/exports/160/mission-pulse.png)

### 19. Owner Load
How uneven is observed ownership, without pretending session count measures capacity?

![Owner Load](agent-focus/exports/160/owner-load.png)

### 20. Shift Brief
What must a human know before stepping away or handing over?

![Shift Brief](agent-focus/exports/160/shift-brief.png)

## Compact examples

These are separately composed character layouts, not scaled-down screenshots.

### 116-column Fleet Quilt
![116-column Fleet Quilt](exports/116/fleet-quilt.png)

### 80-column Decision Desk
![80-column Decision Desk](exports/80/decision-desk.png)

Browse all compact exports: [116 columns](exports/116/) · [80 columns](exports/80/) · [Additional set, 116 columns](agent-focus/exports/116/) · [Additional set, 80 columns](agent-focus/exports/80/).

## Collaboration and evidence boundary

Use issue #409 to identify the concept, terminal width and specific visual or semantic change being discussed. Suggested starting points are Signal Bridge, Proof Gate and Fleet Quilt, but no direction is approved.

Nineteen offline automated tests passed. An independent review failed earlier snapshots; targeted corrections were applied and parent-inspected, with no fresh independent post-correction PASS. Gallery logic was exercised through a DOM simulation; real browser use, measured user comprehension and operational performance are not established. See QA.md for the exact boundary.
