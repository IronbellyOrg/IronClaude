"""Per-eval HOME isolation record + FR-ISO1 methods (DM-006 + COMP-006).

This module defines :class:`HomeIsolation`, the per-eval isolation primitive
the cliEval harness uses to layer a private ``HOME`` on top of the four
``IsolationLayers`` guarantees that already exist in
``superclaude.cli.sprint.executor``:

* ``scoped_work_dir`` (CLAUDE_WORK_DIR)
* ``git_boundary``    (GIT_CEILING_DIRECTORIES)
* ``plugin_dir``      (CLAUDE_PLUGIN_DIR)
* ``settings_dir``    (CLAUDE_SETTINGS_DIR)

``HomeIsolation`` does NOT mutate or replace ``IsolationLayers``; it sits
beside it, contributing one additional layer (``HOME``) plus the session
stamp (``CLAUDE_SESSION_ID``) and optional simulated wall-clock offset
(``CLAUDE_FAKE_TIME_OFFSET``). The COMP-012 probe at
``tests/cli/eval/test_isolation_layers_probe.py`` (Task T02.05) must keep
passing after this extension, which it does because nothing in
``cli/sprint/executor.py`` is touched.

DM-006 record (T02.04) — the four immutable fields
====================================================

``HomeIsolation`` is a ``@dataclass(frozen=True)`` so once an instance is
built it cannot be mutated by downstream consumers. This makes it safe to
share across threads inside the parallel orchestrator (R-058 / T03.16)
without locking. Equality is structural across all four fields via the
dataclass-generated ``__eq__``.

1. ``eval_id``         — the FR-SCH2-validated eval identifier. The id
   flows directly into the per-eval HOME by :meth:`HomeIsolation.setup`
   so it MUST satisfy the FR-SCH2 regex before any filesystem write. The
   ``__post_init__`` hook re-applies :func:`validate_eval_id` (T01.05) so
   a ``HomeIsolation`` can never be constructed with an unsafe id even
   when a caller bypasses the loader.
2. ``home_root``       — the scratch root directory under which the
   per-eval HOME is ``mkdtemp``-ed by :meth:`setup`. Full FR-ISO2 path
   containment lands in T02.08; this module performs only the minimal
   ``parents=True, exist_ok=True`` materialization needed to create
   sibling per-eval HOMEs concurrently.
3. ``session_id``      — the value :meth:`env` stamps into
   ``CLAUDE_SESSION_ID``. Allocation lives in the orchestrator (FR-G2 /
   T03.16); this record only holds the assigned value.
4. ``time_offset_sec`` — optional offset in whole seconds for the eval's
   simulated wall clock. Default ``0`` matches DM-006 verbatim; when the
   value is non-zero :meth:`env` adds ``CLAUDE_FAKE_TIME_OFFSET``. Whether
   the subprocess actually honors the variable is gated on OQ-8 (DOC-OQ8
   / T06.03); keeping the offset opt-in via non-zero values means the
   env dict stays minimal until OQ-8 resolves.

COMP-006 method surface (T02.07) — FR-ISO1
==========================================

The four methods below are the externally observable surface of
COMP-006. They mutate process-local filesystem state (and an internal
private slot tracking the created HOME path) without ever mutating the
four DM-006 fields:

* :meth:`setup`                 — ``mkdtemp`` under ``home_root`` and stash
  the created path on a private ``_home_path`` slot via
  ``object.__setattr__``. Returns the created path. Idempotency is one-
  shot per instance: calling :meth:`setup` twice raises ``RuntimeError``
  rather than silently leaking a directory.
* :meth:`env`                   — returns the env-var dict the subprocess
  needs: ``HOME`` always, ``CLAUDE_SESSION_ID`` always, and
  ``CLAUDE_FAKE_TIME_OFFSET`` only when ``time_offset_sec != 0``. The
  return type pins ``dict[str, str]`` so callers can ``.update()`` it
  alongside ``IsolationLayers.env_vars`` without coercion.
* :meth:`teardown`              — removes the per-eval HOME when ``keep``
  is false, leaves it on disk when ``keep`` is true (so post-mortem
  inspection or NFR-ISO2 ``setup_failed`` tagging in T02.13 can still
  pick the directory up). Always clears the private path slot so the
  instance is safe to garbage-collect.
* :meth:`state_path`            — joins ``suffix`` under the active
  per-eval HOME so consumers (hook adapter T02.14, atomic setup T02.13,
  artifact writers) never need to import :mod:`os.path` themselves. The
  full containment check on ``suffix`` lands in T02.08; this method
  performs the minimum necessary check that the joined path stays under
  ``home_path``.

Cross-links
===========

* DM-006 record spec (roadmap row 26).
* COMP-006 method surface (roadmap rows 28 / 32; T02.07 / T02.11).
* FR-SCH2 :func:`validate_eval_id` (T01.05).
* FR-ISO2 ``containment_guard`` (T02.08) — strengthens the symlink /
  allowlist / regex checks layered on top of :meth:`setup` and
  :meth:`state_path`.
* DOC-OQ8 (T06.03) — gates ``CLAUDE_FAKE_TIME_OFFSET`` semantics.
* COMP-012 probe (T02.05 — ``test_isolation_layers_probe.py``) — pins the
  upstream ``IsolationLayers`` shape this module sits beside.
"""

