# D-0110 — Evidence

## Direct verification commands

```bash
# 1) Confirm AC1 Closure section header exists in decisions.md
grep -nE '^## AC1 Closure' .dev/releases/current/cliEval/decisions.md

# 2) Confirm RESOLVED status line lands on 2026-05-20
grep -nE 'Resolution status: RESOLVED — 2026-05-20' \
  .dev/releases/current/cliEval/decisions.md

# 3) Confirm DOC-OQ9 cross-reference (R6 / row 349 / R-105 / T06.02)
grep -nE 'DOC-OQ9.*(R6|row 349|R-105|T06\.02)' \
  .dev/releases/current/cliEval/decisions.md

# 4) Confirm AC2 cross-reference (R9 / row 352 / R-108 / T06.05)
grep -nE 'AC2.*(R9|row 352|R-108|T06\.05)' \
  .dev/releases/current/cliEval/decisions.md

# 5) Confirm MIG-003 cross-reference (R-116 / row 360 / T06.15)
grep -nE 'MIG-003.*(R-116|row 360|T06\.15)' \
  .dev/releases/current/cliEval/decisions.md

# 6) Confirm R10 revision-log entry recorded
grep -nE '^- R10 \(2026-05-20\): AC1 closure' \
  .dev/releases/current/cliEval/decisions.md

# 7) Confirm README §"Platform support" landed
grep -nE '^## Platform support' README.md

# 8) Confirm README cites AC1 / R-109
grep -nE 'AC1.*R-109|Linux-only for v1' README.md

# 9) Confirm doctor wires the platform precheck (code-level)
grep -nE '_default_platform_probe|NON_LINUX_REFUSAL_TEMPLATE' \
  src/superclaude/cli/eval/commands.py

# 10) Confirm friendly-error template cites AC1 + DOC-OQ9 + decisions.md
grep -nE 'AC1.*roadmap R-109|DOC-OQ9 closure|decisions\.md' \
  src/superclaude/cli/eval/commands.py

# 11) Run the four new doctor tests
uv run pytest tests/cli/eval/test_doctor.py -v -k \
  "non_linux or linux_platform_proceeds or windows or template_cites"

# 12) Full doctor regression check (48 tests)
uv run pytest tests/cli/eval/test_doctor.py
```

Expected: each grep returns at least one match; both pytest commands
exit 0.

## Per-AC verification

| AC bullet (T06.07) | Verification step | Result |
|--------------------|-------------------|--------|
| File `README.md` documents Linux-only v1 scope at the eval CLI section. | `grep -nE '^## Platform support' README.md` + visual review of the new section. | PASS — §"Platform support" section landed, names Supported/macOS-Windows/CI status, cross-links AC1/DOC-OQ9/AC2 closures by relative path. |
| `eval doctor` on non-Linux platform exits with a friendly error. | `uv run pytest tests/cli/eval/test_doctor.py -v -k "non_linux or windows or template_cites"` exercises the Darwin and Windows refusal branches via `monkeypatch.setattr(doctor_module, "_default_platform_probe", lambda: "Darwin"/"Windows")`. | PASS — 4/4 tests pass; Darwin returns `HARD_FAIL_EXIT_CODE`, stderr contains the four AC tokens (`AC1`, `R-109`, `DOC-OQ9`, `decisions.md`), capability checklist is NOT rendered; `--json` does NOT emit a payload. |
| decisions.md `AC1` entry status is `resolved`. | `grep -nE 'Resolution status: RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md` + visual review of §"AC1 Closure". | PASS — §"AC1 Closure" §"Closure of AC1" subsection records `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0110/spec.md` records the platform policy. | File exists with Decision table + AC1 resolution table + DOC-OQ9 / AC2 / MIG-003 cross-references + AC site map + test-coverage summary. | PASS — `artifacts/D-0110/spec.md` written this commit. |

## AC1 resolution evidence

`decisions.md` §"AC1 Closure" §"Closure of AC1":

> - **Question:** Is the cliEval harness Linux-only at v1, and if so,
>   where is the declaration recorded and how is the policy enforced?
> - **Resolution:** Yes — v1 is Linux-only. Declaration sites:
>   `README.md` §"Platform support" (operator-facing) + this
>   `decisions.md` §"AC1 Closure" (ADR-level) + DOC-OQ9 closure (R6,
>   macOS deferral) + AC2 closure (R9, local-only deferral).
>   Enforcement site: `superclaude eval doctor` non-Linux refusal in
>   `src/superclaude/cli/eval/commands.py` (exits 2 with
>   `NON_LINUX_REFUSAL_TEMPLATE` on stderr before any capability gates
>   run). macOS support is deferred to v2 under MIG-003 / R-116 /
>   T06.15.
> - **Resolution status:** RESOLVED — 2026-05-20.

## DOC-OQ9 cross-reference evidence

`decisions.md` §"AC1 Closure" §"Cross-reference to DOC-OQ9 (macOS
follow-up plan)":

