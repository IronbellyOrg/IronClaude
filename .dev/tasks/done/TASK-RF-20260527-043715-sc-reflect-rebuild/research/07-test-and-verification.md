# Research: Test & Verification

**Topic type:** Test & Verification
**Scope:** sc-brainstorm + sc-troubleshoot eval workspaces, Makefile, grader.py, pre-commit, CI
**Status:** Complete
**Date:** 2026-05-27

---

## 1. sc-brainstorm eval workspace (REFERENCE TEMPLATE for sc-reflect)

**Path:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/eval-workspaces/sc-brainstorm/`

**Layout (verbatim):**

```text
sc-brainstorm/
├── SPEC.md                       (684 lines — full skill spec)
├── grader.py                     (279 lines — 8 syntactic assertion types)
├── aggregate_iteration.py        (163 lines — benchmark.json/md/review.html builder)
├── evals/
│   └── evals.json                (eval-fixture catalog — 12 cases for iter-2)
├── iterations/
│   ├── iteration-1/              (3 pilot cases)
│   └── iteration-2/              (12 cases)
│       ├── benchmark.json
│       ├── benchmark.md
│       ├── review.html           (eval-viewer HTML; HTML+embedded JSON pattern)
│       ├── quality-grading.json
│       ├── quality-grading-v1rubric.json
│       ├── strict-blind-inputs/
│       └── eval-<name>/
│           ├── eval_metadata.json   (assertions list — per-case grader input)
│           ├── with_skill/
│           │   └── run-1/
│           │       ├── grading.json   (grader.py output)
│           │       ├── timing.json
│           │       └── outputs/...    (artifacts under test)
│           └── old_skill/
│               └── run-1/{grading.json,timing.json,outputs/}
└── skill-snapshot/
    └── brainstorm-v1.md          (baseline `old_skill` snapshot — v1 version of the skill)
