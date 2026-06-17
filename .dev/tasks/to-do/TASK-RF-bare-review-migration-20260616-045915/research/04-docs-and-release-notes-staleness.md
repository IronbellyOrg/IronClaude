# R4 — Docs & Release-Notes Staleness (sc-bare-review M8/M9 migration)

**Status:** Complete
**Researcher:** R4 (Doc Cross-Validator)
**Scope:** `docs/swarm/` + `docs/dev/lens-contribution-policy.md`; the 6 Phase-9 OPS docs requirement.
**Repo root:** /config/workspace/IronClaude

Staleness tags: **[CODE-VERIFIED]** = claim matches source as of this research; **[CODE-CONTRADICTED]** = claim is false vs source; **[UNVERIFIED]** = could not confirm.

---

## 0. Authoritative requirement sources (cite these in the tasklist)

| Source | What it defines |
|---|---|
| `.dev/releases/complete/MultiModelSwarm/tasklist/phase-9-tasklist.md` | The 6 OPS docs + IDs **OPS-001..006**, roadmap rows **R-150..R-155**, deliverable **D-0135** (T09.06). Operative source of the "6 OPS docs" requirement; titled "Operational Handoff". |
| `.dev/reflect/mms-phase-9-postaudit/REPORT.md` | Audit verdict: **0/8 SHIPPED**, `tasklist_completion_pct: 0.0`, promotion gate BLOCKED. |
| `.dev/releases/complete/MultiModelSwarm/merged-requirements.compressed.md` | Parent spec — architecture-level observability + **NFR-008 / NFR-012** (lens PR-review discipline); no explicit `OPS-*` IDs (those originate in the phase-9 tasklist). |

**OPS ID → deliverable → roadmap row** (from `phase-9-tasklist.md:3,9,45,82,137,176,212`) [CODE-VERIFIED]:

| OPS ID | Roadmap | Task | Required deliverable path |
|---|---|---|---|
| OPS-001 | R-150 | T09.01 | `docs/swarm/operator-runbook.md` |
| OPS-002 | R-151 | T09.02 | `scripts/swarm_env_readiness.sh` + `docs/swarm/env-readiness.md` |
| OPS-003 | R-152 | T09.03 | `docs/swarm/observability-procedure.md` |
| OPS-004 | R-153 | T09.05 | `docs/swarm/rollback-procedure.md` + **tabletop rehearsal sign-off** (STRICT, critical-path) |
| OPS-005 | R-154 / D-0135 | T09.06 | `docs/swarm/lens-contribution-policy.md` |
| OPS-006 | R-155 | T09.07 | `docs/swarm/post-release-metrics.md` |

Checkpoints also required and absent: `phase-9-cp1.md` (T09.04, mid-phase) and `phase-9-cp2.md` (T09.08, exit gate). `REPORT.md:24` — "No `phase-9-cp*.md`; no `checkpoints/` subdir; no T09 exec-log rows." [CODE-VERIFIED]

---

## 1. Inventory of `docs/swarm/` (all dated Jun 10 13:09)

| File | 1-line purpose | Overlap with OPS requirement? |
|---|---|---|
| `README.md` | Documentation index / "start here" + document map for the 8 swarm docs. | none direct |
| `command-reference.md` | Per-flag reference + exit codes for all 8 `swarm` commands. | none direct |
| `lens-catalog.md` | The 7 lenses, 6 recipes, custom-py loader, how to author a lens. | partial vs OPS-005 (authoring), but governance/PR-policy is separate |
| `monitoring-patterns.md` | Three ways to wait on a job (done.json sentinel / JSONL tail / `status --watch`). | **PARTIAL overlap with OPS-003** observability-procedure |
| `oq-resolutions.md` | Design rationale for INV-005/007, OQ-009/010 (maintainer-facing). | none direct |
| `release-notes-v1.md` | What shipped in v1; resume, inject-guard, custom-prompt migration. | contains the FALSE thin-caller claim (§2) |
| `runbook.md` | Operator runbook: env mandate, Rich TUI dep, T2 proxy env, tmux modes. | **PARTIAL overlap with OPS-001** operator-runbook |
| `transport-limits.md` | Phase-1 transport exclusions. | none direct |
| `user-guide.md` | Step-by-step examples across every use case. | partial vs OPS-001 |

### Overlap 1 — `runbook.md` vs OPS-001 `operator-runbook.md`

