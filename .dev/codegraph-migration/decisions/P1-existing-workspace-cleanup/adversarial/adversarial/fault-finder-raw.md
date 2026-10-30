# Round 2.5 Invariant Probe: Fault-Finder Raw Findings (P1 existing-workspace cleanup)

Target: the emerging "amended A" consensus (points 1-10) after Round 2.
Method: read context.md, option-a/b/c.md, diff-analysis.md, round1/round2 advocate transcripts; read-only spot checks of source at the worktree HEAD and `git log`/`git show` history. No tests, installers or `claude mcp` were run.

Counts: 14 findings. HIGH: 1 UNADDRESSED, 1 ADDRESSED. MEDIUM: 8 UNADDRESSED. LOW: 3 UNADDRESSED, 1 ADDRESSED.

---

ID: INV-001
CATEGORY: collection_boundaries
ASSUMPTION: The serena allowlist needs exactly two argv rows: the current pin and ONE "older IronClaude-only registry form" (pre-0e7bc31f `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false`).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The repo's own history shows the earlier installer `setup/components/mcp.py` registered serena at USER scope (`["claude","mcp","add","-s","user","--",server_name] + ...`) with at least four other argvs: `5bee1571` `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)` (split with `.split()`, so a literal `$(pwd)` token is stored); `43112779` `serena start-mcp-server --context ide-assistant --project $(pwd)` (command `serena`, not `uvx`); `00ec67c7` `uvx --from git+... --context ide-assistant` and `... --context ide-assistant --project <shlex.quote(cwd)>` (a per-user absolute path, which no allowlist can list). The one row the consensus adds matches only the `050d5ea2`..`0e7bc31f` form. Every other historical user-scope entry gets "kept: not an IronClaude registration", which is false. The `00ec67c7` code form `uvx --from git+... --context ide-assistant` is byte-identical to the doc-guided hand command (`claude mcp add serena -- uvx ... --context ide-assistant`). So the Round 2 "the `--enable-*` flags tell code from hand" discriminator (round2-advocate-b.md, round2-advocate-c.md) fails for that row. Its fallback, "hand entries land in local scope", depends on the CLI default scope, which is UNVERIFIED. Whether an entry written by pre-fork SuperClaude code counts as "IronClaude-owned" is never decided.
SUGGESTED RESOLUTION: Rebuild the allowlist from `git log -G'start-mcp-server' --all`. Add a rule for the `--project <abs path>` family (prefix match on the fixed tokens plus exactly one trailing path arg). Record an explicit ownership decision for pre-fork SuperClaude shapes.

ID: INV-002
CATEGORY: collection_boundaries
ASSUMPTION: IronClaude only ever wrote codebase-memory registrations with command `/usr/local/bin/codebase-memory-mcp` or `$HOME/.local/bin/codebase-memory-mcp`.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `discover_executable` falls back to the first runnable `Path(path_entry).absolute()/codebase-memory-mcp` on PATH (`install_codebase_memory.py:597-603`). `acquire_codebase_memory` reuses any `external` hit (`:643-650`), and the required install phase then writes `{"type":"stdio","command":str(executable),"args":[]}` (`install_mcp.py:866`, `:895`). Any workspace whose binary lived elsewhere (for example `/usr/bin`, `~/go/bin`, `/home/linuxbrew/.linuxbrew/bin`, `/opt/...`) holds an IronClaude-written entry that the tightened two-path allowlist (round1-advocate-a.md Concessions) labels "kept: not an IronClaude registration". Option A's original basename rule covered these cases; the tightening created this gap.
SUGGESTED RESOLUTION: Match any absolute `command` whose basename is `codebase-memory-mcp`, with stdio type, `args` absent or `[]`, and no env or headers (IronClaude wrote exactly this shape for every discovered path). Reserve a separate ownership tier only for the `$HOME/.local/bin` path (see INV-003).

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: "No IronClaude receipt" means IronClaude did not install the binary behind a `$HOME/.local/bin/codebase-memory-mcp` registration, so removing that registration automatically is safe and leaves no companions behind.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `acquire_codebase_memory` reuses a canonical `~/.local/bin` binary that has no receipt and no pending marker (`install_codebase_memory.py:640-650`), meaning a user or upstream installed it, not IronClaude. The upstream installer "configures detected clients and companion instructions, skills, agents and hooks" (`:668`), so it is a second possible writer of that same entry. In that case IronClaude only verified the entry (`install_mcp.py:864-865`) and wrote nothing. Separately, a `.pending` marker with no receipt (`:89-104`, `:707-708`) means an IronClaude-started upstream run was interrupted and may have left partial upstream companions. Consensus point 2 treats both cases as kind A: it removes the registration and prints no `codebase-memory-mcp uninstall` hint. The result is upstream skills, agents and hooks pointing at an unregistered server, and a registration IronClaude cannot prove it wrote is deleted. This violates the Round 2 rule that "shape proves ownership only when one writer is possible" (round2-advocate-b.md A-002 row).
SUGGESTED RESOLUTION: Gate on the binary, not only the receipt. If `$HOME/.local/bin/codebase-memory-mcp` exists (whether or not a receipt or `.pending` exists), keep the registration and print the absolute upstream uninstall. Remove automatically only when that binary is absent.

