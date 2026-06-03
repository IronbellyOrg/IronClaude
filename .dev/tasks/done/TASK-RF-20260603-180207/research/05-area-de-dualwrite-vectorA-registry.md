# R5 Research — Areas D + E (Dual-Write / Vector A Cutover / Registry Removal)

**Status:** Complete
**Date:** 2026-06-03
**Researcher:** R5 (safety-critical: cutover precondition + doc cross-validator)
**Topic:** (D) R1.4 markdown-path deletion after 3 consecutive parity-passing release cycles per Vector A; (E) spec_id_registry.json dual-write removal + remediate_parser.py + MD-family roadmap_ids reconciliation.

---

## Evidence Log (incremental)

### Finding 0: The tool_write_* flags inventory — [CODE-VERIFIED]

Source: `src/superclaude/cli/roadmap/models.py` L127-155 (PipelineConfig) + L173 (ValidateConfig).

All flags default `False`. Each docstring repeats: "Default False (markdown path is production) until cutover per Vector A >=3 release cycles." There is NO parity-cycle counter anywhere in the dataclass.

There are exactly **12 `tool_write_*` flags** [CODE-VERIFIED: `grep -cE "^\s*tool_write_[a-z_]+:\s*bool" src/superclaude/cli/roadmap/models.py` → 12] — **11 in PipelineConfig** (L127-137) + **1 in ValidateConfig** (`tool_write_validate_reflect`, L155). Do NOT conflate this with the **13 step entries** in `.dev/migrations/r1-4-cutover-counters.yaml`: the yaml has one MORE entry than there are flags because the 13th step, `wiring_verification`, has NO `tool_write_*` flag (it is deterministic-EXEMPT). So: **12 flags ≠ 13 yaml steps** (flags = 12; yaml steps = 13; the difference is the flag-less `wiring_verification` step). The 12 flags (table below shows all 12):

| Flag | Step | Phantom-ID source? | Area |
|------|------|--------------------|------|
| `tool_write_extract` | extract | no | D |
| `tool_write_extract_tdd` | 9.3 TDD extract | no | D |
| `tool_write_generate` | 9.4 generate | YES (PRIMARY) | D |
| `tool_write_diff` | 9.5 diff | no | D |
| `tool_write_debate` | 9.6 debate | no (semantic_layer byte-untouched) | D |
| `tool_write_score` | 9.7 score | no | D |
| `tool_write_merge` | 9.8 merge | YES (SECOND primary) | D |
| `tool_write_spec_fidelity` | 9.9 spec-fidelity | no (convergence path bypasses) | D |
| `tool_write_test_strategy` | 9.11 test-strategy | no | D |
| `tool_write_certify` | 9.11 certify | no | D |
| `tool_write_remediate` | 9.11 remediate | NO ARTIFACT (PARITY-ONLY prompt hint) | E-adjacent |
| `tool_write_validate_reflect` | 9.11 validate reflect | no (ValidateConfig) | D |

Note `tool_write_remediate` is special: its docstring (L154) says it emits NO roadmap-ID-bearing artifact, has NO schema/template/registry entry/executor render hook — it's PARITY-ONLY. The load-bearing guarantee is the default-False prompt stays byte-identical to pre-R1.4. This is the flag tied to remediate_parser.py / Area E.

---

### Finding 1: CUTOVER PRECONDITION — the "3 release cycles" origin and live state — [CODE-VERIFIED, doc-cross-validated]

**The phrase "Vector A >=3 release cycles" appears ONLY in the models.py flag docstrings — NOT in the Vector A architecture doc itself.** [CODE-CONTRADICTED claim of provenance]

- `grep -n -i "cycle|cutover|parity|production"` on `.dev/troubleshoot/roadmap-pipeline-retrospective/wave3-vector-analyses/vector-A-architecture.md` (244 lines) returns NO "3 release cycles", NO "parity-passing", NO "cutover". The doc discusses envelope/post-extractors/fail-open deletion (L148, L172, L189) but never a release-cycle counter.
- The "≥3 consecutive parity-passing release cycles" rule was authored in the **task layer**, not the Vector A doc: `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` L186, L206, L539 (launch instruction **H5** designed the counter mechanism). So the cutover gate is a task-level hardening of Vector A's looser "side-by-side ≥3 releases" cadence — real and binding, just not literally in the Vector A architecture file.

