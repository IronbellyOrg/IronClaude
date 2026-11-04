"""Tests for the shared user setup installed by ``superclaude install``."""

from __future__ import annotations

import json
import os
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


def _defaults() -> dict:
    return json.loads(
        (Path(setup.__file__).parent / "user_settings_defaults.json").read_text()
    )


PONYTAIL_SHA = "7801d061243d7b753bad0e0b3c057cd250b11755"  # upstream tag v5.3.3


def test_defaults_ship_ponytail_pinned() -> None:
    defaults = _defaults()
    catalog = defaults[setup._CATALOG_KEY]
    assert catalog["name"] == "ironclaude"
    assert catalog["owner"]["name"]
    assert defaults["enabledPlugins"]["ponytail@ironclaude"] is True
    entry = next(e for e in catalog["plugins"] if e["name"] == "ponytail")
    assert entry["source"] == {
        "source": "github",
        "repo": "DietrichGebert/ponytail",
        "ref": "v5.3.3",
        "sha": PONYTAIL_SHA,
    }
    # Every catalog entry is pinned to a full commit, never a branch or tag alone.
    for item in catalog["plugins"]:
        assert re.fullmatch(r"[0-9a-f]{40}", item["source"]["sha"]), item["name"]
    assert defaults["env"]["PONYTAIL_DEFAULT_MODE"] == "lite"
    assert "pluginConfigs" not in defaults
    # Every default plugin's marketplace must be installable by install_plugins.
    for plugin in defaults["enabledPlugins"]:
        market = plugin.split("@", 1)[1]
        if market == catalog["name"]:
            assert market not in defaults["extraKnownMarketplaces"]
            continue
        assert defaults["extraKnownMarketplaces"][market]["source"]["repo"], plugin


def test_defaults_hold_no_unpinned_ponytail() -> None:
    defaults = _defaults()
    assert "ponytail@ponytail" not in defaults["enabledPlugins"]
    assert "ponytail" not in defaults["extraKnownMarketplaces"]
    outside_catalog = {k: v for k, v in defaults.items() if k != setup._CATALOG_KEY}
    assert "DietrichGebert" not in json.dumps(outside_catalog)


def test_settings_defaults_add_ponytail_for_existing_users(tmp_path: Path) -> None:
    claude = tmp_path / ".claude"
    claude.mkdir()
    defaults = _defaults()
    old_plugins = {
        p: True for p in defaults["enabledPlugins"] if p != "ponytail@ironclaude"
    }
    old_markets = dict(defaults["extraKnownMarketplaces"])
    (claude / "settings.json").write_text(
        json.dumps(
            {
                "env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"},
                "enabledPlugins": old_plugins,
                "extraKnownMarketplaces": old_markets,
            }
        )
    )
    assert setup.apply_settings_defaults(home=tmp_path)[0]
    settings = _settings(tmp_path)
    assert settings["enabledPlugins"]["ponytail@ironclaude"] is True
    # The catalog stays in the package; Claude Code declares the marketplace
    # itself when install_plugins adds it.
    assert setup._CATALOG_KEY not in settings
    assert "ironclaude" not in settings["extraKnownMarketplaces"]
    assert settings["env"]["PONYTAIL_DEFAULT_MODE"] == "lite"
    for plugin, value in old_plugins.items():
        assert settings["enabledPlugins"][plugin] is value
    for market, value in old_markets.items():
        assert settings["extraKnownMarketplaces"][market] == value
    assert setup.apply_settings_defaults(home=tmp_path) == (
        True,
        "✅ Settings defaults: already present",
    )


def test_settings_defaults_keep_user_ponytail_choices(tmp_path: Path) -> None:
    claude = tmp_path / ".claude"
    claude.mkdir()
    (claude / "settings.json").write_text(
        json.dumps(
            {
                "env": {"PONYTAIL_DEFAULT_MODE": "full"},
                "enabledPlugins": {"ponytail@ironclaude": False},
            }
        )
    )
    assert setup.apply_settings_defaults(home=tmp_path)[0]
    settings = _settings(tmp_path)
    assert settings["env"]["PONYTAIL_DEFAULT_MODE"] == "full"
    assert settings["enabledPlugins"]["ponytail@ironclaude"] is False


