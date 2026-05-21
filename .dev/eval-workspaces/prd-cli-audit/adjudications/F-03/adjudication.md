# F-03 Adjudication — `_tier_min_lines` / `_tier_min_lines_assembly` unwired

**Verdict**: REAL
**Convergence score**: 0.95 (three personas agree on existence; mild divergence on severity)
**Final severity**: HIGH (downgraded from preliminary CRITICAL)
**Fix difficulty**: LOW (≤30 LOC, localized to `gates.py` + one call site in `executor.py`)

---

## Evidence re-verification

| Claim | Re-verified | Result |
|---|---|---|
| `_tier_min_lines` defined at `gates.py:281-283` | yes (Read) | CONFIRMED — returns `{"lightweight":200,"standard":400,"heavyweight":600}.get(tier,400)` |
| `_tier_min_lines_assembly` defined at `gates.py:286-292` | yes (Read) | CONFIRMED — returns `{"lightweight":400,"standard":800,"heavyweight":1500}.get(tier,800)` |
| Zero call sites in src/ and tests/ | `grep -rn "_tier_min_lines"` | CONFIRMED — only the two `def` lines match; no callers anywhere |
| Executor reads `gate.min_lines` directly without tier transform | Read `executor.py:530`, `:587-609` | CONFIRMED — `gate = GATE_CRITERIA.get(step_id)` then `if gate.min_lines > 0: line_count < gate.min_lines` (`executor.py:596-598`) |
| `GATE_CRITERIA` is static (no runtime mutation) | `grep -rn "GATE_CRITERIA\["` and `GATE_CRITERIA *=` in src/ and tests/ | CONFIRMED — only the module-level definition at `gates.py:295` and read sites at `executor.py:40,382,530,685,864`. No assignment, no `.update()`, no monkeypatch in production code. |
| `build-task-file` hardcodes `min_lines=400` | Read `gates.py:367` | CONFIRMED, comment "default standard tier; callers override per tier" (override never built) |
| `assembly` hardcodes `min_lines=800` | Read `gates.py:459` | CONFIRMED, identical pattern |
| Tier reaches executor but is only consumed for agent counts | `grep "tier" executor.py` | CONFIRMED — `self._config.tier` is read at `executor.py:717,735` for `_research_step_count` / `_web_research_step_count`; never read in `_evaluate_gate` |
| F-F-5 witness: `test_e2e_lightweight_prd` passes with 80-line content under supposed 200 floor | Read `test_e2e.py:81-220, 323-354` | **PARTIALLY REFUTED** — `default_line_count=80` is the baseline, but `_make_passing_output` upgrades `build-task-file` to `effective_min = max(80, 400+10) = 410` and `assembly` to `≥810` (`test_e2e.py:88-106, 209`). The test does NOT exercise an 80-line build-task-file. The witness conflates the default baseline with the actual per-step content size. The bug is still real; the cited witness just does not prove it the way claimed. |

---

## Persona 1 — Analyzer (reproducibility)

The reproduction sketch in the finding is directionally correct but slightly miscalibrated.

**What concretely happens at runtime**:
1. User runs `superclaude prd run "..." --tier lightweight`.
2. CLI resolves `config.tier = "lightweight"` via `resolve_config()` (Click → models.py) — verified wired.
3. `PrdExecutor.__init__` stores `self._config`; uses `tier` only for agent-count fanout at `executor.py:717-738`.
4. At gate evaluation (`executor.py:530`), `GATE_CRITERIA["build-task-file"]` returns the frozen `GateCriteria(min_lines=400, ...)` regardless of tier.
5. `_evaluate_gate` (`executor.py:596`) compares `line_count < 400`. A lightweight build-task-file producing 250 lines fails STRICT and the pipeline HALTs (`executor.py:534-535`).

**User-visible signal**: gate_failures diagnostic message `"Insufficient lines: 250 < 400"` plus `Min lines: 250/400` in the log — surfaces in TUI as `gate_state=FAIL` and the pipeline halts on STRICT. So the bug is NOT silent on lightweight (over-strict path) — the user sees a hard failure with a misleading threshold.

**Where the bug IS silent**: heavyweight runs. A heavyweight build-task-file at 500 lines passes the 400-line floor when the contract demands 600. No signal — the pipeline reports success on under-sized output. Same for assembly at 1000 lines (passes 800 floor, should be 1500). This is the truly silent / latent failure mode.

**Reproduction (corrected)**:
- Lightweight over-strictness: `--tier lightweight` with a 250-line task file → HALT at build-task-file with `Min lines: 250/400` (visible failure, wrong floor).
- Heavyweight under-strictness: `--tier heavyweight` with a 450-line task file → PASS (silent, contract violated).

The mock E2E test does NOT catch either path because `_make_passing_output` is hand-tuned to standard-tier thresholds.

