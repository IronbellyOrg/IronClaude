#!/usr/bin/env python3
"""Generate ``src/superclaude/cli/install_retired_data.py`` from release tags.

The installer copies what a release ships but never deletes what a release stops
shipping. ``superclaude install`` and ``superclaude update`` therefore run a retire
step (``src/superclaude/cli/install_retired_files.py``) that removes, from
``~/.claude/commands/sc/``, ``~/.claude/skills/`` and ``~/.claude/agents/``, the
files this data proves IronClaude wrote: same name as something an earlier release
shipped and not shipped now, and a sha256 equal to the file at that release's tag.

Run it at release preparation with the previous release's tag::

    uv run python scripts/gen_retired_install_data.py --tag v5.0.0
    uv run python scripts/gen_retired_install_data.py --tag v5.0.0 --check

``--tag`` may be repeated. A run with one tag only knows the names shipped at that
tag, so a workspace that skipped a release keeps the older retired names only if
every older tag is passed too (ceiling: pass every tag still worth retiring from).
Names come from ``git ls-tree`` against each tag compared with the working tree;
hashes come from ``git cat-file`` of each file at that tag. ``--check`` exits 1 when
the committed data module differs from what would be generated.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTPUT = "src/superclaude/cli/install_retired_data.py"

COMMANDS_DIR = "src/superclaude/commands"
SKILLS_DIR = "src/superclaude/skills"
AGENTS_DIR = "src/superclaude/agents"
# ``install_skill.list_available_skills`` also scans this folder in a source checkout.
ROOT_SKILLS_DIR = "skills"

# The installers skip these files (install_commands.py, install_agents.py).
COMMAND_EXCLUDE = {"README.md"}
AGENT_EXCLUDE = {"README.md", "__init__.py"}


def _git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def _tag_files(repo: Path, tag: str, folder: str) -> list[str]:
    """Paths under ``folder`` at ``tag``, relative to ``folder``."""
    out = _git(repo, "ls-tree", "-r", "--name-only", "-z", tag, "--", folder + "/")
    prefix = folder + "/"
    return sorted(
        path[len(prefix) :]
        for path in out.decode("utf-8").split("\0")
        if path.startswith(prefix)
    )


def _sha256_at(repo: Path, tag: str, path: str) -> str:
    return hashlib.sha256(_git(repo, "cat-file", "blob", f"{tag}:{path}")).hexdigest()


def _shipped_files(repo: Path, folder: str, exclude: set[str]) -> set[str]:
    base = repo / folder
    if not base.is_dir():
        return set()
    return {p.stem for p in base.glob("*.md") if p.is_file() and p.name not in exclude}


def _shipped_skills(repo: Path) -> set[str]:
    names: set[str] = set()
    for folder in (SKILLS_DIR, ROOT_SKILLS_DIR):
        base = repo / folder
        if base.is_dir():
            for item in base.iterdir():
                if item.is_dir():
                    names.add(item.name)
                    names.add(item.name.replace("_", "-"))
    return names


def _flat_markdown(repo: Path, tag: str, folder: str, exclude: set[str]) -> dict:
    """name -> sha256 of ``<name>.md`` at the tag, for top-level markdown files."""
    found = {}
    for rel in _tag_files(repo, tag, folder):
        if "/" in rel or not rel.endswith(".md") or rel in exclude:
            continue
        found[rel[: -len(".md")]] = _sha256_at(repo, tag, f"{folder}/{rel}")
    return found


def _skill_files(repo: Path, tag: str) -> dict:
    """skill name -> {relative path: sha256} at the tag."""
    found: dict[str, dict[str, str]] = {}
    for rel in _tag_files(repo, tag, SKILLS_DIR):
        name, _, inner = rel.partition("/")
        if not inner or name.startswith("_"):
            continue
        found.setdefault(name, {})[inner] = _sha256_at(repo, tag, f"{SKILLS_DIR}/{rel}")
    return found


def generate(repo: Path, tags: list[str]) -> dict:
    """The data for ``repo``: what each tag shipped and the working tree no longer does."""
    commands_now = _shipped_files(repo, COMMANDS_DIR, COMMAND_EXCLUDE)
    agents_now = _shipped_files(repo, AGENTS_DIR, AGENT_EXCLUDE)
    skills_now = _shipped_skills(repo)

    commands: dict[str, set[str]] = {}
    agents: dict[str, set[str]] = {}
    skills: dict[str, dict[str, set[str]]] = {}
    for tag in tags:
        for name, digest in _flat_markdown(
            repo, tag, COMMANDS_DIR, COMMAND_EXCLUDE
        ).items():
            if name not in commands_now:
                commands.setdefault(name, set()).add(digest)
        for name, digest in _flat_markdown(
            repo, tag, AGENTS_DIR, AGENT_EXCLUDE
        ).items():
            if name not in agents_now:
                agents.setdefault(name, set()).add(digest)
        for name, files in _skill_files(repo, tag).items():
            if name in skills_now or name.replace("_", "-") in skills_now:
                continue
            for rel, digest in files.items():
                skills.setdefault(name, {}).setdefault(rel, set()).add(digest)

    def freeze(hashes: set[str]) -> tuple[str, ...]:
        return tuple(sorted(hashes))

    return {
        "tags": tuple(tags),
        "commands": {n: freeze(h) for n, h in sorted(commands.items())},
        "agents": {n: freeze(h) for n, h in sorted(agents.items())},
        "skills": {
            n: {r: freeze(h) for r, h in sorted(files.items())}
            for n, files in sorted(skills.items())
        },
    }


def _hash_tuple(hashes: tuple[str, ...]) -> str:
    return "(" + ", ".join(f'"{h}"' for h in hashes) + ",)"


def render(data: dict) -> str:
    """Deterministic source text of the data module."""
    lines = [
        '"""GENERATED FILE. Do not edit by hand.',
        "",
        "Written by ``scripts/gen_retired_install_data.py --tag "
        + " --tag ".join(data["tags"])
        + "``.",
        "Commands, skills and agents that an earlier release shipped and the current",
        "tree does not, with the sha256 of each file as shipped at that release's tag.",
        "``install_retired_files`` removes an installed copy only when its content has",
        "one of these hashes. Regenerate at release preparation with the previous tag.",
        '"""',
        "",
        "# fmt: off",
        "SOURCE_TAGS = (" + "".join(f'"{t}", ' for t in data["tags"]).rstrip() + ")",
        "",
        "# command name (without .md) -> sha256 of the file at the tag(s)",
        "RETIRED_COMMANDS = {",
    ]
    for name, hashes in data["commands"].items():
        lines.append(f'    "{name}": {_hash_tuple(hashes)},')
    lines += ["}", "", "# agent name (without .md) -> sha256 of the file at the tag(s)"]
    lines.append("RETIRED_AGENTS = {" if data["agents"] else "RETIRED_AGENTS = {}")
    for name, hashes in data["agents"].items():
        lines.append(f'    "{name}": {_hash_tuple(hashes)},')
    if data["agents"]:
        lines.append("}")
    lines += ["", "# skill folder -> {path inside the folder: sha256 at the tag(s)}"]
    lines.append("RETIRED_SKILLS = {")
    for name, files in data["skills"].items():
        lines.append(f'    "{name}": {{')
        for rel, hashes in files.items():
            lines.append(f'        "{rel}": {_hash_tuple(hashes)},')
        lines.append("    },")
    lines += ["}", "# fmt: on", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--tag",
        action="append",
        required=True,
        help="release tag to read (repeatable), usually the previous release",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when the committed data differs; write nothing",
    )
    args = parser.parse_args(argv)

    for tag in args.tag:
        probe = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--verify", "--quiet", tag],
            stdout=subprocess.DEVNULL,
        )
        if probe.returncode != 0:
            print(
                f"tag {tag} not found; fetch it with `git fetch --tags`",
                file=sys.stderr,
            )
            return 2

    text = render(generate(REPO, args.tag))
    target = REPO / OUTPUT
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != text:
            print(
                f"{OUTPUT} is out of date; run this script without --check",
                file=sys.stderr,
            )
            return 1
        print(f"{OUTPUT} is up to date")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