def test_settings_defaults_carry_old_ponytail_opt_out(
    tmp_path: Path, monkeypatch
) -> None:
    """An opt-out under the old id ponytail@ponytail survives the rename."""
    cases = [
        ({"ponytail@ponytail": False}, False),
        ({"ponytail@ponytail": False, "ponytail@ironclaude": True}, True),
        ({"ponytail@ponytail": True}, True),
    ]
    for index, (enabled, expected) in enumerate(cases):
        home = tmp_path / str(index)
        (home / ".claude").mkdir(parents=True)
        (home / ".claude" / "settings.json").write_text(
            json.dumps({"enabledPlugins": dict(enabled)})
        )
        assert setup.apply_settings_defaults(home=home)[0]
        plugins = _settings(home)["enabledPlugins"]
        assert plugins["ponytail@ironclaude"] is expected, enabled
        assert plugins["ponytail@ponytail"] is enabled["ponytail@ponytail"]
        assert setup.apply_settings_defaults(home=home)[1] == (
            "✅ Settings defaults: already present"
        )
    # install_plugins then leaves the opted-out plugin alone.
    calls = []
    opted_out = tmp_path / "0"
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess,
        "run",
        lambda command, **_k: (
            calls.append(command[1:]) or subprocess.CompletedProcess(command, 0, "", "")
        ),
    )
    setup.install_plugins(home=opted_out)
    assert calls  # the other default plugins are still installed
    assert not any("ponytail@ironclaude" in c for c in calls)
    assert not (opted_out / setup._CATALOG_DIR).exists()


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
    # Ponytail comes only from the pinned IronClaude catalog, added before install.
    catalog_dir = home / ".claude" / "ironclaude-marketplace"
    written = json.loads(
        (catalog_dir / ".claude-plugin" / "marketplace.json").read_text()
    )
    assert written == defaults[setup._CATALOG_KEY]
    add = ["plugin", "marketplace", "add", str(catalog_dir)]
    install = ["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"]
    assert calls.index(add) < calls.index(install)
    assert not any("DietrichGebert" in " ".join(c) for c in calls)


def _pinned_home(tmp_path: Path, installed_sha: str, catalog_sha: str) -> Path:
    """A workspace with Ponytail installed and the catalog on disk."""
    home = _plugin_home(tmp_path, {"ponytail@ironclaude": True})
    plugins = home / ".claude" / "plugins"
    plugins.mkdir()
    ours = {"source": "directory", "path": str(home / setup._CATALOG_DIR)}
    (plugins / "known_marketplaces.json").write_text(
        json.dumps({"ironclaude": {"source": ours}})
    )
    record = {"scope": "user", "version": "x", "gitCommitSha": installed_sha}
    (plugins / "installed_plugins.json").write_text(
        json.dumps({"plugins": {"ponytail@ironclaude": [record]}})
    )
    catalog = json.loads(json.dumps(_defaults()[setup._CATALOG_KEY]))
    catalog["plugins"][0]["source"]["sha"] = catalog_sha
    path = home / setup._CATALOG_DIR / ".claude-plugin" / "marketplace.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(catalog))
    return home


def test_plugins_move_ponytail_to_a_new_pin(tmp_path: Path, monkeypatch) -> None:
    old = "16352ac229eb08a9598dcae48fe9f2b342567d86"  # upstream tag v5.3.2
    home = _pinned_home(tmp_path, installed_sha=old, catalog_sha=old)
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command[1:], kwargs.get("env")))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    ok, message = setup.install_plugins(home=home)
    assert ok and message.startswith("✅ Plugins"), message
    path = home / setup._CATALOG_DIR / ".claude-plugin" / "marketplace.json"
    assert json.loads(path.read_text()) == _defaults()[setup._CATALOG_KEY]
    assert [c for c, _ in calls] == [
        ["plugin", "marketplace", "update", "ironclaude"],
        ["plugin", "update", "ponytail@ironclaude", "--scope", "user"],
    ]
    # Only `plugin update` clones over HTTPS; every command uses the checked home.
    assert "CLAUDE_CONFIG_DIR" not in calls[0][1]
    assert calls[0][1]["HOME"] == str(home)
    assert "GIT_CONFIG_COUNT" not in calls[0][1]
    assert calls[1][1]["GIT_CONFIG_VALUE_0"] == "git@github.com:"


