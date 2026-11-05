# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent general-purpose subagent (not an advocate). Raw output: `fault-finder-raw.md`. Proposed resolutions: `invariant-resolutions-proposed.md`. Advocate verdicts on resolutions: `resolution-advocate-{a,b,c}.md` (A: 13 ACCEPT + 1 QUALIFY; B: 13 ACCEPT + 1 QUALIFY; C: 13 ACCEPT + 1 QUALIFY; every QUALIFY is additive and folded into the resolution).

Status column = status AFTER the resolution round. "Probe status" = status the fault-finder assigned against the Round 2 consensus.

| ID | Category | Assumption | Probe status | Status | Severity | Evidence |
|----|----------|------------|--------------|--------|----------|----------|
| INV-001 | collection_boundaries | Serena allowlist needs only the current pin + one older form | UNADDRESSED | ADDRESSED | HIGH | Pre-fork `setup/components/mcp.py` registered at user scope with `--project $(pwd)` literal (5bee1571, 43112779; `subprocess.run(list, shell=(sys.platform=="win32"))` re-verified by orchestrator) and `--context ide-assistant` bare (00ec67c7). Resolved: two-tier provenance rule (code-only rows removed; ambiguous rows kept + one printed line). |
| INV-002 | collection_boundaries | IronClaude only wrote cbm entries at two paths | UNADDRESSED | ADDRESSED | MEDIUM | `install_codebase_memory.py:597-603`, `install_mcp.py:866`. Resolved: absolute command, basename `codebase-memory-mcp`, stdio, `args` []/absent, env/headers empty/absent. |
| INV-003 | guard_conditions | No receipt means IronClaude did not install a `~/.local/bin` binary | UNADDRESSED | ADDRESSED | MEDIUM | `install_codebase_memory.py:640-650,668`. Resolved: gate on binary existence; B's qualification: print the absolute upstream uninstall whenever `$HOME/.local/bin/codebase-memory-mcp` exists. |
| INV-004 | interaction_effects | Receipt rule and registration rule need no order | UNADDRESSED | ADDRESSED | MEDIUM | `install_codebase_memory.py:362-369`. Resolved: classify all state first; fixed action order; one-run convergence test. |
| INV-005 | guard_conditions | Bare `codebase-memory-mcp uninstall -y` targets the kind-B binary | UNADDRESSED | ADDRESSED | MEDIUM | `install_codebase_memory.py:352-355`. Resolved: absolute path + `--dir`, printed only when the file exists. |
| INV-006 | state_variables | Name-parameterised cleanup helper keeps the shape guarantee | UNADDRESSED | ADDRESSED | MEDIUM | `install_mcp.py:916-934` removes by name only. Resolved: matcher required, re-match before remove, never retry a different shape; sub-second TOCTOU residual stated. |
| INV-007 | interaction_effects | 10 s per call is a hard bound; "first" placement protects install | UNADDRESSED | ADDRESSED | MEDIUM | `install_mcp.py:129-141` (`$SHELL -c`, `shell=True`). Resolved: direct exec, new session, process-group kill, 10 s/call, 15 s step cap, `shutil.which`; placed in the slot of the deleted cbm phase; C's qualification: skip note prints the manual command. |
| INV-008 | interaction_effects | Verify-after-remove proves the end state | UNADDRESSED | ADDRESSED | MEDIUM | Running Claude sessions rewrite `~/.claude.json`. Resolved: restart note; `superclaude doctor` warning (never failure) from the shared classifier. |
| INV-009 | sufficiency_challenge | `install` + `--force` refresh covers every upgrade path | UNADDRESSED | ADDRESSED | MEDIUM | `main.py:352-377` (`update`), `install_core.py:62-66`, `install_hooks.py:393-395`, plugin mirror. Resolved: `update` prints a read-only notice; goal claimed for `--force` paths only; plugin mirror added to Phase 1 search scope. |
| INV-010 | sufficiency_challenge | Consensus alone meets the goal | ADDRESSED | ADDRESSED | HIGH | Current serena pin kept. Resolved: decision states "goal met except" with closing conditions. |
| INV-011 | guard_conditions | Simplified file guards are sufficient | UNADDRESSED | ADDRESSED | LOW | `install_codebase_memory.py:95-100,125-139,185-199`. Resolved: reuse existing predicates exactly; HOME-mismatch reported as kept. |
| INV-012 | state_variables | Reader and CLI use the same config file | UNADDRESSED | ADDRESSED | LOW | `install_mcp.py:731-736`. Resolved: cause-specific "unknown" warnings with the manual command. CLI-side resolution remains UNVERIFIED (residual). |
| INV-013 | count_divergence | `--list` preview and step agree | UNADDRESSED | ADDRESSED | LOW | `main.py:161-186,177-185`. Resolved: one pure classifier shared by step, `--list`, `doctor`, `update`; table-driven test. |
| INV-014 | interaction_effects | Coder churn is harmless | ADDRESSED | ADDRESSED | LOW | context.md:11,19. Resolved: no Coder heuristic; the one serena line says Coder re-adds it. |

## Summary

- **Total findings**: 14
- **Probe result (against Round 2 consensus)**: ADDRESSED 2, UNADDRESSED 12 (HIGH 1, MEDIUM 8, LOW 3)
- **After resolution round**: ADDRESSED 14, UNADDRESSED 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
- **Invariant gate**: initially BLOCKED (INV-001 HIGH UNADDRESSED); cleared after the resolution round with unanimous ACCEPT/additive QUALIFY.
- **Residual risks carried into the decision (accepted, not unaddressed findings)**: sub-second delete-by-name window (INV-006); CLI-side `CLAUDE_CONFIG_DIR` resolution UNVERIFIED (INV-012); a running session may write an entry back until restart (INV-008); claude-as-alias-only users are skipped with a printed command (INV-007).
