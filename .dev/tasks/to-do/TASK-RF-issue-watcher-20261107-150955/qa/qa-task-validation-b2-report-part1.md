# QA Report - Task Integrity, Lens b2-self-containment (Partition: P1 to P5, part 1)

**Topic:** issue-watcher task file TASK-RF-issue-watcher-20261107-150955
**Date:** 2026-11-07
**Phase:** task-integrity (lens b2-self-containment)
**Fix cycle:** N/A (fix_authorization: false)

[PARTITION NOTE: Cross-file checks limited to assigned phases P1 to P5. P6 to P10 are covered by another agent.]

## Scope and method

- File: TASK-RF-issue-watcher-20261107-150955.md, lines 154-407 (Phase 1 Steps 1.1-1.8, Phase 2 Steps 2.1-2.11, Phase 3 Steps 3.1-3.11 and Gate A Steps 3.G1-3.G12, Phase 4 Steps 4.1-4.7, Phase 5 Steps 5.1-5.11 and Gate B Steps 5.G1-5.G12) = 72 checklist items (counted with awk over lines 154-407); plus Overview, Execution Context, Open Questions (lines 778-866) as context.
- Sources checked against: docs/designs/issue-watcher.md (D), spec-final.md (S), research/06 (R-003), research/02, 03, 05, and the repository files cited as anchors.
- Item sizes (chars, single paragraph): Step 3.1 = 6711, Step 4.1 = 6467, Step 5.1 = 4985, Step 2.2 = 4673, Step 2.3 = 4345; median item about 2,000.

## Citation spot-check (28 citations checked, more than the 15 required)

