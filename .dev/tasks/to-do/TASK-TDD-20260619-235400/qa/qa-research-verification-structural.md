# QA Report — Research Gap-Fill Verification (Structural)

**Topic:** FR-RH2 reflect config/CLI surface + swarm recipe registry gap-fill
**File under review:** `.dev/tasks/to-do/TASK-TDD-20260619-235400/research/09-reflect-config-cli-surface.md`
**Date:** 2026-06-20
**Phase:** research-gate (single-file gap-fill re-verification)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assumed citations were hallucinated until each was opened and confirmed.

---

## Overall Verdict: PASS

The gap-fill genuinely closes the CRITICAL gap. The previously-unexamined surface — `ReflectConfig` dataclass, `resolve_config()` resolution chain, the Click `--depth`/`--transport`/`--reviewers` surface, `runner.py` `expected_tier` derivation, and the swarm recipe REGISTRY/STRATEGIES binding — is now documented with file:line citations that **open to the exact code claimed**. I sampled 8 load-bearing claims (exceeding the requested 5-6) and opened every cited source. All 8 verified. Two minor line-number drifts (±1–2 lines) and one path-qualifier ambiguity were found; none are load-bearing and none change a single actionable conclusion. No hallucinated paths, no hallucinated functions, no fabricated registry entries.

---

## Claims Sampled & Verified (8)

### Claim 1 — `ReflectConfig` is in `models.py`, NOT `config.py` (the orientation lynchpin)
**Report says:** `models.py:57-91` `@dataclass class ReflectConfig`; imported by `config.py:24` (`from .models import ReflectConfig`).
**Verified:** `models.py:57` `@dataclass`, `models.py:58` `class ReflectConfig:`, body L66-86, `contract_path` property L88-91. `config.py:24` is exactly `from .models import ReflectConfig`.
**Result: PASS.** The single most load-bearing structural claim — that FR-RH2 is a 3-file edit because the dataclass and resolver live in different modules — is correct.

### Claim 2 — Full field list of `ReflectConfig` (19 fields, declaration order, tail-append rule)
**Report says:** 19 fields in order `tasklist_path … max_fix_iterations`, no in-body defaults, auto-fix block (`base_override`, `fix`, `max_fix_iterations`) appended at tail per ordering-rule comment at `models.py:82-83`.
**Verified:** `models.py:66-86` lists exactly those 19 fields in exactly that order. None carry `= default`. The comment "appended AFTER all existing non-default fields to respect the dataclass field-ordering rule" is at `models.py:82-83`. `ReflectResult` (not `ReflectConfig`) is the one using `field(default_factory=...)` — confirmed at `models.py:109`.
**Result: PASS.** Field table is byte-accurate. This is the table FR-RH2 implementers will copy from; it is correct.

### Claim 3 — `--depth` ALREADY EXISTS, fully wired (do NOT re-add)
**Report says:** Click option `commands.py:101-106`, `type=click.Choice(["standard","deep"], case_sensitive=False)`, `default="standard"`; floor `config.py:190` `resolved_depth = "standard" if depth == "quick" else depth`; stored to field `models.py:71`.
**Verified:** `commands.py:101-106` is exactly that `@click.option("--depth", …)` block, verbatim. `config.py:190` is exactly `resolved_depth = "standard" if depth == "quick" else depth`. `depth` is the field at `models.py:70` (report cites `models.py:71` — **off-by-one, see Minor Issues**). The `quick`→`standard` floor is real and correctly described.
**Result: PASS** (1-line citation drift, non-load-bearing). The core claim — `--depth` is pre-existing with a `quick`→`standard` floor and must not be re-added — is correct and verified.

### Claim 4 — `--transport` / `--reviewers` are 100% NET-NEW (zero occurrences)
**Report says:** `grep -rnE "transport|reviewers|openai_compat|negative-witness|negative_witness"` over `src/superclaude/cli/reflect/` returns ONLY the prose comment at `config.py:34`.
**Verified:** Ran that exact grep. Single hit: `config.py:34:# (heterogeneous reviewers + adversarial merge + evidence-validator +`. Zero `transport`, zero `openai_compat`, zero `negative-witness` anywhere in the reflect package.
**Result: PASS.** The net-new claim is independently reproduced. The `[CODE-CONTRADICTED]` tag on the "they exist" assumption is correctly applied.

