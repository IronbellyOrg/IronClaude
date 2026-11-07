# UC-1 Coverage Analysis

- Mode: UC-1 (spec vs. tasklist), analysis only, no execution.
- Spec: `source.md` (one physical line).
- Tasklist: `TASK-WF-fixIssue412SVeri-20261106-215543.md` (Constraints lines 17-24, Task 1 lines 28-37, Task 2 lines 41-52).
- Governing reference: `~/.claude/skills/sc-reflect-protocol/refs/coverage-mapping.md`.
- Deterministic matcher results (containment ratios, `coverage_pct`, `coverage_pct_union`, `S_dev_density`) are NOT computed here. The orchestrator computes them from `inferred-requirements.json`.

## Extraction

### Pass 1 (regex, authoritative)

`ID_REGEX = \b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b` over `source.md`: **0 parsed IDs.**
Near-miss tokens that do not match the regex: `#412`, `Issue412`, `PR245`, `PR29074` (issue/PR references, not requirement IDs).
The plan also carries no regex IDs (tasks are labeled `Task 1`, `Task 2`, not `T-NNN`).

Consequences for the orchestrator (stated, not computed):
- `parsed_total_count = 0`, so parsed-only `coverage_pct` is `null` per the reference (stage 5).
- `inferred_count (21) > parsed_count (0)`, so the Step 1B.2b parse-density guard fires (`coverage_degraded: parsed-sparse`).
- Zero-ID fallback (`coverage_undefined`) does NOT apply, because Pass 2 emitted valid quote-pinned rows.

### Pass 2 (quote-pinned inference)

21 rows, all `source: inferred`, all cited `source.md:1`, each quote a contiguous verbatim substring of the single source line (at most 1 sentence each). Distinct constraints were split; tightly coupled negations were kept together so no constraint loses its "Do not" / "never" polarity (INF-010 keeps "forward --force" and "overwrite edited guides" in one row for that reason). No span-overlap drops apply (no parsed spans exist).

Full rows: `inferred-requirements.json`.

| ID | Requirement (short) |
|---|---|
| INF-001 | Scope: instruction-delivery gaps of #412, not Orca shell behavior |
| INF-002 | Globally loaded rule in core/CLAUDE.md + matching ccsession-tag README |
| INF-003 | ccsession-backed Claude sessions use Claude (CLI), never New Terminal |
| INF-004 | Programmatic creation: version-matched `agent launch` or `worktree create --agent` |
| INF-005 | Explicit terminal surface only when CLI required |
| INF-006 | `terminal create` reserved for shells |
| INF-007 | Preserve supervised worker-start/preamble rules and internal Agent-tool subagents |
| INF-008 | `install_user_setup(force=True)` requests safe refresh with existing guides |
| INF-009 | Nonforce setup still skips existing copies |
| INF-010 | Never forward `--force` to Orca; never overwrite edited guides |
| INF-011 | Show meaningful skipped/warning output; no false refresh-success claim |
| INF-012 | Minimal regression tests in the two named files with observed pre-fix failures |
| INF-013 | Tests cover force propagation, default skip, nonfatal absent/failing Orca |
| INF-014 | Canonical edits only, then `make sync-dev` and `make verify-sync` |
| INF-015 | Never stage `.claude` mirrors; stage `.dev/tasks` |
| INF-016 | No commit/push/PR, global install, other-repo edits |
| INF-017 | Issue #412 already holds PR245/PR29074 refs; not shell-causation proof |
| INF-018 | Failing transcript and historical New Terminal PR remain unverified; preserve boundary |
| INF-019 | Diagnosis partial; runtime cause UNDETERMINED |
| INF-020 | Execution authorized only after reading the checked plan |
| INF-021 | Two-phase bounded plan, no verification-only task |

## Matrix

Semantic coverage (analyst judgment) is reported separately from deterministic containment. The `Containment` column is intentionally left for the orchestrator. "Where" cites plan lines.

| ID | Semantic coverage | Where in plan | Containment (orchestrator) | Note |
|---|---|---|---|---|
| INF-001 | Covered | L19, L23, L32 | to compute | "No runtime Orca change is authorized" (L32) |
| INF-002 | Partial | L30, L35 | to compute | Both files named; nothing checks the rule is in a *globally loaded* part of core/CLAUDE.md (F-3) |
| INF-003 | Partial | L35, L37 | to compute | AC says "distinguish", source says "never" (F-1) |
| INF-004 | Covered | L35 | to compute | "version-matched" moved from the launch to the guide; acceptable reading |
| INF-005 | Covered | L35 | to compute | |
| INF-006 | Covered | L35 | to compute | |
| INF-007 | Covered | L22, L36, L37 | to compute | Tests check the boundaries |
| INF-008 | Covered | L45, L50 | to compute | |
| INF-009 | Covered | L45, L50 | to compute | |
| INF-010 | Partial | L23, L50 | to compute | `--force` covered; edited-guide protection asserted only against IronClaude, not against Orca's normal install (F-2) |
| INF-011 | Covered | L24, L45, L51 | to compute | Success-summary ban sits in Inputs/Constraints, not verbatim in an AC bullet |
| INF-012 | Covered | L30, L37, L45, L52 | to compute | |
| INF-013 | Covered | L45, L50, L51 | to compute | |
| INF-014 | Covered | L21, L47, L52 | to compute | |
| INF-015 | Partial | L21 | to compute | Constraint only; no task step or AC stages `.dev/tasks` (F-4) |
| INF-016 | Covered | L20 | to compute | |
| INF-017 | Covered | L19 | to compute | |
| INF-018 | Partial | L19, L52 | to compute | Neither unverified item is carried into the plan by name (F-5) |
| INF-019 | Covered | L19 | to compute | |
| INF-020 | Not in tasks (contextual) | none | to compute | Execution gate, not task content (F-6) |
| INF-021 | Covered (structural) | L26, L39 | to compute | Plan shape satisfies it; task text will not lexically contain it |

