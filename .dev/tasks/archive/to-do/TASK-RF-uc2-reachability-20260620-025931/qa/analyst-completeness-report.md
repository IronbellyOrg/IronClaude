# Research Completeness Verification — BREADTH Lens

**Topic:** FR-RSR (sc:reflect UC-2 runtime-surface reachability escalation) — task-builder track
**Lens:** BREADTH (modification-site coverage vs TDD §18.2 file inventory)
**Date:** 2026-06-20
**Files analyzed:** 01-skill-gather-gate-anchors.md, 02-skill-contract-classify-failopen-anchors.md, 03-refs-inventory.md, 04-eval-grader-inventory.md, 05-template-and-examples.md
**Depth tier:** Deep
**Analyst:** rf-analyst (no team context)

---

## Method

Ground truth = TDD §18.2 file inventory + the 7 explicit breadth checks in the spawn prompt.
For each modification site the TDD names, verify: (a) a research file covers it, AND (b) the
coverage carries a CURRENT verified line anchor (not merely the TDD's approximate number).
Adversarial stance: flag missing coverage and stale/unverified anchors, do not confirm.

---

## TDD §18.2 File-Inventory Coverage Matrix (BREADTH)

Ground truth = TDD §18.2 "Modified files" + "New files". Each row = a modification
site the TDD names; coverage = which research file documents it WITH a current anchor.

### Modified files

| §18.2 site | Research coverage | Current anchor verified? | Status |
|-----------|-------------------|--------------------------|--------|
| `SKILL.md` §6.1 steps 4b'/4b (extend step 4) | 01 Site 4 | YES — header :453, step 4 = :463, insertion gap 463→464, 4a coexistence noted | COVERED |
| `SKILL.md` §5.3 + pre-filter precedence ¶ (:402) | 01 Site 1 + Site 2 | YES — table header :386, rows 390/391/392/393/398, pre-filter ¶ :402 verbatim | COVERED |
| `SKILL.md` §5.4 `tier_decision.yaml` | 01 Site 3 | YES — header :404, coverage_degraded reason :411, sibling field placement | COVERED |
| `SKILL.md` §10 (new §10.9) | 02 Site 4 | YES — §10.8 mirror :1014, exact insertion between :1025 and `---` :1027 | COVERED |
| `SKILL.md` §9.1 stable contract (+6 fields, bump 1.5.0→1.6.0) | 02 Site 1 | YES — header :660, contract_version :663, UC-2 region :689, append point :709/:711 | COVERED (see Gap G1 on lockstep) |
| `SKILL.md` §9.3 Consumer Field Map (advisory row) | 02 Site 2 | YES — header :851, advisory template :862, field-deletion guard :868 | COVERED |
| `refs/reviewer-spec.md` (FR-RSR.9 grounding-hunk entry) | 03 §1 | YES — invariant :23, headings 25/31/49, FR-4 model :43, insert 47→49 | COVERED (corrects TDD's imprecise line cite) |
| `refs/deviation-taxonomy.md` (§10.9 xref) | 03 §2 | YES — 4-class :5/:117, insertion in Grounding-gaps :115–138 + Drift :56 | COVERED |
| `.dev/eval-workspaces/sc-reflect/grader.py` (regex_absent/yaml_field) | 04 §3 | YES — regex_absent def :162/dispatch :391, yaml_field :336, yaml_field_min :348, falsifier :270/:405 | COVERED |
| `cases/falsifier-suite/…` (keep 2 skeletons green) | 04 §5 | YES — T2-converges (id 19, :466), T2-judge-class (id 20, :482), dual-state README | COVERED |

### New files

| §18.2 site | Research coverage | Verified? | Status |
|-----------|-------------------|-----------|--------|
| `refs/runtime-surface.md` (NEW source-of-truth) | research-notes + 03/04 reference it; confirmed absent | YES — confirmed does NOT yet exist (T1 creates it) | COVERED (content sourced from TDD §6.4/§7.1 + spec, not a code anchor) |
| 5 eval cases `uc2-*` (+ fixtures) | 04 §6 (ids 37–41, per-case fixtures+assertions) | YES — id-2 template verbatim, dual-snapshot mechanism, per-case fixtures | COVERED (see Gap G2: path is `cases/uc2-*`, NOT `evals/uc2-*`) |
| `skill-snapshot/reflect-v1.md` (fail-before baseline) | 04 §4 | YES — 111 lines, 0 runtime_surface refs confirmed via grep | COVERED |
| `<output>/artifacts/runtime-surface-ledger.yaml` (runtime artifact) | 04 + TDD §7.1 schema | YES — RuntimeSurfaceLedgerRow schema captured | COVERED (runtime-only, never committed) |

**§18.2 verdict:** ALL 14 modification/new sites have research coverage with a verified
current anchor (or a documented justified-absence for the NEW source-of-truth files whose
content derives from TDD/spec rather than an existing code anchor). No missing site.

---

## The 7 Spawn-Prompt Breadth Checks

### Check 1 — Every SKILL.md edit site has a CURRENT verified line anchor: **PASS**
All six SKILL.md edit sites (§6.1, §5.3+¶402, §5.4, §10.9, §9.1, §9.3) carry verified
current anchors in files 01/02, independently re-captured against the live 1854-line file
(both researchers ran `wc -l` → 1854, matching research-notes). File 01 explicitly states
"No line-number drift detected between TDD approximate anchors and the verified CURRENT file
for the step-4 insertion site" and re-confirms step 4 = line 463 (TDD's "around step 4").
File 02 re-anchored every contract/classify/fail-open site. Plus bonus coverage of the
fail-open consumers (§6.5 :563/:565, §0.5d :242/:244–250/:261, degraded_components :815),
the §4 audit-log convention (:127), and the NG5 "Will Not run /task" invariant (:1705).

### Check 2 — §9.1 contract_version: ALL lockstep occurrences identified: **PASS (with a minor gap — G1)**
File 02 Site 1 identifies THREE authoritative lockstep sites that must move together on a
1.5.0→1.6.0 bump: `:663` (field + changelog comment), `:804` (prose "Contract version is
`v1.5.0`"), `:1772` (kill-list invariant test `contract_version == "1.5.0"`). I independently
verified all three via grep. This satisfies the check's core intent (a single-site bump would
be incomplete — caught). **Minor completeness gap (G1):** file 02 did NOT enumerate the
`skill_version` derivation references at `:1558` (`"skill_version": "<contract_version from
§9.1>"`) and the illustrative JSON example at `:1641` (`"skill_version": "1.5.0"`). The :1641
literal is an *example* output value (derived, not a source-of-truth declaration), so it is not
strictly an edit site — but it is a stale `1.5.0` literal that will mislead a reader post-bump
and the builder should be told whether to refresh the example. Rated a MINOR gap, not Critical,
because the three authoritative gating sites ARE captured.

### Check 3 — Eval registration mechanism (evals.json schema) + concrete case template: **PASS**
File 04 §1 captures the full `evals/evals.json` shape `{skill_name, iteration, scope, notes,
evals:[...]}`, the per-entry key set (`id, name, case_dir, mode, use_case, spec_ref,
description, inputs, expected, assertions`), the current entry count (36 → new ids 37–41),
the `case_dir` vs `case_file` distinction, AND a full verbatim template entry (id 2,
post-small-diff-clean, lines 39–80). The MAIN-case dir structural template (`input/diff.patch`
+ `input/tasklist.md` + `expected.yaml`) and the `expected.yaml` UC-2 shape are captured in §2.
Concrete and complete.

### Check 4 — reviewer-spec.md three-section invariant + exact FR-RSR.9 insertion point: **PASS (exemplary)**
File 03 §1 captures the invariant (:23), the three section headings (25/31/49), the
`## Grounding hunks` H2 (:31), the FR-4 verify-log routing pattern that FR-RSR.9 must mirror
(:43), two further sibling exemplars (:45 FR-RV3-MED.1, :47 D13), and the exact insertion
point: a bolded `**FR-RSR.9 …**` entry between line 47 and line 49, persona-filtered to qa.
It also CORRECTS the TDD's imprecise "lines 23, 43, 45, 47" claim (43/45/47 are reassertion
sentences, not headings; headings are 25/31/49) — an adversarial doc-cross-validation win.

### Check 5 — Grader assertion-key contracts (regex_absent, yaml_field, yaml_field_min) + count-invariant expressibility: **PASS**
File 04 §3 gives exact signatures and key sets: `regex_absent {target, pattern}` (def :162),
`yaml_field {target, field, expected}` (string ==, dispatch :336), `yaml_field_min {target,
field, min_value}` (numeric ≥, key is `min_value` NOT `value`, dispatch :348),
`falsifier_skeleton_present {case_yaml}` (def :270). CRITICAL constraint surfaced: the three
yaml_* checkers use `parse_yaml_simple` (def :58) which sees ONLY flat top-level non-indented
keys — so `runtime_surface_unreached`/`runtime_surface_degraded` MUST be emitted as top-level
scalars. The count-invariant question is EXPLICITLY answered (§6 id 41): `len(unreached_surfaces)
== runtime_surface_unreached` is NOT expressible by any existing checker (parse_yaml_simple
can't read list length); file 04 flags this to the builder with two concrete options (emit a
precomputed scalar pair, or author a new grader type). This is exactly the expressibility
assessment the check demanded.

### Check 6 — MDTM template rules (A3/B2/M3/I19/I20/anti-orphaning/POST-reflect): **PASS**
File 05 documents the full Template-02 rule surface from the LIVE template
(`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, confirming `.claude/
templates/` is empty per research-notes correction): A3 granular breakdown (:108–112), B2
6-field self-contained item (:159–165), M3 8-step lens sequence (:1059–1096), I19 agent-count
floors + intermediate-gate table (:699–743), I20 serialized fix (:745–757), anti-orphaning
Post-Completion ordering with POST reflect penultimate / Update-status terminal (:1423–1441),
plus a real complex TASK-RF example (reflect-post-gate-wiring) showing the POST reflect
`superclaude reflect run … --depth deep --fix --no-promote` shell-out behind the
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard. Anti-orphaning and POST-reflect both covered.

### Check 7 — Directory-layout discrepancy (evals/ vs cases/) surfaced: **PASS (critical catch)**
File 04 §0 and §2 surface the discrepancy unambiguously and I independently verified it:
`evals/` contains ONLY `evals.json`; all case dirs live under `cases/`. The TDD §18.2, the
research-notes EXISTING_FILES, AND the spawn prompt's own ASSIGNED-FILES framing ("evals/uc2-*")
all use the WRONG path. File 04 states verbatim: "case directories live under `cases/`, NOT
under `evals/`. … There is NO `evals/uc2-*` directory convention — that phrasing in the task
brief is incorrect; cases go in `cases/uc2-*`." Verified by `ls`: cases/ holds falsifier-suite,
post-large-diff-mixed, post-small-diff-clean, etc. This is the single most important breadth
catch — building the 5 new cases at the TDD's stated `evals/uc2-*` path would put them where the
runner does not look. Surfaced correctly.

---

## Cross-File Consistency (BREADTH within assigned subset)

- **File count (1854 lines):** 01 and 02 both independently confirm SKILL.md = 1854 lines
  (research-notes also says 1854; TDD said ~1850). Consistent.
- **§10.8 → §10.9 pattern:** 02 (SKILL.md :1014) and 03 (deviation-taxonomy.md "4 categories,
  not 5") agree the new modifier must mirror §10.8 / route to grounding-gaps, no 5th class.
  Consistent, mutually reinforcing.
- **contract_version 1.5.0:** 02 (SKILL.md) and 04 (skill-snapshot has 0 runtime_surface refs)
  are consistent on the additive-bump framing.
- **No contradictions found** across the five assigned files. Where the TDD is imprecise
  (reviewer-spec line cite; evals/ path), the research files CORRECT it rather than propagate it.

---

## Completeness of Each Research File

| File | Status | Summary | Gaps section | Key takeaways | Evidence anchors | Rating |
|------|--------|---------|--------------|---------------|------------------|--------|
| 01 | Complete | YES | implicit (per-site notes) | YES (5 callouts) | strong, every site line-anchored | Strong |
| 02 | Complete | YES | implicit (re-anchor deltas) | YES (summary deltas) | strong, every site line-anchored | Strong |
| 03 | Complete | YES | insertion-point analysis | YES (builder anchor table + top correction) | strong, CODE-VERIFIED tags | Strong |
| 04 | Complete | YES | GOTCHA + FLAG-TO-BUILDER callouts | YES (7-point load-bearing facts) | strong, grader line-anchored | Strong |
| 05 | Complete | YES | template-vs-example deltas noted | YES (6-rule conformance set) | strong, `02:`/`ex:` citations | Strong |

All five carry Status: Complete, a Summary, evidence anchors, and builder-facing takeaways.
Evidence quality is uniformly strong — every claim cites a file:line, and doc-sourced claims
(file 03) carry explicit `[CODE-VERIFIED]` tags.

---

## Compiled Gaps

### Critical Gaps (block task-building)
- **NONE.** Every TDD §18.2 site is covered with a verified current anchor. The most
  material risk (the `evals/` vs `cases/` path error) is SURFACED by the research, not missed —
  so the builder will place the 5 cases correctly if it heeds file 04 §0.

### Important Gaps (affect quality)
- **NONE that block.** The count-invariant expressibility gap (check 5) is a design decision
  the research correctly hands to the builder with options, not an unanswered hole.

### Minor Gaps (should still be addressed)
- **G1 — contract_version lockstep enumeration is 3 of ~4–5 literal sites.** File 02 names the
  three authoritative gating sites (:663, :804, :1772) but omits the derived `skill_version`
  references at `:1558` (`"<contract_version from §9.1>"` — self-updating, informational) and the
  stale literal `1.5.0` in the JSON example at `:1641`. The builder should be instructed to
  either refresh the :1641 example to 1.6.0 or note it as an illustrative-only value. Source:
  cross-check of file 02 Site 1 against live SKILL.md grep. Severity MINOR (the three gating
  sites are captured; :1641 is an example, not a gate).
- **G2 — path-naming carries into the spawn prompt and TDD.** Documented (not a research gap —
  file 04 caught it) but flagged here so the builder's per-item Output paths use `cases/uc2-*`,
  NOT the TDD §18.2 / spawn-prompt `evals/uc2-*`. The builder MUST override the TDD on this point
  (research-notes already says "TDD wins" on disagreements — but here the CODE wins over the TDD).

---

## Depth Assessment

**Expected depth:** Deep (per research-notes; HIGH complexity 0.85; 10 FRs; multi-file).
**Actual depth achieved:** Deep. The research traces exact line anchors for every edit site,
captures verbatim template entries (id-2 eval, FR-4 reviewer pattern), documents the
edge-vs-symbol count reduction, the dual-snapshot grader partition mechanism, the
parse_yaml_simple flat-key constraint, and the MDTM I19/I20/M3 agent-count floors. This exceeds
Standard (file-level + key functions) and meets the Deep bar (data-flow + integration-point +
pattern analysis). Doc-cross-validation (file 03 correcting the TDD's line cites) is a Deep-tier
behavior.
**Missing depth elements:** None material. G1 is the only depth nit (one un-enumerated derived
literal).

---

## VERDICT: PASS

All 7 breadth checks PASS. All 14 TDD §18.2 modification/new sites have research coverage with
a verified current line anchor (or justified content-source for the NEW source-of-truth files).
No critical or important gaps; two MINOR gaps (G1 contract_version :1641 example literal not
enumerated; G2 `cases/` vs `evals/` path — already surfaced by the research and must override
the TDD). The five assigned research files are mutually consistent, evidence-strong, and
Deep-tier. The builder may proceed, carrying G1 and G2 forward as per-item build notes.

### Structured gap list (carry-forward, non-blocking)
1. **G1 (MINOR):** Add a build note — refresh or annotate the `skill_version: "1.5.0"` example
   at SKILL.md:1641 (and confirm :1558 derives automatically) when bumping to 1.6.0. Three
   authoritative gating sites (:663, :804, :1772) are already captured by file 02.
2. **G2 (MINOR, already surfaced):** Builder per-item Output paths for the 5 new eval cases MUST
   be `cases/uc2-*/`, NOT `evals/uc2-*/`. The CODE (verified `ls`) overrides the TDD §18.2 and
   the spawn-prompt framing on this single point.
