# QA Report: Task-Research Alignment

**QA mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-11-08
**Task file:** `TASK-RF-sweep-phase1-20261108-072653.md` (2856 lines)
**Research:** `research/01` to `research/09` (research/07 and research/08 win on line anchors)
**Stance:** adversarial; the builder is assumed to have dropped or misrepresented findings.

Status: complete. 4 IMPORTANT and 8 MINOR findings. No CRITICAL finding.

## Check 1: research key findings and the items that act on them

| # | Research key finding | Source | Task item(s) | Status |
|---|---|---|---|---|
| 1 | Five pin edits in `test_worker_contract.py`, including `RULE_PHRASES["never-as-worker"]` at :89 | 03 IP-2, 07 (d) | 12.3 (all five, quoted), 5.5 (design names five) | COVERED |
| 2 | WC-16, not WC-14; a second `"WC-14"` key silently overrides | 07 (a), (d) | 5.1 to 5.3, 12.1, 12.3 (`grep -c '"WC-14": ('` is 1) | PARTIAL, see I-1 |
| 3 | `main.py` insert after line 565 | 08 (c) | 5.6, 9.2 | COVERED |
| 4 | `tests/sweep/__init__.py` required | 05 section 3 | 8.7 | COVERED |
| 5 | Guard reads only the test's own markers (`request.function.pytestmark`) | 05 section 2 | 8.8 (grep forbids `get_closest_marker`) | COVERED |
| 6 | Real-git test copies the repo `.gitignore`; the `.gitignore` edit lands first | 05 section 8, 03 IP-6 | 8.6 before 8.9 | COVERED |
| 7 | CHANGELOG `### <title>` plus `#### Added (<topic>)` | 03 R8, 08 (a) | 5.9, 13.6 | COVERED |
| 8 | `UNATTENDED_EXPECT` stays 31; no `## Unattended mode` in `sweep.md` | 07 (e) | 5.8, 11.1, 12.3 | COVERED |
| 9 | Write-verb classification table for `sweep.md` and the skill | 03 IP-3, 07 (e) | 12.3 | COVERED, see M-7 |
| 10 | `ClassifiedRow` undefined; define it as a builder decision | 01 B2, 09 Gap 2 | 8.3, OQ-14 | COVERED |
| 11 | Ten #409 dimensions in the report only, not JSON; `policy` against `policy_of` | 09 Gap 2 | 8.3, 8.12, 10.5, OQ-11 | COVERED |
| 12 | R3-B1 fixtures 6 + 4 in section 11; FR-010 trace | 04 section 2.3, 09 Gap 4 | 2.5 | COVERED |
| 13 | R3-B2 7 fixtures; D9, SP-29 and FR-010 edits | 04 section 3, 09 Gap 4 | 3.2, 3.3 | COVERED |
| 14 | R3-B3 4 fixtures, three `origin unknown:` notes, source row `orca worker-list <run>` | 04 section 4 | 4.1 to 4.4 | COVERED, see M-2 |
| 15 | R3-B1 model fields `dispatch_started`, `dispatch_ended`, `dispatch_status`, `first_record_ts`, read from `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status` | 04 section 2.2 | 2.1 to 2.4 (design); 8.3, 8.4 (code) | PARTIAL, see I-3 |
| 16 | R3-B1 gate: the fields appear in 7.1, 7.2, 2.2, 11, 15.1, 17, 18 | 04:221, 09:171 | 2.7 | MISREPRESENTED, see I-2 |
| 17 | Step 1.16a record-only, with four recorded points | 09 Gap 3, 07 "Other design references" | 5.7, 7.19 | INCONSISTENT, see I-4 |
| 18 | Scoped 1.28 grep, full-tree count 168 | 09 Gap 3 | 14.5 | COVERED |
| 19 | 1.29 pipx option A (`pipx run --spec`) and option B (`pipx install --force`, D4 approval) | 09 Gap 3 | 14.6 to 14.8, OQ-10 | COVERED |
| 20 | Diff-file POST form (`git diff --binary {BASE}` plus `--no-index /dev/null`) | 09 Gap 6 | 14.43, 14.44, OQ-12 | COVERED |
| 21 | Master section 4 "The sweep." and its 5-minute bound; pins at test :209-219 | 07 (c) | 5.4, 12.1 | COVERED for WC-16; see M-8 for R2 |
| 22 | R5 `--agent-wait` HALT with the two options | BUILD-REQUEST, 07 (c) | 6.1 to 6.3 | COVERED |
| 23 | Human-gate pattern (OQ, PENDING record, HALT, J1 clause overridden) | 06 section 9 | 6.x, 7.x, 14.6, 14.7 | COVERED |
| 24 | Step 1.0a: eight templates, `<pkg>`, Run choice, fake id, "sanitized" defined | 09 Gap 3 | 7.14 to 7.18 | COVERED |
| 25 | Step 1.4 live pass rule REPORT:1247 minus the include-remote timing; `uv run` form | 09 Gap 3 | 9.3 | COVERED |
| 26 | Routing row R5 lands no later than `sweep.md` | 03 ordering 2 | 11.2 right after 11.1 | COVERED |
| 27 | R2 before R1 (anchor shift) | 01 C3 | 13.1 then 13.2 | COVERED |
| 28 | `probes.py` calls `subprocess.run` through the module | 05 section 4 | 8.5 | COVERED |
| 29 | Gate sizing at full intensity; one `qa/<gate>/` folder per gate | 09 Gap 5, 06 section 6 | Key Constraints, 1.2 | COVERED |

