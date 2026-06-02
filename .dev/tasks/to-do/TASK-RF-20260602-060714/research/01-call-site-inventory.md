# Research: File Inventory + Call-Site/Data-Flow Tracer

- **Topic:** Exact edit sites for remediation items R1–R5 and the R5 blast radius
- **Scope:** Precise file:line edit sites + data-flow tracing only (NOT patterns/tests/MDTM template)
- **Track goal:** Remediate validated PR #112 + #111 review findings (see `.dev/reviews/PR-112-111-remediation-design.md`)
- **Status:** Complete
- **Date:** 2026-06-02

---

## R1 — Stale "future work" docstring in `id_registry.py`

**File:** `src/superclaude/cli/roadmap/id_registry.py`

**Exact current text to replace (L19-24), verbatim from Read:**
> **Anti-duplication discipline (Contract #8):** This module does NOT
> re-implement any ID pattern. It REUSES
> :func:`superclaude.cli.roadmap.spec_parser.extract_requirement_ids` as the
> single source of truth for ID regex literals. R0.3 will hoist the patterns
> to ``superclaude.contracts.ID_PATTERNS``; the TODO comment below tracks
> that migration.

The self-contradicting clause is L22-24: `"R0.3 will hoist the patterns to ``superclaude.contracts.ID_PATTERNS``; the TODO comment below tracks that migration."`

**Contradicted by:** L37 `from superclaude.contracts import ID_PATTERNS as _ID_PATTERNS` — the migration already shipped. There is NO remaining "TODO comment below"; instead L33-37 is a present-tense comment ("R0.3: source the family list from the canonical contracts registry … Contract #8 satisfied — no duplicate literal definition.").

**Precise edit (1 Edit):** Replace the L22-24 future-tense sentence. The replaceable unit is "R0.3 will hoist the patterns to ``superclaude.contracts.ID_PATTERNS``; the TODO comment below tracks that migration." Design-doc suggested replacement:
> "R0.3 hoisted the family patterns to `superclaude.contracts.ID_PATTERNS`; this module now sources the known-family list from there (see import below). Contract #8 satisfied — no duplicate literal definition."

Note: L20-22 ("It REUSES `extract_requirement_ids` as the single source of truth for ID regex literals") is still true (the *literals* live in spec_parser's `_REQUIREMENT_PATTERNS`; contracts is the *family-name* SoT) — minimal edit only touches the L22-24 future-tense clause; need not rewrite the REUSE sentence. **Acceptance grep:** `grep -n "will hoist\|TODO comment below" id_registry.py` → empty.

**Scope:** comment-only, no behavior change, no other call sites. `_ID_PATTERN_KEYS` (L39) and the dataclass below are unaffected.

---

## R2 — Reset/validate `_id_registry_sidecar_path` global

### gates.py side (CONFIRMED verbatim)

**File:** `src/superclaude/cli/roadmap/gates.py`

- L1039: `_id_registry_sidecar_path: Path | None = None` — module-level global.
- L1042-1049: `def set_id_registry_sidecar_path(path: Path | None) -> None:` — sets the global; docstring says `"None`` clears the hint (used by tests for isolation)."` So a `None`-reset path already exists and is documented.
- L1052-1074: `def _roadmap_ids_within_spec(content: str) -> bool | str:` — the Contract #9 MERGE-gate SemanticCheck. **Fail-shut at L1069-1074:** `if _id_registry_sidecar_path is None: return ("Contract #9: spec_id_registry.json sidecar path was not registered…")`. Only fail-shut branch keyed on the global being `None`.
- Signature is `Callable[[str], bool | str]` (content-only) — R0.1 bridge comment L1028-1037 says R1.3 will widen it to take an envelope. **Do NOT change this signature (deferred to R1.3 per design doc).**
- Sidecar JSON keys read at L1089-1099: `fr_ids, nfr_ids, sc_ids, g_ids, d_ids, accepted_deviation_ids, spec_hash, spec_path` (all via `payload.get(...)`).

### executor.py side — set call + the PIPELINE-RUN ENTRY function

**File:** `src/superclaude/cli/roadmap/executor.py`

- `_save_id_registry(spec_file, output_dir)` defined at **L612**; writes sidecar at `<output_dir>/spec_id_registry.json` (L651), then calls `set_id_registry_sidecar_path(sidecar)` at **L664** (import at L662). CONFIRMED.
- `_save_id_registry` is **called at L1365**, inside `_roadmap_run_step_impl` (per-step impl, def at **L1021**), guarded by `if step.id == "extract" and step.output_file.exists():` (L1350) plus `if hasattr(config, "spec_file") and hasattr(config, "output_dir"):` (L1363). So the sidecar path is ONLY ever set during the extract step; never reset.

**The PIPELINE-RUN ENTRY function = `execute_roadmap(config, resume, no_validate, ...)` at L3397** (executor.py). Top-level run function. It:
- mkdir output_dir (L3425), restores resume state (L3428-3433), routes inputs (L3451), builds steps `steps = _build_steps(config)` at **L3487**, dry-run early-return at **L3490-3492** (`if config.dry_run: _dry_run_output(steps); return`), wires the cosmetic remediator (L3504-3534), then calls `execute_pipeline(steps=steps, config=config, run_step=roadmap_run_step, ...)` at **L3536-3543**.
- `execute_pipeline` itself lives in `src/superclaude/cli/pipeline/executor.py:63` (generic; not roadmap-specific) — drives the steps, where extract eventually runs `roadmap_run_step` → `_roadmap_run_step_impl` → `_save_id_registry`.

**Precise insertion point for `set_id_registry_sidecar_path(None)` reset-at-run-start (BEFORE extract runs):**
Insert in `execute_roadmap`, **after the dry-run early-return guard (L3492) and before `execute_pipeline()` is called (L3537)** — e.g. immediately before the `# Execute pipeline` comment at L3536. It MUST be after the `if config.dry_run: … return` guard so dry-run (which skips extract + sub-skills entirely) isn't disturbed. Requires `from .gates import set_id_registry_sidecar_path` (same import pattern already at executor.py L662).

**Optional path-identity guard scope:** `config.output_dir` IS in scope throughout `execute_roadmap` (used at L3425, L3478). The sidecar is always written at `config.output_dir / "spec_id_registry.json"` (executor L651), so a path-identity check would compare `_id_registry_sidecar_path.parent` against the run's `output_dir`. Design doc: implement reset (1) at minimum; path-identity (2) preferred but can be R1.3 follow-up.

**Resume caveat (data-flow, LIVE CONSTRAINT):** `execute_roadmap` with `resume=True` calls `_apply_resume` (L3498) which may skip already-passing steps — including extract — so on resume the sidecar-set never re-runs. A blind unconditional `set_id_registry_sidecar_path(None)` at run-start would then fail-shut MERGE on resume. The reset must be reconciled with resume: either (a) only reset when extract will actually run, or (b) on resume re-derive the sidecar from an existing `<output_dir>/spec_id_registry.json` if present. The existing extraction.json/sidecar derivation logic at L1273-1279 is the precedent. **Flagged for task author.**

---

## R3 — Harden `arch_lint` Rule 2 against docstring false-positives

**File:** `src/superclaude/tools/arch_lint.py`

**Walker structure (CONFIRMED):** Inside a function (def at L120 returning `list[Violation]`):
- L137: `tree = ast.parse(source, filename=str(path))` — `tree` holds the parsed Module.
- L143: `for node in ast.walk(tree):` — **flat `ast.walk`, NOT a NodeVisitor**. Single loop over all nodes; no parent pointers available.
- Rule 1 (L144-166): Assign/AnnAssign name-rebind.
- **Rule 2 (L168-185):** `if isinstance(node, ast.Constant) and isinstance(node.value, str):` (L169) then `if node.value in canonical_pattern_bodies:` (L170, exact set-membership CONFIRMED), with allow-marker opt-out via `_line_has_allow_marker(source_lines, node.lineno)` at L171.
- Rule 3 (L187-204): ClassDef name-shadow.

**Docstring-detection design constraint:** Because `ast.walk` flattens the tree, a Constant node has no parent reference at iteration time. To skip docstrings, pre-compute the set of docstring `ast.Constant` node `id()`s in a separate pass BEFORE the `ast.walk` loop. A docstring is the `.value` of the first `Expr` statement in the `.body` of a `Module` / `ClassDef` / `FunctionDef` / `AsyncFunctionDef`, where that value is an `ast.Constant` str. Two viable approaches:
1. Walk the tree once collecting `id(n.body[0].value)` for each container node whose `body[0]` is `ast.Expr` wrapping a str `ast.Constant` (covers Module/ClassDef/FunctionDef/AsyncFunctionDef).
2. Use `ast.get_docstring(node, clean=False)` per container — but that returns the string value, not the node, so the id()-set approach (1) is more precise for matching the specific Constant node in the walk.

Then in Rule 2, add `if id(node) in docstring_node_ids: continue` before the membership test (L170). Leave Rules 1 and 3 untouched. The existing allow-marker opt-out stays as the escape hatch for genuine non-docstring literals. **Walker currently returns 0 violations** — change must be behavior-preserving for current inputs.

---

## R4 — `apply_scope()` must not mask grep exit-2 in `repo-inventory.sh`

**File:** `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`

**Confirmed facts:**
- Shebang L1: `#!/bin/sh` (POSIX sh). `set -e` ACTIVE at L9.
- `EXTRA_EXCLUDES` built at L23-27 from `EXCLUDE:` lines in `$SCOPE_FILE`, joined with `|` via `paste -sd'|'`. A malformed EXCLUDE line → invalid combined ERE.
- **`apply_scope()` L29-37 (verbatim):**
  ```sh
  apply_scope() {
      # Filter stdin through default + per-project regex exclusions.
      # `|| true` guards against grep's exit-1 on empty input under `set -e`.
      if [ -n "$EXTRA_EXCLUDES" ]; then
          grep -E -v "($DEFAULT_EXCLUDES|$EXTRA_EXCLUDES)" || true
      else
          grep -E -v "$DEFAULT_EXCLUDES" || true
      fi
  }
  ```
  The `|| true` on BOTH branches (L33, L35) swallows grep exit-2 (invalid ERE) as well as exit-1.
- **Caller site 1 (git path), L49:** `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null | apply_scope)`
- **Caller site 2 (find fallback), L66:** `... 2>/dev/null | sed 's|^\./||' | apply_scope)` (end of the `find` pipeline L51-67).

**grep exit-code semantics needed (POSIX):** exit 0 = ≥1 line matched/kept, exit 1 = no lines matched (legitimate "all filtered / empty input" — must stay OK under `set -e`), exit 2 = error (invalid regex — must be FATAL). Fix per design doc: capture `rc=$?` after `grep -E -v "$pattern"` (no `|| true`), `return 0` for rc 0/1, but `return $rc`/error for rc ≥ 2; callers (L49, L66) must surface a ≥2 status and `exit 1` with a diagnostic naming `$SCOPE_FILE` instead of continuing with empty `FILE_LIST`.

**Pipeline/`set -e` nuance:** under `set -e`, a failing command in the *middle* of a pipe does not abort by default (only the last command's status matters, and `$()` captures it). So `apply_scope` returning non-zero will set the `$()` exit status; the caller needs an explicit check. Note `pipefail` is NOT a POSIX `sh` option, so cannot rely on it.

**SoT discipline:** edit `src/superclaude/skills/...`, then `make sync-dev`, then `make verify-sync`. **Do NOT stage the synced `.claude/skills/...` copy.**

---

## R5 — Milestone-ID `M{n}-D{nn}` blast radius (CORE)

### 5a. Contracts SoT — `src/superclaude/contracts/__init__.py`

`ID_PATTERNS` (L64-70), verbatim:
```python
ID_PATTERNS: Final[dict[str, str]] = {
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+(?:\.\d+)?",  # broader than BUILD-REQUEST verbatim — see §E
    "SC": r"SC-\d+",
    "G": r"G-\d+",  # added per Phase 2 D1 deviation — see header comment
    "D": r"D-?\d+",
}
```
**No `MD` family.** Convention (L58-62): bodies are **anchor-free**; consumers wrap with `\b…\b` at compile time. So an MD body added here must be anchor-free, e.g. `r"M\d+-D-?\d+"` (consumer wraps → `\bM\d+-D-?\d+\b`).

### 5b. spec_parser — `src/superclaude/cli/roadmap/spec_parser.py`

- L20: `from superclaude.contracts import ID_PATTERNS as _CONTRACTS_ID_PATTERNS`.
- L329-332: `_REQUIREMENT_PATTERNS = {family: re.compile(rf"\b{body}\b") for family, body in _CONTRACTS_ID_PATTERNS.items()}` — dict-comprehension over contracts; **family order = contracts dict order** (so to order MD before D the MD key must precede D in `contracts.ID_PATTERNS`).
- L335-346: `extract_requirement_ids(text)` returns `{family: sorted(set(pattern.findall(text)))}`. Currently no MD-dedup logic.

**WORD-BOUNDARY PROOF (verified via `uv run python`):** `\bD-?\d+\b` applied to `"M1-D01"` → matches `'D01'` (span 3-6). In `M1-D01` there is a `\b` between `-` (non-word) and `D` (word), so the bare-D pattern captures the trailing `D01`. So a roadmap using `M1-D01..M1-D54` against a spec defining only `D1,D3,D5` reproduces the master incident (51 phantom_id HIGHs). **The FP is real on the current branch.**

### 5c. structural_checkers — `src/superclaude/cli/roadmap/structural_checkers.py`

- `_canonicalize_requirement_id(family, raw)` at **L295-333**. Current regex L328: `re.match(r"^([A-Z]+)([-_]?)0*(\d+)(.*)$", raw)`. For `raw="D01"` family `D` → `D1`. There is **no `MD` branch** — an `M1-D01` token (if it were extracted as family MD) would fall through to the generic match: prefix=`M`, then `1` … actually `^([A-Z]+)` greedily takes `M`, sep=``, `0*` none, `(\d+)`=`1`, rest=`-D01` → returns `M1-D01` unchanged (single-letter prefix `M` → no sep). But MD is never extracted as a family today, so `M1-D01` is only ever seen as bare `D01`.
- phantom_id / id_schema_drift logic at **L418-472** (`check_signatures`, def L402). Builds `spec_canon` (L424-430) and `roadmap_canon` (L432-437) maps via the canonicalizer, then for each roadmap canon (L441): exact match → skip; canon-in-spec but raw differs → `id_schema_drift` MEDIUM (L446-459); canon-not-in-spec → `phantom_id` HIGH (L460-470). Severity map: `("signatures","phantom_id"): "HIGH"` (L33), `("signatures","id_schema_drift"): "MEDIUM"` (L34).
- **`check_signatures(spec_path, roadmap_path)` signature L402** — current branch has **NO `non_ref_allowlist`** anywhere (`grep -c non_ref ... = 0`).

### 5d. id_registry — `src/superclaude/cli/roadmap/id_registry.py`

- `_ID_PATTERN_KEYS` at L39 = `tuple(_ID_PATTERNS.keys())` (auto-derives from contracts; adding MD to contracts auto-adds the key).
- `SpecIdRegistry` dataclass fields **L77-84**: `fr_ids, nfr_ids, sc_ids, g_ids, d_ids, accepted_deviation_ids, spec_hash, spec_path`. **No `md_ids` field.**
- `union_of_known()` **L86-95** sums `fr_ids+nfr_ids+sc_ids+g_ids+d_ids+accepted_deviation_ids` — would need `+ md_ids`.
- `to_dict()` **L106-122** emits the same 8 keys — would need an `md_ids` key.
- `build_id_registry()` **L125+**: at L156-159 maps `families.get("FR"/"NFR"/...)` into the dataclass — would need `md_ids=tuple(families.get("MD", ()))`.

### 5e. Contract #9 sidecar JSON shape (two consumers)

- **WRITE side:** `id_registry.to_dict()` (L113-122) → keys `fr_ids, nfr_ids, sc_ids, g_ids, d_ids, accepted_deviation_ids, spec_hash, spec_path`. Written by executor `_save_id_registry` (executor.py L612-675) at `<output_dir>/spec_id_registry.json` via `json.dumps(registry.to_dict(), …)` (L653-654).
- **READ side:** `gates.py:_roadmap_ids_within_spec` L1089-1099 reconstructs `SpecIdRegistry(fr_ids=payload.get("fr_ids",()), …)` — would need `md_ids=tuple(payload.get("md_ids", ()))`. Because all reads use `payload.get(... , ())`, an OLD sidecar lacking `md_ids` round-trips safely (defaults to empty) — but a roadmap with MD IDs would then fail-shut Contract #9 unless `md_ids` is populated on both write and read. So **all of: dataclass field + to_dict + build_id_registry mapping + gates read + union_of_known** must change together, or MD IDs become unrepresentable → Contract #9 false-fail.

### 5f. PR #111 behavioral oracle (recovered from `origin/fix/roadmap-md-family-tokenizer-canonicalizer`)

The branch is on `origin` (not local): `remotes/origin/fix/roadmap-md-family-tokenizer-canonicalizer`. Recovered via `git show`. **PR #111 predates the contracts-SoT migration — it INLINED the regex literal** (`re.compile(r"\bM\d+-D-?\d+\b")` directly in `_REQUIREMENT_PATTERNS`). A forward-port (R5 path b) MUST instead source the MD body from `contracts.ID_PATTERNS` (Contract #8 / arch_lint Rule 2 forbids re-inlining).

PR #111 changes (3 mechanisms — note current branch has NONE of them):
1. **MD tokenizer family** — `_REQUIREMENT_PATTERNS` gains `"MD": re.compile(r"\bM\d+-D-?\d+\b")` ordered **BEFORE** `D`; plus `_MD_TRAILING_D_RE = re.compile(r"-(D-?\d+)$")` and a **dedup pass** in `extract_requirement_ids` that strips bare-D tokens that are the trailing portion of an MD token (deletes the `D` key entirely if all bare-D were absorbed).
2. **MD canonicalizer branch** in `_canonicalize_requirement_id`: `if family == "MD": md_match = re.match(r"^(M\d+-D)-?0*(\d+)$", raw)` → returns `f"{md_prefix}{md_num}"` (preserves `M{n}-D` prefix, strips leading zeros on the deliverable index; `M1-D01 -> M1-D1`).
3. **"Explicit non-references" allowlist** — a SEPARATE mechanism (regex anchor `_NON_REF_*` ~L407-412, parser ~L428, used in `check_signatures` ~L473+). `check_signatures` tracks `roadmap_canon_family` per canon and adds D3 allowlist branches: bare-D/bare-G tokens in `non_ref_allowlist` are skipped, and MD-family tokens whose D-suffix is in the allowlist are skipped. **This entire allowlist subsystem is ALSO absent from the current branch** — so path (b) is larger than "add MD": it must port the allowlist parser too, OR the MD fix alone may be insufficient to suppress the FP for roadmaps that rely on the "Explicit non-references" annotation.

**3 unit tests added (the oracle), in `tests/roadmap/test_structural_checkers.py`:**
- `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids` — spec lists `M1-D01..M3-D01` as milestone deliverables, roadmap implements them; with the Explicit-non-references annotation, MD-family resolves `M1-D01 != M2-D01` distinctly and produces 0 phantom_id.
- `test_phantom_id_backward_compatible_without_explicit_non_references` — no annotation → prior behavior preserved.
- `test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d` — bare-D path unaffected (regression guard).

### R5 minimum file set for path (b)

`contracts/__init__.py` (MD body, ordered before D), `spec_parser.py` (MD already auto-picked up via dict-comp ordering IF contracts dict orders MD first; + port `_MD_TRAILING_D_RE` dedup), `structural_checkers.py` (MD canonicalizer branch + port the entire Explicit-non-references allowlist subsystem + `roadmap_canon_family` tracking), `id_registry.py` (`md_ids` field + to_dict + build mapping + union_of_known), `gates.py` (`md_ids` in the L1089-1099 read), + tests + fixtures. arch_lint must stay green (MD literal lives only in contracts SoT). **This is why R5 is an investigation gate, not a one-liner.**

---

## Summary

All five edit sites verified against the current working tree (`refactor/roadmap-pipeline-r0-r1-rewrite`), every claim cited to file:line.

- **R1 (id_registry.py L22-24):** single comment-only Edit; replace the future-tense "R0.3 will hoist … the TODO comment below tracks that migration" clause. Contradicted by the already-present import at L37. Acceptance grep target confirmed.
- **R2:** gates.py global L1039, setter L1042-1049 (already supports `None`), fail-shut L1069-1074. Sidecar set only in extract step (executor L1365 → `_save_id_registry` L612 → setter L664). **Pipeline-run entry = `execute_roadmap` (executor.py L3397);** insert `set_id_registry_sidecar_path(None)` reset after the dry-run guard (L3492) and before `execute_pipeline()` (L3537). `config.output_dir` in scope for the optional path-identity guard. **LIVE CONSTRAINT:** `--resume` (L3498 `_apply_resume`) can skip extract → a naive unconditional reset would fail-shut MERGE on resume; reset must be resume-aware.
- **R3 (arch_lint.py L168-185):** Rule 2 confirmed — flat `ast.walk(tree)` (L143), exact set-membership `node.value in canonical_pattern_bodies` (L170). No NodeVisitor / no parent pointers → docstring-skip needs a pre-computed `id()`-set of docstring Constant nodes (first `Expr` of Module/ClassDef/FunctionDef/AsyncFunctionDef bodies) checked before L170.
- **R4 (repo-inventory.sh L29-37):** `#!/bin/sh`, `set -e` active (L9). `|| true` on both branches (L33/L35) masks grep exit-2. Callers at L49 (git ls-files) and L66 (find). Need rc capture distinguishing 0/1 (ok) from ≥2 (fatal), surfaced at both callers. POSIX sh → no `pipefail`. SoT: edit src/, sync-dev, never stage `.claude/`.
- **R5 (CORE):** word-boundary FP **proven** — `\bD-?\d+\b` extracts `D01` from `M1-D01`. Current branch has **no MD family, no milestone handling, and no "Explicit non-references" allowlist**. PR #111 (recovered from `origin/fix/roadmap-md-family-tokenizer-canonicalizer`) added all three, but **inlined the regex** (must be re-sourced from `contracts.ID_PATTERNS` for Contract #8). Blast radius for path (b): contracts (MD body before D) → spec_parser (MD dedup) → structural_checkers (MD canonicalizer + full allowlist subsystem) → id_registry (`md_ids` field + to_dict + build mapping + union) → gates Contract #9 sidecar read (L1089-1099) → 3 ported unit tests. Sidecar reads use `.get(...,())` so old sidecars round-trip, but MD IDs are unrepresentable until every layer gains `md_ids`.

**Cross-cutting note for task author:** R5 path (b) is materially larger than the design doc's "add an MD entry" framing because the **Explicit-non-references allowlist mechanism is entirely absent from the current branch** (not just MD). The investigation must determine whether MD-family alone closes the FP or whether the allowlist port is also required.
