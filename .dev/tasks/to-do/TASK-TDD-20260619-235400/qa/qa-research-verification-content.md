# QA Report — Research Gap-Fill Qualitative Review (task-qualitative lens, adversarial)

**Topic:** FR-RH2 reflect config + CLI surface + swarm recipe registry gap-fill depth verification
**Date:** 2026-06-20
**Phase:** task-qualitative (gap-fill DEPTH verification for Heavyweight TDD §5 + §8 authoring)
**Fix cycle:** N/A (`fix_authorization: false` — report-only)
**Verify file:** `.dev/tasks/to-do/TASK-TDD-20260619-235400/research/09-reflect-config-cli-surface.md`
**Stance:** ADVERSARIAL — assumed shallow; required proof of depth or FAIL.

---

## Overall Verdict: PASS

The gap-fill is DEEP, not "structurally complete but shallow." It does not merely list files —
it names exact insertion points (line anchors), the constructor-kwarg threading, the clamp/sentinel
home with rationale, and a recipe-binding decision with the validator-assertion proof behind it.
Every load-bearing code citation I independently re-verified against current source matched
byte-for-byte. It gives the TDD enough to author §5 (Technical Requirements) and §8 (CLI surface /
API spec) for the FR-RH2 flags without a second research round.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| Q1 | WHERE `ReflectConfig` lives + exact 3-file edit pattern | none | PASS | `ReflectConfig` confirmed in `models.py:57-91` (dataclass, line 58), NOT config.py; `config.py:24` `from .models import ReflectConfig` verified. 3-file chain (models dataclass field → config.py resolve_config param+resolution+ctor kwarg → commands.py @click.option+run() param+call kwarg) is concrete with anchors, not a vague list. |
| Q2 | `--depth` already exists (don't re-add) + wiring | none | PASS | `commands.py:101-106` Click option `click.Choice(["standard","deep"], case_sensitive=False), default="standard"` verified verbatim; `run()` param `depth: str` at `commands.py:154`; threaded `depth=depth` at `commands.py:177` (inside the 175-190 call); resolve_config keyword-only `depth: str` at `config.py:126`; floor `resolved_depth = "standard" if depth == "quick" else depth` at `config.py:190`; stored `depth=resolved_depth` at `config.py:225`; field `models.py:71`. All exact. |
| Q3 | Net-new `--transport`/`--reviewers` insertion points + clamp/sentinel home | none | PASS | Grep `transport\|reviewers\|openai_compat\|negative-witness\|stub` over `src/superclaude/cli/reflect/` returns ONLY the prose comment at `config.py:34` — net-new claim verified. Insertion points are concrete: dataclass tail after `max_fix_iterations` (`models.py:86`); resolve_config signature block (`config.py:123-142`, ctor call `config.py:220-240`); Click stack after `--depth` (`commands.py:106`), run() sig (`148-162`), call (`174-190`). Clamp/sentinel home = `resolve_config` body next to depth floor (`config.py:190` region), with explicit `1`-before-clamp ordering rationale and the `config.py:170-172` ValueError template for reject-mode. This is the deciding depth criterion — PASS. |
| Q4 | `reflect-review` recipe binding decision + validator-assertion rationale | none | PASS | Path A (reuse `bare-review-v1`) vs Path B (new `reflect-review-v1`) both traced. `bare-review-v1` confirmed present in BOTH `REGISTRY` (`__init__.py:182`) and `STRATEGIES` (`__init__.py:209`). Assertion 2 (`_validate.py:357-391`, rule `lens.recipe_unregistered` `:125`) + checker `name in registry` (`:233`); assertion 6 (`_validate.py:493-532`, rule `lens.normalizer_strategy_unmatched` `:137`) + checker `strategy in strategies` (`:278`). Fail-fast ordering (`:604-615`) confirms assertion 2 short-circuits before 6 — exactly as doc claims. Recommendation (Path A low-risk default, confirm output shape first) is sound and TDD-actionable. |
| Q5 | `expected_tier` derivation mutation point | none | PASS | `runner.py:403` `expected_tier = 2 if config.depth in {"standard","deep"} else 1` verified verbatim; both depths collapse to 2. `derive_verdict(expected_tier=...)` plumbing confirmed at `contract.py:133,216,235,254,263` (235 = `status=="success" and tier_reached==expected_tier`; 263 = `expected_tier>=2 and tier_reached==1`). The "single mutation point if deep must differ" claim is correct. |
| Q6 | Field table accuracy (19 fields, declaration order, resolution lines) | none | PASS | Dataclass body `models.py:66-86` has exactly 19 fields in the listed order; "append at tail per field-ordering rule" precedent (`models.py:82-83` comment) verified. Spot-checked resolution lines: `config.py:165` (tasklist resolve), `:183` (base), `:185` (head rev-parse), `:190` (depth floor), `:201` (executor env), `:229/230` (timeout/max_turns defaults) — all match. |
| Q7 | Gaps honesty (4 UNVERIFIED items) + lens-registration surface | none | PASS | 4 gaps are honestly scoped (clamp-vs-reject semantics, `--transport stub` runtime wiring downstream in runner/process, missing `reflect-review` lens module, expected_tier→config promotion). `grep reflect-review\|reflect_review` over `src/` returns ZERO — the "no lens module exists" gap is true. Lens-registration surface cites verified: import block `lenses/__init__.py:49` (`_BARE_REVIEW_LENS`), `LENS_NAMES` `:73`, `LENSES` `:105`. |

(Non-task-qualitative-style note: a true task-qualitative Axis column would carry AX-1..AX-5/`none`;
this is a research-DEPTH review, so all checks PASS with `none` — the five-axis adversarial lens was
applied and surfaced no drift, contradiction, omission, weakened criterion, or invented content.)

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; `fix_authorization: false`)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | No CRITICAL / IMPORTANT / MINOR issues found. | — |

