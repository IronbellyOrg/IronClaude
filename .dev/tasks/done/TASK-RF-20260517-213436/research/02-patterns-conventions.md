# Research: Patterns & Conventions — hook-sync-and-matcher-fix
**Topic type:** Patterns & Conventions
**Scope:** Makefile verify-sync idioms, hook script header style, JSON formatting, message conventions
**Status:** Complete
**Date:** 2026-05-17
---

## Section 1: Makefile `verify-sync` section pattern (Makefile:154-247)

The `verify-sync` target follows a highly consistent shape across its three component sections (Skills, Agents, Commands). The pattern is built as a single recipe-line shell pipeline (continued with `\`), where every command ends in `; \` so that bash sees one long compound statement and a single `drift` variable persists across all checks.

### 1.1 Section header echo style

Each subsection begins with a blank-line echo followed by a `=== <Section Name> ===` banner echo. Verbatim (Makefile:189-191, the Agents header — Skills uses identical shape at line 158):

```
	echo ""; \
	echo "=== Agents ==="; \
	for agent in src/superclaude/agents/*.md; do \
```

The `===` delimiters are exactly three `=` on each side, with single spaces around the name. The blank-line echo before the header creates visual separation in output between sections.

### 1.2 Forward-check for-loop shape (src → .claude)

The forward check iterates over the source-of-truth directory and verifies each entry exists in `.claude/`. Verbatim (Makefile:159-175, Skills section):

```
	for skill_dir in src/superclaude/skills/*/; do \
		name=$$(basename "$$skill_dir"); \
		case "$$name" in __*) continue;; esac; \
		if [ ! -d ".claude/skills/$$name" ]; then \
			echo "  ❌ MISSING in .claude/skills/: $$name"; \
			drift=1; \
		else \
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
			if [ -n "$$changes" ]; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				echo "$$changes" | sed 's/^/      /'; \
				drift=1; \
			else \
				echo "  ✅ $$name"; \
			fi; \
		fi; \
	done; \
