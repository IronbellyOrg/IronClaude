# QA Report — Final M3 Content Gate (Advisory + Lens-Scoping)

**Topic:** FX1 advisory no-spec correctness slot (never auto-gating) + FX2 CODE-scoped AX-2 sharpening
**Date:** 2026-07-03
**Phase:** task-qualitative (targeted M3 confirmation gate — FX1/FX2 content scoping)
**Fix cycle:** N/A
**fix_authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed FX1 can auto-gate and FX2 is mis-scoped; attempted to prove both.

---

## Overall Verdict: PASS

Both confirmations hold under adversarial scrutiny. FX1's correctness slot is advisory and never auto-gating across both surfaces; FX2 is a CODE-scoped AX-2 sharpening of item 5 with the 15-item count preserved and no AX-6.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FX1 slot advisory/non-gating in `reflect-reviewer.md` | PASS | Role §L30 + `## Correctness gaps` §L101-115 + `persona_lens` §L56 all mark it advisory/non-gating |
| 2 | FX1 slot advisory/non-gating in `deviation-taxonomy.md` | PASS | `## Correctness-gap` §L156-180 routes to distinct `correctness-gaps.yaml`, never `deviation-ledger.yaml` |
| 3 | Counter `correctness_gap_raised` has ZERO gating consumers | PASS | `grep -rn correctness_gap_raised src/superclaude/` → single hit (increment site, taxonomy L166); no reader anywhere |
| 4 | No generic `*-gaps.yaml` aggregator sweeps correctness-gaps into a gate | PASS | SKILL.md gates key to `grounding-gaps.yaml` by name (L832, L1119-1121); no glob |
| 5 | 4-class taxonomy intact (no 5th gating class) | PASS | Classes at taxonomy L26/40/56/73; §L156/158 "no 5th class"; SKILL.md L1007/L1103 "4 categories, not 5" |
| 6 | FX2 is CODE-scoped AX-2 sharpening of item 5 (not doc-only) | PASS | rf-qa-qualitative L670 "Code Compatibility" group, item 5 L674 appended cross-symbol invariant |
| 7 | FX2 directs reading actual sibling symbols ACROSS modules | PASS | L674 "in the module AND across the other modules that receive the same input" (`diagnose()`/`diagnosis.py` vs `load_evidence()`/`evidence.py`) |
| 8 | FX2 count preserved (15 items), no AX-6 | PASS | L660 "Checklist (15 items)"; vocabulary closed `{AX-1..AX-5, none}` L639; `grep AX-6` → 0 hits |
| 9 | FX2 produces AX-2 finding at severity ≥ IMPORTANT | PASS | L674 tail: "annotate any disagreement `axis: AX-2` (Contradictions) at severity ≥ IMPORTANT" |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

---

## FX1 — Advisory no-spec correctness slot NEVER auto-gates (CONFIRMED)

**Surface A — `src/superclaude/agents/reflect-reviewer.md`:**

- **Role note (L30):** the slot is explicitly "Advisory no-spec correctness slot (non-gating)"; states it "MUST NOT be classified as Regression, MUST NOT set `regression_present` or increment `verification_regressions_detected`, and MUST NOT force `needs_human_decision` / `status: partial`. The deviation taxonomy stays exactly four classes — this is a parallel advisory channel, not a 5th deviation class."
- **`## Correctness gaps` sub-section (L101-115):** "separate from the 4-class Deviations table … and NEVER feeds the Adherence counts"; L115 repeats it MUST NOT set `regression_present`, MUST NOT increment `verification_regressions_detected`, MUST NOT enter the unconditional Tier-2/Tier-3 escalation, MUST NOT force `status: partial`; "absent a spec anchor this channel never gates on its own."
- **`persona_lens` (L56):** free-form guidance, explicitly "not a closed enum"; `no-spec-correctness` merely directs the pass toward the advisory channel. It is a lens, not a gate input.