| # | Item | Citation | Result |
|---|------|----------|--------|
| 1 | 1.5 | main.py:559, 561, 564 | CONFIRMED (read lines 555-565) |
| 2 | 1.5/4.1 | swarm/atomic.py:14, :33, 14-39 (no dir fsync, no chmod, `except Exception`) | CONFIRMED |
| 3 | 1.5/5.1 | install_user_setup.py:35 `_ORCA_CLIS`, :198-221 `_find_orca` | CONFIRMED |
| 4 | 1.5/5.1/5.7 | origin_repo.py:65-69, :86-99 | CONFIRMED |
| 5 | 1.5/5.8 | claim.md:29, claim-comment.md:23 marker | CONFIRMED (marker is also the template's last non-empty line) |
| 6 | 1.5/1.4 | test.yml:22, :29, :47 | CONFIRMED |
| 7 | 1.5 | pyproject.toml:16, 114, 135, 174-184 | CONFIRMED |
| 8 | 3.1 | poll-augment-review.sh:48-77, :57 (page longer than 100 rejected) | CONFIRMED (`length <= 100`) |
| 9 | 2.4 | tests/conftest.py:28-79, 82-117 autouse fixtures | CONFIRMED |
| 10 | 2.5/5.6 | test_install_user_setup.py:261, 281-282 | CONFIRMED |
| 11 | 5.4/5.7 | test_issue_repo_resolution.py:15-19, 30-57 | CONFIRMED |
| 12 | 1.6 | D 751 "Package marker; exports nothing" | CONFIRMED |
| 13 | 1.6 | D line 11 | DRIFT: line 11 is the heading "## 1. Purpose and scope" (see MIN-1) |
| 14 | 1.7 | D 95 (row C14), D 761 | CONFIRMED |
| 15 | 2.1 | D 218, 252-265, 638-649; S 309 | CONFIRMED |
| 16 | 2.3 | D 223, 392-401, 697-722; S 330-358 (52 names), 379 | CONFIRMED; I recounted the 57 names of Step 2.3 (52 spec + 5 proposals) and each kind and exit against S 332-358 and DF-41/DF-57: all match |
| 17 | 2.6 | D 658-660 (T2-T4); S 84-94, 128-131 | CONFIRMED |
| 18 | 3.1 | D 219, 537-602, 545, 546, 549, 579-588, 594-600 | CONFIRMED |
| 19 | 3.2-3.5 | D 834-838 | CONFIRMED |
| 20 | 4.1 | D 221, 268-274; "17 fields of D 417-437" | CONFIRMED (counted 17) |
| 21 | 4.1 | D 476-492 T-1..T-13, 511-521 lock | CONFIRMED |
| 22 | 4.2 | D 525-533, 779; R-003 Table 1.3 | CONFIRMED (C1/C3/C4/C5 recipes match) |
| 23 | 5.1 | D 604-636, 674-693, 741 (retry argv); 12-element argv | CONFIRMED (12 elements counted) |
| 24 | 5.6 | D 83 (C2), D 100 (C19) | CONFIRMED |
| 25 | 5.6 | "the original raises" for a top-level JSON list | FALSE (see IMP-4) |
| 26 | 5.7 | D 84 (C3), AC-16 (D 889) | CONFIRMED |
| 27 | 5.8 | D 791 | CONFIRMED |
| 28 | 3.G*/5.G* | R-003 Table 1.6 lens map, 3+3 agent types, G-1/G-4/G-5/G-8 per phase | CONFIRMED |

No item rests on a [CODE-CONTRADICTED] claim as fact: C14 (Step 1.7), C21 (Step 3.6/DF-28) and the lazy-import claim are all corrected in the items and listed in OQ section F. gh and Orca reply shapes are confined to `_assumed_shape` fixtures plus "unverified" comments (Steps 3.1-3.5, 5.1, 5.2).

TB-Add-8 (Context evidence binding): every non-gate item in P1-P5 carries a file:line anchor or an `<!-- evidence-absence: ... -->` comment: PASS. TB-Add-1: grep for TBD/TODO/FIXME over the whole file returned no match: PASS. Grep for "see above", "as above", "same as step" returned no match: PASS (but see IMP-3 and MIN-4 for referenced-content cases that the grep cannot see).

## Issues Found

### Summary table

| # | Severity | Item(s) | Issue (short) |
|---|----------|---------|---------------|
| IMP-1 | IMPORTANT | 5.1, 5.2, 5.5 | How an operation id is extracted from an `unknown` (error) reply is not defined, yet Step 5.5 asserts the unknown fixture "keeps its valid id" |
| IMP-2 | IMPORTANT | 4.1 (consumer: P6 cycle item) | `PendingContext` is named but its fields are never defined anywhere (design, spec, research or task) |
| IMP-3 | IMPORTANT | 3.G12, 5.G12 (pattern repeats in later gates) | Fix cycle 2 is "perform the actions of Steps G8-G11 again": no explicit items, no embedded prompts, no path substitutions |
| IMP-4 | IMPORTANT | 5.6 (also 5.1) | False statement that the original `_find_orca` raises for a top-level JSON list; it catches it |
| IMP-5 | IMPORTANT | 2.2, 2.3, 3.1, 4.1, 5.1 | Items far over the atomicity bound (4,300 to 6,700 chars each, 15-30 distinct behaviours) with no TB-Add-5 split and no single-item justification comment |
| IMP-6 | IMPORTANT | 3.6 | Assertion "no argv contains `title`, `body`" is unsatisfiable: the G4 argv carries `MARKER_JQ`, which contains `.body` |
| MIN-1 | MINOR | 1.6 | Cites design "line 11"; line 11 is a heading, the quoted text is at 751 |
| MIN-2 | MINOR | 1.2 | Verification uses Glob to list directories; Glob lists files, so empty directories cannot be confirmed |
| MIN-3 | MINOR | 3.G2 | Gate A command-reproduction prompt omits `make lint` but tells the agent to compare `p3-g4` |
| MIN-4 | MINOR | 2.8 | The 57-name / kind / exit table is pinned "from Step 2.3" by reference, not restated |
| MIN-5 | MINOR | 2.2, 5.1, 4.1 | Items implement OQ-37, OQ-38, OQ-40, OQ-41/41a readings without citing the OQ index (TB-Add-3) |
| MIN-6 | MINOR | 3.4, 3.1 | `"pageInfo": {...}` placeholder in the project-items fixture; `marker_comments(...)`, `edits(...)`, `project_items(...)`, `reread(...)` signatures elided |
| MIN-7 | MINOR | 2.10, 3.8, 4.6, 5.9 | "re-run until PASSED" has no iteration bound or stop rule (Step 1.8 has "once") |
| MIN-8 | MINOR | 1.1 | No verification clause and no blocker clause (the only item of the five B2 components short in two places) |
| MIN-9 | MINOR | 3.9, 5.10 | "ensuring exit 0" conflicts with "a finding in an untouched file is recorded and NOT fixed" (exit would be nonzero); no verdict rule given |
| MIN-10 | MINOR | 2.3 | `stderr_fallback(..., ts=None, host=None)`: what a `None` becomes is undefined, while the module is barred from reading the clock |
| MIN-11 | MINOR | 2.5 | "finishes well under 5 seconds" is not a measurable bound |
| MIN-12 | MINOR | 4.1 | Imports `parse_utc`, `format_utc`, `valid_issue_number` from `predicates`; D 239 says "types only"; OQ-46 mentions it but does not record it as a departure |
| MIN-13 | MINOR | all creation items | Verification fields are "ensuring ..." prose, not `Verify:` commands with expected output; they rely on the phase-level G-1/G-5 items |

### IMPORTANT issues with exact fixes

**IMP-1 (Steps 5.1, 5.2, 5.5): operation-id source for `unknown` replies is undefined.**
Evidence: Step 5.1 defines id extraction only for "exit 0 with a JSON object whose operation id (first hit in `OPERATION_ID_PATHS`)" and then says an `unknown` outcome keeps "an operation id only when it was parsed and passes the pattern". Step 5.2 builds `orca_launch_unknown.json` with `exit` 1 and "a `stderr` text containing `agent_session_operation_unknown` together with an operation id" (plain text, not JSON). Step 5.5 then asserts "the unknown fixture keeps its valid id". Nothing says where in a non-zero-exit, non-JSON error text a parser may find the id (D 636 only says the id comes "from the error"). The executor must invent a text-scraping rule. This matters because `status` prints the retry command only for `unknown` entries that have an id (S 160, FR-015, D 739), so a wrong rule silently removes the operator's only recovery path.
Fix text:
- Step 5.1: replace "keeping an operation id only when it was parsed and passes the pattern" with: "keeping an operation id only when it was parsed and passes the pattern; for every `unknown` kind the id is looked up, in this order, in the JSON object parsed from stdout and then in the JSON object parsed from stderr (the error reply), each through `OPERATION_ID_PATHS`; plain text that is not a JSON object never yields an id (`operation_id` None); `OPERATION_ID_PATHS` therefore holds both the success path and the error path (unverified proposals, pinned by the two fixtures of Step 5.2)".
- Step 5.2: replace "a `stderr` text containing `agent_session_operation_unknown` together with an operation id" with: "a `stderr` holding the text of a JSON object that contains `agent_session_operation_unknown` and the id `op-test-0001` at the error path of `OPERATION_ID_PATHS`".
- Step 5.5: add the negative case "a plain-text stderr containing `agent_session_operation_unknown` and an id-like token gives `unknown` with `operation_id` None".

**IMP-2 (Step 4.1): `PendingContext` has no field list.**
Evidence: grep over D, S and research 01-06 for `PendingContext` returns no match; the only mentions in the task are Step 4.1 ("and `PendingContext`") and OQ-41, which says "tests pin whatever the module items define". Step 4.1 defines no fields; it only says `mark_pending(doc, n, ctx, now)` sets "approval and `launch_*` fields". The P6 cycle item (line 418) calls `record.mark_pending` and also gives no field names. A mid-task executor on Step 4.1 must guess, and the P6 executor must then read record.py to learn the names.
Fix text (insert in Step 4.1 right after "and `PendingContext`"): "(a frozen dataclass with exactly these fields in this order: `approver_id: int`, `approval_event_id: int`, `approved_at: datetime`, `launch_cwd: str`, `launch_login: str`, `launch_account_id: int`; `mark_pending` copies them into the entry together with `launches` 1 and `consumed_at` and `pending_at` equal to `now`)". Add the same six names to the P6 cycle item where it calls `mark_pending`.

**IMP-3 (Steps 3.G12 and 5.G12): fix cycle 2 is not self-contained.**
Evidence: clause (3) reads "run the next fix cycle by performing, in this same item, the actions of Steps 3.G8, 3.G9, 3.G10 and 3.G11 again (... reports suffixed `-cycle2`)". The prompts of those steps hard-code cycle-1 paths (`qa-consolidated-findings.md`, `qa-fix-report.md`, `qa-verification-structural-report.md`, `qa-verification-content-report.md`), the item does not say which of them change, and the "then evaluate again" step does not say which files it reads. Template line 677 requires "Every step of the fix cycle (consolidation, fix agent spawn, verification spawn) MUST be an explicit `- [ ]` checklist item", and this checklist requires agent-spawning items to embed the full prompt. The same wording is expected in Gates C, D and Final (reviewer of P6-P10 to confirm).
Fix text: replace clause (3) of 3.G12 and 5.G12 with: "(3) otherwise complete the new items Step 3.G13 (consolidate into `qa/gate-a/qa-consolidated-findings-cycle2.md`), 3.G14 (single fix agent, prompt of Step 3.G9 with `qa-consolidated-findings.md` replaced by `qa-consolidated-findings-cycle2.md` and `qa-fix-report.md` by `qa-fix-report-cycle2.md`), 3.G15 and 3.G16 (the two verification agents, prompts of Steps 3.G10 and 3.G11 with the same two substitutions and the outputs `qa-verification-structural-report-cycle2.md` and `qa-verification-content-report-cycle2.md`), each written out in full with the substituted paths, and then re-evaluate this item reading ONLY the `-cycle2` verification reports plus `qa-consolidated-findings-cycle2.md`" (same for Gate B with `gate-b` and 5.G13-5.G16). If the author prefers not to add items, state the substitutions and the files read in the re-evaluation inside clause (3) itself.

**IMP-4 (Step 5.6, also Step 5.1): false claim about the original `_find_orca`.**
Evidence: install_user_setup.py:216 `topics = json.loads(probe.stdout).get("topics", [])` sits inside the `try` whose handler at :217 catches `AttributeError`; a top-level JSON list makes `.get` raise `AttributeError`, which is caught and the candidate is skipped (`continue`). Only the cases that reach :219 outside the `try` raise: `topics` null or an int (`TypeError`), a str or a dict, or a list with a non-dict element (`AttributeError`). This is exactly the DF-36 list (R-003 line 163), which does NOT include a top-level list. Step 5.6 lists "a top-level list" among the shapes for which "the original raises", requires a comment stating that, and weakens the test for that shape to "launch rejects only". Step 5.1 repeats it ("a JSON list ... the original `_find_orca` raises there").
Fix text: in Step 5.6 replace "(a non-dict element, `topics` null, an int, a str, a dict, a top-level list)" with "(a non-dict element, `topics` null, an int, a str, a dict)" and append "; for a top-level JSON list (and any other non-object top-level JSON) the original skips the candidate because `AttributeError` is caught inside its `try` (install_user_setup.py:216-217), so assert that both functions return the same result for that shape". In Step 5.1 change the parenthesis to "(DF-36; for `topics` null, an int, a str, a dict and a non-dict element the original `_find_orca` raises, design row C19; a top-level JSON list is skipped by both)".

**IMP-5 (Steps 2.2, 2.3, 3.1, 4.1, 5.1): atomicity.**
Evidence: item lengths 4,673, 4,345, 6,711, 6,467 and 4,985 characters (median item about 2,000); each creates one file but bundles 15 to 30 distinct functions, constants and rules (Step 4.1 alone lists about 35 named functions, 9 dataclasses and a 12-row transition set), then has one verification sentence. The checklist (item 10, TB-Add-5) requires an item over about 15 lines to be split or to carry a justification comment; none of the five has either (they carry only `<!-- evidence-absence -->`). The phase header "write the file in parts and save after each major section" is a working tip, not a justification, and gives the executor no per-part check.
Fix text (either): (a) split Step 3.1 into three items (3.1a constants, jq/GraphQL text and the G1-G7 argv builders; 3.1b `Reply`, `classify`, `retry_after`, `rate_limit_wait`, `CallBudget`, `Read`; 3.1c the typed reads and their paging, null and budget rules), Step 4.1 into three (4.1a exceptions, `Entry`, `StoreDoc`, `PendingContext`, `validate`, `MIGRATIONS`, `migrate`; 4.1b `Store`, `FileStore.load/save/lock/disabled/disabled_since`, `_fsync_dir`; 4.1c transitions, `sweep`, day-cap helpers, `init_state`, dry-run helpers) and Steps 2.2, 2.3 and 5.1 into two each, each part ending with its own grep or import check; or (b) add to each of the five items the comment `<!-- single-item justification: one module with one cohesive contract; an intermediate file would not import cleanly; executed in parts per the phase header and verified by Steps <next G-1 and G-5 items of the phase> and the import check of Step 2.9 or the boundary test of Step 8.8 -->`. Option (a) is preferred for 3.1 and 4.1.

**IMP-6 (Step 3.6): unsatisfiable argv assertion.**
Evidence: Step 3.6 requires "no argv contains `title`, `body`, `SuperClaude-Org` or `{owner}`". Step 3.1 builds `MARKER_JQ` from D 546, `[.[] | {id, login: .user.login, created_at, updated_at, marker: (.body | contains(<marker>))}]`, and `argv_comments` passes it as the `--jq` argv element, so the G4 argv contains the substring `body`. Read literally, the test fails on G4 (or the executor silently special-cases it). D 556 and FR-003's GWT say the rule is "no argv names `title`, `body` or a comment body field as an OUTPUT field; the only body access is `contains(<marker>)`", which is also how the Gate A security lens (Step 3.G7) states it.
Fix text: replace the clause in Step 3.6 with "no argv requests `title` or `body` as an output field: no element of any argv contains `title`; no element of any argv other than the G4 `--jq` value contains `body`; the G4 `--jq` value equals `MARKER_JQ`, whose only `body` use is `(.body | contains(` ...; no argv contains `SuperClaude-Org` or `{owner}`".

### MINOR notes (not blocking, not rechecked in later rounds)

- MIN-1 (Step 1.6): change "design lines 751 and 11" to "design line 751" (line 11 is the heading "## 1. Purpose and scope").
- MIN-2 (Step 1.2): replace "list them with Glob" with "list them with `ls -d <each directory>` in one Bash call and confirm exit 0" (Glob returns files, not empty directories).
- MIN-3 (Step 3.G2): add "`make lint`" to the commands the agent re-runs (Gate B's prompt already has it), because the same prompt compares `p3-g4`.
- MIN-4 (Step 2.8): either restate the 57 names with kind and exit in the item, or add "re-Read Step 2.3 of this task file before writing the literal list".
- MIN-5 (Steps 2.2, 4.1, 5.1): cite `OQ-37` and `OQ-38` in Step 2.2, `OQ-41` in Step 4.1, `OQ-40`, `OQ-41` and `OQ-41a` in Step 5.1 (TB-Add-3 asks that items depending on an open question reference it by index).
- MIN-6 (Steps 3.4, 3.1): write out the `pageInfo` object (`{"hasNextPage": false, "endCursor": null}`) in the project-items fixture; give the full parameter lists of `marker_comments`, `edits`, `project_items` and `reread` and the type of `Read.value` per read (P6 consumes them).
- MIN-7 (Steps 2.10, 3.8, 4.6, 5.9): add "at most 3 fix-and-rerun rounds, then log the blocker and stop" so the loop is bounded.
- MIN-8 (Step 1.1): add a verification clause ("Read the first 12 lines of this file and confirm `status` and `start_date`") and the standard blocker clause.
- MIN-9 (Steps 3.9, 5.10): state the verdict when `make lint` exits nonzero only because of a file this task did not touch (for example "record the exit code and the file, and mark PASS-WITH-NOTE only if every reported path is outside the files this task created"). Research 03 line 150 shows the baseline is clean ("All checks passed!"), so this should be rare.
- MIN-10 (Step 2.3): state that `ts=None` is written as JSON null and `host=None` as JSON null, or that the caller must pass both.
- MIN-11 (Step 2.5): replace "finishes well under 5 seconds" with "returns in under 3.0 s measured with `time.monotonic()` in the test".
- MIN-12 (Step 4.1): add a sentence that importing the three predicates helpers is a reading of D 239 ("types only") recorded in OQ-46, or add it to OQ section D.
- MIN-13: creation items end with "ensuring ..." prose. The measurable checks exist, but in later items (2.9, 2.10, 2.11, 3.8-3.11, 4.6, 4.7, 5.9-5.11). Acceptable given the phase checkpoints; no change required beyond MIN-2 and MIN-11.

## Checklist results for this lens (10 checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 B2 components in every item | PASS with notes | 71 of 72 items have context (Read list), action, output path, verification ("ensuring") and completion gate ("If unable ... Once done, mark complete"); Step 1.1 lacks verification and blocker clauses (MIN-8) |
| 2 | No item references prior-item context without restating it | FAIL | Step 2.8 (MIN-4); Steps 3.G12 and 5.G12 (IMP-3); Step 4.1 uses `PendingContext` that is defined nowhere (IMP-2) |
| 3 | Agent-spawning items have fully embedded prompts | FAIL (cycle 2 only) | All 18 first-cycle spawn items (3.G2-3.G7, 3.G9-3.G11 and 5.G2-5.G7, 5.G9-5.G11, each prompt embedded in full) PASS; cycle-2 spawns in 3.G12 and 5.G12 are by reference (IMP-3) |
| 4 | File paths specific | PASS | Every output path is a full repo-relative path; QA report names in the gate prompts match the names Steps 3.G8 and 5.G8 read (checked all six per gate) |
| 5 | Verification measurable (commands with expected results) | PASS with notes | Phase checkpoint items give commands and expected exit codes (G-1 exit 5 at P1, exit 0 from P2; G-4, G-5, G-8 with NO_MATCH); creation-item verification is prose (MIN-13); IMP-6 makes one assertion unsatisfiable |
| 6 | No batch items; one item per file, component or gate agent | FAIL | One file per item holds, one agent per spawn item holds, but five items are oversized (IMP-5) |
| 7 | No item rests on a [CODE-CONTRADICTED] or [UNVERIFIED] claim as fact | FAIL (one) | C14, C21, lazy-import and PATH-guard contradictions are corrected; unverified gh and Orca shapes are confined to fixtures; Step 5.6 and 5.1 assert a false behaviour of the original `_find_orca` (IMP-4) |
| 8 | Citations exist and say what the item claims (at least 15) | PASS with notes | 28 checked; 1 drift (MIN-1), 1 false claim (IMP-4) |
| 9 | Code-surface Context fields carry file:line or evidence-absence (TB-Add-8) | PASS | Checked every non-gate item of P1-P5; each has either a file:line anchor or an `<!-- evidence-absence: ... -->` comment |
| 10 | Items a mid-task executor cannot run without information from another phase | listed below | 3 items |

### Items a mid-task executor cannot run without information from another phase (check 10)

1. Step 4.1 (P4): needs the `PendingContext` field list; no phase, design, spec or research file supplies it (IMP-2). The P6 cycle item that calls `record.mark_pending` depends on the same list.
2. Step 5.5 and Step 5.2 (P5): need the rule for extracting an id from an `unknown` error reply; defined nowhere (IMP-1). The P8 e2e stub scenario for an `unknown` launch will depend on the same rule.
3. Step 3.G12 and Step 5.G12 (gate control): the second fix cycle needs the prompts of Steps G8-G11 and a path-substitution rule, which the item does not restate (IMP-3).
Also noted, no finding: Steps 2.1, 2.4 and 2.5 refer forward to Phase 8 only to say that Phase 8 does not exist yet; Step 1.3 refers to Step 10.2 only in a sentence ("BASE is captured in Step 10.2"); neither needs outside information to run.

## Self-audit

- Would the user believe "0 issues"? No, and none is reported: 6 blocking and 13 minor findings, each with a tool-backed citation (Reads of main.py:555-565, atomic.py:1-45, install_user_setup.py:195-225, origin_repo.py:60-105, poll-augment-review.sh:46-80, test_install_user_setup.py:255-287, test_issue_repo_resolution.py:10-62, design 1-14, 80-105, 214-306, 390-535, 537-651, 653-727, 728-800, 826-902, spec 72-134, 148-194, 300-398, R-003 16-250, research/03:146-160, research/05:132-144 and 250-261, template 02 grep for fix-cycle rules, and `awk` item-length measurement).
- Not verified by me (outside the lens or not reachable): the claims in items about behaviour of `gh` and `orca` (unverifiable offline; correctly marked unverified in the items), the content of Phase 6-10 items (assigned to another agent), and whether `uvx --offline ruff@0.15.20` runs on the executor's host.

**Confidence:** Verified: 10/10 lens checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this measures verification coverage of the lens checklist, not the quality of the task file)
**Tool engagement:** Read: 40 | Grep: 16 | Glob: 2 | Bash: 6 (no web research: tavily_search 0, tavily_extract 0, fallbacks 0)

VERDICT: FAIL

Blocking issues (must be fixed before execution): IMP-1, IMP-2, IMP-3, IMP-4, IMP-5, IMP-6. Total: CRITICAL 0, IMPORTANT 6, MINOR 13. Exact fix text for each IMPORTANT issue is given above.

## QA Complete

