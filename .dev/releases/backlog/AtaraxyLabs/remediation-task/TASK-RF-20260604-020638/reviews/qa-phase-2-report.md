# QA Report — Phase-Gate (Phase 2: HIGH fixes H1–H6)

**Topic:** Ataraxy-Labs eval release plan — reflect UC-1 HIGH-finding remediation
**Date:** 2026-06-04
**Phase:** phase-gate (post Phase 2)
**Fix cycle:** N/A (first QA pass; fix_authorization: true)
**Target under review:** `.dev/releases/backlog/AtaraxyLabs/merged-requirements.md`
**Stance:** Adversarial / zero-trust. Every claim re-verified against the real file via Read + grep; no prompt assertion trusted.

---

## Overall Verdict: PASS (after 3 in-place fixes)

All six HIGH acceptance criteria are met in the real file. Three real defects were found by adversarial cross-reference checking and **fixed in-place** (within docs-only authority). One non-blocking observation about non-target file mtimes is logged (outside fixable scope; not a content defect attributable to Phase 2 work).

---

## Per-Finding Verdicts (H1–H6)

| Finding | Verdict | Evidence (file:line / grep) |
|---------|---------|------------------------------|
| **H1** | PASS (after fix) | §3 terminal-state rule @ L110-119; §8.2 @ L282 "inspect KILL is a terminal state ... does not block weave". §3↔§8.2 reconciled. **BUT §14 (L392-393) still carried the original contradiction "Blocked until inspect S4 live+KEEP" — FIXED in-place.** |
| **H2** | PASS | `grep -i owner` → L197 real assignment: "the solo release operator — IronClaude fork maintainer (`RyanW`)". Tie-break resolver @ L201-210 (default KILL-pending-second-pass). §5 prior content (metric groups L169-191) preserved. Tags `[V2]`/`[V2+MERGE]` intact. No placeholder. |
| **H3** | PASS | `grep -iE security\|egress\|secret` → §11.5 @ L330. Covers all three: data-egress path + provider retention (L338-344), secret-scrubbing pre-flight (L346-351), private-fork→3rd-party stance CONDITIONAL (L353-360). §12/§13/§14 still numbered 12/13/14 (L362/377/388) — clean §11.5 insert, no renumber/corruption. Tagged `[MERGE]`. No placeholder. |
| **H4** | PASS | §7 @ L241-256 names concrete solo-operator mechanism: randomized tool naming + LLM adjudicator with provenance-stripped artifacts (evidence-validator pattern) + de-anon after scoring. No longer assumes a human panel ("automated, not a human panel" L244). Rest of §7 (ground-truth tiers L236-239, statistical guards L258-261, tiered minimums L263-265) preserved. Tags intact. No placeholder. |
| **H5** | PASS | §2 G0-1 row @ L66 = "**FIRST Phase-0 action** = the fork PR/merge-count inventory". Backfill method @ L77-84 seeded from §11 curated-defect list. "~30 merge commits + ~150 Python commits" @ L75 (corpus not empty). Consistent with §7 tiered minimums (5PR/3merge, 20PR/10merge) @ L263-265. Existing G0-2/G0-3/G0-substrate rows preserved. Tags `[MERGE]`. No placeholder. |
| **H6** | PASS (after fix) | §4 Runner I/O contract @ L143-153 (input record → normalized JSON output schema). Restored artifacts: `latency-harness.sh` [V3] @ L158, install matrix w/ glibc/musl rows @ L162-165, token-counter [V3] @ L166. §14 Phase-0 1–2d estimate ties to these (L155-156 ↔ L390). V3 content tagged `[V3]`. Existing §4 scenario matrix + harness-component list preserved. **BUT L167 had dangling "(see M2)" — an external audit finding-ID with no in-doc anchor — FIXED in-place.** |

---

## Global Invariants Verified

| Invariant | Result | Evidence |
|-----------|--------|----------|
| Frontmatter intact | PASS | L1-20 read directly; title/status/convergence/tools/provenance_legend all present and unchanged. |
| 14-section + §11.5 structure | PASS | `grep -cE '^## '` = 15 (14 numbered + §11.5); `grep -cE '^### '` = 3 (§8.1/8.2/8.3). Headers L30→L388 in correct order; §12/13/14 not renumbered by the §11.5 insert. |
| Provenance legend followed | PASS | 26 `[V1]/[V2]/[V3]/[MERGE]` tags; all new content (§11.5 `[MERGE]`, §4 artifacts `[V3]`, §2 G0-1 `[MERGE]`, §7 `[MERGE]`, §5 `[V2+MERGE]`) tagged. |
| Docs-only — only target edited by QA | PASS | My 3 Edits hit only `merged-requirements.md` (mtime 02:37:34). No `src/`, no `.claude/`, no tests touched. |
| No stub text introduced | PASS | `grep -niE 'TODO\|FIXME\|placeholder\|lorem\|XXX'` → empty. Two `TBD` hits (L18 frontmatter "MCP names TBD", L300 "weave MCP (TBD)") are **pre-existing real unknowns** about weave's undocumented MCP tool names — NOT stub text, and not introduced in Phase 2 (predate the edit window). |
| Cross-references coherent | PASS (after fixes) | H5→§11 curated-defect list resolves (L79↔L323). H3 §11.5→§6/§8.2/§12/G0-2 all resolve. H1 triangle §3↔§8.2↔§14 now consistent. Dangling audit-finding-ID refs (`see M2` L167, `finding M5` L209) — **both FIXED** (rewritten to in-document anchors). Final scan for `finding M[0-9]/see M[0-9]/(M[0-9])` → empty. |

