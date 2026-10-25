# Independent research verification contract

Reviewers start adversarially. Do not confirm the producer's claims on trust. All intentional writes must remain under .dev/research/upstream-merge-impact/. No source/index/history/ref changes, no fetch, no real revert, no test/build/install commands that write outside the research directory. No nested agents or memory changes.

Read the registered codebase-research template, create a stub immediately, and populate Findings/Gaps/Key Takeaways incrementally at your assigned review output. Return only its path. Give a binary PASS or FAIL; any identified issue of any severity means FAIL until corrected and independently rechecked. For zero findings include Self-Audit naming actual checks.

## Verify assigned reports against primary sources

- Read each assigned report fully from disk. Verify its current completion status, placeholders, every assigned short hash, per-commit decision, applicability result, loss/rewrite cost, and gaps.
- Check unit membership and complete path counts against units.json AND endpoint-inventory.json. The foundation unit has 269 old/new endpoints, not its default name-only manifest's 268. Overall union is 563 unique paths.
- Check historical claims against actual first-parent Git diffs and commit metadata. Source-authored timestamps differ from committer dates; do not confuse incoming source commits with fork merge commits or double count their effects.
- Read every decision-changing file:line citation directly, and verify citations resolve. Save exact source evidence under a uniquely named supporting path if useful. If a source file moved/deleted, require explicitly historical sha:path:line evidence or saved raw historical source. A later commit touching a file is not enough to prove a dependency.
- Verify code/tests/docs/skills/CLI consumer claims with actual reference searches and entry-point traces. Separate static code dependence, test-only use, install/distribution dependence, documented behavior, and unused content. Check dynamic glob/discovery and package/plugin consumers before accepting 'unused'.
- Verify per-commit strict reverse outcomes against reverse-checks.json. Strict reverse patch success is NOT a tested Git revert, and strict failure does NOT prove the three-way revert would conflict. Actual revert/runtime outcomes must be labeled UNVERIFIED. 67449770 has an empty patch, not a code regression or failed reversal.
- Estimates are judgments with assumptions, not measured execution times. No invented breakage or unsupported quantitative claims. Report must not claim tests were run.
- Verdicts must distinguish keeping required behavior from retaining every obsolete historical file. Any recommended partial removal must name exact boundaries and prerequisites, and account for the fork's later work and other units.
- If source claims cannot be confirmed, mark the precise gap UNVERIFIED and verify that the recommendation does not rely on it.
- Review completeness mechanically from artifacts; a producer's completion message alone is not sufficient.

## Findings format

Within Findings, record PASS/FAIL, each concrete defect with report path:line and primary evidence, severity, and required correction. Do NOT edit unit reports yourself. Keep review records on disk even after correction. Parent will route corrections to the original producer and ask you to recheck the revised artifact.
