# Variant 1 — DevOps Lens: Tavily Eval-Harness Capability Gating (tavily-mcp 0.2.x)

**Advocate:** DevOps · **Cluster:** C7 (eval harness = verification vehicle) · **Date:** 2026-06-22

The eval harness is the *operational proof* the whole 0.2.x upgrade hangs on. C1's
acceptance is "an eval-suite capability check"; today **no Tavily eval exists** — only a
docstring example (`models.py:317/322`) and a docs example (`docs/eval/retry.md:137-139`).
This spec makes the proof real and CI-safe.

---

## Decision 1 — Capability name: `mcp_server.tavily` (NOT `mcp.tavily`)

**Verdict: rename the *intended* token, no rename of any shipped logic.** The `mcp.tavily`
string in `models.py:317/322` and `docs/eval/retry.md` is a **docstring/doc example only**
— it is not the convention the loader resolves against. Ground truth in
`capabilities.py:217-240` and `real.yaml:36-40`: every shipped capability uses
`mcp_server.<name>` (e.g. `mcp_server.auggie`). For `requires: [...]` to resolve instead of
SKIP-on-unknown, the eval MUST tag `mcp_server.tavily` and the suite MUST declare it in
`optional_capabilities`. **0.2.x does not change this token.** Action: add ONE spec row to
`_DEFAULT_CAPABILITY_SPECS` so the probe roster knows tavily.

```python
# capabilities.py — append after the airis-mcp-gateway spec (line ~240)
_CapabilitySpec(
    "mcp_server.tavily", "tavily-mcp", "mcp_server",
    "skip", "--no-mcp", "Tavily MCP server reachable",
),
```

The probe is `mcp_server_reachable` → `shutil.which("tavily-mcp")` (capabilities.py:319-340).
Absent binary → `(False, ...)` → SOFT-SKIP. This is the CI-safety hinge.

## Decision 2 — Add a real capability-gated eval (the proof)

Lives in **`real.yaml`** (Decision 3). Copies the exact E2.x shape (id/title/category/
requires/timeout_sec/isolation/no_pty/inputs[prompt+expect_tool_call]/expects[file+exit_code]).
Note the tool name is the **direct-MCP hyphen form** `mcp__tavily__tavily-search`, distinct
from the gateway's underscore `tavily_search` (real.yaml:163 comment).

```yaml
# Append to optional_capabilities (real.yaml:36-40):
  - { name: mcp_server.tavily, gate_flag: "--no-mcp", failure_mode: skip }

# Append to evals (after E15):
  - id: E16
    title: "Tavily MCP search returns at least one result (0.2.x)"
    category: mcp-capability
    requires: [mcp_server.tavily]
    timeout_sec: 120
    isolation:
      home_strategy: ephemeral
    no_pty: skip
    # C1 acceptance: proves tavily_search is callable under tavily-mcp 0.2.x
    # with DEFAULT_PARAMETERS {search_depth:basic, max_results:10}. Gated on
    # mcp_server.tavily → SKIPPED (skip_reason, skip_flag_triggered) when the
    # tavily binary/key is absent, so CI without TAVILY_API_KEY stays green.
    # Tool is the DIRECT-MCP hyphen form, NOT the gateway underscore tool.
    inputs:
      - prompt: "Use mcp__tavily__tavily-search to find the official Tavily API docs site. Return the top result."
        expect_tool_call: mcp__tavily__tavily-search
    expects:
      - exit_code:
          equals: 0
```

