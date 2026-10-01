# Analyst Cross-Validation Report — FR-RSR (UC-2 Reachability)

**Analysis type:** completeness-verification
**Lens:** cross-validation (research files ↔ authoritative TDD/spec ↔ codebase ground truth)
**Date:** 2026-06-20
**Track goal:** Build an MDTM Template-02 tasklist implementing FR-RSR per the authoritative TDD
**Authoritative source:** `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md` (spec secondary)

**Assigned files:**
- 01-skill-gather-gate-anchors.md
- 02-skill-contract-classify-failopen-anchors.md
- 03-refs-inventory.md
- 04-eval-grader-inventory.md
- 05-template-and-examples.md

---

## Method

Read all 5 assigned research files in full. Read the authoritative TDD (`tdd.md`, 1080 lines, both pages) and cross-checked the secondary spec (`spec.md`). Spot-checked 8+ load-bearing SKILL.md anchors directly against `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1854 lines, `wc -l` verified) and the three-section lines of `refs/reviewer-spec.md`. Inventoried the live `.dev/eval-workspaces/sc-reflect/` tree for the directory-layout ground truth. No web research (none authorized, none needed — all evidence is on-disk).

---

## 1. Re-anchored SKILL.md line numbers — spot-check of load-bearing anchors

Every anchor the research files re-anchored was opened and verified against the CURRENT 1854-line `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. All confirmed EXACT — zero drift, zero conflicting anchors between research files.

| Anchor (claim in research) | Research file(s) | Verified line | Match |
|---|---|---|---|
| §5.3 header "Decision logic (applied in order; first match wins)" | R1 site1 (386) | 386 | EXACT |
| §5.3 row 1 confident-PASS STOP (`C ≥ 0.90 … NOT coverage_degraded`) | R1 (390) | 390 | EXACT |
| §5.3 forbid-STOP pre-filter ¶ "Pre-filter precedence (D13)" naming STOP rows "1, 2, or the row-8 default" | R1 site2 (402); TDD D6 (402) | 402 | EXACT |
| §6.1 step 4 `find_referencing_symbols <symbol> include_info:true` | R1 site4 (463); TDD D3 (463) | 463 | EXACT (`# downstream impact + signatures`) |
| §6.1 step 4a `Task(reuse-auditor …)` (insertion gap is 463→464) | R1 (464) | 464 | EXACT |
| §9.1 `contract_version: "1.5.0"` field+changelog comment | R2 site1 (663) | 663 | EXACT |
| §9.1 contract-version prose "Contract version is `v1.5.0`." | R2 (804) | 804 | EXACT |
| §17.7 kill-list invariant test `contract_version == "1.5.0"` | R2 (1772) | 1772 | EXACT |
| §10.8 Reuse-Miss header / end / `---` terminator | R2 site4 (1014 / 1025 / 1027) | 1014, 1025, 1027 | EXACT |
| §17.7 item 6 "5th `unknown` deviation category…Rejected" | R2 site5 (1799) | 1799 | EXACT |
| §9.3 executor.py TurnLedger row | R2 site2 (858) | 858 | EXACT |
| §9.3 sc-task-protocol escalate row | R2 site2 (859) | 859 | EXACT |
| reviewer-spec.md "exactly three sections" invariant sentence | R3 (23) | 23 | EXACT |
| reviewer-spec.md three section HEADINGS | R3 (25/31/49) | 25, 31, 49 | EXACT |
| reviewer-spec.md FR-4 verify-log routing exemplar | R3 (43) | 43 | EXACT |
| reviewer-spec.md FR-RV3-MED.1 / D13 reassertion entries | R3 (45 / 47) | 45, 47 | EXACT |

