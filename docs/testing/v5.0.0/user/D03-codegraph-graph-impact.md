# E2E Test Guide — `Codegraph: auto-index hook, /sc:graph and /sc:impact` (`5.0.0`)

- **Capability:** each new git checkout gets a code-graph index from a session-start hook; `/sc:graph` reports whether the index is ready and, only when you type `/sc:graph init`, builds it; `/sc:impact` lists what depends on named symbols or on a diff and never stops, falling back to Grep when the graph is not usable. Two switches turn parts of this off: `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (the hook only) and `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` (codegraph use in commands, skills and agents only).
- **Audience:** end user
- **Source of truth:** `src/superclaude/hooks/scripts/codegraph-session-start.sh:11-31` and its registration `src/superclaude/hooks/hooks.json:24-31`; `src/superclaude/commands/graph.md:9-53` with `src/superclaude/skills/sc-graph-protocol/SKILL.md:21-151`; `src/superclaude/commands/impact.md:13-63` with `src/superclaude/skills/sc-impact-protocol/SKILL.md:19-178`; the shared rules `src/superclaude/core/CODEGRAPH.md:7-37`; `CHANGELOG.md:84-93`
- **Est. time:** `Tier A: 2 minutes. Tier B: 3 minutes. Tier C: 15-25 minutes in interactive Claude Code sessions.`

## Preconditions

- IronClaude 5.0.0 installed for your user (`superclaude install` done): `superclaude --version` prints `SuperClaude, version 5.0.0`.
- codegraph 1.6.2 installed by `superclaude install` and `~/.local/bin` on your `PATH`, so a bare `codegraph` resolves. `/sc:graph init` may only call bare `codegraph` (allowlist `Bash(codegraph init --yes *)`, `src/superclaude/commands/graph.md:9`); the installer only warns when `~/.local/bin` is not on `PATH` (`src/superclaude/cli/install_codegraph.py:155-163`). Whether `/sc:graph init` works without it is UNVERIFIED; fix `PATH` before Tier C.
- `git` and the `claude` CLI on your `PATH`, and a Claude Code login for Tier C (each Tier C step uses API tokens).
- `/tmp/d03` does not exist (`[ ! -e /tmp/d03 ] && echo OK` prints `OK`). Every file this guide creates is under `/tmp/d03`. The steps set `XDG_STATE_HOME=/tmp/d03/state` so the hook log also lands there. No step installs, registers or edits anything under `~/.claude`, but the Tier C sessions still write there: Claude Code saves each session's history, the freshness hooks that `superclaude install` registers write state and log files under `~/.claude/state/` and `~/.claude/logs/` at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `src/superclaude/hooks/scripts/freshness-session-start.sh:8-9`, `freshness-user-prompt.sh:8-10`), and `auggie-flag-clear.sh` writes there after auggie tool calls (`hooks.json:104`; `auggie-flag-clear.sh:10-12`).
- About memory: the first init of a large checkout can use up to about 1 GB (`CHANGELOG.md:93`); the fixture here has four small files and indexes in well under a second.

## What you're verifying

- The `startup` SessionStart hook starts one background `codegraph init --yes` in a git checkout with no `.codegraph/codegraph.db`, prints nothing, skips a checkout that already has a database, and does nothing when `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`.
- `/sc:graph` prints an 8-line readiness report and one next action; `/sc:graph init` builds the index once and refuses a second build; a bad argument stops with `status: blocked`.
- `/sc:impact` writes `impact.md` and `return-contract.yaml`, labels each row `def-line`, `call-site-verified` or `unresolved`, supports `--diff` and `--tests`, blocks a symbol combined with `--diff`, and with `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` still finishes with `status: partial` on Grep.

---

## Steps

### Tier A — free smoke on your machine (read-only)

#### Step 1 — Versions and the bare `codegraph` `[FREE]`

**Do:**

```bash
superclaude --version; codegraph --version; command -v codegraph
```

**Expected result:** `SuperClaude, version 5.0.0`, then `1.6.2`, then a path (normally `~/.local/bin/codegraph`, a link into `~/.codegraph/versions/v1.6.2/`). An empty last line means `~/.local/bin` is not on `PATH`: fix that before Tier C. (source: pin `Pinned codegraph version: 1.6.2`, `src/superclaude/core/CODEGRAPH.md:34`; bare-name rule `src/superclaude/core/CODEGRAPH.md` section 5 rule 8 and `src/superclaude/commands/graph.md:9`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — codegraph MCP registration `[FREE]`

**Do:**

```bash
claude mcp get codegraph
```

**Expected result:** `Scope: User config (available in all your projects)`, `Type: stdio`, `Args: serve --mcp`, and the environment lines `CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_NO_UPDATE_CHECK=1`, `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`. (source: `src/superclaude/cli/install_mcp.py:862-874`; tool list `src/superclaude/cli/install_codegraph.py:35`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 3 — Commands, guide and hook are installed `[FREE]`

**Do:**

```bash
ls ~/.claude/commands/sc/graph.md ~/.claude/commands/sc/impact.md ~/.claude/CODEGRAPH.md ~/.claude/hooks/codegraph-session-start.sh
grep -c 'codegraph-session-start.sh' ~/.claude/settings.json
```

**Expected result:** The four paths are listed with no `No such file` error, and the count is `1` or more. The hook is registered under `SessionStart` with matcher `startup` and a 5-second timeout. (source: `src/superclaude/hooks/hooks.json:24-31`; the installer merges hook registrations into `~/.claude/settings.json`, `src/superclaude/cli/install_hooks.py:1-5`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local writes under /tmp/d03

#### Step 4 — Create the fixture repository `[LOCAL-WRITE]`

**Do:** (bash; keep this terminal open, Tier C uses a second one)

```bash
[ ! -e /tmp/d03 ] || { echo "remove /tmp/d03 first"; false; }
mkdir -p /tmp/d03/repo/pkg /tmp/d03/repo/tests /tmp/d03/state /tmp/d03/out
cd /tmp/d03/repo && git init -q .
printf '.dev/\n' > .gitignore
touch pkg/__init__.py
cat > pkg/config.py <<'EOF'
def parse_config(text):
    return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)


