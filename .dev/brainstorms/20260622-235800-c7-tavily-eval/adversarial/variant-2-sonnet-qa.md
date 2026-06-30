# Variant 2 — QA change spec: Tavily eval capability gate

## Position
Add a dedicated Tavily MCP eval suite, not a `real.yaml` entry. `real.yaml` currently covers hook matcher behavior; adding web-dependent MCP proof there blurs intent and makes routine real-suite runs depend on an external API. A dedicated suite such as `mcp-tavily.yaml` makes opt-in, skip behavior, and failure triage obvious.

The eval must prove only the stable contract: the `tavily-search` tool can be invoked under tavily-mcp 0.2.x defaults and returns a non-empty result list. It must not assert specific URLs, titles, snippets, ranking, domains, or dates.

## Required capability-gate change
Register `mcp.tavily` as a soft-skip MCP capability before adding the suite. The schema accepts arbitrary `requires[]` strings, but CI safety depends on the resolver recognizing `mcp.tavily` and classifying absence as SKIPPED, not loader error or FAIL. The gate should use `failure_mode: skip` and be covered by `--no-mcp` like the existing MCP capabilities.

## Concrete schema-valid suite YAML

```yaml
name: mcp-tavily
version: "1.0"
description: "Tavily MCP 0.2.x capability gate: direct tavily-search returns at least one result when available, and soft-skips when unavailable."

defaults:
  per_eval_timeout_sec: 90
  per_eval_memory_mb: 512
  capture_tty: true
  keep_home_on_success: false

required_binaries: []

optional_capabilities:
  - name: mcp.tavily
    gate_flag: --no-mcp
    failure_mode: skip

evals:
  - id: TAV1
    title: "Tavily MCP search returns at least one result"
    category: mcp-capability
    requires: [mcp.tavily]
    timeout_sec: 90
    isolation:
      home_strategy: ephemeral
    no_pty: skip
    inputs:
      - prompt: "Use mcp__tavily__tavily-search exactly once to search for `SuperClaude Framework` using the tavily-mcp 0.2.x default parameters only; do not set search_depth or max_results. After the tool returns, print exactly two lines: `TOOL=mcp__tavily__tavily-search` and `RESULT_COUNT=<number of results returned>`. Do not print URLs, titles, snippets, or result text."
        expect_tool_call: mcp__tavily__tavily-search
    expects:
      - stdout:
          contains: "TOOL=mcp__tavily__tavily-search"
      - stdout:
          regex: "(?m)^RESULT_COUNT=[1-9][0-9]*$"
      - stderr:
          not_contains: "Traceback"
      - exit_code:
          equals: 0
```

## Assertion-stability rationale
`inputs.expect_tool_call` is the schema-valid mechanism for proving the tool fired; do not invent a new `expects: - tool_call:` primitive. The `stdout` tool sentinel is defense-in-depth and makes run logs human-auditable. The non-empty count regex proves the response was usable while avoiding volatile web content. `exit_code: 0` proves the harness lifecycle completed, and `stderr` excludes Python crash signatures without treating ordinary web-result wording as a failure.

Do not assert `search_depth: basic` or `max_results: 10` from output: Tavily results do not echo default arguments reliably. The eval should drive the default path by omitting those arguments; separate unit/adapter tests should lock `DEFAULT_PARAMETERS = {"search_depth":"basic","max_results":10}`.

## Map/crawl verdict
Do not add map/crawl evals for C1. They are not required to prove the tavily-mcp 0.2.x search upgrade, and they are more exposed to robots rules, site topology churn, crawl latency, and rate limits. Add them only if C2 explicitly adopts map/crawl and can constrain them to a controlled or fixture-backed target; otherwise they will be flakier than the capability they prove.

## CI-safety proof
When `mcp.tavily` is absent or `--no-mcp` is used, the eval must be reported SKIPPED with no `expects[]` executed and no failing row. CI without a Tavily key therefore remains green. `superclaude eval describe --suite mcp-tavily` must validate the manifest shape; `superclaude eval run --suite mcp-tavily --no-mcp` must produce SKIPPED, not FAILED/ERRORED.

## Acceptance criteria
- `superclaude eval describe --suite mcp-tavily` exits 0.
- `superclaude eval run --suite mcp-tavily --no-mcp` exits green and reports TAV1 as SKIPPED.
- With Tavily configured, TAV1 performs exactly `mcp__tavily__tavily-search`, prints a positive `RESULT_COUNT`, and passes without inspecting URLs/text.
- No Tavily eval is added to `real.yaml`; the suite is isolated as `mcp-tavily.yaml`.
- No map/crawl eval ships unless C2 adopts those tools with a fixture-backed or otherwise non-volatile target.
