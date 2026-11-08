| Status | Result |
|---|---|
| DONE | Read the diff analysis, all three Round-1 statements and both Round-2 rebuttals, then re-read the disputed source lines. |
| NEXT | Final merge by the orchestrator. I wrote no files and ran no tests. |

## Round 2 rebuttal, Variant 3

**Answers to the criticisms of Variant 3**

1. **X-001, the crash exit.** I concede on category. Under the strict rule, Drift ("contradicts nothing") is the wrong label.
   - `_EXIT_CRASH = 1` (`cli.py:35`, used at `:124-129`) is not in the `once` exit list: "0, 2, 3, 4, 5, 6, 7, 75" (design `:114`).
   - AC-17 says "Each verb's exit codes match section 4" (design `:890`).
   - The register says outright that "no R-003 row authorizes" it (deviation-register.md:43).
   - The design does require a crash fallback (`:722`) but gives it no exit code. That lowers the severity. It does not change the category.
   - Final: Regression LOW, non-blocking. The fix is to amend design `:114`.
2. **Wrong path in row 11.** Conceded again. The registration is at `src/superclaude/cli/main.py:563-565`. It is planned in research/06:208 (DF-29), so the row stays Authorized.
3. **Hedged categories.** I have collapsed them into a single label per row. X-002 and X-010 are one root issue. The table has 59 names (`test_audit.py:215-219`), but task `:199` says "exactly 57 entries" and design `:718` says `REASONS` is "equal to the spec's reason table". Both are Regression LOW. X-010 is not a separate defect.
4. **Rows 8 and 10 "closer to aligned".** Accepted. I hold row 10 (X-004) as Necessary, citing design `:237` and `:240` via the diff analysis. I did not re-read them.
5. **Row 6(c) against design `:726`.** The task settles this. The status command must exit "0 healthy, 1 unhealthy, 2 config invalid, 6 store unreadable" (task `:498`, which matches design `:115`).
   - Design `:726` and runbook `issue-watcher-setup.md:432` both leave out exit 2.
   - So C-034 is a documentation omission, not a code defect.

**Updated view of the other variants**

- **V2's strongest point holds.** AC-19 is a real acceptance criterion, and the code contradicts it. I was wrong to weigh impact as if it decided whether the work can be approved.
- **V1 is right that severity is low.** My reasons stand: a local fsync, about 241 s of the 300 s cadence, the lock, and at-most-once still holding.
- **V2 is also right on C-026 and C-036 under the strict rule.**
  - C-026: the design's "anywhere in stdout or stderr" rule (`:634`) can be met together with the 500-byte cap: search before truncating. So the cap does not force the gap.
  - C-036: design `:739` defines `retry` as "`unknown` entries with an `operation_id`". Validation accepts a null `launch_cwd` (`record.py:184`), so a valid store can still lose a retry line.
- **V2 has dropped Regression for C-017, and I agree.** The task prescribes `os.stat`.

## Late launch (C-014 / X-007): final position

- **Category and severity:** Regression, LOW severity, **blocking**. I still back Regression, now with every variant agreeing on the category.
- **What it contradicts:**
  - AC-19, design `:892`: "A sleeping stub ends with `gh_timeout`; no launch starts after 120 s".
  - FR-029, `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md:199`: "No launch starts after 120 s."
  - Design `:647`: "not started when `elapsed() > 120`; the step ends with no entry".
- **The code path:** the last cut-off check is at `cycle.py:1048`. Then come `mark_pending` (`:1060`), the fsync'd save (`:1061`) and an unconditional `launcher.launch` (`:1062`). `launch_allowed()` is `elapsed() <= 120` (`cycle.py:410-412`).
- **Why I changed to blocking:** an acceptance criterion with a direct counterexample should not be approved as met. A Gate C fix already tried to close this exact property (task `:901`). Low impact sets the severity, not whether it blocks.
- **A compatible fix exists:**
  1. Keep `prev = self.doc`. `mark_pending` returns a new document built with `replace` and `_with_entry` (`record.py:554-568`), so `prev` is not changed by it.
  2. After `_save()`, re-check the cut-off.
  3. On failure, restore `prev`, save again, then `raise _Skip("budget_exhausted")`.
- **What the fix gives:**
  - The step ends with "no entry (or `failed`)", which is crash point C1 (design `:527`).
  - If the restore save fails, the entry is left in crash state C3, which becomes `pending_orphan` with no launch (`:529`).
  - The save stays durable before any spawn.
