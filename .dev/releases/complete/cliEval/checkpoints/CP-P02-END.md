# CP-P02-END — Phase 2 / M2 exit gate

**Task:** T02.27 (Phase 2, Roadmap R-023..R-044)
**Covers:** T02.01..T02.26
**Generated:** 2026-05-20
**status: FAIL**

## Summary

Phase 2 cannot exit M2 in the literal sense: two of the four prior
mid-phase checkpoints are still **FAIL** and one of the three M2 exit
criteria is unmet on the live tree.

1. `CP-P02-T01-T05.md` remains **FAIL** because T02.01 (NFR-MAINT1
   physical vendoring of the ptytest fork) has not landed. The
   directory `src/superclaude/cli/eval/pty/` still contains only
   `CHECKLIST.md` (6 194 B) and `PROVENANCE.md` (4 162 B); the upstream
   MIT `LICENSE` is absent, no ptytest module sources are present,
   `from superclaude.cli.eval.pty import pexpect` is unreachable,
   `tests/cli/eval/test_pty_vendor.py` does not exist, and
   `artifacts/D-0023/` + `evidence/T02.01/` are both missing. The
   `PROVENANCE.md` §2 rows `Vendoring date` and `Vendoring commit`
   still read `TBD — set by T02.01 on physical landing of sources`.
   This blocks the M2 exit verification bullet "PROVENANCE.md records
   the vendored ptytest SHA and quarterly review cadence" at the
   "vendored ptytest SHA" half — the SHA `61a4687…1aa5f` is *pinned*
   in PROVENANCE.md §2, but the *sources it points to* have never
   landed, so the cross-reference resolves to a phantom.
2. `CP-P02-T19-T23.md` remains **FAIL** because
   `uv run ruff check src/superclaude/cli/eval/` exits **1** with
   **16 errors** (11× N818, 3× F401, 1× I001, 1× TID252) — one more
   than the 15 errors reported in `CP-P02-T19-T23.md` because T02.25
   introduced an additional F401 (`.config.SCRATCH_ROOT_POLICY`
   imported but unused) on top of the latent Phase 2 hygiene cluster.
   The T02.27 exit criterion `uv run ruff check
   src/superclaude/cli/eval/ exits 0` is therefore NOT MET on the
   current tree.

The remaining mid-phase gates `CP-P02-T07-T11.md` and
`CP-P02-T13-T17.md` are PASS; T02.25 (OPS-002 scratch root policy
across config/isolation/CLI) and T02.26 (R5-mit quarterly drift
checklist) both landed with PASSing tier-proportional checks
(`tests/cli/eval/test_scratch_root_policy.py` → 16 passed in 0.14 s;
`src/superclaude/cli/eval/pty/CHECKLIST.md` carries the AC10 + R5-mit
header, 5-step procedure, owner RyanW, and the next two quarterly
review dates 2026-08-20 and 2026-11-20).

The behavioural M2 contract — HomeIsolation refuses any HOME outside
`EvalConfig.allowed_scratch_roots`, PtyDriver spawns the real `claude`
binary against the dev host and captures its exit code via
`ClaudeProcessAdapter`, and the `anthropic` SDK ban-import lint rule
is wired and active — is **met at the test level**:
`uv run pytest tests/cli/eval/ -v` → **690 passed in 8.18 s, exit 0**
on 2026-05-20, including the 30 TEST-002 containment cases, the 14
TEST-003 symlink-attack cases, the 6 NFR-SEC3 hard-guard cases against
the materialized real `~/.claude/`, the 13-test ClaudeProcessAdapter
suite, the 21-test PtyDriver suite with the `test_real_claude_help_smoketest`
real-subprocess assertion, and the 30-test PtyStream ANSI/buffer
suite. But "behavioural pass" is not enough to flip the gate when the
literal M2 entry blocker (T02.01 vendoring) and the literal exit
criterion (ruff exit 0) are both still red — and especially when
PtyDriver currently imports its `pexpect` through the
`except ImportError: import pexpect as _pexpect  # pragma: no cover -
exercised until T02.01 lands sources` fallback in
`src/superclaude/cli/eval/pty_driver.py`, not from the vendored
floor that NFR-MAINT1 requires.

