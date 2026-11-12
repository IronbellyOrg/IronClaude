# Evidence Validation Report (attempt 1; superseded by evidence-validation.md after repairs, kept as failure history)

**Report under validation**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/REPORT.md.draft
**Timestamp**: 2026-11-08T00:19:18Z
**Total citations**: 14 (12 file:line, 2 command)
**Verified**: 12
**Dropped**: 0
**Passed through (command, no reexec)**: 2
**Suggested report status**: partial (A5 contributes partial). **Structural FAIL: A6 and A7 fired** (repair and revalidation required before publication).
(Returned by evidence-validator; persisted by the parent; table condensed.)

## Verified citations
All 12 file:line citations matched at the cited ranges: CLAUDE.md:308, :320; IronOrca worktree-first-surface.ts:2-14; worker-topology.ts:67-76; worker-start-receipt.ts:101; explicit-worker-terminal-validation.ts:49-54; install_core.py:70-72; src/superclaude/core/CLAUDE.md:47; orca_worktree.py:27 and :42; definitions-core-2.ts:69 and :74. Supplementary (outside Evidence): CLAUDE.md:307, :312; core/CLAUDE.md:52, verified.
Qualifications: item 2 needs the caller at runtime-local-worktree-terminal-startup.ts:202-214 (in tier1-observation.md row 1, not cited in Evidence); item 3 "into an existing worktree / not the seeded one" is inference from `id:${args.worktreeId}`; item 4's recovery string appears only when `releasable` is true (lines 99-103).

## Dropped citations
None.

## Passed-through citations (command, allow_command_reexec=false)
- Item 8 `grep -c "Orca session launches" ~/.claude/CLAUDE.md` → `0`: consistent with tier1-observation.md O5.
- Item 9 `jq` for install-core-stale-warning → `2026-11-07T05:36:16.234Z startup-command-delivery false 0`: the exact output line, including the trailing `0`, was not reproduced verbatim in any file read; the parent should confirm against its capture.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | no definite enum token named; Root cause is UNDETERMINED; all four calibrations 0.30; observation_paths empty |
| A2 | skipped | — | — | input absent: diff_path (null) |
| A3 | no | — | — | draft Date 2026-11-08T00:18:09Z not later than mtime 00:19:10Z + 5 min |
| A4 | no | — | — | closure says "not applicable"; HC0 decisions use `not_applicable` |
| A5 | yes | `consensus_on_unobserved` | partial | candidate-fixes.md:5 says "consensus on the producer (P1) and the edit" and Wave 4 was not run; the Tier 1 and quality-engineer cards are `runtime_behavior`/`source_static` with Runtime check 0.0; hedged as split-pending in the same file, but the trigger has no exemption for a hedge |
| A6 | yes | `reference_value_not_literal` | FAIL (repair and revalidation required) | diagnosability-tasklist.md row M-QE: "Reference value: n/a (first run); counter-case O3 ... gives false (...)": first_instrumented_run was unknown so the exemption does not apply; "n/a (first run)" is not the exact `n/a` token and carries extra prose; not one literal |
| A7 | yes | `run_site_unresolved` | FAIL (repair and revalidation required) | execution-locus.md:4 `RUN-SITE: pending-producers` while producers.md has four rows (P1-P4); locus mtime 00:00:13Z earlier than producers 00:00:28Z |
| A8 | no | — | — | arm is the Orca UI, not a CI job |
| A9 | no | — | — | M-QE reference unobserved first-run n/a (comparison skipped); M-C observed, no literal reference; no control certified (CONTROL-PROOF unknown) |
| A10 | no | — | — | capability-verdict n/a |

## Notes
- A6/A7 are structural FAIL, not a normal partial: repair and revalidate once, or take the failed diagnostic disposition. Nothing was edited by the validator.
- A5 comes from candidate-fixes.md, not the draft text; the draft says no two strong competing fixes exist.
- Not verified: docs under docs/ listed in Documentation Context (no line claims) and the "#412/#415" numbering outside tier1-observation.md O5.
