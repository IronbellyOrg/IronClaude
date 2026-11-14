# Proposal C: one shared vocabulary and one audit record, separate mechanisms

## Answer

Promise only one grant vocabulary (the shared names for who may do what) and one audit record format (the shared shape of the log line that says what was granted and used). Each consumer keeps the trust mechanism its own threat model needs.

## What happens next if the owner picks it

- The ledger records "Q16: one vocabulary and one audit format" with the date (XC-08 (1)).
- Inside the #409 correction pass (OB-08), decision 6 changes from "Decide one design, not two." to "Decide one grant vocabulary and one audit record." (review 04's edit 1; merged-requirements.md line 456, XC-08 (2)).
- The #423 rewrite (V2-01) and the Coder#477 text promise the vocabulary, not a design (XC-08 (2)).
- Defining the vocabulary itself is assigned to SW-12's Phase 4 (trust layer) row in #534 (XC-08 (3), marked PLAN INFERENCE).
- Release 3 of the observer (OB-09) later audits every answer path in that vocabulary (line 398).

## What it unlocks

- OB-08's decision 6 step, V2-01's trust clause and the CO-01 text all have a settled sentence.
- Each consumer can use a model fit for it: the read-only single-host observer, the watcher's local model, the cross-workspace listener, without forcing signing everywhere.
- One audit format means a person can still read grants from all three programs side by side.

## What it costs or risks

- The debate's confidence is only 66 percent (X-005); the point was judged "not decidable from sources" (diff-analysis.md line 89).
- Three mechanisms to build and review instead of one, and a risk that they drift apart beneath shared words.
- A shared vocabulary can hide real differences: the same word ("grant", "read") may mean weaker protection in one program than in another.
- It does not authorize relay (merged-requirements.md line 574); v2 relay still needs its own decision.

## What stays unresolved

- The vocabulary's actual terms and the audit record's fields; both wait for SW-12 Phase 4.
- How each consumer handles poisoned content (relayed text stays data, V2-04, is a separate rule).
