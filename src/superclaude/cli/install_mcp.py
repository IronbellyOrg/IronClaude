"""
MCP Server Installation Module for SuperClaude

Installs and manages MCP servers using the latest Claude Code API.
Based on the installer logic from commit d4a17fc but adapted for modern Claude Code.
"""

import json
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click

from superclaude.cli import install_codebase_memory as codebase_memory

# AIRIS MCP Gateway - Unified MCP solution (recommended)
AIRIS_GATEWAY = {
    "name": "airis-mcp-gateway",
    "description": "Unified MCP gateway with 60+ tools, HOT/COLD management, 98% token reduction",
    "transport": "sse",
    "endpoint": "http://localhost:9400/sse",
    "docker_compose_url": "https://raw.githubusercontent.com/agiletec-inc/airis-mcp-gateway/main/docker-compose.dist.yml",
    "mcp_config_url": "https://raw.githubusercontent.com/agiletec-inc/airis-mcp-gateway/main/config/mcp-config.template.json",
    "repository": "https://github.com/agiletec-inc/airis-mcp-gateway",
}

# Pinned Tavily MCP package version — single source of truth for the pin (review L3).
# Docs/YAML keep the literal `tavily-mcp@0.2.22`, guarded by test_tavily_version_single_pin.
TAVILY_MCP_VERSION = "0.2.22"

# Individual MCP Server Registry (legacy, for users who prefer individual servers)
# Adapted from commit d4a17fc with modern transport configuration
MCP_SERVERS = {
    "context7": {
        "name": "context7",
        "description": "Official library documentation and code examples",
        "transport": "stdio",
        "command": "npx -y @upstash/context7-mcp",
        "required": False,
    },
    "playwright": {
        "name": "playwright",
        "description": "Cross-browser E2E testing and automation",
        "transport": "stdio",
        "command": "npx -y @playwright/mcp@latest",
        "required": False,
    },
    "serena": {
        "name": "serena",
        "description": "Semantic code analysis and intelligent editing",
        "transport": "stdio",
        "command": "uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false",
        "required": False,
    },
    "morphllm-fast-apply": {
        "name": "morphllm-fast-apply",
        "description": "Fast Apply capability for context-aware code modifications",
        "transport": "stdio",
        "command": "npx -y @morphllm/morphmcp",
        "required": False,
        "api_key_env": "MORPH_API_KEY",
        "api_key_description": "Morph API key for Fast Apply",
    },
    "tavily": {
        "name": "tavily",
        "description": "Web search and real-time information retrieval for deep research",
        "transport": "stdio",
        "command": f"npx -y tavily-mcp@{TAVILY_MCP_VERSION}",
        "required": False,
        "api_key_env": "TAVILY_API_KEY",
        "api_key_description": "Tavily API key for web search (get from https://app.tavily.com)",
        "default_parameters": {"search_depth": "basic", "max_results": 10},
    },
    "auggie": {
        "name": "auggie",
        "description": "Augment Code semantic codebase search (codebase-retrieval, ask_question)",
        "transport": "stdio",
        "command": "auggie --mcp --mcp-auto-workspace",
        "required": False,
        "requires_global_binary": {
            "binary": "auggie",
            "install_command": "npm install -g @augmentcode/auggie@0.36.0",
            "package": "@augmentcode/auggie",
            "version": "0.36.0",
            "min_node_version": 20,
        },
        "post_install_message": (
            "   🔑 Auggie requires one-time authentication.\n"
            "      Run: auggie login   (opens browser for OAuth)\n"
            "      Headless alternative: set AUGMENT_SESSION_AUTH env var\n"
            "      Docs: https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code"
        ),
    },
    "codebase-memory-mcp": {
        "name": "codebase-memory-mcp",
        "description": "Native codebase graph memory with full upstream companion setup",
        "transport": "stdio",
        "command": "codebase-memory-mcp",
        "args": [],
        "required": False,
    },
    # Appended last so the numbered install menu keeps its existing numbers.
    # The header value stays the literal ${LITELLM_API_KEY}: Claude Code expands it from the
    # environment at connect time, so no key is stored in the registration.
    "litellm": {
        "name": "litellm",
        "description": "LiteLLM MCP gateway: hosted Augment search, Tavily and Context7 behind one endpoint",
        "transport": "http",
        "url": "http://ibcore:4000/mcp/",
        "headers": {"x-litellm-api-key": "Bearer ${LITELLM_API_KEY}"},
        "required": False,
        "opt_in_only": True,
    },
}


