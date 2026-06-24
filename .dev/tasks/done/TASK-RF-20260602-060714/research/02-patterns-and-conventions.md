# Research 02 — Patterns & Conventions

> **Status:** Complete
> **Topic:** Project conventions that constrain HOW the R1–R5 remediations must be implemented.
> **Repo:** `/config/workspace/IronClaude-RoadmapRewrite`
> **Branch:** `refactor/roadmap-pipeline-r0-r1-rewrite`
> **Driving doc:** `.dev/reviews/PR-112-111-remediation-design.md`
> **Scope note:** Other researchers own exact code sites / blast radius, tests & fixtures, and the MDTM template. This file covers ONLY conventions/patterns. All findings carry `file:line` evidence; unverified items are marked.

---

## 1. Contracts Source-of-Truth pattern (Contract #8)

**SoT file:** `src/superclaude/contracts/__init__.py`.

### 1a. Module is the single source of truth; consumers IMPORT, never re-inline
The module docstring states it explicitly (`contracts/__init__.py:1-6`):
> "This module is the **source of truth** for cross-skill / cross-module constants. Per Contract #5 + #8 (master:§Recurrence #7 + master:§Flaw 5), no other module may redefine these constants — ``make lint-architecture`` enforces this via :mod:`superclaude.tools.arch_lint`."

The consumer-side convention is demonstrated by `id_registry.py:33-39`: it imports `from superclaude.contracts import ID_PATTERNS as _ID_PATTERNS` and derives `_ID_PATTERN_KEYS = tuple(_ID_PATTERNS.keys())` rather than re-declaring any family list. The inline comment there (`id_registry.py:35-36`) reads "Contract #8 satisfied — no duplicate literal definition."

### 1b. `ID_PATTERNS` structure (the registry consumers read)
`contracts/__init__.py:64-70`:
```python
ID_PATTERNS: Final[dict[str, str]] = {
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+(?:\.\d+)?",  # broader than BUILD-REQUEST verbatim — see §E
    "SC": r"SC-\d+",
    "G": r"G-\d+",  # added per Phase 2 D1 deviation — see header comment
    "D": r"D-?\d+",
}
```
- A `dict[str, str]` keyed by **family name** → **anchor-free regex body**. Typed `Final`.
- **Only FR / NFR / SC / G / D today** — confirms R5's premise: **no `MD` family** exists. Any R5-path-b `MD` add lands here as a new key.
- `Final[...]` typing is the house style for every constant in this module (`ID_PATTERNS`, `CONVERGENCE_THRESHOLDS:86`, `GATE_FIELD_NAMES:97`, `THRESHOLDS:122`, `RETURN_CONTRACTS:197`).

### 1c. Anchor-free-body convention (bodies omit `\b`; consumers wrap at compile time)
Header comment `contracts/__init__.py:58-62` (cited verbatim, the load-bearing convention for R5):
> "Pattern bodies do NOT include word-boundary anchors `\b…\b`. Consumers that need anchored matching (e.g. `spec_parser._REQUIREMENT_PATTERNS`) wrap with `\b{ID_PATTERNS["FR"]}\b` at compile time. Keeping bodies anchor-free keeps the SoT regex composable for non-word-boundary contexts (heading-anchored variants in `fidelity_checker.py` — migrated in R1.1 Step 6.3)."

**Constraint on R5-path-b:** an `MD` body added to `ID_PATTERNS` must be **anchor-free** (e.g. a body like `M\d+-D-?\d+`, no `\b`). The wrapping/anchoring is the consumer's job. The design doc's R5 item reiterates this at `PR-112-111-remediation-design.md:117`.

### 1d. `__all__` is the discovery surface for arch_lint
`contracts/__init__.py:202-210` lists all 7 owned names. The header note `contracts/__init__.py:33-36` states arch-lint "extends to the new names automatically via the ``__all__`` discovery." So **anything added to `__all__` is automatically protected** by the name-rebind + class-redef rules (see §2). For R5-path-b: adding only an `ID_PATTERNS` *key* (not a new top-level name) needs no `__all__` change; the new regex body is automatically protected by Rule 2 the moment it appears in `ID_PATTERNS.values()`.