`runbook.md` headings (`runbook.md:1,12,60,92,161`) [CODE-VERIFIED]:
`# MultiModelSwarm Operator Runbook` / `## Environment Mandate (AC-001)` / `## Rich TUI Dependency (AC-007)` / `## T2 Proxy Env Contract (AC-017)` / `## tmux is Optional (AC-008)`.

It is **AC/invariant-organized** (Phase-8 acceptance criteria), NOT workflow-organized.

OPS-001 requires (`phase-9-tasklist.md:20`): "`docs/swarm/operator-runbook.md` documenting **run/status/logs/watch/resume/kill/attach** workflows" + cross-links to OPS-002/003/004 (`:32`). The existing `runbook.md` has no run/status/logs/watch/resume/kill/attach workflow sections — it covers env+TUI+proxy+tmux only.

**Conclusion:** `runbook.md` does NOT satisfy OPS-001 scope. Audit agrees: `REPORT.md:17` — "Absent (`docs/swarm/` has `runbook.md` from Phase 8, **not** `operator-runbook.md`)." [CODE-VERIFIED] → **EXTEND-EXISTING is risky** (different organizing axis + naming collision); recommend NET-NEW `operator-runbook.md` that cross-references `runbook.md` for the env/TUI/tmux material rather than duplicating it.

### Overlap 2 — `monitoring-patterns.md` vs OPS-003 `observability-procedure.md`

`monitoring-patterns.md` headings (`monitoring-patterns.md:1,34,80,121,163`) [CODE-VERIFIED]:
`# Swarm Monitoring Patterns (FR-013 / T07.10)` / `## Pattern 1 — Wait for terminal via done.json sentinel` / `## Pattern 2 — Live-tail the JSONL event stream` / `## Pattern 3 — Watch phase progress with swarm status --watch` / `## Pattern selection`.

It is **"how to WAIT on a job"** (3 polling patterns) — a CI/automation audience (README map: "CI / automation | Three ways to wait on a job").

OPS-003 requires (`phase-9-tasklist.md:93`): "`docs/swarm/observability-procedure.md` documenting **state file / JSONL log / Markdown log / done sentinel + debugging recipes**." A superset: the three-layer durable-observability *artifacts* + debugging procedure, not just the wait patterns.

**Conclusion:** `monitoring-patterns.md` is a strict SUBSET (covers done.json + JSONL only; omits state file, Markdown log, and debugging recipes). Audit agrees: `REPORT.md:19` — "Absent (only `monitoring-patterns.md` present)." [CODE-VERIFIED] → recommend NET-NEW `observability-procedure.md` that cross-references `monitoring-patterns.md` for the wait-patterns and adds the state-file/Markdown-log/debugging-recipe layers.

---

## 2. `release-notes-v1.md` — FALSE thin-caller claim (must reconcile in WS-D)

**The claim** (`docs/swarm/release-notes-v1.md:16-26`), exact quote [CODE-CONTRADICTED]:

> "The `sc-bare-review` skill is now a **~60-line thin caller** over the
> swarm CLI. Preflight, parallel dispatch, normalization, atomic writes,
> and contract emission moved out of
> `src/superclaude/skills/sc-bare-review/scripts/*.sh` and into the
> bundled `bare-review` lens … The shell
> scripts (`t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py`) are
> retired by MIG-003 (T08.07) **after** the A/B parity gate
> (TEST-003 / T08.11) goes green."

**Why it is FALSE / premature:**

- `wc -l src/superclaude/skills/sc-bare-review/SKILL.md` = **231 lines**, not ~60. [CODE-CONTRADICTED]
- The scripts are **still present** — `ls src/superclaude/skills/sc-bare-review/scripts/` shows `t2_dispatch.sh` (5068 B), `t2_normalize.py` (10429 B), `t2_preflight.sh` (9976 B), all dated Jun 8. They were NOT retired. [CODE-CONTRADICTED]
- The release note's own escape clause ("retired … **after** the A/B parity gate goes green") confirms the migration is conditional and unfinished; the "is now a ~60-line thin caller" present-tense headline asserts a completed state that does not exist.

Audit corroboration: `REPORT.md:51` — "SKILL.md **not** a thin caller, legacy `scripts/*.sh` **not** deleted, A/B parity gate Phase-8-homed and library-level only." [CODE-VERIFIED]

