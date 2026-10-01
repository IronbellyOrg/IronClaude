# QA Report — Research Gate (Partition P1: Module-Build Cluster)

**Topic:** FR-DRS deterministic runtime-surface sweep module + product/eval/SKILL integration
**Date:** 2026-06-22
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false

**Assigned files (P1):**
- 01-module-design-and-spec-port.md
- 02-product-path-integration-seam.md
- 03-consumer-wiring-contract-and-prefilter.md
- 04-audit-reuse-sources-and-adaptation.md

**Also read:** research-notes.md, TDD §5.1/§6/§7/§8

---

## Confidence

**Verified:** 6/6 gap-checklist items | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100%

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 6 (each Bash call independently re-verified a specific source claim: ReflectConfig fields, contract.py halt sets, runner chokepoint+diff, SKILL §0.5d/§489, FR/NFR matrix, partition-scope boundaries). No web research performed (all claims local-source-bound).

---

## Scope Note (Partition P1 of 2)

P1 = module-build cluster: files 01 (module design/spec port), 02 (product seam), 03 (consumer wiring), 04 (audit reuse). FR/NFR in P1 scope per the spawn prompt: module FR-001/002/003/004/007/009/010/012; product wiring FR-005/006; hygiene NFR-001..007. FR-008 (eval) is file 05/P2; FR-011 (SKILL demotion) is file 06/P2 — NOT assessed here except for cross-references.

[PARTITION NOTE: Cross-file checks (R1↔R2 contradiction, scope coverage) limited to the 4 P1-assigned files + cited sources. Full cross-file verification across all 8 research files requires merging P1+P2 partition reports.]

---

## Gap-Checklist Results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FR/NFR coverage traceable to research | PASS-with-gaps | Every P1-scope FR/NFR maps to a research file (table below). 2 coverage softspots: availability-surface Python-path source (G-IMP-1), R1↔R2 arg-construction contradiction (G-IMP-2). |
| 2 | run_sweep arg-construction GAP fully characterized w/ remediation | PARTIAL | R2 fully characterizes `diff` + `scope_worktree` with concrete remediations; `availability_surface` is flagged + has a stopgap remediation but the SKILL-Wave-0-vs-Python-path bridge is uncharacterized (G-IMP-1). |
| 3 | Findings actionable for a builder | PASS | R2/R3/R4 give file:line + concrete code blocks; R1 gives pinned signatures + per-unit degrade rules. Builder-item maps present (01 §9, 04 §6). |
| 4 | Missing module↔caller integration details | PASS | R2 §1-§5 pins the exact insertion point (runner.py:444→445), both tier author paths, fix-loop re-audit, writer convention. Verified against live runner.py. |
| 5 | How diff obtained / Wave-0 surface obtained / LSP absence handling | PARTIAL | diff: R2 resolves (compute `git diff config.base`). LSP absence: R1 §1-Unit2 fully specifies (6 absence triggers → DEGRADE-to-floor + auditable marker) — PASS. Wave-0 surface obtain on Python path: GAP (G-IMP-1). |
| 6 | Count-invariant guard BLOCKED-routing specified enough | PASS | R3 §3 gives a concrete `Verdict.BLOCKED` block + `malformed-runtime-surface-count` slug, mirrored on the verified contract.py:200-209 fail-closed pattern; marked RECOMMENDED with builder-consensus note on slug. Actionable. |

---

## FR/NFR Coverage Traceability (P1 scope)

