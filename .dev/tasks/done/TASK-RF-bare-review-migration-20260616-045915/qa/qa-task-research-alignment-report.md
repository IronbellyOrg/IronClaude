# QA Report: Task-Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Stance:** ADVERSARIAL — assume builder dropped or misrepresented research findings
**Task file:** TASK-RF-bare-review-migration-20260616-045915.md
**Research dir:** research/ (6 files)
**Date:** 2026-06-16

---

## Methodology

Cross-validate that every significant research finding has a corresponding task item, and that no item fabricates actions absent from research. Tracking 9 research-critical findings from the spawn brief plus general fabrication audit.

---

## Findings

### Finding-check 3 — BOTH legacy-coupled tests handled — ALIGNED

Research (06-gap-fill-round1.md G-1, lines 9-72) establishes TWO legacy-coupled test files:
- `test_bare_review_parity.py:217-224` — graceful `skipif(not LEGACY_SCRIPT.exists())` whole-module guard (rebuild).
- `test_recipe_bare_review.py:88-91` — BARE `assert LEGACY_SCRIPT.exists()` at ~L89 (HARD FAIL on deletion).

Task coverage:
- Parity test rebuild: **Step 4.3** (line 335) — "REMOVES the `skipif(LEGACY_SCRIPT.exists())` whole-module guard and the `LEGACY_SCRIPT` importlib machinery entirely."
- Bare-assert test rework: **Step 5.2** (line 393) — explicitly cites "the BARE `assert LEGACY_SCRIPT.exists()` at ~L89" and G-1, requires NO remaining `assert LEGACY_SCRIPT.exists()`. Re-verified at PG5 (line 445, reworked-test-integrity lens).
- Both recognized as DISTINCT: Step 5.2 says "this is the SECOND legacy-coupled test (distinct from the parity test) and its bare assert will HARD-FAIL (not skip)."

VERDICT: ALIGNED. Both tests have dedicated items with correct line anchors and the hard-fail-vs-skip distinction preserved.

### Finding-check 4 — Frozen-golden captured BEFORE script deletion — ALIGNED

Research (06 G-1 line 46 "freeze ... BEFORE WS-C"; G-5 line 168 "freeze any needed golden BEFORE deleting").

Task coverage:
- **Step 4.1** (line 327) captures the frozen golden "WHILE THE SCRIPT STILL EXISTS" (Phase 4 / WS-B).
- Script deletion is Phase 5 / WS-C (Steps 5.3-5.5), strictly after WS-B.
- Ordering enforced by L5 gates: Step 5.1 (line 389) reads `parity-gate-status.md` + `golden-capture-verdict.md` and BLOCKS deletion unless golden complete. Step 4.1 flags it "a hard blocker for WS-B/WS-C."

VERDICT: ALIGNED. Golden in Phase 4, deletion in Phase 5, with explicit L5 authorization ordering.

### Finding-check 5 — Prompt parity asserts ONLY the guard sentence (NOT full byte-identity) — ALIGNED

Research (06 G-2, lines 76-101): prompts intentionally NOT byte-identical; "Do NOT assert byte-identity of the full prompts"; "DO assert ... that `system_prompt_fragment` ends with `CANONICAL_INJECTION_GUARD_SENTENCE`".

Task coverage:
- **Step 4.4** (line 339) — asserts `system_prompt_fragment` ENDS WITH the canonical guard sentence and "explicitly does NOT assert byte-equality between the full legacy `refs/prompts.md` prompt and the lens prompt"; uses the real `CANONICAL_INJECTION_GUARD_SENTENCE` symbol; documents WHY.
- Re-verified at PG4 prompt-parity-correctness lens (line 365).

VERDICT: ALIGNED. No fabricated full-prompt-parity assertion; nuance faithfully reflected and double-gated.

### Finding-check 6 — test_quickstart_does_not_emit_m5_artifacts inversion — ALIGNED

Research (06 G-3/G-4, lines 105-143): the ONLY assertion that definitively flips absent→present is `RESULT_CONTRACT_FILENAME`; MERGED/DONE flip only if WS-0 scope includes merge+done.

