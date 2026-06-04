# init-lite Implementation Inventory

**Produced by:** Step 1.3 (Phase 1) · **Date:** 2026-06-03
**Sources:** `research-notes.md`, `research/01-cli-registration.md`, `research/02-command-skill-patterns.md`, `research/03-report-scaffold-behavior.md`, `research/04-test-verification.md`, plus the 2026-06-03 `/sc:reflect` RESOLVED-POLICY amendments to this task.

This inventory is the implementation contract for Phases 2–4. Every file and behavior below is backed by a research citation or an on-disk evidence anchor.

## Source Files To Create

| File | Purpose | Evidence |
|------|---------|----------|
| `src/superclaude/cli/init_lite.py` | Focused Click command module: `init-lite` command + helpers for surface discovery, `ceil(bytes/4)` token estimate, low/medium/high thresholds, report rendering, output-path ownership checks, dry-run handling, scaffold creation. | research 01:25 (focused-module registration); report-writer precedent `src/superclaude/cli/sprint/preflight.py:73` (research 03:18) |
| `src/superclaude/commands/init-lite.md` | Thin `/sc:init-lite` dispatcher: frontmatter (`name: init-lite`, description, category, complexity, mcp-servers, personas), Usage, Flags table, Behavioral Summary, mandatory Activation → `Skill sc:init-lite-protocol`, Examples, Boundaries. Interface + handoff only. | research 02:94, 02:101–104; thin-command Activation evidence `commands/roadmap.md:85`, `commands/tasklist.md:70-84`, `commands/cli-portify.md:76-90` |
| `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` | Backing protocol skill: protocol frontmatter, minimal `allowed-tools` (read/report/scaffold — omit `Edit`), states "invoked only by `/sc:init-lite`", defines safe audit/report/scaffold/dry-run/force workflow + no-mutation rules + token estimate + outputs. | research 02:95, 02:108–111; protocol examples `sc-roadmap-protocol/SKILL.md:1-6,19-28`, `sc-cli-portify-protocol/SKILL.md:1-10`, `sc-recommend-protocol/SKILL.md:9-18` |
| `src/superclaude/skills/sc-init-lite-protocol/refs/*.md` | OPTIONAL — only if bulky report/scaffold templates are needed; lazy-loaded per the refs pattern. Create only if `SKILL.md` would otherwise exceed concise size. | research 02:81, 02:96, 02:110 |

## Source Files To Modify

| File | Change | Evidence |
|------|--------|----------|
| `src/superclaude/cli/main.py` | Add additive registration of the `init-lite` command in the same style as the existing deferred-import block (`main.add_command(..., name="init-lite")`) near the end of the file. | root group `main.py:18-26`; additive registrations `main.py:400-426` (research 01:24) |
| `src/superclaude/cli/install_skills.py` | **Per RESOLVED-POLICY (see Installer Mapping Decision below): likely NO functional change.** The current strip-only-`sc-` behavior already leaves every `sc-*-protocol` skill installed standalone, which is the desired end state. Any edit is permitted ONLY to preserve standalone install of all protocol skills (incl. `sc-init-lite-protocol`); must NOT generalize the strip to `-protocol`. | `install_skills.py:19-30` (`cmd_name = skill_name[3:]`), `:58-68` (skip/rmtree call site), `:94-98` (served-by-command report) |

## Tests To Create Or Modify

| File | Change | Evidence |
|------|--------|----------|
| `tests/cli/test_init_lite.py` (create) | `CliRunner` against `superclaude.cli.main:main`. Cover: `ceil(bytes/4)` incl. 0 and non-multiples; low/medium/high thresholds; surface discovery of `CLAUDE.md`/`.mcp.json`/`.claude/settings.json`/`.claude/commands/sc/foo.md`/`.claude/skills/foo/SKILL.md`/`.claude/agents/foo.md`; dry-run writes nothing & no `.dev/superclaude/`; default report w/ marker & no scaffold; scaffold opt-in (only the two files); `CLAUDE.md` byte preservation across dry-run/default/scaffold/force; idempotent marked-report; `--help` lists all 6 flags; no target-project `.claude/` writes. Use `tmp_path`, assert negative evidence. | research 04:20–31; live-Click precedent `tests/cli/test_cli_registration.py:23-26,57-59` |
| `tests/cli/test_cli_registration.py` (modify) | Add `"init-lite"` to `EXPECTED_TOP_LEVEL_COMMANDS`; assert top-level help lists `init-lite` and `init-lite --help` exposes `--context-optimized`, `--dry-run`, `--output`, `--project-root`, `--scaffold`, `--force`. | roster `test_cli_registration.py:29-48`; roster assertion `:73-82`; help smoke `:108-119` (research 04:12-14) |
| `tests/unit/test_cli_install.py` (modify — nearest installer test module, confirmed on disk) | **F2 regression guard:** assert `sc-init-lite-protocol` installs standalone like the existing protocol skills, AND every existing `sc-<command>-protocol` whose `commands/<command>.md` exists is still installed standalone (sample: `sc-roadmap-protocol`, `sc-reflect-protocol`, `sc-task-protocol`) + post-install `sc-*-protocol` count not reduced; must FAIL against the rejected `-protocol`-stripping fix. NOTE (sc:reflect F2): this module currently has ZERO `served_by_command` coverage. | amended Step 3.3; `install_skills.py:19-30,58-68,94-98`; `tests/unit/test_cli_install.py` exists |

