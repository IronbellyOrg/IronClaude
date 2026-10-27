# D-0059 — Evidence (T05.07 — Wire INV-012 Cross-Cycle Dedup Composition)

**Task:** T05.07
**Roadmap items:** R-096
**Date:** 2026-05-17
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STRICT
**Verification method:** Sub-agent (quality-engineer) + synthetic-fixture self-consistency
**Overall: PASS** (4/4 AC met)

---

## 0. TL;DR

T05.07 lands a new dedicated **INV-012 cross-cycle dedup composition (operational rule)** subsection at `src/superclaude/skills/task-builder/SKILL.md` L1061-1075. The subsection is strictly additive — it sits between the strict-ordering invariant of the 4-step rule (L1059) and the `### A.10: Task File Validation` heading (now L1077). The four preservation invariants from T05.01–T05.05 are byte-identical.

Two synthetic execution-log fixtures (`fixture-cross-cycle-dedup-shrinking.log`, `fixture-cross-cycle-dedup-non-shrink.log`) jointly cover the three behavioral acceptance criteria. The quality-engineer sub-agent ratified all four ACs verbatim against the landed SKILL.md text and against the fixture grep counts (report at `quality-engineer-report.md`, §8 verdict: **PASS (STRICT TIER)**).

| AC | Statement (verbatim) | Sub-agent verdict | Evidence § |
|----|----------------------|-------------------|------------|
| AC1 | Cross-cycle synthetic same-dedup_key fixture contributes 1 to `F_n+1`, not 2 | PASS | §3 + §5 |
| AC2 | No regression halt emitted for the cross-cycle dedup case | PASS | §3 + §5 |
| AC3 | Monotonicity halt fires if cardinality is non-shrinking | PASS | §3 + §5 |
| AC4 | Sub-agent quality-engineer report confirms composition rule documented in SKILL.md | PASS | §4 (report §6) |

Preservation invariants (T05.01 + T05.02 + T05.03 + T05.04 + T05.05 baselines):
SKILL.md L1014-1027 sha256 `1ca8e16e…` unchanged; SKILL.md L1029-1059 sha256 `14c40575…` unchanged; `rf-team-lead.md:417` sha256 `51725c0f…` unchanged; `rf-task-builder.md` L354-364 sha256 `121de142…` unchanged. The new INV-012 subsection at L1061-1075 hashes to `5ff2a180…` and is the only T05.07 SKILL.md addition.

---

## 1. Pre-edit baseline hashes (preservation check)

```
$ sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5  -

$ sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099  -

$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -

$ sed -n '354,364p' src/superclaude/agents/rf-task-builder.md | sha256sum
121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1  -
```

All four match the T05.01..T05.05 baselines. T05.07 did NOT modify any of the four preserved regions.

## 2. New INV-012 subsection (SKILL.md L1061-1075)

The subsection is the only T05.07 source-file change. Verbatim contents:

```
$ sed -n '1061,1075p' src/superclaude/skills/task-builder/SKILL.md
**INV-012 cross-cycle dedup composition (operational rule):**

Synthetic-dnsp findings (PR-03 / FR-CONV.6) COUNT as failures for the `|F_n|` monotonicity comparison — they are real, citable evidence items. **BUT** a synthetic finding with an identical `dedup_key` `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a **DEDUP case, NOT a regression** — its prior-cycle verdict was already FAIL, not PASS. It contributes `1` (not `2`) to `|F_{n+1}|`, and if it persists with nothing else changing it WILL trip the monotonicity guard — the intended behavior. This is the cross-cycle wiring of the F-set identity rule above (L1042-1048).