**WS-D reconciliation requirement:** `release-notes-v1.md:16` must be rewritten to accurate state. Either (a) revert to future/conditional tense ("will become a thin caller once MIG-003 completes"), or (b) if WS-A/B actually performs the migration in this corrective task, update the line to the true final line count + confirm scripts deleted. The note must NOT ship a present-tense "is now ~60 lines" while SKILL.md is 231 lines. The same file repeats the dependency at `release-notes-v1.md:314-329` ("Pre-deletion checklist for legacy shells (MIG-003)") — that section is internally consistent (conditional) and can stay; the §"What changed" headline at line 16 is the contradiction.

> Note: R1 owns SKILL.md/scripts. The 231-line figure here is cross-validation for the doc claim, not the migration plan. Defer the authoritative SKILL.md size/structure to R1.

---

## 3. `docs/dev/lens-contribution-policy.md` — already exists, exceeds OPS-005

**Exists:** `docs/dev/lens-contribution-policy.md`, **515 lines**, dated Jun 8. [CODE-VERIFIED]

**Scope** (`lens-contribution-policy.md:1,3`): `# Lens contribution policy` — "**Scope:** governance for new entries in `cli/swarm/lenses/__init__.py::LENSES`". References roadmap R-039 (FR-040) / R-041 (NFR-008) and **NFR-012 lens-registry PR review discipline**, plus the COMP-023 validator (`cli/swarm/lenses/_validate.py`) and `superclaude swarm validate-lenses` (`:16-25`). [CODE-VERIFIED]

**Coverage vs OPS-005 acceptance criteria** (T09.06 requires: 5 review criteria + validator reference + embedded PR checklist + suspect:true scrutiny):

- `§0 Five-criterion reviewer checklist (TL;DR)` at `:28`, with explicit **C1 Real caller** (`:35`), **C2 §11.5 injection-guard substring** (`:39`), **C3 normalizer_strategy matches recipe output shape** (`:43`), **C4 Real downstream command** (`:49`), **C5 suspect:true by-construction justification** (`:53`). [CODE-VERIFIED] — all 5 criteria present.
- Validator reference: COMP-023 / `_validate.py` / `swarm validate-lenses` (`:24,75`). [CODE-VERIFIED]
- PR checklist embedded as `- [ ]` checkboxes (`:35-57`). [CODE-VERIFIED]
- suspect:true scrutiny: C5 (`:53-57`). [CODE-VERIFIED]

The T09.06 tasklist criteria — "real caller, §11.5 substring, recipe/template alignment, downstream command, suspect scrutiny" (`phase-9-tasklist.md:188-190`) — map **1:1** onto C1-C5 in the existing doc.

**Conclusion — RELOCATE / cross-reference, NOT author-new.** The existing `docs/dev/lens-contribution-policy.md` is a strict superset of the OPS-005 requirement. A second `docs/swarm/lens-contribution-policy.md` authored from scratch would duplicate content and invite drift. Recommended satisfaction options (simplest-first per `feedback_prefer_simpler_proposals`):

1. **Cross-reference (smallest):** Add `docs/swarm/lens-contribution-policy.md` as a thin pointer linking to `docs/dev/lens-contribution-policy.md` as the canonical policy. Satisfies "doc exists at required path" + markdownlint, zero duplication.
2. **Relocate:** Move `docs/dev/lens-contribution-policy.md` → `docs/swarm/lens-contribution-policy.md` and update inbound references. (grep over `phase-9-tasklist.md` for `docs/dev|relocat|already exist|existing` returned **no hits** — the tasklist was authored unaware the dev-side policy already existed, which is why it specified author-from-scratch. This is the key reconciliation note for WS-D.)

Decision hinge for the tasklist: if any file links to `docs/dev/lens-contribution-policy.md` → option 1 (cross-ref) is safer; if no inbound links → option 2 (relocate) is clean.

---

## 4. Per-OPS-doc classification (NET-NEW / EXTEND / RELOCATE) + target path

