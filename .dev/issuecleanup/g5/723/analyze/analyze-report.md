# Branch ownership architecture analysis

## Scope and grounding
Command: `/sc:analyze .github --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/723/analyze`.

Checkout: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`, HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, inspected on 2026-11-24. `.github` is the narrowest existing source directory covering the proposed ownership file and repository workflows; `.github/CODEOWNERS` itself does not exist in this checkout.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:11:38Z; degraded: none

The graph listed eight YAML files under `.github`; its main workflow outline had zero symbols. Caller, callee and symbol-impact queries are not applicable to this declarative surface. Glob, Grep, Read and tracked-tree inspection supplied the source evidence. No graph initialization, builds, tests, installs, source edits or GitHub writes were run. Live repository settings cannot be inspected through the brief's allowed issue/PR view/list commands and remain UNVERIFIED.

## Findings
1. **Medium, missing local ownership declaration.** No CODEOWNERS file was found by `Glob **/CODEOWNERS`, and tracked-tree checks found none at the root, `.github/CODEOWNERS`, or `docs/CODEOWNERS` in HEAD or the cached `origin/master` reference. This verifies the local part of issue 723's gap, not the current remote branch or server configuration. A CODEOWNERS file alone would not establish a required review gate.
2. **Medium, existing checks are not proof of branch protection.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/boundary-guard.yml:15-20` explicitly makes its warning advisory and assigns actual merge control to repository settings. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/contract3-generator-constraint-lint.yml:22-47` checks a PR-body heading on selected file paths, not owner approval. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:191-200` aggregates test failures, not branch rules. No checked workflow creates the proposed rulesets.
3. **Medium, issue proposal has stale temporary scope.** Live PRs 686 and 690 are CLOSED, unmerged; both have an owner-account comment dated 2026-11-23 explaining that PR 707's watcher is the selected design. Issue 723's two temporary ownership lines were explicitly to be removed when these PRs merged or closed. Before any future approved implementation, reconsider those lines rather than copying the original five-path list unchanged.
4. **Verification boundary.** Issue 723 reports an unprotected branch, no repository rulesets, a public repository and a Free organization plan as of 2026-11-22. None of those server or subscription settings was freshly verified here. Zero-approval owner-review enforcement, the admin bypass behavior, organization-wide inherited rules and the three throwaway tests also remain UNVERIFIED. The issue explicitly parks implementation until the owner's go; no such go is recorded in its current body/comments.

## Metrics and recommendations
Inventory: 10 tracked files under `.github`, including 3 workflow YAML files, 4 issue-template YAML files, funding metadata, a PR template and a workflow README; 0 local CODEOWNERS files found. The three workflows were read end to end; the surrounding templates were inventoried only. No runtime or test-pass metrics are claimed.

Recommendation: keep issue 723 open and parked. On a later explicit owner go, first re-read live branch/ruleset settings and settle the overlap with issue 702, refresh the now-closed-PR temporary ownership scope, then follow the issue's Disabled-first configuration, read-back, owner-controlled activation and three throwaway-test sequence. A shared admin login remains outside the protection that a file ownership list can prove; coordinate that limitation with issue 722. Rollback and throwaway cleanup belong to the future authorized run, not this read-only review.