**Surrounding-content match:** For every sampled anchor the surrounding prose matches the research's description of where the new content lands:
- §5.3:402 pre-filter ¶ verbatim names the user-override carve-out (`--tier 1`, `--depth quick`, `--no-escalate`) exactly as R1 site2 and TDD §8.2 describe. `surface_unreached` joins as a third table-wide pre-filter. CONSISTENT.
- §6.1:463 is `include_info:true` already present (FR-3 param-add), §6.1:464 is the existing `4a` reuse-auditor sub-step — confirming R1's "new 4b'/4b slot AFTER 463 and must coexist with the existing 4a" claim. No conflicting anchor.
- §10.8 ends at 1025; 1026 blank; 1027 `---`; 1029 `## 11` — so new §10.9 lands strictly between 1025 and 1027 (R2 site4 + TDD §18.2). CONSISTENT.
- §9.1 UC-2 block: `verification_regressions_detected: <int>   # FR-4` is at 708 and the `deviation_count_by_class.regression` sub-key is in the 689–705 region; the `# Reuse-Miss neighbour sweep` banner is present — confirming R2's FR-RSR.7 6-field append point (end of UC-2 block, ahead of the Reuse-Miss banner). CONSISTENT.

**No conflicting/divergent anchors across the five files.** R1↔R2 agree on every shared §5.3/§6.1/§9.x line. R2 (SKILL.md §10/§17.7) ↔ R3 (`refs/deviation-taxonomy.md`) agree on the "4 classes, not 5 / finding-modifier / route to grounding-gaps" framing. The OLD→NEW deltas the research applied (TDD "~1850 lines" → verified 1854; TDD "around step 4" → verified 463) are internally consistent and surrounding content matches.

### 1a. OLD→NEW delta consistency (TDD vs verified)

The TDD cites anchors at a slightly older revision ("~1850 lines"). Every TDD-cited anchor I sampled (386, 390, 402, 463, 858, 877, 1014, 1700, 1799, and the `"1.5.0"` site) resolves to the SAME line in the current file — i.e. the file has not drifted at the sampled sites. The research's re-anchoring is a no-op-confirmation rather than a correction there, which R1 correctly reports (summary callout 5: "No line-number drift detected"). Note that TDD §2.2 still cites two anchors at slightly older numbers (`§10.3 Drift SKILL.md:937`, `§10.4 Regression SKILL.md:952`); R2 site? and R3 §2 independently re-anchor Drift/Regression — R3 places them in `refs/deviation-taxonomy.md` (lines 56/72) and R2 places the SKILL.md §10.3/§10.4 headers at 937/952. I did not separately open SKILL.md:937/952 in this pass; R2's 937/952 match the TDD's own numbers, so there is no inter-file conflict to resolve (both cite 937/952). [LIMIT: SKILL.md:937/952 not independently re-opened in this report — but no contradiction exists between the sources, so this is not a blocking gap.]

---

## 2. Eval directory-layout discrepancy — GROUND TRUTH (cross-validation point 2)

**This is the single most important cross-validation finding. R4 is CORRECT; the authoritative TDD §15.2/§18.2 AND the spec §4.1/§4.7 are BOTH WRONG on the directory path. Codebase is source of truth.**

### Ground truth (verified by `ls` on the live tree)

```
.dev/eval-workspaces/sc-reflect/
├── evals/
│   └── evals.json          ← the ONLY file in evals/ (no subdirectories)
├── cases/                  ← ALL case dirs live here (falsifier-suite, post-*, pre-*, serena-*, promotion)
├── grader.py
├── skill-snapshot/
└── …
```

- `ls .dev/eval-workspaces/sc-reflect/evals/` → only `evals.json`. **No `evals/uc2-*` directory exists or could exist by convention.**
- `ls -d …/evals/uc2-*` → "No such file or directory" (exit 2).
- `ls -d …/cases/uc2-*` → "No such file or directory" (exit 2) — correctly absent; these are the NEW dirs to be created.
- Every existing `case_dir` value in `evals.json` is `"cases/<name>/"` (verified: `cases/pre-trivial-coverage-gap/`, `cases/post-small-diff-clean/`, `cases/post-large-diff-mixed/`, `cases/serena-wave0-config/`, …). Entry count = 36 (verified `grep -c '"id":'`), so new ids 37–41 are correct.

### Verdict on the discrepancy

