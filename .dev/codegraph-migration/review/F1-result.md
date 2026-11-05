# Task F1 result: Phase 1 review findings applied and tasklist generated (issue #323)

Status: COMPLETE (task F1, 2026-10-29). Planning only: no source, test, doc or environment change; nothing staged or committed.

## 1. Review findings applied to the Phase 1 spec

Spec: `.dev/codegraph-migration/specs/phase-1-removal-spec.md`. Its new `## Review resolution` section (end of file) records each finding. Summary:

| Finding | Result |
|---|---|
| X-4 Serena gate (Phase 2 T0b) | applied: DoD-3, DoD-4, §2.3, §3.1, §3.2 Tier R/Tier K (`env`/`headers` absent or `{}`), §3.4 hint renamed `serena-local`, §3.5 tests, §3.6, §6.2, T12 CHANGELOG rule, T14 step 5, T15 facts-file override, D2. Phase 2 T0b acceptance (`phase-2-codegraph-install-spec.md` T0b block) passes: `rg -c codegraph_ready` = 14 (needs 7 or more), `serena-local` present, Tier R and Tier K lines match |
| X-12 T10/T11 too big | applied: T10a/T10b and T11a/T11b/T11c, each with scoped checks; repo-wide checks on the last piece (split adjusted, Decisions row 2) |
| X-15 CI step churn | applied (Phase 1 hunk): `Install Claude CLI` step kept, comments `test.yml:133-134`, `:155` rewritten |
| X-16 `install --list` on real HOME | applied: T3 runs it in a `mktemp -d` HOME |
| X-17 T5 search hits allowlisted files | applied: `-g` excludes added |
| X-24 row S19 contradiction | applied: keep unchanged (history) |
| X-5 (owner F2) | Phase 1 hunk only: §10 states Phase 2 owns the post-merge live check |
| X-9, X-6, X-7 (owner F3) | no Phase 1 change needed (Phase 1 already matches the prescribed ownership, floor and ledger) |

Handoff files under `.dev/codegraph-migration/handoffs/` were not edited: this task is F1 (N=1), and the brief gives those files to N=2.

## 2. Tasklist package

- Package: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/`
- Plan: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` (schema `workflow-plan/1.2`, 6 phases = groups G0-G5, 19 tasks; workflow quality gate passed and was re-run after the post-reflect edits)
- `source.md` (byte-exact snapshot of the spec at generation), `return-contract.yaml` (contract 1.1, `status: success`), `progress.md` (ledger header plus `PLAN:` pin, no task records)
- Execute with: `/sc:implement .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md`

## 3. Reflect status

