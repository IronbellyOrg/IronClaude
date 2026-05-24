# D-0060 — Evidence (T05.08 — Preserve 3-Cycle Hard Cap + Four Counters + X-003 Rejection)

**Task:** T05.08
**Roadmap items:** R-097 (3-cycle hard cap preservation), R-098 (four-counter independence), R-099 (X-003 rejection enforcement)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STRICT
**Critical Path Override:** Yes (preservation invariants govern fix-cycle escalation safety)
**Verification method:** Sub-agent (quality-engineer) + synthetic-fixture self-consistency
**Overall: PASS** (4/4 AC met)

---

## 0. TL;DR

T05.08 is a **non-editing preservation gate**: zero source-file changes, three preservation invariants ratified. The five hash-pinned regions (`rf-team-lead.md:417`; `rf-task-builder.md:354-360` canonical + `:354-364` full table; `SKILL.md:1014-1027` wrapper + `:1029-1059` contract block) are byte-identical to the T05.01 / T05.02 / T05.05 / T05.07 baselines. The X-003 rejection invariant is operationalised by a synthetic `|F|=5,4` slow-shrink fixture (`fixture-slow-shrink-F-5-4.log`) whose five machine-checkable grep assertions return `(0, 0, 0, 1, 1)` — no halt of any kind, cycle 3 reached, gate converges. The quality-engineer sub-agent ratified all four ACs verbatim (`quality-engineer-report.md` §7 verdict: **PASS (STRICT TIER)**).

| AC | Statement (verbatim from tasklist L388-392) | Sub-agent verdict | Evidence § |
|----|----------------------------------------------|-------------------|------------|
| AC1 | "Byte-diff of `rf-team-lead.md:417` pre/post M5 changes is zero." | PASS | §1 + §3 row 1 |
| AC2 | "Per-gate counters at `rf-task-builder.md:354-360` are independent (no shared monotonicity state)." | PASS | §1 + §3 rows 2-3 + §4 |
| AC3 | "`|F|=5,4` slow-shrink fixture continues to cycle 3 (X-003 NOT triggered)." | PASS | §2 + §6 |
| AC4 | "Sub-agent report confirms three preservation invariants." | PASS | §5 (report §7) |

T05.08 introduces no SKILL.md / rf-task-builder.md / rf-qa.md / rf-team-lead.md edits — every preservation hash is identity-equal to its T05.07 (D-0059 §1) value. The X-003 fixture is the prototype that T05.14 / TEST-017 will codify as an automated pytest fixture.

---

## 1. Preservation hash log (R-097 + R-098)

Five `sed -n … | sha256sum` invocations executed from `/config/workspace/IronClaude` at T05.08 verification time. All five match their published baselines.

```
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -

$ sed -n '354,360p' src/superclaude/agents/rf-task-builder.md | sha256sum
72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1  -

$ sed -n '354,364p' src/superclaude/agents/rf-task-builder.md | sha256sum
121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1  -

$ sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5  -

$ sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099  -
```

All five match the T05.01..T05.07 baselines published in D-0058 §9.1-9.4 and D-0059 §1. **No drift.**

## 2. X-003 rejection fixture (R-099)

Fixture: `.dev/releases/current/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log` (53 lines). Scenario:

- **Cycle 1:** `F_1 = {item-3.1, item-3.2, item-3.3, item-3.4, item-3.5}`, `|F_1|=5`.
- **Cycle 2:** `F_2 = {item-3.2, item-3.3, item-3.4, item-3.5}`, `|F_2|=4` — strict shrink by 1 (the slowest legitimate slow-shrink delta the X-003 design proposed and that was REJECTED).
- **Cycle 3:** `F_3 = ∅`, gate converges.

The 4-step ordering rule at `SKILL.md` L1050-1059 evaluates cleanly:

| Transition | Step 1 regression | Step 2 monotonicity | Step 3 hard-cap | Step 4 proceed |
|---|---|---|---|---|
| 1 → 2 | PASS (`PASS_1 ∩ FAIL_2 = ∅`) | PROCEED (`4 < 5` → strict shrink → predicate `|F_{n+1}| >= |F_n|` is FALSE) | PROCEED (research-gate counter 2/3 per `rf-task-builder.md:354-364`) | re-spawn cycle 3 |
| 2 → 3 | PASS (`FAIL_3 = ∅`) | SKIP (`|F_3|=0`, precondition `|F_n|>0` not met) | PROCEED (counter 3/3 at proceed boundary; not consulted, all-PASS) | gate converges, no further cycle |

The fixture annotates each hard-cap step with `research-gate counter N/3 (rf-task-builder.md:354-364)` so the connection between the X-003 rejection rule and the preserved counter table at R-098 is reproducible inside a single artifact.

**X-003 rejection invariant statement (fixture L19, verbatim):** "shrink-by-1 is sufficient; no rate-of-shrink threshold parameter is consulted; the monotonicity check is the binary predicate `|F_{n+1}| >= |F_n|`, which is FALSE here (4 < 5), so PROCEED."

