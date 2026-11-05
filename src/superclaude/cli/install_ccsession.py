"""Wire the installed ccsession skill into the user's home."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def wire_ccsession(home: Path | None = None) -> tuple[bool, str]:
    home = Path.home() if home is None else Path(home)
    skill = home / ".claude" / "skills" / "ccsession-tag"
    wrapper = skill / "ccsession"
    # Orca's Claude command (Settings > Agents > Claude > Command).
    orca_wrapper = skill / "ccsession-orca"
    hook = skill / "hooks" / "session-start.sh"
    example = skill / "ccsession.env.example"
    if (
        not skill.is_dir()
        or skill.is_symlink()
        or not wrapper.is_file()
        or wrapper.is_symlink()
        or orca_wrapper.is_symlink()
        or hook.parent.is_symlink()
        or not hook.is_file()
        or hook.is_symlink()
        or not example.is_file()
        or example.is_symlink()
    ):
        return False, f"ccsession skill files missing or symlinked in {skill}"

    bin_dir = home / ".local" / "bin"
    dest = bin_dir / "ccsession"
    env = home / ".claude" / "ccsession.env"
    if (env.exists() or env.is_symlink()) and not env.is_file():
        return False, f"ccsession env path is not a file: {env}"
    unmanaged = []
    # A skill installed before ccsession-orca existed is kept by a plain
    # `superclaude install`; ccsession still works, and `update` adds the file.
    scripts = [wrapper, orca_wrapper] if orca_wrapper.is_file() else [wrapper]
    # Keeps ccsession's names in step with /rename (UserPromptSubmit, SessionEnd).
    # The hooks are registered even when a plain install keeps an older skill
    # folder, so give that folder the hook script: beside an older ccsession it
    # does nothing (it asks only a ccsession that knows --sync-name).
    name_hook = hook.parent / "session-name.sh"
    packaged = (
        Path(__file__).resolve().parent.parent
        / "skills"
        / "ccsession-tag"
        / "hooks"
        / "session-name.sh"
    )
    try:
        hook.chmod(0o755)
        if not name_hook.exists() and not name_hook.is_symlink() and packaged.is_file():
            shutil.copyfile(packaged, name_hook)
        if name_hook.is_file() and not name_hook.is_symlink():
            name_hook.chmod(0o755)
        bin_dir.mkdir(parents=True, exist_ok=True)
        for script in scripts:
            script.chmod(0o755)
            link = bin_dir / script.name
            if (link.exists() or link.is_symlink()) and not (
                link.is_symlink() and link.resolve() == script.resolve()
            ):
                unmanaged.append(link)
                continue
            if link.is_symlink():
                link.unlink()
            link.symlink_to(script)
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
        # Coder workspaces: record the gateway address so Orca terminals, which
        # start from a cleared environment, still reach the gateway.
        seeder = skill / "seed-env.py"
        if seeder.is_file() and not seeder.is_symlink():
            subprocess.run(
                [sys.executable, str(seeder), str(env), str(example)],
                check=False,
                capture_output=True,
                timeout=30,
            )
        # Session names now belong to the repo; copy names saved per folder by
        # older versions into their repo's list (once per list, copies only),
        # and, once, the names given with Claude Code's /rename before then.
        # A plain install can keep an older skill whose ccsession would read
        # the option as a launch, so ask only one that knows it.
        if b"--migrate-names)" in wrapper.read_bytes():
            try:
                subprocess.run(
                    [str(wrapper), "--migrate-names"],
                    check=False,
                    capture_output=True,
                    stdin=subprocess.DEVNULL,
                    timeout=60,
                    env={**os.environ, "HOME": str(home)},
                )
            except subprocess.TimeoutExpired:
                pass  # ccsession finishes the move itself on first use.
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"Could not wire ccsession: {exc}"

    if not env.is_file():
        return False, f"ccsession env path is not a file: {env}"
    warnings = []
    if unmanaged:
        paths = ", ".join(str(link) for link in unmanaged)
        verb, it = ("is", "it") if len(unmanaged) == 1 else ("are", "them")
        warnings.append(f"{paths} {verb} unmanaged; leaving {it} unchanged")
    if orca_wrapper not in scripts:
        warnings.append(
            f"{orca_wrapper.name} is not in {skill}; run 'superclaude update' to add it"
        )
    if warnings:
        return True, "ccsession installed; warning: " + "; ".join(warnings)
    return True, f"ccsession wired at {dest}"
