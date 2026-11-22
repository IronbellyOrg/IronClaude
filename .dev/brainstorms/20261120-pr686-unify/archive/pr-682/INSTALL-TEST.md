# INSTALL-TEST: does PR 697 restore the launch guard and worker contract on a host that installed post-682 master?

Date: 2026-11-20
Sources: origin/master 7f0919345479007ad72724dd16b4e4cf08136e65 (contains PR 682 commit 01e7a9e23, checked with `git merge-base --is-ancestor`), origin/ironbelly/revert-pr-682 fd23c01a9ca1f5aee44522f8107a07104f780c4f (PR 697).
Status: COMPLETE

## 1. Conclusion (plain English)

**Only after a named change.** A host that installed post-682 master and then runs plain `superclaude install` from PR 697's tree does NOT get the restored guard or the restored contract. The installer keeps every file that already exists, and it never looks at the `# launch-level-guard-version: 1` stamp. The files are replaced only by `superclaude install --force` or by `superclaude update` (which always forces). With `--force` both files became byte-identical to PR 697's source, with no `.bak` copy of either.

Two more facts that matter:
- For the contract, plain `install` prints a warning that the kept file differs and was NOT updated. For the hook scripts it prints only "Skipped 18 existing script(s)" with no "differs" warning, so a stale guard is skipped silently.
- The only consumer of the version stamp is the launch claim check in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:986-987`, which only tests that the stamp line is present. The stamp is the same in post-682 master (guard without rule 1) and in PR 697 (guard with rule 1), so that check passes on a stale post-682 guard. Bumping the stamp to 2 would not make the installer overwrite anything; it would only make the claim check (constant at `orca_worktree.py:839`) refuse a host that kept the old file, and that constant would need to change in the same PR.

## 2. Installer overwrite rule (file:line)

Paths are in `src/superclaude/cli/` (identical in master and PR 697: `cmp` of install_core.py, install_hooks.py and install_keep.py reported identical).

- Core files, `install_core.py:71-73`: `if dest_file.exists() and not force: skipped.append(...); continue`. Existence only. No hash, no stamp, no mtime. Overwrite at `:76` is a plain `shutil.copy2`, no backup.
- Core stale notice, `install_core.py:97-107`: for skipped files it runs `same_content` (`install_keep.py:18-27`, `filecmp.cmp(..., shallow=False)`, byte compare) and only prints "kept file(s) differ ... NOT updated (run with --force or `superclaude update`)". It never changes the file.
- Hook scripts, `install_hooks.py:282-284`: same rule, `if dest_file.exists() and not force: skipped.append(dest_name); continue`. Overwrite at `:287-288` is `shutil.copy2` plus `chmod 0o755`, no backup. The skip message at `install_hooks.py:205-210` has no differs check.
- `launch-level-guard.sh` is in the installed list at `install_hooks.py:93`; `WORKER-CONTRACT.md` at `install_core.py:28`.
- `install` passes `force` from the flag: `main.py:180` (core) and `main.py:219` (hooks). `update` hard-codes `force=True`: `main.py:383` and `main.py:412`.
- `settings.json` is merged with a timestamped backup on every run (`install_hooks.py:334-340`); that is the only `.bak` the installer writes for this path.

## 3. Why the real CLI was not run (installer steps that cannot be skipped)

`uv run superclaude install --help` offers only `--target`, `--force`, `--list`. There is no flag to select hooks and core only. Running the whole command or `update` would also run:
- codegraph phase, `main.py:244-255` (`install_codegraph_mcp`): required phase, downloads a pinned binary (network; `install_codegraph.py:328` verifies a sha256 of the downloaded archive). `install` only.
- `wire_ccsession`, `main.py:211` / `:406`: `subprocess.run` calls at `install_ccsession.py:94, 108, 133`.
- `install_user_setup`, `main.py:238` / `:422`: runs `orca skills install --agent claude-code` (`install_user_setup.py:289-296`, called at `:505`) and looks up the `claude` binary (`:371`).

None of those can be switched off by a flag, and the brief says to stop rather than run them. So I called the same two functions the CLI calls for these steps, with the same arguments the CLI passes, against the fake home. `superclaude install` step 1 is `install_core_files(force=force)` and step 5 is `install_hooks(force=force)`. This is the exact overwrite logic, but it is NOT the full CLI run (see UNVERIFIED).

## 4. Commands run and results

Throwaway home env used on every installer command: `HOME=/tmp/ic-inst/home XDG_CONFIG_HOME=/tmp/ic-inst/home/.config XDG_CACHE_HOME=/tmp/ic-inst/home/.cache XDG_DATA_HOME=/tmp/ic-inst/home/.local/share`. `UV_CACHE_DIR=/home/coder/.cache/uv` (the real uv cache, so dependencies resolved offline), `uv run --offline --link-mode=copy`, and `UV_PROJECT_ENVIRONMENT=/tmp/ic-inst/venv-<tree>` so no `.venv` was created inside any tree. The only write outside /tmp/ic-inst is uv's own cache entries under /home/coder/.cache/uv (new archive entries from building the package).

1. `git fetch origin` then `git rev-parse`: master 7f09193..., PR 697 branch fd23c01.... OK.
2. `mkdir /tmp/ic-inst/{master,pr697,home}`, `touch /tmp/ic-inst/marker`, BEFORE sha256 and stat of the two real files (section 5). OK.
3. `git -C /home/coder/workspaces/IronClaude archive origin/master | tar -x -C /tmp/ic-inst/master` and the same for `origin/ironbelly/revert-pr-682` into `/tmp/ic-inst/pr697`. OK. The PR worktree, the main checkout and the snapshot folders were not used as install sources; the PR worktree was only read with Read/Grep (its `git status --short` is empty).
4. `uv run --offline superclaude install --help` in /tmp/ic-inst/pr697: OK, options as in section 3.
5. Narrow installer script `/tmp/ic-inst/narrow_install.py` (calls `install_core_files(target_path=<fake>/.claude, force)` and `install_hooks(target_path=<fake>/.claude/settings.json, force)`; prints the module paths, which showed it imported from the tree under test).
6. Step A: from /tmp/ic-inst/master, no `--force`. Exit 0. Core: installed 12 files. Hooks: copied 18 scripts, settings merge `added=18`, seeded 1 data file.
7. Step B: from /tmp/ic-inst/pr697, no `--force`. Exit 0. Core: "Skipped 12 existing files" plus "1 kept file(s) differ from this version and were NOT updated: WORKER-CONTRACT.md". Hooks: "Skipped 18 existing script(s)", settings merge `added=0 skipped-existing=18` with a `settings.json.bak.<stamp>`.
8. Step C: from /tmp/ic-inst/pr697 with `--force`. Exit 0. Core: installed 12 files. Hooks: copied 18 scripts, settings merge `replaced=18` with another `settings.json.bak.<stamp>`.
9. AFTER sha256 and stat of the real files, `find` for stray writes (sections 5 and 7).

## 5. Hashes

Real files, before and after (read-only checks; `diff` of the saved before/after outputs printed SHA IDENTICAL and STAT IDENTICAL):

| File | sha256 before = after | mtime before = after |
|---|---|---|
| /home/coder/.claude/hooks/launch-level-guard.sh | 3f1c5da85c1b3b78680bff1dea2fa9dd5cef3571d89f5f6847667fda27988b8d | 2026-11-18 06:21:59.260490510 +0000 |
| /home/coder/.claude/WORKER-CONTRACT.md | 61ed5bdf8634c1dd9a1d8b33a3da700a9f89ec25eceb4f5f55092632410ed970 | 2026-11-18 06:21:59.239490028 +0000 |

Side note: the real machine's guard still contains `release-worker` (1 match) and its contract still has "Issue pipeline duties" (1 match), and neither hash equals master's or PR 697's source. So this machine holds an older install than post-682 master. It is not a "post-682 host" for this question, which is why a fake home was needed.

Source files:

| Tree | launch-level-guard.sh sha256 | stamp line 10 | `release-worker` count | WORKER-CONTRACT.md sha256 | "Issue pipeline duties" count |
|---|---|---|---|---|---|
| master (post-682) | a561b1a7e7e732b8411c41631c31c6503068f28133d8e1f0de0446384182efb6 | `# launch-level-guard-version: 1` | 0 | d74a0c7b1862e9cbec63504d67730b80f964ee2a4cd1cffbb58e58625893eacf | 0 |
| PR 697 | 71e479dd10760d2319a596693d367fed1e419e884cd56bec7d0e4f0938ba81c9 | `# launch-level-guard-version: 1` | 1 | d5154450ae2462eb107ca36eca2d334ef0820c2abdae7ddf08f6e613fb4fb9e3 | 1 |

