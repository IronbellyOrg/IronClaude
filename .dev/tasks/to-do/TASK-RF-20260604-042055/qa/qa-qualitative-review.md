# QA Report — task-qualitative

**Topic:** Implement reflect-in-task-builder.md + reflect-in-sc-tasklist.md proposals
**Date:** 2026-06-04
**Phase:** task-qualitative
**Fix cycle:** N/A (first pass)

---

## Overall Verdict: FAIL (2 MINOR issues, both fixed in-place)

Adversarial task-qualitative review of all 45 items against the actual target source
files (not research summaries). Every load-bearing anchor was re-verified live; both
proposals' implementer checklists were cross-walked against the task items; the S4 trim
arithmetic, the dogfood POST command runnability, and the G-1 break-risk avoidance were
verified against actual source + test code.

---

## Proposal-1 cross-walk (reflect-in-task-builder.md §8 → task items)

| Proposal-1 §8 delta | Task item | Anchor live-verified | Status |
|---|---|---|---|
| `--spec` to Input surface | Step 2.1 | `## Input` 4-item prose list @29-39, before `### Effective Prompt Examples` @41 | COVERED |
| A.2 spec_path resolution | Step 2.2 | A.2 GOAL/WHY/OUTPUTS/CONTEXT bullets @194-197, before Triage @199 | COVERED |
| New A.10.7 PRE gate + pipeline bullet | Steps 2.3, 2.4 | A.10.6 @1339 ends @1396; A.11 @1398; Exec-Overview steps 12/13 @160-161 | COVERED (drift corrected: between A.10.6 and A.11, not A.10.5/A.11) |
| A.9 POST_REFLECT_GATE block | Step 2.5 | EXEC_CONTEXT_REQ @827 ends @847; DOC STALENESS @849; both inside `text` fence @787 | COVERED |
| New Critical Rule #19 | Step 2.6 | rule 18 @2034 (highest); `**Precedence rule:**` @2036 | COVERED |
| Output Structure frontmatter keys | Step 2.7 | example YAML @1866-1885; `task_type: static` @1878 before `related_docs:` @1879 | COVERED |
| Output Structure penultimate POST item | Step 2.8 | Phase N example @1928; `N.X — Update task status to Done` @1930 (last) | COVERED |
| Validation-checklist POST-present guard | Step 2.9 | checklist @1957-1979; anti-orphaning @1969; TB-Add-8 last @1979 | COVERED (G-1 plain-bullet path) |
| A.11 REFLECT GATES block | Step 2.11 | A.11 @1398; single+multi-track result fences | COVERED |
| New TCS section (§5) + S4 trim | Steps 2.12, 2.13 | between Critical-Rules close `---` @2038 and `## Research Quality Signals` @2040 | COVERED |
| SoT sync / verify / lint | Steps 2.14, 2.15 | Makefile sync-dev/verify-sync; MD040 | COVERED |

Proposal-1: **no omitted delta.** All 11 §8 sub-deltas map to a task item at a live-verified anchor.

## Proposal-2 cross-walk (reflect-in-sc-tasklist.md §6 → task items)

| Proposal-2 §6 delta | Task item | Anchor live-verified | Status |
|---|---|---|---|
| `--no-reflect` command Usage + Arguments | Steps 3.1, 3.2 | Usage @23 (`--spec` already present); Args rows @36-38 | COVERED (`--spec` correctly NOT re-added) |
| `--no-reflect` skill argument-hint | Step 3.3 | `argument-hint:` @9 (command has NO argument-hint key) | COVERED |
| Stage 10.5 pre-reflect fan-out | Step 3.4 | Stage 10 @1359; gate line @1386; `---` @1388; insert between | COVERED |
| 10→11 stage table + lead sentence | Step 3.5 | lead "10 stages" @1392; Stage 10 row @1405 | COVERED |
| Stage bookkeeping (TaskCreate/deps/completion/Tool) | Step 3.6 | TaskCreate @1424; Deps @1439-1449; completion @1451-1462; Tool `Task` @1479 | PARTIAL — see ISSUE-1 |
| 4-invariant checkpoint-is-last amendment | Step 3.7 | Self-Check 6 @1073; structural 18 @1113, 19 @1114, 20 @1115; close-line @1117 | COVERED |
| Cadence rule + template definition amendment | Step 3.8 | `### 4.8` cadence @359; `#### End-of-Phase Checkpoint` @1011 (`<last_num>` @358) | COVERED |
| Templated POST task — inline §6B | Step 3.9 | phase-file content contract @96; metadata table @862-916; checkpoint @1011 | COVERED |
| Templated POST task — mirror phase-template | Step 3.10 | `## End-of-Phase Checkpoint (Mandatory)` @117-125 | COVERED |
| Per-phase COMPLEXITY_SCORE section | Step 3.11 | Tier Dist @707-718; Traceability @759-773; CPO @425-435 | COVERED |
| Index Pre-Reflect column + summary — inline §6A | Step 3.12 | Phase Files table @705-718; metadata @681-684 | COVERED |
| Index Pre-Reflect column + summary — mirror | Step 3.13 | index-template Phase Files @53-57; metadata @21-32 | COVERED |
| validation/reflect-pre,reflect-post,depth-map.yaml | Step 3.14 | intended-locations @87; Target Layout tree @110-123; index Artifact Paths @700 | COVERED |
| SoT sync / verify / lint | Steps 3.15, 3.16 | as above | COVERED |

