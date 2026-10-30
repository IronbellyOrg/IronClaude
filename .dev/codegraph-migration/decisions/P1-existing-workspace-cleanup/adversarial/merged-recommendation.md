<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (option-a.md, architect advocate) -->
<!-- Merge date: 2026-10-29T17:10:00Z -->

# Decision: P1 existing-workspace cleanup (issue #323)

Read `../context.md` first. It holds the verified facts this record relies on (worktree at 55d40308).

<!-- Source: Base (original, modified) — matchers, gate and placement amended by Changes 1-7 -->
## 1. Decision

Adopt amended Option A. `superclaude install` gets an automatic, non-interactive, non-fatal retire step. It removes only user-scope MCP registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own two receipt/marker files once the binary they describe is gone. Proof is tiered by provenance: an exact shape that only IronClaude code could have produced is removed; a shape another writer (Coder's bundle, the upstream installer, a hand-typed docs command) could also have produced is kept and reported with the exact command to remove it. Nothing Coder-owned or upstream-owned is removed: no binary, no uv tool, no updater, no client companion. All data (indexes, caches, memories) is kept. The step is reached on every `superclaude install` run, not gated on `--force`, so both `./update.sh` (`update.sh:8`) and Coder's `ironclaude/install.sh` reach it.

<!-- Source: Base (original, modified) — Variant 2 R2 + INV-001/002/003/005 resolutions, Changes 1, 2, 3, 4 -->
## 2. What is removed automatically

**codebase-memory-mcp registration** (Change 2). A top-level user-scope entry is IronClaude-shaped when all hold:

- `command` is an absolute path whose basename is `codebase-memory-mcp`;
- `type` is `stdio` or absent;
- `args` is absent or `[]`;
- `env` and `headers` are absent or empty.

Reason: IronClaude's required phase registered whatever discovery found on PATH (`install_codebase_memory.py:597-603`, written at `install_mcp.py:866`).

**Binary gate** (Change 3). If the matched entry's `command` equals the unresolved `Path.home().absolute()/.local/bin/codebase-memory-mcp` AND that file exists, the registration is kept (a user or the upstream installer may have written it, `install_codebase_memory.py:640-650`). An entry whose `command` has the form `<some home>/.local/bin/codebase-memory-mcp` with a home other than the current unresolved `Path.home().absolute()` is kept and reported "kept: path differs from current HOME" (fail-safe; INV-011 resolution, which takes precedence over the general rule below; orchestrator post-merge fix). Every other matched entry (Coder's `/usr/local/bin`, any other external path, or the current-HOME `~/.local/bin` path whose binary is gone) is removed.

**serena registration, Tier R** (Change 1). Removed only on an exact argv match (`command` + `args`, as stored by `claude mcp add ... -- <tokens>`, `install_mcp.py:1142-1159`), with `type` stdio or absent and no `env`/`headers` (base guard retained). Rows are copied byte-exact from git history and each is pinned by a test:

| Row | Written by | `command` | `args` |
|---|---|---|---|
| (a) | IronClaude registry, `050d5ea2`..`0e7bc31f` | `uvx` | `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--enable-web-dashboard", "false", "--enable-gui-log-window", "false"]` |
| (b) | pre-fork `setup/components/mcp.py`, `5bee1571` | `uvx` | `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` |
| (c) | pre-fork `setup/components/mcp.py`, `43112779` | `serena` | `["start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` |

`$(pwd)` in rows (b) and (c) is the literal six-character token, not an expanded path. Why these rows prove code wrote them: row (a) differs from the hand-typed docs command of its time by the two `--enable-*` flags (`git show 0e7bc31f`, registry vs docs hunks). Rows (b) and (c) were stored by `subprocess.run([... "-s", "user", "--", name] + run_command.split(), shell=(sys.platform == "win32"))`, so no shell expanded `$(pwd)`; a human shell would have (re-verified by the orchestrator and advocates B and C; resolution-advocate-a.md QUALIFY satisfied). Pre-fork SuperClaude shapes count as IronClaude-owned (same `superclaude` installer lineage).

