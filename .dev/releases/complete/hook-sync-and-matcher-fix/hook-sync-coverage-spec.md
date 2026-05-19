---
name: hook-sync-coverage-spec
type: design-spec
version: 1.0
generated: 2026-05-17T18:14:00Z
release: hook-sync-and-matcher-fix
part: 1 of 2
sibling_part: auggie-flag-clear-matcher-mitigation-spec.md (to be added — Part 2)
---

# Part 1 — `make verify-sync` hook coverage refactor

## 1. Factual answer (the user's research question)

> "Does `make sync-dev` and `superclaude install --force` cover hooks?"

**They cover hooks DIFFERENTLY, and the divergence is the actual root problem — not `verify-sync` alone.**

| Pipeline | Direction | Hook coverage | Mechanism | Failure mode |
|---|---|---|---|---|
| `make sync-dev` | `src/superclaude/` → `.claude/` | **YES, via glob** | `Makefile:137` — `for hook in src/superclaude/hooks/scripts/*.sh` | Adding a new `.sh` to source dir is auto-picked-up; no list to update |
| `superclaude install --force` | `.claude/` → `~/.claude/` | **PARTIAL, via explicit list** | `install_hooks.py:178` — iterates `_FRESHNESS_SCRIPTS` only | If new `.sh` isn't added to `_FRESHNESS_SCRIPTS`, end-user installs miss it silently |
| `make verify-sync` | `src/superclaude/` ↔ `.claude/` | **NO — entirely skipped** | `Makefile:154-247` iterates `skills/`, `agents/`, `commands/` only | New hooks land in `.claude/` invisibly; drift between src/ and .claude/ on hooks is unobservable; drift between .claude/ and `_FRESHNESS_SCRIPTS` is even less observable |

**Concrete consequence of the asymmetry:** a contributor adds `src/superclaude/hooks/scripts/foo-hook.sh`, runs `make sync-dev` (success — copies to `.claude/hooks/foo-hook.sh`), commits, ships. End users running `superclaude install` get every hook EXCEPT `foo-hook.sh` because it's not in `_FRESHNESS_SCRIPTS`. Their `~/.claude/settings.json` may even register the hook (per `hooks.json`) — pointing at a script that was never copied. The hook fires, the shell errors with "file not found", and the harness silently ignores the failure (hooks fail-open).

This exact failure mode would have happened to the auggie-bash-gate work shipped today if the implementer had forgotten the one-line `_FRESHNESS_SCRIPTS` append. The Option 3 task file caught it via Step 3.3's explicit `_FRESHNESS_SCRIPTS` membership assertion — but that's per-task discipline, not a system-level invariant.

## 2. Goals

- **G1** — `make verify-sync` reports drift on every hook file the way it does for skills/agents/commands. Symmetric bidirectional check between `src/superclaude/hooks/scripts/*.sh` and `.claude/hooks/*.sh`.
- **G2** — `make verify-sync` reports a NEW drift class: scripts present in `src/superclaude/hooks/scripts/` but absent from `_FRESHNESS_SCRIPTS` in `install_hooks.py`. This catches the "shipped to .claude/ but not to end-user `~/.claude/`" failure mode.
- **G3** — Zero behavior change to `make sync-dev` or `superclaude install --force`. They already do what they do; only the verification surface widens.
- **G4** — Exits non-zero (CI-friendly) on any hook drift, matching the existing pattern.

## 3. Non-goals

- Do NOT replace `_FRESHNESS_SCRIPTS` with a glob in `install_hooks.py`. The list is intentional — it gates which scripts the installer trusts. A future hook with an `--off-by-default` semantic (or a `.example` file masquerading as `.sh`) shouldn't be auto-deployed. The list stays; verify-sync just ASSERTS that anything in the source dir IS in the list.
- Do NOT add `legacy/session-init.sh` to the verify-sync scope — it lives outside `hooks/scripts/` (in `src/superclaude/scripts/`) and is already special-cased by both sync-dev (`Makefile:143-146`) and install_hooks (`_LEGACY_SCRIPTS`).
- Do NOT touch the `freshness-file-changed.sh` v1-not-registered anomaly — it's documented in `install_hooks.py:36-42`. Verify-sync should detect its presence in `_FRESHNESS_SCRIPTS` (it is there) and in `src/` and `.claude/` (it is), and pass. The fact that `hooks.json` doesn't register it is orthogonal.

## 4. Design

### 4.1 New `verify-sync` section: `=== Hooks ===`

Inserted after the `=== Commands ===` section and before the final `drift` check. Mirrors the existing skill/agent/command pattern verbatim — same `for` loop shape, same `❌ MISSING` / `⚠️ DIFFERS` / `✅` symbols, same `diff -q` invocation.

**Forward check (src → .claude):**

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

**Reverse check (.claude → src):**

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

The `session-init.sh` case-skip is required because it lives in `src/superclaude/scripts/` (the legacy path), not `hooks/scripts/`. Without the skip, the reverse loop would flag it as "missing in hooks/scripts/" every run.

### 4.2 New section: `=== Installer Registration ===`

Inserted after `=== Hooks ===`. Asserts that every `src/superclaude/hooks/scripts/*.sh` is also a member of `_FRESHNESS_SCRIPTS` in `install_hooks.py`. This is the layer-2 check that catches the silent end-user-install gap.

