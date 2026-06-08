---
status: partial
tier_reached: 2
confidence: 0.55
escalation_reason: forced_by_depth_deep
type: model-routing
scope: src/superclaude/skills/sc-reflect-protocol/SKILL.md
correction: "root cause DOWNGRADED — user challenge exposed that the dispositive evidence (gateway-models.json) is a 29-day-stale, discovery-OFF, unreferenced cache; see CORRECTION section"
status_original: success
confidence_original: 0.95
---

> ## ⚠️ CORRECTION (post-publication, 2026-06-03) — root cause downgraded to UNCONFIRMED
>
> A user challenge ("why is `gateway-models.json` referenced at all when it's stale and superseded by `~/.aienv`?") exposed that this REPORT's "dispositive" evidence was unsound:
>
> - **`~/.claude/cache/gateway-models.json` is 29 days stale** (mtime 2026-05-05), **unreferenced in settings.json/.claude.json**, and **`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` is OFF** → the harness almost certainly **does not consult that cache** at all. Citing its claude-only contents as proof that subagents route Anthropic-only was an error (mine, and the background agent's, transitively).
> - **The real config source is `/config/.aienv`** (SuperClaude-installer-managed): a LiteLLM gateway (`:4000/cli`, v1.80.8) with a genuine multi-vendor roster and per-tier proxy keys (`T0..T3ProxyKey`), and `ANTHROPIC_DEFAULT_SONNET_MODEL=gpt-5.5`, `HAIKU=qwen3.6-plus`, `OPUS=claude-opus-4-8`.
>
> **Consequence — the finding may be INVERTED.** With discovery OFF, the harness resolves model aliases from `ANTHROPIC_DEFAULT_*_MODEL`. If the Task `model: sonnet` subagent enum honors `ANTHROPIC_DEFAULT_SONNET_MODEL` the same way the main session does (the documented behavior; `CLAUDE_CODE_SUBAGENT_MODEL` unset), then the reviewers **actually ran multi-vendor** (gpt-5.5 / qwen3.6-plus / claude-opus) — meaning §0.6's `multi` would have been **correct**, and the error was the **unverified `t2_vendor_diversity: single` I emitted in the reflect run** (later "confirmed" by the same stale-cache inference).
>
> **What is NOT resolved:** I could not confirm what the reviewer subagents actually executed on. Live gateway verification was attempted but the `ANTHROPIC_AUTH_TOKEN` virtual key's `/v1/models` view was ambiguous (did not cleanly expose the non-claude aliases) and `/spend/logs` requires admin perms this key lacks. **Neither H-A (claude-only subagents) nor H-B (multi-vendor subagents) is proven.**
>
> **The one tier-independent finding that survives:** §0.6 (alias-name heuristic), the reflect run's `single` self-report, AND the background agent (stale cache) ALL determined vendor diversity **from proxies, never from observed execution**. Whichever way ground truth lands, the robust fix is: derive `t2_vendor_diversity` from an **execution signal** (the actual served model per subagent) or mark it **`unverified`** when no such signal exists — never from alias names or a stale cache.
>
> Everything below this banner is the ORIGINAL (now-suspect) diagnosis, retained for the audit trail. Do NOT action it until ground truth is established (see Definitive Test in Next Steps).

> ## ✅ RESOLUTION (2026-06-03) — original root cause REFUTED; H-B confirmed (~0.90)
>
> Ground truth was established by a controlled, positive-control-validated experiment against the live LiteLLM gateway (`:4000`, v1.80.8):
>
> **Method:** snapshot per-model dollar spend → spawn a `model: sonnet` + `model: haiku` subagent pair (~28K/36K tokens each) → re-snapshot → diff.
>
> **Result:**
> - **Positive control:** `claude-opus-4-8` (the orchestrator) **+10.42** across the window → spend tracking demonstrably captures claude usage in real time.
> - `claude-sonnet-4-6` (**proven-priced**, historical 0.297 > 0): **+0.0** despite the ~28K-token `model: sonnet` probe → the sonnet subagent did **not** run on claude.
> - `claude-haiku`: **+0.0**; `gpt-5.5`: **+0.0**; `qwen3.6-plus`: **+0.0** (the latter two are zero-cost local routes, so usage does not register as dollar spend).
>
> **Conclusion:** subagents spawned via the Task `model: sonnet|haiku` enum resolve through `ANTHROPIC_DEFAULT_*_MODEL` → `gpt-5.5` (OpenAI) / `qwen3.6-plus` (Qwen) / `claude-opus-4-8` (Anthropic). **Vendor heterogeneity is REAL in this environment.** Reflect §0.6's `t2_vendor_diversity: multi` was **correct**; the actual error was the **reflect run's unverified `single` self-report** (corrected in `.dev/reflect/post-mastra-beads-reconciled-20260603021115/`).
>
> **The original root cause (this REPORT below the banner) is WITHDRAWN.** The proposed §0.6 "honesty fix (force single)" is **rejected** — it would have suppressed a correct result. The gateway-models.json cache cited as dispositive was a 29-day-stale, discovery-OFF, unreferenced artifact and should never have been load-bearing (user's catch).
>
> **Residual (optional, downgraded from "fix" to "defense-in-depth"):** §0.6 still infers vendor by alias *name* — correct here, but it would mis-report in an env where an alias names a vendor the harness cannot route to. A robust hardening would derive/confirm `t2_vendor_diversity` from an execution signal (e.g., the served-model attribution) and set `vendor_diversity_source: execution-confirmed | name-heuristic`. Not urgent; not a bug.
>
> **Status:** resolved. **`status: success`** (root cause established: it was a measurement/reporting error on my side, not a protocol routing defect). Final confidence in H-B ≈ 0.90 (the one soft spot: `gpt-5.5`/`qwen` usage is inferred from "priced-claude did not move + config alias mapping," since those routes are zero-cost and leave no spend trace).

# Troubleshoot REPORT — reflect §0.6 reports `t2_vendor_diversity: multi` it cannot deliver

**Tier reached:** 2 (forced by `--depth deep`; diagnosis reached consensus — adversarial debate skipped per skip-rule). **Calibrated confidence: 0.95.**

## Summary

`sc-reflect-protocol` Wave 0 **Step 0.6** infers `t2_vendor_diversity` from a **name heuristic on the `ANTHROPIC_DEFAULT_*_MODEL` alias values** (`gpt-5.5`→OpenAI, `qwen3.6-plus`→Qwen), and emits `multi` when ≥2 vendors are named. But Tier 2 reviewers are spawned via the **§7.1 rotation through the Task/Agent `model` enum (`sonnet|haiku|opus`)**, which the Claude Code harness resolves **only against a claude-only model-discovery set**. The vendor the heuristic *names* and the vendor that *executes* are two different namespaces with no wiring between them, so §0.6 can emit a `multi` that execution structurally cannot honor. The fix is to make §0.6 **honest**: when subagents are spawned via the `model` enum (claude-only resolution), force `t2_vendor_diversity: single` with a `harness-limited` reason and never report a name-heuristic `multi` that the spawn path cannot deliver.

## Diagnosis

Two confirmed, independent facts compose the root cause:

1. **§0.6 is a name heuristic decoupled from execution.** `SKILL.md:213`: "extract the vendor … **by alias-name heuristic**. Emit … `t2_vendor_diversity: multi` (≥2 vendors among resolved aliases)…". Nothing in §0.5 (`:197-211`, which only sets reviewer *count*) or §7.1 (the `sonnet|haiku|opus` rotation) wires the alias *value* to the spawned subagent's actual model.

2. **The harness resolves subagent `model` enums to Anthropic-only by construction.** The gateway model-discovery cache `~/.claude/cache/gateway-models.json` holds **17 entries, 0 of them non-`claude`**. A subagent spawned with `model: sonnet` resolves the `sonnet` alias against that claude-only set — it can never land on the `gpt-5.5` value the env var holds. (`CLAUDE_CODE_SUBAGENT_MODEL` unset; `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` unset.)

So with `SONNET=gpt-5.5` + `HAIKU=qwen3.6-plus`, §0.6 computes `multi`, while the three reviewers all execute as `claude-*`. The recorded `t2_vendor_diversity: single` in the actual reflect run was *correct about the outcome*; the defect is that §0.6 is **capable of emitting `multi`** on a signal with no causal link to execution. This also weakens §11.0 sufficiency gate 2 ("≥2 vendors among reviewer aliases") silently.

**Classification:** primarily a **protocol design flaw** (assumes a subagent-vendor-routing capability the harness lacks), secondarily exposed by an env whose alias values name vendors the discovery filter rejects. NOTE: §19.1 already documents vendor heterogeneity as **v1.1-deferred / warn-only**, so single-vendor *operation* is the documented v1.0 behavior — the bug is narrowly the **dishonest `multi` emission**, not the single-vendor outcome.

## Evidence (all re-verified live this session)

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:213` — §0.6 "by alias-name heuristic … `t2_vendor_diversity: multi` (≥2 vendors)… warn-only in v1."
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:197-211` — §0.5 alias routing decides reviewer **count** only; no vendor-to-spawn binding.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:765-773` — §11.0 sufficiency gate 2 depends on "≥2 vendors among reviewer aliases."
- Live env: `ANTHROPIC_DEFAULT_SONNET_MODEL=gpt-5.5`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=qwen3.6-plus`, `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8`, `ANTHROPIC_BASE_URL=http://192.168.133.101:4000/cli`, `CLAUDE_CODE_SUBAGENT_MODEL` unset, `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` unset.
- `~/.claude/cache/gateway-models.json` — 17 model IDs, **0 non-`claude`** (sample: `claude-opus-4.5`, `claude-sonnet-4-5-20250929`, `claude-3-5-haiku-20241022`).
- Corroboration (background agent `adbb8421`, calibrated 0.93): gateway *is* multi-vendor-capable at the API (`POST /cli/v1/messages model=gpt-5.5` → 200; bare `model=sonnet` → 502, proving the harness resolves alias→concrete `claude-*` before sending) — so the gateway can serve non-Anthropic, but the **subagent spawn path cannot select it**. [INFERRED-corroboration: the 200/502 probes were run by the background agent, not re-run here; the dispositive local fact — the claude-only discovery cache — was re-verified directly.]

## Proposed Fix (chosen — "honesty fix", option a)

Edit **`src/superclaude/skills/sc-reflect-protocol/SKILL.md` §0.6** (`:213`) so vendor diversity is reported from **execution capability, not alias names**:

1. Add a **harness-capability gate** to Step 0.6: before inferring vendor from alias names, determine whether the subagent spawn path can select non-Anthropic models — i.e., whether reviewers are spawned via the Task/Agent `model` enum (which resolves against the gateway model-discovery set). When that set is claude-only (the default unless `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` **and** non-`claude` IDs are present), the alias-named vendors are **not subagent-selectable**.
2. In that case **force `t2_vendor_diversity: single`** with reason `harness-limited: subagent model enum resolves to claude-* only`, **regardless of alias names**. The name-heuristic `multi` is only permitted when the spawn path is verified able to route to the named vendors.
3. Add a telemetry field `vendor_diversity_source: alias-heuristic | harness-capability` (and a `vendor_diversity_reason` string) so consumers can tell an *aspirational* `multi` from an *execution-backed* one. Update §9.1/§9.2 contract + §15.1 metrics accordingly.
4. Reword **§11.0 gate 2** and **§3.4** to state that in a gateway deployment, non-`claude` alias values are not subagent-selectable, so the "≥2 vendors" gate reports `harness-limited` rather than implying achievability. Cross-reference §19.1.
5. `make sync-dev` → `make verify-sync` (SKILL.md edit is a `src/superclaude/` source change; never edit `.claude/` directly).

**Net effect:** §0.6 can no longer emit a `multi` it cannot deliver; single-vendor stays the honest, documented v1.0 behavior, now *correctly labeled* as harness-limited rather than a config the operator could "fix" by setting alias names.

## Alternative Fixes Considered

- **(b) Wire a real multi-vendor spawn path** — replace the `model: sonnet|haiku|opus` spawn with a driver that POSTs concrete non-`claude` IDs to `/cli/v1/messages` (gateway serves them, 200). The *only* path to genuine vendor heterogeneity, but materially larger (a custom reviewer-spawn driver outside the Task tool) and out of scope for v1 per §19.1. Rejected as the immediate fix; recorded as the v1.1 hardening path.
- **(c) Docs-only** — note in §3.4 that non-`claude` alias values aren't subagent-selectable. Necessary but insufficient alone: it leaves §0.6 still *able* to emit a false `multi`. Folded into the chosen fix as step 4.

## Risk + Rollback

- **Risk:** very low — a protocol-doc (SKILL.md) honesty edit + one additive telemetry field. No executable Python. The only behavioral change is that `t2_vendor_diversity` reports `single` (with a reason) instead of a possible spurious `multi`; downstream consumers already tolerate `single` (it's the documented v1.0 norm).
- **Watch after applying:** `make verify-sync` passes; the §12.2 eval rubric line ("≥2 vendors → +1.0") and the §17.6 testability row for `t2_vendor_diversity` still resolve (they should now assert the `harness-capability` source path too).
- **Rollback:** revert the SKILL.md edit + `make sync-dev`.

## Next Steps

`--fix` is set and status is `success` → the Tier 3 remediation chain is offered. On accept, `task-builder` produces an MDTM task file for the §0.6 honesty fix; **you** run `/task <path>` (never auto-executed); `/sc:reflect --type task --validate` is the pre-commit gate.