**THE COUNTER STATE — single source of truth:** `.dev/migrations/r1-4-cutover-counters.yaml` (created 2026-06-02, 3211 bytes). [CODE-VERIFIED by reading the file]

Every one of the **13 step entries** (extract, extract_tdd, generate, diff, debate, score, merge, spec_fidelity, wiring_verification, test_strategy, certify, validate_reflect, remediation) has:
```
tool_write_flag_default: false
release_marker_count: 0
last_marker_release: ""
cutover_eligible: false
cutover_at_count: 3
```
**ALL `release_marker_count: 0`. ALL `cutover_eligible: false`.** Zero release cycles have shipped any `--tool-write-<step>` path in production.

**Cutover decision doc** `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-4-cutover-decision.md` §5 verdict (2026-06-02): **"NOT READY FOR CUTOVER — markdown remains the production default."** §4: every step evaluates to "remain dual-write." A premature cutover (count < 3) is HALT-blocked by design.

**rf-qa-qualitative gate** `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/reviews/r1-4-rf-qa-qualitative.md:83` independently confirmed: "NOT READY FOR CUTOVER… No step claims cutover < 3 cycles."

**QA task-validation** `qa/qa-task-validation-report.md:212`: "R1.6 cleanup (Step 11.5) does NOT delete markdown paths — only fragility stubs, fail-opens, and gate=None bypass. `remediate_parser.py` deletion is explicitly DEFERRED in Follow-Up items."

**No release-cycle hook exists** to auto-increment the counter; increment is "manual via PR review" (yaml header comment) and has never run. There is no CHANGELOG entry, no `.dev/releases/` record, and no git commit incrementing any `release_marker_count`.

**VERDICT: NOT-MET.** All 13 counters at 0/3. Markdown path is the production default for every step. No parity-cycle has been recorded.

---

### Finding 2: Dual-write architecture — markdown path vs tool-write path (Area D) — [CODE-VERIFIED]

Source: `envelope.py` L1-50 (module docstring), L146-205 (spec_ids field docs).

**Two orthogonal "dual-write" layers exist — do NOT conflate them:**

1. **Envelope dual-write (R1.2, Area C territory — R4):** every step's markdown is "just a render"; `envelope.json` sidecar carries canonical counts. This is the master:§Flaw 3 inversion. envelope.py L18-23: "R1.3 wires `code_assertions` to read from the envelope; **R1.6 deletes the markdown-as-substrate code paths**." This is substrate-level and governed by R1.3/R1.6, NOT the per-step tool_write_* flags.

2. **Per-step tool-write dual-write (R1.4, Area D):** each LLM step has BOTH a legacy markdown-prompt path (production, flag=False) AND an opt-in structured-JSON-+-Jinja-render path (flag=True). The "markdown path" = `build_<step>_prompt(..., tool_write=False)` → LLM writes markdown directly. The "tool-write path" = `build_<step>_prompt(..., tool_write=True)` → LLM emits schema-validated JSON → `tool_writer` renders markdown via Jinja template. **Area D's "markdown-path deletion" = deleting the `tool_write=False` branch of each prompt builder + the executor's markdown-dispatch branch, leaving only the tool-write path.**

**spec_id_registry.json / envelope.spec_ids absorption (R0.1 → R1.2):** envelope.py L25-31, L146-167. During dual-write BOTH `<release>/spec_id_registry.json` AND `<release>/envelope.json` are written; their `spec_ids` content is byte-identical (`SpecIdRegistry.to_dict()` shape). The `.. todo:: R1.6` at L164-167 marks the duplicate JSON sidecar for deletion "once gate logic reads `envelope.spec_ids` directly (R1.3+ wires the first `code_assertions` consumer)."

---

### Finding 3: spec_id_registry.json WRITERS and READERS (Area E) — [CODE-VERIFIED] — STRANDED-READER RISK

**WRITER (single):** `executor.py:_save_id_registry` L650-665. Builds registry via `build_id_registry()`, writes `output_dir/spec_id_registry.json` (`registry.to_dict()`, indent=2, sort_keys), then L660-664 **registers the path with gates.py via `set_id_registry_sidecar_path(sidecar)`** so MERGE_GATE can resolve it. The comment L658-659 says: "R1.3 widens the signature and removes the hint." (Also a second hint-repoint path at executor.py L3505-3515.)

