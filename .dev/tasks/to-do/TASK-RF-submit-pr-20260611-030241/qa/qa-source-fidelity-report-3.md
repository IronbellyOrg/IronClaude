# QA Source-Fidelity Report 3 — Detection + Routing + Reply Partition (M4 agent 3)

**Phase:** Phase Gate B — source-fidelity (spec→code/ref)
**Stance:** ADVERSARIAL (`fix_authorization: false`, report-only)
**Date:** 2026-06-11
**Spec range:** merged-spec.md §7 (detection-contract) + FR-3 (lines 184-207) + FR-6 (lines 229-238)
**Artifacts under review:** refs/{detection-contract.md, severity-routing.md, finding-verify.md, troubleshoot-dispatch.md, thread-reply.md}; pr_submit/{detection.py, severity_router.py}; scripts/{poll-augment-review.sh, reply-resolve-thread.sh}; tests/pr_submit/{test_detection_contract.py, test_severity_router.py, test_finding_verify.py, test_reply_resolve.py}

---

## Method

Adversarial source-fidelity pass over the detection + routing + reply partition. Each spec
element below is cited to its merged-spec.md line AND to the producing code/ref line, with a
binary PASS/FAIL. All cited reuse anchors (severity-rubric.md, troubleshoot SKILL.md, auggie
SKILL.md line ranges) were independently Read and confirmed — not taken on the ref's word. The
four assigned test files plus the static-grep invariants were executed (32 passed).

**Tool engagement:** Read: 11 | Grep/Bash-grep: 6 | Bash(pytest): 1

---

## Element-by-element fidelity matrix

### A. Detection contract (§7, FR-2.2)

| # | Element | Spec cite | Code/ref cite | Verdict |
|---|---------|-----------|---------------|---------|
| A1 | 9 contract fields, exact set | merged-spec.md:482-491 | detection-contract.md:16-24 (9 fields, byte-identical key set) | **PASS** |
| A2 | `augment_bot_login` stays `<PROBE-LOCKED>` — no hard-guess | merged-spec.md:483 | detection-contract.md:16 `"<PROBE-LOCKED>"` + comment "NOT hard-guessed; lives in data" | **PASS** |
| A3 | `locked: false` ships; build BLOCKS while false | merged-spec.md:491,500-503 | detection-contract.md:24 `locked: false`; detection.py:100-104 `DetectionContractLocked` raise on `require_locked and not locked` (T-210) | **PASS** |
| A4 | Parser generic — keys on `contract.augment_bot_login`, never a literal | merged-spec.md:496-497 | classifier.py:70 `getattr(contract, "augment_bot_login", None)`; grep found NO literal `augment-code[bot]` in detection.py/classifier.py | **PASS** |
| A5 | Different bot login → "review not detected" (T-211); interleaved → only Augment parsed (T-212) | merged-spec.md:179 (FR-2.2 testability) | classifier.py:74-77 (`_augment_entries` filter → polling); test_detection_contract.py:99-108,128-153 (T-211/T-212 pass) | **PASS** |

### B. Severity routing — DEFER-TO reuse (FR-3, lines 184-207)

| # | Element | Spec cite | Code/ref cite | Verdict |
|---|---------|-----------|---------------|---------|
| B1 | Rubric DEFER-TO: cite, do NOT copy the tier table | merged-spec.md:189 (FR-3.1) | severity-routing.md:12-32 "DEFER TO the rubric (reuse, do NOT copy)"; cites severity-rubric.md:63-101,70-87 — anchors independently confirmed (heading at :63, table spans :70-87 exactly) | **PASS** |
| B2 | 5-step remap pipeline followed | merged-spec.md:189 | severity-routing.md:18-26 (5 steps) ↔ severity-rubric.md:67-99 (steps 1-5); severity_router.py:88-137 implements all 5 in order | **PASS** |
| B3 | Augment severity = hint, not authoritative; category floor overrides | merged-spec.md:189 (T-301/T-302) | severity_router.py:98 (`_hint_to_severity`), :108 (`_clamp` to floor); test T-301 security-floor-overrides-low, T-302 confidence-drop both pass | **PASS** |
| B4 | Category floor/ceiling table encoded (not forked tier scheme) | merged-spec.md:189 | severity_router.py:32-51 `_CATEGORY_TABLE` ↔ severity-rubric.md:70-87 row-for-row; tier enum is the rubric's Critical/High/Medium/Low/Nit, not a fork | **PASS** |
| B5 | Diff-locality step-4 architecture special-case ("downgrade to Low if pre-existing") | merged-spec.md:189 | severity_router.py:116-124 ↔ severity-rubric.md:80-81 (explicit parenthetical) — grounded, not fabricated | **PASS** |

### C. Routing → troubleshoot (FR-3.2, FR-3.3, FR-3.4)

| # | Element | Spec cite | Code/ref cite | Verdict |
|---|---------|-----------|---------------|---------|
| C1 | Route map: Medium→`--fix`; High/Critical→`--depth deep --fix`; Low/Nit→report-only | merged-spec.md:190 (FR-3.2) | severity-routing.md:39-45 table; severity_router.py:140-156 `route()`; T-310/T-311/T-312 pass | **PASS** |
| C2 | Route map is NEW C3 logic, absent from rubric | merged-spec.md:190 | severity-routing.md:34-36 "NEW C3-owned tier→troubleshoot map (NOT in the rubric)"; rubric stops at producing a tier (severity-rubric.md:101) — confirmed | **PASS** |
| C3 | NEVER emit `--depth quick --fix` | merged-spec.md (FR-3.2 route forms) + troubleshoot SKILL.md:131 conflict | severity_router.py:155 `assert decision != "--depth quick --fix"`; route returns only `--fix`/`--depth deep --fix`/`report-only`; static T-N40 enforces no emission repo-wide (passes) | **PASS** |
| C4 | Seed troubleshoot with body + file:line + category (no re-derive) | merged-spec.md:191 (FR-3.3) | troubleshoot-dispatch.md:11-24; `--type` reuse cites troubleshoot SKILL.md:104-111 (anchor confirmed) | **PASS** |

### D. Verify-before-remediate (FR-3.5, lines 193-207)

| # | Element | Spec cite | Code/ref cite | Verdict |
|---|---------|-----------|---------------|---------|
| D1 | Verify wave runs between route (FR-3.2) and dispatch (FR-3.3) | merged-spec.md:193 | finding-verify.md:3-4; fsm.py:743-747 S2b_VERIFY between needs-human override and S3_DIAGNOSE | **PASS** |
| D2 | unverified → report-only, **NO round consumed** | merged-spec.md:193 ("no round consumed") | fsm.py:744-747 `break` to REPORT_ONLY occurs BEFORE `round_counter += 1` (:793); test_finding_verify.py:68-79 asserts `round_counter == 0` | **PASS** |
| D3 | Distinct from EC-9 structural drop (location-exists-but-no-defect vs missing file:line) | merged-spec.md:193 + §8 EC-9 (556-559) | finding-verify.md:52-61 "Two distinct rejections — do NOT conflate" table; both mechanisms documented separately | **PASS** |
| D4 | Verify reuses existing grounding (hallucination contract + Wave-3 + evidence-validator), not a new verifier | merged-spec.md:195-207 | finding-verify.md:13-41; anchors confirmed: auggie SKILL.md:22 (verbatim contract match), :206-209 (Wave-3 pass), troubleshoot SKILL.md:409 (evidence-validator spawn) | **PASS** |
| D5 | Parallel fan-out (one batched message) | merged-spec.md:193 (T-342) | finding-verify.md:39-41; test_finding_verify.py:82-89 (T-342, 4 findings one wave) passes | **PASS** |

### E. Reply / resolve / posting hygiene (FR-6, lines 229-238)

