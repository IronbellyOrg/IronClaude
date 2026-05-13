# D-0015 — Makefile sync-dev hook entries

## Task: T04.03 (STANDARD)

`make sync-dev` now also copies hook scripts (`src/superclaude/hooks/scripts/*.sh` + the legacy `src/superclaude/scripts/session-init.sh`) into `.claude/hooks/` with mode 0755.

## Diff

```diff
@@ Makefile sync-dev target @@
   @mkdir -p .claude/commands/sc
   @for cmd in src/superclaude/commands/*.md; do ... done
+  @mkdir -p .claude/hooks
+  @for hook in src/superclaude/hooks/scripts/*.sh; do \
+    [ -f "$$hook" ] || continue; \
+    name=$$(basename "$$hook"); \
+    cp "$$hook" ".claude/hooks/$$name"; \
+    chmod +x ".claude/hooks/$$name"; \
+  done
+  @if [ -f src/superclaude/scripts/session-init.sh ]; then \
+    cp src/superclaude/scripts/session-init.sh .claude/hooks/session-init.sh; \
+    chmod +x .claude/hooks/session-init.sh; \
+  fi
   @echo "✅ Sync complete."
   @echo "   Skills:   ..."
   @echo "   Agents:   ..."
   @echo "   Commands: ..."
+  @echo "   Hooks:    $$(ls .claude/hooks/*.sh 2>/dev/null | wc -l | tr -d ' ') files"
```

## Validation

```
$ make sync-dev
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   19 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    8 files

$ ls -la .claude/hooks/
total 48
-rwxr-xr-x  freshness-file-changed.sh
-rwxr-xr-x  freshness-post-read.sh
-rwxr-xr-x  freshness-pre-edit.sh
-rwxr-xr-x  freshness-session-start.sh
-rwxr-xr-x  freshness-subagent-start.sh
-rwxr-xr-x  freshness-subagent-stop.sh
-rwxr-xr-x  freshness-user-prompt.sh
-rwxr-xr-x  session-init.sh

$ for h in .claude/hooks/freshness-*.sh; do
    diff "$h" "src/superclaude/hooks/scripts/$(basename $h)"
  done
(empty — all 7 identical)
```

## Acceptance

- 8 hook scripts present in `.claude/hooks/`, all mode 0755.
- Bit-identical to `src/superclaude/hooks/scripts/` source.
- `make sync-dev` output line includes the hooks count.