**LIVE READER (the stranding risk):** `gates.py:_roadmap_ids_within_spec` L997-1055 — the **MERGE_GATE's `roadmap_ids_within_spec` SemanticCheck (Contract #9)**. It reads `_id_registry_sidecar_path.read_text()`, parses JSON, rebuilds `SpecIdRegistry`, and checks `roadmap_ids ⊆ union_of_known()`. **It FAILS CLOSED** (returns a failure string, master:§Flaw 4) if the sidecar is missing/unreadable/malformed (L1011-1031).

**CRITICAL:** the *MERGE_GATE Contract #9* gate reads the **JSON file**, NOT `envelope.spec_ids`. The envelope.py docstring's "R1.3+ migrates it to envelope reads" has NOT happened *for Contract #9* in code. [CODE-VERIFIED: `grep -rn "envelope\.spec_ids" src/superclaude/` shows envelope.py L352 is only the round-trip serializer (`"spec_ids": envelope.spec_ids.to_dict()`), but **`verify_implementation.py` is a SEPARATE, LIVE functional consumer of `envelope.spec_ids`** — `assert_all_frs_resolved` reads `envelope.spec_ids.fr_ids` (`verify_implementation.py:57,95`) and `envelope.spec_ids.accepted_deviation_ids` (`verify_implementation.py:64,120`) as its *only* substrate for the R1.5 fail-closed `verify-implementation` terminal gate. So the earlier claim that "the only `spec_ids` consumer is the round-trip serializer" is FALSE — there is already a production code path that reads typed `envelope.spec_ids` accessors.]

**REPOINT TEMPLATE:** Because `verify_implementation.py:assert_all_frs_resolved` already consumes `envelope.spec_ids.fr_ids` / `envelope.spec_ids.accepted_deviation_ids` directly off the typed envelope (`verify_implementation.py:51-121`), it is the concrete **template** for migrating the MERGE_GATE reader (`gates.py:_roadmap_ids_within_spec`, L997-1055) off the `spec_id_registry.json` file and onto `envelope.spec_ids` — i.e. replace `_id_registry_sidecar_path.read_text()` + JSON re-parse with the same dataclass-accessor pattern (`envelope.spec_ids.<family>_ids`) that verify_implementation already uses. This envelope-read repoint is the **Contract #9 prerequisite for E-registry (spec_id_registry.json) deletion**.

**E-implication:** Deleting `spec_id_registry.json` writes NOW would strand `gates.py:_roadmap_ids_within_spec` → MERGE_GATE fails closed on every run (or the check silently loses its containment guarantee if also deleted). **Area E registry-removal CANNOT proceed until the Contract #9 reader is first re-pointed at `envelope.spec_ids` (the R1.3+ migration the docstring promises but code never did) — using `verify_implementation.py` as the live repoint template.** That re-point is itself a non-trivial code change (widen SemanticCheck signature OR populate the module-level hint from the envelope), not a deletion.

---

### Finding 4: remediate_parser.py (391 lines) — role, consumers, deletion-deferral (Area E) — [CODE-VERIFIED]

Source: `remediate_parser.py` L1-50; consumer grep across `src/`.