Fake home after each step:

| Step | guard sha256 | contract sha256 | `release-worker` | "Issue pipeline duties" |
|---|---|---|---|---|
| A (master, no force) | a561b1a7... (= master source) | d74a0c7b... (= master source) | 0 | 0 |
| B (PR 697, no force) | a561b1a7... (unchanged) | d74a0c7b... (unchanged) | 0 | 0 |
| C (PR 697, --force) | 71e479dd... (= PR 697 source) | d5154450... (= PR 697 source) | 1 | 1 |

`.bak` files: none for the guard or the contract in any step (core and hook overwrites at `install_core.py:76` and `install_hooks.py:287` do not back up). The only `.bak` files in the fake home are two `settings.json.bak.<stamp>` files from steps B and C.

## 6. Step A / B / C findings

- Step A: confirmed. After installing master, the fake guard has NO `release-worker` text and the fake contract has NO "Issue pipeline duties". The stamp line is present.
- Step B: NOT replaced. Guard and contract are byte-identical to the post-682 versions. No `.bak`. The contract gets a stale warning; the guard gets none.
- Step C: the rule that skipped them is the existence check (`install_core.py:71-73`, `install_hooks.py:282-284`). What makes them update: `--force` or `superclaude update`. A stamp bump alone does nothing, and a changed hash alone does nothing, because the installer never reads either.

