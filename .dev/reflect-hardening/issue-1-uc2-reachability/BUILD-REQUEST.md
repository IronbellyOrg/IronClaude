# BUILD_REQUEST — MDTM tasklist for FR-RSR (sc:reflect UC-2 runtime-surface reachability escalation)

## GOAL

Build an MDTM tasklist that implements the **FR-RSR** feature (additive UC-2 runtime-surface reachability
escalation for the `sc-reflect-protocol` skill). Use **Template 02 (complex)**.

## GUIDING DOCUMENT (authoritative — drives scope, structure, sequence, DoD)

- **TDD:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md`

The TDD is the design of record. Derive from it: the task set, the 12 key design decisions (§6.4 D1–D12),
the reconciled data models (§7.1), the new/modified **file inventory** (§18.2), the **rollout order** (§19.3
P1–P6 / §23.2), the **Definition of Done + Release Checklist** (§24), and the risk register (§20). When the TDD
and the spec ever disagree, **the TDD wins** (the two were reconciled in a prior reflect pass; they should agree).

## SECONDARY REFERENCE (mine for detail; NEVER expand scope beyond the TDD)

- **Spec:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-1-uc2-reachability/spec.md`

Use the spec **only** to enrich tasks the TDD already defines, for these six things the TDD intentionally does
not fully duplicate:

1. **Per-FR acceptance criteria (spec §3 `- [ ]` boxes).** Copy each FR's acceptance-criteria checkboxes into the
   corresponding task's verification checklist. This is the single highest-value use of the spec — the TDD's
   §5.1 FR-map points to these but the literal `- [ ]` items live in the spec.
2. **Worked Gherkin scenarios (spec §2.3).** The two before/after traces are the literal **fail-before /
   pass-after** fixture content for the eval task: scenario 1 → `uc2-unwired-surface-passes` (headline, active),
   scenario 2 → `uc2-surface-dynamic-dispatch` (degrade, never Regression).
3. **NFR measurement methods (spec §6 table).** Use the "Measurement" column as each NFR's verification step
   (e.g. NFR-RSR.2 = "re-run the fixture twice, assert byte-identical `runtime-surface-ledger.yaml`").
4. **Degrade-oracle + lang-table content (spec FR-RSR.3 + §1.1 evidence + OQ-RSR.1/2).** The oracle MUST cover
   categories (a) decorator routes, (b) `[project.scripts]`/entry-points, (c) registry/DI/string-dispatch,
   (d) reflection/dynamic-import; and MUST NOT false-flag this repo's own `pyproject.toml:67–69`
   (`superclaude`, `ic`). This is the content the `refs/runtime-surface.md` task enumerates.
5. **Risk → mitigation register (spec §7).** Attach the relevant mitigation as a per-task guard note (esp. the
   silent-no-op risk and the false-`UNREACHED→Regression`-rollback risk).
6. **Blocker ordering (spec §10 "For sc:tasklist").** "Each FR maps to one task. FR-RSR.3 (degrade oracle) and
   FR-RSR.4 (rootwalk) are the highest-risk tasks and MUST land before any UNREACHED verdict is emittable —
   gate them as blockers of FR-RSR.2's UNREACHED path. The contract task (FR-RSR.7) is parallelizable with the
   sweep task. The eval task (FR-RSR.10) is terminal and is the acceptance gate."

## SCOPE & PROJECT CONVENTIONS (non-negotiable)

- **Source of truth = `src/superclaude/` ONLY.** Never edit `.claude/` mirrors. Eval fixtures live under
  `.dev/eval-workspaces/sc-reflect/`. The `runtime-surface-ledger.yaml` is a per-run runtime artifact under
  `<output>/artifacts/`, never committed.
- **After every `SKILL.md` / `refs/` edit:** run `make sync-dev` then `make verify-sync` (must exit 0). This is
  its own terminal task that depends on all SKILL.md/refs edits.
- **UV only** for any Python (the eval grader). Before any Python is pushed, run
  `uv run ruff format --check src/ tests/` (green `make lint` ≠ green CI format).
- This is an **additive minor** change: `contract_version` 1.5.0 → 1.6.0; no existing field renamed/removed/
  retyped; UC-1 and non-surface UC-2 runs must keep emitting inert defaults (byte-stable on those paths).

## RECOMMENDED TASK DECOMPOSITION (one FR → one task, in TDD §19.3 / spec §4.6 dependency order)

