# D-0014 — install_hooks wired into superclaude install orchestrator

## Task: T04.02 (STANDARD)

`src/superclaude/cli/main.py` updated to import `install_hooks` and call it after `install_all_skills` in the `superclaude install` flow.

## Diff (logical, abridged)

```diff
@@ src/superclaude/cli/main.py @@
     from .install_core import (
         install_core_files, ...
     )
+    from .install_hooks import install_hooks
     from .install_skill import list_available_skills
     ...

     # Step 4: Install skills
     ...
     skill_success, skill_message = install_all_skills(force=force)
     click.echo(skill_message)
+    click.echo()
+
+    # Step 5: Install hooks (scripts + additive settings.json merge)
+    click.echo("📦 Installing hooks to ~/.claude/hooks/...")
+    click.echo()
+
+    hooks_success, hooks_message = install_hooks(force=force)
+    click.echo(hooks_message)

-    if not core_success or not cmd_success or not agent_success or not skill_success:
+    if (
+        not core_success
+        or not cmd_success
+        or not agent_success
+        or not skill_success
+        or not hooks_success
+    ):
         sys.exit(1)
```

## Validation

Import smoke (no runtime side effects):
```
$ uv run python -c "from superclaude.cli.main import main; print('main imports OK')"
main imports OK
$ uv run python -c "from superclaude.cli.install_hooks import install_hooks; print('OK')"
OK
```

Existing pytest suite unaffected (the new `install_hooks` test file passes;
no other CLI tests reference the install flow directly).

## Acceptance

- `install_hooks` added to imports and call chain.
- Output messaging follows existing convention (`📦 Installing …` prefix).
- `hooks_success` joins the final `sys.exit(1)` short-circuit.
- Existing test suite still passes (no regressions).
