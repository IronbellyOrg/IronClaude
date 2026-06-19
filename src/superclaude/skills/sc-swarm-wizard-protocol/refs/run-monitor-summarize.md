# Run, monitor & summarize + error diagnostics (load in Wave 3–5)

All commands prefixed `uv run`. Substitute the resolved plan values. `<OUT>` = the chosen output dir.

> **Reassure the novice about `uv run` noise.** Many environments print a one-line warning like
> `warning: VIRTUAL_ENV=… does not match the project environment … will be ignored` before swarm output.
> It is harmless. If the user looks alarmed, say so plainly ("that yellow warning is normal — ignore it")
> rather than letting them think the run broke.

## Stub dry-run (Wave 3 — mandatory gate)

```bash
uv run superclaude swarm run --lens <LENS> --target <TARGET> --output <OUT> --transport stub
```

Success check (do all three):

```bash
test -f <OUT>/.swarm-state.json && grep -q '"state": "terminal"' <OUT>/.swarm-state.json
test -f <OUT>/return-contract.yaml
```

Expect stdout to end `swarm run: dispatched job (mode=lens, workers=N, results=N)` and exit 0.

Tell the user, plainly: "✅ The practice run worked — the pipeline is healthy. Note: that run used a
*stub*, so the findings are placeholder text, not a real review. The real run (next) uses your models."

If it fails → STOP, jump to §Errors, fix, re-dry-run. Never advance to a real run on a red dry-run.

## Launch the real run (Wave 4 — only after go-ahead + green dry-run + env OK)

Use a **fresh output dir** (don't reuse the dry-run dir). Pick the monitoring style:

Foreground + real TTY (live dashboard):

```bash
uv run superclaude swarm run --lens <LENS> --target <TARGET> --output <OUT_REAL> \
  --transport openai_compat --reviewers <N> --tui
```

Background / fire-and-forget (returns a JOB_ID immediately):

```bash
JOB=$(uv run superclaude swarm run --lens <LENS> --target <TARGET> --output <OUT_REAL> \
        --transport openai_compat --detached)
# later: uv run superclaude swarm attach "$JOB"   |   uv run superclaude swarm kill "$JOB"
```

Wizard tailing on the user's behalf (non-TTY) — arm a Monitor and poll state, do NOT add `--tui`:

- `Monitor` on `<OUT_REAL>/execution-log.jsonl` filtering for `worker_done` + failure signatures
  (`worker_done.*(timeout|parse_error|proxy_error)`, `Traceback`, `Error`).
- Completion = `<OUT_REAL>/.swarm-state.json` `state == "terminal"`. For inline runs there is **no
  `done.json`** — never block on it.

Detached completion (the only place `done.json` appears):

```bash
until [ -f <OUT_REAL>/done.json ]; do sleep 2; done   # detached/resume ONLY
```

Live phase/log inspection any time:

```bash
uv run superclaude swarm status --output <OUT_REAL> --watch --watch-interval 2
uv run superclaude swarm logs   --output <OUT_REAL> --tail
```

## Summarize (Wave 5)

Read `<OUT>/return-contract.yaml` and `<OUT>/.swarm-state.json`. Map fields → the plain-language template
in `templates/summary.md`:

- `status` → headline (success / partial / failed).
- `workers_succeeded` / `workers_requested` → "N of M reviewers finished".
- `output_files[].final_path` → where each reviewer's notes are.
- `merged_path` → the combined findings file (the one to read first).
- `recommended_next_command` → the single suggested next action (already rendered — present verbatim as
  copy-paste). Per-worker `status` values explain any non-success.

Then offer: re-run with different settings, or run the recommended next command.

## §Errors — diagnostics (translate every code; always give a next action)

| Signal | Plain-language meaning | Fix / next action |
|---|---|---|
| `uv run superclaude swarm --help` fails | swarm isn't installed or you're not in the repo | run from the repo root; check `uv` is set up |
| `imm4.target_too_small` / exit 1 at preflight | the file is too small/empty (<50 real characters) | pick a bigger/real source file |
| `inv007.env_missing` / `TransportEnvError` | the proxy isn't configured for real models | set `T2ProxyUrl`/`T2ProxyKey`/`T2Model01` from `~/.aienv`, or use a stub run |
| `unknown lens` / `custom` rejected / exit 2 | that lens name isn't usable as a shortcut | pick a listed lens; for custom use the advanced spec path |
| `--reviewers` rejected | the count must be 2, 3, or 4 | choose 2–4 |
| `--detached` exit 2 "tmux" | background mode needs tmux and you're not already inside tmux | install/enable tmux, or run in the foreground |
| `--tui` did nothing | the dashboard only shows on a real terminal | run in a real terminal, or just watch the normal output |
| contract `status: partial`/`failed` | some reviewers failed (timeout / proxy / parse error) | read per-worker `status`; offer `--resume` to retry only the failed ones |
| every worker `proxy_error` with **HTTP 404** on a real run | the proxy is reachable and the key is valid, but the path the CLI POSTs to doesn't exist — the swarm transport posts `{T2ProxyUrl}/chat/completions`, and your configured base doesn't expose chat-completions there (a known `:4000/cli` vs `:4000/cli/v1` base-path mismatch) | tell the user it's a proxy base-URL/routing issue, not a credential or wizard bug; ask them to verify `T2ProxyUrl` in `~/.aienv` exposes the chat-completions route. Do NOT guess or hardcode a corrected path — surface it for the operator to fix. The stub dry-run already proved the pipeline, so this is isolated to the proxy endpoint |
| monitor hangs waiting on `done.json` | inline runs don't write that file | switch to watching `state==terminal` / `status --watch` |

Resume only the failed workers of a prior real run:

```bash
uv run superclaude swarm run --resume <JOB_ID> --output <OUT_REAL> --transport openai_compat
```
