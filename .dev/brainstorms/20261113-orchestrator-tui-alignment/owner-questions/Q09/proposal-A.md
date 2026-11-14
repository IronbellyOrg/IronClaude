# Proposal A: not now; when a reader needs it, the caller captures the JSON from stdout first, and only then consider a stored file

## Answer

Do not store the sweep JSON now; in Phase 2, if a reader needs the machine facts, the caller (the coordinator or a wrapper) saves what the sweep prints on stdout, and NFR-001 ("a sweep adds exactly one report file") is relaxed only if that turns out not to be enough.

## What happens next if the owner picks it

- SW-11 stays DEFERRED in wave W5 (later phases) with the trigger "a named reader (v2, a Coder#477 status record, or the observer if Q17 becomes yes) needs stored sweep facts".
- NFR-001, its design line (`docs/designs/orchestrator-mode.md:128`) and its two pinned tests stay as they are; the sweep code does not change.
- When triggered, the Phase 2 package first tries caller-side capture: the caller writes the stdout JSON where it chooses; the sweep itself still writes one report.
- If capture fails a named need (for example, a reader that is not the caller), a later PR relaxes NFR-001 and changes the two tests and the contract note registry in the same change (`merged-requirements.md:200`).

## What it unlocks

- Keeps PR #539 and the merged sweep exactly as reviewed: no new key, no sidecar (A-004).
- Leaves the producer simple: the sweep stays a "writes one report, prints one JSON object" tool (`docs/designs/orchestrator-mode.md:331`).
- Lets the first real reader (v2 or a status record) define the field list and retention before anything is stored (ADJ A-001: "v2 names its field list first").

## What it costs or risks

- Until Phase 2, the JSON exists only for the length of the call; anyone who needs past machine facts must parse the Markdown report.
- Caller-side capture puts the storage rules (location, retention, file mode) on each caller; two callers could store it differently.
- The question returns later; the decision is deferred, not settled.

## What stays unresolved

Who the first reader is; where a captured file would live and for how long; whether a stored file will ever be needed.