### 1e. Header-comment convention for documented deviations
Deviations from the originating BUILD-REQUEST are logged inline with a pointer to a discovery doc — e.g. `contracts/__init__.py:46-56` (G-family + broader NFR pattern, "logged in phase-outputs/discovery/contracts-consumer-sites.md §E"). R5-path-b adding `MD` should follow this same in-file comment style citing PR #111 as provenance.

---

## 2. arch_lint enforcement (governs R3 and R5-path-b)

**File:** `src/superclaude/tools/arch_lint.py`. **Module docstring** `arch_lint.py:1-44` describes the contract and the three rules.

### 2a. The three rules (all in `scan_file`, `arch_lint.py:116-206`)
| Rule | Node type | Kind label | Site |
|---|---|---|---|
| 1 — name-rebind | `ast.Assign` / `ast.AnnAssign` whose LHS `Name` ∈ `canonical_names` | `"name-rebind"` | `arch_lint.py:144-166` |
| 2 — literal-duplicate | `ast.Constant` string whose value ∈ `canonical_pattern_bodies` (set of `ID_PATTERNS.values()`) | `"literal-duplicate"` | `arch_lint.py:168-185` |
| 3 — class-redef | `ast.ClassDef` whose `name` ∈ `canonical_names` | `"class-redef"` | `arch_lint.py:187-204` (added R1.1 Step 6.3) |

`canonical_names` = `set(contracts.__all__)`; `canonical_pattern_bodies` = `set(ID_PATTERNS.values())` — loaded by import in `_load_canonical_constants` (`arch_lint.py:80-91`). The canonical contracts file itself is exempt (`scan_file` early-returns via `_is_canonical_file`, `arch_lint.py:126-127`, `110-113`).

**Kind enum** is documented on the `Violation` dataclass field comment: `"name-rebind" | "literal-duplicate" | "class-redef"` (`arch_lint.py:67`).

### 2b. Rule 2 matching is EXACT set-membership (R3's hardening target)
`arch_lint.py:170`: `if node.value in canonical_pattern_bodies:`. This is exact whole-string equality against a full regex body — the theoretical false-positive R3 hardens against is a docstring/string literal whose entire value equals a body (e.g. literally `FR-\d+(?:\.\d+)?`). The walker currently returns **0 violations** under `make lint-architecture` (verified live in §4), so R3 is defensive only — confirmed by design doc `PR-112-111-remediation-design.md:66-72` (marked **optional / droppable**).

### 2c. The allow-marker opt-out
- Constant: `_ALLOW_MARKER = "arch-lint: allow-duplicate"` (`arch_lint.py:58`).
- Checker: `_line_has_allow_marker(source_lines, lineno)` returns True iff the 1-based line contains the marker (`arch_lint.py:103-107`).
- **All three rules** honor it via `if _line_has_allow_marker(...): continue` (Rule 1 `:153-154`, Rule 2 `:171-172`, Rule 3 `:191-192`).
- Full opt-out form per docstring `arch_lint.py:19-20`: `# arch-lint: allow-duplicate <reason>` on the offending line.

### 2d. How `make lint-architecture` invokes it
`Makefile:362` defines target `lint-architecture`. The arch_lint invocation is **Check 11 of the architecture suite** (`Makefile:463-473`):
```make
if uv run python -m superclaude.tools.arch_lint \
    --check-contracts src/superclaude/contracts/__init__.py \
    --scan-paths src/superclaude/cli/ > /tmp/arch_lint_check11.out 2>&1; then \
    echo "  ✅ [Check 11]: no contract-constant duplications"; \
else \
    cat /tmp/arch_lint_check11.out | sed 's/^/      /'; \
    errors=$$((errors+1)); \
fi;
```
**Critical scope fact:** `--scan-paths` is `src/superclaude/cli/` ONLY. arch_lint does **not** scan `src/superclaude/tools/` or `src/superclaude/contracts/` against itself. Exit codes per docstring `arch_lint.py:32-35`: `0` clean, `1` ≥1 violation, `2` invocation error.

