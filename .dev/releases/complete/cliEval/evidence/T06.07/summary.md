# T06.07 — Evidence Summary

**Task:** T06.07 — AC1 Linux-only declaration in README + decisions
**Phase:** 6 (Docs ADRs Hardening Sync Platform)
**Deliverable:** D-0110
**Date:** 2026-05-20
**Result:** PASS

## Deliverable

`README.md` declares Linux-only v1 scope at the eval CLI section;
`eval doctor` refuses to run on non-Linux platforms with a friendly
error message that cites AC1 / R-109 / DOC-OQ9; `decisions.md` AC1
closure section records the platform policy with `RESOLVED — 2026-05-20`
status; per-deliverable spec at `artifacts/D-0110/spec.md`.

## Acceptance criteria — verification

| AC bullet (T06.07) | Status | Evidence |
|--------------------|--------|----------|
| File `README.md` documents Linux-only v1 scope at the eval CLI section. | PASS | `README.md` §"Platform support" enumerates Supported=Linux, NON-GOAL=macOS/Windows, NON-GOAL=CI; cross-links AC1/DOC-OQ9/AC2 closures. |
| `eval doctor` on non-Linux platform (or stubbed `platform.system()=="Darwin"`) exits with a friendly error. | PASS | `src/superclaude/cli/eval/commands.py` precheck calls `_default_platform_probe()`, emits `NON_LINUX_REFUSAL_TEMPLATE`, exits `HARD_FAIL_EXIT_CODE (=2)`. `tests/cli/eval/test_doctor.py` covers Darwin + Windows refusal and Linux happy-path regression — 4 new tests; full file 48/48 PASS. |
| `decisions.md` `AC1` entry status is `resolved`. | PASS | `decisions.md` §"AC1 Closure" §"Closure of AC1" subsection: `Resolution status: RESOLVED — 2026-05-20`. |
| `TASKLIST_ROOT/artifacts/D-0110/spec.md` records the platform policy. | PASS | File exists; contains AC1 contract, platform-policy table, AC1 resolution row, AC1↔DOC-OQ9↔AC2 cross-references, AC site map, refusal-message wire-up summary, test coverage list. |

## Verification commands re-run on the final tree (2026-05-20)

```
$ grep -c '^## AC1 Closure' .dev/releases/current/cliEval/decisions.md
1

$ grep -E '^- R10 \(2026-05-20\)' .dev/releases/current/cliEval/decisions.md
- R10 (2026-05-20): AC1 closure (T06.07) — Linux-only v1 platform scope declared in `README.md` §"Platform support"; `eval doctor` refuses non-Linux platforms with a friendly message citing AC1, R-109, and DOC-OQ9; the refusal exits with `HARD_FAIL_EXIT_CODE` (=2). AC2 (local-only) and DOC-OQ9 (macOS deferral) cross-referenced. AC1 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0110/spec.md`.

$ grep -E '^## Platform support' README.md
## Platform support

$ grep -E 'eval doctor: unsupported platform' src/superclaude/cli/eval/commands.py
    "eval doctor: unsupported platform: {system!r}. "

$ uv run pytest tests/cli/eval/test_doctor.py
... 48 passed in 0.22s
```

## Files modified

- `src/superclaude/cli/eval/commands.py` — `import platform`;
  `NON_LINUX_REFUSAL_TEMPLATE` constant; `_default_platform_probe()`
  helper; platform precheck as first action in `doctor` Click command
  (before scratch-root validation).
- `src/superclaude/cli/eval/__init__.py` — re-export
  `NON_LINUX_REFUSAL_TEMPLATE`.
- `tests/cli/eval/test_doctor.py` — 4 new tests: Darwin refusal,
  Windows refusal (`--json` stdout empty), Linux proceeds, template
  ADR-token lock-string.
- `README.md` — added §"Platform support" between Requirements and
  License.
- `.dev/releases/current/cliEval/decisions.md` — R10 revision; added
  §"AC1 Closure" section after §"AC2 Closure".

## Files created

- `.dev/releases/current/cliEval/artifacts/D-0110/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0110/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0110/evidence.md`
- `.dev/releases/current/cliEval/evidence/T06.07/summary.md` (this file)

## AC1 status

Roadmap row 353 (AC1 / R-109) — **SATISFIED.** Both AC elements
("README documents Linux-only v1 scope; `eval doctor` non-Linux
refusal message") are landed by this task.

## Dependencies satisfied

- T06.05 (AC2 closure, local-only v1) — referenced by AC1 closure as
  the paired v1 scope-envelope axis (platform × execution context).
- DOC-OQ9 closure (R6, macOS deferral) — referenced by README and
  refusal message as the v2 deferral pointer for macOS users.

## Downstream unblocked

- T06.08 checkpoint (Phase 6 / T06-T10) can now mark T06.07 PASS.
- T06.09 (SC5 OQ-1..OQ-10 ledger) reads AC1+AC2 closures together as
  the v1 scope-boundary attestation paired with the OQ ledger.
- T06.13 (OPS-005 release checklist) inherits "Linux only" alongside
  "local-only" as v1 release-notes headlines.
- T06.15 (MIG-003 v2 follow-up roadmap entry) inherits AC1 + DOC-OQ9
  as the consolidated macOS-support v2 scope item.
