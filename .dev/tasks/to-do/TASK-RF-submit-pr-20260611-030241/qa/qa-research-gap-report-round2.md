# QA Report — Research Gate (Round 2 Re-Check)

**Topic:** PR review auto-remediation — run-log JSONL substrate, INV-007 write-ahead push triad, FSM/gate, validation gate
**Date:** 2026-06-11
**Phase:** research-gate (gap re-check after gap-fill)
**Fix cycle:** 2
**Lens:** gap-detection
**Fix authorization:** false (report only)

---

## Adversarial stance

Prior round FAILED with 2 CRITICAL + 1 IMPORTANT + 1 MINOR gap. A gap-fill researcher
added file `08-runlog-recovery-fsm-validation.md`. This pass verifies each gap is
ACTUALLY closed with actionable, spec-cited content mapped to module + test, NOT
rubber-stamped. Verification is against the spec, not the research file's self-claims.

---

## Verification Log

File 08 read in full (426 lines). Each gap re-checked against the spec independently
(not against the file's self-claims). Spot-checks performed by reading the actual spec
ranges and counting/comparing token-by-token.

---

## Overall Verdict: PASS

All four prior gaps are genuinely closed with actionable, spec-cited content mapped to
a concrete module + test file. The builder can now author per-item checklist entries for
`run_log.py`, `recovery.py`, `fsm.py`/`loop_guard.py`, and the validation gate without
guessing. No residual gaps. File 08 additionally surfaces three real spec-internal
findings (event-count, VG-3≠VG-4, fix_key) that strengthen the build.

---

## Gap-by-Gap Verification

### GAP-1 (CRITICAL, §11 Run-Log JSONL substrate) — CLOSED

| Spec element | File 08 claim | Spec source | Match? |
|---|---|---|---|
| Authority rule (JSONL authoritative; snapshot=cache; rebuild from JSONL NFR-6) | §1.1 | merged-spec.md:701-705 | EXACT |
| Write-ahead fsync-before-side-effect | §1.1 | :704-705 | EXACT |
| 5 file locations + default output-dir + `--resume` reuse | §1.2 table | :707-716 | EXACT (all 5 paths + default `/config/.../pr-monitor/pr-<N>-<TS>/`) |
| Event envelope (11 fields incl. nested `pr{repo,number,url,base,head}`) | §1.3 | :718-721 | EXACT |
| Event-type list | §1.3a verbatim block | :723-731 | **VERIFIED — counted independently = 32 types** |
| 5 idempotency sets + keys | §1.4 table | :735-744 | EXACT (all 5; `fix_key=sha256(path+line+finding_body)` per :740-741) |
| Module + tests | `run_log.py`(+`models.py`), `test_run_log.py` T-N20/21/22, `test_idempotency.py` T-N01/N02/T-FRESH-COMMENT-NO-DOUBLE-FIX | :733, :801 | MAPPED, actionable |

**Independent event-type count:** I enumerated the verbatim block at spec:724-731 and
counted **32** distinct types. File 08 (§1.3a) claims 32 and correctly flags the prompt's
"~30" as an undercount. It further identifies a **33rd** type, `push_aborted_or_not_landed`,
required by §12.1 (verified at spec:771) but absent from the §11.3 list. This is a genuine
spec-internal inconsistency, correctly surfaced — not an invention. STRONG close.

### GAP-2 (CRITICAL, §12.1 INV-007 + crash-window + FM-1..12) — CLOSED

| Spec element | File 08 claim | Spec source | Match? |
|---|---|---|---|
| INV-007 push triad ordering (push_decision→target_sha→push_initiated→git push→push_completed→S5) | §2.1 numbered list | :754-763 | EXACT, fsync points correct |
| fsync BEFORE `git push` on push_initiated | §2.1 step 3 | :758-759 | EXACT |
| PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` | §2.1 verbatim | :762-763 | EXACT |
| SHA attribution gates round_counter tick | §2.1 | :761-762 | EXACT |
| Crash-window 3-way branch (A landed / B not-landed / C ambiguous) | §2.2 table | :765-773 | EXACT (A→push_completed{recovered}; B→push_aborted_or_not_landed, re-push SAME cycle no re-fix; C→HALT_HUMAN) |
| T-CRASH-WINDOW-NO-DOUBLE-PUSH (`push_count==2`, S5, recovered==True) | §2.2 verbatim | :775-776 | EXACT |
| FM-1..FM-12 catalog | §2.3 table | :778-792 | EXACT (all 12 rows trigger/action/recovery verbatim) |
| Module + test | `recovery.py`(+run_log rebuild, fsm `--resume`/S5), `test_crash_recovery.py` | derived from R4 | MAPPED, actionable |

Cross-links (FM-6/7 → idempotency sets; FM-9 → loop-guard; FM-11 → VG-6; FM-12 →
authority rule) are correct and useful for the builder. STRONG close.

### GAP-3 (IMPORTANT, §5 FSM/gate table + §5.3 INV-016 5-predicate) — CLOSED

| Spec element | File 08 claim | Spec source | Match? |
|---|---|---|---|
| Gate table G-arm/G-edit/G-push predicates + L0-L3 matrix | §3.2 | :294-303 | EXACT (incl. L1→PROPOSED, L2→HALT_BEFORE_PUSH) |
| needs_human_decision ⇒ HALT_HUMAN override | §3.2 | :302-303 | EXACT |
| S2b_VERIFY content-gate (not ordinal), no-round-consume | §3.1 | :305-311 | EXACT |
| INV-016 5-predicate conjunction (verbatim) | §3.3 | :316-334 | EXACT (all 5 predicates, fail-routing, audit record, one-time --yes confirm) |
| T-ZERO-EDIT-NO-PUSH (predicate 5) | §3.3 | :333-334 | EXACT |
| Loop-guard INV-001 increment edge + `>=` not `>` | §3.5 | :602-606, :618-619 | EXACT |
| T-626-OFF-BY-ONE, T-VANISHED-MONO, T-620..629 matrix | §3.5 | :641-659, :626-637 | EXACT |
| Module + tests | `fsm.py`,`loop_guard.py`,`classifier.py`; `test_autonomy_gates.py`,`test_loop_guard.py` | derived | MAPPED, actionable |

The 5-predicate conjunction and fence-post tests are mapped to concrete asserts. CLOSE.

### GAP-4 (MINOR, §10 VG-1..6 ordered list + lint≠format split) — CLOSED

| Spec element | File 08 claim | Spec source | Match? |
|---|---|---|---|
| VG-1..VG-6 ordered table (command, Blocks, Test) | §3.4 table | :669-676 | EXACT (all 6 rows; Blocks=push/push/push/push/commit/arm) |
| VG-3 (`make lint`=`ruff check`) ≠ VG-4 (`ruff format --check`) | §3.4 + note | :673-674, :678-679 | EXACT — two distinct gates; T-511 regression |
| all-green ⇒ validation_status=="validated" feeds §5.3 pred(2) | §3.4 | :666-667 | EXACT |
| §10.1 no-push-on-failure + validation retry no round increment (INV-6/T-520) | §3.4 | :681-685 | EXACT |
| §10.2 commit-and-push gate (origin not upstream, co-author trailer) | §3.4 | :687-693 | EXACT |
| Module + test | `fsm.py` S7_VALIDATING; `test_validation_gate.py` | derived | MAPPED, actionable |

The VG-3/VG-4 split is correctly flagged as load-bearing and tied to the project's own
`reference_make_lint_vs_ci_ruff_format.md` memory note. CLOSE.

---

## Spot-Check Results (adversarial — did the file misstate the spec?)

1. **Event-type count** — re-counted spec:724-731 independently → 32. File says 32, flags
   prompt's "30" undercount + 33rd from §12.1. ACCURATE.
2. **INV-007 ordering** — step-by-step compared §2.1 vs spec:756-763. fsync points,
   field lists, PRE-push key all byte-accurate. ACCURATE.
3. **5 idempotency sets** — all 5 present, keys match spec:739-744; fix_key formula
   `sha256(path+line+finding_body)` matches :740-741. ACCURATE.
4. **VG-3/VG-4 split** — commands match spec:673-674 exactly; "make lint = ruff check
   only" matches the known gotcha at :678-679. ACCURATE.
5. **Crash-window push_count==2** — matches spec:775. Branch-A semantics correctly
   explained. ACCURATE.

No misstatements found. The file does NOT over-claim or invent spec content. Where it
extends beyond extraction (recommending `recovery.py` as a new module name) it explicitly
labels this as a recommendation inherited from R4, not a spec mandate — appropriate.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | GAP-1 §11 run-log fully researched | PASS | §1.1-1.5 maps authority/locations/envelope/32 events/5 idemp sets to run_log.py + tests; verified vs spec:697-744 |
| 2 | GAP-1 event-type list accurate | PASS | independently counted spec:724-731 = 32; file flags +1 (push_aborted_or_not_landed) from :771 |
| 3 | GAP-2 §12.1 INV-007 triad + crash-window + FM-1..12 | PASS | §2.1-2.3 verbatim-match spec:754-792; recovery.py + test_crash_recovery.py mapped |
| 4 | GAP-2 crash-window 3-way branch + double-push test | PASS | §2.2 A/B/C match spec:765-776; push_count==2 verified :775 |
| 5 | GAP-3 §5 gate table + S2b_VERIFY | PASS | §3.1-3.2 match spec:294-314; fsm.py/classifier.py mapped |
| 6 | GAP-3 §5.3 INV-016 5-predicate | PASS | §3.3 verbatim-match spec:316-334; T-ZERO-EDIT-NO-PUSH mapped |
| 7 | GAP-3 loop-guard INV-001 fence-post | PASS | §3.5 matches spec:598-659; T-626/T-VANISHED/T-620..629 mapped to loop_guard.py |
| 8 | GAP-4 §10 VG-1..6 ordered + lint≠format | PASS | §3.4 matches spec:663-693; VG-3≠VG-4 split + T-511 to test_validation_gate.py |
| 9 | Builder can write per-item checklist entries w/o guessing | PASS | every subsystem → module → test file → key test IDs in summary table (file:393-403) |
| 10 | No fabricated/over-claimed spec content | PASS | 5 adversarial spot-checks all accurate; recommendations explicitly labeled |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
None. All four prior gaps closed. The three spec-internal findings the file surfaces
(32-vs-30 event count + 33rd event; VG-3≠VG-4; fix_key dedup threading) are correct and
should be carried into the builder as explicit per-item notes — they are build hardening,
not blockers.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 5 | Grep: 0 | Glob: 0 | Bash: 0
(Read 1 = file 08 full; Reads 2-5 = spec ranges 695-804, 294-340, 663-694, 598-660 —
each targeting a specific gap's spec source for independent cross-validation. No web
research required: all claims are local-spec-bound, not external.)

## Recommendations
- GREEN LIGHT for synthesis. Proceed to Phase 4/5.
- Builder MUST carry these three file-08 notes into per-item checklist entries:
  (a) register **33** event types (32 from §11.3 + `push_aborted_or_not_landed` from §12.1);
  (b) keep VG-3 (`make lint`) and VG-4 (`ruff format --check`) as **two separate gates** —
      collapsing them re-introduces the documented bug (T-511 is the regression test);
  (c) `fix_key = sha256(path+line+finding_body)` is the single dedup key threading
      §11.4 / EC-4 / recovery branch B / FM-6-FM-7 — do not key fix-dedup on comment_id.

## VERDICT: PASS

All four prior gaps (GAP-1 CRITICAL, GAP-2 CRITICAL, GAP-3 IMPORTANT, GAP-4 MINOR) are
genuinely closed with spec-cited, module-mapped, test-mapped, actionable content. No
residual gaps. Not a rubber-stamp — every claim was cross-checked against the spec and the
event-type list was re-counted independently.

## QA Complete
