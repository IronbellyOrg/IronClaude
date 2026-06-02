# Variant 2 — sonnet:analyzer — Phase 9 Unchecked-Item Review

**Stance:** Evidence-quality, logical consistency, redundancy, traceability to spec/master-report. Where does the item's claim diverge from what the code/spec actually says?

**Ground-truth checkbox state:** Verified via the task file: 9.7/9.8/9.9 = `[x]` (DONE, findings logged), 9.10 = `[x]` (N/A user-approved). Unchecked = **9.11, 9.12, PG9.1, PG9.2**. I analyze these.

---

## Step 9.11 — secondary migrations

**Evidence on the established pattern (coherence with 9.2–9.9):** Every completed sub-step (extract→spec_fidelity) followed an identical, QA-accepted recipe: `tool_schemas/<name>.schema.json` + `templates/<name>.md.j2` + `RoadmapConfig.tool_write_<name>=False` + `--tool-write-<name>` Click flag + `build_<name>_prompt(..., tool_write=False)` param + `<name>_tool_definition()` + `tests/roadmap/test_tool_write_step_<name>.py` parity test + registry entry routing to PLAIN `render_step_tool_write` (or `render_step_tool_write_with_id_check` for generate/merge). 9.11 says "repeat the pattern" — structurally sound and consistent. The mechanism exists and is proven (8 steps green, 256/256 regression at 9.9). **Necessity: confirmed; pattern is reusable.**

**Logical inconsistency #1 — remediate dual-classification.** The item asserts `build_remediation_prompt` "is a true LLM-output step." Evidence (remediate_prompts.py L17–81): it is — it *is* an LLM-output step — but its output is **file mutations**, not a structured artifact with requirement IDs. The §3 phantom-ID `roadmap_ids` subset constraint (which master:§Top-3 #3, L437/L490, attributes to roadmap *generators* fabricating FR/NFR/SC/D IDs) has **nothing to constrain** in a file-edit prompt. So "rewrite build_remediation_prompt because it is an LLM step" is TRUE for parity-migration purposes but the item silently inherits the §3 expectation that remediate must enforce roadmap_ids. That expectation is misapplied. Two distinct truths got merged. **This is the highest-severity analytic finding.**

**Logical inconsistency #2 — count drift.** The item header says "test_strategy + certify + validate-reflect (secondary migrations)" = 3 steps, but the body adds `build_remediation_prompt` as a 4th. The H4 preamble enumerates 4 sub-actions (a test_strategy, b certify, c validate-reflect, d consolidated parity test) — but H4's (d) is "consolidated parity test," NOT remediate. So there are now **two different "4-item" decompositions** that don't agree: {test_strategy, certify, validate-reflect, remediate} (body) vs {test_strategy, certify, validate-reflect, parity-test} (H4 preamble). The H5 yaml lists `remediation` as a 13th counter entry, siding with the body. This is a genuine spec-internal contradiction. REFACTOR must reconcile to a single enumeration: 9.11.a test_strategy, 9.11.b certify, 9.11.c validate-reflect, 9.11.d remediate (parity-only, roadmap_ids N/A), 9.11.e consolidated parity test.

**Redundancy check:** No overlap with 9.2–9.10 — these are 4 distinct prompt builders not yet migrated (verified all 4 functions exist: test_strategy prompts.py:2015, certification certify_prompts.py:21, reflect validate_prompts.py:16, remediation remediate_prompts.py:17). Not superseded. Not redundant.

**Verdict: REFACTOR** — necessary; reconcile the two conflicting 4-item enumerations and strip the misapplied §3 roadmap_ids expectation from the file-edit remediate (label it parity-only).

---

## Step 9.12 — cutover criterion

**Evidence on redundancy with H5:** The H5 preamble + the existing `r1-4-cutover-counters.yaml` already implement the counter SoT 9.12's body describes in prose. The body's inline "release_cycle_count (starts at 0, increments per dual-write release)" duplicates the yaml's `release_marker_count: 0` / `cutover_at_count: 3` / `cutover_eligible`. Two representations of the same state = drift risk. **REFACTOR: 9.12 should READ the yaml, not re-describe it.**

