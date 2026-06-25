# Research Notes: Implement RFMerger P1–P5 into the sc:tasklist generator

**Date:** 2026-06-19
**Scenario:** A (Explicit — refreshed spec/PRD/TDD + ledger + matrix + handoff supply most details)
**Depth Tier:** Deep (deep edits across a 1631-line generator skill + CLI + 3 test dirs; multiple subsystems; cross-contract reuse)
**Track Count:** 1 (single cohesive track — all five proposals modify the same `sc-tasklist-protocol` generator + its tests and share the 11-stage pipeline context; NOT independent work streams)
**Status:** Complete

> **Authorization.** This is the implementation build explicitly AUTHORIZED by
> `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/downstream-task-builder-handoff.md`
> (`status: AUTHORIZED`, `review_status: SIGNED-OFF`, P2 = `retain-with-full-set-revalidation-and-guards`,
> P5 = `retain-advisory-only`, authorized 2026-06-19). The prior folder
> `TASK-RF-rfmerger-refresh-20260618-172224/` is a SEPARATE, COMPLETED (🟢 Done) documents-only task that
> PRODUCED the refreshed spec/PRD/TDD; it is NOT this goal. Its `research/` is reused as background.

---

## EXISTING_FILES

### Primary edit target (canonical; `.claude/` is a generated mirror — NEVER an edit/stage target)

- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1631 lines) — **the single authoritative inline 11-stage generator.** All five proposals attach here. Verified current landmarks (2026-06-19):
  - Stage 4 Enrichment: `:444` (Deterministic Enrichment), reporting row `:1534`; tier scoring `:546-646`; `--spec` supplementary task gen `:246`. **P1 `## Execution Context` block + P5 `## Tier Calibration Advisory` attach at Stage 4.**
  - Stage 6 Self-Check / pre-write quality gate (checks 1–20): `:1132-1195`, gate verdict `:1187` ("check 1-20"). **P4 `gate-results.txt` emission attaches at end of Stage 6.** ⚠ Live inconsistency: `:1597` still says "all 17 checks passed" while `:1187` says "check 1-20" — a stray 17-vs-20 (P4 work should standardize on 20; do NOT silently rewrite unrelated text without verifying).
  - Stage 7 Roadmap Validation (2N parallel agents): `:1244-1311`. **P4 prompt injection + P3 DNSP synth-on-agent-failure attach at Stage 7.**
  - Stage 8 Patch Plan: `:1312`. Stage 9 Patch Execution (delegate `sc:task`): `:1409-1427`. Stage 10 Spot-Check: `:1429`. **P2 bounded loop attaches at Stage 10 → Stage 9.**
  - Stage 10.5 Pre-Reflect Sign-off (advisory; PASS/PARTIAL/FAIL all ship; `--remediate` never auto-mutates; skipped under `--no-reflect`): `:1460-1481`. **P2 non-overlap obligation references this boundary.**
  - `feedback-log.md` already named in output layout: `:86`, `:125`. **P5 advisory reads this; never mutates scored tiers.**
  - `--no-reflect` / `--spec` flag semantics: `:9`, `:169` (4.1a Supplementary TDD Context), `:246` (4.4a Supplementary Task Gen). **`--spec §22` self-contradiction: `:49-57` "exactly one input: the roadmap text" vs the documented 4-site `--spec` enrichment.**
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (189 lines) — source-side read-only reference extracted from SKILL.md (NOT a `.claude/` mirror). P1 block shape is reflected here AFTER editing SKILL.md (authoritative); do NOT hand-edit as if it were runtime. Disclosed checkpoint-heading lag (`:110,:128`).
- `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md` (114 lines) — tier algorithm reference (P5 advisory must not alter scored tiers).
- `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` (59 lines) — emission rules; known mirror-lag (omits post-reflect terminal task). Respect, do not propagate.
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` (142 lines).
- `src/superclaude/commands/tasklist.md` (119 lines) — slash wrapper; parses/validates `--spec`/`--output`/`--no-reflect`; mandatorily invokes the skill.
- `src/superclaude/cli/tasklist/` — validate CLI (NOT the generator path). `commands.py` (185), `executor.py` (276), `gates.py` (46), `prompts.py` (234 — `build_tasklist_generate_prompt` vs `build_tasklist_fidelity_prompt`), `models.py` (30).

### Reused contract (P3) — owned by task-builder, NOT redefined

- `src/superclaude/skills/task-builder/SKILL.md:873-911` — the EXISTING `synthetic-dnsp` / DM-003 emission contract (fixed `severity: HIGH`, `source: "synthetic-dnsp"`, 2-element `dedup_key` `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`, `found_n_times`, all-agents-fail Path A/B/C / R-122, strictly-additive merge, N-1 cohort concurrency INV-021). P3 in sc:tasklist **REUSES this verbatim via a thin adapter** for the narrower Stage-7-validation-agent case. A divergent/forked schema is a HALT condition.
- `src/superclaude/skills/task-builder/SKILL.md:1066,1231` — task-builder's `## Execution Context` required section (References/Source areas/Key constraints, no file:line in header). P1's block reuses the same sub-field names + no-file-path discipline; a SECOND incompatible "Execution Context" meaning is a HALT condition.
- PR-02 regression/monotonicity semantics `task-builder/SKILL.md:1290-1305` — P2's monotonicity guard + regression detection REUSE these, do not redefine.

