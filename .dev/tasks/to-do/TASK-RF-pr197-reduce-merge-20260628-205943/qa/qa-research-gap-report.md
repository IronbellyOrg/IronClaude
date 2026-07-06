# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** PR #197 reduce-then-merge MDTM tasklist research gate
**Date:** 2026-06-28
**Phase:** research-gate
**Lens:** gap-detection (adversarial — assume areas missed)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Research dir: `.dev/tasks/to-do/TASK-RF-pr197-reduce-merge-20260628-205943/research/`
Spec: `.dev/brainstorms/pr197-final-merge-strategy/merged-requirements.md` (§7 + Appendix)
Track goal: 6-phase reduce-then-merge plan on `feat/rf-harness-sync`.

Verification log appended incrementally below.

---

## Files Verified

| File | Read | Cross-checked vs spec/ground-truth |
|------|------|-------------------------------------|
| research-notes.md | yes | EXISTING_FILES, GAPS_AND_QUESTIONS, SUGGESTED_PHASES |
| research/01-git-disposition.md | yes | 18-file matrix vs spec Appendix; restore/rm one-liners |
| research/02-reflect-skill-hunk-surface.md | yes | 12-hunk map vs spec Step 3 |
| research/03-taskbuilder-clause-flip.md | yes | clause flip vs spec Step 4; residual tension |
| research/04-template-tests-validation.md | yes | validation commands vs spec Steps 1-6; Makefile/pre-commit |
| spec merged-requirements.md §7 + Appendix | yes | ground truth (source of plan) |

Ground-truth tool checks: git divergence/SHA, `git cat-file -e` on restore targets (refs exist on master), grep sweeps for commit/rollback/baseline/staging coverage across all 4 research files, `npx` availability.

---

## Gap-Focus Findings (8 lens areas)

### Q1 — BASELINE / Step 0 pre-state capture: **GAP (IMPORTANT)**
Spec Step 0 = `git fetch origin && git status` (confirm 1U only) + `uv run pytest tests/cli/reflect tests/swarm -q` **to capture pre-state**. The research "Baseline" sections (01-git-disposition lines 9-22, research-notes lines 14-19) cover only the *git-divergence* baseline (SHA, ahead/behind, 18-file diff). **No research file captures or even mentions the Step 0 pre-state pytest run.** This matters because Steps 2-5 re-run those same suites (`tests/cli/reflect`, `tests/swarm`) as validation; without a recorded pre-state baseline, the builder cannot tell the executor how to distinguish a *pre-existing* failure from a *regression introduced by the reduction*. R4 separately flags `make lint`/`ruff format --check` produce pre-existing noise (104 files, lint-architecture) — the same "is this failure mine?" problem applies to the pytest suites and has no baseline-capture remedy in research. Builder needs: a Phase-0 item that runs the Step 0 suites and records pass/fail counts to a findings sink, referenced by every later validation item.

### Q2 — ORDERING hazards (Step 2 → 3 → 4 cross-interaction): **PARTIAL GAP (MINOR)**
- Step2(runner.py restore) → Step3(SKILL.md surgery): research does NOT explicitly analyze whether restoring master `cli/reflect/runner.py` interacts with any `sc-reflect-protocol/SKILL.md` reference edited in Step 3. Verified independently: these are disjoint surfaces (one is the CLI runner .py, the other is skill prose); no collision exists. So the *absence* is not a correctness risk, but the research never states the non-interaction, leaving the builder to assume it. Low severity.
- Step3(reflect SKILL.md = restore master §7.1 = EXCLUSION) ↔ Step4(task-builder CLI cluster flip = EXCLUSION): R3 (03-taskbuilder-clause-flip lines 187-193 "Residual tension") flags this as **"the single most important cross-researcher dependency"** and leaves it conditionally unresolved ("If R2 keeps reflect instance-level → the flip is incoherent"). R2 (02-reflect-skill-hunk-surface) in fact restores reflect to master = exclusion, which *resolves* the tension favorably — BUT no file closes the loop by stating "R2 confirms reflect → exclusion, therefore the Step-4 CLI flip is coherent." See Q-cross below — promoted to IMPORTANT because the builder must encode this dependency or risk emitting a contradictory Step 4.