| Source | What it says | Correct? |
|---|---|---|
| **Codebase (ground truth)** | cases in `cases/uc2-*/`; `evals/` holds only `evals.json`; register via `case_dir: "cases/uc2-<name>/"` | — (authoritative) |
| **R4 (04-...)** | "case dirs live under `cases/`, NOT `evals/`… NO `evals/uc2-*` convention… cases go in `cases/uc2-*`" | **CORRECT** |
| **TDD §15.2** (761) | column header "Case (dir under `evals/`)" | **WRONG** |
| **TDD §18.2** (823–827) | new files at `…/evals/uc2-*/` | **WRONG** |
| **Spec §4.1** (552–556) + **§4.7** (707–711) | `…/evals/uc2-*/` | **WRONG** |

**The builder MUST follow R4 / the codebase: create `cases/uc2-<name>/` and register each (ids 37–41) with `case_dir: "cases/uc2-<name>/"` in `evals/evals.json`. Do NOT create `evals/uc2-*/` — that path is not in the convention and the runner would not discover it.**

### One precision correction to R4's framing (minor, non-blocking)

R4 §0 attributes the error to "that phrasing in the task brief is incorrect." That under-attributes it: the `evals/uc2-*` path originates in BOTH authoritative documents (TDD §15.2/§18.2 and spec §4.1/§4.7), not merely the brief. The builder's Execution Context / Key Constraints should record this as a known doc-vs-codebase override: **"TDD §18.2 / spec §4.1 `evals/uc2-*` is a known doc error; codebase convention is `cases/uc2-*` — follow the codebase."** This makes the override explicit and auditable so a future reader does not "fix" the tasklist back to the doc path. R4's placement decision is correct; only its attribution of the error source is incomplete.

---

## 3. Data-model count semantics — edge vs symbol (cross-validation point 3)

**AGREEMENT across TDD §7.1, spec §4.5, and the research. No residual edge-vs-symbol contradiction in the CURRENT documents.**

| Field | TDD §7.1 | Spec §4.5 (CURRENT) | Research | Agree? |
|---|---|---|---|---|
| `runtime_surface_unreached` counts… | **SYMBOLS** (reduced verdict), "never edges" (tdd.md:444, 468–480) | "count of UNREACHED **symbols** (reduced per-symbol verdict, NOT edges)" (spec.md:613, 298–301) | R4 §6 id41: "counts SYMBOLS"; R2 site1: lists it as a symbol-count field | YES |
| `runtime_surface_degraded` | true when ≥1 SYMBOL reduced to DEGRADE (tdd.md:445) | "true when ≥1 symbol reduced to DEGRADE" (spec.md:614) | R4 id39 asserts it as a boolean flag | YES |
| `len(unreached_surfaces) == runtime_surface_unreached` invariant | asserted (tdd.md:478, §4.1 success-metric) | asserted (spec.md:299, 312–313) | R4 id41 calls it out as the count-invariant eval; FLAGS the grader can't compute `len(list)==scalar` with `parse_yaml_simple` | YES |
| `requirement_id` type (UnreachedSurface + LedgerRow) | `str \| None` (tdd.md:449, 461) | `str \| None` both TypedDicts (spec.md:618, 633) | R2 site1 lists `runtime_surface_*`; R4 notes `requirement_id` nullable | YES |

**Resolution of the historical contradiction.** The TDD §7.1 "Spec-override annotations" block (tdd.md:482–489) states the spec's §4.5 **code-comment** originally said "edges" and `requirement_id: str`, and that "the spec was updated to match in the same remediation pass, so spec and TDD now agree." I VERIFIED this claim directly: spec.md:613 now reads "**symbols** … NOT edges" and spec.md:618/633 now read `str | None`. **The TDD's claim is TRUE — the spec has been remediated; no residual edge-vs-symbol or `str`-vs-`str|None` contradiction exists in the current files.** The reduction precedence `DEGRADE > UNREACHED > REACHED` (tdd.md:473) is consistently stated in both docs and in the TDD glossary (tdd.md:1071).

