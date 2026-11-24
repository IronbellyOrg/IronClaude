# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-11-23T18:28:13Z
- Variants compared: 3
- Total differences found: 30
- Categories: structural (8), content (10), contradictions (4), unique (8)
- Shared assumptions: 9 (4 UNSTATED)

## Structural Differences

| ID | Aspect | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Verdict line | `Verdict: PASS (with notes)` at v1:7, after persona/model/root lines | `Verdict: PASS` at v2:2, first line after title | `Verdict: FAIL` at v3:8, after an unverified reviewer timestamp line (v3:7) | Medium |
| S-002 | Severity scale | Mixed: rows graded MEDIUM/MEDIUM/LOW, header counts "0 Blocking, 2 Medium, 1 Note" (v1:8); row 3 category "Note" is outside the 4-category taxonomy (calibration r1:9) | No severity scale used; "Blocking0, minor0" (v2:8) | Blocking/Medium with HIGH/MEDIUM column (v3:9, v3:14-17); dual severity-vs-grade labels (calibration r3:9) | Low |
| S-003 | Deviations table | 3 rows, 6 columns (v1:11-15) | No table; "None." (v2:11) | 4 rows, 6 columns, same column set as v1 (v3:12-17) | Medium |
| S-004 | Coverage section | Prose "Adherence summary" only, no per-requirement mapping (v1:17-18) | Dedicated `## Coverage` table mapping INF001-INF008 to plan lines (v2:16-27) | Prose adherence summary with per-unit counts 5+1+0+2+0 (v3:19-20), no plan-line table | Medium |
| S-005 | Supporting-evidence section | `## Why no blocker` (v1:20-25) | `## Independent feasibility` (v2:29-36) | `## What checked and sound` (v3:22-28) | Low |
| S-006 | Limits / self-disclosure | Explicit `## Limits` section: ran nothing, did not glob code-review.md, grep-only helpers, no codegraph (v1:27-28) | Limits folded into `## Notes` (v2:38-39) | Limits folded into `## Notes` (v3:30-31) | Low |
| S-007 | Recommendation section | `## Recommendation` proceed to execution (v1:30-31) | `## Recommendation` accept PASS (v2:41-42) | No recommendation section; corrective actions embedded in row 1 (v3:14) | Low |
| S-008 | Calibration header | 0.73 with explicit warning that the resume consequence is disputed (v1:4) | 0.73 (v2:5) | 0.87 (v3:4) | Low |

## Content Differences

| ID | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Swarm-wizard skill reference tables (`refs/cli-contract.md:44`, `refs/interview.md:65`) | Not mentioned | Not mentioned | Blocking drift: both tables still name `/sc:code-review --apply` for refactor-find; plan81 "No changes to installed skill ... definitions are required" and plan84 count of four leave them stale; fix: add both rows, sync-dev without staging `.claude`, count 4 -> 6 (v3:14) | High |
| C-002 | `docs/swarm/wizard-guide.md:216` follow-up list | Medium drift: still lists `/code-review`; ask Task4 to record broader list as deliberately out of scope in documentation-check.txt (v1:14) | Not mentioned | Medium drift: list no longer true; treated `/code-review` as a real built-in (plugins/superclaude/commands/help.md:85), so not Blocking (v3:15) | Medium |
| C-003 | Bundled-default vs caller-template detection (Task3, plan60) | Medium plan gap: no rule; caller template equal to default "renders same string, harmless"; suggest lens-name/template-equality/absent-compare_files rule (v1:13) | No gap: raw spec_dict local at commands.py:1684,1731-1742, defaults filled at preflight.py:539-543; distinction "not demonstrably infeasible" (v2:35) | Medium drift: scaffold writes the lens default via `_build_spec_from_lens` (commands.py:929,3736), so treating all spec input as caller-owned leaves the placeholder in the documented scaffold-to-stdin flow; add template equality + absent compare_files + a scaffold-to-stdin test (v3:16) | Medium |
| C-004 | Quoting rule for paths in `--compare` list (plan62) | Not raised | Treats "spaces and comma paths" as covered at plan62-68 (v2:25) | Medium drift: consumer interface (adversarial.md:15,39,58) defines comma list but no quoting rule; suggest whole-list double quotes shared by parser and docs (v3:17) | Medium |
| C-005 | Resume behavior | Note: resume never supplies compare_files, so resumed refactor-find would render literal `{compare_files}`; pre-existing, out of plan (v1:15) | Not mentioned | Resume at commands.py:2578-2586 passes no template, so suggestion is empty; no stale command left there (v3:23) | Medium |
| C-006 | Coverage of "Update the matching documentation" (source.md:1) | Covered in substance; four refactor-specific occurrences correct, wizard-guide only a clarity gap (v1:14, v1:18) | INF004 covered at plan79-86, "three docs/four known occurrences" (v2:23, v2:36) | Not covered: matching-docs unit classed as Drift because of the two wizard tables (v3:14, v3:20) | High |
| C-007 | Verdict and severity total | PASS with notes; 0 Blocking, 2 Medium, 1 Note (v1:7-8) | PASS; 0 deviations (v2:2, v2:8) | FAIL; 1 Blocking, 3 Medium (v3:8-9) | High |
| C-008 | Consumer interface compatibility (suspect=False, count 2-10) | `_validate.py:417-429` forbids suspect_files for suspect=False; adversarial.md:39 count matches plan guard (v1:21) | adversarial.md:15,39 accepts 2-10 existing files; skill SKILL.md:42,60-62 requires readability (v2:33) | Authorized expansion: count/path/empty-suggestion guards follow consumer interface (v3:20) | Low |
| C-009 | Red-test feasibility | Availability and argument-list checks should fail today; source inference, not observed (v1:25, v1:28) | test_commands_run.py:507-542 real-dispatch pattern exists; plan requires public group instead (v2:34) | Task dependency chain red -> partial green -> full green -> docs, no cycles (v3:25) | Low |
| C-010 | Scope of production edits | Not separately assessed | Not separately assessed | Two-source-file boundary sound: refactor_find.py:53 and commands.py:2129-2144 (v3:23) | Low |

