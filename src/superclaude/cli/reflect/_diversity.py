"""Diversity helpers shared by reflect ensemble and fallback code."""

from __future__ import annotations

from superclaude.cli.swarm.models import WorkerResult


def compute_model_class_diversity(workers: list[WorkerResult]) -> str:
    """Return ``full`` when at least two succeeded model ids are distinct."""
    distinct_model_ids = {
        worker.model_id
        for worker in workers
        if worker.status == "success" and worker.model_id
    }
    return "full" if len(distinct_model_ids) >= 2 else "insufficient"


def compute_vendor_diversity(workers: list[WorkerResult]) -> str | None:
    """Return vendor diversity over the succeeded reviewers (OI-1: DERIVED).

    Classifies each succeeded worker's ``model_id`` to a vendor and returns
    ``"single"`` when all succeeded reviewers share one vendor (so the FR-11
    single-vendor degrade can fire), ``"multi"`` when ≥2 vendors are present, and
    ``None`` when fewer than two reviewers survived (the single-reviewer-fallback
    trigger owns the reason slug). Distinct ``model_id``s alone are NOT treated as
    multi-vendor — two distinct same-vendor models resolve to ``"single"``.
    """
    succeeded = [worker for worker in workers if worker.status == "success"]
    if len(succeeded) < 2:
        return None
    vendors = {
        _vendor_from_model_id(worker.model_id)
        for worker in succeeded
        if worker.model_id
    }
    return "multi" if len(vendors) >= 2 else "single"


def _vendor_from_model_id(model_id: str) -> str:
    """Classify a proxy ``model_id`` to a coarse vendor family."""
    lowered = model_id.lower()
    for marker, vendor in (
        ("qwen", "qwen"),
        ("deepseek", "deepseek"),
        ("gpt", "openai"),
        ("o1", "openai"),
        ("gemini", "google"),
        ("llama", "meta"),
        ("mistral", "mistral"),
        ("claude", "anthropic"),
    ):
        if marker in lowered:
            return vendor
    # Fall back to the leading path/colon segment as a best-effort vendor key.
    return lowered.split("/", 1)[0].split(":", 1)[0] or "unknown"
