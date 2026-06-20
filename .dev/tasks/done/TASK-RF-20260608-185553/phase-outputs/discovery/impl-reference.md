# Implementation Reference — `superclaude reflect run`

**Status:** In progress
**Date:** 2026-06-09
**Purpose:** Consolidated load-bearing facts for every later phase, extracted from the 8 research files (`research/01-..08-..md`) + driving spec (`.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md`). Each section names its source.

---

## 1. §6 Verdict → Exit Table (VERBATIM) — first-match-wins

**Source:** spec §6 (merged-requirements.md:77-83); grounded in research 08 §7.

The ordering is **blocked → degraded → halted → pass** (first match wins). The verdict function MUST evaluate these branches in EXACTLY this order:

| Order | Condition | verdict | exit |
|-------|-----------|---------|------|
| 1st | contract missing/unparseable, child crash, frontmatter unwritable, or preflight STOP | `blocked` | **2** |
| 1st | child rc==124 (timeout) | `blocked` (timeout) | **2** |
| 1st | `contract_version` missing OR unknown MAJOR (not `1`) | `blocked` (fail-loud) | **2** |
| 2nd | chain-critical degradation per FR-11 (degraded grounding / diversity / adversarial / verification / citations_dropped / input_drift) | `degraded` | **11** |
| 3rd | `status: partial`, OR `regression_present` / `unauthorized_deviation_present` / `needs_human_decision` / `user_decision_required` / `drift>0` / `regression>0` | `halted` | **10** |
| 4th (else) | `status: success` AND none of the above AND expected tier reached (`tier_reached==expected_tier`) | `pass` | **0** |

**Exit-code mapping (the `Verdict.exit_code` property):** `pass`→0, `halted`→10, `degraded`→11, `blocked`→2. `pass` is the ONLY exit-0 path (FR-8). This "mirrors reflect's own 9-condition promotion gate by reading its outputs, never recomputing them" (spec §6).

---

## 2. ClaudeProcess Construction Call Shape

**Source:** research 01 (process.py:24-68, §"Summary" point 2), spec §8 (merged-requirements.md:123-125).

**Import line:** `from superclaude.cli.pipeline.process import ClaudeProcess`

**Construction (ALL kwargs-only — bare `*` at process.py:39 rejects positional):**

```python
proc = ClaudeProcess(
    prompt=<the /sc:reflect slash invocation>,   # delivered via stdin (bypasses MAX_ARG_STRLEN)
    output_file=<output_dir>/reflect-stdout.json,
    error_file=<output_dir>/reflect-stderr.log,
    model=<non-empty resolved model>,            # MUST be non-empty (see below)
    timeout_seconds=3600,                         # MUST override (default is 6300)
    max_turns=<config.max_turns, default 250>,    # G1: MUST override (default is 100)
    output_format="stream-json",
    env_vars=None,                                # FR-10: bare real-env, no custom overlay
)
proc.start()
rc = proc.wait()    # returns child rc; returns 124 on TimeoutExpired (after SIGTERM→SIGKILL)
```

**Two (now THREE with G1) MUST-OVERRIDE defaults:**

1. **`timeout_seconds`** defaults to **6300** (process.py:46/61) — pass **3600** for NFR-5.
2. **`model`** defaults to **`""`** (process.py:44/59) which OMITS the `--model` flag entirely — pass a **non-empty** model so a specific model is forced.
3. **`max_turns`** (G1) defaults to **100** (process.py:43/58) — a Tier-2 reflect run can exceed 100 top-level turns → truncated contract → fail-closed HALT on the common path. Pass `max_turns=config.max_turns` (default 250, see OQ6).

