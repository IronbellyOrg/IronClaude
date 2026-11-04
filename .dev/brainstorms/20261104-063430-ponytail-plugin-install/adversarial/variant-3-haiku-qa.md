# Variant 3 (QA): Ship `ponytail@ponytail` through the existing defaults path, default mode `off`

## Decision Summary

1. **Where**: `user_settings_defaults.json` only — add `enabledPlugins["ponytail@ponytail"]`, `extraKnownMarketplaces.ponytail`, and `env.PONYTAIL_DEFAULT_MODE: "off"`. No new installer step. `apply_settings_defaults` fills nested entries the user lacks (`src/superclaude/cli/install_user_setup.py:137-172`, `_NESTED_KEYS` at `:36`), and `install_plugins` (`:251-311`) already adds any defaults marketplace and installs any defaults plugin.
2. **Update paths**: no changes. `superclaude update` calls `install_user_setup(force=True)` (`src/superclaude/cli/main.py:403-405`); `update.sh:8` runs `superclaude install --force`. Verified this session — both already run the plugin step, and `tests/cli/test_update_command.py:88-97` pins the ordering.
3. **Mode**: installed and enabled, but with IronClaude default mode `off` (filled only when unset). Reason: the issue says "valuable skill missing" — the six `ponytail-*` skills ship and `/ponytail` works — while `off` keeps the always-on ruleset, per-subagent injection, codebase map and statusline nudge out of every default session. QA position: shipping `full` to everyone is an untestable-here behavioural change to every session and subagent; shipping disabled hides the skills and fails the issue.
4. **Failure**: unchanged contract — never fatal, reported by name, rerun retries.
5. **Opt-out**: `enabledPlugins["ponytail@ponytail"]: false` (existing mechanism, proven at `tests/cli/test_install_user_setup.py:92`).
6. **Visibility**: no `install --list` and no `doctor` changes — scope discipline.
7. **Docs/CHANGELOG**: plugin count six → seven, Ponytail paragraph, Unreleased entry.
8. **Tests**: extend `tests/cli/test_install_user_setup.py`; acceptance criteria below.
9. **Coder**: handoff note only, no Coder edits in this PR.

## Requirements

