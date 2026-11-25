# Effective Input Card

## Selector and source state

selector_command: not applicable; the independent evidence reviewer receives explicit report/card/captured-artifact paths and source coordinates, not a Git diff or indirect review selector.
selector_cwd: current worktree root.
base_ref/head_ref: not a review range; source revision recorded in artifacts/source-revision.txt.
dirty_files/staged_files/unstaged_files: not used as review input. Existing task packages and externally changed shared counter are not claimed as this diagnosis's product changes; git diff --stat -- src tests docs returned empty.
excluded_foreign_commits: [] (no history selector).

## Reviewed surface

included_files: REPORT.md.draft when materialized; current hypothesis/calibration; execution-locus.md; producers.md; diagnosability-tasklist.md; this card and other hardening cards; explicit raw foreground/resume capture files and referenced live source ranges.
runtime_surface_claim: this worktree's run_cmd and _run_resume_branch completion omission, bound to imported source paths and captured job outputs, not a repository-wide diff review.
intersection_proof: review selection is explicit file paths, with import-paths.txt binding execution to current source. Reviewer must Read the listed artifacts/source citations; no positive inclusion claim is made until that review returns.
validation_command/validation_result: source import check printed both modules under this worktree; no indirect-selector validation command applies.

## Verdict

HC4: N/A with rationale: no independent review gate consumes an indirect selector. Explicit evidence review remains required; this N/A does not waive HC1's missing repaired-run proof or authorize unrelated staged work.