The remediation scope is bounded to two work items (T02.01 vendoring
+ Phase 2 lint hygiene) plus the carry-forward QE-review documentation
backfill from `CP-P02-T07-T11.md` *Follow-ups* §1 / `CP-P02-T19-T23.md`
*Follow-ups* §2 (T02.09, T02.10, T02.21, T02.22). All four can land
in a single remediation slice; see *Required remediation* below.

## Per-upstream-task status

| Task   | Roadmap | Deliverable | Status | Notes |
|--------|---------|-------------|--------|-------|
| T02.01 | R-023   | D-0023      | **FAIL** | NFR-MAINT1 vendoring not landed. `src/superclaude/cli/eval/pty/` contains only `CHECKLIST.md` + `PROVENANCE.md` (from T02.03 and T02.26); upstream MIT `LICENSE` absent; no ptytest module sources; `tests/cli/eval/test_pty_vendor.py` does not exist; `artifacts/D-0023/` and `evidence/T02.01/` absent. PROVENANCE.md §2 rows `Vendoring date` + `Vendoring commit` still read `TBD`. PtyDriver currently runs against the system-installed `pexpect` via the `ImportError` fallback at `src/superclaude/cli/eval/pty_driver.py:54`, not against the vendored floor. **Blocks M2 exit.** Carried forward from `CP-P02-T01-T05.md`. |
| T02.02 | R-024   | D-0024      | PASS   | `NOTICE` at repo root references ptytest LICENSE (`grep -c ptytest NOTICE` → 4, exit 0). D-10 ADR recorded in `decisions.md` with OQ-4 flipped from OPEN to RESOLVED. |
| T02.03 | R-025   | D-0025      | PASS   | `PROVENANCE.md` pins fork SHA `61a46870e38710c7cfc95f00cefbf0499111aa5f`, records `Quarterly` cadence, names review owner RyanW, anchors next-review date 2026-08-20. `CHECKLIST.md` provides the 5-step review procedure. Cross-reference resolves to a phantom until T02.01 lands sources. |
| T02.04 | R-026   | D-0026      | PASS   | `HomeIsolation` frozen dataclass with the 4 DM-006 fields (eval_id, home_root, session_id, time_offset_sec; default `time_offset_sec=0`). `__post_init__` delegates to `validate_eval_id`. 32 tests in `test_isolation_dataclass.py` PASS. |
| T02.05 | R-027   | D-0027      | PASS   | `tests/cli/eval/test_isolation_layers_probe.py` pins the IsolationLayers API surface (13 tests, read-only). Re-runs green after the T02.07 HomeIsolation extension. |
| T02.06 | -       | D-CP02-MID-T01-T05 | **FAIL** | `CP-P02-T01-T05.md` records `status: FAIL` (T02.01 outstanding). |
| T02.07 | R-028   | D-0028      | PASS   | FR-ISO1 HomeIsolation extension landed in `src/superclaude/cli/eval/isolation.py` (`setup`, `env`, `teardown(keep)`, `state_path(suffix)` + `home_path` property + `is_set_up` predicate). 83 tests PASS. Probe re-runs green post-extension. |
| T02.08 | R-029   | D-0029      | PASS   | FR-ISO2 path containment guard with the 3-check sequence integrated into `HomeIsolation.setup()` AFTER mkdtemp / BEFORE hook deploy. QE-review completed with PASS verdict on the Issue #1 home_root-injection blocker (`config` promoted to required arg). 85 tests PASS. |
| T02.09 | R-030   | D-0030      | PASS   | NFR-SEC2 defense-in-depth tests covering all 4 attack vectors + coverage-matrix pin (19 tests PASS). QE-review documentation gap — see *Follow-ups* §3. |
| T02.10 | R-031   | D-0031      | PASS   | NFR-SEC3 hard-guard tests refuse HOME resolving to the real `~/.claude/` (materialized at `/config/.claude/` on dev host); 6 tests PASS, none skipped. QE-review documentation gap + per-task `evidence.md` missing — see *Follow-ups* §3 and §4. |
| T02.11 | R-032   | D-0032      | PASS   | COMP-006 HomeIsolation integrated component pin (27 tests PASS). DM-006 invariants survive integration. |
| T02.12 | -       | D-CP02-MID-T07-T11 | PASS | `CP-P02-T07-T11.md` exists at `status: PASS`. |
| T02.13 | R-033   | D-0033      | PASS   | NFR-ISO2 atomic try/except wrapper inside `HomeIsolation.setup()`: partial HOME preserved + `setup_failed` tag at `<home>/.eval-meta/setup_failed`, no tag on containment violation (harness-bug vs eval-failure distinction). 19 tests PASS. Mock-EvalRunner buckets failures as `ERRORED`. |
| T02.14 | R-034   | D-0034      | PASS   | COMP-014 `deploy_hooks_to(home_path)` adapter at `src/superclaude/cli/eval/hook_adapter.py` invoking `install_hooks` with `target_dir=home_path`. Idempotent on re-invocation (SHA256 byte-equality assertion). `HookDeployFailed` raised with kebab-case `error_tag` on adapter failure. 12 tests PASS. |
| T02.15 | R-035   | D-0035      | PASS   | NFR-PERF1 perf baseline: 15-parallel × 30 iter (n_samples=450) → **p50 = 1.557 ms, p95 = 3.671 ms** on dev host, three orders of magnitude under the 2.0 s/eval p50 budget. Report `evidence/T02.15/perf.json` with `schema_version=1`. |
| T02.16 | R-036   | D-0036      | PASS   | COMP-007 `PtyDriver` wraps `pexpect.spawn` with the 5-method surface; `test_real_claude_help_smoketest` confirms spawn + exit capture against the real `claude --help` binary. 21 tests PASS. **NB:** `pexpect` is currently imported via the system fallback at `pty_driver.py:54` until T02.01 lands the vendored sources; the F401 `pexpect as _pexpect_module` under `TYPE_CHECKING` is a direct side-effect of this provisional wiring. |
| T02.17 | R-037   | D-0037      | PASS   | COMP-011 `PtyStream` ANSI/buffer layer: ANSI/CSI/OSC/C1 stripping, line-buffered iteration with CRLF normalisation, `PtyTimeout` on stalled read, end-to-end test against `PtyDriver`. 30 tests PASS. |
| T02.18 | -       | D-CP02-MID-T13-T17 | PASS | `CP-P02-T13-T17.md` exists at `status: PASS`. |
| T02.19 | R-038   | D-0038      | PASS   | COMP-013 `ClaudeProcessAdapter` reuse adapter spawning the real `claude` subprocess with `cwd` pinned + `HomeIsolation.env()` injected + stdout/stderr separated; FR-G1 `anthropic` ban-import lint rule wired in `pyproject.toml` `[tool.ruff.lint.flake8-tidy-imports.banned-api]` and probed live (3× TID251 fires). 13 tests PASS. |
| T02.20 | R-039   | D-0039      | PASS   | R1-mit `_check_claude_version()` floor at 0.5.0 sourced from `EvalConfig.min_claude_version` (no hard-coded constant); 0.4.0 stub rejected with exit 2; floor honoured at boundary. 47 supporting tests PASS. |
| T02.21 | R-040   | D-0040      | PASS   | TEST-002 first-class containment test deliverable (30 tests PASS across 4 nested classes + slice-coverage probe). QE-review documentation gap — see *Follow-ups* §3. |
| T02.22 | R-041   | D-0041      | PASS   | TEST-003 first-class symlink-attack test deliverable (14 tests PASS across 5 nested classes); refusal occurs AFTER mkdtemp and BEFORE hook deploy. QE-review documentation gap — see *Follow-ups* §3. |
| T02.23 | R-042   | D-0042      | PASS   | TEST-004 capability gate test deliverable: HARD / SOFT-SKIP / SOFT-XFAIL classifications + `--no-mcp` behaviour + distinct doctor render strings per classification (20 tests PASS). |
| T02.24 | -       | D-CP02-MID-T19-T23 | **FAIL** | `CP-P02-T19-T23.md` records `status: FAIL` (16 ruff violations under `src/superclaude/cli/eval/`). |
| T02.25 | R-043   | D-0043      | PASS   | OPS-002 scratch root policy enforced across `EvalConfig` / `containment_guard` / `eval doctor --output-dir`. Policy doc at `docs/eval/scratch-roots.md` names `/tmp/eval-runs/`, repo `.dev/eval-runs/`, `--output-dir`. Doctor failure message quotes the policy verbatim on `--output-dir /etc/foo` rejection. `EvalConfig.allowed_scratch_roots` remains single source of truth. 16 tests in `test_scratch_root_policy.py` PASS. |
| T02.26 | R-044   | D-0044      | PASS   | R5-mit quarterly ptytest drift review checklist landed at `src/superclaude/cli/eval/pty/CHECKLIST.md` with the AC10 + R5-mit header, 5-step procedure (carried from T02.03), owner RyanW, next 2 review dates 2026-08-20 and 2026-11-20. |

