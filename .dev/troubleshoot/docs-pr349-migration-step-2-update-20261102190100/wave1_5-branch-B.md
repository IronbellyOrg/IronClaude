# Wave 1.5 Branch B — architectural-doc lookup (returned by troubleshoot-analyst; persisted by parent on receipt)

degraded: true (auggie unavailable to the worker; Grep/Glob/Read only). docs/troubleshooting/ does not exist; KNOWLEDGE.md has no matches.

Currency verdicts finalized by the parent (Section 2): file mtimes in this fresh worktree are checkout times, so the parent used the last git commit date of each doc against the last commit of the described code, src/superclaude/cli/main.py (2026-10-30T11:23:25-04:00). No doc has a deprecated/archived/Last-reviewed marker.

| doc_path | last commit | verdict | summary (worker) |
|---|---|---|---|
| docs/releases/v5.0.0.md | 2026-11-02 | current | :143-148 upgrade = pipx reinstall + `superclaude update`; :150 "`./update.sh` does the same"; :69 "needs `superclaude update` (not a plain `superclaude install`)"; :3 "Upgrade with superclaude update"; :152 expects `install --list` codegraph block; :83/:106 credit codegraph download and retire step to `superclaude install`. |
| docs/getting-started/installation.md | 2026-11-02 | current | Update section :326-333 = pipx reinstall + `superclaude update`; :53-57, :363 same; :365 says `install --force` "does the same" as update; 0 codegraph mentions. |
| docs/user-guide/mcp-installation.md | 2026-10-31 | current | :7 `superclaude install` (and so `./update.sh`) installs codegraph as a required phase; :23 failure exits 1 so `./update.sh` stops; :54 Serena retired in the first `superclaude install` where codegraph is ready; :64-66 install runs codegraph phase then retire; :70 `superclaude update` never touches MCP registrations; :71 "`superclaude install --force` reinstalls framework files only" (ambiguous). |
| docs/reference/mcp-server-guide.md | 2026-10-30 | current | :13, :29 codegraph installed/registered by `superclaude install`; :43 stale/wrong version → run `superclaude install`; no `update`. |
| docs/developer-guide/testing-debugging.md | 2026-10-14 | current | `superclaude install --force` fixes missing commands/agents (:164-165, :185-186); no MCP. |
| docs/reference/diagnostic-reference.md | 2026-10-14 | current | plain install never replaces existing files (:262-267); `install --force` for empty files (:277); no MCP. |
| docs/reference/troubleshooting.md | 2026-05-22 | stale | :140 `install --force` re-enables hooks; :10 `python3 -m SuperClaude --version # Should show 4.1.5` (stale). |
| docs/user-guide/freshness-hooks.md | 2026-10-30 | current | hooks distributed by install (:3, :11, :117); no MCP. |
| docs/user-guide/flags.md | 2026-10-30 | current | `--force` on install = reinstall even if files exist (:208). |
| CLAUDE.md | 2026-11-02 | current | install = `pipx install git+... && superclaude install` (:247, :398, :403); never describes update/update.sh/codegraph registration. |

> CAUTION: docs/reference/troubleshooting.md is stale per the Section 2 currency check; treat its claims as advisory, not authoritative.

## Contradictions found by the worker

1. Release notes (:143-150, :69, :3) vs mcp-installation.md:70 and code (main.py:239-263 install runs codegraph + retire; main.py:407 update never touches MCP; update.sh:8 runs install --force): the two upgrade paths in the notes are not equivalent; only `./update.sh` installs codegraph and retires Serena.
2. Release notes :69 vs mcp-installation.md:54 on where Serena is retired (install, not update).
3. installation.md:326-333/:363/:53-57 describe upgrade as `update` only; installation.md:365 says `install --force` "does the same" as update (it also runs codegraph + retire).
4. mcp-installation.md:71 "`install --force` reinstalls framework files only" vs :7/:23 (likely means --force affects only framework files).
5. Unrelated stale content: troubleshooting.md:10.

## Open checks named by the worker

- What `update_notice()` prints when codegraph is not registered at all.
- Whether `superclaude doctor` passes when codegraph is entirely missing (release notes step 4 relies on it).
