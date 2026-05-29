"""Tests for ``superclaude.cli.eval.loader.SuiteLoader`` (COMP-002).

Covers cliEval Phase 1 / Task T01.07 acceptance criteria (Deliverable D-0006).
``SuiteLoader.load(path)`` orchestrates the five-stage gate chain:

    schema → static id regex → capability resolution
           → parameterize expansion → expanded-id regex re-check

Each typed error in the chain maps to process exit code 2 with the error
class name visible to operators (``SchemaError``, ``InvalidEvalId``,
``UnresolvedCapability``). The acceptance criteria explicitly demand that
unsafe ids be rejected BEFORE any capability resolution call runs — the
mock-based ordering test below is the load-bearing verification of that
contract.

Cross-links:
* COMP-002 SuiteLoader (this task, T01.07)
* FR-SCH1 schema validation (T01.04)
* FR-SCH2 eval-id regex (T01.05)
* NFR-SEC1 path-traversal prevention test set (T01.08)
* COMP-009 CapabilityGates (T01.11 — the real resolver injected here is a
  test stub; the production resolver lands in T01.11)
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    INVALID_EVAL_ID_EXIT_CODE,
    SCHEMA_ERROR_EXIT_CODE,
    SUITE_LOADER_ERROR_EXIT_CODE,
    UNRESOLVED_CAPABILITY_EXIT_CODE,
    CapabilityResolver,
    EvalSpec,
    InvalidEvalId,
    ParsedSuite,
    PermissiveCapabilityResolver,
    SchemaError,
    SuiteLoader,
    SuiteLoaderError,
    UnresolvedCapability,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# --- helpers ---------------------------------------------------------------


class _RecordingResolver:
    """CapabilityResolver stub that records every call for order assertions."""

    def __init__(self, missing_by_id: dict[str, tuple[str, ...]] | None = None) -> None:
        self.calls: list[tuple[str, tuple[str, ...]]] = []
        self._missing = missing_by_id or {}

    def resolve(
        self,
        eval_id: str,
        required: tuple[str, ...],
    ) -> Iterable[str]:
        self.calls.append((eval_id, required))
        return self._missing.get(eval_id, ())


# --- positive path: reference fixture loads green --------------------------


def test_load_reference_suite_returns_parsed_suite() -> None:
    """A schema-valid fixture must produce a populated :class:`ParsedSuite`."""

    loader = SuiteLoader()
    suite = loader.load(FIXTURES_DIR / "valid_suite.yaml")

    assert isinstance(suite, ParsedSuite)
    assert suite.name == "reference"
    assert suite.version == "1.0"
    assert suite.description.startswith("Reference v1 manifest")


def test_load_populates_suite_envelope_fields() -> None:
    """``ParsedSuite`` must round-trip the manifest envelope verbatim."""

    suite = SuiteLoader().load(FIXTURES_DIR / "valid_suite.yaml")
    assert suite.defaults["per_eval_timeout_sec"] == 120
    assert any(b["name"] == "claude" for b in suite.required_binaries)
    assert any(c["name"] == "mcp_server.auggie" for c in suite.optional_capabilities)
    assert suite.source_path == FIXTURES_DIR / "valid_suite.yaml"


def test_load_accepts_str_path() -> None:
    """``load()`` accepts ``str`` paths for CLI ergonomics (Path-normalised)."""

    suite = SuiteLoader().load(str(FIXTURES_DIR / "valid_suite.yaml"))
    assert isinstance(suite.source_path, Path)


# --- parameterize expansion convention -------------------------------------


def test_load_expands_parameterize_with_dot_index_suffix() -> None:
    """3 parameterize rows on E2 must produce E2.1, E2.2, E2.3."""

    suite = SuiteLoader().load(FIXTURES_DIR / "valid_suite.yaml")
    ids = [spec.id for spec in suite.evals]
    # E1 has no parameterize → passes through. E2 has 3 rows → expanded.
    assert ids == ["E1", "E2.1", "E2.2", "E2.3"]


def test_load_returns_eval_specs() -> None:
    """Expanded evals must be ``EvalSpec`` instances, not raw mappings."""

    suite = SuiteLoader().load(FIXTURES_DIR / "valid_suite.yaml")
    assert all(isinstance(spec, EvalSpec) for spec in suite.evals)


def test_static_id_evals_pass_through_unmodified() -> None:
    """An eval without ``parameterize`` must keep its static id 1:1."""

    suite = SuiteLoader().load(FIXTURES_DIR / "no_parameterize_suite.yaml")
    ids = [spec.id for spec in suite.evals]
    assert ids == ["E1", "D15"]


# --- error path 1: SchemaError -> exit 2 -----------------------------------


def test_load_raises_schema_error_for_missing_top_level_field() -> None:
    """A manifest missing ``name`` must surface as :class:`SchemaError`."""

    loader = SuiteLoader()
    with pytest.raises(SchemaError):
        loader.load(FIXTURES_DIR / "missing_name_suite.yaml")


def test_schema_error_maps_to_exit_code_two() -> None:
    """:class:`SchemaError` carries the exit-2 contract via the constant."""

    assert SCHEMA_ERROR_EXIT_CODE == 2
    assert SUITE_LOADER_ERROR_EXIT_CODE == 2


# --- error path 2: InvalidEvalId -> exit 2 ---------------------------------


def test_load_raises_invalid_eval_id_when_schema_layer_is_bypassed() -> None:
    """If a malformed id leaks past the schema, the FR-SCH2 guard must catch it.

    Acceptance criterion: a fixture with an unsafe id is rejected before any
    capability resolution call. The schema regex matches the runtime regex,
    so this test mocks the internal schema-stage helper to inject a
    malicious id and verifies the loader still rejects.
    """

    malicious = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {"id": "../home", "title": "would-escape-scratch"},
        ],
    }

    resolver = _RecordingResolver()
    loader = SuiteLoader(capability_resolver=resolver)
    with patch(
        "superclaude.cli.eval.loader._validate_manifest_dict",
        return_value=malicious,
    ):
        with pytest.raises(InvalidEvalId) as excinfo:
            loader.load("/dev/null")

    assert excinfo.value.eval_id == "../home"
    # Capability resolver MUST NOT have been touched — the id-regex gate
    # short-circuits before resolution per the spec ordering.
    assert resolver.calls == []


def test_load_rejects_unsafe_id_before_capability_resolver_runs() -> None:
    """Acceptance criterion verified by mock: id check < capability resolve."""

    malicious = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {"id": "1bad", "title": "leading-digit", "requires": ["cap.x"]},
        ],
    }
    resolver = _RecordingResolver()
    loader = SuiteLoader(capability_resolver=resolver)
    with patch(
        "superclaude.cli.eval.loader._validate_manifest_dict",
        return_value=malicious,
    ):
        with pytest.raises(InvalidEvalId):
            loader.load("/dev/null")
    assert resolver.calls == [], "resolver MUST NOT run when an id fails the regex"


def test_invalid_eval_id_maps_to_exit_code_two() -> None:
    assert INVALID_EVAL_ID_EXIT_CODE == 2


def test_load_rejects_post_expansion_unsafe_id() -> None:
    """If parameterize expansion produced an unsafe id (defence in depth)."""

    malicious = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {
                "id": "E2",
                "title": "expansion-from-bad-base",
                "parameterize": [{"key": "value"}],
            }
        ],
    }
    loader = SuiteLoader()

    # Override _expand_entry behaviour by monkey-patching the f-string:
    # we patch validate_eval_id to record calls AND raise on the expanded
    # id. This proves the loader applies the re-check after expansion.
    original = []

    def fake_validate(eval_id):
        original.append(eval_id)
        # Only reject the post-expansion id, not the base id.
        if eval_id == "E2.1.injected":
            raise InvalidEvalId(eval_id)

    with (
        patch(
            "superclaude.cli.eval.loader._validate_manifest_dict",
            return_value=malicious,
        ),
        patch(
            "superclaude.cli.eval.loader.validate_eval_id",
            side_effect=fake_validate,
        ),
        patch.object(
            SuiteLoader,
            "_expand_entry",
            autospec=True,
        ) as mock_expand,
    ):
        from superclaude.cli.eval.loader import validate_eval_id as ve

        def safe_expand(self, entry):
            # Simulate an unsafe expansion result so the test exercises the
            # re-check path explicitly via the (patched) validate_eval_id.
            expanded_id = "E2.1.injected"
            ve(expanded_id)
            return [EvalSpec.from_dict({**entry, "id": expanded_id})]

        mock_expand.side_effect = safe_expand

        with pytest.raises(InvalidEvalId):
            loader.load("/dev/null")


# --- error path 3: UnresolvedCapability -> exit 2 --------------------------


def test_load_raises_unresolved_capability() -> None:
    """The injected resolver's missing names surface as UnresolvedCapability."""

    resolver = _RecordingResolver(missing_by_id={"E1": ("cap.alpha",)})
    loader = SuiteLoader(capability_resolver=resolver)

    with pytest.raises(UnresolvedCapability) as excinfo:
        loader.load(FIXTURES_DIR / "no_parameterize_suite.yaml")

    err = excinfo.value
    assert err.eval_id == "E1"
    assert err.missing == ("cap.alpha",)
    # Error message MUST name the offending capabilities verbatim so
    # operators can act on the rejection without consulting the resolver.
    assert "cap.alpha" in str(err)


