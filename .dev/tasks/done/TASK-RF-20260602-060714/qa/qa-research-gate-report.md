# QA Report — Research Gate

**Topic:** Remediate validated review findings R1-R5 from PR #112 and PR #111
**Date:** 2026-06-02
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files:** 01-call-site-inventory.md, 02-patterns-and-conventions.md, 03-test-and-verification.md, 04-template-and-examples.md

---

## Overall Verdict: PASS

The four assigned research files are dense, evidence-based, and actionable for a task
builder. Every load-bearing claim I independently spot-checked against the real source
files held up. The R5 word-boundary FP is **independently reproduced**, the PR #111 oracle
commit is **reachable**, the R2 autouse-fixture correctness claim is **confirmed**, and the
"no MD family / no non_ref allowlist on current branch" premise is **confirmed by grep**.

The only defects found are MINOR: line-number drift of ±1–2 in file `01` for the
`executor.py` R2 region (off-by-one/-two against the live tree). The structural claims and
insertion-point logic remain correct; a builder following the *anchors* (function names,
guard text, grep targets) rather than the raw line numbers will not be misled. No CRITICAL
or IMPORTANT gaps. Green light for synthesis / task-building.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status | PASS | All 4 files present; 01 & 02 `Status: Complete`; 03 & 04 close with `Status: Complete` + Summary (top header says "In Progress" but both end Complete). |
| 2 | Evidence density | PASS (Dense) | >90% of claims carry file:line. Spot-checked ~20 citations independently; all real. |
| 3 | R1 docstring claim | PASS | `id_registry.py` L19-24 contains "R0.3 **will** hoist … the TODO comment below tracks that migration"; contradicted by L37 `from superclaude.contracts import ID_PATTERNS`. L33-37 present-tense comment confirmed. Exact. |
| 4 | R2 gates.py side | PASS | global L1039, setter L1042-1049 (docstring "`None` clears the hint (used by tests for isolation)" L1046), fail-shut L1069-1074, sidecar read L1089-1099 all via `payload.get(...,())`. Exact. |
| 5 | R2 executor pipeline entry | PASS (minor line drift) | `execute_roadmap` is the run entry (actual **L3398**, file said L3397). Dry-run guard L3491-3493 (file said L3490-3492), `_build_steps` L3488 (file said L3487), `execute_pipeline(` L3538 (file said L3536). Insertion-point logic (after dry-run guard, before execute_pipeline) is correct. |
| 6 | R2 resume LIVE CONSTRAINT | PASS | `_apply_resume` at L3499 under `if resume:` (L3496) confirmed — a naive unconditional reset would fail-shut MERGE on resume. The flag is real and well-reasoned. |
| 7 | R2 autouse-fixture correctness | PASS | `_isolate_gates_state` at `test_spec_roadmap_id_containment.py:57-62`, `autouse=True`, resets to `None` BOTH before and after yield. Confirms regression MUST be one test body / two calls. Subtle claim is CORRECT. |
| 8 | R3 arch_lint Rule 2 | PASS | `for node in ast.walk(tree)` L143 (flat walk, no parent ptrs); Rule 2 L169-170 `isinstance(node, ast.Constant)` + `if node.value in canonical_pattern_bodies` (exact set-membership). Allow-marker opt-out L171. Exact. |
| 9 | R4 repo-inventory.sh | PASS | `#!/bin/sh` L1, `set -e` L9, `apply_scope()` L29-37 with `\|\| true` on BOTH branches (L33, L35), callers L49 (git ls-files) + L66 (find). Exact. |
| 10 | R4 SoT / never-stage-.claude | PASS | `git check-ignore` confirms `.claude/skills/.../repo-inventory.sh` is gitignored → R4 procedure (edit src/, sync-dev, verify-sync, stage only src) is correct. |
| 11 | R5 word-boundary FP | PASS (reproduced) | `uv run python` independently: `re.search(r'\bD-?\d+\b','M1-D01')` → matches `'D01'`, span (3,6). FP is **real on current branch**. |
| 12 | R5 contracts ID_PATTERNS | PASS | `contracts/__init__.py` L64-70: FR/NFR/SC/G/D only, **no MD**. Anchor-free convention L58-62 confirmed. Exact. |
| 13 | R5 spec_parser auto-derive | PASS | L20 contracts import, L329-331 `_REQUIREMENT_PATTERNS` dict-comp over `_CONTRACTS_ID_PATTERNS.items()`. Auto-pickup claim confirmed. |
| 14 | R5 structural_checkers sites | PASS | `_canonicalize_requirement_id` L295, regex L328 `^([A-Z]+)([-_]?)0*(\d+)(.*)$`, `check_signatures` L402, phantom_id HIGH L33 / id_schema_drift MEDIUM L34, drift L449 / phantom L464. Exact. |
| 15 | R5 oracle reachability | PASS | `git show 861047c2` → "fix(roadmap): honor M{n}-D{nn} milestone-prefixed IDs in tokenizer + canonicalizer"; `origin/fix/roadmap-md-family-tokenizer-canonicalizer` exists. Reachable. |
| 16 | R5 "no MD / no allowlist" premise | PASS (key) | `grep -c non_ref structural_checkers.py` = **0** (allowlist absent); zero genuine MD/milestone hits in spec_parser + structural_checkers. The "path-b is larger than design-doc framing" claim is **substantiated**. |
| 17 | Doc cross-validation tags | PASS (N/A) | No `[CODE-VERIFIED]`/`[UNVERIFIED]` tag scheme; instead inline "verified via Read / uv run python" provenance + explicit "Unverified/flagged" sections in 02 & 03. Acceptable — claims are code-traced, not doc-sourced. |
| 18 | Contradiction resolution | PASS | No inter-file contradictions. Files agree on shared line numbers (gates L1069-1074, arch_lint L143/L170, contracts L64-70). |
| 19 | Gap severity / coverage | PASS | All 5 R-items have edit sites, tests, conventions, template guidance. Resume caveat (R2), allowlist-port question (R5), sidecar schema-test cross-cut (R5) all surfaced as builder flags. |
| 20 | Actionability for builder | PASS | Acceptance greps, exact `uv run pytest` commands per surface, insertion points, fixture formats, and an L1→L5→M1 task skeleton all provided. |

