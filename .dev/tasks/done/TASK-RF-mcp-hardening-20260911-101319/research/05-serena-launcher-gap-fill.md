# Serena launcher gap fill

**Status:** Complete

Verified launch command:

```sh
uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false
```

`serena-agent==1.7.0` provides the `serena` console script. `start-mcp-server`, `--context claude-code`, `--project-from-cwd`, `--enable-web-dashboard false`, and `--enable-gui-log-window false` are valid at Serena v1.7.0. Keep `--enable-web-dashboard false`, which disables the service, rather than only suppressing its browser opening.

**Confidence:** 98%.

Sources:
- https://pypi.org/project/serena-agent/1.7.0/
- https://raw.githubusercontent.com/oraios/serena/v1.7.0/pyproject.toml
- https://raw.githubusercontent.com/oraios/serena/v1.7.0/src/serena/cli.py
- https://oraios.github.io/serena/02-usage/030_clients.html
- https://docs.astral.sh/uv/guides/tools/
