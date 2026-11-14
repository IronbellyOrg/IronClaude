# Merge Log (Q22)

## Metadata
- Base: Variant 1 (proposal-A), `variant-1-original.md`
- Plan: `refactor-plan.md`
- Executor: merge-executor
- Changes applied: 4 of 4
- Output: `../merged-proposal.md`
- Status: success
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: key the rule on the producer's worst normal write gap
- Status: applied (replace)
- Target: title, "Answer", step 1
- Before: stale = older than 3 x the producer's nominal interval; observer threshold 45 s.
- After: stale file = `generatedAt` age greater than the larger of (a) 3 x nominal interval and (b) the documented longest normal write gap, backoff included. Observer: (a) 45 s, (b) about 75 s (labelled an inference from code, not a measurement), threshold about 75 s; a longer measured gap replaces it. Citations `commands.py:294-297`, `collector.py:28-30` kept.
- Provenance: Variant 3 (round1-advocate-V3.md Strengths, C-002, X-003); round1-advocate-V1.md Concessions (proposed merge)
- Consistency edits made because Change 1 made base text false or incomplete:
  - Title: "three of the producer's own intervals" became "three producer intervals or the producer's longest normal write gap, whichever is larger".
  - Step 2: Coder#477 replacement text and CO-03 obligation now name both values.
  - Step 4: "the interval lives in the note" became "the interval and the longest write gap live in the note".
  - Unlocks bullet 3: "shown stale only after three missed writes" became "not shown as a stale file while it is still writing".
  - Cost bullet 1: "a formula" became "a formula with two terms".
  - Cost bullet 2 (backoff): "can cross 45 s and show stale while alive" replaced by "a stopped observer is flagged only after about 75 s, not 45 s; backoff shows in `source.status`; 75 s inferred, not measured" (wording from round1-advocate-V3.md Concession 3).
  - Cost bullet 3 (`--once`): "stale after 45 s" became "stale after the observer's threshold of about 75 s".
  - Unresolved bullet 1: adds the Coder record's longest write gap.

### Change 2: two ages, never one
- Status: applied (replace)
- Target: "What it unlocks", first bullet
- Before: one meaning of "stale" across screen and file; file reader gets the same 45 s.
- After: file age (`generatedAt`, writer alive) is distinct from data age (`source.status`, `source.observedAt`, carrying the 45 s feed verdict, `view.py:543-553`); readers show both; "stale file" and "stale data" are separate words (ADJ line 250).
- Provenance: round1-advocate-V3.md X-001; round1-advocate-V2.md Strength 2

### Change 3: clock rule
- Status: applied (insert)
- Target: step 1 (sub-bullet) and "What stays unresolved" (new bullet)
- Before: no clock assumption stated.
- After: rule assumes a shared host clock (`generatedAt` wall-clock UTC, `view.py:555`, as cited by the advocates); a negative or implausible age prints "age unknown", never "current"; CO-04 states a clock-skew allowance alongside its copy delay. Unresolved: skew allowance for a cross-host reader until CO-04.
- Provenance: round1-advocate-V1.md, -V2.md, -V3.md A-001 responses

### Change 4: replace the interim rule in the note
- Status: applied (append)
- Target: step 1 (sub-bullet)
- Before: no mention of ADJ's interim rule.
- After: the note replaces ADJ's interim "older than one producer cycle" rule (ADJ line 792, cited from variant-2), which would flicker on ordinary timing.
- Provenance: round1-advocate-V2.md Concession 1

## Post-Merge Validation

### Structural
- PASS. One H1, five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved); no skipped levels. Numbered steps 1 to 4 intact. Provenance header comments at top and one `<!-- Source: ... -->` comment per section or changed block.
- PASS. No em dashes or en dashes (grep).

### References
- PASS. All code and document citations come from the base, the plan or the advocate/variant files: `collector.py:28`, `collector.py:28-30`, `collector.py:30`, `view.py:32-34`, `view.py:543-553`, `view.py:555`, `commands.py:294-297`, ADJ lines 222, 250, 792.
- One internal pointer to the plan ("(Change 2)") was replaced with a pointer inside the document ("see 'Two ages, never one' under What it unlocks"), so no reference depends on the plan.

### Contradictions
- PASS. Re-scan of "45 s" / "45 seconds": every remaining use refers to term (a), the screen's feed rule or the data-age verdict in `source.status`; none states 45 s as the file threshold. Every file-threshold statement says about 75 s and labels it an inference.
- Note, not a contradiction: step 3 keeps the base wording "adds its copy delay to the producer's interval". The plan did not target step 3, and the sentence is not false under the merged rule, so it was left unchanged; CO-04's design can state how the delay enters the two-term rule.

## Summary
- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
