# QA Report — research-depth (FR-RSR UC-2 Reachability Escalation)

**Phase:** research-depth (custom lens)
**Date:** 2026-06-20
**Fix authorization:** false (report-only)
**Adversarial stance:** Assume research is superficial until proven otherwise.

**TRACK GOAL:** Build an MDTM Template-02 tasklist implementing FR-RSR — 6 surgical SKILL.md edits + 1 new ref + 2 ref edits + 5 eval cases + sync. Each item must be self-contained / actionable WITHOUT re-reading source.

**LENS FOCUS:** Is the research DEEP enough to produce per-item, self-contained checklist items?

---

## Status: COMPLETE

---

## Files assessed (depth, not just presence)

| File | Bytes | Verdict | Depth signal |
|------|-------|---------|--------------|
| 01-skill-gather-gate-anchors.md | 11.4K | DEEP | 7 sites, verbatim row text, **insertion GAP** (463→464), authoritative-gate WHY (:402 pre-filter ≠ row conjunct) |
| 02-skill-contract-classify-failopen.md | 14.6K | DEEP | 8 sites, 3-site contract_version lockstep, **catches a TDD conflation** (:858 rollback vs :859 escalate), exact §10.9 insertion window |
| 03-refs-inventory.md | 19.5K | DEEP | code-verified anchors; **corrects TDD's reviewer-spec claim** (23/43/45/47 → headings are 25/31/49); coverage-mapping "fact 3" proven by value-space-absence |
| 04-eval-grader-inventory.md | 23.5K | DEEP | end-to-end eval trace; verbatim id-2 template; grader signatures w/ exact keys (`min_value`≠`value`); **parse_yaml_simple flat-key HARD CONSTRAINT**; `with_skill/`/`old_skill/` partition; **corrects task brief's `evals/uc2-*` path error** |
| 05-template-and-examples.md | 33.3K | DEEP | full Template-02 PART1/PART2 rule surface + real TASK-RF example cross-validated (M3/I19/I20, POST-reflect penultimate ordering) |

## Independent source verification (adversarial — anchors must be byte-accurate for self-contained items)

