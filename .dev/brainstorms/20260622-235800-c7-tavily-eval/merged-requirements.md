---
cluster: C7
title: Eval harness — register mcp_server.tavily capability + add live tavily-search verification eval
convergence_score: 0.80
adversarial_status: pass
base_variant: opus:devops
created: 2026-06-23
---

# C7 Merged Spec — Eval Harness Capability Gating

## Convergence summary
2 variants (opus:devops, sonnet:qa). **Critical verified finding** (devops, confirmed by code read): the real eval capability token is `mcp_server.<name>` — `mcp.tavily` (in models.py docstrings + docs/eval/retry.md) is a **stale, non-registered token**. An eval written `requires: [mcp.tavily]` would never resolve → SKIP even when Tavily is present (false-green / zero coverage). qa independently flagged the same risk. Merge: devops's capability registration + correct token, qa's flakiness-proof assertion design.

**Invariant probe — HIGH resolved:** "the requires token doesn't match the resolver" → verified against `capabilities.py` (`_DEFAULT_CAPABILITY_SPECS`, all `mcp_server.*`) and `real.yaml:37-40` (`mcp_server.auggie/...serena`). No `mcp_server.tavily` exists yet. Fix below registers it. Status: ADDRESSED.

## Decisions
| # | Decision |
|---|----------|
| D1 | **Register `mcp_server.tavily`** capability. Add to `real.yaml` capability block (lines ~37-40) `- { name: mcp_server.tavily, gate_flag: "--no-mcp", failure_mode: skip }`. (Optionally also to `_DEFAULT_CAPABILITY_SPECS` in capabilities.py for default availability across suites.) |
| D2 | **Add a live verification eval** in `real.yaml` (consistent with existing E2/E8 MCP-eval + capability-block pattern): `requires: [mcp_server.tavily]`, prompt invoking `mcp__tavily__tavily-search`, expects the tool call + `exit_code 0`. The tool-call firing IS the proof (no tavily-result ledger hook exists). |
| D3 | **Stable assertions only** (qa): assert the tool was called (`expect_tool_call: mcp__tavily__tavily-search`, direct-MCP hyphen form) + exit 0 (+ a non-empty result-count regex IF observable in transcript). **Never** assert URLs, titles, snippets, ranking, or web text — those are the #1 flakiness source. |
| D4 | **CI-safe:** capability gate `failure_mode: skip` → absent `tavily-mcp` binary / `TAVILY_API_KEY`, or `--no-mcp`, yields SKIPPED (skip_reason + skip_flag_triggered), not FAIL. Run stays green without a key. |
| D5 | **No version assertion** — MCP exposes no version to the eval transcript; the `0.2.20` pin is verified at the C1 install layer, not here. |
| D6 | **map/crawl eval deferred** — C2 adopted them, but live map/crawl is volatile; only add behind a gated, fixture/controlled target later. Not in the default CI eval. |
| D7 | **Fix stale `mcp.tavily` docstrings/docs** to `mcp_server.tavily` to remove the false-green trap (handoff to C8 + a models.py docstring edit). |

## Concrete changes (by file)
- `src/superclaude/cli/eval/suites/real.yaml`: add `mcp_server.tavily` to the capability block; add eval `E-tavily-search` per D2/D3.
- `src/superclaude/cli/eval/capabilities.py` (optional): add a `_CapabilitySpec` row for `mcp_server.tavily` (kind `mcp_server`, "Tavily MCP server reachable").
- `src/superclaude/cli/eval/models.py` lines ~317/322: docstring examples `mcp.tavily` → `mcp_server.tavily`.
- `docs/eval/retry.md` lines ~137-139: example `requires: [mcp.tavily]` → `requires: [mcp_server.tavily]` (and title stays).

## Verification / tests
| Check | Asserts |
|-------|---------|
| `superclaude eval describe --suite real` | suite parses; `mcp_server.tavily` recognized; new eval listed |
| eval run without key (CI) | `E-tavily-search` → SKIPPED with skip_reason `capability 'mcp_server.tavily' unresolved`, run green |
| eval run with key (opt-in) | tool call fires; exit 0; non-empty result |
| `test_no_stale_mcp_tavily_token` | grep finds no `mcp.tavily` (only `mcp_server.tavily`) in eval YAML/docs/docstrings |

## Acceptance criteria
- AC1: `mcp_server.tavily` registered; `requires: [mcp_server.tavily]` resolves (not false-green).
- AC2: New eval SKIPS without key (green CI), passes with key.
- AC3: All `mcp.tavily` occurrences corrected to `mcp_server.tavily`.
- AC4: Assertions reference no volatile web content.

## Cross-cluster handoffs
- **This eval is the live-verification vehicle** referenced by C1 (install acceptance) and can host C2's optional gated map/crawl exercise.
- **C8 must fix the stale `mcp.tavily` token** in docs/eval/retry.md (and any other doc). This is a shared correctness item, not cosmetic.
- Confirms gateway `tavily_search` (underscore) vs direct `mcp__tavily__tavily-search` (hyphen) distinction — both valid in their namespaces; the eval uses the direct hyphen form.
