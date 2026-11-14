# Q29: After #539 merges, how does this host's `superclaude` CLI get the sweep command?

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q29 (line 556).

> After #539 merges, how does this host's `superclaude` CLI get the sweep command: the Coder template update or an owner-approved uv-tool reinstall? (new, R25-INV-006)

## The spec's recommended answer (verbatim)

> The Coder template (owner memory `ironclaude-updates-only-via-coder.md`, the lowest source tier, so asked rather than assumed)

## Default if unanswered (verbatim)

> The WC-16 `/sc:sweep` duty is recorded as "not runnable"; XC-04 is held

## What it gates (in words)

- SWEEP-RUNNABLE: a capability gate that holds when, after PR #539 is merged (SW-05) and the owner's chosen route has run, `superclaude sweep --help` exits 0 in the coordinator's own environment and `/sc:sweep` produces one report (`merged-requirements.md:601`).
- Through it, XC-04: the one real-id join comparison between the observer's `dispatchId` list and a sweep's row ids on one real Orca Run (`merged-requirements.md:452`).
- The WC-16 duty: the worker-contract rule that a coordinator runs `/sc:sweep` at most once per 5 minutes; until the gate holds it is recorded as "not runnable" (`merged-requirements.md:601`).
- Wave: W3 (the fourth wave); asked when the item is next (`merged-requirements.md:523`, `:556`).

## Facts the question depends on

1. Owner memory `ironclaude-updates-only-via-coder.md` (2026-11-12): "nobody updates IronClaude in place; updates reach workspaces only through the Coder template and workspace updates" (one exception: `ccsession-models.json` is fetched live).
2. The Coder template installs IronClaude into the image: `templates/VSCode-AIDev02/image/Dockerfile.coder` line 288 `ARG IRONCLAUDE_GIT_SHA=4ab620d1...` and lines 331-332 `UV_TOOL_DIR=/opt/uv/tools UV_TOOL_BIN_DIR=/usr/local/bin uv tool install ...` (read 2026-11-14 in `/home/coder/workspaces/Coder`, branch `feat/494-release-b`; the same pin on the local `origin/main` ref, last fetched 2026-11-12). The Coder workflow `.github/workflows/ironclaude-upstream-monitor.yml` runs daily at 06:00 UTC and opens a pull request bumping that pin when IronClaude master advances (lines 1-13, 337-341). Merging that PR, rebuilding the image, pushing the template and updating the workspace are separate steps after it.
3. Observed on this host 2026-11-14: two installs exist. `/usr/local/bin/superclaude` links to `/opt/uv/tools/superclaude` (image install, revision `4ab620d1`, 2026-11-11). `/home/coder/.local/bin/superclaude` is a user-level uv tool install at revision `d2d8a2d16` (IronClaude master of 2026-11-12), receipt written 2026-11-12 22:12. `PATH` lists `/home/coder/.local/bin` before `/usr/local/bin`, so the user-level install shadows the image install. Who made the user-level install is UNVERIFIED; no Coder template script installs into `~/.local` (grep of `templates/VSCode-AIDev02`).
4. Neither install has the sweep: `superclaude sweep --help` prints "No such command 'sweep'" (probe R25-INV-006, `adversarial/adversarial/invariant-probe.md:14`; re-run 2026-11-14 with the same result).
5. `/sc:sweep` falls back to `uv run --frozen --no-sync superclaude sweep run` only when the first call fails with "command not found", which "No such command" is not (`src/superclaude/skills/sc-sweep-protocol/SKILL.md`, Steps 1-2).
6. Neither `superclaude install` (copies primitives) nor `make sync-dev` (project `.claude/` copies) upgrades the CLI (`merged-requirements.md:1154`).
7. Whether a workspace update restarts the workspace and ends running sessions (coordinator, Orca) is UNVERIFIED. Whether `/home/coder` (and so `~/.local`) persists across a workspace rebuild is UNVERIFIED.
