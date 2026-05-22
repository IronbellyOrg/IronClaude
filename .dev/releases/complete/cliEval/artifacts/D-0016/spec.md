# D-0016 — `resolve_scratch_root` + `ScratchRootViolation` (AC12 enforcement)

**Task:** T01.19 (Phase 1, Roadmap AC12 / R-016)
**Module:** `src/superclaude/cli/eval/config.py`
**Status:** Implemented 2026-05-20

## Purpose

Codify the AC12 scratch-root allowlist policy in a single helper so every
caller that mints scratch directories, per-eval HOMEs, or `--output-dir`
roots funnels through one ingress point. AC12 names the only safe
locations: `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or a CLI-supplied
`--output-dir` resolved against the allowlist; everything else MUST be
rejected before any filesystem write.

## Public surface

| Symbol | Kind | Purpose |
|---|---|---|
| `resolve_scratch_root(path, *, config=None, output_dir=None) -> Path` | function | Resolve `path` and verify it lives under an allowed root. Returns the resolved absolute path on success; raises `ScratchRootViolation` otherwise. |
| `ScratchRootViolation` | exception | Raised on any non-allowlisted resolution. Carries `path` (original input), `resolved` (absolute form), and `allowed` (resolved allowlist actually used for the check). |
| `SCRATCH_ROOT_VIOLATION_EXIT_CODE` | int constant | Exit code (= 2) the CLI maps `ScratchRootViolation` to. Matches the loader-error trio (`SCHEMA_ERROR_EXIT_CODE`, `INVALID_EVAL_ID_EXIT_CODE`, `UNRESOLVED_CAPABILITY_EXIT_CODE`). |

## Allowlist policy

The allowlist is `EvalConfig.allowed_scratch_roots` and ONLY
`EvalConfig.allowed_scratch_roots`. No other module embeds a hard-coded
copy — see the `test_allowlist_source_is_evalconfig` assertion in the
test set, which narrows the config and proves the helper follows.

Default contents (set in `_default_allowed_scratch_roots()` per D-0001):

1. `/tmp/eval-runs`
2. `.dev/eval-runs` (relative; anchors against process CWD via `Path.resolve()`)

The optional `output_dir` argument extends the allowlist *for the current
call only*. It does NOT mutate the supplied config; subsequent calls
without the argument fall back to `config.allowed_scratch_roots` alone.
The `test_output_dir_is_call_scoped_not_persistent` assertion locks this
invariant.

## Resolution semantics

1. The candidate path is normalised: `Path(path).expanduser().resolve(strict=False)`.
   `expanduser()` collapses `~`-prefixed home anchors so they cannot land
   silently inside a sub-tree that happens to contain `eval-runs`.
   `resolve(strict=False)` allows the directory not to exist yet (M1
   exit doctor outline runs do not create the scratch tree).
2. Each allowlist entry is resolved the same way (`_resolve_prefix`).
   Relative defaults (`.dev/eval-runs`) anchor against the process CWD,
   matching the behaviour `HomeIsolation` (T02.06) and the CLI `run`
   command (M2 T02.16) will see at runtime.
3. The resolved candidate passes iff `resolved == prefix` OR
   `resolved.is_relative_to(prefix)` for some prefix in the resolved
   allowlist. Both branches matter: the prefix itself (`/tmp/eval-runs`)
   is a valid scratch root, not merely a parent of one.
4. On no match, `ScratchRootViolation` is raised with the original
   input, the resolved form, and the resolved allowlist embedded so
   doctor / reporter callers can render the failure verbatim without
   re-resolving.

## Acceptance criteria → implementation map

| AC | Implementation site |
|---|---|
| `resolve_scratch_root` raises `ScratchRootViolation` for `/home/user/foo`, `/var/lib/eval-runs`, and any non-allowlisted prefix. | Parametrised `test_rejects_non_allowlisted_paths` (6 prefixes covered: `/home/user/foo`, `/var/lib/eval-runs`, `/etc/passwd`, `/root/.claude`, `/usr/local/share`, `/tmp/other-runs`). |
| Resolved paths under `/tmp/eval-runs/`, `.dev/eval-runs/`, or `--output-dir` pass. | `test_accepts_path_under_tmp_eval_runs`, `test_accepts_path_under_dev_eval_runs`, `test_accepts_path_under_output_dir`. |
| Allowlist source is `EvalConfig.allowed_scratch_roots`; no other module embeds a hard-coded copy. | `test_allowlist_source_is_evalconfig` — narrows the config to a single non-default root and proves the helper follows. |
| `TASKLIST_ROOT/artifacts/D-0016/spec.md` documents the allowlist policy. | This file. |

## Caller contract (downstream consumers)

| Caller | Stage | Notes |
|---|---|---|
| `HomeIsolation.setup()` (T02.06 / FR-ISO2) | pre-`mkdtemp` containment check (defense-in-depth) | Re-applies the same helper inside the isolation layer so a loader bypass still fails closed. |
| `eval run` CLI (M2 T02.16) | `--output-dir` argument resolution | Calls `resolve_scratch_root(output_dir, output_dir=output_dir)` to validate the user-supplied path is itself acceptable (no path traversal, no `~/.claude` etc.). |
| `eval doctor` (T01.13) | informational | May report the resolved allowlist as part of its `--json` payload so operators can sanity-check the policy before runs. |

## Risk / scope notes

* `Path.resolve(strict=False)` does not exist on Python 3.5; we require
  Python ≥ 3.10 per `pyproject.toml`, so the API is available.
* `is_relative_to()` (Python 3.9+) is the comparison primitive; it does
  NOT perform symlink resolution itself — that is `resolve()`'s job in
  the same line. Both are needed; either alone is unsafe.
* Symlink resolution is not separately delegated to `HomeIsolation` here.
  The isolation layer (T02.07, NFR-SEC2) re-resolves symlinks AFTER
  scratch creation but BEFORE hook deploy; that second pass is the
  load-bearing defense against `scratch-is-symlink-to-HOME` attacks.
  This helper's job is the prefix-allowlist check; the two layers are
  intentionally distinct.

## Cross-references

* `src/superclaude/cli/eval/config.py` — implementation.
* `tests/cli/eval/test_scratch_root_allowlist.py` — 19 assertions
  covering exit code, positive prefixes (`/tmp/eval-runs`, `.dev/eval-runs`,
  `--output-dir`), 6 negative prefixes, allowlist-source-of-truth,
  ergonomics, and traversal collapsing.
* `artifacts/D-0001/spec.md` — `EvalConfig.allowed_scratch_roots` field
  schema (the single source of truth this helper consumes).
* Roadmap entries: AC12 (R-016 / row 16) and OPS-002 (row 43).
* Design-spec §5 path containment guard (lines 404–409) — the broader
  policy this helper enforces at the loader / config layer.
