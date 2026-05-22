# D-0059 — T05.07 Spec: Wire INV-012 Cross-Cycle Dedup Composition

**Task:** T05.07 (Phase 5 — M5 Retry Monotonicity + Regression Halts)
**Roadmap items:** R-096 (INV-012 — cross-cycle synthetic-dnsp dedup composition: synthetic findings count as failures for `|F_n|`; identical dedup_key across consecutive cycles is dedup, NOT regression; persistence trips monotonicity intended, not regression)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STRICT
**Confidence:** [████████--] 88%
**Verification method:** Sub-agent (quality-engineer) — read-only ratification + synthetic-fixture self-consistency
**Sub-Agent Delegation:** Required (executed; report at `quality-engineer-report.md`)
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`

---

## 1. Scope

T05.07 operationalises **INV-012** — the cross-cycle synthetic-dnsp dedup composition rule — by landing a dedicated subsection in `src/superclaude/skills/task-builder/SKILL.md` (lines 1061–1075) that:

1. Carries the canonical INV-012 statement that synthetic-dnsp findings (PR-03 / FR-CONV.6) COUNT as failures for `|F_n|` cardinality.
2. States that a synthetic finding with an identical `(assigned_files_range, escalation_ladder_exhaust_point)` `dedup_key` across consecutive cycles **contributes 1 (not 2) to `|F_{n+1}|`** (the core AC1 statement).
3. Specifies the **cross-cycle dedup-key tracking (bookkeeping rule)** — no additional per-cycle state is needed beyond the F-set itself; `F_{n+1}` is computed by the same dedup-key identity as `F_n`.
4. States the **regression-vs-persistence decision rule**: persistence has `dedup_key ∈ FAIL_n` (not `PASS_n`), so the Step 1 set predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is FALSE by construction — cross-cycle persistence is NEVER a regression.
5. Provides **three worked examples** (shrink case, non-shrink case, same-cycle dedup contrast).
6. States the **regression non-emission invariant** (cross-cycle synthetic-dnsp): regression halt MUST NOT be emitted for any item whose dedup-key was in `F_n`; the consumer-side fixture assert (`grep -c "Regression detected on Item" <execution-log>` MUST return `0`) is pinned.

The placement is strictly additive: the subsection sits between the strict-ordering invariant of the 4-step rule (`SKILL.md` L1059) and the `### A.10: Task File Validation` heading (`SKILL.md` L1077, previously L1061 pre-edit). The four preservation invariants from T05.01–T05.05 are byte-identical (see §7 hashes).

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| FR-CONV.5 wrapper (T05.01 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1014-1027 | Houses the INV-012 inline composition note at L1025 (textual cross-reference); the new subsection at L1061-1075 operationalises it |
| API-004 contract block (T05.02 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1029-1059 | Houses the F-set definition with dedup-key identity (L1042-1048) and the 4-step ordering rule (L1050-1059); the new subsection references Step 1 (L1054), Step 2 (L1055), and Step 4 (L1057) by line number |
| 4-step ordering rule (T05.05 ratified) | `src/superclaude/skills/task-builder/SKILL.md` L1050-1059 | Defines the strict precedence regression → monotonicity → hard-cap → proceed; the new INV-012 subsection ties to Step 1 (regression predicate) and Step 2 (monotonicity halt) |
| DM-003 Synthetic DNSP Finding schema | roadmap.md L109 + TDD §8.96 | Defines the 2-tuple `dedup_key=(assigned_files_range, escalation_ladder_exhaust_point)` consumed by the new subsection's bookkeeping rule |
| 3-cycle hard cap (preservation) | `src/superclaude/agents/rf-team-lead.md` L417 | Step 3 backstop referenced by the new subsection's non-shrink example |
| Per-gate counter table (preservation) | `src/superclaude/agents/rf-task-builder.md` L354-364 | Per-gate caps referenced by the new subsection's example transitions |
| Roadmap item R-096 | `.dev/releases/current/task-builder-merge/roadmap.md` L315 | Defines the INV-012 acceptance criteria: "synthetic-same-dedup_key-cycles-N-N+1:contributes-1-not-2-to-F_n+1; persistence:trips-monotonicity-intended-not-regression" |
| T05.05 evidence (immediate predecessor) | `.dev/releases/current/task-builder-merge/artifacts/D-0058/evidence.md` | §8 ratifies the L1025 inline INV-012 composition note and stages T05.07 as the runtime wiring task |
| TDD §8.96 (canonical INV-012 sentence) | `.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md` L896 | Source-of-truth wording for "contributes `1` (not `2`) to `|F_{n+1}|`" verbatim in the subsection opener |
| Release spec §INV-012 | `.dev/releases/current/task-builder-merge/release-spec.md` L205 | "Composition rule is encoded verbatim in the Retry Monotonicity Protocol subsection" — directly mandates the SKILL.md edit site |

## 3. INV-012 subsection (R-096 — operational rule)

The new subsection lives at `src/superclaude/skills/task-builder/SKILL.md` L1061-1075 (sha256 `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`). It contains five paragraphs:

| ¶ | SKILL.md line | Topic |
|---|---|---|
| Heading | 1061 | `**INV-012 cross-cycle dedup composition (operational rule):**` |
| ¶1 (opener) | 1063 | Composition rule: synthetic-dnsp findings COUNT as `|F_n|` failures; same `dedup_key` across consecutive cycles is DEDUP, NOT regression — contributes `1` (not `2`) to `|F_{n+1}|`; persistence trips monotonicity (intended) |
| ¶2 (bookkeeping) | 1065-1067 | Cross-cycle dedup-key tracking: each gate records `F_n` keyed by dedup-key; `F_{n+1}` is computed by the same dedup-key identity; same 2-tuple re-emitted on cycle `n+1` collapses with cycle-`n` counterpart into a single element of `F_{n+1}` BEFORE the monotonicity comparison runs |
| ¶3 (decision rule) | 1069 | Regression vs. persistence: `dedup_key ∈ FAIL_n` implies `dedup_key ∉ PASS_n`, so Step 1 set predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is FALSE by construction; persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|` |
| ¶4 (examples) | 1071-1074 | Three worked examples: (1) cross-cycle dedup + strict shrink → PROCEED; (2) cross-cycle dedup + non-shrink → HALT `[HALT-MONOTONICITY] |F|=2`; (3) same-cycle dedup collapse contrast |
| ¶5 (invariant) | 1075 | Regression non-emission invariant: regression halt MUST NOT be emitted for any item whose dedup-key was in `F_n` (FAIL_n); cross-cycle dedup excluded from regression by construction; consumer fixture assert `grep -c "Regression detected on Item" <execution-log>` MUST return `0` |

## 4. Acceptance criteria coverage

| AC | Statement (verbatim from T05.07 task) | Where verified |
|----|----------------------------------------|----------------|
| AC1 | Cross-cycle synthetic same-dedup_key fixture contributes 1 to `F_n+1`, not 2 | SKILL.md L1063 "contributes `1` (not `2`) to `|F_{n+1}|`" + L1067 (bookkeeping rule) + L1074 (same-cycle contrast); fixture `fixture-cross-cycle-dedup-shrinking.log` shows `|F_2|=2` after cross-cycle synth-K collapse from `|F_1|=3`; fixture `fixture-cross-cycle-dedup-non-shrink.log` shows `|F_2|=2` instead of 3 (cross-cycle collapse) |
| AC2 | No regression halt emitted for the cross-cycle dedup case | SKILL.md L1069 (regression-vs-persistence rule + Step 1 predicate analysis) + L1075 (regression non-emission invariant: MUST NOT + by-construction); fixture-shrinking `grep -c "Regression detected on Item" = 0`; fixture-non-shrink `grep -c "Regression detected on Item" = 0` |
| AC3 | Monotonicity halt fires if cardinality is non-shrinking | SKILL.md L1069 "Persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|`" + L1063 "if it persists with nothing else changing it WILL trip the monotonicity guard — the intended behavior"; fixture-non-shrink emits byte-exact `HALT [HALT-MONOTONICITY] |F|=2` at the cycle-2 transition; cycle 3 NOT attempted |
| AC4 | Sub-agent quality-engineer report confirms composition rule documented in SKILL.md | `quality-engineer-report.md` §6 walks through all five required AC4 elements (heading + composition rule + bookkeeping rule + decision rule + ≥2 worked examples + regression non-emission invariant); overall PASS verdict at §8 |

All four ACs PASS. Sub-agent overall verdict: PASS.

## 5. Sub-agent quality-engineer ratification

A quality-engineer sub-agent was spawned read-only (no Edit / Write / replace_content / replace_symbol_body / insert_*_symbol calls against any source-of-truth file; the only Write call produced the report under `D-0059/`). The sub-agent verified:

- **§2 Preservation (5 hashes):** all four preserved regions byte-identical; A.10 heading still present at SKILL.md L1077 (one blank-line gap after INV-012 subsection ends at L1075).
- **§3 AC1:** verbatim "contributes `1` (not `2`) to `|F_{n+1}|`" at L1063; reinforced at L1067 + L1074.
- **§4 AC2:** Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is FALSE by construction at L1069; normative MUST NOT invariant at L1075.
- **§5 AC3:** biconditional "if and only if `|F_{n+1}| >= |F_n|`" at L1069; tied to Step 2 (L1055); worked numeric trace at L1073.
- **§6 AC4:** heading at line 1061 confirmed; all five required content elements present with verbatim quotes.
- **§7 Fixture verification:** all six grep assertions across both fixtures match required counts exactly.

Sub-agent overall verdict (§8): **PASS (STRICT TIER) — No ambiguities found. No edits made. T05.07 is ratified.**

## 6. Synthetic execution-log fixtures

Two synthetic execution-log fixtures landed under `D-0059/`:

| Fixture | Purpose | AC coverage |
|---|---|---|
| `fixture-cross-cycle-dedup-shrinking.log` | Cross-cycle synth-dnsp dedup + strict shrink: continues to cycle 3, NO regression halt, NO monotonicity halt | AC1 (contributes 1 not 2: `|F_2|=2 < |F_1|=3`) + AC2 (regression-count = 0) |
| `fixture-cross-cycle-dedup-non-shrink.log` | Cross-cycle synth-dnsp dedup + non-shrink: HALT [HALT-MONOTONICITY] at cycle 2, NO regression halt | AC2 (regression-count = 0 even with synth-K persistence) + AC3 (monotonicity halt at non-shrink) |

Per-fixture grep counts (computed at evidence time):

| Fixture | `Regression detected on Item` | `^HALT ` | `^CYCLE 3 START` |
|---|---:|---:|---:|
| shrinking | 0 (required 0) | 0 (required 0) | 1 (required 1) |
| non-shrink | 0 (required 0) | 1 (required 1) | 0 (required 0) |

All six asserts match required counts exactly. The non-shrink fixture also pins the byte-exact `HALT [HALT-MONOTONICITY] |F|=2` payload at line 30 (per API-004 contract row at SKILL.md L1037).

## 7. Preservation invariants (carried from T05.01..T05.06)

T05.07's only source-file edit is the additive subsection at SKILL.md L1061-1075. The following hashes recorded in D-0054 / D-0055 / D-0056 / D-0057 / D-0058 remain unchanged:

| Slice | sha256 |
|---|---|
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `SKILL.md` L1029-1059 (API-004 contract block — T05.02 baseline; includes F-set L1042-1048 and 4-step rule L1050-1059) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `rf-team-lead.md:417` (3-cycle hard cap — preserved end-to-end) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |

The four independent retry counters (RESEARCH_NEEDED, MALFORMED, research-gate gap-fill, per-gate fix cycles) and the global 3-cycle hard cap at `rf-team-lead.md:417` are PRESERVED end-to-end.

`make verify-sync` reports `✅ All components in sync.` for the SKILL.md edit (the unrelated pre-existing hook-script drift is outside T05.07's scope and is tracked separately by the in-flight `feat/hook-sync-and-matcher-fix` branch — see `.claude/skills/task-builder/SKILL.md` ↔ `src/superclaude/skills/task-builder/SKILL.md` parity confirmed via `diff` in §3 of `evidence.md`).

## 8. Dependencies and cross-references

- **Dependencies:** T05.05 (D-0058, F-set + 4-step rule ratified — the new subsection ties to Step 1 (L1054) and Step 2 (L1055) of that rule); FR-CONV.6 dedup-key wire-shape spec (M6 mutual — the new subsection adopts the DM-003 `dedup_key=(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple as the bookkeeping key).
- **Unblocks:**
  - T05.08 (D-0060, preservation invariants + X-003 rejection — depends on T05.07; critical-path override).
  - T05.14 (D-0065, TEST-022 cross-cycle dedup pytest fixture — the runtime fixture that codifies the synthetic-log evidence here).
- **Wire ABI invariant:** The Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is the consumer-side regression-non-emission invariant for cross-cycle synth-dnsp transitions. Consumers (TEST-022 pytest assert at T05.14) MUST verify `grep -c "Regression detected on Item" <execution-log>` returns `0`; producers (rf-task-builder fix-cycle loops) MUST emit the F-set with dedup-key identity per SKILL.md L1042-1048.

## 9. Rollback

Per roadmap R-096 rollback note: the INV-012 operational subsection is the wiring layer for cross-cycle synth-dnsp persistence semantics. Rollback aligns with the FR-CONV.5 wrapper rollback policy (T05.01 / D-0054): the subsection can be removed by reverting the L1060-1076 range and restoring the original single blank-line gap between L1059 and the A.10 heading. The L1025 inline INV-012 reference inside the FR-CONV.5 wrapper (T05.01 baseline) is unchanged by T05.07, so on rollback the textual INV-012 composition note remains in place. Per-gate caps continue to govern fix-cycle escalation via the preserved `rf-team-lead.md:417` hard cap and the per-gate counter table at `rf-task-builder.md:354-364`.

## 10. Slice hashes (for downstream task verification)

| Slice | sha256 |
|---|---|
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline preserved) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `SKILL.md` L1029-1059 (API-004 contract block — T05.02 baseline preserved) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `SKILL.md` L1061-1075 (new INV-012 cross-cycle dedup composition subsection — T05.07 landing) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |
| `rf-team-lead.md:417` (3-cycle hard cap — untouched) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |
