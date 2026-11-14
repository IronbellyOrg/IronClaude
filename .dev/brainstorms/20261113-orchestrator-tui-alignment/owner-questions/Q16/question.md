# Q16: one trust design, or one grant vocabulary and one audit format?

## The question (verbatim from the spec row)

"One trust design, or one grant vocabulary and one audit format?"
Source: merged-requirements.md section 3, row Q16 (line 543). ADJ Part 7 row Q16 (line 786) words it: "Trust: promise one trust design, or one grant vocabulary and one audit record format?"

## The spec's recommended answer

"One vocabulary and one audit format (X-005, 66 percent)". X-005 is the debate point where two reviews contradicted each other on this exact choice; 66 percent is the debate's mean confidence in the recommended side. Source: merged-requirements.md line 543; ADJ line 382.

## Default if unanswered

"PLAN INFERENCE: OB-08 skips decision 6; #423 and Coder#477 promise neither." In words: the #409 correction pass (OB-08, the one ordered edit of issue #409's body) leaves #409's design decision 6 ("Decide one design, not two.") untouched, and the rewrites of issue #423 (Orchestrator v2) and Coder#477 (the workspace listener issue in the IronbellyOrg/Coder repo) promise neither a single design nor a single vocabulary. Source: merged-requirements.md line 543.

## What it gates (work items, in words)

- XC-08 (record the trust vocabulary decision in the owner-decision ledger, then change three issue texts to match). merged-requirements.md line 456.
- OB-08 decision 6 (inside the #409 correction pass, decision 6 becomes "Decide one grant vocabulary and one audit record." only if Q16 = vocabulary). Lines 256 and 701.
- V2-01 (the rewrite of issue #423, Orchestrator v2; Q16 is one of its five clause dependencies). Lines 398 and 730.
- CO-03 (the deferred Coder-repo build of the narrowed workspace listener; Q16 is one of its owner gates). Line 355.
- SW-12 (the deferred "manages work" phases of Orchestrator mode; its Phase 4, the trust layer, is where the vocabulary itself would be defined). Lines 201 and 456.
- Through XC-08 also V2-03 (the v2 brainstorm), V2-04 (v2 first release) and OB-09 (observer release 3, Decision Desk: "every answer path is audited in the vocabulary of XC-08"). Lines 400, 401, 257, 771 (graph row 124).
- Citation note: line numbers in this file were corrected on 2026-11-14 after the Round 1 advocates found three off-row citations; the facts were unchanged.
- Wave: W1 (the first wave after the intake questions). Line 543.

## Facts the question depends on

1. Issue #409 decision 6 currently reads "Decide one design, not two." Source: ADJ line 567 (V4 edit 1 quotes it); diff-analysis.md line 89. The live issue text was not re-read for this file (UNVERIFIED as of today).
2. The two contradicting reviews: review 03 (V3, about Coder#477) accepted "one design" and proposed Edit 7: "The grant format is the one chosen in IronbellyOrg/IronClaude#339 ... This issue does not define a second format." Review 04 (V4, about #423) said: "Do not promise one design in #423 or #409. Promise one grant vocabulary and one audit record format." Source: diff-analysis.md line 89.
3. Reason given for the narrower promise: the three consumers (the #409 observer, #423 v2 and the Coder#477 listener) have different threat models, and signing does not stop poisoned content: #339 comment 2 of 2026-11-05 says "encryption alone is not enough". Source: ADJ lines 295 and 809; diff-analysis.md line 89.
4. V3 itself notes that under watcher option A the watcher's trust is "a different, local model", which supports the narrower promise. Source: diff-analysis.md line 89; ADJ line 809.
5. The debate found the point "not decidable from sources; this is an owner decision". Source: diff-analysis.md line 89; ADJ line 809.
6. No trust layer, grant format, signing scheme or relay exists today. The trust layer is Phase 4 of the deferred "manages work" work (SW-12) and is unbuilt. Source: merged-requirements.md line 129 and line 201.
7. Limit stated by the spec: "Q16's vocabulary does not authorize relay." Source: merged-requirements.md line 574.
8. If Q16 = vocabulary, the spec assigns defining the vocabulary itself to SW-12's Phase 4 row in #534 (PLAN INFERENCE). Source: merged-requirements.md line 456 (XC-08 (3)).