def _run_command(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run a command with proper cross-platform shell handling.

    Args:
        cmd: Command as list of strings
        **kwargs: Additional subprocess.run arguments

    Returns:
        CompletedProcess result
    """
    # Ensure UTF-8 encoding on all platforms to handle Unicode output
    if "encoding" not in kwargs:
        kwargs["encoding"] = "utf-8"
    if "errors" not in kwargs:
        kwargs["errors"] = "replace"  # Replace undecodable bytes instead of raising

    if platform.system() == "Windows":
        # On Windows, wrap command in 'cmd /c' to properly handle commands like npx
        cmd = ["cmd", "/c"] + cmd
        return subprocess.run(cmd, **kwargs)
    else:
        # macOS/Linux: Use string format with proper shell to support aliases
        cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)

        # Use the user's shell to execute the command, supporting aliases
        user_shell = os.environ.get("SHELL", "/bin/bash")
        return subprocess.run(
            cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs
        )


def check_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = _run_command(
            ["docker", "info"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_binary_available(
    binary_name: str, expected_version: Optional[str] = None
) -> bool:
    """Check that a PATH binary runs and, when requested, has an exact version."""
    try:
        result = _run_command(
            [binary_name, "--version"], capture_output=True, text=True, timeout=10
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

    if result.returncode != 0:
        return False
    if expected_version is None:
        return True

    output = result.stdout or ""
    return bool(re.search(rf"(?<!\d){re.escape(expected_version)}(?!\d)", output))


def check_node_version(minimum: int) -> bool:
    """Check that Node.js meets a package-specific minimum major version."""
    try:
        result = _run_command(
            ["node", "--version"], capture_output=True, text=True, timeout=10
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

    if result.returncode != 0:
        return False
    try:
        return int((result.stdout or "").strip().lstrip("v").split(".")[0]) >= minimum
    except (ValueError, IndexError):
        return False


def ensure_global_binary(req: Dict, dry_run: bool) -> bool:
    """Ensure a required global binary is present at its pinned version."""
    binary = req["binary"]
    expected_version = req.get("version")
    min_node_version = req.get("min_node_version")
    if dry_run:
        click.echo(
            f"[DRY RUN] Would verify {binary} version {expected_version}; if missing or stale, request separate approval for: {req['install_command']}"
        )
        return True
    if min_node_version is not None and not check_node_version(min_node_version):
        click.echo(
            f"   ❌ Node.js {min_node_version}+ is required for {req['package']}",
            err=True,
        )
        return False
    if check_binary_available(binary, expected_version):
        return True

    version_note = f" version {expected_version}" if expected_version else ""
    click.echo(f"   ⚠️  '{binary}'{version_note} not available on PATH")
    click.echo(f"   Required: {req['install_command']}")
    if not click.confirm(f"   Install {req['package']} globally now?", default=True):
        click.echo(f"   ⏭️  Skipping {binary} (required binary unavailable)")
        return False

    click.echo(f"   📦 Running: {req['install_command']}")
    install_result = _run_command(
        shlex.split(req["install_command"]), capture_output=True, text=True, timeout=300
    )
    if install_result.returncode != 0:
        click.echo(f"   ❌ Global install failed: {install_result.stderr}", err=True)
        return False
    if not check_binary_available(binary, expected_version):
        click.echo(
            f"   ❌ '{binary}' did not report required version {expected_version} after install",
            err=True,
        )
        return False

    click.echo(f"   ✅ {req['package']} installed globally")
    return True


def install_airis_gateway(dry_run: bool = False) -> bool:
    """
    Install AIRIS MCP Gateway using Docker.

    Installs to ~/.superclaude/airis-mcp-gateway/ to avoid polluting the host.

    Returns:
        True if successful, False otherwise
    """
    from pathlib import Path

    click.echo("\n🚀 Installing AIRIS MCP Gateway (Recommended)")
    click.echo(
        "   This provides 60+ tools through a single endpoint with 98% token reduction.\n"
    )

    install_dir = Path.home() / ".superclaude" / "airis-mcp-gateway"
    compose_file = install_dir / "docker-compose.yml"
    if dry_run:
        click.echo(
            f"[DRY RUN] Would create {install_dir}, download {AIRIS_GATEWAY['docker_compose_url']}, create .env, start Docker Compose and register with Claude Code. Docker is required only for actual installation."
        )
        return True
    if not check_docker_available():
        click.echo("Docker is required but not available.", err=True)
        return False
    click.echo("Docker is available")

    # Create installation directory
    install_dir.mkdir(parents=True, exist_ok=True)
    click.echo(f"   📁 Installation directory: {install_dir}")

    # Download docker-compose file
    click.echo("   📥 Downloading docker-compose configuration...")
    try:
        result = _run_command(
            [
                "curl",
                "-fsSL",
                "-o",
                str(compose_file),
                AIRIS_GATEWAY["docker_compose_url"],
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            click.echo(
                f"   ❌ Failed to download docker-compose file: {result.stderr}",
                err=True,
            )
            return False
    except Exception as e:
        click.echo(f"   ❌ Error downloading: {e}", err=True)
        return False

    # Download mcp-config.json (backend server definitions for the gateway)
    mcp_config_file = install_dir / "mcp-config.json"
    if not mcp_config_file.exists():
        click.echo("   📥 Downloading MCP server configuration...")
        try:
            result = _run_command(
                [
                    "curl",
                    "-fsSL",
                    "-o",
                    str(mcp_config_file),
                    AIRIS_GATEWAY["mcp_config_url"],
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode != 0:
                click.echo(
                    f"   ⚠️  Failed to download mcp-config.json: {result.stderr}",
                    err=True,
                )
                # Create a minimal default config so the gateway can start
                import json

                default_config = {
                    "mcpServers": {
                        "memory": {
                            "command": "npx",
                            "args": ["-y", "@modelcontextprotocol/server-memory"],
                            "env": {},
                            "enabled": True,
                            "mode": "hot",
                            "description": "Session memory",
                        }
                    },
                    "log": {"level": "info"},
                }
                mcp_config_file.write_text(json.dumps(default_config, indent=2))
                click.echo("   ✅ Created minimal default mcp-config.json")
            else:
                # Disable servers that require containers not in docker-compose.dist.yml
                import json

                try:
                    config = json.loads(mcp_config_file.read_text())
                    servers_to_disable = ["airis-agent", "mindbase"]
                    changed = False
                    for server_name in servers_to_disable:
                        if server_name in config.get("mcpServers", {}):
                            config["mcpServers"][server_name]["enabled"] = False
                            changed = True
                    if changed:
                        mcp_config_file.write_text(json.dumps(config, indent=2))
                    click.echo("   ✅ MCP server configuration downloaded")
                except (json.JSONDecodeError, KeyError):
                    click.echo(
                        "   ⚠️  Could not parse mcp-config.json, using as-is",
                        err=True,
                    )
        except Exception as e:
            click.echo(f"   ❌ Error downloading mcp-config.json: {e}", err=True)
            # Create empty but valid config so Docker mount doesn't fail
            mcp_config_file.write_text('{"mcpServers": {}}')
    else:
        click.echo("   ✅ MCP server configuration already exists")

    # Create .env file if it doesn't exist
    env_file = install_dir / ".env"
    if not env_file.exists():
        click.echo("   📝 Creating .env file with default configuration...")
        workspace_dir = Path.home() / "github"
        env_content = f"""# AIRIS MCP Gateway Configuration
# Edit this file to customize your setup

# Workspace directory (host path mounted into containers)
HOST_WORKSPACE_DIR={workspace_dir}

# AIRIS mode (embedded = single-container gateway only)
AIRIS_MODE=embedded

# Mindbase URL (if using mindbase MCP server)
MINDBASE_URL=http://host.docker.internal:18003

# Tavily API key for web search (get from https://app.tavily.com)
TAVILY_API_KEY=
"""
        env_file.write_text(env_content)
        click.echo(f"   ✅ Created .env file at {env_file}")
        click.echo(
            f"   💡 Edit {env_file} to customize settings (e.g., add TAVILY_API_KEY)"
        )
    else:
        click.echo("   ✅ .env file already exists")

    # Start the gateway from the installation directory
    click.echo("   🐳 Starting AIRIS MCP Gateway containers...")
    try:
        result = _run_command(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "--project-directory",
                str(install_dir),
                "up",
                "-d",
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            click.echo(f"   ❌ Failed to start containers: {result.stderr}", err=True)
            return False
    except subprocess.TimeoutExpired:
        click.echo("   ❌ Timeout starting containers", err=True)
        return False

    click.echo("   ✅ Gateway containers started")

    # Wait for gateway to become healthy
    click.echo("   🔍 Checking gateway health...")
    import time

    gateway_healthy = False
    for attempt in range(1, 7):
        try:
            result = _run_command(
                ["curl", "-sf", "http://localhost:9400/health"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                click.echo("   ✅ Gateway is healthy")
                gateway_healthy = True
                break
        except Exception:
            pass

        if attempt < 6:
            click.echo(f"   ⏳ Waiting for gateway to start (attempt {attempt}/6)...")
            time.sleep(5)

    if not gateway_healthy:
        click.echo(
            "   ⚠️  Gateway may still be starting. Check with: curl http://localhost:9400/health",
            err=True,
        )

    # Register with Claude Code
    # SSE transport takes the URL directly (not via npx mcp-remote)
    click.echo("   📝 Registering with Claude Code...")
    try:
        cmd = [
            "claude",
            "mcp",
            "add",
            "--scope",
            "user",
            "--transport",
            "sse",
            AIRIS_GATEWAY["name"],
            AIRIS_GATEWAY["endpoint"],
        ]
        result = _run_command(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            # May already be registered
            if "already exists" in (result.stderr or "").lower():
                click.echo("   ✅ Already registered with Claude Code")
            else:
                click.echo(f"   ⚠️  Registration warning: {result.stderr}", err=True)
        else:
            click.echo("   ✅ Registered with Claude Code")
    except Exception as e:
        click.echo(f"   ⚠️  Registration error: {e}", err=True)

    click.echo("\n✅ AIRIS MCP Gateway installed successfully!")
    click.echo(f"\n📁 Installed to: {install_dir}")
    click.echo("\n📖 Next steps:")
    click.echo("   • Health check: curl http://localhost:9400/health")
    click.echo("   • Web UI: http://localhost:9400")
    click.echo(f"   • Manage: cd {install_dir} && docker compose logs -f")
    click.echo(f"   • Documentation: {AIRIS_GATEWAY['repository']}")
    return True


def _is_interactive() -> bool:
    return sys.stdin.isatty()


def _native_selection_error(scope: str) -> Optional[str]:
    if scope != "user":
        return "Codebase Memory full native lifecycle supports user scope only."
    if platform.system() != "Linux" or platform.machine().lower() not in {
        "amd64",
        "x86_64",
        "arm64",
        "aarch64",
    }:
        return "Automated Codebase Memory lifecycle requires Linux amd64/arm64; use the official manual mechanism on other platforms."
    return None


def _native_lifecycle_notice() -> str:
    return (
        f"Upstream source: {codebase_memory.INSTALL_URL}. Native location: {codebase_memory.canonical_executable()}. "
        "This user/account-wide lifecycle affects detected clients and companion instructions, skills, agents and hooks; graph indexes are retained."
    )


def check_prerequisites(
    selected_servers: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """Check only selected requirements, before any selected installer runs."""
    selected = list(MCP_SERVERS) if selected_servers is None else selected_servers
    errors = []
    try:
        result = _run_command(
            ["claude", "--version"], capture_output=True, text=True, timeout=10
        )
        if result is None or result.returncode != 0:
            errors.append("Claude CLI not found - required for MCP server management")
    except (OSError, subprocess.SubprocessError):
        errors.append(
            "Claude CLI readiness failed - required for MCP server management"
        )

    node_min = 0
    needs_npx = False
    for name in selected:
        info: Dict = MCP_SERVERS.get(name, {})
        if info.get("command", "").startswith(("npx ", "npm ")):
            node_min = max(node_min, 18)
        needs_npx = needs_npx or info.get("command", "").startswith("npx ")
        node_min = max(
            node_min, info.get("requires_global_binary", {}).get("min_node_version", 0)
        )
    if node_min:
        try:
            if not check_node_version(node_min):
                errors.append(f"Node.js {node_min}+ required for selected npm servers")
        except (OSError, subprocess.SubprocessError):
            errors.append(f"Node.js {node_min}+ required for selected npm servers")
    try:
        if needs_npx and not check_binary_available("npx"):
            errors.append("npx/npm is required for selected npm servers")
        if "auggie" in selected:
            auggie: Dict = MCP_SERVERS["auggie"]
            requirement = auggie["requires_global_binary"]
            if not check_binary_available(
                requirement["binary"], requirement["version"]
            ) and not check_binary_available("npm"):
                errors.append("npm is required to acquire the selected Auggie binary")
    except (OSError, subprocess.SubprocessError):
        errors.append("Selected npm executable readiness failed")
    if "airis-mcp-gateway" in selected:
        try:
            if shutil.which("curl") is None:
                errors.append("curl is required for AIRIS MCP Gateway installation")
            if not check_docker_available():
                errors.append(
                    "Docker must be available and running for AIRIS MCP Gateway"
                )
        except (OSError, subprocess.SubprocessError):
            errors.append("Docker readiness failed for AIRIS MCP Gateway")
    if "serena" in selected:
        # Retain the existing optional uv advisory, but only for its consumer.
        try:
            result = _run_command(
                ["uv", "--version"], capture_output=True, text=True, timeout=10
            )
            if result is None or result.returncode != 0:
                click.echo("uv not found - required to run Serena MCP server", err=True)
        except (OSError, subprocess.SubprocessError):
            click.echo("uv not found - required to run Serena MCP server", err=True)
    if codebase_memory.BINARY_NAME in selected:
        found = codebase_memory.discover_executable()
        if found.state == "ambiguous" or (
            found.state == "non_runnable"
            and found.executable != codebase_memory.canonical_executable()
        ):
            errors.append(
                "Native executable discovery is ambiguous or externally non-runnable; resolve it before installation"
            )
        elif found.state not in {"canonical", "external"}:
            for tool in ("curl", "bash"):
                if shutil.which(tool) is None:
                    errors.append(f"{tool} is required for missing native acquisition")
    return not errors, errors


def check_mcp_server_installed(server_name: str) -> bool:
    """Check if an MCP server is already installed."""
    try:
        result = _run_command(
            ["claude", "mcp", "list"], capture_output=True, text=True, timeout=60
        )

        if result is None or result.returncode != 0:
            return False

        # Handle case where stdout might be None
        output = result.stdout
        if output is None:
            return False

        # Parse output to check if server is installed
        return server_name.lower() in output.lower()

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False


def _run_mcp_get(server_name: str) -> Optional[str]:
    """Return the raw stdout of ``claude mcp get <name>``, or ``None``.

    ``claude mcp get`` is an EXACT-name lookup (unlike the ``claude mcp list`` substring scan
    behind :func:`check_mcp_server_installed`), so a non-``None`` return means a server named
    exactly ``server_name`` is registered. ``None`` means it is not registered (non-zero exit)
    or the command could not be run.
    """
    try:
        result = _run_command(
            ["claude", "mcp", "get", server_name],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return None

    if result is None or result.returncode != 0:
        return None
    return result.stdout or None


def _parse_mcp_get_command(output: str) -> Optional[str]:
    """Normalize the ``Command:`` / ``Args:`` lines of ``claude mcp get`` into a single
    ``"<command> <args>"`` string, e.g. ``"npx -y tavily-mcp@0.2.22"``.

    Returns ``None`` when no ``Command:`` line is present, OR when the ``Args:`` line has
    malformed/unbalanced quoting (``shlex.split`` raising ``ValueError``). The ValueError is
    swallowed deliberately: an unparseable registration must be treated as "cannot confirm
    up-to-date" and re-registered, never crash the install.
    """
    command_word: Optional[str] = None
    args_str = ""
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("Command:"):
            command_word = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Args:"):
            args_str = stripped.split(":", 1)[1].strip()

    if not command_word:
        return None

    try:
        tokens = [command_word] + (shlex.split(args_str) if args_str else [])
    except ValueError:
        return None
    return " ".join(tokens)


def _parse_mcp_get_url(output: str) -> Optional[str]:
    """Return the ``URL:`` line of ``claude mcp get`` for an HTTP server, or ``None``."""
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("URL:"):
            return stripped.split(":", 1)[1].strip() or None
    return None


def _parse_mcp_get_headers(output: str) -> Dict[str, str]:
    """Return the ``Headers:`` block of ``claude mcp get`` as ``{name: value}``."""
    headers: Dict[str, str] = {}
    in_headers = False
    for line in output.splitlines():
        stripped = line.strip()
        if stripped == "Headers:":
            in_headers = True
        elif in_headers:
            if not stripped or ":" not in stripped:
                break
            name, value = stripped.split(":", 1)
            headers[name.strip()] = value.strip()
    return headers


def _http_signature(url: str, headers: Dict[str, str]) -> str:
    """One comparable string for an HTTP registration: the URL, then sorted headers."""
    pairs = (f"{name}: {value}" for name, value in sorted(headers.items()))
    return " ".join([url, *pairs])


def _parse_mcp_get_scope(output: str) -> Optional[str]:
    """Normalize the ``Scope:`` line of ``claude mcp get`` into ``local`` | ``user`` |
    ``project``, or ``None`` when absent/unrecognized.

    Used to target a re-register's ``claude mcp remove`` at the scope where the server
    actually lives — never the (possibly different, possibly empty) install-target scope.
    """
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("Scope:"):
            words = stripped.split(":", 1)[1].strip().lower().split()
            first = words[0] if words else ""
            return first if first in ("local", "user", "project") else None
    return None


def get_registered_mcp_command(server_name: str) -> Optional[str]:
    """Return the normalized ``command + args`` string of a registered MCP server.

    Thin wrapper over ``claude mcp get`` parsing. Returns ``None`` when the server is not
    registered OR its registration cannot be parsed (including malformed quoting). Callers
    MUST treat ``None`` as "cannot confirm up-to-date" and reconcile — never as a match (fail
    toward correctness, never toward a silent stale skip).
    """
    output = _run_mcp_get(server_name)
    if output is None:
        return None
    return _parse_mcp_get_command(output)


def prompt_for_api_key(
    server_name: str, env_var: str, description: str
) -> Optional[str]:
    """Prompt user for API key if needed."""
    click.echo(f"\n🔑 MCP server '{server_name}' requires an API key")
    click.echo(f"   Environment variable: {env_var}")
    click.echo(f"   Description: {description}")

    # Check if already set in environment
    if os.getenv(env_var):
        click.echo(f"   ✅ {env_var} already set in environment")
        return os.getenv(env_var)

    # Prompt user
    if click.confirm(f"   Would you like to set {env_var} now?", default=True):
        api_key = click.prompt(f"   Enter {env_var}", hide_input=True)
        return api_key
    else:
        click.echo(
            f"   ⚠️  Proceeding without {env_var} - server may not function properly"
        )
        return None


def read_user_mcp_entry(server_name: str) -> tuple[bool, dict | None]:
    """Read ONLY the exact top-level user entry; False means lookup is unknown.

    Unscoped `mcp get` can return a shadowing local/project entry and its text
    loses JSON fields. Keep existing legacy lookup behavior for other servers.
    No writer lives here: all mutations go through the scoped Claude CLI.
    """

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    try:
        config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
        if config_dir == "":
            return False, None
        path = (
            Path(config_dir).expanduser() if config_dir is not None else Path.home()
        ) / ".claude.json"
        try:
            root = json.loads(
                path.read_text(encoding="utf-8"), object_pairs_hook=unique_object
            )
        except FileNotFoundError:
            return (False, None) if path.is_symlink() else (True, None)
        if not isinstance(root, dict):
            return False, None
        servers = root.get("mcpServers", {})
        if not isinstance(servers, dict):
            return False, None
        if server_name not in servers:
            return True, None
        entry = servers[server_name]
        return (True, entry) if isinstance(entry, dict) else (False, None)
    except (OSError, ValueError, RuntimeError):
        # Never include file contents or exception text: either may contain keys.
        return False, None


def _native_registration_matches(entry: dict | None, executable: Path) -> bool:
    return bool(
        entry is not None
        and entry.get("type", "stdio") == "stdio"
        and entry.get("command") == str(executable)
        and entry.get("args", []) == []
    )


def _run_registration_command(cmd: list[str]) -> bool:
    """Do not expose Claude output/exception argv, which can contain old secrets."""
    try:
        result = _run_command(cmd, capture_output=True, text=True, timeout=60)
        return result is not None and result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _add_user_native_entry(entry: dict) -> bool:
    return _run_registration_command(
        [
            "claude",
            "mcp",
            "add-json",
            codebase_memory.BINARY_NAME,
            json.dumps(entry),
            "--scope",
            "user",
        ]
    )


def _restore_user_native_entry(previous: dict, attempted: dict) -> bool:
    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if not known:
        return False
    if current == previous:
        return True
    if current is not None:
        # A timed-out add may have written our entry. Do not overwrite a third
        # party's concurrent edit when its contents cannot be attributed to us.
        if current != attempted or not _run_registration_command(
            [
                "claude",
                "mcp",
                "remove",
                codebase_memory.BINARY_NAME,
                "--scope",
                "user",
            ]
        ):
            return False
    if not _add_user_native_entry(previous):
        return False
    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    return known and current == previous


def install_codebase_memory_mcp(
    *, scope: str = "user", dry_run: bool = False
) -> tuple[bool, str]:
    """Shared native install/register boundary for framework and MCP callers."""
    invalid = _native_selection_error(scope)
    if invalid:
        return False, invalid
    if dry_run:
        return (
            True,
            "[DRY RUN] "
            + _native_lifecycle_notice()
            + " Would reuse a usable executable or acquire full upstream setup if missing, then ensure exact user stdio registration. No changes made.",
        )
    try:
        ready = _run_command(
            ["claude", "--version"], capture_output=True, text=True, timeout=10
        )
        if ready is None or ready.returncode != 0:
            return (
                False,
                "Prerequisites: Claude CLI is unavailable; acquisition was not started.",
            )
    except (OSError, subprocess.SubprocessError):
        return (
            False,
            "Prerequisites: Claude CLI readiness failed; acquisition was not started.",
        )

    click.echo(_native_lifecycle_notice())
    click.echo("Acquisition: preparing Codebase Memory through the native helper.")
    acquired = codebase_memory.acquire_codebase_memory(scope=scope)
    if not acquired.success:
        return False, f"Acquisition ({acquired.stage}) failed: {acquired.message}"
    executable = acquired.executable
    if executable is None or not executable.is_absolute() or not acquired.version:
        return (
            False,
            "Executable verification: native helper did not provide an absolute executable and version.",
        )
    click.echo(f"Executable verification: {acquired.version} at {executable}")

    known, previous = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if not known:
        return (
            False,
            "Registration lookup failed: cannot establish the exact user entry; no registration reconciliation was attempted.",
        )
    success_message = f"Registration: exact user stdio entry verified ({acquired.version}). Restart clients to load integrations; no indexing or live MCP handshake was performed."
    if _native_registration_matches(previous, executable):
        return True, success_message
    expected = {"type": "stdio", "command": str(executable), "args": []}
    if previous is not None and (previous.get("env") or previous.get("headers")):
        # Restoring this entry would put its values on a process command line
        # (`claude mcp add-json` takes JSON only as an argument), so never replace it.
        return (
            False,
            "Registration: the existing user codebase-memory-mcp entry has env or headers values, so it was not replaced. Update it by hand or remove it with `claude mcp remove codebase-memory-mcp --scope user`, then retry.",
        )
    if previous is not None and not _run_registration_command(
        [
            "claude",
            "mcp",
            "remove",
            codebase_memory.BINARY_NAME,
            "--scope",
            "user",
        ]
    ):
        # A failed or timed-out remove may still have persisted; only `previous`
        # is attributable to us here, so never remove an entry that differs from it.
        if _restore_user_native_entry(previous, previous):
            return (
                False,
                "Registration removal failed; previous user registration is intact. No replacement was attempted.",
            )
        return (
            False,
            "Registration removal failed; restoration failed. User registration may be partial; inspect it before retrying.",
        )
    added = _add_user_native_entry(expected)
    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if added and known and _native_registration_matches(current, executable):
        return True, success_message
    failure = "Registration verification failed" if added else "Registration add failed"
    if previous is not None:
        if _restore_user_native_entry(previous, expected):
            return (
                False,
                f"{failure}; previous user registration restored. Retry the installation.",
            )
        return (
            False,
            f"{failure}; restoration failed. User registration may be partial; inspect it before retrying.",
        )
    return (
        False,
        f"{failure}; user registration may be partial. Inspect it before retrying.",
    )


def _cleanup_user_native_registration() -> tuple[bool, str]:
    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if not known:
        return (
            False,
            "Registration lookup failed; possible partial removal. Inspect user configuration before retrying.",
        )
    if entry is None:
        return True, "Exact user registration is absent."
    if not _run_registration_command(
        [
            "claude",
            "mcp",
            "remove",
            codebase_memory.BINARY_NAME,
            "--scope",
            "user",
        ]
    ):
        return (
            False,
            "User registration cleanup failed; possible partial removal. Inspect it before retrying.",
        )
    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if not known or entry is not None:
        return (
            False,
            "User registration absence could not be verified; possible partial removal. Inspect it before retrying.",
        )
    return (
        True,
        "Exact user registration removed; other scopes were not changed by IronClaude.",
    )


def _exec_claude(argv: list[str], timeout: float) -> int:
    """Run ``claude`` directly (no shell) in its own session; kill the group on timeout.

    Output is discarded: Claude's text or the exception argv can contain old secrets.
    Raises ``subprocess.TimeoutExpired`` after the process group is killed.
    """
    process = subprocess.Popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            process.kill()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
        raise


def _remove_exact_user_entry(
    name: str,
    matcher,
    *,
    deadline: float | None = None,
    per_call_timeout: float = 10.0,
) -> str:
    """Remove the user-scope entry ``name`` only while ``matcher(entry)`` is true.

    The entry is re-read and re-matched right before ``claude mcp remove`` and read
    again afterwards. Returns one of: removed, absent, changed (no longer matches
    before removal; kept), replaced (a different shape appeared after removal; kept),
    unverified, unknown (lookup failed), timeout, failed, skipped (``deadline`` hit,
    a ``time.monotonic()`` value). Nothing is ever retried.
    """
    known, entry = read_user_mcp_entry(name)
    if not known:
        return "unknown"
    if entry is None:
        return "absent"
    if not matcher(entry):
        return "changed"
    timeout = per_call_timeout
    if deadline is not None:
        timeout = min(timeout, deadline - time.monotonic())
        if timeout <= 0:
            return "skipped"
    try:
        returncode = _exec_claude(
            ["claude", "mcp", "remove", name, "--scope", "user"], timeout
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    except OSError:
        return "failed"
    if returncode != 0:
        return "failed"
    known, after = read_user_mcp_entry(name)
    if not known:
        return "unverified"
    if after is None:
        return "removed"
    return "unverified" if matcher(after) else "replaced"


def uninstall_codebase_memory_mcp(
    *, scope: str = "user", confirmed: bool = False, dry_run: bool = False
) -> tuple[bool, str]:
    """Account-wide native removal, then exact-user residual cleanup, with no prompts."""
    if scope != "user":
        return False, "Full Codebase Memory removal supports user scope only."
    preview = codebase_memory.preview_codebase_memory_removal()
    if preview.state not in {"ready", "missing"}:
        return False, preview.message
    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
    if not known:
        return (
            False,
            "Registration lookup failed before removal; no native removal or registration cleanup was attempted.",
        )
    partial = "Registration-only partial cleanup: companion assets were not audited or removed; indexes and updater are retained."
    if dry_run:
        plan = (
            partial
            if preview.state == "missing" and entry is not None
            else preview.message
        )
        return (
            True,
            "[DRY RUN] "
            + _native_lifecycle_notice()
            + " "
            + plan
            + " No native lifecycle, registration changes or prompts were performed.",
        )
    if not confirmed:
        return (
            False,
            preview.message
            + " Explicit confirmation is required (default No); no removal was performed.",
        )
    if preview.state == "missing":
        if entry is None:
            return (
                True,
                "Native executable and exact user registration are absent; no changes made. Companion assets were not audited; indexes and updater are retained.",
            )
        success, message = _cleanup_user_native_registration()
        return success, partial + " " + message

    removed = codebase_memory.uninstall_codebase_memory(scope=scope, confirmed=True)
    if not removed.success:
        return False, removed.message
    success, message = _cleanup_user_native_registration()
    combined = removed.message + " " + message
    if removed.remaining:
        combined += (
            " Alternate PATH entries remain: "
            + ", ".join(map(str, removed.remaining))
            + "."
        )
    return success, combined


def install_mcp_server(
    server_info: Dict, scope: str = "user", dry_run: bool = False
) -> bool:
    """
    Install a single MCP server using modern Claude Code API.

    Args:
        server_info: Server configuration dictionary
        scope: Installation scope (local, project, user)
        dry_run: If True, only show what would be done

    Returns:
        True if successful, False otherwise
    """
    server_name = server_info["name"]
    if server_name == codebase_memory.BINARY_NAME:
        success, message = install_codebase_memory_mcp(scope=scope, dry_run=dry_run)
        click.echo(message, err=not success)
        return success
    transport = server_info["transport"]
    command = server_info.get("command")

    click.echo(f"📦 Installing MCP server: {server_name}")

    # Validate global executables before registration reconciliation so a matching
    # Claude MCP command cannot hide an outdated binary behind it.
    if "requires_global_binary" in server_info and not ensure_global_binary(
        server_info["requires_global_binary"], dry_run
    ):
        return False

    # Check if already installed — and, if so, reconcile version/command drift instead of
    # blindly skipping. A name-only short-circuit silently strands users on a stale pin when
    # the registry version is bumped (e.g. tavily-mcp 0.1.2 -> 0.2.22).
    #
    # check_mcp_server_installed() is only a cheap *substring* scan of `claude mcp list`, so it
    # can false-positive on a similarly-named server or a match in another scope. Before doing
    # anything destructive we re-confirm with `claude mcp get` (an EXACT-name lookup) and
    # reconcile ONLY the precise server it returns — removing it from the scope where it
    # actually lives, never a different (possibly empty) scope that would fail the install.
    if check_mcp_server_installed(server_name):
        registered_output = _run_mcp_get(server_name)
        if registered_output is None:
            # Substring matched but there is no exact-name registration to reconcile (a
            # similarly-named server, or a non-exact list hit). Nothing of ours to remove —
            # fall through and install fresh rather than removing the wrong server.
            click.echo(
                f"   ℹ️  No exact '{server_name}' registration to reconcile; installing fresh."
            )
        else:
            if transport == "http":
                expected_command = _http_signature(
                    server_info["url"], server_info.get("headers", {})
                )
                registered_url = _parse_mcp_get_url(registered_output)
                registered_command = (
                    _http_signature(
                        registered_url, _parse_mcp_get_headers(registered_output)
                    )
                    if registered_url
                    else None
                )
            else:
                expected_command = " ".join(shlex.split(command))
                registered_command = _parse_mcp_get_command(registered_output)
            if (
                registered_command is not None
                and registered_command == expected_command
            ):
                click.echo(f"   ✅ Already installed and up to date: {server_name}")
                return True

            # Drift (version/command change) or an unparseable registration -> re-register.
            registered_scope = _parse_mcp_get_scope(registered_output)
            old_display = registered_command or "<unparseable registration>"
            click.echo(
                f"   ♻️  Re-registering {server_name}: {old_display} → {expected_command}"
            )
            if dry_run:
                click.echo(
                    f"   [DRY RUN] Would re-register {server_name} "
                    f"({old_display} → {expected_command})"
                )
                return True

            # Remove from the scope where the server actually lives (parsed from
            # `claude mcp get`), NOT the install-target scope — the two can differ, and a
            # remove aimed at the wrong scope would fail and abort the install. When the scope
            # is unknown, omit --scope so the CLI removes it from whichever scope it exists in.
            remove_cmd = ["claude", "mcp", "remove", server_name]
            if registered_scope is not None and registered_scope != "local":
                remove_cmd.extend(["--scope", registered_scope])
            remove_result = _run_command(
                remove_cmd, capture_output=True, text=True, timeout=60
            )
            if remove_result is None or remove_result.returncode != 0:
                stderr = (
                    remove_result.stderr.strip()
                    if remove_result is not None and remove_result.stderr
                    else "unknown error"
                )
                click.echo(
                    f"   ❌ Could not remove stale {server_name} before re-register: {stderr}",
                    err=True,
                )
                return False
            # Fall through to the normal install path below to re-add at the expected version.

    # Handle API key requirements
    env_args = []
    secret_env_names = set()  # env var names whose values must be masked in echoes (M1)
    if "api_key_env" in server_info:
        api_key_env = server_info["api_key_env"]
        secret_env_names.add(api_key_env)
        if dry_run:
            api_key = os.getenv(api_key_env)
            if not api_key:
                click.echo(
                    f"[DRY RUN] Would request {api_key_env} during installation; no prompt or key change now."
                )
        else:
            api_key = prompt_for_api_key(
                server_name,
                api_key_env,
                server_info.get("api_key_description", f"API key for {server_name}"),
            )

        if api_key:
            env_args = ["-e", f"{api_key_env}={api_key}"]

    # Inject server-level DEFAULT_PARAMETERS as a repeatable -e pair (M1).
    # Compact JSON (no spaces) keeps the value a single argv token; not a secret,
    # so it is shown in full in echoed commands.
    if "default_parameters" in server_info:
        default_params_json = json.dumps(
            server_info["default_parameters"], separators=(",", ":")
        )
        env_args.extend(["-e", f"DEFAULT_PARAMETERS={default_params_json}"])

    # Build installation command using modern Claude Code API
    # Format: claude mcp add [--transport <transport>] [--scope <scope>] <name> [-e KEY=VALUE]... -- <command>
    # NOTE: <name> must precede `-e` flags. The Claude CLI's `-e` is repeatable per env var
    # and positional binding requires the server name first; placing `-e` before <name>
    # causes the next positional to be parsed as a malformed env spec.

    cmd = ["claude", "mcp", "add", "--transport", transport]

    # Add scope if not default
    if scope != "local":
        cmd.extend(["--scope", scope])

    # Add server name BEFORE env flags (CLI grammar requirement)
    cmd.append(server_name)

    # Add environment variables if any (each as `-e KEY=VALUE`, repeatable)
    if env_args:
        cmd.extend(env_args)

    if transport == "http":
        # `--header` takes several values, so it must come after the URL.
        cmd.append(server_info["url"])
        for header, value in server_info.get("headers", {}).items():
            cmd.extend(["--header", f"{header}: {value}"])
    else:
        # Add separator
        cmd.append("--")

        # Add server command (split into parts)
        cmd.extend(shlex.split(command))

    # Build a display-safe command that masks secret env values (e.g. the API key)
    # while leaving non-secret tokens like DEFAULT_PARAMETERS visible in full (M1).
    def _mask_secret(token: str) -> str:
        if "=" in token:
            key = token.split("=", 1)[0]
            if key in secret_env_names:
                return f"{key}=***"
        return token

    display_cmd = " ".join(_mask_secret(tok) for tok in cmd)

    if dry_run:
        click.echo(f"   [DRY RUN] Would run: {display_cmd}")
        return True

    try:
        click.echo(f"   Running: {display_cmd}")
        result = _run_command(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            click.echo(f"   ✅ Successfully installed: {server_name}")
            if "post_install_message" in server_info:
                click.echo(server_info["post_install_message"])
            return True
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            click.echo(f"   ❌ Failed to install {server_name}: {error_msg}", err=True)
            return False

    except subprocess.TimeoutExpired:
        click.echo(f"   ❌ Timeout installing {server_name}", err=True)
        return False
    except Exception as e:
        click.echo(f"   ❌ Error installing {server_name}: {e}", err=True)
        return False


def list_available_servers():
    """List all available MCP servers."""
    click.echo("📋 Available MCP Servers:\n")

    # Show gateway option first
    click.echo("   ┌─────────────────────────────────────────────────────────────┐")
    click.echo("   │  🚀 AIRIS MCP Gateway (Recommended)                         │")
    gateway_installed = check_mcp_server_installed("airis-mcp-gateway")
    gateway_status = "✅ installed" if gateway_installed else "⬜ not installed"
    click.echo(f"   │     Status: {gateway_status:40} │")
    click.echo("   │     60+ tools, 98% token reduction, Web UI                  │")
    click.echo("   │     Install: superclaude mcp --servers airis-mcp-gateway    │")
    click.echo("   └─────────────────────────────────────────────────────────────┘")
    click.echo()
    click.echo("   Individual Servers (legacy):\n")

    for server_key, server_info in MCP_SERVERS.items():
        name = server_info["name"]
        description = server_info["description"]
        api_key_note = ""

        if "api_key_env" in server_info:
            api_key_note = f" (requires {server_info['api_key_env']})"

        # Check if installed
        is_installed = check_mcp_server_installed(name)
        status = "✅ installed" if is_installed else "⬜ not installed"

        click.echo(f"   {name:25} {status}")
        click.echo(f"      {description}{api_key_note}")
        click.echo()

    click.echo(
        f"Total: {len(MCP_SERVERS)} individual servers + AIRIS Gateway available"
    )


def _show_mcp_install_choices() -> None:
    click.echo("g. AIRIS MCP Gateway (recommended): airis-mcp-gateway; requires Docker")
    for index, (name, info) in enumerate(MCP_SERVERS.items(), 1):
        key_note = f" (requires {info['api_key_env']})" if "api_key_env" in info else ""
        click.echo(f"{index}. {name}: {info['description']}{key_note}")
    click.echo("0. Install all individual servers (except opt-in ones such as litellm)")


def install_mcp_servers(
    selected_servers: Optional[List[str]] = None,
    scope: str = "user",
    dry_run: bool = False,
    use_gateway: Optional[bool] = None,
    *,
    uninstall: bool = False,
    yes: bool = False,
) -> Tuple[bool, str]:
    """Validate the whole selection, then install it or remove only Codebase Memory.

    `yes` controls native removal consent only. It never bypasses API-key or
    global-binary prompts. Dry-run never enters prerequisite/mutation paths.
    """
    if scope not in {"local", "project", "user"}:
        return False, "Invalid MCP scope"
    selected = list(dict.fromkeys(selected_servers or []))
    if not selected and use_gateway is True:
        selected = ["airis-mcp-gateway"]
    if not selected:
        if dry_run:
            click.echo(
                "1. Install MCP servers (default)\n2. Uninstall Codebase Memory MCP\n3. Cancel"
            )
            _show_mcp_install_choices()
            return (
                True,
                "[DRY RUN] Available choices only; select servers explicitly to preview an operation. "
                + _native_lifecycle_notice(),
            )
        if uninstall or yes or not _is_interactive():
            return (
                False,
                "Explicit server selection is required; use --servers codebase-memory-mcp for native lifecycle actions.",
            )
        click.echo(
            "1. Install MCP servers (default)\n2. Uninstall Codebase Memory MCP\n3. Cancel"
        )
        action = click.prompt("Action", default="1", type=click.Choice(["1", "2", "3"]))
        if action == "3":
            return True, "Cancelled; no changes made."
        if action == "2":
            selected, uninstall = [codebase_memory.BINARY_NAME], True
        else:
            _show_mcp_install_choices()
            choice = (
                click.prompt(
                    "Select g for gateway, 0 for all, or comma-separated numbers",
                    default="g",
                )
                .strip()
                .lower()
            )
            if choice == "g":
                selected = ["airis-mcp-gateway"]
            elif choice == "0":
                selected = [
                    name
                    for name, info in MCP_SERVERS.items()
                    if not info.get("opt_in_only")
                ]
            else:
                try:
                    indices = [int(value.strip()) for value in choice.split(",")]
                    names = list(MCP_SERVERS)
                    if not indices or any(
                        index < 1 or index > len(names) for index in indices
                    ):
                        return False, "Invalid selection; no changes made."
                    selected = list(
                        dict.fromkeys(names[index - 1] for index in indices)
                    )
                except ValueError:
                    return False, "Invalid selection; no changes made."
    unknown = [
        name
        for name in selected
        if name != "airis-mcp-gateway" and name not in MCP_SERVERS
    ]
    if unknown:
        return False, "Unknown MCP server selection: " + ", ".join(unknown)
    if uninstall and selected != [codebase_memory.BINARY_NAME]:
        return (
            False,
            "Uninstall accepts only --servers codebase-memory-mcp, not mixed or other servers.",
        )
    if codebase_memory.BINARY_NAME in selected:
        invalid = _native_selection_error(scope)
        if invalid:
            return False, invalid
    if uninstall:
        if not dry_run and not yes and not _is_interactive():
            return (
                False,
                "Noninteractive native removal requires --yes; no changes made.",
            )
        valid, preview = uninstall_codebase_memory_mcp(scope=scope, dry_run=True)
        if dry_run or not valid:
            return valid, preview
        click.echo("Removal preview: " + preview.removeprefix("[DRY RUN] "))
        if not yes and not click.confirm(
            "Proceed with account-wide Codebase Memory removal?", default=False
        ):
            return True, "Removal declined; no changes made."
        return uninstall_codebase_memory_mcp(scope=scope, confirmed=True)

    if not dry_run:
        ready, errors = check_prerequisites(selected)
        if not ready:
            return False, "Prerequisites not met:\n" + "\n".join(errors)
    completed = 0
    failed = []
    for name in selected:
        try:
            if name == "airis-mcp-gateway":
                success = install_airis_gateway(dry_run)
            else:
                success = install_mcp_server(MCP_SERVERS[name], scope, dry_run)
        except (OSError, subprocess.SubprocessError):
            click.echo(
                f"Process error while handling {name}; inspect its installation state before retrying.",
                err=True,
            )
            success = False
        if success:
            completed += 1
        else:
            failed.append(name)
    label = "previewed" if dry_run else "installed"
    if failed:
        return (
            False,
            f"Partially completed: {completed}/{len(selected)} {label}. Failed servers: {', '.join(failed)}",
        )
    return True, f"Successfully {label} {completed} MCP server(s)."