**Roll-up:** 22 tasks landed PASS (T02.02..T02.05, T02.07..T02.11,
T02.13..T02.17, T02.19..T02.23, T02.25, T02.26), 1 task FAIL (T02.01),
2 mid-phase checkpoints PASS (T02.12, T02.18), 2 mid-phase checkpoints
FAIL (T02.06, T02.24).

## Verification (2/3 confirmed)

1. **HomeIsolation refuses any HOME outside
   `EvalConfig.allowed_scratch_roots`** — CONFIRMED.
   - T02.21 (TEST-002, `test_containment.py`) → 30 PASS: repo
     `.dev/eval-runs/` and `/tmp/eval-runs/` accepted; `~/.claude/`,
     `/etc/foo`, `/var/lib/eval-runs/`, `/root/.claude/`,
     `/tmp/other-runs/` rejected; narrowed allowlist rejects even
     canonical `/tmp/eval-runs/`; loader-bypass rejected (9 unsafe-id
     parametrise + `__post_init__`-disabled probe); exit-code-2 path
     covered for both `InvalidEvalId` and `ScratchRootViolation`.
   - T02.10 (NFR-SEC3 hard-guard, `test_hard_guard_real_home.py`) →
     6 PASS, none skipped: real-`~/.claude/`-as-home refused;
     scratch-root symlink into real `~/.claude/` refused;
     per-eval-home symlink into real `~/.claude/` refused. The
     materialized real HOME on the dev host
     (`Path.home() / ".claude"` → `/config/.claude/`) is exercised,
     not stubbed.
   - T02.25 (OPS-002) closes the cross-cutting policy: doctor exits
     non-zero with the policy text quoted verbatim when
     `--output-dir /etc/foo` is supplied.
   - Evidence: `evidence/T02.27/exit-criteria-pytest.log`,
     `evidence/T02.21/pytest-T02.21.log`,
     `evidence/T02.10/pytest-T02.10.log`,
     `evidence/T02.25/pytest-T02.25.log`.

