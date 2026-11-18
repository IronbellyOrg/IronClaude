## Implementation-Plan-Concreteness QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`
**Lens:** implementation-plan-concreteness (adapted to report-only task: inputs for a later plan), Section 8.2 and Section 7.1; domain lens 3 of 3
**Instance and range:** instance a, lines 1 to 2114 (partition file `qa/report-size-and-partition.md`, `MODE: SPLIT`, K = 2115). Section 7.1 (line 3650) and Section 8.2 (line 4369) lie OUTSIDE this range (instance b owns them; located by Grep only, not graded here). Checked in range: Section 3.1 (T-1 to T-6, target shape), 3.3 (SC-01 to SC-33, gates), 3.4 (K-1 to K-9, constraints), 3.5, and the Section 4 / 5 text for integration points.
**Date:** 2026-11-14
**Grading:** owner override (qa/grading-override.md) applied
Status: Complete

### Findings

| # | Severity | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| 1 | IMPORTANT label (minor under grading override) | 3.3 SC-32 (line 1185; same baseline repeated at lines 793, 3426, 4434 in G10) | The no-regression gate for the installed-path rule names the command `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and the baseline "148 lines, 56 files". That command, run as written at HEAD, does not return that baseline. The baseline holds only when the search is limited to `*.md`. A later plan that runs the stated command sees 168 lines in 70 files and cannot tell whether it regressed. Downstream use: the gate input for a later plan; no recommendation, value-inventory destination or conflict outcome rests on the 148 figure (it is stated as "a fact for the plan, not a conflict", line 3426). (minor under grading override) | Bash at HEAD: the stated command gives 168 lines / 70 files (matches by extension: 56 md, 6 sh, 4 pyc, 2 yaml, 1 py, 1 json). The same command with `--include='*.md'` gives 148 lines / 56 files (also with `templates` added). G10 (line 4434) says the count is over `**/*.md` but its command shows no `--include`. | Add `--include='*.md'` to the command in SC-32 and G10 (or state the baseline as 168 / 70 with the file types). |
| 2 | IMPORTANT label (minor under grading override) | 3.4 K-3 (line 1194) | The constraint cites the tests that pin the workflow interface, but two citations do not let a later plan run them as written. (a) `test_workflow_vs_task_builder_companion.py:574-599` has no directory; the file is `tests/cli/eval/test_workflow_vs_task_builder_companion.py` (not under `tests/commands/` with the other cited file). (b) `tests/tasklist/test_tasklist_cli.py:573-580` pins the Stage 10.5 fence ordering ("BEFORE Stage 10.5", P2 loop-back), not `reflect_status` or `reflect_report_path`; that file has no `reflect_status` hit. The substance (the interface is pinned by tests) is true: `test_workflow_command.py:243-261` pins the `nested/reflect-` directory under `--unattended`, and the companion test at :574-599 pins `reflect_status` and `reflect_report_path`. (minor under grading override) | Bash: `find tests -name test_workflow_vs_task_builder_companion.py` returns `tests/cli/eval/...`; `grep -n reflect_status tests/tasklist/test_tasklist_cli.py` returns nothing; `sed -n 573,580p` shows the Stage 10.5 fence assertions. | Give the companion test its full path; cite the tasklist test as the Stage 10.5 ordering pin, or drop it from the `reflect_status` list. |
| 3 | MINOR | 3.3 SC-24 (line 1177) | `reflect_shadow_exit.py:313` is cited without its directory; the file is `scripts/reflect_shadow_exit.py` (the regexes at :59 and `panel_lint.py:188` and the `(s_rate or 0.0) > (l_rate or 0.0)` line at :313 are correct). (minor under grading override) | Bash: `find . -name reflect_shadow_exit.py` returns `./scripts/reflect_shadow_exit.py`; `sed -n 59p;313p` and `panel_lint.py:188` match the claims. | Write `scripts/reflect_shadow_exit.py:313`. |
| 4 | MINOR | 3.3 SC-30, SC-31, SC-33 (lines 1183, 1184, 1186) | The "How it is checked" cell of three criteria names a research matrix, a research section or a row list instead of a command, test path or rule a later plan runs (SC-30: "R16 Part 4 element matrix"; SC-31: "leak check scope `extract.py:135-141`; memory flag absent"; SC-33: the list of G-ids). The other 30 criteria name a test, a probe, a Grep, a `make` target or a file:line. Section 3 states it is the target, not a plan (line 1121), so the runnable form belongs in 8.2, which is outside this range. (minor under grading override) | Read of lines 1152-1186. | In 8.2 give each of the three a runnable form (a test path or a Grep). Instance b should confirm this for 8.2. |
| 5 | MINOR | 3.4 (lines 1188-1200) | Checklist item d asks that compatibility, migration and rollback constraints be stated where they apply. Section 3.4 covers contract 1.8.0 byte-identity (K-1), verdict matrix (K-2), workflow interface (K-3), dual-surface and repository rules (K-4, K-6), plugin mirror (K-9). It has no row for shadow mode (INV-L at line 3167 states "shadow mode changes no verdict; the legacy rotation and the Wave 4 debate stay authoritative until a later stage", in instance b's range) and no back-out or rollback constraint at all: a case-insensitive Grep of the whole report for `rollback`, `roll back`, `revert`, `back out` returns no hit. The report is report-only and the recommendation does not depend on it; it is a gap in the inputs for a later plan. (minor under grading override) | Grep of the report for those words: zero hits; Read of 3.4. | Instance b to check whether 8.2 states how each stage is backed out; if not, add one constraint row (default-off or dormant until a later stage, remove by reverting the stage). |

#### Checked and found true (no finding)

| Item | What was checked | Result |
|---|---|---|
| T-1 | `git ls-files 'src/superclaude/cli/review/*.py'`: 16 files, 5,086 lines; `__init__.py:14-36` optional-module registration loop (`panel_cmd` to `manifest_cmd`, `ModuleNotFoundError` guard) | true |
| K-1 / SC-16 | `panel_lint.py:33` `STABLE_FIELDS_1_8_0` and `:146` `TELEMETRY_FIELDS`; tests `test_pinned_field_lists_match_skill_md` (`:97`), `test_f3_f4_contract_version` (`:193`), `test_shadow_skill_contract.py:42` byte-identical-to-HEAD test | true |
| K-2 / SC-17 | `tests/cli/reflect/test_verdict_mapping.py`: 36 `def test_`; 0.80 threshold pins in `:432-458`; `sc-tasklist-protocol/SKILL.md:1171` and `:1179` state `< 0.80` and exit 0/10/11/2 | true |
| SC-03 / SC-04 pins | `test_review_ledger.py:193-217` (cleared after the next round), `test_review_cli.py:274-292` (cleared by one reviewer's report), `test_review_ledger.py:382` (one valid block is enough) | true |
| SC-14 | `manifest.py:115-127` builds the frozen manifest with `t2_engine_requested` and `t2_engine_effective` | true |
| SC-20 / SC-21 | `reusable_stages`, `read_committed` (manifest.py), `COMPLETION_STATES`, `channel_of` (findings_v2.py), `append_record` (telemetry.py, telemetry_cmd.py) exist | true |
| SC-26 | `fsm.py:364-372` is `is_groundable` (path non-empty, integer line > 0) | true |
| SC-28 | `tests/skills/test_review_severity_rule.py:320` is `test_f_no_old_cap_numbers_outside_implement_protocol` | true |
| SC-32 | `Makefile` has `sync-dev` (109), `verify-sync` (166), `lint-architecture` (362), `lint` (48); `tests/skills/test_primitive_dual_surface_lookup.py` exists | true (baseline command: finding 1) |
| K-6 | `.gitignore:13` is `lib/`; `pyproject.toml:54` pins `ruff==0.15.20` | true |
| K-9 | `git ls-files plugins/superclaude`: 125 files; skills `confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`; no reflect, tasklist, review or rf-* skill or agent | true |
| T-4 integration points | `Wave 4` (sc-workflow-protocol SKILL.md), `Stage 10.5` (sc-tasklist-protocol SKILL.md), `## Review Loop` (commands/spec-panel.md:256) exist | true |

### Summary

- Total findings: 5 (all graded minor under the grading override; none blocking). By information label: critical 0, important 2 (findings 1 and 2), minor 3.
- Blocking under the override: 0. No decision, recommendation, value-inventory destination, conflict outcome or recommendation-bearing number depends on any finding; no required section is missing; no security, data-loss or safety-boundary risk.
- Checklist coverage in this range: (a) gates and constraints in Section 3.3 and 3.4 name a file, test, command or rule in 30 of 33 criteria (finding 4 for the other three) and one gate command does not reproduce its baseline (finding 1); (b) the concrete core elements and module paths of 7.1 are OUTSIDE this range (line 3650; instance b); Section 3.1 T-1 to T-6 name `src/superclaude/cli/review/`, the registration lines and the supply list for a thin module; (c) integration points exist and were checked (T-4, SC-14, SC-26); (d) contract 1.8.0, dual-surface lookup and the plugin mirror are stated as constraints; shadow mode and rollback are not in 3.4 (finding 5).
- Not assessed (outside range): Section 7.1 and Section 8.2 content. Instance b owns them.
- Tool engagement: Read 5 | Grep 3 | Glob 0 | Bash 6 (read-only; no Tavily or web calls).
- Confidence: Verified 4 of 4 applicable checklist items (a, c, d in range; b limited to Section 3.1) | Unverifiable: 0 | Unchecked: 0 (7.1 and 8.2 are out of range, not unchecked).

**Verdict: PASS** (zero blocking findings under the grading override)

Status: Complete