**Surface B — `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`:**

- **`## Correctness-gap` (L156-180):** "Adds **no 5th category** … the taxonomy stays exactly four classes (the 5th was rejected in §17.7 Kill List)." Advisory routing (L162): written to a parallel `<output>/correctness-gaps.yaml`, "NEVER to `deviation-ledger.yaml`. It is advisory only: it does NOT set `regression_present`, does NOT increment `verification_regressions_detected`, does NOT enter the unconditional Tier-2 escalation path, and does NOT force `status: partial` or `needs_human_decision`." Effect column (L166): only `correctness_gap_raised += 1` and a yaml row — "NO `status` / `needs_human_decision` change." Structural separateness (L180): "distinct artifact from both `deviation-ledger.yaml` and `grounding-gaps.yaml`; the three files never share rows."
- Escalation exists only via the second table row (L167): a disagreement that violates a *documented* invariant / spec criterion routes to the *existing* Regression class BY EVIDENCE — that is the spec-relative Regression path, NOT this advisory channel. The advisory channel itself never gates.

**Adversarial disproof attempts (all failed to break the claim):**

1. *"The counter secretly feeds a gate."* — `grep -rn correctness_gap_raised src/superclaude/` returns exactly ONE line: the increment site at taxonomy L166. Zero readers. A counter no one reads cannot gate.
2. *"A generic gaps aggregator sweeps `correctness-gaps.yaml` like it does `grounding-gaps.yaml`."* — The `needs_human_decision` field (SKILL.md L832) and the `status: partial` forcing (SKILL.md L1119-1121) are keyed to `grounding-gaps.yaml` **by name**, not by a `*-gaps.yaml` glob. `grep` for correctness-gap references outside the taxonomy file across the whole `sc-reflect-protocol/` tree returns **nothing** — SKILL.md, report-template.md, reviewer-spec.md do not reference the artifact at all. It is structurally isolated; isolation makes it strictly non-gating.
3. *"It's really a 5th class in disguise."* — Four classes are the only entries in the taxonomy (Authorized L26, Necessary L40, Drift L56, Regression L73); both the taxonomy (L156/158/180) and SKILL.md (L1007, L1103) state 4-not-5, and the correctness-gap dimension is a sibling finding-modifier that routes by evidence, mirroring the already-shipped Grounding-gaps and FR-RH1 patterns.

**FX1 verdict: PASS.** The slot is advisory across BOTH surfaces and cannot auto-gate — not directly, not via the counter, and not via any generic aggregator. The 4-class taxonomy is intact.

---

## FX2 — CODE-scoped AX-2 sharpening of item 5 (CONFIRMED)

Target: `src/superclaude/agents/rf-qa-qualitative.md`.