## Check 2: fabrication spot-check (31 citations read in the repo)

All were read with `sed -n` or `grep` at the current HEAD of this worktree. No fabricated file, function, flag or line was found.

| Task citation | Result |
|---|---|
| `main.py:563`, `:565` issue-watch pair, `:568` `if __name__`, 569 lines | CONFIRMED |
| `WORKER-CONTRACT.md:23` never-as-worker line | CONFIRMED |
| `WORKER-CONTRACT.md:63` WC-14, `:64` WC-15 | CONFIRMED |
| `WORKER-CONTRACT.md:110` "The sweep." (5-minute bound, `--agent-wait`) | CONFIRMED |
| `WORKER-CONTRACT.md:124` "the WC-14 exception", `:151` L1 probe row | CONFIRMED |
| `WORKER-CONTRACT.md:271`, `:273`, `:275`, and the quoted last sentence of :273 | CONFIRMED |
| `test_worker_contract.py:25`, `:86-92`, phrase at `:89` | CONFIRMED |
| `:155` WC-13, `:156` WC-14, `:165` WC-15, `:173` heartbeats | CONFIRMED |
| `:209-212` `liveness-sweep-and-states` phrase | CONFIRMED |
| `:382-391` `NEVER_AS_WORKER` (8 entries) | CONFIRMED |
| `:438` `UNATTENDED_EXPECT`, `:1556` `_check_p2_set`, `:1569` its test | CONFIRMED |
| `:765-767`, `:837`, `:912`, `:1081`, `:1318`, `:1322` | CONFIRMED |
| `:1940-1955` (`AUDIT_ROOTS`, `WRITE_VERB_RE`, `_CATEGORY_RE`), `:1966`, `:2016`, `:3129`, `:3133`, `:3150`; 3195 lines | CONFIRMED |
| `HOW-WE-WORK.md:318`, `:320-321`, `:333`, `:337`, `:396`, `:403`, `:404` | CONFIRMED |
| `docs/user-guide/commands.md:105`, `:107-108`, `:115`, `:116` | CONFIRMED |
| `CHANGELOG.md:5`, `:7`, `:9`, `:19` | CONFIRMED |
| `.gitignore:254` `.dev/sprint-state/` | CONFIRMED (see M-4 for :250) |
| `tests/recommend/test_routing_refresh.py:33`, `:648` | CONFIRMED |
| `tests/core/test_how_we_work_routing_table.py:27`, `:33` | CONFIRMED |
| Developer guide `:991` | CONFIRMED |
| `src/superclaude/pytest_plugin.py:216-222` auto-marker | CONFIRMED |
| `tests/pr_submit/test_conflict_scripts.py:46`, `:63` | CONFIRMED |
| `src/superclaude/cli/recommend/__init__.py:12-20` | CONFIRMED |
| `pyproject.toml:119` `integration` marker | CONFIRMED |
| `sprint/recovery.py:424-434` (link at :433); `swarm/atomic.py:28-31` (fsync) | CONFIRMED |
| `commands/graph.md:9`, `:41-46`; `commands/issue.md:12`, `:23`, `:27`, `:34` | CONFIRMED |
| `output-styles/pragmatic.md:22`, `:53` | CONFIRMED |
| `~/.claude/skills/sc-reflect-protocol/SKILL.md:80`, `:204` | CONFIRMED |
| `APPROVED.md:11` (D4), `:71` (G1) | CONFIRMED |
| SPEC `merged-requirements.md:143` NFR-014 "never carries `--agent-wait`" | CONFIRMED |
| DESIGN: 1013 lines; em-dash count 0; `Total: 9 deviations.` :817; `Total: 23 open items.` :993; the :494 passages; :468; :566 `sources`; :670 old cadence sentence; :739 phrases; :764; :815; :853; :885; :1005; the six `[sweep publish]` messages :106-128; `unscanned: outside root` :507; `not frozen` :740; `origin not proved` :496; `1.4.245-aidev02.780594c521aa` :30 | CONFIRMED (see M-3 for the :497 quote style) |

