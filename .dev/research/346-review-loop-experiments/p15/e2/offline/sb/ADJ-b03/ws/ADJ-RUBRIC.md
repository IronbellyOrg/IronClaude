# Adjudication rubric (read fully before you start)

You adjudicate 4 cases on which two independent labelers disagreed, were unsure, or agreed that the quoted evidence needs
correcting. For each case you get the document, the proposed defect, the proposed quotes and BOTH labelers' answers with their
evidence. Decide from the document text yourself; do not simply pick a side.

## Blocking (the grading check, verbatim from the review rules)

For each finding before you mark it blocking, write the sentence "An implementer who follows the stated text as written builds X,
and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each
other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion
cannot pass. Grade it Medium (NOT blocking) when the sentence needs a guess that the implementer picks the worse of two readings
the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an
unspecified edge case) rather than a stated text that does harm. An apparent conflict that the document itself resolves (a
condition that separates the cases, an explicit exception) is not a defect.

## Fields (one JSON object per case, one line per case, in `adjudication.jsonl`)

- `case_id`
- `defect_real`: `yes`, `no`, or `undecidable` (use `undecidable` only when the document text genuinely cannot settle it).
- `final_evidence_quotes`: when `defect_real` is `yes`, the MINIMAL set (2 or 3, rarely 1) of exact quotes from the document whose
  joint reading shows the defect. Start from the proposed quotes; drop one that is not needed; add the missing passage if the
  proposed set is insufficient. Each quote must be an exact, contiguous substring of one line of the document (copy it, do not
  paraphrase), at most 300 characters, and unique enough to locate. Use `[]` when `defect_real` is `no` or `undecidable`.
- `evidence_sufficient` and `evidence_minimal`: about YOUR `final_evidence_quotes` (`yes` when you were able to give a set;
  `n/a` when `defect_real` is `no`; `undecidable` otherwise).
- `other_blocker`: another blocking defect you noticed, or `none`.
- `reason`: one sentence.
- `confidence`: `high` or `low`.

Write all 4 lines to `adjudication.jsonl` in the workspace root (the directory that holds this rubric). Use the Write tool.
