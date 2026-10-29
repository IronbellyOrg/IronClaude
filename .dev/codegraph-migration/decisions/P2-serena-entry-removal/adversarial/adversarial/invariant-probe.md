# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Probed consensus: corrected Option B (see `debate-transcript.md` Round 2). Resolution column added by the orchestrator: where it is carried in the refactor plan (RP-n) or escalated.

| ID | Category | Assumption | Status | Severity | Evidence | Resolution |
|----|----------|------------|--------|----------|----------|------------|
| INV-001 | sufficiency_challenge | After `./update.sh` on this Coder workspace both servers are completely absent | UNADDRESSED | HIGH | handoff §3.1-3.2: `/usr/local/bin/codebase-memory-mcp` root-owned, baked; `serena-agent` uv tool entry points in `~/.local/bin` (`inventory/serena.md` E9); provenance file present here | Partly fixed: all Serena Coder pieces move to step 2 (RP-6). The baked binary cannot be removed by IronClaude (root-owned); it stays until the step-5 image. ESCALATED as an unmet exception |
| INV-002 | sufficiency_challenge | Removing the kind-B registration makes codebase-memory absent off Coder | UNADDRESSED | HIGH | Phase 1 §3.3 never touches upstream client companions; `inventory/codebase-memory.md` lines 212-217, 244; `install_codebase_memory.py:25` | Registration removed under the predicate (RP-4). Binary and companions stay (removal reopens Phase 1 D2). ESCALATED as an unmet exception |
| INV-003 | collection_boundaries | User-scope `.mcpServers` is the only place a Serena entry lives | UNADDRESSED | MEDIUM | Phase 1 §3.3 never touches local scope or `.mcp.json`; Phase 1 sandbox seeds a project entry and expects it kept | RP-8: acceptance `jq` also checks `.projects[].mcpServers`; `install --list`/`doctor` report local-scope entries with the exact command; removal stays out of scope |
| INV-004 | guard_conditions | Promoting only Tier K row 1 covers every Serena entry IronClaude caused | UNADDRESSED | MEDIUM | Phase 1 §3.2 Tier K keeps the bare `ide-assistant` form (IronClaude `00ec67c7`), the `--project <path>` family, other launchers | RP-3: under the predicate, every user-scope `serena` launcher (argv contains `start-mcp-server`) with no env/headers is removed, printing the removed argv; entries with env/headers kept and reported |
| INV-005 | interaction_effects | A removed entry stays removed | ADDRESSED (Phase 1 accepted risk) | MEDIUM | Phase 1 §3.6; this session has both servers loaded | RP-8: acceptance runs after every Claude session restarts; doctor warns on write-back |
| INV-006 | interaction_effects | Retire finishes inside Coder's 60 s budget or a later boot retries | UNADDRESSED | MEDIUM | 60 s budget vs 30+10+10+60+15 s; `.configured` written; rerun only on SHA change | RP-6: Coder backstop also covers the exact `/usr/local/bin/codebase-memory-mcp` entry; Coder confirms what an outer kill does to a separate process group |
| INV-007 | state_variables | No later install puts old registrations back | UNADDRESSED | MEDIUM | Pin bump to a pre-merge SHA reruns old code; slug PATH choice of `superclaude` unconfirmed | RP-8: Coder acceptance gated on image pin >= merge SHA; Coder confirms which `superclaude` the slug runs |
| INV-008 | guard_conditions | The step-2 migration fits the bundle without breaking tests | UNADDRESSED | MEDIUM | `test-57:602-603` forbids `mcp remove` in the bundle; `spec2-health.sh:79`; manifest health; `test-startup-boot.sh:1978-2066` | RP-6: migration lives in `startup.sh` (or test-57 changes in the same step); health-set and handshake-proof edits listed in step 2 |
| INV-009 | count_divergence | IronClaude and Coder use the same readiness check | UNADDRESSED | LOW | Coder "entry exists" vs IronClaude pinned-version check | RP-6: Coder guard = `codegraph` user entry present AND `"$cmd" --version` prints `1.6.2` (no IronClaude CLI needed) |
| INV-010 | sufficiency_challenge | A passing predicate means codegraph works | UNADDRESSED | LOW | Phase 2 §2.4 user-managed entry passes when its command resolves | Accepted and documented (RP-2): a user-managed entry is the user's chosen replacement |
| INV-011 | count_divergence | cbm removal follows the same predicate everywhere | UNADDRESSED | LOW | Tier R `/usr/local/bin` entry removed unconditionally; Phase 2 §2.1 "can leave neither" | RP-7: rewrite the §2.1 sentence; unit test pins the asymmetry |
| INV-012 | guard_conditions | Retire still runs when the codegraph phase fails | ADDRESSED | LOW | Phase 1 §3.3 placement; `main.py:264-275`; `update.sh:2` | Keep the codegraph-fails sandbox test |
| INV-013 | collection_boundaries | `! command -v serena` holds off Coder | UNADDRESSED | MEDIUM | IronClaude's `serena-docker.json` advised `uv tool install serena-ai` (`inventory/serena.md` row 35); uv tools never touched | RP-8: stated exception with the printed `uv tool uninstall` command |
| INV-014 | state_variables | The `serena-local` hint prevents a removal loop | ADDRESSED | LOW | matchers key on name `serena`; Phase 1 §3.4 text changes | Unit test: the printed hint never uses the name `serena` |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 3 (INV-005, INV-012, INV-014)
- **UNADDRESSED**: 11
  - HIGH: 2 (INV-001, INV-002): escalated; they block the convergence gate
  - MEDIUM: 6 (INV-003, INV-004, INV-006, INV-007, INV-008, INV-013): carried as refactor-plan changes or stated exceptions (warnings, non-blocking)
  - LOW: 3 (INV-009, INV-010, INV-011)