**FR-10 env (research 01 §"build_env"):** `build_env(env_vars=None)` does `os.environ.copy()` then pops ONLY `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. It does NOT strip `HOME`/MCP vars/`ANTHROPIC_DEFAULT_*` aliases. So the wrapper needs NO custom env scrub — `env_vars=None` is exactly the FR-10 "bare real-env overlay." `build_env()` is a public, side-effect-free pure function of `os.environ` — safe to call standalone for FR-11 preflight alias counting. Do NOT use `HomeIsolation`/`ClaudeProcessAdapter` (it hermetically isolates HOME, stripping the MCP+alias vars Tier-2 depends on).

**Timeout contract (research 01 §"wait()"):** `wait()` returns **124** on `subprocess.TimeoutExpired` (after invoking `terminate()` = SIGTERM→10s→SIGKILL via process group). The wrapper maps rc==124 → `blocked`/timeout.

**Dry-run (FR-12):** `build_command()` (process.py:73) and `build_env()` (process.py:97) are public + side-effect-free — callable to print the exact argv WITHOUT launching. The prompt (stdin, not in argv) must be surfaced separately for a faithful dry-run preview.

---

## 3. The §8 Prompt String + WRAPPER-only Flags (must NOT appear)

**Source:** spec §8 (merged-requirements.md:119), research 08 §9/§1.1/§8.

**The single slash invocation the wrapper builds (delivered via stdin):**

```
/sc:reflect --mode post --no-promote --diff <BASE>..HEAD --tasklist <abs> [--spec <abs>] --depth <standard|deep> --executor-model <class> --output <abs-pinned-dir>
```

All flags above are **REAL reflect flags** (research 08 §1.1 confirms each):
- `--mode post` (REAL), `--no-promote` (REAL — hard flag, promotion is default-ON so omission = promotion-on; FR-9), `--diff <BASE>..HEAD` (REAL, UC-2 diff source), `--tasklist <abs>` (REAL), `--spec <abs>` (REAL, conditional — only when frontmatter `spec_path` resolves to one existing absolute file), `--depth standard|deep` (REAL — NEVER `quick` for POST), `--executor-model <class>` (REAL in SKILL body, undocumented in command table — still pass it), `--output <abs-pinned-dir>` (REAL — STOP if under `.claude/{skills,agents,commands}`).

**`--no-promote` handling:** emit `--no-promote` by DEFAULT. Drop it ONLY when `config.promote` is True (then reflect's own gated Wave-7 runs). `--promote` is NOT a reflect flag — opt-in promotion = DROP `--no-promote` from the prompt.

**WRAPPER-only flags that MUST NEVER appear in the prompt string** (research 08 §3/§8 — these are wrapper-side, not reflect flags; passing them would be unknown flags):
- **`--allow-single-vendor`** — modifies the wrapper's FR-11 routing only (suppresses `t2_vendor_diversity==single` → degraded).
- **`--timeout`** — maps to `ClaudeProcess(timeout_seconds=...)`, not a reflect flag.
- **`--dry-run`** — wrapper-local short-circuit (never launches reflect).
- **`--promote`** — maps to DROPPING `--no-promote` from the prompt (NOT a literal flag).

**Also NEVER pass** the debug fail-open flags (`--no-mcp`, `--no-evidence-validator`, `--no-verify`, `--no-doc-discovery`, `--tier`) — they would inject exactly the degradation FR-11 rejects. T2 is forced via `--depth deep`, NOT `--tier 2` (so the `zero-aliases-tier2-conflict` STOP is structurally unreachable).

**"POST never runs quick" is WRAPPER-enforced** (research 08 §3/§8.5): no reflect-internal floor exists; reflect would honor `--depth quick` → STOP at T1. The wrapper/builder must floor depth at `standard`.

---

## 4. FR-11 Degradation Routing Table (14 triggers) + HALT subset + NOT-halt exceptions

**Source:** research 08 §6 (the routing table), research 02 §2.2/§3, spec FR-11 (merged-requirements.md:31).

**Chain-critical `degraded_components` HALT subset (exact-membership, NOT substring):**
```
{"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}
```
Exact membership is required so benign fail-open tokens do NOT over-HALT: `search_deps:lsp_unindexed`, `serena:onboarding-parse`, `serena:pre-v1.5-no-rename-propagation`, `get_current_config`, `neighbour-search:auggie_unavailable` are NOT in the HALT set (research 02 §3, research 08 §8 item 7). `degraded_components` is §9.2 TELEMETRY (non-stable) — read defensively: absent → `[]` (no degradation); malformed → `blocked`.

**The 14 degradation triggers → `degraded` (research 08 §6):**

| # | Trigger | Contract field + degraded value | Block |
|---|---------|----------------------------------|-------|
| 1 | grounding loss: serena | `degraded_components` ∋ `"serena"` | §9.2 telem |
| 2 | grounding loss: auggie | `degraded_components` ∋ `"auggie"` | §9.2 telem |
| 3 | env-aliases lost | `degraded_components` ∋ `"env-aliases"` | §9.2 telem |
| 4 | evidence-validator gate lost | `degraded_components` ∋ `"evidence-validator"` | §9.2 telem |
| 5 | serena context-excluded | `degraded_components` ∋ `"serena:context-excluded"` | §9.2 telem |
| 6 | expected-T2 but ran T1 | `tier_reached == 1` while `expected_tier >= 2` | §9.1 |
| 7 | model-class diversity not full | `t2_model_class_diversity != "full"` | §9.1 |
| 8 | vendor diversity single | `t2_vendor_diversity == "single"` UNLESS `--allow-single-vendor` | §9.1 |
| 9 | adversarial merge unavailable | `adversarial_unavailable == True` | §9.1 |
| 10 | single-reviewer fallback | `merge_method == "single-reviewer-fallback"` | §9.1 |
| 11 | null convergence at T2 | `adversarial_convergence_score is None` AND `tier_reached == 2` | §9.1 |
| 12 | verification didn't run | `verification_ran == False` UNLESS exempted | §9.1 |
| 13 | citations dropped | `citations_dropped > 0` (sample-count field, NOT `_extrapolated`) | §9.1 |
| 14 | input drift | `input_drift_detected == True` | §9.1 |

**NOT-halt exceptions (research 08 §6.1 — must NOT route degraded):**
- **`serena_summary_corroboration: unavailable`** — EXPECTED cross-session (the wrapper always runs a fresh subprocess). Only `disagree` is a signal. Do NOT route `unavailable` to degraded.
- **`verification_ran == False` exemptions** — exempt when `verification_skip_reason ∈ {"read-only-project", "tool-unavailable", "--no-verify"}`. Route degraded ONLY when skip_reason is null/empty (ran-or-should-have-but-didn't).
- **`citations_dropped_extrapolated`** — recording-only, MUST NOT gate. Gate on `citations_dropped` (the sample count).
- **`onboarding_ran: false`** — onboarding is opt-in; normal, not degraded.

**T1-null guard (research 02 §6.2):** the T2 fields (`t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`) are only meaningful at `tier_reached >= 2`. At T1 they may be null/absent — that is NOT degradation (it's the expected T1 shape). Route on `merge_method` FIRST; guard null comparisons.

**HALTED vs DEGRADED (research 08 §7):** `degraded` = reflect LOST the structural machinery (diversity/grounding/adversarial/verification) → audit untrustworthy. `halted` = audit was TRUSTWORTHY (full T2) and FOUND deviations/partial. `blocked` = no usable audit at all.

---

## 5. contract_version Gating Rule

**Source:** research 02 §0/§6.4, research 08 §0, spec FR-5 (merged-requirements.md:25), §10.

- **Authoritative version:** `"1.3.0"` (quoted string) — SKILL.md §9.1 (`:654`/`:791`). The wrapper parses `<output>/return-contract.yaml`, NEVER the REPORT.md header (which lags at `1.2.0` — drift, ignore it).
- **`1.x` tolerant:** any `1.MINOR.PATCH` is forward-compatible. Minor bumps are additive-only; unknown top-level fields are read-and-ignored (NFR-8 / §9.4).
- **Unknown MAJOR → `blocked`:** if `contract_version` is missing OR its MAJOR component is not `1` (e.g. `2.0.0`), fail-loud → `blocked` (exit 2).
- **Field catalog:** every FR-5/FR-11 field lives in §9.1 (stable, 60+ fields). `degraded_components` lives in §9.2 (telemetry, non-stable — tolerate absence). `gate_evaluation` (11-field struct) is in `promotion-log.yaml`, NOT `return-contract.yaml` — the contract carries `promotion_*` scalars instead (irrelevant; wrapper does not promote).

---

## 6. Open Questions + Recommended Defaults (FLAG each in Task Log)

**Source:** task file ## Open Questions section; research 04 §2d (OQ1), research 05 §2/§6.3 (OQ5), research 08 (OQ3), pre-execution audit REPORT.md (OQ6/OQ7).

| OQ | Topic | Recommended default (applied where) |
|----|-------|--------------------------------------|
| **OQ1** | Base branch for `git merge-base` (LOAD-BEARING) | Make base branch a config param defaulting to **`master`** (`_DEFAULT_BASE_BRANCH = "master"`), NEVER hardcode `integration` (origin/HEAD→master). Phase 2 Step 2.2. |
| **OQ2** | `--executor-model` source seam | Read `EXECUTOR_MODEL_CLASS` env FIRST, fall back to frontmatter field if present, else omit (`None`). Phase 2 Step 2.2. |
| **OQ3** | `--remediate` flag | Do NOT pass `--remediate` (wrapper is audit-only by default, FR-9). Phase 3 Step 3.5. |
| **OQ4** | chdir / cwd | No chdir; runner documents it MUST be invoked from repo root (the tasklist's own worktree) so `--diff` resolves. `ClaudeProcess` has no `cwd` param; child inherits parent cwd. |
| **OQ5** | `deviations` serialization shape | Block style via `default_flow_style=False` (yamllint-clean, round-trips). Phase 3 Step 3.2. |
| **OQ6** | `max_turns` ceiling (LOAD-BEARING, G1) | `_DEFAULT_MAX_TURNS = 250` (config layer); pass `max_turns=config.max_turns` to `ClaudeProcess`. NO `--max-turns` CLI flag (keeps §9 option set exact). Phase 2 Step 2.2 / Phase 3 Step 3.5. |
| **OQ7** | `--resume` behavior (IMPORTANT, G2) | Implement skip-on-clean-HEAD short-circuit in `ReflectRunner.run`: if `reflect_post.head == config.head` AND prior `verdict == "pass"`, skip launch and exit 0 (reason `resume-clean-head`). NOT a declared-but-inert flag. Phase 3 Step 3.5; tested Phase 6 Step 6.5. |

---

## 7. Module Dependency Order + Isolation Guardrails

**Source:** research 03 (CLI package map), spec §8/§10.

6-file package under `src/superclaude/cli/reflect/`:
- `models.py` — dataclasses (`ReflectConfig`, `ReflectResult`) + `Verdict(str, Enum)`. Depends on nothing in-package (types only).
- `config.py` — `resolve_config()` (input derivation + preflight ValueErrors). Depends ONLY on `.models`.
- `contract.py` — ISOLATED verdict map (§6) + FR-11 routing + version gating. Depends ONLY on `.models` + stdlib + PyYAML. MUST NOT import `commands.py`/`runner.py`/`config.py` (Risk §10).
- `runner.py` — thin orchestrator (derive → preflight → build prompt + ClaudeProcess → launch → parse → derive verdict → write-back + sidecar). Depends on `config`, `contract`, `models`.
- `commands.py` — Click group `reflect_group` + `run` command. Lazy-imports config/runner in body.
- `__init__.py` — re-exports.

`cli/main.py` registration: deferred import + `main.add_command(reflect_group, name="reflect")` after `init-lite`, before `if __name__ == "__main__":`.

**NFR-1 thinness:** ≤ ~400 LOC total package; zero reflect-logic duplication (no deviation-taxonomy/tier-rubric strings authored in Python — only contract field reads).

**Status:** Complete