### Claim 5 — `expected_tier` derived in runner at `runner.py:403`, collapses both depths to 2
**Report says:** `runner.py:403` `expected_tier = 2 if config.depth in {"standard", "deep"} else 1`; threads into `derive_verdict(expected_tier=...)`.
**Verified:** `runner.py:403` is exactly `expected_tier = 2 if config.depth in {"standard", "deep"} else 1`. It is passed into `derive_verdict(contract, expected_tier=expected_tier, …)` at runner.py:421-426. Both `standard` and `deep` → 2; correctly noted as the single mutation point if `deep` must map elsewhere.
**Result: PASS.** Exact line, exact expression.

### Claim 6 — Twelve `@click.option` decorators quoted verbatim (`commands.py:81-147`)
**Report says:** the command takes one positional `tasklist` arg + 12 options; quotes all twelve.
**Verified:** `commands.py:77-80` positional `tasklist` (`exists=True, dir_okay=False, resolve_path=True`). Options span L81-147: `--tmux`, `--print-command`, `--promote/--no-promote`, `--timeout`, `--depth`, `--output`, `--allow-single-vendor`, `--dry-run`, `--resume`, `--fix/--no-fix`, `--max-fix-iterations`, `--base` = exactly 12, in that order, with the quoted attrs matching. `run()` signature L148-162 takes all 12 + tasklist. `resolve_config(...)` call L175-190 threads each as a kwarg.
**Result: PASS.** Verbatim quotes are accurate; the "no `--model` flag" observation (`_DEFAULT_MODEL` env fallback at `commands.py:31`/L172) is also correct.

### Claim 7 — `bare-review-v1` exists in BOTH `REGISTRY` and `STRATEGIES`
**Report says:** `REGISTRY` at `__init__.py:181-188` contains `"bare-review-v1": BareReviewV1()`; `STRATEGIES` at `__init__.py:208-215` contains `"bare-review-v1": "bare-review-v1"`. Reusing it (Path A) satisfies validator assertions 2 & 6 with zero recipe-package edits.
**Verified:** `recipes/__init__.py:181-188` is the `REGISTRY` dict; L182 is `"bare-review-v1": BareReviewV1()`. `STRATEGIES` dict L208-215; L209 is `"bare-review-v1": "bare-review-v1"`. The N-to-1 "strategy name == recipe name" claim holds for all six entries.
**Result: PASS.** This is the swarm-side gap closure — confirmed exactly as cited.

### Claim 8 — Validator assertions 2 & 6 resolve against REGISTRY/STRATEGIES; lens binding fields
**Report says:** `default_recipe_checker` returns `name in recipes.REGISTRY`; `default_strategy_checker` checks STRATEGIES (or REGISTRY); `LensEntry` carries `recipe_name`/`normalizer_strategy` at `models.py:712-713`; `bare-review` lens sets both to `"bare-review-v1"` at `lenses/bare_review.py:59-60`.
**Verified:** `_validate.py:204` `def default_recipe_checker`, body resolves `getattr(recipes, "REGISTRY", …)` (~L231); rule symbol `lens.recipe_unregistered` at L125. `_validate.py:240` `def default_strategy_checker`, resolves STRATEGIES (~L276) then REGISTRY (~L281); rule `lens.normalizer_strategy_unmatched` at L137. `LensEntry.recipe_name` at `swarm/models.py:712`, `.normalizer_strategy` at `swarm/models.py:713`. `lenses/bare_review.py:59-60` = `recipe_name="bare-review-v1"`, `normalizer_strategy="bare-review-v1"`.
**Result: PASS.** Note: the report's Section 3 cites these `LensEntry` fields as `models.py:712-713` without the `lenses/`-vs-`swarm/` qualifier; the actual file is `src/superclaude/cli/swarm/models.py` (the report's Scope line scopes the swarm work to `src/superclaude/cli/swarm/recipes/` and `lenses/_validate.py`, so the bare `models.py` cite is mildly ambiguous but resolves correctly). Line numbers are exact. Non-load-bearing, see Minor Issues.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `ReflectConfig` location (models.py not config.py) | PASS | Opened `models.py:57-91`, `config.py:24` import |
| 2 | 19-field dataclass list + tail-append rule | PASS | `models.py:66-86`, ordering comment L82-83 |
| 3 | `--depth` pre-exists + `quick`→`standard` floor | PASS | `commands.py:101-106` verbatim, `config.py:190` floor |
| 4 | `--transport`/`--reviewers` net-new (grep) | PASS | Reproduced grep: only `config.py:34` comment |
| 5 | `expected_tier` at `runner.py:403` | PASS | Opened `runner.py:403`, exact expression |
| 6 | 12 Click options verbatim | PASS | `commands.py:77-147`, signature L148-162, call L175-190 |
| 7 | `bare-review-v1` in REGISTRY + STRATEGIES | PASS | `recipes/__init__.py:182` + `:209` |
| 8 | Validator checkers + LensEntry fields | PASS | `_validate.py:204/240`, `swarm/models.py:712-713`, `lenses/bare_review.py:59-60` |

