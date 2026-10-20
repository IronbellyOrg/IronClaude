"""Shared same-directory atomic byte write for normalize and reduce (IMM-6).

Callers prepare the parent directory and encode their payload first; this
leaf only runs the tmp file + fsync + ``os.replace`` transaction.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def write_prepared_bytes(path: Path, data: bytes) -> int:
    """Write ``data`` to ``path`` via tmp file + ``os.replace``; return its length.

    The parent directory must already exist. The tmp file lives in the same
    directory as ``path`` so ``os.replace`` stays atomic across filesystem
    boundaries. On a caught ``Exception`` the tmp file is unlinked (a failed
    unlink is ignored) and the original exception is re-raised.
    """
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, str(path))
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return len(data)
