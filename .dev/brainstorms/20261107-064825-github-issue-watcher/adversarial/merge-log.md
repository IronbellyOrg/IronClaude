# Merge Log: GitHub issue watcher requirements spec

## Metadata

| Field | Value |
|---|---|
| Base | Variant D |
| Executor | merge-executor (Step 5 of the adversarial pipeline) |
| Plan | refactor-plan.md, Changes 1-74 |
| Changes applied | 74 of 74 (72 full, 2 partial) |
| Additional changes | AC-1..AC-7 from base-selection.md "Strengths to incorporate" |
| Status | COMPLETE WITH ESCALATIONS (2 open items for the orchestrator, see Post-Merge Validation) |
| Timestamp | 2026-11-07 |
| Output | merged-output.md (10253 words by `wc -w`) |
| Owner decisions | D1 option A; D2 claim-only; D3 only a validated integer issue number reaches a session prompt |

## Changes Applied

Line numbers are the provenance-comment lines in merged-output.md.

| # | Status | Location | Provenance tag |
|---|---|---|---|
| 1 | applied | §1, line 16 | `<!-- Source: invariant probe INV-024 (round 3) - merged per Change #1 -->` |
| 2 | applied | §1, line 34 | `<!-- Source: Variant A text, ruling C-014 (round 2) - merged per Change #2 -->` |
| 3 | partial | §2, lines 39 and 46 | `<!-- Source: seed brief line 59, verbatim - merged per Change #3 ... -->`; D1-D3 verbatim applied; the agent value is written as the constant `ORCA_AGENT` because the literal value is a banned word in the output files |
| 4 | applied | §2 NG-2, line 65 | `<!-- Source: Base (original, modified) - NG-2 replaced per Change #4 ... -->` |
| 5 | applied | §2, line 50 | `<!-- Source: invariant probe INV-027 (round 3) - merged per Change #5 -->` |
| 6 | applied | §2 NG-5, line 65 | same tag as Change 4 (NG-5 extended per Change #6) |
| 7 | applied | §3, line 79; FR-002, line 112 | `<!-- Source: rulings C-004 (round 3, Variants A, D, E), INV-007 - merged per Change #7 -->` |
| 8 | applied | §3 Tagged, line 81 | `<!-- Source: Variant A text, ruling C-001 (round 2) - merged per Change #8 -->` |
| 9 | applied | §3 Approved, line 83 | `<!-- Source: rulings C-002 (Variants A, B, C), C-013, INV-008, INV-024 - merged per Change #9 -->` |
| 10 | applied | §3, line 91 | `<!-- Source: invariant probe INV-009 (round 3) - merged per Change #10 -->` |
| 11 | applied | §3, line 93 | `<!-- Source: invariant probe INV-026 (round 3), conflict ruling K9 - merged per Change #11 -->` |
| 12 | applied | §3 Project and Backlog, line 95 | `<!-- Source: rulings C-003 (Variant E), X-005, INV-018, K8 - merged per Change #12 ... -->` |
| 13 | applied | §3 Intended owner, line 97 | `<!-- Source: rulings C-004 (round 3), INV-014, K12 - merged per Change #13 ... -->` |
| 14 | applied | §3 Claimed, line 99 | `<!-- Source: ruling C-024 (round 2), INV-021 (round 3) - merged per Change #14 -->` |
| 15 | applied | §3 Eligible, line 101 | `<!-- Source: ruling C-015 (round 2) - merged per Change #15 -->` |
| 16 | applied | §4 preamble, line 106 | `<!-- Source: Variant A text, ruling S-001 (round 2) - merged per Change #16 ... -->` |
| 17 | applied | FR-003, line 115 | `<!-- Source: Variant A text, ruling C-006 (round 2); INV-014 (round 3) - merged per Change #17 -->` |
| 18 | applied | FR-004, line 118 | `<!-- Source: rulings C-006, INV-014 - merged per Change #18 -->` |
| 19 | applied | FR-007, line 127 | `<!-- Source: ruling X-005 (round 3 final), C-015 - merged per Change #19 -->` |
| 20 | applied | FR-022, line 130 | `<!-- Source: Variant A text, ruling C-015 (round 2) - merged per Change #20 -->` |
| 21 | applied | FR-011, line 142 | `<!-- Source: Variant D round-2 text, ruling C-009; conflict ruling K2 - merged per Change #21 ... -->` |
| 22 | applied | FR-014, line 151 | `<!-- Source: invariant probe INV-001 (round 3), ruling C-007, conflict ruling K1 ... - merged per Change #22 ... -->` |
| 23 | applied | FR-014, line 151 | same tag (merged per Change #23) |
| 24 | applied | FR-015, line 154 | `<!-- Source: invariant probe INV-003 (round 3), conflict ruling K3 - merged per Change #24 ... -->` |
| 25 | applied | FR-016, line 157 | `<!-- Source: Variant A text, ruling C-008 (round 2); INV-015; conflict ruling K5 - merged per Change #25 -->` |
| 26 | applied | FR-023, line 160 | `<!-- Source: Variant E text, invariant probe INV-015 (round 3) - merged per Change #26 -->` |
| 27 | applied | FR-024, line 163 | `<!-- Source: invariant probe INV-016 (round 3, ...), conflict ruling K10 - merged per Change #27 -->` |
| 28 | applied | FR-017, line 166 | `<!-- Source: Variant A text, ruling C-018 (round 2); INV-027 (round 3); conflict rulings K6, K7 - merged per Change #28 -->` |
| 29 | applied | FR-018, line 169 | `<!-- Source: Base (original, modified) - mid-cycle re-check appended per Change #29 ... -->` |
| 30 | applied | FR-025, line 172 | `<!-- Source: invariant probe INV-011 (round 3), ruling C-010 - merged per Change #30 -->` |
| 31 | partial | FR-013, line 148 | `<!-- Source: Variants A and D text, ruling C-010 (round 2) - merged per Change #31; ... -->`; argv and probe applied; agent value written as `ORCA_AGENT` (same reason as Change 3) |
| 32 | applied | FR-012, line 145 | `<!-- Source: Variant A text, ruling C-012 (round 2) - merged per Change #32 -->` |
| 33 | applied | FR-019, line 175 | `<!-- Source: invariant probe INV-005 (round 3), conflict ruling K11 - merged per Change #33 -->` |
| 34 | applied | FR-020, line 178; §1 line 28 | `<!-- Source: ruling C-019 (...) - merged per Change #34 -->` |
| 35 | applied | FR-021, line 181 | `<!-- Source: Variant D round-2 text, ruling C-018; INV-006; INV-004 - merged per Change #35 -->` |
| 36 | applied | FR-026, line 184 | `<!-- Source: Variant D text, ruling C-020 (round 2); conflict rulings K7, K10 - merged per Change #36 -->` |
| 37 | applied | FR-027, line 187 | `<!-- Source: Variant A, ruling C-021 (round 1); C-013, INV-019, C-005 - merged per Change #37 -->` |
| 38 | applied | FR-028, line 190 | `<!-- Source: rulings C-016 and X-006 (...), X-007 - merged per Change #38 -->` |
| 39 | applied | FR-029, line 193 | `<!-- Source: invariant probe INV-017 (...), ruling C-008 timeouts - merged per Change #39 -->` |
| 40 | applied | NFR-002, line 201 | `<!-- Source: rulings C-010, INV-011, INV-018, C-025 - merged per Change #40 -->` |
| 41 | applied | NFR-003, line 203 | `<!-- Source: rulings C-003, X-005, INV-018 - merged per Change #41 -->` |
| 42 | applied | NFR-005, line 207 | `<!-- Source: ruling C-022 (round 1, all five variants) - merged per Change #42 -->` |
| 43 | applied | NFR-006, line 209 | `<!-- Source: rulings C-019, C-025; Variant D round 2 - merged per Change #43 -->` |
| 44 | applied | NFR-008, line 213 | `<!-- Source: rulings C-008, INV-017 - merged per Change #44 -->` |
| 45 | applied | NFR-009, line 215 | `<!-- Source: rulings C-006, S-003 (Variant E arithmetic), X-007 - merged per Change #45 -->` |
| 46 | applied | NFR-011, line 219 | `<!-- Source: rulings X-003 (round 3 final), S-005, X-007 - merged per Change #46 -->` |
| 47 | applied | NFR-013, line 223 | `<!-- Source: Base (original, modified) - (b) narrowed and (d) added per Change #47 ... -->` |
| 48 | applied | NFR-014, line 225 | `<!-- Source: Variant A text, ruling S-004 (round 2) - merged per Change #48 -->` |
| 49 | applied | §6 T4, line 230 | `<!-- Source: Base (original, modified) - rows T4, T7, T8, T10 replaced per Changes #49-#52 ... -->` |
| 50 | applied | §6 T7, line 230 | same tag |
| 51 | applied | §6 T8, line 230 | same tag |
| 52 | applied | §6 T10, line 230 | same tag |
| 53 | applied | §6 T13-T16, line 230 | same tag (T13-T16 added per Change #53) |
| 54 | applied | §7, line 258 | `<!-- Source: ruling S-005 (round 2, Variant D text), C-017, conflict ruling K7 - merged per Change #54 -->` |
| 55 | applied | §7, line 261 | `<!-- Source: rulings C-007 (round 3 final), INV-007, INV-015, INV-016, INV-024, U-005 - merged per Change #55 -->` |
| 56 | applied | §7, line 264; FR-010, line 139 | `<!-- Source: ruling C-007 (round 2 Variant D text, confirmed round 3) - merged per Change #56; ... -->` |
| 57 | applied | §7, line 267 | `<!-- Source: ruling C-007 (round 3), INV-001, conflict ruling K1 - merged per Change #57 -->` |
| 58 | applied | §7 transition table, line 273 | `<!-- Source: rulings X-001, X-002 (...), INV-004, INV-002, INV-021, C-024, K13, A-009 - merged per Change #58 (replaces the whole base table) -->`; the base `ineligible` row is gone with the replaced table |
| 59 | applied | §7 parameters, line 270 | `<!-- Source: rulings C-008 (round 2), INV-015, conflict ruling K5 - merged per Change #59 -->` |
| 60 | applied | §7 recovery, line 293 | `<!-- Source: rulings X-003 (round 3 final), C-020, INV-024 - merged per Change #60 -->` |
| 61 | applied | §8 modules, line 300 | `<!-- Source: ruling S-004 (round 2) - merged per Change #61 (...) -->` |
| 62 | applied | §8, line 303 | `<!-- Source: rulings C-021 (Variant A), C-020, C-005 - merged per Change #62 -->` |
| 63 | applied | §8 exit table, line 306 | `<!-- Source: rulings X-007 (round 2, Variant A text), INV-006 (round 3), conflict rulings K4, K6 - merged per Change #63 -->` |
| 64 | applied | §8 tests, line 322 | `<!-- Source: Base (original, modified) - test files and acceptance property appended per Change #64 ... -->` |
| 65 | applied | §8 runbook, line 345 | `<!-- Source: Base (original, modified) - ... step 6 replaced and steps 7-10 appended per Change #65 ... -->` |
| 66 | applied | §8 gates, line 327 | `<!-- Source: ruling S-003 (round 1) - merged per Change #66; ... -->` |
| 67 | applied | §9 FU-1..FU-10, line 361 | `<!-- Source: ruling C-023 (round 2, Variant A text), INV-003, INV-010, ... - merged per Change #67 -->` |
| 68 | applied | §9, line 373 | `<!-- Source: ruling C-023 (round 2, last sentence); seed brief - merged per Change #68 (...) -->` |
| 69 | applied | §10 OD rows, line 378 | `<!-- Source: Base (original, modified) - OD-2, OD-5, OD-7, OD-8, OD-9 replaced and OD-10, OD-11 appended per Change #69 ... -->` |
| 70 | applied | §11 R3, R8, line 396 | `<!-- Source: Base (original, modified) - R3 and R8 rewritten per Change #70 ...; R10-R18 appended per Change #71 ... -->` |
| 71 | applied | §11 R10-R18, line 396 | same tag (R10-R18 appended per Change #71) |
| 72 | applied | §12, line 422; status line 2 | `<!-- Source: Variant A text, ruling S-007 (round 2) - merged per Change #72; ... -->` |
| 73 | applied | §13, line 462 | `<!-- Source: diff-analysis A-001..A-010, rounds 1-3 - merged per Change #73 (new section) -->` |
| 74 | applied | whole document (sweep, no tag) | no provenance comment: a sweep edits in place. Grep found 0 hits for each retired term (filters.py, state.py, item-list, rate_remaining carried, last_cycle_age, unknown_expired, not_backlog, project-number, issue view, `<state-dir>`, would_launch, `result=`, ineligible, exit_code) |

## Additional changes

### Strengths from base-selection.md that the plan did not cover

| ID | Item | Location | Provenance |
|---|---|---|---|
| AC-1 | "Stricter subset" sentence opening §3 | §3, line 76 | `<!-- Source: Base (original, modified) - opening sentence extended per base-selection item 2 (AC-1, Variant C section 3) -->` |
| AC-2 | Alternatives table (options A-C with reasons) | §2, line 53 | `<!-- Source: Variant C, section 2 - merged per base-selection item 3 (AC-2) -->` |
| AC-3 | Orca probe in FR-013 plus threat row T17 | FR-013 line 148; §6 line 230 | `... Orca probe from Variant B FR-014 - merged per base-selection item 11 (AC-3) ...` |
| AC-4 | RC1-RC3 table | §1, line 19 | `<!-- Source: Variant B, section 1.1 - merged per base-selection item 13 (AC-4) -->` |
| AC-5 | Re-approval resets neither `attempts` nor `launches` | §7, line 264 | `... re-approval note from Variant B OD-6, merged per base-selection item 12 (AC-5) -->` |
| AC-6 | SLO and GWT expanded at first use | line 2 and line 106 | noted in those two tags |
| AC-7 | Runbook item-list removal | §8 runbook | covered by Change 74; no separate edit |
| item 8 | Typed stage protocols | not merged | SKIPPED: conflicts with ruling U-001 |

### Consistency fixes made while merging (no new content)

- FR-011 re-read uses `gh api --method GET repos/IronbellyOrg/<repo>/issues/<N>` instead of `gh issue view`, so it fits the NFR-002 argv list.
- FR-001 now expects two idle calls, to match the NFR-009 idle budget.
- NFR-007 scope now refers to FR-022.
- OD-3 and OD-6 aligned with §3 and FR-027.
- FU-4 now includes exit 7.
- Two invented sentences removed during the merge: a parenthetical in the §7 unknown/reset sentence, and a runbook step-1 claim that check-config runs the Orca probe.

## Post-Merge Validation

### Structural

- Headings: one H1 (line 3), then `## 1` to `## 13` at lines 11, 37, 74, 104, 197, 228, 253, 298, 359, 376, 394, 420, 460. No skipped level, no out-of-order number.
- IDs are unique and contiguous: FR-001..FR-029, NFR-001..NFR-014, T1-T17, R1-R18, OD-1..OD-11, FU-1..FU-10, A-001..A-010, NG-1..NG-5, RC1-RC3.

### References

| Measure | Count |
|---|---|
| ID references in total | 377 |
| Resolved (target ID defined in the document) | 377 |
| Broken (out-of-range or undefined IDs) | 0 |

### Contradictions

1. ESCALATE. Plan text: "`unknown` never moves on the lease; it leaves only via `claimed` or `reset`" (§7, from the plan). FR-026 and the Change 58 transition table allow `reset` only from `abandoned`. As merged, an `unknown` entry that never gets claimed can only leave via `claimed`. The plan has to choose: add an `unknown` -> reset row and widen FR-026, or drop "or `reset`".
2. ESCALATE. No exit code is defined for `spawn_error`. The exit table maps "a launch ended failed or unknown" to 7, but the plan does not say whether a `spawn_error` launch counts as that.
3. NOTE. Likelihood and impact for R11-R18 are marked [PROPOSAL]. The plan gave ratings only for R10.
4. NOTE. NFR-003 has to name the repository. Its name contains one of the banned words as a substring, so that substring appears in merged-output.md. A whole-word grep for the four banned words finds 0 hits.
5. NOTE. Many provenance comments name a ruling or invariant probe (for example "ruling C-015" or "invariant probe INV-024"), not "Variant X, section Y". The plan cites rulings as sources, so naming a variant and section would misattribute them. Each tag still ends with "merged per Change #N".

## Checklist verification

Each item was grepped in merged-output.md. Every pattern returned 1 or more hits.

| # | Item | Grep evidence | Result |
|---|---|---|---|
| 1 | Tagged definition | `**Tagged.**` (1) | PASS |
| 2 | Approved definition | `**Approved by a human.**` (1) | PASS |
| 3 | Project and Backlog | `**In a Project and in Backlog.**` (1) | PASS |
| 4 | Intended owner | `**Intended owner.**` (1) | PASS |
| 5 | Eligible | `**Eligible issue.**` (1) | PASS |
| 6 | Routing | `**Routing:**` (1); T7, FR-025, FR-013 present | PASS |
| 7 | Dispatch record | `**Transitions.**` (1); "`launches` is incremented in the same durable write" (1) | PASS |
| 8 | Security model | `T16 \|` (1); `R18 \|` (2); T10 and OD-7 present | PASS |
| 9 | Coder#477 statement | "Option A makes IronbellyOrg/Coder#477 unnecessary" (1) | PASS |
| 10 | Deliverables | `FakeRunner` (2); `_assumed_shape` (2); NFR-005 present | PASS |
| 11 | Follow-ups | `FU-10` (1) | PASS |
| 12 | Acceptance criterion | "starts exactly one mocked launch per eligible issue" (1); FR-012 present | PASS |
| 13 | Open decisions | `OD-11` (2) | PASS |
| 14 | Traceability UNVERIFIED tags | `UNVERIFIED` (12) | PASS |
| 15 | D1-D3 verbatim | full D1-D3 line (1) | PASS |
| 16 | Assumptions | `**A-010** CONSTRAINT` (1) | PASS |
| 17 | Exit table precedence | "first of 2, 6, 7, 5, 3, 4" (1) | PASS |
| 18 | Guarantee wording | "at most one claim session per issue per intact, single dispatch store per login" (1) | PASS |

## Summary

| Measure | Count |
|---|---|
| Planned | 74 |
| Applied | 74 (72 full, 2 partial: Changes 3 and 31) |
| Skipped | 0 |
| Failed | 0 |
| Additional (base-selection) | 7 applied (AC-1..AC-7); 1 skipped (item 8) |
| Escalations | 2 (unknown/reset contradiction; `spawn_error` exit code) |

## Orchestrator follow-up (after the merge executor returned)

- **M1 (contradiction fixed):** Section 7 said an `unknown` entry "leaves only via `claimed` or `reset`" while FR-026 and the transition table allowed `reset` only from `abandoned`. Decision: `reset <N> --forfeit-guarantee` is also allowed from `unknown` (the operator has checked the session first; the guarantee is forfeited explicitly and audited). FR-026 and the transition table row were edited accordingly.
- **M2 (missing exit code fixed):** `abandoned` with reason `spawn_error` now exits 7, like `failed` and `unknown`. The exit-code table, the failure-mode table and the FR-015 acceptance criterion were edited accordingly.
- Both edits were made by the orchestrator after the merge executor's validation and are covered by no further review in this stage; the spec-panel step reviews the whole document next.
