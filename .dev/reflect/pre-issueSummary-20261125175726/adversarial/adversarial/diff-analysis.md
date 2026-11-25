# Diff Analysis: Reviewer Card Comparison (UC-1 pre-execution review of TASK-WF-issueSummary-20261125-175231)

## Metadata
- Generated: 2026-11-25T18:26:00Z
- Variants compared: 2
  - Variant 1 (V1): reviewer 1, analyzer lens, model class haiku (alias claude-gw-tier2; its self-report names an OpenAI model). `variant-1-original.md`, 4 rows (all graded "Blocking (...)" in the text, Severity column MEDIUM), verdict FAIL, calibrated C 0.76.
  - Variant 2 (V2): reviewer 2, qa lens, model class opus (alias claude-gw-tier1a). `variant-2-original.md`, 13 rows (3 Blocking, 3 Medium, 7 Note), verdict FAIL, calibrated C 0.77.
- Context read: plan `TASK-WF-issueSummary-20261125-175231.md` (all 103 lines, referred to below as `plan:<line>`); spec `source.md` (38 lines, `source.md:<line>`); the launcher, wrapper, README, Makefile, `install_ccsession.py` and the README-pinning test (all re-read by the orchestrator this run).
- Focus areas: correctness, coverage, deviation-classification (including each finding's grade).
- Total differences found: 36 (6 structural, 5 content, 3 contradictions, 13 unique contributions, and 4 promoted shared assumptions). Convergence denominator = S + C + X + A = 6 + 5 + 3 + 4 = 18.
- Counting rule: a C row compares how both cards treat one plan subject; a U row lists a finding raised by one card only.
- Grading rule applied to judge grade contradictions (not to re-grade): Blocking only for Decision, Missing or Safety; a plan check that cannot work as written is Blocking (Decision), or Blocking (Missing) when an omitted step is the cause; otherwise Medium or Note. The Severity column (HIGH/MEDIUM/LOW) is a label, not the grade.
- Taxonomy levels: L1 surface, L2 structural, L3 state mechanics (state, guard, boundary, invariant, concurrency, validation rule).

## Structural Differences

| # | Area | Variant 1 (analyzer, haiku class) | Variant 2 (qa, opus class) | Level | Severity |
|---|------|-----------------------------------|----------------------------|-------|----------|
| S-001 | Row count and scope | 4 rows, each one defect, all on tasks 2, 3, 4 and 6 and the spec gate. Dismisses the first-pass card's F4 (`_label_run` wording) and F6 (live-action ownership) in Notes. | 13 rows: 3 Blocking, 3 Medium, 7 Note; rows 8-10 audit the coverage matrix and card arithmetic rather than the plan. | L2 | Medium |
| S-002 | Grade scheme and its consistency | Every row's text says "Blocking (...)" but every Severity cell says MEDIUM, so the label never separates a Blocking row from a Medium one (calibrator: classification clarity 0.55, "Blocking vs MEDIUM" inconsistent). | Text grade and label agree: HIGH on the three Blocking rows (1, 2, 3), MEDIUM on rows 4-6, LOW on the Notes (calibrator: 0.72). | L2 | High |
| S-003 | Adherence-summary method | 37 spec units (INF-005 to INF-041), 34 adherent, 3 "incompletely planned" (INF-009, INF-023, INF-041). INF-009 has no row of its own. | 42 units (41 rows plus SPEC:25), 37 adherent, 5 not (3 Blocking units, 2 Medium); effort-estimate rows counted adherent. | L1 | Low |
| S-004 | Evidence form | Absolute paths with line ranges, 17 citations checked, 0 failed. | `PLAN`/`SPEC` keys plus absolute paths, 32 checked, 4 caveats (rows 8-10 cite inputs the calibrator did not have; one row's range is an env-filter list). | L1 | Low |
| S-005 | Stated unknowns | Self-confidence 0.94; lists as unverified: installed executable contents, Orca configuration, live access. | Self-confidence 0.85; "Not checked": whether child processes keep the switch, the real Claude Code switch, 13 other ccsession test files, tracked `.claude/` files. | L1 | Low |
| S-006 | Reviewer identity metadata | Header says haiku class; footer self-report says "ChatGPT (OpenAI)". | Header says opus class; self-report `claude-gw-tier1a[1m]`, consistent. | L1 | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Level | Severity |
|---|-------|--------------------|--------------------|-------|----------|
| C-001 | Broader regression and lint gates absent (INF-041, `source.md:32`; `plan:74-77, 89`) | Row 4, Blocking (Missing), label MEDIUM: Task 4 runs only the three files; no task owns the broader pytest gate; cites `Makefile:12-15`. Names only pytest. | Row 1, Blocking (Missing), label HIGH: no task runs `make test` or `make lint`; 16 test files mention ccsession, 3 are run; names `tests/core/test_orca_session_launch_guidance.py` which pins the README "### Orca session launches" text while Task 5 edits that section. See U-001. | L3 | High |
| C-002 | Changed launcher never reaches the live route (`plan:98, 101`) | Row 1, Blocking (Missing), label MEDIUM: Task 5 syncs only the checkout mirror, the installed wrapper resolves its adjacent installed launcher (`ccsession-orca:44-54`); asks for verification of the executable plus either a named checkout launcher or an authorised refresh. | Row 2, Blocking (Missing), label HIGH: same cause, adds that Constraint `plan:22` ("`wire_ccsession` copies the launcher unchanged") is wrong and that the executor may run a global install from an unmerged branch. See U-002. | L2 | High |
| C-003 | Task 2 header line placed where `--help` never prints (`plan:46, 51`; `ccsession:143, 2271`) | Row 2, Blocking (Decision): the promised scope notice cannot appear in `--help`; checking only the exit code cannot establish it. | Row 4, Medium: stated reason is false and the check cannot detect it, but nothing the spec requires depends on the line. | L2 | Medium |
| C-004 | Raw-resume launches in Task 3's matrix (`source.md:21`; `tests/unit/test_ccsession_tag.py:1465-1472`) | Row 3, Blocking (Missing): no raw-resume case; the 20-case check can pass without proving the switch on raw-resume arguments. | Row 13, Note: the untagged cases use `-p x` only, but raw `--resume` and `-p` run the same two exec lines (`ccsession:2447-2451`), so line coverage is unchanged. | L2 | Medium |
| C-005 | Task 6 live acceptance (`plan:98-103`) | Row 1 only; Notes call the live-action ownership concern an execution clarification and accept "not run, partial" for message checks. | Row 3, Blocking (Decision): the environment check passes for any ccsession-started process "in an existing terminal", while the spec asks for the coordinator's own process; only the message check has a "not run" fallback. | L3 | High |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Grade of the Task 2 header-line defect (C-003) | Blocking (Decision) | Medium | Medium |
| X-002 | Grade of the missing raw-resume case (C-004) | Blocking (Missing) | Note | Medium |
| X-003 | Severity label of the same deploy-path defect (C-002) | MEDIUM | HIGH | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V2 | Full-suite test `tests/core/test_orca_session_launch_guidance.py:15-16, 40-62` pins the README Orca section (required phrases, and the paragraph after `commands' internal Agent-tool subagents.` must start "Every Orca worktree gets an agent" and match `core/CLAUDE.md`); Task 5 adds a sentence to that section; only the full suite would fail. | High |
| U-002 | V2 | Constraint `plan:22` says `wire_ccsession` "copies the launcher unchanged"; it only creates links and copies two small files (`install_ccsession.py:13-16, 56-57, 61-71`). | Medium |
| U-003 | V2 | Task 3 acceptance `plan:66` ("only the one named variable is captured") is false for the prescribed `_orca_env` fake, which already records `env_names: sorted(os.environ)` and other values (`tests/unit/test_ccsession_tag.py:1833-1839`). | Medium |
| U-004 | V2 | Session-wide effect is understated: any child of a protected session, including a nested `claude`, inherits the switch (`ccsession:2406-2408, 2412-2415` only by analogy); "bare `claude` not covered" is wrong inside a protected session. Not checked against Claude Code itself. | Medium |
| U-005 | V2 | `git status --short` shows no ignored `.claude/` path whatever sync does (`.gitignore:127-128`); the check cannot fail. | Low |
| U-006 | V2 | Task 3 says "one test" and expects "two wrapper cases"; `ccsession-orca` takes the named exec (261) unless `-p`, resume, `CCSESSION_AUTOSTART=0` or a carried name, so a test meant for line 263 may run 261 (`ccsession-orca:227-236, 259-263`). | Low |
| U-007 | V2 | Route trace omits the tab-reopen execs at `ccsession-orca:186, 189`; both still pass through ccsession. | Low |
| U-008 | V2 | Matrix rows INF-002, 003, 004, 006, 026, 033 name the wrong owning task although a real owner exists. | Low |
| U-009 | V2 | `SPEC:25` ("capture only the named non-secret switch") has no matrix row. | Low |
| U-010 | V2 | First-pass card's arithmetic is off (22 unmatched rows split 15 + 6 + 1). | Low |
| U-011 | V1 | `source.md` relative links (`analysis/analyze-ccsession.md`, `accuracy-check.md`) do not resolve inside the package; the original is under `.dev/issues/765/analysis/`. | Low |
| U-012 | V1 | Counts INF-009 (fresh and resumed verification) as incompletely planned in its summary but writes no row for it. | Low |
| U-013 | V1 | Explicitly dismisses the first-pass card's `_label_run` wording (F4) and live-action ownership (F6) as non-defects, with reasons. | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both cards read INF-041 as a missing gate (C-001) | "The required broader regression/lint/format gates" means the whole pytest suite (`make test`) and the project lint gate (`make lint`); the spec names no command. | UNSTATED | Yes |
| A-002 | Both grade the missing gate Blocking (Missing) | A "Run ..." sentence in the spec's cheatsheet table (`source.md:32`) is a requirement the plan must own, not a description of the issue. | UNSTATED | Yes |
| A-003 | Both ask the plan to settle how the changed launcher reaches the live route (C-002) | Running `superclaude install` or `./update.sh` for the live proof is allowed for the implementing session; V2 itself warns it changes every ccsession launch on the host. | UNSTATED | Yes |
| A-004 | Both audit each task as a whole plan reader | The executor reviews each task alone with only the Constraints (template rule), so a cross-task fact (where the changed launcher lives) must be restated in the task that needs it. | UNSTATED | Yes |
| A-005 | Both accept the switch's described effect | Claude Code honours `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` as the spec describes; V2 lists it as not checked. | STATED (V2 Notes) | No |
| A-006 | Both read the brief's plan and hunks | The plan text they read is the plan on disk. | STATED (both read it) | No |

## Summary
- Total structural differences: 6
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 13
- Total shared assumptions surfaced: 6 (UNSTATED: 4, STATED: 2, CONTRADICTED: 0); 4 promoted to [SHARED-ASSUMPTION] diff points A-001 to A-004
- Highest-severity items: S-002, C-001, C-002, C-005, U-001
- Taxonomy levels present: L1 (S-003 to S-006, X-003), L2 (S-001, S-002, C-002, C-003, C-004, X-001, X-002, A-001, A-002), L3 (C-001, C-005, A-003, A-004)
