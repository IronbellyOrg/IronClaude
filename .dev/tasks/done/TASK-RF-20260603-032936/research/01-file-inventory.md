# Research: File Inventory (primary surface + new-module insertion point)

Topic type: File Inventory
Scope: sc-recommend skill/refs, commands/recommend.md, .gitignore cache region, cli/ module structure, main.py registration
Status: In Progress
Date: 2026-06-03

---

## 1. Primary Surface — sc-recommend skill package

All paths relative to repo root (`/config/workspace/IronClaude/.claude/worktrees/recommendv2`). Source of truth is `src/superclaude/`; `.claude/skills/sc-recommend/` is the sync-dev mirror (do NOT edit there). Line counts verified via `wc -l` on 2026-06-03.

### `src/superclaude/skills/sc-recommend/SKILL.md` — 226 lines
- **Purpose**: Full behavioral protocol for `sc-recommend` — the refined-prompt builder. Defines Phase 0 (mandatory surface enumeration + auggie sweep GATE), Phase 1 (net-value eval), Phase 2 (refined-prompt construction), Phase 3 (`--plugin` ecosystem search), anti-fabrication rules R1-R4, and the Return Contract.
- **Key structure (no Python exports — markdown skill)**:
  - Frontmatter: `name: sc-recommend`, `allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily-search, mcp__tavily__tavily-extract, WebFetch, WebSearch`, `argument-hint: "[goal description] [--plugin]"`, `category: utility`.
  - Phase 0 (lines 38-85): Step A Glob enumeration, Step B mandatory single auggie query, Step C per-candidate verification, graceful-degradation table.
  - Phase 1 (lines 87-103): net-value evaluation, anti-bloat default.
  - Phase 2 (lines 105-135): hand-off envelope construction + output template.
  - Phase 3 (lines 137-160): `--plugin` mode.
  - Rules R1-R4 (lines 162-185): no unverified flags / commands / protocol reimplementation / built-ins exempt.
  - Return Contract table (lines 187-198): `status, mode, recommendation_kind, prompt_block, verified_sources, auggie_status, degradation_notes`.