2. **PtyDriver spawns real claude against a 1-eval suite and captures
   exit code via ClaudeProcessAdapter** — CONFIRMED.
   - T02.16 (`test_pty_driver.py`) → 21 PASS, including
     `test_real_claude_help_smoketest` which spawns the real
     `claude --help` binary through `pexpect.spawn` and asserts the
     captured exit code from `wait_exit()`.
   - T02.19 (`test_claude_process_adapter.py`) → 13 PASS, including
     `test_spawn_invokes_real_subprocess_not_anthropic_sdk`,
     `test_spawn_pins_child_cwd_to_adapter_cwd`,
     `test_spawn_injects_home_isolation_env_into_child`,
     `test_spawn_separates_stdout_and_stderr_to_distinct_files`.
   - FR-G1 reinforced by the ban-import lint rule landed in T02.19:
     `pyproject.toml` `[tool.ruff.lint.flake8-tidy-imports.banned-api]`
     rejects `anthropic`, `anthropic.Anthropic`, and
     `anthropic.AsyncAnthropic`; synthetic probe fires 3× TID251
     (`evidence/T02.19/ruff-probe.log`); `grep -rE '^(from anthropic|
     import anthropic)' src/superclaude/cli/eval/` returns no matches.
   - **Caveat:** the `pexpect` floor invoked by `PtyDriver` is the
     system installation, not the vendored fork — see verification
     bullet 3.
   - Evidence: `evidence/T02.27/exit-criteria-pytest.log`,
     `evidence/T02.16/pytest-T02.16.log`,
     `evidence/T02.19/pytest.log`,
     `evidence/T02.19/grep-no-anthropic.log`.

