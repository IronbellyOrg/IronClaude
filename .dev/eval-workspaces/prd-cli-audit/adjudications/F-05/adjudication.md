# Adjudication — F-05: Dynamic step IDs not matched by static GATE_CRITERIA keys

**Finding source:** `.dev/eval-workspaces/prd-cli-audit/findings/F-05-dynamic-step-ids-unmatched-gate-keys.md`
**Files re-verified (this turn):**
- `src/superclaude/cli/prd/executor.py:40, 366-367, 382, 510-552, 631-673, 707-762, 855-891, 976-1004`
- `src/superclaude/cli/prd/gates.py:295-449`

---

## Re-verification (factual)

1. **Dynamic step IDs are minted with numeric suffixes.**
   - `executor.py:727` → `step_id = f"investigation-{i + 1}"`
   - `executor.py:745` → `f"web-research-{i + 1}"`
   - `executor.py:757` → `f"synthesis-{i + 1}"`
   - `executor.py:886` → `f"{qa_step_id}-fix-{cycle + 1}"` (fix-cycle steps)

2. **`GATE_CRITERIA` keys at gates.py:407, 426, 432 are static and bare** — `"investigation"`, `"web-research"`, `"synthesis"` — no numeric suffix, no `*-N` pattern, no callable.

3. **Gate lookup is exact-match, no fallback.** The single call site at `executor.py:530`:
   ```python
   gate = GATE_CRITERIA.get(step_id)
   if gate and status.is_success:
       gate_passed = self._evaluate_gate(step_id, gate, gate_content)
   ```
   For `step_id="investigation-1"`, `.get()` returns `None`; the `if gate` branch is skipped entirely. No `startswith`, no rsplit-on-`-`, no normalizer was found by grep on the executor module.

4. **Other lookup sites confirm same shape.**
   - `executor.py:382` — Stage A gate-failure check (works; Stage A IDs are static).
   - `executor.py:685` — explicit `GATE_CRITERIA.get("assembly")` (literal key, works).
   - `executor.py:864` — `GATE_CRITERIA.get(qa_step_id)` for STRICT-halt logic; `qa_step_id` is `"research-qa"` or `"synthesis-qa"` (literal, works). **But** when the fix-cycle step itself (`research-qa-fix-1`) runs at line 885, its gate lookup at line 530 misses (no `*-fix-N` key in `GATE_CRITERIA`).

5. **Persistence-gap claim confirmed.** `_persist_step_artifact` at executor.py:987 does `_STEP_ARTIFACT_FILES.get(step_id)`; if the dict keys are also static (same shape as `GATE_CRITERIA`), dynamic step IDs would miss persistence too. The finding's note that this method "silently does nothing for these step IDs" is consistent with the exact-match lookup pattern, though the underlying dict was not opened here.

6. **TUI-gap claim confirmed.** `executor.py:366-367` registers only `_STAGE_A_STEPS`; no parallel registration for the dynamically-built Stage B step IDs.

---

## Persona 1 — Analyzer (reproducibility)

**User-visible symptom:** Stage-B agents (`investigation-1..N`, `web-research-1..N`, `synthesis-1..N`) and every fix-cycle step (`research-qa-fix-1`, `synthesis-qa-fix-1`, ...) **silently bypass gate evaluation**. Failure mode is silent, not noisy:

- `_execute_step` at executor.py:530 fetches `gate = None`.
- The `if gate and status.is_success:` guard is falsy → no `_evaluate_gate` call → no `min_lines` check → no semantic-check → no TUI gate-state update → no HALT/VALIDATION_FAIL escalation.
- Status falls through to `PASS` or `PASS_NO_SIGNAL` based purely on subprocess exit + sentinel (executor.py:570-585).

**Reproduction:** the sketch in the finding (printing `gate` after the `.get`) is correct and minimal. A `synthesis-3` step that produces a 5-line stub would satisfy `exit_code == 0`, hit no HALT sentinel, classify as `PASS_NO_SIGNAL`, and march downstream. The `min_lines=80` gate at gates.py:432 never runs against it.

**Fix-cycle bucket:** same silent-pass behavior. The fix-cycle step's own gate is missed at executor.py:530. The QA's STRICT-halt check at executor.py:864 still works (it looks up `qa_step_id`, which is the literal `"research-qa"` or `"synthesis-qa"`), so a failing QA verdict can still halt — but the **fix-cycle agent's output itself is never gated**, so a stub-output gap-filler can pass through to the re-QA round.

**Reproducibility verdict:** trivial to reproduce; no environmental dependencies; deterministic given any Stage-B execution.

---

## Persona 2 — Refactorer (blast radius)

**Affected dynamic step families (by tier):**

| Family | Pattern | Per-tier count | Total per run |
|---|---|---|---|
| `investigation-{1..N}` | executor.py:727 | lightweight=3, standard=5, heavyweight=8 | 3–8 |
| `web-research-{1..N}` | executor.py:745 | lightweight=1, standard=2, heavyweight=3 | 1–3 |
| `synthesis-{1..N}` | executor.py:757 | = `len(load_synthesis_mapping(...))` | typically several |
| `research-qa-fix-{1..N}` | executor.py:886 | up to `max_research_fix_cycles` | 0–N |
| `synthesis-qa-fix-{1..N}` | executor.py:886 | up to `max_synthesis_fix_cycles` | 0–N |

