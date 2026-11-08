# QA Report: task-qualitative, lens qa-gate-sufficiency (rf-qa-qualitative)

**Date:** 2026-11-08. **fix_authorization:** false. **Provenance note:** the reviewing agent is barred from writing report files and returned the report in its message; the orchestrator saved the findings here (condensed, same findings, severities and fix text).

## Overall Verdict: FAIL

No gate has too few agents and no lens is generic; two gate-control defects remain.

## Items Reviewed (summary)

PASS: agent counts (A 6, B 6, C 6, D 6, Final 7, M4 3 = 34, tabulated by line from the 34 spawn items); agent-item shape (own item, embedded prompt, adversarial stance, report-only, report path under qa/); serialized fix and verification; cycle control (regression, then monotonicity, then 2-cycle cap; byte-exact strings, see MINOR-3); cycle-2 conditional items for every gate; lens quality (tailored per gate: security, no-shell, no-text, allowlist, lock/at-most-once are covered); placement (A after P3, B after P5, C after P7, D after P8, Final then M4 in P9, none after P1 or P10); M4 prompts read both sources and the code and carry the 29-row DEVIATION list; the POST reflect item matches SKILL.md 2221-2229 and is a dedicated subagent with an on-disk EV-3 check; BUILD_REQUEST requirements are encoded; effort and unattended safety are realistic; all 21 cited gate-result files have a writer step; `make lint` passes on the current tree (EXIT=0).
FAIL: row 6 (NEEDS OWNER DECISION handling in M4), row 7 (post-fix re-run consequence and coverage).

## Issues

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| 1 | IMPORTANT | Steps 9.M6, 9.M7, 9.M8, 9.M11, 9.M12, 9.M13 | A blocking finding marked NEEDS OWNER DECISION can pass the M4 gate: the cross-source agent's new blocking contradictions can only end that way (the fix agent may not edit D or S), the verifier prompts count a fix report that says "needs owner decision" as acceptable, 9.M8 writes PASS when both verification reports say PASS and tests NEEDS OWNER DECISION only inside the FAIL branch, 9.M13 has the same ordering, and Step 10.7 checks only the Open Questions section, not `qa/m4/`. This breaks "never pass open blocking findings" | In the 9.M6, 9.M7, 9.M11, 9.M12 prompts append: "A row marked NEEDS OWNER DECISION is an open blocking finding. While any such row exists the verdict is FAIL." In Step 9.M8 begin the action with: "FIRST: IF the consolidated findings or `qa-fidelity-fix-report.md` mark any blocking finding NEEDS OWNER DECISION, the gate is NOT passed whatever the two verification verdicts say; go directly to the halt guards below (the PASS branch is unavailable while such a finding is open)." Put the same sentence before the PASS branch in Step 9.M13 |
| 2 | IMPORTANT | Steps 3.G12, 3.G17, 5.G12, 5.G17, 7.G12, 7.G17, 8.G12, 8.G17, 9.F13, 9.F18, 9.M8, 9.M13; Step 10.1 | The post-fix re-run (pytest, make lint, pinned ruff) has no failure branch (the verdict is written PASS first and the output only "recorded"); Step 10.1 writes a PASS/FAIL table but does not halt on FAIL; for the Final and M4 fixes the re-run list omits G-3 (xdist, zero skips), G-7, G-8, G-11 and the Step 9.3 runbook rules, and the M4 verifiers check only pytest, ruff and imports | Append to every post-fix re-run clause listed: "IF any re-run command fails, fix the cause in files this task created or edited (never weaken an assertion) and re-run until it passes, recording each fix; IF it cannot be made to pass, HALT, write the failing output to the Task Log and do not release the next phase." In Steps 9.F13, 9.F18, 9.M8 and 9.M13 replace the re-run of pytest/make lint/ruff by: "re-run Steps 9.4 to 9.16 (G-1 to G-11) in order, with Step 9.3 first when `docs/designs/issue-watcher-setup.md` changed, overwriting the `p9-*` files". Append to Step 10.1: "IF the cited test run or any p9 gate file shows a failure, mark the check FAIL and HALT before Step 10.2." |
| 3 | MINOR | the 8 regression strings | The task uses a comma (`Regression detected on Item X.Y, previously PASS ...`); SKILL.md:1293 uses an em dash, `rf-qa.md:409` and `rf-task-builder.md:417` use a comma | Note only; optionally record in Deviations from Process |
| 4 | MINOR | consolidation items 3.G8, 5.G8, 7.G8, 8.G8, 9.F9, 9.M4 | No unique finding ids across merged lens tables | Append: "give every deduplicated finding a unique id (A-1, A-2, ... for Gate A; B-, C-, D-, F-, M- for the others) and keep the same ids in cycle 2" |
| 5 | MINOR | Step 9.M3 | The cross-source agent classifies against "the 29 authorized departures"; DEVIATION = no decisions such as DF-54 could be called NEW blocking | Change to "covered by any decision DF-01 to DF-60" |
| 6 | MINOR | test-adequacy lenses | "Would fail" is by mental mutation only (agents are report-only) | Optional: allow a scratch copy under /tmp for mutation checks |
| 7 | MINOR | M4 header, DF-08 | Template I21/M4 calls for 3-4 fidelity agents plus the cross-source agent; accepted at 3 total (BUILD_REQUEST, SKILL.md 1151); DF-08 carries stale "M4 (2)" text | Optional: split the design agent into two ranges for 4 |
| 8 | MINOR | `qa_intensity: standard` | I22 describes standard for outputs of about 300-1,500 lines; this change set is larger | Note only |
| 9 | MINOR | /task skill rule 11 | Phases 2, 4 and 6 end with no gate of their own; an executor could add duplicate gates | Optional: add "Gate A/B/C is this phase's boundary gate; add no additional automatic gate" to those headers |

## Self-Audit

(a) Relied on the rf-qa PASS rows for gate totals, cycle-2 item existence, POST position, phase structure, counts, TB-Add-4, DF coverage and Open Questions integrity. (b) Independent checks: extracted and read all 34 spawn items; compared the halt strings with SKILL.md 1293, rf-qa.md:409, rf-task-builder.md:417 and tests/audit/_halt_emitter.py:66; compared the POST prompt with SKILL.md 2221-2229; counted the 29 DEVIATION ids in four M4 prompts against DF-40; read 9.M6/9.M7/9.M8/9.M13 together (found IMPORTANT-1) and 3.G12/9.F13 against 10.1 (found IMPORTANT-2); verified 21 result files have one writer step; ran `make lint` (EXIT=0).

VERDICT: FAIL
