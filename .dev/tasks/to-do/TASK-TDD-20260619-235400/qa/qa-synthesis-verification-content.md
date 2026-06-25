# QA Report — Synthesis Coherence Re-Check (Content / Coherence-B Fix Cycle)

**Topic:** FR-RH2 Headless Ensemble Fix — TDD synthesis §12–§28 coherence
**Date:** 2026-06-20
**Phase:** doc-qualitative (synthesis coherence re-verification)
**Fix cycle:** Re-check after 3 fixes (prior coherence-B pass FAILED on a 5xx-retry contradiction)
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume the fix is incomplete or introduced a new defect; prove the contradiction is gone AND no new incoherence appeared.

**Files re-read in full:**
- `synthesis/synth-06-error-security.md` (TDD §12–§13)
- `synthesis/synth-07-observability-testing.md` (TDD §14–§15)
- `synthesis/synth-08-perf-deps-migration.md` (TDD §16–§19)
- `synthesis/synth-09-risks-alternatives-ops.md` (TDD §20–§28)

---

## Overall Verdict: PASS

The previously-failing 5xx-retry contradiction is resolved and code-correct. The §22 Q6 / synth-06 §12 D3 FR-RH2.7 tension is now consistently emphasized across both files. The (M,N) table, verdict/exit-code map, NFR-7 reconciliation, and Alternatives remain coherent across §12–§28. No new contradiction was introduced by the edits.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 5xx-retry consistent between synth-06 §12.4 and synth-08 §17.2 (both: retry once, 2s backoff) | PASS | synth-06 L90 "retries on exactly one signature (5xx), once, with a 2s backoff … This matches synth-08 §17.2"; L94 table "Retry once with 2s backoff (`on_5xx_backoff_sec=2`) … attempts=2". synth-08 L49 "5xx retry once (`on_5xx=True`, `on_5xx_backoff_sec=2`); backoff sleep excluded"; L60 matrix "5xx … yes, once … attempts 1 or 2". Original "Immediate" wording is GONE. |
| 2 | 5xx/backoff/timeout values match source code (not just internally consistent) | PASS | `dispatch.py:224` `on_5xx=True, on_5xx_backoff_sec=2, on_4xx=False`; backoff slept at `:269-271`; backoff excluded from `elapsed_ms` (`:235,:267`). `_DEFAULT_TIMEOUT_SEC = 180` (`:124`). `attempts: int = 1` default (`models.py:1127`). Both synth files match the code exactly. |
| 3 | synth-09 §22 Q6 (ensemble-empty) notes FR-RH2.7 tension matching synth-06 §12 D3 emphasis | PASS | synth-09 Q6 (L120): Option A "modifies the verdict-derivation path … must be called out as a deliberate amendment against FR-RH2.7's 'derive_verdict unchanged' claim … This is the same FR-RH2.7 tension synth-06 §12 D3 Option A flags: only the exit-code map is mechanically pinned; a new `derive_verdict` branch is a recorded change, not a free one." synth-06 D3 (L45) Option A: "deliberate, recorded amendment … must be called out against FR-RH2.7's 'unchanged' claim (the exit-code map stays unchanged)." Explicit cross-reference + matching emphasis. |
| 4 | `ensemble-empty` slug absence claim is factually correct in both files | PASS | `grep ensemble-empty src/superclaude/cli/reflect/` → ZERO hits. synth-06 D3 (L44) and synth-09 Q6 (L120) both correctly state the slug does not exist in `contract.py` today. |
| 5 | synth-07 ensemble-empty usage does not contradict the D3/Q6 absence finding | PASS | synth-07 L78 carries `[UNVERIFIED: exact "ensemble-empty" string is spec vocabulary; the blocked path is CODE-VERIFIED]`; L200 reiterates the `[UNVERIFIED]` confinement to the slug string. synth-07 uses it as the spec's nominal slug, never asserts code existence. Aligned, not contradictory. |
| 6 | (M,N) verdict-routing table coherent across §12/§14/§17/§20-§28 | PASS | M==0→blocked/exit2, M==1→degraded/exit11, M≥2-<2classes→degraded-model-diversity/exit11, M≥2-≥2classes→pass-eligible/exit0 is uniform: synth-06 §12.2.1 (L36-39) + §12.3 (L80-83); synth-07 §14.3 (L60-63); synth-08 §17.3 (L71-74); synth-09 FR-RH2.9 (L211) + Glossary (L324-330). |
| 7 | verdict/exit-code map (`pass→0/halted→10/degraded→11/blocked→2`) uniform + code-correct | PASS | Identical in synth-07 L123, synth-08 L26, synth-09 L214/L294. Source: `reflect/models.py:15` "`pass` -> 0 … `halted` -> 10, `degraded` -> 11, `blocked` -> 2". |
| 8 | NFR-7 reconciliation coherent (synth-08 §19.6 "CONFIRM-with-scope-extension" vs synth-09 Q2 "Open") | PASS | Not a contradiction: synth-08 §19.6 (L204-217) records the resolved DIRECTION (guarantee preserved; HTTP fan-out ≠ Task nesting; extend Layer B to `ensemble.py`). synth-09 Q2 (L116) keeps the EXACT amendment-text / formal confirm-vs-amend ratification open for FR-RH2.8. synth-09 R3 (L20) + R9 (L26) cross-ref the same framing. Direction-resolved / wording-open is internally consistent. |
| 9 | Alternatives (synth-09 §21) coherent + consistent with reuse/NFR-7 framing elsewhere | PASS | Alt 0/1/2 + integration sub-decision (L36-107) cohere: reuse-by-import S_reuse 0.81 (L67), in-process-import-not-subprocess to dodge the `claude -p` nesting failure, consistent with synth-08 §18.2 private-symbol coupling (L122) and §19.6 NFR-7 mechanism distinction. No internal contradiction. |
| 10 | Auto-fix multiplier + worst-case wall-clock numbers consistent across files | PASS | `max_fix_iterations` default 2; `(max_fix_iterations+1) × reviewers = 3×3 = 9` agrees synth-08 L85 + synth-09 L263. Worst-case single-worker 362s = 180+2+180 (synth-08 L51) — derives directly from the fixed 5xx/2s/180s values. No desync. |
| 11 | `--reviewers` clamp `[2,4]` default 3 + `1`=negative-witness uniform | PASS | synth-08 §17.2 L46, §19.2 L174 (clamp/sentinel ordering), §19.4 L187; synth-09 Q8 L122, §23 L178, §24. Q8 reconciliation (`1` accepted, not clamped to 2) consistent with synth-08 L174 obligation. |

