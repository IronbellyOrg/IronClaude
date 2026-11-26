# Ruff version architecture analysis

## Scope and method
Command: `/sc:analyze pyproject.toml --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/618/analyze`.

The primary target is the dependency declaration, the narrowest file holding IronClaude's Ruff version policy. The scan follows its direct configuration consumers: the lockfile, pre-commit hook, CI lint job, Makefile and PR validation instructions. This is a static architecture review, not a reproduction run. Checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, reviewed 2026-11-24.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:35:21Z; degraded: graph:empty

The graph inventory was available; its workflow outline contained zero symbols. Dependency versions and shell invocations are configuration, so direct Read/Grep evidence supplies the relevant links rather than invented function callers or impact edges.

## Findings and impact
1. **High, delivery reliability: independent version ownership remains.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/pyproject.toml:50-54` hardcodes Ruff 0.15.20 and tells maintainers to bump it deliberately. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/uv.lock:1584-1585` resolves that version, and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.pre-commit-config.yaml:105-113` independently pins its formatter hook to v0.15.20. These are not references to a Coder-owned version source. This is sufficient to show issue #618's single-source acceptance condition is unmet, independently of whether the original formatting failure reproduces today.
2. **High, delivery reliability: local and CI select tools differently.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.github/workflows/test.yml:96-106` installs the dev extra before running Ruff, whereas `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/Makefile:48-55` invokes Ruff through UV without specifying that extra. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:318-325` requires a separate formatting gate and blocks the push on a nonzero exit. The selection difference is verified statically; present-day fallback behavior and an actual false failure are UNVERIFIED in this run.
3. **Medium, change planning: Markdown coverage needs an explicit decision.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/pyproject.toml:174-182` excludes docs and developer artifacts but contains no general Markdown exclusion. That is not proof that the current formatter selects Markdown. The exact 12-file failure remains historical issue evidence, not a newly observed run; choosing exclusion or one-time formatting remains part of the requested change.

## Metrics and limits
Three configured pin sites remain: the dev dependency, its lockfile resolution, and the pre-commit revision. The lockfile is generated state, not a third independent policy decision. The linked live issue was OPEN with no comments; its mentioned PR #614 is MERGED at commit `c00caea930e5a0d68b5c89716a396d916ac41d97`, with planning/documentation changes rather than a Ruff configuration fix. A read-only PR search for `618 in:title,body` returned no results, which does not prove no work exists elsewhere.

No UV, package installation, tests, formatter or workspace creation was run. Coder's current private repository pin, its update mechanism, the historical run log, exact current Markdown failures, fresh-workspace parity, and present CI results are UNVERIFIED. The only source changes authorized by this review are reports inside the assigned directory; no implementation, GitHub write, staging or commit was performed.

## Recommendations
Keep issue #618 open as still-relevant. Plan one owner for the version, explicitly covering how CI and non-Coder contributors obtain the same formatter without unauthorized access to Coder. Treat merely dropping the dev dependency as incomplete unless CI provisioning and pre-commit behavior are also settled. Include the Markdown choice and release ordering in that plan, then validate both dependency-install paths in an authorized implementation run. Suggested triage: complexity medium, size M, priority P1, because the unresolved delivery gate has a documented workaround but can stop otherwise unrelated submissions.
