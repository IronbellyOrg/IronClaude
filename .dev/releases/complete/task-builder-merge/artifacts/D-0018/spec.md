# D-0018 — API-001-M2 BUILD_REQUEST Contract Update Spec

**Task:** T02.03 — Update API-001-M2 BUILD_REQUEST contract
**Phase:** Phase 2 / Milestone M2 (FR-CONV.2 / PR-01)
**Roadmap row:** R-036 (API-001-M2 BUILD_REQUEST → MDTM contract update)
**Branch:** fix/obligation-scanner-meta-context-tests
**Generated:** 2026-05-17
**Dependencies satisfied:** T02.01 (D-0016 PASS, FR-CONV.2 wrapper landed); T01.14 (API-001 contract-freeze ratified)

---

## 1. Scope

T02.03 implements the M2 update to the API-001 BUILD_REQUEST → MDTM contract anchored in M1. The change is strictly additive: the M1-frozen 15-field BUILD_REQUEST schema is preserved byte-identical, and a single optional signal — `EXECUTION_CONTEXT_REQUIREMENTS` — is added to control the `## Execution Context` block emission landed by T02.01 (D-0016) and powered by the DM-001 emitters from T02.02 (D-0017).

The producer / consumer / transport / output / error-mode fields named in the M1 anchor row (roadmap row 21, `API-001`) are unchanged. The MALFORMED retry max-2 failure-mode (Critical Rule #12; orchestrator MALFORMED flow) is preserved verbatim.

## 2. The Frozen 15-Field BUILD_REQUEST Schema

The M1-frozen schema (preserved byte-identical by T02.03) consists of the following 15 fields, in the order they appear in the BUILD_REQUEST template body inside the spawn-prompt at `src/superclaude/skills/task-builder/SKILL.md` (between the `BUILD_REQUEST:` banner and the `INCREMENTAL TASK FILE WRITING` directive):

| # | Field | Role |
|---|-------|------|
| 1 | `GOAL` | What the task file should accomplish when executed |
| 2 | `WHY` | Context for why this task is needed |
| 3 | `TASK_ID_PREFIX` | Always `TASK-RF` for this skill |
| 4 | `TEMPLATE` | `01` (simple) or `02` (complex) |
| 5 | `QA_GATE_REQUIREMENTS` | NONE / FINAL_ONLY / PER_PHASE |
| 6 | `VALIDATION_REQUIREMENTS` | Lint / type-check / build asserts |
| 7 | `TESTING_REQUIREMENTS` | NONE / UNIT / INTEGRATION / E2E / ALL |
| 8 | `DOCUMENTATION STALENESS WARNINGS` | Doc cross-validator findings |
| 9 | `RESEARCH DIR` | `${TASK_DIR}research/` + file listing |
| 10 | `QUALITY GATE RESULTS` | Analyst + QA report locations |
| 11 | `OPEN QUESTIONS (could not be resolved by research)` | Document as risks |
| 12 | `REMAINING GAPS (if any — after max gap-fill rounds)` | Document as limitations |
| 13 | `CRITICAL — GRANULARITY REQUIREMENT` | Per-file/per-component items mandate |
| 14 | `TO BUILD A GOOD TASK FILE, YOU NEED` | Builder readiness checklist |
| 15 | `ESCALATION — CRITICAL OVERRIDE` | No team context override block |

Trailing protocol sections (`INCREMENTAL TASK FILE WRITING`, `EXECUTION CONTEXT BLOCK`, `TASK FILE LOCATION`, `STEPS`) are builder-side directives, not BUILD_REQUEST fields per se — they are body sections of the spawn-prompt and out of scope for the 15-field freeze.

## 3. The New Optional Field — `EXECUTION_CONTEXT_REQUIREMENTS`

Inserted between `TESTING_REQUIREMENTS` and `DOCUMENTATION STALENESS WARNINGS` at `src/superclaude/skills/task-builder/SKILL.md:779`.

**Three permitted values:**

| Value | Behavior |
|-------|----------|
| `AUTO` (default; same as omission) | Builder applies the rollup-signal heuristic (≥3 distinct named source areas inferable from research findings) to decide whether to emit the `## Execution Context` block. Fully-populated form renders all 3 labeled bullets (References, Source areas, Key constraints). Minimal form (GOAL-only BUILD_REQUEST) renders References-only with the other two bullets ABSENT. |
| `REQUIRED` | Builder MUST emit the block. The degraded References-only form is permitted when only GOAL is populated; suppressing the block entirely is a MALFORMED output. |
| `SUPPRESS` | Builder MUST NOT emit the block. Per-item Context fields remain unchanged regardless of this value. Used for thin / throwaway task files. |

**Omission semantics:** absence of the field implies `AUTO`. This is what guarantees strictly-additive behavior — M1 callers that don't know about the new signal get exactly the M1 behavior.

**Violation failure-mode:** the orchestrator-mediation MALFORMED retry max-2 flow (see § 5 below) fires when the builder emits the block under `SUPPRESS` or omits the block under `REQUIRED`.

## 4. Emission Rule — Fully-Populated vs Minimal BUILD_REQUEST

The DM-001 emitters from T02.02 (`SKILL.md:868-916`) define the per-emitter rules. The API-001-M2 contract wires the field-level decision to the block-level emission:

| BUILD_REQUEST shape | `EXECUTION_CONTEXT_REQUIREMENTS` | Header emission |
|---------------------|----------------------------------|-----------------|
| Fully-populated (≥3 inferable source areas) | omitted / `AUTO` | 3 labeled bullets: References + Source areas + Key constraints |
| Fully-populated (≥3 inferable source areas) | `REQUIRED` | 3 labeled bullets (same as AUTO path) |
| Fully-populated (≥3 inferable source areas) | `SUPPRESS` | Block omitted entirely |
| Minimal (GOAL-only) | omitted / `AUTO` | References-only (Source areas + Key constraints absent, not blank-but-present) |
| Minimal (GOAL-only) | `REQUIRED` | References-only (degraded form is permitted under REQUIRED) |
| Minimal (GOAL-only) | `SUPPRESS` | Block omitted entirely |
| Insufficient rollup signal (`<3` inferable source areas, no minimal fixture override) | omitted / `AUTO` | Block omitted entirely |
| Insufficient rollup signal | `REQUIRED` | References-only (force-degrade) |
| Insufficient rollup signal | `SUPPRESS` | Block omitted entirely |

This table is enforced by the prose at:

- `SKILL.md:779-799` — field-body documenting AUTO/REQUIRED/SUPPRESS semantics.
- `SKILL.md:885-891` — "Signal control (API-001-M2)" paragraph in the EXECUTION CONTEXT BLOCK narrative.
- `SKILL.md:1532-1537` — "Optional BUILD_REQUEST signals" reference list in the Builder Agent Prompt subsection.

## 5. MALFORMED Retry Max-2 — Preserved Verbatim

The MALFORMED retry max-2 failure-mode is the API-001 error mode (roadmap row 21: `error-mode:MALFORMED-max-2-retry`). It is preserved unchanged at:

- `SKILL.md:944-948` — orchestrator MALFORMED flow body (`**Maximum 2 MALFORMED rounds**` literal at L977).
- `SKILL.md:1705` — Critical Rule #12 (`Builder mediation has separate retry counters`).

Both occurrences carry the same wording as before T02.03; no edit touched these lines.

The new `EXECUTION_CONTEXT_REQUIREMENTS` field references this failure-mode in its body (`SKILL.md:796-799`): "Failure mode: MALFORMED retry max-2 ... applies when the builder violates this signal — e.g., emitting the block under SUPPRESS, or omitting the block under REQUIRED." This wires the new signal into the existing failure-mode without changing the failure-mode itself.

## 6. Producer / Consumer / Transport — Unchanged

| Contract field | M1 anchor value (roadmap row 21) | Verified at |
|----------------|----------------------------------|-------------|
| Producer | `task-builder` skill | `SKILL.md` orchestrator A.9 (`:733`) |
| Consumer | `rf-task-builder` subagent | `SKILL.md:741` `subagent_type: "rf-task-builder"` |
| Transport | Skill prompt + on-disk MDTM | `SKILL.md:739-960` (prompt body) + `:917` (`TASK FILE LOCATION`) |
| Output | `## Execution Context` block | `SKILL.md:856-944` (emission rules) |
| Error mode | `MALFORMED-max-2-retry` | `SKILL.md:944-948`, `:1705` |

All five contract fields are textually unchanged by T02.03 — only an optional signal is added to control the existing Output emission.

## 7. Acceptance Criteria Mapping (per phase-2-tasklist.md L141-147)

| AC | Criterion | Verification | Evidence § |
|----|-----------|--------------|------------|
| AC1 | BUILD_REQUEST 15-field schema unchanged (byte-diff zero in the existing 15 fields) | Automated strip-and-diff (pre-edit snapshot vs post-edit with new field removed); per-field byte-comparison | `evidence.md` § 1, § 2 |
| AC2 | EXECUTION_CONTEXT_REQUIREMENTS documented as optional in SKILL.md | Field present at `SKILL.md:779` with `[OPTIONAL signal ...]`; listed in "Optional BUILD_REQUEST signals" at `:1532-1537` | `evidence.md` § 3 |
| AC3 | MALFORMED retry max-2 failure-mode preserved verbatim | Literal `**Maximum 2 MALFORMED rounds**` at `SKILL.md:977` unchanged; Critical Rule #12 at `:1705` unchanged | `evidence.md` § 4 |
| AC4 | Generated MDTM from updated contract contains `## Execution Context` block after frontmatter, before first phase | Block already wired by T02.01 (D-0016) at `SKILL.md:1587-1595` of the Output Structure template; new signal does not regress that placement | `evidence.md` § 5 |
| AC5 | Sub-agent report confirms producer/consumer/transport unchanged | `quality-engineer` sub-agent spawned; report attached | `evidence.md` § 6 |

## 8. Scope-Confinement & Invariants

1. **15-field freeze respected** — strip-and-diff against the M1 snapshot returns byte-identical.
2. **Strictly additive** — no existing field renamed, no body edited; only one new optional field inserted between fields 7 and 8.
3. **NFR-CONV.3 hidden-input determinism (header range)** — unaffected. The new field describes signal semantics; the no-file-paths guard applies to the runtime-emitted header bullets (DM-001.SourceAreas), not to documentation prose in the BUILD_REQUEST template.
4. **Per-item Context preservation (CASE-D PR-01)** — unaffected. The new signal only controls the header-block emission; per-item Context fields are not touched under any value (explicitly stated in the SUPPRESS branch body).
5. **TB-Add-7 / TB-Add-8 compatibility (M1)** — unaffected. TB-Add-7 cross-validates SourceAreas-vs-items; the new signal does not change SourceAreas semantics. TB-Add-8 cross-validates per-item Context fields; the new signal does not touch per-item fields.

## 9. Rollback

Per roadmap (R-036): per-FR rollback granularity preserved.

- **Per-line revert** — delete the `EXECUTION_CONTEXT_REQUIREMENTS` field block at `SKILL.md:779-799`, delete the "Signal control (API-001-M2)" paragraph at `:885-891`, and delete the "Optional BUILD_REQUEST signals" bullet list at `:1532-1537`. Re-run `make sync-dev` and `make verify-sync`. The 15-field schema returns to its M1-frozen byte-identical state.
- **Behavior after rollback** — Execution Context block emission falls back to the AUTO heuristic from T02.01/T02.02 (D-0016 / D-0017). No M2 functionality outside this row is regressed.

## 10. Cross-References

- API-001 anchor row: `roadmap.md` L112 (row 21)
- R-036 implementation row: `roadmap.md` L168 (row 5 of M2 table)
- DM-001 frozen contract (T01.13 / D-0011 § 1): referenced; artifact not present on disk at audit time but emission rules consumed via SKILL.md § 856-944.
- T02.01 wrapper landing (D-0016): wraps `## Execution Context` heading in MDTM Output Structure template at `SKILL.md:1587-1595`.
- T02.02 emitter rules (D-0017): defines References / Source areas / Key constraints emitters at `SKILL.md:868-916`.
- Phase 2 tasklist row: `phase-2-tasklist.md` L105-154 (T02.03).
- Quality-engineer sub-agent report: `evidence.md` § 6.

## 11. Notes

- The optional signal mirrors the established pattern of M1's `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` signals (NONE / value / value sets). Placement between TESTING_REQUIREMENTS and DOCUMENTATION STALENESS WARNINGS groups the new signal with the other structural-requirements signals and minimizes diff surface.
- The reference to `SKILL.md A.9 mediation` in the new field body is a section-pointer (no `:NN` line number). The actual MALFORMED flow lives in the A.9 orchestrator-mediation paragraph at `:944-948`. Future cosmetic edits may re-anchor the pointer if A.9 is renumbered; non-blocking for M2.
