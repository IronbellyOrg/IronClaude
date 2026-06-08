# Remediation Design — PR #112 & PR #111 Validated Review Findings

> **Status:** Design proposal (output of `/sc:design`) — combined remediation plan, ready for `/task-builder`.
> **Date:** 2026-06-02
> **Branch:** `refactor/roadmap-pipeline-r0-r1-rewrite`
> **Repo:** `IronbellyOrg/IronClaude` (fork; `origin`)
> **Source PRs:** [#112](https://github.com/IronbellyOrg/IronClaude/pull/112), [#111](https://github.com/IronbellyOrg/IronClaude/pull/111)

## Provenance & Validation Basis

Two parallel `auggie-reviewer` agents independently fetched the GitHub reviews on PR #112 and PR #111, then re-verified every finding against the **current working tree** (not the reviewed commit, which is stale: PR #112 was reviewed at `1c56b50f`, HEAD is `e22b7df3`; PR #111's head `861047c2` is **not** an ancestor of HEAD — the branches diverged).

The sole reviewer on both PRs was `augmentcode[bot]`. No human reviews, no CodeRabbit/Copilot. All bot findings were technically accurate reads of the commit they targeted; the work below is the subset that remains **actionable in the working tree** after divergence + severity recalibration.

Each remediation site was re-Read during this design pass and confirmed verbatim:
- `src/superclaude/cli/roadmap/id_registry.py:22-24`
- `src/superclaude/cli/roadmap/gates.py:1039-1049`, `1069-1074`
- `src/superclaude/tools/arch_lint.py:168-185`
- `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh:29-37`
- `src/superclaude/contracts/__init__.py:64-70` (ID_PATTERNS — FR/NFR/SC/G/D only)

## Repo Discipline (applies to every item below)

- **SoT:** `src/superclaude/` is the source of truth. Edit there, then `make sync-dev`, then `make verify-sync`.
- **Never stage `.claude/`** (except `.claude/settings.json`). The skill-script edit (R4) touches `src/superclaude/skills/...`; the synced `.claude/skills/...` copy must **not** be staged.
- **UV only** for any Python execution (`uv run pytest ...`).
- **Branch:** continue on `refactor/roadmap-pipeline-r0-r1-rewrite`; do not commit to master.

---

## Remediation Items

Severity legend: **BLOCKER > HIGH > MEDIUM > LOW > NIT**. None are blockers; R5 is the only one above LOW and is an **investigation**, not a blind code change.

### R1 — [NIT] Fix stale "future work" docstring in `id_registry.py`

**Problem.** `src/superclaude/cli/roadmap/id_registry.py:22-24` states the R0.3 pattern-hoist to `superclaude.contracts.ID_PATTERNS` is *future* work ("R0.3 **will** hoist the patterns … the TODO comment below tracks that migration"). But the migration already shipped in this same PR: line 37 already does `from superclaude.contracts import ID_PATTERNS as _ID_PATTERNS`, and there is **no** remaining "TODO comment below." The docstring is self-contradicting code drift.

**Design.** Rewrite the final docstring sentence (lines 22-24) to past/present tense and delete the dangling "the TODO comment below tracks that migration" clause. Suggested replacement:
> "R0.3 hoisted the family patterns to `superclaude.contracts.ID_PATTERNS`; this module now sources the known-family list from there (see import below). Contract #8 satisfied — no duplicate literal definition."

**Scope.** Comment-only. No behavior change.
**Acceptance.** Docstring contains no future-tense "will hoist" / "TODO below"; `grep -n "will hoist\|TODO comment below" src/superclaude/cli/roadmap/id_registry.py` returns nothing. `uv run pytest tests/ -k id_registry` still green.
**Effort.** Trivial (single Edit).

---

### R2 — [LOW-MED] Reset/validate `_id_registry_sidecar_path` global to prevent stale-sidecar reuse

**Problem.** `src/superclaude/cli/roadmap/gates.py:1039` declares module-level `_id_registry_sidecar_path: Path | None = None`. It is only ever **set** (by the executor's extract step via `set_id_registry_sidecar_path`, `gates.py:1042`) and never **reset** at the start of a pipeline run. The Contract #9 MERGE-gate check `_roadmap_ids_within_spec` (`gates.py:1052-1074`) is fail-shut **only** when the global is `None` (`gates.py:1069`). In any process that runs a second pipeline without re-running extract — a long-lived test harness, or a future `--resume` / `--start-at merge` path that skips extract — the check would read the **previous** run's sidecar instead of failing shut, validating roadmap IDs against the wrong spec registry.

**Design (defense-in-depth, two complementary guards):**
1. **Reset at run start.** At the pipeline-run entry point (executor, before the extract step runs — co-locate with where gates are wired up), call `set_id_registry_sidecar_path(None)` so a run that never reaches a successful extract fails shut as Contract #9 intends.
2. **Path-identity guard (preferred, stronger).** Have `set_id_registry_sidecar_path` (or the check) record the run's expected `output_dir`, and have `_roadmap_ids_within_spec` reject a sidecar whose parent path does not match the current run's `output_dir` — returning a fail-shut string rather than silently trusting a foreign sidecar.

Implement **both** where feasible; at minimum implement (1) (cheapest, removes the cross-run leak) and document (2) as the R1.3 envelope-migration follow-up (the existing comment at `gates.py:1033-1037` already flags R1.3 will widen the SemanticCheck signature to take an envelope — that is the natural home for path identity).

**Scope.** `src/superclaude/cli/roadmap/gates.py` (+ executor reset call site). Preserve the existing fail-shut semantics at `gates.py:1069-1074` exactly.
**Acceptance.** New regression test: two sequential `_roadmap_ids_within_spec`-exercising runs in one process where the second skips extract → second run returns a fail-shut string (not `True`, not a stale-registry pass). Existing Contract #9 fixtures (`tests/.../*contract*9*` / merge-gate sidecar tests) stay green.
**Effort.** Small (one reset call + one guard + one test). **Do not** change the `Callable[[str], bool|str]` SemanticCheck signature in R0 — that is explicitly deferred to R1.3.

---

### R3 — [NIT / optional] Harden `arch_lint` Rule 2 against docstring false-positives

**Problem.** `src/superclaude/tools/arch_lint.py:169-185` Rule 2 walks **every** `ast.Constant` string node and flags any whose value is in `canonical_pattern_bodies`. The match is **exact set-membership** (`node.value in canonical_pattern_bodies`, line 170), and the walker currently passes clean (0 violations) — so this is **not a live bug**, only defensive hardening. The theoretical FP: a docstring/string literal whose entire value equals a full regex body (e.g. literally `FR-\d+(?:\.\d+)?`). There is also already an opt-out (`# arch-lint: allow-duplicate` via `_line_has_allow_marker`, line 171).

**Design.** Before the membership test, skip nodes that are **docstrings** — i.e. a string `ast.Constant` that is the first statement (`Expr` value) of a `Module` / `ClassDef` / `FunctionDef` / `AsyncFunctionDef` body. Precompute the set of docstring node ids in one pass (or check parentage) and `continue` past them in Rule 2. Leave Rules 1 and 3 untouched. Keep the existing allow-marker opt-out as the escape hatch for genuine non-docstring literals.

**Scope.** `src/superclaude/tools/arch_lint.py` only. Behavior-preserving for all current inputs (walker still returns 0 violations).
**Acceptance.** `make lint-architecture` still exits 0. New unit test: a module whose docstring contains a verbatim `ID_PATTERNS` body string produces **no** `literal-duplicate` violation; a real top-level assignment of the same literal still **does**.
**Effort.** Small. **Marked optional** — schedule but allow `/task-builder` to gate it as lowest priority; it can be dropped if scope must shrink.

---

### R4 — [LOW] `apply_scope()` must not mask `grep` exit-2 (invalid ERE) in `repo-inventory.sh`

**Problem.** `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh:29-37`. `apply_scope()` runs `grep -E -v "(...)" || true`. The `|| true` exists to absorb grep's **exit-1** (no match on empty input under `set -e`), but it **also** swallows grep's **exit-2** — which grep returns when the ERE is invalid. A malformed `EXCLUDE:` line in a project's `.claude-audit/SCOPE.md` (concatenated into `$EXTRA_EXCLUDES` at lines 25-26) produces an invalid combined ERE, grep exits 2, `|| true` masks it, and the audit silently proceeds with an **empty** file list — reporting "Total files: 0" as if the repo were empty.

**Design.** Distinguish exit-1 (legitimate "no match") from exit-2 (error). Replace the bare `|| true` with explicit return-code handling, e.g.:
```sh
apply_scope() {
    local pattern
    if [ -n "$EXTRA_EXCLUDES" ]; then
        pattern="($DEFAULT_EXCLUDES|$EXTRA_EXCLUDES)"
    else
        pattern="$DEFAULT_EXCLUDES"
    fi
    grep -E -v "$pattern"
    rc=$?
    # 0 = matched (lines kept), 1 = no input/all filtered (ok), 2 = bad regex (fatal)
    if [ "$rc" -ge 2 ]; then
        echo "ERROR: invalid exclude regex (grep exit $rc). Check EXCLUDE: lines in $SCOPE_FILE" >&2
        return "$rc"
    fi
    return 0
}
```
Ensure the caller (`FILE_LIST=$(... | apply_scope)`, lines 49 & 66) surfaces the failure rather than continuing with empty output — e.g. check `apply_scope`'s status and `exit 1` with the diagnostic if it is ≥2. Optionally pre-validate `$EXTRA_EXCLUDES` once after lines 25-26 with a throwaway `printf '' | grep -E "$EXTRA_EXCLUDES"` probe so the error names the SCOPE.md line early.

**Scope.** `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`. **Then `make sync-dev`** (skill script lives under `src/superclaude/skills/`). **Do NOT stage the synced `.claude/skills/...` copy.**
**Acceptance.** With a deliberately malformed `EXCLUDE:` (e.g. `EXCLUDE: [unclosed`), the script exits non-zero with a diagnostic naming SCOPE.md — **not** "Total files: 0" exit 0. With a valid empty match it still exits 0. `make verify-sync` passes after sync.
**Effort.** Small (shell only). Pure pipeline-robustness; no functional change to valid runs.

---

### R5 — [MEDIUM] Investigate & decide: milestone-prefixed `M{n}-D{nn}` ID handling in the refactor pipeline

**Problem / framing.** PR #111 (`fix/roadmap-md-family-tokenizer-canonicalizer`, unmerged) added an **`MD` tokenizer family** + canonicalizer branch to eliminate **51 HIGH + 3 MEDIUM `phantom_id`/`id_schema_drift` false-positives** for roadmaps that use milestone-prefixed deliverable IDs like `M1-D01`. The current refactor branch derives all ID families from `superclaude.contracts.ID_PATTERNS` (`src/superclaude/contracts/__init__.py:64-70`), which contains **only** `FR / NFR / SC / G / D` — **no `MD` family**, and `grep` confirms **no** `milestone` / `MD` handling in `spec_parser.py` or `structural_checkers.py`.

**Important nuance (not a clean "regression"):** `origin/master`'s `spec_parser.py` **also** has no MD family — the MD work existed **only** on the unmerged PR #111 branch, and the refactor forked from master. So this is **not** "the refactor deleted a shipped fix"; it is an **open correctness gap**: a roadmap using `M1-D01` IDs run through the refactor pipeline may reproduce the exact 51-HIGH false-positive that PR #111 was created to fix, because `D-?\d+` (the current `D` body) matches only the `D01` tail of `M1-D01`, not the whole token.

**Design — investigation + decision (do NOT blind-port code):**
1. **Reproduce.** Build a minimal roadmap+spec fixture using `M{n}-D{nn}` IDs and run the refactor pipeline's structural/fidelity checks against it. Capture whether `phantom_id` / `id_schema_drift` false-positives appear. (Reuse PR #111's test intent: the 3 unit tests it added are the oracle for correct behavior.)
2. **Decide** between:
   - **(a) Confirmed-not-needed:** if the refactor's tokenizer/canonicalizer already handles `M{n}-D{nn}` correctly via some other mechanism, document why (with the passing fixture as evidence) and close PR #111 as superseded — **with the evidence attached**, not on assumption.
   - **(b) Re-introduce MD, SoT-sourced:** if the FP reproduces, add an `MD` entry to `superclaude.contracts.ID_PATTERNS` (the SoT — Contract #8 forbids re-inlining the literal in `spec_parser.py`/`structural_checkers.py`) and re-wire the tokenizer + canonicalizer + "explicit non-references" allowlist to consume it, porting PR #111's 3 unit tests forward. Respect the anchor-free SoT-body convention documented at `contracts/__init__.py:59-63` (consumers wrap with `\b…\b` at compile time).
3. **Reconcile the registry.** If (b), `id_registry.py`'s `_ID_PATTERN_KEYS` (sourced from `ID_PATTERNS.keys()`, line 39) and `SpecIdRegistry`'s family fields (`fr/nfr/sc/g/d_ids`) must gain an `md_ids` field, and the Contract #9 sidecar JSON schema + fixtures updated — otherwise MD IDs would be unrepresentable in the registry and re-trigger Contract #9 fail-shut. **This cross-cutting impact is why R5 is an investigation gate, not a one-line add.**

**Scope (if path b).** `src/superclaude/contracts/__init__.py`, `cli/roadmap/spec_parser.py`, `cli/roadmap/structural_checkers.py`, `cli/roadmap/id_registry.py`, `cli/roadmap/gates.py` (Contract #9 sidecar), + tests + fixtures. **arch_lint** must still pass (MD body lives only in the SoT).
**Acceptance.**
- Decision recorded in `.dev/reviews/` with the reproduction fixture + result as evidence.
- If (a): fixture demonstrates **0** false-positives on `M{n}-D{nn}`; PR #111 closed as superseded citing the evidence.
- If (b): the 3 ported unit tests pass; the `M{n}-D{nn}` fixture yields **0** `phantom_id`/`id_schema_drift` findings; `make lint-architecture` exits 0 (no duplicated literal); Contract #9 sidecar round-trips `md_ids`; full suite delta vs parent baseline unchanged.
**Effort.** Investigation = small; path (b) = medium-large (cross-cutting SoT + registry + checker). **Gate (b) behind the investigation outcome** — `/task-builder` should model R5 as: [investigate/reproduce] → [decision] → [conditional implement subtree].

---

## Suggested Sequencing for `/task-builder`

1. **R5-investigate** first (highest information value; its outcome may add a large implementation subtree — surface it early).
2. **R1** (trivial docstring) — quick, isolated.
3. **R2** (sidecar reset + test) — isolated to gates/executor.
4. **R4** (shell robustness + `make sync-dev` + `verify-sync`) — isolated to the audit skill.
5. **R3** (optional arch_lint hardening) — lowest priority; droppable.

R1–R4 are mutually independent and may be parallelized. R5's implementation branch (if path b) **must** land before any claim that the refactor pipeline is FP-clean for milestone IDs.

## Out of Scope / Explicitly Not Doing

- Changing the R0 `SemanticCheck` signature (`Callable[[str], bool|str]`) — deferred to R1.3 by design.
- Re-opening or merging PR #111 as-is (its branch is divergent; the forward path is R5, not a merge).
- Independently re-verifying PR #112's unverified body self-claims (test counts, byte-identical PRESERVE invariants) — separate audit if a merge decision needs them.
- Any `.claude/` staging. Sync is mechanical output only.
