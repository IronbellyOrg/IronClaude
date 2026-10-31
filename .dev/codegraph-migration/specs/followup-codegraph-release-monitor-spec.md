# Follow-up spec: codegraph upstream release monitor (issue #323)

Status: complete (task M, 2026-10-30); revised 2026-10-31 to fix every defect in the `/sc:reflect --mode pre` report (`.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/artifacts/reflect/pre-20261030154210/REPORT.md`; see "Review resolution" at the end); revised again 2026-10-31 for the three findings of the PR #335 review (job trust split, `--tag` downgrade, R16 exit code), and a third time for the PR #335 round-2 findings (fetch-failed legs routed, `needs` edges, ref guard); see the last rows of "Review resolution". Planning artifact only; no source, test or workflow file was changed.

## 0. Goal, inputs and evidence rule

**Goal.** A scheduled GitHub workflow in `IronbellyOrg/IronClaude` keeps IronClaude's pinned codegraph version current. When `colbymchenry/codegraph` publishes an eligible newer release, the workflow verifies it (SHA-256 against the release's `SHA256SUMS`, plus `gh attestation verify -R colbymchenry/codegraph`), rewrites the pin in its single source location, proves the candidate in an isolated HOME, and opens a pull request on `IronbellyOrg/IronClaude` only (never upstream) with the release notes. Coder picks the new values up through its existing IronClaude SHA bump (coordinator decision; not reopened here).

**Scope.** Follow-up to Phase 2 of issue #323 (https://github.com/IronbellyOrg/IronClaude/issues/323). Not part of Phase 2: PR #329 (https://github.com/IronbellyOrg/IronClaude/pull/329) lands first. **Precondition for execution: PR #329 is merged to `master`; the executor branches from `origin/master` after that.** It is met: `gh pr view 329 --repo IronbellyOrg/IronClaude` reports MERGED at 2026-10-30T15:23:26Z, merge commit `2f10a0e1`. This spec was read against #329's head `e62ed152`; the reflect pass found every cited line unchanged on `origin/master`.

**Execution setup (before `/sc:implement`, not a plan task).** The planning files are committed on the local branch `ironbelly/codegraph-release-monitor` with subject `docs(plan): codegraph release monitor (#323)`. The executor creates the feature branch in its own worktree and runs `/sc:implement` there, so no plan task ever switches branches under the package's `progress.md`:

```bash
cd /home/coder/workspaces/worktrees/IronClaude/codegraph-release-monitor   # the planning worktree
git fetch origin
PLAN=$(git log --format=%H -1 --grep '^docs(plan): codegraph release monitor' ironbelly/codegraph-release-monitor)
test -n "$PLAN"
git worktree add .dev/worktrees/codegraph-release-monitor-impl -b ironbelly/feat-codegraph-release-monitor origin/master
cd .dev/worktrees/codegraph-release-monitor-impl
git cherry-pick "$PLAN"
# then, in Claude Code started in this directory:
# /sc:implement .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/TASK-WF-followupCodegrap-20261030-153943.md
```

`.dev/worktrees/` is gitignored (`.gitignore:238`) and is the repo's canonical worktree location (repo `CLAUDE.md`). If the cherry-pick conflicts because someone changed the same `.dev/` files on `master`, stop and report on issue #323.

**Inputs read for this spec (2026-10-30):**
- `.dev/codegraph-migration/orchestration/README.md:24-33` (run rules).
- `.dev/codegraph-migration/research/codegraph-evaluation.md` §1 (`:11-25`: platforms, `SHA256SUMS` per release, attestations SLSA v1.0 Build L2 on bundles and `SHA256SUMS`, `gh attestation verify` needs GitHub auth), §5.1 (`:113-127`), §5.6 (`:203-217`), §5.9 (`:238-240`: `codegraph install --print-config claude` prints the entry with no writes), §6 (`:248-287`, gaps the user accepted), §7 (`:289-314`, single IronClaude pin; "a test-time drift check comparing IronClaude's MCP entry with a recorded `codegraph install --print-config claude` fixture", `:310`).
- `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` §2.3-§2.4 (`:73-111`), §5 acceptance-block rules (`:445`), §6 (`:742-760`), §7 (`:762-783`), §8 (`:785-805`).
- `src/superclaude/cli/install_codegraph.py:26-35` (`VERSION = "1.6.2"`, `TAG = f"v{VERSION}"`, the 4-entry `SHA256` dict at `:28-33`, `MCP_TOOLS = "node,search,callers,callees,impact,files,status"` at `:35`), `:271-365` (`acquire`), `:186-190` (`_download`, the one network call).
- `src/superclaude/cli/install_mcp.py:854-874` (`_CODEGRAPH_ENV_KEYS`, `_codegraph_entry(command)`: `type`, `command`, `args ["serve","--mcp"]`, `alwaysLoad: true`, `env` with telemetry off, update check off and `CODEGRAPH_MCP_TOOLS`).
- `tests/cli/test_install_codegraph.py:1-141` (conventions: `box` autouse fixture sets HOME and PATH to tmp dirs, `_download` is the one network fake, `stub()`/`tarball()` builders; `test_u2_pin_integrity` at `:126-141` reads `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt`).
- `.github/workflows/test.yml` (jobs `test`, `swarm-marker-matrix`, `lint`, `doctor-check`, `test-summary`; `setup-uv@v10.3.2`, Python 3.10, `ruff check src/ tests/`, `ruff format --check src/ tests/`; `on: workflow_dispatch` present). `tests/swarm/test_merge_boundary_guards.py:38,46,175` is the precedent for a static workflow test (`yaml.safe_load` of a workflow file; `pyyaml` is in `scripts/dependency_baseline.txt:56`). `tests/skills/test_workflow_archive.py:26-28` is the precedent for loading a script by path with `importlib.util.spec_from_file_location`.
- Coder's monitor, `gh api repos/IronbellyOrg/Coder/contents/.github/workflows/ironclaude-upstream-monitor.yml -H 'Accept: application/vnd.github.raw'` (daily cron plus `workflow_dispatch`; neutral exit with a step summary when the upstream API fails; idempotency by branch `auto/ironclaude-bump-<sha7>` and "open PR exists or remote branch exists" skip; push branch, then proof, then PR; ready PR on PASS, DRAFT PR plus best-effort `needs-build-proof` label on FAIL; `always()` on the PR step so a pushed branch is never orphaned).

