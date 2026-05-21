# D-0030 — NFR-SEC2 Defense-in-Depth Attack Matrix

**Task**: T02.09 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: High (security, defense-in-depth)
**Roadmap**: NFR-SEC2 (`scratch-is-symlink-to-HOME`; `scratch-outside-allowlist`; `eval_id mutation post-construction`; `loader-bypass still rejected`)
**Cross-links**: D-0029 (FR-ISO2 path containment guard, T02.08), D-0028 (HomeIsolation method surface, T02.07), AC12 / T01.19 (resolve_scratch_root), FR-SCH2 / T01.05 (validate_eval_id)

## Goal

Deliver the *positive containment-rejection* test module that proves :class:`HomeIsolation` fails closed against every NFR-SEC2 attack vector. The FR-ISO2 unit surface (T02.08 / D-0029) already pins the three checks inside :func:`containment_guard`; D-0030 sits one layer higher and exercises :meth:`HomeIsolation.setup` end-to-end, asserting that each named attack vector surfaces as :class:`HomeContainmentViolation` with the correct ``check`` identifier (and the correct ``__cause__`` chain) so reporters can bucket failures without parsing the human-readable message.

## Attack matrix

| # | Vector (NFR-SEC2 wording) | Failure surface | ``check`` identifier | ``__cause__`` | Test class |
|---|---|---|---|---|---|
| 1 | ``scratch-is-symlink-to-HOME`` | :class:`HomeContainmentViolation` | ``scratch_root_allowlist`` | :class:`ScratchRootViolation` | ``TestVectorScratchSymlinkToHome`` |
| 2 | ``scratch-outside-allowlist`` | :class:`HomeContainmentViolation` | ``scratch_root_allowlist`` | :class:`ScratchRootViolation` | ``TestVectorScratchOutsideAllowlist`` |
| 3 | ``eval_id-mutation-post-construction`` | :class:`HomeContainmentViolation` | ``eval_id`` | :class:`InvalidEvalId` | ``TestVectorEvalIdMutationPostConstruction`` |
| 4 | ``loader-bypass`` | :class:`InvalidEvalId` (constructor) + :class:`HomeContainmentViolation` (second-layer setup) | n/a (constructor) → ``eval_id`` (setup) | n/a → :class:`InvalidEvalId` | ``TestVectorLoaderBypass`` |

Vector 1 (`scratch-is-symlink-to-HOME`) exercises the catastrophic case from the roadmap risk register (R2): the operator believes they are pointing at an allowlisted scratch root, but the path they supplied is a symlink whose resolved target is non-allowlisted (the real ``$HOME``/``.claude`` in the worst case). :func:`resolve_scratch_root` resolves with ``strict=False`` so the symlink collapses before the membership test runs; the symlink target is intentionally not in the test's allowlist.

Vector 2 (`scratch-outside-allowlist`) is the policy-failure mode. The scratch root is a real (non-symlinked) directory whose path is simply absent from the supplied :attr:`EvalConfig.allowed_scratch_roots`. Catches an off-policy ``--scratch-root`` CLI flag value or a misconfigured deployment.

Vector 3 (`eval_id-mutation-post-construction`) bypasses the frozen-dataclass guarantee via ``object.__setattr__`` (the same escape hatch the class itself uses for the ``_home_path`` slot). The constructor's ``__post_init__`` validation has already passed, so the only thing standing between a tampered id and :func:`tempfile.mkdtemp` is :func:`containment_guard`'s eval_id re-check. Tamper values are restricted to FR-SCH2-rejected ids whose textual form is a legal POSIX filename component — path-separator-bearing tampers (``../escape``, ``E1/x``, ``/etc/passwd``) are covered under vector 4 at construction time where ``__post_init__`` rejects them before any filesystem call.

Vector 4 (`loader-bypass`) exists in two layers:

- *Construction-time defense* — ``HomeIsolation.__post_init__`` re-runs :func:`validate_eval_id` so a caller skipping :class:`SuiteLoader` (programmatic test, future REPL, accidental fixture) hard-fails with :class:`InvalidEvalId` before any filesystem operation becomes reachable.
- *Second-layer defense* — even if the constructor's check were removed by a future refactor (simulated in the test by replacing ``__post_init__`` with a slot-only initializer), :func:`containment_guard`'s own :func:`validate_eval_id` call inside :meth:`HomeIsolation.setup` still rejects. The test deliberately patches ``__post_init__`` (not :func:`validate_eval_id`) so the two layers remain genuinely independent and the regression-pin is meaningful.

