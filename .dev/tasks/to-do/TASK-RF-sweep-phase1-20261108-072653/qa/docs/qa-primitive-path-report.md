# QA Report: Primitive-Path Lens (T290)

**Reviewer:** qa-primitive-path (adversarial, fix_authorization: false)
**Date:** 2026-11-12
**Scope:** every path in `sweep.md`, `sc-sweep-protocol/SKILL.md`, the `WORKER-CONTRACT.md` diff and the `HOW-WE-WORK.md` diffs.
**Rule:** project CLAUDE.md, "Never Hardcode `src/superclaude/` Paths in Installed Primitives".

## Path inventory (read from disk this session)

| File | Line | Path or lookup | Form | Verdict |
|---|---|---|---|---|
| `src/superclaude/commands/sweep.md` | 16, 20 | `~/.claude/WORKER-CONTRACT.md` | installed core-doc path | OK |
| `src/superclaude/commands/sweep.md` | 14, 38 | `<root>/.dev/sweeps/` | runtime report folder in the user's checkout, not a primitive | OK |
| `src/superclaude/commands/sweep.md` | 47-55 | `~/.claude/skills/sc-sweep-protocol/SKILL.md`, then `.claude/skills/sc-sweep-protocol/SKILL.md` | installed first, project copy second and labelled "a dev checkout that ran `make sync-dev`"; line 55 states "Skills read `~/.claude/skills/` first" | OK (dual surface) |
| `src/superclaude/commands/sweep.md` | 45 | `Skill sc:sweep-protocol` | skill name, not a path | OK |
| `src/superclaude/commands/sweep.md` | 55, 61 | `superclaude sweep run` | package behaviour reached through the CLI | OK |
| `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | 15 | `~/.claude/commands/sc/sweep.md`, or the project `.claude/commands/sc/sweep.md` | installed first, project copy second | OK (dual surface) |
| `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | 33 | `~/.claude/output-styles/pragmatic.md` | installed output-style path, informational ("installed as"), not a read directive | OK (see note N1) |
| `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | 4, 23-24 | `superclaude sweep run`, `uv run --frozen --no-sync superclaude sweep run` | CLI only, no package-code path | OK |
| `src/superclaude/core/WORKER-CONTRACT.md` | diff `+` lines (never-as-worker list, WC-16) | none | the only cross-references are the heading names "The sweep." and `### Liveness supervision` in the same file | OK |
| `src/superclaude/core/HOW-WE-WORK.md` and plugin copy | diff `+` lines (2 hunks, identical in both copies) | `.dev/sweeps/`, `~/.claude/WORKER-CONTRACT.md` | installed core-doc path | OK |

## Findings

No BLOCKING or MAJOR finding.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| N1 | MINOR (note, not a defect) | `src/superclaude/skills/sc-sweep-protocol/SKILL.md:33` | Names only `~/.claude/output-styles/pragmatic.md`. This is the only surface that exists: `Makefile:109-155` (`sync-dev`) copies skills, agents, commands, hooks and templates and never output styles or core docs, so there is no project `.claude/` copy to name. The sentence is an "installed as" statement, not an instruction to read a file. | None needed. |
| N2 | MINOR (note) | `.claude/` | No `.claude/commands/sc/sweep.md` or `.claude/skills/sc-sweep-protocol/` exists in this checkout (Glob returned none), so the dual-surface project copies the two primitives name are not present until `make sync-dev` runs. They are gitignored sync-dev output and the wording says "when a project checkout holds its own copy", so the text is accurate. | None needed. Run `make sync-dev` before any `make verify-sync` step. |

## Evidence notes

- Repo's own check from CLAUDE.md, restricted to the in-scope files: `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol src/superclaude/core/WORKER-CONTRACT.md src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` printed nothing (exit 1). Separate Grep calls on `sweep.md`, the skill folder, `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` agree. A wider pattern (`superclaude/(cli|pm_agent|contracts|examples)`) also matched nothing in the two core docs.
- The added lines of the three diffs were extracted and scanned for path-like tokens: the only tokens are `.dev/sweeps/` and `~/.claude/WORKER-CONTRACT.md`, each in the two `HOW-WE-WORK.md` hunks (source and plugin copy). `cmp` reports the source and plugin `HOW-WE-WORK.md` byte-identical. The `WORKER-CONTRACT.md` diff adds no path token.
- Installed locations confirmed in code: `src/superclaude/cli/install_core.py:21,27` lists `HOW-WE-WORK.md` and `WORKER-CONTRACT.md` as core files copied to `~/.claude/`; `src/superclaude/cli/install_user_setup.py:147` installs output styles to `home / ".claude" / "output-styles"`.
- `plugins/` holds no `sweep` command or `sc-sweep-protocol` skill (only the `HOW-WE-WORK.md` mirror, `sc-recommend/SKILL.md:414` using the word "sweep" for an unrelated algorithm, and `sc-implement-protocol` files that were not modified).
- Tests (read-only run): `uv run pytest tests/commands/test_sweep_command.py tests/skills/test_primitive_dual_surface_lookup.py tests/skills/test_worker_contract.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -q` gave 1187 passed. `tests/commands/test_sweep_command.py:164` asserts `"src/superclaude/" not in _text(path)`; lines 37 and 116-126 pin installed-first order and reject an installed-only or project-only activation list.
- No file other than this report was written. No Orca, ccsession or Claude command was run.

## Checks

| id | check | result |
|---|---|---|
| C1 | `sweep.md` (all 68 lines read) has no `src/superclaude/` path and no package-code reference | PASS |
| C2 | `sc-sweep-protocol/SKILL.md` (all 64 lines read) has no `src/superclaude/` path and no package-code reference | PASS |
| C3 | `WORKER-CONTRACT.md` diff adds no `src/superclaude/` path and no other path | PASS |
| C4 | `HOW-WE-WORK.md` diffs (source and plugin copy) add only installed `~/.claude/...` paths and `.dev/sweeps/`; copies byte-identical | PASS |
| C5 | `sweep.md` skill lookup names the installed skill first and the project `.claude/` copy second, labelled as a dev-checkout copy | PASS |
| C6 | `SKILL.md` command lookup names `~/.claude/commands/sc/sweep.md` first and the project `.claude/commands/sc/sweep.md` second | PASS |
| C7 | Core-doc references use the installed form and no project copy of a core doc exists (`Makefile:109-155`, `install_core.py:21,27`) | PASS |
| C8 | Output-style path `~/.claude/output-styles/pragmatic.md` matches the installer destination (`install_user_setup.py:147`) and is informational, not a lookup | PASS |
| C9 | Package behaviour is reached only through the `superclaude sweep run` CLI | PASS |
| C10 | Plugin mirror: `HOW-WE-WORK.md` identical (`cmp`); no sweep primitive mirrored with a `src/` path | PASS |
| C11 | Related tests pass (1187 passed) and `test_sweep_command.py:164` pins the no-`src/superclaude/` rule | PASS |

Verdict: PASS

Blocking count: 0
