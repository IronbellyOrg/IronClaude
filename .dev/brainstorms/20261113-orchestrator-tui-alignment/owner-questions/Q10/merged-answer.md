<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal C) -->
<!-- Merge date: 2026-11-14 -->

# Merged answer: the observer's alone for now; correct the sweep's bullet now and keep its true header

<!-- Source: Base (proposal C), modified by Change 1 (all three advocates) -->
## Answer

For now only the observer may read questions with `check --all --types question`; the sweep keeps `check` outside its allow-list, and after PR #539 merges its report bullet about pending questions is corrected to state only what is established, while its header value "Messages coverage: partial" stays because it is true.

<!-- Source: Base (proposal C), modified by Change 3 (proposal B), Change 1 (all three advocates), Change 2 (proposal A) -->
## What happens next if the owner picks it

- The ledger records "Q10: observer's alone for now, date"; `check` stays forbidden for the sweep (NFR-014; `probes.py:49-60`). Any later sweep read of messages needs a new owner-signed allow-list entry (NFR-014); this answer does not grant one.
- SW-07 (wave W3, after the #539 merge) replaces the bullet at `report.py:534-535` only with exactly: "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." The header value "Messages coverage: partial" at `report.py:199` stays (it is true, pinned by `tests/sweep/test_report.py:590`, shown at `docs/designs/orchestrator-mode.md:610`). SW-07 criterion (3), which says both lines carry exactly that text (`merged-requirements.md:196`), is reworded to cover the bullet only, and the tests that pin the bullet are updated in the same PR.
- The question may be reopened by the owner after the observer's consumption evidence exists: Q10 is reopened when OB-03 and OB-04 have recorded results with the build pinned (OB-05), or if Q6 parks the observer's read; if OB-03 shows consumption, Q10 becomes "neither program reads questions".

<!-- Source: Base (proposal C), unchanged -->
## What it unlocks

- SW-07 can proceed in W3 with a fixed text; the sweep stops claiming a fact that is unproven (ADJ X-016, 61 percent, unproven both ways).
- Keeps the sweep's owner-signed allow-list unchanged, and keeps the two programs separate (one reader of questions).
- Matches the spec's default, so answering costs nothing beyond recording it.

<!-- Source: Base (proposal C), modified by Change 4 (proposal A's advocate) -->
## What it costs or risks

- "For now" leaves the long-term answer open; the question can come back.
- The corrected sentence says "not established", which itself becomes stale once OB-03 produces a result, so a second wording change may follow.
- The coordinator's own wait already wakes on `question` messages and handles each batch before acknowledging it (`WORKER-CONTRACT.md:100-103`), so the sweep not reading questions costs the coordinator a second view, not its only view. The cost falls on a person who wants a summary screen, which is the observer's job (and the observer's questions read is itself switched off until Q6 and its tests).

<!-- Source: Base (proposal C), unchanged -->
## What stays unresolved

Whether the sweep should ever read questions once consumption is measured; whether the observer's read is safe (Q6).
