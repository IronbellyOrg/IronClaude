# sc: → ic: Prefix Rename Tasklist

Generated: 2026-03-24
Source: cleanup-sc-prefix-reference-index.md (283 lines)

## Decision Point: Target Prefix

| Attribute | Value |
|-----------|-------|
| Current prefix (slash commands) | `/sc:` (e.g., `/sc:analyze`, `/sc:roadmap`) |
| Current prefix (skill dirs) | `sc-` (e.g., `sc-roadmap-protocol`) |
| Current prefix (command dir) | `commands/sc/` |
| **Proposed prefix (slash commands)** | **`/ic:`** (for IronClaude) |
| **Proposed prefix (skill dirs)** | **`ic-`** (e.g., `ic-roadmap-protocol`) |
| **Proposed prefix (command dir)** | **`commands/ic/`** |
| Alternative 1 | `/iron:` — more distinctive but longer |
| Alternative 2 | `/icl:` — three chars, avoids ambiguity with "icu", "ice" |

**STATUS: PENDING USER DECISION** — Confirm prefix choice before any execution begins.

---

## Execution Order (dependency-aware)

### Phase 0: DECISION — Confirm target prefix before proceeding

| Task ID | Action | Notes |
|---------|--------|-------|
| P0-001 | Confirm target prefix (`ic:` vs alternatives) | Blocks all subsequent phases |
| P0-002 | Decide whether to support a transition period (both `sc:` and `ic:` accepted) | Affects Phase 1 scope — dual-prefix support adds code complexity |
| P0-003 | Decide whether `.dev/releases/` archives get renamed or left as-is | 1,228 files; recommend SKIP (archival, no runtime impact) |

---

### Phase 1: CRITICAL — Dispatch Code & Config (must deploy atomically)

These files contain hardcoded routing logic. Changing one without the others breaks command discovery, installation, and skill resolution.

| Task ID | File | Change | Risk | Downstream Impact |
|---------|------|--------|------|--------------------|
| P1-001 | `src/superclaude/cli/main.py` (L32-33, L217-218) | `default="~/.claude/commands/sc"` → `"~/.claude/commands/ic"` ; help text same | CRITICAL | If changed alone: `superclaude install` writes to `ic/` but `sync-dev` still writes to `sc/`. Users with existing installs have commands in `sc/` that stop being found. Must coordinate with P1-002, P1-006. |
| P1-002 | `src/superclaude/cli/install_commands.py` (L4, L17, L23, L147, L152) | `commands/sc` → `commands/ic` in docstring, default path, `list_installed_commands()` | CRITICAL | If changed alone: installer targets `ic/` but Makefile sync still writes `sc/`. All installed commands land in wrong dir until P1-006 lands. |
| P1-003 | `src/superclaude/cli/install_skills.py` (L9, L25-26, L59-60, L96-100) | `sc-` prefix checks → `ic-`; `/sc:` → `/ic:` in output messages; `name[3:]` strip logic unchanged (prefix length same) | CRITICAL | If changed alone: skills with `sc-` directory names no longer detected by `_has_corresponding_command()` — they install as standalone skills instead of being served by commands. Must coordinate with Phase 2 directory renames. |
| P1-004 | `src/superclaude/cli/cli_portify/resolution.py` (L76-80, L201-207) | `sc:` prefix stripping → `ic:`; regex `>\s*Skill\s+sc:(\S+)` → `>\s*Skill\s+ic:(\S+)`; return value `f"sc-{skill_name}"` → `f"ic-{skill_name}"` | CRITICAL | If changed alone: `cli-portify run sc:roadmap` stops working immediately. New `ic:` prefix only works after command content files are updated (Phase 3). This is the parser that Claude uses to resolve targets. |
| P1-005 | `scripts/sync_from_framework.py` (L77-104, L444) | `ContentTransformer.transform_command()`: header pattern `→ /sc:\2` → `→ /ic:\2`; ref pattern `/sc:\1` → `/ic:\1`; link pattern `[/sc:\1]` → `[/ic:\1]` | CRITICAL | If changed alone: plugin builds (`make build-plugin`) emit `ic:` prefixed commands but skill directories still named `sc-*`. External SuperClaude_Plugin repo gets inconsistent output. |
| P1-006 | `Makefile` (L130, L131-134, L139, L203-215, L253, L282, L298, L310) | `commands/sc` → `commands/ic` (mkdir, cp, verify-sync, diff); `sc-*-protocol` glob → `ic-*-protocol` in `lint-architecture` | CRITICAL | If changed alone: `make sync-dev` creates `.claude/commands/ic/` but Python installer still defaults to `sc/`. Orphan `sc/` dir remains. `make verify-sync` checks `ic/` path, sees nothing, reports false drift. |