| OPS | Target path (required) | Classification | Rationale |
|---|---|---|---|
| OPS-001 | `docs/swarm/operator-runbook.md` | **NET-NEW** (cross-ref `runbook.md`) | `runbook.md` is AC-organized (env/TUI/proxy/tmux), not the run/status/logs/watch/resume/kill/attach workflow doc OPS-001 needs. Naming differs; do not rename `runbook.md` (linked from README map). Author new, link to `runbook.md` for env/TUI material. |
| OPS-002 | `scripts/swarm_env_readiness.sh` + `docs/swarm/env-readiness.md` | **NET-NEW (both)** | Both MISSING (`REPORT.md:18`). Script checks Python≥3.10/UV/httpx/Click/Rich/tmux(opt)/T2 proxy vars (`phase-9-tasklist.md:56`); doc covers checklist + INV-007 env-missing path (`:57`). Script goes in repo-root `scripts/`, NOT `docs/`. |
| OPS-003 | `docs/swarm/observability-procedure.md` | **NET-NEW** (cross-ref `monitoring-patterns.md`) | `monitoring-patterns.md` is a subset (wait-patterns only). New doc adds state-file/Markdown-log/debugging-recipe layers (`phase-9-tasklist.md:93`). Cross-link the wait patterns. |
| OPS-004 | `docs/swarm/rollback-procedure.md` + tabletop rehearsal sign-off | **NET-NEW** | Absent; no rehearsal (`REPORT.md:21`). STRICT/critical-path — sign-off captured in doc appendix (`phase-9-tasklist.md:150,161`). The rehearsal is an EXECUTION step, not just a doc; tasklist must HALT for human sign-off (cf. `feedback_human_decision_items_must_halt`) — do NOT auto-stamp. |
| OPS-005 | `docs/swarm/lens-contribution-policy.md` | **RELOCATE / cross-reference** | Canonical content already exists at `docs/dev/lens-contribution-policy.md` (515 lines, covers C1-C5 + validator + PR checklist). See §3. Smallest-safe: thin pointer; or relocate if no inbound links. |
| OPS-006 | `docs/swarm/post-release-metrics.md` | **NET-NEW** | Absent (`REPORT.md:23`). Enumerate metrics + review window + backlog-feedback loop (`phase-9-tasklist.md:223`). NOTE: parent spec defers Prometheus/OpenMetrics (§5) — do not claim metrics export. |

Plus checkpoints (not "docs" but required by the phase): `phase-9-cp1.md` (after T09.01-03) and `phase-9-cp2.md` (exit gate) — both **NET-NEW**, under the release tasklist's `checkpoints/` dir; both absent (`REPORT.md:24,16`).

---

## 5. Parent-spec requirement IDs to cite

From `.dev/releases/complete/MultiModelSwarm/merged-requirements.compressed.md` [CODE-VERIFIED]:

- The parent spec does **NOT** define `OPS-*` IDs. OPS-001..006 originate in `phase-9-tasklist.md` (the "Operational Handoff" stream). [CODE-VERIFIED]
- Observability is specified at the **architecture** level: `:51` — "durable observability" as an orchestrator responsibility; `:465` — "three-layer durable observability" (the source of OPS-003's state-file/JSONL/Markdown-log layering). [CODE-VERIFIED]
- `:724` — "Prometheus / OpenMetrics output at event boundaries? **Defer.**" → OPS-006 post-release-metrics must NOT claim Prometheus export; explicitly deferred. [CODE-VERIFIED]
- Lens PR-review discipline IDs: **NFR-008** (R-041) and **NFR-012** (lens-registry PR review discipline) — both already referenced by `docs/dev/lens-contribution-policy.md:16-20`. Cite these for OPS-005. [CODE-VERIFIED]
- No explicit `NFR-*` rollback ID in the parent spec; rollback is purely a phase-9-tasklist deliverable (OPS-004 / R-153). [CODE-VERIFIED — absence]

---

## Summary for the tasklist author (WS-D scope)

1. **0/6 OPS docs + 0/2 checkpoints exist** under the required names (audit `REPORT.md` 0/8 SHIPPED). 5 are NET-NEW; 1 (OPS-005) is satisfiable by RELOCATE/cross-ref to the pre-existing `docs/dev/lens-contribution-policy.md`.
2. **`release-notes-v1.md:16` is the load-bearing staleness defect:** present-tense "is now a ~60-line thin caller" is CODE-CONTRADICTED (SKILL.md=231 lines; `scripts/*.sh` still present). WS-D must reconcile this to the true post-migration state (coordinate with R1 on the final SKILL.md figure).
3. **Two naming collisions to avoid:** `operator-runbook.md` ≠ existing `runbook.md`; `observability-procedure.md` ⊋ existing `monitoring-patterns.md`. New docs cross-reference, not duplicate or rename (both existing files are linked from `README.md` document map).
4. **OPS-004 tabletop rehearsal is a HALT item**, not a doc-only deliverable — sign-off must be human-captured, never auto-stamped.
5. **Cite:** OPS-001..006 / R-150..155 / D-0135 from `phase-9-tasklist.md`; NFR-008 / NFR-012 + "three-layer durable observability" + Prometheus-deferred from the parent merged-requirements spec.