3. **PROVENANCE.md records the vendored ptytest SHA and quarterly
   review cadence** — **NOT CONFIRMED** (SHA pin yes, vendored sources
   no).
   - `src/superclaude/cli/eval/pty/PROVENANCE.md` *§2 Fork SHA pin*
     pins the upstream SHA `61a46870e38710c7cfc95f00cefbf0499111aa5f`
     and records cadence `Quarterly`. The
     `src/superclaude/cli/eval/pty/CHECKLIST.md` lists the 5-step
     review procedure, names owner RyanW, and anchors the next two
     review dates (2026-08-20 and 2026-11-20).
   - **However:** §2 rows `Vendoring date` and `Vendoring commit`
     still read `TBD — set by T02.01 on physical landing of sources`,
     and the *Changes from upstream* subsection reads `*(Populated by
     T02.01 when the vendored sources land. …)* - TBD`. The directory
     contains no upstream MIT `LICENSE`, no `__init__.py`, and no
     ptytest module sources. The SHA pin therefore points to a
     phantom; the M2 entry blocker per `CP-P02-T01-T05.md` is still
     outstanding.
   - Evidence: `ls -la src/superclaude/cli/eval/pty/` → 2 files
     (`CHECKLIST.md`, `PROVENANCE.md`) only.

## Exit Criteria (1/3 met)

- `uv run pytest tests/cli/eval/ -v` passes for M2 modules — **MET**.
  - Actual: exit code **0**, **690 passed in 8.18s**, 0 failed, 0
    skipped, on 2026-05-20.
  - Evidence: `evidence/T02.27/exit-criteria-pytest.log`.
  - Note: this does not cover `tests/cli/eval/test_pty_vendor.py`
    because the file does not exist (T02.01 outstanding); the literal
    text of the criterion ("passes for M2 modules") is met for the
    modules that *exist*, but the M2 module set is incomplete.
- `uv run ruff check src/superclaude/cli/eval/` exits 0 — **NOT MET**.
  - Actual: exit code **1**, **16 errors** in 8 files under
    `src/superclaude/cli/eval/`:
    - **N818 × 11** — exception classes named without `Error` suffix:
      `SuiteNotFound` (`commands.py:554`), `EvalNotFound`
      (`commands.py:570`), `ScratchRootViolation` (`config.py:98`),
      `HookDeployFailed` (`hook_adapter.py:72`),
      `HomeContainmentViolation` (`isolation.py:162`),
      `InvalidEvalId` (`loader.py:108`), `UnresolvedCapability`
      (`loader.py:360`), `PtyDriverTimeout` (`pty_driver.py:81`),
      `PtyDriverNotStarted` (`pty_driver.py:85`), `PtyDriverEOF`
      (`pty_driver.py:89`), `PtyTimeout` (`pty_stream.py:109`). These
      are roadmap-mandated public contracts (FR-ISO2 →
      `HomeContainmentViolation`, COMP-014 → `HookDeployFailed`,
      COMP-011 → `PtyTimeout`, AC12 → `InvalidEvalId`, etc.); the
      correct remediation is `[tool.ruff.lint.per-file-ignores]` or
      `noqa: N818` pragmas, not a rename — see *Required remediation*
      §2 below.
    - **F401 × 3** — unused imports:
      `.config.SCRATCH_ROOT_POLICY` in `commands.py` (introduced by
      T02.25), `os` at `pty_driver.py:44`, `pexpect as
      _pexpect_module` at `pty_driver.py:50` (TYPE_CHECKING block).
      The third is a direct side-effect of the T02.01 vendoring gap
      — once T02.01 lands, the fallback import re-collapses and
      the placeholder can be removed.
    - **I001 × 1** — un-sorted import block at `pty_driver.py:53`.
    - **TID252 × 1** — relative parent-module import at
      `hook_adapter.py:59` (`from ..install_hooks import
      install_hooks`); surfaced by the FR-G1 `TID` selector that
      T02.19 added. Mechanical fix: switch to absolute import.
  - Carried forward from `CP-P02-T19-T23.md` *Follow-ups* §1, plus
    one new F401 introduced by T02.25.
  - Evidence: `evidence/T02.27/ruff-eval.log`.
