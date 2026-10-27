# D-0031 — NFR-SEC3 Hard Guard Against Real `~/.claude/`

**Task**: T02.10 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: High (security; R7 — operator accidentally points harness at their real `~/.claude/`)
**Roadmap**: NFR-SEC3 (`hard guard against real ~/.claude/`)
**Cross-links**: D-0028 (HomeIsolation method surface, T02.07), D-0029 (FR-ISO2 path containment guard, T02.08), D-0030 (NFR-SEC2 attack matrix, T02.09), AC12 / T01.19 (resolve_scratch_root), FR-SCH2 / T01.05 (validate_eval_id), T02.13 (NFR-ISO2 atomic-setup wrapper — partial-HOME tag contract)

## Goal

Pin the *catastrophic-case* contract: when a maintainer accidentally points the eval harness at the host's real `~/.claude/` (typo in `--scratch-root`, inherited shell alias, or a symlink that escapes into it), `HomeIsolation.setup()` MUST refuse via `HomeContainmentViolation` and MUST NOT write anything under the real `~/.claude/` directory.

D-0029 (FR-ISO2 unit surface) and D-0030 (NFR-SEC2 attack matrix) both exercise the guard against synthetic stand-in directories under `pytest`'s `tmp_path`. D-0031 closes the loop by running the same scenarios against the *real* `~/.claude/` directory on the host — the exact directory whose corruption is the worst possible failure mode of the harness.

## Hard-guard contract (NFR-SEC3)

1. **Refusal surface.** `HomeIsolation.setup()` MUST raise `HomeContainmentViolation` whenever the per-eval HOME would resolve to (or inside) the host's real `~/.claude/`, whether passed directly as `home_root` or via a `scratch_root` symlink that escapes there.
2. **Containment bucketing.** The `check` field of the raised exception MUST be:
   - `"scratch_root_allowlist"` when the real `~/.claude/` is passed directly as `home_root` (AC12 / check 2 rejects before any symlink resolution).
   - `"scratch_root_allowlist"` when the scratch root is a symlink that resolves into `~/.claude/` (`resolve_scratch_root` resolves with `strict=False` so the symlink collapses before membership testing).
   - `"home_path_escape"` when the per-eval HOME materializes as a symlink that resolves into `~/.claude/` (FR-ISO2 check 3 — post-mkdtemp resolution — catches the chain).
3. **Refusal-before-side-effects on the real HOME.** No file inside the host's real `~/.claude/` is created, modified, or touched as a side effect of the attempted setup. Every pre-existing direct child of `~/.claude/` MUST be byte-identical post-test (mtime_ns + SHA-256 for files; mtime_ns for directories) — a `_DirSnapshot` mtime fixture proves this.
4. **Per-eval HOME stays empty on refusal.** `HomeIsolation.setup()` invokes `tempfile.mkdtemp` BEFORE `containment_guard` runs (intentional, per the D-0029 spec — partial HOMEs are preserved so the NFR-ISO2 atomic-setup wrapper in T02.13 can tag them as `setup_failed`). When that leaks an empty per-eval HOME under the rejected location, the leak MUST stay empty: the guard fires BEFORE the hook adapter (T02.14) or any eval-state writer touches the per-eval HOME.

## Attack matrix

| # | Vector (NFR-SEC3 wording, T02.10 step list) | Failure surface | `check` identifier | Test |
|---|---|---|---|---|
| 1 | `home_root` resolves directly to real `~/.claude/` (default `EvalConfig`) | `HomeContainmentViolation` | `scratch_root_allowlist` | `TestRealHomeAsScratchRoot.test_setup_refuses_real_dot_claude_as_home_root` |
| 1a | Same vector, leaked per-eval HOME is empty | `HomeContainmentViolation` | `scratch_root_allowlist` | `TestRealHomeAsScratchRoot.test_per_eval_home_is_empty_when_setup_refuses` |
| 1b | Same vector, explicit empty allowlist (strictest config) | `HomeContainmentViolation` | `scratch_root_allowlist` | `TestRealHomeAsScratchRoot.test_setup_refuses_real_dot_claude_with_permissive_config_does_not_help` |
| 2 | Per-eval HOME mints as a symlink into `~/.claude/` (patched `mkdtemp` returns symlink path) | `HomeContainmentViolation` | `home_path_escape` | `TestScratchRootContainsRealHomeViaSymlink.test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude` |
| 3 | Scratch root *itself* is a symlink that resolves into `~/.claude/` | `HomeContainmentViolation` | `scratch_root_allowlist` | `TestScratchRootContainsRealHomeViaSymlink.test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude` |

Vector 1 (and sub-variants 1a/1b) corresponds to step 3 in the T02.10 step list: `home_root` resolves directly to the real `~/.claude/`. The default `EvalConfig.allowed_scratch_roots = (/tmp/eval-runs, .dev/eval-runs)` excludes `~/.claude/`, so AC12 / check 2 rejects without any symlink resolution. Sub-variant 1b proves the rejection is driven by the allowlist comparison itself (not by `~/.claude/` happening to be omitted from the default list) by passing an *empty* allowlist.

