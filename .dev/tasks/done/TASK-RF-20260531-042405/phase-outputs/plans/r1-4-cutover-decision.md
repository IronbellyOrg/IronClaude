# R1.4 Tool-Write Cutover Decision

**Step 9.12 — R1.4 cutover criterion (side-by-side parity over ≥3 release cycles).**
**Authored:** 2026-06-02. **Status at authoring:** INITIAL STATE — 0 release cycles run.

> **Single source of truth for cycle counts:** `.dev/migrations/r1-4-cutover-counters.yaml`.
> This document does NOT re-narrate counters in prose and is NOT a dynamic item — it
> records the authoring-time decision and the cutover rule. Live release-cycle tracking
> (incrementing `release_marker_count`) is DEFERRED to R1.6 / a release-cycle hook.

## 1. Cutover rule (Vector A)

Each LLM step stays **dual-write** (production markdown path + opt-in `--tool-write-<step>`
path) for **≥3 consecutive parity-passing release cycles** before its markdown path may be
deleted. Per-step eligibility is governed by the yaml:

- `release_marker_count >= cutover_at_count` (default 3) ⇒ `cutover_eligible: true`.
- R1.6 flips `tool_write_flag_default: true` and deletes the markdown path **only** for
  steps where `cutover_eligible == true`.
- A premature cutover (`release_marker_count < 3`) is HALT-blocked.

## 2. Migration set (RECONCILED — do NOT use the loose "12 sub-step" framing)

R1.4 comprises **11 genuine LLM tool-write migrations**, plus one deterministic-EXEMPT step,
plus one parity-only step:

| # | Step | Class | Schema+Template+Test | Dual-write flag (default False) | Parity status |
|---|------|-------|----------------------|---------------------------------|---------------|
| 1 | extract | genuine LLM | ✅ | `--tool-write-extract` | Y |
| 2 | extract_tdd | genuine LLM | ✅ | `--tool-write-extract-tdd` | Y |
| 3 | generate | genuine LLM (Contract #3 id-check) | ✅ | `--tool-write-generate` | Y |
| 4 | diff | genuine LLM | ✅ | `--tool-write-diff` | Y |
| 5 | debate | genuine LLM | ✅ | `--tool-write-debate` | Y |
| 6 | score | genuine LLM (Contract #8 registry-sourced) | ✅ | `--tool-write-score` | Y |
| 7 | merge | genuine LLM (Contract #3 id-check) | ✅ | `--tool-write-merge` | Y |
| 8 | spec_fidelity | genuine LLM (convergence PRESERVE) | ✅ | `--tool-write-spec-fidelity` | Y |
| 9 | test_strategy | genuine LLM | ✅ | `--tool-write-test-strategy` | Y |
| 10 | certify | genuine LLM (dynamic post-remediate; R1.3 CodeAssertion) | ✅ | `--tool-write-certify` | Y |
| 11 | validate_reflect | genuine LLM (validate pipeline) | ✅ | `--tool-write-validate-reflect` | Y |
| — | **wiring_verification** | **deterministic-EXEMPT** | N/A (no LLM, no markdown path) | none | N/A |
| — | **remediate** | **parity-only** (file-edit prompt, no roadmap-ID artifact) | param+flag only, no schema/render | `--tool-write-remediate` | Y (prompt byte-identity) |

**wiring_verification** is EXEMPT: `executor.py:1085` runs `run_wiring_analysis`/`emit_report`
(deterministic static analysis, no Claude subprocess) — already in the tool-write end-state,
no LLM markdown path to dual-write or cut over. Rationale: `r1-4-wiring-validation.txt` + Step 9.10.

**remediate** is parity-only: a file-edit-instruction prompt that emits no roadmap-ID-bearing
artifact; its gate artifact (`remediation-tasklist.md`) is written deterministically from
`Finding` objects. Only a `tool_write` prompt param + `--tool-write-remediate` flag + flag=False
byte-identity guarantee were added (no schema/template/render-hook; Contract #3 N/A). Step 9.11.d.

## 3. Per-step parity status (sourced from validation summaries)

All present validation summaries under `phase-outputs/test-results/r1-4-*-validation.txt` are
parity-PASSING. Full 12-file tool-write suite: **155/155 PASS** (re-verified on disk 2026-06-02
after concurrent-session reconciliation). Per-step `r1-4-*-validation.txt` present for: extract,
extract_tdd, generate, diff, debate, score, merge, spec_fidelity, wiring (N/A rationale), and
`r1-4-secondary-validation.txt` (test_strategy + certify + validate_reflect + remediation).

## 4. Per-step IF/ELSE eligibility (iterating the yaml)

For every entry in `.dev/migrations/r1-4-cutover-counters.yaml`:

```
IF release_marker_count >= cutover_at_count (3) AND parity passing:
    -> "ready for cutover"  (markdown path deletable in R1.6)
ELSE:
    -> "remain dual-write"
```

At authoring time **every** entry has `release_marker_count: 0` and `cutover_eligible: false`.
Therefore **every** step evaluates to **"remain dual-write"**. No exceptions, no premature cutover.

## 5. Overall R1.4 readiness verdict

**NOT READY FOR CUTOVER — markdown remains the production default.**

Reason: no release cycle has shipped any `--tool-write-<step>` path in production, so all
`release_marker_count == 0` (< 3 required by Vector A). "Ready for R1.5" does NOT require
cutover completion — it requires that all genuine migrations exist with passing parity tests in
dual-write mode, which IS satisfied (11/11 genuine migrations implemented + parity-green;
wiring EXEMPT; remediate parity-only). The cutover itself (flag-default flip + markdown deletion)
is correctly DEFERRED to R1.6 once the yaml's `release_marker_count >= 3` per step.

## 6. Honesty checklist (per item 9.12 "Ensuring")

- ✅ Honest about cycle count: ALL steps at 0 cycles (yaml is SoT; not re-narrated in prose).
- ✅ No premature cutover: every step "remain dual-write" (Vector A explicit).
- ✅ Readiness verdict grounded in the yaml: iterated all 13 entries, all `cutover_eligible: false`.
- ✅ Migration set reconciled to 11 genuine + wiring EXEMPT + remediate parity-only (not "12 sub-step").
- ✅ Markdown path remains production default until R1.6 cutover.