**Cross-cycle dedup-key tracking (bookkeeping rule).** Each fix-cycle gate records, at end-of-cycle `n`, the FAIL-verdict set `F_n` keyed by dedup-key (ordinary item ID for checklist items; `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple for synthetic-dnsp findings — DM-003 contract row). The next cycle's `F_{n+1}` is computed by the same dedup-key identity, so a synthetic-dnsp finding with the same 2-tuple re-emitted on cycle `n+1` collapses with its cycle-`n` counterpart into a single element of `F_{n+1}` BEFORE the monotonicity comparison runs. No additional per-cycle state is required beyond the F-set itself.

**Regression vs. persistence (cross-cycle decision rule).** The regression check at Step 1 of the 4-step ordering rule (L1054) requires `dedup_key ∈ PASS_n ∩ FAIL_{n+1}`. A synthetic-dnsp finding whose dedup-key was in `F_n` (FAIL_n) and is again in `F_{n+1}` (FAIL_{n+1}) has dedup_key ∉ PASS_n, so it is NEVER a regression — it is **persistence**. Persistence trips Step 2 (monotonicity) if and only if it makes `|F_{n+1}| >= |F_n|` (intended halt — the partition agent is stuck). Persistence with strict shrink elsewhere (e.g., `F_n = {item-3.1, synthetic-K}`, `F_{n+1} = {synthetic-K}` → `|F_{n+1}| = 1 < 2 = |F_n|`) continues to cycle `n+2` per Step 4 (proceed).

**Worked examples (operational illustration):**

1. **Cross-cycle dedup, strict shrink, no halt.** Cycle 1 `F_1 = {item-3.1, item-3.2, synthetic-K}` (`|F_1|=3`); cycle 2 `F_2 = {item-3.2, synthetic-K}` (`|F_2|=2`). Step 1 regression check: `PASS_1 ∩ FAIL_2 = ∅` (item-3.1 was FAIL_1, not PASS_1; synthetic-K was FAIL_1). Step 2 monotonicity check: `|F_2|=2 < |F_1|=3` → strict shrink → PROCEED. Step 4 re-spawns cycle 3. Synthetic-K's cross-cycle persistence contributes 1 to `|F_2|` (not 2), per the dedup-key identity rule.
2. **Cross-cycle dedup, non-shrink, monotonicity halt (intended).** Cycle 1 `F_1 = {item-3.1, synthetic-K}` (`|F_1|=2`); cycle 2 `F_2 = {item-3.2, synthetic-K}` (`|F_2|=2`). Step 1 regression check: `PASS_1 ∩ FAIL_2 = ∅` (item-3.1 → PASS_2; item-3.2 was not in PASS_1; synthetic-K was FAIL_1). Step 2 monotonicity check: `|F_2|=2 >= |F_1|=2` → HALT `[HALT-MONOTONICITY] |F|=2`. The partition agent is stuck; the existing per-gate counter and the `rf-team-lead.md:417` 3-cycle backstop still govern the eventual hard-cap escalation if the operator overrides the monotonicity halt.
3. **Same-cycle dedup collapse (no cross-cycle interaction).** Two synthetic findings emitted on the SAME cycle with the same `dedup_key` collapse into one record with a `found N times` note (PR-03 emitter behavior). They contribute 1 to `|F_n|`, not 2. Cross-cycle composition then operates on the post-collapse set.

**Regression non-emission invariant (cross-cycle synthetic-dnsp).** A regression halt MUST NOT be emitted for any item whose dedup-key was in `F_n` (i.e., FAIL_n) — regardless of whether the item is a synthetic-dnsp finding or an ordinary checklist item. The Step 1 set predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is the only condition that fires the regression halt; cross-cycle dedup is excluded from regression by construction of the predicate. Consumers (fixture asserts) MUST verify `grep -c "Regression detected on Item" <execution-log>` returns `0` for any cross-cycle same-dedup_key transition; the cross-cycle synthetic-dnsp fixture (TEST-022 at T05.14 / D-0065) codifies this invariant.

$ sed -n '1061,1075p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785  -
```

## 3. Fixture verification (AC1, AC2, AC3)

Two synthetic execution-log fixtures landed under `D-0059/`:

### 3.1 `fixture-cross-cycle-dedup-shrinking.log` (AC1 + AC2 positive case)

Scenario: cycle 1 emits `F_1 = {item-3.1, item-3.2, synthetic-K}` (`|F_1|=3`); cycle 2 emits `F_2 = {item-3.2, synthetic-K}` (`|F_2|=2`, cross-cycle synthetic-K collapse to 1 element); cycle 3 emits `F_3 = ∅`. The fix-cycle protocol proceeds to cycle 3 without halt.

```
$ grep -c "Regression detected on Item" .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log
0                ← AC2 PASS — no regression halt for cross-cycle dedup

$ grep -c "^HALT " .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log
0                ← no halt of any kind on strict shrink

$ grep -c "^CYCLE 3 START" .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log
1                ← cycle 3 attempted (continues per Step 4)
```

AC1 verification (composition `1 not 2`): the fixture explicitly records `|F_2| = 2   (post-dedup cardinality; synth re-emitted with identical dedup_key collapses with cycle-1 entry into 1 element of F_2 per SKILL.md L1067)` at line 21. Without cross-cycle dedup-key identity the cardinality would be 3 (item-3.2 + cycle-1 synth + cycle-2 synth). The fixture cites SKILL.md L1067 (bookkeeping rule) and L1075-1079 (regression non-emission invariant) as the governing clauses.

### 3.2 `fixture-cross-cycle-dedup-non-shrink.log` (AC2 + AC3 positive case)

Scenario: cycle 1 emits `F_1 = {item-3.1, synthetic-K}` (`|F_1|=2`); cycle 2 emits `F_2 = {item-3.2, synthetic-K}` (`|F_2|=2`, cross-cycle synthetic-K collapse, item-3.2 NEW). The monotonicity guard halts at the cycle-2 → cycle-3 transition with byte-exact `[HALT-MONOTONICITY] |F|=2`. Cycle 3 is NOT attempted.

```
$ grep -c "Regression detected on Item" .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log
0                ← AC2 PASS — synth-K persistence is NOT a regression even with non-shrink

$ grep -c "^HALT \[HALT-MONOTONICITY\]" .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log
1                ← AC3 PASS — monotonicity halt fires when |F_2| >= |F_1|

$ grep -c "^CYCLE 3 START" .dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log
0                ← cycle 3 NOT attempted (monotonicity guard exits fix-cycle loop)
```

AC1 verification (composition `1 not 2`): the fixture explicitly records `|F_2| = 2   (post-dedup cardinality; synth-K re-emitted with identical dedup_key collapses with cycle-1 entry into 1 element of F_2 per SKILL.md L1067 — contributes 1, not 2)` at line 21. Without cross-cycle dedup the cardinality would be 3 (item-3.2 + cycle-1 synth-K + cycle-2 synth-K). The monotonicity halt fires at `|F_2|=2 >= |F_1|=2` per Step 2 (SKILL.md L1055).

AC3 verification (byte-exact monotonicity halt): the fixture emits `HALT [HALT-MONOTONICITY] |F|=2` at line 30 — byte-identical to the API-004 contract row at SKILL.md L1037 (`[HALT-MONOTONICITY] |F|=<n>` with `<n>=|F_2|=2`).

**Adversarial note (regression-count = 0 with item-3.2 ∈ FAIL_2):** A naïve regression check might fire on item-3.2 (FAIL_2, not in F_1). The fixture's narrative at line 25 explicitly disposes of this: item-3.2 was "simply not in F_1; it is a NEW failure mode this cycle, not a regression — regression requires prior-cycle PASS@N, see SKILL.md L1054". This matches SKILL.md L1054's Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}`: absence from `F_n` is necessary but not sufficient for regression — presence in `PASS_n` is required. The quality-engineer sub-agent independently flagged and confirmed this point (`quality-engineer-report.md` §7 "Adversarial note").

## 4. Sub-agent quality-engineer ratification (AC4)

A quality-engineer sub-agent was spawned READ-ONLY with the instruction "No edits permitted. Produce a structured verdict report." The sub-agent inspected:

- `src/superclaude/skills/task-builder/SKILL.md` lines 1014–1140 (FR-CONV.5 wrapper, API-004 contract block, new INV-012 subsection, A.10 heading)
- `src/superclaude/agents/rf-team-lead.md` line 417 (3-cycle hard cap)
- `src/superclaude/agents/rf-task-builder.md` lines 354-364 (per-gate counter table)
- Both fixtures under `D-0059/`

Report path: `.dev/releases/current/task-builder-merge/artifacts/D-0059/quality-engineer-report.md`

### 4.1 Sub-agent §6 (AC4) verbatim conclusion

> §6 verdict: AC4 PASS — heading is at line 1061 as specified; all five required content elements are present with verbatim text and worked numeric illustration.

The sub-agent walkthrough confirmed:

| Element | SKILL.md line | Status |
|---|---|---|
| Subsection heading | 1061 | YES (verbatim) |
| Composition rule "contributes 1 not 2" | 1063 (+ L1067 + L1074 reinforcements) | YES |
| Tracking bookkeeping rule | 1065-1067 | YES |
| Regression-vs-persistence decision rule | 1069 | YES |
| Worked examples (≥2 required) | 1071-1074 (3 examples — shrink, non-shrink, same-cycle contrast) | YES |
| Regression non-emission invariant | 1075 | YES |

### 4.2 Sub-agent overall verdict (§8) verbatim

> OVERALL: PASS (STRICT TIER)
>
> All four acceptance criteria are satisfied with verbatim, normatively-phrased text in the new SKILL.md L1061–1075 INV-012 subsection. All five preservation invariants (four hash regions + the A.10 heading adjacency) are byte-identical to baseline. Both synthetic execution-log fixtures self-consistently illustrate AC1–AC3 with all six grep assertions matching exactly.
>
> No ambiguities found. No edits made. T05.07 is ratified.

The sub-agent's six-row summary table (`quality-engineer-report.md` §8):

| Check | Verdict |
|---|---|
| §2 Preservation (4 hashes + heading adjacency) | PASS |
| §3 AC1 (1-not-2 composition) | PASS |
| §4 AC2 (no regression halt for cross-cycle dedup) | PASS |
| §5 AC3 (monotonicity halt on non-shrinking persistence) | PASS |
| §6 AC4 (subsection at L1061 with all five required elements) | PASS |
| §7 Fixture self-consistency (6 grep assertions across 2 fixtures) | PASS |

## 5. AC matrix (T05.07 verdict)

| AC | Acceptance criterion | Evidence | Sub-agent verdict | Status |
|---|---|---|---|---|
| AC1 | Cross-cycle synthetic same-dedup_key fixture contributes 1 to `F_n+1`, not 2 | §2 (L1063 verbatim) + §3.1 (`|F_2|=2` not 3 in shrinking fixture) + §3.2 (`|F_2|=2` not 3 in non-shrink fixture) | PASS (`quality-engineer-report.md` §3) | **PASS** |
| AC2 | No regression halt emitted for the cross-cycle dedup case | §2 (L1069 set-predicate derivation + L1075 MUST NOT invariant) + §3.1 (regression-count = 0) + §3.2 (regression-count = 0 even with synth-K persistence + item-3.2 NEW failure) | PASS (`quality-engineer-report.md` §4) | **PASS** |
| AC3 | Monotonicity halt fires if cardinality is non-shrinking | §2 (L1069 biconditional `if and only if`) + §3.2 (byte-exact `HALT [HALT-MONOTONICITY] |F|=2` + cycle 3 NOT attempted) | PASS (`quality-engineer-report.md` §5) | **PASS** |
| AC4 | Sub-agent quality-engineer report confirms composition rule documented in SKILL.md | §4 (sub-agent report walks all five required elements + §8 PASS) | PASS (`quality-engineer-report.md` §6 + §8) | **PASS** |

## 6. Preservation invariants (carried from T05.01..T05.06)

```
$ sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5  -      ← matches T05.01..T05.05 baseline

$ sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099  -      ← matches T05.02..T05.05 baseline

$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -      ← matches T05.01..T05.05 baseline

$ sed -n '354,364p' src/superclaude/agents/rf-task-builder.md | sha256sum
121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1  -      ← matches T05.01..T05.05 baseline
```

The four independent retry counters (RESEARCH_NEEDED, MALFORMED, research-gate gap-fill, per-gate fix cycles) and the global 3-cycle hard cap at `rf-team-lead.md:417` are PRESERVED end-to-end.

`### A.10: Task File Validation` heading still present at SKILL.md L1077 (one blank-line gap after INV-012 subsection ends at L1075). T05.07 inserted 16 lines between L1059 (strict-ordering invariant) and the A.10 heading; no other structural changes were made.

## 7. `src/` ↔ `.claude/` parity

```
$ diff src/superclaude/skills/task-builder/SKILL.md .claude/skills/task-builder/SKILL.md
$ echo "PARITY OK"
PARITY OK
```

The T05.07 SKILL.md edit was synced via `make sync-dev` immediately after the edit and confirmed with a no-op `diff`. The pre-existing repo-wide hook-script drift (unrelated to T05.07 — tracked separately on the in-flight `feat/hook-sync-and-matcher-fix` branch) does not affect SKILL.md parity.

