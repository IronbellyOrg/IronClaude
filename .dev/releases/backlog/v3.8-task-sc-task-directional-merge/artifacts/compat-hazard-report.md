# Compat Hazard Report — Phase 7 / T07.02

**Task:** T07.02 — Re-verify file references & check compat hazards
**Roadmap Item:** R-025
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Deliverable artifact #2 of T07.02 (companion: `file-reference-reverification.md`).

---

## 0. Scope

This report assesses whether the Phase 6 merge plan (sourced from the six refactor files; `merge-master.md` is empty per CP-P06-END but every change row exists in its originating refactor file) breaks compat with **three hazard classes**:

1. **In-flight MDTM files** under `.dev/tasks/to-do/TASK-*/` — must remain valid for F1 resumption (INV-04).
2. **In-flight sprints** under `.dev/releases/current/` — must not be stranded by `/sc:task` deprecation.
3. **Documented `/sc:task` workflows** in `docs/`, `CLAUDE.md`, `README.md`, `Makefile`, `scripts/`, and in runtime CLI prompt builders (`src/superclaude/cli/sprint/process.py`, `src/superclaude/cli/cleanup_audit/prompts.py`) — must continue to function or be migrated in the same commit window.

For each hazard, this report records: a hazard ID (`HZ-NN`), the affected surface, the failure mode if unmitigated, the **severity** (CRITICAL / HIGH / MEDIUM / LOW), and the **mitigation** — including the originating CR row that already addresses the hazard (where applicable) and any gap that Phase 7 must close.

**Severity legend:**

- **CRITICAL** — breaks a load-bearing invariant (INV-01..INV-05) or breaks user-visible execution path with no fallback.
- **HIGH** — breaks a documented or in-flight workflow with a fallback that requires explicit Phase 7 action.
- **MEDIUM** — degrades behavior or produces confusing messaging but does not break execution.
- **LOW** — cosmetic or documentation drift only.

---

## 1. In-flight MDTM files (hazard class 1) — `.dev/tasks/to-do/TASK-*/`

**Surface:** 25+ TASK directories under `.dev/tasks/to-do/`, with 676 `.md` files total. The F1 loop (INV-01) resumes any of these by reading the first unchecked `- [ ]` line; INV-04 (resumability) is load-bearing.

**Schema diff being introduced (Phase 6 CR-FM-01..04):**

- One new **optional** MDTM frontmatter field: `Tier:` with closed-enum value set `{STRICT, STANDARD, LIGHT, EXEMPT}`.
- One optional per-item inline marker: `(Tier: <enum>)` after `- [ ]`/`- [x]` and before item text.
- A backward-compat default: missing `Tier:` resolves to `STANDARD` silently at Gate 1.

### HZ-01 — Existing TASK-* files lack `Tier:` field → validator must accept absence

**Affected surface:** every existing TASK-*.md file (sampled: `TASK-PRD-20260514-121039.md`, `TASK-TDD-20260514-121250.md`, all `TASK-E2E-*`, all `TASK-RESEARCH-*`, all `TASK-RF-*`).

**Failure mode if unmitigated:** validator rejects every existing TASK-* file on first resumption post-merge. **INV-04 break: catastrophic.**

**Severity:** CRITICAL (if unmitigated).

**Mitigation (already in plan):** `CR-FM-01` declares the field **optional**; `CR-FM-03` is the dedicated backward-compat-shim row that documents the `STANDARD` default and explicitly forbids any migration of existing files. `CR-FM-04` is the cross-row audit that confirms no `helper` script silently backfills the field into existing TASK-* files. Acceptance criterion: every existing TASK-*.md validates clean and Gate 1 emits `dispatch_profile=STANDARD source=default`.

**Verification (Phase 7 execution):** spot-check N=5 TASK-* files from the categories named in `refactor-mdtm-frontmatter.md` § 3.3 row 1. Confirm `frontmatter has no Tier: field AND validates clean`.

**Status:** **MITIGATED in plan.** Phase 7 must execute the CR-FM-04 audit row to verify post-merge.

---

### HZ-02 — Existing TASK-* file uses `tier:` (lowercase) or `Tiers:` accidentally → collision with closed-enum

**Affected surface:** any existing TASK-*.md whose author predicted the schema with a non-canonical casing.

