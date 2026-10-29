---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-phase2CodegraphI-20261029-192001
version: "1"
priority: Medium
created_date: "2026-10-29"
---

# Phase 2: install codegraph by default (issue #323)

Source: ./source.md
Goal: `superclaude install` (and so `./update.sh`) installs a pinned, checksum-verified codegraph v1.6.2, registers it at user scope with the tool list chosen by a schema-cost check, retires Serena once codegraph is ready, indexes each checkout on its first session, documents all of it, passes CI and the full-suite baseline gate, and is proven on the real workspace after merge.

## Constraints

- Planning source is `./source.md` (snapshot of `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`). Every task cites the source section it implements; details not repeated here are in that section.
- Preconditions (`./source.md` §5): branch `ironbelly/feat-codememory-codegraph-init`; Phase 1 tasks committed first (Phase 1 and Phase 2 land as one PR and one `master` merge, `./source.md` §8 and D12); `git status --short` clean apart from untracked `.dev/` content. Seams are located by function or block name, not by the `55d40308` line numbers (`./source.md` §1).
- Every acceptance command runs from the worktree root under `bash -euo pipefail` and must exit 0 if and only if its criterion passes. One condition per line: never `A && B` or `! cmd` in the middle of a block (errexit ignores both); write a negative check as `if cmd; then exit 1; fi`. Every `uv run pytest` uses `-p no:cacheprovider`. Run `git status --short` after each task; an unintended modified tracked file is a defect to fix before committing.
- Package evidence lives in this package's `artifacts/` folder (written `./artifacts/` in prose). Shell commands run from the worktree root, so they resolve it with `A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts` (the glob finds the package under `to-do/` or, after archiving, `done/`) and create it with `mkdir -p "$A"` before the first write.
- Tests are judged against the recorded baseline `.dev/codegraph-migration/evidence/P2-baseline-failures.txt` (the suite was not green at `55d40308`): no failing test id may appear outside it. After any full test run, restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with `git checkout --` before committing.
- Hard rules (`./source.md` §7): never run `claude mcp add/remove` or `superclaude install` against the real HOME (sandbox HOMEs only, each asserting the real `.mcpServers` hash is unchanged; the one exception is the read-only `superclaude install --list`); never stage or commit anything under `.claude/` except `.claude/settings.json`; feature branch only; never push to `upstream`; PRs only on `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`).
- `.dev/tasks/` is always staged (`git add .dev/tasks`) at every commit point, this package and its `artifacts/` included.
- Commit points: one conventional commit per task as named in each task, and every task group (phase) ends with a commit point followed by one issue-#323 progress comment, posted with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file /tmp/p2-progress.md` using the body template of `./source.md` §6 (group, commit sha and subject, tasks done, exact test command and its result with failures reported as failures, decisions taken, next group). Never post progress anywhere else.
- Decision rules (`./source.md` §7): simple decisions (one obvious answer, or forced by a pinned test or verified constraint) the executor makes itself; mid-level decisions (two or more viable options with real trade-offs, local to one task) are written as `.dev/codegraph-migration/decisions/P2X-<slug>/option-<x>.md` files (under 40 lines each) and settled by an agent running `/sc:adversarial --compare <files> --depth quick`; complex decisions (installer contract §2, indexing design §3, release order §8, or Phase 1/3 ownership) use `/sc:adversarial --compare <files>` at default depth. Follow the recommendation; log every decision as a row in `.dev/codegraph-migration/decisions/P2X-log.md` (decision, options, method, rationale, folder) in the commit that applies it, and name the folder in the next issue comment.
- Human intervention only for the seven items of `./source.md` §7 (gh auth failure; a `SHA256SUMS` that differs from §0; merging the PR; running `./update.sh` on the real workspace; giving the Coder handoff prompt to a Coder agent; the non-blocking Leg B item; the non-blocking removal of a kept user-scope Serena entry found by Task 16). Never stop to ask otherwise.

## Phase 1: Publish the plan and start the Coder work (group G0)

## Task 1: Record the test baseline, commit the planning files and hand off to Coder

Implements `./source.md` §5 preconditions (baseline) and T0. Record the baseline before any source change, exactly as in §5:

```bash
mkdir -p .dev/codegraph-migration/evidence
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > .dev/codegraph-migration/evidence/P2-baseline-failures.txt
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json
```

Then stage `.dev/codegraph-migration` (specs, handoff, decisions, evidence baseline) and `.dev/tasks`, commit `docs(plan): Phase 2 codegraph install spec and Coder handoff (#323)`, push with `git push origin ironbelly/feat-codememory-codegraph-init`, and post an issue-#323 comment that links `.dev/codegraph-migration/handoff/coder-handoff-prompt.md` on the branch and asks for the Coder work to start (human item 5 of `./source.md` §7).

Acceptance criteria:
- `.dev/codegraph-migration/evidence/P2-baseline-failures.txt` exists and every line matches `^(FAILED|ERROR) tests/`.
- `git ls-files --error-unmatch .dev/codegraph-migration/handoff/coder-handoff-prompt.md .dev/codegraph-migration/handoff/coder-handoff-context.md` exits 0.
- `gh api "repos/IronbellyOrg/IronClaude/contents/.dev/codegraph-migration/handoff/coder-handoff-prompt.md?ref=ironbelly/feat-codememory-codegraph-init" --jq .name` prints `coder-handoff-prompt.md`.
- The commit holds nothing under `.claude/` except `.claude/settings.json` (this block exits 0; the hard rule of `./source.md` §7):
```bash
git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt
if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi
```

## Task 2: Confirm Phase 1's spec carries the Serena gate (T0b)

Depends on: Task 1