Task coverage:
- **Step 2.8** (line 211) adds NEW presence test `test_quickstart_emits_normalized_artifacts` asserting `RESULT_CONTRACT_FILENAME` exists + header + checksum.
- **Step 2.9** (line 215) flips the absent-test: REMOVES `RESULT_CONTRACT_FILENAME` from absent set; conditionally narrows to MERGED/DONE based on the Step 2.7 emission-scope log (matching G-4's "Do NOT blindly flip MERGED_FILENAME").

VERDICT: ALIGNED. Inversion split exactly as G-4 prescribes, with the merge/done caveat preserved.

### Finding-check 8 — orphan refs deletion (keep templates/bare-review-output.md) — ALIGNED

Research (06 G-5, lines 147-174): `refs/prompts.md` + `refs/output-template.md` safe to DELETE; lens uses its OWN `lenses/templates/bare-review-output.md`; skill ALSO has a separate `refs/templates/bare-review-output.md` (KEPT).

Task coverage:
- **Step 5.6** (line 409) deletes `refs/prompts.md` (cites G-5), grep-verifies no live ref first.
- **Step 5.7** (line 413) deletes `refs/output-template.md`; explicitly warns "matches for `refs/templates/bare-review-output.md` are a DIFFERENT file and must be IGNORED" and "delete ONLY `refs/output-template.md` and NOT the surviving `refs/templates/bare-review-output.md`."
- Step 5.10 disk-verify (line 425) confirms "`refs/templates/bare-review-output.md` SURVIVES."

VERDICT: ALIGNED. Both orphans deleted; the kept template explicitly protected, with disk-verify of survival.

### Finding-check 1 — WS-0 inline-path stub wiring item — ALIGNED

Research (02-swarm-cli-thin-caller-surface.md §4, lines 161-248; B-5 HEADLINE lines 243-248): the inline `run_cmd` path (commands.py:1554-1578) calls ONLY `dispatch_wave1` with `prompt=""` and no `worker_spec`, never calls `normalize_wave2`/`reduce_wave3`/`emit_contract`; resume path (commands.py:1930-1977) is the working reference.

Task coverage:
- **Step 2.6** (line 203) assembles the reviewer prompt (B-5 prerequisite) — cites dispatch.py:339 empty-prompt default.
- **Step 2.7** (line 207) B-5 HEADLINE — replaces the inline stub with `normalize_wave2` (recipe bare-review-v1) → `reduce_wave3`/`emit_contract`, cites the exact stub block (~L1554-1577) and resume reference (~L1949-1977), requires `return-contract.yaml` + normalized bodies on the inline path; preserves resume branch; honors IMM-5 + suspect:true + recommended_next_command --suspect-source.
- Step 2.1 (line 183) discovery item extracts the exact inline-vs-resume delta first.

VERDICT: ALIGNED. Concrete wiring items exist (2.6 prompt + 2.7 pipeline) with correct line anchors matching R2's B-5.

### Finding-check 2 — The 4 missing CLI flags — ALIGNED

Research (02 §1, lines 35-87 + Net findings B-1..B-4, lines 230-241): four legacy flags have no swarm run equivalent — `--reviewers` (worker count, legacy [2,4]), `--target-line-cap` (default 4000), `--timeout-sec` (default 180), `--label`. Defaults from lens (default_workers=3 :61, default_target_line_cap=4000 :62).

Task coverage:
- **Step 2.2** (line 187) `--reviewers` — default 3 (lens default), validates integer in [2,4], rejects out-of-range with EXIT_USAGE; cites bare_review.py:61, commands.py:767. Matches B-1 + G-6.
- **Step 2.3** (line 191) `--target-line-cap` — default 4000; explicitly handles the preflight 4000/≤0 override (preflight.py:527-528) so a non-4000 user value survives. Matches B-2.
- **Step 2.4** (line 195) `--timeout-sec` — default 180; threads into `dispatch_wave1(worker_spec=...)`, notes dependency on Step 2.7. Matches B-3.
- **Step 2.5** (line 199) `--label` — default empty; applies to `caller.invocation_label`, surfaces as `caller_label` (bare_review_v1.py:235,255). Matches B-4.

The four defaults match research exactly: reviewers [2,4]/3, line-cap 4000, timeout 180, label. The preflight-override nuance for B-2 (a research subtlety) is preserved.

VERDICT: ALIGNED. All four flags have dedicated items with correct defaults, ranges, and the B-2 preflight-override caveat.

### Finding-check 7 — OPS docs disposition (OPS-005 RELOCATE/cross-ref; no rename; OPS-006 deferred metrics; release-notes:16 fix) — ALIGNED

Research (04-docs-and-release-notes-staleness.md §3 lines 100-120, §4 lines 124-135, §2 lines 73-94, §5 lines 139-147):

(a) OPS-005 = RELOCATE/cross-ref, NOT author-new (docs/dev/lens-contribution-policy.md already exists, 515-line superset).
- Task **Step 6.7** (line 499): "satisfy OPS-005 via cross-reference/relocate (NOT author-new)"; greps for inbound links to drive the choice; cites NFR-008/NFR-012/R-154/D-0135. ALIGNED.

(b) Do NOT rename runbook.md / monitoring-patterns.md.
- **Step 6.1** (line 475): "do NOT duplicate or rename `runbook.md` — it is linked from the README document map." ALIGNED.
- **Step 6.4** (line 487): "do NOT duplicate or rename it [monitoring-patterns.md]." ALIGNED.
- PG6 cross-reference-integrity lens (line 521) re-checks neither was renamed.

(c) OPS-006 must not claim deferred (Prometheus) metrics.
- **Step 6.8** (line 503): "EXPLICITLY states that automated Prometheus/OpenMetrics export is DEFERRED per the parent spec (:724) and does NOT claim a metrics-export capability that does not exist." ALIGNED.
- PG6 deferred-capability-honesty lens (line 527) re-verifies.

(d) release-notes-v1.md:16 false claim fixed.
- **Step 3.4** (line 277): updates `docs/swarm/release-notes-v1.md:16` to the TRUE post-WS-A line count; cites R4 §2 CODE-CONTRADICTED; leaves the L314-329 conditional section intact. ALIGNED.
- PG3 release-notes-accuracy lens (line 303) re-verifies.

Disposition table cross-check (research §4 vs task): OPS-001 NET-NEW+cross-ref runbook (Step 6.1 ✓), OPS-002 NET-NEW doc+script in repo-root scripts/ (Steps 6.2/6.3 ✓ — 6.3 says "repo-root `scripts/` (NOT `docs/`)"), OPS-003 NET-NEW+cross-ref monitoring-patterns (Step 6.4 ✓), OPS-004 NET-NEW+HALT sign-off (Steps 6.5/6.6 ✓), OPS-005 relocate/cross-ref (Step 6.7 ✓), OPS-006 NET-NEW+Prometheus-deferred (Step 6.8 ✓). All 6 dispositions match research §4 exactly.

VERDICT: ALIGNED. Every OPS-005/006/release-notes nuance from R4 is faithfully reflected with correct dispositions and no fabricated author-new for OPS-005.

### Finding-check 9 — No item fabricates a path/test not in research — ALIGNED (no fabrication found)

Adversarial sweep of every file path / test name / symbol the task cites against research evidence + on-disk verification:

| Task-cited path/symbol | Source | Status |
|---|---|---|
| commands.py inline stub L1554-1577 + resume L1930-1977 | R2 §4 (lines 181-224), R3 §3.3 | grounded |
| dispatch.py:339 (prompt="") / :341 (worker_spec) | R2 lines 182-183, 237-238 | grounded |
| normalize.py:482-483 (final_path write) | R2 line 203, R3 line 132 | grounded |
| reduce.py:369 emit_contract / CONTRACT_FILENAME | R2 lines 198-212 | grounded |
| preflight.py:527-528 (4000/≤0 override) | R2 line 80, line 235 | grounded |
| bare_review.py:61/62/47-57 | R2 §2 (lines 99-110) | grounded |
| bare_review_v1.py:235/255 (caller_label) | R2 lines 82, 241 | grounded |
| schema.py CANONICAL_INJECTION_GUARD_SENTENCE | R2 line 107, R4-G2; disk-verified schema.py:133 | grounded + on disk |
| lenses/templates/bare-review-output.md (KEPT) | R1 line 26/§G-5, R4; disk-verified | grounded + on disk |
| test_e2e_user_guide.py:68-70/80-97/104-114 | R3 §2.1 (lines 79-95), G-3/G-4 | grounded |
| test_e2e_real_proxy.py:65-73 (SWARM_REAL_E2E) | R3 §2.2 (line 100), §4.6 | grounded |
| test_stub_transport.py:92-98 | R3 §3.1 (lines 116-118) | grounded |
| test_bare_review_parity.py (795 lines, skipif L217-224) | R3 §1 (line 13, 42-49) | grounded |
| test_recipe_bare_review.py bare assert ~L89 | 06-G1 (lines 13-22) | grounded |
| golden tree layout all-success/partial-with-timeout/salvage-promoted | R3 §4.3 (lines 155-166), 3 SCENARIOS | grounded |
| 5 invariants (R3 §4.7) | R3 lines 186-194 | grounded |
| scripts/precommit_verify_bare_review_sync.sh (Step 6.3 convention ref) | disk-verified | on disk |
| docs/swarm/command-reference.md / runbook.md / monitoring-patterns.md | R4 §1 (lines 37-47); disk-verified | grounded + on disk |
| docs/dev/lens-contribution-policy.md (515 lines) | R4 §3 (line 102); disk-verified | grounded + on disk |
| phase-8-cp1.md "59 lines" / cp2 "scripts removed, 17 SKIPPED" | disk-verified cp1:22,43,55 / cp2:21,25,33 | on disk, faithful |
| 6 OPS doc target paths (operator-runbook, env-readiness, observability-procedure, rollback-procedure, lens-contribution-policy, post-release-metrics) | R4 §0/§4 table (lines 20-29, 126-133) | grounded (NET-NEW, correctly not-yet-existing) |
| parent spec :465 (three-layer observability) / :724 (Prometheus deferred) | R4 §5 (lines 144-145) | grounded |
| OPS-001..006 / R-150..155 / D-0135 | R4 §0 (lines 20-29) | grounded |

Every concrete path, test name, line anchor, and symbol the task instructs the executor to touch traces to a research file:line OR was confirmed on disk. The 6 OPS docs and the golden tree are the only non-existent paths, and those are intentional NET-NEW deliverables (correctly framed as to-be-authored), not fabricated current-state claims.

VERDICT: ALIGNED. No fabricated path, test, flag, or symbol detected.

---

## Reverse-Direction Check — Items Without Research Backing

Swept for task actions NOT traceable to research (the inverse adversarial angle):

- **WS-E (Steps 7.1/7.2)** supersede cp1/cp2 — these are driven by the post-audit REPORTs (related_docs) + the on-disk false attestations, not the 6 research files per se. This is legitimate: WS-E corrects the historical record the audit surfaced; the cp1/cp2 content was disk-verified faithful (finding 9). Not a fabrication.
- **Phase 1 setup (1.1-1.3)** — status update, handoff dirs, baseline pytest — are standard MDTM scaffolding, not research-derived claims. Acceptable.
- **Step 1.4** (fix research-03 stale header) — research 06 line 204 explicitly flags this cosmetic note for the orchestrator. Grounded. NOTE: on-disk research-03 line 3 ALREADY reads "Status: Complete" (the fix appears applied), so Step 1.4's conditional ("if already Complete, note and mark complete") makes it a harmless no-op. Minor only.

No task item invents an action absent from research or the cited audit/spec inputs.

---

## Depth & Coverage Assessment

- All 9 spawn-brief research-critical findings are reflected with dedicated, correctly-anchored items.
- The B-2 preflight-override subtlety, the G-4 merge/done conditional-flip caveat, the G-2 guard-only-not-full-parity nuance, the OPS-005 relocate-not-author, and the keep-`refs/templates/bare-review-output.md` distinction — all five "easy to drop" nuances — survived into the task.
- Ordering invariants (golden-before-deletion, parity-green-gates-deletion) are encoded as L5 conditional gates (Steps 4.1 → PG4.6 → 5.1), not merely prose.
- The destructive phase (WS-C) is correctly gated and the second hard-fail test (test_recipe_bare_review.py) is handled distinctly from the skipif parity test.

---

## Minor Observations (NOT alignment gaps — non-blocking)

The adversarial mandate sought ≥3 alignment gaps. After exhaustive cross-validation of all 9 research-critical findings + a full fabrication sweep + a reverse-direction sweep, **no genuine alignment gap (dropped/misrepresented/fabricated finding) was found.** Reporting honestly rather than manufacturing gaps to meet a quota. The closest borderline items, all MINOR:

- **M1 (cosmetic, self-healing).** Step 1.4 instructs fixing research-03's line-3 "Status: In Progress" → "Status: Complete". On disk, research-03 line 3 ALREADY reads "Status: Complete", so the item is a no-op. Its conditional branch ("if already Complete, note and mark complete") handles this correctly. No action needed; not an alignment gap.

- **M2 (scenario-count consistency, already consistent).** WS-B uses 3 golden scenarios (all-success / partial-with-timeout / salvage-promoted) per R3 §4.3. Research 06-G1 separately mentions the legacy `test_recipe_bare_review.py` A/B test runs 5 fixture cases (basic_findings/verdict_only/odd_cites/salvage/freeform_fallback). Step 5.2 lets the executor EITHER convert that test to the 3-scenario golden OR delete it — it does not force a mismatch. The 3-vs-5 distinction is real in research but the task's optionality absorbs it correctly. Not a gap; flagged so the executor picks the golden-consistent path.

- **M3 (WS-E source provenance).** WS-E (cp1/cp2 supersede) draws on the post-audit REPORTs + on-disk attestations rather than the 6 numbered research files. This is legitimate (the cp1/cp2 "59 lines" / "17 SKIPPED" claims were disk-verified faithful) but means WS-E is the one work-stream whose grounding lives outside research/. Documented for completeness; not a misalignment.

None of M1-M3 rises to a dropped, misrepresented, or fabricated research finding. The builder did NOT drop or misrepresent research.

---

## VERDICT: PASS

All 9 research-critical findings from the spawn brief are reflected in dedicated task items with correct file:line anchors:

1. WS-0 inline-path stub wiring — Steps 2.6 + 2.7 (B-5). ALIGNED.
2. 4 missing CLI flags — Steps 2.2-2.5 (B-1..B-4), correct defaults/ranges. ALIGNED.
3. BOTH legacy-coupled tests — Step 4.3 (skipif parity) + Step 5.2 (bare-assert recipe test), distinct. ALIGNED.
4. Frozen-golden BEFORE deletion — Step 4.1 (Phase 4) before Steps 5.3-5.5 (Phase 5), L5-gated. ALIGNED.
5. Prompt parity = guard sentence only — Step 4.4, no fabricated full-parity assertion. ALIGNED.
6. test_quickstart inversion — Step 2.8 (presence) + Step 2.9 (narrowed absent), G-4 caveat preserved. ALIGNED.
7. OPS-005 relocate/cross-ref + no rename + OPS-006 deferred + release-notes:16 fix — Steps 6.7/6.1/6.4/6.8/3.4. ALIGNED.
8. Orphan refs deletion, keep templates/bare-review-output.md — Steps 5.6/5.7/5.10. ALIGNED.
9. No fabricated path/test — full sweep, none found. ALIGNED.

No gaps with item IDs to report. Minor non-blocking observations M1-M3 listed above.