**No flag.** The research correctly carries the resolved (symbol) semantics. The one actionable item the research surfaces (R4 id41) is real and downstream-correct: because `grader.py`'s `parse_yaml_simple` reads only flat top-level scalars (verified in R4 §3d against grader.py:58 logic), the `len(unreached_surfaces) == runtime_surface_unreached` invariant CANNOT be asserted directly by an existing checker over a list — the skill must emit a precomputed scalar pair, or a new grader type is needed. This is a builder design decision the tasklist must make explicit (it is already flagged by R4 and is consistent with the TDD's `yaml_field`-based acceptance criterion at tdd.md:262/771, which implicitly assumes a scalar comparison).

---

## 4. Regression-counter hygiene + TurnLedger-rollback consumer anchor (cross-validation point 4)

**CONSISTENT across TDD, spec, research, and the verified SKILL.md anchor. Two distinct fields are correctly kept separate, and the rollback-consumer anchor is correctly disambiguated.**

### 4a. Counter hygiene: increment ONLY `deviation_count_by_class.regression`, NEVER `verification_regressions_detected`

| Source | Statement | Consistent? |
|---|---|---|
| TDD D8 (tdd.md:419) | "Increment **ONLY** `deviation_count_by_class.regression`. `verification_regressions_detected` is exit-code-sourced (§10.4 / step 5.5, SKILL.md:708,959)… conflating them corrupts the verified-regression count." | — |
| TDD §8.4 (558), §11.1 (614), Release Crit (997), NG4 (236) | repeatedly: `verification_regressions_detected` "explicitly NOT touched / UNCHANGED (evidence-sourced, not exit-sourced)" | YES |
| Spec (spec.md:142, 213, 416, 433, 468) | "Increment ONLY `deviation_count_by_class.regression`; … `verification_regressions_detected` is exit-code-sourced … never incremented by a reachability finding" | YES |
| Research R2 site1/Summary | confirms `verification_regressions_detected: <int> # FR-4` lives in the existing UC-2 block at SKILL.md:708 and is exit-code-sourced (step 5.5 / §10.4 at :959); the new `runtime_surface_*` fields are a SEPARATE additive cluster | YES |
| **Verified anchor** | SKILL.md:708 `verification_regressions_detected: <int>   # FR-4 (taxonomy-classified Regression exits on a claimed-passing file)` — confirms it is the exit-code-sourced field, distinct from `deviation_count_by_class.regression` (the sub-key in the 689–705 region) | CONFIRMED |

The distinction is load-bearing and is consistently described everywhere. No file conflates the two. **No flag.**

### 4b. TurnLedger-rollback consumer anchor — the executor.py §9.3 row

This is where the research **corrects the TDD**, and the correction is itself internally consistent and VERIFIED.

- **TDD phrasing (the imprecision):** TDD §6.3 (tdd.md:405) and §6.4 D12 (tdd.md:423) say the sprint consumer "reads `deviation_count_by_class.regression` … and triggers TurnLedger rollback (§9.3, SKILL.md:858)."
- **R2's correction (02-...:33, 110):** the §9.3 executor.py TurnLedger **rollback** row at SKILL.md:858 is actually keyed on `per_task_verdicts[].deviation_class == regression`, NOT on the top-level `deviation_count_by_class.regression`. The top-level `deviation_count_by_class.regression > 0` key drives a DIFFERENT consumer — the `sc-task-protocol` end-of-task hook at SKILL.md:859 ("escalate to troubleshoot"). The TDD "conflates two distinct rows."
- **VERIFIED against SKILL.md:** I opened lines 858–859 directly.
  - :858 (executor.py TurnLedger): load-bearing fields `… per_task_verdicts[].deviation_class …`; routing "`deviation_class == regression` triggers TurnLedger rollback". ✔ R2 is correct — the rollback trigger is `per_task_verdicts[].deviation_class`.
  - :859 (sc-task-protocol end-of-task hook): "`deviation_count_by_class.regression > 0` → escalate to troubleshoot". ✔ R2 is correct — the top-level count drives escalation, NOT rollback.