from __future__ import annotations

import shutil
import tempfile
import traceback
from dataclasses import dataclass
from pathlib import Path

from .config import EvalConfig, ScratchRootViolation, resolve_scratch_root
from .loader import InvalidEvalId, validate_eval_id

__all__ = [
    "SETUP_FAILED_TAG_RELPATH",
    "HomeContainmentViolation",
    "HomeIsolation",
    "containment_guard",
]


# NFR-ISO2 atomic-setup contract — see ``HomeIsolation.setup`` docstring and
# D-0033/spec.md. The tag is written under the per-eval HOME so that the
# directory becomes self-describing for downstream consumers (the orchestrator,
# the EvalRunner, post-mortem operators): a HOME that carries this relative
# path is one whose setup raised AFTER ``tempfile.mkdtemp`` materialized the
# directory and BEFORE ``setup`` returned successfully. The constant is
# exported so :class:`EvalRunner` (T03.x) and forensics tooling can locate the
# tag without re-deriving the path.
SETUP_FAILED_TAG_RELPATH = ".eval-meta/setup_failed"


def _write_setup_failed_tag(home_path: Path, exc: BaseException) -> None:
    """Write the NFR-ISO2 ``setup_failed`` artifact tag under ``home_path``.

    The tag distinguishes "harness bug or environmental refusal during
    setup" (status ERRORED) from "eval ran and produced a failing
    assertion" (status FAIL). The contents are split for grep-ability:

    * Line 1 is the exception class name verbatim
      (``type(exc).__name__``), so a downstream EvalRunner can bucket
      the error with a single ``head -n1`` read.
    * The remainder is the formatted traceback for forensic inspection.

    The helper is best-effort: ``setup`` catches and discards any
    exception this function raises so a write failure (e.g. the
    ``.eval-meta`` directory cannot be created because the per-eval HOME
    was made read-only by a future hardening step) never masks the
    original setup exception.

    Args:
        home_path: The per-eval HOME ``mkdtemp``-ed by
            :meth:`HomeIsolation.setup`. The tag is materialized at
            ``home_path / SETUP_FAILED_TAG_RELPATH``.
        exc: The exception that interrupted ``setup``. Used only to
            populate the tag contents; this helper never re-raises it.
    """

    tag_path = home_path / SETUP_FAILED_TAG_RELPATH
    tag_path.parent.mkdir(parents=True, exist_ok=True)
    # ``traceback.format_exception`` reads the active exception state when
    # the helper is invoked from inside an ``except`` clause. Pin the
    # arguments explicitly so the helper also works when called outside
    # one (defensive — the only call site is currently inside ``except``).
    tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    payload = f"{type(exc).__name__}\n" + "".join(tb_lines)
    tag_path.write_text(payload, encoding="utf-8")