---

## Issues Found & Fixed

| # | Severity | Location | Issue | Fix Applied |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | §14 step 4, L393 | **H1 regression / re-contradiction.** Phase 2 reconciled §3↔§8.2 to the terminal-state rule but left §14's timeline step still reading "weave ... Blocked until inspect **S4 live+KEEP**" — the exact original contradiction (an inspect KILL would block weave, contradicting the fixed §8.2). A third instance of the contradiction H1 was meant to eliminate. | Rewrote L393 to "Blocked until inspect reaches a terminal state (KEEP-live OR KILL) per the §3 between-tool gate — weave depends on `sem-core`, not inspect, so an inspect KILL releases weave." |
| 2 | MINOR | §14 step 3, L392 | **H1 consistency (wording).** "inspect ... Blocked until sem **S4 live+KEEP**" was substantively correct (a sem KILL trips CP-1/halt rather than releasing inspect) but did not name the asymmetric case, leaving it inconsistent in form with the §3 terminal-state framing. | Rewrote L392 to make the sem-KILL→CP-1 asymmetry explicit while preserving meaning. |
| 3 | IMPORTANT | §4, L167 (and §5, L209-210) | **Dangling cross-reference / provenance leakage.** L167 "(see M2)" and L209-210 "referenced by finding M5 ... M5 cites it" point at audit finding-IDs (M2, M5) that exist only in the external reflect REPORT.md — they have **no anchor in merged-requirements.md**, so a reader of the deliverable cannot resolve them. Violates the "cross-references coherent" invariant. | L167: removed "(see M2)", replaced with in-doc description of the §5/§8.1 Auggie-token-isolation measurement. L209-210: rewrote "referenced by finding M5" → "the CP-1 checkpoint (§10) and the §12 risk register both rely on this definition" (in-document anchors). |

## Non-Blocking Observation (outside QA fix authority)

The `adversarial/*.md`, `use-cases/*.md`, and dir-level `return-contract.yaml` files under `.dev/releases/backlog/AtaraxyLabs/` show a uniform `birth=ctime=mtime=2026-06-04 02:37:13` — i.e. the whole non-target subtree was **re-materialized at 02:37:13**, ~21s before my own edit at 02:37:34. At session start these same files carried 00:24-00:28 mtimes. This is a uniform infrastructure/snapshot event (same nanosecond cluster), NOT a content-bearing edit by the Phase 2 worker (whose target-file edit window closed at the original 02:34 mtime), and NOT caused by my QA edits (which touched only `merged-requirements.md`). No pre-image exists to content-diff against (all untracked, no git baseline). Logged transparently per zero-trust honesty; not flagged as a fixable defect because (a) it is not attributable to Phase 2 content work, and (b) the docs-only constraint forbids me touching those files. **Recommendation:** if provenance of the AtaraxyLabs subtree matters downstream, snapshot/commit it to establish a baseline before further edits.

## Actions Taken

- Fixed Issue 1 (§14 L393 weave gate) via Edit — verified: L393 now reads terminal-state wording; H1 triangle §3/§8.2/§14 grep-consistent.
- Fixed Issue 2 (§14 L392 inspect gate) via Edit — verified: L392 names sem-KILL→CP-1 asymmetry.
- Fixed Issue 3a (§4 L167 dangling M2) via Edit — verified: no `see M2` remains.
- Fixed Issue 3b (§5 L209-210 dangling M5) via Edit — verified: final grep for dangling finding-IDs returns empty.
- Re-verified structure (15 `##`, 3 `###`), frontmatter (L1-20), 26 provenance tags, and docs-only scope after all edits.

## Recommendations

- **Green light to proceed** past the Phase 2 phase-gate. All 6 HIGH criteria met; all found defects fixed in-place.
- Before Phase 3 (if any), consider committing/snapshotting the AtaraxyLabs subtree to establish a provenance baseline (see Non-Blocking Observation).

---

## Confidence Gate

- **Confidence:** Verified: 6/6 HIGH + 6/6 global invariants | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep(via Bash): 9 | Glob: 0 | Bash(non-grep): 3
  - Tool calls (18 verification actions) ≥ checklist items (12) — engagement minimum satisfied.
  - No web research performed (all claims local/source-truth; no external URL/standard/API lookup required) → tavily/web fallback counters: 0.
- Every HIGH and every global invariant marked VERIFIED carries a cited file:line or grep output above. No item left UNCHECKED. No item UNVERIFIABLE.

## QA Complete