def test_plugins_run_claude_against_the_validated_home(
    tmp_path: Path, monkeypatch
) -> None:
    """Every claude command acts on the profile install_plugins checked."""
    foreign = tmp_path / "cfg" / "plugins"
    foreign.mkdir(parents=True)
    theirs = {"source": {"source": "github", "repo": "someone/ironclaude"}}
    (foreign / "known_marketplaces.json").write_text(json.dumps({"ironclaude": theirs}))
    seen = []

    def fake_run(command, **kwargs):
        # Pick the profile the way the claude CLI does.
        env = kwargs.get("env") or os.environ
        root = env.get("CLAUDE_CONFIG_DIR") or os.path.join(env["HOME"], ".claude")
        seen.append((command[1:], root, env))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setenv("SENTINEL", "kept")
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    for index, profile in enumerate((str(tmp_path / "cfg"), "")):
        monkeypatch.setenv("CLAUDE_CONFIG_DIR", profile)
        home = _plugin_home(tmp_path / str(index), {"ponytail@ironclaude": True})
        seen.clear()
        ok, message = setup.install_plugins(home=home)
        assert ok and message.startswith("✅ Plugins"), message
        assert [c for c, _, _ in seen] == [
            ["plugin", "marketplace", "add", str(home / setup._CATALOG_DIR)],
            ["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"],
        ]
        for _, root, env in seen:
            assert root == str(home / ".claude"), profile
            assert "CLAUDE_CONFIG_DIR" not in env
            assert env["SENTINEL"] == "kept"


def test_plugins_keep_ponytail_at_its_pin(tmp_path: Path, monkeypatch) -> None:
    home = _pinned_home(tmp_path, PONYTAIL_SHA, PONYTAIL_SHA)
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError)
    )
    assert setup.install_plugins(home=home) == (True, "✅ Plugins: already installed")


def _recording_run(calls: list, failing: tuple = ()):
    """A fake `claude` that records commands; commands starting with `failing` exit 1."""

    def fake_run(command, **_kwargs):
        calls.append(command[1:])
        rc = 1 if failing and tuple(command[1 : 1 + len(failing)]) == failing else 0
        return subprocess.CompletedProcess(command, rc, "", "")

    return fake_run


def test_plugins_judge_the_pin_by_the_user_scope_record(
    tmp_path: Path, monkeypatch
) -> None:
    """A project-scope copy at the pin neither hides nor replaces the user copy."""
    old = "16352ac229eb08a9598dcae48fe9f2b342567d86"  # upstream tag v5.3.2
    project = {
        "scope": "project",
        "projectPath": "/work/app",
        "gitCommitSha": PONYTAIL_SHA,
    }
    cases = {
        "mixed": (
            [{"scope": "user", "gitCommitSha": old}, project],
            [
                ["plugin", "marketplace", "update", "ironclaude"],
                ["plugin", "update", "ponytail@ironclaude", "--scope", "user"],
            ],
        ),
        "project-only": (
            [project],
            [["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"]],
        ),
    }
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    for name, (records, expected) in cases.items():
        home = _pinned_home(tmp_path / name, PONYTAIL_SHA, PONYTAIL_SHA)
        path = home / ".claude" / "plugins" / "installed_plugins.json"
        path.write_text(json.dumps({"plugins": {"ponytail@ironclaude": records}}))
        calls = []
        monkeypatch.setattr(setup.subprocess, "run", _recording_run(calls))
        ok, message = setup.install_plugins(home=home)
        assert ok and message.startswith("✅ Plugins"), (name, message)
        assert calls == expected, name


