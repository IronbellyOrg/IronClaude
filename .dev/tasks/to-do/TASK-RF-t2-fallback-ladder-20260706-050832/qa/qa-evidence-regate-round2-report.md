# QA Report — Research Gate (gap-fill re-gate, round 2)

**Topic:** T2 fallback ladder — reflect model fallback research
**Date:** 2026-07-06
**Phase:** research-gate (fix-cycle round 2)
**Lens:** evidence-quality
**Fix cycle:** 2
**Fix authorization:** false (report-only)

---

## Scope

Re-verify citation accuracy after gap-fill round. Files under verification:
- `research/06-config-threading-gap-fill.md` (NEW)
- `research/07-ensemble-t1-integration-seam.md` (NEW)
- `research/04-test-surface.md` (edited framing + WorkerResult cite)
- `research/05-template-and-examples.md` (header Status fix)

Verification method: re-Read each cited source file/line against the claim.

---

## Verification Log

### 1. research/06 config.py citations (src/superclaude/cli/reflect/config.py)

| Claim (research 06) | Source truth | Verdict |
|---|---|---|
| `resolve_config` def at `config.py:237-382` | `def resolve_config(` at **238**; return construct closing `)` at **383** → span 238-383 | Symbol correct; span drifts ~1 low. MINOR |
| signature spans `237-260` | signature 238-261 (`-> ReflectConfig:` at 261) | drift ~1. MINOR |
| last kwarg `reachability: bool = True` at `259` | actually at **260** (259 is `isolate_reviewers`) | off by 1; SUBSTANCE correct (reachability IS last kwarg). MINOR |
| `return ReflectConfig(...)` at `355-381` | `return ReflectConfig(` at **358**, closes **383** | drift 2-3 low. MINOR |
| final forward `reachability=reachability,` at `380`, closing `)` at `381` | `reachability=reachability,` at **382**, `)` at **383** | off by 2; SUBSTANCE correct (it IS the last forwarded field before close). MINOR |
| transport resolved at `326-330`, set `{openai_compat,stub}` | transport resolved 322-328; set literal at **323** | drift 3-5 low; SUBSTANCE correct (transport resolved before return, enabling stub-OFF derived line). MINOR |
| commands.py `--no-reachability` precedent (~L235-240 decorator, ~L368-369 forward, ~L484 tmux) | decorator L236, `reachability=reachability` forward L369, tmux `--no-reachability` L485 | ACCURATE (tilde-approx, all within 1). PASS |

**Finding:** research 06 exhibits a *consistent* ~1-3 line downward drift on config.py line numbers, but every SYMBOL and every SUBSTANTIVE claim (reachability is the last kwarg; reachability=reachability is the last forwarded field before the close; transport is resolved before the return) is correct and constructable. No fabrications. Per gate guidance (line-range off by a few does not block if file+symbol correct) → does not block.

### 2. research/07 ensemble + swarm citations

| Claim (research 07) | Source truth | Verdict |
|---|---|---|
| `resolve_t2_transport_factory(transport, *, reviewers, models=None, env=None)` at `ensemble.py:139-167` | def at **140**, signature 140-146, `return factory` at **168** | Symbol + full signature EXACT; span off by 1. PASS |
| `run_tier2_ensemble` calls it at `ensemble.py:201-205` | `resolve_t2_transport_factory(` call at **201-205** | EXACT. PASS |
| delegates to `_resolve_run_transport_factory(transport, models, env, workers_requested=reviewers)` | lines 162-167 exactly that | EXACT. PASS |
| `_resolve_run_transport_factory` at `swarm/commands.py:612-707` | def **612**, closes **707** | EXACT. PASS |
| `read_env(env)` internally at `commands.py:680` | `config = read_env(env)` at **680** | EXACT. PASS |
| `OpenAICompatTransport(...)` per slot at `commands.py:695-699` | built at **695-699** | EXACT. PASS |
| `run_tier2_ensemble` receives `ReflectConfig` + optional `env` at `ensemble.py:171-178` | def **171**, `env` param at 179, closes 180 | span end off by ~2; SUBSTANCE correct (no SwarmConfig/t1_models/base_url in scope — the load-bearing claim). PASS |