## Findings

### I-1 (IMPORTANT): the WC-14 to WC-16 rename misses six DESIGN mentions, and the R4 pass rule cannot be met

- **Evidence:** `grep -n 'WC-14' docs/designs/orchestrator-mode.md` at HEAD returns coordinator-loop mentions outside the sections that items 5.1 to 5.3 rename (8, 9, 10, 12, 15, 16): line 5 (status line, "Owner approval of the WC-14 text (section 8)"), line 13 (section 1 summary, "the WC-14 "Coordinator loop" contract text"), line 812 (section 13, D6 "WC-14 text of SPEC section 10"), line 835 (section 14, "The REPORT's WC-14 draft"), lines 988 and 989 (section 17 open items 20 and 21, "GQ-11 (WC-14 approval)", "PR #422 overlap with WC-14").
- **What is wrong:** BUILD-REQUEST R4 says "Renumber the design's rule to WC-16 everywhere". research/07:100 listed only design 663-680, 695, 701, 777 and 926, and the builder copied that list without its own grep. Item 5.3 Verification requires every remaining hit to be `worker rule (keep)` or the section 8 sentence, else "log it and stop". None of the six lines is a worker-rule hit, and two of them (812, 835) name the SPEC's and REPORT's historical drafts, which fit neither class. Item 5.12's fix loop sends the executor back to "the owning item (5.1 to 5.11)", and no item owns sections 1, 13, 14 or 17. The phase halts, or the executor improvises.
- **Smallest fix:** extend item 5.3 (or add a 5.3a) to cover sections 1, 13, 14 and 17, and add a third class to the 5.1 hit list, `historical name (keep, cite as WC-14 draft)`, for 812 and 835, with 5.3 and 5.12 accepting it.

### I-2 (IMPORTANT): the R3-B1 mechanical check 2.7 fails by construction

