"""T02.08 -- INV-003 custom-prompt-dir identical-guard test.

Covers roadmap row R-036. INV-003 pins the security-critical property
that the §11.5 prompt-injection guard on the ``--custom-prompt-dir``
escape hatch is enforced **identically** to the lens-driven path. The
two paths feed different sources (a caller-supplied directory of three
text files vs. a registered :class:`LensEntry`'s
``system_prompt_fragment``) into the same downstream worker pipeline,
so a divergence in guard semantics between them would let an attacker
pick the weaker path and bypass §11.5 enforcement.

T02.07 (R-035) already establishes the parametrized cross-path parity
sweep across the three input paths and the shared
:func:`schema.contains_required_substring` predicate. T02.09 (R-037 /
INV-014) layers the full escape-hatch isomorphism gate on top. This
module sits between them and pins the specific INV-003 acceptance
shape:

    * The custom-prompt-dir path REJECTS a ``system.txt`` whose
      contents miss the required substring.
    * The **same content** fed through the lens path's
      :func:`enforce_injection_guard` helper produces an identical
      rejection: same :data:`RULE_INJECTION_GUARD` token, same
      ``injection-guard`` reason, same required-substring quoted in
      the human-readable ``message``. Only the structured ``path``
      field legitimately differs (``custom_prompt_dir/system.txt`` vs.
      ``prompt.system``) so a caller assembling the structured failure
      contract can route the diagnostic to the correct seam.
    * The failure ``message`` identifies the failing rule by quoting
      the required substring -- a human reader can recover the §11.5
      violation source without reading the rule slug.
    * **Mutation gate**: bypassing the guard on the
      custom-prompt-dir path -- whether by skipping the
      :func:`enforce_injection_guard` call entirely or by stubbing the
      shared :func:`schema.contains_required_substring` predicate to
      always-True -- flips the verdict and breaks the parity test.

The mutation gate is the load-bearing structural test. If a future
refactor splits the custom-prompt-dir guard into a path-specific
implementation, the predicate-stub mutation here passes through the
lens path but the custom-prompt-dir path keeps rejecting -- and the
parity assertion fails, surfacing the silent divergence.

Sibling scope:

    * :mod:`test_custom_prompt_dir` (T02.05) exercises the reader's
      happy-path / missing-file / meta.yaml behaviour.
    * :mod:`test_injection_guard_all_paths` (T02.07) sweeps all three
      input paths via parametrize.
    * :mod:`test_escape_hatch_guard_parity` (T02.09) layers the
      INV-014 isomorphism parity gate.
"""

# ruff: noqa: E402 -- module-level ``pytestmark`` intentionally precedes the
# superclaude imports so the marker is registered before collection.

from __future__ import annotations

from pathlib import Path

import pytest

# INV-003 custom-prompt-dir guard (T08.03 / NFR-007). Module-level
# marker so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm.preflight import (
    RULE_INJECTION_GUARD,
    PreflightError,
    PreflightFailure,
    enforce_injection_guard,
    read_custom_prompt_dir,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Shared fixture content
#
# A single haystack string is used through both paths. The lens path
# wraps it via :func:`enforce_injection_guard`; the custom-prompt-dir
# path writes it to ``system.txt`` and lets ``read_custom_prompt_dir``
# call the same helper internally. Both must produce the identical
# (rule, reason, message-substring) triple. ``identical`` here means
# "the same content yields the same diagnostic shape", which is the
# INV-003 acceptance criterion.
# ---------------------------------------------------------------------------


_BAD_SYSTEM: str = "You are a reviewer. Inspect the target carefully and report issues."
"""A system prompt that deliberately omits the §11.5 canonical sentence."""


_GOOD_SYSTEM: str = "You are a reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
"""Companion fixture exercising the accept path; pairs with ``_BAD_SYSTEM``."""


def _write_cpd(
    base: Path,
    *,
    system: str,
    user: str = "Review: {{target}}",
    meta: str = "variables: {}\n",
) -> None:
    """Write the three files into ``base`` for the custom-prompt-dir path."""
    (base / "system.txt").write_text(system, encoding="utf-8")
    (base / "user.txt").write_text(user, encoding="utf-8")
    (base / "meta.yaml").write_text(meta, encoding="utf-8")


