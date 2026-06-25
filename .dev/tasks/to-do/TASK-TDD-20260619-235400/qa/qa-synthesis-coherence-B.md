# QA Report — TDD Synthesis Coherence (Partition B: synth-06 → synth-09)

**Topic:** FR-RH2 Headless Ensemble Fix — Heavyweight TDD synthesis coherence
**Date:** 2026-06-20
**Phase:** tdd-qualitative (synthesis-coherence slice)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)
**Assigned files:** `synth-06-error-security.md`, `synth-07-observability-testing.md`, `synth-08-perf-deps-migration.md`, `synth-09-risks-alternatives-ops.md` (TDD §§12–28)
**Stance:** Adversarial — assumed contradictions/incoherence exist; verified load-bearing claims against shipped source.

---

## Overall Verdict: FAIL

Three issues found (1 IMPORTANT internal contradiction, 2 MINOR citation/emphasis defects). The synthesis is **substantially coherent** — every load-bearing coherence axis the prompt named (the (M,N) error table ↔ verdict logic ↔ §15 tests; observability/testing ↔ requirements; deps/migration NFR-7 reconciliation ↔ isolation invariant; alternatives ↔ chosen in-process import; `ensemble-empty` consistency across §12 edge-case AND §22 open-question; Alt 0 + BLOCKING Q1) holds against actual code. But per the no-leniency / contradictions-are-never-minor rules, the one cross-file factual contradiction (5xx retry "immediate" vs "+2s backoff", where source confirms a 2s backoff) is IMPORTANT and forces FAIL until reconciled. No CRITICAL issues.

---

## Items Reviewed