| FR/NFR | Covered by | Status |
|--------|-----------|--------|
| FR-001 (ledger every run) | 01 §3 step 8, §1.6; 02 §2 | TRACED |
| FR-002 (six scalars exact name) | 01 §7 + prefix caveat; 02 §2.2; 03 §6 | TRACED |
| FR-003 (count invariant by construction) | 01 §5.2; 03 §3 (consumer guard) | TRACED |
| FR-004 (7-step algorithm) | 01 §1, §4, §8 | TRACED |
| FR-005 (product path writes before consume) | 02 §2, §3 (chokepoint runner.py:444→445) | TRACED + source-verified |
| FR-006 (§5.3 derived `surface_unreached`) | 03 §4 + §15.4a truth table | TRACED |
| FR-007 (safety — never clean-pass) | 01 §8 governing posture; SKILL:489 quoted in 06 | TRACED |
| FR-009 (degrade-oracle never Regression) | 01 §4 + §1-Unit4 ("never increment regression") | TRACED |
| FR-010 (fail-open backend → DEGRADE) | 01 §1-Unit2; 03 §1 (token add); 04 §2 | TRACED + source-verified |
| FR-012 (non-surface fast path) | 01 §3 step 3 FAST PATH | TRACED |
| NFR-001 (full determinism) | 01 §6.2 determinism levers | TRACED |
| NFR-002 (idempotency across re-audits) | 02 §3 (fix-loop re-audit runner.py:562) | TRACED + source-verified |
| NFR-003 (no network / writes under `<output>/`) | 01 (implied); 04 §5.1 | PARTIAL — no P1 file explicitly asserts the NFR-003 "no socket/HTTP" static-analysis acceptance criterion as a builder item (G-MIN-2) |
| NFR-004 (atomic writes) | 02 §5; 04 §5.1 | TRACED + source-verified |
| NFR-005 (yamllint-safe `_IndentDumper`) | 02 §5; 04 §5.1 | TRACED + source-verified |
| NFR-006 (`evidence_ref` re-readable) | 01 §2.3 (RuntimeSurfaceLedgerRow note) | TRACED |
| NFR-007 (UV/sync/format hygiene) | 01 §9 scaffold note; research-notes PATTERNS | TRACED |

All 11 P1-scope FRs and 7 NFRs are traceable. No FR/NFR is entirely unexamined. Two are softspots (NFR-003 acceptance-criterion item; the two IMPORTANT gaps below).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| G-IMP-1 | IMPORTANT | 01 §3 line 139; 02 §1 `availability_surface` row + §7; cross-cut | **`availability_surface` Python-path source is uncharacterized.** SKILL §0.5d (SKILL.md:242, verified) defines a four-field Wave-0 availability surface — but it is derived *inside the LLM skill execution*, NOT on `ReflectConfig`. `run_sweep` is called from `runner._audit_once`, which runs in the **Python CLI wrapper**, outside the LLM Wave-0 context. Grep confirmed ZERO `availability\|wave\|probe` matches in config.py/models.py/runner.py. R2 flags the gap and offers a stopgap (pass `{}` floor-forcing empty dict), but no P1 file explains how the Python product path actually obtains the SKILL-derived Wave-0 surface, or confirms that an empty/floor surface is the accepted v1 behavior for the runner-driven path. A builder cannot write a correct `availability_surface=...` item from this research. | Add a research finding (or task Open Question) that resolves: does the runner-driven path (a) build its own minimal availability probe in Python, (b) read a serialized Wave-0 surface the child wrote, or (c) pass a floor-forcing empty dict as accepted v1 behavior? Cite which. This is the same class of gap R2 correctly caught for `diff`/`scope_worktree` but left half-resolved for `availability_surface`. |
| G-IMP-2 | IMPORTANT | 01 §3 line 139 vs 02 §1 KEY FINDING / §7 | **R1↔R2 contradiction on arg construction.** File 01 line 139 restates the TDD verbatim: "`diff`/`base_ref` from `ReflectConfig` audit inputs ... `availability_surface` from the Wave-0 probe on the config." File 02 §1 explicitly found this **wrong against current source** — there is NO diff-text field, NO `scope_worktree` field, NO availability probe (I independently re-verified: `models.py:66-98` has `base`/`tasklist_path`/`output_dir` only; no diff/worktree/availability field; runner.py never computes a unified diff, only passes `--diff config.base` as a ref at runner.py:356). A builder reading file 01 alone would write an incorrect "read availability_surface off the config" item. R1 does delegate ("R2 owns the seam detail") and R2 is correct, so this is not fatal — but an unresolved contradiction between two research files on the same question is a zero-tolerance surface. | Reconcile: either (a) annotate 01 §3 line 139 that the TDD's "already on the config" phrasing is superseded by R2's source-verified finding (3 of 6 args have NO backing field), or (b) have the builder treat 02 §1 as authoritative for arg construction and 01 §3 as the algorithm-flow view only. The builder MUST NOT source `diff`/`scope_worktree`/`availability_surface` "from the config" as 01 §3 line 139 literally states. |
| G-MIN-1 | MINOR | 04 frontmatter line 5 (`**Status:** In Progress`) vs 04 line 265 (`## Status: Complete`) | **File 04 status field is stale/internally inconsistent.** The frontmatter declares "In Progress" while the body's closing status declares "Complete." Checklist item 1 requires every research file to carry Status: Complete. The substance reads complete (TL;DR + 6 sections + per-row disposition + builder action items + summary), so this is a header-hygiene defect, not a content gap — but under zero-tolerance it is a finding. | Update 04 frontmatter line 5 to `**Status:** Complete` to match the body. |
| G-MIN-2 | MINOR | NFR-003 coverage | **NFR-003 "no network" acceptance criterion not surfaced as a builder concern.** The TDD NFR-003 acceptance criterion requires "static analysis confirms zero socket/HTTP/MCP-network calls." No P1 file calls this out as a verification item (04 §5.1 covers writer deps; 01 implies local-only but does not name the no-network static-analysis check). Low impact because the module is pure-Python-local by design, but the explicit acceptance gate is untraced. | Optional: add a one-line note (likely in the test-pattern file 07/P2, but flagged here since NFR-003 is module-scope) that the module-build phase carries a "no network I/O" static check per NFR-003 AC. |

