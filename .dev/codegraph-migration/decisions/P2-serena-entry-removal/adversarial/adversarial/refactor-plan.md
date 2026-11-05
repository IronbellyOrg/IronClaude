# Refactor Plan

## Overview
- Base: Variant 2 (Option B), score 0.898
- Incorporated: Variant 1 (Option A), Variant 3 (Option C), Round 2 refinements, invariant-probe resolutions
- Planned changes: 8 (RP-1 to RP-8)
- Overall risk: Medium (RP-3 and RP-4 widen what IronClaude removes; both are reversible user-scope registrations and print the removed argv)
- Hard limit for the merged output: under 50 lines (caller requirement)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| RP-1 | Bundle stops Serena in Coder step 2 | V2 U-001, all R2 | B bullet 3 (Coder) | replace | X-001 conceded by B R1; research 5.2 row C says safe with the old pin; C-003 92% | Low |
| RP-2 | Guard = `codegraph_ready()` reusing the codegraph phase's own pass check | B R2, A R2, C R2 | B bullet 1 condition | replace | Weaker "command executable" passes a broken/wrong-version binary (B R2, C R2); one function for `install`, `install --list`, `doctor` (A R2); user-managed resolving entry counts (INV-010, accepted) | Low |
| RP-3 | Remove every user-scope `serena` launcher (argv has `start-mcp-server`, stdio, no env/headers) when ready; Tier R rows stay unconditional; env/headers entries kept and reported | INV-004 | B bullet 1 scope ("Other Tier K shapes stay kept") | replace | Tier K still keeps IronClaude's own `00ec67c7` `ide-assistant` shape and other launchers, which violates "completely absent"; removed argv is printed so the user can restore it | Medium |
| RP-4 | Kind-B `~/.local/bin/codebase-memory-mcp` registration removed under the same predicate; binary and companions not removed; upstream `uninstall` printed; escalated | A-002 (all REJECT), INV-002 | new bullet | append | Registration in scope (A, B, C R2); binary removal reopens Phase 1 D2 | Medium |
| RP-5 | Re-register hint uses the name `serena-local` | A-004 (all ACCEPT R2) | messages | insert | Matcher keys on `serena`; no loop; no marker (new state rejected) | Low |
| RP-6 | Coder guarded one-time migration in step 2, in `startup.sh`: remove `serena` only when equal to the bundle argv, and the exact `/usr/local/bin/codebase-memory-mcp` entry, only when a `codegraph` user entry exists whose command prints `1.6.2`; also in step 2: `uv tool uninstall serena-agent`, markers, alias, health set, handshake proof. Step 5: image drops `/usr/local/bin/codebase-memory-mcp` | V1/V3 U-003, C R2, INV-001/-006/-008/-009 | B bullet 3 | replace | Majority ships it guarded in step 2 (C-004 80%); `test-57:602-603` forbids `mcp remove` in the bundle; guard without an IronClaude CLI; backstop for 60 s kills | Medium |
| RP-7 | Amend Phase 1 and Phase 2 texts in the same merge | A R2 point 1, B R2, INV-011 | new bullet | append | Executors otherwise get contradictory specs: Phase 1 §2.3 row, §3.2 Tier K, §3.4 hint, §3.6 row, Phase 1 sandbox expectation, D2; handoff §2.4 and §3.2; Phase 2 file table row, §2.1 "can leave neither", §8 steps 2 and 5 | Low |
| RP-8 | Acceptance: C's unit list, layer-2 seeded sandbox (both branches), Coder boot tests; A's `jq -e` extended to project scope; run after every Claude session restarts; Coder gated on image pin >= merge SHA; stated exceptions | C-007, A-001, INV-003/-005/-007/-013 | B bullet 5 | replace | All three combined (C-007 85%) | Low |

## Base weaknesses addressed
- X-001 ("registration gone after the slug run"): RP-1 + RP-6.
- B's dependency reference to a check defined only in A: RP-8 writes the check out.
- B's "Other Tier K shapes stay kept": RP-3.

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002 | C's `/etc/aidev02/ironclaude-provenance` guard | X-003: the file exists on the user's own workspace, which runs `./update.sh`; cross-repo path coupling |
| C-001 | A's "no IronClaude change" | X-002: never meets the requirement off Coder |
| A-004 | one-time removal marker | new state; the rename does the job (A R2, B R2) |
| C-004 | unguarded step-2 migration | removes Serena under the old pin with no replacement (B R2) |
| INV-002 | automatic upstream `uninstall` of the kind-B binary | Phase 1 D2 rejected prompt-free account-wide uninstall; escalated instead |
| INV-003 | removing local-scope / `.mcp.json` entries | Phase 1 §3.3 "never touched"; reported with the exact command instead |

## Risk Summary
| Change | Impact if wrong | Rollback |
|---|---|---|
| RP-3, RP-4 | a hand-made entry is removed | `claude mcp add` with the printed argv (as `serena-local`) |
| RP-6 | Coder boot regression | revert the Coder step-2 commit; IronClaude unaffected |

## Review Status
- Approval: auto-approved (non-interactive), 2026-10-29
