# Cross-Validation Report — FR-DRS Research (Partition P1)

**Analysis type:** completeness-verification (cross-validation lens)
**Date:** 2026-06-22
**Partition:** P1 of 2 — PRIMARY files 01, 02, 03, 04; seam-read 05, 06, 07
**Track goal:** Implement FR-DRS deterministic runtime-surface sweep + integration per the TDD
**Output:** analyst-cross-validation-report-p1.md

> PARTITION NOTE: Cross-file checks anchored on P1 (files 01-04). Files 05-07 read for
> cross-partition seam verification only. Full cross-file analysis (including 08 and any
> P2-owned consistency) requires merging this report with the P2 partition report.

---

## Seam Verification Matrix (in progress)

| Seam | Files | Status |
|------|-------|--------|
| R1↔R4: rootwalk unit vs _bfs_reachable adaptation | 01,04 | PENDING |
| R2↔R3: surface_unreached derivation OWNER | 02,03 | PENDING |
| R1↔R2: run_sweep signature vs _audit_once args | 01,02 | PENDING |
| R2↔R3: six-field merge point + contract.py wiring | 02,03 | PENDING |
| R3↔R6: §5.3 pre-filter vs §6.1 demotion ownership | 03,06 | PENDING |
| file:line agreement for shared symbols | all | DONE — CONSISTENT |

> Matrix updated after analysis. Detailed seam findings below.

---

## Seam 1 — R1↔R4: rootwalk unit (01 §1.7/§1 Unit 5) vs `_bfs_reachable` adaptation (04 §1)

**Question:** Is depth=1 + DEGRADE-on-partial consistent between R1's `rootwalk_entrypoints` design and R4's `_bfs_reachable` copy plan?

**Verdict: CONSISTENT — no contradiction.**

- **depth=1.** R1 §1 Unit 5 pins "walk from each root toward the candidate with **depth bound = 1**" and §1.7 gates "Confirmed UNREACHED ONLY on complete enumeration with no depth=1 root hit." R4 §1.2/§1.3 independently states the SAME bound and adds the mechanism detail R1 does not: the audit source `_bfs_reachable:591-635` "has NO depth parameter" so "depth=1 must be enforced by the caller." This is REFINEMENT, not contradiction.
- **DEGRADE-on-partial.** R1 §1 Unit 5 rule (5): "any root errors/skipped/unenumerable OR depth bound hit before resolution → enumeration partial → DEGRADE, never UNREACHED." R4 §1.3 skeleton: `if not enumeration_complete: return "DEGRADE"`. Identical semantics. Both cite the 3-state return (REACHED/UNREACHED/DEGRADE) replacing the audit binary `(bool, path)`.
- **Oracle-before-rootwalk ordering.** R1 §8 guarantees 1+2 and R4 §1.3 note ("the degrade-oracle … MUST run before the rootwalk emits any UNREACHED … the rootwalk's own enumeration_complete=False→DEGRADE is the second DEGRADE gate; the oracle is the first") AGREE on ordering and the two-gate structure.
- **Builder-trap agreement.** R4 §1.2 flags `depth>50` at `reachability.py:460` as `_parse_module_recursive`, NOT the BFS — a trap R1 does not mention but does not contradict. Complementary.
- **Counter-hygiene.** R1 §5.2 ("DEGRADE symbols are EXCLUDED from `unreached_surfaces`") and R4 §1.3 ("a DEGRADE symbol is NOT appended to `unreached_surfaces`, preserving `len(unreached_surfaces) == runtime_surface_unreached`") AGREE in intent.

**Minor SEAM-ALIGNMENT note (not a contradiction):** R1 §1 Unit 5 authoritative signature is `rootwalk_entrypoints(surface, roots) -> RootwalkResult` (dataclass with `status`/`hit_root`/`enumeration_complete`). R4's illustrative skeleton names it `rootwalk_depth1(roots, symbol, edges, enumeration_complete) -> Literal["REACHED","UNREACHED","DEGRADE"]`. These are two renderings of one unit — R1 owns "the 6 unit WHAT" per its §9 boundary; R4 owns "ONLY the cli/audit source being copied/adapted." R4's skeleton is provenance-illustrative, not a competing signature. Builder should take R1's `RootwalkResult` return shape. Severity: Minor.