### Test surfaces

- `tests/tasklist/` — `test_tasklist_cli.py` (277), `test_tasklist_fidelity.py` (228), `test_autowire.py` (149), `test_prd_cli.py` (39), `test_prd_prompts.py` (101). New test fns land in `test_tasklist_cli.py`.
- `tests/cli/reflect/` (disk-verified path — NOT `tests/reflect/`) — must stay green (`test_marker_suppression.py`, `test_docs_cli_parity.py`).
- `tests/skills/test_task_builder_merge.py` — PR-01..PR-07 retained-feature content gate (must stay green; P1/P3 add assertions here too).
- `tests/audit/` — `test_inherited_verdict_freshness_inv_002.py`, `test_five_axes_overlay.py`, `test_dnsp_*` (where present).
- `tests/cli/test_verify_sync_hooks.py` (V1-V7) — sync parity.
- `src/superclaude/cli/sprint/config.py:15-32,34-55,73-124,134-146` — Sprint parser conventions (NFR-RFMERGE.4; constrains downstream output, not edited here).

### Driving source documents (the spec of intent)

- `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md` (823 lines) — FR-RFMERGE.1–.7 + gate criteria + §5.3 phase contracts (the per-proposal runtime contracts) + §11 open items.
- `.../prd.md` (830), `.../tdd.md` (1367 — §10 component inventory, §11 user flows, §12 error handling, §15.2 test cases, §22 open questions).
- `.../artifacts/refresh-requirements-ledger.md` (76), `.../artifacts/refresh-validation-matrix.md` (139) — control inputs (P1-P5 dispositions + per-output gates).

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth discipline (ABSOLUTE):** edit `src/superclaude/...` FIRST, then `make sync-dev` + `make verify-sync`. NEVER stage `.claude/{skills,commands,agents,hooks,templates}` (only `.claude/settings.json` is tracked). If `git add` needs `-f` on `.claude/*` → STOP.
- **UV-only** for all Python: `uv run pytest ...`, never bare `pytest`/`python`.
- **Determinism convention:** scored tiers are a pure function of the roadmap; P5 advisory and P1 block must preserve "same roadmap → same scored tiers / same block".
- **Generator works on roadmap TEXT, not a live codebase** → no per-step file paths may be invented (P1).
- **Stage-based prose protocol:** SKILL.md describes each stage as a numbered section with emission rules; edits are inline-prose contract changes, not Python functions (the generator is an LLM-run skill protocol, NOT compiled code — except `cli/tasklist/*` which IS Python).
- **Reuse-over-fork:** P3 and P2 reuse existing task-builder/PR-02 contracts; forking is a HALT.
- **Lint/format gate:** `make lint` runs ruff check; CI separately runs `ruff format --check src/ tests/` — run `uv run ruff format --check src/ tests/` before declaring done (any Python edits).

