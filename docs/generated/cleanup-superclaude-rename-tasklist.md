# SuperClaude -> IronClaude Rename Tasklist

Generated: 2026-03-24
Source: `docs/generated/cleanup-superclaude-reference-index.md` (429 lines, 2,713 files)

## Naming Convention

| Context | Old | New |
|---------|-----|-----|
| Python package name | `superclaude` | `ironclaude` |
| Python module directory | `src/superclaude/` | `src/ironclaude/` |
| CLI command | `superclaude` | `ironclaude` |
| Brand name (prose) | `SuperClaude` | `IronClaude` |
| GitHub org | `SuperClaude-Org` | `IronbellyOrg` |
| GitHub repo | `SuperClaude_Framework` | `IronClaude` |
| Plugin directory | `plugins/superclaude/` | `plugins/ironclaude/` |
| Plugin repo | `SuperClaude_Plugin` | TBD (decide before Phase 2) |
| NPM scope | `@bifrost_inc/superclaude` | `@bifrost_inc/ironclaude` |
| Uppercase constant | `SUPERCLAUDE` | `IRONCLAUDE` |
| .gitignore path | `.superclaude/` | `.ironclaude/` |

---

## Execution Order (dependency-aware)

### Phase 1: CRITICAL -- Package Identity (must be coordinated as a single atomic commit)

All Phase 1 tasks MUST land in a single commit. A partial rename here leaves the package uninstallable.

| Task ID | File | Change | Risk | Downstream Impact |
|---------|------|--------|------|--------------------|
| C-001 | `src/superclaude/` (directory) | Rename to `src/ironclaude/` | CRITICAL | **Every** Python import in the project breaks until updated. This is the single highest-impact change. Must be done together with C-002 through C-006. ~300+ import statements across 282 files (48 in src/, 234 in tests/). |
| C-002 | `pyproject.toml` line 6 | `name = "superclaude"` -> `name = "ironclaude"` | CRITICAL | Changes the PyPI package name. Existing `pip install superclaude` stops resolving. Requires re-publish to PyPI under new name. Version bump to 5.0.0 recommended (breaking change). |
| C-003 | `pyproject.toml` line 64 | `superclaude = "superclaude.cli.main:main"` -> `ironclaude = "ironclaude.cli.main:main"` | CRITICAL | Changes CLI entry point. `superclaude` command stops working after reinstall. All Makefile targets, CI workflows, and user scripts that call `superclaude` break. |
| C-004 | `pyproject.toml` line 68 | `superclaude = "superclaude.pytest_plugin"` -> `ironclaude = "ironclaude.pytest_plugin"` | CRITICAL | Changes pytest plugin registration name. `pytest --trace-config` will show `ironclaude` instead of `superclaude`. Makefile `test-plugin` and CI `grep superclaude` checks break. |
| C-005 | `pyproject.toml` line 71 | `packages = ["src/superclaude"]` -> `packages = ["src/ironclaude"]` | CRITICAL | Build system cannot find package directory without this. `hatch build` fails. |
| C-006 | `pyproject.toml` lines 78-79 | `"src" = "superclaude/_src"` and `"plugins" = "superclaude/_plugins"` -> `ironclaude/...` | CRITICAL | Wheel force-include paths. Built wheel would be missing bundled sources/plugins. |
| C-007 | `pyproject.toml` line 136 | `source = ["src/superclaude"]` -> `source = ["src/ironclaude"]` | CRITICAL | Coverage tool cannot find source. `pytest --cov` reports 0% coverage. |
| C-008 | `pyproject.toml` lines 57-60 | GitHub URLs: `SuperClaude-Org/SuperClaude_Framework` -> `IronbellyOrg/IronClaude` | HIGH | Metadata-only; won't break build but PyPI page shows wrong links. |
| C-009 | `MANIFEST.in` lines 10-30 | All `recursive-include src/superclaude ...` and `plugins/superclaude ...` -> new paths | CRITICAL | Source distribution (`sdist`) will be empty / missing files. `pip install` from sdist breaks. 21 lines to update. |
| C-010 | `package.json` lines 2, 4, 17-18, 22, 25, 27, 30 | NPM package name, org URLs, keywords | HIGH | NPM package identity. Does not block Python package but blocks any JS/TS consumers. |
| C-011 | `.github/workflows/publish-pypi.yml` | 8+ references: PyPI URL, `ls src/superclaude/`, `from superclaude import`, `pip install SuperClaude`, `subprocess.run(['SuperClaude'...])` | CRITICAL | CI publish pipeline will fail on next tag push. Import verification step breaks. Summary block shows wrong name. |
| C-012 | `.github/workflows/test.yml` | 5 references: `import superclaude`, `pytest --cov=superclaude`, `grep superclaude`, `superclaude doctor` | CRITICAL | CI test pipeline fails. Coverage collection breaks. Plugin detection grep fails. |
| C-013 | `.github/workflows/quick-check.yml` line 45 | `grep -q "superclaude"` | HIGH | Quick-check CI gate fails (false negative: package IS installed but under new name). |
| C-014 | `.github/workflows/pull-sync-framework.yml` | `SuperClaude-Org/SuperClaude_Framework` (2 refs) | HIGH | Framework pull-sync workflow targets wrong repo. Non-blocking for local dev but breaks automated sync. |
| C-015 | All Python imports in `src/ironclaude/` (post-rename) | `from superclaude...` -> `from ironclaude...` across 48 files, 105 occurrences | CRITICAL | Internal imports resolve to nothing after C-001 directory rename. Every file with an import must be updated. |
| C-016 | `src/superclaude/__init__.py` | Docstring: `SuperClaude Framework` -> `IronClaude Framework` | LOW | Cosmetic within critical file. Do while touching file anyway. |
| C-017 | `src/superclaude/__version__.py` | Docstring + version bump | HIGH | Should bump to 5.0.0 to signal breaking rename. |

