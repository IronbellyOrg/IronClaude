# T05.07 / D-0059 — Quality Engineer Strict-Tier Ratification

**Date:** 2026-05-17
**Tier:** STRICT (adversarial)
**Mode:** READ-ONLY (zero edits)
**Subject:** Roadmap R-096 — INV-012 cross-cycle dedup composition wired into fix-cycle protocol
**Verifier:** quality-engineer sub-agent (spawned by T05.07 orchestrator)

---

## §1 Identity and Scope

This report ratifies T05.07 byte-for-byte against the four acceptance criteria
(AC1–AC4) plus five preservation invariants and two fixture self-consistency
checks. The verifier used only Read, Grep, and Bash (sha256sum, sed -n,
grep -c). No Edit / Write / replace_content / replace_symbol_body /
insert_*_symbol calls were made against any source-of-truth file. The only
Write call in this session produced this report file under
`.dev/releases/current/task-builder-merge/artifacts/D-0059/` per the
ratification prompt's explicit output directive.

**Files inspected (read-only):**

- `src/superclaude/skills/task-builder/SKILL.md` (lines 1014–1140)
- `src/superclaude/agents/rf-team-lead.md` (line 417)
- `src/superclaude/agents/rf-task-builder.md` (lines 354–364)
- `.dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log`
- `.dev/releases/current/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log`

---

## §2 Preservation Hash Checks (5 hashes)

All five preservation invariants from T05.01–T05.05 are **byte-identical** to
their baselines.

| # | Region | Expected sha256 | Actual sha256 | Verdict |
|---|---|---|---|---|
| 1 | `SKILL.md L1014-1027` (FR-CONV.5 wrapper) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | PASS |
| 2 | `SKILL.md L1029-1059` (API-004 contract block) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | PASS |
| 3 | `rf-team-lead.md:417` (3-cycle hard cap) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | PASS |
| 4 | `rf-task-builder.md L354-364` (per-gate counter table) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | PASS |
| 5 | `### A.10: Task File Validation` heading still present immediately after the INV-012 subsection | — | Located at SKILL.md line **1077** (one blank line gap after INV-012 subsection ends at L1075) | PASS |

**§2 verdict: PASS — all four pre-existing structures are byte-preserved; the
A.10 heading remains structurally adjacent.**

Verification commands (reproducible):

```bash
sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
sed -n '417p'        src/superclaude/agents/rf-team-lead.md      | sha256sum
sed -n '354,364p'    src/superclaude/agents/rf-task-builder.md   | sha256sum
grep -n "### A.10"   src/superclaude/skills/task-builder/SKILL.md
```

---

## §3 AC1 — Cross-cycle synthetic same-dedup_key contributes 1, not 2

**Locate verbatim statement.** SKILL.md line 1063 (within the INV-012
subsection opening paragraph):

```
Synthetic-dnsp findings (PR-03 / FR-CONV.6) COUNT as failures for the `|F_n|` monotonicity comparison — they are real, citable evidence items. **BUT** a synthetic finding with an identical `dedup_key` `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a **DEDUP case, NOT a regression** — its prior-cycle verdict was already FAIL, not PASS. It contributes `1` (not `2`) to `|F_{n+1}|`, and if it persists with nothing else changing it WILL trip the monotonicity guard — the intended behavior. This is the cross-cycle wiring of the F-set identity rule above (L1042-1048).
```

The exact target phrase `contributes \`1\` (not \`2\`) to \`|F_{n+1}|\`` is
present verbatim. The clause is unambiguously scoped to "a synthetic finding
with an identical `dedup_key` `(assigned_files_range,
escalation_ladder_exhaust_point)` across consecutive cycles" — exactly the
AC1 condition.

A second, reinforcing occurrence appears in the bookkeeping paragraph
(L1067):

```
... a synthetic-dnsp finding with the same 2-tuple re-emitted on cycle `n+1` collapses with its cycle-`n` counterpart into a single element of `F_{n+1}` BEFORE the monotonicity comparison runs.
```

A third occurrence appears in the same-cycle dedup example (L1073, example 3):

