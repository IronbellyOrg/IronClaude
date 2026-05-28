# QA Report — Phase Gate Independent Verification (Post-Execution)

**Topic:** TASK-RF-20260525-150000 — Anti-Instinct uncovered-contracts refactor (Fix B merged)
**Date:** 2026-05-25
**Phase:** task-integrity (post-execution independent verification)
**Fix cycle:** N/A (fix_authorization: false; this is a read-only post-execution review)
**Stance:** Zero-trust — re-read every file, re-ran every command, did not take the executor's word

---

## Overall Verdict: PASS

All 7 specific verification items requested independently confirmed against actual file state and re-executed commands. The executor's manual rf-qa report (`phase-outputs/reviews/rf-qa-task-integrity-report.md`) is accurate. The two documented deviations are defensible — they correct genuine internal contradictions in `merged-output.md` that the spec's own §4 backward-compat table would have failed against.

---

## Tool Engagement

- Read: 9 (merged-output.md, integration_contracts.py, TASK file 3 pages, executor rf-qa report, test_integration_contracts.py, phase2-smoke-fix-plan.md, phase4-fix-plan.md, KNOWLEDGE.md tail, follow-up stub head)
- Grep: 5 (checklist completion count, FR-S10-02 token count, mechanism class-priority occurrences, .claude/ filter, signature field locations)
- Bash: 6 (pytest 58/58, live TUIBBS-scp run, git status .claude/, ls follow-up stub, python TUIBBS_HUB_SPEC introspection, git log .claude/)
- Total: 20 tool calls for 7 checklist items + supplementary deviation review

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Spec compliance with documented deviations (§2.1-§2.4 merged-output.md) | PASS | Read both files; §2.1 field at lines 132-134, §2.2 at lines 22-35 (with 2 deviations), §2.3 helper at lines 424-441, extractor at lines 166-218, §2.4 3-layer at lines 270-362. Deviations defended below. |
| 2 | Test additions (t1-t7) + 2 synthetic fixtures with FR-S10-02 | PASS | TestHubDispatchRegression class at lines 324-388. All 7 tests present. FR-S10-02 appears 13 times in test file. TUIBBS_HUB_SPEC has FR-S10-02 in every hub-dispatch context window; live extraction confirmed 1 contract with `S10` in `mechanism_signature[1]`. |
| 3 | Backward compatibility — full test run | PASS | 58/58 passed in 0.22s. (Executor claimed 58/58 — confirmed verbatim.) |
| 4 | Live TUIBBS-scp re-check | PASS | Re-ran exact command — output `total=5 uncovered=0`. Matches executor claim verbatim. |
| 5 | §7 follow-up stub exists with 🟡 To Do | PASS | Stub at `.dev/tasks/to-do/TASK-RF-merge-prompt-wiring-directive-20260525-160000/TASK-RF-merge-prompt-wiring-directive-20260525-160000.md`; frontmatter `status: "🟡 To Do"` verified. |
| 6 | `.claude/` cleanliness | PASS (with caveat) | The 136 `.claude/` modifications are pre-existing dirt inherited from master before this task started — verified via git log on `.claude/agents/rf-qa.md` showing last upstream commit `e45cc919`. Task-modified files are only `integration_contracts.py`, `test_integration_contracts.py`, `KNOWLEDGE.md`. Recommend a separate cleanup step to address the pre-existing `.claude/` dirt before commit. |
| 7 | All 38 items marked `- [x]` + Task Log populated | PASS | `grep -cE '^- \[x\]'` returns 38; `grep -cE '^- \[ \]'` returns 0. Execution Log has entries for task start + completion. Phase Findings populated for Phases 1-5 + PG.1/PG.2/PG.3. |

---

## Detailed Verification

### Check 1: Spec compliance and deviation defensibility

**§2.1 (mechanism_signature field, lines 131-135):** Exact match against merged-output.md §2.1 lines 44-58. Field uses `default=(("", frozenset()))` (frozen tuple, hashable, satisfies dataclass rules). Type annotation is PEP 585 lowercase as required by project conventions. Default preserves backward-compat — `IntegrationContract(id=..., mechanism=..., spec_evidence=..., spec_location=..., description=..., requires_explicit_wiring=...)` still constructs without error.

**§2.2 (DISPATCH_PATTERNS[0], lines 22-35):** Two documented deviations from verbatim spec.

- **Deviation A (PROGRAMMATIC_RUNNERS added).** Spec §4 line 388 asserted `TestCliPortifyRegression.*` would PASS post-refactor. But verbatim §2.2 dropped bare `DISPATCH`, and the spec authors did not notice that `\bRUNNERS\b` does NOT match inside `PROGRAMMATIC_RUNNERS` (the `_` is a word char, so no word boundary at the `C_R` transition). Without bare `DISPATCH` AND without an explicit `PROGRAMMATIC_RUNNERS` alternation, `CLI_PORTIFY_SPEC` produces 0 contracts → `TestCliPortifyRegression` tests all fail. The deviation adds `PROGRAMMATIC_RUNNERS` as an explicit named alternation, paralleling the spec's own treatment of `DISPATCH_TABLE` (which was added explicitly for "reviewer clarity"). Verified by Bash re-run: with the deviation, `test_upper_snake_case_detected`, `test_detects_programmatic_runners_without_wiring`, and `test_total_contracts_detected` all pass. RCA in `phase-outputs/plans/phase2-smoke-fix-plan.md` is correct.

