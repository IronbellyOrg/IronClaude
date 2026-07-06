# R4 — Test Infrastructure + Deterministic-Core Architecture

Status: Complete

Research topic: How skill behaviors are actually tested in this repo, AND resolve
the pivotal architecture question — does the deterministic core (FSM, severity
router, loop-guard, classifier) need to be a real, importable Python module that
the spec's tests import, or can it remain pure-markdown + bash with tests over the
scripts only?

---

## ★ ARCHITECTURE RECOMMENDATION (LEAD)

**The deterministic core MUST be a real, importable Python package.** The spec's
own test bodies are dispositive: they call `run_skill(...)` and assert on a
returned **object's attributes** (`result.round_counter`, `result.push_count`,
`result.reply_count`, `result.summary_posted`, `result.state`), and they call
free functions `remap_severity(finding).remapped_severity`,
`poll_augment_review(pr_num=42) == "polling"`, `classify(...)`, plus a
`third_fix_not_applied(result)` helper (merged-spec.md:649, 882, 912-944). These
are in-process Python calls returning typed values — they cannot be satisfied by a
markdown ref or by a bash subprocess that only emits text.

**Recommended location** (matches existing repo precedent — see §B):

```
src/superclaude/submit_pr/                 # importable pkg: superclaude.submit_pr
├── __init__.py
├── fsm.py            # FSM states (S0..S7 / HALT_*), transition fn, `run_skill()` driver returning a SkillResult dataclass
├── severity.py       # remap_severity(finding) -> Finding(.remapped_severity), routing table
├── loop_guard.py     # round_counter, attributed-re-review fence-post (INV-001), HALT_MAX_ROUNDS gate
├── classifier.py     # classify(...) — finding/autonomy classification
├── detection.py      # poll_augment_review(pr_num) -> state string ("polling"/...)
├── models.py         # SkillResult dataclass (round_counter/push_count/reply_count/summary_posted/state), Finding, enums
└── run_log.py        # JSONL observability (T-N20..N22)
```

**Why `src/superclaude/submit_pr/` and NOT `src/superclaude/skills/sc-submit-pr-protocol/`:**
The skill directory name is **hyphenated** (`sc-submit-pr-protocol`), and a
hyphen is not a legal Python identifier. `import
superclaude.skills.sc-submit-pr-protocol` is a **syntax error**; even
`importlib.import_module("superclaude.skills.sc-submit-pr-protocol")` fails to
resolve as a normal dotted module. Verified live:
`python3 -c "import superclaude.skills.confidence_check"` → ImportError (the dir
is `confidence-check`, hyphen). The repo's existing importable subsystems all use
**underscored** package dirs (`cli/recommend/`, `cli/swarm/`, `cli/cli_portify/`,
`pm_agent/`, `execution/`). The deterministic core should follow that convention.

The hyphenated `src/superclaude/skills/sc-submit-pr-protocol/` remains the **skill
package** (SKILL.md + refs/ + rules/ + scripts/ bash wrappers + the markdown that
the orchestrating LLM reads). The Python core lives in the underscored sibling
package and is imported by both the bash glue (via `uv run python -m
superclaude.submit_pr...` if needed) and the tests.

**Spec defect to flag for the task-builder:** §`merged-spec.md:1025` specifies
`uv run pytest tests/submit_pr/ -v --cov=superclaude.skills.sc-submit-pr-protocol`.
That `--cov` target is **not a resolvable module path** (hyphens). It must become
`--cov=superclaude.submit_pr`. (Coverage's `--cov` accepts a path OR a dotted
module; a path like `src/superclaude/skills/sc-submit-pr-protocol` would measure
markdown+bash, which `coverage.py` cannot instrument — only `.py` files are
covered. So the cov target only produces meaningful numbers against the
underscored Python pkg.)

---

## A. How skill/CLI behaviors are tested in this repo — THREE distinct patterns

There are exactly three test idioms, and the choice depends on whether the unit
under test is Python, bash, or markdown:

### Pattern 1 — Direct module import (for real Python packages)
Used by every CLI subsystem. Tests `import superclaude.cli.<pkg>.<mod>` directly.
- `tests/cli_portify/test_cli.py:18` → `from superclaude.cli.cli_portify.commands import cli_portify_group`
- `tests/cli_portify/test_models.py:19-20` → `from superclaude.cli.cli_portify.convergence import ConvergenceState`
- `tests/recommend/test_dispatch.py:17` → `from superclaude.cli.recommend.dispatch import dispatch`
- `tests/recommend/test_cli_registration.py:8` → `from superclaude.cli.main import main`
- `tests/sprint/...`, `tests/swarm/test_recipe_bare_review.py:40-43` → `from superclaude.cli.swarm.{models,normalize,recipes...} import ...`

