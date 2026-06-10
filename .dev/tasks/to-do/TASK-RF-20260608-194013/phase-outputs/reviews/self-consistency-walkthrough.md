# Self-Consistency Walkthrough (Step 5.3)

- **Date:** 2026-06-09 · **HEAD:** `ab2dae1a` · **Files:** `src/superclaude/skills/task-builder/SKILL.md`, `src/superclaude/agents/rf-qa.md`
- **Method:** grep/read the edited surfaces and assert cross-surface agreement. All evidence is live-line-cited.

## (a) `reflect_post_mode` 8-value set is identical across all surfaces — **PASS**

The load-bearing token `auto-resolved-2-degraded-halt` (the 8th value, OQ-1) is present on every surface; no surface lists only 7:

- SKILL.md A.9 fallback ladder prose `:1082`; `REFLECT_POST_MODE` component doc `:1922`; frontmatter field `:2001`; mode-conditional sentinel comment `:2002`; §6.4 template header `:2087`; §6.5 auto-resolved `:2096`; dial-aware validation bullet `:2148`; Critical Rule 19 `:2205`; depth-reconciliation note `:2260`.
- rf-qa.md TB-Add-9: per-mode active map `:385`; V2 8-value enumeration `:388`; V16 `:398`; MODE-MATCH `:401`.

The full 8-value union `{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt, auto-resolved-2-degraded-halt}` is enumerated verbatim in the SKILL.md frontmatter doc (`:2001`) and rf-qa V2 (`:388`).

## (b) §9.2 per-mode active map ⇆ §9.3 MODE-MATCH agree — **PASS**

In rf-qa.md TB-Add-9 the active map and MODE-MATCH are mutually consistent:

- `none` → active {V1,V2,V3}; MODE-MATCH `none ⇒ V3` (subset, consistent).
- `1`/`auto-resolved-1` → active {V1,V2,V3,V4,V5,V6,V9,V11,V12,V13,V14}; MODE-MATCH `1/auto-1 ⇒ V5 ∧ V6 ∧ V9` (the shape-determining subset).
- `2`/`auto-resolved-2` → active {V1,V2,V3,V4,V7,V8,V10,V11,V12,V13,V14}; MODE-MATCH `2/auto-2 ⇒ V7 ∧ V8 ∧ V10`.
- `halt`/`2-degraded-halt`/`auto-resolved-2-degraded-halt` → active {V1,V2,V3,V4,V15,V16}; MODE-MATCH `halt/degraded ⇒ V15 ∧ V16`.

The MODE-MATCH shape subsets are exactly the mode-discriminating assertions inside each row's active set. Consistent.

## (c) Every spec §13 acceptance row maps to an emitted-template property or a V-assertion — **PASS (with expected unreachable-AT note)**

| AT | Surface |
|---|---|
| AT-FR1 (token parse / MALFORMED) | A.9 producer token-validation prose (SKILL `:1058`–region) |
| AT-FR2 (`none` suppression) | §6.1 (`:2085` region) + V3 |
| AT-FR3 (Mode 1 inline) | §6.2 template + V5/V6/V9 |
| AT-FR4 (Mode 2 wrapper) | §6.3 template + V7/V8 |
| AT-FR5 (auto determinism) | A.9 RESOLVE_AUTO predicate + V2 |
| AT-FR6 (old→new map) | A.9 §5 alias-map prose |
| AT-FR7 (HALT + write-back) | V11/V12 |
| AT-FR8 (`--remediate` scope) | V9/V10 |
| AT-FR9 (single-producer consistency) | MODE-MATCH (TB-Add-9) |
| AT-FR10 (wrapper-absent fallback) | A.9 ladder + V16 |
| AT-FR11 (Mode 1 nesting guard) | §6.2 Verification + FR-11 precondition |
| AT-FR12 (`--spec` threading) | V13 (Mode 1) + §6.3 `spec_path` passthrough (Mode 2) |
| AT-FR13 (fixed-1 advisory) | A.9 §10.4 WARNING prose |
| AT-VALIDATION-1 / AT-MISMATCH-1 / AT-PLUMBING-1 | bounded fixture test (Step 5.5) |

**Expected unreachable ATs:** ATs requiring a `build_tasklist()` end-to-end harness (full cross-implementer auto-determinism over a live MDTM) have **no automated surface** — the builder is an LLM-driven markdown emitter with no callable entry point (research 06). This is expected/acceptable; the mechanically-testable ATs are covered by TB-Add-9 (validation-time) and the Step-5.5 fixture (string/content assertions).

## (d) MODE-MATCH lives in rf-qa.md TB-Add-9, NOT in Critical Rule 12 — **PASS** (OQ-6)

`grep "MODE-MATCH"` returns rf-qa.md `:380/:399/:401` (authored) and SKILL.md `:2148/:2205` (REFERENCES to TB-Add-9 as the authority — not an authored assertion). Critical Rule 12 (SKILL.md `:2191`, retry counters) contains **no** MODE-MATCH. The spec's `:2094` citation imprecision (OQ-6) is correctly handled — the assertion is authored in the rf-qa task-integrity gate, not bolted onto the retry-counter rule.

## (e) §6.3 Mode-2 `--spec` passthrough references an asserted frontmatter field — **PASS** (FR-12)

The §6.3 Mode-2 Action (`:2082`) derives `--spec` "from frontmatter `spec_path`"; the `spec_path:` field is present in the Step-3.1 Output-Structure frontmatter template (`:1990`, pre-existing, retained). So Mode-2 spec threading is not silently dependent on an unasserted field (V13 covers the Mode-1 `--spec`; this confirms the Mode-2 source exists).

## Verdict

All five assertions **PASS**. No contradiction found across the four mode-bearing surfaces (frontmatter doc, Rule 19, validation bullet, rf-qa TB-Add-9). The 8-value oracle is uniform; the active map and MODE-MATCH agree; MODE-MATCH is correctly located; Mode-2 spec threading is grounded.
