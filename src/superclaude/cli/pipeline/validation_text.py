"""Text helpers shared by the tasklist and roadmap validation executors.

Stdlib-only leaf: callers keep their own runners, process seams and loggers.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path


def embed_inputs(input_paths: list[Path]) -> str:
    """Read input files and return their contents as fenced code blocks."""
    if not input_paths:
        return ""
    blocks: list[str] = []
    for p in input_paths:
        content = Path(p).read_text(encoding="utf-8")
        blocks.append(f"# {p}\n```\n{content}\n```")
    return "\n\n".join(blocks)


def sanitize_output(output_file: Path, *, logger: logging.Logger) -> int:
    """Strip conversational preamble before YAML frontmatter."""
    try:
        content = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 0

    if content.lstrip().startswith("---"):
        return 0

    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start() :]
    preamble_bytes = len(preamble.encode("utf-8"))

    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    logger.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes
