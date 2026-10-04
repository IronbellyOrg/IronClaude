# cliEval scratch root policy (OPS-002 / AC12)

**Roadmap:** R-043 / OPS-002 (cross-module scratch-root enforcement).
**Source of truth:** `EvalConfig.allowed_scratch_roots` in
`src/superclaude/cli/eval/config.py` (T01.01 / D-0001). Every CLI command,
isolation primitive, and reporter that touches a scratch directory funnels
through `resolve_scratch_root()` (T01.19 / D-0016) — no module embeds a
second copy of the allowlist.

## The 3 allowed roots

The cliEval harness creates per-eval scratch HOMEs, per-eval working trees,
and any operator-supplied `--output-dir` under **exactly one** of the
following roots. Anything else is rejected before any filesystem write.

| # | Allowed root                  | Provenance                                                                                                                                                            |
|---|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | `/tmp/eval-runs/`             | Canonical M1 scratch root. Lives in `_default_allowed_scratch_roots()` so a fresh checkout works without operator configuration.                                      |
| 2 | `<repo>/.dev/eval-runs/`      | Repo-relative scratch root for sessions that want their artifacts on the same filesystem as the source tree. Anchors against process CWD via `Path.resolve()`.        |
| 3 | `--output-dir <path>`         | Operator-supplied path passed on the command line. Extends the allowlist **for the current invocation only**; never mutates `EvalConfig.allowed_scratch_roots`.       |

> **H4 / strict-sub-path rule (post cliEval Phase 5+6 remediation):** A **bare allowlist prefix** (e.g. `resolve_scratch_root("/tmp/eval-runs")` with no sub-path) now **raises `ScratchRootViolation`**. Only **strict sub-paths** of one of the three allowed roots are accepted — `/tmp/eval-runs/<run-id>/` is fine, but `/tmp/eval-runs` itself is **not**. This closes the AC12 tautology where the allowlist check would silently accept the prefix as a "match" of itself. The `resolved == prefix` accept branch was removed from `resolve_scratch_root` (`src/superclaude/cli/eval/config.py`). Test pinning: `tests/cli/eval/test_scratch_root_allowlist.py::test_resolve_scratch_root_rejects_bare_prefix` + `test_accepts_immediate_subdir_of_allowlist_root`. AC matrix row **H4**.

The canonical policy text emitted by `superclaude eval doctor` and every
other CLI boundary is the `SCRATCH_ROOT_POLICY` constant in
`src/superclaude/cli/eval/config.py` — that constant and this document
must list the same three roots. Drift between them is a release blocker
caught by `tests/cli/eval/test_scratch_root_policy.py`.

## Why an allowlist (and not a denylist)

The cliEval harness runs the real `claude` binary against per-eval HOMEs
that may contain operator-controlled hooks, settings, and prompt material.
A misconfigured scratch root that resolves under `~/.claude/`,
`/etc/`, `/var/lib/`, or any other location with non-eval state would let
a buggy or malicious suite mutate the operator's real environment. The
allowlist closes that surface by **defaulting to refusal**: only the
three named roots above (resolved symlink-free via `Path.resolve()`) are
ever accepted.

The same allowlist powers four layered defenses:

1. **Loader-time validation** (`SuiteLoader`, T01.07) rejects suites
   whose declared scratch root resolves outside the allowlist.
2. **Doctor pre-flight** (`superclaude eval doctor --output-dir`) tells
   operators *before* running a suite whether their `--output-dir` will
   be accepted, and quotes the policy verbatim when it will not.
3. **HomeIsolation containment** (`containment_guard`, T02.08) re-applies
   the check after `mkdtemp` so a symlink swap between loader-time and
   setup-time is still caught. **H5 ordering invariant (post Phase 5+6 remediation):** the runtime allowlist is extended with the resolved `--output-dir` (and the derived `home_root`) **before** the corresponding `mkdir(parents=True)` runs at BOTH call sites — `commands.py::eval_run` (H5a, AC matrix) and `isolation.py::HomeIsolation.setup` (H5b, AC matrix). A non-allowlisted path raises `ScratchRootViolation` **before** any on-disk side effect (OPS-002 / NFR-SEC2). Tests: `tests/cli/eval/test_home_isolation_extend.py::test_eval_run_extends_allowlist_before_mkdir` and `tests/cli/eval/test_containment.py::test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir`.
4. **Atomic setup wrapper** (T02.13) preserves the partial HOME with a
   `setup_failed` artifact tag when any of the above refuse, so
   forensics survive even when the harness aborts mid-setup.

See `D-0016/spec.md`, `D-0029/spec.md`, and `D-0043/spec.md` for the
deliverable-level details.

## How operators encounter the policy

### `superclaude eval doctor --output-dir <path>`

```
$ superclaude eval doctor --output-dir /etc/foo
eval doctor: scratch path escapes AC12 allowlist: path=/etc/foo resolved=/etc/foo allowed=[/tmp/eval-runs, /config/workspace/IronClaude/.dev/eval-runs]

cliEval scratch root policy (AC12 / OPS-002):
  Scratch HOMEs, per-eval working trees, and --output-dir targets MUST
  resolve under one of these allowed roots:
    1. /tmp/eval-runs/        -- canonical M1 scratch root
    2. <repo>/.dev/eval-runs/ -- repo-relative scratch root
    3. --output-dir <path>    -- extends the allowlist for the current
                                  invocation only (call-scoped, never
                                  mutates EvalConfig.allowed_scratch_roots)
  Anything else is rejected before any filesystem write.
  Authoritative reference: docs/eval/scratch-roots.md.
$ echo $?
2
```

The doctor exits `SCRATCH_ROOT_VIOLATION_EXIT_CODE` (= 2), matching the
loader-error trio so CI scripts only need to recognize a single
"harness refused to operate before any filesystem write" outcome.

### `superclaude eval run` (M3+)

Future `eval run`, `eval gather`, and any other command that accepts an
operator-supplied path will catch `ScratchRootViolation` the same way
and render it through `format_scratch_root_violation()`. New CLI surfaces
MUST funnel through that helper instead of reimplementing the message;
this is the OPS-002 cross-module consistency guarantee.

### Programmatic callers

Callers inside `src/superclaude/cli/eval/` invoke
`resolve_scratch_root(path, config=config, output_dir=output_dir)`
directly. The helper accepts an optional `output_dir` keyword that
extends the allowlist for the call only (see
`test_output_dir_is_call_scoped_not_persistent` in
`tests/cli/eval/test_scratch_root_allowlist.py`).

## Updating the policy

Any change to the allowed roots **must** land in four places in one
commit:

1. `_default_allowed_scratch_roots()` in `src/superclaude/cli/eval/config.py`.
2. `SCRATCH_ROOT_POLICY` in the same module.
3. The "The 3 allowed roots" table above.
4. `tests/cli/eval/test_scratch_root_allowlist.py` and
   `tests/cli/eval/test_containment.py` also pin the H4/H5 invariants
   described above (bare-prefix rejection + write-before-validate ordering);
   any allowlist change must update them too.

`tests/cli/eval/test_scratch_root_policy.py` reads the first three locations
and refuses to pass if they disagree, so a drift-introducing PR fails
fast in CI.

## Cross-references

- `R-043 / OPS-002` — roadmap deliverable for cross-module policy enforcement.
- `T01.01 / D-0001` — `EvalConfig` (single source of truth).
- `T01.19 / D-0016` — `resolve_scratch_root` (single ingress point).
- `T02.08 / D-0029` — `containment_guard` (FR-ISO2 defense in depth).
- `T02.25 / D-0043` — this document; doctor wiring + policy renderer.
