"""Mechanical merge module -- Phase 5 / COMP-010 / T05.02 surface.

This module owns the single highest-risk caller-facing boundary in the
swarm. It is invoked only by :func:`superclaude.cli.swarm.reduce.reduce_wave3`
in ``normalize+merge`` mode, behind the :class:`StatusPolicy.floor`
(``M >= floor``) gate, and its sole job is to concatenate each worker's
normalized body in slot-index order with a one-line provenance header.

Boundary contract (AC-011 / AC-012 -- enforced by T05.05 review):

ALLOWED operations -- the entire surface area this module may grow into:
    1. Verbatim concat of per-worker ``final_path`` file contents.
    2. Ordering by :attr:`WorkerResult.index` (slot index, 0..N-1).
       This is structural ordering of *sections*, not semantic ranking.
    3. Prepend one provenance header per section, exactly:
       ``## From {model_label} ({elapsed_ms}ms)``.

DISALLOWED operations -- any addition here is a boundary violation and
must trip T05.05 PR review, T05.08 LOC ceiling, T05.09 boundary test,
or T05.10 scoring-engine grep audit:
    * sort / rank / score / judge findings
    * dedup / filter / drop sections
    * rewrite / paraphrase / reformat content
    * reorder content *within* a worker section
    * cross-worker synthesis or alignment
    * frontmatter / YAML rewriting beyond verbatim passthrough

Scoring, ranking, and adversarial merge live in ``/sc:adversarial``;
this module is intentionally too small to host any of them.

The four structural guards on this file (see T05.05 acceptance):
    1. This docstring (allowed/disallowed enumeration).
    2. <=30 LOC body ceiling -- ``tests/swarm/test_merge_loc_ceiling.py``
       (T05.08, NFR-008).
    3. PR-review discipline on this file path -- documented in
       ``.github/workflows/`` PR-touch check (T05.09).
    4. 3-worker boundary test --
       ``tests/swarm/test_merge_mechanical_only.py`` (T05.09, NFR-009),
       complemented by ``tests/swarm/test_merge_no_transforms.py``
       (T05.11, AC-011 variant).
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import WorkerResult


def mechanical_merge(worker_results: list[WorkerResult]) -> str:
    sections: list[str] = []
    for wr in sorted(worker_results, key=lambda w: w.index):
        path = Path(wr.final_path) if wr.final_path else None
        body = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        header = f"## From {wr.model_label} ({wr.elapsed_ms}ms)"
        sections.append(f"{header}\n\n{body.rstrip()}\n")
    return "\n".join(sections)
