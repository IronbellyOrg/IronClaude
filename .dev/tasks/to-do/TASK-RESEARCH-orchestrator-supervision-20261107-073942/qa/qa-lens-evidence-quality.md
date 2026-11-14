# QA Report — Report Lens: Evidence Quality

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Date:** 2026-11-07
**Phase:** report-lens-evidence-quality (report-validation, single dimension)
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Fix authorization:** false (report only; no file other than this one edited)

---

## Evidence-Quality QA Report

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| I1 | IMPORTANT | Section 5 (lines 637, 678, 688, 706, 729, 742, 803) | Rule (d) is broken. Lines 637, 729 and 803 call the liveness-verdict text at `.dev/orca-command-refactor/inventory/orca-capabilities.md:122-130` a "verified codebase rule" and "the codebase". Those lines are Orca guide quotes (`[G]`, `[G:recovery]`) and help-text quotes (`[H:worker-show]`), not code. Lines 678, 688, 706 and 742 cite `:122`-`:130` with no guide or UNVERIFIED tag. Line 729 also says `host_unavailable` is at `:125`, but it is at `:124` (`:125` lists missing_status, stale_status, restored_unconfirmed and remote). | Tag every one of these citations `[UNVERIFIED — Orca guide]` (or `[G]`). Keep `WORKER-CONTRACT.md:45` (WC-10) as the only codebase rule. Change `host_unavailable` to cite `:124`. |
| I2 | IMPORTANT | Section 2 (line 104); Section 7 X-4 (line 1062) | The labels mix help text with code. Line 104 says "[CODE-VERIFIED as help text]" and line 1062 says "the help is code-verified text". CLI help output is not a code trace, and the evidence taxonomy keeps CODE-VERIFIED for claims checked against source. | Relabel as `[HELP-TEXT]` or `[UNVERIFIED — help text]`. Use CODE-VERIFIED only where a handler under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/` was read. |
| I3 | IMPORTANT | Sections 4 and 8 (lines 383, 451, 499) | The citation is false. These lines cite WC-11 (`src/superclaude/core/WORKER-CONTRACT.md:46`) as the basis for writing the supervision report under `.dev/`. Line `:46` is "Parallel-safe writes": two workers must not write one file, and paths carry a timestamp or slug. It says nothing about `.dev/`. Line 499 itself says "No source fixes a location", which contradicts the citation. | Drop the `:46` citation for the location. Call `.dev/` a working default that is still open (GQ-10). Cite WC-11 only for the timestamp/slug naming rule. |
| I4 | IMPORTANT | Evidence Trail (line 1650) | A deliverable is incomplete. The trail says "`qa/` (24 files)" and lists only files from Phase 3 and earlier. `qa/` holds 54 files, or 43 without the 11 `qa-lens-*` files from this phase. The Phase 5 synthesis-gate files are missing: the analyst-synthesis-accuracy and tracing files, `qa-consolidated-findings-phase5` and its cycle-1 file, and 12 `qa-synthesis-*` files. This fails checklist item 10 (the trail lists every file produced). | Update the count and list the Phase 5 QA files, or state the count as of a named phase. |
| M1 | MINOR | Section 2 (line 88) | The Orca version `1.4.245-aidev02` has no citation. Its source shows up only in the Evidence Trail (line 1622, `07-gate-gap-fill`). | Cite `research/07-gate-gap-fill.md` with a line number inline. |
| M2 | MINOR | Sections 1-2 (lines 13, 36-38, 67, 82, 231, 434, 437, 934) | These cite a file but no line: `issue-summary.md` (36-38), `scope-01-contract.md` (67, 82), `qa-nb4-fix-log.md` (13), `scope-02` (934), "scope-01 test-pinning section" (434), "CLAUDE.md component sync" (437) and "20 headings" (231). This breaks rule (a), but spot checks found the claims true. | Add `:line` to each citation. |
| M3 | MINOR | Section 2 (lines 197, 228) | "14 of 46" (228) has no citation. The claim about the `python -m` docstring (197) names no file and line. | Cite the research file:line that counts the 14 of 46, and the docstring file:line. |
| M4 | MINOR | Sections 2, 5, 6, 8 (lines 125, 212-214, 338-340, 520, 522, 544, 878, 1229) | The Orca JS handler citations (`message-check-handler.js`, `task-handlers.js`) give the bare file name. The full path `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/` appears only at line 1622. I checked the content: the one-read-mode check is near `:17-19`, `callOrchestrationMutation` near `:30`, `compatibilityAck` near `:58-71`, and `task-list` near `:32`. | Give the full path the first time each handler is cited, or add a path legend. |
| M5 | MINOR | Sections 6, 8 (lines 525, 874-877) | `seed-brief.md`, `pragmatic.md` and `launch-job-identity.sh` are cited with no path. They are at `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md`, `src/superclaude/output-styles/pragmatic.md` and `src/superclaude/hooks/scripts/launch-job-identity.sh`. All three exist. | Use the full paths. |
| M6 | MINOR | Section 7 R-3 (line 1006) | "[CODE-VERIFIED bugs]" is cited only through `scope-02:228`. I confirmed the bugs directly in `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh`: `:31` encodes only `/`, `:73` tests `-d .git` (which misses worktrees), and about `:136` builds JSON with awk by hand. | Cite `bootstrap_scan.sh:31`, `:73` and `:136` directly. |
| M7 | MINOR | Section 8 (line 1198) | The SAFE/REVIEW labels are cited at `sc-crash-recovery/SKILL.md:91`. They are at `:90`. The claim is true; only the line number has moved. | Change to `:90`. |
| M8 | MINOR | [CONTRADICTION] at line 1078 | The HOW-WE-WORK range is cited as both `:314-337` and `:318-337`. Both are true: `:314` is the `## Other commands` heading and `:318` is the `<!-- other-commands:v1 -->` marker. The marker should stay. | When resolving it, use `:318-337` for the marker block and `:314` for the heading. |
| M9 | MINOR | [CONTRADICTION] at line 1507 (vs 1198, 1461) | Line 1198 writes the `allowed-tools` patterns as `Bash(git stash *)`, the space form used at `SKILL.md:4`. Line 1461 writes them in the colon form. The marker records this correctly. | When resolving it, use the space form, which matches the file. |
| M10 | MINOR | Evidence Trail (lines 1639-1640) | The list of synthesis files still says "planned; not yet written" and "this file". All of synth-01 to synth-06 exist. The assembler note corrects this, but the stale wording is still there. | Remove the stale wording. |
| M11 | MINOR | Sections 2-3 (lines 84, 179, 247, 267) | These claims cite through research files only ("all via research/..."), not the primary sources. I spot-checked them and they are true. | Add the primary file:line wherever the research file names it. |

