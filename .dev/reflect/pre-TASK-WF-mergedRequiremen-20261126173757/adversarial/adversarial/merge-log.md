# Merge Log

Base: variant-2-original.md (reviewer 2). Donor: variant-1-original.md (reviewer 1). Plan: refactor-plan.md (6 numbered changes). Merge date: 2026-11-26.
Output: `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/merged-output.md`

## Per-change log

| # | Plan change | Source | Applied | Before / after | Validation |
|---|---|---|---|---|---|
| 1 | Verdict line: FAIL; all three HIGH invariants included; BLOCKED_BY_INVARIANTS | Base (reworded) | Yes | Base: FAIL with a long sentence about the approval gate, staging and two contradictions. After: one line, FAIL, 6 Blocking including B-4/B-5/B-6 (INV-001/002/006), BLOCKED_BY_INVARIANTS. | One line; matches the table. |
| 2 | Blocking rows B-1 to B-6 with settled fixes and real plan lines | B-1: V1 F1 + V2 QA-4 (+INV-016). B-2: V1 F5 + V2 QA-5. B-3: V2 QA-6 + V1 F8 (+INV-004). B-4, B-5, B-6: probe INV-001, INV-002, INV-006 | Yes | Base had 5 Blocking (Safety, 3 Decision, 1 Missing). After: 6 Blocking (5 Decision, 1 Missing, 0 Safety). The base's Safety grade is not carried (plan "Changes NOT Being Made"). | Each row has plan lines re-read against the 140-line plan; donor's lines (31 too high) not copied. |
| 3 | Medium rows M-1 to M-9 | M-1 V1 F4/V2 QA-1; M-2 V1 F2 + INV-010; M-3 V1 F3 + INV-012; M-4 V2 QA-2; M-5 V2 QA-3 (+INV-015 wording); M-6 V1 F6 + INV-013; M-7 INV-003; M-8 INV-014; M-9 INV-016 remainder | Yes | Base QA-1, QA-2, QA-3 downgraded to Medium; donor F2, F3, F4, F6 added; four probe rows added. | Grades match the debate's final grades. |
| 4 | Note rows (12): C-010, C-011, C-012, C-013, C-015, INV-004, INV-005, INV-007, INV-008, INV-009, INV-011, INV-015 | N-1 V1 F10/V2; N-2 V1 F10; N-3 V2 QA-7; N-4 donor line offset; N-5 calibration; N-6 to N-12 probe | Yes | Base had 1 Note (QA-7). After: 12 Notes. | Counted in the table: 12. |
| 5 | Coverage check: keep base groups; update INF-020, INF-040, INF-041, INF-051; add the A-003 scope note | Base | Yes | Base groups kept; INF-020 now points at M-4/M-5, INF-040/041 at M-1/M-3, INF-051 at B-3; other groups gained cross-references (B-1, B-2, B-4, B-5, B-6, M-2). Base's candidate-finding disposition block was not carried. | Every plan citation in the section re-read. |
| 6 | Provenance per row, final counts 6/9/12 | All | Yes | Provenance column on all 27 rows (V1, V2 or probe INV-NNN); header comment names base and date 2026-11-26. | Table counted: 6 Blocking, 9 Medium, 12 Note; debate record states the same. |

## Judgment calls and plan ambiguities (reported, not decided strategically)

- The plan says INV items merged into parent rows are "not counted twice", yet its own lists of 9 Medium and 12 Note include M-9 (INV-016 remainder) and INV-004 ("merged into B-3"). To reach the stated 6/9/12 I kept both as separate rows and split the content: B-1 holds the wording and M-9 the enforcing test; B-3 holds the staging step and N-6 the working-folder and ordering risk. If the owner wants them folded into their parents, the real counts would be 6 Blocking, 8 Medium, 11 Note.
- Where the plan gives no fix for a probe Note (N-7, N-8, N-9, N-10) the fix column says "reported only, no fix agreed"; I did not invent one.
- M-6 and M-9 carry "suggested name" test names; these are suggestions, not plan text.
- B-4: the two probe-level tests named in the plan's acceptance call `probes` directly (seen at tests/sweep/test_probes_allowlist.py:831 and :890), so only the `test_cli_contract.py` cases are listed as breaking.
- Not carried (not in the plan's lists): donor F7 (rebuild re-read under lock, wording), donor F9 (stale-header separator), the donor's negative checks (marker registration, `test_readonly.py` patching), and the base's candidate-finding dispositions. The base's "not confirmed" view of the duplicate-row defect is superseded by M-2 (debate item X-001, V1 won).
- Base QA-1's Safety grade was not carried, so the card has no Blocking (Safety) row.

## Post-merge validation

| Check | Result |
|---|---|
| INV-001, INV-002, INV-006 present as Blocking | PASS: B-4, B-5, B-6, each `Blocking (Decision)` (pattern count 3) |
| Every cited line re-Read | PASS: plan (140 lines) and spec (157 lines) read in full; repo lines read in the ranges cited (test_cli_contract.py 186-193, 372-391, 474-493; install_hooks.py 240-283; tests/cli/test_install_hooks.py 85-110, 152-156; probes.py 44-47, 150-159, 370-439; commands.py 84-95, 212-269; report.py 180-197; launch.py 208-253; test_sweep_command.py 494-499; pyproject.toml 182-195; reviewer-2.md 340-398; test_probes_allowlist.py 824-835, 880-891); folder files read in full. No citation points past a file's end. |
| Counts in the debate record match the table | PASS: counted 6 Blocking, 9 Medium, 12 Note (27 rows); the record states 6/9/12, so no correction was needed |
| Sections present | Verdict, Findings, Coverage check, Debate record, Self-reported confidence |
| Header comment | Names base (variant-2-original.md) and merge date 2026-11-26 |
