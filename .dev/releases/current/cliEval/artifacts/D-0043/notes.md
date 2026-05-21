# D-0043 — Design notes

## Why a `SCRATCH_ROOT_POLICY` constant and a `format_scratch_root_violation()` renderer rather than inline strings at each catch site

The temptation at every CLI catch site is to write:

```python
except ScratchRootViolation as exc:
    click.echo(f"eval doctor: {exc}\nAllowed roots: /tmp/eval-runs/, ...", err=True)
    sys.exit(2)
```

That works for one catch site but creates an N-way drift surface as
soon as `eval run`, `eval gather`, and any future operator-facing
command lands. Each one rewrites the policy paragraph from memory;
each one rots independently when the allowlist changes. OPS-002's
job is to **prevent** that drift — so the policy lives in one constant
(`SCRATCH_ROOT_POLICY`) and one renderer (`format_scratch_root_violation`),
and every CLI surface is required to funnel through them. The renderer
also accepts the exception object directly, so the per-violation
forensic detail (offending path, resolved form, allowlist checked)
stays distinct from the static policy text.

`tests/cli/eval/test_scratch_root_policy.py::test_renderer_uses_blank_line_separator`
pins the separator format so a future "simplification" that
concatenates the two strings without a blank line would fail visibly.

## Why `--output-dir` validation runs **before** HARD-capability probing

The doctor command's natural flow is: probe HARD capabilities → render
checklist → exit. Inserting `--output-dir` validation **before** the
probe loop is a deliberate ordering choice for two reasons:

1. **Operator clarity.** A misconfigured `--output-dir` is an
   "invocation refused" outcome, not a "your environment is broken"
   outcome. Running the HARD probes first would mix unrelated
   capability failures (missing `claude` binary, etc.) into the
   doctor's output and bury the actual problem.
2. **Side-effect avoidance.** HARD probes may touch the filesystem
   (the `claude --version` invocation reads the binary, capability
   checks may inspect HOME-shaped paths). If the operator's
   `--output-dir` is hostile (e.g. `/etc/foo`), we want to refuse
   **before any filesystem read** that might depend on the rejected
   path. `test_scratch_violation_takes_precedence_over_hard_probe`
   pins this ordering: the test injects a deliberately broken
   `claude` PATH and asserts that the scratch-root rejection still
   wins.

The exit code (`SCRATCH_ROOT_VIOLATION_EXIT_CODE = 2`) is the same as
`HARD_FAIL_EXIT_CODE = 2` — both signify "harness refused to operate."
That collision is intentional: CI scripts only need to recognize one
"refused" exit code, and the stderr payload disambiguates which class
of refusal fired.

## Why three doc-anti-drift tests (not one big assertion)

`test_scratch_roots_doc_exists`, `test_scratch_roots_doc_names_three_allowed_roots`,
and `test_scratch_roots_doc_references_runtime_modules` could have been
folded into one mega-test. They are split for diagnostic granularity:

| Test | What a failure means |
|---|---|
| `_exists` | Someone deleted or renamed `docs/eval/scratch-roots.md`. The fix is to restore the file at that path. |
| `_names_three_allowed_roots` | The doc and the policy constant disagree on the 3 roots. The fix is to update whichever drifted. |
| `_references_runtime_modules` | The doc no longer cross-references the load-bearing module symbols. The fix is to add the missing reference so prose remains navigable to code. |

A single combined test would surface as "doc is wrong" and force the
developer to bisect which surface drifted. Three named tests turn the
pytest failure list itself into a diagnostic.

## Why `test_narrowing_config_changes_what_resolve_accepts` proves single-source-of-truth and `test_doctor_uses_default_evalconfig_allowlist` proves doctor wiring (two tests, not one)

The first iteration of this slice tried to use monkeypatch against
`_default_allowed_scratch_roots()` to narrow the doctor's effective
allowlist, then assert the doctor rejected what the unpatched allowlist
would have accepted. **It didn't work** — `EvalConfig` uses
`field(default_factory=_default_allowed_scratch_roots)`, and Python
captures the function reference at class-definition time, not on every
construction. Monkeypatching the module attribute changed what
*future* `EvalConfig` classes would see if they were re-defined, but
not what `EvalConfig()` resolved to in the current process.

The fix split the intent into two tests:

* `test_narrowing_config_changes_what_resolve_accepts` — passes an
  explicitly narrowed `EvalConfig(allowed_scratch_roots=(Path("/x"),))`
  directly to `resolve_scratch_root`, proving that the resolver
  respects whatever allowlist it receives. This is the
  "single-source-of-truth" claim.
* `test_doctor_uses_default_evalconfig_allowlist` — calls the doctor
  twice with two different `--output-dir` values (one in the default
  allowlist, one outside it) in the same fixture, asserting the
  doctor's accept/reject pair matches the default-`EvalConfig`
  allowlist. This is the "doctor wires to default config" claim.

Together they pin the contract the original mega-test was trying to
pin, without the frozen-dataclass footgun.

## Why the policy doc lives in `docs/eval/`, not in the deliverable artifacts directory

`.dev/releases/current/cliEval/artifacts/D-0043/spec.md` is a
*deliverable-tracking* document. It lives under `.dev/` because it is
phase-scoped: once the release lands and `current/` rotates, the spec
becomes a historical record. The **policy document** itself is part
of the project's operator-facing surface — it must be checked into
`docs/eval/` so it ships with the package and survives release
rotation. The deliverable spec cross-references the doc; the doc
cross-references the runtime modules and the deliverable spec. Two
locations, two purposes, one policy.

## Sibling-regression posture

Before landing, the family (`test_doctor.py`, `test_config.py`,
`test_scratch_root_allowlist.py`, `test_scratch_root_policy.py`)
runs at **69 passed in 0.18s** — no drift in adjacent deliverables
(D-0029 HomeIsolation, D-0016 `resolve_scratch_root` direct tests,
D-0001 `EvalConfig` field validation). The new `--output-dir` Click
option does not change the doctor's default exit code (`test_doctor.py`
still asserts exit 0 for green environments), and the renderer does
not change `str(ScratchRootViolation)` (the original "AC12" assertion
in `test_scratch_root_allowlist.py` still holds).

## Verification method

T02.25 is STRICT tier with `Verification Method: Direct test execution
+ sub-agent quality-engineer review`. Per phase-2-tasklist Step 5: "Run
`uv run pytest tests/cli/eval/test_scratch_root_policy.py -v`."
Evidence log captures the 16-passed result. Sub-agent
quality-engineer review is the next item on the T02.25 checklist
(STRICT-tier policy: cross-module changes require an independent
adversarial sweep). See `evidence/T02.25/` for run artifacts.