**Facts verified for this spec (2026-10-30):**
1. Upstream releases (`gh api 'repos/colbymchenry/codegraph/releases?per_page=8'`): v1.6.2 2026-10-03, v1.6.1 09-29, v1.6.0 08-26, v1.5.0 07-21, v1.4.1 07-10, v1.4.0 07-10, v1.3.1 07-09, v1.3.0 07-07; none prerelease or draft; 7 assets each (6 archives plus `SHA256SUMS`). `releases/latest` is v1.6.2, equal to the pin today. Release note bodies are long: v1.6.2 is 76,281 characters, over GitHub's 65,536-character PR body limit.
2. `--print-config <id>` exists: `src/bin/codegraph.ts:2803` on upstream `main` (`.option('--print-config <id>', 'Print MCP config snippet for the named agent and exit (no file writes)')`), handled at `:2814-2824`. For `claude` it prints `# Add to <path>\n\n<JSON {"mcpServers":{"codegraph":{...}}}>\n` (`src/installer/targets/claude.ts:241-245`). The parser must skip the `#` line.
3. **The pin is not single-source today.** `git grep -n -E '1\.6\.2|v1\.6\.2' -- ':!.dev' ':!.claude'` finds the version as literals in `tests/cli/test_install_codegraph.py:38,45,96,151,171,175,237,270,639,640,659,691`, `tests/unit/test_cli_doctor.py:241,287`, `tests/cli/test_update_command.py:355`, `docs/user-guide/mcp-installation.md:9,28,31`, `docs/reference/mcp-server-guide.md:29,43`, `CHANGELOG.md:35`, and `install_codegraph.py:39` (a comment). The pin-bump test also hard-codes the *next* version: `tests/cli/test_install_codegraph.py:306` (`def _bump(monkeypatch, version="1.6.3")`) and `:320` (`vdir(box.home, "v1.6.3")`); after a real bump to v1.6.3, `test_u21_pin_bump_keeps_previous_then_prunes` would compare a version directory with itself and fail. `test_u2_pin_integrity` also compares the table with a `.dev/` evidence file. A bump that rewrites only `install_codegraph.py` would fail CI. T1 fixes this first: it rewrites 22 sites (the 15 test literals of `1.6.2`, the 2 test literals of `1.6.3`, and the 5 docs literals); `CHANGELOG.md:35` (history) and the `install_codegraph.py:39` comment (a past measurement) stay.
4. Repo settings (`gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow`): `default_workflow_permissions: read`, `can_approve_pull_request_reviews: true` (Actions may create PRs). The repo is public, default branch `master`. Existing labels: bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix.
5. GitHub rule (https://docs.github.com/en/actions/concepts/security/github_token): events caused by `GITHUB_TOKEN` do not start new workflow runs, except `workflow_dispatch` and `repository_dispatch`; PRs opened or updated with the token start runs in an approval-required state. So the bump PR's `Tests` workflow would wait for approval; the monitor dispatches `test.yml` on the bump branch instead (`test.yml` has `workflow_dispatch`).
6. Coder side (`.dev/codegraph-migration/handoff/coder-handoff-prompt.md:16`): Coder is told to read `MCP_TOOLS`, `VERSION` and `SHA256` from `install_codegraph.py` at the pinned IronClaude SHA in tests and registrations. Coder's image bake does not: it hard-codes the pin. `templates/VSCode-AIDev02/Dockerfile.coder:359` sets `CG_VERSION=1.6.2`, `:361-362` set the linux-x64 and linux-arm64 SHA-256, and `templates/VSCode-AIDev02/scripts/startup.sh:971` sets `aidev_cg_version=1.6.2`, at Coder `origin/main` `25aba75d`; Coder's IronClaude pin is the single ARG at `templates/VSCode-AIDev02/Dockerfile.coder:402`, and Coder's `ironclaude-upstream-monitor.yml` rewrites only that ARG line (`:131-132`). After an IronClaude codegraph bump, the next Coder IronClaude-SHA bump PR therefore fails Coder contract CI: `.github/contract-tests/test-71-codegraph-bake.sh` (`:101-118` compares the module with the Dockerfile pins, with any network) and `.github/contract-tests/test-57-catalogue-configure.sh` (`:300-301`, run with `--network=none`). That blocks the Coder PR safely but needs a Coder-side edit (`.dev/codegraph-migration/review/M-open-questions-analysis.md`, question 2). Recorded as human item 6 (§7), not as a change to this plan.
7. Release age uses `published_at`. GitHub's REST docs (https://docs.github.com/en/rest/releases/releases) define `created_at` as "the date of the commit used for the release, and not the date when the release was drafted or published"; `published_at` is nullable (drafts). `gh` 2.103.3 (local) has `gh label create --force`, `gh run list --workflow ... --json conclusion`, `gh pr ready` and `gh attestation verify -R`.
8. The user's "about two weeks" rule for new dependency versions is coordinator-stated. Negative evidence: `grep -rn -i 'two weeks\|14 days\|release age\|minimum age' ~/.claude/*.md` found nothing; the closest rule on disk is the harness rule that external script versions must be at least two weeks old.

**Evidence rule for the executor.** Every acceptance block runs from the worktree root under `bash -euo pipefail` and must exit 0 only if its criterion passes; one condition per line; a negative check is written `if cmd; then exit 1; fi` (same rule as Phase 2 spec `:445`). Every `uv run pytest` uses `-p no:cacheprovider`. Run `git status --short` after each task: a modified tracked file the task did not intend to change is a defect to fix before committing. Never run `tests/cli/eval/` (it rewrites `.dev/releases/current/cliEval/evidence/T02.15/perf.json`, README `:27`); after any full-suite run, restore that file with `git checkout --`. `$PKG` is this plan's task package, found by its stable id prefix wherever `/sc:implement` keeps it. **Every block that uses `$PKG` starts with** `PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"` (blocks run separately, so a definition never carries over). Task evidence goes under `"$PKG/artifacts/"`, which `git add .dev/tasks` stages; never the project-root `artifacts/` folder, which is never staged.

## 1. Preflight: files that change

Line numbers are from `e62ed152` (PR #329's head). After #329 merges they should be unchanged, but the executor locates each seam by the named function, constant or literal, not by line.

| # | File | Change | Task |
|---|---|---|---|
| F1 | `tests/cli/fixtures/codegraph-SHA256SUMS.txt` (new) | Copy of `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` (header comment line plus the four `codegraph-<asset>.tar.gz` lines). The test fixture the bump rewrites; the `.dev/` evidence file stays untouched as history (README `:12`, historical `.dev/` artifacts stay untouched). | T1 |
| F2 | `tests/cli/test_install_codegraph.py` | `test_u2_pin_integrity` reads F1 instead of the `.dev/` file. Every literal `1.6.2` / `v1.6.2` in fixtures and assertions (`:38,45,96,151,171,175,237,270,639,640,659,691`) becomes `cg.VERSION` / `cg.TAG` (default arguments become `None` resolved to `cg.VERSION` inside, or f-strings). The pin-bump helper's next version (`:306` `version="1.6.3"`, `:320` `"v1.6.3"`) is derived as the next patch of `cg.VERSION` (a small `_next_patch(cg.VERSION)` helper in the test file). New test `test_no_pinned_version_literals_in_tests` in this file scans the three test files of F2-F4 for any `\d+\.\d+\.\d+` literal equal to or above the current pin and fails on a match (it builds its own pattern from `cg.VERSION`, so it holds no literal itself). Locate each site by its literal, not its line number. | T1 |
| F3 | `tests/unit/test_cli_doctor.py` | `_stub(version="1.6.2")` (`:241`) and `"the pin is 1.6.2"` (`:287`) derive from `install_codegraph.VERSION`; the file gains `from superclaude.cli import install_codegraph` (its imports at `:3-15` do not include it today). | T1 |
| F4 | `tests/cli/test_update_command.py` | `"codegraph MCP (pinned v1.6.2; user scope):"` (`:355`) derives from `install_codegraph.TAG`. | T1 |
| F5 | `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md` | Replace the literal version (`:9,28,31` and `:29,43`) with "the pinned version" plus how to read it (`superclaude install --list` prints `codegraph MCP (pinned vX.Y.Z; user scope)`; `install_codegraph.py:26-27` is the source). Add one short "How the pin is updated" paragraph to `mcp-installation.md` naming the monitor (T5). | T1, T5 |
| F6 | `scripts/codegraph_release.py` (new, stdlib only: it imports nothing outside `sys.stdlib_module_names`; values it needs from the installed `superclaude` package are read through a child `sys.executable -c` process, §2.2) | The bump logic (§2.2) as pure functions plus a small CLI with subcommands `check`, `fetch`, `bump`, `record`, `prove`, `body`, `route`, `apply`, `report`. Not packaged (maintainer tooling, like `scripts/verify_deps.py`). | T2, T3 |
| F7 | `tests/cli/test_codegraph_release.py` (new) and `tests/cli/fixtures/codegraph_release/` (new: `releases.json`, `SHA256SUMS`, `print-config-claude.txt`, `fake_mcp_server.py`) | Offline unit tests for F6 (§3). The script is loaded with `importlib.util.spec_from_file_location` (precedent `tests/skills/test_workflow_archive.py:26-28`). | T2, T3 |
| F8 | `.github/workflows/codegraph-release-monitor.yml` (new) | The scheduled workflow (§2.3). Thin: every decision lives in F6. | T4 |
| F9 | `tests/cli/test_codegraph_release_workflow.py` (new) | Static checks of F8 with `yaml.safe_load` (precedent `tests/swarm/test_merge_boundary_guards.py:38,175`). | T4 |
| F10 | `.github/workflows/README.md` | New section "codegraph-release-monitor.yml" (the file lists every workflow; today 3). | T5 |
| F11 | `CHANGELOG.md` | `## [Unreleased]` Added entry for the monitor. The historical v1.6.2 line (`:35`) is not edited. | T5 |

**Not changed, with the reason:** `src/superclaude/cli/install_codegraph.py` (only the bot's bump PRs rewrite `VERSION` and `SHA256`; the `_MAX_MEMBERS` comment at `:39` names v1.6.2 as a past measurement and stays true); `src/superclaude/cli/install_mcp.py` (the drift check reads `_codegraph_entry`; it does not change it); `.github/workflows/test.yml` (dispatched, not edited); `pyproject.toml`, `Makefile`, `scripts/dependency_baseline.txt` (no new dependency: stdlib plus the `gh` CLI that GitHub-hosted runners provide); any primitive under `src/superclaude/{commands,skills,agents,core,hooks,templates}` (none changes; `make sync-dev` runs in T0 and T6 only to refresh the gitignored `.claude/` mirrors the test suite and `make verify-sync` read, and no `.claude/` path is ever staged); `.dev/codegraph-migration/evidence/*` (history).

## 2. Design

### 2.1 Shape

One stdlib script holds every decision and every GitHub side effect except `git push` and is unit-tested offline; the workflow only sequences its subcommands, runs `git commit`/`git push`, and writes summaries (Coder's monitor keeps its logic inline in YAML; this design deliberately does not, so the logic is testable). Flow of one scheduled run:

```text
check  -> no eligible candidate on either line: summary "pinned vA is current (vB waiting, eligible <UTC time>)", exit 0
       -> upstream unreachable: infrastructure outcome (§2.5)
       -> candidate per line (within-major, higher-major; §2.4), plus the idempotency gate per candidate
          (branch_exists, declined, reprove; §2.4): declined -> stop that line; branch_exists -> re-prove leg (no push)
fetch  -> download SHA256SUMS + 4 tarballs, length + hash check, gh attestation verify on all 5 files
          -> integrity failure: issue only, stop (§2.5)
bump   -> rewrite install_codegraph.py VERSION + SHA256, rewrite tests/cli/fixtures/codegraph-SHA256SUMS.txt
push   -> commit + push the NEW branch codegraph/bump-<tag> (only after fetch passed, only when it does not exist yet,
          never in a dry run); pushing before tests and prove lets an aborted or failed proof still get its draft PR
tests  -> pytest on the codegraph test files (§2.3 lists them); a failure is a behaviour failure, stage=tests
prove  -> isolated HOME: acquire (real verified download), --version, index fixture, tools/list, print-config drift
body   -> PR body: old/new pin, hashes, attestation result, proof result, release notes (budgeted; link only for a major)
route  -> decide the actions from the outcome and the existing artifacts (§2.5); apply -> execute them through gh:
          ready PR (within-major, all passed) | draft (major, always) | draft "[proof failed: <stage>]" (behaviour failure);
          then dispatch test.yml on the branch.
jobs   -> check: check | bump (per leg): fetch, bump, push, record | prove (per leg, untrusted, read-only token):
          tests, prove | report (one job, all legs, if: always()): body, route, apply (§2.3 "Jobs")
```

### 2.2 `scripts/codegraph_release.py`

Constants: `REPO = "colbymchenry/codegraph"`, `ASSETS = ("linux-x64", "linux-arm64", "darwin-x64", "darwin-arm64")` (asserted equal to `set(install_codegraph.SHA256)` in a test, so the two never drift), `PIN_FILE = src/superclaude/cli/install_codegraph.py`, `SUMS_FIXTURE = tests/cli/fixtures/codegraph-SHA256SUMS.txt`, `MIN_AGE_DAYS = 14` (§2.4, decision M-b), `NOTES_BUDGET = 60_000` characters.

Pure functions (no I/O; every branch unit-tested):

| Function | Contract |
|---|---|
| `parse_version(tag) -> tuple[int, int, int] \| None` | Accepts only `vMAJOR.MINOR.PATCH` (digits). Anything else (prerelease suffixes, other tags) returns None and is ignored. |
| `read_pin(text) -> tuple[str, dict]` | From the `install_codegraph.py` text: exactly one line `^VERSION = "(\d+\.\d+\.\d+)"$` and exactly one `SHA256 = {` block of four `"<asset>": "<64 hex>",` lines. Any other count raises `ValueError` naming the line. |
| `pick_candidates(releases, pin_version, now, *, min_age_days) -> dict` | Input: the GitHub releases JSON list. Rules of §2.4. Returns one entry per line (`within`, `major`), each `{"tag": <tag or None>, "reason": <text>, "waiting": <tag or None>, "eligible_at": <UTC ISO or None>, "stalled": <bool>}`, plus `skipped` (tag, reason) for every ignored release. |
| `parse_sha256sums(text) -> dict` | The four `codegraph-<asset>.tar.gz` lines (`<64 lowercase hex>  <name>`); other lines (Windows zips) ignored; a missing, duplicated or malformed line for one of the four raises. |
| `rewrite_pin(text, version, hashes) -> str` | Replaces exactly the `VERSION` line and the four dict lines, keeping indentation and quoting byte-for-byte, so `ruff format --check` stays clean. Post-condition checked in the function: `read_pin(result) == (version, hashes)` and the diff touches only those five lines. |
| `render_sums_fixture(tag, sums_text, fetched_at) -> str` | Header comment (same format as F1's first line, naming the tag, the UTC time and the source) plus the four asset lines sorted by name, as `test_u2_pin_integrity` parses them (`splitlines()[1:]`). |
| `tool_problems(names, mcp_tools) -> list[str]` | Compares the `tools/list` names with `{"codegraph_" + t for t in mcp_tools.split(",")}`: one message per missing tool and per extra tool. Empty list = pass. |
| `entry_drift(expected, print_config_text) -> list[str]` | Drops lines starting with `#`, parses the JSON, takes `mcpServers.codegraph`, and compares it with `expected` (IronClaude's `_codegraph_entry(...)`) on every key except `command` (IronClaude registers an absolute realpath, upstream the bare name) and `env` (IronClaude-only keys). One message per differing or new key. Empty list = no drift. |
| `build_body(...) -> str` | PR body (§2.6). Never exceeds 65,000 characters: release notes are added newest-first until `NOTES_BUDGET` is used, the rest replaced by links; for a major, links only. |
| `classify(events) -> "infrastructure" \| "integrity" \| "behaviour" \| None` | Fail-closed classifier over the recorded stage results (§2.5 classification table). Anything that fits no row is `integrity`. |
| `gate(tag, existing) -> dict` | Idempotency gate (§2.4), from the existing artifacts read through `_gh` (open and closed PRs on `codegraph/bump-<tag>`, `git ls-remote --heads origin codegraph/bump-<tag>`): `{"declined": <closed-unmerged PR for this tag>, "branch_exists": <remote branch exists>, "reprove": <branch exists and an open PR is on it>}`. `declined` stops that line; `branch_exists` turns the leg into a re-prove of that branch head with no push. |
| `route(outcome, line, tag, existing) -> list[action]` | Pure router: from the outcome (`pass`, `integrity`, `behaviour`, `infrastructure`), the line (`within`, `major`), the tag and the existing artifacts found by their keys (open or closed PR on `codegraph/bump-<tag>`, open issue with a marker, stored fingerprint, last 3 run conclusions, and for a re-proved branch whether its `SHA256` table equals the hashes verified in the same run) returns the actions to take (`open_pr(ready\|draft, title)`, `comment(pr\|issue, text)`, `mark_ready`, `retitle`, `open_issue(title, marker, body_file)`, `close_superseded(pr)`, `close_issue(marker)`, `noop`). The workflow executes the actions; it decides nothing itself. |
| `fingerprint(outcome, stage, first_error_line, head_sha) -> str` | Stored in an HTML comment `<!-- codegraph-monitor-fp:<value> -->` in the artifact body or its last bot comment; a run comments only when it changed. `head_sha` is the bump branch head for a PR, and the `master` HEAD SHA for artifacts without a branch (integrity and infrastructure issues). |

I/O wrappers (thin; tests replace them through `monkeypatch`):
- `_gh(args, timeout) -> (code, stdout)`: the one subprocess entry for `gh` (argv list, no shell, bounded, the same shape as `install_codegraph.Runner`). Used for `gh api rate_limit` (the preflight), `gh api --paginate --slurp 'repos/colbymchenry/codegraph/releases?per_page=100'` (`--paginate` alone prints one JSON array per page; `--slurp` wraps the pages in one outer array, which `check` flattens), `gh release download <tag> -R colbymchenry/codegraph -p SHA256SUMS -p 'codegraph-<asset>.tar.gz' ... -D <dir>`, and `gh attestation verify <file> -R colbymchenry/codegraph` (once per file, 5 files).
- `_run(argv, *, env, cwd, timeout)`: bounded subprocess for `codegraph` and `python` in `prove`, started in its own process group and killed by group on timeout or exit. Python children always run as `sys.executable` (the interpreter that has the editable `superclaude` install), never a bare `python` from `PATH`.
- `package_values(env) -> dict`: one child `sys.executable -c` that imports `superclaude.cli.install_codegraph` and `superclaude.cli.install_mcp` and prints JSON `{"version", "tag", "sha256", "mcp_tools", "expected_entry"}` (`expected_entry` = `install_mcp._codegraph_entry(<launcher>)` for the launcher passed in). This keeps the script itself stdlib-only: `superclaude.cli` imports `main` and `click` on import (`src/superclaude/cli/__init__.py:13`, `install_mcp.py:21`).
- `mcp_tool_names(binary, cwd, env, timeout=60) -> list[str]`: newline-delimited JSON-RPC over stdio: `initialize`, `notifications/initialized`, `tools/list`; kills the process on exit or timeout. Same protocol as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs:1-30`, ported to Python so the workflow needs no Node and does not depend on a `.dev/` evidence file.

CLI (each subcommand prints a human summary to stdout, appends `key=value` lines to the file named by `--github-output` when given, and exits 0 on success or "nothing to do", 1 on a failed check, 2 on an infrastructure error):
- `check [--min-age-days N] [--tag vX.Y.Z] [--dry-run]` -> `result=none|candidate|infrastructure`, `previous`, `within_tag`, `major_tag` (each empty when that line has nothing), `stalled=true|false`, and per line the gate fields `<line>_declined`, `<line>_branch_exists`, `<line>_reprove`. `--min-age-days` rejects anything but a whole number >= 0 with exit 1 (a bad manual input is a failed check, not an outage) before any download. `--tag` skips selection (manual run) but never the strictly-newer rule of §2.4. It compares the tag with the pin by `parse_version`: a tag newer than the pin goes on the line its major selects (the pin's major: within-major line; a higher major: higher-major line); a tag equal to the pin is accepted only together with `--dry-run` (a re-proof of the current pin on the within-major line; such a run never bumps, pushes or opens anything); a tag older than the pin, which includes every tag with a lower major, is refused with exit 1, with or without `--dry-run`. It also refuses, with exit 1, a tag that `parse_version` rejects or that is not a published, non-draft, non-prerelease release. Every refusal happens before any download and emits no candidate.
- `--github-output <file>` is accepted by every subcommand; `fetch`, `prove` and `check` write their `result=` and `stage=` lines there, never only to stdout.
- `fetch --tag vX.Y.Z --dir D` -> `result=ok|integrity|infrastructure`, `stage=preflight|download|sums|hash|attestation`, plus `asset`, `expected`, `actual` on a hash failure, plus `error` (the first error line, newlines removed, at most 500 characters) on any result other than `ok`; on `stage=attestation` it also saves the first 4 KiB of the last failing `gh attestation verify` output to `D/fetch-error.txt`. Order: download, check each file's byte length equals the release API asset `size`, parse sums, hash each tarball against its sums line, attestation for the four tarballs and `SHA256SUMS` (W4 §1 `:21`: both carry attestations). Retries and classification follow §2.5.
- `route --outcome ... --stage ... --line ... --tag ... --out actions.jsonl` -> writes the §2.2 `route` actions as JSON lines (it reads existing PRs, issues and run conclusions through `_gh` first).
- `apply --actions actions.jsonl [--dry-run]` -> executes each action through `_gh` (`gh pr create`, `gh pr edit`, `gh pr ready`, `gh pr close`, `gh issue create`, `gh issue comment`, `gh issue close`, `gh label create --force`, `gh api .../labels`, `gh workflow run test.yml`), always with `--repo "$GITHUB_REPOSITORY"` and refusing any other repository; label failures are logged and never fail the run; `--dry-run` prints the commands and runs none. This keeps every GitHub side effect except `git push` in tested Python (no bash or jq action executor in YAML).
- `bump --tag vX.Y.Z --dir D` -> rewrites the pin file and F1 from the verified `D/SHA256SUMS`; refuses to run unless `fetch` left `D/.verified` (written last by `fetch`, containing the tag).
- `prove [--keep]` -> `result=pass|fail`, `stage=install|version|index|tools|drift`, `asset=<the asset acquire installed>`, plus `root=<sandbox root>` and `home=<sandbox HOME>` when `--keep` leaves the sandbox in place. The full behaviour-failure stage set used by `route` is `tests|install|version|index|tools|drift|aborted` (`tests` from the workflow's pytest step, `aborted` when the prove step never wrote a result). Runs against the working tree (after `bump`, or on the current pin for a dry run); see §2.5.
- `body --tag vX.Y.Z --previous vA.B.C --proof <log> --out <file>` -> writes the PR body.
- `record --leg <json> --fetch-output <file> --pushed true|false --dir D --out <file>` -> writes the leg record (JSON: tag, line, fetch_result, stage, pushed, head_sha, branch_exists, reprove, dry_run, the four SHA-256 values verified from `D/SHA256SUMS` when `fetch` passed, and `head_table_matches` = the branch head's `SHA256` table equals those values; false when no hashes were verified). When `fetch` did not pass, the record also carries `asset`, `expected`, `actual` and `error` from the fetch output (each empty when absent) and `attestation_output` = the content of `D/fetch-error.txt` (empty when absent, at most 4 KiB): the §2.5 issue-body fields. A leg with no pushed or existing branch (a fresh leg whose fetch or push failed, and a fresh leg of a dry run) records `head_sha` = `github.sha`, which the §2.3 ref guard makes the `master` head, the `fingerprint` value for artifacts without a branch. On a re-prove leg it reads the head SHA and the head's table as data (`git ls-remote`, `git fetch` of the branch, `git show <sha>:src/superclaude/cli/install_codegraph.py` parsed by `read_pin`; nothing from the branch is executed). Runs in the `bump` job with `if: always()` (§2.3).
- `report --legs <json> --records-dir R --proofs-dir P [--dry-run]` -> handles every leg of `--legs` in order, in-process; each leg ends in exactly one of (a), (b) or (c), and none is skipped silently. Per leg it first validates the record as untrusted data (at most 1 MiB; `fetch_result` in {ok, integrity, infrastructure}; tag and line equal to the `--legs` entry); a missing or malformed record is an error for that leg. (a) `fetch_result` `integrity` or `infrastructure` (fresh, re-prove or dry-run leg): the outcome is that class with the record's `stage`; no proof is read, no `git ls-remote` runs and no `body` runs; `route` and `apply` (`--dry-run` in a dry run) file the integrity issue (§2.5: issue only) or run the infrastructure warning, counter and issue. `report` writes the §2.5 issue body from the record to a file that the `open_issue` action names (§2.2 `route`). The record's failure fields are untrusted: `asset` must be empty or one of the four tarball names or `SHA256SUMS`, `expected` and `actual` must be empty or match `^[0-9a-f]{64}$`, `error` is at most 500 characters and `attestation_output` at most 4 KiB; a field that fails is replaced by `detail failed validation; see the run log` and the issue is still filed; like release notes (§2.6), these fields reach `gh` only through `--body-file`, `attestation_output` in a fenced block. (b) `fetch_result` `ok` and the leg pushed, has an existing branch (`branch_exists`: a re-prove leg, §2.4), or is part of a dry run: validates the proof as untrusted data (at most 1 MiB; `result` in {pass, fail}; `stage` in the `prove` stage set; tag and head_sha equal to the record; a missing, duplicate or malformed proof is `stage=aborted`); for a leg that pushed or has an existing branch, checks that `git ls-remote` still shows the record's head_sha (a mismatch is `stage=aborted`); a fresh dry-run leg pushed nothing, so it gets no `ls-remote` check (its head_sha is `github.sha`, §2.2 `record`); the outcome is the proof's result; then runs `body`, `route` (given `head_table_matches`) and `apply` (`--dry-run` in a dry run). (c) `fetch_result` `ok`, not pushed, no existing branch and not a dry run (the push step failed): an error for that leg (§2.5 push failure), logged as `::warning::` naming the tag; no `route`, no `apply`. An error on one leg is logged and the next leg still runs; the exit code is 2 when any leg had an infrastructure outcome or an error, else 0 (§2.5: integrity and behaviour outcomes end green once filed). An empty or unset `--legs` means no legs: exit 0 with no `gh` call.

### 2.3 Workflow `.github/workflows/codegraph-release-monitor.yml`

- `name: codegraph release monitor`; `on: schedule: - cron: "23 6 * * *"` (daily, off the hour) and `workflow_dispatch` with inputs `dry_run` (boolean, default false: run check, fetch, bump, tests and prove, then print the diff, the body and the `apply --dry-run` commands; no push, no PR, no issue, no label, no dispatch), `tag` (string, optional: passed to `check --tag`; must be newer than the pin, or equal to it with `dry_run`; an older tag fails the run with exit 1, §2.2) and `min_age_days` (string, optional, default empty = 14; passed to `check --min-age-days`, decision M-b).
- **Jobs (trust split).** One workflow file, four jobs. Each job runs on a fresh GitHub-hosted VM, so code the untrusted job runs cannot change what a token-bearing job executes. A split at step level inside one job does not hold: an earlier step can rewrite the script, the editable install or the venv, write `$GITHUB_ENV`/`$GITHUB_PATH` for later steps, or leave a daemon running (§2.5).
  - `check` (trusted) runs `check` and outputs a JSON list of legs (one per line with a candidate, each carrying tag, line and gate fields).
  - `bump` (trusted) has `needs: check` and is a matrix over that list (`strategy.matrix.leg: ${{ fromJSON(needs.check.outputs.legs) }}`, `max-parallel: 1`, `fail-fast: false`), `if: needs.check.outputs.legs != '[]'`. Per leg it runs fetch, bump and push, and always writes the leg record (§2.2 `record`).
  - `prove` (untrusted) has `needs: [check, bump]` and is a matrix over the same list with the same strategy and `if: always() && needs.check.result == 'success' && needs.check.outputs.legs != '[]'`: `needs` makes it wait until every `bump` leg has finished and uploaded its record (jobs without `needs` start at once), and `always()` keeps a failed `bump` leg from skipping it, so one failed `bump` leg never skips another leg's proof. It runs the editable install, `tests` and `prove`.
  - `report` (trusted, not a matrix) has `needs: [check, bump, prove]` (the `needs` context holds only the jobs a job lists, so every job that reads `needs.check.*` lists `check`), `if: always() && needs.check.result == 'success' && needs.check.outputs.legs != '[]'`, runs the `report` subcommand, which handles every leg in order.
  - No job declares outputs except `check`, and no job reads a matrix job's outputs (matrix legs overwrite each other's outputs). Per-leg data crosses jobs only as artifacts: `leg-<tag>-<run_attempt>` (the leg record), `bumped-<tag>-<run_attempt>` (dry run only: the two rewritten files) and `proof-<tag>-<head_sha>-<run_attempt>` (the `prove` job's `--github-output` file and log). A partial "Re-run failed jobs" finds no artifacts for its attempt, so every leg is a missing-record error (exit 2) and nothing is filed; re-run the whole workflow instead.
- `if: github.repository == 'IronbellyOrg/IronClaude' && github.ref == 'refs/heads/master'` on **every** job (combined with the job's own condition; in `prove` and `report` after the leading `always() &&`), so forks and the upstream parent never run it, and a manual dispatch on any ref other than `master` ends with every job skipped. A scheduled run passes the ref check (scheduled runs use the default branch, `master`); T7 dispatches with `--ref master`. Limit, UNVERIFIED (no fetched GitHub page states which copy of the workflow file a dispatch on another ref runs; the `github.workflow_ref` example only suggests that ref's copy): if a dispatch runs the dispatched ref's copy, a branch that edits this file can drop the guard, so the guard stops a mistaken or stale-branch dispatch, not a person who can push workflow changes. Renaming the default branch would skip every job until this literal is updated.
- `permissions:` per job, least privilege; everything else none (repo default is `read`, fact 4). `check`: `contents: read`, `pull-requests: read` (the gate's branch and PR lookups). `bump`: `contents: write` (push the branch). `prove`: `contents: read` only. `report`: exactly `contents: write` (delete a superseded bot branch, §2.4), `pull-requests: write` (open, edit, mark ready, close the PR), `issues: write` (integrity and infrastructure issues, label, §2.5), `actions: write` (dispatch `test.yml`; also covers reading the last run conclusions for the infrastructure counter). `attestations: read` is not needed: `gh attestation verify -R colbymchenry/codegraph` calls `GET /repos/colbymchenry/codegraph/attestations/<digest>` (gh `pkg/cmd/attestation/api/client.go:117` at `cli/cli@9490d204`), which GitHub documents as usable "without authentication or the aforementioned permissions if only public resources are requested" (https://docs.github.com/en/rest/repos/attestations), and a `GITHUB_TOKEN` permission only covers the workflow's own repository (https://docs.github.com/en/actions/concepts/security/github_token). gh does require a token to be present (`verify.go:245`), which `GH_TOKEN` on the `fetch` step provides (`.dev/codegraph-migration/review/M-open-questions-analysis.md`, question 1).
- **Token isolation.** Every `actions/checkout` step sets `persist-credentials: false` (precedent `.github/workflows/test.yml:144`; the checkout default `true` would leave the job token in `.git/config` while `prove` runs the third-party codegraph binary). `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` is set only on steps that call `gh` (`check`; `fetch` in `bump`; `report`) and on the push step, which pushes with `git -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $(printf 'x-access-token:%s' "$GH_TOKEN" | base64 -w0)" push origin codegraph/bump-<tag>`. The `prove` job gets no `GH_TOKEN` and no secrets, and its job token is read-only.
  - Trusted jobs (`check`, `bump`, `report`) never run code from a branch the bot pushed, never run the third-party binary, and never install or import the workspace: they check out `github.sha` (a `master` commit while the ref guard above is in the file: on a dispatch `github.sha` is the head of the dispatched ref, and the guard admits only `refs/heads/master`), run only `python3 -I scripts/codegraph_release.py` with the runner's `python3`, and use no `setup-uv`, `actions/cache`, `uv pip install` or `pytest`.
  - Only `prove` uses `setup-uv`, with `enable-cache: false`: setup-uv caches by default, and a cache saved by a run on `master` can be restored by other runs.
  - Every `actions/download-artifact` step sets `path: ${{ runner.temp }}/<unique subdirectory>`; the default path is the workspace, where an artifact could overwrite the script.
  - No `run:` text contains a `${{ needs.`, `${{ steps.`, `${{ matrix.` or `${{ inputs.` expression; such values reach a step only through `env:` (tags come from upstream release names).
- **Dry run.** The push, the `report` side effects and the `test.yml` dispatch are gated on `inputs.dry_run != true`. In a dry run `bump` uploads `bumped-<tag>-<run_attempt>`, `prove` checks out `github.sha` and lays those two files over it, and `report` handles every leg with `apply --dry-run`, which prints the commands instead.
- Optional repository variable `CODEGRAPH_MONITOR_ASSIGNEE` (a GitHub login): when set, every PR and issue the monitor opens is assigned to it (the owner is an organisation, so there is no single owner login; M-c item 5). When unset, nothing is assigned.
- `concurrency: { group: codegraph-release-monitor, cancel-in-progress: false }`; `runs-on: ubuntu-latest`; `timeout-minutes: 30` (four tarballs of about 63 MB each, one real install, one index).
- Steps per job (the §2.1 order). Every job starts with `actions/checkout@v4` (`persist-credentials: false`; `fetch-depth: 0` where git history is read).
  - `check`: `check`.
  - `bump` (per leg): `fetch` (into `${{ runner.temp }}/fetch`). On a re-prove leg `bump` and `push` are skipped (the record reads the branch head as data, §2.2 `record`). Otherwise `bump`, then `push` (only if `fetch` `result == 'ok'`, the gate says `branch_exists` is false and not a dry run). Then, with `if: always()`, `record` (the push step's outcome passed through `env:`) and the upload of `leg-<tag>-<run_attempt>`, so a pushed branch always reaches `report`. In a dry run, after `bump`, the upload of `bumped-<tag>-<run_attempt>`.
  - `prove` (per leg): download the leg record. Every later step runs only when the record's `fetch_result` is `ok` and the leg pushed, has an existing branch or is part of a dry run (the legs §2.2 `report` (b) proves), so a leg whose fetch or push failed runs no untrusted code. Check out the record's `head_sha` (pushed or re-prove leg), or in a dry run `github.sha` plus the `bumped-*` overlay. Then `astral-sh/setup-uv@v10.3.2` with Python 3.10, `activate-environment: true` and `enable-cache: false`, and `uv pip install -e ".[dev]"` (the setup block of `.github/workflows/test.yml`, which is the precedent to mirror and is dispatched, not edited); later steps call the activated venv's `python` and `pytest` directly, never `uv run`. Then `tests` (`pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py tests/cli/test_codegraph_release.py`), `prove`, and, with `if: always()` after the fetch gate, the proof-file step (it records `stage=tests` when `tests` failed and `stage=aborted` when `prove` wrote no result) and the upload of `proof-<tag>-<head_sha>-<run_attempt>`. The `tests` and `prove` steps run third-party code with no token (Coder strips tokens the same way).
  - `report`: download all `leg-*` and all `proof-*` artifacts of this run attempt (one pattern step each, into separate `${{ runner.temp }}` subdirectories), then `report` (`--dry-run` when `inputs.dry_run` is true, passed through `env:`).
- Idempotency: §2.4 "Branches and idempotency" and §2.5 keys; the workflow only executes the `route` actions.
- Commit: author `github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>`, message `chore(deps): bump codegraph pin to <tag>` with body lines `Old: <previous>`, `New: <tag>`, `Release: https://github.com/colbymchenry/codegraph/releases/tag/<tag>`, `Verified: SHA256SUMS hashes and gh attestation verify (5 files)`.
- PR (executed by `apply`): `gh pr create --repo "$GITHUB_REPOSITORY" --base master --head <branch> --title "<title from route>" --body-file <body>` plus `--draft` when `route` says so (never a bare `gh pr create`: repo CLAUDE.md rule; `$GITHUB_REPOSITORY` is `IronbellyOrg/IronClaude` because of the job `if:`). The branch is pushed only after `fetch` passed, so it never carries unverified hashes (M-c), and before `tests`/`prove`, so `report` (`if: always()`, reading the always-uploaded leg record) never leaves a pushed branch without a PR (Coder pattern); if `tests` or `prove` aborted without a result, or the proof is missing or invalid, `report` opens a behaviour-failure draft (`stage=aborted`). A cancelled run, or a `report` job that never runs, can still leave a pushed branch without a PR (the same residual as a crash between push and apply in one job; the next run sees `branch_exists`, §2.4).
- CI on the bump branch (executed by `apply`): after the PR exists, `gh workflow run test.yml --repo "$GITHUB_REPOSITORY" --ref <branch>` (fact 5). The PR body says CI was dispatched and links the Actions page filtered by branch.
- Step summary on every path (none, skipped, pass, behaviour failure, integrity failure, infrastructure failure), so a run is readable without logs.

### 2.4 Candidate selection

Rules from decisions M-a (`decisions/M-major-versions/recommendation.md`) and M-b (`decisions/M-release-age/recommendation.md`); see `## Decisions`.

- **Release list:** `gh api --paginate --slurp 'repos/colbymchenry/codegraph/releases?per_page=100'`, flattened (30 releases exist today, W4 §1; paginate so the list is never cut). Never the `releases/latest` endpoint or flag.
- **Candidate set:** drop drafts, prereleases, tags `parse_version` rejects (each logged with its reason in the summary), and releases without `published_at`. Keep releases strictly newer than the pin by semver. Order by semver, never by date.
- **Two lines, evaluated separately every run:** (1) the *within-major line*: releases with the pin's major; (2) the *higher-major line*: releases with a higher major. A pending major never blocks a minor or patch bump. One run can act on both lines.
- **Pick per line:** the highest-semver release in that line. It is eligible when `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds (inclusive, exact seconds), `MIN_AGE_DAYS = 14`. If it is younger, that line does nothing this run: **no fallback** to an older eligible release (an older one is usually the release upstream already patched).
- **Manual override:** `workflow_dispatch` input `min_age_days` (a whole number, 0 or more; any other value fails the run before any download; scheduled runs always use 14). It changes only the age; pick, verification, proof and human merge stay the same. The summary and the PR body record the override and its value. The `tag` input bypasses the pick for a manual run, never the strictly-newer rule: only a tag newer than the pin, or the pin itself with `dry_run` for a re-proof, is accepted (§2.2 `check --tag`).
- **Within-major path:** verify, rewrite, proof; ready PR on a passed proof, titled `chore(deps): bump codegraph pin to <tag>`.
- **Higher-major path:** the same verify, rewrite and proof on the same code path; the PR is **always a draft**, even on a passed proof, titled `codegraph MAJOR <tag>: manual review`. Its body carries the proof log, hashes and attestation result, a **link** to the release notes (not the text), and a checklist: "read the breaking changes"; "check the Phase 3 skills that call codegraph tools (`rg -l 'codegraph_' src/superclaude`)"; "check `MCP_TOOLS` still names the tools those skills use". Label `codegraph-major` only if it already exists (labels are best-effort; none exists today, fact 4). A person marks it ready and merges, or closes it to decline.
- **Branches and idempotency (M-c rule, reconciled with M-a; see `## Decisions` row "Branch rule"):** one branch per version, `codegraph/bump-<tag>`, on both lines. The monitor never pushes or force-pushes a branch that already exists. `check` owns this gate (§2.2 `gate`, before any download): a declined tag stops the line with no download; if `codegraph/bump-<tag>` exists, the leg checks out that branch and re-proves its head and reports by comment only when the fingerprint changed (§2.5). One open PR per line at a time: when a newer tag becomes the line's candidate, the monitor opens its PR and closes the line's older open bot PR with the comment "superseded by `<new tag>`"; it deletes the older branch only if every commit since `master` is the bot's. This keeps M-a's "never a duplicate PR per line" without force-pushes. An open major draft that conflicts after a 1.x bump merges is left for the person reviewing it (the re-proof comment says "rebase needed" when `git merge-tree` reports a conflict) or is superseded by the next release of that major.
- **Declined version:** if the PR for `codegraph/bump-<tag>` was closed without merging (`gh pr list --repo "$GITHUB_REPOSITORY" --head codegraph/bump-<tag> --state closed --json number,mergedAt`), later runs do nothing for that tag on either line; a newer release (for example `v2.0.1`) is a new candidate. A PR the monitor itself closed as superseded counts the same.
- **Reporting:** the summary names, per line, the release that is waiting and the UTC time it becomes eligible, and adds `::warning::` when the oldest release newer than the pin is at least 28 days old (`2 * MIN_AGE_DAYS`) and the run bumped nothing on that line. Reporting never changes the pick.
- **Pulled or re-tagged releases:** a re-created release has a new `published_at`, so its clock restarts; a deleted release drops out of the set on the next run. If an open bot PR targets a tag that no longer exists upstream, the monitor comments once "release `<tag>` was deleted upstream; close this PR" (fingerprinted) and leaves it to a person; it never merges or silently closes it (simple decision; M-b flagged item 4).

Replay check (from M-b): with the pin below v1.3.0 and daily runs over 2026, the rule bumps on 08-04 to v1.5.0, 09-09 to v1.6.0 and 10-17 to v1.6.2; today (2026-10-30) it bumps nothing (v1.6.2 is the pin).

### 2.5 Proof and failure handling

`prove` (isolated, never the real HOME). Sandbox layout: `<root>` = `tempfile.mkdtemp()`, child `HOME=<root>/home`, child `PATH=<root>/home/.local/bin:/usr/bin:/bin`, index project in `<root>/project`. It asserts at start that the child `HOME` differs from the parent's `Path.home()` and that `shutil.which("codegraph", path=<child PATH>)` is None:
1. **install**: child process `sys.executable -c` with that `HOME` and `PATH`, `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`, `CODEGRAPH_NO_UPDATE_CHECK=1`, running `install_codegraph.acquire(runner)` from the working tree (so the rewritten pin, the real download URL and the real SHA-256 check are what users will run). Pass = `ok` and the returned launcher exists. `acquire` downloads only the runner's own asset (`install_codegraph.py:280-281`, `linux-x64` on `ubuntu-latest`); the other three hashes rest on `SHA256SUMS` plus the attestations, and the PR body names the asset that was install-proved.
2. **version**: `<launcher> --version` prints exactly the new `VERSION`.
3. **index**: a fresh `git init -q` directory holding a copy of `src/superclaude/cli/install_codegraph.py`; `codegraph init --yes` exits 0; `codegraph query acquire` exits 0 and its output names `install_codegraph.py` (same pattern as Phase 2 layer 2 step 4, `evidence/p2-layer2.sh`).
4. **tools**: `mcp_tool_names(launcher, project, env + {"CODEGRAPH_MCP_TOOLS": install_codegraph.MCP_TOOLS})`; `tool_problems(...)` must be empty: every `MCP_TOOLS` tool is listed and nothing else is (Phase 2 relied on an explicit list hiding every other tool, F2 merged method, so an extra tool is a regression too).
5. **drift**: `<launcher> install --print-config claude` (no file writes, fact 2) exits 0; `entry_drift(package_values(...)["expected_entry"], stdout)` must be empty (the expected entry is `install_mcp._codegraph_entry(launcher)`, read through the child process of §2.2).
Every step's command, exit code and the first 200 lines of output go to the proof log; `<root>` (sandbox HOME and project) is deleted unless `--keep`. Any daemon the index or MCP run started is killed by process group on exit (codegraph's daemon outlives the client, W4 §5.7 `:221`); the separate `prove` job (§2.3) is what keeps a surviving daemon away from the token-bearing jobs. The `prove` job is untrusted: its proof only promotes a within-major PR to ready and is never a merge gate; human merge and the dispatched `test.yml` remain the gate.

**Failure outcomes (decision M-c, `decisions/M-proof-failure/recommendation.md`; merged rule `decisions/M-proof-failure/adversarial/M-proof-failure-merged.md`).** Never both an issue and a PR for one failure: exactly one artifact per class.

Classification (fail closed, `classify`):

| Observation | Class |
|---|---|
| `gh api rate_limit` fails, or a download is still short or erroring after one retry | infrastructure |
| A complete download (exit 0, byte length equals the release API asset `size`) whose SHA-256 mismatches its `SHA256SUMS` line twice (re-downloaded once) | integrity |
| `gh attestation verify` fails twice while the `rate_limit` preflight succeeds | integrity |
| `tests`, install, version, index, tools or drift fails after integrity passed, or a step aborted without a result (`stage=aborted`) | behaviour |
| Anything else, or ambiguous | integrity |

A failed `git push` (fetch passed, no branch was pushed) is not a `classify` observation and has no `stage` value: `report` logs it as an error for that leg (`::warning::` naming the tag, exit 2) and files nothing. The run still ends red, so the infrastructure counter below counts it like any failed scheduled run. The next run's gate retries the push, or re-proves the branch if the push did land (`branch_exists`, §2.4).

| Class | Artifact | Key (how later runs find it) | Later runs |
|---|---|---|---|
| Integrity | **Issue only.** No branch, no PR, no hash written anywhere. Title `codegraph <tag>: integrity check failed`, no label. Body: run URL, asset, expected and actual hash or the attestation output, reproduce commands (`gh release download <tag> -R colbymchenry/codegraph ...`, `sha256sum -c`, `gh attestation verify ...`). Assigned to `CODEGRAPH_MONITOR_ASSIGNEE` when set. | HTML marker `<!-- codegraph-monitor:<tag>:integrity -->` in the body (never the title) | Comment only when the fingerprint changed. The monitor **never closes** it; only a person does. A later pass for the same tag still opens its PR, which links the issue. A newer release adds a link comment and leaves it open. |
| Behaviour | **Draft PR only, no issue.** Branch `codegraph/bump-<tag>` (verified hashes only). Title = the pass-path title plus ` [proof failed: <stage>]` (within-major `chore(deps): bump codegraph pin to <tag> [proof failed: tools]`; major `codegraph MAJOR <tag>: manual review [proof failed: tools]`, so "major review" and "proof failed" stay distinct, M-a item 5). Label `needs-codegraph-proof`, created with `gh label create needs-codegraph-proof --force --repo "$GITHUB_REPOSITORY"` and applied in a step with `continue-on-error: true` (the draft state is the gate; the label is best effort). Body: stage, proof log tail, run URL, reproduce commands. | branch name `codegraph/bump-<tag>` | Re-prove the branch head; comment only when the fingerprint changed. If the proof passes at the head **and** the head's `SHA256` table equals the hashes verified in the same run: remove the ` [proof failed: ...]` title suffix and the label, and mark ready (`gh pr ready`) on the within-major line only (a major stays draft, M-a). If the table differs, stay draft and comment. |
| Infrastructure | `::warning::` plus a step summary; the job ends with a **failed** conclusion. Integrity and behaviour outcomes end the job green once `apply` has filed their issue or draft PR, so on scheduled runs a red conclusion means an infrastructure failure or a crash of the monitor itself (both worth escalating); invalid manual input exits 1 before anything runs. | marker `<!-- codegraph-monitor:infra -->` | On an infrastructure failure the run reads the 2 most recent **completed** scheduled runs (`gh run list --repo "$GITHUB_REPOSITORY" --workflow codegraph-release-monitor.yml --event schedule --status completed --limit 2 --json conclusion`; the current, still-running run is excluded by `--status completed`); when both are `failure`, this run is the 3rd in a row, and it opens one issue `codegraph monitor: cannot reach upstream` (or comments on the open one when the fingerprint changed) with the three run URLs. The first later run whose preflight passes and in which no leg has an infrastructure outcome closes that issue (a leg failing at `stage=download` passed the preflight but is still an infrastructure outcome, so it never closes the issue). |

Fingerprint = class, stage, first error line, branch head SHA (`fingerprint`, §2.2). A run whose fingerprint equals the stored one is a no-op for that artifact.

### 2.6 PR body

Sections, in order: one-line summary (`codegraph <previous> -> <tag>`, MAJOR/minor/patch); a table of the four assets with their new SHA-256 and "matches SHA256SUMS: yes"; "Attestation: `gh attestation verify -R colbymchenry/codegraph` passed for 5 files"; proof result with the five stages and a link to the run; "CI: `test.yml` dispatched on this branch" with the link; "Coder: before Coder's IronClaude-SHA bump that includes this change merges, update `templates/VSCode-AIDev02/Dockerfile.coder` `CG_VERSION`/`CG_SHA256` (linux-x64, linux-arm64) and `templates/VSCode-AIDev02/scripts/startup.sh` `aidev_cg_version` to these values; Coder's test-71 and test-57 fail until then" (fact 6); then "Release notes" for every release after the old pin up to the new tag, newest first, each under its own heading with its URL, cut at `NOTES_BUDGET` characters with "(truncated; full notes: <URL>)". A major PR (§2.4) carries links to those releases instead of their text, plus its review checklist. A PR opened with a `min_age_days` override says so with the value. A behaviour-failure draft adds the failed stage, the log tail and reproduce commands at the top. Every body ends with the fingerprint marker (§2.5). Release-note text is untrusted third-party content: it is placed in the body only through `--body-file`, never interpolated into a shell command.

## 3. Tests

All offline: no test touches the network, the real HOME, the real `gh` or a real `codegraph` (same rule as `tests/cli/test_install_codegraph.py:3-5`). `_gh` and `_run` are replaced with recording fakes; HOME points at `tmp_path`.

**`tests/cli/test_codegraph_release.py` (T2, T3):**

| ID | Case |
|---|---|
| R1 | `parse_version`: `v1.6.2` -> (1,6,2); `v2.0.0` -> (2,0,0); `1.6.2`, `v1.6`, `v1.7.0-rc.1`, `nightly` -> None. |
| R2 | `read_pin` on the real `install_codegraph.py` returns `(install_codegraph.VERSION, install_codegraph.SHA256)`; a copy with two `VERSION` lines, a missing asset line, or a 63-hex digest raises `ValueError`. |
| R3 | `ASSETS` equals `set(install_codegraph.SHA256)`. |
| R4 | `pick_candidates` on `fixtures/codegraph_release/releases.json` (the real 8-release list of fact 1 plus synthetic entries, each case sets a fixed `now`): equal pin -> nothing; empty list; only drafts or prereleases; unparsable tag skipped with reason; a release without `published_at` skipped; age 14 days minus 1 s (not eligible), exactly 14 days (eligible), 14 days plus 1 s; newest too young with an older eligible release -> nothing (no fallback) and `waiting` names the newest; a backport published after a higher version (semver order wins, not date); a re-created release (new `published_at` restarts the clock); `min_age_days=0`; a pending `v2.0.0` alongside an eligible `v1.7.1` -> both lines set; stall warning at 28 days; the M-b 2026 replay (pin below v1.3.0, daily `now` at 06:23:00Z, the cron time, from 07-01 to 10-30, with the real `published_at` timestamps in `releases.json`: bumps exactly on 08-04 to v1.5.0, 09-09 to v1.6.0, 10-17 to v1.6.2; the pin advances after each bump). |
| R5 | `parse_sha256sums` on `fixtures/codegraph_release/SHA256SUMS` (the real v1.6.2 file, 6 archives) returns the four tarball digests; missing asset, duplicate line, uppercase or short hex each raise. |
| R6 | `rewrite_pin` on the real `install_codegraph.py` text with `1.7.0` and four fake digests: `read_pin(result)` matches; `difflib` shows exactly 5 changed lines; the result passes `ruff format --check` (run `shutil.which("ruff")` then `ruff format --check -` on it via `subprocess` with stdin; `pytest.skip` with a reason when `ruff` is not on PATH, which only happens outside the dev venv, `pyproject.toml:54`); `TAG` line unchanged (it derives from `VERSION`). |
| R7 | `rewrite_pin` then `importlib` load of the rewritten copy from `tmp_path`: module `VERSION`, `TAG` and `SHA256` equal the new values. |
| R8 | `render_sums_fixture` output parsed exactly as `test_u2_pin_integrity` does (`splitlines()[1:]`, `line.split()`) yields the four assets. |
| R9 | `tool_problems`: exact set passes; one missing tool, one extra tool (`codegraph_explore`) each give one message. |
| R10 | `entry_drift` on `fixtures/codegraph_release/print-config-claude.txt` (the real v1.6.2 output shape: `# Add to ...` line plus JSON with `type`, `command: "codegraph"`, `args`, `alwaysLoad`) against `install_mcp._codegraph_entry(Path("/x/codegraph"))`: no drift. Changed `args`, `alwaysLoad: false`, a new upstream key (`"timeout": 30`), and invalid JSON each report drift. |
| R11 | `build_body`: three releases with 40,000-character notes: body <= 65,000 characters, newest notes complete, the rest replaced by "(truncated; full notes: <URL>)"; the body contains every asset hash and the Coder line. |
| R12 | `fetch` with a fake `_gh` that writes fixture files: OK path writes `.verified` last; a complete tarball whose bytes do not match its sums line on both the first download and the one re-download -> `result=integrity`, `stage=hash`, no `.verified`; a mismatch that clears on re-download passes; a short download (length differs from the asset `size`) after one retry -> `infrastructure`; attestation failure on any of the 5 files on both attempts with the `rate_limit` preflight passing -> `integrity`, `stage=attestation`; download failure after one retry -> `infrastructure`; every result other than `ok` writes one `error=` line of at most 500 characters, and an attestation failure also writes `D/fetch-error.txt` of at most 4 KiB. |
| R13 | `bump` refuses without `.verified` or with a different tag in it (exit 1, no file changed); with it, rewrites both files in a `tmp_path` copy of the repo layout. |
| R14 | `mcp_tool_names` against `fixtures/codegraph_release/fake_mcp_server.py` (a 30-line stdio JSON-RPC server that lists tools named by its env) returns those names; a server that never answers is killed within the timeout and raises. |
| R15 | `prove` with `_run` and `mcp_tool_names` faked: each stage failure sets the matching `stage=`; it refuses to run when the computed child HOME equals the parent HOME. |
| R16 | CLI: `--github-output <file>` gets `key=value` lines; `check` with a failing `_gh` exits 2 with `result=infrastructure`; a non-integer or negative `--min-age-days` (cases `-1`, `abc`, `1.5`) exits 1 before any `_gh` download call. |
| R17 | `classify` (9 cases, M-c merged §9): rate-limit failure; short download after retry; download error after retry; hash mismatch twice on a complete download; hash mismatch once then match (passes); attestation failure twice with preflight OK; attestation failure with preflight failing (infrastructure); tools failure after integrity passed (behaviour); an unknown observation (integrity). |
| R18 | `route` (17 cases): within-major pass -> ready PR with the plain title; major pass -> draft with `codegraph MAJOR`; integrity -> issue only with the marker, no branch action; integrity with no existing branch, PR or issue (a fresh leg) -> exactly one `open_issue` with the marker and a body file, and no other action; behaviour within-major -> draft with ` [proof failed: <stage>]` and label; behaviour major -> draft with both markers in the title; second run, same fingerprint -> `noop`; second run, changed fingerprint -> one comment; existing branch -> re-prove and comment, never push; later pass on a behaviour draft with an equal table -> retitle and mark ready (within-major) / retitle only (major); later pass with a different table -> stay draft and comment; newer tag on a line with an open PR -> open new PR and `close_superseded`; closed-unmerged PR for the tag -> `noop`; integrity issue open and then a pass for the same tag -> PR links the issue and the issue stays open; 3rd failed run in a row -> infra issue; first preflight pass with no infrastructure outcome and an infra issue open -> `close_issue`; a `stage=download` infrastructure outcome with the infra issue open -> no `close_issue`. |
| R19 | Deleted release: an open bot PR whose tag is no longer in the release list gets one fingerprinted comment and is never closed by the monitor. |
| R20 | `gate`: no branch, no PR -> all false; remote branch exists with an open PR -> `branch_exists` and `reprove`; closed-unmerged PR for the tag -> `declined` (and `check` emits no download for that line); `check --tag` with pin `v1.6.2`: `--tag v1.6.2` without `--dry-run` exits 1, and with `--dry-run` emits the pin as the within-major candidate (T7); `--tag v1.6.1` exits 1 both without and with `--dry-run`; a lower-major `--tag v0.9.0` (published and stable in the fixture list) exits 1 both without and with `--dry-run`; `--tag v1.7.0` emits a within-major candidate and `--tag v2.0.0` a higher-major candidate; each refusal makes no `_gh` download call (synthetic fixture entries are documented in the `_comment` key); a two-page `--slurp` release list is flattened. |
| R21 | `apply` with a recording `_gh`: every action becomes the expected `gh` argv and each carries `--repo` equal to `$GITHUB_REPOSITORY`; an action naming any other repository is refused; a failing label call is logged and the run continues; `--dry-run` runs nothing. |
| R22 | `package_values` and `prove` start Python children with `sys.executable`; the sandbox paths are `HOME=<root>/home` and `PATH=<root>/home/.local/bin:/usr/bin:/bin`; the import check of the script (AST over every `Import`/`ImportFrom` node, including indented ones) finds only modules in `sys.stdlib_module_names`. |
| R23 | `record` and `report` with a recording `_gh` and faked git: `record` after a passing fetch carries the four hashes and `head_table_matches`; after a failed fetch it carries no hashes and `head_table_matches` is false. `report`: a valid pass proof routes `pass`; a proof with a wrong tag or head_sha, a second proof for the same leg, a malformed or over-1-MiB file, or no proof routes `stage=aborted`; a record with `fetch_result=integrity` on a re-prove leg routes integrity, not aborted; an `ls-remote` head different from the record routes `stage=aborted`; `mark_ready` is emitted only when `head_table_matches` is true; a dry run calls `apply --dry-run`; an exception on leg 1 still processes leg 2 and the exit code is 2; an empty `--legs` exits 0 with no `_gh` call. `record` after a hash failure also carries `asset`, `expected`, `actual` and `error`, after an attestation failure `error` and `attestation_output` (at most 4 KiB), and on a leg with no branch a `head_sha` equal to `GITHUB_SHA`. `report` on fresh legs: a non-dry-run leg with `fetch_result=integrity`, `stage=hash` and no proof -> exactly one `gh issue create` with `--body-file` whose body carries the integrity marker, the asset and both hashes, no `gh pr` call, no `body` run and no `git ls-remote`, exit 0; the same leg with an `expected` that is not 64 lowercase hex -> the issue is still filed and its body says `detail failed validation; see the run log`; a `stage=attestation` leg with empty `asset`, `expected` and `actual` -> the body carries the attestation output and no `detail failed validation`; a leg with `fetch_result=infrastructure`, `stage=download` and no proof -> one `gh run list` call, the infra issue when both earlier scheduled runs failed and none when only one did, no `close_issue`, exit 2 in both; a dry-run leg with a valid pass proof -> routes `pass` with no `git ls-remote` and calls `apply --dry-run`; a leg with `fetch_result=ok`, `pushed=false`, `branch_exists=false` and not dry run -> a `::warning::` naming the tag, no `route` or `apply` `_gh` call, exit 2, and the next leg is still processed; a leg with `pushed=false` and `branch_exists=true` -> proved per (b); a missing record -> an error for that leg, the next leg still runs, exit 2. |

**`tests/cli/test_codegraph_release_workflow.py` (T4):** `yaml.safe_load` of the workflow: `on` has `schedule` and `workflow_dispatch` with inputs `dry_run`, `tag` and `min_age_days`; the schedule passes no `min_age_days`; the jobs are exactly `check`, `bump`, `prove`, `report`; **every** job's `if` names `IronbellyOrg/IronClaude` and contains `github.ref == 'refs/heads/master'`, the `prove` and `report` conditions start with `always()` and require `needs.check.result == 'success'` and a non-empty legs list, and `bump`'s requires a non-empty legs list; `needs` per job is exactly `check` none, `bump` {check}, `prove` {check, bump}, `report` {check, bump, prove} (a string `needs` read as a one-element set), and every `needs.<job>` expression in a job names a job in that job's own `needs`; `bump` and `prove` are matrices over `fromJSON(needs.check.outputs.legs)` with `max-parallel: 1` and `fail-fast: false`; no job except `check` declares `outputs`; `permissions` per job are exactly `check` `{contents: read, pull-requests: read}`, `bump` `{contents: write}`, `prove` `{contents: read}`, `report` `{contents: write, pull-requests: write, issues: write, actions: write}`; every `actions/checkout` step has `persist-credentials: false`; `check`, `bump` and `report` check out no `ref:` other than the default (`github.sha`), contain no `setup-uv`, `actions/cache`, `uv pip install` or `pytest`, and every script call there is `python3 -I scripts/codegraph_release.py`; `setup-uv` appears only in `prove`, with `enable-cache: false`; `GH_TOKEN` appears only on the check, fetch, push and report steps and never in `prove`, and `prove` references no `secrets.`; every `actions/download-artifact` step's `path` starts with `${{ runner.temp }}/`; in `bump` the record step and its upload, and in `prove` the proof-file step and its upload, have an `if` that starts with `always()`; no `run:` text contains `${{ needs.`, `${{ steps.`, `${{ matrix.` or `${{ inputs.`; no step text contains `SuperClaude-Org`; after joining `\`-continued lines, no `gh pr create` appears in the workflow at all (PRs are opened by `apply`), and the same joined-line check over `scripts/codegraph_release.py` finds `--repo` on every `gh pr`/`gh issue`/`gh workflow`/`gh label` call it builds; every `run:` that calls the script uses `scripts/codegraph_release.py`; per-job step order: `bump` fetch, bump, push, record, record upload; `prove` record download, checkout, setup-uv, install, tests (a `pytest` call naming the five files of §2.3), prove, proof file, proof upload; `report` downloads, then `report`; the push step is gated on `fetch` `result == 'ok'`, on the gate's `branch_exists` being false and on `inputs.dry_run != true`; no `git push` uses `--force` or `--force-with-lease` (M-c: never push an existing branch); the dry-run path gives `report` `--dry-run` (through `env:`), so `apply` and the dispatch run only with `inputs.dry_run != true`; the workflow contains no `gh pr merge` and no `--auto`.

**Existing tests kept green (T1):** `tests/cli/test_install_codegraph.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py`, `tests/cli/test_install_mcp_registry.py`. T1 adds a version-agnostic guard in `tests/cli/test_install_codegraph.py`: `test_u2_pin_integrity` now reads F1, and the new test `test_no_pinned_version_literals_in_tests` asserts that the three test files of F2-F4 contain no `\d+\.\d+\.\d+` literal equal to or above the current `install_codegraph.VERSION` (the guard that keeps the next bump a one-file change).

**Live, opt-in (T3, T6):** `uv run python scripts/codegraph_release.py prove` on the current pin, in an isolated HOME, with the network: install, version, index, tools and drift pass for the pinned version (v1.6.2 today). This is the harness's own proof and also the §2.5 drift check against today's release. Not part of `pytest`.

## 4. Task breakdown (execution order)

Each task ends at a conventional commit point; after each commit, post the §5 issue comment. Stage only the files the task names plus `.dev/tasks` (`git add .dev/tasks`, always staged) and, when a decision was taken, `.dev/codegraph-migration/decisions/MX-*`; never a `.claude/` path. Run `git status --short` after each task; a modified tracked file the task did not intend to change is a defect to fix before committing.

**T0. Verify the execution setup; record the baseline.**
Files: none in source. `"$PKG/artifacts/baseline-failures.txt"` (new).
Change: the §0 "Execution setup" already created this worktree and branch; this task checks it and records the full-suite failure baseline (the suite was not green at Phase 2's base, README `:42`). No branch switch happens inside the plan.
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"; mkdir -p "$PKG/artifacts"
grep -n '^VERSION = ' src/superclaude/cli/install_codegraph.py    # written against "1.6.2"; another value is fine (see Commit note)
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > "$PKG/artifacts/baseline-failures.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
```
Acceptance:
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
test "$(git branch --show-current)" = ironbelly/feat-codegraph-release-monitor
git fetch -q origin
git merge-base --is-ancestor 2f10a0e1e43bee841a4143235a92fc16171c9707 HEAD    # #329's merge commit is in the base
test -f .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md
test -f "$PKG/artifacts/baseline-failures.txt"
test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"
```
If the first two checks fail, the §0 setup was not done: stop as blocked and report it on issue #323 (the executor does not switch branches itself).
Commit: `chore(tasks): record the test baseline for the codegraph release monitor (#323)` (stages `.dev/tasks`, which holds the baseline). If the pin line is no longer `1.6.2` (someone bumped it by hand), continue: nothing in this plan depends on the value, only the T1 literal lists change (simple decision).

**T1. Make the pin a one-file change.**
Files: `tests/cli/fixtures/codegraph-SHA256SUMS.txt` (new), `tests/cli/test_install_codegraph.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py`, `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`.
Change: F1-F5 (§1): copy the evidence checksum lines into F1 and point `test_u2_pin_integrity` at it; replace every pinned-version literal in the three test files with `cg.VERSION` / `cg.TAG` (or `install_codegraph.VERSION` / `.TAG`, adding that import to `tests/unit/test_cli_doctor.py`); derive the `1.6.3` bump-helper literals from the pin; add `test_no_pinned_version_literals_in_tests` (§1 F2, §3); docs say "the pinned version", how to read it, and that `install_codegraph.py:26-27` is the source. Locate each site by its literal, not by line.
Acceptance:
```bash
cmp <(tail -n +2 .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt) <(tail -n +2 tests/cli/fixtures/codegraph-SHA256SUMS.txt)
uv run pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py
if git grep -n -E '1\.6\.[23]' -- tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md; then exit 1; fi
grep -q 'install_codegraph.py' docs/user-guide/mcp-installation.md
uv run ruff check tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py
uv run ruff format --check tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py
git diff --quiet -- src/superclaude/cli/install_codegraph.py .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt
```
Commit: `test(codegraph): derive the pinned version from install_codegraph in tests and docs`
Post-commit mutation check (proves the one-file property on the committed tree, in a throwaway worktree under the canonical `.dev/worktrees/`, which is gitignored at `.gitignore:238`; never edits the real worktree). It bumps `VERSION` to the next patch, minor and major of the current pin in turn (from `1.6.2`: `1.6.3`, `1.7.0`, `2.0.0`), because those are the versions a real bump produces and the ones hidden literals collide with. Only `test_u2_pin_integrity` is deselected (the made-up versions have no checksum lines); every other test must pass for all three. If it fails, fix the missed literal and amend the T1 commit before T2. The output is kept as evidence.
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
M=.dev/worktrees/m-mutation
trap 'git worktree remove --force "$M" 2>/dev/null || true' EXIT
git worktree add -q --detach "$M" HEAD
CUR=$(sed -n 's/^VERSION = "\([0-9.]*\)"$/\1/p' src/superclaude/cli/install_codegraph.py); test -n "$CUR"
IFS=. read -r MA MI PA <<< "$CUR"
for V in "$MA.$MI.$((PA+1))" "$MA.$((MI+1)).0" "$((MA+1)).0.0"; do
  sed -i "s/^VERSION = \"[0-9.]*\"$/VERSION = \"$V\"/" "$M/src/superclaude/cli/install_codegraph.py"
  grep -q "^VERSION = \"$V\"$" "$M/src/superclaude/cli/install_codegraph.py"
  (cd "$M" && uv run pytest -p no:cacheprovider -q tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_codegraph.py --deselect tests/cli/test_install_codegraph.py::test_u2_pin_integrity) 2>&1 | tee -a "$PKG/artifacts/t1-mutation.log"
done
```

**T2. Pure bump logic and its unit tests.**
Files: `scripts/codegraph_release.py` (new), `tests/cli/test_codegraph_release.py` (new), `tests/cli/fixtures/codegraph_release/releases.json`, `tests/cli/fixtures/codegraph_release/SHA256SUMS`, `tests/cli/fixtures/codegraph_release/print-config-claude.txt` (new).
Reads: `src/superclaude/cli/install_codegraph.py` (input of `read_pin`/`rewrite_pin`; `VERSION`, `TAG`, `SHA256`, `MCP_TOOLS` at `:26-35`), `src/superclaude/cli/install_mcp.py` (`_codegraph_entry` at `:862-874`, the shape `entry_drift` compares).
Change: §2.2 constants and every pure function (including `gate`, `classify`, `route`, `fingerprint`); §2.4 rules; §2.5 tables; tests R1-R11 and R17-R20 (the pure parts of R20). Fixture sources: `releases.json` from `gh api 'repos/colbymchenry/codegraph/releases?per_page=8' --jq '[.[] | {tag_name, published_at, draft, prerelease, html_url, body: (.body[:2000]), assets: [.assets[] | {name, size}]}]'` plus synthetic entries appended by hand (documented in a `_comment` key); `SHA256SUMS` from `gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS`; `print-config-claude.txt` from the T3 live run, or, if T3 has not run yet, written from `claude.ts:241-245` and replaced by the real output in T3 (simple decision).
Acceptance:
```bash
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py
uv run ruff check scripts/codegraph_release.py tests/cli/test_codegraph_release.py
uv run ruff format --check scripts/codegraph_release.py tests/cli/test_codegraph_release.py
uv run python -c 'import ast,sys; t=ast.parse(open("scripts/codegraph_release.py").read()); m={(a.name if isinstance(n,ast.Import) else n.module).split(".")[0] for n in ast.walk(t) if isinstance(n,(ast.Import,ast.ImportFrom)) and not getattr(n,"level",0) for a in (n.names if isinstance(n,ast.Import) else [n])}; bad=sorted(x for x in m if x not in sys.stdlib_module_names and x!="__future__"); print(bad); sys.exit(1 if bad else 0)'
```
Commit: `feat(codegraph): add offline-tested release bump logic`

**T3. I/O subcommands, MCP client and live harness proof.**
Files: `scripts/codegraph_release.py`, `tests/cli/test_codegraph_release.py`, `tests/cli/fixtures/codegraph_release/fake_mcp_server.py` (new), `tests/cli/fixtures/codegraph_release/print-config-claude.txt` (real output).
Reads: `src/superclaude/cli/install_codegraph.py` (`acquire` at `:271-365`, `Runner` at `:42-43`), `src/superclaude/cli/install_mcp.py` (`_codegraph_entry` at `:862-874`, through `package_values`), `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (the stdio protocol to port).
Change: `_gh`, `_run`, `package_values`, `mcp_tool_names`, subcommands `check`, `fetch`, `bump`, `record`, `prove`, `body`, `route`, `apply`, `report` (§2.2, §2.5, §2.6), including the §2.5 rules on process-group kill and the 200-line log cap; tests R12-R16 and R20-R23. Then the live proof on the current pin, isolated HOME, network on (the tag is read from the pin, never hard-coded):
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"; mkdir -p "$PKG/artifacts"
REAL_SUM=$(jq -S '.mcpServers' "$HOME/.claude.json" | sha256sum | cut -d' ' -f1)
PIN=v$(sed -n 's/^VERSION = "\([0-9.]*\)"$/\1/p' src/superclaude/cli/install_codegraph.py); test "$PIN" != v
rm -rf /tmp/m-fetch
uv run python scripts/codegraph_release.py check --github-output "$PKG/artifacts/live-check.out" > "$PKG/artifacts/live-check.log"
uv run python scripts/codegraph_release.py fetch --tag "$PIN" --dir /tmp/m-fetch --github-output "$PKG/artifacts/live-fetch.out" > "$PKG/artifacts/live-fetch.log"
uv run python scripts/codegraph_release.py prove --keep --github-output "$PKG/artifacts/live-prove.out" > "$PKG/artifacts/live-prove.log"
ROOT=$(sed -n 's/^root=//p' "$PKG/artifacts/live-prove.out"); test -n "$ROOT"
H=$(sed -n 's/^home=//p' "$PKG/artifacts/live-prove.out"); test -n "$H"
HOME="$H" CODEGRAPH_TELEMETRY=0 CODEGRAPH_NO_UPDATE_CHECK=1 "$H/.local/bin/codegraph" install --print-config claude > tests/cli/fixtures/codegraph_release/print-config-claude.txt
rm -rf "$ROOT" /tmp/m-fetch
test "$(jq -S '.mcpServers' "$HOME/.claude.json" | sha256sum | cut -d' ' -f1)" = "$REAL_SUM"   # the real HOME's MCP servers are unchanged
```
Acceptance:
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py
uv run ruff check scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py
uv run ruff format --check scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py
grep -q '^result=none$' "$PKG/artifacts/live-check.out"
grep -q '^result=ok$' "$PKG/artifacts/live-fetch.out"
grep -q '^result=pass$' "$PKG/artifacts/live-prove.out"
for s in install version index tools drift; do grep -q "$s" "$PKG/artifacts/live-prove.log"; done
grep -q '"mcpServers"' tests/cli/fixtures/codegraph_release/print-config-claude.txt
git diff --quiet -- src/superclaude/cli/install_codegraph.py
```
Commit: `feat(codegraph): verify, prove and describe a codegraph release candidate`, with `.dev/tasks` staged (the live evidence).

**T4. The scheduled workflow and its static test.**
Files: `.github/workflows/codegraph-release-monitor.yml` (new), `tests/cli/test_codegraph_release_workflow.py` (new).
Reads: `.github/workflows/test.yml` (setup block to mirror, `:54-65` and `:141-150`; `persist-credentials: false` at `:144`; dispatched, not edited).
Change: §2.1 order and §2.3 exactly, every bullet (four jobs `check`/`bump`/`prove`/`report`, both matrices with `max-parallel: 1` and `fail-fast: false`, per-job permissions, the trusted-job rules, the artifacts and their `${{ runner.temp }}` download paths, `dry_run` gating, `persist-credentials: false`, token scope, the push command, `fetch-depth: 0`, the commit author and message, the `tests` step and its five files, `prove` and `report` with `if: always()`, the `test.yml` dispatch through `apply`, a step summary on every path), plus the §2.5 infrastructure counter; the static checks of §3.
Acceptance:
```bash
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release_workflow.py
uv run python -c 'import yaml,sys; yaml.safe_load(open(".github/workflows/codegraph-release-monitor.yml"))'
if grep -n 'SuperClaude-Org' .github/workflows/codegraph-release-monitor.yml; then exit 1; fi
if grep -n 'gh pr create' .github/workflows/codegraph-release-monitor.yml; then exit 1; fi   # PRs are opened only by apply (R21 checks its --repo)
test "$(grep -c 'persist-credentials: false' .github/workflows/codegraph-release-monitor.yml)" -ge 4
uv run ruff check tests/cli/test_codegraph_release_workflow.py
uv run ruff format --check tests/cli/test_codegraph_release_workflow.py
```
If `actionlint` is on PATH, also run `actionlint .github/workflows/codegraph-release-monitor.yml` (optional; it is not installed by this plan).
Commit: `ci(codegraph): add the scheduled codegraph release monitor`

**T5. Documentation.**
Files: `.github/workflows/README.md`, `CHANGELOG.md`, `docs/user-guide/mcp-installation.md`.
Change: F10, F11, the F5 "How the pin is updated" paragraph (what the monitor does, the §2.4 rules, what a failure produces, how to run it by hand: `gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true`).
Acceptance:
```bash
grep -q 'codegraph-release-monitor.yml' .github/workflows/README.md
awk '/^## \[Unreleased\]/{f=1;next} /^## \[/{f=0} f' CHANGELOG.md | grep -qi 'codegraph release monitor'
grep -q 'codegraph-release-monitor' docs/user-guide/mcp-installation.md
grep -q '14 days' docs/user-guide/mcp-installation.md
grep -qi 'draft' docs/user-guide/mcp-installation.md
grep -qi 'integrity' docs/user-guide/mcp-installation.md
grep -qF 'gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true' docs/user-guide/mcp-installation.md
if grep -n 'SuperClaude-Org/SuperClaude_Framework/pull' docs/user-guide/mcp-installation.md .github/workflows/README.md; then exit 1; fi
```
Commit: `docs(codegraph): document the codegraph release monitor`

**T6. Final gate and PR.**
Files: none new.
Change: full-suite comparison against the T0 baseline; the T3 live proof re-run on the final tree; open the PR with `/sc:pr-submit --monitor 3`.
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > "$PKG/artifacts/final-failures.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
uv run python scripts/codegraph_release.py prove --github-output "$PKG/artifacts/final-prove.out" > "$PKG/artifacts/final-prove.log"
```
Acceptance:
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
test -z "$(comm -13 "$PKG/artifacts/baseline-failures.txt" "$PKG/artifacts/final-failures.txt")"   # no new failure
grep -q '^result=pass$' "$PKG/artifacts/final-prove.out"
uv run ruff check src/ tests/ scripts/codegraph_release.py
uv run ruff format --check src/ tests/ scripts/codegraph_release.py
make verify-sync
test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"
test "$(gh repo view --json nameWithOwner -q .nameWithOwner)" = IronbellyOrg/IronClaude
```
Then, in Claude Code: `/sc:pr-submit --monitor 3 --head ironbelly/feat-codegraph-release-monitor --title "feat(codegraph): scheduled codegraph release monitor (#323)" --body "<summary, test evidence, live proof log path, link to this spec>"` (fallback only if it cannot run: `gh pr create --repo IronbellyOrg/IronClaude --base master --head ironbelly/feat-codegraph-release-monitor ...`). Before it: the repo CLAUDE.md pre-PR checks (`git remote -v`; `git fetch origin && git log master..origin/master`, rebase onto `origin/master` if the fork moved). After it: the returned URL must start with `https://github.com/IronbellyOrg/IronClaude/pull/`; save it (`printf '%s\n' "<url>" > "$PKG/artifacts/pr-url.txt"`, with `PKG` defined as in §0) and check `grep -q '^https://github.com/IronbellyOrg/IronClaude/pull/[0-9]*$' "$PKG/artifacts/pr-url.txt"`. The issue comment also lists the debate items flagged for the user (`## Decisions`, last paragraph) and §7 item 6 (Coder bake).
Commit point: `chore(tasks): record the codegraph release monitor PR (#323)` (stages `.dev/tasks`: final failures, final proof, PR URL); the issue comment links the PR.

**T7. Post-merge live check (after the human merges, §7 item 2).**
Files: none.
Change: run the monitor once on `master` in dry-run mode with the current pin forced, then once normally, and record both runs. The first line is a mechanical merge gate: `/sc:implement` reaches T7 right after T6, and until a person merges the PR the workflow is not on `master` (dispatch would fail), so the task stops as blocked until then.
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
test "$(gh pr view "$(cat "$PKG/artifacts/pr-url.txt")" --repo IronbellyOrg/IronClaude --json state -q .state)" = MERGED   # else: stop as blocked
git fetch -q origin
PIN=v$(git show origin/master:src/superclaude/cli/install_codegraph.py | sed -n 's/^VERSION = "\([0-9.]*\)"$/\1/p'); test "$PIN" != v
newest_run() {   # the first workflow_dispatch run created after $1, polled for up to 2 minutes
  for _ in $(seq 24); do
    id=$(gh run list --repo IronbellyOrg/IronClaude --workflow codegraph-release-monitor.yml --event workflow_dispatch --limit 5 --json databaseId,createdAt --jq "[.[] | select(.createdAt > \"$1\")] | sort_by(.createdAt) | .[0].databaseId // empty")
    if [ -n "$id" ]; then echo "$id"; return 0; fi
    sleep 5
  done
  return 1
}
T1=$(date -u +%FT%TZ)
gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude --ref master -f dry_run=true -f tag="$PIN"
DRY=$(newest_run "$T1")
gh run watch "$DRY" --repo IronbellyOrg/IronClaude --exit-status
gh run view "$DRY" --repo IronbellyOrg/IronClaude --log > "$PKG/artifacts/post-merge-dry-run.log"
T2=$(date -u +%FT%TZ)
gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude --ref master
NORMAL=$(newest_run "$T2")
gh run watch "$NORMAL" --repo IronbellyOrg/IronClaude --exit-status
gh run view "$NORMAL" --repo IronbellyOrg/IronClaude --log > "$PKG/artifacts/post-merge-normal-run.log"
printf 'dry run: https://github.com/IronbellyOrg/IronClaude/actions/runs/%s\nnormal run: https://github.com/IronbellyOrg/IronClaude/actions/runs/%s\n' "$DRY" "$NORMAL" > "$PKG/artifacts/post-merge-runs.md"
```
Acceptance:
```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
grep -q 'result=ok' "$PKG/artifacts/post-merge-dry-run.log"      # fetch verified the pin
grep -q 'result=pass' "$PKG/artifacts/post-merge-dry-run.log"    # prove passed
PIN=v$(git show origin/master:src/superclaude/cli/install_codegraph.py | sed -n 's/^VERSION = "\([0-9.]*\)"$/\1/p')
test -z "$(gh pr list --repo IronbellyOrg/IronClaude --head "codegraph/bump-$PIN" --state all --json number -q '.[].number')"   # the dry run opened no PR
test -z "$(gh issue list --repo IronbellyOrg/IronClaude --search "codegraph $PIN in:title" --state all --json number -q '.[].number')"   # and no issue
grep -Eq 'result=(none|candidate)' "$PKG/artifacts/post-merge-normal-run.log"
test "$(gh pr list --repo IronbellyOrg/IronClaude --search 'codegraph in:title' --state open --json headRefName -q '[.[].headRefName] | group_by(.) | map(length) | max // 0')" -le 1   # at most one open PR per tag
```
If `gh attestation verify` fails in the dry run, record the exact gh error in the run log and classify it: "authentication required" or similar means `GH_TOKEN` is missing on that step (fix the step env); HTTP 403/429 with a rate-limit message is infrastructure; a verification failure is integrity (§2.5). Do not add `attestations: read`: it cannot change access to another owner's public attestations (§2.3).
Commit point: none; final issue comment with both run URLs and `"$PKG/artifacts/post-merge-runs.md"`.

## 5. Progress reporting on issue #323

After each commit point in §4 (T0, T1, T2, T3, T4, T5), after T6 opens the PR, and after T7, post exactly one comment on issue #323. Nowhere else (no PR comments for progress, no Slack). Body file, so the shell does not mangle it:

```bash
cat > /tmp/m-progress.md <<'EOF'
**codegraph release monitor (follow-up to Phase 2) progress: <task id and name>**

- Commit: <short sha> `<conventional commit subject>` on `ironbelly/feat-codegraph-release-monitor`
- Done: <one line per change>
- Tests: `<exact acceptance command>` -> <N passed / failure summary>
- Live evidence: <none | path under the package's artifacts/ folder | run URL>
- Decisions taken: <none | .dev/codegraph-migration/decisions/MX-<slug>/>
- Next: <next task>
EOF
gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file /tmp/m-progress.md
rm /tmp/m-progress.md
```

A failed acceptance run is reported as failed with its summary, never as done. The T6 and T7 comments link the PR and run URLs; a PR URL must start with `https://github.com/IronbellyOrg/IronClaude/pull/`.

## 6. Autonomy rules for the executor

The executor works without stopping to ask.

| Decision size | Example | Method |
|---|---|---|
| Simple: one obvious answer, or forced by a pinned test or a verified fact | helper names, message wording, fixture layout, summary text, cron minute | decide yourself |
| Mid: two or more viable options with real trade-offs, local to one task | how to kill a codegraph daemon the proof started; how to budget release notes; whether `check` paginates past 30 releases | write each option to `.dev/codegraph-migration/decisions/MX-<slug>/option-<x>.md` (under 40 lines each) and spawn an agent (Agent tool) that runs `/sc:adversarial --compare <files> --depth quick` |
| Complex: changes a §Decisions outcome, the single-pin rule, the PR target, the proof's five stages, or anything Coder consumes (`VERSION`, `SHA256`, `MCP_TOOLS` format in `install_codegraph.py`) | auto-merging bump PRs; moving the pin to a data file; dropping the attestation check | same, without `--depth quick` (`/sc:adversarial --compare <files>`, default standard depth) |

Follow the adversarial recommendation. Record every autonomous decision, in the commit that applies it, as a row in `.dev/codegraph-migration/decisions/MX-log.md` (create on first use): decision, options considered, method (self / adversarial quick / adversarial full), rationale, decision folder. Mention the folder in the next issue comment.

Hard rules (no decision overrides them):
- PRs only on `IronbellyOrg/IronClaude`, through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`); never push to `upstream`; never a bare `gh pr create`, also inside the workflow.
- Never stage a `.claude/` path (only `.claude/settings.json` is tracked, and this plan does not change it); always `git add .dev/tasks`; feature branch only.
- Never run `superclaude install`, `claude mcp add/remove`, `./update.sh` or `codegraph install` (without `--print-config`) against the real HOME; `prove` and the live T3 run use a sandbox HOME and the T3 block checks the real `.mcpServers` is unchanged.
- Never edit `.dev/codegraph-migration/evidence/P2-*` or other historical `.dev/` artifacts; never run `tests/cli/eval/`; restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` after a full run.
- The workflow never merges, approves or auto-merges a PR, and never pushes to `master`.

## 7. Human intervention (minimal list)

1. **Precondition:** PR #329 merged to `master` (met on 2026-10-30, merge commit `2f10a0e1`); the §0 "Execution setup" block is run before `/sc:implement` (it is not a plan task; T0 stops as blocked if it was skipped).
2. Merging the monitor PR (T6) to `master`; T7 stops as blocked until that merge and is re-run after it.
3. Every bump PR the monitor opens later is merged by a person (by design; the workflow never merges). A major draft is marked ready by a person after its checklist; an integrity issue is closed by a person after investigating (possible tampering upstream: do not change a hash by hand to make it pass).
4. A GitHub auth failure for `gh` on the executor's machine (the executor cannot log in for the user).
5. Optional, once: set the repository variable `CODEGRAPH_MONITOR_ASSIGNEE` to the GitHub login that should be assigned monitor PRs and issues (`gh variable set CODEGRAPH_MONITOR_ASSIGNEE --repo IronbellyOrg/IronClaude --body <login>`). Without it nothing is assigned, and notification of drafts is UNVERIFIED (M-c item 6).
6. Coder side, non-blocking for this plan but blocking for Coder's next IronClaude-SHA bump after each codegraph bump: in that Coder bump PR, set `CG_VERSION` (`templates/VSCode-AIDev02/Dockerfile.coder:359`), both `CG_SHA256` lines (`:361-362`) and `aidev_cg_version` (`templates/VSCode-AIDev02/scripts/startup.sh:971`) to the new `VERSION` and `SHA256["linux-x64"]`/`SHA256["linux-arm64"]` from `install_codegraph.py` at the new SHA (or teach Coder's monitor to do that); until then `.github/contract-tests/test-71-codegraph-bake.sh` and test-57 fail (fact 6, at Coder `origin/main` `25aba75d`). The executor states this in the T6 issue comment; the fix is Coder's.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| (a) Major versions: automatic or manual review | A: bump like minors (ready PR); B: issue only, manual bump; C: full automated PR, always draft | adversarial quick (`decisions/M-major-versions/recommendation.md`; C 0.875, B 0.832, A 0.697; convergence 92.9%, 13/14) | C merged with B's per-major candidate selection: a major gets the same verify and proof but always a draft PR titled `codegraph MAJOR <tag>: manual review` with a Phase 3 checklist and linked notes; within-major bumps keep flowing while a major waits. The proof checks tool names and the entry shape, not tool semantics, so a major needs a person (§2.4). |
| (b) Minimum release age | A: none; B: 14 days, newest eligible with fallback; C: 7 days, latest only | adversarial quick (`decisions/M-release-age/recommendation.md`; B 0.819, C 0.806, A 0.685; convergence 100%, 14/14) | B's 14 days (the user's two-week rule) with C's no-fallback: bump only to the highest-semver release once it is at least 14 days old, never to an older one; `min_age_days` dispatch input for a one-off security fix; stall warning at 28 days (§2.4). |
| (c) What a failed proof produces | A: draft PR + label; B: issue only; C: split by failure class | adversarial quick (`decisions/M-proof-failure/recommendation.md`; C 0.748, B 0.760, A 0.606; B and C within 5%, C won the debate-points tiebreaker 9 to 5; convergence 100%, 18/18) | Never both: integrity failure -> issue only, no branch (unverified hashes never sit on a branch; the pin is the only trust anchor, `install_codegraph.py:328-330`); behaviour failure -> draft PR with ` [proof failed: <stage>]` and label `needs-codegraph-proof`; infrastructure -> warning, issue after 3 failed runs in a row (§2.5). |
| Branch rule (conflict between (a) and (c)) | M-a merged rule: one fixed branch per line, rebuilt and force-pushed each run (`decisions/M-major-versions/recommendation.md:21`); M-c merged rule: one branch per version `codegraph/bump-<tag>`, never push an existing branch (`decisions/M-proof-failure/recommendation.md:37-41`) | self (reconciliation) | M-c's rule governs pushes because branch and push behaviour is the scope of that decision and it keeps unverified or human-edited branches from being overwritten; M-a's stated goal (never a duplicate PR per line, majors never block minors) is kept by superseding the older open PR on the same line. Cost accepted: a major draft that conflicts after a 1.x merge is rebased by its reviewer or superseded by the next release. Both sources cited here; neither file was edited. |
| Infrastructure counter (M-c open item N-006) | 1: infra run ends failed, count with `gh run list --json conclusion`; 2: neutral exit, counter stored in a run artifact | self | Option 1 needs no stored state and uses a verified `gh` flag (fact 7); a red run is the honest state when upstream cannot be reached. Integrity and behaviour outcomes end green once their issue or draft exists, so only infrastructure failures and monitor crashes end red, and 3 completed red scheduled runs in a row escalate (revised after reflect finding T1-17: the first wording counted the still-running run and every red outcome). |
| Where the bump logic lives | inline YAML (Coder style); package module under `src/superclaude/cli/`; `scripts/codegraph_release.py` | self | The brief requires offline unit tests; `scripts/` is not installed to users (maintainer tooling, precedent `scripts/verify_deps.py`) and the by-path import has a precedent (`tests/skills/test_workflow_archive.py:26-28`). |
| Single-source pin | bump rewrites every copy (tests, docs); tests and docs derive from `install_codegraph.py` | self | The brief names one source location; fact 3 shows 22 sites to rewrite (15 test literals of `1.6.2`, 2 test literals of the next version `1.6.3`, 5 docs literals). T1 removes them once and adds a guard test plus a next-patch/minor/major mutation check, so a bump touches the pin file plus its checksum fixture only. |
| Checksum record for `test_u2_pin_integrity` | keep reading and rewrite the `.dev/` evidence file; drop the check; copy to `tests/cli/fixtures/` | self | `.dev/` evidence is history and stays untouched (README `:12`); the test keeps catching hand-typed hashes; the bot rewrites the fixture from the same verified `SHA256SUMS`. |
| MCP `tools/list` client | reuse `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (needs Node); Python port in the script | self | CI must not depend on a `.dev/` evidence file; Python lets the unit tests fake the server (R14); no Node step needed. |
| `tools/list` check strictness | every `MCP_TOOLS` tool present (brief); exact set (present and nothing extra) | self | Phase 2's schema-cost decision relied on an explicit list hiding every other tool (`decisions/F2-schema-cost-method/recommendation.md`, X-25 hard stop), so an extra listed tool is a regression too. |
| Drift check fields | whole-entry compare; compare all keys except `command` and `env` | self | IronClaude deliberately registers an absolute command and its own env keys (`install_mcp.py:862-874`); every other key (`type`, `args`, `alwaysLoad`, any new key) must match upstream's `--print-config claude`. |
| CI on bot PRs | rely on PR-triggered `Tests` (approval-gated); dispatch `test.yml` on the branch | self | Fact 5: `GITHUB_TOKEN` PRs start runs only in an approval-required state; `workflow_dispatch` always runs. |
| Release notes in the PR body | full text; link only; budgeted text plus links | self | Fact 1: one release's notes exceed the 65,536-character body limit; within-major PRs carry up to 60,000 characters newest-first plus links; majors carry links (M-a). |
| Open PR for a deleted upstream release (M-b item 4) | close automatically; comment and leave | self | Never close or merge on the bot's own judgment of an upstream deletion; one fingerprinted comment tells the reviewer. |
| Runner | self-hosted (Coder); `ubuntu-latest` | self | `test.yml` already runs every job on `ubuntu-latest`; no Docker or private network is needed. |
| Branch setup for execution (reflect T1-01, T1-27) | branch switch and cherry-pick inside plan task 1; a separate worktree created before `/sc:implement` | self | A switch inside the plan moves the package and its `progress.md` ledger out from under `/sc:implement`; the repo's canonical `.dev/worktrees/` location (repo `CLAUDE.md`) gives the executor its own checkout, and the planning commit is created with the subject the setup block looks for. |
| Push before tests and prove (reflect T1-14) | push after prove (§2.1 first wording); push after fetch and before tests/prove | self | M-c only forbids pushing before integrity passes; pushing right after `fetch` and `bump` lets the `always()` route/apply step open a behaviour draft even when `tests` or `prove` aborts, which the push-after-prove order could not do. |
| Package values through a child process (reflect T1-15) | import `superclaude.cli` in the script; widen "stdlib only"; child `sys.executable -c` | self | Importing `superclaude.cli` runs `main` and `click` (`src/superclaude/cli/__init__.py:13`, `install_mcp.py:21`); one child process keeps the script stdlib-only and testable while still reading the real `MCP_TOOLS` and expected entry. |
| GitHub side effects in Python (reflect T1-21) | bash/jq executor in YAML; `apply` subcommand | self | §2.1 says every decision lives in tested Python; `apply` puts every `gh` call in one function with `--repo` enforced and unit-tested (R21), leaving only `git push` in YAML. |
| Token isolation (reflect T1-26; PR #335 review) | env-only strip on `prove`; `persist-credentials: false` plus token only on `gh` and push steps; a separate untrusted job | self (reflect); adversarial quick (PR #335 review) | `actions/checkout` defaults `persist-credentials` to `true` (its `action.yml`), so an env-only strip leaves the token on disk for third-party code; the repo already uses `persist-credentials: false` (`.github/workflows/test.yml:144`). The PR #335 review showed the step-scoped token is not enough inside one job: an earlier untrusted step can change the script, the venv, `$GITHUB_ENV`/`$GITHUB_PATH` or a cache that a later token-bearing step uses. Untrusted code now runs only in its own read-only job (row "Job layout"). |
| Job layout (PR #335 review) | reusable per-leg workflow with three jobs; one file with three jobs (`check` does every leg's fetch and push); one file with four jobs | adversarial quick (3 proposals; the one-file layout won scoring and debate, with per-leg trusted `bump` jobs and same-run hash carry merged in), then revised for an independent review's blocker | One file, four jobs (§2.3 "Jobs"): `check` and `report` trusted, `bump` trusted per leg, `prove` untrusted per leg with `contents: read`. Per-leg data crosses only as artifacts (matrix job outputs overwrite each other); `prove` and `report` run under `always()` so one failed leg never skips another leg's proof; trusted jobs never install or run workspace or bot-branch code. Replaces the every-job exact-four-permissions rule with per-job least privilege (`report` keeps the four). |
| Idempotency gate owner (reflect R1-02) | `route` after the outcome; `check` before any download | self | Only a gate before `fetch` avoids daily re-downloads of declined tags and non-fast-forward pushes onto existing branches. |

Items the debates flagged for the user (none blocks execution; the executor follows the merged rules and lists them in the T6 issue comment): M-a items 1-6 (`decisions/M-major-versions/recommendation.md:44-51`), M-b items 1-5 (`decisions/M-release-age/recommendation.md:56-62`; item 4 decided above, item 5 verified as fact 7), M-c items 1-8 (`decisions/M-proof-failure/recommendation.md:66-77`; item 3 decided above, item 5 handled by `CODEGRAPH_MONITOR_ASSIGNEE`, item 7 verified as fact 7, item 8 handled by the distinct titles in §2.5).

## Review resolution

`/sc:workflow` ran `/sc:reflect --mode pre` on the first version of this spec and its plan (report `.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/artifacts/reflect/pre-20261030154210/REPORT.md`, status partial: the adversarial merge fell back to the highest-calibrated reviewer). Every finding is fixed in this spec and in the plan:

| Finding(s) | Fix (where) |
|---|---|
| T1-01, T1-27, T1-28 | §0 "Execution setup": planning commit subject, worktree under `.dev/worktrees/`, no branch switch inside the plan; T0 verifies and stops as blocked |
| T1-26 | §2.3 "Token isolation": `persist-credentials: false`, token only on `gh` and push steps; §3 static checks |
| T1-02, T1-03, R2-01 | §0 evidence rule (`PKG` defined in every block, evidence under `"$PKG/artifacts/"`); every §4 block; T1 mutation output teed |
| R3-01 | plan acceptance lines use the `if ...; then exit 1; fi` and `test -z "$(...)"` forms |
| T1-04, T1-05, T1-06, T1-07, T1-18, R1-08 | T7: merge gate, run-id poll after a timestamp, separate greps, both runs watched, pin read from `master`; §2.2 `--tag` equal to the pin only with `--dry-run` |
| T1-14, R2-02, R3-02, R1-08 | §2.1 order (push after fetch, before tests and prove); §2.3 `tests` step with five named files; `stage=tests|aborted` |
| T1-15, T1-09, R1-05, T1-29 | §2.2 `package_values` child via `sys.executable`; AST import check against `sys.stdlib_module_names` (T2) |
| T1-16, R2-03 | §2.5 sandbox layout `<root>/home`; T3 live block removes `<root>` |
| T1-17 | §2.5 infrastructure row and Decisions row |
| T1-21, T1-10 | §2.2 `apply`; §3 R21 and static checks (no `gh pr create` in YAML) |
| R1-01, T1-22 | fact 3, F2, T1 (22 sites; next patch, minor and major mutation check; guard test) |
| R1-02 | §2.2 `gate`, §2.4 branches bullet, §3 R20 |
| R1-06 | `--paginate --slurp` (§2.2, §2.4) |
| R1-07 | §2.3 steps use the activated venv's `python` and `pytest` |
| R1-09, T1-34, T1-35, T1-36, T1-25, T1-19 | §2.3 jobs, matrix, dry-run gating, every-job `if`/permissions, re-prove leg checkout; §3 static checks |
| T1-12, R1-03, R3-03, T1-11, T1-43 | T3 live block with `--github-output` files and per-stage greps; T5 doc greps |
| T1-08 | T1 mutation `trap` |
| T1-20, T1-23, T1-24, T1-30, T1-31, T1-32, T1-33, T1-39, T1-41, T1-42, R2-04, R3-06 | F6 lists `route`/`apply`; §7 renumbered; fingerprint for branchless artifacts; R6 `shutil.which`; §2.3 UNVERIFIED `attestations: read` checked in T7; R4 replay at 06:23Z; F3 import; T1 docs pointer; T2/T3/T4 "Reads:" lines; §1 `make sync-dev` wording; T1 locate-by-literal |
| T1-13, R1-04, R3-05, T1-37, T1-38, R3-04, T1-40 | plan-only gaps: fixed in the plan (pull-link check, Constraints rules, log cap and process-group kill, Task 5 bullets, literal commands in every task) |
| PR #335 review: untrusted `prove` shared a job with token-bearing `route`/`apply` (High) | §2.1 jobs line; F6 and §2.2 `record`, `report`, `route`; §2.3 jobs, per-job permissions, token isolation, dry run, steps, PR; §2.5 daemon and untrusted-proof note; §3 R23 and the static checks; T3, T4; Decisions rows "Token isolation" and "Job layout"; plan Task 4 and Task 5 |
| PR #335 review: `check --tag` allowed a downgrade (Medium) | §2.2 `check --tag` (newer than the pin, equal only with `--dry-run`, older or lower-major exit 1); §2.3 `tag` input; §2.4 manual override; §3 R20; plan Task 4 |
| PR #335 review: R16 said exit 2 for bad `--min-age-days` (Medium) | §3 R16 exits 1 (matches §2.2 and §2.5) |
| PR #335 review round 2: a fresh leg whose fetch failed was never routed (High) | §2.2 `fetch` (`error=`, `D/fetch-error.txt`), `route` (`open_issue` body file), `record` (failure fields, `branch_exists`, `head_sha` for a leg with no branch), `report` (a)-(c), no `ls-remote` on a fresh dry-run leg; §2.3 `prove` gate and partial re-run; §2.5 push-failure paragraph and infrastructure close rule; §3 R12, R18, R23; plan Task 4 and Task 5 |
| PR #335 review round 2: no `needs:` edges between the jobs (Medium) | §2.3 `bump`, `prove`, `report` `needs`; §3 static checks; plan Task 5 |
| PR #335 review round 2: no ref guard; a dispatch on any branch ran the trusted jobs with write tokens (High) | §2.3 every-job `if`, the UNVERIFIED limit, trusted-job checkout note; §3 static checks; plan Task 5 |