### Q3 — `make sync-dev` TIMING (sync before verify-sync, per editing step): **PARTIAL GAP (IMPORTANT)**
The sync→verify-sync ordering is captured **generically** (01-git-disposition line 124 "After edits run make sync-dev"; 03-taskbuilder-clause-flip line 149 "after Edit + make sync-dev"; R4 line 92 verify-sync is the read-only gate). However:
- Step 3 (reflect SKILL.md + refs restore) edits `src/` but **NO research file states that Step 3 must run `make sync-dev` before its validation** — Step 3's spec validation is pytest+grep on `src/`, so the `.claude/` mirror for `sc-reflect-protocol` would be left stale until Step 5. R4 line 99 even notes the `.dev/` tasklist is markdownlint-exempt but says nothing about when the sc-reflect-protocol mirror gets synced. The spec runs `make sync-dev && make verify-sync` only at Steps 1 and 5, NOT after Step 3. So Step 3 src-edits sit un-synced across Step 4 — research does not flag that Step 5's verify-sync is the first integrity check covering Step 3's edits, nor whether an intervening Step-4 verify-sync (Step 4 DOES run verify-sync) would FAIL because Step 3's mirror is stale. **This is a real ordering hazard: Step 4's `make sync-dev` (line 149) will sync BOTH task-builder AND the already-edited reflect SKILL.md, but if Step 4 runs `make verify-sync` before its own sync-dev, or if Step 3 is partially applied, verify-sync drift is ambiguous.** Builder needs explicit per-editing-step sync-dev sequencing (sync-dev immediately after each `src/` edit phase, before that phase's verify-sync), which research does not lay out.

### Q4 — ROLLBACK / safety on validation failure: **GAP (CRITICAL)**
Grep across all 4 research files for `rollback|recover|git reset|--abort|half-applied|undo|revert if|if...fails` returns **ZERO hits**. There is **no recovery guidance anywhere** for:
- A half-applied hunk surgery on `sc-reflect-protocol/SKILL.md` (R2 enumerates 12 hunks across 9 RESTORE + 4 RETAIN edits — the highest-risk, most-error-prone step — with no "if validation V1-V6 fails, how to get back to a known state" path).
- A bad `git checkout origin/master -- <path>` that restores the wrong blob.
- The shared-index hazard: per memory `feedback_parallel_sessions_share_index`, multiple Claude sessions in this worktree share one git index/HEAD; a `git checkout origin/master -- …` or staging during a concurrent session can be clobbered. R4 line 71 even notes a **sibling build `TASK-RF-reflect-ac-hybrid-20260628-205715` is mid-flight** in this same worktree — a live concurrent-session risk — yet no research file warns the tasklist to guard the index or recommends committing-per-step to create rollback points. This is the single most important safety gap for a destructive git-reduction task and blocks a safe builder output.

### Q5 — `.claude/` staging trap after sync-dev: **PARTIAL GAP (IMPORTANT)**
The *negative* rule is covered well (01-git-disposition lines 122-127: never `git add` `.claude/` except settings.json; `-f` = siren; gitignored confirmed). **But the workflow framing the lens asks about is missing:** no research file states that *after `make sync-dev`, `git status` WILL show modified `.claude/` paths* and that the executor must recognize those as expected sync output to be left unstaged — nor does any file give the **positive** staging list (which `src/` paths to `git add` for the commit). Grep for "git add | stage src | what to stage" returns only the negative rule. A builder working only from this research could author a commit item with no guidance on the correct `git add src/...` set, and an executor seeing dirty `.claude/` after sync-dev has no research note telling them that is normal. Couples directly to Q6.