## Summary
- Claims sampled: 8 / 8 verified (target was 5-6; over-sampled)
- Claims passed: 8
- Claims failed: 0
- Critical issues: 0
- Fabricated paths / functions / registry entries: 0
- Tool calls: Read 5 (the 5 cited source files) + 2 Bash grep/sed verification passes — every call mapped to a specific claim, no padding.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | research file §1a / Key Takeaway 2 (`models.py:71`) | `depth` field is actually declared at `models.py:70`, not L71 (off-by-one). The §1 field table row #5 correctly maps to the L66-86 range; only the standalone L71 cite drifts. | Change `models.py:71` → `models.py:70`. Cosmetic; does not affect the conclusion. |
| 2 | MINOR | research file §3 "How a lens binds" (`models.py:712`, `models.py:713`) | `LensEntry` fields are cited as bare `models.py:712-713`; the actual file is `src/superclaude/cli/swarm/models.py`, not the reflect `models.py` referenced throughout §1. Line numbers are exact. | Qualify the path as `swarm/models.py:712-713` to disambiguate from `reflect/models.py`. |
| 3 | MINOR (cosmetic) | research file §1 header / Key Takeaway 1 | Header says "`models.py:57-91`" while the `[CODE-VERIFIED]` tag at L22 says "`models.py:57-86`". The dataclass body ends L86; the property `contract_path` extends the class to L91. Both are defensible (class-with-property vs field-block); minor internal inconsistency. | Optional: standardize on `57-91` (class incl. property) everywhere. |

None of the three issues are load-bearing. Every actionable instruction in the gap-fill (where to append fields, which floor exists, what is net-new, which registry keys to reuse) is backed by a citation that opens to the claimed code.

## Doc-validation tag audit
- `[CODE-VERIFIED]` tags: spot-checked 6 of them against source — all resolve to real code at the cited lines (modulo the two MINOR drifts above).
- `[CODE-CONTRADICTED]` tag (§1c, "transport/reviewers do not exist"): correctly applied — the grep independently confirms zero occurrences.
- `[UNVERIFIED]` tags (4 in Gaps): all four are legitimately downstream/undecided (clamp-vs-reject semantics, `stub` runtime wiring, `reflect-review` lens file, `expected_tier` promotion) — correctly NOT claimed as verified. No untagged doc-sourced claims found.

## Gap-closure assessment
The original CRITICAL gap was that the reflect `config.py`/`ReflectConfig` + `commands.py` Click surface + swarm recipe registry were **unexamined**. After this gap-fill:
- `ReflectConfig` fully enumerated (Claim 1-2). ✔
- `resolve_config()` resolution chain traced incl. `--depth` floor (Claim 3). ✔
- Click `--transport`/`--reviewers`/`--depth` surface characterized; net-new vs pre-existing correctly separated (Claims 3-4, 6). ✔
- `runner.py` `expected_tier` derivation pinned (Claim 5). ✔
- swarm recipe REGISTRY + STRATEGIES binding for `bare-review-v1` confirmed, with the validator assertions that gate a new `reflect-review` lens (Claims 7-8). ✔

The gap is closed. Synthesis can rely on this file's structural claims.

## Confidence Gate
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (of the sampled load-bearing subset)
- **Tool engagement:** Read: 5 | Grep: 1 (bash, reproduced the net-new grep) | Glob: 0 | Bash: 2 (grep + sed line extraction)
- No web research required — all claims are local-source-truth (Tavily-first rule not triggered).
- Scope note: this is a SAMPLED verification (8 load-bearing claims), per the spawn instruction to sample 5-6. The field-table rows and the twelve verbatim Click options were checked exhaustively against source; I did not re-open every one of the ~25 inline `config.py:NNN` resolution-line cites in the §1 table individually, but the surrounding ranges (L165-240) were read in full and are internally consistent. The two MINOR line drifts found suggest the residual unsampled cites may carry similar ±1-2 line cosmetic drift but no fabrication.

## Recommendations
1. Gap-fill PASSES — green light for synthesis to consume `09-reflect-config-cli-surface.md`.
2. (Optional, non-blocking) Author may correct the two MINOR line-number/path drifts (Issues 1-2) for citation hygiene; neither blocks synthesis.

## QA Complete
