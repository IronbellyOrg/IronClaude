# D-0113 — implementation notes

## T01.17 follow-through

T01.17 (`artifacts/D-0015`) declared a `Makefile :: verify-deps` target in
its file inventory (`evidence.md` row 13: "Added (lines 318-322)"), but
the target body was never present in the committed `Makefile`. The CI
workflow (`.github/workflows/test.yml:148`) referenced `make verify-deps`,
which would have failed in CI on the first non-self-hosted run. T06.10
discovered the gap while satisfying its own AC ("`make verify-deps` exits
0 on the final tree") and closed it by adding the four-line target plus
a `.PHONY` entry and a help line. This is a minimal completion of T01.17's
documented intent, not a scope expansion of T06.10.

The fix is local to `Makefile` (no source-of-truth implications under
`src/superclaude/`); `make verify-sync` is unaffected (the four
sync scopes `skills|agents|commands|hooks` do not include `Makefile`).

## Comparison axes

Two diff axes are recorded in `evidence/T06.10/dep-diff.log`:

1. **Post-impl install vs combined AC3 baseline allow-list** — the
   subset check that `verify_deps.py` actually performs. Result: equal
   sets (36 packages each), zero additions, zero removals.
2. **Post-impl install vs pre-eval-CLI snapshot (34 packages)** — the
   "what did the eval CLI actually add" axis that SC3 cares about as a
   release attestation. Result: exactly `pexpect` and `ptyprocess`,
   both AC3-permitted.

The two axes answer different questions. The combined-allow-list axis
proves the gate is consistent with the install set today. The
pre-eval-CLI axis proves the eval CLI work only landed the two
explicitly-permitted transitive runtimes — no surprise direct deps
slipped in.

## On `jsonschema`

The AC3 contract explicitly names `jsonschema` as a permitted addition,
but `jsonschema` was already a direct dependency of `superclaude`
pre-eval-CLI (it appears in the 34-package pre-eval-CLI snapshot at
`evidence/T06.10/baseline-pre-eval-cli.txt`). The eval CLI's
`SuiteLoader` (T01.07) uses it for `suite.schema.json` validation but
does not require pyproject changes. Net contribution to the
post-impl tree: **0 packages** (still 1 entry, unchanged).

## On `ptytest` (vendored)

The vendored fork lives entirely under `src/superclaude/cli/eval/pty/`
and is shipped as source, not as a third-party PyPI dependency. It
therefore does not appear in `uv pip list` at all. Its only effect on
the dependency tree is the runtime requirement on `pexpect`, which the
allow-list permits.

## On CI fail-closed semantics

`scripts/verify_deps.py` exit codes (T01.17 / D-0015 §"Behaviour"):
- `0` — install set is a subset of the allow-list.
- `1` — at least one out-of-list package is installed.
- `2` — baseline file is missing or `uv pip list` failed.

`make verify-deps` propagates the script's exit code through the shell.
`test-summary` in `.github/workflows/test.yml` short-circuits on
`needs.verify-deps.result != 'success'`, so a future out-of-list
addition halts the full CI summary, not just the dependency job.

## On normalisation

Both the install snapshot and the baseline file are normalised by:
- `.lower()` — case-insensitive comparison.
- `.replace('_', '-')` — PEP 503 hyphenation.

This neutralises common upstream metadata drift (e.g. `Jinja2` vs
`jinja2`, `typing_extensions` vs `typing-extensions`) so the gate does
not produce spurious diffs.
