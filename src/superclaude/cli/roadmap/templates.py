"""Template path resolution for roadmap/tasklist output templates.

Resolves template filenames to absolute paths, handling both installed
package (importlib.resources) and development (src/ relative) layouts.
"""

from __future__ import annotations

import logging
from pathlib import Path

_log = logging.getLogger("superclaude.roadmap.templates")

ROADMAP_TEMPLATE = "roadmap_template.compressed.md"
TASKLIST_INDEX_TEMPLATE = "tasklist_index_template.md"
TASKLIST_PHASE_TEMPLATE = "tasklist_phase_template.md"

_EXAMPLES_PACKAGE = "superclaude.examples"


def get_template_path(name: str) -> Path:
    """Resolve a template filename to its absolute path.

    Tries importlib.resources first (works for installed packages),
    falls back to src-relative resolution (development mode).

    Parameters
    ----------
    name:
        Template filename, e.g. ``"roadmap_template.md"``.
        Use the module constants: ROADMAP_TEMPLATE,
        TASKLIST_INDEX_TEMPLATE, TASKLIST_PHASE_TEMPLATE.

    Returns
    -------
    Path
        Absolute path to the template file.

    Raises
    ------
    FileNotFoundError
        If the template cannot be located via either method.
    """
    # Method 1: importlib.resources (installed package)
    try:
        from importlib import resources

        ref = resources.files(_EXAMPLES_PACKAGE).joinpath(name)
        # resources.files() returns a Traversable; as_posix() works
        # on both Path and MultiplexedPath.
        resolved = Path(str(ref))
        if resolved.exists():
            _log.debug("template resolved via importlib.resources: %s", resolved)
            return resolved
    except (ModuleNotFoundError, TypeError):
        pass

    # Method 2: src-relative (development mode)
    src_relative = (
        Path(__file__).resolve().parent.parent.parent  # -> src/superclaude/
        / "examples"
        / name
    )
    if src_relative.exists():
        _log.debug("template resolved via src-relative: %s", src_relative)
        return src_relative

    raise FileNotFoundError(
        f"Template '{name}' not found. Searched: "
        f"importlib.resources({_EXAMPLES_PACKAGE}), {src_relative}"
    )