- `reflect_status: partial`; report `.dev/reflect/pre-phase1RemovalSpe-20261029185357/REPORT.md`; contract `.dev/reflect/pre-phase1RemovalSpe-20261029185357/return-contract.yaml`.
- Why partial: the evidence-validator dropped 3 of 64 report citations (one wrong line number, two over-stated token claims; 0 of 114 sampled requirement rows dropped). Separately, `input_drift_detected: true`, because the parallel Phase 2 finalizer edited `phase-2-codegraph-install-spec.md` during the run. Its §2.12 and T0b checks, which Phase 1 relies on, are unchanged.
- Run: Tier 2. No labeled requirement IDs in the spec, so `coverage_degraded: parsed-sparse`. 340 quote-pinned requirement rows; union coverage 0.7088 by lexical match, and 96 of the 99 unmatched rows are cited by row or section. Calibrated confidence 0.79. Two heterogeneous reviewers (sonnet analyzer, glm-5.3 qa; opus excluded because it wrote the plan), each blind-calibrated (0.75, 0.77). `sc:adversarial` merge at convergence 0.947.
- Verdict: refactor. 12 confirmed plan defects (3 IMPORTANT, 9 MINOR). **All 12 were fixed by editing the generated plan** (and mirrored in the spec's new §8.1). IMPORTANT ones:
  - Task 4 would have deleted a helper that Task 5's still-present uninstall path and the tavily tests need.
  - Task 18's sandbox searches skipped hidden folders and matched allowlisted installed text and backups.
  - Task 18 omitted `CLAUDE_CONFIG_DIR`, so a run could reach the real user config.

  MINOR ones:
  - Red acceptance at Tasks 7/12 (`get_current_config`), Task 8 (`real.yaml:721`), Task 10 (`mcp-servers:` lines) and Task 13 (reflect ref lines).
  - Missing `mkdir -p` lines.
  - Task 12 ran no reflect tests.
  - Ledger and handoff files were never staged.
  - Two scope limits were missing.
  - The DoD-3 sandbox did not seed stale core files.

## 4. Required tasklist properties (task F1 item 3)

| Property | Where in the plan |
|---|---|
| Test command and commit point after every task group | Last task of each group runs pytest and commits: Task 1 (G0 baseline runs), Task 6 (G1), Task 9 (G2), Task 15 (G3), Task 17 (G4 test gate added), Task 19 (G5 test gate added). Every task has its own commit |
| Issue #323 progress comment at each commit point | Same six tasks post the group comment; the exact `gh repo view` check and `gh issue comment 323 --repo IronbellyOrg/IronClaude` command are in Constraints; G0 comment added (spec §9 amended to match) |
| Decision rules | Constraints: simple = self; mid = option files, then an agent runs `/sc:adversarial --compare <option files> --depth quick`; complex = `/sc:adversarial --compare <option files>`; each logged in `$PKG/decisions.md` |
| Final full verification task | Task 18: sync and lint, full suite compared with the baseline, residual search, three sandbox runs (fresh, existing, no CLI), evidence in `$PKG/artifacts/final/summary.md` |

## Decisions

| # | Decision | Options considered | Method | Rationale |
|---|---|---|---|---|
| 1 | Apply X-4 exactly as Phase 2 T0b lists; Tier K message becomes "kept until codegraph is ready"; hint name `serena-local` | leave Phase 1 text and let Phase 2 T3b rewrite later | self | Phase 2 §2.12 is an adversarial-full decision; Phase 2 T0b names the rows and the check; the live entry has `"env":{}` (read-only `jq`) |
| 2 | X-12 split, but `reflect-reviewer` and `reuse-auditor` go to T11a (not T11c), and `sc-pm-protocol` to T10a (not T10b) | review's exact split | self (forced) | Rule G5 ties a roster to its driving skill body (reflect SKILL.md drives both agents; D4/D5 test `reflect-reviewer`); `commands/pm.md:52` loads `sc:pm-protocol` |
| 3 | X-15: keep the CI step, rewrite only its comments | delete in Phase 1 and restore in Phase 2 | self | Phases 1+2 merge as one unit; Phase 2 F12 needs the step |
| 4 | X-24: keep `docs/memory/pm_context.md:77` unchanged | give it to T12 and un-allowlist | self | The line is design history |
| 5 | Cross-phase findings: only the Phase 1 hunk (X-5 pointer); no edit to Phase 2/3 specs or handoff files | edit them too | self (brief) | Ownership rule; handoff files belong to N=2 |
| 6 | Add a G0 issue comment so every group commit point has one | keep G1-G5 only | self | Task F1 item 3 says "at each commit point" |
| 7 | Snapshot `source.md` with `cp` and verify with `cmp` instead of re-typing 130 KB through the Write tool | Write tool as the skill text says | self (deviation, recorded) | The requirement is byte-exactness; `cmp` proves it |
| 8 | Reflect output at its default `.dev/reflect/pre-phase1RemovalSpe-20261029185357/` | put it inside the package | self | Workflow Wave 4 says "defaults for every other flag" |
| 9 | Reflect ran without Serena (fail-open to Read/Grep, recorded as degraded) | use Serena tools | self (run rule) | README: do not depend on tools being removed |
| 10 | Edit the generated plan from the reflect findings after the workflow skill finished; add "task text wins over `./source.md`" to Constraints; mirror the corrections in spec §8.1; keep `source.md` byte-exact | rerun `/sc:workflow`; leave the plan unchanged (workflow's own "Will Not") | self | The brief says to fix plan defects by editing the plan, not by rerunning; the workflow rule binds the skill's run, which had finished |
| 11 | Accept reflect `partial` for input drift without a rerun | rerun reflect | self | The only changed input is F2's Phase 2 spec; the text Phase 1 depends on is unchanged |
| 12 | Seed `progress.md` with the exact ledger header and `PLAN:` pin `/sc:implement` writes at creation | leave it absent (workflow says implement creates it) | self | Coordinator acceptance requires it; `sc-implement-protocol/refs/managed-workspace.md` re-pins a changed hash before the first task, so a header-only ledger resumes at T1 |
| 13 | Removed the empty `/tmp/x` folder a reflect subagent created | leave it | self | My run created it; `rmdir` only removes an empty folder |

No decision needed an adversarial run: each was forced by a cited rule or source line, or had one obvious option. So no `.dev/codegraph-migration/decisions/F1-*` folder was created.
