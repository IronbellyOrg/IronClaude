# Synthesis Quality Review — Gate A (Partition A)

**Analysis type:** synthesis-accuracy (partition A)
**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep TDD
**Date:** 2026-06-21
**fix_authorization:** false (report-only; no edits performed)
**Files reviewed:** 5 — synth-01..synth-05
**Source research dir:** `.dev/tasks/to-do/TASK-TDD-20260621-124414/research/`
**Template:** `src/superclaude/examples/tdd_template.md` (v1.2)

Assigned files (verbatim slice):

- `synth-01-exec-problem-goals.md` (§1–§4)
- `synth-02-requirements.md` (§5)
- `synth-03-architecture.md` (§6)
- `synth-04-data-api.md` (§7–§8)
- `synth-05-state-components.md` (§9–§11)

---

## Overall Verdict: FAIL — 6 issues (0 Critical, 2 High, 3 Medium, 1 Low)

The five synth files are template-aligned, evidence-dense, and traceable to the research
corpus. The backend/library tailoring is largely correct: the six canonical `runtime_surface_*`
scalar names match research/03 verbatim; the ledger schema, reduction precedence, and count
invariant are present and correct; §9/§10 are correctly N/A with rationale; the reflect→audit
import-boundary decision is surfaced with three options and a recommendation. However the review
found accuracy defects — most consequentially a recurring **5-vs-4 eval-case enumeration error**
that appears in three of the five files — that fail the gate under the "any accuracy error =
surface it; gate FAILs on unresolved findings" rule. Specifics below.

---

## 9-Criteria Checklist Results (per file)

| # | Criterion | s01 | s02 | s03 | s04 | s05 |
|---|-----------|-----|-----|-----|-----|-----|
| 1 | Section headers match template | PASS | PASS | PASS | PASS | PASS |
| 2 | Table column structure (FR/NFR, entity Field/Type/Required/Description/Constraints) | n/a | PASS | n/a | PASS | n/a |
| 3 | No fabrication beyond research (5-claim trace) | PASS | PASS | PASS | PASS | PASS |
| 4 | Findings cite actual file paths | PASS | PASS | PASS | PASS | PASS |
| 5 | Section 6 Architecture includes a diagram | -- | -- | PASS | -- | -- |
| 6 | FR-001/NFR-001 + priority + acceptance criteria | n/a | PASS | n/a | n/a | n/a |
| 7 | Cross-references consistent | FAIL | PASS | PASS | PASS | FAIL |
| 8 | No doc-only claims in 6/7/8 ([CODE-VERIFIED] or labeled spec-design) | -- | -- | PASS | PASS | -- |
| 9 | Stale-doc discrepancies surfaced (Section 22) | n/a | n/a | n/a | partial | n/a |

`n/a` = criterion does not apply to that file's section scope. `--` = not in scope for that file.
Criterion 9 is `partial` for s04 because the stale `contract_version` /
`REFLECT_CONTRACT_VERSION = "1.0"` discrepancies ARE surfaced inline (s04 §8.3, s02 §5.3 G3) but
Section 22 Open Questions is owned by another section/partition -- see Issue 6.

---

## Backend/Library Tailoring Verification (spawn-prompt specifics)

| Tailoring check | Result | Evidence |
|-----------------|--------|----------|
| s04 §8 documents six canonical `runtime_surface_*` scalars, names match research/03 | PASS | s04 §8.2 table lists all six; byte-match research/03 lines 27-32 |
| s04 §8 documents module/function API (not HTTP) | PASS | s04 §8.1 "no HTTP endpoints… REPURPOSED to module/function API" + 6 signatures |
| s04 §7 has ledger schema + reduction precedence + count invariant | PASS | §7.1 row shape; §7.2 `DEGRADE > UNREACHED > REACHED`; §7.4 count invariant |
| s05 §9/§10 N/A with rationale | PASS | Both marked N/A with backend/library rationale |
| s03 §6.4 reflect→audit import-boundary (3 options + recommendation) | PASS | §6.4 D1: Option C v1, Option B long-term, Option A avoid; grounded in research/05 §7 |
| Sixth-field prefix caveat surfaced | PASS | s04 §8.2 CRITICAL caveat; s02 §5.3 G4 |

The tailoring is sound. The defects are accuracy/consistency errors layered on a correct backbone.

---

## Findings (by severity)

