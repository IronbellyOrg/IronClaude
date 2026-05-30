# Research: Gap-Fill Round 3 — Target-state contract + OQ prefix governance
**Topic type:** Bounded gap-fill (addresses round-2 F-02 IMPORTANT + F-01 MINOR)
**Status:** In Progress
**Date:** 2026-05-29
---

## 1. Target-State Contract for the Executor (resolves F-02 IMPORTANT)

### Problem statement

Research files `01-scanner-layer-architecture.md` and `05-gap-fill.md` cite specific line numbers (e.g., `_DESCRIPTOR_NOUNS` near L70, `_is_descriptive_context` near L500, `_is_discharge_intent_line` near L530) from a **710-line** scanner. The CURRENT task worktree at `/config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix/` is a **608-line** scanner (fresh from `origin/master`) that does NOT yet contain `_DESCRIPTOR_NOUNS`, `_is_descriptive_context`, or `_is_discharge_intent_line`. Those symbols live on the uncommitted Fix-1 + Fix-3 working tree in the sibling `BareReview` worktree.

### Evidence (captured 2026-05-29)

```
$ wc -l <BareReview>/src/superclaude/cli/roadmap/obligation_scanner.py
  710 .../BareReview/.../obligation_scanner.py
$ wc -l <RoadmapCLI-ObligationFix>/src/superclaude/cli/roadmap/obligation_scanner.py
  608 .../RoadmapCLI-ObligationFix/.../obligation_scanner.py

$ grep -c _is_descriptive_context <BareReview>/.../obligation_scanner.py
3
$ grep -c _is_descriptive_context <RoadmapCLI-ObligationFix>/.../obligation_scanner.py
0

$ git -C <BareReview>/ branch --show-current
brainstorm/t2-bare-reviewer-adjunct

$ git -C <BareReview>/ status -s src/superclaude/cli/roadmap/obligation_scanner.py tests/roadmap/
 M src/superclaude/cli/roadmap/obligation_scanner.py
 M tests/roadmap/test_obligation_scanner.py
 M tests/roadmap/test_obligation_scanner_meta_context.py

$ git -C <BareReview>/ log --oneline -5
a596ef5f docs(brainstorm): add Phase 1.5 handoff prompt
8a1bbc72 feat(skills): add sc-bare-review v1.0 — Phase 1 T2 Bare-Reviewer Adjunct
c7c140ad feat(brainstorm): T2 bare-reviewer adjunct — spec v1.3 + skill stub + tasklist + A/B test harness
9b5a7c96 adding make sync-dev
3c64db96 chore(tasks): graduate 5 completed RF tasks + converge sprint (#104)
```

**Conclusion:** Fix 1 (`_DESCRIPTOR_NOUNS` / `_is_descriptive_context`) and Fix 3 (`_is_discharge_intent_line`) live as **uncommitted working-tree changes** on branch `brainstorm/t2-bare-reviewer-adjunct` in the `BareReview` worktree. They have not landed on `origin/master`. The fresh `RoadmapCLI-ObligationFix` worktree has the pre-fix 608-line scanner.

### Contract (binding on the Phase-2 executor)

1. **Target baseline.** Layer 5 must be implemented on top of the **POST-Fix-1+Fix-3** scanner state (≥710 lines, with all three Layer 4 symbols present). It MUST NOT be implemented on the 608-line `origin/master` baseline currently checked out in this worktree.

2. **Concrete source branch.** Fix 1 + Fix 3 are uncommitted edits on branch `brainstorm/t2-bare-reviewer-adjunct` in worktree `/config/workspace/IronClaude/.claude/worktrees/BareReview/`. Until those edits are committed and merged (or rebased into the current task branch), the target state does not exist on any committed ref.

3. **Sequencing options for the executor (pick exactly one).**
   - **(a) Wait-and-rebase.** Wait for `brainstorm/t2-bare-reviewer-adjunct` to commit Fix 1 + Fix 3, merge to `master`, then rebase the Phase-2 task branch onto the new `master` BEFORE starting Layer 5 implementation.
   - **(b) Rebase-onto-feature.** Rebase the Phase-2 task branch directly onto `brainstorm/t2-bare-reviewer-adjunct` (after Fix 1 + Fix 3 are committed to that branch) BEFORE starting Phase 2 implementation. This option assumes coordination with the bare-reviewer branch owner.

4. **Line-number reference frame.** All line numbers cited in research files `01-scanner-layer-architecture.md` and `05-gap-fill.md` (e.g., insertion point at L545 between `_is_discharge_intent_line` and `_is_meta_context_line`; `_DESCRIPTOR_NOUNS` near L70) are relative to the **POST-Fix-1+Fix-3 711-line scanner** (currently observed at exactly 710 lines — within ±2 of "711-line" framing previously used). They are NOT valid against the 608-line `origin/master` scanner.

