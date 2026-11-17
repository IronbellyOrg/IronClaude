# Merge Execution Log

## Metadata
- Base: Variant 1 (Proposal A, `adversarial/variant-1-original.md`; default model, default persona)
- Executor: merge-executor agent (slot C-04, `reflect-tier2-engine-composition`)
- Plan: `adversarial/refactor-plan.md` (27 planned changes, auto-approved 2026-11-14T17:03:05Z)
- Merged file: `merged-output.md` (374 lines)
- Changes applied: 27 of 27
- Status: success
- Timestamp: 2026-11-14T17:26:37Z

## Changes Applied

Section references below are to `merged-output.md` unless marked "base". Validation lines record what the executor checked: structure (heading level and position), references (every label named in the change resolves in the merged file), contradictions (the change agrees with the rows and sections it touches).

### Change 1: Restate the position as the hybrid (H-C04 / H-C04B)
- **Status**: Applied
- **Source**: Variant 1 advocate Round 2 "Final Position" (H-C04); Variant 2 advocate Round 2 "Final Position" (H-C04B); Variant 2 section 1
- **Target**: Base section 1 (replaced); base section 0 (one line added for `[V]` and `[L]`)
- **Before**: One paragraph: engine B's data inside engine A's shell, "becomes a code step that the orchestrator calls", "no capability listed in section 4 is dropped".
- **After**: Section 1 states the hybrid: engine A, `contract.py`, `ensemble.py`, `runner.py`, `fallback.py`, the 36-test verdict map and the headless lane unchanged; additive write-side helpers; "shell is A's, data is B's" kept only as a description of the write side; skipped helper "detectable, not prevented"; the LLM-keeps sentence kept; pointers to 3.4 and 3.6. Section 0 gains the `[V]`, `[L]` and "[Variant 2 Round 2, not answered by Variant 1]" lines (plan rules 3 and 5) and a label key.
- **Provenance tag**: `<!-- Source: Base (original, modified) — section replaced per Change #1 (C-001 Hybrid 95%; X-001 and X-002 to Variant 2 at 90% ...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (3.2, 3.3, 3.4, 3.6, INV-017 resolve) | Contradictions ✅ (agrees with 3.4, INV-I, section 8 answer 4)

### Change 2: Scope the consistency section to what the code supports
- **Status**: Applied
- **Source**: Variant 2 section 0 (C-01 row note, weaker reading of INV-020); Variant 1 section 2 (kept)
- **Target**: Base section 2, C-01 row and point (a)
- **Before**: C-01 row without the import note; point (a) said the position edits `cli/reflect` (new finalizer modules, the headless lane's use of them).
- **After**: C-01 row carries "holds for the skill panel only; engine A imports nothing from `cli/review` (V-01)". Point (a): the merged plan adds new files and edits no existing engine-A behaviour, so the weaker reading is enough; C-018 label disagreement points to open sub-dispute 1c. C-02 condition, C-03 dependencies and C-01 points (b), (c) kept (only the name "A" for the base position replaced by "this position").
- **Provenance tag**: `<!-- Source: Base (original, modified) — C-01 row and point (a) edited per Change #2 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (9.2 sub-dispute 1c, 3.2 resolve) | Contradictions ✅

### Change 3: Add a per-module "blast radius" table
- **Status**: Applied
- **Source**: Variant 2 section 2 (table "Under Position B"); S-002
- **Target**: Base section 3.1 (second table after the "what is kept" table)
- **Before**: One table (per part kept).
- **After**: Second table with rows: shared core, `runner.py`, `ensemble.py`/`fallback.py`/`_diversity.py`, `contract.py`/`panel_lint.py`/`models.py`, helper command module (placement two-sided), `scripts/reflect_shadow_exit.py`, SKILL and refs, tasklist and task-builder skills. The two dropped sentences ("engine A's own meaning" for CV-5; "Reuse, not new logic") are absent.
- **Provenance tag**: `<!-- Source: Variant 2, Section 2 (table "Under Position B") — merged per Change #3 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (helper row agrees with 3.3 and 9.2 sub-dispute 2; exit-script row agrees with 3.3)

### Change 4: Rewrite the per-step write-side table (steps 1, 5, 7, 10 plus parity at publish; no step-2 helper)
- **Status**: Applied
- **Source**: Variant 1 section 3.2 (base, edited); Variant 1 advocate D2 (a)(b)(c)(e) and N2; Variant 2 advocate D2 verdict
- **Target**: Base section 3.2 (rows 2, 5, 7; "existing code" column; row 1 kept; combined last row corrected; no separate row 6)
- **Before**: Row 2 "parity computed and recorded by code, reuse `recompute_parity`"; row 5 card writer owns file name; row 7 finalizer from existing extractors; last row "called by the same wrapper".
- **After**: Row 2 deleted as a helper (parity recomputed at publish; `recompute_parity`, `PERSONAS`, `tele`, `card_headers`, `_json_map` move into `src/`); row 5 copies `model:` from `resolution.json`, target file OPEN under INV-015 (Position A legacy names; Position B `panel/cards/reviewer-<N>.md`); row 7 finalizer is new mapping code for 5 of 6 fields; last row is the existing CLI calls (`SKILL.md:345, :347`); header "Existing code reused / new code"; introductory sentence corrected. "Open invariants: INV-015." added.
- **Provenance tag**: `<!-- Source: Base (original, modified) — rows 2, 5, 7 and 10, the last row and the "existing code" column rewritten per Changes #4, #5 and #7; row 1 kept ... -->`
- **Validation**: Structural integrity ✅ (table columns consistent, 6 rows) | References ✅ (INV-015, 9.2 sub-dispute 5 resolve) | Contradictions ✅ (agrees with section 8 answer 2, section 5 INV-L)

