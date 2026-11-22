# Qualitative evaluation, pass 1 of 2 (forward order: V1, V2, V3)

Evaluator: independent, not an advocate. Rubric: 30 binary criteria, Claim-Evidence-Verdict. Variants scored as written, before the debate. V1 = variant-1-opus-architect.md, V2 = variant-2-sonnet-analyzer.md, V3 = variant-3-haiku-backend.md. Line numbers below are the variant's own lines.

Code spot-checks run (all read-only, snapshot paths under /home/coder/.cache/ic-snap-20261120 and the planb worktree): master `cycle.py:228` enabled default False (true); master `predicates.py:14` claim marker and `:279` `marker_in_window` (true); master `launch-level-guard.sh:787` COMMIT, PUSH, SUBMIT allowed at FS only (true); master `record.py:34-35` six states (true); master `sweep/commands.py:277-278` JSON to stdout (true); master `sweep/report.py:642-661` rows lack `session_id` and `worktree_path` (true); master `sweep/models.py:103`, `:131` (true); pr-a `wake.py:46-47`, `:69` orchestrator names and `.orchestrator/wakes` (true); pr-a `wake.py:269-299` O_EXCL, fsync, replace (true); pr-a `wake.py:565` ack bucket `taken` (true); pr-a `cycle.py:993-994` never woken again (true); planb `launch.py:48` `GOVERNED_LEVELS_ALLOWED = False` (true); master `orca_worktree.py:1515-1523` `cmd_pending` only writes (true); master `cycle.py:979` `_revalidate` (true); master `cycle.py:1092` save before launch (true); pr-p `plan_body.py:101-139` no fence state (true); pr-p `plan_body.py:138` `plan_check` (true); master `test_security_invariants.py:652`, `:683` (true); master `orca_worktree.py:55-56` IR-7 refusal off (true). No hallucinated code claim found in any variant.

## Completeness

| Id | V1 | V2 | V3 |
|---|---|---|---|
| C1 all Success Criteria | MET: diagram 20-58, per-piece stays/adopted/rewritten/interfaces, K1-K15, S0-S14 with MC-1..7, interface table, OA-1..22, RK table, ledger | MET: tagged diagram 26-58, four pieces, K1-K17, S0-S20 with files/tests/rollback/preconditions, MC-1..10, interface rows, owner items, ledger | NOT MET: stages S6-S8 (lines 170-172) name neither files nor PRs; per-piece paragraphs telegraphic |
| C2 edge cases, failure scenarios | MET: RK-12 abandoned wake, RK-13 crash between ack and state, unreadable process table starts nothing (K11) | MET: R15 stuck `unknown` stalls repo; MC-6 ack without state; 139-char repo names 64 KiB test (289) | MET: failure table 335-354: overlapping poll, lost receipt, crash after marker, restart storm, merge uncertainty |
| C3 dependencies, prerequisites | MET: every stage has Preconditions; S14 needs Coder 515, 516, per-host diff, Approved field (184) | MET: every stage lists preconditions; S20 needs Coder 515 and 516 (312); S7 needs S6 at master sha | MET: stage table Preconditions column (162-174); Coder 515/516 and host diff in S9 |
| C4 completion criteria per stage | MET: each stage lists tests, e.g. S12 Clay T13 cases (180), S9 parity and pin tests (174) | MET: per stage Tests, e.g. S16 refusal list (302), S11 parity test (277) | MET: Tests and checks column per stage; go/no-go evidence rule (178) |
| C5 explicit out of scope | NOT MET: only "D16 left out" (3); no stated out-of-scope list for the spec | NOT MET: "unfinished on purpose" note (409) covers verdicts, not scope exclusions | MET: concurrency, Pipeline launches, label writes, second host stated as separate future changes (178, 44) |
| Subtotal | 4/5 | 4/5 | 4/5 |

## Correctness

