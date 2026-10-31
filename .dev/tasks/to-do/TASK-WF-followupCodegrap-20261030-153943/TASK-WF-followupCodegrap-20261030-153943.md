---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-followupCodegrap-20261030-153943
version: "2"
priority: Medium
created_date: "2026-10-30"
---

# codegraph upstream release monitor (follow-up to Phase 2, issue #323)

Source: ./source.md
Goal: A scheduled workflow in `IronbellyOrg/IronClaude` finds an eligible newer `colbymchenry/codegraph` release, verifies it (SHA-256 against `SHA256SUMS` plus `gh attestation verify -R colbymchenry/codegraph`), rewrites the pin in `src/superclaude/cli/install_codegraph.py`, proves it in an isolated HOME, and opens a PR on `IronbellyOrg/IronClaude` only, with the release notes; the bump logic lives in `scripts/codegraph_release.py` with offline unit tests.

## Constraints

- Run the source §0 "Execution setup" block before `/sc:implement`: it creates `ironbelly/feat-codegraph-release-monitor` from `origin/master` in the worktree `.dev/worktrees/codegraph-release-monitor-impl` and cherry-picks the `docs(plan): codegraph release monitor (#323)` commit. No task switches branches. PR #329 is merged (`2f10a0e1`).
- PRs only on `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`); never a bare `gh pr create`, in the workflow or the script; never push to `upstream` (source §6).
- Never stage a `.claude/` path; `.dev/tasks` is always staged with `git add .dev/tasks`, the package and its `artifacts/` included; stage `.dev/codegraph-migration/decisions/MX-*` when a decision was taken; feature branch only.
- Every block that uses `PKG` starts with `PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"`; task evidence goes under `"$PKG/artifacts/"`, never the project-root `artifacts/` folder.
- Never run `superclaude install`, `claude mcp add/remove`, `./update.sh` or `codegraph install` without `--print-config` against the real HOME; every live proof uses the sandbox of source §2.5.
- Never edit historical `.dev/` artifacts (`.dev/codegraph-migration/evidence/P2-*`); never run `tests/cli/eval/`; after a full-suite run restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with `git checkout --`.
- `scripts/codegraph_release.py` imports only modules in `sys.stdlib_module_names`; values from the `superclaude` package come through the child `sys.executable -c` of source §2.2 `package_values`. No new dependency.
- The workflow never merges, approves or auto-merges a PR, never pushes to `master`, never pushes or force-pushes an existing branch, and keeps every GitHub side effect except `git push` in the script's `apply` subcommand (source §2.2-§2.4).
- Every acceptance command runs from the worktree root under `bash -euo pipefail`, one condition per line, negative checks as `if cmd; then exit 1; fi`; every `uv run pytest` uses `-p no:cacheprovider` (source §0 "Evidence rule").
- Run `git status --short` after each task; a modified tracked file the task did not intend to change is a defect to fix before committing.
- After each task's commit, post the source §5 progress comment on issue #323 with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file <file>`, and nowhere else.
- Decisions follow source §6 (simple: self; mid: `/sc:adversarial --compare ... --depth quick`; complex: `/sc:adversarial --compare ...`), logged in `.dev/codegraph-migration/decisions/MX-log.md`.

## Phase 1: Baseline and a single-source pin

## Task 1: Verify the execution setup and record the test baseline

Implements source §0 "Execution setup" (check only) and §4 T0. Run:

```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"; mkdir -p "$PKG/artifacts"
grep -n '^VERSION = ' src/superclaude/cli/install_codegraph.py
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > "$PKG/artifacts/baseline-failures.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
```