- **Evidence:** item 2.7 needs "the four field names appear in sections 7.1, 7.2, 2.2, 11, 15.1, 17 and 18" plus a section-by-field matrix. The edits the task applies are research/04 edit 5 (7.1 comment: only `first_record_ts`), edit 7 (15.1 item 4: `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status`) and edit 8 (open item 23: the same dotted Orca names). `dispatch_started`, `dispatch_ended` and `dispatch_status` are never written into 7.1, 15.1 or 17. A `grep` for `dispatch_status` does not match `dispatch.status`.
- **What is wrong:** research/04:221 is ambiguous (it lists sections to grep, not a per-cell rule). The task turned it into a strict per-section rule that the research's own edits cannot satisfy. The fix loop ("return to the item that owns the edit (2.1 to 2.6)") has no edit that adds those names, so the executor either loops or adds text research/04 does not specify. That changes the design beyond the review finding.
- **Smallest fix:** state the 2.7 pass rule per section: 7.2 and 18 hold all four model names; 2.2 holds all four; 7.1 holds `first_record_ts`; 11 holds `first_record_ts` and the `dispatch_*` names in the fixtures; 15.1 and 17 hold the three dotted Orca names.

### I-3 (IMPORTANT): the code items misname the R3-B1 model fields and drop `dispatch_status`

- **Evidence:** item 8.3 Context lists `OrcaObservation` "with `dispatch`, `run`, `session_join`, and the Dispatch start `dispatch.dispatchedAt` and end `dispatch.completedAt` fields added by R3-B1". research/04 edit 1 names the model fields `dispatch_started`, `dispatch_ended` and `dispatch_status`; the dotted names are the Orca JSON source paths. `grep -n dispatch_status` on the task file hits only lines 244 to 391 (Phases 2 and 3); no Phase 8 to 14 item names it. Item 8.4 lists the R3-B1 window rule ("UTC parse, inclusive whole-second window") but not its status condition (`pending` or `dispatched` when `dispatch_ended` is None), which needs `dispatch_status`.
- **What is wrong:** this misrepresents a research finding inside a code item. Item 8.3 Verification greps only class and constant names, so a missing or misnamed field passes it, and the defect shows up only in Phase 10, after the impl-core gate.
- **Smallest fix:** in 8.3, name `dispatch_started: datetime | None`, `dispatch_ended: datetime | None`, `dispatch_status: str | None` (parsed from `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status`) and `TranscriptTail.first_record_ts`, and add a `grep -c` for each of the four to the Verification. In 8.4, name the `dispatch_status` condition.

### I-4 (IMPORTANT): items 5.7 and 7.19 define different contents for the step 1.16a record

- **Evidence:** item 5.7 rewrites DESIGN so step 1.16a records "PR #422 is merged at `2327fbd3`; the 15 P2 conversions are on master; `UNATTENDED_EXPECT` has 31 entries; the #409 overlap state". Item 7.19 writes `artifacts/pr422-409-check.md` with research/09's four points: the `gh` state line, `merge-base --is-ancestor 2327fbd3 HEAD`, `merge-base --is-ancestor 495eb96d origin/master`, and the re-read note. 7.19 records neither the 15 P2 conversions nor the 31 count.
- **What is wrong:** the artifact does not match the design text the same task writes. The fidelity gate (items 14.29 to 14.31, DESIGN against artifacts) is likely to flag it and loop.
- **Smallest fix:** make 5.7 use research/09's four points verbatim, or add the P2 count (`test_worker_contract.py:416-432`) and the `UNATTENDED_EXPECT` count of 31 (`:438`) to item 7.19.

### M-1 (MINOR): research/04 edit 9's m2 correction is dropped

Item 2.6 adds `### Fix cycle 3` but omits research/04:95's second instruction: fix the cycle 2 row's "the transcript's earliest timestamp" to "the earliest `timestamp` in the transcript tail" (m2).

### M-2 (MINOR): the R3-B3 fixture count is 4, not 3

The Phase 10 intro (line 1767) says "R3-B3 (3)". research/04 section 4.3 and research/09 Gap 4 give 4, including `test_fr010_incomplete_notes_order`. Item 10.2 lists only the three cases. "every case in that row" still covers the fourth.

### M-3 (MINOR): the item 4.1 anchor quote does not match DESIGN byte-for-byte

