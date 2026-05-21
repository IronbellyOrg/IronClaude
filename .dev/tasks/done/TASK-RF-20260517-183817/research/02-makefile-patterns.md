# Research: Makefile verify-sync Patterns
**Topic type:** Patterns & Conventions
**Scope:** /config/workspace/IronClaude/Makefile lines 154-247 (verify-sync target)
**Status:** Complete
**Date:** 2026-05-17

---

## 1. Target structure overview (Makefile:154-247)

```
verify-sync:                                       # line 154
    @echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."   # line 155
    @drift=0; \                                    # line 156 (single recipe begins)
    echo ""; \                                     # line 157
    echo "=== Skills ==="; \                       # line 158
    <forward loop>                                 # lines 159-175
    <reverse loop>                                 # lines 176-188
    echo ""; \                                     # line 189
    echo "=== Agents ==="; \                       # line 190
    <forward loop>                                 # lines 191-205
    <reverse loop>                                 # lines 206-214
    echo ""; \                                     # line 215
    echo "=== Commands ==="; \                     # line 216
    <forward loop>                                 # lines 217-231
    <reverse loop>                                 # lines 232-240
    echo ""; \                                     # line 241
    <final drift check>                            # lines 242-247
```

The entire target is **one single shell recipe** (one `@drift=0; \` opening at line 156, every subsequent line ending with `\` until line 247's `fi` which has no trailing `\`). All variables (`$$drift`, `$$name`, etc.) persist across the whole recipe because it's one shell invocation.

---

## 2. Pattern element catalog (with evidence)

### 2.1 Section header pattern — Makefile:157-158, 189-190, 215-216, 241

```make
echo ""; \
echo "=== <Name> ==="; \
```

- A blank `echo ""` always precedes the `=== <Name> ===` banner.
- Exactly three equals signs on each side, single space inside.
- Final block (line 241) also starts with `echo "";` before the drift summary.

### 2.2 Drift flag accumulator — Makefile:156, 164, 170, 186, 196, 200, 212, 222, 226, 238, 242-246

- **Init**: `@drift=0; \` at line 156 — the `@` silences only this first line; subsequent lines in the same recipe share the shell.
- **Set to 1**: every failure path uses `drift=1; \` (no quoting, integer comparison later).
- **Final check** at lines 242-246:
  ```make
  if [ "$$drift" -eq 0 ]; then \
      echo "✅ All components in sync."; \
  else \
      echo "❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."; \
      exit 1; \
  fi
  ```
  Note: `-eq 0` (integer compare), `$$drift` (double-`$` for Make-to-shell escape), and `exit 1` is the last statement → no trailing `\`.

### 2.3 Forward check loop shape — Makefile:159-175 (Skills), 191-205 (Agents), 217-231 (Commands)

**Skills variant (directory-based)**, lines 159-175:
```make
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
Note: skills loop relies on the `*/` trailing slash for directory glob; no `[ -f ... ] || continue` because dir glob is well-behaved.

**Agents/Commands variant (file-based)**, lines 191-205:
```make
for agent in src/superclaude/agents/*.md; do \
    name=$$(basename "$$agent"); \
    case "$$name" in README.md) continue;; esac; \
    if [ ! -f ".claude/agents/$$name" ]; then \
        echo "  ❌ MISSING in .claude/agents/: $$name"; \
        drift=1; \
    else \
        if ! diff -q "$$agent" ".claude/agents/$$name" > /dev/null 2>&1; then \
            echo "  ⚠️  DIFFERS: $$name"; \
            drift=1; \
        else \
            echo "  ✅ $$name"; \
        fi; \
    fi; \
done; \
```
Note: forward agents/commands loop does **not** include `[ -f "$$f" ] || continue` — only the reverse loop does. This is because the spec assumes `src/` always has at least one file; if the glob fails it would fall through to the missing branch.

### 2.4 Reverse check loop shape — Makefile:176-188 (Skills), 206-214 (Agents), 232-240 (Commands)

**Agents reverse**, lines 206-214:
```make
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
**Glob-safety guard**: `[ -f "$$agent" ] || continue;` (line 207) — present on every **reverse** loop because `.claude/` may be missing or empty, causing the glob to expand literally. Forward loops omit it.

**Skills reverse**, lines 176-188 — has extra check for "not actually a skill":
```make
for skill_dir in .claude/skills/*/; do \
    [ -d "$$skill_dir" ] || continue; \
    name=$$(basename "$$skill_dir"); \
    case "$$name" in __*) continue;; esac; \
    if [ ! -d "src/superclaude/skills/$$name" ]; then \
        if [ ! -f "$$skill_dir/SKILL.md" ] && [ ! -f "$$skill_dir/skill.md" ]; then \
            echo "  ❌ $$name has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/$$name/."; \
        else \
            echo "  ❌ MISSING in src/superclaude/skills/: $$name (not distributable!)"; \
        fi; \
        drift=1; \
    fi; \
done; \
```
This nested-`if` "extra files in .claude/" pattern is **unique to the skills reverse loop**. Agents/Commands reverse loops have only the single-arm "MISSING in src/" check.

### 2.5 `diff` invocation variants

| Section | Invocation | Why |
|---|---|---|
| Skills (line 166) | `diff -rq --exclude='__init__.py' --exclude='__pycache__'` | Skills are directories — `-r` recursive; excludes Python build cruft that may live in source but not in dev copy |
| Agents (line 198) | `diff -q "$$agent" ".claude/agents/$$name" > /dev/null 2>&1` | Agents are single files; just need exit-code semantics |
| Commands (line 224) | `diff -q "$$cmd" ".claude/commands/sc/$$name" > /dev/null 2>&1` | Same as agents — single-file compare |

**For hooks (which are single `.sh` files)**: the agents/commands pattern (`diff -q ... > /dev/null 2>&1`) is the correct match.

### 2.6 Skip patterns (`case "$$name" in ... esac`)

| Section | Skip pattern | Lines |
|---|---|---|
| Skills | `__*) continue;;` | 161, 179 |
| Agents | `README.md) continue;;` | 193, 209 |
| Commands | `README.md) continue;;` | 219, 235 |

Note: The `sync-dev` recipe (Makefile:133) skips `README.md|__init__.py` for commands, but `verify-sync` only skips `README.md`. The asymmetry is benign because `__init__.py` does not exist in commands/.

### 2.7 Status symbol conventions

- `❌` (red cross) — MISSING file or directory, always increments `drift=1`. Also used for "not distributable" (reverse) and "extra files / no SKILL.md" (skills reverse).
- `⚠️` (warning) — DIFFERS (content mismatch detected by `diff -q`), increments `drift=1`.
- `✅` (green check) — file/dir in sync.
- Note: `⚠️` is only emitted for the DIFFERS path; MISSING uses `❌`.

### 2.8 Per-file output formatting

- **Two-space indent** for every per-file line: `echo "  ✅ $$name"`, `echo "  ❌ MISSING ..."`, `echo "  ⚠️  DIFFERS: ..."`.
- Note: `⚠️` line uses `"  ⚠️  DIFFERS"` (2-space indent + emoji + **two** spaces before DIFFERS — see Makefile:168, 199, 225). The double-space after `⚠️` compensates for visual width of the emoji vs `❌`/`✅`.
- Skill-DIFFERS detail block uses `sed 's/^/      /'` (six spaces) to nest the file-level changes under the `⚠️  DIFFERS:` line (Makefile:169).

### 2.9 Shell continuation & statement separators

- Every line within the recipe ends with `; \` (semicolon then backslash) except the final `fi` at line 247.
- Block-control words (`if`, `then`, `else`, `fi`, `do`, `done`, `for`, `case`, `esac`) also need `; \` after them because they're each on their own physical line.
- Variable expansion uses `$$name` (double-`$`) so Make passes `$name` through to the shell.

### 2.10 Final drift summary block — Makefile:241-247

```make
echo ""; \
if [ "$$drift" -eq 0 ]; then \
    echo "✅ All components in sync."; \
else \
    echo "❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."; \
    exit 1; \
fi
```
Note: this is at the **outermost level** of the recipe. New sections **must be inserted BEFORE line 241** (the blank-echo before the drift check) so the drift accumulator they update is still in scope before the comparison.

---

## 3. Tools currently used vs new sections will need

| Tool | Current use in verify-sync | New section need |
|---|---|---|
| `diff -q` | Agents/Commands forward (lines 198, 224) | Hooks forward (single-file `.sh`) |
| `diff -rq --exclude=...` | Skills forward (line 166) | — |
| `basename` | All forward & reverse loops | Hooks forward & reverse |
| `case ... esac` | Skip patterns (5 occurrences) | `session-init.sh` skip in Hooks reverse |
| `sed` | Skill-DIFFERS detail (line 169) | — |
| `jq` | **NOT currently used** | `=== Hooks Cross-Consistency ===` (per release-spec §5.1) |
| `comm` | **NOT currently used** | `=== Installer Registration ===` (per release-spec §3.2, hook-sync-coverage-spec §4.2) |
| `xargs` | **NOT currently used** | `=== Installer Registration ===` (`xargs -n1 basename`) |
| `sort` / `sort -u` | **NOT currently used** | Both `=== Installer Registration ===` and `=== Hooks Cross-Consistency ===` |
| `uv run` | **NOT currently used in verify-sync** | `=== Installer Registration ===` (`uv run python -c ...`) |
| `grep -oE` | **NOT currently used** | `=== Hooks Cross-Consistency ===` |

**Implication**: The three new sections substantially widen the toolset used inside verify-sync. The existing sections are pure POSIX-shell + `diff`; the new sections add `jq`, `comm`, `xargs`, `sort`, `uv run`, `grep -oE`. The `hook-sync-coverage-spec.md:118` already acknowledges the `uv run` PATH requirement as acceptable.

---

## 4. Cross-check: release spec snippets vs existing patterns

### 4.1 `=== Hooks ===` forward (release-spec §3.1 + hook-sync-coverage-spec §4.1)

**Spec snippet (hook-sync-coverage-spec.md:51-68):**
```make
echo ""; \
echo "=== Hooks ==="; \
for hook in src/superclaude/hooks/scripts/*.sh; do \
    [ -f "$$hook" ] || continue; \
    name=$$(basename "$$hook"); \
    if [ ! -f ".claude/hooks/$$name" ]; then \
        echo "  ❌ MISSING in .claude/hooks/: $$name (run 'make sync-dev')"; \
        drift=1; \
    else \
        if ! diff -q "$$hook" ".claude/hooks/$$name" > /dev/null 2>&1; then \
            echo "  ⚠️  DIFFERS: $$name"; \
            drift=1; \
        else \
            echo "  ✅ $$name"; \
        fi; \
    fi; \
done; \
```

**Divergences from existing pattern:**
- **D1**: Spec includes `[ -f "$$hook" ] || continue;` in the **forward** loop. Existing agents/commands forward loops at lines 191 and 217 do **NOT** have this guard. Existing reverse loops do. **Recommendation:** Keep the guard in the hooks forward loop — `src/superclaude/hooks/scripts/` could theoretically be empty during early development, and the guard is cheap. This is a minor pattern improvement.
- **D2**: Spec MISSING message includes inline help `(run 'make sync-dev')`. Existing agents/commands say just `MISSING in .claude/agents/: $$name` (no parenthetical). **Recommendation:** Either match existing terse style OR keep the help text — the help is genuinely useful here. Mild divergence either way; preference is to keep the help text since it's the actionable fix.
- **D3**: Spec omits any `case "$$name" in ... esac` skip pattern in the forward loop. Existing patterns all have one (`__*`, `README.md`). For hooks, no current `src/hooks/scripts/*.sh` filename needs skipping. **Recommendation:** Match the existing style by adding an empty/placeholder case OR omit. The cleanest match is to omit it from forward (no current need); reverse will need it for `session-init.sh`.

### 4.2 `=== Hooks ===` reverse (hook-sync-coverage-spec §4.1)

**Spec snippet (hook-sync-coverage-spec.md:72-82):**
```make
for hook in .claude/hooks/*.sh; do \
    [ -f "$$hook" ] || continue; \
    name=$$(basename "$$hook"); \
    case "$$name" in session-init.sh) continue;; esac; \
    if [ ! -f "src/superclaude/hooks/scripts/$$name" ]; then \
        echo "  ❌ MISSING in src/superclaude/hooks/scripts/: $$name (not distributable!)"; \
        drift=1; \
    fi; \
done; \
```

**Divergences from existing pattern:** None significant. This matches the agents/commands reverse pattern verbatim (`[ -f ... ] || continue;`, `basename`, `case ... esac` skip, single-arm MISSING check, `(not distributable!)` parenthetical).

### 4.3 `=== Installer Registration ===` (hook-sync-coverage-spec §4.2)

**Spec snippet (hook-sync-coverage-spec.md:92-114):**
```make
echo ""; \
echo "=== Installer Registration ==="; \
src_hooks=$$(ls src/superclaude/hooks/scripts/*.sh 2>/dev/null | xargs -n1 basename | sort); \
registered=$$(uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print('\n'.join(sorted(_FRESHNESS_SCRIPTS)))" 2>/dev/null); \
missing_from_list=$$(comm -23 <(echo "$$src_hooks") <(echo "$$registered")); \
extra_in_list=$$(comm -13 <(echo "$$src_hooks") <(echo "$$registered")); \
if [ -n "$$missing_from_list" ]; then \
    echo "$$missing_from_list" | while read name; do \
        echo "  ❌ MISSING from _FRESHNESS_SCRIPTS: $$name (end-user 'superclaude install' will skip it)"; \
    done; \
    drift=1; \
fi; \
if [ -n "$$extra_in_list" ]; then \
    echo "$$extra_in_list" | while read name; do \
        echo "  ❌ STALE in _FRESHNESS_SCRIPTS: $$name (listed for install but missing from src/)"; \
    done; \
    drift=1; \
fi; \
if [ -z "$$missing_from_list" ] && [ -z "$$extra_in_list" ]; then \
    echo "  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh"; \
fi; \
```

**Divergences from existing pattern:**
- **D4**: Uses **bash process substitution** `<(echo "...")` for the `comm` arguments. This is **bash-only syntax**, not POSIX. Existing sections are POSIX-shell-compatible. Make defaults to `/bin/sh` as `SHELL` — if `/bin/sh` is `dash` (Debian/Ubuntu default), `<(...)` will **fail**. **Recommendation (CRITICAL):** Either:
  - (a) Add `SHELL := /bin/bash` at the top of the Makefile (or this target), OR
  - (b) Rewrite without process substitution using temp files or piped `diff <(echo ...) <(echo ...)` → use intermediate variables and `printf`.
  - Quick fix: substitute the two `<(echo "$$x")` with `<(printf '%s\n' "$$x")` and ensure bash. Without addressing, this section may silently fail under dash with empty `comm` output → false-clean.
- **D5**: Uses `while read name; do ... done` for output formatting. Reasonable; matches the per-file-line indent convention with `  ❌` prefix.
- **D6**: Status symbol convention: uses `❌` for both MISSING and STALE. Existing pattern uses `❌` only for outright missing/wrong; `⚠️` for differs. Since "listed for install but missing from src/" is a different defect class than "missing from registration", calling both `❌` is defensible — they're both hard failures, not soft divergences. **Recommendation:** Acceptable; spec choice stands.
- **D7**: Single `✅` line for the whole section ("matches src/superclaude/hooks/scripts/*.sh") rather than per-file. Existing forward loops emit one `✅` per file. **Recommendation:** Spec choice is more concise for a set-membership check; defensible. Alternatively, the builder could emit per-hook `✅` to match other sections — slightly more verbose output but stylistically consistent. Lean toward spec's terse style here because the check is set-level not file-level.

### 4.4 `=== Hooks Cross-Consistency ===` (release-spec §5.1)

**Spec snippet (release-spec.md:193-213):**
```make
echo ""; \
echo "=== Hooks Cross-Consistency ==="; \
matcher_prefixes=$$(jq -r '.hooks.PostToolUse[].matcher // empty' \
    src/superclaude/hooks/hooks.json 2>/dev/null \
    | grep -oE 'mcp__[a-z_-]+(\.\*|_\.\*|__\.\*)?' \
    | grep -i 'auggie' \
    | sed -E 's/\.\*$$//' | sort -u); \
case_prefixes=$$(grep -oE 'mcp__[a-z_-]+(_\*|__\*|\*)' \
    src/superclaude/hooks/scripts/auggie-flag-clear.sh \
    | grep -i 'auggie' \
    | sed -E 's/\*$$//' | sort -u); \
if [ "$$matcher_prefixes" = "$$case_prefixes" ]; then \
    echo "  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes"; \
else \
    echo "  ❌ DRIFT between hooks.json:60 matcher and auggie-flag-clear.sh case body"; \
    echo "      hooks.json prefixes: $$matcher_prefixes"; \
    echo "      auggie-flag-clear.sh prefixes: $$case_prefixes"; \
    drift=1; \
fi; \
```

**Divergences from existing pattern:**
- **D8**: Uses `jq` — new dependency for verify-sync. If `jq` is missing, the `2>/dev/null` swallows the error and `$$matcher_prefixes` becomes empty → comparison fails loudly with empty-vs-populated mismatch → drift=1. That's loud-on-failure, acceptable.
- **D9**: Detail-output indent uses **six spaces** (`echo "      hooks.json prefixes: ..."`). This matches the skill-DIFFERS sub-line indent at Makefile:169 (`sed 's/^/      /'`). Good consistency.
- **D10**: `sed -E 's/\.\*$$//'` — the `$$` here is escaping `$` for Make→shell, but within the sed expression `$` is an anchor. So the shell sees `sed -E 's/\.\*$//'` which means "strip trailing `.*`". Correct.
- **D11**: Section only emits ONE line (either `✅` or `❌` + 2 detail lines), no per-file iteration. This is a single set-equality check; the format is reasonable.

---

## 5. Recommended verbatim paste-ready blocks

These are aligned with the existing verify-sync style as closely as possible. **Insert all three sections BEFORE line 241** (`echo ""; \` that precedes the final drift check).

NOTE: each line in the blocks below must start with a single TAB character when pasted into the Makefile (Make requires tab-indented recipes). The blocks are shown with leading tab represented as a tab character.

### 5.1 `=== Hooks ===` (forward + reverse)

```make
	echo ""; \
	echo "=== Hooks ==="; \
	for hook in src/superclaude/hooks/scripts/*.sh; do \
		[ -f "$$hook" ] || continue; \
		name=$$(basename "$$hook"); \
		if [ ! -f ".claude/hooks/$$name" ]; then \
			echo "  ❌ MISSING in .claude/hooks/: $$name (run 'make sync-dev')"; \
			drift=1; \
		else \
			if ! diff -q "$$hook" ".claude/hooks/$$name" > /dev/null 2>&1; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				drift=1; \
			else \
				echo "  ✅ $$name"; \
			fi; \
		fi; \
	done; \
	for hook in .claude/hooks/*.sh; do \
		[ -f "$$hook" ] || continue; \
		name=$$(basename "$$hook"); \
		case "$$name" in session-init.sh) continue;; esac; \
		if [ ! -f "src/superclaude/hooks/scripts/$$name" ]; then \
			echo "  ❌ MISSING in src/superclaude/hooks/scripts/: $$name (not distributable!)"; \
			drift=1; \
		fi; \
	done; \
```

**Notes for builder:**
- Tab-indented (matches Makefile recipe convention).
- Forward loop includes `[ -f "$$hook" ] || continue;` (D1 above — minor improvement over existing forward pattern; safe).
- Reverse loop case-skips `session-init.sh` per hook-sync-coverage-spec §4.1 (lives in `src/superclaude/scripts/` not `src/superclaude/hooks/scripts/`).
- MISSING message in forward includes `(run 'make sync-dev')` helper text. If builder wants strict style match with existing agents/commands, drop the parenthetical; otherwise keep it.

### 5.2 `=== Installer Registration ===`

```make
	echo ""; \
	echo "=== Installer Registration ==="; \
	src_hooks=$$(ls src/superclaude/hooks/scripts/*.sh 2>/dev/null | xargs -n1 basename | sort); \
	registered=$$(uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print('\n'.join(sorted(_FRESHNESS_SCRIPTS)))" 2>/dev/null); \
	missing_from_list=$$(comm -23 <(printf '%s\n' "$$src_hooks") <(printf '%s\n' "$$registered")); \
	extra_in_list=$$(comm -13 <(printf '%s\n' "$$src_hooks") <(printf '%s\n' "$$registered")); \
	if [ -n "$$missing_from_list" ]; then \
		echo "$$missing_from_list" | while read name; do \
			echo "  ❌ MISSING from _FRESHNESS_SCRIPTS: $$name (end-user 'superclaude install' will skip it)"; \
		done; \
		drift=1; \
	fi; \
	if [ -n "$$extra_in_list" ]; then \
		echo "$$extra_in_list" | while read name; do \
			echo "  ❌ STALE in _FRESHNESS_SCRIPTS: $$name (listed for install but missing from src/)"; \
		done; \
		drift=1; \
	fi; \
	if [ -z "$$missing_from_list" ] && [ -z "$$extra_in_list" ]; then \
		echo "  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh"; \
	fi; \
```

**CRITICAL BUILDER NOTE — bash process substitution (D4):**

This section uses `<(...)` process substitution, which is **bash-only**. For this to work, the Makefile must use bash as its shell. The current Makefile head should be checked (researcher-1 covers surface verification). If `SHELL := /bin/bash` isn't already set, the builder MUST add this line near the top of the Makefile (before the first target):

```make
SHELL := /bin/bash
```

Alternative (avoids the shell dependency): use temp files —
```make
echo "$$src_hooks" > /tmp/.verify-sync-src-hooks; \
echo "$$registered" > /tmp/.verify-sync-registered; \
missing_from_list=$$(comm -23 /tmp/.verify-sync-src-hooks /tmp/.verify-sync-registered); \
extra_in_list=$$(comm -13 /tmp/.verify-sync-src-hooks /tmp/.verify-sync-registered); \
rm -f /tmp/.verify-sync-src-hooks /tmp/.verify-sync-registered; \
```
The temp-file variant is POSIX-clean. Builder should prefer adding `SHELL := /bin/bash` (matches modern Makefile conventions) unless project policy prohibits.

Also changed `<(echo "$$x")` to `<(printf '%s\n' "$$x")` for robustness on `-e`/`-n` filenames.

### 5.3 `=== Hooks Cross-Consistency ===`

```make
	echo ""; \
	echo "=== Hooks Cross-Consistency ==="; \
	matcher_prefixes=$$(jq -r '.hooks.PostToolUse[].matcher // empty' \
		src/superclaude/hooks/hooks.json 2>/dev/null \
		| grep -oE 'mcp__[a-z_-]+(\.\*|_\.\*|__\.\*)?' \
		| grep -i 'auggie' \
		| sed -E 's/\.\*$$//' | sort -u); \
	case_prefixes=$$(grep -oE 'mcp__[a-z_-]+(_\*|__\*|\*)' \
		src/superclaude/hooks/scripts/auggie-flag-clear.sh \
		| grep -i 'auggie' \
		| sed -E 's/\*$$//' | sort -u); \
	if [ "$$matcher_prefixes" = "$$case_prefixes" ]; then \
		echo "  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes"; \
	else \
		echo "  ❌ DRIFT between hooks.json:60 matcher and auggie-flag-clear.sh case body"; \
		echo "      hooks.json prefixes: $$matcher_prefixes"; \
		echo "      auggie-flag-clear.sh prefixes: $$case_prefixes"; \
		drift=1; \
	fi; \
```

**Notes for builder:**
- Verbatim from release-spec §5.1 with tab indentation for Makefile recipe.
- Multi-line `jq | grep | grep | sed | sort` pipeline uses `\` line continuations correctly.
- Six-space indent on detail lines matches Skills DIFFERS sub-line convention (Makefile:169).
- Depends on `jq`; if missing, will fail loudly (empty matcher_prefixes vs populated case_prefixes → drift=1).

---

## 6. Insertion location summary

**Exact insertion point:** Between Makefile line 240 (`done; \` ending the Commands reverse loop) and line 241 (`echo ""; \` opening the final drift summary).

Order of new sections (per release-spec §3-5):
1. `=== Hooks ===` (forward + reverse)
2. `=== Installer Registration ===`
3. `=== Hooks Cross-Consistency ===`

After insertion, the next line is line 241's `echo ""; \` then the existing final drift block at 242-247 (unchanged). All `drift=1` assignments in the new sections feed the existing accumulator.

---

## 7. Summary of divergences (spec → existing pattern)

| ID | Section | Spec choice | Existing pattern | Recommendation |
|---|---|---|---|---|
| D1 | Hooks forward | `[ -f "$$hook" ] || continue` | No guard in forward | Keep guard — safer, minor improvement |
| D2 | Hooks forward MISSING | `(run 'make sync-dev')` helper | No helper text | Either acceptable; keeping helper aids users |
| D3 | Hooks forward | No `case` skip | All others have one | Acceptable — no current hook needs skipping |
| D4 | Installer Reg | Bash `<(...)` process sub | POSIX shell throughout | **CRITICAL** — add `SHELL := /bin/bash` or use temp files |
| D5 | Installer Reg | `while read name` | per-file loops use `for` | Acceptable for piping `comm` output |
| D6 | Installer Reg | `❌` for MISSING and STALE | `❌` MISSING / `⚠️` DIFFERS | Defensible — both are hard failures |
| D7 | Installer Reg | One ✅ for whole section | One ✅ per file | Defensible — set-level check |
| D8 | Cross-Consistency | New `jq` dep | No `jq` currently | Acceptable — fails loudly if missing |
| D9 | Cross-Consistency | 6-space detail indent | Matches Skills DIFFERS pattern | Good consistency |
| D10 | Cross-Consistency | `sed -E 's/\.\*$$//'` | — | Correct Make-shell escape |
| D11 | Cross-Consistency | No per-file iteration | — | Acceptable — set equality check |

**Highest-priority issue: D4** — the `<(...)` process substitution in `=== Installer Registration ===` will silently fail under `dash` (default `/bin/sh` on Debian/Ubuntu). Builder must either declare `SHELL := /bin/bash` in the Makefile or rewrite using temp files.

---

## 8. Final recommendation for builder

1. **Verify `SHELL` declaration in Makefile** before pasting Installer Registration block. If `SHELL := /bin/bash` is not already present, add it at the top of the Makefile (or guard the section with temp files).
2. **Paste the three blocks in §5.1, §5.2, §5.3 above verbatim** between Makefile lines 240 and 241.
3. **Preserve tab indentation** — Makefile recipe lines must start with a tab (not spaces). Each line in the blocks above leads with a single tab.
4. **Match the existing drift accumulator semantics** — every failure path sets `drift=1`; no failure path early-returns or breaks the loop.
5. **Status: Complete.** All patterns documented with file:line citations; divergences flagged; verbatim blocks ready to paste.
