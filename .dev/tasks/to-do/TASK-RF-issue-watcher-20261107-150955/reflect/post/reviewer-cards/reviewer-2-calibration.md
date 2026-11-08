| Status | Result |
|---|---|
| DONE | Calibrated reviewer 2's card against the five-dimension reflect rubric. Calibrated confidence C = 0.82, which recommends ESCALATE. |
| DONE | Checked all 22 file:line citations in the repository: 21 match exactly, 1 is one line off, 0 are wrong. I could not check 3 uncited counts. |
| DONE | Read the deadline control flow myself. The late-launch defect is real in the source code. Calling it a Regression fits the rubric's anchors, but the card overstates how severe and likely it is. |
| NEXT | Orchestrator: save the report below to the reviewer-2 calibration path. |

# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/reviewer-cards/reviewer-2-card.md
**Rubric**: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T04:55:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Citation grounding | 0.85 | All five deviations carry real file:line evidence. I checked 22 citations: 21 match exactly and 1 is one line off (p9-g2-summary.md:8, where the "CI only" text is on line 9). The rubric's 0.70-0.99 anchor fits because some supporting claims have no citation: the "six test functions, seven parametrized cases" count, the "2,635 watcher tests" figure (p9-g2-summary.md:2 says 2665 across the subset), "Existing timing tests do not exercise a slow pending-state save", and every bullet under "Acceptance-test assessment". |
| Coverage completeness | 0.75 | The card says it audited 13 units (12 assigned acceptance criteria plus the no-skip rule), with 8 adherent and 5 deviations. It never names the 12 criteria by ID and gives no coverage percentage, so I cannot check that the set is complete. It does list explicit gaps ("did not independently reproduce", "did not independently execute a Git comparison"). That fits the rubric's 0.60-0.84 anchor: partial coverage with explicit gaps, and the assigned set cannot be confirmed. |
| Deviation-classification clarity | 0.90 | Each of the five deviations has exactly one category from the taxonomy (Regression, Drift, Necessary deviation, Authorized expansion twice) and a one-line reason. It does not hedge between categories. Points off for finding 1: it is a Regression rated HIGH on source reading only, which the card admits ("established from source control flow, not a runtime reproduction"), and it gives no likelihood reasoning. See the Notes on the central claim. |
| Risk surface coverage | 0.85 | The card names one regression candidate (finding 1) and several invariants that no test covers: no test of a slow pending-state save, permission checks never run as root, eventual dispatch after day two not shown, subprocess coverage for only two commands, and the full-suite failures not reproduced. It misses two secondary points about the blast radius. First, cycle.py:50-52 rejects network filesystems for the state directory, so a save of two seconds or more is a rare edge case. Second, the worst case ends near 241 s, still inside the 300 s cadence. That fits the 0.70-0.99 anchor. |
| Recommendation actionability | 0.75 | Finding 1 names the target, the constraint (keep "durable-before-launch ordering and the specified budget-exhausted outcome") and a check ("add a test whose pending-state save crosses the cutoff"). It does not settle the conflict it names: checking again after the save would leave a pending entry on disk, which contradicts design line 647 ("the step ends with no entry"). Finding 2 says only "Remediate", with no method for the root-only skips. That fits the 0.70-0.99 anchor's lower end ("a minority are advisory"). |

## Calibrated confidence computation

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(five dimensions) | 0.82 | (0.85 + 0.75 + 0.90 + 0.85 + 0.75) / 5 = 4.10 / 5 |
| **calibrated C** | **0.82** | The reflect rubric applies no gates or caps |
| contracted-sink fold-in caps | not applied | The rubric's dimension-3 cap ("a static-only signal classified as Regression caps this dimension") covers only requirements with an explicit `durable_sink:` / `@sink` annotation. Design line 647 has none. |
| spot_check_unverifiable | none | The card cites no remote URLs |
| structural_flags | skipped | The troubleshoot structural assertions do not apply to the reflect rubric |

## Confidence

- **Self-reported (in card)**: none. The card states no confidence number. I scored only against the rubric anchors.
- **Calibrated (this report)**: 0.82
- **Formula applied**: arithmetic mean of the five reflect-rubric dimensions, rounded to 2 decimals. The intermediate value is shown above.
- **Delta**: not computable because the card has no self-report. The card's verdict (FAIL, two blocking findings) is still credible: the evidence holds up. The score falls below 0.85 because coverage cannot be checked, finding 2's fix is vague, and finding 1's severity has no likelihood reasoning. None of these is an error in the evidence.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`, with `forced_by_depth_deep` also applying
- **Rubric rule fired**: "`C < 0.85` is an automatic ESCALATE" (reflection-rubric.md, Threshold guidance). Separately, the depth is `--depth deep`.
- **Execution restriction**: none (`--no-escalate: false`).

## Spot-check results