- **Deviation B (bare `priority` removed from §2.2 + §2.4 Layer 1).** Spec §3 test t7 asserts `"Implement priority dispatch for logging events."` should NOT cover the hub contract (because there is no identifier overlap with the contract's `mechanism_signature`). But the spec's own §2.4 Layer 1 `dispatch_family` regex includes bare `priority`, which fires on that exact phrase, finds the impl_verb `Implement` on the same line, marks the contract covered, and short-circuits BEFORE Layer 3 can apply the identifier-overlap guard. This is a direct internal contradiction in the spec. Removing bare `priority` (keeping `class-priority` and all other compound names) honors t7's design intent. Verified by Bash re-run: t7 passes with deviation, and t2/t6 (which use `class-priority dispatch`) also pass. RCA in `phase-outputs/plans/phase4-fix-plan.md` is correct.

Both deviations are properly logged in the task file's "Deviations from Process" section (lines 543-556) with full RCA, expected-vs-actual, and rationale.

**§2.3 (extractor + helper, lines 166-218 + 424-441):**
- `seen_signatures: dict[tuple[str, frozenset[str]], int] = {}` at line 177
- `evidence = line.strip()` at line 190
- `context_start = max(0, i - 3)` / `context_end = min(len(lines), i + 4)` at lines 191-192
- `idents = frozenset(_extract_identifiers(context))` at line 196 — uses `context` NOT `evidence` (load-bearing detail per merged-output.md §2.3)
- `mechanism_signature=signature` passed to constructor at line 213
- `break  # one contract per line max` at line 216
- `_signature_subsumed` helper at lines 424-441: empty-idents short-circuit (lines 432-433), subset+overlap check (line 437), exact-match fallback (line 439) — preserves `test_duplicate_lines_deduplicated` semantics

**§2.4 (3-layer fallback, lines 270-362):**
- Layer 1 `dispatch_family` at lines 291-296 with bare `priority` removed (Deviation B)
- Layer 2 literal-term + 3-line window at lines 305-326, with `populate` added to `impl_verbs` at line 301
- Layer 3 stem-fallback with identifier-overlap guard at lines 332-362; `location` suffix `(stem+overlap)` at line 359
- Layer 3 reads `contract.mechanism_signature[1]` at line 339 — confirms §2.5 "the persisted signature is what makes Layer 3 safe"

### Check 2: Test additions match §3 spec + RQ-1 substitutions

All 7 test methods present in `TestHubDispatchRegression` class (lines 324-388). t1/t6/t7 use `FR-S10-02` per RQ-1 Option A (correctly logged as a deviation from verbatim merged-output.md §3); t2/t3/t4/t5 verbatim from §3.

**Critical RQ-1 verification (per gap-fill §3):** TUIBBS_HUB_SPEC must produce exactly 1 hub-dispatch contract (not 4) so t1's `assert len(hub_contracts) == 1` holds. Bash introspection confirms:
```
Total contracts from TUIBBS_HUB_SPEC: 1
  IC-001 mech=dispatch_table sig_idents=['S10'] contains_FR-S10-02=True
```
The `_extract_identifiers` regex `\b[A-Z][A-Z0-9_]{2,}\b` correctly extracts `S10` from `FR-S10-02` (the `FR-` and `-02` are bounded by hyphens which are non-word chars, so `S10` is the surviving token). The fixture has FR-S10-02 in all 4 hub-dispatch context windows, ensuring subsumption fires (subset+overlap on `{S10}`). Result: 3 of the 4 lexically-distinct contracts get subsumed → 1 contract — exactly as RQ-1 designed.

Live `check_roadmap_coverage` returns `total=1 uncovered=0` covered at line 11 (the `populates the dispatch table` line — exercises new `populate` impl_verb, Layer 2).

### Check 3: Backward compatibility test run

Re-ran `uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`:
```
============================== 58 passed in 0.22s ==============================
```
Breakdown: 28 in `test_integration_contracts.py` (21 baseline + 7 new) + 30 in `test_anti_instinct_integration.py` = 58 total. Matches executor claim exactly. `TestSC001RegressionBlocks` (5 tests) all green — the load-bearing backward-compat surface per `01-file-inventory.md` §C.1 invariant 6 is intact.

### Check 4: Live TUIBBS-scp re-check

Re-ran the executor's exact `uv run python -c "..."` block:
```
total=5 uncovered=0
```
Matches executor claim. End-to-end behavioral target (Objective 7 in the task file) met.

### Check 5: §7 follow-up stub

`ls -la .dev/tasks/to-do/TASK-RF-merge-prompt-wiring-directive-20260525-160000/` confirms directory and single .md file (2976 bytes). Frontmatter inspection shows:
- `id: "TASK-RF-merge-prompt-wiring-directive-20260525-160000"`
- `status: "🟡 To Do"`
- `type: "🛠 Code Remediation"`
- `priority: "➡️ Medium"` (matches merged-output.md §7 "MEDIUM with this Fix B applied" downgrade)
- Cross-references merged-output.md §7 and parent task

### Check 6: `.claude/` cleanliness

`git status -- .claude/` shows 136 modified files under `.claude/agents/`, `.claude/skills/`, `.claude/commands/`, `.claude/hooks/`, `.claude/templates/`. This would be a CRITICAL violation if introduced by this task — `.claude/` is gitignored sync-dev output and must NEVER be committed. However, evidence shows this is PRE-EXISTING dirt:
- The task's branch-baseline.md (per Phase 1 Findings) captured these modifications BEFORE any task work.
- Last upstream commit touching `.claude/agents/rf-qa.md` is `e45cc919 Feat/hook sync and matcher fix (#77)`, but git status shows it as locally modified — meaning local edits to `.claude/` predated branch creation.
- Files modified by THIS task: only `KNOWLEDGE.md` + `src/superclaude/cli/roadmap/integration_contracts.py` + `tests/roadmap/test_integration_contracts.py` (3 files, 311 insertions, 61 deletions per `git diff --stat`).

**Caveat (IMPORTANT, not BLOCKING for this task's QA):** The pre-existing `.claude/` dirt MUST be addressed before any commit on this `fix/integration-contracts-mechanism-signature` branch — `git add` discipline alone is insufficient because `git add -f` would bypass the gitignore. Recommend a `make sync-dev` reconciliation (sync `src/superclaude/` → `.claude/`) as a pre-commit step, OR a `git checkout HEAD -- .claude/` to drop the local edits, depending on whether `src/superclaude/` has matching changes. This is OUT OF SCOPE for the current task's deliverable but IN SCOPE for the eventual commit hygiene.

### Check 7: Task file progress tracking

`grep -cE '^- \[x\]'` returns 38; `grep -cE '^- \[ \]'` returns 0 → all 38 checklist items marked complete. Frontmatter shows `status: "🟢 Done"`, `completion_date: "2026-05-25"`. Task Log section is well-populated:
- Execution Log: entries for task start + completion
- Phase 1 Findings: 7 items (Steps 1.1-1.7)
- Phase 2 Findings: 6 items (Steps 2.1-2.7 with Cycle 1 revision)
- Phase 3 Findings: 2 items (Steps 3.1-3.10 batched)
- Phase 4 Findings: 3 items (Steps 4.1-4.3 with Cycle 1 fix)
- Phase 5 Findings: 4 items (Steps 5.1-5.4)
- Phase Gate Findings: 3 items (PG.1-PG.3) + final verdict line
- Follow-Up Items: 2 documented
- Deviations: 3 documented with full RCA each

---

## Summary

- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 (pre-existing `.claude/` dirt — NOT introduced by this task; flagged for pre-commit attention)
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT (pre-existing, not task-caused) | `.claude/**` (136 files) | Working tree has 136 modified files under `.claude/` mirror. These are pre-existing inherited from master, NOT introduced by this task. | Before committing this `fix/integration-contracts-mechanism-signature` branch, run `make sync-dev` to reconcile `src/superclaude/` → `.claude/` OR `git checkout HEAD -- .claude/` to drop local edits. Do NOT `git add` any `.claude/` path (gitignored). Per CLAUDE.md ABSOLUTE RULE. |

## Actions Taken

None (fix_authorization: false; this is a read-only post-execution review).

## Recommendations

1. **For the eventual commit on this branch:** Address the pre-existing `.claude/` dirt via reconciliation step before staging. Only the 3 files this task actually modified should be in any commit on this branch: `src/superclaude/cli/roadmap/integration_contracts.py`, `tests/roadmap/test_integration_contracts.py`, `KNOWLEDGE.md`.
2. **For the follow-up:** The §7 stub at `.dev/tasks/to-do/TASK-RF-merge-prompt-wiring-directive-20260525-160000/` is a stub-form task, not a full MDTM task. When that follow-up is scheduled, it will need to be promoted to a full MDTM task file per Template 02.
3. **No code changes needed in this task's deliverable.** The implementation is correct, the deviations are defensible (and the spec authors would themselves have failed §4 backward-compat without them), the tests are comprehensive (58/58 green including all 7 new t1-t7 plus the 51-test baseline), and the end-to-end behavioral target is met (`total=5 uncovered=0` on live TUIBBS-scp v1-MVP).

---

## Confidence

- Verified: 7/7 (every check has at least one tool call directly verifying it)
- Unverifiable: 0
- Unchecked: 0
- Confidence: 100.0%
- Tool engagement: 20 calls / 7 checklist items = 2.86 calls per item (well above the 1:1 minimum)

The executor's manual rf-qa report is independently corroborated. The two documented deviations are not just "acceptable" — they are necessary corrections of internal spec contradictions, and the RCAs in `phase2-smoke-fix-plan.md` and `phase4-fix-plan.md` are correct.

---

## QA Complete

VERDICT: PASS
