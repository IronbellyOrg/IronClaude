<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal A) -->
<!-- Merge date: 2026-11-14 -->

# Q9 merged answer: not now; record that the JSON has no stored form; when a reader needs it, the caller captures stdout first, then an embedded copy in the one report, and only then a separate file

<!-- Source: Base (Variant 1, proposal A); last clause adjusted for consistency with Change 1 (proposal B) -->
## Answer

Do not store the sweep JSON now; in Phase 2, if a reader needs the machine facts, the caller (the coordinator or a wrapper) saves what the sweep prints on stdout; if that is not enough, the sweep embeds the JSON object in its one dated report; NFR-001 ("a sweep adds exactly one report file") is relaxed only if neither turns out to be enough.

<!-- Source: Base (Variant 1, proposal A), first bullet inserted from Variant 3 (proposal C, Change 2), third and fourth bullets modified from Variant 2 (proposal B, Change 1) -->
## What happens next if the owner picks it

- The contract note (XC-05) states: "sweep report JSON v1 is a stdout-only reply; it has no stored form until a named reader triggers SW-11."
- SW-11 stays DEFERRED in wave W5 (later phases) with the trigger "a named reader (v2, a Coder#477 status record, or the observer if Q17 becomes yes) needs stored sweep facts".
- NFR-001, its design line (`docs/designs/orchestrator-mode.md:128`) and its two pinned tests stay as they are; the sweep code does not change.
- When triggered, the Phase 2 package tries these in order, moving to the next only if the previous one fails a named need (for example, a reader that is not the caller):
  1. Caller-side capture: the caller writes the stdout JSON where it chooses; the sweep itself still writes one report.
  2. An embedded copy: the sweep places the JSON object inside its one dated report, before the `Report complete` footer (a pinned test, `tests/sweep/test_cli_contract.py:1476`, requires the report to end with it), inside a fence that backticks in worker-written text cannot close (the existing `sanitize`, `report.py:569-599`, does not touch backticks), with a test that the embedded and stdout copies match apart from `report_path`. Each sweep still adds exactly one file.
  3. Only then a separate file: a later PR relaxes NFR-001 and changes its design line, the two tests and the contract note registry in the same change (`merged-requirements.md:200`).

<!-- Source: Base (Variant 1, proposal A), unchanged -->
## What it unlocks

- Keeps PR #539 and the merged sweep exactly as reviewed: no new key, no sidecar (A-004).
- Leaves the producer simple: the sweep stays a "writes one report, prints one JSON object" tool (`docs/designs/orchestrator-mode.md:331`).
- Lets the first real reader (v2 or a status record) define the field list and retention before anything is stored (ADJ A-001: "v2 names its field list first").

<!-- Source: Base (Variant 1, proposal A), last bullet inserted from diff-analysis A-001 and the shared-assumption responses (Change 3) -->
## What it costs or risks

- Until Phase 2, the JSON exists only for the length of the call; anyone who needs past machine facts must parse the Markdown report.
- Caller-side capture puts the storage rules (location, retention, file mode) on each caller; two callers could store it differently.
- The question returns later; the decision is deferred, not settled.
- Reports live in the gitignored `.dev/sweeps/` folder and are deleted by hand (`.gitignore:256`; design `docs/designs/orchestrator-mode.md:35`), so reading the Markdown report is a best-effort look-back, not a durable record, and an embedded copy is only as durable as its report.

<!-- Source: Base (Variant 1, proposal A), host caveat appended from diff-analysis A-002 and the shared-assumption responses (Change 3) -->
## What stays unresolved

Who the first reader is; where a captured file would live and for how long; whether a stored file will ever be needed; which host the first reader runs on. The trigger asks the first reader which host it runs on: a reader on another host (for example a Coder#477 status record) needs a transport none of these options provides.
