"""Gate functions for deterministic Steps 1-2 of the cli-portify pipeline.

Step 1: validate-config  (EXEMPT)
Step 2: discover-components (STANDARD)

All gate functions return tuple[bool, str] per NFR-004.
EXEMPT tier gates always pass regardless of content.
STANDARD tier gates check frontmatter fields and basic structure.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from superclaude.cli.pipeline.models import GateCriteria

from ..steps.validate_config import ValidateConfigResult

# ---------------------------------------------------------------------------
# Gate criteria for Steps 1-2
# ---------------------------------------------------------------------------

# Step 1: validate-config — EXEMPT (deterministic; pass regardless of content)
VALIDATE_CONFIG_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=0,
    enforcement_tier="EXEMPT",
    semantic_checks=None,
)

# Step 2: discover-components — STANDARD (frontmatter + line count)
DISCOVER_COMPONENTS_GATE = GateCriteria(
    required_frontmatter_fields=["source_skill", "component_count"],
    min_lines=5,
    enforcement_tier="STANDARD",
    semantic_checks=None,
)

# Timing advisory limits (in seconds)
_VALIDATE_CONFIG_TIMING_LIMIT: float = 1.0
_DISCOVER_COMPONENTS_TIMING_LIMIT: float = 5.0


# ---------------------------------------------------------------------------
# Step 1 gate: validate-config
# ---------------------------------------------------------------------------


def gate_validate_config(result: ValidateConfigResult) -> tuple[bool, str]:
    """Gate for validate-config step (EXEMPT tier).

    Checks:
    - Internal consistency: valid=True iff errors is empty
    - Timing advisory: duration must be < 1s

    Returns (True, "") on pass.
    Returns (False, reason) on failure.
    """
    # Consistency check: valid=True must correlate with empty errors
    if result.valid and result.errors:
        return False, (f"Inconsistency: valid=True but errors present: {result.errors}")
    if not result.valid and not result.errors:
        return False, "Inconsistency: valid=False but no errors reported"

    # Timing advisory
    if result.duration_seconds > _VALIDATE_CONFIG_TIMING_LIMIT:
        return False, (
            f"Timing advisory exceeded: {result.duration_seconds:.3f}s > "
            f"{_VALIDATE_CONFIG_TIMING_LIMIT}s limit for validate-config"
        )

    return True, ""


# ---------------------------------------------------------------------------
# Step 2 gate: discover-components
# ---------------------------------------------------------------------------


def gate_discover_components(
    artifact_path: Path,
    actual_duration: Optional[float] = None,
) -> tuple[bool, str]:
    """Gate for discover-components step (STANDARD tier).

    Checks:
    - Artifact file exists
    - YAML frontmatter present
    - Required frontmatter fields: source_skill, component_count
    - Timing advisory (if actual_duration provided): < 5s

    Returns (True, "") on pass.
    Returns (False, reason) on failure.
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"

    content = artifact_path.read_text(encoding="utf-8")

    # Check for YAML frontmatter
    if not re.search(r"^---\s*$", content, re.MULTILINE):
        return False, "Missing YAML frontmatter in component inventory"

    # Extract frontmatter fields
    found_keys: set[str] = set()
    in_fm = False
    fence_count = 0
    for line in content.splitlines():
        if line.strip() == "---":
            fence_count += 1
            if fence_count == 1:
                in_fm = True
            elif fence_count == 2:
                break
            continue
        if in_fm and ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                found_keys.add(key)

    required_fields = ["source_skill", "component_count"]
    for field in required_fields:
        if field not in found_keys:
            return False, f"Missing required frontmatter field: '{field}'"

    # Timing advisory
    if (
        actual_duration is not None
        and actual_duration > _DISCOVER_COMPONENTS_TIMING_LIMIT
    ):
        return False, (
            f"Timing advisory exceeded: {actual_duration:.3f}s > "
            f"{_DISCOVER_COMPONENTS_TIMING_LIMIT}s limit for discover-components"
        )

    return True, ""