def _lens_path_failures(system: str) -> list[PreflightFailure]:
    """Run ``system`` through the lens path's central guard helper.

    The lens path's seam is :func:`enforce_injection_guard`: the
    :func:`run_preflight` driver calls it after lens-defaults expansion
    on ``job.prompt.system``. Invoking the helper directly with the
    same content the custom-prompt-dir test uses is the structural
    equivalent of "same fixture, lens path".
    """
    return enforce_injection_guard(
        system=system,
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
    )


def _cpd_path_failures(base: Path, *, system: str) -> list[PreflightFailure]:
    """Run ``system`` through the custom-prompt-dir reader.

    The reader's seam is the same :func:`enforce_injection_guard` call,
    routed via :func:`read_custom_prompt_dir`. Returning the failure
    list (instead of asserting on raise) keeps the comparison
    structural -- the parity test compares two ``list[PreflightFailure]``
    objects rather than two ``PreflightError`` exception payloads.
    """
    _write_cpd(base, system=system)
    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(
            base,
            required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        )
    return excinfo.value.failures


# ---------------------------------------------------------------------------
# Acceptance #1 -- custom-prompt-dir rejects missing substring.
# ---------------------------------------------------------------------------


def test_custom_prompt_dir_rejects_missing_substring(tmp_path: Path) -> None:
    """INV-003 -- ``--custom-prompt-dir`` preflight rejects a
    ``system.txt`` that lacks the §11.5 required substring.

    The rejection is structured (:class:`PreflightError` with a
    populated ``failures`` list, not a bare exception) so the caller
    can render every failing rule in one pass and assemble the
    M5 ``failed`` contract. The rule token, ``path`` slug, and reason
    token are all pinned here so a refactor that renames any of them
    breaks the test loudly.
    """
    failures = _cpd_path_failures(tmp_path, system=_BAD_SYSTEM)

    assert len(failures) == 1
    failure = failures[0]
    assert failure.rule == RULE_INJECTION_GUARD
    assert failure.path == "custom_prompt_dir/system.txt"
    assert failure.reason == "injection-guard"


def test_custom_prompt_dir_accepts_substring_present(tmp_path: Path) -> None:
    """Complementary accept gate -- a present substring round-trips
    cleanly. Paired with the reject test so a regression that flips
    every verdict to "always-fail" (a different mutation) also breaks
    the suite."""
    _write_cpd(tmp_path, system=_GOOD_SYSTEM)
    system, _, _ = read_custom_prompt_dir(
        tmp_path, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
    )
    assert CANONICAL_INJECTION_GUARD_SENTENCE in system


# ---------------------------------------------------------------------------
# Acceptance #2 -- failure message identifies the failing rule.
# ---------------------------------------------------------------------------


def test_custom_prompt_dir_failure_message_identifies_rule(
    tmp_path: Path,
) -> None:
    """The human-readable ``message`` quotes the required substring so
    a reader can see *which* §11.5 sentence is missing, not just that
    the rule slug fired. Pinning the message contract here keeps the
    diagnostic actionable across future rule-id renames."""
    failures = _cpd_path_failures(tmp_path, system=_BAD_SYSTEM)

    failure = failures[0]
    # The rule slug identifies the rule machine-side.
    assert failure.rule == RULE_INJECTION_GUARD
    # The path slug identifies the offending file.
    assert "custom_prompt_dir/system.txt" in failure.path
    # The message quotes the required substring verbatim (repr-quoted)
    # so a reader can spot the §11.5 missing fragment without consulting
    # the rule registry.
    assert repr(CANONICAL_INJECTION_GUARD_SENTENCE) in failure.message
    # The ``§11.5`` reference is also surfaced in the message body.
    assert "§11.5" in failure.message


# ---------------------------------------------------------------------------
# Acceptance #3 -- identical rejection shape vs lens path.
# ---------------------------------------------------------------------------


