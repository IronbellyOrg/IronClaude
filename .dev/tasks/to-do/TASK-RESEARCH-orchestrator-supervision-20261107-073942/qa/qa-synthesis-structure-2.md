# QA Report — Synthesis Gate, Structure Lens (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Date:** 2026-11-07
**Phase:** synthesis-gate (structure lens, checklist items 1-6)
**Fix cycle:** N/A
**Fix authorization:** false (report only; no synthesis file modified)
**Assigned files:** `synthesis/synth-04-options-recommendation.md`, `synthesis/synth-05-implementation-plan.md`, `synthesis/synth-06-questions-evidence.md`
**Extra executor check:** NB-4 re-check (read-only Orca allowlist must allow `task-list`, `run-list`, `run-current`, `gate-list`; `inbox` still forbidden)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers | PASS | synth-04: `## 6. Options Analysis`, `## 7. Recommendation`. synth-05: `## 8. Implementation Plan` (8.1-8.5 plus Integration Checklist). synth-06: `## 9. Open Questions` (9.1-9.7), `## 10. Evidence Trail`. Read with offset/limit. |
| 2 | Table columns | PASS | synth-04 Options Comparison: Criterion / A1 / A2 / A3 (A4 is rejected and described on its own). synth-05 step tables: Step / Action / Files / Details (steps 1.1-1.29). synth-06 open-question tables have impact and resolution columns. |
| 3 | No fabrication (every claim traced) | FAIL | Three claims are false or have no source (I-1, I-2, I-3). The code cites I spot-checked all resolve: WORKER-CONTRACT.md :23, :45, :58, :60, :61, :74, :108, :126-129, :131-136, :154-158; test_worker_contract.py 86-92, 245-254, ~379, 398-404, ~446, 464-472, 1090-1094, ~1098, ~1166; main.py 555-565; test_routing_refresh.py :33, :647-648; HOW-WE-WORK.md :314, :318, :337, :396; test_how_we_work_routing_table.py 27-40, 291-311, 342-347; test_routing_plugin_parity.py:38; Makefile :362, ~465-476; pyproject.toml 203-206; seed-brief.md :53, :57. |
| 4 | Actual file paths | PASS | Every existing file the plan names resolves. New files have an existing parent directory: `src/superclaude/cli/`, `src/superclaude/commands/`, `src/superclaude/skills/` and `tests/cli/` all exist (checked with `ls -d`). |
| 5 | Two or more options with pros and cons | PASS | synth-04 has A1-A4. Each has a description, an ASCII flow and an Aspect table (Effort, Risk, Reuse, Files, Pros, Cons). A1 is recommended against the comparison table. |
| 6 | Implementation plan names specific files | PASS | synth-05 steps 1.1-1.29 each name file paths plus functions or constants (`NEVER_AS_WORKER`, `RULE_PHRASES`, `_POST_REFRESH_ADDITIONS`, `_OTHER_COMMANDS`, `AUDIT_ROOTS`, `WRITE_VERB_CLASSIFICATION`, the `main.py` deferred import). |
| X | NB-4 re-check (executor extra) | PASS | The corrected allowlist, with `inbox` forbidden, appears at synth-04:18, K-5 (:34) and :62; synth-05:9, step 1.4 and the step 1.10 negative cases; synth-06:11 and row 39. No text in the three files uses the old allowlist (`task-list`, `run-list`, `run-current` or `gate-list` listed as forbidden). |

## Summary

