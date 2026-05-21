# D-0110 — AC1 Linux-only v1 platform declaration spec

**Task:** T06.07 (Phase 6, Roadmap AC1 / R-109)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure with a bounded code wire-up)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## AC1 contract

Roadmap row 353 (AC1 / R-109) requires:

1. `README.md` documents Linux-only v1 scope at the eval CLI section.
2. `eval doctor` on a non-Linux platform (or stubbed
   `platform.system() == "Darwin"`) exits with a friendly error.
3. `decisions.md` `AC1` entry status is `resolved`.
4. `artifacts/D-0110/spec.md` records the platform policy.

The authoritative satisfaction sites are:

- **README:** `README.md` §"Platform support" — operator-facing
  declaration enumerating supported/unsupported platforms + CI status,
  cross-linking the AC1/DOC-OQ9/AC2 closure sections in `decisions.md`.
- **ADR:** `.dev/releases/current/cliEval/decisions.md` §"AC1 Closure" —
  authoritative architectural decision record with cross-references to
  DOC-OQ9 (R6, macOS deferral), AC2 (R9, local-only deferral), and
  MIG-003 (T06.15, v2 follow-up consolidation).
- **Code:** `src/superclaude/cli/eval/commands.py` — `doctor` Click
  command runs a `platform.system()` precheck via
  `_default_platform_probe` before any capability gates; non-Linux
  values render `NON_LINUX_REFUSAL_TEMPLATE` on stderr and exit 2
  (`HARD_FAIL_EXIT_CODE`).
- **Tests:** `tests/cli/eval/test_doctor.py` — four new tests pin the
  Darwin refusal, the Windows refusal, the Linux happy path, and the
  friendly-error template's ADR citations.

## Platform-policy summary

| Field | Value |
|---|---|
| **v1 platform scope** | Linux only (any distribution that meets the Python `>=3.10` + UV requirements). |
| **macOS / Windows status (v1)** | NON-GOAL. No `Darwin` / `Windows` support code lands in v1. |
| **Refusal mechanism** | `superclaude eval doctor` calls `platform.system()` via the injectable `_default_platform_probe` helper. Any value other than `"Linux"` triggers `NON_LINUX_REFUSAL_TEMPLATE.format(system=...)` on stderr and `sys.exit(HARD_FAIL_EXIT_CODE)`. |
| **Refusal exit code** | 2 — reuses `HARD_FAIL_EXIT_CODE`. A non-Linux host is a precondition failure of the same class as a missing `claude` binary; introducing a dedicated `NON_LINUX_EXIT_CODE` would grow the harness exit-code surface without a useful caller-side distinction (the friendly message already names the cause). |
| **Refusal text** | `NON_LINUX_REFUSAL_TEMPLATE` — a module-level constant citing AC1 (R-109) and DOC-OQ9 so the operator can trace the v1 commitment back to the ADR log without a documentation hunt. Pinned as a constant so the four-token lock test (`AC1`, `R-109`, `DOC-OQ9`, `decisions.md`) catches drift. |
| **Scope of the precheck** | `eval doctor` only at v1. `eval run`, `eval list`, `eval describe` inherit the refusal transitively — operators run `eval doctor` first per the OPS-005 release checklist (T06.13). Adding a second refusal site would force a second copy of the wording, doubling the drift surface. |
| **Future macOS landing** | When DOC-OQ9's macOS follow-up ships (MIG-003 / T06.15, target 2026-Q3), the precheck is amended to accept `"Darwin"` and `NON_LINUX_REFUSAL_TEMPLATE` is renamed / re-scoped. Until then this artifact + the `decisions.md` §"AC1 Closure" section are the canonical authority on the platform restriction. |

## AC1 resolution

| AC | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| AC1 | OPEN (roadmap row 353, M6 docs lane) | **RESOLVED — 2026-05-20** | v1 is Linux-only. Declaration sites: `README.md` §"Platform support" (operator-facing) + `decisions.md` §"AC1 Closure" (ADR-level) + DOC-OQ9 closure (R6, macOS deferral) + AC2 closure (R9, local-only deferral). Enforcement site: `superclaude eval doctor` non-Linux refusal in `src/superclaude/cli/eval/commands.py` (exits 2 with `NON_LINUX_REFUSAL_TEMPLATE` on stderr before any capability gates run). macOS support is deferred to v2 under MIG-003 / R-116 / T06.15. |

AC1 is an Acceptance Criterion, not an Open Question; it is therefore
not enumerated in the SC5 OQ-1..OQ-10 ledger (T06.09). The SC5 ledger
nevertheless consumes this closure together with AC2 and DOC-OQ9 as the
v1 scope-boundary attestation that closes the platform + execution-
context commitments for the M6 exit checkpoint.

## Cross-references