### Change 5: Serializer contract: validate and refuse, never filter
- **Status**: Applied
- **Source**: Variant 1 advocate W4 and D2(d); Variant 2 advocate serializer verdict and E-7
- **Target**: Base section 3.2, row 10 (replace "the two constants as allowlist")
- **Before**: "One serializer owns the key set (the two constants as allowlist) and quotes model aliases; the lint runs as a publish gate."
- **After**: Row 10 points to a "Serializer contract" paragraph: YAML with quoted `[1m]` aliases, validate and refuse on a foreign key, never filter; reason `adversarial_subrun_status` (`contract.py:306`, `ensemble.py:793`); JSON-in input marked [Variant 2 Round 2, not answered by Variant 1: E-7]; lint a publish gate for the skill-run lane only; accepted key set OPEN (sub-dispute 3). "Open invariants: INV-005, INV-007, INV-008."
- **Provenance tag**: `<!-- Source: Base (original, modified) — serializer contract: "the two constants as allowlist" replaced per Change #5 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (9.2 sub-dispute 3 resolves) | Contradictions ✅ (agrees with INV-A row)

### Change 6: Helper placement and registration, two-sided
- **Status**: Applied
- **Source**: Variant 1 advocate N1, N6 and D2 placement; Variant 2 advocate R-2 and "D2 placement" verdict
- **Target**: Base section 3.3, first two bullets (replaced); the sentence "cli/review stays free of reflect (C-01)" moved into Position A
- **Before**: Reflect-module code exposed as `superclaude` subcommands; first import edge `cli/reflect` to `cli/review`; the edge "never points the other way".
- **After**: Bullet 1 common ground (not under `reflect_group`, constants never copied, lazy imports, no `src/superclaude/...` path in skill text, one import edge, Check 11 names); bullet 2 the two-sided OPEN entry (compact; full text in 9.2 sub-dispute 2); third bullet (reserved names) kept.
- **Provenance tag**: `<!-- Source: Base (original, modified) — first two bullets replaced per Change #6 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (compact entry and 9.2 entry state the same two positions)