class HomeContainmentViolation(Exception):
    """Raised by :func:`containment_guard` when any FR-ISO2 check fails.

    The exception is the single hard-failure surface of FR-ISO2 — it is
    the only thing :meth:`HomeIsolation.setup` may raise once
    :func:`tempfile.mkdtemp` has succeeded and BEFORE the hook adapter
    (T02.14) writes a single byte under the per-eval HOME. Catching this
    type at the orchestrator level is sufficient to cover all three
    containment checks (eval_id regex, scratch-root allowlist, post-
    mkdtemp symlink resolution); callers MUST NOT branch on the
    underlying :class:`InvalidEvalId` / :class:`ScratchRootViolation`
    causes — they are exposed via ``__cause__`` for forensics only.

    The exception MUST raise before any hook deploy or eval-state
    write so NFR-SEC2 ("hard refusal before side effects") is upheld;
    the NFR-ISO2 atomic-setup wrapper (T02.13) is responsible for
    preserving the partial per-eval HOME with a ``setup_failed`` tag
    once it lands.

    Attributes:
        check: Short identifier for the failed check (``"eval_id"``,
            ``"scratch_root_allowlist"``, ``"home_path_resolution"`` or
            ``"home_path_escape"``). Lets reporters bucket failures
            without parsing the human-readable message.
        home_path: The per-eval HOME path the guard was asked to
            validate. Stored verbatim as supplied by the caller (no
            resolution) so forensics keep the original input.
        scratch_root: The declared scratch root the guard checked
            ``home_path`` against. Stored verbatim.
        eval_id: The eval id under inspection. Stored verbatim
            (``repr``-rendered) so non-string smuggled scalars are
            visible in reporter output.
        detail: Free-form one-line message describing the specific
            failure. Inherits from the underlying cause when one
            exists (e.g. the ``ScratchRootViolation`` rendering).
    """

    def __init__(
        self,
        *,
        check: str,
        home_path: Path,
        scratch_root: Path,
        eval_id: object,
        detail: str,
    ) -> None:
        self.check = check
        self.home_path = home_path
        self.scratch_root = scratch_root
        self.eval_id = eval_id
        self.detail = detail
        super().__init__(
            f"FR-ISO2 containment check {check!r} failed for "
            f"eval_id={eval_id!r} home_path={home_path!s} "
            f"scratch_root={scratch_root!s}: {detail}"
        )


