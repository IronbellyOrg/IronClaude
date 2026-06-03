# R4 — Area C: opus-architect Template-Section Adherence + Spec-Fidelity Step Performance

**Status:** Complete
Date: 2026-06-03
Researcher: R4
Scope: `src/superclaude/cli/roadmap/{models.py,commands.py,prompts.py,executor.py,fidelity_checker.py,convergence.py,semantic_layer.py}`
Priority: Low (partly DIAGNOSTIC)

## Mandate

Determine what is concretely actionable NOW vs investigation-only for:
- opus-architect template-section adherence
- spec-fidelity step performance (one ~1192s sub-agent timeout in live E2E)

---

## 1. AgentSpec / opus:architect — CONFIRMED

`opus-architect` is NOT an agent `.md` file. It is `AgentSpec(model="opus", persona="architect")`.

- **Dataclass**: `models.py:63-90` — `AgentSpec` with fields `model: str`, `persona: str`.
- **Parse**: `models.py:74-85` — `AgentSpec.parse("opus:architect") -> AgentSpec("opus","architect")`; a bare `"opus"` defaults persona to `"architect"` (`models.py:85`).
- **Filename slug**: `models.py:87-90` — `.id` property returns `f"{self.model}-{self.persona}"` → `"opus-architect"`. This becomes the step id `generate-opus-architect` (`executor.py:2516`) and thus the output filename slug.
- **Default generate agent (CLI)**: `commands.py:434` `default="opus:architect"` (help text `commands.py:437` confirms "single-agent for cost efficiency"). The dataclass default pair is `[opus:architect, sonnet:architect]` (`models.py:102-107`).
- **Where model/persona spawns the sub-agent**:
  - `persona` → flows into the PROMPT TEXT only. `build_generate_prompt` (`prompts.py:996-1068`) injects `agent.persona` into `"You are a {agent.persona} specialist..."` (L1027), `primary_persona: {agent.persona}` frontmatter directive (L1058), and `"Apply your {agent.persona} perspective..."` (L1067). The persona is a pure prompt role-instruction; it has NO effect on the model binary selected.
  - `model` → flows to the subprocess. Step constructed with `model=agent_a.model` / `model=agent_b.model` (`executor.py:2530, 2549`). At spawn (`executor.py:1181-1192`) `ClaudeProcess(... model=step.model or config.model ...)` — the per-step `model` (`"opus"`) is passed to `claude -p --model` directly (no resolution; see `models.py:67-68` docstring).

---

## 2. Template-Section Adherence — PROMPT + GATE (two-layer), NOT prompt-only

The generate step runs in tool-write mode when a template is present: `tool_write_mode=_roadmap_template is not None` and `template_path=_roadmap_template` (`executor.py:2531-2532, 2550-2551`). Template resolved via `get_template_path(ROADMAP_TEMPLATE)` (`executor.py:2451`).

### Layer A — Prompt-side enforcement (advisory)
- `wrap_for_incremental_write` (`prompts.py:492-555`) embeds the full template inline as `---BEGIN/END OUTPUT TEMPLATE---` and instructs: use template as "required structural skeleton" (L519), write section-by-section via Write/Edit (L521-525), and self-verify all `{{SC_PLACEHOLDER:` sentinels are replaced (L527-528).
- `_TEMPLATE_STRUCTURE_DIRECTIVE` (`prompts.py:465-477+`) is appended in the markdown (non-tool-write) path (`prompts.py:1055-1056`). It names the `## M{N}:` milestone format, the 9-column deliverable table, and the required top-level H2 sections. **Note:** in tool-write mode this directive is NOT appended (`prompts.py:1052-1056`) — the embedded template + schema are expected to carry structure instead.