**Phase 1 atomicity requirement**: P1-001 through P1-006 MUST be committed and deployed together with Phase 2 directory renames. A partial deploy breaks `superclaude install`, `make sync-dev`, and `make verify-sync`.

**`make sync-dev` transition risk**: During the rename, running `make sync-dev` with the OLD Makefile copies to `commands/sc/` while `install_commands.py` may already target `commands/ic/`. The safest approach is: (1) rename Makefile + Python code in one commit, (2) run `make sync-dev` with new Makefile to create `ic/` paths, (3) delete old `sc/` paths.

---

### Phase 2: HIGH — Directory Renames (must be atomic with Phase 1)

Directory renames cascade — git tracks these as delete+create, so all internal file references must already point to new paths.

#### 2A: Command directories

| Task ID | Path | Rename To | Risk | Downstream Impact |
|---------|------|-----------|------|--------------------|
| P2-001 | `.claude/commands/sc/` (41 files) | `.claude/commands/ic/` | HIGH | Claude Code reads commands from this path. After rename, `/sc:*` commands vanish from Claude Code autocomplete until session restart with new prefix. |

#### 2B: Skill directories (source of truth)

| Task ID | Path | Rename To | Risk | Downstream Impact |
|---------|------|-----------|------|--------------------|
| P2-010 | `src/superclaude/skills/sc-adversarial-protocol/` | `src/superclaude/skills/ic-adversarial-protocol/` | HIGH | `lint-architecture` glob, `install_skills` detection, Activation sections all reference this name |
| P2-011 | `src/superclaude/skills/sc-cleanup-audit-protocol/` | `src/superclaude/skills/ic-cleanup-audit-protocol/` | HIGH | Same as above |
| P2-012 | `src/superclaude/skills/sc-cli-portify-protocol/` | `src/superclaude/skills/ic-cli-portify-protocol/` | HIGH | Contains `decisions.yaml` with `sc:` refs (Phase 3) |
| P2-013 | `src/superclaude/skills/sc-forensic-qa-protocol/` | `src/superclaude/skills/ic-forensic-qa-protocol/` | HIGH | No SKILL.md — verify still needed |
| P2-014 | `src/superclaude/skills/sc-pm-protocol/` | `src/superclaude/skills/ic-pm-protocol/` | HIGH | |
| P2-015 | `src/superclaude/skills/sc-recommend-protocol/` | `src/superclaude/skills/ic-recommend-protocol/` | HIGH | |
| P2-016 | `src/superclaude/skills/sc-release-split-protocol/` | `src/superclaude/skills/ic-release-split-protocol/` | HIGH | |
| P2-017 | `src/superclaude/skills/sc-review-translation-protocol/` | `src/superclaude/skills/ic-review-translation-protocol/` | HIGH | |
| P2-018 | `src/superclaude/skills/sc-roadmap-protocol/` | `src/superclaude/skills/ic-roadmap-protocol/` | HIGH | |
| P2-019 | `src/superclaude/skills/sc-task-unified-protocol/` | `src/superclaude/skills/ic-task-unified-protocol/` | HIGH | Most-referenced skill (sprint, cleanup-audit prompts) |
| P2-020 | `src/superclaude/skills/sc-tasklist-protocol/` | `src/superclaude/skills/ic-tasklist-protocol/` | HIGH | |
| P2-021 | `src/superclaude/skills/sc-validate-roadmap-protocol/` | `src/superclaude/skills/ic-validate-roadmap-protocol/` | HIGH | |
| P2-022 | `src/superclaude/skills/sc-validate-tests-protocol/` | `src/superclaude/skills/ic-validate-tests-protocol/` | HIGH | Contains `classification-algorithm.yaml` with `sc:` refs |

#### 2C: Skill directories (dev copies — must mirror 2B after `make sync-dev`)

