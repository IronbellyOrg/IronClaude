# Research: reflect/config.py `resolve_config` threading (gap-fill)

**Topic type:** Integration Points (gap-fill)
**Scope:** `src/superclaude/cli/reflect/config.py` — `resolve_config`
**Status:** Complete
**Date:** 2026-07-06
**Reason:** A.8 research-depth gate flagged this surface as flagged-but-not-line-grounded by researchers 1–5. Grounded here so the builder can write a per-line threading item.

---

## The threading point for `--no-tier2-fallback` + the 3 new `ReflectConfig` fields

`resolve_config` is defined at **`src/superclaude/cli/reflect/config.py:237-382`** (verified by symbol read 2026-07-06). It is the single funnel from CLI args + frontmatter + git state → `ReflectConfig`. The 3 new fields (`tier2_fallback_enabled`, `tier2_fallback_ladder`, `tier2_fallback_max_attempts`) and the `--no-tier2-fallback` flag thread through here.

### Exact edit points (current line numbers)

1. **Keyword-only param list** (signature spans `config.py:237-260`). The last existing keyword-only param is `reachability: bool = True` at **config.py:259**. Add the new param(s) after it, mirroring the `reachability` precedent:
   ```python
   reachability: bool = True,
   tier2_fallback_enabled: bool = True,   # NEW — flipped OFF by --no-tier2-fallback
   ```
   (`tier2_fallback_ladder` / `tier2_fallback_max_attempts` are NOT CLI-exposed in v1; they carry `ReflectConfig` defaults and need NOT be added to `resolve_config`'s signature unless a CLI flag is added. Only `tier2_fallback_enabled` needs the signature+forward edit for the `--no-tier2-fallback` flag. If a future flag exposes the ladder/max-attempts, add them the same way.)

2. **The `return ReflectConfig(...)` construct** at **config.py:355-381**. The final forwarded field is `reachability=reachability,` at **config.py:380** (just before the closing `)` at 381). Add:
   ```python
       reachability=reachability,
       tier2_fallback_enabled=tier2_fallback_enabled,   # NEW
   ```
   `tier2_fallback_ladder` and `tier2_fallback_max_attempts` are NOT passed here — they take their `ReflectConfig` dataclass defaults (design §7.2: `("T1Model01","T1Model02")` and `2`). This keeps `resolve_config` minimal and every existing call site valid (both new dataclass fields are defaulted).

3. **`--transport stub` fallback-OFF default (design §7.2).** `resolve_config` already resolves `transport` at **config.py:326-330** (`resolved_transport in {"openai_compat","stub"}`). The design says stub should default fallback OFF (the stub pool already certifies). Implement by computing the effective enable AFTER transport resolution:
   ```python
   # design §7.2: stub transport certifies on its own; default fallback OFF for it
   resolved_fb_enabled = tier2_fallback_enabled and resolved_transport != "stub"
   ```
   and forward `tier2_fallback_enabled=resolved_fb_enabled`. (An explicit `--no-tier2-fallback` still forces OFF; there is no `--tier2-fallback` force-ON flag in v1, so stub-OFF is safe.)

### commands.py flag wiring (4 edits — from research 01)

Per research 01, `--no-tier2-fallback` needs FOUR edits in `reflect/commands.py`, mirroring the `--reachability/--no-reachability` precedent (commands.py ~L235-240):
1. the `@click.option("--no-tier2-fallback", ...)` decorator (near the flag block ~L319),
2. the `def run(...)` param (~L336-337),
3. the `resolve_config(..., tier2_fallback_enabled=not no_tier2_fallback)` forward (~L368-369),
4. the tmux `_build_inner_command` forwarding (~L459-497, near the L484 `--no-reachability` precedent) — else the flag silently resets ON in the inner foreground reinvocation.

### Verification for the threading item

- `uv run pytest tests/cli/reflect/ -k "config or resolve"` stays green (new field is defaulted; existing `resolve_config` calls unaffected).
- A new test asserts `resolve_config(..., transport="stub").tier2_fallback_enabled is False` and `resolve_config(..., tier2_fallback_enabled=False).tier2_fallback_enabled is False`.

## Reconciliation: T1 proxy binding SUPERSEDES the design §7.3 default (closes G-2 / C-1)

Research files 02 (§2) and 03 (§5) faithfully report the design §7.3 *default*
(`proxy_url_env=T2_PROXY_URL_ENV`, "reuse the T2 proxy"). **That default is
SUPERSEDED for this environment** and MUST NOT be wired as-is. Authoritative
consolidation (research-notes.md **G1**, cross-validation I-1, completeness G-2):
`~/.aienv` exposes DISTINCT env-var NAMES `T1ProxyUrl`, `T1ProxyKey`, `T1Model01`,
`T1Model02` (names only — values never read, per `feedback_aienv_only_proxy_contract`).
Therefore the correct real-dispatch binding is:

```python
read_env_for_pool(
    model_prefix="T1Model0",
    max_slots=T1_MODEL_MAX_SLOTS,
    proxy_url_env="T1ProxyUrl",     # NOT T2_PROXY_URL_ENV
    proxy_key_env="T1ProxyKey",     # NOT T2_PROXY_KEY_ENV
)
```

The `read_env_for_pool` shape (F3) already parameterizes the proxy-env names, so
this is a call-site argument choice, not a structural change. **The builder MUST
encode the T1Proxy* arm, NOT the design's T2-reuse default**, and gate it behind
the HALT below.

## needs_human_decision HALT semantics (closes G-3)

Per `feedback_human_decision_items_must_halt`: a `needs_human_decision` item MUST
write a PENDING marker and HALT the dependent mutation — it must NEVER auto-apply
a default that ships a change. Concretely, the task item that precedes wiring
**real** fallback dispatch (rollout step 5) MUST:

1. Verify (read-only, names only) that `~/.aienv` / the environment exposes
   `T1ProxyUrl`, `T1ProxyKey`, and at least `T1Model01` — WITHOUT reading or
   printing their values, and WITHOUT probing `:4000/v1` or the proxy API
   (`feedback_aienv_only_proxy_contract`).
2. If confirmed → record the resolved binding decision (`proxy_url_env=T1ProxyUrl`,
   `proxy_key_env=T1ProxyKey`, `model_prefix=T1Model0`) in the task log and proceed.
3. If NOT confirmed, or if the operator has not signed off on the T1-proxy arm →
   write a PENDING entry to the task's `### Open Questions` (do NOT delete existing
   items) and HALT before wiring real dispatch. Do NOT silently fall back to the
   design's T2-reuse default (that would ship an unverified proxy binding).