- **Cache-layer relevance**: This is the cold-path source the spec wants condensed into a ~50-line runbook (merged-requirements §Cold-Path step 1, Implementation Order #4). The Return Contract fields here are the schema the Haiku worker's JSON return extends (adds `native_likely`, `confidence_top2_delta`, `best_model_hint`, `cache_miss`, `cache_update`). Rules R1/R2/R3 are explicitly referenced in the Haiku invocation prompt (merged-requirements §Haiku Invocation Pattern).
- **Dependencies**: References its 3 refs/ files; invoked indirectly by `commands/recommend.md` `## Activation`.

### `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` — 107 lines
- **Purpose**: The "how" of Phase 0 — Glob set (8-row table mapping surface→pattern), the single auggie semantic-rank query template, per-candidate verification (Step C), the verified-candidate YAML record schema, cardinality bound (3 candidates max, 1 auggie call), and the clarifying-question rule.
- **Cache-layer relevance**: The Glob set table (lines 12-24) is the exact surface the `surface_hash` invalidation signal hashes (merged-requirements §Invalidation: `sha256(sorted(Glob('src/superclaude/{commands/*.md,skills/*/SKILL.md,agents/*.md}')))`). The verified-candidate record schema (lines 75-92) is the precursor to a cache row. Note line 94: "Cache these records within a single invocation ... Cache does not persist across invocations" — the lookup-cache feature is the persistence layer this line currently disclaims.
- **Dependencies**: Called by SKILL.md Phase 0.

### `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` — 97 lines
- **Purpose**: The "how" of Phase 1 — the net-value rubric (5 axes), commands-vs-skills-vs-agents tier selection, parallel-agent-fanout special case, the explicit "use native" case list, and the tie-break heuristic.
- **Cache-layer relevance**: Defines `native_fallback` semantics (merged-requirements: native rows are SKIPPED, never reach the table scan — Hot-Path step 3). The "use native" list (lines 76-87) is the classifier's `native_likely` decision basis.
- **Dependencies**: Called by SKILL.md Phase 1.

### `src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md` — 102 lines
- **Purpose**: The "how" of Phase 3 `--plugin` mode — in/out-of-scope source list, search-priority ladder (tech-research → deep-research → Tavily → WebFetch/WebSearch), query patterns, per-candidate result format table, output templates, citation discipline, anti-bleed rule.
- **Cache-layer relevance**: The per-candidate result fields (lines 50-59: name, capability, install command, repo URL, integration notes, version, caveats, citation) map directly to the plugin-table row schema (merged-requirements §Plugin Table). This ref owns the discovery (browse) mode; the cache adds the adoption/eval/hot-path lifecycle on top.
- **Dependencies**: Called by SKILL.md Phase 3.

### `src/superclaude/commands/recommend.md` — 117 lines
- **Purpose**: Thin dispatcher command for `/sc:recommend`. Frontmatter `name: sc:recommend`, `mcp-servers: [auggie, tavily]`, `argument-hint: "<goal description> [--plugin]"`. The `## Activation` section (lines 48-56) mandates `Skill sc-recommend` before any protocol steps and references a PreToolUse hook `sc-recommend-phase0.sh` that defense-in-depths the Phase 0 gate.
- **Flags documented** (lines 30-34): only `--plugin`. Explicitly states "No other flags" — no `--estimate`, `--stream`, `--community`, `--alternatives`, language toggle.
- **Cache-layer relevance**: This is where the NEW `--eval <mode>` flag must be added to the documented flag table (merged-requirements §`--eval` Flag; Implementation Order #7). The "No other flags" line will need revising. The `## Activation` block is where hot-path/cold-path dispatch gets wired conceptually. Hook reference `sc-recommend-phase0.sh` is researcher-06's territory (hooks.json/settings.json).
- **Dependencies**: Activates skill `sc-recommend`; references hook `sc-recommend-phase0.sh`.

---

## 2. `.gitignore` — cache region

Verified `nl -ba .gitignore` 2026-06-03.

- **Lines 101-104** (Claude Code section):
  ```
  101  # Claude Code - only ignore user-specific files
  102  .claude/history/
  103  .claude/cache/        ← spec wants this region modified
  104  .claude/*.lock
  ```
- **Lines 117-118** (Project specific — the blanket ignore + sole exception):
  ```
  117  .claude/
  118  !.claude/settings.json
  ```
- **IMPORTANT for the builder**: There are TWO relevant regions, not one. Line 103 ignores `.claude/cache/` specifically, AND line 117 blanket-ignores all of `.claude/` with line 118 as the only allow-exception. The merged-requirements §Gitignore Exception (lines 85-101 of spec) wants to ADD allow-exceptions (`!.claude/cache/`, `!.claude/cache/sc-recommend-lookup.yaml`, `!.claude/cache/sc-recommend-plugin.yaml`, `!.claude/cache/eval-runs/`, `!.claude/cache/eval-runs/**`) and re-ignore `.claude/cache/sc-recommend-events.jsonl`. gitignore last-match-wins ordering means these allow-rules must come AFTER both line 103 and line 117/118 to take effect. The builder must place them after the line-117/118 block (the spec's example at lines 88-101 shows them grouped with the existing `!.claude/settings.json` exception). Note line 103's existing `.claude/cache/` ignore is now redundant-but-harmless given line 117, but interacts with ordering — flag for builder to resolve cleanly.
- **CLAUDE.md tension**: Project CLAUDE.md has an ABSOLUTE RULE "Never Stage or Commit `.claude/` Contents" with only `settings.json` exempted. The spec explicitly invokes the user-authorized-exception clause (spec line 105). The builder MUST surface this as a human-decision/authorization checkpoint, not silently add the exceptions (per memory `feedback_human_decision_items_must_halt.md`). researcher-06 also covers sync/registration; coordinate.

---

## 3. CLI module structure — where the NEW `cli/recommend/` module goes

### Confirmed: no existing module
`src/superclaude/cli/recommend/` does NOT exist (verified `ls` → No such file or directory). This is a greenfield module.

### Peer module catalog (`src/superclaude/cli/`, verified `ls`)
Subcommand-group modules (the pattern to mirror), smallest-to-largest:

| Module dir | Files | Group registration name | Notes |
|---|---|---|---|
| `cli/tasklist/` | `__init__.py`, `commands.py`, `executor.py`, `models.py`, `gates.py`, `prompts.py` (6 files) | `tasklist` | **Cleanest minimal peer to mirror** — see layout below |
| `cli/prd/` | `__init__.py`, `commands.py`, `config.py`, `models.py`, `gates.py`, `prompts.py`, `executor.py`, + `inventory.py`, `filtering.py`, `monitor.py`, `process.py`, `logging_.py`, `diagnostics.py`, `tui.py`, `_artifact_patterns.py` (15 files) | `prd` | Larger; richer `__init__` exporting `prd_group, PrdConfig, PrdExecutor` |
| `cli/roadmap/` | 27 files incl. `convergence.py` (DeviationRegistry — atomic write), `gates.py`, `models.py`, `commands.py`, `executor.py` | `roadmap` | convergence.py is researcher-02's atomic-write anchor |
| `cli/eval/` | 25 files + `pty/`, `schemas/`, `suites/` subdirs | `eval` (via `eval.commands`) | Large harness — researcher-03's deep map |
| `cli/cleanup_audit/` | (dir) | `cleanup-audit` | underscore dir → hyphen command name |
| `cli/cli_portify/` | `cli_portify/commands.py` | (group's own name) | registered via `.commands` submodule |
| `cli/sprint/` | (dir) | `sprint` | |
| `cli/audit/` | 43 flat files (NO `commands.py` group) | n/a | NOT a click group — internal scanner library used by cleanup_audit |
| `cli/pipeline/` | shared foundation: `models.py` (`PipelineConfig`, `GateCriteria`, `SemanticCheck`, `Step`, `Deliverable`...) | n/a | base classes other modules extend |

### Recommended layout for the NEW `cli/recommend/` module (mirror `cli/tasklist/`)

The `tasklist` module is the cleanest minimal peer and is the closest fit (it is a validation/orchestration command group with config dataclass, gate data, prompts, and an executor). Mirror its 6-file layout:

```
src/superclaude/cli/recommend/
├── __init__.py        # lazy __getattr__ exporting recommend_group (mirror tasklist/__init__.py exactly)
├── commands.py        # @click.group("recommend") + subcommands; defers imports inside command bodies
├── models.py          # config dataclass(es); may extend PipelineConfig OR be standalone
├── executor.py        # orchestration logic (hot/cold dispatch, eval pipeline driver)
├── gates.py           # gate criteria as pure data (if eval adoption gate needs one)
└── prompts.py         # Haiku classifier prompt + condensed cold-path runbook text
```

Likely additional files this feature needs beyond the tasklist skeleton (per merged-requirements Implementation Order, ~700 LoC total):
- A `cache.py` / `lookup_table.py` — the YAML reader/writer (~80 LoC, mirrors `convergence.py:DeviationRegistry` atomic write — researcher-02 owns the mirror detail). Spec §Implementation Order #2.
- A `telemetry.py` — JSONL append (~20 LoC). Spec #6.
- Eval-pipeline glue may live in `executor.py` or a dedicated `eval_pipeline.py` (~200 LoC, reuses `.dev/eval-workspaces/sc-recommend/iteration-1/build_benchmark.py` + `grader.py` — researcher-03 territory). Spec #7.
- Plugin-eval gate logic (~150 LoC). Spec #8.

The final file split is a builder decision; the load-bearing inventory fact is: **mirror `cli/tasklist/`'s `__init__.py` lazy-import + `commands.py` click-group + `models.py` dataclass + `gates.py` pure-data convention**, and reuse `cli/pipeline/models.py` base classes where a config/gate fits.

### `cli/tasklist/__init__.py` pattern (the exact lazy-import convention to copy) — 18 lines
```python
def __getattr__(name: str):
    if name == "tasklist_group":
        from .commands import tasklist_group
        return tasklist_group
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["tasklist_group"]
```
This lazy pattern avoids the circular-import problem main.py works around with deferred `from ... import` statements. (`prd/__init__.py` uses eager `from .commands import prd_group` instead — both work; lazy is preferred for new modules to keep `superclaude --help` fast.)

### `cli/tasklist/commands.py` pattern — 186 lines
- `@click.group("tasklist")` def `tasklist_group()` with docstring + Examples.
- `@tasklist_group.command()` def `validate(...)` with `@click.argument` + many `@click.option` (incl. `--model`, `--debug`).
- Command body defers heavy imports: `from .executor import execute_tasklist_validate` and `from .models import TasklistValidateConfig` are imported INSIDE the function, not at module top.
- Builds a config dataclass, calls the executor, reports a written report path, `sys.exit(1)` on fail.

### `cli/tasklist/models.py` pattern — 31 lines
```python
@dataclass
class TasklistValidateConfig(PipelineConfig):   # extends superclaude.cli.pipeline.models.PipelineConfig
    output_dir: Path = field(default_factory=lambda: Path("."))
    ...
```
Config dataclasses extend `PipelineConfig`. (recommend's config may or may not need pipeline machinery — builder's call.)

### `cli/tasklist/gates.py` pattern — 47 lines
- Module-level `GateCriteria` constant, pure data, semantic-check functions imported from `roadmap/gates.py`. No enforcement logic in the gate-data file (NFR-005 unidirectional-dependency convention).

---

## 4. Exact registration point in `cli/main.py`

Verified `Read src/superclaude/cli/main.py` (431 lines) 2026-06-03.

- **The subcommand-group registration block is lines 400-426**, at module bottom after all top-level `@main.command()` defs. Each group is registered via the identical deferred-import-then-`add_command` idiom (the `# noqa: E402,I001 # intentional: deferred subcommand registration to avoid circular imports` comment is on every one):

```python
# lines 412-414 — the tasklist precedent to mirror:
from superclaude.cli.tasklist import tasklist_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
main.add_command(tasklist_group, name="tasklist")

# lines 424-426 — eval (note: imports from .commands submodule, not package):
from superclaude.cli.eval.commands import eval_group  # noqa: E402,I001 ...
main.add_command(eval_group, name="eval")
```

- **NEW registration to add** (after line 426, before the `if __name__ == "__main__":` block at line 428-430):
```python
from superclaude.cli.recommend import recommend_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
main.add_command(recommend_group, name="recommend")
```
  (Mirrors the `tasklist` form if the new `__init__.py` exports `recommend_group` lazily; use `from superclaude.cli.recommend.commands import recommend_group` if exporting from the submodule like `eval`/`prd`/`cli_portify` do.)

- **`cli/__init__.py`** (16 lines) only exports `main`; it lists commands in a docstring (lines 4-10) but does NOT need editing for a new subcommand group — registration is entirely in main.py. (Optional: add a doc line for `superclaude recommend`.)

### Referenced-symbol existence confirmation (existence only — internals are researcher-02's scope)
- `src/superclaude/cli/roadmap/convergence.py`: `class DeviationRegistry` (line 91), `def save(self)` with "Atomic write: tmp + os.replace()" (lines 304-317). CONFIRMED exists — the spec's atomic-write anchor.
- `src/superclaude/cli/install_mcp.py`: `def check_binary_available(binary_name)` (line 156), `def check_mcp_server_installed(server_name)` (line 470). CONFIRMED exist — the spec's plugin-precondition self-check anchors (merged-requirements Risk #6).

---

## 5. Spec artifacts (in scope context, not files-to-edit)

`.dev/brainstorms/sc-recommend-lookup-cache/`:
- `merged-requirements.md` — 434 lines — the authoritative spec.
- `return-contract.yaml` — 7571 bytes — the worker JSON return contract.
- `round-4-synthetic-eval-cases.md` — 19817 bytes — plugin synthetic-eval-case pipeline (precondition schema referenced by Risk #6).
- `seed-brief.md` — 12590 bytes.
- `adversarial/` subdir.

Existing eval infra the `--eval` pipeline reuses (researcher-03 owns the deep map): `.dev/eval-workspaces/sc-recommend/grader.py`, `.dev/eval-workspaces/sc-recommend/iteration-1/build_benchmark.py`, `.../iteration-1/benchmark.json`.

---

## Summary

**Primary surface (5 edit targets, all under `src/superclaude/`):**
1. `skills/sc-recommend/SKILL.md` (226 L) — cold-path source to condense; Return Contract to extend.
2. `skills/sc-recommend/refs/surface-enumeration.md` (107 L) — owns the Glob set the `surface_hash` hashes; line 94 disclaims the persistence the feature adds.
3. `skills/sc-recommend/refs/delegation-vs-native-heuristics.md` (97 L) — `native_likely`/`native_fallback` decision basis.
4. `skills/sc-recommend/refs/plugin-ecosystem-sources.md` (102 L) — plugin-row schema source.
5. `commands/recommend.md` (117 L) — add `--eval <mode>` flag to the flag table (currently says "No other flags"); revise that line.

**`.gitignore`**: TWO interacting regions — line 103 (`.claude/cache/`) and lines 117-118 (`.claude/` + `!settings.json`). New allow-exceptions must be appended AFTER line 118 (last-match-wins). Requires user-authorization checkpoint per CLAUDE.md ABSOLUTE RULE — builder must HALT, not auto-add.

**NEW module `src/superclaude/cli/recommend/`** (does not exist): mirror `cli/tasklist/`'s 6-file layout (`__init__.py` lazy `__getattr__` exporting `recommend_group`, `commands.py` `@click.group("recommend")` with deferred body-imports, `models.py` dataclass extending `PipelineConfig`, `gates.py` pure-data, `prompts.py`, `executor.py`), plus feature-specific `cache.py`/`telemetry.py` per the ~700-LoC implementation order. Config/gate base classes live in `cli/pipeline/models.py`.

**Registration**: add two lines after `cli/main.py:426` (deferred import + `main.add_command(recommend_group, name="recommend")`), mirroring the lines 412-414 tasklist idiom with the `# noqa: E402,I001` comment. `cli/__init__.py` needs no functional change.

**Confirmed referenced symbols exist** (internals are researcher-02): `roadmap/convergence.py:DeviationRegistry.save` (atomic write, L304-317), `install_mcp.py:check_mcp_server_installed` (L470) + `check_binary_available` (L156).

Status: Complete