```

Structural rules observed:
- Glob source path with trailing `/` for directories (`src/superclaude/skills/*/`) or `*.md` for files.
- `name=$$(basename "$$skill_dir");` — capture basename into `$$name`.
- `case "$$name" in __*) continue;; esac;` — skip-pattern using `case` rather than `if`.
- `if [ ! -d ".claude/.../$$name" ];` — file existence check uses `-f`, directory uses `-d`.
- On miss: print `❌ MISSING in <path>: <name>` and set `drift=1;`.
- On hit: run `diff` (file-level for agents/commands via `diff -q`; recursive for skills via `diff -rq` with `--exclude` flags).
- On differ: print `⚠️  DIFFERS: <name>` (two spaces after the emoji), set `drift=1;`.
- On match: print `✅ <name>` (single space after emoji).

### 1.3 Reverse-check for-loop shape (.claude → src)

The reverse check catches entries that exist in `.claude/` but not in `src/`. Verbatim (Makefile:206-214, Agents):

```
	for agent in .claude/agents/*.md; do \
		[ -f "$$agent" ] || continue; \
		name=$$(basename "$$agent"); \
		case "$$name" in README.md) continue;; esac; \
		if [ ! -f "src/superclaude/agents/$$name" ]; then \
			echo "  ❌ MISSING in src/superclaude/agents/: $$name (not distributable!)"; \
			drift=1; \
		fi; \
	done; \
```

Structural rules:
- Begins with `[ -f "$$X" ] || continue;` (or `-d` for dirs) as a guard against empty globs.
- Uses the same `case "$$name" in <skip-pattern>) continue;; esac;` skip-list idiom.
- Reverse-miss message appends `(not distributable!)` to distinguish from forward-miss.
- No "differs" branch — reverse only checks existence (forward already handled content drift).

### 1.4 Case-skip pattern

Skip-lists for special entries use `case` (not `if`) with `;;` separator and `esac` terminator. Examples:
- `case "$$name" in __*) continue;; esac;` (Makefile:161 — skip dunder dirs)
- `case "$$name" in README.md) continue;; esac;` (Makefile:193,209,219,235 — skip README)

### 1.5 Final drift summary

After all sections, a single drift-summary block produces the exit code. Verbatim (Makefile:241-247):

```
	echo ""; \
	if [ "$$drift" -eq 0 ]; then \
		echo "✅ All components in sync."; \
	else \
		echo "❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."; \
		exit 1; \
	fi
```

Note the absence of `; \` on the final `fi` — this terminates the recipe-line shell statement.

### 1.6 `$$` shell escape and continuation indentation

- All shell variables use `$$` (Make-escaped `$`) — e.g. `$$name`, `$$drift`, `$$(basename "$$skill_dir")`.
- Continuation `\` is the last character of each line; the next line is indented with a single TAB (the Make recipe indent) followed by additional space indentation matching the nesting depth (typically tab + tab for the `for` body, tab + tab + tab for `if` bodies).
- Strings holding paths or names are always double-quoted: `"$$skill_dir"`, `".claude/skills/$$name"`.

---

## Section 2: Hook script header convention

### 2.1 `auggie-flag-clear.sh` (lines 1-7, verbatim)

```
#!/usr/bin/env bash
# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
# auggie-first-hook-proposal-v2.1.md §6 — synchronous (no async:true) per spec-panel Wh-8.
# Fail-open per NFR-3.
set -u

[ "${AUGGIE_FIRST_DISABLE:-0}" = "1" ] && exit 0
```

### 2.2 `freshness-pre-edit.sh` (lines 1-6, verbatim)

```
#!/usr/bin/env bash
# PreToolUse(Edit-class) freshness gate per design §3.3.
# Decision: allow (exit 0) | block (stderr + exit 2). NEVER exit 1 (NFR-10).
# Fail-open per NFR-3: state missing/corrupt → log to stderr, exit 0.

set -u
```

### 2.3 Header convention observed

| Element | Convention |
|---|---|
| Shebang | `#!/usr/bin/env bash` (portable form, NOT `#!/bin/bash`) |
| Line 2 | Hook-event tag + one-line purpose. Format: `# <HookEvent>[(<matcher-class>)]: <purpose>.` Example: `# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.` |
| Line 3 | Spec reference + design rationale. Format: `# <spec-file>.md §<section> — <decision> per <reviewer/tag>.` |
| Line 4 | NFR/contract reference. Format: `# Fail-open per NFR-3.` or `# Decision: ... NEVER exit 1 (NFR-10).` |
| Blank line | Optional — `freshness-pre-edit.sh` has one before `set -u`; `auggie-flag-clear.sh` omits it. |
| Strict mode | `set -u` (NOT `set -euo pipefail`). The hooks deliberately use only `set -u` to preserve fail-open behavior — `set -e` would propagate sub-command failures and break the NFR-3 contract. |
| Disable-env pattern | `[ "${AUGGIE_FIRST_DISABLE:-0}" = "1" ] && exit 0` — single-line guard immediately after `set -u`, using `${VAR:-0}` default and short-circuit `&&`. Allows runtime disable without code change. |

---

## Section 3: JSON style for `hooks.json` (lines 50-70)

Verbatim excerpt (hooks.json:50-68):

```
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/freshness-post-read.sh",
            "timeout": 1,
            "async": true
          }
        ]
      },
      {
        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auggie-flag-clear.sh",
            "timeout": 1
          }
        ]
      }
```

### 3.1 Indentation

2-space indentation throughout. Nesting at line 53 (`"type": "command"`) sits at 12 spaces = 6 levels deep, confirming 2-space-per-level.

### 3.2 Object key ordering

Within each hook entry, keys appear in a stable order:
1. `"matcher"` (when present at the matcher-group level)
2. `"hooks"` (array of hook commands)

Within each hook command object:
1. `"type"` (always `"command"`)
2. `"command"` (the script path)
3. `"timeout"` (integer seconds)
4. `"async"` (optional boolean, last when present)

### 3.3 Matcher string format

Matchers are regex strings. Examples from `hooks.json`:
- `"matcher": "*"` (hooks.json:14 — wildcard, matches any tool)
- `"matcher": "Read"` (hooks.json:49 — exact tool name)
- `"matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol"` (hooks.json:37 — pipe-separated alternation, no spaces around `|`)
- `"matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"` (hooks.json:60 — regex `.*` suffix wildcards, pipe alternation)

Conventions:
- Pipe alternation uses `|` with NO surrounding spaces.
- Wildcard suffix uses regex `.*` (not shell glob `*`).
- Double-underscore namespaces (`mcp__<server>__<tool>`) are preserved literally.

### 3.4 Command path style

Commands use `~/.claude/hooks/<script>.sh` (tilde-prefixed home, not absolute `/home/...` or `$HOME/...`).

---

## Section 4: Error/info message format in verify-sync

The triadic message format is verified by the Skills section. Verbatim (Makefile:162-173):

```
		if [ ! -d ".claude/skills/$$name" ]; then \
			echo "  ❌ MISSING in .claude/skills/: $$name"; \
			drift=1; \
		else \
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
			if [ -n "$$changes" ]; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				echo "$$changes" | sed 's/^/      /'; \
				drift=1; \
			else \
				echo "  ✅ $$name"; \
			fi; \
		fi; \
```

Confirmed format rules:
- Leading indent: two spaces before the emoji (`"  ❌ ..."`).
- `❌ MISSING in <path>/: <name>` — path includes the trailing slash and colon; name follows after a single space.
- `⚠️  DIFFERS: <name>` — TWO spaces after the warning emoji (visible in raw source as `⚠️  DIFFERS`). This is because the warning glyph is narrower than the cross/check emojis in terminal rendering.
- `✅ <name>` — single space after the check emoji, no prefix word.
- Reverse-miss adds `(not distributable!)` suffix (Makefile:211): `echo "  ❌ MISSING in src/superclaude/agents/: $$name (not distributable!)";`.

---

## Section 5: Make-shell idioms

### 5.1 Grep results

`grep -n 'jq' Makefile` → **no matches**. The Makefile does NOT use `jq` anywhere.

`grep -nE 'comm |grep -oE|sed -E|xargs|<\(' Makefile` → only two matches, both for `xargs`:

```
322:		echo "  ✅ [Check 8]: $$(dirname $$skill_md | xargs basename) frontmatter complete"; \
332:			echo "  ❌ ERROR [Check 9]: $$(dirname $$skill_md | xargs basename) SKILL.md name field '$$name_field' does not end in -protocol"; \
```

Both uses are the idiom `dirname X | xargs basename` to extract the parent directory's name.

### 5.2 Findings

The existing Makefile does NOT use:
- `comm` (no set-difference comparisons)
- `<(...)` process substitution (incompatible with portable `/bin/sh`; Make recipes run under `sh -c` by default)
- `grep -oE` (no regex extraction)
- `sed -E` (uses BSD-compatible `sed 's/...'` instead — see Makefile:169, 328)
- `jq` (no JSON parsing in any target)

It DOES use:
- Plain `diff -rq` / `diff -q` for content comparison
- `basename`, `dirname`, `xargs basename` pipelines
- `sed 's/^/.../'` (basic mode, no `-E`) for output indentation
- `grep -q` for boolean presence checks (Makefile:317, 329)
- `case ... in ... ) continue;; esac` for skip-lists

### 5.3 Implication for the new sections

Any new `verify-sync` subsection for hooks/scripts MUST stick to these idioms. Specifically, the builder should:
- AVOID `jq` (even though `hooks.json` is JSON) unless the spec explicitly requires JSON parsing; if needed, gate behind `command -v jq` to preserve portability.
- AVOID `<(...)` process substitution and `comm` (use `diff` or plain glob loops).
- AVOID `sed -E` / `grep -oE` — use basic regex if extraction is required.
- USE the same `for X in <glob>; do ... done; \` loop shape with `case`-based skip-lists, `[ -f|-d ]` guards, and the `❌ MISSING` / `⚠️ DIFFERS` / `✅` message triad.

---

## Section 6: Comment style on hook scripts

Hook scripts use **single-line `#` comments only** — no block-comment style (no `: <<'EOF'` heredocs, no banner boxes). Each comment line is one sentence. Spec references appear inline within the header (lines 2-4) and at decision points later in the script body. The reference format is:

- File-path-style: `auggie-first-hook-proposal-v2.1.md §6` (filename + section sign + section number)
- Inline NFR: `per NFR-3`, `per NFR-10`, `per DQ-3` (Makefile:14 of `freshness-pre-edit.sh` cites `FRESH_HORIZON=1800   # 30 min per DQ-3`)
- Decision rationale: `per spec-panel Wh-8` (reviewer-tag style for adversarial-review decisions)

No JSDoc-style `/** */` blocks (this is shell, not JS). No `# ---` separators or `# === SECTION ===` banners inside scripts — banners are reserved for `verify-sync` output, not hook source.

