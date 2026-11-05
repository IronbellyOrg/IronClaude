# E3-allowlist (Phase 3 Task 2, prerequisite experiment E-3)

Date: 2026-10-31, Claude Code 2.1.316, codegraph 1.6.2. Flag form checked first with `claude --help`: `--allowedTools, --allowed-tools <tools...>` (variadic, so the prompt must come before it), `--permission-mode` (choices include `dontAsk`), `--setting-sources`, `--strict-mcp-config`, `--output-format json`.

## Method

Each row is one headless session, run in the scratch worktree `.dev/worktrees/cg-sandbox`:

```bash
claude -p "Call the Bash tool exactly once with this exact command and no changes, then reply with only the first line of its output, or the word DENIED if the tool call was refused: <command>" \
  --permission-mode dontAsk --setting-sources project --strict-mcp-config \
  --output-format json --allowedTools "<allowedTools>" < /dev/null
```

`dontAsk` denies every tool call that no allow rule matches, and `--setting-sources project` keeps the user's own allow rules and hooks out, so the only allow rule is the one under test. "Allowed" means the JSON result has an empty `permission_denials` list and the command's real output came back; "denied" means the command appears in `permission_denials`. A first attempt with `--model haiku` failed to parse (the gateway answered with a model warning on stderr) and is not counted; the rows below are the rerun on the default model.

## Result

| id | allowedTools | command | exit | permission_denials | first line of result |
|---|---|---|---|---|---|
| a1 | `Bash(codegraph query *)` | `codegraph query install_core_files --json --limit 1` | rc=0 | denials=[] | result: [ |
| a2 | `Bash(codegraph affected *)` | `codegraph affected src/superclaude/cli/install_core.py src/superclaude/cli/main.py --json --quiet` | rc=0 | denials=[] | result: { |
| a3 | `Bash(codegraph node *)` | `codegraph node install_core_files` | rc=0 | denials=[] | result: **install_core_files** (function) |
| a4 | `Bash(codegraph callers *)` | `codegraph callers install_core_files --json --limit 3` | rc=0 | denials=[] | result: { |
| a5 | `Bash(codegraph impact *)` | `codegraph impact install_core_files --depth 1 --json` | rc=0 | denials=[] | result: { |
| a6 | `Bash(codegraph --version)` | `codegraph --version` | rc=0 | denials=[] | result: 1.6.2 |
| a7 | `Bash(codegraph init --yes *)` | `codegraph init --yes /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/.dev/worktrees/cg-nested` | rc=0 | denials=[] | result: ┌  Initializing CodeGraph |
| a8 | `Bash(pgrep -f *)` | `pgrep -f 'codegraph\.js (init|index)'` | rc=0 | denials=[] | result: Exit code 1 |
| n1 | `Bash(codegraph query *)` | `codegraph status` | rc=0 | denials=["codegraph status"] | result: DENIED |
| n2 | `Bash(codegraph callers *)` | `CODEGRAPH_TELEMETRY=0 codegraph callers install_core_files` | rc=0 | denials=["CODEGRAPH_TELEMETRY=0 codegraph callers install_core_files"] | result: DENIED |
| n3 | `Read` | `codegraph query install_core_files --json --limit 1` | rc=0 | denials=["codegraph query install_core_files --json --limit 1"] | result: DENIED |

- Allowed (a1-a8): every per-subcommand pattern the new skills need matches its own invocation, including positional file arguments (`affected a b`, a2), a quoted regex argument (`pgrep -f '…'`, a8) and the user-typed init form `Bash(codegraph init --yes *)` (a7; it built an index in the scratch nested worktree `cg-sandbox/.dev/worktrees/cg-nested`, removed with the sandbox). `pgrep` printing nothing exits 1, which the session reported as "Exit code 1": allowed, no init running.
- Denied (n1-n3): a pattern for one subcommand does not match another (`Bash(codegraph query *)` denies `codegraph status`, n1); a call prefixed with an environment variable is denied even though `Bash(codegraph callers *)` is allowed (n2), which confirms the guide rule "never prefix a call with environment variables"; with no Bash rule the call is denied (n3).
- So closed-Bash consumers can use exact per-subcommand patterns (`Bash(codegraph query *)`, `Bash(codegraph node *)`, `Bash(codegraph callers *)`, `Bash(codegraph impact *)`, `Bash(codegraph affected *)`, `Bash(codegraph --version)`, `Bash(pgrep -f *)`) and never need `Bash(codegraph *)`.
