# Phase 5 Consolidated Synthesis-Gate Findings

**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (issue #339, orchestrator mode Phase 1)
**Date:** 2026-11-07
**Step:** 5.7 merge (one serialized fix agent consumes this file)
**Author:** rf-analyst, report-only (no synthesis, research or task file edited)

## Inputs

All ten Step 5.7 reports in `qa/` were confirmed with Glob and read in full.

| # | Report | Short name | Raw blocking count (as the report rated it) |
|---|---|---|---|
| 1 | `qa/analyst-synthesis-accuracy-1.md` | acc-1 | 1 |
| 2 | `qa/analyst-synthesis-accuracy-2.md` | acc-2 | 5 |
| 3 | `qa/analyst-synthesis-tracing-1.md` | tr-1 | 2 |
| 4 | `qa/analyst-synthesis-tracing-2.md` | tr-2 | 3 |
| 5 | `qa/qa-synthesis-structure-1.md` | st-1 | 1 |
| 6 | `qa/qa-synthesis-structure-2.md` | st-2 | 3 |
| 7 | `qa/qa-synthesis-content-1.md` | co-1 | 1 |
| 8 | `qa/qa-synthesis-content-2.md` | co-2 | 6 |
| 9 | `qa/qa-synthesis-qualitative-report-1.md` | qu-1 | 4 |
| 10 | `qa/qa-synthesis-qualitative-report-2.md` | qu-2 | 5 |
| | **Total raw** | | **31** |

The 31 raw findings collapse to 15 blocking findings after merging duplicates. Some findings that one report rated MINOR were rated IMPORTANT by another report; these were merged at the higher severity (see Conflicts). No raw blocking finding was downgraded, and none was dropped.

Synthesis files: `synthesis/synth-01-problem-current-state.md` (S1), `synth-02-target-gaps.md` (S2), `synth-03-external-findings.md` (S3), `synth-04-options-recommendation.md` (S4), `synth-05-implementation-plan.md` (S5), `synth-06-questions-evidence.md` (S6).

## Grading Rule

- **Blocking** means CRITICAL or IMPORTANT, and also a real defect: a wrong claim, a contradiction (inside one file or between files), or missing required content.
- A finding labelled IMPORTANT that is only wording, or only a moved line number on a claim that is still true, counts as **MINOR**.
- Duplicates are merged into one row at the highest severity any source gave it, and every source report is named.
- Where reports disagree on a claim or a severity, the cited synthesis line and the source line it cites were re-read, and the outcome is recorded under Conflicts.
- Lines named under Conflicts, and the evidence lines quoted in B-01 to B-13 and B-15, were re-read in this pass (2026-11-07). The header lines S1 `:5` and S3 `:7` in B-14, and the line numbers in Notes, are as the source reports give them.

## Blocking Findings

|F_0| = 15

| ID | Source report(s) | Severity | Synthesis file | Section / line | Finding | Required fix |
|---|---|---|---|---|---|---|
| B-01 | acc-1 #1; tr-1 F1; st-1 B1; co-1 #1; qu-1 #1 | IMPORTANT | S1 | Section 2, `:201` | Wrong claim. S1 says `gaps-and-questions.md:125` still reads "Open: 76. Resolved: 24" and is off by one. The line now reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none" (re-read `gaps-and-questions.md:125`). S1 also contradicts S2 `:7` and `:230`, which give 75/25. | Drop the stale-count sentence, or state that `:125` reads 75/25 after the NB-4 fix. Keep the C13 full-verb-form sentence. |
| B-02 | acc-2 F1; st-2 I-1; co-2 #1; qu-2 I-1; tr-2 F4 (rated MINOR) | IMPORTANT | S4 | Contradictions table X-6, `:220` | Wrong claim, the same stale count as B-01: "still says 'Open: 76. Resolved: 24' ... The counts are off by one". `gaps-and-questions.md:125` reads 75/25. | Delete row X-6, or restate it as resolved, citing `gaps-and-questions.md:125` (75/25). |
| B-03 | acc-2 F2; st-2 I-1; co-2 #2; qu-2 I-1; tr-2 F4 (rated MINOR) | IMPORTANT | S5 | 8.4 X-6 `:260`; 8.1 `:172` (C2); 8.1 "sent to Open Questions" `:206`; 8.5 `:282` | Wrong claim and wrong label. X-6 (`:260`) calls `:125` stale and cites "synth-02 C2", and `:282` repeats "stale count at `:125`". S2's C2 (`synth-02:241`) is about the line count of `test_how_we_work_routing_table.py` (360 versus 1202), not the gap count. So `:172` and `:206` send the wrong item to Open Questions under C2. | Remove X-6, or mark it resolved (75/25). Remove "stale count at `:125`" from `:282`. Keep C2 at `:172` and `:206` only as the line-count note it actually is. |
| B-04 | acc-2 F3; tr-2 F2; st-2 I-2; co-2 #3; qu-2 I-2 | IMPORTANT | S6 (against S5) | Section 9 row 17, `:45` | Contradiction. Row 17 (GQ-22) says "Measure once; keep it off by default". S5 step 1.4 (`:62`) puts `--include-remote` in the default argv, and `gaps-and-questions.md:45` keeps GQ-22 open: remote rows read as unverifiable without the flag. | Change row 17 to: `--include-remote` on by default (as S5 1.4), measure its cost once, GQ-22 stays open. Add tr-2's acceptance criterion to S5 step 1.4: one measured run with the flag. |
| B-05 | acc-2 F4; qu-2 I-3; co-2 #11 (rated MINOR) | IMPORTANT | S6 | Section 9 row 58, `:86` | Wrong resolution. Row 58 (GQ-84) says "Apply rule 2 before rule 7". That restates the precedence that causes the problem. `gaps-and-questions.md:107`, S2 `:220` and S5 `:161` all resolve GQ-84 the other way: exited, no `worker_done` and an unreadable transcript give could not determine. | Replace the row 58 resolution with the S5 `:161` text (exited + unreadable transcript -> could not determine; rule 2 needs the transcript read). |
| B-06 | acc-2 F5; qu-2 I-4; co-2 #4(a), #4(b), #4(e); tr-2 F5, F6 (rated MINOR); qu-2 M-3 (part) | IMPORTANT | S5, S6 | S5 step 1.17 `:90`, 8.1 `:138`, `:158`, `:159`, 8.2 OQ-11 `:223`; S6 row 51 `:79` | Open owner decisions are presented as decided. GQ-11 is open (`gaps-and-questions.md:34`; S2 `:103` "WC-14 versus amending WC-1 is open"), yet S5 `:90` says "GQ-11 decided as WC-14" and `:158` maps it to WC-14. GQ-35 is open (`gaps:58`; AMB 9 `:158`), yet S5 `:159` pins `495eb96d`. GQ-10 is open (`gaps:33`; S2 `:187` "the exact directory is an owner decision"), yet S5 `:138` fixes it. OQ-11 (`:223`) lists only G6, GQ-61 and GQ-63, and omits GQ-10, GQ-11 and GQ-35. S6 row 51 (`:79`) gives GQ-61 as "6 h ..." with no owner-decision flag, while S5 `:153` and `gaps:84` keep it an owner decision. | In S5, present GQ-10, GQ-11 and GQ-35 as working defaults that wait on the owner. Add them to OQ-11 (`:223`). In S6 row 51, mark GQ-61 as an owner decision (AMBIGUITY 2) with 6 h as the working default. |
| B-07 | qu-2 I-5; acc-2 M8 (rated MINOR) | IMPORTANT | S6 | Section 9 row 33, `:61` | Wrong claim. Row 33 puts GQ-38 under the message-truncation resolution of GQ-48. GQ-38 is worker-list paging on `page.nextCursor` (`gaps:61`). GQ-48 is the 100-row message cap (`gaps:71`). These are different questions with different resolutions. | Split row 33. GQ-38: page on `page.nextCursor` (S5 1.4). GQ-48: "at least 100 (truncated at 100), total could not determine". |
| B-08 | tr-2 F3; co-2 #5 | IMPORTANT | S6 | Section 9 row 49 `:77` (GQ-59); row 36 `:64` (GQ-41, tr-2 only) | Wrong claim. Row 49 says "Add a version probe to the header", and row 36 says "Record the CLI version in the report header". Both assume a read-only version source exists. `gaps:82` says "No read-only verb that reports the runtime version was found". S5 `:150` and `:197` keep GQ-59 as contracts-only by default, with the probe sent to Open Questions (it needs a runtime-handler read or a throwaway-Run probe). | Row 49: no version probe in Phase 1; `--peek` stays gated; GQ-59 stays open (as S5 `:150`, `:197`). Row 36: GQ-41 stays open (CLI version of the research captures); do not promise a header field without a verified read-only source. |
| B-09 | st-2 I-3 | IMPORTANT | S5 | Step 1.19, `:92` | Wrong claim, in two parts (spot-checked; see Conflicts). (1) It says to add `sweep` to `NEVER_AS_WORKER`, but every entry there is a `/sc:` form (`tests/skills/test_worker_contract.py:245-254`), and S5 1.18 (`:91`) and S2 SC-12 (`:122`) use `/sc:sweep`. (2) It says `_check_never_as_worker` "then checks `sweep.md`". The function checks the `**Never-as-worker list**` line of `_contract()`, which is WORKER-CONTRACT.md (`:398-404`, called at `:545-546`). The `RULE_PHRASES` update is present (`:92`); that part of st-2 I-3 does not hold. | Change step 1.19 to add `/sc:sweep` to `NEVER_AS_WORKER`, and say `_check_never_as_worker` checks the WORKER-CONTRACT.md list line edited in 1.18. Keep the `RULE_PHRASES` `:86-92` update and the test rename. The same bare `sweep` appears in S6 row 10 (`:38`); this pass observed it while checking, and no report raised it. |
| B-10 | co-2 #6 | IMPORTANT | S5 | Step 1.3 rule (2), `:61`, against header `:12` | Contradiction. The header (`:12`) says [UNVERIFIED] items appear in a step only as "treated as could not determine" or "forbidden". Rule (2) uses `liveness.verdict` `exited` as positive proof of stalled. `exited` has never been captured; it is guide text only (`gaps:60`, GQ-37; S5 `:146` uses synthetic rows). | Either label rule (2) as built against synthetic `exited` fixtures, with GQ-37 open and the live-capture check sent to Open Questions, and narrow the header to allow that; or keep the header and change rule (2) to match it. Do not leave the two in conflict. |
| B-11 | tr-1 F2; qu-1 #2 | IMPORTANT | S2 | 4.1 R-2 `:172` against 4.2 G2 `:182`, G5 `:185`, G7 `:187` | Contradiction. R-2 says an in-scope capability that is designed but not wired is "a defect rated Critical", and names G1, G2, G5 and G7. The table rates G1 Critical, but G2 and G5 "Important (N-32); Critical under R-2 if ..." and G7 "Important (N-32)". R-1 (`:171`) says rows keep their source severity. R-1 and R-2 give different ratings for the same rows, and the table follows neither one consistently. | State which rule wins for G2, G5 and G7, and rate those rows to match. For example, R-2 governs: Critical until wired. Or narrow R-2's named list so it excludes them. |
| B-12 | qu-1 #3 | IMPORTANT | S3, S2 | S3 R4 `:216` against R7 `:219`; S2 `:152` against `:90` | Contradiction. R4 / S2 `:152` exclude person-wait time from every printed age. R7 / S2 `:90` sort the waiting-on-a-person list oldest first by age. If wait time is excluded from every printed age, the waiting list has no age to sort by. | Define which age the waiting list sorts on (time since the wait began). Narrow R4 / S2 `:152` to activity ages and the 6 h activity window. |
| B-13 | qu-1 #4 | IMPORTANT | S3 | 5.9 "Agreement across sources", `:183` | Wrong claim, and it contradicts the same file. The line says "no external source contradicts WC-10's core claim". S3's own 5.4 (`:100`, Grafana "partly contradicts"), 5.5 (`:118`, agents-fleet "the automatic abort contradicts WC-10"), and D5 and D6 (`:173-174`) say otherwise, as does S2 `:157` ("Contradicts WC-10; rejected"). | Reword `:183` to name the contradicting sources (Grafana missing-data mapping and the agents-fleet auto-abort, both rejected), and say the remaining sources support WC-10. |
| B-14 | tr-2 F1; acc-1 #2, acc-2 M11, co-1 #3, qu-1 #5, qu-2 M-1, tr-1 F5 (each rated MINOR) | IMPORTANT | S5, S6, S4, S1, S3 | S5 8.4 X-7 `:261`, 8.2 `:211-224`; S6 Section 9 (no row); headers S4 `:3`, S6 `:3`, S1 `:5`, S3 `:7` | Missing required content and a contradiction. S2 4.8 (`:284`) keeps fenced as its own class, and sends the owner choice (six classes as the research question says, or seven) to Open Questions. S5 X-7 settles it ("Section C list ... is canonical") with no OQ entry in 8.2, and S6 has no Section 9 row for it. The headers of S4, S6, S1 and S3 list six classes without fenced, while S5 `:10` lists seven. | Add an open question (six versus seven classes, fenced as its own class or folded into could not determine) to S5 8.2 and to S6 Section 9. Make the class lists at S1 `:5`, S3 `:7`, S4 `:3` and S6 `:3` match S5 `:10` (seven, including fenced), or mark them as the research question's six. |
| B-15 | co-2 #4(c), #4(d); acc-2 M7, tr-2 F8, st-2 M-1, qu-2 M-3 (each rated MINOR) | IMPORTANT | S6 (against S5) | Section 9 rows 27 `:55` (GQ-32), 28 `:56` (GQ-33) | Contradiction. Row 27 gives GQ-32 as "Print the window and the Run ids", and row 28 gives GQ-33 as "Print the omission count". S5 step 1.5 (`:63`) and `:159` resolve them as a root-path scope line (GQ-32) and "list everything" (GQ-33). `gaps:55-56` keep both as open plan decisions. | Make rows 27 and 28 match S5 1.5: a root scope line, and list everything. Or, if S6 is right, change S5. Both files must give the same answer. |

## Conflicts Between Reports (spot-checked)

| # | Claim | Reports and positions | Lines checked | Which is right |
|---|---|---|---|---|
| K-1 | Is the X-6 stale-count claim blocking? (B-02, B-03) | acc-2, st-2, co-2 and qu-2: IMPORTANT. tr-2 F4: MINOR. | `gaps-and-questions.md:125` (75/25); S2 `:7`, `:230`; S4 `:220`; S5 `:260`; S2 C2 `:241` | IMPORTANT is right. The claim is false, not just a moved line: `:125` already reads 75/25. It also contradicts S2, and S5 pins it to an unrelated C2. |
| K-2 | Row 58 (GQ-84) severity (B-05) | acc-2 F4 and qu-2 I-3: IMPORTANT. co-2 #11: MINOR. | S6 `:86`; `gaps:107`; S2 `:220`; S5 `:161` | IMPORTANT is right. "Apply rule 2 before rule 7" gives stalled (proved) in exactly the case that GQ-84, S2 and S5 resolve to could not determine. That is a wrong resolution, not wording. |
| K-3 | Step 1.19 (B-09) | st-2 I-3: three defects (bare `sweep`, "checks `sweep.md`", `RULE_PHRASES` update missing). acc-2: step 1.19 is correct on the 8-entry count and the "all seven" rename. | S5 `:91-92`; `tests/skills/test_worker_contract.py:86-92`, `:245-254`, `:398-404`, `:545-546` | Both are partly right. acc-2 is right on the count (8 entries) and the rename. st-2 is right that the entry must be `/sc:sweep` and that the check reads WORKER-CONTRACT.md. st-2 is wrong that the `RULE_PHRASES` update is missing: S5 `:92` includes it. |
| K-4 | How GQ-59 is framed (B-08) | tr-2 F3: row 49 assumes a read-only version verb. co-2 #5: GQ-59 is a `--peek` / `compatibilityAck` question gated on a runtime-handler read. | `gaps:82`; S5 `:150`, `:197`; S6 `:77` | Both are right. They describe the same defect from two sides. `gaps:82` is titled "Runtime-version or legacyCompatibility probe before trusting --peek" and says no read-only version verb exists. Merged into B-08. |
| K-5 | Row 17 (B-04) | All five reports that raise it agree (acc-2, tr-2, st-2, co-2, qu-2). tr-2 also asks for a measurement acceptance criterion in step 1.4. | S6 `:45`; S5 `:62`; `gaps:45` | No conflict. tr-2's addition is folded into the B-04 fix. |
| K-6 | Six versus seven classes (B-14) | tr-2 F1: IMPORTANT (the open question is dropped). acc-1 #2, acc-2 M11, co-1 #3, qu-1 #5, qu-2 M-1 and tr-1 F5: MINOR (header wording). | S2 `:284`; S5 `:10`, `:211-224`, `:261`; S6 has no row (grep for "fenced" / "six" in S6 matches only rows 10 and 58) | IMPORTANT is right. S2 sends the owner choice to Open Questions, and neither S5 8.2 nor S6 Section 9 carries it. That is missing required content, not only wording. |
| K-7 | GQ-10, GQ-11 and GQ-35 shown as decided (B-06) | acc-2 F5, qu-2 I-4 and co-2 #4: IMPORTANT. tr-2 F5 and F6: MINOR. | S5 `:90`, `:138`, `:158`, `:159`, `:223`; `gaps:33`, `:34`, `:58`, `:152-153`, `:158`; S2 `:103`, `:187` | IMPORTANT is right. The research file and S2 keep all three open as owner decisions. S5 states them as decided, which is a wrong claim. |
| K-8 | Rows 27 and 28 (B-15) | co-2 #4(c), #4(d): IMPORTANT. acc-2 M7, tr-2 F8, st-2 M-1 and qu-2 M-3: MINOR. | S6 `:55-56`; S5 `:63`, `:159`; `gaps:55-56` | IMPORTANT is right. S6 and S5 give different answers to the same two questions. That is a contradiction. |
| K-9 | Row 33 (B-07) | qu-2 I-5: IMPORTANT. acc-2 M8: MINOR. | S6 `:61`; `gaps:61`, `:71` | IMPORTANT is right. GQ-38 (paging) gets the GQ-48 (truncation) answer, which is wrong for GQ-38. |
| K-10 | crash-recovery `SKILL.md:25-27` citation (S2 `:144`, `:243`) | tr-1 F6 (MINOR) questioned it. qu-1 found it valid. | `src/superclaude/skills/sc-crash-recovery/SKILL.md:4`, `:25`, `:26` | qu-1 is right. `:4` allows `Bash(git stash *)`, `:25` has `~/workspace/`, and `:26` has the 72-hour default. No fix needed. |

## Notes (MINOR, non-blocking)

These notes do not count toward |F_0|. The MINOR ratings that were merged into blocking rows (see Conflicts K-1 and K-6 to K-9) are not repeated here. Line numbers are as the source reports give them.

1. **Colon versus space verb form.** Some rows write `orchestration:<verb>` where the pinned form is `orca-ide orchestration <verb>`, for example S6 row 21 (`:49`). Sources: acc-2 M6, tr-2 F7, st-2 M-2, co-2 #9, qu-2 M-2.
2. **Truncation strings differ** between files. S3 `:162` uses "at least N, listing truncated: could not determine the total", where S3 R8 and S5 1.5 use "at least 100 (truncated at 100), total could not determine". Use one string. Sources: tr-2 F9, co-2 #10.
3. **GQ-99 batching** is applied where the batching policy does not reach (the per-sweep Orca call bound is not a Bash inspection batch). S6 row 63 (`:91`) says "Batch where the policy allows". Sources: tr-2 F10, co-2 #12, qu-2 M-5.
4. **S6 `:221` and `:230` are stale.** `:221` says a file is "not yet written", and `:230` gives "qa/ (24 files)". Sources: acc-2 M9, tr-2 F12, st-2 M-3, st-2 M-4, co-2 #13, qu-2 M-4.
5. **S6 rows 18, 22, 24, 26 and 50 lag Section 8.** These questions are answered in S5, but S6 still shows them open. Row 50 says "Leaning A1" where S5 says "Settled as A1" (`:152`). Sources: co-2 #7, tr-2 F13, qu-2 M-3 (rows 18 and 50).
6. **Wrong citations.** S5 `:182` sends scope-01 `:100` to Open Questions while S2 `:251` treats it differently. The S2 `:251` GQ-84 cite is wrong for the 41-test row. Sources: tr-2 F11, co-1 #2.
7. **Guide-only facts in S1 Section 2** (`:79`, `:89`, `:98`) are not separated from code-traced facts (against `:288-294`). Sources: tr-1 F3, co-1 #8.
8. **The forbidden column of the S1 allowlist table** (`:187-193`) omits `check --format` and the rule of one read mode per call. Sources: tr-1 F4, co-1 #7, qu-1 #7.
9. **No §4.8 pointer** for the class count. S1 `:15` has no pointer to S2 §4.8, and the S1 `:5` and S3 `:7` class lists omit fenced. The second part is covered by B-14. Source: tr-1 F5.
10. **S2 `:16` states A1 as decided** in the target section, before Section 7 reaches it. Source: tr-1 F7.
11. **The precedent at S2 `:17` covers only the bare form.** Source: co-1 #9.
12. **Numbering of D5 and D6 in S3.** Source: tr-1 F8.
13. **S3 has no title line.** Source: acc-1 #3.
14. **S3 `:3` says "verified codebase rule"** without a tag. Source: co-1 #6.
15. **S3 `:113` calls GQ-61 an "owner note".** GQ-61 is an open owner decision. Source: qu-1 #9.
16. **S3 source note `:230`** does not record the partial fetch of the Kubernetes node-status page. Source: st-1 M3.
17. **Labels and section form in S3.** The "Relationship:" label, and the Section 3 form. Sources: st-1 M1, st-1 M2.
18. **R-2 (S2 `:172`) has no remediation link**, and scope-02 `:241` is out of scope. Sources: st-1 M4, st-1 M5.
19. **S2 R-3 wording.** R-3 "skips", and the `:156` "code fact" claim. Source: acc-2 M5.
20. **Section and table form in S4.** S4 uses a "Recommended option" label, and the H2s at `:248` and `:263` are unnumbered. Sources: acc-2 M1, acc-2 M2.
21. **Table columns** differ from the template column sets. Sources: acc-2 M3, acc-2 M4.
22. **`agentWait` wording.** Source: acc-2 M10.
23. **`report-template.md` needs its `refs/` prefix** (S4 `:117`, `:170`; S5 step 1.15). Source: co-2 #8.
24. **Option A3 [UNVERIFIED].** Lint Check 11 can already be answered from the Makefile. Source: st-2 M-5.
25. **S1 counts.** S1 `:207` "14 of 46" should be 47, S1 `:210` "20 headings" should be 21, and the `:244` tally is off. Sources: co-1 #4, co-1 #5, qu-1 #8.
26. **S1 rule 4(b)** omits Ruling halt. Source: qu-1 #6.
27. **Bare verb forms** still appear in some prose. Source: qu-1 #10. This is related to note 1.
28. **S5 X-1 (`:255`) overstates crash-recovery.** It says crash-recovery "runs" `git stash` commands beyond `list`; it allows them (`Bash(git stash *)`, `SKILL.md:4`). Source: qu-2 M-6.
29. **S6 row 3 (`:31`) cites a private memory note** as evidence. Source: qu-2 M-7.
30. **Withdrawn:** tr-1 F6, on the crash-recovery `SKILL.md:25-27` citation, is not a finding. The citation is valid (Conflicts K-10).

## NB-4 Re-check

NB-4 re-check: PASS (10 of 10 reports)

Every report confirms the NB-4 fix at `scope-03:99`. The default allowlist includes `orchestration task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden. S2 `:7` and `:230` record this. The fix is pinned by SC-2 (S2 `:112`, S5 `:166`). The stale-count claims in B-01 to B-03 concern only the summary counts, which already read 75/25 at `gaps-and-questions.md:125`. They are not a failure of NB-4.

## Gate

|F_0| = 15

Gate status: FAIL

The gate fails because 15 blocking findings (B-01 to B-15) are open. A serialized fix pass must resolve every B-row; the Notes are optional. After the fix pass, re-run the Step 5.7 gate.
