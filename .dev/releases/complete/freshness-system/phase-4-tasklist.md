# Phase 4 -- install_hooks.py + CLI wiring + packaging

Phase goal: build the installation pipeline that distributes hook scripts and merges `hooks.json` into the user's `~/.claude/settings.json`. This is the central new IronClaude work — the existing `install_core_files` handles `core/*.md` distribution; nothing handles hook scripts or settings.json merging today. Five tasks: implementation, CLI wiring, Makefile, packaging, docs.

---

### T04.01 -- Implement install_hooks.py with atomic additive-merge

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Without this module, `superclaude install -f` cannot distribute the freshness hooks. One bad merge into the user's `~/.claude/settings.json` breaks every hook in their settings. Highest-risk single piece in the whole tasklist. |
| Effort | L | Risk | High | Risk Drivers | data loss if merge clobbers existing user hooks; atomicity if process killed mid-write; permission errors |
| Tier | STRICT | Confidence | `[████████--] 80%` | Requires Confirmation | No | Critical Path Override | Yes |
| Verification Method | Sub-agent security-engineer review + pytest unit tests + manual installer-against-fixture |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | No | Sub-Agent Delegation | Required |
| Deliverable IDs | D-0012, D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/{spec.md, code-review-report.md, evidence.md}`
- `TASKLIST_ROOT/artifacts/D-0013/{test-output.txt, test-fixtures/}`

**Deliverables:**
- `src/superclaude/cli/install_hooks.py` implementing additive merge
- `src/superclaude/tests/test_install_hooks.py` (pytest) — minimum 8 test cases covering: empty target settings.json, existing top-level hooks key with unrelated events, existing same-event with different matcher, existing same-event+same-matcher (collision case), malformed target JSON (graceful refuse), missing target file (creates), permission denied (clear error message), atomic write rollback on crash
- Backup convention: writes `~/.claude/settings.json.bak.<ISO-8601>` before any write, kept indefinitely (not Claude Code's internal 5-rotate scheme — this is install_hooks's own backup)

**Steps:**
1. **[PLANNING]** Read existing `src/superclaude/cli/install_core.py` to match patterns (path discovery via `_get_core_source`, target-path arg, force flag, return tuple shape).
2. **[PLANNING]** Read `InfraDocs:phase5.1-context-refresh-design.md` §5 for the JSON shape being merged.
3. **[PLANNING]** Read `claudedocs/research_hooks_consolidated.md` for the additive-merge constraints (NFR-6/7/10/12).
4. **[EXECUTION]** Module signature: `install_hooks(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`. Default target: `Path.home() / ".claude" / "settings.json"`. Default source: `_get_hooks_source()` returns `package_root / "hooks" / "hooks.json"`.
5. **[EXECUTION]** Script-copy step (must happen BEFORE settings.json merge):
   - Source: `src/superclaude/hooks/scripts/*.sh` (or package-installed equivalent via `_get_hooks_scripts_source()`)
   - Destination: `Path.home() / ".claude" / "hooks"`
   - For each script: `shutil.copy2` + `os.chmod(0o755)`
   - On `force=False`, skip existing files; on `force=True`, overwrite
6. **[EXECUTION]** Settings-merge step:
   - If target file missing → create with shape `{"hooks": <source-hooks>}`. Exit success.
   - If target exists → backup to `<target>.bak.<ISO-8601>` (preserves user state).
   - Read target as JSON. If parse fails → return error tuple with explicit "settings.json is malformed; refusing to write. Backup at <path>" message. Do NOT attempt to fix.
   - Read source hooks.json.
   - Merge logic:
     ```
     existing_hooks = target.get("hooks", {})
     for event, registrations in source_hooks["hooks"].items():
         existing_event = existing_hooks.setdefault(event, [])
         for new_reg in registrations:
             # Check for matcher collision
             new_matcher = new_reg.get("matcher", "*")
             collision = next(
                 (r for r in existing_event if r.get("matcher", "*") == new_matcher),
                 None
             )
             if collision and not force:
                 # Skip with note in result message
                 continue
             if collision and force:
                 # Replace
                 existing_event.remove(collision)
             existing_event.append(new_reg)
     ```
   - Write merged result to temp file in same directory as target (for atomic rename).
   - `os.replace(temp, target)` — atomic on POSIX.
7. **[EXECUTION]** Return `(success: bool, message: str)` matching `install_core_files` convention. Message lists: scripts copied, scripts skipped, scripts failed; events merged, registrations added, registrations skipped due to collision, backup path.
8. **[EXECUTION]** Write pytest tests (D-0013) covering the 8 cases above.
9. **[VERIFICATION]** `uv run pytest tests/test_install_hooks.py -v` exits 0; all 8 cases pass.
10. **[VERIFICATION]** Sub-agent security-engineer review:
    - (a) Verify atomic write semantics (temp + rename, not in-place rewrite).
    - (b) Verify backup is created before ANY write.
    - (c) Verify malformed-target refusal does not destructively alter the target.
    - (d) Verify force-flag does not accidentally remove unrelated user hooks.
    - (e) Verify `chmod 0o755` happens AFTER copy, so a failed copy doesn't leave a 0-byte executable.
    - (f) Verify no `os.system` / shell-out for the merge logic (NFR-6 security).
11. **[VERIFICATION]** Manual installer run against a synthetic fixture: create `/tmp/freshness-install-fixture/settings.json` with 2 unrelated PreToolUse hooks, run `install_hooks(target_path=...)`, confirm the 2 unrelated hooks are preserved AND the 7 freshness hooks are added.

**Acceptance Criteria:**
- File `src/superclaude/cli/install_hooks.py` exists, passes `python -m py_compile`, and matches the signature pattern of `install_core_files`.
- All 8 pytest cases pass (D-0013 test-output.txt shows green).
- Sub-agent review report addresses each of (a)-(f) explicitly with "PASS" or specific concern.
- Manual fixture test confirms unrelated user hooks survive the install.

**Validation:**
- Manual: `cd /config/workspace/IronClaude && uv run python -c "from superclaude.cli.install_hooks import install_hooks; print(install_hooks(target_path=Path('/tmp/fixture/settings.json')))"`
- Evidence: spec.md (links to code), test-output.txt, code-review-report.md, evidence.md (manual fixture run)

**Dependencies:** T03.01 (hooks.json source is registration-complete)
**Rollback:** Delete `src/superclaude/cli/install_hooks.py` and its test file.
**Notes:** No shell-out, no jq dependency. Pure Python with `json` module + `shutil` + `os`. Atomic via `os.replace`. The biggest single-task risk in the whole tasklist; pytest coverage is non-negotiable.

---

### T04.02 -- Wire install_hooks into superclaude install orchestrator

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | `superclaude install` runs install_core / install_commands / install_agents / install_skills today. Without wiring install_hooks in, `make sync-dev && superclaude install -f` does not distribute the freshness work. |
| Effort | XS | Risk | Low | Risk Drivers | side-effect on existing install flow |
| Tier | STANDARD | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | pytest + manual CLI invocation against fresh fixture |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | Yes | Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0014/{spec.md, diff.md, manual-cli-output.txt}`

**Deliverables:**
- `src/superclaude/cli/main.py` updated: `install_hooks` imported and called after `install_core_files`
- Output messaging consistent with existing install flow (`📦 Installing hooks...` etc.)
- Existing test suite for `superclaude install` still passes

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/main.py` install command flow (existing imports + calls).
2. **[EXECUTION]** Add `install_hooks` to imports from `.install_hooks`.
3. **[EXECUTION]** Insert call after `install_core_files` returns. Pattern mirrors existing: `click.echo("📦 Installing hooks..."); hooks_success, hooks_message = install_hooks(force=force); click.echo(hooks_message)`.
4. **[EXECUTION]** Add `hooks_success` to the final success-check chain.
5. **[EXECUTION]** Update list / status commands (if they enumerate installed components) to include hooks.
6. **[VERIFICATION]** `uv run pytest tests/cli/ -v` — existing tests still pass.
7. **[VERIFICATION]** Manual: `uv run superclaude install --target /tmp/fixture --force` runs cleanly and shows the install_hooks output between install_core and install_commands.

**Acceptance Criteria:** diff.md shows `install_hooks` integrated into main.py flow; pytest passes; manual CLI output shows hooks step.

**Validation:** Per step. **Evidence:** diff.md + manual-cli-output.txt.

**Dependencies:** T04.01
**Rollback:** Revert main.py changes (single-file diff).

---

### T04.03 -- Update Makefile sync-dev for hooks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | `make sync-dev` currently syncs skills/agents/commands → `.claude/`. For local-dev parity with `superclaude install`, hooks should also sync. Without this, local IronClaude development can't easily test freshness hooks. |
| Effort | XS | Risk | Low | Risk Drivers | trivial Make recipe addition |
| Tier | STANDARD | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | `make sync-dev` then diff |
| MCP Requirements | None | Fallback Allowed | Yes | Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0015/{spec.md, makefile-diff.md}`

**Deliverables:**
- `Makefile` `sync-dev` target updated to also copy `src/superclaude/hooks/scripts/*.sh` → `.claude/hooks/` (mode 0755 preserved)

**Steps:**
1. **[PLANNING]** Read existing `sync-dev` target (Makefile:108-138).
2. **[EXECUTION]** Add a new recipe section after the commands sync, before the success echo:
   ```makefile
   	@mkdir -p .claude/hooks
   	@for hook in src/superclaude/hooks/scripts/*.sh; do \
   		name=$$(basename "$$hook"); \
   		cp "$$hook" ".claude/hooks/$$name"; \
   		chmod +x ".claude/hooks/$$name"; \
   	done
   ```
3. **[EXECUTION]** Update the success message to also report hooks count.
4. **[VERIFICATION]** Run `make sync-dev`. Check `.claude/hooks/` contains the 7 freshness scripts with mode 0755.
5. **[VERIFICATION]** Compare `.claude/hooks/freshness-*.sh` against `src/superclaude/hooks/scripts/freshness-*.sh` — identical content.

**Acceptance Criteria:** makefile-diff.md shows the new sync recipe; `ls -l .claude/hooks/freshness-*.sh` shows 7 mode-0755 files; `diff .claude/hooks/freshness-X.sh src/.../freshness-X.sh` clean.

**Validation:** Per step. **Evidence:** makefile-diff.md + ls output.

**Dependencies:** T01.02 (source scripts exist), T02.x (real bodies in place to make the sync meaningful)
**Rollback:** Revert Makefile changes.

---

### T04.04 -- MANIFEST.in / setup.py: ship hook scripts in wheel

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | When `superclaude install` runs from a pip-installed package (not a checkout), it needs to find hook scripts inside the installed package. Without MANIFEST.in / setup.py inclusion, sdist tarballs and wheels would omit the .sh files. |
| Effort | XS | Risk | Low | Risk Drivers | wrong glob pattern silently omits files from wheel |
| Tier | STANDARD | Confidence | `[████████--] 85%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | sdist build + tarball inspection |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | Yes | Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0016/{spec.md, sdist-listing.txt, manifest-diff.md, setup-diff.md}`

**Deliverables:**
- `MANIFEST.in` updated to include `src/superclaude/hooks/scripts/*.sh`
- `setup.py` / `pyproject.toml` package_data entry adjusted so the .sh files ship in the wheel
- `_get_hooks_source()` and `_get_hooks_scripts_source()` in `install_hooks.py` resolve correctly against both checkout and installed-package layouts

**Steps:**
1. **[PLANNING]** Read existing `MANIFEST.in` to see the pattern for `*.md` inclusion.
2. **[EXECUTION]** Add line `recursive-include src/superclaude/hooks *.sh *.json` to `MANIFEST.in` (or equivalent if grammar differs).
3. **[EXECUTION]** Read `setup.py` / `pyproject.toml` `package_data` section. Add entry `"superclaude.hooks.scripts": ["*.sh"]` (or `"superclaude": ["hooks/scripts/*.sh", "hooks/*.json"]` depending on existing pattern).
4. **[EXECUTION]** Build sdist: `uv run python -m build --sdist`. Tarball lands in `dist/`.
5. **[VERIFICATION]** `tar tzf dist/*.tar.gz | grep -E "hooks/.*\.(sh|json)$"` lists all 7 .sh files + hooks.json.
6. **[VERIFICATION]** Build wheel: `uv run python -m build --wheel`. Check wheel contains hooks: `unzip -l dist/*.whl | grep hooks/`.

**Acceptance Criteria:** sdist-listing.txt shows all 7 hook scripts + hooks.json; wheel contents include them; manifest-diff.md + setup-diff.md document the changes; `install_hooks.py`'s source-discovery functions resolve correctly in both checkout and installed-from-wheel contexts.

**Validation:** Build + extract + grep. **Evidence:** sdist-listing.txt + manifest-diff.md + setup-diff.md.

**Dependencies:** T04.01, T01.02
**Rollback:** Revert MANIFEST.in / setup.py changes.
**Notes:** Test the wheel install in a fresh venv as a sanity check: `pip install dist/*.whl` then `python -c "from superclaude.cli.install_hooks import _get_hooks_source; print(_get_hooks_source())"`.

---

### T04.05 -- README.md and CHANGELOG.md updates

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Users running `superclaude install -f` get hooks installed; they need to know what they do, what state files appear in `~/.claude/`, and how to opt out if undesired. Without docs, the feature lands silently and surprises users. |
| Effort | XS | Risk | Low | Risk Drivers | none |
| Tier | EXEMPT | Confidence | `[█████████-] 95%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | manual scan |
| MCP Requirements | None | Fallback Allowed | Yes | Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0017/diffs.md`

**Deliverables:**
- `README.md` gains a "Context freshness hooks (v5.x)" section briefly describing the system + linking to `docs/`
- `CHANGELOG.md` gains a freshness-system entry in the next-release section
- New doc page `docs/freshness-hooks.md` (or extend `docs/user-guide/`) with: what it does, what state files appear, how to opt out (remove from `~/.claude/settings.json` `hooks` block), telemetry log location

**Steps:**
1. **[EXECUTION]** Append README section (≤200 words).
2. **[EXECUTION]** Append CHANGELOG entry (1-2 lines).
3. **[EXECUTION]** Create `docs/user-guide/freshness-hooks.md` with: overview, opt-out, FAQ.
4. **[VERIFICATION]** Manual scan of all 3 files for consistency.

**Acceptance Criteria:** Three diffs in diffs.md; opt-out instructions present in docs page; CHANGELOG entry follows existing format.

**Validation:** Per step. **Evidence:** diffs.md.

**Dependencies:** T04.04 (so the docs accurately describe the install behavior)
**Rollback:** Revert the 3 file edits.

---

### Checkpoint: End of Phase 4

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Verification:**
- `uv run pytest tests/test_install_hooks.py -v` passes (all 8 cases).
- `make sync-dev` populates `.claude/hooks/freshness-*.sh` correctly.
- `uv run python -m build --sdist && tar tzf dist/*.tar.gz | grep hooks` lists hook scripts.
- README + CHANGELOG + docs/ updated.

**Exit Criteria:**
- Zero pytest failures.
- Sub-agent security review (D-0012 evidence.md) confirms all 6 review criteria (a)-(f) PASS.
- Manual fixture test (`install_hooks(target_path=/tmp/fixture)`) preserves unrelated user hooks AND adds 7 freshness registrations.
- `~/.claude/` is still NOT modified by any task in this phase (live install belongs to Phase 5).
