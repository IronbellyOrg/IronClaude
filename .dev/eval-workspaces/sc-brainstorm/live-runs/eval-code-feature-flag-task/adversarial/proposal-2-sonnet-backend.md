# Proposal 2 — sonnet / backend

## Stance

Optimize for backend reliability and operational simplicity. Skip the
custom control plane in v1; ship a file-based flag store with a thin
CLI for mutation and a watcher for live reload. Postgres + admin UI
are v2 concerns. The hot path is what matters; everything else can be
boring.

## Core Design

- **Flag store**: YAML file (`flags.yaml`) checked into a config repo,
  loaded into memory at process start, hot-reloaded via inotify /
  watchdog on file change. Schema enforced via Pydantic models.
- **Evaluator** (`feature_flags/evaluator.py`): Pure function
  `evaluate(flag_key, context) -> FlagResult`. No I/O. Reads from the
  in-memory map populated by the loader.
- **CLI** (`feature_flags/cli.py`): `flags set`, `flags unset`,
  `flags list`, `flags audit` commands that edit `flags.yaml` via a
  safe atomic-write helper and append to a structured audit log
  (`flags-audit.jsonl`).
- **OpenFeature shim** (`feature_flags/openfeature.py`): Thin adapter
  exposing the OpenFeature Python SDK surface so call sites can use
  the standard API. Internally delegates to the evaluator.
- **Bucketing**: SHA256 of `<flag-key>:<targeting-key>` mod 10000.
  Slower than Murmur but stdlib-only (no extra deps).

## Configuration

- `flags.yaml` is the single source of truth. Format:

  ```yaml
  flags:
    new-checkout-flow:
      type: boolean
      default: false
      rules:
        - rollout: 25  # 25% of targeting keys
        - allowlist: [internal-team]
      kill_switch: false
      owner: payments-team
      created: 2026-05-15
  ```

- File-based watchers trigger a re-parse + cache swap on change.
  Propagation latency = inotify delay (< 1s typically).
- Audit log is append-only JSONL: `{actor, ts, flag, old, new, reason}`.

## Failure Modes

- Malformed `flags.yaml` → loader rejects atomically; previous
  in-memory cache stays live. Emit error metric + alert.
- File missing on cold start → fail-closed across all flags; emit
  critical alert.
- Watcher dies → log + retry exponentially; cache stays usable
  during retries.

## Tradeoffs

- Pro: No external dependencies for v1 — just a file and the inotify
  watcher. Operationally trivial.
- Pro: Audit log is plain JSONL — easy to grep, tail, ship to Splunk.
- Pro: Sub-ms evaluation is trivial (dict lookup, no caching layer
  needed since the whole store fits in memory).
- Con: Scaling beyond ~10K flags becomes awkward (whole file reloaded
  on every change).
- Con: No multi-environment isolation by default — needs separate
  `flags.yaml` per env, which is a deploy-time concern.
- Con: No admin UI; operators must edit YAML + commit + deploy config
  repo. Faster than redeploying the service but slower than clicking
  a toggle.

## Acceptance Criteria

- Evaluator returns flag value in p99 < 0.5ms (it's a dict lookup).
- File watcher detects changes and swaps cache within 2s of write.
- Audit log JSONL has one entry per mutation, append-only.
- OpenFeature shim passes the boolean + string conformance subset.
- CLI rejects writes that would break schema; preserves previous
  state on rejection.
- Test coverage >= 85% on evaluator and CLI.
