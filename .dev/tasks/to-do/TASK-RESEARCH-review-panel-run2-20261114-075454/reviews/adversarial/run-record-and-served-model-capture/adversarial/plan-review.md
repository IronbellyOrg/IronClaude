# Plan review: refactor-plan.md, slot C-08 (run-record-and-served-model-capture)

Reviewer role: analytical fidelity check only. Read-only except this file. Files read: `refactor-plan.md`, `base-selection.md`, `debate-transcript.md` (Scoring Matrix, Convergence Assessment, Round 2 text), `round2-advocate-A.md`, `round2-advocate-B.md`, `invariant-probe.md`, `round2.5-fault-finder-raw.md`, `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md` (rows X-007 to X-011, A-001 to A-004). All paths are under the `adversarial/` folder of this slot.

Result: 9 DEFECTs (2 of them touch an OPEN point presented as decided), 5 missing items, plus 5 minor notes. Checks 1 to 5 follow.

## Check 1. Facts

29 statements verified OK (all against the debate files):
1. "28 of 31 points agreed (90.3%)": `debate-transcript.md` Convergence Assessment (28/31 = 0.9032). OK.
2. Status BLOCKED_BY_INVARIANTS, 13 HIGH UNADDRESSED: same section and `invariant-probe.md` Summary. OK.
3. HIGH ID list INV-001, 002, 005, 006, 009, 010, 011, 013, 016, 017, 020, 021, 022 (13): `invariant-probe.md` Summary. OK.
4. MEDIUM ID list INV-003, 004, 007, 008, 012, 015, 018 (7): same. OK.
5. 2 LOW ADDRESSED (INV-014, INV-019): same. OK.
6. C-005 and X-011 at 95%: Scoring Matrix. OK.
7. C-002 and X-002 at 95%: Scoring Matrix. OK.
8. X-001 winner Variant 2 at 85%: Scoring Matrix. OK.
9. C-007 at 85% ("both labelled bases derive from one per-run file"): Scoring Matrix. OK.
10. Unresolved set C-001, X-006 (label splits, substance converged) and A-009 (substantive split): Convergence Assessment. OK.
11. A-009 positions (A yes for check-then-append; B no because the reason depends on an append-time refusal that breaks `tests/review/test_review_telemetry.py:363-400`): Scoring Matrix row A-009. OK.
12. The eight B corrections A never answered (telemetry lock dropped, append-time one-live-outcome refusal not shipped, join by `description`, `strict` label rule, `LedgerError.reason`, lock placement in `manifest_cmd.py`, `:228` assertion edit, build order): Convergence Assessment, "Round 2 content that the other advocate did not answer". OK.
13. `ledger.py:116, 121, 154` for `LedgerError.reason`: B R2 4.1 item 6 / N-B5. OK.
14. `ledger.py:114-121, 150-157` ordering of the round-order and duplicate checks before the no-valid-block check: A R2 C1 / N2. OK.
15. `manifest.py:293-296`, `manifest_cmd.py:204`: A R2 N1. OK.
16. `manifest.py:495, 521-524`: B R2 N-B7. OK.
17. `telemetry.py:289, 411-414` shared `validate_record`: A R2 section 1 table, B R2 X-007. OK.
18. `tests/review/test_review_telemetry.py:363-400`: B R2 N-B2. OK.
19. `test_shadow_skill_contract.py:228` pins `model_observed:`; `:65` fence; `:291-299` permuted case: B R2 N-B1, N-B4, C-005. OK.
20. `SKILL.md:585` (`### 6.3`), `:338` (`panel_fallback_reason`), `:344` (`calibrated` has no call site): A R2 / B R2. OK.
21. `cycle.py:7` is a docstring; lock precedent `issue_watch/record.py:389-417` is `LOCK_EX | LOCK_NB`, raises `LockHeld`: A R2 C9, C10. OK.
22. `tests/cli/reflect/test_shadow_exit_script.py:313-319` read-only pin: B R2 N-B6. OK.
23. Round 2.5 measurements: per-event over-count 2.0x to 2.6x (INV-009), per-message `output_tokens` 0.07% to 3.09% of `modelUsage` and 0 of 15 within 2% (INV-010), non-Anthropic `output_tokens` 0 (INV-011), description equal to a reviewer id in 0 of 12 calls (INV-006), interactive layout `subagents/agent-<id>.jsonl` plus `.meta.json` (INV-005). OK.
24. Withdrawn items in Change 1 (`/2`, `record add`, `rev`, `ext{}`, memory move; "A Round 2 N5, item 13"): A R2 section 4 items 4, 7, 13 and "Round 1 positions I have changed". OK.
25. `manifest.py:389-397`, `manifest_cmd.py:174-199` (no path for `failed`/`--publish-from`): A R1 weakness 1, B R2 section 1. OK.
26. Which B R2 item B disagreed with: B 4.1 item 5 (ordinal join) and item 7 (append-time live-outcome refusal) are the DISAGREE verdicts; plan Changes 3 and 12 carry both. OK.
27. Which round items B corrected (lock placement, `strict` rule, `LedgerError.reason`, `:228`, build order, join): plan Change 12 list equals the Convergence Assessment list. OK.
28. "Withdrawn by Advocate B": C-001/C-002/X-002 manifest route (`agents[]`), C-003/X-008 two producers: B R2 section 1 and 4.4. OK.
29. M1 to M5 content in Change 7 (M1 gates `ingest`, `export` `model.observed`, `--print-identity`; M2 gates `rev`; M3 gates non-reviewer rows; M4 one assertion exception; M5 A3 replay): A R2 item 12 plus B R2 4.1 item 12. OK.