```
Two synthetic findings emitted on the SAME cycle with the same `dedup_key` collapse into one record with a `found N times` note (PR-03 emitter behavior). They contribute 1 to `|F_n|`, not 2. Cross-cycle composition then operates on the post-collapse set.
```

The text explicitly distinguishes same-cycle collapse (example 3) from
cross-cycle composition (AC1), and asserts the "1 not 2" rule for both.

**§3 verdict: AC1 PASS — verbatim rule present, scoped correctly, redundantly
reinforced.**

---

## §4 AC2 — No regression halt emitted for cross-cycle dedup

**Locate verbatim statement.** SKILL.md line 1069 (regression-vs-persistence
paragraph):

```
**Regression vs. persistence (cross-cycle decision rule).** The regression check at Step 1 of the 4-step ordering rule (L1054) requires `dedup_key ∈ PASS_n ∩ FAIL_{n+1}`. A synthetic-dnsp finding whose dedup-key was in `F_n` (FAIL_n) and is again in `F_{n+1}` (FAIL_{n+1}) has dedup_key ∉ PASS_n, so it is NEVER a regression — it is **persistence**.
```

The reasoning is set-theoretically explicit: the regression predicate
requires intersection with `PASS_n`, but a persistent synthetic-dnsp's
dedup_key lives in `FAIL_n` (which is disjoint from `PASS_n` by construction
of the verdict partition). The text says "NEVER a regression … it is
**persistence**".

This is reinforced again in the regression-non-emission invariant paragraph
(L1075):

```
**Regression non-emission invariant (cross-cycle synthetic-dnsp).** A regression halt MUST NOT be emitted for any item whose dedup-key was in `F_n` (i.e., FAIL_n) — regardless of whether the item is a synthetic-dnsp finding or an ordinary checklist item. The Step 1 set predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is the only condition that fires the regression halt; cross-cycle dedup is excluded from regression by construction of the predicate.
```

The phrasing "MUST NOT be emitted" + "excluded from regression by
construction of the predicate" is a normative, structural invariant — not a
behavioral observation. It also pins the consumer-side fixture assert:
`grep -c "Regression detected on Item" <execution-log>` MUST return `0`.

**§4 verdict: AC2 PASS — exclusion from regression is stated by set-predicate
construction (the strongest possible form: "by construction") and is
mandatory (MUST NOT).**

---

## §5 AC3 — Monotonicity halt fires if cardinality is non-shrinking

**Locate verbatim statement.** SKILL.md line 1063 (closing clause of the
INV-012 opening paragraph):

```
... if it persists with nothing else changing it WILL trip the monotonicity guard — the intended behavior.
```

And reinforced at SKILL.md L1069 (regression-vs-persistence paragraph):

```
Persistence trips Step 2 (monotonicity) if and only if it makes `|F_{n+1}| >= |F_n|` (intended halt — the partition agent is stuck). Persistence with strict shrink elsewhere (e.g., `F_n = {item-3.1, synthetic-K}`, `F_{n+1} = {synthetic-K}` → `|F_{n+1}| = 1 < 2 = |F_n|`) continues to cycle `n+2` per Step 4 (proceed).
```

The phrasing "if and only if" is biconditional — non-shrinking is the
*only* trigger for the monotonicity halt during persistence, and strict
shrink unambiguously proceeds. The reference to Step 2 (monotonicity, defined
at SKILL.md L1055) ties the rule directly to the strict-ordering 4-step
protocol immediately preceding the INV-012 subsection.

The text additionally labels this "the intended behavior" / "intended halt"
twice, foreclosing the misreading that the halt is a side-effect to be
suppressed. Worked example 2 (L1072) computes the case concretely:
`|F_2|=2 >= |F_1|=2 → HALT [HALT-MONOTONICITY] |F|=2`.

**§5 verdict: AC3 PASS — monotonicity halt is bound to non-shrinking
cardinality by biconditional, tied to Step 2 of the existing 4-step rule, and
labeled intended behavior.**

---

## §6 AC4 — Subsection walkthrough

**Subsection heading verbatim (SKILL.md line 1061):**

```
**INV-012 cross-cycle dedup composition (operational rule):**
```

