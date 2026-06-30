# Base Selection

## Per-issue winners

| Issue | Winner | Combined score | Runner-up | Margin | Tiebreaker |
|-------|--------|----------------|-----------|--------|------------|
| Med-A | **A-S1** (declarative `exists=True, file_okay=False`) | 0.88 | A-S2 (0.71) | 17% | not needed |
| Med-B | **B-S1** (anchor relative `--output` to root) | 0.86 | B-S2 (0.62) | 24% | not needed |

## Scoring rationale (qualitative dimensions)

**Med-A → A-S1**
- Convention-fit: 1.0 — byte-identical to `sprint/commands.py:179,390`.
- Blast-radius: 1.0 — one-line type change; `default="."` keeps default behavior.
- Correctness: 1.0 — usage error (exit 2) is the correct class; fires before any I/O (INV-001).
- Edge/invariant: preserves the empty-but-real-project case (INV-002 / A-001).
- A-S2 loses only on extra lines + convention divergence; its sole win (branded message) is cosmetic.

**Med-B → B-S1**
- Sufficiency: 1.0 — actually resolves the misplacement (X-001, INV-006); B-S2 only documents it.
- Backward-compat: high — identical behavior when `--project-root` is default `.`; change confined to `root != cwd` + relative output.
- Interaction coverage: B-S1 *also* closes the latent `--force` ownership divergence (INV-004, HIGH) that B-S2 leaves open — decisive.
- B-S2 is not discarded: its **help-text/SKILL.md clarification (U-004) is grafted onto the B-S1 base**.

## Strengths to incorporate (merge plan seed)
1. Base = A-S1 + B-S1.
2. Graft U-004 (B-S2): update `--output` help text + SKILL.md §4 to state relative values resolve against `--project-root`.
3. Add the regression tests both findings imply (also discharges review finding L3's `--output`/`--project-root` test gap).

## Edge-case floor
All winning options score ≥1/5 on Invariant & Edge Case Coverage (INV-001..006 addressed). Floor satisfied; no suspension.