DEFECTs:

DEFECT 1 (Change 2, merge row). Plan: "rows from the `except` branch only for the no-valid-block, round-order and duplicate-reviewer causes". Correct fact: the agreed closed `reason` enum has four values, `no_valid_block`, `round_order`, `duplicate_reviewer` and `other`; `LedgerError.reason` defaults to `other`, and B's test (c) pins `refused(other)` for a corrupt ledger. The restriction the debate agreed is "action rows only, never cost rows", not "only three causes". Source: `round2-advocate-A.md` section 4 item 6; `round2-advocate-B.md` 4.1 items 6 and 14(c); `invariant-probe.md` INV-016 evidence (2) (the enum has no `quorum`, and quorum would fall under `other`).

DEFECT 2 (Change 11, concessions). Plan: "the size of the change after repairs is not smaller than B's, so size is not the differentiator". The relationship is reversed. A R2 says B's repaired change "is not the smaller change" (not smaller than A's); B R2 section 1 conceded "not smaller than A" and countered that A's is not small either, so size is not the differentiator. Source: `round2-advocate-A.md` section 2 point 1; `round2-advocate-B.md` section 1 ("A's section 2 point 1" paragraph). It is also not an A concession.

DEFECT 3 (Change 11, concessions). Plan lists "per-event summation double counts (INV-009)" as an extension of "What A concedes". No advocate conceded it; it is a Round 2.5 finding, UNADDRESSED, HIGH, and A had no turn after the probe. Label it a probe finding (Change 12 territory), not a concession. Source: `invariant-probe.md` INV-009; `debate-transcript.md` Convergence Assessment.

DEFECT 4 (Change 8, PR-3; an OPEN point shown as decided). Plan: "SKILL steps 2, 3, 9, 10 with the single test edit". Step 3 is B's added edit (name each Agent call with its reviewer id), which exists only to support the join by `description`, and that join is OPEN (Change 3). A's items 9 and 15 list steps 2, 9, 10 only. Source: `round2-advocate-A.md` items 9, 15; `round2-advocate-B.md` 4.1 items 5, 9(a), 15; `invariant-probe.md` INV-006 ("B's edit would add that"). Step 3 must be marked OPEN with the join.