**Key expect:** `expect_tool_call: mcp__tavily__tavily-search` (proves the 0.2.x tool is
reachable + invoked) plus `exit_code.equals(0)` (clean transcript = non-empty result path,
since an empty/error result aborts the session non-zero). A JSONL-substring assertion (like
E1's `sticky_cleared`) is **not** available — there is no tavily-result ledger hook — so the
tool-call expectation IS the result proof, matching the harness's expressible surface.

## Decision 3 — Where it lives: `real.yaml`, not a new suite

`real.yaml` is the live-MCP, PTY-driven suite and already carries the `optional_capabilities`
machinery + `no_pty: skip` convention. A new suite would duplicate `required_binaries`
(claude/jq/git) and the PTY scaffolding for one eval — pure sprawl. Co-locating E16 with the
auggie/serena live-MCP evals keeps one place where "real MCP works" is proven.

## Decision 4 — Version assertion of 0.2.20: OUT OF SCOPE (argued)

**Verdict: do NOT assert the literal `0.2.20` string in the eval.** MCP does not expose its
package version to the eval transcript — there is no tool-call surface, no env var, no
handshake field the harness reads that carries `0.2.20`. Forcing it would require a bespoke
`expects` predicate (`expect.py` Python callable, not YAML — see real.yaml:204-206) shelling
out to `npm ls tavily-mcp`, which tests the *host's* node_modules, not the running server —
a false proof. The version pin belongs in the **install/config cluster (C1)** where it's
enforced at install time (`DEFAULT_PARAMETERS` + pin live in the MCP config, not the eval).
The eval's job is behavioral: *does tavily-search work on whatever 0.2.x is installed?* — and
E16 proves exactly that. Asserting a version here is the wrong layer.

## Decision 5 (optional, C2) — Deep map/crawl eval, gated

C2 wants a live map/crawl exercise. Add ONE more gated eval, same shape, behind the SAME
capability — keeps it CI-skippable and avoids a second gate token:

```yaml
  - id: E17
    title: "Tavily map/crawl exercises deep retrieval (0.2.x)"
    category: mcp-capability
    requires: [mcp_server.tavily]
    timeout_sec: 180
    isolation:
      home_strategy: ephemeral
    no_pty: skip
    inputs:
      - prompt: "Use mcp__tavily__tavily-extract on https://docs.tavily.com to extract page content. Summarise in one line."
        expect_tool_call: mcp__tavily__tavily-extract
    expects:
      - exit_code:
          equals: 0
```

Longer `timeout_sec` (180) absorbs crawl latency. If C2 prefers a strict map/crawl tool,
swap `tavily-extract` for the 0.2.x map tool name once C2 fixes it — keep the gate identical.

---

## Verification (devops acceptance)

1. `superclaude eval describe --suite real` — MUST list E16 (+E17) in the inventory and
   exit 0 (schema-valid: every field copied from E2.x; `additionalProperties:false` honored).
2. **CI-safe SKIP proof:** in an env with no `tavily-mcp` on PATH / no `TAVILY_API_KEY`,
   `superclaude eval run --suite real` MUST emit E16/E17 with **status SKIPPED**,
   `skip_reason` set, `skip_flag_triggered` populated — and the suite run MUST NOT fail.
   Equivalent: `superclaude eval run --suite real --no-mcp` skips via the `gate_flag`.
3. **Positive proof (gated env):** with tavily reachable + key present, E16 runs, the
   `mcp__tavily__tavily-search` tool-call fires, exit_code 0.
4. `make verify-sync` clean (eval suites + capabilities.py are `src/`-only; no `.claude/`
   mirror touched).

## Acceptance criteria

- [ ] `mcp_server.tavily` spec added to `_DEFAULT_CAPABILITY_SPECS` (capabilities.py).
- [ ] `mcp_server.tavily` declared in `real.yaml` `optional_capabilities` with `gate_flag: --no-mcp`.
- [ ] E16 (search) added; E17 (map/crawl, C2) added or explicitly deferred.
- [ ] `superclaude eval describe --suite real` exits 0; inventory shows new evals.
- [ ] Without tavily binary/key, both evals report SKIPPED and the run stays green (CI gate).
- [ ] No `0.2.20` version literal asserted in any eval body (version lives in C1 config).
- [ ] No rename of `mcp.tavily` docstrings required for function (optional doc-cleanup → C8).

## Biggest risk

The `mcp.tavily` docstring/doc token (`models.py:317/322`, `docs/eval/retry.md:137`) will
mislead an author into tagging `requires: [mcp.tavily]`, which the roster does NOT resolve →
the eval silently SKIPS *even when tavily is present*, giving a false "all green" with zero
actual coverage. Mitigation: the capability MUST be `mcp_server.tavily` AND registered in
`_DEFAULT_CAPABILITY_SPECS`; flag the docstring drift to C8 for cleanup so the next author
isn't trapped.
