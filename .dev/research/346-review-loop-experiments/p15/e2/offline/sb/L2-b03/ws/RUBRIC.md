# Labeling rubric (read fully before you start)

You will label 8 proposed defects. For each case you get a document, one proposed defect (a sentence) and the quoted passages
that the proposer believes show it. Judge only from the document text. Do not edit the document. Do not search the document for
other problems; answer `other_blocker` only if you happened to notice one while checking the claim.

## Blocking (the grading check, verbatim from the review rules)

For each finding before you mark it blocking, write the sentence "An implementer who follows the stated text as written builds X,
and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each
other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion
cannot pass. Grade it Medium (NOT blocking) when the sentence needs a guess that the implementer picks the worse of two readings
the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an
unspecified edge case) rather than a stated text that does harm. An apparent conflict that the document itself resolves (a
condition that separates the cases, an explicit exception) is not a defect.

## Fields (one JSON object per case, one line per case, in `labels.jsonl`)

- `case_id`: copied from the case.
- `defect_real`: `yes` if the proposed defect is real AND blocking per the grading check; `no` otherwise.
- `evidence_sufficient`: `yes` if the quoted passages alone, read in the document, show the defect without reading anything else;
  `no` if another passage is needed; `n/a` when `defect_real` is `no`.
- `evidence_minimal`: `yes` if no quoted passage can be dropped without losing the defect; `no` if one can; `n/a` when
  `defect_real` is `no`.
- `other_blocker`: another blocking defect you noticed (a short quote plus one sentence), or `none`.
- `evidence`: one quote from the document (at most 300 characters) that supports your `defect_real` answer.
- `confidence`: `high` or `low`. Use `low` whenever you had to guess.

Example line (format only, not a real case):
{"case_id": "x-00", "defect_real": "no", "evidence_sufficient": "n/a", "evidence_minimal": "n/a", "other_blocker": "none", "evidence": "...", "confidence": "high"}

Write all 8 lines to `labels.jsonl` in the workspace root (the directory that holds this rubric). Use the Write tool.