| Id | V1 | V2 | V3 |
|---|---|---|---|
| R1 no factual errors | MET: spot-checked `cycle.py:228`, `predicates.py:14`, guard `:787`, `record.py:34-35`, `models.py:103/131`, planb `launch.py:48`: all true | MET: spot-checked `cycle.py:979`, `report.py:642-661`, `security_invariants:652/683`, `launch.py:33`, `orca_worktree.py:1515`: all true | MET: spot-checked `cycle.py:1080-1112`, pr-a `wake.py:269-299`, `:545-581`, `cycle.py:992-994`, pr-p `plan_body.py:101-139`, IR-7: all true |
| R2 feasible approaches | MET: binds F from built grid (95); coordinator-claims end state has fallback to built claim mode (94, RK-7) | MET: keeps built claim path (155); F binding (156); additive config keys with restrictive defaults (158) | MET: F binding (9), save-before-launch already built (52), reuses pr-a fsync wake writer (154) |
| R3 terminology consistent | MET: state words BUILT-ON/OFF, NOT BUILT, REMOVED, DESIGN ONLY defined (188) and used throughout | MET: ledger words defined (317) and [B][P][C][N][D] tags (24) used consistently | MET: BUILT-ON/OFF defined (182); coordinator versus coordinators distinguished (115) |
| R4 no internal contradictions | MET: no conflict found; K1 interim mode, K9 cap 1 and S11 flag rule agree | NOT MET: K14 (168) starts real issues after throwaway run; S15 (296) keeps them off; rows 4, 22 cited but absent | MET: no conflict found; K8 table terse but compatible with 2.4 package-canonical text (84) |
| R5 claims supported | MET: Reason column per K row with file:line (94-108); interface Built column cites lines | MET: reasons with file:line in K table (155-171) and ledger Evidence column (319-351) | MET: absolute-path cites for K2, K11 (111) and built facts (52, 62, 154) |
| Subtotal | 5/5 | 4/5 | 5/5 |

## Structure

| Id | V1 | V2 | V3 |
|---|---|---|---|
| T1 logical ordering | MET: summary, architecture, contradictions, interfaces, stages, ledger, owner actions, risks (sections 1-8) | MET: same eight-section order, sections 1-8 | MET: same eight-section order, sections 1-8 |
| T2 consistent hierarchy | MET: ## sections, ### only for four pieces, bold stage labels uniform | MET: ## sections, ### 2.0-2.4, bold stage labels with uniform Scope/Tests/Rollback bullets | MET: ## sections, ### per piece and integrity rules, stage table uniform |
| T3 separation of concerns | MET: each piece has its own STAYS/ADOPTED/REWRITTEN/INTERFACES block (60-86) | MET: each piece has "What it is" plus four labelled blocks (62-147) | MET: four piece blocks; integrity rules split into own subsection (148-154) |
| T4 navigation aids | MET: K1-K15, S0-S14, MC-1..7, OA-1..22, RK-1..17, lane and O codes mapped per stage | MET: numbered interface rows, MC-1..10, stage map line (223), row cross references (81, 102) | MET: S0-S10 with lane/O mapping column, K1-K16, section cross reference (66) |
| T5 spec conventions | MET: all required sections present: summary, architecture, contradictions, interfaces, stages, built ledger, owner actions, risks | MET: all required sections present | MET: all required sections present |
| Subtotal | 5/5 | 5/5 | 5/5 |

## Clarity

| Id | V1 | V2 | V3 |
|---|---|---|---|
| L1 unambiguous language | MET: picks stated as single choices with explicit reversal conditions (94-108); owner answers spell each effect | MET: picks single-valued with reverse condition column; owner items state each answer's effect (359-376) | NOT MET: owner actions terse and unclear, e.g. "Cap 0: uncapped" (281), "Neither: stop rollout" (213) |
| L2 concrete | MET: exact paths, verbs, argv `gh pr merge ... --match-head-commit` (47), key defaults (97) | MET: exact cron line (179), file paths, NEW test names (214-221) | MET: exact merge argv (64), absolute paths, named crash tests (335-346) |
| L3 one-sentence summary per section | MET: each section opens with a purpose line, e.g. 90, 112, 145, 188 | MET: each piece starts "What it is" (64, 85, 106, 127) | MET: section 1 ten one-line points; each section has a single theme |
| L4 codes defined on first use | NOT MET: "MR-2" (94), "C-INV-1" (102), "U54" (184) used undefined at first use | NOT MET: reading guide (7) helps, but "U3, U8, U54" (312) and "MR-2" (12) undefined | NOT MET: "G2.1", "IR7" (189), "U54" (173), "R9/R17" (230) undefined for the owner |
| L5 actionable decisions | MET: OA-1..22 ordered by needing stage, each with answer effects (221-296) | MET: 18 numbered owner items gated to stages, answers inline (355-376) | MET: ten grouped decision blocks with answer effects (204-325) |
| Subtotal | 4/5 | 4/5 | 3/5 |

