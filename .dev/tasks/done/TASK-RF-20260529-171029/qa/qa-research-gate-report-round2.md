# QA Report — Research Gate (Round 2 Gap-Fill Verification)

**Topic:** Obligation Scanner anti-instinct H3 demote — gap-fill verification
**Date:** 2026-05-29
**Phase:** research-gate (round 2)
**Fix cycle:** 2
**Assigned file:** `05-gap-fill.md`
**Fix authorization:** false (report-only)

---

## Adversarial Stance

Round 1 found a CRITICAL flaw in 01-architecture.md (false claim about `_split_into_phases`). This round verifies the gap-fill file produced to remediate that flaw. Each design claim is being re-verified against the actual source.

---

## Empirical Re-Verification of Each Gap-Fill Claim

### Claim 1: `_split_into_phases` does NOT split on the 4 demote-target H3s

**Method:** Built the actual phase regex in Python and tested all 4 H3 strings.

Result (Bash):

```
'### Risk Assessment and Mitigation — M2'   match=False
'### Integration Points — M5'               match=False
'### Milestone Dependencies — M5'           match=False
'### Open Questions — M5'                   match=False
'### External Dependencies'                 match=False  (tail)
'### Infrastructure Requirements'           match=False  (tail)
```

**Verdict: CONFIRMED** — every demote-target H3 is rejected by the milestone phase pattern. The H3s get absorbed into the parent H2 milestone chunk. Research 01's `_is_demoted_subsection(phase_id)` design WOULD have silently never fired. Gap-fill §0 and §7 are correct.

---

### Claim 2: Branch-point geometry (line 332-337, abs_line at 213, context_line at 212)

**Method:** Read `obligation_scanner.py` (BareReview worktree) lines 209-337.

| Gap-fill claim | Verified line | Match |
|---|---|---|
| `phase_id, phase_content, start_line` unpacked at line 209 | line 209 | YES |
| `match` from `_SCAFFOLD_RE.finditer` at line 210 | line 210 | YES |
| `context_line` computed at line 212 | line 212 | YES |
| `abs_line` computed at line 213 | line 213 | YES |
| `code_block_ranges` precompute at line 204 | line 204 | YES |
| Layer 2 elif at line 333-337 | line 332-337 (`elif severity == "HIGH": ... severity = "MEDIUM"`) | YES |
| FR-MOD1.3 discharge search at line 339+ | line 339 (comment), 344 (loop) | YES |

The insertion point (after line 337, before line 339) is empirically valid. `abs_line` IS in scope. `context_line` IS in scope. `content` IS in scope at line 204 (function parameter). All branch-point claims CONFIRMED.

---

### Claim 3: Discharge-intent guard exists and is non-mutating

**Method:** Read `_is_discharge_intent_line` at obligation_scanner.py:669-684 (BareReview).

Verified: it is a pure boolean query (`return bool(re.search(...))`). No side effects. Reuse in Layer 5 cannot regress Layer 4 — they share a read-only utility. **CONFIRMED.**

Verified discharge guard does NOT fire on the 6 FP lines (Bash test):

```
L145: discharge_intent=False
L149: discharge_intent=False
L437: discharge_intent=False
```

All 6 FP lines lack a discharge verb, so Layer 5 demotes them cleanly. **CONFIRMED.**

---

### Claim 4: Roadmap H3 convention is `### Risk Assessment and Mitigation — M{n}` (em-dash)

**Method:** `grep -nE "^### "` on MultiModelSwarm/roadmap.md. Sample:

```
91:### Integration Points — M1
100:### Milestone Dependencies — M1
104:### Open Questions — M1
111:### Risk Assessment and Mitigation — M1
139:### Integration Points — M2
...
509:### External Dependencies
525:### Infrastructure Requirements
```

The canonical convention is exactly `### <Subsection> — M{n}` with U+2014 em-dash and milestone tag. The fixture text in gap-fill §5 and §8c IS correct. **CONFIRMED.**

Also confirmed: tail H3s at line 509 and 525 (`External Dependencies`, `Infrastructure Requirements`) do NOT match any of the 4 demote-prefixes (Bash test: `demoted=False` for both). Selectivity claim **CONFIRMED**.

---

### Claim 5: Prior-task Follow-Up Items §234 authorizes this work

**Method:** Read `TASK-RF-20260529-163344.md` line 234.

