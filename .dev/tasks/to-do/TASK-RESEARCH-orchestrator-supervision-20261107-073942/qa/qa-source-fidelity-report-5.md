## Cross-Source Contradiction Report

- **Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md` (1716 lines)
- **QA phase:** source-fidelity (cross-source contradictions), fix_authorization: false
- **Source files checked:** 4 (227 + 81 + 34 + 73 = 415 lines)
  - `BUILD-REQUEST.md` (227 lines)
  - `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md` (81 lines)
  - `.dev/issues/339/issue-summary.md` (34 lines)
  - `.dev/issues/339/analysis/analyze-worker-contract.md` (73 lines)
- **Date:** 2026-11-07
- **Known intentional records excluded from findings:** NB-4 exception record (report lines 13, 1645), the two `[CONTRADICTION]` markers (report lines 1095, 1563).

### Contradictions Found

| # | Type | Source File(s) and line | Report Section | Contradiction | Severity |
|---|---|---|---|---|---|
| 1 | Report-vs-Source | `seed-brief.md:68` (classification must be tested on inputs including "unpushed commits"); `issue-summary.md:10` (`/sc:close` only after checks that "nothing of value is uncommitted or unpushed"); `analyze-worker-contract.md:36` (F5: "All commits pushed" is missing from the five refusal conditions) | 3.1 "Safe to close" (report :393-395); step 1.3 `safe_to_close` (:1205) | The report's "worktree removable" recommendation relies only on the five refusal conditions at `WORKER-CONTRACT.md:108`. It has no unpushed-commit check: a Grep for `unpushed`, `pushed` and `ahead` over the whole report returns 0 matches. All three sources name unpushed commits as a required check, and the analysis says this is exactly the gap in the five conditions. As written, Phase 1 can recommend removing a worktree whose commits exist only locally. This breaks the "never lose work" safety rule. | CRITICAL |
| 2 | Report-vs-Source | `seed-brief.md:70` (trust layer = "typed messages, signed narrow grants"); `issue-summary.md:10` (comment 2: "same permission mode, fixed message types, signed narrow grants"); `analyze-worker-contract.md:47-55,62` (S1-S5; trust layer in a later phase) | 8 later-phases table (report :1287); exclusions (:1454, "OTP restart budgets ... moved to Phase 4") | The report defines its "Phase 4: trust layer" as bounded automatic recovery gated on Orca stop proof (an OTP-style restart budget). All three sources define the trust layer as cross-session message trust: the same permission mode, fixed message types and signed narrow grants. The report keeps the phase name but gives it a different feature. The report never mentions bypass mode, macaroon, Biscuit or `CCSESSION_PERMISSIONS`, so the sources' meaning of this phase is not recorded anywhere. | IMPORTANT |
| 3 | Source-vs-Source (hidden) | `issue-summary.md:6` (version 1 = `/sc:sweep` plus `/sc:close`; version 2 = signed grants plus orchestrator of orchestrators); `analyze-worker-contract.md:60-62` (Phase 2 = close; Phase 3 = trust layer plus orchestrator of orchestrators); `seed-brief.md:70` (later phases recorded "with its blockers") | 8 later-phases table (report :1283-1289); Problem Statement (:37) | The sources group the work in two incompatible ways: issue-summary puts `/sc:close` in version 1, while the analysis makes it Phase 2. The report follows neither. It uses a six-phase numbering (2 close, 3 resume, 4 trust, 5 orchestrator of orchestrators, 6 relay) that no source has, and it does not name the disagreement or say which source it follows. Line 37 also quotes the 40 h estimate, which includes the 14 h for `/sc:close`, without saying that this conflicts with the sweep-only first PR. The later-phases table also omits the blockers that `seed-brief.md:70` requires for each phase. | IMPORTANT |
| 4 | Report-vs-Source (unnamed departure) | `analyze-worker-contract.md:34` (F3: a stop recommendation is allowed on "a final turn without worker_done") | Classifier and stall proof (report :162, :368, :863); step 1.3 | The report treats a final turn without `worker_done` as a note only and calls this a "Phase 6 QA narrowing of Section C". That may be a valid narrowing, but it contradicts analysis F3, and the report never names F3 as the source it departs from. | IMPORTANT |
| 5 | Source-vs-Source (hidden) | `seed-brief.md:33,75`, `issue-summary.md:22`, `analyze-worker-contract.md:60` (all make `ccsession --list` a Phase 1 sweep input) | Data sources (report :171, :318, :459, :541, :1512) | The report excludes `ccsession --list` from the sweep's inputs and attributes the reason (it is not read-only) only to scope-02:165. Three sources make it a Phase 1 input. The exclusion may be correct, but the report does not name the conflict with those three sources. | IMPORTANT |
| 6 | Source-vs-Source (hidden) | `analyze-worker-contract.md:42` (F11: "reuse crash-recovery's signals rather than re-implementing them"); `analyze-worker-contract.md:60` (the sweep reads crash-recovery signals); `issue-summary.md:21` (the skill exists "to reuse for session signals"); `BUILD-REQUEST.md:21` (A4, extending crash-recovery, is rejected) | K2 (report :524); :1051 | The report writes a new scanner and re-implements `parse_session_log`. Rejecting A4 (extending the skill) does not rule out reusing its signals, which is what the analysis and the issue summary ask for. The report does not name this tension between `BUILD-REQUEST.md:21` and the other two sources, or explain why reuse is not possible. | IMPORTANT |
| 7 | Report-vs-Source | `BUILD-REQUEST.md:12` ("every Orca worker and ccsession"); `seed-brief.md:66,75` (person-started sessions appear in the first-phase report); `analyze-worker-contract.md:33` (F2: observe them) | Open questions (report :513, :631, :1197, :1503; GQ-09) | The report frames "whether to report person-started sessions at all" as an open owner decision. The sources already answer it for Phase 1: they appear in the report. Framing it as open also hides that research-notes AMBIGUITY 8 conflicts with these sources. | IMPORTANT |
| 8 | Report-vs-Source | `seed-brief.md:42` (CR-01 is the "approved child-worktree trigger rule"); `analyze-worker-contract.md:43` (F12 cites CR-01:12-21 and carries the rule into WC-11) | Open questions (report :546, :1554, :1639) | The report frames worktree-first versus trigger-based placement as open because "CR-01 [is] unread". Two sources record CR-01 as approved and give its content. The report reopens a decision the sources treat as fixed. | IMPORTANT |
| 9 | Report-vs-Source | `seed-brief.md:60` ("`.dev/tasks/` content is never classed as disposable"); `analyze-worker-contract.md:35` (F4) | Constraints 3.3 (report :455-471); safe-to-close rules (:393-396) | The rule that `.dev/tasks/` content is never disposable is missing from the constraints and from the safe-to-close rules. Grep for `disposable`, `valuable`, `untracked` and `never lose` finds no such rule; the only `.dev/tasks` hit is the staging checklist at :1483. Without it, an untracked task package could count as clutter in a "worktree removable" recommendation. | IMPORTANT |
| 10 | Report-vs-Source | `seed-brief.md:35` (HOW-WE-WORK "Orca coordination", lines 396-405, and its plugin copy change); `issue-summary.md:18` (same section listed) | Plan steps 1.20-1.23 (report :1273); :79 | The plan adds only the "Other commands" row to HOW-WE-WORK. Line 79 mentions an Orca-section edit, but no plan step carries it, so the change the seed brief requires to "Orca coordination" and its byte copy is dropped. | IMPORTANT |
| 11 | False attribution | `seed-brief.md:79` (the 6 h window question is still open for the owner) | Camunda finding (report :762); compare :397, :539, :1548 | Line 762 cites "the owner note at GQ-61 that the 6 h window bounds activity only". `gaps-and-questions.md:84` attributes that point to QA finding N-41, not to the owner. The report's own lines 397, 539 and 1548, and `seed-brief.md:79`, say the owner decision is still open. The report attributes to the owner a statement the owner did not make. | IMPORTANT |
| M1 | Report-vs-Source | `seed-brief.md:35,69`; `analyze-worker-contract.md:40` (F9: periodic sweep; also "renew idle subscriptions") | WC-14 draft G3 (report :1235-1237) | "On every coordinator wake" differs from the sources' "periodic sweep", and WC-14 leaves out F9's "renew idle subscriptions". | MINOR |
| M2 | Report-vs-Source | `analyze-worker-contract.md:40` (F9: the order is in no shipped file); `seed-brief.md:61` (installed primitives use installed paths only) | Row 3 (report :1499) | Cites the private memory note `coordinator-never-stop-polling.md` as WC-14's source; a shipped contract cannot point at a private memory file. | MINOR |
| M3 | Source-vs-Source | `BUILD-REQUEST.md:21` (A4 contradicted "by scope-03") | A4 rejection | scope-03 has 0 mentions of A4 or crash-recovery. The report silently follows scope-02 and research-notes:160 rather than naming the wrong citation. | MINOR |
| M4 | Source-vs-Source | `seed-brief.md:33,44`; `issue-summary.md:21`; `analyze-worker-contract.md:19` (all call sc-crash-recovery "read-only") | Correction C3 (report :569) | The report's correction attributes the wrong "read-only" claim only to scope-02, although three assigned sources make the same claim. | MINOR |
| M5 | Report-vs-Source | `issue-summary.md:10`; `BUILD-REQUEST.md:12` ("idle" used for all sessions) | Classes (report :52, :388) | The report limits "idle" to person-started sessions without noting the departure. | MINOR |
| M6 | Source-vs-Source | `seed-brief.md:21` ("analysis F1-F12") | Row C1 (report :567) | The analysis now has F1-F14; the report names only scope-01 and research-notes as sources of the count. | MINOR |
| M7 | Report-vs-Source | `seed-brief.md:33,68` (worker-list `attention` is a tested classification input) | Classifier (report :110) | The classifier does not use `attention`, and line 110 marks it [UNVERIFIED] guide text without naming the conflict with the seed brief. | MINOR |
| M8 | False attribution | `issue-summary.md:6` (the 40 h estimate) | Problem Statement (report :37) | "The issue estimates about 40 h": the estimate comes from the issue summary's analysis, not from the issue itself. | MINOR |

### Checks that passed

- WC-10 ("absence is never proof of death") is stated correctly (report :56, :461).
- A4 (extending sc-crash-recovery) appears only as rejected.
- The 6 h versus 72 h window conflict is named (report :397, :539, :612).
- The six versus seven classes conflict is named (report :9, :392).
- The #409 inventory is labelled DERIVED.
- Contract edits are sequenced after PR #422.
- WC-14 sits inside the Coordinator section.
- WC-6 ("a retry is a new Task") is kept.
- Later phases (`/sc:close`, resume, trust layer, orchestrator of orchestrators, relay) are kept out of Phase 1.

### Summary

- **Sources checked:** 4 (415 lines, each read in full)
- **Statements compared:** about 45
- **Contradictions by severity:** CRITICAL 1, IMPORTANT 10, MINOR 8
- **Blocking findings:** 11 (rows 1-11). The MINOR rows (M1-M8) are notes and do not fail the review on their own.
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read, Grep and Bash calls over the 4 sources and the report (report read in windows of 80 lines or fewer, plus targeted Greps); no web research.

Verdict: FAIL