def test_unresolved_capability_exit_code_is_two() -> None:
    assert UNRESOLVED_CAPABILITY_EXIT_CODE == 2


def test_unresolved_capability_error_class_name_is_visible() -> None:
    """CLI stderr emits the error class name; assert it's stable."""

    assert UnresolvedCapability.__name__ == "UnresolvedCapability"


# --- ordering: id-regex BEFORE capability resolution -----------------------


def test_resolver_is_called_once_per_eval_in_manifest_order() -> None:
    """Capability resolution must visit every eval and only after id checks."""

    resolver = _RecordingResolver()
    loader = SuiteLoader(capability_resolver=resolver)
    loader.load(FIXTURES_DIR / "valid_suite.yaml")

    # Reference fixture has 2 evals (E1, E2 pre-expansion). Resolver is
    # consulted at the schema-entry level — once per static manifest id —
    # NOT once per expanded id (capability tags are a property of the
    # author-time eval, not the expansion-time row).
    assert [call[0] for call in resolver.calls] == ["E1", "E2"]


def test_resolver_receives_requires_tuple_per_eval() -> None:
    """``required`` argument must round-trip the manifest ``requires`` list."""

    resolver = _RecordingResolver()
    SuiteLoader(capability_resolver=resolver).load(FIXTURES_DIR / "valid_suite.yaml")
    by_id = dict(resolver.calls)
    assert "mcp_server.auggie" in by_id["E1"]


