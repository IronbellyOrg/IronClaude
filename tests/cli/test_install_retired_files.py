"""Retire step for commands, skills and agents a release stopped shipping.

Covers the generated data (shape, generator), the removal rules on synthetic data,
and an upgrade from an installed 5.0.0 built from the ``v5.0.0`` tag. Every test uses
a throwaway HOME; nothing here touches the real ``~/.claude``. Tests that need the
tag skip with a reason when it is missing (shallow clone, no tags).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli import install_retired_data as data
from superclaude.cli import install_retired_files as retire
from superclaude.cli.main import main

REPO = Path(__file__).resolve().parents[2]
TAG = "v5.0.0"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _has_tag(tag: str = TAG) -> bool:
    probe = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            "--verify",
            "--quiet",
            f"{tag}^{{commit}}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return probe.returncode == 0


requires_tag = pytest.mark.skipif(
    not _has_tag(),
    reason=f"git tag {TAG} is not present (shallow clone or no tags fetched); "
    "run `git fetch --tags` to enable the tests that read it",
)


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "gen_retired_install_data", REPO / "scripts" / "gen_retired_install_data.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    """A throwaway HOME (and Claude config dir) so no test can touch the real one."""
    home_dir = tmp_path / "home"
    config = tmp_path / "config"
    home_dir.mkdir()
    config.mkdir()
    (config / ".claude.json").write_text(json.dumps({"mcpServers": {}}))
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    assert Path.home() == home_dir
    return home_dir


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


# ---- the generated data ---------------------------------------------------------


def _shipped_sources() -> dict[str, set[str]]:
    src = REPO / "src" / "superclaude"
    skills = {p.name for p in (src / "skills").iterdir() if p.is_dir()}
    root_skills = REPO / "skills"
    if root_skills.is_dir():
        skills |= {p.name for p in root_skills.iterdir() if p.is_dir()}
    return {
        "commands": {p.stem for p in (src / "commands").glob("*.md")},
        "agents": {p.stem for p in (src / "agents").glob("*.md")},
        "skills": skills,
    }


def test_data_names_are_absent_from_the_shipped_sources():
    shipped = _shipped_sources()
    assert not set(data.RETIRED_COMMANDS) & shipped["commands"]
    assert not set(data.RETIRED_AGENTS) & shipped["agents"]
    assert not set(data.RETIRED_SKILLS) & shipped["skills"]


def test_data_shape_hashes_and_names():
    assert data.SOURCE_TAGS and all(isinstance(t, str) and t for t in data.SOURCE_TAGS)
    name = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    part = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._-]*$")
    flat = {**data.RETIRED_COMMANDS, **data.RETIRED_AGENTS}
    for item, hashes in flat.items():
        assert name.match(item), item
        assert hashes and all(HEX64.match(h) for h in hashes), item
    for skill, files in data.RETIRED_SKILLS.items():
        assert name.match(skill), skill
        assert files, skill
        for rel, hashes in files.items():
            assert all(part.match(p) for p in rel.split("/")), (skill, rel)
            assert hashes and all(HEX64.match(h) for h in hashes), (skill, rel)


def test_data_never_lists_swarm_items():
    names = [*data.RETIRED_COMMANDS, *data.RETIRED_AGENTS, *data.RETIRED_SKILLS]
    assert not [n for n in names if "swarm" in n or n == "sc-bare-review"]


@requires_tag
def test_committed_data_equals_the_generator_output():
    generator = _load_generator()
    assert generator.render(generator.generate(REPO, list(data.SOURCE_TAGS))) == (
        REPO / generator.OUTPUT
    ).read_text(encoding="utf-8")


# Names that a release stopped shipping, by release. Each 6.1.0 removal pull request
# adds its names here; the data is generated from the v5.0.0 and v6.0.0 tags.
_REMOVED_IN_6_0_0_COMMANDS = (
    "build",
    "cli-portify",
    "improve",
    "index",
    "index-repo",
    "load",
    "review-translation",
    "roadmap",
    "save",
    "spawn",
    "tasklist",
    "validate-roadmap",
)
_REMOVED_IN_6_0_0_SKILLS = (
    "sc-cli-portify-protocol",
    "sc-review-translation-protocol",
    "sc-roadmap-protocol",
    "sc-tasklist-protocol",
    "sc-validate-roadmap-protocol",
)
_REMOVED_IN_6_1_0_COMMANDS = ("task", "tdd", "validate-tests")
_REMOVED_IN_6_1_0_SKILLS = (
    "operational-guide",
    "prd",
    "readme",
    "sc-task-protocol",
    "sc-validate-tests-protocol",
    "tdd",
    "tech-reference",
    "tech-research",
)
_REMOVED_IN_6_1_0_AGENTS: tuple = ()


@requires_tag
def test_retired_names_are_what_the_releases_removed():
    assert sorted(data.RETIRED_COMMANDS) == sorted(
        _REMOVED_IN_6_0_0_COMMANDS + _REMOVED_IN_6_1_0_COMMANDS
    )
    assert sorted(data.RETIRED_SKILLS) == sorted(
        _REMOVED_IN_6_0_0_SKILLS + _REMOVED_IN_6_1_0_SKILLS
    )
    assert sorted(data.RETIRED_AGENTS) == sorted(_REMOVED_IN_6_1_0_AGENTS)


# ---- the generator, on a throwaway git repository (no dependency on the tag) -----


def _git(repo: Path, *args: str) -> None:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
    }
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@pytest.fixture
def mini_repo(tmp_path):
    repo = tmp_path / "mini"
    src = repo / "src" / "superclaude"
    files = {
        "commands/keep.md": "keep\n",
        "commands/gone.md": "gone v1\n",
        "commands/README.md": "readme\n",
        "agents/stay.md": "stay\n",
        "agents/old.md": "old agent\n",
        "agents/README.md": "readme\n",
        "skills/keepskill/SKILL.md": "keep skill\n",
        "skills/oldskill/SKILL.md": "old skill\n",
        "skills/oldskill/refs/x.md": "ref x\n",
        "skills/_private/SKILL.md": "private\n",
    }
    for rel, text in files.items():
        path = src / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "release one")
    _git(repo, "tag", "v1")
    (src / "commands" / "gone.md").unlink()
    (src / "agents" / "old.md").unlink()
    shutil.rmtree(src / "skills" / "oldskill")
    return repo


def test_generator_lists_what_the_tag_shipped_and_the_tree_no_longer_does(mini_repo):
    generator = _load_generator()
    result = generator.generate(mini_repo, ["v1"])
    assert result["commands"] == {"gone": (sha(b"gone v1\n"),)}
    assert result["agents"] == {"old": (sha(b"old agent\n"),)}
    assert result["skills"] == {
        "oldskill": {
            "SKILL.md": (sha(b"old skill\n"),),
            "refs/x.md": (sha(b"ref x\n"),),
        }
    }


def test_generator_output_is_deterministic_and_loadable(mini_repo):
    generator = _load_generator()
    text = generator.render(generator.generate(mini_repo, ["v1"]))
    assert text == generator.render(generator.generate(mini_repo, ["v1"]))
    namespace: dict = {}
    exec(compile(text, "generated", "exec"), namespace)  # noqa: S102 - our own output
    assert namespace["SOURCE_TAGS"] == ("v1",)
    assert namespace["RETIRED_COMMANDS"] == {"gone": (sha(b"gone v1\n"),)}


def test_generator_check_mode_and_missing_tag(mini_repo, monkeypatch, capsys):
    generator = _load_generator()
    monkeypatch.setattr(generator, "REPO", mini_repo)
    target = mini_repo / generator.OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    assert generator.main(["--tag", "v1", "--check"]) == 1  # nothing written yet
    assert generator.main(["--tag", "v1"]) == 0
    assert generator.main(["--tag", "v1", "--check"]) == 0
    target.write_text(target.read_text().replace(sha(b"gone v1\n")[:8], "00000000"))
    assert generator.main(["--tag", "v1", "--check"]) == 1
    assert generator.main(["--tag", "no-such-tag"]) == 2
    assert "no-such-tag" in capsys.readouterr().err


# ---- the removal rules, on synthetic data ----------------------------------------

OLD_CMD = b"old command body\n"
OLD_AGENT = b"old agent body\n"
SKILL_FILES = {"SKILL.md": b"skill\n", "refs/a.md": b"ref a\n", "__init__.py": b""}


@pytest.fixture
def synthetic(monkeypatch):
    monkeypatch.setattr(data, "RETIRED_COMMANDS", {"gone-cmd": (sha(OLD_CMD),)})
    monkeypatch.setattr(data, "RETIRED_AGENTS", {"gone-agent": (sha(OLD_AGENT),)})
    monkeypatch.setattr(
        data,
        "RETIRED_SKILLS",
        {"gone-skill": {rel: (sha(b),) for rel, b in SKILL_FILES.items()}},
    )


def _claude(home: Path) -> Path:
    return home / ".claude"


def _lay_skill(folder: Path) -> None:
    for rel, body in SKILL_FILES.items():
        path = folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


def test_missing_claude_folder_is_safe_and_creates_nothing(home, synthetic, capsys):
    assert retire.run_retire_files_step() == {}
    assert "No retired commands, skills or agents present." in capsys.readouterr().out
    assert not _claude(home).exists()


def test_provable_items_are_removed_and_the_second_run_is_a_noop(
    home, synthetic, capsys
):
    claude = _claude(home)
    (claude / "commands" / "sc").mkdir(parents=True)
    (claude / "agents").mkdir()
    (claude / "commands" / "sc" / "gone-cmd.md").write_bytes(OLD_CMD)
    (claude / "agents" / "gone-agent.md").write_bytes(OLD_AGENT)
    _lay_skill(claude / "skills" / "gone-skill")
    outcomes = retire.run_retire_files_step()
    assert outcomes == {
        "command:gone-cmd": "removed",
        "agent:gone-agent": "removed",
        "skill:gone-skill": "removed",
    }
    assert not (claude / "commands" / "sc" / "gone-cmd.md").exists()
    assert not (claude / "agents" / "gone-agent.md").exists()
    assert not (claude / "skills" / "gone-skill").exists()
    capsys.readouterr()
    assert retire.run_retire_files_step() == {}
    assert "No retired" in capsys.readouterr().out


def test_an_edited_command_is_kept_with_the_reason_and_the_removal_command(
    home, synthetic, capsys
):
    path = _claude(home) / "commands" / "sc" / "gone-cmd.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(OLD_CMD + b"my edit\n")
    assert retire.run_retire_files_step() == {"command:gone-cmd": "kept"}
    out = capsys.readouterr().out
    assert path.read_bytes() == OLD_CMD + b"my edit\n"
    assert "Kept /sc:gone-cmd" in out and "differs" in out
    assert f"rm {path}" in out


@pytest.mark.parametrize("what", ["extra-file", "extra-folder", "edited", "symlink"])
def test_a_skill_folder_with_anything_unprovable_is_kept_whole(
    home, synthetic, capsys, what
):
    folder = _claude(home) / "skills" / "gone-skill"
    _lay_skill(folder)
    if what == "extra-file":
        (folder / "mine.md").write_text("mine")
    elif what == "extra-folder":
        (folder / "empty-dir").mkdir()
    elif what == "edited":
        (folder / "refs" / "a.md").write_bytes(b"changed\n")
    else:
        (folder / "refs" / "a.md").unlink()
        (folder / "refs" / "a.md").symlink_to(folder / "SKILL.md")
    before = sorted(str(p.relative_to(folder)) for p in folder.rglob("*"))
    assert retire.run_retire_files_step() == {"skill:gone-skill": "kept"}
    out = capsys.readouterr().out
    assert sorted(str(p.relative_to(folder)) for p in folder.rglob("*")) == before
    assert "Kept skill gone-skill" in out and f"rm -r {folder}" in out


def test_a_skill_that_is_a_link_is_kept(home, synthetic, capsys):
    skills = _claude(home) / "skills"
    skills.mkdir(parents=True)
    elsewhere = home / "elsewhere"
    _lay_skill(elsewhere)
    (skills / "gone-skill").symlink_to(elsewhere)
    assert retire.run_retire_files_step() == {"skill:gone-skill": "kept"}
    assert (elsewhere / "SKILL.md").exists()


def test_a_command_that_is_a_link_is_kept(home, synthetic):
    folder = _claude(home) / "commands" / "sc"
    folder.mkdir(parents=True)
    real = home / "real.md"
    real.write_bytes(OLD_CMD)
    (folder / "gone-cmd.md").symlink_to(real)
    assert retire.run_retire_files_step() == {"command:gone-cmd": "kept"}
    assert real.exists()


def test_only_listed_names_are_touched(home, synthetic):
    claude = _claude(home)
    (claude / "commands" / "sc").mkdir(parents=True)
    (claude / "skills" / "user-skill").mkdir(parents=True)
    other = claude / "commands" / "sc" / "other.md"
    other.write_bytes(OLD_CMD)  # same bytes, but the name is not on the list
    mine = claude / "skills" / "user-skill" / "SKILL.md"
    mine.write_text("mine")
    outside = claude / "settings.json"
    outside.write_text("{}")
    assert retire.run_retire_files_step() == {}
    assert other.exists() and mine.exists() and outside.exists()


def test_a_name_the_release_ships_is_never_removed(home, monkeypatch):
    shipped_command = "workflow"
    monkeypatch.setattr(data, "RETIRED_COMMANDS", {shipped_command: (sha(OLD_CMD),)})
    monkeypatch.setattr(data, "RETIRED_AGENTS", {})
    monkeypatch.setattr(data, "RETIRED_SKILLS", {})
    path = _claude(home) / "commands" / "sc" / f"{shipped_command}.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(OLD_CMD)
    assert retire.run_retire_files_step() == {}
    assert path.exists()


def test_unsafe_names_in_the_data_are_ignored(home, monkeypatch):
    monkeypatch.setattr(data, "RETIRED_COMMANDS", {"../evil": (sha(OLD_CMD),)})
    monkeypatch.setattr(data, "RETIRED_AGENTS", {})
    monkeypatch.setattr(data, "RETIRED_SKILLS", {"ok": {"../x": (sha(OLD_CMD),)}})
    victim = _claude(home) / "commands" / "evil.md"
    victim.parent.mkdir(parents=True)
    victim.write_bytes(OLD_CMD)
    assert retire.run_retire_files_step() == {}
    assert victim.exists()


def test_a_custom_commands_folder_is_the_one_cleaned(home, synthetic):
    custom = home / "custom-commands"
    custom.mkdir()
    (custom / "gone-cmd.md").write_bytes(OLD_CMD)
    default = _claude(home) / "commands" / "sc"
    default.mkdir(parents=True)
    (default / "gone-cmd.md").write_bytes(OLD_CMD)
    assert retire.run_retire_files_step(custom) == {"command:gone-cmd": "removed"}
    assert not (custom / "gone-cmd.md").exists()
    assert (default / "gone-cmd.md").exists()


def test_a_failed_delete_is_reported_and_never_raised(
    home, synthetic, monkeypatch, capsys
):
    path = _claude(home) / "commands" / "sc" / "gone-cmd.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(OLD_CMD)
    real_unlink = Path.unlink

    def deny(self, *args, **kwargs):
        if self.name == "gone-cmd.md":
            raise PermissionError("denied")
        return real_unlink(self, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", deny)
    assert retire.run_retire_files_step() == {"command:gone-cmd": "failed"}
    assert "Could not remove /sc:gone-cmd" in capsys.readouterr().out
    assert path.exists()


def test_a_file_edited_between_the_check_and_the_delete_is_kept(
    home, synthetic, monkeypatch, capsys
):
    path = _claude(home) / "commands" / "sc" / "gone-cmd.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(OLD_CMD)
    real = retire._classify_one
    calls = []

    def edit_after_first_look(kind, name, commands_dir):
        found = real(kind, name, commands_dir)
        calls.append(name)
        if kind == "command" and calls.count(name) == 1:
            path.write_bytes(OLD_CMD + b"late edit\n")
        return found

    monkeypatch.setattr(retire, "_classify_one", edit_after_first_look)
    assert retire.run_retire_files_step() == {"command:gone-cmd": "kept"}
    assert path.read_bytes() == OLD_CMD + b"late edit\n"
    out = capsys.readouterr().out
    assert out.count("Kept /sc:gone-cmd") == 1 and f"rm {path}" in out


def test_a_skill_file_edited_after_the_first_delete_is_never_removed(
    home, synthetic, monkeypatch, capsys
):
    """Each file is proven again right before it goes, not once for the folder."""
    folder = _claude(home) / "skills" / "gone-skill"
    _lay_skill(folder)
    real_unlink = Path.unlink
    removed = []

    def edit_the_rest_after_the_first_delete(self, *args, **kwargs):
        real_unlink(self, *args, **kwargs)
        removed.append(self)
        if len(removed) == 1:
            for left in folder.rglob("*"):
                if left.is_file():
                    left.write_bytes(left.read_bytes() + b"my late edit\n")

    monkeypatch.setattr(Path, "unlink", edit_the_rest_after_the_first_delete)
    assert retire.run_retire_files_step() == {"skill:gone-skill": "kept"}
    out = capsys.readouterr().out
    assert len(removed) == 1
    survivors = [p for p in folder.rglob("*") if p.is_file()]
    assert len(survivors) == len(SKILL_FILES) - 1
    assert all(p.read_bytes().endswith(b"my late edit\n") for p in survivors)
    assert "changed while this step ran" in out and f"rm -r {folder}" in out
    assert out.count("Kept") == 1  # one line per item, not a second generic one


# ---- the upgrade from an installed 5.0.0 ------------------------------------------


@pytest.fixture(scope="module")
def release_5_0_0(tmp_path_factory):
    """The commands, skills and agents folders of the v5.0.0 tag, as shipped."""
    if not _has_tag():
        pytest.skip(f"git tag {TAG} is not present")
    dest = tmp_path_factory.mktemp("v5.0.0")
    archive = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "archive",
            "--format=tar",
            TAG,
            "src/superclaude/commands",
            "src/superclaude/skills",
            "src/superclaude/agents",
        ],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    return dest / "src" / "superclaude"


def _install_5_0_0(home: Path, release: Path) -> None:
    """Lay down what `superclaude install` of 5.0.0 copies (plain copies, README skipped)."""
    claude = _claude(home)
    commands = claude / "commands" / "sc"
    commands.mkdir(parents=True)
    for path in (release / "commands").glob("*.md"):
        if path.name != "README.md":
            shutil.copy2(path, commands / path.name)
    agents = claude / "agents"
    agents.mkdir()
    for path in (release / "agents").glob("*.md"):
        if path.name not in {"README.md", "__init__.py"}:
            shutil.copy2(path, agents / path.name)
    skills = claude / "skills"
    skills.mkdir()
    for folder in (release / "skills").iterdir():
        if folder.is_dir() and not folder.name.startswith("_"):
            shutil.copytree(folder, skills / folder.name)


def _snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): (
            sha(p.read_bytes()) if p.is_file() and not p.is_symlink() else "-"
        )
        for p in sorted(root.rglob("*"))
    }


_STUBBED = (
    "superclaude.cli.install_ccsession.wire_ccsession",
    "superclaude.cli.install_hooks.install_hooks",
    "superclaude.cli.install_user_setup.install_user_setup",
)


def _stub_risky_installers(monkeypatch, failing: str | None = None):
    """Stub what talks to Claude Code or edits settings; commands, agents, skills,
    core files and templates stay real so the upgrade is the real one."""
    for path in _STUBBED:
        name = path.rsplit(".", 1)[-1]
        monkeypatch.setattr(path, lambda *a, _n=name, **k: (_n != failing, f"{_n} ok"))
    monkeypatch.setattr(
        "superclaude.cli.install_mcp.install_codegraph_mcp",
        lambda **k: (True, "codegraph ok"),
    )


RETIRED_COMMANDS_5_0_0 = [
    "build",
    "cli-portify",
    "improve",
    "index-repo",
    "index",
    "load",
    "review-translation",
    "roadmap",
    "save",
    "spawn",
    "tasklist",
    "validate-roadmap",
]
RETIRED_SKILLS_5_0_0 = [
    "sc-cli-portify-protocol",
    "sc-review-translation-protocol",
    "sc-roadmap-protocol",
    "sc-tasklist-protocol",
    "sc-validate-roadmap-protocol",
]


@requires_tag
@pytest.mark.parametrize("command", ["install", "update"])
def test_upgrade_from_an_installed_5_0_0(home, release_5_0_0, monkeypatch, command):
    _install_5_0_0(home, release_5_0_0)
    claude = _claude(home)
    commands = claude / "commands" / "sc"
    skills = claude / "skills"
    # a customized copy, a skill folder with an extra file, and unrelated user files
    custom = commands / "roadmap.md"
    custom.write_text(custom.read_text() + "\nmy own tweak\n")
    extra = skills / "sc-tasklist-protocol" / "my-notes.md"
    extra.write_text("my notes")
    user_command = commands / "my-own-command.md"
    user_command.write_text("mine")
    user_skill = skills / "my-own-skill" / "SKILL.md"
    user_skill.parent.mkdir()
    user_skill.write_text("mine")
    src = REPO / "src" / "superclaude"
    # items 6.0.0 still ships: present afterwards, equal to the shipped copy
    kept_6_0_0 = {
        commands / "implement.md": src / "commands" / "implement.md",
        skills / "sc-implement-protocol" / "SKILL.md": src
        / "skills"
        / "sc-implement-protocol"
        / "SKILL.md",
        claude / "agents" / "rf-qa.md": src / "agents" / "rf-qa.md",
    }
    _stub_risky_installers(monkeypatch)

    result = CliRunner().invoke(
        main, [command, *(["--force"] if command == "install" else [])]
    )

    assert result.exit_code == 0, result.output
    expected_gone = [n for n in RETIRED_COMMANDS_5_0_0 if n != "roadmap"]
    assert not [n for n in expected_gone if (commands / f"{n}.md").exists()]
    assert not [
        n
        for n in RETIRED_SKILLS_5_0_0
        if n != "sc-tasklist-protocol" and (skills / n).exists()
    ]
    # kept and explained
    assert custom.exists() and "my own tweak" in custom.read_text()
    assert extra.exists() and (skills / "sc-tasklist-protocol" / "SKILL.md").exists()
    assert "Kept /sc:roadmap" in result.output and f"rm {custom}" in result.output
    assert "Kept skill sc-tasklist-protocol" in result.output
    assert "my-notes.md" in result.output
    assert f"rm -r {skills / 'sc-tasklist-protocol'}" in result.output
    # untouched
    assert user_command.read_text() == "mine" and user_skill.read_text() == "mine"
    for path, shipped in kept_6_0_0.items():
        assert path.read_bytes() == shipped.read_bytes(), path
    assert (commands / "sweep.md").exists()  # a 6.0.0 command is installed

    # a second run changes nothing and is not alarming
    before = _snapshot(claude)
    again = CliRunner().invoke(
        main, [command, *(["--force"] if command == "install" else [])]
    )
    assert again.exit_code == 0, again.output
    assert _snapshot(claude) == before
    assert "Removed" not in again.output.split("Retiring commands")[-1]
    assert "⚠️" not in again.output.split("Retiring commands")[-1]


@requires_tag
def test_upgrade_removes_all_twelve_commands_and_five_skills_when_nothing_is_customized(
    home, release_5_0_0, monkeypatch
):
    _install_5_0_0(home, release_5_0_0)
    claude = _claude(home)
    _stub_risky_installers(monkeypatch)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 0, result.output
    assert [
        n
        for n in RETIRED_COMMANDS_5_0_0
        if (claude / "commands" / "sc" / f"{n}.md").exists()
    ] == []
    assert [n for n in RETIRED_SKILLS_5_0_0 if (claude / "skills" / n).exists()] == []
    assert "Kept" not in result.output.split("Retiring commands")[-1]


@requires_tag
def test_a_custom_target_is_cleaned_instead_of_the_default_folder(
    home, release_5_0_0, monkeypatch
):
    _install_5_0_0(home, release_5_0_0)
    target = home / "elsewhere" / "sc"
    target.mkdir(parents=True)
    shutil.copy2(release_5_0_0 / "commands" / "spawn.md", target / "spawn.md")
    _stub_risky_installers(monkeypatch)
    result = CliRunner().invoke(main, ["install", "--target", str(target)])
    assert result.exit_code == 0, result.output
    assert not (target / "spawn.md").exists()


@pytest.mark.parametrize("failing", [None, "install_hooks"])
@pytest.mark.parametrize("command", ["install", "update"])
def test_the_step_never_changes_the_exit_code(home, monkeypatch, command, failing):
    _stub_risky_installers(monkeypatch, failing=failing)
    expected = 1 if failing else 0
    assert CliRunner().invoke(main, [command]).exit_code == expected

    def boom(*args, **kwargs):
        raise RuntimeError("retire exploded")

    monkeypatch.setattr(retire, "run_retire_files_step", boom)
    result = CliRunner().invoke(main, [command])
    assert result.exit_code == expected, result.output
    assert "Retire step skipped (RuntimeError)" in result.output
