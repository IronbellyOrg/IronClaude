<!-- Written by the main session from the marked report body of this run's merged review card; the reviewing subagent could not write REPORT.md. Third review of the plan, before the cuts debate trimmed the plans. -->

# Reflect report (pre-execution), stage 3 plan, review 3 of 3 (revision 3 of the plan)

```yaml
contract_version: 1.8.0
status: partial                      # forced by one dropped citation (F8, PLAN:45); the content is otherwise complete
mode: pre
tier_reached: 2
confidence_calibrated: 0.86          # mean of the two reviewer-card calibrations (0.88 and 0.84); the T1 card calibrated 0.70
citations_total: 100                 # 55 card citation bullets + 45 inferred-requirement rows
citations_revalidated: 100
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Verdict: NEEDS-REVISION
- Findings: 3 blocking (F1 to F3), 12 non-blocking (F4 to F8 Medium, F9 to F15 minor)
- Run folder: `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116185913/`
- Full finding texts with every citation: `adversarial/merged-review-card.md` (above this block). Aliases: PLAN, SRC, S0, S4, SPEC, README, PRIOR as defined in its second comment line.

## Verdict

NEEDS-REVISION. Revision 3 fixed all three blocking findings of the earlier review in text and the 13 non-blocking ones, but three defects remain that gate the rule switch: the seeded-recall outcome words give R1b no word in the expected small-set case (F1), the found threshold scores the two arms with different panel sizes (F2), and the "a failed gate leaves no rule file switched" guarantee does not hold under `/sc:implement`'s fix pass and retry ladder (F3). Debate: 19 of 20 diff points agreed (95 percent); F3 was graded blocking on the invariant probe's evidence against both advocates' non-blocking grade.

## Earlier findings (review 2, `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116174401/REPORT.md`)

- Earlier F1 (gate ran after the edit): fixed in order (Task 4 is read-only, PLAN:113; Task 6 re-checks before its first edit, PLAN:140; old arm frozen as a copy, PLAN:78). One route stays open: the fix pass (new F3).
- Earlier F2 (outcome words and threshold): fixed in text (PLAN:82, PLAN:96); leaves R1b without a word (new F1) and scores unequal panels (new F2).
- Earlier F3 (QA rules 8 and 9): fixed in text (PLAN:160, PLAN:179, with zero-count lines PLAN:168, PLAN:185); the positive lines pass vacuously (F5) and label-floor lines remain (F6).
- Earlier F4 to F16: fixed (evidence in the card; README:43 now lists the ledger-row fields).

## Findings

F1 | blocking | Task 3's outcome words give R1b no word when the safety class is below its minimum n. R1b is "one event, never advisory" (PLAN:91); PASS needs "the class is at or above its minimum n" and only FAIL has the "R1b fails at any n" exception (PLAN:96); stage 0 says an undersized set is the expected outcome (S0:106). Task 4 reads the word as the gate and Task 14 states RT1 from it (PLAN:257), so an executor must invent a word and a false FAIL reports RT1 tripped. R3 has the same hole (no minimum n for the cosmetic class) and ADVISORY and NOT-MEASURABLE overlap (PLAN:86). Fix: add to PLAN:96 "R1b has no minimum n and is never advisory: PASS when every planted safety defect is found-and-blocking under the new text, FAIL otherwise, with n and the interval shown"; make R3 always advisory; give a precedence order.

F2 | blocking | The found threshold scores arms with different numbers of valid reviewers (PLAN:82: "2 of 3 with three valid reviewers, 2 of 2 with two"). New-arm reviewers are the ones likely to be invalid (PLAN:80, PLAN:82), so 3 against 2 is the expected case; at an illustrative 0.9 per reviewer, 2 of 3 finds a defect 97 percent of the time and 2 of 2 finds it 81 percent, a 16-point artifact against a 5-point margin (S0:106). R1, R1b, R2a and R2b lean toward FAIL (a ruling, the safe side), R3 toward a PASS that needs no ruling, and R1b can falsely report RT1 as tripped (PLAN:257). Fix: score both arms on the same k, the smaller valid count (at least 2), list the reviewers dropped, or mark the line NOT-MEASURABLE.

F3 | blocking | A failed gate does not leave "no rule file switched" (PLAN:21) under `/sc:implement`. A failed Task 6 check is a non-compliant verdict, not a halt: exactly one fix pass (SKILL.md:145; refs/qa.md:245), then the repair round and the ladder, and every halt leaves the failed attempt in the worktree (refs/retry.md:109, :158). Task 6's acceptance lines 2 to 7 (PLAN:146 to PLAN:152) demand the edit and the `v2` row that the task text forbids (PLAN:140); PLAN:22 forbids editing only the result file, the ledger and the gate file. Tasks 7 to 10 read only the registry row (PLAN:158, :177, :193, :203), and a `/sc:implement` Ruling that closes Task 6 (qa.md:254; ledger.md:158) leaves the edit in place; PLAN:22's "does not count" binds the plan text, not the executor. Fix: make acceptance lines 2 to 7 conditional on the first-paragraph check passing; say that no fix pass, repair, retry or adviser step edits src, tests or plugins while the check fails; have Tasks 7 to 14 re-read the gate (hash, five words, ledger rulings), not only the row.

F9 | minor | Task 5's acceptance line says the review help "still lists" `verify`; the command is registered as `verify-citations` (PLAN:132; src/superclaude/cli/review/verify_cmd.py:76). Fix: name the full command names.

F10 | minor | Task 6 says "except the two listed below" (PLAN:142) and then lists three test files (PLAN:152). Fix: "the three".

F11 | minor | Stage 4 reads the bold words of the Rule 6 line (S4:39); Task 8 does not require the rewritten Rule 6 to keep the form `6. **<heading>** ...` (PLAN:177). Fix: add that sentence.

F12 | minor | The Task 13 scan reads Markdown in seven roots (PLAN:240) while SPEC:920 says `src/` or `plugins/`; no hit lies outside the scanned roots today. Fix: say the roots are the complete set or scan all `*.md` under `src/superclaude`.

F13 | minor | The L1 text in Task 7 omits the `reasked` flag and "label stands, listed first" (PLAN:158; SPEC:270); the digest carries the consumer-unknown rule (SPEC:201), so only metric M8 is affected. Fix: add the two clauses.

F14 | minor | The byte-copied request keeps unrevised base text ("by an acceptance line, not by a dependency line", SRC:3; "Do not rely on `Depends on:` for this gate.", SRC:13) while Task 6 has a `Depends on` line on the gate task (PLAN:138); the plan also re-checks the gate in Task 6's body, so the intent holds. Fix: one sentence in the Revision 3 section of the request (SRC:43) that the base text is superseded for this point.

F15 | minor | Task 1's entry check: "the owner has read" the stage 2 summary (SRC:3) is not checked beyond file existence (PLAN:41); the Tree line has no pass criterion (PLAN:45); stage 0 evidence is checked for existence only (PLAN:42). Fix: state in Task 1 that the go covers the reading, that the tree line passes when recorded, and what the stage 0 files must say.

## Follow-up candidates (Medium, never fail a review)

F4 | Medium | In the expected undersized case Task 4 cannot reach PASS in the same run: the ruling must cite the hash of a file Task 3 writes (PLAN:98), `/sc:implement` has no pause between Tasks 3 and 4, resume row H re-reviews the stale FAIL gate file (ledger.md:160) and only a `/sc:implement` Ruling closes Task 4 (ledger.md:158), which PLAN:22 says does not count; Task 6's own ledger check then protects the edit. Task 1's re-run (PLAN:47) needs a new slug (managed-workspace.md:44). Fix: state the order of the two rulings or add an owner stop after Task 3.

F5 | Medium | Positive acceptance lines of Tasks 6 to 8 pass from the inserted digest: "stays open for verification" and `consumer-unknown` (SPEC:199, SPEC:201; PLAN:168, PLAN:185), and the cap checks count "1 or more" (PLAN:147). The zero-count lines still force the old text out, so the loss is replacement prose, not a wrong grade. Fix: pair each phrase with its anchor line.

F6 | Medium | Label-floor and relay lines contradict the rewritten Rule 6 and are in no edit list: rf-qa-qualitative.md:593, :611 (with :612 "cf. Critical Rule #6"), :616, :918 and rf-qa.md:389. They assign labels (information under the digest, SPEC:203), no test pins them, so no verdict changes; AX-2 cites a Rule 6 that Task 8 rewrites, and :918 can prompt a fix of a row graded Medium. Fix: reword them in Tasks 7 and 8 with a `grep -c -F` line each.

F7 | Medium | Reviewer validity is judged after the grades are read (PLAN:82), so the "fixed before dispatch" threshold depends on a later count; R1's gloss "new count not below old" (PLAN:90) passes a swap. Fix: a substring test of each quoted sentence against the two arm copies.

F8 | Medium | Task 3 copies the old arm from the live `pragmatic.md` "as it is now" (PLAN:78) and Task 1 never reads that the registry row is `legacy` and no `digest v2 begin` fence exists; after a partial run and a re-run the old arm would be the new text. Fix: add that check to Task 1. (One citation of this finding, PLAN:45, was dropped by the evidence gate.)

## Inferred requirements (Pass 2)

Pass 1 found one parsed row (REQ-04, SRC:55, covered by Tasks 3 and 6). Pass 2 emitted 45 quote-pinned rows; 44 match a plan item by the containment rule (0.6 of content words), one (INF-002, the stage 0b and 0c evidence, SRC:3) is unmatched by the mechanical rule and is covered by hand in Task 1 (PLAN:42). `coverage_pct` 1.0 (parsed only, 1 row); `coverage_pct_union` 0.9783; `coverage_degraded: parsed-sparse` (inferred 45 against parsed 1) forced Tier 2. All 45 quotes were re-read against their cited lines at Wave 5 (45 verified, 0 dropped). Full table: `artifacts/inferred-table.md`.

## Checked

- Task numbers 1 to 14 contiguous, every `Depends on` points to a lower task, Task 14 depends on 1 to 13, 5 phases; `/tmp/gate_check.py` prints `14 tasks 5 phases PASS`.
- Live lines the plan cites hold (pragmatic.md 221 to 230; rf-qa.md 83, 100, 402, 548, 549; rf-qa-qualitative.md 84, 99, the eight FAIL pairs, 809, 983, 990, 993, 994; rf-analyst.md 75); the cap sentence is on 2 lines of each agent and the digest words it differently; the Critical Rules window hash (980 to 989) ends before Rule 6.
- The digest holds none of the strings the zero-count lines require absent.
- The merge-phrase scan hits only files the plan and the stage 1 allow-list name; no hit under plugins.
- Stage 0, 1, 2 and 4 plans create the names the plan reads and agree on registry counts, allow-list rows and the plugin position.
- RT5 threshold, the RT1 (seeded part) and RT3 split, and the M4, M5, M6, M9, M11, M12 baseline sources match SPEC section 13. The earlier F12 is closed (README:43).
- No commands or tests were run by the reviewers; whether `uv run pytest tests/audit` passes after Tasks 6 to 10 is not established.

## Run notes (protocol deviations and degradations)

- `REPORT.md` was refused by the Write tool; this body is placed here as instructed. `report_path` is null in `return-contract.yaml`.
- Reviewers, advocates, fault-finder, scorers, calibrators, merge-executor and evidence-validator were spawned as plain subagents (a teammate cannot spawn named teammates); every role of the protocol ran.
- Executor class resolved by log heuristic (sonnet, same class as this session); N=2 reviewers (haiku analyzer, opus qa); `t2_model_class_diversity: degraded`, `t2_vendor_diversity: single`, `calibrator_diversity: full`.
- `.dev/reflect/runs.jsonl` and the memory files of section 6.3 were not written, because the lead's rule limits output to the new run folder.
- Citation budget: all 100 citations were re-read (stricter than the sampled policy for more than 20).

## Self-report

confidence: 0.86 (mean of the two calibrated card scores; orchestrator merge)
