# Leftovers for the user (Task 9)

Line numbers: "now" is the edited scripts/README.md after this task; "was" is the same line on base a88f100b (the numbering the plan uses). The edit replaced old lines 7-12 (6 lines) with 3 lines, so every later line moved up by 3.

## 1. scripts/README.md lines that still assume a publish workflow

| Now | Was | Text / section |
|---|---|---|
| 3 | 3 | "Package publishing is not done by a local script; it is handled by the GitHub Actions workflow described below." |
| 5 | 5 | Heading `## Publishing (GitHub Actions)` |
| 11 | 14 | "The workflow publishes under the PyPI project name `SuperClaude`; whether a given fork can publish to that name depends on the PyPI project's ownership." |
| 13-18 | 16-21 | Section `### Required Secrets` (`PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`) |
| 20-25 | 23-28 | Section `### Release steps` (workflow run with `target=testpypi`, "Publish a GitHub release; the workflow builds and uploads to PyPI") |
| 31 | 34 | "Before publishing, ensure version consistency across:" |
| 36 | 39 | "The workflow's "Verify package structure" step prints both versions." |
| 46-50 | 49-53 | Section `### Upload Failures` (repository secrets, version already exists on PyPI, package name available) |
| 61-63 | 64-66 | Security Notes: "Store publishing tokens only as GitHub Actions secrets", "Tokens should have minimal required permissions", "Consider using Trusted Publishing for GitHub Actions" |
| 27 | 30 | Not in the plan's list, found while reading: "...have no workflow equivalent; to build locally without uploading, run `uv build`." (refers to the removed workflow) |

Line 3 and the line 5 heading now contradict the new paragraph at lines 7-9: the paragraph says the workflow was removed and the fork is not published to PyPI, while line 3 still says publishing "is handled by the GitHub Actions workflow described below" and line 5 is still titled "Publishing (GitHub Actions)". The same holds for the sections listed above. This task changed only the one paragraph, as scoped. I can extend the edit to the whole file (rewrite or delete the publishing sections) if you agree; say so and it becomes a separate step.

## 2. .dev/specs/pr-submit-ci-monitor.md mentions of the removed quick-check.yml

Accepted leftover, not edited (historical spec):

- line 18: `  - .github/workflows/quick-check.yml`
- line 28: "already runs the same commands as `quick-check.yml` (pytest, `make lint`"

## 3. For you to confirm: path-filter file limit in contract3-generator-constraint-lint.yml

The header comment of .github/workflows/contract3-generator-constraint-lint.yml (lines 14-15) says a path-filtered workflow is skipped "when the PR diff has more than 3,000 files and the matching file is not among the first 3,000." The Augment review bot said GitHub evaluates path filters against only the first 300 changed files.

Current GitHub documentation sentence (quoted in ./artifacts/t3-github-prereqs.md, section 3), source https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax:

> If the generated diff contains more than 3,000 files and the files the workflow filter matches are not in the first 3,000 returned by the filter, the workflow will not run.

The planning session also found that only older GitHub Enterprise Server docs say 300. So the comment is correct for this repository (github.com); no change was made. Please confirm you agree.