def load_settings(path):
    with open(path) as fh:
        return parse_config(fh.read())
EOF
cat > pkg/cli.py <<'EOF'
from pkg.config import load_settings


def main(path):
    settings = load_settings(path)
    print(settings)
EOF
cat > tests/test_config.py <<'EOF'
from pkg.config import parse_config


def test_parse_config():
    assert parse_config("a=1") == {"a": "1"}
EOF
git add -A && git -c user.name=d03 -c user.email=d03@example.invalid commit -qm fixture
git log --oneline | wc -l
```

**Expected result:** `1`. The fixture has `parse_config` (line 1 of `pkg/config.py`), its caller `load_settings` (defined at line 5, calls it at line 7), the caller's caller `main` (`pkg/cli.py:4`) and a test `test_parse_config` (`tests/test_config.py:4`). `.dev/` is ignored so `/sc:impact` output written into the repo is neither indexed nor shown by `git diff` (ignored files are not indexed, `src/superclaude/core/CODEGRAPH.md:7`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — The fixture starts without an index `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d03/repo
pgrep -f 'codegraph\.js (init|index)' || codegraph status
```

**Expected result:** `pgrep` prints nothing (no init is running), then `CodeGraph Status`, `Project: /tmp/d03/repo`, `⚠ Not initialized` and `ℹ Run "codegraph init" to initialize`. Never run `codegraph status` while `pgrep` prints a line: it can empty an index being built. (source: the "Not initialized" text is what `/sc:graph` classifies as `not_initialized`, `src/superclaude/core/CODEGRAPH.md:13,17`). UNVERIFIED: the exact `codegraph status` lines were observed once with codegraph 1.6.2 on this fixture; no code line, `--help` output or transcript range holds them, so treat the wording as a guide and judge PASS on "not initialized".

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — Hook switched off with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` `[LOCAL-WRITE]`

**Do:**

```bash
SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 CLAUDE_PROJECT_DIR=/tmp/d03/repo XDG_STATE_HOME=/tmp/d03/state \
  sh ~/.claude/hooks/codegraph-session-start.sh; echo "exit=$?"
ls -A /tmp/d03/repo; ls -A /tmp/d03/state
```

