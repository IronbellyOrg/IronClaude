## Verdict
**still-relevant.** Keep issue #618 (make IronClaude's Ruff formatter version follow Coder) open: https://github.com/IronbellyOrg/IronClaude/issues/618.

At checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, reviewed 2026-11-24, IronClaude still explicitly owns its Ruff version: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/pyproject.toml:50-54` pins `ruff==0.15.20`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/uv.lock:1583-1585` resolves it; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.pre-commit-config.yaml:105-113` pins v0.15.20 and requires it to match the project dependency. CI installs the dev extra, then runs Ruff at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:96-106`. Thus the issue's central acceptance condition, replacing IronClaude-owned version selection with one Coder-owned source, is demonstrably not implemented in this checkout.

The live issue is OPEN and has no comments. Its mentioned PR #614 is MERGED, merge commit `c00caea930e5a0d68b5c89716a396d916ac41d97`; its changed files are planning and documentation material, not these Ruff configuration sites. The issue's statement that its original submission run halted is historical context, not evidence that PR #614 remains blocked now. A read-only search of PR titles and bodies for `618` returned no results; this is not proof that no unpublished or indirectly named work exists.

Ran the required analysis on `pyproject.toml`, the narrowest version-policy source, and followed the direct configuration consumers. Analysis: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/618/analyze/analyze-report.md`; command contract: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/618/analyze/return-contract.yaml`.

UNVERIFIED: the present Coder image version and its private repository configuration; the original local monitor log and exact 12-file Markdown failure; fresh-workspace fallback behavior; current CI/workspace formatting parity; any unpushed work. This review did not run UV, install dependencies, run tests or execute the formatter, and did not change project configuration or GitHub records.

## Complexity and size
**complexity medium; size M.** A bounded tooling change spans dependency resolution, an isolated pre-commit environment, CI provisioning, contributor instructions and a Markdown-formatting choice, with cross-repository update ordering to design; deleting one pin alone cannot meet the acceptance conditions.

## Priority
**P1.** The issue records an otherwise unrelated submission stopped by the mandatory formatting check, and the independent version-selection policy remains; installing the dev extra is the issue's stated workaround, so this is delivery reliability work rather than a production outage. The current false failure is UNVERIFIED and PR #614 itself has since merged.

## Concrete next steps
No partial Ruff fix was established in this checkout. These are the remaining issue acceptance steps, not work authorized during this read-only review:

1. Plan one version authority: either use the workspace's Ruff with an explicit CI/contributor provisioning contract, or derive the version from Coder through an agreed transfer mechanism. Verify Coder's actual current source before choosing a value. Do not assume IronClaude's CI can fetch a private repository, and do not add credentials merely to silence this review's verification gap.
2. Bring the three existing pin sites and their comments under that policy, including pre-commit's own installed environment. Set out how non-Coder contributors get the same version, and the order in which the two repositories change when the Coder version changes.
3. Decide explicitly whether to reformat the issue's 12 named Markdown files once or exclude Markdown. Reproduce the affected file list with the chosen version first; the historical list is not a verified current formatter result.
4. Update the affected CI job, Makefile/documented checks and submission gate instructions only as required by that choice. In an authorized implementation run, validate both a workspace without the dev extra and CI with dependencies installed, then run the issue's regression checks and a submission-formatting gate on an unrelated change. No such validation was performed here.

## Dependencies
No numbered prerequisite or issue blocked by #618 is established by its body or comments. Cross-repository coordination with Coder is an implementation requirement, but an issue number and a currently agreed version-transfer mechanism are UNVERIFIED. PR #614 was the reported trigger, not an outstanding dependency or a still-blocked PR.

## Related issues
No other IronClaude issue is directly linked by #618. A read-only search of all issue states for `ruff` returned other lint, validation and general follow-up records, but did not establish a duplicate or a prerequisite for this version-authority request. Those incidental text matches are not promoted into dependencies. The Coder issue #364 mentioned in the body is historical provenance for the reported image pin; its contents and current relevance are UNVERIFIED because this assignment permits GitHub reads only on IronbellyOrg/IronClaude.

## Related PRs
- **PR #614, planning material for the review-panel default and surgical remediation**, https://github.com/IronbellyOrg/IronClaude/pull/614: the only PR explicitly mentioned in #618; MERGED 2026-11-17 at `c00caea930e5a0d68b5c89716a396d916ac41d97`. Read its body, comments, metadata and changed-file list. It supplies incident context, not a Ruff fix.
- **No implementing PR verified.** The read-only all-state search `618 in:title,body` returned no results. A broader `ruff` PR search returned matches, but those results alone do not establish implementation of #618; the checked-out configuration is the decisive evidence that this checkout still owns its own version.