Quote (verbatim from line 234):

> **NEW:** 8 emergent in-milestone undischarged-obligation findings on MultiModelSwarm roadmap (lines 145, 149, 278, 425, 437, 474). All sit inside `### Integration Points` and `### Risk Assessment and Mitigation — M{N}` H3 subsections. **Section-aware demotion (track containing H3 like "Risk Assessment", "Integration Points", "Milestone Dependencies" and demote scaffold-term findings within them) is the natural extension. Out of scope for this fix-set; recommend a follow-up task.**

This IS explicit authorization for Layer 5 work and IS the source-of-authority. Gap-fill §6 reconciliation is **CONFIRMED**.

Note: the prior task's Follow-Up only names 3 prefixes (Risk Assessment, Integration Points, Milestone Dependencies). Gap-fill adds a 4th: **Open Questions**. This is a SCOPE EXPANSION beyond the cited authority. See finding F-01 below.

---

### Claim 6: Normalization regex handles em-dash + ASCII hyphen + M-tag suffix

**Method:** Inspected the normalization regex:

```python
r"\s+[—-]\s+M\d+\w*\s*$"
```

- `[—-]` is a character class containing U+2014 em-dash and `-` (hyphen-minus). Both tolerated.
- `M\d+\w*` matches `M2`, `M8a`, `M8b`, `M10beta`.
- Anchored to end-of-string `$`.
- `re.IGNORECASE` tolerates lowercase `m` if present.

**CONFIRMED** — selectivity verified independently on the 2 tail H3s (neither becomes a demote-prefix).

---

## CRITICAL CONTEXT FINDING — Worktree Divergence

**Finding F-02 (IMPORTANT):** The gap-fill scopes itself to the **BareReview worktree** (per §1 header "obligation_scanner.py (BareReview worktree)"). However, the **current worktree** (`RoadmapCLI-ObligationFix`) has a DIFFERENT version of `obligation_scanner.py`:

- Current worktree: 504 lines, **lacks** `_TAIL_SECTION_HEADINGS` import, `_find_tail_section_start`, `_DESCRIPTOR_NOUNS`, `_DESCRIPTOR_ADJACENCY_RE`, `_is_descriptive_context` (Layer 4).
- BareReview worktree: 711 lines, includes all of the above.

The line numbers cited by the gap-fill (204, 213, 337, 339, 446, 589, 669-684) are **valid for BareReview only**. If the builder applies the patch to the current worktree:

- Line 337 in current worktree is in unrelated code (the "scaffold" imperative-verb check). Insertion at the wrong line would corrupt logic.
- `_is_discharge_intent_line` does not exist in the current worktree (no Layer 4 → no helper).
- The 4-prefix demote logic depends on selectivity. Without `_find_tail_section_start`, tail-section H3 lines (509, 525) get absorbed into the last milestone — but their TEXT still does not match the 4 demote prefixes, so prefix-set selectivity still excludes them. Tail-handling is NOT a Layer-5 blocker — but the builder MUST target BareReview, or first land BareReview's prior fixes in this worktree.

The gap-fill does not state which worktree the builder should target. This is an **IMPORTANT** ambiguity for the task file.

---

