# Merge Log: Q10

## Metadata

- Base: variant-3-original.md (proposal C)
- Plan: refactor-plan.md (4 planned changes, overall risk Low, auto-approved 2026-11-14)
- Source variants used: variant-1-original.md (proposal A), variant-2-original.md (proposal B)
- Output: ../merged-answer.md
- Merge date: 2026-11-14
- Changes NOT applied, per plan: A's eleventh allow-list template; B's "leave the sentence until OB-03"; B's "never" as a standing rule.

## Changes Applied

### Change 1: correct only the bullet; keep the true header value

- Status: applied
- Provenance: all three advocates (A-001)
- Before (Answer): "...and its two report sentences are corrected after PR #539 merges to state only what is established."
- After (Answer): "...and after PR #539 merges its report bullet about pending questions is corrected to state only what is established, while its header value "Messages coverage: partial" stays because it is true."
- Before (What happens next, bullet 2): "SW-07 (wave W3, after the #539 merge) replaces the text at `report.py:199,534` with exactly: "...not established." and updates the tests that pin those strings in the same PR (`merged-requirements.md:196`)."
- After (What happens next, bullet 2): "SW-07 (wave W3, after the #539 merge) replaces the bullet at `report.py:534-535` only with exactly: "...not established." The header value "Messages coverage: partial" at `report.py:199` stays (it is true, pinned by `tests/sweep/test_report.py:590`, shown at `docs/designs/orchestrator-mode.md:610`). SW-07 criterion (3), which says both lines carry exactly that text (`merged-requirements.md:196`), is reworded to cover the bullet only, and the tests that pin the bullet are updated in the same PR."
- Title updated to match: "...correct the sweep's bullet now and keep its true header".

### Change 2: a reopen trigger

- Status: applied
- Provenance: proposal A ("If OB-03 shows consumption, this answer turns into 'never'") and C's advocate
- Before (What happens next, bullet 3): "The question may be reopened by the owner after the observer's consumption evidence exists; nothing is scheduled for that."
- After: "The question may be reopened by the owner after the observer's consumption evidence exists: Q10 is reopened when OB-03 and OB-04 have recorded results with the build pinned (OB-05), or if Q6 parks the observer's read; if OB-03 shows consumption, Q10 becomes "neither program reads questions"."

### Change 3: any sweep read needs a new owner-signed allow-list

- Status: applied
- Provenance: proposal B's framing and B's advocate
- Before (What happens next, bullet 1): "The ledger records "Q10: observer's alone for now, date"; `check` stays forbidden for the sweep (NFR-014; `probes.py:49-60`)."
- After: same text, followed by "Any later sweep read of messages needs a new owner-signed allow-list entry (NFR-014); this answer does not grant one."

### Change 4: the coordinator already receives its questions

- Status: applied
- Provenance: proposal A's advocate (concession 1, `WORKER-CONTRACT.md:100-103` as cited in the plan)
- Before (What it costs or risks, bullet 3): "A coordinator that has only the sweep open still sees no pending questions; it must open the observer (whose questions read is itself switched off until Q6 and its tests)."
- After: "The coordinator's own wait already wakes on `question` messages and handles each batch before acknowledging it (`WORKER-CONTRACT.md:100-103`), so the sweep not reading questions costs the coordinator a second view, not its only view. The cost falls on a person who wants a summary screen, which is the observer's job (and the observer's questions read is itself switched off until Q6 and its tests)."

## Post-Merge Validation

- Heading structure: pass. One H1 title, then the five H2 sections in base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Each section has a `<!-- Source: ... -->` comment; the three provenance header comments are present.
- Internal references resolve: pass. Every id and file:line in the merged answer comes from the base or the plan (NFR-014, `probes.py:49-60`, `report.py:199`, `report.py:534-535`, `tests/sweep/test_report.py:590`, `docs/designs/orchestrator-mode.md:610`, `merged-requirements.md:196`, `WORKER-CONTRACT.md:100-103`, OB-03, OB-04, OB-05, Q6, SW-07, W3, PR #539, ADJ X-016). The cited files were not reopened during the merge; they are taken as verified by the plan.
- New contradictions introduced: 0. Checked: the Answer and bullet 2 now agree that only the bullet changes and the header stays; "the question can come back" (costs bullet 1) agrees with the reopen trigger (Change 2); "keeps the sweep's owner-signed allow-list unchanged" (unlocks bullet 2) agrees with Change 3; the "neither program reads questions" outcome is consistent with the sweep never reading under this answer; the Change 4 bullet no longer claims a sweep-only coordinator sees no questions, and nothing else in the document makes that claim. No em dashes or en dashes.

## Summary

- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