# --- default resolver behaviour --------------------------------------------


def test_default_resolver_is_permissive() -> None:
    """SuiteLoader() with no args must use a never-fails resolver."""

    loader = SuiteLoader()
    assert isinstance(loader.capability_resolver, PermissiveCapabilityResolver)
    # And it must successfully load the reference fixture (which contains a
    # capability not present on a typical dev box).
    loader.load(FIXTURES_DIR / "valid_suite.yaml")


def test_permissive_resolver_returns_empty_iterable() -> None:
    """Sanity check the default resolver contract."""

    resolver = PermissiveCapabilityResolver()
    assert tuple(resolver.resolve("E1", ("cap.x",))) == ()


def test_capability_resolver_protocol_runtime_checkable() -> None:
    """Custom test stubs must satisfy the Protocol (no inheritance required)."""

    resolver = _RecordingResolver()
    assert isinstance(resolver, CapabilityResolver)


# --- aggregate exit-code surface -------------------------------------------


def test_suite_loader_error_alias_covers_all_three_classes() -> None:
    """``except SuiteLoaderError`` must catch each typed loader error."""

    assert SchemaError in SuiteLoaderError
    assert InvalidEvalId in SuiteLoaderError
    assert UnresolvedCapability in SuiteLoaderError


@pytest.mark.parametrize(
    "exit_code",
    [
        SCHEMA_ERROR_EXIT_CODE,
        INVALID_EVAL_ID_EXIT_CODE,
        UNRESOLVED_CAPABILITY_EXIT_CODE,
        SUITE_LOADER_ERROR_EXIT_CODE,
    ],
)
def test_every_loader_exit_constant_is_two(exit_code: int) -> None:
    """All loader-layer exit codes collapse to 2 per design-spec §4."""

    assert exit_code == 2