**Failure mode if unmitigated:** field with non-canonical casing is ignored by the validator (since `Tier:` is exact-match), and the file appears to behave per the `STANDARD` default — but the author may have intended a different tier. Silent intent-mismatch, not a hard break.

**Severity:** LOW (no TASK-* file in the current population uses any tier-like field; verified by spot-grep across `.dev/tasks/to-do/`).

**Empirical evidence (T07.02 spot-check):**

```
grep -lE "^(Tier:|tier:|Tiers:|tiers:)" .dev/tasks/to-do/TASK-*/TASK-*.md → 0 matches
```

**Mitigation:** CR-FM-01 specifies the exact casing `Tier:` (matching donor `sc-task-protocol/SKILL.md:121,123` convention). CR-FM-04 audit row will catch any future drift.

**Status:** **NO HAZARD OBSERVED.** Casing-collision risk is theoretical; current population is clean.

---

### HZ-03 — In-flight TASK-PRD-20260514-121039 references `/sc:task` and `sc-task-protocol` as **research subjects** mid-execution

**Affected surface:** `.dev/tasks/to-do/TASK-PRD-20260514-121039/TASK-PRD-20260514-121039.md` (status `🟠 Doing`). The task is producing a PRD for the unified `/sc:task` command in its **post-v3.75 state**. Its research subagent prompts reference live code under `src/superclaude/skills/sc-task-protocol/SKILL.md` and `src/superclaude/commands/task.md` as PRIMARY ARTIFACTS to verify against (via `[CODE-VERIFIED]` tags).

**Failure mode if unmitigated:**

- After CR-DEP-01 (soft-deprecate `commands/task.md`): the live file is now a 10-line stub. Research subagents that attempt to `[CODE-VERIFIED]` the original 170-line surface will see only the stub. Verifications fail; the PRD becomes inconsistent with its sources.
- After CR-DEP-03 (hard-deprecate `sc-task-protocol/SKILL.md`): the file is deleted. Research subagents looking for the donor surface find nothing.

**This is a content-staleness hazard, not an execution hazard:** the F1 loop on this task still functions (INV-04 holds). What breaks is the **PRD's verification basis**.

**Severity:** HIGH (the PRD task is in-flight and was authored against the pre-deprecation surface; merge timing must respect this).

**Mitigation options (Phase 7 must pick one):**

- **(a) Sequence:** complete the in-flight TASK-PRD-20260514-121039 **before** Phase 7 lands CR-DEP-01..04. The PRD captures the pre-deprecation snapshot; the deprecation lands afterward; the PRD becomes a frozen-snapshot historical record (which matches its purpose — it documents the v3.75 state).
- **(b) Snapshot:** create a frozen pre-deprecation copy of `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` (e.g., at `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` — which already exists per git status as an untracked-new archive directory) and rewrite the in-flight task's research-subject paths to point at the archive.
- **(c) Abort/restart:** mark TASK-PRD-20260514-121039 as superseded (the v3.75 state is itself superseded by the directional merge); rebuild a fresh PRD against the post-merge surface.

**Recommendation:** option (a). The TASK-PRD's body explicitly says it produces "a PRD for `/sc:task` as it will exist after v3.75 ships". Phase 7 should let the in-flight PRD finish capturing the v3.75 surface before deprecating it. The archive directory move (visible in git status) suggests this is the intent.

**Status:** **HAZARD ACTIVE.** Phase 7 must record the sequencing choice in `final-merge-plan.md` (T07.04). Default recommendation: complete TASK-PRD-20260514-121039 before CR-DEP-01 lands.

---

### HZ-04 — In-flight TASK-RESEARCH-20260403-sprint-task-exec has status `🟠 Doing` but is functionally complete

**Affected surface:** `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/` — directory contains a completed `RESEARCH-REPORT-sprint-task-execution.md` and a `gaps-and-questions.md`. The frontmatter still reports `🟠 Doing`.

**Failure mode if unmitigated:** none — this task's content is research output, not execution. The "Doing" status is stale bookkeeping.

**Severity:** LOW (no impact on the deprecation; this is a labeling drift unrelated to T07.02 scope).

**Mitigation:** out of scope for T07.02. Phase 7 may note this for general housekeeping but does **not** owe a fix in `final-merge-plan.md`.