def containment_guard(
    home_path: Path,
    scratch_root: Path,
    eval_id: str,
    *,
    config: EvalConfig,
) -> None:
    """FR-ISO2 three-check defense-in-depth guard.

    The guard layers three independent checks on top of the per-eval
    HOME materialization that :meth:`HomeIsolation.setup` just performed.
    Each check has a distinct attack vector in scope:

    1. **eval_id regex** — re-applies :func:`validate_eval_id` (T01.05).
       The loader (T01.07) already validates the id pre-expand and
       post-expand, but a caller bypassing :class:`SuiteLoader` (e.g.,
       a programmatic test, a future REPL entry point) could construct
       a :class:`HomeIsolation` directly. The re-check closes that
       loader-bypass surface called out in NFR-SEC2.
    2. **Scratch-root allowlist** — re-applies
       :func:`resolve_scratch_root` (T01.19) against ``scratch_root``.
       The helper resolves the path with ``Path.resolve(strict=False)``
       which collapses symlinks; if ``scratch_root`` is a symlink to a
       non-allowlisted target (e.g., ``/home/user/.claude``) the
       resolved form will not match any entry in the resolved
       :attr:`EvalConfig.allowed_scratch_roots`. The allowlist is
       sourced exclusively from the caller-supplied
       :class:`EvalConfig`; nothing inside this module synthesizes a
       fallback that could inject the caller's ``scratch_root``
       into the allowlist after the fact (NFR-SEC2 loader-bypass
       defense — see D-0029 spec rationale).
    3. **Post-mkdtemp path containment** — resolves ``home_path`` with
       ``Path.resolve(strict=True)`` and asserts the resolved form is
       equal to OR a sub-path of the resolved ``scratch_root``. The
       ``strict=True`` mode raises :class:`FileNotFoundError` if the
       per-eval HOME has not been materialized yet, so this is the
       check that pins "guard runs AFTER ``mkdtemp``". Catches the
       attack vector where a symlinked component inside ``home_path``
       points outside ``scratch_root`` even though the textual prefix
       check would have passed.

    On any failure the function raises :class:`HomeContainmentViolation`
    with the failing check identifier. Underlying causes
    (:class:`InvalidEvalId`, :class:`ScratchRootViolation`,
    :class:`FileNotFoundError`) are chained via ``raise ... from`` so
    forensic tooling can still walk ``__cause__``.

    Args:
        home_path: Path to the per-eval HOME directory ``mkdtemp``-ed by
            :meth:`HomeIsolation.setup`. Must exist on disk; the
            ``strict=True`` resolve enforces this so a caller cannot
            invoke the guard "ahead" of ``mkdtemp``.
        scratch_root: Scratch root under which ``home_path`` must
            reside. Need not exist (``strict=False`` resolution); for
            test ergonomics callers can pass a path that
            :class:`HomeIsolation` will create via
            ``mkdir(parents=True, exist_ok=True)`` shortly after.
        eval_id: The eval identifier the per-eval HOME corresponds to.
            Re-validated through :func:`validate_eval_id`.
        config: Required :class:`EvalConfig`. Its
            ``allowed_scratch_roots`` is the sole source of truth for
            the scratch-root allowlist check. The guard refuses to
            synthesize a fallback config: a missing argument is a
            programming error, never a "use the defaults" cue. This
            closes the bypass where a caller could otherwise construct
            ``HomeIsolation(home_root=<attacker-controlled>)`` and have
            the guard quietly add that root to the allowlist.

    Raises:
        HomeContainmentViolation: Any of the three checks failed. The
            ``check`` attribute identifies which one; ``detail`` carries
            the human-readable cause; ``__cause__`` holds the underlying
            exception when applicable.
    """

    # Check 1: eval_id regex. Loader-bypass defense.
    try:
        validate_eval_id(eval_id)
    except InvalidEvalId as exc:
        raise HomeContainmentViolation(
            check="eval_id",
            home_path=home_path,
            scratch_root=scratch_root,
            eval_id=eval_id,
            detail=str(exc),
        ) from exc

    # Check 2: scratch-root allowlist (symlink-aware via resolve_scratch_root).
    # ``config`` is required: see docstring rationale (NFR-SEC2 bypass close).
    try:
        resolved_scratch = resolve_scratch_root(scratch_root, config=config)
    except ScratchRootViolation as exc:
        raise HomeContainmentViolation(
            check="scratch_root_allowlist",
            home_path=home_path,
            scratch_root=scratch_root,
            eval_id=eval_id,
            detail=str(exc),
        ) from exc

    # Check 3: post-mkdtemp symlink resolution + containment under
    # scratch_root. strict=True asserts the HOME exists (i.e., mkdtemp
    # already ran). Any symlink inside home_path is collapsed; the
    # resolved form must equal or live beneath the resolved scratch root.
    try:
        resolved_home = home_path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise HomeContainmentViolation(
            check="home_path_resolution",
            home_path=home_path,
            scratch_root=scratch_root,
            eval_id=eval_id,
            detail=(
                "home_path does not exist on disk; FR-ISO2 requires the "
                "guard to run AFTER mkdtemp materialized the per-eval "
                "HOME"
            ),
        ) from exc

    if not (
        resolved_home == resolved_scratch
        or resolved_home.is_relative_to(resolved_scratch)
    ):
        raise HomeContainmentViolation(
            check="home_path_escape",
            home_path=home_path,
            scratch_root=scratch_root,
            eval_id=eval_id,
            detail=(
                f"resolved home_path {resolved_home!s} escapes resolved "
                f"scratch_root {resolved_scratch!s}"
            ),
        )


