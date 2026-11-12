# Refactor Plan Review 2 (Step 4, analytical reviewer)

Under review: `refactor-plan.md` after the fixes for B1 to B4 of `refactor-plan-review.md`.
Date: 2026-11-08.

## Verdict: FAIL

The fixes for B1 to B4 hold, and every citation in the fixed text matches its source. One new blocking finding (N1) remains: Change 13 says every run writes a new file, which contradicts the exit-2 no-report rule that Change 3 adds. There are also 8 minor findings (m1 to m8).

## Status of B1 to B4

| ID | Fixed? | Evidence |
|----|--------|----------|
| B1 | Yes | Change 3(d) (plan:37) now rewrites the V1:257 row. Its detection becomes "zero-exit `run-current` with the captured no-binding shape (UNVERIFIED until step 1.0a) and no `--run`", its behaviour becomes "`no Run bound: pass --run <id>`, no report, no success JSON (FR-002)", and its exit stays 2. It also says an empty body is `unavailable` on the first call and still exits 2 with the Orca-unavailable message. V3R3:32 says `no_binding` applies "never to an empty body", that empty stdout is an invalid response, that an invalid response on the first call is unavailable, and that the shapes are "UNVERIFIED until step 1.0a". V3R3:31 gives both exit-2 messages and "Neither case writes a report or success JSON". The citations match. |
| B2 | Yes | Change 3(b) adds a fourth required test, gated on step 1.0a. It uses a captured no-binding fixture with zero exit and no `--run`, and checks exit 2, the `no Run bound` text, no report, no success JSON, and no `worker-list` or `worker-show` argv. That last check comes from V1:52. The cited V1R3:22 says "If the lookup succeeds and shows no binding, it exits 2 with `no Run bound: pass --run <id>`". Change 4 (plan:44) adds "a fixture of the captured no-binding JSON classified `no_binding`, gated on step 1.0a (V1R3:23)". V1R3:23 has "a fixture of the captured no-binding JSON asserts `no_binding`", and says that shape "is fixed by the step 1.0a capture". Change 4 also adds the empty-body case classified `unavailable`, cited to V3R3:32, which supports it. |
| B3 | Yes | Change 22 (plan:170) now has one marked real-git test with four assertions: the control (V2:98), the positive `check-ignore` (V1:75), the negative `check-ignore` (Change 35), and status unchanged (V1:75). It amends V1:75 so the FR-025 checks run inside that test. NFR-001 and NFR-013 (V1:81, V1:93) are patched everywhere except "this one marked test". The rationale cites debate-transcript.md:195 (X-010 "as one isolated real-git test") and :221 (A-017 "one isolated real-git test allowed"), and both lines match. Change 35's Risk line (plan:262) and Risk Summary rows 22 and 35 (plan:373, :386) agree. Wording problems remain in m3, m4 and m5. |
| B4 | Yes | Change 30 (plan:226) keeps V1:167 unchanged and says "`unknown` is not added to FR-013". Its rationale cites debate-transcript.md:148 (C-006) and :191 (X-006), and both lines match. A new "not being made" row (plan:345) records the dropped idea. Its claims are correct: V2:160-168 lists five states with no `unknown`, and V2:168 blocks only states 1 to 4. The Risk Summary row for Change 30 (plan:381) no longer mentions `unknown`. A gap in its rollback remains in m6. |

## Findings