ID: INV-004
CATEGORY: interaction_effects
ASSUMPTION: Rule 2 (receipt present -> keep the registration and print the upstream uninstall) and rule 5 (delete the receipt once the binary is absent) are independent and need no order.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Upstream `uninstall` does not delete IronClaude's receipt; only IronClaude's own path unlinks it (`install_codebase_memory.py:362-369`). Once the user runs the printed command, the state is "receipt present, binary absent". If rule 2 is evaluated first in a run, the registration is kept and the install prints `codebase-memory-mcp uninstall -y` for a binary that no longer exists. Rule 5 then deletes the receipt, and the entry is removed only on the NEXT install. If rule 5 runs first, everything converges in one run. The consensus states no order, and its point 2 keys on receipt presence alone.
SUGGESTED RESOLUTION: Define the kind-B gate as receipt present AND binary present, evaluate receipt/marker cleanup (rule 5) before the registration rule, and add a unit test for the "receipt present, binary absent" case.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: The printed hand-off command `codebase-memory-mcp uninstall -y` targets the kind-B binary.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: IronClaude's own removal invokes the exact canonical path with an explicit directory: `[str(executable), "uninstall", "-y", f"--dir={executable.parent}"]` (`install_codebase_memory.py:352-355`). A bare name resolves through PATH. On a workspace that has both the Coder `/usr/local/bin` copy and `~/.local/bin`, or an alternate PATH entry (`_alternate_path_entries`, `:236-256`), the user may run the Coder-owned or a foreign binary's account-wide uninstall without `--dir`. That breaks point 9 ("IronClaude never removes Coder-owned software") by proxy.
SUGGESTED RESOLUTION: Print `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"` (absolute path, explicit dir), and only when that file exists.

ID: INV-006
CATEGORY: state_variables
ASSUMPTION: Reusing a name-parameterised `_cleanup_user_native_registration` keeps the shape guarantee "same-name entries with any other shape are kept" (point 4).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The existing helper does no shape check. It removes whatever user entry has the name (`install_mcp.py:916-934`), and `claude mcp remove <name> --scope user` is delete-by-name with no compare-and-swap. The consensus matches on one read and mutates through a second process. Two failure paths follow: an entry replaced between match and remove (for example a concurrent Claude session or the Coder bundle) is deleted whatever its shape, and a caller that forgets the matcher deletes user-made entries. Existing install code already guards a similar race explicitly ("never remove an entry that differs from it", `:884-885`, `:796-798`).
SUGGESTED RESOLUTION: Make the matcher a required parameter of the helper and re-read and re-match immediately before the remove. After removal, if a different-shaped entry is present, report it and never retry the remove.