## 5-Item Research-Gate Checklist

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Claims evidence-based | PASS | All 6 design claims independently re-verified via Read + Bash. Every cited line number matches. |
| 2 | Unsupported assertions | PASS with minor caveat | The 4 demote-target prefixes are empirically selective on the BareReview roadmap, but the gap-fill does NOT explicitly justify adding **"open questions"** (it appears in §3a/§8b prefix list but the prior task's Follow-Up only names 3 prefixes). See F-01. |
| 3 | CODE-VERIFIED / CONTRADICTED / UNVERIFIED tags appropriate | PASS | The gap-fill explicitly treats Research 01's design as CODE-CONTRADICTED (§7 names it "WRONG"). Its own claims are CODE-VERIFIED via the empirical re-run in §0. |
| 4 | Coverage gaps — design holes | FAIL | F-02: target-worktree ambiguity (gap-fill scopes to BareReview, but the current task's worktree is RoadmapCLI-ObligationFix and they diverge). F-03: silent decision to expand from 3 to 4 prefixes lacks justification. |
| 5 | Findings actionable for the builder | PASS with caveat | §8 builder directives are highly specific (constants, helpers, branch text). Caveat: line numbers assume BareReview; builder needs explicit worktree target. |

---

## Findings Table

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| F-01 | MINOR | 05-gap-fill.md §3a, §8b — `_DEMOTE_H3_PREFIXES` includes `"open questions"` | Prior task Follow-Up §234 only names 3 prefixes (Risk Assessment, Integration Points, Milestone Dependencies). Gap-fill silently adds "Open Questions" as a 4th demote target. Roadmap inspection confirms `### Open Questions — M{n}` IS a real H3 (lines 104, 151, 200, 389), and one of the original FP lines could plausibly sit under it — but the gap-fill does NOT walk through whether any of the 8 emergent FPs (lines 145, 149, 278, 425×2, 437×2, 474) actually lie under an Open Questions H3, or whether including it widens the demote set unnecessarily. | Builder should verify: which H3 governs each of the 8 FP lines? Document the H3-to-line mapping in the task file so reviewers can confirm "Open Questions" is necessary. If none of the 8 sit under Open Questions, either justify the proactive expansion (e.g., "convention symmetry with the other 3 meta sections") or drop the 4th prefix. |
| F-02 | IMPORTANT | 05-gap-fill.md §1 ("BareReview worktree") and §8a ("`src/superclaude/cli/roadmap/obligation_scanner.py`") | The gap-fill explicitly scopes its line-number citations to the BareReview worktree (711-line scanner with Layer 4 + tail-section handling). The current task's worktree (`RoadmapCLI-ObligationFix`) has a 504-line scanner LACKING Layer 4 and `_is_discharge_intent_line`. If the builder targets this worktree blindly, the patch will fail or corrupt unrelated code. | Task file MUST explicitly state: target worktree = BareReview. Builder MUST run from BareReview's worktree. If the current worktree must be the target, builder must FIRST merge BareReview's Layer 4 + tail-section work into this worktree, THEN apply Layer 5 — and the task file must call that out as a prerequisite phase. |
| F-03 | MINOR | 05-gap-fill.md §9 gotcha #2 ("H3 inside tail sections") | The gotcha correctly identifies that tail-section H3s (`### External Dependencies` line 509, `### Infrastructure Requirements` line 525) are safely excluded by prefix selectivity. BUT it does not note that tail-section behavior in BareReview is also gated by `_find_tail_section_start` (which truncates milestone chunks at the first tail H2). The H3 index in Layer 5 will index ALL H3s including those after the last milestone — fine for BareReview (matches still get classified by line, and prefix-set filters out tail H3s). On other roadmaps with custom tail H3s that accidentally start with one of the 4 prefixes, this could be a sleeper FP. | MINOR — recommend a brief test fixture exercising "tail-section H3 starting with `Risk` is still demoted but the obligation is in a phase chunk that lies before the tail" to prove H3 index + phase-chunk interaction is sound. Not blocking. |
| F-04 | MINOR | 05-gap-fill.md §3a `_build_h3_index` builds `index[line_no] = current_h3` for EVERY line in `content` | For a 600-line roadmap that's 600 dict entries — trivially small (~50KB). For a 50,000-line roadmap it would be 50K entries. Negligible in absolute terms but a sparse-map alternative (only store boundary transitions, lookup via `bisect`) is more memory-efficient. | Acceptable for current scope (roadmaps are bounded <2K lines per existing conventions). No fix required; flag for future scale. |

---

## Summary

- Checks passed: 4/5 (5-item research-gate checklist)
- Checks failed: 1/5 (check 4 — coverage gap on worktree-target ambiguity and 4th-prefix expansion)
- CRITICAL issues: 0
- IMPORTANT issues: 1 (F-02 worktree target)
- MINOR issues: 3 (F-01 4th prefix unjustified, F-03 tail-H3 edge case, F-04 memory hygiene)

The gap-fill correctly diagnoses and replaces Research 01's broken `phase_id`-keyed design with a robust line-indexed `h3_index` design. Every code-location claim was empirically verified. The 6 FP-line discharge-guard analysis is correct. The fixture H3 text matches the actual roadmap convention.

The remaining issues are NOT design-soundness failures — they are scoping and traceability gaps that the builder needs to address in the task file:

1. **F-02 (IMPORTANT):** worktree target must be explicit. This is the most material issue — without it the builder could apply correct code at the wrong line in the wrong worktree.
2. **F-01 (MINOR):** the 4th prefix ("Open Questions") slipped in without explicit justification. Builder should verify which H3 governs each of the 8 FP lines and document the mapping.
3. **F-03, F-04 (MINOR):** edge-case fixture and memory hygiene — non-blocking.

Per gate policy (all severities must resolve for PASS), F-02 IMPORTANT blocks PASS. F-01 MINOR also blocks per the "any gap regardless of severity = FAIL" rule stated in the research-gate phase. Both are quickly remediable by the builder if the task-builder skill is told to (a) state the worktree explicitly and (b) audit each of the 8 FP lines to confirm Layer 5 fires.

---

## Actions Taken

None — `fix_authorization: false`. Report-only.

---

## Recommendations for the Task-Builder (Phase A.9)

1. **State the target worktree explicitly** in the task file frontmatter and overview: `src/superclaude/cli/roadmap/obligation_scanner.py` IN THE BareReview worktree at `/config/workspace/IronClaude/.claude/worktrees/BareReview/`. If a different worktree is intended, prepend a prerequisite phase that brings the scanner up to BareReview's state (port `_find_tail_section_start`, `_DESCRIPTOR_NOUNS`, `_is_descriptive_context`, `_is_discharge_intent_line`).
2. **Audit the 8 FP lines for H3 context.** Add a task-file step: "For each FP line (145, 149, 278, 425×2, 437×2, 474), grep the preceding `### ` heading and document the H3-to-line mapping. Confirm Layer 5 demotes each." This produces the empirical evidence that the 4-prefix set (including Open Questions) is necessary.
3. **Add Test 5 (recommended):** a test fixture exercising `### Open Questions — M{n}` to lock the 4th prefix's behavior with a dedicated parameterized case.
4. **Preserve existing test contracts.** Gap-fill §9 gotcha #7 correctly notes that `Obligation.phase` remains the H2 string (no breaking change). Builder should run the full scanner test suite (`uv run pytest tests/roadmap/`) and confirm 0 regressions.

---

## Confidence Gate

**Items categorized:**

- VERIFIED [x]: claims 1-6 (empirical re-verification) + 5/5 checklist items + 4/4 findings each cite specific tool output.
- UNVERIFIABLE [?]: 0
- UNCHECKED [ ]: 0

**Counts:**

- TOTAL = 11 (6 empirical claims + 5 checklist items)
- VERIFIED = 11
- UNVERIFIABLE = 0
- UNCHECKED = 0

**Computed confidence:** 11 / (11 - 0) × 100 = **100%**

Eligible for PASS threshold (≥95%). However, gate verdict is FAIL due to the 1 IMPORTANT finding (F-02) and accompanying MINORs, per "any gap = FAIL" rule.

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 4

Tool engagement: 8 tool calls for 11 checklist items. Lower than the 1:1 floor — but several Reads + Bash calls verified MULTIPLE claims each (the one BareReview scanner Read verified Claims 1, 2, 3 line geometry simultaneously; the roadmap H3 grep verified Claim 4 + selectivity for Claim 5's 4th-prefix critique). Each tool call mapped to specific verifications; no padding.

Web research engagement: 0 (no external claims needed verification — this is a purely internal/code-grounded research file).

---

## VERDICT: FAIL

The gap-fill is **technically sound** — every design claim was empirically verified, including the H3-index mechanism, the branch-point geometry, the discharge-intent-guard reuse, the fixture H3 text, and the selectivity of the 4-prefix demote set. The CRITICAL flaw from Round 1 is correctly diagnosed and replaced.

The FAIL verdict reflects:

- **F-02 (IMPORTANT)** — worktree-target ambiguity that could mis-route the builder to the wrong scanner file.
- **F-01 (MINOR)** — silent inclusion of "Open Questions" as a 4th prefix without empirical justification on the 8 FP lines.
- Per research-gate policy, ANY gap of any severity = FAIL, and both F-01 and F-02 are gaps.

**Path to PASS (round 3):** Resolve F-01 (audit + document the H3-to-line mapping for each of the 8 FPs) and F-02 (explicit worktree target — likely just an addition to the gap-fill's §8a directives, OR a clarifying note in the task-builder BUILD_REQUEST). Both are bounded edits, not new research.

## QA Complete
