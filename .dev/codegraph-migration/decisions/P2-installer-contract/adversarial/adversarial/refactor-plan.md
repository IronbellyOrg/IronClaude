# Refactoring Plan

## Overview
- Base: Variant 3 (option-c, original), score 0.896
- Incorporated: Variant 2 (option-b), Variant 1 (option-a), resolution-round fixes
- Target: `../P2-installer-contract-merged.md`, the final recommendation (under 60 lines, provenance comments included)
- Changes: 12. Overall risk: Low. Every change is additive to C's contract or tightens it; none restructures it.

## Planned Changes

1. **Phase banner and failure output** (L1 forced round + V2 U-004). The banner reads "Installing codegraph (required user-level phase)...". On failure, stderr names the failed stage and the exact recovery command. The phase result still feeds `main.py:264-275`, so install exits 1 after every other phase has run. Risk: Low.
2. **Doctor `codegraph MCP registration`** (C-002, majority). It sets passed=False only when an entry exists and its `command`, resolved with `shutil.which` when it is a bare name (INV-007), is not an executable file. Missing entry, version drift, `codegraph prompt-hook` hook and `CODEGRAPH_START` block are reported as details with passed=True. An unreadable `~/.claude.json` reports "unknown" with passed=True (INV-008). The rationale is downgraded to "tools silently missing" (U-001). Risk: Low.
3. **Owned-entry test, replacing the env/headers refusal** (A-001 + INV-005). An entry counts as owned when its type is stdio or absent, it has no `url` and no `headers`, `args == ["serve","--mcp"]`, and its env keys are a subset of {CODEGRAPH_TELEMETRY, CODEGRAPH_NO_UPDATE_CHECK, CODEGRAPH_MCP_TOOLS}. Owned entries may be replaced, including when a pin bump changes the realpath. Risk: Medium, because it changes the replace guard from `install_mcp.py:867-873`.
4. **User-managed entry** (INV-006). For an entry that is not owned: if its command resolves to an executable, the phase passes with "user-managed codegraph entry kept" plus the remove command. Otherwise the phase fails with that same command. Risk: Low.
5. **Whole-entry matcher** (INV-014). The matcher compares type, command, args, env and alwaysLoad, so drift gets repaired. Risk: Low.
6. **Receipt as a list** (A-002 + INV-010 + INV-011). `~/.codegraph/.superclaude-receipt.json` holds the tag, tarball sha256, link targets and the owned version dirs in install order. It is written only after a verified download, and never for a baked or external binary. A corrupt receipt means delete nothing, never fail, and rewrite it. Risk: Low.
7. **Acquisition safety** (INV-003 + INV-004). Extract to a temp dir, then rename. Never overwrite a link or dir that is not in the receipt; report it instead (registration uses the absolute version-dir path). A link counts as owned only while it points where the receipt says. Risk: Low.
8. **Old version dirs, replacing the `daemons/` lookup** (C-005 + INV-001). Keep the previous owned dir for one run. Delete an older receipt-listed dir only when all three hold: this run's registration was verified; the receipt and `~/.claude.json` both read OK; and none of the registered command realpath, `~/.local/bin/codegraph` or `~/.codegraph/current` (owned or not) resolves inside it. Risk: Medium. This resolves the HIGH blocker INV-001.
9. **Fixed candidate order** (INV-002). Use exactly the context.md order. `--list` prints owned or external status and each link's resolved path. Risk: Low.
10. **Platforms** (INV-012). The downloader's 4-entry platform map. An unsupported platform fails the phase with a named message, matching today's `install_mcp.py:486-496`. Risk: Low.
11. **Coder prerequisites** (INV-015 + INV-009). The handoff states: bake at the exact pin on PATH, test-57 accepts the codegraph registration, no pin bump before the bake, and Phase 1 and Phase 2 land as one master unit. A `timeout 60` kill between registration remove and add is repaired on the next run. Risk: Low.
12. **Size estimate.** About 300 lines (`install_codegraph.py` about 180, `install_mcp.py` +60, `doctor.py` +30, `main.py` +30) and about 33 tests. Risk: Low.

## Changes NOT Being Made
- **V1 `superclaude mcp --uninstall --servers codegraph`** (C-003, X-003). Phase 1 deletes that surface, and the goal never names removal. V1 conceded in Round 2.
- **V1 strict doctor on presence, drift and leftovers** (C-002, C-008). Inside `update.sh` doctor runs only after install exits 0, and `make verify` never exits non-zero (`Makefile:42`). V1 conceded.
- **V1 doctor failing on a missing entry** (C-002 sub-point). It conflicts with documented removal; V2 and V3 form the majority against it.
- **V2 non-fatal phase** (C-001, X-001). It leaves Coder CI's exit-0 check proving nothing, and the ordering advantage was withdrawn. V2 conceded.
- **V2 no receipt and fixed-path `rm -rf`** (C-004, X-004). This can delete an upstream `install.sh` copy. V2 conceded.
- **C's `~/.codegraph/daemons/` per-version lookup.** Unverified; withdrawn by its own advocate.
- **INV-002 version-split machinery, INV-009 time budget, INV-011 keep-aside copy, INV-012 separate table.** These add code without a correctness gain (V2 pushback, accepted).

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 3 | Medium | A wrong ownership test could replace a user's entry | Tests: user entry with env, headers, url or other args is refused |
| 8 | Medium | A wrong reference check could delete a live dir | 3 tests: PATH split, two failed registrations, upstream-repointed link |
| Others | Low | Additive wording, reporting or estimates | Edit the text |

## Review Status
- Approval: auto-approved (non-interactive), 2026-10-29