## Public API touched

None. D-0030 is a test-only deliverable: the production surface was finalized by D-0028 (T02.07) and D-0029 (T02.08); D-0030 adds *positive* (success-rejection) coverage at the integration boundary on top of the existing unit tests.

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| File ``tests/cli/eval/test_defense_in_depth.py`` exists | T02.09 | Module file present + importable. |
| At least 4 tests covering the 4 NFR-SEC2 vectors | T02.09 | Four ``TestVectorXxx`` classes + ``test_attack_matrix_coverage_is_complete`` pins names. 19 total tests (incl. parametrized cases). |
| Each vector test asserts ``HomeContainmentViolation`` | T02.09 | Each test (or the second-layer half of vector 4) raises :class:`HomeContainmentViolation`. Vector 4 constructor-time half raises :class:`InvalidEvalId` (the canonical loader-bypass surface; the CLI boundary maps it to :data:`INVALID_EVAL_ID_EXIT_CODE` = 2). |
| ``uv run pytest tests/cli/eval/test_defense_in_depth.py -v`` exits 0 | T02.09 | See ``TASKLIST_ROOT/evidence/T02.09/pytest-T02.09.log``: 19 passed in 0.14s. |
| Loader-bypass: constructing :class:`HomeIsolation` without :class:`SuiteLoader` still fails containment | T02.09 + NFR-SEC2 | ``TestVectorLoaderBypass.test_construction_rejects_loader_rejected_eval_id`` (7 parametrized cases) + ``test_loader_bypass_setup_still_fails_when_post_init_disabled``. |
| Attack matrix recorded in this spec | T02.09 | Section "Attack matrix" above. |
| ``check`` identifier pinned per vector | NFR-SEC2 bucketing | Each test asserts ``exc_info.value.check == <expected>``. |
| ``__cause__`` chain pinned per vector | Forensics | Each test asserts ``isinstance(exc_info.value.__cause__, <expected>)``. |
| Independence between constructor guard and setup guard | Defense-in-depth | ``test_loader_bypass_setup_still_fails_when_post_init_disabled`` patches ``__post_init__`` (not :func:`validate_eval_id`), proving the two layers fire independently. |

## Test inventory

```
tests/cli/eval/test_defense_in_depth.py
├── TestVectorScratchSymlinkToHome
│   └── test_setup_rejects_scratch_root_symlinked_outside_allowlist  (1)
├── TestVectorScratchOutsideAllowlist
│   └── test_setup_rejects_scratch_root_not_in_allowlist             (1)
├── TestVectorEvalIdMutationPostConstruction
│   └── test_setup_rejects_post_construction_eval_id_mutation        (8 parametrized)
├── TestVectorLoaderBypass
│   ├── test_construction_rejects_loader_rejected_eval_id            (7 parametrized)
│   └── test_loader_bypass_setup_still_fails_when_post_init_disabled (1)
└── test_attack_matrix_coverage_is_complete                          (1)

Total: 19 test cases.
```

## Reserved for follow-up tasks

| Open finding | Reserved to | Reason |
|---|---|---|
| ``CLAUDE_FAKE_TIME_OFFSET`` smuggling not covered | T06.03 (DOC-OQ8) | Behavior gated on OQ-8 resolution; the env var is currently opt-in via ``time_offset_sec`` and not part of the NFR-SEC2 attack matrix. |
| Hard guard against real ``~/.claude/`` | T02.10 (NFR-SEC3) | Distinct deliverable; D-0031 covers the integration test that asserts :meth:`HomeIsolation.setup` refuses any HOME resolving to the real ``~/.claude/``. |
| TOCTOU between ``mkdtemp`` and guard | T02.13 (NFR-ISO2 atomic wrapper) | The atomic wrapper is the natural locus; the guard itself runs synchronously inside ``setup``. |
| Symbolic re-attack via ``state_path`` suffix | Subsumed by D-0028 / D-0029 | :meth:`state_path` enforces relative-only suffixes and ``..`` rejection; covered by ``tests/cli/eval/test_home_isolation_extend.py``. |

## Files touched

| File | Change |
|---|---|
| ``tests/cli/eval/test_defense_in_depth.py`` | New module (19 tests across 4 vector classes + coverage pin). |

Nothing under ``src/superclaude/`` was modified — D-0030 is a test deliverable.