- **Role:** two pure functions — `parse_validation_report(text) -> list[Finding]` (primary, merged reports) and `parse_individual_reports(report_texts) -> list[Finding]` (fallback, with dedup). Parses markdown validation reports (`reflect-merged.md`, `merged-validation-report.md` Consolidated-Findings sections) into `Finding` objects with `status="PENDING"`.
- **PRODUCTION CONSUMERS: NONE in `src/`.** `grep parse_validation_report|parse_individual_reports src/` returns ZERO callers outside remediate_parser.py's own definitions. `remediate.py` references it only in **doc comments** (L22, L426) — it does not import or call the functions. `remediate_executor.py:552` (cited in the comment) is a `finding.status` mutation loop, NOT a parser call. The production remediate flow uses the **registry/JSON path** (`remediate.py:deviations_to_findings`, status default "ACTIVE") — a *different* findings source than the markdown-parser path.
- **TEST CONSUMERS:** 3 test files actually CALL the parser functions — `tests/roadmap/test_remediate_parser.py`, `tests/roadmap/test_pipeline_integration.py:319,596`, `tests/roadmap/test_phase7_hardening.py:600,622,629,649`. [CODE-VERIFIED: `grep -rn "parse_validation_report\(|parse_individual_reports\("` returns callers in exactly these 3 files.] A 4th file, `tests/roadmap/test_tool_write_step_remediation.py`, references `remediate_parser.py` ONLY in a module docstring/flag quote (`:38` — "remediate_parser.py is a DELETION CANDIDATE…"); it does NOT import or call either parser function, so it is NOT a functional test consumer.
- **Why "tool-write collapse target":** prior research (research/01 §A.6, per task file L583) reasoned that once remediate goes tool-write (structured JSON Findings), the markdown-parsing path collapses → parser becomes dead. **BUT** remediate is **parity-only** (Finding 0): no schema, no template, no render hook, no roadmap_ids — the tool-write remediate path does NOT actually emit structured Findings JSON. So the collapse trigger never fired.
- **Deferral reason:** task file L583 explicitly flags it "for R1.6 deletion candidate but NOT yet deleted (dual-write must run for ≥3 release cycles first)." `tests/roadmap/test_tool_write_step_remediation.py:40`: "MUST NOT be deleted now; dual-write must run >= 3 release cycles."
- **Is the remediation-step cutover done?** NO — `remediation` counter in the yaml is `release_marker_count: 0, cutover_eligible: false`. Same precondition as all other steps.

**E-implication:** remediate_parser.py is a deferred deletion gated on (a) the same ≥3-cycle precondition (NOT-MET) AND (b) clarification that no production path will ever need the markdown-parser (since remediate is parity-only, the parser may actually be *already-dead production code* — but it has live TEST coverage in 3 files that CALL its functions, so deletion requires also removing/retargeting those tests). Deleting it now is safe ONLY w.r.t. production callers (none) but breaks 3 test files and violates the explicit ≥3-cycle deferral the task authored.

---

### Finding 5: MD-family reconciliation — residual after 8fd0edc9 — [CODE-VERIFIED]

Commit `8fd0edc9` (RyanW, 2026-06-02 18:46) — `git show --name-only`:
- **src/ changes:** `src/superclaude/contracts/__init__.py` (+96 lines), and 4 schemas (`extract/extract_tdd/generate/merge.schema.json`), 4 guard tests.
- **What it fixed:** the 4 tool-write schemas hard-coded their own `roadmap_ids.items.pattern` and OMITTED the MD family (`M{n}-D{nn}`) → `M1-D01` rejected at schema validation in tool-write mode. Established `superclaude.contracts.roadmap_ids_pattern(step)` assembler + `ROADMAP_ENTITY_ID_FAMILIES` (L225) + `TOOL_WRITE_ROADMAP_ID_FAMILIES` (L254) as single SoT; regenerated all 4 schema patterns from it (MD lands in all four; MD ordered before D — contracts L65, L71 `"MD": r"M\d+-D-?\d+"`).

**MD-family is now fully wired across the registry path** [CODE-VERIFIED]:
- `id_registry.py`: `md_ids` field (L67 docstring + dataclass field), included in `union_of_known()`, `to_dict()` serializes `md_ids` (L128), `build_id_registry` populates `md_ids=tuple(families.get("MD", ()))` (L173).
- `envelope.py` L387-388: round-trip back-compat — `md_ids=tuple(spec_ids_d.get("md_ids", ()))` with `.get(..., ())` so OLD envelope dicts lacking md_ids round-trip to empty (matching the same R5 pattern in gates.py:1044 for old sidecars).
- `contracts/__init__.py` L262 `roadmap_ids_pattern` assembler reads `ID_PATTERNS.values()` so MD is always present in tool-write schemas.

**RESIDUAL MD-family work after 8fd0edc9: effectively NONE structural.** The MD-family is consistently represented in: spec extraction → registry → sidecar JSON → envelope round-trip → Contract #9 containment → tool-write schema patterns. The back-compat `.get(..., ())` shims (envelope.py L387, gates.py L1044) are the only "drift-tolerance" residue — they exist to round-trip OLD artifacts that predate md_ids. **When D/E delete the dual-write/registry path, these back-compat shims become candidates for simplification** (no old-sidecar round-trip needed once the JSON sidecar is gone), but that's cleanup-after-cutover, not blocking work. No phantom MD drift remains.

---

### Finding 6: Sequencing D → E and inter-dependencies — [CODE-VERIFIED reasoning]

**Hard ordering constraints from the code:**

