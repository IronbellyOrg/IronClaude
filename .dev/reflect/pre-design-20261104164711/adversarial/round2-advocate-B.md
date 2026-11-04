# Round 2 — Advocate B (qa card)

## 1. Responses

- **CF-05/06 (A: L drift vs my M necessary). Concede both.** S:1422: step 7 owns the resume rows, so a spec-compliant placement exists; no AC fails falsely. Addendum: Task 8's Task 4 dep (P:155) re-points to 4b, holding the planners Task 8 calls (P:166).
- **A's new 4b-on-5 edge: verified, adopt.** P:114 and P:88/93 append the same file (CF-01 hazard).
- **CF-15, CF-18 (A: L). Concede severity.** CF-15: the reflect test is in no AC; drop authorized (P:28). CF-18: Tasks 10-14 run `test_static_grep.py`; fails loudly by Task 14.
- **CF-17. Agree with A; my R1 U-001 adoption over-reached.** S:1400: X1 omits `expect_checks_after_push`; S:1428's "4, 6, 9" reaches 6 via Task 8. Task 13 alone required.
- **CF-14, CF-07. Concede both.** CF-14 becomes spec defect (P:53 copies S:731's `:86-99`); CF-07 advisory: mirroring spec steps is not deviation.
- **To C:** C-009 — Low agreed; test stays in Task 20. Overconfidence (0.87 vs 0.78) and Q-1 mis-citation conceded.
- **Held:** CF-11/12 Medium — A conceded; S:1316 (fixed identity, capability skip) absent from P:29/P:291.

## 2. Final table

| CF | Sev | Class | Fix | vs A R2 |
|---|---|---|---|---|
| 01 | M | drift | Chain 11→12→13 on 10 | agree |
| 02 | M | drift | 15 on 4a, 12 | agree |
| 03 | M | drift | 16 on 2, 6, 13 + header grep | agree |
| 04 | M | drift | 20 on 6, 9, 18, 19 | agree |
| 05 | L | drift | 4b on 4a, 5, 7; 8 re-point to 4b | agree + addendum |
| 06 | L | drift | Split 4a/4b | agree |
| 07 | L | advisory | Optional log sections | agree |
| 08 | M | drift | Stage paths + `.dev/tasks`; `--cached` AC | agree |
| 09 | M | drift | `test -x` in 10-12 | agree |
| 10 | L | drift | Greps to `./artifacts/` | agree |
| 11 | M | drift | Capability skip in 19 | agree |
| 12 | M | drift | Fixed identity in P:29 | agree |
| 13 | L | drift | Quote S:728 clause in 2 | agree |
| 14 | L | spec defect | Cite `:86-103` | agree (conceded) |
| 15 | L | authorized | Reflect test + log line in 20 | agree (conceded sev) |
| 16 | L | authorized | None | agree |
| 17 | M | drift | 19 on 13; 6, 14 optional | agree |
| 18 | L | drift | `test_static_grep.py` in 11, 12 | agree (conceded sev) |
| 19 | L | drift | C1-C4 sans `--pr`; stderr SHA | agree |
| 20 | L | drift | Anchors + substring AC in 17 | agree |
| 21 | L | necessary | Keep 9→6 (P:178) | agree |
| 22 | M | drift | 10 on 3, 4a | agree |

## 3. Shared assumptions

- **A-001 ACCEPT.** P:184: Task 10 names Task 3 only; one edge closes CF-22 and CF-02.
- **A-002 ACCEPT.** Name-matching missed CF-22; closures need the plan graph, spec case IDs expanded to asserted functions.
- **A-006 QUALIFY.** S:1070: ci-poll documents `expect_checks_after_push` (step-10 column incomplete); S:1428: step-13 column adequate, so Task 13 required.

Verdict: ready-with-fixes. Full agreement with A's R2 table; sole addition: Task 8→4b re-point in CF-05.