---

## Summary

For the `hook-sync-and-matcher-fix` release, any new `verify-sync` subsection that checks hook scripts (`src/superclaude/hooks/scripts/` ↔ installed location) or `hooks.json` matcher consistency MUST mirror the established Skills/Agents/Commands triad: a `=== <Section> ===` banner, a forward `for` loop with `case`-skip and `[ -f|-d ]` guards emitting the `❌ MISSING` / `⚠️ DIFFERS` / `✅` message triad, a reverse `for` loop with `(not distributable!)` suffix, and a single shared `$$drift` variable propagated to the final summary block. Any new hook script created as part of the release MUST follow the established 4-line header (shebang, hook-event + purpose, spec reference + decision rationale, NFR/fail-open contract), `set -u` strict mode (NOT `set -euo pipefail`), and a `${X_DISABLE:-0}` runtime escape hatch.

Most important style rules:

- **`$$` Make-escape, double-quoted vars, TAB+space continuation indent, `; \` line terminators** — every shell variable in a Makefile recipe is `$$VAR`, every path is `"$$VAR"`, and every continuation line ends in `; \`.
- **Message triad: `  ❌ MISSING in <path>/: <name>` / `  ⚠️  DIFFERS: <name>` (two spaces after ⚠️) / `  ✅ <name>`** — exactly two leading spaces, exact emoji + spacing as shown, reverse-miss appends `(not distributable!)`.
- **Hook header: 4 lines (shebang → event+purpose → spec §section + decision → NFR/fail-open), `set -u` only, then runtime-disable guard** — never `set -euo pipefail`, never `#!/bin/bash`, always cite the proposal/design doc and the relevant NFR.
- **JSON style: 2-space indent, key order `matcher` → `hooks` then `type` → `command` → `timeout` → `async`, regex matchers with `|` alternation (no spaces) and `.*` wildcards, `~/.claude/hooks/<name>.sh` command paths.**
- **Portable shell idioms only: no `jq`, no `<(...)`, no `sed -E` / `grep -oE`, no `comm`. Stick to `diff -q` / `diff -rq`, `basename`/`dirname`/`xargs basename`, `grep -q`, basic `sed 's/.../.../'`, and `case ... esac` for skip-lists.**
