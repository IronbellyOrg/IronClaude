# QA Report — Task File Qualitative Review

**Topic:** Fix reflect-reviewer-guard post-audit deviations D1–D4
**Date:** 2026-06-23
**Phase:** task-qualitative
**Fix cycle:** N/A (initial review)
**Fix authorization:** true (scope: files/components referenced by checklist items)

---

## Overall Verdict: FAIL (3 issues found — all FIXED in-place in the task file)

Two CRITICAL operational defects and one MINOR feasibility gap were found and
fixed directly in the task file. All fixes are in-scope (they touch checklist
items D1/D3 and components named in the task's Source Areas). After fixes, the
task is operationally sound and would execute correctly.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (PC.5 reflect run, test cmd, sync) | AX-3 | FAIL→fixed | `--depth/--fix/--promote` flags confirmed in commands.py:81-147; `--isolate-reviewers` default False (commands.py:167) so PC.5 default-path audits dirty tree, no `git add -A` needed; skip-guard precedes run. But D1 design-(b) telemetry edit would no-op (runner.py:682 omitted) — fixed. |
| 2 | Project convention compliance (src→.claude sync, no stage .claude) | none | PASS | Steps 3.3/4.2 run make sync-dev+verify-sync after src/ edits; never stage .claude/. Step 4.2 made conditional on an actual edit (fix). |
| 3 | Intra-phase execution order (HALT before impl) | none | PASS | Phase 2 HALT (Step 2.2) blocks Phase 3; Step 2.2 sets Blocked + STOPs if PENDING; never auto-defaults. Matches needs_human_decision-must-HALT rule. |
| 4 | Function signature verification (ensemble/models/runner) | AX-5 | FAIL→fixed | `_load_review_target()` reads `Path(config.tasklist_path).read_text()` (ensemble.py:441); `tasklist_path` is absolute-resolved (config.py:284) → design (a) needs path-rebasing, not naive join — fixed. |
| 5 | Module context analysis (all reviewer_isolation sites) | AX-3 | FAIL→fixed | THREE assign sites: ensemble.py:315, runner.py:518, runner.py:682. Task named only ensemble.py:315. runner.py:682 sets operator-visible ReflectResult — design (b) MUST edit it — fixed in Steps 1.3/2.1/3.1/3.2/3.4/PG.1. |
| 6 | Downstream consumer analysis (enum consumers) | none | PASS | No external switch-consumer breaks on a new enum value (conflict_detector.py:68 unaffected; process.py reads none). Existing test_reviewer_isolation_gate.py:84 asserts "snapshot" — flagged + fixed as expected-update. |
| 7 | Test validity (falsifier genuine, not stub) | none | PASS | D1 test asserts post-fix behavior absent pre-fix (design (b) value doesn't exist; design (a) target resolves under live path now). Genuine falsifier. Step 3.1 fail-before captured. |
| 8 | Test coverage of primary use case | none | PASS | New test exercises the isolation path end-to-end via the existing isolation-gate fixtures; design (b) mirrors the snapshot-success path. |
| 9 | Error path coverage | none | PASS | D3 Step 4.1 existence-precondition + blocker path; D1 HALT blocker path; reflect-run cannot-execute blocker path all present. |
| 10 | Runtime failure path trace (telemetry data flow) | AX-3 | FAIL→fixed | Traced reviewer_isolation: runner.py:682 writes ReflectResult → persisted to reflect_post; design (b) editing only ensemble.py leaves the operator-visible value as "snapshot" (silent no-op). Fixed. |
| 11 | Completion scope honesty (open questions resolved) | none | PASS | D1 HALT genuinely gates; D2/D4 NON-BLOCKING and do not gate Done; Done item (PC.6) requires PC.1-PC.5 success. |
| 12 | Ambient dependency completeness | AX-3 | FAIL→fixed | design (b) touchpoints incomplete (runner.py + existing test omitted). Fixed across decision record, anchor inventory, falsifier, fix, verify, QA aggregation. |
| 13 | Kwarg sequencing red flags | none | PASS | No add-kwarg-before-add-param pattern; HALT→impl ordering correct. |
| 14 | Function existence claims verified | AX-2 | FAIL→fixed | D3 claim "proposal DOES NOT EXIST" is FALSE — proposal exists (untracked) at canonical root; `pr199-round2-findings/` exists NOWHERE; parent task already corrected the line in the OPPOSITE direction. Fixed (Step 4.1 inverted-premise rewrite). |
| 15 | Cross-reference accuracy (SKILL.md §, anchors) | none | PASS | SKILL.md:268 Step 0.5e item 4 anchor verified verbatim; ensemble.py:218/315/433-444, models.py:139-141, runner.py:682 all confirmed at stated locations. |

## Summary
- Checks passed: 9 / 15 (6 FAIL→fixed in-place)
- Checks failed (unfixed): 0
- Critical issues: 2 (both fixed)
- Minor issues: 1 (fixed)
- Issues fixed in-place: 3

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 3.2 / 3.1 / 2.1 / 1.3 / 3.4 / PG.1 (D1 design (b)) | The design-(b) telemetry-honesty edit list named ONLY `ensemble.py:315-316`, but the operator-visible `ReflectResult.reviewer_isolation` is written at **`runner.py:682`** (`result.reviewer_isolation = "snapshot"`, persisted to `reflect_post`). Editing only ensemble.py is a silent no-op: the value the operator sees stays `"snapshot"`, and the design-(b) falsifier (Step 3.1) asserting `ReflectResult.reviewer_isolation == "snapshot-children-only"` would have no source for the new value. The existing `test_reviewer_isolation_gate.py:84` asserts `== "snapshot"` and would regress with no planned remediation site. | FIXED: added `runner.py:680-683` and the existing test:84 assertion to the edit-site list in Steps 2.1, 3.1, 3.2, 3.4, 1.3 (anchor inventory), and PG.1 (changed-file enumeration now via `git status --short`). Marked the existing-test update as a sanctioned, EXPECTED, non-EXEMPT change. |
| 2 | CRITICAL | Step 4.1 (D3 citation) | D3's premise is STALE/INVERTED. Research claims the proposal `.dev/analysis/pr199-reflect-hardening-proposal-2026-06-22.md` "DOES NOT EXIST" and instructs citing `.dev/reflect-hardening/pr199-round2-findings/`. Ground truth: the proposal **exists** (untracked) at canonical root `/config/workspace/IronClaude/`; `pr199-round2-findings/` exists **NOWHERE** (neither worktree nor canonical); and the parent task's Phase-8 note (POST-REFLECT-TASK.md ~L579) ALREADY rewrote the line to cite the real proposal and STOP citing round2-findings. As written, Step 4.1's own `test -d pr199-round2-findings/` precondition fails → blocker path; if forced, it would REGRESS a correct citation to a non-existent one (re-introducing the exact defect D3 exists to remove). | FIXED: rewrote Step 4.1 to re-verify ground truth across BOTH roots first, branch on actual disk state (no-op if the current line already cites only resolvable sources — which it does), and explicitly FORBID citing `pr199-round2-findings/` (verified to exist nowhere). Step 4.2 sync made conditional on an actual edit. |
| 3 | MINOR | Step 3.2 (D1 design (a)) | `config.tasklist_path` is an ABSOLUTE resolved path (config.py:284 `Path(tasklist_path).resolve()`). Design (a)'s "resolve under `reviewer_grounding_root`" cannot be a naive `grounding_root / tasklist_path` join (the absolute path would discard the root); it requires REBASING the tasklist relative to the repo root then joining under the snapshot. The task item's phrasing understated this. | FIXED: added explicit rebasing instruction + anchor lines to the design (a) clause and directed the falsifier to assert the rebased path resolves under the grounding root. |

## Answers to the Spawn-Brief Verification Questions

1. **Will the D1 edits work as written?**
   - **Design (b):** NO, as originally written — it would silently no-op. The
     operator-visible `ReflectResult.reviewer_isolation` is set at `runner.py:682`
     (verified), not `ensemble.py:315`. The task named only `ensemble.py`. Adding a
     `"snapshot-children-only"` enum value requires touching `models.py` (doc
     comments), BOTH emit sites (`ensemble.py:315-316` AND `runner.py:680-683`),
     the existing `test_reviewer_isolation_gate.py:84` assertion (`== "snapshot"`
     would regress), and `SKILL.md:268`. The task named only the first three.
     **FIXED.** After the fix the design-(b) edit list is complete and correct.
   - **Design (a):** FEASIBLE at `ensemble.py:218 / _load_review_target (433-444) /
     build_worker_prompt (415)` — verified those functions read
     `Path(config.tasklist_path).read_text()`. But `tasklist_path` is absolute, so
     the redirect needs path-rebasing, not a naive join. **FIXED** (MINOR note added).
2. **Is the D1 falsifier genuinely fail-before/pass-after?** YES, by construction.
   Design (b): `"snapshot-children-only"` does not exist pre-fix (verified the enum
   is `disabled|snapshot|stopped-precondition`), so the assertion fails before and
   passes after. Design (a): the target currently resolves under the live
   `tasklist_path` (verified ensemble.py:218/441), so an assertion that it resolves
   under `reviewer_grounding_root` fails before. Step 3.1 explicitly captures the
   fail-before baseline and forbids an EXEMPT label. PASS.
3. **Does the D1 impl gate on the HALT?** YES. Phase 2 Step 2.2 is a hard HALT:
   if `Chosen design:` is empty or `status: PENDING`, it sets frontmatter Blocked
   and STOPs (no further items, no auto-select). Phase 3 header repeats "Do NOT
   begin if Step 2.2 did not authorize it." Matches the needs_human_decision-must-HALT
   project rule. PASS.
4. **POST reflect gate preconditions:** The skip guard (`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`
   check) precedes the run — verified. `--isolate-reviewers` defaults False
   (commands.py:167), so the default-flag PC.5 run audits the working tree without
   a dirty-tree STOP; **no `git add -A` precondition is required** for this task
   (the brief's "git add -A before wrapper" concern does not apply because isolation
   is opt-in and OFF here). The `--depth deep --fix --promote` flags all exist. PASS.
5. **QA gate sufficiency:** PG.2 (3 rf-qa structural) + PG.3 (3 rf-qa-qualitative
   content) = 6 agents, parallel, `fix_authorization: false`, adversarial framing
   on each ("at least 5 errors"); PG.4 serializes fixes via ONE fix agent (per I20);
   PG.5 2-agent verification; max 3 cycles then HALT. PC.3 repeats the 6-agent gate
   post-completion. Meets ≥6 lens-focused serialized-fix floor. PASS.
6. **D2/D4 NON-BLOCKING + D4 no test change:** Phase 5 header marks both NON-BLOCKING
   and forbids setting Blocked on their account. Step 5.2 says "YOU MUST NOT modify
   `test_reviewer_finding_parity.py`" and only verifies the EXEMPT label (verified
   present and correct at the test's lines 1-17). No spurious test change. The Done
   gate (PC.6) does not depend on D2/D4. PASS.

## Actions Taken (fix_authorization: true; all in-scope to D1/D3 + named Source Areas)
- Step 3.2: rewrote design-(b) edit list to include `runner.py:680-683` + the existing
  `test_reviewer_isolation_gate.py:84` assertion update; added design-(a) absolute-path
  rebasing instruction with anchors.
- Step 3.1: added the runner.py:682 source-site note to the design-(b) falsifier.
- Step 3.4: clarified the design-(b) existing-test update is an EXPECTED, sanctioned
  change, not a regression.
- Step 2.1: expanded the design-(b) decision-record edit-site list (so the operator
  reads a complete site list before choosing).
- Step 1.3: expanded the anchor-confirmation to grep ALL THREE reviewer_isolation
  assign sites.
- Step 4.1 (D3): full rewrite — re-verify ground truth across both roots, branch on
  actual disk state (no-op if already correct), FORBID citing the nonexistent
  `pr199-round2-findings/`.
- Step 4.2: made the D3 sync conditional on an actual edit.
- Step PG.1: changed-file enumeration now via `git status --short` (not a hardcoded
  list) and includes runner.py + the existing test for design (b).
- Verification of fixes: re-read the edited Step 3.2 region (task file) and confirmed
  the design-(b) site list, design-(a) note, and Step 4.1 rewrite are coherent and
  internally consistent.

## Self-Audit
1. **How many factual claims independently verified against source?** ~20 — every
   D1 anchor (ensemble.py:218, 315-316, 415, 433-444; models.py:105, 139-143;
   runner.py:518, 682), the THREE reviewer_isolation assign sites, the existing
   isolation-gate test assertion (line 84), the `--isolate-reviewers/--depth/--fix/--promote`
   CLI flags, `tasklist_path` absolute resolution (config.py:284), enum consumers
   (conflict_detector.py:68, process.py), SKILL.md:268 spec sentence, the D4 EXEMPT
   label, and the D3 existence facts at BOTH roots.
2. **Files read to verify:** task file (full), 01-d1-d4-evidence.md, research-notes.md,
   ensemble.py, models.py, runner.py, config.py (grep), commands.py, SKILL.md (grep),
   reflect-reviewer.md (grep), test_reviewer_isolation_gate.py (full),
   test_reviewer_finding_parity.py (label), POST-REFLECT-TASK.md (grep), plus `test -e`
   existence probes across worktree and canonical roots.
3. **Why trust this with non-zero findings?** The two CRITICAL findings each required
   reading the ACTUAL source beyond the research summary: runner.py:682 is invisible
   from the research (which named only ensemble.py:315), and the D3 inversion was only
   detectable by probing both filesystem roots AND reading the parent task's later
   correction note. Neither would surface from a research-summary-only review.
4. **Web research:** None performed — all checks were local-file-bound. Tavily-first
   precedence not triggered.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
- No `## Inherited Structural Verdict` section was present in the spawn prompt; this
  was a standalone task-qualitative review with full independent verification (no
  rf-qa PASS items relied upon). All structural-adjacent checks (anchor/line accuracy,
  cross-references) were re-verified independently via Grep/Read/Bash.

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep/Bash: 9 | Glob: 0 (15 tool calls ≥ 15 checks)
- All 15 checks verified with tool evidence; no unchecked or unverifiable items.

## Recommendations
- The task is now operationally sound. Before execution, the operator should be aware
  that **D3 is most likely a no-op** (the current reflect-reviewer.md line already
  cites the existing untracked proposal correctly per the parent task's correction);
  the rewritten Step 4.1 handles this branch explicitly.
- The D1 design choice remains a genuine operator HALT — recommend the operator read
  the now-complete design-(b) edit-site list (which correctly includes runner.py:682)
  before deciding, since the original list understated design (b)'s blast radius.

## QA Complete
**VERDICT: FAIL — 3 issues found (2 CRITICAL, 1 MINOR), ALL FIXED in-place.** No
unfixable issues remain. The task file is now operationally correct.
