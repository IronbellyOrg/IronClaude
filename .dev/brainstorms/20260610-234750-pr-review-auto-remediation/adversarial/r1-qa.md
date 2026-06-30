---
contract_version: "1.0"
artifact: adversarial-round-statement
round: 1
variant: variant-3-haiku-qa
author_role: ADVOCATE (haiku:qa)
topic: "PR Review Auto-Remediation Monitor (V1.0)"
generated: 2026-06-11
---

# Round 1 — Variant C (haiku:qa) Adversarial Statement

## 1. Position Summary

Variant C takes the position that a remediation monitor is only as safe as its weakest test gap. The spec encodes 90 explicit tests, 10-row fence-post matrices, 7 formal invariants, and 16 named edge cases — every requirement carries a testability note so that nothing ships unverified. The strongest safety claims come from behavioral tests (tool-call-count assertions for autonomy gates) and the canonical off-by-one test (T-626), not from prose assertions.

## 2. Steelman — Variant A (opus:architect)

Variant A's strongest contribution is the **seam discipline** (§2.1, §7): a hard boundary between the unknown (Augment's emission shape) and the deterministic core (FSM, router, loop-guard). The single config-driven `DetectionContract` with `locked:false` as a **mechanically-enforced build gate** (AC-8, NFR-4) is genuinely superior to Variant C's "skill HALTs if config absent" approach — build-time prevention beats runtime failure. The **capability-ceiling FSM** (§3.2: one machine, three gate-checks, ordinal as single integer) eliminates the 2^3 = 8 nested-if bug surface ( §3.3), which is architecturally elegant and directly testable as transition-table row assertions (AC-2..AC-6). The **purity enforcement** (AC-9: static grep that no `gh`/`git` token appears in the deterministic core, R5 seam-leakage risk) is a CI-level safety net that Variant C entirely lacks. These are not cosmetic — they prevent entire classes of future regressions.

## 3. Steelman — Variant B (sonnet-backend)

Variant B's strongest contribution is the **durability substrate** (§"Idempotency & Run-log Schema"): 29 typed JSONL event types, a `state.snapshot.json` cache, five explicit idempotency sets (`processed_review_ids`, `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas`), and a conflict-resolution rule (JSONL authoritative over snapshot). The **12 failure modes** (FM-1..FM-12) with explicit detection/action/recovery — especially crash-after-push-before-reply (FM-6) and crash-after-reply-before-resolve (FM-7) — cover session-loss scenarios that Variant C documents as a "limitation" (T-230) without recovery. The **`--resume <run-log-path>`** first-class CLI flag (§Command contract) and the **wall-clock timeout** ("since entering S3, not cumulative", l.132) are operationally superior to Variant C's underspecified timeout basis. The explicit "is not" list for round_index (l.171-178: not polls, not comments, not pushes, not findings, not reviews-since-last-poll, not reset-after-push) prevents the exact misinterpretations that cause off-by-one bugs.

## 4. Strengths Claimed (Variant C) with Evidence

**S1 — Exhaustive test matrix with per-requirement traceability.** Every FR-1.1..FR-7.1 and NFR-1..NFR-5 maps to concrete test IDs in §4.2's coverage matrix (146 lines). No requirement ships without a named test.

**S2 — Canonical off-by-one test (T-626).** §6.3 provides the most diagnostic assertion messages in any variant: `Expected 2 pushes, got {result.push_count}` with explicit `third_fix_not_applied` check (l.378-391). The test is `@pytest.mark.p0` (§13.2), meaning CI fails fast on every PR if loop-guard regresses.

**S3 — Fence-post matrix completeness.** 10 rows (T-620..T-629) covering: clean-immediate, 1-round, 2-round, 3-round, 5-round, max-rounds-at-cap, off-by-one-at-max-2, max-1, max-0 diagnostic, and validation-fail-retry-within-round. Each row specifies setup, rounds-executed, and expected outcome (§6.2, l.349-360).

**S4 — Autonomy gates proven by tool-call counts, not prose.** §7's Python test code asserts `result.tool_calls_by_name("Write") == 0` for L1 (l.426-427), `result.push_count == 0` for L2 (l.453), and `result.halted == True` for L3+needs_human_decision (l.481). These are behavioral proofs that fail in CI, not acceptance criteria that depend on manual review.

