# Owner ruling, Phase 5 gate (2026-11-18, given in chat)

Conflict: rubric row RB-04 (High) says the count line `seen, not resolved: N | closed by evidence: unavailable (no source)` must be whole on one line also at 80 columns; plan Task 20 says the 80 column screen stays as Phase 4 left it (the short count line `... unavailable`).

Question put to the owner: which wins? Owner answer, verbatim: "Reword 'seen, not resolved' to mean the same thing but be 10 chars or less - can include symbols. Propose 5 and choose best. Same for closed by evidence. Everything else approved."

Candidates proposed and chosen (plain ASCII only, because a non-ASCII symbol becomes `?` in ASCII mode):
- `seen, not resolved`: seen, open (overclaims: reads as confirmed open); unresolved (drops "seen"); seen,unres (cryptic); **seen !done (chosen)**; seen no-fix (11 characters).
- `closed by evidence`: closed-ev (cryptic); proof-shut (odd); by proof (drops "closed"); shut: ok (drops "evidence"); **proof-done (chosen)**.

Applied: at 80 columns only, the questions list count line reads `seen !done: N | proof-done: unavailable (no source)`. At 160 and 116 columns (the strip) and in the record and snapshot, the full words stay. RB-04 (c) and (d) are read with these short forms at 80 columns; the rubric text is untouched (frozen).
