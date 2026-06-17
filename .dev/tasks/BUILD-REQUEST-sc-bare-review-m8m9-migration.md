# BUILD_REQUEST — Corrective MDTM tasklist: sc-bare-review M8/M9 migration completion

**Origin:** `/sc:task --strategy systematic --compliance strict` (STRICT tier, explicit override)
**Template:** 02 (complex task) — multi-file, sequenced, safety-critical (skill execution-path change + script deletion + parity gate)
**Output task file destination:** `.dev/tasks/to-do/` (standard MDTM location)
**Compliance:** STRICT for execution items touching the skill execution path / script deletion / parity gate; STANDARD for doc authoring; LIGHT for archived-attestation edits.

## Background / why this exists

The MultiModelSwarm post-execution audit (9 parallel `/sc:reflect --mode post` passes) found Phases 1–7 COMPLETE but **Phase 8 (M8 migration) and Phase 9 (OPS handoff / M9 parity) INCOMPLETE** — the sc-bare-review migration theme never shipped, and the phase-8 checkpoints falsely attest it did.

**Authoritative evidence (read these first):**
- `/config/workspace/IronClaude/.dev/reflect/mms-phase-8-postaudit/REPORT.md` (M8 — per-task INCOMPLETE/Drift/Regression table)
- `/config/workspace/IronClaude/.dev/reflect/mms-phase-9-postaudit/REPORT.md` (M9 — OPS docs 0/8, migration §16 steps 8+9 unbuilt)
- `/config/workspace/IronClaude/.dev/reflect/mms-postaudit-SUMMARY.md` (cross-phase summary, "core gap" section)

## VERIFIED current state (2026-06-16 — use these exact facts, do NOT re-derive the wrong paths)

1. **SKILL.md is the legacy orchestrator**, 231 lines, still calls the three scripts:
   `/config/workspace/IronClaude/src/superclaude/skills/sc-bare-review/SKILL.md` (lines 35-36, 89, 113, 127).
