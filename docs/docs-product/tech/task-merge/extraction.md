---
spec_source: TDD_TASK_DIRECTIONAL_MERGE.compressed.md
generated: 2026-05-16T14:05:00Z
generator: claude-opus-4-7-requirements-extraction
functional_requirements: 19
nonfunctional_requirements: 18
total_requirements: 37
complexity_score: 0.92
complexity_class: HIGH
domains_detected: [backend, testing, devops, security, documentation, cli, governance]
risks_identified: 21
dependencies_identified: 22
success_criteria_count: 20
extraction_mode: chunked
data_models_identified: 5
api_surfaces_identified: 13
components_identified: 8
test_artifacts_identified: 30
migration_items_identified: 10
operational_items_identified: 5
pipeline_diagnostics: {elapsed_seconds: 353.2, started_at: "2026-05-16T13:58:04.811532+00:00", finished_at: "2026-05-16T14:03:58.028380+00:00"}
---

## Functional Requirements

### FR-TU-1
**Tier field + Gate-1 dispatch + per-item marker** — Recipient frontmatter gains optional `Tier:` field ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}` (CR-FM-01 closed enum). At task entry, executor emits TEXT-ONLY classification header, then fires Gate-1 dispatch **once** (ME-1 binding). Per-item `(Tier: ...)` inline marker is read-only. **Priority:** Must. **AC:** AC-ATK-05 closed-enum register; AC-SM-01 Gate-1 emits `gate-1: dispatch_profile=… source=…` exactly once per task entry.

### FR-TU-2
**Critical/Trivial Path Override at row 1 (CR-7 ORDERING)** — At F1 entry block, three call sites fire in fixed order: `path_override_check()` → `tier_field_validate()` → `gate_1_dispatch()`. Critical paths (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) force tier STRICT (ANY-match); trivial paths (`*.md`, `docs/`, `*test*.py`) take override (ALL-match). CR-7 sentinel comment lands at Step 1. **Priority:** Must. **AC:** AC-ATK-01 AST/line-range check; AC-ATK-13 sentinel audit; AC-SM-07 ordering grep; AC-SM-08 verbatim diff.

### FR-TU-3
**Gate-2 verification roster widening** — Phase-Gate QA block at `task/SKILL.md:181-211` widens `verifier_roster:` to `[rf-qa, quality-engineer]` on STRICT tier. `quality-engineer` is additive only; `rf-qa` always present (ME-2 binding). **Priority:** Must. **AC:** AC-ATK-11 retroactive ME-10 or non-generalization annotation; AC-SM-02 ME traceability.

### FR-TU-4
**D15b git pre-flight (warn-and-continue)** — F1 entry block gains Layer-2 pre-flight `git status` check with five-row disposition matrix: `{clean, dirty, tool-absent, not-a-repo, error-other}` × `{WARN-CONTINUE, GRACEFUL-SKIP}`. **No HALT** (ME-3 binding; INV-01 progress guarantee). **Priority:** Must. **AC:** AC-ATK-02 5-row matrix; AC-ATK-10 input-invalid vs environment-non-ideal asymmetry.

### FR-TU-5
**TFEP baseline snapshot on disk** — Before F1 fires on STRICT/STANDARD tier, executor writes `${TASK_DIR}/research/test-baseline.yaml` containing `uv run pytest --collect-only -q` output. Disk persistence load-bearing for INV-04 across session boundaries (ME-4 tier-gated; LIGHT/EXEMPT skip). **Priority:** Must. **AC:** AC-ATK-03 four-state observation `{absent, empty, parse-fail, schema-fail}` with order pinned `os.path.exists → os.path.getsize → yaml.safe_load → schema`.

### FR-TU-6
**TFEP Prohibitions + Carve-outs (additive to F2)** — F2 catalog at `task/SKILL.md:104-117` (10 numbered entries pre-merge) absorbs 3 additive VIOLATION-level prohibitions + 3 permitted-exception carve-outs via byte-for-byte verbatim transplant from `sc-task-protocol/SKILL.md:127-142` under CR-TASK-08. Post-merge count: 13 entries. **Priority:** Must. **AC:** AC-ATK-11 disposition matrix; CR-TASK-12 verbatim diff audit.

### FR-TU-7
**TFEP escalation gradient + mid-phase rf-qa (FOURTH invocation point)** — TFEP escalation block routes to `rf-qa` mid-phase as the fourth rf-qa invocation point (alongside Phase-Gate L191, post-completion structural L221, post-completion qualitative L230). Six-step flow: halt-and-freeze → 9-field failure context YAML → forensic invocation with tier ladder (light ~5-8K → standard ~15-20K → FULL-STOP) → consume → tasklist insertion → resume `--compliance strict`. **Priority:** Must. **AC:** AC-ATK-11 F-05 paragraph-level surface-widening precedent; AC-SM-02 ME-2 traceability.

### FR-TU-8
**TFEP incident reporting side-effect file** — Per TFEP resolution, executor writes `${TASK_DIR}/research/tfep-incident-report.md` with seven-field schema (donor literal `:225-233`): `{Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts}`. Outcome enum byte-identical to donor `:232`: `{success, escalated, failed}`. **No in-task heading** — side-effect file only. **Priority:** Must. **AC:** AC-ATK-12(b) seven-field schema enumeration; AC-SM-04.

### FR-CS-1
**Step 1: Foundation row landing + CR-7 ORDERING sentinel** — Land 7 mutually-presupposing foundation rows (ME-6 M1 atomicity): CR-FM-01..03, CR-TASK-01..04, CR-7 ordering sentinel, row-1 call-site, AC-ATK-05 register. **Priority:** Must. **Atomicity:** REQUIRED. **Pre-commit gate:** CR-FM-04 ordering grep + sentinel grep.

### FR-CS-2
**Step 2: Tier classification + Gate 1 dispatch** — Land `Tier:` frontmatter contract + Gate 1 dispatch + closed-enum canonicalization (CR-FM-01) + parse-error HALT for malformed Tier (CR-TASK-02). **Priority:** Must. **Dependencies:** FR-CS-1.

### FR-CS-3
**Step 3: Path overrides + Gate-2 roster widening (FR-TU-2 + FR-TU-3)** — Lands TU-2 path overrides and TU-3 verification roster widening on STRICT. **Priority:** Must. **Dependencies:** FR-CS-1, FR-CS-2. **Pre-commit gate:** CR-FM-04 row-1 ordering + ME-2 anchor check.

### FR-CS-4
**Step 4: TU/donor verbatim diff audits + sentinel landing** — CR-TASK-12 seven-diff audit pass (6 donor strings + 1 sentinel-comment block) against donor blocks. **Priority:** Must. **Pre-commit gate:** Zero-diff against `tests/fixtures/donor-blocks/`. **Dependencies:** FR-CS-1..3.

### FR-CS-5
**Step 5: Donor command stubification (atomic, S-2 binding)** — CR-DEP-01 stubify `/sc:task` command + CR-DEP-02 sha256 baseline + CR-DEP-05 CLI residual grep + CR-DOC-01 doc redirect + CR-REF-01..02 sprint CLI re-route + CR-REF-09 sprint TUI re-route. **Priority:** Must. **Atomicity:** REQUIRED (S-2 atomic binding). **Dependencies:** FR-CS-4 + S-1 in-flight discharge.

### FR-CS-6
**Step 6: Donor skill hard-delete (atomic, S-3 binding)** — CR-DEP-03 hard-delete donor SKILL.md + CR-DEP-04 directory absence + CR-DIST-02 sync rule. **Priority:** Must. **Atomicity:** REQUIRED. **Pre-commit gate:** AC-ATK-07 rf-qa F-07 chain verifier PASS; `make verify-sync` returns 0.

### FR-CS-7
**Step 7: Sprint/pipeline integrator fix-up** — No runtime caller emits `/sc:task` post-stubification. **Priority:** Must. **Pre-commit gate:** pytest pass + AC-ATK-17 server-side pre-push hook active.

### FR-CS-8
**Step 8: Documentation rollup + mkdocs build** — CR-DOC-01 fallback (only if Step-5 gate failed with `AUTHORIZE_HOT_FIX=1`) + CR-DOC-13 R-RULE-11 scope. **Priority:** Must. **Pre-commit gate:** `mkdocs build` returns 0 broken-link warnings.

### FR-CS-9
**Step 9: Leave-as-is enforcement across buckets** — Buckets A, C, D, E, F, G, H; CR-REF-12 scoped to `[src]` + `[.claude]`; CR-REF-18 `DEPRECATION-NOTE.md` cluster root check. **Priority:** Must.

### FR-CS-10
**Step 10: Deferred-regen placeholder + frozen-pre-merge banner** — `docs/generated/*` deferred-regen placeholder with banner string in every file referencing `/sc:task` OR `sc-task-protocol`. **Priority:** Must.

### FR-CR-DEP-06
**Post-Step-6 one-shot residual-reference manifest (elevated to Must)** — Post-Step-6 script `scripts/audit/cr_dep_06_manifest.sh` writes `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` enumerating every surviving deprecation-surface string outside authorized leave-as-is buckets with per-string disposition. Pre-commit gate: residual count outside authorized buckets MUST equal **zero**. **Priority:** Must (elevated due to 144 live residual occurrences). **AC:** AC-ATK-18(d) one-shot post-Step-6 manifest; AC-ATK-14(a) CR-DEP-05 grep spec.

## Non-Functional Requirements

### NFR-INV-1
**F1 progress monotonicity** — F1 loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT preserved; no new HALT semantic mid-checklist. Environment-non-ideal MUST warn-and-continue. Per-item dispatch forbidden (ME-1). **Anchors:** `task/SKILL.md:79-98`, `:108-110`, `:115`. **Verification:** AC-ATK-02, AC-ATK-13, AC-ATK-10.

### NFR-INV-2
**F2 catalog additivity** — F2 "Prohibited Actions" catalog at `:104-117` extended only additively. Pre-merge count: 10 numbered entries; TU-6 adds 3 → post-merge ≥ 12 (target 13). No existing prohibition deleted/weakened/narrowed. **Verification:** `pytest tests/skills/task/test_prohibitions_additive.py`; AC-ATK-11.

### NFR-INV-3
**Phase-gate rf-qa floor** — `rf-qa` remains named role at all four invocation points (phase-gate, post-completion structural, post-completion qualitative, mid-phase TFEP TU-7). Widenings permitted; replacements/displacements prohibited (ME-2). **Verification:** Grep returns ≥3 matches for `subagent_type: "rf-qa"`; AC-ATK-07 F-07 chain verifier; AC-ATK-11; CR-FM-04 content-keyed anchor.

### NFR-INV-4a
**Resumability — parse layer** — Every existing MDTM TASK-* file parses and resumes cleanly at structural/parse layer post-merge: YAML frontmatter valid; checklist syntax recognized; task-log append-only; CR-FM-03 default-to-STANDARD shim handles absent `Tier:`. **Verification:** `tests/skills/task/test_compat_shim_parse.py` parametrized over live in-flight population (136 floor); AC-ATK-12(c) sunset binding.

### NFR-INV-4b
**Resumability — semantic layer (HIGHEST EXPOSURE)** — Meaningful resume path through in-flight checklist body MUST survive merge. Content-level deprecated-surface references detected at resume; executor emits Gate-1.5 token; one-shot ack gate; continue execution (warn-and-continue per ME-3, NOT HALT). **Verification:** AC-ATK-18 four sub-bindings: (a) content-layer grep at resume; (b) sprint-emit boundary content-grep; (c) one-shot ack gate via `legacy-surface-ack: 1`; (d) CR-DEP-06 manifest. Manual walkthrough on H-4 named target.

### NFR-INV-5
**Refusal-of-definition** — `Tier:` field + per-item `(Tier: ...)` marker = metadata conditioning which audits run, NOT work-definition driving runtime dispatch. Closed list of authorized per-item-marker consumers (initial: `{CR-TASK-07 baseline-skip}`); new consumer requires new ME-NN row. No embedded runtime classifier (D09b REJECTed). **Verification:** AC-ATK-05 closed-enum committed; `tests/audit/test_marker_consumers.py`; ME-1 design-review checklist.

### NFR-ME-1
**PRE-LOOP DISPATCH ONLY (Load-bearing)** — Per-item dispatch forbidden; protects INV-05. `Tier:` marker is tier-conditioned READ only. AC-ATK-05 closed-enum register is operational manifestation. **Verification:** CR-TASK-02, CR-TASK-03 acceptance.

### NFR-ME-2
**rf-qa SUPPLEMENTED NOT REPLACED (Load-bearing)** — Four invocation points (Gate-2, post-completion structural, post-completion qualitative, mid-phase TU-7). Widenings permitted; replacements prohibited. Content-keyed anchor (CR-FM-04). **Verification:** CR-TASK-05 acceptance; AC-ATK-11; AC-ATK-07.

### NFR-ME-3
**SIDE-CHANNEL ONLY, NO F1 HALT (Load-bearing)** — No new HALT semantics in F1 from TU-4/6/7/8 + TU-5. AC-ATK-02 5-row matrix → warn-and-continue. Input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry per AC-ATK-10. **Verification:** CR-TASK-08 acceptance; AC-ATK-02; AC-ATK-10; AC-ATK-18.

### NFR-ME-4
**BASELINE TIER-GATED (Ancillary)** — TU-5 baseline collection runs only on STRICT/STANDARD. HELD without per-row deltas. **Verification:** CR-TASK-07 acceptance.

### NFR-ME-5
**NO PER-ITEM EXECUTE SUBSTITUTION (Ancillary)** — TU-4 D15b accepted; explicitly REJECTs D15c per-item synthesis at execute-time. **Verification:** CR-TASK-06 acceptance.

### NFR-ME-6
**TIER FIELD + GATE 1 SHIP TOGETHER / M1 atomicity (Load-bearing)** — Seven foundation rows mutually presupposing; land in one source-tree merge. **Verification:** M1 atomicity rule audit at `merge-master.md:60`; AC-ATK-06; AC-ATK-17 server-side pre-push hook.

### NFR-ME-7
**D08 DEFERRED UNTIL PARSER SHIPS (Ancillary)** — Held as terminal DEFER. **Verification:** None re-opened; ledger row 19.

### NFR-ME-8
**D01 DEFERRED UNTIL LOADER SEMANTICS + RULE 6 SPLIT (Ancillary)** — Held as terminal DEFER.

### NFR-ME-9
**DONOR-CEREMONY DROP AUDIT (Load-bearing)** — Load-bearing for R-RULE-11 boundary protecting INV-04 + R-RULE-06. 10 named drops remain dropped. Two axes: (i) rejected-pattern; (ii) surviving-citation (CR-DEP-06). **Verification:** CR-DEP-01 soft-deprecate; CR-DEP-05 audit; R-RULE-11 audit; AC-ATK-17.

### NFR-S-1
**In-flight discharge (population-generalized)** — Any in-flight PRD/TDD task in `.dev/tasks/` whose body references donor surfaces MUST complete before Step 5 OR be snapshot-frozen with decision record. Binds live spec-named targets (`TASK-PRD-20260514-121039` LIVE 258 refs; `TASK-TDD-20260514-121250` LIVE) AND broader population at live in-flight floor (current 136). `--max-wait 14d` default. **Verification:** AC-ATK-08 three sub-bindings: (a) `--max-wait 14d` arg; (b) `scripts/embed_git_sha.py`; (c) CR-DEP-05 grep extension.

### NFR-S-2
**CLI runtime atomicity** — Step-5 commit MUST be atomic with CLI fix-forward. Server-side push-policy enforcer on landing commit at master prevents rebase-split bypass (H-2). Grep scope: `src/superclaude/cli/{sprint,cleanup_audit}/**`. **Verification:** AC-ATK-17 server-side `pre-receive` hook; fallback `scripts/atomic_step_5.sh` `flock -xn /tmp/step5.lock`.

### NFR-S-3
**Makefile sync-rule atomicity with flock** — `make sync-dev` + `make verify-sync` MUST acquire exclusive `flock` on `.claude/skills/.sync-lock`. Covers (a) forward-looking prune-loop race; (b) LIVE copy-overwrite race at `Makefile:121`. **Verification:** AC-ATK-16 pytest concurrency fixture; KPI target 0 flakes across 30 consecutive CI runs.

## Complexity Assessment

**Complexity Score:** 0.92 (HIGH)

**Scoring rationale:**
- **Scope breadth:** 19 functional + 18 NFR + 30 acceptance criteria + 5 data schemas + 10-step commit chain (~70 distinct deliverables)
- **Invariant load:** 5 load-bearing invariants (INV-01..05) with INV-04 split into parse/semantic layers (HIGHEST EXPOSURE per validation-spec §9 L285); 9 manifest exceptions (5 load-bearing, 4 ancillary)
- **Atomicity requirements:** Three coarse-grained atomic commits (Steps 1, 5, 6) under ME-6; rebase-split prevention requires server-side CI enforcement
- **Cross-cutting hazards:** 136-file in-flight floor (monotonic upward); 144 residual occurrences across 40+ files; 6 CLI emission sites; rebase-split bypass (H-2); INV-04 highest exposure
- **Adversarial validation depth:** 47 adversarial artifacts converged at 0.86 score; V1 steelman + V2 attack chain + V3 security-probe
- **Drift discipline:** 5 R-DRIFT-NN items requiring patches; R-DRIFT-03 MEDIUM is M3-blocking; `[CODE-VERIFIED]` tags require 40-char SHA suffix
- **Domain breadth:** backend skill body, CLI, testing fixtures, CI/CD hooks, documentation, governance

**Class:** HIGH — heavyweight feature merge with cross-cutting invariants, atomic commit sequencing, server-side enforcement, and load-bearing resumability across live in-flight population.

## Architectural Constraints

1. **UV-only Python operations** (CLAUDE.md absolute rule) — never `python -m` or bare `pip`.
2. **Source-of-truth discipline** — edit `src/superclaude/`, then `make sync-dev` cascades to `.claude/`.
3. **F1 loop monotonicity (INV-01)** — no new HALT semantics; environment-non-ideal warn-and-continue only.
4. **F2 catalog additivity (INV-02)** — no deletion/weakening of existing prohibitions.
5. **rf-qa floor (INV-03)** — never replaced, never displaced at any invocation surface.
6. **Resumability across session boundaries (INV-04)** — disk-resident artifacts only; in-memory state forbidden for baseline + incident reports.
7. **Refusal-of-definition (INV-05)** — `Tier:` is metadata, NOT runtime classifier; D09b embedded classifier REJECTed terminally.
8. **CR-7 ORDERING binding** — `path_override_check → tier_field_validate → gate_1_dispatch` at row-1, enforced by sentinel + AST-grade grep.
9. **ME-6 M1 atomicity** — 7 foundation rows land in single source-tree merge.
10. **Server-side push enforcement** — `.github/workflows/push-policy.yml` over local `.git/hooks/pre-push` (bypassable via `--no-verify`).
11. **Donor byte-preservation** — TU-6/7/8 byte-for-byte transplant from donor; CR-TASK-12 seven-diff audit.
12. **Outcome enum literal preservation** — `{success / escalated / failed}` byte-identical to donor `sc-task-protocol/SKILL.md:232` per ME-6.
13. **Closed-enum consumer register (AC-ATK-05)** — per-item marker consumers limited to `{CR-TASK-07 baseline-skip}`; new consumer requires ME-10+.
14. **Persona-driven design** (from PRD §7): four personas — MDTM Task Author (P-01), Sprint Executor (P-02), Framework Maintainer (P-03), Downstream Task-Runner (P-04). Anti-personas include casual residual-doc readers, post-Step-5 `/sc:task` authors, rebase-split operators, `TRIVIAL` tier consumers.
15. **Scope boundaries (from PRD §12)** — Permanently out: re-introduction of `/sc:task` non-stubified, donor SKILL.md as parallel live skill, `TRIVIAL` tier value, per-item marker as runtime dispatcher.

## Risk Inventory

1. **R-RES-01 — Tier-conditioned read boundary thin** (MEDIUM) — Wrapper-routed dispatch could describe forbidden per-item dispatch as "read." Mitigation: AC-ATK-05 closed-enum + ME-1 design-time review + CI lint step.
2. **R-RES-02 — F-05 fourth rf-qa invocation widens INV-03 surface** (MEDIUM) — Anchor `extension-point-contracts.md:11-17` NOT amended. Mitigation: AC-ATK-11 retroactive ME-10 OR one-time non-generalizing carve-out.
3. **R-RES-03 — F-04 over-escalation unbounded by design** (MEDIUM) — rf-qa queue flood risk. Mitigation: Reactive refusal threshold post queue-depth telemetry.
4. **R-RES-04 — S-1 hierarchy recorded but not decided** (MEDIUM) — `--max-wait` carrier surface ambiguous. Mitigation: AC-ATK-08 + Engineering Lead disposition pre-Step-5.
5. **R-RES-05 — F-07 procedural chain not manifest binding** (LOW) — Mitigation: AC-ATK-07 rf-qa rebound as F-07 chain-integrity verifier at Step 6 pre-commit.
6. **R-ATK-01 CR-7 markdown discipline weakness** (MEDIUM) — Closed by sentinel + AST-grade grep (AC-ATK-13).
7. **R-ATK-06 Line-number anchor brittleness** (MEDIUM) — Closed by content-hash anchors (CR-FM-04 extension).
8. **R-ATK-16 Make sync-dev worktree race** (HIGH) — Closed by `flock` (AC-ATK-16).
9. **R-ATK-17 Local pre-push bypassable via `--no-verify`** (HIGH) — Closed by server-side push-policy hook (AC-ATK-17).
10. **R-DRIFT-02 Donor anchor off-by-2** (LOW) — Patch `:127-135` → `:133-135` in 3 artifacts + CR-TASK-12 audit anchors pre-Step-4.
11. **R-DRIFT-03 Donor anchor off-by-43** (MEDIUM, M3-blocking) — Patch `:200-210` → `:157-161` in 3 artifacts + CR-TASK-12 audit anchors pre-Step-3.
12. **R-FM-01 Symlink defeat of `make verify-sync`** (LOW/HIGH) — Pre-Step-6 audit: `find -type l` returns empty.
13. **R-FM-02 Step-5 atomic flaky pytest no-progress** (MEDIUM) — Pin env vars; CI gate sign-off.
14. **R-FM-03 Parallel subagent SKILL.md conflict** (MEDIUM) — Ban parallel dispatch on `task/SKILL.md` during Step 5.
15. **R-FM-04 CI/local env divergence** (MEDIUM) — Pin env vars (PYTHONHASHSEED, locale, timezone).
16. **R-FM-05 mkdocs version drift** (MEDIUM) — Pin mkdocs version pre-Step-8.
17. **R-FM-06 `docs/generated/*` regen unscheduled** (MEDIUM) — CR-DEP-06 manifest archives weekly.
18. **R-FM-07 UTF-16 grep evasion** (LOW) — Surfaced as TDD §22 gap.
19. **R-FM-08 Donor file-rename evasion** (LOW) — CR-DEP-04 enforces directory absence not just file absence.
20. **R-OPS-02 H-4 manual operator intervention** (MEDIUM) — AC-ATK-18 + pre-flag at-risk task ID + operator runbook.
21. **Q-GAP-04 `flock` portability on macOS/BSD** (MEDIUM) — `brew install flock` or `lockfile-create` fallback documented.

## Dependency Inventory

**External Dependencies (8):**
1. `git` binary on every executing host (system PATH ≥2.0) — TU-4 pre-flight; CR-DEP-03 hard-delete
2. `uv` runtime (project-pinned) — all Python operations
3. `pytest` (via `uv run pytest`) — Pre-commit gates Steps 1/5/6; TFEP baseline collection
4. `pyyaml` — YAML frontmatter parsing; CR-FM-03 shim; AC-ATK-03 4-state observer
5. `click` (≥8.0.0) — CLI entry points
6. `rich` — CLI terminal output rendering
7. `mkdocs` (build only) — Step-8 gate (FM-05 risk: version pin required)
8. `flock(2)` / POSIX file-locking — AC-ATK-16 (BSD/macOS gap)
9. `sha256sum` (or `shasum -a 256`) — CR-DEP-02 baseline (replaces md5sum per AC-ATK-09)

**Internal Dependencies:**
- `src/superclaude/skills/task/SKILL.md` (recipient, 376 lines)
- `src/superclaude/skills/sc-task-protocol/SKILL.md` (donor, 365 lines — hard-deleted Step 6)
- `src/superclaude/commands/sc/task.md` (donor command facade, 170 lines — stubified Step 5)
- `src/superclaude/cli/sprint/process.py:124,170` (sprint emitter)
- `src/superclaude/cli/cleanup_audit/prompts.py:26,47,69,92,116` (5 cleanup-audit emitters)
- `src/superclaude/pytest_plugin.py`
- `src/superclaude/pm_agent/{confidence,self_check,reflexion}.py`
- `src/superclaude/execution/parallel.py`
- `.pre-commit-config.yaml` + `.git/hooks/` (currently `*.sample` only)
- `Makefile` targets: `make sync-dev`, `make verify-sync`, `make dev`, `make test`
- `docs/generated/*` (83 residuals across 20 files)
- `.dev/releases/backlog/` (61 residuals across 20 files)
- `.dev/tasks/to-do/TASK-PRD-20260514-121039/` (S-1 target, 258 refs, 12 files, LIVE Doing)
- `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/` (H-4, 48 occurrences/10 files)

**Cross-Team Dependencies:** None in scope (all owner-internal: Engineering Lead, Documentation/Release Owner, rf-qa Owner).

## Success Criteria

### KPI-01: TU verdict fidelity (AC-SM-01)
**Target:** 8/8 V/C/K verdicts identical byte-for-byte. **Method:** `tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match`.

### KPI-02: ME traceability (AC-SM-02)
**Target:** 9/9 ME rows trace to ≥1 CR-row. **Method:** `tests/audit/test_me_traceability.py`.

### KPI-03: INV walkthrough survival (AC-SM-03)
**Target:** 5/5 INVs re-readable with worked-example anchor. **Method:** `tests/audit/test_invariant_walkthrough.py`.

### KPI-04: F-finding anchor citations (AC-SM-04)
**Target:** 8/8 F-rows cite valid line ranges. **Method:** `tests/audit/test_f_findings_cite_anchors.py`.

### KPI-05: S-constraint HZ citations (AC-SM-05)
**Target:** 3/3 S-rows cite named hazard. **Method:** `tests/audit/test_s_constraints_cite_hz.py`.

### KPI-06: Row + step counts (AC-SM-06)
**Target:** 67 row-line-items + 10 commit steps. **Method:** `tests/audit/test_row_and_step_counts.py`.

### KPI-07: CR-FM-04 row-1 ordering (AC-SM-07)
**Target:** 2 greps × 3 function names = 6 hits in monotonic order. **Method:** `tests/skills/task/test_cr_fm_04_ordering.py`.

### KPI-08: CR-TASK-12 seven-diff (AC-SM-08)
**Target:** 7/7 zero-diffs against `tests/fixtures/donor-blocks/`. **Method:** `tests/skills/task/test_cr_task_12_donor_diffs.py`.

### KPI-09: Step-5 commit roster (AC-SM-09)
**Target:** Exact-match per `final-merge-plan.md:375`. **Method:** `tests/audit/test_step_5_commit_roster.py`.

### KPI-10: Step-6 commit roster (AC-SM-10)
**Target:** Exact-match per `final-merge-plan.md:381`. **Method:** `tests/audit/test_step_6_commit_roster.py`.

### KPI-11: Zero ledger re-proposals (AC-SM-11)
**Target:** Zero LR-REJECT-* grep hits in `final-merge-plan.md §5`. **Method:** `tests/audit/test_no_rejected_re_proposal.py`.

### KPI-12: In-flight MDTM resume + step-gate zero (AC-SM-12)
**Target:** 100% of live in-flight floor (136 union files monotonic upward) resume cleanly under CR-FM-03; gates 1/5/6 exit 0. **Method:** `tests/audit/test_step_gates.py` + live recount fixture iterating `grep -rl '/sc:task\|sc-task-protocol\|task-unified' .dev/tasks/`.

### KPI-13: Zero unmitigated AC-ATK after Phase 7.5 (K-01)
**Target:** 0 AC-ATK-01..18 in OPEN or PARTIAL state.

### KPI-14: Sprint-runner pytest pass rate (K-02)
**Target:** 100% on `tests/cli/` after CR-DEP-05 stubification.

### KPI-15: Residual occurrences eliminated (K-03)
**Target:** 144 → 0 outside authorized leave-as-is buckets.

### KPI-16: `make verify-sync` flake rate post-flock (K-04)
**Target:** 0 flakes across 30 consecutive CI runs.

### KPI-17: Post-merge audit pass rate (K-05)
**Target:** 100% PASS across 33 spec-named CR rows post-Step-6.

### KPI-18: Donor SKILL.md absent post-Step-6 (K-06)
**Target:** Both `src/` and `.claude/` copies absent.

### KPI-19: Visible command + skill surface count (K-07)
**Target:** 2 paired entries → 1 paired entry.

### KPI-20: Maintenance surface-pair count (K-08)
**Target:** 2 → 1.

**Business success criteria from PRD §19:** Internal framework feature; KPIs are technical/discipline-oriented; no revenue/conversion metrics applicable.

**Legal/Compliance from PRD §17:** No PII/PHI in `tfep-incident-report.md` schema; local-only data posture; no GDPR/CCPA/HIPAA/SOC2/PCI-DSS obligations.

## Open Questions

1. **OQ-TIER-VOCABULARY** (Open) — Confirm canonical post-merge tier vocabulary is `{STRICT, STANDARD, LIGHT, EXEMPT}` (4-tier code); retire vestigial `TRIVIAL` from spec §4. **Owner:** Engineering Lead. **Target:** Before Step 1.
2. **OQ-FM-03-SUNSET** (Open) — Confirm CR-FM-03 default-to-STANDARD shim sunset binding N. Recommended: `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`. **Owner:** Engineering Lead. **Target:** Before Step 1.
3. **OQ-F-NN-BIJECTION** (Open) — Confirm canonical F-NN ↔ TU-NN bijection once `final-merge-plan.md` content audit completes. **Target:** Before Step 7.
4. **OQ-TFEP-FIELD-COUNT** (Investigating) — Resolve TU-8 incident-report 6-vs-7 field cardinality; §7 Schema 4 commits to 7. **Target:** Before Step 4.
5. **OQ-F-05-MANIFESTIZATION** (Open) — Decide retroactive ME-10 vs one-time carve-out for F-05 per AC-ATK-11. **Target:** Before Step 4 (TU-7).
6. **OQ-PROHIBITION-DISPOSITION-MATRIX** (Open) — Decide verifier-spawned F1 disposition per AC-ATK-11 generalization. **Target:** Before Step 3 (TU-6).
7. **Q-R-DRIFT-02** (Open, LOW) — Patch donor anchor `:127-135` → `:133-135` in 3 artifacts + CR-TASK-12 anchors pre-Step-4.
8. **Q-R-DRIFT-03** (Open, MEDIUM, M3-blocking) — Patch donor anchor `:200-210` → `:157-161` in 3 artifacts + CR-TASK-12 anchors pre-Step-3.
9. **Q-R-DOC-01** (Investigating) — Downgrade from "artifact gaps" to "artifact-content verification owed"; cascading flag downgrade on AC-SM-01, -03, -04, -05, -06, -07, -09, -10, -11, -12.
10. **Q-GAP-01..12** — 12 unresolved research gaps (cleanup_audit test absence, HTML-vs-shell sentinel form, non-generalization grep audit, flock portability, helper modules, donor-block fixtures, condensation table, server-side hook hosting, incident-report template alignment, ack persistence shape, schema version uniformity).
11. **Q-GATE-1-5-SCHEMA** (Investigating) — Decide whether `gate-1.5: deleted-related-doc` is 6th canonical schema OR Schema 5 variant. Recommend fold-into-Schema-5.
12. **Q-GATE-1-5-TOKEN-COLLISION** (Open) — Pin grammar `gate-1.5: <subtype> ...` with closed subtype set.

**JTBD coverage gaps from PRD §6:** None identified — all 3 primary JTBDs and 6 related JTBDs map to functional requirements.

## Data Models and Interfaces

### DM-001: `Tier:` Frontmatter Field (Schema 1, CR-FM-01)
**Storage:** Inline in MDTM task file frontmatter (row 1 canonical position). **Cardinality:** 0..1 per task. **Type:** string (closed enumeration). **Valid values:** `STRICT | STANDARD | LIGHT | EXEMPT`. **Required:** Optional. **Default when absent:** `STANDARD` (via CR-FM-03 parse-layer shim; no file mutation). **Mutability:** Author-set at task file creation; NEVER mutated by runtime. **Validation rules:** (1) Closed-enum check by `tier_field_validate(frontmatter: dict) → str`; (2) Dispatch ordering CR-7 via `path_override_check → tier_field_validate → gate_1_dispatch`; (3) Refusal HALT on non-enum value (input-invalid pre-loop); (4) Per-item marker fallback chain. **Constraints:** NOT a runtime classifier (INV-05); NOT mutated post-creation. **Retention:** Lifetime of task file (git-tracked).

### DM-002: Per-Item Inline Marker (Schema 2, CR-FM-02 / AC-ATK-05)
**Storage:** Inline in checklist body. **Cardinality:** 0..N per task. **Marker token form:** `(Tier: <VALUE>)` parenthesized, prefix `Tier:`, single ASCII space, ASCII closing paren. **Regex:** `^- \[[ x]\] \(Tier: (STRICT\|STANDARD\|LIGHT\|EXEMPT)\) `. **Placement:** After checkbox, before item text. **Default when absent:** Falls back to Schema 1; if absent, CR-FM-03 default STANDARD. **Three-level fallback chain:** per-item → task-level → CR-FM-03 STANDARD. **Validation rules:** (1) Same closed enum as Schema 1; (2) Malformed marker is warn-and-continue, never HALT; (3) NO re-dispatch of Gate 1 (ME-1 binding). **Constraints:** Closed-enum consumer register `{CR-TASK-07 baseline-skip}` per AC-ATK-05.

### DM-003: TFEP Baseline YAML (Schema 3, AC-ATK-03)
**Storage:** File-resident at `${TASK_DIR}/research/test-baseline.yaml`. **Cardinality:** 0..1 per task (only STRICT/STANDARD tiers; CR-14). **Emission point:** First Item Protocol, pre-F1 (extension-point row 2). **Collection procedure:** (1) `uv run pytest --collect-only -q`; (2) `uv run pytest --tb=no -q`. **Persistence:** YAML file on disk; reused across resume cycles; written once at First Item Protocol entry. **Schema fields:** `schema_version: int (=1)`, `captured_at: ISO-8601 UTC string`, `tier: {STRICT, STANDARD}`, `tests: list of {test_id, status}` where `status ∈ {passing, failing}`. **Four-state observation order (CANONICAL):** `absent → empty → parse-fail → schema-fail` via `os.path.exists → os.path.getsize → yaml.safe_load → schema`. All four states → warn-and-continue per ME-3. **Retention:** Lifetime of task (git-tracked).

### DM-004: `tfep-incident-report.md` Schema (Schema 4, AC-ATK-12)
**Storage:** File-resident at `${TASK_DIR}/research/tfep-incident-report.md`. **Cardinality:** 0..1 per task (only STRICT post-fire). **Emission point:** Post-Completion Validation phase. **Trigger condition:** STRICT items AND TFEP escalation fired AND failure resolved in-task. **Donor schema source:** `sc-task-protocol/SKILL.md:220-236` (verbatim 7-field block transplant per ME-6). **Seven fields:**
1. `Trigger` (string enum-like): `pre-existing test failure | ≥3 new tests failed simultaneously | runtime exception in implementation code`
2. `Escalation count` (int): `1 | 2 | 3`
3. `Failing tests` (list of `{test_id, classification}` where `classification ∈ {pre-existing, new}`)
4. `Root cause` (free-form markdown)
5. `Solution` (free-form markdown)
6. `Outcome` (closed enum byte-identical to donor `:232`): `success | escalated | failed`
7. `Forensic artifacts` (string path or list-of-strings under `${TASK_DIR}/reviews/`)

**Constraints:** NOT a remediation-plan heading; NOT written for LIGHT/EXEMPT/STANDARD-no-TFEP; NOT written mid-loop; NOT subject to outcome-enum drift (ME-6 binds byte-for-byte). **Validation:** Outcome enum closed; all 7 fields present.

### DM-005: Gate-1.5 Emission Token (Schema 5, polymorphic, AC-ATK-18)
**Storage:** Emission-only — Task Log lines in `## Task Log / Notes` section of resumed MDTM file. **Cardinality:** 0..N per resume. **Folding decision:** Single polymorphic schema with two variants discriminated by event token (NOT 6th canonical schema).

**Variant A — `legacy-surface-reference`:** Triggered by content-grep at resume time matching `{/sc:task, sc-task-protocol, task-unified}`. Byte form: `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. Surface enum = `{/sc:task, sc-task-protocol, task-unified}`.

**Variant B — `deleted-related-doc`:** Triggered by `related_docs:` frontmatter traversal finding ENOENT path. Byte form: `gate-1.5: deleted-related-doc file=<path> action=warn-and-continue referenced_from=<path>`.

**Three-layer compat closure for INV-04:**
- L1 (Parse): CR-FM-03 frontmatter default
- L2 (Content): AC-ATK-18 body-grep → Variant A + one-shot ack
- L3 (Reference): `related_docs:` traversal → Variant B per ENOENT

**One-shot acknowledgment gate:** Single user-facing acknowledgment per resume entry recorded as `gate-1.5: ack received user=<id> ts=<ISO-8601>`. **Constraints:** NOT a HALT trigger; NOT a migration trigger; NOT bundled with `Tier:` migration; NOT subject to silent sunset.

## API Specifications

### API-001: `path_override_check`
**Signature:** `path_override_check(task_target_paths: list[str]) -> forced_stance ∈ {STRICT, LIGHT, none}`. **Position:** FIRST in CR-7 ORDERING. **Body:** Critical hard-elevate (ANY-match against `{auth/, security/, crypto/, models/, migrations/}` → STRICT); Trivial skip (ALL-match against `{*.md, docs/, *test*.py}` → LIGHT); else `none`. **Side effect:** Append 1 line to `## Task Log / Notes`. **Task Log emission:** Exactly one line per call (`path-override: forced_stance=STRICT (matched: <glob>)` | `path-override: forced_stance=LIGHT (...)` | `path-override: no-match`). **Invariant bindings:** INV-01, INV-04, INV-05.

### API-002: `tier_field_validate`
**Signature:** `tier_field_validate(frontmatter: dict) -> tier_field ∈ {STRICT, STANDARD, LIGHT, EXEMPT}`. **Position:** SECOND in CR-7 ORDERING. **Body:** Closed-enum validation; absent `Tier:` → return `STANDARD` (CR-FM-03 compat shim); non-enum value → raise `ValueError`. **Negative-set guard (rejected literals):** `{ITERATIVE, SIMPLE, IMPLEMENT, COMPLEX}`. **Side effect:** None (read-only validator). **Invariant bindings:** INV-01, INV-04, INV-05.

### API-003: `gate_1_dispatch`
**Signature:** `gate_1_dispatch(forced_stance: str, tier_field: str) -> execution_profile`. **Position:** THIRD in CR-7 ORDERING. **Resolution precedence:** (1) `forced_stance == STRICT` → STRICT; (2) `forced_stance == LIGHT` → LIGHT; (3) `none` → map `tier_field`. **ME-1 binding:** Fires once per task at entry, NOT per F1 EXECUTE iteration. **ME-6 binding:** D09a + Gate 1 ship together (CS-1 M1 atomic merge).

### API-004: Sprint CLI Emission Site (sprint/process.py:170)
**Pre-merge literal:** `f"/sc:task Execute all tasks in @{phase_file} "`. **Post-merge literal:** `f"/task Execute all tasks in @{phase_file} "`. **AC-ATK-17 boundary contract:** `assert prompt.startswith("/task Exec"); assert "/sc:task" not in prompt`.

### API-005: Cleanup-Audit Surface Scan (prompts.py:26)
**Builder:** `build_surface_scan_prompt`. **Pre-merge:** `f"/sc:task Perform a surface-level scan ..."`. **Post-merge:** `f"/task Perform a surface-level scan ..."`. **Caller:** `cli/cleanup_audit/executor.py:197` (Step G-001).

### API-006: Cleanup-Audit Structural Analysis (prompts.py:47)
**Builder:** `build_structural_analysis_prompt`. **Pre-merge:** `f"/sc:task Perform deep structural analysis ..."`. **Post-merge:** `f"/task Perform deep structural analysis ..."`. **Callers:** executor.py:211 (G-002), :228 (G-003).

### API-007: Cleanup-Audit Cross-Cutting (prompts.py:69)
**Builder:** `build_cross_cutting_prompt`. **Pre-merge:** `f"/sc:task Detect duplication, sprawl, and consolidation ..."`. **Post-merge:** `f"/task Detect duplication, sprawl, and consolidation ..."`. **Caller:** executor.py:245 (G-004).

### API-008: Cleanup-Audit Consolidation (prompts.py:92)
**Builder:** `build_consolidation_prompt`. **Pre-merge:** `f"/sc:task Consolidate audit findings ..."`. **Post-merge:** `f"/task Consolidate audit findings ..."`. **Caller:** executor.py:263 (G-005).

### API-009: Cleanup-Audit Validation (prompts.py:116)
**Builder:** `build_validation_prompt`. **Pre-merge:** `f"/sc:task Validate audit findings ..."`. **Post-merge:** `f"/task Validate audit findings ..."`. **Caller:** executor.py:278 (G-006).

### API-010: rf-qa Invocation #1 (Phase-Gate)
**Anchor:** `task/SKILL.md:191-198`. **qa_phase:** (existing rf-qa stance). **Spawn envelope (YAML):** `subagent_type: "rf-qa", mode: "bypassPermissions", qa_phase: ..., fix_authorization: true, prompt: <adversarial stance + task file + outputs + ensuring clauses + report path + zero-trust instruction>`. **Output path:** `${TASK_DIR}/reviews/qa-phase-[N]-report.md`. **Partitioning rule:** >6 output files → multiple parallel rf-qa instances with `assigned_files`.

### API-011: rf-qa Invocation #2 (Post-Completion Structural)
**Anchor:** `task/SKILL.md:219-226`. **qa_phase:** `"report-validation"`. **Output path:** `${TASK_DIR}/reviews/qa-final-validation-report.md`. **Additional prompt fields:** ALL outputs across ALL phases; cross-phase consistency.

### API-012: rf-qa-qualitative Invocation #3 (Post-Completion Operational)
**Anchor:** `task/SKILL.md:228-239`. **qa_phase:** `"task-qualitative"`. **Output path:** `${TASK_DIR}/reviews/qa-qualitative-review.md`. **Additional prompt fields:** TARGET_FILE_LIST, modified sources, CLAUDE.md conventions, research dir, `document_type: "Executed Task File"`, 15-item checklist.

### API-013: rf-qa Invocation #4 (Mid-phase TFEP, NEW per TU-7)
**Anchor:** NEW inside TFEP block between L179 and L181. **qa_phase:** `"tfep-incident-[N]"`. **Output path:** `${TASK_DIR}/reviews/qa-tfep-incident-[N]-report.md`. **Additional prompt fields:** TFEP trigger classification; baseline diff; failing tests list; escalation gradient stage. **Authoritative count:** 4 rf-qa invocations post-merge (3 preserved + 1 new TU-7).

### API-014: Donor Command Stubification (CR-DEP-01)
**Source line:** `src/superclaude/commands/task.md:100`. **Current:** `  > Skill sc:task-protocol`. **Post-merge target:** `  > Skill task` (Form 1, synth-05 binding). **Adjacent rewrites:** 8 brand-name occurrences at lines 12, 19, 41, 106, 117, 128, 139, 169. **HTML marker decision:** Preserve `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` tokens verbatim (test-fixture anchor; load-bearing semantic token).

## Component Inventory

### COMP-001: TU-1 — Tier field parser + Gate 1 dispatch
**Kind:** Pre-loop classifier (read-only). **LOC:** ~20 post-merge. **Insertion target:** (a) row 0 CR-7 ORDERING sentinel; (b) new subsection after L73 `### Tier Field Parser + Gate 1 Classification`; (c) +1 bullet inside F1 EXECUTE dispatch L89-96. **Pattern source:** `commands/task.md:55,61,104` closed enum + `sc-task-protocol/SKILL.md:9` enum. **INV protected:** INV-04 (parse layer), INV-05. **ME bound:** ME-1, ME-6. **CR-row author:** CR-FM-01..03, CR-TASK-01..03.

### COMP-002: TU-2 — Path override (critical/trivial)
**Kind:** Pre-loop classifier (read-only). **LOC:** ~10. **Insertion target:** (a) row 0 sentinel (shared with TU-1); (b) new subsection adjacent to TU-1 `### Critical / Trivial Path Override`. **Pattern source:** `sc-task-protocol/SKILL.md:121` (5 critical globs) + `:123` (3 trivial globs). **INV protected:** INV-05. **ME bound:** ME-6. **CR-row author:** CR-TASK-01 + CR-7 ordering sentinel.

### COMP-003: TU-3 — Verification roster widening
**Kind:** Phase-gate + post-completion expansion (additive spawn). **LOC:** ~14. **Insertion target:** (a) +Step 3b inside L191-198; (b) +Step 1b inside L219-226; (c) +Step 4 verdict-processing edit; (d) +bullet in agent-type list L290-299. **Pattern source:** `sc-task-protocol/SKILL.md:89` (quality-engineer) + `:116` (STRICT routing). **INV protected:** INV-03 (rf-qa floor preserved). **ME bound:** ME-2. **CR-row author:** CR-TASK-05.

### COMP-004: TU-4 — Git pre-flight Task Log emission
**Kind:** F1 pre-execution side-channel (5-row warn-and-continue). **LOC:** ~12. **Insertion target:** New subsection between L102 and L104. **Pattern source:** `sc-task-protocol/SKILL.md:82` ("Verify git working directory clean"). **INV protected:** INV-01 (additive surface, no new HALT). **ME bound:** ME-3. **CR-row author:** CR-TASK-06.

### COMP-005: TU-5 — TFEP baseline snapshot
**Kind:** Pre-F1 side-effect file emitter (YAML). **LOC:** ~10 + on-disk `${TASK_DIR}/research/test-baseline.yaml`. **Insertion target:** (a) new subsection between L179 and L181; (b) +bullet inside Session Resumption Step 4. **Pattern source:** `sc-task-protocol/SKILL.md:144-153` (donor in-memory → file-resident per INV-04). **INV protected:** INV-04. **ME bound:** ME-3, ME-4. **CR-row author:** CR-TASK-07.

### COMP-006: TU-6 — TFEP prohibitions + carve-outs
**Kind:** F2 catalog additive insertion + carve-out subsection. **LOC:** +3 bullets (F2: 10 → 13) + ~6 lines carve-out. **Insertion target:** (a) append after L117; (b) carve-out subsection inside TFEP block. **Pattern source:** `sc-task-protocol/SKILL.md:133-135` (3 VIOLATION rules byte-for-byte) + `:137-140` (3 permitted exceptions). **INV protected:** INV-02, INV-01. **ME bound:** ME-3. **CR-row author:** CR-TASK-08, CR-TASK-12.

### COMP-007: TU-7 — TFEP escalation trigger (mid-phase rf-qa)
**Kind:** F1-side-channel escalation router; 4th rf-qa invocation surface. **LOC:** ~15. **Insertion target:** New subsection inside TFEP block. **Pattern source:** `sc-task-protocol/SKILL.md:157-161` (3 MUST-escalate triggers). **INV protected:** INV-03 (additive rf-qa surface; ME-2 preserved). **ME bound:** ME-2, ME-3. **CR-row author:** CR-TASK-09. **AC-ATK-11 carve-out:** one-time non-generalizing.

### COMP-008: TU-8 — TFEP incident report
**Kind:** Post-resolution side-effect file emitter (Markdown). **LOC:** ~12 + on-disk `${TASK_DIR}/research/tfep-incident-report.md`. **Insertion target:** New subsection inside TFEP block. **Pattern source:** `sc-task-protocol/SKILL.md:222-234` (7-field schema byte-for-byte; Outcome enum literal `:232`). **INV protected:** INV-04. **ME bound:** ME-3, ME-6. **CR-row author:** CR-TASK-10, CR-TASK-12.

## Testing Strategy

### Test Pyramid
- **Unit Tests** (`@pytest.mark.unit`): >80% coverage per `superclaude/pm_agent/` module. Tools: `uv run pytest`, `pytest-cov`.
- **Integration Tests** (`@pytest.mark.integration`): Every CR-TASK-NN, CR-FM-NN, CR-DEP-NN row has ≥1 integration test.
- **AC-ATK Tests:** 1 test per AC-ATK-01..18 (18 tests; 100% coverage required).
- **AC-SM Tests:** 1 test per AC-SM-01..12 (12 tests; 100% coverage required).
- **Invariant Survival Walkthrough:** 5 paragraphs (one per INV-01..INV-05) at `invariant-survival-walkthrough.md` + `tests/audit/test_invariant_walkthrough.py`.
- **CI Continuous:** 7 intra-spec audits on every PR.

### TEST-001: AC-ATK-01 (Row1 call order)
**Path:** `tests/skills/task/test_row1_call_order.py::test_path_override_first`. **Asserts:** AST/grep order: `path_override_check → tier_field_validate → gate_1_dispatch`. **Gate:** Step-4 pre-commit.

### TEST-002: AC-ATK-02 (Git dirty dispatch)
**Path:** `tests/skills/task/test_git_dirty_dispatch.py::test_5_row_matrix`. **Asserts:** Parametrize R1..R5; for each: exact Task Log line; action token; proceed sentinel TRUE; no HALT. **Gate:** Step-2 pre-commit.

### TEST-003: AC-ATK-03 (Baseline trinary 4-state)
**Path:** `tests/skills/task/test_baseline_trinary.py::test_4_state_observer`. **Asserts:** Parametrize `{absent, empty, parse-fail, schema-fail}`; observer order pinned (`exists → getsize → safe_load → schema`); all four → `classification=new-all`. **Gate:** Step-3 pre-commit.

### TEST-004: AC-ATK-04 (Condensation table)
**Path:** `tests/audit/test_condensation_table.py::test_79_to_67_to_65`. **Asserts:** 6 bucket rows sum to 79 row-instances → 65 distinct CR-IDs → 67 PASS-line-items; names 2 duplicate CR-IDs.

### TEST-005: AC-ATK-05 (Marker consumers closed set)
**Path:** `tests/audit/test_marker_consumers.py::test_closed_consumer_set`. **Asserts:** Only authorized consumer = `{CR-TASK-07 baseline-skip}`; new consumer requires new ME-NN.

### TEST-006: AC-ATK-06 (Donor diffs seven zero-diffs)
**Path:** `tests/skills/task/test_cr_task_12_donor_diffs.py::test_seven_zero_diffs`. **Asserts:** 7 `diff` invocations return zero against `tests/fixtures/donor-blocks/*.txt`.

### TEST-007: AC-ATK-07 (rf-qa F-07 chain)
**Path:** `tests/audit/test_rf_qa_step6_gate.py::test_chain_links`. **Asserts:** 5 chain anchors verified; rf-qa returns PASS pre-Step-6.

### TEST-008: AC-ATK-08 (Git SHA embedding)
**Path:** `tests/scripts/test_embed_git_sha.py::test_idempotent` + `tests/audit/test_cr_dep_05_grep.py::test_post_step5_stale_verification`. **Asserts:** Every `[CODE-VERIFIED]` tag carries `(git-sha: <SHA>)` suffix; idempotent.

### TEST-009: AC-ATK-09 (sha256 digests)
**Path:** `tests/skills/task/test_cr_task_11_digest.py::test_sha256_matches_baseline`. **Asserts:** All 3 audit digests use sha256 (NOT md5).

### TEST-010: AC-ATK-10 (Pre-loop HALT policy 2-category)
**Path:** `tests/skills/task/test_preloop_halt_policy.py::test_2_category_table`. **Asserts:** Input-invalid Tier → HALT exit-code 2; environment-non-ideal git-dirty → WARN-CONTINUE exit-code 0.

### TEST-011: AC-ATK-11 (ME-10 carve-out)
**Path:** `tests/audit/test_me10_carve_out.py::test_me10_authored_or_annotated`. **Asserts:** ME-10 row authored OR explicit non-generalization annotation present.

### TEST-012: AC-ATK-12 (Incident schema 7 fields + canonical enum)
**Path:** `tests/skills/task/test_tfep_incident_schema.py::test_7_fields` + `tests/audit/test_cr_fm_01_canonical.py::test_canonical_table`. **Asserts:** Schema enumerates exactly 7 fields; Tier enum closed `{STRICT, STANDARD, LIGHT, EXEMPT}`.

### TEST-013: AC-ATK-13 (Row1 ordering grep)
**Path:** `tests/skills/task/test_row1_ordering_grep.py::test_executable_grep`. **Asserts:** Both CR-FM-04 greps return three names in monotonic order.

### TEST-014: AC-ATK-14 (CR-DEP-05 grep 4 sub-resolutions)
**Path:** `tests/audit/test_cr_dep_05_grep.py::test_4_sub_resolutions`. **Asserts:** (a) grep scope correct; (b) cluster root named; (c) gate at Step-6 pre-commit; (d) CR-DOC-13 scope widened.

### TEST-015: AC-ATK-15 (CR-DOC-01 atomic Step-5)
**Path:** `tests/audit/test_cr_doc_01_step.py::test_landed_with_dep_01`. **Asserts:** Step-5 commit roster includes both `commands/task.md` and `docs/user-guide/commands.md`; Step-8 fallback only with `AUTHORIZE_HOT_FIX=1`.

### TEST-016: AC-ATK-16 (Make sync-dev flock)
**Path:** `tests/audit/test_make_sync_dev_flock.py::test_concurrent_worktree`. **Asserts:** Two parallel `make sync-dev` subprocesses; flock held during prune; post-prune dir match expected.

### TEST-017: AC-ATK-17 (Server-side pre-receive hook)
**Path:** `tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected`. **Asserts:** Fabricate rebase-split commit pair; hook exits non-zero on intermediate broken state.

### TEST-018: AC-ATK-18 (Resume content audit + sprint-emit + manifest)
**Path:** `tests/skills/task/test_cr_fm_03_resume_grep.py::test_emission_token_format` + `tests/cli/test_sprint_emit_legacy_grep.py::test_block_emit_on_match` + `tests/audit/test_cr_dep_06_manifest.py::test_manifest_present`. **Asserts:** (a) Gate-1.5 emission canonical grammar; (b) sprint-emit blocks on content match; (c) post-Step-6 manifest enumerates ≥144 residuals.

### TEST-019: AC-SM-01 (V/C/K byte-match)
**Path:** `tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match`. **Asserts:** 8/8 V/C/K verdicts identical byte-for-byte against `transfer-manifest.md §4`.

### TEST-020: AC-SM-02 (ME traceability)
**Path:** `tests/audit/test_me_traceability.py::test_each_me_has_cr_row`. **Asserts:** For ME ∈ {1..9}, ≥1 grep hit in `final-merge-plan.md §5` OR §6.

### TEST-021: AC-SM-03 (Invariant walkthrough)
**Path:** `tests/audit/test_invariant_walkthrough.py::test_inv_1_through_5_re_readable`. **Asserts:** For INV ∈ {1..5}, ≥1 grep hit with associated worked-example anchor.

### TEST-022: AC-SM-04 (F-findings cite anchors)
**Path:** `tests/audit/test_f_findings_cite_anchors.py::test_each_f_row_has_artifact_anchor`. **Asserts:** For F ∈ {01..08}, ≥1 line-range cite.

### TEST-023: AC-SM-05 (S-constraints cite HZ)
**Path:** `tests/audit/test_s_constraints_cite_hz.py::test_s_1_cites_hz03 + test_s_2_cites_hz06_hz07 + test_s_3_cites_hz14`. **Asserts:** 3/3 S-rows cite HZ-NN.

### TEST-024: AC-SM-06 (Row + step counts)
**Path:** `tests/audit/test_row_and_step_counts.py::test_67_rows_in_master + test_10_steps_in_sequence`. **Asserts:** 67 row-line-items + 10 commit steps.

### TEST-025: AC-SM-07 (CR-FM-04 ordering)
**Path:** `tests/skills/task/test_cr_fm_04_ordering.py::test_row_1_order + test_row_10_order`. **Asserts:** 2 greps × 3 function names = 6 hits monotonic; 0 reorders.

### TEST-026: AC-SM-08 (CR-TASK-12 seven-diff)
**Path:** `tests/skills/task/test_cr_task_12_donor_diffs.py::test_6_donor_plus_1_sentinel`. **Asserts:** 7 diffs return zero (6 donor + 1 sentinel block).

### TEST-027: AC-SM-09 (Step-5 commit roster)
**Path:** `tests/audit/test_step_5_commit_roster.py::test_exact_file_list`. **Asserts:** `git log --name-only <step5-commit>` set-equal to `final-merge-plan.md:375` roster.

### TEST-028: AC-SM-10 (Step-6 commit roster)
**Path:** `tests/audit/test_step_6_commit_roster.py::test_exact_file_list`. **Asserts:** Same for Step 6 against `:381`.

### TEST-029: AC-SM-11 (Zero ledger re-proposal)
**Path:** `tests/audit/test_no_rejected_re_proposal.py::test_zero_ledger_re_introductions`. **Asserts:** For every LR-REJECT-* in `rejected-features-ledger.md`, zero grep hits in `final-merge-plan.md §5`.

### TEST-030: AC-SM-12 (Step gates + in-flight resume)
**Path:** `tests/audit/test_step_gates.py + tests/skills/task/test_in_flight_mdtm_resume.py::test_step_1_gate_zero + test_step_5_gate_zero + test_step_6_gate_zero + test_live_inflight_mdtm_resume_clean`. **Asserts:** Gates 1/5/6 exit zero; **fixture iterates LIVE in-flight count at gate-execution time** (NOT hardcoded 25/96/132); 100% resume cleanly under CR-FM-03 shim.

### Test Environments
- Local (developer machine): tmp_path fixtures + `tests/fixtures/donor-blocks/`
- Pre-commit hooks (Steps 1-6): Local working tree + frozen fixtures
- CI (GitHub Actions): Synthetic + intra-spec audits
- Server-side pre-receive (push-time): Landing commit diff
- Resume-time (per task): Live in-flight MDTM file (Gate-1.5)
- Sprint-emit boundary (per tasklist): Rendered tasklist body

## Migration and Rollout Plan

### MIG-001: Step 1 — M1 Atomic Foundation
**Rows (atomic-7 per ME-6 / CR-7 / CR-9):** CR-FM-03 shim, CR-FM-01 + CR-FM-02 canonicalization, CR-TASK-01..04 row-1 ordering, CR-7 ORDERING sentinel, AC-ATK-05 closed-enum register, `tier_field_validate()` + `path_override_check()` + `gate_1_dispatch()` helper modules. **Exit Criteria:** Step-1 pre-commit gate returns 0; AC-SM-07 cleared; AC-SM-12 100% in-flight resume PASS against 136-file population. **Rollback Granularity:** Coarse (atomic-by-design); single revert reverses 7 rows.

### MIG-002: Step 2 — TU-3 + TU-4
**Deliverables:** Gate 2 widened roster `[rf-qa, quality-engineer]` (ME-2 preserved); D15b Layer 2 git pre-flight (warn-and-continue, 5-row matrix per AC-ATK-02); `tier_preflight_git_status()` helper. **Exit Criteria:** AC-ATK-02 5-row dispatch test PASS; AC-ATK-10 two-category fixture PASS. **Rollback Granularity:** Fine (per-CR).

### MIG-003: Step 3 — M3 TFEP Cluster
**Deliverables (R-DRIFT-03 PATCH PRECONDITION):** R-DRIFT-03 anchor patch applied to 3 artifacts + CR-TASK-12 anchors BEFORE this commit; TU-5 TFEP baseline on disk; TU-6 Prohibitions + Carve-outs APPEND-only to F2 (10 → 13); CR-TASK-07..10 acceptance criteria; TU-7 4th rf-qa invocation point; TU-8 incident reporting side-effect file. **Exit Criteria:** AC-ATK-03 4-state observer PASS; AC-ATK-12(b) 7-field schema fixture PASS; AC-CR-TASK-09-F04 over-escalate PASS. **Rollback Granularity:** Fine (per-CR within DM-7/DM-9 order).

### MIG-004: Step 4 — Donor Verbatim Diff Audit Window
**Deliverables (R-DRIFT-02 PATCH PRECONDITION):** R-DRIFT-02 anchor patch applied to 3 artifacts + CR-TASK-12 anchors BEFORE this commit; CR-TASK-12 seven-diff audit fixture at `tests/fixtures/donor-blocks/`; AC-ATK-06 frozen-fixture snapshot script. **Exit Criteria:** CR-TASK-12 returns 7 zero-diffs (AC-SM-08 gate). **Rollback Granularity:** Fine.

### MIG-005: Step 5 — Soft-Deprecation (S-2 Atomic Binding)
**Deliverables (ATOMIC):** CR-DEP-01 donor stubification; CR-DEP-02 sha256 digest baseline; CR-DEP-05 CLI residual grep + cleanup_audit/prompts.py emission re-route; CR-DOC-01 docs rewrite (atomic per AC-ATK-15); CR-REF-01..05 CLI residual deletion; `docs/condensation-table.md` (Q-GAP-08); In-flight target population frozen (S-1 binding). **Exit Criteria:** AC-ATK-15 Step-5 atomicity test PASS; AC-ATK-17 server-side pre-receive hook PASS (no rebase-split bypass); AC-SM-09 commit roster equality test PASS. **Rollback Granularity:** Coarse (atomic, S-2 binding).

### MIG-006: Step 6 — Hard-Delete (S-3 Atomic Binding)
**Deliverables (ATOMIC; INV-04 highest exposure):** CR-DEP-03 donor SKILL.md hard-delete; CR-DEP-04 directory absence + `make sync-dev` prune; AC-ATK-07 rf-qa F-07 chain verifier PASS (pre-hard-delete); AC-ATK-16 `flock` guard on `make sync-dev` (Q-GAP-04 portability); CR-DEP-06 residual manifest written to `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` with all 144 residuals dispositioned. **Exit Criteria:** AC-SM-10 Step-6 commit roster PASS; `make verify-sync` returns 0; Donor `sc-task-protocol/` directory absent from both `src/` and `.claude/`; CR-DEP-06 manifest: residual count outside authorized buckets = 0. **Rollback Granularity:** Destructive-by-default (roll FORWARD preferred over revert).

### MIG-007: Step 7 — Invariant Survival Walkthrough Audit
**Deliverables:** AC-SM-03 walkthrough re-read (5 of 5 INVs); AC-SM-04 8 of 8 F-rows cite valid line ranges; Q-2 content audit complete (downgrades R-DOC-01). **Rollback Granularity:** Fine (annotation/mirror-refresh).

### MIG-008: Step 8 — Documentation Rollup
**Deliverables:** CR-DOC-02..09, CR-DOC-11 partial; mkdocs build returns 0 broken-link warnings; CR-DOC-13 R-RULE-11 audit clean. **Caveat FM-05:** mkdocs version pin recommended pre-Step-8. **Rollback Granularity:** Fine.

### MIG-009: Step 9 — CR-DEP-06 Residual Manifest One-Shot
**Deliverables:** Post-Step-6 one-shot residual-reference manifest finalized; AC-ATK-18(d) closure. **Rollback Granularity:** Fine.

### MIG-010: Step 10 — Audit Closure
**Deliverables:** CR-DOC-10..12 final; CR-DEFER-T06.04 ack; AC-SM-01..12 audits re-run from clean checkout; K-01..K-08 baseline measurements taken. **Rollback Granularity:** Fine.

### Feature Flags
- **CR-FM-03 shim** (default-to-STANDARD): Always-on from Step 1; sunset TBD per OQ-FM-03-SUNSET (recommended `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`). **Cleanup Date:** After CR-MIGR-FM-03 migration ships AND 50 generations AND 90 days post-Step-6.
- **gate-1.4 shim-status counter**: Always-on from Step 1; co-removed with CR-FM-03 shim.
- **gate-1.5 legacy-surface content audit (AC-ATK-18)**: Always-on; indefinite (semantic-layer INV-04 guarantee).
- **Server-side pre-push hook (AC-ATK-17)**: Activates at Step 8; indefinite (CLI surveillance).

### Sequencing Constraints
- **S-1**: In-flight discharge — live spec-named targets (`TASK-PRD-20260514-121039`, `TASK-TDD-20260514-121250`) + broader 132/136-file population must complete OR snapshot-freeze before Step 5; `--max-wait 14d` default.
- **S-2**: CLI runtime atomicity — Step-5 commit atomic with CLI fix-forward; server-side push-policy enforcer on landing commit.
- **S-3**: Makefile sync-rule atomicity — `make sync-dev` + `make verify-sync` acquire exclusive `flock` on `.claude/skills/.sync-lock`.

### Rollback Decision Criteria
- Pre-commit gate failure at any step → block commit
- Post-commit pytest red after Step 5/6 → revert immediately if within atomic boundary; roll forward with hotfix if past Step 6
- `make verify-sync` non-zero post-Step-6 → S-3 atomicity violated; revert or roll forward
- R-RULE-11 audit detects re-introduced REJECTed pattern → revert offending CR-row; re-audit
- In-flight INV-04 semantic failure (H-4 transition-to-Blocked) → add per-task `--compliance strict` override; do NOT revert Step 6

## Operational Readiness

### OPS-001: Critical Path Override Invocation (Runbook R1)
**Symptoms:** F1 dispatched to STRICT tier for item under `auth/`/`security/`/`crypto/`/`models/`/`migrations/` despite frontmatter `Tier:` claiming `LIGHT`/`EXEMPT`. **Diagnosis Steps:** (i) Read Task Log for `path_override fired: matched <pattern>`; (ii) confirm CR-7 ORDERING sentinel still present at row-1 site via grep; (iii) verify `path_override_check()` executed FIRST per CR-FM-04 ordering. **Resolution:** Honor override (STRICT wins); if author insists on LIGHT/EXEMPT, require explicit override-suppression annotation with rf-qa sign-off; never silently bypass CR-7. **Escalation:** rf-qa within 1h if author requests suppression; Engineering Lead within 4h if pattern set itself disputed. **Prevention:** Operator training on CR-7 ORDERING binding; sentinel/AST grep audit at Step-4 pre-commit.

### OPS-002: Gate-1.5 Emission Triage (Runbook R2)
**Symptoms:** Task resume emits `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. **Diagnosis Steps:** (i) Confirm token grammar matches canonical AC-ATK-18(b); (ii) check `legacy-surface-ack: 1` in task frontmatter; (iii) inspect matched symbol against CR-DEP-06 residual manifest disposition. **Resolution:** Acknowledge via one-shot ack; DO NOT HALT (ME-3); patch matched surface only if disposition = `action=violation`. **Escalation:** If matched surface = `bucket=src`, page Engineering Lead within 30 min (manifest expected to be 0 in `src/`). **Prevention:** Weekly CR-DEP-06 manifest re-emit; sprint-emit boundary content-grep blocks regressions.

### OPS-003: Tier Mis-Classification Recovery (Runbook R3)
**Symptoms:** Item executes under wrong tier (e.g., STRICT item dispatched to STANDARD profile). **Diagnosis Steps:** (i) Read frontmatter `Tier:`; (ii) read per-item marker; (iii) compute expected tier per 3-level fallback (per-item → task-level → STANDARD default); (iv) compare to actual dispatch in Task Log. **Resolution:** If dispatch wrong, log incident at `${TASK_DIR}/research/tfep-incident-report.md` (7-field schema); fix canonicalization (case, whitespace) at source; if canonicalization rule itself wrong, page Engineering Lead. **Escalation:** Engineering Lead within 1h if root cause is parser bug; rf-qa for human-author errata. **Prevention:** CR-FM-01 canonicalization table; closed-enum validation at task entry.

### OPS-004: TFEP Escalation Handling (Runbook R4)
**Symptoms:** F-05 authorized TFEP-escalation invocation logged; baseline classifies ≥1 new-test fail. **Diagnosis Steps:** (i) Confirm baseline state at `${TASK_DIR}/research/test-baseline.yaml` (4-state observer per AC-ATK-03); (ii) read TFEP incident report; (iii) classify against carve-outs (3 permitted exceptions per TU-6); (iv) confirm prohibition disposition matrix routing. **Resolution:** If baseline parse-fail or schema-fail → treat as `classification=new`; if carve-out applies → record exception in incident report; if neither → HALT item (input-invalid HALT-permitted per AC-ATK-10) and route to rf-qa for adjudication. **Escalation:** rf-qa within 30 min for adjudication. **Prevention:** AC-ATK-03 4-state observation; tier-gated baseline collection (ME-4).

### OPS-005: In-Flight Resume Triage (Runbook R5)
**Symptoms:** Post-merge resume of in-flight MDTM task (136-file floor); may emit Gate-1.5 token, may ENOENT on `related_docs:` paths. **Diagnosis Steps:** (i) Run CR-FM-03 default-to-STANDARD shim (`gate-1: dispatch_profile=STANDARD source=default`); (ii) Gate-1.5 content grep over task body; (iii) traverse `related_docs:` paths with `find`; emit `gate-1.5: deleted-related-doc` on ENOENT. **Resolution:** Warn-and-continue; set `legacy-surface-ack: 1` if author has reviewed; NEVER HALT mid-resume (INV-04 highest-exposure protector). **Escalation:** Engineering Lead within 4h if resume blocked by parser bug; never block on `related_docs:` ENOENT. **Prevention:** AC-ATK-18 4-part fan-out closure; CR-DEP-06 manifest archives weekly to `docs/generated/`.

### On-Call Expectations
- **On-call team:** rf-qa (primary; Phase-Gate QA + post-completion + TFEP escalation); Engineering Lead (secondary; parser bugs, S-1/S-2/S-3 atomicity violations, V3 security-probe regressions); DevOps (CI hook failures, server-side pre-receive misfires).
- **Expected page volume:** <2 pages/week at steady state post-Phase-7.5; spike expected during Step 5/6 windows.
- **Required response time:** rf-qa: ack 15 min, mitigate 60 min; Engineering Lead: ack 30 min (5 min for atomicity violations); DevOps: ack 30 min.

### Observability — Logging Catalogue
- **Task Log emission schema:** Append-only lines to `## Task Log / Notes` section of MDTM file (preserves INV-04 resumability).
- **Per-TU emission prefixes:** TU-1 `gate-1:`, TU-2 `path-override:`, TU-4 `gate-1.5: pre-flight`, TU-5 `tfep: baseline=`, TU-6 `tfep: prohibition-refusal`, TU-7 `tfep: escalation-trigger`, TU-8 `tfep: incident-report`, AC-ATK-18 `gate-1.5: legacy-surface-reference`, CR-FM-03 `gate-1.4: shim-status`.
- **Single-line emission grammar (BNF-ish):** `<prefix>: <facet>=<value> [<facet>=<value> ...] [reason=<short-token>]`.

### Alerts
- **Pre-receive hook reject on master/integration push:** Critical — author re-composes commit (atomic CR-DEP-01 + CR-DOC-01 + CR-REF-01..05); re-push.
- **Step-5 pre-commit gate fail:** Critical — author fixes failing tests; hot-fix Step-8 fallback requires `AUTHORIZE_HOT_FIX=1`.
- **Resume legacy-surface match:** Warning — operator acknowledges via one-shot ack gate (idempotent).
- **Sprint-emit block-emit:** Warning — author corrects tasklist source; re-emit.
- **`make verify-sync` non-zero:** Critical — run `make sync-dev`; re-verify; manual reconcile under R-RULE-10 if diff persists.
- **TFEP incident-report schema drift on Post-Completion:** Warning — orchestrator re-routes to rf-qa; re-author report; re-validate.

### Capacity Planning
- In-flight MDTM file count (CR-FM-03 shim coverage): 136 → 200-300 (6mo) → 400-600 (12mo); scaling trigger: emission rate >10/day → batch ack pass.
- CR-DEP-06 residual manifest entries: 144 → 50-100 (6mo) → <50 (steady state); audit if residual count grows post-Step-6.
- Pre-commit gate wall-clock: <30s → <45s → <60s; trigger: if >90s, batch by Step.
- `make sync-dev` flock-guarded duration: <5s → <10s → <15s; trigger: investigate skill directory bloat if >30s.
- TFEP incident-report file count: 0 (pre-merge) → 5-20/mo (steady) → 10-40/mo; trigger: if >50/mo, surface as systemic test-failure trend.