| Reference | Where | Why |
|---|---|---|
| **DOC-OQ9 (macOS deferral)** | `decisions.md` R6 / §"DOC-OQ9 Closure" | DOC-OQ9 names the macOS follow-up plan with owner + target date; AC1 is the reciprocal "what v1 IS" to DOC-OQ9's "what v1 IS NOT". The cross-link is intentionally redundant — a maintainer editing one without the other produces drift that the T06.09 SC5 sweep catches. |
| **AC2 (local-only deferral)** | `decisions.md` R9 / §"AC2 Closure" | AC2 names the CI integration deferral and the local-only execution-context restriction. AC1 + AC2 together bound v1 on two orthogonal axes (platform + execution context). Both closures cite each other to close the "Linux + GitHub Actions" / "macOS local" loophole. |
| **MIG-003 (v2 platform follow-up)** | Roadmap row 360 / R-116, owned by T06.15 | MIG-003 is the canonical v2 follow-up roadmap entry consolidating macOS + CI as deferred scope. T06.15 inherits AC1 verbatim as the v1 platform boundary it defers past. |
| **OPS-005 release checklist** | `docs/eval/release-checklist.md` (added by T06.13) | OPS-005 walks the v1 release evidence; the README §"Platform support" section + the `eval doctor` non-Linux refusal are checklist items. |

## README declaration

`README.md` §"Platform support" (added by this task) enumerates:

1. **Supported:** Linux.
2. **macOS / Windows:** Non-goal for v1; `eval doctor` refuses with a
   friendly error citing AC1 (R-109) and exits 2 before running any
   capability gates. The rest of the `superclaude` CLI (sprint, roadmap,
   tasklist, audit) is unaffected.
3. **CI:** Non-goal for v1, cross-referencing AC2; the harness ships no
   GitHub Actions workflow and no `--ci` flag.

The README section cross-links the AC1, DOC-OQ9, and AC2 closure
sections in `decisions.md` so an operator who only reads the README can
still find the ADR log entries that authorise the policy.

## `eval doctor` refusal wire-up

The refusal lands in `src/superclaude/cli/eval/commands.py` (the
`doctor` Click command body) ahead of every other precondition check:

```python
system = _default_platform_probe()
if system != "Linux":
    click.echo(
        NON_LINUX_REFUSAL_TEMPLATE.format(system=system),
        err=True,
    )
    sys.exit(HARD_FAIL_EXIT_CODE)
```

`_default_platform_probe` defaults to `platform.system()` and is
re-bindable by the test suite so the Darwin/Windows refusal branches
can be exercised on a Linux CI box without faking `os.uname()`.
`NON_LINUX_REFUSAL_TEMPLATE` is a module-level string whose `{system}`
placeholder is filled by `platform.system()`'s return value (rendered
with `repr()` semantics so the operator sees the literal token they
have to convert into an issue tracker filter).

## Test coverage

Four new tests in `tests/cli/eval/test_doctor.py`:

1. `test_cli_doctor_refuses_non_linux_with_friendly_message` — Darwin
   monkey-patched into `_default_platform_probe`; assertion that
   `result.exit_code == HARD_FAIL_EXIT_CODE`, that stderr contains the
   `unsupported platform: 'Darwin'`, `Linux-only for v1`, `AC1`, and
   `DOC-OQ9` tokens, and that the capability checklist text
   (`superclaude eval doctor:`) is NOT rendered (refusal short-circuits).
2. `test_cli_doctor_refuses_windows_platform` — Windows on the same
   code path with `--json`; assertion that `result.stdout == ""` (the
   refusal must not emit a JSON payload that a downstream pipe could
   mis-parse).
3. `test_cli_doctor_linux_platform_proceeds` — Linux runs the existing
   happy path (regression check that the precheck is a no-op).
4. `test_non_linux_refusal_template_cites_ac1_and_doc_oq9` — locks the
   friendly-error string to the AC1 / R-109 / DOC-OQ9 / decisions.md
   tokens so a future refactor cannot quietly drop the ADR citations.

All four pass on the final tree (see `evidence/T06.07/summary.md`).

## Acceptance-criteria → site map (T06.07)

| AC bullet (T06.07) | Where satisfied |
|--------------------|-----------------|
| File `README.md` documents Linux-only v1 scope at the eval CLI section. | `README.md` §"Platform support" — new section enumerating Supported / macOS-Windows / CI status with cross-links to the AC1, DOC-OQ9, AC2 closures in `decisions.md`. |
| `eval doctor` on non-Linux platform (or stubbed `platform.system()=="Darwin"`) exits with a friendly error. | `src/superclaude/cli/eval/commands.py` — `doctor` Click command's first action is `_default_platform_probe()` followed by `NON_LINUX_REFUSAL_TEMPLATE.format(system=...)` on stderr + `sys.exit(HARD_FAIL_EXIT_CODE)`. Test coverage in `tests/cli/eval/test_doctor.py`. |
| decisions.md `AC1` entry status is `resolved`. | `.dev/releases/current/cliEval/decisions.md` §"AC1 Closure" §"Closure of AC1": `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0110/spec.md` records the platform policy. | This file. |

## Out of scope for T06.07

- Writing the v2 follow-up roadmap entry consolidating macOS + CI scope
  — owned by T06.15 (MIG-003).
- Adding a platform precheck to `eval run`, `eval list`, or `eval
  describe` — out of scope at v1; operators are documented to run
  `eval doctor` first per the OPS-005 release checklist (T06.13).
- Changing the harness exit-code surface (introducing a dedicated
  `NON_LINUX_EXIT_CODE`) — explicitly rejected; the refusal reuses
  `HARD_FAIL_EXIT_CODE` per the Decision table above.
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for
  AC1 row 353.
- Editing `design-spec.md` — the Linux-only commitment is already
  recorded there (lines 30 and 812); AC1 closure ratifies it in the
  ADR log + README + code, it does not change the design spec.
- Closing other M6 ACs (AC11 source-of-truth gate closed earlier at
  T01.20; AC2 closure owned by T06.05).