5. **Verification command (mandatory, BEFORE Phase 2 begins).** The executor MUST run:
   ```bash
   wc -l src/superclaude/cli/roadmap/obligation_scanner.py
   grep -c _is_descriptive_context src/superclaude/cli/roadmap/obligation_scanner.py
   ```
   The first command MUST report **≥710 lines** AND the second MUST return **≥1**. (Note: `grep -c` emits a count, not a match listing — this keeps the gate machine-checkable.) If either gate fails, STOP and execute the rebase per (3) above before resuming.

6. **Git-status snapshot at task-creation time** (for posterity, so future readers know what was uncommitted when this task was authored):
   ```
   <BareReview>/ status -s src/superclaude/cli/roadmap/obligation_scanner.py tests/roadmap/:
    M src/superclaude/cli/roadmap/obligation_scanner.py
    M tests/roadmap/test_obligation_scanner.py
    M tests/roadmap/test_obligation_scanner_meta_context.py
   ```

---

## 2. Open Questions Prefix Governance (resolves F-01 MINOR)

### Problem statement

The user's spawn prompt explicitly names **4 demote-target subsections**: Risk Assessment Matrix (RAM), Integration Points (IP), Milestone Dependencies (MD), and Open Questions (OQ). Prior task §234 (and the gap-fill analysis in research 03 §5) only enumerated **3** of these (RAM, IP, MD). Reconciliation requires confirming whether any existing FP attributes to "Open Questions" — and if not, documenting OQ inclusion as a forward-looking, user-authorized scope expansion rather than a defect-driven addition.

### Existing 8-FP evidence base (from research 03 §4 + §5)

Re-cited verbatim from `03-fp-evidence.md`:

| Line | H3 Subsection (nearest above) | H2 milestone | Scaffold-term hits |
|---|---|---|---|
| 145 | `Integration Points — M2` | M2 | 1 (stub) |
| 149 | `Milestone Dependencies — M2` | M2 | 1 (stub) |
| 278 | `Integration Points — M5` | M5 | 1 (stub) |
| 425 | `Integration Points — M8a` | M8a | 2 (Stub, stub) |
| 437 | `Risk Assessment and Mitigation — M8a` | M8a | 2 (Stub, stub) |
| 474 | `Risk Assessment and Mitigation — M8b` | M8b | 1 (Stub) |

**Confirmed:** All 8 FPs distribute across exactly **3** H3 prefixes — `Integration Points` (×4 FPs on lines 145, 278, 425×2), `Milestone Dependencies` (×1 FP on line 149), and `Risk Assessment and Mitigation` (×3 FPs on lines 437×2, 474). **NONE of the 8 FPs is attributed to an `Open Questions —` H3.**

### Does the roadmap actually contain Open Questions H3s?

Yes. Per `03-fp-evidence.md` §2 H3 inventory, the following milestones expose `Open Questions — M{n}` H3 subsections:
- L104: `Open Questions — M1`
- L151: `Open Questions — M2`
- L200: `Open Questions — M3`
- L389: `Open Questions — M7`

So the prefix is **structurally present** in the roadmap surface, but no scaffold-term mention currently falls under any of these H3s. Layer 5 protection of Open Questions is therefore **prospective**.

### User's spawn prompt (verbatim, 4-subsection list)

The user-authored prompt that drove this task explicitly enumerates four demote-target subsections — Risk Assessment Matrix, Integration Points, Milestone Dependencies, and Open Questions. The inclusion of "Open Questions" is a deliberate, user-authorized scope expansion beyond the 3 subsections actually exercised by the current 8-FP corpus.

### Governance ruling

1. **Open Questions is a user-authorized PROSPECTIVE inclusion.** The 4th demote-target prefix exists in the matcher set defensively — future roadmap content may legitimately emit scaffold-term mentions under `Open Questions — M{n}` (e.g., open architectural questions about stub semantics, per research 03 §7). Including OQ now avoids a future patch when such content appears.

2. **It is NOT defect-driven.** No existing FP in the current 8-FP corpus sits under Open Questions. The executor MUST NOT search the current roadmap for an OQ-attributed FP to "verify" the OQ branch of Layer 5 — that search will return empty.

3. **Mandatory labeling in BUILD_REQUEST + generated task file.** The Prerequisites section of the generated MDTM task file MUST state explicitly:
   > "Open Questions" is included in the demote-target prefix set PROSPECTIVELY (user-authorized scope expansion). It has no current FP evidence in the 8-FP corpus. The other three prefixes (Integration Points, Milestone Dependencies, Risk Assessment) cover all 8 known FPs. Do not look for an OQ-attributed FP in the current `04-orchestration-roadmap.md` — none exists.

4. **Mandatory test coverage.** Test 3 in the round-2 gap-fill §5 plan is parameterized across the demote-target subsections. Per this governance ruling, the parameterization MUST include an **Open Questions fixture** (a synthetic minimal roadmap snippet with an `### Open Questions — M1` H3 containing a scaffold-term mention) so the prospective coverage is verified by a unit test. Without an OQ fixture, the OQ branch of Layer 5 ships untested and could silently regress.

---

**Status:** Complete
