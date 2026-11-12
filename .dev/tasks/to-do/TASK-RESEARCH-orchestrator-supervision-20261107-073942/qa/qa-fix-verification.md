# QA Report: Fix Verification (Phase 6, report lenses)

**Topic:** Orchestrator mode Phase 1 (issue #339), research report
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 1
**Fix authorization:** false (report only; the report was not edited)
**Report:** `RESEARCH-REPORT-orchestrator-mode.md` (1715 lines at check time)
**Inputs:** `qa/qa-consolidated-findings-phase6.md` (|F_0| = 49), `qa/qa-fix-log.md`

Status: COMPLETE (49 of 49 findings checked)

## Per-finding results

| ID | Result | Evidence (report line numbers are current, 1715-line file) |
|---|---|---|
| P6-01 | RESOLVED | Row 21 `:1516` uses the space form; 3.1 `:342`, step 1.15 `:1226` and step 1.16 `:1227` use the same literals; the `:1562` marker still has both versions, and the resolution is at `:1566`. Precedents checked in source: `sc-swarm-wizard-protocol/SKILL.md:7` `Bash(uv run superclaude swarm *)`; `sc-crash-recovery/SKILL.md:4` space-form `Bash(git status *)` and others. The `command -v` call is gone: the fallback triggers on the PATH call failing (`:342`, `:1226`). |
| P6-02 | RESOLVED | `:342` tags the bare form only [CODE-VERIFIED for the bare form] and calls the fallback a new design (B-19). `sc-reflect-protocol/SKILL.md:63-64` shows only `superclaude reflect contract-status ...` (checked in source). |
| P6-03 | RESOLVED | `:1711-1715`: 43 = 24 + 18 + 1, as of assembly. I counted the bullet contents: 24 and 18 (12 `qa-synthesis-*`). Phase 6 files are excluded. |
| P6-04 | RESOLVED | `:1696-1701` carry the line counts 299/317/230/275/310/233 and no "planned" or "this file" text; the `:1703` note is labelled history. |
| P6-12 | RESOLVED | SC-3 `:439`, step 1.4 `:1205` (the "one named exception"), step 1.10 `:1216` (exact tuples, including `("orca-ide","worktree","ps","--json")`) and the Integration Checklist `:1459` all agree. |
| P6-15 | RESOLVED | Step 1.3 rule 3 `:1204` says it is not buildable from a named field and uses synthetic fixtures only; SC-4 `:440` and S9 row 81a `:1589` agree. New MINOR note N-2 below: rule 2's live reachability. |
| P6-16 | RESOLVED | `:1204` gives detection for 4a, 4b-contract, 4b-ledger (not buildable, row 81b `:1590`) and 4b-Task (no creator field, row 81c `:1591`); step 1.8 `:1214` has one fixture per sub-case. |
| P6-17 | RESOLVED | `:1204` defines activity as the transcript `*.jsonl` mtime from `os.stat`, and routes "person session, active" by rule 7. This matches `research-notes.md:198`, `:202` (read). |
| P6-18 | OPEN (partial) | Rule 6 and the worktree-removable half are fixed in `:1204`. The terminal-releasable half is not. 3.1 `:393` still requires "the session's result has already been read" (Section C, `research-notes.md` terminal releasable "only after the session's result has been read (rule 1/6)"). Step 1.3 `:1204` computes terminal releasable from `terminalState` + `nextAction` only, with no proxy and no could-not-determine rule. The two sections give different conditions for "terminal releasable: yes". Fix: in step 1.3, add "and the sweep's own contract read succeeded (rule 6 sense)" or print could not determine. |
| P6-19 | RESOLVED | Step 1.6 `:1207` gives each option's type and default, a version-1 JSON schema, exit codes 0/1/2, `--output` rejected outside `<root>/.dev/`, `--root` limited to fixed patterns with no symlinks out, and the new `test_cli_contract.py`. MINOR note N-3: the row key list leaves out the session `id`. |
| P6-42 | RESOLVED | Step 1.4 `:1205` gives both signatures, the raise-then-map rule, the caught exception types and the uncaught `ValueError` for a disallowed argv. This matches `reflect/config.py:64-78`, `:103-109`. |
| P6-43 | RESOLVED | Step 1.3 `:1204` names `classify(...) -> Classification` and `safe_to_close(...) -> SafeToClose`, with the types in `models.py`. |
| P6-44 | RESOLVED | Step 1.5 `:1206` names `render` and `write_report`, the two write primitives, and says `commands.py` builds the JSON. |
| P6-45 | RESOLVED | Step 1.2 `:1203` lists the dataclasses, fields and constants, the str-vs-Enum decision, and the ten dimensions. The dimensions match `scope-04-409-layout.md:177-190` (read). |
| P6-46 | RESOLVED | Step 1.11 `:1217` uses a snapshot diff with HOME and XDG moved inside, lists the primitives covered, patches subprocess, and states that there is no precedent. MINOR note N-4: SC-1 `:437` still describes the old patch method. |
| P6-48 | RESOLVED | The brace form is in step 1.4 `:1205`, 3.1 `:356`, step 1.6 and step 1.8 `:1214`; the S2.6 diagram `:297` uses `*/*`. Grep for `.dev/tasks/*/progress` returns 0. |
| P6-23 | RESOLVED | The end-to-end item `:1473` and the WC-14-vs-G1-G7 item `:1474` are present. |
| P6-05 | RESOLVED | Grep `\bOQ-\d+` over the report returns 0 matches. The cross-references are keyed to S9 rows (for example `:1393` "S9 row 98a" and `:1504` row 9). |
| P6-06 | RESOLVED | S7 `:1087-1092` is now a short Recommended approach that points to Section 8 (steps 1.0a-1.29) and Section 5 (context), followed by the Rationale tables `:1058-1085`. |
| P6-07 | RESOLVED | `:1089` and the A1 diagram `:931-932` say `report.py` renders and writes the report and the skill only runs the CLI, with no `Write`; step 1.15 `:1226` adds no `Write` or `Edit`. A2 `:973` and A3 `:1000` keep their own designs, as they should. |
| P6-08 | RESOLVED | `:351` and `:506` (the latter: "kind (b), never (a)") put the frozen plan in kind (b). No "kind (a)" frozen-plan text remains. |
| P6-09 | RESOLVED | K1 `:522` reads "Important (resolved)"; `:172`, `:1306` and `:1645` agree. |
| P6-10 | RESOLVED | `:651` says every `orca-capabilities.md:122-130` cite in S5 is guide or help text; the cites at `:692`, `:702`, `:720`, `:756` and `:817` carry `[UNVERIFIED — Orca guide]`. `host_unavailable` is cited as `:124` at `:692` and `:743`. Grep for "verified codebase rule" returns 0. |
| P6-11 | RESOLVED | 3.1 `:397`, `:465` and G7 `:513` cite `:46` for the naming rule only and call `.dev/` a working default (GQ-10). Grep for "Parallel-safe" returns 0. |
| P6-13 | RESOLVED | Step 1.4 `:1205` sets 50 `worker-show` calls, a 90 s budget under the 120 s Bash timeout, and an explicit Bash timeout of 120000 ms; at the bound, rows get `unscanned: call bound reached` and the report is still written. The skill passes the timeout (`:1226`). The step 1.10 test is at `:1216`; 8.1 GQ-99 `:1330` and S9 row 63 `:1559` give the same resolution. |
| P6-14 | RESOLVED | `:56` reads "Orca's stall proofs". `:162`, the 3.1 diagram `:366-368`, R2 `:862`, step 1.3 `:1204` and row 70 `:1577` limit rule 2 to Orca `exited` or an Orca-observed exit; a transcript-only final turn is a note. MINOR note N-7: Section C `research-notes.md:193` still allows a transcript "proved final", so the report narrows the canonical rule on WC-10 authority, and only `:162` and `:1577` say so. |
| P6-20 | RESOLVED | Step 1.17 `:1234` has the G1-G7 text, with G3 "On every coordinator wake". Step 1.19 `:1236` gives the literal `RULE_PHRASES["WC-14"]` tuple, the 9-entry `NEVER_AS_WORKER`, the rename of `test_never_as_worker_list_names_all_seven_commands` and the new phrase. G6 is an owner decision (`:1371`). I checked the facts in source: `test_worker_contract.py:245-254` holds 8 entries, the `:545` test name is as quoted, `# Coordinator rules` is at about `:163`, and the never-as-worker phrase matches `WORKER-CONTRACT.md:23`. |
| P6-21 | RESOLVED | Dependencies has a #422 row `:1189` (gates steps 1.17-1.19, with two orders) and a #409 re-diff gate `:1188`. Step 1.16a `:1233` runs `gh pr view 422 --repo IronbellyOrg/IronClaude`. GQ-62 is placed inside Phase 1 at `:545`, `:1324`, `:1369` and row 52 `:1548`. Whether #422 touches steps 1.21-1.23 is disclosed as not checked, and step 1.16a handles it. |
| P6-22 | RESOLVED | The step 1.4 live check `:1205` gives the command, a pass rule (exit 0, 90 s budget, expected class per recorded state, no probe-error rows) and `artifacts/sweep-live-check-1.4.json`. Step 1.29 `:1258` gives a pass rule and `artifacts/sweep-help-pipx.txt`. MINOR note N-5: the step 1.4 acceptance runs `superclaude sweep run`, which does not exist until steps 1.6-1.7. |
| P6-24 | RESOLVED | S5 `:831` says that of D1, D3 and D4 only D1 contradicts WC-10, and lists D5 and D6 as separate rejections; S4.8 `:616` matches. |
| P6-25 | RESOLVED | `:36` names the question's six classes and says Section C adds fenced as the seventh (rule 3, `research-notes.md:194`; rule 3 confirmed in source). `:1393`, `:1622`, step 1.9 `:1215` and X-7 `:1430` agree. OQ-13 is now S9 row 98a, still open. |
| P6-26 | RESOLVED | The Effort basis `:1050` marks the grades [UNVERIFIED] judgment and counts the steps: 34 = 2 + 7 + 6 + 3 + 4 + 7 + 5, which matches the 1.0/1A-1F headings `:1191-1250`. It cites the ~20 h figure (`issue-summary.md:6`), puts hours in S9 row 81d, and says the recommendation does not rest on effort. |
| P6-27 | RESOLVED | S2.4 rows `:251-260` anchor `sc-issue-command.md:384`/`:355`, `reflect/config.py:103`, `sc-crash-recovery/SKILL.md:137` and `seed-brief.md:62`; K-1/K-2/K-4 cite `seed-brief.md:53`, `:54`, `:62` (`:888-891`). I checked in source: `sc-issue-command.md:384` is "No CLI (...) code", and the brainstorm `seed-brief.md:53/54/62` lines match. |
| P6-28 | RESOLVED | 4.6 `:577` states the 41 `def test_` count (verified earlier in source) and marks only the cross-references stale. 8.1 `:1347` says "Settled in 4.6". "settled by GQ-84" is gone. |
| P6-29 | RESOLVED | 8.3 `:1410` relabels the agents-fleet and SAM row "Context only, unfetched (D6) ... not support for any WC-14 clause", and traces G1/G2 to GQ-04. |
| P6-30 | RESOLVED | `:157`, `:470`, C4 `:569`, S-09 `:597`, R-2 `:1024`, `:1151`, `:1546`, row 84 `:1602` and row 90 `:1613` narrow the claim to `--all` plus one allowlist entry, with single-project mode using the cwd. `:470` cites the host layout as a host observation. Grep `SKILL.md:25-27` returns 0. |
| P6-31 | RESOLVED | Rationale `:1060-1066` no longer uses a contracts import; A1 Reuse `:952-953`, `:980` and `:1007-1008` say `superclaude.contracts` has no sweep vocabulary. Step 1.4 `:1205` says none of them is needed. |
| P6-32 | RESOLVED | The Comparison Risk row `:1044` and Rationale `:1064` rate A1 Medium and list GQ-37, G-A, GQ-34, GQ-22, read-verb side effects and GQ-25. "only open runtime item" returns 0. |
| P6-33 | RESOLVED | A1 Risk `:952` reads "provable at the argv and local-filesystem level"; K-5 `:1063` adds the step 1.0a probe; step 1.0a `:1195` (`artifacts/readonly-probe.md`) and row 79 `:1586` agree. The NB-4 record is intact (`:13`). |
| P6-34 | RESOLVED | `--include-remote` is off by default at 3.1 `:348`, SC-2 `:438` (flags per verb), the A1 diagram `:922`, step 1.4 `:1205` (a one-time cost measure to `artifacts/include-remote-cost.txt`), the step 1.10 test `:1216` and S9 row 17 `:1512`. |
| P6-35 | RESOLVED | Step 1.4 `:1205`, 3.1 `:431`, S7 X-2 `:1081`, 8.4 X-2 `:1425` and 8.1 `:1339` specify the `--root` scan of `.dev/tasks/{to-do,done}/*/` with `unscanned: orca unavailable`; the Orca-down test is at `:1216`. |
| P6-36 | RESOLVED | Step 1.0b `:1196` gates GQ-09/10/11/35/61/63 and the APPROVED.md read (GQ-100), records the answers in `artifacts/owner-decisions.md`, and names the steps each one blocks; S7 `:1056` and 8.1 `:1318` agree. |
| P6-37 | RESOLVED | K-1 `:888` says "The coordinator-only half is a contract rule, not a mechanical guard". |
| P6-38 | RESOLVED | SC-7 `:443`, `:1463` and step 1.12 `:1218` test what the sweep sees ("stays listed while its source still shows it, whatever its age") and give "until answered" to WC-14 G5. MINOR note N-6: 3.1 `:396` still says "so 'kept until answered' holds". |
| P6-39 | RESOLVED | Dependencies `:1186` reads "WC-2 to WC-13; WC-1 unused; no WC-14 today". GQ-11 is restated as "add WC-14, or reuse the unused WC-1 ID" at `:46`, `:429`, `:543`, `:630`, `:1234`, `:1391`, `:1504` and `:1631`. No "override WC-1" remains. |
| P6-40 | RESOLVED | 8.4 X-1 `:1424` reads "described as read-only, but its allowed-tools permit `git stash *` (`SKILL.md:4`)"; S7 X-1 `:1080` agrees. |
| P6-41 | RESOLVED | 8.4 X-4 `:1427` reads "Apply the split rule (guide reading for stop decisions, `06-orca-open-questions.md` Gap 19 `:144`)"; S7 X-4 `:1083` applies the same split rule. |
| P6-47 | RESOLVED | Steps 1.24a (`:1247`, the developer guide `:991` plus re-reads of `:336/:394/:799/:993/:2203`) and 1.24b (CHANGELOG) are present, with Integration Checklist items `:1479-1480` and Rollback `:1273`. |
| P6-49 | RESOLVED | Rollback `:1262-1278` lists the files and registrations per step group, says what happens to reports already written (`:1276`) and covers WC-14 against the owner decision (step 1.0b; `:1278`). |

## Required preserved items

| Item | Present | Evidence |
|---|---|---|
| NB-4 exception record | Yes | `:13`, `:1644` |
| [CONTRADICTION] marker 1 | Yes | `:1094-1096`, resolution `:1098` |
| [CONTRADICTION] marker 2 | Yes | `:1562-1564`, resolution `:1566` |

## Open blocking findings

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| P6-18 | IMPORTANT (contradiction) | Step 1.3 `:1204` vs 3.1 `:393` and S5 `:679` | Terminal releasable still depends on a fact no probe observes. 3.1 and S5 say yes only after the session's result has been read. Step 1.3 computes yes from `terminalState` reclaimable + `nextAction` release alone. That drops the condition without a proxy, and step 1.3 itself calls the coordinator's reading not observable (worktree half). The fix log row for P6-18 covers rule 6 and worktree removable only. | In step 1.3, either print "terminal releasable: could not determine (result read not observable)" for a releasable terminal, or define the proxy, for example "and the sweep's own read of `return-contract.yaml` succeeded (rule 6 sense)", and use that wording in 3.1 `:393` and `:679`. |

## New findings introduced by the fixes

No new blocking finding. MINOR notes (they do not count toward `|F_1|`):

| # | Location | Note |
|---|---|---|
| N-1 | S7 `:1098` | The resolution under the first marker is labelled "Phase 6 QA, P6-06", but P6-06 is the S7-duplication finding; the line-range resolution belongs to a different ID. |
| N-2 | 3.1 diagram `:366`, SC-5/SC-6 | On live rows rule 2 never yields stalled (proved), because fencing cannot be excluded (step 1.3 `:1204`; SC-4 `:440`; row 81a `:1589`). 3.1 and SC-6 do not say so. |
| N-3 | Step 1.6 `:1207` | The JSON row key list leaves out a session `id`. |
| N-4 | SC-1 `:437` | Still describes the old patch method; step 1.11 now uses the snapshot diff. |
| N-5 | Step 1.4 acceptance `:1205` | The live check runs `superclaude sweep run`, which exists only after steps 1.6-1.7. Run it after 1.7. |
| N-6 | 3.1 `:396` | "so 'kept until answered' holds": SC-7 now says the sweep cannot see answers (G-B). |
| N-7 | `:162`, `:1577` | Rule 2 is narrowed from Section C (`research-notes.md:193` allows a transcript "proved final"). This is correct under WC-10, but only these two places say it. |
| N-8 | A1 diagram `:918` | Shows "sys.exit(1) on error"; step 1.6 defines exit codes 0/1/2. |
| N-9 | S7 X-4 `:1083` | Still says "Open" in the evidence column, while its effect column and 8.4 `:1427` apply the split rule. |

## PASS set (48)

P6-01, P6-02, P6-03, P6-04, P6-05, P6-06, P6-07, P6-08, P6-09, P6-10, P6-11, P6-12, P6-13, P6-14, P6-15, P6-16, P6-17, P6-19, P6-20, P6-21, P6-22, P6-23, P6-24, P6-25, P6-26, P6-27, P6-28, P6-29, P6-30, P6-31, P6-32, P6-33, P6-34, P6-35, P6-36, P6-37, P6-38, P6-39, P6-40, P6-41, P6-42, P6-43, P6-44, P6-45, P6-46, P6-47, P6-48, P6-49.

## Counts

- `|F_0|` = 49; `|F_1|` = **1** (P6-18). This is strictly fewer, so the monotonicity guard does not fire. There is no regression: this is cycle 1 and no earlier PASS set exists.
- Adversarial stance: I expected 5 or more bad fixes and found 1 open blocking finding plus 9 MINOR residues. Every RESOLVED row cites the current line it was checked at, and the source facts the fixes rely on were re-read (WORKER-CONTRACT `:23`, `test_worker_contract.py:245-254`/`:545`, `research-notes.md:190-200`, `sc-issue-command.md:384`, `seed-brief.md:53-68`, the earlier crash-recovery, swarm-wizard and reflect checks).

## Confidence

- **Confidence:** Verified: 49/49 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement (both context windows of this cycle, approximate):** Read: 40 | Grep: 45 | Glob: 0 | Bash: 6. No web research.
- Limit: the very long step rows (`:1204`, `:1205`, `:1234`, `:1236`) were checked by targeted Grep excerpts as well as offset reads. A defect in an unexcerpted part of those lines could be missed.

## Verdict: FAIL

One blocking finding is open: P6-18, the terminal releasable condition. `|F_1| = 1`. Fix cycle 2 must resolve P6-18 only; the MINOR notes need no fix pass.
