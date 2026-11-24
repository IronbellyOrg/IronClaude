# Evidence Validation Report

**Report under validation**: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s/.dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/REPORT.md.draft
**Timestamp**: 2026-11-23T17:24:22Z
**Total citations**: 9 grouped evidence items
**Verified**: 7
**Dropped**: 0
**Passed through (command, no reexec)**: 2
**Suggested report status**: success (citation/structural checks only; prior blocked status and HC1 blocker stay)
**Binary verdict**: PASS for independent diagnostic evidence, not repair acceptance

## Verified citations
| # | Type | Location | Verdict |
|---|---|---|---|
| 1 | file:line | src/superclaude/cli/swarm/lenses/refactor_find.py:53 | verified executable stale command template |
| 2 | file:line | src/superclaude/cli/swarm/commands.py:2141-2143,2145-2157 | verified literal existing-review prefix and template/substitution handoff |
| 3 | source/artifact | src/superclaude/cli/swarm/reduce.py:672-697,701-702; stub-run/return-contract.yaml:64 | verified rendered/stored/emitted command; final paths match artifact lines27,39,51 |
| 4 | captured output | tier1-observation.md:8-11,29-36 | verified missing packaged/installed namespaced command and actual input checks; independent Glob found no code-review under packaged commands or ~/.claude/commands |
| 5 | declared interface | src/superclaude/commands/adversarial.md:15,39; /home/coder/.claude/commands/sc/adversarial.md:15,39; /home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md:60-62 | verified comma-separated 2-10 existing readable files; declared contract only, not executed |
| 6 | documentation | docs/dev/lens-contribution-policy.md:287-292,317-334; docs/swarm/lens-catalog.md:25,49 | verified real-command/flags requirement and duplicated stale follow-up |
| 7 | implementation/tests | src/superclaude/cli/swarm/lenses/_validate.py:603-609; tests/swarm/test_bundled_lenses.py:119-122; tests/swarm/test_reduce.py:305-314 | six checks do not test command existence; template presence and fictional /sc:foo interpolation verified |

## Dropped citations
None.

## Passed-through citations (command, allow_command_reexec=false)
| # | Command | Note |
|---|---|---|
| 8 | uv run superclaude swarm run --lens refactor-find ... --transport stub | not re-executed by policy; captured exit0/stdout matches observation:22 and existing result artifacts |
| 9 | uv run pytest tests/swarm/test_bundled_lenses.py tests/swarm/test_reduce.py -q | not re-executed by policy; 76 passed in 0.92s matches observation:40-44 |

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | - | - | string headline, calibrated0.92; both disputed strings present in captured failing-output spans |
| A2 | skipped | - | - | diff_path null; zero measurement rows/no instrumentation diff |
| A3 | no | - | - | draft Date17:22:17 before mtime17:24:07+5min, not midnight; calibration timestamp valid; no other time claims |
| A4 | no | - | - | blocked is an allowed hardening verdict |
| A5 | skipped | - | - | candidate-fixes.md absent; no Tier2/consensus claim |
| A6 | skipped | - | - | no Reference-context probe rows, first_instrumented_run={} |
| A7 | no | - | - | RUN-SITE resolved at reduce.py:672 local .venv; one producer row, no pending sentinel |
| A8 | no | - | - | same-shell local run, no identified failing CI arm |
| A9 | skipped | - | - | no reference-arm value/probe; unknown control is not certified |
| A10 | no | - | - | capability-verdict n/a, not blocked; emitter search also present |

## HC5 off-path review
**Performed**: YES
**Binary verdict**: PASS (diagnostic evidence only). Does not authorize implementation or clear HC1.

Read runtime-entrypoint.md, contract-ledger.md, unmask-sweep.md, effective-input.md and the full stub-run/return-contract.yaml. Independently Read lens:53, commands:2141-2159 and2576-2586, preflight:537-545, reduce:668-705, validator:600-611.

- Included evidence is the real original CLI output, not a fabricated fix or unrelated diff. Result artifact has job_id lens-refactor-find-39439f65, status success and three existing final report paths. Line64 contains the stale command and literal prefix.
- effective-input.md and supplied working-tree evidence indicate no tracked-source change, only diagnostic output. No repair/diff was substituted.
- Cards explicitly state positive witness not run/NOT PROVEN, HC1 FAIL for repair closure, and no repaired-state coverage. Correctly not claimed as implementation acceptance.
- Spot-checked ledger rows match source. Did not Read commands.py:929-930 or wizard rows, so no independent assertion on those rows.
- HC5's pending-review requirement is satisfied by this receipt. Parent may change HC5 to performed/PASS; HC1 stays FAIL and closure stays blocked.

## Notes
Zero blocking defects. Reviewed all nine evidence items, the dependent Documentation/Diagnosis/Proposed Fix claims and the boundary cards against the draft. Source and captured output establish the stale template plus literal prefix. Existing cited tests check presence/interpolation, so baseline passes do not disprove the bug.

Minor Notes (not fix-pass triggers):
- A separate marketplace code-review command file exists under ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-review/commands/code-review.md. Different namespace, not /sc:code-review, no demonstrated --apply contract; does not refute namespaced absence.
- Draft duration says final duration goes in audit footer; validator cannot independently verify it. Parent should fill actual final clock.
- Contribution policy:311 uses src/superclaude/commands/sc/<name>.md, while packaged commands use src/superclaude/commands/<name>.md. Draft does not rely on that incorrect lookup line.

Skipped A2/A5/A6/A9 are recorded, not passed. Not Read by validator: doc-context.md, diagnosability-context.md, tier1-hypothesis.md, tier1-callers.md, branch files, audit.log; they are not evidence citations in the nine-item list. Parent owns this output. No files modified or commands run by reviewer. Preserve failed > blocked > partial > success; the suggested success cannot remove the existing repair-closure blocker.
