# Codebase Memory Live Smoke Gate

**Status: PASSED, 2026-10-22.** Live smoke run by the operator in a disposable Coder workspace; evidence in [`live-smoke-evidence/`](live-smoke-evidence/). The original procedure text below is kept unchanged for provenance.

## Live Smoke Result (2026-10-22)

| Check | Result | Evidence |
|---|---|---|
| Code under test | Commit `c180cf39` on branch `CodebaseMemoryMCP`, installed with `uv tool install`; branch flags active | `smoke/source-commit.txt`, `smoke/which.txt` |
| Environment | Linux amd64 Coder workspace, operator's disposable account | operator report |
| Acquisition | Upstream `main/install.sh`, asset `codebase-memory-mcp-linux-amd64-portable.tar.gz`, checksum verified, version 0.12.1, binary SHA-256 `77745491…709` | `smoke/5-reinstall.log`, `smoke/native-version.txt` |
| Receipt | Created on acquisition; matches binary identity and hash; recreated after reinstall | `smoke/receipt-1.json`, `smoke/receipt-2.json` |
| Companion merge | Install adds lines and files only, with no existing line changed or removed, across Claude, Codex, OpenCode, Augment and Pi config. IronClaude hooks and the seeded user hook are intact. `~/.claude/CLAUDE.md` is untouched | `content/install.diff`, `content/seed-counts.txt` |
| Unrelated hook still runs | Seeded PreToolUse Bash hook fired during a live `claude -p` Bash call alongside upstream hooks | operator output `SMOKE_SEED_HOOK` |
| Registration and live query | User scope, stdio, absolute path, no arguments; real `list_projects` response (0 projects) | `smoke/2-mcp-get.txt`, `smoke/2-list-projects.txt` |
| Look-alike and other-scope entries | User look-alike entry and same-named project and local entries preserved through install and removal | `smoke/2-fixture-entries.txt`, `smoke/4-fixture-entries.txt` |
| Repeat install | No new download or install; only a settings backup added; dry-run and `--list` make no changes | `smoke/3-repeat.diff`, `smoke/3-*.log` |
| Removal | Binary, receipt and user entry removed. Graph cache sentinel and `activity.db` index kept. Updater `~/.local/bin/install.sh` left and reported. All 9 captured config files restored byte-for-byte to their pre-install state | `smoke/4-uninstall.log`, `smoke/4-localbin.txt`, `content/uninstall-vs-before.diff` (empty) |
| Update vs restore | `superclaude update` does not restore the removed tool; explicit `superclaude install` re-acquires with a fresh receipt; sentinel retained | `smoke/5-update.log`, `smoke/5-reinstall.log` |

Known residuals (upstream-owned, accepted):
- The first install appended a redundant PATH line (`~/.bashrc:291-292`, "Added by codebase-memory-mcp install"), which removal does not take out. Permitted by `source.md:94` (upstream shell/PATH changes).
- The first install created `~/.codex/AGENTS.md` and `~/.config/opencode/AGENTS.md`; after removal they remain as empty files.

Evidence limits:
- The first `smoke/` merge diff is invalid: its install command failed on a terminal paste glitch (exit 127) after an earlier unseeded install. The merge check was redone with full file contents in `content/`.
- The seeded `CLAUDE.md` marker was never written, because bash history expansion on `<!--` rejected the command. Coverage instead comes from `CLAUDE.md` being byte-identical across install and removal.
- The workspace still had the operator's real proxy/Codex configuration rather than fresh disposable credentials.

Task 7 documents the procedure; it does not execute or authorize downloads, native installation/removal, live client processes, release, staging, commit, push or publication. Documentation is frozen for independent QA; the parent owns the task ledger and Q0 pin.

## Operator Procedure and Pass Conditions