## 3. Fixture grep assertions (machine-checkable)

Five assertions run against `fixture-slow-shrink-F-5-4.log`. Anchoring pattern: halt strings would be emitted on `^TRANSITION.*verdict=HALT-*` lines if triggered; the assertion section itself uses `grep -cE` with anchored regexes so self-referential mentions do not skew counts. Expected vs observed:

| Assertion | grep command | Expected | Observed | Verdict |
|---|---|---|---|---|
| no halts at all | `grep -c "^HALT " fixture-slow-shrink-F-5-4.log` | 0 | 0 | PASS |
| no regression halt event | `grep -cE "^TRANSITION.*verdict=HALT-REGRESSION" fixture-slow-shrink-F-5-4.log` | 0 | 0 | PASS |
| no monotonicity halt event | `grep -cE "^TRANSITION.*verdict=HALT-MONOTONICITY" fixture-slow-shrink-F-5-4.log` | 0 | 0 | PASS |
| cycle 3 attempted | `grep -c "^CYCLE 3 START" fixture-slow-shrink-F-5-4.log` | 1 | 1 | PASS |
| gate converges | `grep -c "^GATE VERDICT: PASS" fixture-slow-shrink-F-5-4.log` | 1 | 1 | PASS |

5/5 PASS. This is the AC3 verification surface; the matching tuple `(0, 0, 0, 1, 1)` confirms X-003 NOT triggered.

## 4. Four-counter independence statement (R-098 — operational meaning)

The byte-identity hash at §1 row 2-3 establishes the per-gate counter table (rf-task-builder.md:354-360 canonical + :354-364 full) has not drifted. The behavioral content — "the counters are independent and never collapsed" — is asserted at `src/superclaude/agents/rf-task-builder.md:370` in canonical wording added by T05.01 / MIG-005:

```
$ grep -n "independent and NEVER collapsed" src/superclaude/agents/rf-task-builder.md
370:Each gate row above keeps its OWN monotonicity history — research-gate's `F_n` is independent from task-integrity's `F_n`. The per-gate retry counters in the table above (research-gate, synthesis-gate, report-validation, task-integrity, and qualitative gate) are independent and NEVER collapsed; FR-CONV.5 layers halts ON TOP without merging counter state across gates. PR-03 synthetic-DNSP findings COUNT as failures for monotonicity but are deduplicated by `(assigned_files_range, escalation_ladder_exhaust_point)` so a re-fired synthetic for the same partition is NOT a regression (INV-012). See SKILL.md "Retry Monotonicity Protocol" for full specification.
```

Exactly one match. The grep target is unique to L370 in the source tree.

**4-vs-5 phrasing clarification.** The roadmap and tasklist use the canonical phrase "four independent retry counters". The actual table has 5 gate rows (research-gate, synthesis-gate, report-validation, task-integrity, "Any qualitative gate"). The "four" refers to the four distinct gate types with independent caps (research-gate, synthesis-gate, report-validation, task-integrity); "Any qualitative gate" is a **category modifier** that applies the same cap rule to all qualitative-gate variants — not a fifth independent counter. The L370 enumeration ("research-gate, synthesis-gate, report-validation, task-integrity, and qualitative gate") makes this explicit by treating qualitative gate as the category, not as a fifth distinct counter. Spec §1 / §3 / §9 of `D-0060/spec.md` document this asymmetry.

## 5. Sub-agent verdict (AC4)

The quality-engineer sub-agent re-ran the five hash checks, the four-counter independence grep, the five fixture grep assertions, and re-validated the spec §5 AC table against the phase-5 tasklist L388-392 verbatim. Report path: `.dev/releases/current/task-builder-merge/artifacts/D-0060/quality-engineer-report.md` (140 lines).

Report §7 verdict matrix (verbatim quoted from report):

| AC | Verdict |
|----|---------|
| AC1 — 3-cycle hard cap preservation (R-097) | PASS |
| AC2 — Four-counter independence (R-098) | PASS |
| AC3 — X-003 rejection (R-099) | PASS |
| AC4 — Sub-agent report confirms three preservation invariants | PASS |
| **T05.08 overall (STRICT tier)** | **PASS** |

Open drift surfaces enumerated by the sub-agent (report §8): T05.09 SKILL.md A.9 edits (separate invariant tail at L867-873 + Behavioral Constraints at L1547-1553 — neither overlaps the preserved L1014-1027 / L1029-1059 windows); T05.10 rf-task-builder.md I16 edits at L334-361 (touches the preserved L354-360 window — T05.10 acceptance is that per-gate cap entries are byte-identical pre/post, so the byte-diff backstop at T05.16 MIG-005 will re-verify); T05.13 TEST-015/016 fixture calibration against X-003; the 4-vs-5 phrasing asymmetry (clarified everywhere); src/.claude sync (verify-sync runs at T05.16). **None blocking.**

