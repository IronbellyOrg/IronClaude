# Reflect Reviewer — Deviation Findings (reviewer 3, refactorer, model class opus -> claude-gw-tier1a)

Paths: PLAN = .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md ; DESIGN = docs/designs/sc-issue-launch-level-hook.md ; TOW = tests/skills/test_issue_orca_worktree.py ; OW = src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py ; TIP = tests/skills/test_issue_protocol.py ; SKILL = src/superclaude/skills/sc-issue-protocol/SKILL.md ; TIH = tests/cli/test_install_hooks.py ; IH = src/superclaude/cli/install_hooks.py

Total deviations: 11 (Regression 2, Drift 9) plus 1 advisory correctness gap. Adherent tasks: 15 of 22.

| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Regression | PLAN:287-299 (Task 18) | Task 18 adds guard-version, registration and jq checks but only updates the tests near TOW:1303 and :1324. The shared launch_scene fixture writes only "#!/bin/sh\n", so about 12 tests expecting "launched" would fail the new checks, and la3 and la6 change outcome. | TOW:994-1013 (fixture); TOW:1051,1124,1196,1210,1234,1265,1276,1301,1481,1534,1571,1594 (launched asserts); TOW:1159-1167 (la3); TOW:1295-1324 (la6); PLAN:293 | HIGH |
| 2 | Regression | PLAN:314-325 (Task 20) | Under IR-7 a governed launch with no L2 is refused and the plan builds no L2, so Task 20 turns every "launched" test into a refusal, including Task 18's own passing case and Task 19's tests. No fixture adds an owned L2 hook. | DESIGN:355; DESIGN:514; PLAN:298; TOW:994-1013 | HIGH |
| 3 | Drift | PLAN:314-325 (Task 20) | Owner decision (card R-2) is not owned by any task; Task 20 implements first and writes ir7-consequence.md afterwards, switching off the PR 425 claim pipeline with no recorded approval. | PLAN:320; DESIGN:355; OW:908-1009 | HIGH |
| 4 | Drift | PLAN:320 (Task 20) | "Owned shared hook file and recorded B-CTX contract marker" is not defined by the design; the design says a header alone does not prove ownership. The plan invents an interface the unbuilt L2 hook must later match. | DESIGN:512; DESIGN:508-514 | MEDIUM |
| 5 | Drift | PLAN:301-312 vs PLAN:314-325 | Task 19 reports a missing L2 as a status line on a launched claim; Task 20 then refuses that same case, so Task 19's tests describe a state that cannot exist after Task 20. | PLAN:305, PLAN:310, DESIGN:514 | MEDIUM |
| 6 | Drift | PLAN:287-312 (Tasks 18, 19) | The meaning of the enforcement_hook field and the claim status after the change is unstated; a new return key breaks the test that pins the ten return-contract keys. | SKILL:133,136,150; TIP:487-514; TIP:467-468; OW:722-725,986-989 | MEDIUM |
| 7 | Drift | PLAN:75 (Task 3) | Acceptance requires all 18 message ids from the real script while classifiers are stubs; most ids are reachable only after Tasks 4 to 10. | PLAN:75; merged-requirements.md:1302; :1293 | MEDIUM |
| 8 | Drift | PLAN:301-312 (Task 19) | The IR-5 re-claim test duplicates existing test la2. | TOW:1106-1128 | LOW |
| 9 | Drift | PLAN:26 | The edit-scope constraint excludes .dev/, but tasks write evidence into the package artifacts/ directory under .dev/. | PLAN:26; PLAN:320 | LOW |
| 10 | Drift | PLAN:349 (Task 22) | Treats any skipped test as failure, but existing tests skip on non-Linux and as root. | PLAN:349; tests/hooks/test_launch_job_identity.py:18; tests/hooks/test_freshness_subagent_start_policy.py:72; TOW:1186,1428 | LOW |
| 11 | Drift | Tasks 1-2 | Ignore the existing opt-in probe tests/hooks/fixtures/launch_level/live_probe.py, so a second probe would duplicate it. | live_probe.py | LOW |

One-line fixes: (1) Task 18 updates launch_scene (valid guard with version line, settings.json with both registrations, known jq) and lists every re-baselined test including la3 and la6; (2) Task 20 adds an owned-L2 fixture and lists tests that move from launched to refused; (3) add a blocking owner-decision task before Task 20 and write ir7-consequence.md before implementation; (4) detect only absence (always W-L2-ABSENT) or move the owned case to the L2 plan and drop the invented marker; (5) merge Tasks 19 and 20 or restate Task 19's assertions; (6) state the new enforcement_hook values and claim status, or update the ten-key test and SKILL.md in the same task; (7) keep only header and NOBIND/BROKEN formatting in Task 3, move per-id tests to Tasks 5-11 or Task 17; (8) point Task 19 at la2; (9) add the package artifacts/ to the edit-scope constraint; (10) allow environment skips in Task 22; (11) cite live_probe.py in Task 1 and reuse it in Task 2.

Checked and correct: Task 1 is first; Task 12 hook order is compatible with the pinned tests (freshness test pins only literal Bash matchers, TIH:825-857 wants launch-job-identity last); Task 13 fake-script list is needed (IH:248-250; TIH:89-105); Task 13 installer change is probably not needed (IH:354-449 works per event); --pipeline none never reaches the launch step (TOW:1373); 18 message ids is the right count; cited T-ids exist in the requirements.

Advisory A (Task 14, LOW): the guard's position holds only in the shipped hooks.json; _merge_settings appends new registrations at the end on upgrade (IH:446-449), so Task 14 must not assert a fixed position in the installed settings.json.

Correctness gap (advisory, non-gating): Task 18 tests would depend on the real machine: FakeOrca.env copies os.environ (TOW:102-110), so CLAUDE_CONFIG_DIR and the real PATH/jq leak into the fixture (TOW:994-1013, OW:704-725). Fix: unset CLAUDE_CONFIG_DIR and control the jq on PATH.

T1 card claims not confirmed: F7 source files not found; per-task T-id correctness; card coverage ratios; plugin hooks.json byte-identity (not read); CI jq availability.

<!-- calibration: mean_C 0.78, calibrated_confidence 0.70, calibrator opus (degraded diversity) -->
