# Q18: a channel copying the observer snapshot to the TUIBBS host?

## The question (verbatim from the spec row)

"A channel copying the snapshot to the TUIBBS host?"
Source: merged-requirements.md section 3, row Q18 (line 545). ADJ Part 7 row Q18 (line 788) words it in full: "Do you want a channel that copies the observer snapshot from the Coder workspace to the separate TUIBBS host?"

## The spec's recommended answer

"Not before observer R4 or an owner statement that a TUIBBS screen is planned." R4 is the observer's planned fourth release, the remote fleet (ADJ glossary line 92). Source: merged-requirements.md line 545; ADJ line 788.

## Default if unanswered

"ADJ recommendation applies": no channel until one of those two triggers. Source: merged-requirements.md line 545.

## What it gates (work items, in words)

- CO-04 (deferred: the snapshot copy channel to the TUIBBS host). "Not before observer release R4 or an owner statement that a TUIBBS screen is planned (Q18). When opened: a transport, an identity envelope (the snapshot `scope` is only `object` or `"UNKNOWN"`), an age rule (Q22) and re-sanitising are each specified." merged-requirements.md line 356; graph row 82 (line 729).
- CO-01 (text): the reply posted on Coder#477 (the workspace listener issue in the IronbellyOrg/Coder repository) states "the channel per Q18". merged-requirements.md line 353 (Q18 in its owner-question column); graph row 76 (line 723).
- Wave: W5 (the last wave). Line 545.

## Facts the question depends on

1. TUIBBS is the owner's separate TUI platform on a different SSH host; the observer snapshot is shaped so a read-only Go screen there could read it later. ADJ glossary line 91.
2. The observer snapshot ("observe snapshot v1") is a file rewritten every live cycle in the user state directory (`$XDG_STATE_HOME/superclaude/observe/`, mode 0600). ADJ lines 131 and 244.
3. "No document in TUIBBS mentions Coder or Orca (not searched exhaustively)", and the snapshot is "a file in the Coder workspace; something must copy it". round2-rebuttal-V5.md line 20, citing sibling `tuibbs-review/notes-3.md` lines 74 to 84 (sibling worktree files, untracked per ADJ line 457; not re-read here, UNVERIFIED as of today).
4. Before a TUIBBS screen can read anything, four things are missing: a transport, an identity envelope (`scope` is only `object` or `"UNKNOWN"`, with only per-row `hostId` and `hostKind`), an age rule (no liveness field), and re-sanitising. ADJ line 306 (Part 2.7).
5. The owner's 2026-11-08 record says the observer "may become a TUIBBS module" and marks it "Background, not deciding". ADJ line 306; round2-rebuttal-V5.md line 134 (record in a sibling worktree, UNVERIFIED as of today).
6. The source disagreement D-9: "Does the owner want a snapshot-copy channel to TUIBBS at all?" Review 03 (V3) said a Coder-to-host channel is needed; the owner's record said "background, not deciding". Settling fact: "The owner's statement on whether a TUIBBS screen is planned before R4." Owner only. round2-rebuttal-V5.md line 72.
7. Related question Q4 (what "TUI Panel" means): working reading "`superclaude observe`; TUIBBS a possible later reader; single-host; read-only" at about 70 to 75 percent; a TUIBBS reading about 15 percent. merged-requirements.md line 531; ADJ line 306. If the owner answers Q4 with "TUIBBS", "CO-04 becomes the relevant deferred item and Q18 must be asked" (merged-requirements.md line 1177).
8. Related question Q3 (Coder#477): close is recommended "if the observer stays single-host and TUIBBS is not near". ADJ line 773.
9. The spec lists "TUIBBS screen, snapshot transport to another host (Q18), observer release 4 remote fleet, multi-host (A-007)" as out of scope until later. merged-requirements.md line 145. The contract note states "single owner, single OS user, single host" once (merged-requirements.md line 453, XC-05).
10. No transport is selected until Q4, Q18 and the real authentication behaviour are settled (PLAN INFERENCE). merged-requirements.md line 375.
