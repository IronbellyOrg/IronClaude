"""
SuperClaude Doctor Command

Health check for SuperClaude installation.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from .install_skills import skill_activation_targets


def run_doctor(verbose: bool = False) -> Dict[str, Any]:
    """
    Run SuperClaude health checks

    Args:
        verbose: Include detailed diagnostic information

    Returns:
        Dict with check results
    """
    checks = []

    # Check 1: pytest plugin loaded
    plugin_check = _check_pytest_plugin()
    checks.append(plugin_check)

    # Check 2: Agents installed
    agents_check = _check_agents_installed()
    checks.append(agents_check)

    # Check 3: Skills installed
    skills_check = _check_skills_installed()
    checks.append(skills_check)

    # Check 4: Configuration
    config_check = _check_configuration()
    checks.append(config_check)

    return {
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }


def _check_pytest_plugin() -> Dict[str, Any]:
    """
    Check if pytest plugin is loaded

    Returns:
        Check result dict
    """
    try:
        import pytest

        # Try to get pytest config
        try:
            config = pytest.Config.fromdictargs({}, [])
            plugins = config.pluginmanager.list_plugin_distinfo()

            # Check if superclaude plugin is loaded
            superclaude_loaded = any(
                "superclaude" in str(plugin[0]).lower() for plugin in plugins
            )

            if superclaude_loaded:
                return {
                    "name": "pytest plugin loaded",
                    "passed": True,
                    "details": ["SuperClaude pytest plugin is active"],
                }
            else:
                return {
                    "name": "pytest plugin loaded",
                    "passed": False,
                    "details": ["SuperClaude plugin not found in pytest plugins"],
                }
        except Exception as e:
            return {
                "name": "pytest plugin loaded",
                "passed": False,
                "details": [f"Could not check pytest plugins: {e}"],
            }

    except ImportError:
        return {
            "name": "pytest plugin loaded",
            "passed": False,
            "details": ["pytest not installed"],
        }


def _check_agents_installed() -> Dict[str, Any]:
    """
    Check if agents are installed

    Returns:
        Check result dict
    """
    agents_dir = Path("~/.claude/agents").expanduser()

    if not agents_dir.exists():
        return {
            "name": "Agents installed",
            "passed": True,  # Optional, so pass
            "details": ["No agents installed (run 'superclaude install')"],
        }

    agents = [f.stem for f in agents_dir.glob("*.md") if f.name != "README.md"]

    if agents:
        return {
            "name": "Agents installed",
            "passed": True,
            "details": [f"{len(agents)} agent(s) installed"],
        }
    else:
        return {
            "name": "Agents installed",
            "passed": True,  # Optional
            "details": ["No agents installed (run 'superclaude install')"],
        }


def _check_skills_installed(
    skills_dir: Optional[Path] = None, commands_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Check installed skills and resolve command activation dependencies."""
    if skills_dir is None:
        skills_dir = Path.home() / ".claude" / "skills"
    if commands_dir is None:
        commands_dir = Path.home() / ".claude" / "commands" / "sc"

    # Find skills (directories with SKILL.md or implementation.md)
    skills = []
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir() and any(
                (item / m).exists()
                for m in ("SKILL.md", "skill.md", "implementation.md")
            ):
                skills.append(item.name)
    skills.sort()

    required_skills = set()
    if commands_dir.exists():
        for command_path in commands_dir.glob("*.md"):
            required_skills.update(skill_activation_targets(command_path))

    installed = set(skills)
    unresolved = sorted(
        target
        for target in required_skills
        if target not in installed and target.replace(":", "-", 1) not in installed
    )
    if unresolved:
        return {
            "name": "Skills installed",
            "passed": False,
            "details": ["Missing command-required skill(s): " + ", ".join(unresolved)],
        }

    if skills:
        return {
            "name": "Skills installed",
            "passed": True,
            "details": [f"{len(skills)} skill(s) installed: {', '.join(skills)}"],
        }

    return {
        "name": "Skills installed",
        "passed": True,  # Optional when no installed command requires one
        "details": ["No skills installed (optional)"],
    }


def _check_configuration() -> Dict[str, Any]:
    """
    Check SuperClaude configuration

    Returns:
        Check result dict
    """
    # Check if package is importable
    try:
        import superclaude

        version = superclaude.__version__

        return {
            "name": "Configuration",
            "passed": True,
            "details": [f"SuperClaude {version} installed correctly"],
        }
    except ImportError as e:
        return {
            "name": "Configuration",
            "passed": False,
            "details": [f"Could not import superclaude: {e}"],
        }