### Q6 — COMMIT strategy: **GAP (CRITICAL)**
Grep for `git commit|commit the|must be committed|commit guidance|commit item|commit strateg` across all research + research-notes = **ZERO hits (literally "NO COMMIT GUIDANCE FOUND IN RESEARCH").** The spec is explicitly *reduce-**then-merge***: Steps 2-4 mutate the working tree (restores, rm, hunk edits) and Step 6 does `git push origin feat/rf-harness-sync`. **A push pushes commits — but no step and no research file commits the reductions.** Between Step 5 (validation) and Step 6 (push) there is an un-bridged gap: the working-tree reductions must be staged + committed before push, or `git push` ships nothing (or ships the un-reduced branch). research-notes RECOMMENDED_OUTPUTS (line 63) describes "7 phases ... final completion" but never a commit phase. R4's PR-hygiene section (lines 122-156) covers rebase/push/auggie-review but **skips the commit entirely**. This is a structural hole: the builder has no research basis to author the commit item(s) that make Step 6's push meaningful. CRITICAL — without it the tasklist's terminal push is a no-op or ships wrong content.

### Q7 — Findings actionable for a task builder: **MOSTLY PASS (one MINOR)**
The four research files are exceptionally actionable where they have coverage: exact line numbers, verbatim before/after text, exact single-line commands (dry-run-verified), explicit grep validations with expected results, and named footguns (markdownlint variant, lint-architecture noise, ruff 104-file noise). This is dense, builder-ready evidence. The one actionability defect: the markdownlint command. Spec Step 1 literally says `npx markdownlint-cli2 "...{glob}..."`; R4 (lines 98-106, 161) verified the repo actually uses **`markdownlint-cli`** (v0.38.0, NOT cli2) and that bare `markdownlint`/`markdownlint-cli2` are not on PATH, recommending `npx -y markdownlint-cli@0.38.0 <6 explicit paths>`. This is a *correct catch* by R4 (a spec-vs-reality discrepancy) — but it is buried as a "FLAG" rather than stated as a directive resolution, and R4 does not note that the spec's brace-glob `{operational-guide,readme,...}` may not expand under `npx`+the shell quoting the spec uses. Builder must be told explicitly: use the 6 enumerated paths, `markdownlint-cli@0.38.0`, not the spec's literal cli2 glob. MINOR (info present, resolution under-stated).

### Q8 — Integration: reflect SKILL.md hunk surgery ↔ refs/ files restored in Step 3: **GAP (IMPORTANT)**
Step 3 restores `refs/reviewer-spec.md` and `refs/reflection-rubric.md` to master (full checkout) **and** hunk-surgically restores SKILL.md §7.1 to master's executor-class-exclusion model. For these to be consistent, master's refs must describe the same exclusion model that master's §7.1 describes — they do, by construction (both come from the same master commit). **But no research file cross-validates this.** Grep of 02-reflect-skill-hunk-surface for any reviewer-spec/reflection-rubric consistency check returns empty; R2 enumerates SKILL.md hunks in isolation and never reads the refs to confirm the restored SKILL.md §7.1/§11.3 prose agrees with the restored refs' reviewer-composition/rubric content. R2 §3.4 (line 137) does confirm the *N=2 floor* survives in master §7.1 so the retained EV hunks' cross-references stay valid — good — but that is the EV↔SKILL consistency, NOT the SKILL↔refs consistency the lens asks about. Risk: if #197 changed a ref in a way that a *partial* master-restore of SKILL.md leaves dangling (e.g., SKILL.md cites a refs section that master's refs name differently), the surgery passes greps but ships an internally inconsistent skill. Builder should add a post-Step-3 consistency check (does restored SKILL.md reference the restored refs by names/sections that exist in the master refs). Not closed by research.

### Q-cross (promoted) — R2/R3 dependency not closed: **IMPORTANT**
R3 explicitly hands off the reflect-disposition reconciliation as "R3 does not own this reconciliation ... the single most important cross-researcher dependency for Step 4" (03 line 193). R2 supplies the answer (reflect → master = exclusion) but the two files were never reconciled into a single statement. The research package as a whole leaves the most consequential cross-step coherence question (is Step 4's exclusion-flip coherent given Step 3's reflect state?) answered only by the QA agent connecting R2+R3 manually. A builder reading the files independently could miss it. The tasklist MUST encode: "Step 4 CLI flip → exclusion is coherent BECAUSE Step 3 restores reflect to master's exclusion model; clauses 4/5 contract-field wording must match master's actual contract (R2 §2.4/§2.7 telemetry fields restored)."

---