**Phase 1 validation gate**: After committing, run:
```bash
uv pip install -e ".[dev]"
ironclaude --version
uv run pytest --co -q  # collect tests without running
uv run python -c "from ironclaude import __version__; print(__version__)"
```

---

### Phase 2: HIGH -- CLI, Makefile & User-Facing Identity

Phase 2 can begin only after Phase 1 is validated. These changes update references that point to the old package name.

| Task ID | File | Change | Risk | Downstream Impact |
|---------|------|--------|------|--------------------|
| H-001 | `Makefile` (all targets) | 50+ refs: `superclaude` command calls, `import superclaude`, `src/superclaude/` paths, brand strings | HIGH | `make verify`, `make test-plugin`, `make doctor`, `make sync-dev`, `make verify-sync`, `make build-plugin` all break until updated. Also update `PLUGIN_DIST` path and `SuperClaude_Plugin` repo reference. |
| H-002 | `src/ironclaude/cli/main.py` | 33 refs: `prog_name`, help text, usage examples, brand strings | HIGH | CLI `--help` output shows old name. `prog_name` affects how Click formats error messages. |
| H-003 | `src/ironclaude/cli/doctor.py` | 16 refs: health check labels, import paths, brand strings | HIGH | `ironclaude doctor` output says "SuperClaude is healthy". Confusing but not breaking. |
| H-004 | `src/ironclaude/cli/__init__.py` | 7 refs: usage docstring | MEDIUM | Module docstring only. |
| H-005 | `src/ironclaude/cli/install_commands.py` | 9 refs: `plugins/superclaude/commands/` paths, brand strings | HIGH | Install command copies from wrong directory path. `ironclaude install` fails to find commands. |
| H-006 | `src/ironclaude/cli/install_core.py` | 5 refs: module paths | HIGH | Core file installation uses wrong source paths. |
| H-007 | `src/ironclaude/cli/install_skill.py` | refs to `superclaude` paths | HIGH | Skill installation broken. |
| H-008 | `src/ironclaude/cli/install_skills.py` | refs to `superclaude` paths | HIGH | Bulk skill install broken. |
| H-009 | `src/ironclaude/cli/install_agents.py` | refs to `superclaude` paths | HIGH | Agent installation broken. |
| H-010 | `src/ironclaude/cli/install_mcp.py` | 5 refs: command references, module paths | HIGH | MCP install references old CLI name. |
| H-011 | `src/ironclaude/pytest_plugin.py` | 6 refs: entry point name, marker registration, header | HIGH | Plugin header in pytest output shows old name. Marker help strings reference old name. |
| H-012 | `src/ironclaude/cli/sprint/executor.py` | 19 refs: module import paths | HIGH | Sprint execution fails on bad imports (already fixed by C-015, but brand strings remain). |
| H-013 | `src/ironclaude/cli/cli_portify/executor.py` | 12 refs | HIGH | CLI-portify executor has hardcoded module paths in prompts/templates. |
| H-014 | `src/ironclaude/cli/cli_portify/commands.py` | 9 refs | HIGH | Portify CLI group references. |
| H-015 | `src/ironclaude/cli/cli_portify/steps/__init__.py` | 8 refs | HIGH | Step registry module paths. |
| H-016 | `src/ironclaude/cli/cli_portify/steps/panel_review.py` | 6 refs | HIGH | Panel review template references. |
| H-017 | `src/ironclaude/cli/roadmap/commands.py` | 10 refs | HIGH | Roadmap CLI subcommand group. |
| H-018 | `src/ironclaude/cli/cleanup_audit/` (3 files) | 4 refs total | MEDIUM | Cleanup audit module brand strings. |
| H-019 | `plugins/superclaude/` (directory) | Rename to `plugins/ironclaude/` | HIGH | Plugin build/distribution path. 23 files. `MANIFEST.in` already updated in C-009. Makefile `PLUGIN_DIST` updated in H-001. |
| H-020 | Remaining `src/ironclaude/cli/` files (61 files, 1-4 refs each) | `from superclaude` imports (already done in C-015) + any brand strings in help text, prompts | MEDIUM | Mostly handled by C-015. Grep for residual `SuperClaude` / `superclaude` brand strings in CLI help/output. |
| H-021 | `CLAUDE.md` (root) | 50+ refs: brand, command, module, URL/org | HIGH | Primary project identity file. Claude Code reads this. Wrong name causes confusion in agent sessions. |
| H-022 | `README.md` | 40+ refs: brand, command, module, URL/org | HIGH | Public-facing project identity. |
| H-023 | `SECURITY.md` | 20+ refs: brand, URL/org | MEDIUM | Security policy references. |
| H-024 | `PROJECT_INDEX.md` / `PROJECT_INDEX.json` | 25+ refs | MEDIUM | Project navigation index. |
| H-025 | `LICENSE` | 1 ref: `Copyright (c) 2024 SuperClaude Framework Contributors` | LOW | Legal but cosmetic. |
| H-026 | `.gitignore` line 108 | `.superclaude/` -> `.ironclaude/` | LOW | Ignore pattern for local config directory. |
| H-027 | `.env.example` | 1 ref: comment | LOW | Cosmetic. |
| H-028 | `.pre-commit-config.yaml` | 1 ref: comment | LOW | Cosmetic. |
| H-029 | `.github/FUNDING.yml` | 2 refs: brand in comments | LOW | Cosmetic. |
| H-030 | `.github/workflows/readme-quality-check.yml` | 1 ref: brand string | LOW | Cosmetic label in CI. |
| H-031 | `setup.py` | 1 ref: comment | LOW | Legacy file, cosmetic. |
| H-032 | `superclaude` (root file) | CLI wrapper script | HIGH | If this is a shell wrapper invoking the old entry point, it breaks. Rename file to `ironclaude`. |
| H-033 | `scripts/build_superclaude_plugin.py` | 4 refs + filename | HIGH | Plugin build script. Rename file to `build_ironclaude_plugin.py`. Update Makefile reference in H-001. |
| H-034 | `scripts/sync_from_framework.py` | 11 refs: org URLs, module paths | MEDIUM | Sync utility references wrong remote. |
| H-035 | `scripts/uninstall_legacy.sh` | 22 refs: brand, command, module paths | MEDIUM | Legacy uninstaller. Could keep old name references intentionally (it removes old files). Add new name removal logic. |
| H-036 | `scripts/publish.sh` | 4 refs | MEDIUM | Publish script brand/command references. |