def test_plugins_refuse_a_foreign_ironclaude_marketplace(
    tmp_path: Path, monkeypatch
) -> None:
    """A marketplace that only shares the name `ironclaude` is never used."""
    other = tmp_path / "elsewhere"
    foreign_entries = [
        {"source": {"source": "github", "repo": "someone/ironclaude"}},
        {"source": {"source": "directory", "path": str(other)}},
        {"source": {"source": "directory", "path": ".claude/ironclaude-marketplace"}},
        {"source": "directory"},
        {},
        "not an object",
    ]
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    for index, entry in enumerate(foreign_entries):
        home = _pinned_home(tmp_path / str(index), "0" * 40, "0" * 40)
        registry = home / ".claude" / "plugins" / "known_marketplaces.json"
        registry.write_text(json.dumps({"ironclaude": entry}))
        before = registry.read_bytes()
        calls = []
        monkeypatch.setattr(setup.subprocess, "run", _recording_run(calls))
        ok, message = setup.install_plugins(home=home)
        assert ok and message.startswith("⚠️  Plugins"), (entry, message)
        assert "ironclaude (registered from another source" in message, entry
        assert not any("ironclaude" in " ".join(c) for c in calls), (entry, calls)
        assert registry.read_bytes() == before


def test_plugins_refuse_an_unresolvable_ironclaude_registration(
    tmp_path: Path, monkeypatch
) -> None:
    """A registered path that cannot be resolved is not ours; the run goes on."""
    (tmp_path / "a").symlink_to(tmp_path / "b")
    (tmp_path / "b").symlink_to(tmp_path / "a")
    loop = tmp_path / "a" / "catalog"  # resolve() raises RuntimeError before 3.13
    nul = str(tmp_path / "nul\x00dir")  # resolve() raises ValueError everywhere
    enabled = {"ponytail@ironclaude": True, "playwright@claude-plugins-official": True}
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    for index, bad in enumerate((str(loop), nul)):
        home = _pinned_home(tmp_path / str(index), PONYTAIL_SHA, PONYTAIL_SHA)
        settings = home / ".claude" / "settings.json"
        settings.write_text(json.dumps({"enabledPlugins": enabled}))
        registry = home / ".claude" / "plugins" / "known_marketplaces.json"
        entry = {"source": {"source": "directory", "path": bad}}
        registry.write_text(
            json.dumps({"ironclaude": entry, "claude-plugins-official": {}})
        )
        before = registry.read_bytes()
        calls = []
        monkeypatch.setattr(setup.subprocess, "run", _recording_run(calls))
        ok, message = setup.install_plugins(home=home)
        assert ok and message.startswith("⚠️  Plugins"), (bad, message)
        assert "ironclaude (registered from another source" in message, bad
        assert calls == [
            ["plugin", "install", "playwright@claude-plugins-official"]
            + ["--scope", "user", "-y"]
        ], bad
        assert registry.read_bytes() == before


def test_plugins_accept_ours_through_a_symlinked_home(
    tmp_path: Path, monkeypatch
) -> None:
    real = _pinned_home(tmp_path / "real", PONYTAIL_SHA, PONYTAIL_SHA)
    link = tmp_path / "link"
    link.symlink_to(real)
    registry = real / ".claude" / "plugins" / "known_marketplaces.json"
    ours = {"source": "directory", "path": str(link / setup._CATALOG_DIR)}
    registry.write_text(json.dumps({"ironclaude": {"source": ours}}))
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError)
    )
    assert setup.install_plugins(home=real) == (True, "✅ Plugins: already installed")


