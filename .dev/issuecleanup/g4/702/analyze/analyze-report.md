# Architecture analysis

## Scope and method

Command: `/sc:analyze .github --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/702/analyze`.

Read-only static review at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on 2026-11-24. The proposed `.github/rulesets/` directory does not exist, so `.github` is the narrowest existing source directory containing the issue's configuration area. Inspected its three workflow files, the release procedure, contributor guidance, documentation indexes and existing local push hook as boundary evidence. No source, settings, Git index or remote changed.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:54:11Z; degraded: none

Graph discovery returned eight YAML files under `.github`; the main workflow has zero indexed symbols. Callers, callees and symbol impact are not applicable to these declarative files; native file discovery, content searches and direct reads supply the evidence instead. No graph result was treated as proof of absent server settings.

## Severity-rated findings

1. **Medium: the repository-side deliverables for #702 are absent.** Glob `.github/**/*` contains the three workflows, issue forms, funding file and pull-request template, but none of `.github/rulesets/protect-master.json`, `protect-integration.json` or `protect-release-tags.json`. Glob `tests/docs/*` returns four unrelated tests, not the requested ruleset test. Glob `docs/developer-guide/*protection*` returns no branch-protection guide. Neither documentation index links the proposed guide. This is missing configuration-as-code and operational evidence, not proof that live GitHub settings are absent.
2. **Medium: existing automation and local hooks are not equivalent to server-side branch rules.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/boundary-guard.yml:19-20` explicitly says the check is advisory; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/contract3-generator-constraint-lint.yml:22-29` selects only pull requests touching validator files. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:3-8` runs tests on pushes and pull requests, not a pre-push server control. The local push hook protects only main/master (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-pre-push.sh:17`), and explicitly allows ordinary actors at line 188. It does not implement #702's all-actor master/integration/tag policy.
3. **Medium: two open proposals require an owner decision before implementation.** Live issue #723 is explicitly parked pending the owner's go. It proposes code-owner review and an admin pull-request bypass on master, and only deletion/force-push restrictions on integration initially. #702 instead proposes no bypass actors, no code-owner requirement and pull-request-only integration, plus release-tag rules. They overlap but are not interchangeable duplicates; neither issue can be declared completed from the other.
4. **Note: existing generic standards are not this fork's applied policy.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/developer-guide/git-standards-protocols.md:379-386` describes main/release branches and required approvers. It neither supplies the three JSON files nor demonstrates enforcement on master/integration. Do not count that prose as completion.

## Metrics and boundaries

Three workflow YAML files inspected; zero requested ruleset JSON files, zero requested branch-protection guide files and zero requested ruleset tests found in their specified locations. Content search of all workflow files found no `git push`, `git tag`, `gh release` or `gh pr` invocation. This is bounded source evidence, not an audit of external GitHub Apps, deploy keys or webhooks.

The release procedure already opens a pull request before tagging (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/developer-guide/release-procedure.md:37-59`) and pushes a new tag (`:86-94`). That flow is consistent with the intended branch restrictions and permitted new-tag creation, but compatibility against applied rules is UNVERIFIED. Tests/builds, live ruleset reads and trial pushes were not run because the brief permits only issue/PR reads on GitHub and forbids environment creation. Current enforcement, admin permissions, plan entitlement and the proposed API parameters remain UNVERIFIED.

## Recommendations

Keep #702 open as still-relevant. First have the coordinator obtain the owner's decision reconciling #702 with the parked #723, without treating either issue's proposed policy as approval. After that decision, implement only the selected JSON, documentation and small static test scope. Keep application, trial-repository checks, remote enforcement proof and any follow-up issue creation as separately authorized actions. Never use an attempted push to a protected production branch as part of this read-only review.