```

**Conclusion:** sc-reflect MUST mirror this layout exactly. `skill-snapshot/reflect-v1.md` is the analogue (with the caveat per spec §13.1 that v1 of reflect is the existing `/sc:reflect` command file — this is the snapshot reflect compares against).

---

## 2. sc-brainstorm `grader.py` — the 8 inherited assertion types

**Read fully (279 lines).** All 8 types follow this signature pattern:

```python
def check_assertion(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    # assertion is a dict from eval_metadata.json with keys:
    #   type:    (one of the 8 below)
    #   target:  relative path under base_dir (typically with_skill/outputs/...)
    #   text:    human-readable description (echoed to grading.json)
    #   ... type-specific fields ...
    # returns (passed: bool, evidence: str)
```

**The 8 types reflect inherits:**

| Type | Required fields | Behavior |
|---|---|---|
| `file_exists` | `target` | `target_path.exists() and target_path.is_file()` |
| `frontmatter_field` | `target`, `field`, `expected` | YAML frontmatter parse (`---` delimited) → field value compare case-insensitive |
| `section_present` | `target`, `section_pattern` | Regex match against `^#+\s+.*<pattern>.*$` (MULTILINE+IGNORECASE) |
| `section_enumerated` | `target`, `section_pattern`, `min_items` | Section bullet/numbered count via `^\s*(?:[-*+]\|\d+\.)\s+\S` |
| `yaml_field` | `target`, `field`, `expected` | Flat YAML parse → string compare |
| `yaml_field_min` | `target`, `field`, `min_value` | Flat YAML parse → numeric ≥ check |
| `yaml_substring` | `target`, `field`, `substring_any` | Flat YAML parse → any substring match (case-insensitive) |
| `dir_count` | `target`, `min_files` | Count of regular files in dir ≥ threshold |

**Helpers (reusable for reflect's extensions):**
- `read_text(p)` → `str | None` (returns None on FileNotFoundError/IsADirectoryError)
- `parse_frontmatter(text)` → dict (naive line-split; handles flat fields only)
- `parse_yaml_simple(text)` → dict (NO nesting; flat key:value at column 0 only — **reflect's `yaml_list_contains` needs PyYAML or extended parser**)
- `find_section(text, section_pattern)` → `(start, end)` char offsets
- `count_enumerated_items(text, section_pattern)` → int

**Grading partition convention:** `check_assertion` looks at `target` prefix to route — `with_skill/...` vs `old_skill/...`. Each side writes its own `grading.json`. **Reflect must preserve this convention.**

**Reflect's 6 new semantic types** (per spec §11 / `refs/grader-extensions.md`):

| Type | Pattern (predicted from spec text) |
|---|---|
| `citation_resolves` | Read file at `assertion["cited_file"]`, lines `cited_line ± 5`; compare against `assertion["expected_snippet"]`. Fixture-root remapping via `assertion["fixture_root_remap"]` dict. |
| `regex_present` / `regex_absent` | `re.search(assertion["pattern"], read_text(target), flags=...)` |
| `yaml_list_contains` | `yaml.safe_load(read_text(target))[field]` must include `assertion["expected_item"]` (requires PyYAML — extension over `parse_yaml_simple`) |
| `matrix_covers_items` | Read coverage matrix YAML/JSON; check ≥ `min_coverage_pct` of `assertion["source_items"]` are covered |
| `checkpoint_logged` | Grep `audit.log` for row matching `assertion["checkpoint_name"]` |
| `deviation_class_matches` | Parse deviation register; verify entry tagging matches annotated fixture |

**Reflect's 2 NEW assertion types per §14.5.7:**

| Type | Pattern |
|---|---|
| `path_exists` | Mirror of `file_exists` but accepts dirs/symlinks (`target_path.exists()`); short addition to `grader.py`. |
| `path_does_not_exist` | Inverse — assertion passes if `not target_path.exists()`. Used by Wave 7 promotion no-promote tests. |

**Hook points (where to add new types in `grader.py`):**
- Add new `if a_type == "<new_type>": ...` branches to `check_assertion()` (lines 99-192). The existing 8 types' pattern serves as the template — each is an if-block returning `(passed, evidence)`.
- The fallback `return False, f"Unknown assertion type: {a_type}"` at line 192 will auto-flag missing types.

**Copy verbatim or adapt?** Reflect should COPY VERBATIM and EXTEND. The 8 inherited types are skill-agnostic; the partition routing (`with_skill/old_skill`) is generic; the runner (`grade_eval`, `main`) needs no changes. Only the `check_assertion()` switch grows.

---

## 3. sc-brainstorm `aggregate_iteration.py` — conventions reflect mirrors

**Read fully (163 lines).** Generates 3 outputs per iteration:

1. `benchmark.json` — full run records with per-config (with_skill/old_skill) statistics
2. `benchmark.md` — human-readable summary table (Pass Rate, Time, Tokens, Delta)
3. `review.html` — eval-viewer with embedded JSON (single-file HTML, includes `<script>const EMBEDDED_DATA = {...}</script>` pattern)

**Per-run record schema:**

```python
{
  "eval_id": int, "eval_name": str, "configuration": "old_skill" | "with_skill",
  "run_number": 1, "result": {
    "pass_rate", "passed", "failed", "total",
    "time_seconds", "tokens", "tool_calls", "errors"
  },
  "expectations": [...], "notes": []
}
```

**Per-config summary uses `summarize()`:** computes mean, stddev, count for `pass_rate`, `time_seconds`, `tokens`, `tool_calls` plus sum of `errors`.

**Input files per run:** `grading.json` (from grader.py) + `timing.json` (operator-supplied, contains `total_duration_seconds`, `total_tokens`, `tool_uses`).

**Quality re-grade hook:** if `quality-grading.json` exists in iter dir, the markdown gets a "Strict Quality Re-grade" section with `mean_v2`, `mean_v1`, `mean_delta` from `aggregate_totals`.

**Reflect should copy this verbatim** with `skill_name` changed to `sc-reflect-protocol`.

---

## 4. sc-troubleshoot eval workspace — diverging pattern

**Path:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/eval-workspaces/sc-troubleshoot/`

**Layout differs from sc-brainstorm:**

```text
sc-troubleshoot/
├── agent-design.md               (NO SPEC.md — uses agent-design.md naming)
├── evals/
│   ├── evals.json                (6 eval cases — tier1/tier2 troubleshoot fixtures)
│   └── fixtures/
│       └── real-bug-scratch-root/  (synthetic source files for eval input — see below)
│           ├── commands.py
│           ├── config.py
│           └── scratch-roots.md
├── iteration-1/                  (NOT iterations/iteration-1/ — flat layout!)
│   ├── benchmark.json, benchmark.md, review.html
│   └── eval-<name>/{eval_metadata.json, old_skill/, with_skill/}
├── iteration-2/
├── iteration-3/
├── forensic-analysis/
├── meta-eval-test-is-wrong/      (meta-eval test: "is the test itself wrong?")
├── phase4-5-errors-20260521202240/
└── skill-snapshot/
    └── troubleshoot.md
```

**Critical divergences from sc-brainstorm:**

1. **NO `grader.py` / `aggregate_iteration.py` at top level** (`find … -name "*.py"` confirmed only fixture files exist). Troubleshoot uses inline `eval_metadata.json` with empty `assertions: []` — grading is done elsewhere or by hand. **Reflect should NOT follow this pattern** — sc-brainstorm's grader-driven approach is the spec-mandated model.
2. **Fixtures live under `evals/fixtures/`** — synthetic source files used as eval inputs. Reflect needs this pattern for `citation_resolves` fixture-root remapping per spec §11 and §17.5.
3. **Iteration dirs are flat** (`iteration-1/` instead of `iterations/iteration-1/`). Reflect should adopt sc-brainstorm's nested `iterations/iteration-N/` for consistency with the grader's `<iteration-dir>` CLI arg.
4. **`meta-eval-test-is-wrong/`** is a notable pattern: when the executor flags "the eval fixture itself is wrong," there's a dedicated subdir for that meta-case. Reflect's `falsifier-suite/T2-converges-on-wrong.yaml` (spec line 1063) is the analogue.

**Verdict on reflect's choice:** **Copy sc-brainstorm's layout end-to-end (grader.py + aggregate_iteration.py + iterations/iteration-N/), add sc-troubleshoot's `evals/fixtures/` pattern for synthetic source files.**

---

## 5. eval_metadata.json schema (per-case)

**Authoritative schema from `iterations/iteration-2/eval-code-add-rate-limiting/eval_metadata.json`:**

```json
{
  "eval_id": 1,
  "eval_name": "code-add-rate-limiting",
  "prompt": "Brainstorm how to add rate limiting ...",
  "topic": "...",
  "expected": {
    "domain": "code",
    "strategy": "systematic",
    "proposal_count": 2,
    "enrichment_expected": ["codebase"]
  },
  "assertions": [
    {"text": "seed_brief.md exists in output dir",
     "type": "file_exists",
     "target": "with_skill/outputs/seed-brief.md"},
    {"text": "...",
     "type": "frontmatter_field",
     "target": "with_skill/outputs/seed-brief.md",
     "field": "domain", "expected": "code"}
  ]
}
```

**For reflect, `expected` should hold:** `expected_verdict`, `expected_tier`, `expected_promotion_action`, `expected_deviations_by_class`, etc. (per spec §11). The `assertions` list grows with reflect's 6+2 new types.

---

## 6. Makefile — full target inventory

**Path:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/Makefile` (528 lines)

**Targets that EXIST today (reflect uses or references):**

| Target | Lines | Body summary | Reflect relevance |
|---|---|---|---|
| `install` | 5-10 | `uv pip install -e ".[dev]"` | inherited |
| `test` | 13-15 | `uv run pytest` | inherited |
| `test-plugin` | 18-20 | pytest --trace-config | inherited |
| `doctor` | 23-25 | `uv run superclaude doctor` | inherited |
| `verify` | 28-45 | Multi-step health check | inherited |
| `lint` | 48-50 | `uv run ruff check .` | gate for reflect's grader.py |
| `format` | 53-55 | `uv run ruff format .` | applied to reflect's grader.py |
| `clean` | 58-63 | rm build artifacts | unaffected |
| `build-plugin` | 68-71 | `scripts/build_superclaude_plugin.py` | runs against new reflect skill |
| `sync-plugin-repo` | 73-87 | rsync to ../SuperClaude_Plugin | unaffected |
| `translate` | 90-106 | neural-cli README translation | unaffected |
| **`sync-dev`** | 108-163 | `src/superclaude/{skills,agents,commands,hooks,templates}` → `.claude/`; uses `find … -exec sh -c …` to recursively copy skill subdirs (refs/, rules/, scripts/, etc.); preserves perms on shell hooks (`chmod +x`); EXCLUDES `__init__.py` and `__pycache__`; skips skills whose name starts with `__` | **CRITICAL — reflect skill MUST land here** |
| **`verify-sync`** | 165-353 | Walks skills/agents/commands/hooks/templates in both directions; `diff -rq` per skill dir; ALSO checks `_FRESHNESS_SCRIPTS` registration list; ALSO checks `hooks.json` matcher vs `auggie-flag-clear.sh` case body; EXITS 1 on any drift | **Pre-commit + CI gate** |
| `verify-deps` | 356-359 | `scripts/verify_deps.py` (AC3/R-015) | unaffected unless reflect adds Python deps (PyYAML already in pyproject) |
| **`lint-architecture`** | 362-478 | Checks 1-2: bidirectional command↔skill links; Checks 3-4: command size (200 warn / 500 hard); Check 6: `## Activation` present in paired commands; Check 8: SKILL.md frontmatter completeness (`name:`, `description:`, `allowed-tools:`); Check 9: skill name ends in `-protocol`; Check 10: no `*-workspace/` in `.claude/skills/`; Checks 5/7 skipped (pending design) | **Reflect's command rewrite MUST pass Checks 1, 6, 8, 9** |
| **`eval-skill`** | 481-488 | `mkdir -p .dev/eval-workspaces/$(SKILL) && realpath …` — creates the workspace directory and prints the absolute path. Errors if `SKILL` unset. | **Reflect uses: `make eval-skill SKILL=sc-reflect-protocol`** |
| `help` | 491-522 | Documentation | unaffected |
| `uninstall-legacy` | 525-527 | `scripts/uninstall_legacy.sh` | unaffected |

**Targets that DO NOT EXIST and must be created per spec §17.5 / line 1589:**

| New target | Spec source | Proposed body |
|---|---|---|
| `reflect-eval` | spec line 691, 1509, 1589 | Full eval-suite: `cd .dev/eval-workspaces/sc-reflect-protocol && uv run python grader.py iterations/iteration-N && uv run python aggregate_iteration.py` (with iter resolution via env or default-to-latest). ~2 min target. |
| `reflect-eval-quick` | spec line 691, 1589 | 3 pilot cases only: `cd .dev/eval-workspaces/sc-reflect-protocol && SC_REFLECT_CASES=pilot uv run python grader.py iterations/iteration-N`. <30s target. |
| `sync-cost-profile` | spec line 1514 | Refresh `refs/cost-profile.yaml` from §15 table (build-time tooling; could be a manual script + verify step) |

**Verification recipe for new targets after addition:**

```bash
# 1. Verify target syntax (no errors)
make -n reflect-eval-quick
make -n reflect-eval

# 2. Verify body runs to completion
make eval-skill SKILL=sc-reflect-protocol  # bootstrap workspace
make reflect-eval-quick                    # should exit 0
```

---

## 7. Pre-commit config

**Path:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.pre-commit-config.yaml`

**Relevant hooks (in order of relevance to reflect):**

1. **`markdownlint`** (line 71-82) — runs `markdownlint --fix`. **EXCLUDES `\.dev/.*`** — so docs/specs/notes under `.dev/eval-workspaces/sc-reflect-protocol/` are EXEMPT. But `src/superclaude/skills/sc-reflect-protocol/SKILL.md` is NOT exempt and MUST pass markdownlint with the config at `.markdownlint.json`:

   ```json
   {"default": true, "MD013": false, "MD029": false, "MD036": false, "MD033": false}
   ```

   (Line length, ordered list numbering, emphasis-as-heading, inline HTML — all disabled.)
2. **`block-claude-generated-mirrors`** (line 102-109, AC11/R-017) — `scripts/precommit_block_claude_mirrors.sh` blocks staging of `.claude/{skills,agents,commands,hooks,templates}/`. **This is the safety net for the CLAUDE.md "never stage .claude/" rule.** Reflect's task MUST stage `src/superclaude/skills/sc-reflect-protocol/**` only, never `.claude/skills/sc-reflect-protocol/**`.
3. `check-yaml`, `check-json`, `check-toml`, `yamllint`, `shellcheck` — reflect's grader.py + new Makefile targets + new YAML refs must pass.
4. `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending` — bare-minimum hygiene.
5. `detect-secrets` (baseline `.secrets.baseline`) + hardcoded-secret grep — reflect docs must not include literal API keys (use placeholders like `${ANTHROPIC_API_KEY}`).
6. `conventional-pre-commit` (commit-msg stage) — `feat:`/`fix:`/`docs:`/`refactor:`/`test:`/`chore:` convention enforced on commits.

**No `verify-sync` pre-commit hook** — `verify-sync` runs in CI (see §8), not pre-commit. The pre-commit `block-claude-generated-mirrors` covers the staging side; CI catches full drift.

---

## 8. CI workflows

**Path:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.github/workflows/`

**Relevant workflows:**

- `quick-check.yml` — runs `make verify-sync` AND `make lint-architecture` on every push/PR
- `test.yml` — runs `make verify-deps` plus pytest/lint/plugin-check/doctor-check; gates overall success
- `publish-pypi.yml`, `pull-sync-framework.yml`, `readme-quality-check.yml` — unrelated

**No reflect-specific workflow today.** Spec line 1589 mandates `make reflect-eval-quick` on PRs touching `src/superclaude/skills/sc-reflect-protocol/` or `src/superclaude/commands/reflect.md`. This requires:

- Either a new workflow `reflect-eval.yml` with `paths:` triggers, OR
- Adding `make reflect-eval-quick` as a step to existing `quick-check.yml` guarded by a path filter

**Proposed workflow stub** (for spec §17.5 / line 1589 compliance):

```yaml
# .github/workflows/reflect-eval.yml
name: reflect-eval
on:
  pull_request:
    paths:
      - 'src/superclaude/skills/sc-reflect-protocol/**'
      - 'src/superclaude/commands/reflect.md'
      - '.dev/eval-workspaces/sc-reflect-protocol/**'
jobs:
  quick:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: make dev
      - run: make reflect-eval-quick
```

---

## 9. pyproject.toml — relevant fields for reflect

**Dependencies already present that reflect needs:**

- `pyyaml>=6.0` (line 38) — needed for reflect's `yaml_list_contains` (the simple parser in inherited grader.py is insufficient)
- `jsonschema>=4.0.0` (line 39) — usable for return-contract schema validation
- `pexpect>=4.9` (line 40) — for CLI subprocess testing

**Skill-creator dep NOT present in pyproject.toml.** Spec §13.1 (line 1090) says "skill-creator 2.0 ships out of the box (`run_loop.py`, `eval-viewer/generate_review.py`, comparator/grader/analyzer sub-agents)". This appears to be a CLAUDE-CODE-PLUGIN dependency (loaded via the `Skill` tool — see system-reminder listing `skill-creator:skill-creator`), NOT a Python package dep. **Reflect's task does not need to add `skill-creator` to pyproject.toml.**

**Ruff exclusions (line 182):**

```toml
extend-exclude = [
    ".dev/",
    "tests/audit/fixtures/syntax_error.py",
]
```

**Important:** `grader.py` and `aggregate_iteration.py` will live under `.dev/eval-workspaces/sc-reflect-protocol/` so they are **EXEMPT from ruff**. Reflect does not need to make them pass `make lint`. (Same applies to sc-brainstorm's existing grader.py — verified.)

**Pytest markers (line 111-135):** No reflect-specific markers exist. Reflect MAY add `@pytest.mark.reflect_eval` but spec does not require it.

---

## 10. VERIFICATION RECIPE TABLE (the deliverable)

| Build unit type | File / artifact | Verification command |
|---|---|---|
| **Reflect SKILL.md frontmatter** | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | `grep -E "^(name\|description\|allowed-tools):" src/superclaude/skills/sc-reflect-protocol/SKILL.md` then `make lint-architecture` (Check 8) |
| **Reflect SKILL.md size** | same | `wc -l src/superclaude/skills/sc-reflect-protocol/SKILL.md` — ideally <500 lines (Check 4 hard limit applies to commands but is the team norm for skills too) |
| **Reflect SKILL.md markdown** | same | `markdownlint src/superclaude/skills/sc-reflect-protocol/SKILL.md` (using `.markdownlint.json`) |
| **Reflect SKILL.md sync** | both src + .claude mirror | `make sync-dev && make verify-sync` (exits 0 only when matched) |
| **Each ref/*.md** | `src/superclaude/skills/sc-reflect-protocol/refs/*.md` | `markdownlint src/superclaude/skills/sc-reflect-protocol/refs/*.md` + spec-mention check: `grep -l "<ref-filename>" src/superclaude/skills/sc-reflect-protocol/SKILL.md` (each ref must be loaded by some wave per spec §16) |
| **YAML refs (cost-profile.yaml)** | `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` | `python -c "import yaml; yaml.safe_load(open('src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml'))"` |
| **Command file** | `src/superclaude/commands/reflect.md` | `make lint-architecture` (Checks 1, 6: paired skill exists + `## Activation` present) + `wc -l < src/superclaude/commands/reflect.md` ≤500 |
| **Bidirectional command↔skill link** | both | `make lint-architecture` (Checks 1+2 — both pass or fail together) |
| **Eval workspace dir** | `.dev/eval-workspaces/sc-reflect-protocol/` | `make eval-skill SKILL=sc-reflect-protocol` (creates + prints absolute path) |
| **grader.py (copy + extension)** | `.dev/eval-workspaces/sc-reflect-protocol/grader.py` | `uv run python -c "from pathlib import Path; import sys; sys.path.insert(0, '.dev/eval-workspaces/sc-reflect-protocol'); import grader"` (syntactic check). Then unit-test each new type by feeding a synthetic eval_metadata.json. |
| **grader.py functional** | per iteration dir | `uv run python .dev/eval-workspaces/sc-reflect-protocol/grader.py .dev/eval-workspaces/sc-reflect-protocol/iterations/iteration-1` |
| **aggregate_iteration.py** | `.dev/eval-workspaces/sc-reflect-protocol/aggregate_iteration.py` | `uv run python .dev/eval-workspaces/sc-reflect-protocol/aggregate_iteration.py` (writes benchmark.{json,md} + review.html) |
| **evals/evals.json** | `.dev/eval-workspaces/sc-reflect-protocol/evals/evals.json` | `python -c "import json; json.load(open('.dev/eval-workspaces/sc-reflect-protocol/evals/evals.json'))"` |
| **Per-case eval_metadata.json** | `.dev/eval-workspaces/sc-reflect-protocol/iterations/iteration-N/eval-<name>/eval_metadata.json` | `python -c "import json; m=json.load(open('<path>')); assert {'eval_id','eval_name','assertions'} <= m.keys()"` |
| **Fixtures (citation_resolves bait)** | `.dev/eval-workspaces/sc-reflect-protocol/evals/fixtures/<scenario>/...` | Files exist + `grader.py` `citation_resolves` returns expected results |
| **skill-snapshot baseline** | `.dev/eval-workspaces/sc-reflect-protocol/skill-snapshot/reflect-v1.md` | `test -s .dev/eval-workspaces/sc-reflect-protocol/skill-snapshot/reflect-v1.md` (non-empty) — should be a snapshot of the EXISTING `/sc:reflect` command for old_skill comparison |
| **`make reflect-eval-quick` (NEW)** | Makefile + workspace | Add target → `make -n reflect-eval-quick` (syntax check) → `make reflect-eval-quick` (must exit 0 with 3 pilot cases passing) |
| **`make reflect-eval` (NEW)** | Makefile + workspace | Add target → `make reflect-eval` (full case set, ~2 min, exit 0) |
| **CI cadence** | `.github/workflows/reflect-eval.yml` (NEW) | Push branch with reflect changes → workflow triggers → green status |
| **Pre-commit on commit** | global gate | `pre-commit run --files <staged paths>` — should NOT block on `.dev/eval-workspaces/sc-reflect-protocol/*.md` (markdownlint excludes `.dev/`); MUST block on any accidentally-staged `.claude/skills/sc-reflect-protocol/**` |
| **End-to-end ship gate** | all of above | `make sync-dev && make verify-sync && make lint && make lint-architecture && make test && make reflect-eval-quick` — all green |

---

## 11. Verification infrastructure that DOES NOT YET EXIST (must be built)

1. **`make reflect-eval-quick`** target — proposed body in §6 above. Spec line 1589 mandates this for PRs touching reflect.
2. **`make reflect-eval`** target — proposed body in §6 above. Spec line 691 references it as the full CI gate.
3. **`make sync-cost-profile`** target — spec line 1514 references this for keeping `refs/cost-profile.yaml` in lockstep with the §15 cost table. Optional unless the task takes on cost-profile maintenance.
4. **`.github/workflows/reflect-eval.yml`** — proposed stub in §8 above. Without it, CI cadence per spec §17.5 / line 1589 cannot be enforced mechanically.
5. **`refs/grader-extensions.md`** — Python sketch + docs for the 6 semantic types + 2 new `path_exists`/`path_does_not_exist` types. Per spec §11 and §17.5.
6. **PyYAML usage in grader.py** — sc-brainstorm's `parse_yaml_simple` is flat-key only; reflect's `yaml_list_contains` requires `import yaml; yaml.safe_load(...)`. PyYAML is already in `pyproject.toml` deps, so importable.
7. **`skill-snapshot/reflect-v1.md`** — must be captured from the current `/sc:reflect` command file (`src/superclaude/commands/reflect.md` as it stands BEFORE the rewrite) before the task begins, so the eval can compare `old_skill` (v1) vs `with_skill` (v2 sc-reflect-protocol).

---

## Summary

**Verification infrastructure present and ready:**

- `make sync-dev` / `make verify-sync` (handle the `src/` ↔ `.claude/` round-trip for new skill dir)
- `make lint-architecture` (enforces command↔skill pairing, frontmatter completeness, `-protocol` suffix — reflect must pass Checks 1, 6, 8, 9)
- `make eval-skill SKILL=sc-reflect-protocol` (bootstraps `.dev/eval-workspaces/sc-reflect-protocol/`)
- sc-brainstorm's `grader.py` (279 lines) is **copy-verbatim ready**; extend `check_assertion()` switch with 6 semantic + 2 path types
- sc-brainstorm's `aggregate_iteration.py` (163 lines) is **copy-verbatim ready**; change `skill_name` constant only
- Pre-commit `block-claude-generated-mirrors` enforces "never stage .claude/" — protects reflect's task from CLAUDE.md violation
- Pre-commit `markdownlint` EXCLUDES `.dev/` — so eval-workspace docs are unconstrained
- `pyproject.toml` has `pyyaml`, `jsonschema`, `pexpect` already

**Must-build infrastructure:**

- 2-3 new Makefile targets (`reflect-eval`, `reflect-eval-quick`, optionally `sync-cost-profile`)
- 1 new CI workflow (`.github/workflows/reflect-eval.yml`)
- 2 new grader assertion types in `check_assertion()` (`path_exists`, `path_does_not_exist`) per §14.5.7
- 6 new semantic grader types per `refs/grader-extensions.md` (`citation_resolves`, `regex_present`/`absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged`, `deviation_class_matches`)
- skill-snapshot baseline (`reflect-v1.md`) captured before the rewrite

**Risk note:** `skill-creator 2.0` (spec §13.1) is a CLAUDE-CODE PLUGIN skill (confirmed in the available-skills system-reminder), not a pip dependency. Reflect does NOT need to add it to `pyproject.toml`. The skill-creator workflow runs in the Claude Code session.

**sc-brainstorm `grader.py` answer (open question from prompt):** **COPY VERBATIM, then extend.** The 8 existing types are skill-agnostic; the runner logic (`grade_eval`, `main`, `build_grading`) needs no adaptation; the partition routing (`with_skill/old_skill` target prefixes) is generic and exactly what reflect needs. Only `check_assertion()`'s if-chain grows. The flat `parse_yaml_simple` parser may need to be replaced with `yaml.safe_load` (PyYAML) to support `yaml_list_contains` over nested YAML structures.