Proposal-2: all §6 deltas mapped; one PARTIAL (ISSUE-1) on a secondary bookkeeping surface.

---

## Items Reviewed (15-item task-qualitative checklist × 5 adversarial axes)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `make sync-dev`/`verify-sync` exist (Makefile @109/@166); regression cmd `uv run pytest tests/audit/ tests/skills/test_task_builder_merge.py tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py` — all 4 paths exist on disk; preconditions (start_commit captured Step 1.3 before POST consumer) satisfied |
| 2 | Project convention compliance | none | PASS | All edits target `src/superclaude/` (SoT); sync-dev loop @117 recursively copies `templates/*.md` under skill → Step 3.15 claim accurate; verify-sync `diff -rq` @178 catches unsynced mirror; mirrors edited as PAIR (3.9+3.10, 3.12+3.13) |
| 3 | Intra-phase execution-order sim | none | PASS | Phase 1 captures start_commit + anchors before Phase 2/3 edits; Step 1.4 drift-guard precedes all edits; sync (2.14) before verify (2.15); edits before tests (Phase 4) |
| 4 | Function/anchor signature verification | AX-1 | PASS (drift corrected) | Every load-bearing anchor live-grepped: A.10.6@1339, A.11@1398, rule-18@2034, EXEC_CTX@827, 4 checkpoint invariants@1073/1113/1114/1115, cadence@359, Stage10@1359. Task corrects the proposal's STALE "between A.10.5 and A.11" → "between A.10.6 and A.11" |
| 5 | Module context analysis | none | PASS | A.9 insert stays inside the `text` fence @787 (no new fence); API-004 halt wire-strings (1062-1123) + BLOCK_HEADER `## Inherited Structural Verdict` (1232/1380) are NOT adjacent to the A.9 BUILD_REQUEST template (787-855) — byte-exact preservation directive is sound |
| 6 | Downstream consumer analysis | AX-3 | PASS (1 MINOR fixed) | 4-invariant amendment (3.7) + cadence/template (3.8) co-amended; mirrors paired. Stage 10.5 bookkeeping surfaces: Step 3.6 originally named 4 but a 5th (prose Dependency-chain @1415-1420) was at risk — FIXED |
| 7 | Test validity | none | PASS | Verification steps run the REAL pytest suites + verify-sync + markdownlint on the actual edited files (not stubs); S4-trim grep (2.13) asserts literal token set |
| 8 | Test coverage of primary use case | none | PASS | research-04 regression subset covers the break-risk surfaces (audit/ DNSP+INV, merge test, checkpoint tests); FINAL_ONLY rf-qa + rf-qa-qualitative gate (5.2) exercises end-to-end edit landing |
| 9 | Error-path coverage | none | PASS | Every item has a "log blocker / mark complete" branch; 2.15/3.16 have markdownlint-FIX-then-recheck loop; 4.2 triages NEW-vs-baseline failures |
| 10 | Runtime failure-path trace | AX-2 | PASS (1 MINOR fixed) | Dogfood POST `/sc:reflect` command uses only real reflect flags (--mode post/--remediate/--diff/--tasklist/--spec/--depth/--executor-model all verified in reflect.md); UC-2 `--diff` satisfies STOP guard; `<START_COMMIT>` resolvable from frontmatter. "larger proposal" mislabel FIXED |
| 11 | Completion-scope honesty | none | PASS | Open Question @416 is informational (POST depth floor), not item-basis; dogfood item HALTs with `reflect_post: PENDING`, does NOT self-resolve; Done-flip is strictly last |
| 12 | Ambient dependency completeness | AX-3 | PASS (covered by ISSUE-1 fix) | argument-hint (3.3) vs command Usage (3.1) correctly split; validation/ dir convention (3.14) covers reflect-pre/reflect-post/depth-map; index column + summary paired inline+mirror |
| 13 | Kwarg sequencing | none | PASS | No "add kwarg before add param" inversion; spec_path producer (A.2, 2.2) before A.10.7 consumer (2.3); start_commit producer (1.3) before dogfood consumer |
| 14 | Existence claims grep-verified | AX-5 | PASS | "blockedBy 0 hits" CONFIRMED (grep empty); "after Phase only @1993 Content-Rules" CONFIRMED; "no TB-Add-9 / 28 items" CONFIRMED (rf-qa.md@298 + merge-test@69,190); no invented files/flags |
| 15 | Template cross-references | none | PASS | Both mirror templates read live; headers self-declare "extracted from SKILL.md §6A/6B"; End-of-Phase Checkpoint@117-125 (phase mirror), Phase Files table@53-57 (index mirror) confirmed |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|-------------|--------|
| 1 | MINOR | Step 3.6 (AX-3 omission) | Named only 4 stage-bookkeeping surfaces; a 5th — the PROSE `**Dependency chain** (Stages 7-10):` block @SKILL.md:1415-1420 (distinct from the TaskCreate `Dependencies:` block @1439) — would be left inconsistent after Stage 10.5 lands (it says "Stage 10 is blocked by Stage 9" but never gains "Stage 10.5 is blocked by Stage 10"). Execution-only inconsistency (the prose mirrors the TaskCreate deps), not a runtime break. | Broaden Step 3.6 to enumerate FIVE surfaces incl. the 1415-1420 prose chain; clarify that narrative "Stages 7-10" mentions describe the validation sub-range and need NOT change. | FIXED in-place |
| 2 | MINOR | Post-Completion dogfood item (AX-2 contradiction) | Prose rationale says "the larger proposal is passed" but it passes `reflect-in-task-builder.md` (279 lines) while `reflect-in-sc-tasklist.md` is 297 lines — the actually-larger one. The `--spec` CHOICE is fine (it matches frontmatter `spec_path:` @48) but the "larger" justification is factually wrong. | Reword to "PRIMARY proposal (frontmatter-consistent)"; note the two are comparable size so neither is materially larger. | FIXED in-place |