Stub-transport work (rollout steps 1–4: `fallback.py` pure helpers, contract
metadata, controller wiring behind `tier2_fallback_enabled` with `--transport stub`,
swarm T1 slot resolution + `read_env_for_pool`) does NOT depend on this HALT and
proceeds unblocked — the stub transport certifies without any real proxy.

## F4 wall-clock grounding (closes G-6 / GAP-3)

Verified `runner.py:505-513` (symbol read 2026-07-06): the in-process Tier-2 path
computes `expected_tier` then, for `expected_tier == 2 and ClaudeProcess is
_ProductionClaudeProcess`, calls `run_tier2_ensemble(config)` DIRECTLY and sets
`rc = 0` — there is **no outer `ClaudeProcess` timeout wrapping the ensemble** at
this layer. This confirms F4's premise: the shared run deadline must be captured
INSIDE `run_tier2_ensemble` (design §7.4: `deadline = _monotonic() +
config.timeout_seconds`), because no caller-level timeout bounds the fallback
loop. `config.timeout_seconds` is the single budget source (default 3600, per
`resolve_config` `timeout or _DEFAULT_TIMEOUT_SECONDS`).

## Summary

The flag/field threading is a bounded, low-risk edit: 1 signature param + 1 return-forward in `config.py` (+ the stub-OFF derived line), plus the 4-point `commands.py` flag wiring. The 2 non-CLI dataclass fields ride their `ReflectConfig` defaults and need no `resolve_config` change. No existing call site breaks (all new fields defaulted). The T1-proxy binding uses the `T1ProxyUrl`/`T1ProxyKey` arm (NOT the T2-reuse default) behind a needs_human_decision HALT; F4's deadline is captured inside `run_tier2_ensemble` (no outer timeout exists). The ensemble→swarm T1 acquisition seam is grounded separately in `research/07-ensemble-t1-integration-seam.md` (GAP-2).