`make lint` runs `lint-architecture` first as a prerequisite, then `ruff check .` (`Makefile:48-50`).

### 2e. Constraint this imposes on R3 and R5-path-b
- **R3** edits `src/superclaude/tools/arch_lint.py` only (design `:70`). Because that file is **not** in `--scan-paths`, R3 cannot self-trip; acceptance is "`make lint-architecture` still exits 0" + a new unit test (design `:71`).
- **R5-path-b** must keep the `MD` regex body living **only** in `ID_PATTERNS`. If any consumer under `src/superclaude/cli/` (e.g. `spec_parser.py`, `structural_checkers.py`) re-inlines the literal `MD` body string, **Rule 2 fires and `make lint-architecture` exits non-zero** (design `:117`, `:120`, `:124`). Consumers must import the body and wrap with `\b…\b` at compile time per §1c. Acceptance criterion in design: "`make lint-architecture` exits 0 (no duplicated literal)" (`:124`).

---

## 3. Fail-shut invariant (Contract #9) — R2 must preserve exactly

**Function:** `_roadmap_ids_within_spec(content: str) -> bool | str` at `src/superclaude/cli/roadmap/gates.py:1052-1113`.

### 3a. The fail-shut contract (return a failure STRING, never True)
Docstring `gates.py:1061-1063`:
> "Fail-shut: if the sidecar is missing/unreadable/malformed the check returns a string (failure) rather than ``True`` (master:§Flaw 4 — no fail-open defaults)."

Every error path returns a descriptive string; `True` is returned **only** when violations are empty (`gates.py:1106-1107`):
| Failure mode | Site | Returns |
|---|---|---|
| sidecar path not registered (global is `None`) | `gates.py:1069-1074` | failure string |
| sidecar unreadable (`OSError`) | `gates.py:1076-1082` | failure string |
| sidecar not valid JSON (`JSONDecodeError`) | `gates.py:1084-1087` | failure string |
| schema mismatch (`TypeError`/`ValueError`) | `gates.py:1089-1101` | failure string |
| roadmap IDs ∉ known set | `gates.py:1108-1113` | failure string (preview of ≤5) |
| all IDs known | `gates.py:1106-1107` | `True` |

### 3b. The module-global hint mechanism (R2's actual target)
- Declaration: `_id_registry_sidecar_path: Path | None = None` (`gates.py:1039`).
- Setter: `set_id_registry_sidecar_path(path: Path | None)` (`gates.py:1042-1049`); docstring notes `None` clears the hint "(used by tests for isolation)" (`gates.py:1046`).
- The `None`-means-fail-shut guard is `gates.py:1069-1074`.
- Rationale comment `gates.py:1028-1037`: the SemanticCheck signature is `Callable[[str], bool | str]` (content only). R0.1 keeps that signature; R1.3 will widen it to take an envelope. `None` = "not yet set" → fail CLOSED.

**R2 constraint:** the design (`PR-112-111-remediation-design.md:52-60`) adds a run-start reset + optional path-identity guard but must **preserve the existing fail-shut semantics at `gates.py:1069-1074` exactly**, and must **NOT** change the `Callable[[str], bool | str]` signature (deferred to R1.3 — design `:60`, `:141`; out-of-scope list). Any new guard must return a fail-shut **string**, never `True`/`False`-that-passes.

---

## 4. Sync discipline (governs R4; also any synced output)

### 4a. SoT → sync-dev → .claude/ rule (CLAUDE.md, project)
`CLAUDE.md` (project root) "🔄 Component Sync" section: "**Source of truth**: `src/superclaude/` is the canonical location… The `superclaude install` CLI reads from here." Workflow: (1) edit `src/superclaude/skills/…`, (2) `make sync-dev`, (3) `make verify-sync`.