- **Placement is code-scoped, not document-only:** the sharpening is appended to **item 5 "Module context analysis"** (L674), which sits under the `##### Code Compatibility` group header (L670) alongside item 4 (Function signature verification) and item 6 (Downstream consumer analysis). It is not a new item and not a doc-group check.
- **Directs reading actual sibling source symbols across modules:** L674 adds "Cross-symbol input-shape invariant (annotate `axis: AX-2`): sibling functions that consume the SAME input parameter MUST agree on its accepted shape … Read the ACTUAL sibling functions that consume the shared input — **in the module AND across the other modules that receive the same input** — not just the one under review, and compare how each handles it." The worked example is the real F1/PR#209 cross-module case: `diagnose()` in `diagnosis.py` vs `load_evidence()` / `_evidence_sha256()` in `evidence.py`. Cross-module reading is explicit.
- **Produces an AX-2 finding at severity ≥ IMPORTANT:** L674 tail — "annotate any disagreement `axis: AX-2` (Contradictions) at severity ≥ IMPORTANT." This aligns with the AX-2 axis definition (L597-604) and Critical Rule #6 (contradictions are never MINOR).
- **Count preserved (15 items), no AX-6:** L660 "Checklist (15 items)"; items enumerate 1-15 with no duplication (the sharpening is appended text on item 5, not a new numbered item). The Axis vocabulary is the closed set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` (L639); `grep AX-6` across the file → 0 hits. No sixth axis was introduced.
- **Adaptation table consistency:** the item-5 row of the adaptation table (L705) was updated to carry the cross-symbol invariant note while retaining its doc-task column — consistent with the code-scoped sharpening, no scope leak.

**Adversarial disproof attempts (all failed):**

1. *"It's actually a document-only check."* — It lives in the Code Compatibility group and instructs reading actual source symbols across modules; the doc-task column is a mandatory-adaptation mirror, not the primary scope.
2. *"It bumped the count or added AX-6."* — Count is still 15 (L660); no AX-6 anywhere; vocabulary remains the closed 5-axis + `none` set.

**FX2 verdict: PASS.**

---

## Issues Found

None. (Adversarial stance applied; no CRITICAL/IMPORTANT/MINOR issues surfaced. The absence of findings here is backed by the explicit disproof attempts above, each grounded in a grep result or a cited line.)

---

## Self-Audit

**Independent verification performed (this is a source-grounded review, not a reliance pass):**

1. **How many factual claims verified against source:** 9 checks, each grounded in a Read or Grep of the actual source file — counter-consumer count, artifact isolation, class count, item count, axis vocabulary, placement, severity phrasing, cross-module directive.
2. **Files read/grepped:**
   - `src/superclaude/agents/reflect-reviewer.md` (full Read)
   - `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` (Read L140-181 + header grep)
   - `src/superclaude/agents/rf-qa-qualitative.md` (targeted grep of item 5, AX-2, AX-6, count)
   - `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (grep of gating symbols / gaps-artifact keying)
   - `grep -rn correctness_gap_raised src/superclaude/` (counter-consumer census → 1 hit, increment-only)
   - `grep` correctness-gap references across `sc-reflect-protocol/` excluding taxonomy → 0 hits (isolation proof)
3. **Why trust a PASS with 0 issues:** the PASS is not an absence of looking — each claim carries a specific line citation or a grep census, and the two most dangerous auto-gating vectors (a hidden counter consumer; a generic `*-gaps.yaml` aggregator) were explicitly hunted and disproven (single increment-only hit; name-keyed not glob-keyed gates). A false PASS here would require a gating consumer that grep did not surface — the census makes that highly unlikely.
4. **Web research:** none performed (fully local source-bound review); no Tavily/fallback engagement required.

**(a) Reliance list — inherited structural PASS items skipped:** None. No `## Inherited Structural Verdict` section was supplied in the spawn prompt; this review ran standalone against source.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Counter-consumer census — verified `correctness_gap_raised` has zero readers via `grep -rn` (increment site only, taxonomy L166).
- Aggregator-glob disproof — verified `needs_human_decision` / `status: partial` gates are name-keyed to `grounding-gaps.yaml` (SKILL.md L832, L1119-1121), not a `*-gaps.yaml` glob, via targeted grep.
- Class-count invariant — verified exactly four classes at taxonomy L26/40/56/73 + "no 5th" affirmations at L156/158/180 and SKILL.md L1007/L1103.

---

## Confidence

- **Verified:** 9/9 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
- **Tool engagement:** Read: 2 | Grep: 6 | Glob: 0 | Bash: 6 (grep/ls invocations)
- Tool calls (8 Read+Grep-equivalent, plus bash-hosted greps) ≥ checks confirmed; no padding — each grep/Read mapped to a specific confirmation above.

## Recommendations

- Proceed. FX1 and FX2 are content-correct and correctly scoped as specified for the M3 gate. No remediation required.

## QA Complete

---

_Grounding root: `/config/workspace/IronClaude/.dev/worktrees/pr209-harden` (worktree). All citations resolved against `src/superclaude/` source-of-truth files, not `.claude/` sync output._