| # | Citation | Result |
|---|---|---|
| 1 | cycle.py:1048 | Verified: the last `launch_allowed()` check, after the git origin call |
| 2 | docs/designs/issue-watcher.md:647 | Verified: "Orca launch, 120 s, never shortened, not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line" |
| 3 | cycle.py:1060 | Verified: `mark_pending`, then `_save()` at line 1061, then `d.launcher.launch(...)` at line 1062 with no deadline check in between |
| 4 | record.py:370 | Verified: `save` serializes to JSON, writes atomically, sets mode 0600, then syncs the directory (lines 370-378) |
| 5 | test_cli.py:1070 | Verified: `NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, ...)` |
| 6 | TASK file:188 | Verified: "No test may use `pytest.skip`, `skipif` or `xfail`" |
| 7 | test_cli.py:967 | Verified: root `skipif` |
| 8 | test_record.py:739 | Verified: root `skipif` |
| 9 | test_cycle.py:735 | Verified: root `skipif`. Items 5, 7, 8 and 9 are exactly the "four root-dependent skip expressions" |
| 10 | test_cycle.py:4694 | Verified: `pytest.skip` when not on Linux |
| 11 | test_cycle.py:4150 | Verified: the comment about the second day |
| 12 | spec-final.md:363 | Verified: "after the clock advances 24 h the rest launch, one per cycle" |
| 13 | test_cycle.py:4154 | Verified: `second_day = min(count - capped, 6)` |
| 14 | TASK file:1038 | Verified: judgment call (3) discloses the min(N-6, 6) reading |
| 15 | p9-g2-summary.md:2 | Verified: subset command, 2665 passed, 1 skipped |
| 16 | 06-gap-fill-decisions.md:28 | Verified: decision DF-05, full suite in CI only |
| 17 | p9-g2-summary.md:8 | One line off: line 8 holds the skip note, and "Full suite: CI only (decision DF-05)" is on line 9. The claim itself is true |
| 18 | test_module_boundaries.py:57 | Verified: the `record` rule allows sibling `predicates` |
| 19 | docs/designs/issue-watcher.md:239 | Verified: "`predicates` (types only ...)" |
| 20 | TASK file:332 | Verified: allows `parse_utc`, `format_utc`, `valid_issue_number` |
| 21 | test_module_boundaries.py:20 | Verified: discloses "design 5.3 says 'types only'" |
| 22 | main.py:563 | Verified: imports and registers `issue_watch_group` at lines 563-565 |
| no cite | "six test functions, seven parametrized cases" | Could not check (needs a count of `NOT_ROOT` uses; I had no search tool) |
| no cite | "Existing timing tests do not exercise a slow pending-state save" | Could not check (test_cycle.py is about 4,700 lines; I had no search tool) |
| no cite | "2,635 watcher tests passing with zero skips" | Could not check. p9-g2-summary.md:2 shows 2665 for the wider subset, so the 2,635 figure must come from a report the card does not cite |

## Notes

- **Reflect rubric used.** Per the orchestrator's instruction, I used the five-dimension reflect rubric with an arithmetic mean. I skipped the troubleshoot Runtime-check cross-table, the gated-minimum formula, the verdict-direction cap and the structural assertions.
- **Card frontmatter missing.** The card declares no claim class, evidence class or verdict direction. Under the troubleshoot defaults (runtime behaviour, no evidence), finding 1 would count as a dynamic claim backed only by source reading. I record this only; it does not change the score here.
- **Central HIGH claim (finding 1): the defect is confirmed.** `Deadline.launch_allowed()` returns `elapsed() <= LAUNCH_CUTOFF_S` (cycle.py:410-412, cutoff 120.0 at line 43). After the last check at cycle.py:1048, the code builds the context in memory (1052-1059), then calls `mark_pending` (1060) and `self._save()` (1061). `_save` reaches `FileStore.save`, which does an atomic write, chmod and directory sync (record.py:370-378). Then `d.launcher.launch(..., LAUNCH_TIMEOUT_S)` runs at line 1062 with no further check. If the save pushes elapsed time past 120 s, a full 120 s launch starts after the cutoff, which breaks design line 647. The ordering is a fixed fact of the code, so reading the source is enough to prove the defect exists. What the source does not prove is that a save can take that long.
- **Do the anchors support "Regression"?** Yes, on both anchors. Deviation-classification clarity asks for one category with a defensible reason. A stated requirement ("not started when `elapsed() > 120`") that the code can violate is a Regression, not Drift, which means an unauthorized change that breaks no requirement. The static-only cap in the dimension-3 fold-in covers only annotated sink requirements, so it does not apply. Its spirit is honoured anyway: the card says the finding is static-only. Risk surface coverage names "regression candidates" and "untested invariants" as the load-bearing items, and finding 1 is both. The weaker part is the HIGH / Blocking severity. The card does not say how likely the trigger is (cycle.py:50-52 rejects network filesystems, so the save is a local sync), and it does not size the consequence (about 241 s against a 300 s cadence). The card's own recommendation also leaves the fix's design conflict open: a check after the save would leave a pending entry with no launch, which contradicts "no entry" at design line 647.
- **Finding 2 classification.** Drift is defensible. The task text at line 188 bans `skipif` and `pytest.skip` outright, and the code uses both. The card correctly notes that zero-skip runs as a normal user do not show compliance with that rule.
- No files were changed. I ran no commands or tests.

I did not check the three uncited counts, and I did not read `_save`'s error handling. Neither changes the verdict on finding 1.
