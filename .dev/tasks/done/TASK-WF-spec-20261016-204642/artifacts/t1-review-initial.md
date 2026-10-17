# Task 1 independent review — initial

Verdict: missing. AC1/AC2 unmet, AC3/AC4 met. No extra scope.

Independent reviewer reproduced:
- A formal Cosmos review lacking submitted_at/submittedAt was accepted through createdAt fallback after a watermark.
- A contextual legacy review with watermark but no expected head or commit, and an explicit null head_sha, could become clean.
- A validly formatted but future-dated submission (year9999) became clean.
- poll_succeeded accepted missing threads_ok on recognizable Cosmos evidence while classify correctly returned polling.

Evidence at review time: classifier.py lines65–79,188–228,324–359; source.md lines50,56,105,109. Shared selection, identity isolation, root provenance, unresolved historical roots and malformed marker guards were present; no unrequested changes found.

One coordinated fix pass authorized by the execution protocol. Keep the core deterministic: capture observed_at in the poll adapter and compare completion submission time to that input rather than reading the clock inside the classifier. The extra snapshot field is a necessary implementation detail of the source's future-evidence guard, not a new feature or provider abstraction.

Separately, parent reran139 Cosmos/legacy detection regressions successfully before this correction; passing those tests did not substitute for this source-compliance review.
