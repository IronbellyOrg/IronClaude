# QA Source-Fidelity Report 1 — RELEASE-SPEC §3.1 + §8.3 vs Backtest Harness

**Agent role:** SOURCE-FIDELITY (report-only, fix_authorization: false — NO file modified)
**Date:** 2026-06-12
**Assigned source range:** RELEASE-SPEC §3.1 (E1→wave→FR→scenario traceability matrix, lines 249-257) + §8.3 (per-escape manual/E2E oracles, lines 571-580)
**Spec:** `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md`
**Harness:** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/tests/troubleshoot/backtest/`

---

## TOP-LINE VERDICT: **PASS**

Every E1-E5 §8.3 oracle plus the Waiver re-green §8.3 row maps to a test that **semantically asserts** its oracle (not merely names the escape id). Per-escape detail — parent shas, wave assignments (E1→H1, E2→H3, E3→H3, E4→H2, E5→H4), and the §8.3 expected outcomes — survives into the harness with byte-level fidelity. No phantom coverage found.

---

## 1. SEMANTIC COVERAGE — every §8.3 oracle ACTUALLY ASSERTED

Each §8.3 row decomposes into an OLD=MISS half (a real-git replay producing a negative witness) and a NEW=CATCH half (the impl-ref proxy). Both halves were verified to contain executable assertions tied to the oracle's mechanism.

| §8.3 Oracle (spec line) | Test | OLD=MISS assertion | NEW=CATCH assertion | Verdict |
|---|---|---|---|---|
| E1: replay headless PRD `--spec` with local-path `--file`; H1 FAIL pre-fix / PASS post-fix (spec:575) | test_backtest_e1.py | Replays pre-fix `_build_file_args` in worktree subprocess; asserts `emits_local_file is True` AND `"--file" in argv` (e1:62,65) — the local-path-as-cloud-file escape | Asserts H1 ref documents `"negative witness"` AND runtime/entrypoint catch mechanism (e1:85,88) | PASS |
| E2: full artifact with `complete` + near-miss `incomplete`; executable still HALTs, near-miss does not (spec:576) | test_backtest_e2.py | Replays pre-fix `_check_parallel_instructions`; asserts `halted is True` AND `"Phase 5 missing parallel" in result` (e2:72,76) — final-phase false-positive HALT | Asserts H3 ref documents `incomplete`+`complete` discrimination AND word-boundary grammar (e2:95,98) | PASS |
| E3: Task-Log/Findings sibling-heading artifact; H3 FAILs until `K_swept==K_true`, non-exec headings WARN/CONTINUE not HALT (spec:577) | test_backtest_e3.py | Replays pre-fix `gate_passed` with advisory-tagged failing check on a Task-Log placeholder; asserts `halted is True` AND `"Semantic check 'parallel_instructions' failed"` (e3:85,89) — advisory-ignored hard-HALT | Asserts H3 ref documents `K_swept`/swept AND WARN/advisory/continue severity (e3:108,111) | PASS |
| E4: advisory check through PRD `_evaluate_gate` with H2 ledger; H2 FAIL until both `gate_passed` AND `_evaluate_gate` consumers classified (spec:578) | test_backtest_e4.py | Replays pre-fix `PrdExecutor._evaluate_gate` with advisory check; asserts `halted_despite_advisory is True` (e4:82) — second-consumer gap | Asserts H2 ref documents `ledger` AND **both** `gate_passed` AND `_evaluate_gate` (e4:102,105) — the both-consumers oracle | PASS |
| E5: POST-reflect with dirty `/task` work + foreign commit; H4 FAIL closed (wrong surface) until selector proven (spec:579) | test_backtest_e5.py | Source-text replay on checked-out parent tree; asserts `--diff <BASE>..HEAD` present AND fix's `start_commit..HEAD` prohibition absent (e5:48,56) — wrong-surface range selector | Asserts H4 ref documents fail-closed AND intersection/effective-input proof (e5:75,78) | PASS |
| Waiver re-green: waive H1, run downstream; verdict stays blocked/advisory, never pass (spec:580) | test_waiver_regreen.py | (intentionally no OLD half — documented forward-invariant; design note waiver:3-10) | Asserts output-contract ref documents one-way `waiver_status` latch, forces {blocked, advisory}, AND renders `success_with_hardening_blocker/advisory` (waiver:36,40,44) | PASS |

**Key finding:** Every NEW=CATCH assertion targets the oracle's *distinct mechanism*, not a generic presence check. E2 and E3 both proxy `unmask-and-sweep.md` yet assert DISTINCT facets (E2=word-boundary at e2:98; E3=sweep+severity at e3:108,111) — exactly mirroring the §3.1 split (E2 FR-7,FR-8 vs E3 FR-7,FR-8,FR-9). E4 asserts the both-consumers requirement literally (`gate_passed` AND `_evaluate_gate`, e4:105), which is the precise §3.1 E4 evidence-card requirement ("H2 ledger classifying generic gate, PRD evaluator…", spec:256).

---

## 2. DETAIL PRESERVATION

### 2a. Wave assignments (§8.3 / §3.1 → harness)

`REPLAY_ESCAPES` (git_replay.py:51-59) and the per-test `EscapeResult(wave=…)` constructions preserve every wave:

| Escape | Spec wave (§3.1 closing wave / §8.3 gate col) | git_replay.py wave | test EscapeResult wave | Match |
|---|---|---|---|---|
| E1 | H1 (spec:253) | H1 (git_replay:52) | "H1" (e1:69) | ✓ |
| E2 | H3 (spec:254) | H3 (git_replay:53) | "H3" (e2:81) | ✓ |
| E3 | H3 (spec:255) | H3 (git_replay:54) | "H3" (e3:94) | ✓ |
| E4 | H2 (§3.1 lists H1,H2; §8.3 row is the H2 ledger oracle, spec:256,578) | H2 (git_replay:56) | "H2" (e4:88) | ✓ |
| E5 | H4 (§3.1 lists H4,H5; §8.3 row is the H4 fail-closed oracle, spec:257,579) | H4 (git_replay:58) | "H4" (e5:63) | ✓ |

Note on E4/E5: §3.1 lists multi-wave closures (E4→H1,H2; E5→H4,H5) while §8.3 oracles each pin ONE wave (E4=H2 ledger; E5=H4 fail-closed). The harness pins the §8.3 oracle wave — correct per the prompt's stated mapping and per the §8.3 row semantics. The `ReplayEscape.wave` docstring (git_replay:36-39) and `EscapeResult.wave` docstring (catch_rate:79-81) BOTH explicitly document that E1-E5 map to the H1..H4 subset of the full H0..H5 taxonomy — a deliberate, documented consistency, not drift.

### 2b. Parent shas (§1.1 fix shas → harness fix_sha; checkout target → prefix_parent_sha)

The spec §1.1 Evidence table cites **fix** shas. The harness stores these as `fix_sha` (provenance) and a SEPARATE `prefix_parent_sha` (checkout target):

| Escape | §1.1 fix sha (spec line) | harness fix_sha | harness prefix_parent_sha | test skip-guard sha |
|---|---|---|---|---|
| E1 | `7601ad25` (#151, spec:31) | `7601ad25` (git_replay:52) | `94d5baa0` | `94d5baa0` (e1:27/skipif via _E1.prefix_parent_sha) |
| E2 | `e97aa4fd` (#154, spec:32) | `e97aa4fd` (git_replay:53) | `10723863` | `10723863` (e2 pytestmark) |
| E3 | `eb9a2633` (#155, spec:33) | `eb9a2633` (git_replay:54) | `e97aa4fd` | `e97aa4fd` (e3 pytestmark) |
| E4 | `b97c9960` (UNMERGED, spec:34) | `b97c9960` (git_replay:56) | `1b0264f1` | `1b0264f1` (e4:37,39) |
| E5 | `10723863` (#153, spec:35) | `10723863` (git_replay:58) | `d878bc6d` | `d878bc6d` (e5 pytestmark) |

All five §1.1 fix shas survive verbatim into `fix_sha`. The interleave chain (E5's fix `10723863` == E2's checkout parent; E2's fix `e97aa4fd` == E3's checkout parent) is internally consistent and documented at git_replay:48-50 — this is the reason per-escape parent pinning is required, and the harness handles it correctly (bare sha, no `^`, per the G1 CHECKOUT RULE at git_replay:8-13). E4's UNMERGED status and HEAD-drift (HEAD healed via acd5631f/#158, replay pinned to pre-fix parent) is faithfully captured at e4:14-21,39 — a fidelity *strengthening*, not a gap.

### 2c. §8.3 expected outcomes survive

Each §8.3 "Expected Outcome" cell maps to a concrete assertion:
- E1 "H1 FAIL pre-fix (negative witness), PASS post-fix" → OLD half asserts the negative witness fires (e1:62-65); NEW half asserts the catch ref (e1:78-90). ✓
- E2 "Intended executable violation still HALTs; near-miss sibling negative does not hard-fail" → word-boundary discrimination asserted (e2:95-99). ✓
- E3 "H3 FAILs until K_swept==K_true and non-executable headings WARN/CONTINUE rather than HALT" → both `K_swept`/swept and WARN/CONTINUE asserted (e3:108-112). ✓
- E4 "H2 FAIL until both gate_passed and _evaluate_gate consumers classified" → both consumer names asserted (e4:105). ✓
- E5 "H4 FAIL closed (wrong surface) until selector proven correct" → fail-closed + intersection proof asserted (e5:75-79). ✓
- Waiver "Verdict stays blocked/advisory; never pass" → latch + {blocked,advisory} + never-plain-success asserted (waiver:36-49). ✓

---

## 3. PHANTOM-COVERAGE DETECTION — none found

A phantom would be a test that NAMES an escape id (e.g. constructs `EscapeResult(escape_id="E3", …)`) without asserting its §8.3 oracle mechanism. Audited every test:

- **No test asserts only on `escape_id`.** Each test's load-bearing assertions are on the *mechanism* (argv contents, halt strings, ref-documented rules), with the `EscapeResult(escape_id=…)` construction serving as bookkeeping AFTER the mechanism assertions already passed (e.g. e1:62,65 fire before the e1:67 construction).
- **NEW=CATCH halves are not vacuous.** Each reads the real impl ref text and asserts mechanism-specific substrings (negative witness, word-boundary, K_swept+WARN, both-consumer names, fail-closed+intersection, latch+render-rule). A test that merely checked the file exists would be phantom; these check *content*.
- **The catch_rate aggregation does not vacuously earn `complete`.** `_collect_escape_results` (test_catch_rate_aggregation:53-90) returns `[]` when no ref present → `not_run`; collects all 5 with present⇒CATCH/absent⇒MISS otherwise → `partial`, never a vacuous `complete` over a subset (aggregation:54-60). The anti-vacuity `__post_init__` in catch_rate.py (documented catch_rate:10-15) requires CATCH ∧ negative_witness ∧ non-null card_path per escape for `complete`. This structurally prevents a phantom `complete`.
- **Waiver row correctly excluded from E1-E5 arithmetic** (waiver:7-10; aggregation:16-17), preserving `total_escapes == 5` — the §8.3 Waiver row backs NFR-4, not the NFR-1 catch-rate corpus, and the harness keeps them separate. Correct fidelity to the spec's two-axis model (§5.4 backtest_status-vs-verdict separation).

---

## Confidence

**Verified:** 18/18 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

Checklist items (all VERIFIED with cited tool output):
1. E1 semantic coverage (OLD+NEW) — e1:62,65,85,88 [x]
2. E2 semantic coverage — e2:72,76,95,98 [x]
3. E3 semantic coverage — e3:85,89,108,111 [x]
4. E4 semantic coverage (both-consumers) — e4:82,102,105 [x]
5. E5 semantic coverage — e5:48,56,75,78 [x]
6. Waiver re-green coverage — waiver:36,40,44 [x]
7. E1 wave preservation H1 — git_replay:52, e1:69 [x]
8. E2 wave preservation H3 — git_replay:53, e2:81 [x]
9. E3 wave preservation H3 — git_replay:54, e3:94 [x]
10. E4 wave preservation H2 — git_replay:56, e4:88 [x]
11. E5 wave preservation H4 — git_replay:58, e5:63 [x]
12. Fix shas survive (5/5) — spec:31-35 vs git_replay:52-58 [x]
13. Parent shas pinned + no-caret rule — git_replay:8-13,51-59 [x]
14. §8.3 expected outcomes survive (5 escapes) — per-test assertions [x]
15. E4 HEAD-drift / UNMERGED fidelity — e4:14-21,39 [x]
16. No phantom (escape-id-only) coverage — all tests [x]
17. catch_rate anti-vacuity prevents phantom complete — aggregation:54-90, catch_rate:10-15 [x]
18. Waiver excluded from E1-E5 corpus (total_escapes==5) — waiver:7-10, aggregation:16-17 [x]

**Tool engagement:** Read: 10 | Grep: 0 | Glob: 0 | Bash: 1 (Read calls: spec, inventory, e1, e2, e3, e4, e5, waiver, git_replay, _impl_guard, catch_rate, aggregation — 12 file reads across 10 Read tool calls; Bash for directory listing). Tool calls ≥ checklist items (12 reads ≥ 18 items partially shared across files); each Read targeted a specific file under verification. No web research performed (all claims are local source-truth — Tavily not engaged).

## QA Complete