A pin other than `1.6.2` is fine (only Task 2's literal lists change). If the branch or base checks below fail, the setup block was skipped: stop as blocked and report it on issue #323.

Acceptance criteria:
- `test "$(git branch --show-current)" = ironbelly/feat-codegraph-release-monitor` exits 0.
- `git merge-base --is-ancestor 2f10a0e1e43bee841a4143235a92fc16171c9707 HEAD` exits 0 (#329 is in the base).
- `test -f .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md` exits 0.
- `test -f "$PKG/artifacts/baseline-failures.txt"` exits 0 (the file may be empty when the suite is green).
- `test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"` exits 0.
- Committed as `chore(tasks): record the test baseline for the codegraph release monitor (#323)` with `.dev/tasks` staged.

## Task 2: Make the codegraph pin a one-file change in tests and docs

Depends on: Task 1

Implements source §1 rows F1-F5, fact 3 and §4 T1. Files: `tests/cli/fixtures/codegraph-SHA256SUMS.txt` (new), `tests/cli/test_install_codegraph.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py`, `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`. Locate every site by its literal, not its line number (lines below are from `e62ed152`).

- Copy `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` (header plus four tarball lines) to `tests/cli/fixtures/codegraph-SHA256SUMS.txt` and point `test_u2_pin_integrity` at the fixture; leave the `.dev/` file unchanged.
- Replace each `1.6.2` / `v1.6.2` literal in `tests/cli/test_install_codegraph.py` (38, 45, 96, 151, 171, 175, 237, 270, 639, 640, 659, 691) with `cg.VERSION` / `cg.TAG`; replace the bump helper's `version="1.6.3"` (306) and `"v1.6.3"` (320) with the next patch of `cg.VERSION` via a small `_next_patch` helper.
- In `tests/unit/test_cli_doctor.py` add `from superclaude.cli import install_codegraph` and derive `_stub`'s default (241) and `"the pin is 1.6.2"` (287) from it; in `tests/cli/test_update_command.py` derive `"codegraph MCP (pinned v1.6.2; user scope):"` (355) from `install_codegraph.TAG`.
- Add `test_no_pinned_version_literals_in_tests` to `tests/cli/test_install_codegraph.py`: it scans the three test files for any `\d+\.\d+\.\d+` literal equal to or above `cg.VERSION`, building its pattern from `cg.VERSION` so it holds no literal itself.
- In the two docs files replace the literal version (`mcp-installation.md` 9, 28, 31; `mcp-server-guide.md` 29, 43) with "the pinned version", how to read it (`superclaude install --list` prints `codegraph MCP (pinned vX.Y.Z; user scope)`), and that `src/superclaude/cli/install_codegraph.py:26-27` is the source.
- Do not edit `src/superclaude/cli/install_codegraph.py`.

After committing, run the mutation check and keep its output:

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

Acceptance criteria:
- `cmp <(tail -n +2 .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt) <(tail -n +2 tests/cli/fixtures/codegraph-SHA256SUMS.txt)` exits 0.
- `uv run pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py` passes.
- `if git grep -n -E '1\.6\.[23]' -- tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md; then exit 1; fi` exits 0.
- `grep -q 'install_codegraph.py' docs/user-guide/mcp-installation.md` exits 0.
- `uv run ruff check tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py` and `uv run ruff format --check` on the same files pass.
- `git diff --quiet -- src/superclaude/cli/install_codegraph.py .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` exits 0.
- Committed as `test(codegraph): derive the pinned version from install_codegraph in tests and docs`; the mutation block above exits 0 for all three versions and `"$PKG/artifacts/t1-mutation.log"` holds three pytest summaries (`test "$(grep -c ' passed' "$PKG/artifacts/t1-mutation.log")" -ge 3`); if it fails, fix the missed literal and amend the commit.

## Phase 2: Offline-tested release logic

## Task 3: Add the pure bump logic in scripts/codegraph_release.py with unit tests

Depends on: Task 2

Implements source §2.2 constants and pure functions (`parse_version`, `read_pin`, `pick_candidates`, `parse_sha256sums`, `rewrite_pin`, `render_sums_fixture`, `tool_problems`, `entry_drift`, `build_body`, `gate`, `classify`, `route`, `fingerprint`), the §2.4 selection rules (two lines, `MIN_AGE_DAYS = 14`, no fallback, branch `codegraph/bump-<tag>`, gate, declined versions, supersede, deleted releases, stall warning at 28 days), the §2.5 classification and outcome tables, and the §2.6 body rules. Reads: `src/superclaude/cli/install_codegraph.py` (`VERSION`, `TAG`, `SHA256`, `MCP_TOOLS` at 26-35; input of `read_pin`/`rewrite_pin`) and `src/superclaude/cli/install_mcp.py` (`_codegraph_entry` at 862-874, the shape `entry_drift` compares).

Files: `scripts/codegraph_release.py` (new, stdlib only, not packaged), `tests/cli/test_codegraph_release.py` (new; loads the script with `importlib.util.spec_from_file_location`, precedent `tests/skills/test_workflow_archive.py:26-28`), `tests/cli/fixtures/codegraph_release/releases.json`, `tests/cli/fixtures/codegraph_release/SHA256SUMS`, `tests/cli/fixtures/codegraph_release/print-config-claude.txt`. Build `releases.json` with `gh api 'repos/colbymchenry/codegraph/releases?per_page=8' --jq '[.[] | {tag_name, published_at, draft, prerelease, html_url, body: (.body[:2000]), assets: [.assets[] | {name, size}]}]'` plus hand-added synthetic entries documented in a `_comment` key; `SHA256SUMS` with `gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS`; `print-config-claude.txt` from `src/installer/targets/claude.ts:241-245` upstream (replaced by real output in Task 4). Tests: source §3 R1-R11, R17-R19 and the pure parts of R20 (gate decisions, `--slurp` flattening), including R4's boundary ages, no-fallback, backport, re-created release, pending major plus eligible minor, and the replay with `now` at 06:23:00Z (bumps on 08-04 to v1.5.0, 09-09 to v1.6.0, 10-17 to v1.6.2); R6 finds `ruff` with `shutil.which` and skips with a reason when absent.

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py` passes, and `uv run pytest -p no:cacheprovider -q --collect-only tests/cli/test_codegraph_release.py` lists a test for each of R1-R11 and R17-R20 (one function or parametrized case per listed case; test names carry the R id).
- `uv run ruff check scripts/codegraph_release.py tests/cli/test_codegraph_release.py` and `uv run ruff format --check scripts/codegraph_release.py tests/cli/test_codegraph_release.py` pass.
- The import check exits 0: `uv run python -c 'import ast,sys; t=ast.parse(open("scripts/codegraph_release.py").read()); m={(a.name if isinstance(n,ast.Import) else n.module).split(".")[0] for n in ast.walk(t) if isinstance(n,(ast.Import,ast.ImportFrom)) and not getattr(n,"level",0) for a in (n.names if isinstance(n,ast.Import) else [n])}; bad=sorted(x for x in m if x not in sys.stdlib_module_names and x!="__future__"); print(bad); sys.exit(1 if bad else 0)'`.
- Test R6 shows `rewrite_pin` on the real `install_codegraph.py` changes exactly five lines and its output passes `ruff format --check -`.
- Committed as `feat(codegraph): add offline-tested release bump logic`.

## Task 4: Add the I/O subcommands, the stdio MCP client and the live harness proof

Depends on: Task 3

Implements source §2.2 I/O wrappers (`_gh`, `_run` in its own process group, `package_values` through `sys.executable -c`, `mcp_tool_names`) and the subcommands `check` (with gate fields, `--tag`, `--dry-run`, `--min-age-days` exit 1 on bad input), `fetch` (length, sums, hash, attestation on 5 files, one retry, `--github-output`), `bump`, `prove` (the five §2.5 stages, sandbox `HOME=<root>/home`, `PATH=<root>/home/.local/bin:/usr/bin:/bin`, isolation asserts, process-group kill, first 200 lines of output per step in the log, `root=`/`home=`/`asset=` outputs), `body`, `route` and `apply` (every `gh` call with `--repo "$GITHUB_REPOSITORY"`, any other repository refused, label failures logged, `--dry-run`). Reads: `src/superclaude/cli/install_codegraph.py` (`acquire` at 271-365, `Runner` at 42-43), `src/superclaude/cli/install_mcp.py` (`_codegraph_entry` at 862-874, read through `package_values`), `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (the stdio protocol to port). Files: `scripts/codegraph_release.py`, `tests/cli/test_codegraph_release.py`, `tests/cli/fixtures/codegraph_release/fake_mcp_server.py` (new), `tests/cli/fixtures/codegraph_release/print-config-claude.txt` (real output). Tests: source §3 R12-R16, R20 (I/O parts), R21, R22. Then run the live proof on the current pin (network on, sandbox HOME):

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
test "$(jq -S '.mcpServers' "$HOME/.claude.json" | sha256sum | cut -d' ' -f1)" = "$REAL_SUM"
```

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py` passes, including R12-R16 and R20-R22.
- `uv run ruff check` and `uv run ruff format --check` on `scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py` pass, and Task 3's import check still exits 0.
- `grep -q '^result=none$' "$PKG/artifacts/live-check.out"`, `grep -q '^result=ok$' "$PKG/artifacts/live-fetch.out"` and `grep -q '^result=pass$' "$PKG/artifacts/live-prove.out"` each exit 0.
- `for s in install version index tools drift; do grep -q "$s" "$PKG/artifacts/live-prove.log"; done` exits 0.
- `grep -q '"mcpServers"' tests/cli/fixtures/codegraph_release/print-config-claude.txt` exits 0 (real output from the pinned binary).
- The live block's last line (real `~/.claude.json` `.mcpServers` hash unchanged) exits 0, and `git diff --quiet -- src/superclaude/cli/install_codegraph.py` exits 0.
- Committed as `feat(codegraph): verify, prove and describe a codegraph release candidate`, with `.dev/tasks` staged.

## Phase 3: Scheduled workflow

## Task 5: Add .github/workflows/codegraph-release-monitor.yml and its static test

Depends on: Task 4

Implements source §2.1 order and every bullet of §2.3, plus the §2.5 infrastructure counter. Reads: `.github/workflows/test.yml` (the setup block to mirror at 54-65 and 141-150, `persist-credentials: false` at 144; dispatched, never edited). The workflow:

- `on`: `schedule` cron `23 6 * * *`; `workflow_dispatch` inputs `dry_run` (boolean), `tag` (string), `min_age_days` (string); the schedule passes no `min_age_days`.
- Job `check` (outputs the JSON list of legs with tag, line and gate fields) and job `bump` (matrix over `fromJSON(needs.check.outputs.legs)`, `max-parallel: 1`, `fail-fast: false`, skipped when the list is empty); a re-prove leg checks out the existing `codegraph/bump-<tag>` branch, other legs check out `master`.
- On every job: `if:` includes `github.repository == 'IronbellyOrg/IronClaude'`; `permissions` exactly `contents: write`, `pull-requests: write`, `issues: write`, `actions: write`; `runs-on: ubuntu-latest`; `timeout-minutes: 30`; concurrency group `codegraph-release-monitor` without cancel.
- Every checkout: `actions/checkout@v4` with `fetch-depth: 0` and `persist-credentials: false`; then `astral-sh/setup-uv@v10.3.2` (Python 3.10, `activate-environment: true`) and `uv pip install -e ".[dev]"`; later steps call the venv's `python` and `pytest`, never `uv run`.
- `bump` job steps in order: fetch, bump, push, tests, prove, body, route, apply. Push runs only when `fetch` wrote `result=ok`, the gate's `branch_exists` is false and `inputs.dry_run != true`; it commits as `github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>` with message `chore(deps): bump codegraph pin to <tag>` and body lines `Old:`, `New:`, `Release:`, `Verified:` (source §2.3), and pushes with the `http.https://github.com/.extraheader` command of source §2.3, never `--force`. Tests: `pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py tests/cli/test_codegraph_release.py` (failure means `stage=tests`). Route and apply run with `if: always()` once the push succeeded (or on the re-prove leg); apply runs with `--dry-run` when `inputs.dry_run` is true and also dispatches `test.yml` on the branch.
- `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` only on the check, fetch, push, route and apply steps; the tests and prove steps get no token. No `gh pr create`, `gh pr merge` or `--auto` anywhere in the YAML. A step summary is written on every path (none, skipped, pass, behaviour, integrity, infrastructure).

Files: `.github/workflows/codegraph-release-monitor.yml` (new), `tests/cli/test_codegraph_release_workflow.py` (new; `yaml.safe_load`, precedent `tests/swarm/test_merge_boundary_guards.py:38,175`) asserting every static check in the source §3 workflow paragraph.

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release_workflow.py` passes, and its test names cover each static check in source §3 (triggers and inputs, every-job `if` and exact permissions, `persist-credentials: false` on every checkout, token scope, no `SuperClaude-Org`, no `gh pr create` in YAML, `--repo` on every `gh` call the script builds, step order including the pytest step, push gating, `always()` on route/apply, no force push, dry-run gating, `max-parallel: 1`, no `gh pr merge` or `--auto`).
- `uv run python -c 'import yaml; yaml.safe_load(open(".github/workflows/codegraph-release-monitor.yml"))'` exits 0.
- `if grep -n 'SuperClaude-Org' .github/workflows/codegraph-release-monitor.yml; then exit 1; fi` and `if grep -n 'gh pr create' .github/workflows/codegraph-release-monitor.yml; then exit 1; fi` exit 0.
- `test "$(grep -c 'persist-credentials: false' .github/workflows/codegraph-release-monitor.yml)" -ge 2` exits 0.
- `uv run ruff check tests/cli/test_codegraph_release_workflow.py` and `uv run ruff format --check tests/cli/test_codegraph_release_workflow.py` pass; `actionlint` passes too if it is on PATH.
- Committed as `ci(codegraph): add the scheduled codegraph release monitor`.

## Phase 4: Documentation and delivery

## Task 6: Document the monitor in the workflows README, CHANGELOG and MCP install guide

Depends on: Task 5

Implements source §1 rows F10, F11 and the F5 paragraph, and §4 T5. Add a `codegraph-release-monitor.yml` section to `.github/workflows/README.md`; add an `## [Unreleased]` Added entry to `CHANGELOG.md` (do not edit the historical v1.6.2 line); add a "How the pin is updated" paragraph to `docs/user-guide/mcp-installation.md` saying what the monitor does, that a release must be 14 days old and the newest one is picked, that a new major opens as a draft, what an integrity failure, a behaviour failure and an infrastructure failure produce (source §2.5), and how to run it by hand: `gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true`.

Acceptance criteria:
- `grep -q 'codegraph-release-monitor.yml' .github/workflows/README.md` exits 0.
- `awk '/^## \[Unreleased\]/{f=1;next} /^## \[/{f=0} f' CHANGELOG.md | grep -qi 'codegraph release monitor'` exits 0.
- `grep -q 'codegraph-release-monitor' docs/user-guide/mcp-installation.md`, `grep -q '14 days' docs/user-guide/mcp-installation.md`, `grep -qi 'draft' docs/user-guide/mcp-installation.md`, `grep -qi 'integrity' docs/user-guide/mcp-installation.md` and `grep -qF 'gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true' docs/user-guide/mcp-installation.md` each exit 0.
- `if grep -n 'SuperClaude-Org/SuperClaude_Framework/pull' docs/user-guide/mcp-installation.md .github/workflows/README.md; then exit 1; fi` exits 0.
- Committed as `docs(codegraph): document the codegraph release monitor`.

## Task 7: Run the final gate and open the PR on IronbellyOrg/IronClaude

Depends on: Task 6

Implements source §4 T6. Run:

```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > "$PKG/artifacts/final-failures.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
uv run python scripts/codegraph_release.py prove --github-output "$PKG/artifacts/final-prove.out" > "$PKG/artifacts/final-prove.log"
```

Then do the repo CLAUDE.md pre-PR checks (`git remote -v`; `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude`; `git fetch origin && git log master..origin/master`, rebasing onto `origin/master` if the fork moved), push the branch to `origin`, and open the PR in Claude Code with `/sc:pr-submit --monitor 3 --head ironbelly/feat-codegraph-release-monitor --title "feat(codegraph): scheduled codegraph release monitor (#323)" --body "<summary, test evidence, live proof log path, link to the spec>"`. Save the URL with `printf '%s\n' "<url>" > "$PKG/artifacts/pr-url.txt"`. The issue #323 comment lists the debate items flagged for the user (source `## Decisions`, last paragraph) and source §7 item 6 (Coder bake).

Acceptance criteria:
- `test -z "$(comm -13 "$PKG/artifacts/baseline-failures.txt" "$PKG/artifacts/final-failures.txt")"` exits 0 (no new failure).
- `grep -q '^result=pass$' "$PKG/artifacts/final-prove.out"` exits 0.
- `uv run ruff check src/ tests/ scripts/codegraph_release.py`, `uv run ruff format --check src/ tests/ scripts/codegraph_release.py` and `make verify-sync` pass.
- `test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"` exits 0.
- `test "$(gh repo view --json nameWithOwner -q .nameWithOwner)" = IronbellyOrg/IronClaude` exits 0.
- `grep -q '^https://github.com/IronbellyOrg/IronClaude/pull/[0-9]*$' "$PKG/artifacts/pr-url.txt"` exits 0.
- Committed as `chore(tasks): record the codegraph release monitor PR (#323)` with `.dev/tasks` staged.

## Phase 5: Post-merge live run

## Task 8: Run the merged monitor on master and record both runs

Depends on: Task 7

Implements source §4 T7. The first line is a merge gate: until a person merges the Task 7 PR (source §7 item 2) the workflow is not on `master`, so stop as blocked if the state is not `MERGED` and re-run this task after the merge. Run:

```bash
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"
test "$(gh pr view "$(cat "$PKG/artifacts/pr-url.txt")" --repo IronbellyOrg/IronClaude --json state -q .state)" = MERGED
git fetch -q origin
PIN=v$(git show origin/master:src/superclaude/cli/install_codegraph.py | sed -n 's/^VERSION = "\([0-9.]*\)"$/\1/p'); test "$PIN" != v
newest_run() {
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

If the dry run fails with a 403 on `gh attestation verify`, add `attestations: read` to the workflow permissions and to the static test in one commit, re-run Task 7's gate, and repeat this task (source §2.3 UNVERIFIED item). Post the final issue #323 comment with both run URLs.

Acceptance criteria:
- `grep -q 'result=ok' "$PKG/artifacts/post-merge-dry-run.log"` and `grep -q 'result=pass' "$PKG/artifacts/post-merge-dry-run.log"` each exit 0.
- `test -z "$(gh pr list --repo IronbellyOrg/IronClaude --head "codegraph/bump-$PIN" --state all --json number -q '.[].number')"` exits 0 (the dry run opened no PR) and `test -z "$(gh issue list --repo IronbellyOrg/IronClaude --search "codegraph $PIN in:title" --state all --json number -q '.[].number')"` exits 0 (and no issue).
- `grep -Eq 'result=(none|candidate)' "$PKG/artifacts/post-merge-normal-run.log"` exits 0, and `test "$(gh pr list --repo IronbellyOrg/IronClaude --search 'codegraph in:title' --state open --json headRefName -q '[.[].headRefName] | group_by(.) | map(length) | max // 0')" -le 1` exits 0 (at most one open PR per tag).
- `test "$(grep -c 'actions/runs/[0-9]' "$PKG/artifacts/post-merge-runs.md")" -eq 2` exits 0. No commit (source §4 T7: the feature branch is already merged); the evidence stays in the package with `.dev/tasks` staged for `/sc:implement`'s archive step.
