"""File-based evidence loading for detection-contract setup."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SURFACE_FILES = {
    "reviews": "gh-reviews.json",
    "comments": "gh-comments.json",
    "check_runs": "gh-check-runs.json",
}


@dataclass(frozen=True)
class EvidenceBundle:
    """Captured PR evidence loaded from disk without live GitHub access."""

    probe_dir: Path
    repo: str | None
    pr_number: int | None
    captured_at: str | None
    surfaces: list[str]
    # Requirement §4.5/§8: omitted surfaces must be reported distinctly from present/validated surfaces.
    omitted_surfaces: list[str]
    reviews: list[dict[str, Any]]
    comments: list[dict[str, Any]]
    check_runs: list[dict[str, Any]]
    combined_payload: dict[str, Any]
    sha256: str
    pagination_complete: bool | None
    # Requirement §6.3/§7.6: cross-PR evidence validates shape only, never current-PR readiness.
    cross_pr_shape_only: bool = False

    def summary(self) -> str:
        """Render safe metadata only; never include raw payload bodies."""
        return "\n".join(
            [
                f"probe_dir={self.probe_dir}",
                f"repo={self.repo or '<unknown>'}",
                f"pr_number={self.pr_number if self.pr_number is not None else '<unknown>'}",
                f"captured_at={self.captured_at or '<unknown>'}",
                f"surfaces={','.join(self.surfaces) or '<none>'}",
                f"omitted_surfaces={','.join(self.omitted_surfaces) or '<none>'}",
                f"counts=reviews:{len(self.reviews)},comments:{len(self.comments)},check_runs:{len(self.check_runs)}",
                f"sha256={self.sha256}",
                f"pagination_complete={self.pagination_complete}",
                f"cross_pr_shape_only={self.cross_pr_shape_only}",
            ]
        )


def load_evidence(probe_dir: Path) -> EvidenceBundle:
    """Load captured evidence files from ``probe_dir`` and compute canonical SHA-256."""
    root = Path(probe_dir)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"probe evidence directory not found: {root}")

    combined_file = root / "combined-payload.json"
    manifest = _load_optional_json(root / "manifest.json")
    present_surfaces: list[str] = []
    omitted_surfaces: list[str] = []

    loaded_combined = combined_file.exists()
    if loaded_combined:
        combined_payload = _load_json(combined_file)
    else:
        combined_payload = {}

    surface_payloads: dict[str, list[dict[str, Any]]] = {}
    loaded_surface = False
    for surface, filename in SURFACE_FILES.items():
        path = root / filename
        if path.exists():
            loaded_surface = True
            present_surfaces.append(surface)
            surface_payloads[surface] = _as_list_of_dicts(_load_json(path), surface)
        else:
            omitted_surfaces.append(surface)
            surface_payloads[surface] = []

    if not loaded_combined and not loaded_surface:
        raise FileNotFoundError(f"no captured evidence JSON found under: {root}")

    if not combined_payload:
        combined_payload = {
            "reviews": surface_payloads["reviews"],
            "comments": surface_payloads["comments"],
            "check_runs": surface_payloads["check_runs"],
        }
    else:
        for surface in SURFACE_FILES:
            value = _surface_from_combined(combined_payload, surface)
            if value is not None:
                surface_payloads[surface] = value
                if surface not in present_surfaces:
                    present_surfaces.append(surface)
                if surface in omitted_surfaces:
                    omitted_surfaces.remove(surface)

    metadata = _metadata_from_payload(combined_payload, manifest)
    canonical = json.dumps(
        combined_payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return EvidenceBundle(
        probe_dir=root,
        repo=metadata.get("repo"),
        pr_number=_as_int(metadata.get("pr_number")),
        captured_at=metadata.get("captured_at") or _latest_mtime(root),
        surfaces=sorted(present_surfaces),
        omitted_surfaces=sorted(omitted_surfaces),
        reviews=surface_payloads["reviews"],
        comments=surface_payloads["comments"],
        check_runs=surface_payloads["check_runs"],
        combined_payload=combined_payload,
        sha256=hashlib.sha256(canonical).hexdigest(),
        pagination_complete=_pagination_complete(combined_payload, manifest),
        cross_pr_shape_only=bool(metadata.get("cross_pr_shape_only", False)),
    )


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = _load_json(path)
    return data if isinstance(data, dict) else {}


def _as_list_of_dicts(value: Any, surface: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        nested = value.get(surface)
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, dict)]
        for key in ("items", "nodes", "data"):
            items = value.get(key)
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]
    return []


def _surface_from_combined(
    payload: dict[str, Any], surface: str
) -> list[dict[str, Any]] | None:
    if surface in payload:
        return _as_list_of_dicts(payload.get(surface), surface)
    aliases = {"check_runs": ("checkRuns", "checks", "check_runs")}
    for alias in aliases.get(surface, (surface,)):
        if alias in payload:
            return _as_list_of_dicts(payload.get(alias), surface)
    return None


def _metadata_from_payload(
    combined_payload: dict[str, Any], manifest: dict[str, Any]
) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for source in (manifest, combined_payload.get("metadata"), combined_payload):
        if isinstance(source, dict):
            _copy_first(metadata, source, "repo", "repository", "owner_repo")
            _copy_first(metadata, source, "pr_number", "pr", "pull_request_number")
            _copy_first(metadata, source, "captured_at", "capturedAt", "fetched_at")
            _copy_first(metadata, source, "cross_pr_shape_only", "shape_only")
    return metadata


def _copy_first(
    target: dict[str, Any], source: dict[str, Any], key: str, *aliases: str
) -> None:
    if key in target:
        return
    for candidate in (key, *aliases):
        value = source.get(candidate)
        if value not in (None, ""):
            target[key] = value
            return


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _latest_mtime(root: Path) -> str | None:
    mtimes = [p.stat().st_mtime for p in root.glob("*.json") if p.is_file()]
    if not mtimes:
        return None
    from datetime import datetime, timezone

    return datetime.fromtimestamp(max(mtimes), tz=timezone.utc).isoformat()


def _pagination_complete(
    combined_payload: dict[str, Any], manifest: dict[str, Any]
) -> bool | None:
    for source in (manifest, combined_payload.get("metadata"), combined_payload):
        if isinstance(source, dict):
            for key in ("pagination_complete", "complete", "has_next_page"):
                value = source.get(key)
                if isinstance(value, bool):
                    return not value if key == "has_next_page" else value
    return None
