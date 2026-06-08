"""Swarm configuration -- SwarmConfig dataclass + path resolution.

T01.09 (COMP-003): immutable runtime configuration for the
``superclaude swarm`` CLI verb. Mirrors the role of
``cli/sprint/config.py::SprintConfig`` but enforces ``frozen=True``
semantics so downstream pipeline stages (manifest snapshot DM-016,
dispatch M3, ResultContract emit DM-012) read from a single source of
truth: in-place mutation would silently break INV-001 / INV-016
(resolved-lens immutability).

Resolution happens at construction time:

* **Output directory** -- relative paths are resolved against ``work_dir``
  so callers can pass either absolute or repo-relative locations
  without ambiguity.
* **T2 proxy env-var contract (AC-017)** -- ``T2ProxyUrl`` /
  ``T2ProxyKey`` / ``T2Model01..T2Model09`` are read from the
  environment via :meth:`SwarmConfig.from_env`. Missing values are
  recorded as ``None`` / an empty tuple rather than raised; the
  structured failure path lives at dispatch time (INV-007 env-missing
  contract), keeping config construction itself total.
* **Operational defaults** -- ``dry_run``, ``debug``, ``log_level``
  default to the conservative values appropriate for a fresh shell.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional

__all__ = [
    "SwarmConfig",
    "DEFAULT_OUTPUT_DIR",
    "T2_PROXY_URL_ENV",
    "T2_PROXY_KEY_ENV",
    "T2_MODEL_ENV_PREFIX",
    "T2_MODEL_MAX_SLOTS",
]

# Default output directory for swarm job artifacts (resolved against
# ``work_dir`` when the caller does not specify one explicitly). Sits
# under ``.dev/`` so generated artifacts stay out of the distributable
# ``src/`` and ``.claude/`` trees per the repo's sync-discipline rule.
DEFAULT_OUTPUT_DIR: Path = Path(".dev/swarm-state")

# T2 proxy env-var contract (AC-017). Spelled exactly as documented in
# the roadmap so a grep for the constant lands on both the spec and the
# code.
T2_PROXY_URL_ENV = "T2ProxyUrl"
T2_PROXY_KEY_ENV = "T2ProxyKey"

# Per-worker model identifiers live in numbered slots ``T2Model01`` ..
# ``T2Model0N``. The prefix below is concatenated with a zero-padded
# 1-based index when probing the environment.
T2_MODEL_ENV_PREFIX = "T2Model0"

# Maximum number of T2 model slots probed from the environment. Bounded
# at nine because the documented suffix is a single digit (``0N``) and
# the preflight worker-count guard (INV-005 / OQ-007) will trip before
# realistic deployments hit this ceiling.
T2_MODEL_MAX_SLOTS = 9


@dataclass(frozen=True)
class SwarmConfig:
    """Immutable runtime configuration for the ``superclaude swarm`` verb.

    Construct via :meth:`from_env` when env-var resolution is required
    (the common path for CLI invocations) or directly when callers have
    already resolved every field (tests, programmatic callers, retries).

    Attributes:
        work_dir: Absolute working directory anchoring relative paths.
        output_dir: Absolute output directory for job artifacts.
        t2_proxy_url: Value of ``T2ProxyUrl`` at construction, or
            ``None`` when the variable is unset / empty.
        t2_proxy_key: Value of ``T2ProxyKey`` at construction, or
            ``None`` when unset / empty.
        t2_models: Tuple of per-slot model identifiers read from
            ``T2Model01`` .. ``T2Model09`` in slot order, skipping
            empty slots so the tuple is dense.
        dry_run: When True, the pipeline emits artifacts and stops
            short of dispatching workers.
        debug: When True, enables verbose logging at every stage.
        log_level: Default log level for the swarm logger
            (``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``).
    """

    work_dir: Path
    output_dir: Path
    t2_proxy_url: Optional[str] = None
    t2_proxy_key: Optional[str] = None
    t2_models: tuple[str, ...] = ()
    dry_run: bool = False
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(
        cls,
        *,
        work_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        env: Optional[Mapping[str, str]] = None,
        dry_run: bool = False,
        debug: bool = False,
        log_level: str = "INFO",
    ) -> "SwarmConfig":
        """Build a :class:`SwarmConfig` from process env + explicit overrides.

        ``work_dir`` defaults to the current working directory.
        ``output_dir`` defaults to :data:`DEFAULT_OUTPUT_DIR` resolved
        against ``work_dir``. ``env`` defaults to ``os.environ`` -- pass
        an explicit mapping in tests to keep the construction
        deterministic.

        Missing T2 env vars produce ``None`` / empty tuple rather than
        raising: the structured env-missing failure surface is the
        dispatch path (INV-007), not config construction. This keeps
        ``SwarmConfig.from_env`` total so callers can construct, log,
        and then decide how to react to absences.
        """
        env_map: Mapping[str, str] = env if env is not None else os.environ
        resolved_work = Path(work_dir).resolve() if work_dir else Path.cwd().resolve()
        resolved_output = cls._resolve_output_dir(resolved_work, output_dir)
        models = cls._collect_t2_models(env_map)
        return cls(
            work_dir=resolved_work,
            output_dir=resolved_output,
            t2_proxy_url=env_map.get(T2_PROXY_URL_ENV) or None,
            t2_proxy_key=env_map.get(T2_PROXY_KEY_ENV) or None,
            t2_models=models,
            dry_run=dry_run,
            debug=debug,
            log_level=log_level,
        )

    def resolve_path(self, path: Path | str) -> Path:
        """Resolve ``path`` against :attr:`work_dir` when relative.

        Absolute paths are returned unchanged after passing through
        :class:`Path` so callers always receive a ``Path`` instance.
        """
        candidate = Path(path)
        if candidate.is_absolute():
            return candidate
        return (self.work_dir / candidate).resolve()

    def missing_t2_env_vars(self) -> tuple[str, ...]:
        """Return the names of T2 env vars that were unset at construction.

        Helper for the INV-007 env-missing surface: dispatch checks this
        before opening the live transport and emits a structured error
        instead of letting httpx fail with an unhelpful 401/connection
        refused.
        """
        missing: list[str] = []
        if not self.t2_proxy_url:
            missing.append(T2_PROXY_URL_ENV)
        if not self.t2_proxy_key:
            missing.append(T2_PROXY_KEY_ENV)
        if not self.t2_models:
            missing.append(f"{T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS}")
        return tuple(missing)

    @staticmethod
    def _resolve_output_dir(
        work_dir: Path,
        output_dir: Optional[Path],
    ) -> Path:
        candidate = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR
        if candidate.is_absolute():
            return candidate
        return (work_dir / candidate).resolve()

    @staticmethod
    def _collect_t2_models(env_map: Mapping[str, str]) -> tuple[str, ...]:
        models: list[str] = []
        for index in range(1, T2_MODEL_MAX_SLOTS + 1):
            value = env_map.get(f"{T2_MODEL_ENV_PREFIX}{index}")
            if value:
                models.append(value)
        return tuple(models)