**Phase 2 validation gate**:
```bash
make verify          # All checks pass with new name
make test-plugin     # Plugin discovered as "ironclaude"
make sync-dev        # Sync completes without errors
make verify-sync     # No drift detected
ironclaude doctor    # Health check passes
```

---

### Phase 3: MEDIUM -- Tests & Tooling

Phase 3 can begin after Phase 1 (imports fixed). Phase 2 is NOT a hard prerequisite -- tests care about imports, not Makefile brand strings.

| Task ID | File | Change | Risk | Downstream Impact |
|---------|------|--------|------|--------------------|
| M-001 | `tests/` -- all 234 files with imports | `from superclaude...` -> `from ironclaude...` (965 occurrences) | MEDIUM | Tests fail to import until fixed. This is mechanical: find-and-replace across all test files. No functional logic changes needed. |
| M-002 | `tests/conftest.py` (if exists) | Update any `superclaude` fixture references | MEDIUM | Shared fixtures may reference old package name. |
| M-003 | `tests/test_cleanup_audit_structure.py` | 20 import refs -- highest density test file | MEDIUM | Straightforward import rename. |
| M-004 | `tests/sprint/test_preflight.py` | 61 refs -- highest total ref count in tests | MEDIUM | Many mocked paths like `superclaude.cli.sprint.preflight.Path`. Mock targets must match new module name. |
| M-005 | `tests/roadmap/test_convergence.py` | 47 refs | MEDIUM | Same as M-004: mock targets referencing `superclaude.` module paths. |
| M-006 | `tests/audit/test_ac_validation.py` | 39 refs | MEDIUM | Heavy mock usage of old module paths. |
| M-007 | `tests/sprint/test_phase8_halt_fix.py` | 23 refs | MEDIUM | Mock paths. |
| M-008 | `tests/sprint/test_regression_gaps.py` | 24 refs | MEDIUM | Mock paths. |
| M-009 | `tests/cli_portify/test_discover_components.py` | 17 refs | MEDIUM | Mock paths + potentially hardcoded path strings in assertions. |
| M-010 | `tests/cli_portify/test_monitor.py` | 18 refs | MEDIUM | Mock paths. |
| M-011 | `tests/sprint/diagnostic/test_instrumentation.py` | 13 refs | MEDIUM | Mock paths. |
| M-012 | `tests/roadmap/test_cli_contract.py` | 13 refs | MEDIUM | CLI invocation tests may assert `superclaude` in command output. |
| M-013 | `tests/cli_portify/test_cli.py` | 12 refs | MEDIUM | CLI contract tests. |
| M-014 | `tests/v3.3/test_wiring_points_e2e.py` | 12 refs | MEDIUM | Wiring validation tests. |
| M-015 | `tests/pipeline/test_trailing_gate.py` | 31 refs | MEDIUM | Heavy mock usage. |
| M-016 | `.claude/commands/sc/` (10 files) | Brand and command references | MEDIUM | Dev copies. Will be overwritten by `make sync-dev` after src/ is updated. Can skip manual editing -- just run sync. |
| M-017 | `.claude/agents/` (4 files) | Brand references | MEDIUM | Dev copies. Same as M-016. |
| M-018 | `.claude/skills/sc-*/` (35 files across skill dirs) | Brand, module, command references | MEDIUM | Dev copies. Same as M-016. Consider renaming `sc-*` prefix to `ic-*` (separate decision). |
| M-019 | `src/ironclaude/commands/` (11 .md files) | Brand/command refs in markdown command definitions | MEDIUM | `sc.md` (7 refs), `help.md` (6 refs), `cli-portify.md` (5 refs) are highest. These define slash command behavior. |
| M-020 | `src/ironclaude/skills/` (12+ files) | Brand/module refs in skill definitions | MEDIUM | `sc-cli-portify-protocol/refs/code-templates.md` (12 refs) is densest. Skills reference `superclaude` module paths in code templates. |
| M-021 | `src/ironclaude/agents/` (5 files) | Brand references | MEDIUM | Agent definition prose. |
| M-022 | `src/ironclaude/core/` (8 files) | Brand references | MEDIUM | `CLAUDE.md` (11 refs) is densest. Framework identity docs. |
| M-023 | `src/ironclaude/execution/__init__.py` | 2 refs: docstring + import path | LOW | Already handled in C-015 for import. Docstring is cosmetic. |
| M-024 | `scripts/eval_1.py`, `eval_2.py`, `eval_3.py`, `eval_runner.py` | Module import refs | MEDIUM | Eval scripts import from `superclaude`. Will fail until updated. |
| M-025 | `scripts/fidelity-check-setup.sh` | Module path refs | LOW | Setup script. |
| M-026 | `scripts/cleanup.sh` | 2 brand refs | LOW | Cosmetic. |
| M-027 | `scripts/README.md` | 4 refs | LOW | Script documentation. |
| M-028 | `AGENTS.md` (root) | 3 refs | LOW | Cosmetic. |

