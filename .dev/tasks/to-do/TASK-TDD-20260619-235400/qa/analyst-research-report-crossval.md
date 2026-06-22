# Cross-Validation Report — Research Gate (OI-1 joint satisfiability + reuse-audit re-confirmation)

- **Analyst:** rf-analyst (cross-validation, adversarial stance)
- **Mode:** report-only (`fix_authorization: false`)
- **Date:** 2026-06-20
- **Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`
- **Files read (full):** `01-reflect-runner-seam.md`, `02-reflect-contract-verdict.md`, `05-swarm-reduce-merge-contract.md`, `06-swarm-lens-registry.md`, `07-nfr7-guard-test-harness.md`, `08-precedents-adversarial-handoff.md`, `reuse-audit.yaml`
- **Scope note:** This is a CONSISTENCY cross-validation of research files against each other (not a re-trace of source code). Where the report says a claim is "code-grounded," that means the research file carries a `[CODE-VERIFIED]` tag with file:line evidence; I verified the evidence is present and internally consistent, not that I independently re-read every cited source line.

---

## Verdict: **PASS (with 2 surfaced contradictions, both non-blocking)**

Both cross-cutting concerns are satisfied:

- **Concern (1) — OI-1 joint satisfiability:** PASS. Every reflect-consumed verdict field (`tier_reached`, `merge_method`, `reviewer_count`, `t2_model_class_diversity`, `degraded_components`) has either an identified swarm-emitted source OR a clearly-flagged gap requiring `ensemble.py` synthesis. The reflect half (02) and swarm half (05) do not contradict each other on the substance of the field correspondence.
- **Concern (2) — reuse-audit re-confirmation:** PASS. All four verdicts are re-confirmed in the relevant research file with grounded file:line evidence.

The two contradictions surfaced (C1, C2) are a stale cross-reference and a known design-vs-current-state gap. Neither breaks OI-1 satisfiability; both are documented inside the research set itself. Details below.

---

## Concern (1): OI-1 Field-Correspondence — Joint Satisfiability of 02 (reflect side) + 05 (swarm side)

### Method

OI-1 requires that for each verdict field `derive_verdict` reads, the swarm side either (a) emits a directly-mapped source, or (b) the gap is explicitly flagged as needing `ensemble.py` synthesis. I cross-checked the five named fields against:
- file 02 §3/§5 (reflect-side consumption: which trigger reads each field, exit-code routing),
- file 05 §3 (swarm DM-012 `ResultContract` field table) and §7 (the explicit swarm→reflect mapping table).

### Field-by-field join table

| Reflect-consumed field | Reflect side (02) — consumer + behavior | Swarm side (05) — source or gap | Joint status |
|---|---|---|---|
| `tier_reached` | 02 §3 Trigger 6 (`degraded-tier1`, L263-264) + §5 PASS gate (L235, must `== expected_tier`); coerced to `None` if non-int (02 §6, contract.py L116-117) | 05 §3: **ABSENT** on DM-012. 05 §7: explicitly flagged "Must be SYNTHESIZED by an `ensemble.py`-style layer from swarm execution facts (reviewers run / merge mode)" | **(b) gap flagged** ✓ |
| `merge_method` | 02 §3 Trigger 10 (`== "single-reviewer-fallback"` → `single-reviewer-fallback`, L280-281) | 05 §3: **ABSENT**. 05 §7: flagged "Must be DERIVED from swarm `amalgamation_mode` + M (`merged_path is None` ⇔ no merge)" | **(b) gap flagged** ✓ |
| `reviewer_count` | (task-brief field; 02 does not name it as a discrete consumer — see Observation O1 below) | 05 §7: "Absent as a named key; swarm equivalent = `workers_succeeded` (M) or `len(output_files)` … rename + re-derive" | **(a) source identified** (`workers_succeeded`) ✓ |
| `t2_model_class_diversity` | 02 §3 Trigger 7 (set AND `!= "full"` → `degraded-model-diversity`, L267-269; T1-null guard) | 05 §3: **ABSENT**. 05 §7: flagged "Must be COMPUTED by `ensemble.py` from the distinct model classes in `output_files`" (distinct `model_id`/`model_label`) | **(b) gap flagged + raw source named** ✓ |
| `degraded_components` | 02 §2 (list-shape BLOCKED guard, L184-193) + §3 Trigger 1-5 (membership in `_DEGRADED_COMPONENTS_HALT_SET`, L259-260) | 05 §3/§7: not a DM-012 field; not in 05's §7 mapping table | **see Observation O2 below** — not contradicted, but coverage is thinner than the other four |

### Do the two halves contradict each other? NO.

The two files agree on the load-bearing structural claim and reinforce it from both sides:

1. **Two disjoint schemas, one filename.** 02 §6/Gaps treats the producer side as out-of-scope `[UNVERIFIED]` and says the swarm→reflect emission "must be cross-checked." 05 §6 Contract B independently establishes the same fact from the swarm side: the swarm DM-012 `return-contract.yaml` and the reflect `return-contract.yaml` are **two disjoint schemas sharing only the key name `status`** (with different semantics — IMM-5 worker verdict vs reflect tier-success). These are complementary, not contradictory.

2. **`status` semantic divergence is flagged identically on both sides.** 02 §4/§5 reads `status == "success"`/`"failed"`/`"partial"` for the reflect tier-success/halt logic. 05 §3 + §7 note swarm `status` is the IMM-5 `success`/`partial`/`failed` worker verdict and explicitly mark it "**Re-mapping required; not a passthrough.**" Agreement.

3. **`ensemble.py` is the synthesis layer — both files name it, both flag it absent.** 02 Gaps defers the producer join to the skill/ensemble layer; 05 Gaps #1 states `[CODE-CONTRADICTED] — no ensemble.py exists` (`find src -name "*ensemble*"` → nothing). 01 §(c) and 08 §4 corroborate. No file claims `ensemble.py` exists; every file that mentions it flags it as to-be-built. Consistent.

**Conclusion (1):** OI-1 is JOINTLY SATISFIABLE from these two halves. Of the five fields, three (`tier_reached`, `merge_method`, `t2_model_class_diversity`) are correctly flagged as `ensemble.py`-synthesis gaps with their raw swarm source facts named; one (`reviewer_count`) has a direct swarm source (`workers_succeeded`); one (`degraded_components`) is structurally consumed reflect-side but under-addressed swarm-side (Observation O2 — a coverage thinness, not a contradiction). The two halves are mutually reinforcing on the central "disjoint-schema → mapping-layer-required" finding.

### Observations within Concern (1)

- **O1 — `reviewer_count` is not a first-class field in file 02.** File 02's tables (which exhaustively enumerate every field `derive_verdict` reads) do NOT list a `reviewer_count` contract field. 05 §7 correctly notes it is "Absent as a named key" and maps it to `workers_succeeded`. So the brief's `reviewer_count` is a *conceptual* verdict input realized reflect-side via `tier_reached`/`merge_method`/diversity rather than a literally-read contract key. This is consistent across files (07 §5 also treats `reviewer_count` as an inferred witness name, not a confirmed contract field), but a reader of OI-1 should not expect a `reviewer_count:` key in either `return-contract.yaml`. **Not a contradiction; a naming-precision note for the TDD.**

- **O2 — `degraded_components` swarm-side provenance is the thinnest link.** Reflect consumes `degraded_components` heavily (it is the only field gating BOTH a BLOCKED list-shape guard AND DEGRADED triggers 1-5). But 05's §7 swarm→reflect mapping table does NOT include a row for `degraded_components`, and 05 §3 (DM-012 table) shows no DM-012 field that maps to it. This is logically consistent with the "disjoint schema" thesis (it's simply another field `ensemble.py` must synthesize), but unlike `tier_reached`/`merge_method`/`t2_model_class_diversity`, file 05 never explicitly says "`degraded_components` must be synthesized from X." 01 §"caveats" #3 partially fills this (the ensemble must "populate those honestly from whichever pool it actually used," referring to diversity/vendor degraded triggers). **Recommendation for synth-04:** add an explicit `degraded_components` row to the OI-1 correspondence table naming its synthesis source (swarm capability-loss telemetry / transport-degrade signals), so all five reflect-consumed fields have symmetric treatment.

---

## Concern (2): Reuse-Audit Verdict Re-Confirmation

For each of the four `reuse-audit.yaml` findings, I checked whether the relevant research file re-confirms the recorded verdict with grounded file:line evidence.

| # | Candidate | reuse-audit verdict | Re-confirmed in | Grounded evidence present? | Status |
|---|---|---|---|---|---|
| 1 | `src/superclaude/cli/reflect/ensemble.py` | **reuse-by-import** | 01 §"Reuse-audit re-confirmation" (L220-251) | YES — names the 3 swarm symbols with exact file:line: `dispatch_wave1` `dispatch.py:L334`, `_resolve_run_transport_factory` `commands.py:L612`, `reduce_wave3` `reduce.py:L555`; all confirmed sync (`grep ^async def\|await` → no matches); isolation rules (runner.py L8-12) satisfied | **RE-CONFIRMED** ✓ |
| 2 | `src/superclaude/cli/swarm/lenses/reflect_review.py` | **mirror-shape** | 06 §2 + §6a + Key Takeaway 6 | YES — `bare_review.py` `LENS` literal L40-75 cited field-by-field as the mirror source; `suspect=True` L63, `tier="T2"` L64, next-cmd L65-68; validator assertion 3 (`_validate.py` L128) names `{suspect_files}` requirement | **RE-CONFIRMED** ✓ |
| 3 | `src/superclaude/cli/swarm/lenses/templates/reflect-review-output.md` | **mirror-shape** | 06 §5a + §6b + Key Takeaway 6 | YES — `feasibility-probe-output.md` frontmatter block cited at L46-62, pinning convention at L98-100; blend-in of `bare-review-output.md` `## Suspect files` section (L13-16) justified by `suspect=True` | **RE-CONFIRMED** ✓ |
| 4 | `tests/cli/reflect/test_ensemble_stub_integration.py` | **mirror-shape** | 07 §5 "Reuse-audit re-confirmation" (L156-158) | YES — swarm precedent `tests/swarm/test_commands_run.py` cited at L507-568 (`results==workers`, behavioral-artifact witnesses) + `test_inv005_pool_guard.py` two-tier structure; explicitly argues NOT reuse-by-import (file doesn't exist, different package/transport) and NOT extract-shared (over-coupling) | **RE-CONFIRMED** ✓ |

### Cross-check: do the research files' verdict justifications match the reuse-audit's own evidence?

The `reuse-audit.yaml` neighbour refs are consistent with the research files:
- Finding 1's neighbours (`dispatch.py:344`, `commands.py:619`, `reduce.py:578`) point at the same swarm symbols 01 re-confirms (minor line offsets: audit's `dispatch.py:344` snippet "Fan prompt across N workers" vs 01's `dispatch_wave1` def at L334 — these are the docstring-line vs def-line of the same function; **not a contradiction**, see C3 below).
- Finding 2's neighbours are all `bare_review.py` lines (L40, L63, L64, L66) — exactly the literal 06 mirrors.
- Finding 3's neighbours are `feasibility-probe-output.md` lines (L44, L52, L98) — exactly the template 06 mirrors.
- Finding 4's neighbours are `test_commands_run.py` lines (L516, L548, L551) — within the L507-568 block 07 cites.

**Conclusion (2):** all four verdicts RE-CONFIRMED with grounded, mutually-consistent file:line evidence.

---

## Contradictions Surfaced (adversarial pass)

### C1 — [STALE CROSS-REFERENCE, non-blocking] File 05 calls file 02 a "stub header only"; file 02 is now Complete.

- **05 §7 (L222)** states verbatim: *"`02-reflect-contract-verdict.md` exists but is a **stub header only** (`Status: In Progress`, no field table body yet as of this turn)."* 05 §7 then says the reflect-side join "completes in synthesis (synth-04)" and that 05 read `reflect/contract.py` directly "rather than relying on the absent file." 05 Gaps #3 repeats this (`[UNVERIFIED] — reflect-side field table … is a stub header only`).
- **File 02 is dated 2026-06-20, Status: Complete**, and contains the full reflect-side field-correspondence tables (§2-§5) that 05 said were absent.
- **Assessment:** This is a **temporal artifact**, not a substantive disagreement. 05 is dated 2026-06-19; 02 was completed 2026-06-20 (the next day). 05 was written when 02 was genuinely still a stub. The two files do NOT disagree on any field's semantics — 05 sourced the reflect fields directly from `contract.py` and arrived at the SAME field set 02 documents (compare 05 §6 Contract B's reflect key list — `status, tier_reached, t2_model_class_diversity, merge_method, adversarial_convergence_score, deviation_count_by_class, report_path, remediation_task_path` — against 02's tables: identical coverage). **Impact: low.** **Action for synth-04:** when assembling, do not carry forward 05's "02 is a stub" language; 02 is complete and authoritative for the reflect side. The OI-1 table should be assembled from 02 (reflect) + 05 (swarm), and 05 §7's interim mapping table is now superseded/confirmable by 02.

### C2 — [DESIGN-vs-CURRENT-STATE, intentional, non-blocking] The swarm↔reflect wiring described in §6 does not exist in current code.

- **05 Gaps #1 and #2** carry `[CODE-CONTRADICTED]` tags: (#1) "no `ensemble.py` exists" (`find` → nothing); (#2) "reflect does NOT currently consume swarm artifacts" (`grep -rn "t2-swarm\|final_path\|output_files" src/superclaude/cli/reflect/` → zero hits). 05 explicitly labels the §6 path-confinement contracts as *"design assertions to be built, not existing enforcement."*
- **01, 07, 08 all corroborate** the same fact (ensemble.py absent; `test_ensemble_stub_integration.py` absent; reflect package has no swarm/adversarial/final_path refs).
- **Assessment:** This is **not a contradiction between research files** — every file agrees. It is correctly tagged `[CODE-CONTRADICTED]` *against the task brief's framing* (the brief speaks of these as if they exist). For a TDD/hardening task this is expected and correct: the files are honestly distinguishing "design target" from "current code." **Impact: low (and properly disclosed).** No action needed beyond ensuring the TDD frames OI-1/FR-RH2.3 as to-be-built. **This is a model of correct staleness-tagging discipline — flagged here as a positive, not a defect.**

### C3 — [LINE-OFFSET, cosmetic] reuse-audit.yaml neighbour line numbers are docstring-lines; research files cite def-lines.

- `reuse-audit.yaml` finding 1 cites `reduce.py:578` ("Compute status, trigger merge, emit the final ResultContract") and `dispatch.py:344`. Files 01/05 cite `reduce_wave3` **def at L555** and `dispatch_wave1` **def at L334**. 05 §1 reconciles this explicitly: `reduce_wave3` "def at **L555**, docstring … at **L578**." So the audit pinned the *docstring* line, the research the *def* line — same symbol.
- **Assessment:** cosmetic; same symbols, same functions. **Impact: negligible.** Mentioned only for completeness of an adversarial sweep.

---

## Cross-File Consistency Spot-Checks (no contradiction found)

These were checked and came back CLEAN (recording them so the gate has evidence the checks ran):

1. **`final_path` (not `merged.md`) consumption rule** — asserted identically in 05 §4/§6 Contract A, 06 §5, and 08 §1.2/§4.3 (`commands.py` L2066-2081 precedent). All three agree reflect/Mode-A consumes per-reviewer `final_path`, never the mechanical `merged.md`. Consistent.
2. **`mechanical_merge` scoring-free boundary** — 05 §2 (merge.py 8 LOC, AC-011/AC-012 disallow list) and 08 §4.3 (FR-RH2.3 AC: "no scoring/ranking/dedup added to merge.py") agree. Consistent.
3. **Diversity-source reconciliation tension** — 01 caveat #3 ( reflect's `ANTHROPIC_DEFAULT_*` 3-Claude-alias pool vs swarm's `T2Model0N` proxy pool) is a genuine open design question, raised consistently in 01 and not contradicted elsewhere. 06 §2 confirms no lens holds a model ID (models come from `job.workers.models`/T2 pool). Consistent framing.
4. **`--suspect-source` undocumented in adversarial protocol** — 08 §4.2/Gaps `[CODE-CONTRADICTED]` (emitted by swarm/bare-review, unparsed by `sc-adversarial-protocol/SKILL.md`). This is a real seam gap but is internal to 08's scope and does not contradict 02/05/06/07. Surfaced here for TDD awareness (it affects FR-RH2.3 handoff but not OI-1 field correspondence).
5. **NFR-7 isolation rules** — 01 §"Isolation guardrails" (runner.py L8-12: no async, no sprint/roadmap import, ClaudeProcess-only) and 07 Part 1-2 (the two-layer guard + `ensemble.py` extension) agree on the same invariant and the same `commands.py --tmux subprocess.run` carve-out. Consistent.

---

## Recommendations (for synth-04 / TDD author; report-only, no fixes applied)

1. **Resolve C1 at assembly time:** treat file 02 as the authoritative reflect-side OI-1 half; discard 05 §7's "02 is a stub" framing and its interim self-sourced mapping table where 02 now supersedes it. Re-verify 05 §7's mapping rows against 02's tables when building the canonical OI-1 correspondence table.
2. **Close O2:** add an explicit `degraded_components` synthesis row to the OI-1 correspondence table so all five reflect-consumed verdict fields have a named swarm source/synthesis path (currently the thinnest-covered field).
3. **Carry O1 forward as a naming note:** OI-1 has no literal `reviewer_count:` contract key; it is realized via `workers_succeeded` (swarm) → `tier_reached`/`merge_method`/diversity (reflect). State this so the TDD doesn't spec a phantom key.
4. **Keep C2/C3 as-is:** C2 is correct design-vs-current tagging; C3 is cosmetic. No remediation needed.
5. **Flag the `--suspect-source` seam (08)** in the TDD's OI-4/FR-RH2.3 section even though it is outside OI-1 — it is the one genuine `[CODE-CONTRADICTED]` cross-skill gap that will bite at implementation.

---

## Summary

**PASS.** OI-1 is jointly satisfiable from file 02 (reflect consumer half) + file 05 (swarm emitter half): every reflect-consumed verdict field is either directly sourced from a swarm DM-012 field (`reviewer_count` ← `workers_succeeded`) or explicitly flagged as requiring `ensemble.py` synthesis with its raw swarm source named (`tier_reached`, `merge_method`, `t2_model_class_diversity`); `degraded_components` is consumed reflect-side and is the one field whose swarm-side synthesis path is under-specified (O2 — coverage thinness, not contradiction). The two halves do not contradict; they mutually reinforce the load-bearing "two disjoint `return-contract.yaml` schemas → mapping layer required" finding. All four reuse-audit verdicts (ensemble.py=reuse-by-import; reflect_review lens / reflect-review template / stub test=mirror-shape) are re-confirmed in 01/06/07 with grounded, mutually-consistent file:line evidence. Two contradictions surfaced — C1 (file 05 calls file 02 a stub; 02 is now Complete — a 1-day temporal artifact, low impact, resolve at assembly) and C2 (the swarm↔reflect wiring is design-target-not-current-code — correctly `[CODE-CONTRADICTED]`-tagged by every file, expected for a TDD task) — plus C3 (cosmetic line-offset). None block the OI-1 gate.