## Contradictions

| ID | Point of conflict | Variant 1 position | Variant 2 position | Variant 3 position | Impact |
|---|---|---|---|---|---|
| X-001 | Verdict, and whether Task4 covers all "matching documentation" (source.md:1) | PASS (with notes); four refactor-specific occurrences "correct", only wizard-guide.md:216 flagged Medium (v1:7, v1:14) | PASS; INF004 covered by "three docs/four known occurrences" at plan79-86 (v2:2, v2:23, v2:36) | FAIL; Task4 can pass while two active swarm-wizard reference tables still recommend the missing command; count should be six, not four (v3:8, v3:14) | High |
| X-002 | Consequence of a resumed refactor-find run | Resume never supplies compare_files, so the resumed run "would render literal {compare_files}" (v1:15) | Silent | Resume "passes no template, so suggestion empty"; untouched resume leaves no stale command (v3:23) | Medium |
| X-003 | Whether the default-vs-caller template distinction is a plan deviation | Yes, Medium plan gap: "Risk named, rule not" (v1:13) | No: zero deviations; distinction "not demonstrably infeasible within named edit location" (v2:8, v2:35) | Yes, Medium drift: scaffold-to-stdin flow would keep the placeholder (v3:16) | Medium |
| X-004 | Whether plan62 adequately specifies path quoting | Silent | Covered: plan62-68 handles "spaces and comma paths" (v2:25) | Not covered: comma list without a quoting rule; parser and docs may diverge (v3:17) | Medium |

Source facts observed (recorded by this diff agent; no winner chosen):

- X-001: plan line 79 limits Task4 to docs/swarm/README.md, docs/swarm/lens-catalog.md and docs/swarm/user-guide.md; plan line 81 says "No changes to installed skill or command definitions are required."; plan line 84 says "all four known stale occurrences". `src/superclaude/skills/sc-swarm-wizard-protocol/refs/cli-contract.md:44` currently reads ``| `refactor-find` | "find small safe cleanups to apply" | 3 | `findings_table_v1` | `/sc:code-review --apply` |`` and `refs/interview.md:65` reads ``| cleanups | `refactor-find` | stub→openai_compat | 3 | tui | `/sc:code-review --apply` |``. Neither file is named in plan lines 79-86. `docs/swarm/wizard-guide.md:216` reads "The follow-up each lens hands off to: `/sc:adversarial`, `/code-review`, `/sc:reflect`," and is also not named. Whether these count as "matching documentation" is the judgment in dispute; the stale text itself is present.
- X-002: `src/superclaude/cli/swarm/commands.py:2578-2586` calls `reduce_wave3(combined, mode=..., output_dir=..., workers_requested=..., status_policy=..., job_id=..., resume=True)` with no `recommended_next_command_template` or `recommended_next_command_substitutions` argument (arguments read directly, not inferred from grep). `src/superclaude/cli/swarm/reduce.py:553` defaults `recommended_next_command_template: str = ""`; `reduce.py:672-674` renders via `_render_recommended_next_command`, and `reduce.py:460-461` returns `""` when the template is empty. The literal-placeholder passthrough at `reduce.py:463-467` applies only to a non-empty template. Calibration r1:16 reaches the same reading.
- X-004: plan line 62 says "Handle ordinary output paths with spaces through appropriate argument quoting; an unrepresentable comma within a path must not silently become two comparison files." It names no concrete quoting form.

## Unique Contributions

