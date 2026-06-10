# Refactoring Plan (base = V1)

## Planned changes (incorporate into V1 base)
| # | Source | Target in base | Approach | Risk |
|---|--------|----------------|----------|------|
| 1 | V2 | Verdict vocab + §6 table | Replace {pass,fail,partial,error} with {pass,halted,degraded,blocked}; add fail-closed `degraded` row | Low (additive) |
| 2 | V2 | New FR-11 | Add fail-closed degradation detection (preflight alias count + post-contract checklist) | Low |
| 3 | V2 | FR-6 | Add compare-before-write race safety + wrapper-result.yaml sidecar to V1's surgical write | Low |
| 4 | V2 | FR-11 | Add FM-13: summarize_changes:unavailable is expected, not a halt | Low |
| 5 | V3 | §8 | Add stdin prompt delivery + concrete ClaudeProcess construction + file layout + main.py line | Low |
| 6 | V3 | FR-6 | Add atomic os.replace + yamllint _IndentedDumper mechanism | Low |
| 7 | V3 | FR-9 | --no-promote as a hard flag in the prompt string | Low |
| 8 | fix | §8 | Correct X-001: reflect --output in PROMPT only, not claude argv | Low (correctness) |

## Changes NOT made (base superior)
- Kept V1's NOT-HomeIsolation (rejected V2's "optionally HomeIsolation").
- Kept V1's builder-bakes-TCS-depth (rejected V3's hardcoded --depth deep, V2's wrapper-derives).
- Kept timeout 3600 (rejected V2's 1800).
- Kept V1's opt-in reversible POST_REFLECT_MODE flag.