Both issues are MINOR and were fixed in-place (fix_authorization: true). Neither would have caused
execution failure; ISSUE-1 a doc-consistency drift, ISSUE-2 a misleading-rationale contradiction.

### S4-trim observation (NOT a defect — operator-instructed, recorded for the POST audit)

The TRACK GOAL explicitly instructs `S4 token-set trim → {after Phase \d+, depends_on:}`. The task
(Steps 2.12/2.13) implements this LITERALLY and correctly does NOT silently retain the proposal's
4-token form. Adversarial note: the trim swaps the proposal's per-item dependency-reference form
`depends on N\.\d+` for the frontmatter YAML key `depends_on:`, which is emitted at most ONCE per
file (it is a frontmatter array key, not a per-item body token — confirmed: `depends_on:` has 0 hits
in generated MDTM bodies in the real corpus, and appears as `depends_on: []` only in frontmatter).
So the trimmed S4 will be near-inert (counts ≤1). However: this is the operator's explicit
instruction, S4 retains weight ×2, and proposal §5.3's band-threshold re-check is unaffected (S5/S1
dominate; bands ≤12/13-34/≥35 unchanged) — so TCS determinism and band partitioning survive the
trim coherently. This is drift-BY-INSTRUCTION, not drift-by-error; it is in-scope and faithful.
Recorded here so the fresh-session POST reflect operator is aware the trimmed S4 signal is weak.

