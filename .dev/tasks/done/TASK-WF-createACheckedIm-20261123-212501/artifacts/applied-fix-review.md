# Independent Applied-Fix Review

## AC marks

Reviewer: swarm-applied-fix-qa, independent read-only review, 2026-11-24. Paths below are repo-relative or package-relative under ./artifacts/.

1. Diff scope: applied-product.diff:1-33 changes only two blocks in commands.py: the validate-lenses docstring and scaffold lens-option help. applied-product.diff:34-87 changes only the Path import and three regressions in test_cli_registration.py. Live source matches at commands.py:435-440,3780-3790 and test_cli_registration.py:17,106-137. Reviewer cannot run git; parent independently ran git diff --name-only HEAD -- src tests docs and observed only these two files. Internal comments/adjacent diagnostics are unchanged as required.
2. Validate-lenses help: commands.py:436-440 and public-after.txt:11-17 omit the false option and name JobSpec custom_prompt_dir with lens: custom, preflight validation and inline custom prompts. Live preflight.py:1569-1596 applies the directory only for custom plus a nonempty field. schema.py:685-723 enforces the binding without requiring a directory for every custom spec; inline support is explicit at schema.py:700-704.
3. Scaffold help: commands.py:3784-3789 and public-after.txt:63-70 omit the false option, preserve no-registry-defaults rejection, and describe optional directory-backed or inline prompts.
4. Parser: public-after.txt:78-84 retains the same command/directory, unknown-option diagnostic and exit 2 as public-before.txt:73-79. Directory remains empty. test_cli_registration.py:129-137 pins this. No option or registration was added.
5. Tests: test_cli_registration.py:106-137 invokes root main, strips whitespace and checks absence plus positive field/lens binding; scaffold requires inline guidance. Reviewer did not read the red logs, only confirmed their presence; reproducing-history verification remains the per-task and FINAL reviewers' responsibility.
6. Preserved contracts: commands.py:3826-3844 custom/unknown rejection code is untouched, with corresponding tests passed at related-tests-green.txt:72-73. Validation warning/custom-only tests pass at :34-45. Directory/preflight/guard tests pass at :75-103. Guard/metadata paths are absent from the product diff.
7. Test evidence: related-tests-green.txt:5-11 records coverage plugin unavailable and command exit 4. Same five files run without coverage at :14, with 80 passed, 1 skipped, exit 0 at :105-107. Existing NOTSET placeholder skip at :31. Coverage was not measured.
8. Historical rows: diagnostic-disposition.md:9-21 records new local evidence only, preserving historical pending rows and making no environment explanation. Its still-required applied-review sentence describes the earlier checkpoint, not this completed review.

## Findings and result

No defect found. All four checklist answers are no: ac-outcome-missing, false-claim, harmful-effect, quoted-constraint-breach. No anchors required and no confirmed blocker. Parent-derived result: compliant for the bounded applied fix, not a successful model-backed custom job or a coverage measurement.

All-no form Note: diagnostic-disposition.md:21 still says independent applied-fix review is required. This was true when Task 2 wrote the checkpoint. This separate persisted review and the later Task 4 ledger record provide the new evidence; the earlier checkpoint is retained unchanged. The reviewer requested no code change. This note does not block completion.

## Source revision for historical citations (2026-11-24)

Source line numbers above describe the pre-rebase reviewed state, recorded in local commit `f8ba6a491a63717f4ac66bff8d1f6d3c3f9d64ad`, not the rebased PR head. See [source-revision-map.json](./source-revision-map.json) for a published-base-plus-patch reconstruction, exact source hashes, and ranges pinned to PR revision `1b16d73832dfdb228ee7f6e4075ea4b14ee46235`. In particular, historical `commands.py:3784-3789` maps to `commands.py:4137-4142` there. This annotation preserves the original review and does not claim a new review or test run.