def test_plugins_skip_dependents_of_a_failed_marketplace(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    # The IronClaude catalog cannot be added: Ponytail is not installed, while
    # plugins from other marketplaces still are.
    home = _plugin_home(
        tmp_path / "add",
        {"ponytail@ironclaude": True, "playwright@claude-plugins-official": True},
    )
    calls = []
    add_ours = ("plugin", "marketplace", "add", str(home / setup._CATALOG_DIR))
    monkeypatch.setattr(setup.subprocess, "run", _recording_run(calls, add_ours))
    ok, message = setup.install_plugins(home=home)
    assert ok and "ponytail@ironclaude (marketplace ironclaude unavailable)" in message
    assert [
        "plugin",
        "install",
        "ponytail@ironclaude",
        "--scope",
        "user",
        "-y",
    ] not in (calls)
    assert [
        "plugin",
        "install",
        "playwright@claude-plugins-official",
        "--scope",
        "user",
        "-y",
    ] in calls
    # A pin move whose marketplace update fails does not update the plugin.
    old = "16352ac229eb08a9598dcae48fe9f2b342567d86"
    home = _pinned_home(tmp_path / "update", old, old)
    calls = []
    update = ("plugin", "marketplace", "update")
    monkeypatch.setattr(setup.subprocess, "run", _recording_run(calls, update))
    ok, message = setup.install_plugins(home=home)
    assert ok and "ponytail@ironclaude (marketplace ironclaude unavailable)" in message
    assert calls == [["plugin", "marketplace", "update", "ironclaude"]]

    # A marketplace command that raises counts as failed too.
    def raising_run(command, **_kwargs):
        calls.append(command[1:])
        if command[1:3] == ["plugin", "marketplace"]:
            raise subprocess.TimeoutExpired(command, 1)
        return subprocess.CompletedProcess(command, 0, "", "")

    home = _plugin_home(tmp_path / "raise", {"ponytail@ironclaude": True})
    calls = []
    monkeypatch.setattr(setup.subprocess, "run", raising_run)
    ok, message = setup.install_plugins(home=home)
    assert ok and "ponytail@ironclaude (marketplace ironclaude unavailable)" in message
    assert all(c[:2] != ["plugin", "install"] for c in calls)


def test_plugins_catalog_write_failure_is_not_fatal(
    tmp_path: Path, monkeypatch
) -> None:
    home = _plugin_home(tmp_path, {"ponytail@ironclaude": True})
    (home / setup._CATALOG_DIR).write_text("not a directory")
    calls = []
    monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")
    monkeypatch.setattr(
        setup.subprocess, "run", lambda command, **k: calls.append(command)
    )
    ok, message = setup.install_plugins(home=home)
    assert ok and message.startswith("⚠️  Plugins")
    assert "ironclaude (catalog not written)" in message
    assert not calls


def test_plugins_skip_already_installed(tmp_path: Path, monkeypatch) -> None:
    home = _plugin_home(tmp_path, {"playwright@claude-plugins-official": True})
    plugins = home / ".claude" / "plugins"
    plugins.mkdir()
    (plugins / "known_marketplaces.json").write_text(
        json.dumps({"claude-plugins-official": {}})
    )
    (plugins / "installed_plugins.json").write_text(
        json.dumps(
            {"plugins": {"playwright@claude-plugins-official": [{"scope": "user"}]}}
        )
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
    names = ("anthropics/claude-plugins-official", "playwright@claude-plugins-official")
    ok, message = setup.install_plugins(home=home)
    assert ok and message.startswith("⚠️  Plugins")
    assert all(name in message for name in names), message
    assert "--scope" not in message
    ok, message = setup.install_plugins(home=home, deadline=0)
    assert ok and "time limit" in message
    assert all(f"{name} (time limit)" in message for name in names), message
    assert "--scope" not in message


def test_plugins_skip_when_claude_cli_is_absent(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(setup.shutil, "which", lambda _name: None)
    assert setup.install_plugins(home=tmp_path) == (
        True,
        "⏭️  Plugins: claude CLI not found; skipped",
    )


def test_shipped_setup_contains_no_personal_home_paths() -> None:
    personal = re.compile(r"/Users/[A-Za-z]|/home/(?!coder/)[a-z]")
    for root in ("rules", "templates", "output-styles"):
        for path in (PKG / root).rglob("*"):
            if path.is_file() and path.suffix in (".md", ".contract", ".json"):
                assert not personal.search(path.read_text()), path