Semantic tally (analyst, not matcher): 15 Covered, 5 Partial, 1 Not-in-tasks (contextual). No requirement is wholly uncovered.

Expected containment weakness (qualitative only): INF-017, INF-019, INF-020, INF-021 are context/plan-shape rows whose wording the task items do not repeat; low containment for them would reflect wording, not a task gap.

## Findings

No blocking gap. Six minor gaps, ordered by impact.

**F-1 (Minor, highest priority) — "never New Terminal" softened to "distinguish".** Source INF-003 is a prohibition. Task 1 AC (L35) only requires the surfaces to "distinguish Claude (CLI) ... from New Terminal", and the test (L37) checks "the shell/CLI distinction". A doc that merely describes both options passes. Fix: AC and test should require an explicit prohibition of New Terminal for ccsession-backed Claude sessions.

**F-2 (Minor) — edited-guide protection depends on unverified Orca behavior.** Source INF-010 says do not overwrite edited guides. AC L50 only says contents "are not rewritten by IronClaude"; Constraint L24 says edited copies "may be skipped" by Orca. If Orca's normal (non-`--force`) install does overwrite edited guides, the forced refresh violates the requirement and no AC catches it. Fix: require recorded evidence from installed `orca-ide skills install --help` (already a Task 2 input, L45) that non-force install does not overwrite edited copies, or state the residual risk.

**F-3 (Minor) — "globally loaded" not verified.** INF-002 requires a globally loaded rule. No AC checks that the rule sits in content of `src/superclaude/core/CLAUDE.md` that is installed and always loaded (as opposed to a doc read only on demand). Fix: add to Task 1 AC that the guidance test asserts the rule is present in the file installed as `~/.claude/CLAUDE.md`.

**F-4 (Minor) — `.dev/tasks` staging has no step.** INF-015's "stage .dev/tasks" appears only as Constraint L21. Neither task's Outputs nor AC requires `git add .dev/tasks` or evidence of it. Fix: add a staging line to Task 2 Outputs/AC.

**F-5 (Minor) — unverified-evidence boundary only partly carried.** INF-018 names two unverified items (failing agent transcript, historical New Terminal semantic-change PR). The plan states causation is UNDETERMINED (L19) and claims no UI reproduction (L52), but never names these two items, so an executor could cite them as known. Fix: name them in Constraints as unverified.

**F-6 (Minor, informational) — execution authorization not recorded.** INF-020 gates execution on the user reading the checked plan. The plan does not record it. This is executor gating, not task content; listed so the orchestrator does not count it as a task gap.

Other observations (not gaps):
- Plan additions beyond source, judged reasonable and in scope: preserve the Settings > Agents > Claude > Command `ccsession-orca` prerequisite (L30, L36); preserve executable identification, deadline and three-skill list (L45); extra regression suites `tests/unit/test_cli_install.py` and `tests/core/test_claude_md_routing_block.py` (L52).
- Task 1 edits a skill README but `make sync-dev` runs only in Task 2 (L47). If Task 2 stops early, `.claude` mirrors drift. Low risk; Task 2 depends on Task 1.
- Default-skip and nonfatal-Orca tests describe existing behavior, so they cannot "fail before the fix"; AC L52 correctly limits the red/green requirement to the new refresh checks.

## Self-Audit

- Every quote in `inferred-requirements.json` is a contiguous verbatim substring of `source.md` line 1, checked against the Read output in this session. All quotes are 1 sentence or a sentence fragment (limit is 2).
- Every clause of the source line maps to at least one INF row; no clause dropped, from the opening scope sentence through "no verification-only task".
- Pass 1 count of 0 was checked against the regex: no `R-`, `REQ-`, `SPEC-` or `T-` followed by digits appears in the source or plan.
- No matcher numbers were invented. The containment column, `coverage_pct_union` and `S_dev_density` are left to the orchestrator.
- Bias check: the task said to assume errors exist. Five Partial findings were raised; none was judged blocking because each requirement has at least a constraint-level or AC-level anchor in the plan. F-1 is the strongest candidate for promotion to blocking if prohibition-vs-description is treated as a correctness issue.
- Limits: no code, Orca help output or installed guide was read; F-2 and F-3 are risks inferred from plan wording, not verified defects.
- Files written: only this file and `inferred-requirements.json`, both under the requested `artifacts/` directory. No Bash, Git, GitHub or Orca action was taken.