### Change 7: Helper-owned stage advance, scope two-sided, with preconditions
- **Status**: Applied
- **Source**: Variant 1 advocate D2 and W2; Variant 2 advocate E-3 and "D2 stage ownership" verdict
- **Target**: Base section 3.2 (new column "Stage advance") and section 3.3 (new bullet)
- **Before**: No stage-advance text.
- **After**: Column in the 3.2 table (restates Position B's three named stages and says nothing for Position A beyond its general rule); 3.3 bullet: in-process advance with output hashes, skill text stops advancing the stage, `OutOfOrder`/`Conflict`, "a skip is detectable if the kernel verifies output hashes" (never "unskippable"; `manifest.py:285-291` checks only hash format), optional hash-versus-file check; preconditions with the recipe-test rewrite, identical re-advance and exit-script rule marked [Variant 2 Round 2, not answered by Variant 1: E-3, R-3]; scope OPEN (sub-dispute 4). "Open invariants: INV-002, INV-006, INV-013, INV-017."
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... stage-advance bullet added per Change #7 (C-004 Hybrid, 90%; X-002 Variant 2, 90%) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (agrees with INV-I row, section 8 answer 4)

### Change 8: Replace the grounded lane through the wrapper with a deferral
- **Status**: Applied
- **Source**: Variant 1 advocate W1 and D3; Variant 2 sections 3.2 E6-E10
- **Target**: Base section 3.4, first bullet; section 3.1 row "Tier-2 branch" (note on `runner.py:546-572`)
- **Before**: "reached through the skill or through the `ClaudeProcess` else-branch (`runner.py:546-572`)".
- **After**: 3.4 first bullet states DEFERRED with the routing facts (`runner.py:538-545`, `--depth` `standard` or `deep`, marker at `:560`, restricted profile `process.py:145-154`) and keeps the `reflect-reviewer` tool-list facts; 3.1 Tier-2 row carries the note.
- **Provenance tag**: `<!-- Source: Base (original, modified) — grounded-lane bullet replaced by a deferral per Change #8 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (3.6 resolves) | Contradictions ✅ (agrees with section 1)

### Change 9: Add 3.6 "single-engine step"
- **Status**: Applied
- **Source**: Variant 2 section 5 (trigger paragraph) and section 1 (Option 3); Variant 1 advocate D3, D7; Variant 2 advocate E-5, E-8, R-5, D7 verdict
- **Target**: Base new section 3.6 (after 3.5)
- **Before**: Section did not exist.
- **After**: Status NAMED, NOT SCHEDULED; one decision with a fork (Option 3 or D3); only the owner-answer trigger prong written as agreed; M4 prong, T5-gate prong and Stage 5 deadline carried two-sided (1b), the last two marked [Variant 2 Round 2, not answered by Variant 1]; shared preconditions; Option 3 extra preconditions marked; M-B failure is an owner escalation; default direction OPEN (sub-dispute 6). "Open invariants: INV-010."
- **Provenance tag**: `<!-- Source: Variant 2, Section 5 (trigger paragraph) and Section 1 (Option 3); Variant 1 advocate Round 2 D3 and D7; ... — merged per Change #9 ... -->`
- **Validation**: Structural integrity ✅ (H3 under section 3) | References ✅ (4.1 E7, E13, 4.3, section 6 step 4, 9.2 resolve) | Contradictions ✅ (section 1 says neither engine is retired now; 3.6 is conditional and unscheduled)

### Change 10: Headless lane unchanged, with the corrected disclosure sentence
- **Status**: Applied
- **Source**: Variant 2 section 2 and E11; Variant 1 advocate W5, W8, D5; Variant 2 advocate R-4 and D5 verdict
- **Target**: Base section 3.4, second and third bullets (replaced, including "Both lanes end in the same serializer"); section 3.5 (disclosure bullet appended)
- **Before**: A lens change to findings-v2, a lint gate on the headless contract, "moves it into one place where a lint can see it".
- **After**: 3.4: headless lane unchanged (`ensemble.py`, `fallback.py`, `reflect_review.py`, layout), no lens change, no headless lint gate, revisit at 0.704 / 0.867 [UNVERIFIED figures]; the facts on hard-coded versus parameter-supplied counts, with R-4 marked; headless finalizer deferral bullet. 3.5: disclosure bullet with the sentence "a tested deviation seam exists with no production producer" marked as the Variant 2 advocate's R-4 wording; C-007 label OPEN (1a).
- **Provenance tag**: `<!-- Source: Variant 2, Section 2 ("what this position leaves as it is") and E11; ... — merged per Change #10 (C-005 Variant 2, 95%; C-007 unresolved, 55%) -->` and the 3.4 tag
- **Validation**: Structural integrity ✅ | References ✅ (9.2 sub-dispute 1a resolves) | Contradictions ✅ (INV-M and INV-I rows agree)

### Change 11: CV-5 recorded as "acknowledged non-conforming, change deferred" with release conditions
- **Status**: Applied
- **Source**: Variant 1 section 3.5 first bullet (reworded); Variant 1 advocate W3 and D4; Variant 2 advocate R-1
- **Target**: Base section 3.5, first bullet
- **Before**: "`merge_method: adversarial` only after a disk-confirmed merge (CV-5, decided): the count-derived label at `ensemble.py:773` is non-conforming."
- **After**: Same decided sentence plus: `ensemble.py:773` and the I1 witness not edited (V-10); slug effect `null-convergence` to `single-reviewer-fallback`, exit 11 unchanged; `LEGAL_MERGE_METHODS` has two values; no verdict effect today; release conditions (a) and (b); conditions also written in SKILL section 9.2 beside the CV-5 sentence.
- **Provenance tag**: `<!-- Source: Base (original, modified) — first bullet replaced per Change #11 (C-011 Hybrid 90%; X-003 Hybrid 95%; X-009 Variant 1 90%) -->`
- **Validation**: Structural integrity ✅ | References ✅ (3.6 resolves) | Contradictions ✅ (INV-B row agrees)

### Change 12: Do-now document and script fixes, D1
- **Status**: Applied
- **Source**: Variant 2 sections 1(i), 2; Variant 1 advocate D1
- **Target**: Base section 3.5, second bullet; status DO NOW
- **Before**: "The skill prose ... is reconciled to the code; that is a skill text edit, not a code change."
- **After**: DO NOW list: CV-1 and CV-2 prose at `SKILL.md:703, :1317, :1480-1481, :1755`; CV-3 one diversity word; CV-9 at `scripts/reflect_shadow_exit.py:313`; CV-6 and CV-8 lines from the third and fourth bullets; `:838-839` residue with the reconciling statement in `### 9.2`; arm-A re-measure after D1 marked [Variant 2 Round 2, not answered by Variant 1]. Merged with Change 20's append in one bullet. "Open invariants: INV-009, INV-012, INV-015."
- **Provenance tag**: `<!-- Source: Base (original, modified) — second bullet extended per Change #12 ... and Change #20 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 6 step 0 resolves) | Contradictions ✅ (INV-K row agrees)

### Change 13: Complete CV-8 document correction
- **Status**: Applied
- **Source**: Variant 2 section 2 (document row); Variant 1 advocate W12; V-18
- **Target**: Base section 3.5, fourth bullet "Executor exclusion"
- **Before**: Documents "are [CODE-CONTRADICTED] for the production path"; the base corrected no document now.
- **After**: Corrected now with the complete list: `sc-tasklist-protocol/SKILL.md:1141, :1152, :1165, :1170, :1177`, `task-builder/SKILL.md:2389`; `:2247` described as what it says; per-lane mechanics kept as the later route in 3.6; INV-009 kept open. "Open invariants: INV-009."
- **Provenance tag**: `<!-- Source: Base (original, modified) — fourth bullet's correction sentence replaced per Change #13 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 14: `--t2-engine` gets no new value; `reviewer_briefs_materialized` on three ref lines
- **Status**: Applied
- **Source**: Variant 2 section 2 (`--t2-engine` row) and section 4 INV-A row; V-16, V-30
- **Target**: Base section 3.5, third bullet; section 3.1 (one row appended)
- **Before**: `refs/reviewer-spec.md:51, :57, :78`; "the ref is the side that changes unless 9.2 and both constants are amended together".
- **After**: Ref edited on all three lines (CV-6), "ref edit first"; `--t2-engine` stays a skill flag, no new value, `panel` rejected (`SKILL.md:87`) while kernel `ENGINES` accepts it (`manifest.py:51`); 3.1 gains the `--t2-engine` row.
- **Provenance tag**: `<!-- Source: Variant 2, Section 2 (`--t2-engine` row) and Section 4 (INV-A row) — merged per Change #14 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (INV-A row agrees)

### Change 15: Add staging evidence rows
- **Status**: Applied
- **Source**: Variant 2 section 3.1, E1-E5; U-010
- **Target**: Base section 4.1 (rows E9-E13 after E8; `commands.py:254-257` appended to E1)
- **Before**: Rows E1-E8.
- **After**: E9 (engine A contract is `mode: post`), E10 (skill panel UC-1 shadow only, `panel` rejected, UC-2 ignored until Stage 5), E11 (panel never run as authoritative engine), E12 (no consumer passes `--t2-engine`), E13 (Stages 3 and 4 never reach the wrapper; collision starts at Stage 5), E13 marked [Variant 2 Round 2, not answered by Variant 1: E-5] and named as the evidence behind the deadline of 1b.
- **Provenance tag**: `<!-- Source: Base (original, modified) — rows E1 and E7 extended per Changes #15 and #16; ... rows E9-E13 incorporated from Variant 2, Section 3.1 (E1-E5) and Section 3.5 (E21, E22) per Change #15 (U-010) ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (the label "E9" of the Variant 2 text is disambiguated in 9.1 as "not row E9 of 4.1") | Contradictions ✅

### Change 16: Retirement accounting and preconditions
- **Status**: Applied
- **Source**: Variant 2 section 3.5 E21 and E22; Variant 2 advocate R-5 and E-2; Variant 1 advocate W6
- **Target**: Base section 4.1, row E7 (appended); section 4.3 (one bullet appended)
- **Before**: E7 listed "snapshot-grounded children" as an unqualified loss.
- **After**: E7: snapshot carried as a flag-gated option (`models.py:94-100`); test mass 507 matches in 44 files (97 and 58); I1 witness `:141-171`; `fallback.py:49-82`; survivors; replacement for the I1 witness marked [Variant 2 Round 2, not answered by Variant 1: R-5, E-2], with the common point that a replacement is needed. 4.3 bullet: reviewer-count rule as a 3.6 precondition, `read_committed` wiring marked. "Open invariants: INV-010."
- **Provenance tag**: see Change 15 (4.1 tag) and the 4.3 tag `<!-- Source: Base (original, modified) — GQ-067 bullet rewritten per Change #17 ... two bullets appended per Changes #17 and #16 -->`
- **Validation**: Structural integrity ✅ | References ✅ (3.6 resolves) | Contradictions ✅

### Change 17: Evidence limits: allowlist, in-repo readers, reuse claims, GQ-067
- **Status**: Applied
- **Source**: Variant 1 advocate shared-assumption table; Variant 2 section 8 (GQ-067 / OQ-8); V-12, V-32
- **Target**: Base section 4.3 (bullets appended; GQ-067 sentence rewritten)
- **Before**: GQ-067 as a wrapper-switch question; "valid under either answer".
- **After**: "an analysis, not an observation" kept; GQ-067 is the readers question (`synth-10` Q-08), needs an in-repo reader inventory (`sc-tasklist-protocol/SKILL.md:1171, :1179`, `phase-template.md:191, :199`, `task/SKILL.md:580`); "valid under either answer" deleted; the "exactly one" key claim qualified (counts 19 and 18, `_make_result` alias reads uncounted) and left open under INV-008. "Open invariants: INV-008."
- **Provenance tag**: 4.3 tag as in Change 16
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (agrees with 3.2 serializer contract and 9.2 sub-dispute 3)

### Change 18: Rewrite the INV-L row: common ground plus a two-sided shape
- **Status**: Applied
- **Source**: Variant 1 advocate D2a; Variant 2 advocate E-1, E-2 and the D2a verdict; Variant 2 section 4 INV-L row
- **Target**: Base section 5, INV-L row
- **Before**: One artifact (the contract) as the change of writer; admissible only if value-equal on recorded runs.
- **After**: "Endangered, HIGH" kept; common ground (comparison artifact until promotion; promotion after M-A and M-B and 0 verdict differences); shape OPEN: Position A (D2a) `panel/contract.code.yaml` plus siblings, Position B (E-1) three points, marked [Variant 2 Round 2, not answered by Variant 1]; kernel facts (`publish_files` refused in shadow `manifest.py:496-500`; `read_committed` unwired); owner question copied as written. "Open invariants: INV-001, INV-014, INV-019."
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... INV-L per Change #18 (C-017 Hybrid, 90%; E-1 and E-2 are Variant 2 Round 2) ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (9.2 sub-dispute 5, section 6 steps 0, 1, 3 resolve) | Contradictions ✅

### Change 19: Correct the INV-A, INV-B, INV-I and INV-M rows
- **Status**: Applied
- **Source**: Variant 1 advocate W3, W4, W5 and "What I concede to V2"; Variant 2 section 4
- **Target**: Base section 5, rows INV-A, INV-B, INV-I, INV-M
- **Before**: INV-A "Preserved ... allowlist"; INV-B "one narrow effect ... MEDIUM"; INV-I "Preserved and extended"; INV-M "headless output directories Preserved" next to an M4 that changed the layout.
- **After**: INV-A "validates and refuses", condition "ref edit first", names `adversarial_subrun_status`; INV-B preserved for the map and 36 tests, CV-5 deferred, "narrow effect" sentence deleted, I1 witness collision stated, HIGH if the edit were made; INV-I "Preserved" (fail-closed only where a Python parent exists; extension returns with a headless finalizer); INV-M "Preserved", true because the headless layout and lens do not change.
- **Provenance tag**: section 5 tag (see Change 18)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (the four rows agree with 3.4, 3.5 and section 8)

### Change 20: Rewrite INV-K and the edit-fence accounting
- **Status**: Applied
- **Source**: Variant 2 section 4 (INV-A and INV-K rows); Variant 1 advocate W11; V-15
- **Target**: Base section 5, INV-K row; section 3.5 skill-text bullet (appended)
- **Before**: "SKILL.md edits stay under `### 4.3a` (allowed)".
- **After**: Allow-list widened in the same change for `## 8`, `## 12`, `## 14` lines; `:838-839` recorded residue with the reconciling statement in `### 9.2`; base's `arch_lint` finding kept; `test_no_new_src_superclaude_hit_in_the_skill_directory` (`:78-98`) added; edit-location rule (skill and ref edits under `src/superclaude/...`, then `make sync-dev`). "Open invariants: INV-016."
- **Provenance tag**: section 5 tag and the 3.5 second-bullet tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (3.5 bullet and INV-K row agree; see Executor Note 4)

### Change 21: Add invariant rows for the recursion marker and the import chain
- **Status**: Applied
- **Source**: Variant 1 advocate N1, N6; Variant 2 advocate verification table (both "HOLDS IN PART")
- **Target**: Base section 5 table (two rows after INV-N)
- **Before**: No such rows.
- **After**: "Added: recursion marker does not silence the new commands" (preserved only if not under `reflect_group`; pin (iii)) and "Added: import chain" (preserved only if lazy; import-direction pin two-sided). Neither row invents an INV id.
- **Provenance tag**: section 5 tag
- **Validation**: Structural integrity ✅ | References ✅ (section 6 step 2, 9.2 sub-dispute 2 resolve) | Contradictions ✅

### Change 22: Restructure section 6 into the ordered measurement sequence
- **Status**: Applied (with one deliberate omission, Executor Note 5)
- **Source**: Variant 1 section 6 (M1-M5); Variant 2 section 5; Variant 1 advocate D6 and W9; Variant 2 advocate E-1, E-4, E-7, R-3, R-4 and the D6 verdict
- **Target**: Base section 6 (restructured)
- **Before**: M1 pins, M2 replay oracle, M3 completeness, M4 headless lane, M5 quality.
- **After**: Steps 0-5 with counts-for, counts-against and a decision rule each: (0) arm A, marked Variant 2 Round 2 (E-4); (1) M-A narrowed; (2) pins; (3) M-B with arms OPEN (sub-dispute 5); (4) M3-ext; (5) Variant 2's M4 dropped. Mapping from old M1-M5 stated at the top. Old M4 removed with the headless lint gate; old M5 kept as "Quality (old M5): a stated non-claim". Run counts stay unchecked. "Open invariants: INV-003, INV-011 (step 0); INV-007, INV-008 (step 1); INV-008 (step 2); INV-003, INV-011, INV-013, INV-014 (step 3)."
- **Provenance tag**: `<!-- Source: Base (original, modified) — section restructured into the ordered measurement sequence per Change #22 (C-019 Hybrid, 90%; S-005 Hybrid, 90%); ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (M-A, M-B, M3-ext, steps 0-5, sub-disputes 1b and 5 resolve) | Contradictions ✅

### Change 23: Add the four pins and the recipe-test rewrite
- **Status**: Applied
- **Source**: Variant 1 advocate N6 and D6 step 2; Variant 2 advocate pins verdict
- **Target**: Base section 6 (under step 2)
- **Before**: M1 pins listed as "pass, or each rewritten pin is named".
- **After**: Pins (i) source-contract test, (ii) import-direction pin (two-sided), (iii) marker-set run, (iv) moved-parity unit test; rewritten recipe test; identical re-advance no-op test marked [Variant 2 Round 2, not answered by Variant 1: E-3]; existing pins stay green untouched. "Open invariants: INV-008."
- **Provenance tag**: section 6 tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (agrees with INV rows added by Change 21)

### Change 24: Replace M3 with M3-ext, the extended seam probe
- **Status**: Applied
- **Source**: Variant 2 section 5 (M3, U-011); Variant 1 advocate N3; Variant 2 advocate N3 verdict
- **Target**: Base section 6 (step 4 of Change 22)
- **Before**: Old M3 was "completeness of the failure classes" (folded into step 3).
- **After**: Probe with the marker set and `reviewer_profile=True`: agent calls complete, artifacts on disk, a `review` command not suppressed; also run against engine A's own scorer child (`ensemble.py:537-553`), marked [Variant 2 Round 2, not answered by Variant 1: N3 verdict]; outcomes stated in advance; gates D3 and Option 3 only.
- **Provenance tag**: section 6 tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 25: Update the PR and rf-qa effects section
- **Status**: Applied
- **Source**: Variant 2 section 6; Variant 1 advocate W1, W9; V-03
- **Target**: Base section 7: `--fix` bullet (replaced), M13 bullet and M10/M11 bullet (appended)
- **Before**: "A makes a dormant path live".
- **After**: `--fix` stays dormant and nothing here moves it; the grounded lane is deferred (3.6); M13 refers to the M-A replay (section 6 step 1); M10/M11 gains "the kernel stays free of `cli/swarm`; swarm is imported by `ensemble.py`, `fallback.py`, `_diversity.py:5`" and "generality of the helpers for PR review is not verified". The last bullet (effect on a later review of the change) adjusted to the open import-edge direction and widened fence.
- **Provenance tag**: `<!-- Source: Base (original, modified) — `--fix` bullet replaced and M13 and M10/M11 bullets extended per Change #25 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 26: Correct the strongest-objection answers
- **Status**: Applied
- **Source**: Variant 1 advocate W2, W7; Variant 2 section 7 answers 3 and 4
- **Target**: Base section 8, answers 1, 2 and 4 (replaced); answers 3 and 5 kept
- **Before**: Answer 1 "the only option in which no capability on that list is dropped"; answer 2 "The new code is the write side only. The readers exist"; answer 4 "fail the run closed".
- **After**: Answer 1: no capability moves now, none dropped, engine choice is 3.6, base claim withdrawn; answer 2: extractors cover one of six fields, `recompute_parity` in `scripts/`, finalizer and moved parity are new code with tests; answer 4: fail-closed only where a Python parent exists, detectable not prevented, M-B measures it, INV-017 open. Answers 3 and 5 kept; the measurement names in answer 5 updated to the new section 6.
- **Provenance tag**: `<!-- Source: Base (original, modified) — objection carried (position name only); answers 1, 2 and 4 replaced per Change #26 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (agrees with section 1, INV-I row, 3.4)

### Change 27: Add section 9: open items, open sub-disputes, unaddressed invariants
- **Status**: Applied
- **Source**: Variant 2 section 8; debate Convergence Assessment; `invariant-probe.md`; plan sections "Open Sub-Disputes" and "Unaddressed invariants"
- **Target**: Base new section 9 (9.1 open items, 9.2 open sub-disputes, 9.3 unaddressed invariants)
- **Before**: Section did not exist.
- **After**: 9.1: GQ-067, OQ-20, RE-4 [UNVERIFIED], Variant 2's E9 (disambiguated from row E9), INV-L wording, owner's headless answer and Stage 5 deadline, unchecked run counts, pointer to 9.3. 9.2: six two-sided entries copied from the plan, each marked OPEN, the Variant 2 Round 2 items marked. 9.3: the 17-row table, each OPEN (15 MEDIUM, 2 LOW), "Attaches to" expressed as places in the merged file.
- **Provenance tag**: three tags, one per subsection (Variant 2 Section 8; debate Round 2 final positions and Convergence Assessment; `invariant-probe.md`)
- **Validation**: Structural integrity ✅ (H3 9.1-9.3, H4 sub-disputes under 9.2) | References ✅ | Contradictions ✅

## Executor Notes (deviations, judgment calls and residual risks)

1. **Naming.** In text carried over from the base, the base's name "A" for its own position is replaced by "this position" (cosmetic), so that "Position A" and "Position B" in two-sided entries mean only the two advocates' Round 2 positions. Quotations of base text keep the original wording. Section 0 states this.
2. **Tag `[L]`.** Plan rule 3 defines `[L]` as taken from the diff-analysis ledger. Several citations in the plan come from the Round 2 files or from the plan itself and not from the ledger; they are tagged `[L]` and section 0 defines `[L]` to include them. No citation was re-read by the executor (plan rule 3).
3. **Section 9.3 "Attaches to" column.** The plan's column names plan change numbers. The merged file has no change numbers, so the column names the place in the merged file where the invariant attaches. The "Open invariants: INV-nnn" lines at the end of each attached block are present as the plan requires.
4. **Observation, not resolved (`SKILL.md:838-839`).** The plan (V-15) says only `:839` carries a comment; Variant 2's text (section 2, INV-A row) calls both `:838` and `:839` stale inline comments. The merged file carries the plan's statement, tagged `[L]` (3.5, second bullet), and does not decide between them. The design does not depend on it: both lines stay as residue inside frozen 9.1.
5. **Deliberate omission in Change 22 (old M5).** The base's last sentence of M5 ("A would be shown wrong for the headless lane if that lane's findings add nothing the grounded lane lacks ... the added surface of that lane would then have no measured justification") is not carried. Its object, the headless lane's added surface (lens change, lint gate), was removed by Change 10, so the sentence would describe something the merged position does not build. The plan keeps M5 "a stated non-claim"; the non-claim and the named seeded-defect measurement are kept. If the lead wants the sentence verbatim it can be restored.
6. **Label clash E9.** Plan change 27 says "E9 closed only by M3-ext", where E9 is Variant 2's seam-probe item. The merged file's 4.1 has its own row E9 (engine A's contract is `mode: post`). 9.1 therefore says "Variant 2's item E9 (not row E9 of 4.1)".
7. **Stage-advance cells in 3.2.** The plan asks for a column "who advances the stage". The cells restate only what Position B names (`resolved`, `calibrated`, `debated` helper-owned; `clustered` and `validated` orchestrator-advanced) and the table note says Position A's general rule; nothing is written for Position A that its text does not say.
8. **Two-sided entries appear twice.** Sub-dispute 2 (placement), 4 (stage scope) and 5 (INV-L shape) are stated compactly where they bite (3.3, 3.2 and 3.3, section 5 and section 6 step 3) and in full in 9.2. The compact and full versions state the same two positions.
9. **Residual risk carried from the plan.** Counts and line numbers in changes 22 and 23 come from the debate and are not re-read (plan review log, last paragraph). All run counts stay unchecked (V-34).
10. **Hook note.** The freshness hook required a Read of each output file before the first Edit of it in this session; both files were written by the executor and were then read once.

## Post-Merge Validation

Checks were run on `merged-output.md` (374 lines) with Grep and a read-only shell count; no code was re-read.

### Structural Integrity
- Heading hierarchy: ✅ One H1; H2 sections 0 to 9 in order; H3 under 3 (3.1-3.6), under 4 (4.1-4.3) and under 9 (9.1-9.3); H4 only under 9.2 (sub-disputes 1-6). No level gaps, no orphaned subsection, document starts with H1 after the provenance comments.
- Section ordering: ✅ Base order kept (0-8); 3.6 follows 3.5; section 9 follows section 8. Forward references (3.2 to section 6 and 9.2, section 1 to 3.6) point to sections that exist.
- Document flow: ✅ No placeholder or `{{` left (0 matches); provenance header (3 comment lines) present; 27 `<!-- Source: ... -->` tags on sections and significant blocks; status line present at top and at end; convergence facts present (42 of 45, 93.33%, 3 unresolved labels, 17 UNADDRESSED, none HIGH).
- Plan rules: ✅ Rule 1 (six two-sided OPEN entries, 41 occurrences of "OPEN"); rule 2 (all 17 UNADDRESSED invariants in 9.3 and attached in the body); rule 3 (base tags kept; `[V]` and `[L]` added; line added to section 0); rule 4 (edit-location rule stated, no instruction to stage any mirror path; checked by search: no `.claude/` path and no `git add` in the file); rule 5 (23 uses of "Variant 2 Round 2, not answered by Variant 1", covering E-4 step 0, E-5 deadline, E-7 JSON-in, E-2 `read_committed` wiring, R-4 wording, the T5-gate prong, E-1 shape, E-3 preconditions, R-3 exit-script rule, N3 scorer-child probe, R-5 replacement).

### Internal References
- Total references: 255 (counted by pattern on non-comment lines: 120 section tokens of the form 3.1-3.6, 4.1-4.3 and 9.1-9.3; 37 "section N" references; 98 label references to steps 0-5, sub-dispute 1-6, rows E7, E9-E13, and the labels M-A, M-B, M3-ext). The count is by pattern and may include a few false positives.
- Resolved: 255
- Broken: 0
- Not counted as internal (external to the paper): references to the skill file's own headings (`### 9.1`, `### 9.2`, `### 4.3a`, `### 5.4`, "SKILL section 9.2", "SKILL section 10", "`SKILL.md` 9.4": 16 tokens of the `### 9.x`/"SKILL section 9.2" form plus the others), `s06` section 6.12.0, research-file section labels (`s6.2`, `s8(d)` and so on), and the debate-record labels (V-nn, N1-N7, W1-W12, R-n, E-n, X-nnn, C-nnn); section 0 defines them as provenance labels.
- Invariant labels: ✅ INV-001 to INV-019 (17 rows) each appear in 9.3 and in the body at their attachment point; INV-A to INV-N (14 rows) are in the section 5 table, plus the two added rows; INV-004, INV-018 and INV-020 are referenced as ADDRESSED only. INV numbers of other slots in section 2 are identified as such in section 0.
- Evidence rows: ✅ E1 to E13 are all rows of 4.1; the one label clash (Variant 2's item E9) is disambiguated in 9.1 (Executor Note 6).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Rows and sections the plan names, checked against the new D2, D4 and D5 text:
  - INV-B row against 3.5 (first bullet, D4) and section 8: ✅ CV-5 edit deferred in all three; I1 witness collision HIGH only if the edit were made.
  - INV-I row against 3.4, section 1 and section 8 answer 4: ✅ fail-closed only where a Python parent exists; the headless finalizer is deferred; skipped helper detectable, not prevented, in all four places.
  - INV-K row against 3.5 (D1 bullet) and 3.1 SKILL row: ✅ same lines (`:703` under `## 8`, `:1317` under `## 12`, `:1480-1481` under `## 14`), allow-list widened in the same change, `:838-839` residue with the statement in `### 9.2`.
  - INV-M row against 3.4 (D5): ✅ headless layout and lens unchanged.
  - INV-A row against 3.2 serializer contract, 3.5 third bullet and 9.2 sub-dispute 3: ✅ validate and refuse; ref edit first; accepted set two-sided.
  - INV-L row against 3.2 (rows 5, 7, 10), section 6 step 3 and 9.2 sub-dispute 5: ✅ comparison artifact until promotion; shape stated two-sided everywhere.
  - Section 1 against 3.6: ✅ "neither engine is retired now"; 3.6 is conditional and NOT SCHEDULED.
  - Search for phrases the plan deletes ("only option in which no capability ... is dropped", "becomes a code step that the orchestrator calls", "valid under either answer", "unskippable", "engine A's own meaning", "Reuse, not new logic", "narrow effect"): ✅ they remain only inside sentences that record their deletion.
- Tensions that exist in the debate and are carried, not introduced by the merge: the card-writer target (INV-015), whether helper refusal fits shadow's "continue as legacy" (INV-006), the `:838-839` comment count (Executor Note 4), and the six OPEN sub-disputes.

## Summary

- Total changes planned: 27
- Successfully applied: 27
- Failed: 0
- Skipped: 0
- Applied with a recorded judgment call: Change 22 (one base sentence of old M5 not carried, Executor Note 5); Changes 4 and 7 (stage-advance cells state only Position B's named stages, Executor Note 7)
- Open items carried, not resolved by the merge: 6 two-sided sub-disputes (9.2), 17 UNADDRESSED invariants (9.3: 15 MEDIUM, 2 LOW, 0 HIGH), the items listed in 9.1
- Post-merge validation: PASS
