# Refactoring Plan: Merge into Base (Variant 1, Option A)

## Overview
- Base: Variant 1 (option-a.md, architect advocate)
- Incorporating strengths from: Variant 2 (option-b.md), Variant 3 (option-c.md), Round 2.5 invariant probe + resolution round
- Planned changes: 12
- Risk level: Medium overall (the matcher and gate changes alter what is removed; every change narrows or fixes removal, none widens it beyond entries IronClaude can prove it wrote, except INV-002 which restores coverage of IronClaude's own PATH-discovered entries)
- Output: `../merged-recommendation.md` (decision record format: decision, removal rules, never-touch list, data policy, failure semantics, placement/bounds, user-facing output, Coder/plugin handoffs, goal-met-except record, acceptance tests, rejected alternatives, provenance)

## Planned Changes

### Change 1: Serena provenance-tiered exact allowlist (from Variant 2 R2 + INV-001)
- **Source**: round2-advocate-b.md §2; invariant-resolutions-proposed.md INV-001; resolution-advocate-{a,b,c}.md
- **Target**: Base step 2 serena matcher (replace)
- **Rationale**: A-001 CONTRADICTED; INV-001 HIGH (pre-fork user-scope rows 5bee1571/43112779/00ec67c7); unanimous ACCEPT after `shell=(sys.platform=="win32")` re-verified.
- **Integration**: Tier R (removed): exact argv of the 050d5ea2..0e7bc31f registry form; exact argv rows containing the literal token `$(pwd)` (5bee1571 uvx form; 43112779 `serena` form). Tier K (kept, one printed line): current pin, bare `--context ide-assistant` form, `--project <abs path>` family, any other `serena` user entry whose argv contains `start-mcp-server`. Others: "kept: not a Serena launcher registration".
- **Risk**: Medium — fixed rows must be copied byte-exact from git history; a test pins each row.

### Change 2: codebase-memory matcher = absolute basename shape (from INV-002)
- **Source**: fault-finder INV-002; resolution-advocate-c.md (withdrew exact-path request)
- **Target**: Base step 2 cbm matcher (replace)
- **Rationale**: IronClaude's required phase registered whatever discovery found on PATH (`install_codebase_memory.py:597-603`, `install_mcp.py:866`).
- **Integration**: absolute `command` with basename `codebase-memory-mcp`; `type` stdio or absent; `args` absent or `[]`; `env`/`headers` absent or empty.
- **Risk**: Low — registration-only; restorable with one printed command.

### Change 3: Binary-existence gate + absolute upstream uninstall hint (from Variant 2 R1/R2 ordering, INV-003, INV-005, B's qualify)
- **Target**: Base step 2 + step 5 (modify)
- **Integration**: If the matched entry's command equals the unresolved `Path.home().absolute()/.local/bin/codebase-memory-mcp` AND that file exists: keep the registration. Whenever that file exists (whatever the matched entry): print `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"` labelled "for a codebase-memory you or IronClaude installed under ~/.local/bin; removes its own client companions, keeps indexes". Any other matched entry: removed, with the note that a self-installed codebase-memory has its own `uninstall`.
- **Risk**: Low.

### Change 4: IronClaude receipt and `.pending` marker cleanup (from Variant 2, A-006, Variant 3 condition, INV-011)
- **Target**: Base step 4 (exception added to never-touch list) — insert
- **Integration**: Delete `~/.local/bin/.superclaude-codebase-memory.json` and `~/.local/bin/.superclaude-codebase-memory.pending` only when `~/.local/bin/codebase-memory-mcp` is absent and each passes the existing predicates (regular, user-owned, single link, `mode & 0o077 == 0`, `O_NOFOLLOW`; `_check_install_directory` for `~/.local`, `~/.local/bin`). Otherwise list them.
- **Risk**: Low — two IronClaude-named private files only.

### Change 5: One classifier, fixed action order (INV-004, INV-013)
- **Target**: Base Implementation paragraph (modify)
- **Integration**: pure `classify_retired_entries()` reads all state once; actions run (1) receipt/marker cleanup, (2) cbm registration, (3) serena registration. Shared by install, `install --list`, `doctor`, `update`.
- **Risk**: Low.

### Change 6: Safe removal helper (INV-006; base U-001)
- **Target**: Base step 3 + Implementation (modify)
- **Integration**: `_remove_exact_user_entry(name, matcher)` — matcher required; re-read and re-match immediately before `claude mcp remove <name> --scope user`; re-read after: absent -> removed; same shape -> warn "could not verify"; different shape -> "replaced concurrently, kept", never retried. Phase 2 reuses it.
- **Risk**: Low; sub-second delete-by-name window recorded as residual.

### Change 7: Execution bounds and placement (INV-007; C's qualify; A-003)
- **Target**: Base step 3 timeout + step 6 + placement (replace)
- **Integration**: exec `claude` directly (argv list, no `$SHELL -c`), `start_new_session=True`, kill the process group on timeout; 10 s per call; 15 s cap for the whole step; `shutil.which("claude")` None -> skip note that prints the exact manual `claude mcp remove <name> --scope user` for each entry that would have been removed. Placement: after all framework-file steps, in the slot of the deleted codebase-memory phase (`main.py:254`), before the exit-code block (`main.py:264`), inside its own `try/except Exception` that only warns.
- **Risk**: Medium — new subprocess wrapper; covered by tests with a stub `claude` that hangs.

### Change 8: Read-only surfaces (Variant 3 U-005 in cheaper form; INV-008; INV-009)
- **Target**: new subsection "Read-only surfaces" (insert)
- **Integration**: `superclaude install --list` replaces the cbm block (`main.py:161-186`) with one line per retired name; `superclaude doctor` warns (never fails) when the classifier still finds a removable entry; `superclaude update` prints only "legacy registration present: run `superclaude install`" (keeps its no-MCP contract, `docs/user-guide/mcp-installation.md:24`).
- **Risk**: Low.

### Change 9: User-facing messages (INV-008, INV-012; base step 5)
- **Target**: Base step 5 (modify)
- **Integration**: per action one line; restart note after any removal; cause-specific "unknown" warnings with the manual command; data delete commands (`~/.cache/codebase-memory-mcp`, `~/.serena`, project `.serena/`) printed "only if you no longer need them"; `uv tool uninstall serena-agent` printed as "if you installed it yourself; Coder workspaces reinstall it at start".
- **Risk**: Low.

### Change 10: Coder and plugin-mirror handoffs (Variant 3 step 4; INV-009d; INV-014)
- **Target**: new section "Handoffs" (insert)
- **Integration**: Phase 2 Coder handoff: stop the bundle registering/installing Serena, drop the image binary, remove any Coder-owned startup registration. Phase 1 search scope includes `plugins/superclaude/hooks/hooks.json` and `plugins/superclaude/mcp/configs/serena*.json`. No Coder-detection heuristic.
- **Risk**: Low.

### Change 11: Goal-met-except record and residual risks (INV-010; round2-advocate-c.md statement)
- **Target**: new section (insert)
- **Integration**: list exceptions with closing conditions; residual risks (TOCTOU, CLI `CLAUDE_CONFIG_DIR`, live-session write-back, alias-only `claude`, hand-made identical entries removed and restorable).
- **Risk**: Low.

### Change 12: Acceptance tests (base "4-6 unit tests plus one CLI integration test", expanded)
- **Target**: Base Implementation (modify)
- **Integration**: table-driven classifier test (every allowlist row, near-miss rows, env/headers, local/project entries ignored, receipt/marker/binary states incl. "receipt present, binary absent"), helper tests (concurrent replacement, verify failure), bound tests (hanging stub `claude`, missing CLI), CLI integration test (temp HOME, stub `claude`, exit code unchanged on failure), `update.sh` command list unchanged (`tests/cli/test_update_script.py:13-18`).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base / Rejecting |
|------------|-------------------|---------------------------|
| C-002 / X-002 | B: `uv tool uninstall serena-agent` (+ `uv cache clean`) | Coder installed it (no receipt); breaks Coder's `serena --help` health check and churns; B conceded (R1). |
| C-008 | B: automated receipt-gated upstream uninstall, keep slimmed `install_codebase_memory.py` for a release | Keeps the 759-line module and its 300 s path (`install_codebase_memory.py:28`) alive for unverified kind-B workspaces; account-wide prompt-free uninstall is what `install_mcp.py:981-986` forbids; B withdrew (R2). |
| C-002 | B: delete updater `~/.local/bin/install.sh` | Upstream file; policy "The adjacent updater is left in place" (`install_codebase_memory.py:74-78`); B conceded. |
| C-001 / X-001 | C: no automatic step; `superclaude mcp --retire-legacy [--dry-run] [--yes]` with interactive confirm | Fails the goal on `./update.sh` (X-003); prompt-free exact-entry removal is existing behaviour (`install_mcp.py:874-895`); C withdrew the flag (R2). |
| U-005 | C: separate `--dry-run` | Replaced by the read-only `install --list` line from the shared classifier (Change 8). |
| C-003 | A: basename + substring serena matcher | Misses IronClaude-written rows and matches hand-made ones (A-001, INV-001). |
| A-003 | A R2: place the step first | INV-007: the `$SHELL -c` timeout is not a hard bound; framework files must not wait on a CLI call. |
| INV-014 | C R2: Coder detection via `serena-agent` uv tool | Unverified signal; would change wording only. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | A provable row mis-copied -> entry kept (fail-safe) or near-miss removed | Test pins exact rows; drop the row |
| 2 | Low | Hand-made identical cbm entry removed | Printed re-add command |
| 3 | Low | Hint printed when not needed | Wording only |
| 4 | Low | Receipt deleted early | Gate on binary absence + predicates |
| 5 | Low | Preview and action disagree | Shared classifier test |
| 6 | Low | Concurrent entry deleted | Re-match; residual stated |
| 7 | Medium | Hang or skip | Process-group kill + 15 s cap; step is idempotent |
| 8-12 | Low | Text only / tests | Revert the section |

## Review Status
- [x] Auto-approved (default, non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T17:05:00Z
