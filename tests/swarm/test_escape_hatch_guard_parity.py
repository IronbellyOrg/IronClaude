"""T02.09 -- INV-014 escape-hatch isomorphism test.

Covers roadmap row R-037. INV-014 declares the load-bearing structural
invariant: the lens-driven path and the ``--custom-prompt-dir`` escape
hatch are **isomorphic** under §11.5 enforcement. Concretely, there is a
structure-preserving map between the two paths' failure outputs --
identical ``rule`` token, identical ``reason`` token, identical message
body modulo the path label -- and an isomorphic acceptance path.

Relationship to sibling tests
=============================

    * :mod:`test_injection_guard_all_paths` (T02.07 / R-035) sweeps the
      three input paths via parametrize and pins a single shared
      enforcement code path. It catches mutations that flip every path
      at once.
    * :mod:`test_custom_prompt_dir_injection_guard` (T02.08 / R-036 /
      INV-003) pins the specific INV-003 acceptance: the
      custom-prompt-dir reader's guard delegates to the same helper as
      the lens path, with identical rule + reason tokens. It catches
      mutations on the custom-prompt-dir side specifically.
    * **This module (T02.09 / R-037 / INV-014)** layers the
      *isomorphism* gate on top: it asserts the bijection between paths
      via a parametrized "drive a violation through path X" helper that
      returns a normalised failure-shape tuple. The parity assertion
      compares the tuple from the lens path to the tuple from the
      custom-prompt-dir path. The load-bearing mutation gate is
      asymmetric: a monkeypatch that bypasses the guard on **one path
      only** must break the parity assertion. This is the
      "asymmetric guard regression" wording in the T02.09 acceptance
      criteria.

Why an isomorphism instead of equality
======================================

The two paths legitimately differ on the ``path`` slug: the lens path
reports ``prompt.system`` (the JobSpec field that holds the resolved
system prompt) and the custom-prompt-dir path reports
``custom_prompt_dir/system.txt`` (the file on disk that holds the
caller's override). Both seams need to be routable from the failed
contract, so requiring byte-equality on the entire failure shape would
be wrong. INV-014 instead requires a *normalised* equality that strips
the path label from the comparison while still pinning that the path
labels exist on both sides. That is the bijection: there is a
structure-preserving function ``f`` mapping (lens-failure,
cpd-failure) → (normalised-rule, normalised-reason, normalised-tail)
that returns the same triple for both paths under any input.
"""

# ruff: noqa: E402 -- module-level ``pytestmark`` intentionally precedes the
# superclaude imports so the marker is registered before collection.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pytest

