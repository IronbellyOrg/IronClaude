# QA Report — Fix Cycle verification (repeat cycle 1, last allowed fix pass)

**Topic:** Orchestrator mode Phase 1 research report (issue #339)
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 2 (repeat cycle 1; verifies C1-01 to C1-05)
**Fix authorization:** false (report not edited)
**Inputs:** `qa/qa-consolidated-findings-phase6-cycle1.md`, `qa/qa-fix-log-cycle1.md`, `RESEARCH-REPORT-orchestrator-mode.md`, `qa/qa-fix-verification.md` (regression check), `research/research-notes.md`, `gaps-and-questions.md` (task root; there is no `research/gaps-and-questions.md`)

---

Report length now: 1716 lines (`wc -l`). Line numbers below are current; the findings file used the 1715-line numbering (most cited lines moved by +1).

## Original findings (C1-01 to C1-05)

| ID | Result | Evidence (checked in the report and in the cited research) |
|---|---|---|
| C1-01 | RESOLVED | A1 Description `:900` now reads "The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep run`; `report.py` renders and writes the dated report and the skill reads the result." This matches the A1 diagram `:932-933`, step 1.5 `:1207` ("the only write") and step 1.15 `:1227` (no `Write`/`Edit`; "`report.py` renders and writes the report, step 1.5; the skill only reads it"). Grep for "skill writes" / "writes the report": only A2 `:974` (model-driven option, its own design) and A3 `:1001` (left unchanged as the finding instructed). |
| C1-02 | RESOLVED | Step 1.3 `:1205`: "The policy dimension ... is computed for every row independently of the class (GQ-96 ...): a blocked implement contract gets class waiting on a person (a) from rule 1 and policy frozen, and is listed under (b) too. Rule 4b sets the class only for rows with no earlier match (the `failed` contract ..., the ledger and the ready-Task cases)." S3.1 new bullet `:391` uses the same words and adds "so a frozen `/sc:implement` plan is never hidden (`WORKER-CONTRACT.md:133-136`)". Step 1.8 `:1215` fixture: "asserts both outputs: class waiting on a person (a) from rule 1 and policy frozen, so it is also listed under (b); GQ-96". GQ-96 row `:561` aligned. Evidence checked: `research-notes.md:190` (first match wins), `:192` (rule 1), `:197` ((b) "reported under the policy dimension ... `data-dictionary.md:27`"); `gaps-and-questions.md:119` (GQ-96 resolved, "dimensions are independent"). The 4b-contract detection (frozen when the contract is `blocked`) is now a policy detection only; the class path for `blocked` is rule 1. See MINOR notes N-1, N-2. |
| C1-03 | RESOLVED | SC-1 `:438` "How it is checked" now describes the snapshot diff (path, size, `st_mtime_ns`, SHA-256), `HOME` and `XDG_STATE_HOME` inside the isolated root, only the dated report and a new `--output` directory may differ, subprocess entry points patched with `side_effect=AssertionError` (step 1.11). Source cell: "Subprocess half: `tests/cli/reflect/test_contract_status_cli.py:44-66` pattern ... Snapshot diff: plan decision, no in-repo precedent". Matches step 1.11 `:1218` and Integration Checklist `:1458`. See MINOR note N-3 for the 8.1 row `:1305`. |
| C1-04 | RESOLVED | The "could not determine" wording is present, word for word, at step 1.3 `:1205` ("... Phase 1 prints \"terminal releasable: could not determine (result read not observable); Orca: reclaimable, next action release\", with no proxy for the read"), S3.1 `:394` and S5 `:680`. No proxy added. The three places now give the same condition. Grep for `reclaimable`/`terminalState` finds no other place that states the releasable condition. See MINOR note N-4. |
| C1-05 | RESOLVED | Step 1.0b `:1197`: "GQ-11 rule ID (S9 row 9), with the WC-14 wording, is a hard gate: steps 1.17-1.19 do not start until the owner's answer on GQ-11 is recorded; \"working default accepted\" counts only when the owner says it"; closing sentence "other unanswered decisions (all except GQ-11) keep the working default". Rollback `:1279` uses the same gate words, points to step 1.0b, and keeps "WC-14 does not land on the working default alone". Step 1.17 `:1235` ("WC-14 is the working default ..., pending the owner decision") and S9 row 9 `:1505` do not contradict a gate that holds 1.17 until the answer. Evidence: `gaps-and-questions.md:34` (GQ-11 "open (owner decision)", "WC-14 is the working name"). See MINOR note N-5. |

## Regression check (items RESOLVED in `qa/qa-fix-verification.md`)

I re-checked every previously RESOLVED item whose report text these edits touched (A1 Description, S3.1, SC-1, S4.5 GQ-96, S5 `:680`, steps 1.0b, 1.3, 1.8, Rollback).

| Prior item | Touched by | Still passes? | Evidence |
|---|---|---|---|
| P6-07 (rendering owner) | C1-01 | Yes, strengthened | `:900`, `:932-933`, `:1207`, `:1227` all say `report.py` writes, skill reads. |
| P6-08 (frozen plan is kind (b)) | C1-02 | Yes | `:351`, `:507` ("The frozen-plan test at `WORKER-CONTRACT.md:133-136` gives kind (b), never (a)") still hold: the (a) of a blocked implement contract comes from rule 1 (the contract's question), not from the frozen-plan test, which still gives (b). Wording note N-2. |
| P6-16 (rule 4 sub-case detection, one fixture each) | C1-02 | Yes | 4a, 4b-contract, 4b-ledger (row 81b) and 4b-Task (row 81c) detection remain in `:1205`; step 1.8 `:1215` still has one fixture per sub-case. |
| P6-43 (classifier signatures) | C1-02, C1-04 | Yes | `classify(...) -> Classification` and `safe_to_close(...) -> SafeToClose` unchanged in `:1205`. |
| P6-46 (step 1.11 snapshot diff) | C1-03 | Yes | Step 1.11 `:1218` unchanged; SC-1 now agrees (N-4 of the prior report closed). |
| P6-36 (step 1.0b gates) | C1-05 | Yes, stricter | `:1197` still records answers in `artifacts/owner-decisions.md`, reads APPROVED.md, and names the steps each decision blocks. |
| P6-39 (GQ-11 wording "add WC-14, or reuse the unused WC-1 ID") | C1-05 | Yes | `:1197` "GQ-11 rule ID", `:1279` "WC-14 as a new ID"; grep finds no "override WC-1". |
| P6-49 (Rollback content) | C1-05 | Yes | Rollback table `:1267-1275`, report retention `:1277`, WC-14 owner gate `:1279`. |
| P6-20, P6-21 (steps 1.17-1.19 text and #422 gate) | C1-05 | Yes | `:1190`, `:1234`, `:1235-1237` unchanged. |

Regressions: **none**. No item that was PASS at the previous verification is FAIL now.

## Required preserved items

| Item | Present | Evidence |
|---|---|---|
| NB-4 exception record | Yes | `:13`, `:1645` |
| [CONTRADICTION] marker 1 | Yes | `:1095-1097`, resolution `:1099` |
| [CONTRADICTION] marker 2 | Yes | `:1563-1565`, resolution `:1567` |

## New findings introduced by the fixes

No new blocking finding. I looked for at least five defects in the fixes and found five, but each is wording, test coverage of a stated rule, or an unreached enum value, with the rule itself stated correctly in the plan; by the review severity rule they are MINOR notes and do not count toward `|F_2|`.

| # | Severity | Location | Note |
|---|---|---|---|
| N-1 | MINOR | Steps 1.3 `:1205`, 1.5 `:1207`, 1.6 `:1208`, 1.12 `:1219` | "Listed under (b) too" is stated in step 1.3 and S3.1, but no step names who computes the `policy` field (`classify` returns `Classification`, which has no policy field; `safe_to_close` returns `SafeToClose`), and step 1.6 `waiting.b` and the step 1.12 report test do not say the (b) list is "waiting_kind b, or policy frozen". The freeze is not hidden even if built from `waiting_kind` only, because Retained problems lists "policy frozen" (`:1207`) and the Sessions table shows the policy column. Suggest: name the (b) list rule in 1.5/1.6 and add one 1.12 case. |
| N-2 | MINOR | G-B row `:507` | "gives kind (b), never (a)" is literally true of the frozen-plan test, but a reader may take it as contradicting `:391`/`:1205` (a blocked implement contract is class (a) by rule 1). Suggest adding "(a blocked contract is also (a) by rule 1)". |
| N-3 | MINOR | 8.1 gap map `:1305` | "Read-only proof tests ... Allowlist and `side_effect=AssertionError` tests" still names only the subprocess half of step 1.11; the snapshot diff is omitted. True but incomplete; same staleness C1-03 fixed at SC-1. |
| N-4 | MINOR | Step 1.2 `:1204`, step 1.9 `:1216`; `research-notes.md:218` | After C1-04, `SafeToClose.terminal` can never be "yes" (as `worktree` already could not), but step 1.2 still lists "yes" as a value, and step 1.9 has no case for the new "terminal releasable: could not determine (result read not observable)" output. Also, Section C says terminal releasable holds "only after the session's result has been read (rule 1/6)", which points at the sweep's own contract read; the report narrows that on WC-10 grounds without saying it narrows Section C (compare prior note N-7). The orchestrator chose this option deliberately; record the narrowing in S9 or step 1.3. |
| N-5 | MINOR | Rollback opening `:1265`; S7 `:1057`; S8 `:1392`; step 1.0b `:1197` | `:1265` still says Phase 1 "changes a shared contract (WC-14 and the never-as-worker list) on working defaults", and `:1057`/`:1392` say the plan "uses working defaults for ... GQ-11". These are defensible (WC-14 G7 still rests on the GQ-10 default; WC-14 is the working name) but read against the `:1279` hard gate in the same section. Step 1.0b also does not say whether steps 1.20-1.29 (including the 1.24b CHANGELOG entry that names WC-14) wait while GQ-11 is unanswered; the existing #422 path (`:1190`, `:1234`, move 1.17-1.19 to a follow-up PR) is the likely answer and could be named. |

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | C1-01 fix applied and correct | PASS | Read `:893-937`; Grep "skill writes / writes the report / report.py" |
| 2 | C1-02 fix applied and correct | PASS | Read `:356-445`, `:1194-1233`; Grep GQ-96; Read `research-notes.md:186-221`; Grep `gaps-and-questions.md:119` |
| 3 | C1-03 fix applied and correct | PASS | Read `:438`; Grep SC-1 / step 1.11 references (`:1305` note N-3) |
| 4 | C1-04 fix applied and correct | PASS | Grep `releasable` / `reclaimable`; Bash print of `:680`; Read `research-notes.md:218` |
| 5 | C1-05 fix applied and correct | PASS | Read `:1197`, `:1236-1279`; Bash print of `:1235`, `:1392`, `:1051`, `:1190`, `:1234`, `:1370`; Grep GQ-11; `gaps-and-questions.md:34` |
| 6 | Regression check against `qa/qa-fix-verification.md` | PASS | Read its `:14-83`; re-checked P6-07, P6-08, P6-16, P6-20, P6-21, P6-36, P6-39, P6-43, P6-46, P6-49 in the current report |
| 7 | Preserved items (NB-4, two [CONTRADICTION] markers with resolutions) | PASS | Grep plus Bash print of `:13`, `:1095-1099`, `:1563-1567`, `:1645` |
| 8 | New issues introduced by the fixes | PASS (5 MINOR notes, 0 blocking) | See table above |

**Set of items that PASS:** C1-01, C1-02, C1-03, C1-04, C1-05; regression check (P6-07, P6-08, P6-16, P6-20, P6-21, P6-36, P6-39, P6-43, P6-46, P6-49 all still pass); preserved items (NB-4 record, [CONTRADICTION] marker 1 and 2 with their resolutions).

## Summary

- Original blocking findings: 5; RESOLVED 5; OPEN 0
- New blocking findings: 0; new MINOR notes: 5 (N-1 to N-5, not counted)
- Regression: none (no PASS-to-FAIL item)
- Monotonicity: `|F_2| = 0 < |F_1| = 5`, no halt
- Issues fixed in-place: 0 (fix authorization false; the report was not edited)

**Open blocking count: `|F_2| = 0`**

## Confidence gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 15 | Glob: 1 | Bash: 4 (all read-only `sed -n` / `wc -l` prints of cited report lines)
- No web research was needed.
- UNCHECKED items: none. UNVERIFIABLE items: none.
- Limits: I did not re-read the whole 1716-line report; I read every section the five findings and the fix log name, and grepped for other places that state the same rules (rendering owner, releasable condition, SC-1 method, GQ-11 gate, policy and kind (b)).

## Recommendations

- Proceed. Optional before the plan stage: fold N-1 (name the (b) list rule and test it) and N-4 (record that terminal releasable narrows Section C `:218`) into the `/sc:workflow` plan; N-2, N-3 and N-5 are wording.

## QA Complete

## Verdict: PASS