- **FR-001** `user_settings_defaults.json` carries `"ponytail@ponytail": true` in `enabledPlugins`, first in map order (budget triage: the issue's target installs before the six already-documented plugins when the 30 s budget runs short; `tests/cli/test_install_user_setup.py:199-209` asserts membership, not order).
- **FR-002** The defaults carry `extraKnownMarketplaces.ponytail.source.repo = "DietrichGebert/ponytail"`, so `install_plugins` issues `claude plugin marketplace add DietrichGebert/ponytail` (`install_user_setup.py:273-279`).
- **FR-003** The defaults carry `env.PONYTAIL_DEFAULT_MODE: "off"`, filled only when the user has not set it (`env` is a nested key, per-entry fill at `:158-161`).
- **FR-004** A user value `enabledPlugins["ponytail@ponytail"]: false` results in zero ponytail install commands (`install_plugins` filters on `is True`, `:266`).
- **FR-005** A user value `env.PONYTAIL_DEFAULT_MODE: "full"` (or `lite`/`ultra`) is never overwritten by the default `"off"`.
- **FR-006** Fix the pre-existing failure-label defect: `failed.append(args[3])` (`install_user_setup.py:303`) records `"--scope"` for every failed `plugin install` (argv is `["plugin","install",<id>,"--scope","user","-y"]`), so with seven plugins the warning cannot say which one failed. Build an explicit label per command (plugin id for installs, repo for marketplace adds) and use it in both the failure and time-limit paths (`:290-310`). The existing tests only assert the `⚠️  Plugins` prefix (`tests/cli/test_install_user_setup.py:229-242`), which is why this went unnoticed.
- **FR-007** `superclaude install`, `superclaude update` and `update.sh` need no code changes beyond FR-001..FR-006; the update regression is already pinned by `tests/cli/test_update_command.py:88-97,129-133`.
- **NFR-001** Plugin-step failure (offline, non-zero exit, timeout) never changes the exit code of install or update (`install_plugins` returns `True` on every path, `:258,307,311`; keep it that way).
- **NFR-002** No write outside `~/.claude/`; in particular the installer must not create `~/.config/ponytail/config.json`.
- **NFR-003** The 30 s shared network budget (`_NETWORK_BUDGET`, `:35`) is not raised.
- **NFR-004** No installed primitive references a `src/superclaude/` path (docs changes only touch `docs/`).

## Design

Exact edits:

1. `src/superclaude/cli/user_settings_defaults.json` — `env` block gains `"PONYTAIL_DEFAULT_MODE": "off"`; `enabledPlugins` gains `"ponytail@ponytail": true` as the first entry; `extraKnownMarketplaces` gains (first):
   ```json
   "ponytail": { "source": { "source": "github", "repo": "DietrichGebert/ponytail" } }
   ```
2. `install_user_setup.py:271-310` — build `commands` as `(label, argv)` pairs: `("ponytail@ponytail", ["plugin","install",...])`, `("DietrichGebert/ponytail", ["plugin","marketplace","add",...])`; append `label` (plus `" (time limit)"` where applicable) to `failed`. Behaviour otherwise identical.
3. `docs/getting-started/installation.md:353-360` — count and paragraph (below).
4. `CHANGELOG.md:5` — Unreleased entry (below).

## Interaction with IronClaude behaviour

- **Pragmatic style**: `src/superclaude/output-styles/pragmatic.md:136-160` already carries a ponytail-derived ladder. Ponytail's ruleset overlaps it by design. With `off` as the IronClaude default nothing is injected, so the Pragmatic contract (response format, ladder) is untouched in the default state. A user who opts in gets both rule sets — their choice, documented.
- **Hook events**: Ponytail registers SessionStart/SubagentStart/UserPromptSubmit via its own plugin hook files (`hooks/claude-codex-hooks.json`), not via settings.json; IronClaude's hooks (freshness, ccsession) register in settings.json. No settings-merge collision is possible — `apply_settings_defaults` never touches `hooks`.
- **`off` is genuinely dormant, verified upstream (2026-11-04)**: SessionStart exits before writing the flag or emitting rules (research-light.md:13); SubagentStart runs `if (!mode || mode === 'off') { process.exit(0); }` (`hooks/ponytail-subagent.js`); UserPromptSubmit (`hooks/ponytail-mode-tracker.js`) stays silent on ordinary prompts and only reacts to `/ponytail ...` — so opting in per session is exactly `/ponytail full`.
- **Subagent tax and statusline nudge**: in non-off modes every Task-spawned agent (adversarial panels, reviewers, orchestrated Orca workers) receives the ruleset, and the one-time statusline nudge fires because the installer never sets `statusLine` (codebase-context.md:43). Default `off` avoids both by construction.
- **`/sc:implement` independence** (`source.md:208-224`: never invokes ponytail-review) holds under every mode — no code dependency either way.
- **Not mode-gated — caveat**: the band module writes a per-turn row to `~/.config/ponytail/band/<project>.csv` and rebuilds `board.html` whenever the plugin is enabled and a project is detected; `record()` gates only on `options.ledger !== false && b.project !== ''` (`hooks/band/register.tsx:155-167`), not on mode. Enabled-with-`off` still ships the skills but the ledger can still write. Documented, not fought.

## Failure Behaviour

| Condition | Behaviour today (verified) | Change needed |
|---|---|---|
| No `claude` CLI | `"⏭️  Plugins: claude CLI not found; skipped"`, ok (`:258`) | none |
| Offline / non-zero exit | plugin id listed in `⚠️  Plugins: not installed: ...; rerun`, ok (`:306-310`) | FR-006 label fix only |
| 30 s budget exhausted | `"(time limit)"` entries, remaining commands skipped, ok (`:290-293`) | none; ponytail first in order (FR-001) so it wins contention |
| Budget partially spent | marketplace add persists in `known_marketplaces.json` (written by `claude` itself; the in-memory `known[market] = source` at `:279` is same-run dedup only), so a rerun retries just the install | none |
| No `node` | plugin installs fine; its hooks fail at session start (`node -e ...`, timeout 15 s). What Claude Code then shows is UNVERIFIED. The `claude` CLI itself is a Node app, so `claude` present without `node` is unlikely on Coder | docs note |
| Settings `enabledPlugins` not a dict | coerced to `{}` (`:265`), nothing installs, message says "already installed" — pre-existing cosmetic quirk | none (out of scope) |

## Opt-out

1. **Whole plugin**: `enabledPlugins["ponytail@ponytail"]: false` in `~/.claude/settings.json` — respected by `:266`, never refilled (per-entry fill, `:158-161`). Same mechanism as playwright today.
2. **Rules only**: leave the plugin enabled; the IronClaude default `off` already silences rules. To go louder set `env.PONYTAIL_DEFAULT_MODE` to `lite`/`full`/`ultra` (never overwritten); to flip per session use `/ponytail`.
3. **Ledger/band**: Ponytail's own config (`userConfig.ledger`, default true). The exact user-facing surface for flipping it is UNVERIFIED here; docs point to Ponytail's README rather than inventing one.

## Visibility (install --list / doctor)

No. `install --list` (`main.py:86-172`) inventories IronClaude-owned components; plugins are Claude-Code-managed artifacts, and a plugin block would be a new read surface plus tests for nothing #330 asks. `doctor` (`doctor.py:17-54`) has no plugin check, and a FAIL there would contradict the never-fatal plugin design (unlike codegraph, a required phase that legitimately exits 1). If observability is wanted later, file it separately as a warning-level detail line.

## Docs and CHANGELOG

- `docs/getting-started/installation.md:353-360`: "six plugins" → "seven plugins, including `playwright`, `frontend-design` and `ponytail`"; add: what Ponytail is; that IronClaude defaults it to `off` so its ruleset, per-subagent context and statusline nudge stay out of sessions until you run `/ponytail <level>` or set `env.PONYTAIL_DEFAULT_MODE`; that the per-turn ledger CSV (`~/.config/ponytail/band/`) is Ponytail's own default (`userConfig.ledger`, not mode-gated) with a pointer to its README; `node` is required for its hooks.
- `CHANGELOG.md:5` Unreleased: "### Added — `superclaude install`/`update` now install the `ponytail@ponytail` plugin (marketplace `DietrichGebert/ponytail`) on every workspace, defaulting to mode `off` via `env.PONYTAIL_DEFAULT_MODE`; opt out with `enabledPlugins[\"ponytail@ponytail\"]: false`. Plugin failure messages now name the plugin instead of `--scope`."
- Acceptance: `grep -rn "six plugins" docs/` returns nothing.

## Tests and Acceptance Criteria

Extend `tests/cli/test_install_user_setup.py` (fake-`claude` pattern, `:182-241`; no real network, no real `~/.claude`):

- **T1 defaults carry ponytail**: parse the shipped defaults; assert `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"]["repo"] == "DietrichGebert/ponytail"`, `env["PONYTAIL_DEFAULT_MODE"] == "off"`.
- **T2 fill-only-missing** (extend `:73-98`): fresh HOME → settings gain ponytail plugin `true`, marketplace entry, `PONYTAIL_DEFAULT_MODE "off"`; preset `enabledPlugins["ponytail@ponytail"]: false` and `env.PONYTAIL_DEFAULT_MODE: "full"` → both survive verbatim.
- **T3 install commands** (extend `:182-209`): `["plugin","marketplace","add","DietrichGebert/ponytail"]` in calls; `"ponytail@ponytail"` in installs; a user `false` yields no ponytail commands (mirror `:187,207`).
- **T4 already-installed skip** (extend `:212-226`): ponytail present in `installed_plugins.json` → no install command for it.
- **T5 failure labels (FR-006)**: non-zero-exit fake → `⚠️` message contains `ponytail@ponytail` and not `--scope`; `deadline=0` → `ponytail@ponytail` appears with `(time limit)`.
- **T6 update regression**: unchanged `tests/cli/test_update_command.py` suite green (proves update runs the step; `isolated_home_guard` at `:44-46` keeps it network-free).
- **T7 no fatal path**: `install_plugins` returns `ok=True` under claude-absent, non-zero-exit, and `deadline=0`, with ponytail among the wanted set.

Manual acceptance (one throwaway HOME under /tmp, never this workspace's `~/.claude`; requires the real `claude` CLI): after install, `~/.claude/plugins/installed_plugins.json` contains `ponytail@ponytail` and settings show `PONYTAIL_DEFAULT_MODE: "off"`. **UNVERIFIED platform assumption to check here**: that a settings-`env` value reaches plugin hook processes; if it does not, Ponytail's resolution falls through to `full` (research-light.md:12) and the default would be wrong. If that check fails, fall back to documenting `~/.config/ponytail/config.json {"defaultMode":"off"}` as the guaranteed path (the installer must still not write that file, NFR-002).

Done when: `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py` green; docs grep clean; CHANGELOG entry present.

## Risks

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| Settings `env` does not reach plugin hooks → default resolves to `full`, not `off` | low-med | medium (always-on rules everywhere, the exact outcome this variant avoids) | T7 manual throwaway-HOME check before merge; docs carry the `config.json` fallback |
| Upstream drift: a future Ponytail release changes `off` early-exit or hook surface (no version pin; marketplace installs latest; `off` behaviour verified 2026-11-04 at v5.3.3) | med (time) | med | CHANGELOG names the verified version; docs link the upstream README |
| 30 s budget: 3rd marketplace clone + 7th install on slow networks hits the time limit | med | low (reported, rerun retries, and ponytail is first) | FR-001 ordering; FR-006 label fix makes the retry advice actionable |
| No `node` on a target host → hook errors each session start (display UNVERIFIED) | low (Coder images ship node; `claude` needs it) | low-med | docs note |
| Ledger CSV/board writes continue in `off` (not mode-gated) — unexpected disk writes | certain when enabled + project detected | low | documented in install docs |
| Pragmatic-style users opting into `full` get duplicated ladder instructions in every session and subagent | med | low (quality of output, not correctness) | docs state the overlap and recommend `off`/`lite` |

## Out of Scope

- Any `install --list` or `doctor` plugin reporting.
- Pinning or vendoring a Ponytail version; writing `~/.config/ponytail/` anything.
- Editing `main.py` update flow or `update.sh` (no change required).
- IronClaude-side mode switching, statusline work, or band integration.
- Coder template edits (below).

## Coder Handoff

No Coder repo edit in this PR. Handoff needed, one line to the template owner: confirm the workspace template installs `superclaude` from the fork (`pipx install git+https://github.com/IronbellyOrg/IronClaude`, per `CLAUDE.md` install docs) rather than a pinned older version, so new workspaces pick up the defaults change; if it pins a version, bump the pin in the same release train. The template's 60-second install ceiling (`install_user_setup.py:31-33`) already encloses the 30 s plugin budget, which is not raised.
