"""Wiring analysis configuration and whitelist loading.

Provides WiringConfig for controlling wiring analysis behavior including
provider directory conventions, exclude patterns, registry detection patterns,
and whitelist-based suppression. Whitelist strictness varies by rollout_mode
per OQ-3 decision (D-0001).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)

# Default regex patterns for dispatch registry detection (section 4.2.1).
# Matches module-level dict assignments named like STEP_REGISTRY, FOO_DISPATCH, etc.
DEFAULT_REGISTRY_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^[A-Z_]*REGISTRY$"),
    re.compile(r"^[A-Z_]*DISPATCH$"),
    re.compile(r"^[A-Z_]*HANDLERS$"),
    re.compile(r"^[A-Z_]*ROUTER$"),
    re.compile(r"^[A-Z_]*BUILDERS$"),
    re.compile(r"^PROGRAMMATIC_RUNNERS$"),
)


class WiringConfigError(Exception):
    """Raised for invalid whitelist or config in non-shadow rollout modes."""


@dataclass
class WhitelistEntry:
    """A single suppression entry from wiring_whitelist.yaml."""

    symbol: str
    reason: str
    finding_type: str = "unwired_callable"


@dataclass
class WiringConfig:
    """Configuration for the wiring analysis engine.

    Fields:
        provider_dir_names: Directory basenames treated as provider directories
            for orphan module detection (section 5.2.2).
        exclude_patterns: Glob patterns for files excluded from analysis.
            Excluded files increment files_skipped per OQ-2.
        registry_patterns: Compiled regex patterns for identifying dispatch
            registry variables in source files (section 5.2.3).
        whitelist_path: Path to wiring_whitelist.yaml for suppression entries.
            None means no whitelist suppression.
        rollout_mode: Controls strictness of whitelist validation and
            blocking semantics per OQ-3/OQ-6.
    """

    provider_dir_names: frozenset[str] = frozenset(
        {"steps", "handlers", "validators", "checks"}
    )
    exclude_patterns: list[str] = field(
        default_factory=lambda: ["test_*.py", "conftest.py", "__init__.py"]
    )
    registry_patterns: tuple[re.Pattern[str], ...] = DEFAULT_REGISTRY_PATTERNS
    whitelist_path: Path | None = None
    rollout_mode: Literal["shadow", "soft", "full"] = "shadow"


def load_whitelist(
    path: Path | None,
    rollout_mode: Literal["shadow", "soft", "full"] = "shadow",
) -> list[WhitelistEntry]:
    """Load suppression entries from a wiring whitelist YAML file.

    Args:
        path: Path to whitelist YAML. Returns empty list if None or nonexistent.
        rollout_mode: Controls error handling for malformed entries.
            - shadow: warn and skip malformed entries (OQ-3)
            - soft/full: raise WiringConfigError on malformed entries

    Returns:
        List of WhitelistEntry instances for suppression matching.
    """
    if path is None or not path.exists():
        return []

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        if rollout_mode == "shadow":
            logger.warning("Malformed whitelist YAML at %s: %s", path, exc)
            return []
        raise WiringConfigError(
            f"Malformed whitelist YAML at {path}: {exc}"
        ) from exc

    if not isinstance(raw, dict):
        if rollout_mode == "shadow":
            logger.warning("Whitelist at %s is not a mapping, skipping", path)
            return []
        raise WiringConfigError(f"Whitelist at {path} is not a mapping")

    entries: list[WhitelistEntry] = []

    for section_key in ("unwired_callables", "orphan_modules", "unwired_registries"):
        section = raw.get(section_key, [])
        if not isinstance(section, list):
            if rollout_mode == "shadow":
                logger.warning(
                    "Whitelist section '%s' is not a list, skipping", section_key
                )
                continue
            raise WiringConfigError(
                f"Whitelist section '{section_key}' is not a list"
            )

        # Map section keys to finding_type values
        finding_type_map = {
            "unwired_callables": "unwired_callable",
            "orphan_modules": "orphan_module",
            "unwired_registries": "unwired_registry",
        }
        finding_type = finding_type_map[section_key]

        for item in section:
            if not isinstance(item, dict) or "symbol" not in item:
                if rollout_mode == "shadow":
                    logger.warning(
                        "Malformed whitelist entry in '%s': %r, skipping",
                        section_key,
                        item,
                    )
                    continue
                raise WiringConfigError(
                    f"Malformed whitelist entry in '{section_key}': {item!r}"
                )

            entries.append(
                WhitelistEntry(
                    symbol=item["symbol"],
                    reason=item.get("reason", ""),
                    finding_type=finding_type,
                )
            )

    return entries
