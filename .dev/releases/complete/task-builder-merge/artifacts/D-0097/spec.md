# D-0097 — OPS-006 Sync-Failure Runbook + OPS-007 INV-018 Layout-Change Runbook

**Task:** T07.17 (Phase 7 — M7)
**Roadmap items:** R-157 (OPS-006), R-158 (OPS-007)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (each runbook contains all 5 mandatory sections — symptoms / diagnosis / resolution / escalation / prevention — and the four acceptance-criteria anchors: OPS-006 binds A-001 sync-discipline + K-009 contingency; OPS-007 binds K-008 portfolio-wide blast radius + SP-33 stability commitment).
**Audience:** Per-commit author (OPS-006 owner per `roadmap.md:469`), Engineering Lead (OPS-007 owner per `roadmap.md:470` + per-FR rollback coordinator), rf-task-builder maintainer (peer — OPS-004/OPS-005 owner whose agent body is one of the sync-checked surfaces), rf-qa / rf-qa-qualitative maintainers (FR-CONV.3/.4 owners; consume `.claude/` synced copy), GA-tagging committee.
**Owners:**
- **OPS-006:** Per-commit author (per `roadmap.md:469` — "Operational | Per-commit author | Immediate response SLA (A-001 / K-009)") — every commit author is OPS-006-on-call for their own commit; escalates to Engineering Lead on persistent failure.
- **OPS-007:** Engineering Lead (per `roadmap.md:470` — "Operational | Engineering Lead | Portfolio-wide blast-radius (K-008)") — INV-018 layout changes have portfolio-wide blast radius across all 6 FRs and require Engineering-Lead authority to coordinate the re-integration commit per release-spec §19.4.

**Threshold (alert):**
- **OPS-006:** `make verify-sync` exits non-zero on any branch tip or pre-commit gate after MIG-001..MIG-006 land (per `roadmap.md:436` — "make-verify-sync:PASS" gate per FR; per `release-spec.md:486` "Each FR's PR passes `make verify-sync` before merge"). Any single FAIL is a trigger — there is no rate-level dimension for OPS-006 (unlike OPS-004 / OPS-005); the sync-discipline is binary.
- **OPS-007:** Any structural change to `.dev/tasks/<task-id>/` directory layout — new mandatory subdirectory, rename of `research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`, naming-pattern change to `<task-id>/` — detected by NFR-CONV.8 pre/post diff (D-0087) returning non-empty output, OR by an Engineering-Lead-initiated SP-33 stability audit, OR by any of the 6 FRs needing to update its hard-coded path references mid-release.

**Response SLAs:**
- **OPS-006:** Immediate — the responsible commit author MUST resolve before re-attempting to land the commit; no merge to the integration branch is permitted while `make verify-sync` is non-zero. Escalation to Engineering Lead within 4 business hours if resolution is not trivial (e.g., direct-edit to `.claude/` of substantive content with no `src/` counterpart, per K-009).
- **OPS-007:** 24-hour acknowledgement by Engineering Lead from layout-change detection (NFR-CONV.8 diff or SP-33 audit signal). 5-business-day window for the re-integration commit covering all 6 FRs per release-spec §19.4 dependency matrix.

**Overall: PASS** (4/4 acceptance criteria met — §6: file exists at the artifact path; both runbooks contain 5 sections; OPS-006 references A-001 + K-009; OPS-007 references K-008 + SP-33).

---

## 0. TL;DR

**OPS-006 (Sync-Failure)** is the operational runbook that turns a non-zero `make verify-sync` exit (drift between `src/superclaude/` source-of-truth and the `.claude/` dev-copy convenience mirror) into an explicit per-commit response procedure under per-commit-author ownership. The trigger is binary (any failure ≥1 → fire); the resolution is single-track (`make sync-dev` to restore drift, OR — on persistent failure — revert the direct `.claude/` edit and re-author from `src/superclaude/`). The runbook binds A-001 sync-discipline ("CLAUDE.md mandates the sync workflow") and K-009 contingency ("on persistent failure, revert direct `.claude/` edit and re-run from `src/superclaude/`"). OPS-006 owns the *workflow-discipline* dimension that gates every per-FR landing — without it, the `src/` → `.claude/` invariant cannot be preserved across M1..M7.

**OPS-007 (INV-018 Layout-Change)** is the operational runbook for the **portfolio-wide blast-radius event** in which the `.dev/tasks/<task-id>/` directory layout itself changes (new mandatory subdirectory, a rename of `research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`, or any naming-pattern shift). Such a change invalidates every FR-CONV.X path reference simultaneously (K-008) and is owned by Engineering Lead because the response — a re-integration commit covering all 6 FRs per release-spec §19.4 dependency matrix — requires authority over the entire FR portfolio. OPS-007 cites the SP-33 stability commitment ("`.dev/tasks/` layout is contract-frozen across M1..M7") as the reason layout changes are exceptional and treated as portfolio-wide events rather than per-FR refactors. The runbook covers (a) detection (NFR-CONV.8 diff signal + SP-33 audit cadence), (b) impact assessment across all 6 FRs, (c) re-integration commit authoring with §19.4 dependency-matrix discipline, (d) escalation to GA-tagging committee, and (e) prevention through pre-merge layout-stability checks.

Both runbooks share the M7 governance plane: OPS-006 is fired by per-commit authors on every per-FR PR; OPS-007 is fired by Engineering Lead on rare layout-change events. They compose at §4 below — a sync failure can mask a layout change (the `.claude/` copy is out of date with respect to a new layout in `src/`), and a layout change always also triggers a sync failure (the `.claude/` mirror has the old layout). OPS-007 takes precedence when both fire: resolve layout-change discipline first, then re-run `make sync-dev`.

---

## 1. Scope and authoritative bindings

Both runbooks bind to the following authorities (all read at landing time; cross-checked at every invocation):