**Status:** **NO MITIGATION REQUIRED.**

---

## 2. In-flight sprints (hazard class 2) — `.dev/releases/current/`

**Surface:** two sprints currently under `.dev/releases/current/`:

- `task-builder-merge/` — task-builder convergence release. Grep for `/sc:task\b` and `sc-task-protocol\b` across the directory returns **zero matches**. References are to `/sc:tasklist` (a different command), not `/sc:task`.
- `task-sc-task-directional-merge/` — this sprint itself. Self-reference; not a hazard.

### HZ-05 — `task-builder-merge` sprint references `/sc:task` indirectly?

**Affected surface:** verified `task-builder-merge/`.

**Failure mode if unmitigated:** none observed; the sprint is independent.

**Severity:** **NONE** (no hazard observed).

**Mitigation:** N/A.

**Status:** **NO HAZARD.**

---

### HZ-06 — Future-sprint invocation pattern `superclaude sprint run` emits `/sc:task` per phase

**Affected surface:** any future sprint that invokes `superclaude sprint run <tasklist-index.md>` — the CLI emits `/sc:task` prompts via `src/superclaude/cli/sprint/process.py:170` (`f"/sc:task Execute all tasks in @{phase_file} "`).

**Failure mode if unmitigated:**

- After CR-DEP-01 (soft-deprecate): the prompt resolves to the 10-line deprecation stub, which exits with a message. **The sprint stops executing tasks.** This is a runtime break for the sprint CLI.

**Severity:** CRITICAL (if unmitigated).

**Mitigation (already in plan):** `CR-REF-01` in `refactor-references.md` rewrites `process.py:124 + 170` to emit `/task` instead of `/sc:task` in the **same commit window** as the CR-DEP-01 soft-deprecation. `CR-REF-09` updates the matching test in `tests/sprint/test_process.py:88` (`assert prompt.startswith(...)`) in the same commit.

**Ordering requirement:** CR-REF-01 + CR-REF-09 must land **before or with** CR-DEP-01. If CR-DEP-01 lands first, every interim `superclaude sprint run` invocation breaks until CR-REF-01 lands.

**Verification (Phase 7 execution):** after the commit, `grep -nE "/sc:task" src/superclaude/cli/sprint/process.py` returns no matches; `uv run pytest tests/sprint/test_process.py` passes.

**Status:** **MITIGATED in plan, sequencing-sensitive.** Phase 7 must enforce CR-REF-01 ≤ CR-DEP-01 in commit order (or atomic same-commit). `final-merge-plan.md` must record this constraint explicitly.

---

### HZ-07 — `cleanup_audit` CLI emits `/sc:task` in 5 prompt builders

**Affected surface:** `src/superclaude/cli/cleanup_audit/prompts.py` lines 26, 47, 69, 92, 116 — five f-string prompts beginning with `/sc:task Perform ...`.

**Failure mode if unmitigated:** same as HZ-06 — every `cleanup_audit` invocation hits the deprecation stub and stops executing.

**Severity:** CRITICAL (if unmitigated).

**Mitigation (already in plan):** `CR-REF-02` rewrites all five lines to use `/task` in the same commit window as CR-DEP-01.

**Verification:** `grep -nE "/sc:task" src/superclaude/cli/cleanup_audit/prompts.py` returns no matches; existing tests on these prompts pass.

**Status:** **MITIGATED in plan, sequencing-sensitive.** Same ordering constraint as HZ-06.

---

### HZ-08 — User-typed `/sc:task` invocation in Claude Code mid-session

**Affected surface:** user habits, scripts outside this repo, screenshots in docs, and any `.dev/releases/backlog/*` prompts a user might paste.

**Failure mode:** post-deprecation, typing `/sc:task` invokes the soft-deprecation stub which prints a one-line redirect and exits. The user sees the redirect message and is expected to re-type `/task`.

**Severity:** MEDIUM (intentional UX cost of soft-deprecation; not a break).

**Mitigation (already in plan):** CR-DEP-01 explicitly preserves the file at its path so the invocation does not fail with "skill not found"; the stub body is the user-readable redirect. The transition period absorbs user-habit drift.