**Expected result:** `exit=0` with no other output from the hook; `/tmp/d03/repo` holds only `.git`, `.gitignore`, `pkg` and `tests` (no `.codegraph`); `/tmp/d03/state` is empty. (source: `src/superclaude/hooks/scripts/codegraph-session-start.sh:11`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — Hook builds the index of a new clone `[LOCAL-WRITE]`

**Do:**

```bash
git clone -q /tmp/d03/repo /tmp/d03/hooked
out=$(env -u SUPERCLAUDE_CODEGRAPH_AUTOINIT CLAUDE_PROJECT_DIR=/tmp/d03/hooked XDG_STATE_HOME=/tmp/d03/state \
  sh ~/.claude/hooks/codegraph-session-start.sh); echo "exit=$? stdout=[$out]"
for i in $(seq 1 30); do [ -e /tmp/d03/hooked/.codegraph/codegraph.db ] && ! pgrep -f 'codegraph\.js (init|index)' >/dev/null && break; sleep 1; done
ls -A /tmp/d03/hooked/.codegraph; tail -n 12 /tmp/d03/state/superclaude/codegraph-init.log
cd /tmp/d03/hooked && codegraph status | tail -n 2
```

**Expected result:** `exit=0 stdout=[]` (the hook returns at once and prints nothing). `.codegraph/` holds `.gitignore` and `codegraph.db`. The log `/tmp/d03/state/superclaude/codegraph-init.log` ends with the init output, including `Initialized in /tmp/d03/hooked`, `Indexed 4 files` and `Done`. The last status line is `✓ Index is up to date`. (source: binary lookup, git top level, skip rules and the one detached `nohup codegraph init --yes <top>` with its log path, `src/superclaude/hooks/scripts/codegraph-session-start.sh:15-31`). UNVERIFIED: the log lines (`Initialized in ...`, `Indexed 4 files`, `Done`, `✓ Index is up to date`) and the file count were observed once with codegraph 1.6.2 on this fixture; no code line, `--help` output or transcript range holds them. PASS needs `.codegraph/codegraph.db` and a log that ends without an error.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — Hook skips a checkout that already has a database `[LOCAL-WRITE]`

**Do:**

```bash
before=$(wc -c < /tmp/d03/state/superclaude/codegraph-init.log)
CLAUDE_PROJECT_DIR=/tmp/d03/hooked XDG_STATE_HOME=/tmp/d03/state sh ~/.claude/hooks/codegraph-session-start.sh
sleep 2; after=$(wc -c < /tmp/d03/state/superclaude/codegraph-init.log); echo "before=$before after=$after"
```

**Expected result:** `before` and `after` are equal: no second init starts, because `.codegraph/codegraph.db` exists (in any state). (source: `src/superclaude/hooks/scripts/codegraph-session-start.sh:24-25`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — interactive Claude Code sessions

Run these in a second terminal. Type each `/sc:` line at the Claude Code prompt exactly as shown. `<UTC>` stands for the time of the check, `YYYY-MM-DDTHH:MM:SSZ`. If `/tmp` is a symbolic link on your system (macOS), paths in reports show the resolved form (for example `/private/tmp/d03/repo`), because the skills use `realpath` (`src/superclaude/skills/sc-graph-protocol/SKILL.md:37`).

#### Step 9 — `/sc:graph` in a checkout that is not initialized `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d03/repo && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 XDG_STATE_HOME=/tmp/d03/state claude
```

```text
/sc:graph
```

**Expected result:** Claude loads the `sc:graph-protocol` skill and prints the 8-line report in this order: `codegraph 1.6.2 (pin 1.6.2: match)`; `index: not_initialized (none), checked <UTC>`; `access: mcp; MCP lookup tools listed: yes`; a counts line (no counts exist yet, so the numbers are missing; the exact wording for missing counts is UNVERIFIED); `pending: unknown` or a number; `telemetry: <on|off|unknown> — opt out: export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile`; `switch off codegraph in primitives: SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; `next: type /sc:graph init to index this worktree (the session-start hook normally does this; about 4.5 s and 34 MB per 500 files)`. From a shell, `ls -A /tmp/d03/repo` still shows no `.codegraph`: the hook was switched off for this session. (source: `src/superclaude/commands/graph.md:21,40`; classification `src/superclaude/skills/sc-graph-protocol/SKILL.md:40`; next action `SKILL.md:57`; report lines `SKILL.md:142-151`; hook switch `src/superclaude/hooks/scripts/codegraph-session-start.sh:11`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 10 — `/sc:graph init` builds the index `[CLAUDE-SESSION]`

**Do:** (same session)

```text
/sc:graph init --output-dir /tmp/d03/out/init1
```

**Expected result:** The preflight allows `form: default`; Claude runs exactly one `codegraph init --yes /tmp/d03/repo` (timeout 10 minutes), then re-checks. The report now reads `index: fresh (own), checked <UTC>` and `next: index ready`. From a shell, `ls /tmp/d03/repo/.codegraph/codegraph.db` exists and `/tmp/d03/out/init1/return-contract.yaml` contains `command: graph`, `subcommand: init`, `status: success`, `index_state: fresh`, `worktree_relation: own`, `pin_match: true`, `next_action: none` and `init: {requested: true, form: default, ran: true, exit_code: 0, refused_reason: null}`. If the report shows `partial`, record the `index_state` it shows. (source: `src/superclaude/commands/graph.md:44-53`; preflight `src/superclaude/skills/sc-graph-protocol/SKILL.md:68-83`; contract and status rules `SKILL.md:85-110`; `next: index ready` `SKILL.md:62`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — A second `/sc:graph init` is refused `[CLAUDE-SESSION]`

**Do:** (same session)

```text
/sc:graph init --output-dir /tmp/d03/out/init2
```

**Expected result:** No `codegraph init` call runs; the preflight refuses because this worktree already has its own fresh index (rebuilding is not offered). `/tmp/d03/out/init2/return-contract.yaml` contains `subcommand: init`, `status: blocked` and `refused_reason: already_initialized` in the `init` block, with `ran: false`. (source: `src/superclaude/skills/sc-graph-protocol/SKILL.md:75,106-110`; `src/superclaude/commands/graph.md:46,64`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 12 — Invalid argument `[CLAUDE-SESSION]`

**Do:** (same session)

```text
/sc:graph bogus
```

**Expected result:** The message ``Unknown subcommand `bogus`; use `status` or `init` `` and `status: blocked`; no Bash command runs. (source: `src/superclaude/skills/sc-graph-protocol/SKILL.md:23-25`; `src/superclaude/commands/graph.md:31`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 13 — `/sc:impact` with a symbol `[CLAUDE-SESSION]`

**Do:** (same session)

```text
/sc:impact parse_config
```

**Expected result:** Claude loads `sc:impact-protocol` and prints the `## Summary` table of the report. Two files are written in `/tmp/d03/repo/.dev/impact/parse-config-<YYYYMMDDTHHMMSSZ>/`: `impact.md` and `return-contract.yaml`. The contract shows `command: impact`, `status: success` (or `partial` only when `degraded` holds a token other than `graph:unresolved`), `input: {mode: symbols, symbols: [parse_config], ...}`, `readiness` with `access: mcp` and `index_state: fresh`, `advisory: false`, a `symbols` entry for `parse_config` in `pkg/config.py` with `start_line: 1`, and `dependents` rows that include at least:

- `caller: load_settings`, `file: pkg/config.py`, `def_line: 5`, `partition: prod`, `hop: 1`, `source: callers`, `resolution: call-site-verified`, `call_site_line: 7`
- `caller: test_parse_config`, `file: tests/test_config.py`, `def_line: 4`, `partition: test`, `hop: 1`, `resolution: def-line` (only production rows get call-site confirmation)
- `caller: main`, `file: pkg/cli.py`, `def_line: 4`, `hop: 2`, `source: impact`, `resolution: def-line`

`impact.md` starts with YAML front matter, then these headings in order: `## Summary`, `## How to read this`, `## Readiness`, `## Input`, `## Definitions`, `## Production dependents`, `## Test dependents`, `## Limits`, `## Degraded and fallbacks` (`## Unclassified dependents`, `## Tests (advisory)` and `## Unmapped files` appear only when they have content). (source: default output dir and slug `src/superclaude/skills/sc-impact-protocol/SKILL.md:29`; steps 4-7 `SKILL.md:42-46`; advisory rule `SKILL.md:55` with `Freshness experiment E-1: outcome-A` at `src/superclaude/core/CODEGRAPH.md:35`; status merge `SKILL.md:98-103`; layout `SKILL.md:144-157`; outputs `src/superclaude/commands/impact.md:47-50`; extra rows of kind file, such as `test_config.py`, may also appear.) UNVERIFIED: the three `dependents` rows are what `codegraph callers` and `codegraph impact` returned once for this fixture with codegraph 1.6.2; no code line, `--help` output or transcript range holds them.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 14 — `/sc:impact --diff` `[CLAUDE-SESSION]`

**Do:** first, in your first terminal:

```bash
cd /tmp/d03/repo && sed -i.bak 's/if "=" in line)/if "=" in line and not line.startswith("#"))/' pkg/config.py && rm pkg/config.py.bak
git diff --stat; git rev-parse HEAD
```

Then in the session:

```text
/sc:impact --diff --output-dir /tmp/d03/out/diff1
```

**Expected result:** `git diff --stat` shows `pkg/config.py | 2 +-`. `/tmp/d03/out/diff1/return-contract.yaml` shows `input.mode: diff`, `diff_base` equal to the SHA `git rev-parse HEAD` printed, `changed_files: [pkg/config.py]`, a `symbols` entry `name: parse_config` with `mapped_by: hunk`, and the same dependents as Step 13. Status is `success`, or `partial` with `graph:stale` if codegraph had not yet synced your edit (the index catches up only while a codegraph MCP server watches the worktree). (source: diff mode D1-D4 `src/superclaude/skills/sc-impact-protocol/SKILL.md:41`; `--diff` default `HEAD` `src/superclaude/commands/impact.md:32`; stale handling `SKILL.md:170`; `src/superclaude/core/CODEGRAPH.md:83`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 15 — `/sc:impact --tests` `[CLAUDE-SESSION]`

**Do:**

```text
/sc:impact parse_config --tests --output-dir /tmp/d03/out/tests1
```

**Expected result:** The contract has `input.tests: true`, `tests: [{path: tests/test_config.py, source: both}]` and `selection_source: advisory` (`codegraph affected pkg/config.py --json --quiet` returns `tests/test_config.py`, and the name heuristic `**/test_config.*` finds the same file). If `affected` contributed nothing, the row is `source: heuristic` and `selection_source: heuristic_only`. `impact.md` has a `## Tests (advisory)` section ending with `Adds tests to a selection; never removes any.` (source: `src/superclaude/skills/sc-impact-protocol/SKILL.md:47,94-95,154`; `src/superclaude/commands/impact.md:35`). UNVERIFIED: that `codegraph affected` returns `tests/test_config.py` (and so `source: both`) was observed once with codegraph 1.6.2 on this fixture; no code line, `--help` output or transcript range holds it. The `heuristic` fallback above is the code-backed alternative.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 16 — A symbol and `--diff` together are blocked `[CLAUDE-SESSION]`

**Do:**

```text
/sc:impact parse_config --diff --output-dir /tmp/d03/out/blocked1
```

**Expected result:** The run stops at flag validation with `status: blocked`; no codegraph lookup runs. The contract is still written because the output directory resolves: `/tmp/d03/out/blocked1/return-contract.yaml` shows `status: blocked`. Afterwards, exit the session (`/exit`) and restore the fixture: `cd /tmp/d03/repo && git checkout -- pkg/config.py`. (source: "either symbols or `--diff`, never both" `src/superclaude/commands/impact.md:31`; STOP rule and contract-on-block `src/superclaude/skills/sc-impact-protocol/SKILL.md:21-23,100`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 17 — The hook indexes a new clone at session start `[CLAUDE-SESSION]`

**Do:**

```bash
git clone -q /tmp/d03/repo /tmp/d03/clone2
cd /tmp/d03/clone2 && env -u SUPERCLAUDE_CODEGRAPH_AUTOINIT XDG_STATE_HOME=/tmp/d03/state claude
```

Wait about 10 seconds, then from your first terminal run `ls /tmp/d03/clone2/.codegraph/` and `grep -c 'Initialized in /tmp/d03/clone2' /tmp/d03/state/superclaude/codegraph-init.log`. Then in the session:

```text
/sc:graph
```

**Expected result:** `.codegraph/` holds `codegraph.db` (and `.gitignore`); the `grep -c` count is `1`. The report shows `index: fresh (own)` and `next: index ready`. If the init is still running you see `index: stale` and `next: an init or index is running (usually the session-start hook); wait and run /sc:graph status`; run `/sc:graph` again after a few seconds. Exit the session afterwards. (source: registration `src/superclaude/hooks/hooks.json:24-31`; hook `src/superclaude/hooks/scripts/codegraph-session-start.sh:21-31`; running-init branch `src/superclaude/skills/sc-graph-protocol/SKILL.md:39,60`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 18 — `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` degrades but never stops `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d03/repo && SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off XDG_STATE_HOME=/tmp/d03/state claude
```

```text
/sc:graph
/sc:impact parse_config --output-dir /tmp/d03/out/off1
```

**Expected result:** `/sc:graph` reports `index: disabled (unknown), checked <UTC>`, `access: none; ...` and `next: codegraph use in primitives is switched off by SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off; unset it to use the graph`. `/sc:impact` still finishes and writes both files; `/tmp/d03/out/off1/return-contract.yaml` shows `status: partial`, `graph:disabled` in `degraded`, `readiness` with `index_state: disabled` and `access: none`, and `dependents` rows with `source: grep`, `resolution: unresolved` and `caller: null`. It never says the symbol has no dependents. Exit the session afterwards. (source: switch `src/superclaude/core/CODEGRAPH.md:11`; `src/superclaude/skills/sc-graph-protocol/SKILL.md:36,54`; Grep fallback `src/superclaude/skills/sc-impact-protocol/SKILL.md:48`; failure table row `SKILL.md:167`; never stops `src/superclaude/commands/impact.md:13,63`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[CLAUDE-SESSION]` `/sc:graph status --worktree-local` | The message "`--worktree-local` applies only to `init`" and `status: blocked` | `src/superclaude/skills/sc-graph-protocol/SKILL.md:26` | ☐ |
| `[CLAUDE-SESSION]` `/sc:graph status --output-dir /tmp/d03/repo/.git/x` (session in `/tmp/d03/repo`) | `status: blocked`; nothing written inside `.git/` | `src/superclaude/skills/sc-graph-protocol/SKILL.md:27` | ☐ |
| `[CLAUDE-SESSION]` In a new clone started with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (no index): `/sc:graph init --worktree-local` | Refused, `refused_reason: worktree_local_not_nested`; no init runs | `src/superclaude/skills/sc-graph-protocol/SKILL.md:79` | ☐ |
| `[CLAUDE-SESSION]` `/sc:impact Config.parse_config` | `status: blocked`: pass the bare name; codegraph has no `Class/method` addressing | `src/superclaude/skills/sc-impact-protocol/SKILL.md:23` | ☐ |
| `[CLAUDE-SESSION]` `/sc:impact parse_config --depth 4` | `status: blocked` (depth must be 1-3) | `src/superclaude/skills/sc-impact-protocol/SKILL.md:25` | ☐ |
| `[CLAUDE-SESSION]` `/sc:impact --diff nosuchref` | `status: blocked` (the base ref does not resolve) | `src/superclaude/skills/sc-impact-protocol/SKILL.md:24` | ☐ |
| `[CLAUDE-SESSION]` `/sc:impact parse_config --test-depth 2` (no `--tests`) | `status: blocked` | `src/superclaude/skills/sc-impact-protocol/SKILL.md:28` | ☐ |
| `[CLAUDE-SESSION]` `/sc:impact parse_config --caller sc-implement-protocol --output-dir /tmp/d03/out/caller1` | Chat output is three lines: status, degraded tokens, contract path | `src/superclaude/commands/impact.md:38`; `src/superclaude/skills/sc-impact-protocol/SKILL.md:32` | ☐ |
| `[LOCAL-WRITE]` In `/tmp/d03/hooked`, append a line to `pkg/cli.py`, then `pgrep -f 'codegraph\.js (init\|index)' \|\| codegraph status` with no Claude session open | `Pending Changes:` and `Modified:  1 files`: a stale index is detectable without an MCP server | `src/superclaude/core/CODEGRAPH.md:19,37`; UNVERIFIED: the `Pending Changes:` and `Modified:  1 files` text was observed once with codegraph 1.6.2 and is in no code line, `--help` output or transcript range | ☐ |
| `[CLAUDE-SESSION]` A new clone started with `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` only (hook switch unset) | `.codegraph/codegraph.db` still appears: the primitives switch does not affect the hook | `src/superclaude/core/CODEGRAPH.md:26`; `CHANGELOG.md:87` | ☐ |
| `[CLAUDE-SESSION]` Delete `/tmp/d03/clone2/.codegraph`, then resume with `claude --continue` in `/tmp/d03/clone2` | No new index: the hook is registered for the `startup` matcher only. That Claude Code reports a resumed session as `resume`, not `startup`, is Claude Code behaviour: UNVERIFIED here | `src/superclaude/hooks/hooks.json:24` | ☐ |

## Cleanup

```bash
cd /tmp && rm -rf /tmp/d03
```

This removes the fixture, its clones and their `.codegraph/` indexes, the hook log under `/tmp/d03/state` and every `/sc:graph` and `/sc:impact` output. No step changed your `~/.claude` setup or MCP registrations. The Claude Code sessions of Tier C stay in Claude Code's own session history, like any session.

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