| ID | Severity | Location | Issue | Fix |
|----|----------|----------|-------|-----|
| N1 | blocking | Change 13 integration point (plan:107); Change 3(a) (plan:37); Change 40 (plan:296) | Change 13 adds the requirement "every run writes a new file". Change 3(a) adds "Neither case writes a report or success JSON" for both exit-2 cases without `--run`, and V1:266 still has the exit-1 write failure that writes no report. Change 40 puts both rules into the same new "CLI contract and re-run idempotency" section, so the merged spec would state both side by side. The plan's sentence paraphrases V3:180 ("each invocation deliberately preserves a new observation"), where the context is not sharing one path. V3:164 qualifies it with "Exit 2 ... no report is required". The plan drops that qualification. | Reword it as "every run that publishes a report writes a new file; it never reuses or overwrites an earlier path. A run that exits 1 or 2 writes no report (Change 3)." Alternatively, keep V3:180's wording with the V3:164 sentence. |
| m1 | minor | Change 4 Risk (plan:45) | The Risk line still says "New seam behaviour with three tests". After the B2 fix, Change 4 adds five ACs: the unavailable causes, the middle `worker-show`, the later malformed body, the `no_binding` fixture, and the empty body. | Change the line to five ACs, or drop the count. |
| m2 | minor | Change 3(b) (plan:37) | "Only the last two publish (V3R3:31)" comes before the new fourth test. If the executor copies the tests in order, "the last two" reads as tests 3 and 4, and test 4 does not publish. | Name them instead: "Only the explicit-Run and established-binding tests publish." |
| m3 | minor | Change 22 (plan:170); V2:98 | V2:98 skips the whole test as inconclusive when the control shows no rewrite. Change 22 says "only this assertion is reported as inconclusive", but one pytest test has only one outcome. If the control runs first and skips, the two `check-ignore` assertions and the status check never run, so a skip could hide them. | Say the `check-ignore` and status assertions run before the control, and that an inconclusive control then skips the test. Or state another mechanism that keeps their results visible. |
| m4 | minor | Change 22 assertion (4) (plan:170); V1:75 | V1:75 says "a sweep leaves `git status --porcelain` unchanged". Change 22 says "writing a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged" and still cites V1:75. The plan narrows the check without saying so. | Either keep V1's wording (run the sweep, with the seams other than git patched) or say that this is a narrowing of V1:75. |
| m5 | minor | Change 35 (plan:261-262) vs Change 22 (plan:170) | Only Change 35's Risk field says the negative `check-ignore` runs inside the marked test. Its integration point, which the executor applies, just appends the check to FR-025, and Change 22 assertion (3) already adds the same check. The executor gets the same check twice, and the "one test" placement is not in the integration point. | Put the sentence in Change 35's integration point, and say the check is already assertion (3) of the Change 22 test, so FR-025 only refers to it. |
| m6 | minor | Change 30 Target (plan:224); Risk Summary row 30 (plan:381) | Change 30 now edits V1:164 and FR-013 (V1:63), but its rollback only says "Restore V1:164". Its Target still says "package-state table V1:158-167 ... (replace)", although the integration point keeps every row except V1:164. | Rollback: "Restore V1:164 and remove `archive-blocked` from FR-013". Target: name V1:164 and V1:63 only. |
| m7 | minor | V1:240 (WC-14), V1:72 (FR-022), V1:117 (B4) | With Change 3, an Orca outage without `--run` exits 2 with no report and no JSON. That is a common case, not only a misconfiguration. WC-14 says the coordinator "runs `/sc:sweep` and reads its report before it acts". B4 and FR-022 say the skill reads the report path from JSON. No change says what the skill or coordinator does on exit 2. V1 already had exit 2 for a missing binding, so this is a gap, not a direct contradiction. | Add one sentence to FR-022: on exit 2 the skill shows the stderr message and says to re-run with `--run <id>` (V1R3:22: "The person gets the full degraded report by passing `--run`"). |
| m8 | minor | V1:264; Change 41 (plan:303); Change 4 (V3R3:32) | V1:264's detection is "Key missing in JSON", and the field then stays `unknown` with exit 0. INV-002 treats JSON that "cannot establish the operation's captured success ... shape" as an invalid response, which is `call_failed` later in the run. Change 41 calls V1:264 the "unknown schema field" row, but V1:264 is about a missing key, not an extra one. Exit 2 without `--run` is not affected, because rows are read only after a binding exists. | State that V1:264 covers optional keys only, and that a missing key in the captured success shape follows Change 4. |

## Self-Audit

Every file was read in chunks of 150 lines or fewer. `refactor-plan.md` was not edited. The minor findings of review 1 (M1 to M12) were not rechecked.

1. **Files read.** `refactor-plan.md` lines 1-401 (whole). `refactor-plan-review.md` (whole). `variant-1-opus-architect.md` lines 1-333 (whole). `debate/round3-final-v3.md` lines 25-64, which include 31-34. `debate/round3-final-v1.md` lines 1-68 (whole). `variant-3-haiku-backend.md` lines 158-189. `variant-2-opus-analyzer.md` lines 90-101 and 158-169. `debate-transcript.md` and `diff-analysis.md` were grepped for C-006, C-011, X-006, X-010 and A-017, and the matching lines were read.
2. **Check 1, fixes and citations.** All four fixes are in place (table above). These citations were checked against their source lines and match: V3R3:31, V3R3:32, V1R3:22, V1R3:23, V1:52, V1:75, V1:81, V1:93, V1:63, V1:164, V1:167, V2:93, V2:98, V2:160-168, and debate-transcript.md:148, :191, :195 and :221.
3. **Check 2, new contradictions.**
   - Change 3 vs Change 4: consistent. The empty body is `unavailable` in both, `no_binding` needs the captured shape in both, and both gate the no-binding test on step 1.0a. They overlap: Change 3(b) tests the exit code and message, and Change 4 tests the classification. That overlap is acceptable.
   - Change 22 vs Change 35: no contradiction on the number of real-git tests. The wording problems are m3, m4 and m5.
   - Change 30 vs the "not being made" row and the Risk Summary: consistent on `unknown`. The rollback gap is m6.
   - Outside the named pairs, Change 13 contradicts Change 3 (N1).
4. **Check 3, V1 passages about exit 2 without `--run`.** A grep of V1 for "exit 0", "exit code", "--run", "No Run bound", "exit 2", "run-current", "Orca down" and "unavailable" found these lines:
   - V1:51 is the `--help` exit 0, which is unaffected.
   - V1:52 is covered by Change 3(a) and (b).
   - V1:53 and V1:54 are other exit-2 usage errors, which are consistent.
   - V1:68 is covered by Change 3(c).
   - V1:69 is covered by Change 3(a) and (b).
   - V1:256 and V1:257 are covered by Change 3(d).
   - V1:266 is covered by Change 3(d).
   - V1:294 (GQ-104) is consistent.
   - V1:40, V1:186 and V1:234 are neutral.

   No V1 passage that contradicts exit 2 without `--run` is left uncovered. V1:240, V1:72 and V1:117 assume a report exists, which is the gap in m7. V1:264 is the gap in m8.
5. **Not checked.** `base-selection.md`, `invariant-probe.md`, `convergence-tracking.md` and the V2R3 file were not re-read. Citations to them in the fixed text (Conv:273, V2R3:25) were not rechecked.