Confirmed at line 1061 by `sed -n '1061p'`. The line preceding (L1059) is
the strict-ordering invariant terminator of the 4-step rule; L1060 is a
blank gap line; L1061 opens the new INV-012 subsection. The subsection
terminates at line 1075; line 1076 is a blank gap; line 1077 begins
`### A.10: Task File Validation`. The placement is exactly as specified:
between the 4-step rule terminator and the A.10 heading, additive.

**Paragraph-by-paragraph coverage walkthrough:**

| ¶ | Line(s) | Topic | Required AC4 element | Covered |
|---|---|---|---|---|
| Heading | 1061 | Subsection title | Subsection heading at L1061 | YES (verbatim above) |
| ¶1 (opener) | 1063 | F-set counting + "1 not 2" + monotonicity tie-in | Composition (contributes 1 not 2) | YES (verbatim §3) |
| ¶2 (bookkeeping) | 1065–1067 | Dedup-key tracking rule, F_n → F_{n+1} collapse before monotonicity | Tracking bookkeeping rule | YES |
| ¶3 (regression vs persistence) | 1069 | Step 1 predicate analysis, persistence definition, biconditional with Step 2 | Regression-vs-persistence decision rule | YES (verbatim §4, §5) |
| ¶4 heading | 1071 | "Worked examples (operational illustration):" | Worked-examples header | YES |
| ¶4 ex 1 | 1072 | Cross-cycle dedup, strict shrink, no halt — full numeric trace | Worked example (shrink case) | YES |
| ¶4 ex 2 | 1073 | Cross-cycle dedup, non-shrink, intended monotonicity halt — full numeric trace | Worked example (non-shrink case) | YES |
| ¶4 ex 3 | 1074 | Same-cycle dedup collapse vs cross-cycle composition | Worked example (third — exceeds ≥2 floor) | YES |
| ¶5 (invariant) | 1075 | Regression non-emission invariant + consumer fixture assert | Regression-non-emission invariant | YES (verbatim §4) |

**Element checklist (AC4 requirements):**

