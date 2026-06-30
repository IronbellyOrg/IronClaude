# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 statements + Round 2 rebuttals + Round 2.5 invariant probe)
- Convergence achieved: 86%
- Convergence threshold: 80%
- Focus areas: least-surprise, backward-compat, convention-fit, testability, blast-radius
- Advocates: 4 strategy positions across 2 issues

## Round 1: Advocate Statements

### Med-A · A-S1 (declarative `exists=True, file_okay=False`)
**Steelman of A-S2 first:** A body-level `ClickException` gives a branded message and can be unit-tested as a function — genuinely nicer UX copy.
**Position:** Change `init_lite.py:295` to `click.Path(exists=True, file_okay=False, path_type=Path)`. This is the *exact* pattern at `sprint/commands.py:179,390`. One line; Click rejects nonexistent/non-dir roots at parse time with exit code 2 (the correct class for a bad CLI argument) **before any body code runs**, so no dirs are ever created under a typo'd root. `default="."` always exists → default path unaffected.
**Concession:** Click's message is generic.

### Med-A · A-S2 (imperative `ClickException` guard)
**Steelman of A-S1 first:** Declarative is idiomatic and minimal.
**Position:** Keep the type; add `if not root.is_dir(): raise click.ClickException(...)` after `:335`. Branded message matches `:248,258`.
**Concession:** As placed (command body, post-`resolve()`), it protects the *same* scope as A-S1 with more lines, and only a future *extracted* helper would benefit — and no such helper exists today.

### Med-B · B-S1 (anchor relative `--output` to `root`)
**Steelman of B-S2 first:** Zero behavior change is the safest possible posture, and the existing echo at `:349` already prints the absolute landing path.
**Position:** At `:339`, anchor a relative `--output` to `root`: `out_path = (output if output.is_absolute() else root / output).resolve()`. This *resolves* the finding instead of narrating it. Crucially, when `--project-root` is the default `.`, `root == cwd.resolve()`, so the resolved path is **byte-identical** to today — the behavior change bites *only* the exact buggy case (`root != cwd` + relative output).
**Concession:** Requires a new regression test for the `root != cwd` case (which should exist anyway per review L3).

### Med-B · B-S2 (preserve CWD + document)
**Steelman of B-S1 first:** Anchoring to root is the least-surprise mental model.
**Position:** Keep `Path(output).resolve()`; add help-text + SKILL.md note that relative `--output` is CWD-relative; rely on the existing echo for visibility.
**Concession:** Does not remove the inconsistency the finding raises; the surprise is only visible *after* the write.

## Round 2: Rebuttals

- **Against A-S2:** The only durable advantage is message copy. Exit code 2 (A-S1) is *more* correct for an argument error than ClickException's exit 1. Convention-fit + minimalism dominate a cosmetic message. → A-S1 holds.
- **Against B-S2 (decisive, X-001):** "Document the surprise" fails the sufficiency bar — the finding asks for *consistency*, not a footnote. The echo fires *after* directories are created in the wrong place. → B-S1 holds; B-S2's doc value is grafted, not the base.

## Round 2.5: Invariant Probe (fault-finder)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Validation fires before any filesystem write/dir creation | ADDRESSED | HIGH | A-S1 rejects at parse (pre-body); B-S1 only computes a path (no I/O). `_write_report` still runs `_is_protected_context_path` |
| INV-002 | collection_boundaries | Existing-but-empty project still succeeds (A-001) — fix must reject only nonexistent/non-dir, never empty | ADDRESSED | HIGH | `exists=True, file_okay=False` accepts any existing dir incl. empty; B-S1 untouched by surface count |
| INV-003 | guard_conditions | B-S1 must not double-anchor an absolute `--output` | ADDRESSED | MEDIUM | `output if output.is_absolute() else root / output` branch guards it |
| INV-004 | interaction_effects | **`_is_init_lite_owned(root, out_path)` is root-relative, but CWD-relative `out_path` can diverge from `root` → `--force` ownership misclassifies when `root != cwd`** | UNADDRESSED-by-B-S2 / ADDRESSED-by-B-S1 | HIGH | `init_lite.py:115-126,253-256`: B-S2 leaves out_path CWD-anchored while ownership is root-anchored → latent second bug; B-S1 couples them, closing it |
| INV-005 | interaction_effects | A-S1 + B-S1 compose: root validated-to-exist before `root / output` anchoring | ADDRESSED | LOW | A-S1 guarantees `root` exists; B-S1 anchors to it |
| INV-006 | sufficiency_challenge | Does each winning fix ALONE green its finding? | ADDRESSED | HIGH | A-S1: typo→parse-reject→no dirs created (sufficient; residual "typo to an existing dir" is semantically-valid input, out of scope). B-S1: relative output now lands under audited project (sufficient). B-S2: FAILS — documents, does not fix |

**Invariant gate:** 0 HIGH UNADDRESSED items remain for the *winning* combination (A-S1 + B-S1 + B-S2 doc graft). INV-004 is HIGH and is *only* resolved by B-S1 — this is the strongest single argument against B-S2 as base.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence |
|------------|--------|-----------|----------|
| C-001 (Med-A locus) | A-S1 | 85% | Convention `sprint/commands.py:179,390`; minimal |
| C-002 (Med-A exit semantics) | A-S1 | 78% | Exit 2 correct for arg error |
| C-003 (Med-B inconsistency) | B-S1 | 84% | Resolves vs documents |
| C-004 (Med-B risk) | B-S1 | 80% | Blast radius confined to `root != cwd` |
| X-001 (sufficiency) | B-S1 | 88% | INV-006 + INV-004 |
| U-004 graft | B-S2 (into B-S1) | 75% | Doc clarification is additive value |

## Convergence Assessment
- Points resolved: 6 of 6
- Alignment: 86% (≥ 80% threshold)
- Status: CONVERGED
- Unresolved points: none