**Phase 3 validation gate**:
```bash
uv run pytest --co -q              # All tests collect successfully
uv run pytest tests/ -x --timeout=60  # Tests pass (first failure stops)
make sync-dev && make verify-sync  # .claude/ synced and verified
```

---

### Phase 4: LOW -- Documentation & Archives

Phase 4 has no functional dependencies on other phases. Can be done at any time, even weeks later. These are cosmetic changes with zero runtime impact.

| Task ID | File | Change | Risk | Downstream Impact |
|---------|------|--------|------|--------------------|
| L-001 | `docs/user-guide/` (8 files) | Brand, command refs in user-facing docs | LOW | Users see old name in docs. No functional impact. |
| L-002 | `docs/developer-guide/` (6 files) | Brand, module refs | LOW | Developers see old name. |
| L-003 | `docs/reference/` (16 files) | Brand, module refs | LOW | Reference docs. |
| L-004 | `docs/generated/` (61 files) | Brand, module, command refs in generated artifacts | LOW | These are pipeline output artifacts. Regenerating via roadmap/sprint pipelines will pick up new name automatically. Manual rename optional. |
| L-005 | `docs/research/` (25 files) | Brand refs | LOW | Historical research notes. |
| L-006 | `docs/analysis/` (10 files) | Brand refs | LOW | Analysis artifacts. |
| L-007 | `docs/memory/`, `docs/mcp/`, `docs/getting-started/`, etc. (11 files) | Brand refs | LOW | Assorted docs. |
| L-008 | `.dev/releases/complete/` (~1,950 files) | Brand, module refs in archived release artifacts | LOW | **Do NOT bulk-rename.** These are historical records. Renaming would falsify the historical record of what was shipped under the `superclaude` name. Add a note to `.dev/README.md` explaining the rename instead. |
| L-009 | `.dev/releases/backlog/` (~55 files) | Brand refs in planning docs | LOW | Active planning docs. Rename in active backlog items only. |
| L-010 | `.dev/releases/current/` (~30 files) | Brand refs | LOW | Current release artifacts. Update as part of ongoing sprint work. |
| L-011 | `.dev/benchmarks/` (46 files) | Brand refs | LOW | Benchmark results. Historical. |
| L-012 | `.dev/research/` (5 files) | Brand refs | LOW | Research notes. |
| L-013 | `src/ironclaude/hooks/README.md` | 4 refs | LOW | Hook documentation. |
| L-014 | `src/ironclaude/scripts/README.md` | 4 refs | LOW | Script documentation. |
| L-015 | `src/ironclaude/modes/MODE_Introspection.md`, `MODE_Business_Panel.md` | 1 ref each | LOW | Mode documentation. |
| L-016 | `src/ironclaude/scripts/clean_command_names.py` | 2 refs | LOW | Utility script. |
| L-017 | `src/ironclaude/scripts/session-init.sh` | 1 ref | LOW | Session init script. |

