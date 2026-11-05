# F2 decision: how Phase 2 measures the codegraph tool-list schema cost

Review finding X-1 (`.dev/codegraph-migration/review/review.md:49-52`) moves Phase 3's schema-cost experiment E-5 into Phase 2: before the installer registers `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"`, Phase 2 must check that listing those 7 tools instead of the default `codegraph_explore` adds at most 2K tokens to every session (threshold from `decisions/P3-access-model/adversarial/P3-access-model-merged.md:152-157`, "proposed, not measured"). Failure branch (same file :157): the key lists only `status`.

Facts:
- Default listing is explore only (`research/codegraph-evaluation.md:94`, `tools.ts:1953`); the explicit list hides every unnamed tool (source-cited `tools.ts:2926-2929`, never observed; X-25).
- The registration uses `alwaysLoad: true` (Phase 2 §2.4), so listed tools are not deferred behind tool search (`research/codegraph-evaluation.md:77`).
- A W4 stdio client already ran `initialize` + `tools/list` against `codegraph serve --mcp` (`research/codegraph-evaluation.md:205-216`).
- Claude Code 2.1.312 has `--mcp-config` and `--strict-mcp-config` (`claude --help`, observed 2026-10-29).
- Phase 2 rules: never `claude mcp add/remove` against the real HOME; sandbox HOME has no Claude login.
- The check runs once, in task T2 before the expected entry is written, by an unattended executor.
