# Next-Session Prompt — Phase 7 / R1.2 — `PipelineEnvelope` + Sidecar JSON + Dual-Write Migration

**Copy-paste the following into a fresh Claude Code session.** Self-contained: references all SoT files by absolute path.

---

## Prompt

I'm continuing the roadmap-pipeline brittleness-elimination rewrite. R0 bridge + R1.1 closed clean. Phase 7 (R1.2 — `PipelineEnvelope` dataclass + sidecar JSON + dual-write migration) is next.

**Working branch:** `refactor/roadmap-pipeline-r0-r1-rewrite` in worktree `/config/workspace/IronClaude-RoadmapRewrite/`. Verify with `git -C /config/workspace/IronClaude-RoadmapRewrite branch --show-current` — should be `refactor/roadmap-pipeline-r0-r1-rewrite`, HEAD = `daa10416` (R1.1). If the worktree is missing, recreate via `git worktree add /config/workspace/IronClaude-RoadmapRewrite refactor/roadmap-pipeline-r0-r1-rewrite`.

**Task file:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` — 48/108 items checked (Phases 1-6 + PGs). Phase 7 = Steps 7.1-7.4 + PG7.1/PG7.2.

**Phase 7 scope (R1.2 — PipelineEnvelope substrate inversion):** Per BUILD-REQUEST §R1.2 + §MVR §1 + master:§Flaw 3:

1. Design `PipelineEnvelope` dataclass shape per §MVR §1 (`release_id`, `spec_hash`, `spec_ids`, `artifacts`, `findings`, `counts`, `convergence`, `accepted_deviations`) + sidecar JSON layout (`<release>/envelope.json`). Write design doc to `phase-outputs/plans/r1-2-envelope-design.md`.
2. Implement `src/superclaude/cli/roadmap/envelope.py` — frozen dataclass + supporting `ArtifactRef`/`AcceptedDeviation` dataclasses + atomic `load_envelope`/`save_envelope` helpers. **Invariant:** "LLM never writes gate-pass counts directly" (master:§Flaw 3 substrate-inversion). `ConvergenceState` MUST be imported from `convergence.py` (PRESERVE — do NOT redefine).
3. Implement per-step Python post-extractors for all 14 `_build_steps` entries — each extractor parses the step's markdown artifact deterministically (using `spec_parser` helpers, **no new parsers** per Contract #6), updates the envelope additively. Add `POST_EXTRACTORS` dispatch map. Wire dispatch into `executor.roadmap_run_step` at L955 — dual-write phase: markdown still written AND envelope additively updated.
4. Absorb R0.1's `spec_id_registry.json` into `envelope.spec_ids`. Mark `spec_id_registry.json` as R1.6-deletion-point in a TODO.
5. Tests: `tests/roadmap/test_pipeline_envelope.py` — round-trip equality, atomic write safety, dispatch-map completeness, dual-write markdown preservation.

**Source-of-truth files (read these before starting):**

- BUILD-REQUEST: `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md` (§R1.2 at L170, §MVR §1 at L84-101)
- Master retrospective (Flaw 3 — markdown-as-substrate failure modes): `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave2-master-report/master-report.md`
- Vector A (envelope effort envelope ~600 LOC): `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-A-architecture.md`
- R1 file inventory (research/01 §A.8 → `models.py:RoadmapConfig` at L93; §B → `cli/pipeline/models.py` dataclass conventions): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/research/01-file-inventory.md`
- Patterns (research/02 §1.1 → the 12 steps in `_build_steps`): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/research/02-patterns-conventions.md`
- R1.1 closure artifacts (precedent for Phase 7's adversarial gate structure): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-1-proceed-decision.md` + `/config/workspace/IronClaude/.dev/reflect/r1-1-uc2-validation/REPORT.md`

**Outstanding remediations baked into the task file (apply when phases arrive):**

