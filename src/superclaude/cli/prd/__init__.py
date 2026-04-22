"""PRD pipeline -- CLI-driven Product Requirements Document generation.

This package implements the `superclaude prd` command group.
Phase 1 modules: models, gates, inventory, filtering.
Phase 2 modules: prompts, config.
Phase 3 modules: monitor, process, logging_, diagnostics, tui, executor.
Phase 4 modules: commands (CLI surface).
"""

from .commands import prd_group
from .executor import PrdExecutor
from .models import PrdConfig

__all__ = ["prd_group", "PrdConfig", "PrdExecutor"]