1. **T1 — `refs/runtime-surface.md` (source of truth).** Author the tagger allowlist, the
   language→(test-marker, comment-syntax) table, the degrade-oracle table (categories a–d), the rootwalk
   algorithm + depth bound (OQ-RSR.3, mirror §4.0 link-following depth=1), and the ledger schema. **Critical-path
   predecessor for everything** — blocks T2–T9.
2. **T2 — SKILL.md §6.1 tagger (step 4b', FR-RSR.1) + sweep (step 4b, FR-RSR.2).** Symbol-anchored tagger
   (NOT requirement-anchored); per-edge ledger → per-symbol counts; read-only. Depends T1.
3. **T3 — SKILL.md §9.1 +6 additive fields + `contract_version` 1.6.0 + §9.3 advisory consumer row (FR-RSR.7).**
   Parallelizable with T2 (additive, no dependency on sweep internals).
4. **T4 — degrade oracle (FR-RSR.3) + entrypoint-rootwalk (FR-RSR.4).** Highest-risk; **gate as a blocker of
   T2's UNREACHED verdict** — no UNREACHED may be emitted until T4 lands. Default all dynamic/registry/decorator/
   reflection/`[project.scripts]` wiring + partial-rootwalk + unknown-lang to **DEGRADE → §10.6 Grounding Gap,
   never Regression**.
5. **T5 — SKILL.md §5.3 table-wide forbid-STOP pre-filter `surface_unreached` + §5.4 tier_decision reason
   (FR-RSR.5).** Depends T3. Degrade-only runs (`runtime_surface_unreached == 0`) do NOT force T2.
6. **T6 — SKILL.md new §10.9 UNREACHED finding-modifier + `refs/deviation-taxonomy.md` xref (FR-RSR.6).** Maps by
   evidence onto the 4 classes; NO 5th class; increment ONLY `deviation_count_by_class.regression`, never
   `verification_regressions_detected`. Depends T2/T4 (consumes ledger status).
7. **T7 — `refs/reviewer-spec.md` ledger grounding-hunk entry (FR-RSR.9).** qa-persona; preserve the "exactly
   three sections" invariant. Depends T2. Parallel with T5/T6.
8. **T8 — fail-open on backend/tool loss (FR-RSR.8).** `backend: none` / tool failure → Grounding Gap +
   `degraded_components`, never STOP, never silent-PASS. Wired into the sweep; verify independently.
9. **T9 — eval coverage (FR-RSR.10) — TERMINAL ACCEPTANCE GATE.** One active headline case
   (`uc2-unwired-surface-passes`, real fixtures, **FAIL pre-change / PASS post-change**) + four MAIN companions
   (`positive-control`, `dynamic-dispatch`, `degraded-backend`, `test-only-ref`) under `evals/`; extend
   `grader.py` `regex_absent` / `yaml_field` only if needed; the two existing falsifier skeletons stay green;
   assert the count invariant `len(unreached_surfaces) == runtime_surface_unreached`.
10. **T10 — `make sync-dev` + `make verify-sync` clean + Release Checklist (TDD §24.2).** Depends on all
    SKILL.md/refs edits (T2–T8).

## PER-TASK DEFINITION OF DONE

Each task's verification checklist MUST include: (a) the spec §3 acceptance-criteria `- [ ]` boxes for that FR;
(b) the relevant NFR measurement method (spec §6) where one applies; (c) `make sync-dev && make verify-sync`
clean for any SKILL.md/refs edit; (d) the TDD §24.1 DoD line(s) for that work. Prefer **adversarial-stance
rf-qa with `fix_authorization`** for the MDTM quality gates.

## HUMAN-DECISION HANDLING

The open questions OQ-RSR.1–5 (spec §11) have stated resolution targets — resolve them per those targets during
implementation (e.g. enumerate the allowlist/lang-table rows in `refs/runtime-surface.md`, pick the rootwalk
depth bound). OQ-RSR.5 is already **accepted** per TDD D12. Only if a genuine product/scope ambiguity surfaces
that the spec's resolution target does NOT cover, write a `PENDING` item that **halts** the dependent task —
never auto-default a scope-shaping choice.

## OUTPUT

Write the MDTM tasklist to the standard task-builder location (`.dev/tasks/to-do/TASK-…`). Do not run `/task`;
this BUILD_REQUEST only authors the tasklist.
