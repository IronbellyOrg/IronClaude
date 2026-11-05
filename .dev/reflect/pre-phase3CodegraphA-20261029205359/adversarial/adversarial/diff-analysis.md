# Diff Analysis: Tier-2 reviewer-card comparison (sc:reflect UC-1, Phase 3 codegraph plan)

## Metadata
- Generated: 2026-10-29T21:12:00Z
- Variants compared: 2
  - Variant 1: `reviewer-1-card.yaml` (sonnet, analyzer persona; 15 findings; calibrator C=0.73, all 15 confirmed)
  - Variant 2: `reviewer-2-card.yaml` (haiku alias glm-5.3, qa persona; 6 findings + 1 advisory note; calibrator C=0.67, 4 confirmed, 2 unverifiable)
- Target under review: plan `TASK-WF-phase3CodegraphA-20261029-204913.md` (cited `plan:N`) against `source.md` (cited `source.md:N`)
- Focus: correctness, coverage, deviation-classification
- Input warning: both inputs are YAML, not Markdown; copied as `variant-N-original.md` unchanged except trailing whitespace.
- Output-path note: `--output` already ends in `adversarial/`, so the step artifacts are written directly into it (no third `adversarial/` level).
- Total differences found: 31
- Categories: structural (3), content (6), contradictions (3), unique (16), shared assumptions (3 promoted)

## Orchestrator pre-verification (read from repo before the debate)

