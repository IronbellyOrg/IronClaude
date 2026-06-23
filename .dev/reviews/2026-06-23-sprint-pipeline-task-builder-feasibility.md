# Feasibility Study: Refactoring the Sprint Run CLI Pipeline to Orchestrate `/task` + `task-builder`

**Date:** 2026-06-23
**Status:** Feasibility study — review only, no code changes
**Question:** Replace the Sprint pipeline's current orchestration of `sc:tasklist` (input) + `sc:task` (execution) with `task-builder` (input) + `/task` (execution).

---

## 1. How the Sprint Run Pipeline Works Today (Review)

**Entry:** `superclaude sprint run <tasklist-index.md>` → Click group/command in
`src/superclaude/cli/sprint/commands.py:16-278`. Dispatches to `execute_sprint()` (or tmux).

**Input contract (from `sc:tasklist`):** a multi-file bundle — `tasklist-index.md` plus
`phase-N-tasklist.md` files. Sprint discovers phases by regex
(`config.py:58-146`) and parses tasks with bespoke patterns
(`config.py:189-196`): `### T<PP>.<TT> -- Title` headings, metadata tables
(`Tier`, `Dependencies`, `Command`, `Classifier`), and `### Checkpoint:` sections.

**Orchestration loop:** `executor.py:1712-2100+`. Per active phase, modern path delegates
**per task** via `execute_phase_tasks()` (`executor.py:1303-1509`) → `_run_one_task()`.

**Dispatch mechanism:** each phase/task spawns a `claude --print --verbose` subprocess
(`process.py:137-266`). The prompt is literally:

```
/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic
+ sprint context + tier execution rules + checkpoint-scan rules + result-file rule
```

**Supporting machinery (substantial):**
- 4-layer env isolation per task — `CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`,
  `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR` (`executor.py:180-221`).
- Budget: `TurnLedger`; telemetry: `ShadowGateMetrics`; remediation: `DeferredRemediationLog`.
- Resume: `ResumePlanner` + `DriftAssessor` (hashes the tasklist to detect drift) +
  `BoundaryIntegrityGate` (`commands.py:441-543`).
- Handoff records (typed, schema v1) → `results/handoff/phase-{N}-task-{ID}.json`.
- Wiring gates (post-task / post-phase), checkpoints.
- Data models in `models.py` (800+ lines); ~15 test files under `tests/sprint/`.

**Key invariant:** the phase tasklist file is **read-only** from Sprint's perspective.
Completion is tracked out-of-band — via the result file
(`EXIT_RECOMMENDATION: CONTINUE|HALT`), the stream-json transcript, and handoff records —
**not** by mutating the tasklist. Tier compliance (STRICT/STANDARD/LIGHT/EXEMPT) is injected
into the prompt and enforced by the subprocess.

---

## 2. What `task-builder` + `/task` Provide

**`task-builder`** (`skills/task-builder/SKILL.md`) produces a single **MDTM task file** per
work item at `.dev/tasks/to-do/TASK-RF-<subject>-<ts>/TASK-RF-*.md`: YAML frontmatter
(`status`, `reflect_pre/post`, …), phases (Phase 1 setup; Phase 2+ work), and B2
self-contained checklist items with embedded `ensuring…` verification clauses, plus a
research/ + qa/ evidence trail. It stops at file creation.

**`/task`** (`skills/task/SKILL.md`) runs the **F1 loop** (READ → IDENTIFY → EXECUTE → UPDATE
→ REPEAT): reads the file, executes the first unchecked `- [ ]` item, marks it `- [x]`
**on disk**, runs rf-qa phase-gate QA at each phase boundary, post-completion validation, and
flips frontmatter `status` to `🟢 Done`. It is **session-resumable** by re-reading the file.

---

## 3. The Four Structural Mismatches (the crux)

