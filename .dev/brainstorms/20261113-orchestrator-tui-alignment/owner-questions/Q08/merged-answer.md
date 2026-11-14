<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal C) -->
<!-- Merge date: 2026-11-14 -->
# Q8 merged answer: write the owner's direction-selection record now, covering every gate field

<!-- Source: Base (proposal C), modified by Change 1 (from proposal A and C's advocate concession 1) -->
## Answer

The owner writes one dated paragraph, in their own words, that records every field the direction-selection gate checks (field list from `acceptance-tests.md:70` on `origin/master`): the date, the option chosen (the staged direction), who decided, where the owner's statement lives, the default before questions are observed, the default after, the post-link choice or its deferral, the fallback date, the stack confirmation, the command name (`superclaude observe`) and the owner's confirmed reading of "production integration". The post-link choice and the fallback date may be written "deferred to release 3". #409's acceptance criterion 1 stays as written and is then met by citing that record.

<!-- Source: Base (proposal C), modified by Change 1 (first bullet), Change 2 (BC-18 bullet, from C's advocate concession 3 and proposal A) and Change 3 (new interim bullet, from proposal A) -->
## What happens next if the owner picks it

- The owner writes the paragraph, covering every field listed in the Answer, in a file at a location of the owner's choosing (UNVERIFIED where; `merged-requirements.md:250`) and the ledger records its path and date (OB-02).
- Agents cite it and never edit it (`release-gates.md:22`).
- OB-08 (the #409 correction pass) posts BC-18 changed to point at the record (the status line becomes "direction selected 2026-11-08 (staged); confirmed in the owner's record of <date>, <path>, written after releases 1 and 2 shipped"), instead of "not met as recorded".
- If the record does not exist when OB-08 posts, BC-18 posts as proposed, with the status line "not met as recorded", instead of being left out as the spec default would do.
- OB-09 (release 3) is no longer blocked by OB-02.

<!-- Source: Base (proposal C); third bullet modified by Change 4 (from proposal B) -->
## What it unlocks

- Closes the one open item the debate found on the observer's direction (ADJ A-003, 96 percent: "only the selection record is open").
- Keeps the acceptance criterion unchanged, so no one can say the bar was moved.
- The paragraph may cite the owner's earlier decisions (2026-11-08 "Stage it", 2026-11-11) as background and say that the staged direction chosen then still stands, so the direction part is short to write. The 2026-11-08 file says it was "Recorded by an Orca worker" (its line 3), so it supports the owner-written record but cannot replace it.
- Fixes the meaning of "production integration" in the owner's words, which later releases and #409 readers can rely on.

<!-- Source: Base (proposal C); gate-field bullet replaced by Change 1 -->
## What it costs or risks

- Owner writing time, and the owner must choose where the file lives.
- The paragraph is longer than a three-item note, because it must cover every field the gate checks; two of those fields (the post-link choice and the fallback date) may be written as deferred to release 3.
- It records retroactively a selection already acted on (releases 1 and 2 shipped first), so it documents rather than precedes the decision.
- If it cites the 2026-11-08 record, that file must first be saved from the sibling worktree (Q7).

<!-- Source: Base (proposal C), unchanged -->
## What stays unresolved

Where the record lives; whether release 3's later choices (post-link, fallback date) need a second dated record.
