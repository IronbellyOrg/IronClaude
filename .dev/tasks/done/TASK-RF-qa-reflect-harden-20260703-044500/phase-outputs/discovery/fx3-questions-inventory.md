# FX3 Field-Resolution Discovery Inventory (Step 2.1)

Source (current tree, HEAD 46a787da):
- `src/superclaude/pr_submit/contract_setup/questions.py`
- `src/superclaude/pr_submit/contract_setup/evidence.py`

## (a) Every `_answer_default(<literal>)` call + its literal

| Line | Call | Literal (answer field) |
|------|------|------------------------|
| 158 | `_answer_default("detected_augment_identity")` | `detected_augment_identity` |
| 165 | `_answer_default("author_association_values")` | `author_association_values` |
| 170 | `_answer_default("emission_shape")` | `emission_shape` |
| 177 | `_answer_default("findings_locus")` | `findings_locus` |
| 184 | `_answer_default("severity_field_path")` | `severity_field_path` |
| 189 | `_answer_default("review_completeness_signal")` | `review_completeness_signal` |
| 196 | `_answer_default("decline_detection_fields")` | `decline_detection_fields` |
| 201 | `_answer_default("expected_classifier_result")` | `expected_classifier_result` |

All 8 literals ∈ SetupAnswers fields. ✓

## (b) Every `_evidence_attr(attr, answer_attr=?)` call → derived answer_key + evidence_attr

`_evidence_attr` factory: `questions.py:64-76`; indirection `answer_key = answer_attr or attr` at L68.

| Line | Call | `evidence_attr` (=attr) | `answer_key` (=answer_attr or attr) |
|------|------|-------------------------|-------------------------------------|
| 131 | `_evidence_attr("repo")` | `repo` | `repo` |
| 136 | `_evidence_attr("pr_number", answer_attr="probe_pr")` | `pr_number` | `probe_pr` |

- answer_key `repo` ∈ SetupAnswers ✓; evidence_attr `repo` ∈ EvidenceBundle ✓
- answer_key `probe_pr` ∈ SetupAnswers ✓; evidence_attr `pr_number` ∈ EvidenceBundle ✓

**THE F3 TRAP:** The buggy original `_evidence_attr("pr_number")` (missing `answer_attr="probe_pr"`)
would derive `answer_key = "pr_number"`, which is NOT a SetupAnswers field (the answer field is
`probe_pr`) → the deriver's `getattr(answers, "pr_number", None)` silently returns `None`, dropping the
operator's answer. FX3 assertion (2) (`answer_key ∈ SetupAnswers fields`) catches exactly this.

## (c) Full `SetupAnswers` field name set (17 fields, questions.py:14-38)

```
repo, probe_pr, operation, evidence_source, surfaces_to_inspect,
detected_augment_identity, augment_app_slug, author_association_values,
emission_shape, findings_locus, severity_field_path, review_completeness_signal,
decline_detection_fields, expected_classifier_result, run_validation,
write_local_locked_contract, next_step
```

## (d) Full `EvidenceBundle` attr name set (13 dataclass fields, evidence.py:18-37)

```
probe_dir, repo, pr_number, captured_at, surfaces, omitted_surfaces,
reviews, comments, check_runs, combined_payload, sha256, pagination_complete,
cross_pr_shape_only
```

## SUBSET-direction note

`augment_app_slug` is a REAL SetupAnswers field (questions.py:28) intentionally referenced by NO
deriver (it is set alongside `detected_augment_identity`). Therefore the FX3 check MUST be SUBSET
(`referenced ⊆ valid`), NEVER onto/exhaustive — an onto check would false-positive on `augment_app_slug`.

Likewise many EvidenceBundle attrs (probe_dir, surfaces, reviews, etc.) are never named by an
`_evidence_attr` call; the evidence-side check is also SUBSET.

All entries extracted directly from current source with exact line numbers. Nothing fabricated.