Vectors 2 and 3 correspond to step 4 in the T02.10 step list: scratch root somehow contains `~/.claude/` via symlink escape. Vector 2 mirrors the existing D-0029 mkdtemp-patch pattern (`test_setup_catches_symlink_escape_under_explicit_config` in `tests/cli/eval/test_path_containment.py`) but targets the real `~/.claude/`. Vector 3 is the sibling case where the scratch root *itself* is a symlink — `resolve_scratch_root` strips the symlink before the allowlist test, so check 2 catches it before check 3 has a chance to run.

## Public API touched

None. D-0031 is a test-only deliverable: the production surface was finalized by D-0028 (T02.07) and D-0029 (T02.08); D-0031 adds *integration-level* coverage against the host's real `~/.claude/` directory on top of the existing unit + attack-matrix tests.

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| File `tests/cli/eval/test_hard_guard_real_home.py` exists | T02.10 | Module file present + importable. |
| At least 2 tests proving `HomeIsolation.setup()` refuses real `~/.claude/` | T02.10 | Two test classes (`TestRealHomeAsScratchRoot`, `TestScratchRootContainsRealHomeViaSymlink`) totaling 5 tests + 1 coverage pin = 6 total. |
| Tests pass on a host where `~/.claude/` exists | T02.10 | See `TASKLIST_ROOT/evidence/T02.10/pytest-T02.10.log`: 6 passed in 0.15s on host with `/config/.claude/` present. |
| Tests skipped (with explicit reason) on hosts where `~/.claude/` does not exist | T02.10 | `real_claude_dir` fixture calls `pytest.skip` with a reason naming the missing path. |
| Refusal occurs before any FS write under the rejected HOME | T02.10 | `_DirSnapshot` mtime fixture (SHA-256 + mtime_ns of direct children, `Path.lstat()` for symlink layer) captured pre-test and compared post-test in every snapshot-bearing test. |
| Hard-guard contract recorded in this spec | T02.10 | Section "Hard-guard contract (NFR-SEC3)" above. |

## Test inventory

```
tests/cli/eval/test_hard_guard_real_home.py
├── TestRealHomeAsScratchRoot
│   ├── test_setup_refuses_real_dot_claude_as_home_root              (1)
│   ├── test_per_eval_home_is_empty_when_setup_refuses               (1)
│   └── test_setup_refuses_real_dot_claude_with_permissive_config_does_not_help  (1)
├── TestScratchRootContainsRealHomeViaSymlink
│   ├── test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude  (1)
│   └── test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude   (1)
└── test_hard_guard_contract_pin                                     (1)

Total: 6 test cases.
```

## Fixtures introduced

| Fixture | Scope | Role |
|---|---|---|
| `real_claude_dir` | function | Locate `Path.home() / ".claude"`; `pytest.skip` with explicit reason if absent. |
| `dot_claude_snapshot` | function | Capture `_DirSnapshot` of every direct child of `~/.claude/` (mtime_ns + SHA-256 for files, mtime_ns for directories) BEFORE the test runs. |
| `cleanup_leaked_eval_homes` | function | Teardown — remove any directories whose name starts with the test module's eval-id prefix (`HardguardevalT0210-`) that appeared under `~/.claude/` during the test. |

The `_EVAL_ID = "HardguardevalT0210"` module constant scopes leak cleanup so the fixture can ONLY ever touch directories the module itself created (never any pre-existing `~/.claude/` content). Operators can grep for the prefix under `~/.claude/` to confirm cleanup ran.

## Reserved for follow-up tasks

| Open finding | Reserved to | Reason |
|---|---|---|
| Absolute hard guard (refuse `~/.claude/` even if the operator adds it to the allowlist) | T06.03 (DOC-OQ8) | The current FR-ISO2 contract is "allowlist is the source of truth". An absolute-deny against `~/.claude/` regardless of allowlist requires the OQ-8 design decision (would change config semantics). |
| Per-eval HOME mkdtemp ordering — guard runs AFTER mkdtemp | T02.13 (NFR-ISO2 atomic wrapper) | Partial-HOME preservation is intentional; the leaked empty per-eval HOME is the atomic-setup wrapper's `setup_failed` tag input. T02.10 only asserts the leak is empty, not that it is absent. |
| TOCTOU between guard and mkdtemp | T02.13 (NFR-ISO2 atomic wrapper) | The atomic wrapper is the natural locus; the guard itself runs synchronously inside `setup`. |

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_hard_guard_real_home.py` | New module (6 tests across 2 attack-vector classes + 1 coverage pin). |
| `.dev/releases/current/cliEval/artifacts/D-0031/spec.md` | New (this file). |
| `.dev/releases/current/cliEval/artifacts/D-0031/notes.md` | New. |
| `.dev/releases/current/cliEval/artifacts/D-0031/evidence.md` | New. |
| `.dev/releases/current/cliEval/evidence/T02.10/pytest-T02.10.log` | New. |

Nothing under `src/superclaude/` was modified — D-0031 is a test-only deliverable.