**Assessment:** R2's correction is accurate and well-evidenced. However, note a subtlety the builder must preserve: the by-evidence §10.9 mapping (FR-RSR.6) increments `deviation_count_by_class.regression` (the top-level count). The rollback row (:858) keys on `per_task_verdicts[].deviation_class`. For the TDD's stated rollback-coupling (D12) to actually fire, the UNREACHED-contradiction Regression must surface in BOTH the top-level count AND the relevant `per_task_verdicts[]` entry's `deviation_class`. The TDD/spec narrative treats "increment regression → rollback" as a single step; mechanically it spans the two §9.3 rows. **This is not a contradiction in the research (R2 flags exactly this two-row split) but it IS a precision the tasklist should carry forward** so the builder writes the §9.3 advisory row and the §10.9 modifier without re-introducing the TDD's "single field triggers rollback" shorthand. R2 already states the corrected mechanics; the builder must use R2's version, not the TDD's shorthand.

- TDD D12 (tdd.md:423) and OQ-RSR.5 (tdd.md:944) consistently ACCEPT the rollback coupling as intentional; R2 site2 and the research summary carry that forward. CONSISTENT.

**No blocking flag.** The research's disambiguation is correct and verified; the only action is "builder uses R2's two-row mechanics, not the TDD's one-row shorthand," which R2 already supplies.

---

## 5. Other internal-consistency checks across the five files

| Check | Finding | Status |
|---|---|---|
| SKILL.md total line count | R1 says 1854 (`wc -l`), R2 says 1854. Verified 1854. | CONSISTENT |
| contract bump 1.5.0 → 1.6.0, THREE sites move in lockstep (663/804/1772) | R2 site1 lists all three; verified all three currently read "1.5.0". §9.4 minor-bump rule at SKILL.md:877 (R2 site3) governs. | CONSISTENT |
| §10.9 is a finding-modifier (NOT a 5th class), mirrors §10.8 | R2 site4 (SKILL.md §10.8 at 1014) + R3 §2 (`refs/deviation-taxonomy.md` "4 categories, not 5" at lines 5/117) + TDD D7 (tdd.md:418) all agree; §17.7 item 6 (1799) is the binding rejection. | CONSISTENT |
| reviewer-spec.md "three-section invariant at lines 23,43,45,47" (TDD §27.1 tdd.md:1047) | R3 CORRECTS this: line 23 = invariant sentence; 25/31/49 = the actual section HEADINGS; 43/45/47 = the FR-4/FR-RV3-MED.1/D13 reassertion-exemplar entries. VERIFIED: 23 is the invariant, 25/31/49 are `## T1 card excerpt`/`## Grounding hunks`/`## Coverage slice`, 43 is the FR-4 verify-log entry. R3 is correct; the TDD's "23,43,45,47" is imprecise. | R3 CORRECTLY FLAGS; builder uses 25/31/49 + insert FR-RSR.9 between 47 and 49 |
| fail-open policy §6.5 (SKILL.md:563–565) inherited by FR-RSR.8 | R1 site6 + R2 site6/7 (degraded_components slug `runtime-surface:backend_unavailable` at SKILL.md:815) + TDD §12.3 (tdd.md:664) agree. | CONSISTENT |
| "reflect AUTHORS, never runs /task" (NG5) | R2 site8 (SKILL.md:1700/1705) + TDD NG5 (tdd.md:237–238) + R5 (POST reflect gate uses `superclaude reflect run`, never `/sc:task`) agree. | CONSISTENT |
| grader assertion types the eval FR uses | R3 §4 (grader-extensions.md: `regex_absent`/`falsifier_skeleton_present` DEFINED; `yaml_field`/`yaml_field_min` BASELINE-inherited) ↔ R4 §3 (grader.py: `regex_absent` def line 162, `yaml_field` inline 336, `yaml_field_min` inline 348, key is `min_value` not `value`/`threshold`). The two views are about DIFFERENT files (the ref that specifies vs the code that implements) and are mutually consistent. TDD §15.1 (tdd.md:754–755) cites grader.py:162/152/336/270/405 — consistent with R4's line numbers. | CONSISTENT |
| Headline eval is dual-snapshot (FAIL-pre via `old_skill/`, PASS-post via `with_skill/`); `skill-snapshot/reflect-v1.md` is the fail-before baseline | R4 §0/§4 (target-prefix partition in grade_eval) + TDD §15.3 (tdd.md:776–778). | CONSISTENT |
| MDTM Template 02 conformance surface (R5) is independent of FR-RSR content | R5 documents template/example rules; no overlap or conflict with R1–R4's domain claims. | CONSISTENT (orthogonal) |

