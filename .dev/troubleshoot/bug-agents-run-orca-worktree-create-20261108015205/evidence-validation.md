# Evidence Validation Report

<!-- Returned by evidence-validator, persisted by parent on receipt 2026-11-08T02:25Z -->

**Report under validation**: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md.draft
**Timestamp**: 2026-11-08T02:21:46Z
**Total citations**: 22 (16 file:line, 6 command)
**Verified**: 16
**Dropped**: 0
**Passed through (command, no reexec)**: 6
**Suggested report status**: partial (A5 literal reading; no drops; A6/A7 not fired; A8 not fired)

## Verified citations

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | CLAUDE.md:308 (Ev 1) | verified |
| 2 | file:line | CLAUDE.md:320 (Ev 1) | verified; no `--agent`; 303-325 never mention the first terminal |
| 3 | file:line | IronOrca runtime-local-worktree-terminal-startup.ts:202-214 (Ev 2) | verified; createTerminal at :210 |
| 4 | file:line | runtime-local-worktree-terminal-startup.ts:259-269 (Ev 2) | verified; also requires activate !== true and runHooks !== true (note 4) |
| 5 | file:line | IronOrca src/shared/worktree-first-surface.ts:2-14 (Ev 3) | verified |
| 6 | file:line | IronOrca workspace-creation.ts:209 (Ev 4) | verified |
| 7 | file:line | workspace-creation.ts:239-271 (Ev 4) | verified; setupTerminalHandle only under awaitTerminalProvisioning (:250-269, :266); range stops early (note 5) |
| 8 | file:line | src/superclaude/core/CLAUDE.md:48-50 (Ev 5) | verified |
| 9 | file:line | src/superclaude/cli/install_core.py:70-72 (Ev 12) | verified |
| 10 | file:line | tests/core/test_orca_session_launch_guidance.py:14-31 (Ev 13) | verified; parametrized over both copies (:10-12); 12 phrases (:17-30) |
| 11 | file:line | CLAUDE.md:307-320 (Diagnosis) | verified |
| 12 | file:line | CLAUDE.md:307, :312 (Doc context) | verified |
| 13 | file:line | core/CLAUDE.md "ends at line 53" | verified; section opens :45, next heading :55 |
| 14 | file:line | ccsession-tag/README.md "ends at line 237" | verified; `#### The one question rule` at :239 |
| 15 | file:line | CLAUDE.md "after line 310" | verified |
| 16 | file:line | CLAUDE.md "example block (318-324)" | verified |

## Dropped citations

None.

## Passed-through citations (command, allow_command_reexec=false)

| # | Command | Note |
|---|---------|------|
| 1 | Ev 6 daemon jq | matches N8 for all 7 worktrees |
| 2 | Ev 7 transcript jq | matches N1 (18 rows, 1 with --agent, 11 cd follow-ups); 20:35:28.903Z precision from N6 |
| 3 | Ev 8 grep installed copy | matches N12 |
| 4 | Ev 9 issue-473-claim | matches N10 and N8 |
| 5 | Ev 10 --help | matches N2 |
| 6 | Ev 11 git log | matches N13 |

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| A1 | no | — | — | only enum-like token "Other" (catch-all); max calibrated 0.67; mechanism token hasCommand=false in captured N8 |
| A2 | skipped | — | — | input absent: diff_path (null) |
| A3 | no | — | — | no Timestamp line; Duration/Date are placeholders; no T00:00:00Z |
| A4 | no | — | — | "HC0 not run — applicability unassessed" is the contract form |
| A5 | yes | `consensus_on_unobserved` | partial | adversarial invoked (first clause not met); second clause met literally: tier2-quality-engineer-calibration.md:10 states evidence_class source_static for a runtime claim; candidate-fixes.md:3 states shared diagnosis. Mitigation: tier1/RCA cards are log_evidence and the mechanism is observed in N8 |
| A6 | no | — | — | no Reference-context value; first_instrumented_run {} |
| A7 | no | — | — | RUN-SITE resolved (execution-locus.md:4); producers.md has P1 |
| A8 | no | — | — | OBSERVE-VIA same-shell; not a CI job |
| A9 | no | — | — | no literal Reference-context value |
| A10 | no | — | — | capability-verdict n/a |

## Notes (claim-level, not citations)

1. "2-3 s after the create" is not true for all 7: gh-pin-latest ~1-2 s; orca-idle-sleep ~10 s; others ~2-4 s; fix-flaky 2.3 s. Suggest "within about 1 to 10 s" (also in Diagnosability Context).
2. "5 handed work ... in a separate new tab (Evidence 7)": N1 leaves seeded vs new unsettled for 4 of them and lists af4401a8 as a supervised worker; "separate" is settled by N8 (Evidence 6). Cite 6 and 7 together.
3. "worktrees whose create carried an agent have no such row (Evidence 9)": only issue-473-claim has a known creation path, via `worker-start --agent claude`, not `worktree create --agent`; issue-331 and sc-issue-claim-pipeline-flag creation not captured; 1779a921 agent create not checked in daemon log. n=1; soften.
4. Evidence 2 is narrower: callerProvidesInitialSurface also needs activate !== true and runHooks !== true (:266-267); the :202 seed branch runs only when no activate/setup/defaultTabs/startup applies (:149, :187); setup/default-tab creates seed through provisioning (not cited). The fix's guards fit that structure.
5. Evidence 4: workspace-creation.ts returns a startupTerminal handle at :279-290 only when didSpawnStartup; the seed branch discards its result (:210) and sets neither; extend range to :290.
6. `superclaude update` force-install: main.py:340 defines update, main.py:365 calls install_core_files(force=True); suggest adding next to Evidence 12.
7. Other tokens checked and holding: test_fo18_exact_commands_and_no_forbidden_flag at tests/skills/test_issue_orca_worktree.py:794; FO-18 docs/designs/sc-issue-claim-pipeline-flag.md:333; D2 :370; WC-13 WORKER-CONTRACT.md:62; orca_worktree.py exists; test_claude_md_routing_block.py exists; terminal close/list usage matches N3; both proposed pinned phrases are literal substrings of the proposed append text.
8. A1 judgment: strict reading would add one partial contribution (same as current).
9. A5 judgment: same partial outcome either way.
10. Zero drops: all citations point at stable files and matched on Read.

Not checked: no commands re-run; installed Orca vs checkout; daemon rows and transcripts read only via tier1-observation.md.