| Task ID | Path | Rename To | Risk | Downstream Impact |
|---------|------|-----------|------|--------------------|
| P2-030 | `.claude/skills/sc-adversarial-protocol/` | `.claude/skills/ic-adversarial-protocol/` | HIGH | Read by Claude Code at runtime |
| P2-031 | `.claude/skills/sc-cleanup-audit-protocol/` | `.claude/skills/ic-cleanup-audit-protocol/` | HIGH | |
| P2-032 | `.claude/skills/sc-cli-portify-protocol/` | `.claude/skills/ic-cli-portify-protocol/` | HIGH | |
| P2-033 | `.claude/skills/sc-pm-protocol/` | `.claude/skills/ic-pm-protocol/` | HIGH | |
| P2-034 | `.claude/skills/sc-recommend-protocol/` | `.claude/skills/ic-recommend-protocol/` | HIGH | |
| P2-035 | `.claude/skills/sc-release-split-protocol/` | `.claude/skills/ic-release-split-protocol/` | HIGH | |
| P2-036 | `.claude/skills/sc-release-split-protocol-workspace/` | `.claude/skills/ic-release-split-protocol-workspace/` | HIGH | Contains eval data (JSON files with `sc:` refs) |
| P2-037 | `.claude/skills/sc-review-translation-protocol/` | `.claude/skills/ic-review-translation-protocol/` | HIGH | |
| P2-038 | `.claude/skills/sc-roadmap-protocol/` | `.claude/skills/ic-roadmap-protocol/` | HIGH | |
| P2-039 | `.claude/skills/sc-task-unified-protocol/` | `.claude/skills/ic-task-unified-protocol/` | HIGH | |
| P2-040 | `.claude/skills/sc-tasklist-protocol/` | `.claude/skills/ic-tasklist-protocol/` | HIGH | |
| P2-041 | `.claude/skills/sc-validate-roadmap-protocol/` | `.claude/skills/ic-validate-roadmap-protocol/` | HIGH | |
| P2-042 | `.claude/skills/sc-validate-tests-protocol/` | `.claude/skills/ic-validate-tests-protocol/` | HIGH | |

**Recommended approach**: Rename `src/` dirs first (P2-010..P2-022), then run `make sync-dev` with updated Makefile to regenerate `.claude/` dirs. Then delete any orphan `.claude/skills/sc-*` dirs. This avoids manually renaming 2C items.

#### 2D: Special file rename

| Task ID | Path | Rename To | Risk | Downstream Impact |
|---------|------|-----------|------|--------------------|
| P2-050 | `.claude/commands/sc/sc.md` | `.claude/commands/ic/ic.md` | HIGH | This is the meta-command (help/list). Filename must match prefix. |
| P2-051 | `src/superclaude/commands/sc.md` | `src/superclaude/commands/ic.md` | HIGH | Source of truth for P2-050. Content also needs `/sc:` → `/ic:` updates. |

---

### Phase 3: HIGH — Command/Skill File Content (internal references)

These are content updates inside the renamed files — changing `/sc:` references, `> Skill sc:` directives, and `sc-*-protocol` name strings inside SKILL.md and command .md files.

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P3-001 | All 42 `src/superclaude/commands/*.md` files | `/sc:` → `/ic:` in cross-references; `> Skill sc:` → `> Skill ic:` in Activation sections | HIGH | Activation sections are parsed by `resolution.py` regex — pattern must match new prefix |
| P3-002 | All 13 `src/superclaude/skills/ic-*-protocol/SKILL.md` files (post-rename) | `name: sc-*-protocol` → `name: ic-*-protocol`; any `/sc:` → `/ic:` refs | HIGH | SKILL.md `name:` field is used for matching in `lint-architecture` |
| P3-003 | `src/superclaude/skills/ic-cli-portify-protocol/decisions.yaml` | `sc:` references → `ic:` | MEDIUM | Config YAML parsed by cli-portify pipeline |
| P3-004 | `src/superclaude/skills/ic-validate-tests-protocol/classification-algorithm.yaml` | `sc:` references → `ic:` | MEDIUM | Config YAML for test classification |
| P3-005 | `src/superclaude/skills/ic-cleanup-audit-protocol/scripts/repo-inventory.sh` | Comment: `/sc:cleanup-audit` → `/ic:cleanup-audit` | LOW | Comment only, no runtime effect |
| P3-006 | Run `make sync-dev` to propagate all content changes to `.claude/` | N/A | HIGH | Must happen after all src/ content changes |

---

### Phase 4: MEDIUM — Cross-References (agents, tests, prompt templates)