DEFECT 5 (Change 8 PR-1 and Change 2 telemetry row; OPEN A-009 decided by omission). Plan PR-1: "lock helper, manifest lock in `manifest_cmd.py`, `strict` at append, `LedgerError.reason`, tests"; Change 2 telemetry row names only `strict` and `load` unchanged. A's PR-1 contains "telemetry lock plus `strict` plus the live-outcome check"; B's PR-1 contains `live_outcome_conflicts` and no telemetry lock. The plan names none of these three, so an executor will silently choose B's side. Neither the "lock helper" row nor the telemetry row says "telemetry lock and append-time one-live-outcome refusal: OPEN (A-009), A: yes (check-then-append), B: no (breaks `test_review_telemetry.py:363-400`; offers `live_outcome_conflicts` at load)". Source: `round2-advocate-A.md` items 2, 7, 15; `round2-advocate-B.md` 4.1 items 2, 7, 15; Scoring Matrix A-009.

DEFECT 6 (Base Weaknesses Addressed, row 4). Plan: weakness "No lock on `append_record` ..." with "Better variant / source: Variant 2 for the lock; both for the helper". B dropped the telemetry append lock in Round 2 (4.1 item 2: ".append.lock is dropped"; 4.4 item 4); the party asking for it is A (R2 item 2, N6), and the point is split. Variant 2 is the source only for the manifest-lock placement in `manifest_cmd.py` (N-B7). The row should not list the `append_record` lock as addressed. Source: `round2-advocate-B.md` 4.1 item 2, 4.4 item 4; Scoring Matrix A-009.

DEFECT 7 (Change 5, target). Plan: "correct item 20 and item 14" with integration point "Section 4.3 and a new 4.6". The debate corrects only item 20 (the `cycle.py` hit, X-012); the plan's rationale gives no correction for item 14 and no debate file corrects it (item 14 is only cited in X-009 and A-003 as context). Also item 20 sits in base section 4.4 (items 19 and 20), not 4.3; item 14 sits in 4.3. Source: `diff-analysis.md` rows X-009, A-003; `round1-advocate-B.md` weakness 9; `round2-advocate-A.md` C9; `variant-1-original.md` sections 4.3 and 4.4.

DEFECT 8 (Base Weaknesses Addressed, row 8). Plan: "Change 3: `export` projects cost into `reviewer_run`; deterministic ids". Change 3 (events schema, writers, adapter) contains no text on `export`, cost projection or deterministic ids, and no other change contains it (Change 1 names `record export` only). The target the row points to does not carry the fix. Source: `round2-advocate-A.md` C4, item 8; `round2-advocate-B.md` 4.1 item 8.

DEFECT 9 (Change 2, attribution). Plan: "(X-003, X-004, conceded by A)". A conceded X-004 only (A R1 concession 1; A R2 C1). X-003 was INTRA-B, conceded by B (B R1 concession 2; B R2 section 1), and A adopted B's repair with the restriction. Source: `diff-analysis.md` summary (INTRA-A: X-004, X-010; INTRA-B: X-002, X-003, X-007, X-008, X-009).

Minor notes (not counted as DEFECTs):
- Change 6 "stale-lock fallback text": the debate wording is "a failed or timed-out lock is recorded as `panel_fallback_reason` and the run continues as legacy" (A R2 item 2; B R2 4.1 item 2). "Stale-`rev`" was B's original text, and `rev` is deferred.
- Change 5 "(0 of 15 within 2%)" next to "0.07% to 3.09% of `modelUsage`" can be misread: 12 of 15 ratios are below 2%. The probe means none of the 15 sums is within 2% of equality with `modelUsage`.
- Change 10 cites "A Round 2 item 10" for the withdrawal of the cross-run all-agents store; that is item 10 of "Round 1 positions I have changed". The resolution item that states the crawl is item 11.
- Change 11 says rewrite parts 1 and 4 of the base answer but gives no rationale for part 4; the objection paragraph itself still names the `/2` bump and the memory writer, which the hybrid dropped.
- Change 6 INV-F: the fence pin counts the literal `src/superclaude` across the whole reflect skill directory, not only `### 4.3a` (A section 5, `test_shadow_skill_contract.py:98`).

## Check 2. OPEN points presented as decided

