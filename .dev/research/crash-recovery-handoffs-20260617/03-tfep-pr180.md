# TFEP PR180 handoff

## Current state

- Lane: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`.
- Branch: `feat/tfep-troubleshoot-backend` tracking `origin/feat/tfep-troubleshoot-backend`.
- HEAD: `c8363739ce8f634ab3c65862a96428dd6b0d6d66` (`feat(tfep): migrate Test Failure Escalation Protocol off /sc:forensic onto /sc:troubleshoot`).
- PR: `https://github.com/IronbellyOrg/IronClaude/pull/180`, OPEN, base `master`, merge state `UNSTABLE`.
- Local worktree status at handoff: no tracked modifications, but one untracked review artifact directory exists: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/reviews/pr-180-20260617-1250/`.
- The MDTM task file says `status: "Done"` and completion date `2026-06-17`: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/TASK-RF-tfep-troubleshoot-migration-20260616-174519.md`.
- The final local task evidence claims `make sync-dev` and `make verify-sync` passed with exit 0, and states no `.claude/` paths were staged: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/reports/final-regression-summary.md`.
- The final residual-reference sweep says zero live `/sc:forensic` or bare `forensic` hits in `src/superclaude/skills/sc-task-protocol/SKILL.md` and `src/superclaude/commands/task.md`, and zero `/sc:forensic` hits under `src/`: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/test-results/final-residual-sweep.txt`.
- PR checks currently fail. `gh pr checks 180 --repo IronbellyOrg/IronClaude` shows failures for Dependency Allow-list (AC3), Lint and Format Check, Quick Test (Python 3.10), Test Summary, and Test on Python 3.10/3.11/3.12. Passing checks include Generator-Constraint Considered, Pytest Plugin Check, SuperClaude Doctor Check, and the two Swarm acceptance lanes.
- `gh run view ... --log` and `--log-failed` returned no log body in this session, but `gh run view ... --json jobs` did expose the failing job/step names. Re-fetch logs or open the job URLs in a browser before fixing CI.

Read-only commands used:

- `/usr/bin/git -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend status --short --branch`
- `/usr/bin/git -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend rev-parse HEAD`
- `/usr/bin/gh pr view 180 --repo IronbellyOrg/IronClaude --json number,title,state,isDraft,headRefName,headRepositoryOwner,baseRefName,mergeStateStatus,reviewDecision,statusCheckRollup,comments,reviews,commits,url,updatedAt`
- `/usr/bin/gh pr checks 180 --repo IronbellyOrg/IronClaude`

## QA conflict analysis

There are two different QA-conflict classes.

1. `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-content-backend-neutrality-pg6.md` looks stale against the final source for its two concrete FAILs.
   - It flags report-section layout prose at old `SKILL.md:257-258`, but the final source now reads `Root cause` and `Solution` from the return contract only, with no `Diagnosis`, `Proposed Fix`, or `Next Steps` section-layout clauses.
   - It flags `Tier-2 hypothesis cards` and `adversarial artifacts` at old `SKILL.md:260`, but the final source now says `troubleshoot report_path (REPORT.md), audit_log_path (audit.log), and any additional diagnostic artifacts emitted by the backend`.
   - This is corroborated by `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/pg6-verdict.md`, which records PG6 as PASS after one fix cycle and says the N1/N2 backend-neutrality leaks were fixed.

2. `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-post-domain-backend-neutrality.md` does not look stale for all findings; it is a real unresolved policy disagreement unless the team explicitly accepts these as non-blocking follow-ups.
   - The final source still says the diagnostic backend declaration promises backend swaps only change the declaration and invocation string.
   - The final source still contains backend-shaped wording outside those exact surfaces: `runs autonomously through all its phases`; `see sc:troubleshoot-protocol Wave 5 emission`; the Step 5 ownership note names `troubleshoot`; the incident artifacts line still names `troubleshoot` plus concrete `REPORT.md` and `audit.log` filenames.
   - `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-post-consolidated-findings.md` explicitly classifies the backend-neutrality leaks as `NOT FIXED` and calls them acceptable backend cross-references rather than residual forensic leaks.
   - `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-post-verification-content.md` then PASSes the final state and says those backend-neutrality items are follow-ups, not gate-blockers.

Bottom line: PG6's named fail file is stale after its fix cycle; the post-completion backend-neutrality FAIL is not fully stale. The final close-out chose to override/defer that lens rather than remediate it. If the intended invariant is strict backend swap-neutrality, remediation is still required. If the intended invariant is only zero live `/sc:forensic` residue plus a functioning troubleshoot adapter, the final PASS rationale is internally documented but should be made explicit in the PR narrative because it contradicts a FAIL QA artifact committed in the PR.

## First next action

Decide the backend-neutrality contract before touching code. The smallest safe action is to re-run one fresh, adversarial backend-neutrality review against the final source and treat it as authoritative over the stale PG6 file and the disputed post-completion disposition.

Single-line command/prompt for a new session:

`cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend && /sc:reflect --mode post --focus backend-neutrality --target /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md --context /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-post-domain-backend-neutrality.md`

If that is not a supported reflect shape in this checkout, use this paste-ready prompt instead:

