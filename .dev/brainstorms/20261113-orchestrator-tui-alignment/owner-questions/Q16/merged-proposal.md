<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original) -->
# Proposal C: one shared vocabulary and one audit record, separate mechanisms

<!-- Source: Base (original) -->
## Answer

Promise only one grant vocabulary (the shared names for who may do what) and one audit record format (the shared shape of the log line that says what was granted and used). Each consumer keeps the trust mechanism its own threat model needs.

<!-- Source: Base (original, modified); reason: two bullets appended per Changes #2 and #1 of refactor-plan.md -->
## What happens next if the owner picks it

- The ledger records "Q16: one vocabulary and one audit format" with the date (XC-08 (1)).
- Inside the #409 correction pass (OB-08), decision 6 changes from "Decide one design, not two." to "Decide one grant vocabulary and one audit record." (review 04's edit 1; merged-requirements.md line 456, XC-08 (2)).
- The #423 rewrite (V2-01) and the Coder#477 text promise the vocabulary, not a design (XC-08 (2)).
- Defining the vocabulary itself is assigned to SW-12's Phase 4 (trust layer) row in #534 (XC-08 (3), marked PLAN INFERENCE).
- Release 3 of the observer (OB-09) later audits every answer path in that vocabulary (line 257).
<!-- Source: Variant 2 (proposal-B), "What it unlocks" bullet 2, diff point U-002; merged per Change #2 -->
- The vocabulary and the audit format have one owner, the SW-12 Phase 4 row, and no other issue defines a second vocabulary or audit format.
<!-- Source: Variant 1 (proposal-A), "What happens next" bullet 4, diff point U-001; merged per Change #1 -->
- When SW-12's Phase 4 row is opened, the owner re-confirms this narrow promise with the draft vocabulary in view. This is a checkpoint only; no work is held until then.

<!-- Source: Base (original) -->
## What it unlocks

- OB-08's decision 6 step, V2-01's trust clause and the CO-01 text all have a settled sentence.
- Each consumer can use a model fit for it: the read-only single-host observer, the watcher's local model, the cross-workspace listener, without forcing signing everywhere.
- One audit format means a person can still read grants from all three programs side by side.

<!-- Source: Base (original, modified); reason: one mitigation inserted per Change #3 and one bullet appended per Change #4 of refactor-plan.md -->
## What it costs or risks

- The debate's confidence is only 66 percent (X-005); the point was judged "not decidable from sources" (diff-analysis.md line 89).
- Three mechanisms to build and review instead of one, and a risk that they drift apart beneath shared words.
- A shared vocabulary can hide real differences: the same word ("grant", "read") may mean weaker protection in one program than in another.
<!-- Source: round1-advocate-2.md "Overall" and round1-advocate-3.md "Concessions"; merged per Change #3 -->
- Mitigation: when SW-12 Phase 4 defines the vocabulary, each term states what it actually enforces in each program, so the shared audit record does not suggest equal protection where there is none.
- It does not authorize relay (merged-requirements.md line 574); v2 relay still needs its own decision.
<!-- Source: round1-advocate-3.md "Concessions" (shared injection target); merged per Change #4 -->
- One shared audit format is also a shared injection target. Audit records can carry text from issues, sessions or another program, so they are untrusted input (TB-UNTRUSTED, merged-requirements.md line 632), and every program that reads them must re-sanitise them.

<!-- Source: Base (original) -->
## What stays unresolved

- The vocabulary's actual terms and the audit record's fields; both wait for SW-12 Phase 4.
- How each consumer handles poisoned content (relayed text stays data, V2-04, is a separate rule).
