# Phase Gate 3 — Consolidated Findings (WS-A)

**Status: Complete**
**Date:** 2026-06-16
**Consolidated verdict: FAIL** (delegation-clarity + line-budget reported issues)

## Per-lens verdicts

| Lens | Verdict | Issues |
|------|---------|--------|
| structural / line-budget-and-script-free | PASS (79 lines, 0 t2_ refs) | flagged the L10 scripts-retired claim (IMPORTANT) |
| structural / contract-preservation | PASS | 3 MINOR observability-field reductions (acceptable) |
| structural / CLI-flag-accuracy | PASS | none (8/8 flags real; 5 undocumented flags intentionally omitted) |
| content / delegation-clarity | **FAIL** | C1 (CRITICAL), C2 (CRITICAL), C3 (IMPORTANT) |
| content / release-notes-accuracy | PASS | 1 MINOR (MIG-003/TEST-003 vs WS-C ID-vocabulary cosmetic) |
| content / mirror-parity | PASS | src↔mirror byte-identical (sha256 match), verify-sync exit 0 |

## Consolidated issues (all in `src/superclaude/skills/sc-bare-review/SKILL.md`)

### C1 — IMPORTANT/CRITICAL — premature "scripts retired" claim
- **Lenses:** line-budget (IMPORTANT), delegation-clarity (CRITICAL)
- **Detail:** SKILL.md L10 meta comment states "legacy bundled scripts **retired**" (present tense), but `scripts/t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py` are still on disk — deletion is WS-C (Phase 5), not yet done. This is exactly the false-attestation pattern the whole migration corrects.
- **Fix:** reword to future-gated — "legacy bundled scripts retired in WS-C of the corrective task" — matching the release-notes-v1.md:16 phrasing. **FIX NOW.**

### C2 — CRITICAL — `--c7*` mapping ambiguity (would-error reading)
- **Lenses:** delegation-clarity
- **Detail:** SKILL.md L31 places "(`--c7*` accepted but no-op)" inside the sentence mapping caller flags onto `swarm run` flags, which reads as if `swarm run` accepts `--c7` — it does NOT (no such option, no `ignore_unknown_options`), so passing `--c7` to the CLI would error. `--c7*` are SKILL-level inputs the caller may pass to `Skill sc-bare-review`; the skill IGNORES them and does NOT forward them to `swarm run`.
- **Fix:** move the `--c7*` note out of the swarm-flag-mapping clause and state explicitly that `--c7*` are accepted at the skill boundary but NOT forwarded to the CLI (no-op). **FIX NOW.**

### C3 — IMPORTANT — `T2Timeout` wrongly in the required-STOP env list
- **Lenses:** delegation-clarity
- **Detail:** SKILL.md L32 says the swarm preflight "requires the T2 proxy env contract (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`/`T2Timeout`) and STOPs naming any missing var." Verified against `transports/openai_compat.py:173-174`: `TransportEnvError` fires only for `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`. `T2Timeout` is the `--timeout-sec` default (180), NOT a STOP-required var. L61 (failure table) already lists only the three. L32 contradicts L61 and the code.
- **Fix:** drop `T2Timeout` from the required-STOP env list on L32 (keep the three). **FIX NOW.**

## Informational (not fixed)
- N1: contract YAML omits `model_label`/`bytes`/`elapsed_ms`/`target_truncated` per-file fields and compresses the failure table 13→5 rows — acceptable thin-caller compression; none is a caller-facing behavioral guarantee (contract-preservation lens).
- N2: release-notes uses "WS-C / CLI-vs-frozen-golden parity" while L318-321 uses "MIG-003 / TEST-003 A/B parity" — cosmetic ID-vocabulary divergence, not a state contradiction (release-notes-accuracy lens).
- N3: `docs/swarm/release-notes-v1.md` shows as a modified tracked file — expected (Step 3.4 reconcile), not drift (mirror-parity lens out-of-scope observation).

## Fix-application note
Fixes applied DIRECTLY by the orchestrator (single serialized editor — I20 intent preserved), as in PG2. All three are precise SKILL.md wording corrections the orchestrator authored; the independent PG3.5 verification round supplies the independence check.
