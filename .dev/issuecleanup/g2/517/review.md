# Independent evidence review

Template: review skeleton in `.dev/issuecleanup/g2/468/report-template.md`.

## Verdict
**PASS.** Independent fresh-context evidence-validator review found no blocking defect in findings.md or analyze/analyze-report.md. It confirmed the source supports keeping #517 open, the effort-400 handling is missing, and an ordinary cooldown switch rule would violate the no-parking requirement. The parent persisted this result because the reviewer has read-only tools.
## Scope checked
The reviewer read both reports in chunks of at most 80 lines, checked every required heading against the adopted template, and independently inspected proxy source and associated test excerpts. It confirmed unchanged effort forwarding (proxy :844-847), unmatched effort 400 (:396-433, :933-962), model-wide cooldown (:123, :471-475, :914-927), image-only no-parking handling (:419-422, :956-987), both tier and named-model entry routes (:698-706), the two Tier 3 slots, documented model order and worker effort workaround.

It checked the real-proxy test fixture and extra-field support at tests/unit/test_ccsession_tiers.py:847-907, existing test bodies at :1048, :1075, :1104, :1117 and :1137, and searched ccsession test filenames for effort coverage. It found no effort-recovery test. It did not read the unrelated-error test's parameter list; the producing session read it directly at :1039-1046. Recommended no-parking list-walk behavior and accurate terminal error reporting fit the existing source.
## Blocking findings
None. Required report sections are present, the core source claims and line citations held, and the recommendation remains a proposal rather than an approved implementation change.
## Follow-up candidates and notes
- Independent reviewer did not verify GitHub state/timeline/merge identities, graph metadata, local HEAD, or live gateway facts; the parent session collected GitHub and git evidence, and live behavior remains explicitly UNVERIFIED.
- The medium complexity and size S assessment is a judgment supported by its explanation, not a measured duration.
- Existing bounded filename-scoped effort searches do not prove that no differently named or unpushed test exists.
- Implementation caution, already in the reports: keep last-error and oversized-backup bookkeeping consistent so effort incompatibility never becomes a false out-of-usage response.
- The read-only out-of-allowlist timeline API call and early read-size deviations are disclosed; disclosure does not retroactively authorize them. No source change or outward mutation occurred.
- No nonblocking defect requiring a follow-up issue was identified; no runtime tests were run by the reviewer.