Notes on items judged under this lens:
- The two [CONTRADICTION] markers (`:1078`, `:1507`) are surfaced correctly and should stay. Each can be resolved as M8 and M9 describe.
- The NB-4 gate exception is recorded with a citation to its fix log (`qa-nb4-fix-log.md`). This is acceptable evidence. The only defect is the missing line number (M2).
- Lines 390-395 that start with `## ` are mock output inside a code fence. They are not real headers and no finding was raised against them.

Checked and found true (no finding): `sc-crash-recovery/SKILL.md:25-27`; `WORKER-CONTRACT.md` is 203 lines; `cli/main.py:519/555/559/561/564-565`; 41 tests in `test_worker_contract.py` and its cited line anchors (`:163`, `:245-254`, `:379`, `:398`, `:446`, `:545`, `:1090-1094`, `:1098`, `:1166`); `test_routing_refresh.py:33/38-40`; `pyproject.toml:54` and `:203-206`; `Makefile:362` and `:467-476`; `install_core.py:27`; `ccsession` is 1975 lines; `05-orca-row-schema.md:167-178`; `sc-reflect-protocol/SKILL.md:63-64` (contract-status commands); `sc-swarm-wizard-protocol/SKILL.md:7` (allowed-tools); `docs/designs/sc-issue-command.md:384` ("No CLI"); the artifacts `lc16-show-4.json`, `lc17-show-1.json`, `lc01-show-1.json` and `lc01-step7.txt`; and the line counts of all 10 research files.

### Summary

| Checklist part | Result | Findings |
|---|---|---|
| (a) file:line, not a directory | PASS with notes | M1, M2, M3, M4, M5, M6, M7, M11 (format only; every claim checked was true) |
| (b) no unverified claim stated as fact | FAIL | I1, I2, I3 |
| (c) no hallucinated paths | PASS | None. Every path checked exists. M5 lists paths given without a directory. |
| (d) code evidence kept apart from doc evidence; Orca guide text not called verified | FAIL | I1, I2 |
| Evidence Trail completeness (supports a-d) | FAIL | I4, M10 |

- Counts: CRITICAL 0 | IMPORTANT 4 | MINOR 11 | Total 15
- Fixed in place: 0 (fix authorization false)

**Verdict: FAIL** (4 blocking findings: I1-I4)

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 16 | Grep: 2 | Glob: 0 | Bash: 5 (4 batched scripts, one of which had a failed `ls-tree` pathspec command)

Limitations (reported, not counted as unchecked parts): I could not read the #409 file contents at commit `495eb96d` that the report cites by line: `canvas.py:73-81`, the `agent_focus.py` lines, `data-dictionary.md` and `DESIGN-CONTRACT.md:11`. `git ls-tree` on the subpaths I tried printed nothing, so those line citations are still unverified by this lens. They could hide moved line numbers. A wrong path there would fall under check (c).

