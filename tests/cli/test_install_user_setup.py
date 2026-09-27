"""Tests for the shared user setup installed by ``superclaude install``."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from superclaude.cli import install_user_setup as setup

PKG = Path(setup.__file__).resolve().parent.parent


def _settings(home: Path) -> dict:
    return json.loads((home / ".claude" / "settings.json").read_text())


def test_rules_install_and_are_excluded_by_exact_path(tmp_path: Path) -> None:
    ok, message = setup.install_rules(home=tmp_path)
    assert ok, message
    rules = tmp_path / ".claude" / "rules"
    for group in ("core", "contextual", "prompts"):
        assert any((rules / group).glob("*.md"))
    assert _settings(tmp_path)["claudeMdExcludes"] == [
        f"{rules}/core/**",
        f"{rules}/contextual/**",
        f"{rules}/prompts/**",
    ]
    # A second run adds nothing and keeps the user's own excludes.
    settings = _settings(tmp_path)
    settings["claudeMdExcludes"].insert(0, "/mine/**")
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps(settings))
    assert setup.install_rules(home=tmp_path)[0]
    assert _settings(tmp_path)["claudeMdExcludes"][0] == "/mine/**"
    assert len(_settings(tmp_path)["claudeMdExcludes"]) == 4


def test_rules_keep_user_edits_unless_forced(tmp_path: Path) -> None:
    setup.install_rules(home=tmp_path)
    rule = tmp_path / ".claude" / "rules" / "core" / "quality_gates.md"
    rule.write_text("edited")
    setup.install_rules(home=tmp_path)
    assert rule.read_text() == "edited"
    setup.install_rules(home=tmp_path, force=True)
    assert rule.read_text() != "edited"


def test_every_rules_reference_in_templates_and_rules_ships() -> None:
    """Templates read rules on demand from ~/.claude/rules; each must exist."""
    pattern = re.compile(r"~/\.claude/rules/([A-Za-z_]+/[A-Za-z_]+\.md)")
    missing = set()
    for root in (PKG / "templates", PKG / "rules"):
        for path in root.rglob("*.md"):
            for rel in pattern.findall(path.read_text()):
                if not (PKG / "rules" / rel).is_file():
                    missing.add(rel)
    assert not missing
    # No project-relative rules path may remain: it resolves nowhere outside IronFlow.
    stale = re.compile(r"(?<![~/\w])\.claude/rules/")
    for root in (PKG / "templates", PKG / "rules"):
        for path in root.rglob("*.md"):
            assert not stale.search(path.read_text()), path


def test_output_style_installs(tmp_path: Path) -> None:
    ok, message = setup.install_output_styles(home=tmp_path)
    assert ok, message
    style = tmp_path / ".claude" / "output-styles" / "pragmatic.md"
    assert style.read_text().startswith("---\nname: Pragmatic")


def test_settings_defaults_fill_only_missing_values(tmp_path: Path) -> None:
    claude = tmp_path / ".claude"
    claude.mkdir()
    (claude / "settings.json").write_text(
        json.dumps(
            {
                "model": "sonnet",
                "env": {"CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION": "10"},
                "enabledPlugins": {"playwright@claude-plugins-official": False},
                "hooks": {"Stop": []},
            }
        )
    )
    ok, message = setup.apply_settings_defaults(home=tmp_path)
    assert ok, message
    settings = _settings(tmp_path)
    assert settings["model"] == "sonnet"
    assert settings["env"]["CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION"] == "10"
    assert settings["env"]["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"] == "1"
    assert settings["enabledPlugins"]["playwright@claude-plugins-official"] is False
    assert settings["enabledPlugins"]["notion@claude-plugins-official"] is True
    assert settings["outputStyle"] == "Pragmatic"
    assert settings["hooks"] == {"Stop": []}
    assert list(claude.glob("settings.json.bak.*"))
    again = setup.apply_settings_defaults(home=tmp_path)
    assert again == (True, "✅ Settings defaults: already present")


def test_settings_defaults_refuse_malformed_file(tmp_path: Path) -> None:
    claude = tmp_path / ".claude"
    claude.mkdir()
    (claude / "settings.json").write_text("{not json")
    ok, message = setup.apply_settings_defaults(home=tmp_path)
    assert not ok
    assert (claude / "settings.json").read_text() == "{not json"
    assert "left untouched" in message


def test_orca_skills_skip_when_orca_is_absent(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(setup.shutil, "which", lambda _name: None)
    assert setup.install_orca_skills(home=tmp_path) == (
        True,
        "⏭️  Orca skills: Orca CLI not found; skipped",
    )


def test_orca_skills_ignore_a_non_orca_program(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "orca"
    fake.write_text("#!/bin/sh\necho screen reader\n")
    fake.chmod(0o755)
    monkeypatch.setattr(setup.shutil, "which", lambda name: str(fake))
    ok, message = setup.install_orca_skills(home=tmp_path)
    assert ok and "not found" in message


def test_orca_skills_request_the_three_skills(tmp_path: Path, monkeypatch) -> None:
    calls = []
    skills = tmp_path / ".claude" / "skills"

    def fake_run(command, **_kwargs):
        calls.append(command)
        if command[1:3] == ["skills", "list"]:
            return subprocess.CompletedProcess(
                command, 0, json.dumps({"topics": [{"name": "orca-cli"}]}), ""
            )
        for name in setup._ORCA_SKILLS:
            (skills / name).mkdir(parents=True, exist_ok=True)
            (skills / name / "SKILL.md").write_text("x")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/bin/{name}")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    ok, message = setup.install_orca_skills(home=tmp_path)
    assert ok and message.startswith("✅ Orca skills")
    install = calls[-1]
    assert install[1:3] == ["skills", "install"]
    for name in setup._ORCA_SKILLS:
        assert name in install
    assert install.count("--skill") == 3
    # Already present: no further Orca calls.
    calls.clear()
    assert (
        setup.install_orca_skills(home=tmp_path)[1]
        == "✅ Orca skills: already installed"
    )
    assert not calls


def test_orca_failure_never_fails_install(tmp_path: Path, monkeypatch) -> None:
    def fake_run(command, **_kwargs):
        if command[1:3] == ["skills", "list"]:
            return subprocess.CompletedProcess(
                command, 0, json.dumps({"topics": [{"name": "orca-cli"}]}), ""
            )
        raise subprocess.TimeoutExpired(command, setup._ORCA_TIMEOUT)

    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/bin/{name}")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    ok, message = setup.install_orca_skills(home=tmp_path)
    assert ok and message.startswith("⚠️  Orca skills")


def _plugin_home(tmp_path: Path, enabled: dict) -> Path:
    claude = tmp_path / ".claude"
    claude.mkdir(parents=True, exist_ok=True)
    (claude / "settings.json").write_text(json.dumps({"enabledPlugins": enabled}))
    return tmp_path


def test_plugins_install_missing_enabled_defaults(tmp_path: Path, monkeypatch) -> None:
    defaults = json.loads(
        (Path(setup.__file__).parent / "user_settings_defaults.json").read_text()
    )
    wanted = {p: True for p in defaults["enabledPlugins"]}
    wanted["notion@claude-plugins-official"] = False  # user turned it off
    home = _plugin_home(tmp_path, wanted)
    calls = []

    def fake_run(command, **_kwargs):
        calls.append(command[1:])
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    ok, message = setup.install_plugins(home=home)
    assert ok and message.startswith("✅ Plugins")
    assert [
        "plugin",
        "marketplace",
        "add",
        "anthropics/claude-plugins-official",
    ] in calls
    assert ["plugin", "marketplace", "add", "Lum1104/Understand-Anything"] in calls
    installs = [c[2] for c in calls if c[:2] == ["plugin", "install"]]
    assert "notion@claude-plugins-official" not in installs
    assert "frontend-design@claude-plugins-official" in installs
    assert "understand-anything@understand-anything" in installs


def test_plugins_skip_already_installed(tmp_path: Path, monkeypatch) -> None:
    home = _plugin_home(tmp_path, {"playwright@claude-plugins-official": True})
    plugins = home / ".claude" / "plugins"
    plugins.mkdir()
    (plugins / "known_marketplaces.json").write_text(
        json.dumps({"claude-plugins-official": {}})
    )
    (plugins / "installed_plugins.json").write_text(
        json.dumps({"plugins": {"playwright@claude-plugins-official": []}})
    )
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError)
    )
    assert setup.install_plugins(home=home) == (True, "✅ Plugins: already installed")


def test_plugin_failures_and_time_limit_never_fail_install(
    tmp_path: Path, monkeypatch
) -> None:
    home = _plugin_home(tmp_path, {"playwright@claude-plugins-official": True})
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess,
        "run",
        lambda command, **k: subprocess.CompletedProcess(command, 1, "", "boom"),
    )
    ok, message = setup.install_plugins(home=home)
    assert ok and message.startswith("⚠️  Plugins")
    ok, message = setup.install_plugins(home=home, deadline=0)
    assert ok and "time limit" in message


def test_shipped_setup_contains_no_personal_home_paths() -> None:
    personal = re.compile(r"/Users/[A-Za-z]|/home/(?!coder/)[a-z]")
    for root in ("rules", "templates", "output-styles"):
        for path in (PKG / root).rglob("*"):
            if path.is_file() and path.suffix in (".md", ".contract", ".json"):
                assert not personal.search(path.read_text()), path