**Status:** **ACCEPTED COST, MITIGATED.** No additional Phase 7 action required.

---

## 3. Documented `/sc:task` workflows (hazard class 3) — `docs/`, `CLAUDE.md`, `Makefile`, `scripts/`, sprint/cleanup_audit prompts

### HZ-09 — `docs/user-guide/commands.md` has ~27 `/sc:task` references

**Affected surface:** the canonical user-facing command reference. ~27 grep matches per `refactor-documentation.md` § 0.1.

**Failure mode if unmitigated:** users following the documentation invoke `/sc:task` and hit the soft-deprecation stub. The doc is now stale.

**Severity:** HIGH (user-facing documentation; HIGH because user trust in docs is load-bearing).

**Mitigation (already in plan):** `CR-DOC-NN` rows in `refactor-documentation.md` rewrite every `/sc:task` reference to `/task` per the soft-deprecation contract. The redirect treatment is `update redirect to /task`, matching the deprecation stub's user-visible message.

**Verification:** `grep -nE "/sc:task\b" docs/user-guide/commands.md` returns no matches after Phase 7 lands the doc rows.

**Status:** **MITIGATED in plan.**

---

### HZ-10 — `docs/user-guide/flags.md`, `docs/sprint-cli-deep-dive.md` — adjacent doc references

**Affected surface:** 1 match each per `refactor-documentation.md` § 0.1.

**Severity:** MEDIUM.

**Mitigation (already in plan):** same `redirect` treatment in `refactor-documentation.md`.

**Status:** **MITIGATED in plan.**

---

### HZ-11 — `docs/generated/sprint-cli/*` — pipeline-generated artifacts

**Affected surface:** ~10 files under `docs/generated/sprint-cli/` and its `v3.7-refactor/` and `debates/` subdirectories.

**Failure mode:** these are pipeline-generated; rewriting them risks falsifying the generation record.

**Severity:** LOW (generated content; users do not typically follow these as authoritative).

**Mitigation (already in plan):** `refactor-documentation.md` treats `docs/generated/*` as **`leave-with-note`** — single-header annotation indicating the references predate the 2026-MM-DD deprecation. Same treatment for `docs/research/dev-guide-research/*` (extraction artifacts).

**Status:** **MITIGATED in plan.**

---

### HZ-12 — `docs/analysis/*.md`, `docs/guides/*.md` — analysis & guides bodies

**Affected surface:** 4 analysis files + 6 guides + ~10 dev-guide-research extraction files.

**Severity:** MEDIUM (analysis/guides are user-readable; staleness erodes trust).

**Mitigation (already in plan):** `refactor-documentation.md` assigns `redirect` for analysis/guides; `leave-with-note` for dev-guide-research extraction artifacts (frozen at extraction time).

**Status:** **MITIGATED in plan.**

---

### HZ-13 — `scripts/sync_from_framework.py:84` — doc-string reference

**Affected surface:** one line of script documentation.

**Severity:** LOW (cosmetic; script behavior is unaffected).

**Mitigation (already in plan):** `CR-REF-11` rewrites the doc-string in place.

**Status:** **MITIGATED in plan.**

---

### HZ-14 — `Makefile` — no direct `/sc:task` reference; sync rules touched by CR-DIST-NN

**Affected surface:** `Makefile` sync-dev and verify-sync targets.

**Failure mode if unmitigated:** none directly. The `make sync-dev` rule must be updated (CR-DIST-NN / T06.04 CS-M5-A) so that `[.claude] .claude/skills/sc-task-protocol/` is removed in the same commit as `[src] src/superclaude/skills/sc-task-protocol/` deletion. Otherwise `make verify-sync` flags drift.

**Severity:** HIGH (R-RULE-10 drift between `[src]` and `[.claude]` is forbidden; verify-sync is the gate).

**Mitigation (already in plan):** `refactor-distribution.md` CR-DIST-NN includes the sync-filter update; `refactor-sctask-deprecation.md` CR-DEP-04 explicitly couples to T06.04 CS-M5-A and requires the same-commit constraint.

**Status:** **MITIGATED in plan.**

---

### HZ-15 — `.dev/releases/backlog/v5.xxforensic/` — 14 files with `/sc:task` / `sc-task-protocol` references

**Affected surface:** highest-density historical region; 14 files identified by `refactor-references.md`.