- Checkpoint report `CP-P02-END.md` records pass/fail per task in
  Phase 2 — **MET** (this file, *Per-upstream-task status* table
  above).

## Required remediation before this checkpoint can flip to PASS

The remediation scope is bounded; both blockers are tractable inside
a single follow-up slice.

1. **Land T02.01 (NFR-MAINT1 physical vendoring of the ptytest
   fork).** Per the remediation block in `CP-P02-T01-T05.md`:
   - Copy the ptytest sources from upstream
     `brandon-fryslie/ptytest@61a46870e38710c7cfc95f00cefbf0499111aa5f`
     into `src/superclaude/cli/eval/pty/` with the upstream MIT
     `LICENSE` retained verbatim.
   - Pin `pexpect>=4.9` via vendored module imports so that
     `from superclaude.cli.eval.pty import pexpect` resolves and
     reports `pexpect.__version__ >= 4.9`.
   - Update `PROVENANCE.md` §2 rows `Vendoring date` + `Vendoring
     commit`, and populate the *Changes from upstream* subsection.
   - Add `tests/cli/eval/test_pty_vendor.py` exercising the vendored
     import + version floor + any local changes' contract.
   - Populate `artifacts/D-0023/{spec,notes,evidence}.md` and
     `evidence/T02.01/` with the vendoring plan, SHA pin alignment,
     and pytest log.
   - Remove the `except ImportError: import pexpect as _pexpect`
     fallback at `src/superclaude/cli/eval/pty_driver.py:54` and the
     associated `pexpect as _pexpect_module` placeholder import at
     line 50 (this also closes 1 of the 3 outstanding F401
     violations).
2. **Resolve the 16 `ruff check src/superclaude/cli/eval/`
   violations.** Recommended approach, single commit:
   - Edit `pyproject.toml` to add a
     `[tool.ruff.lint.per-file-ignores]` entry exempting the 7
     affected files from `N818` (justification:
     roadmap-mandated public-contract class names per FR-ISO2 /
     COMP-006 / COMP-011 / COMP-014 / AC12 / loader API);
     alternatively pin individual `noqa: N818` pragmas on each
     declaration.
   - `src/superclaude/cli/eval/commands.py` — remove the unused
     `.config.SCRATCH_ROOT_POLICY` import introduced by T02.25 (or
     promote it to a runtime use, if downstream code needs it).
   - `src/superclaude/cli/eval/hook_adapter.py:59` — replace
     `from ..install_hooks import install_hooks` with `from
     superclaude.cli.install_hooks import install_hooks`.
   - `src/superclaude/cli/eval/pty_driver.py:44` — remove unused
     `import os`.
   - `src/superclaude/cli/eval/pty_driver.py` — bundle the
     T02.01-mandated `pexpect as _pexpect_module` removal here so
     both F401s land in one pass; run `ruff check --fix` to
     reorder the import block (I001).
   - After both commits land, re-run `uv run ruff check
     src/superclaude/cli/eval/` and confirm exit 0; re-run this
     checkpoint and flip *status: FAIL* → *status: PASS* in place
     (the per-task status table updates for T02.01 only). Estimated
     effort: ~15 minutes for the lint slice, ~30–60 minutes for the
     vendoring slice including test authoring.