**No contradictions found between the five research files.** Every place two files touch the same component, they agree (and where they refine a TDD imprecision — R2 on the §9.3 rollback row, R3 on the reviewer-spec three-section lines, R4 on the eval directory — all three refinements are VERIFIED correct against the codebase).

---

## 6. Compiled gaps / actions for the builder

### Critical (must be encoded as explicit overrides in the tasklist)
1. **Eval directory path:** create `cases/uc2-<name>/` (NOT `evals/uc2-*/`); register with `case_dir: "cases/uc2-<name>/"` ids 37–41 in `evals/evals.json`. The TDD §18.2 / spec §4.1 `evals/uc2-*` path is a verified doc error — codebase wins. (§2 above.)

### Important (precision the tasklist must carry, not TDD shorthand)
2. **TurnLedger rollback mechanics:** use R2's two-row split — `per_task_verdicts[].deviation_class == regression` triggers the executor.py rollback (SKILL.md:858); `deviation_count_by_class.regression > 0` drives the sc-task-protocol escalate row (SKILL.md:859). Do NOT reproduce the TDD's "increment the count → rollback" one-row shorthand. (§4b.)
3. **reviewer-spec.md anchors:** three section headings are 25/31/49; insert the FR-RSR.9 grounding-hunk entry between line 47 (D13 exemplar) and line 49 (`## Coverage slice`), mirroring the FR-4 entry at line 43 — NOT a 4th `## ` section. The TDD §27.1 "23,43,45,47" is imprecise (those are the invariant + reassertion lines). (§5, R3.)
4. **Count-invariant eval mechanism:** `len(unreached_surfaces) == runtime_surface_unreached` cannot be asserted by `parse_yaml_simple`-backed checkers over a list; the tasklist must specify the chosen mechanism (precomputed scalar pair, or a new grader type). (§3, R4 id41.)
5. **contract bump lockstep:** the 1.5.0 → 1.6.0 bump must update ALL THREE sites together — SKILL.md:663 (field+changelog), :804 (prose), :1772 (kill-list invariant test). (§5, R2.)

### Minor
6. R4's attribution of the `evals/uc2-*` error to "the task brief" should be re-attributed to the TDD+spec in the Execution Context, so the override is auditable. (§2.)

### Limitations of this pass (disclosed)
- SKILL.md:937 (§10.3 Drift) and :952 (§10.4 Regression) headers were NOT independently re-opened. R2 and the TDD both cite 937/952, so there is no inter-source conflict to adjudicate; the builder should re-confirm these two anchors at edit time per standard freshness discipline, but they are not a cross-validation gap (no contradiction exists). 
- This is a single-instance (non-partitioned) analysis covering all 5 assigned files; cross-file checks are complete (no PARTITION NOTE needed).

---

## VERDICT: PASS

**Rationale.** The five research files are mutually consistent, individually well-evidenced (every load-bearing line anchor I spot-checked resolved EXACT against the current SKILL.md / refs / eval tree), and correctly grounded against the authoritative TDD with the codebase as tie-breaker. The three places the research diverges from the TDD/spec (eval directory `cases/` vs `evals/`; the §9.3 rollback two-row split; the reviewer-spec three-section line numbers) are all CORRECT codebase-grounded refinements of TDD imprecisions, not errors in the research — they are the research doing its job. The historical edge-vs-symbol and `requirement_id` type contradictions have been remediated in the spec (verified), so no residual data-model contradiction exists.

The verdict is PASS because the research is fit to drive the tasklist build, **conditioned on the builder encoding the six compiled actions above** — most critically action #1 (eval directory override), which is the one place blind adherence to the authoritative TDD would produce broken output. None of the six actions require re-research; all are already surfaced (with correct resolutions) inside the research files themselves. No contradictions between research files. No fabrication detected. No unverified doc-sourced claims passed through (the doc-vs-code discrepancies are all explicitly flagged and resolved to code).