**IronClaude receipt and marker** (Change 4). Delete `~/.local/bin/.superclaude-codebase-memory.json` and `~/.local/bin/.superclaude-codebase-memory.pending` only when `~/.local/bin/codebase-memory-mcp` is absent AND each file passes the existing private-file predicates exactly: regular file, `st_uid == getuid()`, `st_nlink == 1`, `st_mode & 0o077 == 0`, opened with `O_NOFOLLOW` (`install_codebase_memory.py:95-100`, `:185-199`); and `~/.local` and `~/.local/bin` pass `_check_install_directory` (`:125-139`). Otherwise the files are listed, not deleted. These are the only files the step ever deletes.

<!-- Source: Base (original, modified) — Variant 3 handoff + INV-001 Tier K, Changes 1 and 3 -->
## 3. What is kept and only reported

**serena, Tier K** (kept; one printed line per run):

- The current pin `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false` (identical to `install_mcp.py:59`, today's docs command and Coder's bundle argv).
- The bare `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant` (pre-fork `00ec67c7`; byte-identical to the old doc-guided hand command).
- The `--project <absolute path>` family (`00ec67c7`; a per-user path no allowlist can list).
- Any other user-scope `serena` entry whose argv contains `start-mcp-server`.

Printed line: "Legacy Serena registration kept (IronClaude cannot prove it wrote it; Coder workspaces re-add it at start). Remove it yourself with `claude mcp remove serena --scope user`."

**Different-shape entries**: a `serena` entry without `start-mcp-server` is reported "kept: not a Serena launcher registration" (no hint). A `codebase-memory-mcp` entry that fails the Section 2 shape is reported "kept: not an IronClaude registration".

**Kind-B registration**: a matched `codebase-memory-mcp` entry pointing at the current-HOME `~/.local/bin/codebase-memory-mcp` while that file exists is kept (binary gate), and so is one pointing at a `~/.local/bin` path under a different home ("kept: path differs from current HOME").

<!-- Source: Base (original, modified) — step 4 list extended with Change 4 exception and permission/hook note -->
## 4. Never touched