def test_same_fixture_yields_identical_rejection_on_both_paths(
    tmp_path: Path,
) -> None:
    """INV-003 core property: the *same* system-prompt content fed
    through both paths produces an *identical* diagnostic shape.

    The structural definition of "identical" used here:

        * Same number of failures (1).
        * Same ``rule`` token (both :data:`RULE_INJECTION_GUARD`).
        * Same ``reason`` token (``"injection-guard"``).
        * Same message tail after the path prefix is stripped -- the
          two messages differ only in the ``path_label`` they were
          built with; everything after that label (the required
          substring, the §11.5 reference) is byte-identical.

    The intentional difference is ``path``: the lens path reports
    ``prompt.system`` (the JobSpec field that owns the prompt) and
    the custom-prompt-dir path reports
    ``custom_prompt_dir/system.txt`` (the file on disk that owns the
    prompt). Both seams need to be routable from the failed contract;
    the parity is on rule + reason + message body, not on the path
    field.
    """
    lens_failures = _lens_path_failures(_BAD_SYSTEM)
    cpd_failures = _cpd_path_failures(tmp_path, system=_BAD_SYSTEM)

    assert len(lens_failures) == 1
    assert len(cpd_failures) == 1
    lens_f = lens_failures[0]
    cpd_f = cpd_failures[0]

    # Rule + reason tokens are byte-identical -- the structural §11.5
    # invariant. INV-014 isomorphism (T02.09) builds on this property.
    assert lens_f.rule == cpd_f.rule == RULE_INJECTION_GUARD
    assert lens_f.reason == cpd_f.reason == "injection-guard"

    # Path slugs intentionally differ -- callers route the diagnostic
    # to the right seam (the JobSpec field vs. the on-disk file).
    assert lens_f.path == "prompt.system"
    assert cpd_f.path == "custom_prompt_dir/system.txt"
    assert lens_f.path != cpd_f.path

    # Message bodies share the §11.5 reference and the required
    # substring; only the path-label prefix differs. Stripping the
    # path label from each message must yield byte-identical tails.
    lens_tail = lens_f.message.replace(lens_f.path, "<PATH>")
    cpd_tail = cpd_f.message.replace(cpd_f.path, "<PATH>")
    assert lens_tail == cpd_tail


# ---------------------------------------------------------------------------
# Acceptance #4 -- mutation gate. Bypassing the guard on the
# custom-prompt-dir path flips the verdict.
# ---------------------------------------------------------------------------


def test_mutation_bypassing_predicate_flips_custom_prompt_dir_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Mutation gate: stub :func:`schema.contains_required_substring`
    at the preflight-side import site to always-True. The previously
    rejected ``system.txt`` now passes through cleanly -- the gate
    that pins INV-003 detects this regression.

    The double-edged shape is intentional: the test confirms both
    that (a) without the mutation the path rejects, and (b) with the
    mutation the path accepts. A future refactor that hard-codes a
    private predicate inside :func:`read_custom_prompt_dir` would
    leave the path rejecting even with the stub installed -- in that
    case the mutation would not flip the verdict and this test would
    fail, surfacing the divergence."""
    # Sanity check the un-mutated path rejects.
    pre_mutation = _cpd_path_failures(tmp_path, system=_BAD_SYSTEM)
    assert len(pre_mutation) == 1
    assert pre_mutation[0].rule == RULE_INJECTION_GUARD

    # Mutate the shared predicate at the preflight-side import. The
    # preflight module imports :func:`contains_required_substring`
    # by name, so the patch must target the preflight namespace
    # binding -- patching the schema-side binding alone would not
    # rebind the preflight import.
    monkeypatch.setattr(
        "superclaude.cli.swarm.preflight.contains_required_substring",
        lambda _h, _n: True,
    )

    # With the mutation in place, the same content now passes. The
    # reader returns the trio without raising, proving the rejection
    # in :func:`_cpd_path_failures` was driven by the shared
    # predicate -- not by a custom-prompt-dir-only side channel.
    _write_cpd(tmp_path, system=_BAD_SYSTEM)
    system, _, _ = read_custom_prompt_dir(
        tmp_path, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
    )
    assert system == _BAD_SYSTEM


def test_mutation_skipping_guard_call_would_fail_parity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Complementary mutation: stub
    :func:`enforce_injection_guard` to a no-op at the preflight-side
    import. The custom-prompt-dir path now bypasses the §11.5 check
    entirely -- a more aggressive regression than the predicate
    mutation. The reader accepts the bad fixture, demonstrating that
    the production path's rejection flowed through this exact helper
    and not a duplicate inline check.

    Pinning both mutations (predicate-level and helper-level) covers
    the two refactor shapes that could silently weaken the
    custom-prompt-dir guard: a predicate split or a guard-call
    removal."""
    monkeypatch.setattr(
        "superclaude.cli.swarm.preflight.enforce_injection_guard",
        lambda **_kwargs: [],
    )

    _write_cpd(tmp_path, system=_BAD_SYSTEM)
    # With the helper stubbed to a no-op, the reader no longer
    # rejects the bad system.txt -- confirming the production
    # rejection flows through this exact call site.
    system, _, _ = read_custom_prompt_dir(
        tmp_path, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
    )
    assert system == _BAD_SYSTEM
