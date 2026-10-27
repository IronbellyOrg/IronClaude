# Eval Run: 2026-05-21T22:46:08Z / 224608Z-fd761175
**Suite:** /config/workspace/IronClaude/src/superclaude/cli/eval/suites/real.yaml | **Parallel:** 8 | **Duration:** 0.1s

## Result: 17 passed, 0 failed, 0 skipped, 0 errored, 0 interrupted, 0 timeout

| ID | Title | Status | Duration | Notes |
|---|---|---|---|---|
| E1 | auggie-first sticky lifecycle — set then clear | PASS | 0.0s | — |
| E2.1 | auggie matcher coverage — mcp__auggie__* | PASS | 0.0s | — |
| E2.2 | auggie matcher coverage — mcp__auggie-mcp__* | PASS | 0.0s | — |
| E2.3 | auggie matcher coverage — mcp__airis-mcp-gateway__auggie_* | PASS | 0.0s | — |
| E3 | SessionStart unmatched (session-init) hook fires | PASS | 0.0s | — |
| E4 | SessionStart matcher=* freshness hook fires | PASS | 0.0s | — |
| E5 | UserPromptSubmit freshness hook fires | PASS | 0.0s | — |
| E6 | PreToolUse Edit matcher fires | PASS | 0.0s | — |
| E7 | PreToolUse Write matcher fires | PASS | 0.0s | — |
| E8 | PreToolUse serena matcher fires | PASS | 0.0s | — |
| E9 | PostToolUse Read async hook fires | PASS | 0.0s | — |
| E10 | SubagentStart hook fires | PASS | 0.0s | — |
| E11 | SubagentStop hook fires | PASS | 0.0s | — |
| E12 | Hook deploy idempotency | PASS | 0.0s | — |
| E13 | Hook stderr error fails open | PASS | 0.0s | — |
| E14 | Concurrent SessionStart bursts | PASS | 0.0s | — |
| E15 | hook timeout fails open with telemetry | PASS | 0.0s | — |

## Counts
- manifest_n: 17
- expanded_n_prime: 17
- kept_k: 17
- skipped_s: 0
- kept_plus_skipped_equals_n_prime: true

_Finished at 2026-05-21T22:46:08Z._