**Finding:** research 07 citations are essentially exact. The core corrective claim (the ensemble has no `swarm_config` in scope; design §2.1 pseudocode `make_fallback_slot_factory(pool=swarm_config.t1_models,...)` is NOT constructable at the seam; creds are read from env internally) is fully verified against source. No errors.

### 3. research/04 WorkerResult fix + framing (src/superclaude/cli/swarm/models.py)

| Claim (research 04) | Source truth | Verdict |
|---|---|---|
| `WorkerResult` dataclass at `models.py:1019-1129` | `@dataclass` **1019**, `class WorkerResult` **1020**, ends **1129** | CORRECT (was wrongly 1010-1012 — now fixed). PASS |
| `index` (L1110) | `index: int = 0` at **1110** | EXACT. PASS |
| `final_path` (L1114) | at **1114** | EXACT. PASS |
| `model_id` (L1115) | at **1115** | EXACT. PASS |
| `status` (L1118) | at **1118** | EXACT. PASS |
| `__post_init__` (L1123-1129) raises ValueError on out-of-enum status | def **1123**, closes **1129** | EXACT. PASS |

**Framing check:** research 04 lines 12-16 now open with "Correction (post-review): these were originally framed as 'BLOCKING design errors.' The design was patched in the same session... So the two items below are now CONFIRMATIONS of the current design, not conflicts." Finding A/B headers both carry "(Design §9 agrees.)". The former BLOCKING/design-broken framing is SOFTENED to a design-agrees confirmation. PASS.

### 4. research/05 header Status

Line 3 now reads `**Status: Complete**` (previously "In Progress"). PASS.

### 5. New citation errors introduced in 06/07

None found. Research 07 is exact. Research 06's config.py line numbers drift ~1-3 low but contain no fabricated symbols or non-constructable claims; the commands.py wiring cites (tilde-approximate) are accurate. No NEW defects.

---

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 1
  (No web research — all claims are local source-truth-bound.)
- Every one of the 5 spawn-prompt verification items was checked against re-Read source.

---

## Overall Verdict: PASS

### Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | research/06 config.py cites (def, last kwarg, return-forward) | PASS (w/ MINOR drift) | Re-read config.py:230-269 + 320-383; symbols correct, line #s ~1-3 low, substance constructable |
| 2 | research/07 ensemble/swarm cites | PASS | Re-read ensemble.py:135-209 + commands.py:608-708; near-exact, corrective claim verified |
| 3 | research/04 WorkerResult 1019-1129 + __post_init__ 1123-1129 + softened framing | PASS | Re-read models.py:1015-1131; all field lines EXACT; BLOCKING→design-agrees confirmed |
| 4 | research/05 header Status: Complete | PASS | Re-read line 3: `**Status: Complete**` |
| 5 | No new citation errors in 06/07 | PASS | 07 exact; 06 drift only, no fabrication; commands.py precedent verified (L236/369/485) |

### Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

### Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | research/06 lines 13,17,24 | config.py line numbers drift ~1-3 low (def 238 not 237; last kwarg 260 not 259; return-forward 382 not 380; closing paren 383 not 381; transport set 323 not 326-330). Symbols + substance all correct and constructable. | Non-blocking. Optionally bump the config.py line numbers by +1 to +3 to match current source. Does NOT block synthesis per gate guidance. |

### Previously-flagged defects — resolution status
- WorkerResult mis-cited 1010-1012 → **FIXED** (now 1019-1129, field lines exact).
- research 04 "BLOCKING design errors" framing → **FIXED** (now design-agrees confirmation).
- research 05 header "In Progress" → **FIXED** (now Complete).

### Recommendations
- PASS. Green light for synthesis. The lone MINOR (research 06 config.py line drift) is cosmetic — every symbol resolves and every edit point is constructable against current source; the ±1-3 offsets do not risk synthesis hallucination.

## QA Complete