### Issue 1 — HIGH — Eval-case tables enumerate 5 cases as only 4 rows (cross-reference + accuracy error)

**Files:** synth-01 §4.1 ("Per-case deterministic expectations"), synth-02 FR-008 acceptance
criteria, synth-05 §11.2 "Success Criteria (AC-2)".

**What's wrong:** All three files state "the 5 FR-RSR eval cases (ids 37-41)" but render a
**4-row** case table that collapses two distinct cases into one. synth-01 §4.1 and synth-05 §11.2
use a row labeled `unwired / test-only` (or `unwired / test-only-ref`), merging case 37 and case
41 into a single line. synth-02 FR-008 does the same in prose: "unwired/test-only → UNREACHED +
count invariant".

**Why it's an error (ground truth):** research/04 §"The 5 cases" (lines 92–122, 175–180) and
research/00 AC-2 (line 96) enumerate **five separate cases**, of which 37 and 41 are *different*
fixtures with *different* assertion focus:
- Case **37** `uc2-unwired-surface-passes` — the headline FAIL-pre/PASS-post case; emits
  `runtime_surface_unreached>=1` + Regression, suppresses clean PASS (research/04:176).
- Case **41** `uc2-surface-test-only-ref` — test/comment-only referrer; UNREACHED, **and is the
  host of the `yaml_list_len_eq` count-invariant assertion** (research/04:122, 180).

These are not the same case: 37 is "no production referrer at all," 41 is "only test/comment
referrers," and 41 is specifically the count-invariant host. Collapsing them into one row both
under-counts the table (4 ≠ the stated 5) and erases case 41's distinct count-invariant role.

**Severity rationale:** HIGH — the AC-2 case set is load-bearing for the Testing Strategy (§15)
and the determinism guarantee; an off-by-one case table propagated across three files will mislead
the implementer about how many fixtures must pass and which one hosts the count-invariant check.

**Fix (for the owning agent):** expand each 4-row table to 5 rows, separating case 37
(`unwired-surface-passes`) from case 41 (`test-only-ref`), and tag case 41 as the count-invariant
host. Source: research/04 lines 92–122, 175–180.

---

### Issue 2 — HIGH — synth-01 §2.2 symptom table misattributes the `unreachable_surfaces` improvised name to the wrong path / wires a forbidden-name claim that overstates the spec

**File:** synth-01 §2.2 symptom table, row "Ad-hoc field names on non-escalating paths".

**What's wrong:** The row reads: "quiet-UNREACHED emitted `surface_production_reachable: false` /
`unreachable_surfaces` — all after the prose was strengthened to forbid them." The clause "all
after the prose was strengthened to forbid them" asserts that the strengthened SKILL.md prose
**explicitly forbade** each of these three names. Ground truth (research/00 §3 lines 45–49) lists
the improvised names observed but says the prose "was strengthened to forbid exactly those names"
only for the headline set. research/03 §1.1 (lines 44–46) records the names the comment
**explicitly** forbids: `runtime_surface_reachable`, `reachability_path`,
`static_caller_absent_is_expected` — it does **not** list `surface_production_reachable`,
`surface_reachability_verdict`, or `unreachable_surfaces` among the explicitly-forbidden tokens.

So the synth-01 claim that all three observed improvised names were specifically forbidden by the
strengthened prose is **stronger than the evidence**. The names were *observed* (research/00) but
only a different subset is *documented as explicitly forbidden* (research/03 §1.1).

**Severity rationale:** HIGH — this is the problem-statement evidence that justifies the entire
feature; an overstated "the prose forbade X and X persisted anyway" claim is exactly the kind of
fabrication-adjacent embellishment a TDD reviewer must catch. The underlying argument (improvised
names persisted despite strengthening) is true; the specific "forbade exactly these" attribution
is not fully supported for all three names.

**Fix:** soften to "improvised names were observed on the non-escalating paths even after the
prose was strengthened" and, if listing explicitly-forbidden tokens, cite the research/03 §1.1 set
(`runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`) rather than
implying the observed names were all named in the forbid-list.

---

### Issue 3 — MEDIUM — synth-04 §8.2 "Consumer-that-reads-it" overstates sprint-executor as a live reader without the SPEC-ONLY caveat in every row

**File:** synth-04 §8.2 contract-field surface table.