---

## Notable Strengths (adversarial cross-check passed)

These were checked hard and held up against live source — recorded so a 0-CRITICAL verdict is credible, not lazy:

- **R2's 3-gap arg-construction finding is CORRECT and high-value.** Independently re-verified: `ReflectConfig` (models.py:57-98) has no `diff`/`scope_worktree`/`availability_surface` field; runner.py:356 passes `--diff config.base` as a single ref and never materializes a unified diff; config.py:95 docstring confirms the diff is computed "downstream" (by the child). R2 caught a real TDD-vs-source contradiction and gave concrete remediations for 2 of the 3.
- **R3's contract.py wiring is byte-accurate.** `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33) contains exactly the 5 tokens R3 quoted; the `any(...)` membership fires `"degraded-components"`; the 200-209 fail-closed bool block exists as the model for the count-invariant guard; the `deviations["regression"] > 0 → "regression"` branch exists. The I7 "no 5th deviation class" reuse strategy is sound.
- **R4's reuse/inversion semantics are precise.** The `_bfs_reachable` depth=1-at-call-site + DEGRADE-on-partial inversions, the `_TEST_PREFIXES`/`_TEST_INFIXES` unknown→SOURCE→DEGRADE inversion, and the `_DYNAMIC_PATTERNS` KEEP:monitor→DEGRADE inversion are all clearly specified with the builder-trap flag (depth>50 guard is module-parse, NOT the BFS).
- **LSP-overlay absence handling (checklist item 5) is fully specified** in 01 §1-Unit2: six concrete absence triggers → DEGRADE-to-floor with an auditable marker; floor stays ground truth (never load-bearing). Actionable.
- **Count-invariant guard BLOCKED-routing (checklist item 6) is specified enough**: R3 §3 gives the `Verdict.BLOCKED` + `malformed-runtime-surface-count` block; the only soft edge is the slug name deferred to builder consensus, which R3 correctly flags rather than hides.

---

## Overall Verdict: FAIL

**Rationale:** Per the research-gate zero-tolerance rule, ANY gap of any severity = FAIL. P1 research is strong (no CRITICAL gaps; all P1-scope FR/NFR traceable; the hardest seam question — the 3-arg construction gap — was caught correctly by R2), but two IMPORTANT gaps and two MINOR gaps remain to be resolved before synthesis:

- **G-IMP-1** (IMPORTANT) — `availability_surface` Python-path source uncharacterized.
- **G-IMP-2** (IMPORTANT) — R1↔R2 contradiction on arg construction (file 01 line 139 restates a source-false TDD claim).
- **G-MIN-1** (MINOR) — file 04 frontmatter Status "In Progress" vs body "Complete."
- **G-MIN-2** (MINOR) — NFR-003 no-network static-analysis acceptance criterion not surfaced.

All four are resolvable with small targeted edits (no re-research of a whole topic required). G-IMP-1 and G-IMP-2 are the load-bearing ones — both concern `run_sweep` arg construction, the single most builder-critical seam in the module-build cluster.

## QA Complete