## GAPS_AND_QUESTIONS (for researchers to resolve against CURRENT source)

1. Exact current line ranges + surrounding prose for each P1-P5 attachment point (the spec/TDD citations are from 2026-06-18; verify no drift).
2. The exact Stage-7 prompt-build site and finding-merge step where P3 synth + P4 injection attach (in SKILL.md prose and/or `cli/tasklist/prompts.py`).
3. The 20-check quality-gate exact structure + where `gate-results.txt` emission would slot (P4) + the live 17-vs-20 stray at `:1597`.
4. How existing `tests/tasklist/test_tasklist_cli.py` exercises generation (fixtures, parse helpers) so new test fns match conventions.
5. The exact task-builder DM-003 field contract + which `tests/skills/test_task_builder_merge.py` / `tests/audit/test_dnsp_*` assertions P3 must conform to.
6. The Stage 9 `sc:task` delegate prose + Stage 10/10.5 boundary, to define P2's loop and prove non-overlap with Stage 10.5.
7. `--spec §22` settlement: confirm the SKILL.md:49-57 "exactly one input" wording vs the 4 `--spec` enrichment sites; characterize the smallest behavior-preserving reconciliation.

## RECOMMENDED_OUTPUTS (research/ files; build on prior folder's research where noted)

| # | Topic type | Output file |
|---|------------|-------------|
| 01 | File Inventory + Stage Map | `research/01-skill-stage-map.md` |
| 02 | Patterns & Conventions | `research/02-skill-conventions.md` |
| 03 | Integration Points (DNSP/PR-02/reflect/sc:task/sprint) | `research/03-integration-contracts.md` |
| 04 | Data Flow Tracer (per-proposal attachment trace) | `research/04-proposal-attachment-trace.md` |
| 05 | Test & Verification | `research/05-tests-and-verification.md` |
| 06 | Template & Examples (MDTM 02 + prior task example) | `research/06-template-and-examples.md` |
| 07 | Doc Cross-Validator (verify spec/TDD citations vs current source + settle --spec §22) | `research/07-citation-crossval-and-spec.md` |

## SUGGESTED_PHASES (researcher assignments — 7 researchers, Deep tier, single track; ALL spawned in one message)

- **R01 File Inventory + Stage Map** — Scope: `sc-tasklist-protocol/SKILL.md` (all 11 stages), `phase-template.md`, `index-template.md`, `commands/tasklist.md`, `cli/tasklist/*`. Catalog every stage with current line ranges, exports/fns, and the EXACT attachment point for each of P1 (Stage 4 block), P3 (Stage 7), P4 (Stage 6 emit + Stage 7 inject), P2 (Stage 9/10), P5 (Stage 4 advisory). Others cover: R03 the reused contracts, R04 the data-flow, R05 tests.
- **R02 Patterns & Conventions** — Scope: SKILL.md authoring style, determinism conventions, markdown emission shapes, the 20-check gate structure, tier-classification rules. Document how to add prose/templates consistently. Others: R01 the inventory, R04 the flow.
- **R03 Integration Points** — Scope: `task-builder/SKILL.md:873-911` (DM-003), `:1066,:1231` (Execution Context), `:1290-1305` (PR-02); `sc-reflect-protocol` Stage-10.5 boundary; `sc:task` delegate; `cli/sprint/config.py` conventions. Map exact field contracts P3/P2/P1 must conform to + the non-overlap boundary for P2 vs Stage 10.5. Others: R01 stage map, R05 the test assertions.
- **R04 Data Flow Tracer** — Scope: trace the 11-stage generation end-to-end (Stage 4 enrich/tier-score → Stage 6 self-check → Stage 7 validation 2N agents + merge → Stage 8/9/10 patch → Stage 10.5). Pin where each P1-P5 hooks, what data each consumes/emits, and the determinism path. Others: R01 inventory, R03 contracts.
- **R05 Test & Verification** — Scope: `tests/tasklist/*` (esp. `test_tasklist_cli.py` conventions/fixtures), `tests/cli/reflect/*`, `tests/skills/test_task_builder_merge.py`, `tests/audit/test_dnsp_*`, `tests/cli/test_verify_sync_hooks.py`. Document per-test-file structure + the EXACT new test fns from spec §8.1 / TDD §15.2 and how to author each. Others: R03 the contracts under test.
- **R06 Template & Examples** — Scope: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (rules A3/A4/B2, M3/M4/I19-I22, PR-02 monotonicity), plus the prior `TASK-RF-rfmerger-refresh-20260618-172224/TASK-RF-rfmerger-refresh-20260618-172224.md` as a worked complex-task example. Document required sections + QA-gate encoding patterns. Others: R05 tests.
- **R07 Doc Cross-Validator** — Scope: cross-validate EVERY spec/TDD citation against CURRENT source (`SKILL.md:873-911`, `:1066,:1231`, `:1132-1194`, `:1460-1481`, `:169-182`, `:246-271`, `:1297-1308`, `:1466-1471`, `:1290-1305`; the 17-vs-20 stray at `:1597`). Tag each [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]. Settle `--spec §22`: characterize the smallest behavior-preserving reconciliation of `:49-57` vs the 4 enrichment sites. Others: R01 stage map.