**What's wrong:** The table lists "sprint executor SPEC-ONLY" for `runtime_surface_unreached` and
`unreached_surfaces`, which is correct. But the broader synth narrative (synth-02 FR-006, synth-03
§6.3) repeatedly names "the `sprint run` executor" as a consumer that "MUST consume the
deterministically-written scalars." research/03 §5.2/§5.3 and synth-02 §5.3 G2 establish the
ground truth: `cli/sprint/executor.py` **reads no reflect contract today** (imports `TurnLedger`
for budget only); wiring it is "a net-new integration, not a field-read swap."

synth-02 G2 surfaces this honestly as a gap, and synth-04 tags it SPEC-ONLY — so the *data* is
present. The inconsistency is that synth-03 §6.3 / FR-006 phrase the executor as an existing
reader ("read the deterministic scalars") in the requirement body without the SPEC-ONLY/unbuilt
qualifier that appears elsewhere. A reader of FR-006 alone would believe the read path exists.

**Severity rationale:** MEDIUM — the gap IS surfaced (synth-02 G2, synth-04 SPEC-ONLY tag), so this
is a consistency defect, not a buried fabrication. But FR-006's unqualified "MUST consume" wording
contradicts the SPEC-ONLY reality stated two files over.

**Fix:** add the "(spec-only consumer today; wiring is net-new — see §5.3 G2)" qualifier to FR-006
and synth-03 §6.3's sprint-executor mention so all three files agree the executor read path is
unbuilt.

---

### Issue 4 — MEDIUM — synth-05 §11.1 step-8 exit-code mapping is asserted but not grounded to a cited source in the synth set

**File:** synth-05 §11.1 step 8 and the sequence-diagram final arrow:
`exit code (pass=0 / halted=10 / degraded=11 / blocked=2)`.

**What's wrong:** The verdict→exit-code mapping `pass=0 / halted=10 / degraded=11 / blocked=2` is
stated as fact in synth-05 (§11.1 step 8, and the cross-reference note "owned by §6 Architecture /
`models.Verdict.exit_code`"). None of the five assigned synth files actually *contains* a
[CODE-VERIFIED] citation for these specific integer values, and §6 (synth-03) does **not** define
the exit-code mapping despite synth-05 pointing there as its owner. The cross-reference is dangling:
synth-05 defers to §6 for the mapping, but synth-03 §6 never states it.

I could not trace `degraded=11` to any of the assigned synth files or to the research excerpts read
(research/02 covers `derive_verdict` ordering blocked→degraded→… but the read excerpt did not pin
the integer 11; the user's own memory note records exit-11 as "degraded" which is consistent, but a
memory note is not a research-file citation). This is an **unverified claim** within the synth set:
the value is plausibly correct but is not sourced inside the documents under review, and its stated
owner section does not carry it.

**Severity rationale:** MEDIUM — likely-correct but uncited within the partition, and the
cross-reference to §6 is broken (points at a section that does not define the mapping). Per the
zero-fabrication standard, an exit-code contract asserted without an in-document [CODE-VERIFIED]
trace must be flagged.

**Fix:** either (a) add a [CODE-VERIFIED] citation to `models.Verdict.exit_code` (the actual source
file/line) where the mapping first appears, or (b) have §6 (synth-03) actually define the mapping
so synth-05's cross-reference resolves. Mark `[UNVERIFIED within partition A]` until grounded.

---

### Issue 5 — MEDIUM — synth-03 §6.2 cites `commands.py:254` for `reflect_group.run()` but the diagram label says `reflect_group.run() — commands.py:254` while research pins the call as `ReflectRunner(config).run()` at commands.py:254

**File:** synth-03 §6.2 mermaid node `CMD["reflect_group.run() — commands.py:254"]`.

**What's wrong:** research/02 line 63 pins commands.py:254 to `result = ReflectRunner(config).run()`
— i.e. line 254 is the *runner invocation*, not the definition of a `reflect_group.run()` command
callback. The synth label conflates the Click command function name (`reflect_group.run`) with the
line that actually holds `ReflectRunner(config).run()`. The line number is right; the symbol named
at that line is mislabeled. A reader following the citation to commands.py:254 will find a
`ReflectRunner(...).run()` call, not a `reflect_group.run()` definition.

**Severity rationale:** MEDIUM — citation line is correct but the symbol attribution at that line
is inaccurate (S3/S1-class citation drift). Not load-bearing for the design, but it is exactly the
kind of file:line/symbol mismatch the accuracy review exists to catch.

**Fix:** relabel the node to `ReflectRunner(config).run() — commands.py:254` (matching research/02
line 63), or cite the actual line of the `reflect_group.run` command definition if that is the
intended referent.

---

### Issue 6 — LOW — Stale-doc discrepancies are surfaced inline but criterion 9 (§22 Open Questions placement) cannot be confirmed within partition A's scope

**Files:** synth-04 §8.3, synth-02 §5.3 G3 (both surface the
`ensemble.REFLECT_CONTRACT_VERSION = "1.0"` vs SKILL `1.6.0` discrepancy).

**What's wrong:** Criterion 9 requires stale-doc discrepancies to be surfaced in §22 (Open
Questions). The two known stale discrepancies (contract_version 1.0/1.6.0; OQ-DRS.3) ARE surfaced —
but inline in §8.3 and in the §5.3 gap table, not in a §22 section. §22 is not part of any assigned
file (s01–s05 cover §1–§11), so I cannot confirm the discrepancies are also carried into §22 where
the criterion wants them. This is a partition-scope limitation, not a confirmed defect.

