# Diff Analysis — reflect-cli-wrapper (3 variants)

- Variants: V1 opus:architect (421L), V2 sonnet:analyzer (431L), V3 haiku:backend (510L)
- Generated: 2026-06-08

## Structural (S)
| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Org model | FR/NFR + Arch + ReuseMap + Integration plan | Failure-Mode Register-first | FR/NFR + code-block impl | Low |
| S-002 | Verdict vocab | pass/fail/partial/error | pass/halted/degraded/blocked | exit 0/1/2 | Medium |

## Content (C)
| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Window mechanic | foreground default + --tmux opt-in + --print-command | blocking default + --attach tmux | foreground blocking | Low (converged) |
| C-002 | Wrapper home | cli/reflect/ Click subcommand | cli/reflect/ subcommand | cli/reflect/ subcommand | Low (unanimous) |
| C-003 | Headless env | bare ClaudeProcess real env; NOT HomeIsolation (load-bearing) | ClaudeProcess scrub; "optionally" HomeIsolation/cwd | bare _build_env real env | Medium |
| C-004 | Degradation posture | surface as RISK, pass stands | FAIL-CLOSED halt (degraded verdict) | not addressed | HIGH |
| C-005 | Timeout default | 3600s | 1800s | 3600s | Low |
| C-006 | Frontmatter write | surgical YAML edit | compare-before-write race-safe + sidecar | atomic os.replace + yamllint dumper | Medium (complementary) |
| C-007 | --no-promote | passthrough default | passthrough default | hard flag IN PROMPT | Low |
| C-008 | --depth / TCS | builder bakes depth (single producer) | wrapper derives TCS | --depth deep hardcoded | Medium |

## Contradictions (X)
| # | Conflict | Positions | Impact |
|---|----------|-----------|--------|
| X-001 | reflect `--output` placement | V3 puts `--output` on the `claude` argv AND prompt; V1/V2 put it only in the `/sc:reflect` prompt | HIGH — `--output` is a SKILL flag (prompt), not a `claude` CLI flag; V3's argv `--output` is a bug. Resolved: prompt-only. |
| X-002 | Degraded audit = pass? | V1 surfaces, lets pass stand; V2 halts (fail-closed) | HIGH — for a GATE, fail-closed wins (see invariant probe) |

## Unique contributions (U)
| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | V2 | Fail-closed degradation checklist (degraded_components, t2_*_diversity, adversarial null, citations_dropped, verification_ran) | HIGH |
| U-002 | V2 | summarize_changes:unavailable is EXPECTED cross-session, NOT a halt (FM-13) | HIGH |
| U-003 | V2 | compare-before-write race safety + wrapper-result.yaml sidecar | Medium |
| U-004 | V3 | stdin prompt delivery (bypass MAX_ARG_STRLEN) | High |
| U-005 | V3 | atomic os.replace + yamllint _IndentedDumper (matches memory reference_yamllint_indent_sequences_pyyaml) | High |
| U-006 | V3 | concrete file layout + exact main.py registration line | High |
| U-007 | V1 | NOT HomeIsolation (would strip MCP/aliases) — boundary rationale | HIGH |
| U-008 | V1 | opt-in reversible POST_REFLECT_MODE template flag | High |
| U-009 | V1 | builder bakes --depth (single TCS producer, no drift) | Medium |

## Shared assumptions (A)
| # | Assumption | Class | Promoted |
|---|-----------|-------|----------|
| A-001 | `claude --print` runs slash commands headlessly and the child invokes the SKILL (not just echoes prompt) | UNSTATED | yes → invariant probe |
| A-002 | Tier 2 needs ≥2 aliases + MCP present; top-level launch alone is not sufficient | UNSTATED | yes → invariant probe (sufficiency) |
| A-003 | task frontmatter already carries a `reflect_post:` field (master HALT writes PENDING) | STATED (V1) | no |

## Summary
2 structural, 8 content, 2 contradictions (both resolved), 9 unique, 3 shared-assumptions (2 promoted). Highest severity: C-004/X-002 (fail-closed), X-001 (V3 --output argv bug).