### Layer B — GATE-side enforcement (binding, deterministic)
`GENERATE_A_GATE` (`gates.py:1136-1185`, `GENERATE_B_GATE` aliases it at `gates.py:1191`) is `enforcement_tier="STRICT"` and runs semantic checks that DIRECTLY validate template adherence:
- `template_sections_present` (`gates.py:1170-1183`) — fails if any required top-level H2 (Executive Summary, Milestone Summary, Dependency Graph, Resource Requirements and Dependencies, Risk Register, Success Criteria and Validation Approach, Decision Summary, Timeline Estimates) is missing, or if no `## M{N}:` milestone with its required subsections exists.
- `no_template_sentinels` (`gates.py:1165-1169`) — fails if any `{{SC_PLACEHOLDER:*}}` remains.
- `deliverable_table_schema` (`gates.py:1160-1164`) — enforces the exact 9-column header.
- `minimum_deliverable_rows` (`gates.py:1155-1159`) — granularity floor of 20 rows.

**Verdict on adherence**: It is NOT prompt-only. There is a hard STRICT gate that fails the step (and triggers retry, `retry_limit=1`) when the opus-architect output drifts from the template's section skeleton. `gates.py` is OUTSIDE R4's edit scope but is load-bearing context.

### Where adherence could still drift (residual risk)
- The gate checks section PRESENCE and the table HEADER schema; it does NOT check per-section semantic completeness or per-row field-level fidelity (that is the spec-fidelity step's job — `prompts.py:1059-1064` "FIELD-LEVEL FIDELITY" is prompt guidance, not a generate-gate check).
- Drift between `_TEMPLATE_STRUCTURE_DIRECTIVE`'s named sections (`prompts.py:465-477`) and `template_sections_present`'s named sections (`gates.py:1170-1183`) is a maintenance hazard: two hardcoded section lists that must stay in sync. They currently agree, but a template change touches the `.j2`, the prompt directive, AND the gate list — three places. This is the only concrete "hardening" candidate in scope, and it is a refactor/dedup, not a bug fix.

---

## 3. Spec-Fidelity Performance / the 1192s Timeout — ROOT CAUSE IDENTIFIED

### The timeout inventory
- generate: `timeout_seconds=900` (`executor.py:2526, 2545`), `retry_limit=1`
- spec-fidelity: `timeout_seconds=600` (`executor.py:2676`), `retry_limit=1`
- debate/merge: 600; most others 300; extract 1800 for TDD input (`executor.py:2507`)

The observed **1192s EXCEEDS both 900 and 600**. A single ClaudeProcess step CANNOT run 1192s: the subprocess timeout is enforced at `executor.py:1188` (`timeout_seconds=step.timeout_seconds`) and yields exit 124 → `StepStatus.TIMEOUT` (`executor.py:1213-1221`). So 1192s is NOT a single step's process wall-clock.

### Root cause: convergence mode bypasses the step-level timeout
Convergence is **default-ON** (`commands.py:362` `"convergence_enabled": not no_convergence`; flag is `--no-convergence`, default off → enabled). When the step id is `spec-fidelity` and `convergence_enabled` is True, the executor short-circuits BEFORE building any ClaudeProcess:

```
executor.py:1068-1073
if step.id == "spec-fidelity" and config.convergence_enabled:
    return _run_convergence_spec_fidelity(step, config, started_at)
```

`_run_convergence_spec_fidelity` (`executor.py:1533-1712`) runs `execute_fidelity_with_convergence(... max_runs=3 ...)` (`executor.py:1693-1702`) **synchronously, with NO wall-clock cap derived from `step.timeout_seconds`**. The `timeout_seconds=600` on the spec-fidelity Step is therefore DEAD in convergence mode — it is only consulted on the single-shot path (which convergence never reaches). This is the structural reason 1192s > 600 is even possible.

> **Spec-fidelity Step gate shape — LIVE form (DO NOT encode the deleted `gate=None if convergence_enabled` bypass).** [CODE-VERIFIED] The R1.6 cleanup (commit `17b8ee94`, on this branch) **DELETED** the old `gate=None if convergence_enabled` bypass. The spec-fidelity `Step(...)` now unconditionally sets **`gate=SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`** (`executor.py:2675`; the deletion is documented in the in-line comment at `executor.py:2666-2674` — "the `gate=None if convergence_enabled` bypass is DELETED. Both modes now use the convergence-aware gate"). The gate constant is defined at `gates.py:1363` (`SPEC_FIDELITY_GATE_CONVERGENCE_AWARE = GateCriteria(...)`) and wired into `STEP_GATES` at `gates.py:1578` (`("spec-fidelity", SPEC_FIDELITY_GATE_CONVERGENCE_AWARE)`). Both convergence and `--no-convergence` modes now run this same gate (in convergence mode it validates the terminal report frontmatter + carries the runtime `convergence_passed` CodeAssertion; in non-convergence mode `envelope.convergence is None` so the assertion vacuously passes). The latency analysis above is unaffected — only the gate-shape description is corrected so the builder does not encode the deleted `gate=None` form.

### What drives the latency (compounding inner LLM calls)
Each convergence run calls `_run_checkers` (`executor.py:1590-1636`), which invokes:
1. `run_all_checkers` (structural; non-LLM, cheap).
2. `run_semantic_layer` (`semantic_layer.py:413`) via `claude_process_factory=lambda: _ClaudeRunner(config)` (`executor.py:1607`). Each `_ClaudeRunner.run` spawns a fresh `ClaudeProcess` at **`timeout_seconds=300`** (`executor.py:1514-1521`) — the convergence inner-call cap, NOT 600.
3. For each semantic HIGH finding, `validate_semantic_high` (`semantic_layer.py:570-638`) runs a prosecutor+defender adversarial debate = **2 parallel `_ClaudeRunner` LLM calls** (`semantic_layer.py:634-638`), each up to 300s.
4. `run_fidelity_check` (`fidelity_checker.py`, via `executor.py:1623`) — codebase-evidence scan.
Then `_run_remediation` (`executor.py:1638-1691`) may invoke `execute_remediation` (a further LLM-backed patch loop) on active HIGH findings.

With `max_runs=3` convergence loops, and per-run = (1 semantic batch call + N debate-pair calls + remediation), the inner 300s calls accumulate. **1192s ≈ four sequential ~300s inner LLM calls** (e.g., 2 convergence runs each with a semantic call + one debate pair, plus a remediation call). The 1192s is the SUM of inner `_ClaudeRunner`/remediation calls inside one convergence-mode spec-fidelity step, NOT one model invocation.

### `build_spec_fidelity_prompt` is largely NOT on the hot path in convergence mode
`build_spec_fidelity_prompt` (`prompts.py:1806-1885+`) builds the single-shot comparison prompt. The Step still passes it (`executor.py:2658-2664`) but in convergence mode it is **never sent** — convergence uses the semantic-layer prompts (PROSECUTOR/DEFENDER templates in `semantic_layer.py`) instead. So tuning `build_spec_fidelity_prompt` would NOT reduce the 1192s on a convergence run; it only affects `--no-convergence` runs.

### Latency drivers summary
- **Primary**: convergence `max_runs=3` × per-run inner LLM calls (semantic batch + per-HIGH 2× debate + remediation), each capped at 300s but summing unbounded vs the step's nominal 600.
- **Secondary**: input size — semantic layer reads full spec+roadmap sections (`executor.py:1599-1600`); larger roadmaps → more sections → more/longer batch calls.
- **Model**: inner calls use `config.model` (`executor.py:1519`), NOT necessarily opus (the convergence runner is config-model, not agent-model).

---

## 4. Candidate Fixes — Actionable-Now vs Investigation-Only

| # | Candidate | Safe/Deterministic? | Verdict |
|---|-----------|---------------------|---------|
| a | **Bump generate `timeout_seconds` (900→higher)** at `executor.py:2526,2545` | SAFE, deterministic, surgical (two literal edits) | **Actionable NOW** — but ONLY hardens the *generate* step. It does NOT address the 1192s, which is a convergence-mode spec-fidelity event, not a generate timeout. Low-value for the reported symptom; defer unless generate timeouts are independently observed. |
| b | **Bump spec-fidelity `timeout_seconds` (600→higher)** at `executor.py:2676` | Deterministic edit, but **INERT in convergence mode** | **Investigation-only / trap.** This literal is dead on the default (convergence) path (§3). Editing it gives a false sense of a fix while changing nothing for the observed run. Do NOT add as a "fix" item without a note that it only affects `--no-convergence`. |
| c | **Add a wall-clock cap to the convergence path** (derive a budget from `step.timeout_seconds` and enforce it across `execute_fidelity_with_convergence` / `_run_convergence_spec_fidelity`) | NOT safe-trivial — touches the convergence control loop and likely `convergence.py` | **Investigation-only.** This is the *correct* structural fix for "1192s > 600" but it (i) requires design (graceful partial-convergence vs hard abort), and (ii) `convergence.py` is a PRESERVE/byte-untouched file (§5). High blast radius. Documented follow-up, not a task item. |
| d | **Reduce spec-fidelity / semantic-layer input** (cap sections, batch, or compress before the semantic call) | NOT safe-trivial — changes `semantic_layer.py` behavior + finding fidelity | **Investigation-only.** Genuine latency lever (§3 secondary driver) but `semantic_layer.py` is PRESERVE/byte-untouched (§5) and reducing input risks missing deviations. Needs measurement first. |
| e | **Lower convergence inner-call timeout (300→lower) or `max_runs` (3→2)** at `executor.py:1521` / `executor.py:1699` | Deterministic edits | **Investigation-only.** Directly bounds worst-case latency, but trades off convergence quality (fewer remediation rounds / truncated semantic calls). Requires a quality-vs-latency decision + E2E re-measure. Not blindly safe. |
| f | **Template-adherence hardening — dedup the section list** between `_TEMPLATE_STRUCTURE_DIRECTIVE` (`prompts.py:465-477`), `template_sections_present` (`gates.py:1170-1183`), and the `.j2` template | Refactor; deterministic but cross-file (one file is out of scope) | **Actionable NOW (small) but LOW priority.** No active bug — the lists currently agree. Value is future-drift prevention. Worth a single task item ONLY if the task is already touching these files; otherwise a documented follow-up. |
| g | **Generate prompt template instruction** — the prompt already embeds the template + the STRICT gate enforces sections (§2). | n/a | **No action.** Adherence is already two-layer enforced. No gap to close here. |
| h | **Model/persona change** (e.g., opus→sonnet for generate, or change inner convergence model) | Config/CLI change | **Investigation-only.** A model swap affects cost, latency, AND output quality simultaneously; cannot be evaluated without A/B data. Out of scope for a deterministic task. |

### Recommended CONCRETE change set (for the task file)
**The single highest-confidence, in-scope, deterministic item:** NONE of the candidates is both (a) a real fix for the 1192s AND (b) safe + PRESERVE-respecting. The 1192s root cause (convergence bypasses the step timeout, candidate c) lives behind a PRESERVE boundary.

Therefore the concrete task recommendation is:
1. **Investigation/diagnostic item (primary)**: Document the convergence-timeout-bypass finding (§3) as the explanation for the 1192s. Add an explicit note in the spec-fidelity Step (`executor.py:~2666-2676`, comment-only, no behavior change) that `timeout_seconds=600` is INERT under `convergence_enabled` and the real budget is `max_runs × inner-300s` calls. This is a SAFE comment edit that prevents the next engineer from "fixing" it via candidate (b).
2. **Optional small item (f)** — only if in scope: extract the required-section list into ONE shared constant consumed by both the prompt directive and the gate, eliminating the 2-place (3 with `.j2`) drift hazard. Note `gates.py` is outside R4's stated scope, so this likely belongs in a separate follow-up.
3. **Documented follow-up (NOT task items)**: candidates (c), (d), (e) — the genuine latency fixes — require design + measurement + crossing the PRESERVE boundary. Capture as an "investigation: bound convergence spec-fidelity latency" follow-up.

Reject as task items: (a) wrong target, (b) inert/trap, (g) already done, (h) needs A/B data.

---

## 5. PRESERVE Constraints — MUST NOT CHANGE

- **`convergence.py` and `semantic_layer.py` are PRESERVE / byte-untouched** in the R1.4 dual-write effort. Confirmed by the in-tree docstring at `prompts.py:1843-1845`: "convergence.py / semantic_layer.py are PRESERVE, byte-untouched". Any latency fix that edits these two files (candidates c, d, e-partial) violates the dual-write invariant and must be an explicit, separately-authorized change — NOT folded into this Low-priority task.
- Corollary: candidate (c) (convergence wall-clock cap) and (d) (input reduction in the semantic layer) cannot be implemented without touching PRESERVE files. This is the decisive reason they are investigation-only.
- `fidelity_checker.py` is in scope but is invoked best-effort inside the convergence loop (`executor.py:1617-1636`, wrapped in try/except that continues on failure) — changes there affect convergence behavior and should be treated cautiously.

---

## Status: Complete

### Summary
- **opus-architect = `AgentSpec(model="opus", persona="architect")`** — parse `models.py:74-85`, `.id` slug `models.py:87-90`, CLI default `commands.py:434`. Persona is prompt-only; model is passed to `claude -p --model` at `executor.py:1186`.
- **Template adherence is two-layer, NOT prompt-only**: prompt embeds the template (`prompts.py:492-555`) AND a STRICT gate (`GENERATE_A_GATE`, `gates.py:1136-1185`) hard-fails missing sections / leftover sentinels / wrong table schema, with `retry_limit=1`. No adherence gap to fix; only a cosmetic 3-place section-list drift hazard.
- **The 1192s is NOT a single-step timeout.** It is the SUM of inner LLM calls inside convergence-mode spec-fidelity. Convergence is default-ON and `_run_convergence_spec_fidelity` (`executor.py:1533-1712`) runs `max_runs=3` synchronously, completely bypassing the Step's `timeout_seconds=600`. Inner `_ClaudeRunner` calls cap at 300s each (`executor.py:1521`); a semantic batch call + per-HIGH 2× debate calls + remediation across multiple runs sums to ~1192s. `build_spec_fidelity_prompt` is dead on this path.

### Actionable-now vs investigation-only VERDICT
- **Actionable NOW (concrete task item)**: a SAFE, behavior-neutral **comment** on the spec-fidelity Step (`executor.py:~2666-2676`) recording that `timeout_seconds=600` is INERT under convergence and the effective budget is `max_runs × 300s` inner calls — so a future engineer does not "fix" 1192s by bumping a dead literal (candidate b trap). Optionally, the section-list dedup (candidate f) IF the task already touches those surfaces.
- **Investigation-only (documented follow-up, do NOT implement here)**: the real latency fixes — a convergence wall-clock cap (c), semantic-layer input reduction (d), and lowering `max_runs`/inner-timeout (e) — because all either cross the **PRESERVE boundary** (`convergence.py`/`semantic_layer.py` byte-untouched) or trade convergence quality for latency and need measurement.
- **Reject**: bump generate timeout (a, wrong target), bump spec-fidelity timeout (b, inert/trap), prompt hardening (g, already enforced by gate), model swap (h, needs A/B).
- **Net**: Area C is correctly classed "Low / partly diagnostic." The only safe deterministic change is documentary; every behavioral fix for the 1192s is gated by the PRESERVE constraint and belongs in a separate, authorized investigation.