Item 4.1 anchors on "The guard's 'join completed' condition fails" (single quotes, copied from research/04). DESIGN :497 reads `The guard's "join completed" condition fails`. A `grep -F` with the task text misses the anchor.

### M-4 (MINOR): the `.gitignore` block range in item 8.6 is wrong

Item 8.6 calls `:250-254` "the sprint-state block". `.gitignore:250` is `.dev/pr-monitor/` (read at HEAD). The insertion point after `:254` is right. research/03 IP-6 also notes that :255-257 continue the sprint-state block (the e2e-reflect entry).

### M-5 (MINOR): research/05 test edge cases are missing from the Verify clauses

None of these appears in the task (grep counts 0): CI runs the sweep tests under xdist (`-n auto`), so the tests must be order-independent with no module-level mutable state; Click 8.5.1 keeps `result.stderr` separate, so the `[sweep publish]` lines are read from `result.stderr`; the AST import test needs a synthetic mutation case (research/05 section 7; research/02 section 4 "mutation guarantee").

### M-6 (MINOR): the `__getattr__` signature differs from DESIGN

Item 8.2 asks for `def __getattr__(name: str)` "line for line" like recommend. research/02 section 2 says the DESIGN signature is `-> object` and that the annotated form is what the design specifies.

### M-7 (MINOR): write-verb classification order and regex

research/03 ordering constraint 3 says to classify in the same step that writes `sweep.md` and the skill. The task does it in 12.3. That is defensible, because the `never-worker` category applies only once 12.2 lands, but the deviation is not stated. The 12.3 grep `git (add|...)` also misses the `git -C <path> <verb>` form that `WRITE_VERB_RE` (`test_worker_contract.py:1948-1951`) matches. The pytest run in 12.3 catches it, so the risk is low.

### M-8 (MINOR): routing row R2 keeps "sweeps on every wake" without the 5-minute bound

Item 5.2 only renumbers R2, and item 13.1 says "or the revised DESIGN wording, if design fix R4 aligned it", but no R4 item aligns it. The guide bullet will state the cadence without the bound that WC-16 and contract :110 carry.

## Check 3: research edge cases and caveats in Verify clauses

Reflected: the guard's own-marker rule (8.8), `from subprocess import run` (8.5), the integration test PASSED and not skipped (8.9), the `.gitignore` copy (8.9), `raising=False` removed (8.11), UNVERIFIED facts held until 1.0a (OQ-13, 7.17 HALT on a differing field), before and after reads equal (7.16), forbidden tokens grep (7.16), `output_input_overlap` sibling path (1.2, 14.43), the 168 count at a different base (14.5), D4 for pipx (14.8), HALT on GQ-10, GQ-11, GQ-35, GQ-63 and D9 answers that need a design revision. Missing or misstated: I-2, I-3, M-5.

## Check 4: dependency ordering

The phase order matches the research and the BUILD-REQUEST: the design fixes (Phases 2 to 6) come before every code item; the R5 HALT blocks Phase 7 onward; 1.0b, 1.0a and 1.16a come before Phase 8; D9 gates 8.4; `.gitignore` (8.6) comes before the real-git test (8.9); conftest (8.8) comes before the 1.4a test (8.9); R5 (11.2) comes right after `sweep.md` (11.1); the contract, the five pins and R7 come together in Phase 12, after GQ-11 and 1.16a; R2 comes before R1, and R1, R4 and R3 come together; sync-dev runs in 14.1; the diff file and POST come last. One caveat: R4 renumbers to WC-16 (Phase 5) before the owner answers GQ-11 (7.3, 7.4). This follows the BUILD-REQUEST order, and the WC-1 branch HALTs with a re-plan, so it is acceptable. Ordering note: M-7.

## Summary

- Blocking: I-1, I-2, I-3, I-4 (4 IMPORTANT).
- Non-blocking: M-1 to M-8.
- Fabrication: none found in 31 spot-checked citations.

VERDICT: FAIL