@dataclass(frozen=True)
class HomeIsolation:
    """Per-eval HOME isolation record + COMP-006 method surface.

    DM-006 fixes the immutable four-field record contract:

    * ``eval_id``        — ``str``, required. Re-validated in
      ``__post_init__`` via :func:`validate_eval_id` so any unsafe id
      raises :class:`superclaude.cli.eval.InvalidEvalId` BEFORE any
      consumer can derive a filesystem path from it.
    * ``home_root``      — ``pathlib.Path``, required. Scratch root under
      which the per-eval HOME is created by :meth:`setup`. The dataclass
      stores it as-is; full containment is FR-ISO2's responsibility
      (T02.08).
    * ``session_id``     — ``str``, required. Value :meth:`env` stamps
      into ``CLAUDE_SESSION_ID`` for the subprocess. Allocation lives in
      the orchestrator (FR-G2 / T03.16); this record only holds the
      assigned value.
    * ``time_offset_sec`` — ``int``, defaults to ``0``. Optional simulated
      wall-clock offset in whole seconds; :meth:`env` emits
      ``CLAUDE_FAKE_TIME_OFFSET`` only when non-zero. Full activation is
      gated on OQ-8 (DOC-OQ8 / T06.03).

    The four declared fields are frozen — mutation raises
    ``dataclasses.FrozenInstanceError``. A single private slot,
    ``_home_path``, tracks the post-:meth:`setup` HOME directory; it is
    written via ``object.__setattr__`` (the documented escape hatch for
    frozen dataclasses) and never participates in equality or hashing.
    """

    eval_id: str
    home_root: Path
    session_id: str
    time_offset_sec: int = 0

    def __post_init__(self) -> None:
        """Re-apply the FR-SCH2 guard and initialize the private path slot.

        The FR-SCH2 re-validation makes loader-bypass impossible:
        constructing a ``HomeIsolation`` with an unsafe ``eval_id``
        raises :class:`InvalidEvalId` before any filesystem operation
        becomes reachable. The private ``_home_path`` slot is set to
        ``None`` so :meth:`env` / :meth:`state_path` can raise a clear
        error when called before :meth:`setup`.
        """

        validate_eval_id(self.eval_id)
        object.__setattr__(self, "_home_path", None)

    # ------------------------------------------------------------------
    # COMP-006 method surface (FR-ISO1)
    # ------------------------------------------------------------------

    @property
    def home_path(self) -> Path:
        """Return the per-eval HOME directory created by :meth:`setup`.

        Raises :class:`RuntimeError` when :meth:`setup` has not yet been
        called or when :meth:`teardown` has already cleared the slot,
        so the failure mode is "obvious AttributeError" instead of a
        silent ``None`` flowing into an env dict.
        """

        home = self._home_path  # type: ignore[attr-defined]
        if home is None:
            raise RuntimeError(
                "HomeIsolation.setup() must be called before accessing home_path"
            )
        return home

    @property
    def is_set_up(self) -> bool:
        """Return ``True`` when :meth:`setup` has created a per-eval HOME
        and :meth:`teardown` has not yet been called.

        Lets callers (atomic setup wrapper T02.13, the orchestrator)
        ask whether teardown is needed without catching exceptions.
        """

        return self._home_path is not None  # type: ignore[attr-defined]

    def setup(self, *, config: EvalConfig) -> Path:
        """Create the per-eval HOME directory under ``home_root``.

        Uses :func:`tempfile.mkdtemp` with the eval_id as prefix so
        sibling per-eval HOMEs under the same ``home_root`` are
        guaranteed to be unique by the OS (atomic on POSIX, see
        ``mkdtemp`` docs). Parallel evals never collide on directory
        names; mutating one HOME cannot affect siblings because each
        HOME is its own ``mkdtemp`` root.

        After ``mkdtemp`` succeeds, :func:`containment_guard` (FR-ISO2,
        T02.08) is applied AFTER the per-eval HOME has been
        materialized and BEFORE any hook deploy or eval-state write.
        The guard re-validates ``eval_id`` against the FR-SCH2 regex,
        re-applies the AC12 scratch-root allowlist, and
        ``Path.resolve(strict=True)``-checks the freshly created HOME
        against the scratch root. Any failure surfaces as
        :class:`HomeContainmentViolation`; the partial per-eval HOME is
        left on disk so callers can route teardown through
        ``teardown(keep=True)`` for forensic inspection (the
        containment exception itself carries the full forensic
        payload — see NFR-ISO2 contract below).

        Idempotency rule: calling :meth:`setup` twice on the same
        instance raises :class:`RuntimeError`. This prevents the silent
        directory leak that would otherwise occur if a caller looped
        over an instance, and it makes the atomic-setup wrapper
        (T02.13) easier to reason about.

        Args:
            config: Required :class:`EvalConfig`. Its
                ``allowed_scratch_roots`` provides the scratch-root
                allowlist :func:`containment_guard` enforces.
                ``setup`` deliberately refuses to synthesize a
                fallback that injects ``self.home_root`` into the
                allowlist — that would defeat the AC12 check, because a
                caller can construct ``HomeIsolation`` with any
                ``home_root`` (per-instance, the dataclass cannot
                meaningfully validate it). Production callers
                (orchestrator T03.16) pass the run's resolved config;
                tests build an :class:`EvalConfig` whose allowlist
                includes the test scratch root.

        Returns:
            The freshly created per-eval HOME path (also recorded on
            :attr:`home_path`).

        Raises:
            RuntimeError: If :meth:`setup` was already called on this
                instance and :meth:`teardown` has not run since.
            HomeContainmentViolation: Any of the three FR-ISO2 checks
                failed; the per-eval HOME directory was created and is
                preserved on disk for inspection with a
                ``setup_failed`` tag (NFR-ISO2 — see below).

        NFR-ISO2 atomic-setup contract (T02.13 / D-0033)
        ------------------------------------------------

        Any exception raised AFTER :func:`tempfile.mkdtemp` and BEFORE
        ``setup`` returns successfully MUST leave the per-eval HOME on
        disk. The private ``_home_path`` slot stays populated so a
        caller that wraps ``setup`` in ``try/finally`` can route
        teardown through ``teardown(keep=True)`` to preserve the
        partial HOME for forensics.

        Non-containment exceptions additionally drop a ``setup_failed``
        artifact tag at ``<home>/.eval-meta/setup_failed`` (constant
        :data:`SETUP_FAILED_TAG_RELPATH`). The tag's first line is the
        exception class name; the body is the formatted traceback. The
        tag distinguishes harness bugs / environmental refusal (status
        ERRORED — tag present, no eval output) from real eval failures
        (status FAIL — eval ran, expectations missed). The tag write
        is best-effort: a secondary exception during tag write is
        discarded so the original exception is the one the caller
        sees. The original exception type is preserved verbatim — the
        wrapper adds the tag side effect, it does not re-wrap or
        re-classify the exception.

        :class:`HomeContainmentViolation` is the deliberate exception
        to the tag-write rule: writing under a HOME the guard just
        refused could land under the real ``~/.claude/`` directory
        when the scratch root or the ``mkdtemp`` result is symlinked
        there (the attack matrix exercised by NFR-SEC3 in T02.10).
        The violation exception itself is the forensic signal — its
        ``check``, ``home_path``, ``scratch_root``, ``eval_id`` and
        ``detail`` attributes carry everything a reporter needs to
        bucket the eval as ERRORED.
        """

        if self._home_path is not None:  # type: ignore[attr-defined]
            raise RuntimeError(
                f"HomeIsolation.setup() already called for eval_id={self.eval_id!r}"
            )

        # Ensure the scratch root exists. ``parents=True, exist_ok=True``
        # is safe because the FR-ISO2 guard below catches any path that
        # resolves outside the policy allowlist.
        self.home_root.mkdir(parents=True, exist_ok=True)

        home = Path(
            tempfile.mkdtemp(prefix=f"{self.eval_id}-", dir=str(self.home_root))
        )
        object.__setattr__(self, "_home_path", home)

        # NFR-ISO2 atomic-setup wrapper. Anything that raises beyond this
        # line — FR-ISO2 containment_guard today, any future post-mkdtemp
        # work (hook deploy verification, capability stamping) tomorrow —
        # leaves the per-eval HOME on disk so ``teardown(keep=True)``
        # preserves the directory for post-mortem inspection without a
        # re-resolve. The ``_home_path`` slot stays populated for the
        # same reason.
        #
        # Tag-write asymmetry between containment and non-containment
        # exceptions:
        #
        # * :class:`HomeContainmentViolation` — NO tag is written.
        #   Writing a file under a HOME the guard just refused would
        #   breach the NFR-SEC3 invariants enforced in T02.10
        #   (`test_hard_guard_real_home.py`): when ``scratch_root`` is
        #   (or symlinks to) the real ``~/.claude/``, or when
        #   :func:`tempfile.mkdtemp` returned a symlinked path that
        #   resolves outside ``scratch_root``, any write under ``home``
        #   lands inside real ``~/.claude/``. The containment exception
        #   itself carries the full forensic payload (``check``,
        #   ``home_path``, ``scratch_root``, ``eval_id``, ``detail``)
        #   so the orchestrator can bucket the eval as ERRORED without
        #   the tag.
        # * Any other ``Exception`` — tag is written. These are
        #   harness bugs or post-containment failures (e.g., hook deploy
        #   verification under T02.14) where the per-eval HOME is known
        #   to be inside the allowlisted scratch root and the tag is
        #   safe to write. The tag write is best-effort: a secondary
        #   failure is swallowed so the original exception surfaces
        #   unchanged.
        try:
            # FR-ISO2 defense-in-depth: re-check eval_id, scratch-root
            # allowlist, and symlink-resolved containment AFTER mkdtemp
            # and BEFORE the hook adapter (T02.14) writes anything under
            # the per-eval HOME.
            containment_guard(
                home_path=home,
                scratch_root=self.home_root,
                eval_id=self.eval_id,
                config=config,
            )
        except HomeContainmentViolation:
            # NFR-SEC3: no FS writes under a refused HOME. The
            # containment exception itself is the structured signal.
            raise
        except Exception as exc:
            try:
                _write_setup_failed_tag(home, exc)
            except Exception:
                pass
            raise
        return home

    def env(self) -> dict[str, str]:
        """Return the env-var dict the subprocess needs for HOME isolation.

        * ``HOME`` is always present.
        * ``CLAUDE_SESSION_ID`` is always present (FR-ISO1 mandate).
        * ``CLAUDE_FAKE_TIME_OFFSET`` is present only when
          ``time_offset_sec`` differs from the default ``0``. Keeping the
          variable opt-in means OQ-8 (DOC-OQ8 / T06.03) does not have to
          be resolved before this method is safe to call: a caller that
          does not request a time offset gets the historic two-key dict.

        Callers ``.update()`` this dict alongside
        ``IsolationLayers.env_vars`` to assemble the full subprocess
        env; the return type is pinned to ``dict[str, str]`` so the
        merge is type-clean.

        Raises :class:`RuntimeError` if invoked before :meth:`setup`,
        because the ``HOME`` value would otherwise have to be a
        fabricated placeholder.
        """

        env: dict[str, str] = {
            "HOME": str(self.home_path),
            "CLAUDE_SESSION_ID": self.session_id,
        }
        if self.time_offset_sec != 0:
            env["CLAUDE_FAKE_TIME_OFFSET"] = str(self.time_offset_sec)
        return env

    def teardown(self, keep: bool) -> None:
        """Tear down the per-eval HOME directory.

        * ``keep=False`` removes the directory tree (``shutil.rmtree``
          with ``ignore_errors=False``; any failure surfaces to the
          caller so the orchestrator can decide whether to flag the
          eval as cleanup-failed).
        * ``keep=True`` leaves the directory on disk for post-mortem
          inspection — this is the branch the NFR-ISO2 atomic setup
          wrapper (T02.13) takes when ``setup`` partially fails, and the
          branch :meth:`teardown` is called on under ``--keep-home``
          (T03.18).

        Either way, the private ``_home_path`` slot is cleared after
        teardown, so subsequent :meth:`env` / :meth:`state_path` calls
        fail loudly instead of pointing at a stale (possibly deleted)
        path. Calling :meth:`teardown` when no HOME has been set up is
        a no-op — callers are not required to track setup state
        themselves.
        """

        home = self._home_path  # type: ignore[attr-defined]
        if home is None:
            return  # No-op: setup never ran, or teardown already ran.

        try:
            if not keep:
                shutil.rmtree(home)
        finally:
            # Always clear the slot — even if rmtree raised, the path
            # is no longer trustworthy for future env() / state_path()
            # consumers and callers will re-run setup() if they want a
            # fresh HOME.
            object.__setattr__(self, "_home_path", None)

    def state_path(self, suffix: str) -> Path:
        """Return ``home_path / suffix`` after a light containment check.

        ``suffix`` must be a relative path (no leading separator) and
        must not contain ``..`` components — otherwise the returned
        path could escape ``home_path`` and undermine the
        per-eval HOME isolation. Full FR-ISO2 containment
        (symlink resolution + allowlist) lands in T02.08; this method
        performs only the minimum check necessary to keep the
        primitive safe in isolation.

        Raises :class:`ValueError` for any suffix that escapes
        ``home_path``. Raises :class:`RuntimeError` if invoked before
        :meth:`setup` (via :attr:`home_path`).
        """

        candidate = Path(suffix)
        if candidate.is_absolute():
            raise ValueError(
                f"state_path suffix must be relative, got absolute path: {suffix!r}"
            )
        if ".." in candidate.parts:
            raise ValueError(
                f"state_path suffix must not contain '..' components: {suffix!r}"
            )

        joined = self.home_path / candidate
        # Defense-in-depth: even with the part check above, refuse any
        # joined path that does not resolve under home_path. This
        # complements the FR-ISO2 guard in T02.08 (which will resolve
        # symlinks); here we work on the lexical path because
        # state_path may legitimately be called before the suffix
        # exists on disk.
        try:
            joined.relative_to(self.home_path)
        except ValueError as exc:
            raise ValueError(
                f"state_path suffix escapes home_path: {suffix!r}"
            ) from exc
        return joined