For a standard-tier run with no fix cycles: **5 investigation + 2 web-research + K synthesis ≈ 10+ ungated agent invocations per PRD pipeline run.** Heavyweight is worse (8 + 3 + K). With fix cycles, the count grows.

**Accidental-match check:** I cross-walked every dynamic ID shape against the 17 static keys in gates.py:295-449.
- No key in `GATE_CRITERIA` matches a hyphen-N suffix pattern.
- The closest literal collisions (`"research-qa"`, `"synthesis-qa"`) are looked up directly via the QA-orchestration path at executor.py:864 *before* the fix step runs, so those literal keys are reachable and not affected.
- No dynamic family accidentally lands on a static key. The gap is uniform.

**Sibling gaps:** the finding correctly identifies two adjacent breakages with the same root cause (exact-match dict lookup on a synthetic key):
- `_persist_step_artifact` at executor.py:987 — same `.get(step_id)` shape on `_STEP_ARTIFACT_FILES`.
- TUI registration at executor.py:366-367 — Stage-B steps never enter the TUI step list, so progress/gate visualization for the largest chunk of work is absent.

The fix touches three call sites with the same normalization need; not a sprawling refactor but more than a one-line patch.

---

## Persona 3 — Architect (severity calibration)

**Quality-enforcement intent vs. reality.** The `GATE_CRITERIA` table is the project's declarative content-quality contract — `min_lines`, `required_frontmatter_fields`, `semantic_checks`, and the STRICT/STANDARD/LIGHT escalation ladder. Investigation/web-research/synthesis are the **content-production phase** of the PRD pipeline; gating them is precisely where quality enforcement matters most (a stub `synthesis-3.md` poisons the final assembly).

**What the bug downgrades:**
- `synthesis` gate (gates.py:432, STANDARD, `min_lines=80`) — never fires per-agent.
- `investigation` gate (gates.py:407, STANDARD, `min_lines=50`) — never fires per-agent.
- `web-research` gate (gates.py:426, STANDARD, `min_lines=30`) — never fires per-agent.

These are STANDARD-tier (degrade-to-VALIDATION_FAIL, don't halt), so even when working they wouldn't HALT the run — but they would still mark gate state, prevent silent quality regressions in the per-step record, and feed downstream visibility. With the bug, they're inert.

**Compensating controls:** the QA steps (`research-qa`, `synthesis-qa`) at gates.py:413, 438 *do* still fire as literal lookups, and they have STRICT enforcement with semantic verdict checks. So content can still be caught at the QA aggregation layer — but only if the QA agent does its job correctly. The per-agent gates were designed as the first line of defense; that defense is currently absent.

**Severity calibration:** Preliminary HIGH stands. Not CRITICAL because:
- STRICT-tier QA gates downstream still execute and can catch aggregate quality failures.
- Pipeline doesn't crash; it just under-enforces.
Not MEDIUM because:
- Affects every Stage-B run (100% reproducibility).
- Hits the declared quality-enforcement contract for the most expensive phase of the pipeline.
- Silent — no logs, no warnings, no metrics indicate the bypass.
- Compounds with the persistence-gap and TUI-gap siblings.

**HIGH** is the right calibration.

---

## Convergence

| Field | Value |
|---|---|
| **Verdict** | **REAL** |
| **Convergence score** | **0.98** (three personas independently verified the same root cause; finding's evidence reproduced line-for-line) |
| **Final severity** | **HIGH** |
| **Fix difficulty** | **LOW-MEDIUM** — single root cause (exact-match dict lookup on synthetic IDs) with three call sites needing the same fix. Options: (a) introduce a `_normalize_step_id(step_id) -> base_key` helper that strips trailing `-N` and `-fix-N`, apply at the three `.get()` sites (executor.py:530, 987, plus TUI registration logic); or (b) convert `GATE_CRITERIA` lookup into a function that handles dynamic families. Option (a) is smaller. Risk: ensure `"research-qa"` and `"synthesis-qa"` literal keys aren't accidentally normalized away — easy to guard with an "only strip if trailing token is purely numeric" rule. Estimated 30–60 lines incl. unit tests. |

### Synthesis

F-05 is a real, deterministic, silent quality-enforcement gap. Stage-B's dynamic step IDs (`investigation-N`, `web-research-N`, `synthesis-N`, `*-fix-N`) never match any key in the static `GATE_CRITERIA` dict because the lookup at executor.py:530 is exact-match with no normalizer or prefix fallback. The result is that 6–14+ content-production agents per run — exactly the steps the STANDARD-tier `min_lines` gates at gates.py:407/426/432 were written to protect — bypass gate evaluation entirely and are recorded as `PASS` or `PASS_NO_SIGNAL` regardless of output quality. The sibling persistence-gap (`_persist_step_artifact` at executor.py:987) and TUI-registration gap (executor.py:366-367) share the same root cause and should be fixed together. STRICT downstream QA gates partially compensate but do not substitute for per-agent enforcement. Severity: HIGH. Fix difficulty: LOW-MEDIUM, single normalizer plus three call-site updates.
