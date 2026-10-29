# P2 review report: Phase 2 spec and Coder handoff (issue #323)

Reviewer: independent adversarial review, read-only, 2026-10-29. Deliverables: A = `specs/phase-2-codegraph-install-spec.md`, B = `handoff/coder-handoff-prompt.md`, C = `handoff/coder-handoff-context.md` (all under `.dev/codegraph-migration/`).

## Verdict: FAIL

18 findings: 0 CRITICAL, 7 IMPORTANT, 11 MINOR. The structure is complete and most citations are accurate. The failures are in the indexing hook design, in a registration premise that was never checked, in commands that would fail as written, and in the missing trigger for the Coder prerequisite.

## Findings

1. **IMPORTANT. The hook's rebuild rule races with a live daemon or an init still running, and the guidance makes a redundant rebuild certain.** A:205-207 (§3.2 step 5), A:190, A:192, A:222, A:537 (D3).
   - Evidence: when a database exists without the marker, the hook runs `codegraph index <top>` (a full rebuild). That state occurs in four cases:
     - a second session starts while the first session's background `init` is still running;
     - the agent follows the A:222 guidance and runs `codegraph init --yes` itself, which writes no marker;
     - a user runs `init` themselves;
     - Coder pre-builds the index (A:192).
   - In every case the session's own MCP daemon is starting or running (`alwaysLoad`), and A:222 itself says "the MCP daemon owns the index". C:23 says `codegraph sync` fails with a lock error while the daemon runs.
   - `probe-results.md:7-8` tested only init against init with no daemon. Neither `index` against a running `init` nor `index` against a live daemon was probed. The A:222 guidance also tells the agent to run `codegraph index` during an open session.
   - Fix: decide from `codegraph status`. If the last run is complete, only touch the marker; if it is truncated, run `index`. Probe `index` against a live daemon and against a running `init` before shipping, and align the CLAUDE.md text with the result.

2. **IMPORTANT. The core CLAUDE.md fallback guidance never reaches Coder workspaces.** A:38 (F6), A:187, A:216-224.
   - Evidence: `research/install-update-flow.md:89` states "On a Coder workspace the core `CLAUDE.md` does not reach the user". Coder's slug saves and restores `~/.claude/CLAUDE.md` byte for byte (`:232`, Coder `catalogue/ironclaude/install.sh:44-66,112-125`).
   - A's §3.1 row 2 relies on that guidance as the fallback for sessions that start before the index exists. B:32 and C:101 mention the save/restore but draw no conclusion from it.
   - Fix: state the gap in A §3.4. Require in B that Coder carry the same codegraph block in `T/workspace_defaults/CLAUDE.md`, including a migration for existing workspaces whose seed is never re-copied, or choose another delivery channel.

3. **IMPORTANT. A required phase rests on an unverified CLI behaviour.** A:89, A:96-98, A:176.
   - Evidence: the phase passes only if re-reading `~/.claude.json` after `claude mcp add-json` gives an entry equal to the expected one, comparing the whole entry (type, command, args, env, alwaysLoad).
   - `research/codegraph-evaluation.md:77` says neither registration command was run; only the argv shape came from `--help`. Nobody has shown that the CLI stores `alwaysLoad` and `env` unchanged.
   - If it drops or normalizes a field, every install exits 1, which also fails Coder's slug. The only real-CLI check is T9, in the last task group.
   - Fix: add a sandbox probe to T2 before its commit: isolated `CLAUDE_CONFIG_DIR`, a real `claude mcp add-json`, then `jq` the stored entry. Compare only the fields that probe shows are kept.

