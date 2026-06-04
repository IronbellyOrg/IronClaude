# Next-Session Prompt — Phase 8 / R1.3 — `GateCriteria.code_assertions` + First `CodeAssertion` (RESUMPTION)

**Copy-paste the following into a fresh Claude Code session.** Self-contained: references all SoT files by absolute path.

This prompt **resumes mid-phase**: Phase 7 (R1.2 — PipelineEnvelope) is logically done (all items checked, rf-qa PASS, proceed-decision written) but **not yet committed**. Phase 8 Step 8.1 (design) is done; Steps 8.2-8.4 + PG8.1/PG8.2 remain.

---

## Prompt

I'm continuing the roadmap-pipeline brittleness-elimination rewrite. R0 bridge + R1.1 + R1.2 closed logically. Phase 8 (R1.3 — `GateCriteria.code_assertions` slot + first `CodeAssertion` wiring) is in progress; Step 8.1 design is complete, Steps 8.2-8.4 + PG8.1/PG8.2 remain.

**Working branch:** `refactor/roadmap-pipeline-r0-r1-rewrite` in worktree `/config/workspace/IronClaude-RoadmapRewrite/`. Verify with `git -C /config/workspace/IronClaude-RoadmapRewrite branch --show-current` — should be `refactor/roadmap-pipeline-r0-r1-rewrite`, HEAD = `daa10416` (R1.1 — R1.2 work is staged in the working tree but not yet committed). If the worktree is missing, recreate via `git worktree add /config/workspace/IronClaude-RoadmapRewrite refactor/roadmap-pipeline-r0-r1-rewrite`.

**Task file:** `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` — 55/108 items checked (Phases 1-7 + Step 8.1 done; Phases 8 partial, 9-13 + PGs remain).

**Uncommitted R1.2 working-tree state (verify before starting):**

```bash
cd /config/workspace/IronClaude-RoadmapRewrite && git status --short
```

Expected uncommitted files:
- `M src/superclaude/cli/roadmap/executor.py` — wrapper-rename refactor for post-extractor dispatch
- `?? src/superclaude/cli/roadmap/envelope.py` — `PipelineEnvelope` dataclass + 13 post-extractors + dispatch map (~724L)
- `?? tests/roadmap/test_pipeline_envelope.py` — 9 envelope tests (~357L)

These were authored during Phase 7 and have already passed the PG7.1 rf-qa task-integrity gate (PASS verdict at `phase-outputs/reviews/r1-2-rf-qa-task-integrity.md`). The first decision in this session is whether to commit them standalone (recommended — preserves R1.2 / R1.3 atomicity per session-pacing precedent) OR carry them into the Phase 8 commit.

**Phase 8 scope (R1.3 — code-graph predicates in gate contract):** Per BUILD-REQUEST §R1.3 + §MVR §2 + §Contract #2 + master:§Flaw 1:

1. ✅ **Step 8.1 (DONE — do not re-execute):** Design at `phase-outputs/plans/r1-3-codeassertion-design.md`. `CodeAssertion` dataclass shape `(name: str, check_fn: Callable[[PipelineEnvelope, Path], Finding | None], failure_message: str)`. AST walker for dispatch-reachability uses Python's `ast` module. Backward compat via `code_assertions=None` default.
2. **Step 8.2 (next):** Extend `src/superclaude/cli/pipeline/models.py` with `CodeAssertion` dataclass + `GateCriteria.code_assertions: list[CodeAssertion] | None = None` slot. Preserve existing GateCriteria consumers (default None = empty list = no behavior change).
3. **Step 8.3:** Create `src/superclaude/cli/roadmap/code_assertions.py` with `assert_step_reachable(envelope, repo_path) -> Finding | None` (AST walk of `_build_steps`) + `assert_envelope_artifacts_present(envelope, repo_path) -> Finding | None`. Modify `gates.py:CERTIFY_GATE` to include the new code_assertion. Modify `cli/pipeline/gates.py:gate_passed` to iterate `code_assertions` and call their `check_fn(envelope, repo_path)`. Wire `build_certify_step()` into `_build_steps` (resolves master:§Flaw 1 "certify unreached" — may absorb `wiring-verification` since R1.5 `verify-implementation` supersedes it; step-count budget ≤14 per Acceptance gate #6).
4. **Step 8.4:** Create `tests/roadmap/test_dispatch_reachability.py` (Contract #2) with `test_certify_step_reachable`, `test_unwired_step_caught`, `test_all_gates_have_assertions`, `test_codeassertion_signature_invariant`. Run pytest + ruff + format, write summary.
5. **PG8.1:** Aggregate R1.3 outputs, spawn rf-qa task-integrity (adversarial-stance prompt covers backward-compat / AST false PASS / step-count budget / PRESERVE / Contract #5 stubs).
6. **PG8.2:** Act on QA verdict, write proceed-decision for Phase 9 entry.

**Source-of-truth files (read these before starting):**

- BUILD-REQUEST: `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md` (§R1.3 at ~L171, §MVR §2 at L103-115, §Contract #2 at ~L60, Acceptance gate #6 step-count budget)
- Master retrospective (Flaw 1 — `build_certify_step` unreached): `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave2-master-report/master-report.md`
- Vector A (CodeAssertion + GateCriteria invert axes): `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-A-architecture.md`
- R1 file inventory (research/01 §A.1 → `executor.py:build_certify_step` lines 1899-1944; §B → `cli/pipeline/models.py` dataclass conventions L82-105): `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/research/01-file-inventory.md`
- Patterns (research/02 §1.3 → `build_certify_step` unreached today): `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/research/02-patterns-conventions.md`
- **R1.3 design (Step 8.1 — read this FIRST):** `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-codeassertion-design.md`
- R1.2 closure precedent: `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-2-proceed-decision.md` + `/config/workspace/IronClaude-RoadmapRewrite/.dev/reflect/r1-2-uc1-validation/`

**Outstanding remediations baked into the task file (apply when phases arrive):**

- M1-M7: medium findings tracked in `### Phase Findings` sections
- M8, M9: ✅ resolved in R0
- C1: substrate-leak — Phase 11 (R1.6 cleanup)
- H1: ✅ resolved
- H2: sequencing prerequisite — Phase 10 → 11
- H3 + H4 + H5: Phase 9 hardening

**Session pacing (carry forward from R0/R1.1/R1.2):**

1. **First decision:** commit the uncommitted R1.2 work as a standalone commit (recommended — see §Commit-R1.2-first below) OR carry into the Phase 8 commit. Default: commit R1.2 first.
2. **Second move (mandatory if not done):** Check `/config/workspace/IronClaude-RoadmapRewrite/.dev/reflect/` for an existing `r1-3-uc1-*` directory. If none exists, run `/sc:reflect --mode pre --tier 1 --depth standard --tasklist /config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md --spec /config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md --output /config/workspace/IronClaude-RoadmapRewrite/.dev/reflect/r1-3-uc1-validation/` — UC-1 coverage/gap audit for the remaining Phase 8 steps vs §R1.3 + §MVR §2 + §Contract #2. Adjustments fold back into the task file before execution.
3. **Execution:** `/task /config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` — `task` skill processes the remaining 53 unchecked items sequentially via the F1 loop, spawning sub-agents per item. Will pick up at Step 8.2 (8.1 is already marked done).
4. **After commit (post-Phase-8):** `/sc:reflect --mode post --tier 1 --target <commit-hash>` per the R1.1/R1.2 pattern.
5. **Halt for user confirmation before Phase 9 launch.**

### Commit-R1.2-first (recommended approach)

```bash
cd /config/workspace/IronClaude-RoadmapRewrite
git add src/superclaude/cli/roadmap/envelope.py \
        src/superclaude/cli/roadmap/executor.py \
        tests/roadmap/test_pipeline_envelope.py
git commit -m "feat(roadmap/envelope): R1.2 — PipelineEnvelope + 13 post-extractors + dual-write

Per BUILD-REQUEST §R1.2 + §MVR §1 + master:§Flaw 3. Frozen 8-field
PipelineEnvelope dataclass with ConvergenceResult binding (documented
in r1-2-envelope-design.md). 13 named post-extractors + POST_EXTRACTORS
dispatch map + dynamic generate-* prefix resolver. executor wrapper-rename
refactor (_roadmap_run_step_impl + roadmap_run_step wrapper +
_apply_post_step_envelope_update helper). 9 envelope tests + 150/150
regression-guarded tests PASS. ruff clean. PG7.1 rf-qa task-integrity:
PASS (10/10 sub-bullets, 100% confidence, 0 issues at any severity).
PRESERVE invariants (convergence.py, commands.py, structural_checkers.py)
byte-identical to daa10416. Envelope dual-write LIVE for 1 release cycle
before R1.6 markdown-as-substrate cleanup.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

Then proceed to Phase 8 work with the worktree clean and atomic R1.2 / R1.3 commits.

**CLAUDE.md absolute rules:**

- UV-only Python (`uv run pytest`, `uv pip install` — never bare `pip` / `python -m`)
- SoT is `src/superclaude/`; never stage `.claude/{skills,commands,agents,hooks,templates}/*` (except `settings.json`); `make sync-dev` after editing `src/`; `make verify-sync` before commits
- PR target: `IronbellyOrg/IronClaude` ONLY, never upstream `SuperClaude-Org/SuperClaude_Framework`
- **PRESERVE invariants (do NOT touch under any circumstance during R1 Phases 8-10):** `src/superclaude/cli/roadmap/{commands,structural_checkers,convergence,cosmetic_remediator}.py`. Phase 8 may MODIFY `cli/pipeline/models.py` (extending `GateCriteria`) and `cli/pipeline/gates.py` (adding `code_assertions` iteration in `gate_passed`) — these are NOT on the PRESERVE list. The roadmap-side `gates.py` is allowed to be modified to add the new `code_assertions=[...]` field to `CERTIFY_GATE` (this is the §MVR §2 wiring requirement). `executor.py:_build_steps` is allowed to be modified to wire `build_certify_step`. Phase 11 (R1.6) MAY touch convergence's gate-wiring point but not its public API.

**Recommended first move sequence:**

```bash
# 1. Verify worktree state
git -C /config/workspace/IronClaude-RoadmapRewrite status --short

# 2. Commit R1.2 (if uncommitted)
# (use the Commit-R1.2-first block above)

# 3. Run Phase 8 UC-1 pre-execution reflect
/sc:reflect --mode pre --tier 1 --depth standard \
  --tasklist /config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md \
  --spec /config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md \
  --output /config/workspace/IronClaude-RoadmapRewrite/.dev/reflect/r1-3-uc1-validation/

# 4. Execute remaining task items
/task /config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md
```

**Expected scope:** ~1-2 eng-weeks (smaller than R1.2 — adding a slot to an existing dataclass + first CodeAssertion + dispatch wiring; ~200 LOC delta per Vector A). Likely 1-2 commits, parent `<R1.2-commit-hash>` (or `daa10416` if R1.2 is rolled into Phase 8 commit). Target frontmatter state at completion: 61/108 items checked.

**Status report expected at completion:** R1.2 commit hash (if committed standalone), R1.3 commit hash(es), frontmatter state, items checked, rf-qa verdict, sc:reflect UC-2 verdict, PRESERVE audit (`convergence.py` / `commands.py` / `structural_checkers.py` / `cosmetic_remediator.py` all empty-diff vs the appropriate parent), recommendation for Phase 9 entry (R1.4 — tool-write rewrite, the longest sub-phase).

---

## Optional — Verifications before/during Phase 8

1. **Re-run R1.2 sc:reflect UC-2 on the new R1.2 commit** once it lands — converts the original R1.1-era `partial` evidence-validator status to `success` and validates the substrate inversion end-to-end. Not blocking.
2. **Smoke-run the pipeline post-Phase 8 wiring** to confirm `CodeAssertion` fires correctly:
   ```bash
   cd /config/workspace/IronClaude-RoadmapRewrite
   uv run superclaude roadmap run \
     /config/workspace/IronClaude-RoadmapRewrite/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md \
     --output /config/workspace/IronClaude-RoadmapRewrite/.dev/releases/Current/MultiModelSwarm-r1-3-test
   ```
   Expected: pipeline runs to `certify` step (now wired via R1.3), `envelope.json` written, `CERTIFY_GATE` evaluates the new `assert_step_reachable` CodeAssertion successfully.
3. **Synthetic dispatch-unreachability probe** — temporarily delete one entry from `_build_steps`, run `test_unwired_step_caught` from Step 8.4, confirm it surfaces a HIGH Finding. Restore the entry. This is the Contract #2 falsifier eval.
