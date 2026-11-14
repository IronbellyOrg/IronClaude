# Refactor Plan Review 3 (final review)

Under review: `refactor-plan.md` after the fix for N1 of `refactor-plan-review-2.md`.
Date: 2026-11-08.

## Verdict: FAIL

N1 is fixed for exit 2: Change 13 no longer says every run writes a file, and it now agrees with Change 3. But the fix adds a new requirement, "a run that exits 1 ... writes no report", that no cited source supports in full and that the merge would carry into the spec. That is one blocking finding (P1). There is one minor finding (p1).

Note: the exit-1 wording came from the fix that review 2 suggested for N1. The author applied that suggestion as written. The problem is in the suggestion, not in how it was applied.

## Status of N1

| ID | Fixed? | Evidence |
|----|--------|----------|
| N1 | Yes, for exit 2 | Change 13 (plan:107) now says "every run that publishes a report writes a new dated file and never reuses or overwrites an earlier path". Change 3(a) (plan:37) says that for both exit-2 cases without `--run`, "Neither case writes a report or success JSON" (verbatim from V3R3:31). Change 3(c) says exit 0 "means collection completed and the report was successfully published". So every run that publishes exits 0 and writes a new file, and the two exit-2 cases write none. The two rules no longer contradict each other. The AC "two report-publishing sweeps with the same injected `now` produce two files" is also consistent. The added exit-1 clause is a separate problem (P1). |

## Findings

| ID | Severity | Location | Issue | Fix |
|----|----------|----------|-------|-----|
| P1 | blocking | Change 13 integration point (plan:107); placed in Change 40's "CLI contract and re-run idempotency" section (plan:296) | The new clause "a run that exits 1 or 2 writes no report (Change 3; V3:164)" turns "exit 1 writes no report" into a spec requirement. The cited sources do not support it. (1) V3:164 is only about exit 2, and even there it says "no report is required", not "no report is written". (2) Change 3 says only "write failure exits 1 without success JSON" (V3R3:31) and that exit 1 covers "any report write failure" (plan:37(c)). It says nothing about a file on disk. (3) Only one exit-1 case has a source that says nothing is written: V1:265, an allowlist miss, "no report written". V1:266 (output dir not writable) says only "JSON not printed". (4) V3, the source Change 13 cites ("Add from V3:181-187"), allows for a leftover file. V3:182 reserves the final path exclusively, which creates the file before its content is written. V3:184 says "On handled write failure, remove only this invocation's incomplete output if it can be identified safely". V3:356 lists "full disk or partial write" as exit 1 with "no success JSON; preserve previous reports", not as "no file". (5) Nothing in the sources rules out an exit 1 after publication, for example a failure to print the success JSON once the report is written. The new clause would then require deleting a published report. As written, an executor would add a test asserting that no file exists after any exit 1. A partial write on a full disk, after the path is reserved, could not meet that test unless the code deleted files beyond what V3:184 allows. | Limit the no-report clause to exit 2 and restate exit 1 from its sources: "A run that exits 2 writes no report (Change 3; V3R3:31). A run that exits 1 prints no success JSON and never overwrites an earlier report (Change 3; V3R3:43). On a handled write failure it removes only its own incomplete output, and only if it can identify that output safely (V3:184). Any file left behind lacks the `Report complete` footer (V3:187)." Keep V1:265's "no report written" as it is, for the allowlist-miss row only. |
| p1 | minor | Change 8 INV-017 entry (plan:72); Change 9 (plan:79); Change 3(a) (plan:37) | INV-017 says that when `orca-ide` is missing, the failure "is visible as `binary not found: orca-ide`". Change 9 attaches that reason to the unavailable class. Without `--run`, though, Change 3(a) fixes the exit-2 stderr message verbatim as `Orca unavailable; no Run binding could be established: pass --run <id>`, and that message does not include the reason. In that case no report exists to carry the reason either. So no requirement makes the claim true on the no-`--run` path. This does not conflict with the no-report rule: "takes the outage path" covers both the exit-2 branch with no report and the `--run` branch with a degraded report. | In Change 9's failure row, also put the reason on stderr for exit 2 without `--run`, for example by appending `(binary not found: orca-ide)` to the Change 3 message. Or narrow INV-017 to "visible in the report coverage header when `--run` is passed; without `--run`, only the Orca-unavailable message appears". |

## Self-Audit

Every file was read in chunks of 150 lines or fewer. `refactor-plan.md` was not edited. The minor findings of reviews 1 and 2 (M1 to M12, m1 to m8) were not rechecked.

1. **Files read.** `refactor-plan.md` lines 33-114 (Changes 3 to 14) and 290-298 (Change 40). Line 219 (Change 29) was printed through Bash because it mentions a partial report. `refactor-plan-review-2.md` lines 1-57. `variant-3-haiku-backend.md` lines 150-190. `debate/round3-final-v3.md` lines 25-44, which include 31-34 and 43. `variant-1-opus-architect.md` lines 252-267.
2. **Check 1, N1.** Fixed for exit 2. See the N1 status table.
3. **Check 2, sources for "exit 1 writes no report".** V3:164 and V3R3:31-34 do not say it. V3R3:31 says only "write failure exits 1 without success JSON". V3R3:43 says "Failed publication exits 1 without success JSON or overwriting an earlier observation". Only V1:265 (allowlist miss) says no report is written. V3:182, :184, :186 and :356 allow incomplete output to remain. The clause is in Change 13's integration point, so the merge would carry it into the spec. Graded blocking (P1).
4. **Check 3, INV-017 (plan:72).** It does not conflict with Change 3 on writing a report. "Every sweep takes the outage path" is about which binary runs, and the outage path covers both the no-report and the degraded-report branches. Its visibility claim is not guaranteed without `--run` (p1).
5. **Check 4, grep.** I grepped the plan for "every run", "every sweep", "always writes", "exit 1" and "exits 1", and also for "each run", "each sweep", "each invocation", "writes no", "write nothing", "incomplete output" and "partial". Hits:
   - "every run": plan:107 only. It is the fixed text and is consistent.
   - "every sweep": plan:72 only (Check 3).
   - "always writes": no hits.
   - "exit 1" and "exits 1": plan:37 (Change 3, write failure without success JSON) is consistent. plan:44 is a `worker-show` exit code, not the sweep's exit code. plan:100 (Change 12, "Failed publication exits 1 without success JSON or overwriting an earlier observation") is consistent with Change 3, but it is weaker than plan:107's "writes no report"; this is part of P1. plan:107 is P1.
   - "write no": plan:198 (`--output` escape and overlap exit 2 and write nothing) is consistent with the exit-2 half.
   - "partial": plan:219 adds V3's process-killed row ("no partial report presented as complete"). A killed process does not exit 1, so this row does not conflict, but it confirms that the plan expects leftover files to be possible.
6. **Not checked.** `convergence-tracking.md`, `invariant-probe.md` and the V1R3 and V2R3 files were only grepped, not re-read. The citations they carry in Changes 3 and 12 were not rechecked.