ID: INV-007
CATEGORY: interaction_effects
ASSUMPTION: "10 s per retire CLI call" is a hard bound, and placing the step FIRST protects the rest of the install from Coder's 60 s kill.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `_run_registration_command` goes through `_run_command`, which runs `"$SHELL" -c '<quoted argv>'` with `shell=True` and `capture_output` (`install_mcp.py:129-141`, `:766-772`). On timeout Python kills only the shell. If the shell does not exec the command (for example fish, or rc-file work), the `claude` grandchild survives, keeps the pipes open, and `subprocess.run` blocks until it exits. The orphan may also persist the removal after IronClaude has reported "failed" (the "timed-out remove that persisted" case). With the step first, one hang can use up Coder's whole `timeout 60` budget (context.md:10,18), and Coder then kills install before ANY framework file is copied. That is worse than the status quo. Claude CLI cold-start time under `--network=none` is UNVERIFIED as under 10 s. Separately, the "missing `claude` -> skip" rule must use `shutil.which` (`install_user_setup.py:251-258` pattern). Through `_run_command`, a missing CLI exits 127 and is reported as a failure, not a skip.
SUGGESTED RESOLUTION: Exec `claude` directly (argv list, no shell, `start_new_session=True`, kill the process group on timeout), cap the whole retire step (for example 15 s) and skip the remaining CLI calls once the cap is reached, and detect a missing CLI with `shutil.which`.

ID: INV-008
CATEGORY: interaction_effects
ASSUMPTION: Verify-after-remove (re-reading `~/.claude.json`) proves the end state that `./update.sh` delivers.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `./update.sh` is typically run from a shell inside, or next to, live Claude Code sessions. Claude Code keeps `~/.claude.json` state in memory and rewrites the whole file, so a running session can write the removed `mcpServers` entry back after the verify read. The consensus lists no "restart sessions" note in points 1-10. It was accepted only in Round 1 (round1-advocate-a.md A-007, round1-advocate-c.md A-007), and A-004 was left as "risk the existing path already accepts". `superclaude doctor`, which runs right after install in `update.sh:10`, gains no check for this case, so an entry that comes back goes unseen until the next install.
SUGGESTED RESOLUTION: Print "restart all Claude sessions, then run `superclaude install --list` to confirm". Have `superclaude doctor` report any retired-name entry that matches the allowlist.

ID: INV-009
CATEGORY: sufficiency_challenge
ASSUMPTION: Placing the retire step in `superclaude install`, plus the `--force` refresh of hooks and core files, covers every existing-workspace upgrade path.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: (a) The docs tell users to "run `superclaude update` after upgrading" (`docs/user-guide/how-we-work.md:3`). `update` is a separate command (`main.py:352`, `install_core_files(force=True)` at `:377`) that is documented never to touch MCP state (`docs/user-guide/mcp-installation.md:24`), so it never reaches the retire step and both registrations stay. (b) Any `superclaude install` without `--force` (pipx users, Coder starts with no SHA change) skips existing core files (`install_core.py:62-66`) and skips refreshing the owned hook registration (`install_hooks.py:393-395`). Stale `~/.claude/CLAUDE.md`, `HOW-WE-WORK.md` and `RESEARCH_CONFIG.md` Serena mentions, and the `mcp__serena__*` PreToolUse matcher (`hooks.json:47`), therefore persist. Option A's claim that "the forced install rewrites the hook matcher and ~/.claude/CLAUDE.md" (option-a.md:20) holds only under `--force`. (c) Coder applies `--force` only on the SHA-change start (context.md:10). Whether a SHA-change run killed at 60 s is retried with `--force` is UNVERIFIED (Coder `catalogue/ironclaude/install.sh:91-95` is not in this repo). (d) The plugin mirror `plugins/superclaude/hooks/hooks.json` carries the same matcher, and `plugins/superclaude/mcp/configs/serena*.json` still ship.
SUGGESTED RESOLUTION: Run the same retire function from `superclaude update`. In the acceptance criteria, pin that the goal is only claimed for `--force` paths, list the non-forced residue, and add the plugin mirror to the Phase 1 search scope.

ID: INV-010
CATEGORY: sufficiency_challenge
ASSUMPTION: The consensus, applied alone, delivers the goal "leave no ... Serena MCP entry ... that IronClaude owns" on `./update.sh`.
STATUS: ADDRESSED
SEVERITY: HIGH
EVIDENCE: Point 3 keeps the current pin on every workspace, including non-Coder dev workspaces where `superclaude mcp --servers serena` (default `--scope user`, `main.py:288-292`) is the most likely writer. round2-advocate-c.md records this as a known goal miss. Together with INV-001 (other historic argvs kept) and INV-009 (paths that do not reach the step), the consensus delivers the goal only for the cbm entry and one serena row, and only on `--force` install paths. The miss is recorded, but the decision must not say "goal met".
SUGGESTED RESOLUTION: State in the decision record that the goal is "met except: current serena pin (all workspaces), unlisted historic serena argvs, non-`--force`/`update` paths", each with its closing condition.

ID: INV-011
CATEGORY: guard_conditions
ASSUMPTION: "Regular, single-link, user-owned file" plus "absolute `$HOME/.local/bin`" are sufficient and stable guards for receipt/marker deletion and path matching.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The existing predicates are stricter. Both files must also be private (`st_mode & 0o077 == 0`) and opened with `O_NOFOLLOW` (`install_codebase_memory.py:95-100`, `:185-199`), and `~/.local` and `~/.local/bin` must be non-symlinked, user-owned and not group- or world-writable (`_check_install_directory`, `:125-139`). The consensus drops these. Also, `canonical_executable()` uses `Path.home().absolute()`, which is unresolved (`:54-55`). The stored command therefore embeds `$HOME` as it was at write time, and a matcher that resolves symlinks, or a HOME that changed (a symlinked or relocated home), fails to match. The entry is then kept (fail-safe, but a silent goal miss).
SUGGESTED RESOLUTION: Reuse `_acquisition_pending`, the `_read_acquisition_receipt` checks and `_check_install_directory` exactly. Compare `command` against the unresolved `Path.home().absolute()` form and report a mismatch as "kept: path differs from current HOME".

ID: INV-012
CATEGORY: state_variables
ASSUMPTION: `read_user_mcp_entry` and `claude mcp remove --scope user` operate on the same configuration file.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The reader honours `CLAUDE_CONFIG_DIR` and treats an empty value as "unknown" (`install_mcp.py:731-736`). The CLI inherits the environment (`env=os.environ`, `:139-141`), but its resolution is UNVERIFIED (round1 A-004 responses). If the two diverge, the step warns on every install forever with no remediation text. An empty `CLAUDE_CONFIG_DIR`, or a duplicate key in `~/.claude.json` (`:722-727`), also produces a permanent "unknown" warning. All installers write `~/.claude` whatever `CLAUDE_CONFIG_DIR` says, so on such accounts the retired-primitive cleanup in INV-009 targets the wrong directory.
SUGGESTED RESOLUTION: Give the "unknown" warning a specific cause (unset/empty `CLAUDE_CONFIG_DIR`, parse failure, duplicate key) and the exact manual `claude mcp remove` command.

ID: INV-013
CATEGORY: count_divergence
ASSUMPTION: The read-only `--list` preview (point 8) and the mutating step reach the same verdict for each name.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The `--list` block is rewritten separately (`main.py:161-186`). The verdict depends on the allowlist plus receipt, `.pending` and binary state (points 2 and 5, INV-003, INV-004). If the preview and the step are coded separately, "will be removed" and the actual action can disagree, as the current `--list` already uses a matcher different from the one the installer uses (`_native_registration_matches`, `main.py:177-185`).
SUGGESTED RESOLUTION: Have one pure classifier `classify_retired(name) -> (verdict, reason)` that both `--list` and the step call, and pin it with a shared table-driven test.

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: On Coder, removing the older serena form or printing the current-pin removal command is harmless churn.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Coder's bundle registers `serena` "only if absent, on every workspace start" (context.md:11,19). Removing an older IronClaude form therefore hands the slot to Coder's current pin on the next start (a replacement, not a removal). The per-run line "remove it with `claude mcp remove serena --scope user`" invites users to delete a Coder-owned entry that comes back on the next start. Whether the bundle runs before or after `superclaude install` within one start is UNVERIFIED. Point 9 (the Coder handoff) is the stated closure.
SUGGESTED RESOLUTION: On workspaces where `serena-agent` is a uv tool (Coder signal, heuristic), word the line "kept: managed by the Coder bundle; removal will be undone at next start" instead of printing the remove command.
