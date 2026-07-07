"""Unit tests for reflect fallback slot-name factory binding."""

import pytest

from superclaude.cli.reflect.fallback import make_fallback_slot_factory
from superclaude.cli.swarm.commands import ModelPoolTooSmallError
from superclaude.cli.swarm.models import WorkerResult


class RecordingTransport:
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult(model_id=self.model_id)


def test_fallback_slot_factory_binds_slot_name_to_ladder_position() -> None:
    built_models: list[str] = []

    def build_transport(model_id: str) -> RecordingTransport:
        built_models.append(model_id)
        return RecordingTransport(model_id)

    factory = make_fallback_slot_factory(
        pool=("m-a", "m-b"),
        ladder=("T1Model01", "T1Model02"),
        build_transport=build_transport,
    )

    first = factory("T1Model01")
    second = factory("T1Model02")

    assert first.model_id == "m-a"
    assert second.model_id == "m-b"
    assert built_models == ["m-a", "m-b"]


def test_fallback_slot_factory_raises_when_pool_too_small_for_slot() -> None:
    factory = make_fallback_slot_factory(
        pool=("m-a",),
        ladder=("T1Model01", "T1Model02"),
        build_transport=RecordingTransport,
    )

    with pytest.raises(ModelPoolTooSmallError):
        factory("T1Model02")
