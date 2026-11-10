
## Prior blocking findings

Each prior blocking id from `round1.md:14,18,20,26,29` is re-checked against the AFTER text only.

| id | status | why (AFTER text; candidate line numbers) |
|---|---|---|
| L1 | resolved | Every sub-claim that passed the grading check in `round1.md:39-288` is now consistent with the AFTER text, see the sub-claim list below. Sub-claims that were never blocking-grade (a requirement the document does not state) stay as follow-up candidates. |
| L5 | resolved | AC-C1 is now a separate code block with an unescaped ERE alternation, `orca-ide` matched in any form, seven `orca` verbs, and exemptions for `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` (candidate 178-184, SA-2 at 147). I ran the command text on a sandbox control tree: it printed the `orca orchestration` line in a command file and the `orca-ide status` line in a second command file, and printed nothing for the two exempt core files or for `skills/ccsession-tag/`. P0 now runs the smoke runs first and writes the contract only after AC-0.4 passes (candidate 158). |
| L7 | resolved | Step 3 now waits 240000 ms and is repeated with step 2 between waits (candidate 190), so the interval between `worker-show` observations is at most 4 minutes plus call time, inside the 5-minute limit of step 2 (candidate 189). The 240 s wait also matches AC-4.3 (candidate 218). |
| L13 | resolved | Section 1.1 now ends "plus the defect fixes section 3 names (SA-4)" (candidate 16), and SA-4 lists the explain, roadmap, validate-roadmap, validate-tests, business-panel, load and contract-gap fixes (candidate 149). An implementer following 1.1 no longer skips them. |
| L16 | resolved | The troubleshoot row now tells the coordinator "no `--depth deep` with fewer than 10 words until P2" (candidate 91), which removes the STOP that asks a person. The 10-word STOP is evidenced at `INV-B:239` (the `SKILL.md:57` citation itself is UNVERIFIED by me). |

L1 sub-claims, checked one by one (finding ids from `round1.md`):

