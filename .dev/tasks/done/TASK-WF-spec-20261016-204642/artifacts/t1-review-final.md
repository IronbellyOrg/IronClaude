# Task 1 independent re-QA

Verdict: compliant. One fix pass completed; no remaining reproduced source requirement gap or extra scope.

- T1.AC1 met: lifecycle regressions cover current-head, historical resolved/unresolved findings, author isolation and contextual legacy freshness.
- T1.AC2 met: formal submission time only, full expected-head/commit agreement, valid bounded Cosmos metadata, latest-evidence barrier, strict watermark and observation-time future guard.
- T1.AC3 met: explicit false and missing Cosmos completeness flags block completion; positive count with insufficient details returns polling and empty selection; poll_succeeded likewise rejects missing Cosmos flags.
- T1.AC4 met: classify and actionable_finding_comments share selection; stable root/thread/review IDs and nullable/original hints survive; historical open roots are not watermark-filtered. Poll seam and package exports match the interface.

The same independent reviewer reran all four original memory-only reproductions against the corrected worktree module; all now fail closed while fully attributed and context-free legacy controls retain intended behavior. The T1117 test change only supplies realistic submission/head/commit fields, without changing its expected outcomes.

Writer reported550 complete PR-submit tests and106 Cosmos classifier cases passing plus changed-file Ruff checks. Parent independently verified139 earlier detection cases and97 frozen adapter/static cases; final integrated checks will be rerun after remaining tasks. Tests supplement, not replace, the per-AC source review.