- Join method: OPEN in Change 3, but Change 8 carries the step 3 edit that belongs to the description join. DEFECT 4.
- Telemetry lock (A-009) and append-time one-live-outcome refusal: OPEN in Change 12 and in "Changes NOT Being Made", but decided by omission in Changes 2 and 8 and wrongly listed as addressed in the weaknesses table. DEFECTs 5 and 6.
- M1(c) feasibility: OPEN (INV-010) in Change 7. OK.
- What the gate does with a printed finding, missing-events third state, vacuous mismatch on A3, class versus id collapse: OPEN in Change 9. OK.
- INV-016 quorum reason: Change 4 says the quorum refusal and "the quorum reason are not covered (INV-016, UNADDRESSED, HIGH)". That is accurate (the enum has no `quorum`) and it does not claim closure. OK, with the wording suggestion to say "OPEN" rather than "not covered".
- INV-001 not stated as closed: Change 4. OK.

## Check 3. Conclusions the debate did not reach

- Change 11 concession list (DEFECTs 2 and 3).
- Change 8 build order is adopted from B although A never answered it and it is not a code fact. Change 8 marks it "A did not answer it", and Change 12 lists it as unanswered, so the plan is internally consistent with its own governing rule; the Convergence Assessment says only code-verified B corrections are adopted. Treat as a note: label the order OPEN-adopted, not agreed.
- No other added conclusion found.

## Check 4. Sources and targets

All 12 changes name a source and a target that exist. Verified: `variant-1-original.md` sections 1 to 8 (section 2 table rows incl. manifest, telemetry, `openai_compat.py`, `merge_cmd.py`, memory; section 3 C-01/C-02/C-03 bullets and "Disagreement: none found"; section 4 items 14 and 20 and subsections 4.1 to 4.5; section 5 two lists; section 6 M1 to M5; section 7; section 8 objection plus answer parts 1 to 4 and the closing "What A concedes" paragraph). `round2-advocate-A.md` section 4 items 1 to 15 and section 1 C1 to C10. `round2-advocate-B.md` section 4.1 items 1 to 15, N-B1 to N-B10. `variant-2-original.md` sections 2 (reflect_shadow_exit row), 5.2, 6, 7, 8 (M4). Only target defects: DEFECT 7 (4.3 vs 4.4) and DEFECT 8 (Change 3 does not hold the cited text). Change 5 names a new 4.6, which does not exist and is a creation.

## Check 5. Missing from the plan (max 5)

1. `record export` design: deterministic `record_id` (hash of run_id, step, round, reviewer_id, attempt), required `--dir` or `SUPERCLAUDE_REVIEW_TELEMETRY_DIR` with no cwd default (A-006, 90%), visible `record_absent` (A-008, 90%), skip a null join and say why, `panel` group source from the resolution JSON. Source: A R2 item 8; B R2 4.1 item 8.
2. Agreed lock-helper properties (A-005 Hybrid 90%): blocking acquire with timeout, lazy `import fcntl`, `LockTimeout`/`LockUnavailable`, two lock files `manifest.lock` and `events.lock`, lock file created on demand and never unlinked, failed lock recorded as `panel_fallback_reason`. Source: A R2 item 2; B R2 4.1 item 2, N-B8.
3. Merge `--events` safety contract: without the flag merge is byte-identical to HEAD, a failed events write is a stderr warning with unchanged stdout, exit code, ledger and report, merge never reads events, `merged` rows carry `counts` from `findings.parse_block`. Source: A R2 item 6; B R2 4.1 item 6, N-B5. (INV-016 and INV-021 attack exactly this.)
4. B's `live_outcome_conflicts` count at `load` as the alternative to an append-time refusal (the second half of A-009). Source: B R2 4.1 item 7, 15.
5. The agreed identity rule and SKILL step content: `observed` only when every reviewer and calibrator row has exactly one served id; step 2 drops the `model_observed:` header instruction, step 9 copies from `export --print-identity`, step 10 runs `ingest` before `advance published`. INV-017 (HIGH) shows the step 9 versus step 10 order is unresolved, so the plan should state the content and mark the order OPEN. Source: A R2 items 8, 9; B R2 4.1 item 9; `invariant-probe.md` INV-014, INV-017.