**Logical consistency of the IF/ELSE:** The item's "IF release_cycle_count >= 3 AND parity passing → ready for cutover; ELSE remain dual-write" is correct and matches Vector A. The "overall readiness verdict requires ALL steps ready OR documented exception" is sound. At authoring time (0 cycles), the only consistent output is "all dual-write, none eligible, R1.4 not ready for cutover" — the item correctly anticipates this. Logic = fine; sourcing = wrong (prose not yaml).

**Fragility — temporal mismatch.** "≥3 release cycles" is wall-clock/release-cadence time. This task will be marked complete and archived to `done/` in days; 3 release cycles take weeks-months. An item whose completion criterion depends on future releases **cannot truly complete** within the task. The item half-acknowledges this ("updated by the worker agent as live releases accumulate") but then says "mark this item complete." That's the contradiction: you cannot both "track live releases until 3 pass" and "mark complete now." REFACTOR: 9.12 completes by producing the *initial-state* decision doc + an explicit deferral of the cutover trigger to R1.6/release-hook. The yaml persists across the task boundary; the checklist item does not.

**Verdict: REFACTOR** — fold the inline counter into the H5 yaml-as-SoT; scope completion to the initial decision + deferral; treat wiring_verification entry as exempt.

---

## Step PG9.1 — aggregate + rf-qa-qualitative

**Evidence-quality of the checks:** Strong. (b) "parity tests actually compare rendered tool output to markdown output (not just exit codes)" is the right adversarial probe — verified that the completed parity tests do assert byte-identity / rendered-output equivalence (e.g. `test_build_spec_fidelity_prompt_default_byte_identical`, `test_rendered_*_satisfies_gate`), so the gate's probe is answerable with real evidence. (g) "zero new return True stubs" directly targets the master-report stub anti-pattern. (h) markdown-stays-default is the Vector A safety property.

**Inconsistency — the "12" again.** Check (a)'s "12 sub-steps all have schema+template+dual-write+parity" is arithmetically wrong against the as-built reality: 8 primary done (extract, extract_tdd, generate, diff, debate, score, merge, spec_fidelity) + wiring EXEMPT + 4 secondary (9.11) = 12 *nominal* but only **11 carry schema+template+parity** (wiring has none by design). A literal-minded rf-qa reading check (a) will flag wiring as a missing artifact = false FAIL, exactly the failure mode the 9.10 finding pre-empted by writing the exemption to the validation glob. The check text must encode the exemption. REFACTOR check (a).

**Redundancy with interim QA (H3):** PG9.1 partially overlaps the interim QA after 9.5 and 9.10. But that's by design (cumulative terminal gate vs incremental checkpoints) and the spec's halt-precedence cadence wants both. Not wasteful. KEEP the gate; fix only check (a).

**Verdict: REFACTOR (light)** — fix check (a) "12 all" → "11 genuine migrations + wiring exempt + remediate-surface clarification."

---

## Step PG9.2 — act on verdict

**Logical structure:** The conditional (PASS → proceed-decision + Phase 10; FAIL → fix/re-spawn ≤3 → HALT+escalate) is the proven L5 pattern, identical to PG8.2/PG7 etc. No internal inconsistency. Evidence: every prior PG used this shape and passed QA.

**Traceability:** "record: 12 steps dual-write, cutover deferred" — the "12" here is loosely worded (really 11 dual-write + 1 wiring-exempt + remediate-parity) but in a *proceed-decision record* it's a summary count, lower-stakes than in a gate predicate. Acceptable; could note "11 dual-write + wiring exempt" for precision.

**Verdict: KEEP** — standard act-on-verdict; optional precision tweak to the recorded count.

---

## Analyzer's phase-coherence summary

All four items trace to real spec requirements and to a proven, QA-accepted mechanism — none are superseded by 9.1–9.10. The systematic defect across the phase is a **representation/count inconsistency**: the number "12" and the identity of "remediate" are used inconsistently across the item bodies, the H4/H5 preambles, and the as-built code. Specifically:
- **Highest impact:** the file-editing `build_remediation_prompt` is wrongly slotted as a §3 phantom-ID (`roadmap_ids`) target; that constraint belongs on the roadmap-producing remediate surface or nowhere.
- The "12 sub-steps all have schema+template+parity" predicate (9.11 implicit, PG9.1 check (a)) is false for wiring-by-design and will produce false FAILs.
- 9.12 duplicates the H5 yaml in prose and is mis-scoped as completable despite a multi-release dependency.
Recommend REFACTOR on 9.11, 9.12, PG9.1; KEEP PG9.2. No DISCARDs.
