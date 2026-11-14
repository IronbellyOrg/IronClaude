<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: PR #539 merged plus the shared capture recorded, with a sufficiency check

<!-- Source: Base (original) -->
## Answer

For #423, "#339 is complete" means PR #539 (the read-only sweep) is merged and the shared live Orca capture (#534) is recorded. Restoring the sweep's `working` class in code is not part of the gate. `/sc:close`, resume and the trust layer are prerequisites only if the v2 brainstorm decides v2 relays to agents, not only to a person.

<!-- Source: Base (original, modified) - Changes 1, 2 -->
## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; it is also the spec's default reading (merged-requirements.md:541).
- V2-01 (the #423 rewrite) states: "starts after PR #539 merges and the #534 shared capture is recorded"; ADJ's words "that restores the sweep's `working` class" become "that records the values the `working` class needs".
- V2-02 (the gate check) passes on a dated ledger entry citing the merge and the capture record (merged-requirements.md:399). That entry also states whether the recorded values are enough to build the `working` rule's four conditions (classify.py:251-257); if they are not, it is recorded as a known v2 limit and a #534 row. (Change 1)
- SW-14 (restore the class) is not needed for v2; it stays a #534 follow-up.
- Optional: if the owner sets a date and the capture still cannot run by then, the gate drops to PR #539 merged, with live-value fields marked pending in the v2 design. (Change 2)

<!-- Source: Base (original) -->
## What it unlocks

- v2 is designed with the real live values in hand, without waiting for a code PR.
- The gate is a matter of records a ledger entry can check.
- Close to ADJ's recommendation; other phases stay out unless v2 relays to agents.

<!-- Source: Base (original) -->
## What it costs or risks

- v2 may be built while the sweep still shows working sessions as "could not determine", and v2 may not change a sweep class (merged-requirements.md:401).
- Still waits on a live capture, which needs Orca reachable and an answer on who runs it (Q24).
- Departs slightly from ADJ's literal wording.

<!-- Source: Base (original, modified) - Change 2 -->
## What stays unresolved

- When the `working` class is restored.
- Whether v2 relays to agents (brainstorm; Q15 bears on it).
- Whether the owner sets a fallback date.
