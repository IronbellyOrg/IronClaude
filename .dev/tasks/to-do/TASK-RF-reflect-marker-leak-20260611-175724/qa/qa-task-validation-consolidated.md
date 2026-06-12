# Task-Validation Consolidated Findings + Fix Directive (A.10 + A.10.25 + A.10.5)

5 validation agents (2 rf-qa structural + 1 rf-analyst alignment + 2 rf-qa-qualitative) all returned FAIL. Consolidated below with orchestrator decisions on the nuanced items. ONE serialized fix agent (I20) applies ALL of these.

## CRITICAL (must fix — would mislead or break execution)

- **C1 — POST-gate false-green suppression (Step 4.14).** The guarded `if [marker=1]; then echo suppressed; exit 0; else superclaude reflect run …` counts a *suppressed nested gate* as POST success without running any audit. **FIX:** Step 4.14 must (a) ASSERT `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` is UNSET/absent before claiming dogfood proof; (b) if the marker is `1` (executing inside a wrapper), record a DEVIATION and treat the step as "dogfood deferred — nested-gate suppression, NOT proof" (do NOT count as success); the dogfood proof requires a marker-absent run.
- **C2 — `--promote` vs Step 4.15 path collision.** Step 4.14 uses `--promote`, which moves the task dir to `done/` on clean PASS, but Step 4.15 reads/writes the `to-do/` path. **FIX:** change Step 4.14's wrapper invocation to **`--no-promote`** (the dogfood audits in place, matching the parent task's own 6.3). Remove `--promote`.

## IMPORTANT

- **I1 — §6.1.1 control-count preface (Step 2.1).** The envelope says "All eight controls are mandatory"; adding control (i) makes nine. **FIX:** Step 2.1 must ALSO update the preface count "eight"→"nine" (and QA Step 4.2 checks it).
- **I2 — `template_schema_doc` cites `.claude/` mirror (frontmatter L47).** **FIX:** change to `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (source-of-truth path).
- **I3 — `sc-tasklist-protocol/SKILL.md` "NO UPDATE NEEDED" resolution dropped.** **FIX:** add an explicit Key-Constraint / Step-1.3 assertion that `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` marker references are confirmed OUT OF SCOPE (O2 gate-emission skip guards) and must NOT be edited.
- **I4 — B2 dynamic scope in Steps 4.10/4.11** ("all files changed by the fix agent"). **FIX:** name the specific files the verification agents read: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `tests/cli/reflect/test_marker_suppression.py`, the task file, and (if edited) the contract — instead of "all files changed by the fix agent".
- **I5 — Step 4.9 fix-agent prompt uses relative filenames.** **FIX:** use absolute paths (`…/qa/qa-consolidated-findings.md`, `…/qa/qa-fix-agent-report.md`).
- **I6 — Parallel-batch encoding for Steps 4.2-4.7.** M3 wants the 6 lens agents spawned in parallel (one message). **FIX:** add a directive at the top of the QA gate that Steps 4.2-4.7 are a single PARALLEL batch (spawn all 6 report-only agents in ONE message), each marked complete as it returns.
- **I7 — Fix-cycle loop under-encoded (Steps 4.10-4.12).** References 2 cycles but no loop. **FIX:** Step 4.12 must encode: if either verification report FAILs and cycle<2, re-consolidate → ONE serialized fix agent → re-run both verification agents → re-evaluate (regression→monotonicity→cap per the Phase Gate Findings protocol).
- **I8 — Cross-worktree contract edit safety (Step 2.3).** **DECISION: DEFAULT TO THE DEFERRAL ARTIFACT.** Per worktree discipline (`feedback_worktree_discipline`), editing the sibling `reflectWrapper` worktree's contract from THIS worktree is unsafe (it may collide with the sibling task that owns it). **FIX:** Step 2.3 should DEFAULT to writing the deferral artifact (`phase-outputs/plans/contract-carveout-deferral.md` with the exact deferred patch), and only edit the sibling contract if the operator explicitly authorizes it in-session. Frame the contract edit as the non-default path.
- **I9 — Step 3.5 overclaims ("re-proves the fix").** The source-contract test + marker tests prove TEXT presence + existing marker-guard behavior, NOT live verification-grandchild env stripping. **FIX:** reword Step 3.5 to state it proves the source-contract presence of the env-strip control + that nested-gate suppression still holds; reserve end-to-end behavior claims for Step 4.14.
- **I10 — Skill-load-path fallback (Step 4.14 / OQ).** **DECISION: SIMPLIFY.** Keep the concern as an Open Question only; in Step 4.14, add a concrete note that the dogfood runs AFTER `make sync-dev` (which updates the worktree `.claude/` the subprocess reads) — and IF the gate still exit-11s, record the unit-test + manual marker-absent `env -u` pytest proof as the documented acceptance evidence (a deviation, not a silent pass). Remove the vague "sync or install to the path the subprocess reads" prose; replace with: "the dogfood is best-effort; the binding acceptance evidence is the regression test + the marker-absent pytest proof."
- **I11 — Frontmatter missing fields + blocked-status inconsistency.** Step 4.15 uses `🔴 Blocked`; the Frontmatter Update Protocol uses `⚪ Blocked`. **FIX:** make blocked-status consistent (`⚪ Blocked`). Add any template-required frontmatter fields flagged (created_date is present; ensure no contradictory status enum).

## MINOR

- M1 — "## Post-Completion Actions" section absent. NON-BLOCKING: anti-orphaning is already satisfied (status→Done is the last item inside the final phase). Optional; skip unless trivial.

## Fix disposition
ONE rf-qa fix agent (fix_authorization: true) applies C1-C2 + I1-I11 to the task file (and only the task file — these are task-file fixes, no source edits). M1 optional. Then 1 verification agent confirms. Max 2 cycles.