#### 4A: Dispatch prompt templates (Python code with `/sc:` in string literals)

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P4-001 | `src/superclaude/cli/sprint/process.py` (L124, L170) | `/sc:task-unified` → `/ic:task-unified` in prompt string | MEDIUM | Prompt sent to Claude — wrong prefix means Claude can't find the command |
| P4-002 | `src/superclaude/cli/cleanup_audit/prompts.py` (L26, L47, L69, L92, L116) | `/sc:task-unified` → `/ic:task-unified` in 5 prompt templates | MEDIUM | Same risk as P4-001; 5 occurrences |
| P4-003 | `src/superclaude/cli/roadmap/validate_prompts.py` (L49, L57) | `sc:tasklist` → `ic:tasklist` in prompt text | MEDIUM | Prompt references for roadmap validation |
| P4-004 | `src/superclaude/cli/cli_portify/commands.py` (L22-25, L128) | `sc:roadmap` → `ic:roadmap` in docstring/examples | MEDIUM | Help text only — no runtime parsing, but confusing if stale |
| P4-005 | `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py` (L7, L55) | `sc:brainstorm` → `ic:brainstorm` in comment and skill detection | MEDIUM | Affects whether brainstorm fallback is triggered |

#### 4B: Agent definition files

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P4-010 | `src/superclaude/agents/pm-agent.md` | `/sc:pm` → `/ic:pm` | MEDIUM | Agent instruction text |
| P4-011 | `src/superclaude/agents/deep-research-agent.md` | `/sc:research` → `/ic:research` | MEDIUM | |
| P4-012 | `src/superclaude/agents/debate-orchestrator.md` | `sc:adversarial` / `/sc:adversarial` → `ic:adversarial` / `/ic:adversarial` | MEDIUM | |
| P4-013 | `src/superclaude/agents/socratic-mentor.md` | `/sc:socratic-clean-code`, `/sc:socratic-patterns`, `/sc:analyze`, `/sc:implement`, `/sc:document` → `/ic:*` | MEDIUM | 5 distinct references |
| P4-014 | Run `make sync-dev` again (or just agents sync) to propagate to `.claude/agents/` | N/A | MEDIUM | |

#### 4C: Test files

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P4-020 | `tests/cli_portify/test_resolution.py` | `sc:` prefix in test inputs/assertions → `ic:` | MEDIUM | Tests will fail until updated |
| P4-021 | `tests/cli_portify/test_discover_components.py` | `sc-` path expectations → `ic-` | MEDIUM | |
| P4-022 | `tests/cli_portify/test_brainstorm_gaps.py` | `sc:brainstorm` → `ic:brainstorm` | MEDIUM | |
| P4-023 | `tests/cli_portify/integration/test_orchestration.py` | `sc:` references → `ic:` | MEDIUM | |
| P4-024 | `tests/unit/test_review_translation.py` | `sc:` → `ic:` | MEDIUM | |
| P4-025 | `tests/sprint/test_process.py` | `/sc:task-unified` → `/ic:task-unified` | MEDIUM | |
| P4-026 | `tests/sc-roadmap/` (3 files: compliance, path conventions, routing) | `sc-roadmap` paths/refs → `ic-roadmap`; consider renaming test dir `tests/sc-roadmap/` → `tests/ic-roadmap/` | MEDIUM | Directory name is test organization, not runtime |
| P4-027 | `tests/pipeline/` (7 files) | `sc:` references in test data → `ic:` | MEDIUM | |
| P4-028 | `tests/test_sc_roadmap_refactor.sh` | 20+ `sc-` path references → `ic-`; consider renaming file itself | MEDIUM | Shell test, likely needs path updates |

#### 4D: Eval/workspace JSON files

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P4-030 | `.claude/skills/ic-release-split-protocol-workspace/*.json` (post-rename) | `/sc:release-split` → `/ic:release-split` in eval prompts and metadata | MEDIUM | Eval correctness depends on matching current prefix |

#### 4E: Script/shell files

| Task ID | File(s) | Change Pattern | Risk | Notes |
|---------|---------|---------------|------|----|
| P4-040 | `.dev/research/research-memory-optimization.sh` | `/sc:research`, `commands/sc/research.md` → `/ic:research`, `commands/ic/research.md` | LOW | Research script, not core pipeline |

---

### Phase 5: LOW — Documentation & Archives

