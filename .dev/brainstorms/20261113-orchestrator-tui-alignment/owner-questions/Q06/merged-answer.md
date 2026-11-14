<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal C) -->
<!-- Merge date: 2026-11-14 -->

# Proposal C: no flip before the seeded test; decide the scope after the evidence is in

<!-- Source: Base (original, modified), Change 1 (from Variant 2, proposal B) -->
## Answer

Do not flip the guard before the seeded consumption test (and the other listed prerequisites) has run; the owner writes the scope sentence, "this Run only" or "any Run my terminal holds", after seeing the test and live-layout records. Note when choosing: "this Run only" means the pinned Run `run_93bfa00cae2b`, which is an old "Claim issue 375" Run, so the narrow scope would let the panel read only that old Run; the choice between the two scopes stays the owner's.

<!-- Source: Base (original, modified), Change 2 (from Variant 1, proposal A) -->
## What happens next if the owner picks it

- Wave W1: OB-03 (seeded test on a throwaway Run, from a terminal that holds no Run) runs under its own permission row; then OB-04 (one live attempt in the holder terminal of a disposable coordinator Run the owner names under Q30); OB-05 records the Orca build string.
- Wave W2: the owner reads those records and writes the scope sentence; only then is OB-06 (the flip pull request) opened from a fresh branch off `origin/master`, quoting the sentence and enforcing it with a test that refuses an out-of-scope Run (`merged-requirements.md:254`).
- If OB-03 shows any seeded message missing, OB-06 stops and the record says "consumes" (`merged-requirements.md:1000`).
- If the live lanes cannot run (the Orca app is not reachable, or Q24 or Q30 is not answered), OB-03, OB-04, OB-05 and OB-06 are recorded in the ledger as "parked by owner, Q6, date", with the trigger "the Orca app answers a read verb and Q24 and Q30 are answered" (the ORCA-AVAILABLE gate, `merged-requirements.md:604`).

<!-- Source: Base (original) -->
## What it unlocks

- The test runs now, so the consumption question (ADJ X-016) gets its first diagnostic evidence.
- The scope choice is made on evidence: if the live attempt shows the panel unusable or lossy, the owner can choose the narrow scope or no flip without having committed in advance (`merged-requirements.md:1001`).
- Matches ADJ's "do not flip the guard before action 4 (a) and (b)" (ADJ line 195).

<!-- Source: Base (original) -->
## What it costs or risks

- A second owner question later (the scope sentence), adding one round of owner latency before the flip.
- The flip PR cannot be built until W2, so the panel stays dark longer.
- The live tests still need the Orca app reachable, Q24 (who runs the live reads) and Q30 (which Run OB-04 reads) answered, and their permission rows.

<!-- Source: Base (original, modified), Change 1 (from Variant 2, proposal B) -->
## What stays unresolved

The scope sentence itself until W2, including whether the narrow scope, which covers only the old pinned Run `run_93bfa00cae2b`, is worth a flip; consumption on any live Run other than the disposable one OB-04 reads (the test is necessary, not sufficient).