---

## Dependency Graph

```
Phase 1 (CRITICAL: Package Identity)
  |
  +---> Phase 2 (HIGH: CLI & User-Facing)
  |       |
  |       +---> Phase 2 validation gate
  |
  +---> Phase 3 (MEDIUM: Tests & Tooling)
  |       |
  |       +---> Phase 3 validation gate
  |
  (Phase 2 + Phase 3 can run in parallel after Phase 1)

Phase 4 (LOW: Documentation)
  |
  (No dependencies -- can run at any time, including before Phase 1)
  (But practically, run after Phase 3 so grep-based tooling works)
```

**Hard dependencies**:
- Phase 1 MUST complete before Phase 2 or Phase 3 can begin (imports must resolve)
- Phase 2 and Phase 3 are independent of each other
- Phase 4 is independent of everything

**Recommended execution order**: Phase 1 -> Phase 2 + Phase 3 (parallel) -> Phase 4

---

## Rollback Plan

### Before Starting
1. Create a dedicated branch: `git checkout -b rename/superclaude-to-ironclaude`
2. Ensure `master` is clean and all tests pass: `uv run pytest`
3. Tag the last known-good state: `git tag pre-rename-v4.2.0`

### If Phase 1 Fails
Phase 1 is atomic -- if any part fails, revert the entire commit:
```bash
git revert HEAD       # If committed
git checkout -- .     # If uncommitted
```
The old `src/superclaude/` directory name is restored, all imports work again.

