# MultiModelSwarm — Rollback Procedure (OPS-004 / R-153)

> 📚 Part of the [swarm documentation](./README.md). For day-2 workflows see the
> [operator runbook](./runbook.md) (OPS-001); for the original migration
> sequencing see the [release notes](./release-notes-v1.md) (MIG-004) and its
> "Pre-deletion checklist for legacy shells (MIG-003)" section.
>
> **Status:** Phase 9 / M9 operational-handoff deliverable. Authored under
> tasklist row **T09.05** (Roadmap **R-153** / **OPS-004** / D-0134) for the
> swarm / `sc-bare-review` migration. STRICT tier, critical-path.
>
> **Scope:** how to roll back the M8/M9 thin-caller migration of the
> `sc-bare-review` skill, how to restore the retired legacy shell-dispatch
> scripts from git history if ever needed, and the conditions that TRIGGER a
> rollback.
>
> **Why this doc exists:** untested rollback procedures fail when needed
> (roadmap risk register **R-016**). This document MUST be validated via a
> human-run tabletop rehearsal — see the
> [Tabletop Rehearsal Sign-Off](#tabletop-rehearsal-sign-off) appendix, which is
> deliberately left **PENDING / UNSTAMPED** until an operator runs it.

## What was migrated (the state we may roll back from)

The M8/M9 corrective migration
(`TASK-RF-bare-review-migration-20260616-045915`) made these changes:

- `src/superclaude/skills/sc-bare-review/SKILL.md` became an **80-line thin
  caller** over `superclaude swarm run --lens bare-review` (previously 231
  lines of inline orchestration). Landed by commit `2355bfe1`
  (`feat(sc-bare-review): WS-A thin-caller SKILL.md (231→80) + PG3 gate pass`).
- The legacy shell-dispatch implementation is **being retired** by the M8/M9
  migration. The deletions of the following files are part of this migration's
  WS-C work; once the migration commits land they are removed from the working
  tree:
  - `src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh`
  - `src/superclaude/skills/sc-bare-review/scripts/t2_dispatch.sh`
  - `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
  - `src/superclaude/skills/sc-bare-review/refs/prompts.md`
  - `src/superclaude/skills/sc-bare-review/refs/output-template.md`

**Git reality (important for recovery):** these files were **NOT** deleted by an
earlier commit. They are present **in full** at commit `2355bfe1` — the current
`feat/sc-bare-review-m8m9-migration` HEAD, i.e. the state **before** this M8/M9
migration commits its `git rm` deletions. Their removal is carried by the
migration commit(s) themselves. To recover the legacy path you therefore restore
from `2355bfe1` (the commit just before the deletion lands), not from any
pre-existing commit. The exact migration/deletion SHA is found at recovery time
with `git log --oneline -- src/superclaude/skills/sc-bare-review/scripts/` (the
first commit showing the deletion) — see options A and B below.

## Rollback trigger conditions

Initiate a rollback when ANY of the following holds. These map to the three
rollback scenarios defined for OPS-004 (T09.05 planning step):

| # | Trigger condition | Scenario |
|---|---|---|
| T1 | **Thin-caller regression** — `swarm run --lens bare-review` produces materially different or broken review output vs. the retired shell path; the `bare-review` lens / normalizer mis-shapes the contract; or the 80-line `SKILL.md` caller fails to dispatch. | thin-caller regression |
| T2 | **Detached / orchestrator failure** — detached (tmux) mode fails to launch, dropping jobs, or the swarm CLI itself is unavailable in an environment where the legacy skill path was the only working route. | detached mode failure |
| T3 | **Parity break** — a post-migration discrepancy surfaces that the A/B parity gate (TEST-003 / T08.11) did not catch: e.g. the `bare-review` golden fixtures regress, or normalized output diverges on a real target. | parity break |
| T4 | **Env-contract regression** — the shared T2 proxy env contract (INV-007) behaves differently through the CLI than through the retired scripts in a way that blocks operators. | thin-caller regression |

If none of T1–T4 apply, do NOT roll back — prefer a forward fix on the
thin-caller / lens. Rollback restores deprecated code and re-opens the drift
the migration closed; treat it as a last resort.

## Rollback option A — revert the thin-caller migration (preferred)

This is the cleanest reversal when the regression is in the migration commit
itself and history is otherwise linear. It undoes the thin-caller `SKILL.md`
change AND re-introduces the deleted scripts/refs in one operation, with a new
commit that is auditable and itself revertible.

```bash
# 1. Identify the migration commit(s) that landed the WS-C deletions. The first
#    commit showing the legacy scripts being deleted IS the migration commit.
git log --oneline -- src/superclaude/skills/sc-bare-review/scripts/

# 2. Revert that M8/M9 migration commit (or the squash/merge commit once merged)
#    on branch feat/sc-bare-review-m8m9-migration. This re-introduces the deleted
#    scripts/refs AND undoes the thin-caller SKILL.md change in one inverse commit.
git revert --no-edit <migration-commit-sha>

# 3. Re-materialize the synced mirror from source-of-truth, then verify.
make sync-dev
make verify-sync

# 4. Run the skill / parity tests to confirm the legacy path is healthy again.
uv run pytest tests/swarm/test_bare_review_parity.py -v
```

Notes:

- `<migration-commit-sha>` is the commit (or merge commit, once the branch is
  merged) that lands the WS-C `git rm` deletions — the first entry returned by
  the `git log` in step 1. It is **not** a fixed historical SHA; resolve it live
  at rollback time. As of this writing the legacy files are still present at HEAD
  `2355bfe1`, so the deletion commit is the one that comes *after* it.
- `git revert` is preferred over `git reset` because it preserves history and
  never rewrites published commits on `feat/sc-bare-review-m8m9-migration` or
  `master`.
- If the migration spanned more than one commit, revert them newest-first
  (e.g. `git revert --no-edit <newer-sha> <older-sha>`), or revert a range with
  `git revert --no-edit <oldest>^..<newest>`.
- Per project rules, NEVER `git add` anything under `.claude/`. Edit
  `src/superclaude/` and let `make sync-dev` regenerate the mirror.

## Rollback option B — restore only the legacy scripts/refs from history

Use this surgical path when you want the deprecated shell-dispatch files back in
the working tree WITHOUT reverting the entire migration commit (e.g. to run the
old path side-by-side for a one-off comparison, or to cherry-pick a single
script). It checks the deleted blobs out of `2355bfe1` — the commit just **before**
the deletion lands, where the files are still present byte-for-byte.

```bash
# Restore the three retired scripts + two refs from the commit before the deletion.
# 2355bfe1 is the HEAD-before-deletion anchor (files present in full there).
git checkout 2355bfe1 -- \
  src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh \
  src/superclaude/skills/sc-bare-review/scripts/t2_dispatch.sh \
  src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py \
  src/superclaude/skills/sc-bare-review/refs/prompts.md \
  src/superclaude/skills/sc-bare-review/refs/output-template.md

# Re-sync the mirror and verify source/.claude parity.
make sync-dev
make verify-sync

# Stage + commit only the src/ side (the restored files reappear as adds).
git add src/superclaude/skills/sc-bare-review/scripts/ \
        src/superclaude/skills/sc-bare-review/refs/prompts.md \
        src/superclaude/skills/sc-bare-review/refs/output-template.md
git commit -m "revert(sc-bare-review): restore retired legacy shell-dispatch path"
```

Notes:

- **Robust SHA-agnostic variant** — instead of hardcoding `2355bfe1`, find the
  deletion commit for a single file and restore from its parent:
  `git log --oneline --diff-filter=D -- <path>` returns the commit that deleted
  the file; then `git checkout <that-commit>^ -- <path>` restores it from the
  commit immediately before the deletion. This survives further history movement.
- Confirm the file is present in the source commit before restoring, e.g.
  `git cat-file -t 2355bfe1:src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
  prints `blob` when the file exists there; or list all of them with
  `git ls-tree -r --name-only 2355bfe1 -- src/superclaude/skills/sc-bare-review/`.
- `git checkout <sha> -- <path>` restores the file content AND stages it; the
  explicit `git add` above is belt-and-suspenders for the directory-level add.
- This option leaves the thin-caller `SKILL.md` in place — only use it if the
  caller can still drive the restored scripts. If you ALSO need the 231-line
  `SKILL.md` back, prefer option A (full revert) instead of hand-restoring it.

## Artifact preservation (do this BEFORE any rollback)

Roll back the code, but preserve forensic evidence so the regression can be
diagnosed and a forward fix authored:

- **Do NOT delete** in-flight swarm job artifacts: `.swarm-state.json`,
  `execution-log.jsonl`, `execution-log.md`, and the `done.json` sentinel for
  any affected run. Copy the run's HOME directory aside before reverting.
- Capture the failing `swarm run --lens bare-review` invocation, its exit code,
  and the `return-contract.yaml` it emitted.
- Record which trigger (T1–T4 above) fired, with the concrete observed-vs-expected
  diff, in the incident record. This becomes the input to the post-rollback
  forward-fix task.
- Note the SHAs involved (the M8/M9 migration/deletion commit resolved via
  `git log --oneline -- src/superclaude/skills/sc-bare-review/scripts/`, and the
  restore source `2355bfe1` — the commit just before the deletion) and the exact
  rollback command used.

## After rollback

1. Re-run the parity / golden tests to confirm the restored path is green
   (`uv run pytest tests/swarm/test_bare_review_parity.py -v`).
2. File a forward-fix task to re-attempt the migration with the regression
   addressed; the migration is still the desired end-state (it closes the
   source/`.claude` drift the legacy scripts re-introduce).
3. Update [`release-notes-v1.md`](./release-notes-v1.md) "What changed" /
   MIG-003 sections to reflect that the thin-caller migration was rolled back,
   so the docs do not assert a completed state that no longer holds.

## Tabletop Rehearsal Sign-Off

**PENDING — UNSTAMPED. This appendix MUST be completed by a human operator who
actually runs the rollback tabletop rehearsal (OPS-004 / R-153, T09.05
verification). Do NOT pre-fill, auto-stamp, or fabricate any Date, Rehearser, or
Outcome below.** Per the roadmap risk register (R-016), an untested rollback
procedure is treated as NOT validated until this table is signed by a human who
exercised the steps above against a real (or fixture) swarm job.

| Field | Value |
|---|---|
| Date |  |
| Rehearser |  |
| Scenarios exercised (T1 / T2 / T3 / T4) |  |
| Rollback option exercised (A / B) |  |
| Outcome (PASS / FAIL) |  |
| Lessons learned / doc corrections |  |

> Until the row above is filled in by the human rehearser, the OPS-004 rollback
> deliverable remains **NOT validated**. The tasklist acceptance criterion
> "Rehearsal: completed on `<date>`" stays unsatisfied while this appendix is
> unstamped.