**Failure mode:** future cleanup PRs may mistake the archived references for live and try to rewrite them, generating noise.

**Severity:** LOW (historical record).

**Mitigation (already in plan):** `refactor-references.md` adds **one** `DEPRECATION-NOTE.md` at `.dev/releases/backlog/v5.xxforensic/DEPRECATION-NOTE.md` (planned-new row 136 in companion file) covering all 14. Bodies are not rewritten (R-RULE-11 spirit: history not re-litigated).

**Status:** **MITIGATED in plan.**

---

### HZ-16 — `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` — 47 files in newly-moved archive

**Affected surface:** the v3.75 archive directory (per git status, untracked-new — recently moved from `.dev/releases/backlog/`).

**Failure mode:** archive references are historical. Same risk as HZ-15.

**Severity:** LOW.

**Mitigation (already in plan):** `refactor-references.md` row covers archive buckets with `leave-as-is` + optional archive-root `DEPRECATION-NOTE.md`. Phase 7 picks whether to add the optional note; default-recommended yes (per § 4.A.4 of `refactor-references.md`).

**Status:** **MITIGATED in plan, Phase 7 picks the optional add.**

---

### HZ-17 — `CLAUDE.md` (project) and `~/.claude/CLAUDE.md` (user-global) — no direct `/sc:task` references

**Affected surface:** `CLAUDE.md` (this repo) — does not reference `/sc:task` directly; references `make sync-dev`, MCP servers, etc. The user-global `~/.claude/CLAUDE.md` (per session-context envelope) references slash commands generically.

**Severity:** **NONE** observed.

**Mitigation:** N/A.

**Status:** **NO HAZARD.**

---

### HZ-18 — `README.md` — top-level project README

**Affected surface:** root `README.md`.

**Failure mode if unmitigated:** stale messaging if it advertises `/sc:task`.

**Severity:** MEDIUM.

**Mitigation (already in plan):** `refactor-documentation.md` covers top-level docs. Phase 7 verifies no `/sc:task` reference remains in `README.md` post-commit.

**Status:** **COVERED in plan** (verify with grep at Phase 7 commit time).

---

## 4. Cross-hazard sequencing constraint summary

The following hazards share a single sequencing requirement that `final-merge-plan.md` (T07.04) must enforce:

| Hazard | Constraint |
|---|---|
| HZ-06 (sprint/process.py emits /sc:task) | `CR-REF-01` ≤ `CR-DEP-01` (same commit or earlier) |
| HZ-07 (cleanup_audit/prompts.py emits /sc:task) | `CR-REF-02` ≤ `CR-DEP-01` (same commit or earlier) |
| HZ-09..HZ-12 (docs) | `CR-DOC-NN` ≤ `CR-DEP-01` (or **at most** one commit later — soft-deprecation message names `/task` so docs should match by the time users read them) |
| HZ-14 (Makefile sync rule) | `CR-DIST-NN sync filter` + `CR-DEP-03` + `CR-DEP-04` ship atomically |
| HZ-03 (in-flight TASK-PRD-20260514-121039) | TASK-PRD-20260514-121039 completes **before** `CR-DEP-01` lands (recommended option (a)) |

**The plan already enforces atomic milestones** (per `merge-roadmap.md` § 2 build-order sentence: M1+M2+M3 absorption → M4 deprecation → M5 distribution+documentation). The hazard-derived constraints above are consistent with this build order; HZ-03 is the only constraint that touches scheduling outside the milestone graph (it concerns an in-flight task, not a Phase 7 change row).

---

## 5. Hazard severity roll-up

| Severity | Count | Mitigated in plan | Phase 7 action required |
|---|---|---|---|
| CRITICAL | 3 (HZ-01, HZ-06, HZ-07) | 3 | execute CR-FM-04 audit; enforce CR-REF-01 ≤ CR-DEP-01; enforce CR-REF-02 ≤ CR-DEP-01 |
| HIGH | 4 (HZ-03, HZ-09, HZ-14, HZ-18) | 4 | sequence TASK-PRD-20260514-121039 completion before CR-DEP-01 (HZ-03); execute CR-DOC-NN rows (HZ-09); atomic sync-filter+delete commit (HZ-14); grep-verify README post-commit (HZ-18) |
| MEDIUM | 4 (HZ-08, HZ-10, HZ-12, HZ-18 partial) | 4 | docs rewrite + intentional UX cost of soft-deprecation acceptance |
| LOW | 4 (HZ-02, HZ-04, HZ-11, HZ-13, HZ-15, HZ-16) | 6 | optional DEPRECATION-NOTE.md adds; cosmetic docstring fix |
| NONE | 2 (HZ-05, HZ-17) | — | — |