**S5 — Edge-case catalog (EC-1..EC-16).** Each of 16 edge cases has a dedicated fixture, scenario, expected behavior, and assertion (§5). Critical ones: review-arrives-during-fix (EC-5), timeout-mid-remediation (EC-6), `--max-rounds=0` diagnostic mode (EC-8), and `gh` not installed (EC-15).

**S6 — "Validation failure does NOT consume round" as a tested design decision.** INV-6 (§6.1, l.344) + T-520 (§10.3, l.622-628) explicitly encode this with fixture asserting `round_counter == 1` despite 2 validation attempts. QD-1 (l.713-716) explains the rationale.

**S7 — Severity rubric tested independently.** QD-6 (l.737-742): "14 category-to-severity mappings from the rubric table, plus all three confidence adjustments and both diff-locality adjustments" as a pure unit test with no orchestration dependency.

## 5. Weaknesses Identified (Variant C) with Evidence

**W1 — No config-constant schema; runtime HALT instead of build gate.** Variant C has no equivalent of A's `detection-contract.md` with `locked:false` build gate (A §4.1, §7). Instead, "config constant absent → skill HALTs with 'probe first' error" (T-210, EC-11, FR-2.2, l.68-69). This is a runtime guard — a build can succeed and deploy with a missing probe, failing only at invocation. A's approach blocks the build; C's approach blocks the user.

**W2 — Run-log schema is underspecified.** NFR-3 says "per-run log `.dev/.../monitor-run-<PR>.jsonl`" with testability notes T-N20..T-N22 (l.121: file exists, events have timestamp/round/state, valid JSONL). But there is no event-envelope schema (B has 29 typed events, §"JSONL event envelope", l.314-334), no `state.snapshot.json` recovery cache, no idempotency-set definitions beyond T-N01's "replay same findings twice → assert reply once." Variant C cannot recover from crash-mid-push the way B's FM-6/FM-7 can.

**W3 — No formal state machine.** Variant C uses 7 invariants (INV-1..INV-7, §6.1) and 3 detection states (D0/D1/D2, §8) but no state-transition diagram. There is no equivalent of A's 7-state FSM (§3.1) or B's 14 canonical states (S0..S14, l.76-91). Without a formal state model, the test assertions rely on the implementer's interpretation of "state = polling" vs "state = findings" — the exact ambiguity A's seam was designed to prevent.

**W4 — Session-close recovery is a documented limitation, not a design.** T-230 (l.70): "close session mid-poll → monitor drops, run-log records `session_closed` event. No code assertion beyond logging (documented limitation)." Variant B's `--resume <run-log-path>` is a first-class recovery path (FM-1, l.626). Variant C accepts session-loss as permanent.

**W5 — Timeout clock basis is vague.** "overall timeout default ~30 min, configurable" (FR-2.3, l.67) and "`--timeout` configurable, fires at deadline" (diff-analysis X-007). Variant B explicitly specifies "wall-clock elapsed time since entering S3_WAITING_FOR_REVIEW for the current review wait, not cumulative process lifetime" (l.132). Variant C's ambiguity means an implementer could use cumulative time, causing premature timeout on multi-round runs.

**W6 — Finding dedup conflates comment_id with file:line hash.** QD-5 (l.732-735) says "Reply … posted once per thread, not once per finding" keyed on comment_id. But EC-4 (l.250) says "Deduplicated by `file:line` + finding body hash." These are two different dedup keys for two different purposes (reply dedup vs finding dedup), and the spec doesn't clarify which governs the troubleshoot-invocation boundary.

## 6. Concessions

- **Detection contract:** Variant A's `locked:false` build gate (AC-8) is mechanically superior to C's runtime HALT. A build-time block prevents the scenario where CI passes, the skill deploys, and a user hits a "probe first" error at runtime. I concede A wins on C-001.
- **Run-log durability:** Variant B's 29-event schema + snapshot cache + 5 idempotency sets + conflict-resolution rule (B §"Idempotency & Run-log Schema") is significantly more rigorous than C's "valid JSONL" assertion. For crash-recovery, B's approach is necessary. I concede B wins on C-005.
- **Structural differences S-002/S-004/S-007:** Section count (S-002), FR numbering convention (S-004), and path convention (S-007) are cosmetic and non-load-bearing. I concede all three.
- **Timeout clock:** Variant B's wall-clock-per-wait definition (l.132) is clearer than C's per-deadline approach. I concede B has the better spec on X-007, though C's "let in-flight fix finish past deadline" (EC-6) is a valuable safety addition B lacks.