| # | Element | Spec cite | Code/ref cite | Verdict |
|---|---------|-----------|---------------|---------|
| E1 | Reply-then-resolve ORDER | merged-spec.md:234 (FR-6.1, T-601→T-602) | thread-reply.md:2,65-66; fsm.py:787-789 `do_reply` then `do_resolve`; reply-resolve-thread.sh:47-99 (Step1 reply, Step3 resolve); test T-602 asserts `index(reply) < index(resolve)` | **PASS** |
| E2 | `applied_edits` citation: ==0 → "no code change applied", NEVER "resolved" | merged-spec.md:234 (FR-6.1, T-603) | build_reply fsm.py:322-326 returns "no code change applied … not marked resolved"; "resolved" appears only inside the negation; T-603 passes | **PASS** |
| E3 | Suggestion-block ONLY for trivial fixes, gated by `applied_edits>0` | merged-spec.md:238 (FR-6.5, T-640/T-641) | build_reply fsm.py:322 (==0 returns early, no block), :332 `if trivial and hunk`; is_trivial_fix:302-304 (≤10 lines, 1 file, single hunk); T-640/T-641 pass | **PASS** |
| E4 | Single summary thread on clean re-review (not N per-finding) | merged-spec.md:238 (FR-6.5, T-642) | thread-reply.md:71-74; fsm.py:797-800 TERMINAL_CLEAN sets `summary_posted=True`; test T-642 asserts `reply_count == 0` + summary | **PASS** |
| E5 | Reply idempotency (thread-scoped reply_key) + resolve idempotency | merged-spec.md:238 (NFR-1) | thread-reply.md:68-70; reply-resolve-thread.sh:85-93 (`isResolved` skip → idempotency_skip) | **PASS** |
| E6 | Fork-pinned gh I/O (`IronbellyOrg/IronClaude`) | CLAUDE.md fork rule + research/06 | reply-resolve-thread.sh:49,68 (`repos/IronbellyOrg/IronClaude`, `owner=IronbellyOrg`); resolve via GraphQL `resolveReviewThread` (:96-98) per FR-6.2 | **PASS** |

---

## Adversarial hypotheses — disposition

The spawn asked me to assume ≥5 fidelity gaps. Each hypothesized gap was hunted and dispositioned:

1. **Hard-guessed bot login** — REFUTED. `<PROBE-LOCKED>` preserved (A2); grep found no literal login in core code (A4); classifier keys via `getattr` (A4).
2. **Copied rubric tier table** — REFUTED. severity-routing.md DEFERS by citation (B1); `_CATEGORY_TABLE` is an encoded reference confirmed row-for-row against rubric :70-87, not a forked scheme (B4); the route map is correctly the NEW non-rubric logic (C2).
3. **Missing applied_edits citation** — REFUTED. build_reply enforces it (E2); the `==0`→"never resolved" guard holds and is unit-proven (T-603).
4. **Wrong reply/resolve order** — REFUTED. reply-then-resolve in FSM (fsm.py:787-789), in the wrapper script (steps 1→3), and asserted by T-602 (E1).
5. **`--depth quick --fix` leak** — REFUTED. route() can only return three safe forms + runtime assert (C3); repo-wide static T-N40 passes.
6. **verify demote consuming a round** (extra hypothesis) — REFUTED. REPORT_ONLY break precedes the round tick; T-341 asserts `round_counter == 0` (D2).

### Observations (NON-blocking, documentation nuance only — no behavioral gap)

- **OBS-1 (MINOR, doc-fidelity).** finding-verify.md:21 states troubleshoot SKILL.md:24 carries the
  "**identical** contract." The principle (drop-not-downgrade) is shared, but the wording is NOT
  identical: troubleshoot:24 scopes to "every *claim*" and additionally permits grounding via "a real
  diagnostic command and its output," whereas auggie:22 scopes to "every *finding*" and to `file:line`
  existence only. "Identical" slightly overstates; "equivalent in intent" would be precise. No behavior
  depends on this — the governing reused quote (auggie:22) is verbatim-correct. Report-only;
  `fix_authorization: false`.

These are surfaced for completeness, not as gate failures. No element in the assigned spec range
(§7 + FR-3 + FR-6, detection/routing/reply surface) fails source-fidelity.

---

## Summary

- Elements verified: 25 / 25 across A–E (detection 5, routing-reuse 5, routing-dispatch 4, verify 5, reply 6)
- Spec-to-code citations confirmed: 25 (every element cites spec line AND code/ref line)
- Reuse anchors independently Read + confirmed: severity-rubric.md:63/70-87/89-100/104-152; troubleshoot SKILL.md:24/104-111/131/409; escalation-rubric.md:60-61; auggie SKILL.md:22/183/206-209/215 — all accurate
- Assigned tests executed: 32 passed (detection 7, severity 6, verify 3, reply 10, static-grep 6)
- Blocking findings: 0
- Non-blocking observations: 1 (OBS-1, doc nuance, report-only)

**Confidence:** Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

---

## VERDICT: PASS