## Risk coverage

| Id | V1 | V2 | V3 |
|---|---|---|---|
| K1 3+ risks with likelihood and impact | NOT MET: single Sev column (302); no likelihood per risk | NOT MET: single sev column (382); likelihood given only once, owner item 2 (360) | NOT MET: Severity column only (333); no likelihood |
| K2 mitigation per risk | MET: each RK row pairs a proving test or control, e.g. RK-11 cap stays 1, RK-10 hook | MET: rows carry a narrowing control, e.g. R1 real issues off, R2 file pull fallback | MET: "Required test and safe failure" column gives safe behaviour per row (333-354) |
| K3 failure modes and recovery | MET: per-stage rollback; `DISABLED`, `enabled: false`, `start_mode: claim` (184); M2 recovery (RK-12) | MET: per-stage rollback; DISABLED or remove cron line (313); abandoned wake retargeted (MC test, 289) | MET: outbox replay, retarget, startup reconcile (152); per-stage rollback column |
| K4 external dependencies, failure scenarios | MET: RK-5 Coder 515/516 with `worktree_invalid`; RK-8 Orca `tui-idle`, U5, U25 | MET: R4 cron and Coordinator worktree; R2 mailbox fallback; R22 Orca tag | MET: outside-Run mailbox, blind process lookup, Coder image rows (340-353) |
| K5 monitoring, validation for detection | MET: `status --all` skip reasons (RK-16), post-merge audit AU1-AU8, `coordinator_absent` reason | MET: `status --json` `recent_skips` (197), audit log, live-test record (313) | MET: go/no-go evidence (178), operator sees unknown (336), audit and status reducer |
| Subtotal | 4/5 | 4/5 | 4/5 |

## Invariant and edge case coverage

| Id | V1 | V2 | V3 |
|---|---|---|---|
| I1 collection boundaries | MET: wake at most 64 KiB (123); `status --all` three repos one unreadable; observer three empty states (176) | MET: 139-char repo names fit 64 KiB test (289); empty folder, zero rows, could-not-read (307) | MET: empty folder, zero rows, failed read differ (76); reject over-size JSON (150) |
| I2 cross-component state interactions | MET: one store-state union keeping `claimed` for MR-2 in both modes (64); ack only after state (40) | MET: merged state machine (78) and cap counted over store plus claim files (163) | MET: ack carries matching issue-state revision; poll verifies state before accepting (130, 150) |
| I3 guard condition gaps | MET: fail closed on weakening config (180); missing `jq` refuses (178); absent keys safe (97) | MET: missing key gives most restrictive value (158); unreadable file counts in flight (163) | MET: reject symlinks, wrong schema, mismatched repo/issue/round (150); unknown never empty (44) |
| I4 count divergence | NOT MET: no duplicate-counter or off-by-one analysis; cap only "absent reads as 1" (102) | MET: "one issue with a store entry and a claim file counts once" (305); K17 counted-state set (171) | MET: duplicate wake returns existing state (150); overlapping poll one reservation; restart budget persisted (335, 342) |
| I5 interaction effects | MET: RK-6 revert plus PR 686 break `--help`; K1 claim and coordinator sharing a worktree removed | MET: R24 merge path safe only as a unit; R9 claim agent and coordinator in one worktree | MET: lock order rule, producer releases before delivery (150); cap race with hand-back deadlock (345) |
| Subtotal | 4/5 | 5/5 | 5/5 |

## Totals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 4 | 4 |
| Correctness | 5 | 4 | 5 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 4 | 3 |
| Risk coverage | 4 | 4 | 4 |
| Invariant and edge case | 4 | 5 | 5 |
| Total | 26/30 | 26/30 | 26/30 |

Three-way tie on the total. The losses differ: V1 loses out-of-scope, codes, likelihood and count divergence; V2 loses out-of-scope, the internal K14/S15 contradiction, codes and likelihood; V3 loses per-stage files, clarity of its owner actions, codes and likelihood.

## Edge-case floor

V1 4/5, V2 5/5, V3 5/5. All three are above the floor of 1 of 5 and eligible as base.
