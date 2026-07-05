"""Swarm test package conftest -- IMM/INV marker registry (T08.03 / NFR-007).

This conftest pins the per-IMM and per-INV acceptance coverage matrix so
``uv run pytest tests/swarm/ -m imm`` and ``-m inv`` select disjoint,
enumerable subsets. The markers themselves are registered in
``pyproject.toml`` under ``[tool.pytest.ini_options]`` so ``--strict-markers``
accepts them globally. This module documents the IMM/INV → test-file
mapping and surfaces it as a fixture for any future suite-consolidation
work (T08.09 / T08.10).

Mapping (canonical, from phase-8-tasklist §T08.03 + roadmap NFR-007):

IMM (5 cases):
    * IMM-3 parallelism                   -- test_imm3_parallel.py
    * IMM-4 empty-target STOP (49-byte)   -- test_imm4_empty_target.py
    * IMM-5 status matrix                 -- test_imm5_status.py
    * IMM-6 atomic-write mid-write kill   -- test_imm6_atomic_write.py
    * §11.5 end-marker target safety      -- test_prompt_injection_neutralization.py

INV (7 cases):
    * INV-001 manifest lens rehydration   -- test_resume_uses_manifest_lens.py
    * INV-002 Python-only dispatch        -- test_concurrency_python_only.py
    * INV-003 custom-prompt-dir guard     -- test_custom_prompt_dir_injection_guard.py
    * INV-005 worker-vs-pool guard        -- test_inv005_pool_guard.py
    * INV-007 empty-pool failure          -- test_inv007_empty_pool.py
    * INV-010 resume merge regen          -- test_resume_regenerates_merge.py
    * INV-014 escape-hatch isomorphism    -- test_escape_hatch_guard_parity.py

Each backing module sets ``pytestmark = pytest.mark.imm`` (or ``inv``) at
module scope so every test it carries inherits the marker -- selecting
the subset with ``-m imm`` / ``-m inv`` then yields all assertions
discharging that case.
"""

from __future__ import annotations

import pytest

IMM_COVERAGE_MAP: dict[str, str] = {
    "IMM-3": "test_imm3_parallel.py",
    "IMM-4": "test_imm4_empty_target.py",
    "IMM-5": "test_imm5_status.py",
    "IMM-6": "test_imm6_atomic_write.py",
    "11.5": "test_prompt_injection_neutralization.py",
}

INV_COVERAGE_MAP: dict[str, str] = {
    "INV-001": "test_resume_uses_manifest_lens.py",
    "INV-002": "test_concurrency_python_only.py",
    "INV-003": "test_custom_prompt_dir_injection_guard.py",
    "INV-005": "test_inv005_pool_guard.py",
    "INV-007": "test_inv007_empty_pool.py",
    "INV-010": "test_resume_regenerates_merge.py",
    "INV-014": "test_escape_hatch_guard_parity.py",
}


@pytest.fixture(scope="session")
def imm_coverage_map() -> dict[str, str]:
    """Return the canonical IMM-case → test-file map.

    Suite-consolidation work (T08.09 / TEST-001) should derive its
    enumeration from this fixture so the canonical mapping stays in
    exactly one place.
    """

    return dict(IMM_COVERAGE_MAP)


@pytest.fixture(scope="session")
def inv_coverage_map() -> dict[str, str]:
    """Return the canonical INV-case → test-file map.

    Suite-consolidation work (T08.10 / TEST-002) should derive its
    enumeration from this fixture so the canonical mapping stays in
    exactly one place.
    """

    return dict(INV_COVERAGE_MAP)