---

## Seam 2 — R2↔R3: `surface_unreached` derivation OWNER (double-ownership check)

**Verdict: CONSISTENT — clean primary/fallback split, no double-ownership.**

- R3 §4 "Owner": **RECOMMENDED = the sweep / reflect CLI wrapper writes `surface_unreached` at `runner._audit_once`** (same merge point as the six scalars, just before `parse_contract` @445); **FALLBACK = `derive_verdict` (contract.py:130)**. R3 explicitly: "This item straddles R2/R3 — R3 owns the contract.py fallback half + the §5.3 gate transform; R2 owns the runner merge-point write. Cross-reference R2."
- R2 §7/§2: R2 owns the runner merge-overwrite of the six scalars at the `_audit_once` chokepoint. R2 does NOT claim ownership of the `surface_unreached` field by name — it owns the merge *mechanism/location* R3 designates as the derivation's recommended home.
- COMPLEMENTARY: R3 designs WHAT the derivation transform is and names the merge point as its home; R2 owns the merge-point write. They cross-reference each other's seams explicitly. No contradiction.

**Cross-check — merge-point anchors agree:** R3 §4 ("runner._audit_once @394, parse_contract @445"); R2 §2/§3 ("_audit_once (394-453)", "parse_contract(config.contract_path) at runner.py:445", insertion "between current runner.py:444 and runner.py:445"). IDENTICAL anchors.

---

## Seam 3 — R1↔R2: `run_sweep` signature (01 §3) vs `_audit_once` arg construction (02 §1)

**Verdict: CONSISTENT — R2 REFINES (does not contradict) R1.**

