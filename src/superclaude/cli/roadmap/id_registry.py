"""Spec-ID registry — Contract #9 enforcement primitive.

This module implements the **Spec-ID Registry** mandated by
BUILD-REQUEST §R0 item 1 + §Contract item #9 (master:§Recurrence #4).

**Contract #9 invariant:** every requirement ID that appears in a merged
roadmap MUST belong to the union of:

    spec_ids ∪ accepted_deviation_ids

i.e. ``roadmap_id_set ⊆ spec_id_set ∪ accepted_deviation_id_set``.

The canonical "phantom-ID" incident the registry prevents is master report
row #4 (A12:F-A12-01): TUIBBS v1-MVP produced 54 ``phantom_id`` HIGHs
because a roadmap referenced ``D01..D54`` while the spec only defined
``D1, D3, D5``. Every prior remediation hardened orchestration around the
broken comparator; this registry is the comparator-side fix.

**Anti-duplication discipline (Contract #8):** This module does NOT
re-implement any ID pattern. It REUSES
:func:`superclaude.cli.roadmap.spec_parser.extract_requirement_ids` as the
single source of truth for ID regex literals. R0.3 will hoist the patterns
to ``superclaude.contracts.ID_PATTERNS``; the TODO comment below tracks
that migration.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

# R0.3: source the family list from the canonical contracts registry.
# The registry's ID extraction itself delegates to spec_parser, so this
# constant only enumerates KNOWN families. Contract #8 satisfied — no
# duplicate literal definition.
from superclaude.contracts import ID_PATTERNS as _ID_PATTERNS

_ID_PATTERN_KEYS: tuple[str, ...] = tuple(_ID_PATTERNS.keys())


@dataclass(frozen=True)
class SpecIdRegistry:
    """Immutable record of declared IDs for a single spec + accepted deviations.

    Fields are tuples (not lists) so the registry is hashable and safe to
    pass across pipeline boundaries. R1.2's :class:`PipelineEnvelope` will
    absorb this object as its ``spec_ids`` slot; the JSON sidecar written
    by the extract step is the proto-envelope.

    Parameters
    ----------
    fr_ids:
        Declared FR-family identifiers (canonical form from spec_parser).
    nfr_ids:
        Declared NFR-family identifiers.
    sc_ids:
        Declared Success-Criteria identifiers.
    g_ids:
        Declared Goal identifiers (G-family).
    d_ids:
        Declared Deviation/Decision identifiers (lenient pattern matches
        both ``D5`` and ``D-5``; master:§Recurrence #4 documents the
        asymmetry this lenient pattern previously caused with strict
        comparators).
    accepted_deviation_ids:
        IDs accepted via ``dev-*-accepted-deviation.md`` records in the
        output dir; merged from
        :func:`spec_patch.scan_accepted_deviation_records`.
    spec_hash:
        SHA-256 of the spec file content at registry-build time (16 chars,
        for cheap drift detection in PG2.2).
    spec_path:
        Absolute path to the spec file the registry was built from.
    """

    fr_ids: tuple[str, ...]
    nfr_ids: tuple[str, ...]
    sc_ids: tuple[str, ...]
    g_ids: tuple[str, ...]
    d_ids: tuple[str, ...]
    accepted_deviation_ids: tuple[str, ...]
    spec_hash: str
    spec_path: Path

    def union_of_known(self) -> frozenset[str]:
        """Return the frozen set of every known ID (spec + accepted)."""
        return frozenset(
            self.fr_ids
            + self.nfr_ids
            + self.sc_ids
            + self.g_ids
            + self.d_ids
            + self.accepted_deviation_ids
        )

    def contains(self, roadmap_id: str) -> bool:
        """Return ``True`` iff the given ID is in the union of known IDs.

        This is the Contract #9 containment primitive. Callers
        (e.g. the MERGE_GATE SemanticCheck) iterate IDs extracted from a
        roadmap and assert :meth:`contains` for each.
        """
        return roadmap_id in self.union_of_known()

    def to_dict(self) -> dict[str, list[str] | str]:
        """Return a JSON-serializable representation (sidecar format).

        The format is stable across R0.1 → R1.2 so the
        ``spec_id_registry.json`` sidecar absorbs cleanly into the
        :class:`PipelineEnvelope` when R1.2 lands.
        """
        return {
            "fr_ids": list(self.fr_ids),
            "nfr_ids": list(self.nfr_ids),
            "sc_ids": list(self.sc_ids),
            "g_ids": list(self.g_ids),
            "d_ids": list(self.d_ids),
            "accepted_deviation_ids": list(self.accepted_deviation_ids),
            "spec_hash": self.spec_hash,
            "spec_path": str(self.spec_path),
        }


def build_id_registry(
    spec_path: Path,
    accepted_deviations: list[str] | None = None,
) -> SpecIdRegistry:
    """Build a :class:`SpecIdRegistry` from a spec file.

    Reuses :func:`spec_parser.extract_requirement_ids` to honor Contract #8
    (no duplicate regex literals).

    Parameters
    ----------
    spec_path:
        Absolute path to a spec markdown file.
    accepted_deviations:
        Optional list of accepted deviation IDs (typically merged from
        :func:`spec_patch.scan_accepted_deviation_records`). ``None`` is
        treated as an empty list.

    Returns
    -------
    SpecIdRegistry
        Immutable registry. ``spec_hash`` is the first 16 hex chars of the
        SHA-256 of the spec file's UTF-8 bytes.
    """
    # Local import avoids a potential circular import if spec_parser ever
    # grows a reverse dependency on id_registry. Keeps the boundary clean.
    from .spec_parser import extract_requirement_ids

    text = spec_path.read_text(encoding="utf-8")
    spec_hash = sha256(text.encode("utf-8")).hexdigest()[:16]

    families = extract_requirement_ids(text)
    return SpecIdRegistry(
        fr_ids=tuple(families.get("FR", ())),
        nfr_ids=tuple(families.get("NFR", ())),
        sc_ids=tuple(families.get("SC", ())),
        g_ids=tuple(families.get("G", ())),
        d_ids=tuple(families.get("D", ())),
        accepted_deviation_ids=tuple(sorted(set(accepted_deviations or ()))),
        spec_hash=spec_hash,
        spec_path=spec_path,
    )


def extract_roadmap_ids(roadmap_text: str) -> frozenset[str]:
    """Extract every requirement-family ID present in a roadmap text.

    Like :func:`build_id_registry`, this REUSES
    :func:`spec_parser.extract_requirement_ids` (Contract #8 anti-duplication).
    Returned as a ``frozenset`` because the caller (MERGE_GATE
    SemanticCheck) only needs set-containment semantics.
    """
    from .spec_parser import extract_requirement_ids

    families = extract_requirement_ids(roadmap_text)
    flat: set[str] = set()
    for ids in families.values():
        flat.update(ids)
    return frozenset(flat)
