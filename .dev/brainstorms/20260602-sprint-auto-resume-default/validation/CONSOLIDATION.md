# Adversarial Validation — Consolidation

Date: 2026-06-02 · Target: v4.3.5 (minor upgrade) · Driver: design.md DD-1..DD-5

Five parallel `general-purpose` agents each ran `/sc:adversarial` (Skill sc-adversarial-protocol)
against ONE design decision and wrote a verdict to `DD-N-verdict.md`. Every verdict's *intent*
was upheld; all five returned **REFACTOR** with concrete, code-grounded defects. All proposed
spec changes were applied to `design.md` serially (no concurrent writes).

| DD | Verdict | Conf | Core defect found | Fix applied |
|----|---------|------|-------------------|-------------|
| DD-1 | REFACTOR | 0.82 | Rationale factually wrong: `phase_start` logged AFTER spawn (`executor.py:1335` vs `:1331`); JSONL append non-durable (`logging_.py:265-267`, no fsync/rename) → last line can tear on crash. Latent bug: torn `phase_complete` would re-run a completed non-idempotent phase. | Rewrote DD-1 to anchor on the **atomic** `result.json` (`executor.py:2070-2072`) as authoritative; ledger = corroboration. §3 COMPLETED keys off result.json, not the event. Added concurrency caveat to §12 R2. |
| DD-2 | REFACTOR | 0.82 | Haiku sign-off flipped the gate verdict (contradicts NFR-3); "last-completed task" object absent on single-process path (empty `task_results[]`). | Made Haiku **advisory only** (never changes `passed`), **scoped to `granularity==TASK`**, skipped for PHASE. Added `coherence_warnings` to `BoundaryReport`; CI-safe empty-verdict path. |
| DD-3 | REFACTOR | 0.86 | `.failed-<ts>` rename is inlined in `merge_recovery_bundle` (not reusable), bundle-scoped, NOT reversed by `rerun-tasks --restore`; `sprint resume --restore` is vaporware; gate rename races the rerun engine's own stash. | Switched to **report-only default + opt-in COPY** quarantine reusing the `preserved/`+`manifest.json` shape that existing `restore_from_bundle` reverses. Cover deliverable files (not just transcripts). Acquire `.recovery-locks`. |
| DD-4 | REFACTOR | 0.87 | Tier 0 NOT whitespace-safe (`_content_sha256_excluding_rerun_block` strips only the RERUN block) → AC-4 must be Tier 1; DriftAssessor hashed `index_path` instead of per-phase `phase_obj.file`; stored vs current hash must use the same fn+file (INV-001). | AC-4 moved to Tier 1 (`git diff --ignore-all-space` / normalize-rehash). Pinned hash to `_content_sha256_excluding_rerun_block(phase_obj.file)` on both sides. Tier 1 composes `parse_tasklist` + `extract_checkpoint_paths`. |
| DD-5 | REFACTOR | 0.95 | `position_explicit = (start_phase != 1) or (end_phase != 0)` cannot tell explicit `--start 1` from no flag (`--start` default=1) → silently breaks FR-4.4/AC-7. | Use Click `ctx.get_parameter_source(...) == COMMANDLINE` (add `@click.pass_context` to `run()`), or `None`-sentinel defaults mirroring `rerun-tasks --phase/--tasks`. |

## Net effect on the feature
- **Durability model corrected:** atomic `result.json` is the truth anchor, not the lossy log.
- **No LLM on any gate-verdict path:** all LLM use is advisory; CI runs without `claude` behave identically.
- **Cleanup is now report-only-by-default + reversible copy** — strictly safer, reuses existing restore.
- **Drift detection pinned to the right file + function**, AC-4 correctly located in Tier 1.
- **The flag-bypass bug** (the worst failure mode for a non-idempotent pipeline) is fixed before any code.

Artifacts: `DD-{1..5}-verdict.md` (+ per-agent `DD-N-debate-transcript.md` / `DD-N-pos-*.md` where written).