- t1b-1 F1, t2-1 F2, t3-1 F2, t3-2 F2 (AC-1.1 against 13 versus 37 commands): resolved. AC-1.1 now tests only the commands named in the P1 row except load (candidate 203); section 3 says load and ready commands with no fix get neither section nor flag (candidate 76).
- t1b-1 F2, t2-1 F17 (file-valued output flags): resolved by "where the output flag names a file, the contract is `<file>.return-contract.yaml`" (candidate 62).
- t1b-1 F3, t3-2 F18 (adversarial path): resolved by "where the command's section 3 row names a different path (adversarial), that path applies" (candidate 62).
- t1b-1 F4, t3-1 F5, t3-2 F8 (empty or unknown status read as succeeded): resolved by WC-5 (candidate 63).
- t1b-1 F5, t3-2 F1 (P0 step 3 and step 4 demanded a contract no P0 command writes): resolved for the path and the YAML assertion (candidate 190-191, 202). A residual outcome-match wording issue is N3 below.
- t1b-1 F6, t2-1 F7, t2-1 F8, t3-2 F4 (retry and fresh directories): resolved for directory-valued outputs by 2.3 and WC-3 "the contract of the last run is the one reported" (candidate 61, 73). The file-valued case is N4 below.
- t1b-1 F7, t3-2 F15 (ask path against AC-2.2 and `agentWait`): resolved by the AC-2.2 brief wording and the step-2 exception (candidate 189, 208).
- t1b-1 F9, t1b-1 F11, t3-1 F13, t3-2 F5, t3-2 F19 (authorising flag, fixed output paths): resolved by WC-9 "where the command has no such flag, the action stays off" and WC-11/2.3 "runs one Task per worktree at a time" and "depends on the previous such Task" (candidate 67, 69, 73).
- t2-1 F11, t3-1 F14, t3-2 F9 (SA-1 against WC-1, no owner): resolved by SA-1 "every prompt of a command" (candidate 146) and WC-1 "checked by 7.2 step 1 in every phase" (candidate 59), where step 1 requires `state: ready`.
- t2-1 F16, t3-1 F20 (Orca file check stated as fact): resolved by "Orca is assumed not to check the file (UNVERIFIED 3)" (candidate 62, 282).
- t2-1 F22 (stall called invisible): resolved by WC-2 "a stall shows only through `agentWait` or a missing report" (candidate 60).
- t3-1 F6 (E3 cites a skill-direct contract): resolved, E3 now says the run "used the Agent-tool route" (candidate 23).
- t3-1 F1 (generated report paths): resolved by the WC-4 exception "except the generated paths section 3 names, which the worker reports in `--report-path`" (candidate 62).
- t3-2 F7 (subagent wrapper not checked): resolved, step 5 now also searches for an Agent-tool call (candidate 192).
- t3-2 F14 (step 6 against a shared worktree): resolved, step 6 is limited to a single-worker run (candidate 193).
- Not changed and not blocking-grade (each states a requirement the document never states, or a design choice, so under the grading check it is Medium): t1b-1 F12 (worker tool-permission prompts have no requirement), t2-1 F10 (two code-editing workers can break each other's build without sharing a file), t3-1 F12 (no bound or escalation for `ask` resumption), t1b-1 F13 and t3-2 F16 (no contract version field), t3-2 F11 (a FAIL audit is sent as succeeded, by design, with the verdict in the body), t3-2 F20 (which question a command with two gates carries), t1b-1 F17 (P1 title says "no gate" over commands that refuse a mode). They are carried under follow-up candidates and do not keep L1 open.

## Findings on changed lines

Only changed lines and the text that depends on them are covered. All four findings below are non-blocking: each needs the implementer to choose between two readings the text allows.

=== REQUIREMENTS ANALYSIS ===

**N1** (Wiegers, Adzic) MAJOR graded Medium, origin=changed, priority Medium. The new WC-5 line (candidate 63) sends `--outcome failed` "for a missing, empty, unparseable or unknown-status report" and `succeeded` only when "its `status` is `succeeded` or `partial`". Section 3.1 (unchanged, candidate 79) says the worker "reports the named file until Phase 1 adds the contract", and those named files are Markdown with no `status` key (troubleshoot `REPORT.md` is not YAML, `INV-B:242`; cleanup-audit and index-repo write Markdown). One reading: a successful troubleshoot smoke run in P0 is reported `failed` because its report has no `status`. The other reading: WC-5 only applies once the contract exists. The text does not say which, and the P0 smoke step 3 (candidate 190) cannot be passed on the first reading. Recommendation: one sentence in WC-5 saying the mapping applies to the WC-4 contract, and that a pre-contract report is judged by the command's own result. Not blocking: the sentence "an implementer builds X and X is wrong" needs a guess about which reading is picked. Quote of the changed line it depends on: "`--outcome failed` for `failed` or `blocked`, and for a missing, empty, unparseable or unknown-status report".

**N2** (Wiegers) MAJOR graded Medium, origin=changed, priority Medium. WC-4 now says "Commands that already write a contract keep their fields and add the missing ones; a status word outside the four counts as `failed` (WC-5)" (candidate 62). The inventories name only `status` (`INV-B:272`) and do not list the status vocabularies the existing contracts use (brainstorm `INV-A:97`, workflow, adversarial, cli-portify), so whether a correct existing contract uses one of the four words is UNVERIFIED. If one does not, a successful run is reported `failed`. Recommendation: list the existing words once, or map them, in `WORKER-CONTRACT.md` during P0. Not blocking: the evidence for a wrong outcome is missing, not contradicted.

=== ARCHITECTURE ANALYSIS ===

**N3** (Fowler, Nygard) MINOR, origin=changed. Step 3 pass condition (candidate 190) still reads "its `--outcome` matches the contract's `status` under WC-5" and adds "(in P0, the command's existing report file)" only for the path. In P0 no smoke command except adversarial and workflow has a contract with a `status` (see N1). Recommendation: in P0 compare the outcome with the command's own result. Note only.

**N4** (Newman, Hohpe) MINOR, origin=changed. WC-4 adds `<file>.return-contract.yaml` for file-valued output flags (candidate 62), but section 3 still defines "Contract" as `<output-dir>/return-contract.yaml` (candidate 76) and 2.3 and WC-6 speak of an "output directory" and a "fresh output directory" for retries (candidate 61, 73). For file-valued commands (tdd, init-lite, spec-panel after P2) the retry rule is stated for directories only, and init-lite's row still says "Re-run overwrites its marked report" (candidate 87). The coordinator can supply a fresh file path, but the text does not say so. Recommendation: say "output path" instead of "output directory" in 2.3 and WC-6. Note only.

## Guard Condition Boundary Table

Scoped to guards on changed lines (command bullet 5). Classes left out are given one line of reason. Nygard builds, Crispin checks completeness, Whittaker attacks the entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome guard | WC-5, candidate 63 | Zero/Empty | empty report file | not `succeeded`/`partial` | `--outcome failed` | OK |
| WC-5 outcome guard | WC-5, candidate 63 | Sentinel Value Match | status word outside the four | not in the set | `failed` (WC-4, candidate 62) | OK |
| WC-5 outcome guard | WC-5 against 3.1, candidate 63, 79 | Legitimate Edge Case | pre-contract Markdown report with no `status` | ambiguous | not specified for P0 or the 3.1 interim | GAP (N1, Medium) |
| WC-4 contract location | WC-4, candidate 62 | Typical | `--output <dir>` | directory rule | `<dir>/return-contract.yaml` | OK |
| WC-4 contract location | WC-4, candidate 62 | Legitimate Edge Case | `--output <file>` | file rule | `<file>.return-contract.yaml` | OK |
| WC-4 contract location | WC-4, candidate 62 | Divergence | generated path (workflow, research) | exception clause | worker reports the path in `--report-path` | OK |
| WC-9 flag guard | WC-9, candidate 67 | Legitimate Edge Case | command with no authorising flag | flag absent | action stays off | OK |
| 2.3 fixed-path guard | 2.3 and WC-11, candidate 69, 73 | Maximum/Overflow | a second Task on a fixed-path command | dependency rule | depends on the previous such Task | OK |
| P0 gate | P0 row, candidate 158 | Legitimate Edge Case | AC-0.4 fails | gate false | contract not written; "a failure here reopens section 1" (candidate 202) | OK |
| Step 3 wait | 7.2 step 3, candidate 190 | Maximum/Overflow | wait of 240000 ms | repeats | step 2 between waits | OK |
| Troubleshoot brief guard | 3.1 troubleshoot, candidate 91 | One/Minimal | `--depth deep` with 9 words | brief forbids | not dispatched until P2 | OK |

Left out: a Zero/Empty row for WC-9, the 2.3 guard and the P0 gate, because a missing flag, a first Task and an unrun check are the same as the typical case there.

Pipeline Dimensional Analysis and the correctness-focus registries do not apply: the changed lines hold no multi-stage count pipeline and `--focus correctness` was not requested.

## Follow-up candidates

Medium (warnings, not blocking): N1, N2.
Minor notes: N3, N4, and these unchanged-origin notes: no requirement for worker tool-permission prompts (t1b-1 F12); two code-editing workers can break each other's build without sharing a file (t2-1 F10); no bound or escalation for `ask` resumption (t3-1 F12); no contract version field (t3-2 F16); a FAIL audit is sent as `succeeded` (t3-2 F11); no rule for which question a two-gate command carries (t3-2 F20); P1 titled "no gate" over commands that refuse a mode (t1b-1 F17); "paid external run" in WC-9 is undefined; the other non-blocking ids of `round1.md:367-383` (L2 to L22 less the blocking ones) keep their round-1 grade and are not re-opened.

Whether to open an issue for these is a question for the user, once per loop. This run is not `--unattended`, but the reviewer could not ask in this worker context, so the question is passed to the coordinator and no issue was created.

## Coverage

scoped PASS: changed lines + prior blockers. Covered: all 21 hunks of the diff, every prior blocking finding (L1, L5, L7, L13, L16) and all sub-claims of L1, SA-1/SA-2/SA-4 and WC-1 to WC-11 as they depend on changed lines, the AC-C1 command by a sandbox positive control, section 1.1, 2.3, 3.1 and 6/7 rows that quote changed lines. Not covered: whole-document assurance (a separate, labelled first review would be needed), and every citation into files outside `inventory/` (UNVERIFIED). The reviser's per-finding byte report and fix map were not supplied to this run; the file grew from 57763 to 59727 bytes (+1964), and I could not attribute bytes to finding ids.

## Reviser brief

No blocking finding is open, so no ids are listed. (Rules, as the Review Loop states them: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report bytes before and after and bytes added and deleted per finding id.) No brief clause was overridden.

## Findings block

```findings-v1
{"id": "N1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "and for a missing, empty, unparseable or unknown-status report", "anchor2": "the worker reports the named file until Phase 1 adds the contract", "refs": ["WC-5", "3.1", "AC-0.4"], "claim": "A pre-contract Markdown report with no status can be read as failed under WC-5, so a successful P0 troubleshoot smoke run may be sent as failed."}
{"id": "N2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "a status word outside the four counts as `failed` (WC-5)", "refs": ["WC-4", "WC-5"], "claim": "Existing contracts' status words are not listed, so a correct existing contract could be reported failed."}
{"id": "N3", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "its `--outcome` matches the contract's `status` under WC-5", "refs": ["7.2", "AC-0.4"], "claim": "P0 step 3 compares the outcome with a status that most P0 commands do not write."}
{"id": "N4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "an output directory no other Task uses", "anchor2": "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`", "refs": ["WC-4", "WC-6", "2.3"], "claim": "Retry and contract-location wording covers directories only while some commands take a file."}
{"prior": "L1", "status": "resolved"}
{"prior": "L5", "status": "resolved"}
{"prior": "L7", "status": "resolved"}
{"prior": "L13", "status": "resolved"}
{"prior": "L16", "status": "resolved"}
```

verdict: PASS