## TEMPLATE_NOTES

- **MDTM Template: 02 (Complex Task)** — discovery + build + per-proposal implementation + tests + QA gates + the documents-source-transformation (spec→implementation) profile. Definitely not Template 01.
- **Tier: Deep** — 1631-line generator, 5 proposals, 3 test dirs, cross-contract reuse, multi-subsystem.
- **QA_INTENSITY: full**; **QA_GATE_REQUIREMENTS: PER_PHASE** (template 02 default; per-proposal phases each get a gate).
- **TESTING_REQUIREMENTS: UNIT** (+ existing integration suites stay green). **VALIDATION_REQUIREMENTS:** `make lint`, `uv run ruff format --check src/ tests/`, `make sync-dev`, `make verify-sync`, and the exact pytest commands below.
- **SPEC_PATH:** `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md` → tasklist frontmatter `spec_path:` + threaded into A.10.7 PRE reflect `--spec`.
- **POST_REFLECT_GATE: ENABLED.**
- Exact runtime commands (UV-only, disk-verified): `uv run pytest tests/tasklist/ -v`; `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`; `uv run pytest tests/cli/reflect/ -v`; `uv run pytest tests/skills/test_task_builder_merge.py -v`; `make sync-dev`; `make verify-sync`.

## AMBIGUITIES_FOR_USER

- **`--spec §22` input-contract reconciliation (settled here as a bounded design decision; one residual decision flagged).** P1–P5 do NOT depend on or alter `--spec` semantics. The risk is a pre-existing SKILL.md self-contradiction (`:49-57` "exactly one input: the roadmap text" vs the 4 documented `--spec` enrichment sites). **Settlement for this build:** the tasklist will include a bounded, behavior-preserving doc-consistency edit reconciling the `:49-57` wording to acknowledge `--spec` as an OPTIONAL supplementary input (the behavior already supports it), changing NO runtime behavior. **Residual Open Question (NOT silently decided — surfaced for the human):** whether the maintainer instead wants to REMOVE `--spec` enrichment to make the generator genuinely roadmap-only — a larger behavior change out of P1-P5 scope. The tasklist records this as an Open Question; it does not auto-apply the removal.
- Otherwise intent is clear: implement P1 (conservative `## Execution Context`), P2 (retain-with-full-set-revalidation-and-guards, 2-total-pass cap, no Stage-10.5 overlap), P3 (reuse task-builder synthetic-dnsp DM-003 + all-agents-fail guard + provenance), P4 (gate-results.txt passthrough), P5 (retain-advisory-only, never mutate scored tiers), plus carried-gap tests (`--no-reflect`/Stage 10.5, slash flags, `sc:task` naming, stale-token prevention).
