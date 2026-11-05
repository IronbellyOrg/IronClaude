# IronClaude Release Readiness

- Generated: 2026-10-31 (Orca task task_0b3bc8e78ff0, dispatch ctx_a299db243b36)
- Worktree: `.dev/worktrees/release-readiness`, branch `research/release-readiness-20261031`, base `origin/master` 75d0d1e2
- Method: `/sc:analyze --focus architecture --depth deep` plus read-only git, gh and orca commands. Every claim cites a file:line, SHA, PR/issue number or command.

## 1. Summary

- **Baseline.** The package says `4.3.5` since 2026-06-04 (`5d660ca9`), but 4.3.5 was never tagged or released: the only tag is `v3.9` (a 4.2.0 commit), there are no GitHub Releases, and `CHANGELOG.md` has only an `Unreleased` section (25 entries, one marked Breaking). 381 commits and 169 merged PRs have landed since.
- **Delivery today.** Users install from `master` (`pipx install git+...`, `./update.sh`); Coder pins a SHA (`2cb683f`). No workflow, script or Makefile target cuts a release; `changelog_maintenance.md` describes a manual tag-and-release procedure with three defects (git-ignored notes folder, `gh` without `--repo`, undefined "release gate").
- **In-flight work.** One open PR (#303, conflicting, deferred). Two live Orca workers: the `/sc:pr-submit` Codex refactor (plan only, 0 of 15 tasks run, deferred) and the QA-loop investigation (research, gates the release). The codegraph Phase 3 post-merge check is pending and gates the release; the codegraph release monitor plan is merged but unexecuted (deferred). Cleanup candidates: 17 unmerged branches (4 need triage: B1, B2, B6, B9), 11 branches already squash-merged, and 27 finished or superseded plan packages still in `.dev/tasks/to-do/`.
- **Proposal.** Release **`v5.0.0`**, cut when (1) the Phase 3 post-merge check passes after `./update.sh`, (2) the QA-loop `FINDINGS.md` names no shipped-protocol defect (or its fix merged), and (3) the release PR (version files + changelog cut + notes) merges green. Tag that merge commit; then `/sc:post-release v5.0.0` and point the Coder pin at the tag. Suggested window 2026-11-02 to 2026-11-06, conditional on those events.
- **New defect found.** PR #336's post-merge instruction ("after `superclaude install`") would not refresh the installed skills: plain install skips existing skills, commands, agents and core files (`src/superclaude/cli/install_skills.py:102-103`, `install_core.py:66-68`). Use `./update.sh` or `superclaude update`.

## 2. Current release baseline

| Fact | Value | Evidence |
|---|---|---|
| Declared package version | `4.3.5` | `pyproject.toml:7`, `src/superclaude/__init__.py:8` |
| When 4.3.5 was set | 2026-06-04, commit `5d660ca9` "feat(sprint): v4.3.5 auto-resume default ... (#124)" | `git log -S'version = "4.3.5"' -- pyproject.toml` |
| Git tags (local and `origin`) | Only `v3.9` (tag object `f15ff7f5`, commit `efaa33db`, 2026-05-18). At that commit `pyproject.toml` says `version = "4.2.0"`, so the tag name does not match the package version. | `git ls-remote --tags origin`; `git show v3.9:pyproject.toml` |
| GitHub Releases on the fork | None | `gh release list --repo IronbellyOrg/IronClaude` printed nothing |
| Upstream parent latest release | `v4.3.0`, 2026-03-22 (for collision context only) | `gh release list --repo SuperClaude-Org/SuperClaude_Framework` |
| `CHANGELOG.md` | Has only `## [Unreleased]` (line 5); no versioned section has ever been cut. 25 `###` entries, 386 lines. One entry is labelled **Breaking** (line 49). | `grep -n '^## ' CHANGELOG.md` |
| Change volume since 4.3.5 was set | 381 commits on `origin/master` since `5d660ca9`; 169 PRs merged after 2026-06-04; 474 commits since `v3.9` | `git rev-list --count 5d660ca9..origin/master`; `gh pr list --state all` |
| `origin/master` head | `75d0d1e2` (2026-10-31 18:09Z, PR #336); CI "Tests" workflow success on it and on the four commits before it | `gh run list --branch master --limit 5` |
| Local `master` checkout | `55d40308`, 12 commits behind `origin/master`, no local commits, clean | `git -C /home/coder/workspaces/IronClaude status --short --branch` |
| Open PRs | 1: #303 (onboarding deck), CONFLICTING/DIRTY | `gh pr list --state open`; GraphQL `mergeable` |
| Issue #323 (codegraph) | CLOSED 2026-10-31T00:09:27Z; Phases 1-3 merged as #329, #334, #335, #336 | `gh issue view 323`; `git log origin/master` |
| Coder workspace pin | Coder PR #423 (merged 2026-10-31T00:41Z) pins IronClaude at `2cb683f`, which is before #334, #335 and #336 | `gh pr list --repo IronbellyOrg/Coder --search codegraph` |

## 3. How an official release is cut

### 3.1 What actually delivers code to users today

- There is no publish step. `scripts/README.md:3` says "This fork is not published to PyPI, so there is no publishing script or workflow"; `scripts/README.md:7` records that `.github/workflows/publish-pypi.yml` was removed in PR 280; `scripts/README.md:11` says `scripts/publish.sh` is retired and `uv build` is the local-only build.
- Users install from the git default branch: `pipx install git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install` (CLAUDE.md, "Installation"; `scripts/README.md:9`). `update.sh:7-8` runs `pipx install --force ./` then `superclaude install --force`.
- Coder workspaces consume IronClaude by a pinned SHA that is bumped in the Coder repo (Coder PR #423 bumped it to `2cb683f`). The codegraph plan records "the monitor bumps Coder's pin on every `master` commit" and "Merge is always human; the merge also triggers a Coder pin bump" (`.dev/codegraph-migration/FINAL-SUMMARY.md:309`, `:311`). How that bump is triggered is UNVERIFIED from this repository (it lives in `IronbellyOrg/Coder`).
- Consequence: every merge to `master` is already a de facto release for anyone who installs or updates. A tagged "official release" today is a label plus release notes, not a delivery mechanism.

### 3.2 CI that exists

`.github/workflows/` holds only `test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` and `README.md` (`ls .github/workflows/`). `test.yml` runs on push/PR to `master` or `integration` and on manual dispatch (`.github/workflows/README.md`, "Triggers"), with jobs test, swarm-marker-matrix, lint (ruff, `make verify-deps`, `make sync-dev` + `make verify-sync`, `make lint-architecture`), doctor-check (`superclaude install` + `superclaude doctor`) and test-summary. No workflow runs on tags or creates releases. The `Makefile` has no release, tag or version target (`grep -n -i 'release\|tag\|version' Makefile` finds only the `make verify` version printout at lines 35-36 and an unrelated path at line 95).

### 3.3 The documented release procedure (the only one found)

`src/superclaude/rules/core/changelog_maintenance.md` is the only IronClaude document that describes cutting a release. A human runs every step; nothing automates it.

1. Decide whether a detailed release-notes file is required: always for a new major or minor version, breaking changes, architectural changes or 10+ files changed (`changelog_maintenance.md:89-96`).
2. Create it from `.claude/templates/workflow/changelog_template.md` as `YYYY-MM-DD_vX.Y.Z_SHORT_DESCRIPTION.md` in `.claude/changelogs/` (`:103-108`). The template source exists at `src/superclaude/templates/workflow/changelog_template.md`.
3. Move the `Unreleased` items into a new `[X.Y.Z] - YYYY-MM-DD` section, link the detailed file, update comparison links (`:110-117`).
4. Keep the version consistent in `pyproject.toml` and `src/superclaude/__init__.py` (`scripts/README.md`, "Version Management").
5. `git tag -a vX.Y.Z -m "Release vX.Y.Z - Brief Description"` and `git push origin vX.Y.Z` (`:125-128`).
6. `gh release create vX.Y.Z --title ... --notes-file .claude/changelogs/...` (`:134-136`). Per CLAUDE.md, any `gh` call must carry `--repo IronbellyOrg/IronClaude`; the documented command does not, so it would target the upstream parent by default.
7. Start a new `## [Unreleased]` section (`:141-149`).
8. After the tag exists: `/sc:post-release vX.Y.Z` syncs user docs, technical docs, install scripts (validated by real end-to-end runs) and human test guides (`src/superclaude/commands/post-release.md:3,15,35`).

### 3.4 Gaps in the procedure

| Gap | Evidence |
|---|---|
| The "release gate" that `/sc:post-release` says tags the version is not defined anywhere. | `src/superclaude/commands/post-release.md:3,15`, `src/superclaude/skills/sc-post-release-protocol/SKILL.md:41` name it; `grep -rni 'release gate' src/ docs/` also hits `docs/user-guide/commands.md:333` (which repeats the phrase) and roadmap-pipeline code (`src/superclaude/cli/pipeline/guard_resolution.py`, `guard_pass.py`, `fmea_promotion.py`, `trailing_gate.py:633` "Release gates are ALWAYS blocking"). Those are gates inside the roadmap pipeline, not a step that tags a package version. No version-tagging gate was found in code, CI or docs (UNVERIFIED that none exists elsewhere). |
| Detailed release notes would be written into a git-ignored folder. | `changelog_maintenance.md:107` says save to `.claude/changelogs/`; `.gitignore:123` (`.claude/*`) ignores it (`git check-ignore -v .claude/changelogs/x.md`). CLAUDE.md forbids staging anything under `.claude/` except `settings.json`. |
| `gh release create` example lacks `--repo IronbellyOrg/IronClaude`. | `changelog_maintenance.md:134`; CLAUDE.md "PR Target = Fork" rule. |
| The developer-guide release section is for a different project and unfinished. | `docs/developer-guide/git-standards-protocols.md:54` describes "the GFxAI project"; `:67` "Section 6: Release and Tagging documented - **To Do**". |
| Tag naming is inconsistent with the package version. | `v3.9` tags a commit whose version is 4.2.0 (section 2). |
| Plain `superclaude install` does not refresh existing installed files. | Core, commands, agents and skills are skipped when they exist and `--force` is absent: `src/superclaude/cli/install_core.py:66-68`, `install_commands.py:55-56`, `install_agents.py:51-52`, `install_skills.py:102-103`. Only `superclaude install --force`, `superclaude update` (`src/superclaude/cli/main.py:365-404`, every installer call there passes `force=True`) or `./update.sh` (`update.sh:8`) refresh them. This matters for every post-merge check below. |

Who triggers a release: a human maintainer, by hand, following section 3.3. Nothing in this repository triggers it automatically (no tag or release workflow, no Makefile target).

## 4. Inventory of in-flight work

Verdict key: **IN** = should be in the next release; **GATE** = not shipped code, but its result decides go/no-go; **DEFERRED** = a later release; **ABANDONED-candidate** = a human can retire it (delete branch, archive package or close issue) after a look. Ahead/behind counts are against `origin/master` `75d0d1e2` from `git rev-list --left-right --count origin/master...<ref>` (behind first). "Residual" means files the branch changed that still differ from `origin/master` (`git diff --name-only origin/master <ref> -- <files the branch changed>`); for squash-merged branches 0 residual means the content is on master.

### 4.1 Active work (live Orca workers or pending checks)

| # | Item | Location | Status | Remaining work | Risk | Verdict and reason |
|---|---|---|---|---|---|---|
| A1 | `/sc:pr-submit` handles Codex review threads like Augment | Worktree `.dev/worktrees/pr-submit-codex`, branch `feat/pr-submit-codex-reviews` at `d1b69dd3` (1 behind, 0 ahead, no commits yet). Untracked: `.dev/pr-submit-codex/design/pr-submit-codex-design.md` (29 KB) and plan `.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/` (15 tasks, no `progress.md`, so 0 executed). Orca `task_fa91cc7b202b`, dispatch `ctx_421bb15b7195` live; an earlier dispatch `ctx_2ff0f9ac5f09` failed. | Plan written; pre-execution reflect card scored C=0.83 with `escalation_recommendation: escalate` and two open notes (design section 14 contradiction, section 17 UNVERIFIED items not treated as risks) (`artifacts/reflect-pre/reflection-card.yaml`) | Resolve the reflect notes, execute 15 tasks, open PR, review | Medium-high: `/sc:pr-submit --monitor 3` is the mandatory PR path (CLAUDE.md "PR Target = Fork"), so a defect breaks every PR | **DEFERRED** to the following minor release. It has not started executing, and holding a release whose content is already on `master` for a 15-task change adds risk without benefit. If it merges before the cut-off events in section 6 complete, it simply rides along. |
| A2 | Endless QA-loop investigation (codebase-memory vs codegraph) | Worktree `.dev/worktrees/qa-loop-investigation`, branch `research/qa-loop-codememory-20261031` at `75d0d1e2` (0/0). Untracked `.dev/qa-loop-investigation/` with `README.md` and four `research/` files; only `research/02-github.md` has content (13.9 KB); `FINDINGS.md` and the evaluation and debate folders do not exist yet. Orca `task_b3e713500353`, dispatch `ctx_643ac2e7c0d6` live. | Research in progress | Finish synthesis, evaluation, debate, `FINDINGS.md` | Unknown until findings exist. Interim evidence: the #323 inventory comment (2026-10-29T16:20:52Z, quoted in `research/02-github.md`) says codebase-memory had "12 files, all installer/CLI/docs/tests. No skill, command or agent uses it", which argues against it causing protocol QA loops | **GATE**. Research only, ships nothing. If `FINDINGS.md` names a defect in a shipped protocol (`/sc:implement` or `/sc:workflow` QA) that causes unbounded loops, that fix becomes a release blocker; otherwise it does not hold the release. |
| A3 | Codegraph Phase 3 post-merge live check | PR #336 body: "After merge and `superclaude install`, run `/sc:troubleshoot "install_core_files skips files" --depth quick` once to confirm the installed command writes `tier1-callers.md`." Evidence of why: `.dev/codegraph-migration/experiments/P3-T11-smoke.md:94-101` (installed pre-Phase-3 skill shadowed the new one). | Pending. `orca worktree ps` shows the "Orchestrator" session in `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init` with the line "run superclaude install and the troubleshoot check"; its result is UNVERIFIED. | Run the check and record the result on #323 | Medium. Defect found here: plain `superclaude install` skips every existing skill, command, agent and core file (`install_skills.py:102-103`, `install_core.py:66-68`), so after a plain install the old troubleshoot skill and old `~/.claude/CLAUDE.md` stay and the check can fail or pass for the wrong reason. The smoke record's expectation that "the next `superclaude install`" fixes the shadowing (`P3-T11-smoke.md:97`) is therefore wrong. The smoke record's expectation that "the next `superclaude install`" fixes the shadowing (`P3-T11-smoke.md:97`) is therefore wrong. Use `./update.sh` (`update.sh:8`, `--force`) or `superclaude update` (`main.py:365-404`). | **GATE** (must pass before tagging). |
| A4 | Codegraph upstream release monitor | Plan merged in #335 (`d1b69dd3`); package `.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/` (8 tasks; `progress.md` holds only the header and `PLAN:` pin, 0 tasks started). Spec `.dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md`. | Planned, not executed | Run spec section 0 setup, `/sc:implement` the package, then the post-merge live dry run (spec T7, line 416) | Low for the release (adds a new scheduled workflow and `scripts/codegraph_release.py`, nothing existing changes). PR #335 body lists UNVERIFIED: the `attestations: read` permission and whether Coder's image bake reads the pin from `install_codegraph.py`. | **DEFERRED**. Not needed for users; the pinned codegraph `1.6.2` ships either way (CHANGELOG.md:42). |
| A5 | Coder side of Phase 3 | Coder pin is `2cb683f` (Coder PR #423), before #336. The #323 Coder addendum (comment 2026-10-31T15:56:54Z) asks for a pin bump plus a re-sync of the `SUPERCLAUDE_CODEGRAPH_BEGIN/END` block of `src/superclaude/core/CLAUDE.md` into the Coder seed and existing workspaces. | Pending, cross-repo | Bump Coder pin to the release commit or tag; re-sync the marker block | Medium: Coder users otherwise run Phase 2 without Phase 3 guidance | **IN** as a post-tag step (point the pin at the tag, not at an arbitrary `master` SHA). |

### 4.2 Open pull requests

| # | Item | Location | Status | Remaining work | Risk | Verdict and reason |
|---|---|---|---|---|---|---|
| P1 | Onboarding deck built from the routing guide | PR #303, branch `docs/onboarding-deck-default-planner`, head `5bf31eb3` (2026-10-26), 41 behind, 1 ahead, 158 files | OPEN; `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`; CI `SUCCESS` on head; 0 review threads (GraphQL `reviewThreads`) | Rebase; reconcile with issue #320 ("Compare PR #303 onboarding guidance with recovered SC/BMAD command research"); rebuild from the current `HOW-WE-WORK.md`, which gained `/sc:graph` and `/sc:impact` rows in #336 | Low (docs only), but stale: it was built from the routing guide at `adaa28d9` (commit subject) | **DEFERRED**. Docs, not shipped behavior; it needs a rebuild before it is accurate. |

### 4.3 Unmerged branches with their own unmerged content

| # | Branch | Last commit | Ahead/behind, residual | PR | What it holds | Verdict and reason |
|---|---|---|---|---|---|---|
| B1 | `origin/feat/auggie-claim-gate` | `edd340a5` 2026-10-28 | 3 ahead / 112 behind; 211 non-`.dev` files differ | none | "feat(auggie-review): publish only admitted defects through a claim gate", plus `713d8e42` "route grounding off hosted Augment; replace auggie-review CLI" and `c21858af` "rename Augment consumers to the LiteLLM gateway tool name". Plans `.dev/tasks/to-do/TASK-WF-design-20261020-090627` (12 tasks) and `TASK-WF-designV2-20261020-132032` (13 tasks) have no `progress.md`. | **DEFERRED** (human decision 7.4). Large, 112 commits behind master, overlaps the auggie-review remediation already merged in #296/#300 and the codegraph changes to auggie-review in #336. |
| B2 | `origin/fix/root-plugin` | `c35506f9` 2026-10-25 | 1 ahead / 56 behind; 49 non-`.dev` files (`.claude-plugin/plugin.json`, root `agents/*.md`), 2,991 files total | none | "fix(plugin): restore root reflection and preserve pending evidence" | **DEFERRED** pending triage (decision 7.5). No PR, so it was never reviewed; whether master already fixed it is UNVERIFIED. |
| B3 | `ironbelly/cifail` (local only) | `6bb595c2` 2026-10-28 | 1 ahead / 51 behind; 3 brainstorm files differ from the merged #316 commit `093a9b98` | none | "10x increase to brainstorm budgets to account for caching" | **ABANDONED-candidate**. Same intent as #316 (merged as `093a9b98`, "Increased Budget by 10x"); differs in 3 files (`git diff --stat 093a9b98 ironbelly/cifail -- src/superclaude/skills/sc-brainstorm-protocol`: 15 lines each way). Confirm the merged version is the wanted one. |
| B4 | `ironbelly/codegraph-release-monitor` (local only) | `d7e98797` 2026-10-31 | 39 ahead / 5 behind; 197 residual, mostly `.dev/` | none | "docs(plan): codegraph release monitor (#323)" | **ABANDONED-candidate**. Its `-plan` sibling merged as #335 with 0 residual; this looks like the pre-review copy (UNVERIFIED that nothing unique remains). |
| B5 | `backup/pre-rebase-phase2-1793367773` (local only) | `1134665a` 2026-10-30 | 35 ahead / 12 behind; 200 residual `.dev/` files | none | Pre-rebase backup of codegraph Phase 2 | **ABANDONED-candidate** after confirming #329 holds everything wanted. |
| B6 | `origin/feature/prd-spec-flag` | `ff1a3f10` 2026-06-07 | 3 ahead / 383 behind; 9 non-`.dev` files incl. `src/superclaude/cli/sprint/rerun_tasks.py` | none | "fix(sprint): rerun-tasks verify-checkpoints option mismatch" plus reflect doc fixes | **DEFERRED** pending triage: a sprint fix that may still matter; 383 behind. |
| B7 | `origin/reflectWrapper` | `879bb64f` 2026-06-10 | 4 ahead / 371 behind; 32 non-`.dev` files (`src/superclaude/cli/reflect/*`) | #157 CLOSED | `superclaude reflect run` POST-gate wrapper, task-builder `--reflect` dial | **ABANDONED-candidate**: PR closed unmerged. |
| B8 | `origin/brainstorm/t2-bare-reviewer-adjunct` | `757a3824` 2026-05-30 | 5 ahead / 406 behind; 12 non-`.dev` files | none | sc-bare-review v1.0 and scanner fixes; `src/superclaude/skills/sc-bare-review/` already exists on master | **ABANDONED-candidate**: the skill landed on master by another route (`ls src/superclaude/skills/sc-bare-review/`). |
| B9 | `origin/fix/claude-process-stdin-large-prompts` | `2c212794` 2026-05-01 | 12 ahead / 517 behind; 5 non-`.dev` files (`src/superclaude/cli/pipeline/process.py`, tests) | none | stdin patch for huge prompts with tests | **DEFERRED** pending triage: 517 behind; whether master solved it is UNVERIFIED. |
| B10 | `origin/fix/eval-doc-tests` | `9d62a723` 2026-10-04 | 1 / 145; 10 files | #260 CLOSED | Duplicate of #259 (merged) | **ABANDONED-candidate**. |
| B11 | `origin/sync/framework` | `d3cf5938` 2026-10-23 | 1 / 78; 20 files | #283 CLOSED | Automated framework sync, retired by #291 ("Retire framework sync, Codecov upload ...") | **ABANDONED-candidate**. |
| B12 | `.dev`-only leftovers: `origin/chore/sprint-progress-report-template` (2 files), `origin/claude/task-builder-template-review-rqaq63` (2 review docs), `origin/docs/ataraxy-labs-eval-plan-remediation` (29 backlog files), `origin/docs/auggie-review-workflow-implement-plan` (3 files), `origin/ReflectInTaskList` (#138 merged; 35 `.dev` files), `origin/feature/ccsession-native-install` (#236 merged; 73 `.dev` task files) | 2026-05-30 to 2026-10-09 | residual is `.dev/` only (batch output above) | see column | Planning and evidence documents only | **DEFERRED** (not shipped). Decide per branch whether the `.dev` records are worth a small archive PR; nothing affects the package. |

### 4.4 Branches whose content is already on master (squash-merged; residual 0 or identical to the merge commit)

`chore/codegraph-migration-followup` (#334), `feat/codegraph-adoption` (#336), `ironbelly/codegraph-release-monitor-plan` (#335), `chore/tasks-review-loops-done-t5-ruling` (#317), `docs/recovered-command-evaluation` (#319), `ironbelly/OrcaCLISkillRefactor` (#306, #308), `ironbelly/refactor-sc-auggie-review-remediation` (#296, #300), `chore/preserve-retired-worktree-artifacts` (no PR, residual 0), `ironbelly/mcp-litellm-gateway-entry` (#327; `git diff 00d4a559 <branch>` on its 4 files is empty), `ironbelly/BrainstormBudget` (#316; identical to `093a9b98`), `fix/restore-eval-docs` (#259). **ABANDONED-candidate** (branch deletion only). Worktrees still attached to some of them: `.dev/worktrees/codegraph-adoption` (clean), `/home/coder/workspaces/worktrees/IronClaude/codegraph-release-monitor` (clean), `/home/coder/workspaces/worktrees/IronClaude/mcp-litellm-gateway-entry` (untracked `.codegraph/` only), `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init` (**untracked** `.dev/codegraph-migration/review/M-open-questions-analysis.md`, `.dev/session-recovery/`, `.dev/troubleshoot/docs-pr334-gh-attestation-verify-omits-artifact-20261030165933/`: save these before removing it). `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` is on `ironbelly/OrcaCLICommandRefactor-Specs` with 0 ahead / 3 behind and a clean tree: no work in it.

### 4.5 Plan packages in `.dev/tasks/to-do/` on master

| Package | State (from task file / `progress.md`) | Verdict |
|---|---|---|
| `TASK-WF-followupCodegrap-20261030-153943` | 8 tasks, 0 started | A4, DEFERRED |
| `TASK-WF-implementTheAppr-20261024-060449` (recommend routing refresh) | T1-T8 `complete` with three human rulings; last line `FINAL: issues evidence=./artifacts/final-review-1.json:1,...`; the work merged as #295 (2026-10-24) | **ABANDONED-candidate** for the to-do folder: shipped, but the final review recorded issues and the package was never archived. Confirm the rulings, then archive. |
| `TASK-WF-mergedOutput-20261024-165151`, `TASK-WF-planTheSpecAtDev-20261024-182838` (severity model for `/sc:implement`) | 14 tasks each, no `progress.md`; the feature merged as #297 (2026-10-25) | **ABANDONED-candidate** (superseded plans). |
| `TASK-WF-design-20261020-090627`, `TASK-WF-designV2-20261020-132032` (auggie claim gate) | 12 and 13 tasks, no `progress.md` | Tied to B1, DEFERRED |
| `TASK-WF-specScRecommendR-20261024-055620` | only `return-contract.yaml` | ABANDONED-candidate |
| `TASK-RESEARCH-recommend-refresh-20261024-044336` | `status: research-complete-pending-user-approval`; implemented by #295 | ABANDONED-candidate (archive) |
| `TASK-pr-submit-defaults-20260616` | `status: in-progress`, 7 of 9 boxes; open: reflect post gate and "Commit, push, and open a PR" (lines 43-44). Superseded: #177 set default L1 (2026-06-17), #285 set default monitor 3. | ABANDONED-candidate |
| 17 `TASK-RF-*` / `TASK-TDD-*` packages with `status: "🟢 Done"` and every box ticked (e.g. `TASK-RF-t2-fallback-ladder-20260706-050832` 94/94, `TASK-RF-tasklist-rfmerge-20260619-041423` 158/158) | Done since June-July, never moved to `done/` | ABANDONED-candidate (archive move only) |
| `TASK-RF-fr-rh1-1.7.0-integ-20260625-163500`, `TASK-RF-pr197-reduce-merge-20260628-205943`, `TASK-RF-reflect-config-error-observability-20260707-024841`, `TASK-RF-troubleshoot-hardening-20260611-023739` | No task file, only output folders (`qa`, `research`, `reflect-post`, `phase-outputs`) | ABANDONED-candidate (orphan evidence) |
| Loose files `ISSUE-pipeline-one-shot-output.md`, `PRD_TASK_MANAGEMENT_SYSTEM.md` | Not packages | Not assessed; outside release scope |

`.dev/releases/current/` holds `WorkflowV3` (`TASKLIST.md` 0 of 5 boxes ticked; last commit `5619aef1` 2026-09-30, while `/sc:workflow` task packages shipped in #256), `cleanup-debt-reduction` (shipped as #274, `08cbea9e`) and `cliEval` (evidence only, last commit `c1621ae6` 2026-07-25). None is a version release checklist; there is no release checklist file in the repository (`.dev/releases/templates/` holds only `CLICKUP-RELEASE-TASK-TEMPLATE.md`, a per-feature ClickUp template).

### 4.6 Open issues

| Issue | Relevance to the release | Verdict |
|---|---|---|
| #332 `/sc:load` lists a Write step but has no `.superclaude/.gitignore` instruction | Directly tied to the breaking change: session memory now lives in `<project>/.superclaude/memory/` (CHANGELOG.md:56, inside the "Breaking" entry at line 49), so users may commit it unknowingly | **IN** if a small fix lands before the cut-off; otherwise a release-notes warning |
| #333 `sc-crash-recovery` `bootstrap_scan.sh` exits non-zero and prints no JSON | A shipped skill fails on a fresh repo (repro in the issue body) | **IN** if fixed before cut-off; small, isolated |
| #315 Agent-spawned worktree sessions stuck at the ccsession name prompt | Hurts Orca workers. The proposed fix in the last comment allows only letters, digits, `.`, `_`, `-`, which conflicts with #325 (merged), which allows spaces and most characters (CHANGELOG.md:20). No branch or PR found. | **DEFERRED**; the fix must be redesigned against #325 |
| #324 Remove Serena | Done by #329 (CHANGELOG.md:49-54) but still open, 0 comments | **ABANDONED-candidate** (close as done) |
| #313 Tests must not depend on old `.dev/` logs and plans | CI fragility (2026-10-27 breakage after #306/#308); does not change shipped behavior | DEFERRED |
| #29, #143, #201, #289, #290, #302, #305, #320, #322, #326, #330, #331 | Features, designs, process decisions | DEFERRED |

No open issue carries a release, blocker or milestone label (`gh issue list --json labels,milestone`: every milestone is `-`; labels are only `bug` or `enhancement`).

## 5. Dependencies and ordering

```text
A3 post-merge check (./update.sh, then /sc:troubleshoot) ─┐
A2 QA-loop FINDINGS.md (blocker? → fix PR first) ─────────┼─► R1 release PR (version + CHANGELOG cut) ─► R2 tag v5.0.0 + GitHub Release ─► R3 /sc:post-release v5.0.0
optional: #332, #333 small fixes, if merged first ────────┘                                              └─► A5 Coder pin bump to the tag + CLAUDE.md marker re-sync
After the tag (next minor): A1 pr-submit Codex → A4 codegraph release monitor (its bump PRs go through /sc:pr-submit) → remove the one-release .serena fallback → housekeeping (section 4.3-4.5)
```

1. **A3 first, and run it correctly.** The #336 instruction is "After merge and `superclaude install`, run `/sc:troubleshoot "install_core_files skips files" --depth quick`". A plain `superclaude install` skips existing skills and core files (`src/superclaude/cli/install_skills.py:102-103`, `src/superclaude/cli/install_core.py:66-68`), so the installed pre-Phase-3 troubleshoot skill would stay and shadow the new one, the same failure seen in `.dev/codegraph-migration/experiments/P3-T11-smoke.md:94`. Run `./update.sh` (`update.sh:7-8`, uses `--force`) or `superclaude update` (`src/superclaude/cli/main.py:365-404`), start a new Claude session (a running session keeps the tool list it started with: #323 G6 comment 2026-10-30T21:35:25Z), then the troubleshoot check. Pass means `tier1-callers.md` is written with call-site-verified rows for `install` and `update` in `src/superclaude/cli/main.py`, as in the smoke record (`P3-T11-smoke.md:95`).
2. **A2 before R1.** If `FINDINGS.md` attributes endless QA loops to a defect in a shipped protocol, the fix merges before the release PR. If it attributes them to the old memory MCPs (now removed by #329) or to session state, the release proceeds and the findings go in the release notes.
3. **R1 after A2 and A3.** One PR on the fork via `/sc:pr-submit --monitor 3` (CLAUDE.md rule): set `version = "5.0.0"` in `pyproject.toml:7` and `__version__` in `src/superclaude/__init__.py:8`; move the 25 `Unreleased` entries into `## [5.0.0] - <date>`; add the release-notes file (decision 7.3); open a fresh `## [Unreleased]`. Anything that merges before R1 is opened rides along; anything after goes under the new `Unreleased`.
4. **R2 on R1's merge commit**, never on a later `master` SHA: `git tag -a v5.0.0`, `git push origin v5.0.0`, `gh release create v5.0.0 --repo IronbellyOrg/IronClaude ...` (`changelog_maintenance.md:125-136`, with `--repo` added per CLAUDE.md).
5. **R3 and A5 after R2.** `/sc:post-release` requires an existing tag (`src/superclaude/commands/post-release.md:15,35`). Coder's pin should point at the tag commit so Coder users and git users get the same code; the marker block re-sync comes from the #323 addendum (comment 2026-10-31T15:56:54Z).
6. **A1 and A4 after the tag.** A1 (15 tasks, 0 executed) changes the mandatory PR tool; A4 adds a scheduled workflow whose bump PRs will be reviewed through `/sc:pr-submit`, so landing A1 first means A4's PRs get Codex threads handled. A4's own order is fixed by PR #335: merge the monitor PR before its live dry run (spec T7, `followup-codegraph-release-monitor-spec.md:416`).
7. **The one-release Serena fallback.** `CHANGELOG.md:56` says "For one release `/sc:load` still reads an existing project `.serena/memories/<key>.md`". Tagging v5.0.0 is what makes "one release" concrete: removal of that fallback belongs in the release after v5.0.0.
8. **Housekeeping is independent.** Deleting the ABANDONED-candidate branches (sections 4.3-4.4), archiving Done packages (4.5) and closing #324 can happen any time; doing it after the tag keeps the release diff small. Save the untracked files in `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init` before removing that worktree.

## 6. Proposed release

### 6.1 Version: `5.0.0` (tag `v5.0.0`)

- The repository's own rule: "MAJOR (X.0.0): Breaking changes, incompatible API changes" (`src/superclaude/rules/core/changelog_maintenance.md:157`).
- The `Unreleased` section contains user-visible incompatible changes:
  - `CHANGELOG.md:49` entry titled "Breaking: codebase-memory-mcp and Serena removed; session memory moves to `.superclaude/memory/` files (#323)".
  - `CHANGELOG.md:54`: `superclaude mcp` loses `--uninstall` and `--yes`; `superclaude mcp --servers serena` now fails with "Unknown MCP server selection: serena".
  - `CHANGELOG.md:57`: `/sc:reflect` loses `--onboard` and `--with-hierarchy`.
  - `CHANGELOG.md:21`: `/ccsession-tag` retired (use `/rename`).
  - `CHANGELOG.md:157` (heading) and `:168`: `/sc:pr-submit` drops `--yes`.
  - `CHANGELOG.md:203`: core files `ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`, `MCP.md` no longer shipped.
- Plus large additive features (codegraph installed by default, `/sc:impact`, `/sc:graph`, ccsession tiers and naming, routing guide), 381 commits and 169 merged PRs since 4.3.5 was set (section 2). A patch (4.3.6) is ruled out; a minor (4.4.0) would contradict the rule above.
- Caveat for decision 7.1: CLAUDE.md ("Plugin System (v5.0 - Not Yet Available)") reserves "v5.0" for a TypeScript plugin system that links to the upstream parent's issue #419. The fork's numbering already diverged from upstream (fork 4.3.5, upstream latest `v4.3.0`), so the collision is cosmetic, but a human should confirm.
- Per `changelog_maintenance.md:89-96` a major version requires a detailed release-notes file (decision 7.3 for where it lives).

### 6.2 Cut-off point

Cut the release when all three of these are true, and tag the merge commit of the release PR:

1. **A3 passed**: after `./update.sh` (or `superclaude update`) and a new session, `/sc:troubleshoot "install_core_files skips files" --depth quick` writes `tier1-callers.md` with call-site-verified rows, and the result is posted on #323.
2. **A2 concluded**: `.dev/qa-loop-investigation/FINDINGS.md` exists in the QA-loop worktree and either names no defect in a shipped protocol, or the fix it names has merged to `master`.
3. **R1 merged**: the release PR (version `5.0.0` in both version files, `CHANGELOG.md` `[5.0.0]` section, release-notes file) merged on the fork with the `Tests` workflow's `test-summary` job green.

Content cut-off: everything on `origin/master` when R1 is opened. Today that is `75d0d1e2` plus whatever lands before R1. A1 (pr-submit Codex), A4 (release monitor), P1 (#303) and B1 (claim gate) are excluded unless they merge before R1 is opened.

### 6.3 Go/no-go checks before tagging

Run on the R1 merge commit. Every check must pass; any failure is a no-go.

| # | Check | Command | Pass condition |
|---|---|---|---|
| G1 | Fork target | `git remote -v`; `gh repo view --json nameWithOwner -q .nameWithOwner` | `origin` is `IronbellyOrg/IronClaude`; gh prints `IronbellyOrg/IronClaude` (CLAUDE.md pre-PR checks) |
| G2 | CI on the exact commit | `gh run list --repo IronbellyOrg/IronClaude --branch master --limit 3 --json headSha,conclusion,workflowName` | `Tests` = `success` for the R1 merge SHA |
| G3 | Version consistency | `grep -n '^version' pyproject.toml; grep -n '__version__ =' src/superclaude/__init__.py; uv run superclaude --version` | all three say `5.0.0` |
| G4 | Changelog cut | `grep -n '^## ' CHANGELOG.md` | `## [Unreleased]` is empty and followed by `## [5.0.0] - <date>`; the "Breaking" entry is in 5.0.0 |
| G5 | Full local suite and gates (same as CI, on the build host) | `make test`; `make lint`; `make verify-sync`; `make verify-deps`; `make lint-architecture` | all exit 0 |
| G6 | Package builds | `uv build` (`scripts/README.md:11`) | wheel and sdist built, no upload |
| G7 | Upgrade path on an existing workspace | `./update.sh`, new session, `superclaude doctor`, `superclaude install --list`, `/sc:graph status` | doctor passes; `--list` shows the codegraph block and retired names (CHANGELOG.md:45, :65); `/sc:graph status` reports an index state |
| G8 | A3 and A2 conditions | section 6.2 items 1-2 | recorded on #323 and in `FINDINGS.md` |
| G9 | No open PR meant for this release | `gh pr list --repo IronbellyOrg/IronClaude --state open` | only deferred PRs (today: #303) |

After a GO: `git tag -a v5.0.0 -m "Release v5.0.0 - codegraph replaces codebase-memory and Serena"`, `git push origin v5.0.0`, `gh release create v5.0.0 --repo IronbellyOrg/IronClaude --title "v5.0.0 - ..." --notes-file <release-notes file>`, then `/sc:post-release v5.0.0` and the Coder pin bump (A5).

### 6.4 Date window

Recommended window: **2026-11-02 to 2026-11-06**, conditional on section 6.2. Basis: both gating items are being worked today (Orca dispatch `ctx_643ac2e7c0d6` live on A2; the A3 check is in the "Orchestrator" session per `orca worktree ps`), and the release PR itself only edits two version lines, the changelog and one notes file. The evidence supports the order of events more than the dates: if A2 names a protocol defect, the window moves by the time that fix takes.

## 7. Decisions needed from a human

Each is one question with a recommendation. They are listed in the order they block the release.

**7.1 Version number.** Should the next release be `5.0.0` (the repository's semver rule, because the changelog holds a "Breaking" entry and removed options), or `4.4.0` (keeping "v5.0" for the TypeScript plugin system CLAUDE.md mentions)?
Recommendation: `5.0.0`. Users who run `superclaude mcp --servers serena` or `/sc:reflect --onboard` get errors after updating (CHANGELOG.md:54, :57), which is exactly what a major number warns about; the v5.0 plugin note refers to the upstream parent's roadmap, whose numbering the fork no longer follows.

**7.2 The `/sc:pr-submit` Codex refactor (A1).** Should the release wait for it, or ship without it and take it in 5.1.0?
Recommendation: ship without it. Its 15-task plan has not started executing and its pre-execution review asked for escalation (`reflection-card.yaml`, C=0.83), while everything else in the release is already on `master` and in users' hands.

**7.3 Where the release notes file lives.** `changelog_maintenance.md:107` says `.claude/changelogs/`, which `.gitignore:123` ignores and CLAUDE.md forbids staging. Where should the v5.0.0 detailed notes be committed?
Recommendation: a new tracked file `docs/releases/v5.0.0.md` (no `docs/releases/` exists yet; `ls docs/`), used as the `gh release create --notes-file`; fix the path in `src/superclaude/rules/core/changelog_maintenance.md` in a follow-up PR.

**7.4 The auggie claim-gate branch (B1).** Should `origin/feat/auggie-claim-gate` (3 commits, 211 non-`.dev` files, 112 commits behind, no PR) be revived after the release or retired?
Recommendation: decide after 5.0.0; do not rebase it now. Its two unexecuted plans overlap auggie-review work merged since (#296, #300, #336), so reviving it means re-planning from current `master`, not merging the branch.

**7.5 The root-plugin fix (B2).** Should someone triage `origin/fix/root-plugin` (`c35506f9`, 49 non-`.dev` files including `.claude-plugin/plugin.json`, never opened as a PR) into a PR, or delete it?
Recommendation: triage it after the release with a diff against `master`; it is not a release blocker because it was never on `master`.

**7.6 Running the A3 check.** Will the maintainer run the post-merge check with `./update.sh` (or `superclaude update`) instead of the plain `superclaude install` that PR #336 names?
Recommendation: yes. Plain install skips existing skills (`install_skills.py:102-103`), so the check would exercise the old troubleshoot skill.

**7.7 Defining the "release gate".** `/sc:post-release` says "the release gate tags the version" but no gate is defined anywhere. Should the go/no-go list in section 6.3 become that gate?
Recommendation: yes, use section 6.3 for v5.0.0 and write it into the release procedure afterwards.

**7.8 Cleanup.** May the ABANDONED-candidate branches (sections 4.3-4.4), the Done and superseded plan packages (4.5) and issue #324 be retired in one housekeeping change after the tag?
Recommendation: yes, after the tag, and only after the untracked files in `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init` are saved.

## 8. Evidence log (commands run)

All commands were read-only. Nothing was staged, committed, pushed, tagged, fetched into refs, or changed in another worktree, PR, issue or Orca worker. Run 2026-10-31 between 18:24Z and about 19:10Z.

| Purpose | Command (run from `/home/coder/workspaces/IronClaude` unless noted) |
|---|---|
| Worktrees | `git worktree list` |
| Unmerged branches | `git branch -a --no-merged origin/master --format='%(refname:short)\|%(committerdate:short)\|%(objectname:short)\|%(subject)'` |
| Tags | `git ls-remote --tags origin`; `git tag -l`; `git show v3.9:pyproject.toml` |
| Per-worktree state | batch script: `git -C <path> status --short --branch --untracked-files=normal`, `git -C <path> rev-list --left-right --count origin/master...HEAD`, `git -C <path> log -3` for all 9 worktrees |
| Per-branch content | batch script: `git rev-list --left-right --count origin/master...<b>`, `git diff --name-only origin/master...<b>`, residual `git diff --name-only origin/master <b> -- <files>`, non-`.dev` file lists, `git diff --stat 00d4a559 <litellm branch>`, `git diff --stat 093a9b98 <brainstorm branches>` |
| PRs | `gh pr list --repo IronbellyOrg/IronClaude --state open\|merged\|closed\|all ... --json ...`; GraphQL `pullRequest(number:303){mergeable mergeStateStatus reviewThreads ...}`; `gh pr view 336`, `gh pr view 335` |
| Issues | `gh issue list --repo IronbellyOrg/IronClaude --state open --json number,title,labels,updatedAt,milestone`; `gh issue view 323` (comments, closedAt); `gh issue view 324 315 333 313 322` |
| CI | `gh run list --repo IronbellyOrg/IronClaude --branch master --limit 5` |
| Releases | `gh release list --repo IronbellyOrg/IronClaude`; `gh release list --repo SuperClaude-Org/SuperClaude_Framework --limit 5` (read-only) |
| Coder pin | `gh pr list --repo IronbellyOrg/Coder --state all --search codegraph` |
| Version history | `git log origin/master -S'version = "4.3.5"' -- pyproject.toml`; `git rev-list --count 5d660ca9..origin/master`; `git rev-list --count v3.9..origin/master` |
| Plan packages | loop over `.dev/tasks/to-do/*/` counting `- [x]` / `- [ ]`, `status:`, `progress.md` lines and `T<n>: <state>` records; same for the pr-submit worktree package |
| Orca | `orca orchestration worker-list --json`; `orca worktree ps`; `orca orchestration check --terminal <self> --json` |
| Release process | `ls .github/workflows/`; `.github/workflows/README.md`; `grep -n -i 'release\|tag\|version\|build' Makefile`; Grep for `release gate\|git tag\|gh release\|publish` across `src/`, `docs/`, `scripts/`; Read `src/superclaude/rules/core/changelog_maintenance.md:60-185`; `scripts/README.md`; `src/superclaude/commands/post-release.md`; `git check-ignore -v .claude/changelogs/x.md` |
| Install behavior | Read `src/superclaude/cli/install_core.py:1-90`; Grep `exists() and not force` in `src/superclaude/cli/install_*.py`; Grep `--force` in `update.sh`, `install.sh`, `src/superclaude/cli/main.py` |
| Codegraph records | Read `.dev/codegraph-migration/experiments/P3-T11-smoke.md:80-101`; `.dev/codegraph-migration/FINAL-SUMMARY.md:305-312` |
| In-flight artifacts | `find` listings of `.dev/qa-loop-investigation/`, `.dev/pr-submit-codex/` and the pr-submit plan package; Read of their `README.md`, `research/02-github.md:1-60`, `reflection-card.yaml` |

Not done, by constraint: running `superclaude install`, `./update.sh` or the A3 check; `git fetch`; contacting any other Orca worker. The A3 result and the Coder-side pin trigger stay UNVERIFIED here.
