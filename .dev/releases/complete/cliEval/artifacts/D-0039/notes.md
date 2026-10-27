# D-0039 — Design notes for the claude version pin

## Why a config field, not a doctor constant

The phase-2 AC (T02.20) explicitly says "version floor is sourced from
`EvalConfig` (not hard-coded in doctor)." Two reasons drove this:

1. **Single source of truth.** When R1 follow-up bumps the floor (e.g.
   to `0.6.0` after a breaking `claude` release), the change lands in
   `config.py` only. The doctor module never grows a duplicate copy
   that could drift.
2. **Test seam ergonomics.** Existing tests monkeypatch the probe
   callable, but the floor itself was previously baked in. By moving
   it into `EvalConfig`, tests construct a strict / permissive config
   and exercise the boundary without monkeypatching module state.

## Why keep `min_version=` as an explicit kwarg

The legacy `_check_claude_version(probe=…, min_version=…)` signature is
still in use across the existing `tests/cli/eval/test_doctor.py`
fixtures. Removing it would have produced churn unrelated to T02.20.
The new kwarg `config=` is preferred for new tests; the explicit
`min_version=` is a permitted shortcut.

## Why no `max_version` enforcement yet

R1-mit was scoped to a closed-floor / open-ceiling policy at M2. A
future M3+ task can add `max_claude_version` to `EvalConfig` (and a
matching probe row) without breaking the M2 floor contract. The tuple
type is forward-compatible.

## Why the regex did not need to change

The pre-existing `_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")`
already extracts the first `X.Y.Z` triple in the probe output. Banner
variants observed in M1/M2 dev hosts (`claude 0.5.0`, `claude 0.7.3
(build 12)`) all conform. If a future banner adds a `v` prefix or a
build suffix that swallows the patch digit, this regex still extracts
the first triple — verified by
`test_version_probe_passes_on_higher_release`.

## Why the import order moved

`commands.py` already imports from `.capabilities`, `.loader`,
`.models`, `.suites`. Adding `.config` between `.capabilities` and
`.loader` keeps the relative-import block alphabetical (matches the
existing convention in `src/superclaude/cli/eval/`).