4. **IMPORTANT. The layer-2 script (§4.2) cannot run on a Coder workspace, and the T9 real-HOME check proves nothing.** A:283, A:287-292, A:302, A:421.
   - Evidence: the PATH filter drops `/usr/local/bin`, but `command -v` on this workspace gives `/usr/local/bin/claude` and `/usr/local/bin/uv`. Step 1 therefore fails with `uv: command not found` under `set -e`, and the phase would fail on `claude --version` anyway.
   - T9 checks `~/.claude.json` "before and after", but the script has run `export HOME=$S/home`, so `~` points at the sandbox (deleted in step 5), not at the real file.
   - No `trap` cleans up on failure. The step-2 `uv run` under the dead proxy has no `--no-sync`.
   - Fix:
     - Put symlinks for `claude`, `uv`, `git` and `jq` in a `$S/bin` shim dir and build PATH from it, so a baked codegraph stays hidden.
     - Capture `REAL_HOME=$HOME` before the export and check `"$REAL_HOME/.claude.json"`.
     - Add `trap 'rm -rf "$S"' EXIT`.
     - Use `uv run --no-sync`.

5. **IMPORTANT. The T11 acceptance command fails as written.** A:443.
   - Evidence: running `gh pr view --repo IronbellyOrg/IronClaude --json url -q .url` gives "argument required when using the --repo flag", exit 1 (gh 2.103.3, tested).
   - Fix: `gh pr view ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude --json url -q .url`.

6. **IMPORTANT. Nothing starts the Coder prerequisite.** A:497-508 (§8), A:482-486 (§7 human list), B:22.
   - Evidence: steps 1-2 must merge on Coder before T11 can merge, but no task commits or pushes the handoff files, and none gives B to a Coder agent or opens a Coder issue.
   - `git status` shows `?? .dev/codegraph-migration/` (nothing tracked), so B:22's `gh api .../contents/...?ref=<branch>` would return 404.
   - Fix:
     - Add a task early in A that commits the spec and handoff files and starts the Coder work with B, or list it as a human step in §7.
     - Make T11's gate verify that Coder steps 1-2 are merged.

7. **IMPORTANT. The hook and the guidance assume `codegraph` is on PATH, but the installer guarantees only an absolute path in the registration.** A:79, A:201, A:222, U22 (A:259).
   - Evidence: on a fallback install the launcher is `~/.local/bin/codegraph`, which is often not on PATH (macOS by default). There `command -v codegraph` fails, the hook exits silently, and the guidance's `codegraph init --yes` gives "command not found".
   - When a non-owned older `codegraph` is on PATH (the U22 case), the hook indexes with a different version than the registered MCP server.
   - Fix: make the hook resolve the same binary the registration uses (for example `~/.codegraph/current/bin/codegraph` when it is owned, or a path the installer records). Alternatively, have the installer warn when the chosen binary is not first on PATH. Add both cases to the hook tests.

8. **MINOR. The baseline cannot detect a swapped failure.** A:316, A:319, A:433.
   - Evidence: `--tb=no ... | tail -3` keeps only the summary count, in `/tmp`, which a multi-session executor can lose. "No more failures than baseline" does not catch a new failure that replaces an old one.
   - Fix: store the full `FAILED|ERROR` list in the task package and diff it the way Phase 1 T14 does (`phase-1-removal-spec.md:683`).

9. **MINOR. The T7 acceptance proves only a total.** A:404.
   - Evidence: `rg -n 'codegraph' <4 files> | wc -l # expect: > 0 in every file` counts matches across all four files, not per file.
   - Fix: `for f in README.md docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md CHANGELOG.md; do rg -q codegraph "$f" || { echo "missing: $f"; exit 1; }; done`.

10. **MINOR. The T1 pin check is fragile and manual.** A:327.
    - Evidence: `gh release download ... -D /tmp/p2-sums` fails on a re-run because the file already exists. "Must print the four §0 lines exactly" is checked by eye.
    - Fix: add `--clobber`, then `diff` against a heredoc of the four expected lines.