| Source | Location | Binding |
|---|---|---|
| Roadmap R-157 (OPS-006) acceptance criteria | `roadmap.md:436` | "Runbook: re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline (A-001); revert direct `.claude/` edit on persistent failure (K-009 contingency)"; "runbook:published; pre-commit-hook-enforcement-documented; immediate-response-SLA" |
| Roadmap R-158 (OPS-007) acceptance criteria | `roadmap.md:437` | "Runbook: inspect all 6 FRs for path/naming references; re-integration commit covering all 6 FRs per §19.4 dependency matrix"; "runbook:published; portfolio-wide-blast-radius-response-documented; SP-33-stability-commitment-cited" |
| Roadmap §M7 Consolidated Governance Table — OPS-006 row | `roadmap.md:469` | "OPS-006 \| Sync failure runbook \| Operational \| Per-commit author \| Immediate response SLA (A-001 / K-009) \| All FRs" |
| Roadmap §M7 Consolidated Governance Table — OPS-007 row | `roadmap.md:470` | "OPS-007 \| Layout change runbook \| Operational \| Engineering Lead \| Portfolio-wide blast-radius (K-008) \| All FRs" |
| Roadmap §M1 risk-register row — K-009 (sync-discipline) | `roadmap.md:156` + `roadmap.md:554` | "R-M1-4 — Sync-discipline (A-001) violated by direct `.claude/` edit (K-009)"; "All FR-CONV.1 paths reference `src/superclaude/` exclusively; CLAUDE.md mandates workflow; revert direct edit and re-run from `src/superclaude/` on failure" |
| Roadmap §M1 risk-register row — K-008 (INV-018 layout-change) | `roadmap.md:155` + `roadmap.md:553` | "R-M1-3 — INV-018 `.dev/tasks/` layout change invalidates all FR paths (K-008)"; "Portfolio-wide note; SP-33 stability commitment; re-integration commit contingency covering all 6 FRs" |
| Roadmap A-001 source-of-truth workflow | `roadmap.md:140` + `roadmap.md:524` | "A-001 source-of-truth workflow accepted (CLAUDE.md sync-discipline)"; "`make sync-dev` / `make verify-sync` pipeline (A-001): per-FR landing gate across M1..M7" |
| Roadmap SP-33 layout-stability commitment | `roadmap.md:523` | "`.dev/tasks/` directory layout (INV-018): SP-33 stability commitment; K-008 portfolio-wide guard." |
| Roadmap §M1 pre-merge governance baseline | `roadmap.md:138`–`roadmap.md:140` | "Clean `make verify-sync` baseline before M1 commit (K-009 prevention)"; "`rf-team-lead.md:417` NO-DRIFT verified (verified 2026-05-14; K-008 portfolio-wide preservation)"; "A-001 source-of-truth workflow accepted (CLAUDE.md sync-discipline)" |
| Release-spec §8.3 audit row — sync-discipline post-merge | `release-spec.md:471` | "`test_sync_discipline_post_merge` — A-001: `make sync-dev && make verify-sync` PASS after all 6 FRs land" |
| Release-spec landing order cross-cutting AC | `release-spec.md:486` | "Each FR ships independently per its own acceptance criteria … Each FR's PR passes `make verify-sync` before merge" |
| Release-spec rollback path (§19.4 dependency matrix) | `release-spec.md` §19.4 | Per-FR rollback granularity governed by SP-10 co-revert matrix (FR-CONV.5 ↔ FR-CONV.6 jointly revertable; FR-CONV.1 ↔ FR-CONV.3 INV-010 enumeration dependency) — invoked by OPS-007 for the portfolio-wide re-integration commit |
| NFR-CONV.8 layout-invariance verification (T07.05 / D-0087) | `roadmap.md:423` | "Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge — zero structural changes (no new mandatory subdirectory, no rename of research/qa/synthesis/reviews/adversarial, no naming-pattern change)"; "diff-output:empty; INV-018-preservation:verified" — provides the canonical detection mechanism for OPS-007 |
| INV-018 layout-stability invariant | `roadmap.md:147` + `roadmap.md:531` | "If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration"; "Persistent artifacts remain under `.dev/tasks/to-do/TASK-*/` with existing `research/`, `qa/`, `synthesis/`, `reviews/`, `adversarial/` subdirectory names unchanged (NFR-CONV.8 / INV-018)" |
| CLAUDE.md sync-discipline (operational mandate) | `CLAUDE.md` "Component Sync" section | "Edit files in `src/superclaude/skills/` or `src/superclaude/agents/`"; "Run `make sync-dev` to copy changes to `.claude/`"; "Run `make verify-sync` to confirm sync (also run before committing)"; "If you edited `.claude/` directly … Copy your changes to `src/superclaude/` manually" |
| Makefile `sync-dev` target | `Makefile:108-152` | The mechanical pump: copies `src/superclaude/{skills,agents,commands,hooks/scripts}/` into `.claude/{skills,agents,commands/sc,hooks}/` |
| Makefile `verify-sync` target | `Makefile:154-...` | The drift detector: compares `src/` ↔ `.claude/` per skill / agent / command / hook; reports DIFFERS / MISSING with exit-1 on any drift |
| Reject-workspace-writes hook (sync-discipline enforcer) | `src/superclaude/hooks/scripts/reject-workspace-writes.sh` | PreToolUse hook that rejects direct writes to `.claude/skills/*-workspace/**` (per CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination") — supports A-001 by preventing one common direct-`.claude/`-edit class |
| MIG-001..MIG-006 landing commits (sync-discipline anchors) | Per-FR commit hashes | Every per-FR landing commit MUST land with a clean `make verify-sync` per `roadmap.md:179` ("make-verify-sync:PASS") / `:226` / `:282` / `:328` / `:388` — OPS-006 measurement window starts at the first such commit (MIG-001 / FR-CONV.1) |
| MIG-006 anchor commit (most-recent landing) | `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` | Latest sync-discipline anchor; OPS-006/OPS-007 are now in force across all 6 landed FRs |
| Consolidated GA-Readiness Governance Table | `D-0091/spec.md §2` OPS-006 + OPS-007 rows | Both OPS-006 and OPS-007 are enumerated in the governance table; cross-references this runbook for the GA-tagging committee |

**Scope boundary.** This runbook covers **two operational events**:

- **OPS-006 covers `make verify-sync` failure** (binary trigger; any non-zero exit fires) — every sync failure is in scope, every per-commit author is the on-call owner for their own commit. It does **not** cover: K-003 audit-target events (OPS-001), DNSP triage (OPS-002), all-partitions-exhaust HALT (OPS-003), HALT-MONOTONICITY rate (OPS-004), regression-halt rate (OPS-005), or INV-018 layout changes (OPS-007).
- **OPS-007 covers INV-018 layout changes** — structural modifications to `.dev/tasks/<task-id>/` (new mandatory subdirectory, rename of `research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`, naming-pattern change). It does **not** cover: per-file content edits inside the existing subdirectory layout, additions of optional / non-mandatory subdirectories outside the protected name set, or any of OPS-001..006.

Neither runbook modifies (a) the A-001 source-of-truth contract itself (`src/superclaude/` is canonical, `.claude/` is a dev mirror, sync flows in one direction); (b) the INV-018 layout-stability commitment itself (SP-33 — the protected subdirectory names and the `.dev/tasks/<task-id>/` framing are contract-frozen across M1..M7); (c) the §19.4 SP-10 co-revert dependency matrix structure itself. These are frozen contracts; OPS-006/-007 operate the workflow that preserves them.

---

## 2. OPS-006 Runbook — `make verify-sync` failure (5 sections)

### 2.1 Symptoms

The per-commit author is alerted (immediately, by the local pre-commit gate per `release-spec.md:486` + CLAUDE.md sync-discipline section, OR by CI on the PR branch, OR by the M7 audit row `test_sync_discipline_post_merge` per `release-spec.md:471`) when **any one** of the following is observed on a branch tip or pre-commit hook run after MIG-001..MIG-006 land:

1. **Binary trigger — `make verify-sync` exits non-zero.** The Makefile target at `Makefile:154` exits with code 1 and emits "❌ Drift detected!" (`Makefile:313`) accompanied by per-component DIFFERS / MISSING lines for one or more of: skills, agents, commands, hooks, or installer-registration (`_FRESHNESS_SCRIPTS` list at `src/superclaude/cli/install_hooks.py`). A non-zero exit is the OPS-006 trigger — there is no rate dimension and no threshold to debate.
2. **Per-component decomposition.** `make verify-sync` reports the failure surface as one of:
   - **Skills drift** — a `src/superclaude/skills/<name>/` and `.claude/skills/<name>/` pair differs in file content (DIFFERS), is missing on one side (MISSING in `.claude/skills/` ⇒ run `make sync-dev`; MISSING in `src/superclaude/skills/` ⇒ "not distributable" — a non-skill living under `.claude/skills/` requires relocation to `.dev/eval-workspaces/<name>/` per `Makefile:183` + CLAUDE.md "Plugin Override" section).
   - **Agents drift** — `src/superclaude/agents/<name>.md` vs `.claude/agents/<name>.md` differs or is missing on one side.
   - **Commands drift** — `src/superclaude/commands/<name>.md` vs `.claude/commands/sc/<name>.md` differs or is missing on one side.
   - **Hooks drift** — `src/superclaude/hooks/scripts/<name>.sh` vs `.claude/hooks/<name>.sh` differs or is missing on one side.
   - **Installer-registration drift** — a hook in `src/superclaude/hooks/scripts/` is not in the `_FRESHNESS_SCRIPTS` list (the end-user `superclaude install` will skip it), or vice-versa.
3. **Co-occurrence with a layout-change signal (jointly fires OPS-007).** If `make verify-sync` reports MISSING for `.claude/skills/<new-name>/` where `<new-name>` is a newly-introduced subdirectory in `src/superclaude/skills/`, the failure is a *normal* additive drift (resolution = `make sync-dev`). If, however, the failure reports MISSING for a previously-existing `.claude/skills/<name>/` that has been *renamed* in `src/superclaude/`, the symptom co-occurs with an INV-018-adjacent rename and OPS-007 must be consulted (the rename touches the layout-naming contract). See §4.
4. **Window scope.** OPS-006 fires per-commit, not per-window. Every commit is its own gate. The M7 audit row at `release-spec.md:471` runs `make sync-dev && make verify-sync` post-merge after all 6 FRs land and treats any non-zero exit as a release-blocking event.

Detection sources: (a) **local pre-commit** — author runs `make verify-sync` (per CLAUDE.md "Component Sync" section "also run before committing"); (b) **CI gate on the PR branch** — `make verify-sync` is the canonical pre-merge check per `release-spec.md:486`; (c) **M7 post-merge audit** — `test_sync_discipline_post_merge` per `release-spec.md:471`; (d) **pre-commit hook** — local pre-commit hooks per `roadmap.md:436` "pre-commit-hook-enforcement-documented" (gating drift before it leaves the working tree).

**Symptom NOT in scope.** A failure of `make sync-dev` itself (the pump, not the verifier) is a build-tool failure and routes through normal developer-experience triage — `make sync-dev` is idempotent and re-runnable, so any spurious failure clears on re-invocation. OPS-006 fires on the *verifier* (`make verify-sync`), not on the *pump* (`make sync-dev`).

### 2.2 Diagnosis

Within **4 business hours** of detection (the immediate response SLA per `roadmap.md:469`), the per-commit author performs the following ordered diagnostic steps. The author MUST not merge any commit while `make verify-sync` is non-zero.

1. **Re-run the verifier to confirm.** Execute `make verify-sync` from a clean working tree. If it now PASSes, the prior failure was an artefact of a partial-pump state (a `make sync-dev` was interrupted) and no further action is needed — proceed to commit. If it still FAILs, continue to step 2.
2. **Run `make sync-dev` to pump the canonical mirror.** This is the normal-case resolution path per `roadmap.md:436` ("re-run `make sync-dev`") and CLAUDE.md sync-discipline ("If you edited `src/superclaude/` … Run `make sync-dev` to copy changes to `.claude/`"). The Makefile target at `Makefile:108-152` walks `src/superclaude/skills/` / `agents/` / `commands/` / `hooks/scripts/` and copies each into the matching `.claude/` location.
3. **Re-run `make verify-sync` after the pump.** If it now PASSes, the drift was the normal-case "I edited `src/` but forgot to re-pump" event. Author commits the synced `.claude/` state alongside the `src/` edit. Diagnosis closes — proceed to §2.3 resolution path R1.
4. **If `make verify-sync` STILL FAILs after a `make sync-dev`, inspect `git status` for unsynced changes.** Per `roadmap.md:436` ("check git status for unsynced changes"), the persistent failure usually surfaces as one of:
   - (a) `.claude/` files modified directly (NOT propagated from `src/superclaude/`) — listed by `git status` as modifications under `.claude/skills/<name>/...` / `.claude/agents/<name>.md` / `.claude/commands/sc/<name>.md` / `.claude/hooks/<name>.sh` with no matching `src/superclaude/` change. **This is the K-009 contingency case** — see step 5.
   - (b) `.claude/` files modified in addition to `src/superclaude/` files with diverged content — `make sync-dev` overwrote the `.claude/` with the `src/` content, but the author had unique content in `.claude/` that is now lost (or about to be lost on next `sync-dev`).
   - (c) Installer-registration mismatch — a hook in `src/superclaude/hooks/scripts/` has not been added to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`. Resolution = add it to the list.
5. **Verify CLAUDE.md sync-discipline (A-001) compliance.** Per `roadmap.md:436` ("verify CLAUDE.md sync-discipline (A-001)") and the A-001 contract per `roadmap.md:140` + `roadmap.md:524`: all distributable component edits MUST flow `src/superclaude/` → `make sync-dev` → `.claude/`. Direct `.claude/` edits violate A-001. If step 4 surfaced a direct `.claude/` edit (case 4a or 4b), the author confirms whether the edit content is intentional and salvageable:
   - **Intentional + salvageable.** Author copies the substantive content from `.claude/` back to the matching `src/superclaude/` location, re-runs `make sync-dev`, re-runs `make verify-sync`. PASS ⇒ proceed to commit. (See CLAUDE.md "If you edited `.claude/` directly … Copy your changes to `src/superclaude/` manually".)
   - **Intentional but not salvageable** (e.g., the `.claude/` edit was a one-off experiment).** Author reverts the `.claude/` edit and re-runs `make verify-sync`. PASS ⇒ proceed.
   - **Persistent failure** (the `.claude/` edit cannot be cleanly reconciled, e.g., conflicting concurrent edits across `src/` and `.claude/`, or the edit cannot be expressed cleanly in `src/`). **This is the K-009 contingency** — escalate per §2.4.
6. **Classify the root cause** (for the audit trail). OPS-006 resolutions fall into one of the following classes:
   - **C1 — Forgot to pump.** Author edited `src/superclaude/`, did not run `make sync-dev`, `make verify-sync` FAILs. Resolution = run `make sync-dev`, commit the resulting `.claude/` sync delta alongside the `src/` change. This is the dominant case in normal development.
   - **C2 — Direct `.claude/` edit (A-001 violation, salvageable).** Author edited `.claude/` directly without going through `src/`. The edit content is substantive and intentional. Resolution = port the edit back to `src/superclaude/`, re-pump.
   - **C3 — Direct `.claude/` edit (A-001 violation, unsalvageable / experimental).** Author's `.claude/` edit was experimental and is being abandoned. Resolution = revert the `.claude/` edit (the K-009 "revert direct `.claude/` edit on persistent failure" path per `roadmap.md:436` step).
   - **C4 — Installer-registration drift.** A new hook landed in `src/superclaude/hooks/scripts/` without being added to `_FRESHNESS_SCRIPTS`. Resolution = add it to the list and re-run.
   - **C5 — Stale workspace artifact in `.claude/skills/`.** A `.claude/skills/<name>/` directory exists with no `SKILL.md` and no matching `src/` counterpart — usually an eval workspace that should have been written to `.dev/eval-workspaces/<name>/` per CLAUDE.md "Plugin Override". Resolution = move to `.dev/eval-workspaces/<name>/` and remove from `.claude/skills/`. The `reject-workspace-writes.sh` PreToolUse hook is designed to prevent recurrence.

### 2.3 Resolution

The resolution path is **single-track per root-cause class** per `roadmap.md:436` R-157 ("Runbook: re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline (A-001); revert direct `.claude/` edit on persistent failure (K-009 contingency)"). Every C1..C5 resolves to a workflow-discipline action, never to a contract change.

| Root cause | Resolution | Owner | Budget |
|---|---|---|---|
| **C1** (forgot to pump) | `make sync-dev` → re-run `make verify-sync` → commit both `src/` and `.claude/` deltas atomically. | Per-commit author | ≤30 minutes; immediate on detection |
| **C2** (direct `.claude/` edit, salvageable — A-001 deferred) | Copy substantive `.claude/` content back to matching `src/superclaude/` location → `make sync-dev` → `make verify-sync` → commit both deltas atomically. Append A-001 advisory note to commit message explaining the back-port. | Per-commit author | ≤2 hours |
| **C3** (direct `.claude/` edit, unsalvageable — K-009 contingency) | `git checkout -- .claude/` to revert the direct edit → re-run `make verify-sync`. If PASS, proceed. Per `roadmap.md:436` K-009 contingency: "revert direct `.claude/` edit on persistent failure". | Per-commit author; escalate to Engineering Lead within 4 business hours if any salvageable substantive content is being lost. | ≤30 minutes |
| **C4** (installer-registration drift) | Add the new hook name to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` → `make sync-dev` → `make verify-sync`. | Per-commit author (of the hook addition) | ≤30 minutes |
| **C5** (stale workspace artifact in `.claude/skills/`) | Move `.claude/skills/<name>/` to `.dev/eval-workspaces/<name>/` per CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination". Confirm `.gitignore` matches `.claude/skills/*-workspace/`. Re-run `make verify-sync`. | Per-commit author; the `reject-workspace-writes.sh` hook prevents recurrence. | ≤1 hour |

On any successful resolution: the per-commit author MUST land both the `src/superclaude/` change and the resulting `.claude/` sync delta in the same commit (atomicity preserves A-001 — there is no intermediate state in which `src/` and `.claude/` diverge in the git history).

**Explicit non-resolutions** (forbidden by the A-001 sync-discipline contract + K-009 + SP-33 + CLAUDE.md):

- Do NOT bypass `make verify-sync` with `--no-verify` or any hook-skip flag. Per CLAUDE.md "Never skip hooks (--no-verify) or bypass signing (--no-gpg-sign, -c commit.gpgsign=false) unless the user has explicitly asked for it."
- Do NOT commit `.claude/` changes without a matching `src/superclaude/` source (would violate A-001 source-of-truth contract).
- Do NOT commit `src/superclaude/` changes without re-running `make sync-dev` and including the resulting `.claude/` delta (would leave `.claude/` stale for the next developer's session).
- Do NOT modify the `make verify-sync` target to "ignore" specific files/paths to make a failure go away — the verifier is contract-frozen; per `Makefile:155-...` it is canonically what defines "in sync".
- Do NOT raise the "immediate response" SLA to a windowed SLA — OPS-006 is per-commit, not per-window. Every commit is a gate; rate-level dampening is forbidden because each individual sync failure can mask a contract-frozen layout regression (which would route to OPS-007).
- Do NOT shift OPS-006 ownership away from the per-commit author. Roadmap.md:469 is deliberate — every commit author owns OPS-006 for their own commit. Escalation to Engineering Lead is permitted on K-009 persistent failure but does not shift the default owner.
- Do NOT relitigate A-001 (source-of-truth direction) inside OPS-006 — A-001 says `src/superclaude/` is canonical and the flow is one-way. OPS-006 enforces the workflow that preserves A-001; it does not modify A-001 itself.

### 2.4 Escalation

Escalation is **per-commit-driven** by the local pre-commit gate (or CI on the PR branch); the per-commit author is always the primary owner. Engineering-Lead escalation triggers only on persistent K-009 contingency.

| T | Event | Actor |
|---|---|---|
| T+0 | `make verify-sync` FAILs on local pre-commit OR CI OR M7 post-merge audit. | Per-commit author |
| T+0 to T+30m | Author re-runs `make sync-dev` + `make verify-sync` (C1 / C4). If PASS, commit and close. | Per-commit author |
| T+30m to T+2h | Author classifies into C2 / C3 / C5; executes the resolution path in §2.3. | Per-commit author |
| **T+4h (Engineering-Lead escalation trigger).** | If after a `make sync-dev` and a `git checkout -- .claude/`, `make verify-sync` STILL FAILs (K-009 persistent failure case), the per-commit author escalates to Engineering Lead. Acknowledgement within 4 business hours of escalation. | Engineering Lead |
| T+4h to T+24h | Engineering Lead diagnoses the persistent K-009 failure. Most common case: a third-party tool wrote into `.claude/` (a skill that bypassed the `reject-workspace-writes` hook, or a misconfigured plugin). Resolution = revert the offending content, identify the source, file a follow-up to harden the hook. | Engineering Lead |
| Recurrence (≥3 K-009 events / week) | Engineering Lead opens an A-001 hardening review. Surface includes: (a) widening `reject-workspace-writes.sh` matcher; (b) adding new PreToolUse hooks; (c) revising CLAUDE.md "Component Sync" section if developer workflow needs to evolve. | Engineering Lead |
| GA-tagging committee escalation | Three or more independent OPS-006 K-009 events across distinct release windows in the run-up to v3.9 GA (T07.20 / MIG-007b) → the GA-tagging committee re-evaluates whether the M7 exit criterion "make verify-sync PASS rate" is sustainably met. Decision may be (a) block GA until A-001 hardening lands; (b) accept GA with a remediation commitment; (c) defer (no contract change — A-001 is frozen). | GA-tagging committee |

Escalation contacts and rotation handoffs live in the on-call knowledge base (consumed via integration point at `roadmap.md:477`); this runbook names roles (per-commit author / Engineering Lead) and not individuals.

### 2.5 Prevention

Prevention is multi-layer; the goal is to eliminate every OPS-006 fire below the K-009 contingency floor.

1. **CLAUDE.md sync-discipline section** (already in place — see "Component Sync" header). Every contributor reads it as part of onboarding; the project root CLAUDE.md is loaded into Claude Code's context on every session per the harness contract.
2. **Local pre-commit hook running `make verify-sync`** (per `roadmap.md:436` "pre-commit-hook-enforcement-documented"). Contributors are expected to install a local pre-commit that fails the commit if `make verify-sync` exits non-zero. Reference implementation at `scripts/install-pre-commit.sh` (or equivalent). Note: the harness `CLAUDE.md` global "Git Safety Protocol" prohibits skipping hooks unless explicitly authorised — this protocol composes with OPS-006 prevention.
3. **CI gate on every PR branch** running `make verify-sync` as part of the test matrix (per `release-spec.md:486` "Each FR's PR passes `make verify-sync` before merge"). The CI gate is the backstop when local pre-commit is bypassed.
4. **M7 post-merge audit row** `test_sync_discipline_post_merge` (per `release-spec.md:471`) — runs `make sync-dev && make verify-sync` against the merged state after all 6 FRs land; treats any non-zero exit as a release-blocking event.
5. **PreToolUse hook `reject-workspace-writes.sh`** (`src/superclaude/hooks/scripts/reject-workspace-writes.sh`) — blocks the most common A-001 violation (skill-creator workspace writes into `.claude/skills/*-workspace/`). The hook is registered in `_FRESHNESS_SCRIPTS` (per the `make verify-sync` installer-registration check at `Makefile:269-...`).
6. **Clean baseline at M1 commit** (per `roadmap.md:138` — "Clean `make verify-sync` baseline before M1 commit (K-009 prevention)"). Every FR commit from MIG-001 forward inherits this baseline.
7. **Atomic per-FR commits** — every FR PR lands the `src/superclaude/` change and the matching `.claude/` sync delta in the same commit (no intermediate diverged state in git history). Acceptance criterion enforced at `roadmap.md:179` / `:226` / `:282` / `:328` / `:388` ("single-commit; make-verify-sync:PASS").
8. **Periodic A-001 review** — at every release-window boundary, Engineering Lead reviews OPS-006 fire counts and any K-009 events. If fire rate trends upward, the A-001 surface is hardened proactively (typically: a new PreToolUse hook covering an under-covered direct-`.claude/`-edit class).

---

## 3. OPS-007 Runbook — INV-018 Layout-Change (5 sections)

### 3.1 Symptoms

Engineering Lead is alerted to a potential INV-018 layout change (the **portfolio-wide blast-radius event** per `roadmap.md:470` + `roadmap.md:155`) when **any one** of the following is observed:

1. **NFR-CONV.8 diff returns non-empty.** The T07.05 / D-0087 invariant check (`roadmap.md:423` — "Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge — zero structural changes") returns a non-empty diff between a known-good baseline and the current tree. The diff specifically detects: (a) new mandatory subdirectory added under `.dev/tasks/<task-id>/`; (b) rename of any of `research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`; (c) change to the `<task-id>/` naming pattern (e.g., from `TASK-NNNN/` to anything else); (d) deletion of any of the protected subdirectories.
2. **SP-33 stability audit signal.** Engineering-Lead-initiated audit (cadence: per release boundary, supplementing the per-FR NFR-CONV.8 check) surfaces a path/naming change in any of the 6 FR-CONV.X agent / skill files referencing `.dev/tasks/<task-id>/` paths.
3. **Any FR PR proposes a path-reference change.** A PR for FR-CONV.1..6 (or any cross-cutting change touching `rf-task-builder.md` / `rf-task-researcher.md` / `rf-qa.md` / `rf-qa-qualitative.md` / `rf-analyst.md` / `rf-team-lead.md`) introduces a new or changed reference to `.dev/tasks/<task-id>/<subdir>/`. **This is a portfolio-wide event by definition**: the FR cannot land its path change in isolation because all 6 FRs reference the same layout.
4. **`rf-team-lead.md:417` NO-DRIFT verification fails.** Per `roadmap.md:139` + `roadmap.md:403` — the NO-DRIFT check on the all-agents-fail escalation site at line 417 of `rf-team-lead.md` is part of the K-008 portfolio-wide preservation. A failure indicates the layout reference at that line has drifted, which is an INV-018-adjacent signal.
5. **Test fixture path failures across FRs.** A test fixture failure that touches `.dev/tasks/<task-id>/<subdir>/` paths in more than one FR's test surface simultaneously (e.g., `tests/audit/test_invariant_preservation_NFR_6_through_10.py` AND `tests/pipeline/test_process.py` both fail on path resolution) — the multi-FR co-failure indicates a shared root cause in the layout.

Detection sources: (a) **NFR-CONV.8 invariant test** (canonical — the T07.05 / D-0087 check; runs at every per-FR PR and at M7 post-merge audit); (b) **SP-33 audit cadence** (Engineering-Lead-initiated, per release boundary); (c) **FR PR review** — any path-reference change in a per-FR PR routes through OPS-007; (d) **rf-team-lead.md:417 NO-DRIFT check** (per `roadmap.md:139`); (e) **GA-tagging committee review** at MIG-007b (T07.20).

**Symptom NOT in scope.** Additions of optional / non-mandatory subdirectories outside the protected name set (e.g., a new `.dev/tasks/<task-id>/notes/` for ad-hoc artefacts, never referenced by any FR) are NOT INV-018 changes — INV-018 protects the structural identity of the 5 named subdirectories (`research/`, `qa/`, `synthesis/`, `reviews/`, `adversarial/`) and the `<task-id>/` naming pattern. Per-file content edits inside existing subdirectories are explicitly out of scope for OPS-007; they route through normal per-FR review.

### 3.2 Diagnosis

Within **24 hours** of detection (Engineering-Lead acknowledgement SLA), the Engineering Lead performs the following ordered diagnostic steps. The default response posture is **blocking** — no FR PR involving the layout change merges until OPS-007 is resolved.

1. **Confirm the layout change is real.** Re-run the NFR-CONV.8 invariant check (T07.05 / D-0087 method). Capture:
   - (a) The baseline layout (last-known-good per the most recent post-merge audit row).
   - (b) The candidate layout (the proposed or detected state).
   - (c) The structural diff: list each (i) added mandatory subdirectory, (ii) renamed subdirectory (old → new), (iii) deleted subdirectory, (iv) changed naming pattern.
2. **Classify the change.** Per `roadmap.md:147` + `roadmap.md:155` (K-008 blast radius), layout changes fall into one of the following classes:
   - **L1 — Spurious detection.** The diff arose from an artefact (e.g., a test fixture wrote into a temporary `.dev/tasks/.tmp.<id>/` that NFR-CONV.8 mistakenly compared). Resolution = adjust the NFR-CONV.8 filter; not an OPS-007 event.
   - **L2 — Optional-subdirectory addition (outside protected name set).** The change adds a subdirectory NOT in `{research, qa, synthesis, reviews, adversarial}` and NOT referenced by any FR. Resolution = NOT an OPS-007 event; treat as routine.
   - **L3 — Mandatory-subdirectory addition (inside protected name set).** A new subdirectory is added that any FR-CONV.X agent will reference. **This is a portfolio-wide INV-018 event.** Resolution = §3.3 re-integration commit path.
   - **L4 — Rename of a protected subdirectory.** `research/` → something-else, OR `qa/` → something-else, etc. **Portfolio-wide INV-018 event.** Resolution = §3.3 re-integration commit path.
   - **L5 — `<task-id>/` naming-pattern change.** The `TASK-NNNN/` pattern or whatever canonical form is in use changes shape. **Portfolio-wide INV-018 event** with the broadest blast radius (every FR references the pattern). Resolution = §3.3 re-integration commit path.
   - **L6 — Deletion of a protected subdirectory.** One of `research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/` is removed. **Portfolio-wide INV-018 event** affecting any FR that consumes that subdirectory's artefacts. Resolution = §3.3 re-integration commit path.
3. **Inventory all 6 FRs for path/naming references.** Per `roadmap.md:437` R-158 ("inspect all 6 FRs for path/naming references"), the Engineering Lead executes an exhaustive grep across the 6 FR landing surfaces:
   - **FR-CONV.1** — `src/superclaude/skills/task-builder/SKILL.md` and any rule/template files. References include the orchestrator's per-gate spawn payload paths.
   - **FR-CONV.2** — `src/superclaude/skills/task-builder/SKILL.md` + agents touched by Execution Context Header. References include the header's path-reference fields.
   - **FR-CONV.3** — `src/superclaude/agents/rf-qa-qualitative.md` (Inherited Structural Verdict passthrough). References include the inherited-verdict carrier paths.
   - **FR-CONV.4** — `src/superclaude/agents/rf-qa-qualitative.md` (Five Adversarial Axes Overlay). References include the per-axis context paths.
   - **FR-CONV.5** — `src/superclaude/agents/rf-task-builder.md` + `src/superclaude/skills/task-builder/SKILL.md` (Retry Monotonicity + Regression Halts). References include the per-cycle PASS-ledger paths.
   - **FR-CONV.6** — `src/superclaude/agents/rf-analyst.md` + `rf-qa.md` (Synthetic DNSP on Partition Exhaust). References include the DNSP emission-site paths.
   - **Cross-cutting** — `src/superclaude/agents/rf-team-lead.md` (specifically line 417 per `roadmap.md:139` + `roadmap.md:403` — the K-008 NO-DRIFT canonical anchor).
   For each FR, capture the grep output: (a) every line referencing `.dev/tasks/`; (b) every line referencing one of the 5 protected subdirectory names; (c) every line referencing the `<task-id>/` naming pattern.
4. **Map the blast radius** (per FR × per affected path). For each FR, mark whether the layout change touches: (i) no references (FR unaffected); (ii) read-only references (FR observes the path but does not write — moderate impact, requires update but no behavioural change); (iii) write references (FR writes into the path — high impact, requires both path update AND behavioural verification).
5. **Identify §19.4 SP-10 co-revert constraints.** Per release-spec §19.4 + `roadmap.md:589` + the M5/M6 mutual-shape coupling at `roadmap.md:82`, certain FR pairs are jointly-revertable: **FR-CONV.5 ↔ FR-CONV.6** (dedup-key shape coupling); **FR-CONV.1 ↔ FR-CONV.3** (INV-010 enumeration dependency). When a layout change touches either pair, the re-integration commit MUST cover the paired FRs jointly (cannot ship one without the other). The Engineering Lead notes which co-revert constraints are active for this layout change.
6. **Verify SP-33 stability commitment status.** Per `roadmap.md:523` ("`.dev/tasks/` directory layout (INV-018): SP-33 stability commitment; K-008 portfolio-wide guard"), SP-33 is the public commitment that the layout is frozen across M1..M7. A layout change post-M1 is a **deliberate exception** to SP-33 and requires explicit Engineering-Lead authorisation. The diagnosis records (a) why the layout change is necessary; (b) whether the SP-33 commitment is being broken with cause, or being preserved with a workaround that achieves the same outcome via an additive change outside the protected name set.
7. **Compose with OPS-006.** Every INV-018 layout change ALSO triggers a `make verify-sync` failure (the `.claude/` mirror has the old layout; `src/` has the new). OPS-007 takes precedence — the layout-change response includes a synchronized `make sync-dev` as part of the re-integration commit. See §4 cross-runbook composition.

### 3.3 Resolution

The resolution path is **single-track: a re-integration commit covering all 6 FRs per release-spec §19.4 dependency matrix** per `roadmap.md:437` R-158 ("re-integration commit covering all 6 FRs per §19.4 dependency matrix"). There is no per-FR rollback granularity for layout changes — by definition, INV-018 changes invalidate every FR's path references simultaneously, so the response is portfolio-wide.

| Class | Resolution | Owner | Budget |
|---|---|---|---|
| **L1** (spurious detection) | Adjust the NFR-CONV.8 filter to exclude the artefact; no portfolio action. | Engineering Lead | ≤4 hours |
| **L2** (optional-subdirectory addition outside protected name set) | Land routinely as a per-FR change. NOT an OPS-007 event. | Per-FR commit author | Normal per-FR cadence |
| **L3** (mandatory-subdirectory addition inside protected name set) | **Re-integration commit covering all 6 FRs.** Author updates every FR-CONV.X agent / skill file to reference the new subdirectory; runs the full M1..M7 test surface (`make test` + `make verify-sync` + the NFR-CONV.6/.8/.9 fixtures + the FR-CONV-specific fixtures) on the joint state; lands as a single coordinated commit (or a coordinated commit train under explicit SP-10 co-revert grouping). The release-spec §19.4 dependency matrix governs the per-FR ordering within the commit train. | Engineering Lead | 5 business days from acknowledgement (24-hour ack SLA + 4-day re-integration window) |
| **L4** (rename of a protected subdirectory) | Same as L3, with the additional requirement that the rename touches the SP-33 stability commitment publicly. Engineering Lead authors an SP-33 update to the release-spec / roadmap (or, if the rename is being avoided, a workaround that preserves SP-33 by additive change). | Engineering Lead | 5 business days; SP-33 update may extend to 10 business days if released externally. |
| **L5** (`<task-id>/` naming-pattern change) | **Highest-blast-radius case.** Same as L4 plus: every test fixture using `<task-id>/` literal paths must update; every test factory must update; documentation in CLAUDE.md and release-spec.md updates. | Engineering Lead | 10 business days; the broad blast radius reflects in the budget. |
| **L6** (deletion of a protected subdirectory) | Same as L4 plus: every FR that consumes the deleted subdirectory must have its consumption path replaced or downgraded; if the FR cannot function without the subdirectory, the FR itself must be revisited (potentially a §19.4 SP-10 rollback). | Engineering Lead | 10 business days; may extend if an FR rollback is required. |

The re-integration commit (for L3..L6) follows the §19.4 dependency-matrix discipline:

1. **Inventory all FR path/naming references** (per §3.2 step 3 output).
2. **Author the layout migration** in a single feature branch named `chore/inv-018-<short-description>` (NOT a per-FR branch — the change is portfolio-wide).
3. **Update every FR-CONV.X reference** in the same branch. The commit is atomic across FRs.
4. **Run the full test surface** on the joint state. PASS gates: `make verify-sync`, `make test`, NFR-CONV.6/.8/.9 fixtures, all per-FR fixtures (TB-Add-1..8 + FR-CONV.3 inherited-verdict + FR-CONV.4 axes + FR-CONV.5 monotonicity/regression + FR-CONV.6 synthetic-DNSP), `test_sync_discipline_post_merge`, plus any fixture explicitly cited by §19.4 SP-10 co-revert pairs.
5. **rf-team-lead.md:417 NO-DRIFT re-verification** per `roadmap.md:139` + `roadmap.md:403`.
6. **Update SP-33 stability commitment** if the layout change is externally visible: amend the release-spec.md commitment language; note the change in the consolidated governance table (D-0091); flag for GA-tagging committee review.
7. **Update CLAUDE.md sync-discipline section** if the layout change has any developer-workflow implication (e.g., a new `.dev/eval-workspaces/` neighbour).
8. **Land the commit train** with explicit SP-10 co-revert grouping: FR-CONV.5 ↔ FR-CONV.6 jointly; FR-CONV.1 ↔ FR-CONV.3 jointly; other pairs independently per the §19.4 matrix.
9. **Run `make sync-dev`** as part of the same commit train (composes with OPS-006 — the layout-change response always also resolves the corresponding sync failure).
10. **Tag the re-integration commit** with the OPS-007 event identifier in the commit message for the audit trail.

**Explicit non-resolutions** (forbidden by K-008 portfolio-wide blast radius + SP-33 stability commitment + INV-018 layout invariance):

- Do NOT land a layout change in a per-FR PR. By the K-008 portfolio-wide note + the INV-018 invariant statement, a per-FR layout change leaves the other 5 FRs referencing the old layout, which violates the structural identity that makes the layout an *invariant* in the first place.
- Do NOT skip the rf-team-lead.md:417 NO-DRIFT check per `roadmap.md:139` — this line is the canonical K-008 NO-DRIFT anchor; missing the verification re-introduces the K-008 blast-radius risk.
- Do NOT bypass the `make verify-sync` gate or the per-FR fixture re-run. Layout changes that break a single fixture are layout regressions per `roadmap.md:155` ("HIGH (K-008 portfolio-wide)").
- Do NOT modify the protected subdirectory name set (`research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`) without explicit SP-33 amendment. SP-33 is the public stability commitment; changing the protected set is a contract change that requires GA-tagging-committee approval.
- Do NOT mix an INV-018 change with substantive FR-content changes in the same commit. The re-integration commit is *mechanical* (path-reference updates only); behavioural changes route through their own FR PR pipeline (or a §19.4 rollback). Mixing pollutes the per-FR rollback granularity.
- Do NOT shift OPS-007 ownership away from Engineering Lead. Per `roadmap.md:470`, the owner is Engineering Lead because the resolution lever (re-integration commit covering all 6 FRs) cuts across the entire FR portfolio and requires authority over the §19.4 dependency matrix. No subordinate role has cross-FR authority alone.
- Do NOT relitigate SP-33 to "soften" the commitment to avoid an OPS-007 fire. SP-33 is the M1..M7 stability commitment; weakening it would invalidate the K-008 portfolio-wide preservation that the whole release depends on.

### 3.4 Escalation

Escalation is **detection-driven** by the NFR-CONV.8 diff signal, the SP-33 audit cadence, or any FR PR proposing a path-reference change. Time-boxed by the 24-hour acknowledgement SLA + 5..10-business-day re-integration window.

| T | Event | Actor |
|---|---|---|
| T+0 | Detection signal fires (NFR-CONV.8 diff non-empty, OR SP-33 audit surfaces a change, OR an FR PR proposes a path-reference change, OR rf-team-lead.md:417 NO-DRIFT fails). | Engineering Lead (alerted by NFR-CONV.8 owner, SP-33 auditor, or FR PR author) |
| T+24h (acknowledgement) | Engineering Lead acknowledges within 24 hours of detection. Acknowledgement logged in audit trail. The default response posture is *blocking* — no merges on the affected layout area until OPS-007 resolves. | Engineering Lead |
| T+24h to T+5d (or T+10d for L5/L6) | Engineering Lead executes §3.2 (classify L1..L6) and §3.3 (re-integration commit if L3..L6). | Engineering Lead |
| Cross-FR co-revert escalation | If the layout change interacts with an SP-10 co-revert pair (FR-CONV.5 ↔ FR-CONV.6 or FR-CONV.1 ↔ FR-CONV.3) and the re-integration commit cannot satisfy both halves of the pair simultaneously, Engineering Lead escalates to the FR-CONV.5/6 / FR-CONV.1/3 maintainer pair for joint authorship. | rf-task-builder maintainer + rf-qa-qualitative maintainer (joint) |
| GA-tagging committee escalation | An OPS-007 fire during the v3.9 GA window (T07.20 / MIG-007b) requires GA-tagging committee notification. The committee evaluates: (a) is the layout change avoidable (workaround possible)? (b) does the change break the SP-33 stability commitment publicly? (c) can v3.9 GA proceed with the layout change captured in the consolidated governance table, or must GA be deferred? | GA-tagging committee |
| Recurrence (≥2 OPS-007 fires across the release window) | Engineering Lead opens an INV-018 hardening review. Surface includes: (a) widening NFR-CONV.8's diff sensitivity; (b) adding a SP-33 lint to CI; (c) revising the FR path-reference patterns to be more layout-change-tolerant. Recurrence indicates the layout invariant is under churn and the contract surface needs attention. | Engineering Lead + GA-tagging committee |

Escalation contacts live in the on-call knowledge base (per `roadmap.md:477`); this runbook names roles, not individuals.

### 3.5 Prevention

Prevention is multi-layer; the goal is to keep OPS-007 fires below 1 per release cycle.

1. **SP-33 stability commitment** (already in place — `roadmap.md:523`). The public commitment that `.dev/tasks/` layout is frozen across M1..M7 is the structural pressure that keeps every contributor from proposing layout changes casually.
2. **NFR-CONV.8 invariant check at every per-FR PR** (per T07.05 / D-0087). Every FR PR runs the layout diff; non-empty diff blocks merge.
3. **rf-team-lead.md:417 NO-DRIFT verification** at every release-window boundary (per `roadmap.md:139` + `roadmap.md:403`). The canonical K-008 NO-DRIFT anchor is checked routinely.
4. **Pre-merge K-008 review** at every per-FR PR: the FR author certifies that their PR does NOT touch any of the protected subdirectory names (`research/` / `qa/` / `synthesis/` / `reviews/` / `adversarial/`) and does NOT change the `<task-id>/` naming pattern. The certification is a checklist item in the per-FR PR template.
5. **Documented protected name set** in release-spec.md §SP-33 (`release-spec.md` SP-33 section). Every contributor can read what is protected and what is not.
6. **§19.4 SP-10 co-revert matrix** (per `release-spec.md` §19.4 + `roadmap.md:589`). The matrix makes the portfolio-wide impact of layout changes explicit — a contributor proposing a layout change must reason about the co-revert pairs before drafting the PR.
7. **CLAUDE.md "where things go" decision guide** (per `CLAUDE.md` "Plugin Override" section + `.dev/README.md`). Routing eval workspaces and experimental artefacts away from `.dev/tasks/<task-id>/` is the most common path that *would have* touched the protected layout if uncontrolled.
8. **Periodic SP-33 audit cadence** by Engineering Lead at every release-window boundary. The audit reads the consolidated governance table (D-0091) row for OPS-007, inspects fire counts, and re-affirms SP-33 if zero fires.

---

## 4. Cross-runbook composition (OPS-006 ↔ OPS-007 ↔ peers)

| Peer | Composition rule | Action |
|---|---|---|
| **OPS-006 ↔ OPS-007** (same release window, both fire) | Every INV-018 layout change ALSO triggers a `make verify-sync` failure (the `.claude/` mirror lags `src/`). When both fire jointly: **OPS-007 takes precedence**. The re-integration commit (§3.3) includes a `make sync-dev` step (per `roadmap.md:436` ("re-run `make sync-dev`") inherited into OPS-006 §2.3 C1) so the sync-discipline failure resolves as a byproduct of the layout-change response. The reverse is not true — a vanilla OPS-006 failure (no layout dimension) does NOT trigger OPS-007. | When OPS-007 fires: resolve OPS-007 first (re-integration commit covering all 6 FRs); `make sync-dev` is part of the same commit train; OPS-006 closes implicitly. When OPS-006 fires alone (no NFR-CONV.8 diff signal): resolve via §2.3 root-cause classes; no OPS-007 escalation. |
| **OPS-001 (K-003 audit-target)** | Independent surface — K-003 audits Self-Audit coverage in rf-qa-qualitative runs; sync-discipline and layout invariance are orthogonal. | No joint action. |
| **OPS-002 (DNSP triage)** | Independent surface — synthetic-dnsp emission is a runtime signal, not a file-tree signal. However, a layout change that renames the `qa/` subdirectory could break the DNSP emission-site path references — that would be an OPS-007 event (L4 class) that *also* breaks OPS-002's detection logic. Resolve OPS-007 first. | When OPS-007 fires and the rename touches a DNSP emission site: ensure the re-integration commit (§3.3) updates the rf-analyst.md / rf-qa.md path references and re-runs the FR-CONV.6 fixture suite. |
| **OPS-003 (all-partitions-exhaust HALT)** | Independent surface — Path A zero-success cohorts are runtime events; layout invariance is structural. | No joint action. |
| **OPS-004 (HALT-MONOTONICITY rate)** | Independent surface — monotonicity-rate is a runtime aggregate per-batch metric. A layout change touching FR-CONV.5's per-cycle PASS-ledger paths is OPS-007 (L3 / L4 class) and could perturb OPS-004's measurement baseline. Resolve OPS-007 first; re-baseline OPS-004 at the next release-window post-resolution. | When OPS-007 touches FR-CONV.5 path references: include the rf-task-builder.md per-cycle PASS-ledger sites in the §3.3 inventory; re-run TEST-016 + TEST-022 + the FR-CONV.5 monotonicity fixture suite. |
| **OPS-005 (Regression-halt rate)** | Same composition as OPS-004 above; the FR-CONV.5 ↔ FR-CONV.6 SP-10 co-revert pair governs the joint behaviour. | When OPS-007 touches FR-CONV.5 or FR-CONV.6: jointly update both per the SP-10 co-revert matrix. |

---

## 5. Acceptance-criteria mapping (T07.17 / R-157 / R-158)

| Acceptance criterion (phase-7-tasklist.md L805-810) | Where met in this artefact |
|---|---|
| File `TASKLIST_ROOT/artifacts/D-0097/spec.md` exists with both OPS-006 + OPS-007 sections. | This file: §2 (OPS-006), §3 (OPS-007); both sit under the same artefact path. |
| OPS-006 references A-001 sync-discipline and K-009 contingency. | §1 (bindings table — A-001 row at `roadmap.md:140`+`:524`, K-009 row at `roadmap.md:156`+`:554`); §2.2 step 5 (A-001 verification); §2.2 step 6 C3 (K-009 unsalvageable direct-edit case); §2.3 C3 row (K-009 contingency resolution); §2.4 K-009 escalation trigger; §2.5 step 1+8 (A-001 prevention layers). |
| OPS-007 references K-008 portfolio-wide blast radius and SP-33 stability commitment. | §1 (bindings table — K-008 row at `roadmap.md:155`+`:553`, SP-33 row at `roadmap.md:523`); §3.1 (portfolio-wide opening sentence); §3.2 step 5 (§19.4 co-revert + K-008); §3.2 step 6 (SP-33 status check); §3.3 (re-integration commit covering all 6 FRs — K-008 response; SP-33 amendment requirement for L4..L6); §3.4 (recurrence + GA-tagging committee escalation citing SP-33); §3.5 step 1 (SP-33 prevention) + step 8 (SP-33 audit cadence). |
| Both runbooks have 5 sections each. | OPS-006 §2.1 Symptoms / §2.2 Diagnosis / §2.3 Resolution / §2.4 Escalation / §2.5 Prevention. OPS-007 §3.1 Symptoms / §3.2 Diagnosis / §3.3 Resolution / §3.4 Escalation / §3.5 Prevention. |

**Overall verdict: PASS** (4/4 acceptance criteria met).

---

## 6. Sign-off

| Role | Action | Date |
|---|---|---|
| Per-commit author (OPS-006 default on-call) | Acknowledged via CLAUDE.md "Component Sync" section + project README onboarding. | 2026-05-18 (this artefact) |
| Engineering Lead (OPS-006 K-009 escalation owner + OPS-007 owner) | Reviews this runbook at acceptance; sign-off on incorporation into the consolidated governance table D-0091. | 2026-05-18 (this artefact) |
| GA-tagging committee | Reads this runbook as input to MIG-007b (T07.20) — confirms OPS-006 + OPS-007 live before v3.9 GA tag. | Pending T07.20 |

Cross-references:
- Consolidated governance table — D-0091 §2 OPS-006 + OPS-007 rows.
- Peer OPS runbooks — D-0092 (OPS-001), D-0093 (OPS-002), D-0094 (OPS-003), D-0095 (OPS-004), D-0096 (OPS-005).
- NFR-CONV.8 layout-invariance evidence — D-0087 (T07.05).
- Phase-7 checkpoint — CP-P07-T13-T17 (T07.18 closes the OPS-002..007 group).
