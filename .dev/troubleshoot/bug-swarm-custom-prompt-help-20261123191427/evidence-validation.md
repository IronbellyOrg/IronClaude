# Evidence Validation Report

**Report under validation**: ./REPORT.md.draft
**Timestamp**: 2026-11-23T19:29:02Z
**Total citations**: 8 Evidence items
**Verified**: 7 (worker headline; eight verified table rows below)
**Dropped**: 0
**Passed through (command, no reexec)**: 4 command claims attached to Evidence6-8; captured text independently verified.
**Result**: PASS
**Suggested report status**: blocked, solely existing HC1/HC5 repaired-state blockers, not a citation defect.

Scope checked independently: all source/capture citations in Evidence1-8, repeated Documentation/Audit/hardening artifact references, A1-A10. Every cited file read at cited range. Zero findings accepted without quota.

## Verified citations

| # | Type | Location | Verdict |
|---|---|---|---|
| 1 | source | src/superclaude/cli/swarm/commands.py:438 | verified, docstring literal names --custom-prompt-dir |
| 2 | source | src/superclaude/cli/swarm/commands.py:3785 | verified, option-help literal names same option |
| 3 | docs | docs/swarm/command-reference.md:56-61 | verified, not a run flag, JobSpec field and custom lens; formatting normalization acknowledged |
| 4 | source | src/superclaude/cli/swarm/preflight.py:1592-1615 | verified, custom lens, dict field and directory reader; not execution proof |
| 5 | source | src/superclaude/cli/swarm/schema.py:710-734 | verified, nonempty field binding; absent/empty case permitted |
| 6 | capture | ./scaffold-help.txt:24; ./validate-lenses-help.txt:7 | verified, full raw help contains stale flag; exits parent-observed |
| 7 | capture | ./run-rejection.txt:4 | verified, No such option error; exit parent-observed |
| 8 | capture | ./module-origin.txt:1 | verified, absolute current-checkout commands.py path |

## Dropped citations

None. No line, file or snippet mismatches.

## Passed-through citations (command, allow_command_reexec=false)

| Command | Note |
|---|---|
| uv run superclaude swarm scaffold --help | Not reexecuted; captured text independently read. |
| uv run superclaude swarm validate-lenses --help | Same. |
| uv run superclaude swarm run --custom-prompt-dir /tmp | Same; exit2 parent-observed. |
| uv run python -I -c 'import superclaude.cli.swarm.commands as commands; print(commands.__file__)' | Same; path capture verified. |

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | none | none | Static wording, not definite enum headline; calibration1.00; stale text in provenance-bound captures. |
| A2 | skipped | none | none | input absent: diff_path=null; tasklist proposes no instrumentation change. |
| A3 | no | none | none | Date19:27:11Z earlier than draft mtime19:28:55Z+5min; not midnight. Pending Duration is not timestamp. |
| A4 | no | none | none | Closure verdict blocked belongs to contract. |
| A5 | skipped | none | none | input absent: candidate-fixes.md; no Tier2/adversarial/consensus or dynamic claim. |
| A6 | no | none | none | No Reference-context cell or first-run n/a exemption; true/false prediction cells are not reference observations. |
| A7 | no | none | none | RUN-SITE resolved to commands.py438/3785, not pending-producers. |
| A8 | no | none | none | Same-shell local CLI, not CI job. |
| A9 | skipped | none | none | No actual reference arm, comparator none; pending rows do not certify control. |
| A10 | no | none | none | capability-verdict n/a, two usable capture routes, no unsupported capability block. |

## Notes

- All eight Evidence items match sources; quoting preserves docstring versus option-help markup. Source and capture distinction explicit.
- All referenced context, calibration, locus, snapshot, audit and four hardening cards exist.
- Calibration has six dimension rows, nine C-rule rows and1.00 bounded score.
- Byte count13359 and parent exit statuses were not independently executable with read-only tools; not load-bearing for static claim. Parent tool results carry those observations.
- run-help directory placeholder is not rejected flag spelling. No unsolicited adjacent change needed.
- Existing HC1/HC5 FAIL and latched waiver remain disclosed, not relabelled passing by evidence PASS.
- Validator did not read or mutate preexisting validation stub. No inputs absent except null diff, absent candidate-fixes and no Reference-context cell.
- Parent receipt note: worker headline says Verified7 but table has8 verified rows. Preserve this minor count inconsistency rather than invent a citation drop; verdict and zero-drop evidence unchanged.