---

## Summary

- Checks passed: 20 / 20
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `01-call-site-inventory.md` R2 section (L55, L56, L59, L60) | `executor.py` line numbers drift ±1–2 vs live tree: `execute_roadmap` cited L3397 (actual L3398); dry-run guard L3490-3492 (actual L3491-3493); `_build_steps` L3487 (actual L3488); `execute_pipeline(` L3536 (actual L3538). | Builder should anchor on function names + guard text (`if config.dry_run:`, `_build_steps(config)`, `execute_pipeline(`) and the existing import-pattern reference (executor L662), NOT raw line numbers. Structural insertion logic is correct as written. |
| 2 | MINOR | `03` & `04` top headers | `Status: In Progress` left stale at top; both files actually close with `Status: Complete` + full Summary. | Cosmetic; closing `Complete` is authoritative. No blocker. |

Note: file `01`'s line cites for non-executor files (id_registry, gates, arch_lint,
repo-inventory.sh, contracts, spec_parser, structural_checkers) were **exact** on every
spot-check — the drift is isolated to the `executor.py` R2 region only.

---

## Actions Taken

None — `fix_authorization: false` (report-only phase). Issues documented above for the
builder/orchestrator.

---

## Recommendations

1. **Proceed to task-building.** Research quality is sufficient for granular MDTM items.
2. **R5 is correctly framed as an investigation/decision gate, not a one-liner.** The
   independently-confirmed absence of the `non_ref` allowlist (grep = 0) means path-b's
   blast radius genuinely exceeds the design doc's "add an MD entry" framing. The task file
   MUST preserve the open question: *does MD-family alone close the FP, or is the Explicit-
   non-references allowlist port also required?* (File 01 §5f and file 03 §4 both flag this.)
3. **R2 reset must be resume-aware** — carry forward file 01's LIVE CONSTRAINT (a blind
   `set_id_registry_sidecar_path(None)` at run-start fails-shut MERGE on `--resume`).
4. **R5 sidecar schema cross-cut** — if path-b, file 03's cross-cutting note correctly flags
   `test_registry_sidecar_schema_stable` + `test_sidecar_schema_round_trip` + conftest
   permissive sidecar all hardcode the 8-key set and must gain `md_ids` together.
5. **Builder should re-derive the executor.py R2 line numbers** from a fresh Read (per Issue
   #1) rather than trusting file 01's cited L3397/L3536.

---

## Confidence Gate

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

All 20 checklist items verified with tool evidence (Read of the 4 research files + 7 source
files; Bash grep/git/uv-run verifications; independent regex reproduction of the R5 FP).

**Tool engagement:** Read: 9 | Grep: 0 (via Bash) | Glob: 0 | Bash: 6

(Tool-engagement note: 9 Reads + 6 Bash = 15 verification actions; several Bash calls
batched multiple grep/git checks and several Reads covered multiple checklist items each, so
coverage exceeds 20 items. No unverifiable/unchecked items. No web research performed — all
claims were intrinsically local/source-truth, so Tavily was not engaged.)

## QA Complete