| # | Dimension | Sprint + `sc:task` (today) | `task-builder` + `/task` (proposed) | Impact |
|---|-----------|----------------------------|--------------------------------------|--------|
| 1 | **Input format** | `phase-N-tasklist.md`, `T<PP>.<TT>` headings + metadata tables | MDTM file, frontmatter + B2 checklist | Sprint's `config.py` parsers don't read MDTM. Need new parser or a translation layer. |
| 2 | **State / source of truth** | Phase file **read-only**; progress via result file + transcript + handoff | Progress by **mutating the file** (checkboxes + frontmatter) | Biggest conflict. `DriftAssessor` hashes the tasklist to detect tampering — a file that mutates *during* execution breaks drift-by-hash. |
| 3 | **Unit of work** | One subprocess per phase/task; explicit per-task delegation | F1 loop is **non-delegable** (Rule #12, `skills/task/SKILL.md:371`); one `/task` runs *all* phases inline in one session | Collides head-on. Sprint wants fine-grained subprocess control; `/task` wants to own the whole task. |
| 4 | **Granularity / mapping** | One tasklist bundle = whole sprint (phases) | One MDTM file = one work item (with internal phases) | "sprint = N task files" vs "sprint = 1 tasklist". No clean 1:1 map. |

**Secondary gaps:** result-file `EXIT_RECOMMENDATION` and checkpoint-section conventions have
no MDTM equivalent (need adapter for HALT/CONTINUE); tier → QA-intensity mapping must be
defined. **What carries over cleanly:** the 4-layer env isolation and `CLAUDE_WORK_DIR`
scoping are orthogonal to which skill runs inside — they work unchanged.

---

## 4. The Blocking Dependency

Mismatch #3 is already on the roadmap. The
`.dev/reviews/2026-06-22-per-phase-delegated-execution-task-builder.md` study proposes a
**two-level loop**: an orchestrator P-loop that spawns a fresh `rf-phase-executor` per phase,
with F1 re-scoped to a single phase. That refactor is **exactly** what makes `/task` map onto
Sprint's per-phase subprocess model — without it, a single `/task` call swallows an entire
task in one session and Sprint loses its per-phase isolation, budget granularity, and gates.

**Conclusion: the per-phase delegation refactor is the natural prerequisite/enabler for this
Sprint refactor.** Doing the Sprint swap first would mean re-implementing per-phase delegation
inside the Sprint layer, then throwing it away.

---

## 5. Two Viable Shapes

**(A) Thin adapter / bridge — cheap spike (S–M effort).**
Keep all of Sprint's orchestration, budget, isolation, and resume machinery. Change only:
swap the prompt from `/sc:task @phase_file` to `/task @mdtm_file`; add a format translator
(phase-file ⇄ MDTM); reconcile result-file vs on-disk-checkbox state (pick one ledger).
Fastest way to validate end-to-end; leaves the state-model conflict (#2) only partially
resolved. Good as a proof-of-concept.

**(B) Re-architecture — Sprint as a thin MDTM orchestrator (L effort).**
Sprint = a set of `TASK-RF-*` files (or one MDTM file whose phases are the sprint phases).
Sprint's loop calls `/task` per file/phase and reads frontmatter `status` + checkbox state as
the **single** progress ledger — which actually *simplifies* resume (the on-disk task file
becomes the canonical state, retiring much of the result-file/handoff plumbing). Requires the
per-phase delegation refactor first, and reworking `DriftAssessor` to tolerate intentional
in-flight mutation (hash structure, not content). Best long-term fit; aligns with the
direction the `/task` system is already heading.

---

## 6. Verdict & Recommendation

**Feasible, but not a drop-in.** It is a swap of both the *data contract* and the *unit of
orchestration*, not a string change. The hard part is the state-model inversion (#2) and the
non-delegable F1 loop (#3) — and #3 is already being solved independently.

**Recommended path:**
1. **Land the per-phase delegation refactor first** (2026-06-22 review). It is the keystone;
   the Sprint swap is low-value and high-rework without it.
2. **Spike approach (A)** behind a flag to validate the `/task` prompt + MDTM translation
   end-to-end on one real sprint, measuring against current behavior.
3. **Then commit to approach (B)** — collapse onto the on-disk MDTM file as the single ledger,
   retire the result-file/handoff duplication, and adapt `DriftAssessor` to structural hashing.

**Rough sizing:** prerequisite refactor = the larger lift; (A) spike ≈ days; (B) ≈ a
multi-phase effort touching `executor.py`, `config.py`, `models.py`, resume/drift gates, and
`tests/sprint/`. Do not start the Sprint swap until the per-phase delegation work is merged.