`In /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend, read /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md and /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/qa/qa-post-domain-backend-neutrality.md, then decide whether the remaining backend-neutrality items are blocking; do not edit until you state the exact contract decision.`

## Validation/QA/test plan

After the contract decision, validate in this order:

1. Re-fetch current PR state: `gh pr view 180 --repo IronbellyOrg/IronClaude --json number,title,state,mergeStateStatus,statusCheckRollup,comments,reviews,commits,url,updatedAt`.
2. Fetch failing CI details before reproducing: `gh run view 27668613404 --repo IronbellyOrg/IronClaude --json conclusion,jobs,url` and `gh run view 27668613409 --repo IronbellyOrg/IronClaude --json conclusion,jobs,url`.
3. Reproduce local sync parity after any source edits: `make -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend sync-dev` and `make -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend verify-sync`.
4. Re-run the focused residual sweep: `rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/commands/task.md`.
5. Re-run quality gates that CI is failing or likely exercising: `make -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend lint`, `uv run --directory /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend ruff format --check src/ tests/`, and `uv run --directory /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend pytest`.
6. If dependency allow-list still fails, inspect the workflow/script before editing: `rg -n "allow-list|allowlist|Dependency Allow-list|AC3" /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.github /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/scripts /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/tests /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src`.
7. If CI failures are caused by committed `.dev/` markdown/artifact formatting rather than product source, decide whether those audit artifacts belong in PR #180 at all before formatting hundreds of files.

## Cleanup plan

- Do not stage `.claude/` mirrors. Only stage source-of-truth files under `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/` plus any deliberately retained `.dev/` artifacts.
- Inspect the untracked review directory before deleting or retaining it: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/reviews/pr-180-20260617-1250/`.
- The untracked review directory contains a zero-byte `findings.json`, zero-byte `auggie-stderr.log`, an `auggie-raw.json` whose embedded result reports zero findings, and `inputs/metadata.json` for PR #180 commit `c8363739`.
- If this is an ephemeral local review cache, remove it before committing/pushing any remediation: `rm -rf /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/reviews/pr-180-20260617-1250`.
- If the PR-size/CI failures are driven by committed `.dev/tasks` and `.dev/brainstorms` artifacts, consider a cleanup commit that removes or sharply reduces those artifacts from the PR after confirming the user wants the auditable trail excluded.

## PR monitor notes

- L1 monitor did not arm in this lane. I found no PR-submit monitor JSONL/log artifacts in the worktree; only the `pr-submit.md` command files exist.
- PR #180 has exactly one PR comment from `augmentcode`: the large-PR opt-in message requesting a comment of `augment review` before reviewing. There are no GitHub reviews in `gh pr view` output.
- A local untracked review artifact exists at `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/reviews/pr-180-20260617-1250/`; its `auggie-raw.json` says an Auggie-style protocol review found zero findings, but GitHub's Augment bot has not reviewed because it is waiting for large-PR opt-in.
- Because pushes do not trigger Augment re-review in this repo, after any remediation push, request review explicitly with a PR comment if Augment credits/policy permit: `gh pr comment 180 --repo IronbellyOrg/IronClaude --body "auggie review"`.
- Current PR checks are failing independently of Augment review. Do not treat a zero-finding local Auggie artifact as merge readiness.

## Risks

- The committed QA trail contains FAIL artifacts while the task frontmatter says Done. This is a process risk and reviewer-confusion risk even if the code is accepted.
- The backend-neutrality contract is internally ambiguous: strict reading says several remaining backend-shaped references violate the declaration; final close-out says those references are acceptable cross-references/follow-ups.
- PR #180 is very large: 164 files changed and about 15k insertions, mostly `.dev/` evidence. This likely contributed to Augment's large-PR opt-in and may contribute to CI/lint/allow-list failures.
- CI is red on lint, dependency allow-list, and full tests. The local task explicitly said no pytest was required because this was docs/skill prose, but repository CI does run broader gates.
- The post-reflect evidence says the wrapper was recursion-suppressed and returned exit 0; that is a pass for the wrapper path but not the same as an independent deep reflect audit.
- If remediation edits source files, run `make sync-dev` and `make verify-sync`; never stage `.claude/` generated mirrors.

## New-session prompt

`Work in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend on branch feat/tfep-troubleshoot-backend for PR #180 at c8363739. First invoke Skill sc:analyze with args "/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend --focus quality --depth deep --format report". Read /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/03-tfep-pr180.md, then inspect current git status and PR checks with read-only commands. Resolve the QA conflict before code edits: decide whether strict backend-neutrality requires fixing the remaining references in /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/src/superclaude/skills/sc-task-protocol/SKILL.md, especially "through all its phases", "Wave 5", the ownership note naming troubleshoot, and REPORT.md/audit.log artifact filenames. If you edit, edit only src/superclaude source-of-truth files, then run make -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend sync-dev and make -C /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend verify-sync, do not stage .claude paths, reproduce failing CI gates locally, clean or preserve /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/reviews/pr-180-20260617-1250 intentionally, and after pushing comment "auggie review" on PR #180 if review is desired.`