> DOC-OQ9 closure (R6 above, roadmap row 349, R-105, owned by T06.02)
> records the macOS follow-up plan with owner RyanW and target date
> 2026-Q3. AC1 is the reciprocal: AC1 declares what v1 IS (Linux-only);
> DOC-OQ9 declares what v1 IS NOT (macOS) and names the owner + target
> window for the deferred capability.

## AC2 cross-reference evidence

`decisions.md` §"AC1 Closure" §"Cross-reference to AC2 (local-only
declaration)":

> AC2 closure (R9 above, roadmap row 352, R-108, owned by T06.05)
> records the CI integration deferral and the local-only execution-
> context restriction. AC1 + AC2 together bound v1 on two orthogonal
> axes: AC1 restricts the platform (Linux), AC2 restricts the
> execution context (local developer machines, no CI).

## MIG-003 cross-reference evidence

`decisions.md` §"AC1 Closure" §"Cross-reference to MIG-003 (v2
platform follow-up plan)":

> MIG-003 (R-116, roadmap row 360, owned by T06.15) is the canonical v2
> follow-up roadmap entry that names both macOS support and CI
> integration as deferred scope. AC1 lands the platform half of the v1
> scope envelope; DOC-OQ9 inherits AC1 verbatim as the v1 boundary it
> defers past; AC2 lands the execution-context half.

## Refusal text evidence

`src/superclaude/cli/eval/commands.py`:

```python
NON_LINUX_REFUSAL_TEMPLATE: str = (
    "eval doctor: unsupported platform: {system!r}. "
    "The cliEval harness ships Linux-only for v1 (AC1, roadmap R-109). "
    "macOS support is deferred to v2 — see DOC-OQ9 closure in "
    ".dev/releases/current/cliEval/decisions.md."
)
```

Rendered with `system="Darwin"`:

> `eval doctor: unsupported platform: 'Darwin'. The cliEval harness
> ships Linux-only for v1 (AC1, roadmap R-109). macOS support is
> deferred to v2 — see DOC-OQ9 closure in
> .dev/releases/current/cliEval/decisions.md.`

## Test-run evidence

`uv run pytest tests/cli/eval/test_doctor.py -v -k "non_linux or
linux_platform_proceeds or windows or template_cites"`:

```
tests/cli/eval/test_doctor.py::test_cli_doctor_refuses_non_linux_with_friendly_message PASSED [ 25%]
tests/cli/eval/test_doctor.py::test_cli_doctor_refuses_windows_platform PASSED [ 50%]
tests/cli/eval/test_doctor.py::test_cli_doctor_linux_platform_proceeds PASSED [ 75%]
tests/cli/eval/test_doctor.py::test_non_linux_refusal_template_cites_ac1_and_doc_oq9 PASSED [100%]

======================= 4 passed, 44 deselected in 0.22s =======================
```

`uv run pytest tests/cli/eval/test_doctor.py`:

```
============================== 48 passed in 0.22s ==============================
```

## AC1 acceptance crosscheck

Roadmap row 353 (AC1 / R-109) AC: *"Linux-only declared in README;
`eval doctor` refuses non-Linux platforms with a friendly error."*

| AC element | Satisfied at |
|------------|--------------|
| "Linux-only declared in README" | `README.md` §"Platform support" — three-clause enumeration (Supported / macOS-Windows / CI) with cross-links to AC1, DOC-OQ9, AC2 closures. |
| "`eval doctor` refuses non-Linux platforms with a friendly error" | `src/superclaude/cli/eval/commands.py` — `doctor` Click command runs `_default_platform_probe()` first and renders `NON_LINUX_REFUSAL_TEMPLATE.format(system=...)` on stderr + `sys.exit(HARD_FAIL_EXIT_CODE)` when the value is not `"Linux"`. Tests in `tests/cli/eval/test_doctor.py` exercise Darwin, Windows, and the Linux happy path. |

Both AC elements satisfied.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.07/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R10, §"AC1 Closure")
- Companion spec: `artifacts/D-0110/spec.md`
- Design rationale: `artifacts/D-0110/notes.md`
- Code: `src/superclaude/cli/eval/commands.py` (platform precheck +
  `NON_LINUX_REFUSAL_TEMPLATE` + `_default_platform_probe`)
- Tests: `tests/cli/eval/test_doctor.py` (4 new tests)
- README: `README.md` §"Platform support"
- Downstream consumers:
  - T06.09 (SC5 OQ-1..OQ-10 ledger; reads AC1+AC2+DOC-OQ9 closures
    together as the v1 scope-boundary attestation)
  - T06.13 (OPS-005 release checklist; carries "Linux only" as v1
    release-notes headline and walks the `eval doctor` non-Linux
    refusal as a checklist item)
  - T06.15 (MIG-003 v2 follow-up roadmap entry; consolidates macOS
    + CI deferrals without re-deriving the AC1 v1 commitment)
  - T06.16 (M6 exit checkpoint; reads AC1 closure as one of the five
    SC1-SC5 satisfaction sites)
