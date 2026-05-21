# Troubleshoot Report: `eval run` Accepts Forbidden Scratch Roots That `doctor` Rejects

**Issue type:** bug (OPS-002 / AC12 policy bypass)
**Severity:** HIGH — silently writes to forbidden paths (e.g. `/etc/foo`).
**Scope:** `commands.py::eval_run` (~lines 1472-1477) + `config.py::resolve_scratch_root` (167-231).

## 1. Issue description

- `eval doctor --output-dir /etc/foo` correctly exits 2 with the canonical policy text.
- `eval run --output-dir /etc/foo --target src/foo` silently succeeds and creates `/etc/foo`.

Both should funnel through `resolve_scratch_root()` and enforce the same `EvalConfig.allowed_scratch_roots` allowlist.

## 2. Root cause

### doctor (correct), commands.py:815-817

```python
if output_dir is not None:
    try:
        resolve_scratch_root(output_dir)        # candidate only, NO kwarg
```

Allowlist stays default `(/tmp/eval-runs, <repo>/.dev/eval-runs)`. `/etc/foo` rejected.

### eval_run (buggy), commands.py:1468-1477

```python
requested_output = output_dir if output_dir is not None else _default_output_dir(run_id)
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
    output_dir=output_dir,     # BUG: same value as candidate
)
```

### The resolver, config.py:216-231

```python
allowed = [_resolve_prefix(p) for p in config.allowed_scratch_roots]
if output_dir is not None:
    allowed.append(_resolve_prefix(Path(output_dir)))   # appends candidate to its own allowlist
...
for prefix in allowed:
    if resolved == prefix or resolved.is_relative_to(prefix):
        return resolved        # trivially true
```

When the candidate IS the `output_dir`, the resolved candidate is appended to `allowed`, so `resolved == prefix` always fires. The allowlist check becomes a **tautology**. `/etc/foo`, `/root`, `/`, anything passes.

### Intent vs. misuse

The `output_dir=` kwarg (docs config.py:192-195, scratch-roots.md:91-97) is meant to extend the allowlist for **sub-paths minted inside the operator's output dir** (per-eval HOMEs, working trees) — i.e. when the candidate is a CHILD of an already-validated root. `eval_run` misuses it by passing the same value for both the candidate and the policy extension. `doctor` shows the correct pattern: validate the root first WITHOUT the kwarg.

## 3. Evidence

- `config.py:167-231` — resolver definition; self-extension bug at 219-220.
- `commands.py:815-817` — doctor's correct call.
- `commands.py:1466-1477` — eval_run's buggy call.
- `scratch-roots.md:16-20, 91-97` — `--output-dir` is "call-scoped", intended for sub-path checks, never to authorize the root itself.

## 4. Proposed solutions (ranked)

### A. Recommended: drop the self-referential kwarg in `eval_run`

Change `commands.py:1472-1477` to:

```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
)
```

Forces `--output-dir` to live under one of the canonical allowlist roots, matching `doctor`. **Risk: LOW** — restores designed behavior.

### B. Defense-in-depth: tighten the resolver

Make `resolve_scratch_root` reject the self-allowlisting pattern:

```python
if output_dir is not None:
    od_resolved = _resolve_prefix(Path(output_dir))
    if resolved == od_resolved:
        base_allowed = allowed[:-1]
        if not any(resolved == p or resolved.is_relative_to(p) for p in base_allowed):
            raise ScratchRootViolation(candidate, resolved, base_allowed)
        return resolved
```

Protects every present and future caller. **Risk: MEDIUM** — public-helper semantic change; needs a unit test.

### C. Preferred for landing: A + B + regression test

Apply A to close the live bug, B to prevent reintroduction, plus a test asserting `resolve_scratch_root("/etc/foo", output_dir="/etc/foo")` raises.

## 5. Risk assessment

| Solution | Closes bug | Future-proof | Surface |
|----------|-----------|--------------|---------|
| A        | yes       | no           | 1 line  |
| B        | yes       | yes          | resolver semantics |
| C (A+B)  | yes       | yes          | 1 line + resolver guard |

## 6. Verification plan (when `--fix` is authorized)

1. `eval run --output-dir /etc/foo --target src/foo` → exit 2, no directory created.
2. `eval run --output-dir /tmp/eval-runs/sanity --target src/foo` → success.
3. `uv run pytest tests/cli/eval/test_scratch_root_policy.py tests/cli/eval/test_scratch_root_allowlist.py -v` → green.
4. `eval doctor --output-dir /etc/foo` still exits 2.

## 7. Recommended next action

Stop here per `--fix`-not-supplied default. Operator may re-run with `--fix` to apply Solution C.
