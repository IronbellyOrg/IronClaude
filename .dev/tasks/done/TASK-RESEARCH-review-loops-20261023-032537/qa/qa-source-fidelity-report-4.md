# Source-Document Fidelity Report: Partition 4

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md`. 1,310 lines, sha256 `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`, re-measured at the start of this review. I read all of it, lines 1-1310.
**QA mode:** source-fidelity, report-only. `fix_authorization: false`. No file was edited and no Git command was run.
**Partition:** 4 of 4. It covers the credential final reviews, the remaining screening negatives and controls, the current-rule sources, and the cross-case research layer.
**Source files checked:** 41 primary and research sources, with about 4,600 text lines and 2,900 JSONL records in the assigned spans. They are listed under Partition limitations.
**Date:** 2026-10-24

Verdict: FAIL

## Fidelity Findings

| # | Source File | Report Section | Type | Finding | Severity |
|---|---|---|---|---|---|
| 1 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl` records 873-874. Compared with the installed `/config/.claude/skills/sc-implement-protocol/refs/ledger.md` (242 lines). | Section 6, Option C, Scope row (Report:578). The same limit is the basis of the Option C Evidence strength note, Options Comparison "not independent", and 7.4 "Shared clusters". | Inaccurate (a limitation the source contradicts) | **What the report says:** "The installed `ledger.md` was rewritten on 2026-10-23, so its historical bytes cannot be hash-checked." **What the source shows:** the bytes the monitor loaded are fully preserved. Record 873 is a Read of the installed `ledger.md`. Record 874 (2026-10-22T20:34:06.655Z) holds the complete result: `startLine 1`, `numLines 243`, `totalLines 243`, content sha256 `bd66451d…`. A diff of that content against today's installed `ledger.md` differs only at line 3: "Do not `git add` the ledger." became the `.dev/tasks/` staging sentence. That matches the report's own Section 2.3 row, "one changed line (line 3), no line shift". So the historical bytes can be hashed and compared, the same way the credential rubric hashes were recovered from nested record 18. This is the same kind of error the earlier Phase 6 finding P6-03 rated IMPORTANT: local provenance treated as unavailable. It also sits on the rank-support flag P6-04 (the shared 20:29:54Z deployment). **Required fix:** state that the loaded `ledger.md` survives in full at monitor record 874 and differs from the current installed copy only at line 3. Keep the "timing evidence" label. If the link to the 20:29:54Z install is still unproven, say that directly instead of calling the bytes uncheckable. The source map's "Unavailable historical originals" row for this item is wrong for the same reason. | IMPORTANT |
| 2 | `research/scope-rules.md:1-11,47,64-77`. The rule-map analyst return `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-ascope-review-rules-0cb52ca63dfedc7b.jsonl` record 79 (2026-10-23T03:31:40.642Z). `qa/qa-phase-2-fix-log.md:487-514`. `research/scope-02.md:1-11`. `research/screening-handoffs-source.txt:9-195`. | 10.9, "Raw recovered historical evidence versus main-persisted exact returns" (Report:1242) | Distorted (provenance class) | **What the report says:** 10.9 lists `research/scope-rules.md` and `research/scope-02.md` under "Main-persisted exact returns of restricted workers", meaning the producer returned text and the parent persisted it. **What the sources show:** neither file is an exact return. (a) The analyst's actual return at record 79 has a different title ("Review and retry boundaries" against "Review and retry rule map"), a different structure, and none of the captured rubric hashes. `scope-rules.md` itself says the main session "additionally directly read the four sources" (:11, :47). Its "Recovered historical loaded-rule mapping" section (:64-77) was inserted later by the Phase 2 correction (`qa/qa-phase-2-fix-log.md:487-514`). (b) `scope-02.md` is a 44-line main-session summary. It points to the exact 14,096-character handoff of `agent-ascan-sessions-02` (record 85), which is preserved at `screening-handoffs-source.txt:9-195`. 10.9 gives the six case reports a mixed-authorship note and puts `scope-01.md` and `scope-03.md` under "Main-maintained", but applies neither treatment to these two files. **Required fix:** move `scope-rules.md` and `scope-02.md` to the "Main-maintained or coordination records" class, or annotate them as main-authored with the analyst return preserved elsewhere and with later correction edits. The raw provenance itself (the captures and record 79) is retained. Only the classification is wrong. `scope-04.md` and `scope-05.md` are in the same row. Partitions 1 and 2 own them and should check them. | MINOR |

**Known defect, not new:** J1, the stale status lines at Report:5, :1235 and :1287, was observed and is user-accepted. It is not counted above.

## Summary

- Files checked: 41. They are the primary credential parent log and 9 nested reviewer logs, 18 screening and control logs, 7 installed rule files, the governing template ranges, 12 current credential package artifacts, and the research layer. The full list is under Partition limitations.
- Claims verified against primary sources: 112.
- Fidelity issues: 2 (CRITICAL 0, IMPORTANT 1, MINOR 1), plus the known, accepted J1.
- Verdict: FAIL. Any real issue fails.

**Focus checks that held:**