| ID | Variant | Contribution | Evidence | Value |
|---|---|---|---|---|
| U-001 | Variant 3 | Two swarm-wizard skill reference tables still name `/sc:code-review --apply`; plan81 denial of skill changes and plan84 count of four must change | v3:14; source cli-contract.md:44, interview.md:65 | High |
| U-002 | Variant 3 | Scaffold-to-stdin flow (`_build_spec_from_lens`, commands.py:929,3736; command-reference.md:82; operator-runbook.md:55) needs a dedicated test so a scaffolded default is not treated as caller-owned | v3:16 | Medium |
| U-003 | Variant 3 | Concrete quoting rule: whole-list double quotes shared between test parser and docs | v3:17 | Medium |
| U-004 | Variant 2 | Per-requirement coverage table mapping INF001-INF008 to plan lines | v2:18-27 | Medium |
| U-005 | Variant 2 | Notes that existing test_commands_run.py:507-542 invokes the subcommand directly while the plan requires the public CLI group | v2:34 | Low |
| U-006 | Variant 1 | Optional disposition for wizard-guide.md:216: record the broader list as deliberately out of scope in documentation-check.txt | v1:14 | Low |
| U-007 | Variant 1 | Bare-review golden `all-success/return-contract.yaml:28` requires the existing-review prefix (calibration r1:7 could not find it at the guessed path) | v1:23 | Low |
| U-008 | Variant 3 | Confirms historical exclusions (release-notes-v1.md:34, william.md:50) are proper | v3:27 | Low |

## Shared Assumptions

| ID | Agreement point | Implicit precondition | Classification | Evidence |
|---|---|---|---|---|
| A-001 | The defect is the template literal at refactor_find.py:53 | `recommended_next_command_template=("/sc:code-review --apply {compare_files}")` is the only refactor-find source of the stale command | STATED | v1:21, v2:30, v3:23; source refactor_find.py:53 read |
| A-002 | `/sc:adversarial --compare` with 2-10 existing files is a valid non-suspect replacement | adversarial.md:15,39 is the authoritative consumer contract and the installed skill matches it | STATED | v1:21, v2:33, v3:17 |
| A-003 | The fresh-run builder at commands.py:2129-2157 is the correct and sufficient edit point | All fresh-run recommendation paths go through this one block; no other caller of `reduce_wave3` passes a refactor-find template | UNSTATED [SHARED-ASSUMPTION] | v1:22, v2:31, v3:23; calibration r1:19 "did not enumerate all reduce callers" |
| A-004 | The four named doc occurrences (README:67, lens-catalog:25/49, user-guide:200) are real and stale | Line numbers stay valid until Task4 runs | STATED | v1:14, v2:36, v3:27 |
| A-005 | No existing test pins the stale `/sc:code-review --apply` command | A grep-level absence in tests/swarm is enough; no golden or snapshot elsewhere pins it | UNSTATED [SHARED-ASSUMPTION] | v1:24, v3:26; v2 implicit via feasibility (v2:34) |
| A-006 | Plan is plan-only; no current repaired evidence is expected | Execution needs separate approval | STATED | v1:31, v2:42, v3:31; plan19 |
| A-007 | `/sc:code-review` is not a packaged command | The plan's absence statement is correct; v1 did not glob for code-review.md (v1:28) and v3 treats `/code-review` as a separate real built-in (v3:15) | UNSTATED [SHARED-ASSUMPTION] | v1:25,28; v2:20; v3:14 |
| A-008 | Caller overrides are visible and preservable through `setdefault` / inline_job | Precedence contract at preflight.py:539-543 is unchanged by the fix | STATED | v1:13,23; v2:35; v3:16 |
| A-009 | Reviewer grounding on the live worktree is acceptable | reviewer_isolation=disabled did not change the files read | UNSTATED [SHARED-ASSUMPTION] | v1:5, v2:7, v3:5 |

## Summary
- Total structural differences: 8 (S-001 to S-008)
- Total content differences: 10 (C-001 to C-010)
- Total contradictions: 4 (X-001 to X-004)
- Total unique contributions: 8 (U-001 to U-008)
- Total shared assumptions surfaced: 9 (A-001 to A-009); UNSTATED [SHARED-ASSUMPTION]: 4 (A-003, A-005, A-007, A-009); STATED: 5; CONTRADICTED: 0
- Highest-severity items: X-001 / C-001 / C-006 / C-007 / U-001 (verdict PASS/PASS/FAIL turns on whether the two swarm-wizard reference tables at cli-contract.md:44 and interview.md:65 are "matching documentation" that Task4 must cover); then X-002 (resume consequence, literal placeholder vs empty suggestion), X-003 (default-vs-caller detection), X-004 (quoting rule).
- Calibrated weights for the debate: Variant 1 0.73, Variant 2 0.73, Variant 3 0.87 (reviewer-{1,2,3}-calibration.md). Calibration r1:16 already marks Variant 1's resume consequence as wrong against source.
- This file records differences only; it does not debate, score or pick a winner.