---

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa PASS items I skipped structural re-check for:**
- Relied on rf-qa PASS for check 5 (Anchors match research, live-verified) — I did NOT re-run the full anchor-accuracy parse; instead I independently re-grepped the LOAD-BEARING anchors only.
- Relied on rf-qa PASS for checks 1-4, 8, 9, TB-Add-1..8, BS-1..8 (frontmatter shape, item structure, S4 literal-set presence, G-1 plain-bullet, mirror-pairing, UV-only subset, no-multiline-paste, /sc:task-never).
- Relied on rf-qa PASS for check 16 (start_commit producer-before-consumer execution order).

**(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT and my own tool work was required (≥1, INV-019):**
- **Anchor COMPOSITION (not just accuracy):** rf-qa verified the A.10.6/A.11 LINE numbers; I read the actual 1339-1398 region and confirmed the A.10.7 additive insert COMPOSES at the blank line between A.10.6's end (1396) and A.11 (1398) WITHOUT displacing the DM-005 contract YAML or the API-004 wire-strings. rf-qa's line-accuracy check could not establish this. (Read: task-builder SKILL.md @1339-1408.)
- **Cross-proposal completeness:** rf-qa does not cross-walk BOTH proposals' implementer checklists against the items; I built both cross-walk tables above and found the Step 3.6 omission (ISSUE-1) that no structural check would surface.
- **Dogfood command RUNNABILITY:** rf-qa verified the command is single-line; I verified every flag exists on the actual `reflect.md` surface and that the UC-2 `--diff` STOP-guard is satisfied — establishing the gate is operationally executable, not just well-formed.
- **Break-risk avoidance against TEST code:** I grepped `test_task_builder_merge.py` and confirmed the literal `"#### Checklist (28 items)"` assertions @69,190 — proving the G-1 path (no rf-qa.md edit) keeps those tests green, which the structural verdict asserts but does not demonstrate against the test source.

Self-Audit questions:
1. **Factual claims independently verified against source:** ~30 (every anchor line, both token-set grep results, all 4 reflect-flag existences, the 28-items test assertions, the sync-dev/verify-sync Makefile behavior, MD040 config).
2. **Files read to verify:** task-builder/SKILL.md (8 regions), sc-tasklist-protocol/SKILL.md (7 regions), commands/tasklist.md (full), commands/reflect.md (flag surface), both mirror templates (full), Makefile (sync loops), .markdownlint.json, both proposals (full), research-01 (S4 section), and grep/ls against rf-qa.md + 4 test files + real corpus.
3. **Why trust this review found real issues:** I found 2 genuine MINOR defects (a 5th bookkeeping surface omission and a size mislabel) that required reading the ACTUAL SKILL.md prose-vs-TaskCreate dependency duplication and comparing proposal line counts — neither derivable from research summaries. Adversarial stance held: I did not accept "0 issues."
4. **Web research:** None performed (all verification was local-file-bound — no external vendor/standard lookup required for this protocol-edit task). Tavily-first rule N/A this review.

---

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 7 | Glob: 0 | Bash: 8 (Bash calls bundled grep/wc/ls verifications). Total source-touching calls (20) ≥ 15 checklist items — engagement minimum satisfied.
- Every checklist item maps to ≥1 concrete tool verification above; no padding.

---

## Recommendations

1. Both MINOR issues are FIXED in-place — no further action required before execution.
2. The S4-trim observation is informational; flag it to the fresh-session POST reflect operator so the
   trimmed S4's near-inert behavior is noted in the deviation audit (it is in-scope and instructed).
3. The FINAL_ONLY rf-qa + rf-qa-qualitative gate (Step 5.2) should, during execution, re-confirm the
   1415-1420 prose dependency-chain block actually received the Stage 10.5 entry (the ISSUE-1 fix makes
   the item DIRECT it, but verify the executor lands it).

---

## VERDICT: FAIL

Two MINOR issues found (ISSUE-1 AX-3 omission, ISSUE-2 AX-2 contradiction), BOTH fixed in-place via
Edit under fix_authorization: true. Per task-qualitative policy (ALL severities must resolve before
proceeding; no severity is exempt), the pre-fix verdict is FAIL. With both fixes applied and verified,
the task plan is now operationally sound and would succeed if executed. No CRITICAL or IMPORTANT issues
exist. No unfixable issues remain.

## QA Complete
