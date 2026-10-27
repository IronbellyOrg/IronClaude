# D-0030 — Implementation Notes

## Design choices

### Why this module sits one layer higher than D-0029

D-0029 (`tests/cli/eval/test_path_containment.py`) is the *unit* surface for the FR-ISO2 :func:`containment_guard` — it calls the guard directly with hand-crafted inputs. D-0030 is the *integration* surface: it constructs real :class:`HomeIsolation` instances, calls :meth:`HomeIsolation.setup`, and asserts the guard fires from inside the full ``setup`` pipeline. Both surfaces are needed:

- The unit tests prove the guard's three checks are individually correct.
- The integration tests prove the four NFR-SEC2 vectors are caught when the guard is invoked the way production code invokes it (via :meth:`HomeIsolation.setup`, after :func:`tempfile.mkdtemp`, before any hook deploy).

Without D-0030, a refactor that accidentally re-ordered the guard call (e.g. moved it before ``mkdtemp``, or wrapped it in a try/except that swallowed the violation) could leave D-0029 passing while NFR-SEC2 silently regressed.

### Why vector 3 only uses POSIX-safe tamper values

The post-construction mutation test forces an unsafe ``eval_id`` after construction, then calls :meth:`setup`. Inside ``setup``, ``tempfile.mkdtemp(prefix=f"{self.eval_id}-", dir=str(self.home_root))`` runs BEFORE :func:`containment_guard`. If the tampered id contains a path separator (``/etc/passwd``, ``E1/x``) or escapes the directory (``../escape``), ``mkdtemp`` itself raises an ``OSError`` (``PermissionError`` or ``FileNotFoundError`` from ``os.mkdir``) before the guard ever runs.

That outcome is still defense-in-depth — the kernel fails closed, no per-eval HOME is created, no hook writes anywhere. But it is the *wrong* failure surface to assert against from this test: the guard's eval_id check would not have been reached, so the test would not be proving what its name says it proves.

The fix is to restrict the parametrize list to FR-SCH2-rejected ids whose textual form is a legal POSIX filename component (no ``/``, no leading ``/``). Path-separator tampers are still covered — under vector 4 at construction time, where :meth:`__post_init__` rejects them before ``setup`` is even called.

### Why vector 4's second-layer test patches ``__post_init__`` instead of :func:`validate_eval_id`

The two layers in vector 4 share the same module-level binding to :func:`validate_eval_id`:

- ``isolation.py`` imports ``validate_eval_id`` from ``loader.py`` (``from .loader import validate_eval_id``).
- ``__post_init__`` calls it via that binding.
- :func:`containment_guard` also calls it via that binding.

If the test monkeypatched ``isolation.validate_eval_id`` to a no-op, *both* layers would be disabled simultaneously, and a tampered id like ``../escape`` would then escape via :func:`tempfile.mkdtemp`'s prefix concatenation (creating ``scratch_root/../escape-XXXX`` in the parent of ``scratch_root``). The guard's third check (``home_path_escape``) would catch it — which is correct defense-in-depth behavior, but it does NOT prove the guard's *eval_id* check is independent.

The fix is to patch ``HomeIsolation.__post_init__`` directly (replacing it with a slot-only initializer that skips the validation). :func:`validate_eval_id` itself remains untouched, so :func:`containment_guard`'s reference still points at the real implementation. With a tamper id like ``"9bad"`` (FR-SCH2-rejected but a legal POSIX filename prefix), :func:`tempfile.mkdtemp` succeeds cleanly under ``scratch_root``, and the failure that surfaces IS unambiguously the guard's eval_id check (``check == "eval_id"``).

### Why the parametrize lists overlap deliberately

Vector 3 and vector 4 both include ``9bad``, ``{{template}}``, ``${shell}``, ``E1\nE2`` etc. This overlap is intentional: the two vectors exercise *different* layers — vector 3 hits the guard's check after construction, vector 4 hits the constructor's check directly. Keeping the lists symmetric documents that both layers must reject the same input set, which is the core defense-in-depth invariant.

### Why ``test_attack_matrix_coverage_is_complete`` exists

A future refactor could rename or delete a vector class. Without an explicit coverage pin, the matrix would silently shrink and CI would not notice. The coverage test enumerates the four canonical vector names (matching the roadmap row 30 wording exactly) and asserts the corresponding classes exist in this module. A rename forces an update both to the roadmap-citation comment and to the canonical list, which is the right blast radius for an NFR-SEC2 refactor.

## Test-vs-implementation balance

Acceptance criterion says "at least 4 tests"; this module ships 19 (4 vector classes, some heavily parametrized, plus the coverage pin). The expansion is justified:

- Vector 3's parametrize covers 8 distinct FR-SCH2-rejected shapes (leading digit, empty, whitespace, template smuggling, shell-substitution smuggling, newline injection, leading dash, lowercase start). Each shape exercises a different branch of the regex; if one class were removed by a future refactor we want to know.
- Vector 4's parametrize covers 7 loader-rejected shapes spanning path traversal, absolute path, separator smuggling, leading digit, template/shell smuggling, and newline injection.
- The second-layer setup test pins the *layered* property (not just the constructor's check) so a refactor weakening one layer is caught.

Total runtime: 0.14s — the parametrize expansion is not a performance concern.

## What this module does NOT cover

- ``CLAUDE_FAKE_TIME_OFFSET`` env-var smuggling: out of scope until OQ-8 (T06.03) resolves. The variable is opt-in via ``time_offset_sec != 0`` and not part of the NFR-SEC2 attack matrix.
- Real ``~/.claude/`` hard guard: T02.10 / D-0031 owns that integration test. NFR-SEC3 is a separate deliverable.
- Symlink chain escape inside the per-eval HOME after creation: T02.08 / D-0029 covers this at the unit level (``test_raises_on_symlink_chain_escape``); D-0030 does not duplicate it.
- TOCTOU between ``mkdtemp`` and the guard: T02.13 (NFR-ISO2 atomic wrapper) is the natural locus.

## Sanity verification

| Check | Result |
|---|---|
| ``uv run pytest tests/cli/eval/test_defense_in_depth.py -v`` | 19 passed in 0.14s |
| ``uv run pytest tests/cli/eval/test_path_containment.py tests/cli/eval/test_home_isolation_extend.py tests/cli/eval/test_isolation_dataclass.py -q`` | 117 passed in 0.28s (no regression in sibling modules) |