Verified a representative cross-section of the most load-bearing cited anchors against ACTUAL source (not the research's own claims):

- **SKILL.md (1854 lines, confirmed `wc -l`):** :386 §5.3 header ✓; :390 row-1 verbatim ✓; :402 pre-filter precedence paragraph verbatim ✓ (names STOP rows "1, 2, or the row-8 default" ✓); :463 step-4 `find_referencing_symbols` ✓; :464 step-4a reuse-auditor ✓ (insertion gap real); contract_version `"1.5.0"` at :663/:804/:1772 all ✓ (3-site lockstep real); §10.8 ends :1025, `---` at :1027, §11 at :1029 ✓ (§10.9 window real); :1799 kill-list item 6 ✓; **:858 TurnLedger rollback keyed on `per_task_verdicts[].deviation_class == regression` vs :859 escalate on `deviation_count_by_class.regression` ✓ — the conflation correction is CORRECT**; :1705 Will-Not-run-/task invariant ✓; UC-2 region :689 / verification fields :705/:708 / reuse banner :711 ✓.
- **reviewer-spec.md:** :23 invariant sentence ✓; :25/:31 headings ✓; :43/:45/:47 are the FR-4/FR-RV3-MED.1/D13 **reassertion entries, NOT headings** ✓ — the R3 correction of the TDD is CORRECT and exactly anchored.
- **deviation-taxonomy.md:** :5 + :117 "4 categories" ✓; :62 unmapped ✓; :119 grounding-gaps routing ✓.
- **grader.py:** `check_regex_absent` def :162 ✓; `yaml_field` inline dispatch :336 ✓; `yaml_field_min` :348 ✓ (key `min_value`); `check_falsifier_skeleton_present` :270 ✓; `parse_yaml_simple` def :58 + **indented-line skip at :71 `startswith(" ")` ✓ — the flat-key constraint is REAL**; `with_skill/`/`old_skill/` prefix partition :422-423 ✓.
- **evals.json:** 36 entries (`grep -c '"id":'` = 36 → next ids 37-41 correct ✓); id-2 entry structure ✓.
- **cases/:** `post-small-diff-clean/{input/{diff.patch,tasklist.md},expected.yaml}` layout ✓; falsifier skeletons carry `status: skeleton-pending-iteration-3-fixture` ✓.
- **skill-snapshot/reflect-v1.md:** 111 lines ✓; `grep -c runtime_surface|reachability|UC-2` = 0 ✓ (fail-before baseline real).
- **TDD + spec exist** (.dev/reflect-hardening/issue-1-uc2-reachability/{tdd.md 69.8K, spec.md 59.7K, BUILD-REQUEST.md}); TDD carries the degrade-oracle / lang→(test-marker,comment-syntax) table / rootwalk / tagger CONTENT (§6.4 D1-D4, §7.1, §1 invariants) the research correctly defers to for T1/runtime-surface.md authoring.

**Zero anchor drift found across the entire verified sample.** Every line number, every verbatim quote, every count matched current source. This is the property that makes per-item self-contained Context blocks possible without re-reading source.

---

## Lens questions — direct answers

**Q1 — Do the files explain HOW/WHY the modification sites work, not just WHERE?** YES, deeply.
- WHY §5.3 needs a TABLE-WIDE pre-filter not a row: file 01 Site 2 + the verified :402 paragraph establish the pre-filter is *authoritative* and row conjuncts are "redundant safeties" — so FR-RSR.5 must amend :402 (the gate), with optional redundant `NOT surface_unreached` conjuncts on rows 1/2. The builder can write "amend the pre-filter paragraph, not just a row" with citation.
- HOW the §6.1 sweep reuses the already-fetched referrer set: file 01 Site 4 pins step-4 `find_referencing_symbols include_info:true` at :463 (the "fetched-and-discarded" referrer set), insertion gap 463→464, must coexist with existing 4a. The §4 audit.log per-step row convention captured. This is HOW, anchored.
- WHY contract_version changes at 3 sites: file 02 Site 1 names :663 (field+changelog), :804 (prose), :1772 (kill-list invariant test) and states they "must move together" — verified all three exist. §9.4 minor-bump clause (:877) + read-and-ignore forward-compat (:895) give the WHY it's safe.

**Q2 — Is the eval mechanism traced end-to-end?** YES — file 04 is the strongest file. Registration (verbatim id-2 template + key list) → fixtures (case_dir layout, expected.yaml-is-oracle-not-target gotcha) → grader assertion keys (exact per-type key sets; `min_value` not `value`/`threshold`) → FAIL-pre/PASS-post partition (`with_skill/`/`old_skill/` prefix at grade_eval :422-423 + reflect-v1.md baseline). The builder can write each of the 5 per-case items WITHOUT re-reading grader.py. It additionally surfaces a REAL gap (id-41 `len(unreached)==count` invariant is inexpressible by existing checkers) and gives the builder concrete options — exactly the depth that prevents a broken eval item.

**Q3 — Are the two load-bearing invariants + counter hygiene reflected with enough specificity to write verification clauses?** YES.
- Symbol-anchored tagger: research-notes §"Two load-bearing invariants" (1) + TDD §1 invariant 1 (verified present) — `requirement_id` nullable, keys off Wave-1A resolved symbol kind.
- Degrade-default-to-Grounding-Gap: file 02 Site 4/6 + file 03 §2 (§10.9 routes to grounding-gaps, NOT a 5th class) + TDD §1 invariant 2 (verified). The §10.6 Grounding Gap target and §17.7-item-6 "no 5th class/counter" constraint are both anchored.
- Counter hygiene: research-notes D8 + file 02 Site 2 — increment ONLY `deviation_count_by_class.regression`, NEVER `verification_regressions_detected` (exit-code-sourced at :959, verified mechanic). The :858/:859 disambiguation gives the builder the exact field a verification clause must (and must not) assert.

**Q4 — Could the builder write T1 (runtime-surface.md), T2 (sweep), and T9 (evals) WITHOUT re-reading source?** YES for all three.
- **T1 runtime-surface.md authoring:** content comes from TDD §6.4 D1-D4 + §7.1 (degrade-oracle/lang-table/rootwalk — verified present in TDD); placement/house-style from file 03 (refs conventions, the "exactly three sections" sibling discipline) + file 02 contract anchors. Self-contained.
- **T2 sweep item:** file 01 Site 4 (insertion gap, step numbering 4b'/4b coexisting with 4a, audit.log row) + Site 6 (§6.5 fail-open inheritance, gate the pre-filter on a SUCCESSFUL sweep) + TDD §6 flow diagram. Self-contained.
- **T9 eval items:** file 04 §6 gives per-case fixtures + assertions + ids; the only residual is the id-41 invariant mechanism, which is FLAGGED with options (not left silent). Self-contained.

**Where is it thin?** Two minor, non-blocking soft spots (below). Neither prevents a self-contained item; both are already flagged by the research itself.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (for builder, not research) |
|---|----------|----------|-------|------------------------------------------|
| 1 | MINOR | file 04 §6 id-37/40, §2 GOTCHA | The exact emitted-YAML filename + top-level-vs-nested placement for the new `runtime_surface_*` fields is stated as **presumed** `with_skill/outputs/contract.yaml`, deferred to "R1/R2 confirm". R1/R2 (files 01/02) anchor the §9.1 CONTRACT fields but do not pin the runtime ARTIFACT emission filename/path the grader asserts against. Because `parse_yaml_simple` only reads flat top-level keys, an eval item that asserts `yaml_field runtime_surface_unreached` against the wrong file or a nested key silently FAILs. | Builder: derive the emitted artifact path/shape from TDD §7.1 / §9 (return-contract.yaml vs contract.yaml) and pin it explicitly in each T9 assertion item's Context; do not leave "presumed". The research correctly flagged this — it is a builder action, not a research gap. |
| 2 | MINOR | file 04 §6 id-41 | The `len(unreached_surfaces) == runtime_surface_unreached` count invariant is **inexpressible by any existing grader checker** (parse_yaml_simple can't read list length; no checker computes len==scalar). Research gives two options but does not decide. | Builder: pick option (a) emit a precomputed scalar pair + two `yaml_field` asserts, OR (b) author an 11th grader type per grader-extensions.md template (file 03 §4 gives the exact `## <name>` + `check_<name>` + dispatcher-registration pattern). Decide in the T9/grader item, do not leave open. Adequately scoped by research. |

Both are correctly characterized by the research as builder-decisions with named resolution paths — they are NOT research-depth deficiencies (the research did its job by surfacing them with options rather than papering over them).

---

## Self-Audit

**(a) Reliance list — items where I relied on research claims and then independently re-verified:**
- Relied on file 01's SKILL.md anchors → re-Read :386/:390/:402/:463/:464 from source (all ✓).
- Relied on file 02's contract_version 3-site claim + :858/:859 conflation correction → re-Read all 4 lines (all ✓, conflation correction CONFIRMED).
- Relied on file 03's reviewer-spec correction (headings 25/31/49 not 43/45/47) → re-Read :23/:25/:31/:43/:45/:47/:49 (correction CONFIRMED).
- Relied on file 04's grader/evals claims → re-Read grader.py defs + parse_yaml_simple skip + grade_eval partition + counted evals.json ids + listed case dirs + checked snapshot (all ✓).

**(b) Independent semantic checks (≥1 required):**
- **Anchor-drift check:** grepped/sed'd ~40 distinct cited line anchors across 5 source files; found ZERO drift. This is the load-bearing semantic property for "self-contained items without re-reading source" — verified by tool, not asserted.
- **TDD-content-presence check for T1:** independently grepped TDD for degrade-oracle/lang-table/rootwalk/tagger content (the T1 source-of-record) — present at TDD §6.4/§7.1/§1, confirming T1 is authorable from TDD+research without source re-read.
- **Constraint-reality check:** confirmed the `parse_yaml_simple` flat-key constraint (grader.py:71) and the 36→37-41 id math are REAL, not paraphrase — these are the two facts most likely to break an eval item if wrong.

**Confidence:** Verified: 4/4 lens questions answered with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (research-depth lens).
**Tool engagement:** Read: 6 | Grep/sed (Bash): 6 multi-target verification batches (~40 distinct anchor checks) | Glob: 0.
**Web research:** none performed (lens is entirely local-source-bound; no external lookup required).

---

## VERDICT: PASS

The research is DEEP — not a surface inventory. Across all five files it explains HOW and WHY each modification site works (authoritative pre-filter vs redundant row conjuncts; fetched-and-discarded referrer set; 3-site contract lockstep), traces the eval mechanism end-to-end (registration → fixtures → grader keys → FAIL-pre/PASS-post partition), and reflects both load-bearing invariants + counter hygiene with field-level specificity. It independently **corrects two upstream errors** (the TDD's reviewer-spec line claim; the task brief's `evals/uc2-*` path) and **catches a TDD conflation** (:858 rollback vs :859 escalate) — markers of genuine depth, not box-checking. Every sampled anchor verified byte-accurate against current source with zero drift. The builder can author the T1, T2, and T9 items (and all six SKILL.md edits + 2 ref edits) from research + TDD WITHOUT re-reading source. The two MINOR soft spots are builder-decisions the research correctly surfaced with named resolution paths, not depth gaps.

Per the no-leniency rule, the two MINOR items are recorded as FINDINGS the builder must close during authoring (pin the emitted-YAML target path for the runtime fields; decide the id-41 count-invariant mechanism). They do not impugn the research's depth and do not block task-building.

## QA Complete
