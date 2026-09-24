"""Wire the installed ccsession skill into the user's home."""

import os
import shutil
from pathlib import Path


def wire_ccsession(home: Path | None = None) -> tuple[bool, str]:
    home = Path.home() if home is None else Path(home)
    skill = home / ".claude" / "skills" / "ccsession-tag"
    wrapper = skill / "ccsession"
    hook = skill / "hooks" / "session-start.sh"
    example = skill / "ccsession.env.example"
    if (
        not skill.is_dir()
        or not wrapper.is_file()
        or not hook.is_file()
        or not example.is_file()
    ):
        return False, f"ccsession skill files missing in {skill}"

    dest = home / ".local" / "bin" / "ccsession"
    env = home / ".claude" / "ccsession.env"
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
            with env.open("xb") as target, example.open("rb") as source:
                os.chmod(target.fileno(), 0o600)
                shutil.copyfileobj(source, target)
    except OSError as exc:
        return False, f"Could not wire ccsession: {exc}"

    if collision:
        return (
            True,
            f"ccsession installed; warning: {dest} is unmanaged; leaving it unchanged",
        )
    return True, f"ccsession wired at {dest}"