11. **MINOR. The ordering rationale contradicts the required test.** A:35, A:59 versus A:262.
    - Evidence: codegraph is ordered before the retire step "so the replacement is registered before the old servers are removed", yet A:262 requires the retire step to still run when the codegraph phase fails. A failed phase therefore leaves neither server.
    - Fix: either drop the rationale or gate the retire step on codegraph success (coordinate with Phase 1 §3).

12. **MINOR. Wrong citation.** A:232.
    - Evidence: `tests/cli/test_install_mcp_tavily.py:404-406` is cited for "calls `pytest.fail`", but those lines hold fixture fields and `monkeypatch.setenv("HOME", ...)`. The `pytest.fail` is at `:416`.
    - Fix: cite `:410-416`.

13. **MINOR. The hook prose has a shell bug if copied literally.** A:205.
    - Evidence: written as `cmd=init --yes`, POSIX sh runs a command named `--yes` with `cmd=init` in its environment.
    - Fix: `cmd='init --yes'`.

14. **MINOR. The "receipt-owned interrupted run" branch can never happen.** A:78, A:80, A:110.
    - Evidence: the receipt is written last (step 7), so a run interrupted after the rename or link steps leaves a dir and links that are never receipt-owned. They are reused, but never recorded, never pruned, and reported as external by `--list`.
    - Fix: write the receipt entry before the rename and links, or drop the branch and say how such leftovers are handled.

15. **MINOR. A and C depend on a Phase 1 section that is still a stub.** A:59, A:525, C:52.
    - Evidence: `phase-1-removal-spec.md:302-303` is `## 3. Existing-workspace cleanup design` followed by `<!-- TODO -->`. C:52 states the retire step's matching rules ("IronClaude's or the Coder bundle's exact argv") as fact.
    - Fix: mark them UNVERIFIED in A and C until Phase 1 §3 is written, and re-check them then.

16. **MINOR. B has two self-containment gaps.** B:22, B:23-25.
    - Evidence:
      - The `gh api repos/...contents/...?ref=<branch>` URL is unquoted, so zsh fails with "no matches found".
      - The inline fallback facts omit the `.superclaude-init-ok` marker (only C:48 has it). If C is unreachable, Coder's index automation triggers the one-off rebuild described in finding 1.
    - Fix: quote the URL, and add the marker sentence to B's inline facts.

17. **MINOR. The headless-session cost is not disclosed.** A:198, A:212-214.
    - Evidence: the `startup` matcher fires on every new `claude` process, including headless `claude -p` sessions that IronClaude pipelines start in fresh git repos or worktrees (sprint, swarm, cliEval isolated HOMEs). Each one starts a background init of up to about 1 GB. Parallel sessions in one new worktree compound finding 1.
    - Fix: document `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` for pipelines and CI, or skip when the session is non-interactive. Add a test.

18. **MINOR. Two acceptance checks are weak.** A:421 (T9), A:341 (T2).
    - Evidence: T9's "every 'expect' line in §4.2 holds" is not a mechanical command. T2's `rg -n '"codegraph"'` passes even if the dispatch branch is missing, because the registry entry alone matches, and a named constant would not match at all.
    - Fix: make each §4.2 expect line an assertion (`test`, `jq -e`, `grep -q`) so the script itself fails. For T2, assert the dispatch with the registry test rather than `rg`.

## Checks that passed (no finding)

- **Brief coverage:** A §1-§8 plus `## Decisions` cover A1-A9; §9 is the Shared files section. B contains:
  - the goal;
  - touchpoints marked as leads to verify on current `main`;
  - the research instruction for new worktrees and projects (B:39-41);
  - the ordering (B:43-51) and the pin (B:31, B:48);
  - tests, commits, and PRs on IronbellyOrg/Coder only (B:59-61);
  - #323 comments (B:62) and the autonomy rules (B:65-73).
  
  B is 77 lines, within the 150-line limit. C covers the brief's C items.
- **Consistency:**
  - Pin and hashes are identical in A:17-20, B:23 and C:13-14, and match `/tmp/codegraph-eval.fQfO/dl/SHA256SUMS`.
  - The registration JSON is identical in A:89, B:16 and C:41.
  - The hook marker, matcher and timeout agree between A §3.2, C §2.3 and `P2-indexing-sync-merged.md`.
  - The D3 change from `index --force` to `index` is justified by `probe-results.md:7`.
  - The installer contract matches `P2-installer-contract-merged.md`: required phase, narrow doctor check, receipt, owned-entry rule, old-dir pruning.
  - Helper keep/delete and the retire-step position agree with `phase-1-removal-spec.md:512-514`.
  - The CI Claude CLI step (deleted by Phase 1, re-added by T8) agrees with `phase-1-removal-spec.md:524`.
  - The B and C ordering matches A §8.
- **Tarball claim:** v1.6.2 linux-x64 has 1380 members (60 directories, 1320 files, no links) under the single top dir `codegraph-linux-x64`, as A:77 states.

## Self-audit (what I checked)

- Read in full: the brief (P2-phase2-spec.md), README rules, A, B, C, both merged decision files, probe-results.md, and Phase 1 spec §2-§3 and §6.2-§10.
- Read in part: `install-update-flow.md` §1.7, §4.1-4.2; `codegraph-evaluation.md` registration lines 59-77, 100, 293-304.
- Source citations checked by reading the file (more than 40, all correct except finding 12):
  - `update.sh:1-10`;
  - `main.py:155-190` (the `:161-186` list block), `:245-280` (phase `:254-262`, no `force` at `:255`, exit `:264-275`), `:346`, `:431`;
  - `install_mcp.py:55-61`, `:101-108`, `:112-141`, `:486-503`, `:714-754`, `:757-812`, `:766-772`, `:789-812`, `:815-913`, `:830-843`, `:867-873`, `:916-948`, `:1025-1028`;
  - `doctor.py:26-44`, `:52`; `install_hooks.py:42-79`; `hooks/hooks.json:47`; `plugins/.../hooks.json:37`;
  - `core/CLAUDE.md:18-24`, `:21`, `:90`, `:112`; `tests/cli/test_update_script.py:13-18`; `tests/core/test_claude_md_routing_block.py:79-81`;
  - `tests/cli/test_update_command.py:28-76`, `:345-372`; `tests/cli/test_install_mcp_tavily.py:382-416`, `:426-455`;
  - `tests/unit/test_cli_install.py:138-153`, `:377`, `:412-425`, `:898-903` (presence-only check, so new scripts do not break it); `tests/cli/test_install_hooks.py:684-687`;
  - `.github/workflows/test.yml:130-171`; `docs/user-guide/mcp-installation.md:5-26`, `:52`; `docs/reference/mcp-server-guide.md:9`, `:31-55`;
  - `README.md:64`, `:75`; `pyproject.toml:16`; `Makefile:42`; `install_user_setup.py` (no `permissions`, confirmed); `plugins/superclaude/core` (no CLAUDE.md, confirmed).
- Test file existence: `test_verify_sync_hooks.py`, `test_cli_registration.py`, `tests/unit/test_cli_doctor.py`, `tests/docs`, `tests/recommend` and `tests/core` exist. `test_install_mcp_cli.py` does not exist yet; Phase 1 creates it, as A says.
- Commands run, all read-only:
  - `command -v claude uv jq gh git`;
  - `gh pr view --repo ... --json url` (reproduced the error in finding 5);
  - `tar -tvzf` on the W4 tarball;
  - a hash cross-check against W4's SHA256SUMS;
  - `rg -i codegraph` outside `.dev/` (no hit, as A §0 says);
  - `git status --short`, which shows only untracked `.dev/codegraph-migration/` (no tracked file modified by this review).
- Not checked: the Coder `path:line` citations (external repo at `e25f787c`) and live `claude mcp add-json` behaviour (forbidden by the run rules; that gap is finding 3).