- Checks passed: 6 / 7 (items 1, 2, 4, 5, 6 and the NB-4 extra)
- Checks failed: 1 (item 3, no fabrication)
- Critical issues: 0
- Important (blocking) issues: 3
- Minor issues (notes): 5
- Issues fixed in-place: 0 (fix_authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | synth-04 §7 Contradictions table, X-6 (line 220); synth-05 §8.4 X-6 (line 260) and the "stale count" row at line 206 | These rows say `gaps-and-questions.md:125` "still says Open: 76. Resolved: 24" with GQ-03 open. The file now reads "100 rows. Open: 75. Resolved: 25 ... Open blocking QA finding: none; GQ-03 (NB-4) was fixed". The claim is false against the current source. synth-06:13 already has the correct 75/25. | Remove X-6 from both files, or rewrite it to say the :125 counts are current (75 open, 25 resolved, GQ-03 resolved). Remove the stale-count item from synth-05:206. |
| I-2 | IMPORTANT | synth-06 §9.1 row 17 (GQ-22), line 45 | The resolution reads "Measure once; keep it [`--include-remote`] off by default". This contradicts the research and the plan:<br>- research `scope-02:121`: "always pass `--include-remote`; unverifiable remote rows go to 'could not determine'"<br>- `05-orca-row-schema:21,66`: the guide uses `worker-list --include-remote --json`<br>- the plan passes the flag (synth-04:60, synth-05 step 1.4) | Change row 17 to: always pass `--include-remote`, because remote rows otherwise read as unverifiable. The flag's cost stays [UNVERIFIED]; measure it once. |
| I-3 | IMPORTANT | synth-05 §8 step 1.19, line 92 | The step makes two errors:<br>- It says "add `sweep` to `NEVER_AS_WORKER`". The tuple uses the `/sc:` form, so the entry is `/sc:sweep`.<br>- It says `_check_never_as_worker` (`:398-404`) "then checks `sweep.md`". The function only checks that each tuple entry appears in backticks on the single `**Never-as-worker list**` line of WORKER-CONTRACT.md (test_worker_contract.py:398-404; research scope-01:96). No research file says it reads `sweep.md`.<br>The step also leaves out that `RULE_PHRASES["never-as-worker"]` (:86-92) pins the full list sentence, so it must change in the same edit (scope-01:96). | Rewrite step 1.19:<br>- add `"/sc:sweep"` to `NEVER_AS_WORKER`<br>- state that `_check_never_as_worker` then requires `` `/sc:sweep` `` on WORKER-CONTRACT.md:23<br>- update the `never-as-worker` phrase in `RULE_PHRASES` in the same change |
| M-1 | MINOR | synth-06 row 27 (GQ-32) vs synth-05 step 1.5 | Row 27 sets the scope line to "the window and the Run ids". Step 1.5 prints the root path, which matches research scope-04 open question 5. | Align row 27 with step 1.5: the root path, with the window added if wanted. |
| M-2 | MINOR | synth-06 row 21 (GQ-26), line 49 vs synth-05 step 1.15 | Row 21 uses the colon form `Bash(superclaude sweep:*)`; step 1.15 uses the space form `Bash(superclaude sweep *)`. | Use one form in both. |
| M-3 | MINOR | synth-06 §10 line 221 | Lists synth-05 as "planned; not yet written", but synth-05 exists (309 lines). | Mark synth-05 as written. |
| M-4 | MINOR | synth-06 §10 line 230 | Says "qa/ (24 files)". qa/ now holds 35 files, including the reports this gate is writing. | Recount at assembly. |
| M-5 | MINOR | synth-04 §6, A3 risk text | Tags as [UNVERIFIED] whether lint check 11 scans skill scripts. This can be answered: Makefile Check 11 (~465-476) passes `--scan-paths src/superclaude/cli/` only. | Replace the tag with the fact: skill scripts are not scanned. |

## Actions Taken

None. fix_authorization is false. I modified no synthesis or research file. The synthesis mtimes (synth-04 20:28, synth-05 20:46, synth-06 20:43 UTC) are all earlier than this report's creation (20:48). I re-checked I-1 to I-3 against the current files after that.

## Recommendations

- Fix I-1, I-2 and I-3 in the synthesis files, then re-run this partition's gate (fix cycle 1).
- Apply M-1 to M-5 at assembly. They do not block.
- Merge this report with partition 1's. The cross-file checks here covered only synth-04, synth-05 and synth-06.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 7 | Glob: 1 | Bash: 3 (plus Write: 1, Edit: 1). No web research was performed.
- Unchecked items: none. Unverifiable items: none.

## QA Complete

## Verdict: FAIL