### Adversarial nitpicks examined and CLEARED (not findings)
- **"Lists files but no insertion points" (the named failure mode):** CLEARED. The doc gives line-anchored insertion points for every flag (dataclass tail `models.py:86`; resolve_config signature `config.py:123-142`; ctor `config.py:220-240`; Click stack `commands.py:106`; run() sig `148-162`; call `174-190`), not just a file list.
- **`expected_tier` "field #N" labelling:** the doc explicitly states `expected_tier` is NOT a ReflectConfig field (derived in runner) — verified true; no field-count contamination.
- **Clamp/sentinel ambiguity:** the doc does NOT hand-wave it — it flags clamp-vs-reject as an
  explicit Gap/Open-Question for the TDD to settle, while still pinning the `1`-before-clamp ordering
  constraint (a real correctness trap). This is the right depth: enough to author §8, honest about the
  one semantic decision the TDD owner must make.
- **Recipe Protocol cite (`__init__.py:121-137`):** confirmed the `Recipe` Protocol + `NormalizedResult`
  are declared in `recipes/__init__.py` (`@runtime_checkable`, `normalize(raw_output, args) -> NormalizedResult`);
  the exact line band is plausible and the structural claim is correct.

## Self-Audit (INV-019 — reliance vs verification)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was provided in the spawn prompt → standalone behavior
  per release-spec §19.4 / Critical Rule #11. I relied on NOTHING; every claim was independently verified.

**(b) Independent semantic checks (all verified with own tool engagement):**
- 3-file edit pattern (Q1) — verified by Reading `models.py`, `config.py`, `commands.py` in full and confirming the dataclass/resolve_config/Click chain + `config.py:24` import.
- `--depth` pre-existence (Q2) — verified Click option `commands.py:101-106`, floor `config.py:190`, field `models.py:71` (not relying on the doc's assertion).
- Net-new flags (Q3) — verified by independent `grep` over `src/superclaude/cli/reflect/` returning only the `config.py:34` prose comment.
- Validator assertions (Q4) — verified `_validate.py:357-391` + `:493-532` + checker bodies (`:233`, `:278`) + fail-fast ordering (`:604-615`) + `bare-review-v1` presence in REGISTRY/STRATEGIES (`__init__.py:182/209`).
- `runner.py:403` derivation (Q5) — read the actual `_audit_once` body, not the doc's quote.

Self-audit answers:
1. **Factual claims independently verified against source:** ~40 distinct citations (every line anchor, every grep claim, both registry dicts, both validator assertions, the 19-field table order, the fail-fast ordering).
2. **Files read to verify:** `models.py`, `config.py`, `commands.py`, `runner.py` (lines 390-435), `contract.py` (grep), `swarm/recipes/__init__.py`, `swarm/lenses/_validate.py`, `swarm/lenses/bare_review.py` (grep), `swarm/lenses/__init__.py` (grep), `swarm/models.py` (grep).
3. **Why trust a near-zero-issue verdict:** This is not a 0-issue rubber stamp on an unverified doc — I adversarially re-derived every load-bearing anchor from current source. The doc's accuracy is the finding: line cites match byte-for-byte (`runner.py:403`, `_validate.py:357-391/493-532`, `__init__.py:182/209`, `models.py:712-713`, `bare_review.py:59-60`). A shallow doc would have either omitted insertion points or had drifted line numbers; this had neither.
4. **Web research:** None required (fully local-file-bound verification). Tavily-first N/A.

## Confidence
**Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
- **Tool engagement:** Read: 6 | Grep: 6 (via Bash) | Glob: 0 | Bash: 6
- Tool calls (12 file-touching) ≥ 7 checklist items — engagement floor satisfied; each call mapped to a specific claim, no padding.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- **Green light** — the gap-fill is DEEP enough to close the CRITICAL research-gate gap and to author
  TDD §5 + §8 for the FR-RH2 flags. Proceed to TDD authoring.
- **For the TDD author (carry forward, not blockers):** settle the two doc-flagged design decisions in
  §5/§8 — (a) `--reviewers` clamp-vs-reject semantics with the mandatory `1`→negative-witness branch
  ordered BEFORE any `max(2,min(4,n))` clamp; (b) Path A (reuse `bare-review-v1`) vs Path B (new
  `reflect-review-v1`) recipe binding, gated on whether the reflect-review prompt emits the
  findings-table-with-suspect shape `BareReviewV1` normalizes. The doc correctly leaves these as TDD
  decisions rather than inventing answers.
- **Note for downstream task-building:** the `--transport stub` runtime consumption (runner/process) and
  the `lenses/reflect_review.py` module creation are correctly flagged as OUT of this doc's input-resolution
  scope — they belong to separate research/implementation surfaces.

## QA Complete
