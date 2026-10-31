# Task M result: codegraph upstream release monitor (spec and plan)

Date: 2026-10-30 to 2026-10-31. Worker task `task_1a3ad1434d76`, dispatch `ctx_166b698e7e94`. Branch `ironbelly/codegraph-release-monitor` (local only, stacked on PR #329's head `e62ed152`). Planning only: no source, test or workflow file changed.

## Spec

`.dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md` (539 lines). Sections: §0 goal, inputs, 8 verified facts, execution setup and evidence rule; §1 preflight (11 files); §2 design (run order, `scripts/codegraph_release.py` contract, workflow, candidate selection, proof and failure handling, PR body); §3 tests (R1-R22 plus static workflow checks); §4 tasks T0-T7, each with files, change, exact acceptance commands and a conventional commit point; §5 issue #323 progress comments; §6 autonomy rules (simple self, mid `/sc:adversarial --compare ... --depth quick`, complex `/sc:adversarial --compare ...`); §7 human intervention (6 items); `## Decisions` (21 rows); `## Review resolution`.

Findings that change the original outline:
- The pin is not single-source today: 22 literal sites in tests and docs (including `1.6.3` at `tests/cli/test_install_codegraph.py:306,320`, which would break the first patch bump). T1 removes them and adds a guard test plus a next-patch/minor/major mutation check.
- `codegraph install --print-config claude` exists (upstream `src/bin/codegraph.ts:2803`) and prints a `# Add to <path>` line before the JSON.
- Bot PRs opened with `GITHUB_TOKEN` get approval-gated CI, so the monitor dispatches `test.yml` on the bump branch.
- `actions/checkout` keeps the token in `.git/config` by default; the workflow uses `persist-credentials: false` because `prove` runs the third-party binary.
- Release notes can exceed the PR body limit (v1.6.2: 76,281 characters); bodies are budgeted at 60,000 characters with links.
- Whether Coder's codegraph image bake reads `VERSION`/`SHA256` from `install_codegraph.py` is UNVERIFIED (human item 6).

## Package

`.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/`:
- `TASK-WF-followupCodegrap-20261030-153943.md`: plan (schema `workflow-plan/1.2`, version 2), 5 phases, 8 tasks.
- `source.md`: byte-identical to the spec (`cmp` prints nothing).
- `progress.md`: header plus the `PLAN:` pin over the final plan and `source.md`.
- `return-contract.yaml`: contract 1.1, status success, handoff none, `reflect_status: partial`.
- `artifacts/reflect/pre-20261030154210/`: the full reflect run (moved here from `.dev/reflect/`, the implement protocol's convention for reflect output; `.dev/reflect/` is outside this task's staging scope).

Next step for execution: run the spec's §0 "Execution setup" block (worktree `.dev/worktrees/codegraph-release-monitor-impl` on new branch `ironbelly/feat-codegraph-release-monitor` from `origin/master`, cherry-pick the `docs(plan): codegraph release monitor (#323)` commit), then in that directory `/sc:implement .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/TASK-WF-followupCodegrap-20261030-153943.md`.

## Reflect status

`/sc:workflow --depth standard --handoff none` ran its advisory `/sc:reflect --mode pre`: **partial**. Report: `.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/artifacts/reflect/pre-20261030154210/REPORT.md`.
- Tier 2 (forced: the spec's labels `R1`/`T0` give Pass 1 zero ids, so coverage came from 338 quote-pinned Pass 2 rows; 4 domains). Reviewers: sonnet, glm-5.3 (haiku slot), fable; calibrator opus. All said revise.
- Why partial: two `sc:adversarial` merge attempts stalled (their advocate subagents never returned), so fallback F2 used the best-calibrated reviewer card (`merge_method: single-reviewer-fallback`, `adversarial_unavailable: true`). The evidence validator upheld 108 of 109 citations (1 external `action.yml` anchor dropped), and 30 of 30 sampled requirement quotes were exact. No input drift.
- Findings: 2 critical (no planning commit to cherry-pick; job token readable by the third-party binary), 18 important, 31 minor rows. **All fixed** in the spec, `source.md` and plan version 2 (spec `## Review resolution` maps each finding to its fix). A fresh reflect on version 2 was not run.

## Decisions taken

| Decision | Options considered | Method | Result |
|---|---|---|---|
| (a) Major versions | A ready PR like minors; B issue only; C full PR always draft | `/sc:adversarial --compare ... --depth quick` (`decisions/M-major-versions/`) | C (0.875 vs B 0.832, A 0.697): same verify and proof, always a draft titled `codegraph MAJOR <tag>: manual review`; within-major bumps keep flowing |
| (b) Minimum release age | A none; B 14 days with fallback; C 7 days latest only | adversarial quick (`decisions/M-release-age/`) | B with C's no-fallback (0.819): highest-semver release once 14 days old, never an older one; `min_age_days` manual override; stall warning at 28 days |
| (c) Failed proof output | A draft PR; B issue only; C split by failure class | adversarial quick (`decisions/M-proof-failure/`) | C (tiebreak over B): integrity failure = issue only, no branch; behaviour failure = draft PR `[proof failed: <stage>]`; infrastructure = warning, issue after 3 failed runs |
| Branch rule (conflict between a and c) | fixed branch per line, force-pushed; branch per version, never re-pushed | self | per-version branch `codegraph/bump-<tag>`, older PR on the line superseded |
| Others (17 rows) | see spec `## Decisions` | self | logic in a tested stdlib script; GitHub side effects in its `apply` subcommand; push before tests and prove; package values via a child process; token isolation; gate in `check`; worktree setup before `/sc:implement` |

## Precondition for execution

PR #329 merged to `master`, the executor branching from `master` after that. **Met:** `gh pr view 329` reports MERGED at 2026-10-30T15:23:26Z, merge commit `2f10a0e1`. The executor still runs the §0 setup block first (T0 verifies it and stops as blocked if skipped).

## Open items

- Items the decision debates flagged for the user (none blocks execution): spec `## Decisions`, last paragraph.
- UNVERIFIED: whether `gh attestation verify` in Actions needs `attestations: read` (T7 dry run shows it; the fix path is in the spec).
- UNVERIFIED: Coder's bake reading the pin from `install_codegraph.py` (human item 6).
- The planning branch is local only (not pushed, per this task's constraints); the setup block must run in this clone, or someone pushes the branch first.
- One `python3` call (not `uv run`) edited `return-contract.yaml` during this task; it changed no tracked file.