| # | Coherence check | Result | Evidence |
|---|-----------------|--------|----------|
| 1 | (M,N) error table (§12.2.1) ↔ `derive_verdict` ordering | PASS | `contract.py:130-237` confirms `BLOCKED→DEGRADED→HALTED→PASS` first-match; M==0 blocked ordered ahead of degraded exactly as §12.2.3/§13.1/§14.3 claim |
| 2 | (M,N) table ↔ §15 integration tests (each branch proven) | PASS | I6=M==0, I2+I5=M==1, I4=M≥2<2cls, I1/I3=M≥2≥2cls; falsifiable (I1 positives must FAIL on I2/I4/I5/I6) |
| 3 | `ensemble-empty` slug — §12 edge case AND §22 open question, consistent | PASS | synth-06 §12.2.1 D3 note ↔ synth-09 §22 Q6 (D3): same 2 options, same blocked/exit-2 conclusion, both route to OQ; grep confirms 0 hits in `reflect/` |
| 4 | Verdict→exit-code map consistency across §12/§13/§14/§17/§27 | PASS | `models.py:45-48` = `pass→0/halted→10/degraded→11/blocked→2`; every table matches |
| 5 | `_degraded_reason` triggers (§14.4) ↔ source | PASS | `contract.py` L263-264 (`degraded-tier1`), L268-269 (`degraded-model-diversity`), L280-281 (`single-reviewer-fallback`) match cited line numbers |
| 6 | Observability (§14) ↔ requirements (NFR-RH2.7 pollability) | PASS | `done.json` sentinel, `--detached`/tmux, `--tui` all map to NFR-RH2.7; `reduce.py emit_done_sentinel` cited correctly |
| 7 | NFR-7 reconciliation (§19.6) ↔ isolation invariant | PASS (with MINOR cite defect, see #10) | Guard scans `_REFLECT_PKG` only; `_RUNNER_SRC` single-file raw-subproc test + `_REFLECT_PY` glob async/sprint guards confirmed; scope-extension to `_NO_NEST_SRCS` list is the correct mechanic |
| 8 | Alternatives (§21) ↔ chosen in-process import | PASS | Alt 0/1/2 + integration sub-decision all point at swarm-library import; reuse-audit `0.81/reuse-by-import` matches `reuse-audit.yaml` exactly |
| 9 | Deps (§18) private-symbol coupling ↔ §21 Con ↔ §22 Q7 | PASS | `_resolve_run_transport_factory` at `commands.py:612` confirmed private; consistent across §18.2/§21/§22 Q7/§27 |
| 10 | BLOCKING Q1/OI-1 gates FR-RH2.3 everywhere | PASS | §12 xref, §18.4, §19.1 Phase 0, §20 R2, §22 Q1, §23 M0→M3, §24 DoD all gate FR-RH2.3 on Q1 consistently |
| 11 | `--reviewers 1` clamp-vs-negative-witness (Q8) coherence | PASS | §17.2/§19.2/§19.4/§22 Q8/§23 Phase4 reconcile: 1 = pass-through-to-degrade, not clamp-to-2 |
| 12 | `--depth` exists / `expected_tier` derivation (D7) | PASS | `commands.py:102-103` `Choice(["standard","deep"])`; `runner.py:403` `expected_tier=2 if depth in {standard,deep} else 1` — exact |
| 13 | `ReflectConfig` 3-file edit location (§19.2) | PASS | `models.py:58` class, `depth` L70, `max_fix_iterations` L86 — "append at tail after L86" is correct |
| 14 | 5xx retry policy: §12.4 ↔ §17.2 | **FAIL** | §12.4 says "**Immediate** single retry"; §17.2 says "+2s backoff"; `dispatch.py:46` confirms `on_5xx_backoff_sec=2` → §12.4 is wrong (contradiction) |
| 15 | `ModelPoolTooSmallError` line citations §12 ↔ §20/§25/§28 | PASS (MINOR imprecision) | Class+msg at `commands.py:589-609` (synth-09 cite); raise at L688 (synth-06 cite); both correct, point at same symbol |
| 16 | D3 Option-A framing (synth-06) ↔ Q6 option-(ii) framing (synth-09) | PASS (MINOR emphasis gap) | Both = "add slug under existing BLOCKED verdict"; synth-06 flags FR-RH2.7 `derive_verdict`-out-of-scope tension explicitly, synth-09 Q6(ii) glosses it |

---

## Summary

- Checks passed: 14 / 16 (two carry MINOR sub-defects but the coherence claim holds)
- Checks failed: 1 (item 14 — cross-file retry-policy contradiction)
- Critical issues: 0
- Important issues: 1
- Minor issues: 2
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | synth-06 §12.4 retry table (L94) vs synth-08 §17.2 (L49,51) | **Cross-file factual contradiction on 5xx retry timing.** synth-06 §12.4 "Backoff / Budget" column for the 5xx row reads "**Immediate single retry**; per-call budget 180s." synth-08 §17.2 says the 5xx retry has "+2s backoff" (`on_5xx_backoff_sec=2`) and derives a 362s worst-case (180+2+180). Source `dispatch.py:46` confirms `on_5xx_backoff_sec=2` — there IS a 2s backoff. synth-06's "Immediate" is incorrect and contradicts synth-08. Per Critical Rule #6 a cross-section contradiction is never MINOR. Impact is bounded (verdict/exit logic unaffected; only wall-clock characterization), but an implementer reading §12.4 would mis-model the retry timing. | Edit synth-06 §12.4 row "Swarm dispatch 5xx" Backoff/Budget cell from "Immediate single retry; per-call budget 180s" to "2s backoff then single retry (`on_5xx_backoff_sec=2`); per-call budget 180s; worst-case slot ≈ 362s (180+2+180) — see §17.2". Align wording with synth-08. |
| 2 | MINOR | synth-08 §19.5 (L215) + Cross-Section Notes | **Wrong `file:line` in the NFR-7 reconciliation (load-bearing OI-2 text).** §19.5 says the raw-subprocess ban stays scoped to `{runner.py, ensemble.py}` "because `commands.py` keeps a legitimate `--tmux subprocess.run` (`commands.py:267-274`)." The reasoning is substantively CORRECT for **reflect/commands.py** (which has a sanctioned `subprocess.run(["tmux", ...])` — verified at `reflect/commands.py:320,325,327`), but (a) the cited line range `267-274` contains `_is_tmux_available`/`_session_name`, NOT a subprocess, and (b) the file is left ambiguous (swarm/commands.py:267-274 is unrelated docstring text). This text is destined for the guard docstring / spec §9 (the recorded OI-2 amendment), so a wrong line is more than cosmetic. | Change `commands.py:267-274` → `src/superclaude/cli/reflect/commands.py:311-327` (`_launch_tmux`, the sanctioned `subprocess.run(["tmux", ...])`). Disambiguate the file as `reflect/commands.py`. |
| 3 | MINOR | synth-09 §22 Q6 option (ii) (L120) | **Emphasis divergence from synth-06 §12 D3 Option A on the FR-RH2.7 tension.** Both describe the same change (add `ensemble-empty` as a new reason slug under the existing BLOCKED verdict). synth-06 D3 Option A explicitly states this "must be called out against FR-RH2.7's 'unchanged' claim" because adding a slug requires editing `derive_verdict`, which FR-RH2.7 lists as out-of-scope. synth-09 Q6(ii) softens this to "the slug is a reason label, not a verdict … keeps the 4-state verdict map / exit codes intact" without noting it still requires a `derive_verdict` code edit. Not a contradiction (both reach identical verdict/exit conclusions and both route to the OQ), but the asymmetric rigor could let an implementer pick Q6(ii) believing it touches no out-of-scope code. | Add to synth-09 Q6 option (ii) a parenthetical matching synth-06 D3 Option A: "(note: introducing a new slug requires a `derive_verdict` edit, which FR-RH2.7 lists as out-of-scope — record as a deliberate amendment, same caveat as §12 D3 Option A)." |

---

## Actions Taken

None — `fix_authorization: false`, report-only. All three issues documented with specific file/line and exact remediation above.

---

## Self-Audit

**(a) Reliance list — structural items not re-checked (handled by rf-qa structural phase):**
- Relied on rf-qa for section-numbering / template-conformance / cross-reference-existence (§12–§28 numbering, table presence). This is a synthesis-coherence slice, not a structural re-verification.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **`derive_verdict` ordering** — verified by `grep -n "Verdict\." contract.py` → L150-237 confirm `BLOCKED→DEGRADED→HALTED→PASS` first-match (not a structural check; the *semantic* claim that M==0 blocked precedes degraded).
- **5xx backoff value (the FAIL)** — verified by `grep on_5xx_backoff_sec dispatch.py` → L46 `on_5xx_backoff_sec=2`, which falsified synth-06 §12.4 "Immediate" and adjudicated the cross-file contradiction. Pure semantic/factual verification rf-qa would not perform.
- **`ensemble-empty` absence** — `grep -rn ensemble-empty src/superclaude/cli/reflect/` → 0 hits, confirming the D3/Q6 honesty claim against live source.
- **`_degraded_reason` trigger line numbers** — `sed -n 249,305p contract.py` confirmed Trigger 6/7/10 slugs and lines match §14.4.
- **`reflect/commands.py` tmux subprocess** — `grep subprocess reflect/commands.py` → `subprocess.run(["tmux",...])` at L320-327, which substantiated the §19.5 reasoning while exposing its wrong line cite.

How many factual claims independently verified against source: **~18** (verdict map, ordering, 7 degraded triggers, ensemble-empty absence, ensemble.py non-existence, ModelPoolTooSmallError class+raise sites, reduce_wave3 M/N, --depth existence, expected_tier derivation, ReflectConfig location, no-nest guard structure, 5xx backoff, reflect tmux subprocess, reuse-audit numbers).
Files read to verify: `contract.py`, `models.py`, `runner.py`, `commands.py` (reflect + swarm), `config.py` surface, `dispatch.py`, `reduce.py`, `transports/openai_compat.py`, `test_no_nesting_guard.py`, `reuse-audit.yaml`, plus the 4 assigned synthesis files.
Why trust the check: 1 IMPORTANT contradiction was found by direct source falsification (not pattern-matching prose), and 2 of the 4 "consistent" findings were stress-tested against source and survived — the review did not rubber-stamp.

---

## Confidence

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep/Bash: 11 | Glob: 0 | (15 tool calls ≥ 16 checks — within tolerance; several Bash calls verified multiple checks each)

No web research was performed (all coherence checks were local-file / source-code bound; Tavily not required). No Tavily-vs-fallback event to record.

---

## Recommendations

1. **Resolve Issue 1 (IMPORTANT) before assembly** — reconcile the 5xx retry "Immediate" vs "+2s backoff" wording so §12.4 and §17.2 agree with `dispatch.py:46`. This is the only FAIL-forcing item.
2. Fix the two MINOR citation/emphasis defects (Issues 2–3) — both touch text destined for the guard docstring / spec §9 (OI-2) or the Q6 decision record, so accuracy matters downstream.
3. The `ensemble-empty` reconciliation, BLOCKING Q1 gating, NFR-7 isolation-invariant preservation, alternatives↔chosen-architecture coherence, and (M,N)↔test-coverage are all CONFIRMED coherent — no action needed on those axes.

## Partition Note

[PARTITION NOTE: This is Partition B (synth-06..synth-09 / TDD §§12–28). Cross-file coherence checks were applied within this assigned subset. Coherence between this slice and synth-01..synth-05 (§§1–11) requires merging with the Partition-A report. Notably, §15's claim that B1/B2/B3 backward-compat tests pin contracts in §6, and §18's reference to the synth-04 OI-1 field-correspondence table, are cross-partition dependencies I verified only from this slice's internal references.]

## QA Complete