- **Signature byte-match.** R1 §3 and R2 §1 quote the SAME pinned signature: `run_sweep(diff, base_ref, scope_worktree, tasklist, output_dir, availability_surface, *, lsp=None) -> SweepResult`. Both cite TDD §8.1.2. Identical arg names, order, and the keyword-only `lsp`.
- **The arg-GAP finding is a REFINEMENT, not a contradiction.** R1 §3 narrates the *intended* sourcing, mirroring the TDD (e.g. `availability_surface` "from the Wave-0 probe on the config"). R2 §1 INDEPENDENTLY VERIFIED against current source and found 3 of 6 args have NO backing config field: `diff` (no diff-text field — compute `git diff config.base`), `scope_worktree` (no field — derive/add), `availability_surface` (no field, no Wave-0 probe — TDD's "already on the config" claim "INCORRECT against current source").
- This matches each file's declared role: R1 owns the [SPEC]-tagged design (ports the TDD); R2 owns the [CODE-VERIFIED] product seam. R1's design is not wrong — it relays the TDD; R2 catches that the TDD's config-sourcing assumption fails against current `models.py`/`config.py`. **High-value cross-validation: R2 corrects an unverified TDD assumption R1 faithfully relayed.** Builder gets R1's design + R2's "3 clean, 3 gaps" reality check.

**Fast-path consistency.** R1 §3 step 3 (FR-012 fast path: `tagged == [] → SweepResult` with `sweep_ran:False`, no ledger) is consistent with R2's `runtime_surface_sweep_ran` detection contract and R5/R7's fast-path unit. No conflict.

**Consumer-ordering consistency.** R1 §3 ("scalars merge-overwrite before any consumer parses") = R2 §3 (D4: sweep+merge before `parse_contract`). Aligned.

---

## Seam 4 — R2↔R3: six-field merge point + contract.py wiring (line-number conflict check)

**Verdict: CONSISTENT — same anchors, no conflict.**

- Both place the six-scalar merge at the `_audit_once` chokepoint before `parse_contract` (R2 §2-§3 @444→445; R3 §0/§4 @445).
- **The 6th-field prefix caveat is stated IDENTICALLY in three files:** R1 §7 ("only 5 of 6 carry `runtime_surface_`; `unreached_surfaces` has NO prefix; never a `startswith` glob"), R2 §2/§7 ("the 6th field `unreached_surfaces` has NO prefix — key on exact names, never a `startswith("runtime_surface_")` glob"), R3 §6 (keys on exact names). No divergence.
- **No producer/consumer overlap.** R3 §1 (add `"runtime-surface:backend_unavailable"` to `_DEGRADED_COMPONENTS_HALT_SET` @contract.py:31-33, reuse `"degraded-components"` @259-260), §2 (`_halted_reason` NO-EDIT, producer populates `deviation_count_by_class.regression`, existing @324-325 branch reuses `"regression"`), §3 (count-invariant guard mirroring @200-209). R2 owns producer; R3 owns consumer. Seam drawn in R3 §6 and matches R2 §7. No double-ownership.

**Cross-check — the `runtime-surface:backend_unavailable` token agrees across R3, R5, R6:** R3 §1, R5 §6 ("append `runtime-surface:backend_unavailable` to `degraded_components`, add token to `_DEGRADED_COMPONENTS_HALT_SET`"), R6 P3 (SKILL.md:489 PRESERVE). All quote the EXACT token string. Strong consistency.

---

## Seam 5 — R3↔R6: §5.3 pre-filter (R3) vs §6.1 demotion (R6) ownership split

**Verdict: CONSISTENT — clean ownership split, no overlap contradiction.**

- R3 §5/§6: "§6.1/§9.1 demotion = R6 (NOT R3). R3's SKILL scope is §5.3 only, which is **verify-and-leave**." R3 §5 confirms §5.3 lines 390-391/402/412 are ALREADY present and match the TDD — R3 does NOT edit them.
- R6 §2 CRITICAL note: "the demotion is confined to §6.1 (lines ~465-491). The §5.3 pre-filter (R3's territory) and the §9.1 contract field set … are NOT rewritten." R6 P9-P11 lists §5.3 lines 390/391/402/412 as PRESERVE (don't touch).
- MUTUAL cede: R3 owns §5.3 (verify-and-leave), R6 owns §6.1 (demote). Neither claims the other's region. **No overlap contradiction.**

**Cross-check — §5.3 line numbers agree:** R3 §5 table (386/388-389/390/391/398/402/412) and R6 P9-P11 (390/391/402/412). Shared anchors IDENTICAL.

**Cross-check — derived value literal agrees triple:** R3 §4 (`surface_unreached = "runtime_surface_unreached"`, SKILL.md:412), R6 P11 (schema literal `"runtime_surface_unreached"`), R7 §2.4 (derivation test asserts exact string `"runtime_surface_unreached"`). Triple-consistent.

---

## Shared-symbol file:line citation agreement (the named-symbol cross-check)

Every symbol cited in ≥2 files within scope, with the file:line each researcher gives. All agree.

| Symbol / anchor | R1 (01) | R2 (02) | R3 (03) | R4 (04) | R5 (05) | R6 (06) | R7 (07) | Agreement |
|---|---|---|---|---|---|---|---|---|
| `_audit_once` | 394-453 (§3) | 394-453 (§0,§2) | @394 (§0,§4) | — | — | — | — | CONSISTENT |
| `parse_contract` call site | 445 (§3 implied) | 445 (§2,§3) | 445 (§0,§4) | — | — | — | — | CONSISTENT |
| fix-loop re-audit | — | 561-562 (§3) | — | — | — | — | — | single-source |
| `_IndentDumper` | 58-67 (§1 builder note) | 58-67 (§5) | — | 58-67 (§4.2,§5.1) | — | — | — | CONSISTENT |
| `_atomic_write_text` | (§1 builder note) | 70-89 (§5) | — | 70-89 (§5.1) | — | — | — | CONSISTENT |
| `ensemble.REFLECT_CONTRACT_VERSION` ("1.0") | — | 59 (§4) emit @501 | — | — | — | 59 (§3.2) used @501 | 59 (§Stale Doc) | CONSISTENT |
| `models.py:contract_path` property | 96 (§3) | 95-98 (§0,§1) | — | — | — | — | — | CONSISTENT (95-98 spans the 96 R1 cites) |
| `_DEGRADED_COMPONENTS_HALT_SET` | — | — | 31-33 (§1), fires @259-260 | — | — | — | — | single-source |
| `_LOAD_BEARING_BOOL_FIELDS` fail-closed block | 200-209 (§5.2) | — | 200-209 (§3), set @47-57 | — | — | — | — | CONSISTENT |
| `_halted_reason` regression branch | — | — | 307/324-325 (§2) | — | — | — | — | single-source |
| `_bfs_reachable` | (§1.7 named, no line) | — | — | 591-635 (§1.1) | — | — | — | CONSISTENT (R1 names, R4 pins) |
| `pyproject.toml [project.scripts]` | 68-69 (§1.7) | — | — | (named, no line) | — | — | — | CONSISTENT |
| `grader.py` C-6 bucketing | — | — | — | — | 448-449 (§2) | — | — | single-source |
| `check_yaml_list_len_eq` | — | — | — | — | 191-210 (§1.2) | — | — | single-source |
| SKILL.md §5.3 lines | — | — | 390-391/402/412 (§5) | — | — | 390/391/402/412 (P9-P11) | 412 (§2.4) | CONSISTENT |
| SKILL.md §9.1 six-field block | (§7 names fields) | — | 721-735 (§5 cross-check) | — | — | 720-736 (§3.1) | — | CONSISTENT |
| SKILL.md:489 sweep paragraph | — | — | — | — | — | 489 (§1.2,P1-P4,P8) | — | single-source |
| count invariant `len(unreached_surfaces)==runtime_surface_unreached` | §5.2 | §3 | §3 (guard) | §1.3 | §1.2 (case 41) | P8 | §2.1 | CONSISTENT (all identical form) |

**No conflicting file:line citation for any shared symbol.** Where two files cite the same symbol, the line numbers match exactly or one is a sub-range of the other (e.g. R1 `models.py:96` ⊂ R2 `models.py:95-98`; R3 §5.3 `390-391` = R6 `390/391`). The few single-source rows are owned cleanly by the file whose scope covers them (no other file makes a competing claim).

---

## Version-constant inconsistency — REPORTED CONSISTENTLY (a real defect all three flag the same way)

This is a CODE defect (not a research contradiction), and the three files that touch it agree on the facts AND the disposition:

- R2 §4 / §7: `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (ensemble.py:59, emitted @501) is "stale vs the SKILL-declared `1.6.0`"; flag as a defect; "likely no version bump (OQ-DRS.3)" but the `1.0` vs `1.6.0` Tier-2-path disagreement is a separate real defect.
- R6 §3.2: ensemble.py:59 `"1.0"` is "Two minor generations behind the skill's `1.6.0`"; "This is a CODE change in ensemble.py, NOT a SKILL change … keep this OUT of the Phase-4 SKILL item."
- R7 §Stale Documentation: ensemble.py:59 `"1.0"` "is stale vs the SKILL-declared `1.6.0` (TDD §8.3) — a producer-side reconcile item, not a test item."

All three: same line (59), same stale value ("1.0"), same target (1.6.0), same disposition (reconcile in product-path/code phase, NOT the SKILL phase; no contract_version bump for the six additive fields). **No contradiction — convergent.**

**One subtle alignment to flag for the builder (Minor):** R6 §3.2 resolves OQ-DRS.3 as "**no bump** — stays 1.6.0" for the §9.1 `contract_version`. R2 §4 phrases it as "OQ-DRS.3: likely no version bump." These agree (no bump), but R6 is more definitive. The ensemble.py:59 `"1.0"` reconcile is orthogonal to the §9.1 `1.6.0` no-bump decision — all files keep these two separate correctly. No action beyond noting both belong to the product/code phase.

---

## Checklist Results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cross-file consistency — same files/symbols agree | PASS | Seams 1-5 + shared-symbol table all CONSISTENT |
| 2 | No contradictory claims between files | PASS | Zero contradictions. R2↔R1 arg-gap is a refinement/correction of a relayed TDD assumption, not a research contradiction |
| 3 | Shared deps (run_sweep, contract.py slugs, _bfs_reachable) documented consistently | PASS | run_sweep signature byte-matches R1/R2; `degraded-components`/`regression` slug reuse agrees R3/R5; `_bfs_reachable` R1-names/R4-pins consistently |
| 4 | Integration-point descriptions match across researchers | PASS | `_audit_once` @394-453, merge @444→445, `parse_contract` @445 identical across R1/R2/R3; SKILL §5.3 lines identical R3/R6 |

---

## Seam-alignment notes for the builder (all Minor — no FAIL)

These are NOT contradictions; they are places where the builder must pick the authoritative rendering. Each has a clear owner per the files' own scope boundaries:

1. **rootwalk signature (R1 vs R4 skeleton).** Use R1's authoritative `rootwalk_entrypoints(surface, roots) -> RootwalkResult`; R4's `rootwalk_depth1(...)->Literal[...]` is provenance-illustrative only. (Seam 1)
2. **`surface_unreached` derivation home (R2/R3 straddle).** R3 designates `runner._audit_once` merge point as RECOMMENDED owner, `derive_verdict` as FALLBACK. R2 owns the merge mechanism there. Builder writes ONE item at the merge point; both files agree. (Seam 2)
3. **3 run_sweep arg gaps (R1 design vs R2 source-truth).** Take R2's [CODE-VERIFIED] reality: `diff` = compute `git diff config.base`; `scope_worktree` = derive/add field; `availability_surface` = add probe or floor-forcing empty dict. The TDD's "already on the config" is wrong for these three. (Seam 3)
4. **ensemble.py:59 `"1.0"` reconcile (R2/R6/R7 agree).** Code-phase item, NOT the Phase-4 SKILL item; no §9.1 contract_version bump. (Version cross-check)
5. **§15.4a derivation-test home (R7 self-flagged, depends on R3).** R7 defaults to `test_runtime_surface.py`; coordinate with R3's derivation owner. Already cross-referenced consistently. (Seam 5 adjacent)

---

## VERDICT: PASS

Partition P1 (files 01-04 primary; 05-07 seam-read) shows **zero cross-file contradictions** and **zero conflicting file:line citations** for any shared symbol. The five anchored seams (R1↔R4 rootwalk, R2↔R3 derivation owner, R1↔R2 run_sweep args, R2↔R3 merge point, R3↔R6 demotion split) are all CONSISTENT. The single most valuable cross-validation is R2 independently CODE-VERIFYING and correcting an unverified TDD config-sourcing assumption that R1 faithfully relayed (3 of 6 `run_sweep` args have no backing config field) — this is the research set working as intended (design file + source-truth file converging), not a defect in either file.

**Gap list (FAIL items):** NONE. No critical, important, or blocking cross-file gaps found in the P1 scope.

**Minor seam-alignment notes (5, listed above):** advisory only — each names the authoritative rendering and is already cross-referenced consistently between the owning files. They do not block synthesis.

> PARTITION SCOPE LIMIT: This report covers cross-file consistency anchored on P1 (01-04) with seam-reads into 05-07. It does NOT cover: file 08 (MDTM template) consistency, any P2-internal seams not touching 01-04, or full N-way contradiction sweep across the P2-owned file set. Merge with the P2 partition report for complete cross-file coverage.
