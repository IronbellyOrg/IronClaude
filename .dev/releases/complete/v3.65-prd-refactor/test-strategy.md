---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 2
work_milestones: 4
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: prd-refactor-spec.md
generated: "2026-04-03T05:58:41.396794+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — PRD Skill Refactoring

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

With MEDIUM complexity and a 1:2 interleave ratio, 2 validation milestones cover 4 work phases:

| Validation Milestone | Covers Phases | Trigger Point | Focus |
|---|---|---|---|
| **VM-1: Extraction Fidelity Gate** | Phase 1 (Preparation) + Phase 2 (Content Extraction) | After Phase 2 exit criteria met | Content integrity — every extracted block matches original word-for-word; all 4 refs/ files exist with correct content |
| **VM-2: Restructure + Final Verification Gate** | Phase 3 (SKILL.md Restructuring) + Phase 4 (Verification, Sync, Commit) | After Phase 4 exit criteria met | Structural correctness — SKILL.md within line/token budget, zero stale refs, loading declarations correct, E2E behavioral regression passes |

**Rationale**: Phase 1 is pure prerequisite checking (low risk, no code changes) — bundling it with Phase 2 under VM-1 is safe. Phase 3 modifies SKILL.md and Phase 4 validates the entire system — VM-2 gates the final deliverable.

---

## 2. Test Categories

### 2.1 Unit Tests (Automated, per-file)

| Test ID | What | Method | Phase |
|---|---|---|---|
| UT-01 | Each refs/ file exists at expected path | `test -f .claude/skills/prd/refs/<file>` | VM-1 |
| UT-02 | Each refs/ file has a purpose header (first 5 lines contain `#` heading) | `head -5 refs/<file> \| grep -c '^#'` | VM-1 |
| UT-03 | SKILL.md line count 430–500 | `wc -l SKILL.md` | VM-2 |
| UT-04 | refs/ directory contains exactly 4 files | `ls refs/ \| wc -l` | VM-1 |
| UT-05 | Combined line count 1,370–1,400 | `wc -l SKILL.md refs/*` sum | VM-2 |
| UT-06 | Token estimate ≤ 2,000 (SKILL.md lines × 4.5) | Arithmetic check | VM-2 |

### 2.2 Integration Tests (Diff-based fidelity)

| Test ID | What | Method | Phase |
|---|---|---|---|
| IT-01 | 8 agent prompt templates: zero content diff | `diff` each template block against original lines 553–967 | VM-1 |
| IT-02 | Synthesis mapping: zero content diff | `diff` against original lines 969–1106 | VM-1 |
| IT-03 | Validation checklists: zero content diff | `diff` against original lines 1108–1254 | VM-1 |
| IT-04 | BUILD_REQUEST: exactly 6 SKILL CONTEXT FILE path changes, zero other changes | `diff` against original lines 344–508; count changed lines | VM-1 |
| IT-05 | Zero stale section references in SKILL.md | `grep -cE '".*section"' SKILL.md` returns 0 | VM-2 |
| IT-06 | Loading declarations at A.7 reference all 4 refs/ files | `grep 'refs/' SKILL.md` matches expected patterns | VM-2 |
| IT-07 | Cross-references in BUILD_REQUEST resolve | `grep 'refs/agent-prompts.md' refs/build-request-template.md` | VM-1 |
| IT-08 | Max concurrent refs ≤ 2 in loading declarations | Manual inspection of A.7 block | VM-2 |
| IT-09 | B05/B30 merge: B05 intact + B30's 6 QA paths appended | `diff` B05 section; count QA path rows | VM-2 |
| IT-10 | `make verify-sync` passes | `make verify-sync` exit code 0 | VM-2 |

### 2.3 End-to-End Tests (Behavioral regression)

| Test ID | What | Method | Phase |
|---|---|---|---|
| E2E-01 | PRD skill invocation completes Stage A | Invoke skill on test product; verify task file created | VM-2 |
| E2E-02 | Task file contains all 8 baked-in agent prompts | `grep` for unique strings from each prompt template in task file | VM-2 |
| E2E-03 | Stage B completes with PRD at expected output location | Invoke `/task` on generated task file; verify output | VM-2 |
| E2E-04 | Output structure matches pre-refactoring baseline | Compare section headings of generated PRD against baseline | VM-2 |

### 2.4 Acceptance Tests (Success criteria sweep)

All 12 success criteria from the extraction document, validated as a batch in VM-2:

| SC# | Criterion | Maps to Test |
|---|---|---|
| 1 | SKILL.md 430–500 lines | UT-03 |
| 2 | 4 refs/ files | UT-04 |
| 3 | Combined 1,370–1,400 lines | UT-05 |
| 4 | Agent prompt fidelity | IT-01 |
| 5 | Checklist fidelity | IT-03 |
| 6 | BUILD_REQUEST fidelity | IT-04 |
| 7 | Zero stale refs | IT-05 |
| 8 | Loading declarations at A.7 | IT-06 |
| 9 | Cross-refs in BUILD_REQUEST | IT-07 |
| 10 | Token budget | UT-06 |
| 11 | Max concurrent refs | IT-08 |
| 12 | Behavioral regression | E2E-01 through E2E-04 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**1:2 (MEDIUM complexity)**: This refactoring is mechanical but precision-critical. Content loss (Risk #1, HIGH severity) and cross-reference breakage (Risk #2, HIGH severity) are best caught immediately after extraction, not deferred to the end. However, Phase 1 (prerequisite checks) carries negligible risk and doesn't warrant its own validation milestone.

### Interleaving Timeline

```
Phase 1: Preparation          ─── low risk, no code changes
Phase 2: Content Extraction    ─── HIGH risk (content loss)
  ├── VM-1 GATE ──────────────── Stop here. Run UT-01..04, IT-01..04, IT-07
  │                               CRITICAL/MAJOR issues → stop-and-fix
Phase 3: SKILL.md Restructure ─── MEDIUM risk (stale refs, line count)
Phase 4: Verify + Commit       ─── verification-heavy
  └── VM-2 GATE ──────────────── Full sweep. Run UT-03..06, IT-05..10, E2E-01..04, all SC
                                  CRITICAL/MAJOR issues → stop-and-fix before commit
```

### Parallel Test Execution Within Gates

**VM-1** (after Phase 2):
- Wave 1 (parallel): UT-01, UT-02, UT-04 — file existence and structure checks
- Wave 2 (parallel): IT-01, IT-02, IT-03, IT-04, IT-07 — all diff-based fidelity checks
- Gate decision: All pass → proceed to Phase 3. Any CRITICAL/MAJOR → stop-and-fix.

**VM-2** (after Phase 4):
- Wave 1 (parallel): UT-03, UT-05, UT-06, IT-05, IT-06, IT-08, IT-09, IT-10 — structural checks
- Wave 2 (sequential): E2E-01 → E2E-02 → E2E-03 → E2E-04 — behavioral regression (sequential dependency)
- Gate decision: All 12 SC pass → commit. Any CRITICAL/MAJOR → stop-and-fix before commit.

---

## 4. Risk-Based Test Prioritization

Tests ordered by the risk they mitigate, highest severity and probability first:

| Priority | Risk | Tests | Rationale |
|---|---|---|---|
| **P0** | #1 Content loss (HIGH/Low) | IT-01, IT-02, IT-03, IT-04 | Word-for-word fidelity is the central constraint; failure here invalidates the entire refactoring |
| **P0** | #2 Cross-reference breakage (HIGH/Med) | IT-05, IT-07, IT-06 | Most likely defect class — prose references silently surviving as stale strings |
| **P1** | #4 Builder path resolution (MED/Low) | E2E-01, E2E-02 | Runtime failure invisible until actual invocation; only E2E catches it |
| **P1** | #3 Loading order wrong (MED/Low) | IT-06, IT-08 | Wrong-phase loading causes silent context bloat or missing prompts |
| **P2** | #7 Spec freshness (MED/Low) | UT-05 (combined line count) | Stale fidelity index produces line count mismatch — canary signal |
| **P2** | #5 B05/B30 merge (LOW/Low) | IT-09 | Low severity, well-documented merge strategy |
| **P3** | #6 Missing refs/ file (MED/Low) | UT-01, UT-04 | Self-diagnosing at runtime; test is cheap insurance |

**Execution order within VM-1**: P0 tests first. If IT-01 through IT-04 fail, do not proceed — content loss must be fixed before structural checks matter.

---

## 5. Acceptance Criteria Per Milestone

### VM-1: Extraction Fidelity Gate

| # | Criterion | Pass Condition | Severity if Failed |
|---|---|---|---|
| VM1-1 | 4 refs/ files exist | `ls refs/ \| wc -l` = 4 | CRITICAL |
| VM1-2 | Each file has purpose header | First line is markdown heading | MAJOR |
| VM1-3 | Agent prompts: zero content diff (8 templates) | `diff` returns empty for all 8 | CRITICAL |
| VM1-4 | Synthesis mapping: zero content diff | `diff` returns empty | CRITICAL |
| VM1-5 | Validation checklists: zero content diff | `diff` returns empty | CRITICAL |
| VM1-6 | BUILD_REQUEST: exactly 6 path changes | `diff` shows exactly 6 changed lines, all SKILL CONTEXT FILE updates | CRITICAL |
| VM1-7 | BUILD_REQUEST cross-refs resolve | `grep` finds `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` | MAJOR |
| VM1-8 | refs/ combined line count ~870 (±30) | `wc -l refs/*` between 840–900 | MINOR |

**Gate rule**: Zero CRITICAL failures. Zero MAJOR failures. If any CRITICAL or MAJOR → stop-and-fix before Phase 3.

### VM-2: Restructure + Final Verification Gate

| # | Criterion | Pass Condition | Severity if Failed |
|---|---|---|---|
| VM2-1 | SKILL.md 430–500 lines | `wc -l` in range | CRITICAL |
| VM2-2 | Combined line count 1,370–1,400 | Sum of all 5 files | MAJOR |
| VM2-3 | Zero stale section references | `grep` returns 0 matches | CRITICAL |
| VM2-4 | Loading declarations at A.7 | `grep 'refs/'` matches 4 file paths in A.7 section | CRITICAL |
| VM2-5 | Max 2 concurrent refs in orchestrator | Manual check of A.7 loading block | MAJOR |
| VM2-6 | Token estimate ≤ 2,000 | lines × 4.5 ≤ 2,000 (soft; accept ≤ 2,160) | MINOR |
| VM2-7 | B05/B30 merge correct | B05 intact + 6 QA paths appended | MAJOR |
| VM2-8 | `make verify-sync` passes | Exit code 0 | CRITICAL |
| VM2-9 | E2E: Stage A completes, task file created | Invocation succeeds | CRITICAL |
| VM2-10 | E2E: Task file contains all 8 prompts | `grep` for unique prompt strings | CRITICAL |
| VM2-11 | E2E: Stage B produces PRD at expected location | File exists at output path | CRITICAL |
| VM2-12 | E2E: Output structure matches baseline | Section heading comparison | MAJOR |

**Gate rule**: Zero CRITICAL failures. Zero MAJOR failures. All 12 success criteria from extraction document pass. Only then → atomic commit.

---

## 6. Quality Gates Between Phases

### Gate G0: Phase 1 → Phase 2 (Preparation → Extraction)

**Type**: Lightweight checklist (no formal validation milestone)

| Check | Method | Blocking? |
|---|---|---|
| Fidelity index exists and covers B01–B30 | File read + block count | Yes |
| No line gaps or overlaps in fidelity index | Range arithmetic check | Yes |
| SKILL.md baseline SHA recorded | `git hash-object` output captured | Yes |
| Feature branch created | `git branch --show-current` | Yes |
| `refs/` directory created | `test -d refs/` | Yes |
| Reference implementation accessible | `ls .claude/skills/sc-adversarial-protocol/refs/` | Yes |

**Policy**: All checks must pass. Any failure is CRITICAL — do not begin extraction against an unverified baseline.

### Gate G1 (= VM-1): Phase 2 → Phase 3 (Extraction → Restructuring)

**Full validation milestone.** All VM-1 acceptance criteria above.

**Policy**: stop-and-fix for CRITICAL and MAJOR. This is the most important gate — content fidelity established here is the foundation for all subsequent phases.

**Risk burn-down checkpoint**: After G1, Risks #1 (content loss), #5 (B05/B30 merge), and #6 (missing refs/) should be retired. If any related test fails, the risk is NOT retired and must be re-addressed.

### Gate G2: Phase 3 → Phase 4 (Restructuring → Verification)

**Type**: Quick structural check (not a full validation milestone, but prevents wasted E2E effort)

| Check | Method | Blocking? |
|---|---|---|
| SKILL.md line count 430–500 | `wc -l` | Yes |
| No extracted content remains in SKILL.md | `grep` for unique strings from each moved block | Yes |
| Loading declarations present at A.7 | `grep 'refs/' SKILL.md` | Yes |
| Zero stale section references | `grep` for prose section names | Yes |

**Policy**: If SKILL.md is over 500 lines or still contains extracted content, fix before running the expensive E2E tests in Phase 4.

**Risk burn-down checkpoint**: After G2, Risks #2 (cross-reference breakage) and #3 (loading order) should be retired.

### Gate G3 (= VM-2): Phase 4 → Commit

**Full validation milestone.** All VM-2 acceptance criteria above, including E2E behavioral regression.

**Policy**: stop-and-fix for CRITICAL and MAJOR. Commit only after all 12 success criteria pass. All evidence artifacts (fidelity index update, diff logs, grep outputs, E2E transcript) must be produced.

**Risk burn-down checkpoint**: After G3, Risks #4 (builder path resolution) and #7 (spec freshness) should be retired. All 7 risks retired = green light to commit.

---

## Appendix: Test Execution Scripts

Key verification commands for implementer reference:

```bash
# VM-1 quick sweep (run after Phase 2)
ls .claude/skills/prd/refs/ | wc -l                          # expect: 4
wc -l .claude/skills/prd/refs/*                               # expect: ~870 total

# VM-2 structural sweep (run after Phase 3)
wc -l .claude/skills/prd/SKILL.md                             # expect: 430-500
wc -l .claude/skills/prd/SKILL.md .claude/skills/prd/refs/*   # expect: 1370-1400
grep -cE '".*section"' .claude/skills/prd/SKILL.md            # expect: 0
grep 'refs/' .claude/skills/prd/SKILL.md                      # expect: 4 refs/ paths at A.7

# VM-2 cross-reference check
grep 'refs/agent-prompts.md' .claude/skills/prd/refs/build-request-template.md    # expect: match
grep 'refs/synthesis-mapping.md' .claude/skills/prd/refs/build-request-template.md # expect: match
grep 'refs/validation-checklists.md' .claude/skills/prd/refs/build-request-template.md # expect: match

# VM-2 sync verification
make verify-sync                                              # expect: exit 0
```