1. **D (per-step markdown-path deletion) is gated on the ≥3-cycle precondition PER STEP** (yaml counters). Currently ALL NOT-MET. D cannot delete any markdown path now.
2. **E-registry (delete spec_id_registry.json writes) is gated on re-pointing the Contract #9 reader** (`gates.py:_roadmap_ids_within_spec`) at `envelope.spec_ids` first — the R1.3+ migration that never landed. This is a PREREQUISITE code change, independent of the cycle counter, but ALSO blocked because deleting the writer strands the live MERGE_GATE reader.
3. **E-remediate_parser (delete the parser) is gated on (a) ≥3-cycle remediation precondition (NOT-MET) AND (b) retargeting/removing 3 test files that CALL its functions.** Production has no caller, but the task explicitly deferred it.
4. **The envelope-substrate deletion (R1.6 "deletes the markdown-as-substrate code paths") is a DIFFERENT layer** (R1.3 code_assertions must consume envelope first) — overlaps E-registry's reader-migration prerequisite.

**Verified-green-between requirement:** after any markdown-path deletion (D) or registry-reader re-point (E), the full `tests/roadmap` suite (1957 passed/13 skipped per 8fd0edc9 message) plus the tool-write parity suites (161 passed/1 skipped) plus `make verify-sync` + `make lint-architecture` (Check 11 anti-duplication) must stay green. MERGE_GATE Contract #9 behavioral tests must specifically pass against the NEW reader source.

