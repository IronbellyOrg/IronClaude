"""Wire the installed ccsession skill into the user's home."""

import os
import shutil
import tempfile
from pathlib import Path


def wire_ccsession(home: Path | None = None) -> tuple[bool, str]:
    home = Path.home() if home is None else Path(home)
    skill = home / ".claude" / "skills" / "ccsession-tag"
    wrapper = skill / "ccsession"
    hook = skill / "hooks" / "session-start.sh"
    example = skill / "ccsession.env.example"
    if (
        not skill.is_dir()
        or skill.is_symlink()
        or not wrapper.is_file()
        or wrapper.is_symlink()
        or hook.parent.is_symlink()
        or not hook.is_file()
        or hook.is_symlink()
        or not example.is_file()
        or example.is_symlink()
    ):
        return False, f"ccsession skill files missing or symlinked in {skill}"

    dest = home / ".local" / "bin" / "ccsession"
    env = home / ".claude" / "ccsession.env"
    if (env.exists() or env.is_symlink()) and not env.is_file():
        return False, f"ccsession env path is not a file: {env}"
    try:
        wrapper.chmod(0o755)
        hook.chmod(0o755)
        dest.parent.mkdir(parents=True, exist_ok=True)
        collision = (dest.exists() or dest.is_symlink()) and not (
            dest.is_symlink() and dest.resolve() == wrapper.resolve()
        )
        if not collision:
            if dest.is_symlink():
                dest.unlink()
            dest.symlink_to(wrapper)
        if not env.exists() and not env.is_symlink():
            staged_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    dir=env.parent, prefix=".ccsession-env-", delete=False
                ) as staged:
                    staged_path = Path(staged.name)
                    os.fchmod(staged.fileno(), 0o600)
                    with example.open("rb") as source:
                        shutil.copyfileobj(source, staged)
                try:
                    os.link(staged_path, env)
                except FileExistsError:
                    pass  # Another installer seeded it first; keep their file.
            finally:
                if staged_path is not None:
                    staged_path.unlink(missing_ok=True)
    except OSError as exc:
        return False, f"Could not wire ccsession: {exc}"

    if not env.is_file():
        return False, f"ccsession env path is not a file: {env}"
    if collision:
        return (
            True,
            f"ccsession installed; warning: {dest} is unmanaged; leaving it unchanged",
        )
    return True, f"ccsession wired at {dest}"
