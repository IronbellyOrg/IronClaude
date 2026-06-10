# Merge Log

Base: Variant 1 (opus:architect). Output: merged-output.md.

| # | Change | Applied | Provenance |
|---|--------|---------|------------|
| 1 | 4-state verdict vocab + §6 table | yes | V2 |
| 2 | FR-11 fail-closed degradation detection | yes | V2 |
| 3 | FR-6 compare-before-write + sidecar | yes | V2 |
| 4 | summarize_changes:unavailable not-a-halt | yes | V2 |
| 5 | §8 stdin prompt + ClaudeProcess construction + file layout | yes | V3 |
| 6 | FR-6 atomic os.replace + yamllint dumper | yes | V3 |
| 7 | --no-promote hard prompt flag | yes | V3 |
| 8 | X-001 fix: reflect --output in prompt, not claude argv | yes | merge correction |

## Post-merge validation
- Structural integrity: PASS (FR/NFR/Arch/Window/Verdict/OQ/Impl/Scope/Risks/InvariantProbe).
- Internal references: PASS (FR-1..12, NFR-1..8 resolve).
- New contradictions introduced: 0.
- Status: success.