## 7. Cleanliness of the real home

- Installer-owned paths in the real `~/.claude` (hooks, settings.json, WORKER-CONTRACT.md, CLAUDE.md, templates, skills, agents, commands): nothing newer than the marker. No new `.bak` files.
- `find /home/coder/.claude -newer marker -type f` listed 6 files, all live-session writes by running sessions, not by this test: `state/tool-call-counter/<this session id>.txt` and its `.lock`, `state/reads.jsonl`, `backups/.claude.json.backup.<n>`, and 2 transcript files under `projects/-home-coder-workspaces-IronClaude`. Also changed outside `.claude`: `~/.claude.json`, `~/.config/orca/` runtime files, `~/.local/share/{tailscale,code-server}` logs, which belong to the running Orca/Coder processes. The fake HOME was set on every installer command, so this test did not target those paths.
- uv cache: new entries under `/home/coder/.cache/uv` (allowed by the brief; this is the only intended write outside /tmp/ic-inst).
- Repository: no write, no stage, no commit; the PR worktree `git status --short` is empty. No GitHub or Orca call was made.

## 8. UNVERIFIED

- The full `superclaude install` and `superclaude update` commands were not executed (they run the network codegraph phase, ccsession subprocesses and `orca skills install`). Their hook and core steps call the functions tested here with `force=force` and `force=True` (`main.py:180, 219, 383, 412`), so the same outcome is expected, but it was not observed through the CLI.
- Which command the owner's hosts actually run (`install`, `install --force`, `update`, or a Coder template that only copies files) was not checked. The conclusion for a given host depends on that.
- Whether a host's installed `settings.json` hook registrations still point at the installed guard path was not tested (the fake home was fresh, so registrations were created by step A).
- The behavior of `--force` on user-edited files elsewhere (rules, output styles) was not tested; only the guard and contract were measured.