**Mechanism**: shell out to Python to import the list. Mirrors the `uv run python -c "..."` pattern already used in the auggie-bash-gate Phase 3 verification (proven to work in CI). Single-command — no parser logic in the Makefile.

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

**Caveat — `freshness-file-changed.sh`**: this script IS in `_FRESHNESS_SCRIPTS` (per the v1-keep-on-disk docstring at `install_hooks.py:36-42`) AND IS in `src/superclaude/hooks/scripts/` — so the check passes for it cleanly. The "not registered in hooks.json" anomaly is a separate orthogonal concern, not in scope for this refactor.

**Caveat — `uv run` requirement**: the check requires `uv` to be on PATH. In CI this is already a prerequisite (the test suite uses `uv run pytest`). For local dev runs without uv, the Python subprocess returns non-zero and the comm comparison silently passes (`$$registered` is empty → `missing_from_list` is the full src/ list → drift=1 with all hooks marked missing). That's loud-on-failure, not silent-bypass — acceptable.

### 4.3 What does NOT change

- `make sync-dev` body is untouched.
- `_FRESHNESS_SCRIPTS` list is untouched (verify-sync asserts it; doesn't modify it).
- `install_hooks.py` is untouched.
- The existing `=== Skills ===` / `=== Agents ===` / `=== Commands ===` sections are untouched.

## 5. Files affected

| # | Action | Path | LOC change |
|---|---|---|---|
| 1 | MODIFY | `Makefile` (lines 240-247 — insert two new sections before the final `drift` check) | ~30 lines added |
| 2 | (none for src/superclaude/) | — | — |
| 3 | (none for tests/) | — | TODO — see §7 |

**Surface area: 1 file, ~30 LOC.**

## 6. Acceptance criteria

- **AC-1**: `make verify-sync` on the current tree exits 0 (no false-positives introduced by the new sections).
- **AC-2**: After `rm .claude/hooks/auggie-bash-gate.sh`, `make verify-sync` reports `❌ MISSING in .claude/hooks/: auggie-bash-gate.sh` and exits non-zero. After `make sync-dev`, verify-sync exits 0 again.
- **AC-3**: After temporarily removing `"auggie-bash-gate.sh"` from `_FRESHNESS_SCRIPTS` (revert after test), `make verify-sync` reports `❌ MISSING from _FRESHNESS_SCRIPTS: auggie-bash-gate.sh` and exits non-zero.
- **AC-4**: After temporarily adding a fake `"ghost-hook.sh"` entry to `_FRESHNESS_SCRIPTS` (revert after test), `make verify-sync` reports `❌ STALE in _FRESHNESS_SCRIPTS: ghost-hook.sh` and exits non-zero.
- **AC-5**: `session-init.sh` (legacy path) does NOT trigger a false-positive in the reverse hook check.

## 7. Test plan

Two options, pick one based on project preference:

**Option A — Pytest wrapper around `make verify-sync`** *(recommended; mirrors `tests/hooks/test_auggie_first.py` style)*:

`tests/cli/test_verify_sync_hooks.py` — uses `subprocess.run(["make", "verify-sync"], ...)` to invoke the target, asserts on exit code and stdout patterns. Test fixtures use `tmp_path` + `git checkout` of a known-good tree, then mutate it to trigger each AC scenario.

Cons: invokes `make`, which requires `make` on PATH (already required by the project Makefile).

**Option B — Pure-Python re-implementation of the verify-sync logic, tested in isolation**:

Extract the hook-coverage logic into a `superclaude.cli.verify_sync` module with a `verify_hooks() -> tuple[bool, list[str]]` function. Makefile shells out to `uv run python -m superclaude.cli.verify_sync hooks`. Tests live in `tests/cli/test_verify_sync.py` and call the function directly.

Pros: faster, more granular, no make dependency in tests. Cons: introduces a new CLI module and a Python↔Make boundary that didn't exist before.

**Recommendation: Option A.** Smaller diff, matches existing CI pattern, no new code surface. Defer Option B to a separate refactor if the Makefile-shell logic grows.

## 8. Risks

- **R1 — `uv run` boot time**: the Installer Registration check shells out to `uv run python -c`. On cold runs this adds ~200-500 ms to `make verify-sync` wall-clock. Acceptable; verify-sync is not in a tight loop.
- **R2 — `comm` requires sorted input**: handled by `sort` in the pipeline. If a hook filename contains whitespace or quotes, the check could miscompare; current naming convention prevents this (`[a-z-]+\.sh`). Document as a constraint, don't engineer around hypothetical filenames.
- **R3 — Reverse-check skip-list grows**: today only `session-init.sh` needs `case`-skipping. If `freshness-file-changed.sh` ever moves out of `src/hooks/scripts/`, the skip list grows. Acceptable maintenance cost.

## 9. Rollback

One-line: revert the Makefile changes. The hook-coverage section can be deleted without affecting any other part of verify-sync. No state to migrate.

---

**Status:** Complete. **Next:** Part 2 — auggie-flag-clear matcher mitigation (brainstorm → adversarial debate → design), then bundle Part 1 + Part 2 into a unified `release-spec.md` for this directory.