| Task ID | Scope | Change Pattern | Risk | Notes |
|---------|-------|---------------|------|----|
| P5-001 | `CLAUDE.md` (project root) | `commands/sc/`, `/sc:`, `sc-*-protocol` refs → `ic` equivalents | LOW | Developer onboarding doc |
| P5-002 | `/config/.claude/CLAUDE.md` (user global) | `commands/sc/`, `.claude/commands/sc/` → `ic` equivalents | LOW | User-level instructions |
| P5-003 | `PROJECT_INDEX.md` (L84) | `commands/sc/` → `commands/ic/` | LOW | Project structure reference |
| P5-004 | `README.md` | `/sc:` command examples → `/ic:` | LOW | |
| P5-005 | `docs/user-guide/` (7 files) | `/sc:` command refs → `/ic:` | LOW | User-facing docs |
| P5-006 | `docs/reference/` (9 files) | `/sc:` command refs → `/ic:` | LOW | |
| P5-007 | `docs/developer-guide/` (4 files) | `/sc:`, `sc-*-protocol` refs → `ic` equivalents | LOW | |
| P5-008 | `docs/generated/` (28+ files) | `/sc:` refs → `/ic:` | LOW | Generated docs — consider regenerating instead of find/replace |
| P5-009 | `docs/generated/dev-guide-research/` (28 files) | `/sc:` refs → `/ic:` | LOW | Research extractions |
| P5-010 | `docs/generated/contributor-knowledge-base/` (3 files) | `/sc:`, `sc-*` refs → `ic` equivalents | LOW | |
| P5-011 | `docs/research/` (6 files) | `sc-` refs → `ic-` | LOW | |
| P5-012 | `docs/analysis/` (4 files) | `sc` refs (careful — `superclaude` must not be touched) | LOW | |
| P5-013 | `docs/guides/` (1 file) | `/sc:`, `sc-` refs → `ic` equivalents | LOW | |
| P5-014 | `docs/getting-started/` (2 files) | `/sc:` refs → `/ic:` | LOW | |
| P5-015 | `.dev/releases/` (~1,228 files) | **RECOMMENDED: SKIP** — archival artifacts, no runtime impact | LOW | Can be batch-renamed later if desired; risk of false positives in archived content |

---

## Dependency Graph

```
Phase 0 (Decision)
    │
    ▼
Phase 1 (Dispatch Code) ◄──── Must deploy atomically with Phase 2
    │                          P1-003 depends on P2-010..P2-022 (skill dir names)
    ▼
Phase 2 (Directory Renames) ─── Then run `make sync-dev` to regenerate .claude/
    │
    ▼
Phase 3 (File Content) ──────── Activation sections must match Phase 1 regex
    │                            Then run `make sync-dev` again
    ▼
Phase 4A (Prompt Templates) ─── Can run in parallel with 4B, 4C, 4D, 4E
Phase 4B (Agents)
Phase 4C (Tests)              ── Tests should pass after 4C; run `uv run pytest` as gate
Phase 4D (Eval JSON)
Phase 4E (Scripts)
    │
    ▼
Phase 5 (Docs) ──────────────── Safe to do any time after Phase 2; no runtime dependency
```

### Critical Coordination Points

1. **Phase 1 + Phase 2 must be a single commit** (or a fast-follow pair with no `make sync-dev` or `superclaude install` between them). If Phase 1 lands without Phase 2, `install_skills.py` can't find `ic-*` dirs because they're still named `sc-*`.

2. **`make sync-dev` must run twice**: once after Phase 2 directory renames (to create `.claude/skills/ic-*/` and `.claude/commands/ic/`), and once after Phase 3 content updates (to propagate file content changes).

3. **`make verify-sync` is the gate**: after Phases 1-3, `make verify-sync` must pass. If it reports drift, something was missed.

4. **Test suite is the final gate**: after Phases 1-4C, `uv run pytest` must pass. Failures indicate missed renames in test assertions.

---

## Natural Occurrence Safeguards

### Safe replacement patterns (use these, not bare `sc` replacement)

```bash
# Pattern 1: Slash command prefix (safe — unique delimiter)
#   Matches: /sc:analyze, /sc:roadmap, /sc:task-unified
#   Does NOT match: /ascar, /disc
sed 's|/sc:|/ic:|g'

# Pattern 2: Skill directory prefix (word-boundary safe via hyphen delimiter)
#   Matches: sc-roadmap-protocol, sc-adversarial-protocol
#   Does NOT match: disc-recovery, asco-report
sed 's|sc-\([a-z].*-protocol\)|ic-\1|g'
# Or more precisely:
sed 's|\bsc-\([a-zA-Z][a-zA-Z0-9-]*-protocol\)|ic-\1|g'

# Pattern 3: Command directory path (safe — always preceded by path separator)
#   Matches: commands/sc/, commands/sc, .claude/commands/sc/
sed 's|commands/sc\b|commands/ic|g'

# Pattern 4: Skills directory path (safe — always preceded by path separator)
#   Matches: skills/sc-, .claude/skills/sc-
sed 's|skills/sc-|skills/ic-|g'

# Pattern 5: Activation directive (safe — specific syntax)
#   Matches: > Skill sc:roadmap
sed 's|Skill sc:|Skill ic:|g'

# Pattern 6: Python string prefix check (safe — specific code pattern)
#   Matches: .startswith("sc-")
sed 's|startswith("sc-")|startswith("ic-")|g'

# Pattern 7: Python prefix strip (safe — specific code pattern)
#   Matches: name[3:]  (strip "sc-" → strip "ic-", same length, no change needed)
# NOTE: No change required — "ic-" is also 3 chars.
```

### DANGEROUS patterns — DO NOT USE

```bash
# NEVER do a bare 'sc' replacement:
sed 's|sc|ic|g'          # BREAKS: superclaude, disc, ASCII,asco, etc.

# NEVER replace 'sc' at word boundaries without delimiter context:
sed 's|\bsc\b|ic|g'      # BREAKS: abbreviations like "sc" meaning "scale", "scenario"

# NEVER replace inside the Python package name:
# 'superclaude' contains 'sc' but is Story 4's scope, not this rename
```

### Validation regex (post-rename — these should return ZERO matches)

```bash
# After all phases complete, these greps should return no matches
# (excluding .dev/releases/ if P5-015 was skipped):

# Residual /sc: command references
grep -rn '/sc:' src/ .claude/ tests/ docs/ --include='*.md' --include='*.py' --include='*.yaml' --include='*.sh' | grep -v '.dev/releases/' | grep -v 'superclaude'

# Residual sc-*-protocol directory references
grep -rn 'sc-[a-z].*-protocol' src/ .claude/ tests/ docs/ --include='*.md' --include='*.py' --include='*.yaml' | grep -v '.dev/releases/'

# Residual commands/sc/ path references
grep -rn 'commands/sc[/"]' src/ .claude/ tests/ Makefile PROJECT_INDEX.md CLAUDE.md | grep -v '.dev/releases/'
```

---

## Rollback Plan

### If rename is partially deployed and breaks

1. **Immediate**: `git revert <commit-sha>` the rename commit(s) to restore `sc:` prefix across all files
2. **Verify**: `make verify-sync` passes, `uv run pytest` passes
3. **Clean up**: Delete any orphan `.claude/commands/ic/` or `.claude/skills/ic-*` directories that `make sync-dev` may have created before revert

### If users have already installed with new prefix

1. Ask users to run `superclaude install --force` after revert to reinstall `sc:` commands
2. Users may need to manually delete `~/.claude/commands/ic/` and `~/.claude/skills/ic-*/`

### Prevention: Feature branch strategy

1. Execute all phases on a feature branch (e.g., `feature/ic-prefix-rename`)
2. Run full test suite: `uv run pytest`
3. Run `make verify-sync` and `make lint-architecture`
4. Test `superclaude install --list` in a clean environment
5. Only merge to integration after all gates pass

---

## Estimated Scope

| Phase | Files Modified | Files Renamed/Moved | Effort |
|-------|---------------|-------------------|--------|
| Phase 1 | 6 Python/Make files | 0 | Small (targeted edits) |
| Phase 2 | 0 (renames only) | 27 directories + 2 files | Medium (git mv) |
| Phase 3 | ~55 .md + 2 .yaml files | 0 | Medium (bulk sed with safe patterns) |
| Phase 4 | ~8 .py + 8 .md + ~18 test files + ~10 .json | 1-2 test dirs | Large (careful, many files) |
| Phase 5 | ~88 doc files | 0 | Medium (bulk, low risk) |
| **Total** | **~185 files** | **~29 dirs/files** | |

**Note**: `.dev/releases/` (1,228 files) excluded from estimate per P0-003 recommendation.
