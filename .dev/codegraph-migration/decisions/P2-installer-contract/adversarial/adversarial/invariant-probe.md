# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Consensus probed: Option C base (required phase + U-004 recovery command; doctor fails only on a dangling registered command; receipt with owned-dir list; documented removal + `--list` ownership; keep previous owned dir one run; A-001 env-key-subset owned-entry test). Orchestrator spot-checks: `install_mcp.py:755-762` matcher compares only type/command/args (confirms INV-014); `codegraph-evaluation.md:59` upstream writes bare `"command":"codegraph"` (confirms INV-007).

| ID | Category | Assumption | Status | Severity | Evidence | Fix (smallest) |
|----|----------|------------|--------|----------|----------|----------------|
| INV-001 | collection_boundaries | Deleting "older" receipt-listed version dirs is safe | UNADDRESSED | HIGH | Consensus pt 5; `codegraph-evaluation.md:300-302`. Bake wins on PATH while `~/.local/bin/codegraph`/`~/.codegraph/current` still target an older owned dir; or two failed registrations leave the command on v1 and v1 is deleted | Delete a listed dir only if no owned link and no registered `command` resolves inside it, and only after this run's registration verified |
| INV-002 | state_variables | Candidate order matches what the shell runs | UNADDRESSED | MEDIUM | `codegraph-evaluation.md:300` "(or the PATH winner)" vs `context.md:7` fixed order | One fixed order; when an external binary is reused, leave owned links but report the version split in `--list` |
| INV-003 | guard_conditions | Paths IronClaude writes are IronClaude's | UNADDRESSED | MEDIUM | Upstream `install.sh` uses the same layout (`codegraph-evaluation.md:44-47`) | Never overwrite a link/dir not already in the receipt; extract to temp then rename |
| INV-004 | guard_conditions | Receipt paths stay ours | UNADDRESSED | MEDIUM | Upstream prune or `codegraph upgrade` can repoint links | A link is owned only while it points where the receipt says (also in `--list`) |
| INV-005 | guard_conditions | env-key subset alone proves ownership | UNADDRESSED | MEDIUM | Test ignores `type`/`args`/`url`; restore puts JSON on a command line (`install_mcp.py:775-786`) | Also require type stdio (or absent), no `url`, and `args == ["serve","--mcp"]` |
| INV-006 | interaction_effects | Required phase vs a refused user entry | UNADDRESSED | MEDIUM | `install_mcp.py:867-873` refuse -> `main.py:264-275` exit 1 every run | If the refused user entry's command is executable, pass with "user-managed entry kept" |
| INV-007 | guard_conditions | "not an executable file" detects a broken registration | UNADDRESSED | MEDIUM | Upstream bare `codegraph` command (`codegraph-evaluation.md:59`) | Resolve a bare name with `shutil.which` first |
| INV-008 | state_variables | `~/.claude.json` readable | UNADDRESSED | LOW | `install_mcp.py:857-862` | Doctor reports "unknown", passed=True; install message names the file |
| INV-009 | interaction_effects | Phase fits Coder's 60 s bound | UNADDRESSED | MEDIUM | 60 s per registration call (`install_mcp.py:769`); outer `timeout 60` can kill between remove and add | Document that the next run repairs it; bounded calls (no new budget machinery) |
| INV-010 | count_divergence | "previous"/"older" ordered | UNADDRESSED | LOW | Pin downgrade ambiguity | Receipt list in install order; "previous" = last registered before this run |
| INV-011 | state_variables | Receipt valid | UNADDRESSED | LOW | Corrupt/missing receipt rewritten drops owned dirs | Corrupt receipt = delete nothing, never fail install; keep file aside |
| INV-012 | guard_conditions | Every host runs the bundle | UNADDRESSED | LOW | macOS already exits 1 today (`install_mcp.py:486-496`) | Explicit 4-platform table; unsupported platform = phase failure with a named message (as today) |
| INV-013 | guard_conditions | Claude CLI present | ADDRESSED | LOW | Readiness check first (`install_mcp.py:829-842`) | None |
| INV-014 | sufficiency_challenge | `./update.sh` ends registered and pinned | ADDRESSED (conditional) | LOW | `update.sh:2,8,10`; matcher ignores `env`/`alwaysLoad` (`install_mcp.py:755-762`) | New matcher compares the whole expected entry |
| INV-015 | sufficiency_challenge | Consensus alone gives a fresh Coder workspace a registration | UNADDRESSED | MEDIUM | Needs bake at exact pin, test-57 edit, and a bump-order gate (`install-update-flow.md` 5.3) | Out of IronClaude scope: state these as Coder handoff prerequisites |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 2 (INV-013, INV-014 conditional)
- **UNADDRESSED**: 13
  - HIGH: 1 (INV-001)
  - MEDIUM: 8 (INV-002, 003, 004, 005, 006, 007, 009, 015)
  - LOW: 4 (INV-008, 010, 011, 012)

CONVERGENCE BLOCKED after Round 2.5: 1 HIGH-severity UNADDRESSED invariant (INV-001). A resolution round was run (see debate-transcript.md, "Resolution round").