The design doc reiterates this as repo discipline (`PR-112-111-remediation-design.md:24`): "Edit there, then `make sync-dev`, then `make verify-sync`."

### 4b. ABSOLUTE RULE — never stage `.claude/` (except settings.json)
`CLAUDE.md` "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents": `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output. The **only** tracked file is `.claude/settings.json`. Never `git add .claude/skills/...`, never `git add -f` on a `.claude/` path. The `-f` requirement is "the violation siren — STOP." Confirmed in user global memory `feedback_claude_dir_gitignored.md` (MEMORY.md index).

### 4c. Exact R4 procedure (this is the load-bearing convention for R4)
R4 edits `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` (a skill script under `src/superclaude/skills/...`). Procedure:
1. **Edit `src/` side only:** `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`.
2. **`make sync-dev`** — copies it to `.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` (script files are picked up by the `find … -exec cp` loop in `Makefile:112-125`; non-`__init__.py`, non-`__pycache__` files under each skill dir are synced, and the loop `chmod +x` only applies to hooks, not skill scripts — the cp preserves the file).
3. **`make verify-sync`** — confirms `src/` ↔ `.claude/` match (diffs each skill dir, `Makefile:166-187`; exits 1 on drift).
4. **Stage ONLY the `src/` side.** Do NOT `git add` the synced `.claude/skills/...` copy (design `:101`: "**Do NOT stage the synced `.claude/skills/...` copy.**"; `:25`).

Acceptance for R4 explicitly includes "`make verify-sync` passes after sync" (design `:102`).

### 4d. Relevant Makefile target quotes
- **`test:`** (`Makefile:13-15`): `uv run pytest`.
- **`lint:`** (`Makefile:48-50`): depends on `lint-architecture`, then `uv run ruff check .`.
- **`format:`** (`Makefile:53-55`): `uv run ruff format .`.
- **`sync-dev:`** (`Makefile:109-163`): syncs `src/superclaude/{skills,agents,commands,hooks,templates}` → `.claude/`. Skill-file loop at `Makefile:112-125`.
- **`verify-sync:`** (`Makefile:166-…`): per-skill `diff -rq --exclude='__init__.py' --exclude='__pycache__'`; sets `drift=1` and ultimately exits non-zero on any divergence (`Makefile:166-187`).
- **`lint-architecture:`** (`Makefile:362-…`): the multi-check suite; arch_lint is Check 11 (`Makefile:463-473`).
- The full `.PHONY` line confirms target names: `Makefile:1`.

### 4e. R4 site verification (current code, for the implementer's convenience)
`repo-inventory.sh:29-37` is `apply_scope()` with the `|| true` masking issue (the `grep -E -v "(…)" || true` pattern at `:33` and `:35`). The two callers are `FILE_LIST=$(git ls-files … | apply_scope)` at `:49` and the `find … | apply_scope` at `:66` — matching the design doc's "lines 49 & 66" (`PR-112-111-remediation-design.md:99`). The `set -e` is at `:9`; `EXTRA_EXCLUDES` is built from `SCOPE.md` `EXCLUDE:` lines at `:24-27`.

---

## 5. UV-only Python rule + test invocation convention

- **CLAUDE.md (project)** "🐍 Python Environment Rules": "This project uses **UV** for all Python operations. Never use `python -m`, `pip install`, or `python script.py` directly." Required forms: `uv run pytest`, `uv run pytest tests/pm_agent/`, `uv pip install package`, `uv run python script.py`.
- **User global CLAUDE.md** Core Rule #1: "**UV only** — never `python -m` or bare `pip`."
- **Test invocation convention:** `uv run pytest <path> -v`, by marker `uv run pytest -m <marker>`, with coverage `uv run pytest --cov=superclaude`. `make test` is just `uv run pytest` (`Makefile:14-15`).
- Note the one sanctioned `python -m` form is **inside the Makefile** for arch_lint: `uv run python -m superclaude.tools.arch_lint …` (`Makefile:465`) — still under `uv run`, satisfying the rule.
- Design doc reinforces: "**UV only** for any Python execution (`uv run pytest ...`)" (`PR-112-111-remediation-design.md:26`). Every R-item acceptance that runs tests must use `uv run pytest` (e.g. R1 `:43`, R2 `:59`).

---

## 6. Branch / commit discipline

- **Stay on `refactor/roadmap-pipeline-r0-r1-rewrite`.** Design doc repo discipline (`PR-112-111-remediation-design.md:27`): "**Branch:** continue on `refactor/roadmap-pipeline-r0-r1-rewrite`; do not commit to master." Current branch confirmed via session git status = `refactor/roadmap-pipeline-r0-r1-rewrite`.
- **Feature branches only; never master/main.** User global CLAUDE.md Core Rule #4: "Git — feature branches only; never commit directly to master/main." Project CLAUDE.md "🌿 Git Workflow": `master ← integration ← feature/* …`.
- **PR target = fork `IronbellyOrg/IronClaude`, NEVER upstream** (relevant only if a PR is opened later). Project CLAUDE.md "ABSOLUTE RULE: PR Target = Fork": every `gh pr create` MUST carry `--repo IronbellyOrg/IronClaude --base master --head <branch>`; bare `gh pr create` defaults to the public upstream and is forbidden. Mirrored in user memory `feedback_pr_target_fork_only.md`.
- **Commit only when asked** (harness default); this is remediation work, not auto-commit. No instruction in the design doc to commit/PR — the deliverable is the working-tree change + green gates.

---

## Summary — convention constraints per remediation item

- **R1 (docstring):** comment-only edit in `src/superclaude/cli/roadmap/id_registry.py:22-24`. The drift is confirmed: lines 22-24 say "R0.3 **will** hoist … the TODO comment below tracks that migration," but `:37` already imports `ID_PATTERNS` and there is no remaining TODO. No sync (not a skill). Re-verify with `uv run pytest tests/ -k id_registry`.
- **R2 (sidecar reset):** preserve fail-shut at `gates.py:1069-1074` exactly; new guards return failure **strings**; do NOT touch the `Callable[[str], bool|str]` signature (R1.3 territory). `uv run pytest` for the regression test.
- **R3 (arch_lint hardening, optional):** edits `tools/arch_lint.py` only — outside arch_lint's own `--scan-paths`, so it can't self-trip. Keep the allow-marker opt-out (`:58`, `:103-107`) intact; harden Rule 2 (`:168-185`) for docstrings. Acceptance: `make lint-architecture` still exits 0.
- **R4 (shell robustness):** edit `src/superclaude/skills/.../repo-inventory.sh` → `make sync-dev` → `make verify-sync` → stage **only** `src/`. NEVER `git add` the `.claude/skills/...` copy (no `-f`).
- **R5-path-b (MD family):** new `MD` key in `ID_PATTERNS` must be **anchor-free**; consumers under `src/superclaude/cli/` import + wrap `\b…\b` and must NOT re-inline the literal (else arch_lint Rule 2 / Check 11 fails). Follow the in-file deviation-comment convention citing PR #111. Whether `__all__` changes depends on whether new top-level names are added (a new dict *key* alone does not).
- **All items:** UV-only execution; stay on `refactor/roadmap-pipeline-r0-r1-rewrite`; if a PR is opened, `--repo IronbellyOrg/IronClaude`.

### Unverified / flagged
- The exact `tests/` paths and fixture names for Contract #9 sidecar / `id_registry` are **out of my scope** (tests-researcher owns them) — I cite only the production sites.
- I did **not** run `make lint-architecture` / `make verify-sync` in this pass; the "currently 0 violations / passes" claims are sourced from the design doc's verification (`PR-112-111-remediation-design.md:66`, `:15-21`) and the code structure, not a fresh execution in this session.
