---
card_tier: 1
mode: pre
claim_class: static_defect
evidence_class: source_static
verdict_direction: AFFIRM
self_reported_confidence: 0.80
---

# Tier 1 reflection card: P1 static plan (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md` (the inline brief; the driving document it points to is `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`)
- Tasklist: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (below: `plan`)
- Coverage: `artifacts/coverage-matrix.yaml` (parsed 0, inferred 14, coverage_pct_union 0.50, parsed-sparse). Excerpts: `artifacts/grounding-hunks.md`.
- Findings: 0 blocking, 5 should-fix, 2 minor (7 total).

Severity key: **blocking** = the executor would halt, breach a quotable Constraint, or the plan misses a required deliverable; **should-fix** = a correct run can produce a false FAIL, an unverifiable acceptance criterion, or the executor has to guess; **minor** = clarity.

## Analyzer: root cause and deviation

### F-001: The Task 15 path-list criterion compares against a `git status` that can hold unrelated paths
- Severity: should-fix
- Claim: The last Task 15 criterion says the report's repo-path list "equals the output of `git status --short` for the working tree, ignoring paths under `.dev/tasks/` and the `.claude/` folder". The working tree can also hold other uncommitted planning paths (for example `.dev/reflect/` output and the `.dev/orca-command-refactor/decisions/APPROVED.md` edit, if the coordinator has not committed them when the executor runs). The equality then fails although every task did its job.
- Evidence:
  - `plan:289` "The repo-path list in the report equals the output of `git status --short` for the working tree, ignoring paths under `.dev/tasks/` and the `.claude/` folder."
  - `source.md:11` "Do not execute the plan: no /sc:implement, no commit, no push, no superclaude install, no live Orca run."
- Tag: Grounded
- Fix: Restrict the comparison to the paths the plan can change: `git status --short -- src tests plugins`.

### F-002: Brainstorm's nested-call behaviour goes beyond the spec's P1 row
- Severity: should-fix
- Claim: The spec's P1 brainstorm row names only "automatic research enrichment ... is off". Task 3 also moves brainstorm's adversarial output under `<report-dir>/nested/adversarial-<n>/` and passes `--unattended` to the `/sc:analyze` enrichment, which follows the spec's nested propagation rule (section 2.1) but changes where artifacts land under `--unattended`. The plan records this as decision D-P1-4, so it is disclosed, but it is not in the row the brief points at, and a reviewer reading only the row would call it scope creep.
- Evidence:
  - `spec:221` "adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow (ready, no gate change) and analyze, build, business-panel, design, document, explain, index, test (no gate)"
  - `spec:62` "under `--unattended`, a command that invokes another `/sc:` command or protocol skill ... passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/`"
  - `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:273` "--output <output>/adversarial/"
  - `plan:43` "D-P1-4: the nested propagation rule (spec section 2.1) is applied to brainstorm"
- Tag: Grounded
- Fix: Keep D-P1-4 and report it as an owner-visible decision; no plan change.

### F-003: The `command` key collides with the existing short-name key in graph and impact
- Severity: should-fix
- Claim: The spec's worker field `command` is "the exact command line"; graph's and impact's own contracts already define `command` as the short name (`graph`, `impact`). The plan keeps the existing value (D-P1-1), so the 7.2 step 4 check (non-empty) passes, but the worker contract no longer carries the exact command line for those two commands.
- Evidence:
  - `spec:72` "`command` (the exact command line)"
  - `src/superclaude/skills/sc-graph-protocol/SKILL.md:90` "| `command` | string | `graph` |"
  - `src/superclaude/skills/sc-impact-protocol/SKILL.md:74` "| `command` | string | `impact` |"
  - `plan:43` "D-P1-1: graph and impact already write a `command` key holding the short name"
- Tag: Grounded
- Fix: Keep D-P1-1 and report the collision to the coordinator for a spec decision.

### F-004: `--report-dir` next to a command's own directory flag is the plan's reading, not stated outright by the spec
- Severity: should-fix
- Claim: The section skeleton says each section accepts `--report-dir` or the command's own directory flag, and the new tests require the token `--report-dir` in all sixteen sections. The spec's wording ("for a command without such a flag, or a brief that does not pass it") supports this reading but can also be read as "only commands without their own flag take `--report-dir`".
- Evidence:
  - `spec:58` "the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it)"
  - `plan:24` "exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; if the command has none, `--report-dir` only"
- Tag: [INFERRED] (reading of the spec sentence)
- Fix: State it as UNVERIFIED in the static report (the plan's Task 15 already lists it).

### F-005: Deterministic containment leaves seven brief requirements unmapped to a task
- Severity: should-fix
- Claim: The containment rule maps 7 of 14 inferred rows to a task; the other 7 (INF-001, 002, 003, 006, 009, 010, 014) are covered by Constraints bullets rather than by one task item, so the matcher reports `none` although the plan covers them.
- Evidence:
  - `artifacts/coverage-matrix.yaml` rows INF-001, INF-002, INF-003, INF-006, INF-009, INF-010, INF-014 with `match_method: none`
  - `plan:20` "The live checks AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7 and AC-1.8 and the P1 phase report belong to the P1 live plan"
  - `plan:21` "No task in this plan commits, pushes, installs into `~/.claude`, starts an Orca worker, runs an Orca command or asks the owner a question."
- Tag: Grounded
- Fix: None to the plan; the report states that these rows are Constraint-level.

## QA: coverage and acceptance

### F-006: Business-panel frontmatter move is judged by a deletion count the diff algorithm can exceed
- Severity: minor
- Claim: Task 11 accepts "at most 4 deleted lines" for `business-panel.md`. Moving the heading and the two fence lines deletes 3 lines; a diff may count the unchanged `---` lines as moved. The bound has little margin.
- Evidence:
  - `plan:223` "`git diff --numstat` shows at most 4 deleted lines"
  - `src/superclaude/commands/business-panel.md:1-11` (heading, blank line, yaml fence, `---` pair, key lines, closing fence)
- Tag: [INFERRED]
- Fix: None required; the criterion also checks the keys and values are unchanged.

### F-007: Task 10 and Task 11 each bundle three commands
- Severity: minor
- Claim: Each bundled task names every file, so the "no bulk task" rule holds, but a per-task reviewer has more to hold in view.
- Evidence:
  - `plan:195` "## Task 10: Convert `/sc:analyze`, `/sc:build` and `/sc:design`"
  - `plan:208` "## Task 11: Convert `/sc:test`, `/sc:explain` and `/sc:business-panel`"
- Tag: Grounded
- Fix: None.

## Recommendations

- Apply the F-001 fix before the first `/sc:implement` start (any later edit halts the run).
- Report D-P1-1, D-P1-4 and the F-004 reading to the coordinator.
