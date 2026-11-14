# Merge Log: Q9 merged answer

## Metadata

- Base: variant-1-original.md (proposal A)
- Plan: refactor-plan.md (3 planned changes, overall risk Low, auto-approved 2026-11-14)
- Source variants: variant-2-original.md (proposal B), variant-3-original.md (proposal C); diff-analysis A-001 and A-002 via the plan
- Output: ../merged-answer.md
- Merge date: 2026-11-14
- Executor: merge-executor

## Changes Applied

### Change 1: an ordered Phase 2 fallback with the embedded form before any sidecar

- Status: APPLIED
- Provenance tag: `[Variant 2, proposal B, as corrected by B's advocate]`
- Target: "What happens next", third and fourth bullets
- Before:
  - "When triggered, the Phase 2 package first tries caller-side capture: the caller writes the stdout JSON where it chooses; the sweep itself still writes one report."
  - "If capture fails a named need (for example, a reader that is not the caller), a later PR relaxes NFR-001 and changes the two tests and the contract note registry in the same change (`merged-requirements.md:200`)."
- After: one bullet with a numbered order, moving to the next step only if the previous one fails a named need: (1) caller-side capture of stdout; (2) an embedded copy inside the one dated report, before the `Report complete` footer (`tests/sweep/test_cli_contract.py:1476`), in a fence that backticks in worker-written text cannot close (`sanitize`, `report.py:569-599`, does not touch backticks), with a test that the embedded and stdout copies match apart from `report_path`; (3) only then a separate file, where a later PR relaxes NFR-001 and changes its design line, the two tests and the contract note registry in the same change (`merged-requirements.md:200`).
- Consistency cascade: the Answer's last clause said NFR-001 is relaxed "only if that turns out not to be enough" (that = caller capture). It now reads "if that is not enough, the sweep embeds the JSON object in its one dated report; NFR-001 ... is relaxed only if neither turns out to be enough." The title was updated to match, as instructed. No other text changed.

### Change 2: record now that the JSON has no stored form

- Status: APPLIED
- Provenance tag: `[Variant 3, proposal C, "What happens next" third bullet]`
- Target: "What happens next", new first bullet
- Before: (no such bullet)
- After: "The contract note (XC-05) states: "sweep report JSON v1 is a stdout-only reply; it has no stored form until a named reader triggers SW-11.""

### Change 3: durability and host caveats

- Status: APPLIED
- Provenance tag: `[diff-analysis A-001 and A-002, shared-assumption responses]`
- Target 1: "What it costs or risks", new last bullet
  - Before: (no such bullet)
  - After: "Reports live in the gitignored `.dev/sweeps/` folder and are deleted by hand (`.gitignore:256`; design `docs/designs/orchestrator-mode.md:35`), so reading the Markdown report is a best-effort look-back, not a durable record, and an embedded copy is only as durable as its report."
- Target 2: "What stays unresolved"
  - Before: "Who the first reader is; where a captured file would live and for how long; whether a stored file will ever be needed."
  - After: "Who the first reader is; where a captured file would live and for how long; whether a stored file will ever be needed; which host the first reader runs on. The trigger asks the first reader which host it runs on: a reader on another host (for example a Coder#477 status record) needs a transport none of these options provides."

### Not applied (per plan "Changes NOT Being Made")

- B's "embed now" (C-001, X-001): not applied.
- C's "never, close SW-11" (C-001, C-003, C-005): not applied. Only C's contract-note sentence was taken, reworded by the plan to keep SW-11 deferred.

## Post-Merge Validation

- Heading structure: PASS. One H1 title, then the five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). No skipped levels. Provenance header comments present; one `<!-- Source: ... -->` comment above each H2.
- Internal references resolve: PASS. Every id, path and line number in the merged answer appears in the base, the plan or a source variant (NFR-001, SW-11, W5, XC-05, Q17, A-004, ADJ A-001, PR #539, Coder#477, `docs/designs/orchestrator-mode.md:128`, `:331`, `:35`, `merged-requirements.md:200`, `tests/sweep/test_cli_contract.py:1476`, `report.py:569-599`, `.gitignore:256`). None were invented. The numbered steps (1) to (3) are referenced only within the same bullet.
- New contradictions introduced: 0.
  - Checked: "NFR-001 ... stay as they are; the sweep code does not change" (now) against step 3 relaxing NFR-001 (later, only when triggered): consistent, different times.
  - Checked: the XC-05 sentence "no stored form until a named reader triggers SW-11" against SW-11 staying DEFERRED with that trigger: consistent.
  - Checked: "Keeps PR #539 ... no sidecar" against step 3: consistent, step 3 is a later PR.
  - Checked: the Answer against the ordered fallback: the Answer was adjusted (see Change 1 cascade) so it names the embedded step; without that adjustment it would have implied NFR-001 is relaxed straight after caller capture.
- Writing rules: no em dashes or en dashes in the merged answer.

## Summary

- Planned: 3
- Applied: 3
- Failed: 0
- Skipped: 0
- Note: one consistency edit outside the planned targets (the Answer's last clause and the title), recorded under Change 1.
