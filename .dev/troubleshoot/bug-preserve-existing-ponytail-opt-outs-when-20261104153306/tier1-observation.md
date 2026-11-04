# Tier 1 observation

Captured 2026-11-04T15:33:17Z, run=local repro, arm=failing (current branch ironbelly/issue-330-ponytail-pin @ 1a181bd8), command: `timeout 120 uv run python /tmp/t14c-repro/repro.py` (throwaway HOME via tempfile; settings.json = {"enabledPlugins": {"ponytail@ponytail": false}}), stream=stdout:

```text
apply: True
ponytail entries after defaults: {'ponytail@ponytail': False, 'ponytail@ironclaude': True}
install_plugins would want ponytail@ironclaude: True
```

The third line recomputes install_plugins' `wanted` expression (install_user_setup.py:297) on the resulting settings; install_plugins itself was not run (it would call the claude CLI).