Implements `./source.md` T0b and §9 (row `install_retired_mcp.py`). The Phase 1 finalizer (F1) is expected to have amended `.dev/codegraph-migration/specs/phase-1-removal-spec.md` already (review finding X-4). Run the T0b acceptance lines; if any fails, make the edits T0b lists in that file (DoD-3, §2.3 row, §3.2 Tier R and Tier K "env/headers absent or `{}`", §3.4 hint renamed to `serena-local`, §3.6 closing condition, the sandbox expectation "Legacy Serena registration kept", D2, each pointing at `./source.md` §2.12) and, if Phase 1 T15 wrote `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, append a "Phase 2 override: Serena removal" section quoting §2.12. Commit `docs(plan): align Phase 1 retire rules with the Phase 2 codegraph gate (#323)` only if `phase-1-removal-spec.md` or `phase2-facts-from-phase1.md` changed. State in the task completion message (and the G0 comment) whether Phase 1 already carried the amendments or this task made them (`./source.md` T0b "Reported to the coordinator"). Group G0 commit point: then post the G0 issue comment (`./source.md` §6).

Acceptance criteria:
- These all exit 0:
```bash
test "$(rg -c 'codegraph_ready' .dev/codegraph-migration/specs/phase-1-removal-spec.md)" -ge 7
rg -q 'serena-local' .dev/codegraph-migration/specs/phase-1-removal-spec.md
rg -q 'Tier R \(removed\).*absent or `\{\}`' .dev/codegraph-migration/specs/phase-1-removal-spec.md
rg -q 'Tier K \(kept.*absent or `\{\}`' .dev/codegraph-migration/specs/phase-1-removal-spec.md
test ! -e .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md || rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md
```
- The G0 comment exists on issue #323, names the commit(s) of Tasks 1-2 and says which T0b path was taken.

## Phase 2: Installer core (group G1)

## Task 3: Run the tool-list schema-cost check and choose `MCP_TOOLS` (T2 step 0)

Depends on: Task 2

Implements `./source.md` §2.4 "Tool list" and T2 "Step 0" (review findings X-1, X-25), with the method of `.dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md` §1-§7 (authoritative for every detail). Needs no repository code, so it runs before Task 4.
- First action, from the worktree root: `A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts`, `mkdir -p "$A"`, `A=$(realpath "$A")` (absolute, so it survives `cd` into `$W`), and `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`.
- Save the stdio client given verbatim in `./source.md` T2 step 0 as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs`.
- Leg A (always): private `mktemp -d` dir with sandbox `HOME`/`CLAUDE_CONFIG_DIR` and telemetry off; download the pinned v1.6.2 tarball for this platform, verify its SHA-256 against `./source.md` §0 before extracting (mismatch: stop, human item 2), extract, `git init -q` a tiny repo, run the client twice from it (run 1 with `CODEGRAPH_MCP_TOOLS` unset, run 2 with `node,search,callers,callees,impact,files,status`), writing the outputs straight to `"$A/t3-run1.json"` and `"$A/t3-run2.json"` (absolute, so they survive `rm -rf "$W"`), and compute `D` and the recorded data fields.
- X-25 hard stop: run 2 lists exactly the seven `codegraph_*` tools (no `codegraph_explore`) and its `explore_call_error` is `true`; otherwise stop, write no value, log a mid-level decision.
- Bands: `D <= 6000` bytes gives the seven tools; `D > 8000` gives `status`; in between, Leg B (four headless `claude -p` runs with `--strict-mcp-config`, ABAB order, `.mcpServers` hash guard, validity guards a-d of the merged method §5) decides; Leg B not run or invalid gives `status` and the non-blocking human item 6 of `./source.md` §7.
- If the value is `status`, apply the §2.4 failure branch: every literal seven-tool value in `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`, its §3.4 first sentence, and both Coder handoff files under `.dev/codegraph-migration/handoff/` is replaced in the same commit as Task 4.
- Write `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` with the 16 one-fact lines of the merged method §7, ending `Selected MCP_TOOLS: <value>`.

Acceptance criteria:
- This block exits 0:
```bash
node --check .dev/codegraph-migration/evidence/p2-mcp-tools.mjs
test "$(wc -l < .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md)" -eq 16
tail -1 .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md | rg -q '^Selected MCP_TOOLS: (node,search,callers,callees,impact,files,status|status)$'
rg -qx 'Explore hidden: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
rg -qx 'Explore call blocked: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts
jq -e '(.tools | map(.name) | index("codegraph_explore")) == null and .explore_call_error == true' "$A/t3-run2.json"
test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"
```

## Task 4: Add the pinned, checksum-verified acquisition module (T1)

Depends on: Task 3

Implements `./source.md` T1, F1, §2.2 (discovery, pointer file `~/.codegraph/.superclaude-bin`), §2.3 (acquisition, platforms, tar member checks, receipt-first rename and links), §2.6 (receipt, pruning), §2.11 module shape, and tests U1-U10, U20-U22 and U24 of §4.1 (U11 belongs to Task 5, which creates the phase function it tests). Create `src/superclaude/cli/install_codegraph.py` (standard library only) with `VERSION = "1.6.2"`, `TAG`, the four-asset `SHA256` table and `MCP_TOOLS` set to the `Selected MCP_TOOLS:` value from Task 3's evidence file, and `tests/cli/test_install_codegraph.py` (download faked through `install_codegraph._download`, fixture tarball built in `tmp_path`; U2 asserts `MCP_TOOLS` equals the evidence value and contains no `explore`). First re-check the pin with the `gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS -D /tmp/p2-sums --clobber` and `diff` command of `./source.md` T1 (any difference: stop, human item 2). Commit `feat(install): add pinned, checksum-verified codegraph acquisition` together with Task 3's client, evidence file and `./artifacts/t3-run*.json`.

Acceptance criteria:
- The T1 pin check prints nothing and exits 0.
- `uv run pytest tests/cli/test_install_codegraph.py -q -p no:cacheprovider` passes with U1-U10, U20-U22 and U24 present.
- `uv run ruff check src/superclaude/cli/install_codegraph.py tests/cli/test_install_codegraph.py` exits 0.
- `test "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')" = "$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md)"` exits 0.

## Task 5: Register codegraph at user scope with exact-entry repair (T2 steps 1-2)

Depends on: Task 4

Implements `./source.md` T2 steps 1-2, F2 (a)-(e), §2.4 (registration JSON with `CODEGRAPH_MCP_TOOLS` from `MCP_TOOLS`, `claude --version` checked before discovery and acquisition, entry table: absent / equal / owned / user-managed, bounded argv runner with `start_new_session=True`, 10 s and 60 s timeouts), §2.11, and tests U11-U19, U23, U25 plus the registry and dispatch tests of §4.1, in `src/superclaude/cli/install_mcp.py`, `tests/cli/test_install_codegraph.py` and `tests/cli/test_install_mcp_registry.py`. Step 1 is the sandbox `add-json` shape probe of `./source.md` T2 (writes `.dev/codegraph-migration/evidence/P2-add-json-shape.json`); if `claude mcp add-json` exits non-zero there, stop and take a mid-level decision. Step 2 finds the helpers with the `rg` command of T2 and adds a `name` parameter or re-creates missing ones from `git show 55d40308:src/superclaude/cli/install_mcp.py`. Commit `feat(mcp): register codegraph at user scope with exact-entry repair`. Group G1 commit point: then post the G1 issue comment.

Acceptance criteria:
- The step-1 probe leaves the real `.mcpServers` hash unchanged, and this block exits 0 (or the shape difference is logged as a decision and the matcher follows the stored shape):
```bash
MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT"
E=$(jq -cn --arg t "$MT" '{"type":"stdio","command":"/opt/x/bin/codegraph","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":$t}}')
jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json
```
- `uv run pytest tests/cli/test_install_codegraph.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/recommend -q -p no:cacheprovider` passes.
- `uv run pytest tests/cli/test_install_mcp_registry.py -q -p no:cacheprovider -k codegraph` selects and passes the registry-contract and dispatch tests (not "0 selected").
- U11 asserts a failing `claude --version` fails the phase before discovery or download; U12 asserts the add-json JSON carries `env.CODEGRAPH_MCP_TOOLS == install_codegraph.MCP_TOOLS`; U14 replaces an owned entry whose env lacks that key.
- `jq -e 'type == "object"' .dev/codegraph-migration/evidence/P2-add-json-shape.json` exits 0.
- The G1 comment exists on issue #323.

## Phase 3: CLI wiring and Serena retirement (group G2)

## Task 6: Make codegraph a required `superclaude install` phase with a `--list` block (T3)

Depends on: Task 5

Implements `./source.md` T3, F3, §2.1 (phase placed after `install_user_setup`, before Phase 1's retire step; failure keeps framework work and exits 1; `--force` not forwarded), §2.8 (`--list` block, read-only), and the `tests/cli/test_update_command.py` additions of §4.1, in `src/superclaude/cli/main.py` and `tests/cli/test_update_command.py`. The §2.8 `Ready for Serena retirement` line needs `codegraph_ready()`, which Task 7 creates, so this task prints the other three lines and Task 7 adds the fourth. Commit `feat(install): make codegraph a required user-level install phase`.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes.
- `uv run superclaude install --help` output contains `codegraph`.
- A test shows `install --list` prints the codegraph block (Executable, Owner, User registration) and calls neither `_download` nor `claude mcp`.

## Task 7: Retire Serena registrations once codegraph is ready (T3b)

Depends on: Task 6

Implements `./source.md` T3b, F18 and §2.12: `codegraph_ready()` in `src/superclaude/cli/install_mcp.py`, the gate passed from `src/superclaude/cli/main.py` into `src/superclaude/cli/install_retired_mcp.py` (removal by launcher shape under any name except `serena-local`, `env`/`headers` absent or `{}`, kind-B `~/.local/bin/codebase-memory-mcp` registration, printed argv and `uninstall -y` command), the `Ready for Serena retirement` line of the §2.8 `--list` block, with the test matrix of T3b in Phase 1's retire-step test file and `tests/cli/test_update_command.py`. Commit `feat(install): retire Serena registrations once codegraph is ready (#323)`.

Acceptance criteria:
- This block exits 0 (the assignment aborts under `-e` when no retire-step test file exists, so the gate can never run without it):
```bash
F=$(rg -l -g '*.py' install_retired_mcp tests)
test -n "$F"
uv run pytest $F tests/cli/test_update_command.py tests/cli/test_install_codegraph.py -q -p no:cacheprovider
uv run pytest $F -q -p no:cacheprovider -k "codegraph and serena"
test ! -e .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md || rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md
```
- Tests prove: codegraph failed keeps the current-pin Serena entry and exits 1; ready removes `serena` and a non-`serena` `start-mcp-server` launcher with `"env":{}`; non-empty `env`/`headers` are kept; `serena-local` is never removed; a second run is a no-op; Tier R and `/usr/local/bin/codebase-memory-mcp` removal stay unconditional; `install` and `install --list` read the same `codegraph_ready()` and `--list` prints `Ready for Serena retirement: yes | no (<reason>)`.

## Task 8: Report codegraph registration health in doctor (T4)

Depends on: Task 7

Implements `./source.md` T4, F4 and §2.7: `_check_codegraph()` in `src/superclaude/cli/doctor.py` (fails only on a dangling registered command; detail lines for missing entry, version drift, `codegraph prompt-hook`, `<!-- CODEGRAPH_START -->` block, unreadable `~/.claude.json`; always `Ready for Serena retirement: yes | no (<reason>)` from the same `codegraph_ready()`), tested in `tests/unit/test_cli_doctor.py`. Commit `feat(doctor): report codegraph registration health`. Group G2 commit point: then post the G2 issue comment.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_update_command.py -q -p no:cacheprovider` passes.
- A test patches `codegraph_ready()` once and asserts both `install` and doctor report its value.
- The G2 comment exists on issue #323.

## Phase 4: Indexing hook (group G3)

## Task 9: Index each checkout on its first session with a SessionStart hook (T5)

Depends on: Task 8

Implements `./source.md` T5, F7, F17 and §3.2 (POSIX `sh`, always exit 0, silent; opt-out `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`; binary from `~/.codegraph/.superclaude-bin` else `command -v codegraph`; git top-level not `$HOME` or `/`; only when `<top>/.codegraph/codegraph.db` is absent; detached `nohup … init --yes "$top"`), with every hook test listed in §3.2. Files: `src/superclaude/hooks/scripts/codegraph-session-start.sh` (new, executable), `src/superclaude/hooks/hooks.json` (SessionStart, matcher `startup`, timeout 5), `plugins/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/scripts/codegraph-session-start.sh` (copy), `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS`), `tests/cli/test_codegraph_session_start_hook.py` (new), `tests/cli/test_install_hooks.py`, `tests/unit/test_cli_install.py`. Commit `feat(hooks): index each checkout with codegraph on its first session`. Group G3 commit point: then post the G3 issue comment.

Acceptance criteria:
- This block exits 0 (review finding X-11: `tests/cli/test_verify_sync_hooks.py` fails 3 tests at `55d40308`, so it is judged only by the baseline diff):
```bash
uv run pytest tests/cli/test_codegraph_session_start_hook.py tests/cli/test_install_hooks.py tests/unit/test_cli_install.py -q -p no:cacheprovider
sh -n src/superclaude/hooks/scripts/codegraph-session-start.sh
cmp src/superclaude/hooks/scripts/codegraph-session-start.sh plugins/superclaude/hooks/scripts/codegraph-session-start.sh
make sync-dev
make verify-sync
test -f .dev/codegraph-migration/evidence/P2-baseline-failures.txt
uv run pytest tests/cli/test_verify_sync_hooks.py -q -p no:cacheprovider -rfE --tb=no > /tmp/p2-t5-vsh.txt 2>&1 || true
grep -E '[0-9]+ passed' /tmp/p2-t5-vsh.txt >/dev/null
if grep -E 'INTERNALERROR|no tests ran' /tmp/p2-t5-vsh.txt; then exit 1; fi
{ grep -E '^(FAILED|ERROR) ' /tmp/p2-t5-vsh.txt || true; } | sed 's/ - .*//' | sort > /tmp/p2-t5-vsh-fail.txt
comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt /tmp/p2-t5-vsh-fail.txt > /tmp/p2-t5-new.txt
test ! -s /tmp/p2-t5-new.txt
```
- The hook test proves the hook returns in under 1 s while the stub `codegraph` sleeps 10 s, and that stdout is always empty.
- The G3 comment exists on issue #323.

## Phase 5: Guidance, docs, CI and sandbox proof (group G4)

## Task 10: Add the codegraph MCP row and marker-delimited guidance block (T6)

Depends on: Task 9

Implements `./source.md` T6, F6 and §3.4 in `src/superclaude/core/CLAUDE.md`: one MCP table row `| codegraph      | Code graph: symbols, callers, impact, file outlines | (auto) |` (keep the `| Flag (advisory) |` header pinned by `tests/core/test_claude_md_routing_block.py`), and the §3.4 guidance block between lines `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` and `<!-- SUPERCLAUDE_CODEGRAPH_END -->`, using the seven-tool first sentence or the `status`-only sentence according to `MCP_TOOLS` (review findings X-2, X-9). Do not edit the Serena row or the "Symbolic queries" refresh row (Phases 1 and 3). Commit `docs(core): add codegraph MCP row and usage rule`.

Acceptance criteria:
- This block exits 0:
```bash
uv run pytest tests/core -q -p no:cacheprovider
test "$(rg -c '^\| codegraph ' src/superclaude/core/CLAUDE.md)" -eq 1
test "$(rg -c -x '<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->' src/superclaude/core/CLAUDE.md)" -eq 1
test "$(rg -c -x '<!-- SUPERCLAUDE_CODEGRAPH_END -->' src/superclaude/core/CLAUDE.md)" -eq 1
sed -n '/^<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->$/,/^<!-- SUPERCLAUDE_CODEGRAPH_END -->$/p' src/superclaude/core/CLAUDE.md | rg -q 'codegraph_status'
if rg -n 'codegraph_explore|CODEGRAPH_START' src/superclaude/core/CLAUDE.md; then exit 1; fi
```

## Task 11: Document the default codegraph install, indexing and removal (T7)

Depends on: Task 10

Implements `./source.md` T7, F8-F11 and F19 in `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `README.md`, `CHANGELOG.md` and `.gitignore` (`.codegraph/`): §2.6 removal commands, §2.10 failure table (short form), the registered tool list `CODEGRAPH_MCP_TOOLS` and why `codegraph_explore` is hidden (§2.4), §3.3 costs and the exact scope of `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (hook only; every switch uses the `SUPERCLAUDE_CODEGRAPH_` prefix, review X-14), the opt-in `post-checkout` recipe, the `core.excludesFile` tip, and §2.12 (Serena removed once codegraph is ready, `serena-local`, what is kept by policy, the escalated residuals). Commit `docs(mcp): document default codegraph install, indexing and removal`.

Acceptance criteria:
- This block exits 0:
```bash
uv run pytest tests/docs -q -p no:cacheprovider
for f in README.md docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md CHANGELOG.md; do rg -q codegraph "$f" || { echo "missing: $f"; exit 1; }; done
rg -q 'SUPERCLAUDE_CODEGRAPH_AUTOINIT=0' docs/user-guide/mcp-installation.md
rg -q 'claude mcp remove codegraph --scope user' docs/user-guide/mcp-installation.md
rg -q 'serena-local' docs/user-guide/mcp-installation.md
rg -q 'serena-local' CHANGELOG.md
rg -q 'CODEGRAPH_MCP_TOOLS' docs/user-guide/mcp-installation.md
rg -qx '\.codegraph/' .gitignore
if rg 'Legacy Serena registration kept' CHANGELOG.md | rg -v 'codegraph'; then exit 1; fi
```

## Task 12: Keep the Claude CLI in the CI doctor job (T8)

Depends on: Task 11

Implements `./source.md` T8, F12 and D29 in `.github/workflows/test.yml` (`doctor-check` job): run `rg -n 'name: Install Claude CLI' .github/workflows/test.yml`; if the step exists (Phase 1 kept it, review X-15), only make its comment and the `permissions` comment name codegraph; if Phase 1 deleted it, re-add it from `git show 55d40308:.github/workflows/test.yml` (lines 155-159, `npm install -g @anthropic-ai/claude-code@2.1.286`) before `Install native components`, with comments naming codegraph. Commit `ci: keep Claude CLI for the required codegraph install phase`.

Acceptance criteria:
- `uv run python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; print(s); sys.exit(0 if "Install Claude CLI" in s else 1)'` exits 0 (pyyaml is a project dependency, so the project environment is used).
- `rg -n 'codegraph' .github/workflows/test.yml` shows the rewritten comments.

## Task 13: Record the isolated-HOME install, index and tool-list proof (T9)

Depends on: Task 12

Implements `./source.md` T9 and §4.2 (layer 2, steps 1-8 including 5b): save the §4.2 script as `.dev/codegraph-migration/evidence/p2-layer2.sh`, run it (needs network to GitHub, a working `claude`, `uv sync` once beforehand, and Tasks 4-9 committed because it clones the worktree), and keep its output `.dev/codegraph-migration/evidence/P2-layer2.md`. If step 5's `claude mcp get` cannot run in the sandbox, apply the §4.2 Notes fallback (stdio `initialize` + `tools/list`, asserting `serverInfo.name == "codegraph"`) and record that in `P2-layer2.md`. If a real Claude Code session can be started in a fresh clone, record whether the hook's background `init` survives the hook and the session's end (`pgrep -f 'codegraph\.js init'`); otherwise record "process-group survival inside Claude Code: UNVERIFIED". Commit `test(codegraph): record isolated-HOME install and index evidence`. Group G4 commit point: then post the G4 issue comment including the T9 outputs.

Acceptance criteria:
- This block exits 0:
```bash
bash -n .dev/codegraph-migration/evidence/p2-layer2.sh
bash .dev/codegraph-migration/evidence/p2-layer2.sh
test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK
```
- The script's assertions cover: verified download and registration including `env.CODEGRAPH_MCP_TOOLS`, idempotency with a dead proxy, offline reuse, real index and query, MCP connection, step 5b tool list equal to `MCP_TOOLS` with `codegraph_explore` absent and its call failing, Serena and kind-B retirement, real hook init, codegraph-unavailable case keeping Serena, real HOME unchanged.
- The G4 comment exists on issue #323.

## Phase 6: Full gate and PR (group G5)

## Task 14: Run the full verification gate and fix what it finds (T10)

Depends on: Task 13

Implements `./source.md` T10: the final full verification of the branch before the PR. Fix any defect the gate finds in this phase's files only (commit `fix(codegraph): <what the gate found>` when a fix was needed). The block copies the run output and the new-failure list into `./artifacts/` before the gating line, so the evidence exists even when the gate fails; always commit that evidence afterwards (`test(codegraph): record final gate evidence`), so Task 15's rebase starts from a clean tree.

Acceptance criteria:
- This block exits 0:
```bash
A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts
mkdir -p "$A"
make sync-dev
test -f .dev/codegraph-migration/evidence/P2-baseline-failures.txt
uv run pytest -p no:cacheprovider -q -rfE --tb=no tests > /tmp/p2-final-run.txt 2>&1 || true
cp /tmp/p2-final-run.txt "$A/t14-final-run.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json
grep -E '[0-9]+ passed' /tmp/p2-final-run.txt >/dev/null
if grep -E 'INTERNALERROR|Interrupted|no tests ran' /tmp/p2-final-run.txt; then exit 1; fi
{ grep -E '^(FAILED|ERROR) ' /tmp/p2-final-run.txt || true; } | sed 's/ - .*//' | sort > /tmp/p2-final-failures.txt
comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt /tmp/p2-final-failures.txt > /tmp/p2-new-failures.txt
cp /tmp/p2-new-failures.txt "$A/t14-new-failures.txt"
test ! -s /tmp/p2-new-failures.txt
make lint
make verify-sync
```
- `git status --short` shows no unintended tracked change, and nothing under `.claude/` except `.claude/settings.json` is staged.
- `./artifacts/t14-final-run.txt` and `./artifacts/t14-new-failures.txt` are committed; the latter is empty.

## Task 15: Open or update the shared Phase 1 + Phase 2 PR on the fork (T11)

Depends on: Task 14

Implements `./source.md` T11 and §8. After the project `CLAUDE.md` pre-PR checks (`git remote -v` shows origin `IronbellyOrg/IronClaude`; `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude`; rebase onto `origin/master` if it moved), run `/sc:pr-submit --monitor 3 --head ironbelly/feat-codememory-codegraph-init --title "feat: replace codebase-memory and Serena with codegraph (#323)" --body "<Phase 1 + Phase 2 summary; links to both specs>"`; if the Phase 1 executor already opened the PR, push to it instead. Do not merge (human item 3). Commit point: none for this task (PR only). Group G5 commit point: then post the G5 issue comment with the PR URL and the Coder ordering status, plus the merge-gate output below.

Acceptance criteria:
- `gh pr view ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude --json url -q .url` prints a URL starting `https://github.com/IronbellyOrg/IronClaude/pull/`.
- `gh pr checks ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude` shows every check passing, including `doctor-check`.
- The three merge-gate commands of `./source.md` T11 (Coder `Dockerfile.coder` has the pinned linux-x64 hash; test-57 asserts a codegraph registration; the bundle `install.sh` no longer sets `SERENA_PIN` or `uv tool install`s `serena-agent`) are run and their output is in the G5 comment; the comment says "do not merge" unless all three print.

## Phase 7: Post-merge live verification (group G6)

## Task 16: Prove "completely absent" on the real workspace after merge (T12)

Depends on: Task 15

Implements `./source.md` T12 and §2.12 (review finding X-5). Trigger: the human merged the PR and ran `./update.sh` on this workspace, then restarted every Claude session (human items 3 and 4). In a new session, from the worktree root, run the read-only checks below (no `claude mcp add/remove`, no `superclaude install` other than `--list`), and confirm from the session's own tool list that `mcp__codegraph__codegraph_callers` (or, in the `status`-only branch, `mcp__codegraph__codegraph_status`) is listed and `mcp__codegraph__codegraph_explore` is not. Nothing is written in the repository (`./source.md` T12 "Files: none"): outputs go to `/tmp/p2-t16-*` and into the G6 comment. Commit point: none in the repository (post-merge); group G6 commit point is the final issue-#323 comment with every command, its output, the printed removal commands, the tool-list observation, the PR URL and the Coder ordering status.

Acceptance criteria:
- This block exits 0 only when user scope is clean and codegraph is healthy; it records both scope results first, so every later check still runs and reports:
```bash
rc=0; jq -e '(.mcpServers // {}) | (has("serena") or has("codebase-memory-mcp") or (to_entries | map(select(.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | length > 0)) | not' ~/.claude.json || rc=$?
echo "$rc" > /tmp/p2-t16-us.rc; test "$rc" -le 1
rc=0; jq -e '[(.projects // {}) | .[] | (.mcpServers // {}) | has("serena") or has("codebase-memory-mcp")] | any | not' ~/.claude.json || rc=$?
echo "$rc" > /tmp/p2-t16-ls.rc; test "$rc" -le 1
jq -r '(.mcpServers // {}) | to_entries[] | select(.key == "serena" or .key == "codebase-memory-mcp" or (.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | "claude mcp remove \(.key) --scope user"' ~/.claude.json > /tmp/p2-t16-user-cmds.txt
jq -r '(.projects // {}) | to_entries[] | .key as $p | (.value.mcpServers // {}) | keys[] | select(. == "serena" or . == "codebase-memory-mcp") | "cd \($p) && claude mcp remove \(.) --scope local"' ~/.claude.json > /tmp/p2-t16-local-cmds.txt
MT=$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')
jq -e --arg t "$MT" '.mcpServers.codegraph | .args == ["serve","--mcp"] and .env.CODEGRAPH_MCP_TOOLS == $t and .env.CODEGRAPH_TELEMETRY == "0"' ~/.claude.json
test "$("$(jq -r '.mcpServers.codegraph.command' ~/.claude.json)" --version)" = 1.6.2
claude mcp get codegraph > /tmp/p2-t12-get.txt 2>&1 || true
grep -i 'connected' /tmp/p2-t12-get.txt >/dev/null
if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi
superclaude install --list > /tmp/p2-t12-list.txt
grep -F 'Ready for Serena retirement: yes' /tmp/p2-t12-list.txt >/dev/null
superclaude doctor
test "$(cat /tmp/p2-t16-us.rc)" -eq 0
```
- A local-scope hit (`/tmp/p2-t16-ls.rc` is 1) is not a plan failure (`./source.md` §2.12): the G6 comment lists `/tmp/p2-t16-local-cmds.txt` for the user.
- A user-scope hit (`/tmp/p2-t16-us.rc` is 1, an entry the retire step kept) keeps Task 16 open: the G6 comment lists `/tmp/p2-t16-user-cmds.txt` for the user (non-blocking human item 7), and the block is re-run after the user acts.
- The G6 comment on issue #323 contains the outputs of every line above and the tool-list observation.