| Fact | Evidence | Bears on |
|---|---|---|
| `/sc:pr-submit` accepts `--body`, not `--body-file`; the skill runs `gh pr create ... --body "..."` | `src/superclaude/commands/pr-submit.md:8,26,54`; `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:189`; `--body-file` only appears in `scripts/reply-resolve-thread.sh` | R1-01 |
| `test_other_commands_membership_and_live_references` asserts `members == _OTHER_COMMANDS` (9 fixed names, no `sc:graph`/`sc:impact`) | `tests/core/test_how_we_work_routing_table.py:27-37,294` | R1-03, X-001 |
| `.dev/codegraph-migration/` has zero tracked files; the plan package is also untracked | `git ls-files .dev/codegraph-migration` prints nothing; session git status `?? .dev/codegraph-migration/`, `?? .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/` | R1-06 |
| `commands/reflect.md:6` has `mcp-servers:`; spec row 29 anchors reflect.md `:144,158,166-172` only | `src/superclaude/commands/reflect.md:6`; `source.md:118` | R2-02 |
| `commands/troubleshoot.md:6` `mcp-servers:` is inside row 13's anchor list | `src/superclaude/commands/troubleshoot.md:6`; `source.md:102` | R2-02 (calibrator) |
| `commands/task.md:6` `mcp-servers: [context7, serena, playwright, morphllm]`; row 40 strips `serena` in Phase 1 and adds `codegraph` only to six other commands | `src/superclaude/commands/task.md:6`; `source.md:129` | R1-09 |
| `test_routing_refresh.py` asserts `shipped == active` at `:639-640` | `tests/recommend/test_routing_refresh.py:637-640` | context for Task 8/9 |
| `make sync-dev` copies skills, agents (and commands/hooks/templates), not core docs | `Makefile` sync-dev target; `source.md:250` | R1-07 |

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|---|---|---|---|
| S-001 | Finding layout | 15 one-line flow-map findings, no summary line | 6 block findings, top-level `verdict:` line and an `advisory_notes:` list | Low |
| S-002 | Deviation-class vocabulary | Uses all four classes (regression 2, drift 7, necessary 4, authorized 2) | Uses `drift` for all 6 | Medium |
| S-003 | Non-actionable findings | None; every finding carries a plan fix | 2 of 6 findings carry "No plan change" / "None" (R2-03, R2-04) | Low |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity |
|---|---|---|---|---|
| C-001 | Task 14 final commit point (`plan:223-224`) | R1-08: keep the commit, but posting comment G and logging its URL after it breaks "no tracked change afterwards"; post G before the commit | R2-05: the commit + push contradicts spec T12 "no new commit unless the monitor pushes fixes" (`source.md:288`); align or log | Medium |
| C-002 | Baseline (b) paths vs Task 13 union (`plan:37`, `:210`) | R1-04: important drift; one shared test-path set; copy the pipeline text into Constraints | Advisory note only: strict superset, spec-authored, no finding | Medium |
| C-003 | Row 40 / Task 7 metadata (`plan:122`) | R1-09: `commands/task.md` "(metadata only)" has no defined change | R2-02: Task 7 names troubleshoot and reflect for row 40 but lacks those files; Tasks 6 and 10 omit row 40 | Medium |
| C-004 | Commit-message and commit-list text | R1-14: Task 2's "only" list omits `.dev/tasks` | R2-06: Task 13 message differs from spec T11; (calibrator) Task 8 message differs from spec T6 | Low |
| C-005 | Overall verdict | Two Regressions (R1-01, R1-03); many important drifts | "No CRITICAL, no Regression"; coverage holds at requirement-union level | High |
| C-006 | Coverage method | Executability of commands, flags and tests | Matrix attribution and requirement-span coverage (R2-03, R2-04) | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Whether the plan carries a Regression | R1-03: Task 12 adds two rows to the `other-commands` table and no task edits `_OTHER_COMMANDS`, so `tests/core/test_how_we_work_routing_table.py:294` fails | `verdict:` "No CRITICAL, no Regression" | High |
| X-002 | Should Task 14 make a final commit | Implicitly yes (fix reorders comment G before the commit) | No new commit unless the monitor pushes fixes, per spec | Medium |
| X-003 | Severity of the baseline/union mismatch | important, needs a plan fix | advisory, spec-authored, no plan finding | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | R1-01 `/sc:pr-submit` has no `--body-file` | High |
| U-002 | 1 | R1-02 `./artifacts/pr-body.md` is the never-staged project-root folder | High |
| U-003 | 1 | R1-03 `_OTHER_COMMANDS` membership test breaks | High |
| U-004 | 1 | R1-05 "any installer" vs Task 3's `install_core.py` edit | Medium |
| U-005 | 1 | R1-06 untracked plan package and inputs absent from an `origin/master` worktree | High |
| U-006 | 1 | R1-07 live smoke has no route to a session that sees the new commands | Medium |
| U-007 | 1 | R1-10 STRICT step 7 edited by Task 7 and Task 12 with no precedence | Medium |
| U-008 | 1 | R1-11 `git diff --name-only HEAD` cannot see a committed change | Low |
| U-009 | 1 | R1-12 sentinel scan must exclude the plugin copy; `codegraph sync` prose outside "Never" | Medium |
| U-010 | 1 | R1-13 Task 9 omits the lookup line and the dual-surface lookup test | Low |
| U-011 | 1 | R1-15 non-runnable `<baseline (a)>` placeholder | Low |
| U-012 | 1 (calibration) | plan:37 drops `source.md:30` G3 continue rule (T1-T10 may proceed) | Medium |
| U-013 | 2 | R2-01 `graph:not_initialized` fallback message must name `/sc:graph init` | Medium |
| U-014 | 2 | R2-03 seven coverage-matrix mis-attributions; INF-017 wording | Low (matrix artifact, not plan) |
| U-015 | 2 | R2-04 requirement spans absent from the 119-row matrix but carried by the plan | Low (matrix artifact, not plan) |
| U-016 | 2 (calibration) | Task 8 commit message `manual init` vs spec `user-typed init` | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | Both cards judge "plan omits X" without reading `DES` (R1 self-audit: "DES and E-1..E-7 inputs not read"; R2 self-audit lists no DES read) | Plan text that builds a file "from `DES` §n" does not already carry the item | UNSTATED | Yes |
| A-002 | Both treat plan omissions as drift even where the plan says "Apply source §1.2 rows N-M" | The executor reads only the plan text, not the referenced `source.md` rows | UNSTATED | Yes |
| A-003 | Both count missing `mcp-servers:` edits as findings | `mcp-servers:` frontmatter has a consumer whose absence matters (spec says none: `source.md:63`) | UNSTATED | Yes |
| A-004 | Both | Phase 1 and Phase 2 land first and leave the text the spec assumes | STATED (`source.md:9-13`, `plan:20`) | No |

### Promoted shared-assumption points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Omissions inside "build from DES §n" tasks are real | R1-13, R2-02 (new commands' frontmatter) | Medium: such findings are unverifiable until DES is read | Open for debate |
| A-002 | Omissions carried by a "source §1.2 row N" reference are drift | R2-02, R2-01, U-012 | High: decides Drift vs no finding | Open for debate |
| A-003 | `mcp-servers:` gaps are consequential | R2-02 | Medium: decides important vs minor | Open for debate |

## Taxonomy tags (AD-5)

- L1 surface: S-001, S-003, C-004, C-006
- L2 structural: S-002, C-001, C-003, C-005, X-002, A-001, A-002, A-003
- L3 state mechanics: C-002, X-001, X-003 (test-membership invariant, baseline validation rule)

## Summary
- Total structural differences: 3
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 16
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-005, X-001, U-001, U-002, U-003, U-005
- Similarity check: differences far above 10% of comparable items; debate runs.
- Convergence denominator: S + C + X + A = 3 + 6 + 3 + 3 = 15