Follow [Release Gate: Separately Authorized Live Smoke](../../../../../docs/user-guide/mcp-installation.md#release-gate-separately-authorized-live-smoke).

- Obtain explicit approval first. Use a disposable Linux amd64/arm64 VM/container with a separate account and process namespace, with no host HOME/config/cache/credential/Docker-socket/project-MCP mounts or shared host processes. Changing HOME on the developer account alone is insufficient for account-wide native activation/removal.
- Provide clean UV/Claude CLI/curl/Bash and the approved IronClaude release wheel inside that environment. Use only disposable credentials if a client needs authentication. No new container harness or runbook script is required.
- Record approval, wheel identity, OS/architecture, moving bootstrap URL/observation time/source revision, release asset/checksum identity and actual installed native version/hash. A reviewed source SHA does not pin the bootstrap or verify the packaged binary.
- Perform fresh normal framework installation with full upstream companion setup. Compare unrelated user hooks/config/instructions/registrations against a baseline and framework files/hooks against the approved wheel. Inspect every detected client's actual changes.
- Verify exact user stdio registration and a real MCP `list_projects` response after client restart, not just registration text or a direct CLI query. Do not index a repository as an installation step or smoke workaround.
- Repeat framework and explicit MCP installation: require reuse with no new download/native installation/upgrade. Check list/dry-run are prompt-free and mutation-free.
- Remove through the confirmed native lifecycle. Require canonical binary and matching acquisition receipt absence, exact user-entry absence, unchanged graph/cache sentinel hashes, preservation of unrelated assets/project-local entries, and truthful retained-updater/alternate-PATH status. Do not manually delete residual assets to manufacture a pass.
- Confirm update does not restore the removed tool; a later explicit framework install restores it with fresh proof and retained sentinels. Keep redacted commands, exit statuses, query response and before/after evidence here before disposing of the environment.

**Stop rule:** if upstream overwrites unrelated framework/user assets, stop, keep release blocked and revise the integration with the user. No quiet binary-only fallback. Any failed or unverified pass condition leaves this gate blocked. Only separately authorized, reviewed live evidence can close it.

## Task 7 Coverage

| Acceptance area | Documentation surface |
|---|---|
| AC1: default/menu/flags/scope/platform/prerequisites | Installation guide default setup, quick start, scopes and prerequisites; reference native lifecycle. Linux-only automation follows `operator-direction.md`, superseding the frozen macOS portability requirement. Manual macOS/Windows setup is not a framework-phase bypass. |
| AC2: full upstream effects, consent, indexes, partial/external removal | Installation guide safe removal/outcomes and reference troubleshooting; receipt is created only by actual acquisition and must match canonical identity/hash. Updater/indexes stay; IronClaude residual cleanup is exact-user only. |
| AC3: trust, reuse/version, update, list/force/target/dry-run | Installation guide reuse/previews, command examples and reference native lifecycle; no adopt/skip/upgrade flags or indexing/handshake claims. |
| AC4: default provisioning versus optional runtime | Optional-design introduction and directly affected onboarding examples; other MCPs and native runtime fallbacks remain optional/unchanged. |
| AC5–6: real upstream release gate, no binary-only fallback | Operator procedure above and in the installation guide; execution remains pending and release blocked. |
| AC7: source-to-task traceability and exclusions | Crosswalk below; evidence stays in this task's artifacts directory. README changes are limited to affected install enumeration/comment. Existing install/MCP help already covers the new component; no code edit needed. |

## Frozen Source Crosswalk

| Source area | Owning tasks |
|---|---|
| Sections 1–2, 4: full bootstrap, discovery, bounded execution, exact registration | Tasks 1–2 |
| Section 5: verified canonical native removal, consent and retained indexes | Task 3 |
| Sections 3, 5: registry/menu, scopes, prerequisites, repeatable selection, dry-run | Task 4 |
| Sections 3–4: default framework phase, list/force/target, unchanged update | Task 5 |
| Section 7: isolated executable failure/safety regression matrix | Task 6 |
| Sections 6–8: focused docs, live release gate, explicit exclusions | Task 7 |

The unchanged source snapshot retains original macOS wording for provenance. `operator-direction.md` and current code/user direction define Linux amd64/arm64 automation. No general package-manager framework, dependency, bundled graph skill/agent, automatic upgrade, graph indexing, index deletion, general server uninstall, project-scoped native lifecycle or Windows integration was added by Task 7.

## Verification Evidence and Limits

Documentation work verified on 2026-10-20 in `/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP`.

- Read the actual worktree's relevant `main.py`, `install_mcp.py` and `install_codebase_memory.py` functions, frozen source, Task 7 ACs/constraints and operator direction. Serena's active-project view did not include the worktree's new module, so source reads, not that graph, grounded the behavior. Auggie context was obtained before edits; Context7 checked Claude MCP scope/query and upstream install/uninstall/read-only query contracts.
- Read-only help commands, both exit 0: `PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv PYTHONPATH=/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/src uv run --active --no-sync superclaude install --help` and the same prefix with `superclaude mcp --help`. Newly documented CLI options/selections were checked against these and the actual dispatch; no real install, MCP get/list, native version probe or upstream script ran.
- Direct `git show <Q0>:<path> | cmp - <absolute-worktree-path>` comparisons all exited 0 for the three product modules and the four Task 6 regression files against parent pin `8038c05f23306cd13728121421df996bc1343499`. Plain tree-to-worktree diff initially represented snapshot-added/untracked files as deletions; direct byte comparisons resolve that limitation. No Git mutation was performed.
- Documentation whitespace check: `git diff --check` over the four allowed existing documentation files exited 0. The gate file is new documentation, not live execution evidence.
- Prior Task 6 evidence (`t6-cli-regressions.txt` and `t6-qa.md`) records **242 passed, 1 skipped** in the focused four-file mocked suite. Task 7 did not rerun tests. The two documented legacy MCP mypy diagnostics remain a known failed product-typecheck result, not a clean bill of health.

**No live proof exists from Task 7.** Mocked suite success, source review, help output and documentation checks do not prove upstream merge safety, released-binary lifecycle behavior or a live MCP connection.