- [x] Composition rule "contributes 1 not 2" stated — ¶1 (L1063), ¶3 (L1067 reinforcement), ¶4 ex 3 (L1074 reinforcement)
- [x] Tracking bookkeeping rule — ¶2 (L1065–1067), pins dedup-key as `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple per DM-003 contract row
- [x] Regression-vs-persistence decision rule — ¶3 (L1069), set-predicate derivation
- [x] Worked examples — three examples (≥2 required); two cross-cycle (shrink + non-shrink) plus a same-cycle contrast
- [x] Regression-non-emission invariant — ¶5 (L1075), normative MUST NOT + by-construction grounding + fixture assert

All five required AC4 elements are present with verbatim text and tied to
existing structural anchors (Step 1/Step 2 of the 4-step rule at L1054/1055,
the F-set identity rule at L1042-1048, the API-004 contract block at
L1029-1059, the DM-003 contract row, the rf-task-builder per-gate cap table
at L354-364, and the rf-team-lead 3-cycle backstop at L417).

**§6 verdict: AC4 PASS — heading is at line 1061 as specified; all five
required content elements are present with verbatim text and worked numeric
illustration.**

---

## §7 Fixture Verification

Two synthetic execution-log fixtures landed under
`.dev/releases/current/task-builder-merge/artifacts/D-0059/`. Required
grep counts and observed values:

### Fixture 1: `fixture-cross-cycle-dedup-shrinking.log`

| Assertion | Required | Observed | Verdict |
|---|---:|---:|---|
| `grep -c "Regression detected on Item"` (AC2) | 0 | 0 | PASS |
| `grep -c "^HALT "` (AC1 — no halt in shrink case) | 0 | 0 | PASS |
| `grep -c "^CYCLE 3 START"` (cycle 3 attempted) | 1 | 1 | PASS |

Self-consistency trace: `F_1={item-3.1, item-3.2, synth-K}` `|F_1|=3` →
`F_2={item-3.2, synth-K}` `|F_2|=2 < 3` (strict shrink, synth-K cross-cycle
persistence contributes 1 not 2) → CYCLE 3 starts → `F_3=∅`, gate
converges. The fixture cites SKILL.md L1061-1079 and L1067 as the governing
clauses, and pins the API-004 contract block sha256
`14c40575…` — matching the §2 preservation hash.

### Fixture 2: `fixture-cross-cycle-dedup-non-shrink.log`

| Assertion | Required | Observed | Verdict |
|---|---:|---:|---|
| `grep -c "Regression detected on Item"` (AC2 — no regression for synth-K persistence OR for new failure item-3.2 not previously PASS) | 0 | 0 | PASS |
| `grep -c "^HALT "` (AC3 — monotonicity halt fires) | 1 | 1 | PASS |
| `grep -c "^CYCLE 3 START"` (cycle 3 NOT attempted) | 0 | 0 | PASS |

Self-consistency trace: `F_1={item-3.1, synth-K}` `|F_1|=2` → cycle 2
yields `F_2={item-3.2, synth-K}` `|F_2|=2 >= |F_1|=2` (non-shrink, synth-K
persistence still contributes 1 not 2; item-3.2 is a *new* failure not in
`PASS_1` in a regression-eligible sense — the fixture's prose distinguishes
"new failure mode" from regression and notes item-3.2 was "simply not in
`F_1`"). The halt message is the byte-exact `[HALT-MONOTONICITY] |F|=2` per
the API-004 contract row (SKILL.md L1037). Cycle 3 is explicitly NOT
started; rf-team-lead.md:417 3-cycle backstop is explicitly NOT consulted
because the FR-CONV.5 monotonicity guard exits earlier.

**§7 verdict: PASS — both fixtures self-consistently illustrate AC1/AC2 in
the shrink case and AC2/AC3 in the non-shrink case, with all six grep
assertions matching their required counts exactly.**

**Adversarial note:** Fixture 2's regression-count of 0 is non-trivial. A
naïve regression check might fire on item-3.2 (FAIL in cycle 2, not in
F_1) — the fixture's narrative correctly disposes of this: item-3.2 was
"simply not in F_1; it is a NEW failure mode this cycle, not a regression —
regression requires prior-cycle PASS@N, see SKILL.md L1054". This matches
SKILL.md's Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}`: absence from
`F_n` is necessary but not sufficient for regression; presence in `PASS_n` is
required. The fixture correctly enforces the predicate.

---

## §8 Overall Verdict

**OVERALL: PASS (STRICT TIER)**

All four acceptance criteria are satisfied with verbatim, normatively-phrased
text in the new SKILL.md L1061–1075 INV-012 subsection. All five preservation
invariants (four hash regions + the A.10 heading adjacency) are byte-identical
to baseline. Both synthetic execution-log fixtures self-consistently
illustrate AC1–AC3 with all six grep assertions matching exactly.

| Check | Verdict |
|---|---|
| §2 Preservation (4 hashes + heading adjacency) | PASS |
| §3 AC1 (1-not-2 composition) | PASS |
| §4 AC2 (no regression halt for cross-cycle dedup) | PASS |
| §5 AC3 (monotonicity halt on non-shrinking persistence) | PASS |
| §6 AC4 (subsection at L1061 with all five required elements) | PASS |
| §7 Fixture self-consistency (6 grep assertions across 2 fixtures) | PASS |

**No ambiguities found. No edits made. T05.07 is ratified.**

**Reasoning:** The INV-012 subsection is structurally additive (sits between
L1059 strict-ordering invariant terminator and L1077 A.10 heading), does not
mutate any preserved region (all four hashes match T05.01–T05.05 baselines),
and operationalises the cross-cycle dedup composition rule using
set-theoretic derivation (Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}`)
that mathematically excludes cross-cycle persistence from regression by
construction. The biconditional binding to Step 2 (monotonicity) gives
unambiguous halt behavior on non-shrinking cardinality. The three worked
examples (two cross-cycle, one same-cycle contrast) cover both AC verdicts
(shrink → proceed; non-shrink → halt) and the same-cycle baseline. The
regression-non-emission invariant uses MUST NOT and ties to a verifiable
consumer assert (`grep -c "Regression detected on Item"` MUST return 0).
Both fixtures pin the API-004 contract block sha256 and satisfy all six
grep assertions on the first read.