## Summary
- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; no defects found)

## Issues Found
None. The fix-cycle target (5xx-retry contradiction) is resolved; no new contradiction detected.

## Resolution Confirmation (prior FAIL → now PASS)
- **Prior defect:** synth-06 described the 5xx retry as "Immediate" while synth-08 described it as "+2s backoff" — a direct contradiction on retry timing.
- **Now:** Both files state "retry once with 2s backoff" verbatim, both cite `on_5xx_backoff_sec=2`, both treat the backoff sleep as excluded from `elapsed_ms`, and synth-06 L90 adds an explicit "This matches synth-08 §17.2" cross-reference. The fixed value is also independently confirmed against `dispatch.py:224,269-271`. CONFIRMED RESOLVED.

## Confidence Gate
- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 5 (via Bash grep) | Glob: 0 | Bash: 5
- Tool-call count (4 Read + 5 grep-bearing Bash) ≥ 11 checklist items is below a strict 1:1 only by batching multiple cross-file grep checks into single Bash calls; each grep directly targeted a specific check (5xx values, exit-code map, ensemble-empty absence, NFR-7 phrasing, multiplier/clamp numbers). No padding calls.
- No UNCHECKED items. No UNVERIFIABLE items.

## Tool-engagement summary (web research)
No external web lookup was required — this is a local-file + source-code coherence review. Tavily was not invoked; no fallback occurred.

## Self-Audit
1. **How many factual claims independently verified against source code?** Five code-grounded facts: `on_5xx_backoff_sec=2` + backoff-excluded-from-elapsed_ms (`dispatch.py:224,235,267,269-271`); `_DEFAULT_TIMEOUT_SEC=180` (`dispatch.py:124`); `attempts` default 1 (`models.py:1127`); exit-code map (`reflect/models.py:15`); `ensemble-empty` absence from `src/superclaude/cli/reflect/` (zero grep hits). The remaining checks are cross-file textual-coherence comparisons, each grep-evidenced.
2. **Specific files read to verify claims?** All four synth files in full; plus targeted greps over `src/superclaude/cli/swarm/dispatch.py`, `src/superclaude/cli/swarm/models.py`, `src/superclaude/cli/reflect/models.py`, and `src/superclaude/cli/reflect/` (ensemble-empty sweep).
3. **If 0 issues, why trust the check?** The single load-bearing fix (5xx timing) was verified three independent ways: (a) both files now say "once, 2s backoff"; (b) an explicit cross-reference line was added; (c) the value matches shipped source. The two highest-risk edit seams — `ensemble-empty` slug status (synth-07 vs 06/09) and NFR-7 status (synth-08 "resolved" vs synth-09 "open") — were specifically probed for newly-introduced contradiction and found to be intentional UNVERIFIED-caveated / direction-vs-wording distinctions, not desyncs.

## Recommendations
- None blocking. Proceed to assembly. The D3/Q6 (`ensemble-empty`) and OI-2/Q2 (NFR-7 amendment text) items remain correctly recorded as Open Questions for implementation time — that is by design, not a coherence defect.

## QA Complete