# INV-014 escape-hatch isomorphism (T08.03 / NFR-007). Module-level
# marker so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm import preflight as preflight_mod
from superclaude.cli.swarm.preflight import (
    RULE_INJECTION_GUARD,
    PreflightError,
    PreflightFailure,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Path identifiers + shared fixtures.
#
# The parametrize ids are the path labels; each path is exercised through
# a tiny driver that returns the structured ``PreflightFailure`` list. The
# isomorphism assertions then normalise the failures into a
# ``NormalisedFailure`` triple (rule, reason, tail) where ``tail`` is the
# message body with the path label substituted by a sentinel. Two paths
# are isomorphic iff their normalised triples are equal.
# ---------------------------------------------------------------------------


PATH_LENS: str = "lens"
PATH_CPD: str = "custom_prompt_dir"

PATH_IDS: tuple[str, ...] = (PATH_LENS, PATH_CPD)

# Expected per-path slug values. Pinned here so a refactor that renames
# either slug surfaces in this module and not just T02.07/T02.08.
EXPECTED_PATH_SLUG: dict[str, str] = {
    PATH_LENS: "prompt.system",
    PATH_CPD: "custom_prompt_dir/system.txt",
}


# Bad system prompt: deliberately omits the canonical §11.5 sentence so
# both paths reject. Reused across all parametrized cases so the
# isomorphism is asserted against a single source-of-truth payload.
_BAD_SYSTEM: str = (
    "You are a reviewer. Inspect the target carefully and report issues. "
    "Do NOT include the canonical guard sentence here."
)
_GOOD_SYSTEM: str = "You are a reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE


def _write_cpd(
    base: Path,
    *,
    system: str,
    user: str = "Review: {{target}}",
    meta: str = "variables: {}\n",
) -> None:
    """Materialise the three files the custom-prompt-dir reader needs."""
    (base / "system.txt").write_text(system, encoding="utf-8")
    (base / "user.txt").write_text(user, encoding="utf-8")
    (base / "meta.yaml").write_text(meta, encoding="utf-8")


# ---------------------------------------------------------------------------
# Path drivers -- each returns the structured failure list for a given
# (path_id, system) pair. Both drivers route through the same
# ``enforce_injection_guard`` helper in production; the asymmetric
# mutation gate below proves that by demonstrating a regression where
# only one driver still hits the helper.
# ---------------------------------------------------------------------------


def _drive_lens(_tmp_path: Path, *, system: str) -> list[PreflightFailure]:
    """Lens-path driver: call the central guard helper directly.

    ``run_preflight`` invokes :func:`enforce_injection_guard` against
    ``job.prompt.system`` immediately after lens-defaults expansion. The
    helper is the single seam the lens path crosses on the way to
    dispatch, so driving it directly with the bad fixture is the
    structural equivalent of "the lens path's §11.5 enforcement".
    Returning the failure list (rather than raising) keeps the
    comparison shape uniform with the custom-prompt-dir driver below.

    The lookup goes through :data:`preflight_mod` attribute access (not
    the directly-imported name) so the asymmetric-mutation tests below
    can swap the helper via :func:`monkeypatch.setattr` on the module
    and have the swap propagate here -- mirroring how
    :func:`run_preflight` resolves the helper at call time.
    """
    return preflight_mod.enforce_injection_guard(
        system=system,
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
    )


def _drive_cpd(tmp_path: Path, *, system: str) -> list[PreflightFailure]:
    """Custom-prompt-dir driver: materialise the trio and read it.

    :func:`read_custom_prompt_dir` raises :class:`PreflightError` on
    rejection; the test harness unwraps that into the failure list so
    both drivers return the same shape. A reader that returns cleanly
    (i.e., the guard passed) yields an empty list -- matching the
    success contract of :func:`enforce_injection_guard`.

    As with the lens driver, the reader is looked up through
    :data:`preflight_mod` attribute access so monkeypatch swaps on the
    module reach this call site.
    """
    _write_cpd(tmp_path, system=system)
    try:
        preflight_mod.read_custom_prompt_dir(
            tmp_path,
            required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        )
    except PreflightError as exc:
        return list(exc.failures)
    return []


_PathDriver = Callable[
    [
        Path,
    ],
    list[PreflightFailure],
]

PATH_DRIVERS: dict[str, Callable[..., list[PreflightFailure]]] = {
    PATH_LENS: _drive_lens,
    PATH_CPD: _drive_cpd,
}


# ---------------------------------------------------------------------------
# Normalisation -- the structure-preserving map under which the lens and
# custom-prompt-dir failures are equal.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NormalisedFailure:
    """The image of a :class:`PreflightFailure` under the INV-014 map.

    Fields are byte-identical across both paths for the same input. The
    ``message_tail`` field carries the message with the path label
    substituted by a literal ``<PATH>`` sentinel so the comparison
    ignores the legitimately different path slug while still surfacing
    any other divergence in the message body (rule reference, missing
    substring quote, §11.5 reference).
    """

    rule: str
    reason: str
    message_tail: str


def _normalise(failure: PreflightFailure) -> NormalisedFailure:
    """Map a :class:`PreflightFailure` to its INV-014 image."""
    return NormalisedFailure(
        rule=failure.rule,
        reason=failure.reason,
        message_tail=failure.message.replace(failure.path, "<PATH>"),
    )


# ---------------------------------------------------------------------------
# Acceptance #1 -- parametrized rejection parity.
#
# Both paths reject the same bad fixture with the same rule + reason +
# normalised message body. The parametrize id surfaces in pytest output
# so a divergence on either path names the offending path immediately.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path_id", PATH_IDS)
def test_each_path_rejects_missing_substring(tmp_path: Path, path_id: str) -> None:
    """INV-014 acceptance: each path independently rejects the bad
    fixture with the canonical injection-guard rule. Parametrized so a
    refactor that only breaks one path surfaces the offending path id
    in the failing-test report.
    """
    driver = PATH_DRIVERS[path_id]
    failures = driver(tmp_path, system=_BAD_SYSTEM)

    assert len(failures) == 1, (
        f"{path_id}: expected exactly one §11.5 failure; got {failures!r}"
    )
    failure = failures[0]
    assert failure.rule == RULE_INJECTION_GUARD, (
        f"{path_id}: unexpected rule token {failure.rule!r}"
    )
    assert failure.reason == "injection-guard", (
        f"{path_id}: unexpected reason token {failure.reason!r}"
    )
    assert failure.path == EXPECTED_PATH_SLUG[path_id], (
        f"{path_id}: expected path slug "
        f"{EXPECTED_PATH_SLUG[path_id]!r}; got {failure.path!r}"
    )


@pytest.mark.parametrize("path_id", PATH_IDS)
def test_each_path_accepts_substring_present(tmp_path: Path, path_id: str) -> None:
    """Complementary accept gate. Pairs with the reject parametrize so a
    regression that always-rejects (a different mutation than
    always-accepts) also breaks the suite. Without this gate a
    monkeypatch that forces every call to fail would slip past T02.09."""
    driver = PATH_DRIVERS[path_id]
    failures = driver(tmp_path, system=_GOOD_SYSTEM)
    assert failures == [], (
        f"{path_id}: good fixture should pass cleanly; got {failures!r}"
    )


# ---------------------------------------------------------------------------
# Acceptance #2 -- structural isomorphism between the two paths.
#
# Drive the same violation through both paths and assert the normalised
# failures are equal. The structured definition of "equal" is the
# NormalisedFailure triple above: rule + reason + message body with the
# path label stripped. Path slugs legitimately differ and are asserted
# separately so a regression that *also* breaks the path slugs is caught.
# ---------------------------------------------------------------------------


def test_normalised_failures_are_isomorphic(tmp_path: Path) -> None:
    """INV-014 core: the bijection between paths preserves rule, reason,
    and message body verbatim (modulo the path-label substitution).

    This is the structural identity that pins "escape-hatch isomorphism".
    A future refactor that re-implements the failure shape on one path
    (different message phrasing, different reason slug, dropped §11.5
    reference) breaks the equality and surfaces a divergence at exactly
    one point in the suite -- this test.
    """
    cpd_root = tmp_path / "cpd"
    cpd_root.mkdir(parents=True, exist_ok=True)

    lens_failures = _drive_lens(tmp_path, system=_BAD_SYSTEM)
    cpd_failures = _drive_cpd(cpd_root, system=_BAD_SYSTEM)

    assert len(lens_failures) == 1
    assert len(cpd_failures) == 1

    lens_image = _normalise(lens_failures[0])
    cpd_image = _normalise(cpd_failures[0])

    # The bijection: under normalisation, the two paths produce the same
    # triple. Pinned via dataclass equality so a regression on any field
    # surfaces here.
    assert lens_image == cpd_image, (
        "INV-014 isomorphism broken: lens normalised failure "
        f"{lens_image!r} != cpd normalised failure {cpd_image!r}"
    )

    # Path labels differ -- intentional, and asserted positively so a
    # regression that collapses the two paths' slugs (a different kind
    # of regression) is also caught.
    assert lens_failures[0].path != cpd_failures[0].path
    assert lens_failures[0].path == EXPECTED_PATH_SLUG[PATH_LENS]
    assert cpd_failures[0].path == EXPECTED_PATH_SLUG[PATH_CPD]


def test_message_body_quotes_required_substring_on_both_paths(
    tmp_path: Path,
) -> None:
    """The message body on both paths must quote the required substring
    verbatim (repr-quoted) so a human reader can recover the §11.5
    fragment that is missing without consulting the rule registry.

    Asserted on both paths to layer a content-level isomorphism gate on
    top of the structural one: even if the rule + reason tokens line up,
    a divergence on whether the message quotes the substring (or the
    §11.5 marker) breaks the human-facing parity that operators rely on
    when triaging failures."""
    cpd_root = tmp_path / "cpd"
    cpd_root.mkdir(parents=True, exist_ok=True)

    lens_failures = _drive_lens(tmp_path, system=_BAD_SYSTEM)
    cpd_failures = _drive_cpd(cpd_root, system=_BAD_SYSTEM)

    for label, failure in (
        (PATH_LENS, lens_failures[0]),
        (PATH_CPD, cpd_failures[0]),
    ):
        assert repr(CANONICAL_INJECTION_GUARD_SENTENCE) in failure.message, (
            f"{label}: message does not quote required substring ({failure.message!r})"
        )
        assert "§11.5" in failure.message, (
            f"{label}: message does not reference §11.5 ({failure.message!r})"
        )


# ---------------------------------------------------------------------------
# Acceptance #3 -- the load-bearing mutation gate.
#
# An asymmetric regression -- one that bypasses the guard on *one path
# only* -- must break the isomorphism. The two sub-tests below simulate
# the two halves of the asymmetric mutation: one weakens the lens path,
# the other weakens the custom-prompt-dir path. Each sub-test re-runs
# the isomorphism assertion under the mutation and asserts it now
# fails. The combined coverage proves the isomorphism gate detects an
# asymmetric weakening from *either* side -- not just one.
# ---------------------------------------------------------------------------


def _isomorphism_holds(tmp_path: Path) -> bool:
    """Re-run the isomorphism check under whatever monkeypatch is live.

    Returns ``True`` iff both paths reject and produce the same
    normalised failure triple. The asymmetric mutation tests below flip
    this to ``False`` by weakening exactly one path, and assert the
    return value flips with them. Keeping the check as a helper (rather
    than raising) means the mutation tests can express the load-bearing
    property as a single boolean flip.
    """
    cpd_root = tmp_path / "cpd"
    cpd_root.mkdir(parents=True, exist_ok=True)

    lens_failures = _drive_lens(tmp_path, system=_BAD_SYSTEM)
    cpd_failures = _drive_cpd(cpd_root, system=_BAD_SYSTEM)

    if len(lens_failures) != 1 or len(cpd_failures) != 1:
        return False
    return _normalise(lens_failures[0]) == _normalise(cpd_failures[0])


def test_isomorphism_holds_without_mutation(tmp_path: Path) -> None:
    """Baseline for the mutation-gate sub-tests: in the un-mutated
    production code, the isomorphism holds. Pinned as a standalone
    assertion so a regression in the helper itself (rather than the
    paths) is distinguishable from a regression in production code."""
    assert _isomorphism_holds(tmp_path) is True


def test_asymmetric_mutation_weakening_lens_breaks_isomorphism(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Asymmetric weakening on the **lens** side: rebind
    :func:`enforce_injection_guard` -- when called with the lens path's
    default ``path_label='prompt.system'`` -- to a no-op while leaving
    the custom-prompt-dir call site (which passes
    ``path_label='custom_prompt_dir/system.txt'``) untouched.

    The lens driver now accepts the bad fixture; the custom-prompt-dir
    driver still rejects it. Two failures of unequal length break the
    normalised-equality assertion in :func:`_isomorphism_holds` so the
    helper returns ``False`` -- proving the isomorphism gate detects a
    lens-side weakening.
    """
    real_enforce = preflight_mod.enforce_injection_guard

    def _selective_enforce(
        system: str, required_substring: str, *, path_label: str = "prompt.system"
    ) -> list[PreflightFailure]:
        # Weaken only the lens-side call site (identified by its default
        # path label). The custom-prompt-dir reader passes a different
        # path_label, so it continues to delegate to the real helper.
        if path_label == EXPECTED_PATH_SLUG[PATH_LENS]:
            return []
        return real_enforce(system, required_substring, path_label=path_label)

    monkeypatch.setattr(preflight_mod, "enforce_injection_guard", _selective_enforce)

    # Sanity: the lens driver now accepts the bad fixture (mutation
    # took effect) and the cpd driver still rejects (its call site is
    # untouched).
    lens_failures = _drive_lens(tmp_path / "lens-probe", system=_BAD_SYSTEM)
    cpd_root = tmp_path / "cpd-probe"
    cpd_root.mkdir()
    cpd_failures = _drive_cpd(cpd_root, system=_BAD_SYSTEM)
    assert lens_failures == [], "lens-side mutation did not weaken lens path"
    assert len(cpd_failures) == 1, (
        "custom-prompt-dir path should still reject the bad fixture"
    )

    # Load-bearing assertion: the isomorphism is broken.
    assert _isomorphism_holds(tmp_path / "check") is False


def test_asymmetric_mutation_weakening_cpd_breaks_isomorphism(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Asymmetric weakening on the **custom-prompt-dir** side: replace
    :func:`read_custom_prompt_dir` with a variant that skips the
    :func:`enforce_injection_guard` call entirely while preserving the
    file-reading shape. The lens path is untouched.

    The cpd driver now accepts the bad fixture; the lens driver still
    rejects it. Same shape of asymmetric divergence as the
    lens-weakening test, but the broken side is opposite. The
    isomorphism helper flips to ``False`` -- proving INV-014's bijection
    detects asymmetric weakening from either side.
    """

    def _unguarded_read(
        path: str | Path,
        *,
        required_substring: str = "",
    ) -> tuple[str, str, dict[str, object]]:
        # File-shape parity with the real reader: read the three files
        # and return the trio. Skip the §11.5 substring enforcement so
        # the cpd path no longer raises on a bad system.txt.
        base = Path(path)
        system = (base / "system.txt").read_text(encoding="utf-8")
        user = (base / "user.txt").read_text(encoding="utf-8")
        return system, user, {}

    monkeypatch.setattr(preflight_mod, "read_custom_prompt_dir", _unguarded_read)

    # Sanity: the cpd driver now accepts the bad fixture (mutation took
    # effect) and the lens driver still rejects (its call site is
    # untouched).
    lens_failures = _drive_lens(tmp_path / "lens-probe", system=_BAD_SYSTEM)
    cpd_root = tmp_path / "cpd-probe"
    cpd_root.mkdir()
    cpd_failures = _drive_cpd(cpd_root, system=_BAD_SYSTEM)
    assert len(lens_failures) == 1, "lens path should still reject the bad fixture"
    assert cpd_failures == [], "custom-prompt-dir mutation did not weaken cpd path"

    # Load-bearing assertion: the isomorphism is broken.
    assert _isomorphism_holds(tmp_path / "check") is False
