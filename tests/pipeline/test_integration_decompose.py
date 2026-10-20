"""Integration tests for decomposition pipeline pass -- T01.04."""

from __future__ import annotations

from superclaude.cli.pipeline.deliverables import decompose_deliverables
from superclaude.cli.pipeline.models import Deliverable, DeliverableKind


class TestPipelineIntegration:
    """Integration tests verifying decomposition pass behavior in pipeline context."""

    def _make_spec_deliverables(self) -> list[Deliverable]:
        """Known spec input: 2 behavioral + 1 doc deliverable."""
        return [
            Deliverable(id="D-1", description="Implement retry with bounded attempts"),
            Deliverable(id="D-2", description="Document API endpoint"),
            Deliverable(id="D-3", description="Parse configuration from YAML file"),
        ]

    def test_known_spec_produces_implement_verify_pairs(self):
        """Known spec input produces correct Implement/Verify pairs."""
        deliverables = self._make_spec_deliverables()
        result = decompose_deliverables(deliverables)

        # 2 behavioral (split to 4) + 1 doc (pass through) = 5
        assert len(result) == 5

        # Check behavioral pairs
        assert result[0].id == "D-1.a"
        assert result[0].kind == DeliverableKind.IMPLEMENT
        assert result[1].id == "D-1.b"
        assert result[1].kind == DeliverableKind.VERIFY

        # Check doc pass-through
        assert result[2].id == "D-2"
        assert result[2].description == "Document API endpoint"

        # Check second behavioral pair
        assert result[3].id == "D-3.a"
        assert result[3].kind == DeliverableKind.IMPLEMENT
        assert result[4].id == "D-3.b"
        assert result[4].kind == DeliverableKind.VERIFY

    def test_non_behavioral_unchanged(self):
        deliverables = [
            Deliverable(id="D-1", description="Document API endpoints"),
            Deliverable(id="D-2", description="Describe the auth flow"),
        ]
        result = decompose_deliverables(deliverables)
        assert len(result) == 2
        assert result[0].id == "D-1"
        assert result[1].id == "D-2"
        assert [d.to_dict() for d in result] == [d.to_dict() for d in deliverables]

    def test_milestone_order_preserved(self):
        """Deliverable ordering within a milestone is preserved."""
        deliverables = [
            Deliverable(id="D-1", description="Implement feature A"),
            Deliverable(id="D-2", description="Document feature A"),
            Deliverable(id="D-3", description="Implement feature B"),
        ]
        result = decompose_deliverables(deliverables)

        # D-1 splits first, then D-2 passes through, then D-3 splits
        ids = [d.id for d in result]
        assert ids == ["D-1.a", "D-1.b", "D-2", "D-3.a", "D-3.b"]

    def test_idempotency_byte_identical(self):
        """Running the pipeline twice produces identical output."""
        deliverables = self._make_spec_deliverables()
        first = decompose_deliverables(deliverables)
        second = decompose_deliverables(first)

        assert len(first) == len(second)
        for a, b in zip(first, second):
            assert a.to_dict() == b.to_dict()

    def test_verify_deliverables_contain_state_assertions(self):
        """Release Gate Rule 3: .b deliverables contain state assertions."""
        deliverables = [
            Deliverable(id="D-1", description="Implement retry logic"),
        ]
        result = decompose_deliverables(deliverables)
        verify = result[1]
        assert verify.id == "D-1.b"
        assert verify.kind == DeliverableKind.VERIFY
        # Rule 3: must contain state assertion or boundary case
        assert "post-condition assertions" in verify.description
        assert "input domain boundaries" in verify.description

    def test_empty_input(self):
        assert decompose_deliverables([]) == []

    def test_all_behavioral(self):
        """All behavioral deliverables double in count."""
        deliverables = [
            Deliverable(id=f"D-{i}", description=f"Implement feature {i}")
            for i in range(5)
        ]
        result = decompose_deliverables(deliverables)
        assert len(result) == 10
        # All even indices are .a, odd are .b
        for i in range(0, 10, 2):
            assert result[i].id.endswith(".a")
            assert result[i + 1].id.endswith(".b")