**Severity rationale:** LOW — the discrepancies are surfaced *somewhere* (satisfying the spirit of
criterion 9); only their §22 placement is unverifiable from partition A.

**Fix / handoff:** the orchestrator merging partition reports should confirm §22 (owned by a later
synth file outside A) carries the contract-version staleness as an Open Question. [PARTITION NOTE:
§22 is outside partition A's assigned files; criterion 9 §22-placement check deferred to the
partition that owns §22.]

---

## 5-Claim Fabrication Trace (criterion 3 sample)

| # | Claim (synth file) | Traced to | Verdict |
|---|--------------------|-----------|---------|
| 1 | Six canonical scalar names (s04 §8.2) | research/03 lines 27-32 (verbatim) | VERIFIED |
| 2 | `_audit_once` at runner.py:394-453, `parse_contract` at runner.py:445 (s03 §6.2, s04 §7.5) | research/02 lines 135, 152, 380 | VERIFIED |
| 3 | `_bfs_reachable` adapt depth=1 + DEGRADE-on-partial (s03 §6.1 stage ROOTWALK, §6.4 D1) | research/05 §5 lines 157-189 | VERIFIED |
| 4 | Ledger written 1 of 9 quiet-path runs (s01 §2.2, §4.1) | research/00 §3 lines 53-55 | VERIFIED |
| 5 | `_LOAD_BEARING_BOOL_FIELDS` fail-closed block at contract.py:200-209 (s04 §7.4) | research/02 lines 214-215, 226 | VERIFIED |

No fabrication detected in the sampled claims — every traced claim resolves to a research-file
citation. The defects in Issues 1–5 are accuracy/consistency/over-attribution errors, not invented
facts (with the exception of Issue 4's exit-code values, which are *unsourced within the partition*
rather than contradicted).

---

## PARTITION NOTE

Cross-file checks (contradictions, cross-references, coverage audit) were applied within partition
A's assigned subset (synth-01..synth-05, covering TDD §1–§11). Checks that reach sections outside
this subset — specifically criterion 9's §22 Open Questions placement (Issue 6) and FR-006's
sprint-executor wiring against §15 Testing Strategy / later sections — are limited to the assigned
files. Full cross-file analysis requires merging this report with the partition(s) covering §12–§28.

---

## Recommendations

1. **Fix Issue 1 first (HIGH, 3 files):** expand all eval-case tables from 4 rows to 5, separating
   case 37 (unwired) from case 41 (test-only-ref), and label 41 as the count-invariant host.
2. **Fix Issue 2 (HIGH):** soften synth-01 §2.2's forbid-attribution to match research/03 §1.1's
   actual explicitly-forbidden token set.
3. **Reconcile Issue 3 (MEDIUM):** add the SPEC-ONLY/unbuilt qualifier to FR-006 and synth-03 §6.3.
4. **Ground Issue 4 (MEDIUM):** add a [CODE-VERIFIED] source for the exit-code mapping or have §6
   define it so synth-05's cross-reference resolves.
5. **Fix Issue 5 (MEDIUM):** relabel the commands.py:254 node to the symbol research/02 pins there.
6. **Hand off Issue 6 (LOW):** confirm §22 carries the contract-version staleness during merge.

**Gate verdict: FAIL** — 2 HIGH + 3 MEDIUM unresolved accuracy/consistency findings. Re-run gate A
after fixes 1–5 land.

**Status:** Complete