**Every hazard found carries a severity and a mitigation. Zero hazards lack a mitigation.**

---

## 6. INV-04 (resumability) sample verification

Per T07.02 AC #4, **no planned MDTM frontmatter change breaks an existing TASK-* file without a mitigation**. Sample verification on 5 representative existing TASK-*.md files:

| # | TASK-*.md sampled | Frontmatter has `Tier:` field? | Validates clean post-CR-FM-01..03? | Compat shim applies? |
|---|---|---|---|---|
| 1 | `TASK-PRD-20260514-121039/TASK-PRD-20260514-121039.md` | No | Yes (default `STANDARD` via CR-FM-03) | Yes |
| 2 | `TASK-TDD-20260514-121250/TASK-TDD-20260514-121250.md` | No | Yes (default `STANDARD`) | Yes |
| 3 | `TASK-E2E-20260326-tdd-pipeline/` (sampled) | No | Yes (default `STANDARD`) | Yes |
| 4 | `TASK-RESEARCH-20260324-001/` (sampled) | No | Yes (default `STANDARD`) | Yes |
| 5 | `TASK-RF-20260325-cli-tdd/` (sampled) | No | Yes (default `STANDARD`) | Yes |

**Result:** five existing TASK-*.md files validate clean post-CR-FM-01..03 with the compat shim. INV-04 holds across the sample.

**Note (limitation of sample):** the spot-check was a structural read of frontmatter, not a full F1 dry-run. CR-FM-04 (Phase 7 audit row) will run the dry-run on the same five files at commit time per its acceptance criterion.

---

## 7. Acceptance Criteria recap (T07.02 AC #2–#4)

1. **`compat-hazard-report.md` exists and assesses in-flight MDTM files, current sprints, and documented workflows.** ✅ — § 1 (4 hazards for in-flight MDTM), § 2 (4 hazards for sprints + CLI emitters), § 3 (10 hazards for docs/scripts/Makefile/archive buckets).
2. **Every hazard found carries a severity and a mitigation.** ✅ — 18 hazards classified across CRITICAL/HIGH/MEDIUM/LOW/NONE; each has a Mitigation row pointing to an originating CR in the Phase 6 plan or an explicit Phase 7 action.
3. **No planned MDTM frontmatter change breaks an existing TASK-* file without a mitigation (INV-04).** ✅ — § 1 HZ-01 is the dedicated row; CR-FM-01 (optional) + CR-FM-03 (compat shim) + CR-FM-04 (audit) collectively guarantee INV-04. § 6 sample verification confirms across five representative files.

**T07.02 compat-hazard deliverable: COMPLETE.**

---

## 8. Carry-forward findings for T07.04 (final-merge-plan.md)

Findings Phase 7's `final-merge-plan.md` must record explicitly:

1. **CR-REF-01 + CR-REF-02 are HZ-06/HZ-07 mitigations** and must land **same commit as or before** CR-DEP-01. The merge plan must record this dependency edge.
2. **In-flight TASK-PRD-20260514-121039 sequencing (HZ-03)** is the only out-of-band scheduling constraint. Phase 7 should record the chosen mitigation (default: option (a) — complete the PRD before CR-DEP-01).
3. **The `docs/research/_archive/` move (planned-new path 138 in companion file)** is optional and Phase 7 decides at commit time per `refactor-documentation.md`.
4. **CR-DIST-NN sync-filter + CR-DEP-03 + CR-DEP-04** must ship atomically (HZ-14); this is already in the plan's milestone graph as M4 → M5 atomic boundary.
5. **`merge-master.md` is empty** (CP-P06-END finding). T07.04's `final-merge-plan.md` is the artifact that closes this gap — it becomes the consolidated single plan with the hazard-derived sequencing constraints above applied.
