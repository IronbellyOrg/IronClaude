# Recurrence Corpus

This directory holds disk-backed test fixtures that encode **documented recurring failure modes** from the roadmap-pipeline retrospective (master:§Recurrence Matrix rows #1-22). Each fixture proves the Contract #1 invariant: **MUST FAIL pre-fix, MUST PASS post-fix.**

## Layout

```text
tests/roadmap/fixtures/recurrence/
├── README.md                          # this file
├── anti_instinct/                     # Contract #10  (master:§Recurrence #6)
├── spec_fidelity/                     # Contract #4   (master:§Recurrence #1)
├── frontmatter_parser/                # Contract #6   (master:§Recurrence #8)
├── retry_contract/                    # Contract #7
├── threshold_registry/                # Contract #8   (master:§Recurrence #7)
└── id_containment/                    # Contract #9   (master:§Recurrence #4)
```

## Naming convention

```text
<failure_class>/<case_name>.md            # the input under test
<failure_class>/<case_name>.expected.json # the expected outcome (assertions)
```

Each case is paired: a markdown input fixture + a JSON file describing the
expected pipeline / gate output. Tests load both via the
`recurrence_corpus_dir` and `recurrence_case` fixtures registered in
`tests/roadmap/conftest.py`.

## Loader pattern (parametrized via indirect fixture)

```python
@pytest.mark.parametrize(
    "recurrence_case",
    [
        ("id_containment", "spec_roadmap_drift_case"),
    ],
    indirect=True,
)
def test_phantom_id_rejected(recurrence_case):
    input_path, expected = recurrence_case
    # ... assertions against `expected`
```

## Adding a new case

1. Identify the documented incident in `master-report.md` (cite the row #
   and the partition reference, e.g. `A12:F-A12-01`).
2. Add `<failure_class>/<new_case_name>.md` with a minimal reproducer
   (<200 lines preferred).
3. Add `<failure_class>/<new_case_name>.expected.json` with the expected
   gate / scanner output (post-fix behavior).
4. Add a test (in the appropriate `test_*_recurrence.py` file) that
   parametrizes the case.
5. Verify Contract #1: the test FAILS against the parent commit and PASSES
   against the fix commit.

**No fabricated cases.** Each fixture must trace to a real documented
incident in `master-report.md`, `wave3-vector-analyses/`, or
`partition reports A1-A14`.