This is the pattern the submit-pr deterministic core needs.

### Pattern 2 — `importlib.util.spec_from_file_location` (for Python shipped INSIDE a hyphenated skill dir)
**This is the closest existing precedent to the spec's situation** and the proof
that skills *can* ship Python logic. `sc-bare-review/scripts/t2_normalize.py` is
loaded by file path because its skill dir is hyphenated and has no `__init__.py`:
- `tests/swarm/test_bare_review_parity.py:56-58, 234-240`:
  ```python
  spec = importlib.util.spec_from_file_location(
      "t2_normalize_legacy_for_parity_t0811", str(LEGACY_SCRIPT))
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module  # then module.main(...) in-process
  ```
  `LEGACY_SCRIPT = src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
  (test_bare_review_parity.py:110-119).
- Comment at test_bare_review_parity.py:56-58 explicitly notes: *"no `__init__.py`
  in `.../sc-bare-review/scripts/`"* — so it can't be a normal import.

Precedent for **shipping Python in a skill**: confirmed.
- `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
- `src/superclaude/skills/sc-crash-recovery/scripts/parse_session_log.py`

BUT this importlib pattern is awkward for a 7-module deterministic core with
cross-imports, and `coverage.py` does not cleanly instrument file-path-loaded
modules under the `--cov=<dotted-module>` form. Hence Pattern 1 (real underscored
package) is the right call for submit-pr, with the hyphenated skill dir holding
only SKILL.md + bash wrappers.

### Pattern 3a — subprocess over a shell SCRIPT (for bash skill logic)
- `tests/skills/test_repo_inventory_nongit.py:36-42`:
  ```python
  subprocess.run(["sh", str(SCRIPT), target], cwd=cwd, capture_output=True, text=True)
  ```
  `SCRIPT = src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`
  Tests parse stdout (`re.search(r"Total files:\s+(\d+)", stdout)`).

### Pattern 3b — markdown text-assertion (for SKILL.md / agent contracts)
- `tests/skills/test_task_builder_merge.py:21-52`: reads `SKILL.md` /
  `agents/rf-qa.md` as text and asserts substrings/section counts
  (`assert "#### Checklist (27 items)" in rf_qa_text`,
  `assert "TB-Add-3" in rf_qa_text`).

**Mapping to submit-pr:** The spec needs ALL THREE — Pattern 1 for the
deterministic core (FSM/router/loop-guard/classifier), Pattern 3a/subprocess +
mock for the `gh`/bash glue (T-104/T-105 static grep, T-N40/N41 core-purity), and
Pattern 3b text-assert for SKILL.md/hook contract checks (T-104 grep for `gh`
without `--repo`, T-701..703 hook update).

---

## B. Precedent: does a skill have a backing Python module? — YES (partial)

- Skills DO ship Python today: `t2_normalize.py`, `parse_session_log.py` (§A
  Pattern 2). So "a skill having Python logic" is established and accepted.
- HOWEVER no skill yet has a *full importable underscored Python package as its
  deterministic core*. The submit-pr core would be the first to formalize the
  cleaner Pattern-1 layout (`src/superclaude/submit_pr/`). This is consistent with
  — not a departure from — how `cli/swarm/` grew (swarm has both a skill
  `sc-bare-review` AND an importable `superclaude.cli.swarm` package; the parity
  test bridges them). Submit-pr should mirror that swarm split:
  - hyphenated skill dir `skills/sc-submit-pr-protocol/` = LLM-facing markdown + bash
  - underscored Python pkg `superclaude.submit_pr` = deterministic, unit-tested core

- `[tool.coverage.run] source = ["src/superclaude"]` (pyproject.toml:142-143) — the
  whole tree is the coverage source, so a new `src/superclaude/submit_pr/` is
  covered automatically; the `--cov=superclaude.submit_pr` narrows the report.

---

## C. The 21 test files → module mapping

Spec test layout at merged-spec.md:427-470. Map each test file to the core
module(s) it exercises (Pattern 1 unless noted):