- M1-M7: medium findings from sc:reflect Tier-2 on the original task file (in §Phase 6 - R1.1 Contracts Extension Findings already + §Post-Execution Findings section)
- M8: ✅ resolved in `665d34ca`
- M9: ✅ resolved in `1c56b50f`
- C1: substrate-leak remediation — applies at Phase 11 (R1.6 cleanup)
- H1: ✅ Step 5.1 corrected (Contract #5 pipeline-blocking, #9 PR-blocking)
- H2: sequencing prerequisite — applies at Phase 10 (R1.5 verify-implementation) → Phase 11 (R1.6 fail-open deletion must precede)
- H3 + H4 + H5: Phase 9 hardening (interim QA checkpoints + Step 9.11 split + build cutover counter)

**Session pacing (carry forward from R0/R1.1):**

1. **First move (mandatory):** `/sc:reflect --mode pre` on the Phase 7 portion of the tasklist vs BUILD-REQUEST §R1.2 + §MVR §1 — coverage/gap audit before token spend on execution. If a UC-1 pre-execution reflect has already been run for Phase 7, skip this step (check `/config/workspace/IronClaude/.dev/reflect/` for any `r1-2-uc1-*` or `phase-7-uc1-*` directory).
2. **Execution:** `/task /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` — the `task` skill processes Phase 7 checklist items sequentially via the F1 execution loop, spawning sub-agents per item as needed, tracking progress via frontmatter + task log.
3. **After commit:** `/sc:reflect --mode post --tier 1 --target <commit-hash>` on the new commit(s) per the same pattern as R1.1 closure. If sc:reflect surfaces Critical/High, propose fixes and wait for confirmation. If only Medium, log to task file medium-tracker and continue.
4. **Halt for user confirmation before Phase 8 launch.**

**CLAUDE.md absolute rules:**

- UV-only Python (`uv run pytest`, `uv pip install` — never bare `pip` / `python -m`)
- SoT is `src/superclaude/`; never stage `.claude/{skills,commands,agents,hooks,templates}/*` (except `settings.json`); `make sync-dev` after editing `src/`; `make verify-sync` before commits
- PR target: `IronbellyOrg/IronClaude` ONLY, never upstream `SuperClaude-Org/SuperClaude_Framework`
- **PRESERVE invariants (do NOT touch under any circumstance during R1 Phases 7-10):** `src/superclaude/cli/roadmap/{commands,structural_checkers,convergence,cosmetic_remediator}.py`. Phase 7 reads `convergence.py` (for `ConvergenceState`/`RunMetadata`/`ConvergenceResult` types) but MUST NOT modify it. Phase 11 (R1.6) MAY touch convergence's gate-wiring point but not its public API.

**Recommended first move:** Run `/sc:reflect --mode pre --tier 1 --depth standard --tasklist /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md --spec /config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md --output /config/workspace/IronClaude/.dev/reflect/r1-2-uc1-validation/` — scopes the audit to Phase 7's section (Steps 7.1-7.4 + PG7.1-7.2) against §R1.2 + §MVR §1 coverage. Then `/task <task-file-path>` to execute.

**Expected scope:** ~2-3 eng-weeks (largest of R0/R1.1/R1.2 — Vector A estimates ~600 LOC new + ~150 LOC deletions for duplicate frontmatter parsers; 14 post-extractors stage-by-stage). Likely 2-4 commits on `refactor/roadmap-pipeline-r0-r1-rewrite` (parent: `daa10416`).

**Status report expected at completion:** commit hashes, frontmatter state, items checked (target 54/108 after Phase 7 + PG closure), rf-qa verdict, sc:reflect UC-2 verdict, PRESERVE audit (`convergence.py` / `commands.py` / `structural_checkers.py` / `cosmetic_remediator.py` all empty-diff), recommendation for Phase 8 entry.

---

## Optional — Verifications before/during Phase 7

1. **Verify R1.1 sc:reflect status is `success` (not `partial`) on a fresh run** — the R1.1 UC-2 verdict shipped as `partial` because the evidence-validator agent hit a transient 503. Re-running `/sc:reflect --mode post --tier 1 --target daa10416 --output /config/workspace/IronClaude/.dev/reflect/r1-1-uc2-validation-rerun/` when the gateway is healthy will convert it to `success`. Not blocking for Phase 7.
2. **Smoke-run the pipeline post-Phase 7 dual-write** to confirm `envelope.json` and the existing markdown output are both produced without divergence:
   ```
   cd /config/workspace/IronClaude-RoadmapRewrite
   uv run superclaude roadmap run \
     /config/workspace/IronClaude/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md \
     --output /config/workspace/IronClaude-RoadmapRewrite/.dev/releases/Current/MultiModelSwarm-r1-2-test
   ```
   Expected: `envelope.json` written; markdown artifacts unchanged byte-for-byte vs an R1.1-era run on the same input.