### If Phase 2 or 3 Fails
These are incremental. Fix individual files and re-commit. The package itself (Phase 1) is already working.

### If PyPI Publish Fails
- The old `superclaude` package on PyPI cannot be renamed -- it stays forever
- Publish `ironclaude` as a new package
- Optionally publish a final `superclaude==4.2.1` that prints a deprecation warning and points to `ironclaude`

### If GitHub Org/Repo Rename Fails
- GitHub supports repo renames with automatic redirects (old URL -> new URL)
- Org renames also create redirects
- Update all hardcoded URLs in Phase 2 after confirming the GitHub rename succeeds
- GitHub redirects last indefinitely but should not be relied upon permanently

### Emergency: Keep Old CLI Name as Alias
If users depend heavily on the `superclaude` command, add a temporary compatibility entry point in `pyproject.toml`:
```toml
[project.scripts]
ironclaude = "ironclaude.cli.main:main"
superclaude = "ironclaude.cli.main:main"  # Deprecated alias, remove in v6.0
```

---

## Execution Statistics

| Phase | Files | Estimated Refs | Mechanical (find-replace) | Manual Review Required |
|-------|-------|----------------|---------------------------|------------------------|
| Phase 1 | ~290 | ~1,100 | 95% (imports) | pyproject.toml, MANIFEST.in, workflows |
| Phase 2 | ~100 | ~300 | 70% (brand strings) | CLI help text, Makefile logic, install paths |
| Phase 3 | ~280 | ~1,000 | 90% (test imports + mocks) | Mock target paths, CLI output assertions |
| Phase 4 | ~2,100 | ~3,000+ | 100% (or skip) | None -- cosmetic only |
| **Total** | **~2,770** | **~5,400+** | | |

## Key Decisions Required Before Starting

1. **Version bump**: Recommend `5.0.0` (semver major = breaking change). Confirm with maintainers.
2. **GitHub org rename**: `SuperClaude-Org` -> `IronbellyOrg` -- when? Before or after code rename?
3. **PyPI strategy**: New package `ironclaude` or attempt to rename existing `superclaude`? (Renaming is not supported by PyPI; must be a new package.)
4. **NPM package**: Rename `@bifrost_inc/superclaude` -> `@bifrost_inc/ironclaude`?
5. **Plugin repo**: `SuperClaude_Plugin` -> what? `IronClaude_Plugin`?
6. **Skill prefix**: Keep `sc-*` (short, established) or rename to `ic-*`? Renaming `sc-` prefix affects directory names, SKILL.md `name:` fields, Makefile `lint-architecture` checks, and `.claude/commands/sc/` path.
7. **Deprecation alias**: Ship `superclaude` CLI alias in v5.0 for backward compatibility?
8. **Archive policy**: Rename `.dev/releases/complete/` content or leave as historical record?