## 7. Contested Point Positions

### X-001 -- `--max-rounds=0` semantics
**Winner: C.** A leaves 0 undefined (diff-analysis: "0 not addressed", l.61). B rejects it for monitor 2/3 (B l.224: "Values below 1 are invalid when --monitor 2 or --monitor 3"). C treats it as a valid diagnostic mode (C QD-2, l.718-720: "monitor and report but never remediate," tested T-628/T-E08). A diagnostic mode is a genuine user need — letting operators observe Augment findings without any remediation risk. C's behavior (equivalent to L1 regardless of --monitor) is safe and tested. B's rejection is unnecessarily restrictive.

### X-002 -- Does validation failure consume a round?
**Winner: C.** A leaves it implicit (A FSM: "retry≤budget / HALT", round impact unstated). B couples retry to round budget (B l.481: "one additional fix attempt may occur only if round_index < max_rounds"). C explicitly separates validation retries from round progression (C INV-6, l.344: "validation failure does NOT increment round_counter"; T-520 tests this). A validation failure is a self-inflicted wound, not a new review cycle — consuming round budget on it would artificially reduce the number of real remediation attempts. C's design is correct and tested.

### X-003 -- Reply dedup keying
**Winner: C.** A dedups on comment_id in RunLog (A NFR-1, l.313). B uses two keys: `replied_comment_ids` for replies AND `finding_id="aug-<comment_id>-<stable_hash>"` for finding dedup (B l.260, l.419-425) — more rigorous but more complex. C uses comment_id for reply dedup (C QD-5, l.732-735: "posted once per thread, not once per finding") and file:line+hash for finding dedup (C EC-4, l.250). The two-key approach in B is more correct (prevents both double-reply and double-troubleshoot), but C's comment_id-first approach is simpler and sufficient for the reply-idempotency gate. C's weakness is the conflation of the two purposes (see W6). **Qualified winner: B for rigor, C for simplicity.** The spec needs both dedup keys explicitly separated — I concede B's two-set approach is the correct design, but C's principle (thread-level reply, not per-finding) is the right behavioral invariant.

### X-004 -- Detection-contract: enforced build-gate vs advisory vs runtime-HALT
**Winner: A.** A's `locked:false` → "skill refuses to arm … build BLOCKED" (A AC-8, NFR-4, l.320) is mechanically enforced at build/parse time. B's "empirically validated before release" (B l.240) is advisory/release-time — no primitive. C's "config constant absent → skill HALTs" (C T-210) is a runtime guard. Build-time prevention > runtime HALT > advisory. A's approach ensures the skill cannot even be installed without a probe, which is the strongest safety position.

### X-005 -- Round-counter start/indexing
**Winner: C (with reservations).** A starts at 0: "initial review is round 0" (A L8.1). B starts at 1: "first remediation is round 1" (B l.217). C starts at 0 (C INV-1) but T-629 asserts `round_sequence == [0, 1]` and `round_counter == 2` for two executed rounds (C l.408). C's mixed representation (0-indexed sequence, count-based counter) is the most precise for testing: the sequence proves which rounds executed, the counter proves how many. The potential confusion (round_counter==2 means 2 rounds, not round-2) is resolved by T-626's explicit assertion `assert result.round_counter == 2, f"Expected 2, got {result.round_counter}"` (C l.378). A's "round 0" is ambiguous — does "round 0" mean the zeroth round or zero rounds? C's dual representation is testable and unambiguous.