**Recommended order IF preconditions were met:** E-reader-repoint (gates Contract #9 → envelope.spec_ids) → verify green → E-registry-writer-deletion → verify green → D per-step markdown deletions (only for cutover_eligible steps) → verify green → E-remediate_parser deletion + test cleanup → verify green. But NONE of the entry preconditions are currently satisfied.

---

## Status: Complete

### Summary

- **Finding 0:** exactly **12** `tool_write_*` flags (11 PipelineConfig L127-137 + 1 ValidateConfig L155), all default False — NOT to be conflated with the **13** step entries in `r1-4-cutover-counters.yaml` (the 13th, `wiring_verification`, is flag-less / deterministic-EXEMPT). Of the 12 flags: 10 genuine LLM migrations + remediate (parity-only, no schema/template/render). The yaml's 13 steps = the 12 flagged steps + `wiring_verification`.
- **Finding 1:** The "≥3 release cycles" rule is task-authored (TASK-RF-20260531-042405 H5), NOT in the Vector A doc. SoT counter file `.dev/migrations/r1-4-cutover-counters.yaml` has ALL 13 steps at `release_marker_count: 0`, `cutover_eligible: false`. No release-cycle hook, no CHANGELOG/release record, no increment commit exists.
- **Finding 2:** Two distinct dual-write layers — envelope-substrate (R1.2/R1.3/R1.6) vs per-step tool-write (R1.4). Area D = deleting the `tool_write=False` markdown branch of each prompt builder + executor dispatch.
- **Finding 3:** spec_id_registry.json: single writer (`executor.py:_save_id_registry` L650), one LIVE reader (`gates.py:_roadmap_ids_within_spec` L997, MERGE_GATE Contract #9, fail-closed). The gate reads the JSON FILE, not envelope.spec_ids — the promised R1.3+ envelope-read migration never landed. Deleting the writer now strands the gate.
- **Finding 4:** remediate_parser.py (391 LOC) has ZERO production callers in src/ (only doc-comments in remediate.py + 3 TEST files that CALL its functions). It's effectively already-dead production code, but the task explicitly deferred deletion to ≥3-cycle cutover and 3 test files still exercise it (a 4th, `test_tool_write_step_remediation.py`, only quotes it in a docstring).
- **Finding 5:** MD-family fully reconciled by 8fd0edc9 (contracts SoT assembler + 4 schema regen). No residual structural drift; only back-compat `.get(...,())` shims remain, simplifiable post-cutover.
- **Finding 6:** D blocked on per-step ≥3-cycle counters (all 0). E-registry blocked on reader-repoint prerequisite. E-parser blocked on cycle precondition + test retargeting.

---

## **CUTOVER PRECONDITION VERDICT: NOT-MET**

**Evidence (decisive):** `.dev/migrations/r1-4-cutover-counters.yaml` — every one of 13 step entries has `release_marker_count: 0` and `cutover_eligible: false`; `cutover_at_count: 3`. Corroborated by `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-4-cutover-decision.md` §5 ("NOT READY FOR CUTOVER — markdown remains the production default"), `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/reviews/r1-4-rf-qa-qualitative.md:83`, and `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-4-proceed-decision.md:28` ("Markdown remains production default until ≥3 release cycles per step"). No release-cycle hook, CHANGELOG entry, `.dev/releases/` record, or git commit has ever incremented a counter. The "≥3 release cycles" criterion is binding (task-authored H5 mechanism) and currently 0/3 for all steps.

---

## Per-area recommended task design

### Area D (markdown-path deletion) — **PRECONDITION-CHECK-THEN-HALT**

Because the cutover precondition is NOT-MET, item D MUST be authored as check-then-HALT, NOT delete-now:

1. At execution, READ `.dev/migrations/r1-4-cutover-counters.yaml`.
2. For each step, evaluate `release_marker_count >= cutover_at_count (3) AND cutover_eligible == true`.
3. **If ANY target step is NOT cutover-eligible** (current reality: all 13): write a PENDING marker (e.g. to the task findings + a `.dev/migrations/` note) recording "markdown-path deletion HALTED — step X at N/3 cycles, markdown remains production default per Vector A," and **HALT — do NOT delete any `tool_write=False` branch or executor markdown-dispatch branch.**
4. Only for steps that ARE cutover-eligible may deletion proceed: delete the markdown prompt branch + executor dispatch branch, flip `tool_write_flag_default: true` in the yaml, then run `tests/roadmap` + tool-write parity suite + verify-sync + lint-architecture green.

This directly honors the [Human-decision items must HALT, not auto-default] memory: never auto-apply a default that ships a production-code deletion.

### Area E (registry dual-write removal + remediate_parser.py) — **PRECONDITION-CHECK-THEN-HALT + PREREQUISITE-FIRST**

E has TWO blockers beyond the cycle counter, so author as check-then-HALT with an explicit prerequisite:

1. **E-registry (spec_id_registry.json writes):** at execution, verify the Contract #9 reader has been re-pointed. CHECK: does `gates.py:_roadmap_ids_within_spec` read `envelope.spec_ids` instead of `_id_registry_sidecar_path.read_text()`? **If NO (current reality), HALT** — write a PENDING marker "registry-writer deletion HALTED — MERGE_GATE Contract #9 still reads spec_id_registry.json; envelope-read migration (R1.3+) not implemented; deleting the writer would strand a fail-closed gate." Deleting the writer is gated on FIRST landing the reader-repoint (a separate code change), THEN ≥3-cycle parity.
2. **E-remediate_parser.py:** at execution, READ the `remediation` counter. **If `cutover_eligible: false` (current reality), HALT** — write PENDING "remediate_parser.py deletion DEFERRED per task TASK-RF-20260531-042405 L583 + test_tool_write_step_remediation.py:40, remediation at 0/3 cycles." Note for the author: production callers are already ZERO, but 3 test files (`tests/roadmap/test_remediate_parser.py`, `tests/roadmap/test_pipeline_integration.py`, `tests/roadmap/test_phase7_hardening.py`) CALL its functions; a 4th (`tests/roadmap/test_tool_write_step_remediation.py:38`) only quotes it in a docstring (no import/call). Deletion requires removing/retargeting those 3 calling test files AND the cycle precondition.
3. **MD-family:** no HALT needed — fully reconciled (8fd0edc9). Optional follow-up only: simplify the back-compat `.get(...,())` shims (envelope.py L387, gates.py L1044) AFTER the JSON sidecar is gone.

**Net:** Both D and E are check-then-HALT under current state. No production code may be deleted in this task until (a) the per-step cutover counters reach 3/3 AND (b) for E-registry, the Contract #9 envelope-read migration lands first. The safe deliverable now is the HALT-guarded scaffolding + PENDING markers, not deletions.

---

## Gaps and Questions

Blockers documented inline; no open research gaps — the D/E HALT design is decisive on the NOT-MET cutover precondition. All cutover counters are 0/3 (`.dev/migrations/r1-4-cutover-counters.yaml`), the Contract #9 reader-repoint prerequisite is unimplemented (with `verify_implementation.py` as the live repoint template), and the remediate_parser.py deferral is fully evidenced. No further investigation is required before the task can be authored as check-then-HALT.
