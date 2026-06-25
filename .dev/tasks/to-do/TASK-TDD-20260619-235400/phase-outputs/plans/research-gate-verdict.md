# Research-Gate Verdict (Step 3.12) — TASK-TDD-20260619-235400

**Date:** 2026-06-20
**Consolidated verdict before fix:** FAIL (1 CRITICAL + 6 IMPORTANT directives + minors)
**Action:** Fixes applied. Re-verification pending in Step 3.13.

## Fix applied (C1 — CRITICAL)
Spawned a gap-fill Code Tracer agent → wrote `research/09-reflect-config-cli-surface.md` (`[CODE-VERIFIED]`). Closes the unexamined FR-RH2 new-input surface. Key corrections that synthesis MUST honor:
- **`ReflectConfig` lives in `models.py:57-91`** (config.py:24 imports it). Adding an FR-RH2 field is a 3-file edit: `models.py` dataclass (append at tail after `max_fix_iterations` L86), `config.py resolve_config()` (L123-240), `commands.py run()` (`@click.option` + signature + kwarg).
- **`--depth {standard|deep}` ALREADY EXISTS** — `commands.py:101-106` → `config.py:190` (floors `quick`→`standard`) → `models.py:71`. Do NOT re-add. (Corrects spec §4.2 implication.)
- **`expected_tier` derived in the runner** — `runner.py:403`: `2 if config.depth in {"standard","deep"} else 1`. Both depths → tier 2. Single mutation point if `deep` must differ.
- **`--transport` + `--reviewers` are 100% net-new** (zero occurrences in cli/reflect). Reuse the `--depth` `click.Choice` idiom for `--transport`; put the `--reviewers` `[2,4]` clamp + the `1`→negative-witness branch in `resolve_config` (house convention: resolution in config.py, not a Click callback). Branch the `1` sentinel BEFORE clamping or it gets rewritten to 2.
- **Recipe binding (closes I4):** reusing the already-registered **`bare-review-v1`** (`swarm/recipes/__init__.py` REGISTRY L182 + STRATEGIES L209) satisfies validator assertions 2 & 6 with ZERO recipe-package edits — recommended default. A new `reflect-review-v1` recipe is needed ONLY if reflect-review needs a different output shape than the bare-review findings table.

## Binding synthesis directives (I1-I6, I5 — recorded, no research-file rewrites needed)
These are forward-looking instructions for Phase 5 synthesis (carried so each synth agent honors them):
- **D1 (synth-04):** treat `02-reflect-contract-verdict.md` as AUTHORITATIVE/Complete; disregard file 05's stale "02 is a stub" framing (timestamp artifact).
- **D2 (synth-04):** the OI-1 correspondence table's left column = file 02's FULL verdict-driver field set (≥20 fields, not file 05's 7); right column = file 05's DM-012 swarm source (mostly "absent → synthesize/default in ensemble.py"). Flag every reflect field with no swarm source.
- **D3 (synth-06 §12 + synth-09 §22):** reconcile the `ensemble-empty` M==0 slug — it does NOT exist in `contract.py` today (BLOCKED reasons are contract-missing/child-crash/contract-version-missing/unknown-major-version/malformed-*). This collides with FR-RH2.7 "verdict map unchanged." Specify either a new `derive_verdict` M==0 BLOCKED branch (deliberate recorded change) or mapping M==0 onto an existing BLOCKED trigger; surface as an Open Question.
- **D4 (synth-03/synth-08):** specify the `reflect-review` recipe binding (reuse `bare-review-v1` recommended) AND note a net-new `lenses/reflect_review.py` LENS module is required (distinct from the recipe surface; none exists today).
- **D5 (synth-09 §22/OI-4):** carry `--suspect-source` emitted-but-unparsed-by-Mode-A as an Open Question (teach Mode A to parse, or keep advisory). `[CODE-CONTRADICTED]`, already research-tagged.
- **D6 (synth-06 §12):** carry the INV-005 arithmetic gap (`workers_failed` vs `workers_requested`) as an edge case.
- **D7 (synth-08 §19):** `ReflectConfig`'s 3-file edit location (models.py not config.py) is the migration mechanics; `--depth` pre-existing.

## Minors (no action)
Off-by-one whole-file line-count nits in prose (runner 598→597, merge 58→57, SKILL 81→80, process 354→353, LensEntry class L636→L637); all body `file:line` anchors verified correct (47/47 + 27/27 across the two evidence-QA agents).

**Post-fix status:** CRITICAL closed; directives recorded. Proceed to Step 3.13 verification round.