2. **The 3 legacy scripts to retire live UNDER THE SKILL DIR, not repo-root `scripts/`:**
   `/config/workspace/IronClaude/src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh`
   `/config/workspace/IronClaude/src/superclaude/skills/sc-bare-review/scripts/t2_dispatch.sh`
   `/config/workspace/IronClaude/src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
   (plus `scripts/__pycache__/`). They are present → the legacy golden baseline CAN be captured before deletion.
3. **The thin-caller target is real and wired:** `superclaude swarm run --lens bare-review` (FR-020 lens shortcut in `src/superclaude/cli/swarm/commands.py:1199-1213`) expands defaults → `bare-review-v1` recipe (`src/superclaude/cli/swarm/recipes/bare_review_v1.py`) + `lenses/bare_review.py` (3 workers, suspect:true, T2, §11.5 guard).
4. **Parity test** `/config/workspace/IronClaude/tests/swarm/test_bare_review_parity.py` is docstring-scoped to "T08.11" and (per audit) compares two LIBRARY surfaces, not the skill/CLI end-to-end; its `skipif(LEGACY_SCRIPT.exists())` currently resolves FALSE (17 passed, not skipped).
5. **docs/swarm/ existing:** command-reference, lens-catalog, monitoring-patterns, oq-resolutions, README, release-notes-v1, runbook, transport-limits, user-guide.
   - `release-notes-v1.md` ALREADY falsely states the skill "is now a ~60-line thin caller" — must be reconciled (true only after WS-A ships).
   - `monitoring-patterns.md` partially overlaps the OPS "observability-procedure"; `runbook.md` partially overlaps "operator-runbook".
6. **`docs/dev/lens-contribution-policy.md` ALREADY EXISTS** (T02.27) — the Phase-9 OPS item that wanted `docs/swarm/lens-contribution-policy.md` is a RELOCATE/REFERENCE, not net-new authoring.
7. **Phase-8 checkpoints to supersede:** `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-cp1.md` and `phase-8-cp2.md` (cp1 claims "SKILL.md 59 lines"→disk 231; cp2 claims "scripts removed / parity 17 SKIPPED"→disk present / 17 PASSED). NOTE: `complete/` is currently git-untracked.
8. **Sync discipline (MANDATORY):** any edit under `src/superclaude/skills/sc-bare-review/` triggers the pre-commit hook `scripts/precommit_verify_bare_review_sync.sh` (MIG-001) requiring src↔`.claude/` mirror parity → the tasklist MUST include `make sync-dev` + `make verify-sync` after the SKILL.md rewrite, and MUST NOT stage `.claude/` directly.

## Required work-streams (build MDTM items covering all five, with explicit sequencing)

**WS-A (STRICT) — Rewrite SKILL.md as ~60-line thin caller.** Replace the 231-line script orchestrator with a thin caller that invokes `superclaude swarm run --lens bare-review --target … --output … [--reviewers N --transport openai_compat --target-line-cap N --timeout-sec N --label …]` and relays the return contract. Preserve the caller-facing option surface. AC: ≤80 lines; no `scripts/t2_*` references; `make sync-dev` + `make verify-sync` green; MIG-001 mirror hook passes.

**WS-B (STRICT) — Rebuild parity test as end-to-end CLI-vs-legacy A/B gate.** DESIGN CONSTRAINT: a live "legacy" side disappears once WS-C deletes the scripts. So: (1) capture a FROZEN legacy golden baseline by running the legacy scripts on a fixed fixture target BEFORE deletion; (2) rebuild `tests/swarm/test_bare_review_parity.py` to drive `superclaude swarm run --lens bare-review` (CLI subprocess) and assert output parity against the frozen golden; (3) rescope docstring off "T08.11" to the M8/M9 migration; (4) replace the `skipif(LEGACY_SCRIPT.exists())` guard with a post-deletion-valid gate. AC: gate exercises the CLI subprocess (not library composition); deterministic; green against the new thin caller.

**WS-C (STRICT, depends on WS-A + WS-B green) — Retire the 3 legacy scripts** at `src/superclaude/skills/sc-bare-review/scripts/{t2_preflight.sh,t2_dispatch.sh,t2_normalize.py}` (+ `__pycache__`). ONLY after parity holds. AC: scripts gone; SKILL.md has no references; full swarm suite green; `make verify-sync` green.

**WS-D (STANDARD) — Author the missing Phase-9 OPS docs under `docs/swarm/`.** Reconcile against existing files:
  - `operator-runbook.md` (extend/supersede existing `runbook.md` — decide one canonical, no duplication)
  - `env-readiness.md` + `swarm_env_readiness.sh` (env preflight script — decide its home; non-Anthropic, T2 proxy env per .aienv contract)
  - `observability-procedure.md` (extend/reference existing `monitoring-patterns.md`)
  - `rollback-procedure.md` + a tabletop-rehearsal record (STRICT critical-path item per Phase-9 T09.05)
  - `lens-contribution-policy.md` — RECONCILE existing `docs/dev/lens-contribution-policy.md` (relocate to docs/swarm/ or cross-reference; do NOT duplicate)
  - `post-release-metrics.md`
  Also fix `docs/swarm/release-notes-v1.md` so it no longer claims the thin caller shipped before WS-A lands (or sequence the note to land with WS-A).

**WS-E (LIGHT) — Supersede the false phase-8 cp1/cp2 attestations.** Add a correction/superseded notice to `.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-cp{1,2}.md` recording that the migration claims were false at attestation time and pointing to this corrective tasklist + the post-audit REPORTs. (Archived, untracked record — LIGHT.)

## Sequencing / dependencies
WS-A → WS-B (needs thin caller to test; capture legacy golden while scripts still exist) → (parity green) → WS-C. WS-D and WS-E are independent and can run in parallel. WS-E should reference the completed WS-A/C outcomes.

## Global constraints (bake into every relevant item)
- UV for all Python (`uv run …`); never bare `python`/`pip`.
- Source-of-truth: edit `src/superclaude/…` then `make sync-dev`; NEVER stage `.claude/` (gitignored except settings.json).
- No Anthropic SDK in swarm transports; T2 proxy env per `~/.aienv` only.
- Each STRICT item: spawn quality-engineer verification; run `uv run pytest tests/swarm/ -v`; TFEP applies on pre-existing-test regressions.
- Note (out of scope, do not fold in): a pre-existing ruff F401 set (127) across the swarm module makes `make lint` red independently — do not let it mask new failures; gate on `uv run pytest` + targeted ruff on touched files only.

## Acceptance for the tasklist itself
Per-item: id, compliance tier, dependencies, concrete file paths (use the VERIFIED paths above), acceptance criteria, verification command. Include a final exit-gate item asserting: SKILL.md ≤80 lines & script-free, scripts deleted, parity gate green end-to-end CLI, 6 OPS docs reconciled/present, cp1/cp2 superseded, `make verify-sync` green, full swarm suite green.