| Test file | Primary module(s) imported | Pattern |
|---|---|---|
| `test_skill_parse.py` | `submit_pr.fsm` (arg parse / `run_skill` flags, resume) | 1 |
| `test_pre_pr_checks.py` | `submit_pr.fsm` + mock_gh (origin/rebase/URL) | 1+mock |
| `test_monitor_arm.py` | `submit_pr.fsm`, `submit_pr.detection` | 1 |
| `test_detection_contract.py` | `submit_pr.detection` (`poll_augment_review`) | 1 |
| `test_timeout.py` | `submit_pr.detection` (interval/backoff) | 1 |
| `test_severity_router.py` | `submit_pr.severity` (`remap_severity`) | 1 |
| `test_finding_verify.py` | `submit_pr.fsm`/`classifier` (verify-before-remediate) | 1+mock |
| `test_troubleshoot_seed.py` | `submit_pr.fsm` (seed/batch troubleshoot) | 1+mock |
| `test_autonomy_gates.py` | `submit_pr.classifier`/`fsm` (autonomy, ZERO-EDIT-NO-PUSH) | 1 |
| `test_validation_gate.py` | `submit_pr.fsm` (validation gate) | 1 |
| `test_loop_guard.py` | `submit_pr.loop_guard` (round_counter, off-by-one) | 1 |
| `test_reply_resolve.py` | `submit_pr.fsm`/reply (suggestion-block, summary) | 1+mock |
| `test_idempotency.py` | `submit_pr.run_log`/reply (no double-post) | 1+mock |
| `test_rate_limit.py` | gh-call wrapper (403 backoff) | 1+mock |
| `test_run_log.py` | `submit_pr.run_log` (JSONL) | 1 |
| `test_crash_recovery.py` | `submit_pr.fsm` resume + `run_log` reconstruction | 1+mock |
| `test_edge_cases.py` | mixed core modules (EC-1..16) | 1+mock |
| `test_hook_update.py` | hook contract (text-assert/subprocess) | 3a/3b |
| `test_static_grep.py` | grep over `skills/.../` + `hooks/` sources | 3b |
| `test_validated_not_verified.py` | `submit_pr.fsm`/classifier (INV-015 audit) | 1 |
| (+ `conftest.py`, `__init__.py`, `fixtures/`) | — | — |

`run_skill()` is the single integration driver living in `submit_pr/fsm.py`
(or a `submit_pr/__init__.py` re-export) returning a `SkillResult` dataclass from
`submit_pr/models.py`. Free functions `remap_severity`, `poll_augment_review`,
`classify` are imported from their respective modules and re-exported at package
top-level so test bodies can `from superclaude.submit_pr import run_skill,
remap_severity, poll_augment_review, classify, load_fixture`.

---

## D. conftest / fixture patterns to reuse

The spec's `tests/submit_pr/conftest.py` needs `mock_gh`, `mock_monitor`,
`fixture_findings`, `tmp_skill_dir`, `mock_skill_env`, `load_fixture`. Existing
patterns to copy:

- **`tmp_path` + monkeypatch.setenv** — pervasive; e.g. tests/conftest.py:82-117
  `_redirect_reflexion_writes` uses `monkeypatch.setenv` + `tmp_path`. Use the same
  for `tmp_skill_dir` and any env the gh wrapper reads.
- **subprocess mocking / fake `gh`** — for `mock_gh`, either (a) monkeypatch the
  thin gh wrapper function in `submit_pr` (preferred — keeps tests in-process and
  fast, mirrors recommend/swarm), or (b) put a fake `gh` on PATH via `tmp_path`
  bin dir for the subprocess/static-grep tests. The repo favors (a) for unit
  speed; reserve (b) for `test_static_grep.py` / integration.
- **module-scoped text fixtures** — tests/skills/test_task_builder_merge.py:30-53
  shows `@pytest.fixture(scope="module")` returning `PATH.read_text()`; reuse for
  SKILL.md/hook text-assert tests.
- **fixture corpus dir** — tests/swarm/test_bare_review_parity.py:108
  `FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"`; mirror as
  `tests/submit_pr/fixtures/` (spec already lists the JSON fixtures). `load_fixture`
  = `json.loads((FIXTURES_DIR / name).read_text())`.
- **REPO_ROOT anchor** — `Path(__file__).resolve().parents[2]` (used in
  test_task_builder_merge.py:20 and test_bare_review_parity.py:109) to locate
  `src/superclaude/skills/...` for static-grep tests.

---

## E. Pytest marker registration — REQUIRED action (else --strict-markers fails)

`pyproject.toml:107-110` sets `addopts = ["-v", "--strict-markers", "--tb=short"]`.
With `--strict-markers`, **any unregistered marker is a hard collection error**.
All markers live in `[tool.pytest.ini_options] markers = [...]`
(pyproject.toml:114-139). Current list (verified) registers: unit, integration,
hallucination, performance, slow, confidence_check, self_check, reflexion,
complexity, diagnostic, diagnostic_l0..l3, diagnostic_negative, e2e_trailing,
backward_compat, property_based, nfr_benchmark, gate_performance,
context_injection_test, thread_safety, agent_regression, imm, inv.

**The spec adds markers `loop_guard`, `autonomy`, `recovery`, `p0`, `loop`
(R4 brief) — NONE are registered.** The task-builder MUST add these to the
`markers` list in pyproject.toml `[tool.pytest.ini_options]`, e.g.:

```toml
    "loop_guard: Loop-guard / round-counter fence-post tests (INV-001)",
    "autonomy: Autonomy-tier gate tests (zero-edit-no-push, etc.)",
    "recovery: Crash-recovery / resume reconstruction tests (FM-1..12)",
    "p0: P0 priority acceptance tests",
    "loop: FSM loop / re-review cycle tests",
```

There is no second marker registry (no `pytest.ini`, no `setup.cfg`
`[tool:pytest]`, no `conftest.py` `pytest_configure(config.addinivalue_line(...))`
for markers) — `pyproject.toml` is the single source. Confirmed by grepping; the
only marker config is the pyproject block.

(Note: `unit`/`integration` are ALSO auto-applied by directory per CLAUDE.md
"Auto-markers" — but they are still explicitly registered in pyproject, so the new
markers must be too; directory-autouse does not bypass `--strict-markers`.)

---

## F. Coverage config

- `[tool.coverage.run] source = ["src/superclaude"]`, omit `*/tests/*`,
  `*/test_*`, `*/__pycache__/*`, `*/.*` (pyproject.toml:142-148).
- `[tool.coverage.report]` has `show_missing = true` and standard `exclude_lines`
  (pyproject.toml:151-166).
- `pytest-cov>=4.0.0` is in `[project.optional-dependencies] dev` and `test`
  (pyproject.toml).
- **Coverage only instruments `.py`** — markdown/bash skill assets are invisible to
  `coverage.py`. This is the structural reason the deterministic core MUST be
  Python for the spec's `--cov` line (1025) to mean anything. Corrected target:
  `--cov=superclaude.submit_pr`.

---

## G. Banned-import landmine (do not trip)

`pyproject.toml:[tool.ruff.lint.flake8-tidy-imports.banned-api]` (FR-G1) **bans any
`import anthropic`** repo-wide. The submit-pr core must NOT import the anthropic
SDK; LLM-shaped steps (troubleshoot seeding, finding verify) are driven via the
real `claude` subprocess or mocked in tests, never an in-process SDK call. Tests
for those paths use `mock`/monkeypatch, not a live SDK.

---

## SUMMARY

1. **DECISION: the deterministic core must be a real importable Python package** —
   `src/superclaude/submit_pr/` (underscored), because the spec's test bodies call
   `run_skill(...)` and assert on returned-object attributes + free functions
   (`remap_severity`, `poll_augment_review`, `classify`) — pure in-process Python
   contracts (merged-spec.md:649,882,912-944).
2. **Hyphen defect:** `--cov=superclaude.skills.sc-submit-pr-protocol`
   (merged-spec.md:1025) is unresolvable (hyphens ≠ Python identifiers; verified).
   Use `--cov=superclaude.submit_pr`. Skill dir stays hyphenated for markdown+bash;
   Python core lives in the underscored sibling pkg — mirrors the existing
   `sc-bare-review` skill ↔ `superclaude.cli.swarm` split.
3. **Three test idioms exist** (module-import / importlib-file-load /
   subprocess+text-assert); submit-pr uses module-import (Pattern 1) for the core,
   subprocess/grep (3a/3b) for gh-glue + SKILL.md/hook contracts.
4. **Precedent confirmed:** skills already ship Python (`t2_normalize.py`,
   `parse_session_log.py`), loaded via `importlib.util.spec_from_file_location`
   (tests/swarm/test_bare_review_parity.py:234-240).
5. **Markers `loop_guard/autonomy/recovery/p0/loop` are UNregistered** — must be
   added to `pyproject.toml [tool.pytest.ini_options] markers` or `--strict-markers`
   (addopts, pyproject.toml:108) fails collection. pyproject is the single marker
   registry.
6. **Coverage** source already `src/superclaude` (covers the new pkg
   automatically); `pytest-cov` is a declared dev/test dep; coverage only sees
   `.py` (reinforces #1). Do not import `anthropic` (FR-G1 ruff ban).

Key files cited: pyproject.toml:107-166 (addopts/markers/coverage/ruff-ban);
tests/conftest.py:82-117 (tmp_path+monkeypatch fixture pattern);
tests/cli_portify/test_cli.py:18 + tests/recommend/test_dispatch.py:17 (Pattern 1
imports); tests/swarm/test_bare_review_parity.py:56-58,110-119,234-240 (Pattern 2
importlib + skill-ships-Python precedent); tests/skills/test_repo_inventory_nongit.py:36-42
(Pattern 3a subprocess); tests/skills/test_task_builder_merge.py:30-53 (Pattern 3b
text-assert); merged-spec.md:427-470 (test layout), :649/:882/:912-944 (Python test
bodies), :1025 (broken --cov path).
