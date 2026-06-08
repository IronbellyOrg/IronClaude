# Next-Session Prompt — Phase 6 / R1.1 — Extend `superclaude.contracts` SoT

**Copy-paste the following into a fresh Claude Code session.** This prompt is self-contained: it references all the source-of-truth files by absolute path and does not depend on prior session context.

---

## Prompt

I'm continuing the roadmap-pipeline brittleness-elimination rewrite. R0 bridge (Phases 1-5) is complete on PR #112 at https://github.com/IronbellyOrg/IronClaude/pull/112. Now I want to land Phase 6 (R1.1 — extend `superclaude.contracts` SoT module) using the same one-phase-per-launch pattern from R0.

**Working branch:** `refactor/roadmap-pipeline-r0-r1-rewrite` in the worktree at `/config/workspace/IronClaude-RoadmapRewrite/`. Verify with `git -C /config/workspace/IronClaude-RoadmapRewrite branch --show-current` — should be `refactor/roadmap-pipeline-r0-r1-rewrite`. If the worktree is missing, recreate it from origin via `git worktree add /config/workspace/IronClaude-RoadmapRewrite refactor/roadmap-pipeline-r0-r1-rewrite` (the branch exists on origin per PR #112).

**Task file:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` — 42/108 items checked (Phases 1-5 + PGs). Phase 6 = Steps 6.1-6.5 + PG6.1/PG6.2/PG6.3.

**Phase 6 scope (R1.1 — extend contracts SoT):** Per BUILD-REQUEST §R1.1 + §MVR §5 (read `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`):

1. Extend `src/superclaude/contracts/__init__.py` (R0.3 landed `ID_PATTERNS` + `CONVERGENCE_THRESHOLDS` + `GATE_FIELD_NAMES`; R1.1 adds the rest):
   - `RETURN_CONTRACTS` — per-skill return-type schemas (e.g., `AdversarialReturn` dataclass per Vector A §5 example)
   - Full threshold registry — fingerprint min_coverage_ratio, structural-audit threshold, validate convergence thresholds, etc. (reconcile scalars currently scattered across `cli/roadmap/fingerprint.py`, `spec_structural_audit.py`, `gates.py`, `validate_executor.py`)
2. Extend `arch_lint.py` Check 11 to cover the new constants (no module re-defines `RETURN_CONTRACTS` or the new threshold values)
3. Migrate the consumer sites currently holding those scattered scalars to import from `superclaude.contracts`

**Source-of-truth files (read these before starting):**

- BUILD-REQUEST: `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`
- Master retrospective (REWRITE verdict + 5 flaws + recurrence matrix): `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave2-master-report/master-report.md`
- Vector A (MVR spec): `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-A-architecture.md`
- Vector C (Brittleness-Elimination Contract): `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-C-recurrence.md`
- R0 acceptance report: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/reports/r0-acceptance-report.md`
- R0 closure sc:reflect REPORT: `/config/workspace/IronClaude/.dev/reflect/r0-closure-uc2-validation/REPORT.md`

**Outstanding remediations baked into the task file (apply when phases arrive):**

- M1-M7: medium findings carried forward from sc:reflect Tier-2 on the original task file (in task file §"Post-Execution Findings" section)
- M8: ✅ resolved in `665d34ca`
- M9: ✅ resolved in `1c56b50f`
- C1: substrate-leak remediation — applies at Phase 11 (R1.6 cleanup)
- H1: ✅ Step 5.1 corrected (Contract #5 pipeline-blocking, #9 PR-blocking)
- H2: sequencing prerequisite — applies at Phase 10 (R1.5 verify-implementation) → Phase 11 (R1.6 fail-open deletion must precede)
- H3 + H4 + H5: Phase 9 hardening (interim QA checkpoints after Steps 9.5 and 9.10; split Step 9.11 into a-d; build cutover counter)

**Session pacing (carry forward from R0):**

1. Execute ONE phase + its rf-qa gate per launch
2. Then run `/sc:reflect --mode post` on the new commit(s)
3. If sc:reflect surfaces Critical/High: propose fixes, wait for confirmation
4. If only Medium: log to task file medium-tracker, continue
5. Halt for user confirmation before next phase

**CLAUDE.md absolute rules:**

- UV-only Python (`uv run pytest`, `uv pip install` — never bare `pip` / `python -m`)
- Source-of-truth is `src/superclaude/`; never stage `.claude/{skills,commands,agents,hooks,templates}/*` (except `settings.json`); always `make sync-dev` after editing `src/`; `make verify-sync` before commits
- PR target: `IronbellyOrg/IronClaude` ONLY, never upstream `SuperClaude-Org/SuperClaude_Framework`
- PRESERVE invariants (do NOT touch under any circumstance during R1 phases 6-10): `src/superclaude/cli/roadmap/{commands,structural_checkers,convergence,cosmetic_remediator}.py`. Phase 11 (R1.6) MAY touch convergence's gate-wiring point but not its public API.

**Recommended first move:** Run scope discovery (Glob/Grep for current uses of the scalars R1.1 will pull into the registry: fingerprint thresholds, structural-audit thresholds, validate convergence thresholds; AdversarialReturn shape consumers). Then design `RETURN_CONTRACTS` shape, then implement, then test, then rf-qa, then sc:reflect.

**Expected scope:** ~1 eng-week (smallest of R1 phases). 1 commit on `refactor/roadmap-pipeline-r0-r1-rewrite` (parent: `1c56b50f`).

**Status report expected at completion:** commit hash, frontmatter state, items checked, rf-qa verdict, sc:reflect UC-2 verdict, PRESERVE audit, recommendation for Phase 7 entry.

---

## Optional — E2E acceptance tests to run on the R0 branch BEFORE starting Phase 6

If you want operational confidence that R0 actually works end-to-end before extending it:

1. **Re-run the originally failing MultiModelSwarm pipeline command on the R0 branch:**

   ```bash
   cd /config/workspace/IronClaude-RoadmapRewrite
   uv run superclaude roadmap run \
     /config/workspace/IronClaude/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md \
     --output /config/workspace/IronClaude-RoadmapRewrite/.dev/releases/Current/MultiModelSwarm-r0-test
   ```

   Expected: the anti-instinct step PASSES (it FAILED on this exact command at the start of the originating session).

2. **Synthetic spec-drift probe — verify Contract #9 actually fires:**

   Create a spec defining `FR-001..FR-005`, a roadmap claiming `FR-099`, run the pipeline; MERGE_GATE should fail-shut on the phantom ID. Single-command shape:

   ```bash
   cd /config/workspace/IronClaude-RoadmapRewrite
   # Author the synthetic spec + roadmap under .dev/tasks/ad-hoc/contract-9-probe/
   # Then invoke the pipeline; expect "Contract #9: roadmap_ids not in spec_ids" failure string
   ```

3. **Final sc:reflect UC-2 on M9 itself** (`bdfad6d3..1c56b50f`) — Tier-1 standard depth, closes belt-and-suspenders on the R0 chain.