- **Test to add:** a clock that passes 120 s inside `store.save`. It should assert no launcher call, the restored entry, and a `budget_exhausted` decision line.

## What blocks approval

- **Blocks approval:** only C-014 / X-007.
- **Must be fixed before the task is closed, but does not block:** X-006 / C-013, the skips. They break task `:188` ("No test may use `pytest.skip`, `skipif` or `xfail`"), so they are Regression MEDIUM. They are MEDIUM because `NOT_ROOT` (`test_cli.py:1070`) silently skips the file-mode security tests when the suite runs as root. They do not block because every recorded gate run had zero skips (task `:908`).
- **Everything else:** non-blocking documentation or test-hygiene findings.

## UPDATED POINT TABLE

| Point | Final classification | Backs | Conf. | Evidence | Changed |
|---|---|---|---|---|---|
| X-001 | Regression LOW, non-blocking (design gives a crash no code) | V2 | 65% | `cli.py:35`, `:124-129`; design `:114`, `:890`, `:722`; register `:43` | Yes |
| X-002 | Regression LOW, non-blocking (same root issue as X-010) | V2 | 65% | task `:199`; design `:718`; `test_audit.py:215-219` | Yes |
| X-003 | Authorized for 3 functions and the type; Regression LOW for `valid_operation_id` | V2 | 60% | task `:332`; `record.py:23-29`, `:183`; design `:239` | Yes |
| X-004 | Necessary LOW; parity test advised | V3 | 80% | design `:237-240` (from the diff analysis); `launch.py:30` | No |
| X-005 | Authorized LOW | none | 88% | task `:193`; `runner.py:89` | No |
| X-006 | Regression MEDIUM, fix before closing the task, not blocking | V2 (category) | 72% | task `:188`, `:908`; `test_cli.py:1070` | Yes |
| X-007 | Regression LOW, **blocking** | V2 | 75% | `cycle.py:1048-1062`, `:410-412`; design `:892`, `:647` | Yes (now blocking) |
| X-008 | Advisory LOW (option parsing unverified) | V3 | 65% | `launch.py:36`, `:119-132` | No |
| X-009 | Not a defect | V3 | 88% | `cycle.py:693`, `:1033-1034` | No |
| X-010 | Same finding as X-002 (Regression LOW) | V2 | 65% | task `:199`; setup `:344` | Yes |
| C-014 | Regression LOW, **blocking**; fix with snapshot and restore | V2 | 75% | `cycle.py:1060-1062`; `record.py:554-568`; design `:527-529`, `:647` | Yes |
| C-013 | Same as X-006 | V2 (category) | 72% | task `:188`; `test_cli.py:1070` | Yes |
| C-016 | Advisory LOW; matches the design | V1 | 70% | `record.py:689-703` | No |
| C-017 | Advisory LOW (runbook claims more than the code does) | V1/V3 | 75% | `record.py:421-431`; setup `:296`, `:301` | No |
| C-018 | Advisory LOW | V1 | 70% | `cycle.py:685-690` | No |
| C-019 | Advisory, unverified | V1 | 50% | `runner.py:91-101` | No |
| C-024 | Advisory LOW-MEDIUM; matches the design; reply shape unverified | V1 | 65% | design `:633`, `:636`; `launch.py:39-45` | No |
| C-026 | Regression LOW, non-blocking (a compatible fix exists) | V2 | 55% | design `:634`; `runner.py:126`; `launch.py:322` | Yes |
| C-036 | Regression LOW, nearly unreachable, non-blocking | V2/V3 | 60% | design `:739`; `record.py:184`; `record.py:548-549`; `cycle.py:1271-1280` | Yes |
| C-037 | Advisory LOW | V3 | 75% | `audit.py:381-404`; design `:722` | No |
| C-034 | Documentation Drift LOW; code exits are authorized | V3 (narrowed) | 80% | setup `:53`, `:432`; task `:498`; design `:115`, `:121`, `:726` | Yes (part c) |
| C-022 | Advisory LOW-MEDIUM; the tie rule is prescribed by the task | V1 | 75% | `predicates.py:199-209`; task `:196` | No |

**Recommended action:** before approval, fix C-014 with the snapshot-and-restore re-check after `_save()` and add the slow-save test. Replace the five skip sites in the same pass.

Not checked: I ran no tests and reproduced nothing. Design `:237-240` and the full text of task `:332` were not re-read this round.