---

## Persona 2 — Refactorer (blast radius)

This is a recurring "tier-aware helper exists, consumer never reads it" pattern. Sibling instances:

1. **F-22 (EXEMPT/LIGHT enforcement_tier not recognized)** — `gates.py` declares four entries as `EXEMPT`/`LIGHT`, but `executor.py:531-540` only special-cases `STRICT`. Anything not `STRICT` is treated the same. Same shape as F-03: contract declared at gate definition, consumer ignores half the contract. Confirmed by reading the finding.

2. **`GateCriteria` field surface mismatch (latent)** — `GateCriteria` is a static dataclass; the comments "callers override per tier" at `gates.py:367` and `:459` indicate intended dynamism. No constructor accepts tier; no factory function exists. The architectural seam was specified in comments and stubbed with helpers but never bridged.

3. **Tier consumption asymmetry in executor** — `self._config.tier` is read for fanout (`executor.py:717-738`) but never for gate construction. The pipeline has two parallel tier-aware code paths, only one is wired. Pattern: "fanout tier-aware, gates tier-blind."

**Blast radius scope**:
- 2 specific gates affected today (`build-task-file`, `assembly`).
- Latent: any future `min_lines` knob added to a tier-sensitive step will inherit the same blind spot until the seam is built.
- Related to F-22: both are "GateCriteria contract declared but executor ignores part of it." A clean fix should refactor `_evaluate_gate` to consume the full GateCriteria contract (tier-aware min_lines + EXEMPT/LIGHT semantics) in one pass.

**Pattern tag**: P2 (dead code with declared intent) + P7 (architectural seam declared but unbuilt). Consistent with F-03's pattern tags.

---

## Persona 3 — Architect (severity calibration)

Preliminary CRITICAL needs downgrading. Calibration:

**Arguments for CRITICAL**:
- Spec/contract violation: tier knob is user-facing CLI flag; ignoring it silently violates the documented heavyweight/lightweight contract.
- Silent in the heavyweight direction (under-strict) — false PASS on contract-violating output is the worst signal class.

**Arguments against CRITICAL (for HIGH)**:
- Does not crash, corrupt state, leak data, or block the pipeline in any tier other than via the (visible, recoverable) lightweight HALT.
- Affects 2 of ~17 gates; not systemic across the pipeline.
- No production user impact today because the only tier with field telemetry is standard, where the hardcoded 400/800 happens to be correct.
- Fix is mechanical and local; no migration, no data backfill, no API break.
- Tests do not exercise it (test harness padding masks the bug), so there is no test-suite regression to manage.

**Arguments against HIGH (for MEDIUM)**:
- Discoverable via any real-world lightweight/heavyweight run.
- Per-tier gate thresholds are a load-bearing piece of the tier abstraction; if tiers are advertised as quality contracts, this empties two of the contracts.

**Calibration**: HIGH. The silence-in-heavyweight mode is the deciding factor (could produce false-pass PRDs that fail downstream consumers), but the bug is contained, mechanically simple, and does not block or corrupt. CRITICAL should be reserved for data loss, security, or full-pipeline-halt classes. This is "tier contract not honored on 2 gates" — serious, not catastrophic.

---

## Convergence — Synthesis

All three personas converge on REAL. The two helper functions exist at `gates.py:281-292`, have zero call sites in src/ and tests/ (grep-confirmed), and `GATE_CRITERIA` is constructed once at import with hardcoded standard-tier values that the executor reads directly via `gate.min_lines` at `executor.py:596` without any tier transform. `--tier` flows correctly through `PrdConfig.tier` and is consumed for agent fanout (`executor.py:717-738`) but never for gate construction — confirming the "wired to config, ignored at gate" trace. The defect manifests two ways: (a) visible over-strict HALT on lightweight builds where 250-line output is rejected against the 400-line floor, and (b) silent under-strict PASS on heavyweight builds where 500-line task files satisfy the 400 floor instead of the intended 600. F-F-5's witness (`test_e2e_lightweight_prd` at `default_line_count=80`) is partially refuted: the test fixture pads `build-task-file` to 410 lines via `_make_passing_output`, so it does not actually exercise an 80-line build-task-file — but this does not change the verdict, only the cited evidence. The pattern is a sibling of F-22 (declared GateCriteria contract ignored by executor's narrow consumer), suggesting a single refactor of `_evaluate_gate` to consume the full contract (tier-aware min_lines + EXEMPT/LIGHT semantics) would close both. Severity calibrates from preliminary CRITICAL to HIGH: the silent heavyweight false-pass is serious enough to warrant priority fixing but contained to 2 of ~17 gates with no crash, corruption, or block; fix difficulty is LOW (wire `_config.tier` into `_evaluate_gate` and call the existing helpers, ~30 LOC).
