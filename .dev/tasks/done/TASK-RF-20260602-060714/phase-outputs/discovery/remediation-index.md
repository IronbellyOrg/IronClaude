# Remediation Index — R1-R5 Acceptance Criteria + Parent Test Baseline

**Source:** `.dev/reviews/PR-112-111-remediation-design.md`
**Captured:** 2026-06-02 06:52

## Findings & Acceptance Criteria (quoted from the design doc)

### R1 — [NIT] Stale docstring in `id_registry.py`
- **Site:** `src/superclaude/cli/roadmap/id_registry.py:22-24` (says R0.3 "will hoist … TODO comment below" but the import already shipped at L37).
- **Acceptance:** docstring contains no future-tense "will hoist" / "TODO below"; `grep -n "will hoist\|TODO comment below" src/superclaude/cli/roadmap/id_registry.py` returns nothing. `uv run pytest -k id_registry` still green. Comment-only, no behavior change.

### R2 — [LOW-MED] Reset/validate `_id_registry_sidecar_path` global
- **Site:** `gates.py:1039` global; reset belongs in `executor.py::execute_roadmap` (after dry-run guard, before execute_pipeline).
- **Acceptance:** resume-aware reset (must NOT fail-shut MERGE on legitimate `--resume`); preserve fail-shut at `gates.py:1069-1074` exactly; do NOT change the `Callable[[str],bool|str]` signature (deferred to R1.3). New single-test-body regression: two sequential `_roadmap_ids_within_spec` runs in ONE test body where run 2 skips extract → returns fail-shut string (not stale pass). Existing Contract #9 fixtures stay green.

### R3 — [NIT/optional, droppable] arch_lint Rule 2 docstring hardening
- **Site:** `src/superclaude/tools/arch_lint.py:168-185` (flat `ast.walk`, parent-blind).
- **Acceptance:** skip docstring Constant nodes before membership check via precomputed id()-set; `make lint-architecture` still exits 0; new test: docstring with verbatim ID_PATTERNS body → no `literal-duplicate`; real top-level literal of same body → still flagged. OPTIONAL — droppable if scope shrinks.

### R4 — [LOW] `apply_scope()` grep exit-2 masking in `repo-inventory.sh`
- **Site:** `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh:29-37` (`|| true` on both grep branches; `#!/bin/sh` + `set -e`, POSIX no pipefail).
- **Acceptance:** distinguish exit-1 (ok) from exit-2 (fatal); malformed `EXCLUDE:` regex → exit non-zero with diagnostic naming SCOPE.md (NOT "Total files: 0" exit 0); valid empty match still exit 0. set-e-safe `if FILE_LIST=$(…); then :; else …` guarding at both callers (L49, L66). Then `make sync-dev` + `make verify-sync`; stage ONLY src/ side, NEVER `.claude/`.

### R5 — [MEDIUM] Milestone `M{n}-D{nn}` ID handling — investigation+decision gate
- **Proven FP:** `\bD-?\d+\b` extracts `D01` from `M1-D01`. Branch has no MD family in `contracts.ID_PATTERNS` (FR/NFR/SC/G/D only), no canonicalizer, no allowlist.
- **Acceptance (a CLOSE):** fixture shows 0 FP on `M{n}-D{nn}`; record evidence; recommend closing PR #111 as superseded; Phase 4 skipped.
- **Acceptance (b PROCEED):** FP reproduces → add MD body to `contracts.ID_PATTERNS` (anchor-free, SoT — never inline); thread `md_ids` across SpecIdRegistry field + union_of_known + to_dict + build_id_registry + gates sidecar read + envelope.py + test_pipeline_envelope.py (R1.2 sites) + schema tests + conftest; port PR #111's 3 oracle tests (`git show 861047c2 -- tests/roadmap/test_structural_checkers.py`) + disk-backed fixture; `M{n}-D{nn}` fixture yields 0 phantom_id/id_schema_drift; `make lint-architecture` exits 0; Contract #9 sidecar round-trips `md_ids`.

## Final-Validation Acceptance (all findings)
`make lint-architecture` exits 0; `make verify-sync` passes; targeted `uv run pytest` per surface passes; full-suite pass/fail delta vs baseline unchanged (no NEW failures); branch/remote hygiene confirmed; NEVER stage `.claude/`.

## Parent Test Baseline

**Full-suite (`uv run pytest -q tests/`):** BLOCKED by a **pre-existing, unrelated** collection error — `tests/sprint/test_summarizer.py` and `tests/sprint/test_retrospective.py` fail to collect with `ImportError: cannot import name 'invoke_haiku' from 'superclaude.cli.sprint.summarizer'`. This is in the `sprint` subsystem, entirely outside the R1-R5 (roadmap/contracts/tools) scope, and predates this task. Verbatim tail:
```
ERROR tests/sprint/test_retrospective.py
ERROR tests/sprint/test_summarizer.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
========================= 1 skipped, 2 errors in 4.57s =========================
```

**Targeted baseline (the actual R1-R5 surfaces — `uv run pytest -q tests/roadmap/ tests/contracts/`):**
```
======================= 1963 passed, 12 skipped in 7.83s =======================
```
**→ Delta target for Phase 6: `1963 passed, 12 skipped` on `tests/roadmap/ tests/contracts/` must be preserved (new tests add to the passed count; ZERO new failures). The unrelated sprint collection error is out of scope and must not be "fixed" by this task.**