3. **QE-review documentation backfill (T02.09, T02.10, T02.21,
   T02.22).** Carried forward from `CP-P02-T07-T11.md` *Follow-ups*
   §1 and `CP-P02-T19-T23.md` *Follow-ups* §2. All four tasks are
   STRICT-tier with Sub-Agent Delegation Required; their
   `artifacts/D-003{0,1}/evidence.md` and
   `artifacts/D-004{0,1}/evidence.md` should carry a quality-engineer
   PASS verdict + reviewer name + date. Substantive containment +
   symlink-attack coverage is already proven by 30 + 14 + 19 + 6 = 69
   passing security tests; the audit-trail backfill is procedural,
   not corrective. Bundle with the remediation slice.
4. **T02.10 per-task `evidence.md` missing.** Carried forward from
   `CP-P02-T07-T11.md` *Follow-ups* §2 and `CP-P02-T13-T17.md`
   *Follow-ups* §2. Hygiene cleanup; `artifacts/D-0031/evidence.md`
   already covers the AC mapping, so this is purely about consistency
   with sibling evidence directories.
5. **Mid-phase checkpoint flips.** Once §1 + §2 land:
   - Re-run `CP-P02-T01-T05.md` and flip `status: FAIL` → `status:
     PASS` (T02.01 row updates, exit-criteria pytest invocation
     finally collects `test_pty_vendor.py`).
   - Re-run `CP-P02-T19-T23.md` and flip `status: FAIL` → `status:
     PASS` (ruff exit 0).
   - Re-run this gate (T02.27) and flip `status: FAIL` → `status:
     PASS` (T02.06 + T02.24 rows update; Exit Criteria 1 + 2 both
     met; Verification bullet 3 confirmed).

## Artifacts and evidence

- Mid-phase checkpoints: `CP-P02-T01-T05.md` (FAIL — T02.01),
  `CP-P02-T07-T11.md` (PASS — T02.07..T02.11), `CP-P02-T13-T17.md`
  (PASS — T02.13..T02.17), `CP-P02-T19-T23.md` (FAIL — 16 ruff
  violations).
- Per-task artifacts under `artifacts/D-0024..D-0044/` (D-0023
  absent).
- Per-task evidence under `evidence/T02.02..T02.26/` (T02.01 absent;
  T02.10 has `pytest-T02.10.log` only, no `evidence.md`).
- M2-suite pytest log captured live during this checkpoint:
  `evidence/T02.27/exit-criteria-pytest.log` → 690 passed in 8.18s,
  exit 0.
- M2-suite ruff log captured live during this checkpoint:
  `evidence/T02.27/ruff-eval.log` → 16 errors, exit 1.

## Cross-references

- Phase tasklist: `.dev/releases/current/cliEval/phase-2-tasklist.md`
  (T02.27 § lines 1287–1336; covered tasks T02.01–T02.26 at lines
  5–1285).
- Roadmap items: R-023..R-044 spanning NFR-MAINT1 vendoring (R-023) →
  R5-mit quarterly drift checklist (R-044).
- Prior Phase 2 checkpoints: `CP-P02-T01-T05.md`,
  `CP-P02-T07-T11.md`, `CP-P02-T13-T17.md`,
  `CP-P02-T19-T23.md`.
- Phase 1 exit: `CP-P01-END.md` (FAIL — T01.14 ExpectDSL interface
  outstanding, orthogonal to M2 scope; tracked separately under
  Phase 1 remediation).
- Relevant ADRs: `decisions.md` §D-10 (OQ-4 / M2 entry blocker
  cleared); FR-G1 (real subprocess discipline) reinforced by the
  TID251 ban-import rule landed in T02.19; R1-mit version pin landed
  in T02.20; NFR-ISO2 atomic try/except landed in T02.13;
  NFR-PERF1 perf budget pinned by T02.15.
- Downstream gate: Phase 3 entry (M3) gated on this PASS once the
  remediation slice above lands.
