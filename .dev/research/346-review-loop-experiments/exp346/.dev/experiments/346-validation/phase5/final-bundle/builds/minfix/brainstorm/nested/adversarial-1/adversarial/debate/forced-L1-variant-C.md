# Variant C — forced surface round

The alternatives deserve credit first: A favors short, reusable names; B makes checker operations easy to scan; C makes ownership and meaning explicit. The preferences below concern labels and presentation only, not schema behavior, budgets or admission policy.

| L1 id (L1-C1..) | issue | preferred | steelman of other | evidence |
|---|---|---|---|---|
| L1-C1 | Helper skill folder naming | B: `sc-fixcheck`; concise and directly matches `fixcheck.py`. | C's `sc-spec-panel-minfix-protocol` visibly associates the helper with its caller; A's `fix-budget` describes the purpose without framework shorthand. Installation behavior needs separate verification and is not decided by this naming preference. | B:242-243 names `sc-fixcheck/scripts/fixcheck.py`; C:151-152 uses the longer caller-specific name; A:145-146 uses `fix-budget`. |
| L1-C2 | Finding-reference field wording | C: `finding_id`, rather than bare `id`, for ledger entries and machine finding records. | A's `id` is shorter and clear inside a finding-only record; B's `finding` reads naturally in its human-authored ledger. | C:75,80 uses `finding_id`; A:58 uses `id`; B:140 uses `finding`. |
| L1-C3 | Budget row labels | C: full severity/eligibility labels in the human-facing table, regardless of internal enum spelling. | A's B/C/L and B's C/M/m make dense tables compact and match their machine classes directly. Full labels consume more width. | C:57-60 spells out the classes; A:76-78 uses B/C/L; B:174-176 uses C/M/m. |
| L1-C4 | Name of the added command reference section | B: `## Fix Budget`; names the feature directly and matches the budget terminology. | C's `## Minimal fix gate` emphasizes that this is an admission boundary, not merely advice about size. That emphasis remains useful in the section's opening sentence. | B:265 names `## Fix Budget`; C:176 names `## Minimal fix gate`. |

S-001 — Steelman: different section orders could privilege operational flow or evidence. Position: retain the shared eight-section sequence; there is no actual three-way ordering disagreement to resolve. Classification: L2 (document structure), not L1; wording of individual headings would be L1. Evidence: diff-analysis:19 explicitly records the same sequence for A, B and C.

S-002 — Steelman: B's finer subdivisions improve navigation through a long reference; A's intermediate depth balances scanning and continuity. Position: prefer C's lighter subdivision, adding a heading only when it separates a distinct lookup task; do not impose an exact heading-count target. Classification: L2 (hierarchy and chunking), not L1; capitalization or numbering style alone would be L1. Evidence: diff-analysis:20 records A 23, B 38 and C 19 headings, all at maximum depth 3.