## 8. Cross-reference to downstream M5 tasks

| Downstream task | Inherits from this task |
|---|---|
| T05.08 (D-0060, preservation invariants + X-003 rejection) | Critical-path override: T05.08 must re-verify `rf-team-lead.md:417` byte-identical, four-counter independence at `rf-task-builder.md:354-364`, and X-003 REJECTED on `|F|=5,4` slow-shrink. T05.07's preservation hashes (§6) feed directly into T05.08's byte-diff = 0 check. |
| T05.12 (CP-P05-T07-T11 mid-phase checkpoint) | One of three Verification bullets: "INV-012 cross-cycle dedup composition rule documented (D-0059 evidence)". |
| T05.14 (D-0065, TEST-017 slow-shrink + TEST-022 cross-cycle dedup pytest fixtures) | TEST-022 is the runtime pytest codification of `fixture-cross-cycle-dedup-shrinking.log` (this evidence §3.1) — same `F_1 = {item-3.1, item-3.2, synth-K}` → `F_2 = {item-3.2, synth-K}` setup, same regression-count = 0 assertion, same cycle-3-attempted assertion. |
| T05.18 (CP-P05-END end-of-phase checkpoint) | M5 Exit Conditions include "cross-cycle dedup not regression" — this is the T05.07 INV-012 wiring + TEST-022 codification. |
| M7 ESCALATION-OBSERVABILITY (FF_RETRY_MONOTONICITY_GUARDS audit) | The regression non-emission invariant at SKILL.md L1075 (consumer fixture assert) is a verifiable observability hook for the M7 K-005 false-halt-rate audit. |

## 9. Slice hashes (for downstream task verification)

| Slice | sha256 |
|---|---|
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline preserved) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `SKILL.md` L1029-1059 (API-004 contract block + F-set + 4-step rule — T05.02 baseline preserved) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `SKILL.md` L1061-1075 (new INV-012 cross-cycle dedup composition subsection — T05.07 landing) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |
| `rf-team-lead.md:417` (3-cycle hard cap — untouched) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |

---

## 10. Verdict

**T05.07 PASS — all 4 AC met.**

- **AC1:** Cross-cycle synthetic same-dedup_key contributes 1 to `|F_{n+1}|`, not 2 — verbatim at SKILL.md L1063 + reinforced at L1067 + L1074; fixture-shrinking `|F_2|=2` (would be 3 without cross-cycle collapse); fixture-non-shrink `|F_2|=2` (would be 3) ✅
- **AC2:** No regression halt emitted for cross-cycle dedup — set-predicate derivation at L1069 ("dedup_key ∉ PASS_n, so it is NEVER a regression — it is **persistence**") + normative MUST NOT invariant at L1075; both fixtures report `grep -c "Regression detected on Item" = 0` ✅
- **AC3:** Monotonicity halt fires if cardinality non-shrinking — biconditional at L1069 ("trips Step 2 (monotonicity) if and only if `|F_{n+1}| >= |F_n|`") + worked example 2 at L1073 (`|F_2|=2 >= |F_1|=2 → HALT [HALT-MONOTONICITY] |F|=2`); fixture-non-shrink emits the byte-exact halt payload + cycle-3-not-attempted ✅
- **AC4:** Sub-agent quality-engineer report confirms composition rule documented — `quality-engineer-report.md` §6 walks all five required AC4 elements; §8 overall verdict: **PASS (STRICT TIER) — No ambiguities found. No edits made. T05.07 is ratified.** ✅

**Overall: PASS** — all four acceptance criteria PASS, all four preservation invariants byte-identical, both fixtures self-consistent, sub-agent ratification PASS. T05.07 unblocks T05.08 (critical-path preservation invariants), T05.12 (mid-phase checkpoint), and T05.14 (TEST-022 pytest fixture).