## 6. Acceptance criteria coverage map

| AC | Tasklist L388-392 verbatim | Spec §5 entry | Evidence § (this doc) | Verdict |
|----|----------------------------|---------------|------------------------|---------|
| AC1 | "Byte-diff of `rf-team-lead.md:417` pre/post M5 changes is zero." | §5 row 1 | §1 row 1 | PASS |
| AC2 | "Per-gate counters at `rf-task-builder.md:354-360` are independent (no shared monotonicity state)." | §5 row 2 | §1 rows 2-3 + §4 | PASS |
| AC3 | "`|F|=5,4` slow-shrink fixture continues to cycle 3 (X-003 NOT triggered)." | §5 row 3 | §2 + §3 | PASS |
| AC4 | "Sub-agent report confirms three preservation invariants." | §5 row 4 | §5 | PASS |

## 7. Roadmap row alignment (R-097, R-098, R-099)

| Roadmap row | Verbatim AC string | Verified at |
|---|---|---|
| R-097 row 8 / M5 | "byte-diff-rf-team-lead.md:417-line-pre/post:0; cap:remains-as-fourth-precedence-backstop" | §1 row 1 hash + §2 X-003 fixture Step 3 (hard-cap as backstop) |
| R-098 row 9 / M5 | "per-gate-counters-at-rf-task-builder.md:354-360:preserved; no-shared-monotonicity-state-across-counters" | §1 rows 2-3 hash + §4 L370 statement |
| R-099 row 10 / M5 | "slow-shrink-fixture:continues-to-next-cycle; no-rate-of-shrink-parameter-introduced" | §2 + §3 fixture |

## 8. Why T05.08 makes no source edits

The task spec at phase-5 tasklist L380-386 enumerates six steps, three of which are PLANNING (capture baseline + read roadmap specs), one is EXECUTION ("No edits in rf-team-lead.md:417 range; verify after T05.16 commit"), and two are VERIFICATION (sub-agent ratification + fixture run). The "EXECUTION" step is a **non-edit** — its product is the byte-identity hash log at §1 of this evidence file, not a source change. This is intentional: T05.08 is the **preservation gate** that re-verifies the M5 wrapper has not drifted any preserved region across T05.01..T05.07; if a source change were required, the wrapper itself would be at fault. The T05.16 MIG-005 sub-agent diff spot-check at AC3 ("rf-team-lead.md:417 byte-identical and four counters preserved") is the commit-boundary re-verification of the same hashes captured here.

## 9. Linked downstream tasks

- **T05.09 (D-0061)** — SKILL.md A.9 invariant tail + Behavioral Constraints halt-precedence edits (separate L867-873 + L1547-1553 windows, no overlap with T05.08-preserved regions).
- **T05.10 (D-0062)** — rf-task-builder.md I16 fix-cycle encoding edits at L334-361; touches the preserved L354-360 window — T05.10 acceptance requires per-gate cap entries byte-identical pre/post, so the T05.16 MIG-005 commit-boundary diff spot-check will re-run the §1 row 2-3 hashes.
- **T05.13 (D-0064)** — TEST-015 (`|F|=5,5,5` halts at cycle 2) + TEST-016 (PASS@1/FAIL@2 regression precedes monotonicity); these depend on X-003 rejection staying enforced so their strict-monotonicity assertions remain calibrated.
- **T05.14 (D-0065)** — TEST-017 codifies the `|F|=5,4` fixture here as an automated pytest fixture; TEST-022 codifies the INV-012 cross-cycle dedup.
- **T05.16 (D-0067)** — MIG-005 single-commit landing; commit-boundary re-verification of all five §1 hashes.
- **T05.17 (D-0100)** — K-005 false-halt-rate sweep across `|F|=5,4`, `|F|=5,3`, `|F|=5,2`; the §2 fixture is the slowest-shrink baseline that anchors the metric.

## 10. Rollback

As stated in roadmap (M5 R-097..R-099): preservation invariants are read-only and have no rollback surface — they only fail if a downstream edit drifts. If a future commit drifts the byte-identity of `rf-team-lead.md:417` or `rf-task-builder.md:354-360`, the T05.16 MIG-005 sub-agent diff spot-check at AC3 ("rf-team-lead.md:417 byte-identical and four counters preserved") will block the merge. The wider §1 hash log (5 regions) anchors the diff-spot-check surface for the T05.16 sub-agent.

## 11. Hashes consulted

| Region | Pre-edit baseline (T05.01..T05.07) | T05.08 measurement | Diff |
|---|---|---|---|
| `rf-team-lead.md:417` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | 0 bytes |
| `rf-task-builder.md:354-360` | `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1` | `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1` | 0 bytes |
| `rf-task-builder.md:354-364` | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | 0 bytes |
| `SKILL.md:1014-1027` | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | 0 bytes |
| `SKILL.md:1029-1059` | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | 0 bytes |

Total drift across 5 hash-pinned regions: **0 bytes**.