- Local scope (`projects.*.mcpServers` in `~/.claude.json`) and project `.mcp.json`, whatever the entry name or shape.
- All binaries: Coder's root-owned `/usr/local/bin/codebase-memory-mcp`, `~/.local/bin/codebase-memory-mcp`, any other copy.
- uv tools (`serena-agent`, installed by Coder's bundle), the upstream updater `~/.local/bin/install.sh` ("The adjacent updater is left in place", `install_codebase_memory.py:74-78`), upstream client companions.
- Caches and indexes (`~/.cache/codebase-memory-mcp`), `~/.serena`, project `.serena/` folders.
- User permissions in Claude settings. IronClaude ships no permission entries for these servers; its only server-specific framework entry is the `mcp__serena__*` PreToolUse matcher (`src/superclaude/hooks/hooks.json:47`), which the existing installer refreshes in place under `--force` (`install_hooks.py:393-431`). The retire step does not edit it.
- Exception: the two IronClaude receipt/marker files in Section 2, under its predicates only.

<!-- Source: Base (original) — keep-indexes policy; delete commands from Change 9 -->
## 5. Data policy

Indexes and memories are KEPT, matching existing policy ("IronClaude does not erase companion/cache files", `install_codebase_memory.py:74-78`) and upstream `uninstall`, which keeps indexes unless `--delete-indexes` (context.md:17). The step prints delete commands for `~/.cache/codebase-memory-mcp`, `~/.serena` and project `.serena/` folders, labelled "only if you no longer need them". It never runs them.

<!-- Source: Base (original, modified) — step 6 plus INV-006/007/012 failure classes, Changes 6, 7, 9 -->
## 6. Failure semantics

The step is non-fatal: no outcome changes the `superclaude install` exit code. Why: `update.sh` runs under `set -euo pipefail` (`update.sh:2`), so a non-zero install exit would stop `make sync-dev` and `superclaude doctor` (`tests/cli/test_update_script.py:81-88`); a lookup failure must never block a framework install.

| Failure class | Behaviour and message |
|---|---|
| Lookup "unknown" | Warning names the cause (unset or empty `CLAUDE_CONFIG_DIR`, unreadable or unparseable file, duplicate key, non-object) and prints `claude mcp remove <name> --scope user`. |
| Entry changed before removal | Re-match fails: entry kept, reported, never retried. |
| Same shape after removal | Warning "could not verify", with the manual command. |
| Different shape after removal | "replaced concurrently, kept"; never retried. |
| Per-call timeout (10 s) | Process group killed; warning with the manual command. |
| Step cap reached (15 s) | Remaining CLI calls skipped with a warning; next install retries (the step is idempotent). |
| `shutil.which("claude")` is None | Skip note that prints the exact `claude mcp remove <name> --scope user` for each entry that would have been removed (covers alias-only `claude`). |
| Receipt/marker fails a predicate | File listed, not deleted. |
| Any other exception | Caught by the step's own `try/except Exception`; warning only. |

<!-- Source: Base (original, modified) — placement replaced per INV-007, Changes 5 and 7 -->
## 7. Placement, ordering and bounds

**Placement.** After all framework-file steps, in the slot of the deleted codebase-memory phase (`main.py:254`), before the exit-code block (`main.py:264`), inside its own `try/except Exception` that only warns. Framework files never wait on a Claude CLI call; a run killed by Coder's 60 s bound simply retries next install. Condition (UNVERIFIED but plausible): the deleted phase frees more than the step's 15 s.

**Ordering.** One pure classifier reads all state once (entries, binary existence, receipt, marker); actions then run in a fixed order: (1) receipt/marker cleanup, (2) codebase-memory registration, (3) serena registration. A "receipt present, binary absent" workspace converges in one run.

**Bounds.**

- Exec `claude` directly (argv list, no `$SHELL -c`). The existing `_run_command` runs `$SHELL -c` with `shell=True` (`install_mcp.py:129-141`), so its timeout kills only the shell.
- `start_new_session=True`; kill the process group on timeout.
- 10 s per call; 15 s cap for the whole step.
- Missing CLI detected with `shutil.which("claude")` before any call.
- No subprocess runs when no entry needs removal (zero cost on fresh workspaces).

<!-- Source: Variant 3 (U-005, cheaper form) + INV-008/009, Change 8; Base step 5 modified by Change 9 -->
## 8. Read-only surfaces and user-facing messages

**Read-only surfaces** (all call the same classifier, never mutate):

- `superclaude install --list`: the codebase-memory block (`main.py:161-186`, which calls code Phase 1 deletes) is replaced by one line per retired name: "absent", "will be removed (IronClaude shape)" or "kept: <reason>".
- `superclaude doctor`: warns, never fails, when the classifier still finds a removable entry (`update.sh` exit unchanged).
- `superclaude update`: prints only "legacy registration present: run `superclaude install`". It keeps its documented never-touches-MCP contract (`docs/user-guide/mcp-installation.md:24`).

**Messages** (one line per action):

- After any removal: "Restart running Claude sessions; a running session can write the entry back. Check with `superclaude install --list`."
- After a codebase-memory removal: "If you installed codebase-memory-mcp yourself, its own `uninstall` removes its client companions."
- After a Tier R serena removal: the exact removed `command` + `args`, plus "To keep using Serena, register it yourself, e.g. `claude mcp add --scope user serena -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`" (option order mirrors IronClaude's own call, `install_mcp.py:1142-1159`) (advocate C's Round 2 condition for accepting Tier R removal, round2-advocate-c.md §2; orchestrator post-merge fix).
- Whenever `~/.local/bin/codebase-memory-mcp` exists, whatever entry matched: `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"`, labelled "for a codebase-memory you or IronClaude installed under ~/.local/bin; removes its own client companions, keeps indexes". Never a bare `codebase-memory-mcp uninstall` (it could resolve to Coder's copy via PATH).
- `uv tool uninstall serena-agent`, labelled "if you installed it yourself; Coder workspaces reinstall it at start".
- The Tier K serena line (Section 3), cause-specific "unknown" warnings (Section 6), and the data delete commands (Section 5).

<!-- Source: Base (original, modified) — Implementation paragraph, Changes 5, 6, 7 -->
## 9. Implementation outline

- One small module (or a block in `install_mcp.py`) holding a `RETIRED_MCP_SERVERS` table of name -> matcher. Comment on the table: "remove after the first release in which Coder's image and bundle no longer ship either server" (a later cleanup task).
- `classify_retired_entries() -> list[(name, verdict, reason)]`: pure; reuses `read_user_mcp_entry(name)` (`install_mcp.py:714-754`); shared by install, `install --list`, `doctor` and `update`.
- `_remove_exact_user_entry(name, matcher)`: matcher is a required parameter; re-reads and re-matches immediately before `claude mcp remove <name> --scope user`; re-reads after (absent -> removed; same shape -> "could not verify"; different shape -> "replaced concurrently, kept", never retried). It replaces the name-only `_cleanup_user_native_registration` (`install_mcp.py:916-948`). Phase 2's codegraph registration reuses it.
- A direct-exec CLI wrapper with the Section 7 bounds.
- The new code names both retired servers, so the Phase 1 acceptance search needs an allowlist entry for this module until the sunset task removes it.

<!-- Source: Variant 3 step 4 + INV-009d + INV-014, Change 10 -->
## 10. Handoffs

- **Coder (Phase 2 handoff):** stop the bundle registering and installing Serena, drop the image's codebase-memory binary, remove any Coder-owned startup registration. Until then Coder's bundle re-adds `serena` at each workspace start; no Coder-detection heuristic is added (the Tier K line already says so).
- **Plugin mirror (Phase 1 search scope, not this step):** `plugins/superclaude/hooks/hooks.json` (same matcher) and `plugins/superclaude/mcp/configs/serena*.json`.
- **Upstream uninstaller:** a `~/.local/bin` codebase-memory binary and its client companions are left to the printed absolute upstream `uninstall` (Section 8).

<!-- Source: INV-010 + round2-advocate-c.md residual statement + invariant-probe.md residuals, Change 11 -->
## 11. Goal status: met except

The goal is claimed for `./update.sh` and Coder SHA-change runs (both `--force`). It is met except:

| Exception | Closing condition |
|---|---|
| Current serena pin kept on every workspace, including non-Coder dev workspaces where `superclaude mcp --servers serena` most likely wrote it | A verified Coder-workspace signal exists, or Coder's bundle stops registering Serena (Phase 2); the sunset task then removes the row automatically |
| Other Tier K serena rows (bare `--context ide-assistant`, `--project <abs path>`, other `start-mcp-server` entries) kept | IronClaude cannot prove ownership; closes when the user runs the printed command |
| Non-forced installs keep stale core/hook text (Serena mentions in `~/.claude/CLAUDE.md`, `HOW-WE-WORK.md`, `RESEARCH_CONFIG.md`; `hooks.json:47` matcher) | Next `--force` install; non-forced runs already print "Skipped N existing files (use --force to overwrite)" (`install_core.py:82-87`) |
| `superclaude update` does not remove registrations | Prints the read-only notice; next `superclaude install` |
| Coder re-adds `serena` at each start | Phase 2 Coder handoff |
| Kind-B `~/.local/bin` binary and upstream companions left | User runs the printed absolute upstream `uninstall`; next install then removes the registration and receipt/marker |
| Whether a Coder SHA-change run killed at 60 s is retried with `--force` is UNVERIFIED (Coder `install.sh:91-95` not in this repo) | Confirm in the Coder repo |

**Residual risks (accepted):**

- `claude mcp remove` is delete-by-name, so a sub-second window between re-match and removal remains (INV-006).
- CLI-side `CLAUDE_CONFIG_DIR` resolution is UNVERIFIED; reader and CLI could diverge (INV-012).
- A running Claude session can write a removed entry back until restarted (INV-008).
- A `claude` defined only as a shell alias is skipped, with the manual command printed (INV-007).
- A hand-made entry identical to an IronClaude shape is removed; it is restorable with one command.
- Statement from round2-advocate-c.md: "On non-Coder workspaces, a user-scope `serena` entry that exactly matches the current `serena-agent==1.7.0` pin is kept, not removed, because IronClaude cannot tell it from the identical entry Coder's bundle writes. This leaves one IronClaude-written registration of a retired server. It still works (uvx fetches the pinned package; it depends on no binary the image stops shipping), needs no privilege, and `superclaude install` prints the exact one-line removal command on every run. The gap closes when a verified Coder-workspace signal exists or when Coder's bundle stops registering Serena (Phase 2 handoff); the sunset task then removes this entry automatically."

<!-- Source: Base (original, modified) — "4-6 unit tests plus one CLI integration test", expanded by Change 12 -->
## 12. Acceptance tests

- **Classifier (table-driven):** every Tier R row (removed); every Tier K row (kept, line printed); near-miss rows (one token changed, extra or missing arg, expanded `$(pwd)`); non-empty `env`/`headers` (kept); relative cbm command (kept); cbm `~/.local/bin` path under a different home (kept, "path differs from current HOME"); local-scope and project `.mcp.json` entries ignored; binary, receipt and marker states, including "receipt present, binary absent" converging in one run.
- **Helper:** concurrent replacement between match and remove (kept, not retried); verify failure (warning).
- **Bounds:** stub `claude` that hangs (process group killed, 15 s cap honoured); missing CLI (skip note with manual commands).
- **CLI integration:** temp HOME, stub `claude`; install exit code unchanged when the step fails.
- **Unchanged contract:** `update.sh` command list and order unchanged (`tests/cli/test_update_script.py:13-18`).

<!-- Source: refactor-plan.md "Changes NOT Being Made" -->
## 13. Rejected alternatives

- B: `uv tool uninstall serena-agent` (+ `uv cache clean`): Coder installed it with no receipt; breaks Coder's `serena --help` health check and churns. B conceded (R1).
- B: automated receipt-gated upstream uninstall, keeping a slimmed `install_codebase_memory.py` for a release: keeps the 759-line module and its 300 s path (`install_codebase_memory.py:28`) for unverified kind-B workspaces; prompt-free account-wide uninstall is what `install_mcp.py:981-986` forbids. B withdrew (R2).
- B: delete the updater `~/.local/bin/install.sh`: upstream file; policy leaves it in place (`install_codebase_memory.py:74-78`). B conceded.
- C: no automatic step, `superclaude mcp --retire-legacy [--dry-run] [--yes]` with interactive confirm: fails the goal on `./update.sh` (X-003); prompt-free exact-entry removal is existing behaviour (`install_mcp.py:874-895`). C withdrew (R2).
- C: separate `--dry-run`: replaced by the read-only `install --list` line from the shared classifier.
- A (original): basename + substring serena matcher: misses IronClaude-written rows and matches hand-made ones (A-001, INV-001).
- A (R2): place the step first: the `$SHELL -c` timeout is not a hard bound; framework files must not wait on a CLI call (INV-007).
- C (R2): Coder detection via the `serena-agent` uv tool: unverified signal; would change wording only (INV-014).

<!-- Source: debate-transcript.md + base-selection.md + invariant-probe.md -->
## 14. Debate summary

- Base selection: Option A 0.877, Option C 0.730, Option B 0.717 (`adversarial/base-selection.md`); A won or co-won 21 of 23 debate points.
- Convergence: 100% (23 of 23 points) after two rounds plus a resolution round (`adversarial/debate-transcript.md`).
- Invariant gate: blocked after Round 2.5 by INV-001 (HIGH); cleared when all 14 findings were resolved with unanimous ACCEPT or additive QUALIFY (`adversarial/invariant-probe.md`, `adversarial/invariant-resolutions-proposed.md`, `adversarial/resolution-advocate-{a,b,c}.md`).
- Merge plan and log: `adversarial/refactor-plan.md`, `adversarial/merge-log.md`.