## Safety Invariants

1. **Dry-run writes nothing** — `--dry-run` creates no files and does NOT create `.dev/superclaude/` (research 03:21,24).
2. **Default = report only** — writes only `.dev/superclaude/context-audit.md` (or explicit `--output`) bearing marker `<!-- generated-by: superclaude init-lite context-audit v1 -->`; no scaffold (research 03:19,37).
3. **Scaffold = opt-in, scoped** — `--scaffold` creates only `.dev/superclaude/project-guidance/SKILL.md` and `.dev/superclaude/project-guidance/refs/README.md` (research 03:22).
4. **Target-project context is read-only** — never modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, `.claude/agents/**` under ANY flag combination (research 03:23,37).
5. **`--force` scope pin (sc:reflect F4)** — overwrites ONLY init-lite-owned generated artifacts under `.dev/superclaude/` (the marked report / `--output` path + scaffold files); never creates/overwrites outside `.dev/superclaude/`; never overwrites a non-`--output` file lacking the marker; never overrides invariant #4 (amended Step 2.1; research 03:37).
6. **Deterministic token model** — `ceil(bytes/4)`; thresholds `low < 1000`, `medium 1000–4000`, `high > 4000` — pinned by tests since not pre-existing code (research 03:28).
7. **Protocol-skill install preservation (sc:reflect F1)** — all 16 existing `sc-*-protocol` skills + `sc-init-lite-protocol` remain installed standalone (RESOLVED-POLICY).
8. **Edge cases** — missing `CLAUDE.md` → report "none found", don't create; missing `.claude/` → report zero assets, don't create; output exists without marker & no `--force` → clear Click error (research 03:34-37).

## Validation Commands (UV/make only)

1. `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py -v` (Step 4.1)
2. Targeted installer test selection, e.g. `uv run pytest tests/unit/test_cli_install.py -v` (Step 4.2)
3. `make sync-dev` (Step 4.3)
4. `make verify-sync` (Step 4.4)
5. `make lint` **and** `uv run ruff format --check src/ tests/` (Step 4.5, sc:reflect F3 — `make lint` alone is not CI parity; CI runs format-check at `.github/workflows/test.yml:98-100`)

## Installer Mapping Decision

**RESOLVED-POLICY (sc:reflect F1, 2026-06-03): keep all protocol skills installed standalone — scope narrowly.**

Research 02:83–90/117 presented a fork: either (a) rename the skill to `sc-init-lite/` so the current strip-`sc-` logic maps it to `commands/init-lite.md` (→ NOT installed standalone), or (b) generalize `_has_corresponding_command` to map `sc-<command>-protocol` → `commands/<command>.md`. **Both branches of that fork are rejected** by the resolved policy because:

- Branch (b) would match **all 16** existing `sc-*-protocol` skills (every one has a matching `commands/<command>.md`), move them into `served_by_command`, and `shutil.rmtree` their standalone installs (`install_skills.py:58-68,94-98`). Every `/sc:*` command activates its skill by name (`commands/reflect.md:125` → `> Skill sc:reflect-protocol`), so removing the standalone installs would break command activation for end-user (`superclaude install`) installs.
- Branch (a) makes init-lite inconsistent with the 16 (which ARE installed standalone today).

**Decision:** Keep the requested `sc-init-lite-protocol` name and make **no installer change that reclassifies any protocol skill as command-backed**. `sc-init-lite-protocol` is installed standalone exactly like the 16 existing protocol skills — the accepted tradeoff being that it appears as a standalone skill alongside the `/sc:init-lite` command, identical to how all 16 existing protocol skills behave today. Step 2.3's implementation is therefore expected to be a no-op or a comment/guard clarifying intent; Step 3.3's tests lock the behavior so a future over-broad fix cannot silently sweep the 16.