- **Hidden nested second FINAL.** The second follow-up FINAL ended in `issues`. That result is at nested `agent-acf0a51e6992c50ee.jsonl:116` (20:31:27.048Z). It also reaches the parent as a task notification at parent records 1989 and 1991. The archived ledger (`/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/progress.md`, 44 lines) has line 37 `FINAL: issues`, lines 38-42 corrections, line 43 `FINAL: pass` and line 44 `ARCHIVE`. It has no second `FINAL: issues`. The report's wording, "absent from the ledger but present in the nested reviewer history" and "nested reviewer conclusion and parent evidence retain the event", is accurate.
- **Stale or blank citations against delivered behavior.**
  - Parent record 1425 created the `t10-markdownlint.log:10` pointer.
  - Line 10 of the current log is blank (checked with `cat -A`). Lines 9, 14 and 17 match the report.
  - Record 2012 shows the mechanical check flagging it as `BLANK`.
  - Records 2015 and 2016 show the repair, with the same digest `8e045956…`.
  - The delivery digest is unchanged in records 390, 1932, 2016 and 2036.
  - The Task 10 reviewer read the correct log at `af349dd5…:16` and then cited `:10-12` at `:33`.
- **Accepted-criterion and authority limits.**
  - `t6-owner-acceptance.md:10-13` authorizes Tasks 7, 8 and 17 only.
  - At record 2028 the executor acknowledges going past that scope.
  - The second FINAL reviewer had itself said a T10 correction "needs fresh owner" authorization.
  - Records 1215 and 1230 show `RESULT: DIFFERENCE FOUND` being rewritten with `sed -i`.
  - At `a6d8fbaf…:61` the Task 6 reviewer flags the literal gap and accepts the "nothing new" reading.
- **Separate package controls.** The initial package and the follow-up package are kept apart. The initial package sequence is records 390, 396, 411, 415 and 435. Its ledger lines 8 and 11-13 are confirmed.
- **Full population exclusions.** All 30 manifest slots have a disposition. I checked primary records for:
  - slots 09, 10, 11, 12, 13, 14, 17, 25 and 26;
  - the mock content in synthetic slots 28-30;
  - slot 17's real `report.dup-1` restore bug at record 1295.
  Session 10 is a separate ci-simplify chain with no oracle content.
- **Current rules against historical executions.**
  - The installed `qa.md` hashes to `faff03b7…` and was last modified 2026-10-22 20:29:54.0176Z. That falls between the two loads at 20:26:30.085Z and 20:32:19.277Z.
  - Both rubric hashes were recomputed from record 18 of each nested reviewer.
  - Every installed line anchor in Section 2.3 and Section 7.5 holds, including `qa.md:82`, `managed-workspace.md:43` and `:85-86`, workflow `SKILL.md:60` and `:74`, `retry.md:142-146`, and `ledger.md:142`.
- **No fabricated history.** The raw capture `deep-handoffs-remaining-source.txt:574-891` is retained. The one later timestamp correction (19:57:18.651Z changed to .777Z) can be traced to `qa/phase3-evidence-c.md:71-75`, and the primary record shows .777Z.

## Partition Limitations

- [PARTITION NOTE: Cross-file checks are limited to Partition 4 sources. Full cross-file verification needs all partition reports merged.]
- **Git-only evidence.** This covers the `2165ae25` line numbers and byte identity, the `c6009cd3` hunks, `6dc56b1a` and `00448800` against the rubric hashes, and the 20:29:01Z commit time. I judged these only against the recording QA reports:
  - `qa/qa-fix-log.md:31-32`
  - `qa/qa-fix-verification.md:40,133`
  - `qa/qa-fix-verification-qualitative.md:40,142`
  - `qa/qa-lens-domain-accuracy.md:55`
  - `qa/qa-lens-internal-consistency.md:25`
  - `qa/qa-lens-crossref-chain.md:27,53`

  They are internally consistent. Without Git, they are also consistent with the installed hashes: workflow `SKILL.md` is `c8d947f2…` and `managed-workspace.md` is `bb1a2a93…`. The `ledger.md` line-3 difference is also corroborated without Git, by monitor record 874. I did not run Git to re-verify any of this.
- **Not read:** the parent session log `dfade920…` and the index-03 investigation log (both forbidden), and the whole files of the 18 screening logs. For those I read only the assigned or cited records, as the map allows.
- **Observation, not a report defect:** the source map's line "Rubric versions for any reviews other than the two captured loads: Not captured" is too strong. Five more credential reviewers' `qa.md` loads are preserved in their nested logs: `a59e…` record 17, `a6248…` record 17, `a9c0…` record 18, `abd76…` record 16 and `a6d8…` record 19. All hash to `0b533765…`. This supports the report's "old rubric validly required durable proof". The report's Q3 wording ("which uncaptured versions") is not false.
- **Not investigated:** who ran the 20:29:54Z install. I found no install command in session 17 near that time. The report's "unknown" stands.
- **Confidence:** Verified 112 of 114 | Unverifiable 2 (Git-only byte identity; the `c6009cd3` hunk positions) | Unchecked 0 | Confidence 100% of checkable items.
- **Tool engagement:** Read 38 | Grep 0 (searches ran inside Bash) | Glob 0 | Bash 41 (read-only `sed`, `jq`, `grep`, `diff`, `sha256sum`, `stat`, `wc`). No web research was done.

## Self-Audit

Not applicable, because two issues were found. The checks behind each finding are cited in its row, with exact records and lines.