### X-006 -- Where needs_human_decision is determined
**Winner: Draw.** A evaluates it post-routing on RoutedFinding at FIXING entry (A §3.1 FSM: `needs_human_decision → HALT_HUMAN`). B classifies it at detection (B l.293: "ambiguous API contract, security posture, migration behavior, or user-visible behavior → mark needs_human_decision = true"). C asserts it at the gate level in tests (C T-430, EC-7). All three reach the same behavioral outcome — HALT regardless of autonomy level. The timing difference (classify vs route vs gate) is an implementation detail. C's test-driven approach proves the invariant behaviorally (tool-call assertions), which is sufficient.

### X-007 -- Timeout clock basis
**Winner: B.** A says "single 30-min wait" (A FR-A3). B says "wall-clock elapsed time since entering S3_WAITING_FOR_REVIEW for the current review wait, not cumulative process lifetime" (B l.132). C says "`--timeout` configurable, fires at deadline" (diff-analysis X-007) with EC-6 letting in-flight fix finish past deadline (C l.263-265). B's per-wait re-clock is the clearest definition and prevents cumulative-time bugs across multi-round runs. C's "let current fix finish past deadline" is a valuable safety addition but doesn't compensate for the ambiguous clock basis.

### X-008 -- Ungroundable/missing file:line finding handling
**Winner: C.** A doesn't specify (diff-analysis: "parser captures path,line; no drop rule"). B says "may still be reported, but may not be auto-fixed at level 3 unless /sc:troubleshoot can ground them" (B l.285) — keep + conditional gate. C says "finding dropped per hallucination contract, reported as 'ungroundable' in run-log" (C EC-9, l.285-286). Dropping ungroundable findings is the safest default: an auto-fix on an ungrounded finding is a hallucination-driven file mutation, which is worse than no fix. C's explicit drop + run-log reporting prevents the "fix" of a non-existent file or wrong line.

## 8. Shared-Assumption Verdicts

| ID | Verdict | Evidence (one line) |
|---|---|---|
| **A-001** | **QUALIFY** | All variants poll `gh pr view --json reviews,comments` (A FR-A3, B l.107-117, C T-201-203) — but Augment could emit via check-runs or non-gh surfaces; R1 probe must enumerate all surfaces before the poller is complete. |
| **A-002** | **QUALIFY** | All variants seed troubleshoot with `{body, path, line, severity, evidence}` (A §4.6, B FR-5, C T-320) — but `/sc:troubleshoot`'s actual CLI interface for pre-loaded findings is not documented in any variant; this is a cross-skill contract that needs explicit verification. |
| **A-003** | **REJECT** | The Monitor tool spec auto-stops high-volume monitors and times out long ones (memory: session-close = documented limitation, C T-230). A 30-min poll at ≥30s interval may produce too few events and be evicted — none of the three variants address low-volume eviction, only high-volume auto-stop. |
| **A-004** | **QUALIFY** | A asserts SHA self-attribution (A L8.3, l.354-355) which is the strongest mechanism. B and C assert causality but don't prove the attribution mechanism (diff-analysis AD-4, l.93). SHA-match is necessary but not sufficient — Augment could re-review on a different commit. |
| **A-005** | **ACCEPT** | All three variants re-grade Augment's severity hint through the reused rubric (A FR-A4, B l.282, C T-301/QD-6) and C independently tests all 14 category mappings (C QD-6, l.737-742). The rubric exists and the remap is testable. |
| **A-006** | **QUALIFY** | A asserts the exact GraphQL mutation `resolveReviewThread(threadId:<node-id>)` (A FR-A8, l.299-300). B hedges "if GitHub's exact reply or resolve endpoint differs … isolate in helper" (B FR-8.5, l.567-568). The REST reply endpoint is documented; the GraphQL resolve thread mutation for review comments (vs PR comments) needs empirical verification. |
| **A-007** | **REJECT** | All three gate push on targeted tests + lint + format (A VG-1..4, B §"Validation Gates", C T-501..511) — but a test-passing fix that changes product behavior (the R4 blast-radius risk, A l.417, C l.662) gets auto-pushed. Validation is necessary but not sufficient for "safe to push." |
| **A-008** | **QUALIFY** | All variants key idempotency on comment/thread IDs (A thread_id at parse, B 5 idempotency sets, C QD-5). But whether Augment re-posts findings as new comment_ids on re-review is unprobed — if it does, comment_id dedup fails and the same fix is replied twice. The R1 probe must verify comment_id stability across re-reviews. |
